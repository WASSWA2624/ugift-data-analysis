"""Build the MF and REF asset registers from the shared SK workbook.

Follows outputs/PROMPT_POPULATE_ASSET_REGISTERS.md. The SK workbook is the
stage-1 register and is not rewritten.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fill_borrowed_costs import (
    add_donor,
    clean_lg,
    common_life,
    groups_for,
    median,
    norm_lg,
    norm_name,
    parse_date,
    row_years,
    service_months,
    shillings,
    source_note,
    usable_name,
)
from fill_clear_template_fields import classify, explicit_token
from fill_gou_template import book_code, location_segment1
from merge_shared_asset_registers import blank_tag, clean

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / "outputs" / "asset-register-2026-09-23" / "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx"
MF = ROOT / "outputs" / "asset-register-2026-09-23" / "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
REF = ROOT / "outputs" / "asset-register-2026-09-23" / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
SAMPLE = ROOT / "Sample Header of Asset Register..xlsx"
UNIT = re.compile(r"\s*\[item \d+ of \d+\]\s*$", re.I)
LOOSE = re.compile(
    r"\b(kettles?|spoons?|forks?|calculators?|staplers?|stapling machines?|pen-?holders?|"
    r"punches|paper trays?|pin-?holders?|staple holders?|typewriters?)\b",
    re.I,
)
CONSUMABLE = re.compile(r"\b(pack of|single use|surgicle packs?|graph paper)\b", re.I)
NATURAL = re.compile(r"\b(natural resources?|mineral rights?|wildlife|forests?)\b", re.I)
NON_DEPR = re.compile(r"\b(work in progress|\bwip\b|operating lease)\b", re.I)
FAULTY = re.compile(
    r"not\s+(?:in\s+use|function|received|available)|damag|broken|obsolete|unserviceable|"
    r"\bfault|\bdisposed\b|\blost\b|\bmissing\b",
    re.I,
)
FUNCTIONAL = re.compile(r"\bin use\b|function|working well|\bavailable\b|verified|good condition", re.I)
PLACEHOLDER = {"n a", "na", "nil", "nill", "none", "null", "not applicable", "-"}
MONEY = {"FIXED_ASSETS_COST", "DEPRN_RESERVE", "YTD_DEPRN", "SALVAGE_VALUE"}
BLUE = PatternFill("solid", fgColor="9DC3E6")
ORANGE = PatternFill("solid", fgColor="F4B183")
GREEN = PatternFill("solid", fgColor="C6EFCE")
FILLS = {1: BLUE, 2: ORANGE, 3: GREEN}


def headers() -> list[str]:
    workbook = load_workbook(SAMPLE, read_only=True, data_only=True)
    row = [clean(value) for value in next(workbook.active.iter_rows(max_row=1, values_only=True))]
    workbook.close()
    return row


def plain(value: object) -> str:
    text = clean(value)
    folded = re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()
    return "" if folded in PLACEHOLDER or text in {"-", "—"} else text


def as_number(value: object) -> int | float | None:
    if isinstance(value, bool) or value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return int(value) if float(value).is_integer() else float(value)
    text = plain(value).replace(",", "")
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        number = float(text)
        return int(number) if number.is_integer() else number
    return None


def as_date(value: object) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return plain(value)


def condition(status: str) -> tuple[str, str]:
    if not status:
        return "", ""
    faulty = bool(FAULTY.search(status))
    functional = bool(FUNCTIONAL.search(status)) and not FAULTY.search(status)
    if faulty and not functional:
        label = "Faulty"
    elif functional and not faulty:
        label = "Functional"
    else:
        label = ""
    longer = "" if not label or re.fullmatch(r"(?i)functional|faulty", status.strip()) else status
    return label, longer


def facility_name(name: str, kind: str) -> str:
    text = plain(name)
    if not text:
        return ""
    kind_text = kind.casefold()
    health = "health" in kind_text or bool(re.search(r"(?i)health|\bhc\b|h\s*/\s*c|h\.c", text))
    school = "school" in kind_text or (bool(re.search(r"(?i)school|\bseed\b", text)) and not health)
    if health:
        text = re.sub(r"(?i)\bhealth\s+cent(?:re|er)\s*(?:ii+|iv|111|11|2|3)?\b", "Health Centre III", text)
        text = re.sub(r"(?i)\bh\.?\s*/?\s*c\.?\s*(?:ii+|iii|111|11|2|3)?\b", "Health Centre III", text)
        text = re.sub(r"(?i)(?:\s*Health Centre III\b)+", " Health Centre III", text)
        if "Health Centre III" not in text:
            text = f"{text} Health Centre III"
    elif school and not re.search(r"(?i)seed secondary school", text):
        text = re.sub(r"(?i)\s*(seed\s+)?(secondary\s+)?schools?$", "", text)
        text = re.sub(r"(?i)\s*seed$", "", text).strip()
        text = f"{text} Seed Secondary School"
    return re.sub(r"\s+", " ", text).strip()


def facility_kind(kind: str, name: str) -> str:
    blob = f"{kind} {name}".casefold()
    if "health" in blob or re.search(r"\bhc\b|health centre", blob):
        return "Health centre"
    if "school" in blob or "seed" in blob:
        return "School"
    return "Health centre" if "health" in kind.casefold() else "School" if kind else ""


def choose(index: dict, name: str, government: str, years: tuple[int, ...], minor: str):
    bucket = index.get(name)
    if not bucket:
        return None
    if government and government in bucket:
        groups = groups_for(bucket, (government,), minor, years)
        if groups:
            return 1, groups
    others = tuple(item for item in bucket if item != government)
    if others:
        groups = groups_for(bucket, others, minor, years)
        if groups:
            return 2, groups
    groups = groups_for(bucket, tuple(bucket), minor, years)
    return (3, groups) if groups else None


def money_cell(sheet, value: int | float, fill=None) -> WriteOnlyCell:
    cell = WriteOnlyCell(sheet, value=int(value) if float(value).is_integer() else value)
    cell.number_format = "#,##0.##"
    if fill is not None:
        cell.fill = fill
    return cell


def remark_bundle(parts: list[str]) -> str:
    kept = []
    for part in parts:
        text = plain(part)
        if text and text not in kept:
            kept.append(text)
    return " ".join(kept)


def classify_row(description: str):
    bare = UNIT.sub("", description).strip()
    if not bare or CONSUMABLE.search(bare) or re.fullmatch(r"-?\d+", bare):
        return None
    return classify(bare)


def build_values(source: dict, headers_row: list[str], *, borrow: bool, costs: dict, lives: dict, displays: dict, cache: dict, stats: Counter) -> list:
    item = plain(source.get("Equipment/Item"))
    description = plain(source.get("Item Description"))
    unit = plain(source.get("Unit"))
    name = item or description
    if unit:
        name = f"{name} [{unit}]"
    bare = UNIT.sub("", item or description).strip()
    kind = facility_kind(plain(source.get("Facility type")), plain(source.get("Facility")))
    facility = facility_name(plain(source.get("Facility")), kind)
    status_label, longer_status = condition(plain(source.get("Equipment status")))
    classified = classify_row(bare)
    loose = bool(LOOSE.search(bare))
    natural = bool(NATURAL.search(bare))
    non_depr = bool(NON_DEPR.search(bare))
    major = minor1 = minor2 = ""
    life = as_number(source.get("Life in Months"))
    depreciates = False
    if classified and not loose:
        major, minor1, minor2, class_life, depreciates = classified
        if life is None and class_life:
            life = class_life
        stats["class"] += 1
    if natural or loose or (classified and not depreciates):
        depreciates = False
    if non_depr:
        depreciates = False
    if life is not None and (not isinstance(life, (int, float)) or life <= 0):
        life = None
    cost = as_number(source.get("Cost"))
    years = row_years(as_date(source.get("Date Of Purchase")), as_date(source.get("Date Placed In Service")))
    government = norm_lg(clean_lg(plain(source.get("Local Government"))))
    minor_key = norm_name(minor2)
    asset_name = norm_name(bare)
    notes = []
    cost_fill = None
    life_fill = None
    if borrow and usable_name(asset_name):
        if cost is None:
            found = choose(costs, asset_name, government, years, minor_key)
            if found:
                method, groups = found
                values = [value for _, _, bucket in groups for value in bucket]
                cost = shillings(median(values))
                cost_fill = FILLS[method]
                notes.append(source_note(method, groups, displays, asset_name, "cost"))
                stats[f"cost_{method}"] += 1
        if life is None and status_label != "Faulty":
            found = choose(lives, asset_name, government, years, minor_key)
            if found:
                method, groups = found
                values = [value for _, _, bucket in groups for value in bucket]
                life = common_life(values)
                life_fill = FILLS[method]
                notes.append(source_note(method, groups, displays, asset_name, "life"))
                stats[f"life_{method}"] += 1
                if classified is None:
                    depreciates = not loose and not natural and not non_depr
    capitalized = bool(cost) and not loose and not natural and not CONSUMABLE.search(bare) and (classified or usable_name(asset_name))
    if loose or natural or CONSUMABLE.search(bare):
        capitalized = False
    if major == "LAND":
        capitalized = bool(cost)
        depreciates = False
    if capitalized:
        stats["capitalized"] += 1
    placed = parse_date(as_date(source.get("Date Placed In Service")))
    reserve = as_number(source.get("Acc Dep Cost"))
    ytd = as_number(source.get("Ytd Deprn"))
    salvage = 0 if depreciates and life and (capitalized or cost) else None
    calculated_nbv = None
    if borrow and status_label == "Functional" and cost is not None and life and life >= 12 and placed and salvage is not None and salvage < cost:
        months, ytd_months = service_months(placed, int(life))
        depreciable = cost - salvage
        monthly = depreciable / life
        accumulated = min(depreciable, monthly * months)
        current = monthly * ytd_months
        if reserve is None:
            reserve = shillings(accumulated)
            stats["reserve"] += 1
        if ytd is None:
            ytd = shillings(current)
            stats["ytd"] += 1
        calculated_nbv = max(0, shillings(float(cost) - float(reserve)))
    source_nbv = as_number(source.get("Net Book Value"))
    remarks = remark_bundle([
        longer_status,
        plain(source.get("Remarks")),
        " ".join(notes),
        f"Facility type: {kind}" if kind else "",
        f"Item description: {description}" if description and description != bare else "",
        f"Date of purchase: {as_date(source.get('Date Of Purchase'))}" if as_date(source.get("Date Of Purchase")) else "",
        f"Recoverable cost: {plain(source.get('Recoverable cost'))}" if plain(source.get("Recoverable cost")) else "",
        f"Source net book value: {source_nbv}" if source_nbv is not None else "",
        f"Net book value: {calculated_nbv}" if calculated_nbv is not None else "",
        f"Source file: {plain(source.get('Source file'))}" if plain(source.get("Source file")) else "",
        f"Source location: {plain(source.get('Source location'))}" if plain(source.get("Source location")) else "",
    ])
    tag = "Not Engraved" if blank_tag(source.get("Tag Number (engrave no.)")) else plain(source.get("Tag Number (engrave no.)"))
    evidence = f"{bare} {description}"
    values = {
        "BOOK_TYPE_CODE": book_code(plain(source.get("Local Government"))),
        "DESCRIPTION": name or None,
        "ASSET_CATEGORY_MAJOR": major or None,
        "ASSET_CATEGORY_MINOR1": minor1 or None,
        "ASSET_CATEGORY_MINOR2": minor2 or None,
        "ASSET_TYPE": "CAPITALIZED" if capitalized else None,
        "FIXED_ASSETS_UNITS": 1,
        "LOCATION_SEGMENT1": location_segment1(plain(source.get("Local Government"))),
        "LOCATION_SEGMENT2": plain(source.get("Department")) or None,
        "LOCATION_SEGMENT3": facility or None,
        "FIXED_ASSETS_COST": (cost, cost_fill),
        "ASSET_EXP_ACCT_ACCOUNT": "221012" if loose else None,
        "DATE_PLACED_IN_SERVICE": as_date(source.get("Date Placed In Service")) or None,
        "DEPRECIATE_FLAG": "NO" if (loose or natural or non_depr or major == "LAND") else "YES" if depreciates and life else None,
        "DEPRN_METHOD_CODE": "STL" if depreciates and life else None,
        "LIFE_IN_MONTHS": (life, life_fill) if life else None,
        "DEPRN_RESERVE": reserve,
        "YTD_DEPRN": ytd,
        "SALVAGE_VALUE": salvage,
        "ASSET_NUMBER": plain(source.get("Asset Number")) or None,
        "TAG_NUMBER": tag,
        "SERIAL_NUMBER": explicit_token(evidence, "serial"),
        "MANUFACTURER_NAME": explicit_token(evidence, "manufacturer"),
        "MODEL_NUMBER": explicit_token(evidence, "model"),
        "IN_USE_FLAG": "YES" if status_label == "Functional" else "NO" if status_label == "Faulty" else None,
        "ATTRIBUTE15": remarks or None,
    }
    return [values.get(header) for header in headers_row]


def index_sources(sheet) -> tuple[dict, dict, dict]:
    rows = sheet.iter_rows(values_only=True)
    header = [clean(value) for value in next(rows)]
    index = {name: position for position, name in enumerate(header)}
    costs: dict = {}
    lives: dict = {}
    displays: dict = {}
    for count, row in enumerate(rows, 2):
        source = {name: row[position] if position < len(row) else None for name, position in index.items()}
        bare = UNIT.sub("", plain(source.get("Equipment/Item")) or plain(source.get("Item Description"))).strip()
        asset_name = norm_name(bare)
        if not usable_name(asset_name):
            continue
        government_text = clean_lg(plain(source.get("Local Government")))
        government = norm_lg(government_text)
        classified = classify_row(bare)
        minor = norm_name(classified[2]) if classified else ""
        years = row_years(as_date(source.get("Date Of Purchase")), as_date(source.get("Date Placed In Service")))
        cost = as_number(source.get("Cost"))
        if isinstance(cost, (int, float)) and cost > 0:
            add_donor(costs, displays, asset_name, government, years, minor, shillings(cost), government_text)
        life = as_number(source.get("Life in Months"))
        if isinstance(life, (int, float)) and life >= 12:
            add_donor(lives, displays, asset_name, government, years, minor, int(life), government_text)
        if count % 100000 == 0:
            print(f"indexed {count:,}", flush=True)
    return costs, lives, displays


def write_book(path: Path, header: list[str], rows, readme_lines) -> None:
    workbook = Workbook(write_only=True)
    sheet = workbook.create_sheet("Asset Register")
    sheet.freeze_panes = "A2"
    header_cells = []
    for value in header:
        cell = WriteOnlyCell(sheet, value=value)
        cell.font = Font(bold=True, color="FFFFFF")
        header_cells.append(cell)
    sheet.append(header_cells)
    count = 0
    for values in rows:
        output = []
        for name, value in zip(header, values):
            if isinstance(value, tuple):
                amount, fill = value
                output.append(money_cell(sheet, amount, fill) if amount is not None else None)
            elif name in MONEY and isinstance(value, (int, float)):
                output.append(money_cell(sheet, value))
            else:
                output.append(value)
        sheet.append(output)
        count += 1
        if count % 50000 == 0:
            print(f"{path.name} {count:,}", flush=True)
    sheet.auto_filter.ref = f"A1:{get_column_letter(len(header))}{count + 1}"
    notes = workbook.create_sheet("Read Me")
    for line in readme_lines():
        notes.append([line])
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)
    print(f"wrote {count:,} {path}", flush=True)


def source_rows():
    workbook = load_workbook(SK, read_only=True, data_only=True)
    sheet = workbook["Asset Register"]
    rows = sheet.iter_rows(values_only=True)
    header = [clean(value) for value in next(rows)]
    index = {name: position for position, name in enumerate(header)}
    for row in rows:
        yield {name: row[position] if position < len(row) else None for name, position in index.items()}
    workbook.close()


def readme(stats: Counter, borrowed: bool) -> list[str]:
    lines = [
        "UgIFT asset register",
        "Guidelines read: GOU Asset Accounting Policies and Guidelines 2023, sections 3.2.1, 3.2.2, 3.2.3, 3.3.3, 3.3.5, 5, and Annex 1 lives encoded for each classified asset.",
        "One row is one physical asset. FIXED_ASSETS_UNITS is 1. A counted source line is marked [item 1 of 100] in DESCRIPTION.",
        "ASSET_TYPE is CAPITALIZED only when the asset is controlled, has service potential beyond one year, already exists, and has a measurable cost. There is no shilling threshold.",
        "Kettles, spoons, forks, calculators, staplers, pen-holders, punches, paper trays, pin and staple holders, and typewriters are not capitalized. Their expense account is 221012.",
        "Land is capitalized and is not depreciated. Work in progress and operating leases are not depreciated. Salvage value is nil where the row depreciates (section 5.7).",
        "DEPRN_METHOD_CODE is STL where a life applies. Life comes from the source, otherwise from the class life.",
        "ATTRIBUTE1 to ATTRIBUTE15 keep the sample headers. The source does not state class attributes such as plot number, floor count, or chainage, so those stay blank.",
        "ATTRIBUTE15 holds remarks: longer condition text, unmapped source fields, and, in the REF workbook, borrowed-cost notes. The sample header has no Remarks column.",
        "LOCATION_SEGMENT4, ASSET_CATEGORY_MINOR3, ASSET_KEY_SEGMENT1, EMPLOYEE_NUMBER, AMORTIZATION_START_DATE, and AMORTIZE_NBV_FLAG stay blank. The guidelines do not state those values for these assets.",
        "PRORATE_CONVENTION_CODE stays blank. The guidelines require straight line but do not name a prorate convention code.",
        "Clearing-account segments stay blank. The guidelines do not state them. Expense-account segments other than 221012 for loose tools stay blank for the same reason.",
        "Recoverable cost is not written as salvage value.",
        f"Classified rows: {stats['class']:,}. Capitalized rows: {stats['capitalized']:,}.",
    ]
    if borrowed:
        lines.extend([
            "White cost cells are prices stated on the source. Blue, orange, and green cells are borrowed.",
            "Blue: same local government, same purchase year or the nearest year. Orange: other local governments. Green: the whole register, used only when the first two found no price.",
            "A borrowed price is the median of assets with the same name. Where both rows have a class, the class matches. The source sentence is in ATTRIBUTE15.",
            "Straight-line depreciation is calculated to 30 September 2026 where cost, nil residual, life, and the month placed in service are known and the asset is in use. Amounts already on the source were left unchanged.",
            f"Borrowed costs: same government {stats['cost_1']:,}; other governments {stats['cost_2']:,}; whole register {stats['cost_3']:,}.",
            f"Borrowed lives: same government {stats['life_1']:,}; other governments {stats['life_2']:,}; whole register {stats['life_3']:,}.",
        ])
    else:
        lines.append("This workbook does not borrow missing prices. Borrowed prices, with colours, are in the REF workbook.")
    return lines


def emit(borrow: bool, costs: dict, lives: dict, displays: dict, header: list[str], stats: Counter):
    cache: dict = {}
    for source in source_rows():
        yield build_values(
            source, header, borrow=borrow, costs=costs, lives=lives,
            displays=displays, cache=cache, stats=stats,
        )


def main() -> None:
    header = headers()
    print("indexing source prices", flush=True)
    workbook = load_workbook(SK, read_only=True, data_only=True)
    costs, lives, displays = index_sources(workbook["Asset Register"])
    workbook.close()
    print("writing MF", flush=True)
    mf_stats: Counter = Counter()
    write_book(MF, header, emit(False, costs, lives, displays, header, mf_stats), lambda: readme(mf_stats, False))
    print("writing REF", flush=True)
    ref_stats: Counter = Counter()
    write_book(REF, header, emit(True, costs, lives, displays, header, ref_stats), lambda: readme(ref_stats, True))


if __name__ == "__main__":
    main()
