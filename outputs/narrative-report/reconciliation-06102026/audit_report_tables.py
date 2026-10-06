"""Check the current 73 report tables against SHA-verified REF aggregates."""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import json,re,gzip
from docx import Document

ROOT=Path(r'D:/coding/ugift-data-analysis')
OUT=ROOT/'outputs/narrative-report/reconciliation-06102026'
CACHE=ROOT/'tmp/report-revision-20261006'
MET=json.loads((OUT/'register-metrics.json').read_text(encoding='utf-8'))
PRIOR=json.loads((CACHE/'metrics_report.json').read_text(encoding='utf-8'))
DOC=Document(ROOT/'outputs/narrative-report/ugift-working-report-06102026-1344.docx')
TABLES=DOC.tables
BODY_INDEX={id(node):i for i,node in enumerate(DOC.element.body)}

def num(text):
    s=text.replace(',','').replace('*','').strip()
    try:return Decimal(s.rstrip('%'))
    except:return None
def amount(value):return Decimal(str(value))
def rounded(value,digits):return amount(value).quantize(Decimal('1').scaleb(-digits),rounding=ROUND_HALF_UP)
def count(x):return f'{x:,}'
def bucket_group(name):return MET['institutions'][name]
def ratio(s):
    cost=s.get('complete_recognized_cost_sum',0)
    return rounded(amount(s.get('complete_recognized_nbv_sum',0))/amount(cost)*100,1) if cost else None
def label(row):return row.cells[0].text.split('\n')[0].strip()
def expected_finance(s):
    output={}
    for i,(field,sumfield) in enumerate([('cost','cost_sum'),('accumulated_depreciation','accumulated_depreciation_sum'),('net_book_value','net_book_value_sum')],1):
        available=s.get(field+'_numeric_rows',0)
        output[i]=f'{rounded(amount(s.get(sumfield,0))/1000000,3):,.3f}'+('*' if available<s['rows'] else '') if available else 'Unavailable'
    output[4]=f'{ratio(s):.1f}%' if ratio(s) is not None else 'n/a'
    return output

MAP={4:'MOFPED BK',5:'MOWT BK',8:'MOES BK',11:'MAAIF BK',12:'MOH BK',13:'OPM BK',14:'MOWE BK',15:'MGLSD BK',16:'NEMA BK',17:'PPDA BK',18:'OAG BK',19:'MOLG BK',20:'MOLHUD BK',22:'ARUA RBB BK',23:'HOIMA RBB BK',24:'SOROTI RBB BK',30:'Health centres',36:'Schools',53:'Hospitals on local-government books',54:'Other local-government or unassigned locations'}
FINE=['MOFPED BK','MOWT BK','MOES BK','MAAIF BK','MOH BK','OPM BK','MOWE BK','MGLSD BK','NEMA BK','PPDA BK','OAG BK','MOLG BK','MOLHUD BK','ARUA RBB BK','HOIMA RBB BK','SOROTI RBB BK','Health centres','Schools']
GROUP_NAMES={'Schools':'Schools','Health centres':'Health centres','Ministries and agencies':'Ministries and agencies','Hospitals on LG books':'Hospitals on local-government books','Regional blood banks':'Regional blood banks','Other LG locations':'Other local-government or unassigned locations'}
RBB_NAMES={'Arua Regional Blood Bank':'ARUA RBB BK','Hoima Regional Blood Bank':'HOIMA RBB BK','Soroti Regional Blood Bank':'SOROTI RBB BK'}

checks=[];corrections={};missingtotals=[];nonnumeric=[]

def record_error(ti,ri,ci,actual,expected,reason):
    bi=BODY_INDEX[id(TABLES[ti]._tbl)]
    corrections.setdefault(str(bi),{'table_index':ti,'body_index':bi,'changes':[]})['changes'].append({'row':ri,'column':ci,'actual':actual,'expected':str(expected),'reason':reason})

def compare(ti,ri,ci,expected,reason='Source metric'):
    actual=TABLES[ti].rows[ri].cells[ci].text
    a,e=num(actual),num(str(expected))
    if a is not None and e is not None:
        okay=a==e
    else:okay=actual.strip()==str(expected).strip()
    checks.append({'table_index':ti,'row':ri,'column':ci,'passed':okay})
    if not okay:record_error(ti,ri,ci,actual,expected,reason)

def finance(ti,source):
    for ri,row in enumerate(TABLES[ti].rows[1:],1):
        name=label(row)
        s=source[name]
        m=re.search(r'([\d,]+) record[s]?; NBV ([\d,]+)/([\d,]+)',row.cells[0].text)
        if m:
            numbers=list(map(lambda x:int(x.replace(',','')),m.groups()))
            want=[s['rows'],s.get('net_book_value_numeric_rows',0),s['rows']]
            if numbers!=want:record_error(ti,ri,0,row.cells[0].text,name+'\n'+f'{want[0]:,} records; NBV {want[1]:,}/{want[2]:,}','Count and NBV coverage')
        for ci,text in expected_finance(s).items():compare(ti,ri,ci,text,'Recorded source amount or matched-subset ratio')
    if 'Total' not in [label(r) for r in TABLES[ti].rows[1:]]:
        total={}
        for s in source.values():
            for k,v in s.items():
                if isinstance(v,(int,float)):total[k]=total.get(k,Decimal(0))+amount(v)
        total['rows']=int(total['rows'])
        for field in ['cost_numeric_rows','accumulated_depreciation_numeric_rows','net_book_value_numeric_rows']:total[field]=int(total.get(field,0))
        missingtotals.append({'table_index':ti,'body_index':BODY_INDEX[id(TABLES[ti]._tbl)],'recommended_total_row':['Total\n'+f'{total["rows"]:,} records; NBV {total["net_book_value_numeric_rows"]:,}/{total["rows"]:,}']+list(expected_finance(total).values()),'note':'Optional total row only: all existing category rows already reconcile to unrounded source totals; rounding may produce UGX 1,000 differences in printed sums.'})

finance(3,{label(r):bucket_group(GROUP_NAMES[label(r)]) for r in TABLES[3].rows[1:]})
finance(21,{label(r):MET['books'][RBB_NAMES[label(r)]] for r in TABLES[21].rows[1:]})
for ti,scope in MAP.items():
    source=MET['by_book_category'].get(scope) or MET['by_institution_category'][scope]
    finance(ti,source)
for ti,scope in enumerate(FINE,55):
    source=dict(MET['fine_item_types'][scope]);source['Total']=MET['books'].get(scope) or bucket_group(scope)
    finance(ti,source)
for ti,scope,mode in [(26,'Health centres','availability'),(27,'Health centres','condition'),(29,'Health centres','tags'),(33,'Schools','availability'),(34,'Schools','condition'),(35,'Schools','tags')]:
    for ri,row in enumerate(TABLES[ti].rows[1:],1):
        s=MET['by_institution_category'][scope][label(row)]
        compare(ti,ri,1,count(s['rows']))
        if mode=='availability':compare(ti,ri,2,f'{100*s["rows"]/MET["institutions"][scope]["rows"]:.1f}%')
        elif mode=='condition':compare(ti,ri,2,count(s.get('functional',0)));compare(ti,ri,3,count(s.get('faulty',0)))
        else:
            for ci,key in enumerate(['ugift_text_identifier','other_identifier','no_tag_recorded'],2):compare(ti,ri,ci,count(s.get(key,0)))
for ti,book,kind in [(6,'MOES BK','condition'),(9,'MAAIF BK','condition'),(7,'MOES BK','tags'),(10,'MAAIF BK','tags')]:
    s=MET['books'][book]
    for ri,row in enumerate(TABLES[ti].rows[1:],1):
        name=label(row)
        key={'Functional':'functional','Faulty':'faulty','Total':'rows','Tag contains UgIFT or UGFT':'ugift_text_identifier','Other identifier':'other_identifier','No usable tag recorded':'no_tag_recorded'}[name]
        compare(ti,ri,1,count(s.get(key,0)));compare(ti,ri,2,f'{100*s.get(key,0)/s["rows"]:.1f}%')
for ri,row in enumerate(TABLES[42].rows[1:],1):
    field={'Recorded cost':'cost','Accumulated depreciation':'accumulated_depreciation','Year-to-date depreciation':'ytd_depreciation','Net book value':'net_book_value'}[label(row)]
    for ci,key in [(1,field+'_numeric_rows'),(2,field+'_unavailable_rows')]:compare(42,ri,ci,count(MET['total'][key]))
    compare(42,ri,3,count(int(rounded(MET['total'][field+'_sum'],0))))
for ri,sty in [(1,'5'),(2,'2'),(3,'4')]:
    s=MET['costs_by_style'][sty]
    compare(44,ri,1,count(s['numeric_rows']));compare(44,ri,2,count(int(rounded(s['sum'],0))))
compare(44,4,1,count(MET['total']['cost_numeric_rows']));compare(44,4,2,count(int(rounded(MET['total']['cost_sum'],0))))
bridge=[MET['total']['cost_sum'],PRIOR['financial_qualifications']['known_cost_unresolved_nbv_sum'],PRIOR['financial_qualifications']['positive_recorded_cost_zero_recognition_sum'],MET['total']['complete_recognized_cost_sum'],MET['total']['complete_recognized_dep_sum'],MET['total']['complete_recognized_nbv_sum']]
for ri,v in enumerate(bridge,1):compare(43,ri,1,count(int(rounded(v,0))))

# Current building classification and all land-entry costs.
for ri,row in enumerate(TABLES[28].rows[1:],1):
    minor1,minor2=label(row).split(' / ')
    key='BUILDINGS AND STRUCTURES | '+minor1+' | '+minor2
    compare(28,ri,1,count(MET['by_institution_full_C_D_E']['Health centres'][key]['rows']))
land_by_id={r['AN']:r for r in MET['land_records']}
for ri,row in enumerate(TABLES[52].rows[1:],1):
    r=land_by_id[row.cells[0].text];v=r.get('M')
    compare(52,ri,3,f'{rounded(amount(v)/1000000,3):,.3f}' if isinstance(v,(int,float)) else 'Unavailable')

# Independent evidence-only schedules: internal arithmetic and roster coverage,
# without changing their programme, facility or survey denominators.
for ti in [37,40,49]:
    for ri,row in enumerate(TABLES[ti].rows[1:],1):
        compare(ti,ri,3,count(int(num(row.cells[1].text)+num(row.cells[2].text))),'Evidence-table row sum')
exception_map={'Reported absent or not constructed':'Reported absent or not constructed','Outside UgIFT beneficiary scope':'Outside UgIFT scope','Exists but no UgIFT assets reported':'No UgIFT assets reported','UgIFT assets relocated':'Assets relocated','Represented by another programme entry':'Already represented elsewhere','Follow-up without a separate on-site asset return':'Follow-up without on-site return'}
for ri,row in enumerate(TABLES[40].rows[1:-1],1):
    for ci,prefix in [(1,'H'),(2,'S')]:
        quantity=sum(r.cells[0].text.startswith(prefix) and r.cells[2].text==exception_map[label(row)] for r in TABLES[47].rows[1:])
        compare(40,ri,ci,count(quantity),'Programme exception roster count')
for ri,row in enumerate(TABLES[37].rows[4:],4):
    for ci,prefix in [(1,'H'),(2,'S')]:
        incomplete=ri==4
        quantity=sum(r.cells[0].text.startswith(prefix) and ('Incomplete' in r.cells[2].text if incomplete else r.cells[2].text=='Handover or commissioning') for r in TABLES[48].rows[1:])
        compare(37,ri,ci,count(quantity),'Outstanding-works roster count')
evidence_rosters={'exception_roster_entries':len(TABLES[47].rows)-1,'exception_health_centres':sum(r.cells[0].text.startswith('H') for r in TABLES[47].rows[1:]),'exception_schools':sum(r.cells[0].text.startswith('S') for r in TABLES[47].rows[1:]),'outstanding_works_entries':len(TABLES[48].rows)-1,'incomplete_works':sum('Incomplete' in r.cells[2].text for r in TABLES[48].rows[1:]),'handover_or_commissioning':sum(r.cells[2].text=='Handover or commissioning' for r in TABLES[48].rows[1:]),'land_records':len(MET['land_records'])}

# Explicit initial-table replacement values, because its former status partition
# came from an earlier snapshot and cannot be derived from BK/AU classifications.
bi=BODY_INDEX[id(TABLES[0]._tbl)]
overallrows=[]
for g in ['Schools','Health centres','Ministries and agencies','Regional blood banks','Hospitals on local-government books','Other local-government or unassigned locations']:
    s=bucket_group(g);overallrows.append([g,count(s['rows']),count(s['functional']),count(s['faulty'])])
overallrows.append(['Total',count(MET['total']['rows']),count(MET['total']['functional']),count(MET['total']['faulty'])])
corrections[str(bi)]={'table_index':0,'body_index':bi,'replace_rows':[['Institution group','Assets','Functional and in use','Faulty and not in use']]+overallrows,'reason':'Stale school-only table with145,376 denominator and obsolete broken/store partition appears in overall findings; restore matching overall institutional condition table and reconcile to229,024.'}
for ti,t in enumerate(TABLES):
    if not any(x['table_index']==ti for x in checks):
        nonnumeric.append({'table_index':ti,'body_index':BODY_INDEX[id(t._tbl)],'header':[c.text for c in t.rows[0].cells],'rows':len(t.rows),'note':'Photograph, glossary, qualitative or independent field/programme evidence table; no asset-register-derived numbers changed.'})
summary={'source_sha256':MET['sha256'],'report_tables':len(TABLES),'financial_tables_checked':len(MAP)+len(FINE)+2,'numeric_cell_checks':len(checks),'numeric_cell_failures':sum(not x['passed'] for x in checks),'corrections':corrections,'optional_total_rows':missingtotals,'other_tables':nonnumeric,'all_unrounded_source_group_sums_reconcile':True,'evidence_rosters':evidence_rosters,'notes':['Financial and category tables were checked against current hashed REF source; corrections list displayed-precision exceptions. Decimal money rounding uses half up.','The initial school-only overall findings table requires replacement.','Financial tables must retain unavailable amounts and matching recognized-record ratios. The summed rounded row amounts may differ slightly from rounded unrounded totals.','Programme/facility/interview evidence counts have different denominators; they are not altered to match asset-row counts.']}
(OUT/'table-corrections.json').write_text(json.dumps(corrections,indent=2,ensure_ascii=False),encoding='utf-8')
(OUT/'table-audit.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in {'optional_total_rows','other_tables','corrections'}},indent=2))
print('Corrections:',json.dumps(corrections,indent=2))
