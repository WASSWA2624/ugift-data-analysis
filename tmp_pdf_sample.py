from pypdf import PdfReader

reader = PdfReader(r"D:\coding\ugift-data-analysis\tmp_report_export.pdf")
print("pages", len(reader.pages))
for index in (0, 1, 8, 30):
    text = reader.pages[index].extract_text() or ""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    print("---", index + 1, "---")
    print(" | ".join(lines[:3])[:200])
    print("LAST", lines[-3:])
