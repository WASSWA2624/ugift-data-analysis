from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import re,json,hashlib
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
fp=P.parent/'ugift-working-report-06102026-1344-reconciled.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def tx(e):return ''.join(e.xpath('.//w:t/text()',namespaces=ns))
def norm(s):return re.sub(r'\s+',' ',s).strip()
z=ZipFile(fp);b=E.fromstring(z.read('word/document.xml')).find('w:body',ns)
blocks=[]
for i,e in enumerate(b):
 style=e.xpath('./w:pPr/w:pStyle/@w:val',namespaces=ns)
 blocks.append({'i':i,'kind':E.QName(e).localname,'text':tx(e),'style':style,'page_break_before':e.xpath('./w:pPr/w:pageBreakBefore/@w:val',namespaces=ns) or bool(e.find('w:pPr/w:pageBreakBefore',ns) is not None),'explicit_page_breaks':len(e.xpath('.//w:br[@w:type="page"]',namespaces=ns)),'section_breaks':len(e.xpath('.//w:sectPr',namespaces=ns)),'section_types':e.xpath('.//w:sectPr/w:type/@w:val',namespaces=ns),'last_rendered_page_breaks':len(e.xpath('.//w:lastRenderedPageBreak',namespaces=ns)),'table_rows':[[tx(c) for c in r.findall('w:tc',ns)] for r in e.findall('w:tr',ns)],'chart_ids':e.xpath('.//c:chart/@r:id',namespaces=ns),'image_ids':e.xpath('.//a:blip/@r:embed',namespaces=ns)})
start=next(x['i'] for x in blocks if x['style'] and x['style'][0].startswith('Heading') and norm(x['text'])=='Appendix L Responses to reviewer comments')
main_start=next(x['i'] for x in blocks if x['style'] and x['style'][0].startswith('Heading') and norm(x['text'])=='Executive summary')
def fmt(e):
 n=E.QName(e).localname
 if n in ['lastRenderedPageBreak','bookmarkStart','bookmarkEnd','proofErr','commentRangeStart','commentRangeEnd','commentReference']:return None
 attrs={E.QName(k).localname:v for k,v in e.attrib.items() if not E.QName(k).localname.startswith('rsid') and E.QName(k).localname not in ['paraId','textId']}
 children=[s for c in e if (s:=fmt(c)) is not None]
 return [n,attrs,e.text,children]
inventory=[]
for i in range(main_start,start):
 e=b[i];inventory.append({'i':i,'kind':E.QName(e).localname,'text':tx(e),'table_rows':blocks[i]['table_rows'],'semantic_format':fmt(e)})
out={'source_sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'main_body_start':main_start,'appendix_l_start':start,'body_blocks_count':len(blocks),'preceding_and_appendix_blocks':blocks[max(start-8,0):],'appendix_l_xml':[{'i':i,'xml':E.tostring(b[i]).decode()} for i in range(start,len(b))],'preserved_main_body_inventory':inventory,'document_final_section_xml':E.tostring(b[-1]).decode()}
(P/'appendix-l-removal-baseline.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k not in ['appendix_l_xml','preserved_main_body_inventory','document_final_section_xml']},indent=2,ensure_ascii=False))
print('FINAL SECTION',E.tostring(b[-1]).decode())
