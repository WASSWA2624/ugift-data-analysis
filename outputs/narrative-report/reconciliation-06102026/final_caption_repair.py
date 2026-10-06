from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
FILE=Path(__file__).resolve().parent.parent/'ugift-working-report-06102026-1344-reconciled.docx'
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
with ZipFile(FILE) as z:parts={p:z.read(p) for p in z.namelist()}
root=E.fromstring(parts['word/document.xml'])
body=root.find('w:body',N)
text=lambda p:''.join(p.xpath('.//w:t/text()',namespaces=N))
for p in list(body):
    if text(p).startswith('Figure 46 compares these arrangements'):
        previous=p.getprevious()
        if previous is not None and previous.find('.//c:chart',N) is not None:
            body.remove(p)
            previous.addprevious(p)
            print('Placed maintenance comparison before graph; caption immediately below graph.')
if not any(text(p).strip()=='Table of Contents' for p in body):
    reference=FILE.parent/'ugift-working-report-06102026-1344.docx'
    with ZipFile(reference) as z:
        source=E.fromstring(z.read('word/document.xml'))
    title=next(deepcopy(p) for p in source.xpath('.//w:p',namespaces=N) if text(p).strip()=='Table of Contents')
    for child in list(title):
        if child.tag!='{'+N['w']+'}pPr':title.remove(child)
    for attr in list(title.attrib):
        if attr.endswith('}paraId') or attr.endswith('}textId'):del title.attrib[attr]
    r=E.SubElement(title,'{'+N['w']+'}r')
    t=E.SubElement(r,'{'+N['w']+'}t');t.text='Table of Contents'
    anchor=next(p for p in body if p.tag.endswith('}p') and text(p).startswith('Executive summary'))
    anchor.addprevious(title)
    print('Restored the original Table of Contents heading as plain text outside its field.')
parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(FILE,'w',ZIP_DEFLATED) as z:
    for p,data in parts.items():z.writestr(p,data)
