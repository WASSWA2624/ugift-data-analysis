from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,re
P=Path(__file__).resolve().parent
F=P.parent/'ugift-working-report-06102026-1344-reconciled.docx'
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def text(x):return ''.join(x.xpath('.//w:t/text()',namespaces=N))
with ZipFile(F) as z:
    root=E.fromstring(z.read('word/document.xml'))
    body=root.find('w:body',N)
    paras=[{'i':i,'text':text(x),'style':x.xpath('./w:pPr/w:pStyle/@w:val',namespaces=N)} for i,x in enumerate(body) if x.tag.endswith('}p')]
    (P/'final-paragraphs.json').write_text(json.dumps(paras,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Stale metric scan:')
    for p in paras:
        if re.search(r'7000|145,376|16,668|16,664|63,606|Figure\s+4[6-9]|Figure\s+9[789]|76\.0%|31\.4%',p['text']):print(p['i'],p['text'])
    print('Figure captions:')
    for p in paras:
        if re.match(r'^Figure\s+[0-9]+',p['text']) and 'Caption' in p['style']:print(p['i'],p['text'])
    print('Charts:')
    for i,x in enumerate(body):
        chart=x.find('.//c:chart',N)
        if chart is not None:print(i,chart.get('{'+N['r']+'}id'))
    print('Strike count',len(root.xpath('.//w:strike',namespaces=N)))
    print('Highlight colours',set(root.xpath('.//w:highlight/@w:val',namespaces=N)))
