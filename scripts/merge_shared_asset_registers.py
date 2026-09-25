"""Merge shared UgIFT asset registers into one workbook.

Sources are the shared workbooks under raw-data-grouped (team, district and
multi-team files), not facility-by-facility copies. The column layout follows
new-templates-to-follow. A source line that states a quantity becomes that
many rows, one physical item each.
"""

from __future__ import annotations

import hashlib
import re
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path

import xlrd
from docx import Document
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
GROUPED = ROOT / "raw-data-grouped"
OUTPUT = ROOT / "outputs" / "asset-register-2026-09-23" / "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx"

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
BULK_ITEM = re.compile(
    r"(?i)\b(desks?|chairs?|stools?|tables?|shelves|benches|beds?|cupboards?|couches?|cylinders?)\b"
)
MODEL_TAIL = re.compile(
    r"(?i)^(laserjet|laptop|printer|elitebook|probook|latitude|inspiron|pavilion|"
    r"thinkpad|monitor|cpu|iphone|samsung|nokia|tecno|inch|gen|core|mhz|gb)$"
)
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


def path_context(path: Path) -> tuple[str, str]:
    """Local government and facility implied by the grouped folder path."""
    parts = path.relative_to(GROUPED).parts
    if "_district-documents" in parts:
        index = parts.index("_district-documents")
        if index:
            return parts[index - 1].replace("-", " "), ""
    if parts and re.fullmatch(r"team-\d+", parts[0]) and len(parts) >= 3:
        if parts[1] not in {"_team-documents", "_district-documents"}:
            facility = ""
            if parts[2] not in {"_district-documents", "_team-documents"}:
                facility = parts[2].replace("-", " ")
            return parts[1].replace("-", " "), facility
    return "", ""


def default_lg(path: Path) -> str:
    return path_context(path)[0]


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
        if not path.is_file() or path.suffix.lower() not in {".xls", ".xlsx", ".docx"}:
            continue
        if path.name.startswith("~$"):
            continue
        if excluded_programme_file(path):
            continue
        found.append(path)
    grouped: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for path in found:
        grouped[(str(path.parent).casefold(), family_key(path))].append(path)
    chosen: list[Path] = []
    for paths in grouped.values():
        paths.sort(key=lambda item: (
            {".xlsx": 0, ".xls": 1, ".docx": 2}.get(item.suffix.lower(), 3),
            -item.stat().st_size, len(str(item)), str(item),
        ))
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


def docx_has_asset_table(path: Path) -> bool:
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml")
    except (OSError, zipfile.BadZipFile, KeyError):
        return False
    return b"equipment" in xml.lower() and (b"asset number" in xml.lower() or b"item description" in xml.lower())


def docx_tables(path: Path) -> list[tuple[str, list[list[object]]]]:
    document = Document(path)
    tables = []
    for index, table in enumerate(document.tables, 1):
        rows = [[clean(cell.text) for cell in row.cells] for row in table.rows]
        tables.append((f"Table {index}", rows))
    return tables


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


def context_from_line(text: str) -> tuple[str, str] | None:
    raw = clean(text)
    if not raw or len(raw) > 120 or raw.endswith(":"):
        return None
    if re.match(r"(?i)class\s+\d", raw) or re.match(r"(?i)cost cent", raw):
        return None
    banner = parse_banner(raw)
    if banner and (banner[0] or banner[1]):
        return banner
    if re.search(r"(?i)\b(district|municipal council|local government|city)\b", raw) and not re.search(
        r"(?i)health|school|hospital|blood bank", raw
    ):
        return raw, ""
    if re.search(r"(?i)health|seed|school|blood bank|hospital", raw):
        return "", raw
    return None


def flexible_mapping(row: list[object]) -> dict[str, int] | None:
    texts = [norm(value) for value in row]
    if not any(texts):
        return None
    roles: dict[str, int] = {}
    descriptions: list[int] = []
    for index, text in enumerate(texts):
        if not text or text in {"sn", "s n", "no", "item no", "pg no"}:
            continue
        if "imei" in text or "serial" in text or "engrave" in text or text.startswith("tag"):
            roles.setdefault("tag", index)
        elif "remark" in text or text.endswith("notes") or "notes" in text:
            roles.setdefault("remarks", index)
        elif "status" in text or text == "condition":
            roles.setdefault("status", index)
        elif "unit cost" in text:
            roles.setdefault("cost", index)
        elif ("cost" in text and "total" not in text and "center" not in text and "centre" not in text):
            roles.setdefault("cost", index)
        elif "qty" in text or "quantity" in text:
            roles.setdefault("explicit_qty", index)
        elif text in {"department", "section"} or text.startswith("department"):
            roles.setdefault("department", index)
        elif "asset category" in text and "sub" not in text:
            roles.setdefault("department", index)
        elif "physical location" in text or text in {"facility", "school", "schools", "location"}:
            roles.setdefault("facility", index)
        elif "location" in text and "department" in text:
            roles.setdefault("department", index)
        elif text in {"district", "local government"} or "local gov" in text:
            roles.setdefault("lg", index)
        elif any(token in text for token in ("date of purchase", "date purchased", "date of acquisition", "delivery date")) or text.startswith("date of pur"):
            roles.setdefault("purchase", index)
        elif "placed" in text or "issue date" in text:
            roles.setdefault("service", index)
        elif text in {"equipment", "equipment item", "equipment name"} or text.startswith("equipment /") or text.startswith("equipment item"):
            roles.setdefault("item", index)
        elif "description" in text or text in {"asset", "equipment asset"}:
            descriptions.append(index)
        elif "model" in text:
            roles.setdefault("description", index)
    if "item" not in roles and descriptions:
        roles["item"] = descriptions.pop(0)
    if descriptions and "description" not in roles:
        roles["description"] = descriptions[0]
    useful = {"tag", "status", "cost", "explicit_qty", "department", "facility"}
    if "item" in roles and len(useful & set(roles)) >= 1 and len(roles) >= 3:
        return roles
    device_sheet = any(token in text for text in texts for token in ("imei", "serial", "device", "sim card"))
    if "tag" in roles and device_sheet and ("facility" in roles or "lg" in roles or "imei" in " ".join(texts)):
        roles.setdefault("item", -1)
        return roles
    return None


def sheet_label(sheet_name: str, filename: str) -> str:
    blob = f"{sheet_name} {filename}".casefold()
    if "tela" in blob or "phone" in blob:
        return "Phone"
    if "tab" in blob:
        return "Tablet"
    if "inspection" in blob or "device" in blob:
        return "Inspection device"
    return ""


def looks_like_budget_codes(assets: list[Asset]) -> bool:
    if len(assets) < 8:
        return False
    codes = sum(1 for asset in assets if re.fullmatch(r"\d{5,8}", asset.item))
    return codes / len(assets) > 0.5


def parse_flexible_sheet(
    sheet_name: str, rows: list[list[object]], source: str, filename: str, fallback_lg: str,
) -> list[Asset]:
    header_at = None
    mapping: dict[str, int] = {}
    for index, row in enumerate(rows[:15]):
        found = flexible_mapping(row)
        if found:
            header_at = index
            mapping = found
            break
    if header_at is None:
        return []
    label = sheet_label(sheet_name, filename)
    carry_lg = fallback_lg
    carry_facility = ""
    for row in rows[:header_at]:
        label_text = norm(row[0]) if row else ""
        value = clean(row[1]) if len(row) > 1 else ""
        if value and label_text in {"school name", "name of school", "facility", "health facility", "name of health facility"}:
            carry_facility = value
            continue
        if value and label_text in {"district", "name of lg", "local government"}:
            carry_lg = value
            continue
        context = context_from_line(first_text(row))
        if not context:
            continue
        carry_lg = context[0] or carry_lg
        carry_facility = context[1] or carry_facility
    assets: list[Asset] = []
    item_index = mapping.get("item", -1)
    for row_number, row in enumerate(rows[header_at + 1:], header_at + 2):
        if not any(clean(value) for value in row):
            continue
        context = context_from_line(first_text(row))
        probe = take_asset(row, {key: value for key, value in mapping.items() if value >= 0}, source, "")
        if context and not any([probe.tag, probe.status, probe.cost, probe.explicit_qty, probe.description]):
            carry_lg = context[0] or carry_lg
            carry_facility = context[1] or carry_facility
            continue
        asset = probe
        asset.source_location = f"{sheet_name} row {row_number}"
        if item_index < 0:
            asset.item = label
        if not asset.item or norm(asset.item) in {"description", "asset description", "equipment", "total"}:
            continue
        if asset.department and not asset.facility and re.search(r"school|health|hospital|blood bank|\bhc\b", asset.department, re.I):
            asset.facility = asset.department
            asset.department = ""
        asset.lg = asset.lg or carry_lg
        asset.facility = asset.facility or carry_facility
        asset.facility_type = facility_type_for(asset.facility, asset.department, sheet_name, filename)
        assets.append(asset)
    if looks_like_budget_codes(assets):
        return []
    if not any(asset.tag or asset.status or asset.cost not in (None, "") or asset.explicit_qty or asset.description for asset in assets):
        return []
    return assets


def read_workbook(path: Path) -> list[Asset]:
    relative = path.relative_to(GROUPED).as_posix()
    fallback_lg, fallback_facility = path_context(path)
    assets: list[Asset] = []
    if path.suffix.lower() == ".docx":
        if not docx_has_asset_table(path):
            return []
        sheets = docx_tables(path)
    else:
        sheets = sheet_rows(path)
    template_maps = []
    for _name, rows in sheets:
        for row in rows[:20]:
            mapping = classify_header(row)
            if mapping:
                template_maps.append(mapping)
                break
    workbook_has_places = any("lg" in mapping or "facility" in mapping for mapping in template_maps)
    for name, rows in sheets:
        mapping = next((classify_header(row) for row in rows[:20] if classify_header(row)), None)
        if mapping and sheet_is_duplicate_draft(name, mapping, workbook_has_places):
            continue
        parsed: list[Asset] = []
        if mapping:
            parsed = parse_template_sheet(name, rows, relative, path.name, fallback_lg)
        if not parsed:
            parsed = parse_qty_register(name, rows, relative, fallback_lg)
        if not parsed:
            parsed = parse_flexible_sheet(name, rows, relative, path.name, fallback_lg)
        assets.extend(parsed)
    for asset in assets:
        if not asset.lg:
            asset.lg = fallback_lg
        if not asset.facility:
            asset.facility = fallback_facility
        if not asset.facility_type:
            asset.facility_type = facility_type_for(asset.facility, asset.department, "", path.name)
    return assets


def bare_count(value: object) -> int | None:
    """A cell whose whole value is a count, not a year, serial or amount."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)) and float(value).is_integer():
        count = int(value)
    else:
        text = clean(value).replace(",", "")
        if not re.fullmatch(r"\d{1,4}", text):
            return None
        count = int(text)
    if count in range(1990, 2036) or not 1 < count <= MAX_QUANTITY:
        return None
    return count


def trailing_quantity(item: str) -> tuple[str, int] | None:
    """'Examination Couch 2' and 'Desks 125' state the count after the item name.

    A model suffix such as LaserJet 1320 or Laptop 840 is not a count.
    Larger counts are accepted only for bulk items such as desks and chairs.
    """
    match = re.fullmatch(r"(.+?)\s+(\d{1,4})", clean(item))
    if not match:
        return None
    count = int(match.group(2))
    name = clean(match.group(1)).rstrip(" ,.;")
    if not name or count in range(1990, 2036) or not 1 < count <= MAX_QUANTITY:
        return None
    last = name.split()[-1]
    if MODEL_TAIL.match(last):
        return None
    if count > 40 and not BULK_ITEM.search(name):
        return None
    return name, count


def phrase_count(text: object) -> tuple[int, str] | None:
    """'2 microscopes, white' states a count in front of the description."""
    raw = clean(text)
    match = re.match(
        r"(?i)^(\d{1,3})\s+(?!inch\b|lit(?:re|er)s?\b|mm\b|cm\b|kg\b|gb\b|mhz\b|w\b)(.+)$",
        raw,
    )
    if not match:
        return None
    count = int(match.group(1))
    if 1 < count <= 40:
        return count, clean(match.group(2))
    return None


def embedded_quantity(text: str) -> int | None:
    """A count written inside a description, such as 'qty 100' or '3 classrooms'."""
    raw = clean(text)
    if not raw or bare_count(raw):
        return None
    patterns = (
        rf"(?i)\b(?:qty|quantity|no\.?\s*of\s+(?:assets|items)|number\s+of\s+(?:assets|items))\s*[:\-]?\s*({COUNT_WORD})\b",
        rf"(?i)\b({COUNT_WORD})\s*(?:pcs|pieces|units|items|desks?|chairs?|benches|stools?|tables?|beds?|sets|labs?|classrooms?|blocks?)\b",
    )
    for pattern in patterns:
        match = re.search(pattern, raw)
        if match and (count := as_count(match.group(1))) and 1 < count <= MAX_QUANTITY:
            return count
    return None


def per_item_amount(value: object, total: int) -> object:
    """Split a line total across the rows created from that line."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or total <= 1:
        return value
    share = value / total
    if abs(share - round(share)) < 1e-6:
        return int(round(share))
    return round(share, 2)


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
    """Choose how many asset rows a source line represents.

    A stated quantity is taken from a quantity column, a number in brackets,
    a trailing count on the item name, or — when this is the only line for
    that item — a bare number in Asset Number, the description, or another
    text field. The same rules already expand quantities in the 22 September
    register: one physical item becomes one row.
    """
    if asset.explicit_qty and asset.explicit_qty > 1:
        return asset.item, [(asset.explicit_qty, None)]
    parenthetical = parenthetical_quantity(asset.item)
    if parenthetical:
        name, count = parenthetical
        return name, [(count, None)]
    if alone:
        trailing = trailing_quantity(asset.item)
        if trailing:
            name, count = trailing
            return name, [(count, None)]
        if blank_tag(asset.tag) and (count := bare_count(asset.asset_number)):
            return asset.item, [(count, None)]
        if blank_tag(asset.tag) and (found := phrase_count(asset.asset_number)):
            return asset.item, [(found[0], None)]
        if count := bare_count(asset.description):
            return asset.item, [(count, None)]
        if found := phrase_count(asset.description):
            return asset.item, [(found[0], None)]
        if count := embedded_quantity(asset.description):
            return asset.item, [(count, None)]
        if count := embedded_quantity(asset.asset_number):
            return asset.item, [(count, None)]
        furniture = furniture_quantity(asset.item)
        if furniture:
            name, count = furniture
            return name, [(count, None)]
        leading = re.fullmatch(r"([1-9]\d{0,2})\s+(.+)", asset.item)
        if leading and 1 < int(leading.group(1)) <= 100:
            return clean(leading.group(2)), [(int(leading.group(1)), None)]
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
                if total > 1:
                    if blank_tag(asset.tag) and bare_count(asset.asset_number) == total:
                        copy.asset_number = ""
                    elif blank_tag(asset.tag) and (found := phrase_count(asset.asset_number)) and found[0] == total:
                        copy.asset_number = ""
                        if not copy.description or blank_tag(copy.description):
                            copy.description = found[1]
                    if bare_count(asset.description) == total:
                        copy.description = ""
                    elif (found := phrase_count(asset.description)) and found[0] == total:
                        copy.description = found[1]
                    for field_name in ("recoverable", "cost", "acc_dep", "nbv", "ytd"):
                        setattr(copy, field_name, per_item_amount(getattr(copy, field_name), total))
                    copy.extras["unit"] = f"item {running} of {total}"
                exploded.append(copy)
    return exploded


def blank_tag(value: str) -> bool:
    text = norm(value)
    return not text or bool(re.search(r"not engrav|n a|none|nil", text))


def identity_item(item: str) -> str:
    parenthetical = parenthetical_quantity(item)
    if parenthetical:
        return parenthetical[0]
    trailing = trailing_quantity(item)
    if trailing:
        return trailing[0]
    return item


def line_signature(asset: Asset) -> tuple[str, ...]:
    """Identity of one recorded line, ignoring which workbook it came from."""
    tag = "" if blank_tag(asset.tag) else norm(asset.tag)
    item = norm(identity_item(asset.item))
    if tag:
        return ("tag", tag, item)
    description = "" if bare_count(asset.description) else norm(asset.description)
    return ("line", item, description, norm(asset.status), norm(asset.department))


def represented_count(asset: Asset) -> int:
    _, groups = decide_groups(asset, alone=True)
    return sum(count for count, _ in groups)


def union_facility_submissions(assets: list[Asset]) -> tuple[list[Asset], list[str]]:
    """Keep every distinct item when a facility was submitted more than once.

    The same line in two returns is kept once, at the larger recorded count.
    An item that appears in only one return is kept.
    """
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
        buckets: dict[tuple[str, ...], list[Asset]] = defaultdict(list)
        for rows in sources.values():
            for asset in rows:
                buckets[line_signature(asset)].append(asset)
        folded = 0
        for rows in buckets.values():
            by_file: dict[str, list[Asset]] = defaultdict(list)
            for asset in rows:
                by_file[asset.source_file].append(asset)
            if len(by_file) < 2:
                continue
            winner = max(
                by_file,
                key=lambda name: (
                    sum(represented_count(asset) for asset in by_file[name]),
                    len(by_file[name]),
                ),
            )
            for name, file_rows in by_file.items():
                if name == winner:
                    continue
                folded += len(file_rows)
                for asset in file_rows:
                    drop.add(id(asset))
        if folded:
            sample = next(iter(next(iter(sources.values()))))
            notes.append(
                f"{sample.facility} ({sample.lg}): {len(sources)} returns combined; "
                f"{folded} repeated lines folded in; items found in only one return were kept."
            )
    kept = [asset for asset in assets if id(asset) not in drop]
    return kept, notes


def check_examples() -> None:
    def groups(item="", status="", remarks="", qty=None, alone=True, asset_number="", description="", tag=""):
        asset = Asset(
            item=item, status=status, remarks=remarks, explicit_qty=qty,
            asset_number=asset_number, description=description, tag=tag,
        )
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
    assert groups(item="Office chairs", asset_number="286", tag="N/A") == ("Office chairs", [(286, None)])
    assert groups(item="Examination Couch 2") == ("Examination Couch", [(2, None)])
    assert groups(item="Autoclave 20 Liters., Duo Operated 2")[0].endswith("Operated")
    assert groups(item="Autoclave 20 Liters., Duo Operated 2")[1] == [(2, None)]
    assert groups(item="Desks", description="120", tag="N/A")[1] == [(120, None)]
    assert groups(item="CPU", asset_number="15", tag="SSUGU-SEED PC/02")[1] == [(1, None)]
    assert groups(item="Desks", asset_number="120", alone=False)[1] == [(1, None)]
    assert groups(item="HP LASERJET 1300")[1] == [(1, None)]
    assert groups(item="HP LAPTOP 840")[1] == [(1, None)]
    assert groups(item="LASERJET 1320")[1] == [(1, None)]
    assert groups(item="School desks 120") == ("School desks", [(120, None)])
    assert groups(item="Counting chamber", asset_number="2 microscopes, white", tag="N/A")[1] == [(2, None)]
    assert groups(item="Monitor", description="15 inch screen")[1] == [(1, None)]
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
        "Each physical item is one row, the same rule as the 22 September register. Where a source line stated a quantity, that line was repeated once per item. Unit shows item 1 of 100, and the units column in the GOU template is 1.",
        "A quantity was taken from a quantity column, a number in brackets, a trailing count on the item name such as Examination Couch 2, a bare number in Asset Number or the description when that was the only line for the item, or a count written in the status or remarks. Lines that were already one row per item were left as one row.",
        "Where a grouped line carried one cost, that figure was treated as the line total and divided by the quantity, so each asset row holds its share.",
        "Spreadsheets and Word verification tables under raw-data-grouped were read, except programme-documents. The data-management chat in that folder is the exception.",
        "Photographs, narrative reports and the reconciliation lists are not asset lines.",
        "Draft sheets were left out where the same workbook already had a consolidated sheet with local government and facility columns.",
        "Where a team submitted more than one workbook for the same facility, the lists were combined. A repeated line was kept once, at the larger count. An item present in only one return was kept.",
        "",
        "Sources:",
        *sources,
        "",
        "Facilities combined from more than one return:",
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
    collected, overlap_notes = union_facility_submissions(collected)
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
