"""Mine informant / received-by strings from team report Python modules."""
from __future__ import annotations

import ast
import re
from pathlib import Path

SRC = Path("src")
PHONE = re.compile(r"0[7]\d{8}")
ROLEY = re.compile(
    r"head\s*teacher|deputy|in[-\s]?charge|incharge|DOS|CAO|Town Clerk|"
    r"DEO|DHO|CFO|Education Officer|Health Officer|informant|Received by|"
    r"person in charge|acting",
    re.I,
)

files = sorted(SRC.glob("team1[0-5]*.py")) + sorted((SRC / "team15_data").glob("*.py"))
files = [p for p in files if p.is_file()]
files = sorted(set(files))

print(f"Scanning {len(files)} files\n")

for path in files:
    text = path.read_text(encoding="utf-8", errors="replace")
    # string literals that look like people contacts
    for m in re.finditer(r"""(['"])(.*?)\1""", text, re.S):
        s = m.group(2)
        if "\n" in s and len(s) > 200:
            continue
        s1 = " ".join(s.split())
        if len(s1) < 8 or len(s1) > 220:
            continue
        has_phone = bool(PHONE.search(s1))
        has_role = bool(ROLEY.search(s1))
        has_name = bool(re.search(r"\b(Mr\.?|Ms\.?|Mrs\.?|Miss|Dr\.?)\b|[A-Z][a-z]+ [A-Z][a-z]+", s1))
        if has_phone and (has_role or has_name):
            print(f"{path.name}: {s1}")
        elif has_role and has_name and re.search(
            r"Received by|Informant|INFORMANT|Incharge:|head teacher|in-charge|deputy head|DOS,",
            s1,
            re.I,
        ):
            # named leaders without phone
            if re.search(r"who is not named|not named|Nobody|None\.|not recorded", s1, re.I):
                continue
            print(f"{path.name}: {s1}")
