import zipfile
from pathlib import Path

root = Path(r"D:\coding\ugift-data-analysis\outputs\asset-register")
needles = [
    b"KCCA",
    b"MODV",
    b"MoDVA",
    b"Kampala Capital",
    b"Ministry of Defence",
    b"Ministry of Defense",
]
files = [
    ("REF sheet1", "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx", "xl/worksheets/sheet1.xml"),
    ("REF strings", "REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx", "xl/sharedStrings.xml"),
    ("MF sheet1", "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx", "xl/worksheets/sheet1.xml"),
    ("MF sheet2", "ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx", "xl/worksheets/sheet2.xml"),
    ("SK sheet1", "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx", "xl/worksheets/sheet1.xml"),
    ("SK sheet2", "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx", "xl/worksheets/sheet2.xml"),
]
keep = max(len(n) for n in needles) - 1
for label, name, member in files:
    counts = {n: 0 for n in needles}
    with zipfile.ZipFile(root / name) as workbook, workbook.open(member) as handle:
        pending = b""
        while True:
            chunk = handle.read(8 * 1024 * 1024)
            data = pending + chunk
            if chunk:
                scan, pending = data[:-keep], data[-keep:]
            else:
                scan, pending = data, b""
            for needle in needles:
                counts[needle] += scan.count(needle)
            if not chunk:
                break
    shown = {n.decode(): v for n, v in counts.items() if v}
    print(label, shown or "none")
