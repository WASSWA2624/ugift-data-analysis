from pypdf import PdfReader

r = PdfReader(r"D:\coding\ugift-data-analysis\outputs\narrative-report\_export_mda.pdf")
needles = (
    "4.2.5 ",
    "4.2.17 ",
    "4.3 Health",
    "4.4 Seed",
    "4.5 Blood",
    "4.6 Facilities",
    "4.7 UgIFT",
    "4.8 Summary",
    "5 Recommendations",
    "6 Conclusion",
    "Appendix A",
    "Appendix I",
    "Table 12:",
    "Table 13:",
    "Figure 46:",
    "Figure 47:",
    "Executive summary",
)
for i, page in enumerate(r.pages):
    text = page.extract_text() or ""
    hits = [n for n in needles if n in text]
    if not hits:
        continue
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    last = lines[-1][:90] if lines else ""
    print(f"PDF {i+1} | {last} | {hits}")
