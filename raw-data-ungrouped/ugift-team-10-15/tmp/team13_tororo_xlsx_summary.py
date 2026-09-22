# -*- coding: utf-8 -*-
from collections import Counter
from pathlib import Path
import openpyxl

wb = openpyxl.load_workbook(
    Path(r"d:\coding\apps\ugift\tmp\team13-wa-later") / "TORORO DLG ASSET REGISTER FOR SEED SCHOOLS 25.26.xlsx",
    data_only=True)
ws = wb.active
locs = Counter()
headers = None
for i, row in enumerate(ws.iter_rows(values_only=True), 1):
    vals = list(row)
    if i == 1:
        headers = vals
        continue
    # heading rows: description filled, qty empty, looks like a school name
    desc = (vals[1] or "")
    qty = vals[2]
    loc = vals[6]
    if qty in (None, "") and desc and not str(desc).replace(".","").isdigit():
        print("HEAD", i, desc)
    if loc:
        locs[str(loc).strip()] += 1
print("\nLocations:")
for k, v in locs.most_common():
    print(f"  {v:4}  {k}")
print("total data rows-ish", sum(locs.values()))
