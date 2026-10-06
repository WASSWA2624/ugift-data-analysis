import json,re
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
d=json.loads((P/'structure-audit.json').read_text(encoding='utf-8'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for key in ['baseline','current']:
 z=ZipFile(d[key]['file']);body=E.fromstring(z.read('word/document.xml')).find('w:body',ns)
 for b,el in zip(d[key]['blocks'],body):
  runs=[]
  for run in el.xpath('.//w:r',namespaces=ns):
   text=''.join(run.xpath('.//w:t/text()',namespaces=ns))
   col=run.xpath('./w:rPr/w:highlight/@w:val',namespaces=ns)
   strike=bool(run.xpath('./w:rPr/w:strike[not(@w:val="0")]',namespaces=ns))
   runs.append({'text':text,'highlight':col[0] if col else None,'strike':strike})
  b['runs']=runs
  b['accepted_text']=''.join(r['text'] for r in runs if r['highlight']!='red' and not r['strike'])
  b['prior_text']=''.join(r['text'] for r in runs if r['highlight']!='green')
  b['green_text']=''.join(r['text'] for r in runs if r['highlight']=='green')
  b['red_text']=''.join(r['text'] for r in runs if r['highlight']=='red')
  b['green_share_of_accepted']=len(b['green_text'].strip())/len(b['accepted_text'].strip()) if b['accepted_text'].strip() else None
  b['green_runs']=sum(1 for r in runs if r['highlight']=='green')

fullgreen=[];partial=[]
for b in d['current']['blocks']:
 if b['green_runs']:
  if b['green_share_of_accepted'] is not None and b['green_share_of_accepted']>.97:fullgreen.append(b['index'])
  else:partial.append(b['index'])
d['highlight_inventory']={'wholly_green_blocks':fullgreen,'partial_green_blocks':partial,'recommended_whole_added_sections':[
 {'name':'Executive summary','current_start':44,'current_end_exclusive':50,'reason':'All new executive-summary narrative is green; heading unhighlighted.'},
 {'name':'Priority actions','current_start':51,'current_end_exclusive':57,'reason':'All heading and narrative text green.'},
 {'name':'3.4.1 Arua Regional Blood Bank','current_start':354,'current_end_exclusive':361,'reason':'Heading title and all content newly added; section number not green.'},
 {'name':'3.4.2 Hoima Regional Blood Bank','current_start':361,'current_end_exclusive':368,'reason':'Heading title and all content newly added; section number not green.'},
 {'name':'3.4.3 Soroti Regional Blood Bank','current_start':368,'current_end_exclusive':375,'reason':'Heading title and all content newly added; section number not green.'},
 {'name':'5.1 Actions to address the reported service gaps','current_start':505,'current_end_exclusive':508,'reason':'Heading title, text and table newly added.'},
 {'name':'Appendices A-K','current_start':509,'current_end_exclusive':627,'reason':'Entire appendix sections are added material; prefix letters sometimes unhighlighted.'}
]}
d['restoration_plan']=[
 {'archived_base_index':645,'asset':'word/charts/chart1.xml','counterpart_current_index':151,'caption_current_index':150,'title':'Figure 1: Distribution of assets','action':'Current corrected image present. If native structure is requested restore native chart in place of image and update cache/embedded worksheet to register institution totals; do not add duplicate.'},
 {'archived_base_index':726,'asset':'word/charts/chart5.xml','counterpart_current_index':162,'caption_current_index':161,'title':'Figure 2: Reasons for equipment not in use','action':'Current corrected image present; interview-reasons data are not in MF asset register. Preserve verified interview denominator and counts, use original layout only.'},
 {'archived_base_index':647,'asset':'word/charts/chart2.xml','counterpart_current_index':172,'caption_current_index':171,'title':'Figure 3: Asset marking and Identification','action':'Current corrected image present. Original uses engraved vs properly engraved overlapping series; update to tag contains UgIFT/other identifier/no usable tag and state correct denominator if reusing chart.'},
 {'archived_base_index':649,'asset':'word/charts/chart3.xml','counterpart_current_index':187,'caption_current_index':186,'title':'Figure 4: Assets available at verified MDAs','action':'Current corrected image present; use corrected MDA counts. Caption currently above graph; move below.'},
 {'archived_base_index':651,'asset':'word/charts/chart4.xml','counterpart_current_index':193,'caption_current_index':192,'title':'Figure 5: Asset marking and Identification at MDAs','action':'Current corrected image present; original marking values wrong. Update to register tag fields before restoring.'},
 {'archived_base_index':740,'asset':'word/media/image98.png','title':'Soroti Blood bank','insertion':'current blood-bank photo table body376, before section3.5 body377','action':'Restore only after identifying scene/label from image; image had been removed to revision record as deleted photograph.'},
 {'archived_base_index':742,'asset':'word/media/image99.png','title':'Blood bank refrigerator Soroti Blood bank','insertion':'current blood-bank photo table body376, before section3.5 body377','action':'Restore unchanged photograph with supplied caption, unless it duplicates a retained image.'},
 {'archived_base_index':637,'title':'Appendix L Responses to reviewer comments','insertion':'after current Appendix K ending body626','action':'Wholly new baseline appendix omitted in current. Can restore section/summary table with green new-section highlight if user intends all deleted tables to return. Its disposition text refers to current corrected data and must be checked.'},
 {'archived_base_index':142,'title':'Service-date exceptions methodology table','insertion':'baseline2.6.1 Review of service dates block140, current2.6 financial methodology body134','action':'Removed with service-date methodology subsection before3.2; do not restore automatically because user explicitly says preserve current content before3.2 except metrics.'}
]

base=d['baseline']['blocks'];cur=d['current']['blocks']
archive_tables=[]
for b in base[638:]:
 if b['kind']=='tbl':
  title=base[b['index']-1]['text']
  # closest current table via header/content similarity is unreliable for differently classified categories.
  archive_tables.append({'baseline_index':b['index'],'label':title,'rows':len(b['rows']),'headers':b['rows'][0],'action':'Reuse original table structure with reconciled values at corresponding main-report location; do not append superseded figures as findings.'})
d['archived_table_inventory']=archive_tables
(P/'structure-audit.json').write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf-8')
lines=[
 'STRUCTURE AUDIT AND RESTORATION PLAN',
 'Baseline0000: 744 body blocks,94 tables,100 image occurrences,5 native charts.',
 'Current1344: 628 body blocks,73 tables,79 image occurrences,0 native charts.',
 'Section3.2 boundary: current body index182; baseline index190 (zero-based body-child indices).',
 'All79 main-report image occurrences remain in current. Missing visual objects are archived superseded graphs and two deleted photographs, not empty main graph slots.',
 'Twenty superseded/reviewer appendix tables were removed at end plus one service-date methodology table before3.2. Current table1 was replaced with old school-condition table; metrics/category definitions conflict with narrative and must be reconciled.',
 'Do not append old superseded archive with outdated numbers. Restore valid original structure at corresponding main section and update all values.',
 '', 'WHOLE NEW SECTIONS TO KEEP GREEN',
 *[f"{s['current_start']}-{s['current_end_exclusive']-1}: {s['name']} ({s['reason']})" for s in d['highlight_inventory']['recommended_whole_added_sections']],
 '', 'NATIVE CHARTS',
 *[json.dumps(c,ensure_ascii=False) for c in d['native_chart_inventory']],
 '', 'RESTORATION PLAN',
 *[json.dumps(c,ensure_ascii=False) for c in d['restoration_plan']],
 '', 'ARCHIVED TABLES',
 *[json.dumps(c,ensure_ascii=False) for c in archive_tables],
 '', 'PARTIAL GREEN BLOCK INDICES',str(partial),
 '', 'CURRENT HEADINGS AND BLOCKS',
 *[f"{b['index']:04}: {b['kind']} {b['accepted_text']}" for b in cur]
]
(P/'structure-audit.txt').write_text('\n'.join(lines),encoding='utf-8')
print('\n'.join(lines[:30]))
