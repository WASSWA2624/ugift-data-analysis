"""Crop high-res pages into readable bands."""
from pathlib import Path
from PIL import Image

hi = Path(r"d:\coding\apps\ugift\tmp\toolkit-hires")
out = Path(r"d:\coding\apps\ugift\tmp\hires-bands")
out.mkdir(exist_ok=True)

def do(stem, n, parts=5):
    img = Image.open(hi / f"{stem}-p{n:02d}.png")
    w, h = img.size
    img.crop((0, 0, w, int(h * 0.14))).save(out / f"{stem}-p{n:02d}-h.png")
    step = 0.20
    overlap = 0.04
    y = 0.10
    i = 0
    while y < 0.98:
        y1 = min(1.0, y + step + overlap)
        img.crop((0, int(h * y), w, int(h * y1))).save(out / f"{stem}-p{n:02d}-b{i}.png")
        y += step
        i += 1
    print(stem, n, w, h, "bands", i)

for stem, pages in (("mukoto", range(1, 12)), ("namboko", range(1, 12))):
    for n in pages:
        do(stem, n)
