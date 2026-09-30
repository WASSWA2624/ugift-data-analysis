from docx import Document

d = Document(r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx")
for i in (52, 53, 177):
    print(i, d.paragraphs[i].text[:140])
