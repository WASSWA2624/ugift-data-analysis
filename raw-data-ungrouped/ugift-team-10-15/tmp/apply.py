# -*- coding: utf-8 -*-
"""Record a facility's chosen frames by their contact-sheet numbers.

The numbers are the ones printed on the sheet, so a choice made by eye is
written down without retyping a file name and getting it wrong.

    python tmp/apply.py selections.json

The file is a list of {"tag": ..., "picks": [[number, "caption"], ...]}.
Writing goes through `src/report_photos.py`, which stays the single record of
what the report embeds.
"""
from __future__ import annotations

import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tmp"))

import sheet as S                                              # noqa: E402

STORE = os.path.join(ROOT, "tmp", "chosen.json")


def load():
    if os.path.exists(STORE):
        return json.load(io.open(STORE, encoding="utf-8"))
    return {}


def main(path):
    directories = dict(S.facilities())
    chosen = load()
    for entry in json.load(io.open(path, encoding="utf-8")):
        tag = entry["tag"]
        if tag not in directories:
            raise SystemExit("unknown facility: %s" % tag)
        names = S.candidates(directories[tag]) or \
            S.candidates(directories[tag], keep_all=True)
        picks = []
        for number, caption in entry["picks"]:
            if not 1 <= number <= len(names):
                raise SystemExit("%s: frame %d is off the sheet (%d frames)"
                                 % (tag, number, len(names)))
            picks.append([names[number - 1], caption])
        files = [p[0] for p in picks]
        if len(set(files)) != len(files):
            raise SystemExit("%s: the same frame twice" % tag)
        caps = [p[1].strip().lower() for p in picks]
        if len(set(caps)) != len(caps):
            raise SystemExit("%s: the same caption twice" % tag)
        chosen[tag] = picks
        print("%-58s %d frames" % (tag, len(picks)))
    json.dump(chosen, io.open(STORE, "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print("recorded %d facilities in %s" % (len(chosen), STORE))


if __name__ == "__main__":
    main(sys.argv[1])
