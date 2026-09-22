# -*- coding: utf-8 -*-
"""Dump captions for new Team 13 photos as JSON for naming."""
import json, re
from pathlib import Path

chat = Path(r"d:\coding\apps\ugift\tmp\team13-wa-later\WhatsApp Chat with Group 13 Ugift.txt")
text = chat.read_text(encoding="utf-8", errors="replace")
pat = re.compile(
    r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APap][Mm])?)\s+-\s+([^:]+):\s+(.*)$"
)
msgs = []
cur = None
for line in text.splitlines():
    m = pat.match(line)
    if m:
        if cur:
            msgs.append(cur)
        cur = {"date": m.group(1), "time": m.group(2), "sender": m.group(3).strip(), "text": m.group(4)}
    elif cur:
        cur["text"] += "\n" + line
if cur:
    msgs.append(cur)

caps = {}
for msg in msgs:
    m = re.match(r"^(IMG-\d{8}-WA\d+\.jpg) \(file attached\)(?:\n?(.*))?$", msg["text"], re.S)
    if not m:
        continue
    fn, cap = m.group(1), (m.group(2) or "").strip()
    if fn.startswith("IMG-20260901-") or fn.startswith("IMG-20260902-"):
        caps[fn] = {
            "caption": cap,
            "sender": msg["sender"],
            "date": msg["date"],
            "time": msg["time"],
        }

out = Path(r"d:\coding\apps\ugift\tmp\team13_new_captions.json")
out.write_text(json.dumps(caps, indent=2, ensure_ascii=False), encoding="utf-8")
print("captions", len(caps))
uncap = [k for k, v in sorted(caps.items()) if not v["caption"]]
print("uncaptioned", len(uncap))
for k in uncap:
    print(" ", k)
