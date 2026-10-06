"""Preserve report prose and package while reconciling metrics and Word charts."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import gzip
import hashlib
import json
import math
import re

from lxml import etree as E
from openpyxl import Workbook

WORK = Path(__file__).resolve().parent
ROOT = WORK.parents[2]
REPORTS = WORK.parent
CACHE = ROOT / 'tmp/report-revision-20261006'
SOURCE = REPORTS / 'ugift-working-report-06102026-1344.docx'
REFERENCE = REPORTS / 'ugift-working-report-06102026-0000.docx'
DEST = REPORTS / 'ugift-working-report-06102026-1344-reconciled.docx'
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'pr': 'http://schemas.openxmlformats.org/package/2006/relationships',
    'ct': 'http://schemas.openxmlformats.org/package/2006/content-types',
}

def q(name):
    prefix, local = name.split(':')
    return f'{{{NS[prefix]}}}{local}'

def node(name, attrs=None, text=None):
    el = E.Element(q(name))
    for key, value in (attrs or {}).items():
        el.set(q(key) if ':' in key else key, str(value))
    el.text = text
    return el

def txt(el):
    return ''.join(el.xpath('.//w:t/text()', namespaces=NS))

def clean_space(value):
    return re.sub(r'\s+', ' ', value).strip()

def run_is_green(r):
    return bool(r.xpath('./w:rPr/w:highlight[@w:val="green"]', namespaces=NS))

def accepted(el):
    return ''.join(txt(r) for r in el.xpath('.//w:r', namespaces=NS)
                   if not r.xpath('./w:rPr/w:strike[not(@w:val="0")]', namespaces=NS))

def set_paragraph(p, value, green=False):
    exemplar = next((r.find('w:rPr', NS) for r in p.findall('w:r', NS)
                     if r.find('w:rPr', NS) is not None), None)
    for child in list(p):
        if child.tag != q('w:pPr'):
            p.remove(child)
    r = node('w:r')
    props = deepcopy(exemplar) if exemplar is not None else node('w:rPr')
    for el in list(props):
        if E.QName(el).localname in {'highlight', 'strike', 'dstrike'}:
            props.remove(el)
    if green:
        props.append(node('w:highlight', {'w:val': 'green'}))
    r.append(props)
    t = node('w:t', text=value)
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r.append(t)
    p.append(r)

def mark(el, green=False):
    for r in el.xpath('.//w:r', namespaces=NS):
        props = r.find('w:rPr', NS)
        if props is None:
            props = node('w:rPr')
            r.insert(0, props)
        for old in list(props):
            if E.QName(old).localname in {'highlight', 'strike', 'dstrike'}:
                props.remove(old)
        if green and txt(r).strip():
            props.append(node('w:highlight', {'w:val': 'green'}))
    for props in el.xpath('.//w:pPr/w:rPr', namespaces=NS):
        for old in list(props):
            if E.QName(old).localname in {'highlight', 'strike', 'dstrike'}:
                props.remove(old)

def paragraph(value, style='Caption', green=False):
    p = node('w:p')
    pr = node('w:pPr')
    pr.append(node('w:pStyle', {'w:val': style}))
    p.append(pr)
    set_paragraph(p, value, green)
    return p

def cell(value, width, header=False, green=False):
    tc = node('w:tc')
    pr = node('w:tcPr')
    pr.append(node('w:tcW', {'w:w': width, 'w:type': 'dxa'}))
    pr.append(node('w:vAlign', {'w:val': 'center'}))
    if header:
        pr.append(node('w:shd', {'w:fill': 'E7ECF0'}))
    tc.append(pr)
    p = paragraph(str(value), style='Normal', green=green)
    ppr = p.find('w:pPr', NS)
    ppr.append(node('w:spacing', {'w:before': 60, 'w:after': 60, 'w:line': 240, 'w:lineRule': 'auto'}))
    rpr = p.find('w:r/w:rPr', NS)
    rpr.append(node('w:rFonts', {'w:ascii': 'Times New Roman', 'w:hAnsi': 'Times New Roman'}))
    rpr.append(node('w:sz', {'w:val': 17}))
    if header:
        rpr.append(node('w:b'))
    tc.append(p)
    return tc

def table(headers, rows, widths, green=False):
    t = node('w:tbl')
    pr = node('w:tblPr')
    pr.append(node('w:tblW', {'w:w': sum(widths), 'w:type': 'dxa'}))
    pr.append(node('w:tblLayout', {'w:type': 'fixed'}))
    borders = node('w:tblBorders')
    for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        borders.append(node('w:' + side, {'w:val': 'single', 'w:sz': 4, 'w:color': 'D9D9D9'}))
    pr.append(borders)
    margins = node('w:tblCellMar')
    for side in ['top', 'left', 'bottom', 'right']:
        margins.append(node('w:' + side, {'w:w': 70, 'w:type': 'dxa'}))
    pr.append(margins)
    t.append(pr)
    grid = node('w:tblGrid')
    for width in widths:
        grid.append(node('w:gridCol', {'w:w': width}))
    t.append(grid)
    for i, values in enumerate([headers, *rows]):
        tr = node('w:tr')
        trpr = node('w:trPr')
        if i == 0:
            trpr.append(node('w:tblHeader'))
        tr.append(trpr)
        for j, value in enumerate(values):
            tr.append(cell(value, widths[j], i == 0, green))
        t.append(tr)
    return t

def count(value):
    return f'{value:,.0f}'

M = json.loads((CACHE / 'metrics_report.json').read_text(encoding='utf-8'))
S = json.loads((CACHE / 'facility_survey_current_summary.json').read_text(encoding='utf-8'))
P = json.loads((WORK / 'prose-corrections.json').read_text(encoding='utf-8'))
entries = P.get('entries', P)
if isinstance(entries, list):
    entries = {str(x['index']): x for x in entries}
with ZipFile(SOURCE) as z:
    parts = {name: z.read(name) for name in z.namelist()}
with ZipFile(REFERENCE) as z:
    oldparts = {name: z.read(name) for name in z.namelist()}
doc = E.fromstring(parts['word/document.xml'])
body = doc.find('w:body', NS)
blocks = list(body)
oldbody = E.fromstring(oldparts['word/document.xml']).find('w:body', NS)
rels = E.fromstring(parts['word/_rels/document.xml.rels'])
cts = E.fromstring(parts['[Content_Types].xml'])
audit = {'source_sha256': hashlib.sha256(parts['word/document.xml']).hexdigest(),
         'prose_changes': [], 'tables_restored': [], 'charts': [], 'caption_moves': []}
green_ranges = [(44, 49), (51, 56), (354, 374), (487, 494), (505, 507), (509, 626)]

# Apply text-only changes to the original paragraph slots, retaining paragraph styles.
for i, el in enumerate(blocks):
    isgreen = any(start <= i <= end for start, end in green_ranges)
    if el.tag == q('w:p'):
        entry = entries.get(str(i))
        if entry and (not isinstance(entry, dict) or entry.get('action','replace_text')=='replace_text'):
            value = entry['text'] if isinstance(entry, dict) else entry
            set_paragraph(el, value, isgreen)
            audit['prose_changes'].append({'body_index': i, 'text': value})
    # Resolve word-level markup within tables to the corrected version.
    elif el.tag == q('w:tbl'):
        for p in el.xpath('.//w:p', namespaces=NS):
            if any(run_is_green(r) for r in p.findall('w:r', NS)) and p.xpath('.//w:strike', namespaces=NS):
                set_paragraph(p, clean_space(accepted(p)), isgreen)
    mark(el, isgreen)

# Correct repeated headline metrics without altering other early-section prose.
early = {
    149: txt(blocks[149]) + ' Hospitals hold 3,067 assets (1.3%) and other local-government locations hold four (less than 0.1%).',
    159: txt(blocks[159]).replace('over 7000 assets mainly in seed secondary schools and Health Centres had not been used requiring installation or the facility itself was not yet ready.', '13,520 assets, mainly in seed secondary schools and Health Centres, were classified as faulty and out of use. Some were awaiting installation or the facility itself was not yet ready.'),
    168: 'The verification revealed that 50,329 (22.0%) of the assets had usable identifiers and 178,695 (78.0%) had no usable identifier recorded. Of all assets, 22,253 (9.7%) had identifiers containing UgIFT or UGFT as a form of identification.',
    169: txt(blocks[169]).replace('assets that were not engraved', 'assets without usable identifiers'),
    177: 'Overall, the 229,024 assets across the different institutions had an available recorded value of UGX 996,812,628,890. Based on the straight-line depreciation method, available accumulated depreciation was UGX 165,185,197,307 and available net book value was UGX 595,801,587,531 as at 30th September 2026. Recorded values vary by institution, with MDAs at UGX 32,054,743,836, Blood Banks at UGX 1,503,720,926, Seed Secondary Schools at UGX 700,242,561,371 and Health Centres at UGX 260,692,452,291, as indicated in table 2. Hospital and other local-government assets account for the remaining UGX 2,319,150,466. These available totals cover different populations; Appendix A reconciles cost less depreciation to net book value for assets with complete accounting information.',
}
for i, value in early.items():
    set_paragraph(blocks[i], value)
    audit['prose_changes'].append({'body_index': i, 'text': value, 'reason': 'metric reconciliation'})

# Preserve the original TOC title outside Word's regenerated field range.
toc_title=blocks[11].find('.//w:sdtContent/w:p',NS)
if toc_title is not None and clean_space(txt(toc_title))=='Table of Contents':
    title=deepcopy(toc_title)
    # The source placed its label inside the TOC field; copy only the heading,
    # leaving the field start and instruction in their existing content control.
    set_paragraph(title,'Table of Contents')
    mark(title)
    blocks[11].addprevious(title)
    for t in toc_title.xpath('.//w:t',namespaces=NS):
        t.text=''

# Reconcile the field-condition description with the register's numeric grouping.
scope_note=paragraph('The condition descriptions in section 2.5 distinguish physically faulty assets from usable items in store or awaiting installation. The quantitative tables use the current register codes: 215,504 assets marked Functional and in use, and 13,520 marked Faulty and not in use. All entries marked not in use carry the Faulty code in these totals, including usable stored or uninstalled items; the 13,520 therefore does not represent a count of physically broken assets.',style='Normal',green=True)
blocks[532].addprevious(scope_note)

# Restore the original overall institution-by-institution table with supported status fields.
books = [('MOFPED BK', 'MoFPED'), ('MOWT BK', 'MoWT'), ('MOES BK', 'MoES'), ('MAAIF BK', 'MAAIF'),
         ('MOH BK', 'MoH'), ('OPM BK', 'OPM'), ('MOWE BK', 'MoWE'), ('MGLSD BK', 'MoGLSD'),
         ('NEMA BK', 'NEMA'), ('PPDA BK', 'PPDA'), ('OAG BK', 'OAG'), ('MOLG BK', 'MoLG'), ('MOLHUD BK', 'MoLHUD')]
insts = [('Health centres', 'Health centres'), ('Schools', 'Seed Secondary Schools'),
         ('Regional blood banks', 'Blood Banks'), ('Hospitals on local-government books', 'Hospitals on LG books'),
         ('Other local-government or unassigned locations', 'Other LG locations')]
condition_rows = []
for bucket, name in [(M['books'][book], name) for book, name in books] + [(M['institutions'][key], name) for key, name in insts]:
    condition_rows.append([name, count(bucket['rows']), count(bucket['functional']), count(bucket['faulty']), f"{100*bucket['functional']/bucket['rows']:.1f}%"])
t = M['total']
condition_rows.append(['Total', count(t['rows']), count(t['functional']), count(t['faulty']), f"{100*t['functional']/t['rows']:.1f}%"])
overall = table(['Institution', 'Assets', 'Functional and in use', 'Faulty and not in use', 'Functional share'], condition_rows, [2650, 1300, 1650, 1650, 1678])
blocks[156].getparent().replace(blocks[156], overall)
audit['tables_restored'].append({'source_block': 641, 'destination_block': 156, 'rows': condition_rows})

# Reinstate the deleted service-date metric table in its existing appendix, preserving early content.
date_table = deepcopy(oldbody[141])
mark(date_table, True)
blocks[522].addprevious(paragraph('Service-date entries across all assets', green=True))
blocks[522].addprevious(date_table)
blocks[522].addprevious(paragraph('Categories are mutually exclusive; rounded percentages may not total 100.0%.', green=True))
audit['tables_restored'].append({'source_block': 141, 'destination': 'Appendix B'})

# Restore the omitted full new reviewer-response section, without the superseded archive.
for i in (635, 636, 637):
    clone = deepcopy(oldbody[i])
    mark(clone, True)
    body.insert(len(body)-1, clone)
audit['tables_restored'].append({'source_block': 637, 'destination': 'Appendix L'})

# Add explicit totals to finance/category tables where the existing presentation omits them.
def add_total_row(tel, bucket, finance=False, availability=False, condition=False, identifiers=False):
    trs = tel.findall('w:tr', NS)
    if txt(trs[-1].find('w:tc', NS)).strip().lower().startswith('total'):
        return
    row = deepcopy(trs[-1])
    cells = row.findall('w:tc', NS)
    if finance:
        label = f"Total\n{count(bucket['rows'])} assets; NBV {count(bucket['net_book_value_numeric_rows'])}/{count(bucket['rows'])}"
        ratio = 100 * bucket['complete_recognized_nbv_sum'] / bucket['complete_recognized_cost_sum'] if bucket['complete_recognized_cost_sum'] else None
        values = [label, f"{bucket['cost_sum']/1e6:,.3f}" + ('*' if bucket.get('cost_unavailable_rows') else ''),
                  f"{bucket['accumulated_depreciation_sum']/1e6:,.3f}" + ('*' if bucket.get('accumulated_depreciation_unavailable_rows') else ''),
                  f"{bucket['net_book_value_sum']/1e6:,.3f}" + ('*' if bucket.get('net_book_value_unavailable_rows') else ''), f'{ratio:.1f}%' if ratio is not None else 'n/a']
    elif availability:
        values = ['Total', count(bucket['rows']), '100.0%']
    elif condition:
        values = ['Total', count(bucket['rows']), count(bucket['functional']), count(bucket['faulty'])]
    elif identifiers:
        values = ['Total', count(bucket['rows']), count(bucket['ugift_text_identifier']), count(bucket['other_identifier']), count(bucket['no_tag_recorded'])]
    else:
        return
    for tc, value in zip(cells, values):
        ps = tc.findall('w:p', NS)
        set_paragraph(ps[0], str(value))
        for p in ps[1:]:
            tc.remove(p)
    tel.append(row)
    mark(row, any(x.xpath('.//w:highlight[@w:val="green"]', namespaces=NS) for x in trs[0]))
    # Keep a total with at least its preceding data row when a table splits.
    for p in trs[-1].xpath('.//w:p',namespaces=NS):
        pr=p.find('w:pPr',NS)
        if pr is None:
            pr=node('w:pPr');p.insert(0,pr)
        if pr.find('w:keepNext',NS) is None:
            pr.append(node('w:keepNext'))

finance_tables = {179: M['total'], 352: M['institutions']['Regional blood banks'],
                 359: M['books']['ARUA RBB BK'], 366: M['books']['HOIMA RBB BK'], 373: M['books']['SOROTI RBB BK'],
                 404: M['institutions']['Health centres'], 435: M['institutions']['Schools']}
for index, (book, _) in zip([204, 214, 228, 242, 254, 265, 274, 282, 296, 307, 317, 328, 339], books):
    finance_tables[index] = M['books'][book]
for index, bucket in finance_tables.items():
    add_total_row(blocks[index], bucket, finance=True)
for index, group, kind in [(383, 'Health centres', 'availability'), (391, 'Health centres', 'condition'),
                           (401, 'Health centres', 'identifiers'), (420, 'Schools', 'availability'),
                           (424, 'Schools', 'condition'), (430, 'Schools', 'identifiers')]:
    add_total_row(blocks[index], M['institutions'][group], **{kind: True})

# Use a single conventional half-up display for the two exact half-unit cases.
corrections=json.loads((WORK/'table-corrections.json').read_text(encoding='utf-8'))
for index, correction in corrections.items():
    for change in correction.get('changes',[]):
        tr=blocks[int(index)].findall('w:tr',NS)[change['row']]
        tc=tr.findall('w:tc',NS)[change['column']]
        ps=tc.findall('w:p',NS)
        set_paragraph(ps[0],change['expected'],True)
        for p in ps[1:]:
            tc.remove(p)

# Exact original photographic captions already sit below their retained originals.

def fresh_relationship(target, reltype):
    used = {el.get('Id') for el in rels}
    number = 1
    while f'rId{number}' in used:
        number += 1
    rid = f'rId{number}'
    rels.append(node('pr:Relationship', {'Id': rid, 'Target': target, 'Type': NS['r'] + '/' + reltype}))
    return rid

def register_type(path, content_type):
    if not cts.xpath('./ct:Override[@PartName=$name]', namespaces=NS, name='/' + path):
        cts.append(node('ct:Override', {'PartName': '/' + path, 'ContentType': content_type}))

def chart_cache(formula, values, numeric=False, fmt='0'):
    ref = node('c:numRef' if numeric else 'c:strRef')
    ref.append(node('c:f', text=formula))
    cache = node('c:numCache' if numeric else 'c:strCache')
    if numeric:
        cache.append(node('c:formatCode', text=fmt))
    cache.append(node('c:ptCount', {'val': len(values)}))
    for i, value in enumerate(values):
        pt = node('c:pt', {'idx': i})
        pt.append(node('c:v', text=str(value)))
        cache.append(pt)
    ref.append(cache)
    return ref

def series(index, label, categories, values, percent=False):
    s = node('c:ser')
    s.append(node('c:idx', {'val': index}))
    s.append(node('c:order', {'val': index}))
    col = chr(ord('B') + index)
    tx = node('c:tx')
    tx.append(chart_cache(f'Sheet1!${col}$1', [label]))
    s.append(tx)
    sp = node('c:spPr')
    fill = node('a:solidFill')
    fill.append(node('a:srgbClr', {'val': ['244656', '9FAEB5', 'D9D9D9'][index % 3]}))
    sp.append(fill)
    line = node('a:ln')
    line.append(node('a:noFill'))
    sp.append(line)
    s.append(sp)
    cat = node('c:cat')
    cat.append(chart_cache(f'Sheet1!$A$2:$A${len(categories)+1}', categories))
    s.append(cat)
    val = node('c:val')
    val.append(chart_cache(f'Sheet1!${col}$2:${col}${len(categories)+1}', values, True, '0.0%' if percent else '#,##0'))
    s.append(val)
    return s

def chart_text_properties(size=1000):
    tx = node('c:txPr')
    tx.append(node('a:bodyPr'))
    tx.append(node('a:lstStyle'))
    p = node('a:p')
    pr = node('a:pPr')
    dr = node('a:defRPr', {'sz': size})
    dr.append(node('a:latin', {'typeface': 'Arial'}))
    pr.append(dr)
    p.append(pr)
    p.append(node('a:endParaRPr', {'lang': 'en-US'}))
    tx.append(p)
    return tx

def build_chart(template, categories, values, labels, percent=False, horizontal=False):
    root = E.fromstring(oldparts[f'word/charts/chart{template}.xml'])
    chart = root.find('c:chart', NS)
    for title in root.xpath('.//c:title | .//c:externalData | .//c:userShapes', namespaces=NS):
        title.getparent().remove(title)
    auto = chart.find('c:autoTitleDeleted', NS)
    if auto is not None:
        auto.set('val', '1')
    plot = chart.find('c:plotArea', NS)
    for el in plot.xpath('./c:layout | ./c:dTable', namespaces=NS):
        plot.remove(el)
    graph = next(el for el in plot if E.QName(el).localname.endswith('Chart'))
    for s in graph.findall('c:ser', NS):
        graph.remove(s)
    insertion = next((i for i, el in enumerate(graph) if E.QName(el).localname in {'dLbls', 'gapWidth', 'overlap', 'axId'}), len(graph))
    for j, (label, numbers) in enumerate(zip(labels, values)):
        graph.insert(insertion+j, series(j, label, categories, numbers, percent))
    ispie = graph.tag == q('c:pieChart')
    if ispie:
        colors=['244656','3D7088','7096A6','9EBAC6','BC9A6B','D3D8DC']
        s=graph.find('c:ser',NS)
        before=s.find('c:cat',NS)
        for j in range(len(categories)):
            point=node('c:dPt')
            point.append(node('c:idx',{'val':j}))
            sp=node('c:spPr')
            fill=node('a:solidFill')
            fill.append(node('a:srgbClr',{'val':colors[j%len(colors)]}))
            sp.append(fill)
            point.append(sp)
            s.insert(s.index(before),point)
    direction = graph.find('c:barDir', NS)
    if direction is not None and horizontal:
        direction.set('val', 'bar')
    # Drop source-specific axis maxima and old layout/label overrides.
    for axis in plot.xpath('./c:catAx | ./c:valAx', namespaces=NS):
        for el in axis.xpath('./c:scaling/c:max | ./c:scaling/c:min | ./c:majorUnit | ./c:minorUnit | ./c:txPr', namespaces=NS):
            el.getparent().remove(el)
        axis.append(chart_text_properties(900))
        # Old chart4's filled axis shapes obscure percent labels as black boxes.
        axis_sp=axis.find('c:spPr',NS)
        if axis_sp is not None:
            axis.remove(axis_sp)
        axis_sp=node('c:spPr')
        axis_sp.append(node('a:noFill'))
        axis_line=node('a:ln');axis_line.append(node('a:noFill'));axis_sp.append(axis_line)
        axis.append(axis_sp)
        if percent and axis.tag==q('c:valAx'):
            scaling=axis.find('c:scaling',NS)
            scaling.append(node('c:max',{'val':1}))
            scaling.append(node('c:min',{'val':0}))
            axis.append(node('c:majorUnit',{'val':0.2}))
        elif horizontal and axis.tag==q('c:valAx'):
            largest=max(max(v) for v in values)
            target=max(largest/5,1)
            magnitude=10**math.floor(math.log10(target))
            major=next(scale*magnitude for scale in [1,2,2.5,5,10] if scale*magnitude>=target)
            axis.append(node('c:majorUnit',{'val':major}))
        nf = axis.find('c:numFmt', NS)
        if nf is not None:
            nf.set('formatCode', '0%' if percent else '#,##0')
            nf.set('sourceLinked', '0')
        if horizontal:
            pos = axis.find('c:axPos', NS)
            if pos is not None:
                pos.set('val', 'l' if axis.tag == q('c:catAx') else 'b')
            orient = axis.find('c:scaling/c:orientation', NS)
            if orient is not None and axis.tag == q('c:catAx'):
                orient.set('val', 'maxMin')
    for el in root.xpath('.//c:extLst', namespaces=NS):
        el.getparent().remove(el)
    for old in graph.findall('c:dLbls', NS):
        graph.remove(old)
    if len(values) == 1:
        dl = node('c:dLbls')
        dl.append(node('c:numFmt', {'formatCode': '0.0%' if percent else '#,##0', 'sourceLinked': 0}))
        dl.append(node('c:dLblPos', {'val': 'bestFit' if ispie else 'outEnd'}))
        for flag in ['showLegendKey', 'showCatName', 'showSerName', 'showPercent', 'showBubbleSize']:
            dl.append(node('c:'+flag, {'val': 0}))
        dl.append(node('c:showVal', {'val': 1}))
        dl.append(chart_text_properties(900))
        graph.insert(insertion+len(labels), dl)
    legend = chart.find('c:legend', NS)
    if legend is None and len(values)>1:
        legend=node('c:legend')
        legend.append(node('c:legendPos',{'val':'b'}))
        legend.append(node('c:overlay',{'val':0}))
        chart.append(legend)
    if len(values) == 1 and not ispie:
        if legend is not None:
            chart.remove(legend)
    elif legend is not None:
        for el in legend.xpath('./c:layout | ./c:txPr', namespaces=NS):
            legend.remove(el)
        pos = legend.find('c:legendPos', NS)
        if pos is not None:
            pos.set('val', 'b')
        legend.append(chart_text_properties(900))
    # Remove any visual frame, preserving square corners.
    corners = root.find('c:roundedCorners', NS)
    if corners is not None:
        corners.set('val', '0')
    sp = root.find('c:spPr', NS)
    if sp is not None:
        root.remove(sp)
    root.append(node('c:spPr'))
    root.find('c:spPr', NS).append(node('a:noFill'))
    chart_line=node('a:ln');chart_line.append(node('a:noFill'));root.find('c:spPr',NS).append(chart_line)
    ext = node('c:externalData', {'r:id': 'rIdData'})
    ext.append(node('c:autoUpdate', {'val': 0}))
    root.append(ext)
    return E.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

def install_chart(body_index, template, categories, values, labels, percent=False, horizontal=False):
    number = len(audit['charts']) + 1
    part = f'word/charts/chart-reconciled-{number}.xml'
    parts[part] = build_chart(template, categories, values, labels, percent, horizontal)
    register_type(part, 'application/vnd.openxmlformats-officedocument.drawingml.chart+xml')
    workbook_path = f'word/embeddings/chart-reconciled-{number}.xlsx'
    wb = Workbook()
    sheet = wb.active
    sheet.title = 'Sheet1'
    sheet.append(['Category', *labels])
    for i, category in enumerate(categories):
        sheet.append([category, *[numbers[i] for numbers in values]])
    if percent:
        for row in sheet.iter_rows(min_row=2, min_col=2):
            for c in row:
                c.number_format = '0.0%'
    data = BytesIO()
    wb.save(data)
    parts[workbook_path] = data.getvalue()
    register_type(workbook_path, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    chartrels = node('pr:Relationships')
    chartrels.append(node('pr:Relationship', {'Id': 'rIdData', 'Type': NS['r']+'/package', 'Target': '../embeddings/'+Path(workbook_path).name}))
    parts[f'word/charts/_rels/{Path(part).name}.rels'] = E.tostring(chartrels, xml_declaration=True, encoding='UTF-8', standalone=True)
    rid = fresh_relationship('charts/'+Path(part).name, 'chart')
    p = blocks[body_index]
    graphic_data = p.find('.//a:graphicData', NS)
    assert graphic_data is not None, body_index
    graphic_data.clear()
    graphic_data.set('uri', NS['c'])
    graphic_data.append(node('c:chart', {'r:id': rid}))
    dp = p.find('.//wp:docPr', NS)
    if dp is not None:
        dp.set('name', f'Reconciled chart {number}')
        dp.set('descr', '; '.join(f'{category}: '+', '.join(str(numbers[i]) for numbers in values) for i,category in enumerate(categories)))
    # Retain the physical image dimensions already used in the report.
    mark(p)
    audit['charts'].append({'body_index': body_index, 'part': part, 'template': template, 'categories': categories, 'labels': labels, 'values': values, 'percent': percent})

group_order = ['Ministries and agencies', 'Regional blood banks', 'Health centres', 'Schools', 'Hospitals on local-government books', 'Other local-government or unassigned locations']
group_labels = ['Ministries and agencies', 'Blood Banks', 'Health Centres', 'Seed Secondary Schools', 'Hospitals on LG books', 'Other LG locations']
buckets = [M['institutions'][key] for key in group_order]
install_chart(151, 1, group_labels, [[b['rows'] for b in buckets]], ['Assets'])
reason_keys = ['power', 'training_skills', 'installation', 'incomplete_buildings_space', 'accessories_consumables', 'staffing']
reason_names = ['Power supply', 'Training or skills', 'Installation', 'Incomplete buildings or space', 'Accessories or consumables', 'Staffing']
reason_data = S['utilisation_blockers']['from_answers']['total']['reasons']
install_chart(162, 5, reason_names, [[reason_data[key]['n'] for key in reason_keys]], ['Respondent facilities'], horizontal=True)
install_chart(172, 2, group_labels+['Total'], [[b.get(key,0)/b['rows'] for b in buckets+[M['total']]] for key in ['ugift_text_identifier','other_identifier','no_tag_recorded']], ['UgIFT or UGFT identifier','Other identifier','No usable identifier'], True)
install_chart(187, 3, [name for _,name in books], [[M['books'][key]['rows'] for key,_ in books]], ['Assets'])
install_chart(193, 4, [name for _,name in books], [[M['books'][book].get(key,0)/M['books'][book]['rows'] for book,_ in books] for key in ['ugift_text_identifier','other_identifier','no_tag_recorded']], ['UgIFT or UGFT identifier','Other identifier','No usable identifier'], True)

# All remaining register graphs use the same verified aggregates as their tables.
for index, book in [(209,'MOWT BK'), (218,'MOES BK'), (232,'MAAIF BK'), (248,'MOH BK'), (259,'OPM BK'),
                    (284,'MGLSD BK'), (290,'NEMA BK'), (301,'PPDA BK'), (313,'OAG BK'), (332,'MOLHUD BK')]:
    cats = sorted(M['by_book_category'][book].items(), key=lambda item: -item[1]['rows'])
    install_chart(index, 3, [k for k,_ in cats], [[b['rows'] for _,b in cats]], ['Assets'], horizontal=True)
items = Counter()
with gzip.open(CACHE/'metrics_rows.jsonl.gz', 'rt', encoding='utf-8') as stream:
    for line in stream:
        d=json.loads(line)
        if d['A']!='MOLG BK':
            continue
        desc=str(d.get('AX') or '').casefold()
        label='Photocopiers' if 'copier' in desc else 'Laptops' if 'laptop' in desc else 'Computer components' if 'computer' in desc else 'Vehicle' if 'vechicl' in desc or 'vehicle' in desc else 'Other assets'
        items[label]+=1
install_chart(322,3,list(items),[list(items.values())],['Assets'],horizontal=True)
cats=sorted(M['by_institution_category']['Health centres'].items(),key=lambda item:-item[1]['rows'])
for index, key in [(384,'rows'), (388,'faulty'), (398,'ugift_text_identifier')]:
    label={'rows':'Assets','faulty':'Faulty assets','ugift_text_identifier':'Assets with UgIFT or UGFT tag'}[key]
    install_chart(index,3,[k for k,_ in cats],[[b.get(key,0) for _,b in cats]],[label],horizontal=True)

# Interview-based charts retain their separate respondent units and denominators.
hb=lambda k:S['benefits']['health_centres'][k]['Health centre']['pct']/100
sb=lambda k:S['benefits']['schools'][k]['School']['pct']/100
install_chart(458,3,['Health Centres: any benefit','Schools: any benefit','Health Centres: equipment supports services','Health Centres: maternity services','Schools: learning environment','Schools: access to education','Schools: practical science or ICT'],[[hb('any_benefit'),sb('any_benefit'),hb('equipment_quality'),hb('maternity'),sb('learning_environment'),sb('access'),sb('practical_ict')]],['Share of respondents'],True,True)
challenge_keys=['power','staffing','space_infrastructure','security_fencing','repair_maintenance','staff_housing','water','training_skills','equipment_not_installed','incomplete_works']
challenge_names=['Power supply','Staffing','Space or infrastructure','Security or fencing','Maintenance support','Staff housing','Water supply','Equipment training','Installation or incomplete delivery','Works or handover']
install_chart(472,3,challenge_names,[[S['challenges']['raised'][key]['total']['pct']/100 for key in challenge_keys]],['Share of 477 respondents'],True,True)
mech=S['maintenance_headline']['mechanism_over_answered_q2']
install_chart(481,3,['Repairs from facility funds or staff','Outside technical support','Maintenance not yet needed','No repair arrangement'],[[mech[key][group]['pct']/100 for key in ['facility_level_any','external_technical_support_any','not_yet','no_arrangement']] for group in ['Health centre','School','Total']],['Health Centres (278 respondents)','Schools (191 respondents)','All facilities (469 respondents)'],True,True)
intervals=S['maintenance_headline']['frequency']['fixed_interval_breakdown']
install_chart(484,3,['Annually','Monthly','Quarterly','Every school term','Twice yearly','Weekly or daily'],[[intervals[key]['n'] for key in ['annually','monthly','quarterly','termly','twice_yearly','weekly_or_daily']]],['Facilities with a fixed interval'],horizontal=True)

# Captions supply the visible unit and the metric selected by each graph.
set_paragraph(blocks[161],'Figure 2: Reasons for equipment not in use reported by facilities (156 respondents; multiple responses)')
set_paragraph(blocks[389],'Figure 18: Faulty assets at Health Centres by category')
set_paragraph(blocks[399],'Figure 19: Health Centre assets with UgIFT or UGFT identifiers by category')
# Place the existing comparison prose before the graph it describes.
comparison=blocks[480]
comparison.getparent().remove(comparison)
blocks[481].addprevious(comparison)

# Keep the existing caption wording, with every caption physically below its graph.
for chart in audit['charts']:
    p = blocks[chart['body_index']]
    previous = p.getprevious()
    if previous is not None and previous.tag == q('w:p') and re.match(r'^Figure\s+\d+\s*:',txt(previous).strip()):
        previous.getparent().remove(previous)
        p.addnext(previous)
        audit['caption_moves'].append(chart['body_index'])
    pr = p.find('w:pPr',NS)
    if pr is None:
        pr=node('w:pPr');p.insert(0,pr)
    if pr.find('w:keepNext',NS) is None:
        pr.append(node('w:keepNext'))
    following=p.getnext()
    if following is not None and following.tag==q('w:p'):
        nextpr=following.find('w:pPr',NS)
        if nextpr is not None:
            for keep in nextpr.findall('w:keepNext',NS):
                nextpr.remove(keep)

# Strip residual revision highlighting from ancillary package parts and request field refresh.
for path,data in list(parts.items()):
    if path.startswith('word/') and path.endswith('.xml') and not path.startswith('word/charts/') and path!='word/document.xml':
        try:
            root=E.fromstring(data)
        except E.XMLSyntaxError:
            continue
        changed=False
        for highlight in root.xpath('.//w:highlight',namespaces=NS):
            highlight.getparent().remove(highlight);changed=True
        if path=='word/settings.xml':
            update=root.find('w:updateFields',NS)
            if update is None:
                update=node('w:updateFields');root.append(update)
            update.set(q('w:val'),'true');changed=True
        if changed:
            parts[path]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
parts['word/document.xml']=E.tostring(doc,xml_declaration=True,encoding='UTF-8',standalone=True)
parts['word/_rels/document.xml.rels']=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
parts['[Content_Types].xml']=E.tostring(cts,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(DEST,'w',ZIP_DEFLATED) as z:
    for path,data in parts.items():
        z.writestr(path,data)
(WORK/'reconciliation-applied.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(DEST)
print('Charts:',len(audit['charts']),'restored tables:',len(audit['tables_restored']),'caption moves:',len(audit['caption_moves']))
