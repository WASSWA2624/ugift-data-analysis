"""Refresh grouped source files without changing their contents.

The source index is authoritative for existing placements. New sources are routed
using reviewed mappings below and existing exact-content placements. Ambiguous
material stays in an unassigned folder. Run --audit to check historical sources;
run --verify to verify the source and destination hashes of this update.
"""
from __future__ import annotations

import argparse
import atexit
import csv
import hashlib
import io
import json
import re
import subprocess
import tempfile
import zipfile
from functools import lru_cache
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPED = ROOT / 'raw-data-grouped'
SOURCE_ROOTS = ('raw-data-ungrouped', 'new-raw-data-221092026-1114')
SOURCE_COLUMN = 'source (in raw-data-ungrouped)'
DEST_COLUMN = 'destination (in raw-data-grouped)'


_RAR_TEMP_FILES = {}


def _cleanup_rar_temp_files():
    for _, path in _RAR_TEMP_FILES.values():
        try:
            path.unlink()
        except FileNotFoundError:
            pass


atexit.register(_cleanup_rar_temp_files)


def rar_members(data):
    """Return the regular-file entries in a RAR without altering the source."""
    try:
        result = subprocess.run(
            ['tar', '-tvf', str(rar_temp_path(data))],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except FileNotFoundError as error:
        raise RuntimeError('RAR source found, but the system tar/bsdtar reader is unavailable.') from error
    if result.returncode:
        detail = result.stderr.decode(errors='replace').strip()
        raise RuntimeError(f'Could not list RAR source: {detail}')
    members = []
    for line in result.stdout.decode(errors='replace').splitlines():
        fields = line.split(maxsplit=8)
        if len(fields) != 9:
            raise RuntimeError(f'Could not parse RAR member listing: {line}')
        mode, size, name = fields[0], fields[4], fields[8]
        if mode.startswith('d'):
            continue
        members.append((name.replace('\\', '/'), int(size)))
    return members


def rar_temp_path(data):
    """Materialise a cached, read-only RAR copy for the system archive reader."""
    cache_key = id(data)
    cached = _RAR_TEMP_FILES.get(cache_key)
    if cached is not None and cached[0] is data:
        return cached[1]
    with tempfile.NamedTemporaryFile(suffix='.rar', delete=False) as stream:
        stream.write(data)
        path = Path(stream.name)
    # Retaining the bytes object makes the identity key safe from reuse in this process.
    _RAR_TEMP_FILES[cache_key] = (data, path)
    return path


def read_rar_member(data, name):
    """Read one RAR member through bsdtar (`tar` on the supported Windows runtime)."""
    try:
        result = subprocess.run(
            ['tar', '-xOf', str(rar_temp_path(data)), name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except FileNotFoundError as error:
        raise RuntimeError('RAR source found, but the system tar/bsdtar reader is unavailable.') from error
    if result.returncode:
        detail = result.stderr.decode(errors='replace').strip()
        raise RuntimeError(f'Could not read RAR member {name}: {detail}')
    return result.stdout


def walk_rar(data, prefix):
    for name, _ in rar_members(data):
        content = read_rar_member(data, name)
        path = prefix + '::' + name
        yield path, content
        if name.lower().endswith('.zip'):
            try:
                yield from walk_zip(content, path)
            except zipfile.BadZipFile:
                pass
        elif name.lower().endswith('.rar'):
            yield from walk_rar(content, path)


def walk_zip(data, prefix):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            name = member.filename.replace('\\', '/')
            content = archive.read(member)
            path = prefix + '::' + name
            yield path, content
            if name.lower().endswith('.zip'):
                try:
                    yield from walk_zip(content, path)
                except zipfile.BadZipFile:
                    pass
            elif name.lower().endswith('.rar'):
                yield from walk_rar(content, path)


def sources():
    for source_root in SOURCE_ROOTS:
        for path in sorted((ROOT / source_root).rglob('*')):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT / source_root).as_posix()
            if relative.startswith('ugift-team-10-15/tmp/'):
                continue
            content = path.read_bytes()
            yield source_root, relative, content
            if path.suffix.lower() == '.zip':
                try:
                    for member, member_content in walk_zip(content, relative):
                        yield source_root, member, member_content
                except zipfile.BadZipFile:
                    pass
            elif path.suffix.lower() == '.rar':
                for member, member_content in walk_rar(content, relative):
                    yield source_root, member, member_content


def load_index():
    with (GROUPED / '_index.csv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        row.setdefault('source root', 'raw-data-ungrouped')
    return rows


def inventory():
    """List sources without decompressing every historical photo/document."""
    def rar_archive_members(data, prefix):
        for name, size in rar_members(data):
            relative = prefix + '::' + name
            yield relative, size
            if relative.lower().endswith('.zip'):
                try:
                    content = read_rar_member(data, name)
                    yield from archive_members(zipfile.ZipFile(io.BytesIO(content)), relative)
                except zipfile.BadZipFile:
                    pass
            elif relative.lower().endswith('.rar'):
                yield from rar_archive_members(read_rar_member(data, name), relative)

    def archive_members(archive, prefix):
        with archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                relative = prefix + '::' + member.filename.replace('\\', '/')
                yield relative, member.file_size
                if relative.lower().endswith('.zip'):
                    try:
                        yield from archive_members(zipfile.ZipFile(io.BytesIO(archive.read(member))), relative)
                    except zipfile.BadZipFile:
                        pass
                elif relative.lower().endswith('.rar'):
                    yield from rar_archive_members(archive.read(member), relative)
    for source_root in SOURCE_ROOTS:
        for path in sorted((ROOT / source_root).rglob('*')):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT / source_root).as_posix()
            if relative.startswith('ugift-team-10-15/tmp/'):
                continue
            yield source_root, relative, path.stat().st_size
            if path.suffix.lower() == '.zip':
                yield from ((source_root, name, size) for name, size in archive_members(zipfile.ZipFile(path), relative))
            elif path.suffix.lower() == '.rar':
                data = path.read_bytes()
                yield from ((source_root, name, size)
                            for name, size in rar_archive_members(data, relative))


@lru_cache(maxsize=16)
def source_bytes(source_root, relative):
    parts = relative.split('::')
    if len(parts) == 1:
        return (ROOT / source_root / relative).read_bytes()
    container = source_bytes(source_root, '::'.join(parts[:-1]))
    if parts[-2].lower().endswith('.rar'):
        return read_rar_member(container, parts[-1])
    with zipfile.ZipFile(io.BytesIO(container)) as archive:
        return archive.read(parts[-1])


# Reviewed against the master list, document cover/interview fields and the
# supervisor chat of 21-22 September 2026. Multiple folders mean a shared form.
ROUTES = [
    ('depaul - bunyoro, tooro and greater mityana -current', [
        '_multi-team/bunyoro-tooro-greater-mityana',
        'team-30/_team-documents',
    ], 'Updated consolidated register for Teams 29-33; Team 30 copy retained for discoverability.'),
    ('lwamata', ['team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School'], 'Lwamata Town Council Seed Secondary School return; Kiboga local government.'),
    ('sofia health centre', ['team-13/Busia MC/Sofia-Health-Centre-III'], 'Sofia Health Centre III facility return; Busia Municipal Council.'),
    ('img_20260922_0002', ['team-10/Moroto/Rupa-Seed-Secondary-School/_supporting-documents'], 'Rupa Seed Secondary School land-title and boarding-request supporting records.'),
    ('kitayunjwa', ['team-18/Kamuli/Kitayunjwa-Seed-Secondary-School'], 'School named in source and master list.'),
    ('nakitokolo', ['team-32/Wakiso/Nakitokolo-HC-III'], 'Wakiso local government stated on cover.'),
    ('ngomamene', ['team-32/Gomba/Ngomamene-HC-III'], 'Gomba on cover; interview spells facility Ngomenene.'),
    ('mamba', ['team-32/Gomba/Mamba-HC-III'], 'Identity conflict: filename/cover indicate Mamba, Gomba; interview says Kibiri. Review before relying on facility-level findings.'),
    ('matugga', ['team-32/Nansana MC/Matugga-HC-III'], 'Nansana Municipal Council stated on cover (spelled Nasanana).'),
    ('kibiri', ['team-32/Makindye-Ssabagabo MC/Kibiri-HC-III'], 'Kibiri/Makindye-Ssabagabo in filename and interview; toolkit checklist labels Gomba/Mamba. Identity conflict requires review.'),
    ('nyendo', ['team-33/Masaka City/Nyendo-HC-III'], 'Local government and facility identified by source archive and master list.'),
    ('kabatemere', ['team-33/Lyantonde/Kabatemere-HC-III', 'team-33/Lyantonde/Rwamabara-Seed-Secondary-School'], 'Shared source covers Kabatemere HC III and Rwamabara Seed School.'),
    ('lyakajjuka', ['team-33/Lyantonde/Lyakajjuka-HC-III', 'team-33/Lyantonde/Kasagama-Seed-Secondary-School'], 'Shared source covers Lyakajjuka HC III and Kasagama Seed School.'),
    ('wamatovu', ['team-32/Mpigi/Wamatovu-Seed-Secondary-School'], 'Mpigi local government identified in filename and master list.'),
    ('ntwetwe', ['team-29/Kyankwanzi/Ntwetwe-Seed-Secondary-School'], 'School and local government confirmed by source and master list.'),
    ('mpasana', ['team-29/Kakumiro/Christ-the-King-Mpasana-Seed-Secondary-School'], 'School interview names Christ the King Seed School Mpasana; Kakumiro cover.'),
    ('nsambya', ['team-29/Kyankwanzi/Nsambya-Seed-Secondary-School'], 'School interview and Kyankwanzi cover.'),
    ('birembo', ['team-29/Kakumiro/St-Matia-Mulumba-Birembo-Seed-Secondary-School'], 'School interview and Kakumiro cover.'),
]
CHAT_ROUTES = {
    'ASSET VERIFICATION AND RECORDING TOOL KIT 222 (3).docx': (['team-18/Kamuli MC/Busota-HC-III'], 'Supervisor identifies Busota on 21 September 2026 at 16:47; checklist/master use Kamuli MC, although cover says Kamuli district.'),
    'Icheme HC IIII_ASSET VERIFICATION AND RECORDING TOOL KIT.docx': (['team-05/Oyam/Iceme-HC-III'], 'Master-list local government; exact duplicate reuse checked.'),
    'Onywako HC IIII_ASSET VERIFICATION AND RECORDING TOOL KIT.docx': (['team-05/Lira/Onywako-HC-III'], 'Report explicitly says no physical verification; retaining a report does not establish a completed visit.'),
    'data updates - western.xls': (['_multi-team/teams-19-21'], 'Supervisor workbook with records for Buhweju, Mitooma and Mbarara; original retained intact.'),
    'IMG-20260922-WA0000.jpg': (['team-17/Jinja/Buwala-Seed-Secondary-School/_reconciliation-evidence'], 'Master-list screenshot; supervisor 22 September 2026 08:10 says Buwala replaces Butagaya. Not an on-site photograph.'),
    'IMG-20260922-WA0001.jpg': (['team-17/Namayingo/Mutumba-Seed-Secondary-School/_reconciliation-evidence'], 'Master-list screenshot; supervisor 22 September 2026 08:10 says Mutumba replaces Mwema. Not an on-site photograph.'),
}
CHAT_NAME = 'WhatsApp Chat with DATA MANAGEMENT UGIFT.zip'
WEMIS_RAR = ('ugift-team-10-15/source-documents/All WIP Ugift.zip::'
             'All WIP Ugift/WEMIS DISTRICT EQUIPMENT.rar')
WEMIS_RAR_NOTE = ('Programme-level WEMIS tablet, desktop and UPS handover records by district; '
                  'reviewed page by page and found not to identify facility returns.')


def route(relative):
    basename = relative.split('::')[-1].split('/')[-1]
    if relative == CHAT_NAME or f'/{CHAT_NAME}' in relative:
        if basename in CHAT_ROUTES:
            return CHAT_ROUTES[basename]
        return ['_multi-team/programme-documents/data-management-chat'], 'Supervisor discussion and source archive retained for reconciliation decisions.'
    team_archive = re.search(
        r'UGIFT DEPAUL\.zip::UGIFT DEPAUL/TEAM\s+(25\s*&\s*30|\d+)',
        relative,
        re.I,
    )
    if team_archive:
        team_label = team_archive.group(1)
        team_numbers = (25, 30) if '&' in team_label else (int(team_label),)
        return (
            [f'team-{number:02d}/_team-documents' for number in team_numbers],
            f'Archive member filed under Team {team_label}; retained as team-level evidence pending facility-specific indexing.',
        )
    for token, folders, note in ROUTES:
        if token in basename.lower():
            if token == 'kibiri' and basename == 'KIBIRI HC III report.docx':
                note = 'Kibiri process report; Makindye-Ssabagabo local government.'
            return folders, note
    return ['_multi-team/_unassigned'], 'No reviewed facility mapping; retained for follow-up without guessing.'


def update():
    rows = load_index()
    original_count = len(rows)
    by_source = defaultdict(list)
    by_basename = defaultdict(list)
    for row in rows:
        if (row['source root'] == 'raw-data-ungrouped'
                and row[SOURCE_COLUMN] == WEMIS_RAR):
            row['note'] = WEMIS_RAR_NOTE
        by_source[row['source root'], row[SOURCE_COLUMN]].append(row)
        if row[DEST_COLUMN] and row['status'] in ('placed', 'duplicate'):
            by_basename[Path(row[DEST_COLUMN]).name].append(row)
    hashes = {}
    def file_hash(relative):
        if relative not in hashes:
            path = GROUPED / relative
            hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        return hashes[relative]
    changed_files, new_facilities, unresolved = [], set(), []
    def place(data, folder, basename):
        target_folder = GROUPED / folder
        existed = target_folder.is_dir()
        target_folder.mkdir(parents=True, exist_ok=True)
        if not existed and folder.startswith('team-') and len(Path(folder).parts) == 3:
            new_facilities.add(folder)
        digest = hashlib.sha256(data).hexdigest()
        # Identical material is stored once within each destination folder.
        for candidate in target_folder.iterdir():
            if candidate.is_file() and candidate.stat().st_size == len(data):
                destination = candidate.relative_to(GROUPED).as_posix()
                if file_hash(destination) == digest:
                    return destination, 'duplicate'
        candidate = target_folder / basename
        suffix = 2
        while candidate.exists():
            candidate = target_folder / f'{Path(basename).stem} ({suffix}){Path(basename).suffix}'
            suffix += 1
        # New files are independent copies: never overwrite or edit a hardlink.
        candidate.write_bytes(data)
        destination = candidate.relative_to(GROUPED).as_posix()
        hashes[destination] = digest
        changed_files.append(destination)
        return destination, 'placed'
    # Earlier runs placed previously unseen sources in _unassigned. Reapply the
    # reviewed routing rules so newly classified archive and chat material moves
    # into the relevant evidence area without altering bytes.
    obsolete_unassigned = set()
    migrated_rows = 0
    for row in list(rows):
        relative = row[SOURCE_COLUMN]
        old_destination = row[DEST_COLUMN]
        if not (
            row['source root'] == 'new-raw-data-221092026-1114'
            and old_destination.startswith('_multi-team/_unassigned/')
        ):
            continue
        folders, note = route(relative)
        if folders == ['_multi-team/_unassigned']:
            continue
        data = source_bytes(row['source root'], relative)
        placements = [place(data, folder, Path(old_destination).name) for folder in folders]
        obsolete_unassigned.add(old_destination)
        row[DEST_COLUMN], row['status'] = placements[0]
        row['note'] = note
        for destination, status in placements[1:]:
            extra_row = dict(row)
            extra_row[DEST_COLUMN] = destination
            extra_row['status'] = status
            rows.append(extra_row)
        migrated_rows += 1
    for source_root, relative, _ in inventory():
        key = source_root, relative
        if key in by_source:
            continue
        data = source_bytes(source_root, relative)
        digest = hashlib.sha256(data).hexdigest()
        basename = relative.split('::')[-1].split('/')[-1]
        if basename.startswith('~$') or basename.lower().endswith('.py'):
            new_rows = [{DEST_COLUMN: '', 'status': 'skipped', 'note': 'Office lock file or working script; not facility data.'}]
        elif relative.startswith(WEMIS_RAR + '::'):
            new_rows = [{DEST_COLUMN: '', 'status': 'in-archive', 'note': WEMIS_RAR_NOTE}]
        elif basename.lower().endswith(('.zip', '.rar')) and relative != CHAT_NAME:
            new_rows = [{DEST_COLUMN: '', 'status': 'extracted', 'note': 'Archive contents indexed individually.'}]
        else:
            prior_rows = by_source.get(('raw-data-ungrouped', relative), []) if source_root != 'raw-data-ungrouped' else []
            prior_destinations = [r[DEST_COLUMN] for r in prior_rows if r[DEST_COLUMN] and r['status'] in ('placed', 'duplicate') and file_hash(r[DEST_COLUMN]) == digest]
            # Reuse exact matches from the prior index, retaining all placements
            # for a single document that covers several facilities.
            if not prior_destinations:
                prior_destinations = sorted({r[DEST_COLUMN] for r in by_basename[basename] if file_hash(r[DEST_COLUMN]) == digest})
            if prior_destinations:
                new_rows = [{DEST_COLUMN: d, 'status': 'duplicate', 'note': 'Byte-identical to existing grouped source; original placement retained.'} for d in prior_destinations]
            else:
                folders, note = route(relative)
                new_rows = []
                if folders == ['_multi-team/_unassigned']:
                    unresolved.append({'source root': source_root, 'source': relative})
                for folder in folders:
                    destination, status = place(data, folder, basename)
                    new_rows.append({DEST_COLUMN: destination, 'status': status, 'note': note})
        for row in new_rows:
            row.update({SOURCE_COLUMN: relative, 'source root': source_root, 'sha256': digest})
            rows.append(row)
            by_source[key].append(row)
            if row[DEST_COLUMN] and row['status'] in ('placed', 'duplicate'):
                by_basename[Path(row[DEST_COLUMN]).name].append(row)
    referenced_destinations = {row[DEST_COLUMN] for row in rows if row[DEST_COLUMN]}
    removed_orphans = []
    for destination in sorted(obsolete_unassigned - referenced_destinations):
        target = (GROUPED / destination).resolve()
        unassigned_root = (GROUPED / '_multi-team' / '_unassigned').resolve()
        if target.is_file() and target.parent == unassigned_root:
            target.unlink()
            removed_orphans.append(destination)
    fields = [SOURCE_COLUMN, DEST_COLUMN, 'status', 'note', 'source root', 'sha256']
    staging = GROUPED / '_index.csv.new'
    with staging.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    staging.replace(GROUPED / '_index.csv')
    result = {'index_rows_before': original_count, 'index_rows_after': len(rows),
              'new_index_rows': len(rows) - original_count, 'new_files': changed_files,
              'migrated_archive_rows': migrated_rows, 'removed_orphans': removed_orphans,
              'new_facilities': sorted(new_facilities), 'unresolved': unresolved,
              'status_counts': dict(Counter(r['status'] for r in rows)),
              'root_counts': dict(Counter(r['source root'] for r in rows))}
    output = ROOT / 'tmp' / 'grouping-update-summary.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({
        key: len(value) if isinstance(value, list) else value
        for key, value in result.items()
    }, indent=2))


def audit():
    rows = load_index()
    by_source = {(row['source root'], row[SOURCE_COLUMN]): row for row in rows}
    unseen, changed, missing = [], [], []
    seen = set()
    destination_hashes = {}
    for source_root, relative, content in sources():
        key = source_root, relative
        seen.add(key)
        digest = hashlib.sha256(content).hexdigest()
        row = by_source.get(key)
        if row is None:
            unseen.append({'root': source_root, 'source': relative,
                           'size': len(content), 'sha256': digest})
        elif row['status'] in ('placed', 'duplicate'):
            destination = row[DEST_COLUMN]
            if destination not in destination_hashes:
                target = GROUPED / destination
                destination_hashes[destination] = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
            if destination_hashes[destination] != digest:
                changed.append({'root': source_root, 'source': relative,
                                'destination': destination, 'size': len(content),
                                'sha256': digest, 'previous_sha256': destination_hashes[destination]})
    for key, row in by_source.items():
        if key not in seen:
            missing.append(row)
    result = {'new': unseen, 'changed': changed, 'missing_indexed_sources': missing,
              'source_entry_count': len(seen), 'prior_index_entry_count': len(rows)}
    output = ROOT / 'tmp' / 'grouping-audit.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({key: len(value) if isinstance(value, list) else value for key, value in result.items()}, indent=2))
    print('New source types:', Counter(Path(item['source']).suffix.lower() for item in unseen))
    print('New top-level sources:', Counter((item['root'], item['source'].split('::')[0]) for item in unseen))
    print('Changed sources:', json.dumps(changed, indent=2))


def verify():
    rows = load_index()
    sources_checked = set()
    destinations_checked = set()
    problems = []
    for row in rows:
        if not row.get('sha256'):
            continue
        key = row['source root'], row[SOURCE_COLUMN]
        if key not in sources_checked:
            if hashlib.sha256(source_bytes(*key)).hexdigest() != row['sha256']:
                problems.append({'source': key, 'error': 'source content changed'})
            sources_checked.add(key)
        destination = row[DEST_COLUMN]
        if destination and row['status'] in ('placed', 'duplicate'):
            target = GROUPED / destination
            if not target.is_file():
                problems.append({'destination': destination, 'error': 'missing destination'})
            elif hashlib.sha256(target.read_bytes()).hexdigest() != row['sha256']:
                problems.append({'destination': destination, 'error': 'content differs from source'})
            destinations_checked.add(destination)
    result = {'sources_checked': len(sources_checked), 'destinations_checked': len(destinations_checked), 'problems': problems}
    (ROOT / 'tmp' / 'grouping-verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    if problems:
        raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit', action='store_true')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    if args.update:
        update()
    elif args.verify:
        verify()
    else:
        audit()
