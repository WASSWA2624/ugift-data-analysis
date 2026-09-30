import fitz

doc = fitz.open(r"D:\coding\ugift-data-analysis\tmp_report_export.pdf")
# printed page = pdf page number - 1; render printed 34, 35, 37, 42
for printed in (34, 35, 37, 42):
    page = doc[printed]  # 0-based index equals printed number
    pix = page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3), alpha=False)
    path = rf"D:\coding\ugift-data-analysis\tmp_page_{printed}.png"
    pix.save(path)
    print("saved", path, "footer check", page.get_text()[:80].replace("\n", " | "))
doc.close()
