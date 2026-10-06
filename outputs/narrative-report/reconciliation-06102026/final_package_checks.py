from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from hashlib import sha256
from collections import Counter
import json,re,posixpath

WORK=Path(__file__).resolve().parent
REPORT=WORK.parent/'ugift-working-report-06102026-1344-reconciled.docx'
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def text(x):return ''.join(x.xpath('.//w:t/text()',namespaces=N))
with ZipFile(REPORT) as z:
    names=set(z.namelist())
    root=E.fromstring(z.read('word/document.xml'))
    body=root.find('w:body',N)
    rels=E.fromstring(z.read('word/_rels/document.xml.rels'))
    targets={r.get('Id'):r.get('Target') for r in rels}
    chart_errors=[]
    for p in body:
        c=p.find('.//c:chart',N)
        if c is None:continue
        rid=c.get('{'+N['r']+'}id')
        chart=E.fromstring(z.read('word/'+targets[rid]))
        next_p=p.getnext()
        if next_p is None or not re.match(r'^Figure\s+\d+\s*:',text(next_p).strip()):chart_errors.append({'relationship':rid,'problem':'caption does not immediately follow graph'})
        if chart.find('.//c:title',N) is not None:chart_errors.append({'relationship':rid,'problem':'embedded title remains'})
        if chart.find('.//c:roundedCorners',N).get('val')!='0':chart_errors.append({'relationship':rid,'problem':'rounded corners'})
    link_errors=[]
    for name in names:
        if not name.endswith('.rels'):continue
        directory=posixpath.dirname(posixpath.dirname(name))
        for rel in E.fromstring(z.read(name)):
            if rel.get('TargetMode')=='External':continue
            target=rel.get('Target','')
            resolved=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(directory,target))
            if resolved not in names:link_errors.append({'part':name,'target':resolved})
    flags={
        'tables':len(root.xpath('./w:body/w:tbl',namespaces=N)),
        'native_charts':len(root.xpath('.//c:chart',namespaces=N)),
        'strike_count':len(root.xpath('.//w:strike',namespaces=N)),
        'highlight_colours':sorted(set(root.xpath('.//w:highlight/@w:val',namespaces=N))),
        'chart_checks':chart_errors,
        'unresolved_package_targets':link_errors,
        'toc_title_present':any(text(p).strip()=='Table of Contents' for p in body if p.tag.endswith('}p')),
        'bookmark_errors':bool(root.xpath('.//w:t[contains(.,"Error! Bookmark")]',namespaces=N)),
        'sha256':sha256(REPORT.read_bytes()).hexdigest(),
    }
    (WORK/'final-package-checks.json').write_text(json.dumps(flags,indent=2),encoding='utf-8')
    print(json.dumps(flags,indent=2))
    assert not chart_errors and not link_errors
    assert flags['strike_count']==0 and flags['highlight_colours']==['green']
    assert flags['toc_title_present'] and not flags['bookmark_errors']
