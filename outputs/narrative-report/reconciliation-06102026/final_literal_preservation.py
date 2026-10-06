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
with ZipFile(P.parent/'ugift-working-report-06102026-1344.docx') as z:
    original=E.fromstring(z.read('word/document.xml')).find('w:body',N)
audit={'source_sha256':sha256(F.read_bytes()).hexdigest(),'paragraphs':[]}
source=ast.parse((P/'final_reference_revision.py').read_text(encoding='utf-8'))
helpers=ast.Module(body=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in {'replace_span','revise'}],type_ignores=[])
exec(compile(helpers,'run_preserving_editor','exec'),globals())
edits=[
    ('By location, most MDA assets','three Lenovo ThinkPad laptops, one HP LaserJet printer','three Lenovo think pad Laptops, one HP Laser Jet Color Printer',185),
    ('At MDA level, there were 16,663 asset records','Figure 5 below shows','The figure 5 below shows',191),
    ('Overall, the 229,024 assets across the different institutions','Health Centres','Health Centers',177),
    ('Overall, the 229,024 assets across the different institutions','as indicated in table 2','as indicated in the table 2',177),
    ('At MDA level, apart from sixteen faulty assets','Prime Minister','Prime minister',189),
]
for prefix,old,new,source_index in edits:
    p=next(p for p in body if text(p).startswith(prefix))
    original_text=''.join(text(r) for r in original[source_index].xpath('.//w:r',namespaces=N) if not r.xpath('./w:rPr/w:highlight[@w:val="green"]',namespaces=N))
    assert ' '.join(new.split()) in ' '.join(original_text.split()),(source_index,new,repr(original_text))
    if old not in text(p) and new in text(p):continue
    assert old in text(p)
    revise(p,text(p).replace(old,new))
parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(F,'w',ZIP_DEFLATED) as z:
    for name,data in parts.items():z.writestr(name,data)
audit['output_sha256']=sha256(F.read_bytes()).hexdigest()
(P/'final-literal-preservation.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print('Exact source wording restored in protected paragraphs; metrics unchanged.')
