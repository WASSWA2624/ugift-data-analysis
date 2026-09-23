"""Repair BOOK_TYPE_CODE and FACILITY_NAME in the UgIFT asset register.

The resolver follows a strict evidence order:

1. reconciled facility ID;
2. reconciled facility folder/source path;
3. the source-line LG and facility fields;
4. the exact worksheet row named by ``Source locator`` (including section
   headers and carried-down district/facility columns);
5. a facility/LG explicitly present in the source description;
6. the owning district or MDA when the source is an entity-wide register.

Unsupported values remain blank. The script rebuilds from the committed
workbook when requested, inserts FACILITY_NAME beside BOOK_TYPE_CODE, and
keeps the native Excel table metadata synchronized with the worksheet.
"""

from __future__ import annotations

import argparse
import csv
import io
import math
import re
import subprocess
from collections import Counter, defaultdict
from copy import copy
from dataclasses import dataclass
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Iterable, Iterator

import xlrd
from docx import Document
from openpyxl import load_workbook
from openpyxl.formula.translate import Translator
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import TableColumn

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = ROOT / "outputs" / "asset-register-2026-09-22" / "UgIFT Asset Register.xlsx"
RECONCILIATION_PATH = ROOT / "raw-data-grouped" / "facility-reconciliation.csv"
LOCATION_MASTER_PATH = ROOT / "Location(3)2.xlsx"
GIT_WORKBOOK_PATH = "outputs/asset-register-2026-09-22/UgIFT Asset Register.xlsx"
ORIGINAL_REGISTER_ASSET_ROWS = 226_705
INVALID_FACILITY_STATUSES = {"Reported absent", "No UgIFT assets", "Outside UgIFT", "Replaced"}
LATEST_ROOT = ROOT / "new-raw-data-221092026-1114" / "new-raw-data-22092026-1556"
LATEST_WESTERN_PATH = LATEST_ROOT / "DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT.xls"
LATEST_LWAMATA_PATH = LATEST_ROOT / "UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH (1).docx"
LATEST_SOFIA_PATH = LATEST_ROOT / "Sofia health centre 111 eastern division busia MC.pdf"
LATEST_WESTERN_SOURCE = "_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls"
LATEST_LWAMATA_SOURCE = "team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH (1).docx"
LATEST_SOFIA_SOURCE = "team-13/Busia MC/Sofia-Health-Centre-III/Sofia health centre 111 eastern division busia MC.pdf"
LATEST_MAKOKOTO_SOURCE = "team-30/_team-documents/MAKOKOTO SEED SCHOOL UGIFT ASSET VERIFICATION TOOLKIT - FINAL - 1.docx"
LATEST_NYAMARWA_SOURCE = "team-30/_team-documents/NYAMARWA SEED SCHOOL UGIFT ASSET VERIFICATION AND RECORDING TOOL KIT - FINAL.docx"
LATEST_MAKOKOTO_PATH = ROOT / "raw-data-grouped" / LATEST_MAKOKOTO_SOURCE
LATEST_NYAMARWA_PATH = ROOT / "raw-data-grouped" / LATEST_NYAMARWA_SOURCE
LATEST_SOURCE_FILES = {
    LATEST_WESTERN_SOURCE,
    LATEST_LWAMATA_SOURCE,
    LATEST_SOFIA_SOURCE,
    LATEST_MAKOKOTO_SOURCE,
    LATEST_NYAMARWA_SOURCE,
}

SOURCE_LOCATOR_RE = re.compile(
    r"^Worksheet\s+(.*?),\s*rows?\s+(\d+)(?:\s*-\s*\d+)?\s*$", re.I
)
LG_PREFIX_RE = re.compile(
    r"^(.*?(?:DISTRICT LOCAL GOV'?T|MUNICIPAL COUNCIL|CITY COUNCIL|DISTRICT LG|\sDLG|\sMC|\sCITY))(?=-)",
    re.I,
)

MDA_NAMES = {
    "MAAIF": "Ministry of Agriculture, Animal Industry and Fisheries",
    "MOES": "Ministry of Education and Sports",
    "MOFPED": "Ministry of Finance, Planning and Economic Development",
    "MOGLSD": "Ministry of Gender, Labour and Social Development",
    "MOH": "Ministry of Health",
    "MOLG": "Ministry of Local Government",
    "MOWE": "Ministry of Water and Environment",
    "MOWT": "Ministry of Works and Transport",
    "NEMA": "National Environment Management Authority",
    "OAG": "Office of the Auditor General",
    "OPM": "Office of the Prime Minister",
    "PPDA": "Public Procurement and Disposal of Public Assets Authority",
}

MDA_TEXT_MARKERS = (
    ("ministry of agriculture animal industry and fisheries", "MAAIF"),
    ("ministry of education and sports", "MOES"),
    ("ministry of finance planning and economic development", "MOFPED"),
    ("ministry of gender labour and social development", "MOGLSD"),
    ("ministry of health", "MOH"),
    ("ministry of local government", "MOLG"),
    ("ministry of water and environment", "MOWE"),
    ("ministry of works and transport", "MOWT"),
    ("office of the auditor general", "OAG"),
    ("office of the prime minister", "OPM"),
    ("national environment management authority", "NEMA"),
    ("public procurement and disposal of public assets authority", "PPDA"),
)

LG_ALIASES = {
    "amolata": "amolatar",
    "buyend": "buyende",
    "fortportal city": "fort portal city",
    "kabalore": "kabarole",
    "kakumuro": "kakumiro",
    "kyakwanzi": "kyankwanzi",
    "kyankwazi": "kyankwanzi",
    "lira disrict": "lira",
    "liras city": "lira city",
    "nebbi municipality": "nebbi mc",
    "ssembabule": "sembabule",
}

INVALID_LG_KEYS = {
    "central",
    "district",
    "eastern",
    "not allocated",
    "northern",
    "unspecified",
    "western",
}

FACILITY_MARKERS = re.compile(
    r"\b(?:HC\s*(?:II|III|IV|2|3|4|111|LLL)|HEALTH\s*CENT(?:RE|ER)|"
    r"HOSPITAL|BLOOD\s*BANK|SEED\s*(?:SECONDARY\s*)?SCHOOL|SECONDARY\s*SCHOOL)\b",
    re.I,
)

RAW_FACILITY_RE = re.compile(
    r"\b([A-Z][A-Z0-9 .&'()-]{1,55}?\s+(?:HC\s*(?:II|III|IV|2|3|4|111|LLL)|"
    r"HEALTH\s*CENT(?:RE|ER)(?:\s*(?:II|III|IV|2|3|4))?|BLOOD\s*BANK|"
    r"SEED\s*(?:SECONDARY\s*)?SCHOOL|SECONDARY\s*SCHOOL|HOSPITAL))\b",
    re.I,
)


def clean_text(value: object) -> str:
    """Return readable text without spreadsheet escape and ellipsis noise."""
    if value is None:
        return ""
    text = str(value).replace("\xa0", " ").replace("\\", "")
    text = re.sub(r"[…]+", " ", text)
    return re.sub(r"\s+", " ", text).strip(" \t\r\n-–—|,;:")


def normalized_key(value: object) -> str:
    text = clean_text(value).casefold().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def normalized_path(value: str) -> str:
    return "/".join(
        normalized_key(part)
        for part in value.replace("\\", "/").split("/")
        if part
    )


def lg_key(value: object) -> str:
    text = normalized_key(value)
    text = re.sub(r"\b(?:district local government|district local govt|local government)\b", " ", text)
    text = re.sub(r"\bdistrict\b", " ", text)
    text = re.sub(r"\bdlg\b", " ", text)
    text = re.sub(r"\bmunicipal(?:ity| council)?\b", " mc ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return LG_ALIASES.get(text, text)


def facility_key(value: object) -> str:
    text = normalized_key(value)
    text = re.sub(r"\bhealth\s*cent(?:re|er)\b", " hc ", text)
    text = re.sub(r"\b(?:h\s*c)\s*(?:111|lll|3)\b", " hc iii ", text)
    text = re.sub(r"\b(?:h\s*c)\s*(?:11|2)\b", " hc ii ", text)
    text = re.sub(r"\b(?:h\s*c)\s*(?:1v|4)\b", " hc iv ", text)
    text = re.sub(r"\bsecondary\s+school\b", " ss ", text)
    text = re.sub(r"\bincharge\b", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def mda_from_text(value: object) -> str | None:
    key = normalized_key(value)
    for marker, code in MDA_TEXT_MARKERS:
        if marker in key:
            return code
    return None


def format_raw_facility(value: object) -> str | None:
    """Extract a readable facility name from a tag, user title, or heading."""
    text = clean_text(value)
    for segment in re.split(r"[/|]", text):
        match = RAW_FACILITY_RE.search(clean_text(segment))
        if not match:
            continue
        facility = re.sub(r"\bINCHARGE\b.*$", "", match.group(1), flags=re.I).strip()
        facility = facility.title()
        facility = re.sub(r"\bHc\s*(?:111|Lll|3|Iii)\b", "HC III", facility, flags=re.I)
        facility = re.sub(r"\bHc\s*(?:11|2|Ii)\b", "HC II", facility, flags=re.I)
        facility = re.sub(r"\bHc\s*(?:1v|4|Iv)\b", "HC IV", facility, flags=re.I)
        return facility
    return None


@dataclass(frozen=True)
class Facility:
    name: str
    lg: str


@dataclass(frozen=True)
class Resolution:
    lg: str | None
    facility: str | None
    lg_rule: str
    facility_rule: str


class MasterData:
    """Canonical LG/facility names and their supported aliases."""

    def __init__(self) -> None:
        self.facility_by_id: dict[str, Facility] = {}
        self.status_by_id: dict[str, str] = {}
        self.invalid_facility_ids: set[str] = set()
        self.folder_to_facility: dict[str, Facility] = {}
        self.lg_display: dict[str, str] = {}
        self.facility_aliases_by_lg: dict[str, dict[str, Facility]] = defaultdict(dict)
        self.global_facility_aliases: dict[str, list[Facility]] = defaultdict(list)
        self._load_location_master()
        self._load_reconciliation()
        self._lg_search = sorted(self.lg_display, key=len, reverse=True)

    def _remember_lg(self, value: object, *, prefer: bool = False) -> str:
        display = clean_text(value)
        key = lg_key(display)
        if key and (prefer or key not in self.lg_display):
            self.lg_display[key] = display
        return key

    def _load_location_master(self) -> None:
        workbook = load_workbook(LOCATION_MASTER_PATH, read_only=True, data_only=True)
        sheet = workbook.active
        for (value,) in sheet.iter_rows(min_row=2, values_only=True):
            match = LG_PREFIX_RE.search(clean_text(value))
            if match:
                self._remember_lg(match.group(1), prefer=True)
        workbook.close()

    def _load_reconciliation(self) -> None:
        with RECONCILIATION_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                facility_id = clean_text(row.get("id"))
                name = clean_text(row.get("field_name") or row.get("name"))
                lg = clean_text(row.get("lg"))
                if not facility_id or not name or not lg:
                    continue

                status = clean_text(row.get("status"))
                self.status_by_id[facility_id] = status
                if status in INVALID_FACILITY_STATUSES:
                    self.invalid_facility_ids.add(facility_id)
                    continue

                lgk = self._remember_lg(lg)
                canonical_lg = self.lg_display.get(lgk, lg)
                facility = Facility(name, canonical_lg)
                self.facility_by_id.setdefault(facility_id, facility)

                aliases = {
                    facility_key(name),
                    facility_key(row.get("name")),
                    facility_key(row.get("field_name")),
                }
                aliases.update(
                    alias.replace(" seed ss", " ss")
                    for alias in tuple(aliases)
                    if " seed ss" in alias
                )
                aliases.update(
                    alias.replace(" regional blood bank", " blood bank")
                    for alias in tuple(aliases)
                    if " regional blood bank" in alias
                )
                folder = clean_text(row.get("folder")).replace("\\", "/").strip("/")
                if folder:
                    folder_key = normalized_path(folder)
                    self.folder_to_facility.setdefault(folder_key, facility)
                    aliases.add(facility_key(PurePosixPath(folder).name))

                for alias in {item for item in aliases if item}:
                    self.facility_aliases_by_lg[lgk].setdefault(alias, facility)
                    if facility not in self.global_facility_aliases[alias]:
                        self.global_facility_aliases[alias].append(facility)

    def canonical_lg(self, value: object) -> str | None:
        raw = clean_text(value)
        if not raw:
            return None
        upper = re.sub(r"[^A-Z0-9]+", "", raw.upper())
        for code in MDA_NAMES:
            if upper == code:
                return code

        key = lg_key(raw)
        if not key or key in INVALID_LG_KEYS:
            return None
        if key in self.lg_display:
            return self.lg_display[key]

        scores = sorted(
            ((SequenceMatcher(None, key, candidate).ratio(), candidate) for candidate in self.lg_display),
            reverse=True,
        )
        if scores and scores[0][0] >= 0.86 and (
            len(scores) == 1 or scores[0][0] - scores[1][0] >= 0.06
        ):
            return self.lg_display[scores[0][1]]
        return None

    def find_lg_in_text(self, value: object) -> str | None:
        text = f" {normalized_key(value)} "
        for key in self._lg_search:
            if len(key) >= 4 and f" {key} " in text:
                return self.lg_display[key]
        return None

    def facility_from_path(self, value: object) -> Facility | None:
        path = normalized_path(clean_text(value))
        prefix = "raw data grouped/"
        if path.startswith(prefix):
            path = path[len(prefix) :]
        parts = path.split("/")
        for length in range(len(parts) - 1, 1, -1):
            candidate = "/".join(parts[:length])
            if candidate in self.folder_to_facility:
                return self.folder_to_facility[candidate]
        return None

    def canonical_facility(self, value: object, lg: object = None) -> Facility | None:
        key = facility_key(value)
        if not key:
            return None
        lgk = lg_key(lg)
        aliases = self.facility_aliases_by_lg.get(lgk, {}) if lgk else {}

        if key in aliases:
            return aliases[key]
        contained = [
            facility
            for alias, facility in aliases.items()
            if len(alias) >= 5 and f" {alias} " in f" {key} "
        ]
        if contained:
            return max(contained, key=lambda item: len(facility_key(item.name)))

        if aliases and len(key) >= 5:
            scores = sorted(
                ((SequenceMatcher(None, key, alias).ratio(), alias) for alias in aliases),
                reverse=True,
            )
            if scores and scores[0][0] >= 0.90 and (
                len(scores) == 1 or scores[0][0] - scores[1][0] >= 0.05
            ):
                return aliases[scores[0][1]]

        matches = self.global_facility_aliases.get(key, [])
        return matches[0] if len(matches) == 1 else None

    def find_facility_in_text(self, value: object, lg: object = None) -> Facility | None:
        key = facility_key(value)
        if not key:
            return None
        aliases = self.facility_aliases_by_lg.get(lg_key(lg), {}) if lg else {}
        if not aliases:
            aliases = {
                alias: facilities[0]
                for alias, facilities in self.global_facility_aliases.items()
                if len(facilities) == 1
            }
        matches = [
            (len(alias), facility)
            for alias, facility in aliases.items()
            if len(alias) >= 5 and f" {alias} " in f" {key} "
        ]
        if matches:
            return max(matches, key=lambda item: item[0])[1]
        return None

    def school_from_tag(self, value: object) -> Facility | None:
        match = re.search(r"\b([A-Z][A-Z'-]{3,})\s*/\s*SSS\b", clean_text(value), re.I)
        if not match:
            return None
        prefix = normalized_key(match.group(1))
        candidates = {
            facilities[0]
            for alias, facilities in self.global_facility_aliases.items()
            if len(facilities) == 1 and alias.startswith(prefix + " ") and alias.endswith(" ss")
        }
        return next(iter(candidates)) if len(candidates) == 1 else None


def usable_facility_text(value: object, master: MasterData, lg: object = None) -> str | None:
    text = clean_text(value)
    if not text:
        return None
    key = facility_key(text)
    if key in {"unspecified", "not allocated", "not applicable", "n a", "district"}:
        return None
    compact = re.sub(r"[^A-Za-z0-9]", "", text)
    if " " not in text and len(compact) >= 10 and any(ch.isdigit() for ch in compact):
        return None
    if lg and lg_key(text) == lg_key(lg):
        return None
    canonical = master.canonical_facility(text, lg)
    if canonical:
        return canonical.name
    if len(text) > 100 or text.count("/") >= 3:
        return None
    return text


def entity_name(lg: str) -> str:
    if lg in MDA_NAMES:
        return MDA_NAMES[lg]
    base = re.sub(
        r"\s+(?:DISTRICT LOCAL GOV'?T|DISTRICT LOCAL GOVERNMENT|DISTRICT|DLG)$",
        "",
        clean_text(lg),
        flags=re.I,
    ).strip()
    upper = base.upper()
    if upper.endswith(" MC"):
        return f"{base[:-3].strip().title()} Municipal Council"
    if upper.endswith(" CITY"):
        return f"{base.title()} Council"
    return f"{base.title()} District Local Government"


def book_code(lg: str | None) -> str | None:
    if not lg:
        return None
    if lg in MDA_NAMES:
        return f"{lg} BK"
    text = clean_text(lg).upper()
    for old, new in (
        (" DISTRICT LOCAL GOV'T", ""),
        (" DISTRICT LOCAL GOVT", ""),
        (" DISTRICT LOCAL GOVERNMENT", ""),
        (" MUNICIPAL COUNCIL", " MC"),
        (" DISTRICT LG", ""),
        (" LOCAL GOVERNMENT", ""),
        (" DISTRICT", ""),
        (" DLG", ""),
    ):
        if text.endswith(old):
            text = (text[: -len(old)] + new).strip()
            break
    return f"{text} BK" if text else None


def parse_labeled_value(text: str, label: str) -> str | None:
    match = re.search(rf"{label}\s*:\s*([^|]+)", text, re.I)
    return clean_text(match.group(1)) if match else None


def header_kind(value: object) -> str | None:
    key = normalized_key(value)
    if key in {"district", "local government", "local govvernment", "lg", "entity"}:
        return "lg"
    if key in {
        "facility",
        "health facility",
        "health centre",
        "health center",
        "hospital",
        "location",
        "school",
    }:
        return "facility"
    return None


class SourceTracer:
    """Read an exact source worksheet row and its nearest location context."""

    def __init__(self, master: MasterData) -> None:
        self.master = master

    def trace(self, source_file: object, locator: object) -> Resolution | None:
        match = SOURCE_LOCATOR_RE.match(clean_text(locator))
        if not match:
            return None
        relative = clean_text(source_file).replace("/", "\\")
        path = ROOT / relative
        if not path.exists() and path.parent.exists():
            wanted = normalized_key(path.name)
            matches = [item for item in path.parent.iterdir() if normalized_key(item.name) == wanted]
            if len(matches) == 1:
                path = matches[0]
        if not path.exists() or path.suffix.casefold() not in {".xlsx", ".xlsm", ".xls"}:
            return None
        sheet_name, row_number = match.group(1), int(match.group(2))
        result = self._contexts(str(path.resolve()), sheet_name).get(row_number)
        if not result:
            return None
        lg, facility = result
        return Resolution(lg, facility, "source worksheet", "source worksheet")

    @lru_cache(maxsize=None)
    def _contexts(self, absolute_path: str, requested_sheet: str) -> dict[int, tuple[str | None, str | None]]:
        return self._scan_rows(self._read_rows(Path(absolute_path), requested_sheet))

    def _read_rows(self, path: Path, requested_sheet: str) -> Iterator[tuple[int, tuple[object, ...]]]:
        if path.suffix.casefold() == ".xls":
            book = xlrd.open_workbook(path, on_demand=True)
            sheet = self._xlrd_sheet(book, requested_sheet)
            try:
                for row_index in range(sheet.nrows):
                    yield row_index + 1, tuple(sheet.row_values(row_index))
            finally:
                book.release_resources()
            return

        workbook = load_workbook(path, read_only=True, data_only=True)
        sheet = self._openpyxl_sheet(workbook, requested_sheet)
        try:
            for row_number, row in enumerate(sheet.iter_rows(values_only=True), 1):
                yield row_number, tuple(row)
        finally:
            workbook.close()

    @staticmethod
    def _openpyxl_sheet(workbook, requested: str):
        if requested in workbook.sheetnames:
            return workbook[requested]
        wanted = requested.strip().casefold()
        for name in workbook.sheetnames:
            if name.strip().casefold() == wanted:
                return workbook[name]
        raise KeyError(f"Worksheet {requested!r} not found")

    @staticmethod
    def _xlrd_sheet(workbook, requested: str):
        try:
            return workbook.sheet_by_name(requested)
        except xlrd.biffh.XLRDError:
            wanted = requested.strip().casefold()
            for name in workbook.sheet_names():
                if name.strip().casefold() == wanted:
                    return workbook.sheet_by_name(name)
            raise

    def _scan_rows(
        self, rows: Iterable[tuple[int, tuple[object, ...]]]
    ) -> dict[int, tuple[str | None, str | None]]:
        contexts: dict[int, tuple[str | None, str | None]] = {}
        lg_columns: set[int] = set()
        facility_columns: set[int] = set()
        current_lg: str | None = None
        current_facility: str | None = None

        for row_number, row in rows:
            texts = [clean_text(value) for value in row]
            nonblank = [(index, text) for index, text in enumerate(texts) if text]
            joined = " | ".join(text for _, text in nonblank)

            for index, text in nonblank:
                kind = header_kind(text)
                if kind == "lg":
                    lg_columns.add(index)
                elif kind == "facility":
                    facility_columns.add(index)

            explicit_lg = parse_labeled_value(joined, r"(?:NAME OF LG|ENTITY)")
            explicit_facility = parse_labeled_value(joined, r"NAME OF (?:HEALTH )?FACILITY")
            if explicit_lg:
                current_lg = self.master.canonical_lg(explicit_lg) or current_lg
            if explicit_facility:
                canonical = self.master.canonical_facility(explicit_facility, current_lg)
                current_facility = canonical.name if canonical else clean_text(explicit_facility)

            for index in lg_columns:
                if index < len(row):
                    candidate = self.master.canonical_lg(row[index])
                    if candidate:
                        current_lg = candidate
            for index in facility_columns:
                if index < len(row):
                    candidate = usable_facility_text(row[index], self.master, current_lg)
                    if candidate and header_kind(candidate) is None:
                        current_facility = candidate

            row_lg = self.master.find_lg_in_text(joined)
            if row_lg and len(nonblank) <= 5:
                current_lg = row_lg
            effective_lg = row_lg or current_lg

            # A facility named in a tag or description applies to that source
            # row only. Carry it forward only when the sparse row is a section
            # title; otherwise a single mention in a district-wide register
            # would incorrectly relabel every following asset.
            row_facility = self.master.find_facility_in_text(joined, effective_lg)
            if not row_facility:
                row_facility = self.master.school_from_tag(joined)
            if not row_facility:
                raw_candidates = [
                    text
                    for _, text in nonblank
                    if "/" in text or "incharge" in text.casefold()
                ]
                if len(nonblank) <= 5:
                    raw_candidates.append(joined)
                raw_facility = next(
                    (format_raw_facility(text) for text in raw_candidates if format_raw_facility(text)),
                    None,
                )
            else:
                raw_facility = None
            if row_facility and len(nonblank) <= 5:
                current_facility = row_facility.name
                current_lg = row_facility.lg
            if raw_facility and len(nonblank) <= 5:
                current_facility = raw_facility
            effective_facility = (
                row_facility.name if row_facility else raw_facility or current_facility
            )
            if row_facility:
                effective_lg = row_facility.lg

            contexts[row_number] = (effective_lg, effective_facility)
        return contexts


def facility_from_filename(source_file: object, master: MasterData, lg: object) -> Facility | None:
    stem = Path(clean_text(source_file)).stem
    if not FACILITY_MARKERS.search(stem):
        return None
    return (
        master.find_facility_in_text(stem, lg)
        or master.find_facility_in_text(stem)
        or master.canonical_facility(stem, lg)
    )


def facility_from_description(description: object, master: MasterData, lg: object) -> Facility | None:
    text = clean_text(description)
    found = master.find_facility_in_text(text, lg)
    if found:
        return found
    parts = [clean_text(part) for part in re.split(r"\s+-\s+", text) if clean_text(part)]
    for candidate in reversed(parts[-3:]):
        if FACILITY_MARKERS.search(candidate):
            return master.canonical_facility(candidate, lg)
    return None


def lg_from_district_path(source_file: object, master: MasterData) -> str | None:
    parts = [part for part in clean_text(source_file).replace("\\", "/").split("/") if part]
    for index, part in enumerate(parts):
        if normalized_key(part) == "district documents" and index >= 1:
            return master.canonical_lg(parts[index - 1])
    return None


def source_maps(
    ws_source, master: MasterData
) -> tuple[dict[int, str], dict[int, str], Counter, dict[str, Counter], set[str]]:
    """Map register rows to source-backed LG and facility values."""
    headers = [cell.value for cell in next(ws_source.iter_rows(min_row=1, max_row=1))]
    index = {name: i for i, name in enumerate(headers)}
    tracer = SourceTracer(master)
    lg_by_row: dict[int, str] = {}
    facility_by_row: dict[int, str] = {}
    rules: Counter = Counter()
    unresolved = {"lg": Counter(), "facility": Counter()}
    kept_source_refs: set[str] = set()

    for row in ws_source.iter_rows(min_row=2, values_only=True):
        first = row[index["Register first row"]]
        last = row[index["Register last row"]]
        if first is None or last is None:
            continue

        source_ref = clean_text(row[index["Source reference"]])
        facility_id = clean_text(row[index["Facility ID"]])
        source_file = row[index["Source file"]]
        source_path_key = normalized_path(clean_text(source_file))
        source_lg = row[index["Local government / MDA"]]
        source_facility = row[index["Facility / location"]]
        source_asset = row[index["Asset in source"]]
        represented = int(last) - int(first) + 1

        if facility_id in master.invalid_facility_ids:
            rules[f"Removed: {master.status_by_id[facility_id]}"] += represented
            continue

        lg: str | None = None
        facility: str | None = None
        lg_rule = ""
        facility_rule = ""

        reconciled = master.facility_by_id.get(facility_id)
        if reconciled:
            lg, facility = reconciled.lg, reconciled.name
            lg_rule = facility_rule = "reconciled facility ID"

        if not reconciled:
            path_facility = master.facility_from_path(source_file)
            if path_facility:
                lg, facility = path_facility.lg, path_facility.name
                lg_rule = facility_rule = "reconciled source folder"

        if not lg:
            lg = master.canonical_lg(source_lg)
            if lg:
                lg_rule = "source-line LG"
        if not lg:
            lg = lg_from_district_path(source_file, master)
            if lg:
                lg_rule = "district source path"

        if not facility:
            canonical = master.canonical_facility(source_facility, lg)
            if canonical:
                facility = canonical.name
                lg = canonical.lg
                facility_rule = "canonicalized source-line facility"
                lg_rule = lg_rule or "source-line facility"

        traceable_source = any(
            marker in source_path_key
            for marker in (
                "team documents",
                "district documents",
                "busoga and part of central",
                "pdf to excel",
                "fwdugiftassets",
                "mda status register",
            )
        )
        if traceable_source and (not facility or not lg):
            try:
                traced = tracer.trace(source_file, row[index["Source locator"]])
            except (OSError, KeyError, ValueError, xlrd.biffh.XLRDError):
                traced = None
            if traced:
                traced_facility = master.canonical_facility(traced.facility, traced.lg or lg)
                if not lg and traced.lg:
                    lg, lg_rule = traced.lg, traced.lg_rule
                if not facility and traced_facility:
                    facility = traced_facility.name
                    lg = traced_facility.lg
                    facility_rule = "canonicalized source worksheet"
                    lg_rule = lg_rule or "source worksheet facility"

        if not facility:
            described = facility_from_description(source_asset, master, lg)
            if described:
                facility, lg = described.name, described.lg
                facility_rule = "source description"
                lg_rule = lg_rule or "source description facility"

        if not facility:
            named = facility_from_filename(source_file, master, lg)
            if named:
                facility, lg = named.name, named.lg
                facility_rule = "source filename"
                lg_rule = lg_rule or "source filename facility"

        source_facility_text = clean_text(source_facility)
        owner_location = (
            not source_facility_text
            or (lg and lg_key(source_facility_text) == lg_key(lg))
            or bool(re.search(r"\b(?:district|municipal|city|local government|ministry)\b", source_facility_text, re.I))
        )
        if not facility and lg and owner_location:
            facility = entity_name(lg)
            facility_rule = "LG named as source location"

        if not facility and lg and "district documents" in source_path_key and owner_location:
            facility = entity_name(lg)
            facility_rule = "district-register owner"
        if not facility and lg in MDA_NAMES:
            facility = MDA_NAMES[lg]
            facility_rule = "MDA-register owner"

        source_context = normalized_key(
            f"{source_file} {row[index['Source locator']]} "
            f"{row[index['Source remarks and qualifications']]}"
        )
        if not lg:
            explicit_mda = mda_from_text(f"{source_facility} {facility} {source_asset}")
            if explicit_mda:
                lg = explicit_mda
                lg_rule = "explicit MDA name"
                facility = MDA_NAMES[lg]
                facility_rule = "explicit MDA name"
        if not lg:
            context_rules = (
                ("wemis", "MOWE", "WEMIS source context"),
                ("motorcycles for moh ugift", "MOH", "MOH worksheet heading"),
                ("for auditors", "OAG", "auditor-register context"),
                ("bped", "MOFPED", "BPED register context"),
                ("original entity heading nema", "NEMA", "MDA worksheet heading"),
                ("original entity heading ppda", "PPDA", "MDA worksheet heading"),
                ("fwdugiftassets", "MOFPED", "central UgIFT register owner"),
            )
            for marker, code, rule in context_rules:
                if marker in source_context:
                    lg, lg_rule = code, rule
                    break
        if not facility and lg in MDA_NAMES:
            facility = MDA_NAMES[lg]
            facility_rule = lg_rule

        rules[f"LG: {lg_rule}" if lg else "LG: unresolved"] += represented
        rules[f"Facility: {facility_rule}" if facility else "Facility: unresolved"] += represented
        if not lg:
            unresolved["lg"][clean_text(source_file)] += represented
        if not facility:
            unresolved["facility"][clean_text(source_file)] += represented

        if not lg or not facility:
            rules["Removed: not mapped to a valid facility or traceable owner"] += represented
            continue

        kept_source_refs.add(source_ref)
        for register_row in range(int(first), int(last) + 1):
            lg_by_row[register_row] = lg
            facility_by_row[register_row] = facility

    return lg_by_row, facility_by_row, rules, unresolved, kept_source_refs


def copy_cell(source, target) -> None:
    value = source.value
    if isinstance(value, str) and value.startswith("="):
        try:
            value = Translator(value, origin=source.coordinate).translate_formula(target.coordinate)
        except (TypeError, ValueError):
            pass
    target.value = value
    if source.has_style:
        target._style = copy(source._style)
    if source.number_format:
        target.number_format = source.number_format
    if source.hyperlink:
        target._hyperlink = copy(source.hyperlink)
    if source.comment:
        target.comment = copy(source.comment)


def copy_row(ws, source_row: int, target_row: int, max_column: int) -> None:
    if source_row == target_row:
        return
    for column in range(1, max_column + 1):
        copy_cell(ws.cell(source_row, column), ws.cell(target_row, column))
    if source_row in ws.row_dimensions:
        ws.row_dimensions[target_row] = copy(ws.row_dimensions[source_row])
        ws.row_dimensions[target_row].index = target_row


def compact_register(ws, kept_rows: set[int]) -> dict[int, int]:
    """Remove rejected asset rows in one forward copy and one tail deletion."""
    row_map: dict[int, int] = {}
    target_row = 2
    max_column = ws.max_column
    for source_row in sorted(row for row in kept_rows if row >= 2):
        copy_row(ws, source_row, target_row, max_column)
        row_map[source_row] = target_row
        target_row += 1
    if target_row <= ws.max_row:
        ws.delete_rows(target_row, ws.max_row - target_row + 1)
    return row_map


SOURCE_LINE_ROW_REFERENCE = re.compile(
    r"(?P<prefix>(?:'Source Lines'|Source Lines)!\$?[A-Z]{1,3}\$?)(?P<row>\d+)",
    re.I,
)


def remap_source_line_formulas(ws, source_row_map: dict[int, int]) -> int:
    """Retarget absolute Source Lines references after source-row compaction."""
    updated = 0
    missing: set[int] = set()
    for cell in ws._cells.values():
        formula = cell.value
        if not isinstance(formula, str) or not formula.startswith("=") or "source lines" not in formula.casefold():
            continue

        def replace(match: re.Match[str]) -> str:
            old_row = int(match.group("row"))
            new_row = source_row_map.get(old_row)
            if new_row is None:
                missing.add(old_row)
                return match.group(0)
            return f'{match.group("prefix")}{new_row}'

        remapped = SOURCE_LINE_ROW_REFERENCE.sub(replace, formula)
        if remapped != formula:
            cell.value = remapped
            updated += 1
    if missing:
        sample = ", ".join(str(row) for row in sorted(missing)[:12])
        raise ValueError(f"Retained formulas reference removed Source Lines rows: {sample}")
    return updated


def retarget_source_line_formulas(ws, first_row: int, last_row: int, source_row: int) -> int:
    """Point formulas in newly appended assets at their new Source Lines row."""
    updated = 0
    for row in ws.iter_rows(min_row=first_row, max_row=last_row):
        for cell in row:
            formula = cell.value
            if not isinstance(formula, str) or not formula.startswith("=") or "source lines" not in formula.casefold():
                continue
            remapped = SOURCE_LINE_ROW_REFERENCE.sub(
                lambda match: f'{match.group("prefix")}{source_row}', formula
            )
            if remapped != formula:
                cell.value = remapped
                updated += 1
    return updated


def compact_source_lines(ws, kept_source_refs: set[str], row_map: dict[int, int]) -> dict[int, int]:
    headers = [cell.value for cell in ws[1]]
    index = {name: position + 1 for position, name in enumerate(headers)}
    target_row = 2
    max_row = ws.max_row
    max_column = ws.max_column
    source_row_map: dict[int, int] = {}
    for source_row in range(2, max_row + 1):
        source_ref = clean_text(ws.cell(source_row, index["Source reference"]).value)
        if source_ref not in kept_source_refs:
            continue
        old_first = int(ws.cell(source_row, index["Register first row"]).value)
        old_last = int(ws.cell(source_row, index["Register last row"]).value)
        copy_row(ws, source_row, target_row, max_column)
        source_row_map[source_row] = target_row
        ws.cell(target_row, index["Register first row"]).value = row_map[old_first]
        ws.cell(target_row, index["Register last row"]).value = row_map[old_last]
        ws.cell(target_row, index["Items represented"]).value = old_last - old_first + 1
        target_row += 1
    if target_row <= ws.max_row:
        ws.delete_rows(target_row, ws.max_row - target_row + 1)
    if ws.auto_filter.ref:
        ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
    return source_row_map


def source_rows_are_all_retained(ws, kept_source_refs: set[str]) -> bool:
    headers = [cell.value for cell in ws[1]]
    source_reference_column = headers.index("Source reference") + 1
    return all(
        clean_text(ws.cell(row, source_reference_column).value) in kept_source_refs
        for row in range(2, ws.max_row + 1)
    )


def count_from_text(value: object) -> int | None:
    text = clean_text(value)
    match = re.fullmatch(r"0*(\d+(?:\.0+)?)\s*(?:items?|units?|blocks?)?", text, re.I)
    if not match:
        return None
    count = int(float(match.group(1)))
    return count if 0 < count <= 10000 else None


def register_source_record(
    *, facility_id: str, lg: str, facility: str, asset: str, source_file: str,
    source_locator: str, quantity: int, quantity_basis: str, condition: str = "",
    remarks: str = "", service_date: object = None, life_months: object = None,
    tag_number: str = "", asset_details: str = "",
) -> dict[str, object]:
    qualifications = [clean_text(remarks), "Flattened field form. Template-only labels without observations excluded."]
    if quantity > 1 and tag_number:
        qualifications.append("Source tag applies to an aggregate group and is not a unique per-unit identifier.")
    qualifications.append("Per-item cost unavailable")
    return {
        "Local government / MDA": lg,
        "Facility / location": facility,
        "Asset in source": asset,
        "Source file": source_file,
        "Source locator": source_locator,
        "Quantity basis": quantity_basis,
        "Source unit cost (UGX)": None,
        "Source line total (UGX)": None,
        "Cost treatment": "Cost not established",
        "Original purchase date": None,
        "Original service date": service_date,
        "Original condition": clean_text(condition),
        "Source remarks and qualifications": "; ".join(item for item in qualifications if item),
        "Asset details in source": clean_text(asset_details),
        "Facility ID": facility_id,
        "quantity": quantity,
        "life_months": life_months,
        "tag_number": clean_text(tag_number),
    }


def explicit_group_quantity(group: list[list[object]]) -> int | None:
    """Return a written/recorded quantity, preserving an explicit zero."""
    text = " | ".join(clean_text(value) for row in group for value in row if clean_text(value))
    if re.search(r"\b(?:observed|observe)\b[^0-9]*(?:nil|nill|none)\b", text, re.I):
        return 0
    patterns = (
        r"\binventory\s+quantity\b[^0-9]*(\d+)",
        r"\bsupplier\s+quantity\b[^0-9]*(\d+)",
        r"\bqty\b[^0-9]*(\d+)",
        r"\b(?:observed|observe)\b[^0-9]*(\d+)",
        r"\bsupplied\b[^0-9]*(\d+)",
        r"\b(\d+)\s*-\s*supplied\b",
    )
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return int(match.group(1))
    for row in group[1:]:
        for column in (0, 1):
            if column < len(row) and (quantity := count_from_text(row[column])) is not None:
                return quantity
    return None


def latest_western_records(master: MasterData) -> list[dict[str, object]]:
    if not LATEST_WESTERN_PATH.is_file():
        return []
    relative = LATEST_WESTERN_SOURCE
    ranges = [
        ("UGIFT HEALTH 2", 1749, 2019, "H023"),
        ("UGIFT HEALTH 2", 2022, 2306, "H020"),
        ("UGIFT HEALTH 2", 2309, 2592, "H291"),
        ("UGIFT HEALTH 2", 2593, 2880, "H297"),
        ("UGIFT HEALTH", 7877, 8116, "H013"),
        ("UGIFT HEALTH", 8122, 8355, "H011"),
        ("UGIFT HEALTH", 8634, 8867, "H301"),
        ("UGIFT HEALTH", 8876, 9100, "X011"),
        ("UGIFT HEALTH", 9107, 9146, "H014"),
    ]
    workbook = xlrd.open_workbook(LATEST_WESTERN_PATH, on_demand=True)
    records: list[dict[str, object]] = []
    try:
        for sheet_name, first, last, facility_id in ranges:
            sheet = workbook.sheet_by_name(sheet_name)
            facility = master.facility_by_id[facility_id]
            rows = [(row_number, sheet.row_values(row_number - 1)) for row_number in range(first, last + 1)]
            starts = []
            for position, (_, row) in enumerate(rows):
                label = clean_text(row[0] if row else "")
                if not label or count_from_text(label) is not None:
                    continue
                if normalized_key(label) in {
                    "equipment item", "description", "not engraved", "n a", "na",
                    "in use", "not in use", "functional", "functioning",
                }:
                    continue
                starts.append(position)
            for item_index, start in enumerate(starts):
                stop = starts[item_index + 1] if item_index + 1 < len(starts) else len(rows)
                row_number, first_row = rows[start]
                group = [row for _, row in rows[start:stop]]
                label = clean_text(first_row[0])
                quantity = explicit_group_quantity(group)
                observed = quantity is not None or any(clean_text(row[column]) for row in group for column in (1, 3, 5, 9, 13, 14))
                if not observed:
                    continue
                if quantity == 0:
                    continue
                quantity = quantity or 1
                values = lambda column: [clean_text(row[column]) for row in group if clean_text(row[column])]
                details = ", ".join(dict.fromkeys(values(3)))
                asset = f"{label} - {details}" if details else label
                condition = "; ".join(dict.fromkeys(values(13)))
                remarks = "; ".join(dict.fromkeys(values(14)))
                tags = "; ".join(dict.fromkeys(values(5)))
                life = next((value for row in group for value in [row[4]] if isinstance(value, (int, float)) and value > 0), None)
                service = next((value for row in group for value in [row[7]] if clean_text(value)), None)
                records.append(register_source_record(
                    facility_id=facility_id, lg=facility.lg, facility=facility.name,
                    asset=asset, source_file=relative,
                    source_locator=f"Worksheet {sheet_name}, row {row_number}",
                    quantity=quantity,
                    quantity_basis="explicit source quantity" if quantity > 1 else "single completed observation",
                    condition=condition, remarks=remarks, service_date=service,
                    life_months=life, tag_number=tags, asset_details=details,
                ))
    finally:
        workbook.release_resources()
    return records


def makokoto_health_records(master: MasterData) -> list[dict[str, object]]:
    """Extract only observed Makokoto HC III items; blank template rows stay excluded."""
    if not LATEST_MAKOKOTO_PATH.is_file():
        return []
    facility = master.facility_by_id["H012"]
    table = Document(LATEST_MAKOKOTO_PATH).tables[5]
    records: list[dict[str, object]] = []
    for row_number, row in enumerate(table.rows[1:], 2):
        values = [clean_text(cell.text) for cell in row.cells]
        asset = values[0]
        if not asset:
            continue
        quantity = explicit_group_quantity([values])
        if quantity is None:
            department_count = re.search(r"(?:\s*-\s*|\s+)(\d+)\s*$", values[1])
            quantity = int(department_count.group(1)) if department_count else None
        if not quantity:
            continue
        records.append(register_source_record(
            facility_id="H012", lg=facility.lg, facility=facility.name,
            asset=asset, source_file=LATEST_MAKOKOTO_SOURCE,
            source_locator=f"Table 6, row {row_number}", quantity=quantity,
            quantity_basis="observed/supplied count in the facility checklist",
            condition=values[13], remarks=values[14],
            service_date=values[7] or None, life_months=values[4] or None,
            tag_number=values[5], asset_details=values[3],
        ))
    return records


def school_table_records(
    master: MasterData, *, path: Path, source_file: str, facility_id: str,
    table_indexes: tuple[int, ...],
) -> list[dict[str, object]]:
    """Extract counted school assets from grouped checklist tables."""
    if not path.is_file():
        return []
    facility = master.facility_by_id[facility_id]
    document = Document(path)
    records: list[dict[str, object]] = []
    for table_index in table_indexes:
        table = document.tables[table_index]
        rows = [
            (row_number, [clean_text(cell.text) for cell in row.cells])
            for row_number, row in enumerate(table.rows[1:], 2)
        ]
        starts = [
            position for position, (_, values) in enumerate(rows)
            if values and values[0] and count_from_text(values[0]) is None
        ]
        for item_index, start in enumerate(starts):
            stop = starts[item_index + 1] if item_index + 1 < len(starts) else len(rows)
            row_number, values = rows[start]
            group = [row_values for _, row_values in rows[start:stop]]
            quantity = explicit_group_quantity(group)
            if not quantity:
                continue
            details = values[3] if len(values) > 3 else ""
            asset = f"{values[0]} - {details}" if details else values[0]
            records.append(register_source_record(
                facility_id=facility_id, lg=facility.lg, facility=facility.name,
                asset=asset, source_file=source_file,
                source_locator=f"Table {table_index + 1}, row {row_number}",
                quantity=quantity, quantity_basis="count written beneath item label",
                condition=values[13] if len(values) > 13 else "",
                remarks=values[14] if len(values) > 14 else "",
                service_date=values[7] if len(values) > 7 and values[7] else None,
                life_months=values[4] if len(values) > 4 and values[4] else None,
                tag_number=values[5] if len(values) > 5 else "",
                asset_details=details,
            ))
    return records


def team30_school_records(master: MasterData) -> list[dict[str, object]]:
    return [
        *school_table_records(
            master, path=LATEST_MAKOKOTO_PATH, source_file=LATEST_MAKOKOTO_SOURCE,
            facility_id="S069", table_indexes=(10, 11, 12),
        ),
        *school_table_records(
            master, path=LATEST_NYAMARWA_PATH, source_file=LATEST_NYAMARWA_SOURCE,
            facility_id="S236", table_indexes=(10, 11, 12),
        ),
    ]


def quantity_from_remarks(value: object) -> int:
    text = clean_text(value)
    for pattern in (r"\btotal of\s+(\d+)\b", r"\bhas\s+(\d+)\b", r"\b(\d+)\s+newly constructed\b"):
        match = re.search(pattern, text, re.I)
        if match:
            return int(match.group(1))
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    match = re.search(r"\b(one|two|three|four|five)\s+newly constructed\b", text, re.I)
    return words[match.group(1).casefold()] if match else 1


def lwamata_records(master: MasterData) -> list[dict[str, object]]:
    if not LATEST_LWAMATA_PATH.is_file():
        return []
    relative = LATEST_LWAMATA_SOURCE
    facility = master.facility_by_id["S001"]
    document = Document(LATEST_LWAMATA_PATH)
    records: list[dict[str, object]] = []
    for table_index in (4, 6):
        table = document.tables[table_index]
        for row_number, row in enumerate(table.rows[1:], 2):
            values = [clean_text(cell.text) for cell in row.cells]
            asset = values[0]
            if not asset or normalized_key(asset) in {"n a", "na"}:
                continue
            remarks = values[14]
            quantity = quantity_from_remarks(remarks)
            details = values[3]
            asset_label = f"{asset} - {details}" if details and normalized_key(details) not in {"n a", "na"} else asset
            records.append(register_source_record(
                facility_id="S001", lg=facility.lg, facility=facility.name,
                asset=asset_label, source_file=relative,
                source_locator=f"Table {table_index + 1}, row {row_number}",
                quantity=quantity,
                quantity_basis="explicit count in remarks" if quantity > 1 else "single completed observation",
                condition=values[13], remarks=remarks,
                service_date=values[7] if values[7] and values[7] != "N/A" else None,
                life_months=values[4] or None, tag_number=values[5], asset_details=details,
            ))
    return records


def sofia_records(master: MasterData) -> list[dict[str, object]]:
    """Transcribe the explicit quantities in Sofia HC III's scanned checklist."""
    if not LATEST_SOFIA_PATH.is_file():
        return []
    relative = LATEST_SOFIA_SOURCE
    facility = master.facility_by_id["X041"]
    checklist = [
        (3, "B.P. Machine, Digital", 2, "Black screen with white casing"),
        (3, "B.P. Machine, Aneroid, wall mounted", 3, "Gauge with black bracket"),
        (3, "Autoclave, 20 litre, duo operated", 2, "Stainless steel"),
        (3, "Bowl, Kick", 2, "Stainless steel"),
        (3, "Bowl Stand", 3, "Stainless steel"),
        (3, "Counting Chamber, Neubauer Improved", 1, "Glass with red marking"),
        (3, "Cupboard, Steel, Lockable", 4, "Brown-grey with black handles"),
        (3, "Drip Stand", 13, "Stainless steel with rubber base"),
        (5, "ESR Stand", 1, "White"),
        (5, "Examination Couch", 4, "Black mattress with stainless-steel frame"),
        (5, "Examination Light, LED", 4, ""),
        (5, "Glucometer", 4, "Grey"),
        (5, "Haemoglobin Meter, Digital", 2, "White with screen and red marking"),
        (5, "Height Meter", 2, ""),
        (5, "Instrument Trolley", 4, ""),
        (5, "Microscope, Binocular", 1, "White and black"),
        (5, "Otoscope", 1, ""),
        (5, "Patient Screen", 6, "Blue and white with stainless-steel frame"),
        (5, "Patient Trolley", 1, "Stainless steel"),
        (7, "Refrigerator, Basic", 3, "White-grey CHICO refrigerator"),
        (7, "Stethoscope", 8, "Black"),
        (7, "Stop Watch", 2, "White"),
        (7, "Stretcher", 2, "Blue mattress"),
        (7, "Stove, Gas", 2, ""),
        (7, "Weighing Scale with Height Meter, Adult", 5, "White base with height ruler"),
        (7, "Weighing Scale, Infant", 4, "White"),
        (7, "Weighing Scale, Toddler", 2, ""),
        (7, "Wheel Chair", 5, "Black with metal frame"),
        (7, "Projector", 2, "Audio-visual equipment row"),
        (7, "Projector Screen", 2, "Audio-visual equipment row"),
        (7, "DVD Player", 3, "Black; audio-visual equipment row"),
        (7, "Medical Waste Bin", 20, "Stainless steel"),
        (7, "Wall Clock", 7, "Black and white"),
        (9, "Diagnostic Equipment Set for MCH", 2, "Stainless steel"),
        (9, "Diagnostic Equipment Set for OPD", 2, "Stainless steel"),
        (9, "Glassware Set, Laboratory, Basic", 2, ""),
        (9, "Hollow Ware Set, Treatment", 2, "Stainless steel"),
        (9, "Instrument Set, Dressing", 2, "Stainless steel"),
        (9, "Instrument Set, Basic ENT", 3, "Stainless steel"),
        (9, "Instrument Set, Suture", 2, "Stainless steel"),
        (9, "Pulse Oximeter, Handheld", 4, "Black screen with white casing"),
        (9, "Bed, Adult Patient with Mattress", 30, "Black mattress with stainless-steel frame"),
        (9, "Bed, Pediatric Patient with Mattress", 10, "Black mattress with stainless-steel frame"),
        (11, "Bedside Locker", 10, "White-blue plastic"),
        (11, "Cupboard, Instrument", 1, "Stainless steel"),
        (11, "Delivery Bed, Hydraulic Manual", 2, "Black mattress"),
        (11, "Oxygen Therapy Apparatus, Minimum 45L Cylinder", 4, ""),
        (11, "Resuscitator Manual, Infant, with all Mask Sizes", 10, "Plastic balloon form"),
        (11, "Resuscitator Manual, Adult, with all Mask Sizes", 10, "Plastic balloon form"),
        (11, "Suction Apparatus, Electric", 3, ""),
        (11, "Nebulizer, Ultrasonic", 1, ""),
        (11, "Oxygen Concentrator, Duo Flow", 4, ""),
        (11, "Bench", 4, "Blue-grey with metal frame"),
        (13, "Disinfection Bucket", 10, "White"),
        (13, "Baby Cot", 2, "Blue and black"),
        (13, "Diagnostic Equipment Set for Ward", 2, "Stainless steel"),
        (13, "Hollow Ware Set, Ward", 2, "Stainless steel"),
        (13, "Instrument Set, Delivery", 2, "Stainless steel"),
        (13, "Instrument Set, Stitch Removing", 2, "Stainless steel"),
        (13, "MVA Kit", 5, "Plastic container"),
        (13, "Stool, Laboratory", 5, "Blue"),
        (15, "Penguin Sucker", 3, "Plastic container in penguin shape"),
        (15, "Fetoscope, Doppler", 3, ""),
        (15, "Bubble CPAP", 2, ""),
        (15, "Centrifuge, Electric", 2, "Blue and white"),
        (15, "Kangaroo Mother Care Chair", 1, "Brown"),
        (15, "Radiant Infant Warmer", 2, "White and red"),
        (15, "Haemoglobin Meter, Sahli", 2, ""),
        (15, "Examination Light", 1, "Head-mounted surgical lamp"),
        (17, "Instrument Set, ENT Basic for HCIII", 2, "Stainless steel"),
        (17, "Bag Valve Mask, Ambu Bag, Neonatal", 15, ""),
        (17, "Office Chair", 7, "Black with stainless-steel frame"),
        (17, "Desk", 5, "Wooden, black, with metallic stand"),
        (19, "Filing Cabinet", 2, "Grey metallic"),
        (19, "Non-Residential Clinical Building Block", 4, "OPD and maternity buildings"),
        (19, "Residential Staff-Quarter Block", 2, "Two staff-quarter blocks"),
        (19, "Pit Latrine Stance", 4, "Two female and two male stances"),
        (19, "Bathroom", 4, "Two female and two male bathrooms"),
        (19, "Water Tank, 3,000 Litre", 1, ""),
        (19, "Water Tank, 10,000 Litre", 2, "One connected to a pump"),
        (19, "Water Pump", 2, "One pump reported installed"),
        (19, "Placenta Pit", 1, ""),
        (19, "Waste Pit", 1, ""),
    ]
    records = []
    for page, asset, quantity, details in checklist:
        records.append(register_source_record(
            facility_id="X041", lg=facility.lg, facility=facility.name,
            asset=f"{asset} - {details}" if details else asset,
            source_file=relative, source_locator=f"PDF page {page}",
            quantity=quantity,
            quantity_basis="handwritten quantity beside checklist item",
            remarks="Quantity manually transcribed from the scanned facility return.",
            asset_details=details,
        ))
    return records


def shift_column_dimensions_for_insert(ws, insert_at: int) -> None:
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


def asset_keys(value: object) -> list[str]:
    text = clean_text(value)
    base = re.split(r"\s+-\s+", text, maxsplit=1)[0]
    keys = [normalized_key(text), normalized_key(base)]
    return list(dict.fromkeys(key for key in keys if key))


def source_template_rows(ws_source, ws_register) -> dict[str, int]:
    headers = [cell.value for cell in ws_source[1]]
    index = {name: position for position, name in enumerate(headers)}
    templates: dict[str, int] = {}
    for row in ws_source.iter_rows(min_row=2, values_only=True):
        first = row[index["Register first row"]]
        asset = row[index["Asset in source"]]
        if not first or not asset:
            continue
        for key in asset_keys(asset):
            templates.setdefault(key, int(first))
    return templates


def template_row_for_asset(asset: object, templates: dict[str, int], *, health: bool) -> int:
    for key in asset_keys(asset):
        if key in templates:
            return templates[key]
    wanted = asset_keys(asset)[-1]
    first_word = wanted.split()[0] if wanted else ""
    candidates = [key for key in templates if key.startswith(first_word + " ") or key == first_word]
    if not candidates:
        candidates = [key for key in templates if first_word and first_word in key]
    if candidates:
        score, match = max((SequenceMatcher(None, wanted, key).ratio(), key) for key in candidates)
        if score >= 0.55:
            return templates[match]
    defaults = ("stethoscope", "b p machine digital") if health else ("school desks", "desk")
    for default in defaults:
        if default in templates:
            return templates[default]
    raise ValueError(f"No classification template is available for {asset!r}")


def location_display(lg: str) -> str:
    upper = clean_text(lg).upper()
    if upper in MDA_NAMES:
        return upper
    if upper.endswith(" MC") or upper.endswith(" CITY"):
        return upper
    return f"{upper} DLG"


def append_new_records(workbook, master: MasterData) -> dict[str, int]:
    register = workbook["Asset Register"]
    source = workbook["Source Lines"]
    source_headers = [cell.value for cell in source[1]]
    source_index = {name: position + 1 for position, name in enumerate(source_headers)}
    existing_record_keys = {
        (
            clean_text(source.cell(row, source_index["Facility ID"]).value),
            normalized_key(source.cell(row, source_index["Source locator"]).value),
            normalized_key(source.cell(row, source_index["Asset in source"]).value),
        )
        for row in range(2, source.max_row + 1)
    }
    candidate_records = [
        *latest_western_records(master),
        *lwamata_records(master),
        *sofia_records(master),
        *makokoto_health_records(master),
        *team30_school_records(master),
    ]
    records = [
        record for record in candidate_records
        if (
            clean_text(record["Facility ID"]),
            normalized_key(record["Source locator"]),
            normalized_key(record["Asset in source"]),
        ) not in existing_record_keys
    ]
    if not records:
        return {"source_lines_added": 0, "asset_rows_added": 0}

    templates = source_template_rows(source, register)
    location_by_lg: dict[str, str] = {}
    for row in range(2, register.max_row + 1):
        book = clean_text(register.cell(row, 1).value)
        location = clean_text(register.cell(row, 10).value)
        if book and location:
            location_by_lg.setdefault(book, location)

    max_reference = max(
        (
            int(match.group(1))
            for row in range(2, source.max_row + 1)
            if (match := re.fullmatch(r"SRC-(\d+)", clean_text(source.cell(row, 1).value)))
        ),
        default=0,
    )
    register_max_column = register.max_column
    source_max_column = source.max_column
    current_register_row = register.max_row
    current_source_row = source.max_row
    source_style_row = current_source_row
    added_rows = 0
    for record in records:
        max_reference += 1
        source_ref = f"SRC-{max_reference:06d}"
        first_register_row = current_register_row + 1
        facility = master.facility_by_id[clean_text(record["Facility ID"])]
        book = book_code(facility.lg)
        health = "health centre" in facility.name.casefold()
        template_row = template_row_for_asset(record["Asset in source"], templates, health=health)
        quantity = int(record["quantity"])
        for item_number in range(1, quantity + 1):
            current_register_row += 1
            target_row = current_register_row
            copy_row(register, template_row, target_row, register_max_column)
            description = (
                f"{record['Asset in source']} - {facility.name} - {facility.lg} "
                f"[{source_ref}; item {item_number} of {quantity}]"
            )
            register.cell(target_row, 1).value = book
            register.cell(target_row, 2).value = facility.name
            register.cell(target_row, 3).value = description
            register.cell(target_row, 9).value = 1
            register.cell(target_row, 10).value = location_by_lg.get(book, location_display(facility.lg))
            register.cell(target_row, 14).value = None
            register.cell(target_row, 33).value = None
            life = record.get("life_months")
            if isinstance(life, (int, float)) and not isinstance(life, bool) and math.isfinite(float(life)) and float(life) > 0:
                register.cell(target_row, 36).value = int(float(life))
            for column in (38, 39, 41, 43, 44, 45, 46, 47, 49):
                register.cell(target_row, column).value = None
            status_text = normalized_key(f"{record.get('Original condition', '')} {record.get('Source remarks and qualifications', '')}")
            if "not in use" in status_text:
                register.cell(target_row, 48).value = "NO"
            elif "in use" in status_text:
                register.cell(target_row, 48).value = "YES"
            for column in range(51, register_max_column + 1):
                register.cell(target_row, column).value = None
            added_rows += 1
        last_register_row = current_register_row

        current_source_row += 1
        target_source_row = current_source_row
        copy_row(source, source_style_row, target_source_row, source_max_column)
        source.cell(target_source_row, source_index["Source reference"]).value = source_ref
        source.cell(target_source_row, source_index["Register first row"]).value = first_register_row
        source.cell(target_source_row, source_index["Register last row"]).value = last_register_row
        source.cell(target_source_row, source_index["Items represented"]).value = quantity
        for header in source_headers[4:]:
            source.cell(target_source_row, source_index[header]).value = record.get(header)
        retarget_source_line_formulas(
            register, first_register_row, last_register_row, target_source_row
        )

    if source.auto_filter.ref:
        source.auto_filter.ref = f"A1:{get_column_letter(source_max_column)}{current_source_row}"
    return {"source_lines_added": len(records), "asset_rows_added": added_rows}


def synchronize_asset_table(ws) -> None:
    table = ws.tables["AssetRegister"]
    headers = [ws.cell(1, column).value for column in range(1, ws.max_column + 1)]
    if len(table.tableColumns) == ws.max_column - 1 and headers[1] == "FACILITY_NAME":
        table.tableColumns.insert(1, TableColumn(id=2, name="FACILITY_NAME"))
    if len(table.tableColumns) != ws.max_column:
        raise ValueError(
            f"AssetRegister has {len(table.tableColumns)} table columns but the worksheet has {ws.max_column} columns"
        )
    for column_number, (column, header) in enumerate(zip(table.tableColumns, headers), 1):
        column.id = column_number
        column.name = str(header)
    table.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
    if table.autoFilter is not None:
        table.autoFilter.ref = table.ref


def update_read_me(ws, *, removed_rows: int, added_rows: int, final_rows: int) -> None:
    replacements = {
        "Template": (
            "The Asset Register sheet preserves the supplied template fields and adds "
            "FACILITY_NAME immediately after BOOK_TYPE_CODE, for 65 columns in total. "
            "The illustrative laptop row was removed."
        ),
        "Missing information": (
            "BOOK_TYPE_CODE and FACILITY_NAME are resolved from reconciled facility IDs, "
            "facility folders, source-line values, exact source worksheet rows and section "
            "headers, and explicit facility/LG text in source descriptions. District- or "
            "MDA-wide registers use the owning entity when no more specific facility is "
            f"recorded. {removed_rows:,} asset rows without a valid facility or traceable owner "
            f"were removed; {added_rows:,} rows from the latest source batch were added. "
            f"The final register contains {final_rows:,} asset rows."
        ),
    }
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=3):
        label = row[0].value
        if label in replacements:
            row[1].value = replacements[label]
        if label == "BOOK_TYPE_CODE":
            row[1].value = (
                "Derive from the reconciled or source-traced local government/MDA, remove "
                "DLG/district wording, retain MC or City where applicable, and append ' BK'."
            )
            row[2].value = "Sample Header of Asset Register..xlsx; source-line reconciliation"


def latest_source_totals(ws) -> tuple[int, int]:
    headers = [cell.value for cell in ws[1]]
    index = {name: position + 1 for position, name in enumerate(headers)}
    legacy_prefix = f"{LATEST_ROOT.relative_to(ROOT).as_posix()}/"
    source_lines = 0
    asset_rows = 0
    for row in range(2, ws.max_row + 1):
        source_file = clean_text(ws.cell(row, index["Source file"]).value)
        if source_file not in LATEST_SOURCE_FILES and not source_file.startswith(legacy_prefix):
            continue
        source_lines += 1
        asset_rows += int(ws.cell(row, index["Items represented"]).value)
    return source_lines, asset_rows


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


def build(path: Path, from_git_head: bool, dry_run: bool = False) -> dict[str, object]:
    workbook = load_input(path, from_git_head)
    master = MasterData()
    lg_by_row, facility_by_row, rules, unresolved, kept_source_refs = source_maps(
        workbook["Source Lines"], master
    )

    register = workbook["Asset Register"]
    facility_column, _ = ensure_facility_column(register)
    original_rows = register.max_row - 1
    kept_rows = set(lg_by_row) & set(facility_by_row)
    if not dry_run:
        expected_register_rows = set(range(2, register.max_row + 1))
        if kept_rows == expected_register_rows:
            row_map = {row: row for row in expected_register_rows}
        else:
            row_map = compact_register(register, kept_rows)
        source_sheet = workbook["Source Lines"]
        if source_rows_are_all_retained(source_sheet, kept_source_refs):
            source_row_map = {row: row for row in range(2, source_sheet.max_row + 1)}
        else:
            source_row_map = compact_source_lines(source_sheet, kept_source_refs, row_map)
        remapped_formula_count = remap_source_line_formulas(register, source_row_map)
        lg_by_row = {row_map[old_row]: value for old_row, value in lg_by_row.items() if old_row in row_map}
        facility_by_row = {row_map[old_row]: value for old_row, value in facility_by_row.items() if old_row in row_map}
        additions = append_new_records(workbook, master)
    else:
        row_map = {row: row for row in kept_rows}
        remapped_formula_count = 0
        additions = {"source_lines_added": 0, "asset_rows_added": 0}
    headers = [cell.value for cell in next(register.iter_rows(min_row=1, max_row=1))]
    location_column = headers.index("LOCATION_SEGMENT1") + 1

    stats: Counter = Counter()
    examples: list[tuple[int, str | None, str | None]] = []
    for row_number in range(2, register.max_row + 1):
        lg = lg_by_row.get(row_number)
        if not lg and dry_run:
            lg = master.canonical_lg(register.cell(row_number, location_column).value)
            if lg:
                rules["LG: register location"] += 1

        retained_or_new = not dry_run or row_number in kept_rows
        book = book_code(lg)
        facility = facility_by_row.get(row_number)
        if retained_or_new:
            book = book or clean_text(register.cell(row_number, 1).value) or None
            facility = facility or clean_text(register.cell(row_number, facility_column).value) or None
        register.cell(row_number, 1).value = book
        register.cell(row_number, facility_column).value = facility
        stats["populated_book" if book else "blank_book"] += 1
        stats["populated_facility" if facility else "blank_facility"] += 1
        if len(examples) < 12 and (not book or not facility):
            examples.append((row_number, book, facility))

    synchronize_asset_table(register)
    current_removed_rows = original_rows - len(kept_rows)
    total_source_lines_added, total_asset_rows_added = latest_source_totals(workbook["Source Lines"])
    removed_rows = ORIGINAL_REGISTER_ASSET_ROWS + total_asset_rows_added - (register.max_row - 1)
    if removed_rows < 0:
        raise ValueError("Final register exceeds the original rows plus traced new-source rows.")
    update_read_me(
        workbook["Read Me"], removed_rows=removed_rows,
        added_rows=total_asset_rows_added, final_rows=register.max_row - 1,
    )
    workbook.calculation.calcMode = "auto"
    workbook.calculation.fullCalcOnLoad = True
    workbook.calculation.forceFullCalc = True

    if dry_run:
        workbook.close()
    else:
        save_atomically(workbook, path)

    return {
        "populated_book": stats["populated_book"],
        "blank_book": stats["blank_book"],
        "populated_facility": stats["populated_facility"],
        "blank_facility": stats["blank_facility"],
        "rules": rules,
        "unresolved": unresolved,
        "unresolved_examples": examples,
        "removed_rows": removed_rows,
        "source_lines_added": total_source_lines_added,
        "asset_rows_added": total_asset_rows_added,
        "current_removed_rows": current_removed_rows,
        "current_source_lines_added": additions["source_lines_added"],
        "current_asset_rows_added": additions["asset_rows_added"],
        "final_rows": register.max_row - 1,
        "remapped_formula_count": remapped_formula_count,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_PATH)
    parser.add_argument(
        "--from-git-head", action="store_true", help="Start from the clean committed workbook."
    )
    parser.add_argument("--dry-run", action="store_true", help="Resolve and report values without saving.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    stats = build(args.path, args.from_git_head, args.dry_run)
    print(
        f"Filled BOOK_TYPE_CODE on {stats['populated_book']:,} rows; "
        f"left blank {stats['blank_book']:,}."
    )
    print(
        f"Filled FACILITY_NAME on {stats['populated_facility']:,} rows; "
        f"left blank {stats['blank_facility']:,}."
    )
    print(
        f"Removed {stats['removed_rows']:,} rows without a valid facility or traceable owner; "
        f"added {stats['asset_rows_added']:,} rows from {stats['source_lines_added']:,} new source lines. "
        f"Final register: {stats['final_rows']:,} rows."
    )
    print(f"Retargeted {stats['remapped_formula_count']:,} Source Lines formula references.")
    print("Resolution rules:")
    for rule, count in stats["rules"].most_common():
        print(f"  {count:>7,}  {rule}")
    for field in ("lg", "facility"):
        print(f"Top unresolved {field} sources:")
        for source_file, count in stats["unresolved"][field].most_common(12):
            print(f"  {count:>7,}  {source_file}")
    if stats["unresolved_examples"]:
        print("First unresolved rows:", stats["unresolved_examples"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
