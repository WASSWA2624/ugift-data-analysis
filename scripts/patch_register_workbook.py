"""Apply reviewed cell updates without rebuilding a large XLSX workbook.

Only named cells are serialized again; all other worksheet bytes and package
parts are preserved. Expected values make stale or repeated plans fail safely.
This is the lossless assembly step for spreadsheet-tool-authored updates.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import tempfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

ROW = re.compile(rb'<row\b[^>]*?(?:/>|>.*?</row>)', re.S)
ROW_START = re.compile(rb'<row(?=[\s/>]|$)')
CELL = re.compile(rb'<c\b[^>]*?(?:/>|>.*?</c>)', re.S)
REFERENCE = re.compile(r'([A-Z]+)([1-9][0-9]*)\Z')


def worksheet_parts(stream):
    """Yield ordered (is_row, bytes) chunks with at most one XML row buffered."""
    buffer = b''
    while chunk := stream.read(1024 * 1024):
        buffer += chunk
        position = 0
        for match in ROW.finditer(buffer):
            if match.start() > position:
                yield False, buffer[position:match.start()]
            yield True, match.group()
            position = match.end()
        buffer = buffer[position:]
        # Keep an incomplete row; release prefixes/suffixes in bounded chunks.
        start = ROW_START.search(buffer)
        if start is not None and start.start() > 0:
            yield False, buffer[:start.start()]
            buffer = buffer[start.start():]
        elif start is None and len(buffer) > 8:
            yield False, buffer[:-8]
            buffer = buffer[-8:]
    if ROW_START.search(buffer):
        raise ValueError('Incomplete worksheet row')
    if buffer:
        yield False, buffer


def cell_value(cell: bytes | None, shared: list[str]):
    if cell is None:
        return None
    node = ET.fromstring(cell)
    if node.find('f') is not None:
        raise ValueError(f'Cannot overwrite formula {node.get("r")}')
    kind = node.get('t')
    value = node.findtext('v')
    if kind == 'inlineStr':
        return ''.join(part.text or '' for part in node.iter('t'))
    if kind == 's':
        return shared[int(value)] if value is not None else None
    if value is None or kind in {'str', 'e', 'd'}:
        return value
    if kind == 'b':
        return value == '1'
    number = float(value)
    return int(number) if number.is_integer() else number


def cell_xml(reference: str, value, previous: bytes | None, style: int | None = None) -> bytes:
    # Preserve the existing cell attributes, including its number format/fill.
    attrs = dict(ET.fromstring(previous).attrib) if previous else {'r': reference}
    if style is not None:
        attrs['s'] = str(style)
    if value is None:
        attrs.pop('t', None)
        body = ''
    elif isinstance(value, bool):
        attrs['t'] = 'b'
        body = f'<v>{int(value)}</v>'
    elif isinstance(value, (int, float)):
        if not math.isfinite(value):
            raise ValueError('Non-finite spreadsheet value')
        attrs['t'] = 'n'
        body = f'<v>{value}</v>'
    elif isinstance(value, str):
        attrs['t'] = 'inlineStr'
        body = f'<is><t xml:space="preserve">{escape(value)}</t></is>'
    else:
        raise TypeError(f'Unsupported cell value: {type(value).__name__}')
    attributes = ' '.join(f'{name}="{escape(str(content), {chr(34): "&quot;"})}"' for name, content in attrs.items())
    return f'<c {attributes}>{body}</c>'.encode('utf-8')


def column_index(reference: str) -> int:
    result = 0
    for char in REFERENCE.fullmatch(reference).group(1):
        result = result * 26 + ord(char) - 64
    return result


def patch_row(raw: bytes, changes: list[dict], shared: list[str]) -> bytes:
    cells = {ET.fromstring(match.group()).get('r'): match.group() for match in CELL.finditer(raw)}
    if len(cells) != len(CELL.findall(raw)):
        raise ValueError('Duplicate cell references in source row')
    for change in changes:
        row = REFERENCE.fullmatch(change['cell']).group(2)
        for column, expected in change.get('identity', {}).items():
            reference = f'{column}{row}'
            if cell_value(cells.get(reference), shared) != expected:
                raise ValueError(f'{reference}: asset identity does not match reviewed source')
    for change in changes:
        reference = change['cell']
        previous = cells.get(reference)
        actual = cell_value(previous, shared)
        expected = change['expected']
        if actual != expected and not (actual in (None, '') and expected in (None, '')):
            raise ValueError(f'{reference}: expected {expected!r}, found {actual!r}')
        cells[reference] = cell_xml(reference, change['value'], previous, change.get('style'))
    start = raw[:raw.index(b'>') + 1]
    if start.endswith(b'/>'):
        start = start[:-2] + b'>'
    heights = [change['row_height'] for change in changes if 'row_height' in change]
    if heights:
        height = max(heights)
        if not isinstance(height, (int, float)) or not 0 < height <= 409:
            raise ValueError('Invalid reviewed row height')
        start = re.sub(rb'\s+(?:ht|customHeight)="[^"]*"', b'', start)
        start = start[:-1] + f' ht="{height}" customHeight="1">'.encode()
    # Rows in these generated registers contain cells only; do not drop unknown XML.
    content = raw[raw.index(b'>') + 1:raw.rfind(b'</row>')] if b'</row>' in raw else b''
    if CELL.sub(b'', content).strip():
        raise ValueError('Unsupported non-cell content in row')
    return start + b''.join(cells[key] for key in sorted(cells, key=column_index)) + b'</row>'


def apply_updates(source: Path, destination: Path, updates: list[dict]) -> dict:
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError('Use a separate destination; review it before replacement')
    if destination.exists():
        raise FileExistsError(destination)
    grouped = defaultdict(lambda: defaultdict(list))
    seen = set()
    for update in updates:
        reference = REFERENCE.fullmatch(update['cell'])
        if reference is None:
            raise ValueError(f'Invalid cell: {update["cell"]}')
        key = (update['sheet'], update['cell'])
        if key in seen:
            raise ValueError(f'Duplicate update: {key}')
        seen.add(key)
        grouped[update['sheet']][int(reference.group(2))].append(update)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    applied = 0
    try:
        with ZipFile(source) as original:
            ns = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
            rel = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
            relationships = {node.get('Id'): node.get('Target') for node in ET.fromstring(original.read('xl/_rels/workbook.xml.rels'))}
            names = {}
            for sheet in ET.fromstring(original.read('xl/workbook.xml')).find(ns + 'sheets'):
                target = relationships[sheet.get(rel + 'id')]
                names[sheet.get('name')] = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            unknown = set(grouped) - set(names)
            if unknown:
                raise ValueError(f'Unknown sheets: {unknown}')
            by_path = {names[name]: rows for name, rows in grouped.items()}
            shared = []
            if 'xl/sharedStrings.xml' in original.namelist():
                with original.open('xl/sharedStrings.xml') as handle:
                    for _, node in ET.iterparse(handle, events=('end',)):
                        if node.tag == ns + 'si':
                            shared.append(''.join(part.text or '' for part in node.iter(ns + 't')))
                            node.clear()
            with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.register-', suffix='.xlsx', delete=False) as handle:
                temporary = Path(handle.name)
            with ZipFile(temporary, 'w', compression=ZIP_DEFLATED, compresslevel=6) as target:
                for entry in original.infolist():
                    with original.open(entry) as reader, target.open(entry, 'w', force_zip64=True) as writer:
                        if entry.filename not in by_path:
                            shutil.copyfileobj(reader, writer, 1024 * 1024)
                            continue
                        pending = dict(by_path[entry.filename])
                        for is_row, raw in worksheet_parts(reader):
                            if is_row:
                                row = int(re.search(rb'\br="([0-9]+)"', raw[:raw.index(b'>')]).group(1))
                                changes = pending.pop(row, [])
                                if changes:
                                    raw = patch_row(raw, changes, shared)
                                    applied += len(changes)
                            writer.write(raw)
                        if pending:
                            raise ValueError(f'Missing target rows: {sorted(pending)[:10]}')
            with ZipFile(temporary) as check:
                if check.testzip() is not None:
                    raise ValueError('Output ZIP integrity failure')
            if applied != len(updates):
                raise ValueError('Not every update was applied')
            os.replace(temporary, destination)
            return {'updates_applied': applied, 'source': str(source), 'destination': str(destination)}
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--updates', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(apply_updates(args.source, args.out, json.loads(args.updates.read_text(encoding='utf-8'))), indent=2))


if __name__ == '__main__':
    main()
