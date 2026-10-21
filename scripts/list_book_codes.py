"""Refresh the package README's BOOK_TYPE_CODE index from the current register."""

from __future__ import annotations

import argparse
import html
import re
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "outputs"
    / "asset-register"
    / "UGIFT-ASSET-REGISTER-21102026.xlsx"
)
OUTPUT = SOURCE.with_name("README.md")
INDEX_START = "<!-- book-type-code:start -->"
INDEX_END = "<!-- book-type-code:end -->"
CELL = re.compile(br'<c\b(?=[^>]*\br="A\d+")[^>]*(?<!/)>.*?</c>', re.DOTALL)
CELL_TYPE = re.compile(br'\bt="([^"]*)"')
TEXT = re.compile(br'<t(?:\s[^>]*)?>(.*?)</t>', re.DOTALL)
NUMBER = re.compile(br'<v>([^<]*)</v>')
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def _normalize_text(text: str) -> str:
    text = text.replace("\u2028", " ").replace("\u2029", " ")
    return re.sub(r"\s+", " ", text).strip()


def cell_text(raw: bytes) -> str:
    return _normalize_text(html.unescape(raw.decode("utf-8", "replace")))


def book_code_index_counts(markdown: str) -> Counter[str]:
    """Read only the marked book-code table, excluding other README tables."""
    if markdown.count(INDEX_START) != 1 or markdown.count(INDEX_END) != 1:
        raise ValueError("Expected one book-code index marker pair")
    start = markdown.index(INDEX_START) + len(INDEX_START)
    end = markdown.index(INDEX_END)
    if end < start:
        raise ValueError("Book-code index markers are out of order")
    counts: Counter[str] = Counter()
    for line in markdown[start:end].splitlines():
        if match := re.fullmatch(r"\|\s*\d+\s*\|\s*(.*?)\s*\|\s*([\d,]+)\s*\|", line):
            counts[match.group(1).replace(r"\|", "|")] += int(match.group(2).replace(",", ""))
    return counts


def book_code_counts(source: Path) -> Counter[str]:
    """Count inline, shared-string and numeric codes without loading the sheet."""
    counts: Counter[str] = Counter()
    with zipfile.ZipFile(source) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in workbook.namelist():
            with workbook.open("xl/sharedStrings.xml") as strings:
                for _, element in ET.iterparse(strings, events=("end",)):
                    if element.tag == NS + "si":
                        parts = []
                        for child in element:
                            if child.tag == NS + "t":
                                parts.append(child.text or "")
                            elif child.tag == NS + "r":
                                parts.append(child.findtext(NS + "t", ""))
                        shared_strings.append("".join(parts))
                        element.clear()
        pending = b""
        while chunk := sheet.read(1024 * 1024):
            pending += chunk
            boundary = pending.rfind(b"</row>")
            if boundary < 0:
                continue
            boundary += len(b"</row>")
            complete, pending = pending[:boundary], pending[boundary:]
            for cell in CELL.findall(complete):
                kind = CELL_TYPE.search(cell)
                value = NUMBER.search(cell)
                if kind is not None and kind.group(1) == b"s":
                    if value is not None:
                        counts[_normalize_text(shared_strings[int(value.group(1))])] += 1
                elif text := TEXT.findall(cell):
                    counts[cell_text(b"".join(text))] += 1
                elif value is not None:
                    counts[cell_text(value.group(1))] += 1
    counts.pop("BOOK_TYPE_CODE", None)  # the header cell A1 is not a code
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", type=Path, default=SOURCE, help="Asset-register workbook to read")
    parser.add_argument("--out", type=Path, help="Markdown output path; defaults to README.md beside the workbook")
    args = parser.parse_args()
    output = args.out or args.ref.with_name(OUTPUT.name)
    counts = book_code_counts(args.ref)
    lines = [
        "## BOOK_TYPE_CODE",
        "",
        f"{len(counts):,} unique values in `{args.ref.name}`.",
        "",
        "| No. | Book code | Rows |",
        "|---:|---|---:|",
    ]
    ordered = sorted(counts.items(), key=lambda item: (item[0].casefold(), item[0]))
    for number, (name, count) in enumerate(ordered, start=1):
        lines.append(f"| {number} | {name.replace('|', '\\|')} | {count:,} |")
    output.parent.mkdir(parents=True, exist_ok=True)
    index = f"{INDEX_START}\n" + "\n".join(lines) + f"\n{INDEX_END}\n"
    existing = output.read_text(encoding="utf-8") if output.exists() else "# UgIFT asset registers\n"
    if INDEX_START in existing or INDEX_END in existing:
        if existing.count(INDEX_START) != 1 or existing.count(INDEX_END) != 1:
            raise ValueError(f"Expected one book-code index marker pair in {output}")
        start = existing.index(INDEX_START)
        end = existing.index(INDEX_END)
        if end < start:
            raise ValueError(f"Book-code index markers are out of order in {output}")
        content = existing[:start] + index + existing[end + len(INDEX_END):].lstrip("\r\n")
    else:
        content = existing.rstrip() + "\n\n" + index
    output.write_text(content, encoding="utf-8")
    print(f"{len(counts):,} codes; {sum(counts.values()):,} rows -> {output}")


if __name__ == "__main__":
    main()
