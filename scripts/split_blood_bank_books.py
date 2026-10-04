"""Give Hoima, Arua and Soroti regional blood banks their own books.

Moves only those blood-bank rows. Other rows on ARUA BK, HOIMA CITY BK and
SOROTI BK stay. UBTS BK is emptied onto HOIMA RBB BK and ARUA RBB BK.
"""
from __future__ import annotations

import html
import re
import zipfile
from collections import Counter
from pathlib import Path

from drop_referral_hospitals_and_ubts import FILES, ROOT, SheetReader, column_value, shared_labels

BANKS = {
    "hoima": ("HOIMA RBB BK", "HOIMA RBB", "Hoima Regional Blood Bank"),
    "arua": ("ARUA RBB BK", "ARUA RBB", "Arua Regional Blood Bank"),
    "soroti": ("SOROTI RBB BK", "SOROTI RBB", "Soroti Regional Blood Bank"),
}
BY_FACILITY = {display: key for key, (_book, _segment, display) in BANKS.items()}
UBTS_BOOKS = {"UBTS BK", "Uganda Blood Transfusion Services"}
EXPECTED = {
    "REF": {"hoima": 170, "arua": 338, "soroti": 115},
    "MF": {"hoima": 171, "arua": 340, "soroti": 115},
    "SK": {"hoima": 171, "arua": 340, "soroti": 115},
}
STAY_OLD = "The Hoima, Arua and Soroti regional blood banks stay."
STAY_NEW = "The Hoima, Arua and Soroti regional blood banks each have their own book: HOIMA RBB BK, ARUA RBB BK and SOROTI RBB BK."
SOROTI_OLD = "Soroti Regional Blood Bank stays on the Soroti vote."
SOROTI_NEW = "Soroti Regional Blood Bank is on SOROTI RBB BK."
CODE_OLD = "OPM BK, UBTS BK)"
CODE_NEW = "OPM BK, HOIMA RBB BK, ARUA RBB BK, SOROTI RBB BK)"


def bank_from_text(text: str) -> str:
    found = []
    for key, (_book, _segment, display) in BANKS.items():
        if display.casefold() in text.casefold() or re.search(rf"(?i)\b{key}\b", text):
            found.append(key)
    if len(found) == 1:
        return found[0]
    if len(found) > 1:
        return "mixed"
    return ""


def classify(book: str, facility: str, blob: str) -> str:
    if facility in BY_FACILITY:
        return BY_FACILITY[facility]
    if book in UBTS_BOOKS:
        return bank_from_text(blob)
    return ""


def retarget(row_xml: bytes, column: bytes, new_text: str) -> bytes:
    match = re.search(br'<c r="' + column + br'(\d+)"([^>/]*)(?:/>|>(.*?)</c>)', row_xml, re.DOTALL)
    if match is None:
        raise RuntimeError(f"column {column.decode()} missing")
    number, attrs = match.group(1), match.group(2)
    style = re.search(br'\ss="(\d+)"', attrs)
    style_attr = b' s="' + style.group(1) + b'"' if style else b""
    cell = b'<c r="' + column + number + b'"' + style_attr + b' t="inlineStr"><is><t>' + html.escape(new_text).encode() + b"</t></is></c>"
    return row_xml[: match.start()] + cell + row_xml[match.end() :]


def fields_for(label: str) -> tuple[dict[str, bytes], tuple[bytes, bytes]]:
    if label == "SK":
        return {"book": b"P", "facility": b"Q", "remarks": b"O", "source": b"T"}, (b"P",)
    return {"book": b"A", "facility": b"K", "segment": b"I", "description": b"B", "remarks": b"BL"}, (b"A", b"I")


def rewrite_sheet(src, out, labels: dict[int, str], label: str) -> tuple[Counter[str], Counter[str]]:
    fields, _targets = fields_for(label)
    reader = SheetReader(src)
    out.write(reader.take_until(b"<sheetData"))
    out.write(reader.take_until(b">"))
    moved: Counter[str] = Counter()
    left: Counter[str] = Counter()
    seen = 0
    while row := reader.next_row():
        seen += 1
        if seen % 50000 == 0:
            print(f"  {label} row {seen:,}", flush=True)
        values = {name: column_value(row, column, labels) for name, column in fields.items()}
        blob = " ".join(values.get(name, "") for name in ("facility", "description", "remarks", "source"))
        which = classify(values["book"], values["facility"], blob)
        if not which:
            out.write(row)
            continue
        if which == "mixed":
            raise RuntimeError(f"{label} row names more than one blood bank: {values['book']} {values['facility'][:80]}")
        book, segment, display = BANKS[which]
        left[values["book"]] += 1
        if label == "SK":
            row = retarget(row, b"P", display)
        else:
            row = retarget(row, b"A", book)
            row = retarget(row, b"I", segment)
        moved[which] += 1
        out.write(row)
    out.write(reader.rest())
    print(f"  {label} moved {dict(moved)} from {dict(left)}", flush=True)
    return moved, left


def require_replace(data: bytes, old: str, new: str, required: bool) -> bytes:
    found = data.count(old.encode())
    if found == 0 and not required:
        return data
    if found != 1:
        raise RuntimeError(f"{old[:70]!r} found {found}")
    return data.replace(old.encode(), new.encode(), 1)


def patch_notes(name: str, member: str, data: bytes) -> bytes:
    data = require_replace(data, STAY_OLD, STAY_NEW, True)
    data = require_replace(data, SOROTI_OLD, SOROTI_NEW, name != "SK")
    data = require_replace(data, CODE_OLD, CODE_NEW, name != "SK")
    return data


def prepare(label: str, dest: Path) -> tuple[Counter[str], Counter[str]]:
    path = FILES[label]
    labels = shared_labels(path) if label == "REF" else {}
    moved: Counter[str] = Counter()
    left: Counter[str] = Counter()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(dest, "w", allowZip64=True) as zout:
        for info in zin.infolist():
            target = zipfile.ZipInfo(filename=info.filename, date_time=info.date_time)
            target.compress_type = info.compress_type or zipfile.ZIP_DEFLATED
            target.external_attr = info.external_attr
            if info.filename == "xl/worksheets/sheet1.xml":
                print("rewriting", path.name, flush=True)
                with zin.open(info) as src, zout.open(target, "w") as out:
                    moved, left = rewrite_sheet(src, out, labels, label)
                continue
            data = zin.read(info)
            if info.filename == "xl/sharedStrings.xml" or (info.filename == "xl/worksheets/sheet2.xml" and label != "REF"):
                data = patch_notes(label, info.filename, data)
            with zout.open(target, "w") as out:
                out.write(data)
    return moved, left


def verify(label: str, path: Path) -> None:
    labels = shared_labels(path) if label == "REF" else {}
    fields, _targets = fields_for(label)
    books: Counter[str] = Counter()
    stray = 0
    with zipfile.ZipFile(path) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        reader = SheetReader(sheet)
        reader.take_until(b"<sheetData")
        reader.take_until(b">")
        while row := reader.next_row():
            values = {name: column_value(row, column, labels) for name, column in fields.items()}
            book = values["book"]
            books[book] += 1
            facility = values["facility"]
            if facility in BY_FACILITY:
                expected_book = BANKS[BY_FACILITY[facility]][2 if label == "SK" else 0]
                if book != expected_book:
                    stray += 1
            if book in UBTS_BOOKS:
                stray += 1
    if stray:
        raise RuntimeError(f"{label} still has {stray} blood-bank rows on another book")
    expected = EXPECTED[label]
    for key, count in expected.items():
        book = BANKS[key][2 if label == "SK" else 0]
        if books[book] != count:
            raise RuntimeError(f"{label} {book} {books[book]}, expected {count}")
    print(label, "verified", {BANKS[key][0]: expected[key] for key in expected}, flush=True)


def update_readme(ref_moves: Counter[str], ref_left: Counter[str]) -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    start = text.index("<!-- book-type-code:start -->")
    end = text.index("<!-- book-type-code:end -->")
    rows = []
    for line in text[start:end].splitlines():
        match = re.fullmatch(r"\|\s*\d+\s*\|\s*(.*?)\s*\|\s*([\d,]+)\s*\|", line)
        if match:
            rows.append([match.group(1), int(match.group(2).replace(",", ""))])
    deductions = dict(ref_left)
    if sum(deductions.values()) != sum(ref_moves.values()):
        raise RuntimeError(f"deductions {sum(deductions.values())} != moves {sum(ref_moves.values())}")
    by_name = {name: count for name, count in rows}
    for name, count in deductions.items():
        if by_name.get(name, 0) < count:
            raise RuntimeError(f"{name} has {by_name.get(name)} rows, removing {count}")
        by_name[name] -= count
        if by_name[name] == 0:
            del by_name[name]
    for key, count in ref_moves.items():
        by_name[BANKS[key][0]] = count
    ordered = sorted(by_name.items(), key=lambda item: (item[0].casefold(), item[0]))
    lines = [
        "## BOOK_TYPE_CODE",
        "",
        f"{len(ordered):,} unique values in `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`.",
        "",
        "| No. | Book code | Rows |",
        "|---:|---|---:|",
    ]
    for number, (name, count) in enumerate(ordered, start=1):
        lines.append(f"| {number} | {name} | {count:,} |")
    index = "<!-- book-type-code:start -->\n" + "\n".join(lines) + "\n<!-- book-type-code:end -->\n"
    text = text[:start] + index + text[end + len("<!-- book-type-code:end -->") :].lstrip("\r\n")
    text = text.replace(STAY_OLD, STAY_NEW, 1)
    old_note = "Uganda Blood Transfusion Services stays, including the Hoima and Arua regional blood banks on `UBTS BK`. Soroti Regional Blood Bank stays on `SOROTI BK`."
    new_note = "Hoima, Arua and Soroti regional blood banks are on `HOIMA RBB BK`, `ARUA RBB BK` and `SOROTI RBB BK`."
    if old_note not in text:
        raise RuntimeError("README blood-bank sentence was not found")
    text = text.replace(old_note, new_note, 1)
    note = (
        "## Blood banks separated — 4 October 2026\n\n"
        "Hoima, Arua and Soroti regional blood banks now have their own books: `HOIMA RBB BK`, `ARUA RBB BK` and `SOROTI RBB BK`. "
        f"REF holds {ref_moves['hoima']:,} Hoima rows, {ref_moves['arua']:,} Arua rows and {ref_moves['soroti']:,} Soroti rows. "
        "Rows moved off `UBTS BK`, and the blood-bank rows moved off `HOIMA CITY BK`, `ARUA BK` and `SOROTI BK`. Other rows on those district and city books stayed.\n\n"
    )
    marker = "## Referral hospitals removed — 4 October 2026\n\n"
    if marker not in text:
        raise RuntimeError("referral section missing")
    text = text.replace(marker, note + marker, 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    moves = {}
    left = {}
    temps = {label: path.with_suffix(".rbb-tmp.xlsx") for label, path in FILES.items()}
    replaced = False
    try:
        for label in ("REF", "MF", "SK"):
            moves[label], left[label] = prepare(label, temps[label])
            if dict(moves[label]) != EXPECTED[label]:
                raise RuntimeError(f"{label} moves {dict(moves[label])}, expected {EXPECTED[label]}")
        print("verifying", flush=True)
        for label in ("REF", "MF", "SK"):
            verify(label, temps[label])
        for label, path in FILES.items():
            temps[label].replace(path)
        replaced = True
        update_readme(moves["REF"], left["REF"])
    finally:
        if replaced:
            for temp in temps.values():
                if temp.exists():
                    temp.unlink()
    print("done", flush=True)


if __name__ == "__main__":
    main()
