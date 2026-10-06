from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import re,json,hashlib
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
oldpath=P/'final-structure-preservation-audit.json'
baseline=P/'appendix-l-removal-baseline.json'
if not baseline.exists():baseline.write_bytes(oldpath.read_bytes())
old=json.loads(baseline.read_text(encoding='utf-8'))
assert old['final_sha256']=='167911fcdfddb87f069628c94584e3ffc0a7a39d976dd84384cf6aa3675901b7'
fp=P.parent/'ugift-working-report-06102026-1344-reconciled.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def tx(e):return ''.join(e.xpath('.//w:t/text()',namespaces=ns))
def norm(s):return re.sub(r'\s+',' ',s).strip()
z=ZipFile(fp);body=E.fromstring(z.read('word/document.xml')).find('w:body',ns);new=[]
for i,e in enumerate(body):
 x={'i':i,'kind':E.QName(e).localname,'text':tx(e),'style':e.xpath('./w:pPr/w:pStyle/@w:val',namespaces=ns),'green':[],'red':[],'otherhighlight':[],'strike':[],'images':e.xpath('.//a:blip/@r:embed',namespaces=ns),'charts':e.xpath('.//c:chart/@r:id',namespaces=ns),'rows':[[tx(c) for c in r.findall('w:tc',ns)] for r in e.findall('w:tr',ns)] if E.QName(e).localname=='tbl' else None}
 for r in e.xpath('.//w:r',namespaces=ns):
  text=tx(r);cols=r.xpath('./w:rPr/w:highlight/@w:val',namespaces=ns);col=cols[0] if cols else None
  if col in ['green','red']:x[col].append(text)
  elif col and col!='none':x['otherhighlight'].append({'color':col,'text':text})
  if r.xpath('./w:rPr/w:strike[not(@w:val="0")]|./w:rPr/w:dstrike[not(@w:val="0")]',namespaces=ns):x['strike'].append(text)
 new.append(x)
ob=old['body_blocks'];oi=next(x['i'] for x in ob if x['style'] and x['style'][0].startswith('Heading') and norm(x['text'])=='Executive summary');oj=next(x['i'] for x in ob if x['style'] and x['style'][0].startswith('Heading') and norm(x['text'])=='Appendix L Responses to reviewer comments');ni=next(x['i'] for x in new if x['style'] and x['style'][0].startswith('Heading') and norm(x['text'])=='Executive summary')
before=ob[oi:oj];after=[x for x in new[ni:] if x['kind']!='sectPr'];changes=[]
fields=['kind','text','style','images','charts','rows','otherhighlight']
for k,(a,b) in enumerate(zip(before,after)):
 diff={f:{'before':a.get(f),'after':b.get(f)} for f in fields if a.get(f)!=b.get(f)}
 for f in ['green','red','strike']:
  if ''.join(a.get(f,[]))!=''.join(b.get(f,[])):diff[f]={'before':a.get(f),'after':b.get(f)}
 if diff:changes.append({'baseline_i':a['i'],'final_i':b['i'],'changes':diff})
trailing=[]
for i in range(max(len(body)-5,0),len(body)):
 e=body[i];trailing.append({'i':i,'kind':E.QName(e).localname,'text':tx(e),'page_break_before':e.find('w:pPr/w:pageBreakBefore',ns) is not None,'explicit_page_breaks':len(e.xpath('.//w:br[@w:type="page"]',namespaces=ns)),'paragraph_section_breaks':len(e.xpath('./w:pPr/w:sectPr',namespaces=ns)),'pPr_xml':E.tostring(e.find('w:pPr',ns)).decode() if e.find('w:pPr',ns) is not None else None})
section=body[-1]
out={'baseline_sha256':old['final_sha256'],'final_sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'baseline_actual_appendix_l_heading_index':oj,'baseline_removed_blocks':[{'i':x['i'],'kind':x['kind'],'text':x['text']} for x in ob[oj:] if x['kind']!='sectPr'],'baseline_preserved_main_blocks':len(before),'final_preserved_main_blocks':len(after),'preserved_main_body_changes':changes,'main_body_exactly_preserved':len(before)==len(after) and not changes,'appendix_l_and_table68_absent_everywhere':not any(re.search(r'Appendix\s+L|Table\s+68\b',x['text'],re.I) for x in new),'final_section_properties_retained':E.QName(section).localname=='sectPr','final_section_type':section.xpath('./w:type/@w:val',namespaces=ns),'final_section_xml':E.tostring(section).decode(),'trailing_blocks':trailing,'trailing_explicit_page_break':any(x['explicit_page_breaks'] or x['paragraph_section_breaks'] or x['page_break_before'] for x in trailing if x['kind']=='p'),'counts':{'baseline_tables':old['counts']['tables'],'final_tables':sum(x['kind']=='tbl' for x in new),'final_native_charts':sum(len(x['charts']) for x in new),'final_images':sum(len(x['images']) for x in new)}}
(P/'appendix-l-removal-verification.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k not in ['baseline_removed_blocks','final_section_xml','trailing_blocks']},indent=2,ensure_ascii=False))
