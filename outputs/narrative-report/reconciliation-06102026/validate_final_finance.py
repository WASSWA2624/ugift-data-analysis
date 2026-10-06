"""Read-only audit of all final category and detailed finance tables."""
from pathlib import Path
from docx import Document
from hashlib import sha256
import json
import re

OUT = Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
namespace = {}
source = (OUT/'audit_report_tables.py').read_text(encoding='utf-8').split('finance(3,')[0]
exec(compile(source, str(OUT/'audit_report_tables.py'), 'exec'), namespace)
namespace['DOC'] = Document(OUT.parent/'ugift-working-report-06102026-1344-reconciled.docx')
namespace['TABLES'] = namespace['DOC'].tables
namespace['BODY_INDEX'] = {id(node):i for i,node in enumerate(namespace['DOC'].element.body)}
tables, met = namespace['TABLES'], namespace['MET']
original_label = namespace['label']
def label(row):
    text = original_label(row)
    return 'Total' if re.match(r'^Total(?:\s|$)', text) else text
namespace['label'] = label
finance = namespace['finance']
groups = namespace['GROUP_NAMES']
all_groups = {label(row): met['total'] if label(row)=='Total' else met['institutions'][groups[label(row)]] for row in tables[3].rows[1:]}
finance(3, all_groups)
banks = {label(row): met['institutions']['Regional blood banks'] if label(row)=='Total' else met['books'][namespace['RBB_NAMES'][label(row)]] for row in tables[21].rows[1:]}
finance(21, banks)
checked_tables = [3, 21]
for original_index, scope in namespace['MAP'].items():
    index = original_index + (1 if original_index >= 52 else 0)
    category_source = dict(met['by_book_category'].get(scope) or met['by_institution_category'][scope])
    if any(label(row)=='Total' for row in tables[index].rows[1:]):
        category_source['Total'] = met['books'].get(scope) or met['institutions'][scope]
    finance(index, category_source)
    checked_tables.append(index)
for index, scope in enumerate(namespace['FINE'], 56):
    fine_source = dict(met['fine_item_types'][scope])
    fine_source['Total'] = met['books'].get(scope) or met['institutions'][scope]
    finance(index, fine_source)
    checked_tables.append(index)
result = {'report_sha256': sha256((OUT.parent/'ugift-working-report-06102026-1344-reconciled.docx').read_bytes()).hexdigest(),
          'tables_checked': len(checked_tables), 'cells_checked': len(namespace['checks']),
          'failed_cells': len([c for c in namespace['checks'] if not c['passed']]),
          'corrections': namespace['corrections'], 'missing_total_rows': namespace['missingtotals']}
(OUT/'final-financial-table-validation.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='missing_total_rows'}, indent=2, ensure_ascii=False))
