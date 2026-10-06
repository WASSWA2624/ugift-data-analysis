from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import re,json,hashlib,difflib
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def tx(e):return ''.join(e.xpath('.//w:t/text()',namespaces=ns))
def norm(s):return re.sub(r'\s+',' ',s).strip()
def read(path):
 z=ZipFile(path);b=E.fromstring(z.read('word/document.xml')).find('w:body',ns);out=[]
 for i,e in enumerate(b):
  text=norm(tx(e));prior=norm(''.join(tx(r) for r in e.xpath('.//w:r',namespaces=ns) if not r.xpath('./w:rPr/w:highlight[@w:val="green"]',namespaces=ns)))
  out.append({'i':i,'text':text,'prior':prior,'style':e.xpath('./w:pPr/w:pStyle/@w:val',namespaces=ns),'kind':E.QName(e).localname})
 return out
fp=P.parent/'ugift-working-report-06102026-1344-reconciled.docx'
o=read(P.parent/'ugift-working-report-06102026-1344.docx');f=read(fp)
def mark(bs,s):return next(x['i'] for x in bs if x['style'] and x['style'][0].startswith('Heading') and x['text'].startswith(s))
os=mark(o,'1 Introduction');oe=mark(o,'3.3 MDA specific');fs=mark(f,'1 Introduction');fe=mark(f,'3.3 MDA specific');offset=fs-os
changes=[];same=[]
for p in o[os:oe]:
 if p['kind']!='p' or not p['text']:continue
 base=p['prior'] or p['text'];caption=re.match(r'^(Figure|Table)\s+(\d+):',base,re.I)
 if caption:
  options=[q for q in f[fs:fe] if q['text'].startswith(caption.group(1)+' '+caption.group(2)+':')]
 else:
  options=[q for q in f[fs:fe] if q['text']==base]
 final=min(options,key=lambda q:abs(q['i']-(p['i']+offset))) if options else f[p['i']+offset]
 rec={'original_i':p['i'],'final_i':final['i'],'original_text':base,'final_text':final['text'],'inline_green_removed':p['text']!=base,'entirely_green_source':not p['prior']}
 if base!=final['text']:
  seq=difflib.SequenceMatcher(a=base.split(),b=final['text'].split(),autojunk=False)
  rec['word_changes']=[{'operation':tag,'original':' '.join(base.split()[a:b]),'final':' '.join(final['text'].split()[c:d])} for tag,a,b,c,d in seq.get_opcodes() if tag!='equal']
  changes.append(rec)
 else:same.append({'original_i':p['i'],'final_i':final['i']})
out={'sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'range':'Sections 1 through and including 3.2','unchanged_paragraphs':same,'changed_paragraphs':changes}
(P/'final-protected-wording-differences.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'sha256':out['sha256'],'unchanged_count':len(same),'changed_paragraphs':changes},indent=2,ensure_ascii=False))
