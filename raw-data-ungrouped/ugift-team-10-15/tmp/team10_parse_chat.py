# -*- coding: utf-8 -*-
import os, re
from pathlib import Path

chat = Path(r"d:\coding\apps\ugift\tmp\team10-wa\WhatsApp Chat with Ugift Team 10.txt")
text = chat.read_text(encoding="utf-8", errors="replace")
print("chat chars:", len(text), "lines:", text.count("\n")+1)

# dates range
dates = re.findall(r"(\d{1,2}/\d{1,2}/\d{2,4})", text)
print("first 5 date tokens:", dates[:5], "last 5:", dates[-5:])

# media attachments mentioned
media = re.findall(r"((?:IMG|VID|STK|PTT|AUD)-[A-Za-z0-9-]+\.(?:jpg|jpeg|png|mp4|webp)|[^\n]+\.(?:pdf|docx|xlsx|xls|doc))", text, re.I)
print("attachment mentions:", len(media))
from collections import Counter
c = Counter(media)
print("unique attachments mentioned:", len(c))
# show non-img
for name, n in sorted(c.items()):
    if not name.upper().startswith(("IMG-", "VID-", "STK-", "AUD-", "PTT-")):
        print(" DOC:", repr(name), n)

print("\n=== LAST 80 LINES ===")
lines = text.splitlines()
for line in lines[-80:]:
    print(line)

print("\n=== PDF-related context ===")
for i, line in enumerate(lines):
    low = line.lower()
    if ".pdf" in low or "verification kit" in low or "seed sch" in low and "pdf" in low:
        start = max(0, i-2)
        end = min(len(lines), i+4)
        print("---")
        for j in range(start, end):
            print(f"{j}: {lines[j]}")
