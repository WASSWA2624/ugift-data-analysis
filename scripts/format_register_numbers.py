"""Show amounts with thousands separators and keep the header visible."""

import re
import zipfile
from pathlib import Path

PATH = Path(
    r"D:\coding\ugift-data-analysis\outputs\asset-register-2026-09-23"
    r"\REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
)
MONEY = {"H", "M", "AI", "AK", "AL", "AM", "AZ", "BA"}
OPEN = re.compile(rb'<c r="([A-Z]+)(\d+)"([^>/]*)(/?)>')


def ensure_writable(path: Path) -> None:
    try:
        handle = open(path, "r+b")
    except PermissionError:
        import win32com.client

        workbook = win32com.client.GetObject(str(path.resolve()))
        application = workbook.Application
        workbook.Close(SaveChanges=False)
        if application.Workbooks.Count == 0:
            application.Quit()
        return
    handle.close()


def patch_styles(xml: bytes) -> bytes:
    if b'formatCode="#,##0.##"' in xml:
        return xml
    xml = xml.replace(
        b"<fonts ",
        b'<numFmts count="1"><numFmt numFmtId="164" formatCode="#,##0.##"/></numFmts><fonts ',
        1,
    )
    xml = xml.replace(b'<fonts count="1"', b'<fonts count="2"', 1)
    xml = xml.replace(
        b"</fonts>",
        b'<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/><family val="2"/></font></fonts>',
        1,
    )
    xml = xml.replace(b'<fills count="5">', b'<fills count="6">', 1)
    xml = xml.replace(
        b"</fills>",
        b'<fill><patternFill patternType="solid"><fgColor rgb="FF1F4E79"/>'
        b'<bgColor indexed="64"/></patternFill></fill></fills>',
        1,
    )
    number = (
        b'<xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1" applyAlignment="1">'
        b'<alignment horizontal="right"/></xf>'
        b'<xf numFmtId="164" fontId="0" fillId="2" borderId="0" xfId="0" applyNumberFormat="1" applyFill="1" applyAlignment="1">'
        b'<alignment horizontal="right"/></xf>'
        b'<xf numFmtId="164" fontId="0" fillId="3" borderId="0" xfId="0" applyNumberFormat="1" applyFill="1" applyAlignment="1">'
        b'<alignment horizontal="right"/></xf>'
        b'<xf numFmtId="164" fontId="0" fillId="4" borderId="0" xfId="0" applyNumberFormat="1" applyFill="1" applyAlignment="1">'
        b'<alignment horizontal="right"/></xf>'
        b'<xf numFmtId="0" fontId="1" fillId="5" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1">'
        b'<alignment horizontal="center" vertical="center" wrapText="1"/></xf>'
    )
    xml = xml.replace(b'<cellXfs count="4">', b'<cellXfs count="9">', 1)
    xml = xml.replace(b"</cellXfs>", number + b"</cellXfs>", 1)
    return xml


def patch_sheet(sheet: bytes) -> bytes:
    sheet = re.sub(rb' s="1"(?!\d)', b' s="5"', sheet)
    sheet = re.sub(rb' s="2"(?!\d)', b' s="6"', sheet)
    sheet = re.sub(rb' s="3"(?!\d)', b' s="7"', sheet)

    def retag(match: re.Match) -> bytes:
        column = match.group(1).decode()
        row = match.group(2).decode()
        rest = match.group(3)
        close = match.group(4)
        if row == "1":
            if b" s=" not in rest:
                rest = b' s="8"' + rest
        elif column in MONEY and b" s=" not in rest:
            rest = b' s="4"' + rest
        return b'<c r="' + match.group(1) + match.group(2) + b'"' + rest + close + b">"

    sheet = OPEN.sub(retag, sheet)
    sheet = sheet.replace(
        b'<row r="1" spans="1:64" x14ac:dyDescent="0.35">',
        b'<row r="1" spans="1:64" ht="32" customHeight="1" x14ac:dyDescent="0.35">',
        1,
    )
    sheet = sheet.replace(
        b'<sheetView tabSelected="1" topLeftCell="A295" workbookViewId="0"><selection activeCell="F1" sqref="F1"/></sheetView>',
        b'<sheetView tabSelected="1" topLeftCell="A1" workbookViewId="0">'
        b'<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
        b'<selection pane="bottomLeft" activeCell="A2" sqref="A2"/></sheetView>',
        1,
    )
    cols = (
        b"<cols>"
        b'<col min="1" max="1" width="22" customWidth="1"/>'
        b'<col min="2" max="2" width="28" customWidth="1"/>'
        b'<col min="3" max="5" width="28" customWidth="1"/>'
        b'<col min="6" max="7" width="16" customWidth="1"/>'
        b'<col min="8" max="8" width="12" customWidth="1"/>'
        b'<col min="9" max="11" width="24" customWidth="1"/>'
        b'<col min="13" max="13" width="18" customWidth="1"/>'
        b'<col min="32" max="32" width="22" customWidth="1"/>'
        b'<col min="35" max="35" width="16" customWidth="1"/>'
        b'<col min="37" max="39" width="18" customWidth="1"/>'
        b'<col min="42" max="42" width="18" customWidth="1"/>'
        b'<col min="52" max="53" width="18" customWidth="1"/>'
        b'<col min="55" max="55" width="42" customWidth="1"/>'
        b"</cols>"
    )
    sheet = re.sub(rb"<cols>.*?</cols>", cols, sheet, count=1, flags=re.S)
    return sheet


def main() -> None:
    ensure_writable(PATH)
    print("reading", flush=True)
    with zipfile.ZipFile(PATH) as source:
        pieces = []
        sheet = b""
        for item in source.infolist():
            data = source.read(item.filename)
            if item.filename == "xl/worksheets/sheet1.xml":
                sheet = data
            elif item.filename == "xl/styles.xml":
                pieces.append((item.filename, patch_styles(data)))
            else:
                pieces.append((item.filename, data))
    print("formatting", flush=True)
    sheet = patch_sheet(sheet)
    temporary = PATH.with_suffix(".tmp.xlsx")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as target:
        for name, data in pieces:
            target.writestr(name, data)
        target.writestr("xl/worksheets/sheet1.xml", sheet)
    temporary.replace(PATH)
    print("rows", sheet.count(b"<row "))
    print("broken", len(re.findall(rb'<row r="\d+ spans=', sheet)))
    print("frozen", b'state="frozen"' in sheet)
    print("format", b'formatCode="#,##0.##"' in pieces[[name for name, _ in pieces].index("xl/styles.xml")][1])
    print("size", PATH.stat().st_size)


if __name__ == "__main__":
    main()
