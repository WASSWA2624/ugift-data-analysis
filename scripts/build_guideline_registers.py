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
    common_life,
    groups_for,
    median,
    norm_name,
    parse_date,
    row_years,
    shillings,
    usable_name,
)
from fill_clear_template_fields import classify, explicit_token
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
ATTRIBUTE_GUIDE = ROOT / "Updated Attributes for Asset Categories.xlsx"

AS_OF = date(2026, 9, 30)
FY_START = date(2026, 7, 1)
UNIT = re.compile(r"\s*\[item \d+ of \d+\]\s*$", re.I)
# Section 3.3.3: small office equipment and loose tools are expensed on 221012.
LOOSE = re.compile(
    r"\b(kettles?|spoons?|(?<!tuning )forks?(?!\s?lift)|calculators?|staplers?|stapling machines?|pen-?holders?|"
    r"punches|punch|paper trays?|pin-?holders?|staple holders?|type\s?writers?)\b",
    re.I,
)
CONSUMABLE = re.compile(
    r"\b(pack of|packs?\b|pkts?|single[- ]use|surgic\w* packs?|graph paper|filter paper|cover slips?|slides?,? pack|"
    r"gloves|syringes?(?!\s*pumps?)|cotton wool|bandages?|reagents?|test strips?|toner|cartridges?|stationery|"
    r"chalk(?!\s*boards?)|exercise books?|text ?books?|papers?(?!\s*(?:shredders?|cutters?|trimmers?))|"
    r"tubings?|visking|labels?|droppers?|petri dish(?:es)?|bulbs?|fl[ou]{1,2}rescent tubes?|test tubes?|corks?|bungs?|"
    r"crocodile clips?|litmus|indicator paper|reels?|rolls?|boxes|\bboxe?s? of\b|wires?(?!\s*gauze)|boiling tube brushes)\b",
    re.I,
)
NATURAL = re.compile(r"\b(natural resources?|mineral rights?|wildlife|forests?|wetlands?|rivers?|lakes?)\b", re.I)
NON_DEPR = re.compile(
    r"\b(work in progress|\bwip\b|under construction|operating lease|incomplete building|"
    r"(?:on-?\s?going|ongoing)\s+constructions?|still\s+under\s+construction|not\s+(?:yet\s+)?complet\w+)\b",
    re.I,
)
# Section 3.2.1 condition 3: the asset must exist. A row whose status says it was
# never received, or whose remark says the asset itself is missing, lost or stolen.
NOT_EXISTING = re.compile(
    r"\bnot\s+(?:yet\s+)?(?:received|delivered|supplied)\b|\bnever\s+(?:received|delivered)\b|"
    r"\bdidn'?t\s+receive\b|\bnot\s+among\b|\bwas\s+not\s+(?:delivered|supplied)\b|"
    r"^\s*(?:missing|lost|stolen|disposed|taken away|not there)\b|\b(?:is|are|was|were|got|went|been)\s+(?:missing|lost|stolen|disposed|taken away)\b",
    re.I,
)
TOTAL_LINE = re.compile(r"(?i)^\s*(?:sub|grand)?\s*totals?\b|\btotal\s+(?:equipment|asset|units?|quantit)")
REPAIR = re.compile(
    r"(?i)^\s*(?:repairs?|servicing|maintenance|overhaul)\s+(?:of|to|for)\b|\bspare\s+(?:parts?|tyres?|bottles?)\b|"
    r"\breplacement\s+(?:parts?|engine|battery|tyres?)\b"
)
GENERIC_HEAD = re.compile(
    r"(?i)^(?:\w+[\s\-]+){0,2}(?:equipments?|items?|sets?|machines?|furnitures?|assorted.*|schools?|hospitals?|assets?|tools?|materials?|fittings?)$"
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
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:[a-z]+\s+){0,2}(?:are\s+|were\s+|is\s+|was\s+)?"
    r"(?:not\b|non[\s\-]|broken|damaged|faulty|spoilt?|missing|stolen|dead|lost|obsolete|unserviceable|out\s+of|in\s+(?:the\s+)?stores?\b)"
)
PLACEHOLDER_TEXT = re.compile(r"(?i)^(n/?a|na|nil+|none|null|-+|–|—|not applicable|not indicated|\.+|…+|_+)$")
MONEY = {"FIXED_ASSETS_COST", "DEPRN_RESERVE", "YTD_DEPRN", "SALVAGE_VALUE"}
BLUE = PatternFill("solid", fgColor="9DC3E6")
ORANGE = PatternFill("solid", fgColor="F4B183")
GREEN = PatternFill("solid", fgColor="C6EFCE")
FILLS = {1: BLUE, 2: ORANGE, 3: GREEN}
BRANDS = (
    "HP", "Hewlett Packard", "Dell", "Lenovo", "Acer", "Asus", "Toshiba", "Apple", "Samsung", "LG", "Sony", "Epson",
    "Canon", "Kyocera", "Brother", "Xerox", "Ricoh", "Sharp", "Panasonic", "Philips", "Hisense", "Cisco", "D-Link",
    "TP-Link", "Huawei", "Tecno", "Nokia", "Itel", "APC", "Mercury", "Luminous", "Kenwood", "Hikvision", "Dahua",
    "Olympus", "Nikon", "Zeiss", "Omron", "Sinocare", "Mindray", "Toyota", "Nissan", "Isuzu", "Mitsubishi", "Honda",
    "Yamaha", "TVS", "Bajaj", "Ford", "Suzuki", "Hyundai", "Kia", "Mazda", "Perkins", "Cummins", "Fiat", "Volvo",
    "Steelmate", "Binatone", "Ramtons", "Von", "Solarmax", "Felicity", "Victron", "Growatt", "Microsoft", "Intel",
)
MATERIALS = (
    (re.compile(r"(?i)\b(wooden|wood|timber|mahogany|mvule)\b"), "Wooden"),
    (re.compile(r"(?i)\b(metallic|metal|steel|iron|aluminium|aluminum|stainless)\b"), "Metallic"),
    (re.compile(r"(?i)\bplastic\b"), "Plastic"),
    (re.compile(r"(?i)\bleather\b"), "Leather"),
)
BUILDING_USE = (
    (re.compile(r"(?i)class\s*room|classroom|lecture|school block|dormitor|hostel|staff\s*room|teachers?"), "School"),
    (re.compile(r"(?i)laborator|science lab|\blab\b"), "Laboratory"),
    (re.compile(r"(?i)librar"), "Library"),
    (re.compile(r"(?i)kitchen"), "Kitchen"),
    (re.compile(r"(?i)\bstore|storage|warehouse"), "Store"),
    (re.compile(r"(?i)\bward|maternity|\bopd\b|out.?patient|theatre|theater|clinic|dispensar|health|mch|placenta|sick\s*bay|labour|labor"), "Hospital"),
    (re.compile(r"(?i)office|admin|reception|board\s*room"), "Office"),
    (re.compile(r"(?i)dining|canteen|mess\b"), "Canteen"),
    (re.compile(r"(?i)mortuar"), "Mortuary"),
    (re.compile(r"(?i)garage|workshop"), "Garage"),
)
FURNITURE_USER = (
    (re.compile(r"(?i)laborator|science lab|\blab\b"), "Laboratory"),
    (re.compile(r"(?i)\bstores?\b|storage"), "Storage"),
    (re.compile(r"(?i)\bward|maternity|\bopd\b|\bmch\b|\bipd\b|theatre|health|clinic|dispensar|patient|labour|antenatal|postnatal"), "Hospital"),
    (re.compile(r"(?i)board\s*room"), "Boardroom"),
    (re.compile(r"(?i)conference|meeting|hall"), "Conference room"),
    (re.compile(r"(?i)reception"), "Reception"),
    (re.compile(r"(?i)librar|study|class\s*room|classroom|students?|learners?|pupils?|academ|education|edn"), "Study"),
    (re.compile(r"(?i)office|admin|head\s*teacher|bursar|secretary|registr|record"), "Office"),
    (re.compile(r"(?i)staff\s*house|residen|quarters|dormitor|hostel"), "Residential"),
)


# ------------------------------------------------------------------ references

def read_headers() -> list[str]:
    workbook = load_workbook(SAMPLE, read_only=True, data_only=True)
    row = [clean(value) for value in next(workbook.active.iter_rows(max_row=1, values_only=True))]
    workbook.close()
    return row


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


def attribute_guide() -> dict[str, dict[int, str]]:
    """{normalised minor 2 class: {attribute position: meaning}} from the attribute workbook."""
    guide: dict[str, dict[int, str]] = {}
    if not ATTRIBUTE_GUIDE.exists():
        return guide
    workbook = load_workbook(ATTRIBUTE_GUIDE, read_only=True, data_only=True)
    sheet = workbook["Attributes"]
    minor2 = ""
    for row in sheet.iter_rows(min_row=3, values_only=True):
        row = list(row) + [None] * 20
        if row[3]:
            minor2 = clean(row[3])
        meanings = {position: clean(value) for position, value in enumerate(row[5:18], 1) if value}
        if meanings and minor2:
            key = norm_name(minor2.replace("&", "and").replace("-", " "))
            key = key.replace("non residential buildings", "non residential buildings")
            guide.setdefault(key, meanings)
    workbook.close()
    aliases = {
        "med lab research appliances": ["med lab research appliances"],
        "non residential buildings": ["non residential buildings"],
        "oil pipelines reservoirs": ["oil pipelines and reservoirs"],
    }
    for target, sources in aliases.items():
        for source in sources:
            if source in guide and target not in guide:
                guide[target] = guide[source]
    return guide


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


def condition(status: str) -> tuple[str, str]:
    """('Functional' | 'Faulty' | '', longer wording for Remarks)."""
    text = plain(status)
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
    elif negative:
        label = "Faulty"
    elif positive:
        label = "Functional"
    else:
        label = ""
    longer = "" if label and re.fullmatch(r"(?i)functional|faulty|functioning|good|in use|working|ok(?:ay)?|good condition", text) else text
    return label, longer


def attribute_condition(label: str, status: str, allowed: str) -> str:
    """The attribute guide's condition value for this class."""
    text = plain(status)
    options = allowed.casefold()
    if "excellent" in text.casefold() and "excellent" in options:
        return "Excellent"
    if re.search(r"(?i)obsolete|condemned", text) and "obsolete" in options:
        return "Obsolete"
    if re.search(r"(?i)grounded", text) and "grounded" in options:
        return "Grounded"
    if label == "Functional":
        if "running" in options:
            return "Running"
        if "good and in use" in options:
            return "Good and In Use"
    if label == "Faulty" and re.search(r"(?i)damag|broken|fault|repair|spoil|not\s+(?:function|working)|non[- ]?function|dead|cracked|worn", text):
        if "needs repair" in options:
            return "Needs Repair"
    return ""


def first_brand(text: str) -> str:
    for brand in BRANDS:
        if re.search(rf"(?i)(?<![A-Za-z]){re.escape(brand)}(?![A-Za-z])", text):
            return brand
    return ""


def material(text: str) -> str:
    found = []
    for pattern, name in MATERIALS:
        match = pattern.search(text)
        if match:
            found.append((match.start(), name))
    return min(found)[1] if found else ""


def lookup(table, text: str) -> str:
    for pattern, name in table:
        if pattern.search(text):
            return name
    return ""


def registration_number(text: str) -> str:
    match = re.search(r"\b(U[A-Z]{1,2}\s?\d{3,4}\s?[A-Z]{1,2})\b", text)
    return match.group(1) if match else ""


def engine_type(text: str) -> str:
    match = re.search(r"(?i)\b(diesel|petrol|electric|hybrid)\b", text)
    return match.group(1).capitalize() if match else ""


def year_of_manufacture(text: str) -> str:
    match = re.search(r"(?i)\b(?:yom|year of manufacture|manufactured)\s*[:\-]?\s*((?:19|20)\d{2})\b", text)
    return match.group(1) if match else ""


def rooms(text: str) -> str:
    match = re.search(r"(?i)\b(\d{1,3})\s*(?:rooms?|stances?|class\s*rooms?|classrooms?|units?|stanza)\b", text)
    return match.group(1) if match else ""


def term(text: str) -> str:
    match = re.search(r"(?i)\b(semi[- ]?permanent|permanent|temporary)\b", text)
    if not match:
        return ""
    word = match.group(1).casefold()
    return "Semi-permanent" if word.startswith("semi") else "Permanent" if word == "permanent" else ""


def land_type(text: str) -> str:
    match = re.search(r"(?i)\b(freehold|leasehold|customary|untitled|mailo)\b", text)
    return match.group(1).capitalize() if match else ""


def land_status(text: str) -> str:
    match = re.search(r"(?i)\b(encroached|developed|undeveloped|under development)\b", text)
    return match.group(1).capitalize() if match else ""


def user_name(remarks: str) -> tuple[str, str]:
    match = re.search(r"(?i)\buser\s*(?:name)?\s*:\s*([^,;|]+)", remarks)
    name = clean(match.group(1)) if match else ""
    match = re.search(r"(?i)\b(?:user\s*)?title\s*:\s*([^,;|]+)", remarks)
    title = clean(match.group(1)) if match else ""
    return name, title


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
    "asset", "assets", "others", "other", "various", "assorted", "assorted items", "fittings", "building", "buildings",
    "structure", "structures", "block", "blocks", "equipments", "tools", "materials", "furniture and fittings", "ict",
    "ict equipment", "electrical", "electricals", "machinery", "machine", "items", "item", "set", "sets", "kit", "kits",
}


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


def money_cell(sheet, value: int | float, fill=None) -> WriteOnlyCell:
    cell = WriteOnlyCell(sheet, value=int(value) if float(value).is_integer() else value)
    cell.number_format = "#,##0.##"
    if fill is not None:
        cell.fill = fill
    return cell


def money_text(value: int | float) -> str:
    """An amount written in Remarks with the same thousands separators as the cells."""
    if float(value).is_integer():
        return f"{int(value):,}"
    return f"{float(value):,.2f}".rstrip("0").rstrip(".")


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
        self.guide = attribute_guide()
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
            if found and (LOOSE.search(bare) or CONSUMABLE.search(bare)) and not extra_classify(bare):
                found = None
            if found:
                # Annex 1 decides life, method and salvage for the class it names.
                row = self.annex1.get(norm_name(found[2]))
                if row:
                    found = (row["major"], row["minor1"], row["minor2"], row["months"], row["depreciate"])
        self.class_cache[key] = found
        return found

    def attributes(self, minor2: str, facts: dict) -> dict[str, str]:
        """ATTRIBUTE columns the class guide defines and the source states."""
        values: dict[str, str] = {}
        meanings = self.guide.get(norm_name(minor2)) if minor2 else None
        if not meanings:
            return values
        for position, meaning in meanings.items():
            low = meaning.casefold()
            value = ""
            if re.search(r"\btag\b|engrave", low):
                value = facts["tag"]
            elif low.startswith("heritage"):
                value = ""
            elif "serial" in low:
                value = facts["serial"]
            elif low.startswith("type (") and "plastic" in low:
                value = material(facts["text"])
            elif low.startswith("make"):
                value = facts["make"]
            elif low.startswith("condition"):
                value = attribute_condition(facts["status_label"], facts["status"], meaning)
            elif "date of purchase" in low or "date of acquisition" in low:
                value = facts["purchase"]
            elif "placed in service" in low:
                value = facts["placed"]
            elif "user name" in low:
                value = facts["user"]
            elif "user title" in low or low == "user title":
                value = facts["title"]
            elif low.startswith("user ("):
                value = lookup(FURNITURE_USER, f"{facts['department']} {facts['text']}")
            elif "registration number" in low:
                value = registration_number(facts["text"])
            elif "engine type" in low:
                value = engine_type(facts["text"])
            elif "chassis" in low:
                value = explicit_token(facts["text"], "chassis") or ""
            elif "year of manufacture" in low:
                value = year_of_manufacture(facts["text"])
            elif low.startswith("use ("):
                value = lookup(BUILDING_USE, f"{facts['text']} {facts['department']}")
            elif "number of rooms" in low:
                value = rooms(facts["text"])
            elif low.startswith("term"):
                value = term(facts["text"])
            elif "plot" in low:
                match = re.search(r"(?i)\bplot\s*(?:no\.?|number)?\s*[:\-]?\s*([A-Za-z0-9/\-]+)", facts["text"])
                value = match.group(1) if match else ""
            elif "title deed" in low:
                match = re.search(r"(?i)\btitle\s*(?:deed)?\s*(?:no\.?|number)?\s*[:\-]?\s*([A-Za-z0-9/\-]+)", facts["text"])
                value = match.group(1) if match else ""
            elif low.startswith("type (") and "freehold" in low:
                value = land_type(facts["text"])
            elif low.startswith("purpose"):
                value = "School" if facts["kind"] == "School" else "Hospital" if facts["kind"] == "Health centre" else ""
            elif low.startswith("current status"):
                value = land_status(facts["text"])
            if value:
                values[f"ATTRIBUTE{position}"] = value
        return values


def explicit_chassis(text: str) -> str:
    match = re.search(r"(?i)\bchassis\s*(?:no\.?|number|#)?\s*[:\-]?\s*([A-Za-z0-9\-]{5,25})", text)
    return match.group(1) if match else ""


MACHINERY = "MACHINERY AND EQUIPMENT"
OTHER = "OTHER MACHINERY AND EQUIPMENT"
EXTRA_CLASSES = (
    # Spellings the source uses that the shared classifier misses; the Annex 1 row
    # then supplies life and method.
    (re.compile(r"(?i)\b(wheel\s*chairs?|stop\s*watch(?:es)?|bowl,?\s*kick|kick\s*bowls?|balances?|volumetric flasks?|flasks?|"
                r"micrometer(?: screw)? gauges?|vernier|mortars? and pestles?|retort stands?|dissecting (?:kits?|sets?)|ammeters?|"
                r"voltmeters?|galvanometers?|spatulas?|wash bottles?|glass blocks?|tripod stands?|thermometers?|microscopes?|"
                r"forceps|autoclaves?|sterili[sz]ers?|oxygen cylinders?|patient beds?|hospital beds?|delivery beds?|examination couch(?:es)?|"
                r"weighing scales?|drip stands?|patient screens?|blood pressure machines?|bp machines?|syringe pumps?|tuning forks?)\b"),
     (MACHINERY, OTHER, "MED LAB RESEARCH APPLIANCES", 60, True)),
    (re.compile(r"(?i)\b(?:convex|concave|converging|diverging|plane)\b.*\b(?:lens(?:es)?|mirrors?)\b|\b(?:lens(?:es)?|mirrors?)\b.*\b(?:convex|concave|converging|diverging)\b|\bmagnifying glass(?:es)?\b"),
     (MACHINERY, OTHER, "PRECISION OPTICAL INSTRUMENTS", 60, True)),
    (re.compile(r"(?i)\b(cpus?|cpu_light duty|central processing units?|desktop computers?|computers?|laptops?|monitors?|keyboards?|printers?|photo\s*copiers?|scanners?|projectors?|routers?|network switch(?:es)?|switch(?:es)?\b.*\b(?:port|network|lan)|ups\b|uninterrupt\w* power suppl(?:y|ies)|tablets?|smart ?phones?|tela phones?)\b"),
     (MACHINERY, "ICT EQUIPMENT", "LIGHT ICT HARDWARE", 60, True)),
    (re.compile(r"(?i)\b(servers?|server processors?)\b"), (MACHINERY, "ICT EQUIPMENT", "HEAVY ICT HARDWARE", 60, True)),
    (re.compile(r"(?i)\b(single seats?|seats?|desks?|deks|chairs?|stools?|bench(?:es)?|tables?|shel(?:f|ves?|ve)|cupboards?|cabinets?|lockers?|"
                r"mattress(?:es)?|matress(?:es)?|notice\s*boards?|chalk\s*boards?|black\s*boards?|white\s*boards?|wardrobes?|beds?(?!\s*(?:side|rock)))\b"),
     (MACHINERY, OTHER, "FURNITURE AND FITTINGS", 60, True)),
    (re.compile(r"(?i)\b(paper shredders?|shredders?|photocopiers?|fax machines?|laminators?|binding machines?|safes?|wall clocks?|clocks?)\b"),
     (MACHINERY, OTHER, "OFFICE EQUIPMENT", 60, True)),
    (re.compile(r"(?i)\b(staff quarters?|teachers?['’]?\s*quarters?|staff houses?|teachers?['’]?\s*houses?|residential|dormitor(?:y|ies)|hostels?)\b(?!.*\b(latrine|toilet|kitchen)\b)"),
     ("BUILDINGS AND STRUCTURES", "DWELLINGS", "RESIDENTIAL BUILDINGS", 600, True)),
    (re.compile(r"(?i)\bnon\s*-?\s*residential\b|\b(class\s*rooms?|classrooms?|administration blocks?|admin blocks?|office blocks?|laborator(?:y|ies) blocks?|science blocks?|"
                r"library blocks?|ict blocks?|multi-?purpose halls?|dining halls?|assembly halls?|kitchens?|latrines?|toilets?|bathrooms?|washrooms?|sick bays?|wards?|"
                r"theatre blocks?|store blocks?|opd blocks?|mch blocks?|maternity wards?|placenta pits?|incinerators?|buildings?\b(?!\s*materials))\b"),
     ("BUILDINGS AND STRUCTURES", "BUILDINGS OTHER THAN DWELLINGS", "NON RESIDENTIAL BUILDINGS", 600, True)),
    (re.compile(r"(?i)\b(?:school|office|hospital|facility|health\s*cent\w*|hc\s*iii?|institutional)?\s*land\b(?!\s*(?:rover|cruiser|line|scape|lord|mark))|^plots?(?: of land)?\b"),
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
    match = re.search(r"(?i)\bmodel\s*(?:no\.?|number|#)?\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9./\-]{1,24}(?:\s+[A-Za-z0-9./\-]*\d[A-Za-z0-9./\-]*)?)\b", text)
    if not match:
        return ""
    token = match.group(1).strip(" .,-/")
    if token.casefold() in SERIAL_STOP or not (re.search(r"\d", token) or re.fullmatch(r"[A-Z][A-Za-z0-9\-]{2,}", token)):
        return ""
    return token


def explicit_manufacturer(text: str) -> str:
    match = re.search(r"(?i)\b(?:made by|manufactured by|manufacturer)\s*[:\-]?\s*([A-Z][A-Za-z0-9&.' \-]{1,40})", text)
    if not match:
        return ""
    token = clean(match.group(1)).strip(" .,-")
    return token if token.casefold() not in SERIAL_STOP else ""


# ---------------------------------------------------------------- one MF row

def build_values(source: dict, registers: Registers, *, borrow: bool, costs: dict, lives: dict, stats: Counter) -> list:
    item = plain(source.get("Equipment/Item"))
    description = plain(source.get("Item Description"))
    unit = plain(source.get("Unit"))
    bare = display_item(canonical_item(UNIT.sub("", item or description).strip()))
    name = f"{bare} [{unit}]" if unit else bare
    remarks_source = plain(source.get("Remarks"))
    status_text = plain(source.get("Equipment status"))
    status_label, longer_status = condition(status_text)
    text_blob = f"{bare} {description} {remarks_source}"

    # Place: one spelling per fact.
    lg_text = plain(source.get("Local Government"))
    lg = resolve_lg(lg_text) or lg_from_text(lg_text) if lg_text else None
    kind = plain(source.get("Facility type"))
    kind = "School" if kind.casefold().startswith(("school", "seed")) else "Health centre" if kind.casefold().startswith("health") else facility_kind(plain(source.get("Facility")))
    facility_text = plain(source.get("Facility"))
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
    classified = None if total_line or repair else registers.classify(bare)
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
        stats["class"] += 1
    if major == "BUILDINGS AND STRUCTURES" and NON_DEPR.search(remarks_source):
        non_depr = True
    life = as_life(source.get("Life in Months"))
    if life is not None and (not isinstance(life, (int, float)) or life <= 0):
        life = None
    life_source = life is not None
    if life is None and class_life and class_depreciates:
        life = class_life
    is_land = major == "LAND"
    # Section 5.5: straight line where a life applies; a source life on a loose-tool
    # row is kept as the mapping row requires.
    depreciates = bool(life) and not is_land and not natural and not non_depr and not consumable and (not loose or life_source)
    if classified and not class_depreciates and not life_source:
        depreciates = False

    cost = as_number(source.get("Cost"))
    cost_fill = None
    life_fill = None
    # A date the source states is written one way (ISO); wording stays as written.
    purchase_value = as_date(source.get("Date Of Purchase"))
    purchase_text = purchase_value.isoformat() if purchase_value else as_date_text(source.get("Date Of Purchase"))
    placed_value = as_date(source.get("Date Placed In Service"))
    placed_text = placed_value.isoformat() if placed_value else as_date_text(source.get("Date Placed In Service"))
    years = row_years(purchase_text, placed_text)
    asset_name = norm_name(bare)
    minor_key = norm_name(minor2)
    lg_key = lg.key if lg else ""
    specific = usable_name(asset_name) and asset_name not in GENERIC_NAMES and not GENERIC_HEAD.match(bare) and not total_line and not repair
    if borrow and specific and not consumable and not loose and not natural:
        if cost is None:
            found = choose(costs, asset_name, lg_key, years, minor_key)
            if found:
                method, groups = found
                values = [value for _, _, bucket in groups for value in bucket]
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

    # Section 3.2.1: controlled, service potential beyond a year, exists, measurable.
    # The status column decides existence; a remark counts only when the status is
    # blank or negative itself (a remark about part of a group is not the row's fate).
    if status_label == "Functional":
        exists = not NOT_EXISTING.search(status_text)
    elif status_text:
        exists = not NOT_EXISTING.search(status_text) and not (status_label == "Faulty" and NOT_EXISTING.search(remarks_source))
    else:
        exists = not NOT_EXISTING.search(remarks_source)
    service_potential = bool(classified) or specific or (life_source and life and life >= 12)
    capitalized = bool(cost) and exists and not loose and not consumable and not natural and not total_line and not repair and service_potential
    if is_land:
        capitalized = bool(cost) and exists
        depreciates = False
    if capitalized:
        stats["capitalized"] += 1

    reserve = as_number(source.get("Acc Dep Cost"))
    ytd = as_number(source.get("Ytd Deprn"))
    salvage = 0 if depreciates and life else None
    computed_nbv = None
    placed = placed_value if isinstance(placed_value, date) else None
    if borrow and status_label == "Functional" and cost is not None and life and placed and salvage is not None:
        figures = depreciation(float(cost), float(salvage), int(life), placed)
        if figures:
            accumulated, current = figures
            if reserve is None:
                reserve = shillings(accumulated)
                stats["reserve"] += 1
            if ytd is None:
                ytd = shillings(current)
                stats["ytd"] += 1
            computed_nbv = max(0, shillings(float(cost) - float(reserve)))
    source_nbv = as_number(source.get("Net Book Value"))

    tag_raw = plain(source.get("Tag Number (engrave no.)"))
    tag = "Not Engraved" if blank_tag(tag_raw) else tag_raw
    serial = explicit_serial(text_blob)
    manufacturer = explicit_manufacturer(text_blob)
    model = explicit_model(text_blob)
    user, title = user_name(remarks_source)
    facts = {
        "tag": tag,
        "serial": serial,
        "text": text_blob,
        "make": manufacturer or first_brand(f"{bare} {description}"),
        "status": status_text,
        "status_label": status_label,
        "purchase": purchase_text,
        "placed": placed_text,
        "user": user,
        "title": title,
        "department": plain(source.get("Department")),
        "kind": kind,
    }
    attributes = registers.attributes(minor2, facts) if classified else {}
    purchase_in_attribute = any("purchase" in registers.guide.get(norm_name(minor2), {}).get(int(key[9:]), "").casefold() for key in attributes)

    asset_number = plain(source.get("Asset Number"))
    if asset_number and unit:
        total = re.search(r"of (\d+)\]?$", unit)
        if total and re.fullmatch(r"\d+", asset_number) and int(asset_number) == int(total.group(1)):
            asset_number = ""  # that cell was the quantity

    recoverable = as_number(source.get("Recoverable cost"))
    recoverable_text = money_text(recoverable) if recoverable is not None else plain(source.get("Recoverable cost"))
    remarks = remark_bundle([
        f"Equipment status: {status_label}" if status_label else "",
        f"Source status: {longer_status}" if longer_status else "",
        "Repair or spare part (section 3.2.3): not a new asset" if repair else "",
        "Total line: not an asset" if total_line else "",
        f"Remarks: {remarks_source}" if remarks_source else "",
        f"Facility type: {kind}" if kind else "",
        f"Item Description: {description}" if description and description != bare else "",
        f"Date Of Purchase: {purchase_text}" if purchase_text and not purchase_in_attribute else "",
        f"Date Placed In Service: {placed_text}" if placed_text and placed_value is None else "",
        f"Recoverable cost: {recoverable_text}" if recoverable_text else "",
        f"Net Book Value: {money_text(source_nbv)}" if source_nbv is not None else "",
        f"Net book value (cost less accumulated depreciation): {money_text(computed_nbv)}" if computed_nbv is not None else "",
        f"Source file: {plain(source.get('Source file'))}" if plain(source.get("Source file")) else "",
        f"Source location: {plain(source.get('Source location'))}" if plain(source.get("Source location")) else "",
    ])

    # Annex 2: the depreciation expense account of the class (2312xx, as on the sample
    # row) for a capitalized asset; 221012 for small office equipment and loose tools.
    expense_account = None
    clearing_account = None
    if loose:
        expense_account = "221012"
    elif capitalized and minor2:
        acquisition = ANNEX2_BY_MINOR2.get(norm_name(minor2))
        expense_account = "231" + acquisition[3:] if acquisition else None
        clearing_account = "513001"

    values = {
        "BOOK_TYPE_CODE": book_code,
        "DESCRIPTION": name or None,
        "ASSET_CATEGORY_MAJOR": major or None,
        "ASSET_CATEGORY_MINOR1": minor1 or None,
        "ASSET_CATEGORY_MINOR2": minor2 or None,
        "ASSET_TYPE": "CAPITALIZED" if capitalized else None,
        "FIXED_ASSETS_UNITS": 1,
        "LOCATION_SEGMENT1": segment1,
        "LOCATION_SEGMENT2": department_text(source.get("Department")) or None,
        "LOCATION_SEGMENT3": facility or None,
        "FIXED_ASSETS_COST": (cost, cost_fill) if cost is not None else None,
        "ASSET_EXP_ACCT_ACCOUNT": expense_account,
        "ASSET_CLR_ACCT_ACCOUNT": clearing_account,
        "DATE_PLACED_IN_SERVICE": placed_value,
        "DEPRECIATE_FLAG": "NO" if (is_land or non_depr) and not total_line else "YES" if depreciates else None,
        "DEPRN_METHOD_CODE": "STL" if depreciates else None,
        "LIFE_IN_MONTHS": (life, life_fill) if life and (depreciates or life_source) else None,
        # Section 3.3.5.2: depreciation begins on the first day of the month the asset
        # is available for use; the sample row codes that convention GOU PRO CO.
        "PRORATE_CONVENTION_CODE": "GOU PRO CO" if depreciates else None,
        "DEPRN_RESERVE": reserve,
        "YTD_DEPRN": ytd,
        "SALVAGE_VALUE": salvage,
        "ASSET_NUMBER": asset_number or None,
        "TAG_NUMBER": tag,
        "SERIAL_NUMBER": serial or None,
        "MANUFACTURER_NAME": manufacturer or None,
        "MODEL_NUMBER": model or None,
        "IN_USE_FLAG": "YES" if status_label == "Functional" else "NO" if status_label == "Faulty" else None,
        "ATTRIBUTE15": remarks or None,
    }
    values.update(attributes)
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
    text = plain(value)
    if not text:
        return None
    if header == "TAG_NUMBER" and blank_tag(text):
        return "Not Engraved"
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


def index_sources(rows_iter, registers: Registers) -> tuple[dict, dict]:
    costs: dict = {}
    lives: dict = {}
    displays: dict = {}
    for count, source in enumerate(rows_iter, 2):
        bare = display_item(canonical_item(UNIT.sub("", plain(source.get("Equipment/Item")) or plain(source.get("Item Description"))).strip()))
        asset_name = norm_name(bare)
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
        life = as_life(source.get("Life in Months"))
        if isinstance(life, (int, float)) and life >= 12:
            add_donor(lives, displays, asset_name, government, years, minor, int(life), lg_text)
        if count % 100000 == 0:
            print(f"indexed {count:,}", flush=True)
    return costs, lives


# ------------------------------------------------------------------- writing

def write_book(path: Path, header: list[str], rows, readme_lines) -> int:
    workbook = Workbook(write_only=True)
    sheet = workbook.create_sheet("Asset Register")
    sheet.freeze_panes = "A2"
    header_cells = []
    for value in header:
        cell = WriteOnlyCell(sheet, value=value)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E79")
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
    for line in readme_lines(count):
        notes.append([line])
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
        yield {name: row[position] if position < len(row) else None for name, position in index.items()}
    workbook.close()


BLANK_REASONS = {
    "ASSET_CATEGORY_MINOR3": "The guidelines classify to minor 2 (Annex 1); the item master that defines minor 3 was not supplied.",
    "LOCATION_SEGMENT4": "Neither the guidelines nor the source state a fourth location segment.",
    "ASSET_EXP_ACCT_FUND": "The guidelines do not state this account segment for these assets.",
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
    "ATTRIBUTE14": "The class attribute guide defines positions 1 to 13 only.",
}


def readme(stats: Counter, borrowed: bool, filled: Counter, headers: list[str]):
    def lines(count: int) -> list[str]:
        text = [
            "UgIFT asset register" + (" (REF: borrowed prices and calculated depreciation)" if borrowed else " (MF)"),
            "Built from ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx, one MF row per SK row. The SK workbook was not changed.",
            "Guideline sections used: GOU Asset Accounting Policies and Guidelines 2023 (April 2023) sections 3.1.3 and Annex 1 (classes and useful lives), "
            "3.2.1 (recognition conditions), 3.2.2 (initial cost; no capitalization threshold; illustration of ICT and other equipment over 5 years), "
            "3.2.3 (repairs and spare parts), 3.3.3 (small office equipment and loose tools expensed on 221012), 3.3.5 (group assets with subsidiary records), "
            "3.3.6 (donated assets), 5.5 (straight-line method; work in progress and operating leases not depreciated), 5.7 (nil residual value), "
            "5.14 (land not depreciated), Annex 2 (chart of accounts asset classification).",
            "One row is one physical asset (section 3.3.5 subsidiary record). FIXED_ASSETS_UNITS is 1. A counted source line is marked [item 1 of 100] in DESCRIPTION.",
            "ASSET_TYPE is CAPITALIZED only when section 3.2.1 holds: the facility controls the asset, it has service potential beyond one year, it exists "
            "(a line marked not received, not delivered, missing, lost, stolen or disposed does not), and its cost is measured on the source"
            + (" or borrowed on this workbook." if borrowed else ". Rows without a cost stay blank; the REF workbook fills them after borrowing."),
            "Kettles, spoons, forks, calculators, staplers, pen-holders, punches, paper trays, pin and staple holders and typewriters (section 3.3.3) are not capitalized; "
            "their expense account is 221012 and they carry no class or life. Single-use packs, graph paper and other consumables are not capitalized. Natural resources are not capitalized (3.2.1.4).",
            "ASSET_CATEGORY_MAJOR, MINOR1 and MINOR2 are the Annex 1 classes read from the asset name. Generic names (equipment, item, set, machine), totals, counts and consumable packs stay blank; no class is taken from the facility type. "
            "A row with a generic name is not capitalized either: its service potential beyond one year cannot be read from the source.",
            "DESCRIPTION is the equipment name in one spelling: the toolkit's spelling for its standard items, and title case for names the source typed in capitals; a counted line carries [item 1 of 100]. DATE_PLACED_IN_SERVICE is a date where the source states one and otherwise the source wording (a year or a financial year).",
            "LIFE_IN_MONTHS is the source life where stated, otherwise the Annex 1 life of the class (ICT and other equipment 60 months). DEPRECIATE_FLAG is YES with DEPRN_METHOD_CODE STL where a life applies (section 5.5); "
            "NO for land (5.14), work in progress and operating leases (5.5). SALVAGE_VALUE is 0 on depreciable rows (5.7); the source recorded no residual values.",
            "ASSET_EXP_ACCT_ACCOUNT is 221012 for small office equipment and loose tools (3.3.3), and for a capitalized asset the Annex 2 depreciation expense account of its class (2312xx, e.g. 231221 Light ICT hardware, 231235 Furniture and Fittings, 231233 Medical and Laboratory appliances), the account the sample row uses. "
            "ASSET_CLR_ACCT_ACCOUNT is 513001 (net assets/accumulated funds), the account the guidelines credit when an asset is brought into the register (3.2.2 illustration) and the sample row's clearing account. No other account segment is stated by the guidelines.",
            "PRORATE_CONVENTION_CODE is GOU PRO CO on depreciable rows: section 3.3.5.2 states that depreciation begins on the first day of the month the asset is available for use, and the sample row codes that convention GOU PRO CO.",
            "BOOK_TYPE_CODE is the local government in upper case without District, Local Government or DLG wording, hyphens as spaces, MC or CITY kept, and BK appended (HOIMA BK, MADI OKOLLO BK, KIIRA MC BK). "
            "LOCATION_SEGMENT1 is the same government in vote form (MADI\\-OKOLLO DLG, BUSIA MC, MBARARA CITY). LOCATION_SEGMENT2 is the department in upper case. LOCATION_SEGMENT3 is the facility, ending in Seed Secondary School or Health Centre III.",
            "Equipment status is written as Functional or Faulty only; IN_USE_FLAG is YES for Functional and NO for Faulty. Longer status wording is in ATTRIBUTE15 (Remarks). A blank or placeholder tag is Not Engraved; a real engraved number is kept as written.",
            "SERIAL_NUMBER, MANUFACTURER_NAME and MODEL_NUMBER are filled only where the source states them explicitly (serial, s/n, model, made by).",
            "ATTRIBUTE1 to ATTRIBUTE13 keep the sample headers; their meaning follows the class attribute guide (Updated Attributes for Asset Categories.xlsx) and each is filled only where the source states the fact: "
            "for ICT, office, electrical, medical, precision and furniture classes ATTRIBUTE1 tag/engrave code, ATTRIBUTE2 serial number (furniture: user), ATTRIBUTE3 material type, ATTRIBUTE4 make, ATTRIBUTE5 condition (Good and In Use, Needs Repair, Obsolete), "
            "ATTRIBUTE6 date of purchase, ATTRIBUTE7 user name, ATTRIBUTE8 user title; for vehicles ATTRIBUTE1 registration, ATTRIBUTE2 engine type, ATTRIBUTE3 chassis, ATTRIBUTE4 make, ATTRIBUTE6 date of purchase, ATTRIBUTE7 condition (Running, Grounded, Needs Repair); "
            "for buildings ATTRIBUTE1 plot, ATTRIBUTE4 use, ATTRIBUTE7 rooms, ATTRIBUTE8 date of purchase, ATTRIBUTE9 term; for land ATTRIBUTE1 tenure, ATTRIBUTE6 purpose, ATTRIBUTE7 status.",
            "ATTRIBUTE15 holds Remarks: the sanitized Equipment status (Functional or Faulty), the source status wording moved out of the status field, the source Remarks, and every SK field with no column in A-BL and no class attribute, each labelled with its source column name (Facility type, Item description, Date of purchase, Date placed in service where the source wrote words instead of a date, Recoverable cost, Source net book value, Source file, Source location). "
            "The sample header has no Remarks or Net Book Value column and the attribute guide defines positions 1 to 13 only, so position 15 is used. Recoverable cost is not written as SALVAGE_VALUE.",
            "Every filled cell was sanitized: trimmed, single spaces, no line breaks, placeholders (N/A, nil, none, -) cleared, one spelling per fact. Amounts are shown with thousands separators (#,##0.##) and were not recalculated while cleaning.",
            "Columns left blank and why:",
        ]
        for header in headers:
            if filled.get(header, 0) == 0:
                text.append(f"  {header}: {BLANK_REASONS.get(header, 'The guidelines and the source do not state it for any row.')}")
        text.append(f"Rows: {count:,}. Classified rows: {stats['class']:,}. Capitalized rows: {stats['capitalized']:,}.")
        if borrowed:
            text.extend([
                "Borrowed purchase costs: a white cost cell is a price stated on the source. Blue (#9DC3E6): median price of assets with the same name in the same local government, same purchase year or the closest year. "
                "Orange (#F4B183): other local governments, same year or the nearest period. Green (#C6EFCE): the whole workbook, used only when steps 1 and 2 found no price. Where both rows have an asset class, the class matches. "
                "Generic names (equipment, furniture, medical equipment, item, set, machine, buildings, land) borrow nothing. The cell colour is the only marker; Remarks never say a cost or life was borrowed.",
                "Borrowed useful lives follow the same order and colours: the most common life of assets with the same name, only where life is at least 12 months and the asset is not marked out of use. A life already on the row stays white.",
                "Straight-line depreciation is calculated to 30 September 2026 where cost, nil residual (5.7), life in months and the month placed in service are known and the asset is in use: monthly charge = (cost - residual) / life; "
                "DEPRN_RESERVE runs from the placed-in-service month through September 2026 and stops at the end of the useful life; YTD_DEPRN is the July-September 2026 portion; net book value (cost - accumulated depreciation) is written in ATTRIBUTE15 because the sample header has no NBV column. Amounts already on the source were left unchanged.",
                "After borrowing, ASSET_TYPE is CAPITALIZED where the section 3.2.1 tests are met and the row is not small office equipment, a loose tool or a consumable.",
                f"Borrowed costs: same government {stats['cost_1']:,}; other governments {stats['cost_2']:,}; whole workbook {stats['cost_3']:,}. "
                f"Borrowed lives: same government {stats['life_1']:,}; other governments {stats['life_2']:,}; whole workbook {stats['life_3']:,}. "
                f"Depreciation reserve calculated on {stats['reserve']:,} rows; year-to-date on {stats['ytd']:,} rows.",
            ])
        else:
            text.append("This workbook does not borrow missing prices. Borrowed prices and lives, with colours, are in REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx.")
        return text

    return lines


def emit(borrow: bool, registers: Registers, costs: dict, lives: dict, stats: Counter, filled: Counter, limit: int | None):
    for source in source_rows(limit):
        values = build_values(source, registers, borrow=borrow, costs=costs, lives=lives, stats=stats)
        for header, value in zip(registers.headers, values):
            if value is not None and not (isinstance(value, tuple) and value[0] is None):
                filled[header] += 1
        yield values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=None, help="only the first N SK rows (for a sample run)")
    parser.add_argument("--only", choices=["mf", "ref"], default=None)
    args = parser.parse_args()
    registers = Registers(read_headers())
    print("indexing source prices", flush=True)
    costs, lives = index_sources(source_rows(), registers)
    if args.only != "ref":
        print("writing MF", flush=True)
        stats: Counter = Counter()
        filled: Counter = Counter()
        write_book(MF, registers.headers, emit(False, registers, costs, lives, stats, filled, args.limit), readme(stats, False, filled, registers.headers))
    if args.only != "mf":
        print("writing REF", flush=True)
        stats = Counter()
        filled = Counter()
        write_book(REF, registers.headers, emit(True, registers, costs, lives, stats, filled, args.limit), readme(stats, True, filled, registers.headers))


if __name__ == "__main__":
    main()
