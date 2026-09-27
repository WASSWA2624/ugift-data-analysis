"""Merge shared UgIFT asset registers into one workbook.

Sources are the shared workbooks under raw-data-grouped (team, district and
multi-team files), not facility-by-facility copies. The column layout follows
new-templates-to-follow. A source line that states a quantity becomes that
many rows, one physical item each.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import pickle
import re
import sys
import zipfile
from xml.etree import ElementTree
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path

import xlrd
from docx import Document
from openpyxl import Workbook, load_workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asset_source_layouts import (
    repair_nshwere_furniture,
    repair_nyamarwa_air_conditioner,
    repair_reviewed_unit_blocks,
)
from ugift_places import (
    LocalGovernment,
    _edit_distance,
    canonical_facility,
    facility_base,
    facility_key,
    facility_kind,
    fuzzy_owner,
    is_placeholder,
    known_facilities,
    known_local_governments,
    lg_from_text,
    lg_of_known_facility,
    resolve_lg,
    resolve_mda,
)

ROOT = Path(__file__).resolve().parents[1]
GROUPED = ROOT / "raw-data-grouped"
RECONCILIATION = GROUPED / "facility-reconciliation.csv"
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

# The SK column each Asset field is written to (for the Read Me fill counts).
HEADER_OF_FIELD = {
    "life": "Life in Months", "purchase": "Date Of Purchase", "service": "Date Placed In Service",
    "recoverable": "Recoverable cost", "cost": "Cost", "acc_dep": "Acc Dep Cost", "nbv": "Net Book Value",
    "ytd": "Ytd Deprn", "department": "Department", "description": "Item Description",
}

MODEL_TAIL = re.compile(
    r"(?i)^(laserjet|laptop|printer|elitebook|probook|latitude|inspiron|pavilion|"
    r"thinkpad|monitor|cpu|iphone|samsung|nokia|tecno|inch|gen|core|mhz|gb)$"
)
# A model family anywhere in the name makes a trailing number a model, not a count.
MODEL_FAMILY = re.compile(r"(?i)\b(laserjet|laptop|elitebook|probook|latitude|inspiron|pavilion|thinkpad|thinkbook|ideapad|printer|deskjet|officejet|prolite|optiplex|vostro|(?:ms|microsoft)\s+office|office\s+(?:pro|professional)|windows)\b")
# A number beside one of these labels is an identifier, date or amount. Explicit
# quantity phrases elsewhere in the same cell remain eligible for extraction.
NUMBER_CONTEXT = re.compile(
    r"(?i)\b(?:serial|model|engine|chassis|registration|reg\.?\s*no|"
    r"asset\s*(?:id|no|number)|tag\s*(?:id|no|number)|code|cost|price|amount|"
    r"ugx|ush|ugshs?|shillings?|shs|usd|eur|gbp|manufactur\w*|acquir\w*|"
    r"purchas\w*|power|voltage|capacity|dimensions?|length|width|height|date|year|january|february|march|april|may|june|july|august|"
    r"september|october|november|december)\b"
)
WORD_COUNTS = {
    "a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90,
}
COUNT_SCALES = {"hundred": 100, "thousand": 1000, "million": 1000000, "billion": 1000000000, "trillion": 1000000000000}
NUMBER_WORD = "(?:" + "|".join((*WORD_COUNTS, *COUNT_SCALES)) + ")"
COUNT_WORD = rf"(?:\d+(?:,\d{{3}})*|{NUMBER_WORD}(?:[ -]+(?:and[ -]+)?{NUMBER_WORD})*)"
# A decimal fraction or signed negative must never contribute its integer tail.
COUNT_START = r"(?<![\w,/\-−])(?<!\d\.)"
COUNT_END = r"(?![\d.,])\b"


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


def squash(value: object) -> str:
    """Header text without spaces, so 'Equipme nt Item' and 'Equipment/Item' compare equal."""
    return norm(value).replace(" ", "")


def as_count(token: str) -> int | None:
    token = clean(token).casefold().replace(",", "")
    if token.isdecimal():
        return int(token)
    total = current = 0
    for word in re.split(r"[ -]+", token):
        if word == "and":
            continue
        if word in WORD_COUNTS:
            current += WORD_COUNTS[word]
        elif word == "hundred":
            current = (current or 1) * 100
        elif word in COUNT_SCALES:
            total += (current or 1) * COUNT_SCALES[word]
            current = 0
        else:
            return None
    return total + current or None


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


# Files under raw-data-grouped that carry an asset table but are not a return of
# the facility they are filed under. Each is left out with its reason on Read Me.
EXCLUDED_SOURCES: dict[str, str] = {
    "team-13/Tororo/Kamuli-HC-III/88_facility-fixed-asset-register_ref-kamuli.xls":
        "IFMS fixed-asset register format example: its rows name Jinja Regional Referral Hospital "
        "wards, vehicles and plots, not Kamuli Health Centre III assets.",
}

# Folders whose workbooks are programme lists or later copies of returns that are
# already read from the team folders. Each is left out with its reason on Read Me.
EXCLUDED_FOLDERS: dict[str, str] = {
    "_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams":
        "The MDA status registers there are programme supply and WIP lists (55,468 of 58,818 rows are "
        "'programme supply, not field-verified' transcriptions of programme-documents), and the LG register and "
        "registers-by-facility workbooks are later copies of the team-10 to team-15 Asset-Verification-Toolkit "
        "returns that are read from the team folders. Reading both would count each facility two to five times.",
    "_multi-team/teams-10-15/pdf-to-excel":
        "Conversions of the TELA phone and tablet distribution lists and a scanned supply schedule: distribution "
        "lists record what was supplied, not what a facility holds.",
}

# Every folder a byte-identical copy of a source was filed under. A combined
# health-centre-and-school return is filed under both facilities, so the copy that
# is read keeps both contexts and each table is assigned to the facility of its kind.
CONTEXTS: dict[Path, list[tuple[str, str]]] = {}


def candidate_files() -> list[Path]:
    found: list[Path] = []
    for path in GROUPED.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".xls", ".xlsx", ".docx"}:
            continue
        if path.name.startswith("~$"):
            continue
        if excluded_programme_file(path):
            continue
        relative = path.relative_to(GROUPED).as_posix()
        if relative in EXCLUDED_SOURCES or any(relative.startswith(folder + "/") for folder in EXCLUDED_FOLDERS):
            continue
        found.append(path)
    grouped: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for path in found:
        grouped[(str(path.parent).casefold(), path.stem.casefold())].append(path)
    chosen: list[Path] = []
    for paths in grouped.values():
        suffixes = {item.suffix.lower() for item in paths}
        if ".docx" in suffixes and suffixes & {".xls", ".xlsx"}:
            # The same stem as a spreadsheet and a Word file: keep the spreadsheet.
            paths.sort(key=lambda item: (
                {".xlsx": 0, ".xls": 1, ".docx": 2}.get(item.suffix.lower(), 3),
                -item.stat().st_size, len(str(item)), str(item),
            ))
            chosen.append(paths[0])
        else:
            chosen.extend(paths)
    by_digest: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(chosen, key=lambda item: str(item).casefold()):
        by_digest[file_hash(path)].append(path)
    unique: list[Path] = []
    CONTEXTS.clear()
    for copies in by_digest.values():
        # Prefer the copy filed under a facility folder over a team-level copy.
        copies.sort(key=lambda item: (not path_context(item)[1], not path_context(item)[0], str(item).casefold()))
        kept = copies[0]
        contexts: list[tuple[str, str]] = []
        for copy in copies:
            context = path_context(copy)
            if context[0] and context not in contexts:
                contexts.append(context)
        CONTEXTS[kept] = contexts
        unique.append(kept)
    unique.sort(key=lambda item: str(item).casefold())
    return unique


def docx_has_asset_table(path: Path) -> bool:
    """The prompt's test: an Equipment/Item header, or a description column with
    condition, quantity, tag, or cost. Word splits header words across runs, so the
    text is compared with tags and spaces removed."""
    # A damaged/unreadable document is a source error, not evidence of no table.
    # The caller records it in the source audit so it can be retried explicitly.
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    tables = re.findall(rb"<w:tbl>.*?</w:tbl>", xml, re.S)
    for table in tables:
        text = re.sub(rb"<[^>]+>", b"", table)
        blob = re.sub(rb"[^a-z0-9]+", b"", text.lower())
        if b"equipmentitem" in blob or b"equipmentasset" in blob:
            return True
        if b"description" in blob and any(
            token in blob for token in (b"condition", b"status", b"quantity", b"qty", b"tagnumber", b"engrave", b"cost")
        ):
            return True
        if b"item" in blob and any(token in blob for token in (b"quantity", b"qty", b"supplied", b"found", b"functional")):
            return True
    return False


W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
HEALTH_SECTION = re.compile(r"(?i)^\s*(health\s+cent(?:re|er)s?(\s+checklist)?|health\s+facilit(?:y|ies))\b")
SCHOOL_SECTION = re.compile(
    r"(?i)^\s*(school\s+verification|school\s+interview|school\s+furniture|ict\s+items\s+to\s+verify|"
    r"buildings\s+to\s+verify|seed\s+schools?|schools?\s+checklist)\b"
)


def docx_cell_text(tc) -> str:
    return clean(xml_text(tc))


MC_FALLBACK = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"


def xml_text(element) -> str:
    """The text of a Word element: line breaks and paragraph ends become spaces, and
    the duplicate copy of a text box kept for old Word versions (mc:Fallback) is
    read once."""
    pieces: list[str] = []

    def walk(node) -> None:
        if node.tag == MC_FALLBACK:
            return
        if node.tag == f"{W_NS}t":
            pieces.append(node.text or "")
        elif node.tag in (f"{W_NS}br", f"{W_NS}tab", f"{W_NS}cr"):
            pieces.append(" ")
        elif node.tag == f"{W_NS}p" and pieces:
            pieces.append(" ")
        for child in node:
            walk(child)

    walk(element)
    return "".join(pieces)


def docx_grid_rows(table_element) -> list[list[object]]:
    """Table rows laid on the column grid, so a horizontally merged cell fills its
    first grid column and leaves the rest blank instead of repeating its text."""
    rows: list[list[object]] = []
    for tr in table_element.iter(f"{W_NS}tr"):
        row: list[object] = []
        for tc in tr.findall(f"{W_NS}tc"):
            span = 1
            properties = tc.find(f"{W_NS}tcPr")
            if properties is not None:
                grid = properties.find(f"{W_NS}gridSpan")
                if grid is not None:
                    try:
                        span = max(1, int(grid.get(f"{W_NS}val", "1")))
                    except ValueError:
                        span = 1
            row.append(docx_cell_text(tc))
            row.extend([""] * (span - 1))
        rows.append(row)
    return rows


def docx_tables(path: Path) -> list[tuple[str, list[list[object]], str]]:
    """Tables in document order, each preceded by the paragraphs written since the
    previous table (the toolkit's "Name of LG ... Name of SCHOOL ..." banners), with
    the checklist section the table sits in: Health centre, School, or blank."""
    document = Document(path)
    tables: list[tuple[str, list[list[object]], str]] = []
    pending: list[list[object]] = []
    section = ""
    index = 0
    for child in document.element.body.iterchildren():
        tag = child.tag.replace(W_NS, "")
        if tag == "p":
            text = clean(xml_text(child))
            if not text:
                continue
            if HEALTH_SECTION.match(text):
                section = "Health centre"
            elif SCHOOL_SECTION.match(text):
                section = "School"
            if len(text) <= 200:
                pending.append([text])
        elif tag == "tbl":
            index += 1
            rows = docx_grid_rows(child)
            labels = label_rows(rows)
            if labels:
                # A two-column details table ("Name of Local Government" | "Amuria")
                # is a banner for the asset tables that follow it.
                pending.extend(labels)
            tables.append((f"Table {index}", list(pending) + rows, section))
            pending = []
    return tables


LABEL_CELL = re.compile(
    r"(?i)^\s*(name\s+of\s+(the\s+)?)?(lg|l\.g\.?|local\s+government|district|health\s+facility|facility|school|"
    r"health\s+cent(re|er)(\s*iii)?|seed\s+school|facility\s+name|school\s+name)\s*:?\s*$"
)


def label_rows(rows: list[list[object]]) -> list[list[object]]:
    """Banner pseudo-rows from a details table of label | value pairs."""
    found: list[list[object]] = []
    if len(rows) > 40:
        return found
    for row in rows:
        cells = [clean(value) for value in row if clean(value)]
        if len(cells) != 2 or not LABEL_CELL.match(cells[0]) or is_placeholder(cells[1]):
            continue
        label = cells[0].rstrip(": ")
        if re.search(r"(?i)lg|local\s+government|district", label):
            found.append([f"NAME OF LG: {cells[1]}"])
        else:
            found.append([f"NAME OF FACILITY: {cells[1]}"])
    return found


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
    """Map a template header row (Equipment/Item, Department, ...) to field names.

    Header words are compared without spaces because Word tables often break a
    word across runs ("Equipme nt Item", "Item descriptio n", "Date of purcha se").
    """
    keys = [squash(value) for value in row]
    if not any(keys):
        return None
    has_equipment = any(key.startswith("equipmentitem") or key == "equipment" for key in keys)
    mapping: dict[str, int] = {}
    fallback_remarks: int | None = None
    for index, key in enumerate(keys):
        if not key or key in INDEX_KEYS:
            continue
        text = clean(row[index])
        if re.search(r"supplied|delivered|calloff|ordered|deficit|expected|requisition", key):
            # What was supplied or ordered is not what was found.
            continue
        field_name = None
        if key.startswith("equipmentitem") or key.startswith("equipmentname") or key in ITEM_KEYS:
            # "Equipment / Item Description", "Equipment Name", "Asset Description":
            # the item column, whatever sits in the line-number column before it.
            field_name = "item"
        elif "status" in key and ("note" in key or "location" in key):
            # "Status / Location / Notes" is free text; a plain status column wins.
            fallback_remarks = index if fallback_remarks is None else fallback_remarks
        elif "status" in key or key == "condition" or "functionality" in key:
            field_name = "status"
        elif "remark" in key:
            field_name = "remarks"
        elif "tag" in key or "engrave" in key:
            field_name = "tag"
        elif key.startswith("life") or "lifeinmonth" in key:
            field_name = "life"
        elif "purcha" in key or "datepurchased" in key or key.startswith("dateofpur"):
            field_name = "purchase"
        elif "placed" in key:
            field_name = "service"
        elif "recover" in key:
            field_name = "recoverable"
        elif "accdep" in key or "accumulated" in key:
            field_name = "acc_dep"
        elif "netbook" in key:
            field_name = "nbv"
        elif "ytd" in key or "deprn" in key or "depreciation" in key:
            field_name = "ytd"
        elif "assetnumber" in key or key == "assetno":
            field_name = "asset_number"
        elif "descriptio" in key:
            field_name = "description"
        elif key.startswith("equipmentitem") or key == "equipment" or key == "equipmentasset":
            field_name = "item"
        elif key == "item":
            field_name = "description" if has_equipment else "item"
        elif "department" in key:
            field_name = "department"
        elif key in {"qty", "quantity"} or key.startswith(("qty", "quantity", "numberverified", "noverified", "physicalcount", "countverified")) or key.endswith("qty"):
            field_name = "explicit_qty"
        elif "serial" in key:
            field_name = "serial"
        elif key.startswith("manufactur") or key == "make":
            field_name = "manufacturer"
        elif key.startswith("model"):
            field_name = "model"
        elif key in {"cost", "initialcost", "costugx"} or key.startswith("cost"):
            field_name = "cost"
        elif "localgov" in key or key in {"district", "localgovernment", "localgovt", "mda"}:
            field_name = "lg"
        elif any(token in key for token in ("healthcentre", "healthcenter", "hospital", "school", "location", "facility")):
            field_name = "facility"
        elif key in {"education", "educational", "health", "edn"} and index == mapping.get("item", -2) + 1:
            # The Department header cell overtyped with the department itself.
            field_name = "department"
        elif key.endswith("district") or resolve_lg(text, fuzzy=False) is not None:
            # A consolidation sheet that typed the block's district into the header cell.
            field_name = "lg"
        elif looks_like_facility(text) and facility_kind(text):
            field_name = "facility"
        if field_name and field_name not in mapping:
            mapping[field_name] = index
            if field_name == "facility" and facility_kind(text) and not re.search(r"(?i)location|physical", text):
                # "HEALTH CENTRE" / "SCHOOL" over the column: its bare names are that kind.
                mapping["facility_header_kind"] = facility_kind(text)
    if "remarks" not in mapping and fallback_remarks is not None:
        mapping["remarks"] = fallback_remarks
    if "item" not in mapping and "description" in mapping and (not keys[0] or keys[0] in INDEX_KEYS or 0 in mapping.values()):
        # The description column beside a line-number column names the item.
        mapping["item"] = mapping.pop("description")
    if "item" not in mapping and "department" in mapping and ("asset_number" in mapping or "tag" in mapping) \
            and len(mapping) >= 5 and 0 not in mapping.values() and keys[0] not in INDEX_KEYS:
        # A header whose first cell was overtyped ("MCH" for "Equipment/ Item").
        mapping["item"] = 0
    if "item" in mapping and len([name for name in mapping if name != "facility_header_kind"]) >= 4:
        return mapping
    return None


# Line-number columns: never the item, never a count.
INDEX_KEYS = {
    "vote", "itemno", "sn", "sno", "srno", "slno", "no", "nos", "number", "pgno", "s", "sr", "sl", "count",
    "line", "id", "ref", "sr.no", "itemnumber", "lineno", "num",
}
TOTAL_ITEM = re.compile(r"(?i)^\s*(?:sub|grand)?\s*totals?\b")
ITEM_KEYS = {
    "equipment", "equipmentasset", "equipments", "equipmentsitem", "assetequipment", "assetdescription",
    "assetsdescription", "itemname", "nameofitem", "assetname", "nameofasset", "equipmentdescription",
    "nameofequipment", "descriptionofasset", "descriptionofequipment",
}


def looks_like_facility(text: str) -> bool:
    """A named school or health facility: a type word alone ("Health", "Education",
    "Seed school"), a count ("2 at school") or a department is not a facility name."""
    text = clean(text)
    if len(text) < 4 or len(text) > 80 or is_placeholder(text) or re.match(r"\d", text):
        return False
    if re.search(r"(?i)regional blood bank|\bhospital\b|ministry of", text):
        return True
    if not facility_kind(text):
        return False
    if HEALTH_SECTION.match(text) or SCHOOL_SECTION.match(text) or re.search(
        r"(?i)\b(checklist|interview|discussion|verification|furniture|ict items|buildings to|equipment)\b", text
    ):
        return False
    if re.search(
        r"(?i)\b(fences?|blocks?|tanks?|latrines?|toilets?|desks?|chairs?|tables?|beds?|stools?|kits?|sets?|machines?|"
        r"computers?|printers?|uniforms?|textbooks?|books?|shelves|shelf|thermometers?|instrument|basic|pit|kitchen|bins?)\b",
        text,
    ) and not re.search(r"(?i)name\s+of", text):
        # "School fence", "Instrument set, ENT Basic for HCIII": an item, not a place.
        return False
    base = facility_base(text)
    if re.search(r"\d{3,}", base) or re.match(r"(ugift|team|sheet|table|copy|final|residential|non residential|buildings?)\b", base):
        return False
    if len(base.split()) > 6:
        return False
    return len(base) >= 3 and base not in {
        "education", "educational", "health", "edn", "primary", "secondary", "seed", "general", "the", "at",
        "furniture", "items", "buildings", "name", "facility", "ugift", "ugift health", "ugift health 2",
    }


def strip_lg_prefix(text: str) -> tuple[str, str]:
    """'LIRA DISTRICT LOCAL GOVERNMENT ANYOMOREM HEALTH CENTRE III' -> (lg, facility)."""
    match = re.match(
        r"(?i)^\s*(?:name\s+of\s+lg\s*:?\s*)?([A-Za-z][A-Za-z' \-]{2,30}?\s+(?:district\s+local\s+gov(?:ernment|'?t)|"
        r"district|dlg|municipal\s+council|municipality|city\s+council|city|mc|lg|dc))\b[\s,:\-–]*(.+)$",
        text,
    )
    if match and resolve_lg(match.group(1)) and looks_like_facility(match.group(2)):
        return match.group(1), clean(match.group(2))
    return "", text


PLACE_HEADER = re.compile(r"(?i)district|local\s*gov|facility|school|health|location|hospital|lg\b|hc\b|centre|center")


def trailing_place_columns(rows: list[list[object]], mapping: dict[str, int], header: list[object] | None = None) -> dict[str, int]:
    """Map unlabeled columns that hold local government and facility names.

    Only a column whose header is blank or names a place is considered, and it
    counts as the local-government column only when most of its values name a
    known local government, and as the facility column only when most of its
    values read as a school or health facility. Item names, counts, amounts, and
    section labels such as "ENT Basic for HCIII" do not qualify.
    """
    if "lg" in mapping and "facility" in mapping:
        return mapping
    used = set(mapping.values())
    if header is not None:
        for index, value in enumerate(header):
            text = clean(value)
            if text and not PLACE_HEADER.search(text) and resolve_lg(text, fuzzy=False) is None \
                    and not (looks_like_facility(text) and facility_kind(text)) and not bare_place_name(text):
                # A place name typed into the header cell ("KYIKWAKYA") still heads a
                # place column; any other heading rules the column out.
                used.add(index)
    lg_scores: Counter[int] = Counter()
    facility_scores: Counter[int] = Counter()
    bare_scores: Counter[int] = Counter()
    filled: Counter[int] = Counter()
    for row in rows[:120]:
        for index, value in enumerate(row):
            text = clean(value)
            if index in used or not text:
                continue
            filled[index] += 1
            if len(text) > 80:
                continue
            if resolve_lg(text) is not None:
                lg_scores[index] += 1
            elif looks_like_facility(text):
                facility_scores[index] += 1
            header_text = clean(header[index]) if header is not None and index < len(header) else ""
            if bare_place_name(text) and (not header_text or bare_place_name(header_text)):
                # An unlabeled column of bare names beside the district column ("MASAKA"
                # is a health centre here even though a district shares the name).
                bare_scores[index] += 1
    updated = dict(mapping)
    if "lg" not in updated:
        best = [index for index, count in lg_scores.most_common() if count >= 3 and count >= 0.6 * filled[index]]
        if best:
            updated["lg"] = best[0]
    if "facility" not in updated:
        best = [
            index for index, count in facility_scores.most_common()
            if count >= 3 and count >= 0.6 * filled[index] and index != updated.get("lg")
        ]
        if best:
            updated["facility"] = best[0]
        elif "lg" in updated:
            near = [
                index for index, count in bare_scores.most_common()
                if count >= 3 and count >= 0.6 * filled[index] and index > updated["lg"] and index <= updated["lg"] + 2
            ]
            if near:
                updated["facility"] = near[0]
                updated["facility_header_kind"] = ""
    return updated


NAME_OF_LG = (
    r"(?:(?:name\s+of\s+(?:the\s+)?(?:lg|l\.g\.?|local\s+government|district)|district|local\s+government)\s*[:\-]\s*"
    r"|name\s+of\s+(?:the\s+)?(?:lg|l\.g\.?|local\s+government|district)\s*)"
)
NAME_OF_FACILITY = (
    r"(?:(?:name\s+of\s+(?:the\s+)?(?:health\s+)?(?:facility|school|health\s+cent(?:re|er)|seed\s+school|h/?c(?:\s*iii)?)|"
    r"facility\s+name|health\s+facility|facility|school\s+name|school|health\s+cent(?:re|er))\s*[:\-]\s*|"
    r"name\s+of\s+(?:the\s+)?(?:health\s+)?(?:facility|school|health\s+cent(?:re|er)|seed\s+school|h/?c(?:\s*iii)?)\s*)"
)


def banner_part(text: str) -> str:
    """A name written on a dotted template line, without the dots and placeholders."""
    text = clean(re.sub(r"[.…_]{2,}|(?<=\s)[.…_](?=\s)", " ", text)).strip(" :-–—.,")
    # The name ends where the next template heading starts ("... SCHOOL VERIFICATION
    # CHECKLIST NAME OF THE SCHOOL ...", "... NB: ...").
    text = re.split(
        r"(?i)\s+(?:school|health\s+cent(?:re|er))\s+verification\s+checklist|\s+checklist\b|\s+name\s+of\s+|\s+n\.?b\.?\s*:|\s+notes?\s*:",
        text,
    )[0].strip(" :-–—.,")
    if is_placeholder(text):
        return ""
    # "MAMBA SEED SECONDARY SCHOOL – NEBBI DLG" names the government after a dash.
    return text


def split_trailing_lg(facility: str) -> tuple[str, str]:
    match = re.search(r"^(.*?)[\s,]+[–\-]\s*([A-Za-z][A-Za-z .'\-]{2,40}(?:\bdlg|\bdistrict|\bmc|\bcity|\blg|\bdc)\.?)\s*$", facility, re.I)
    if match and resolve_lg(match.group(2)):
        return clean(match.group(1)), clean(match.group(2))
    # "KYEIHARA HC III MITOOMA": the last word or two name the local government.
    words = clean(facility).split()
    for size in (2, 1):
        if len(words) > size + 1:
            head, tail = " ".join(words[:-size]), " ".join(words[-size:])
            if resolve_lg(tail, fuzzy=False) and facility_kind(head) and looks_like_facility(head):
                return head, tail
    return facility, ""


def parse_banner(text: str) -> tuple[str, str] | None:
    raw = clean(text)
    if len(raw) < 6 or is_placeholder(raw):
        return None
    low = raw.casefold()
    asset_word = re.search(
        r"\b(machine|desks?|chairs?|stools?|autoclave|bowl|computer|monitor|cupboard|printer|tables?|"
        r"set|instrument|beds?|mask|kit|apparatus|shelves|screen|projector|trolley|stand|scale|meter)\b",
        low,
    )
    if asset_word and "name of" not in low and "ugift asset" not in low and not re.search(r"(?i)\b(district|dlg|d\.?c\.?|mc|city)\b", low):
        return None
    match = re.search(rf"(?i){NAME_OF_LG}(.*?)\s*{NAME_OF_FACILITY}(.*)$", raw)
    if match:
        facility, extra = split_trailing_lg(banner_part(match.group(2)))
        return banner_part(match.group(1)) or extra, facility
    match = re.search(rf"(?i){NAME_OF_FACILITY}(.*)$", raw)
    if match:
        facility, extra = split_trailing_lg(banner_part(match.group(1)))
        return extra, facility
    match = re.search(rf"(?i){NAME_OF_LG}(.*)$", raw)
    if match:
        return banner_part(match.group(1)), ""
    match = re.search(r"(?i)^(.+?)\s+ugift\s+asset\s+verification.*?,\s*(.+)$", raw)
    if match:
        return clean(match.group(2)), clean(match.group(1))
    match = re.search(r"(?i)^(.+?)\s+ugift\s+asset\s+verification\s+tool\s*kit\s+(.+)$", raw)
    if match:
        return clean(match.group(2)), clean(match.group(1))
    if "," in raw and re.search(r"(?i)hc\s*(?:ii+|iv)?|health|school|\bsss\b|seed", raw):
        # "BITSYA HCIII, BUHWEJU DC" names the facility, then its government. An item
        # such as "Instrument set, ENT Basic for HCIII" has no government after its comma.
        parts = [clean(part) for part in raw.split(",") if clean(part)]
        if len(parts) >= 2 and resolve_lg(parts[-1]) is not None and looks_like_facility(parts[0]):
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
    # A cell holding nothing but a facility name ("ADEKNINO HC II", "Kigumba S.S.S").
    if len(raw) <= 60 and looks_like_facility(raw) and not re.search(r"(?i)\b(machine|set|kit|bin|bed|chair|desk|stool|table)\b", raw):
        return "", raw
    return None


def first_text(row: list[object]) -> str:
    for value in row:
        text = clean(value)
        if text:
            return text
    return ""


def row_text(row: list[object]) -> str:
    """Every filled cell of a row in one string, so a banner split over cells
    ("NAME OF LG:" | "DOKOLO" | "NAME OF HEALTH FACILITY:" | "ADOK HC III") reads whole."""
    return clean(" ".join(clean(value) for value in row if clean(value)))


def bare_integer(value: object) -> int | None:
    """A cell holding only a whole number. Excel turns a typed "(3)" into -3, so the
    sign is dropped."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)) and float(value).is_integer():
        return abs(int(value))
    text = clean(value).replace(",", "")
    if re.fullmatch(r"[-(]?\d+\)?", text):
        return abs(int(re.sub(r"[()\s]", "", text)))
    # "2+3 = 5" or "2 + 3": the count written as a sum of the per-room counts.
    if re.fullmatch(r"[\d\s+=()\-]+", text) and re.search(r"\d", text):
        numbers = [int(number) for number in re.findall(r"\d+", text)]
        if "=" in text:
            return numbers[-1]
        return sum(numbers) if "+" in text else numbers[0]
    return None


def placeholder_only(asset: Asset) -> bool:
    """A template line with nothing but the item name: every other field blank, a
    dash, or dots. It records no asset."""
    fields = [
        asset.department, asset.asset_number, asset.description, asset.tag, asset.status, asset.remarks,
        asset.life, asset.purchase, asset.service, asset.recoverable, asset.cost, asset.acc_dep, asset.nbv, asset.ytd,
    ]
    for value in fields:
        if value in (None, ""):
            continue
        if isinstance(value, str) and (is_placeholder(value) or re.fullmatch(r"[\-–—.…_/ ]+", value)):
            continue
        return False
    return True


FRAGMENT = re.compile(r"(?i)^(?:[\(\[]?\d+[\)\]]?\s+\w+|one|two|three|four|five|six|[a-z(]).{0,40}$")
NOT_RECEIVED = re.compile(r"(?i)^(?:didn'?t\s+receive|not\s+received|none\s+received|nil)\b")
# A department or room written where the item name goes, on a continuation row:
# "MCH (2)", "OPD(1) STORE (1)", "General ward".
DEPARTMENT_WORD = re.compile(
    r"(?i)^(?:(?:mch|opd|ipd|store|stores|lab|laboratory|maternity|general|ward|theatre|theater|kitchen|office|"
    r"admin|administration|dispensary|pharmacy|records|reception|staff\s*room|library|classroom|dormitory|"
    r"emergency|paediatric|pediatric|antenatal|postnatal|delivery|injection|dressing|treatment|inpatient|outpatient)"
    r"\s*(?:ward|room|block|unit)?\s*[\(\[]?\s*\d{0,3}\s*[\)\]]?\s*[,;/&+]?\s*){1,4}$"
)


def cell(row: list[object], mapping: dict[str, int], name: str) -> object:
    index = mapping.get(name)
    if index is None or index >= len(row):
        return None
    return row[index]


def looks_like_subheader(asset: Asset) -> bool:
    return norm(asset.description) == "description" and not any([
        asset.item, asset.tag, asset.status, asset.remarks, asset.cost, asset.asset_number,
    ])


def looks_like_label(asset: Asset, row: list[object] | None = None) -> bool:
    if asset.tag or asset.status or asset.cost not in (None, "") or asset.asset_number:
        return False
    text = asset.item or asset.description
    if not text and row is not None:
        filled = [clean(value) for value in row if clean(value)]
        text = filled[0] if len(filled) == 1 else ""
    if not text or asset.department:
        return False
    banner = parse_banner(text)
    return banner is not None and bool(banner[0] or banner[1])


def facility_type_for(facility: str, department: str, sheet: str, filename: str) -> str:
    """'School' or 'Health centre', the only two facility types the register uses."""
    kind = facility_kind(facility)
    if kind:
        return kind
    if re.search(r"(?i)blood\s*bank|hospital|clinic|referral", facility):
        # A regional blood bank or hospital is a health facility in the two-kind scheme.
        return "Health centre"
    kind = facility_kind(department)
    if kind:
        return kind
    if re.search(r"(?i)\beducation(al)?\b|\bedn\b|academics?|classroom|laborator|library|dormitor", department):
        return "School"
    if re.search(r"(?i)\bopd\b|\bmch\b|maternity|\bward\b|\bipd\b|theatre|dispens", department):
        return "Health centre"
    broader = f"{sheet} {filename}"
    if re.search(r"health|hospital|\bhc\b|hciii", broader, re.I) and not re.search(r"school|\bsss?\b|seed", broader, re.I):
        return "Health centre"
    if re.search(r"school|education|\bsss?\b|seed", broader, re.I) and not re.search(r"health|hospital|\bhc\b|hciii", broader, re.I):
        return "School"
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


def same_place(left: str, right: str) -> bool:
    """Two spellings of one facility name: equal bases, a few edits apart with the
    same opening, or the same letters in another order."""
    a, b = facility_base(left), facility_base(right)
    if not a or not b:
        return False
    if a == b or sorted(a) == sorted(b):
        return True
    if a[:1] != b[:1]:
        return False
    distance = _edit_distance(a, b)
    prefix = len(os.path.commonprefix([a, b]))
    return distance <= 2 or (distance == 3 and prefix >= 4 and min(len(a), len(b)) >= 6)


def bare_place_name(text: str) -> bool:
    """A value of a labelled facility column without a type word ("BUTAWATA" under
    a HEALTH CENTRE header); status, department and header words do not qualify."""
    text = clean(text)
    if not text or is_placeholder(text) or len(text.split()) > 4 or re.search(r"\d", text):
        return False
    if DEPARTMENT_WORD.match(text) or re.match(
        r"(?i)^(?:education(?:al)?|health|hospital|school|facility|location|name|n/?a|none|nil|yes|no|functional|"
        r"faulty|good|new|not|non|in\s+use|verified|broken|damaged|missing|total)(?![A-Za-z])",
        text,
    ):
        return False
    return re.fullmatch(r"[A-Za-z][A-Za-z .'\-/&]{2,45}", text) is not None


def unit_row(asset: Asset) -> bool:
    """A row without an item name that still records one unit: a description together
    with a department, tag, status, remark, cost or date. A wrapped line of the row
    above carries only a fragment of one cell."""
    if not asset.description:
        return False
    if re.match(r"^[a-z]", asset.description) and len(asset.description) < 25 and not asset.tag and not asset.status:
        return False
    others = sum(1 for value in (asset.department, asset.tag, asset.status, asset.remarks) if value)
    others += sum(1 for value in (asset.cost, asset.purchase, asset.service) if value not in (None, ""))
    return others >= 1


def merge_continuation(previous: Asset, current: Asset) -> None:
    previous.extras.setdefault("source_cells", []).extend(current.extras.get("source_cells", ()))
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
    explicit = quantity_cell(cell(row, mapping, "explicit_qty"))
    cost = number_or_text(cell(row, mapping, "cost"))
    unit_cost = number_or_text(cell(row, mapping, "unit_cost")) if "unit_cost" in mapping else None
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
        cost=cost if cost not in (None, "") else unit_cost,
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
    # Keep every column for explicit count phrases, including columns the toolkit
    # does not map. Numeric monetary/date/identifier cells are never bare counts.
    asset.extras["source_cells"] = [clean(value) for value in row if isinstance(value, str) and clean(value)]
    if norm(asset.item) in {"equipment item", "equipment", "description", "asset description", "item", "facility fitting installation"}:
        # A repeated header line, not an asset.
        asset.item = ""
        asset.extras["header_repeat"] = True
    elif asset.item and (is_placeholder(asset.item) or TOTAL_ITEM.match(asset.item)):
        # A dash, "N/A" or a "TOTAL ..." line names no asset.
        asset.item = ""
        asset.extras["placeholder_item"] = True
    # A merged Word cell read once per spanned column ("KYESS KYESS KYESS").
    asset.tag = re.sub(r"(?i)^(\S+)(?:\s+\1)+$", r"\1", asset.tag)
    # Model, serial and manufacturer columns are kept as stated facts in the description.
    for role, label in (("model", "Model"), ("serial", "Serial number"), ("manufacturer", "Made by")):
        value = clean(cell(row, mapping, role)) if role in mapping else ""
        if value and not is_placeholder(value):
            asset.description = join_text(asset.description, f"{label} {value}", "; ")
    if (cost in (None, "") and unit_cost not in (None, "")) or ("unit_cost" in mapping and "cost" not in mapping):
        # A unit price is already one item's share: it is not divided by the count.
        asset.extras["unit_cost"] = True
    if "explicit_qty" in mapping:
        asset.extras["qty_column"] = True
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
            mapped_rows.append((index, trailing_place_columns(rows[index + 1:index + 40], mapping, row)))
    if not mapped_rows:
        return []
    assets: list[Asset] = []
    carry_lg = fallback_lg
    carry_facility = ""
    carry_column = ""
    mapping = None
    header_indexes = {index for index, _ in mapped_rows}
    active = {index: item for index, item in mapped_rows}
    block_last: Asset | None = None
    pending: Asset | None = None
    for row_number, row in enumerate(rows, 1):
        if (row_number - 1) in header_indexes:
            mapping = active[row_number - 1]
            block_last = None
            pending = None
            # The facility carries across the furniture, ICT and buildings sub-tables of
            # one block until a banner, label row or place column names another.
            # A banner written on the rows just above the header names the block. A
            # data row of the previous block is not a banner.
            for above in rows[max(0, row_number - 9):row_number - 1]:
                filled = [clean(value) for value in above if clean(value)]
                text = row_text(above)
                if len(filled) > 4 and not re.search(r"(?i)name\s+of", text):
                    continue
                banner = parse_banner(text)
                if banner:
                    carry_lg = banner[0] or carry_lg
                    carry_facility = banner[1] or carry_facility
            continue
        if mapping is None:
            banner = parse_banner(row_text(row))
            if banner:
                carry_lg = banner[0] or carry_lg
                carry_facility = banner[1] or carry_facility
            continue
        if not any(clean(value) for value in row):
            continue
        asset = take_asset(row, mapping, source, f"{sheet_name} row {row_number}")
        if asset.extras.get("placeholder_item"):
            if not asset.description or is_placeholder(asset.description):
                continue
            asset.item, asset.description = asset.description, ""
        if looks_like_subheader(asset) or asset.extras.get("header_repeat"):
            # The "Description" sub-header row may carry the block's place columns.
            if asset.lg and resolve_lg(asset.lg):
                carry_lg = asset.lg
            if asset.facility and (looks_like_facility(asset.facility) or ("facility" in mapping and bare_place_name(asset.facility))):
                if not (carry_facility and same_place(asset.facility, carry_facility)):
                    carry_facility = asset.facility
            continue
        continuation = not asset.item and block_last is not None and (asset.description or asset.remarks or asset.tag or asset.status)
        if not continuation and looks_like_label(asset, row):
            banner = parse_banner(row_text(row)) or parse_banner(asset.item or first_text(row))
            if banner:
                carry_lg = banner[0] or carry_lg
                carry_facility = banner[1] or carry_facility
                block_last = None
            continue
        if asset.lg and (resolve_lg(asset.lg) or lg_from_text(asset.lg)):
            new_lg, old_lg = resolve_lg(asset.lg), resolve_lg(carry_lg) if carry_lg else None
            if new_lg is not None and old_lg is not None and new_lg.key != old_lg.key:
                # A new district block: the facility of the block above does not carry.
                carry_facility, carry_column = "", ""
            carry_lg = asset.lg
        else:
            asset.lg = carry_lg
        header_kind = mapping.get("facility_header_kind") or ("" if "facility" not in mapping else facility_type_for("", "", sheet_name, filename))
        if asset.facility and carry_facility and same_place(asset.facility, carry_facility):
            # "ALAORMIT HC III" under the banner "AKOROMIT HC III": one facility, the
            # banner's spelling.
            asset.facility = carry_facility
        if asset.facility and (looks_like_facility(asset.facility) or ("facility" in mapping and bare_place_name(asset.facility))):
            carry_facility = asset.facility
            carry_column = header_kind if "facility" in mapping and not looks_like_facility(asset.facility) else ""
        elif asset.facility and "facility" in mapping and not is_placeholder(asset.facility):
            # The column's own value stands, whatever the tests say of it.
            carry_facility, carry_column = asset.facility, header_kind
        else:
            asset.facility = carry_facility
        if carry_column and asset.facility == carry_facility:
            asset.extras["column_facility"] = carry_column
        count = bare_integer(asset.item) if asset.item else None
        department_word = bool(asset.item) and DEPARTMENT_WORD.match(asset.item) is not None
        # "Classroom Block" with its own cost and status is a building, not the
        # department of the row above.
        department_row = department_word and not (
            asset.status or asset.cost not in (None, "") or asset.purchase not in (None, "") or (asset.tag and not blank_tag(asset.tag))
        )
        if pending is not None and (count is not None or (department_word or not asset.item) and not placeholder_only(asset)):
            department_row = department_word
            # Count-on-next-row layout: the item name sat alone on the previous row and
            # this row starts with the count (or the department), then the item's data.
            if department_row:
                asset.department = join_text(asset.department, asset.item, "; ")
            asset.item = ""
            if count is not None and count > 0:
                pending.explicit_qty = count
            merge_continuation(pending, asset)
            pending.facility_type = facility_type_for(pending.facility, pending.department, sheet_name, filename)
            assets.append(pending)
            block_last = pending
            pending = None
            continue
        if pending is not None:
            if not placeholder_only(pending):
                # A filled asset held back for a count row that never came.
                pending.facility_type = facility_type_for(pending.facility, pending.department, sheet_name, filename)
                assets.append(pending)
                block_last = pending
            # The lone item name was a section label, a template line the facility
            # never received, or a fragment of the previous item's text.
            elif block_last is not None and FRAGMENT.match(pending.item) and squash(pending.item) not in TOOLKIT_INDEX:
                block_last.description = join_text(block_last.description, pending.item)
            pending = None
        if count is not None and (
            asset.description or asset.status or asset.cost not in (None, "") or asset.purchase not in (None, "")
        ):
            # A line number in the item column of a row that carries its own status,
            # cost or date: the row is an asset named by its description, not a count.
            if not asset.description:
                continue
            if count > 0 and blank_tag(asset.tag) and asset.explicit_qty is None:
                asset.explicit_qty = count
            asset.item, asset.description = asset.description, ""
            count = None
        if (count is not None or department_row) and block_last is not None:
            if department_row:
                asset.department = join_text(asset.department, asset.item, "; ")
            asset.item = ""
            if count is not None and block_last.explicit_qty is None and count > 0:
                block_last.explicit_qty = count
            merge_continuation(block_last, asset)
            continue
        if not asset.item and block_last is not None and unit_row(asset):
            # One unit per row under the item's name: "Drip Stand" on the first row,
            # then a row per stand with its own description, tag or status.
            asset.item = block_last.extras.get("unit_item") or identity_item(block_last.item)
            asset.extras["unit_row"] = True
            asset.extras["unit_item"] = asset.item
            if not block_last.extras.get("unit_row"):
                block_last.extras["has_unit_rows"] = True
            if not asset.department:
                asset.department = block_last.department
            asset.facility_type = facility_type_for(asset.facility, asset.department, sheet_name, filename)
            assets.append(asset)
            block_last = asset
            continue
        if not asset.item and block_last is not None and (asset.description or asset.tag or asset.status or asset.remarks or asset.department):
            merge_continuation(block_last, asset)
            continue
        if not asset.item:
            continue
        if NOT_RECEIVED.match(asset.item) and placeholder_only(asset):
            continue
        if placeholder_only(asset):
            if block_last is not None and squash(f"{block_last.item} {asset.item}") in TOOLKIT_INDEX:
                # "Instrument set, ENT" / "Basic for HCIII": one item name wrapped over
                # two rows; a count row may still follow it.
                block_last.item = clean(f"{block_last.item} {asset.item}")
                if assets and assets[-1] is block_last:
                    assets.pop()
                pending = block_last
                block_last = None
                continue
            pending = asset
            continue
        asset.facility_type = facility_type_for(asset.facility, asset.department, sheet_name, filename)
        assets.append(asset)
        block_last = asset
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
                elif text in {"department", "section"}:
                    mapping["department"] = col
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
        asset.facility_type = facility_type_for(asset.facility, asset.department, sheet_name, source)
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
        asset.extras["source_cells"] = [clean(value) for value in row if isinstance(value, str) and clean(value)]
        if not asset.facility_type:
            asset.facility_type = "Seed school"
        assets.append(asset)
    return assets


def context_from_line(text: str) -> tuple[str, str] | None:
    """A line above or between asset rows that names the place: a banner, a known
    local government, or a facility name standing alone."""
    raw = clean(text)
    if not raw or len(raw) > 160 or raw.endswith(":") or is_placeholder(raw):
        return None
    if re.match(r"^[.\u2026…]{3,}", raw):
        remainder = re.sub(r"^[.\u2026…\s]+", "", raw)
        if re.fullmatch(r"(?i)(district(\s+lo+c+a+l+\s+government)?|health\s+cent(?:re|er)\s*(?:iii|3)?)", remainder.strip()):
            return None
    if re.match(r"(?i)class\s+\d", raw) or re.match(r"(?i)cost cent|source\b|vote\b", raw):
        return None
    # "Local Government: Rubirizi District | Facility: Munyonyi HC III"
    pieces = [piece for piece in re.split(r"\s*\|\s*", raw) if piece]
    if len(pieces) > 1:
        lg_text = facility_text = ""
        for piece in pieces:
            banner = parse_banner(piece)
            if banner:
                lg_text = lg_text or banner[0]
                facility_text = facility_text or banner[1]
        if lg_text or facility_text:
            return lg_text, facility_text
    banner = parse_banner(raw)
    if banner and (banner[0] or banner[1]):
        return banner
    if len(raw) <= 60 and resolve_lg(raw) is not None:
        return raw, ""
    if len(raw) <= 60 and lg_from_text(raw) is not None and not facility_kind(raw):
        return raw, ""
    if len(raw) <= 80 and looks_like_facility(raw):
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
        elif "status" in text or text == "condition" or "functionality" in text or text.startswith("functional"):
            roles.setdefault("status", index)
        elif "unit cost" in text or "unit price" in text or "cost per unit" in text:
            roles.setdefault("unit_cost", index)
        elif "total cost" in text or "total amount" in text:
            roles.setdefault("cost", index)
        elif ("cost" in text and "center" not in text and "centre" not in text and "control" not in text):
            roles.setdefault("cost", index)
        elif re.search(r"\b(supplied|delivered|call\s*off|ordered|deficit|register)\b", text):
            # What was supplied is not what was found.
            continue
        elif "qty" in text or "qtty" in text or "qnty" in text or "quantity" in text or text in {"found", "verified", "counted", "physical count", "number found"}:
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
        elif "description" in text or text in {"asset", "equipment asset", "item", "items", "item name", "name of item", "asset name"}:
            descriptions.append(index)
        elif "model" in text:
            roles.setdefault("description", index)
    if "item" not in roles and descriptions:
        roles["item"] = descriptions.pop(0)
    if descriptions and "description" not in roles:
        roles["description"] = descriptions[0]
    # The prompt's test: a description column together with condition, quantity,
    # tag, or cost. A device list with serial numbers but no item column is not one.
    useful = {"tag", "status", "cost", "explicit_qty"}
    if "item" in roles and len(useful & set(roles)) >= 1 and len(roles) >= 3:
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
    for row_number, row in enumerate(rows[header_at + 1:], header_at + 2):
        if not any(clean(value) for value in row):
            continue
        context = context_from_line(row_text(row))
        probe = take_asset(row, mapping, source, "")
        if context and not any([probe.tag, probe.status, probe.cost, probe.explicit_qty, probe.description]):
            carry_lg = context[0] or carry_lg
            carry_facility = context[1] or carry_facility
            continue
        asset = probe
        asset.source_location = f"{sheet_name} row {row_number}"
        if not asset.item or norm(asset.item) in {"description", "asset description", "equipment", "total"}:
            continue
        if placeholder_only(asset) and not asset.explicit_qty:
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


def reconciliation_sources() -> dict[str, list[tuple[str, str, str]]]:
    """Source file -> [(local government, facility, type), ...] from the
    reconciliation. Used only after the row, the banner and the folder path have
    all failed to name the place, and only when one facility of the row's kind
    is tied to the file."""
    found: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    if not RECONCILIATION.exists():
        return {}
    with RECONCILIATION.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            name = row.get("field_name") or row.get("name") or ""
            kind = row.get("type") or ""
            if not name or kind not in {"School", "Health centre"}:
                continue
            for column in ("source", "additional_sources"):
                for source in (row.get(column) or "").split(";"):
                    source = source.strip()
                    place = (row.get("lg") or "", name, kind)
                    if source and place not in found[source]:
                        found[source].append(place)
    return dict(found)


RECONCILED: dict[str, list[tuple[str, str, str]]] = {}
PLACE_NOTES: Counter = Counter()
SUPERVISOR_DECISIONS = GROUPED / "supervisor-decisions.csv"
_DISTRICT_CORRECTIONS: dict[str, LocalGovernment] | None = None


def district_corrections() -> dict[str, LocalGovernment]:
    """Facility key -> the vote the supervisor corrected it to, from the 'District
    corrected' and 'Local government corrected' decisions in supervisor-decisions.csv."""
    global _DISTRICT_CORRECTIONS
    if _DISTRICT_CORRECTIONS is None:
        found: dict[str, LocalGovernment] = {}
        if SUPERVISOR_DECISIONS.exists():
            with SUPERVISOR_DECISIONS.open(encoding="utf-8-sig", newline="") as handle:
                for row in csv.DictReader(handle):
                    if not re.search(r"(?i)\b(?:district|local government) corrected\b", row.get("decision") or ""):
                        continue
                    lg = resolve_lg(row.get("lg") or "")
                    if lg is None:
                        continue
                    for name in re.split(r"\s*;\s*", f"{row.get('ground_names') or ''};{row.get('master_names') or ''}"):
                        name = name.strip()
                        if name and facility_kind(name):
                            found[facility_key(name, facility_kind(name))] = lg
        _DISTRICT_CORRECTIONS = found
    return _DISTRICT_CORRECTIONS


def only_of_kind(places, kind: str):
    """The single place of this kind in a list of (lg, facility) or (lg, facility, kind)."""
    matches = []
    for place in places:
        facility = place[1]
        place_kind = place[2] if len(place) > 2 else facility_kind(facility)
        if kind and place_kind == kind and facility:
            matches.append(place)
    return matches[0] if len(matches) == 1 else None


def resolve_places(asset: Asset, contexts: list[tuple[str, str]], relative: str) -> None:
    """Settle the local government and facility of one row.

    Order: the row's own values, then the banner already carried into the row,
    then the folder path (every folder a byte-identical copy was filed under, matched
    to the table's facility kind), then the reconciliation file when it ties this
    source to one facility of that kind. A banner that names another facility than the
    folder of the same kind is a template line left unedited: the filing decides, and
    the count is reported on Read Me. Names are written in one spelling.
    """
    kind = asset.facility_type if asset.facility_type in {"School", "Health centre"} else ""
    banner_lg, banner_facility = strip_lg_prefix(asset.facility) if asset.facility else ("", "")
    if banner_facility and not banner_lg:
        # "KYEIHARA HC III MITOOMA": the district written after the facility.
        banner_facility, banner_lg = split_trailing_lg(banner_facility)
    column_kind = asset.extras.get("column_facility") or ""
    if not (banner_facility and not is_placeholder(banner_facility)
            and (looks_like_facility(banner_facility) or (column_kind and bare_place_name(banner_facility)))):
        banner_facility = ""
    if not kind and column_kind and banner_facility:
        kind = column_kind
    if not kind:
        kind = facility_kind(banner_facility) or facility_kind(asset.facility) if asset.facility else ""
    lg = resolve_lg(asset.lg) if asset.lg else None
    if lg is None and asset.lg:
        lg = lg_from_text(asset.lg)
    if lg is None and banner_lg:
        lg = resolve_lg(banner_lg)
    if lg is None and banner_facility:
        lg = lg_from_text(banner_facility)

    folder = only_of_kind(contexts, kind) if kind else None
    if folder is None and len(contexts) == 1:
        folder = contexts[0]
        if kind and facility_kind(folder[1]) and facility_kind(folder[1]) != kind:
            folder = None
    folder_lg = (resolve_lg(folder[0]) or lg_from_text(folder[0])) if folder and folder[0] else None
    if folder and folder_lg is None and folder[1]:
        folder_lg = lg_of_known_facility(folder[1], kind)
    folder_facility = folder[1] if folder else ""

    facility_text = banner_facility
    if folder_facility:
        if not facility_text:
            facility_text = folder_facility
        elif facility_key(facility_text, kind) != facility_key(folder_facility, kind):
            probe_lg = lg or folder_lg
            banner_display = canonical_facility(facility_text, probe_lg, kind)[0]
            folder_display = canonical_facility(folder_facility, folder_lg, kind)[0]
            if facility_key(banner_display, kind) != facility_key(folder_display, kind):
                PLACE_NOTES[f"{relative}: banner '{facility_text}' replaced by filed facility '{folder_display}'"] += 1
                facility_text = folder_facility
                lg = folder_lg or lg
    if lg is None:
        lg = folder_lg
    if lg is None and contexts:
        governments = {resolve_lg(context[0]) for context in contexts}
        governments.discard(None)
        if len(governments) == 1:
            lg = governments.pop()

    if not facility_text or lg is None:
        reconciled = only_of_kind(RECONCILED.get(relative, []), kind) if kind else None
        if reconciled is None and len(RECONCILED.get(relative, [])) == 1:
            reconciled = RECONCILED[relative][0]
        if reconciled:
            if lg is None:
                lg = resolve_lg(reconciled[0])
            if not facility_text:
                facility_text = reconciled[1]
                kind = kind or reconciled[2]
    if not kind and facility_text:
        kind = facility_kind(facility_text)
    if lg is None and facility_text and not is_placeholder(facility_text):
        # The reconciliation names the one local government of this facility.
        lg = lg_of_known_facility(facility_text, kind)
    if facility_text and not is_placeholder(facility_text) and lg is not None and not folder_facility:
        # A consolidation sheet that carries the previous block's district onto a
        # facility the reconciliation places in another local government.
        bucket = known_facilities().get(lg.key, {})
        if facility_key(facility_text, kind) not in bucket:
            # A facility the reconciliation lists, by its exact name, under one other
            # government is a district carried onto the wrong block of a consolidation
            # sheet. The vote the source states stands when only a fuzzy name match
            # points elsewhere (Kaukura is not Kakure), or when the other vote is the
            # sibling of the same name (Lira City is not folded into Lira).
            owner = lg_of_known_facility(facility_text, kind)
            if owner is not None and owner.key != lg.key and norm(owner.base) != norm(lg.base):
                PLACE_NOTES[f"{relative}: '{facility_text}' moved from {lg.display} to {owner.display}"] += 1
                lg = owner
    elif facility_text and lg is not None and folder_lg is not None and folder_lg.key != lg.key:
        # The banner wrote the district ("Apac") for a facility filed, and reconciled,
        # under the municipality ("Apac MC"): the filing names the vote.
        key = facility_key(facility_text, kind)
        if key in known_facilities().get(folder_lg.key, {}) and key not in known_facilities().get(lg.key, {}):
            PLACE_NOTES[f"{relative}: '{facility_text}' moved from {lg.display} to {folder_lg.display} (filed there)"] += 1
            lg = folder_lg
    if facility_text and not is_placeholder(facility_text) and lg is not None:
        # A supervisor's ruling on the facility's government ("Muggi HCIII is in
        # Mayuge district not kagadi district") decides over the label on the return.
        corrected = district_corrections().get(facility_key(facility_text, kind or facility_kind(facility_text)))
        if corrected is not None and corrected.key != lg.key:
            PLACE_NOTES[f"{relative}: '{facility_text}' moved from {lg.display} to {corrected.display} (supervisor decision)"] += 1
            lg = corrected
    asset.extras["facility_raw"] = facility_text
    if facility_text and not is_placeholder(facility_text):
        display, found_kind = canonical_facility(facility_text, lg, kind)
        asset.facility = display
        asset.facility_type = found_kind or kind
    else:
        asset.facility = ""
        asset.facility_type = kind
    asset.lg = lg.display if lg else ""
    asset.extras["lg_key"] = lg.key if lg else ""
    asset.extras["facility_key"] = facility_key(asset.facility, asset.facility_type) if asset.facility else ""


def mark_serial_asset_numbers(assets: list[Asset]) -> None:
    """An Asset Number column that counts 1, 2, 3 down the sheet is a line number,
    never a quantity."""
    numbers = [bare_integer(asset.asset_number) for asset in assets if asset.asset_number]
    if len(numbers) < 5:
        return
    integers = [number for number in numbers if number is not None]
    if len(integers) < 0.8 * len(numbers):
        return
    steps = sum(1 for previous, current in zip(integers, integers[1:]) if current - previous == 1)
    if steps >= 0.6 * (len(integers) - 1):
        for asset in assets:
            asset.extras["serial_asset_number"] = True


FACILITY_LEVEL_FOLDERS = ("_team-documents", "_district-documents")


def team_level(relative: str) -> bool:
    """A team, district or multi-team document names no facility in its path."""
    parts = relative.split("/")
    return relative.startswith("_multi-team/") or any(part in FACILITY_LEVEL_FOLDERS for part in parts)


_KNOWN_ANYWHERE: set[str] | None = None


def known_anywhere(key: str) -> bool:
    """A facility the reconciliation lists under any local government (a source
    that writes Jinja for a Jinja City facility still names a UgIFT facility)."""
    global _KNOWN_ANYWHERE
    if _KNOWN_ANYWHERE is None:
        _KNOWN_ANYWHERE = {facility for bucket in known_facilities().values() for facility in bucket}
    return bool(key) and key in _KNOWN_ANYWHERE


def in_scope(asset: Asset) -> bool:
    """A row of a team- or district-level register belongs to the register only when
    it names a UgIFT facility: one the reconciliation lists for that local
    government, or a seed school, Health Centre III or regional blood bank by name."""
    if not asset.facility:
        return False
    key = asset.extras.get("facility_key") or facility_key(asset.facility, asset.facility_type)
    bucket = known_facilities().get(asset.extras.get("lg_key") or "", {})
    if key in bucket or known_anywhere(key):
        return True
    if asset.extras.get("column_facility") and asset.facility_type in {"School", "Health centre"}:
        # Named under a HEALTH CENTRE or SCHOOL column of a programme verification sheet.
        return True
    raw = asset.extras.get("facility_raw") or asset.facility
    if "/_district-documents/" in asset.source_file:
        # A district-wide register lists every health centre of the district; only a
        # seed school named as such, or a reconciled facility, is the programme's.
        return bool(re.search(r"(?i)\bseed\b", raw))
    return bool(re.search(r"(?i)\bseed\b|health\s*cent(?:re|er)\s*(?:iii|111|3)\b|\bhc\s*(?:iii|111|3)\b|regional blood bank", raw))


def sheet_places(name: str) -> tuple[str, str]:
    """A sheet named "KABALE- LG" or "Kigarama Seed SS" is a banner for its rows."""
    text = clean(name)
    if re.fullmatch(r"(?i)sheet\s*\d*|table\s*\d*|master|data|register|list|summary", text):
        return "", ""
    lg = resolve_lg(text)
    if lg:
        return lg.display, ""
    banner = parse_banner(text)
    if banner:
        return banner
    if looks_like_facility(text):
        return "", text
    return "", ""


STEM_NOISE = re.compile(
    r"(?i)\b(ugift|ugft|asset|assets|verification|recording|tool|kit|toolkit|final|edited|copy|of|and|form|report|"
    r"template|field|excel|updated|register|data|team|\d+)\b|[\(\)\[\]_\-.,]+"
)


def stem_places(path: Path) -> tuple[str, str]:
    """A file named "UGIFT BULAGA_HCIII.docx" or "KIGANDO SEED.docx" names its facility."""
    text = clean(STEM_NOISE.sub(" ", path.stem))
    if not text:
        return "", ""
    banner = parse_banner(text)
    if banner and (banner[0] or banner[1]):
        return banner
    lg = lg_from_text(text)
    if looks_like_facility(text) and not re.search(r"(?i)\b(and|&)\b", text):
        return (lg.display if lg else ""), text
    return (lg.display if lg else ""), ""


def facility_from_description(asset: Asset) -> str:
    """An IFMS row may put only its facility name in Description, with no site column.

    Recover that row-level location without treating a payment mentioning a school
    as another physical asset. District scope is still checked by in_scope().
    """
    description = clean(asset.description)
    if asset.facility or not description or not looks_like_facility(description):
        return ""
    if re.search(r"\b(?:water\s*(?:works|supply|schemes?)|payments?|expenses?|insurance|services)\b", norm(asset.item)):
        return ""
    lg = resolve_lg(asset.lg) if asset.lg else None
    kind = facility_kind(description)
    key = facility_key(description, kind)
    if (lg is not None and key in known_facilities().get(lg.key, {})) or known_anywhere(key):
        return description
    # A seed school explicitly named as such is in scope even when the master
    # has no entry. Transaction prose ('payment ... for ... school') is not a name.
    if kind == "School" and re.search(r"(?i)\bseed\b", description) and not re.search(
        r"(?i)\b(?:payments?|construction|works|for|to|at|supply|services|insurance|retention|"
        r"water|extension|installation|cost|maintenance|rehabilitation)\b", description,
    ):
        return description
    return ""


def read_workbook(path: Path) -> list[Asset]:
    relative = path.relative_to(GROUPED).as_posix()
    contexts = CONTEXTS.get(path) or [context for context in [path_context(path)] if context[0]]
    weak_context: tuple[str, str] | None = None
    if not contexts:
        stem_lg, stem_facility = stem_places(path)
        if stem_facility and not re.search(
            r"(?i)\b(schools|centres|centers|hcs|dtb|team|list|register|facilities|hospitals|health|centre|center|"
            r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b",
            stem_facility,
        ):
            # "UGIFT BULAGA_HCIII.docx" names its one facility; used only when no
            # banner or column in the file names one.
            weak_context = (stem_lg, stem_facility)
    fallback_lg = contexts[0][0] if contexts and len({context[0] for context in contexts}) == 1 else ""
    assets: list[Asset] = []
    offsets: dict[str, int] = {}
    if path.suffix.lower() == ".docx":
        if not docx_has_asset_table(path):
            return []
        sheets = docx_tables(path)
        # Banner paragraphs are prepended to each table; row numbers in Source
        # location still count the table's own rows.
        for name, rows, _kind in sheets:
            offsets[name] = sum(1 for row in rows if len(row) == 1 and not isinstance(row, tuple)) if rows else 0
        sheets = [(name, rows, kind) for name, rows, kind in sheets]
    else:
        sheets = [(name, rows, "") for name, rows in sheet_rows(path)]
    template_maps = []
    for _name, rows, _kind in sheets:
        for row in rows[:40]:
            mapping = classify_header(row)
            if mapping:
                template_maps.append(mapping)
                break
    workbook_has_places = any("lg" in mapping and "facility" in mapping for mapping in template_maps)
    last_docx_places: dict[str, tuple[str, str]] = {}
    last_docx_header: dict[str, list[object]] = {}
    for name, rows, section_kind in sheets:
        if SUPPLY_SHEET.search(name):
            # A delivery note, requisition voucher or interview sheet lists what was
            # issued, not what was found.
            continue
        header_row = next((row for row in rows[:40] if classify_header(row)), None)
        mapping = classify_header(header_row) if header_row is not None else None
        if path.suffix.lower() == ".docx":
            previous_header = last_docx_header.get(section_kind)
            if header_row is None and rows and previous_header is not None and len(rows[-1]) == len(previous_header):
                # A table split across pages continues the previous table's columns.
                lead = 0
                while lead < len(rows) and len(rows[lead]) == 1:
                    lead += 1
                rows = rows[:lead] + [list(previous_header)] + rows[lead:]
                offsets[name] = offsets.get(name, 0) + 1
                mapping = classify_header(previous_header)
            elif header_row is not None:
                last_docx_header[section_kind] = header_row
        if mapping and sheet_is_duplicate_draft(name, mapping, workbook_has_places):
            continue
        sheet_lg, sheet_facility = sheet_places(name) if path.suffix.lower() != ".docx" else ("", "")
        parsed: list[Asset] = []
        if mapping:
            parsed = parse_template_sheet(name, rows, relative, path.name, sheet_lg or fallback_lg)
        if not parsed:
            parsed = parse_qty_register(name, rows, relative, sheet_lg or fallback_lg)
        if not parsed:
            parsed = parse_flexible_sheet(name, rows, relative, path.name, sheet_lg or fallback_lg)
        offset = offsets.get(name, 0)
        mark_serial_asset_numbers(parsed)
        if path.suffix.lower() == ".docx" and parsed:
            # A Word table split across pages continues the facility named before
            # the previous table of the same checklist section.
            previous = last_docx_places.get(section_kind)
            if previous and not any(asset.facility for asset in parsed):
                for asset in parsed:
                    asset.lg, asset.facility = asset.lg or previous[0], previous[1]
            places = {(asset.lg, asset.facility) for asset in parsed if asset.facility}
            if len(places) == 1:
                last_docx_places[section_kind] = places.pop()
        for asset in parsed:
            if section_kind:
                asset.facility_type = section_kind
            if not asset.facility and sheet_facility:
                asset.facility = sheet_facility
            if offset:
                asset.source_location = re.sub(
                    r"row (\d+)$", lambda found: f"row {int(found.group(1)) - offset}", asset.source_location
                )
        assets.extend(parsed)
    for asset in assets:
        if "/_district-documents/" in relative and (description_facility := facility_from_description(asset)):
            asset.facility = description_facility
            asset.facility_type = facility_kind(description_facility)
            asset.extras["description_facility"] = True
        if not asset.facility_type:
            asset.facility_type = facility_type_for(asset.facility, asset.department, "", path.name)
        if weak_context and not (asset.facility and looks_like_facility(asset.facility)):
            asset.facility = weak_context[1]
            asset.lg = asset.lg or weak_context[0]
    # A workbook whose banners name two or more facilities of one kind is a team's
    # consolidation filed under one facility folder: its banners decide, not the folder.
    named: dict[str, set[str]] = defaultdict(set)
    for asset in assets:
        if asset.facility and not is_placeholder(asset.facility) and looks_like_facility(asset.facility):
            kind = asset.facility_type if asset.facility_type in {"School", "Health centre"} else facility_kind(asset.facility)
            named[kind or ""].add(facility_key(strip_lg_prefix(asset.facility)[1] or asset.facility, kind or ""))
    for asset in assets:
        kind = asset.facility_type if asset.facility_type in {"School", "Health centre"} else facility_kind(asset.facility)
        many = bool(asset.facility) and len(named.get(kind or "", ())) >= 2
        resolve_places(asset, [] if many else contexts, relative)
        if not asset.facility_type and asset.facility:
            # The folder named the facility only now (a blood bank, a hospital).
            asset.facility_type = facility_type_for(asset.facility, asset.department, "", path.name)
    if team_level(relative) and not any(context[1] for context in contexts) and weak_context is None:
        # A district-wide or team-wide register: rows that name no UgIFT facility
        # (district offices, sub-counties, primary schools) are outside this register.
        kept = [asset for asset in assets if in_scope(asset)]
        if len(kept) < len(assets):
            SCOPE_NOTES[relative] = (len(assets) - len(kept), len(assets))
        assets = kept
    return assets


SCOPE_NOTES: dict[str, tuple[int, int]] = {}
SUPPLY_SHEET = re.compile(r"(?i)voucher|delivery\s*note|requisition|invoice|receipt|interview|distribution\s*list|dispatch|\bdeployed\b")


def bare_count(value: object) -> int | None:
    """A positive whole count in a field whose context permits a quantity."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)) and float(value).is_integer():
        count = int(value)
    else:
        raw = clean(value).strip("()[]").replace(",", "")
        count = int(raw.split(".")[0]) if re.fullmatch(r"\+?\d+(?:\.0+)?", raw) else as_count(raw)
    return count if count is not None and count > 0 else None


def quantity_cell(value: object) -> int | None:
    """A dedicated quantity cell may contain '120', '120 pcs' or number words."""
    if count := bare_count(value):
        return count
    found = phrase_count(value)
    return found[0] if found else embedded_quantity(clean(value))


def trailing_quantity(item: str) -> tuple[str, int] | None:
    """'Examination Couch 2' and 'Desks 125' state the count after the item name.

    A model suffix such as LaserJet 1320 or Laptop 840 is not a count.
    """
    match = re.fullmatch(rf"(.+?)\s+({COUNT_WORD})", clean(item), re.I)
    if not match:
        return None
    count = as_count(match.group(2))
    name = clean(match.group(1)).rstrip(" ,.;")
    if not name or not count or NUMBER_CONTEXT.search(name):
        return None
    last = name.split()[-1]
    if MODEL_TAIL.match(last) or MODEL_FAMILY.search(name):
        return None
    if last.casefold().strip(".,") in PORT_WORDS and count in {4, 8, 12, 16, 24, 48}:
        # "Network switch 24", "Patch panel 24": the port count of one device.
        return None
    return name, count


PORT_WORDS = {"switch", "switches", "panel", "panels", "hub", "hubs", "router", "routers"}


def phrase_count(text: object) -> tuple[int, str] | None:
    """'2 microscopes, white' states a count in front of the description. A size
    or specification ('15 inch', '3 stance', '24 port') is not a count."""
    raw = clean(text)
    match = LEADING_COUNT.match(raw)
    if not match:
        return None
    count = as_count(match.group(1))
    if not count or NUMBER_CONTEXT.match(clean(match.group(2))):
        return None
    return count, clean(match.group(2))


def embedded_quantity(text: str) -> int | None:
    """An explicit count phrase, safe to inspect in any source column."""
    raw = clean(text)
    if not raw or bare_count(raw):
        return None
    patterns = (
        rf"(?i)\b(?:qty|quantity|no\.?\s*of\s+(?:assets|items|pieces|units)|number\s+of\s+(?:assets|items|pieces|units))\s*[:=]?\s*{COUNT_START}({COUNT_WORD}){COUNT_END}",
        rf"(?i){COUNT_START}({COUNT_WORD})(?![\d.,])\s*(?:pcs|pieces|units|assets?|items?)\b",
        rf"(?i){COUNT_START}({COUNT_WORD}){COUNT_END}\s*(?:desks?|chairs?|bench(?:es)?|stools?|tables?|beds?|shel(?:f|ves)|machines?|microscopes?|computers?|laptops?)\b",
        # "They are 13 metallic grey steel", "They received 20 beds": a count in prose.
        rf"(?i)\b(?:they\s+are|there\s+are|received|recieved|delivered|has|have|got)\s+{COUNT_START}({COUNT_WORD}){COUNT_END}\s+[a-z]",
    )
    for index, pattern in enumerate(patterns):
        for match in re.finditer(pattern, raw):
            if index == 2:
                prefix = re.split(r"[;\n]", raw[:match.start()])[-1]
                if NUMBER_CONTEXT.search(prefix) or MODEL_FAMILY.search(prefix) or re.search(r"(?i)\b(?:gen|generation|series)\b", prefix):
                    continue
            if (count := as_count(match.group(1))) and count > 0:
                return count
    return None


def per_item_amount(value: object, total: int) -> object:
    """Split a line total across the rows created from that line."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or total <= 1:
        return value
    share = value / total
    # Store the full share, so splitting 100 across three units conserves 100.
    # Display formatting may round; the saved accounting values must not lose cents.
    return int(share) if share.is_integer() else share


def furniture_quantity(item: str) -> tuple[str, int] | None:
    match = re.fullmatch(
        r"(?i)(desks?|chairs?|stools?|tables?|shel(?:f|ves)|bench(?:es)?|beds?|cupboards?)\s+(\d+)",
        clean(item),
    )
    if not match:
        return None
    count = int(match.group(2))
    if count > 0:
        return match.group(1), count
    return None


def parenthetical_quantity(item: str) -> tuple[str, int] | None:
    match = re.fullmatch(rf"(.+?)\s*[\(\[]\s*({COUNT_WORD})\s*[\)\]]", clean(item), re.I)
    if not match:
        return None
    count = as_count(match.group(2))
    name = clean(match.group(1))
    if count and not NUMBER_CONTEXT.search(name) and not MODEL_FAMILY.search(name):
        if name.split()[-1].casefold().strip(".,") in PORT_WORDS and count in {4, 8, 12, 16, 24, 48}:
            return None
        return name, count
    return None


QUANTITY_IDENTIFIER_CONTEXT = re.compile(
    r"(?i)\b(?:s\s*[/.-]?\s*n|lot|cat\.?\s*no|number|type|"
    r"ushs?|ugshs?|btu|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)\b"
)
QUANTITY_MODEL_CONTEXT = re.compile(
    r"(?i)\b(?:office\s+jet|dvr|catalyst|ram|rom|memory|processor|core\s+i[3579]|"
    r"intel|ryzen|celeron|pentium|xeon|i[3579]|ssd|hdd|frequency|resolution|mt[\s-]*400)\b"
)
QUANTITY_MEASURE_CONTEXT = re.compile(
    r"(?i)\b(?:swg\s*\d+|\d+\s*gauge|\d+\s*n?m[3³]\s*/\s*(?:h|hr|hour))\b"
)
QUANTITY_COMPONENT = re.compile(
    r"(?i)^(?:(?:spare|pvc|bed|silver|white|black|blue|red|grey|gray|stainless(?:\s+steel)?|metallic|big|large|small)\s+)*"
    r"(?:bedrooms?|(?:sitting|dining)\s+rooms?|sections?|jars?|wheels?|wheelers?|handles?|shel(?:f|ves)|stands?|legs?|locks?|folds?|sided|burners?|"
    r"bottles?|tub(?:e|es|ing)|rooms?|roomed|doors?|drawers?|ports?|seaters?|gauge|n?m[3³]\s*/\s*(?:h|hr|hour)|va|cc|btu)\b"
)


def quantity_inventory_text(text: str) -> str:
    """Read package counts without treating the package's contents as assets.

    Only the inference text changes; original item/description wording remains
    on the source record. A box, pack or set can itself have a stated quantity.
    """
    raw = clean(text)
    package = r"(?:packs?|box(?:es)?|sets?|kits?)"
    contents = rf"{COUNT_START}{COUNT_WORD}{COUNT_END}(?:\s*(?:pcs|pieces|items|units)\b)?"
    raw = re.sub(rf"(?i)\b({package})\s+of\s+{contents}", r"\1", raw)
    raw = re.sub(rf"(?i)\b({package})\s*[\[(]\s*{contents}\s*[\])]", r"\1", raw)
    raw = re.sub(rf"(?i)\b(?:containing|contains?|comprising)\s+{contents}", "", raw)
    return clean(raw)


def quantity_specification(text: str) -> bool:
    """Reject weak counts in identifier/specification prose after raw parsing."""
    raw = clean(text)
    return bool(
        NUMBER_CONTEXT.search(raw) or QUANTITY_IDENTIFIER_CONTEXT.search(raw)
        or MODEL_FAMILY.search(raw) or QUANTITY_MODEL_CONTEXT.search(raw) or QUANTITY_MEASURE_CONTEXT.search(raw)
        or re.search(r"(?i)\b(?:ups\s*\d+|ce\s*\d+|\d+\s*(?:va|cc))\b", raw)
        or re.search(r"\b(?=\S*[A-Za-z])(?=\S*\d)[A-Za-z0-9/-]+\s+\d+\s*$", raw)
    )


def component_quantity(tail: str, item: str) -> bool:
    match = QUANTITY_COMPONENT.match(clean(tail))
    if not match:
        return False
    component = match.group().casefold()
    # Shelves/bottles can themselves be the registered asset, but are parts of
    # a cupboard/suction machine. Ratings and room counts are never unit counts.
    if re.search(r"\b(?:va|cc|btu|gauge|n?m[3³]|rooms?|bedrooms?|sections?|roomed|ports?|seaters?|sided|folds?|burners?|wheelers?)\b", component):
        return True
    component_words = {word.rstrip("s") for word in re.findall(r"[a-z]+", component)}
    item_words = {word.rstrip("s") for word in re.findall(r"[a-z]+", item.casefold())}
    return not bool(component_words & item_words)


def asset_quantity_phrase(text: str, item: str = "") -> int | None:
    """Explicit units/count phrases, excluding parts of the named asset."""
    raw = quantity_inventory_text(text)
    patterns = (
        rf"(?i)\b(?:qty|quantity|no\.?\s*of\s+(?:assets|items|pieces|units)|number\s+of\s+(?:assets|items|pieces|units))\s*[:=]?\s*{COUNT_START}({COUNT_WORD}){COUNT_END}",
        rf"(?i){COUNT_START}({COUNT_WORD})(?![\d.,])\s*(?:pcs|pieces|units|assets?|items?)\b",
        rf"(?i){COUNT_START}({COUNT_WORD}){COUNT_END}\s*(?:desks?|chairs?|bench(?:es)?|stools?|tables?|beds?|shel(?:f|ves)|machines?|microscopes?|computers?|laptops?)\b",
        rf"(?i)\b(?:they\s+are|there\s+are|received|recieved|delivered)\s+{COUNT_START}({COUNT_WORD}){COUNT_END}\s+[a-z]",
        rf"(?i){COUNT_START}({COUNT_WORD}){COUNT_END}\s+(?:packs?|box(?:es)?|sets?|kits?)\b",
    )
    found = []
    for index, pattern in enumerate(patterns):
        for match in re.finditer(pattern, raw):
            prefix = re.split(r"[;\n]", raw[:match.start()])[-1]
            if index and re.search(r"(?i)\b(?:has|have|with|contain\w*|compris\w*|capacity)\s*[:=]?\s*$", prefix):
                continue
            if index == 4 and re.search(r"(?i)\d\s*[x×]\s*$", prefix):
                # A cover-slip dimension (22×22 pack) is not 22 packs.
                continue
            if index == 1 and component_quantity(raw[match.end():], item):
                continue
            if index == 2:
                if quantity_specification(prefix) or re.search(r"(?i)\b(?:gen|generation|series)\b", prefix):
                    continue
                noun_tail = raw[match.end(1):].lstrip()
                if component_quantity(noun_tail, item) or re.match(r"(?i)bed\s+rooms?\b", noun_tail):
                    continue
            if (count := as_count(match.group(1))) and count > 0:
                found.append(count)
    return max(found) if found else None


def condition_groups(status: str, remarks: str, *additional: str, asset_item: str = "") -> list[tuple[int, str | None]] | None:
    """Add subsets within a statement, reconcile totals across separate cells."""
    statements = list(dict.fromkeys(quantity_inventory_text(value) for value in (status, remarks, *additional) if clean(value)))
    alternatives = []
    for text in statements:
        def subset_of_total(match: re.Match) -> str:
            total = as_count(match.group(2))
            if total:
                alternatives.append([(total, None)])
            return match.group(1)
        text = re.sub(rf"(?i){COUNT_START}({COUNT_WORD}){COUNT_END}\s+out\s+of\s+({COUNT_WORD}){COUNT_END}", subset_of_total, text)
        matches = list(re.finditer(
            rf"(?i){COUNT_START}({COUNT_WORD}){COUNT_END}\s+(?:are\s+|were\s+|is\s+|was\s+)?(?:still\s+)?"
            r"(verified\s+and\s+in\s+good\s+use|verified\s+as\s+good|good|(?:not\s+)?in\s+(?:active\s+)?use|"
            r"functional|functioning|working|usable|kept\s+in\s+(?:the\s+)?store|in\s+(?:the\s+)?store|boxed|"
            r"broken|damaged|faulty|spoilt|stolen|missing|lost|not\s+functional|non[- ]functional|not\s+working)\b",
            text,
        ))
        positioned = [(match.start(), match.end(), as_count(match.group(1)), match.group(2).capitalize()) for match in matches]
        # Departmental subsets are also written "In use (04)" / "In store 4".
        reverse_positions = []
        for match in re.finditer(
            rf"(?i)\b((?:not\s+)?in\s+(?:active\s+)?use|in\s+(?:the\s+)?store|"
            rf"not\s+functional|functional|not\s+working|working|damaged|broken|stolen|missing)"
            rf"\s*[:=-]?\s*\(\s*({COUNT_WORD}){COUNT_END}\s*\)?", text,
        ):
            reverse_positions.append((match.start(), match.end(), as_count(match.group(2)), match.group(1).capitalize()))
        # An unclosed parenthesis is common in source cells: "In use (04 In
        # store (04)" must not also parse the first 04 as "04 In store".
        positioned = [value for value in positioned if not any(start <= value[0] < end for start, end, _, _ in reverse_positions)]
        positioned.extend(reverse_positions)
        positioned.sort(key=lambda value: value[0])
        groups = [(count, label) for _, _, count, label in positioned]
        groups = [(count, phrase) for count, phrase in groups if count]
        if groups:
            if len(groups) > 1 and re.search(r"(?i)\b(?:but|except|including|of\s+which)\b", text[positioned[0][1]:positioned[1][0]]):
                # "120 verified, of which 4 broken" states 120 total. The first
                # condition applies to the remaining 116, not another 120 units.
                remaining = groups[0][0] - sum(count for count, _ in groups[1:])
                if remaining >= 0:
                    groups = ([(remaining, groups[0][1])] if remaining else []) + groups[1:]
            alternatives.append(groups)
            continue
        verified = [as_count(value) for value in re.findall(rf"(?i)(?<!not ){COUNT_START}({COUNT_WORD}){COUNT_END}\s+verified\b", text)]
        received = [as_count(value) for value in re.findall(rf"(?i){COUNT_START}({COUNT_WORD}){COUNT_END}\s+(?:were\s+|was\s+)?(?:received|recieved|supplied)\b", text)]
        received += [as_count(value) for value in re.findall(rf"(?i)\b(?:received|recieved|supplied|counted)\s+{COUNT_START}({COUNT_WORD}){COUNT_END}", text)]
        received += [as_count(value) for value in re.findall(rf"(?i)\ball the\s+{COUNT_START}({COUNT_WORD}){COUNT_END}", text)]
        if verified:
            alternatives.append([(max(verified), None)])
        elif received:
            alternatives.append([(max(received), None)])
        elif count := asset_quantity_phrase(text, asset_item):
            alternatives.append([(count, None)])
    if not alternatives:
        return None
    # Different cells often paraphrase the same group: "2 functional" and "all
    # 2 in use" are two statements of two units. Distinct conditions (116 good,
    # 4 damaged) remain separate subsets even when stated in different columns.
    subsets: dict[str, tuple[int, str]] = {}
    for groups in alternatives:
        statement_counts: dict[str, tuple[int, str]] = {}
        for count, label in groups:
            if label is None:
                continue
            category = norm(label)
            if re.search(r"broken|damaged|faulty|spoilt|not functional|non functional|not working", category):
                category = "unserviceable"
            elif re.search(r"store|boxed", category):
                category = "stored"
            elif not re.search(r"stolen|missing|lost|not in use", category):
                category = "operating"
            previous = statement_counts.get(category, (0, label))
            statement_counts[category] = (previous[0] + count, previous[1])
        for category, group in statement_counts.items():
            if category not in subsets or group[0] > subsets[category][0]:
                subsets[category] = group
    if subsets:
        alternatives.insert(0, list(subsets.values()))
    return max(alternatives, key=lambda groups: sum(count for count, _ in groups))


MEASURE_WORD = (
    r"(?:seater|seaters|stances?|stanza|ports?|inch(?:es)?|in|phases?|drawers?|months?|mths?|years?|yrs?|"
    r"lit(?:re|er)s?|ltrs?|l|ml|kgs?|g|gm|kva|kw|hp|volts?|v|watts?|w|gb|tb|mm|cm|m|x|way|tiers?|doors?|steps?|pins?|"
    r"ohms?|amps?|a|pieces?\s+set|piece\s+set|in\s+1|blocks?|classrooms?|rooms?|labs?|bed\s+capacity|capacity)"
)
LEADING_COUNT = re.compile(rf"(?i)^({COUNT_WORD})\s+(?!{MEASURE_WORD}\b)([A-Za-z].+)$")


def stated_count(asset: Asset) -> tuple[str, list[tuple[int, str | None]]] | None:
    """Read all count evidence once; repeated totals do not add extra units."""
    candidates: list[tuple[int, str]] = []
    name = asset.item
    item_text = quantity_inventory_text(asset.item)
    description_text = quantity_inventory_text(asset.description)
    if asset.explicit_qty:
        candidates.append((asset.explicit_qty, "quantity column"))
    if asset.extras.get("recorded_group_total"):
        provenance = "; ".join(asset.extras.get("source_group_locations", [asset.source_location]))
        candidates.append((asset.extras["recorded_group_total"], f"recorded group total; {provenance}; {asset.extras.get('quantity_layout_evidence', '')}"))
    item_count = None if QUANTITY_MODEL_CONTEXT.search(item_text) or QUANTITY_MEASURE_CONTEXT.search(item_text) else parenthetical_quantity(item_text) or trailing_quantity(item_text)
    if item_count:
        name, count = item_count
        candidates.append((count, "item"))
    elif found := phrase_count(item_text):
        if not component_quantity(found[1], asset.item):
            name = found[1]
            candidates.append((found[0], "item"))
    description_is_model_label = (
        asset.source_file.endswith("/Sikuda-HC-III/Asset-Verification-Toolkit.docx")
        and asset.source_location == "Table 6 row 73"
        and re.search(r"(?i)78\s+green.*79\s+maroon", asset.description)
        and re.search(r"(?i)all\s+three\s+are\s+functional", asset.remarks)
    )
    if description_is_model_label:
        candidates.append((3, "source row states one green and two maroon stoves, all three functional; 78/79 describe models"))
    elif count := bare_count(description_text):
        if not (re.match(r"^0\d", asset.description) and not blank_tag(asset.tag)):
            candidates.append((count, "description"))
    elif found := phrase_count(description_text):
        if not component_quantity(found[1], asset.item) and not re.match(r"(?=\S*[A-Za-z])(?=\S*\d)\S+", found[1]):
            candidates.append((found[0], "description"))
    elif not quantity_specification(description_text):
        if found := parenthetical_quantity(description_text) or trailing_quantity(description_text):
            candidates.append((found[1], "description"))
    if (asset.source_file == "team-15/Bukwo/Mutushet-HC-III/Asset-Verification-Toolkit.docx"
            and asset.source_location == "Table 6 row 103"
            and bare_count(asset.asset_number) == 3
            and re.search(r"(?i)one\s+set\s+containing\s+11\s+items", asset.description)):
        # Original table uses Asset Number as quantity (adjacent sets 2/4/3).
        # The description states one set's composition; retain that ambiguity.
        candidates.append((3, "source count conflict: Asset Number records 3 hospital hollow-ware sets; description says one set containing 11 items; preserve 3 sets and the original descriptive wording"))
    # Raw cells retain facts from arbitrary/unknown columns and original strings
    # converted to dates or monetary values by the mapped fields.
    non_quantity_dates = {clean(value) for value in (asset.purchase, asset.service)
                          if clean(value) and not asset_quantity_phrase(clean(value), asset.item)}
    source_texts = [value for value in asset.extras.get("source_cells", ()) if clean(value) not in non_quantity_dates]
    texts = list(dict.fromkeys([
        asset.item, asset.description, asset.status, asset.remarks, asset.department,
        asset.asset_number, asset.tag, *source_texts,
    ]))
    conditions = condition_groups(asset.status, asset.remarks, *texts, asset_item=asset.item)
    for text in texts:
        if count := asset_quantity_phrase(text, asset.item):
            candidates.append((count, text))
    if conditions:
        candidates.append((sum(count for count, _ in conditions), "condition subsets"))
    # A bare number under "Asset Number" is ambiguous. Use it as a count only
    # when independent item/description/quantity evidence is absent; a serial
    # cannot outvote a stated count of 1, 3 or 120.
    from_asset_number = blank_tag(asset.tag) and not asset.extras.get("serial_asset_number") and not asset.extras.get("qty_column")
    if not candidates and from_asset_number and not quantity_specification(asset.asset_number):
        if asset.extras.get("alone") and (count := bare_count(asset.asset_number)):
            candidates.append((count, "asset number"))
        elif found := phrase_count(asset.asset_number):
            if not component_quantity(found[1], asset.item) and not re.match(r"(?=\S*[A-Za-z])(?=\S*\d)\S+", found[1]):
                candidates.append((found[0], "asset number"))
    if not candidates:
        return None
    total = max(count for count, _ in candidates)
    if asset.extras.get("recorded_group_total") and total != asset.extras["recorded_group_total"]:
        candidates.append((total, "source count conflict: distinct stated condition subsets exceed the recorded group total; preserve the physical subsets"))
    elif conditions and total == sum(count for count, _ in conditions):
        smaller_totals = sorted({count for count, label in candidates if label in {"item", "description", "quantity column"} and count < total})
        if smaller_totals:
            candidates.append((total, f"source count conflict: explicit condition subsets total {total}, against other recorded counts {smaller_totals}; preserve the physical subsets"))
    asset.extras["quantity_evidence"] = candidates
    if conditions and sum(count for count, _ in conditions) == total:
        return name, conditions
    return name, [(total, None)]


def decide_groups(asset: Asset, alone: bool, repeats: int = 1, per_unit_block: bool = False, same_quantity: bool = True) -> tuple[str, list[tuple[int, str | None]]]:
    """Choose how many asset rows a source line represents.

    Only source layout or distinct unit identifiers can prove a line is already
    one unit. Repetition and repeated counts are never grounds for discarding a
    grouped line's stated quantity. Legacy keyword arguments remain accepted.
    """
    asset.extras["alone"] = alone
    if any(asset.extras.get(key) for key in ("has_unit_rows", "unit_row", "proven_unit_row")):
        # The units of this line are listed on the rows below it, one each.
        return identity_item(asset.item), [(1, None)]
    found = stated_count(asset)
    if not found:
        return asset.item, [(1, None)]
    name, groups = found
    return name, groups


def presence_key(asset: Asset) -> tuple[str, str, str, str]:
    """One return's rows for one item at one facility."""
    return (
        asset.source_file,
        asset.extras.get("lg_key") or norm(asset.lg),
        asset.extras.get("facility_key") or norm(asset.facility),
        norm(identity_item(asset.item)),
    )


def exact_key(asset: Asset) -> tuple[str, ...]:
    """The same line typed again: same item text, description, department and tag
    (or no tag). The same count in two departments is two stated counts."""
    return presence_key(asset)[:3] + (
        norm(asset.item), norm(asset.description), norm(asset.department), norm(asset.tag) if not blank_tag(asset.tag) else "",
    )


def exclude_reviewed_zero_rows(parsed: dict[str, list[Asset]]) -> list[dict[str, object]]:
    """Honor six reviewed zero inventories, retaining the source contradictions."""
    reviewed = {
        "team-14/Sironko/Buyobo-HC-III/Asset-Verification-Toolkit.docx": {
            "Table 6 row 202", "Table 6 row 229", "Table 6 row 233",
        },
        "team-14/Bududa/Nakatsi-Seed-Secondary-School/Asset-Verification-Toolkit.docx": {
            "Table 11 row 23", "Table 11 row 26", "Table 11 row 28",
        },
    }
    audit: list[dict[str, object]] = []
    for source, locations in reviewed.items():
        assets = parsed.get(source, [])
        remove = set()
        for asset in assets:
            if asset.source_location not in locations or not re.search(r"\(\s*0+\s*\)\s*$", asset.item):
                continue
            reason = "The original source explicitly records zero and states 'Recorded as none held'; no physical asset is recorded."
            if "Nakatsi-Seed" in source:
                reason = (
                    "Source count conflict: the item explicitly records zero while the generic condition says "
                    "available and serialised. Original cells and related returns provide no tag, serial, "
                    "unit identity or positive quantity. Retained zero; the separate Human ear model (1) stays."
                )
            audit.append({"source_file": source, "source_location": asset.source_location,
                          "item": asset.item, "quantity": 0, "status": "zero_count_omitted", "reason": reason})
            remove.add(id(asset))
        assets[:] = [asset for asset in assets if id(asset) not in remove]
    return audit


def propagate_count_fragment_repairs(
    parsed: dict[str, list[Asset]], corrections: list[tuple[Asset, str, str, str]],
) -> list[dict[str, object]]:
    """Apply source-proven fragment fixes to matching statements in other returns.

    No rows are added or removed. The independently recovered original group
    already supplies its assets; this only prevents a malformed mirror anchor
    from surviving reconciliation as a second, miscounted asset group.
    """
    def identity(asset: Asset) -> tuple[str, ...]:
        return (
            asset.extras.get("lg_key") or norm(asset.lg),
            asset.extras.get("facility_key") or norm(asset.facility),
            norm(asset.item), norm(asset.department), norm(asset.status),
            "" if blank_tag(asset.tag) else norm(asset.tag),
        )

    by_identity: dict[tuple[str, ...], list[Asset]] = defaultdict(list)
    for assets in parsed.values():
        for asset in assets:
            by_identity[identity(asset)].append(asset)
    audit: list[dict[str, object]] = []
    for primary, old_description, new_description, fragment in corrections:
        for mirror in by_identity[identity(primary)]:
            if mirror.source_file == primary.source_file or norm(mirror.description) != norm(old_description):
                continue
            source_cells = mirror.extras.get("source_cells")
            if not source_cells or any(norm(fragment) in norm(value) for value in source_cells):
                # If the raw row itself contains the item list, it is a genuine
                # mixed source statement and needs its own layout review.
                continue
            original = mirror.description
            mirror.description = new_description
            proof = (
                f"Removed parser-appended fragment '{fragment}' from this matching return: "
                f"the raw source cells do not contain it, and {primary.source_file} "
                f"({primary.source_location}) supplies the independently verified anchor and separate asset row."
            )
            mirror.extras.setdefault("mirrored_fragment_repairs", []).append({
                "old_description": original, "new_description": new_description,
                "fragment": fragment, "primary_source": primary.source_file,
                "primary_location": primary.source_location,
            })
            mirror.extras["quantity_layout_evidence"] = join_text(
                mirror.extras.get("quantity_layout_evidence", ""), proof
            )
            audit.append({
                "source_file": mirror.source_file, "source_location": mirror.source_location,
                "item": mirror.item, "quantity": represented_count(mirror),
                "status": "mirror_fragment_repaired", "reason": proof,
            })
    return audit


def recover_standalone_count_rows(parsed: dict[str, list[Asset]]) -> list[dict[str, object]]:
    """Recover explicit named/count rows mistaken for empty toolkit placeholders.

    Read only the XML table grid, without loading a DOCX's embedded media. A
    table must have one resolved facility among its retained rows. Existing
    source rows keep their recorded facts; only an exact appended item fragment
    belonging to a recovered, separate source row is removed.
    """
    audit: list[dict[str, object]] = []
    corrections: list[tuple[Asset, str, str, str]] = []
    counted_name = re.compile(r"(?i)\((\d[\d,]*)\)\s*$")
    reviewed_sources = 0
    for source, assets in parsed.items():
        if not source.lower().endswith(".docx") or not assets:
            continue
        reviewed_sources += 1
        if reviewed_sources % 50 == 0:
            print(f"Source count-layout review: {reviewed_sources} DOCX files", flush=True)
        locations = {asset.source_location: asset for asset in assets}
        with zipfile.ZipFile(GROUPED / source) as archive:
            document = ElementTree.fromstring(archive.read("word/document.xml"))
        body = document.find(f"{W_NS}body")
        if body is None:
            continue
        recovered: list[Asset] = []
        for table_number, table in enumerate(body.findall(f"{W_NS}tbl"), 1):
            table_name = f"Table {table_number}"
            rows = docx_grid_rows(table)
            mapping = next((found for row in rows[:40] if (found := classify_header(row))), None)
            if not mapping:
                continue
            # read_workbook subtracts all one-cell rows, including any in the
            # table itself, from its prefixed banner/table numbering.
            offset = sum(len(row) == 1 for row in rows)
            anchors = [asset for asset in assets if asset.source_location.startswith(f"{table_name} row ")]
            places = {(asset.lg, asset.facility, asset.facility_type) for asset in anchors}
            for index, values in enumerate(rows, 1):
                location = f"{table_name} row {index - offset}"
                if location in locations:
                    continue
                filled = [(column, clean(value)) for column, value in enumerate(values)
                          if clean(value) and not is_placeholder(clean(value))
                          and not re.fullmatch(r"[\-–—.…_/ ]+", clean(value))]
                if len(filled) != 1 or filled[0][0] != mapping.get("item"):
                    continue
                item = filled[0][1]
                if (source == "team-05/Lira City/Anyomorem-HC-III/Anyomorem HC III_ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx"
                        and location == "Table 6 row 2" and norm(item) == "gas 01"):
                    # The original page break splits "Stove," (Table 5 row 17)
                    # from "Gas 01"; the retained stove already records one unit.
                    continue
                previous = [asset for asset in anchors
                            if (row_match := re.search(r" row (\d+)$", asset.source_location))
                            and int(row_match.group(1)) < index - offset]
                previous.sort(key=lambda asset: int(asset.source_location.rsplit(" row ", 1)[1]), reverse=True)
                if re.fullmatch(r"(?i)\s*\d+\s*(?:sets?|units?|pieces?|pcs|items?)\s*", item):
                    continue  # A count/unit label does not independently name an asset.
                receipt_words = {"received", "recieved", "receieved", "receuvef", "eeceived"}
                words = set(re.findall(r"[a-z]+", item.casefold()))
                if words & receipt_words:
                    named_words = words - receipt_words - {"was", "were", "they", "are", "all"} - set(WORD_COUNTS)
                    parent_words = set(re.findall(r"[a-z]+", previous[0].item.casefold())) if previous else set()
                    if not named_words or named_words <= parent_words:
                        continue  # Receipt evidence belongs to the named parent row.
                if (source == "team-20/Buhweju/Kiyanja-HC-III/KIYANJA HC 3.docx"
                        and location == "Table 11 row 25" and norm(item) == "1 administ"):
                    continue  # One administrative building is part of the recorded eight.
                department_label = DEPARTMENT_WORD.fullmatch(item) and not re.search(
                    r"(?i)\b(?:blocks?|buildings?|houses?|halls?|library|kitchen)\b", item
                )
                status_label = re.fullmatch(
                    r"(?i)(?:all\s+)?(?:not\s+in\s+use|in\s+use|functional|faulty|broken|damaged|good(?:\s+condition)?)",
                    clean(re.sub(r"[\d(),.\-]+", " ", item)),
                )
                if not re.search(r"[A-Za-z]", item) or department_label or status_label or NOT_RECEIVED.match(item):
                    continue
                match = counted_name.search(item)
                # Use the same guarded count grammar as filled source rows for
                # prefixes, suffixes, compact units and written-out quantities.
                # A plain terminal parenthesized count also covers models that
                # are themselves assets (for example a human anatomy model).
                if MODEL_FAMILY.search(item):
                    continue
                raw = take_asset(values, mapping, source, location)
                component_set = bool(re.search(
                    r"(?i)\bset\s+of\s+\d+\s*$|\b(?:kit|set)\b.*\(\s*\d+\s+pieces?\s*\)\s*$", item
                ))
                if not match and not component_set and quantity_specification(item):
                    continue
                count = as_count(match.group(1)) if match else None
                if component_set:
                    count = 1
                elif count is None:
                    stated = stated_count(raw)
                    count = sum(quantity for quantity, _ in stated[1]) if stated else None
                if count is None or count <= 0:
                    continue
                entry = {"source_file": source, "source_location": location, "item": raw.item, "quantity": count}
                if len(places) != 1:
                    audit.append({**entry, "status": "skipped", "reason": "No unambiguous resolved facility in the same table"})
                    continue
                anchor = anchors[0]
                raw.lg, raw.facility, raw.facility_type = next(iter(places))
                raw.explicit_qty = count
                raw.extras.update({key: anchor.extras[key] for key in ("lg_key", "facility_key", "central") if key in anchor.extras})
                raw.extras["recorded_group_total"] = count
                raw.extras["quantity_layout_evidence"] = "A separate original table row contains this asset name and its explicit quantity."
                if component_set:
                    raw.extras["proven_unit_row"] = True
                    raw.extras["quantity_layout_evidence"] = (
                        f"The independently named source asset '{item}' is one kit/set; its number describes "
                        "the contents, not multiple kits or sets. Original wording is retained in the description."
                    )
                    raw.description = item
                raw.extras["source_group_locations"] = [location]
                raw.extras["source_layout_recovered"] = True
                # Preserve all original amounts/dates on the previous row and
                # remove only text which the parser appended from this exact row.
                for prior in previous:
                    if raw.item in prior.description:
                        original_index = int(prior.source_location.rsplit(" row ", 1)[1]) + offset - 1
                        original_description = clean(cell(rows[original_index], mapping, "description"))
                        if raw.item not in original_description:
                            old_description = prior.description
                            prior.description = clean(prior.description.replace(raw.item, "", 1))
                            prior.extras.setdefault("separated_source_rows", []).append(location)
                            corrections.append((prior, old_description, prior.description, raw.item))
                        break
                if component_set:
                    raw.item = clean(re.sub(r"(?i)\s+of\s+\d+\s*$|\s*\(\s*\d+\s+pieces?\s*\)\s*$", "", item))
                recovered.append(raw)
                locations[location] = raw
                audit.append({**entry, "status": "recovered", "reason": raw.extras["quantity_layout_evidence"]})
        if recovered:
            assets.extend(recovered)
            # Keep physical table order so layout and continuation proof remains
            # deterministic and generated quantity audit blocks are easy to trace.
            def source_order(asset: Asset) -> tuple[int, int]:
                match = re.fullmatch(r"Table (\d+) row (-?\d+)", asset.source_location)
                return tuple(map(int, match.groups())) if match else (10**9, 10**9)
            assets.sort(key=source_order)
    audit.extend(propagate_count_fragment_repairs(parsed, corrections))
    return audit


def repair_anyomorem_column_fragments(assets: list[Asset]) -> None:
    """Restore the bench group from its verified, flattened source columns."""
    for asset in assets:
        if (asset.source_file != "team-05/_team-documents/team five hospitals.xlsx"
                or asset.source_location != "Sheet1 row 1380"
                or norm(asset.item) != "not in use"
                or norm(asset.description) != "bench 2025 good condition"):
            continue
        asset.extras["source_layout_original"] = {
            "item": asset.item, "description": asset.description,
            "source_location": asset.source_location,
        }
        asset.item = "Bench"
        asset.description = "Bench"
        asset.department = "Reception room Maternity"
        asset.status = "Good condition"
        asset.remarks = "All in use (3)"
        asset.explicit_qty = 3
        asset.source_location = "Sheet1 rows 1440-1444"
        asset.extras["source_cells"] = ["Bench", "Reception room Maternity", "Good condition", "All in use (3)"]
        asset.extras["recorded_group_total"] = 3
        asset.extras["quantity_layout_evidence"] = (
            "Original Anyomorem HC III toolkit paragraphs before Table 11 and shared "
            "Sheet1 rows 1440-1444 state Bench, Reception room Maternity, Good condition, "
            "All in use (3). Flattened columns had joined the preceding Not in use label "
            "and its (1) to this bench record. The separate 2025 entry is a year."
        )
        asset.extras["source_group_locations"] = [asset.source_location]


def repair_kungu_unit_fragments(assets: list[Asset]) -> None:
    """Preserve Kungu's complete unit records and distinguish a wrapped fragment."""
    locations = {
        "team-06/_team-documents/TEAM SIX HOSPITALS DTB1.xlsx": ("Sheet1", 1821, 1822, (1827, 1831, 1832), 1844),
        "team-06/Apac/Kungu-HC-III/KUNGU HCIII.docx": ("Table 6", 39, 40, (44, 45, 46), 55),
    }
    indexed = {(asset.source_file, asset.source_location): asset for asset in assets if asset.source_file in locations}
    removed = set()
    for source, (table, last_couch, fragment, glucometers, lens_row) in locations.items():
        couch = indexed.get((source, f"{table} row {last_couch}"))
        continuation = indexed.get((source, f"{table} row {fragment}"))
        if couch and continuation and couch.tag.endswith("/EC/2021-04") and not any((continuation.tag, continuation.status, continuation.remarks, continuation.service, continuation.purchase)):
            merge_continuation(couch, continuation)
            couch.extras["source_group_locations"] = [couch.source_location, continuation.source_location]
            couch.extras["quantity_layout_evidence"] = "Four complete EC01-04 couch records; following department/colour/life-only line is a wrapped fragment, not a fifth asset."
            removed.add(id(continuation))
        for number in glucometers:
            asset = indexed.get((source, f"{table} row {number}"))
            if asset and norm(identity_item(asset.item)) == "glucometer":
                asset.extras["proven_unit_row"] = True
                asset.extras["quantity_layout_evidence"] = "Source count conflict: header reports 1 glucometer, but the table contains two distinct GLU01/02 tags and a third complete dated functional record; preserve all three physical records."
                asset.extras["source_group_locations"] = [f"{table} row {value}" for value in glucometers]
        lens = indexed.get((source, f"{table} row {lens_row}"))
        if lens and lens.tag.endswith("/ML/2021-01") and "low resolution power lens" in lens.remarks.casefold():
            lens.extras.setdefault("original_source_identity", lens.item)
            lens.item = "Low resolution power lens"
            lens.extras["unit_item"] = lens.item
            lens.extras["proven_unit_row"] = True
            lens.extras["quantity_layout_evidence"] = "Identity uncertainty: original item cell is blank after four TR01-04 trolley records; ML01 and 'Low resolution power lens' identify a separate device. Retain that source wording without inferring a microscope identity."
            lens.extras["source_group_locations"] = [lens.source_location]
    if removed:
        assets[:] = [asset for asset in assets if id(asset) not in removed]


def repair_building_property_fragments(assets: list[Asset]) -> None:
    """Rejoin Busaale's residential-building details split in its consolidation."""
    source = "_multi-team/busoga-and-part-of-central/Health Center Updated Asset Register  222.xlsx"
    rows = {asset.source_location: asset for asset in assets if asset.source_file == source}
    building = rows.get("Health Center row 4550")
    if building is None or norm(building.item) != "residential buildings":
        return
    fragments = [rows[f"Health Center row {number}"] for number in range(4551, 4557)
                 if f"Health Center row {number}" in rows]
    if not fragments:
        return
    # The primary BUSAALE HC III.docx Table 6 row 259 places every following
    # room/kitchen/bathroom detail in one description: "1 Block; 2 Units".
    building.extras["source_group_locations"] = [building.source_location, *(asset.source_location for asset in fragments)]
    for asset in fragments:
        merge_continuation(building, asset)
    building.extras["recorded_group_total"] = 2
    building.extras["quantity_layout_evidence"] = "Primary BUSAALE HC III.docx Table 6 row 259 records one residential block with two units; consolidation rows 4551-4556 split its room, kitchen and bathroom description and are not additional assets."
    removed = {id(asset) for asset in fragments}
    assets[:] = [asset for asset in assets if id(asset) not in removed]


def repair_wrapped_quantity_blocks(assets: list[Asset]) -> None:
    """A wrapped group description is not a list of individually recorded units."""
    removed = set()
    for index, first in enumerate(assets):
        if not first.extras.get("has_unit_rows"):
            continue
        rows = [first]
        for offset in range(index + 1, len(assets)):
            following = assets[offset]
            if not following.extras.get("unit_row") or presence_key(following) != presence_key(first):
                break
            rows.append(following)
        counts = [row.explicit_qty for row in rows if row.explicit_qty]
        identifiers = [norm(row.tag) for row in rows if not blank_tag(row.tag)]
        # The original tables put a total below multiple departmental/capacity
        # descriptions. A larger stated total cannot be represented by those
        # few untagged description lines. Full tagged unit lists stay intact.
        if len(rows) < 2 or len(counts) != 1 or counts[0] <= len(rows):
            continue
        if len(identifiers) > 1 and len(set(identifiers)) == len(identifiers):
            continue
        first.explicit_qty = counts[0]
        first.extras["recorded_group_total"] = counts[0]
        first.extras["quantity_layout_evidence"] = "Wrapped departmental/capacity descriptions share one recorded group total."
        first.extras["source_group_locations"] = [row.source_location for row in rows]
        first.extras.pop("has_unit_rows", None)
        for row in rows[1:]:
            merge_continuation(first, row)
            removed.add(id(row))
    if removed:
        assets[:] = [asset for asset in assets if id(asset) not in removed]


def repair_burondo_numbered_layout(assets: list[Asset]) -> None:
    """Restore the numbered UPS list and wrapped records verified in Table 12."""
    source = "team-26/Bundibugyo/Burondo-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT BURONDO HEALTH CENTRE III AND KISUBA SEED SCHOOL.docx"
    rows = {int(asset.source_location.rsplit(" row ", 1)[1]): asset for asset in assets
            if asset.source_file == source and asset.source_location.startswith("Table 12 row ")}
    header = rows.get(2)
    if not header or header.extras.get("source_layout_repaired"):
        return
    removed = set()
    unit_numbers = (4, 10, 14, 17, 20)
    if all(number in rows for number in unit_numbers):
        for number in unit_numbers:
            asset = rows[number]
            asset.description = join_text(asset.item, asset.description)
            asset.item = "UPS"
            asset.department = header.department
            asset.status = asset.status or header.status
            asset.remarks = asset.remarks or header.remarks
            asset.explicit_qty = 1
            asset.extras["proven_unit_row"] = True
            asset.extras["quantity_layout_evidence"] = "Source Table 12 numbers five UPS units (01)-(05), each with a separate serial."
        removed.add(id(header))
    for first_number, continuation_numbers in ((23, (24,)), (39, (40, 41, 50)), (60, (61,))):
        first = rows.get(first_number)
        if first is None:
            continue
        for number in continuation_numbers:
            if number in rows:
                merge_continuation(first, rows[number])
                removed.add(id(rows[number]))
        first.extras.pop("has_unit_rows", None)
        first.extras.pop("unit_row", None)
        first.extras["source_layout_repaired"] = True
        first.extras["quantity_layout_evidence"] = "Wrapped description, condition and serial lines in source Table 12."
        if first_number == 39:
            first.item = "Desktop computer"
            first.explicit_qty = 23
            first.extras["recorded_group_total"] = 23
            first.extras["quantity_layout_evidence"] += " Remarks state 15 working and 8 not working."
    assets[:] = [asset for asset in assets if id(asset) not in removed]


def mark_unit_records(assets: list[Asset]) -> None:
    """Confirm repeated group labels against distinct unit tags/serials."""
    repair_anyomorem_column_fragments(assets)
    repair_kungu_unit_fragments(assets)
    repair_building_property_fragments(assets)
    repair_burondo_numbered_layout(assets)
    repair_wrapped_quantity_blocks(assets)
    grouped: dict[tuple, list[Asset]] = defaultdict(list)
    for asset in assets:
        grouped[presence_key(asset) + (asset.source_location.rsplit(" row ", 1)[0],)].append(asset)
    for rows in grouped.values():
        if len(rows) < 2:
            continue
        identifiers = []
        counts = set()
        for asset in rows:
            serial = re.search(r"(?i)\bserial(?: number| no\.?)?\s*[:=]?\s*([^;]+)", asset.description)
            identifiers.append(norm(asset.tag) if not blank_tag(asset.tag) else norm(serial.group(1)) if serial else "")
            found = stated_count(asset)
            counts.add(sum(count for count, _ in found[1]) if found else 1)
        group_identifiers = any(re.search(r"\b(?:group|batch|lot)(?:\b|\d)", value) for value in identifiers)
        if 1 < max(counts) <= len(rows) and all(identifiers) and len(set(identifiers)) == len(rows) and not group_identifiers:
            evidence = (
                f"Distinct unit identifiers prove {len(rows)} individual source records; "
                "repeated group quantities and differing condition totals are not additional assets."
            )
            for asset in rows:
                asset.extras["proven_unit_row"] = True
                existing = asset.extras.get("quantity_layout_evidence", "")
                if evidence not in existing:
                    asset.extras["quantity_layout_evidence"] = "; ".join(filter(None, (existing, evidence)))


QUANTITY_AUDIT: list[dict] = []


def write_audit(path: Path, rows: list[dict]) -> None:
    """Persist source evidence before any expansion or workbook write can fail."""
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def explode(assets: list[Asset], audit_path: Path | None = None) -> list[Asset]:
    presence = Counter(presence_key(asset) for asset in assets)
    mark_unit_records(assets)
    QUANTITY_AUDIT.clear()
    planned = []
    output_count = 0
    for asset in assets:
        item, groups = decide_groups(asset, presence[presence_key(asset)] == 1)
        total = sum(count for count, _ in groups)
        output_count += total
        planned.append((asset, item, groups, total))
        QUANTITY_AUDIT.append({
            "source_file": asset.source_file, "source_location": asset.source_location,
            "facility": asset.facility, "item": asset.item, "output_rows": total,
            "quantity_evidence": json.dumps(asset.extras.get("quantity_evidence", []), ensure_ascii=False),
            "quantity_layout_evidence": asset.extras.get("quantity_layout_evidence", ""),
            "source_group_locations": json.dumps(asset.extras.get("source_group_locations", [asset.source_location]), ensure_ascii=False),
            "conflicting_counts": len({count for count, _ in asset.extras.get("quantity_evidence", [])}) > 1,
            "unit_record_proven": bool(any(asset.extras.get(key) for key in ("has_unit_rows", "unit_row", "proven_unit_row"))),
            "line_cost": asset.cost, "unit_cost": bool(asset.extras.get("unit_cost")),
            "line_recoverable": asset.recoverable, "line_acc_dep": asset.acc_dep,
            "line_nbv": asset.nbv, "line_ytd": asset.ytd,
        })
    if audit_path is not None:
        write_audit(audit_path, QUANTITY_AUDIT)
    if output_count > 1_048_575:
        largest = sorted(QUANTITY_AUDIT, key=lambda row: row["output_rows"], reverse=True)[:5]
        raise ValueError(f"The source quantities require {output_count:,} rows, exceeding Excel's 1,048,575 asset rows. Review the source counts or authorize multiple sheets. Largest splits: {largest}")
    exploded: list[Asset] = []
    for asset, item, groups, total in planned:
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
                copy.item = canonical_item(item)
                for key in ("lg_key", "facility_key"):
                    if asset.extras.get(key):
                        copy.extras[key] = asset.extras[key]
                if asset.extras.get("filled_from"):
                    copy.extras["filled_from"] = set(asset.extras["filled_from"])
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
                        if field_name == "cost" and asset.extras.get("unit_cost"):
                            continue
                        setattr(copy, field_name, per_item_amount(getattr(copy, field_name), total))
                    if copy.description and (found := LEADING_COUNT.match(copy.description)) and as_count(found.group(1)) == total:
                        copy.description = clean(found.group(2))
                    copy.extras["unit"] = f"item {running} of {total}"
                exploded.append(copy)
    return exploded


def blank_tag(value: str) -> bool:
    """A tag cell that names no tag: blank, N/A, none, nil, not engraved and the
    like. Anything holding a digit is a real number (UG/NILE/01, KAN/A/12)."""
    text = norm(value)
    if not text or is_placeholder(value):
        return True
    # "Not engraved (2)" or "N/A 2" is still no tag.
    text = re.sub(r"\s*\(?\d{1,3}\)?$", "", text).strip() if re.match(r"(not|nor|n a|na|none|nil|no tag)", text) else text
    # "Nor engraved", "Not engrved", "Notengraved": a slip of up to two letters in "not engraved".
    if not re.search(r"\d", text) and _edit_distance(re.sub(r"\s+", "", text), "notengraved") <= 2:
        return True
    if re.search(r"\d", text):
        return False
    if re.search(
        r"\b(?:all|some|they|none|no|not|yet|were|are|was)\b.*\b(?:engrav|tagg|label|number)|\bengrav\w*\b.*\b(?:not|no)\s+number|"
        r"^labell?ed$|inad\w*\s+tagg|unable\s+to\s+see|no+t\s*engrav|^not\s+yet$|^no\s+engrave|^engraved\s+(?:but\s+)?not\b|^(?:blank|nothing)$",
        text,
    ):
        # "All not engraved yet", "some are engraved but not numbered", "labelled".
        return True
    return re.fullmatch(
        r"(not\s*(yet\s*)?engrav\w*|not\s*tagged|no\s*tags?|not\s*labell?ed|not\s*(available|applicable|indicated)|"
        r"engraved|nil+|none|n\s*a|na|yes|no|not|tag\s*number.*|to\s+be\s+engraved|pending)(\s.*)?",
        text,
    ) is not None


TOOLKIT_ITEMS = ROOT / "reference" / "toolkit_items.json"


def _toolkit_index() -> dict[str, str]:
    index: dict[str, str] = {}
    if TOOLKIT_ITEMS.exists():
        import json

        for names in json.load(TOOLKIT_ITEMS.open(encoding="utf-8")).values():
            for name in names:
                index.setdefault(squash(name), name)
                index.setdefault(squash(re.sub(r"[^A-Za-z0-9 ]", "", name)), name)
    return index


TOOLKIT_INDEX = _toolkit_index()


def canonical_item(item: str) -> str:
    """The toolkit's spelling of an equipment name where the source spells the same
    name without spaces or with letters split across runs ("B.P.Machine,Digital",
    "Autoclav e 20 Liters.,Du o Operated")."""
    text = clean(item)
    if not text:
        return text
    key = squash(text)
    found = TOOLKIT_INDEX.get(key) or TOOLKIT_INDEX.get(squash(re.sub(r"[^A-Za-z0-9 ]", "", text)))
    return found or text


def identity_item(item: str) -> str:
    parenthetical = parenthetical_quantity(item)
    if parenthetical:
        return canonical_item(parenthetical[0])
    trailing = trailing_quantity(item)
    if trailing:
        return canonical_item(trailing[0])
    return canonical_item(item)


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


# Stage 1, "Empty or unclear fields": a fact that another statement of the same
# line, or another row of the same item at the same facility, states fills a cell
# the kept line left empty. Nothing is guessed: a value is copied only when every
# statement of it agrees, and a money figure only when it is a unit figure.
FILL_FIELDS = ("life", "purchase", "service", "recoverable", "cost", "acc_dep", "nbv", "ytd", "department", "description")
MONEY_FIELDS = {"recoverable", "cost", "acc_dep", "nbv", "ytd"}
FILL_NOTES: Counter = Counter()
# The two template workbooks named by the prompt. raw-data-grouped holds byte-identical
# copies; they supply a fact for a facility already on the register, never a new row.
TEMPLATE_DONORS = (
    "_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/registers-by-facility/updated-asset-registers/"
    "new-templates-to-follow/Health Center Updated Asset Register.xlsx",
    "_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/registers-by-facility/updated-asset-registers/"
    "new-templates-to-follow/Seed School Updated Asset Register.xlsx",
)
TEMPLATE_FOLDER = ROOT / "new-templates-to-follow"


def blank_fact(value: object) -> bool:
    if value is None or value == "":
        return True
    if isinstance(value, (int, float, date, datetime)):
        return False
    return is_placeholder(value)


def fact_key(value: object) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, (int, float)):
        return repr(float(value))
    return norm(value)


def stated_values(rows: list[Asset], field_name: str) -> list[tuple[str, object, str]]:
    return [
        (fact_key(getattr(row, field_name)), getattr(row, field_name), row.source_file)
        for row in rows if not blank_fact(getattr(row, field_name))
    ]


def copy_fact(target: Asset, field_name: str, stated: list[tuple[str, object, str]]) -> bool:
    """Write the one value the statements agree on; disagreement leaves the cell empty."""
    if not stated or len({key for key, _, _ in stated}) != 1:
        return False
    setattr(target, field_name, stated[0][1])
    FILL_NOTES[field_name] += 1
    for _, _, source in stated:
        if source != target.source_file:
            target.extras.setdefault("filled_from", set()).add(source)
    return True


def fill_from_folded_lines(winners: list[Asset], losers: list[Asset]) -> None:
    """The kept line takes a fact the folded statement of the same line recorded.
    A money figure is taken only from a statement that counted the same units."""
    # Counts describe the original statements, before any missing fact is filled.
    # A large repeated-item bucket must not reparse every loser's count for each
    # monetary field of every winner.
    loser_groups: dict[int, list[Asset]] = defaultdict(list)
    for source in losers:
        loser_groups[represented_count(source)].append(source)
    winner_counts = {id(target): represented_count(target) for target in winners}
    for target in winners:
        for field_name in FILL_FIELDS:
            if not blank_fact(getattr(target, field_name)):
                continue
            pool = losers
            if field_name in MONEY_FIELDS:
                pool = loser_groups.get(winner_counts[id(target)], [])
            copy_fact(target, field_name, stated_values(pool, field_name))


def facility_item_key(asset: Asset) -> tuple[str, str, str]:
    return (
        asset.extras.get("lg_key") or norm(asset.lg),
        asset.extras.get("facility_key") or norm(asset.facility),
        norm(identity_item(asset.item)),
    )


def fill_within_facility(assets: list[Asset], donors: list[Asset]) -> None:
    """After the quantity split, the rows of one item at one facility share a fact
    that some of them left empty, and the template workbooks state a fact for a
    facility already on the register. A money figure is copied only from a return
    that priced every unit of that item, or at least two of them, so one line total
    is never spread over the units of another line."""
    groups: dict[tuple[str, str, str], list[Asset]] = defaultdict(list)
    for asset in assets:
        if asset.facility and asset.item:
            groups[facility_item_key(asset)].append(asset)
    extra: dict[tuple[str, str, str], list[Asset]] = defaultdict(list)
    for asset in donors:
        if asset.facility and asset.item:
            extra[facility_item_key(asset)].append(asset)
    for group_key, rows in groups.items():
        donors_here = extra.get(group_key, [])
        for field_name in FILL_FIELDS:
            blanks = [row for row in rows if blank_fact(getattr(row, field_name))]
            if not blanks:
                continue
            stated = stated_values(rows, field_name) or stated_values(donors_here, field_name)
            if not stated:
                continue
            if field_name in MONEY_FIELDS:
                totals = Counter(row.source_file for row in rows + donors_here)
                counted = Counter(source for _, _, source in stated)
                stated = [entry for entry in stated if counted[entry[2]] >= 2 or counted[entry[2]] == totals[entry[2]]]
                if not stated:
                    continue
            for row in blanks:
                copy_fact(row, field_name, stated)


def template_donors() -> tuple[list[Asset], list[str]]:
    """Rows of the two template workbooks, used only to fill a fact."""
    donors: list[Asset] = []
    notes: list[str] = []
    for relative in TEMPLATE_DONORS:
        path = GROUPED / relative
        original = TEMPLATE_FOLDER / path.name
        if not path.exists():
            notes.append(f"Template workbook not found under raw-data-grouped: {relative}.")
            continue
        same = original.exists() and file_hash(path) == file_hash(original)
        try:
            rows = read_workbook(path)
        except Exception as error:  # noqa: BLE001 - a template that cannot be read fills nothing
            notes.append(f"Template workbook not read: {relative} ({error}).")
            continue
        donors.extend(rows)
        notes.append(
            f"new-templates-to-follow/{path.name}: {len(rows):,} lines read as a source of facts only"
            + (" (byte-identical copy filed at " + relative + ")." if same else f" (read from {relative}; new-templates-to-follow copy differs).")
        )
    return explode(donors), notes


NUMERIC_ITEM = re.compile(r"^[\(\[]?-?0*\d+(?:,\d{3})*(?:\.0)?[\)\]]?$")


def settle_unnamed_lines(assets: list[Asset]) -> tuple[list[Asset], list[str]]:
    """A line whose item cell holds only a number or a placeholder names no asset.

    Where the description names the asset, it becomes the item name: a line number
    or a count sat in the item column. A positive count there beside a blank tag is
    the line's quantity, as a count in Asset Number is. Where nothing else on the
    line is stated, the line is a count or an unedited template line and is left out.
    """
    kept: list[Asset] = []
    dropped = 0
    renamed = 0
    counted = 0
    for asset in assets:
        item = clean(asset.item)
        if item and not NUMERIC_ITEM.match(item) and not is_placeholder(item):
            kept.append(asset)
            continue
        description = clean(asset.description)
        if description and not NUMERIC_ITEM.match(description) and not is_placeholder(description) and bare_count(description) is None:
            count = bare_count(item) if item else None
            if count is not None and blank_tag(asset.tag) and asset.explicit_qty is None:
                asset.explicit_qty = count
                counted += 1
            asset.item = description
            asset.description = ""
            renamed += 1
            kept.append(asset)
            continue
        dropped += 1
    notes = [
        f"{dropped:,} lines whose item cell held only a number or a placeholder, and whose description named nothing, were left out: "
        f"a count or an unedited template line names no asset. On {renamed:,} such lines the description named the asset and became the item name; "
        f"on {counted:,} of them the number in the item cell, beside a blank tag, was read as the line's quantity."
    ]
    return kept, notes


# ------------------------------------------------------- central government (MDAs)
#
# Ministries, agencies and referral hospitals keep their UgIFT assets on their own
# votes. Their returns sit in folders this register otherwise leaves out, so they are
# read by name: the ministries' verification returns (one sheet per MDA), the
# programme's own fixed-asset registers, the two regional blood-bank inventories, and
# the hospital and inspectorate rows of the consolidated MDA status register.
PROGRAMME_FOLDER = "_multi-team/programme-documents/All WIP Ugift/All WIP Ugift"
MDA_STATUS_REGISTER = "_multi-team/programme-documents/MDA status register.xlsx"
PROGRAMME_REGISTERS = (
    f"{PROGRAMME_FOLDER}/fwdugiftassets/UGIFT .ASSETS REGISTER-BPED.xls",
    f"{PROGRAMME_FOLDER}/fwdugiftassets/UGIFT FIXED ASSETS REGISTER FOR FY2022.2023..xls",
    f"{PROGRAMME_FOLDER}/fwdugiftassets/UGIFT ASSETS REGISTER FOR FY2023.2024 FOR AUDITORS.xls",
    f"{PROGRAMME_FOLDER}/fwdugiftassets/UGIFT ASSETS REGISTER FOR FY2024.2025..xls",
    f"{PROGRAMME_FOLDER}/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
)
INVENTORIES = (
    (f"{PROGRAMME_FOLDER}/Ugift  Inventory collection HOIMA blood bank.xlsx", "Hoima Regional Blood Bank"),
    (f"{PROGRAMME_FOLDER}/Ugift Arua bb chemmart inventory.xlsx", "Arua Regional Blood Bank"),
)
MDA_CONSOLIDATION = "_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-WIP-consolidated-MDA-status-register.xlsx"
CENTRAL_NOTES: Counter = Counter()
HOSPITAL_WORD = re.compile(r"(?i)\b(?:gh|general hospital|hospital|rrh|nrh|nrmh|cufh|isolation cent(?:re|er)|blood bank)\b")


def place_central(asset: Asset, vote: LocalGovernment, facility: str, kind: str) -> None:
    """Settle a central-government row: the vote, the site as written, and the keys
    the union, quantity and fill steps group on."""
    asset.lg = vote.display
    asset.facility = clean(facility)
    asset.facility_type = kind
    asset.extras["lg_key"] = vote.key
    asset.extras["facility_key"] = facility_key(asset.facility or vote.display, kind) or f"{norm(vote.display)}|"
    asset.extras["central"] = True
    CENTRAL_NOTES[vote.display] += 1


def hospital_name(text: str) -> str:
    name = clean(text)
    name = re.sub(r"(?i)\bGH\b", "General Hospital", name)
    name = re.sub(r"(?i)\bRRH\b", "Regional Referral Hospital", name)
    name = re.sub(r"(?i)\bNRH\b", "National Referral Hospital", name)
    return re.sub(r"\s+", " ", name).strip()


def read_mda_status_register(path: Path) -> list[Asset]:
    """The ministries' verification returns: one toolkit-layout sheet per MDA."""
    relative = path.relative_to(GROUPED).as_posix()
    assets: list[Asset] = []
    for name, rows in sheet_rows(path):
        sheet_vote = resolve_mda(name)
        parsed = parse_template_sheet(name, rows, relative, path.name, sheet_vote.display if sheet_vote else "")
        for asset in parsed:
            vote = (resolve_lg(asset.lg) if asset.lg else None) or sheet_vote
            if vote is None:
                continue
            if vote.kind == "MDA":
                place_central(asset, vote, "", "MDA")
            else:
                # A vehicle the ministry handed to a district: the district's asset,
                # kept at its headquarters.
                place_central(asset, vote, f"{vote.display} District Headquarters", "Local government office")
            assets.append(asset)
    return assets


def _column_index(keys: list[str], *names: str) -> int | None:
    for wanted in names:
        for index, key in enumerate(keys):
            if key.startswith(wanted):
                return index
    return None


def read_programme_register(path: Path) -> list[Asset]:
    """The programme's fixed-asset registers (vehicles, motorcycles, ICT, furniture,
    software). The vote is the ministry the Location column names, else the section
    label, else the register's owner (MoFPED). A row located at a local government
    office is that government's asset and outside this register."""
    relative = path.relative_to(GROUPED).as_posix()
    owner = resolve_mda("MOFPED")
    assets: list[Asset] = []
    for name, rows in sheet_rows(path):
        if re.search(r"(?i)total", name):
            continue
        header_at = None
        for index, row in enumerate(rows[:15]):
            keys = [squash(value) for value in row]
            if any(key.startswith("description") for key in keys) and any(
                key.startswith(("makemodel", "identification", "category")) or "serialno" in key for key in keys
            ):
                header_at = index
                break
        if header_at is None:
            continue
        keys = [squash(value) for value in rows[header_at]]
        col = {
            "category": _column_index(keys, "category"), "qty": _column_index(keys, "qty"), "description": _column_index(keys, "description"),
            "make": _column_index(keys, "makemodel"), "reg": _column_index(keys, "regno", "registrationnumber"), "colour": _column_index(keys, "colour"),
            "engine": _column_index(keys, "engineno", "enginenumber"), "chassis": _column_index(keys, "chassisno", "chassisnumber"),
            "capacity": _column_index(keys, "engcapacity", "enginecapacity"), "condition": _column_index(keys, "workingcond", "wcond", "functionality"),
            "year": _column_index(keys, "yearofman"), "acquired": _column_index(keys, "dateofacquisition"),
            "ident": _column_index(keys, "identificationno", "identification"), "serial": _column_index(keys, "serialno"),
            "location": _column_index(keys, "location"), "room": _column_index(keys, "room"), "user": _column_index(keys, "username"),
            "title": _column_index(keys, "usertitle", "title"), "department": _column_index(keys, "userdepartment", "userdept", "component"),
            "cost": _column_index(keys, "costsinugx", "costinugx", "costinugandacurency", "cost"), "life": _column_index(keys, "expectedusefullife"),
            "warranty": _column_index(keys, "warrantyexp", "warrenty"), "supplier": _column_index(keys, "supplier"),
        }

        def get(row: list[object], field: str) -> object:
            index = col.get(field)
            return row[index] if index is not None and index < len(row) else None

        section_vote = None
        previous_date: object = None
        for number, row in enumerate(rows[header_at + 1:], header_at + 2):
            filled = [value for value in row if value not in (None, "")]
            if not filled:
                continue
            description = clean(get(row, "description"))
            category = clean(get(row, "category")) if col["category"] is not None else ""
            identity = clean(get(row, "ident")) or clean(get(row, "reg"))
            if len([value for value in filled if isinstance(value, str)]) <= 1 and not identity and not clean(get(row, "serial")):
                # A section label ("Ministry of Water and Evir..", "VEHICLES PROCURED
                # UNDER UGIFT", a subtotal): it names the section's vote or nothing.
                label = next((clean(value) for value in filled if isinstance(value, str)), "")
                vote = resolve_lg(label) or lg_from_text(label)
                if vote is not None and vote.kind == "MDA":
                    section_vote = vote
                continue
            if re.match(r"(?i)^(?:assets? register|consolidated|vehicles? (?:procured|under)|furniture|total|summary)", description) and not identity:
                vote = lg_from_text(description)
                if vote is not None and vote.kind == "MDA":
                    section_vote = vote
                continue
            if not description and not category:
                continue
            if squash(description) in {"description", "makemodel"} or squash(category) == "category":
                continue
            acquired = get(row, "acquired")
            if isinstance(acquired, str) and acquired.strip() in {'"', "''", "〃"}:
                acquired = previous_date
            elif acquired not in (None, ""):
                previous_date = acquired
            details = [
                description if category else "",
                f"Model {clean(get(row, 'make'))}" if clean(get(row, "make")) else "",
                f"Serial number {clean(get(row, 'serial'))}" if clean(get(row, "serial")) and not is_placeholder(get(row, "serial")) else "",
                f"Engine No. {clean(get(row, 'engine'))}" if clean(get(row, "engine")) else "",
                f"Chassis No. {clean(get(row, 'chassis'))}" if clean(get(row, "chassis")) else "",
                f"Engine capacity {clean(get(row, 'capacity'))}" if clean(get(row, "capacity")) else "",
                f"Colour {clean(get(row, 'colour'))}" if clean(get(row, "colour")) else "",
                f"Year of manufacture {clean(get(row, 'year')).replace('.0', '')}" if clean(get(row, "year")) else "",
            ]
            remarks = [
                f"Room {clean(get(row, 'room'))}" if clean(get(row, "room")) else "",
                f"User {clean(get(row, 'user'))}" if clean(get(row, "user")) else "",
                f"User title {clean(get(row, 'title'))}" if clean(get(row, "title")) else "",
                f"Supplier {clean(get(row, 'supplier'))}" if clean(get(row, "supplier")) else "",
                f"Warranty {clean(get(row, 'warranty'))}" if clean(get(row, "warranty")) else "",
            ]
            quantity = clean(get(row, "qty"))
            count = quantity_cell(quantity)
            condition = clean(get(row, "condition"))
            asset = Asset(
                item=category or description,
                department=clean(get(row, "department")),
                description="; ".join(part for part in details if part),
                life=number_or_text(get(row, "life")),
                tag=identity,
                purchase=excel_date(acquired),
                cost=number_or_text(get(row, "cost")),
                status="" if squash(condition) in {"workingcond", "wcond", "functionality"} else condition,
                remarks="; ".join(part for part in remarks if part),
                explicit_qty=count,
                source_file=relative,
                source_location=f"{name.strip()} row {number}",
            )
            asset.extras["source_cells"] = [clean(value) for value in row if isinstance(value, str) and clean(value)]
            if re.fullmatch(r"(?i)\d+(?:\.\d+)?\s*(?:years?|yrs?|months?)", asset.department or ""):
                # The FY2024/25 motorcycle sheet heads its useful-life column "User Department".
                asset.life, asset.department = asset.department, ""
            location = clean(get(row, "location"))
            vote = (resolve_lg(location) or lg_from_text(location)) if location else None
            if vote is not None and vote.kind != "MDA":
                CENTRAL_NOTES["(local government offices, left out)"] += 1
                continue
            vote = vote or section_vote or owner
            site = location if location and resolve_mda(location) is not None and resolve_mda(location).code == "MOFPED" and norm(location) not in {"mofped", "ugift secretariat"} else ""
            place_central(asset, vote, site, "MDA")
            assets.append(asset)
    return assets


def read_inventory(path: Path, facility: str) -> list[Asset]:
    """A blood-bank equipment inventory: equipment, model, serial, engraved number,
    condition grade, department and room."""
    relative = path.relative_to(GROUPED).as_posix()
    vote = resolve_mda(facility)
    assets: list[Asset] = []
    for name, rows in sheet_rows(path):
        header_at = next((index for index, row in enumerate(rows[:10]) if any("serialno" in squash(value) for value in row)), None)
        if header_at is None or vote is None:
            continue
        keys = [squash(value) for value in rows[header_at]]
        col = {
            "item": _column_index(keys, "equipmentname"), "model_name": _column_index(keys, "modelname"), "type": _column_index(keys, "type"),
            "model": _column_index(keys, "modelno"), "serial": _column_index(keys, "serialno"), "tag": _column_index(keys, "engravedno"),
            "condition": _column_index(keys, "condition"), "department": _column_index(keys, "department"), "room": _column_index(keys, "room"),
        }

        def get(row: list[object], field: str) -> str:
            index = col.get(field)
            return clean(row[index]) if index is not None and index < len(row) else ""

        for number, row in enumerate(rows[header_at + 1:], header_at + 2):
            item = get(row, "item") or get(row, "model_name")
            if not item or not any(value not in (None, "") for value in row):
                continue
            details = [
                f"Model {get(row, 'model_name')} {get(row, 'model')}".strip() if col["item"] is not None and (get(row, "model_name") or get(row, "model")) else (f"Model {get(row, 'model')}" if get(row, "model") else ""),
                f"Serial number {get(row, 'serial')}" if get(row, "serial") and not is_placeholder(get(row, "serial")) else "",
            ]
            asset = Asset(
                item=item,
                department=get(row, "department"),
                description="; ".join(part for part in details if part),
                tag=get(row, "tag"),
                status=f"Condition {get(row, 'condition')}" if get(row, "condition") else "",
                remarks=f"Room {get(row, 'room')}" if get(row, "room") else "",
                source_file=relative,
                source_location=f"{name.strip()} row {number}",
            )
            asset.extras["source_cells"] = [clean(value) for value in row if isinstance(value, str) and clean(value)]
            place_central(asset, vote, facility, "Blood bank")
            assets.append(asset)
    return assets


def read_mda_consolidation(path: Path) -> list[Asset]:
    """Hospital and inspectorate rows of the consolidated MDA status register: MoH
    supplies to referral, national and general hospitals, and the MoES inspection
    tablets held at district inspectorates. Local-government facility rows (field
    returns read from the team folders, and programme supply lists) and the
    ministries' ICT rows (read from their own registers) are left to those sources."""
    relative = path.relative_to(GROUPED).as_posix()
    assets: list[Asset] = []
    for name, rows in sheet_rows(path):
        header_at = next((index for index, row in enumerate(rows[:10]) if any(squash(value).startswith("equipmentitem") for value in row)), None)
        if header_at is None:
            continue
        header = rows[header_at]
        mapping = classify_header(header)
        if not mapping:
            continue
        category_at = next((index for index, value in enumerate(header) if squash(value) == "category"), None)
        group = ""
        for number, row in enumerate(rows[header_at + 1:], header_at + 2):
            filled = [value for value in row if value not in (None, "")]
            if not filled:
                continue
            lg_text = clean(cell(row, mapping, "lg"))
            facility_text = clean(cell(row, mapping, "facility"))
            if len(filled) == 1 and lg_text:
                group = lg_text
                continue
            if not clean(cell(row, mapping, "item")):
                continue
            category = clean(row[category_at]) if category_at is not None and category_at < len(row) else ""
            remarks = clean(cell(row, mapping, "remarks"))
            if TOTAL_ITEM.match(lg_text) or TOTAL_ITEM.match(facility_text) or TOTAL_ITEM.match(group):
                continue
            if re.search(r"(?i)mda ict register", remarks):
                # The ministries' own registers are read directly.
                continue
            vote = resolve_mda(facility_text) or resolve_mda(lg_text) or resolve_mda(group)
            kind = ""
            facility = ""
            if vote is not None and vote.code != "KCCA" and not re.search(r"hospital", vote.display, re.I) and resolve_mda(facility_text) is None \
                    and re.search(r"(?i)health\s*cent|\bhc\s*(?:ii|iii|iv|2|3|4)\b|\bh/?c\b|seed|school|\bs\.?s\.?s?\b", facility_text):
                # A ministry's supply to a local-government facility: that facility's
                # field return is the record, read from the team folders.
                CENTRAL_NOTES["(ministry supplies to local-government facilities, left out)"] += 1
                continue
            if vote is not None:
                kind = "Hospital" if re.search(r"hospital", vote.display, re.I) else "MDA"
                if category.casefold() == "mda" and re.search(r"(?i)inspection", facility_text):
                    lg = resolve_lg(lg_text) or lg_from_text(lg_text)
                    if lg is not None and lg.kind != "MDA":
                        facility = f"{lg.display} District Inspectorate"
                    elif re.search(r"(?i)^(?:western|eastern|northern|central|karamoja|west nile|busoga|bukedi|bugisu|teso|sebei|acholi|lango|ankole|bunyoro|tooro|rwenzori|kigezi)\b", lg_text):
                        facility = f"{clean(lg_text).title()} Region Inspectorate"
                    else:
                        # Tablets the ministry had not yet allocated to a district.
                        facility = ""
                elif facility_text and resolve_mda(facility_text) is None:
                    # A site of the vote: "Kisenyi Health Centre IV" under KCCA.
                    facility = hospital_name(facility_text)
                elif facility_text and kind == "Hospital" and re.search(r"(?i)\b(?:upper|lower|isolation|annex|unit|wing|cent(?:re|er)|blood bank)\b", facility_text):
                    # A site inside the hospital vote ("Upper Mulago NRH", "Mulago Isolation Center").
                    facility = hospital_name(facility_text)
            elif facility_text and HOSPITAL_WORD.search(facility_text) and not re.search(r"(?i)health\s*cent|\bhc\b|\bh/?c\b", facility_text):
                # A general hospital under its district: the district's asset.
                lg = resolve_lg(lg_text) or lg_from_text(lg_text) or lg_from_text(group) or resolve_lg(re.sub(r"(?i)\b(?:gh|general hospital|hospital)\b.*$", "", facility_text))
                if lg is None or lg.kind == "MDA":
                    CENTRAL_NOTES["(hospital rows with no vote, left out)"] += 1
                    continue
                vote, kind, facility = lg, "Hospital", hospital_name(facility_text)
            elif resolve_mda(lg_text) is None and resolve_mda(group) is None and lg_text and (resolve_lg(lg_text) or lg_from_text(lg_text)) and re.search(r"(?i)health cent(?:re|er)\s*iv|\bhc\s*iv\b", facility_text):
                continue
            else:
                continue
            asset = take_asset(row, mapping, relative, f"{name.strip()} row {number}")
            place_central(asset, vote, facility, kind)
            assets.append(asset)
    return assets


def read_central_sources(source_audit: list[dict] | None = None) -> dict[str, list[Asset]]:
    """Every central-government source, keyed by its path under raw-data-grouped."""
    found: dict[str, list[Asset]] = {}
    readers = [(MDA_STATUS_REGISTER, read_mda_status_register)]
    readers += [(relative, read_programme_register) for relative in PROGRAMME_REGISTERS]
    readers += [(relative, (lambda path, facility=facility: read_inventory(path, facility))) for relative, facility in INVENTORIES]
    readers.append((MDA_CONSOLIDATION, read_mda_consolidation))
    for relative, reader in readers:
        path = GROUPED / relative
        if not path.exists():
            CENTRAL_NOTES[f"(missing source: {relative})"] += 1
            if source_audit is not None:
                source_audit.append({"source_file": relative, "status": "missing", "asset_rows": 0, "error": "Named central-government source does not exist"})
            continue
        try:
            assets = reader(path)
        except Exception as error:
            if source_audit is None:
                raise
            source_audit.append({"source_file": relative, "status": "error", "asset_rows": 0, "error": f"{type(error).__name__}: {error}"})
            print(f"SOURCE ERROR {relative}: {type(error).__name__}: {error}", flush=True)
            continue
        if source_audit is not None:
            source_audit.append({"source_file": relative, "status": "parsed" if assets else "no_asset_rows", "asset_rows": len(assets), "error": ""})
        if assets:
            found[relative] = assets
    return found


def source_files(asset: Asset) -> str:
    """The row's file, then any file another fact on the row was taken from."""
    extra = sorted(set(asset.extras.get("filled_from", ())) - {asset.source_file})
    return asset.source_file if not extra else "; ".join([asset.source_file, *extra])


def union_facility_submissions(assets: list[Asset]) -> tuple[list[Asset], list[str]]:
    """Keep every distinct item when a facility was submitted more than once.

    The same line in two returns is kept once, at the larger recorded count.
    An item that appears in only one return is kept.
    """
    grouped: dict[tuple[str, str], dict[str, list[Asset]]] = defaultdict(lambda: defaultdict(list))
    for asset in assets:
        key = asset.extras.get("facility_key") or facility_key(asset.facility, asset.facility_type)
        if not key:
            continue
        grouped[(asset.extras.get("lg_key") or norm(asset.lg), key)][asset.source_file].append(asset)
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
            losers: list[Asset] = []
            for name, file_rows in by_file.items():
                if name == winner:
                    continue
                folded += len(file_rows)
                losers.extend(file_rows)
                for asset in file_rows:
                    drop.add(id(asset))
            fill_from_folded_lines(by_file[winner], losers)
        if folded:
            sample = next(iter(next(iter(sources.values()))))
            notes.append(
                f"{sample.facility} ({sample.lg}): {len(sources)} returns combined; "
                f"{folded} repeated lines folded in; items found in only one return were kept."
            )
    kept = [asset for asset in assets if id(asset) not in drop]
    return kept, notes


def check_examples() -> None:
    def groups(item="", status="", remarks="", qty=None, alone=True, asset_number="", description="", tag="", repeats=None):
        asset = Asset(
            item=item, status=status, remarks=remarks, explicit_qty=qty,
            asset_number=asset_number, description=description, tag=tag,
        )
        if repeats is None:
            repeats = 1 if alone else 2
        return decide_groups(asset, alone, repeats)

    assert groups(status="2 functional and one in the store")[1] == [(2, "Functional"), (1, "In the store")]
    assert groups(remarks="116 verified as good then 4 damaged")[1] == [(116, "Verified as good"), (4, "Damaged")]
    assert groups(remarks="Received 2 and all still functioning.")[1] == [(2, None)]
    assert groups(remarks="39 desks were supplied")[1] == [(39, None)]
    assert groups(item="B.P. Machine, Digital(2)", alone=True) == ("B.P. Machine, Digital", [(2, None)])
    # The same bracketed line in two departments of one return still states two each.
    assert groups(item="B.P. Machine, Digital(2)", alone=False, repeats=1) == ("B.P. Machine, Digital", [(2, None)])
    assert groups(item="Office Chairs (20)", alone=False, repeats=21) == ("Office Chairs", [(20, None)])
    # Repetition alone does not establish that a source already lists units.
    assert groups(item="Laboratory stools (192)", alone=False, repeats=193) == ("Laboratory stools", [(192, None)])
    assert groups(item="Desks", qty=60, alone=False) == ("Desks", [(60, None)])
    assert groups(item="3 SEATER SCHOOL DESK")[1] == [(1, None)]
    assert groups(item="24 PORT SWITCH")[1] == [(1, None)]
    assert groups(item="Mattresses", description="60 mattresses, foam", tag="N/A")[1] == [(60, None)]
    assert groups(item="Laptop Dell 15")[1] == [(1, None)]
    assert groups(item="Bench 50") == ("Bench", [(50, None)])
    assert groups(remarks="600 verified as good then 4 damaged")[1] == [(600, "Verified as good"), (4, "Damaged")]
    assert groups(item="Bed, Adult", asset_number="14 beds and mattress", tag="BUKMB/HC/01")[1] == [(14, None)]
    assert bare_integer("(3)") == 3 and bare_integer(-9) == 9 and bare_integer("12 stances") is None
    assert blank_tag("Not yet engraved") and blank_tag("No tag") and blank_tag("Engraved") and blank_tag("Tag Number ( engrave no.)")
    assert not blank_tag("UG/NILE/01") and not blank_tag("579-BUN-ACTF-01") and not blank_tag("KAN/A/12")
    assert looks_like_facility("ADAGMON HC 111") and not looks_like_facility("2 at school") and not looks_like_facility("Educational")
    assert parse_banner("Instrument set, ENT Basic for HCIII") is None
    assert parse_banner("Facility Name: Abalang HC III") == ("", "Abalang HC III")
    assert parse_banner("ADEKNINO HC II") == ("", "ADEKNINO HC II")
    assert groups(item="Desks 125") == ("Desks", [(125, None)])
    assert groups(item="Desks 107", alone=False, repeats=108)[1] == [(107, None)]
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
    workbook = Workbook(write_only=True)
    sheet = workbook.create_sheet("Asset Register")
    header_font = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
    header_fill = PatternFill("solid", fgColor="1F4E79")
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{max(len(assets) + 1, 2)}"
    widths = {
        1: 36, 2: 18, 3: 18, 4: 42, 5: 14, 6: 28, 7: 18, 8: 20, 9: 16, 10: 14,
        11: 14, 12: 16, 13: 14, 14: 28, 15: 42, 16: 28, 17: 36, 18: 16, 19: 12,
        20: 55, 21: 28,
    }
    for index, width in widths.items():
        sheet.column_dimensions[get_column_letter(index)].width = width
    sheet.row_dimensions[1].height = 30
    cells = [WriteOnlyCell(sheet, value=value) for value in HEADERS]
    for cell_item in cells:
        cell_item.font = header_font
        cell_item.fill = header_fill
        cell_item.alignment = Alignment(wrap_text=True, vertical="center")
    sheet.append(cells)
    for asset in assets:
        sheet.append([
            asset.item, asset.department, asset.asset_number, asset.description, display(asset.life),
            asset.tag, display(asset.purchase), display(asset.service), asset.recoverable, asset.cost,
            asset.acc_dep, asset.nbv, asset.ytd, asset.status, asset.remarks,
            asset.lg, asset.facility, asset.facility_type, asset.extras.get("unit", ""),
            source_files(asset), asset.source_location,
        ])
    notes_sheet = workbook.create_sheet("Read Me")
    lines = [
        "One workbook. Health centres and seed schools are rows in Asset Register, not separate files.",
        "Columns follow the health-centre and seed-school templates in new-templates-to-follow. Facility holds the facility name in one spelling; Facility type is School or Health centre.",
        "Each physical item is one row, the same rule as the 22 September register. Where a source line stated a quantity, that line was repeated once per item. Unit shows item 1 of 100, and the units column in the GOU template is 1.",
        "Every retained source line was scanned for a positive whole-number count, with no quantity cap or restriction to item types. Counts may be in a quantity column, brackets, an item suffix or prefix, description, status, remarks, or an explicit count phrase in any other column, including number words. A bare Asset Number is a count only for the item's sole line with a blank tag. Repeated totals are counted once and distinct condition subsets are added.",
        "Model numbers (LaserJet 1320, Laptop 840), measures (15 inch, 20 litres, 3 seater, 2 stance, 24 port), dates, money and identifiers are not counts. Number size alone never excludes a count. A repeated total is suppressed only where the source layout lists unit rows or distinct tags/serials confirm the units. Identical grouped rows each retain their own quantity; unit rows are never deduplicated.",
        "Where a grouped line carried one cost, recoverable cost, accumulated depreciation, net book value or year-to-date depreciation, that figure was treated as the line total and divided by the quantity, so each asset row holds its share. A unit price was not divided.",
        "Equipment names spelt without spaces or with letters split across Word runs were written in the toolkit's spelling (B.P. Machine, Digital; Autoclave 20 Liters.,Duo Operated).",
        "Spreadsheets and Word verification tables under raw-data-grouped were read, except programme-documents. The data-management chat in that folder is the exception. A file is an asset source when it has an asset table: an Equipment/Item header, or a description column with condition, quantity, tag or cost.",
        "Photographs, narrative reports, reconciliation lists and distribution lists are not asset lines. In one folder the spreadsheet was kept over a Word file of the same stem, and byte-for-byte duplicates were read once.",
        "Draft sheets (Table 1, Sheet 1) were left out where the same workbook already had a consolidated sheet with local government and facility columns.",
        "Facility and local government come from the row, then from a banner on the sheet (Name of LG, Name of health facility, Name of school, or a facility name standing alone, also in Word paragraphs and details tables), then from the folder path team-NN/<Local government>/<Facility>/. "
        "A combined health-centre-and-school return filed under both facility folders gives its health-centre tables to the health centre and its school tables to the school. Where none of these names the place, the reconciliation's link from the file to one facility of that kind, or the facility named in the file name, was used.",
        "Local governments are written in the spelling of facility-reconciliation.csv (one typing slip tolerated: Muyuge is Mayuge); facility names in the reconciliation spelling where the name is listed, otherwise ending in Seed Secondary School or Health Centre III. "
        "A district-wide or team-wide register contributes only the rows that name a UgIFT health centre or seed school; district offices, sub-counties, primary schools and water schemes are outside this register.",
        "Where a team submitted more than one workbook for the same facility, the lists were combined. Two returns are the same facility when the normalised local government and facility name match. A repeated line (same tag and item, or same item, description, status and department) was kept once, from the return with the larger stated count. An item present in only one return was kept. "
        "A re-saved copy of a return whose lines are all in another copy was read once.",
        "",
        "Sources:",
        *sources,
        "",
        "Facilities combined from more than one return, files left out, and other notes:",
        *(notes or ["None."]),
    ]
    notes_sheet.column_dimensions["A"].width = 140
    for index, line in enumerate(lines, 3):
        notes_sheet.row_dimensions[index].height = max(18, 15 * ((len(str(line)) + 129) // 130))
    title = WriteOnlyCell(notes_sheet, value="UgIFT shared asset register")
    title.font = Font(bold=True, size=14, color="1F4E79")
    notes_sheet.append([title])
    notes_sheet.append([])
    for line in lines:
        note = WriteOnlyCell(notes_sheet, value=line)
        note.alignment = Alignment(wrap_text=True, vertical="top")
        notes_sheet.append([note])
    workbook.save(OUTPUT)


def row_signature(asset: Asset) -> tuple[str, ...]:
    # The facility is part of the line: the same lines filed for another facility are
    # another return, not a copy.
    return (
        norm(identity_item(asset.item)), norm(asset.description), norm(asset.tag), norm(asset.status), norm(asset.department),
        str(represented_count(asset)),
        asset.extras.get("facility_key") or norm(asset.facility),
    )


def drop_near_duplicates(parsed: dict[str, list[Asset]]) -> list[str]:
    """Drop a workbook whose lines are all (98 percent or more) already in another
    workbook: a re-saved copy of the same return that differs only in its label
    cells, so byte comparison did not catch it. The copy filed under a facility
    folder is the one kept. Returns notes."""
    notes: list[str] = []
    signatures = {relative: Counter(row_signature(asset) for asset in assets) for relative, assets in parsed.items()}
    # A team-level copy of a return may have resolved its rows to another facility
    # than the copy filed under the facility folder (a template banner left in the
    # document), so such a copy is compared on its lines alone.
    lines_only: dict[str, Counter] = {}
    for relative, signature_counts in signatures.items():
        line_counts: Counter = Counter()
        for signature, count in signature_counts.items():
            line_counts[signature[:6]] += count
        lines_only[relative] = line_counts
    # Candidates share at least one distinctive line, so compare only within groups.
    by_line: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for relative, counter in signatures.items():
        for signature in counter:
            if signature[1] or signature[2] or signature[3]:
                by_line[signature].add(relative)
    neighbours: dict[str, set[str]] = defaultdict(set)
    for members in by_line.values():
        if 1 < len(members) <= 12:
            for member in members:
                neighbours[member] |= members - {member}

    def rank(relative: str) -> tuple:
        under_facility = "/_team-documents/" not in relative and "/_district-documents/" not in relative and not relative.startswith("_multi-team/")
        return (under_facility, len(parsed[relative]), -len(relative))

    def folder_key(relative: str) -> tuple[str, str] | None:
        parts = relative.split("/")
        if len(parts) >= 4 and parts[0].startswith("team-") and not parts[1].startswith("_") and not parts[2].startswith("_"):
            place = parts[2].replace("-", " ")
            return norm(parts[1]), facility_key(place, facility_kind(place))
        return None

    dropped: set[str] = set()
    # The same file name filed under a facility folder and again at team level is
    # one return saved twice; the copy filed under the facility is the one read.
    by_stem: dict[str, list[str]] = defaultdict(list)
    for relative in parsed:
        by_stem[norm(Path(relative).stem)].append(relative)
    for copies in by_stem.values():
        filed = [relative for relative in copies if folder_key(relative)]
        loose = [relative for relative in copies if not folder_key(relative) and "/_team-documents/" in relative]
        if filed and loose:
            for relative in loose:
                dropped.add(relative)
                notes.append(f"{relative}: {len(parsed[relative]):,} lines, the same file name is filed under {filed[0]}; that copy is read.")
    for smaller in sorted(parsed, key=rank):
        if smaller in dropped or len(parsed[smaller]) < 20:
            continue
        for larger in sorted(neighbours.get(smaller, ()), key=rank, reverse=True):
            if larger in dropped or rank(larger) <= rank(smaller):
                continue
            if folder_key(smaller) and folder_key(larger) and folder_key(smaller) != folder_key(larger):
                # The same lines filed under two facilities are two returns; both are kept.
                continue
            table = signatures if folder_key(smaller) else lines_only
            shared = sum(min(count, table[larger].get(signature, 0)) for signature, count in table[smaller].items())
            if shared >= 0.98 * len(parsed[smaller]):
                dropped.add(smaller)
                notes.append(f"{smaller}: {len(parsed[smaller]):,} lines, {shared:,} already in {larger}; read once.")
                break
    for relative in dropped:
        del parsed[relative]
    return notes


# Bump when source parsing/place resolution changes. Quantity reconciliation and
# workbook formatting changes do not invalidate the retained raw source rows.
PARSER_CACHE_VERSION = 2


def parsed_fingerprint(files: list[Path]) -> dict:
    source_paths = set(files)
    source_paths.update(GROUPED / relative for relative in (
        MDA_STATUS_REGISTER, MDA_CONSOLIDATION, *PROGRAMME_REGISTERS,
        *(relative for relative, _facility in INVENTORIES),
    ))
    dependencies = [
        Path(__file__).with_name("ugift_places.py"), RECONCILIATION,
        GROUPED / "supervisor-decisions.csv", TOOLKIT_ITEMS, ROOT / "Location(3)2.xlsx",
    ]
    return {
        "parser_version": PARSER_CACHE_VERSION,
        "sources": [
            (str(path.resolve()), path.stat().st_size, path.stat().st_mtime_ns)
            if path.exists() else (str(path.resolve()), None, None)
            for path in sorted(source_paths)
        ],
        "dependencies": [(str(path.resolve()), file_hash(path) if path.exists() else None) for path in dependencies],
    }


def parse_sources(files: list[Path], cache_path: Path | None = None) -> tuple[dict[str, list[Asset]], list[dict]]:
    """Optionally reuse an explicitly supplied, trusted local raw-parse cache."""
    fingerprint = parsed_fingerprint(files) if cache_path is not None else None
    if cache_path is not None and cache_path.exists():
        with cache_path.open("rb") as handle:
            cached = pickle.load(handle)
        if cached.get("fingerprint") == fingerprint:
            PLACE_NOTES.update(cached["place_notes"])
            SCOPE_NOTES.update(cached["scope_notes"])
            CENTRAL_NOTES.update(cached["central_notes"])
            print(f"Using validated raw-source checkpoint {cache_path}", flush=True)
            return {
                source: [Asset(**row) for row in rows]
                for source, rows in cached["parsed"].items()
            }, cached["source_audit"]
        print("Raw-source checkpoint does not match sources or parser version; reading sources again.", flush=True)
    parsed: dict[str, list[Asset]] = {}
    source_audit: list[dict] = []
    for path in files:
        relative = path.relative_to(GROUPED).as_posix()
        try:
            assets = read_workbook(path)
        except Exception as error:
            source_audit.append({"source_file": relative, "status": "error", "asset_rows": 0, "error": f"{type(error).__name__}: {error}"})
            print(f"SOURCE ERROR {relative}: {type(error).__name__}: {error}", flush=True)
            continue
        source_audit.append({"source_file": relative, "status": "parsed" if assets else "no_asset_rows", "asset_rows": len(assets), "error": ""})
        if not assets:
            continue
        parsed[relative] = assets
        print(f"{len(assets):6,}  {relative}", flush=True)
    for relative, assets in read_central_sources(source_audit).items():
        parsed[relative] = assets
        print(f"{len(assets):6,}  {relative}  (central government)", flush=True)
    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = cache_path.with_suffix(cache_path.suffix + ".tmp")
        with temporary.open("wb") as handle:
            pickle.dump({
                "fingerprint": fingerprint,
                "parsed": {source: [vars(asset) for asset in assets] for source, assets in parsed.items()},
                "source_audit": source_audit,
                "place_notes": dict(PLACE_NOTES), "scope_notes": dict(SCOPE_NOTES), "central_notes": dict(CENTRAL_NOTES),
            }, handle, protocol=pickle.HIGHEST_PROTOCOL)
        temporary.replace(cache_path)
        print(f"Saved raw-source checkpoint {cache_path}", flush=True)
    return parsed, source_audit


def main() -> None:
    global OUTPUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Output directory (defaults to outputs/asset-register-2026-09-23)")
    parser.add_argument("--parsed-cache", type=Path, help="Save/reuse this trusted local raw-parse checkpoint; source metadata and parser version must match")
    args = parser.parse_args()
    if args.out is not None:
        OUTPUT = args.out / OUTPUT.name
    check_examples()
    RECONCILED.update(reconciliation_sources())
    files = candidate_files()
    parsed, source_audit = parse_sources(files, args.parsed_cache)
    write_audit(OUTPUT.with_suffix(".source-audit.csv"), source_audit)
    print(f"Raw sources ready: {sum(len(rows) for rows in parsed.values()):,} rows in {len(parsed):,} returns", flush=True)
    zero_audit = exclude_reviewed_zero_rows(parsed)
    layout_audit = zero_audit + recover_standalone_count_rows(parsed)
    layout_summaries = [f"Reviewed zero quantity: {row['item']}, {row['source_file']} ({row['source_location']}). {row['reason']}"
                        for row in zero_audit]
    reviewed_layouts = []
    for source_assets in parsed.values():
        reviewed_layouts.extend(repair_nshwere_furniture(source_assets))
        reviewed_layouts.extend(repair_nyamarwa_air_conditioner(source_assets))
    reviewed_layouts.extend(repair_reviewed_unit_blocks(parsed))
    for summary in reviewed_layouts:
        layout_summaries.append(
            f"Reviewed source layout: {summary['source_file']} ({summary['source_location']}): "
            f"{summary['source_records']} parsed records reconciled into {summary['named_groups']} named groups "
            f"and {summary['physical_assets']} physical assets. {summary['reason']}"
        )
        status = "mixed_assets_recovered" if summary["named_groups"] > 1 else "source_layout_repaired"
        layout_audit.append({
            "source_file": summary["source_file"], "source_location": summary["source_location"],
            "item": ", ".join(summary["counts_by_item"]), "quantity": summary["physical_assets"],
            "status": "reviewed_unit_records" if summary.get("status") == "reviewed_unit_records" else status,
            "reason": summary["reason"] + "; counts: " + json.dumps(summary["counts_by_item"]),
        })
    write_audit(OUTPUT.with_suffix(".source-layout-audit.csv"), layout_audit)
    print(f"Source layout review complete: {len(layout_audit):,} audit entries", flush=True)
    # Source layout proof must be settled before counts enter duplicate signatures.
    for source_assets in parsed.values():
        mark_unit_records(source_assets)
    print("Source unit-record proofs complete; comparing duplicate returns", flush=True)
    duplicate_notes = drop_near_duplicates(parsed)
    for note in duplicate_notes:
        print("near duplicate:", note, flush=True)
    print(f"Duplicate-return review complete: {len(parsed):,} returns retained", flush=True)
    collected: list[Asset] = [asset for assets in parsed.values() for asset in assets]
    used: list[str] = [f"{relative} ({len(assets):,} source rows)" for relative, assets in parsed.items()]
    mark_unit_records(collected)
    collected, overlap_notes = union_facility_submissions(collected)
    print(f"Return reconciliation complete: {len(collected):,} source rows retained", flush=True)
    collected, unnamed_notes = settle_unnamed_lines(collected)
    overlap_notes = list(overlap_notes) + unnamed_notes + [f"Near-duplicate workbook left out: {note}" for note in duplicate_notes]
    overlap_notes.extend(layout_summaries)
    overlap_notes.append(
        f"Original DOCX table review recovered {sum(row['status'] == 'recovered' for row in layout_audit):,} "
        f"standalone named/count rows; {sum(row['status'] == 'skipped' for row in layout_audit):,} rows require "
        f"facility-context review. Evidence is in {OUTPUT.with_suffix('.source-layout-audit.csv').name}."
    )
    mirror_repairs = {(row['source_file'], row['source_location']) for row in layout_audit
                      if row['status'] == 'mirror_fragment_repaired'}
    if mirror_repairs:
        overlap_notes.append(
            f"Source-proven fragment corrections were also applied to {len(mirror_repairs):,} matching rows "
            "in other returns before reconciliation. Their raw source cells confirm the text was appended "
            "by parsing; no physical rows were added or removed from those returns."
        )
    source_errors = [row for row in source_audit if row["status"] in {"error", "missing"}]
    overlap_notes += [f"SOURCE {row['status'].upper()}: {row['source_file']}: {row['error']}" for row in source_errors]
    overlap_notes.append(
        f"Source coverage: {len(source_audit):,} selected files inspected; "
        f"{sum(row['status'] == 'parsed' for row in source_audit):,} supplied asset rows; "
        f"{sum(row['status'] == 'no_asset_rows' for row in source_audit):,} had no in-scope asset rows; "
        f"{len(source_errors):,} were missing or failed to parse. File-level outcomes are in {OUTPUT.with_suffix('.source-audit.csv').name}."
    )
    central = sorted(((vote, count) for vote, count in CENTRAL_NOTES.items() if not vote.startswith("(")), key=lambda item: -item[1])
    overlap_notes.append(
        "Central government: ministries, agencies and referral hospitals keep their UgIFT assets on their own votes and stay on the register. "
        "Their rows come from the ministries' verification returns (_multi-team/programme-documents/MDA status register.xlsx, one sheet per MDA), the programme's "
        "fixed-asset registers (fwdugiftassets/*.xls; a row located at a local government office is that government's asset and is left out: "
        f"{CENTRAL_NOTES['(local government offices, left out)']:,} lines), the Hoima and Arua regional blood-bank inventories (Uganda Blood Transfusion Services), "
        "and the hospital and district-inspectorate rows of UGiFT-WIP-consolidated-MDA-status-register.xlsx (MoH supplies to referral, national and general hospitals; "
        "MoES inspection tablets). The rest of that consolidation (local-government facility rows, programme supply lists, the ministries' ICT rows) is read from the team "
        f"folders and the ministries' own registers instead. Source lines by vote: " + "; ".join(f"{vote} {count:,}" for vote, count in central) + "."
    )
    overlap_notes += [f"Left out: {relative}. {reason}" for relative, reason in EXCLUDED_SOURCES.items()]
    overlap_notes += [f"Left out folder: {folder}/. {reason}" for folder, reason in EXCLUDED_FOLDERS.items()]
    if PLACE_NOTES:
        overlap_notes.append(
            f"Banner facility replaced by the filed facility of the same kind, or a facility moved to the local government "
            f"the reconciliation lists it under, on {sum(PLACE_NOTES.values()):,} rows in {len(PLACE_NOTES)} tables: "
            + "; ".join(sorted(PLACE_NOTES)[:12])
        )
    for relative, (dropped, total) in sorted(SCOPE_NOTES.items(), key=lambda item: -item[1][0]):
        overlap_notes.append(
            f"Out of scope: {relative}: {dropped:,} of {total:,} lines name no UgIFT health centre or seed school "
            "(district offices, sub-counties, primary schools, water schemes) and were left out."
        )
    audit_path = OUTPUT.with_suffix(".quantity-audit.csv")
    exploded = explode(collected, audit_path=audit_path)
    print(f"Quantity expansion complete: {len(exploded):,} physical asset rows", flush=True)
    quantity_audit = list(QUANTITY_AUDIT)
    for row in quantity_audit:
        evidence = json.loads(row["quantity_evidence"])
        decisions = [text for _, text in evidence if text.startswith("source count conflict:")]
        if decisions:
            totals = ", ".join(str(count) for count in sorted({count for count, _ in evidence}))
            overlap_notes.append(
                f"Reviewed source quantity conflict: {row['facility']}, {row['item']}, "
                f"{row['source_file']} ({row['source_location']}) states counts {totals}; "
                f"retained {row['output_rows']} physical assets. " + "; ".join(decisions)
            )
    layout_decisions = sorted({
        (row["facility"], row["source_file"], row["quantity_layout_evidence"])
        for row in quantity_audit if any(word in row["quantity_layout_evidence"].lower()
                                        for word in ("conflict", "identity uncertainty"))
    })
    overlap_notes.extend(f"Reviewed source layout conflict: {facility}, {source}. {evidence}"
                         for facility, source, evidence in layout_decisions)
    overlap_notes.append(
        f"Quantity reconciliation: {len(collected):,} retained source lines produced {len(exploded):,} asset rows; "
        f"the sum of per-line quantities is {sum(row['output_rows'] for row in quantity_audit):,}. "
        f"{sum(row['output_rows'] > 1 for row in quantity_audit):,} lines were expanded and "
        f"{sum(row['unit_record_proven'] for row in quantity_audit):,} source unit records retained one row. "
        f"Per-line count evidence, source file/location and price basis are in {audit_path.name}."
    )
    donors, donor_notes = template_donors()
    fill_within_facility(exploded, donors)
    overlap_notes += donor_notes
    overlap_notes.append(
        "Cells filled from another statement of the same fact (same facility, same item, every statement agreeing): "
        + ", ".join(f"{HEADER_OF_FIELD[name]} {count:,}" for name, count in sorted(FILL_NOTES.items(), key=lambda item: -item[1]))
        if FILL_NOTES else "No empty cell had another statement of the same fact to fill it."
    )
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
    print(f"sources with no in-scope asset rows: {sum(row['status'] == 'no_asset_rows' for row in source_audit)}; source errors/missing: {len(source_errors)}")


if __name__ == "__main__":
    main()
