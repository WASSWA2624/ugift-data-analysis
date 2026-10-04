"""Remove the leading quantity from '19 lab stools [item n of 19]' descriptions."""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drop_referral_hospitals_and_ubts import SheetReader, column_value, shared_labels
from patch_register_workbook import apply_updates

REF = Path(r"D:\coding\ugift-data-analysis\outputs\asset-register\REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx")
PATTERN = re.compile(r"^19 lab stools \[item (\d+) of 19\]$")


def main() -> None:
    labels = shared_labels(REF)
    updates = []
    rows = 0
    with zipfile.ZipFile(REF) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        reader = SheetReader(sheet)
        reader.take_until(b"<sheetData")
        reader.take_until(b">")
        while row := reader.next_row():
            rows += 1
            if rows == 1:
                continue
            text = column_value(row, b"B", labels)
            match = PATTERN.fullmatch(text)
            if not match:
                continue
            updates.append({
                "sheet": "Asset Register",
                "cell": f"B{rows}",
                "expected": text,
                "value": f"lab stools [item {match.group(1)} of 19]",
            })
    if len(updates) != 38:
        raise SystemExit(f"expected 38 descriptions, found {len(updates)}")
    destination = REF.with_suffix(".stool-tmp.xlsx")
    destination.unlink(missing_ok=True)
    apply_updates(REF, destination, updates)
    destination.replace(REF)
    print(f"updated {len(updates)} descriptions", flush=True)


if __name__ == "__main__":
    main()
