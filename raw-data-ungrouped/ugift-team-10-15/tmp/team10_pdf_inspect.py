# -*- coding: utf-8 -*-
import os
from pathlib import Path

try:
    import fitz
except ImportError:
    print("no fitz")
    fitz = None

out = Path(r"d:\coding\apps\ugift\tmp\team10-pdf-pages")
out.mkdir(parents=True, exist_ok=True)
src = Path(r"d:\coding\apps\ugift\tmp\team10-wa")

pdfs = sorted(src.glob("*.pdf"))
for pdf in pdfs:
    print("=" * 70)
    print(pdf.name, pdf.stat().st_size)
    if fitz is None:
        continue
    doc = fitz.open(pdf)
    print("pages:", doc.page_count)
    for i, page in enumerate(doc, 1):
        text = page.get_text("text") or ""
        print(f"--- page {i} text chars {len(text)} ---")
        print(text[:2500])
        if i <= 3:
            pix = page.get_pixmap(matrix=fitz.Matrix(1.4, 1.4), alpha=False)
            dest = out / ("%s-p%d.png" % (pdf.stem[:40].replace(" ", "_"), i))
            pix.save(str(dest))
            print("wrote", dest.name, pix.width, pix.height)
    doc.close()
