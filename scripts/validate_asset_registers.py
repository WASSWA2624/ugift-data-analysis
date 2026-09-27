"""Read-only, streaming checks for the SK, MF and REF asset-register workbooks.

Run after all three build commands. Writes a compact JSON report and returns 1
when a definite rule violation is found. Source interpretation and donor choice
still require source review; the report explicitly separates those limitations
and permitted missing-cost exceptions from errors.

    python scripts/validate_asset_registers.py
    python scripts/validate_asset_registers.py --out path/to/registers --limit 6000

The optional limit is a smoke check only: it does not establish final row counts,
complete source groups, footer filters or the book-code index.
"""

from __future__ import annotations

import argparse
import json
import math
import posixpath
import re
import shutil
import time
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from itertools import zip_longest
from pathlib import Path
from zipfile import ZipFile
from xml.sax.saxutils import escape

from register_audits import read_audit_rows
from list_book_codes import book_code_index_counts

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "outputs" / "asset-register"
NAMES = {
    "SK": "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx",
    "MF": "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
    "REF": "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
}
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
SK_HEADERS = [
    "Equipment/Item", "Department", "Asset Number", "Item Description", "Life in Months",
    "Tag Number (engrave no.)", "Date Of Purchase", "Date Placed In Service", "Recoverable cost",
    "Cost", "Acc Dep Cost", "Net Book Value", "Ytd Deprn", "Equipment status", "Remarks",
    "Local Government", "Facility", "Facility type", "Unit", "Source file", "Source location",
]
ATTRIBUTE = {n: f"ATTRIBUTE{n}({('Equipment/ Item' if n == 1 else SK_HEADERS[n - 1])})" for n in range(1, 16)}
UNIT = re.compile(r"item (\d+) of (\d+)", re.I)
SUFFIX = re.compile(r"\s*\[(item \d+ of \d+)\]$", re.I)
PLACEHOLDER = re.compile(r"^(?:n/?a|nil+|none|null|-|not applicable)$", re.I)
BORROW_COLORS = {"9DC3E6", "F4B183", "C6EFCE"}
WHITE_COLORS = {None, "FFFFFF"}
MONEY_FORMAT = '#,##0.##;-#,##0.##;"-"'
MONEY = {"FIXED_ASSETS_COST", "SALVAGE_VALUE", "DEPRN_RESERVE", "YTD_DEPRN"} | {ATTRIBUTE[n] for n in (9, 10, 11, 12, 13)}
REQUIRED = {
    "ASSET_EXP_ACCT_FUND", "DEPRECIATE_FLAG", "LIFE_IN_MONTHS", "PRORATE_CONVENTION_CODE",
    "DEPRN_RESERVE", "YTD_DEPRN", "SALVAGE_VALUE", "TAG_NUMBER", "IN_USE_FLAG",
} | {ATTRIBUTE[n] for n in (1, 2, 3, 9, 10, 11, 12, 13, 14, 15)}
MIRRORS = {ATTRIBUTE[5]: "LIFE_IN_MONTHS", ATTRIBUTE[8]: "DATE_PLACED_IN_SERVICE",
           ATTRIBUTE[10]: "FIXED_ASSETS_COST", ATTRIBUTE[11]: "DEPRN_RESERVE", ATTRIBUTE[13]: "YTD_DEPRN"}
BORROW_NOTE = re.compile(r"\bborrow(?:ed|ing)?\b.{0,80}\b(?:cost|price|date|life)\b|"
                         r"\b(?:cost|price|date|life)\b.{0,80}\b(?:borrow(?:ed|ing)?|median|other local government)\b", re.I)


def column_index(reference: str) -> int:
    result = 0
    for letter in reference:
        if not letter.isalpha():
            break
        result = result * 26 + ord(letter.upper()) - 64
    return result - 1


def text(element: ET.Element | None) -> str:
    return "" if element is None else "".join(part.text or "" for part in element.iter(NS + "t"))


def number(value: object) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value) if math.isfinite(value) else None
    if isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        if re.fullmatch(r"-?\d+(?:\.\d+)?", cleaned):
            return float(cleaned)
    return None


def blank(value: object) -> bool:
    return value is None or value == ""


def equal(left: object, right: object) -> bool:
    """Allow whole-shilling rounding only for independently calculated amounts."""
    a, b = number(left), number(right)
    return abs(a - b) <= 1.01 if a is not None and b is not None else left == right


def same_value(left: object, right: object) -> bool:
    """Mapped values, dates and lives must retain their exact numeric value."""
    a, b = number(left), number(right)
    return a == b if a is not None and b is not None else left == right


def source_amount_equal(left: object, right: object) -> bool:
    """Ignore only insignificant Excel floating-point serialization differences."""
    a, b = number(left), number(right)
    return a is not None and b is not None and math.isclose(a, b, rel_tol=1e-14, abs_tol=1e-9)


def work_in_progress(source: dict, record: dict) -> bool:
    if record.get("ASSET_TYPE") == "CIP":
        return True
    wording = " ".join(str(source.get(name) or "") for name in ("Equipment/Item", "Item Description", "Equipment status", "Remarks"))
    building = record.get("ASSET_CATEGORY_MAJOR") == "BUILDINGS AND STRUCTURES" or bool(re.search(
        r"\b(?:buildings?|structures?|classrooms?|latrines?|toilets?|quarters?|dormitor(?:y|ies)|laborator(?:y|ies)|construction)\b", wording, re.I))
    unfinished = bool(re.search(
        r"\b(?:under\s+constr\w*|work\s+in\s+progress|wip|unfinished|incomplete|"
        r"not\s+(?:yet\s+)?(?:complete\w*|finished)|pending\s+completion|"
        r"ongoing|on[- ]going|construction\s+in progress)\b", wording, re.I))
    return building and unfinished


def check_source_amounts(source: dict, mf: dict, ref: dict, row: int, errors: "Findings", metrics: Counter):
    for source_column, targets in {
        "Cost": ("FIXED_ASSETS_COST", ATTRIBUTE[10]),
        "Acc Dep Cost": ("DEPRN_RESERVE", ATTRIBUTE[11]),
        "Ytd Deprn": ("YTD_DEPRN", ATTRIBUTE[13]),
        "Net Book Value": (ATTRIBUTE[12],),
        "Recoverable cost": (ATTRIBUTE[9],),
    }.items():
        original = number(source.get(source_column))
        if original is None:
            continue
        for target in targets:
            metrics["SK_MF_recorded_amount_checks"] += 1
            if not source_amount_equal(mf.get(target), original):
                errors.add("recorded_source_amount_changed", "MF", row, {"source_column": source_column, "column": target, "source": original, "actual": mf.get(target)})
    for primary, targets in {
        "DEPRN_RESERVE": ("DEPRN_RESERVE", ATTRIBUTE[11]),
        "YTD_DEPRN": ("YTD_DEPRN", ATTRIBUTE[13]),
        ATTRIBUTE[12]: (ATTRIBUTE[12],),
    }.items():
        original = number(mf.get(primary))
        if original is None:
            continue
        for target in targets:
            metrics["MF_REF_recorded_amount_checks"] += 1
            if not source_amount_equal(ref.get(target), original):
                errors.add("recorded_source_amount_changed", "REF", row, {"source_column": primary, "column": target, "source": original, "actual": ref.get(target)})


@dataclass(slots=True)
class Cell:
    value: object = None
    style: int = 0
    error: bool = False
    formula: bool = False


EMPTY = Cell()


class WorkbookReader:
    """Read XLSX rows without materializing worksheet XML or openpyxl cells."""

    def __init__(self, path: Path):
        self.path = path
        self.archive = ZipFile(path)
        self.shared: list[str] = []
        if "xl/sharedStrings.xml" in self.archive.namelist():
            with self.archive.open("xl/sharedStrings.xml") as stream:
                for _, node in ET.iterparse(stream, events=("end",)):
                    if node.tag == NS + "si":
                        self.shared.append(text(node))
                        node.clear()
        workbook = ET.fromstring(self.archive.read("xl/workbook.xml"))
        props = workbook.find(NS + "workbookPr")
        self.epoch = datetime(1904, 1, 1) if props is not None and props.get("date1904") in ("1", "true") else datetime(1899, 12, 30)
        relationships = ET.fromstring(self.archive.read("xl/_rels/workbook.xml.rels"))
        paths = {item.get("Id"): item.get("Target", "") for item in relationships}
        self.sheets = {}
        for sheet in workbook.find(NS + "sheets"):
            target = paths[sheet.get(REL_NS + "id")]
            self.sheets[sheet.get("name")] = target.lstrip("/") if target.startswith("/") else posixpath.normpath("xl/" + target)
        styles = ET.fromstring(self.archive.read("xl/styles.xml"))
        custom = {int(item.get("numFmtId")): item.get("formatCode") for item in styles.findall(NS + "numFmts/" + NS + "numFmt")}
        fills = []
        for item in styles.findall(NS + "fills/" + NS + "fill"):
            pattern = item.find(NS + "patternFill")
            foreground = None if pattern is None else pattern.find(NS + "fgColor")
            fills.append(foreground.get("rgb", "")[-6:] if foreground is not None and pattern.get("patternType") == "solid" else None)
        self.styles = []
        for item in styles.findall(NS + "cellXfs/" + NS + "xf"):
            fmt_id = int(item.get("numFmtId", 0))
            fmt = custom.get(fmt_id, "General")
            is_date = fmt_id in set(range(14, 23)) | {45, 46, 47} or bool(re.search(r"[yd]", re.sub(r'"[^"]*"|\[[^]]*\]', "", fmt), re.I))
            self.styles.append((fills[int(item.get("fillId", 0))], fmt, is_date))
        self.metadata: dict[str, dict] = {}

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.archive.close()

    def rows(self, name: str):
        metadata = self.metadata.setdefault(name, {})
        with self.archive.open(self.sheets[name]) as stream:
            parent = None
            for event, node in ET.iterparse(stream, events=("start", "end")):
                if event == "start":
                    if node.tag == NS + "sheetData":
                        parent = node
                    continue
                if node.tag == NS + "pane":
                    metadata["pane"] = dict(node.attrib)
                elif node.tag == NS + "autoFilter":
                    metadata["filter"] = node.get("ref")
                elif node.tag == NS + "cols":
                    metadata["column_widths"] = len(node)
                elif node.tag == NS + "row":
                    cells = []
                    for item in node:
                        if item.tag != NS + "c":
                            continue
                        index = column_index(item.get("r", "A1"))
                        cells.extend([EMPTY] * (index + 1 - len(cells)))
                        kind, style = item.get("t"), int(item.get("s", 0))
                        raw = item.findtext(NS + "v")
                        if kind == "inlineStr":
                            value = text(item.find(NS + "is"))
                        elif kind == "s":
                            value = self.shared[int(raw)] if raw is not None else None
                        elif kind == "d":
                            value = datetime.fromisoformat(raw).date() if raw else None
                        elif raw is None:
                            value = None
                        elif kind in ("str", "e"):
                            value = raw
                        else:
                            value = float(raw)
                            if self.styles[style][2]:
                                value = (self.epoch + timedelta(days=value)).date()
                            elif value.is_integer():
                                value = int(value)
                        cells[index] = Cell(value, style, kind == "e", item.find(NS + "f") is not None)
                    yield int(node.get("r", 0)), cells
                    node.clear()
                    if parent is not None:
                        parent.clear()


class Findings:
    def __init__(self):
        self.counts = Counter()
        self.examples = defaultdict(list)

    def add(self, rule: str, book: str, row: int | None, detail: object):
        key = f"{book}.{rule}"
        self.counts[key] += 1
        if len(self.examples[key]) < 8:
            self.examples[key].append({"row": row, "detail": detail})

    def as_dict(self):
        return {key: {"count": count, "examples": self.examples[key]} for key, count in sorted(self.counts.items())}


class QuantityAudit:
    """Reconcile each ordered retained source line with its exact SK unit block."""

    MONEY_FIELDS = {"line_cost": "Cost", "line_recoverable": "Recoverable cost", "line_acc_dep": "Acc Dep Cost",
                    "line_nbv": "Net Book Value", "line_ytd": "Ytd Deprn"}

    def __init__(self, path: Path, stack: ExitStack, errors: Findings, warnings: Findings, metrics: Counter):
        self.path, self.errors, self.warnings, self.metrics = path, errors, warnings, metrics
        self.reader = read_audit_rows(path, "quantity")
        self.current = None
        self.line_number = 1
        self.count = 0
        self.first_row = 0
        self.sums = Counter()
        self.filled = Counter()

    def next_source(self, row: int | None) -> dict | None:
        """Advance past excluded zero-output evidence without consuming an SK row."""
        for entry in self.reader:
            self.line_number += 1
            self.metrics["quantity_audit_source_lines_inspected"] += 1
            try:
                total = int(entry.get("output_rows", ""))
            except (TypeError, ValueError):
                total = -1
            if total < 0:
                self.metrics["quantity_audit_invalid_source_lines"] += 1
                self.errors.add("quantity_audit_invalid_quantity", "SK", row, {
                    "audit_line": self.line_number, "source": entry.get("source_file"),
                    "location": entry.get("source_location"), "output_rows": entry.get("output_rows"),
                    "reason": "Expected a nonnegative integer physical row count",
                })
                continue
            if total == 0:
                self.metrics["audited_zero_output_source_lines"] += 1
                continue
            return entry
        return None

    def take(self, sk: dict, row: int):
        if self.current is None:
            self.current = self.next_source(row)
            self.count, self.first_row, self.sums, self.filled = 0, row, Counter(), Counter()
            if self.current is None:
                self.errors.add("quantity_audit_exhausted", "SK", row, "No retained-source line accounts for this asset")
                return
            self.metrics["audited_retained_source_lines"] += 1
            if self.current.get("conflicting_counts", "").lower() == "true":
                self.warnings.add("conflicting_source_counts", "SK", row, {
                    "audit_line": self.line_number, "source": self.current.get("source_file"),
                    "location": self.current.get("source_location"), "evidence": self.current.get("quantity_evidence"),
                })
        entry = self.current
        total = int(entry["output_rows"])
        self.count += 1
        self.metrics["audited_physical_rows"] += 1
        expected_unit = f"item {self.count} of {total}" if total > 1 else ""
        if str(sk.get("Unit") or "") != expected_unit:
            self.errors.add("source_line_quantity_sequence", "SK", row, {"audit_line": self.line_number, "expected": expected_unit, "actual": sk.get("Unit")})
        for audit_column, sk_column in (("source_file", "Source file"), ("source_location", "Source location"), ("facility", "Facility")):
            actual = str(sk.get(sk_column) or "")
            expected = entry.get(audit_column, "")
            valid = actual == expected or (sk_column == "Source file" and actual.startswith(expected + "; "))
            if not valid:
                self.errors.add("source_line_audit_identity", "SK", row, {"audit_line": self.line_number, "column": sk_column, "expected": expected, "actual": actual})
        for audit_column, sk_column in self.MONEY_FIELDS.items():
            amount = number(sk.get(sk_column))
            if amount is not None:
                self.sums[audit_column] += amount
                self.filled[audit_column] += 1
        if self.count != total:
            return
        self.metrics["quantity_audit_expected_rows"] += total
        evidence = json.loads(entry.get("quantity_evidence") or "[]")
        unit_record = entry.get("unit_record_proven", "").lower() == "true"
        if unit_record:
            self.metrics["audited_existing_unit_records"] += 1
        elif evidence and max(int(value[0]) for value in evidence) > total:
            self.errors.add("stated_quantity_reduced", "SK", self.first_row, {"audit_line": self.line_number, "evidence": evidence, "actual": total})
        if total > 1 and any(value[1] != "quantity column" for value in evidence):
            self.metrics["audited_groups_with_quantity_outside_quantity_column"] += 1
        for audit_column, sk_column in self.MONEY_FIELDS.items():
            original = number(entry.get(audit_column))
            if original is None:
                continue  # Later fact filling may supply an originally empty amount.
            expected = original * total if audit_column == "line_cost" and entry.get("unit_cost", "").lower() == "true" else original
            self.metrics[f"source_line_{sk_column}_conservation_checks"] += 1
            tolerance = max(0.02, abs(expected) * 1e-10)
            if self.filled[audit_column] != total or abs(self.sums[audit_column] - expected) > tolerance:
                self.errors.add("source_line_money_conservation", "SK", self.first_row, {
                    "audit_line": self.line_number, "column": sk_column, "expected": expected,
                    "actual": self.sums[audit_column], "priced_units": self.filled[audit_column], "physical_units": total,
                })
        self.current = None

    def finish(self, limited: bool):
        if limited:
            return
        if self.current is not None:
            self.errors.add("source_line_quantity_incomplete", "SK", self.first_row, {"audit_line": self.line_number, "expected": self.current["output_rows"], "actual": self.count})
        remaining_lines = remaining_rows = 0
        while (entry := self.next_source(None)) is not None:
            remaining_lines += 1
            remaining_rows += int(entry["output_rows"])
        if remaining_lines:
            self.errors.add("quantity_audit_unexported_sources", "SK", None, {
                "source_lines": remaining_lines, "physical_rows": remaining_rows,
            })


def validate(args) -> dict:
    errors, warnings = Findings(), Findings()
    counts, metrics, filled_columns = Counter(), Counter(), defaultdict(Counter)
    groups, code_counts, vote_codes = {}, Counter(), defaultdict(set)
    started = time.monotonic()
    from ugift_places import resolve_lg  # Shared reference names, never builder/calculation functions.

    with ExitStack() as stack:
        audit = QuantityAudit(args.quantity_audit, stack, errors, warnings, metrics) if args.quantity_audit else None
        books = {key: stack.enter_context(WorkbookReader(args.out / name)) for key, name in NAMES.items()}
        sample = stack.enter_context(WorkbookReader(ROOT / "Sample Header of Asset Register..xlsx"))
        _, sample_row = next(sample.rows(next(iter(sample.sheets))))
        expected = [ATTRIBUTE.get(int(m.group(1)), c.value) if (m := re.fullmatch(r"ATTRIBUTE(\d+)", str(c.value))) else c.value for c in sample_row]
        streams, headers = {}, {}
        for key, book in books.items():
            if "Asset Register" not in book.sheets:
                raise ValueError(f"{book.path}: missing Asset Register sheet")
            streams[key] = book.rows("Asset Register")
            _, row = next(streams[key])
            headers[key] = [c.value for c in row]
            required = SK_HEADERS if key == "SK" else expected
            if headers[key] != required or len(required) != (21 if key == "SK" else 64):
                errors.add("headers", key, 1, {"actual": headers[key], "expected": required})
        index = {key: {name: n for n, name in enumerate(values)} for key, values in headers.items()}
        previous_sk = None
        limit_reached = False
        for ordinal, triple in enumerate(zip_longest(*(streams[key] for key in NAMES)), 1):
            if args.limit and ordinal > args.limit:
                limit_reached = True
                break
            rows, cells, values = {}, {}, {}
            for key, entry in zip(NAMES, triple):
                if entry is None:
                    continue
                rows[key], cells[key] = entry
                counts[key] += 1
                values[key] = {name: cells[key][n].value if n < len(cells[key]) else None for name, n in index[key].items()}
                filled_columns[key].update(name for name, value in values[key].items() if not blank(value))
                if not any(not blank(v) for v in values[key].values()):
                    errors.add("empty_asset_row", key, rows[key], "Blank row inside register")
            sk, mf, ref = (values.get(key, {}) for key in NAMES)
            unit = str(sk.get("Unit") or "")
            if sk:
                if audit:
                    audit.take(sk, rows["SK"])
                identity = tuple(sk.get(name) for name in SK_HEADERS[:18])
                if identity == previous_sk:
                    metrics["adjacent_identical_SK_assets_ignoring_Unit_and_provenance"] += 1
                previous_sk = identity
                if unit:
                    match = UNIT.fullmatch(unit)
                    if not match:
                        errors.add("unit_syntax", "SK", rows["SK"], unit)
                    else:
                        item, total = map(int, match.groups())
                        key = tuple(sk.get(name) for name in ("Source file", "Source location", "Local Government", "Facility", "Equipment/Item"))
                        if key not in groups:
                            groups[key] = {"total": total, "count": 0, "seen": bytearray((total + 7) // 8), "row": rows["SK"]}
                        group = groups[key]
                        group["count"] += 1
                        metrics["expanded_unit_rows"] += 1
                        if total != group["total"] or not 1 <= item <= total:
                            errors.add("unit_group_range", "SK", rows["SK"], unit)
                        else:
                            byte, bit = divmod(item - 1, 8)
                            if group["seen"][byte] & (1 << bit):
                                errors.add("unit_number_repeated", "SK", rows["SK"], {"unit": unit, "source": key})
                            group["seen"][byte] |= 1 << bit
            for key in ("MF", "REF"):
                if key not in values:
                    continue
                record, book, row_number = values[key], books[key], rows[key]
                def cell(name):
                    n = index[key].get(name, -1)
                    return cells[key][n] if 0 <= n < len(cells[key]) else EMPTY

                if record.get("FIXED_ASSETS_UNITS") != 1:
                    errors.add("one_asset_per_row", key, row_number, record.get("FIXED_ASSETS_UNITS"))
                description = str(record.get("DESCRIPTION") or "")
                actual_unit = SUFFIX.search(description)
                if (actual_unit.group(1).lower() if actual_unit else "") != unit.lower():
                    errors.add("unit_suffix_preserved", key, row_number, {"SK": unit, "description": description})
                remarks = str(record.get(ATTRIBUTE[15]) or "")
                for label in ("Source file", "Source location"):
                    source = re.sub(r"[\r\n]+", " ", str(sk.get(label) or "")).strip()
                    if source and f"{label}: {source}" not in remarks:
                        errors.add("source_provenance_preserved", key, row_number, label)
                condition = record.get(ATTRIBUTE[14])
                if condition not in ("Functional", "Faulty") or record.get("IN_USE_FLAG") != {"Functional": "YES", "Faulty": "NO"}.get(condition):
                    errors.add("condition_and_in_use", key, row_number, [condition, record.get("IN_USE_FLAG")])
                if blank(record.get("TAG_NUMBER")) or record.get("TAG_NUMBER") != record.get(ATTRIBUTE[6]):
                    errors.add("tag", key, row_number, [record.get("TAG_NUMBER"), record.get(ATTRIBUTE[6])])
                code, segment = str(record.get("BOOK_TYPE_CODE") or ""), str(record.get("LOCATION_SEGMENT1") or "")
                if not re.fullmatch(r"[A-Z][A-Z0-9 ]* BK", code) or re.search(r"\b(?:DISTRICT|DLG|LOCAL GOVERNMENT|\d+) BK$", code):
                    errors.add("book_code_format", key, row_number, code)
                if key == "REF":
                    code_counts[code] += 1
                    vote_codes[segment].add(code)
                lg = resolve_lg(str(sk.get("Local Government") or ""))
                if lg is None:
                    errors.add("unknown_vote", key, row_number, sk.get("Local Government"))
                elif code != lg.book_type_code or segment != lg.location_segment1:
                    errors.add("vote_mapping", key, row_number, {"code": code, "segment": segment, "expected": [lg.book_type_code, lg.location_segment1]})
                facility, kind = str(record.get("LOCATION_SEGMENT3") or ""), sk.get("Facility type")
                suffix = {"School": "Seed Secondary School", "Health centre": "Health Centre III"}.get(kind)
                if suffix and not facility.endswith(suffix):
                    errors.add("facility_suffix", key, row_number, facility)
                if kind not in {"School", "Health centre", "MDA", "Hospital", "Blood bank", "Local government office", "Health facility"}:
                    errors.add("facility_type", key, row_number, kind)
                if record.get("DEPRECIATE_FLAG") == "YES":
                    for name in ("DEPRN_METHOD_CODE", "PRORATE_CONVENTION_CODE", "SALVAGE_VALUE"):
                        if blank(record.get(name)):
                            errors.add("depreciation_input", key, row_number, name)
                    if record.get("DEPRN_METHOD_CODE") != "STL" or (number(record.get("LIFE_IN_MONTHS")) or 0) < 12:
                        errors.add("depreciation_method_and_life", key, row_number, [record.get("DEPRN_METHOD_CODE"), record.get("LIFE_IN_MONTHS")])
                if BORROW_NOTE.search(remarks.partition("Source file:")[0]):
                    warnings.add("review_borrowing_wording_in_remarks", key, row_number, remarks[:250])
                for name, value in record.items():
                    selected = cell(name)
                    if selected.error or selected.formula and blank(value):
                        errors.add("excel_error_or_uncached_formula", key, row_number, name)
                    if isinstance(value, str):
                        # Source paths are preserved exactly, even if a filename has two spaces.
                        cleaned = value.partition("Source file:")[0].rstrip() if name == ATTRIBUTE[15] else value
                        if cleaned != cleaned.strip() or re.search(r"\s{2,}|[\r\n]", cleaned):
                            errors.add("text_whitespace", key, row_number, {"column": name, "value": cleaned[:160]})
                        if PLACEHOLDER.fullmatch(value):
                            errors.add("placeholder", key, row_number, {"column": name, "value": value})
                    if name in MONEY and isinstance(value, (int, float)) and book.styles[selected.style][1] != MONEY_FORMAT:
                        errors.add("amount_format", key, row_number, name)
                if key != "REF":
                    continue
                cost = number(record.get("FIXED_ASSETS_COST"))
                cost_missing = cost is None
                if cost_missing:
                    warnings.add("no_comparable_cost_exception", key, row_number, description)
                for name in REQUIRED:
                    if blank(record.get(name)):
                        if cost_missing and name in {ATTRIBUTE[n] for n in (9, 10, 12)}:
                            warnings.add("missing_cost_dependent_value", key, row_number, name)
                        else:
                            errors.add("required_value", key, row_number, name)
                if blank(record.get("DATE_PLACED_IN_SERVICE")):
                    if work_in_progress(sk, record):
                        metrics["WIP_blank_date_exceptions"] += 1
                    else:
                        errors.add("required_date", key, row_number, description)
                if 0 < (cost or 0) < 10000:
                    errors.add("immaterial_cost_not_zero", key, row_number, cost)
                if cost == 0 and record.get("ASSET_TYPE") == "CAPITALIZED":
                    errors.add("nil_cost_capitalized", key, row_number, description)
                for attribute, primary in MIRRORS.items():
                    if not same_value(record.get(attribute), record.get(primary)) or book.styles[cell(attribute).style][0] != book.styles[cell(primary).style][0]:
                        errors.add("finished_value_mirror", key, row_number, {"column": attribute, "primary": primary})
                for name in ("FIXED_ASSETS_COST", "LIFE_IN_MONTHS", "DATE_PLACED_IN_SERVICE"):
                    color = book.styles[cell(name).style][0]
                    if color not in WHITE_COLORS | BORROW_COLORS:
                        errors.add("borrow_cell_color", key, row_number, {"column": name, "color": color})
                    if color in BORROW_COLORS:
                        metrics[f"borrowed_{name}_{color}"] += 1
                # Borrowed prices must be colored unless the immaterial-cost rule zeroed them.
                if cost and (blank(mf.get("FIXED_ASSETS_COST")) or not source_amount_equal(cost, mf.get("FIXED_ASSETS_COST"))):
                    if book.styles[cell("FIXED_ASSETS_COST").style][0] not in BORROW_COLORS:
                        errors.add("changed_cost_without_color", key, row_number, cost)
                if ordinal <= 2000 or ordinal % 997 == 0:
                    check_calculation(record, mf, row_number, errors, metrics, sk)
            if mf and ref:
                check_source_amounts(sk, mf, ref, rows["REF"], errors, metrics)
                for name in ("BOOK_TYPE_CODE", "DESCRIPTION", "ASSET_NUMBER", "TAG_NUMBER", ATTRIBUTE[1], ATTRIBUTE[3], ATTRIBUTE[14], ATTRIBUTE[15]):
                    if mf.get(name) != ref.get(name):
                        errors.add("MF_REF_identity_preserved", "REF", rows["REF"], name)
            if ordinal % 50000 == 0:
                print(f"validated {ordinal:,} aligned rows ({time.monotonic() - started:.1f}s)", flush=True)

        if len(set(counts.values())) != 1 or len(counts) != 3:
            errors.add("row_count_match", "ALL", None, dict(counts))
        if audit:
            audit.finish(limit_reached)
        for source, group in groups.items():
            if group["count"] != group["total"]:
                target = warnings if limit_reached else errors
                target.add("incomplete_unit_group", "SK", group["row"], {"expected": group["total"], "actual": group["count"], "source": source})
        metrics["expanded_source_groups"] = len(groups)
        metrics["source_groups_above_500"] = sum(group["total"] > 500 for group in groups.values())
        metrics["largest_source_quantity"] = max((group["total"] for group in groups.values()), default=0)
        for segment, codes in vote_codes.items():
            if len(codes) != 1:
                errors.add("one_code_per_vote", "REF", None, {"segment": segment, "codes": sorted(codes)})
        for key, book in books.items():
            meta = book.metadata["Asset Register"]
            if meta.get("pane", {}).get("topLeftCell") != "A2" or meta.get("pane", {}).get("state") not in ("frozen", "frozenSplit"):
                errors.add("frozen_header", key, 1, meta.get("pane"))
            if not meta.get("column_widths"):
                errors.add("column_widths", key, 1, meta)
            if not limit_reached:
                expected_filter = f"A1:{'U' if key == 'SK' else 'BL'}{counts[key] + 1}"
                if meta.get("filter") != expected_filter:
                    errors.add("header_filter", key, 1, {"actual": meta.get("filter"), "expected": expected_filter})
            if "Read Me" not in book.sheets:
                errors.add("read_me", key, None, "Missing Read Me sheet")
            else:
                notes = "\n".join(str(c.value or "") for _, row in book.rows("Read Me") for c in row)
                if not re.search(r"(?:quantit|physical|unit row|one.row.per)", notes, re.I):
                    warnings.add("read_me_quantity_checks", key, None, "No quantity/unit validation statement found")
                if not re.search(r"(?:check|validat|reconcil)", notes, re.I):
                    warnings.add("read_me_rule_checks", key, None, "No validation/check statement found")
                if re.search(r"numbers above 500|2 to 500|at most 500", notes, re.I):
                    errors.add("obsolete_quantity_limit", key, None, "Read Me still documents a maximum quantity of 500")
                if key != "SK" and not limit_reached:
                    for name in headers[key]:
                        if not filled_columns[key][name] and name not in notes:
                            errors.add("all_blank_column_reason", key, None, name)
        if not limit_reached:
            index_path = args.out / "README.md"
            if index_path.exists():
                try:
                    index_counts = book_code_index_counts(index_path.read_text(encoding="utf-8"))
                except ValueError as error:
                    errors.add("book_code_index", "ALL", None, str(error))
                else:
                    if index_counts != code_counts:
                        errors.add("book_code_index", "ALL", None, {"missing_or_wrong": dict(code_counts - index_counts), "extra_or_wrong": dict(index_counts - code_counts)})
            else:
                errors.add("book_code_index", "ALL", None, "Missing README.md book-code index")
    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(), "directory": str(args.out.resolve()),
        "scope": "limited smoke check" if limit_reached else "full workbook scan",
        "quantity_audit": str(args.quantity_audit.resolve()) if args.quantity_audit else None,
        "passed": not errors.counts, "duration_seconds": round(time.monotonic() - started, 2),
        "row_counts": dict(counts), "metrics": dict(metrics),
        "errors": errors.as_dict(), "review_notes": warnings.as_dict(),
        "limitations": [
            "A complete Unit sequence proves the exported group is intact, not that an unexpanded raw quantity was interpreted correctly.",
            ("Retained-source quantities and original monetary totals were reconciled to ordered SK blocks using the quantity audit; source interpretation, retained-return choice and donor selection still need source review."
             if args.quantity_audit else "Source quantity interpretation, retained-return choice, per-unit line-total reconciliation and donor selection need source-level audits."),
            "Missing costs and dependent carrying amounts are review notes only because the prompt permits assets with no comparable price.",
            "Depreciation checks use independently recomputed deterministic samples, including measured uncapitalized rows with unambiguous source existence; ambiguous existence is counted as skipped. Recorded source reserve, YTD and NBV are checked for preservation on every row.",
            "Vote spelling uses the shared reference-name resolver; visual layout and ambiguous source remarks need independent review.",
        ],
    }


def check_calculation(ref: dict, mf: dict, row: int, errors: Findings, metrics: Counter, source: dict | None = None):
    cost, salvage, life = (number(ref.get(name)) for name in ("FIXED_ASSETS_COST", "SALVAGE_VALUE", "LIFE_IN_MONTHS"))
    placed = ref.get("DATE_PLACED_IN_SERVICE")
    reserve = number(ref.get("DEPRN_RESERVE"))
    if cost is not None and reserve is not None and salvage is not None and blank(mf.get(ATTRIBUTE[12])):
        metrics["independent_NBV_checks"] += 1
        if not equal(ref.get(ATTRIBUTE[12]), max(salvage, cost - reserve)):
            errors.add("NBV_calculation", "REF", row, {"cost": cost, "reserve": reserve, "actual": ref.get(ATTRIBUTE[12])})
    if ref.get("DEPRECIATE_FLAG") != "YES" or not isinstance(placed, date) or None in (cost, salvage, life) or life <= 0:
        return
    if ref.get("ASSET_TYPE") != "CAPITALIZED":
        source = source or {}
        existence_wording = " ".join(str(source.get(name) or "") for name in ("Equipment status", "Remarks"))
        # Detailed lost/stolen group wording may refer to only part of a group or
        # to another item. Skip ambiguous samples instead of independently
        # guessing existence; measured generic rows with clear evidence are checked.
        if re.search(r"\b(?:not|never|unable|missing|lost|stolen|disposed|condemned|unverified|written\s+off|could)\b", existence_wording, re.I):
            metrics["depreciation_samples_skipped_ambiguous_existence"] += 1
            return
        metrics["uncapitalized_depreciation_samples"] += 1
    start = placed.year * 12 + placed.month - 1
    finish, fy_start = 2026 * 12 + 8, 2026 * 12 + 6
    monthly = max(0, cost - salvage) / life
    accumulated = monthly * min(life, max(0, finish - start + 1))
    ytd = monthly * max(0, min(finish, start + life - 1) - max(fy_start, start) + 1)
    if blank(mf.get("DEPRN_RESERVE")):
        metrics["independent_reserve_checks"] += 1
        if not equal(ref.get("DEPRN_RESERVE"), accumulated):
            errors.add("reserve_calculation", "REF", row, {"actual": ref.get("DEPRN_RESERVE"), "expected": accumulated})
    elif reserve is not None:
        ytd = min(ytd, max(0, cost - salvage - reserve))
    if blank(mf.get("YTD_DEPRN")):
        metrics["independent_YTD_checks"] += 1
        if not equal(ref.get("YTD_DEPRN"), ytd):
            errors.add("YTD_calculation", "REF", row, {"actual": ref.get("YTD_DEPRN"), "expected": ytd})


def record_read_me(directory: Path, result: dict, report_path: Path):
    """Append actual check outcomes without loading or reserializing asset sheets.

    Asset-sheet XML and existing styles are preserved. A plain wrapped style is
    appended only if none exists. An earlier report from this validator is
    replaced, so repeat runs are tidy.
    """
    marker = "Asset-register validation | "
    metrics = result["metrics"]
    outcomes = [
        f"{result['scope']} at {result['generated_utc']}: "
        + ("PASS" if result["passed"] else "FAIL — see the detailed report and findings below"),
        "Rows inspected: " + "; ".join(f"{key} {value:,}" for key, value in result["row_counts"].items()),
        "Checks run: sample headers/order; one unit per MF/REF row; source provenance and row identity across stages; "
        "complete SK Unit sequences; vote mapping; facility suffixes; condition/use flags; tags; required values; "
        "text sanitation; amount formats; borrowed-cell colors; MF/REF mirrors; frozen header and column widths. "
        + ("Full-scan checks also covered row totals, filters and the README.md book-code index." if result["scope"] == "full workbook scan" else
           "This was a limited smoke check; complete row totals, unfinished quantity groups, filters and the README.md book-code index are not certified."),
        f"Expanded source groups inspected: {metrics.get('expanded_source_groups', 0):,}; "
        f"unit rows: {metrics.get('expanded_unit_rows', 0):,}; groups above 500: {metrics.get('source_groups_above_500', 0):,}; "
        f"largest stated Unit group: {metrics.get('largest_source_quantity', 0):,}. "
        f"Adjacent duplicate-looking SK asset rows retained: {metrics.get('adjacent_identical_SK_assets_ignoring_Unit_and_provenance', 0):,}.",
        "Independent calculations checked after REF borrowing: "
        f"reserve {metrics.get('independent_reserve_checks', 0):,}; YTD {metrics.get('independent_YTD_checks', 0):,}; "
        f"NBV {metrics.get('independent_NBV_checks', 0):,}; uncapitalized depreciation samples {metrics.get('uncapitalized_depreciation_samples', 0):,}; "
        f"samples skipped for ambiguous existence {metrics.get('depreciation_samples_skipped_ambiguous_existence', 0):,}. "
        f"Recorded-amount comparisons: SK to MF {metrics.get('SK_MF_recorded_amount_checks', 0):,}; "
        f"MF to REF {metrics.get('MF_REF_recorded_amount_checks', 0):,}. Recorded source depreciation and NBV remain authoritative.",
        "Detailed report: " + report_path.name,
    ]
    for key, finding in result["errors"].items():
        outcomes.append(f"Failed rule: {key}; {finding['count']:,} findings. Examples are in the JSON report.")
    for key, finding in result["review_notes"].items():
        outcomes.append(f"Review note: {key}; {finding['count']:,} occurrences. These are not silently treated as passed rules.")
    outcomes.extend("Scope limitation: " + line for line in result["limitations"])
    outcomes.extend("Independent review: " + line for line in result.get("independent_reviews", []))
    if result.get("quantity_audit"):
        outcomes.append(
            f"Quantity audit reconciled against SK before borrowing: {metrics.get('audited_retained_source_lines', 0):,} retained source lines; "
            f"{metrics.get('audited_zero_output_source_lines', 0):,} excluded zero-output evidence lines; "
            f"{metrics.get('audited_physical_rows', 0):,} physical rows; {metrics.get('audited_existing_unit_records', 0):,} existing unit records; "
            f"{metrics.get('audited_groups_with_quantity_outside_quantity_column', 0):,} groups with count evidence outside the quantity column. "
            "Monetary checks: " + "; ".join(f"{key.removeprefix('source_line_').removesuffix('_conservation_checks')} {count:,}"
                                            for key, count in metrics.items() if key.startswith("source_line_") and key.endswith("_conservation_checks"))
        )
    for name in NAMES.values():
        path = directory / name
        if path.with_name("~$" + path.name).exists():
            raise RuntimeError(f"Close the workbook before recording its validation: {path}")
        with WorkbookReader(path) as book:
            if "Read Me" not in book.sheets:
                raise ValueError(f"Cannot append validation: {path} has no Read Me sheet")
            target = book.sheets["Read Me"]
            xml = book.archive.read(target).decode("utf-8")
            style_xml = book.archive.read("xl/styles.xml").decode("utf-8")
        style_root = ET.fromstring(style_xml)
        formats = style_root.find(NS + "cellXfs")
        if formats is None:
            raise ValueError(f"Cannot style validation notes: {path} has no cellXfs")
        wrap_style = None
        for index, style in enumerate(formats):
            alignment = style.find(NS + "alignment")
            if style.get("fontId", "0") == "0" and style.get("fillId", "0") == "0" \
                    and style.get("numFmtId", "0") == "0" and alignment is not None \
                    and alignment.get("wrapText") in ("1", "true"):
                wrap_style = index
                break
        style_changed = wrap_style is None
        if style_changed:
            wrap_style = len(formats)
            if "</cellXfs>" not in style_xml:
                raise ValueError(f"Unsupported cell style XML in {path}")
            new_style = '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'
            style_xml = style_xml.replace("</cellXfs>", new_style + "</cellXfs>", 1)
            style_xml = re.sub(r'(<cellXfs\b[^>]*\bcount=")\d+("[^>]*>)',
                               lambda match: match.group(1) + str(wrap_style + 1) + match.group(2), style_xml, count=1)
        # Existing validators always produce inline-string rows with this prefix.
        xml = re.sub(r"<row\b[^>]*>.*?</row>", lambda match: "" if marker in match.group(0) else match.group(0), xml, flags=re.S)
        last = max((int(value) for value in re.findall(r'<row\b[^>]*\br="(\d+)"', xml)), default=0)
        additions = []
        for offset, line in enumerate(outcomes, 1):
            row = last + offset
            height = min(409, max(30, (math.ceil(len(marker + line) / 105) + 1) * 15))
            additions.append(f'<row r="{row}" ht="{height}" customHeight="1"><c r="A{row}" s="{wrap_style}" t="inlineStr"><is><t>{escape(marker + line)}</t></is></c></row>')
        if "</sheetData>" not in xml:
            raise ValueError(f"Unsupported Read Me XML in {path}")
        xml = xml.replace("</sheetData>", "".join(additions) + "</sheetData>", 1)
        xml = re.sub(r'<dimension\b[^>]*/>', f'<dimension ref="A1:A{last + len(outcomes)}"/>', xml, count=1)
        temporary = path.with_name(path.name + ".validation.tmp")
        try:
            with ZipFile(path) as source, ZipFile(temporary, "w") as destination:
                for member in source.infolist():
                    if member.filename == target:
                        destination.writestr(member, xml.encode("utf-8"))
                    elif member.filename == "xl/styles.xml" and style_changed:
                        destination.writestr(member, style_xml.encode("utf-8"))
                    else:
                        with source.open(member) as incoming, destination.open(member, "w") as outgoing:
                            shutil.copyfileobj(incoming, outgoing, length=1024 * 1024)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
        print(f"Recorded validation on {path.name}: Read Me", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Directory containing all three workbooks")
    parser.add_argument("--report", type=Path, help="JSON destination; default: <out>/validation-report.json")
    parser.add_argument("--limit", type=int, help="Smoke-check this many aligned rows; not final validation")
    parser.add_argument("--quantity-audit", type=Path, help="Stage 1 asset-register-audits.json.gz (or legacy quantity-audit CSV), for row and pre-borrow monetary reconciliation")
    parser.add_argument("--record-read-me", action="store_true", help="Record actual check outcomes on each Read Me after validation")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    result = validate(args)
    destination = args.report or args.out / "validation-report.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    if args.record_read_me:
        record_read_me(args.out, result, destination)
    print(json.dumps({key: result[key] for key in ("scope", "passed", "duration_seconds", "row_counts", "metrics")}, indent=2))
    print(f"Rule failures: {sum(value['count'] for value in result['errors'].values()):,}; report: {destination}")
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
