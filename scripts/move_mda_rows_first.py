"""Put central-government (MDA) rows above local-government rows.

Order inside each group stays as it is. Cell values, formatting and the other
workbook parts are unchanged. Only row numbers and cell references move.
"""

from __future__ import annotations

import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fill_register_gaps import load_strings
from patch_register_workbook import cell_value, worksheet_parts
from ugift_places import MDA_VOTES

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "outputs" / "asset-register" / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
SHEET = "xl/worksheets/sheet1.xml"
MDA_BOOKS = {f"{code} BK" for code, _display, _pattern in MDA_VOTES}
A_CELL = re.compile(rb'<c r="A(\d+)"([^>]*?)(?:/>|>(.*?)</c>)', re.S)
CELL_REF = re.compile(rb'r="([A-Z]+)(\d+)"')


def book_code(raw: bytes, shared: list[str]) -> str:
    match = A_CELL.search(raw)
    if not match:
        return ""
    value = cell_value(match.group(0), shared)
    return str(value or "").strip()


def renumber(raw: bytes, new: int) -> bytes:
    old = re.match(rb'<row r="(\d+)"', raw).group(1)
    if int(old) == new:
        return raw
    new_text = str(new).encode()

    def replace(match: re.Match[bytes]) -> bytes:
        if match.group(2) != old:
            return match.group(0)
        return b'r="' + match.group(1) + new_text + b'"'

    raw = CELL_REF.sub(replace, raw)
    return raw.replace(b'<row r="' + old + b'"', b'<row r="' + new_text + b'"', 1)


def write_record(handle, raw: bytes) -> None:
    handle.write(len(raw).to_bytes(4, "little"))
    handle.write(raw)


def read_records(path: Path):
    with path.open("rb") as handle:
        while length := handle.read(4):
            yield handle.read(int.from_bytes(length, "little"))


def main() -> None:
    temp = ROOT / "outputs" / "asset-register"
    mda_path = temp / ".mda-rows.bin"
    rest_path = temp / ".other-rows.bin"
    counts = Counter()
    header = b""
    preamble = b""
    suffix = b""
    seen_row = False
    print("splitting", flush=True)
    with zipfile.ZipFile(REF) as workbook, mda_path.open("wb") as mda_file, rest_path.open("wb") as rest_file:
        shared = load_strings(workbook.read("xl/sharedStrings.xml"))
        stream = workbook.open(SHEET)
        for is_row, raw in worksheet_parts(stream):
            if not is_row:
                if seen_row:
                    suffix += raw
                else:
                    preamble += raw
                continue
            seen_row = True
            number = int(re.match(rb'<row r="(\d+)"', raw).group(1))
            if number == 1:
                header = raw
                continue
            code = book_code(raw, shared)
            if code in MDA_BOOKS:
                write_record(mda_file, raw)
                counts[code] += 1
                counts["mda"] += 1
            else:
                write_record(rest_file, raw)
                counts["other"] += 1
        stream.close()
    print(f"mda {counts['mda']:,} other {counts['other']:,}", flush=True)
    for code, count in sorted(counts.items()):
        if code not in {"mda", "other"}:
            print(f"{count}\t{code}")
    if not counts["mda"]:
        raise SystemExit("No MDA rows found")
    destination = REF.with_name(REF.stem + ".ordered.xlsx")
    if destination.exists():
        destination.unlink()
    print("writing", flush=True)
    with zipfile.ZipFile(REF) as original, zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as target:
        for entry in original.infolist():
            if entry.filename == SHEET:
                with target.open(SHEET, "w", force_zip64=True) as sheet:
                    sheet.write(preamble)
                    sheet.write(header)
                    number = 2
                    for raw in read_records(mda_path):
                        sheet.write(renumber(raw, number))
                        number += 1
                    mda_end = number
                    for raw in read_records(rest_path):
                        sheet.write(renumber(raw, number))
                        number += 1
                    sheet.write(suffix)
                if number - 2 != counts["mda"] + counts["other"]:
                    raise SystemExit("Row count changed")
            else:
                target.writestr(entry, original.read(entry.filename))
    print("checking", flush=True)
    with zipfile.ZipFile(destination) as workbook:
        if workbook.testzip() is not None:
            raise SystemExit("Zip check failed")
        shared = load_strings(workbook.read("xl/sharedStrings.xml"))
        stream = workbook.open(SHEET)
        seen_other = False
        checked = 0
        for is_row, raw in worksheet_parts(stream):
            if not is_row:
                continue
            number = int(re.match(rb'<row r="(\d+)"', raw).group(1))
            if number == 1:
                continue
            code = book_code(raw, shared)
            is_mda = code in MDA_BOOKS
            if is_mda and seen_other:
                raise SystemExit(f"MDA row after a local-government row at {number}")
            if not is_mda:
                seen_other = True
            if number != checked + 2:
                raise SystemExit(f"Row number gap at {number}")
            checked += 1
        stream.close()
    if checked != counts["mda"] + counts["other"]:
        raise SystemExit("Verification count mismatch")
    destination.replace(REF)
    mda_path.unlink(missing_ok=True)
    rest_path.unlink(missing_ok=True)
    print(f"wrote {REF} mda_rows {counts['mda']:,} first_local_government_row {mda_end}")


if __name__ == "__main__":
    main()
