"""Recalculate REF depreciation, net book value, and the linked attributes.

Straight line to 30 September 2026. Monthly charge is (cost - salvage) / life.
The reserve runs from the placed-in-service month through September 2026 and
stops at the end of useful life. Year-to-date is the July-September 2026
portion. Land, work in progress, and rows that do not depreciate stay at a
nil charge. A blank cost is unknown: its depreciation and carrying amount are 0.
Recorded costs are not changed.
"""

from __future__ import annotations

import sys
import zipfile
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fill_borrowed_costs import shillings
from fill_register_gaps import load_strings
from patch_register_workbook import CELL, apply_updates, cell_value, worksheet_parts

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "outputs" / "asset-register" / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
EPOCH = date(1899, 12, 30)
AS_OF = date(2026, 9, 30)
AS_OF_INDEX = 2026 * 12 + 9
FY_START_INDEX = 2026 * 12 + 7
WHITE_MONEY = 3
NO_CHARGE = {"CIP", "EXPENSED", "NOT CAPITALIZED", "NOT RECOGNIZED"}
FIELDS = {
    "C": "major",
    "G": "type",
    "M": "cost",
    "AF": "placed",
    "AG": "flag",
    "AI": "life",
    "AK": "reserve",
    "AL": "ytd",
    "AM": "salvage",
    "BF": "recoverable",
    "BG": "attr_cost",
    "BH": "attr_reserve",
    "BI": "nbv",
    "BJ": "attr_ytd",
}
OUTPUTS = {
    "reserve": "AK",
    "ytd": "AL",
    "recoverable": "BF",
    "attr_cost": "BG",
    "attr_reserve": "BH",
    "nbv": "BI",
    "attr_ytd": "BJ",
}


def amount(value: object) -> float | None:
    if isinstance(value, bool) or value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        compact = value.replace(",", "").strip()
        if compact.replace(".", "", 1).lstrip("-").isdigit():
            return float(compact)
    return None


def whole(value: object) -> int | None:
    number = amount(value)
    if number is None:
        return None
    return shillings(number)


def serial_date(value: object) -> date | None:
    number = amount(value)
    if number is None or not 20000 <= number <= 60000:
        return None
    return EPOCH + timedelta(days=int(number))


def column_of(reference: str) -> str:
    return "".join(character for character in reference if character.isalpha())


def service_months(placed: date, life: int) -> tuple[int, int]:
    start = placed.year * 12 + placed.month
    if start > AS_OF_INDEX:
        return 0, 0
    end = min(AS_OF_INDEX, start + life - 1)
    months = end - start + 1
    overlap_start = max(start, FY_START_INDEX)
    overlap_end = min(end, AS_OF_INDEX)
    return months, max(0, overlap_end - overlap_start + 1)


def schedule(cost: int, salvage: int, life: int, placed: date) -> tuple[int, int, int]:
    """Return reserve, year-to-date depreciation, and net book value."""
    depreciable = cost - salvage
    if life < 12 or depreciable <= 0 or placed > AS_OF:
        return 0, 0, max(cost, salvage)
    months, ytd_months = service_months(placed, life)
    monthly = depreciable / life
    accumulated = min(depreciable, monthly * months)
    current = monthly * ytd_months
    if accumulated >= depreciable - 0.5 and ytd_months:
        current = max(0.0, depreciable - monthly * (months - ytd_months))
    reserve = min(shillings(accumulated), depreciable)
    ytd = min(shillings(current), reserve)
    return reserve, ytd, cost - reserve


def targets_for(row: dict) -> dict[str, int | None]:
    cost = whole(row.get("cost"))
    salvage = whole(row.get("salvage")) or 0
    life = whole(row.get("life")) or 0
    placed = serial_date(row.get("placed"))
    depreciates = (
        str(row.get("flag") or "") == "YES"
        and str(row.get("major") or "") != "LAND"
        and str(row.get("type") or "") not in NO_CHARGE
        and cost is not None
        and life >= 12
        and placed is not None
    )
    if cost is None:
        reserve = ytd = recoverable = nbv = 0
        attr_cost = None
    elif depreciates:
        reserve, ytd, nbv = schedule(cost, salvage, life, placed)
        recoverable = nbv
        attr_cost = cost
    else:
        reserve = ytd = 0
        nbv = max(salvage, cost)
        recoverable = nbv
        attr_cost = cost
    return {
        "reserve": reserve,
        "ytd": ytd,
        "recoverable": recoverable,
        "attr_cost": attr_cost,
        "attr_reserve": reserve,
        "nbv": nbv,
        "attr_ytd": ytd,
    }


def row_values(raw: bytes, shared: list[str]) -> dict[str, object]:
    values = {}
    for match in CELL.finditer(raw):
        xml = match.group()
        reference = xml.split(b'r="', 1)[1].split(b'"', 1)[0].decode()
        column = column_of(reference)
        if column in FIELDS:
            values[FIELDS[column]] = cell_value(xml, shared)
    return values


def same(current: object, new: int | None) -> bool:
    if new is None:
        return current in (None, "")
    return whole(current) == new


def updates_for(row_number: int, row: dict) -> list[dict]:
    updates = []
    for name, new in targets_for(row).items():
        if new is None or same(row.get(name), new):
            continue
        column = OUTPUTS[name]
        updates.append({
            "sheet": "Asset Register",
            "cell": f"{column}{row_number}",
            "expected": row.get(name) if row.get(name) not in ("",) else None,
            "value": new,
            "style": None if isinstance(row.get(name), (int, float)) else WHITE_MONEY,
        })
    return updates


def main() -> None:
    apply = "--apply" in sys.argv
    print("reading", flush=True)
    updates = []
    stats = Counter()
    examples = []
    with zipfile.ZipFile(REF) as workbook:
        shared = load_strings(workbook.read("xl/sharedStrings.xml"))
        stream = workbook.open("xl/worksheets/sheet1.xml")
        for is_row, raw in worksheet_parts(stream):
            if not is_row or raw.startswith(b'<row r="1"'):
                continue
            row_number = int(raw.split(b'r="', 1)[1].split(b'"', 1)[0])
            row = row_values(raw, shared)
            stats["rows"] += 1
            if whole(row.get("cost")) is None:
                stats["blank_cost"] += 1
            elif str(row.get("flag") or "") == "YES" and str(row.get("major") or "") != "LAND":
                stats["depreciating"] += 1
            changes = updates_for(row_number, row)
            if changes:
                stats["changed_rows"] += 1
                stats["changed_cells"] += len(changes)
                for change in changes:
                    stats[change["cell"].rstrip("0123456789")] += 1
                if len(examples) < 12:
                    examples.append((row_number, row.get("cost"), row.get("reserve"), changes[0]["value"], changes[0]["cell"]))
            if apply:
                updates.extend(changes)
            if stats["rows"] % 50000 == 0:
                print(f"scanned {stats['rows']:,} changed rows {stats['changed_rows']:,}", flush=True)
        stream.close()
    print("STATS")
    for key, count in sorted(stats.items()):
        print(f"{count}\t{key}")
    for example in examples:
        print("example", example)
    if not apply:
        print("dry run")
        return
    if not updates:
        print("already reconciled")
        return
    destination = REF.with_name(REF.stem + ".financials.xlsx")
    if destination.exists():
        destination.unlink()
    result = apply_updates(REF, destination, updates)
    destination.replace(REF)
    print("wrote", REF, result)


if __name__ == "__main__":
    main()
