import pythoncom
import win32com.client

target = r"D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.pdf"
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
    print("saved", getattr(doc, "Saved", None), "name", getattr(doc, "Name", name))
    try:
        doc.Close(False)
        print("closed pdf")
    except Exception as error:
        print("close failed", error)
