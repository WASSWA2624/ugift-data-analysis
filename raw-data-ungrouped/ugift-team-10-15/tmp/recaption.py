# -*- coding: utf-8 -*-
"""Shorten a caption without touching the frame it belongs to.

A caption sits in a column no wider than its own frame, so a long sentence
under a narrow frame runs to four or five lines and pulls the line apart. This
rewrites the caption in both the working record and `report_photos.py`, keyed
by facility and file name so the wrong frame cannot be relabelled.

    python tmp/recaption.py captions.json

The file is a list of [tag, filename-fragment, new caption].
"""
from __future__ import annotations

import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "tmp", "chosen.json")


def main(path):
    chosen = json.load(io.open(STORE, encoding="utf-8"))
    for tag, fragment, caption in json.load(io.open(path, encoding="utf-8")):
        picks = chosen.get(tag)
        if picks is None:
            raise SystemExit("%s is not in the working record" % tag)
        hits = [p for p in picks if fragment in p[0]]
        if len(hits) != 1:
            raise SystemExit("%s: %d frames match %r" % (tag, len(hits), fragment))
        print("%-46s %-34s -> %s" % (tag[:46], hits[0][1][:34], caption))
        hits[0][1] = caption
    json.dump(chosen, io.open(STORE, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1])
