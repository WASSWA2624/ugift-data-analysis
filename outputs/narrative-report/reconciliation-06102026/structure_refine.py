import json, re
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
d=json.loads((P/'structure-audit.json').read_text(encoding='utf-8'))
ns={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart','a':'http://schemas.openxmlformats.org/drawingml/2006/main','w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
z=ZipFile(d['baseline']['file'])
out=[]
for b in d['baseline']['blocks']:
 if b['charts']:
  chart=E.fromstring(z.read('word/'+b['charts'][0]['target']))
  series=[]
  for s in chart.xpath('.//c:ser',namespaces=ns):
   series.append({'label':s.xpath('./c:tx//c:v/text()',namespaces=ns),'categories':s.xpath('./c:cat//c:v/text()',namespaces=ns),'values':s.xpath('./c:val//c:v/text()',namespaces=ns)})
  out.append({'body_index':b['index'],'previous_text':d['baseline']['blocks'][b['index']-1]['text'],'chart':b['charts'],'title':chart.xpath('.//c:title//a:t/text()',namespaces=ns),'series':series})
d['native_chart_inventory']=out
(P/'structure-audit.json').write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
print('ALL VISUAL ARCHIVE INDEX/NAME')
for b in d['baseline']['blocks'][638:]:
 if b['images'] or b['charts']:print(b['index'],d['baseline']['blocks'][b['index']-1]['text'],[im['target'] for im in b['images']],b['charts'])
print('HIGHLIGHTED CURRENT HEADINGS')
for b in d['current']['blocks']:
 if b.get('style') and b.get('highlights'):print(b['index'],b['style'],b['highlight_share'],b['text'])
