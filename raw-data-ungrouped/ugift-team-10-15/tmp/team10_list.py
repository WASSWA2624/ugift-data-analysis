# -*- coding: utf-8 -*-
import os, zipfile
from pathlib import Path

team = Path(r"d:\coding\apps\ugift\facility-registers\team-10")
print("=== DIR LISTING ===")
for p in sorted(team.iterdir()):
    kind = "DIR" if p.is_dir() else "FILE"
    size = p.stat().st_size if p.is_file() else "-"
    print(f"{kind:4} {size:>12}  {p.name!r}")

zpath = team / "WhatsApp Chat with Ugift Team 10.zip"
print("\nZIP exists:", zpath.exists(), "size:", zpath.stat().st_size if zpath.exists() else None)
if zpath.exists():
    with zipfile.ZipFile(zpath) as z:
        names = z.namelist()
    print("ZIP entries:", len(names))
    exts = {}
    bases = []
    for n in names:
        b = n.split("/")[-1]
        if not b:
            continue
        bases.append(b)
        e = Path(b).suffix.lower() or "(none)"
        exts[e] = exts.get(e, 0) + 1
    print("ZIP by ext:", sorted(exts.items()))
    print("ZIP unique basenames:", len(set(bases)))
    # write list
    out = Path(r"d:\coding\apps\ugift\tmp\team10_zip_names.txt")
    out.write_text("\n".join(sorted(set(bases))), encoding="utf-8")
    print("wrote", out)
