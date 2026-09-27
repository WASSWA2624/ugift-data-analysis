"""Refresh the package README's BOOK_TYPE_CODE index from the REF register."""

from __future__ import annotations

import argparse
import html
import re
import zipfile
from collections import Counter
from pathlib import Path

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "outputs"
    / "asset-register"
    / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
)
OUTPUT = SOURCE.with_name("README.md")
INDEX_START = "<!-- book-type-code:start -->"
INDEX_END = "<!-- book-type-code:end -->"
TEXT = re.compile(br'<c r="A\d+"[^>]*><is><t[^>]*>([^<]*)</t>')
NUMBER = re.compile(br'<c r="A\d+"[^>]*><v>([^<]*)</v>')


def cell_text(raw: bytes) -> str:
    text = html.unescape(raw.decode("utf-8", "replace"))
    text = text.replace("\u2028", " ").replace("\u2029", " ")
    return re.sub(r"\s+", " ", text).strip()


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
    """Count the builder's inline book codes without loading the entire sheet."""
    counts: Counter[str] = Counter()
    with zipfile.ZipFile(source) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        pending = b""
        while chunk := sheet.read(1024 * 1024):
            pending += chunk
            boundary = pending.rfind(b"</row>")
            if boundary < 0:
                continue
            boundary += len(b"</row>")
            complete, pending = pending[:boundary], pending[boundary:]
            for pattern in (TEXT, NUMBER):
                counts.update(cell_text(value) for value in pattern.findall(complete))
    counts.pop("BOOK_TYPE_CODE", None)  # the header cell A1 is not a code
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", type=Path, default=SOURCE, help="REF workbook to read")
    parser.add_argument("--out", type=Path, help="Markdown output path; defaults to README.md beside the REF workbook")
    args = parser.parse_args()
    output = args.out or args.ref.with_name(OUTPUT.name)
    counts = book_code_counts(args.ref)
    lines = [
        "## BOOK_TYPE_CODE",
        "",
        f"{len(counts):,} unique values in `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`.",
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
