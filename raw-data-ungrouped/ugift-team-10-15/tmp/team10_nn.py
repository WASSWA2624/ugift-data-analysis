# -*- coding: utf-8 -*-
import os, re
from pathlib import Path

base = Path(r"d:\coding\apps\ugift\facility-registers\team-10")
for dist in ["Nakapiripirit", "Amudat", "Nabilatuk", "Moroto", "Napak"]:
    d = base / dist
    if not d.exists():
        continue
    print("===", dist, "===")
    for fac in sorted(p for p in d.iterdir() if p.is_dir()):
        files = [f.name for f in fac.iterdir() if f.is_file()]
        media = [f for f in files if re.match(r"^\d+_", f)]
        nums = []
        for f in media:
            m = re.match(r"^(\d+)_", f)
            if m:
                nums.append(int(m.group(1)))
        mx = max(nums) if nums else 0
        jpg = sum(1 for f in files if f.lower().endswith(".jpg"))
        pdf = [f for f in files if f.lower().endswith(".pdf") and not re.match(r"^[A-Z]", f)]
        tk = [f for f in files if "Toolkit" in f or "hand-filled" in f]
        print(" %s  files=%d  numbered=%d  maxNN=%d  jpg=%d  tk=%s" % (
            fac.name, len(files), len(media), mx, jpg, tk[:6]))
