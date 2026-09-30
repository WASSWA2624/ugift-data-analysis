from pypdf import PdfReader

reader = PdfReader(r"D:\coding\ugift-data-analysis\tmp_report_export.pdf")
out = open(r"D:\coding\ugift-data-analysis\tmp_toc_pdf.txt", "w", encoding="utf-8")
for index in range(1, 8):
    text = reader.pages[index].extract_text() or ""
    out.write(f"\n===== PDF {index + 1} =====\n")
    out.write(text)
out.close()
print("wrote")
