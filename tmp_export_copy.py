import shutil
import win32com.client

src = r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx"
copy = r"D:\coding\ugift-data-analysis\tmp_report_export.docx"
pdf = r"D:\coding\ugift-data-analysis\tmp_report_export.pdf"
shutil.copyfile(src, copy)
word = win32com.client.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = 0
try:
    doc = word.Documents.Open(copy)
    print("opened", flush=True)
    doc.ExportAsFixedFormat(pdf, 17)
    print("exported", flush=True)
    doc.Close(False)
finally:
    word.Quit()
