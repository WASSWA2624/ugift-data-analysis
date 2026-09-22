"""Tighter crops: Mukoto buildings + Namboko all."""
from pathlib import Path
from PIL import Image

root = Path(r"d:\coding\apps\ugift\tmp\team13-pdf-pages-later")
out = Path(r"d:\coding\apps\ugift\tmp\toolkit-crops")

def bands(stem, dest_prefix, extra=None):
    img = Image.open(root / f"{stem}.png")
    w, h = img.size
    img.crop((0, 0, w, int(h * 0.16))).save(out / f"{dest_prefix}-h.png")
    slices = [
        (0.12, 0.36),
        (0.28, 0.52),
        (0.44, 0.68),
        (0.60, 0.84),
        (0.76, 1.00),
    ]
    for i, (a, b) in enumerate(slices):
        img.crop((0, int(h * a), w, int(h * b))).save(out / f"{dest_prefix}-s{i}.png")
    if extra:
        extra(img, w, h)

# Mukoto buildings p08-p11
for n in range(8, 12):
    bands(f"Mukoto-seed-secondary-school-namisindwa-p{n:02d}", f"mk-p{n:02d}")

# Mukoto p06 item column
img = Image.open(root / "Mukoto-seed-secondary-school-namisindwa-p06.png")
w, h = img.size
img.crop((0, int(h * 0.10), int(w * 0.55), int(h * 0.70))).save(out / "mk-p06-items.png")
img.crop((int(w * 0.35), int(h * 0.10), w, int(h * 0.70))).save(out / "mk-p06-rest.png")

# Namboko all
for n in range(1, 12):
    bands(f"Namboko-seed-secondary-school-namisindwa-p{n:02d}", f"nb-p{n:02d}")

print("done")
