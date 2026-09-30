import re
import shutil
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from pypdf import PdfReader

PDF = Path(r"D:\coding\ugift-data-analysis\tmp_report_export.pdf")
DOC = Path(r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx")
OFFICIAL = Path(r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.pdf")

reader = PdfReader(str(PDF))
chunks = []
for page in reader.pages:
    text = page.extract_text() or ""
    if "List of acronyms" in text and chunks:
        break
    chunks.append(text)
blob = re.sub(r"\s+", " ", " ".join(chunks))


def page_for(title):
    key = re.sub(r"\s+", " ", title).strip()
    start = 0
    while True:
        index = blob.find(key, start)
        if index < 0:
            return None
        after = blob[index + len(key): index + len(key) + 280]
        match = re.match(r"[\s\.]{0,260}(\d{1,3})\b", after)
        if match:
            return match.group(1)
        start = index + 1


def set_result(paragraph, number):
    seen = False
    for node in paragraph._p.iter():
        if node.tag == qn("w:fldChar") and node.get(qn("w:fldCharType")) == "separate":
            seen = True
            continue
        if seen and node.tag == qn("w:t") and node.text and node.text.strip().isdigit():
            node.text = number
            return True
    return False


document = Document(DOC)
updated = 0
missing = []
for paragraph in document.paragraphs:
    if "PAGEREF" not in paragraph._p.xml:
        continue
    if paragraph.style and paragraph.style.name.startswith("Heading"):
        break
    title = paragraph.text.split("\t")[0].strip()
    if not title:
        continue
    number = page_for(title)
    if number is None:
        missing.append(title[:80])
        continue
    if set_result(paragraph, number):
        updated += 1
    else:
        missing.append("NORESULT " + title[:80])

document.save(DOC)
print("updated", updated, "missing", len(missing))
for item in missing[:15]:
    print(" -", item)

try:
    shutil.copyfile(PDF, OFFICIAL)
    print("pdf replaced")
except OSError as error:
    print("pdf copy failed", error)
