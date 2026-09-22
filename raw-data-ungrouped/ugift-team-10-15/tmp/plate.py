# -*- coding: utf-8 -*-
"""How a facility's chosen frames will lay out: lines, heights, and fill.

    python tmp/plate.py                 every facility in report_photos
    python tmp/plate.py <tag-fragment>  one facility, line by line
"""
from __future__ import annotations

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

SRC = io.open(os.path.join(ROOT, "src", "build_consolidated_final_report.py"),
              encoding="utf-8").read().split("if __name__")[0]
B = {}
exec(compile(SRC, "builder", "exec"), B)

import json                                                    # noqa: E402

import report_photos                                           # noqa: E402
from PIL import Image, ImageOps                                # noqa: E402

STORE = os.path.join(ROOT, "tmp", "chosen.json")
# While selection is under way the working record is the authority; anything
# not yet re-chosen falls back to what the report already carries.
SETS = dict(report_photos.PHOTOS)
if os.path.exists(STORE):
    SETS.update({k: [tuple(v) for v in vs]
                 for k, vs in json.load(io.open(STORE, encoding="utf-8")).items()})

CAPTION_IN = 0.20            # one line of 8 pt caption plus its lead


def aspects_for(tag):
    team, lg, folder = tag.split("_", 2)
    directory = os.path.join(ROOT, "facility-registers", "team-" + team[1:],
                             lg, folder)
    out = []
    for filename, _caption in SETS[tag]:
        with Image.open(os.path.join(directory, filename)) as im:
            im = ImageOps.exif_transpose(im)
            out.append(im.width / float(im.height))
    return out


def plate(tag, verbose=False):
    aspects = aspects_for(tag)
    if not aspects:
        return None
    rows = B["plan_plate"](aspects)
    worst, total_h = 1.0, 0.0
    for row in rows:
        raw = B["row_height"]([aspects[i] for i in row])
        height = B["drawn_height"]([aspects[i] for i in row])
        used = sum(aspects[i] * height for i in row) + len(row) * B["GUTTER_IN"]
        fill = used / B["PLATE_W_IN"]
        worst = min(worst, fill)
        total_h += height + CAPTION_IN
        if verbose:
            print("    line of %d  h=%.2f in  fill=%3d%%   %s"
                  % (len(row), height, round(fill * 100),
                     " ".join("%.2f" % aspects[i] for i in row)))
    return worst, total_h, len(aspects), len(rows)


def main():
    fragment = sys.argv[1] if len(sys.argv) > 1 else ""
    rows = []
    for tag in sorted(SETS):
        if fragment and fragment.lower() not in tag.lower():
            continue
        if fragment:
            print(tag)
        result = plate(tag, verbose=bool(fragment))
        if result:
            rows.append((result[0], result[1], result[2], result[3], tag))
    if fragment:
        return
    rows.sort()
    print("%-58s %5s %5s %6s %5s" % ("facility", "n", "lines", "height",
                                     "fill"))
    for fill, height, count, lines, tag in rows:
        flag = "  <-- thin" if fill < 0.90 else (
            "  <-- tall" if height > 6.2 else "")
        print("%-58s %5d %5d %5.1f\" %4d%%%s"
              % (tag, count, lines, height, round(fill * 100), flag))
    print("\n%d facilities, %d photographs, %d thin, %d tall"
          % (len(rows), sum(r[2] for r in rows),
             sum(1 for r in rows if r[0] < 0.90),
             sum(1 for r in rows if r[1] > 6.2)))


if __name__ == "__main__":
    main()
