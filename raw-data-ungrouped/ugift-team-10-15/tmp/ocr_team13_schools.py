"""OCR Mukoto and Namboko toolkit pages for transcription."""
from pathlib import Path
import sys

try:
    import pytesseract
    from PIL import Image
except ImportError:
    print("MISSING", file=sys.stderr)
    sys.exit(1)

root = Path(r"d:\coding\apps\ugift\tmp\team13-pdf-pages-later")
out = Path(r"d:\coding\apps\ugift\tmp\ocr_team13_schools")
out.mkdir(exist_ok=True)

for prefix in (
    "Mukoto-seed-secondary-school-namisindwa",
    "Namboko-seed-secondary-school-namisindwa",
):
    for i in range(1, 12):
        p = root / f"{prefix}-p{i:02d}.png"
        if not p.exists():
            print("missing", p)
            continue
        img = Image.open(p)
        # upscale a bit for handwriting
        img2 = img.resize((img.width * 2, img.height * 2))
        text = pytesseract.image_to_string(img2)
        dest = out / f"{prefix}-p{i:02d}.txt"
        dest.write_text(text, encoding="utf-8")
        print("wrote", dest.name, "chars", len(text))
