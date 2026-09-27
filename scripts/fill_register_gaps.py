"""Fill blank REF cells in columns that already have values.

Follows outputs/PROMPT_POPULATE_ASSET_REGISTERS.md. Existing values stay.
A blank is filled only when the guidelines, the row, or the SK source register
state it. Work in progress keeps a blank placed-in-service date. Generic names
with no comparable price stay blank.

    python scripts/fill_register_gaps.py           # report only
    python scripts/fill_register_gaps.py --apply   # write the REF workbook
"""

from __future__ import annotations

import argparse
import re
import zipfile
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import build_guideline_registers as guide
from fill_borrowed_costs import add_donor, groups_for, median, row_years, shillings, usable_name
from merge_shared_asset_registers import canonical_item

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "outputs" / "asset-register" / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
SK = ROOT / "outputs" / "asset-register" / "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx"
ROW = re.compile(rb'<row r="(\d+)"([^>]*)>(.*?)</row>', re.S)
CELL = re.compile(rb'<c r="([A-Z]+)(\d+)"([^>]*?)(?:/>|>(.*?)</c>)', re.S)
UNIT = re.compile(r"\s*\[item \d+ of \d+\]\s*$", re.I)
FRAGMENT = re.compile(
    r"(?i)^\s*(?:pcs?|pieces?|[\d./]+|&\s*components|adult|paediat\w*|pediatric\s+\d+\s*pcs|not engraved)\s*$"
)
EPOCH = date(1899, 12, 30)
MONEY_STYLE = {1: 5, 2: 2, 3: 11}
DATE_STYLE = {1: 6, 2: 7, 3: 8}
WHITE_MONEY = 4
WHITE_DATE = 3

STRINGS: list[str] = []
COLUMNS: dict[str, int] = {}
SK_DESCRIPTION: dict[int, str] = {}
SK_PURCHASE: dict[int, str] = {}
SK_COST: dict[int, float] = {}
COSTS: dict = {}
DATES: dict = {}
CLASS_COSTS: dict = {}
FACILITY_MONTHS: dict[tuple[str, str], Counter] = {}
LG_MONTHS: dict[str, Counter] = {}
ALL_MONTHS: Counter = Counter()
REGISTERS: guide.Registers | None = None


def column_number(letters: str) -> int:
    number = 0
    for character in letters:
        number = number * 26 + ord(character) - 64
    return number


def column_letters(number: int) -> str:
    letters = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def unescape(text: str) -> str:
    return text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#10;", " ")


def escape(text: str) -> str:
    cleaned = "".join(character for character in text if character >= " " or character == "\t")
    return cleaned.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_strings(xml: bytes) -> list[str]:
    strings = []
    for item in re.finditer(rb"<si>(.*?)</si>", xml, re.S):
        parts = re.findall(rb"<t[^>]*>(.*?)</t>", item.group(1), re.S)
        strings.append("".join(unescape(part.decode("utf-8", "replace")) for part in parts))
    return strings


def cell_text(attrs: bytes, inner: bytes | None) -> str:
    if not inner:
        return ""
    if b't="s"' in attrs:
        match = re.search(rb"<v>(\d+)</v>", inner)
        if match:
            index = int(match.group(1))
            return STRINGS[index].strip() if index < len(STRINGS) else ""
    match = re.search(rb"<t[^>]*>(.*?)</t>|<v>(.*?)</v>", inner, re.S)
    if not match:
        return ""
    raw = match.group(1) if match.group(1) is not None else match.group(2)
    return unescape(raw.decode("utf-8", "replace")).strip()


def style_of(attrs: bytes) -> int | None:
    match = re.search(rb's="(\d+)"', attrs)
    return int(match.group(1)) if match else None


def parse_row(body: bytes) -> dict[int, tuple[str, int | None, bytes]]:
    cells = {}
    for cell in CELL.finditer(body):
        number = column_number(cell.group(1).decode())
        cells[number] = (cell_text(cell.group(3), cell.group(4)), style_of(cell.group(3)), cell.group(0))
    return cells


def value(cells: dict, column: int) -> str:
    return cells[column][0] if column in cells else ""


def number(text: str) -> float | None:
    if text is None or text == "":
        return None
    try:
        return float(str(text).replace(",", ""))
    except ValueError:
        return None


def placed_date(text: str) -> date | None:
    if re.fullmatch(r"\d{5}", text or ""):
        serial = int(text)
        if 20000 <= serial <= 60000:
            return EPOCH + timedelta(days=serial)
    return guide.as_date(text)


def excel_serial(value_date: date) -> int:
    return (value_date - EPOCH).days


def text_cell(row_number: str, column: int, text: str, style: int | None = None) -> bytes:
    ref = f"{column_letters(column)}{row_number}"
    style_attr = f' s="{style}"' if style is not None else ""
    return f'<c r="{ref}"{style_attr} t="inlineStr"><is><t>{escape(text)}</t></is></c>'.encode()


def number_cell(row_number: str, column: int, amount: int | float, style: int | None) -> bytes:
    ref = f"{column_letters(column)}{row_number}"
    style_attr = f' s="{style}"' if style is not None else ""
    rendered = int(amount) if float(amount).is_integer() else amount
    return f'<c r="{ref}"{style_attr}><v>{rendered}</v></c>'.encode()


def bare_name(description: str) -> str:
    return UNIT.sub("", description).strip()


def asset_key(name: str) -> str:
    return guide.borrow_key(guide.display_item(canonical_item(name)))


def specific_name(name: str, key: str) -> bool:
    return bool(key) and usable_name(key) and key not in guide.GENERIC_NAMES and not guide.GENERIC_HEAD.match(name)


def work_in_progress(asset_type: str, description: str, status: str, remarks: str) -> bool:
    if asset_type == "CIP":
        return True
    return bool(guide.NON_DEPR.search(f"{description} {status} {remarks}"))


def non_asset(name: str) -> bool:
    return bool(
        guide.LOOSE.search(name) or guide.CONSUMABLE.search(name) or guide.REPAIR.search(name)
        or guide.SERVICE.search(name) or guide.TOTAL_LINE.search(name) or guide.NATURAL.search(name)
        or FRAGMENT.search(name)
    )


def load_sk() -> None:
    with zipfile.ZipFile(SK) as workbook:
        sheet = workbook.read("xl/worksheets/sheet1.xml")
    description = column_number("D")
    purchase = column_number("G")
    cost = column_number("J")
    for match in ROW.finditer(sheet):
        row_number = int(match.group(1))
        if row_number == 1:
            continue
        cells = parse_row(match.group(3))
        text = value(cells, description)
        if text:
            SK_DESCRIPTION[row_number] = text
        bought = value(cells, purchase)
        if bought:
            SK_PURCHASE[row_number] = bought
        amount = number(value(cells, cost))
        if amount is not None:
            SK_COST[row_number] = amount
        if row_number % 50000 == 0:
            print(f"sk {row_number:,}", flush=True)


def index_donors(sheet: bytes) -> None:
    displays: dict = {}
    class_prices: dict[str, list] = {}
    all_prices: dict[str, list] = {}
    for match in ROW.finditer(sheet):
        row_number = int(match.group(1))
        if row_number == 1:
            continue
        cells = parse_row(match.group(3))
        name = bare_name(value(cells, COLUMNS["DESCRIPTION"]))
        key = asset_key(name)
        if not specific_name(name, key) or non_asset(name):
            continue
        government = value(cells, COLUMNS["BOOK_TYPE_CODE"])
        minor = guide.norm_name(value(cells, COLUMNS["ASSET_CATEGORY_MINOR2"]))
        purchase = value(cells, COLUMNS[guide.ATTRIBUTE[7]])
        cost_text, cost_style, _ = cells.get(COLUMNS["FIXED_ASSETS_COST"], ("", None, b""))
        amount = number(cost_text)
        if cost_style == WHITE_MONEY and amount is not None and amount > 0:
            years = row_years(purchase, "")
            add_donor(COSTS, displays, key, government, years, minor, shillings(amount), government)
            all_prices.setdefault(key, []).append(shillings(amount))
            if minor:
                add_donor(CLASS_COSTS, displays, minor, government, years, "", shillings(amount), government)
                class_prices.setdefault(minor, []).append(shillings(amount))
        date_text, date_style, _ = cells.get(COLUMNS["DATE_PLACED_IN_SERVICE"], ("", None, b""))
        placed = placed_date(date_text) if date_style == WHITE_DATE else None
        if placed and date(1990, 1, 1) <= placed <= guide.AS_OF:
            years = row_years(purchase, placed.isoformat())
            add_donor(DATES, displays, key, government, years, minor, guide.month_index(placed), government)
            facility = guide.norm_name(value(cells, COLUMNS["LOCATION_SEGMENT3"]))
            FACILITY_MONTHS.setdefault((government, facility), Counter())[guide.month_index(placed)] += 1
            LG_MONTHS.setdefault(government, Counter())[guide.month_index(placed)] += 1
            ALL_MONTHS[guide.month_index(placed)] += 1
        if row_number % 50000 == 0:
            print(f"donors {row_number:,}", flush=True)
    guide.PRICE_MEDIAN.clear()
    guide.PRICE_MEDIAN.update({name: median(prices) for name, prices in all_prices.items() if len(prices) >= 3})
    guide.CLASS_MEDIAN.clear()
    guide.CLASS_MEDIAN.update({minor: median(prices) for minor, prices in class_prices.items() if len(prices) >= 3})
    guide.CLASS_COSTS.clear()
    guide.CLASS_COSTS.update(CLASS_COSTS)
    guide.finalize_cost_donors(COSTS)
    CLASS_COSTS.clear()
    CLASS_COSTS.update(guide.CLASS_COSTS)


def choose_values(index: dict, name: str, government: str, years: tuple[int, ...], minor: str):
    found = guide.choose(index, name, government, years, minor)
    if not found:
        return None
    method, groups = found
    values = [item for _, _, bucket in groups for item in bucket]
    return method, values


def borrow_cost(key: str, government: str, years: tuple[int, ...], minor: str):
    found = choose_values(COSTS, key, government, years, minor)
    if found:
        method, values = found
        values = guide.plausible(values, key)
        if values:
            return shillings(median(values)), MONEY_STYLE[method], f"name_{method}"
    if minor and not COSTS.get(key):
        found = choose_values(CLASS_COSTS, minor, government, years, "")
        if found:
            method, values = found
            if values:
                return shillings(median(values)), MONEY_STYLE[method], f"class_{method}"
    return None


def borrow_date(key: str, government: str, years: tuple[int, ...], minor: str, facility: str):
    found = choose_values(DATES, key, government, years, minor)
    if found:
        method, values = found
        if values:
            return guide.month_date(guide.common_life(values)), DATE_STYLE[method], f"name_{method}"
    pool = FACILITY_MONTHS.get((government, facility))
    method = 1
    if not pool:
        pool = LG_MONTHS.get(government)
    if not pool and ALL_MONTHS:
        pool = ALL_MONTHS
        method = 3
    if pool:
        return guide.month_date(pool.most_common(1)[0][0]), DATE_STYLE[method], f"place_{method}"
    return None


def expense_for(minor: str) -> str | None:
    acquisition = guide.ANNEX2_BY_MINOR2.get(guide.norm_name(minor))
    return "231" + acquisition[3:] if acquisition else None


def update_row(match: re.Match[bytes], stats: Counter, examples: dict[str, list], apply: bool) -> bytes:
    row_number = match.group(1).decode()
    if row_number == "1":
        return match.group(0)
    cells = parse_row(match.group(3))
    row_index = int(row_number)
    description = bare_name(value(cells, COLUMNS["DESCRIPTION"]))
    status = value(cells, COLUMNS[guide.ATTRIBUTE[14]])
    remarks = value(cells, COLUMNS[guide.ATTRIBUTE[15]])
    detail = value(cells, COLUMNS[guide.ATTRIBUTE[4]])
    purchase = value(cells, COLUMNS[guide.ATTRIBUTE[7]])
    government = value(cells, COLUMNS["BOOK_TYPE_CODE"])
    facility = guide.norm_name(value(cells, COLUMNS["LOCATION_SEGMENT3"]))
    asset_type = value(cells, COLUMNS["ASSET_TYPE"])
    major = value(cells, COLUMNS["ASSET_CATEGORY_MAJOR"])
    minor = value(cells, COLUMNS["ASSET_CATEGORY_MINOR2"])
    source_description = SK_DESCRIPTION.get(row_index, "")
    key = asset_key(description)
    equivalent = guide.reviewed_equivalent(description, source_description or detail)
    found = None
    if not major:
        found = REGISTERS.classify(equivalent or description)
        if found is None and source_description and not equivalent:
            found = REGISTERS.classify(guide.display_item(canonical_item(source_description)))
    if found:
        minor = found[2]
    denied = guide.denies_asset(status, description, detail) or guide.denies_asset(remarks, description, detail)
    pending = work_in_progress(asset_type, description, status, remarks)
    loose = bool(guide.LOOSE.search(description)) and found is None
    years = row_years(purchase, "")
    cost_column = COLUMNS["FIXED_ASSETS_COST"]
    has_cost = cost_column in cells
    cost = number(value(cells, cost_column)) if has_cost else None
    life_column = COLUMNS["LIFE_IN_MONTHS"]
    life = number(value(cells, life_column)) if life_column in cells else None
    flag = value(cells, COLUMNS["DEPRECIATE_FLAG"])
    derived_nil = bool(found) and has_cost and cost == 0 and (life or 0) == 0 and not denied and not pending
    additions: dict[int, bytes] = {}

    def add(column: int, xml: bytes, kind: str) -> None:
        additions[column] = xml
        stats[kind] += 1

    if found and not major:
        add(COLUMNS["ASSET_CATEGORY_MAJOR"], text_cell(row_number, COLUMNS["ASSET_CATEGORY_MAJOR"], found[0]), "class")
        add(COLUMNS["ASSET_CATEGORY_MINOR1"], text_cell(row_number, COLUMNS["ASSET_CATEGORY_MINOR1"], found[1]), "class_minor")
        add(COLUMNS["ASSET_CATEGORY_MINOR2"], text_cell(row_number, COLUMNS["ASSET_CATEGORY_MINOR2"], found[2]), "class_minor")
        label = guide.display_item(canonical_item(description)) or description
        add(COLUMNS["ASSET_CATEGORY_MINOR3"], text_cell(row_number, COLUMNS["ASSET_CATEGORY_MINOR3"], label), "class_minor")
        if len(examples["class"]) < 12:
            examples["class"].append(f"{description} -> {found[2]}")
        if (life or 0) == 0 and found[4] and not pending:
            stated = number(value(cells, COLUMNS[guide.ATTRIBUTE[5]]))
            months = int(stated) if stated and stated >= 12 else int(found[3] or guide.FALLBACK_LIFE)
            add(life_column, number_cell(row_number, life_column, months, None), "life")
            add(COLUMNS[guide.ATTRIBUTE[5]], number_cell(row_number, COLUMNS[guide.ATTRIBUTE[5]], months, None), "life_attr")
            life = months

    cost_changed = False
    if not has_cost or derived_nil:
        source_cost = SK_COST.get(row_index)
        borrowed = None
        can_price = not pending and not loose and not non_asset(description) and specific_name(description, key)
        if source_cost is not None and source_cost >= guide.MIN_COST and (not has_cost or derived_nil):
            borrowed = (shillings(source_cost), WHITE_MONEY, "source_cost")
        elif source_cost is not None and source_cost < guide.MIN_COST and not has_cost:
            borrowed = (0, WHITE_MONEY, "nil")
        elif can_price and (source_cost is None) and (not has_cost or derived_nil):
            borrowed = borrow_cost(key, government, years, guide.norm_name(minor))
        if borrowed:
            amount, cost_style, kind = borrowed
            if amount < guide.MIN_COST:
                amount = 0
                cost_style = WHITE_MONEY
                kind = "nil"
            cost = amount
            cost_changed = True
            stat = "cost_nil" if amount == 0 else f"cost_{kind}"
            add(cost_column, number_cell(row_number, cost_column, amount, cost_style), stat)
            add(COLUMNS[guide.ATTRIBUTE[10]], number_cell(row_number, COLUMNS[guide.ATTRIBUTE[10]], amount, cost_style), "cost_attr")
            if amount and len(examples["cost"]) < 12:
                examples["cost"].append(f"{description} {amount} {kind}")
        elif not has_cost and (loose or non_asset(description)):
            cost = 0
            cost_changed = True
            add(cost_column, number_cell(row_number, cost_column, 0, WHITE_MONEY), "cost_nil")
            add(COLUMNS[guide.ATTRIBUTE[10]], number_cell(row_number, COLUMNS[guide.ATTRIBUTE[10]], 0, WHITE_MONEY), "cost_nil_attr")

    date_column = COLUMNS["DATE_PLACED_IN_SERVICE"]
    placed = placed_date(value(cells, date_column)) if date_column in cells else None
    if placed is None and not pending:
        bought = guide.as_date(purchase) or guide.year_only_date(purchase)
        if bought:
            placed = bought
            add(date_column, number_cell(row_number, date_column, excel_serial(bought), WHITE_DATE), "date_same_row")
            add(COLUMNS[guide.ATTRIBUTE[8]], number_cell(row_number, COLUMNS[guide.ATTRIBUTE[8]], excel_serial(bought), WHITE_DATE), "date_attr")
        elif specific_name(description, key) or found or major:
            borrowed_date = borrow_date(key, government, years, guide.norm_name(minor), facility)
            if borrowed_date:
                placed, date_style, kind = borrowed_date
                add(date_column, number_cell(row_number, date_column, excel_serial(placed), date_style), f"date_{kind}")
                add(COLUMNS[guide.ATTRIBUTE[8]], number_cell(row_number, COLUMNS[guide.ATTRIBUTE[8]], excel_serial(placed), date_style), "date_attr")
                if len(examples["date"]) < 12:
                    examples["date"].append(f"{description} {placed.isoformat()} {kind}")

    measurable = cost is not None and cost >= guide.MIN_COST and not denied and not pending and not loose and not non_asset(description)
    if measurable and (found or major or specific_name(description, key)) and not asset_type:
        add(COLUMNS["ASSET_TYPE"], text_cell(row_number, COLUMNS["ASSET_TYPE"], "CAPITALIZED"), "type")
        asset_type = "CAPITALIZED"
        if COLUMNS["ASSET_CLR_ACCT_ACCOUNT"] not in cells:
            add(COLUMNS["ASSET_CLR_ACCT_ACCOUNT"], text_cell(row_number, COLUMNS["ASSET_CLR_ACCT_ACCOUNT"], "513001"), "clearing")
    if loose and not asset_type and COLUMNS["ASSET_EXP_ACCT_ACCOUNT"] not in cells:
        add(COLUMNS["ASSET_EXP_ACCT_ACCOUNT"], text_cell(row_number, COLUMNS["ASSET_EXP_ACCT_ACCOUNT"], "221012"), "loose_account")
    if asset_type in {"CAPITALIZED", "CIP"} and minor and COLUMNS["ASSET_EXP_ACCT_ACCOUNT"] not in cells and COLUMNS["ASSET_EXP_ACCT_ACCOUNT"] not in additions:
        account = expense_for(minor)
        if account:
            add(COLUMNS["ASSET_EXP_ACCT_ACCOUNT"], text_cell(row_number, COLUMNS["ASSET_EXP_ACCT_ACCOUNT"], account), "expense")

    depreciate = flag == "YES" or (found and found[4] and measurable and not pending)
    if found and measurable and found[4]:
        if flag != "YES":
            add(COLUMNS["DEPRECIATE_FLAG"], text_cell(row_number, COLUMNS["DEPRECIATE_FLAG"], "YES"), "flag")
        if COLUMNS["DEPRN_METHOD_CODE"] not in cells:
            add(COLUMNS["DEPRN_METHOD_CODE"], text_cell(row_number, COLUMNS["DEPRN_METHOD_CODE"], "STL"), "method")
        depreciate = True
    reserve = number(value(cells, COLUMNS["DEPRN_RESERVE"])) if COLUMNS["DEPRN_RESERVE"] in cells else 0
    ytd = number(value(cells, COLUMNS["YTD_DEPRN"])) if COLUMNS["YTD_DEPRN"] in cells else 0
    inputs_changed = cost_changed or date_column in additions or life_column in additions
    if depreciate and measurable and life and life >= 12 and placed and inputs_changed and (reserve or 0) == 0 and (ytd or 0) == 0:
        figures = guide.depreciation(float(cost), 0.0, int(life), placed)
        if figures:
            accumulated, current = figures
            reserve = shillings(accumulated)
            ytd = shillings(current)
            add(COLUMNS["DEPRN_RESERVE"], number_cell(row_number, COLUMNS["DEPRN_RESERVE"], reserve, WHITE_MONEY), "reserve")
            add(COLUMNS["YTD_DEPRN"], number_cell(row_number, COLUMNS["YTD_DEPRN"], ytd, WHITE_MONEY), "ytd")
            add(COLUMNS[guide.ATTRIBUTE[11]], number_cell(row_number, COLUMNS[guide.ATTRIBUTE[11]], reserve, WHITE_MONEY), "reserve_attr")
            add(COLUMNS[guide.ATTRIBUTE[13]], number_cell(row_number, COLUMNS[guide.ATTRIBUTE[13]], ytd, WHITE_MONEY), "ytd_attr")

    if cost is not None:
        carrying = shillings(max(0.0, float(cost) - float(reserve or 0)))
        for column, kind in ((guide.ATTRIBUTE[9], "recoverable"), (guide.ATTRIBUTE[12], "nbv")):
            index = COLUMNS[column]
            current = number(value(cells, index)) if index in cells else None
            if index not in cells or (cost_changed and (current or 0) == 0):
                add(index, number_cell(row_number, index, carrying, WHITE_MONEY), kind)

    evidence = " ".join(part for part in (description, detail, source_description) if part)
    if COLUMNS["SERIAL_NUMBER"] not in cells:
        token = guide.explicit_serial(evidence)
        if token:
            add(COLUMNS["SERIAL_NUMBER"], text_cell(row_number, COLUMNS["SERIAL_NUMBER"], token), "serial")
    if COLUMNS["MODEL_NUMBER"] not in cells:
        token = guide.explicit_model(evidence)
        if token:
            add(COLUMNS["MODEL_NUMBER"], text_cell(row_number, COLUMNS["MODEL_NUMBER"], token), "model")
    if COLUMNS["MANUFACTURER_NAME"] not in cells:
        token = guide.explicit_manufacturer(evidence)
        if token:
            add(COLUMNS["MANUFACTURER_NAME"], text_cell(row_number, COLUMNS["MANUFACTURER_NAME"], token), "manufacturer")

    if COLUMNS[guide.ATTRIBUTE[4]] not in cells and source_description:
        cleaned = guide.clean_description(source_description)
        if cleaned and cleaned.casefold() != description.casefold() and re.search(r"[A-Za-z]{3,}", cleaned):
            add(COLUMNS[guide.ATTRIBUTE[4]], text_cell(row_number, COLUMNS[guide.ATTRIBUTE[4]], cleaned), "description")
            if len(examples["description"]) < 12:
                examples["description"].append(cleaned[:80])
    if COLUMNS[guide.ATTRIBUTE[7]] not in cells and row_index in SK_PURCHASE:
        source_purchase = SK_PURCHASE[row_index]
        parsed = guide.as_date(source_purchase)
        if parsed:
            add(COLUMNS[guide.ATTRIBUTE[7]], number_cell(row_number, COLUMNS[guide.ATTRIBUTE[7]], excel_serial(parsed), WHITE_DATE), "purchase")
        elif guide.year_only_date(source_purchase):
            add(COLUMNS[guide.ATTRIBUTE[7]], text_cell(row_number, COLUMNS[guide.ATTRIBUTE[7]], source_purchase.strip()), "purchase_year")

    if not additions:
        return match.group(0)
    if not apply:
        return match.group(0)
    ordered = []
    for column in sorted(set(cells) | set(additions)):
        ordered.append(additions[column] if column in additions else cells[column][2])
    body = b"".join(ordered)
    attrs = re.sub(rb'spans="\d+:\d+"', b'spans="1:64"', match.group(2))
    return b'<row r="' + match.group(1) + b'"' + attrs + b">" + body + b"</row>"


def read_headers(sheet: bytes) -> None:
    match = ROW.search(sheet)
    cells = parse_row(match.group(3))
    COLUMNS.clear()
    for index, (text, _, _) in cells.items():
        COLUMNS[text] = index
    required = [
        "DESCRIPTION", "BOOK_TYPE_CODE", "LOCATION_SEGMENT3", "ASSET_CATEGORY_MAJOR", "ASSET_CATEGORY_MINOR1",
        "ASSET_CATEGORY_MINOR2", "ASSET_CATEGORY_MINOR3", "ASSET_TYPE", "FIXED_ASSETS_COST", "ASSET_EXP_ACCT_ACCOUNT",
        "ASSET_CLR_ACCT_ACCOUNT", "DATE_PLACED_IN_SERVICE", "DEPRECIATE_FLAG", "DEPRN_METHOD_CODE", "LIFE_IN_MONTHS",
        "DEPRN_RESERVE", "YTD_DEPRN", "SERIAL_NUMBER", "MANUFACTURER_NAME", "MODEL_NUMBER",
        guide.ATTRIBUTE[4], guide.ATTRIBUTE[5], guide.ATTRIBUTE[7], guide.ATTRIBUTE[8], guide.ATTRIBUTE[9],
        guide.ATTRIBUTE[10], guide.ATTRIBUTE[11], guide.ATTRIBUTE[12], guide.ATTRIBUTE[13], guide.ATTRIBUTE[14],
        guide.ATTRIBUTE[15],
    ]
    missing = [name for name in required if name not in COLUMNS]
    if missing:
        raise SystemExit(f"REF header is missing {missing}")


def append_readme(sheet: bytes, note: str) -> bytes:
    numbers = [int(item) for item in re.findall(rb'<row r="(\d+)"', sheet)]
    row_number = max(numbers) + 1 if numbers else 1
    addition = (
        f'<row r="{row_number}" spans="1:1" ht="80" customHeight="1">'
        f'<c r="A{row_number}" s="10" t="inlineStr"><is><t>{escape(note)}</t></is></c></row>'
    )
    sheet = sheet.replace(b"</sheetData>", addition.encode() + b"</sheetData>")
    return re.sub(rb'ref="A1:A\d+"', f'ref="A1:A{row_number}"'.encode(), sheet, count=1)


def ensure_green_money(styles: bytes) -> bytes:
    extra = b'<xf numFmtId="164" fontId="0" fillId="5" borderId="0" xfId="0" applyNumberFormat="1" applyFill="1"/>'
    if extra in styles:
        return styles
    styles = styles.replace(b"</cellXfs>", extra + b"</cellXfs>", 1)
    return styles.replace(b'<cellXfs count="11">', b'<cellXfs count="12">', 1)


def note_for(stats: Counter) -> str:
    return (
        "Gap fill of columns that already had values, using the 2023 guidelines and the SK source register. "
        f"Classes filled: {stats['class']}. "
        f"Costs borrowed or restored: {sum(stats[key] for key in stats if key.startswith('cost_name_') or key.startswith('cost_class_') or key == 'cost_source_cost')}. "
        f"Nil costs on lines that are not assets: {stats['cost_nil']}. "
        f"Placed-in-service dates filled: {sum(stats[key] for key in stats if key.startswith('date_name_') or key.startswith('date_place_') or key == 'date_same_row')}. "
        f"Asset type set where cost is measurable: {stats['type']}. "
        f"Expense accounts: {stats['expense'] + stats['loose_account']}. "
        f"Depreciation reserves calculated: {stats['reserve']}. "
        f"Serials: {stats['serial']}. Models: {stats['model']}. Manufacturers: {stats['manufacturer']}. "
        f"Source descriptions: {stats['description']}. Source purchase dates: {stats['purchase'] + stats['purchase_year']}. "
        "Borrowed amounts are marked only by the cell colour. Work in progress keeps a blank service date. "
        "Generic names with no comparable price, and columns the guidelines do not state, stay blank."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    global REGISTERS, STRINGS
    REGISTERS = guide.Registers(guide.read_headers())
    print("reading SK", flush=True)
    load_sk()
    print(f"sk descriptions {len(SK_DESCRIPTION):,} purchases {len(SK_PURCHASE):,} costs {len(SK_COST):,}", flush=True)
    with zipfile.ZipFile(REF) as workbook:
        STRINGS = load_strings(workbook.read("xl/sharedStrings.xml"))
        sheet = workbook.read("xl/worksheets/sheet1.xml")
        others = [(item.filename, workbook.read(item.filename)) for item in workbook.infolist() if item.filename != "xl/worksheets/sheet1.xml"]
    read_headers(sheet)
    print("indexing donors", flush=True)
    index_donors(sheet)
    stats: Counter = Counter()
    examples = {"class": [], "cost": [], "date": [], "description": []}
    print("filling", flush=True)
    filled = ROW.sub(lambda match: update_row(match, stats, examples, args.apply), sheet)
    print("STATS")
    for key, count in sorted(stats.items()):
        if count:
            print(f"{count}\t{key}")
    for label, items in examples.items():
        print("---", label)
        for item in items[:12]:
            print(item)
    if not args.apply:
        print("dry run only; pass --apply to write")
        return
    styles = None
    rewritten = []
    for name, data in others:
        if name == "xl/styles.xml" and stats["cost_class_3"] + stats["cost_name_3"]:
            data = ensure_green_money(data)
        if name == "xl/worksheets/sheet2.xml":
            data = append_readme(data, note_for(stats))
        rewritten.append((name, data))
    temporary = REF.with_suffix(".tmp.xlsx")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as target:
        for name, data in rewritten:
            target.writestr(name, data)
        target.writestr("xl/worksheets/sheet1.xml", filled)
    temporary.replace(REF)
    print("wrote", REF, REF.stat().st_size)


if __name__ == "__main__":
    main()
