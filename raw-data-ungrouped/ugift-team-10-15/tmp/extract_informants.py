"""Extract Informant interviewed / Received by from facility & LG docs only."""
from pathlib import Path
from docx import Document
import re

ROOT = Path("facility-registers")

def tables_and_paras(path: Path):
    try:
        doc = Document(path)
    except Exception:
        return []
    lines = []
    for p in doc.paragraphs:
        t = p.text.strip()
        if t:
            lines.append(t)
    for table in doc.tables:
        for row in table.rows:
            cells = [c.text.strip() for c in row.cells]
            if any(cells):
                lines.append(" | ".join(cells))
    return lines

KEY = re.compile(
    r"Informant interviewed|Received by|Also (?:seen|present)|Directed to|"
    r"Officers named|Also seen",
    re.I,
)

for team in range(10, 16):
    print(f"\n===== TEAM {team} =====")
    team_dir = ROOT / f"team-{team}"
    # facility reports + district docs only
    for path in sorted(team_dir.rglob("*.docx")):
        if path.name.startswith("~"):
            continue
        rel = path.relative_to(team_dir).as_posix()
        if "_team-documents" in rel:
            continue
        # skip toolkit fills / photo folders - only reports & district docs
        name = path.name.lower()
        if not (
            "facility-report" in name
            or "school-" in name
            or "health-centre" in name
            or "lg-courtesy" in name
            or "lg-officer" in name
            or "team-field-note" in name
            or "-school-" in name
            or "-health-" in name
        ):
            # also catch pattern like Nakapiripirit-school-Moruita...
            if not re.search(r"-(school|health-centre)-", name):
                if "field-note" not in name and "courtesy" not in name and "officer" not in name:
                    continue
        lines = tables_and_paras(path)
        hits = [ln for ln in lines if KEY.search(ln)]
        # also grab line after Informant if split
        if not hits:
            continue
        print(f"\n{rel}")
        for h in hits:
            h = " ".join(h.split())
            if len(h) > 300:
                h = h[:300] + "…"
            print(f"  {h}")
