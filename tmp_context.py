import zipfile
from pathlib import Path

root = Path(r"D:\coding\ugift-data-analysis\outputs\asset-register")
with zipfile.ZipFile(root / "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx") as workbook:
    text = workbook.read("xl/worksheets/sheet2.xml").decode("utf-8")
start = text.find("Central government")
print(text[start:start + 2500])
print("---TAIL---")
print(text[text.find("Kampala Capital") - 400: text.find("Kampala Capital") + 200])
