"""Fill blank purchase costs from comparable assets, then calculate depreciation.

Existing purchase prices stay as they are, with the default white background.
Borrowed prices are coloured by source and explained in Remarks.
"""

import re
import zipfile
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

PATH = Path(
    r"D:\coding\ugift-data-analysis\outputs\asset-register-2026-09-23"
    r"\REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
)
ROW = re.compile(rb'<row r="(\d+)"([^>]*)>(.*?)</row>', re.S)
CELL = re.compile(
    rb'<c r="(BC|BA|AY|AM|AL|AK|AI|AH|AG|AF|M|I|E|B)(\d+)"[^>]*(?:/>|>.*?</c>)',
    re.S,
)
ALL_CELLS = re.compile(rb'<c r="([A-Z]+)(\d+)"[^>]*(?:/>|>.*?</c>)', re.S)
AS_OF = date(2026, 9, 30)
AS_OF_INDEX = 2026 * 12 + 9
FY_START_INDEX = 2026 * 12 + 7
STRINGS: list[str] = []
GENERIC = {
    "medical equipment", "equipment", "furniture", "school furniture",
    "audio visual equipment", "laboratory tools", "laboratory tool",
    "inspection device", "buildings", "non residential buildings",
    "residential buildings", "land", "office land", "school land",
    "item", "set", "other", "machine", "metallic", "schools", "hospitals",
    "good", "functional", "faulty", "assorted", "accessory", "accessories",
}
MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


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
    return (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&#10;", " ")
    )


def escape(text: str) -> str:
    cleaned = "".join(character for character in text if character >= " " or character == "\t")
    return cleaned.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_strings(xml: bytes) -> list[str]:
    strings = []
    for item in re.finditer(rb"<si>(.*?)</si>", xml, re.S):
        parts = re.findall(rb"<t[^>]*>(.*?)</t>", item.group(1), re.S)
        strings.append("".join(unescape(part.decode("utf-8", "replace")) for part in parts))
    return strings


def cell_text(cell: bytes) -> str:
    if b't="s"' in cell[:180]:
        match = re.search(rb"<v>(\d+)</v>", cell)
        if match:
            index = int(match.group(1))
            if index < len(STRINGS):
                return STRINGS[index].strip()
    match = re.search(rb"<t[^>]*>(.*?)</t>|<v>(.*?)</v>", cell, re.S)
    if not match:
        return ""
    raw = match.group(1) if match.group(1) is not None else match.group(2)
    return unescape(raw.decode("utf-8", "replace")).strip()


def shillings(value: float) -> int:
    return int(Decimal(str(round(value, 2))).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def stated_money(text: str) -> float | None:
    if not text:
        return None
    compact = text.replace(",", "").replace(" ", "")
    if re.fullmatch(r"\d+(?:\.\d+)?", compact):
        value = float(compact)
        return value if value > 0 else None
    if re.search(r"(?:=|/=|ugx|shs)", text, re.I):
        match = re.search(r"\d[\d,]*(?:\.\d+)?", text)
        if match:
            value = float(match.group(0).replace(",", ""))
            return value if value > 0 else None
    return None


def stated_number(text: str) -> float | None:
    compact = text.replace(",", "").strip()
    if re.fullmatch(r"-?\d+(?:\.\d+)?", compact):
        return float(compact)
    return None


def norm_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def usable_name(name: str) -> bool:
    return bool(name) and len(name) >= 4 and name not in GENERIC and not re.fullmatch(r"\d+", name)


def clean_lg(text: str) -> str:
    text = text.replace("\\-", "-").replace("\\", "")
    return re.sub(r"\s+", " ", text).strip()


def norm_lg(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean_lg(text).casefold()).strip()


def years_in(text: str) -> set[int]:
    years = {int(year) for year in re.findall(r"(?:19|20)\d{2}", text)}
    match = re.fullmatch(
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?,?\s+(\d{2})",
        text.strip(),
        re.I,
    )
    if match:
        year = int(match.group(2))
        years.add(2000 + year if year < 70 else 1900 + year)
    return years


def row_years(purchase: str, placed: str) -> tuple[int, ...]:
    found = years_in(purchase)
    if not found:
        found = years_in(placed)
    return tuple(sorted(found))


def safe_date(year: int, month: int, day: int) -> date | None:
    if not (1990 <= year <= 2035 and 1 <= month <= 12 and 1 <= day <= 31):
        return None
    try:
        return date(year, month, min(day, 28 if month == 2 else 30 if month in {4, 6, 9, 11} else 31))
    except ValueError:
        return None


def parse_date(text: str) -> date | None:
    value = text.strip()
    if not value or re.fullmatch(r"(?:19|20)\d{2}", value):
        return None
    doubled = re.fullmatch(r"(\d{1,2}/\d{1,2}/\d{4})\1", value)
    if doubled:
        value = doubled.group(1)
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", value)
    if match:
        return safe_date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    match = re.fullmatch(r"(\d{4})-(\d{2})", value)
    if match:
        return safe_date(int(match.group(1)), int(match.group(2)), 1)
    match = re.fullmatch(r"(\d{5})", value)
    if match:
        serial = int(match.group(1))
        if 20000 <= serial <= 60000:
            return date(1899, 12, 30) + timedelta(days=serial)
        return None
    match = re.fullmatch(r"(\d{1,2})[./](\d{1,2})[./](\d{2,4})", value)
    if match:
        first, second, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
        if year < 100:
            year += 2000 if year < 70 else 1900
        if first > 12:
            return safe_date(year, second, first)
        if second > 12:
            return safe_date(year, first, second)
        return safe_date(year, second, first)
    match = re.search(
        r"(\d{1,2})?(?:st|nd|rd|th)?\s*[-/]?\s*"
        r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
        r"jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
        r"\.?,?\s*[-/]?\s*(\d{2,4})",
        value,
        re.I,
    )
    if match and len(re.sub(r"[^a-z]", "", value.casefold())) <= 12:
        month = MONTHS[match.group(2)[:3].lower()]
        year = int(match.group(3))
        if year < 100:
            year += 2000 if year < 70 else 1900
        day = int(match.group(1) or 1)
        return safe_date(year, month, day)
    return None


def service_months(placed: date, life: int) -> tuple[int, int]:
    start = placed.year * 12 + placed.month
    if start > AS_OF_INDEX:
        return 0, 0
    end = min(AS_OF_INDEX, start + life - 1)
    months = end - start + 1
    overlap_start = max(start, FY_START_INDEX)
    overlap_end = min(end, AS_OF_INDEX)
    return months, max(0, overlap_end - overlap_start + 1)


def year_distance(target: tuple[int, ...], donor: tuple[int, ...]) -> int | None:
    if not target or not donor:
        return None
    return min(abs(left - right) for left in target for right in donor)


def common_life(values: list[int]) -> int:
    counts: dict[int, int] = defaultdict(int)
    for value in values:
        counts[value] += 1
    top = max(counts.values())
    tied = [value for value, count in counts.items() if count == top]
    if len(tied) == 1:
        return tied[0]
    middle = median(values)
    return min(tied, key=lambda value: (abs(value - middle), value))


def median(prices: list[int]) -> float:
    ordered = sorted(prices)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def groups_for(name_bucket: dict, governments: tuple[str, ...], minor: str, target_years: tuple[int, ...]) -> list:
    candidates = []
    for government in governments:
        by_minor = name_bucket.get(government, {})
        if minor:
            slices = []
            if minor in by_minor:
                slices.append(by_minor[minor])
            if "" in by_minor:
                slices.append(by_minor[""])
        else:
            slices = list(by_minor.values())
        for yearly in slices:
            candidates.extend((government, years, prices) for years, prices in yearly.items())
    if not candidates or not target_years:
        return candidates
    dated = [item for item in candidates if item[1]]
    if not dated:
        return candidates
    best = min(year_distance(target_years, item[1]) for item in dated)
    return [item for item in dated if year_distance(target_years, item[1]) == best]


def borrow(index: dict, cache: dict, name: str, government: str, years: tuple[int, ...], minor: str):
    key = (name, government, years, minor)
    if key in cache:
        return cache[key]
    name_bucket = index.get(name)
    if not name_bucket:
        cache[key] = None
        return None
    result = None
    if government and government in name_bucket:
        groups = groups_for(name_bucket, (government,), minor, years)
        if groups:
            result = (1, groups)
    if result is None and government:
        others = tuple(item for item in name_bucket if item != government)
        groups = groups_for(name_bucket, others, minor, years) if others else []
        if groups:
            result = (2, groups)
    if result is None and not government:
        groups = groups_for(name_bucket, tuple(name_bucket), minor, years)
        if groups:
            result = (3, groups)
    cache[key] = result
    return result


def year_phrase(groups: list) -> str:
    years = sorted({year for _, donor_years, _ in groups for year in donor_years})
    if not years:
        return "purchase year not stated"
    if len(years) == 1:
        return f"purchase year {years[0]}"
    if len(years) <= 3:
        return "purchase years " + " and ".join(str(year) for year in years)
    return f"purchase years {years[0]}-{years[-1]}"


def source_note(method: int, groups: list, displays: dict, name: str, kind: str) -> str:
    governments = sorted({displays.get((name, group[0]), group[0]) for group in groups if group[0]})
    if len(governments) == 1:
        government = governments[0]
    elif governments:
        government = f"{len(governments)} local governments"
    else:
        government = "local government not stated"
    count = sum(len(values) for _, _, values in groups)
    if kind == "life":
        label = "Borrowed life"
        counted = "one asset with the same name" if count == 1 else f"the most common life of {count} assets with the same name"
    else:
        label = "Borrowed purchase cost"
        counted = "one asset with the same name" if count == 1 else f"the median price of {count} assets with the same name"
    period = year_phrase(groups)
    if method == 1:
        return f"{label} from the same local government ({government}), {period}, {counted}."
    if method == 2:
        where = "another local government" if len(governments) == 1 else "other local governments"
        return f"{label} from {where} ({government}), {period}, {counted}."
    return f"{label} from the whole register ({government}), {period}, {counted}."


def take(index: dict, cache: dict, displays: dict, name: str, government: str, years: tuple[int, ...], minor: str, kind: str):
    key = (kind, name, government, years, minor)
    if key in cache:
        return cache[key]
    found = borrow(index, {}, name, government, years, minor)
    if not found:
        cache[key] = None
        return None
    method, groups = found
    values = [value for _, _, bucket in groups for value in bucket]
    chosen = common_life(values) if kind == "life" else shillings(median(values))
    cache[key] = (method, chosen, source_note(method, groups, displays, name, kind))
    return cache[key]


def add_donor(index: dict, displays: dict, name: str, government: str, years: tuple[int, ...], minor: str, value: int, display: str) -> None:
    slot = index.setdefault(name, {}).setdefault(government, {}).setdefault(minor, {})
    slot.setdefault(years, []).append(value)
    if display:
        displays[(name, government)] = display


def text_cell(row_number: str, column: int, value: str) -> bytes:
    ref = f"{column_letters(column)}{row_number}"
    return f'<c r="{ref}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'.encode()


def number_cell(row_number: str, column: int, value: int, style: int | None = None) -> bytes:
    ref = f"{column_letters(column)}{row_number}"
    style_attr = f' s="{style}"' if style else ""
    return f'<c r="{ref}"{style_attr}><v>{value}</v></c>'.encode()


def patch_styles(xml: bytes) -> bytes:
    if b"FF9DC3E6" in xml:
        return xml
    fills = (
        b'<fill><patternFill patternType="solid"><fgColor rgb="FF9DC3E6"/>'
        b'<bgColor indexed="64"/></patternFill></fill>'
        b'<fill><patternFill patternType="solid"><fgColor rgb="FFF4B183"/>'
        b'<bgColor indexed="64"/></patternFill></fill>'
        b'<fill><patternFill patternType="solid"><fgColor rgb="FFC6EFCE"/>'
        b'<bgColor indexed="64"/></patternFill></fill>'
    )
    styles = (
        b'<xf numFmtId="0" fontId="0" fillId="2" borderId="0" xfId="0" applyFill="1"/>'
        b'<xf numFmtId="0" fontId="0" fillId="3" borderId="0" xfId="0" applyFill="1"/>'
        b'<xf numFmtId="0" fontId="0" fillId="4" borderId="0" xfId="0" applyFill="1"/>'
    )
    xml = xml.replace(b'<fills count="2">', b'<fills count="5">', 1)
    xml = xml.replace(b"</fills>", fills + b"</fills>", 1)
    xml = xml.replace(b'<cellXfs count="1">', b'<cellXfs count="4">', 1)
    xml = xml.replace(b"</cellXfs>", styles + b"</cellXfs>", 1)
    return xml


def add_readme(xml: bytes) -> bytes:
    if b"white background" in xml:
        return xml
    notes = [
        "Purchase costs already recorded in the register are unchanged and have a white background.",
        "Blue purchase costs are borrowed from the same local government. The same purchase year is used first, then the nearest year.",
        "Orange purchase costs are borrowed from another local government, using the same purchase year or the nearest year.",
        "Green purchase costs are borrowed from the whole register. This is used only when the asset's own local government is not stated.",
        "A borrowed cost is the median price of assets with the same name. Where both assets have a class, the class must match. The source is written in Remarks.",
        "Useful life already recorded is unchanged and has a white background. A missing life uses the same blue, orange, and green sources. The value is the most common life of the matching assets, and its source is written in Remarks.",
        "Straight-line depreciation is calculated to 30 September 2026 where cost, residual value, life in months, and the month placed in service are known. Monthly charge = (cost - residual) / life in months. Accumulated depreciation counts each month from the placed-in-service month through September 2026 and stops at the end of the useful life. Year-to-date depreciation is the July-September 2026 portion. Net book value is cost minus accumulated depreciation. Amounts already recorded in those columns were left unchanged. Residual value follows the 2023 guidelines: nil unless a residual was already recorded.",
    ]
    rows = [int(number) for number in re.findall(rb'<row r="(\d+)"', xml)]
    start = max(rows) + 1 if rows else 1
    extra = []
    for offset, note in enumerate(notes):
        number = start + offset
        extra.append(
            f'<row r="{number}" spans="1:1" x14ac:dyDescent="0.35">'
            f'<c r="A{number}" t="inlineStr"><is><t>{escape(note)}</t></is></c></row>'
        )
    xml = xml.replace(b"</sheetData>", "".join(extra).encode() + b"</sheetData>", 1)
    end = start + len(notes) - 1
    xml = re.sub(rb'<dimension ref="[^"]*"', f'<dimension ref="A1:A{end}"'.encode(), xml, count=1)
    return xml


def ensure_writable(path: Path) -> None:
    try:
        handle = open(path, "r+b")
    except PermissionError:
        import win32com.client

        workbook = win32com.client.GetObject(str(path.resolve()))
        application = workbook.Application
        workbook.Close(SaveChanges=False)
        if application.Workbooks.Count == 0:
            application.Quit()
        return
    handle.close()


def check_examples() -> None:
    assert parse_date("2024-03-08") == date(2024, 3, 8)
    assert parse_date("20/9/2025") == date(2025, 9, 20)
    assert parse_date("20/9/202520/9/2025") == date(2025, 9, 20)
    assert parse_date("Feb, 2024") == date(2024, 2, 1)
    assert parse_date("12th/June/2024") == date(2024, 6, 12)
    assert parse_date("7TH JULY 2024") == date(2024, 7, 7)
    assert parse_date("June 2024") == date(2024, 6, 1)
    assert parse_date("Nov 25") == date(2025, 11, 1)
    assert parse_date("2024") is None
    assert parse_date("Health") is None
    assert shillings((55_000_000 / 120) * 12) == 5_500_000
    assert common_life([60, 60, 120]) == 60
    assert common_life([60, 120]) == 60
    months, ytd = service_months(date(2024, 3, 8), 120)
    assert months == 31 and ytd == 3


def main() -> None:
    check_examples()
    ensure_writable(PATH)
    global STRINGS
    print("reading", flush=True)
    with zipfile.ZipFile(PATH) as source:
        pieces = []
        sheet = b""
        for item in source.infolist():
            data = source.read(item.filename)
            if item.filename == "xl/worksheets/sheet1.xml":
                sheet = data
            elif item.filename == "xl/styles.xml":
                pieces.append((item.filename, patch_styles(data)))
            elif item.filename == "xl/worksheets/sheet2.xml":
                pieces.append((item.filename, add_readme(data)))
            elif item.filename == "xl/sharedStrings.xml":
                STRINGS = load_strings(data)
                pieces.append((item.filename, data))
            else:
                pieces.append((item.filename, data))

    print("indexing", flush=True)
    costs: dict = {}
    lives: dict = {}
    displays: dict = {}
    pending = []
    for match in ROW.finditer(sheet):
        if match.group(1) == b"1":
            continue
        cells = {found.group(1).decode(): found.group(0) for found in CELL.finditer(match.group(3))}
        name = norm_name(cell_text(cells.get("B", b"")))
        minor = norm_name(cell_text(cells.get("E", b"")))
        government_text = clean_lg(cell_text(cells.get("I", b"")))
        government = norm_lg(government_text)
        purchase = cell_text(cells.get("AY", b""))
        placed_text = cell_text(cells.get("AF", b""))
        years = row_years(purchase, placed_text)
        cost = stated_money(cell_text(cells.get("M", b"")))
        if cost and usable_name(name):
            add_donor(costs, displays, name, government, years, minor, shillings(cost), government_text)
        life_text = stated_number(cell_text(cells.get("AI", b"")))
        life = int(life_text) if life_text and life_text > 0 else None
        if life and life >= 12 and usable_name(name):
            add_donor(lives, displays, name, government, years, minor, life, government_text)
        salvage = stated_number(cell_text(cells.get("AM", b"")))
        reserve = stated_number(cell_text(cells.get("AK", b"")))
        ytd = stated_number(cell_text(cells.get("AL", b"")))
        nbv = stated_number(cell_text(cells.get("BA", b"")))
        flag = cell_text(cells.get("AG", b""))
        method_code = cell_text(cells.get("AH", b""))
        placed = parse_date(placed_text)
        usable_life = life if life and life >= 12 else None
        needs_cost = cost is None and usable_name(name)
        needs_life = life is None and usable_name(name) and flag != "NO"
        needs_figures = (
            flag == "YES" and cost is not None and usable_life
            and (reserve is None or ytd is None or nbv is None or salvage is None)
        )
        if needs_cost or needs_life or needs_figures:
            pending.append((
                match.group(1), name, government, years, minor, cost, salvage,
                usable_life, life is None, placed, reserve, ytd, nbv, flag, method_code,
            ))

    print("matching", len(pending), flush=True)
    changes = {}
    stats = {
        "cost_same": 0, "cost_other": 0, "cost_register": 0,
        "life_same": 0, "life_other": 0, "life_register": 0,
        "reserve": 0, "ytd": 0, "nbv": 0, "salvage": 0,
    }
    cache: dict = {}
    for row_id, name, government, years, minor, cost, salvage, life, borrow_life, placed, reserve, ytd, nbv, flag, method_code in pending:
        writes: dict[str, object] = {}
        notes = []
        if cost is None and usable_name(name):
            found = take(costs, cache, displays, name, government, years, minor, "cost")
            if found:
                method, cost, note = found
                writes["cost"] = (cost, method)
                notes.append(note)
                stats[["cost_same", "cost_other", "cost_register"][method - 1]] += 1
        if borrow_life and usable_name(name) and flag != "NO":
            found = take(lives, cache, displays, name, government, years, minor, "life")
            if found:
                method, life, note = found
                writes["life"] = (life, method)
                notes.append(note)
                stats[["life_same", "life_other", "life_register"][method - 1]] += 1
                if not flag:
                    writes["flag"] = "YES"
                    flag = "YES"
                if not method_code:
                    writes["method"] = "STL"
        if notes:
            writes["notes"] = notes
        depreciates = flag == "YES"
        if depreciates and salvage is None and cost is not None and life and placed:
            salvage = 0
            writes["salvage"] = 0
            stats["salvage"] += 1
        if depreciates and cost is not None and salvage is not None and life and life >= 12 and placed and salvage < cost:
            months, ytd_months = service_months(placed, life)
            depreciable = cost - salvage
            monthly = depreciable / life
            accumulated = min(depreciable, monthly * months)
            current = monthly * ytd_months
            if accumulated >= depreciable - 0.5 and ytd_months:
                current = max(0, depreciable - monthly * (months - ytd_months))
            if reserve is None:
                writes["reserve"] = shillings(accumulated)
                stats["reserve"] += 1
            if ytd is None:
                writes["ytd"] = shillings(current)
                stats["ytd"] += 1
        used_reserve = reserve if reserve is not None else writes.get("reserve")
        if nbv is None and cost is not None and used_reserve is not None:
            writes["nbv"] = max(0, shillings(float(cost) - float(used_reserve)))
            stats["nbv"] += 1
        if writes:
            changes[row_id] = writes
    del pending, costs, lives, displays, cache
    print(stats, "rows", len(changes), flush=True)

    def update_row(match: re.Match) -> bytes:
        change = changes.get(match.group(1))
        if not change:
            return match.group(0)
        row_number = match.group(1).decode()
        present = {
            column_number(found.group(1).decode()): found.group(0)
            for found in CELL.finditer(match.group(3))
        }
        # Keep every original cell, including columns this pattern does not read.
        all_cells = {
            column_number(found.group(1).decode()): found.group(0)
            for found in ALL_CELLS.finditer(match.group(3))
        }
        if "cost" in change:
            amount, style = change["cost"]
            all_cells[13] = number_cell(row_number, 13, amount, style)
        if "life" in change and stated_number(cell_text(present.get(35, b""))) is None:
            amount, style = change["life"]
            all_cells[35] = number_cell(row_number, 35, amount, style)
        if "flag" in change and not cell_text(present.get(33, b"")):
            all_cells[33] = text_cell(row_number, 33, "YES")
        if "method" in change and not cell_text(present.get(34, b"")):
            all_cells[34] = text_cell(row_number, 34, "STL")
        if "notes" in change:
            current = cell_text(present.get(55, b""))
            fresh = [note for note in change["notes"] if note not in current]
            if fresh:
                all_cells[55] = text_cell(row_number, 55, f"{current} {' '.join(fresh)}".strip())
        if "salvage" in change and 39 not in present:
            all_cells[39] = number_cell(row_number, 39, change["salvage"])
        if "reserve" in change and stated_number(cell_text(present.get(37, b""))) is None:
            all_cells[37] = number_cell(row_number, 37, change["reserve"])
        if "ytd" in change and stated_number(cell_text(present.get(38, b""))) is None:
            all_cells[38] = number_cell(row_number, 38, change["ytd"])
        if "nbv" in change and stated_number(cell_text(present.get(53, b""))) is None:
            all_cells[53] = number_cell(row_number, 53, change["nbv"])
        body = b"".join(xml for _, xml in sorted(all_cells.items()))
        return b'<row r="' + match.group(1) + b'"' + match.group(2) + b">" + body + b"</row>"

    print("writing", flush=True)
    sheet = ROW.sub(update_row, sheet)
    temporary = PATH.with_suffix(".tmp.xlsx")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as target:
        for name, data in pieces:
            target.writestr(name, data)
        target.writestr("xl/worksheets/sheet1.xml", sheet)
    temporary.replace(PATH)
    print("size", PATH.stat().st_size)
    print(stats)


if __name__ == "__main__":
    main()
