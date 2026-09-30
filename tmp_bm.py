from docx import Document
from docx.oxml.ns import qn

d = Document(r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx")
p = d.paragraphs[498]
names = [bm.get(qn("w:name")) for bm in p._p.iter(qn("w:bookmarkStart"))]
print(names)
print(p._p.xml[p._p.xml.find("<w:bookmarkStart"): p._p.xml.find("<w:bookmarkStart") + 200])
