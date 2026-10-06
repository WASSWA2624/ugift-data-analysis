"""Remove the user's unwanted final appendix without changing other content."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from hashlib import sha256
import json

P=Path(__file__).resolve().parent
F=P.parent/'ugift-working-report-06102026-1344-reconciled.docx'
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
text=lambda el:''.join(el.xpath('.//w:t/text()',namespaces=N))
with ZipFile(F) as z:parts={name:z.read(name) for name in z.namelist()}
root=E.fromstring(parts['word/document.xml'])
body=root.find('w:body',N)
blocks=list(body)
index=next(i for i,p in enumerate(blocks) if text(p).startswith('Appendix L Responses to reviewer comments') and p.xpath('./w:pPr/w:pStyle[starts-with(@w:val,"Heading")]',namespaces=N))
removed=[]
before_text=[text(p) for p in blocks[:index]]
before_charts=[parts[name] for name in sorted(parts) if name.startswith('word/charts/')]
audit={'source_sha256':sha256(F.read_bytes()).hexdigest(),'appendix_start_body_index':index,'removed_blocks':[]}
for el in blocks[index:]:
    if el.tag=='{'+N['w']+'}sectPr':continue
    audit['removed_blocks'].append({'tag':E.QName(el).localname,'text':text(el)})
    body.remove(el)
assert [text(p) for p in list(body)[:index]]==before_text
assert len([x for x in audit['removed_blocks'] if x['tag']=='tbl'])==1
parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
assert before_charts==[parts[name] for name in sorted(parts) if name.startswith('word/charts/')]
with ZipFile(F,'w',ZIP_DEFLATED) as z:
    for name,data in parts.items():z.writestr(name,data)
audit['output_sha256']=sha256(F.read_bytes()).hexdigest()
(P/'appendix-l-removal.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'removed_blocks':len(audit['removed_blocks']),'removed_tables':1,'other_body_text_unchanged':True,'chart_parts_unchanged':True,'sha256':audit['output_sha256']},indent=2))
