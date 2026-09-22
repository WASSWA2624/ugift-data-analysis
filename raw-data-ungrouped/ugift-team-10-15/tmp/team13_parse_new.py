# -*- coding: utf-8 -*-
"""Parse Team 13 later chat: captions by date, docs, and which zip files are new vs already mapped."""
import re, sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, r"d:\coding\apps\ugift\src")
import team_registers as T
import team13_media

chat = Path(r"d:\coding\apps\ugift\tmp\team13-wa-later\WhatsApp Chat with Group 13 Ugift.txt")
text = chat.read_text(encoding="utf-8", errors="replace")

pat = re.compile(
    r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APap][Mm])?)\s+-\s+([^:]+):\s+(.*)$"
)
msgs = []
current = None
for line in text.splitlines():
    m = pat.match(line)
    if m:
        if current:
            msgs.append(current)
        current = {"date": m.group(1), "time": m.group(2), "sender": m.group(3).strip(), "text": m.group(4)}
    elif current:
        current["text"] += "\n" + line
if current:
    msgs.append(current)

# Collect already-mapped source filenames
t = T.TEAMS["team-13"]
team13_media.apply(t)
mapped = set()
mapped.update(t.get("team_docs", {}))
mapped.update(t.get("repeats", {}))
for d, cfg in t["districts"].items():
    mapped.update(cfg.get("lg_docs", {}))
    for fac, files in cfg.get("facilities", {}).items():
        mapped.update(files)

zip_files = [p.name for p in Path(r"d:\coding\apps\ugift\tmp\team13-wa-later").iterdir() if p.is_file()]
print("ZIP files:", len(zip_files))
print("MAPPED source names:", len(mapped))
new = [f for f in sorted(zip_files) if f not in mapped and not f.lower().endswith(".txt")]
print("NEW (not in mapping):", len(new))
for f in new:
    print(" ", f)

print("\n===== TEXT MESSAGES (no file attached) from 8/31 onward =====")
for msg in msgs:
    # parse date loosely
    d = msg["date"]
    # keep 8/31, 9/1, 9/2
    if not (d.startswith("8/31") or d.startswith("31/8") or d.startswith("9/1") or d.startswith("9/2") or d.startswith("1/9") or d.startswith("2/9")):
        continue
    t = msg["text"]
    if "(file attached)" in t and t.strip().endswith("(file attached)"):
        continue  # bare attachment, no caption
    preview = t.replace("\n", " | ")[:500]
    print(f"{msg['date']} {msg['time']} | {msg['sender'][:28]:28} | {preview}")

print("\n===== ALL CAPTIONED ATTACHMENTS 8/31+ =====")
att = re.compile(r"^((?:IMG|VID|STK)-[\w-]+\.\w+|\S.*?\.(?:pdf|xlsx|xls|docx))\s+\(file attached\)(?:\s*\n?(.*))?$", re.S)
for msg in msgs:
    d = msg["date"]
    if not (d.startswith("8/31") or d.startswith("31/8") or d.startswith("9/") or d.startswith("1/9") or d.startswith("2/9")):
        continue
    m = re.match(r"^(.+?) \(file attached\)(?:\n?(.*))?$", msg["text"], re.S)
    if not m:
        if "(file attached)" not in msg["text"] and "omitted" not in msg["text"].lower():
            print(f"TEXT {msg['date']} {msg['time']} | {msg['sender'][:24]:24} | {msg['text'][:300].replace(chr(10),' | ')}")
        continue
    fn, cap = m.group(1), (m.group(2) or "").strip()
    if cap:
        print(f"{msg['date']} {msg['time']} | {fn} | {cap[:200]}")
