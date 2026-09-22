# -*- coding: utf-8 -*-
"""Set a facility up for photograph selection.

Prints the entry the report carries for the facility - the frames have to
evidence that entry, not a general impression of the site - then lays the whole
gallery out as numbered contact sheets.

    python tmp/pick.py <tag-fragment> [...]
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tmp"))

import report_notes                                            # noqa: E402
import report_photos                                           # noqa: E402
import sheet as S                                              # noqa: E402


def run(fragment):
    hits = [(t, d) for t, d in S.facilities() if fragment.lower() in t.lower()]
    if not hits:
        print("no facility matches", fragment)
        return
    os.makedirs(S.OUT, exist_ok=True)
    for tag, directory in hits:
        note = report_notes.NOTES.get(tag, "(no entry written)")
        print("\n" + "=" * 78)
        print(tag)
        print("-" * 78)
        print(note)
        held = report_photos.PHOTOS.get(tag, [])
        if held:
            print("- currently embedded:")
            for fn, cap in held:
                print("    %-70s %s" % (fn, cap))
        names = S.candidates(directory)
        if not names:
            names = S.candidates(directory, keep_all=True)
            print("- nothing survived the paperwork filter; showing all")
        print("- %d candidate frames" % len(names))
        per = 24
        pages = (len(names) + per - 1) // per
        for page in range(1, pages + 1):
            block = names[(page - 1) * per:page * per]
            path = os.path.join(S.OUT, "%s__%d.png" % (tag, page))
            S.sheet(tag, directory, block, page).save(path)
            print("  SHEET %s" % path)
        for i, name in enumerate(names, start=1):
            print("  %3d  %s" % (i, name))


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        run(arg)
