"""Find Description cells that begin with a leading 19 before lab stools."""
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drop_referral_hospitals_and_ubts import SheetReader, column_value, shared_labels

REF = Path(r"D:\coding\ugift-data-analysis\outputs\asset-register\REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx")


def main() -> None:
    labels = shared_labels(REF)
    found = Counter()
    rows = []
    n = 0
    with zipfile.ZipFile(REF) as workbook, workbook.open("xl/worksheets/sheet1.xml") as sheet:
        reader = SheetReader(sheet)
        reader.take_until(b"<sheetData")
        reader.take_until(b">")
        while row := reader.next_row():
            n += 1
            if n == 1:
                continue
            text = column_value(row, b"B", labels)
            if "lab stool" in text.casefold():
                found[text] += 1
                if len(rows) < 5:
                    rows.append((n, text, column_value(row, b"BA", labels)[:80]))
    print("matches", sum(found.values()))
    for text, count in found.most_common():
        print(count, repr(text))
    print("samples", rows)


if __name__ == "__main__":
    main()
