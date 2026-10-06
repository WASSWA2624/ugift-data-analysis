import json,re
from pathlib import Path
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
d=json.loads((P/'structure-audit.json').read_text(encoding='utf-8'))
b={x['index']:x for x in d['current']['blocks']}
def norm(s):return re.sub(r'\s+',' ',s).strip()
def old(i):return norm(b[i]['prior_text'])
def new(i):return norm(b[i]['accepted_text'])

fix={
177:'Overall, the 229,024 assets across the different institutions had a recorded value of UGX 996,812,628,890. Based on the straight-line depreciation method, available accumulated depreciation was UGX 165,185,197,307 and available net book value was UGX 595,801,587,531 as at 30th September 2026. Recorded values vary by institution, with MDAs at UGX 32,054,743,836, Blood Banks at UGX 1,503,720,926, Seed Secondary Schools at UGX 700,242,561,371 and Health Centres at UGX 260,692,452,291, as indicated in table 2. The table also includes hospital and other local-government assets. Available costs, depreciation and net book values cover different populations; the financial reconciliation appendix gives the matched accounting population.',
184:'The exercise recorded 16,663 assets of the different categories across all the thirteen asset-holding Ministries and agencies. In terms of categorization, the exercise recorded 15,192 ICT equipment items including desktop computers, laptops, tablets and Uninterruptible Power Supply (UPS) units, 77 transport items, 99 furniture and fittings, 48 other classified assets, 1,235 items outside fixed-asset classification and 12 unclassified entries.',
185:'By location, most MDA assets (94.6%) were at MoES, MoWE and MAAIF while PPDA was found with only five assets including three Lenovo ThinkPad laptops, one HP LaserJet printer and one Samsung Galaxy tablet as indicated in figure 4 below.',
189:'At MDA level, apart from sixteen faulty assets at Ministry of Works and Transport, one faulty double-cabin pickup at Ministry of Health and three faulty laptops at the Office of the Prime Minister, the rest of the assets, 16,643 (99.9%), were recorded as functional and in use. The Ministry of Education and Sports holds 10,783 of these assets, mainly TELA handsets and tablets, all recorded as in use at the different schools across the country. LGFC and MoPS indicated that they never received UgIFT assets.',
191:'At MDA level, there were 16,663 asset records, of which 5,045 (30.3%) had usable identifiers, with 4,925 assets (29.6%) bearing UgIFT or UGFT in the tag field and 120 (0.7%) carrying another identifier. The majority of assets, 11,618 (69.7%), had no usable tag recorded. Figure 5 below shows the identification status of the assets at the different MDAs. These tag-field counts do not confirm physical engraving.',
198:'Asset availability: The ministry keeps a UgIFT asset register and the consolidated register for all MDAs that received UgIFT assets. A total of 458 assets were recorded at the ministry including 230 ICT items, 99 furniture and fittings, 21 transport items, 37 other classified assets, 65 items outside fixed-asset classification and six unclassified entries. The main items were office chairs and desks, desktop computers, tablets and 20 Toyota Hilux double-cabin pickups.',
199:'Condition and functionality: All 458 assets (100.0%) were recorded as functional and in use, and none was classified as faulty.',
201:'Marking and identification: A total of 282 assets (61.6%) had usable identifiers and 176 (38.4%) had no usable tag recorded. Of all 458 assets, 247 (53.9%) had UgIFT or UGFT in the tag field and 35 (7.6%) carried another identifier. The 20 double-cabin pickups were identified by their registration numbers rather than UgIFT tag text. These tag-field counts do not confirm physical engraving.',
207:'Asset availability: The Ministry did not provide a UgIFT Asset Register. The MoWT register contained 87 assets, of which 69 ICT items were mainly desktop computers, monitors, uninterruptible power supply (UPS) units, video-conferencing equipment, printers and photocopiers; one Toyota Hilux pickup; sixteen items outside fixed-asset classification; and one unclassified entry. The sixteen items outside fixed-asset classification were keyboards. The unclassified entry was entered as Ministry of Local Government, as presented in Figure 6. Computer components are recorded separately and are included in these totals.',
210:'Condition and functionality: Of the 87 assets, 71 (81.6%) were recorded as functional and in use; sixteen (18.4%) were recorded as faulty and not in use.',
211:'Marking and Identification: Of the 87 assets, 79 (90.8%) had usable identifiers, with 77 (88.5%) having UgIFT or UGFT in the tag field and two (2.3%) carrying another identifier; eight (9.2%) had no usable tag recorded.',
217:old(217).replace('figure 46c','figure 7'),
220:'All the 10,783 assets (100.0%) are recorded as functional and in use. All the 456 laptops are recorded as functional and in use. Their identification status is shown in table 6.',
223:'Marking and Identification: Of the 10,783 assets, 458 (4.2%) had UgIFT or UGFT in the tag field, while 10,325 (95.8%) had no usable tag recorded. None of the handset or tablet records has a usable tag recorded; the tag fields do not confirm physical engraving.',
231:'Asset availability: The team recorded UgIFT assets at the Ministry of Agriculture, Animal Industry and Fisheries (MAAIF) and established that it held 2,045 assets. These included 1,236 ICT equipment items, two transport items and 807 others, comprising 797 outside fixed-asset classification, five other classified assets and five unclassified entries. The ICT items were mainly 819 tablets, 211 computers (162 desktop CPU entries and 49 laptops), 149 monitors and 21 printers. The breakdown of the assets mentioned above is shown in figure 8.',
234:'All 2,045 assets (100.0%) are recorded as functional and in use. All 211 computers and 819 tablets are recorded as functional and in use. Identification is reported separately in table 9.',
237:'Marking and Identification: Of the 2,045 assets, 1,232 (60.2%) had usable identifiers, 1,228 (60.0%) with UgIFT or UGFT in the tag field and four (0.2%) with another identifier; 813 (39.8%) had no usable tag recorded. The denominator includes all ministry records, including items outside fixed-asset classification, and the tag fields do not confirm physical engraving.',
246:'Asset availability: A total of 260 assets were recorded. Of the 260 assets, 31 were classified as ICT equipment, 25 as transport equipment (motor vehicles and motorcycles), six as other classified assets and 198 as items outside fixed-asset classification, as indicated in Figure 9.',
250:'Condition and functionality: The assets recorded as functional and in use were 259 (99.6%). Only one asset, a double-cabin pickup, was recorded as faulty and not in use.',
251:'Marking and Identification: Out of the 260 assets, 32 (12.3%) had usable identifiers while 228 (87.7%) had no usable tag recorded. There were fourteen (5.4%) assets with UgIFT or UGFT in the tag field and eighteen (6.9%) with other identifiers. These tag fields do not confirm physical engraving.',
258:old(258).replace('Figure 46f','Figure 10'),
261:'Condition and functionality: Seven assets (70.0%) were recorded as functional and in use. Three (30.0%) were recorded as faulty and out of use.',
262:'Marking and identification: All the ten laptops (100.0%) had UgIFT or UGFT in the tag field.',
268:'Asset availability: The Asset Verification at the Ministry of Water and Environment found out that the ministry keeps a general register which does not conform to IFMIS Standards. The register recorded 2,939 assets, of which 2,782 were classified as ICT equipment and 157 outside fixed-asset classification. The assets received by the Ministry included 2,368 tablets, of which 2,344 were Euron tablets; computers and related monitors, keyboards and UPS units; and 31 laptops. The Ministry also received sixteen real-time kinematic GPS machines. Computer components are recorded separately and are included in these totals.',
269:old(269).replace('included157','included 157').replace('7 airborne ground-penetrating radar units','seven survey units described as ground-penetrating radar equipment')+' These items are already included in the ministry total.',
270:'Asset condition and functionality: The findings further indicated that all 2,939 assets (100.0%) were recorded as functional and in use, and none was classified as faulty.',
271:'Marking and Identification: The ministry received a total of 2,939 assets, of which 2,897 (98.6%) had usable identifiers, 2,864 (97.4%) with UgIFT or UGFT in the tag field and 33 (1.1%) with another identifier; 42 (1.4%) had no usable tag recorded. These tag fields do not confirm physical engraving.',
277:'Asset availability: The Asset Verification at the Ministry of Gender, Labour and Social Development found out that the ministry keeps a UgIFT asset register which had ten UgIFT assets. These comprised eight Lenovo computers, including four ThinkBook laptops, and two Samsung tablets. Figure 11 presents the UgIFT assets recorded for MoGLSD.',
278:'Asset condition and functionality: The findings further indicate that all ten UgIFT assets (100.0%) were recorded as functional and in use.',
279:'Marking and Identification: Eight Lenovo computers (80.0%) had UgIFT or UGFT in the tag field and the two Samsung tablets (20.0%) had no usable tag recorded.',
288:'National Environment Management Authority (NEMA) had six ICT items: four computers, a printer and a heavy-duty photocopier.',
289:'Condition and functionality: All six assets (100.0%) were recorded as functional and in use.',
293:'One asset (16.7%), the heavy-duty photocopier, had UgIFT or UGFT in the tag field while the other five (83.3%) had no usable tag recorded.',
300:old(300).replace('Figure 46j','Figure 13'),
303:'Asset condition and functionality: All the five assets (100.0%) were recorded as functional and in use.',
304:'Asset marking and identification: All five assets (laptops, a tablet and a printer) had UgIFT or UGFT in the tag field.',
310:old(310).replace('figure 46k','figure 14'),
311:'Asset condition and functionality: All twenty assets (100.0%) were recorded as functional and in use.',
312:'Asset marking and Identification: Six assets (30.0%) had UgIFT or UGFT in the tag field and fourteen (70.0%) carried other identifiers. The other identifiers were the office\'s own asset codes or vehicle registration numbers for the two pickups. These tag-field counts do not confirm physical engraving.',
320:'Asset availability: The asset verification at the Ministry of Local Government (MoLG) found that the ministry kept a UgIFT asset register and had thirteen UgIFT assets: one double-cabin pickup and twelve ICT items. The ICT assets comprised six computer entries, four laptops and two photocopier entries, one described as heavy duty. Figure 15 presents the UgIFT assets recorded for MoLG.',
324:'Asset condition and functionality: The findings further indicate that all thirteen assets (100.0%) were recorded as functional and in use.',
325:'Asset marking and identification: Out of the thirteen assets, eight (61.5%) had usable identifiers while five (38.5%) had no usable tag recorded. Of the eight identified assets, seven (53.8% of all assets) had UgIFT or UGFT in the tag field while one (7.7%) carried another identifier. These tag-field counts do not confirm physical engraving.',
331:'Asset availability: The findings from the verification exercise indicate that MoLH &UD had 27 UgIFT assets. These include 25 Honda motorcycles and two other entries described as Accessories (12-Helmets). The description has not been multiplied by twelve to derive a helmet count.',
334:old(334),
335:'Asset condition and functionality: All the 27 assets (100.0%) were recorded as functional and in use, and none was classified as faulty.',
336:'Asset marking and Identification: None of the 27 assets had UgIFT or UGFT in the tag field. Thirteen (48.1%) had other identifiers and fourteen (51.9%) had no usable tag recorded. The motorcycles\' registration numbers are distinguished from UgIFT tag text.',
343:old(343),
344:'Asset availability: The three regional blood banks held a total UgFT asset base of 602 recorded assets. The exercise recorded assets at the three regional blood banks as follows: Arua Regional Blood Bank held 324 assets, Hoima Regional Blood Bank had 163 and Soroti Regional Blood Bank had 115 assets. This subtotal excludes assets attributed to other institutions or locations.',
346:'Assets at the regional blood banks were generally recorded as functional and in use: 578 (96.0%) had that status. Only Arua Regional Blood Bank had faulty assets, accounting for all 24 (4.0%) faulty assets in the three-bank total.',
348:'Of the 602 regional blood-bank assets, 76 (12.6%) had usable identifiers and 526 (87.4%) had no usable tag recorded. Twenty-six (4.3%) carried UgIFT or UGFT in the tag field and fifty (8.3%) carried another identifier. These tag-field counts do not confirm physical engraving.',
350:'Available recorded value was UGX 1,503,720,926 and available net book value at 30 September 2026 was UGX 826,632,084. Available accumulated depreciation was UGX 553,688,842. Recorded cost is available for 589 of the 602 regional blood-bank records, and net book value is unavailable for thirteen. The available columns cover different populations; the financial reconciliation appendix gives the matched accounting population.',
375:old(375),
378:'The programme list at the LG level contained 629 UgIFT facilities, of which 371 were Health Centres and 258 were Seed Secondary Schools. Supporting returns accounted for 590 entries and 39 had discrepancies requiring reconciliation. A total of 208,688 assets were recorded at Health Centres and school locations, of which 63,432 were for Health Centres and 145,256 were for schools. Of the 208,688 assets, 195,224 (93.5%) were recorded as functional and in use while 13,464 (6.5%) were recorded as faulty and not in use. A further 3,067 assets were attributed to hospitals and four to other local-government locations. The details are presented in sections 3.6 (Health Centres) and 3.7 (Seed Secondary Schools).',
381:'The verification findings indicate that health facilities had 63,432 recorded assets across the different categories which include clinical and laboratory equipment, furniture, maternity ward equipment, ICT equipment, buildings, land and other items. The register includes 7,746 items outside fixed-asset classification. Table 24 and Figure 17 present the assets by category.',
387:'The findings indicate that of the 63,432 health-centre assets, 57,759 (91.1%) were recorded as functional and in use and 5,673 (8.9%) were recorded as faulty and not in use. Figure 18 and Table 25 present the condition of the assets. These two register categories do not establish separate current counts of items in store, broken items and other reasons for non-use.',
392:'The field records describe health-centre assets that were not in use for other reasons, including those not delivered to the facility (still in stores at LGs), idle items, items with missing parts, lack of power, items not required at the facility, rooms or wards unavailable for installation, items held at another facility, items awaiting installation, lost or missing items and equipment unused because staff were not trained or no specialist was available to operate it. Examples include a wall-mounted blood-pressure machine at Butawata Health Centre III (Mubende District) recorded as not functional; a wheelchair at Aarapoo Health Centre III (Serere District) that had not been delivered; a patient screen at Ayer Health Centre III (Kole District) that was on the delivery note but not seen; a paediatric bed at Okwerodot Health Centre III (Kole District) supplied without a mattress; and an autoclave at Anamwany Health Centre III (Amolatar District) unused for lack of electricity. The register\'s two condition categories do not provide a separate count for these reasons.',
393:'In terms of buildings and structures, health-centre records total 2,260, comprising 487 residential-building entries, 1,402 non-residential-building entries, 364 other-structure entries and seven water-supply-system entries. Residential buildings are staff houses and other buildings described as residential. Some entries require reclassification, so the record total does not establish a count of separate buildings. Table 26 presents the classifications.',
397:'Of the 63,432 assets in Health Centres, 9,541 (15.0%) had usable identifiers and 53,891 (85.0%) had no usable tag recorded. It was noted that 3,824 (6.0%) carried UgIFT or UGFT in the tag field and 5,717 (9.0%) carried other identifiers, as depicted in Figure 19 and Table 27. These tag-field counts do not confirm physical engraving.',
406:'Recorded value is the cost in the verification records. For recognized assets with complete accounting figures, net book value is that cost less accumulated depreciation to 30 September 2026 and is not taken below zero. Available costs, depreciation and net book values cover different populations; the financial reconciliation appendix gives the matched accounting population.',
407:old(407),
409:old(409),
418:'The findings showed that schools had 145,256 recorded assets covering the following categories: school buildings, water facilities, furniture, computers and related equipment such as monitors, UPS units and keyboards; ICT equipment including printers, photocopiers, cameras and projectors; and other school assets such as laboratory items, electrical items, plant and machinery and sports equipment. Table 29 presents the details. The school group follows recorded locations and includes schools whose programme assignment requires confirmation.',
422:'Out of 145,256 assets, 137,465 (94.6%) were recorded as functional and in use. The verification further established that 7,791 (5.4%) were recorded as faulty and not in use. Table 30 indicates the asset condition. These register categories do not establish separate current counts of items in store, broken items and other reasons for non-use.',
425:'Functional assets are recorded as in use and faulty assets as not in use. The two condition columns sum to the assets recorded. They do not establish separate counts of good items in store, broken items and other reasons for non-use.',
426:'School furniture and fittings (desks, tables, chairs, shelves and stools) is the largest category with 107,792 assets. Of these, 102,521 were recorded as functional and in use while 5,271 were recorded as faulty. ICT equipment had 10,404 assets recorded as functional and in use.',
428:'Of the 145,256 school assets, 35,601 (24.5%) had usable identifiers while 109,655 (75.5%) had no usable tag recorded. A total of 13,478 (9.3%) carried UgIFT or UGFT in the tag field and 22,123 (15.2%) carried other identifiers, as shown in Table 31. These tag-field counts do not confirm physical engraving.',
431:'Movable assets exclude buildings, structures and land. The table groups recorded tag text as UgIFT or UGFT, another identifier or no usable tag. Buildings, structures and land are identified through property and site records rather than engraving.',
432:'3.8 Financial Value of school assets',
437:'Recorded value is the cost in the verification records. For recognized assets with complete accounting figures, net book value is that cost less accumulated depreciation to 30 September 2026. Available costs, depreciation and net book values cover different populations; the financial reconciliation appendix gives the matched accounting population.',
439:'The verification established that there were a number of facilities that were either completed or not completed. Table 33 provides the programme-list construction baseline and the documented outstanding-work findings separately.',
442:'Counts are facilities. Programme-list completion labels and the documented outstanding-work findings may concern the same facilities and must not be added together. Outstanding-work counts are documented minimums.',
443:'Table 33 indicates that the programme list recorded 547 facilities as complete and 82 as ongoing before verification. The reviewed evidence identifies at least 70 facilities with incomplete works, comprising 57 schools and thirteen Health Centres, and another thirteen awaiting handover or commissioning, comprising eleven schools and two Health Centres. Some facilities were providing services while works remained incomplete. These findings and the programme-list completion labels describe different matters and must not be added together.',
444:old(444),
450:'The verification exercise established that there were mismatches between information from the programme list and what was found on the ground. Out of 629 programme-list entries, 590 (93.8%) had supporting returns and 39 (6.2%) had discrepancies requiring reconciliation. These include entries on the programme list without matching returns or with conflicting location or facility-type information. Renamed facilities already matched to returns are not added to the 39 exceptions. Table 34 provides the details.',
453:'Counts are programme-list facilities: 24 Health Centres and fifteen schools, giving 39 distinct exceptions. HC means Health Centre; SSS means Seed Secondary School. Renamed facilities already matched to returns are not added to this total.',
455:old(455).replace('237 (83.5%)','238 (83.8%)').replace('70 (24.6%)','71 (25.0%)').replace('60 (21.1%)','61 (21.5%)').replace('163 (57.4%)','164 (57.7%)'),
456:old(456).replace('Figure 88','Figure 44'),
461:old(461)+' Percentages use 477 facility responses unless a facility type is specified; categories overlap.',
462:'Insufficient Power supply which was reported by 201 facilities (42.1%), including 44.4% of Health Centre respondents and 38.9% of school respondents;',
463:old(463).replace('32.3%','32.1%').rstrip(',')+' (153 of 477).',
464:old(464)+' (151 of 477).',
465:old(465).replace('27.3%','27.0%').rstrip(',')+' (129 of 477).',
466:old(466).rstrip(',')+' (106 of 477).',
467:old(467)+' (105 of 477).',
468:old(468).rstrip('.')+' (96 of 477).',
469:old(469).rstrip(',')+' (82 of 284), and 1.6% of schools (three of 193).',
470:'Incomplete or delayed works, handover or commissioning reported by 28.0% of Seed Secondary School respondents (54 of 193) and 10.2% of Health Centre respondents (29 of 284).',
471:old(471).rstrip('.')+' (84 of 477).',
478:old(478).replace('151 facilities (32.2%)','152 facilities (32.4%)').replace('84 (17.9%)','85 (18.1%)'),
480:old(480).replace('Figure 98','Figure 46').replace('41.0%','41.4%'),
483:old(483).replace('Figure 99','Figure 47').replace('62 (12.6%)','61 (12.3%)'),
486:old(486),
499:old(499).replace('three damaged laptops','three laptops recorded as faulty').replace('six broken blood pressure machines','six blood-pressure machines recorded as faulty'),
500:old(500).replace('115 facilities with works outstanding, starting with the 22 of them that were not yet providing services','83 documented facilities with works or handover outstanding, comprising seventy with incomplete works and thirteen awaiting handover or commissioning. These are documented minimums'),
501:old(501),
502:old(502),
503:old(503),
}

# Reconcile financial statements using the original opening sentence and new accounting values.
finance={202:('5,615,661,760','6,204,318,000'),212:('340,968,220','455,932,376'),226:('14,760,581,751','14,925,128,359'),240:('1,844,366,458','2,856,556,593'),252:('953,859,009','1,186,689,609'),272:('5,993,100,537','5,029,981,561'),280:('20,120,000','46,180,000'),294:('27,324,409','46,824,409'),315:('228,773,680','388,773,680'),326:('31,114,879','343,320,450'),337:('597,549,997','487,349,999')}
for i,(ov,nv) in finance.items():
 s=old(i).replace(ov,nv)
 if i==212:s=s.replace('Table 3','Table 4')
 # The additional accounting figures are metrics, not editorial substitutions.
 revised=new(i)
 tail=revised[revised.find('Accumulated depreciation'):] if 'Accumulated depreciation' in revised else ''
 tail=re.sub(r' The table below gives the category breakdown\.?','',tail)
 fix[i]=s+' '+tail
fix[263]=old(263)+' Accumulated depreciation is UGX 48,181,770 and net book value is UGX 5,353,530 at 30 September 2026.'
fix[305]='Financial Value of assets: The MF register states a recorded cost of UGX 30,153,500 for these assets. Accumulated depreciation is UGX 13,066,516 and net book value is UGX 17,086,984 at 30 September 2026.'
fix[402]='Financial Value of assets: The findings indicate that the available recorded value of assets was UGX 260,692,452,291 and the available net book value was UGX 189,403,577,197, while available accumulated depreciation was UGX 39,211,094,700 as at 30 September 2026. Table 28 gives the recorded value and net book value. Cost is available for 63,183 of 63,432 records; net book value is unavailable for 7,828. Available columns cover different populations; the financial reconciliation appendix gives the matched accounting population.'
fix[433]='The available recorded value was UGX 700,242,561,371, the available net book value was UGX 394,241,708,595 and available accumulated depreciation was UGX 104,574,530,246 as at 30 September 2026, as shown in Table 32. Cost is available for 144,445 of the 145,256 school records; net book value is unavailable for 14,807. Available columns cover different populations; the financial reconciliation appendix gives the matched accounting population.'

# Old captions are retained with the sequential numbering already displayed in accepted revisions.
caption_indices=[186,208,213,219,221,224,233,235,238,249,260,285,291,302,314,323,333,351,382,385,389,390,394,399,400,403,411,419,423,429,434,440,451,459,473,482,485]
caption_override={
224:'Table 6: Recorded tag content of assets at MoES',238:'Table 9: Recorded tag content of assets at MAAIF',394:'Table 26: Health Centre records classified as buildings and structures',399:'Figure 19: Recorded tag content: Health Centres',429:'Table 31: Identification of assets at schools',440:'Table 33: Programme-list construction baseline and documented outstanding works',451:'Table 34: Inconsistencies between the programme list and the facilities found',419:'Table 29: Availability of assets at schools',423:'Table 30: Condition of assets: schools',434:'Table 32: Recorded value and net book value: schools',459:'Figure 44: Programme Benefits'}
for i in caption_indices:
 orig=old(i);rev=new(i)
 mt=re.match(r'\s*(Figure|Table)\s+(\d+):',rev)
 if mt:orig=re.sub(r'^\s*(Figure|Table)\s+[^:]+:',mt.group(1)+' '+mt.group(2)+':',orig)
 fix[i]=caption_override.get(i,orig)

new_ranges=[(44,57),(354,375),(487,495),(505,508),(509,627)]
mapping={}
for x in d['current']['blocks']:
 i=x['index']
 if x['kind']!='p' or not x['green_runs'] or not x['accepted_text'].strip():continue
 if x['green_share_of_accepted']==1:continue
 if i<182 and i!=177:
  corrected=new(i);why='Preserve current pre-3.2 wording; only formatting needs clearing outside whole new sections.'
 elif any(a<=i<c for a,c in new_ranges):
  corrected=new(i);why='Retain the complete newly added section; the unhighlighted section-number prefix must not cause deletion of its title.'
 else:
  corrected=fix.get(i,old(i));why='Remove inline green editorial substitutions, restore original prose and minimally correct metrics, classification or numbering.' if i in fix else 'Remove inline green editorial substitutions and restore original prose verbatim apart from normalized run spacing.'
 mapping[str(i)]={'text':norm(corrected),'original_text':old(i),'accepted_revised_text':new(i),'rationale':why}
for i,s in fix.items():
 if str(i) not in mapping:mapping[str(i)]={'text':norm(s),'original_text':old(i),'accepted_revised_text':new(i),'rationale':'Metric reconciliation in an otherwise retained paragraph.'}

# Specific heading-title revision is a whole title rather than a sentence fragment.
for i in [416,432,267,454,460,487,490]:
 corrected={416:'3.7 Seed Secondary Schools',267:'3.3.7 Ministry of Water and Environment',454:'3.12 UgIFT support to service delivery',460:'3.12.1 Gaps and Challenges',487:'4.2 Obsolete and Unserviceable Assets',490:'4.3 Missing and Unrecorded Assets'}.get(i,fix.get(i,new(i)))
 mapping[str(i)]={'text':corrected,'original_text':old(i),'accepted_revised_text':new(i),'rationale':'Retain complete heading title; remove duplicate obsolete numbering.'}
for k,v in mapping.items():
 v['requires_text_edit']=norm(v['text'])!=norm(v['accepted_revised_text'])
 v['action']='retain_current' if int(k) in [9,126] else 'replace_text'

meta={'index_basis':'Zero-based direct child of word/document.xml w:body in original1344 document. Tables and figures also consume indices.','entries':mapping,'counts':{'entries':len(mapping)},'notes':['Before3.2 preserve current wording except metric177; parent also needs reconcile nonhighlighted metric paragraphs148,149,154,168,169 and the old table156.','For individual financial aggregates sum available source values, so cost-depreciation may differ from displayed NBV. Coverage/financial appendix qualifiers are retained.','For full new sections retain accepted complete paragraphs and green styling; do not use prior_text which often contains only a number.','New or restored tables and changed captions outside complete new sections must be unhighlighted.','Standalone allgreen paragraphs are not word-interleaving; retain them and clear green formatting unless within a full new section.','All metrics are from existing accepted revised text and preservation cache; independent workbook audit by metric agent should supersede a number if fresh validation differs.']}
(P/'prose-corrections.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
(P/'prose-corrections.txt').write_text('\n\n'.join(k+' '+v['text'] for k,v in mapping.items()),encoding='utf-8')
print(json.dumps(meta['counts']))
