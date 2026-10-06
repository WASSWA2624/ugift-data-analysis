from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,re
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def tx(e):return ''.join(e.xpath('.//w:t/text()',namespaces=ns))
def norm(s):return re.sub(r'\s+',' ',s).strip()
def read(p):
 z=ZipFile(p);root=E.fromstring(z.read('word/document.xml'));num=E.fromstring(z.read('word/numbering.xml')) if 'word/numbering.xml' in z.namelist() else None
 styles=E.fromstring(z.read('word/styles.xml')); stylemap={e.get('{'+ns['w']+'}styleId'):e for e in styles.findall('w:style',ns)}
 paras=[]
 for i,e in enumerate(root.find('w:body',ns)):
  if E.QName(e).localname!='p':continue
  pr=e.find('w:pPr',ns);style=e.xpath('./w:pPr/w:pStyle/@w:val',namespaces=ns)
  il=e.xpath('./w:pPr/w:numPr/w:ilvl/@w:val',namespaces=ns);ids=e.xpath('./w:pPr/w:numPr/w:numId/@w:val',namespaces=ns)
  linked=False
  if not ids and style and style[0] in stylemap:
   st=stylemap[style[0]];ids=st.xpath('./w:pPr/w:numPr/w:numId/@w:val',namespaces=ns);il=st.xpath('./w:pPr/w:numPr/w:ilvl/@w:val',namespaces=ns);linked=bool(ids)
  fmt=None;numxml=None
  if ids and num is not None:
   nums=num.xpath('./w:num[@w:numId="'+ids[0]+'"]',namespaces=ns)
   if nums:
    ne=nums[0];aid=ne.xpath('./w:abstractNumId/@w:val',namespaces=ns)
    ae=num.xpath('./w:abstractNum[@w:abstractNumId="'+aid[0]+'"]',namespaces=ns)[0] if aid else None
    lv=ae.xpath('./w:lvl[@w:ilvl="'+(il[0] if il else '0')+'"]',namespaces=ns) if ae is not None else []
    fmt={'num_id':ids[0],'abstract_num_id':aid[0] if aid else None,'ilvl':il[0] if il else '0','from_style':linked,'level_xml':E.tostring(lv[0]).decode() if lv else None,'num_xml':E.tostring(ne).decode()}
    if lv:
     for name in ['numFmt','lvlText','start','suff','lvlJc']:
      v=lv[0].find('w:'+name,ns);fmt[name]=v.get('{'+ns['w']+'}val') if v is not None else None
     for k in ['left','hanging','firstLine']:
      in_=lv[0].find('w:pPr/w:ind',ns);fmt[k]=in_.get('{'+ns['w']+'}'+k) if in_ is not None else None
  paras.append({'i':i,'text':tx(e),'style':style,'pPr_xml':E.tostring(pr).decode() if pr is not None else None,'numbering':fmt})
 return paras
o=read(P.parent/'ugift-working-report-06102026-1344.docx');f=read(P.parent/'ugift-working-report-06102026-1344-reconciled.docx')
targets=['Increase the adequacy','Improve the equity','Strengthen performance','Expand access']
obj=[]
for start in targets:
 orig=next(x for x in o if norm(x['text']).startswith(start));final=next(x for x in f if norm(x['text']).startswith(start))
 obj.append({'original':orig,'final':final})
end=next(x['i'] for x in o if norm(x['text']).startswith('3.3 MDA specific'))
endf=next(x['i'] for x in f if x['style'] and x['style'][0].startswith('Heading') and norm(x['text']).startswith('3.3 MDA specific'))
changes=[];matched=[]
for x in o:
 if x['i']>=end:continue
 if not x['numbering']:continue
 matches=[y for y in f if y['i']<endf and norm(y['text'])==norm(x['text'])]
 if not matches:changes.append({'original':x,'final':None,'issue':'Original numbered paragraph text notmatched inprotectedrange.'});continue
 y=matches[-1]
 def sem(a):
  n=a['numbering'];return {k:n.get(k) for k in ['ilvl','numFmt','lvlText','start','suff','lvlJc','left','hanging','firstLine']} if n else None
 rec={'original':x,'final':y,'original_semantics':sem(x),'final_semantics':sem(y)}
 matched.append(rec)
 if sem(x)!=sem(y):changes.append(rec)
report={'objective_paragraphs':obj,'protected_numbered_paragraphs_count':len(matched),'protected_numbering_changes':changes,'protected_numbered_paragraphs':matched}
(P/'protected-numbering-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('OBJECTIVES')
for r in obj:print(json.dumps({'original_i':r['original']['i'],'final_i':r['final']['i'],'text':r['final']['text'],'final_numFmt':r['final']['numbering']['numFmt'],'final_lvlText':r['final']['numbering']['lvlText'],'final_start':r['final']['numbering']['start']},ensure_ascii=False))
print('ALLNUMBERINGCHANGES')
for r in changes:print(json.dumps({k:r[k] for k in r if k not in ['original','final']},ensure_ascii=False),r['original']['i'],r['original']['text'],r['final']['i'] if r['final'] else None)
print('MATCHEDCOUNT',len(matched))
