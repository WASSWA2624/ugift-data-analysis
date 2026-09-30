from docx import Document

d = Document(r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx")
want = (
    "Executive summary",
    "4.2 Ministries",
    "4.2.5 Ministry",
    "4.3 Health",
    "6 Conclusion",
    "Figure 46a:",
    "Figure 47:",
    "Appendix I",
)
for p in d.paragraphs:
    text = p.text
    if any(text.startswith(item) for item in want) and "\t" in text:
        print(text[:110])
