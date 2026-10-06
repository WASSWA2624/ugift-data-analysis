"""Create internal QA overviews and a page-text inventory from rendered PDF."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    pages = sorted(args.directory.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
    out = args.directory / "contact-sheets"
    out.mkdir(exist_ok=True)
    for start in range(0, len(pages), 12):
        group = pages[start:start + 12]
        canvas = Image.new("RGB", (1800, 1640), "#DDDDDD")
        draw = ImageDraw.Draw(canvas)
        for i, path in enumerate(group):
            with Image.open(path) as image:
                thumb = ImageOps.contain(image.convert("RGB"), (434, 510))
            x = (i % 4) * 450 + (450 - thumb.width) // 2
            y = (i // 4) * 545 + 26
            canvas.paste(thumb, (x, y))
            draw.text(((i % 4) * 450 + 12, (i // 4) * 545 + 8), path.stem, fill="#000000")
        canvas.save(out / f"pages-{start + 1}-{start + len(group)}.jpg", quality=90)
    pdfs = list(args.directory.glob("*.pdf"))
    if pdfs:
        reader = PdfReader(pdfs[0])
        inventory = []
        for index, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            inventory.append({"page": index, "width_points": float(page.mediabox.width),
                              "height_points": float(page.mediabox.height), "text": text,
                              "image_count": len(page.images)})
        (args.directory / "page-inventory.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf8")
    print(f"Contact sheets generated for {len(pages)} pages")

if __name__ == "__main__":
    main()
