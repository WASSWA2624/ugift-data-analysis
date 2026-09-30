import time
import win32com.client

src = r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx"
pdf = r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT-mda-export.pdf"

word = win32com.client.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = 0
doc = None
try:
    doc = word.Documents.Open(src)
    doc.Activate()
    word.ActiveWindow.View.Type = 3
    pages = doc.ComputeStatistics(2)
    print("pages", pages, flush=True)
    doc.Repaginate()
    updated = doc.Fields.Update()
    print("updated", updated, flush=True)
    shown = 0
    for index in range(1, doc.Fields.Count + 1):
        field = doc.Fields(index)
        code = field.Code.Text
        if "PAGEREF heading_24" in code or "PAGEREF heading_mofped" in code or "Executive" in field.Result.Text:
            print(code.strip(), "=>", field.Result.Text.strip(), flush=True)
            shown += 1
            if shown >= 6:
                break
    doc.Save()
    doc.ExportAsFixedFormat(pdf, 17)
    print("exported", flush=True)
    doc.Close(False)
finally:
    word.Quit()
