import re
import zipfile
from pathlib import Path

root = Path(r"D:\coding\ugift-data-analysis\outputs\asset-register")
pat = re.compile(br"([A-Z]{1,3})(\d+)")
files = [
    "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
    "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
    "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx",
]
for name in files:
    with zipfile.ZipFile(root / name) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        head = sheet.read(8000)
        sheet.seek(0, 2)
        size = sheet.tell()
        sheet.seek(max(0, size - 1500))
        tail = sheet.read()
    print("===", name)
    start = head.find(b"<sheetData")
    print("HEAD", [m.group(0).decode() for m in pat.finditer(head[:start])])
    end = tail.find(b"</sheetData>")
    print("TAIL", [m.group(0).decode() for m in pat.finditer(tail[end:])])
    wb = zipfile.ZipFile(root / name).read("xl/workbook.xml")
    print("WB", [m.group(0).decode() for m in pat.finditer(wb)])
