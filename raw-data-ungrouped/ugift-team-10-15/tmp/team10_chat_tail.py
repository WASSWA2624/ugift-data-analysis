# -*- coding: utf-8 -*-
import sys
from pathlib import Path

chat = Path(r"d:\coding\apps\ugift\tmp\team10-wa\WhatsApp Chat with Ugift Team 10.txt")
text = chat.read_text(encoding="utf-8", errors="replace")
# strip bidi marks that break windows console
text = text.replace("\u2068", "").replace("\u2069", "").replace("\u200e", "").replace("\u200f", "")
lines = text.splitlines()

# print from 31 Aug afternoon onward, plus any 1 Sep
out = Path(r"d:\coding\apps\ugift\tmp\team10_chat_tail.txt")
keep = []
for i, line in enumerate(lines):
    if "9/1/26" in line or "9/01/26" in line or line.startswith("9/1/") or "8/31/26, 20" in line or "8/31/26, 21" in line or "8/31/26, 22" in line:
        keep.append("%d: %s" % (i, line))
    # also capture following caption lines without timestamps after 9/1
print("9/1 and late 8/31 lines:", len(keep))

# dump last 120 lines cleanly
tail = "\n".join(lines[-150:])
out.write_text(tail, encoding="utf-8")
print("wrote", out, "chars", len(tail))

# dump all 9/1 context
out2 = Path(r"d:\coding\apps\ugift\tmp\team10_chat_sep1.txt")
idxs = [i for i, line in enumerate(lines) if "9/1/26" in line]
start = max(0, (idxs[0] - 15) if idxs else 0)
out2.write_text("\n".join(lines[start:]), encoding="utf-8")
print("sep1 dump from line", start, "to", len(lines))
