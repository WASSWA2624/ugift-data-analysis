"""Keep a financial note attached and give retained photographs a stable reference."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
from hashlib import sha256
import json

P=Path(__file__).resolve().parent
F=P.parent/'ugift-working-report-06102026-1344-reconciled.docx'
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
Q=lambda name:'{'+N['w']+'}'+name
text=lambda el:''.join(el.xpath('.//w:t/text()',namespaces=N))
with ZipFile(F) as z:
    parts={name:z.read(name) for name in z.namelist()}
root=E.fromstring(parts['word/document.xml'])
body=root.find('w:body',N)
before=sha256(F.read_bytes()).hexdigest()

def keep_next(p):
    pr=p.find('w:pPr',N)
    if pr is None:
        pr=E.Element(Q('pPr'));p.insert(0,pr)
    keep=pr.find('w:keepNext',N)
    if keep is None:
        keep=E.SubElement(pr,Q('keepNext'))
    keep.set(Q('val'),'1')

title=next(p for p in body if text(p).startswith('Table 52:'))
table=title.getnext()
assert table.tag==Q('tbl')
note=table.getnext()
assert text(note).startswith('Amounts in UGX million.')
for p in table.findall('w:tr',N)[-1].xpath('.//w:p',namespaces=N):
    keep_next(p)

intro=next(p for p in body if text(p)=='The photos below show some of the asets')
texts=intro.xpath('.//w:t',namespaces=N)
texts[0].text='Figure 16A shows some of the assets verified at regional blood banks.'
for t in texts[1:]:t.text=''
photos=intro.getnext()
assert photos.tag==Q('tbl')
exemplar=next(p for p in body if text(p).startswith('Figure 16:'))
caption=deepcopy(exemplar)
for attr in list(caption.attrib):
    if attr.endswith('}paraId') or attr.endswith('}textId'):del caption.attrib[attr]
exemplar_rp=next((r.find('w:rPr',N) for r in caption.findall('w:r',N) if r.find('w:rPr',N) is not None),None)
for child in list(caption):
    if child.tag!=Q('pPr'):caption.remove(child)
r=E.SubElement(caption,Q('r'))
if exemplar_rp is not None:r.append(deepcopy(exemplar_rp))
E.SubElement(r,Q('t')).text='Figure 16A: Asset photographs from regional blood banks'
pr=caption.find('w:pPr',N)
keep=pr.find('w:keepNext',N)
if keep is None:keep=E.SubElement(pr,Q('keepNext'))
keep.set(Q('val'),'0')
photos.addnext(caption)
for p in photos.findall('w:tr',N)[-1].xpath('.//w:p',namespaces=N):
    keep_next(p)

parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(F,'w',ZIP_DEFLATED) as z:
    for name,data in parts.items():z.writestr(name,data)
audit={'source_sha256':before,'output_sha256':sha256(F.read_bytes()).hexdigest(),'changes':['Keep Table 52 Total row with its financial note','Reference eight retained blood-bank photographs as composite Figure 16A, preserving all existing Figure 1–47 numbers'],'metrics_changed':False}
(P/'final-layout-repairs.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print(json.dumps(audit,indent=2))
