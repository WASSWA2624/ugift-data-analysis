# -*- coding: utf-8 -*-
import os, re
from pathlib import Path

root = Path(r"d:\coding\apps\ugift")
team = root / "facility-registers" / "team-10"
wa = team / "WhatsApp Chat with Ugift Team 10"

print("ZIPS:", [p.name for p in team.glob("*.zip")])
print("WA exists:", wa.exists(), "is_dir:", wa.is_dir())
print("README files:")
for p in team.rglob("README.md"):
    print(" ", p)

wa_files = []
if wa.exists():
    for p in wa.iterdir():
        if p.is_file():
            wa_files.append(p.name)
print("WA file count:", len(wa_files))
exts = {}
for n in wa_files:
    e = Path(n).suffix.lower() or "(none)"
    exts[e] = exts.get(e, 0) + 1
print("WA by ext:", sorted(exts.items()))

src = (root / "src" / "team_registers.py").read_text(encoding="utf-8")
m = re.search(r'"team-10": \{', src)
m2 = re.search(r'"team-11": \{', src)
block = src[m.start():m2.start()]
mapped = set(re.findall(r'"((?:IMG|VID|STK|PTT|AUD)-[^"]+)"', block))
mapped |= set(re.findall(r'"([^"]+\.(?:pdf|docx|xlsx|xls|doc))"', block))
print("Mapped media/docs in team-10 block:", len(mapped))

skip = {
    "Team-10-Field-Itinerary-1.pdf",
    "SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx",
}

unfiled = [
    n for n in sorted(wa_files)
    if n not in mapped and n not in skip and not n.lower().endswith(".txt")
]
print("Unfiled count:", len(unfiled))
print("Unfiled:")
for n in unfiled:
    p = wa / n
    print(" ", n, p.stat().st_size)

missing_from_wa = sorted(mapped - set(wa_files))
print("Mapped but not in WA folder:", len(missing_from_wa))
for n in missing_from_wa[:40]:
    print(" ", n)

# repeats already defined?
repeats = re.findall(r'"((?:IMG|VID|STK)-[^"]+)"', src[src.find('"repeats"'):src.find('"team-11"') if False else m2.start()])
print("repeats keys near team-10 end - skip")

# also list existing filed photos in tree (excluding WA and reports)
filed = []
for dp, dns, fs in os.walk(team):
    if "WhatsApp" in dp or "_unpack" in dp:
        continue
    for f in fs:
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".mp4", ".pdf", ".xlsx", ".xls")):
            if re.match(r"^(?:[A-Z][A-Za-z]+-(?:school|health-centre|local-government-report|team-\d+-daily-log|LG-)|team-\d+-process-report)", f):
                continue
            if f == "Asset-Verification-Toolkit.docx":
                continue
            filed.append((os.path.relpath(os.path.join(dp, f), team), f))
print("Filed evidence files in tree:", len(filed))
