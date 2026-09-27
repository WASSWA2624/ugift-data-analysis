"""Build the MF and REF asset registers from the shared SK workbook.

Follows outputs/PROMPT_POPULATE_ASSET_REGISTERS.md, Stage 2 (MF), the
sanitising rules, and Stage 3 (REF). The SK workbook is the Stage 1 register and
is not rewritten.

    python scripts/build_guideline_registers.py            # both workbooks
    python scripts/build_guideline_registers.py --limit 5000   # a quick sample run
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import textwrap
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fill_borrowed_costs import (
    GENERIC as GENERIC_BORROW_NAMES,
    add_donor,
    common_life,
    groups_for,
    median,
    norm_name,
    parse_date,
    row_years,
    shillings,
    usable_name,
)
from fill_clear_template_fields import classify
from merge_shared_asset_registers import blank_tag, canonical_item, clean
from ugift_places import (
    LocalGovernment,
    canonical_facility,
    facility_display,
    facility_kind,
    is_placeholder,
    lg_from_text,
    resolve_lg,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "asset-register-2026-09-23"
SK = OUT / "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx"
MF = OUT / "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
REF = OUT / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
SAMPLE = ROOT / "Sample Header of Asset Register..xlsx"
ANNEX1 = ROOT / "reference" / "annex1_asset_classes.csv"
ANNEX2 = ROOT / "reference" / "annex2_asset_accounts.csv"

AS_OF = date(2026, 9, 30)
FY_START = date(2026, 7, 1)
UNIT = re.compile(r"\s*\[item \d+ of \d+\]\s*$", re.I)
# The 15 columns of the SK template, carried into ATTRIBUTE1-ATTRIBUTE15 in this
# order. Each MF header reads ATTRIBUTEn(<SK column>).
SK_COLUMNS = (
    "Equipment/ Item", "Department", "Asset Number", "Item Description", "Life in Months",
    "Tag Number (engrave no.)", "Date Of Purchase", "Date Placed In Service", "Recoverable cost",
    "Cost", "Acc Dep Cost", "Net Book Value", "Ytd Deprn", "Equipment status", "Remarks",
)
ATTRIBUTE = {position: f"ATTRIBUTE{position}({name})" for position, name in enumerate(SK_COLUMNS, 1)}
DATE_FORMAT = "yyyy-mm-dd"
# Department of the vote a facility of each kind belongs to, used only when the
# source left the Department cell empty. A hospital's assets sit under its hospital
# services department in Location(3)2.xlsx; a ministry's under UNSPECIFIED (the
# master's own value where a vote has no department split, e.g. MOLG).
KIND_DEPARTMENT = {
    "Health centre": "HEALTH", "School": "EDUCATION", "Hospital": "HOSPITAL SERVICES", "MDA": "UNSPECIFIED",
    "Blood bank": "UNSPECIFIED", "Local government office": "ADMINISTRATION AND MANAGEMENT", "Health facility": "HEALTH",
}
# Facility types whose names are kept as written (no Seed Secondary School or Health
# Centre III suffix): central-government rows and the few local-government offices.
CENTRAL_KINDS = {"MDA", "Hospital", "Blood bank", "Local government office", "Health facility"}
# Section 3.3.3: small office equipment and loose tools are expensed on 221012.
# Section 3.3.3: small office equipment and loose tools, "kettles, spoons, forks,
# calculators, stapling machines, pen-holders, punches, paper trays, pin and staple
# holders, type writer etc.", and items of the same nature the returns list: small
# office and kitchen ware, hand tools and cleaning items, computer accessories that are
# no asset on their own, and single-patient or measuring aids.
LOOSE = re.compile(
    r"\b(kettles?|spoons?|(?<!tuning )forks?(?!\s?lift)|cutlery|knives|plates|cups|mugs|jugs|flasks?(?!\s*(?:volumetric|conical|erlenmeyer|round))|thermos(?:es)?|"
    r"calculators?|stap+lers?|stap+ling machines?|pen-?holders?|punches|punch|punching machines?|paper punch(?:es|ers)?|paper trays?|"
    r"(?:office|file|document|letter|desk|in|out) trays?|pin-?holders?|staple holders?|drawing pins?|office pins?|pins?(?!\s*boards?)\b|type\s?writers?|"
    r"wall clocks?|clocks?|stop ?watch(?:es)?|timers?|scissors?|cord scissors?|spatulas?|rulers?|dusters?|files?(?:\s+and\s+folders?)?\b(?!\s*(?:cabinet|server))|folders?|"
    r"(?:mid[- ]upper[- ]arm|muac|measuring|tape) ?measures?|(?:mid[- ]upper[- ]arm|muac) tapes?|tape measures?|"
    r"buckets?|disinfection buckets?|basins?(?!\s*(?:stand|unit))|bins?|waste bins?|dust ?bins?|pedal bins?|mops?|brooms?|brushes|torch(?:es)?|padlocks?|hammers?|spanners?|screw ?drivers?|pliers|wrench(?:es)?|"
    r"keyboards?|mouses?|mice|computer mice|cables?|power cables?|extension cables?|chargers?|adapt[eo]rs?|flash disks?|usb sticks?|memory cards?|surge protectors?|power surge protectors?|"
    r"penguin suckers?|bulb suckers?|tongue depressors?)\b|^\s*trays?\s*$",
    re.I,
)
# A service or subscription is not a controlled tangible resource with service
# potential beyond a year (section 3.2.1.2): internet connectivity for a period,
# engraving, testing and commissioning, installation as a line of its own.
SERVICE = re.compile(
    r"(?i)^\s*(?:(?:computer\s+)?software\b[^;]*\bsubscriptions?\b|"
    r"(?:annual|monthly|yearly)\s+(?:computer\s+)?software\b|"
    r"(?:internet|wifi|wi-fi|data|network)\s*(?:connection|connectivity|subscription|bundle|services?)\b|"
    r"engrav(?:ing|ement)s?\b|testing and commissioning|installation(?:\s+(?:of|services?|works?))?\s*$|training\b|"
    r"(?:annual|monthly|yearly)\s+(?:licen[cs]e|subscription|fee)|warranty\b|maintenance\s*(?:services?|contract)?\s*$|"
    r"(?:transport(?:ation)?|delivery|freight|shipping)\s+(?:costs?|charges?|fees?)|labou?r\s+(?:costs?|charges?))"
)
CONSUMABLE = re.compile(
    r"\b(glassware|(?:volumetric|conical|erlenmeyer|round[- ]bottom|flat[- ]bottom) flasks?|beakers?|pipettes?|burettes?|"
    r"pack of|packs?\b|pkts?|single[- ]use|surgic\w* packs?|graph paper|filter paper|cover slips?|slides?,? pack|microscope slides?|"
    r"gloves|syringes?(?!\s*pumps?)|cotton wool|bandages?|reagents?|test strips?|toner|cartridges?|stationery|"
    r"chalk(?!\s*boards?)|exercise books?|text ?books?|papers?(?!\s*(?:shredders?|cutters?|trimmers?))|"
    r"tubings?|visking|labels?|droppers?|petri dish(?:es)?|bulbs?|fl[ou]{1,2}rescent tubes?|test tubes?|test tube (?:racks?|holders?)|corks?|bungs?|rubber bungs?|"
    r"crocodile clips?|litmus|indicator paper|reels?|rolls?|\bboxe?s? of\b|wires?(?!\s*gauze)|boiling tube brushes|"
    r"cannulas?|canulars?|canular|nasal cannulas?|ticker tape|wire ga[u]?ges?|catheters?|swabs?|needles?(?!\s*(?:holders?|destroyers?|cutters?))|plasters?|"
    r"instruction manuals?|manuals?|goggles?|assorted tyres|tyres?|iron fil+ings|petri ?dish(?:es)?)\b",
    re.I,
)
NATURAL = re.compile(r"\b(natural resources?|mineral rights?|wildlife|forests?|wetlands?|rivers?|lakes?)\b", re.I)
NON_DEPR = re.compile(
    r"\b(work in progress|\bwip\b|under\s+constr\w+|operating lease|incomplete(?:\s+building)?|"
    r"(?:on-?\s?going|ongoing)(?:\s+constructions?)?|still\s+(?:under|being)\s+\w+|not\s+(?:yet\s+)?complet\w+|"
    r"unfinished|not\s+finished|pending\s+completion|constr[au]ction\s+(?:on-?going|ongoing|in progress))\b",
    re.I,
)
# Section 3.2.1 condition 3: the asset must exist. A row whose status says it was
# never received, or whose remark says the asset itself is missing, lost or stolen.
NOT_EXISTING = re.compile(
    r"\bnot\s+(?:yet\s+)?(?:received|delivered|supplied)\b|\bnever\s+(?:received|delivered)\b|"
    r"\bdidn'?t\s+receive\b|\bnot\s+among\b|\bwas\s+not\s+(?:delivered|supplied)\b|"
    r"^\s*(?:missing|lost|stolen|disposed|taken away|not there)\b|\b(?:is|are|was|were|got|went|been)\s+(?:missing|lost|stolen|disposed|taken away)\b|"
    r"(?<!not )(?<!never )(?<!no )(?<!nothing )\b(?:stolen|lost)\b(?!\s+(?:and\s+)?(?:replaced|recovered|found))|"
    # Section 3.2.1 condition 3 also fails where the verification team could not find
    # the asset, or the source says it was disposed of, written off or condemned.
    r"\bnot\s+(?:yet\s+)?(?:seen|verified|found|traced|available|physically\s+verified)\b|\bcould\s+not\s+be\s+(?:seen|traced|verified|found)\b|"
    r"\bunable\s+to\s+(?:see|trace|verify|find)\b|\bdisposed\s*(?:off?)?\b|\bwritten\s+off\b|\bcondemned\b|\bbo(?:a)?r?ded\s+off\b|"
    r"\bclaims?\b.{0,30}\b(?:lost|stolen|missing)\b",
    re.I,
)
TOTAL_LINE = re.compile(r"(?i)^\s*(?:sub|grand)?\s*totals?\b|\btotal\s+(?:equipment|asset|units?|quantit)")
REPAIR = re.compile(
    r"(?i)^\s*(?:repairs?|servicing|maintenance|overhaul)\s+(?:of|to|for)\b|\bspare\s+(?:parts?|tyres?|bottles?)\b|"
    r"\breplacement\s+(?:parts?|engine|battery|tyres?)\b"
)
GENERIC_HEAD = re.compile(
    r"(?i)^(?:\w+[\s\-]+){0,2}(?:equipments?|items?|sets?|machines?|furnitures?|assorted.*|schools?|hospitals?|assets?|tools?|materials?|fittings?)$|^assorted\b"
)
FAULTY = re.compile(
    r"\bnot\s+(?:yet\s+)?(?:been\s+)?(?:in\s+|being\s+)?(?:use|used|usable|service|installed|assembled|fixed|connected|"
    r"function\w*|working|operational|available|received|delivered|supplied|seen|there|found)\b|"
    r"\bnot\s+(?:all\s+)?(?:in\s+)?(?:a\s+)?(?:very\s+)?good\b|\bnot\s+(?:in\s+)?(?:good\s+)?(?:working\s+)?(?:condition|order|state|shape)\b|"
    r"(?<!not )(?<!non-)(?<!non )(?<!un)damag|(?<!not )(?<!non-)(?<!non )(?<!un)broken|obsolete|unserviceable|\bfault|\bdisposed\b|\blost\b|"
    r"\bmissing\b|\bstolen\b|spoil|repairs?\s+(?:required|needed)|needs?\s+repair|under\s+repair|\bdead\b|non[- ]?function|"
    r"dys-?function|mal-?function|out\s+of\s+(?:use|order|service)|\bcracked\b|\bworn\s*out\b|\bin\s+(?:the\s+)?stores?\b|grounded|"
    r"didn'?t\s+receive|\bidle\b|\bcondemned\b|written\s+off|\b(?:poor|bad)\b(?:\s+(?:condition|state|shape))?|\btorn\b|\bno\s+power\b|"
    r"\bleak\w*|\bexpired\b|\brotten\b|\brusty\b",
    re.I,
)
FUNCTIONAL = re.compile(
    r"\bin\s+(?:active\s+|daily\s+|full\s+)?use\b|(?<!non)(?<!non-)(?<!non )(?<!dys)(?<!mal)\bfunction\w*|working\s+well|\bworking\b|"
    r"\bavailable\b|verified|good\s+condition|\bgood\b|"
    r"\bok(?:ay)?\b|\bnew\b|excellent|operational|(?<!un)serviceable|\bfine\b|\bintact\b|\brunning\b|\bwell\b|\bfair\b|\busable\b",
    re.I,
)
# "not in use", "non functional": the words after the negation are not evidence of use.
NEGATED_CLAUSE = re.compile(r"(?i)\b(?:not|non|no|never|neither|without|un)\b[\s\-]*(?:yet\s+)?(?:\w+[\s\-]*){0,4}")
# A line that splits the group: "16 in use and 13 not", "some broken", "1 not in good
# condition, others good", "verified 180 stools of which 9 stools were broken".
MIXED = re.compile(
    r"(?i)\b(?:some|others?|except|whereas|while|the\s+rest|remaining|partly|partially|not\s+all|a\s+few|few|majority|most\s+of)\b|"
    r"\bfunction\w*\s*(?:and|/|,|&)?\s*non[\s\-]*function|"
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:[a-z]+\s+){0,2}(?:are\s+|were\s+|is\s+|was\s+)?"
    r"(?:not\b|non[\s\-]|broken|damaged|faulty|spoilt?|missing|stolen|dead|lost|obsolete|unserviceable|out\s+of|in\s+(?:the\s+)?stores?\b)"
)
PLACEHOLDER_TEXT = re.compile(r"(?i)^(n/?a|na|nil+|none|null|-+|–|—|not applicable|not indicated|\.+|…+|_+)$")
MONEY = {"FIXED_ASSETS_COST", "DEPRN_RESERVE", "YTD_DEPRN", "SALVAGE_VALUE"} | {ATTRIBUTE[n] for n in (9, 10, 11, 12, 13)}
BLUE = PatternFill("solid", fgColor="9DC3E6")
ORANGE = PatternFill("solid", fgColor="F4B183")
GREEN = PatternFill("solid", fgColor="C6EFCE")
FILLS = {1: BLUE, 2: ORANGE, 3: GREEN}


# ------------------------------------------------------------------ references

def read_headers() -> list[str]:
    """The sample header, with ATTRIBUTEn renamed ATTRIBUTEn(<SK column>)."""
    workbook = load_workbook(SAMPLE, read_only=True, data_only=True)
    row = [clean(value) for value in next(workbook.active.iter_rows(max_row=1, values_only=True))]
    workbook.close()
    renamed = []
    for value in row:
        match = re.fullmatch(r"ATTRIBUTE(\d+)", value)
        renamed.append(ATTRIBUTE.get(int(match.group(1)), value) if match else value)
    return renamed


def annex1() -> dict[str, dict]:
    """Annex 1 rows keyed by minor 2 class name (normalised)."""
    classes: dict[str, dict] = {}
    with ANNEX1.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = norm_name(row["asset_category_minor2"])
            months = row["life_months"]
            classes[key] = {
                "major": row["asset_category_major"],
                "minor1": row["asset_category_minor1"],
                "minor2": row["asset_category_minor2"],
                "depreciate": row["depreciate"].strip().lower() == "yes",
                "method": row["deprn_method"] if row["deprn_method"] not in {"N/A", ""} else "",
                "months": int(months) if months.isdigit() else None,
                "salvage": 0 if row["salvage_value"].strip() == "0" else None,
            }
    return classes


ANNEX2_BY_MINOR2 = {
    "residential buildings": "312111", "other dwellings": "312119", "non residential buildings": "312121",
    "buildings other than dwellings": "312129", "roads and bridges": "312131", "airports and airfields": "312132",
    "railways and subways": "312133", "oil pipelines reservoirs": "312134", "water supply systems": "312135",
    "power lines stations plants": "312136", "ict network lines": "312137", "other structures": "312139",
    "heavy vehicles": "312211", "light vehicles": "312212", "water vessels": "312213", "aircrafts": "312214",
    "train engines and wagons": "312215", "cycles": "312216", "other transport equipment": "312219",
    "light ict hardware": "312221", "heavy ict hardware": "312222", "television radio transmitter": "312223",
    "other ict equipment": "312229", "office equipment": "312231", "electrical machinery": "312232",
    "med lab research appliances": "312233", "precision optical instruments": "312234",
    "furniture and fittings": "312235", "musical instruments": "312236", "sports equipment": "312237",
    "road furniture": "312238", "plant machinery": "312239", "computer software": "312423",
    "computer databases": "312424", "research and development": "312421",
}


# ------------------------------------------------------------------- helpers

def plain(value: object) -> str:
    """One clean text: trimmed, single spaces, no line breaks; a placeholder is blank."""
    text = clean(value)
    if not text or PLACEHOLDER_TEXT.match(text) or is_placeholder(text):
        return ""
    return text


def as_number(value: object) -> int | float | None:
    if isinstance(value, bool) or value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return int(value) if float(value).is_integer() else float(value)
    text = plain(value)
    text = re.sub(r"(?i)^(ugx|ush|shs?\.?|sh|@)\s*[.:]?\s*", "", text)
    text = re.sub(r"(?i)(\s*(ugx|ush|shs?|/=|/-|/|each|only|per\s+unit|@|-|=)\.?)+\s*$", "", text).strip()
    million = re.fullmatch(r"(?i)(\d+(?:\.\d+)?)\s*m(?:illion)?", text)
    if million:
        return int(float(million.group(1)) * 1_000_000)
    # A thousands group written with a space or a comma and a space: "760 000", "668, 133".
    text = re.sub(r"(?<=\d)[ ,]\s*(?=\d{3}(?:\D|$))", "", text).replace(",", "")
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        number = float(text)
        return int(number) if number.is_integer() else number
    return None


def as_life(value: object) -> int | float | None:
    """Life in months from '60', '20 months', '7 yrs', '5 years'."""
    number = as_number(value)
    if number is not None:
        return number
    text = plain(value)
    match = re.fullmatch(r"(?i)(\d+(?:\.\d+)?)\s*(months?|mths?|mos?|yrs?|years?)\.?", text)
    if not match:
        return None
    amount = float(match.group(1))
    if match.group(2).lower().startswith("y"):
        amount *= 12
    return int(amount) if amount.is_integer() else amount


def as_date_text(value: object) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return plain(value)


def normalise_date_text(text: str) -> str:
    """'26/04 /2021', '23rd-10-23', '08th/02/24', 'I6/05/2025' written the one way."""
    text = re.sub(r"(?i)(?<=\d)\s*(?:st|nd|rd|th)\b", "", text)
    text = re.sub(r"\s*([/.\-])\s*", r"\1", text)
    text = re.sub(r"(?<![A-Za-z])[Il](?=\d)", "1", text)
    text = re.sub(r"^(\d{1,2})-(\d{1,2})-(\d{2,4})$", r"\1/\2/\3", text)
    return text


def as_date(value: object) -> date | None:
    """A real date where the source states one. Wording that states no date
    ("Not given", "Not yet in use") is no date; the text goes to Remarks."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = plain(value)
    if not text or not re.search(r"\d", text) or re.match(r"(?i)^(?:not|no|none|nil|still|pending|yet|un)\b", text):
        return None
    return parse_date(text) or parse_date(normalise_date_text(text))


# Status wording typed without spaces or with a dash for "non": one spelling before
# the Functional and Faulty patterns are applied.
STATUS_SPLITS = (
    (re.compile(r"(?i)\bgood\s*and\s*functional\b|\bgoodandfunctional\b"), "good and functional"),
    (re.compile(r"(?i)\bgoodcondition\b"), "good condition"),
    (re.compile(r"(?i)\bverygood\b"), "very good"),
    (re.compile(r"(?i)\bstillingoodcondition\b"), "still in good condition"),
    (re.compile(r"(?i)\bnotfunctional\b|\bnotfunctioning\b"), "not functional"),
    (re.compile(r"(?i)\bnone[\s\-–—]*functional\b|\bnon[\s\-–—]+function"), "non function"),
    (re.compile(r"(?i)\bnotinuse\b|\bnot\s+in-use\b"), "not in use"),
    (re.compile(r"(?i)\binuse\b"), "in use"),
    (re.compile(r"(?i)\bbutfaulty\b"), "but faulty"),
    (re.compile(r"(?i)\bafunctioning\b"), "a functioning"),
)
IN_USE = re.compile(r"(?i)(?<!not )(?<!never )(?<!no longer )\bin\s+(?:active\s+|daily\s+|full\s+)?use\b")


def status_words(status: str) -> str:
    text = plain(status).replace("–", "-").replace("—", "-")
    for pattern, replacement in STATUS_SPLITS:
        text = pattern.sub(replacement, text)
    return text


def condition(status: str) -> tuple[str, str]:
    """('Functional' | 'Faulty' | '', longer wording for Remarks)."""
    text = status_words(status)
    if not text:
        return "", ""
    negative = bool(FAULTY.search(text))
    # The positive words inside a negated clause ("not in use") are not counted.
    positive = bool(FUNCTIONAL.search(NEGATED_CLAUSE.sub(" ", text)))
    numbers = re.findall(r"\d+", text)
    mixed = bool(MIXED.search(text)) or (positive and negative and len(numbers) >= 2)
    if mixed and (negative or positive):
        # The line splits the group; the source does not say which unit this is.
        label = ""
    elif IN_USE.search(text) and not NOT_EXISTING.search(text):
        # "In use but in poor condition": the asset is in use (IN_USE_FLAG YES); the
        # condition wording stays in Remarks.
        label = "Functional"
    elif negative:
        label = "Faulty"
    elif positive:
        label = "Functional"
    else:
        label = ""
    longer = "" if label and re.fullmatch(r"(?i)functional|faulty|functioning|good|in use|working|ok(?:ay)?|good condition", text) else text
    return label, longer


def year_only_date(text: str) -> date | None:
    """A source date given only as a year ('2025') or a financial year ('FY 2022/23',
    '2021-2022'): the first month of that year, or 1 July of that financial year."""
    value = plain(text).casefold()
    value = re.sub(r"^(?:fy|f/y|financial\s+year)\s*[:\-]?\s*", "", value).strip()
    match = re.fullmatch(r"((?:19|20)\d{2})\s*[/\-]\s*((?:19|20)?\d{2})", value)
    if match:
        first = int(match.group(1))
        second = int(match.group(2))
        second = second + (first // 100) * 100 if second < 100 else second
        if second == first + 1:
            return date(first, 7, 1)
        return None
    match = re.fullmatch(r"(?:19|20)\d{2}", value)
    if match and 1990 <= int(value) <= AS_OF.year:
        return date(int(value), 1, 1)
    return None


# Median stated price per asset name over the whole workbook, filled by index_sources;
# a donor price twenty times above or below it is a line total or a typing slip.
PRICE_MEDIAN: dict[str, float] = {}
PRICE_BAND = 20.0
# Donors for a row whose name has no priced match: the Annex 1 class (same government,
# then other governments), and for the placed-in-service month the other assets of
# the same facility, then of the same government, then of the whole workbook.
CLASS_COSTS: dict = {}
CLASS_MEDIAN: dict[str, float] = {}
FACILITY_MONTHS: dict[tuple[str, str], Counter] = {}
LG_MONTHS: dict[str, Counter] = {}
ALL_MONTHS: Counter = Counter()
# The guidelines' general life for equipment (3.2.2 illustration; most Annex 1
# machinery classes): applied to an asset whose name Annex 1 does not class.
FALLBACK_LIFE = 60
# A unit cost under this amount is immaterial and is carried at nil (shown as "-").
MIN_COST = 10_000
# Plausibility band of a price against its Annex 1 class median, used where the
# name has fewer than three stated prices; wider than the name band because a class
# spans stools and cupboards alike.
CLASS_BAND = 50.0
MONEY_FORMAT = '#,##0.##;-#,##0.##;"-"'
# Every row of the sample header carries fund 01 (the Consolidated Fund).
FUND_SEGMENT = "01"
NOT_ENGRAVED = "Not engraved"
COUNT_NEGATIVE = re.compile(
    r"(?i)(\d+)\s*(?:[a-z]+\s+){0,3}?(?:non[\s\-]*function\w*|not\s+(?:function\w*|working|in\s+use|good)|broken|damaged|faulty|spoilt?|dead|obsolete|missing|lost|stolen|unserviceable)"
)
COUNT_POSITIVE = re.compile(r"(?i)(\d+)\s*(?:[a-z]+\s+){0,3}?(?:function\w*|working|good|in\s+use|operational|verified)")


def majority_status(text: str) -> str:
    """'133 functional 43 non-functional': the larger stated count decides the group's
    units; '' when the wording gives no counts or they tie."""
    negative = sum(int(match.group(1)) for match in COUNT_NEGATIVE.finditer(text))
    stripped = COUNT_NEGATIVE.sub(" ", text)
    positive = sum(int(match.group(1)) for match in COUNT_POSITIVE.finditer(stripped))
    if positive > negative:
        return "Functional"
    if negative > positive:
        return "Faulty"
    return ""


def denies_asset(text: str, item: str, description: str = "") -> bool:
    """A whole-row absence, excluding a partial group or another named item."""
    text = status_words(text)
    if not NOT_EXISTING.search(text):
        return False
    positive = FUNCTIONAL.search(NEGATED_CLAUSE.sub(" ", text))
    subset = re.search(r"(?i)\b(some|others?|except|the rest|remaining|a few|partly|partially)\b", text)
    if MIXED.search(text) and (positive or subset):
        return False
    subject = re.search(
        r"(?i)\b((?:[a-z]+\s+){0,3}[a-z]+)\s+(?:was|were|is|are|has|have)\s+"
        r"(?:not|never)\s+(?:been\s+)?(?:delivered|supplied|received)\b", text,
    )
    if subject:
        words = {word for word in norm_name(subject.group(1)).split()
                 if len(word) > 3 and word not in {
                     "item", "items", "asset", "assets", "equipment", "this", "that",
                     "they", "these", "those", "were", "which",
                 }}
        if words and not words & set(norm_name(f"{item} {description}").split()):
            return False
    return True


def clean_description(text: str) -> str:
    """The item description as field wording: trimmed, one space, no stray
    punctuation, a capital first letter; nothing when the cell held only a count, a
    unit word or a placeholder."""
    value = plain(text)
    value = re.sub(r"\s*[;,]\s*$", "", value).strip(" .-_/")
    value = re.sub(r"\s+([,;:.])", r"\1", value)
    if not value or re.fullmatch(r"(?i)[\d\s.,/()-]+|pcs?|pieces?|units?|nos?\.?|set|sets|item|items|same|ditto|as above|\"|''", value):
        return ""
    if len(value) < 2:
        return ""
    return value[:1].upper() + value[1:]


def borrow_key(bare: str) -> str:
    """The name assets are matched on for borrowing: normalised, with the last word
    made singular so Desks borrow from Desk and Desktop computers from Desktop computer."""
    words = norm_name(bare).split()
    if not words:
        return ""
    last = words[-1]
    if len(last) > 3 and not re.fullmatch(r"\d+", last):
        if re.search(r"(?:ches|shes|xes|sses)$", last):
            last = last[:-2]
        elif last.endswith("ies"):
            last = last[:-3] + "y"
        elif last.endswith("s") and not last.endswith("ss"):
            last = last[:-1]
    words[-1] = last
    return " ".join(words)


def plausible(values: list, name: str) -> list:
    """Donor prices inside the plausibility band of the name's workbook-wide median.
    With fewer than three stated prices for the name nothing can be excluded."""
    centre = PRICE_MEDIAN.get(name)
    if centre is None or centre <= 0:
        return values
    kept = [value for value in values if centre / PRICE_BAND <= value <= centre * PRICE_BAND]
    return kept


def month_index(value: date) -> int:
    return value.year * 12 + value.month - 1


def month_date(index: int) -> date:
    return date(index // 12, index % 12 + 1, 1)


# Department cells that name no department: a category word, "all", a facility name.
DEPARTMENT_NOISE = re.compile(
    r"(?i)^(?:all(?:\s+departments?)?|every|general|various|assorted|equipments?|furnitures?|school furniture|buildings?|books|items?|assets?|"
    r"in\s+store|health cent(?:re|er)\s*(?:iii|3)?|seed(?:\s+secondary)?\s+school|ugift)$"
)
FACILITY_IN_DEPARTMENT = re.compile(r"(?i)\b(?:health cent(?:re|er)|hc\s*iii|h/?c\s*iii|seed secondary school|seed school|secondary school|s\.?s\.?s?\b)")


def location_department(department: str) -> str:
    """The department for LOCATION_SEGMENT2: counts dropped from a list ("OPD 02;
    MATERNITY 01"), and nothing where the cell named a facility or a category of
    items rather than a department."""
    text = department
    if not text:
        return ""
    if ";" in text or re.search(r"\b0\d\b", text):
        text = re.sub(r"\s*\b\d{1,3}\b(?=\s*(?:;|,|/|$))", "", text)
        text = re.sub(r"\s*;\s*", "; ", text).strip(" ;,/")
    if not text or DEPARTMENT_NOISE.match(text) or FACILITY_IN_DEPARTMENT.search(text):
        return ""
    return text


def department_text(value: str) -> str:
    text = plain(value)
    if not text or not re.search(r"[A-Za-z]{2}", text):
        return ""
    if re.fullmatch(r"(?i)(?:not\s+\w+(?:\s+\w+)?|missing|nil|none|n/?a)", text):
        # A status typed in the department column names no department.
        return ""
    text = re.sub(r"\s*[\(\[]\s*\d{1,3}\s*[\)\]]", "", text)
    text = re.sub(r"\s*;\s*", "; ", text)
    text = re.sub(r"\s+", " ", text).strip(" ;,")
    upper = text.upper()
    for pattern, replacement in DEPARTMENT_SYNONYMS:
        upper = re.sub(pattern, replacement, upper)
    upper = re.sub(r"\s+", " ", upper)
    # One spelling of each department once: "EDUCATION; EDUCATION; OFFICE" -> "EDUCATION; OFFICE".
    tokens: list[str] = []
    for token in re.split(r"\s*;\s*", upper):
        token = token.strip(" ,.-")
        if token and token not in tokens:
            tokens.append(token)
    return "; ".join(tokens)


# One spelling of a department across the returns (applied in order).
DEPARTMENT_SYNONYMS = (
    (r"\bEDN\b|\bEDUC\b|\bEDUCATIONAL\b|\bEDUCATION\s+(?:DEPT|DEPARTMENT|SECTOR|SECONDARY)\b", "EDUCATION"),
    (r"\bHEALTH\s+(?:DEPT|DEPARTMENT|SERVICES?|FACILIT(?:Y|IES)|SECTOR)\b|\bHEALTHSERVICES\b", "HEALTH"),
    (r"\bSCIENCE\s+LABS?\b|\bSCIENCE\s+LABORATOR(?:Y|IES)\b|\bSCI\s+LAB\b", "SCIENCE LABORATORY"),
    (r"\bICT\s+LABS?\b|\bICT\s+LABORATORY\b|\bCOMPUTER\s+LABS?\b|\bCOMPUTER\s+LABORATORY\b", "ICT LABORATORY"),
    (r"\bLABS?\b|\bLABORATORIES\b", "LABORATORY"),
    (r"\bCLASS\s*ROOMS?\b", "CLASSROOM"),
    (r"\bSTAFF\s*R(?:OO)?M\b", "STAFF ROOM"),
    (r"\bADMIN\b", "ADMINISTRATION"),
    (r"\bMAT\b", "MATERNITY"),
    (r"\bPEDIATRIC\b", "PAEDIATRIC"),
    (r"\bLABOUR\s+SUIT\b", "LABOUR SUITE"),
    (r"\bHOSP\b", "HOSPITAL"),
    (r"\bH\s*/?\s*C\s*(?:III|3)\b|\bHCIII\b|\bHEALTH\s+CENTER\s+III\b", "HEALTH CENTRE III"),
    (r"\s+(?:DEPT|DEPARTMENT)\b", ""),
)


ACRONYMS = {
    "UPS", "CPU", "LED", "LCD", "TV", "HP", "BP", "ICT", "PC", "USB", "DVD", "CD", "LG", "AC", "DC", "ENT", "MCH",
    "OPD", "IPD", "VIP", "PVC", "GI", "HDMI", "LAN", "WIFI", "ID", "ESR", "CPAP", "MVA", "VHF", "UHF", "PA", "HIV",
    "TB", "KVA", "KW", "ML", "MM", "CM", "KG", "GB", "TB", "RAM", "SSD", "HDD", "CCTV", "DSTV", "GPS", "IT", "ICU",
    "MRI", "CT", "ECG", "PPE", "HB", "BPM", "FM", "AM", "UV", "IV", "PSA", "APC", "MSI", "IEC", "UK", "USA",
}
ACRONYM = re.compile(r"^[A-Z]+\d+[A-Z\d]*$|^\d+[A-Z]+$")
GENERIC_NAMES = {
    "asset", "assets", "others", "other", "various", "assorted", "assorted items", "assorted laboratory glassware and apparatus",
    "assorted glassware", "assorted apparatus", "fittings", "building", "buildings",
    "structure", "structures", "block", "blocks", "equipments", "tools", "materials", "furniture and fittings", "ict",
    "ict equipment", "electrical", "electricals", "machinery", "machine", "items", "item", "set", "sets", "kit", "kits",
}
GENERIC_NAMES.update(GENERIC_BORROW_NAMES)


def display_item(name: str) -> str:
    """One spelling of an item name: an all-capitals name is written in title case,
    keeping short acronyms (UPS, CPU, LED, HP) and model codes as written."""
    text = clean(name)
    if not text or re.search(r"[a-z]", text):
        return text
    words = []
    for word in text.split():
        core = re.sub(r"[^A-Za-z0-9]", "", word)
        if core in ACRONYMS or ACRONYM.match(core) or re.search(r"\d", core) or len(core) <= 1:
            words.append(word)
        else:
            words.append(word[:1] + word[1:].lower())
    return " ".join(words)


def styled_cell(sheet, header: str, value, fill=None) -> WriteOnlyCell:
    """An amount with thousands separators, a date written one way, and the borrowed-
    value colour where one applies."""
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    cell = WriteOnlyCell(sheet, value=value)
    if header in MONEY and isinstance(value, (int, float)):
        cell.number_format = MONEY_FORMAT
    elif isinstance(value, (date, datetime)):
        cell.number_format = DATE_FORMAT
    if fill is not None:
        cell.fill = fill
    return cell


def remark_bundle(parts: list[str]) -> str:
    kept: list[str] = []
    for part in parts:
        text = plain(part)
        if text and text not in kept:
            kept.append(text)
    return "; ".join(kept)


def months_between(start: date, end: date) -> int:
    return (end.year - start.year) * 12 + end.month - start.month + 1


def depreciation(cost: float, residual: float, life: int, placed: date) -> tuple[float, float] | None:
    """(accumulated to 30 September 2026, July-September 2026 charge)."""
    if life <= 0 or placed > AS_OF or cost <= residual:
        return None
    monthly = (cost - residual) / life
    served = min(months_between(placed, AS_OF), life)
    accumulated = monthly * served
    # Year to date: the months of July-September 2026 that fall inside the useful life.
    last_month_index = placed.year * 12 + placed.month - 1 + life - 1
    fy_first = FY_START.year * 12 + FY_START.month - 1
    as_of_index = AS_OF.year * 12 + AS_OF.month - 1
    start_index = max(fy_first, placed.year * 12 + placed.month - 1)
    end_index = min(as_of_index, last_month_index)
    ytd_months = max(0, end_index - start_index + 1)
    return accumulated, monthly * ytd_months


# ------------------------------------------------------------------- classes

class Registers:
    def __init__(self, headers: list[str]):
        self.headers = headers
        self.annex1 = annex1()
        self.class_cache: dict[str, tuple | None] = {}

    def classify(self, bare: str):
        """Annex 1 class for a bare item name, or None. Generic names, totals, counts,
        consumable packs, and loose tools have no class."""
        key = bare.casefold()
        if key in self.class_cache:
            return self.class_cache[key]
        found = None
        if bare and not TOTAL_LINE.search(bare) and not REPAIR.search(bare) and not re.fullmatch(r"-?\d+", bare):
            found = extra_classify(bare) or classify(bare)
            if found and (LOOSE.search(bare) or CONSUMABLE.search(bare)):
                # "Microscope slides pack of 72", "Rubber bungs for conical flasks": the
                # pack, not the apparatus it serves, is what the line names.
                found = None
            if found:
                # Annex 1 decides life, method and salvage for the class it names.
                row = self.annex1.get(norm_name(found[2]))
                if row:
                    found = (row["major"], row["minor1"], row["minor2"], row["months"], row["depreciate"])
        self.class_cache[key] = found
        return found

MACHINERY = "MACHINERY AND EQUIPMENT"
OTHER = "OTHER MACHINERY AND EQUIPMENT"
EXTRA_CLASSES = (
    # The registered asset is explicitly software, even when its name states
    # that the licences are for computers. Hardware bundled with software keeps
    # its hardware class because this rule requires a software-led item name.
    (re.compile(r"(?i)^\s*(?:computer\s+)?software\b"),
     ("OTHER FIXED ASSETS", "INTELLECTUAL PROPERTY PRODUCTS", "COMPUTER SOFTWARE", 60, True)),
    # Spellings the source uses that the shared classifier misses; the Annex 1 row
    # then supplies life and method.
    (re.compile(r"(?i)\b(sterili[sz](?:ation|ing|er)?\s*drums?|dressing\s*drums?|instrument\s*drums?|b\.?\s*p\.?\s*cuffs?|blood\s*pressure\s*cuffs?|delivery\s*(?:sets?|kits?)|"
                r"suture\s*(?:sets?|kits?)|dressing\s*(?:sets?|kits?)|instrument\s*(?:sets?|kits?)|hollow\s*ware|penguin\s*suckers?|kidney\s*dish(?:es)?|gallipots?|galipots?)\b"),
     (MACHINERY, OTHER, "MED LAB RESEARCH APPLIANCES", 60, True)),
    (re.compile(r"(?i)\b(cap\s*boards?|cup\s*boards?|cubboards?|cardboards?\s+(?:cupboard|wardrobe)|double\s*basins?|wash\s*(?:hand\s*)?basins?|sinks?|inbuilt\s*shelves|"
                r"soft\s*boards?|display\s*boards?|book\s*shelves|book\s*shelf|reading\s*tables?)\b"),
     (MACHINERY, OTHER, "FURNITURE AND FITTINGS", 60, True)),
    (re.compile(r"(?i)\b(megaphones?|public\s*address(?:\s*systems?)?|pa\s*systems?|loud\s*hailers?|hand\s*sets?|desk\s*phones?|telephone\s*sets?)\b"),
     (MACHINERY, "ICT EQUIPMENT", "OTHER ICT EQUIPMENT", 60, True)),
    # Field spellings of laboratory and medical apparatus.
    (re.compile(r"(?i)\b(hollo\s*ware|holloware|retr?ort\s*stands?|con?u?nting\s*chambers?|ph\s*meters?|g[\s\-]?clamps?|(?:concave|convex|concavex)\s*mirrors?|"
                r"cell\s*washers?|(?:blood\s*)?(?:coagulation|congulation)\s*an[a]?l?y[sz]ers?|an[a]?l?y[sz]ers?|cool\s*boxes|cold\s*boxes|vaccine\s*carriers?|instrument\s*trays?|"
                r"(?:^|\s)p\.?\s*machine,?\s*digital|examinat\s*ion\s*(?:couch|bed|light)?|heat\s*sources?|bunsen\s*burners?|spirit\s*lamps?|tripods?)\b"),
     (MACHINERY, OTHER, "MED LAB RESEARCH APPLIANCES", 60, True)),
    (re.compile(r"(?i)\b(notices?\s*boards?|din\s*boards?|pin\s*boards?|glass\s*lights?|lock\s*ups?|hairs)\b"),
     (MACHINERY, OTHER, "FURNITURE AND FITTINGS", 60, True)),
    (re.compile(r"(?i)\b(lap\s*tops?|systems?\s*units?|cable\s*locks?)\b"),
     (MACHINERY, "ICT EQUIPMENT", "LIGHT ICT HARDWARE", 60, True)),
    (re.compile(r"(?i)\b(solar(?:\s*systems?|\s*panels?|\s*power|\s*batter(?:y|ies))?|air\s*conditions?|air\s*conditioners?|power\s*cables?|extension\s*cables?)\b"),
     (MACHINERY, OTHER, "ELECTRICAL MACHINERY", 60, True)),
    (re.compile(r"(?i)\b(tanks?|water\s*tanks?|h?ash\s*pits?|hashpits?|placenta\s*pits?|blockplacenta\s*pits?|tents?|fences?|gates?)\b"),
     ("BUILDINGS AND STRUCTURES", "STRUCTURES", "OTHER STRUCTURES", 240, True)),
    (re.compile(r"(?i)\b(staff\s*qua[rt]+ers?|teachers?['’]?\s*qua[rt]+ers?|staff\s*houses?)\b(?!.*\b(latrine|latrin|toilet|kitchen)\b)"),
     ("BUILDINGS AND STRUCTURES", "DWELLINGS", "RESIDENTIAL BUILDINGS", 600, True)),
    (re.compile(r"(?i)\b(wheel\s*chairs?|stop\s*watch(?:es)?|bowl,?\s*kick|kick\s*bowls?|balances?|volumetric flasks?|flasks?|"
                r"micrometer(?: screw)? gauges?|vernier|mortars? and pestles?|retort stands?|dissecting (?:kits?|sets?)|ammeters?|"
                r"voltmeters?|galvanometers?|spatulas?|wash bottles?|glass blocks?|tripod stands?|thermometers?|microscopes?|"
                r"forceps|autoclaves?|sterili[sz]ers?|oxygen cylinders?|patient beds?|hospital beds?|delivery beds?|examination couch(?:es)?|"
                r"weighing scales?|drip stands?|patient screens?|blood pressure machines?|bp machines?|syringe pumps?|tuning forks?)\b"),
     (MACHINERY, OTHER, "MED LAB RESEARCH APPLIANCES", 60, True)),
    (re.compile(r"(?i)\b(?:convex|concave|converging|diverging|plane)\b.*\b(?:lens(?:es)?|mirrors?)\b|\b(?:lens(?:es)?|mirrors?)\b.*\b(?:convex|concave|converging|diverging)\b|\bmagnifying glass(?:es)?\b"),
     (MACHINERY, OTHER, "PRECISION OPTICAL INSTRUMENTS", 60, True)),
    # A building named after what it houses ("Library and computer block", "Main hall",
    # "2-stance VIP latrin") is a building, so these come before the equipment words.
    (re.compile(r"(?i)\b(staff quarters?|teachers?['’]?\s*quarters?|staff houses?|teachers?['’]?\s*houses?|dormitor(?:y|ies)|hostels?)\b(?!.*\b(latrine|latrin|toilet|kitchen)\b)"),
     ("BUILDINGS AND STRUCTURES", "DWELLINGS", "RESIDENTIAL BUILDINGS", 600, True)),
    (re.compile(r"(?i)\b(blocks?|halls?|latrines?|latrins?|toilets?|kitchens?|class\s*rooms?|classrooms?|wards?|ict-?library|library)\b(?!\s*(?:materials|books?|shel))"),
     ("BUILDINGS AND STRUCTURES", "BUILDINGS OTHER THAN DWELLINGS", "NON RESIDENTIAL BUILDINGS", 600, True)),
    (re.compile(r"(?i)\b(concrete work\s*tops?|work\s*tops?|sports? fields?|play\s*grounds?|hand ?washing facilit(?:y|ies)|land\s*scaping|landscaping|fenc(?:e|es|ing)|walkways?|pav(?:ing|ements?)|drainage systems?|perimeter walls?|water tanks?|rain ?water harvest\w*)\b"),
     ("BUILDINGS AND STRUCTURES", "STRUCTURES", "OTHER STRUCTURES", 240, True)),
    (re.compile(r"(?i)\b(cpus?|cpu_light duty|central processing units?|desktop computers?|computers?|laptops?|monitors?|keyboards?|printers?|photo\s*copiers?|scanners?|projectors?|routers?|network switch(?:es)?|switch(?:es)?\b.*\b(?:port|network|lan)|ups\b|uninterrupt\w* power suppl(?:y|ies)|tablets?|smart ?phones?|tela phones?|"
                r"switch(?:es)?|fire\s*walls?|patch panels?|network racks?|server racks?|racks?|network video recorders?|nvrs?|access points?|surge protectors?|power surge protectors?)\b"),
     (MACHINERY, "ICT EQUIPMENT", "LIGHT ICT HARDWARE", 60, True)),
    (re.compile(r"(?i)\b(artery forceps?|dis+ecting forceps?|spong[e]? holding forceps?|forceps?|stet[eh]o?scopes?|bowel lotions?|kidney trays?|kidney dish(?:es)?|"
                r"pulx?oxy?meters?|pulse oximeters?|oximeters?|sphygmomanometers?|nebuli[sz]ers?|suction machines?|resuscitators?|otoscopes?|fetoscopes?|"
                r"glucometers?|haemoglobinometers?|centrifuges?|colorimeters?|incubators?|refrigerators?|fridges?|freezers?)\b"),
     (MACHINERY, OTHER, "MED LAB RESEARCH APPLIANCES", 60, True)),
    (re.compile(r"(?i)\b(servers?|server processors?)\b"), (MACHINERY, "ICT EQUIPMENT", "HEAVY ICT HARDWARE", 60, True)),
    # Annex 1 row 7: a local area network installation is an ICT network line.
    (re.compile(r"(?i)^\s*lan\b|\blocal\s+area\s+network\b|\blan\s+(?:installation|cabling|network|infrastructure)\b|\bstructured\s+cabling\b"),
     ("BUILDINGS AND STRUCTURES", "STRUCTURES", "ICT NETWORK LINES", 240, True)),
    # The ministries' fleets: Annex 1 rows 14 (light vehicles) and 18 (cycles).
    (re.compile(r"(?i)\b(motor\s*cycles?|motorbikes?|boda\s*bodas?|yamaha\s+xtz|bicycles?)\b"),
     (MACHINERY, "TRANSPORT EQUIPMENT", "CYCLES", 60, True)),
    (re.compile(r"(?i)\b(motor\s*ve[ch]{2}icles?|ve[ch]{2}icles?|double\s*cabin|pick[- ]?ups?|toyota\s+hilux|hilux|ford\s+ranger|land\s*cruiser|prado|station\s*wagons?|"
                r"saloon\s*cars?|mini\s*bus(?:es)?|ambulances?|vans?\b|trucks?)\b"),
     (MACHINERY, "TRANSPORT EQUIPMENT", "LIGHT VEHICLES", 60, True)),
    (re.compile(r"(?i)\b(single seats?|seats?|desks?|deks|chairs?|stools?|bench(?:es)?|tables?|shel(?:f|ves?|ve)|cupboards?|cabinets?|carbinets?|cabinates?|carbinates?|lockers?|"
                r"mattress(?:es)?|matress(?:es)?|notice\s*boards?|chalk\s*boards?|black\s*boards?|white\s*boards?|wardrobes?|pigeon boxes|beds?(?!\s*(?:side|rock)))\b"),
     (MACHINERY, OTHER, "FURNITURE AND FITTINGS", 60, True)),
    (re.compile(r"(?i)\b(paper shredders?|shredders?|photocopiers?|fax machines?|laminators?|binding machines?|safes?|wall clocks?|clocks?)\b"),
     (MACHINERY, OTHER, "OFFICE EQUIPMENT", 60, True)),
    (re.compile(r"(?i)\bnon\s*-?\s*residential\b"),
     ("BUILDINGS AND STRUCTURES", "BUILDINGS OTHER THAN DWELLINGS", "NON RESIDENTIAL BUILDINGS", 600, True)),
    (re.compile(r"(?i)(?<!non)(?<!non )(?<!non-)\bresidential\b(?!.*\b(latrine|toilet|kitchen)\b)"),
     ("BUILDINGS AND STRUCTURES", "DWELLINGS", "RESIDENTIAL BUILDINGS", 600, True)),
    (re.compile(r"(?i)\b(class\s*rooms?|classrooms?|administration blocks?|admin blocks?|office blocks?|laborator(?:y|ies) blocks?|science blocks?|"
                r"library blocks?|ict blocks?|multi-?purpose halls?|dining halls?|assembly halls?|kitchens?|latrines?|toilets?|bathrooms?|washrooms?|sick bays?|wards?|"
                r"theatre blocks?|store blocks?|opd blocks?|mch blocks?|maternity wards?|placenta pits?|incinerators?|buildings?\b(?!\s*materials))\b"),
     ("BUILDINGS AND STRUCTURES", "BUILDINGS OTHER THAN DWELLINGS", "NON RESIDENTIAL BUILDINGS", 600, True)),
    (re.compile(r"(?i)\b(?:school|office|hospital|facility|health\s*cent\w*|hc\s*iii?|institutional)?\s*land\b(?!\s*(?:rover|cruiser|line|scap|lord|mark))|^plots?(?: of land)?\b"),
     ("LAND", "LAND", "LAND", None, False)),
)


def extra_classify(bare: str):
    text = bare.casefold()
    for pattern, result in EXTRA_CLASSES:
        if pattern.search(text):
            if result[2] in {"RESIDENTIAL BUILDINGS", "NON RESIDENTIAL BUILDINGS"} and re.search(r"(?i)\b(bed|couch|chair|desk|table|stool|cupboard|shelf|shelves|locker)\b", text):
                # "Shelve (Class room)" is furniture in a classroom, not the classroom.
                continue
            if result[2] == "LAND" and re.search(r"(?i)\b(land\s*line|landline)\b", text):
                continue
            return result
    return None


SERIAL_STOP = {"not", "no", "numbers", "number", "since", "because", "plate", "missing", "unknown", "none", "nil", "na", "n/a", "ised", "isation", "ized"}


def explicit_serial(text: str) -> str:
    match = re.search(r"(?i)\b(?:serial(?:\s*(?:no\.?|number|#))?|s\s*/\s*n|sn)\b\s*[:\-.]?\s*([A-Za-z0-9][A-Za-z0-9./\-]{3,30})\b", text)
    if not match:
        return ""
    token = match.group(1).strip(" .,-/")
    if token.casefold() in SERIAL_STOP or not re.search(r"\d", token) or re.search(r"(?i)\bserial\b.*,\s*\w+.*,\s*\w+", text):
        return ""
    return token


def explicit_model(text: str) -> str:
    if re.match(r"(?i)\s*model\s+(?:of\s+)?(?:human|skeleton|torso|heart|brain|eye|ear|kidney|lung|dna|cell|atom|plant|animal)", text):
        # "Model Human Brain" is a teaching model, not a model number.
        return ""
    match = re.search(r"(?i)\bmodel\s*(?:no\.?|number|#)?\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9./\-]{1,24}(?:\s+[A-Za-z0-9./\-]*\d[A-Za-z0-9./\-]*)?)\b", text)
    if not match:
        return ""
    token = match.group(1).strip(" .,-/")
    if token.casefold() in SERIAL_STOP or re.fullmatch(r"[A-Z][a-z]+", token):
        return ""
    if not (re.search(r"\d", token) or re.fullmatch(r"[A-Z][A-Za-z0-9\-]{2,}", token)):
        return ""
    return token


def explicit_manufacturer(text: str) -> str:
    match = re.search(
        r"(?i)\b(?:made by|manufactured by|manufacturer)\s*[:\-]?\s*([A-Z][A-Za-z0-9&.'\- ]{1,40}?)(?=\s*(?:[;,.(/]|$|\b(?:serial|model|s/n|sn|and|in|with|for)\b))",
        text,
    )
    if not match:
        return ""
    token = clean(match.group(1)).strip(" .,-")
    if not token or token.casefold() in SERIAL_STOP or re.match(r"(?i)^(?:different|various|several|the|a|an|local|some|unknown|not)\b", token):
        return ""
    return token


# ---------------------------------------------------------------- one MF row

def build_values(source: dict, registers: Registers, *, borrow: bool, costs: dict, lives: dict, dates: dict, stats: Counter) -> list:
    item = plain(source.get("Equipment/Item"))
    description = plain(source.get("Item Description"))
    unit = plain(source.get("Unit"))
    bare = display_item(canonical_item(UNIT.sub("", item or description).strip()))
    item_name = display_item(canonical_item(UNIT.sub("", item).strip())) if item else ""
    name = f"{bare} [{unit}]" if unit else bare
    remarks_source = plain(source.get("Remarks"))
    status_text = plain(source.get("Equipment status"))
    status_label, longer_status = condition(status_text)
    if not status_label:
        # No condition in the status cell, or wording that splits the group: the
        # remark decides where it states one; a count majority decides a split group;
        # an asset the team recorded without a condition is taken as functional.
        inferred = condition(remarks_source)[0] if remarks_source else ""
        if denies_asset(status_text, bare, description) or denies_asset(remarks_source, bare, description):
            status_label = "Faulty"
        elif inferred:
            status_label = inferred
            stats["status_from_remark"] += 1
        else:
            status_label = majority_status(f"{status_text} {remarks_source}") or "Functional"
            stats["status_default"] += 1
        longer_status = status_text

    # Place: one spelling per fact.
    lg_text = plain(source.get("Local Government"))
    lg = resolve_lg(lg_text) or lg_from_text(lg_text) if lg_text else None
    kind = plain(source.get("Facility type"))
    facility_text = plain(source.get("Facility"))
    if kind in CENTRAL_KINDS or (lg is not None and lg.kind == "MDA" and not kind):
        # A ministry, agency or hospital row: the site is written as the source states
        # it, and a vote with no site named takes the location master's UNSPECIFIED.
        kind = kind if kind in CENTRAL_KINDS else "MDA"
        facility = facility_text or "UNSPECIFIED"
    else:
        kind = "School" if kind.casefold().startswith(("school", "seed")) else "Health centre" if kind.casefold().startswith("health") else facility_kind(facility_text)
        facility = canonical_facility(facility_text, lg, kind)[0] if facility_text else ""
        if facility:
            facility = facility_display(facility, kind or facility_kind(facility))
    if lg is None and lg_text:
        book_code = fallback_book_code(lg_text)
        segment1 = fallback_segment1(lg_text)
    else:
        book_code = lg.book_type_code if lg else None
        segment1 = lg.location_segment1 if lg else None

    # Class, life, depreciation. A generic item name is classified from the description.
    total_line = bool(TOTAL_LINE.search(bare))
    repair = bool(REPAIR.search(bare) or (description and REPAIR.search(description)))
    service = bool(SERVICE.search(bare))
    classified = None if total_line or repair or service else registers.classify(bare)
    if classified is None and description and not total_line and not repair and (GENERIC_HEAD.match(bare) or not registers.classify(bare)):
        classified = registers.classify(display_item(canonical_item(description)))
    class_word = bare if registers.classify(bare) else (description if classified else bare)
    loose = bool(LOOSE.search(class_word)) and not (classified and not LOOSE.search(class_word))
    consumable = bool(CONSUMABLE.search(class_word)) and not classified
    if classified is None:
        loose = bool(LOOSE.search(bare) or (description and LOOSE.search(description) and GENERIC_HEAD.match(bare)))
        consumable = bool(CONSUMABLE.search(bare) or (description and CONSUMABLE.search(description) and GENERIC_HEAD.match(bare)))
    natural = bool(NATURAL.search(bare))
    non_depr = bool(NON_DEPR.search(f"{bare} {description}"))
    major = minor1 = minor2 = ""
    class_life = None
    class_depreciates = False
    if classified:
        major, minor1, minor2, class_life, class_depreciates = classified
    if major == "BUILDINGS AND STRUCTURES" and (NON_DEPR.search(remarks_source) or NON_DEPR.search(status_text)):
        # Section 5.5: a building still under construction is work in progress.
        non_depr = True
    life = as_life(source.get("Life in Months"))
    if life is not None and (not isinstance(life, (int, float)) or life <= 0):
        life = None
    source_life = life
    if life is not None and life < 12:
        # Section 3.2.1.2: a non-current asset serves beyond one year, so a stated life
        # under twelve months is unclear wording ("3" for three years?). The class life
        # applies; the stated figure stays in ATTRIBUTE5 on the MF workbook.
        stats["life_short"] += 1
        life = None
    life_source = life is not None
    if life is None and class_life and class_depreciates:
        life = class_life
    is_land = major == "LAND"
    # A line that is not a non-current asset: a total, a repair, a service, a
    # consumable, a loose tool (3.3.3) or a natural resource (3.2.1.4).
    non_asset = total_line or repair or service or consumable or loose or natural
    if non_asset:
        # Expensed or not recognised: no life or depreciation; a stated life stays in
        # ATTRIBUTE5 on the MF workbook.
        life = None
        life_source = False
        major = minor1 = minor2 = ""
    elif life is None:
        # Annex 1 gives every class a life (land 600 months, though it does not
        # depreciate); an asset Annex 1 does not class takes the guidelines' general
        # equipment life of 60 months.
        life = class_life or FALLBACK_LIFE
        if class_life is None:
            stats["life_default"] += 1
    if minor2:
        stats["class"] += 1
    # Section 5.5: straight line where a life applies.
    depreciates = bool(life) and not is_land and not non_depr and not non_asset
    if classified and not class_depreciates and not life_source:
        depreciates = False

    cost_source = as_number(source.get("Cost"))
    # Numeric zero is a recorded immaterial cost, distinct from an absent price.
    # Preserve it; only missing prices or demonstrated positive-price outliers
    # can be replaced by a comparable amount.
    cost = cost_source
    cost_fill = None
    cost_outlier = False
    life_fill = None
    date_fill = None
    # A date the source states is written one way (ISO); wording stays as written.
    purchase_value = as_date(source.get("Date Of Purchase"))
    purchase_text = purchase_value.isoformat() if purchase_value else as_date_text(source.get("Date Of Purchase"))
    placed_source = as_date(source.get("Date Placed In Service"))
    placed_text = placed_source.isoformat() if placed_source else as_date_text(source.get("Date Placed In Service"))
    years = row_years(purchase_text, placed_text)
    asset_name = borrow_key(bare)
    minor_key = norm_name(minor2)
    lg_key = lg.key if lg else ""
    specific = (bool(classified) or usable_name(asset_name)) and asset_name not in GENERIC_NAMES and not GENERIC_HEAD.match(bare) \
        and not total_line and not repair and not service
    if borrow and cost is not None and cost > 0 and not non_depr:
        # A recorded cost twenty times above or below the median for the name (or,
        # where the name has fewer than three prices, fifty times off its class median)
        # is a block total typed on one unit, a divided line total, or a slip: the unit
        # price is borrowed instead and the recorded figure stays in ATTRIBUTE10 on the
        # MF workbook.
        centre = PRICE_MEDIAN.get(asset_name)
        band = PRICE_BAND
        if centre is None and minor_key in CLASS_MEDIAN:
            centre, band = CLASS_MEDIAN[minor_key], CLASS_BAND
        if centre and not (centre / band <= cost <= centre * band):
            cost = None
            cost_outlier = True
            stats["cost_outlier"] += 1
    # Stage 3, the date first: the placed-in-service date the source states, else the
    # purchase date on the same row (the asset was available for use from its
    # purchase), else the first month of the year or financial year the row states.
    # Work in progress is not yet available for use (5.14): no date is derived or
    # borrowed for it, and no completed asset's price is borrowed for it.
    construction = non_depr and major == "BUILDINGS AND STRUCTURES"
    placed = None if construction else placed_source
    if borrow and placed is None and not non_depr:
        if purchase_value:
            placed = purchase_value
            stats["date_purchase"] += 1
        else:
            placed = year_only_date(placed_text) or year_only_date(purchase_text)
            if placed:
                stats["date_year"] += 1
    if borrow and specific and not consumable and not loose and not natural and not non_depr:
        if placed is None:
            # Same asset name; same government, same year else the nearest, then other
            # governments, then the whole workbook. The most common month is taken.
            found = choose(dates, asset_name, lg_key, years, minor_key)
            if found:
                method, groups = found
                months = [value for _, _, bucket in groups for value in bucket]
                placed = month_date(common_life(months))
                date_fill = FILLS[method]
                stats[f"date_{method}"] += 1
        if cost is None:
            found = choose(costs, asset_name, lg_key, years, minor_key)
            if found:
                method, groups = found
                values = plausible([value for _, _, bucket in groups for value in bucket], asset_name)
                if values:
                    cost = shillings(median(values))
                    cost_fill = FILLS[method]
                    stats[f"cost_{method}"] += 1
        if life is None and status_label != "Faulty":
            found = choose(lives, asset_name, lg_key, years, minor_key)
            if found:
                method, groups = found
                values = [value for _, _, bucket in groups for value in bucket]
                life = common_life(values)
                life_fill = FILLS[method]
                stats[f"life_{method}"] += 1
                depreciates = not is_land and not natural and not non_depr
    if borrow:
        if cost is None and specific and not costs.get(asset_name) and not non_asset and not non_depr and minor_key:
            # Step 4: no priced asset of the same name anywhere, so the Annex 1 class
            # supplies the price, same government first, then other governments.
            found = choose(CLASS_COSTS, minor_key, lg_key, years, "")
            if found:
                method, groups = found
                values = [value for _, _, bucket in groups for value in bucket]
                cost = shillings(median(values))
                cost_fill = FILLS[method]
                stats[f"cost_class_{method}"] += 1
        if cost is None and (non_asset or non_depr):
            # A line that is not recognised as an asset, or works with no cost stated,
            # carries no value.
            cost = 0
            stats["cost_nil"] += 1
        elif cost is None:
            stats["cost_unpriced"] += 1
        if cost is not None and 0 <= cost < MIN_COST:
            # An immaterial unit cost is carried at nil and is not capitalized.
            cost = 0
            cost_fill = None
            depreciates = False
            stats["cost_small"] += 1
        if placed is None and not non_depr:
            # The month the other assets of the same facility were placed in service,
            # else of the same government, else of the whole workbook.
            pool = FACILITY_MONTHS.get((lg_key, norm_name(facility_text)))
            method = 1
            if not pool:
                pool = LG_MONTHS.get(lg_key)
            if not pool and ALL_MONTHS:
                pool = ALL_MONTHS
                method = 3
            if pool:
                placed = month_date(pool.most_common(1)[0][0])
                date_fill = FILLS[method]
                stats[f"date_place_{method}"] += 1

    # Section 3.2.1: controlled, service potential beyond a year, exists, measurable.
    # The status column decides existence; a remark counts only when the status is
    # blank or negative itself (a remark about part of a group is not the row's fate).
    # A remark that the line was not delivered, was stolen or is lost denies the row
    # unless it splits the group ("18 were stolen, 10 in use").
    exists = not denies_asset(status_text, bare, description) and not denies_asset(remarks_source, bare, description)
    service_potential = bool(classified) or specific or (life_source and life and life >= 12)
    capitalized = bool(cost) and exists and not loose and not consumable and not natural and not total_line and not repair and not service \
        and not non_depr and service_potential
    if is_land:
        capitalized = bool(cost) and exists
        depreciates = False
    # A building still under construction is work in progress: recorded at the cost
    # the source states, not depreciated (5.5, 5.14), and typed CIP as the earlier
    # register did.
    work_in_progress = non_depr and exists and major == "BUILDINGS AND STRUCTURES" and bool(cost_source)
    if capitalized:
        stats["capitalized"] += 1
    if work_in_progress:
        stats["cip"] += 1

    reserve_source = as_number(source.get("Acc Dep Cost"))
    ytd_source = as_number(source.get("Ytd Deprn"))
    nbv_source = as_number(source.get("Net Book Value"))
    reserve = reserve_source
    ytd = ytd_source
    # Section 5.7: no residual value, on every row.
    salvage = 0
    computed_nbv = None
    # Straight line to 30 September 2026 on a row that exists and whose cost, nil
    # residual, life and placed-in-service month are known; an asset out of use still
    # consumes its life (IPSAS 17). A figure the source recorded stays; the blank one
    # beside it is calculated.
    if borrow and depreciates and exists and cost is not None and life and placed:
        figures = depreciation(float(cost), float(salvage), int(life), placed)
        if figures:
            accumulated, current = figures
            if reserve is None:
                reserve = shillings(accumulated)
                stats["reserve"] += 1
                if ytd is None:
                    # The schedule already stops at the end of the useful life.
                    ytd = shillings(current)
                    stats["ytd"] += 1
            elif ytd is None:
                # Against a reserve the source recorded, the year-to-date charge cannot
                # exceed the depreciation still to be charged.
                remaining = max(0.0, float(cost) - float(salvage) - float(reserve))
                ytd = shillings(min(current, remaining))
                stats["ytd"] += 1
    if borrow and reserve is None:
        # Nothing to charge: no depreciation, no cost, or an asset that does not exist.
        reserve = 0
        stats["reserve_nil"] += 1
    if borrow and ytd is None and reserve is not None:
        ytd = 0
    if cost is not None and reserve is not None:
        # Net book value is the check: cost less accumulated depreciation, never below
        # the residual value.
        computed_nbv = shillings(max(float(salvage or 0), float(cost) - float(reserve)))

    tag_raw = plain(source.get("Tag Number (engrave no.)"))
    tag = NOT_ENGRAVED if blank_tag(tag_raw) else tag_raw
    # Wording in the tag cell beyond a placeholder ("All not engraved yet", "engraved
    # but not numbered") is field information and goes to Remarks.
    engraving_note = tag_raw if tag == NOT_ENGRAVED and tag_raw and not is_placeholder(tag_raw) \
        and not re.fullmatch(r"(?i)(?:not|nor|non)\s*(?:yet\s*)?engra\w*|engraved|not|none|nil|n/?a", tag_raw) else ""
    # Only the description states these (the prompt's rule); the remarks do not.
    serial = explicit_serial(description)
    manufacturer = explicit_manufacturer(description)
    model = explicit_model(description)

    asset_number = plain(source.get("Asset Number"))
    if asset_number and unit:
        total = re.search(r"of (\d+)\]?$", unit)
        if total and re.fullmatch(r"\d+", asset_number) and int(asset_number) == int(total.group(1)):
            asset_number = ""  # that cell was the quantity
    if not asset_number and source.get("_row"):
        # The register's own reference for a row the source did not number.
        asset_number = f"UGIFT-{int(source['_row']):06d}"
        stats["asset_number_reference"] += 1

    recoverable = as_number(source.get("Recoverable cost"))
    recoverable_value = recoverable if recoverable is not None else (plain(source.get("Recoverable cost")) or None)
    if borrow and recoverable is None:
        # No impairment was recorded, so the recoverable amount is the carrying amount.
        recoverable_value = computed_nbv if computed_nbv is not None else (0 if cost == 0 else None)
    department = department_text(source.get("Department"))
    # The department of the vote a facility of this kind belongs to, when the source
    # left the cell empty or named no department; ATTRIBUTE2 keeps the source value.
    segment2 = location_department(department) or KIND_DEPARTMENT.get(kind)
    if not location_department(department) and segment2:
        stats["department_kind"] += 1
    if cost is not None and reserve_source is not None and float(reserve_source) > float(cost):
        stats["reserve_over_cost"] += 1
    # The file path is kept as spelled on disk (a repeated space is part of some names).
    source_file = re.sub(r"[\r\n]+", " ", str(source.get("Source file") or "")).strip()
    source_location = plain(source.get("Source location"))
    # Words typed into an amount column ("133 functional 43 non-functional" under Ytd
    # Deprn) are no amount; they are kept as remarks under the column's name.
    worded_amounts = []
    for column in ("Recoverable cost", "Cost", "Acc Dep Cost", "Net Book Value", "Ytd Deprn"):
        raw = plain(source.get(column))
        if raw and as_number(raw) is None:
            worded_amounts.append(f"{column}: {raw}")
    # Remarks: the source Remarks, the status wording moved out of Equipment status,
    # and every SK field with no column of its own, each labelled with its column name.
    # Remarks carry only what the field recorded: the remark, the status wording, words
    # typed into amount cells, wording in the tag cell, and the SK fields with no
    # column of their own.
    remarks = remark_bundle([
        remarks_source,
        f"Source status: {longer_status}" if longer_status and longer_status.casefold() != status_label.casefold() else "",
        *worded_amounts,
        f"Engraving: {engraving_note}" if engraving_note else "",
        f"Facility type: {kind}" if kind else "",
    ])
    trail = "; ".join(part for part in (f"Source file: {source_file}" if source_file else "", f"Source location: {source_location}" if source_location else "") if part)
    remarks = f"{remarks}; {trail}" if remarks and trail else (remarks or trail)

    # Annex 2: the depreciation expense account of the class (2312xx, as on the sample
    # row) for a capitalized asset; 221012 for small office equipment and loose tools.
    # 513001 is credited whenever an asset is brought into the register (3.2.2
    # illustration), whether or not Annex 1 names its class.
    expense_account = None
    clearing_account = None
    if loose:
        expense_account = "221012"
    elif capitalized or work_in_progress:
        acquisition = ANNEX2_BY_MINOR2.get(norm_name(minor2)) if minor2 else None
        expense_account = "231" + acquisition[3:] if acquisition else None
        clearing_account = "513001"
    # Every row states a life: the Annex 1 or general life, 0 on a line that is no asset.
    life_cell = (life, life_fill) if life else 0
    purchase_cell = purchase_value or (purchase_text if year_only_date(purchase_text) else None)

    values = {
        "BOOK_TYPE_CODE": book_code,
        "DESCRIPTION": name or None,
        "ASSET_CATEGORY_MAJOR": major or None,
        "ASSET_CATEGORY_MINOR1": minor1 or None,
        "ASSET_CATEGORY_MINOR2": minor2 or None,
        # Minor 3 is the item-master level below Annex 1 (its footnote 5); the sample
        # row writes the item name there ("Laptop" for "HP Laptop silver").
        "ASSET_CATEGORY_MINOR3": bare if minor2 else None,
        "ASSET_TYPE": "CAPITALIZED" if capitalized else "CIP" if work_in_progress else None,
        "FIXED_ASSETS_UNITS": 1,
        "LOCATION_SEGMENT1": segment1,
        "LOCATION_SEGMENT2": segment2 or None,
        "LOCATION_SEGMENT3": facility or None,
        # Every location combination in Location(3)2.xlsx closes with UNSPECIFIED, as
        # the sample row does.
        "LOCATION_SEGMENT4": "UNSPECIFIED",
        "FIXED_ASSETS_COST": ((cost, cost_fill) if cost is not None else None) if borrow else cost_source,
        # The fund segment every row of the sample header carries.
        "ASSET_EXP_ACCT_FUND": FUND_SEGMENT,
        "ASSET_EXP_ACCT_ACCOUNT": expense_account,
        "ASSET_CLR_ACCT_ACCOUNT": clearing_account,
        "DATE_PLACED_IN_SERVICE": None if construction else ((placed, date_fill) if borrow and placed else placed_source),
        "DEPRECIATE_FLAG": "YES" if depreciates else "NO",
        "DEPRN_METHOD_CODE": "STL" if depreciates else None,
        "LIFE_IN_MONTHS": life_cell,
        # Section 3.3.5.2: depreciation begins on the first day of the month the asset
        # is available for use; the sample row codes that convention GOU PRO CO, and the
        # book applies one convention to every row.
        "PRORATE_CONVENTION_CODE": "GOU PRO CO",
        "DEPRN_RESERVE": reserve,
        "YTD_DEPRN": ytd,
        "SALVAGE_VALUE": salvage,
        "ASSET_NUMBER": asset_number or None,
        "TAG_NUMBER": tag,
        "SERIAL_NUMBER": serial or None,
        "MANUFACTURER_NAME": manufacturer or None,
        "MODEL_NUMBER": model or None,
        "IN_USE_FLAG": "YES" if status_label == "Functional" else "NO",
        # The SK columns in order. MF carries the source values; REF carries the values
        # after borrowing and calculation, with the same cell colours as the main columns.
        ATTRIBUTE[1]: item_name or bare or None,
        ATTRIBUTE[2]: segment2 or None,
        ATTRIBUTE[3]: asset_number or None,
        ATTRIBUTE[4]: clean_description(description) or None,
        ATTRIBUTE[5]: life_cell if borrow else source_life,
        ATTRIBUTE[6]: tag,
        ATTRIBUTE[7]: purchase_cell,
        ATTRIBUTE[8]: None if construction else (((placed, date_fill) if placed else None) if borrow else placed_source),
        ATTRIBUTE[9]: recoverable_value,
        ATTRIBUTE[10]: ((cost, cost_fill) if cost is not None else None) if borrow else cost_source,
        ATTRIBUTE[11]: reserve if borrow else reserve_source,
        ATTRIBUTE[12]: (nbv_source if nbv_source is not None else computed_nbv) if borrow else nbv_source,
        ATTRIBUTE[13]: ytd if borrow else ytd_source,
        ATTRIBUTE[14]: status_label,
        ATTRIBUTE[15]: remarks or None,
    }
    return [sanitize(values.get(header), header) for header in registers.headers]


def sanitize(value, header: str):
    """Every filled cell: trimmed text, single spaces, no line breaks, placeholders
    cleared, recorded amounts untouched."""
    if value is None:
        return None
    if isinstance(value, tuple):
        return value
    if isinstance(value, (int, float, date, datetime)):
        return value
    if header == "LOCATION_SEGMENT4" or (header in ("LOCATION_SEGMENT2", "LOCATION_SEGMENT3", ATTRIBUTE[2]) and clean(value).upper() == "UNSPECIFIED"):
        # UNSPECIFIED is the location master's own value here, not a placeholder.
        return clean(value) or None
    if header == ATTRIBUTE[15] and isinstance(value, str) and "Source file: " in value:
        # The file path after "Source file:" keeps its spelling; the rest is cleaned.
        head, _, tail = value.partition("Source file: ")
        head = plain(head).rstrip("; ").strip()
        tail = re.sub(r"[\r\n]+", " ", tail).strip()
        return f"{head}; Source file: {tail}" if head else f"Source file: {tail}"
    text = plain(value)
    if not text:
        return None
    if header in ("TAG_NUMBER", ATTRIBUTE[6]) and blank_tag(text):
        return NOT_ENGRAVED
    return text


def fallback_book_code(lg_text: str) -> str | None:
    text = clean(lg_text).upper().replace("\\", "")
    text = re.sub(r"\b(DISTRICT\s+LOCAL\s+GOV(?:ERNMENT|'?T)|DISTRICT|LOCAL\s+GOVERNMENT|DLG|LG)\b", " ", text)
    text = re.sub(r"\b(MUNICIPAL\s+COUNCIL|MUNICIPALITY)\b", "MC", text)
    text = re.sub(r"\bCITY\s+COUNCIL\b", "CITY", text)
    text = re.sub(r"[\-–]", " ", text)
    text = re.sub(r"[^A-Z0-9 ]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return f"{text} BK" if text else None


def fallback_segment1(lg_text: str) -> str | None:
    code = fallback_book_code(lg_text)
    if not code:
        return None
    base = code[:-3].strip()
    if base.endswith(" MC") or base.endswith(" CITY"):
        return re.sub(r"\s*-\s*", r"\\-", base)
    return f"{base} DLG"


# ----------------------------------------------------------------- borrowing

def choose(index: dict, name: str, government: str, years: tuple[int, ...], minor: str):
    """Stage 3 search order: same local government (same year, else closest),
    other local governments, then the whole workbook only when the first two
    steps find no price (a row whose government is not stated)."""
    bucket = index.get(name)
    if not bucket:
        return None
    if government:
        if government in bucket:
            groups = groups_for(bucket, (government,), minor, years)
            if groups:
                return 1, groups
        others = tuple(item for item in bucket if item != government)
        if others:
            groups = groups_for(bucket, others, minor, years)
            if groups:
                return 2, groups
        return None
    groups = groups_for(bucket, tuple(bucket), minor, years)
    return (3, groups) if groups else None


def index_sources(rows_iter, registers: Registers) -> tuple[dict, dict, dict]:
    """Stage 3 donors: stated prices, stated lives, and stated placed-in-service (else
    purchase) months, by asset name, government, class and year."""
    costs: dict = {}
    lives: dict = {}
    dates: dict = {}
    displays: dict = {}
    all_prices: dict[str, list] = {}
    for count, source in enumerate(rows_iter, 2):
        bare = display_item(canonical_item(UNIT.sub("", plain(source.get("Equipment/Item")) or plain(source.get("Item Description"))).strip()))
        asset_name = borrow_key(bare)
        if not usable_name(asset_name) or asset_name in GENERIC_NAMES or GENERIC_HEAD.match(bare) or TOTAL_LINE.search(bare) \
                or REPAIR.search(bare) or CONSUMABLE.search(bare) or LOOSE.search(bare):
            continue
        lg_text = plain(source.get("Local Government"))
        lg = resolve_lg(lg_text) or lg_from_text(lg_text) if lg_text else None
        government = lg.key if lg else ""
        classified = registers.classify(bare)
        minor = norm_name(classified[2]) if classified else ""
        years = row_years(as_date_text(source.get("Date Of Purchase")), as_date_text(source.get("Date Placed In Service")))
        cost = as_number(source.get("Cost"))
        if isinstance(cost, (int, float)) and cost > 0:
            add_donor(costs, displays, asset_name, government, years, minor, shillings(cost), lg_text)
            all_prices.setdefault(asset_name, []).append(shillings(cost))
        life = as_life(source.get("Life in Months"))
        if isinstance(life, (int, float)) and life >= 12:
            add_donor(lives, displays, asset_name, government, years, minor, int(life), lg_text)
        placed = as_date(source.get("Date Placed In Service")) or as_date(source.get("Date Of Purchase"))
        if placed and date(1990, 1, 1) <= placed <= AS_OF:
            add_donor(dates, displays, asset_name, government, years, minor, month_index(placed), lg_text)
        if count % 100000 == 0:
            print(f"indexed {count:,}", flush=True)
    PRICE_MEDIAN.clear()
    PRICE_MEDIAN.update({name: median(values) for name, values in all_prices.items() if len(values) >= 3})
    return costs, lives, dates


def index_fallbacks(rows_iter, registers: Registers) -> None:
    """Class-level prices and facility-, government- and workbook-level placed-in-
    service months, for rows whose name has no priced or dated match."""
    CLASS_COSTS.clear()
    CLASS_MEDIAN.clear()
    FACILITY_MONTHS.clear()
    LG_MONTHS.clear()
    ALL_MONTHS.clear()
    class_prices: dict[str, list] = {}
    displays: dict = {}
    for source in rows_iter:
        bare = display_item(canonical_item(UNIT.sub("", plain(source.get("Equipment/Item")) or plain(source.get("Item Description"))).strip()))
        if TOTAL_LINE.search(bare) or REPAIR.search(bare) or CONSUMABLE.search(bare) or LOOSE.search(bare) or SERVICE.search(bare):
            continue
        lg_text = plain(source.get("Local Government"))
        lg = resolve_lg(lg_text) or lg_from_text(lg_text) if lg_text else None
        government = lg.key if lg else ""
        years = row_years(as_date_text(source.get("Date Of Purchase")), as_date_text(source.get("Date Placed In Service")))
        classified = registers.classify(bare)
        cost = as_number(source.get("Cost"))
        if classified and isinstance(cost, (int, float)) and cost > 0:
            minor = norm_name(classified[2])
            name = borrow_key(bare)
            centre = PRICE_MEDIAN.get(name)
            if centre is None or centre / PRICE_BAND <= cost <= centre * PRICE_BAND:
                add_donor(CLASS_COSTS, displays, minor, government, years, "", shillings(cost), lg_text)
                class_prices.setdefault(minor, []).append(shillings(cost))
        placed = as_date(source.get("Date Placed In Service")) or as_date(source.get("Date Of Purchase"))
        if placed and date(1990, 1, 1) <= placed <= AS_OF:
            index = month_index(placed)
            FACILITY_MONTHS.setdefault((government, norm_name(plain(source.get("Facility")))), Counter())[index] += 1
            LG_MONTHS.setdefault(government, Counter())[index] += 1
            ALL_MONTHS[index] += 1
    CLASS_MEDIAN.update({minor: median(values) for minor, values in class_prices.items() if len(values) >= 3})


def finalize_cost_donors(costs: dict) -> None:
    """Remove wrongly priced donors before government/year priority is applied.

    Otherwise an outlier that is the only local price prevents the search from
    continuing to valid prices in other votes. Empty buckets must also disappear.
    """
    for index, by_class in ((costs, False), (CLASS_COSTS, True)):
        for name, governments in list(index.items()):
            for government, minors in list(governments.items()):
                for minor, yearly in list(minors.items()):
                    centre = CLASS_MEDIAN.get(name) if by_class else PRICE_MEDIAN.get(name)
                    band = CLASS_BAND if by_class else PRICE_BAND
                    if centre is None and not by_class:
                        centre, band = CLASS_MEDIAN.get(minor), CLASS_BAND
                    if centre:
                        for years, values in list(yearly.items()):
                            valid = [value for value in values if centre / band <= value <= centre * band]
                            if valid:
                                yearly[years] = valid
                            else:
                                del yearly[years]
                    if not yearly:
                        del minors[minor]
                if not minors:
                    del governments[government]
            if not governments:
                del index[name]


# ------------------------------------------------------------------- writing

def write_book(path: Path, header: list[str], rows, readme_lines) -> int:
    workbook = Workbook(write_only=True)
    sheet = workbook.create_sheet("Asset Register")
    sheet.freeze_panes = "A2"
    widths = {"DESCRIPTION": 40, "LOCATION_SEGMENT2": 26, "LOCATION_SEGMENT3": 36, "ASSET_CATEGORY_MAJOR": 26, "ASSET_CATEGORY_MINOR1": 30,
              "ASSET_CATEGORY_MINOR2": 30, "ASSET_CATEGORY_MINOR3": 30, "TAG_NUMBER": 24, ATTRIBUTE[1]: 34, ATTRIBUTE[4]: 44, ATTRIBUTE[6]: 24, ATTRIBUTE[15]: 70}
    for position, name in enumerate(header, 1):
        sheet.column_dimensions[get_column_letter(position)].width = widths.get(name, 18 if name.startswith("ATTRIBUTE") else 16)
    sheet.row_dimensions[1].height = 75
    header_cells = []
    for value in header:
        cell = WriteOnlyCell(sheet, value=value)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E79")
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        header_cells.append(cell)
    sheet.append(header_cells)
    count = 0
    for values in rows:
        output = []
        for name, value in zip(header, values):
            fill = None
            if isinstance(value, tuple):
                value, fill = value
            if value is None:
                output.append(None)
            elif fill is not None or (name in MONEY and isinstance(value, (int, float))) or isinstance(value, (date, datetime)):
                output.append(styled_cell(sheet, name, value, fill))
            else:
                output.append(value)
        sheet.append(output)
        count += 1
        if count % 50000 == 0:
            print(f"{path.name} {count:,}", flush=True)
    sheet.auto_filter.ref = f"A1:{get_column_letter(len(header))}{count + 1}"
    notes = workbook.create_sheet("Read Me")
    notes.column_dimensions["A"].width = 140
    for number, line in enumerate(readme_lines(count), 1):
        cell = WriteOnlyCell(notes, value=line)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        if number == 1:
            cell.font = Font(bold=True, size=14, color="1F4E79")
        # Set dimensions before appending because write-only rows stream directly.
        wrapped_lines = max(1, len(textwrap.wrap(str(line), width=130)))
        notes.row_dimensions[number].height = max(24, 15 * wrapped_lines + 8)
        notes.append([cell])
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)
    print(f"wrote {count:,} rows to {path}", flush=True)
    return count


def source_rows(limit: int | None = None):
    workbook = load_workbook(SK, read_only=True, data_only=True)
    sheet = workbook["Asset Register"]
    rows = sheet.iter_rows(values_only=True)
    header = [clean(value) for value in next(rows)]
    index = {name: position for position, name in enumerate(header)}
    for number, row in enumerate(rows):
        if limit is not None and number >= limit:
            break
        if not any(value not in (None, "") for value in row):
            continue
        record = {name: row[position] if position < len(row) else None for name, position in index.items()}
        record["_row"] = number + 2  # the row's number in the SK workbook
        yield record
    workbook.close()


BLANK_REASONS = {
    "ASSET_EXP_ACCT_FUND_SOURCE": "The guidelines do not state this account segment for these assets.",
    "ASSET_EXP_ACCT_PROGRAMME": "The guidelines do not state this account segment for these assets.",
    "ASSET_EXP_ACCT_COST_CENTER": "The guidelines do not state this account segment for these assets.",
    "ASSET_EXP_ACCT_PROJECT": "The guidelines do not state this account segment for these assets.",
    "ASSET_EXP_ACCT_BUDGET_OUTPUTS": "The guidelines do not state this account segment for these assets.",
    "ASSET_EXP_ACCT_SPARE": "The guidelines do not state this account segment for these assets.",
    "ASSET_EXP_ACCT_GEO_LOCATION": "The guidelines do not state this account segment for these assets.",
    "ASSET_CLR_ACCT_FUND": "The guidelines do not state a clearing account for these assets.",
    "ASSET_CLR_ACCT_FUND_SOURCE": "The guidelines do not state a clearing account for these assets.",
    "ASSET_CLR_ACCT_PROGRAMME": "The guidelines do not state a clearing account for these assets.",
    "ASSET_CLR_ACCT_COST_CENTER": "The guidelines do not state a clearing account for these assets.",
    "ASSET_CLR_ACCT_PROJECT": "The guidelines do not state a clearing account for these assets.",
    "ASSET_CLR_ACCT_BUDGET_OUTPUTS": "The guidelines do not state a clearing account for these assets.",
    "ASSET_CLR_ACCT_SPARE": "The guidelines do not state a clearing account for these assets.",
    "ASSET_CLR_ACCT_GEO_LOCATION": "The guidelines do not state a clearing account for these assets.",
    "ASSET_CLR_ACCT_ACCOUNT": "No row is capitalized, so no clearing account applies.",
    "PRORATE_CONVENTION_CODE": "No row depreciates, so no prorate convention applies.",
    "ASSET_KEY_SEGMENT1": "Neither the guidelines nor the source state an asset key.",
    "EMPLOYEE_NUMBER": "The source names no employee numbers.",
    "AMORTIZATION_START_DATE": "No intangible asset in the source states an amortization start date.",
    "AMORTIZE_NBV_FLAG": "The guidelines do not state an amortize-NBV treatment for these assets.",
}


def readme(stats: Counter, borrowed: bool, filled: Counter, headers: list[str]):
    def lines(count: int) -> list[str]:
        text = [
            "UgIFT asset register" + (" (REF: borrowed prices, lives and dates, and calculated depreciation)" if borrowed else " (MF)"),
            "Built from ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx, one MF row per SK row. The SK workbook was not changed. Columns A-BL are the 64 headers of "
            "Sample Header of Asset Register..xlsx; ATTRIBUTE1 to ATTRIBUTE15 carry the 15 columns of the SK template in the template's order and are headed ATTRIBUTEn(<SK column>), "
            "from ATTRIBUTE1(Equipment/ Item) to ATTRIBUTE15(Remarks).",
            "Guideline sections used: GOU Asset Accounting Policies and Guidelines 2023 (April 2023) sections 3.1.3 and Annex 1 (classes and useful lives), "
            "3.2.1 (recognition conditions), 3.2.2 (initial cost; no capitalization threshold; illustration of ICT and other equipment over 5 years), "
            "3.2.3 (repairs and spare parts), 3.3.3 (small office equipment and loose tools expensed on 221012), 3.3.5 (group assets with subsidiary records; "
            "depreciation from the first day of the month the asset is available for use), 3.3.6 (donated assets), 5.5 (straight-line method; work in progress and "
            "operating leases not depreciated), 5.7 (nil residual value), 5.14 (land and assets under construction not depreciated), Annex 2 (chart of accounts asset classification).",
            "One row is one physical asset (section 3.3.5 subsidiary record). FIXED_ASSETS_UNITS is 1. A counted source line is marked [item 1 of 100] in DESCRIPTION.",
            "ASSET_TYPE is CAPITALIZED only when section 3.2.1 holds: the vote controls the asset (an asset held for the facility at its district store is controlled by the vote), "
            "it has service potential beyond one year, it exists (a line marked not received, not delivered, missing, lost, stolen, disposed of, written off or condemned does not, nor one the "
            "verification team could not see, find or verify; a remark about another item or about part of a group does not deny the row), and its cost is measured on the source"
            + (" or borrowed on this workbook." if borrowed else ". Rows without a cost stay blank; the REF workbook fills them after borrowing.")
            + f" A building the source says is still under construction is work in progress: ASSET_TYPE CIP at the cost the source states ({stats['cip']:,} rows), not depreciated (5.5, 5.14), "
            "with no placed-in-service date or price borrowed for it. A service or subscription (internet connectivity for a period, engraving, testing and commissioning, installation as a line of its own) "
            "is not a controlled resource with service potential beyond a year (3.2.1.2): it carries no class, no cost borrowing and no ASSET_TYPE.",
            "The guidelines set no capitalization threshold (3.2.2.1): every non-current asset is capitalized whatever its value, and similar low-value units acquired in one transaction (desks, laboratory stools, surgical instruments, computers in a laboratory) are a group asset (3.3.5) whose subsidiary records are the unit rows of this register, each marked CAPITALIZED. "
            "Small office equipment and loose tools (3.3.3: kettles, spoons, forks, calculators, staplers, pen-holders, punches, paper trays, pin and staple holders, typewriters, and items of the same nature: clocks and stop watches, scissors, spatulas, rulers, measuring and MUAC tapes, buckets, bins, mops, hand tools, "
            "keyboards, mice, cables, chargers, surge protectors, penguin suckers) are not capitalized whatever their value; their expense account is 221012 and they carry no class, life or depreciation (a life the source typed stays in ATTRIBUTE5 on the MF workbook). "
            "Single-use packs, graph paper, laboratory glassware and other consumables are not capitalized. Natural resources are not capitalized (3.2.1.4). A unit price far below the price of the same item elsewhere (a line total divided, or a slip) is not a low-value asset: the REF workbook borrows the unit price for it.",
            "ASSET_CATEGORY_MAJOR, MINOR1 and MINOR2 are the Annex 1 classes read from the asset name. ASSET_CATEGORY_MINOR3 is the item name, the item-master level below Annex 1 "
            "(Annex 1 footnote 5), written as the sample row writes it (Laptop for HP Laptop silver). Generic names (equipment, item, set, machine), totals, counts and consumable packs "
            "carry no class; no class is taken from the facility type. A row with a generic name is not capitalized either: its service potential beyond one year cannot be read from the source.",
            "DESCRIPTION is the equipment name in one spelling: the toolkit's spelling for its standard items, and title case for names the source typed in capitals; a counted line carries [item 1 of 100].",
            "LIFE_IN_MONTHS is the source life where stated ('7 yrs' read as 84 months), otherwise the Annex 1 life of the class (ICT and other equipment 60 months; land 600 months although it does not depreciate), "
            f"and for an asset whose name Annex 1 does not class the guidelines' general equipment life of 60 months ({stats['life_default']:,} rows). A line that is no non-current asset (a total, a repair, a service, a consumable, a loose tool) carries 0. "
            f"A stated life under 12 months ({stats['life_short']:,} rows, mostly '3' or '2') is unclear wording, since a non-current asset serves beyond one year (3.2.1.2): the class life applies and the stated figure stays in ATTRIBUTE5(Life in Months) on the MF workbook. "
            "DEPRECIATE_FLAG is YES with DEPRN_METHOD_CODE STL where a life applies (section 5.5) and NO on every other row: land (5.14), work in progress and operating leases (5.5), and lines that are no asset. "
            "SALVAGE_VALUE is 0 on every row (5.7, nil residual value); the source recorded no residual values. PRORATE_CONVENTION_CODE is GOU PRO CO on every row, the book's one convention (3.3.5.2 and the sample row).",
            "ASSET_EXP_ACCT_FUND is 01, the Consolidated Fund, the fund segment the sample row carries, on every row. "
            "ASSET_EXP_ACCT_ACCOUNT is 221012 for small office equipment and loose tools (3.3.3), and for a capitalized asset the Annex 2 depreciation expense account of its class (2312xx, e.g. 231221 Light ICT hardware, 231235 Furniture and Fittings, 231233 Medical and Laboratory appliances), the account the sample row uses. "
            "ASSET_CLR_ACCT_ACCOUNT is 513001 (net assets/accumulated funds), the account the guidelines credit when an asset is brought into the register (3.2.2 illustration) and the sample row's clearing account, on every CAPITALIZED or CIP row; "
            "a capitalized row whose name Annex 1 does not class carries the clearing account only, since its expense account follows the class. No other account segment is stated by the guidelines.",
            f"ASSET_NUMBER and ATTRIBUTE3(Asset Number) carry the number the source states; where the source stated none, the register's own reference UGIFT-<SK row number> ({stats['asset_number_reference']:,} rows), so every row can be cited; it is not an IFMS asset number.",
            "BOOK_TYPE_CODE is the local government in upper case without District, Local Government or DLG wording, hyphens as spaces, MC or CITY kept, and BK appended (HOIMA BK, MADI OKOLLO BK, KIIRA MC BK). "
            "LOCATION_SEGMENT1 is the same government in vote form as Location(3)2.xlsx spells it, so the row loads in IFMS (MADI\\-OKOLLO DLG, BUSIA MC, HOIMA CC; the master's BULISA DLG, LUWERO DLG, KASANDA DLG, NTUNGUMO DLG, NAKAPIRIPIRI DLG and KIRA MC are kept where they differ from the gazetted spelling in BOOK_TYPE_CODE). "
            "LOCATION_SEGMENT2 is the department in upper case in one spelling (counts and facility or category words typed in the department cell are not departments); where the source left the department empty it is the department of the vote "
            f"that a facility of that kind belongs to (HEALTH for a health centre, EDUCATION for a seed school, HOSPITAL SERVICES for a hospital, UNSPECIFIED for a ministry; {stats['department_kind']:,} rows), and ATTRIBUTE2(Department) carries that same department. "
            "LOCATION_SEGMENT3 is the facility, ending in Seed Secondary School or Health Centre III; a hospital, blood bank, ministry site or local government office keeps its own name. LOCATION_SEGMENT4 is UNSPECIFIED, the fourth segment of every location combination in Location(3)2.xlsx and of the sample row.",
            "Central government: ministries, agencies and referral hospitals keep their UgIFT assets on their own votes and stay on the register. Their BOOK_TYPE_CODE is the vote code Location(3)2.xlsx spells plus BK (MOFPED BK, MOH BK, MOES BK, MOLG BK, MOLHUD BK, MGLSD BK, MAAIF BK, MOWE BK, MOWT BK, NEMA BK, PPDA BK, OAG BK, OPM BK, KCCA BK, UBTS BK for the regional blood banks, ARUA RRH BK and the other referral hospitals), "
            "LOCATION_SEGMENT1 that same code, LOCATION_SEGMENT2 the department the source states (else UNSPECIFIED, or HOSPITAL SERVICES for a hospital) and LOCATION_SEGMENT3 the site the source names (Finance Building, Embassy House, a district inspectorate, a blood bank) or UNSPECIFIED. "
            "Their rows come from the ministries' verification returns, the programme's fixed-asset registers, the two blood-bank inventories and the hospital rows of the consolidated MDA status register, as the SK Read Me records.",
            "Equipment status is written as Functional or Faulty on every row, in ATTRIBUTE14(Equipment status); IN_USE_FLAG is YES for Functional and NO for Faulty. "
            "Functional covers in use (also 'in use but in poor condition'), functional, functioning, working, available, verified, good condition and new; Faulty covers damaged, broken, not functioning, not in use, in store (not in use), not received, not seen, obsolete, unserviceable, disposed, lost and missing. "
            f"Where the status cell was empty the Remarks decided ({stats['status_from_remark']:,} rows); where the wording split the group the larger stated count decided; an asset the team recorded with no condition anywhere is taken as Functional ({stats['status_default']:,} rows). "
            "Words run together or dashed in the source (goodandfunctional, non - functional) were read as the words they spell. Longer status wording is in ATTRIBUTE15(Remarks) as 'Source status'. "
            "A blank tag, or a placeholder for one (Not engraved, Nor engraved, Not, N/A and any wording within two letters of 'not engraved'), is written Not engraved; a real engraved number is kept as written; any other wording in the tag cell is in Remarks as 'Engraving'.",
            "SERIAL_NUMBER, MANUFACTURER_NAME and MODEL_NUMBER are filled only where the description states them explicitly (serial, s/n, model, made by).",
            "ATTRIBUTE1(Equipment/ Item) to ATTRIBUTE15(Remarks) are the SK columns in order, headed with the field template's spelling of each column (Equipment/ Item as the health-centre template writes it): Equipment/ Item, Department, Asset Number, Item Description, Life in Months, Tag Number (engrave no.), "
            "Date Of Purchase, Date Placed In Service, Recoverable cost, Cost, Acc Dep Cost, Net Book Value, Ytd Deprn, Equipment status, Remarks. "
            + ("On this REF workbook ATTRIBUTE5(Life in Months), ATTRIBUTE8(Date Placed In Service), ATTRIBUTE10(Cost), ATTRIBUTE11(Acc Dep Cost), ATTRIBUTE12(Net Book Value) and ATTRIBUTE13(Ytd Deprn) "
               "show the finished value, the same as LIFE_IN_MONTHS, DATE_PLACED_IN_SERVICE, FIXED_ASSETS_COST, DEPRN_RESERVE and YTD_DEPRN, with the same cell colour (white where the source stated it); "
               "ATTRIBUTE12 is the source net book value where stated, otherwise cost less DEPRN_RESERVE, not below SALVAGE_VALUE. ATTRIBUTE8 holds a date only and remains empty for work in progress."
               if borrowed else
               "On this MF workbook every ATTRIBUTE column carries the source value as sanitized; nothing is borrowed or calculated here."),
            "ATTRIBUTE15(Remarks) holds only what the field recorded: the source Remarks, the status wording moved out of Equipment status ('Source status'), words typed into an amount column under that column's name, wording in the tag cell ('Engraving'), "
            "and the SK fields with no column in A-BL, each labelled with its source column name (Facility type, Source file, Source location; the file path keeps its spelling on disk). Nothing in it is written by the register itself. "
            "ATTRIBUTE4(Item Description) is the field description trimmed to one spacing with a capital first letter; a cell that held only a count, a unit word or a placeholder is left empty. "
            "ATTRIBUTE9(Recoverable cost) is the amount the source states" + ("; where the source states none it is the carrying amount (cost less DEPRN_RESERVE), since no impairment was recorded (recoverable amount as the impairment test, not salvage value)." if borrowed else ".")
            + " Dates are written yyyy-mm-dd; ATTRIBUTE7(Date Of Purchase) keeps a year or financial year the source wrote and is empty where the wording could not be read as a date"
            + ("; ATTRIBUTE8 is the finished placed-in-service date." if borrowed else "; ATTRIBUTE8 is the placed-in-service date the source states, empty where it wrote words."),
            "Every filled cell was sanitized: trimmed, single spaces, no line breaks, placeholders (N/A, nil, none, -) cleared, one spelling per fact. Amounts are shown with thousands separators and a nil amount as '-' (format #,##0.##;-#,##0.##;\"-\"); they were not recalculated while cleaning.",
            "Columns left blank and why:",
        ]
        for header in headers:
            if filled.get(header, 0) == 0:
                text.append(f"  {header}: {BLANK_REASONS.get(header, 'The guidelines and the source do not state it for any row.')}")
        text.append(f"Rows: {count:,}. Classified rows: {stats['class']:,}. Capitalized rows: {stats['capitalized']:,}. Work-in-progress (CIP) rows: {stats['cip']:,}.")
        if borrowed:
            text.extend([
                "DATE_PLACED_IN_SERVICE was finished first, an empty date treated like an empty cost: the placed-in-service date the source states (white); else the purchase date on the same row "
                f"({stats['date_purchase']:,} rows, white); else the first month of the year, or 1 July of the financial year, the row states ({stats['date_year']:,} rows, white); "
                "else the most common placed-in-service month of assets with the same name, borrowed in the same order and colours as a cost (blue same government, orange other governments, green whole workbook). "
                f"Where no asset of the same name carries a date, the month the other assets of the same facility were placed in service is taken (blue, {stats['date_place_1']:,} rows including the same government), else the whole workbook's most common month (green, {stats['date_place_3']:,} rows). "
                "Work in progress keeps no placed-in-service date. The cell colour is the only marker of a borrowed date; Remarks never describe it.",
                "Borrowed purchase costs: a white cost cell is a price stated on the source. Blue (#9DC3E6): median price of assets with the same name in the same local government, same purchase year or the closest year. "
                "Orange (#F4B183): other local governments, same year or the nearest period. Green (#C6EFCE): the whole workbook, used only when steps 1 and 2 found no price. Where both rows have an asset class, the class matches. "
                "Names are matched in the singular (Desks borrow from Desk). A stated price more than twenty times above or below the median stated price of that name across the workbook (a line total typed on one unit, or a slip) is left out of the donors where three or more prices exist, "
                f"and a recorded cost outside that band is treated the same way on this workbook: the unit price is borrowed and coloured, and the recorded figure stays in ATTRIBUTE10(Cost) on the MF workbook ({stats['cost_outlier']:,} rows). "
                f"Where no asset of the same name carries a price, the Annex 1 class supplies it (same government blue {stats['cost_class_1']:,}; other governments orange {stats['cost_class_2']:,}). "
                f"A line that is no asset, and works with no cost stated, carry 0 ({stats['cost_nil']:,} rows); {stats['cost_unpriced']:,} assets with neither a priced namesake nor a priced class remain without a cost. "
                f"A unit cost under UGX 10,000, stated or borrowed, is immaterial and is carried at 0 ({stats['cost_small']:,} rows), which the amount format shows as '-'; such a row is not capitalized and carries no depreciation. "
                "Where a name has fewer than three stated prices, a recorded cost fifty times above or below the median of its Annex 1 class is treated as wrongly priced in the same way. "
                "Generic names (equipment, furniture, medical equipment, item, set, machine, buildings, land) borrow nothing. The cell colour is the only marker; Remarks never say a cost or life was borrowed.",
                "Borrowed useful lives follow the same order and colours: the most common life of assets with the same name, only where life is at least 12 months and the asset is not marked out of use. A life already on the row stays white.",
                "Straight-line depreciation is calculated to 30 September 2026 on every row that exists and has a cost, nil residual (5.7), a life in months and a placed-in-service month, whether in use or not (an idle asset still consumes its life): "
                "monthly charge = (cost - residual) / life; DEPRN_RESERVE runs from the placed-in-service month through September 2026 and stops at the end of the useful life; YTD_DEPRN is the July-September 2026 portion and cannot exceed the depreciation still to be charged. "
                "A depreciation figure the source recorded stays as written and only the blank figure beside it is calculated. Net book value (cost less DEPRN_RESERVE, not below SALVAGE_VALUE) is written in ATTRIBUTE12(Net Book Value); the sample header has no NBV column. "
                f"On {stats['reserve_over_cost']:,} rows the accumulated depreciation the source recorded exceeds the cost on the row (mostly a borrowed price beside a source figure): both are kept as recorded and the net book value is shown at the residual value. "
                f"DEPRN_RESERVE and YTD_DEPRN are 0 where there is nothing to charge: no depreciation, no cost, or an asset that does not exist ({stats['reserve_nil']:,} rows).",
                "After borrowing, ASSET_TYPE is CAPITALIZED where the section 3.2.1 tests are met and the row is not small office equipment, a loose tool or a consumable.",
                f"Borrowed costs: same government {stats['cost_1']:,}; other governments {stats['cost_2']:,}; whole workbook {stats['cost_3']:,}. "
                f"Borrowed lives: same government {stats['life_1']:,}; other governments {stats['life_2']:,}; whole workbook {stats['life_3']:,}. "
                f"Borrowed placed-in-service months: same government {stats['date_1']:,}; other governments {stats['date_2']:,}; whole workbook {stats['date_3']:,}. "
                f"Depreciation reserve calculated on {stats['reserve']:,} rows; year-to-date on {stats['ytd']:,} rows.",
            ])
        else:
            text.append("This workbook does not borrow missing prices, lives or dates and calculates no depreciation. Those, with colours, are in REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx.")
        return text

    return lines


def emit(borrow: bool, registers: Registers, costs: dict, lives: dict, dates: dict, stats: Counter, filled: Counter, limit: int | None):
    for source in source_rows(limit):
        values = build_values(source, registers, borrow=borrow, costs=costs, lives=lives, dates=dates, stats=stats)
        for header, value in zip(registers.headers, values):
            if value is not None and not (isinstance(value, tuple) and value[0] is None):
                filled[header] += 1
        yield values


def main() -> None:
    global SK, MF, REF
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=None, help="only the first N SK rows (for a sample run)")
    parser.add_argument("--only", choices=["mf", "ref"], default=None)
    parser.add_argument("--sk", type=Path, default=None, help="read this SK workbook instead of the one in outputs")
    parser.add_argument("--out", type=Path, default=None, help="write the MF and REF workbooks into this folder")
    args = parser.parse_args()
    if args.sk is not None:
        SK = args.sk
    if args.out is not None:
        MF = args.out / MF.name
        REF = args.out / REF.name
    registers = Registers(read_headers())
    print("indexing source prices, lives and dates", flush=True)
    costs, lives, dates = index_sources(source_rows(), registers)
    print("indexing class prices and placed-in-service months", flush=True)
    index_fallbacks(source_rows(), registers)
    finalize_cost_donors(costs)
    if args.only != "ref":
        print("writing MF", flush=True)
        stats: Counter = Counter()
        filled: Counter = Counter()
        write_book(MF, registers.headers, emit(False, registers, costs, lives, dates, stats, filled, args.limit), readme(stats, False, filled, registers.headers))
    if args.only != "mf":
        print("writing REF", flush=True)
        stats = Counter()
        filled = Counter()
        write_book(REF, registers.headers, emit(True, registers, costs, lives, dates, stats, filled, args.limit), readme(stats, True, filled, registers.headers))


if __name__ == "__main__":
    main()
