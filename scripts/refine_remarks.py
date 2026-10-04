"""Rewrite ATTRIBUTE15 so each remark states function and notable facts only."""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drop_referral_hospitals_and_ubts import SheetReader, column_value, shared_labels
from patch_register_workbook import apply_updates

REF = Path(r"D:\coding\ugift-data-analysis\outputs\asset-register\REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx")
SHEET = "Asset Register"
DROP_PREFIX = re.compile(
    r"(?i)^(?:source file|source location|additional source|facility type)\s*:"
)
PROCESS_REVIEW = re.compile(
    r"(?i)(?:depreciation|ytd covers|unit cost|comparable|recorded department/room|"
    r"classification|carrying value|cost left blank|donor rows|recalculated)"
)
FIELD_CONCERN = re.compile(
    r"(?i)(not on the (?:ministry )?list|verify existence|write-off|missing|lost|stolen|"
    r"disposed|bodied off|boded off|could not (?:see|find)|cannot be found|condemned)"
)
STATUS_ONLY = re.compile(
    r"(?i)^(?:functional|functioning|working|in use|good(?:\s+and|\s*&\s*)?\s*functional|"
    r"faulty|non[-\s]?functional|not functional|not functioning)\.?$"
)
PLACEHOLDER = re.compile(r"(?i)^(?:n/?a|nil|none|not stated|unknown|-+)$")
RESIDUAL = re.compile(
    r"(?i)(?:"
    r"\b(?:ugx|ushs?|shs|shillings)\b|"
    r"\b(?:unit cost|depreciat\w*|carrying value|cost left blank|comparable|fixed-asset cost|purchase price|valuation|expensed item)\b|"
    r"\bytd covers\b|"
    r"team-\d+|_multi-team[/\\]|source file|source location|additional source|"
    r"\.(?:xls|xlsx|docx|pdf)\b|"
    r"\btable \d+\b|\brow \d+\b"
    r")"
)


def clauses(text: str) -> list[str]:
    return [part.strip(" ;") for part in re.split(r"\s*;\s*", text) if part.strip(" ;")]


def sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip(" .;")
    text = re.sub(r"(?i)\bboded off\b", "bodied off", text)
    text = re.sub(r"(?i)\bin user\b", "in use", text)
    text = re.sub(r"(?i)\bform the ministry\b", "from the ministry", text)
    if not text:
        return ""
    if text[-1] not in ".!?":
        text += "."
    return text[0].upper() + text[1:]


def condition_phrase(text: str) -> str:
    raw = re.sub(r"\s+", " ", text).strip(" .;")
    folded = raw.casefold()
    folded = folded.replace("in user", "in use").replace("&", "and")
    folded = re.sub(r"\s+", " ", folded)
    if folded in {"functional", "functioning", "working", "good and functional", "good functional"}:
        return ""
    if folded in {"in use and good condition", "in use and in good condition", "good condition and in use"}:
        return "In use and in good condition."
    if folded in {"good working condition", "good condition", "in good condition"}:
        return "Good working condition."
    if folded in {"faulty", "not functional", "non functional", "non-functional", "not functioning"}:
        return ""
    return sentence(raw)


def remarkable(text: str, description: str) -> str:
    cleaned = re.sub(r"(?i)^(?:engraving|source status|review|cost|recoverable cost|acc dep cost|net book value|ytd deprn)\s*:\s*", "", text).strip()
    if not cleaned or PLACEHOLDER.match(cleaned):
        return ""
    if description and cleaned.casefold() == description.casefold():
        return ""
    if re.fullmatch(r"(?i)not engraved|engraved", cleaned):
        return "Not engraved."
    return sentence(cleaned)


def clean_sentence(part: str) -> str:
    """Drop a cost, team-toolkit, or source-document sentence, keeping any other fact in it."""
    part = re.sub(r"(?i)\s*\(?\s*the team toolkit\b.*", "", part)
    part = re.sub(r"(?i)\s*team toolkit\b.*", "", part)
    part = re.sub(r"(?i)\s*cost (?:amount )?is for .*", "", part)
    part = re.sub(r"(?i),\s*cost is for .*", "", part)
    part = re.sub(r"(?i)\s+and the cost columns", " column", part)
    part = re.sub(r"(?i)\s+and no cost(?= or status)", "", part)
    part = part.strip(" ,;.")
    if not part:
        return ""
    if re.search(
        r"(?i)unit price|medical equipment list|no price is written|construction cost|"
        r"\bcost column\b|doesn.?t indicate the|fixed-asset cost|depreciat|comparable-price|\bugx\b",
        part,
    ):
        return ""
    if part[-1] not in ".!?":
        part += "."
    return part[0].upper() + part[1:]


def refine(remarks: str, in_use: str, description: str) -> str:
    status = ""
    extras: list[str] = []
    for clause in clauses(remarks):
        if DROP_PREFIX.match(clause) or re.search(r"(?i)recorded department/room", clause):
            continue
        if clause.casefold().startswith("source status:"):
            status = condition_phrase(clause.split(":", 1)[1])
            continue
        if clause.casefold().startswith("review:"):
            body = clause.split(":", 1)[1].strip()
            if FIELD_CONCERN.search(body):
                extras.append("Existence and write-off still need confirmation.")
            elif not PROCESS_REVIEW.search(body):
                extras.append(sentence(body))
            continue
        if re.fullmatch(r"(?i)cost:\s*ugx", clause):
            continue
        phrase = remarkable(clause, description)
        if phrase and phrase not in extras and not RESIDUAL.search(phrase):
            extras.append(phrase)
    if in_use == "YES":
        lead = "Functional."
    elif in_use == "NO":
        lead = "Not functional."
    else:
        lead = ""
    if status and STATUS_ONLY.match(status):
        status = ""
    parts = [lead]
    if status and status.casefold().strip(".") not in lead.casefold():
        parts.append(status)
    for extra in extras:
        folded = extra.casefold().strip(".")
        if any(folded == part.casefold().strip(".") or folded in part.casefold() for part in parts if part):
            continue
        parts = [part for part in parts if part.casefold().strip(".") not in folded]
        parts.append(extra)
    kept = []
    for part in parts:
        part = clean_sentence(part)
        if not part or RESIDUAL.search(part):
            continue
        kept.append(part)
    if not kept and (in_use == "YES" or in_use == "NO"):
        kept = ["Functional." if in_use == "YES" else "Not functional."]
    return " ".join(kept).strip()


def main() -> None:
    labels = shared_labels(REF)
    updates = []
    shown = 0
    rows = 0
    with zipfile.ZipFile(REF) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        reader = SheetReader(sheet)
        reader.take_until(b"<sheetData")
        reader.take_until(b">")
        while row := reader.next_row():
            rows += 1
            if rows == 1:
                continue
            current = column_value(row, b"BL", labels)
            revised = refine(current, column_value(row, b"AU", labels), column_value(row, b"B", labels))
            if not revised or revised == current:
                continue
            interesting = RESIDUAL.search(current)
            if interesting and shown < 6:
                print("OLD", current[:320].replace("\n", " "))
                print("NEW", revised[:320])
                print("---")
                shown += 1
            updates.append({
                "sheet": SHEET,
                "cell": f"BL{rows}",
                "expected": current,
                "value": revised,
            })
    print(f"changes {len(updates):,} of {rows - 1:,}", flush=True)
    if "--apply" not in sys.argv:
        return
    destination = REF.with_suffix(".remarks-tmp.xlsx")
    destination.unlink(missing_ok=True)
    apply_updates(REF, destination, updates)
    destination.replace(REF)
    print("applied", flush=True)


if __name__ == "__main__":
    main()
