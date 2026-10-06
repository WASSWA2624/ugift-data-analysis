from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import re,json
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
fp=P.parent/'ugift-working-report-06102026-1344-reconciled.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def tx(x):return ''.join(x.xpath('.//w:t/text()',namespaces=ns))
def norm(s):return re.sub(r'\s+',' ',s).strip()
z=ZipFile(fp);b=E.fromstring(z.read('word/document.xml')).find('w:body',ns);bs=[]
for i,e in enumerate(b):
 bs.append({'i':i,'kind':E.QName(e).localname,'text':norm(tx(e)),'style':e.xpath('./w:pPr/w:pStyle/@w:val',namespaces=ns),'charts':e.xpath('.//c:chart/@r:id',namespaces=ns),'images':e.xpath('.//a:blip/@r:embed',namespaces=ns)})
captions=[{'i':x['i'],'kind':m.group(1),'number':int(m.group(2)),'text':x['text']} for x in bs if (m:=re.match(r'^(Figure|Table)\s+(\d+):',x['text'],re.I))]
vague=[];generic=[];unlabelled=[]
for x in bs:
 if re.search(r'\b(table|figure|graph|chart)s?\s+(above|below)|\b(above|below|following)\s+(table|figure|graph|chart)s?',x['text'],re.I):vague.append(x)
 elif re.search(r'\b(the|following|these|a)\s+(table|figure|graph|chart)s?\b',x['text'],re.I) and not re.search(r'\b(Table|Figure)\s+\d+',x['text'],re.I):generic.append(x)
 if x['kind']=='tbl' and not x['images']:
  prev=[p for p in bs[:x['i']] if p['text'] and p['kind']=='p']
  nearest=prev[-1] if prev else None
  if nearest and not re.match(r'^Table\s+\d+:',nearest['text'],re.I):unlabelled.append({'i':x['i'],'preceding':nearest['text'],'text_start':x['text'][:220]})
report={'file':str(fp),'paragraphs':bs,'captions':captions,'vague_references':vague,'generic_references_without_number':generic,'unlabelled_data_tables':unlabelled}
(P/'figure-table-reference-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('VAGUE REFERENCES')
for x in vague:print(x['i'],x['kind'],x['text'])
print('GENERIC UNNUMBERED REFERENCES')
for x in generic:print(x['i'],x['kind'],x['text'])
print('UNLABELLED DATA TABLES')
for x in unlabelled:print(x)
