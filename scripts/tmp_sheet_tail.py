"""Inspect sheet tails and the exact KCCA/MoDVA read-me phrases."""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

ROOT = Path(r"D:\coding\ugift-data-analysis\outputs\asset-register")


def tail(name: str) -> None:
    path = ROOT / name
    with zipfile.ZipFile(path) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        sheet.seek(0, 2)
        size = sheet.tell()
        sheet.seek(max(0, size - 2500))
        data = sheet.read().decode("utf-8", "replace")
    print("===", name, "tail")
    print(data[-1800:])
    print()


def formulas(name: str) -> None:
    path = ROOT / name
    count = 0
    with zipfile.ZipFile(path) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        pending = b""
        while chunk := sheet.read(8 * 1024 * 1024):
            pending += chunk
            count += pending.count(b"<f>")
            count += pending.count(b"<f ")
            pending = pending[-10:]
    print(name, "formula tags", count)


def phrase(name: str, needle: str) -> None:
    path = ROOT / name
    with zipfile.ZipFile(path) as workbook:
        if "xl/sharedStrings.xml" in workbook.namelist():
            text = workbook.read("xl/sharedStrings.xml").decode("utf-8", "replace")
        else:
            text = workbook.read("xl/worksheets/sheet2.xml").decode("utf-8", "replace")
    start = 0
    print("=== phrases", name, needle)
    while True:
        index = text.find(needle, start)
        if index < 0:
            break
        print(text[max(0, index - 180): index + 220].replace("\n", " "))
        print("---")
        start = index + len(needle)


def main() -> None:
    for name in (
        "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx",
    ):
        tail(name)
        formulas(name)
    phrase("REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx", "KCCA BK")
    phrase("ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx", "KCCA BK")
    phrase("ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx", "Kampala Capital City Authority")
    phrase("ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx", "Ministry of Defence and Veteran Affairs")


if __name__ == "__main__":
    main()
