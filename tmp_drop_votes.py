"""Drop KCCA and MoDVA rows from the three asset-register workbooks."""
from __future__ import annotations

import bisect
import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(r"D:\coding\ugift-data-analysis\outputs\asset-register")
FILES = {
    "REF": ROOT / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
    "MF": ROOT / "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
    "SK": ROOT / "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx",
}
REF_CODES = {b"413971": "KCCA BK", b"420411": "MODV BK"}
MF_CODES = {b"KCCA BK": "KCCA BK", b"MODV BK": "MODV BK"}
SK_CODES = {
    b"Kampala Capital City Authority": "KCCA BK",
    b"Ministry of Defence and Veteran Affairs": "MODV BK",
}
CELL_REF = re.compile(br"([A-Z]{1,3})(\d+)")
ROW_NUMBER = re.compile(br'\br="(\d+)"')


def iter_complete(sheet, end_marker: bytes):
    pending = b""
    while True:
        end = pending.find(end_marker)
        if end != -1:
            end += len(end_marker)
            yield pending[:end]
            pending = pending[end:]
            continue
        chunk = sheet.read(8 * 1024 * 1024)
        if not chunk:
            if pending:
                yield pending
            return
        pending += chunk
        if len(pending) > 64 * 1024 * 1024:
            raise RuntimeError("worksheet row exceeded 64MB")


def column_text(row_xml: bytes, column: bytes) -> bytes:
    match = re.search(br'<c r="' + column + br'\d+"[^>]*>(.*?)</c>', row_xml, re.DOTALL)
    if match is None:
        return b""
    body = match.group(1)
    shared = re.search(br"<v>(\d+)</v>", body)
    if shared and b"<is>" not in body:
        return shared.group(1)
    text = re.search(br"<t[^>]*>(.*?)</t>", body, re.DOTALL)
    return text.group(1).strip() if text else b""


def drop_rows(path: Path, column: bytes, codes: dict[bytes, str]) -> dict[str, list[int]]:
    found: dict[str, list[int]] = {label: [] for label in dict.fromkeys(codes.values())}
    seen = set()
    with zipfile.ZipFile(path) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        started = False
        pending = b""
        while True:
            if not started:
                chunk = sheet.read(1024 * 1024)
                if not chunk:
                    break
                pending += chunk
                at = pending.find(b"<sheetData")
                if at < 0:
                    continue
                pending = pending[pending.find(b">", at) + 1 :]
                started = True
            end = pending.find(b"</row>")
            sheet_end = pending.find(b"</sheetData>")
            if sheet_end != -1 and (end == -1 or sheet_end < end):
                break
            if end == -1:
                chunk = sheet.read(8 * 1024 * 1024)
                if not chunk:
                    break
                pending += chunk
                continue
            end += len(b"</row>")
            row_xml = pending[:end]
            pending = pending[end:]
            number = int(ROW_NUMBER.search(row_xml).group(1))
            seen.add(number)
            label = codes.get(column_text(row_xml, column))
            if label:
                found[label].append(number)
    if seen != set(range(1, max(seen) + 1)):
        raise RuntimeError(f"{path.name} row numbers are not contiguous")
    print(path.name, "rows", max(seen), {label: len(rows) for label, rows in found.items()}, flush=True)
    return found


def shift_refs(blob: bytes, ordered: list[int]) -> bytes:
    def repl(match: re.Match[bytes]) -> bytes:
        old = int(match.group(2))
        if old <= 1:
            return match.group(0)
        return match.group(1) + str(old - bisect.bisect_left(ordered, old)).encode()

    return CELL_REF.sub(repl, blob)


def rewrite_sheet(src, out, ordered: list[int], drop: set[int]) -> dict[int, bytes]:
    samples: dict[int, bytes] = {}
    probe = min(drop) - 1
    preamble = b""
    while b"<sheetData" not in preamble:
        chunk = src.read(1024 * 1024)
        if not chunk:
            raise RuntimeError("sheetData missing")
        preamble += chunk
    at = preamble.find(b"<sheetData")
    head, rest = preamble[:at], preamble[at:]
    tag_end = rest.find(b">") + 1
    out.write(shift_refs(head, ordered))
    out.write(rest[:tag_end])
    pending = rest[tag_end:]
    kept = dropped = 0
    while True:
        end = pending.find(b"</row>")
        sheet_end = pending.find(b"</sheetData>")
        if sheet_end != -1 and (end == -1 or sheet_end < end):
            epilogue = pending[sheet_end:] + src.read()
            out.write(shift_refs(epilogue, ordered))
            break
        if end == -1:
            chunk = src.read(8 * 1024 * 1024)
            if not chunk:
                raise RuntimeError("truncated worksheet")
            pending += chunk
            continue
        end += len(b"</row>")
        chunk = pending[:end]
        pending = pending[end:]
        row_at = chunk.find(b"<row")
        out.write(chunk[:row_at])
        row_xml = chunk[row_at:]
        old = int(ROW_NUMBER.search(row_xml).group(1))
        if old in drop:
            dropped += 1
            continue
        new = old - bisect.bisect_left(ordered, old)
        if old in {2, probe}:
            samples[old] = row_xml
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
    if dropped != len(drop):
        raise RuntimeError(f"dropped {dropped}, expected {len(drop)}")
    print(f"  kept {kept:,} dropped {dropped:,}", flush=True)
    return samples


def require_replace(data: bytes, old: bytes, new: bytes, count: int) -> bytes:
    found = data.count(old)
    if found != count:
        raise RuntimeError(f"{old!r} found {found}, expected {count}")
    return data.replace(old, new)


def prepare(path: Path, dest: Path, drop: set[int], ordered: list[int], samples_out: dict) -> None:
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(dest, "w") as zout:
        for info in zin.infolist():
            target = zipfile.ZipInfo(filename=info.filename, date_time=info.date_time)
            target.compress_type = info.compress_type or zipfile.ZIP_DEFLATED
            target.external_attr = info.external_attr
            if info.filename == "xl/worksheets/sheet1.xml":
                print("rewriting", path.name, flush=True)
                with zin.open(info) as src, zout.open(target, "w") as out:
                    samples_out[path.name] = rewrite_sheet(src, out, ordered, drop)
                continue
            data = zin.read(info)
            if info.filename == "xl/sharedStrings.xml":
                data = require_replace(data, b"KCCA BK, ", b"", 1)
                for token in (b"KCCA BK", b"KCCA", b"MODV BK", b"MODV"):
                    data = require_replace(data, b"<si><t>" + token + b"</t></si>", b"<si><t></t></si>", 1)
                if b"KCCA" in data or b"MODV" in data:
                    raise RuntimeError("shared strings still name KCCA or MODV")
            elif info.filename == "xl/worksheets/sheet2.xml" and path.name.startswith("ALL_UGIFT_ASSET_REGISTER_MF"):
                data = require_replace(data, b"KCCA BK, ", b"", 1)
            elif info.filename == "xl/worksheets/sheet2.xml" and path.name.startswith("ALL_UGIFT_ASSET_REGISTER_SK"):
                data = require_replace(data, b"Kampala Capital City Authority 38; ", b"", 1)
                data = require_replace(data, b"Ministry of Defence and Veteran Affairs 9; ", b"", 1)
            elif info.filename == "xl/workbook.xml":
                data = require_replace(
                    data,
                    b"$225134",
                    b"$234380",
                    1,
                )
            with zout.open(target, "w") as out:
                out.write(data)


def row_xml(path: Path, number: int) -> bytes:
    token = f'<row r="{number}"'.encode()
    with zipfile.ZipFile(path) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        pending = b""
        while chunk := sheet.read(8 * 1024 * 1024):
            pending += chunk
            at = pending.find(token)
            if at != -1:
                end = pending.find(b"</row>", at)
                while end == -1:
                    extra = sheet.read(1024 * 1024)
                    if not extra:
                        break
                    pending += extra
                    end = pending.find(b"</row>", at)
                return pending[at : end + len(b"</row>")]
            pending = pending[-len(token) :]
    raise RuntimeError(f"row {number} missing in {path.name}")


def count_needles(path: Path, member: str) -> dict[str, int]:
    needles = [b"KCCA", b"MODV", b"MoDVA", b"Kampala Capital", b"Ministry of Defence", b"Ministry of Defense"]
    counts = {needle: 0 for needle in needles}
    keep = max(len(needle) for needle in needles) - 1
    with zipfile.ZipFile(path) as workbook, workbook.open(member) as handle:
        pending = b""
        while True:
            chunk = handle.read(8 * 1024 * 1024)
            data = pending + chunk
            scan, pending = (data[:-keep], data[-keep:]) if chunk else (data, b"")
            for needle in needles:
                counts[needle] += scan.count(needle)
            if not chunk:
                break
    return {needle.decode(): count for needle, count in counts.items() if count}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    start = text.index("<!-- book-type-code:start -->")
    end = text.index("<!-- book-type-code:end -->")
    rows = []
    for line in text[start:end].splitlines():
        match = re.fullmatch(r"\|\s*\d+\s*\|\s*(.*?)\s*\|\s*([\d,]+)\s*\|", line)
        if not match:
            continue
        name = match.group(1)
        if name in {"KCCA BK", "MODV BK"}:
            continue
        rows.append((name, int(match.group(2).replace(",", ""))))
    if len(rows) != 194 or sum(count for _, count in rows) != 234379:
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
    old = "234,613"
    if text.count(old) != 2:
        raise RuntimeError(f"expected two current totals, found {text.count(old)}")
    text = text.replace(old, "234,379")
    note = (
        "### 29 September 2026 — KCCA and MoDVA removed\n\n"
        "51 Kampala Capital City Authority rows and 183 Ministry of Defence and Veteran Affairs rows were removed from the SK, MF and REF registers.\n\n"
    )
    marker = "## Revision history\n\n"
    if marker not in text:
        raise RuntimeError("revision history missing")
    text = text.replace(marker, marker + note, 1)
    path.write_text(text, encoding="utf-8")


def update_reports() -> None:
    validation = ROOT / "validation-report.json"
    text = validation.read_text(encoding="utf-8")
    for line in ('        "KCCA BK": 51,\n', '        "MODV BK": 183,\n'):
        if text.count(line) != 2:
            raise RuntimeError(f"{line!r} count {text.count(line)}")
        text = text.replace(line, "")
    if text.count("234613") != 7:
        raise RuntimeError(f"validation totals {text.count('234613')}")
    text = text.replace("234613", "234379")
    hashes = {
        "4e21f42641927c4b821fbfa8c971199827e18893a8f748501cf06435bf8eaa6a": sha256(FILES["SK"]),
        "dd7c30f8275425c5da671440682aa7ad2ebae1c036d64cb368534b7ad8ff0da7": sha256(FILES["MF"]),
        "599e4e6430ee6e736805f772391fc51eea70efb40030dbcfb40e510f353a2b9a": sha256(FILES["REF"]),
    }
    for old, new in hashes.items():
        if text.count(old) != 1:
            raise RuntimeError(f"hash {old} count {text.count(old)}")
        text = text.replace(old, new)
    validation.write_text(text, encoding="utf-8")

    consolidation = ROOT / "consolidation-report.json"
    report = consolidation.read_text(encoding="utf-8")
    marker = '  "asset_rows": 234613,'
    if report.count(marker) != 1:
        raise RuntimeError("canonical asset_rows marker missing")
    report = report.replace(marker, '  "asset_rows": 234379,', 1)
    replacements = {
        "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx": sha256(FILES["MF"]),
        "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx": sha256(FILES["SK"]),
        "README.md": sha256(ROOT / "README.md"),
        "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx": sha256(FILES["REF"]),
        "validation-report.json": sha256(validation),
    }
    for name, digest in replacements.items():
        pattern = rf'("{re.escape(name)}": ")[0-9a-f]{{64}}(")'
        report, count = re.subn(pattern, rf"\g<1>{digest}\2", report, count=1)
        if count != 1:
            raise RuntimeError(f"hash field for {name} not updated")
    consolidation.write_text(report, encoding="utf-8")


def main() -> None:
    grouped = {}
    grouped["REF"] = drop_rows(FILES["REF"], b"A", REF_CODES)
    grouped["MF"] = drop_rows(FILES["MF"], b"A", MF_CODES)
    grouped["SK"] = drop_rows(FILES["SK"], b"P", SK_CODES)
    sets = []
    for label, found in grouped.items():
        if [len(found["KCCA BK"]), len(found["MODV BK"])] != [51, 183]:
            raise RuntimeError(f"{label} counts {found}")
        sets.append(set(found["KCCA BK"]) | set(found["MODV BK"]))
    if sets[0] != sets[1] or sets[1] != sets[2]:
        raise RuntimeError("KCCA and MODV row numbers differ between workbooks")
    drop = sets[0]
    if 1 in drop or len(drop) != 234:
        raise RuntimeError(f"unexpected drop set {len(drop)}")
    ordered = sorted(drop)
    print("drop", ordered[0], "...", ordered[-1], "last row", 234614 - len(drop), flush=True)
    temps = {label: path.with_suffix(".drop-tmp.xlsx") for label, path in FILES.items()}
    samples: dict[str, dict[int, bytes]] = {}
    try:
        for label, path in FILES.items():
            prepare(path, temps[label], drop, ordered, samples)
            before = min(drop) - 1
            for number in (2, before):
                if row_xml(temps[label], number) != samples[path.name][number]:
                    raise RuntimeError(f"{label} row {number} changed")
            members = ["xl/worksheets/sheet1.xml", "xl/worksheets/sheet2.xml"]
            if label == "REF":
                members.append("xl/sharedStrings.xml")
            for member in members:
                leftover = count_needles(temps[label], member)
                if leftover:
                    raise RuntimeError(f"{label} {member} still has {leftover}")
            print(label, "verified", flush=True)
        for label, path in FILES.items():
            temps[label].replace(path)
        update_readme()
        update_reports()
    finally:
        for temp in temps.values():
            if temp.exists():
                temp.unlink()
    print("done", flush=True)


if __name__ == "__main__":
    main()
