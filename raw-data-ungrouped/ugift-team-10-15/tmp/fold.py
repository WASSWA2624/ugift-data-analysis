# -*- coding: utf-8 -*-
"""Write the reviewed selections back into `src/report_photos.py`.

The working record under `tmp/chosen.json` is where a review session records
what it kept; this makes `report_photos.py` say the same thing, so the module
stays the one place the report reads its photographs from.

    python tmp/fold.py
"""
from __future__ import annotations

import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import report_photos                                           # noqa: E402

TARGET = os.path.join(ROOT, "src", "report_photos.py")
STORE = os.path.join(ROOT, "tmp", "chosen.json")

DOCSTRING = '''# -*- coding: utf-8 -*-
"""The photographs the field report embeds, and what each one shows.

Every entry here was chosen by looking at the picture, not at its file name.
Each facility's whole gallery was laid out as a numbered contact sheet and
reviewed frame by frame against that facility's own written entry, because the
frames have to evidence what the entry says - the works, the supplied assets,
and whatever is wrong with them - and not give a general impression of a site.

How many are kept is decided by the gallery and by the page, not by a quota.
A facility whose gallery carries the whole story is given up to ten frames; one
photographed twice is given two. Frames are also chosen for their shapes, since
a line of pictures only fills the text column when the shapes on it add up to
its width: a tall frame is kept beside a wide one, and a set of six 16:9 frames
is not kept when three of them would leave a line short.

File names are not reliable evidence. Some frames are captioned
`uncaptioned-asset`; some carry a caption that belongs to a different subject
(a stained ceiling filed as a signboard at Bundege HC III, a table edge filed
as a chair backrest at Nakatsi); and several folders hold frames belonging to a
neighbouring facility - school furniture and ICT under Kwirwot HC III, health
equipment under Malaba Seed School, Iyolwa desks under Sop Sop. Those were left
out, and every caption asserting an engraved mark was read off the image.

Paperwork - toolkits, registers, delivery notes, visitors' books - is evidence
but not illustration, and none of it appears here. Nor do frames of people:
faces of staff, patients and learners are kept out of a published document.
Frames stored upside down are left out rather than turned, because the file is
the evidence as it was taken.

Keyed by `<team>_<local government>_<facility folder>`, matching the register
tree under `facility-registers/`.
"""

'''


def main():
    chosen = json.load(io.open(STORE, encoding="utf-8"))
    photos = dict(report_photos.PHOTOS)
    photos.update({k: [tuple(v) for v in vs] for k, vs in chosen.items()})

    out = [DOCSTRING, "PHOTOS = {\n"]
    for tag in sorted(photos):
        out.append('    "%s": [\n' % tag)
        for filename, caption in photos[tag]:
            out.append('        ("%s",\n' % filename)
            out.append('         "%s"),\n' % caption.replace('"', '\\"'))
        out.append("    ],\n")
    out.append("}\n")
    io.open(TARGET, "w", encoding="utf-8", newline="\n").write("".join(out))
    print("%d facilities, %d photographs -> %s"
          % (len(photos), sum(len(v) for v in photos.values()), TARGET))


if __name__ == "__main__":
    main()
