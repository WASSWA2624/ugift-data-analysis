"""Replace dotted placeholder names with the facility named by the source file.

A form heading such as '…...............DISTRICT LOCAL GOVERNMENT' has no
name. The source path on the same row does.
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_guideline_registers import facility_name
from fill_gou_template import book_code, location_segment1

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "outputs" / "asset-register" / "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx",
    ROOT / "outputs" / "asset-register" / "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
    ROOT / "outputs" / "asset-register" / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
]
LEADER = re.compile(r"^(?:&#8230;|\u2026|\.{3,})+")
GENERIC_LG = re.compile(r"(?i)^district(\s+lo+c+a+l+\s+government)?$")
GENERIC_FACILITY = re.compile(r"(?i)^health\s+cent(?:re|er)(?:\s+iii|\s+3)?$")
PATH = re.compile(r"team-\d+/([^/<]+)/([^/<]+)/")
TEXT = re.compile(r"<t([^>]*)>(.*?)</t>", re.S)


def xml_escape(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def visible(value: str) -> str:
    text = value.replace("&#8230;", " ").replace("\u2026", " ")
    text = re.sub(r"[.\u2024\u2025]{2,}", " ", text)
    return re.sub(r"\s+", " ", text).strip(" .")


def from_path(row: str) -> tuple[str, str]:
    found = PATH.search(row)
    if not found:
        return "", ""
    local = found.group(1).replace("-", " ")
    slug = found.group(2).replace("-", " ")
    kind = "Health centre" if re.search(r"(?i)\bhc\b|health", slug) else "School" if re.search(r"(?i)seed|school", slug) else ""
    return local, facility_name(slug, kind)


def reconstruct(value: str, local: str, facility: str) -> str:
    if not LEADER.match(value):
        return value
    kind = "book" if re.search(r"(?i)\sBK$", value.strip()) else ""
    if not kind and re.search(r"(?i)\s(DLG|MC|CITY)$", value.strip()):
        kind = "vote"
    cleaned = visible(value)
    cleaned = re.sub(r"(?i)\s+(BK|DLG|MC|CITY)$", "", cleaned).strip()
    if GENERIC_LG.match(cleaned):
        chosen = local
    elif GENERIC_FACILITY.match(cleaned):
        chosen = facility
    else:
        chosen = facility_name(cleaned, "Health centre" if re.search(r"(?i)health|\bhc\b", cleaned) else "")
        if not chosen:
            chosen = cleaned
    if not chosen:
        return ""
    if kind == "book":
        return book_code(chosen) or chosen
    if kind == "vote":
        return location_segment1(chosen) or chosen
    return chosen


def repair_row(row: bytes) -> bytes:
    text = row.decode("utf-8")
    if "&#8230;" not in text and "…..." not in text and "....." not in text:
        return row
    local, facility = from_path(text)

    def replace(match: re.Match[str]) -> str:
        rebuilt = reconstruct(match.group(2), local, facility)
        if rebuilt == match.group(2):
            return match.group(0)
        return f"<t{match.group(1)}>{xml_escape(rebuilt)}</t>"

    return TEXT.sub(replace, text).encode("utf-8")


def repair(path: Path) -> tuple[int, int]:
    if not path.is_file():
        print(f"missing {path}", flush=True)
        return 0, 0
    temporary = path.with_suffix(".repair.xlsx")
    changed = 0
    rows = 0
    with zipfile.ZipFile(path) as source, zipfile.ZipFile(
        temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6
    ) as target:
        sheet = source.read("xl/worksheets/sheet1.xml")
        pieces = []
        cursor = 0
        while True:
            start = sheet.find(b"<row ", cursor)
            if start < 0:
                pieces.append(sheet[cursor:])
                break
            if start > cursor:
                pieces.append(sheet[cursor:start])
            end = sheet.find(b"</row>", start)
            row = sheet[start:end + 6]
            new = repair_row(row)
            if new != row:
                changed += 1
            pieces.append(new)
            rows += 1
            cursor = end + 6
            if rows % 100000 == 0:
                print(f"{path.name} {rows:,} rows, {changed:,} repaired", flush=True)
        for item in source.infolist():
            if item.filename != "xl/worksheets/sheet1.xml":
                target.writestr(item, source.read(item.filename))
        target.writestr("xl/worksheets/sheet1.xml", b"".join(pieces))
    temporary.replace(path)
    print(f"repaired {changed:,} of {rows:,} in {path.name}", flush=True)
    return rows, changed


def main() -> None:
    for path in TARGETS:
        repair(path)


if __name__ == "__main__":
    main()
