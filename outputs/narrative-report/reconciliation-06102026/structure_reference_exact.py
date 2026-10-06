from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,hashlib,re
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
plan=json.loads((P/'figure-table-reference-corrections.json').read_text(encoding='utf-8'))
fp=Path(plan['source_file']);z=ZipFile(fp);ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
body=E.fromstring(z.read('word/document.xml')).find('w:body',ns)
raw={i:''.join(el.xpath('.//w:t/text()',namespaces=ns)) for i,el in enumerate(body)}
norm=lambda s:re.sub(r'\s+',' ',s).strip()
paragraphs={};flat=[]
for i,v in plan['corrections'].items():
 i=int(i)
 if norm(raw[i])!=v['old_text']:raise ValueError(f'Source changed at {i}')
 entry={'text':v['text'],'rationale':v['rationale'],'body_index_at_audit':i,'protected':False,'preceding_exact_text':raw[i-1]}
 flat.append({'exact_old_text':raw[i],**entry})
 if raw[i] in paragraphs:
  existing=paragraphs[raw[i]]
  paragraphs[raw[i]]={'occurrences':existing.get('occurrences',[existing])+[entry]}
 else:paragraphs[raw[i]]=entry

# Table2's MDA row includes NBV coverage16,567/16,663 and starred available-only costs/depreciation/NBV;
# its explanatory note identifies missing/pending amounts, so this replacement is supported.
i=290
old=raw[i]
new=old.replace('The table below gives the category breakdown and identifies any unavailable amounts.','Table 2 also identifies unavailable amounts.')
if new==old:raise ValueError('Protected dangling reference text not found')
paragraphs[old]={'text':new,'rationale':'Metric-reconciliation reference correction only: Table2 flags available-only amounts and MDA NBV coverage; no aggregate category table follows this paragraph.','body_index_at_audit':i,'protected':True}
flat.append({'exact_old_text':old,**paragraphs[old]})

table_captions={}
for v in plan['proposed_new_caption_assignments']:
 i=v['table_body_index'];r=body[i].find('w:tr',ns)
 headers=[''.join(c.xpath('.//w:t/text()',namespaces=ns)) for c in r.findall('w:tc',ns)]
 table_captions[raw[i]]={'caption':v['caption'],'number':v['number'],'placement':'immediately_above','highlight':'green','body_index_at_audit':i,'headers':headers,'prior_paragraph_exact_text':raw[i-1]}

insertions=[]
for v in plan['proposed_insertions']:
 i=v['before_body_index'];insertions.append({'before_exact_table_text':raw[i],'text':v['text'],'highlight':'green','body_index_at_audit':i})

out={'source_file':str(fp),'source_sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'paragraph_corrections_by_exact_old_text':paragraphs,'paragraph_corrections':flat,'table_caption_insertions_by_exact_table_text':table_captions,'paragraph_insertions':insertions,'protected_reference_validation':{'actual_section3_2_heading_index':277,'actual_section3_3_heading_index':291,'protected_paragraph_exact_text':old,'replacement_sentence':'Table 2 also identifies unavailable amounts.','table2_MDA_row':'Ministries and agencies16,663 records; NBV16,567/16,66332,054.744*19,787.511*10,265.925*34.2%','support':'Table2 amounts carry available-only asterisks; its note says one or more amounts are missing or pending calculation and displays NBVcoverage.'},'notes':['Keys are exact concatenated w:t text from latestfinal DOCX. Resolve exact matches before mutating because newcaptions shiftindices.','One repeated photograph-intro text occurs twice (HealthCentres502 andSchools539), with different Figure ranges. For this key read occurrences array and usepreceding_exact_text or body_index_at_audit. Flatparagraph_corrections has44entries.','Insert Table35-68 captions in green; all belong to retained newsections5.1 orAppendicesA-L.','The protected section3.2 change is only the financial table reference, as explicitly authorized byparent metric-reconciliation instruction. Otherprotectedsections1-through3.2prose remains untouched.','Seven photograph-layouttables are referenced as figure ranges, not numbered as datatables.','Appendices mainheading exactoldtext Annexures Appendices is replaced withAppendices.'], 'counts':{'paragraph_corrections':len(flat),'unique_old_text_keys':len(paragraphs),'new_table_captions':len(table_captions),'inserted_paragraphs':len(insertions)}}
(P/'figure-table-reference-exact.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out['counts']))
print(json.dumps(out['protected_reference_validation'],ensure_ascii=False))
