from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json, difflib, re, posixpath, hashlib

ROOT=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report')
OUT=ROOT/'reconciliation-06102026'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing','v':'urn:schemas-microsoft-com:vml'}
def tx(el): return ''.join(el.xpath('.//w:t/text()',namespaces=NS))
def audit(name):
 p=ROOT/name
 z=ZipFile(p)
 d=E.fromstring(z.read('word/document.xml'))
 rels={r.get('Id'): {'target':r.get('Target'),'type':r.get('Type')} for r in E.fromstring(z.read('word/_rels/document.xml.rels'))}
 body=d.find('w:body',NS)
 blocks=[]
 tableidx=0
 for i,el in enumerate(body):
  kind=E.QName(el).localname
  b={'index':i,'kind':kind,'text':tx(el)}
  if kind=='p':
   b['style']=el.xpath('./w:pPr/w:pStyle/@w:val',namespaces=NS)
   b['highlights']=[]
   for run in el.xpath('.//w:r',namespaces=NS):
    vals=run.xpath('./w:rPr/w:highlight/@w:val',namespaces=NS)
    if vals:b['highlights'].append({'val':vals[0],'text':tx(run)})
   total=len(b['text'].strip())
   hi=len(''.join(h['text'] for h in b['highlights']).strip())
   b['highlight_share']=hi/total if total else None
  elif kind=='tbl':
   tableidx+=1;b['table_index']=tableidx
   b['rows']=[[tx(c) for c in r.findall('w:tc',NS)] for r in el.findall('w:tr',NS)]
  images=el.xpath('.//a:blip/@r:embed | .//v:imagedata/@r:id',namespaces=NS)
  charts=el.xpath('.//c:chart/@r:id',namespaces=NS)
  b['images']=[dict(id=x,**rels.get(x,{})) for x in images]
  b['charts']=[dict(id=x,**rels.get(x,{})) for x in charts]
  b['docprs']=[dict(n.attrib) for n in el.xpath('.//wp:docPr',namespaces=NS)]
  blocks.append(b)
 parts=[{'name':n,'size':len(z.read(n)),'sha256':hashlib.sha256(z.read(n)).hexdigest()} for n in z.namelist() if n.startswith('word/media/') or n.startswith('word/charts/') or n.startswith('word/embeddings/')]
 a={'file':str(p),'blocks':blocks,'parts':parts,'relationships':rels,'counts':{'body_blocks':len(blocks),'tables':tableidx,'image_occurrences':sum(len(b['images']) for b in blocks),'chart_occurrences':sum(len(b['charts']) for b in blocks)}}
 return a

base=audit('ugift-working-report-06102026-0000.docx');cur=audit('ugift-working-report-06102026-1344.docx')
sm=difflib.SequenceMatcher(a=[b['kind']+':'+b['text'] for b in base['blocks']],b=[b['kind']+':'+b['text'] for b in cur['blocks']],autojunk=False)
ops=[]
for tag,ai,aj,bi,bj in sm.get_opcodes():
 if tag!='equal':ops.append({'tag':tag,'base_range':[ai,aj],'current_range':[bi,bj]})
report={'baseline':base,'current':cur,'sequence_changes':ops}
(OUT/'structure-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
lines=[]
for key,a in [('BASELINE',base),('CURRENT',cur)]:
 lines+=[key+' '+json.dumps(a['counts'])]
 for b in a['blocks']:
  t=b['text']
  if b['kind']=='tbl':lines.append(f"{b['index']:04} TABLE {b['table_index']} rows={len(b['rows'])} "+str(b['rows'][:2]))
  elif b['images'] or b['charts']:lines.append(f"{b['index']:04} VISUAL "+json.dumps({'text':t,'images':b['images'],'charts':b['charts'],'docprs':b['docprs']},ensure_ascii=False))
  else:lines.append(f"{b['index']:04} "+('HI '+str(b['highlight_share'])+' ' if b.get('highlights') else '')+t)
 lines+=['']
lines+=['CHANGES '+json.dumps(ops)]
(OUT/'structure-audit.txt').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'baseline':base['counts'],'current':cur['counts'],'changes':ops},indent=2))
