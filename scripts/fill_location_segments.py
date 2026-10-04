"""Fill location segments that the row or the location master already names.

LOCATION_SEGMENT4 stays UNSPECIFIED: every combination in Location(3)2.xlsx
ends with that segment. A ministry row with no named department or site keeps
UNSPECIFIED. A named blood bank, Finance Building, or a recorded department
that matches one master department for that vote is written in.
"""
from __future__ import annotations

import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drop_referral_hospitals_and_ubts import SheetReader, column_value, shared_labels
from patch_register_workbook import apply_updates

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "outputs" / "asset-register" / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
MASTER = ROOT / "Location(3)2.xlsx"
SHEET = "Asset Register"
DEPT = re.compile(r"Recorded department/room:\s*([^;]+)")
BANKS = {
    "HOIMA RBB BK": "Hoima Regional Blood Bank",
    "ARUA RBB BK": "Arua Regional Blood Bank",
    "SOROTI RBB BK": "Soroti Regional Blood Bank",
}
ALIASES = {
    "engineering": "HEALTH INFRASTRUCTURE",
    "district administration": "ADMINISTRATION AND MANAGEMENT",
}
# Official department names checked against the institution's own site, used when the
# location master has no matching department. Sources: molg.go.ug (District Administration),
# Ministry of Health strategic plan and the National RBF Unit (Planning, Financing and Policy),
# ppda.go.ug (Strategy and Planning), nema.go.ug (Office of the Executive Director).
OFFICIAL = {
    ("MOLG", "district administration"): "DISTRICT ADMINISTRATION",
    ("MOH", "rbf"): "PLANNING, FINANCING AND POLICY",
    ("PPDA", "strategy planning"): "STRATEGY AND PLANNING",
    ("NEMA", "exective directors office"): "OFFICE OF THE EXECUTIVE DIRECTOR",
    ("NEMA", "executive directors office"): "OFFICE OF THE EXECUTIVE DIRECTOR",
}


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def master_departments() -> dict[str, set[str]]:
    import openpyxl
    book = openpyxl.load_workbook(MASTER, read_only=True, data_only=True)
    found: dict[str, set[str]] = defaultdict(set)
    for index, row in enumerate(book.active.iter_rows(values_only=True)):
        if index == 0 or not row or not row[0]:
            continue
        parts = re.split(r"(?<!\\)-", str(row[0]))
        if len(parts) < 2:
            continue
        department = parts[1].strip()
        if department and department.upper() != "UNSPECIFIED":
            found[parts[0].strip()].add(department)
    book.close()
    return found


def departments_for(segment1: str, departments: dict[str, set[str]]) -> set[str]:
    if segment1 in departments:
        return departments[segment1]
    token = segment1.replace("\\-", " ").split()[0].upper()
    matches = [name for name in departments if name.upper().startswith(token)]
    if len(matches) == 1:
        return departments[matches[0]]
    return set()


def department_name(recorded: str, segment1: str, choices: set[str]) -> str:
    if not recorded:
        return ""
    vote = segment1.replace("\\-", " ").split()[0].upper()
    official = OFFICIAL.get((vote, norm(recorded)))
    if official:
        return official
    if not choices:
        return ""
    folded = {norm(choice): choice for choice in choices}
    exact = folded.get(norm(recorded))
    if exact:
        return exact
    alias = ALIASES.get(norm(recorded))
    if alias and norm(alias) in folded:
        return folded[norm(alias)]
    return ""


def updates_for(row_number: int, segment2: str, segment3: str, attribute: str, book: str, segment1: str, recorded: str, departments: dict[str, set[str]]) -> list[dict]:
    changes = []
    if segment3 == "UNSPECIFIED" and book in BANKS:
        changes.append(("K", BANKS[book]))
    elif segment3 == "UNSPECIFIED" and norm(recorded) == "finance building":
        changes.append(("K", "Finance Building"))
    if segment2 == "UNSPECIFIED":
        department = department_name(recorded, segment1, departments_for(segment1, departments))
        if department:
            changes.append(("J", department))
            if attribute == "UNSPECIFIED":
                changes.append(("AY", department))
    return [
        {"sheet": SHEET, "cell": f"{column}{row_number}", "expected": "UNSPECIFIED", "value": value}
        for column, value in changes
    ]


def main() -> None:
    departments = master_departments()
    labels = shared_labels(REF)
    updates = []
    summary: dict[str, int] = defaultdict(int)
    rows = 0
    with zipfile.ZipFile(REF) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        reader = SheetReader(sheet)
        reader.take_until(b"<sheetData")
        reader.take_until(b">")
        while row := reader.next_row():
            rows += 1
            if rows == 1:
                continue
            segment2 = column_value(row, b"J", labels)
            segment3 = column_value(row, b"K", labels)
            if segment2 != "UNSPECIFIED" and segment3 != "UNSPECIFIED":
                continue
            remarks = column_value(row, b"BL", labels)
            recorded = DEPT.search(remarks)
            planned = updates_for(
                rows, segment2, segment3, column_value(row, b"AY", labels),
                column_value(row, b"A", labels), column_value(row, b"I", labels),
                recorded.group(1).strip() if recorded else "", departments,
            )
            for change in planned:
                summary[f"{change['cell'][:1]}={change['value']}"] += 1
            updates.extend(planned)
    print(f"rows {rows - 1:,} updates {len(updates):,}", flush=True)
    for key, count in sorted(summary.items()):
        print(f"  {count:,} {key}", flush=True)
    if not updates:
        return
    destination = REF.with_suffix(".location-tmp.xlsx")
    if destination.exists():
        destination.unlink()
    apply_updates(REF, destination, updates)
    destination.replace(REF)
    print("applied", flush=True)


if __name__ == "__main__":
    main()
