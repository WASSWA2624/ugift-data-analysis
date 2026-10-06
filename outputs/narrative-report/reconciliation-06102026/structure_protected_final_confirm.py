from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,hashlib,re
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
fp=P.parent/'ugift-working-report-06102026-1344-reconciled.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def tx(e):return re.sub(r'\s+',' ',''.join(e.xpath('.//w:t/text()',namespaces=ns))).strip()
review=json.loads((P/'final-protected-wording-differences.json').read_text(encoding='utf-8'))
# The root authorized restoration of these three remaining original source-language tokens.
repairs={177:[('Health Centres at UGX','Health Centers at UGX'),('as indicated in table 2.','as indicated in the table 2.')],189:[('Office of the Prime Minister,','Office of the Prime minister,')]}
classes={149:'Complete the institution population so the narrative totals tally.',159:'Correct the non-use total and distinguish recorded Faulty status from waiting for installation.',161:'Identify the survey respondent denominator and multiple-response basis of Figure 2.',168:'Correct identifier counts, all-asset denominator, and UgIFT/UGFT classification.',169:'Align the MoES description to recorded identifier availability rather than inferred physical engraving.',177:'Correct financial totals, date, institutional population, available coverage and matched-accounting qualifications.',184:'Correct MDA record count and accounting-category quantities/coverage.',185:'Correct MDA aggregate percentage and state its denominator.',189:'Correct faulty/functional totals and distinguish register condition from physical confirmation.',191:'Correct MDA identifier quantities, denominator and tag-field coverage.',195:'Authorized Table 2 reference identifying unavailable financial amounts.'}
z=ZipFile(fp);b=E.fromstring(z.read('word/document.xml')).find('w:body',ns)
oz=ZipFile(P.parent/'ugift-working-report-06102026-1344.docx');ob=E.fromstring(oz.read('word/document.xml')).find('w:body',ns)
first_heading=next(i for i,e in enumerate(ob) if e.xpath('./w:pPr/w:pStyle[starts-with(@w:val,"Heading")]',namespaces=ns) and tx(e).startswith('1 Introduction'))
review_heading=next(r['final_i'] for r in review['unchanged_paragraphs'] if r['original_i']==first_heading)
actual_heading=next(i for i,e in enumerate(b) if e.xpath('./w:pPr/w:pStyle[starts-with(@w:val,"Heading")]',namespaces=ns) and tx(e).startswith('1 Introduction'))
navigation_index_shift=actual_heading-review_heading
unexpected=[];verified=[]
for row in review['changed_paragraphs']:
 expected=row['final_text']
 for old,new in repairs.get(row['original_i'],[]):expected=expected.replace(old,new)
 actual=tx(b[row['final_i']+navigation_index_shift])
 rec={'original_i':row['original_i'],'final_i':row['final_i']+navigation_index_shift,'reason':classes.get(row['original_i']),'expected_text':expected,'actual_text':actual,'matches_completed_word_review':expected==actual}
 verified.append(rec)
 if expected!=actual:unexpected.append(rec)
unchanged=[]
for row in review['unchanged_paragraphs']:
 original=ob[row['original_i']]
 prior=re.sub(r'\s+',' ',''.join(''.join(r.xpath('.//w:t/text()',namespaces=ns)) for r in original.xpath('.//w:r',namespaces=ns) if not r.xpath('./w:rPr/w:highlight[@w:val="green"]',namespaces=ns))).strip()
 expected=prior or tx(original);actual=tx(b[row['final_i']+navigation_index_shift])
 if expected!=actual:unchanged.append({'original_i':row['original_i'],'final_i':row['final_i']+navigation_index_shift,'expected_text':expected,'actual_text':actual})
out={'sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'review_basis_sha256':review['sha256'],'protected_nonempty_paragraphs_reviewed':len(review['changed_paragraphs'])+len(review['unchanged_paragraphs']),'exactly_unchanged_paragraphs':len(review['unchanged_paragraphs']),'metric_and_coverage_paragraphs':len(verified),'metric_and_coverage_changes':verified,'unexpected_metric_paragraph_changes':unexpected,'unexpected_nonmetric_paragraph_changes':unchanged,'no_remaining_protected_nonmetric_wording_changes':not unexpected and not unchanged}
(P/'final-protected-wording-confirmation.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='metric_and_coverage_changes'},indent=2,ensure_ascii=False))
