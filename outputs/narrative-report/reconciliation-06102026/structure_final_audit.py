from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,re,difflib,hashlib
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def norm(s):return re.sub(r'\s+',' ',s).strip()
def tx(el):return ''.join(el.xpath('.//w:t/text()',namespaces=ns))
def read(p):
 z=ZipFile(p);root=E.fromstring(z.read('word/document.xml'));body=root.find('w:body',ns);bs=[]
 for i,el in enumerate(body):
  t=E.QName(el).localname;b={'i':i,'kind':t,'text':tx(el),'accepted':''}
  b['green']=[];b['red']=[];b['otherhighlight']=[];b['strike']=[]
  for run in el.xpath('.//w:r',namespaces=ns):
   rt=tx(run);cols=run.xpath('./w:rPr/w:highlight/@w:val',namespaces=ns);col=cols[0] if cols else None
   strike=bool(run.xpath('./w:rPr/w:strike[not(@w:val="0")]|./w:rPr/w:dstrike[not(@w:val="0")]',namespaces=ns))
   if col=='green':b['green'].append(rt)
   if col=='red':b['red'].append(rt)
   if col and col not in ['green','red','none']:b['otherhighlight'].append({'color':col,'text':rt})
   if strike:b['strike'].append(rt)
   if col!='red' and not strike:b['accepted']+=rt
  b['style']=el.xpath('./w:pPr/w:pStyle/@w:val',namespaces=ns)
  b['images']=el.xpath('.//a:blip/@r:embed',namespaces=ns)
  b['charts']=el.xpath('.//c:chart/@r:id',namespaces=ns)
  b['rows']=[[tx(c) for c in row.findall('w:tc',ns)] for row in el.findall('w:tr',ns)] if t=='tbl' else None
  bs.append(b)
 return z,bs,root
origpath=P.parent/'ugift-working-report-06102026-1344.docx';finalpath=P.parent/'ugift-working-report-06102026-1344-reconciled.docx'
oz,ob,oroot=read(origpath);fz,fb,froot=read(finalpath)
omark=next(x['i'] for x in ob if x['style'] and x['style'][0].startswith('Heading') and norm(x['accepted']).startswith('3.3 MDA specific'))
fmark=next(x['i'] for x in fb if x['style'] and x['style'][0].startswith('Heading') and norm(x['text']).startswith('3.3 MDA specific'))
ostart=next(x['i'] for x in ob if x['style'] and x['style'][0].startswith('Heading') and norm(x['accepted']).startswith('1 Introduction'))
fstart=next(x['i'] for x in fb if x['style'] and x['style'][0].startswith('Heading') and norm(x['text']).startswith('1 Introduction'))
ot=[norm(x['accepted']) for x in ob[ostart:omark] if x['kind']=='p' and x['accepted'].strip()]
ft=[norm(x['text']) for x in fb[fstart:fmark] if x['kind']=='p' and x['text'].strip()]
ops=[]
for tag,ai,aj,bi,bj in difflib.SequenceMatcher(a=ot,b=ft,autojunk=False).get_opcodes():
 if tag!='equal':ops.append({'operation':tag,'original':ot[ai:aj],'final':ft[bi:bj]})
section=None;greenoutside=[];highlights=[]
for b in fb:
 t=norm(b['text'])
 if b['style'] and (b['style'][0].startswith('Heading') or t=='Executive summary'):
  section=t
 allowed=(section in ['Executive summary','Priority actions','3.4.1 Arua Regional Blood Bank','3.4.2 Hoima Regional Blood Bank','3.4.3 Soroti Regional Blood Bank','4.2 Obsolete and Unserviceable Assets','4.3 Missing and Unrecorded Assets','5.1 Actions to address the reported service gaps'] or (section or '').startswith('Appendix ') or (section or '') in ['Extent of existing cost estimates','Rules for an approved register correction','Principal references','MoFPED','MoWT','MoES','MAAIF','MoH','OPM','MoWE','MoGLSD','NEMA','PPDA','OAG','MoLG','MoLHUD','Arua Regional Blood Bank','Hoima Regional Blood Bank','Soroti Regional Blood Bank','Health centres','Schools'])
 if b['green']:
  highlights.append({'body_index':b['i'],'section':section,'text':t[:200],'green_text':''.join(b['green'])[:200],'allowed':allowed})
  if not allowed:greenoutside.append(highlights[-1])
red=[{'body_index':b['i'],'text':b['red']} for b in fb if b['red']]
strikes=[{'body_index':b['i'],'text':b['strike']} for b in fb if b['strike']]
other=[{'body_index':b['i'],'highlight':b['otherhighlight']} for b in fb if b['otherhighlight']]
rels={el.get('Id'):el.get('Target') for el in E.fromstring(fz.read('word/_rels/document.xml.rels'))}
charts=[]
for b in fb:
 if b['charts']:
  rid=b['charts'][0];part='word/'+rels[rid];cr=E.fromstring(fz.read(part))
  nexttexts=[norm(x['text']) for x in fb[b['i']+1:b['i']+5] if x['kind']=='p' and x['text'].strip()]
  charts.append({'body_index':b['i'],'part':part,'caption_following':nexttexts[0] if nexttexts else None,'title_text':cr.xpath('.//c:title//a:t/text()',namespaces=ns),'caption_below':bool(nexttexts and re.match(r'Figure\s+\d+:',nexttexts[0]))})
headings=[{'body_index':x['i'],'text':norm(x['text']),'style':x['style'][0]} for x in fb if x['style'] and x['style'][0].startswith('Heading')]
headingbad=[x for x in headings if re.match(r'^\d+(\.\d+)*\s+\d+(\.\d+)*\s',x['text']) or re.match(r'^\d+(\.\d+)*$',x['text'])]
audit={'source_file':str(origpath),'final_file':str(finalpath),'final_sha256':hashlib.sha256(finalpath.read_bytes()).hexdigest(),'counts':{'blocks':len(fb),'tables':sum(x['kind']=='tbl' for x in fb),'image_occurrences':sum(len(x['images']) for x in fb),'native_chart_occurrences':len(charts)},'pre3_2_changes':ops,'green_outside_whole_sections':greenoutside,'green_blocks':highlights,'red_highlight':red,'struck_text':strikes,'other_highlights':other,'charts':charts,'headings':headings,'bad_headings':headingbad,'body_blocks':fb}
(P/'final-structure-preservation-audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:audit[k] for k in ['counts','green_outside_whole_sections','red_highlight','struck_text','other_highlights','bad_headings']},indent=2,ensure_ascii=False))
print('CHART CAPTION ERRORS',[(x['body_index'],x['caption_following']) for x in charts if not x['caption_below']])
print('CHART TITLES',[x for x in charts if x['title_text']])
