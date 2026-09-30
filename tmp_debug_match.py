import re
from pypdf import PdfReader
from docx import Document

reader = PdfReader(r"D:\coding\ugift-data-analysis\tmp_report_export.pdf")
chunks = []
for page in reader.pages[:8]:
    chunks.append(page.extract_text() or "")
blob = re.sub(r"\s+", " ", " ".join(chunks))
key = "Executive summary"
index = blob.find(key)
print("index", index)
print(repr(blob[index:index + 80]))
print("--- doc samples ---")
d = Document(r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx")
for i in (29, 52, 53, 190):
    print(i, repr(d.paragraphs[i].text[:100]))
