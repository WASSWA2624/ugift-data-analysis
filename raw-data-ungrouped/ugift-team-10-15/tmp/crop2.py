"""Tighter crops of serial/status regions."""
from pathlib import Path
from PIL import Image

root = Path(r"d:\coding\apps\ugift\tmp\team13-pdf-pages-later")
out = Path(r"d:\coding\apps\ugift\tmp\toolkit-crops")

def save(img, name, box):
    img.crop(box).save(out / name)

# Mukoto p04 ICT left - serials are in middle columns
p = Image.open(root / "Mukoto-seed-secondary-school-namisindwa-p04.png")
w, h = p.size
save(p, "mk-p04-head.png", (0, 0, w, int(h * 0.22)))
save(p, "mk-p04-desk.png", (0, int(h * 0.18), w, int(h * 0.42)))
save(p, "mk-p04-proj-ups.png", (0, int(h * 0.32), w, int(h * 0.62)))
save(p, "mk-p04-ups-srv.png", (0, int(h * 0.45), w, int(h * 0.72)))
save(p, "mk-p04-cctv-air.png", (0, int(h * 0.58), w, int(h * 0.88)))
save(p, "mk-p04-note.png", (0, int(h * 0.78), w, h))
# left margin quantities
save(p, "mk-p04-margin.png", (0, int(h * 0.18), int(w * 0.18), int(h * 0.90)))

p = Image.open(root / "Mukoto-seed-secondary-school-namisindwa-p05.png")
w, h = p.size
save(p, "mk-p05-head.png", (0, 0, w, int(h * 0.18)))
save(p, "mk-p05-r1.png", (int(w * 0.45), int(h * 0.12), w, int(h * 0.40)))
save(p, "mk-p05-r2.png", (int(w * 0.45), int(h * 0.32), w, int(h * 0.58)))
save(p, "mk-p05-r3.png", (int(w * 0.45), int(h * 0.50), w, int(h * 0.78)))
save(p, "mk-p05-r4.png", (int(w * 0.45), int(h * 0.70), w, h))

p = Image.open(root / "Mukoto-seed-secondary-school-namisindwa-p06.png")
w, h = p.size
save(p, "mk-p06-all.png", (0, 0, w, h))
save(p, "mk-p06-top.png", (0, 0, w, int(h * 0.55)))
save(p, "mk-p06-bot.png", (0, int(h * 0.40), w, h))

p = Image.open(root / "Mukoto-seed-secondary-school-namisindwa-p07.png")
w, h = p.size
save(p, "mk-p07-left.png", (0, 0, int(w * 0.55), h))
save(p, "mk-p07-right.png", (int(w * 0.45), 0, w, h))

print("ok mukoto ict")
