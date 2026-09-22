# -*- coding: utf-8 -*-
"""Contact sheets of the frames no team described, for reading by eye."""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, "src")
import gallery_index as gi  # noqa: E402

OUT = "tmp/gallery/sheets"
CELL = 330
COLS = 4
ROWS = 4
PAD = 22


def font(size=16):
    for name in ("arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    teams, _measured = gi.build(verbose=False)
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    for facility in gi.all_facilities(teams):
        blank = [f for f in facility.kept if not f.description]
        if not blank:
            continue
        key = "%s__%s" % (facility.lg_folder.replace(" ", "-"), facility.folder)
        manifest[key] = [f.rel for f in blank]
        per = COLS * ROWS
        for start in range(0, len(blank), per):
            chunk = blank[start:start + per]
            rows = (len(chunk) + COLS - 1) // COLS
            sheet = Image.new(
                "RGB", (COLS * (CELL + PAD) + PAD,
                        rows * (CELL + PAD + 20) + PAD + 26), "white")
            draw = ImageDraw.Draw(sheet)
            draw.text((PAD, 6), "%s  |  frames %d-%d"
                      % (key, start, start + len(chunk) - 1),
                      fill="black", font=font(17))
            for i, frame in enumerate(chunk):
                col, row = i % COLS, i // COLS
                x = PAD + col * (CELL + PAD)
                y = 30 + row * (CELL + PAD + 20)
                draw.text((x, y), "[%d]" % (start + i), fill="black",
                          font=font(17))
                with Image.open(frame.path) as im:
                    im = ImageOps.exif_transpose(im).convert("RGB")
                    im.thumbnail((CELL, CELL))
                    sheet.paste(im, (x, y + 20))
            sheet.save("%s/%s_%03d.png" % (OUT, key, start))
    with open("tmp/gallery/sheets/manifest.json", "w") as fh:
        json.dump(manifest, fh, indent=1)
    for key, rels in manifest.items():
        print("%-60s %d" % (key, len(rels)))


if __name__ == "__main__":
    main()
