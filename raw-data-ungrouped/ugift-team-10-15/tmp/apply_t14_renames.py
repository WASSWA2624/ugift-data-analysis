# -*- coding: utf-8 -*-
"""Apply Team 14 photo renames: disk + names.py + team14_media/__init__.py."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"d:/coding/apps/ugift")
TEAM = ROOT / "facility-registers" / "team-14"
TMP = ROOT / "tmp"
NAMES_PY = ROOT / "src" / "team14_media" / "names.py"
MEDIA_INIT = ROOT / "src" / "team14_media" / "__init__.py"

# September generic names fixed from reading the photos.
SEPT = {
    TEAM / "Bududa/Bubungi-HC-III/74_circular-supply-delivery-note-page_ref20260902-0013.jpg":
        "74_circular-supply-delivery-note-11073-centrifuge-and-kangaroo-chair_ref20260902-0013.jpg",
    TEAM / "Bududa/Bubungi-HC-III/75_circular-supply-delivery-note-page-2_ref20260902-0014.jpg":
        "75_circular-supply-delivery-note-11069_ref20260902-0014.jpg",
    TEAM / "Bududa/Bubungi-HC-III/76_circular-supply-delivery-note-page-3_ref20260902-0003.jpg":
        "76_circular-supply-delivery-note-11070_ref20260902-0003.jpg",
    TEAM / "Bududa/Bubungi-HC-III/78_circular-supply-delivery-note-page-4_ref20260902-0004.jpg":
        "78_circular-supply-delivery-note-11072_ref20260902-0004.jpg",
    TEAM / "Bududa/Bubungi-HC-III/79_circular-supply-delivery-note-11071-second-copy_ref20260902-0012.jpg":
        "79_circular-supply-delivery-note-11071_ref20260902-0012.jpg",
    TEAM / "Bulambuli/Bukibologoto-HC-II/02_destroyed-block-view-2_ref20260902-0007.jpg":
        "02_block-corner-over-collapsed-ground_ref20260902-0007.jpg",
    TEAM / "Bulambuli/Bukibologoto-HC-II/03_destroyed-block-view-3_ref20260902-0006.jpg":
        "03_frontage-and-porch-on-the-slope_ref20260902-0006.jpg",
    TEAM / "Bulambuli/Bukibologoto-HC-II/04_destroyed-block-view-4_ref20260902-0008.jpg":
        "04_block-corner-over-collapsed-ground-view-2_ref20260902-0008.jpg",
    TEAM / "Bulambuli/Bukibologoto-HC-II/07_simu-sub-county-offices_ref20260902-0010.jpg":
        "07_simu-sub-county-signboard-and-offices_ref20260902-0010.jpg",
    TEAM / "Bulambuli/Bulaago-HC-III/36_hand-filled-toolkit-checklist-view-2_ref20260902-0169.jpg":
        "36_hand-filled-toolkit-checklist-esr-stand-to-patient-trolley_ref20260902-0169.jpg",
    TEAM / "Bulambuli/Bulaago-HC-III/37_hand-filled-toolkit-checklist-view-3_ref20260902-0165.jpg":
        "37_hand-filled-toolkit-checklist-refrigerator-to-wall-clock_ref20260902-0165.jpg",
    TEAM / "Bulambuli/Bulaago-HC-III/38_hand-filled-toolkit-checklist-view-4_ref20260902-0168.jpg":
        "38_hand-filled-toolkit-checklist-diagnostic-sets-to-pediatric-beds_ref20260902-0168.jpg",
    TEAM / "Bulambuli/Bulaago-HC-III/39_hand-filled-toolkit-checklist-view-5_ref20260902-0167.jpg":
        "39_hand-filled-toolkit-checklist-kidney-dish-to-bench_ref20260902-0167.jpg",
    TEAM / "Bulambuli/Bulaago-HC-III/40_hand-filled-toolkit-checklist-view-6_ref20260902-0166.jpg":
        "40_hand-filled-toolkit-checklist-disinfection-buckets-to-laboratory-stool_ref20260902-0166.jpg",
    TEAM / "Bulambuli/Bulaago-HC-III/41_hand-filled-toolkit-checklist-view-7_ref20260902-0161.jpg":
        "41_hand-filled-toolkit-checklist-penguin-sucker-to-cheatle-jar_ref20260902-0161.jpg",
    TEAM / "Bulambuli/Bulaago-HC-III/42_hand-filled-toolkit-checklist-view-8_ref20260902-0162.jpg":
        "42_hand-filled-toolkit-checklist-ent-set-to-office-tables_ref20260902-0162.jpg",
    TEAM / "Bulambuli/Bulaago-HC-III/35_hand-filled-toolkit-checklist_ref20260902-0170.jpg":
        "35_hand-filled-toolkit-checklist-bp-machine-to-bowl-lotion_ref20260902-0170.jpg",
}


def load_maps() -> dict[Path, str]:
    renames: dict[Path, str] = dict(SEPT)
    for path in sorted(TMP.glob("t14_renames_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        # Find folder by looking up any key under team-14
        for old, new in data.items():
            old_name = Path(old).name
            new_name = Path(new).name
            matches = list(TEAM.rglob(old_name))
            if not matches:
                print("MISSING on disk:", old_name, "from", path.name)
                continue
            if len(matches) > 1:
                print("AMBIGUOUS", old_name, matches)
            src = matches[0]
            renames[src] = new_name
    return renames


def apply_disk(renames: dict[Path, str]) -> list[tuple[str, str]]:
    done = []
    for src, new_name in sorted(renames.items(), key=lambda x: str(x[0])):
        if not src.exists():
            # maybe already renamed
            if (src.parent / new_name).exists():
                done.append((src.name, new_name))
                continue
            print("SKIP missing", src)
            continue
        dest = src.parent / new_name
        if src.name == new_name:
            continue
        if dest.exists() and dest.resolve() != src.resolve():
            print("CONFLICT", dest)
            continue
        src.rename(dest)
        done.append((src.name, new_name))
    return done


def patch_text_file(path: Path, pairs: list[tuple[str, str]]) -> int:
    text = path.read_text(encoding="utf-8")
    n = 0
    # longest old names first to avoid partial collisions
    for old, new in sorted(pairs, key=lambda x: -len(x[0])):
        if old == new:
            continue
        if old in text:
            text = text.replace(old, new)
            n += 1
    path.write_text(text, encoding="utf-8")
    return n


def main():
    renames = load_maps()
    print("planned renames", len(renames))
    done = apply_disk(renames)
    print("disk renamed", len(done))
    pairs = done
    print("names.py patched", patch_text_file(NAMES_PY, pairs))
    print("media init patched", patch_text_file(MEDIA_INIT, pairs))
    # leftover uncaptioned
    left = list(TEAM.rglob("*uncaptioned*"))
    print("remaining uncaptioned", len(left))
    out = TMP / "t14_renames_applied.json"
    out.write_text(json.dumps({a: b for a, b in done}, indent=1), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
