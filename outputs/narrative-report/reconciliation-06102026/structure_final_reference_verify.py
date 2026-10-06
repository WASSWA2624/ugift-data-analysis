from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from copy import deepcopy
import hashlib,json,re

P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
fp=P.parent/'ugift-working-report-06102026-1344-reconciled.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def tx(e):return ''.join(e.xpath('.//w:t/text()',namespaces=ns))
def norm(s):return re.sub(r'\s+',' ',s).strip()
def read(path):
 z=ZipFile(path);root=E.fromstring(z.read('word/document.xml'));body=root.find('w:body',ns);bs=[]
 for i,e in enumerate(body):
  prior=''.join(tx(r) for r in e.xpath('.//w:r',namespaces=ns) if not r.xpath('./w:rPr/w:highlight[@w:val="green"]',namespaces=ns))
  bs.append({'i':i,'kind':E.QName(e).localname,'text':norm(tx(e)),'prior':norm(prior),'style':e.xpath('./w:pPr/w:pStyle/@w:val',namespaces=ns),'images':e.xpath('.//a:blip/@r:embed',namespaces=ns),'charts':e.xpath('.//c:chart/@r:id',namespaces=ns),'el':e})
 return z,bs
z,bs=read(fp);oz,ob=read(P.parent/'ugift-working-report-06102026-1344.docx')
real_start=next(x['i'] for x in bs if x['style'] and x['style'][0].startswith('Heading') and x['text'].startswith('1 Introduction'))
end=next(x['i'] for x in bs if x['style'] and x['style'][0].startswith('Heading') and x['text'].startswith('3.3 MDA specific'))
oend=next(x['i'] for x in ob if x['style'] and x['style'][0].startswith('Heading') and x['text'].startswith('3.3 MDA specific'))
caps=[]
for x in bs[real_start:]:
 paras=[x['el']] if x['kind']=='p' else x['el'].xpath('.//w:p',namespaces=ns)
 for p in paras:
  text=norm(tx(p));m=re.match(r'^(Figure|Table)\s+(\d+[A-Z]?):',text,re.I)
  if m:caps.append({'i':x['i'],'kind':m.group(1).title(),'number':int(m.group(2)) if m.group(2).isdigit() else m.group(2).upper(),'text':text})
targets={(x['kind'],x['number']):x for x in caps}
duplicates=[]
for k in targets:
 rows=[x for x in caps if (x['kind'],x['number'])==k]
 if len(rows)>1:duplicates.append(rows)
refs=[];vague=[];unlabelled=[]
for x in bs[real_start:]:
 if x['kind']!='p' or re.match(r'^(Figure|Table)\s+\d+[A-Z]?:',x['text'],re.I):continue
 if re.search(r'\b(?:table|figure|graph|chart|photo)s?\s+(?:above|below)|\b(?:above|below|following)\s+(?:table|figure|graph|chart|photo)s?',x['text'],re.I):
  vague.append({'i':x['i'],'protected':x['i']<end,'text':x['text']})
 for m in re.finditer(r'\b(Figures?|Tables?)\s+(\d+[A-Z]?(?:\s*(?:to|–|-|and|,)\s*\d+[A-Z]?)*)',x['text'],re.I):
  kind='Figure' if m.group(1).lower().startswith('figure') else 'Table';expr=m.group(2);nums=[int(n) if n.isdigit() else n.upper() for n in re.findall(r'\d+[A-Z]?',expr,re.I)]
  if len(nums)==2 and all(isinstance(n,int) for n in nums) and re.search(r'\bto\b|–|-',expr):nums=list(range(nums[0],nums[1]+1))
  refs.append({'i':x['i'],'kind':kind,'numbers':nums,'phrase':m.group(0),'protected':x['i']<end,'missing_targets':[n for n in nums if (kind,n) not in targets],'text':x['text']})
for x in bs[real_start:]:
 if x['kind']!='tbl' or x['images']:continue
 prev=next((p for p in reversed(bs[:x['i']]) if p['kind']=='p' and p['text']),None)
 if not prev or not re.match(r'^Table\s+\d+:',prev['text'],re.I):unlabelled.append({'i':x['i'],'preceding':prev['text'] if prev else None,'start':x['text'][:160]})
newcaps=[]
for x in caps:
 if x['kind']=='Table' and x['number']>=35:
  runs=bs[x['i']]['el'].xpath('.//w:r[.//w:t]',namespaces=ns)
  nongreen=[tx(r) for r in runs if tx(r).strip() and not r.xpath('./w:rPr/w:highlight[@w:val="green"]',namespaces=ns)]
  newcaps.append({**x,'nongreen_text':nongreen})
# Word may add transient rsid/namespace attributes while saving. Compare actual formatting elements.
def sem(e,ignore_num=False):
 if e is None:return None
 n=E.QName(e).localname
 if n in ['highlight','strike','dstrike']:return None
 if ignore_num and n=='numId':return None
 attrs={E.QName(k).localname:v for k,v in e.attrib.items() if not E.QName(k).localname.startswith('rsid')}
 children=[s for c in e if (s:=sem(c,ignore_num)) is not None]
 return [n,attrs,children]
prefixes=['Increase the adequacy','Improve the equity','Strengthen performance','Expand access']
format_changes=[];matched=[];unmatched=[]
cor=json.loads((P/'prose-corrections.json').read_text(encoding='utf-8'))
entries=cor.get('corrections',cor.get('entries',[])) if isinstance(cor,dict) else cor
corrected={int(i):norm(r.get('text','')) for i,r in entries.items()} if isinstance(entries,dict) else {r.get('body_index',r.get('i')):norm(r.get('text',r.get('corrected_text',''))) for r in entries}
ostart=next(x['i'] for x in ob if x['style'] and x['style'][0].startswith('Heading') and x['text'].startswith('1 Introduction'))
offset=real_start-ostart
for x in ob:
 if x['i']<ostart or x['i']>=oend or x['kind']!='p' or not x['text']:continue
 base=x['prior'] or x['text']
 ys=[y for y in bs[real_start:end] if y['text']==base]
 if not ys and x['i'] in corrected:ys=[y for y in bs[real_start:end] if y['text']==corrected[x['i']]]
 if not ys:
  candidate=bs[x['i']+offset]
  if candidate['kind']=='p':
   ys=[candidate]
   unmatched.append({'original_i':x['i'],'original_text':x['prior'],'final_i':candidate['i'],'final_text':candidate['text'],'format_checked_by_preserved_position':True})
  else:
   unmatched.append({'original_i':x['i'],'original_text':x['prior'],'format_checked_by_preserved_position':False})
   continue
 y=min(ys,key=lambda r:abs(r['i']-(x['i']+offset)));ign=any(x['prior'].startswith(s) for s in prefixes)
 cm=re.match(r'^(Figure|Table)\s+(\d+):',x['prior'],re.I)
 if cm:
  newcap=targets.get((cm.group(1).title(),int(cm.group(2))))
  if newcap:y=bs[newcap['i']]
 a=sem(x['el'].find('w:pPr',ns),ign);b=sem(y['el'].find('w:pPr',ns),ign)
 rec={'original_i':x['i'],'final_i':y['i'],'text':x['prior'],'format_unchanged':a==b,'authorized_objective_numId_exception':ign}
 matched.append(rec)
 if a!=b:format_changes.append({**rec,'original_pPr':a,'final_pPr':b})
num=json.loads((P/'protected-numbering-audit.json').read_text(encoding='utf-8'))
num_bad=[x for x in num['protected_numbering_changes'] if not any(x['original']['text'].startswith(s) for s in prefixes)]
objok=all(r['final']['numbering']['numFmt']=='lowerLetter' and r['final']['numbering']['lvlText']=='%1)' and r['final']['numbering']['start']=='1' for r in num['objective_paragraphs'])
report={'file':str(fp),'sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'protected_end_body_index':end,'counts':{'caption_figures':sum(x['kind']=='Figure' for x in caps),'caption_tables':sum(x['kind']=='Table' for x in caps),'paragraph_references':len(refs),'new_green_table_captions':len(newcaps),'protected_numbered_paragraphs':num['protected_numbered_paragraphs_count'],'protected_paragraph_formats_matched':len(matched)},'duplicate_captions':duplicates,'missing_reference_targets':[r for r in refs if r['missing_targets']],'vague_references_after3_2':[x for x in vague if not x['protected']],'protected_vague_references_preserved':[x for x in vague if x['protected']],'unlabelled_data_tables':unlabelled,'new_table_numbers':[x['number'] for x in newcaps],'new_table_captions_not_green':[x for x in newcaps if x['nongreen_text']],'objective_a_to_d_verified':objok,'unauthorized_protected_numbering_changes':num_bad,'protected_paragraph_format_changes':format_changes,'unmatched_protected_paragraphs':unmatched,'caption_inventory':caps,'references':refs,'protected_paragraph_format_matches':matched}
(P/'final-reference-preservation-verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
keys=['sha256','counts','duplicate_captions','missing_reference_targets','vague_references_after3_2','unlabelled_data_tables','new_table_numbers','new_table_captions_not_green','objective_a_to_d_verified','unauthorized_protected_numbering_changes','protected_paragraph_format_changes']
print(json.dumps({k:report[k] for k in keys},indent=2,ensure_ascii=False))
