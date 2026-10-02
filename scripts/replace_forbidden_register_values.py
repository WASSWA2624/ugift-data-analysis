"""Replace PENDING CLASSIFICATION and Pending calculation with calculated values.

Classification comes from the item, its description, or the cited source row.
Depreciation is straight-line to 30 September 2026. A measured cost is taken from
the row, the cited source, a unit price in the remarks, or a comparable asset.
Where no cost can be measured, accumulated and year-to-date depreciation are 0.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_guideline_registers as guide
from fill_borrowed_costs import (
    add_donor,
    groups_for,
    median,
    norm_name,
    shillings,
    usable_name,
)
from fill_register_gaps import load_strings
from merge_shared_asset_registers import canonical_item, clean
from patch_register_workbook import CELL, apply_updates, cell_value, worksheet_parts

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "outputs" / "asset-register" / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
GROUPED = ROOT / "raw-data-grouped"
EPOCH = date(1899, 12, 30)
UNIT = re.compile(r"\s*\[item \d+ of \d+\]\s*$", re.I)
FILE_RE = re.compile(r"Source file:\s*([^;]+)")
LOC_RE = re.compile(r"Source location:\s*(.+?)\s+row\s+(\d+)", re.I)
UNIT_PRICE_RE = re.compile(r"(?i)unit price\s*(?:ugx|ush|ugshs|shs)?\s*[:\-]?\s*([\d,]+(?:\.\d+)?)")
VARIANT = re.compile(
    r"(?i)^(?:adult|paediat\w*|pediat\w*|neonat\w*|infant|child|children|small|medium|large|"
    r"x{1,2}l|brown|grey|gray|black|white|blue|green|silver|red|yellow|light brown|"
    r"pcs|pc|pieces?|\d[\d./]*)$"
)
HEADER_ITEM = re.compile(r"(?i)equipment\s*/?\s*item")
KEEP = {
    "A": "book",
    "B": "item",
    "C": "major",
    "D": "minor1",
    "E": "minor2",
    "G": "type",
    "M": "cost",
    "V": "expense",
    "AE": "clearing",
    "AF": "placed",
    "AG": "flag",
    "AH": "method",
    "AI": "life",
    "AK": "reserve",
    "AL": "ytd",
    "AM": "salvage",
    "BA": "description",
    "BD": "purchase",
    "BF": "recoverable",
    "BG": "attr_cost",
    "BH": "attr_reserve",
    "BI": "nbv",
    "BJ": "attr_ytd",
    "AP": "tag",
    "BK": "status",
    "BL": "remarks",
}
CLEAR = ("", "", "", 0, False)
BUILDING = ("BUILDINGS AND STRUCTURES", "BUILDINGS OTHER THAN DWELLINGS", "NON RESIDENTIAL BUILDINGS", 600, True)
STRUCTURE = ("BUILDINGS AND STRUCTURES", "STRUCTURES", "OTHER STRUCTURES", 240, True)
NETWORK = ("BUILDINGS AND STRUCTURES", "STRUCTURES", "ICT NETWORK LINES", 240, True)
FURNITURE = ("MACHINERY AND EQUIPMENT", "OTHER MACHINERY AND EQUIPMENT", "FURNITURE AND FITTINGS", 60, True)
MEDICAL = ("MACHINERY AND EQUIPMENT", "OTHER MACHINERY AND EQUIPMENT", "MED LAB RESEARCH APPLIANCES", 60, True)
ELECTRICAL = ("MACHINERY AND EQUIPMENT", "OTHER MACHINERY AND EQUIPMENT", "ELECTRICAL MACHINERY", 60, True)
ICT = ("MACHINERY AND EQUIPMENT", "ICT EQUIPMENT", "OTHER ICT EQUIPMENT", 60, True)
LIGHT_ICT = ("MACHINERY AND EQUIPMENT", "ICT EQUIPMENT", "LIGHT ICT HARDWARE", 60, True)
SIZE_CODE = re.compile(r"^\d+(?:\.\d+)?/\d+(?:\.\d+)?$")
MONEY_STYLE = {1: 4, 2: 1, 3: 11}
WHITE_MONEY = 3
CLASS_PENDING = "PENDING CLASSIFICATION"
CALC_PENDING = "Pending calculation"


def bare(text: object) -> str:
    return UNIT.sub("", clean(text)).strip()


def amount(value: object) -> float | None:
    if isinstance(value, bool) or value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        compact = value.replace(",", "").strip()
        if re.fullmatch(r"-?\d+(?:\.\d+)?", compact):
            return float(compact)
    return None


def serial_date(value: object) -> date | None:
    number = amount(value)
    if number is None or not 20000 <= number <= 60000:
        return None
    return EPOCH + timedelta(days=int(number))


def years_of(row: dict) -> tuple[int, ...]:
    found = set()
    for key in ("purchase", "placed"):
        text = str(row.get(key) or "")
        found.update(int(year) for year in re.findall(r"(?:19|20)\d{2}", text))
        parsed = serial_date(row.get(key))
        if parsed:
            found.add(parsed.year)
    return tuple(sorted(found))


def service_months(placed: date, life: int) -> tuple[int, int]:
    start = placed.year * 12 + placed.month
    as_of = 2026 * 12 + 9
    if start > as_of:
        return 0, 0
    end = min(as_of, start + life - 1)
    months = end - start + 1
    overlap_start = max(start, 2026 * 12 + 7)
    overlap_end = min(end, as_of)
    return months, max(0, overlap_end - overlap_start + 1)


def depreciation_figures(cost: float, life: int, placed: date, salvage: float) -> tuple[int, int]:
    depreciable = cost - salvage
    if life < 12 or depreciable <= 0 or placed > guide.AS_OF:
        return 0, 0
    months, ytd_months = service_months(placed, life)
    monthly = depreciable / life
    accumulated = min(depreciable, monthly * months)
    current = monthly * ytd_months
    if accumulated >= depreciable - 0.5 and ytd_months:
        current = max(0.0, depreciable - monthly * (months - ytd_months))
    reserve = min(shillings(accumulated), shillings(depreciable))
    ytd = min(shillings(current), reserve)
    return reserve, ytd


def column_of(reference: str) -> str:
    return "".join(character for character in reference if character.isalpha())


def row_cells(raw: bytes, shared: list[str]) -> dict[str, object]:
    values = {}
    for match in CELL.finditer(raw):
        xml = match.group()
        reference = xml.split(b'r="', 1)[1].split(b'"', 1)[0].decode()
        column = column_of(reference)
        if column in KEEP:
            values[KEEP[column]] = cell_value(xml, shared)
    return values


def classify_text(registers: guide.Registers, text: str):
    text = bare(text)
    if not text:
        return None
    equivalent = guide.reviewed_equivalent(text, "")
    found = registers.classify(equivalent or text)
    if found:
        return found
    disc = re.sub(r"(?i)\bhard disc\b", "hard disk", text)
    if disc != text:
        return registers.classify(disc)
    return None


def non_asset_name(text: str) -> bool:
    text = bare(text)
    if not text:
        return False
    return bool(
        guide.LOOSE.search(text)
        or guide.CONSUMABLE.search(text)
        or guide.REPAIR.search(text)
        or guide.SERVICE.search(text)
        or guide.TOTAL_LINE.search(text)
        or guide.NATURAL.search(text)
    )


def robust_prices(prices: list[int]) -> list[int]:
    if len(prices) < 3:
        return prices
    centre = median(prices)
    if not centre:
        return prices
    kept = [price for price in prices if centre / guide.PRICE_BAND <= price <= centre * guide.PRICE_BAND]
    return kept or prices


def choose_price(name_bucket: dict, government: str, minor: str, years: tuple[int, ...]):
    if government and government in name_bucket:
        groups = groups_for(name_bucket, (government,), minor, years)
        if groups:
            prices = robust_prices([price for _, _, bucket in groups for price in bucket])
            if prices:
                return 1, shillings(median(prices))
    others = tuple(item for item in name_bucket if item != government)
    if others:
        groups = groups_for(name_bucket, others, minor, years)
        if groups:
            prices = robust_prices([price for _, _, bucket in groups for price in bucket])
            if prices:
                return 2, shillings(median(prices))
    return None


def borrow_price(index: dict, names: list[str], government: str, minor: str, years: tuple[int, ...]):
    for name in names:
        key = guide.borrow_key(name)
        if not usable_name(key) or key in guide.GENERIC_NAMES or guide.GENERIC_HEAD.match(name):
            continue
        bucket = index.get(key)
        if not bucket:
            continue
        found = choose_price(bucket, government, norm_name(minor), years)
        if found:
            return found
        found = choose_price(bucket, government, "", years)
        if found:
            return found
    return None


def borrow_class(index: dict, government: str, minor: str, years: tuple[int, ...]):
    minor_key = norm_name(minor)
    bucket = index.get(minor_key)
    if not bucket:
        return None
    return choose_price(bucket, government, "", years)


class SourceBook:
    def __init__(self) -> None:
        self.paths: dict[str, Path | None] = {}
        self.sheets: dict[tuple[str, str], tuple[list[list[str]], dict]] = {}

    def locate(self, relative: str) -> Path | None:
        key = relative.strip().replace("\\", "/")
        if key in self.paths:
            return self.paths[key]
        direct = GROUPED / key
        self.paths[key] = direct if direct.exists() else None
        return self.paths[key]

    def load(self, relative: str, sheet_name: str):
        path = self.locate(relative)
        if path is None:
            return None
        key = (str(path), sheet_name.casefold())
        if key in self.sheets:
            return self.sheets[key]
        suffix = path.suffix.lower()
        rows: list[list[str]] = []
        if suffix == ".xls":
            import xlrd

            book = xlrd.open_workbook(path, on_demand=True)
            names = {name.casefold(): name for name in book.sheet_names()}
            actual = names.get(sheet_name.casefold())
            if actual is None:
                self.sheets[key] = ([], {})
                return self.sheets[key]
            sheet = book.sheet_by_name(actual)
            for index in range(sheet.nrows):
                rows.append([clean(sheet.cell_value(index, column)) for column in range(min(sheet.ncols, 18))])
            book.release_resources()
        elif suffix == ".docx":
            from merge_shared_asset_registers import docx_tables

            tables = docx_tables(path)
            chosen = None
            for name, table_rows, _section in tables:
                if name.casefold() == sheet_name.casefold():
                    chosen = table_rows
                    break
            if chosen is None:
                number = re.fullmatch(r"table\s+(\d+)", sheet_name, re.I)
                if number:
                    index = int(number.group(1)) - 1
                    if 0 <= index < len(tables):
                        chosen = tables[index][1]
            rows = [[clean(cell) for cell in list(row)[:18]] for row in (chosen or [])]
        elif suffix == ".xlsx":
            from openpyxl import load_workbook

            book = load_workbook(path, read_only=True, data_only=True)
            names = {name.casefold(): name for name in book.sheetnames}
            actual = names.get(sheet_name.casefold())
            if actual is None:
                book.close()
                self.sheets[key] = ([], {})
                return self.sheets[key]
            sheet = book[actual]
            for row in sheet.iter_rows(values_only=True):
                rows.append([clean(value) for value in list(row)[:18]])
            book.close()
        else:
            self.sheets[key] = ([], {})
            return self.sheets[key]
        header = {}
        item_column = 0
        for index, row in enumerate(rows[:40]):
            if any(HEADER_ITEM.search(cell) for cell in row):
                header["header"] = index
                for column, cell in enumerate(row):
                    label = norm_name(cell)
                    if HEADER_ITEM.search(cell):
                        item_column = column
                    elif label == "cost":
                        header["cost"] = column
                    elif "description" in label:
                        header["description"] = column
                break
        header["item"] = item_column
        self.sheets[key] = (rows, header)
        return self.sheets[key]


def citation(remarks: str) -> tuple[str, str, int] | None:
    files = FILE_RE.findall(remarks or "")
    locations = LOC_RE.findall(remarks or "")
    if not files or not locations:
        return None
    return files[-1].strip(), locations[-1][0].strip(), int(locations[-1][1])


def source_context(book: SourceBook, remarks: str, register_item: str):
    found = citation(remarks)
    if not found:
        return None
    relative, sheet, row_number = found
    loaded = book.load(relative, sheet)
    if not loaded or not loaded[0]:
        return None
    rows, header = loaded
    target = bare(register_item).casefold()

    def contains(source_row: list[str]) -> bool:
        if len(target) < 4:
            return False
        return any(bare(cell).casefold() == target or target in bare(cell).casefold() for cell in source_row)

    index = row_number - 1 if 1 <= row_number <= len(rows) else None
    if target and (index is None or not contains(rows[index])):
        hits = [position for position, source_row in enumerate(rows) if contains(source_row)]
        if hits and index is not None:
            index = min(hits, key=lambda position: abs(position + 1 - row_number))
        elif hits:
            index = hits[0]
    if index is None or not 0 <= index < len(rows):
        return None
    current = rows[index]
    item_column = header.get("item", 0)
    for column, cell in enumerate(current):
        if target and bare(cell).casefold() == target:
            item_column = column
            break
    item = current[item_column] if item_column < len(current) else ""
    description = ""
    if "description" in header and header["description"] < len(current):
        description = current[header["description"]]
    extras = [
        bare(cell) for cell in current
        if bare(cell) and bare(cell).casefold() not in {target, "education", "health", "n/a", "na"}
        and not re.fullmatch(r"[\d./]+", bare(cell))
    ]
    cost = None
    if "cost" in header and header["cost"] < len(current):
        cost = amount(current[header["cost"]])
        if cost is not None and re.fullmatch(r"\d{5}", current[header["cost"]]):
            cost = None
    parents = []
    blanks = 0
    for cursor in range(index - 1, header.get("header", -1), -1):
        parent = rows[cursor][item_column] if item_column < len(rows[cursor]) else ""
        parent = bare(parent)
        if not parent:
            blanks += 1
            if blanks > 2 and parents:
                break
            continue
        blanks = 0
        if HEADER_ITEM.search(parent) or re.fullmatch(r"\d+", parent):
            continue
        parents.append(parent)
        if len(parents) >= 8:
            break
    return {
        "item": item, "description": description, "extras": extras, "cost": cost,
        "parents": parents, "sheet": sheet,
    }


def squeeze(text: str) -> str:
    """Join a single letter that was split from the previous word ('Diagnosti c')."""
    return re.sub(r"(?<=[A-Za-z])\s+(?=[A-Za-z]\b)", "", text)


def evidence_class(text: str, life: float | None, tag: str):
    """Classes established by reading the source wording, not by the facility type."""
    text = squeeze(text)
    text = re.sub(r"(?i)\binstrume\s*nt\b", "instrument", text)
    text = re.sub(r"(?i)\bequipme\s*nt\b", "equipment", text)
    text = re.sub(r"(?i)\bdiagnosti\s*c\b", "diagnostic", text)
    if re.search(r"(?i)\bhuman\b", text) and re.search(r"(?i)\b(?:brain|nero|nervous|ear|eye|heart|skeleton|torso|teeth)\b", text):
        return MEDICAL
    if re.search(r"(?i)\b(mesuring|measuring)\s+cylinders?\b|\bdensity bottles?\b|\bfraction\w* columns?\b|\b(?:lei|lie)big condensers?\b|\bplastic funnels?\b|\bmethanol\b|\bmarble chips\b|\boptical pins\b|\bboiling tub", text):
        return CLEAR
    if re.search(r"(?i)\b(?:borax|dichromate|ferricyanide|ferrous cyanide|ferrocyanide|acetate|metabisulp\w*|sulphite|thiosulphate|chlorate|cyanide|bismath\w*|cremate|potassium|sodium)\b", text):
        return CLEAR
    if re.fullmatch(r"(?i)condition", text):
        return CLEAR
    if re.search(r"(?i)\bpestles?\b|\bmayo\b.{0,20}\bscirr?ors?\b", text):
        return MEDICAL
    if re.search(r"(?i)\bdiagnosti\w*\s+equip", text):
        return CLEAR
    if re.search(
        r"(?i)\(\s*\d+\s*(?:g|gm|ml|l)\s*\)|\b(?:acid|hydroxide|sulphate|sulfate|chloride|nitrate|carbonate|monoxide|"
        r"pellets|ethanol|glucose|fructose|sucrose|chloroform|chrolophom|formaldehyde|pepsin|trypsin|phenol|"
        r"phenolphthalein|phenolalein|fehling|oxalic|cupric|lime water|silver nitrate|methyl orange|eosin|"
        r"starch|butan-\d-ol|diastase|enzymes|hydrogen peroxide|magnesium|propan-\d-ol|zinc |aluminum oxide|"
        r"bromine|leishman|iodine solution|benedict|bromothymol|indicator)\b",
        text,
    ) and not re.search(r"(?i)\bcharts?\b", text):
        return CLEAR
    if re.search(r"(?i)\b(lotion bowels?|lotion bowls?|cheatle jars?|humidifier bottles?)\b", text):
        return MEDICAL
    if re.search(r"(?i)\b(models and posters|study charts|wall charts?|reproductive diseases charts?|universal indicator charts?|anatomical models?)\b", text):
        return MEDICAL
    if re.search(r"(?i)\b(?:models?|charts?)\b", text) and re.search(
        r"(?i)\b(?:human|brain|eye|ear|heart|skeleton|torso|nervous|digestive|reproductive|teeth|urinary|dissection)\b",
        text,
    ):
        return MEDICAL
    if re.search(r"(?i)\b(?:optiplex|ideashare|handheld gps|\bgps\b|drones?)\b", text):
        return ICT if re.search(r"(?i)drone|ideashare", text) else LIGHT_ICT
    if re.search(r"(?i)\boracle\b|\bdeveloper suite\b|\bdatabase\b", text):
        return ("OTHER FIXED ASSETS", "INTELLECTUAL PROPERTY PRODUCTS", "COMPUTER SOFTWARE", 60, True)
    if re.search(r"(?i)\b(?:soll(?:er|ar)|solar)\b.*\bcontrollers?\b|\bcontrollers?\b.*\b(?:solar|soll)", text):
        return ELECTRICAL
    if re.search(r"(?i)\bict controllers?\b", text):
        return LIGHT_ICT
    if re.search(r"(?i)\bsaction\b|\bsuction apparatus\b|\binstrument sets?\b|\bdissection\b|drip\s*stands?|\bpulse\b", text):
        return MEDICAL
    if re.search(r"(?i)\bsets?\b", text) and re.search(r"(?i)diagnostic|instrument|mch|stitch|suture", text):
        return MEDICAL
    if re.fullmatch(r"(?i)wall", text):
        return STRUCTURE
    if re.search(r"(?i)\bsteel lockable\b|\bcushioned\b", text):
        return FURNITURE
    if re.search(r"(?i)\btwin house\b|\bstaff houses?\b", text):
        return ("BUILDINGS AND STRUCTURES", "DWELLINGS", "RESIDENTIAL BUILDINGS", 600, True)
    if re.search(r"(?i)\bstaff\b", text) and re.search(r"(?i)\broom\b", text):
        return BUILDING
    if re.search(r"(?i)\bcharts?\b", text) and not re.search(r"(?i)\bsolutions?\b", text):
        return MEDICAL
    if re.search(r"(?i)\b(?:not yet delivered|on-?going constructions)\b", text):
        return CLEAR
    if re.fullmatch(r"(?i)extensions?|sanitation box(?:es)?|items? no\.?|pcs|pc|ppda", text):
        return CLEAR
    if re.search(r"(?i)^ministry of\b|^(?:condition|[a-g])\b.*\b(?:repair|replacement|disposed|out of order|in use|not in use)\b", text):
        return CLEAR
    if re.search(r"(?i)\bgrain silos?\b", text):
        return STRUCTURE
    if re.search(r"(?i)\b(shower roses?|stop corks?|stop cocks?)\b", text):
        return FURNITURE
    if re.search(r"(?i)\btrunking\b", text):
        return NETWORK
    if re.search(r"(?i)\bground penetrating (?:radar|ladder)|\bgpr\b", text):
        return ICT
    if re.search(r"(?i)\b(?:science\s+)?laborator(?:y|ies)\b", text) and re.search(r"(?i)\b(?:unit|block|rooms?|paint|colour|color)\b", text):
        return BUILDING
    if re.fullmatch(r"(?i)hospitals?|schools?", text) and ((life or 0) >= 240 or "BULD" in tag.upper()):
        return BUILDING
    return None


def resolved_class(registers: guide.Registers, row: dict, context: dict | None):
    names = [bare(row.get("description")), bare(row.get("item"))]
    if context:
        names.extend([bare(context.get("description")), bare(context.get("item"))])
        names.extend(context.get("extras") or [])
        current = bare(context.get("item") or row.get("item"))
        variant = VARIANT.match(current) or SIZE_CODE.match(current)
        for parent in context.get("parents") or []:
            if variant or VARIANT.match(parent) or SIZE_CODE.match(parent):
                names.append(f"{parent}, {current}")
                names.append(parent)
            elif classify_text(registers, parent):
                names.append(parent)
                break
    seen = set()
    ordered = []
    for name in names:
        key = name.casefold()
        if name and key not in seen:
            seen.add(key)
            ordered.append(name)
    life = amount(row.get("life"))
    tag = str(row.get("tag") or "")
    for name in ordered:
        found = classify_text(registers, name)
        if found:
            return found, name
        found = evidence_class(name, life, tag)
        if found:
            return found, name
    department = re.search(r"Recorded department/room:\s*([^;]+)", str(row.get("remarks") or ""))
    if department and (VARIANT.match(bare(row.get("item"))) or len(bare(row.get("item"))) <= 4):
        label = bare(department.group(1))
        found = classify_text(registers, label) or evidence_class(label, life, tag)
        if found:
            return found, label
    for name in ordered:
        if non_asset_name(name) or guide.GENERIC_HEAD.match(name):
            return CLEAR, name
    if context and len(bare(row.get("item"))) <= 16:
        blob = squeeze(" ".join([*(context.get("parents") or [])[:4], bare(row.get("item"))]))
        found = evidence_class(blob, life, tag)
        if found:
            return found, blob
        found = classify_text(registers, blob)
        if found:
            return found, blob
    location = f"{(context or {}).get('sheet') or ''} {row.get('remarks') or ''}"
    if re.search(r"(?i)\bland\b", location) and re.search(r"\d", bare(row.get("item"))):
        return ("LAND", "LAND", "LAND", 600, False), bare(row.get("item"))
    return None, bare(row.get("item"))


def measured_cost(row: dict, context: dict | None) -> tuple[float | None, int | None]:
    existing = amount(row.get("cost"))
    if existing is None:
        existing = amount(row.get("attr_cost"))
    if existing is not None:
        return existing, None
    if context and context.get("cost") not in (None, 0):
        return float(context["cost"]), WHITE_MONEY
    match = UNIT_PRICE_RE.search(str(row.get("remarks") or ""))
    if match:
        price = float(match.group(1).replace(",", ""))
        if price > 0:
            return price, WHITE_MONEY
    return None, None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    registers = guide.Registers(guide.read_headers())
    print("reading register", flush=True)
    with zipfile.ZipFile(REF) as workbook:
        shared = load_strings(workbook.read("xl/sharedStrings.xml"))
        stream = workbook.open("xl/worksheets/sheet1.xml")
        affected = {}
        name_costs: dict = {}
        class_costs: dict = {}
        displays: dict = {}
        for is_row, raw in worksheet_parts(stream):
            if not is_row or raw.startswith(b'<row r="1"'):
                continue
            hit = CLASS_PENDING.encode() in raw or CALC_PENDING.encode() in raw
            if not hit and b"<v>" not in raw:
                continue
            values = row_cells(raw, shared) if hit or b'r="M' in raw else None
            if values is None:
                continue
            if hit:
                row_number = int(re.search(rb'\br="([0-9]+)"', raw).group(1))
                affected[row_number] = values
            if hit:
                continue
            cost = amount(values.get("cost"))
            minor = str(values.get("minor2") or "")
            name = bare(values.get("item"))
            if cost is None or cost < guide.MIN_COST or not minor or minor == CLASS_PENDING:
                continue
            government = str(values.get("book") or "")
            price = shillings(cost)
            minor_key = norm_name(minor)
            class_costs.setdefault(minor_key, {}).setdefault(government, {}).setdefault("", {}).setdefault(years_of(values), []).append(price)
            key = guide.borrow_key(name)
            if usable_name(key) and key not in guide.GENERIC_NAMES and not guide.GENERIC_HEAD.match(name):
                add_donor(name_costs, displays, key, government, years_of(values), minor_key, price, government)
        stream.close()
    print(f"affected {len(affected):,} name donors {len(name_costs):,}", flush=True)

    sources = SourceBook()
    updates = []
    stats = Counter()
    unresolved = Counter()
    examples = defaultdict(list)
    for row_number, row in affected.items():
        if row_number % 250 == 0:
            print(f"resolved {len(updates):,} updates through row {row_number}", flush=True)
        needs_class = any(row.get(key) == CLASS_PENDING for key in ("major", "minor1", "minor2"))
        calc_columns = {
            "AK": row.get("reserve"),
            "AL": row.get("ytd"),
            "BH": row.get("attr_reserve"),
            "BJ": row.get("attr_ytd"),
            "BF": row.get("recoverable"),
            "BI": row.get("nbv"),
        }
        needs_calc = any(value == CALC_PENDING for value in calc_columns.values())
        context = None
        found = None
        resolved_name = bare(row.get("item"))
        if needs_class or needs_calc:
            found, resolved_name = resolved_class(registers, row, None)
        missing_cost = amount(row.get("cost")) is None and amount(row.get("attr_cost")) is None
        if (needs_class and found is None) or (needs_calc and missing_cost):
            context = source_context(sources, str(row.get("remarks") or ""), str(row.get("item") or ""))
            if context is None and citation(str(row.get("remarks") or "")):
                stats["source_unread"] += 1
            if context and (found is None or missing_cost):
                found, resolved_name = resolved_class(registers, row, context)
        if needs_class:
            if found and found is not CLEAR and found[0]:
                stats["class_resolved"] += 1
                for column, value in (("C", found[0]), ("D", found[1]), ("E", found[2])):
                    if row.get({"C": "major", "D": "minor1", "E": "minor2"}[column]) == CLASS_PENDING:
                        updates.append({
                            "sheet": "Asset Register",
                            "cell": f"{column}{row_number}",
                            "expected": CLASS_PENDING,
                            "value": value,
                        })
            elif found is CLEAR or non_asset_name(resolved_name) or non_asset_name(bare(row.get("item"))):
                stats["class_cleared"] += 1
                for column in ("C", "D", "E"):
                    if row.get({"C": "major", "D": "minor1", "E": "minor2"}[column]) == CLASS_PENDING:
                        updates.append({
                            "sheet": "Asset Register",
                            "cell": f"{column}{row_number}",
                            "expected": CLASS_PENDING,
                            "value": None,
                        })
            else:
                stats["class_unresolved"] += 1
                label = bare(row.get("item"))
                unresolved[label] += 1
                if len(examples[label]) < 2:
                    parent = context["parents"][0] if context and context.get("parents") else ""
                    source_item = context.get("item") if context else ""
                    examples[label].append(f"row {row_number} | source {source_item} | parent {parent} | {str(row.get('description') or '')[:80]}")
        if not needs_calc:
            continue
        salvage = amount(row.get("salvage")) or 0.0
        cost, cost_style = measured_cost(row, context)
        cost_origin = "existing" if amount(row.get("cost")) is not None or amount(row.get("attr_cost")) is not None else (
            "source" if cost_style == WHITE_MONEY else "none"
        )
        minor = found[2] if found else str(row.get("minor2") or "")
        if minor == CLASS_PENDING:
            minor = ""
        specific_names = []
        if context and context.get("parents") and VARIANT.match(bare(context.get("item") or row.get("item"))):
            specific_names.append(bare(context["parents"][0]))
        specific_names.append(resolved_name)
        specific_names.append(bare(row.get("description")))
        borrowed = None
        if cost is None and minor and found and found[4] and not non_asset_name(resolved_name):
            if str(row.get("type") or "") != "CIP" and not guide.NON_DEPR.search(str(row.get("remarks") or "")):
                borrowed = borrow_price(name_costs, specific_names, str(row.get("book") or ""), minor, years_of(row))
                if borrowed:
                    cost = float(borrowed[1])
                    cost_style = MONEY_STYLE[borrowed[0]]
                    cost_origin = "borrowed"
        life = amount(row.get("life"))
        if (life is None or life < 12) and found and found[3]:
            life = float(found[3])
        elif life is None or life < 12:
            life = float(guide.FALLBACK_LIFE if found and found[4] else 0)
        placed = serial_date(row.get("placed"))
        depreciates = bool(found[4]) if found else str(row.get("flag") or "") == "YES"
        if str(row.get("type") or "") in {"CIP", "EXPENSED", "NOT CAPITALIZED", "NOT RECOGNIZED"}:
            depreciates = str(row.get("type") or "") not in {"CIP", "EXPENSED", "NOT CAPITALIZED", "NOT RECOGNIZED"}
        if non_asset_name(resolved_name) or guide.denies_asset(str(row.get("remarks") or ""), resolved_name, str(row.get("description") or "")):
            depreciates = False
        if str(row.get("type") or "") == "CIP" or guide.NON_DEPR.search(f"{row.get('item') or ''} {row.get('remarks') or ''}"):
            depreciates = False
        if cost is None:
            reserve = ytd = 0
            recoverable = 0
            stats["calc_zero"] += 1
        elif cost < guide.MIN_COST:
            cost = 0
            reserve = ytd = 0
            recoverable = 0
            stats["calc_immaterial"] += 1
        elif depreciates and life and life >= 12 and placed and str(row.get("flag") or "") != "NO":
            reserve, ytd = depreciation_figures(cost, int(life), placed, salvage)
            recoverable = max(0, shillings(cost - reserve))
            stats["calc_" + cost_origin] += 1
        elif depreciates and life and life >= 12 and placed and cost_origin in {"source", "borrowed"}:
            reserve, ytd = depreciation_figures(cost, int(life), placed, salvage)
            recoverable = max(0, shillings(cost - reserve))
            stats["calc_" + cost_origin] += 1
        else:
            reserve = ytd = 0
            recoverable = shillings(cost) if cost else 0
            stats["calc_not_depreciated"] += 1
        calculated = {
            "AK": reserve,
            "AL": ytd,
            "BH": reserve,
            "BJ": ytd,
            "BF": recoverable,
            "BI": recoverable,
        }
        for column, current in calc_columns.items():
            if current == CALC_PENDING:
                updates.append({
                    "sheet": "Asset Register",
                    "cell": f"{column}{row_number}",
                    "expected": CALC_PENDING,
                    "value": calculated[column],
                    "style": WHITE_MONEY,
                })
        if cost_origin in {"source", "borrowed"} and amount(row.get("cost")) is None:
            for column in ("M", "BG"):
                updates.append({
                    "sheet": "Asset Register",
                    "cell": f"{column}{row_number}",
                    "expected": row.get("cost") if column == "M" else row.get("attr_cost"),
                    "value": shillings(cost),
                    "style": cost_style,
                })
            stats["costs_written"] += 1
            if cost >= guide.MIN_COST and depreciates and str(row.get("type") or "") in {"", "PENDING VALUATION"}:
                updates.append({
                    "sheet": "Asset Register",
                    "cell": f"G{row_number}",
                    "expected": row.get("type") or None,
                    "value": "CAPITALIZED",
                })
                if row.get("flag") != "YES":
                    updates.append({
                        "sheet": "Asset Register",
                        "cell": f"AG{row_number}",
                        "expected": row.get("flag") or None,
                        "value": "YES",
                    })
                if row.get("method") != "STL":
                    updates.append({
                        "sheet": "Asset Register",
                        "cell": f"AH{row_number}",
                        "expected": row.get("method") or None,
                        "value": "STL",
                    })
                if not row.get("expense") and minor:
                    account = guide.ANNEX2_BY_MINOR2.get(norm_name(minor))
                    if account:
                        updates.append({
                            "sheet": "Asset Register",
                            "cell": f"V{row_number}",
                            "expected": None,
                            "value": "231" + account[3:],
                        })
                if not row.get("clearing"):
                    updates.append({
                        "sheet": "Asset Register",
                        "cell": f"AE{row_number}",
                        "expected": None,
                        "value": "513001",
                    })
    print("STATS")
    for key, count in sorted(stats.items()):
        print(f"{count}\t{key}")
    (Path(__file__).with_name("_unresolved.txt")).write_text(
        "\n".join(f"{count}\t{name}\t{examples[name][:1]}" for name, count in unresolved.most_common()),
        encoding="utf-8",
    )
    print("unresolved names", len(unresolved), "rows", sum(unresolved.values()))
    for name, count in unresolved.most_common(40):
        print(f"{count}\t{name}")
        for example in examples[name]:
            print("   ", example)
    print("updates", len(updates))
    if not args.apply:
        print("dry run")
        return
    if stats["class_unresolved"]:
        raise SystemExit("Unresolved classifications remain; nothing was written")
    destination = REF.with_suffix(".replaced.xlsx")
    if destination.exists():
        destination.unlink()
    # Whole-register borrowed costs use the green money style.
    with zipfile.ZipFile(REF) as original, zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as staged:
        for entry in original.infolist():
            data = original.read(entry.filename)
            if entry.filename == "xl/styles.xml" and b'fillId="5"' in data and b'<cellXfs count="12">' not in data:
                data = data.replace(b'<cellXfs count="11">', b'<cellXfs count="12">', 1)
                extra = b'<xf numFmtId="164" fontId="0" fillId="5" borderId="0" xfId="0" applyNumberFormat="1" applyFill="1"/>'
                data = data.replace(b"</cellXfs>", extra + b"</cellXfs>", 1)
            staged.writestr(entry, data)
    result = apply_updates(destination, destination.with_suffix(".patched.xlsx"), updates)
    destination.unlink()
    result_path = Path(result["destination"])
    result_path.replace(REF)
    print("wrote", REF, result)


if __name__ == "__main__":
    main()
