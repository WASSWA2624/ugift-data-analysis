from pathlib import Path
import json,re,hashlib
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
d=json.loads((P/'figure-table-reference-audit.json').read_text(encoding='utf-8'))
b={x['i']:x for x in d['paragraphs']}
file=Path(d['file'])
corrections={}
def correct(i,new,rationale):
 corrections[str(i)]={'body_index':i,'old_text':b[i]['text'],'text':new,'rationale':rationale}
def replace(i,old,new,rationale):correct(i,b[i]['text'].replace(old,new),rationale)
replace(416,'in the figure','in Figure 15','Replace generic graph reference with the MoLG figure number.')
for i,n in [(452,21),(459,22),(466,23)]:replace(i,'The table below','Table '+str(n),'Replace vague category-finance table reference with its existing number.')
replace(526,'The table groups','Table 31 groups','Replace generic school identification table reference.')
replace(502,'The photos below','The photographs in Figures 20 to 23','Reference the health-centre photo group by its existing figure-number range.')
replace(504,'The photos below','The photographs in Figure 24 and Figures 25 to 27','Reference the incomplete-health-centre figures by their existing numbers.')
replace(507,'The following three photographs','Figures 25 to 27','Reference the three Benet photographs by figure number.')
replace(539,'The photos below','The photographs in Figures 28 to 30','Reference the completed-school figure group by number.')
replace(541,'The photos below','The photographs in Figures 31 to 43','Reference the unfinished-school figure group by number.')
correct(603,'Appendices','Remove duplicate old Annexures heading left alongside its new title.')

# Existing numbered tables/graphs with no prose reference can be referenced by one short sentence.
main_missing_table_refs={297:(3,'Table 3 presents the category breakdown.'),315:(5,'Table 5 presents condition and use.'),321:(7,'Table 7 presents the category breakdown.'),329:(8,'Table 8 presents condition and use.'),335:(10,'Table 10 presents the category breakdown.'),347:(11,'Table 11 presents the category breakdown.'),358:(12,'Table 12 presents the category breakdown.'),367:(13,'Table 13 presents the category breakdown.'),375:(14,'Table 14 presents the category breakdown.'),389:(15,'Table 15 presents the category breakdown.'),400:(16,'Table 16 presents the category breakdown.'),410:(17,'Table 17 presents the category breakdown.'),421:(18,'Table 18 presents the category breakdown.'),432:(19,'Table 19 presents the category breakdown.'),445:(20,'Table 20 presents the blood-bank financial values.')}
for i,(n,sentence) in main_missing_table_refs.items():
 if 'Table '+str(n) not in b[i]['text']:correct(i,b[i]['text']+' '+sentence,'Supply an explicit prose reference to a numbered table that currently has only a caption.')
if 'Figure 12' not in b[383]['text']:correct(383,b[383]['text']+' Figure 12 presents the asset categories.','Supply an explicit NEMA figure reference.')

captions=[]
names=[
 'Actions to address the reported service gaps',
 'Available financial amounts and accounting coverage',
 'Reconciliation of recorded cost and net book value',
 'Basis of recorded cost estimates',
 'Service-date entries across all assets',
 'Service-date exception examples and supporting evidence',
 'Definitions used in the analysis',
 'Programme-list exception roster',
 'Documented outstanding works and handover',
 'Facility interview scope and denominators',
 'Asset reconciliation examples',
 'Photographic schedule',
 'Land records and ownership evidence',
 'Recorded financial values for hospitals on local-government books',
 'Recorded financial values for other local-government locations',
 *[f'Financial values by asset type at {name}' for name in ['MoFPED','MoWT','MoES','MAAIF','MoH','OPM','MoWE','MoGLSD','NEMA','PPDA','OAG','MoLG','MoLHUD','Arua Regional Blood Bank','Hoima Regional Blood Bank','Soroti Regional Blood Bank','Health Centres','schools']],
 'Responses to reviewer comments'
]
for n,t in enumerate(d['unlabelled_data_tables'],start=35):
 captions.append({'table_body_index':t['i'],'number':n,'caption':'Table '+str(n)+': '+names[n-35],'placement':'Immediately above existing table','source_table_text_start':t['text_start'],'requires_new_number':True})

proposed_refs={
605:'Table 36 shows the available financial amounts and accounting coverage.',
607:'Table 37 reconciles the available recorded cost to net book value.',
612:'Table 38 presents the basis of recorded costs.',
619:'Table 39 presents mutually exclusive service-date categories; rounded percentages may not total 100.0%.',
620:None,
631:None,
640:None,
643:None,
647:'Table 44 gives the interview denominators.',
651:None,
654:'Table 46 provides the photographic schedule.',
657:None,
661:'Table 48 presents the category financial values.',
664:'Table 49 presents the category financial values.',
669:None,
727:None
}
for i,s in proposed_refs.items():
 if s:correct(i,b[i]['text']+' '+s,'Add explicit reference after assigning the proposed new table number.')
replace(605,'Amounts below','Amounts in Table 36','Remove a remaining unnumbered positional reference to financial amounts.')
replace(620,'The cases below','The cases in Table 40','Reference the service-date exception table after assigning its proposed number.')
replace(631,'The definitions below','The definitions in Table 41','Reference the definitions table after assigning its proposed number.')
replace(640,'The 39 entries below','The 39 entries in Table 42','Reference the exception roster after assigning its proposed number.')
replace(643,'This schedule','Table 43','Reference the outstanding-works schedule after assigning its proposed number.')
replace(651,'The cases below','The cases in Table 45','Reference the reconciliation example table after assigning its proposed number.')
replace(657,'The table lists','Table 47 lists','Reference the land schedule after assigning its proposed number.')
replace(669,'The following tables','Tables 50 to 67','Reference all eighteen asset-type financial tables by their proposed number range.')
replace(727,'The table below','Table 68','Reference the restored reviewer response table after assigning its proposed number.')

insertions=[{'before_body_index':601,'text':'Table 35 sets out the actions, responsible officers and evidence of completion.','purpose':'Reference the action schedule after assigning its proposed number.'}]
protected=[{'body_index':290,'text':b[290]['text'],'reason':'Within protected section 3.2. It says a category-breakdown table is below, but section3.3 immediately follows.','correct_reference':'Table 2 contains the overall MDA financial aggregate; Tables 3 to 19 give separate ministry category schedules.','proposed_minimal_replacement':'Table 2 gives the overall ministry financial values and identifies unavailable amounts; Tables 3 to 19 provide the ministry-specific category breakdowns.','conflict':'Reference wording correction is requested globally but the user separately says strictly preserve sections1 through3.2 exceptmetrics. Do not edit this protected paragraph without resolving precedence; do not use Table3 as if it were aggregateMDA.'}]
report={'source_file':str(file),'source_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'index_basis':'Zero-based direct body child in latest Word-materialized DOCX (731 blocks). Original prior audit indices are offset by95; match old_text before edit because numbering caption insertions will shift later indices.','corrections':corrections,'proposed_new_caption_assignments':captions,'proposed_insertions':insertions,'protected_conflicts':protected,'notes':['Thirty-four data tables lack numeric captions; proposed numbering is Table35-68, continuing existingTable1-34 without renumbering any protected tables.','Seven tables are photograph layouts; identify their contents as Figure ranges instead of assigning spurious data-table numbers.','Some original photographs in earlier sections have no Figure labels; do not alter protected section1-through3.2 photo captions merely to assign new IDs.','Caption insertion/prose changes occur only after actualHeading2 section3.3 atbody291; protectedsection3.2 spans277-290.','Use old_text matching and verify sourcehash before applying index-based changes.','Reference proposals do not change any metric.'], 'counts':{'corrections':len(corrections),'new_table_captions':len(captions),'protected_conflicts':len(protected)}}
(P/'figure-table-reference-corrections.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(report['counts']))
print('TABLE CAPTIONS',[(x['table_body_index'],x['number']) for x in captions])
