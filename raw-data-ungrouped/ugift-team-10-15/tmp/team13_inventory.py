# -*- coding: utf-8 -*-
import os, zipfile
from pathlib import Path
from collections import defaultdict

base = Path(r"d:\coding\apps\ugift\facility-registers\team-13")
print("=== TOP LEVEL ===")
for p in sorted(base.iterdir(), key=lambda x: x.name.lower()):
    kind = "DIR " if p.is_dir() else "FILE"
    size = p.stat().st_size if p.is_file() else ""
    print(f"{kind} {p.name}  {size}")

print("\n=== EXISTING TREE (non-image) ===")
counts = defaultdict(int)
exts = defaultdict(int)
for p in base.rglob("*"):
    if p.is_file() and "WhatsApp" not in p.parts and "_unpack" not in p.parts:
        counts[str(p.parent.relative_to(base))] += 1
        exts[p.suffix.lower()] += 1
print("-- by folder --")
for k, v in sorted(counts.items()):
    print(f"  {v:4}  {k}")
print("-- by ext --")
for k, v in sorted(exts.items(), key=lambda x: -x[1]):
    print(f"  {v:4}  {k}")

zips = list(base.glob("*.zip"))
print("\n=== ZIP CONTENTS ===")
for zpath in zips:
    print("ZIP:", zpath.name, "size", zpath.stat().st_size)
    with zipfile.ZipFile(zpath) as z:
        names = z.namelist()
        print("entries:", len(names))
        for n in sorted(names):
            info = z.getinfo(n)
            print(f"  {info.file_size:10}  {n}")
