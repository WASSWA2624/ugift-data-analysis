import pythoncom
import win32com.client

target = r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.docx"
context = pythoncom.CreateBindCtx(0)
table = pythoncom.GetRunningObjectTable()
enum = table.EnumRunning()
while True:
    monikers = enum.Next(1)
    if not monikers:
        break
    moniker = monikers[0]
    try:
        name = moniker.GetDisplayName(context, None)
    except Exception:
        continue
    if name.lower() != target.lower():
        continue
    obj = table.GetObject(moniker).QueryInterface(pythoncom.IID_IDispatch)
    doc = win32com.client.Dispatch(obj)
    print("saved", doc.Saved, "readonly", doc.ReadOnly, "name", doc.Name)
    if doc.Saved:
        doc.Close(False)
        print("closed")
    else:
        print("unsaved, left open")
