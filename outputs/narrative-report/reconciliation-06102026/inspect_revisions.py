from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import json
BASE=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def text(el):return ''.join(el.xpath('.//w:t/text()',namespaces=NS))
with ZipFile(BASE/'ugift-working-report-06102026-1344.docx') as z:
    root=etree.fromstring(z.read('word/document.xml'))
    body=root.find('w:body',NS)
    rows=[]
    for i,el in enumerate(body):
        if etree.QName(el).localname!='p':continue
        runs=el.xpath('.//w:r',namespaces=NS)
        nongreen=''.join(text(r) for r in runs if not r.xpath('./w:rPr/w:highlight[@w:val="green"]',namespaces=NS))
        green=''.join(text(r) for r in runs if r.xpath('./w:rPr/w:highlight[@w:val="green"]',namespaces=NS))
        style=el.xpath('./w:pPr/w:pStyle/@w:val',namespaces=NS)
        revised=''.join(text(r) for r in runs if not r.xpath('./w:rPr/w:strike[not(@w:val="0")]',namespaces=NS))
        rows.append({'i':i,'style':style,'original':nongreen,'green':green,'revised':revised,'full':text(el)})
    (OUT/'revision-paragraphs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'original-prose.txt').write_text('\n'.join(f"P{r['i']} {','.join(r['style'])} {'NEW' if not r['original'].strip() and r['green'].strip() else ''} {r['original'] or r['green']}" for r in rows),encoding='utf-8')
    print('mixed',sum(bool(r['green'].strip() and r['original'].strip()) for r in rows))
    (OUT/'revised-prose.txt').write_text('\n'.join(f"P{r['i']} {','.join(r['style'])} {'NEW' if not r['original'].strip() and r['green'].strip() else ''} {r['revised']}" for r in rows),encoding='utf-8')
    (OUT/'mixed-pairs.txt').write_text('\n'.join(f"P{r['i']}\nORIGINAL {r['original']}\nREVISED {r['revised']}\n" for r in rows if r['green'].strip() and r['original'].strip()),encoding='utf-8')
