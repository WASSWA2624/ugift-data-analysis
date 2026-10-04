"""Remove referral-hospital rows from the three asset-register workbooks.

SK, MF and REF stay aligned. Uganda Blood Transfusion Services stays, as do the
Hoima, Arua and Soroti regional blood banks. A general hospital on a district vote
is kept. The rewrite drops worksheet rows and renumbers them. Shared strings that
name a removed vote stay in the string table so other cells that mention a hospital
in passing are not blanked.
"""
from __future__ import annotations

import bisect
import html
import re
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "outputs" / "asset-register"
FILES = {
    "REF": ROOT / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
    "MF": ROOT / "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
    "SK": ROOT / "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx",
}
EXPECTED = {
    "ARUA RRH BK": 251,
    "BUTABIKA NRMH BK": 288,
    "ENTEBBE RH BK": 269,
    "FORT PORTAL RRH BK": 203,
    "GULU RRH BK": 301,
    "HOIMA RRH BK": 223,
    "JINJA RRH BK": 305,
    "KABALE RRH BK": 347,
    "KAWEMPE RH BK": 196,
    "KAYUNGA RRH BK": 172,
    "KIRUDDU RH BK": 283,
    "LIRA RRH BK": 214,
    "MASAKA RRH BK": 363,
    "MBALE RRH BK": 229,
    "MBARARA RRH BK": 271,
    "MOROTO RRH BK": 368,
    "MUBENDE RRH BK": 220,
    "MULAGO NRH BK": 138,
    "NAGURU RH BK": 248,
    "SOROTI RRH BK": 214,
    "YUMBE RRH BK": 112,
}
DISPLAY = {
    "ARUA RRH BK": "Arua Regional Referral Hospital",
    "BUTABIKA NRMH BK": "Butabika National Referral Mental Hospital",
    "ENTEBBE RH BK": "Entebbe Regional Referral Hospital",
    "FORT PORTAL RRH BK": "Fort Portal Regional Referral Hospital",
    "GULU RRH BK": "Gulu Regional Referral Hospital",
    "HOIMA RRH BK": "Hoima Regional Referral Hospital",
    "JINJA RRH BK": "Jinja Regional Referral Hospital",
    "KABALE RRH BK": "Kabale Regional Referral Hospital",
    "KAWEMPE RH BK": "Kawempe National Referral Hospital",
    "KAYUNGA RRH BK": "Kayunga Regional Referral Hospital",
    "KIRUDDU RH BK": "Kiruddu National Referral Hospital",
    "LIRA RRH BK": "Lira Regional Referral Hospital",
    "MASAKA RRH BK": "Masaka Regional Referral Hospital",
    "MBALE RRH BK": "Mbale Regional Referral Hospital",
    "MBARARA RRH BK": "Mbarara Regional Referral Hospital",
    "MOROTO RRH BK": "Moroto Regional Referral Hospital",
    "MUBENDE RRH BK": "Mubende Regional Referral Hospital",
    "MULAGO NRH BK": "Mulago National Referral Hospital",
    "NAGURU RH BK": "China-Uganda Friendship Hospital Naguru",
    "SOROTI RRH BK": "Soroti Regional Referral Hospital",
    "YUMBE RRH BK": "Yumbe Regional Referral Hospital",
}
BOOK_BY_DISPLAY = {name: code for code, name in DISPLAY.items()}
ROW_NUMBER = re.compile(br'\br="(\d+)"')
SI = re.compile(br"<si>(.*?)</si>", re.DOTALL)
SI_TEXT = re.compile(br"<t[^>]*>(.*?)</t>", re.DOTALL)
BOOKS = {code: code for code in EXPECTED}
POLICY = (
    "Central government: ministries, agencies and referral hospitals keep their UgIFT assets on their own votes and stay on the register. "
    "Their BOOK_TYPE_CODE is the vote code Location(3)2.xlsx spells plus BK (MOFPED BK, MOH BK, MOES BK, MOLG BK, MOLHUD BK, MGLSD BK, MAAIF BK, MOWE BK, MOWT BK, NEMA BK, PPDA BK, OAG BK, OPM BK, UBTS BK for the regional blood banks, ARUA RRH BK and the other referral hospitals), "
    "LOCATION_SEGMENT1 that same code, LOCATION_SEGMENT2 the department the source states (else UNSPECIFIED, or HOSPITAL SERVICES for a hospital) and LOCATION_SEGMENT3 the site the source names (Finance Building, Embassy House, a district inspectorate, a blood bank) or UNSPECIFIED. "
    "Their rows come from the ministries' verification returns, the programme's fixed-asset registers, the two blood-bank inventories and the hospital rows of the consolidated MDA status register, as the SK Read Me records."
)
POLICY_NEW = (
    "Central government: ministries, agencies and Uganda Blood Transfusion Services keep their UgIFT assets on their own votes and stay on the register. "
    "The Hoima, Arua and Soroti regional blood banks stay. Kampala Capital City Authority, the Ministry of Defence and Veteran Affairs and the referral hospitals are left out. "
    "A ministry, agency or blood-bank BOOK_TYPE_CODE is the vote code Location(3)2.xlsx spells plus BK (MOFPED BK, MOH BK, MOES BK, MOLG BK, MOLHUD BK, MGLSD BK, MAAIF BK, MOWE BK, MOWT BK, NEMA BK, PPDA BK, OAG BK, OPM BK, UBTS BK), "
    "LOCATION_SEGMENT1 that same code, LOCATION_SEGMENT2 the department the source states (else UNSPECIFIED) and LOCATION_SEGMENT3 the site the source names (Finance Building, Embassy House, a district inspectorate or a blood bank) or UNSPECIFIED. "
    "Those rows come from the ministries' verification returns, the programme's fixed-asset registers and the Hoima and Arua blood-bank inventories, as the SK Read Me records. "
    "Soroti Regional Blood Bank stays on the Soroti vote. A general hospital held on a district vote stays on that district's book."
)
SK_OLD = (
    "Central government: ministries, agencies and referral hospitals keep their UgIFT assets on their own votes and stay on the register. Their rows come from"
)
SK_NEW = (
    "Central government: ministries, agencies and Uganda Blood Transfusion Services keep their UgIFT assets on their own votes and stay on the register. "
    "The Hoima, Arua and Soroti regional blood banks stay. Referral hospitals were removed on 4 October 2026. "
    "Kampala Capital City Authority and the Ministry of Defence and Veteran Affairs are left out. Ministry, agency and blood-bank rows come from"
)


def plain(raw: bytes) -> str:
    return html.unescape(raw.decode("utf-8", "replace")).replace("\u2028", " ").strip()


def shared_labels(path: Path) -> dict[int, str]:
    labels: dict[int, str] = {}
    with zipfile.ZipFile(path) as workbook:
        if "xl/sharedStrings.xml" not in workbook.namelist():
            return labels
        data = workbook.read("xl/sharedStrings.xml")
    for index, match in enumerate(SI.finditer(data)):
        parts = SI_TEXT.findall(match.group(1))
        labels[index] = plain(b"".join(parts)) if parts else ""
    return labels


def column_value(row_xml: bytes, column: bytes, labels: dict[int, str]) -> str:
    match = re.search(br'<c r="' + column + br'\d+"([^>/]*)(?:/>|>(.*?)</c>)', row_xml, re.DOTALL)
    if match is None or match.group(2) is None:
        return ""
    attrs, body = match.group(1), match.group(2)
    if b't="s"' in attrs:
        found = re.search(br"<v>(\d+)</v>", body)
        return labels.get(int(found.group(1)), "") if found else ""
    found = re.search(br"<t[^>]*>([^<]*)</t>", body, re.DOTALL)
    return plain(found.group(1)) if found else ""


class SheetReader:
    """Forward reader. Compacts the buffer instead of copying it on every row."""

    def __init__(self, handle):
        self.handle = handle
        self.buf = bytearray()
        self.pos = 0

    def _compact(self) -> None:
        if self.pos > 8 * 1024 * 1024:
            del self.buf[: self.pos]
            self.pos = 0

    def _fill(self) -> bool:
        self._compact()
        chunk = self.handle.read(8 * 1024 * 1024)
        if not chunk:
            return False
        self.buf += chunk
        return True

    def take_until(self, marker: bytes) -> bytes:
        while True:
            at = self.buf.find(marker, self.pos)
            if at != -1:
                end = at + len(marker)
                data = bytes(self.buf[self.pos : end])
                self.pos = end
                return data
            if not self._fill():
                raise RuntimeError(f"{marker!r} missing")

    def next_row(self) -> bytes | None:
        while True:
            row_end = self.buf.find(b"</row>", self.pos)
            if row_end != -1:
                end = row_end + len(b"</row>")
                row = bytes(self.buf[self.pos : end])
                self.pos = end
                return row
            if b"</sheetData>" in self.buf[self.pos : self.pos + 64]:
                return None
            if not self._fill():
                if b"</sheetData>" in self.buf[self.pos :]:
                    return None
                raise RuntimeError("worksheet ended inside a row")

    def rest(self) -> bytes:
        tail = [bytes(self.buf[self.pos :])]
        while chunk := self.handle.read(8 * 1024 * 1024):
            tail.append(chunk)
        return b"".join(tail)


def sheet_rows(path: Path):
    with zipfile.ZipFile(path) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        reader = SheetReader(sheet)
        reader.take_until(b"<sheetData")
        reader.take_until(b">")
        while row_xml := reader.next_row():
            yield int(ROW_NUMBER.search(row_xml).group(1)), row_xml


BLOOD_BANKS = ("Hoima Regional Blood Bank", "Arua Regional Blood Bank", "Soroti Regional Blood Bank")


def collect(path: Path, column: bytes, labels: dict[int, str], names: dict[str, str], facility_column: bytes) -> tuple[dict[str, list[int]], int, Counter[str], int]:
    found: dict[str, list[int]] = {code: [] for code in names.values()}
    seen: set[int] = set()
    banks: Counter[str] = Counter()
    book_counts: Counter[str] = Counter()
    ubts = 0
    last = 0
    for number, row_xml in sheet_rows(path):
        seen.add(number)
        last = number
        if number % 50000 == 0:
            print(f"  {path.name} row {number:,}", flush=True)
        if number == 1:
            continue
        label = column_value(row_xml, column, labels)
        if label:
            book_counts[label] += 1
        code = names.get(label)
        if code:
            found[code].append(number)
        elif label in {"UBTS BK", "Uganda Blood Transfusion Services"}:
            ubts += 1
        facility = column_value(row_xml, facility_column, labels)
        if facility in BLOOD_BANKS:
            banks[facility] += 1
    if seen != set(range(1, last + 1)):
        raise RuntimeError(f"{path.name} row numbers are not contiguous")
    return found, last, banks, ubts, book_counts


def require_replace(data: bytes, old: str, new: str) -> bytes:
    raw_old, raw_new = old.encode(), new.encode()
    found = data.count(raw_old)
    if found != 1:
        raise RuntimeError(f"{old[:80]!r} found {found}, expected 1")
    return data.replace(raw_old, raw_new, 1)


def stamp_last_row(blob: bytes, new_last: int) -> bytes:
    encoded = str(new_last).encode()

    def dimension(match: re.Match[bytes]) -> bytes:
        return match.group(1) + encoded + match.group(2)

    blob = re.sub(br'(<dimension ref="[A-Z]+\d+:[A-Z]+)\d+(")', dimension, blob, count=1)
    blob = re.sub(br'(<autoFilter ref="[A-Z]+\d+:[A-Z]+)\d+(")', dimension, blob, count=1)
    return blob


def rewrite_sheet(src, out, ordered: list[int], drop: set[int], new_last: int) -> None:
    reader = SheetReader(src)
    out.write(stamp_last_row(reader.take_until(b"<sheetData"), new_last))
    out.write(reader.take_until(b">"))
    kept = dropped = 0
    while row_xml := reader.next_row():
        old = int(ROW_NUMBER.search(row_xml).group(1))
        if old in drop:
            dropped += 1
            continue
        new = old - bisect.bisect_left(ordered, old)
        if new != old:
            row_xml = re.sub(
                br'r="([A-Z]*)' + str(old).encode() + br'"',
                lambda match, new=new: b'r="' + match.group(1) + str(new).encode() + b'"',
                row_xml,
            )
        out.write(row_xml)
        kept += 1
        if kept % 50000 == 0:
            print(f"  kept {kept:,}", flush=True)
    out.write(stamp_last_row(reader.rest(), new_last))
    if dropped != len(drop) or kept != new_last:
        raise RuntimeError(f"kept {kept}, dropped {dropped}, expected last row {new_last}")
    print(f"  kept {kept:,} dropped {dropped:,}", flush=True)


def prepare(path: Path, dest: Path, ordered: list[int], drop: set[int], new_last: int, column_letter: str) -> None:
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(dest, "w", allowZip64=True) as zout:
        for info in zin.infolist():
            target = zipfile.ZipInfo(filename=info.filename, date_time=info.date_time)
            target.compress_type = info.compress_type or zipfile.ZIP_DEFLATED
            target.external_attr = info.external_attr
            if info.filename == "xl/worksheets/sheet1.xml":
                print("rewriting", path.name, flush=True)
                with zin.open(info) as src, zout.open(target, "w") as out:
                    rewrite_sheet(src, out, ordered, drop, new_last)
                continue
            data = zin.read(info)
            if info.filename == "xl/sharedStrings.xml":
                data = require_replace(data, POLICY, POLICY_NEW)
            elif info.filename == "xl/worksheets/sheet2.xml" and path.name.startswith("ALL_UGIFT_ASSET_REGISTER_MF"):
                data = require_replace(data, POLICY, POLICY_NEW)
            elif info.filename == "xl/worksheets/sheet2.xml" and path.name.startswith("ALL_UGIFT_ASSET_REGISTER_SK"):
                data = require_replace(data, SK_OLD, SK_NEW)
            elif info.filename == "xl/workbook.xml":
                pattern = br"(<definedName name=\"_xlnm\._FilterDatabase\"[^>]*>\'Asset Register\'!\$A\$1:\$" + column_letter.encode() + br"\$)\d+"
                data, count = re.subn(pattern, lambda match: match.group(1) + str(new_last).encode(), data, count=1)
                if count != 1:
                    raise RuntimeError(f"{path.name} filter range was not updated")
            with zout.open(target, "w") as out:
                out.write(data)


def counts_ok(found: dict[str, list[int]]) -> None:
    actual = {code: len(rows) for code, rows in found.items()}
    if actual != EXPECTED:
        raise RuntimeError(f"counts {actual}")


def verify(path: Path, column: bytes, labels: dict[int, str], names: dict[str, str], facility_column: bytes, new_last: int, banks: Counter[str], ubts: int) -> None:
    found, last, kept_banks, kept_ubts, _books = collect(path, column, labels, names, facility_column)
    leftover = sum(len(rows) for rows in found.values())
    if leftover or last != new_last:
        raise RuntimeError(f"{path.name} still has {leftover} target rows, last row {last}")
    if kept_banks != banks or kept_ubts != ubts:
        raise RuntimeError(f"{path.name} blood banks changed from {banks} / {ubts} to {kept_banks} / {kept_ubts}")


def update_readme(ref_assets: int, sk_assets: int, books: Counter[str]) -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    start = text.index("<!-- book-type-code:start -->")
    end = text.index("<!-- book-type-code:end -->")
    rows = sorted(
        ((name, count) for name, count in books.items() if name not in EXPECTED and name != "BOOK_TYPE_CODE"),
        key=lambda item: (item[0].casefold(), item[0]),
    )
    removed = sum(EXPECTED.values())
    if sum(count for _, count in rows) != ref_assets or any(name in EXPECTED for name, _count in rows):
        raise RuntimeError(f"book index {len(rows)} codes, {sum(count for _, count in rows)} rows")
    lines = [
        "## BOOK_TYPE_CODE",
        "",
        f"{len(rows):,} unique values in `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`.",
        "",
        "| No. | Book code | Rows |",
        "|---:|---|---:|",
    ]
    for number, (name, count) in enumerate(rows, start=1):
        lines.append(f"| {number} | {name} | {count:,} |")
    index = "<!-- book-type-code:start -->\n" + "\n".join(lines) + "\n<!-- book-type-code:end -->\n"
    text = text[:start] + index + text[end + len("<!-- book-type-code:end -->") :].lstrip("\r\n")
    opening = (
        "It contains 234,351 asset rows. The IFMIS update of 28 September 2026 had brought the registers to 234,613 asset rows; "
        "KCCA and MoDVA were removed on 29 September 2026."
    )
    if opening not in text:
        raise RuntimeError("opening total sentence was not found")
    text = text.replace(
        opening,
        f"It contains {ref_assets:,} asset rows. The IFMIS update of 28 September 2026 had brought the registers to 234,613 asset rows; "
        "KCCA and MoDVA were removed on 29 September 2026. Referral hospitals were removed on 4 October 2026. "
        "The Hoima, Arua and Soroti regional blood banks stay.",
        1,
    )
    note = (
        "## Referral hospitals removed — 4 October 2026\n\n"
        f"Removed {removed:,} referral-hospital rows from the SK, MF and REF registers. "
        "Uganda Blood Transfusion Services stays, including the Hoima and Arua regional blood banks on `UBTS BK`. "
        "Soroti Regional Blood Bank stays on `SOROTI BK`. General hospitals held on a district vote were kept. "
        f"The REF register now contains {ref_assets:,} asset rows. The SK and MF registers now contain {sk_assets:,} asset rows.\n\n"
    )
    marker = "| `ifmis-review.csv` | Unresolved IFMIS identities and conflicting recorded facts. |\n\n"
    if marker not in text:
        raise RuntimeError("package table end was not found")
    text = text.replace(marker, marker + note, 1)
    history = (
        "### 4 October 2026 — referral hospitals removed\n\n"
        f"{removed:,} referral-hospital rows were removed from the SK, MF and REF registers. "
        "The Hoima, Arua and Soroti regional blood banks stay. "
        f"The REF register now contains {ref_assets:,} asset rows, and the SK and MF registers contain {sk_assets:,}.\n\n"
    )
    history_marker = "## Revision history\n\n"
    if history_marker not in text:
        raise RuntimeError("revision history missing")
    text = text.replace(history_marker, history_marker + history, 1)
    path.write_text(text, encoding="utf-8")


def preflight_text() -> None:
    with zipfile.ZipFile(FILES["REF"]) as workbook:
        shared = workbook.read("xl/sharedStrings.xml")
    with zipfile.ZipFile(FILES["MF"]) as workbook:
        mf_notes = workbook.read("xl/worksheets/sheet2.xml")
    with zipfile.ZipFile(FILES["SK"]) as workbook:
        sk_notes = workbook.read("xl/worksheets/sheet2.xml")
    if shared.count(POLICY.encode()) != 1 or mf_notes.count(POLICY.encode()) != 1:
        raise RuntimeError("MF or REF Read Me policy sentence was not found once")
    if sk_notes.count(SK_OLD.encode()) != 1:
        raise RuntimeError("SK Read Me policy sentence was not found once")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "It contains 234,351 asset rows." not in readme or "## Revision history\n\n" not in readme:
        raise RuntimeError("README markers were not found")


def main() -> None:
    if sum(EXPECTED.values()) != 5215 or set(DISPLAY) != set(EXPECTED):
        raise RuntimeError("expected removal table is inconsistent")
    preflight_text()
    ref_labels = shared_labels(FILES["REF"])
    if not set(EXPECTED) <= set(ref_labels.values()):
        raise RuntimeError("REF shared strings do not contain every referral-hospital book code")
    print("counting", flush=True)
    ref_found, ref_last, ref_banks, ref_ubts, ref_books = collect(FILES["REF"], b"A", ref_labels, BOOKS, b"K")
    mf_found, mf_last, mf_banks, mf_ubts, _mf_books = collect(FILES["MF"], b"A", {}, BOOKS, b"K")
    sk_found, sk_last, sk_banks, sk_ubts, _sk_books = collect(FILES["SK"], b"P", {}, BOOK_BY_DISPLAY, b"Q")
    counts_ok(ref_found)
    counts_ok(mf_found)
    counts_ok(sk_found)
    for label, banks, ubts in (("REF", ref_banks, ref_ubts), ("MF", mf_banks, mf_ubts), ("SK", sk_banks, sk_ubts)):
        if ubts < 1 or any(banks[name] == 0 for name in BLOOD_BANKS):
            raise RuntimeError(f"{label} blood banks {dict(banks)} UBTS {ubts}")
        print(label, "keeps", dict(banks), "UBTS", ubts, flush=True)
    drops = {
        "REF": set().union(*ref_found.values()),
        "MF": set().union(*mf_found.values()),
        "SK": set().union(*sk_found.values()),
    }
    if any(1 in rows for rows in drops.values()) or any(len(rows) != 5215 for rows in drops.values()):
        raise RuntimeError("unexpected drop set")
    print(
        {label: (len(rows), last) for label, rows, last in (
            ("REF", drops["REF"], ref_last), ("MF", drops["MF"], mf_last), ("SK", drops["SK"], sk_last)
        )},
        flush=True,
    )
    kept_books = sum(count for name, count in ref_books.items() if name not in EXPECTED)
    if kept_books != ref_last - 1 - len(drops["REF"]):
        raise RuntimeError(f"REF book totals {kept_books}, kept rows {ref_last - 1 - len(drops['REF'])}")
    plans = {
        "REF": (drops["REF"], ref_last - len(drops["REF"]), "BL"),
        "MF": (drops["MF"], mf_last - len(drops["MF"]), "BL"),
        "SK": (drops["SK"], sk_last - len(drops["SK"]), "U"),
    }
    temps = {label: path.with_suffix(".drop-tmp.xlsx") for label, path in FILES.items()}
    replaced = False
    try:
        for label, path in FILES.items():
            drop, new_last, column = plans[label]
            prepare(path, temps[label], sorted(drop), drop, new_last, column)
        print("verifying", flush=True)
        verify(temps["REF"], b"A", shared_labels(temps["REF"]), BOOKS, b"K", plans["REF"][1], ref_banks, ref_ubts)
        verify(temps["MF"], b"A", {}, BOOKS, b"K", plans["MF"][1], mf_banks, mf_ubts)
        verify(temps["SK"], b"P", {}, BOOK_BY_DISPLAY, b"Q", plans["SK"][1], sk_banks, sk_ubts)
        for label, path in FILES.items():
            temps[label].replace(path)
        replaced = True
        update_readme(plans["REF"][1] - 1, plans["SK"][1] - 1, ref_books)
    finally:
        if replaced:
            for temp in temps.values():
                if temp.exists():
                    temp.unlink()
    print("done", flush=True)


if __name__ == "__main__":
    main()
