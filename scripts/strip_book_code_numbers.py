"""Drop a stray number immediately before BK in the REF book code.

AGAGO 2 BK becomes AGAGO BK when AGAGO BK already exists.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "outputs" / "asset-register" / "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
CELL = re.compile(
    br'(<c r="A\d+"[^>]*><is><t>)([A-Z][A-Z ]*(?:MC|CITY)?)(?:\s+\d{1,3})( BK</t>)'
)
PLAIN = re.compile(br'<c r="A\d+"[^>]*><is><t>([A-Z][A-Z ]*(?:MC|CITY)? BK)</t>')


def main() -> None:
    with zipfile.ZipFile(PATH) as source:
        sheet = source.read("xl/worksheets/sheet1.xml")
        others = [
            (item, source.read(item.filename))
            for item in source.infolist()
            if item.filename != "xl/worksheets/sheet1.xml"
        ]
    plain = set(PLAIN.findall(sheet))

    def replace(match: re.Match[bytes]) -> bytes:
        base = match.group(2) + b" BK"
        if base in plain:
            return match.group(1) + base + b"</t>"
        return match.group(0)

    updated, count = CELL.subn(replace, sheet)
    temporary = PATH.with_suffix(".books.xlsx")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as target:
        for item, data in others:
            target.writestr(item, data)
        target.writestr("xl/worksheets/sheet1.xml", updated)
    temporary.replace(PATH)
    print(f"replaced {count:,} book codes")


if __name__ == "__main__":
    main()
