"""Undo reference-style changes within the user's protected sections."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from difflib import SequenceMatcher
from hashlib import sha256
import ast,json

P=Path(__file__).resolve().parent
F=P.parent/'ugift-working-report-06102026-1344-reconciled.docx'
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
text=lambda p:''.join(p.xpath('.//w:t/text()',namespaces=N))
with ZipFile(F) as z:parts={n:z.read(n) for n in z.namelist()}
root=E.fromstring(parts['word/document.xml'])
body=root.find('w:body',N)
boundary=next(i for i,p in enumerate(body) if text(p).startswith('3.3 MDA specific') and p.xpath('./w:pPr/w:pStyle[@w:val="Heading2"]',namespaces=N))
audit={'source_sha256':sha256(F.read_bytes()).hexdigest(),'paragraphs':[]}
# Reuse the run-preserving text editor without executing the authoring script.
source=ast.parse((P/'final_reference_revision.py').read_text(encoding='utf-8'))
helpers=ast.Module(body=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in {'replace_span','revise'}],type_ignores=[])
exec(compile(helpers,'run_preserving_editor','exec'),globals())
changes=json.loads((P/'final-reference-changes.json').read_text(encoding='utf-8'))['paragraphs'][44:]
for entry in changes:
    matches=[p for p in list(body)[:boundary] if text(p)==entry['text']]
    if matches:
        assert len(matches)==1
        revise(matches[0],entry['old_text'])
assert len(audit['paragraphs'])==6
parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(F,'w',ZIP_DEFLATED) as z:
    for name,data in parts.items():z.writestr(name,data)
audit['output_sha256']=sha256(F.read_bytes()).hexdigest()
(P/'protected-reference-wording-restored.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print('Restored original reference wording in six protected paragraphs; reconciled numbers unchanged.')
