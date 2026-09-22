# -*- coding: utf-8 -*-
"""Verify Team 14 tree after rebuild, then mirror to Drive (RULES.md 7)."""
import filecmp
import os
import shutil
import zipfile
from pathlib import Path

base = Path(r"d:/coding/apps/ugift/facility-registers/team-14")
drive_root = Path(r"G:/My Drive/UgIFT/team-14")
zip_path = next(base.glob("WhatsApp Chat with *.zip"))

print("=== leftover unpack / README ===")
for name in ("_wa_unpack", "_wa_extract", "_unpack"):
    print(" ", name, (base / name).exists())
readmes = list(base.rglob("README*"))
print(" READMEs", readmes)

print("\n=== keep-critical files ===")
need = [
    base / "Bududa/Bubungi-HC-III/72_circular-supply-delivery-note-11069_ref20260902-0000.jpg",
    base / "Bududa/Bubungi-HC-III/90_hand-filled-toolkit-challenges-and-recommendations_ref20260903-0052.jpg",
    base / "Bududa/Bubungi-HC-III/Asset-Verification-Toolkit.docx",
    base / "Sironko/Simu-Pondo-HC-III/45_circular-supply-delivery-note-10016_ref20260901-0159.jpg",
    base / "Sironko/Simu-Pondo-HC-III/48_hand-filled-toolkit-verification-details-and-discussion-guide_ref20260903-0040.jpg",
    base / "Sironko/Simu-Pondo-HC-III/Asset-Verification-Toolkit.docx",
    base / "Bududa/_district-documents/05_issue-voucher-521-bubungi-hc-iii_ref20260902-scan01.jpg",
    base / "Bududa/_district-documents/Bududa-issue-and-goods-vouchers-scanned.pdf",
    base / "_team-documents/field-report-transcript.txt",
    base / "_team-documents/team-14-process-report.docx",
]
for p in need:
    print(" ", "OK" if p.exists() else "MISSING", p.relative_to(base))

print("\n=== zip vs mapped (via dest on disk) ===")
import sys
sys.path.insert(0, r"d:/coding/apps/ugift/src")
import team_registers as T
import team14_media
t = T.TEAMS["team-14"]
team14_media.apply(t)
mapped = set()
mapped.update(t.get("team_docs", {}))
for cfg in t["districts"].values():
    mapped.update(cfg.get("lg_docs", {}))
    for files in cfg.get("facilities", {}).values():
        mapped.update(files)
with zipfile.ZipFile(zip_path) as z:
    zip_files = {Path(n).name for n in z.namelist() if not n.endswith("/")}
from team_registers import SKIP
unfiled = sorted(f for f in zip_files if f not in mapped and f not in SKIP and not f.lower().endswith(".txt"))
print(" zip", len(zip_files), "unfiled", unfiled)

print("\n=== toolkits ===")
for p in sorted(base.rglob("Asset-Verification-Toolkit.docx")):
    print(" ", p.relative_to(base), p.stat().st_size)

print("\n=== transcript tail ===")
text = (base / "_team-documents/field-report-transcript.txt").read_text(encoding="utf-8")
print(text.strip().splitlines()[-3:])

# Drive mirror: only team-14, exclude zip / transcript / unpack
EXCLUDE_NAMES = {
    "field-report-transcript.txt",
}
EXCLUDE_SUFFIX = (".zip",)
EXCLUDE_DIR_PREFIX = ("WhatsApp Chat", "_wa_", "_unpack")

def excluded(rel: Path) -> bool:
    parts = rel.parts
    if any(p.startswith(EXCLUDE_DIR_PREFIX) or p.startswith("WhatsApp Chat") for p in parts):
        return True
    if rel.name in EXCLUDE_NAMES:
        return True
    if rel.suffix.lower() in EXCLUDE_SUFFIX:
        return True
    if rel.name.lower().endswith(".txt") and "WhatsApp Chat" in rel.name:
        return True
    return False

src_files = {}
for p in base.rglob("*"):
    if not p.is_file():
        continue
    rel = p.relative_to(base)
    if excluded(rel):
        continue
    src_files[rel] = p

drive_files = {}
if drive_root.exists():
    for p in drive_root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(drive_root)
        drive_files[rel] = p

added = replaced = removed = skipped = 0
# Remove Drive copies of excluded kinds (7.3)
if drive_root.exists():
    for rel, dp in list(drive_files.items()):
        if excluded(rel) or rel.name == "RULES.md":
            dp.unlink()
            removed += 1
            drive_files.pop(rel, None)
            print(" drive remove excluded", rel)

# Remove Drive files deleted here
for rel, dp in list(drive_files.items()):
    if rel not in src_files:
        dp.unlink()
        removed += 1
        print(" drive remove gone", rel)

# Add / replace
for rel, sp in src_files.items():
    dest = drive_root / rel
    if rel not in drive_files:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sp, dest)
        added += 1
    else:
        same = False
        try:
            same = sp.stat().st_size == drive_files[rel].stat().st_size and filecmp.cmp(sp, dest, shallow=False)
        except OSError:
            same = False
        if same:
            skipped += 1
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(sp, dest)
            replaced += 1

print("\n=== Drive mirror team-14 ===")
print(" added", added, "replaced", replaced, "removed", removed, "unchanged", skipped)
print(" drive exists", drive_root.exists())
