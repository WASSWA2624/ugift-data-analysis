# -*- coding: utf-8 -*-
"""Contact sheets of every frame in the gallery, for the people review.

Whether a photograph is a picture of somebody, or a picture of an asset that
happens to have somebody in it, is a judgement no file name answers. So every
frame is laid out to be looked at, forty to a sheet, each numbered with its
position in the gallery order.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, "src")
import gallery_index as gi  # noqa: E402

OUT = "tmp/gallery/people"
COLS, ROWS = 8, 5
CELL = 185
PAD = 8
LABEL = 13
HEAD = 30


def font(size=13):
    for name in ("arialbd.ttf", "arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    teams, _measured = gi.build(verbose=False)
    os.makedirs(OUT, exist_ok=True)
    frames = []
    for team in teams:
        if team.records:
            for fr in team.records.kept:
                frames.append((fr, "%s team records" % team.label))
        for lg in team.local_governments:
            for facility in lg.facilities:
                where = "%s %s / %s" % (team.label, lg.folder, facility.name)
                for fr in facility.kept:
                    frames.append((fr, where))
    print("%d frames" % len(frames))

    manifest = [fr.rel for fr, _w in frames]
    with open("tmp/gallery/people/manifest.json", "w") as fh:
        json.dump(manifest, fh)

    per = COLS * ROWS
    small, big = font(12), font(15)
    for start in range(0, len(frames), per):
        chunk = frames[start:start + per]
        rows = (len(chunk) + COLS - 1) // COLS
        sheet = Image.new("RGB", (COLS * (CELL + PAD) + PAD,
                                  HEAD + rows * (CELL + LABEL + PAD)), "white")
        draw = ImageDraw.Draw(sheet)
        seen = []
        for fr, where in chunk:
            if where not in seen:
                seen.append(where)
        draw.text((PAD, 7), "[%d-%d]   %s" % (start, start + len(chunk) - 1,
                                              "  |  ".join(seen)[:190]),
                  fill="black", font=big)
        for i, (fr, _where) in enumerate(chunk):
            col, row = i % COLS, i // COLS
            x = PAD + col * (CELL + PAD)
            y = HEAD + row * (CELL + LABEL + PAD)
            draw.text((x, y), str(start + i), fill="black", font=small)
            try:
                with Image.open(fr.path) as im:
                    im = ImageOps.exif_transpose(im).convert("RGB")
                    im.thumbnail((CELL, CELL))
                    sheet.paste(im, (x, y + LABEL))
            except Exception as exc:
                draw.text((x, y + LABEL), "ERR %s" % exc, fill="red",
                          font=small)
        sheet.save("%s/sheet_%04d.png" % (OUT, start))
    print("%d sheets in %s" % (len(range(0, len(frames), per)), OUT))


if __name__ == "__main__":
    main()
