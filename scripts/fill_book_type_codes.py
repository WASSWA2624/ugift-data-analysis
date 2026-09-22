"""Populate BOOK_TYPE_CODE and FACILITY_NAME in the UgIFT asset register.

BOOK_TYPE_CODE follows the supplied sample row:
  LOCATION_SEGMENT1 ``MADI\\-OKOLLO DLG`` -> ``MADI OKOLLO BK``

FACILITY_NAME is inserted immediately after BOOK_TYPE_CODE. Reconciled
facility names take precedence; the Source Lines facility/location value is
used when no reconciliation name exists. Obvious serial/tag-only values are
not treated as facility names.

The script also keeps the AssetRegister Excel table definition synchronized
with the added column. A worksheet/table column-count mismatch is treated by
Excel as corrupt workbook content.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import subprocess
from copy import copy
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import TableColumn

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = ROOT / "outputs" / "asset-register-2026-09-22" / "UgIFT Asset Register.xlsx"
RECONCILIATION_PATH = ROOT / "raw-data-grouped" / "facility-reconciliation.csv"
GIT_WORKBOOK_PATH = "outputs/asset-register-2026-09-22/UgIFT Asset Register.xlsx"

SUFFIX_RULES = (
    (" DISTRICT LOCAL GOV'T", ""),
    (" DISTRICT LOCAL GOVT", ""),
    (" DISTRICT LOCAL GOVERNMENT", ""),
    (" MUNICIPAL COUNCIL", " MC"),
    (" DISTRICT LG", ""),
    (" LOCAL GOVERNMENT", ""),
    (" DISTRICT", ""),
    (" DLG", ""),
    (" LG", ""),
)


def normalized_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).replace("\\", "").replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


def to_book(location: object) -> str | None:
    text = normalized_text(location).upper()
    if not text:
        return None
    for old, new in SUFFIX_RULES:
        if text.endswith(old):
            text = (text[: -len(old)] + new).strip()
            break
    if not text:
        return None
    return text if text.endswith(" BK") else f"{text} BK"


def load_reconciliation() -> tuple[dict[str, str], set[str]]:
    facility_by_id: dict[str, str] = {}
    local_governments: set[str] = set()
    with RECONCILIATION_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            facility_id = (row.get("id") or "").strip()
            facility = (row.get("field_name") or row.get("name") or "").strip()
            local_government = normalized_text(row.get("lg")).casefold()
            if facility_id and facility:
                facility_by_id.setdefault(facility_id, facility)
            if local_government:
                local_governments.add(local_government)
    return facility_by_id, local_governments


def usable_source_facility(value: object, local_governments: set[str]) -> str | None:
    facility = normalized_text(value)
    if not facility:
        return None
    compact = re.sub(r"[^A-Za-z0-9]", "", facility)
    if " " not in facility and len(compact) >= 10 and any(ch.isdigit() for ch in compact):
        return None
    if facility.casefold() in local_governments:
        return None
    return facility


def source_maps(
    ws_source,
    reconciled_facilities: dict[str, str],
    local_governments: set[str],
) -> tuple[dict[int, str], dict[int, str], int]:
    """Map Asset Register row number to supported LG and facility names."""
    headers = [cell.value for cell in next(ws_source.iter_rows(min_row=1, max_row=1))]
    index = {name: i for i, name in enumerate(headers)}
    lg_by_row: dict[int, str] = {}
    facility_by_row: dict[int, str] = {}
    rejected_identifier_values = 0

    for row in ws_source.iter_rows(min_row=2, values_only=True):
        first = row[index["Register first row"]]
        last = row[index["Register last row"]]
        if first is None or last is None:
            continue

        facility_id = normalized_text(row[index["Facility ID"]])
        source_facility = usable_source_facility(
            row[index["Facility / location"]], local_governments
        )
        if row[index["Facility / location"]] and not source_facility:
            rejected_identifier_values += 1
        facility = reconciled_facilities.get(facility_id) or source_facility
        local_government = normalized_text(row[index["Local government / MDA"]])

        for register_row in range(int(first), int(last) + 1):
            if local_government and register_row not in lg_by_row:
                lg_by_row[register_row] = local_government
            if facility and register_row not in facility_by_row:
                facility_by_row[register_row] = facility

    return lg_by_row, facility_by_row, rejected_identifier_values


def shift_column_dimensions_for_insert(ws, insert_at: int) -> None:
    """Shift explicitly configured column dimensions one column to the right."""
    captured = {}
    for column_index in range(insert_at, ws.max_column + 1):
        letter = get_column_letter(column_index)
        if letter in ws.column_dimensions:
            captured[column_index] = copy(ws.column_dimensions[letter])

    for column_index in captured:
        del ws.column_dimensions[get_column_letter(column_index)]

    for column_index, dimension in captured.items():
        destination = get_column_letter(column_index + 1)
        dimension.index = destination
        dimension.min = column_index + 1
        dimension.max = column_index + 1
        ws.column_dimensions[destination] = dimension


def ensure_facility_column(ws) -> tuple[int, bool]:
    """Insert FACILITY_NAME after BOOK_TYPE_CODE when missing."""
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    if len(headers) > 1 and headers[0] == "BOOK_TYPE_CODE" and headers[1] == "FACILITY_NAME":
        return 2, False
    if "FACILITY_NAME" in headers:
        return headers.index("FACILITY_NAME") + 1, False

    shift_column_dimensions_for_insert(ws, 2)
    ws.insert_cols(2)
    ws.cell(1, 2).value = "FACILITY_NAME"
    ws.cell(1, 2)._style = copy(ws.cell(1, 1)._style)
    ws.column_dimensions["B"].width = 32
    return 2, True


def synchronize_asset_table(ws) -> None:
    """Synchronize the table range and column metadata with worksheet headers."""
    table = ws.tables["AssetRegister"]
    headers = [ws.cell(1, column).value for column in range(1, ws.max_column + 1)]

    if len(table.tableColumns) == ws.max_column - 1 and headers[1] == "FACILITY_NAME":
        table.tableColumns.insert(1, TableColumn(id=2, name="FACILITY_NAME"))
    if len(table.tableColumns) != ws.max_column:
        raise ValueError(
            f"AssetRegister has {len(table.tableColumns)} table columns but "
            f"the worksheet has {ws.max_column} columns"
        )

    for column_number, (column, header) in enumerate(zip(table.tableColumns, headers), 1):
        column.id = column_number
        column.name = str(header)

    table.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
    if table.autoFilter is not None:
        table.autoFilter.ref = table.ref


def update_read_me(ws) -> None:
    replacements = {
        "Template": (
            "The Asset Register sheet preserves the supplied template fields and adds "
            "FACILITY_NAME immediately after BOOK_TYPE_CODE, for 65 columns in total. "
            "The illustrative laptop row was removed."
        ),
        "Missing information": (
            "Unsupported information remains genuinely blank. Transaction-dependent "
            "account segments, employee numbers, unidentified tags, incomplete dates "
            "and unestablished values are not copied from the sample. BOOK_TYPE_CODE is "
            "derived from supported LOCATION_SEGMENT1 text, or the Source Lines local "
            "government when location is blank, following the supplied sample pattern. "
            "FACILITY_NAME uses the reconciled facility name when available and otherwise "
            "uses the supported Source Lines facility/location value; identifier-only "
            "values are not treated as facility names."
        ),
    }
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=3):
        label = row[0].value
        if label in replacements:
            row[1].value = replacements[label]
        if label == "BOOK_TYPE_CODE":
            row[1].value = (
                "Derive from supported LOCATION_SEGMENT1 or Source Lines local government "
                "text using the supplied sample Book pattern: remove DLG/district wording, "
                "retain MC where applicable, and append ' BK'."
            )
            row[2].value = "Sample Header of Asset Register..xlsx; user-requested derivation"


def load_input(path: Path, from_git_head: bool):
    if not from_git_head:
        return load_workbook(path)
    workbook_bytes = subprocess.check_output(
        ["git", "show", f"HEAD:{GIT_WORKBOOK_PATH}"], cwd=ROOT
    )
    return load_workbook(io.BytesIO(workbook_bytes))


def save_atomically(workbook, path: Path) -> None:
    temporary_path = path.with_name(f".{path.name}.tmp.xlsx")
    if temporary_path.exists():
        temporary_path.unlink()
    workbook.save(temporary_path)
    workbook.close()
    temporary_path.replace(path)


def build(path: Path, from_git_head: bool) -> dict[str, int]:
    assert to_book(r"MADI\-OKOLLO DLG") == "MADI OKOLLO BK"
    assert to_book("ABIM DISTRICT LOCAL GOV'T") == "ABIM BK"
    assert to_book("KAPCHORWA MUNICIPAL COUNCIL") == "KAPCHORWA MC BK"
    assert to_book("MOES") == "MOES BK"

    workbook = load_input(path, from_git_head)
    reconciled_facilities, local_governments = load_reconciliation()
    lg_by_row, facility_by_row, rejected_identifiers = source_maps(
        workbook["Source Lines"], reconciled_facilities, local_governments
    )

    register = workbook["Asset Register"]
    facility_column, _ = ensure_facility_column(register)
    headers = [cell.value for cell in next(register.iter_rows(min_row=1, max_row=1))]
    location_column = headers.index("LOCATION_SEGMENT1") + 1

    populated_book = 0
    blank_book = 0
    populated_facility = 0
    blank_facility = 0

    for row_number in range(2, register.max_row + 1):
        book = to_book(register.cell(row_number, location_column).value) or to_book(
            lg_by_row.get(row_number)
        )
        facility = facility_by_row.get(row_number)

        if book:
            register.cell(row_number, 1).value = book
            populated_book += 1
        else:
            blank_book += 1

        if facility:
            register.cell(row_number, facility_column).value = facility
            populated_facility += 1
        else:
            blank_facility += 1

    synchronize_asset_table(register)
    update_read_me(workbook["Read Me"])

    workbook.calculation.calcMode = "auto"
    workbook.calculation.fullCalcOnLoad = True
    workbook.calculation.forceFullCalc = True
    save_atomically(workbook, path)

    return {
        "populated_book": populated_book,
        "blank_book": blank_book,
        "populated_facility": populated_facility,
        "blank_facility": blank_facility,
        "rejected_identifiers": rejected_identifiers,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_PATH)
    parser.add_argument(
        "--from-git-head",
        action="store_true",
        help="Start from the clean committed workbook before applying the fix.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    stats = build(args.path, args.from_git_head)
    print(f"Filled BOOK_TYPE_CODE on {stats['populated_book']:,} rows; left blank {stats['blank_book']:,}.")
    print(f"Filled FACILITY_NAME on {stats['populated_facility']:,} rows; left blank {stats['blank_facility']:,}.")
    print(f"Ignored {stats['rejected_identifiers']:,} source identifier-only values as facility names.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
