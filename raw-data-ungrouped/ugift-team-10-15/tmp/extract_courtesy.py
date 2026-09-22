"""Extract text from LG courtesy-call docs only."""
from pathlib import Path
from docx import Document
import re

ROOT = Path("facility-registers")
PHONE = re.compile(r"(?:\+?256[\s\-]*)?0?7\d[\d\s\-/]{6,12}\d", re.I)

def doc_text(path: Path) -> str:
    try:
        doc = Document(path)
    except Exception:
        return ""
    parts = []
    for p in doc.paragraphs:
        if p.text.strip():
            parts.append(p.text.strip())
    for t in doc.tables:
        for row in t.rows:
            cells = [c.text.strip() for c in row.cells if c.text.strip()]
            if cells:
                parts.append(" | ".join(cells))
    return "\n".join(parts)

for team in range(10, 16):
    paths = sorted((ROOT / f"team-{team}").rglob("*LG-courtesy-call.docx"))
    paths += sorted((ROOT / f"team-{team}").rglob("*LG-officer-interview*.docx"))
    print(f"\n======== TEAM {team} ({len(paths)} docs) ========")
    for p in paths:
        text = doc_text(p)
        print(f"\n--- {p.relative_to(ROOT)} ---")
        # print whole short docs
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for ln in lines:
            ln = " ".join(ln.split())
            if len(ln) > 350:
                ln = ln[:350] + "…"
            print(ln)
