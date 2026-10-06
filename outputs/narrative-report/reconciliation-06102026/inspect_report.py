from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import json

BASE = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

def text(el):
    return ''.join(el.xpath('.//w:t/text()', namespaces=NS))

for name in ['ugift-working-report-06102026-1344.docx', 'ugift-working-report-06102026-0000.docx']:
    with ZipFile(BASE/name) as z:
        root = etree.fromstring(z.read('word/document.xml'))
        body = root.find('w:body',NS)
        rows = []
        for i,el in enumerate(body):
            kind = etree.QName(el).localname
            if kind=='p':
                style = el.xpath('./w:pPr/w:pStyle/@w:val', namespaces=NS)
                highlights = el.xpath('.//w:highlight/@w:val', namespaces=NS)
                green = ''.join(text(r) for r in el.xpath('.//w:r[w:rPr/w:highlight[@w:val="green"]]', namespaces=NS))
                images = el.xpath('.//a:blip/@r:embed', namespaces=NS)
                rows.append({'i':i,'kind':kind,'style':style,'text':text(el),'highlight':highlights,'green':green,'images':images})
            elif kind=='tbl':
                cells = [[text(c) for c in row.findall('w:tc',NS)] for row in el.findall('w:tr',NS)]
                rows.append({'i':i,'kind':kind,'cells':cells})
        stem=Path(name).stem
        (OUT/(stem+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
        lines=[]
        for row in rows:
            if row['kind']=='p':
                lines.append(f"P{row['i']} {','.join(row['style'])} H{','.join(set(row['highlight']))} I{','.join(row['images'])} {row['text']}")
            else:
                lines.append(f"TABLE BLOCK {row['i']} ({len(row['cells'])} rows)")
                lines.extend(' | '.join(r) for r in row['cells'])
        (OUT/(stem+'.txt')).write_text('\n'.join(lines),encoding='utf-8')
        print(name, 'paragraphs',sum(r['kind']=='p' for r in rows),'tables',sum(r['kind']=='tbl' for r in rows),'images',sum(len(r.get('images',[])) for r in rows),'green-paragraphs',sum(bool(r.get('green')) for r in rows))
