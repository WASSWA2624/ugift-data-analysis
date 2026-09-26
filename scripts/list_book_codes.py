"""Write every distinct BOOK_TYPE_CODE from the REF register."""

from __future__ import annotations

import html
import re
import zipfile
from collections import Counter
from pathlib import Path

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "outputs"
    / "asset-register-2026-09-23"
    / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
)
OUTPUT = SOURCE.with_name("BOOK_TYPE_CODE.md")
TEXT = re.compile(br'<c r="A\d+"[^>]*><is><t[^>]*>([^<]*)</t>')
NUMBER = re.compile(br'<c r="A\d+"[^>]*><v>([^<]*)</v>')


def cell_text(raw: bytes) -> str:
    text = html.unescape(raw.decode("utf-8", "replace"))
    text = text.replace("\u2028", " ").replace("\u2029", " ")
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    sheet = zipfile.ZipFile(SOURCE).read("xl/worksheets/sheet1.xml")
    counts: Counter[str] = Counter()
    for value in TEXT.findall(sheet):
        counts[cell_text(value)] += 1
    for value in NUMBER.findall(sheet):
        counts[cell_text(value)] += 1
    lines = [
        "# BOOK_TYPE_CODE",
        "",
        f"{len(counts):,} unique values in `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`.",
        "",
        "| No. | Book code | Rows |",
        "|---:|---|---:|",
    ]
    ordered = sorted(counts.items(), key=lambda item: (item[0].casefold(), item[0]))
    for number, (name, count) in enumerate(ordered, start=1):
        lines.append(f"| {number} | {name.replace('|', '\\|')} | {count:,} |")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(counts):,} codes -> {OUTPUT}")


if __name__ == "__main__":
    main()
