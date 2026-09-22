# -*- coding: utf-8 -*-
"""Contact sheets for choosing the field report's photographs.

Lays a facility's gallery out as a numbered grid so every frame is looked at
before it is used. Paperwork, people and working files are dropped first,
because none of them can appear in the report anyway.

    python tmp/sheet.py <tag-fragment> [...]
    python tmp/sheet.py --list
"""
from __future__ import annotations

import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

REG = os.path.join(ROOT, "facility-registers")
OUT = os.path.join(ROOT, "tmp", "sheets")
EXT = {".jpg", ".jpeg", ".png"}

# Paperwork is evidence, but it is not illustration; people are not published.
DROP = re.compile(
    r"hand-filled|toolkit|check-?list|discussion-guide|"
    r"asset-register|register-(page|sheet|book|extract|entry|entries|line)|"
    r"-register\b|^register|delivery-note|delivery-slip|goods-received|"
    r"inventory|visitor|log-?book|receipt|invoice|price-schedule|"
    r"schedule-page|ifms|minutes|letter|memo|report-page|form\b|"
    r"handover|hand-over-(note|certificate)|certificate|"
    r"member|team-|colleague|supervisor|head-?teacher|headteacher|"
    r"in-?charge-(?!office)|staff-member|nurse|midwife|learner|pupil|student|"
    r"people|interview|group-photo|selfie|vehicle|car-|driver|"
    r"^_z_|_z_",
    re.I,
)


def tag_of(team, lg, folder):
    return "%s_%s_%s" % (team.replace("team-", "t"), lg, folder)


def facilities():
    out = []
    for team in sorted(os.listdir(REG)):
        td = os.path.join(REG, team)
        if not team.startswith("team-") or not os.path.isdir(td):
            continue
        for lg in sorted(os.listdir(td)):
            ld = os.path.join(td, lg)
            if not os.path.isdir(ld) or lg.startswith("_"):
                continue
            for folder in sorted(os.listdir(ld)):
                fd = os.path.join(ld, folder)
                if os.path.isdir(fd) and not folder.startswith("_"):
                    out.append((tag_of(team, lg, folder), fd))
    return out


def candidates(directory, keep_all=False):
    names = sorted(f for f in os.listdir(directory)
                   if os.path.splitext(f)[1].lower() in EXT)
    if keep_all:
        return names
    return [f for f in names if not DROP.search(f)]


def label_of(filename):
    stem = os.path.splitext(filename)[0]
    stem = re.sub(r"_ref.*$", "", stem)
    stem = re.sub(r"^\d+_", "", stem)
    return stem.replace("-", " ")


def shape_of(directory, name):
    """P tall, L wide, S square - and how far from square, in tenths."""
    try:
        with Image.open(os.path.join(directory, name)) as im:
            im = ImageOps.exif_transpose(im)
            a = im.width / float(im.height)
    except Exception:
        return "?"
    return "%.2f" % a


def sheet(tag, directory, names, page, tile=290, cols=6, rows=4):
    font = ImageFont.load_default()
    pad, cap_h = 8, 26
    cell_w, cell_h = tile + pad, tile + cap_h + pad
    canvas = Image.new("RGB", (cols * cell_w + pad, rows * cell_h + pad + 22),
                       "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((pad, 6), "%s   sheet %d" % (tag, page), fill="black", font=font)
    for i, name in enumerate(names):
        r, c = divmod(i, cols)
        x, y = pad + c * cell_w, 22 + pad + r * cell_h
        try:
            with Image.open(os.path.join(directory, name)) as im:
                im = ImageOps.exif_transpose(im).convert("RGB")
                im.thumbnail((tile, tile), Image.Resampling.LANCZOS)
                off = ((tile - im.width) // 2, (tile - im.height) // 2)
                canvas.paste(im, (x + off[0], y + off[1]))
        except Exception as exc:                       # unreadable frame
            draw.text((x + 4, y + 4), "unreadable\n%s" % exc, fill="red",
                      font=font)
        draw.rectangle([x, y, x + tile, y + tile], outline="#cccccc")
        draw.rectangle([x, y, x + 34, y + 18], fill="#1f3a5f")
        draw.text((x + 6, y + 5), "%d" % (i + 1 + (page - 1) * cols * rows),
                  fill="white", font=font)
        # The shape of the frame, because a line of frames is only balanced
        # when the shapes on it add up to the width of the column.
        draw.rectangle([x + tile - 42, y, x + tile, y + 18], fill="#7a5230")
        draw.text((x + tile - 38, y + 5), shape_of(directory, name),
                  fill="white", font=font)
        text = label_of(name)[:46]
        draw.text((x + 2, y + tile + 5), text, fill="#333333", font=font)
    return canvas


def run(fragment):
    hits = [(t, d) for t, d in facilities() if fragment.lower() in t.lower()]
    if not hits:
        print("no facility matches", fragment)
        return
    os.makedirs(OUT, exist_ok=True)
    for tag, directory in hits:
        names = candidates(directory)
        if not names:
            names = candidates(directory, keep_all=True)
            note = " (nothing survived the filter; showing everything)"
        else:
            note = ""
        print("\n== %s   %d candidate frames%s" % (tag, len(names), note))
        per = 24
        for page in range(1, (len(names) + per - 1) // per + 1):
            block = names[(page - 1) * per:page * per]
            img = sheet(tag, directory, block, page)
            path = os.path.join(OUT, "%s__%d.png" % (tag, page))
            img.save(path)
            print("   ", path)
        for i, name in enumerate(names, start=1):
            print("   %3d  %s" % (i, name))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        for tag, directory in facilities():
            print(len(candidates(directory)), tag)
    else:
        for arg in sys.argv[1:]:
            run(arg)
