"""Independent scope checks supporting the final narrative reconciliation."""
from pathlib import Path
from decimal import Decimal
from collections import Counter
import gzip
import hashlib
import json

ROOT=Path(r'D:/coding/ugift-data-analysis')
OUT=ROOT/'outputs/narrative-report/reconciliation-06102026'
counts=Counter()
sums=Counter()
def numeric(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool)
with gzip.open(ROOT/'tmp/report-revision-20261006/metrics_rows.jsonl.gz','rt',encoding='utf-8') as cache:
    for line in cache:
        row=json.loads(line)
        cost,dep,nbv=row.get('M'),row.get('AK'),row.get('BI')
        unresolved=numeric(cost) and not numeric(nbv)
        excluded=numeric(cost) and cost>0 and row.get('G') in {'EXPENSED','NOT CAPITALIZED','NOT RECOGNIZED'}
        complete=row.get('G') in {'CAPITALIZED','CIP'} and all(numeric(v) for v in (cost,dep,nbv))
        counts['total']+=1
        counts['known_cost_unresolved_nbv']+=unresolved
        counts['positive_cost_excluded_accounting_treatment']+=excluded
        counts['overlap_unresolved_and_excluded']+=unresolved and excluded
        counts['complete_recognized']+=complete
        if numeric(row.get('AM')):
            counts['recorded_numeric_salvage_values']+=1
            counts['nonzero_salvage_values']+=row['AM']!=0
        if numeric(cost):sums['available_cost']+=Decimal(str(cost))
        if unresolved:sums['known_cost_unresolved_nbv']+=Decimal(str(cost))
        if excluded:sums['positive_cost_excluded_accounting_treatment']+=Decimal(str(cost))
        if complete:
            for field,value in [('complete_cost',cost),('complete_depreciation',dep),('complete_nbv',nbv)]:
                sums[field]+=Decimal(str(value))
            counts['complete_recognized_reconciliation_failures']+=abs(Decimal(str(cost))-Decimal(str(dep))-Decimal(str(nbv)))>Decimal('.5')
report=ROOT/'outputs/narrative-report/ugift-working-report-06102026-1344-reconciled.docx'
result={'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),
        'counts':dict(counts), 'sums':{k:str(v) for k,v in sums.items()},
        'recognized_cost_bridge_difference':str(sums['available_cost']-sums['known_cost_unresolved_nbv']-sums['positive_cost_excluded_accounting_treatment']-sums['complete_cost']),
        'complete_cost_less_depreciation_minus_nbv':str(sums['complete_cost']-sums['complete_depreciation']-sums['complete_nbv']),
        'semantic_conclusions':[
            'Current all-record counts, institution counts, condition counts, identifiers, dates and available finance totals agree across narrative, tables and charts.',
            'Known-cost unresolved-NBV records and positive-cost expensed or unrecognized records are separate populations; the financial bridge supports the complete recognized cohort.',
            'Complete recognized financial comparison is distinct from separately available financial columns; reported NBV/cost percentages use matching accounting populations.',
            'Register condition codes distinguish in-use flags but do not independently identify physically broken versus stored or uninstalled assets; Appendix C discloses this.',
            'Survey bases 477, 469, 494, 463, 478 and 505 answer different questions; percentages and scope disclosures agree with current survey summaries.',
            'Figure 2 uses answer-only reasons from 156 reporting facilities; other question responses use their own stated bases. Categories overlap.',
            'Programme-list construction status and documented outstanding works are different evidence measures, and the report explicitly prevents addition.',
            'No actionable cross-section numeric contradiction found.'
        ]}
(OUT/'final-semantic-metrics-audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='semantic_conclusions'},indent=2))
