"""Merge shared UgIFT asset registers into one workbook.

Sources are the shared workbooks under raw-data-grouped (team, district and
multi-team files), not facility-by-facility copies. The column layout follows
new-templates-to-follow. A source line that states a quantity becomes that
many rows, one physical item each.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path

import xlrd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
GROUPED = ROOT / "raw-data-grouped"
OUTPUT = ROOT / "outputs" / "asset-register-2026-09-23" / "UgIFT Shared Asset Register.xlsx"

HEADERS = [
    "Equipment/Item",
    "Department",
    "Asset Number",
    "Item Description",
    "Life in Months",
    "Tag Number (engrave no.)",
    "Date Of Purchase",
    "Date Placed In Service",
    "Recoverable cost",
    "Cost",
    "Acc Dep Cost",
    "Net Book Value",
    "Ytd Deprn",
    "Equipment status",
    "Remarks",
    "Local Government",
    "Facility",
    "Facility type",
    "Unit",
    "Source file",
    "Source location",
]

MAX_QUANTITY = 500
SKIP_DIR_NAMES = {
    "new-templates-to-follow",
    "samples",
    "assets-supplied-by-ugift",
    "pdf-to-excel",
    "registers-by-facility",
    "updated-asset-registers",
}
WORD_COUNTS = {
    "a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
}
COUNT_WORD = r"(?:\d{1,4}|one|two|three|four|five|six|seven|eight|nine|ten|a|an)"


@dataclass
class Asset:
    item: str = ""
    department: str = ""
    asset_number: str = ""
    description: str = ""
    life: object = None
    tag: str = ""
    purchase: object = None
    service: object = None
    recoverable: object = None
    cost: object = None
    acc_dep: object = None
    nbv: object = None
    ytd: object = None
    status: str = ""
    remarks: str = ""
    lg: str = ""
    facility: str = ""
    facility_type: str = ""
    explicit_qty: int | None = None
    source_file: str = ""
    source_location: str = ""
    extras: dict = field(default_factory=dict)

    def signal(self) -> bool:
        return any([
            self.item, self.description, self.tag, self.status, self.remarks,
            self.cost not in (None, ""), self.asset_number,
        ])


def clean(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    text = str(value).replace("\xa0", " ").replace("\r", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()


def norm(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).casefold()).strip()


def as_count(token: str) -> int | None:
    token = token.casefold()
    if token.isdigit():
        return int(token)
    return WORD_COUNTS.get(token)


def excel_date(value: object) -> object:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, (int, float)) and 20_000 <= float(value) <= 60_000:
        try:
            return xlrd.xldate_as_datetime(float(value), 0).date()
        except Exception:
            return value
    return value


def number_or_text(value: object) -> object:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value
    text = clean(value)
    if not text:
        return None
    bare = text.replace(",", "")
    if re.fullmatch(r"-?\d+", bare):
        return int(bare)
    if re.fullmatch(r"-?\d+\.\d+", bare):
        number = float(bare)
        return int(number) if number.is_integer() else number
    return text


def family_key(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"\s*[\(\[]\d+[\)\]]\s*$", "", stem)
    stem = re.sub(r"\s*-\s*copy\s*$", "", stem, flags=re.I)
    return re.sub(r"\s+", " ", stem).strip().casefold()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def default_lg(path: Path) -> str:
    parts = path.parts
    if "_district-documents" in parts:
        index = parts.index("_district-documents")
        if index:
            return parts[index - 1].replace("-", " ")
    return ""


def excluded_programme_file(path: Path) -> bool:
    """Leave out programme-documents, but keep the data-management chat."""
    parts = path.parts
    if "programme-documents" not in parts:
        return False
    index = parts.index("programme-documents")
    remainder = parts[index + 1:]
    return not (remainder and remainder[0] == "data-management-chat")


def candidate_files() -> list[Path]:
    found: list[Path] = []
    for path in GROUPED.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".xls", ".xlsx"}:
            continue
        if path.name.startswith("~$"):
            continue
        if excluded_programme_file(path):
            continue
        parts = set(path.parts)
        if parts & SKIP_DIR_NAMES:
            continue
        if not ({"_team-documents", "_district-documents", "_multi-team"} & parts):
            continue
        found.append(path)
    grouped: dict[str, list[Path]] = defaultdict(list)
    for path in found:
        grouped[family_key(path)].append(path)
    chosen: list[Path] = []
    for paths in grouped.values():
        paths.sort(key=lambda item: (-item.stat().st_size, len(str(item)), str(item)))
        chosen.append(paths[0])
    seen: set[str] = set()
    unique: list[Path] = []
    for path in sorted(chosen, key=lambda item: str(item).casefold()):
        digest = file_hash(path)
        if digest in seen:
            continue
        seen.add(digest)
        unique.append(path)
    return unique


def sheet_rows(path: Path) -> list[tuple[str, list[list[object]]]]:
    if path.suffix.lower() == ".xls":
        book = xlrd.open_workbook(path, on_demand=True)
        loaded = []
        try:
            for name in book.sheet_names():
                sheet = book.sheet_by_name(name)
                rows = []
                for row_index in range(sheet.nrows):
                    values = []
                    for col in range(sheet.ncols):
                        cell = sheet.cell(row_index, col)
                        if cell.ctype == xlrd.XL_CELL_DATE:
                            try:
                                values.append(xlrd.xldate_as_datetime(cell.value, book.datemode))
                            except Exception:
                                values.append(cell.value)
                        elif cell.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                            values.append(None)
                        elif cell.ctype == xlrd.XL_CELL_NUMBER and float(cell.value).is_integer():
                            values.append(int(cell.value))
                        else:
                            values.append(cell.value)
                    rows.append(values)
                loaded.append((name, rows))
        finally:
            book.release_resources()
        return loaded
    workbook = load_workbook(path, read_only=True, data_only=True)
    loaded = []
    try:
        for name in workbook.sheetnames:
            sheet = workbook[name]
            loaded.append((name, [list(row) for row in sheet.iter_rows(values_only=True)]))
    finally:
        workbook.close()
    return loaded


def classify_header(row: list[object]) -> dict[str, int] | None:
    texts = [norm(value) for value in row]
    if not any(texts):
        return None
    has_equipment = any(text in {"equipment item", "equipment"} or text.startswith("equipment item") for text in texts)
    mapping: dict[str, int] = {}
    for index, text in enumerate(texts):
        if not text:
            continue
        field_name = None
        if "status" in text or text == "condition":
            field_name = "status"
        elif "remark" in text:
            field_name = "remarks"
        elif "tag" in text or "engrave" in text:
            field_name = "tag"
        elif "life" in text:
            field_name = "life"
        elif "purchase" in text or "date purchased" in text or text.startswith("date of pur"):
            field_name = "purchase"
        elif "placed" in text:
            field_name = "service"
        elif "recoverable" in text:
            field_name = "recoverable"
        elif "acc dep" in text or "accumulated" in text:
            field_name = "acc_dep"
        elif "net book" in text:
            field_name = "nbv"
        elif "ytd" in text or "deprn" in text or "depreciation" in text:
            field_name = "ytd"
        elif "asset number" in text:
            field_name = "asset_number"
        elif "description" in text:
            field_name = "description"
        elif text in {"equipment item", "equipment"} or text.startswith("equipment item"):
            field_name = "item"
        elif text == "item":
            field_name = "description" if has_equipment else "item"
        elif "department" in text:
            field_name = "department"
        elif text in {"qty", "quantity"} or text.startswith("quantity"):
            field_name = "explicit_qty"
        elif text in {"cost", "initial cost", "cost ugx"} or text.startswith("cost"):
            field_name = "cost"
        elif "local gov" in text or text in {"district", "local government", "local govt"}:
            field_name = "lg"
        elif any(token in text for token in ("health centre", "health center", "hospital", "school", "location", "facility")):
            field_name = "facility"
        if field_name and field_name not in mapping:
            mapping[field_name] = index
    if "item" in mapping and len(mapping) >= 4:
        return mapping
    return None


def trailing_place_columns(rows: list[list[object]], mapping: dict[str, int]) -> dict[str, int]:
    """Map unlabeled columns that hold local government and facility names."""
    if "lg" in mapping and "facility" in mapping:
        return mapping
    used = set(mapping.values())
    scores: Counter[int] = Counter()
    for row in rows[:80]:
        for index, value in enumerate(row):
            text = clean(value)
            if index in used or len(text) < 3 or len(text) > 40:
                continue
            if re.search(r"\d{3,}", text):
                continue
            if re.fullmatch(r"[A-Za-z][A-Za-z .'/()-]{2,40}", text):
                scores[index] += 1
    ranked = [index for index, count in scores.most_common() if count >= 3]
    updated = dict(mapping)
    if "lg" not in updated and ranked:
        updated["lg"] = ranked.pop(0)
    if "facility" not in updated and ranked:
        updated["facility"] = ranked.pop(0)
    return updated


def parse_banner(text: str) -> tuple[str, str] | None:
    raw = clean(text)
    if len(raw) < 6:
        return None
    low = raw.casefold()
    asset_word = re.search(
        r"\b(machine|desk|chair|stool|autoclave|bowl|computer|monitor|cupboard|printer|table)\b",
        low,
    )
    if asset_word and "name of" not in low and "ugift asset" not in low:
        return None
    match = re.search(
        r"(?i)name of\s+lg\s*[:\-]?\s*(.+?)\s+name of\s+(?:the\s+)?(?:health\s+)?(?:facility|school)\s*[:\-]?\s*(.+)$",
        raw,
    )
    if match:
        return clean(match.group(1)), clean(match.group(2))
    match = re.search(r"(?i)name of\s+(?:health\s+)?(?:facility|school)\s*[:\-]?\s*(.+)$", raw)
    if match:
        return "", clean(match.group(1))
    match = re.search(r"(?i)name of\s+lg\s*[:\-]?\s*(.+)$", raw)
    if match:
        return clean(match.group(1)), ""
    match = re.search(r"(?i)^(.+?)\s+ugift\s+asset\s+verification.*?,\s*(.+)$", raw)
    if match:
        return clean(match.group(2)), clean(match.group(1))
    match = re.search(r"(?i)^(.+?)\s+ugift\s+asset\s+verification\s+tool\s*kit\s+(.+)$", raw)
    if match:
        return clean(match.group(2)), clean(match.group(1))
    if "," in raw and re.search(r"(?i)hc\s*(?:ii+|iv)?|health|school|\bsss\b|seed", raw):
        parts = [clean(part) for part in raw.split(",") if clean(part)]
        if len(parts) >= 2:
            return parts[-1], parts[0]
    match = re.search(
        r"(?i)^(.+?\b(?:HC\s*III|HCIII|HEALTH\s+CENT(?:RE|ER).*|SEED(?:\s+SECONDARY)?\s+SCHOOL|SSS))\s+(.+\bDISTRICT)\s*$",
        raw,
    )
    if match:
        return clean(match.group(2)), clean(match.group(1))
    if re.fullmatch(
        r"(?i)[A-Z0-9][A-Z0-9 .'/()-]{2,80}(?:SEED(?:\s+SECONDARY)?\s+SCHOOL|HEALTH\s+CENT(?:RE|ER)(?:\s+[IVX0-9]+)?|HC\s*III|HCIII|SSS)",
        raw,
    ):
        return "", raw
    return None


def first_text(row: list[object]) -> str:
    for value in row:
        text = clean(value)
        if text:
            return text
    return ""


def cell(row: list[object], mapping: dict[str, int], name: str) -> object:
    index = mapping.get(name)
    if index is None or index >= len(row):
        return None
    return row[index]


def looks_like_subheader(asset: Asset) -> bool:
    return norm(asset.description) == "description" and not any([
        asset.item, asset.tag, asset.status, asset.remarks, asset.cost, asset.asset_number,
    ])


def looks_like_label(asset: Asset) -> bool:
    if asset.tag or asset.status or asset.cost not in (None, "") or asset.asset_number:
        return False
    text = asset.item or asset.description
    return bool(text) and parse_banner(text) is not None and not asset.department


def facility_type_for(facility: str, department: str, sheet: str, filename: str) -> str:
    nearby = f"{facility} {department}"
    if re.search(r"health|hospital|\bhc\b|hciii|hc\s*iii|hc\s*ii", nearby, re.I):
        return "Health centre"
    if re.search(r"school|education|\bsss\b|seed", nearby, re.I):
        return "Seed school"
    broader = f"{sheet} {filename}"
    if re.search(r"health|hospital", broader, re.I):
        return "Health centre"
    if re.search(r"school|education", broader, re.I):
        return "Seed school"
    return ""


def join_text(left: str, right: str, divider: str = " ") -> str:
    left, right = clean(left), clean(right)
    if not right or right.casefold() in left.casefold():
        return left
    if not left:
        return right
    if left.endswith(("/", "-")):
        return f"{left}{right}"
    return f"{left}{divider}{right}"


def merge_continuation(previous: Asset, current: Asset) -> None:
    previous.department = join_text(previous.department, current.department, "; ")
    previous.description = join_text(previous.description, current.description)
    previous.tag = join_text(previous.tag, current.tag)
    previous.status = join_text(previous.status, current.status)
    previous.remarks = join_text(previous.remarks, current.remarks)
    for name in ("life", "purchase", "service", "recoverable", "cost", "acc_dep", "nbv", "ytd", "asset_number"):
        if getattr(previous, name) in (None, "") and getattr(current, name) not in (None, ""):
            setattr(previous, name, getattr(current, name))
    if not previous.lg and current.lg:
        previous.lg = current.lg
    if not previous.facility and current.facility:
        previous.facility = current.facility


def take_asset(row: list[object], mapping: dict[str, int], source: str, location: str) -> Asset:
    quantity = number_or_text(cell(row, mapping, "explicit_qty"))
    explicit = quantity if isinstance(quantity, int) and 0 < quantity <= MAX_QUANTITY else None
    asset = Asset(
        item=clean(cell(row, mapping, "item")),
        department=clean(cell(row, mapping, "department")),
        asset_number=clean(cell(row, mapping, "asset_number")),
        description=clean(cell(row, mapping, "description")),
        life=number_or_text(cell(row, mapping, "life")),
        tag=clean(cell(row, mapping, "tag")),
        purchase=excel_date(cell(row, mapping, "purchase")),
        service=excel_date(cell(row, mapping, "service")),
        recoverable=number_or_text(cell(row, mapping, "recoverable")),
        cost=number_or_text(cell(row, mapping, "cost")),
        acc_dep=number_or_text(cell(row, mapping, "acc_dep")),
        nbv=number_or_text(cell(row, mapping, "nbv")),
        ytd=number_or_text(cell(row, mapping, "ytd")),
        status=clean(cell(row, mapping, "status")),
        remarks=clean(cell(row, mapping, "remarks")),
        lg=clean(cell(row, mapping, "lg")),
        facility=clean(cell(row, mapping, "facility")),
        explicit_qty=explicit,
        source_file=source,
        source_location=location,
    )
    if norm(asset.item) in {"equipment item", "equipment", "description"}:
        asset.item = ""
    return asset


def sheet_is_duplicate_draft(name: str, mapping: dict[str, int], workbook_has_places: bool) -> bool:
    """Skip OCR fragments and single-facility drafts when a consolidated sheet exists."""
    if not workbook_has_places:
        return False
    if re.fullmatch(r"table\s*[1-3]", name.strip(), flags=re.I):
        return True
    unnamed = re.fullmatch(r"sheet\s*[1-3]", name.strip(), flags=re.I)
    return bool(unnamed and "lg" not in mapping and "facility" not in mapping)


def parse_template_sheet(
    sheet_name: str, rows: list[list[object]], source: str, filename: str, fallback_lg: str,
) -> list[Asset]:
    mapped_rows: list[tuple[int, dict[str, int]]] = []
    for index, row in enumerate(rows):
        mapping = classify_header(row)
        if mapping:
            mapped_rows.append((index, trailing_place_columns(rows[index + 1:index + 40], mapping)))
    if not mapped_rows:
        return []
    assets: list[Asset] = []
    carry_lg = fallback_lg
    carry_facility = ""
    mapping = None
    header_indexes = {index for index, _ in mapped_rows}
    active = {index: item for index, item in mapped_rows}
    for row_number, row in enumerate(rows, 1):
        if (row_number - 1) in header_indexes:
            mapping = active[row_number - 1]
            continue
        if mapping is None:
            banner = parse_banner(first_text(row))
            if banner:
                carry_lg = banner[0] or carry_lg
                carry_facility = banner[1] or carry_facility
            continue
        if not any(clean(value) for value in row):
            continue
        asset = take_asset(row, mapping, source, f"{sheet_name} row {row_number}")
        if looks_like_subheader(asset):
            continue
        banner_text = asset.item or first_text(row)
        if looks_like_label(asset):
            banner = parse_banner(banner_text)
            if banner:
                carry_lg = banner[0] or carry_lg
                carry_facility = banner[1] or carry_facility
            continue
        if asset.lg:
            carry_lg = asset.lg
        else:
            asset.lg = carry_lg
        if asset.facility:
            carry_facility = asset.facility
        else:
            asset.facility = carry_facility
        if not asset.item and assets and (asset.description or asset.tag or asset.status or asset.remarks):
            merge_continuation(assets[-1], asset)
            continue
        if not asset.item:
            continue
        asset.facility_type = facility_type_for(asset.facility, asset.department, sheet_name, filename)
        assets.append(asset)
    return assets


def parse_qty_register(sheet_name: str, rows: list[list[object]], source: str, fallback_lg: str) -> list[Asset]:
    header_at = None
    mapping: dict[str, int] = {}
    for index, row in enumerate(rows[:15]):
        texts = [norm(value) for value in row]
        if "qty" in texts and "description" in texts and "condition" in texts:
            header_at = index
            for col, text in enumerate(texts):
                if text == "description":
                    mapping["item"] = col
                elif text in {"qty", "quantity"}:
                    mapping["explicit_qty"] = col
                elif "cost" in text:
                    mapping["cost"] = col
                elif "purchase" in text or text.startswith("date"):
                    mapping["purchase"] = col
                elif text == "user":
                    mapping["remarks"] = col
                elif text == "location":
                    mapping["facility"] = col
                elif text == "condition":
                    mapping["status"] = col
                elif "asset number" in text or text == "no":
                    mapping["asset_number"] = col
            break
    if header_at is None:
        return []
    assets: list[Asset] = []
    facility = ""
    for row_number, row in enumerate(rows[header_at + 1:], header_at + 2):
        asset = take_asset(row, mapping, source, f"{sheet_name} row {row_number}")
        if asset.remarks and not re.search(r"\d", asset.remarks):
            asset.remarks = f"User: {asset.remarks}"
        filled = [clean(value) for value in row if clean(value)]
        if len(filled) == 1 and parse_banner(filled[0]):
            facility = filled[0]
            continue
        if not asset.item:
            continue
        asset.facility = asset.facility or facility
        asset.lg = asset.lg or fallback_lg
        asset.department = "Education"
        asset.facility_type = "Seed school"
        assets.append(asset)
    return assets


def parse_pallisa(sheet_name: str, rows: list[list[object]], source: str) -> list[Asset]:
    header_at = None
    texts: list[str] = []
    for index, row in enumerate(rows[:12]):
        texts = [norm(value) for value in row]
        if any("asset description" in text or text == "description" for text in texts) and "condition" in texts:
            header_at = index
            break
    if header_at is None:
        return []
    columns = {text: index for index, text in enumerate(texts) if text}
    def col(*names: str) -> int | None:
        for name in names:
            if name in columns:
                return columns[name]
        for text, index in columns.items():
            if any(name in text for name in names):
                return index
        return None
    item_col = col("asset description", "description")
    tag_col = col("tag number", "tag")
    dept_col = col("section", "department-location", "location- department", "location-department")
    facility_col = col("location")
    cost_col = col("cost ugx", "cost")
    date_col = col("date of purchase", "date of acquisition")
    status_col = col("condition")
    user_col = col("user name")
    title_col = col("user title")
    assets: list[Asset] = []
    for row_number, row in enumerate(rows[header_at + 1:], header_at + 2):
        def value(index: int | None) -> object:
            if index is None or index >= len(row):
                return None
            return row[index]
        item = clean(value(item_col))
        if not item or norm(item) in {"description", "asset description"}:
            continue
        facility = clean(value(facility_col))
        department = clean(value(dept_col))
        if facility and not re.search(r"school|health|hc|hospital", facility, re.I) and re.search(r"school|health|hc", department, re.I):
            facility, department = department, facility
        user = clean(value(user_col))
        title = clean(value(title_col))
        remarks = ", ".join(part for part in (user, title) if part)
        asset = Asset(
            item=item,
            department=department,
            tag=clean(value(tag_col)),
            purchase=excel_date(value(date_col)),
            cost=number_or_text(value(cost_col)),
            status=clean(value(status_col)),
            remarks=remarks,
            lg="Pallisa",
            facility=facility,
            facility_type=facility_type_for(facility, department, sheet_name, "pallisa"),
            source_file=source,
            source_location=f"{sheet_name} row {row_number}",
        )
        if not asset.facility_type:
            asset.facility_type = "Seed school"
        assets.append(asset)
    return assets


def read_workbook(path: Path) -> list[Asset]:
    relative = path.relative_to(GROUPED).as_posix()
    fallback = default_lg(path)
    assets: list[Asset] = []
    sheets = sheet_rows(path)
    if "REGISTAR" in path.name.upper() or "REGISTER UGIFT" in path.name.upper() and "PALLISA" in path.name.upper():
        for name, rows in sheets:
            assets.extend(parse_pallisa(name, rows, relative))
        if assets:
            return assets
    drafted = False
    template_maps = []
    for name, rows in sheets:
        for row in rows[:20]:
            mapping = classify_header(row)
            if mapping:
                template_maps.append(mapping)
                break
    workbook_has_places = any("lg" in mapping or "facility" in mapping for mapping in template_maps)
    for name, rows in sheets:
        mapping = next((classify_header(row) for row in rows[:20] if classify_header(row)), None)
        if mapping and sheet_is_duplicate_draft(name, mapping, workbook_has_places):
            drafted = True
            continue
        if mapping:
            assets.extend(parse_template_sheet(name, rows, relative, path.name, fallback))
            continue
        qty_rows = parse_qty_register(name, rows, relative, fallback)
        if qty_rows:
            assets.extend(qty_rows)
    if not assets and "PALLISA" in path.name.upper():
        for name, rows in sheets:
            assets.extend(parse_pallisa(name, rows, relative))
    if drafted and not assets:
        return []
    return assets


def furniture_quantity(item: str) -> tuple[str, int] | None:
    match = re.fullmatch(
        r"(?i)(desks?|chairs?|stools?|tables?|shelves|benches|beds?|cupboards?)\s+(\d{2,4})",
        clean(item),
    )
    if not match:
        return None
    count = int(match.group(2))
    if 1 < count <= MAX_QUANTITY:
        return match.group(1), count
    return None


def parenthetical_quantity(item: str) -> tuple[str, int] | None:
    match = re.fullmatch(r"(.+?)\s*[\(\[]\s*(\d{1,4})\s*[\)\]]", clean(item))
    if not match:
        return None
    count = int(match.group(2))
    if 1 < count <= MAX_QUANTITY:
        return clean(match.group(1)), count
    return None


def condition_groups(status: str, remarks: str) -> list[tuple[int, str | None]] | None:
    text = clean(f"{status}. {remarks}")
    if not text:
        return None
    match = re.search(r"(?i)(\d{1,4})\s+verified as good\s+then\s+(\d{1,4})\s+damaged", text)
    if match:
        return [(int(match.group(1)), "Verified as good"), (int(match.group(2)), "Damaged")]
    match = re.search(r"(?i)(\d{1,4})\s+verified and in good use\s*\.?\s*(\d{1,4})\s+broken", text)
    if match:
        return [(int(match.group(1)), "Verified and in good use"), (int(match.group(2)), "Broken")]
    match = re.search(r"(?i)all\s+(\d{1,4})\s+verified as good.*?(\d{1,4})\s+broken", text)
    if match:
        return [(int(match.group(1)), "Verified as good"), (int(match.group(2)), "Broken")]
    functional = re.search(rf"(?i)\b({COUNT_WORD})\s+function(?:al|ing)\b", text)
    store = re.search(rf"(?i)\b({COUNT_WORD})\s+(?:other\s+)?in\s+(?:the\s+)?store\b", text)
    if functional or store:
        groups = []
        if functional and (count := as_count(functional.group(1))):
            groups.append((count, "Functional"))
        if store and (count := as_count(store.group(1))):
            groups.append((count, "In the store"))
        if sum(count for count, _ in groups) > 1:
            return [(count, label) for count, label in groups if 0 < count <= MAX_QUANTITY]
    verified = [int(item) for item in re.findall(r"(?i)(?<!not )(\d{1,4})\s+verified\b", text)]
    received = [int(item) for item in re.findall(r"(?i)(\d{1,4})\s+(?:were\s+|was\s+)?(?:received|recieved|supplied)\b", text)]
    received += [int(item) for item in re.findall(r"(?i)\b(?:received|recieved|supplied|counted)\s+(\d{1,4})\b", text)]
    received += [int(item) for item in re.findall(r"(?i)\ball the\s+(\d{1,4})\b", text)]
    verified = [item for item in verified if 0 < item <= MAX_QUANTITY]
    received = [item for item in received if 0 < item <= MAX_QUANTITY]
    if verified and received:
        return [(verified[0], None)]
    if len(verified) == 1:
        return [(verified[0], None)]
    if len(set(received)) == 1 and received:
        return [(received[0], None)]
    match = re.search(
        r"(?i)\b(\d{1,4})\s+(?:desks?|chairs?|stools?|tables?|shelves|benches|items?|units?)\b(?:\s+\w+){0,3}\s+(?:supplied|received|verified)",
        text,
    )
    if match and 1 < int(match.group(1)) <= MAX_QUANTITY:
        return [(int(match.group(1)), None)]
    return None


def decide_groups(asset: Asset, alone: bool) -> tuple[str, list[tuple[int, str | None]]]:
    if asset.explicit_qty and asset.explicit_qty > 1:
        return asset.item, [(asset.explicit_qty, None)]
    parenthetical = parenthetical_quantity(asset.item)
    if parenthetical:
        name, count = parenthetical
        return name, [(count, None)]
    if alone:
        furniture = furniture_quantity(asset.item)
        if furniture:
            name, count = furniture
            return name, [(count, None)]
        groups = condition_groups(asset.status, asset.remarks)
        if groups and sum(count for count, _ in groups) > 1:
            return asset.item, groups
    return asset.item, [(1, None)]


def explode(assets: list[Asset]) -> list[Asset]:
    presence = Counter((norm(asset.lg), norm(asset.facility), norm(asset.item)) for asset in assets)
    exploded: list[Asset] = []
    for asset in assets:
        alone = presence[(norm(asset.lg), norm(asset.facility), norm(asset.item))] == 1
        item, groups = decide_groups(asset, alone)
        total = sum(count for count, _ in groups)
        running = 0
        for count, status in groups:
            for _ in range(count):
                running += 1
                copy = Asset(**{key: getattr(asset, key) for key in (
                    "item", "department", "asset_number", "description", "life", "tag",
                    "purchase", "service", "recoverable", "cost", "acc_dep", "nbv", "ytd",
                    "status", "remarks", "lg", "facility", "facility_type", "explicit_qty",
                    "source_file", "source_location",
                )})
                copy.item = item
                if status:
                    copy.status = status
                copy.extras["unit"] = f"{running} of {total}" if total > 1 else ""
                exploded.append(copy)
    return exploded


def jaccard(left: Counter[str], right: Counter[str]) -> float:
    keys_left, keys_right = set(left), set(right)
    union = keys_left | keys_right
    if not union:
        return 0.0
    return len(keys_left & keys_right) / len(union)


def drop_overlapping_facilities(assets: list[Asset]) -> tuple[list[Asset], list[str]]:
    grouped: dict[tuple[str, str], dict[str, list[Asset]]] = defaultdict(lambda: defaultdict(list))
    for asset in assets:
        if not norm(asset.facility):
            continue
        grouped[(norm(asset.lg), norm(asset.facility))][asset.source_file].append(asset)
    drop: set[int] = set()
    notes: list[str] = []
    for sources in grouped.values():
        if len(sources) < 2:
            continue
        names = list(sources)
        counters = {name: Counter(norm(asset.item) for asset in rows) for name, rows in sources.items()}
        dominated: set[str] = set()
        for left in names:
            for right in names:
                if left == right or left in dominated or right in dominated:
                    continue
                if min(len(sources[left]), len(sources[right])) < 5:
                    continue
                if jaccard(counters[left], counters[right]) < 0.75:
                    continue
                if len(sources[left]) == len(sources[right]):
                    loser, winner = sorted((left, right))[1], sorted((left, right))[0]
                elif len(sources[left]) < len(sources[right]):
                    loser, winner = left, right
                else:
                    loser, winner = right, left
                dominated.add(loser)
                sample = sources[loser][0]
                notes.append(
                    f"{sample.facility} ({sample.lg}): kept {winner}; left out {loser} "
                    f"({len(sources[loser])} rows overlapping {len(sources[winner])})."
                )
        for name in dominated:
            for asset in sources[name]:
                drop.add(id(asset))
    kept = [asset for asset in assets if id(asset) not in drop]
    return kept, notes


def check_examples() -> None:
    def groups(item="", status="", remarks="", qty=None, alone=True):
        asset = Asset(item=item, status=status, remarks=remarks, explicit_qty=qty)
        return decide_groups(asset, alone)

    assert groups(status="2 functional and one in the store")[1] == [(2, "Functional"), (1, "In the store")]
    assert groups(remarks="116 verified as good then 4 damaged")[1] == [(116, "Verified as good"), (4, "Damaged")]
    assert groups(remarks="Received 2 and all still functioning.")[1] == [(2, None)]
    assert groups(remarks="39 desks were supplied")[1] == [(39, None)]
    assert groups(item="B.P. Machine, Digital(2)", alone=False) == ("B.P. Machine, Digital", [(2, None)])
    assert groups(item="Desks 125") == ("Desks", [(125, None)])
    assert groups(item="Desks 107", alone=False)[1] == [(1, None)]
    assert groups(remarks="40 verified and in good use.45 broken")[1][0][0] == 40
    assert groups(remarks="Counted 21 and verified them")[1] == [(21, None)]
    assert groups(status="Not received")[1] == [(1, None)]
    assert groups(remarks="120 receive , 118 verified and in use")[1] == [(118, None)]
    assert groups(item="CPU", status="working well", alone=False)[1] == [(1, None)]
    banner = parse_banner("NAME OF LG: DOKOLO DISTRICT LOCAL GOVERNMENT NAME OF HEALTH FACILITY: ABALANG HEALTH CENTER III")
    assert banner and "ABALANG" in banner[1].upper()
    assert parse_banner("BITSYA HCIII, BUHWEJU DC")[0].upper().startswith("BUHWEJU")
    assert parse_banner("School Desks") is None


def display(value: object) -> object:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return value


def write_workbook(assets: list[Asset], sources: list[str], notes: list[str]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Asset Register"
    header_font = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
    header_fill = PatternFill("solid", fgColor="1F4E79")
    sheet.append(HEADERS)
    for cell_item in sheet[1]:
        cell_item.font = header_font
        cell_item.fill = header_fill
        cell_item.alignment = Alignment(wrap_text=True, vertical="center")
    for asset in assets:
        sheet.append([
            asset.item, asset.department, asset.asset_number, asset.description, display(asset.life),
            asset.tag, display(asset.purchase), display(asset.service), asset.recoverable, asset.cost,
            asset.acc_dep, asset.nbv, asset.ytd, asset.status, asset.remarks,
            asset.lg, asset.facility, asset.facility_type, asset.extras.get("unit", ""),
            asset.source_file, asset.source_location,
        ])
    sheet.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{sheet.max_row}"
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{max(sheet.max_row, 2)}"
    widths = {
        1: 36, 2: 18, 3: 18, 4: 42, 5: 14, 6: 28, 7: 18, 8: 20, 9: 16, 10: 14,
        11: 14, 12: 16, 13: 14, 14: 28, 15: 42, 16: 28, 17: 36, 18: 16, 19: 12,
        20: 55, 21: 28,
    }
    for index, width in widths.items():
        sheet.column_dimensions[get_column_letter(index)].width = width
    sheet.row_dimensions[1].height = 30
    notes_sheet = workbook.create_sheet("Read Me")
    notes_sheet["A1"] = "UgIFT shared asset register"
    notes_sheet["A1"].font = Font(bold=True, size=14, color="1F4E79")
    lines = [
        "One workbook. Health centres and seed schools are rows in Asset Register, not separate files.",
        "Columns follow the health-centre and seed-school templates in new-templates-to-follow. Facility holds the template Health Centre / Location value.",
        "Each physical item is one row. Where a source line stated a quantity, that line was repeated once per item and Unit shows the sequence.",
        "A quantity was taken from a quantity column, a number in brackets on the item name, a single furniture line such as Desks 125, or a count written in the status or remarks. Lines that were already one row per item were left as one row.",
        "Cost is the figure written on the source line, copied onto each item from that line.",
        "Files under programme-documents were left out. The data-management chat in that folder is the exception.",
        "Draft sheets were left out where the same workbook already had a consolidated sheet with local government and facility columns.",
        "Where the same facility was filled in more than one shared workbook and the item lists matched, the fuller list was kept.",
        "",
        "Sources:",
        *sources,
        "",
        "Facilities kept from one shared workbook where another copy overlapped:",
        *(notes or ["None."]),
    ]
    for index, line in enumerate(lines, 3):
        notes_sheet.cell(index, 1, line)
    notes_sheet.column_dimensions["A"].width = 140
    workbook.save(OUTPUT)


def main() -> None:
    check_examples()
    files = candidate_files()
    collected: list[Asset] = []
    used: list[str] = []
    skipped: list[str] = []
    for path in files:
        relative = path.relative_to(GROUPED).as_posix()
        try:
            assets = read_workbook(path)
        except Exception as error:
            skipped.append(f"{relative} ({error})")
            continue
        if not assets:
            skipped.append(relative)
            continue
        collected.extend(assets)
        used.append(f"{relative} ({len(assets):,} source rows)")
        print(f"{len(assets):6,}  {relative}", flush=True)
    collected, overlap_notes = drop_overlapping_facilities(collected)
    exploded = explode(collected)
    multi = sum(1 for asset in exploded if asset.extras.get("unit"))
    print(f"source rows kept {len(collected):,}; output rows {len(exploded):,}; rows from a quantity split {multi:,}")
    largest = Counter(
        (asset.source_location, asset.item, asset.extras.get("unit", "").split(" of ")[-1])
        for asset in exploded if asset.extras.get("unit")
    )
    print("largest splits:")
    seen = set()
    for (location, item, total), _count in largest.most_common(12):
        key = (location, item, total)
        if key in seen:
            continue
        seen.add(key)
        print(f"  {total:>4}  {item}  {location}")
    write_workbook(exploded, used, overlap_notes)
    print(f"wrote {OUTPUT}")
    print(f"skipped {len(skipped)} shared workbooks with no template register")


if __name__ == "__main__":
    main()
