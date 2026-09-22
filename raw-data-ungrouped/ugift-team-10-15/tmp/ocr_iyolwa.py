from easyocr import Reader
from pathlib import Path
import json

r = Reader(["en"], gpu=False)
src = Path(r"d:\coding\apps\ugift\tmp\team13-pdf-pages-later")
out = Path(r"d:\coding\apps\ugift\tmp\team13-iyolwa-ocr")
out.mkdir(parents=True, exist_ok=True)

for i in range(1, 14):
    name = f"Iyolwa-seed-school-p{i:02d}.png"
    p = src / name
    print("OCR", name, flush=True)
    res = r.readtext(str(p), detail=1, paragraph=False)
    lines = []
    for box, text, conf in res:
        ys = [pt[1] for pt in box]
        xs = [pt[0] for pt in box]
        lines.append(
            {
                "t": text,
                "c": round(float(conf), 2),
                "x": int(min(xs)),
                "y": int(min(ys)),
                "x2": int(max(xs)),
                "y2": int(max(ys)),
            }
        )
    lines.sort(key=lambda d: (d["y"] // 15, d["x"]))
    (out / f"p{i:02d}.json").write_text(json.dumps(lines, indent=1), encoding="utf-8")
    txt = [f"{d['y']:4d},{d['x']:4d} {d['c']:.2f} {d['t']}" for d in lines]
    (out / f"p{i:02d}.txt").write_text("\n".join(txt), encoding="utf-8")
    print("  n=", len(lines), flush=True)

print("done")
