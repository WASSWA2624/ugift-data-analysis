"""Find every KCCA / MoDVA mention in the asset-register package."""
from __future__ import annotations

import gzip
import re
import zipfile
from pathlib import Path

ROOT = Path(r"D:\coding\ugift-data-analysis\outputs\asset-register")
NEEDLES = ("KCCA", "MODV", "MoDVA", "MODVA", "Kampala Capital", "Ministry of Defence", "Ministry of Defense")


def show(label: str, text: str, limit: int = 12) -> None:
    print(f"--- {label}")
    count = 0
    for needle in NEEDLES:
        found = [match.start() for match in re.finditer(re.escape(needle), text)]
        if not found:
            continue
        print(f"  {needle}: {len(found)}")
        for start in found[:3]:
            snippet = text[max(0, start - 60): start + 80].replace("\n", " ")
            print("   ", snippet)
        count += len(found)
    if count == 0:
        print("  none")


def main() -> None:
    show("README", (ROOT / "README.md").read_text(encoding="utf-8"))
    show("validation", (ROOT / "validation-report.json").read_text(encoding="utf-8"))
    show("consolidation", (ROOT / "consolidation-report.json").read_text(encoding="utf-8"))
    show("ifmis", (ROOT / "ifmis-review.csv").read_text(encoding="utf-8", errors="replace"))
    with gzip.open(ROOT / "asset-register-audits.json.gz", "rt", encoding="utf-8", errors="replace") as handle:
        audit = handle.read()
    show("audits", audit, limit=6)
    for name in (
        "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx",
    ):
        with zipfile.ZipFile(ROOT / name) as workbook:
            sheet2 = workbook.read("xl/worksheets/sheet2.xml").decode("utf-8", "replace")
        show(name + " sheet2", sheet2)


if __name__ == "__main__":
    main()
