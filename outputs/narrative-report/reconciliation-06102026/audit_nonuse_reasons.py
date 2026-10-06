"""Reapply documented reason rules to current REF remarks for NO rows only.

This is a source-wording screen, not proof that a particular physical asset is
damaged. The normalized generic Faulty label and finance-review metadata are
removed so they cannot turn all unused rows into a damaged count.
"""
import gzip,json,re,sys
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(r'D:/coding/ugift-data-analysis');OUT=ROOT/'outputs/narrative-report/reconciliation-06102026'
sys.path.insert(0,str(ROOT/'tmp/narrative-report-2809/analysis'))
import utilization_rules as R
sys.path.insert(0,str(OUT))
from audit_register_metrics import institution

comp=R.compile_rules();counts=Counter();groups=defaultdict(Counter);samples=defaultdict(list);memo={}
for line in gzip.open(ROOT/'tmp/report-revision-20261006/metrics_rows.jsonl.gz','rt',encoding='utf-8'):
    d=json.loads(line)
    if d.get('AU')!='NO':continue
    note=str(d.get('BL') or '')
    # Current remarks begin with the generic reconciled BK label. It has no
    # specific cause information and is excluded from reason attribution.
    note=re.sub(r'^\s*Faulty\.\s*','',note,flags=re.I)
    note=re.split(r'(?i);\s*(?:Date review\s*\(|REF cost review|Cost review\s*\(|Department/location review)',note)[0]
    # Separate accounting/provenance labels from equipment findings.
    note='; '.join(p.strip() for p in note.split(';') if not re.match(r'(?i)^\s*(?:cost|recoverable cost|engraving|financial|depreciation|source file|source location|date|purchase date|placed.in.service date|life in months|life|asset type|finance review)\s*:',p))
    building=d.get('C')=='BUILDINGS AND STRUCTURES'
    text=R.clean_text('','',note,building)
    if text not in memo:
        flags=R.flags(comp,text);primary=R.primary(flags);memo[text]=(R.REPORT_CATEGORY.get(primary,primary),flags)
    key,flags=memo[text];counts[key]+=1;groups[institution(d)][key]+=1
    if len(samples[key])<8:samples[key].append({'row':d['row'],'asset_number':d.get('AN'),'facility':d.get('K'),'item':d.get('AX'),'source_remarks':d.get('BL'),'classification_text':text})
assert sum(counts.values())==13520
result={'source_sha256':json.loads((OUT/'register-metrics.json').read_text(encoding='utf-8'))['sha256'],
 'population':'Current REF AU == NO, exactly 13,520 records.',
 'method':'Documented prior reason-rule precedence applied to current BL remarks, with generic leading Faulty label and accounting-review provenance removed. Every row assigned once. Reasons are wording-based; repeated aggregate remarks need physical validation before interpreting them as individual damage/storage counts.',
 'labels':{k:R.REPORT_LABELS[k] for k in counts},'counts':counts,'by_institution':groups,'samples':samples,
 'figure_pairs':[[R.REPORT_LABELS[k],v] for k,v in counts.most_common()],
 'note':'No-reason rows are explicit and remain in the denominator. This chart reports stated wording categories, not a confirmed broken/in-store condition partition.'}
(OUT/'nonuse-reasons.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'counts':counts,'figure_pairs':result['figure_pairs']},indent=2))
