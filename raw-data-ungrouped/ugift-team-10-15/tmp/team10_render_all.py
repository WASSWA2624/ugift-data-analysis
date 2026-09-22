# -*- coding: utf-8 -*-
import os
from pathlib import Path
import fitz

src = Path(r"d:\coding\apps\ugift\tmp\team10-wa")
out = Path(r"d:\coding\apps\ugift\tmp\team10-pdf-pages")
out.mkdir(parents=True, exist_ok=True)

for pdf in sorted(src.glob("*.pdf")):
    if pdf.name.lower().startswith("lopei"):
        continue
    stem = pdf.stem.replace(" ", "_").replace(".", "")[:36]
    doc = fitz.open(pdf)
    print(pdf.name, "pages", doc.page_count)
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
        dest = out / ("%s-p%02d.png" % (stem, i))
        pix.save(str(dest))
        print(" ", dest.name, pix.width, pix.height)
    doc.close()
