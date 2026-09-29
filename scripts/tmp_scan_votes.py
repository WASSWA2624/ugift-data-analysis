"""Locate KCCA and MODV rows in the three asset-register workbooks."""
from __future__ import annotations

import re
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(r"D:\coding\ugift-data-analysis\outputs\asset-register")
CELL = re.compile(br'<c r="([A-Z]+)(\d+)"[^>]*>(.*?)</c>')


def iter_rows(sheet):
    pending = b""
    while chunk := sheet.read(4 * 1024 * 1024):
        pending += chunk
        boundary = pending.rfind(b"</row>")
        if boundary < 0:
            continue
        boundary += len(b"</row>")
        complete, pending = pending[:boundary], pending[boundary:]
        yield from re.finditer(br"<row\b[^>]*>.*?</row>", complete, re.DOTALL)
    if pending:
        yield from re.finditer(br"<row\b[^>]*>.*?</row>", pending, re.DOTALL)


def scan_shared(path: Path, targets: dict[bytes, str]) -> None:
    cols: Counter = Counter()
    rows: dict[str, list[int]] = {label: [] for label in targets.values() if label.endswith("BK")}
    with zipfile.ZipFile(path) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        for match in iter_rows(sheet):
            row_xml = match.group(0)
            for cell in CELL.finditer(row_xml):
                value = re.search(br"<v>(\d+)</v>", cell.group(3))
                if value is None or value.group(1) not in targets:
                    continue
                label = targets[value.group(1)]
                cols[(label, cell.group(1).decode())] += 1
                if label.endswith("BK") and cell.group(1) == b"A":
                    rows[label].append(int(cell.group(2)))
    print(path.name, "cols", dict(cols))
    for label, numbers in rows.items():
        numbers.sort()
        contiguous = numbers == list(range(numbers[0], numbers[-1] + 1)) if numbers else None
        print(label, "n", len(numbers), "min", numbers[:3], "max", numbers[-3:], "contiguous", contiguous)


def scan_inline(path: Path, column: bytes, needles: dict[bytes, str]) -> None:
    hits: dict[str, list[int]] = {label: [] for label in needles.values()}
    with zipfile.ZipFile(path) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        for match in iter_rows(sheet):
            row_xml = match.group(0)
            for cell in CELL.finditer(row_xml):
                if cell.group(1) != column:
                    continue
                text = cell.group(3)
                for needle, label in needles.items():
                    if needle in text:
                        hits[label].append(int(cell.group(2)))
    print(path.name)
    for label, numbers in hits.items():
        numbers.sort()
        contiguous = numbers == list(range(numbers[0], numbers[-1] + 1)) if numbers else None
        print(" ", label, "n", len(numbers), "min", numbers[:3], "max", numbers[-3:], "contiguous", contiguous)


def main() -> None:
    scan_shared(
        ROOT / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        {b"413971": "KCCA BK", b"413973": "KCCA", b"420411": "MODV BK", b"420413": "MODV"},
    )
    scan_inline(
        ROOT / "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        b"A",
        {b"KCCA BK": "KCCA BK", b"MODV BK": "MODV BK"},
    )
    scan_inline(
        ROOT / "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx",
        b"P",
        {
            b"Kampala Capital City Authority": "KCCA",
            b"Ministry of Defence": "MODV",
            b"Ministry of Defense": "MODV-us",
        },
    )


if __name__ == "__main__":
    main()
