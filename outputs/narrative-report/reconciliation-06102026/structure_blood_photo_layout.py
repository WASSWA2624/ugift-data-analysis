from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json
from pypdf import PdfReader
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def tx(x):return ''.join(x.xpath('.//w:t/text()',namespaces=ns))
z=ZipFile(P.parent/'ugift-working-report-06102026-1344-reconciled.docx');body=E.fromstring(z.read('word/document.xml')).find('w:body',ns)
i=next(i for i,x in enumerate(body) if tx(x)=='The photos below show some of the asets')
rels={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('word/_rels/document.xml.rels'))}
tab=body[i+1]
rows=[]
for ri,row in enumerate(tab.findall('w:tr',ns)):
 cells=[]
 for ci,c in enumerate(row.findall('w:tc',ns)):
  rids=c.xpath('.//a:blip/@r:embed',namespaces=ns)
  cells.append({'cell':ci,'text':tx(c),'image_parts':[rels[r] for r in rids]})
 rows.append({'row':ri,'cells':cells})
doc=PdfReader(P/'final-reference-render'/'ugift-working-report-06102026-1344-reconciled.pdf').pages
pages=[]
for pi,p in enumerate(doc):
 t=p.extract_text()
 if 'photos below show some of the' in t or any(s in t for s in ['Donor couches at Hoima','Freezer at Hoima Regional','Refrigerators at Soroti Regional']):
  pages.append({'physical_page':pi+1,'text':t,'rect':list(p.mediabox)})
out={'sentence_body_index':i,'photo_table_body_index':i+1,'photos':sum(len(c['image_parts']) for r in rows for c in r['cells']),'rows':rows,'following_blocks':[{'i':j,'kind':E.QName(body[j]).localname,'text':tx(body[j])} for j in range(i+2,i+7)],'pages':pages}
(P/'blood-bank-photo-layout-audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
