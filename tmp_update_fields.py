import win32com.client

src = r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx"
pdf = r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.pdf"

word = win32com.client.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = 0
try:
    doc = word.Documents.Open(src)
    updated = doc.Fields.Update()
    doc.Save()
    doc.ExportAsFixedFormat(pdf, 17)
    doc.Close(False)
    print("fields", updated)
finally:
    word.Quit()
