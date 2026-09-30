from docx import Document
from docx.oxml.ns import qn

d = Document(r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx")
count = 0
for p in d.paragraphs:
    xml = p._p.xml
    if "SEQ Figure" not in xml:
        continue
    count += 1
    if count <= 3 or "Health centres" in p.text:
        texts = [t.text for t in p._p.iter(qn("w:t"))]
        print(count, texts)
print("seq fields", count)
