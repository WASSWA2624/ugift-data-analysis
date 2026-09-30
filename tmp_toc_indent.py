from docx import Document

d = Document(r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx")
for i in (30, 31, 50, 51, 52):
    p = d.paragraphs[i]
    print(i, repr(p.text[:70]))
    print(p._p.xml[p._p.xml.find("<w:pPr"): p._p.xml.find("</w:pPr>") + 8])
    print("---")
