# -*- coding: utf-8 -*-
import zipfile, os
from pathlib import Path

zpath = Path(r"d:\coding\apps\ugift\facility-registers\team-10\WhatsApp Chat with Ugift Team 10.zip")
out = Path(r"d:\coding\apps\ugift\tmp\team10-wa")
out.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(zpath) as z:
    for info in z.infolist():
        print("ZIP:", repr(info.filename), "size", info.file_size)
        # extract
        target = out / Path(info.filename).name
        with z.open(info) as src, open(target, "wb") as dst:
            dst.write(src.read())
        print("  ->", target, target.stat().st_size)

print("\n=== extracted ===")
for p in sorted(out.iterdir()):
    print(p.name, p.stat().st_size)
