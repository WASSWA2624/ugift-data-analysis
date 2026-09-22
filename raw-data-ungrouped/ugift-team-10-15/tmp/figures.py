# -*- coding: utf-8 -*-
"""Rewrite the report's spelled-out quantities as figures.

A field report reads as one when its counts are figures: `67 of the 76
register lines`, not `Sixty-seven of the seventy-six`. The rule applied here
is figures from two upwards; `one` stays a word, because in English it is as
often an article as a count (`the one facility`, `not one carton was opened`,
`one of the 7 wall clocks`), and a sentence never opens on a digit - the
handful that did are recast by hand in RECASTS below.

Works on the source through the syntax tree, so only the strings the report
prints are touched: docstrings, comments and code are left exactly as they
are.

    python tmp/figures.py            report what would change
    python tmp/figures.py --write    apply it
"""
from __future__ import annotations

import ast
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# Sentences that opened on a number word, recast so they open on a word.
# Keyed by facility so a phrase cannot match somewhere it was not meant to.
# --------------------------------------------------------------------------

RECASTS = {
    "t10_Amudat_Looro-Seed-Secondary-School": [
        ("Eleven blocks stand in the compound, from",
         "The compound holds eleven blocks, from"),
    ],
    "t10_Nabilatuk_Lolachat-Seed-School": [
        ("Thirteen blocks stand in the compound, including",
         "The compound holds thirteen blocks, including"),
    ],
    "t11_Abim_Alerek-Seed-Secondary-School": [
        ("Six of the eleven ICT lines are still in their cartons, the",
         "Of the eleven ICT lines, six are still in their cartons, the"),
    ],
    "t12_Kibuku_St-Johns-Seed-Secondary-School-Kirika": [
        ("Fifteen CPUs and eight monitors are recorded stolen and the case",
         "The school records fifteen CPUs and eight monitors stolen and the "
         "case"),
    ],
    "t12_Kibuku_Lwatama-HC-III": [
        ("Two different marks are cut into the assets and they belong",
         "The assets carry two different marks and they belong"),
    ],
    "t12_Budaka_Mugiti-Seed-Secondary-School": [
        ("Three socket boxes stand with their covers off",
         "On the outside, three socket boxes stand with their covers off"),
    ],
    "t12_Mbale_Lwasso-Seed-Secondary-School": [
        ("Twenty Dell CPUs and the lightning conductors are recorded stolen,",
         "The school records twenty Dell CPUs and the lightning conductors "
         "stolen,"),
    ],
    "t13_Busia_Buwembe-HC-III": [
        ("Seven assets are cut with the facility's own name and none with a "
         "number;",
         "The facility's own name is cut into seven assets and none carries a "
         "number;"),
    ],
    "t13_Namisindwa_Namboko": [
        ("Seventeen chairs, two laboratory stools and some ICT lines are "
         "marked non-functional or stolen;",
         "The register marks seventeen chairs, two laboratory stools and some "
         "ICT lines non-functional or stolen;"),
    ],
    "t13_Manafwa_Sibanga-Seed-School": [
        ("Ten monitors and twenty processors are recorded stolen,",
         "The school records ten monitors and twenty processors stolen,"),
    ],
    "t14_Bududa_Nakatsi-Seed-Secondary-School": [
        ("Six classroom rooms on two blocks were said to be too few, and "
         "twenty-one computers too few for a hundred senior-one learners.",
         "The six classroom rooms on two blocks were said to be too few, and "
         "the twenty-one computers too few for a hundred senior-one "
         "learners."),
    ],
    "t14_Sironko_Buyobo-HC-III": [
        ("Sixty-seven of the seventy-six register lines carry a status,",
         "Of the seventy-six register lines, sixty-seven carry a status,"),
    ],
    "t15_Bukwo_Chepkwasta-HC-III": [
        ("Fifteen classes of equipment are engraved here, from",
         "Engraving here covers fifteen classes of equipment, from"),
        ("Five more classes carry no mark at all.",
         "A further five classes carry no mark at all."),
    ],
    "t15_Bukwo_Brim-HC-III": [
        ("Eight classes of asset are engraved, including the autoclave, "
         "microscope, height meter and patient beds, and five are not.",
         "Engraving covers eight classes of asset, including the autoclave, "
         "microscope, height meter and patient beds, and five are not "
         "marked."),
    ],
    "t15_Bukwo_Tulel-HC-III": [
        ("Fourteen classes of asset are recorded not engraved and none is "
         "recorded engraved.",
         "The register records fourteen classes of asset not engraved and "
         "none engraved."),
    ],
    "t15_Kween_Kitawoi-Seed-Secondary-School": [
        ("Three desktops are recorded spoilt and the",
         "The school records three desktops spoilt and the"),
    ],
    "t15_Kween_Moyok-HC-III": [
        ("Eight classes of asset are engraved KWN/MED EQ/MOYOK HCIII, "
         "including the patient beds, refrigerator and lockable cupboard, and "
         "five are not.",
         "Engraving covers eight classes of asset marked KWN/MED EQ/MOYOK "
         "HCIII, including the patient beds, refrigerator and lockable "
         "cupboard, and five are not marked."),
    ],
    "t15_Kween_Kaptum-HC-III": [
        ("Four classes of asset are recorded not engraved, and the",
         "The register records four classes of asset not engraved, and the"),
    ],
    "t15_Kween_Terenpoy-HC-III": [
        ("Of forty-five items with a usage recorded,",
         "Of the forty-five items with a usage recorded,"),
        ("Three classes are recorded not engraved and the",
         "The register records three classes not engraved and the"),
    ],
    "t15_Kween_Atar-HC-III": [
        ("Four wheelchairs stand stacked and unused,",
         "The four wheelchairs stand stacked and unused,"),
    ],
    "t15_Kapchorwa_Kabeywa-Seed-Secondary-School": [
        ("Twenty-three of the school's uninterruptible power supplies are "
         "reported stolen and the projector lost;",
         "The school reports twenty-three of its uninterruptible power "
         "supplies stolen and the projector lost;"),
    ],
    "t15_Kapchorwa_Kaptanya-Seed-Secondary-School": [
        ("Two other classes of asset carry no mark.",
         "A further two classes of asset carry no mark."),
    ],
    "t15_Kapchorwa_Chemosong-HC-III": [
        ("Three oxygen concentrators and much of the rest",
         "The three oxygen concentrators and much of the rest"),
    ],
}

# --------------------------------------------------------------------------
# Word to figure
# --------------------------------------------------------------------------

UNITS = {
    "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19,
}
TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90,
}
ONES = dict(UNITS, one=1)

# Scale phrases keep their scale word: `about 2 billion shillings` reads as
# money, `2,000,000,000` does not.
SCALES = [
    (re.compile(r"\bthirteen thousand\b", re.I), "13,000"),
    (re.compile(r"\btwo billion\b", re.I), "2 billion"),
    (re.compile(r"\bseven hundred million\b", re.I), "700 million"),
    (re.compile(r"\ba hundred(?= senior-one)", re.I), "100"),
]

# `one` stays a word; `three-digit` and `senior-one` are adjectives, not counts
KEEP = re.compile(r"(?:three-digit|senior-one)", re.I)

# `one` is not a number word on its own here, but it is half of `twenty-one`
_TENS_UNIT = r"(?:%s)(?:-(?:%s))?" % ("|".join(TENS), "|".join(ONES))
_NUMBER = re.compile(r"\b(%s|%s)\b" % (_TENS_UNIT, "|".join(UNITS)), re.I)


def value_of(word):
    word = word.lower()
    if "-" in word:
        tens, unit = word.split("-", 1)
        return TENS[tens] + ONES[unit]
    return TENS.get(word) or UNITS[word]


def to_figures(text):
    for pattern, replacement in SCALES:
        text = pattern.sub(replacement, text)

    out, cursor = [], 0
    for keep in KEEP.finditer(text):
        out.append(_NUMBER.sub(lambda m: str(value_of(m.group(0))),
                               text[cursor:keep.start()]))
        out.append(keep.group(0))
        cursor = keep.end()
    out.append(_NUMBER.sub(lambda m: str(value_of(m.group(0))), text[cursor:]))
    return "".join(out)


# --------------------------------------------------------------------------
# Writing a string back into the source, wrapped where it was wrapped
# --------------------------------------------------------------------------

WIDTH = 79


def literal(text, indent):
    """`text` as a Python string literal, wrapped to the source width."""
    body = text.replace("\\", "\\\\").replace('"', '\\"')
    room = WIDTH - indent - 2
    if len(body) <= room:
        return '"%s"' % body

    lines, current = [], ""
    for word in body.split(" "):
        piece = word if not current else current + " " + word
        if len(piece) > room and current:
            lines.append(current + " ")
            current = word
        else:
            current = piece
    lines.append(current)
    pad = " " * indent
    return ("\n" + pad).join('"%s"' % line for line in lines)


def rewrite(path, wanted):
    """Replace the string nodes `wanted(node, key) -> new text or None`."""
    source = io.open(path, encoding="utf-8").read()
    lines = source.split("\n")
    offsets, running = [], 0
    for line in lines:
        offsets.append(running)
        running += len(line) + 1

    def at(lineno, col):
        return offsets[lineno - 1] + col

    edits = []
    for key, node in wanted:
        new = to_figures(node.value)
        if new == node.value:
            continue
        edits.append((at(node.lineno, node.col_offset),
                      at(node.end_lineno, node.end_col_offset),
                      literal(new, node.col_offset), node.value, new))

    for start, end, text, _old, _new in sorted(edits, reverse=True):
        source = source[:start] + text + source[end:]
    return source, edits


def apply_recasts(text, key):
    for old, new in RECASTS.get(key, []):
        if old not in text:
            raise SystemExit("recast does not match %s:\n  %s" % (key, old))
        text = text.replace(old, new)
    return text


def notes_nodes(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and node.targets[0].id == "NOTES":
            for key, value in zip(node.value.keys, node.value.values):
                value.value = apply_recasts(value.value, key.value)
                yield key.value, value


def photo_nodes(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and node.targets[0].id == "PHOTOS":
            for key, frames in zip(node.value.keys, node.value.values):
                for frame in frames.elts:
                    yield key.value, frame.elts[1]


def run(write):
    total = 0
    for name, nodes in (("report_notes.py", notes_nodes),
                        ("report_photos.py", photo_nodes)):
        path = os.path.join(ROOT, "src", name)
        tree = ast.parse(io.open(path, encoding="utf-8").read())
        source, edits = rewrite(path, list(nodes(tree)))
        print("\n== %s: %d strings changed" % (name, len(edits)))
        for _s, _e, _t, old, new in edits:
            print("   - %s\n   + %s" % (old[:150], new[:150]))
        total += len(edits)
        if write:
            io.open(path, "w", encoding="utf-8", newline="\n").write(source)
    print("\n%d strings%s" % (total, " written" if write else " (dry run)"))


if __name__ == "__main__":
    run("--write" in sys.argv)
