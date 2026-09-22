# -*- coding: utf-8 -*-
"""Extract Team 13 later WhatsApp zip and summarise chat attachments."""
import os, re, zipfile
from pathlib import Path
from collections import defaultdict

zip_path = Path(r"d:\coding\apps\ugift\facility-registers\team-13\WhatsApp Chat with Group 13 Ugift.zip")
dest = Path(r"d:\coding\apps\ugift\tmp\team13-wa-later")
dest.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(zip_path) as z:
    # extract only txt + non-jpg first for speed? actually extract all - we need photos
    names = z.namelist()
    print("extracting", len(names), "files")
    z.extractall(dest)

# flatten
for p in dest.rglob("*"):
    if p.is_file() and p.parent != dest:
        target = dest / p.name
        if not target.exists():
            p.rename(target)

chat = dest / "WhatsApp Chat with Group 13 Ugift.txt"
text = chat.read_text(encoding="utf-8", errors="replace")
print("chat bytes", chat.stat().st_size, "lines", text.count("\n")+1)

# WhatsApp format typically: DD/MM/YYYY, HH:MM - Name: message
# or [DD/MM/YYYY, HH:MM:SS] Name: message
attached = re.findall(r"((?:IMG|VID|STK|PTT|AUD)-[\w-]+\.(?:jpg|jpeg|png|webp|mp4|opus)|[^\n]+\.(?:pdf|xlsx|xls|docx|doc))", text, re.I)
print("attachment-like mentions in chat:", len(attached))

# Parse messages
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
print("parsed messages:", len(msgs))

# Print last 80 messages (new content) and any with pdf/xls
print("\n===== MESSAGES WITH DOCS OR CAPTIONS (non-omitted) =====")
omit = ("omitted",)
for i, msg in enumerate(msgs):
    t = msg["text"]
    if any(x in t.lower() for x in [".pdf", ".xls", ".xlsx", ".docx", ".mp4", "file attached"]) or (
        "<attached" in t.lower() or "(file attached)" in t.lower()
    ):
        preview = t.replace("\n", " | ")[:400]
        print(f"{msg['date']} {msg['time']} | {msg['sender'][:30]:30} | {preview}")

print("\n===== LAST 100 MESSAGES =====")
for msg in msgs[-100:]:
    preview = msg["text"].replace("\n", " | ")[:350]
    print(f"{msg['date']} {msg['time']} | {msg['sender'][:28]:28} | {preview}")
