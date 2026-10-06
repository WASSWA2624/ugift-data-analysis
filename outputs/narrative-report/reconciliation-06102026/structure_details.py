import json
from pathlib import Path
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
d=json.loads((P/'structure-audit.json').read_text(encoding='utf-8'))
maps={641:156,643:179,675:214,677:222,679:225,681:236,683:239,700:352,702:383,704:391,706:401,708:404,716:420,718:424,720:430,722:435,724:395,736:441,738:452}
for a in d['archived_table_inventory']:
 bi=a['baseline_index'];a['current_counterpart_index']=maps.get(bi)
 a['baseline_rows']=d['baseline']['blocks'][bi]['rows']
 if bi in maps:a['current_rows']=d['current']['blocks'][maps[bi]]['rows']
 if bi==641:a['recommendation']='Restore the full institution-by-institution condition overview structure here, expanded to hospital/other local-government rows. Current table156 is school-only and contradicts the overall-condition narrative. MF register only provides Functional/Faulty, not In store/Broken/Other; replace those unavailable detailed headers with Functional and Faulty or use field-source evidence if separately available.'
 elif bi in maps:a['recommendation']='Equivalent table remains in main report with register classification/accounting fields; do not duplicate archived old table. Keep/reconcile current equivalent unless restoring the specific original visual style.'
 else:a['recommendation']='No distinct main counterpart; resolve against document scope before adding.'
for p in d['restoration_plan']:
 if p.get('title')=='Service-date exceptions methodology table':p['archived_base_index']=141;p['insertion']='baseline2.6.1 Review of service dates block138; current2.6 financial methodology body134'
d['highlight_inventory']['recommended_whole_added_sections'].extend([
 {'name':'4.2 Obsolete and Unserviceable Assets','current_start':487,'current_end_exclusive':490,'reason':'Heading existed but full body paragraphs green; retain this complete section and green body if treating complete added substantive section as new.'},
 {'name':'4.3 Missing and Unrecorded Assets','current_start':490,'current_end_exclusive':495,'reason':'Heading existed but all four substantive body paragraphs green; retain whole section content.'}
])
d['inline_highlight_edit_rule']={
 'preserve_pre_3_2':'Current blocks0-181 preserve wording and paragraph structure except metric corrections; do not apply green-removal text extraction here.',
 'mixed_prose_after_3_2':'For paragraph with nongreen substantive text and word-level red+green replacement pairs, prior_text (drop onlygreen text; keepred text) restores the original grammatical sentence. Clear red highlight/strike then correct metrics/numeric interpretation necessary for register agreement.',
 'whole_sections':'Do not strip allgreen title/body sections merely because a section-number run is nongreen. New sections listed in highlight_inventory must remain.',
 'tables':'Current revised tables are allgreen, usually complete replacements of superseded original tables. Keep their reconciled data and clear highlighting outside a whole new section; removinggreen runs would erase table contents.',
 'captions':'Restore caption original wording by droppinggreen but use final sequential figure/table IDs as numbering corrections; put captions below every graph.',
 'allgreen_paragraphs':'Standalone allgreen paragraphs are not mixed inline prose. Retain useful metrics, source/denominator notes and new complete discussion sections. Only keep green styling when belonging to whole new section.',
 'exceptions':'Original prose includes outdated condition claims (e.g all87 MoWTassetsfunctional) and engraving-rate denominators unavailable in MF. Those require minimal metric/category corrections beyond literal number replacement; otherwise old wording contradicts table.'}
(P/'structure-audit.json').write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf-8')
with (P/'structure-audit.txt').open('a',encoding='utf-8') as f:
 f.write('\n\nEXACT ARCHIVED TABLE TO CURRENT TABLE MAP\n')
 for a in d['archived_table_inventory']:f.write(json.dumps(a,ensure_ascii=False)+'\n')
 f.write('\nINLINE HIGHLIGHT SEMANTICS\n'+json.dumps(d['inline_highlight_edit_rule'],indent=2,ensure_ascii=False))
print(json.dumps(d['inline_highlight_edit_rule'],indent=2,ensure_ascii=False))
