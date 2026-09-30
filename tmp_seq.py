from docx import Document

d = Document(r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx")
for p in d.paragraphs:
    if p.style and p.style.name == "Caption1" and "Health centres" in p.text and p.text.startswith("Figure"):
        print(p.text[:90])
