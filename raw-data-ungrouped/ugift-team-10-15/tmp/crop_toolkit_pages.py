"""Crop toolkit pages into horizontal bands for closer reading."""
from pathlib import Path
from PIL import Image

root = Path(r"d:\coding\apps\ugift\tmp\team13-pdf-pages-later")
out = Path(r"d:\coding\apps\ugift\tmp\toolkit-crops")
out.mkdir(exist_ok=True)

# Crop each page into header + 6 overlapping bands.
PAGES = [
    "Mukoto-seed-secondary-school-namisindwa",
    "Namboko-seed-secondary-school-namisindwa",
]

for prefix in PAGES:
    for i in range(1, 12):
        p = root / f"{prefix}-p{i:02d}.png"
        img = Image.open(p)
        w, h = img.size
        # header
        img.crop((0, 0, w, int(h * 0.18))).save(out / f"{prefix}-p{i:02d}-h.png")
        # 5 overlapping body bands
        for b, (y0, y1) in enumerate([
            (0.12, 0.38),
            (0.30, 0.56),
            (0.48, 0.74),
            (0.66, 0.92),
            (0.82, 1.00),
        ]):
            img.crop((0, int(h * y0), w, int(h * y1))).save(
                out / f"{prefix}-p{i:02d}-b{b}.png"
            )
        print(prefix, i, w, h)
