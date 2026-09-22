from pathlib import Path
import re

t = Path(r"d:/coding/apps/ugift/src/team14_media/names.py").read_text(encoding="utf-8")
keys = re.findall(r"'(IMG-[^']+)'", t)
print("mapped imgs", len(keys), "unique", len(set(keys)))

base = Path(r"d:/coding/apps/ugift/facility-registers/team-14")
jpgs = [j for j in base.rglob("*.jpg") if "_wa_extract" not in str(j) and "tmp" not in str(j)]
print("filed jpgs", len(jpgs))

for p in [
    base / "Bulambuli/Sisiyi-Seed-Secondary-School/team-field-note.docx",
    base / "Sironko/Simu-Pondo-HC-III",
    base / "Bududa/Bumusi-HC-III",
]:
    print(p.name if p.is_file() else p, "->", p.exists())
    if p.is_dir():
        for f in sorted(p.iterdir()):
            if f.suffix.lower() in {".docx", ".pdf"} or "invent" in f.name.lower():
                print(" ", f.name)
