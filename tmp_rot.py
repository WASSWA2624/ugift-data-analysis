import pythoncom

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
    except Exception as error:
        name = f"err {error}"
    if "UgIFT" in name or "Word" in name or "ugift" in name.lower():
        print(name)
