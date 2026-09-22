"""Re-render key toolkit pages at higher resolution."""
from pathlib import Path
import fitz

src = Path(r"d:\coding\apps\ugift\tmp\team13-wa-later")
out = Path(r"d:\coding\apps\ugift\tmp\toolkit-hires")
out.mkdir(parents=True, exist_ok=True)

jobs = [
    ("Mukoto seed secondary school namisindwa .pdf", "mukoto"),
    ("Namboko seed secondary school namisindwa.pdf", "namboko"),
]
for name, stem in jobs:
    doc = fitz.open(src / name)
    print(name, doc.page_count)
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=fitz.Matrix(2.8, 2.8), alpha=False)
        dest = out / f"{stem}-p{i:02d}.png"
        pix.save(str(dest))
        print(" ", dest.name, pix.width, pix.height)
    doc.close()
