"""Read-only final checks of chart captions and register-code scope disclosure."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as ET
import json
import hashlib
import posixpath
import re

ROOT = Path(r'D:/coding/ugift-data-analysis')
OUT = ROOT/'outputs/narrative-report/reconciliation-06102026'
PATH = OUT.parent/'ugift-working-report-06102026-1344-reconciled.docx'
NS = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'c':'http://schemas.openxmlformats.org/drawingml/2006/chart',
      'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

with ZipFile(PATH) as archive:
    document = ET.fromstring(archive.read('word/document.xml'))
    rels = ET.fromstring(archive.read('word/_rels/document.xml.rels'))
    parts = {r.get('Id'):posixpath.normpath('word/'+r.get('Target')) for r in rels}
    body = list(document.find('w:body',NS))
    captions = []
    for index, element in enumerate(body):
        charts = element.findall('.//c:chart',NS)
        for chart in charts:
            following = next((b for b in body[index+1:] if ''.join(b.xpath('.//w:t/text()',namespaces=NS)).strip()),None)
            text = ''.join(following.xpath('.//w:t/text()',namespaces=NS))
            pstyle = following.find('w:pPr/w:pStyle',NS)
            style = pstyle.get('{'+NS['w']+'}val') if pstyle is not None else None
            captions.append({'part':parts[chart.get('{'+NS['r']+'}id')], 'next_text':text,'style':style,
                             'caption_immediately_below':bool(re.match(r'^Figure\s+\d+\s*:',text) and style=='Caption')})
    paragraphs = [''.join(p.xpath('.//w:t/text()',namespaces=NS)) for p in document.findall('.//w:body/w:p',NS)]
    scope = next(p for p in paragraphs if p.startswith('The condition descriptions in section 2.5'))
    figure2 = next(c for c in captions if re.match(r'^Figure\s+2\s*:',c['next_text']))
    figure46 = next(c for c in captions if re.match(r'^Figure\s+46\s*:',c['next_text']))
    result = {'report_sha256':hashlib.sha256(PATH.read_bytes()).hexdigest(), 'native_chart_count':len(captions),
              'all_native_captions_immediately_below':all(c['caption_immediately_below'] for c in captions),
              'caption_failures':[c for c in captions if not c['caption_immediately_below']],
              'figure2_caption':figure2['next_text'], 'figure46_caption':figure46['next_text'],
              'appendixC_scope':scope,
              'scope_pass':all(s in scope for s in ['215,504','13,520','usable stored or uninstalled','does not represent a count of physically broken assets']),
              'captions':captions}
(OUT/'final-scope-caption-validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='captions'},indent=2,ensure_ascii=False))
