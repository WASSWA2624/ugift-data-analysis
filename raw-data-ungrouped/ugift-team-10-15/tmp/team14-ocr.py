# -*- coding: utf-8 -*-
"""OCR Team 14 unfiled photos (half-size) and write captions JSON."""
import json, os, sys, time
from PIL import Image
import numpy as np
import easyocr

SRC = r"d:\coding\apps\ugift\tmp\team14-wa\all"
OUT = r"d:\coding\apps\ugift\tmp\team14-ocr.json"
LOG = r"d:\coding\apps\ugift\tmp\team14-ocr-log.txt"

# already-mapped originals we do not need to OCR for filing
SKIP = {
    "IMG-20260824-WA0107.jpg", "IMG-20260824-WA0140.jpg", "IMG-20260824-WA0141.jpg",
    "IMG-20260824-WA0142.jpg", "IMG-20260824-WA0144.jpg", "IMG-20260824-WA0146.jpg",
    "IMG-20260824-WA0148.jpg", "IMG-20260826-WA0218.jpg", "IMG-20260826-WA0219.jpg",
    "IMG-20260826-WA0220.jpg", "IMG-20260826-WA0221.jpg", "IMG-20260826-WA0222.jpg",
    "IMG-20260826-WA0223.jpg", "IMG-20260826-WA0224.jpg", "IMG-20260826-WA0225.jpg",
    "IMG-20260826-WA0226.jpg", "IMG-20260826-WA0227.jpg", "IMG-20260826-WA0228.jpg",
    "IMG-20260826-WA0229.jpg", "IMG-20260826-WA0230.jpg", "IMG-20260826-WA0231.jpg",
    "IMG-20260826-WA0232.jpg", "IMG-20260826-WA0233.jpg", "IMG-20260826-WA0234.jpg",
    "IMG-20260826-WA0235.jpg", "IMG-20260826-WA0236.jpg",
}

# Bududa HC III already filed
for n in range(162, 195):
    SKIP.add("IMG-20260827-WA0%03d.jpg" % n)
# St Marys / Mutufu / Sisiyi already filed
for n in range(0, 62):
    SKIP.add("IMG-20260828-WA00%02d.jpg" % n)

done = {}
if os.path.isfile(OUT):
    done = json.load(open(OUT, encoding="utf-8"))

files = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".jpg") and f not in SKIP)
todo = [f for f in files if f not in done]
print("todo", len(todo), "done", len(done), "skip", len(SKIP), flush=True)

reader = easyocr.Reader(["en"], gpu=False, verbose=False)
t0 = time.time()
for i, f in enumerate(todo, 1):
    p = os.path.join(SRC, f)
    try:
        im = Image.open(p)
        w, h = im.size
        im = im.resize((max(1, w // 2), max(1, h // 2)))
        texts = reader.readtext(np.array(im), detail=0)
        texts = [t.strip() for t in texts if t and t.strip()]
    except Exception as e:
        texts = ["__ERR__ %s" % e]
    done[f] = texts
    if i % 10 == 0 or i == len(todo):
        json.dump(done, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        elapsed = time.time() - t0
        line = "%d/%d %s %s (%.1fs)\n" % (i, len(todo), f, texts[:6], elapsed)
        open(LOG, "a", encoding="utf-8").write(line)
        print(line.strip(), flush=True)

json.dump(done, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("finished", len(done), "in", time.time() - t0, flush=True)
