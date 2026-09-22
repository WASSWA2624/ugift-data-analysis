# -*- coding: utf-8 -*-
"""Patch src/team14_media/__init__.py with Sept 3 photo mappings from filed JSON."""
import json
import re
from pathlib import Path

ROOT = Path(r"d:\coding\apps\ugift")
filed = json.loads((ROOT / "tmp/t14_sep3_filed_photos.json").read_text(encoding="utf-8"))
init_path = ROOT / "src/team14_media/__init__.py"
text = init_path.read_text(encoding="utf-8")

# Build new entries for PHOTOS dict
new_entries = []
for key, files in sorted(filed["photos"].items()):
    district, facility = key.split("|", 1)
    body = []
    for img, (newname, cap) in files.items():
        if newname == "DEFER_BUBUNGI_CHALLENGES":
            continue
        body.append(
            "        %r: (\n"
            "            %r,\n"
            "            %r,\n"
            "        )," % (img, newname, cap)
        )
    if not body:
        continue
    new_entries.append(
        "    (%r, %r): {\n%s\n    }," % (district, facility, "\n".join(body))
    )

block = "\n".join(new_entries)

# Insert before the closing brace of PHOTOS = { ... }
# Find PHOTOS = { and its matching close before FACILITY_DOCS
m = re.search(r"^PHOTOS = \{", text, re.M)
if not m:
    raise SystemExit("PHOTOS not found")
start = m.end()
# find FACILITY_DOCS =
m2 = re.search(r"^FACILITY_DOCS = \{", text, re.M)
if not m2:
    raise SystemExit("FACILITY_DOCS not found")
# back up to the closing } of PHOTOS
before = text[:m2.start()].rstrip()
if not before.endswith("}"):
    raise SystemExit("expected PHOTOS to end before FACILITY_DOCS")
# insert before that closing }
# Find last }\n\n before FACILITY_DOCS
idx = before.rfind("\n}")
head = before[:idx]
tail = text[m2.start():]
# Avoid duplicating if already patched
if "IMG-20260903-WA0066.jpg" in text:
    print("already patched PHOTOS")
else:
    text = head + "\n" + block + "\n}\n\n" + tail
    init_path.write_text(text, encoding="utf-8")
    print("patched PHOTOS with", len(new_entries), "facility blocks")

# Add LG docs for scanned vouchers
lg_snip = '''        "Scanned_20260902_152229.pdf": (
            "Bududa-issue-and-goods-vouchers-scanned.pdf",
            "Bududa District issue and goods vouchers scanned on 2 September: "
            "issue vouchers 521 and 523 for Bubungi HC III, issue voucher 522 "
            "for Bupoto HC III, and goods voucher 634 for Bukalasi HC III.",
        ),
'''
# Put under Bududa in LG_DOCS if not present
if "Scanned_20260902_152229.pdf" not in init_path.read_text(encoding="utf-8"):
    text = init_path.read_text(encoding="utf-8")
    # LG_DOCS currently only has Sironko; add Bududa block
    if '"Bududa":' not in text.split("LG_DOCS = {", 1)[1].split("}", 1)[0]:
        text = text.replace(
            "LG_DOCS = {\n    \"Sironko\": {",
            "LG_DOCS = {\n    \"Bududa\": {\n"
            + lg_snip
            + "    },\n    \"Sironko\": {",
        )
        init_path.write_text(text, encoding="utf-8")
        print("added Bududa LG_DOCS")
    else:
        print("Bududa LG_DOCS present; manual check needed")
else:
    print("scan pdf already in init")
