from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json

P = Path(__file__).resolve().parent
N = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
starts = ['Increase the adequacy', 'Improve the equity', 'Strengthen performance', 'Expand access']
out = {}
for name in ['ugift-working-report-06102026-1344.docx', 'ugift-working-report-06102026-0000.docx', 'ugift-working-report-06102026-1344-reconciled.docx']:
    with ZipFile(P.parent / name) as z:
        root = E.fromstring(z.read('word/document.xml'))
        numbering = E.fromstring(z.read('word/numbering.xml'))
        paras = []
        for p in root.xpath('.//w:body/w:p', namespaces=N):
            text = ''.join(p.xpath('.//w:t/text()', namespaces=N))
            if not any(text.startswith(start) for start in starts):
                continue
            props = p.find('w:pPr', N)
            num_id = p.xpath('./w:pPr/w:numPr/w:numId/@w:val', namespaces=N)
            abstract = []
            if num_id:
                num = numbering.xpath('./w:num[@w:numId=$v]', namespaces=N, v=num_id[0])[0]
                aid = num.find('w:abstractNumId', N).get('{'+N['w']+'}val')
                abstract = [E.tostring(num).decode(), E.tostring(numbering.xpath('./w:abstractNum[@w:abstractNumId=$v]', namespaces=N, v=aid)[0]).decode()]
            paras.append({'text': text, 'pPr': E.tostring(props).decode() if props is not None else None, 'numbering': abstract})
        out[name] = paras
(P/'objective-numbering-audit.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
for name, rows in out.items():
    print(name)
    for row in rows:
        pr=E.fromstring(row['pPr']) if row['pPr'] else None
        print(row['text'][:30], E.tostring(pr).decode() if pr is not None else '')
        if row['numbering']:
            abstract=E.fromstring(row['numbering'][1])
            print([(l.get('{'+N['w']+'}ilvl'), l.find('w:numFmt',N).get('{'+N['w']+'}val'), l.find('w:lvlText',N).get('{'+N['w']+'}val')) for l in abstract.findall('w:lvl',N)])
