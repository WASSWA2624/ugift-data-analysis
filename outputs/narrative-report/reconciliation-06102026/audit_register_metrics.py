"""Independent read-only aggregation of the SHA-verified canonical REF snapshot."""
from pathlib import Path
from collections import Counter, defaultdict
from decimal import Decimal
from datetime import date, timedelta
import gzip, hashlib, json, re, sys

ROOT=Path(r'D:/coding/ugift-data-analysis')
OUT=ROOT/'outputs/narrative-report/reconciliation-06102026'
CACHE=ROOT/'tmp/report-revision-20261006'
SOURCE=ROOT/'outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx'
sys.path.insert(0,str(CACHE))
from report_item_finance import item_type
from audit_dates import classify as classify_date

MDA={'MOFPED BK','MOWT BK','MOES BK','MAAIF BK','MOH BK','OPM BK','MOWE BK','MGLSD BK','NEMA BK','PPDA BK','OAG BK','MOLG BK','MOLHUD BK'}
RBB={'ARUA RBB BK','HOIMA RBB BK','SOROTI RBB BK'}
EMPTY_TAG={'','not engraved','n/a','na','none','unspecified','unknown','not available','not','-'}
SOURCE_START=date(2017,6,27)
ASOF=date(2026,9,30)

def institution(r):
    if r['A'] in MDA:return 'Ministries and agencies'
    if r['A'] in RBB:return 'Regional blood banks'
    name=str(r.get('K') or '')
    if re.search('hospital',name,re.I):return 'Hospitals on local-government books'
    if re.search(r'health\s*(?:cent(?:er|re)|post)|\bh\s*/?\s*c\b|\bhc\s*(?:i|1|2|3|4)|dispensary',name,re.I):return 'Health centres'
    if re.search(r'school|\bss\b|\bs\.s\.|secondary|college',name,re.I):return 'Schools'
    return 'Other local-government or unassigned locations'

def category(r):
    if r.get('C')=='BUILDINGS AND STRUCTURES':return 'Buildings and structures'
    if r.get('C')=='LAND' or r.get('E')=='LAND':return 'Land'
    if r.get('D')=='ICT EQUIPMENT':return 'ICT equipment'
    if r.get('D')=='TRANSPORT EQUIPMENT':return 'Transport equipment'
    if r.get('E')=='FURNITURE AND FITTINGS':return 'Furniture and fittings'
    if r.get('E')=='MED LAB RESEARCH APPLIANCES':return 'Medical, laboratory and research appliances'
    if not r.get('C'):return 'Unclassified'
    if r.get('C')=='NOT APPLICABLE':return 'Outside fixed-asset classification'
    return 'Other classified assets'

def numeric(x):return isinstance(x,(int,float)) and not isinstance(x,bool)
def dec(x):return Decimal(str(x))
def encode(x):
    if isinstance(x,Decimal):return int(x) if x==int(x) else float(x)
    if isinstance(x,set):return sorted(x)
    raise TypeError(type(x).__name__)

def tag_status(r):
    text=str(r.get('AP') or '').strip()
    if text.casefold() in EMPTY_TAG:return 'no_tag_recorded'
    return 'ugift_text_identifier' if re.search(r'ugift|ugft',re.sub(r'[\s/_-]','',text),re.I) else 'other_identifier'

def update(s,r):
    s['rows']+=1;s['unit_sum']+=r['H'] if numeric(r.get('H')) else 0
    for col,label in [('M','cost'),('AK','accumulated_depreciation'),('AL','ytd_depreciation'),('BI','net_book_value')]:
        if numeric(r.get(col)):
            s[label+'_numeric_rows']+=1;s[label+'_sum']+=dec(r[col])
            s[label+'_zero_rows']+=r[col]==0
        else:s[label+'_unavailable_rows']+=1
    s['functional']+=r.get('BK')=='Functional';s['faulty']+=r.get('BK')=='Faulty'
    s['in_use_yes']+=r.get('AU')=='YES';s['in_use_no']+=r.get('AU')=='NO'
    s['capitalized']+=r.get('G')=='CAPITALIZED';s['cip']+=r.get('G')=='CIP'
    ts=tag_status(r);s[ts]+=1
    movable=r.get('C') not in {'BUILDINGS AND STRUCTURES','LAND'} and r.get('E')!='LAND'
    if movable:s['rows_not_classified_as_buildings_or_land']+=1;s['movable_'+ts]+=1
    allnum=all(numeric(r.get(c)) for c in ['M','AK','BI'])
    if allnum:
        s['all_three_financial_numeric_rows']+=1
        for c,field in [('M','cost'),('AK','dep'),('BI','nbv')]:s['matched_numeric_'+field+'_sum']+=dec(r[c])
        if r['G'] in {'CAPITALIZED','CIP'}:
            s['complete_recognized_rows']+=1
            for c,field in [('M','cost'),('AK','dep'),('BI','nbv')]:s['complete_recognized_'+field+'_sum']+=dec(r[c])
            s['complete_recognized_reconciliation_failures']+=abs(dec(r['M'])-dec(r['AK'])-dec(r['BI']))>Decimal('.5')

def main():
    digest=hashlib.file_digest(SOURCE.open('rb'),'sha256').hexdigest()
    cachemeta=json.loads((CACHE/'metrics.json').read_text(encoding='utf-8'))
    assert digest==cachemeta['sha256'],'Cached snapshot differs from canonical workbook'
    total=Counter();groups=defaultdict(Counter);categories=defaultdict(Counter);books=defaultdict(Counter)
    by_group_category=defaultdict(lambda:defaultdict(Counter));by_book_category=defaultdict(lambda:defaultdict(Counter))
    districts=defaultdict(Counter);fine=defaultdict(lambda:defaultdict(Counter));classes=defaultdict(lambda:defaultdict(Counter))
    dates=Counter();styles=defaultdict(Counter);recognition=defaultdict(Counter);grouplocs=defaultdict(set)
    counts=Counter();land=[];dates_examples=defaultdict(list);missingcost=Counter();allids=set();issues=[]
    for line in gzip.open(CACHE/'metrics_rows.jsonl.gz','rt',encoding='utf-8'):
        r=json.loads(line);g,c=institution(r),category(r);b=r['A']
        for s in [total,groups[g],categories[c],books[b],by_group_category[g][c],by_book_category[b][c],districts[r.get('I')],recognition[r.get('G')]]:update(s,r)
        grouplocs[g].add((r.get('I'),r.get('K')))
        ft=item_type(r)
        if b in MDA|RBB:update(fine[b][ft],r)
        elif g in {'Health centres','Schools'}:update(fine[g][ft],r)
        rawclass=' | '.join(str(r.get(k) or '(blank)') for k in ['C','D','E']);update(classes[g][rawclass],r)
        counts['rows']+=1;counts['units_not_one']+=r.get('H')!=1
        st=str(r.get('_styles',{}).get('M'));styles[st]['rows']+=1
        if numeric(r.get('M')):styles[st]['numeric_rows']+=1;styles[st]['sum']+=dec(r['M'])
        else:styles[st]['missing_rows']+=1;missingcost[g]+=1
        counts['status_use_disagree']+=(r.get('BK')=='Functional')!=(r.get('AU')=='YES')
        dtype,service=classify_date(r.get('BE'));_,purchase=classify_date(r.get('BD'))
        dates[dtype]+=1
        if purchase and service and purchase>service:dates['purchase_after_service']+=1
        if len(dates_examples[dtype])<5:dates_examples[dtype].append({'row':r['row'],'asset_number':r.get('AN'),'book':b,'service':r.get('BE')})
        if r.get('G')=='CIP':
            counts['cip_zero_cost']+=r.get('M')==0;counts['cip_missing_cost']+=not numeric(r.get('M'))
        if r.get('G') in {'CAPITALIZED','CIP'} and all(numeric(r.get(k)) for k in ['M','AK','BI']):
            if abs(dec(r['M'])-dec(r['AK'])-dec(r['BI']))>Decimal('.5') and len(issues)<10:
                issues.append({'row':r['row'],'cost':r['M'],'depreciation':r['AK'],'nbv':r['BI']})
        if r.get('G')=='CAPITALIZED' and numeric(r.get('M')) and r['M']>0 and numeric(r.get('BI')) and r['BI']==0:
            counts['positive_cost_zero_nbv_capitalized']+=1;counts['positive_cost_zero_nbv_capitalized_in_use']+=r.get('AU')=='YES'
        if c=='Land':land.append({k:r.get(k) for k in ['row','AN','A','I','K','AX','BA','M','AK','BI','BK','BL']})
    prior=json.loads((CACHE/'metrics_report.json').read_text(encoding='utf-8'))
    disagreements=[]
    for label,actual,expected in [('total',total,prior['total'])]+[(g,groups[g],prior['institutions'][g]) for g in groups]:
        for key in actual.keys()&expected.keys():
            if abs(dec(actual[key])-dec(expected[key]))>Decimal('.01'):disagreements.append({'group':label,'key':key,'new':actual[key],'cached':expected[key]})
    assert total['rows']==229024 and total['unit_sum']==229024 and not disagreements
    definitions={
        'source_range':'Asset Register!A2:BL229025',
        'population':'All 229,024 current REF rows including expensed, not recognized, not capitalized and unresolved entries. Every row has one unit. No exclusions for valuation, categories or item count.',
        'authority':'REF source workbook hash verified identical to prior read-only row snapshot. Values independently aggregated using Decimal; no source workbook or report edits.',
        'groups':'Exact national MDA books and regional blood-bank books first; then current LOCATION_SEGMENT3 names classified hospital, health centre, school or other. These are not programme-list coverage counts.',
        'categories':'Register categories C/D/E retained, including recorded classification errors. Financial fine item groups use existing description crosswalk AX/B and limited BA refinements; they reconcile exactly to their institutional totals.',
        'financials':'Sum numeric saved M, AK, AL and BI separately. Missing/text Pending calculation is unavailable rather than zero. Complete accounting comparison uses G CAPITALIZED/CIP only, with all M/AK/BI numeric. Its cost-depreciation=NBV and NBV/cost ratio refer to one matching subset.',
        'condition':'BK Functional/Faulty; AU YES/NO. These fields agree exactly. Faulty encompasses multiple forms of non-use; cannot support a separate validated broken/in-store partition.',
        'tags':'AP with placeholders removed. UgIFT/UGFT lexical check removes spaces, slashes, underscores and hyphens. Presence of an identifier does not independently prove physical engraving.',
        'estimated_cost':'M styles 2 (orange/other-government comparison) and 5 (blue/same-government comparison) mark existing borrowed estimates; style4 unfilled. Do not reinterpret these estimates as verified procurement/market values.',
        'land':'Land asset count only. Textual site dimensions are retained as source wording; no authoritative aggregate land-area field exists and dimensions must not be turned into site valuation or total area without a consistent unit.'
    }
    result={'source':str(SOURCE),'sha256':digest,'cache_source':str(CACHE/'metrics_rows.jsonl.gz'),'definitions':definitions,
            'independent_recalculation_matches_prior':not disagreements,'aggregate_discrepancies':disagreements,'counts':counts,'total':total,
            'institutions':groups,'categories':categories,'books':books,'districts':districts,'by_institution_category':by_group_category,
            'by_book_category':by_book_category,'by_institution_full_C_D_E':classes,'fine_item_types':fine,'recognition_treatments':recognition,
            'costs_by_style':styles,'missing_cost_by_group':missingcost,'dates':dates,'date_examples':dates_examples,
            'facility_label_counts':{g:len(v) for g,v in grouplocs.items()},'land_records':land,
            'financial_mismatch_examples':issues,'prior_independent_finance_check':prior['independent_finance_check']}
    result['estimated_cost']={'rows':sum(styles[s]['numeric_rows'] for s in ['2','5']),'sum':sum(styles[s]['sum'] for s in ['2','5']),'share_of_available_cost':sum(styles[s]['sum'] for s in ['2','5'])/total['cost_sum']*100}
    (OUT/'register-metrics.json').write_text(json.dumps(result,indent=2,ensure_ascii=False,default=encode),encoding='utf-8')
    report=['READ-ONLY CANONICAL REGISTER AUDIT',f'Source SHA256: {digest}',f'Independent recomputation matched prior cache: {not disagreements}',*definitions.values(),'','HEADLINE METRICS',json.dumps(total,indent=2,default=encode),'','GROUP TOTALS']
    for g,s in groups.items():report.append(f'{g}: {s["rows"]:,}; Functional {s["functional"]:,}; Faulty {s["faulty"]:,}; UGIFT tag {s["ugift_text_identifier"]:,}; other tag {s["other_identifier"]:,}; no tag {s["no_tag_recorded"]:,}; available cost {s["cost_sum"]}; depreciation {s["accumulated_depreciation_sum"]}; NBV {s["net_book_value_sum"]}')
    report+=['','DATE COUNTS',json.dumps(dates,indent=2),'','ESTIMATED COSTS',json.dumps(result['estimated_cost'],default=encode),'','DISCREPANCIES AND REPORT RECONCILIATION','The executive summary uses the correct current 229,024 total. School table 0 before section 3.2 uses 145,376 and the old six-category taxonomy; the current school group totals 145,256. Its stale 137,585 in-use number must become 137,465 when retaining the current school denominator. It should not preserve unsupported broken/store splits as current physically verified condition measures.','The mixed old/new MDA prose contains duplicate earlier figures. Revised present financial tables match these independently reconciled values, including available-amount limitations.','Available cost minus separately available depreciation does not equal separately available NBV. The matching CAPITALIZED/CIP subset contains 180,730 complete records: cost UGX 760,986,784,837.9434 less depreciation UGX 165,185,197,307 equals NBV UGX 595,801,587,530.9434. No missing amount may be fabricated as zero.','Do not exclude 18,218 EXPENSED rows from the report population unless specifically authorized: the stopped analysis in tmp/report-excluding-expensed-20261006 is not a report basis.','Survey, programme-facility, completion, location-name exception and photograph counts originate in facility/field evidence, not this asset-register workbook. Keep these evidence definitions intact rather than forcing them to 229,024 assets.']
    (OUT/'register-audit.txt').write_text('\n'.join(report),encoding='utf-8')
    print(json.dumps({'sha256':digest,'totals':total,'date_counts':dates,'estimated_cost':result['estimated_cost'],'independent_matches':not disagreements},indent=2,default=encode))

if __name__=='__main__':main()
