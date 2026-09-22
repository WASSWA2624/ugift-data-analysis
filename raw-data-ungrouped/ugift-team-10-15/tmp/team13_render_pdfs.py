# -*- coding: utf-8 -*-
"""Render new Team 13 hand-filled toolkit PDFs to PNG pages."""
from pathlib import Path
import fitz

src = Path(r"d:\coding\apps\ugift\tmp\team13-wa-later")
out = Path(r"d:\coding\apps\ugift\tmp\team13-pdf-pages-later")
out.mkdir(parents=True, exist_ok=True)

pdfs = [
    "Iyolwa seed school .pdf",
    "Kamuli health centre 111.pdf",
    "Sop sop health centre 111 tororo.pdf",
    "Mukoto seed secondary school namisindwa .pdf",
    "Namboko seed secondary school namisindwa.pdf",
]
for name in pdfs:
    pdf = src / name
    stem = (
        name.replace(" .pdf", "")
        .replace(".pdf", "")
        .strip()
        .replace(" ", "-")
        .replace(".", "")
    )
    doc = fitz.open(pdf)
    print(name, "pages", doc.page_count, "size", pdf.stat().st_size)
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False)
        dest = out / ("%s-p%02d.png" % (stem, i))
        pix.save(str(dest))
        print(" ", dest.name, pix.width, pix.height)
    doc.close()
