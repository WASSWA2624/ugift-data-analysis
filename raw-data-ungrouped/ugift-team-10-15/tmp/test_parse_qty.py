# -*- coding: utf-8 -*-
"""Qty extraction helpers for the LG MDA status register."""
from __future__ import annotations

import re

SKIP_UNIT = re.compile(
    r"^(?:deg|degree|degrees|w|kw|v|vac|ah|ml|l|litre|litres|liter|liters|"
    r"cm|mm|m|metre|metres|meter|meters|gm|g|kg|swg|port|ports|"
    r"gen|th|inch|inches|%)$",
    re.I,
)

# Words that mean the preceding number is a count of items / structures.
COUNT_WORD = re.compile(
    r"^(?:blocks?|rooms?|stances?|bathrooms?|speakers?|sets?|pcs?|pc|"
    r"pieces?|units?|nos?|rolls?|pads?|sheets?|chairs?|desks?|tables?|"
    r"tanks?|beds?|houses?|class(?:rooms?|es)?|machines?|boxes?|"
    r"quarters?|received|written|margin|total)$",
    re.I,
)

PCS_RE = re.compile(r"(?<![A-Za-z])(\d+)\s*(?:pcs?|pc)\.?(?!\w)", re.I)
LEADING_RE = re.compile(r"^(\d+)\s+[A-Za-z]")
PAREN_RE = re.compile(r"[\(\[\{]([^\)\]\}]+)[\)\]\}]")
TRAILING_COMMA_RE = re.compile(
    r",\s*(\d+)\s*(?:blocks?|rooms?|pcs?|pc|pieces?|units?)?\s*$", re.I
)
BARE_COUNT_RE = re.compile(
    r"(?<![A-Za-z])(\d+)\s+(?:blocks?|rooms?|stances?|sets?|houses?|"
    r"classrooms?|quarters?)\b",
    re.I,
)


def _from_paren(inner: str):
    inner = (inner or "").strip()
    if not inner:
        return None

    # Bare number: (64)
    m = re.match(r"^(\d+)\s*$", inner)
    if m:
        return int(m.group(1))

    # Glued spec unit: (100W, 200W) / (12V) — not a quantity
    m = re.match(r"^(\d+)([A-Za-z]+)", inner)
    if m and SKIP_UNIT.match(m.group(2)):
        return None

    # (3 of 15)
    m = re.match(r"^(\d+)\s+of\s+\d+", inner, re.I)
    if m:
        return int(m.group(1))

    # (2 x 5,000 litres)
    m = re.match(r"^(\d+)\s*[x×]", inner, re.I)
    if m:
        return int(m.group(1))

    # (120, three seaters) / (2; Lab.) / (3 blocks / 6 classes)
    m = re.match(r"^(\d+)\s*[,;/]", inner)
    if m:
        return int(m.group(1))

    # (2 blocks) (1 roll) (28 received) (259 chairs in total)
    # (2 Ham Hb machine) (5 margin) (3 are store) (1 Height meter)
    m = re.match(r"^(\d+)\s+([A-Za-z]+)", inner)
    if m:
        n = int(m.group(1))
        word = m.group(2)
        if SKIP_UNIT.match(word):
            return None
        if COUNT_WORD.match(word):
            return n
        # soft accept: number + any word that is not a clear spec unit
        # e.g. "(2 Ham Hb machine)", "(3 are store)", "(1 Height meter)"
        if word.lower() in {
            "ham", "are", "height", "lab", "opd", "ict", "admin",
            "neonatal", "adult", "infant", "electric", "duo", "basic",
            "digital", "manual", "wall", "aneroid", "ambu", "main",
            "residential", "non",
        }:
            # "are"/"ham"/"height" after a count → treat as qty;
            # descriptive-only words without a real count sense → skip below
            if word.lower() in {"ham", "are", "height"}:
                return n
            return None
        # Default: number + unknown word → treat as quantity (field practice
        # almost always puts the count first in parentheses).
        return n

    return None


def parse_qty(item: str):
    """Best-effort quantity from an equipment / item name."""
    if not item:
        return None
    s = str(item).strip()
    if not s:
        return None

    # 1) Explicit pcs / PC — last match wins ("24 port 2pcs" → 2)
    pcs = list(PCS_RE.finditer(s))
    if pcs:
        return int(pcs[-1].group(1))

    # 2) Leading count: "251 chairs", "21 Desktop computer"
    m = LEADING_RE.match(s)
    if m:
        return int(m.group(1))

    # 3) Parentheses / brackets — first successful extract
    for m in PAREN_RE.finditer(s):
        q = _from_paren(m.group(1))
        if q is not None:
            return q

    # 4) Trailing ", N" / ", N blocks" / ", N pcs"
    m = TRAILING_COMMA_RE.search(s)
    if m:
        return int(m.group(1))

    # 5) Bare "N blocks/rooms/..." outside parentheses
    m = BARE_COUNT_RE.search(s)
    if m:
        return int(m.group(1))

    return None


if __name__ == "__main__":
    samples = [
        ("Office tables (112)", 112),
        ("251 chairs", 251),
        ("Bag Valve mask (Ambu Bag), Neonatal", None),
        ("Staff quarters (2 blocks)", 2),
        ("Red wire 50cm (1 roll)", 1),
        ("Prism (60 deg) equilateral 38mm", None),
        ("Visking tube (30 metres)", None),
        ("Solar panels (100W, 200W) monocrystalline", None),
        ("School desks (120, three seaters)", 120),
        ("Classroom blocks (6, one of them the administration block)", 6),
        ("Water tanks (2 x 5,000 litres)", 2),
        ("Toilet block (2 rooms)", 2),
        ("Public address system (2 speakers)", 2),
        ("Pit latrine blocks (5 blocks) (16 stances) (2 bathrooms)", 5),
        ("Office chairs (259 chairs in total)", 259),
        ("Desktops (28 received)", 28),
        ("Multipurpose Printer (1 pc received)", 1),
        ("Resuscitator Manual, Infant, with all Mask sizes (3 of 15)", 3),
        ("Class rooms (3 blocks / 6 classes)", 3),
        ("Haemoglobin Meter, Digital (2 Ham Hb machine)", 2),
        ("Refrigerator, Basic (2; Lab.)", 2),
        ("Autoclave 20 Liters., Duo Operated (2; 25 L and 20 L)", 2),
        ("Bowl, Kick (5; margin also 7)", 5),
        ("Diagnostic Equipment Set for OPD (2 sets)", 2),
        ("Oxygen Concentrator, Duo Flow (1; 3 boxes)", 1),
        ("B.P Machine (Aneroid wall mounted)", None),
        ("Centrifuge (Electric)", None),
        ("School desks 120pcs", 120),
        ("Chairs 226pcs.", 226),
        ("Desktop Computers 28 pcs", 28),
        ("Network Switch 24 port 2pcs", 2),
        ("Air conditioners, 1", 1),
        ("UPS, 20 pcs", 20),
        ("Non residential, 7 blocks", 7),
        ("Residential kitchen, 3", 3),
        ("Network switch 24 port", None),
        ("Constantan SWG 26", None),
        ("Autoclave 20 Liters.,Duo Operated", None),
        ("Laptops (2)", 2),
        ("Science Lab (1 block)", 1),
        ("Graph paper large (50 sheets, 1 pad)", 50),
        ("Weighing Scale with Height Meter, Adult (1 Height meter)", 1),
        ("Bed, Pediatric Patient, With Mattress (5 margin)", 5),
        ("Resuscitator Manual, Infant (3 are store)", 3),
        ("Multi Purpose Hall (main hall)", None),
        ("Pit latrines (residential)", None),
    ]
    failed = 0
    for text, expect in samples:
        got = parse_qty(text)
        ok = got == expect
        if not ok:
            failed += 1
            print("FAIL", expect, got, repr(text))
    print("failed", failed, "of", len(samples))
