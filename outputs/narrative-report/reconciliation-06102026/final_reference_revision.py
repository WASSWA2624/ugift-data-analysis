"""Apply precise references and restore requested objective list formatting."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
from difflib import SequenceMatcher
from hashlib import sha256
import json
import re

P = Path(__file__).resolve().parent
F = P.parent / 'ugift-working-report-06102026-1344-reconciled.docx'
N = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
Q = lambda name: '{'+N['w']+'}'+name
text = lambda el: ''.join(el.xpath('.//w:t/text()', namespaces=N))
recipe = json.loads((P/'figure-table-reference-exact.json').read_text(encoding='utf-8'))
assert sha256(F.read_bytes()).hexdigest() == recipe['source_sha256']
with ZipFile(F) as z:
    parts = {name: z.read(name) for name in z.namelist()}
root = E.fromstring(parts['word/document.xml'])
body = root.find('w:body', N)
blocks = list(body)
boundary = next(i for i,p in enumerate(blocks) if text(p).startswith('3.3 MDA specific') and p.xpath('./w:pPr/w:pStyle[@w:val="Heading2"]',namespaces=N))
audit = {'source_sha256': recipe['source_sha256'], 'paragraphs': [], 'captions': [], 'objective_numbering': []}

def replace_span(p, start, end, replacement):
    nodes = p.xpath('.//w:t', namespaces=N)
    offset = 0
    positions = []
    for t in nodes:
        value = t.text or ''
        positions.append((t, offset, offset+len(value)))
        offset += len(value)
    if start == offset:
        assert nodes
        nodes[-1].text = (nodes[-1].text or '') + replacement
        return
    inserted = False
    for t, lo, hi in positions:
        if hi <= start or lo >= end and not (start == end and lo <= start < hi):
            continue
        old = t.text or ''
        a, b = max(0, start-lo), min(len(old), end-lo)
        t.text = old[:a] + (replacement if not inserted else '') + old[b:]
        t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
        inserted = True
    assert inserted, (start,end,replacement)

def revise(p, value):
    old = text(p)
    for tag,a,b,c,d in reversed(SequenceMatcher(a=old,b=value,autojunk=False).get_opcodes()):
        if tag != 'equal':
            replace_span(p,a,b,value[c:d])
    assert text(p) == value
    if old != value:
        audit['paragraphs'].append({'old_text':old,'text':value})

for entry in recipe['paragraph_corrections']:
    i = entry['body_index_at_audit']
    p = blocks[i]
    assert text(p) == entry['exact_old_text'], (i,text(p))
    assert i >= boundary or i == recipe['protected_reference_validation']['actual_section3_3_heading_index']-1
    revise(p,entry['text'])

# Standardize numbered citations only after the protected section 3.2.
for p in blocks[boundary:]:
    if p.tag != Q('p'):
        continue
    value = text(p)
    value = re.sub(r'\b(figure|table)(s?)\s+(\d+)',lambda m:m.group(1).capitalize()+m.group(2)+' '+m.group(3),value,flags=re.I)
    value = re.sub(r'\b((?:Figure|Table)s?\s+\d+(?:\s+to\s+\d+)?)\s+(?:below|above)\b',r'\1',value)
    value = re.sub(r'\b(?:below|above)\s+in\s+((?:Figure|Table)s?\s+\d+)',r'in \1',value)
    revise(p,value)

def paragraph(value, style, green=True):
    p = E.Element(Q('p'))
    pr = E.SubElement(p,Q('pPr'))
    E.SubElement(pr,Q('pStyle')).set(Q('val'),style)
    E.SubElement(pr,Q('keepNext'))
    r = E.SubElement(p,Q('r'))
    rp = E.SubElement(r,Q('rPr'))
    if green:
        E.SubElement(rp,Q('highlight')).set(Q('val'),'green')
    E.SubElement(r,Q('t')).text = value
    return p

for exact, entry in recipe['table_caption_insertions_by_exact_table_text'].items():
    table = blocks[entry['body_index_at_audit']]
    assert table.tag == Q('tbl') and text(table) == exact
    table.addprevious(paragraph(entry['caption'],'Caption'))
    audit['captions'].append(entry['caption'])
for entry in recipe['paragraph_insertions']:
    table = blocks[entry['body_index_at_audit']]
    assert text(table) == entry['before_exact_table_text']
    table.getprevious().addprevious(paragraph(entry['text'],'Normal'))

# A separate native list prevents changes to other existing numbered lists.
numbering = E.fromstring(parts['word/numbering.xml'])
num_id = max(int(x.get(Q('numId'))) for x in numbering.findall('w:num',N)) + 1
abstract_id = max(int(x.get(Q('abstractNumId'))) for x in numbering.findall('w:abstractNum',N)) + 1
starts = ['Increase the adequacy','Improve the equity','Strengthen performance','Expand access']
objectives = [next(p for p in blocks if text(p).startswith(start)) for start in starts]
old_id = objectives[0].find('w:pPr/w:numPr/w:numId',N).get(Q('val'))
old_num = numbering.xpath('./w:num[@w:numId=$v]',namespaces=N,v=old_id)[0]
old_abstract_id = old_num.find('w:abstractNumId',N).get(Q('val'))
abstract = deepcopy(numbering.xpath('./w:abstractNum[@w:abstractNumId=$v]',namespaces=N,v=old_abstract_id)[0])
abstract.set(Q('abstractNumId'),str(abstract_id))
nsid = abstract.find('w:nsid',N)
if nsid is not None:
    nsid.set(Q('val'),'6F626A31')
level = abstract.xpath('./w:lvl[@w:ilvl="0"]',namespaces=N)[0]
level.find('w:start',N).set(Q('val'),'1')
level.find('w:numFmt',N).set(Q('val'),'lowerLetter')
level.find('w:lvlText',N).set(Q('val'),'%1)')
numbering.insert(len(numbering.findall('w:abstractNum',N)),abstract)
num = E.SubElement(numbering,Q('num'))
num.set(Q('numId'),str(num_id))
E.SubElement(num,Q('abstractNumId')).set(Q('val'),str(abstract_id))
for p in objectives:
    p.find('w:pPr/w:numPr/w:numId',N).set(Q('val'),str(num_id))
    audit['objective_numbering'].append({'text':text(p),'format':'a), b), c), d)'})

parts['word/document.xml'] = E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
parts['word/numbering.xml'] = E.tostring(numbering,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(F,'w',ZIP_DEFLATED) as z:
    for name,data in parts.items():
        z.writestr(name,data)
audit['output_sha256'] = sha256(F.read_bytes()).hexdigest()
(P/'final-reference-changes.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'revised_paragraphs':len(audit['paragraphs']),'numbered_table_captions':len(audit['captions']),'restored_objectives':len(audit['objective_numbering']),'sha256':audit['output_sha256']},indent=2))
