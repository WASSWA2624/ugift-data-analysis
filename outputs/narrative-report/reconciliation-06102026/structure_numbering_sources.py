from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
out=[]
for name in ['ugift-working-report-06102026-0000.docx','ugift-working-report-06102026-1344.docx','UgIFT Asset Verification Report - Updated.docx','UgIFT Asset Verification Report-Draft 01-10-2026.docx','UgIFT Asset Verification Report.docx']:
 z=ZipFile(P/name);d=E.fromstring(z.read('word/document.xml'));num=E.fromstring(z.read('word/numbering.xml'));res=[]
 for p in d.xpath('.//w:p',namespaces=ns):
  text=''.join(p.xpath('.//w:t/text()',namespaces=ns))
  if text.startswith('Increase the adequacy') or text.startswith('Improve the equity') or text.startswith('Strengthen performance') or text.startswith('Expand access'):
   ids=p.xpath('./w:pPr/w:numPr/w:numId/@w:val',namespaces=ns);levels=p.xpath('./w:pPr/w:numPr/w:ilvl/@w:val',namespaces=ns)
   if ids and num.xpath('./w:num[@w:numId="'+ids[0]+'"]',namespaces=ns):
    ne=num.xpath('./w:num[@w:numId="'+ids[0]+'"]',namespaces=ns)[0];aid=ne.xpath('./w:abstractNumId/@w:val',namespaces=ns)[0];ae=num.xpath('./w:abstractNum[@w:abstractNumId="'+aid+'"]',namespaces=ns)[0];lv=ae.xpath('./w:lvl[@w:ilvl="'+(levels[0] if levels else '0')+'"]',namespaces=ns)[0]
    rec={'text':text,'numId':ids[0],'abstractNumId':aid,'ilvl':levels[0] if levels else '0','numFmt':lv.xpath('./w:numFmt/@w:val',namespaces=ns),'lvlText':lv.xpath('./w:lvlText/@w:val',namespaces=ns),'pPr_xml':E.tostring(p.find('w:pPr',ns)).decode(),'num_xml':E.tostring(ne).decode(),'abstract_xml':E.tostring(ae).decode()}
   else:rec={'text':text,'numId':ids[0] if ids else None,'definition_missing':bool(ids),'pPr_xml':E.tostring(p.find('w:pPr',ns)).decode() if p.find('w:pPr',ns) is not None else None}
   res.append(rec)
 out.append({'file':name,'objectives':res})
print(json.dumps([{'file':x['file'],'objectives':[{k:y.get(k) for k in ['text','numId','abstractNumId','ilvl','numFmt','lvlText']} for y in x['objectives']]} for x in out],indent=2))
(P/'reconciliation-06102026'/'protected-numbering-source-history.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
