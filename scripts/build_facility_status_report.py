"""Build the concise facility reconciliation report from reviewed JSON.

Run after reconcile_facilities.py.
The PDF is a readable view; the companion CSVs retain full source paths and notes.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, LongTable, NextPageTemplate,
    PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / 'tmp/reconciliation/reconciled.json'
DEFAULT_OUTPUT = ROOT / 'raw-data-grouped/facility-data-status.pdf'
NAVY = colors.HexColor('#183B48')
TEAL = colors.HexColor('#16766C')
INK = colors.HexColor('#23343B')
MUTED = colors.HexColor('#607077')
LINE = colors.HexColor('#CBD5D9')
PALE = colors.HexColor('#EEF3F4')
WIDTH, HEIGHT = A4
MARGIN = 37
CONTENT = WIDTH - MARGIN * 2
TOP = HEIGHT - 48
BOTTOM = 42
GAP = 26
COL = (CONTENT - GAP) / 2
AS_OF = '24 September 2026'
SUPERVISOR_CORRECTIONS = {
    24: 'Lawrence Kalyowa',
}


def register_fonts():
    font_dir = Path('C:/Windows/Fonts')
    names = {'Body': 'arial.ttf', 'Body-Bold': 'arialbd.ttf', 'Body-Italic': 'ariali.ttf'}
    if all((font_dir / name).exists() for name in names.values()):
        for family, filename in names.items():
            pdfmetrics.registerFont(TTFont(family, str(font_dir / filename)))
        pdfmetrics.registerFontFamily('Body', normal='Body', bold='Body-Bold', italic='Body-Italic')
        return 'Body', 'Body-Bold', 'Body-Italic'
    return 'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique'


FONT, BOLD, ITALIC = register_fonts()
STYLES = {
    'body': ParagraphStyle('body', fontName=FONT, fontSize=10, leading=14, textColor=INK, spaceAfter=7),
    'small': ParagraphStyle('small', fontName=FONT, fontSize=8.7, leading=11.5, textColor=MUTED, spaceAfter=5),
    'table': ParagraphStyle('table', fontName=FONT, fontSize=9.5, leading=12.4, textColor=INK),
    'table-small': ParagraphStyle('table-small', fontName=FONT, fontSize=8.8, leading=11.3, textColor=INK),
    'table-num': ParagraphStyle('table-num', fontName=FONT, fontSize=9.5, leading=12.4,
                                textColor=INK, alignment=TA_RIGHT),
    'table-small-num': ParagraphStyle('table-small-num', fontName=FONT, fontSize=8.8, leading=11.3,
                                      textColor=INK, alignment=TA_RIGHT),
    'table-small-num-accent': ParagraphStyle('table-small-num-accent', fontName=BOLD, fontSize=8.8,
                                             leading=11.3, textColor=TEAL, alignment=TA_RIGHT),
    'table-head': ParagraphStyle('table-head', fontName=BOLD, fontSize=8.8, leading=11, textColor=colors.white),
    'title': ParagraphStyle('title', fontName=BOLD, fontSize=29, leading=32, textColor=NAVY, spaceAfter=12),
    'section': ParagraphStyle('section', fontName=BOLD, fontSize=20, leading=24, textColor=NAVY, spaceAfter=12, keepWithNext=True),
    'sub': ParagraphStyle('sub', fontName=BOLD, fontSize=12.1, leading=16, textColor=NAVY, spaceBefore=8, spaceAfter=7, keepWithNext=True),
    'team': ParagraphStyle('team', fontName=BOLD, fontSize=11, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=3, keepWithNext=True),
    'lg': ParagraphStyle('lg', fontName=BOLD, fontSize=9.6, leading=12.5, textColor=TEAL, spaceBefore=6, spaceAfter=2.5, keepWithNext=True),
    'roster': ParagraphStyle('roster', fontName=FONT, fontSize=9.6, leading=12.2, textColor=INK, spaceAfter=1.6),
    'metric': ParagraphStyle('metric', fontName=BOLD, fontSize=24, leading=28, textColor=NAVY),
    'label': ParagraphStyle('label', fontName=BOLD, fontSize=9.2, leading=12, textColor=NAVY),
    'metric-note': ParagraphStyle('metric-note', fontName=FONT, fontSize=8.3, leading=10.5, textColor=MUTED),
    'eyebrow': ParagraphStyle('eyebrow', fontName=BOLD, fontSize=9.2, leading=12, textColor=TEAL,
                              spaceAfter=4, uppercase=True),
}


def plain(value):
    value = str('' if value is None else value).replace('\u2013', '-').replace('\u2014', '-').replace('\u2011', '-')
    return re.sub(r'\s+', ' ', value).strip()


def e(value):
    return escape(plain(value))


def p(value, style='body'):
    return Paragraph(value, STYLES[style])


def percentage(value, total):
    return 0 if not total else value / total * 100


def percentage_text(value, total):
    return f'{percentage(value, total):.1f}%'


def number_cell(value, *, small=False, accent=False, bold=False):
    if accent:
        style = 'table-small-num-accent'
    else:
        style = 'table-small-num' if small else 'table-num'
    text = e(value)
    return p(f'<b>{text}</b>' if bold and not accent else text, style)


def metric_card(count, total, label, note):
    content = [
        [p(f'{count} <font size="13">/ {total}</font>', 'metric')],
        [p(f'{percentage_text(count, total)}  {e(label)}', 'label')],
        [p(e(note), 'metric-note')],
    ]
    result = Table(content, colWidths=[CONTENT / 4 - 12])
    result.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, 0), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 1),
        ('TOPPADDING', (0, 1), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 1), (-1, -2), 2),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 7),
    ]))
    return result


def display_name(record):
    """Return the canonical reconciled facility name used in outputs."""
    return plain(record.get('field_name') or record.get('ground_name') or record.get('name', ''))


def source_caption(record):
    refs = [record['id']]
    if record.get('decision_ref'):
        refs.append(record['decision_ref'])
    if record.get('source_locator'):
        refs.append(record['source_locator'])
    return ' | '.join(refs)


def compact_note(record):
    reviewed_wording = {
        'H227': 'The supervisor could not identify Lodonga TC in Yumbe. The district should confirm the master entry.',
        'H149': 'The supervisor confirms the facility exists but received no UgIFT assets. The master assigns it to Kitgum MC.',
        'H086': 'Sulaina says Buyinda was not verified because it is outside UgIFT. Her messages alternate between a school and health centre; confirm they refer to the listed Buyinda Health Centre III.',
    }
    if record.get('id') in reviewed_wording:
        return reviewed_wording[record['id']]
    note = plain(record.get('note', ''))
    match = re.search(r'the filed form names ([^.]+)\.', note)
    if match:
        return f'The filed form names {match[1]}. Confirm and correct the facility-specific return.'
    match = re.search(r'Master/prior report: ([;]+|[^;]+); register: (.+)\.', note)
    if match:
        return f'The register places the facility in {match[2]}; the master lists {match[1]}. Confirm the local government.'
    note = note.replace(' before closing verification.', ' before closing the record.')
    note = note.replace('Unconfirmed possible match:', 'Possible name match, still unconfirmed:')
    return note


def table(rows, widths, header=True, small=False, padding=5):
    rendered = []
    for index, row in enumerate(rows):
        style = 'table-head' if header and index == 0 else ('table-small' if small else 'table')
        rendered.append([cell if isinstance(cell, (Paragraph, list)) else p(e(cell), style) for cell in row])
    result = LongTable(rendered, colWidths=widths, repeatRows=1 if header else 0, hAlign='LEFT')
    commands = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), padding),
        ('RIGHTPADDING', (0, 0), (-1, -1), padding),
        ('TOPPADDING', (0, 0), (-1, -1), padding),
        ('BOTTOMPADDING', (0, 0), (-1, -1), padding),
        ('LINEBELOW', (0, 0), (-1, -1), .35, LINE),
    ]
    if header:
        commands += [('BACKGROUND', (0, 0), (-1, 0), NAVY), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PALE])]
    result.setStyle(TableStyle(commands))
    return result


class Report(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(str(filename), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=48, bottomMargin=BOTTOM, title='UgIFT facility data status',
                         author='UgIFT data reconciliation', subject='Master list and field-return reconciliation, 24 September 2026')
        height = TOP - BOTTOM
        full = Frame(MARGIN, BOTTOM, CONTENT, height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='full')
        left = Frame(MARGIN, BOTTOM, COL, height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='left')
        right = Frame(MARGIN + COL + GAP, BOTTOM, COL, height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='right')
        self.addPageTemplates([PageTemplate(id='full', frames=[full], onPage=self.decorate),
                               PageTemplate(id='columns', frames=[left, right], onPage=self.decorate)])
        self.section_pages = {}

    def decorate(self, canv, doc):
        canv.saveState()
        canv.setFont(BOLD, 8.5)
        canv.setFillColor(NAVY)
        canv.drawString(MARGIN, HEIGHT - 25, 'UgIFT  /  FACILITY DATA STATUS')
        canv.setFont(FONT, 8.2)
        canv.setFillColor(MUTED)
        canv.drawRightString(WIDTH - MARGIN, HEIGHT - 25, AS_OF)
        canv.setStrokeColor(LINE)
        canv.setLineWidth(.5)
        canv.line(MARGIN, HEIGHT - 33, WIDTH - MARGIN, HEIGHT - 33)
        canv.line(MARGIN, 31, WIDTH - MARGIN, 31)
        canv.setFont(FONT, 8)
        canv.drawString(MARGIN, 18, 'Master list, field returns and supervisor decisions')
        canv.drawRightString(WIDTH - MARGIN, 18, str(doc.page))
        canv.restoreState()

    def afterFlowable(self, flowable):
        if getattr(flowable, 'section_key', None):
            key = flowable.section_key
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(), key, level=0)
            self.section_pages[key] = self.page


def section(story, number, title, columns=False, first=False):
    if not first:
        story.extend([NextPageTemplate('columns' if columns else 'full'), PageBreak()])
    heading = p(f'<font color="#16766C">{number:02d}</font>  {e(title)}', 'section')
    heading.section_key = f'section-{number}'
    story.append(heading)


def names_by_team(story, records, mark, heading_flowables=()):
    groups = defaultdict(lambda: defaultdict(list))
    for record in records:
        groups[int(record['team'])][record['lg']].append(record)
    prefix = list(heading_flowables)
    for team in sorted(groups):
        for lg_index, lg in enumerate(sorted(groups[team], key=str.casefold)):
            labels = []
            for record in sorted(groups[team][lg], key=lambda r: (r['type'], display_name(r).casefold())):
                mark.append(record['id'])
                labels.append(f'<font color="#607077">{e(record["id"])}</font> {e(display_name(record))}')
            # One short paragraph per local government avoids a row of blank
            # space after every facility while preserving every name and ID.
            block = prefix
            prefix = []
            if lg_index == 0:
                block.append(p(f'Team {team}', 'team'))
            block.extend([
                p(f'<b><font color="#16766C">Team {team} / {e(lg)}</font></b><br/>' + '; '.join(labels) + '.', 'roster'),
                Spacer(1, 3),
            ])
            story.append(KeepTogether(block))


def build(data, output):
    master = data['records']
    extras = data.get('extras', [])
    counts = Counter(r['status'] for r in master)
    if len(master) != data['master_facilities'] or len({r['id'] for r in master}) != len(master):
        raise ValueError('Master records must contain one unique retained ID per facility.')
    allowed = {'Field evidence', 'No return', 'Needs review', 'Reported absent', 'No UgIFT assets', 'Outside UgIFT', 'Replaced'}
    if set(counts) - allowed:
        raise ValueError(f'Unrecognized master statuses: {set(counts) - allowed}')
    unmatched = [r for r in extras if r.get('scope') == 'Ground return only']
    blood = [r for r in extras if r.get('scope') == 'Allocation only']
    marked = []
    story = []
    completed = [r for r in master if r['status'] == 'Field evidence']
    completed_count = len(completed)
    register_completed = [
        r for r in completed
        if 'completed from consolidated register' in r.get('verification', '').lower()
    ]
    facility_return_count = completed_count - len(register_completed)
    exception_count = sum(counts[s] for s in ['Reported absent', 'No UgIFT assets', 'Outside UgIFT', 'Replaced'])
    coverage_count = len(master) - counts['No return']
    priority_teams = (25, 30, 32)
    priority_no_return = sum(1 for r in master if r['status'] == 'No return' and int(r['team']) in priority_teams)
    marker = p('01 / EXECUTIVE SUMMARY', 'eyebrow')
    marker.section_key = 'section-1'
    story.append(marker)
    story.append(p('Facility completion status', 'title'))
    story.append(p(f'<b>Coverage is {coverage_count} of {len(master)} master facilities '
                   f'({percentage_text(coverage_count, len(master))}).</b> Coverage includes every facility except the '
                   f'{counts["No return"]} with no return. Within this coverage, {completed_count} are complete, '
                   f'{counts["Needs review"]} need a decision and {exception_count} have an explained outcome. '
                   f'The completed total includes {facility_return_count} with '
                   f'facility-specific material and {len(register_completed)} with identifiable information in consolidated '
                   'asset registers. “Complete” means the data is sufficient for this reconciliation; it does not certify that '
                   'every asset was physically inspected.'))
    story.append(p(f'The master contains {data["master_rows"]} source rows and {len(master)} distinct schools and health centres. '
                   'Kapedo in Karenga, Nyamarunda in Kibaale and Kidubuli Health Centre III in Kabarole are each listed twice '
                   'within the same local government, so each facility is counted once. '
                   f'The {len(blood)} regional blood banks are reported separately. School names use the Seed Secondary School '
                   'standard, and every master Health Centre II is shown at its upgraded Health Centre III level.', 'small'))
    cards = Table([[
        metric_card(coverage_count, len(master), 'Coverage', 'Every status except No return'),
        metric_card(counts['No return'], len(master), 'No return', 'Facility evidence outstanding'),
        metric_card(counts['Needs review'], len(master), 'Needs review', 'Reconciled; confirmation remains'),
        metric_card(exception_count, len(master), 'Explained cases', 'Excluded from outstanding returns'),
    ]], colWidths=[CONTENT / 4] * 4)
    cards.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#E9F2EF')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#F0F3F4')),
        ('BACKGROUND', (2, 0), (2, 0), colors.HexColor('#FBF4E8')),
        ('BACKGROUND', (3, 0), (3, 0), colors.HexColor('#EAF0F3')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LINEAFTER', (0, 0), (-2, -1), 4, colors.white),
    ]))
    story.extend([Spacer(1, 5), cards, Spacer(1, 9)])
    story.append(p('Status of the distinct master facilities', 'sub'))
    definitions = [
        ['Status', 'Count', '%', 'What it means'],
        ['Completed', number_cell(completed_count, small=True),
         number_cell(percentage_text(completed_count, len(master)), small=True, accent=True),
         'Identifiable facility information is available in a facility return or consolidated register. Examples: Ntwetwe Seed '
         'Secondary School has a facility toolkit; Awei Seed Secondary School has identifiable rows in the Team 7 register.'],
        ['No return', number_cell(counts['No return'], small=True),
         number_cell(percentage_text(counts['No return'], len(master)), small=True, accent=True),
         'No matched facility return or identifiable asset row is on file, and no documented reason places it in another status. This does not prove absence. '
         'Example: Kiziranfumbi Seed Secondary School, Kikuube.'],
        ['Needs review', number_cell(counts['Needs review'], small=True),
         number_cell(percentage_text(counts['Needs review'], len(master)), small=True, accent=True),
         'A submitted alternate name, commissioning stage, access constraint, or verification account requires confirmation. '
         'These cases count as reconciled coverage, but not as completed field evidence.'],
        ['Explained cases', number_cell(exception_count, small=True),
         number_cell(percentage_text(exception_count, len(master)), small=True, accent=True),
         f'{counts["Reported absent"]} reported absent; {counts["No UgIFT assets"]} no UgIFT assets; '
         f'{counts["Outside UgIFT"]} outside UgIFT; {counts["Replaced"]} replaced.'],
    ]
    status_table = table(definitions, [90, 42, 40, CONTENT - 172], small=True, padding=4.2)
    story.append(status_table)
    story.append(p(f'<b>Replaced / {counts["Replaced"]} facility / '
                   f'{percentage_text(counts["Replaced"], len(master))}.</b> The replacement already has its own '
                   'master entry, so its evidence is counted there once. Example: Loinya Health Centre III was replaced by '
                   'Liko Health Centre III; Liko is already represented by master entry H212.', 'small'))
    story.append(p('The immediate follow-up', 'sub'))
    story.append(p(f'Start with Teams 25, 30 and 32, which account for {priority_no_return} of the '
                   f'{counts["No return"]} outstanding returns. Resolve the {counts["Needs review"]} reconciled cases awaiting confirmation '
                   'and confirm the reported absences with the relevant local governments. '
                   'Onywako has a return but explicitly was not physically verified; Iceme has conflicting accounts of the visit.'))
    story.append(p(f'{len(unmatched)} unmatched ground names or returns are listed separately. Some may be aliases of master entries; '
                   'they are not a confirmed count of additional facilities and are not added to the master evidence totals.', 'small'))
    story.append(p('Reading the lists: H = health-centre master row; S = school master row; X = unmatched ground record; B = blood bank. '
                   '“Team 17,” for example, means the field team responsible for that facility. SS means secondary school; MC means municipal council. '
                   'IDs link to the companion reconciliation and evidence CSVs.', 'small'))
    story.append(p(f'<b>Percentage basis.</b> Summary percentages use the {len(master)} distinct master facilities. '
                   f'Each team coverage percentage uses that team\'s listed facilities and includes every status except No return. '
                   f'The {len(unmatched)} unmatched ground '
                   f'names or returns and {len(blood)} regional blood banks are excluded.', 'small'))
    story.append(p('<b>Report sections.</b> 2 Team responsibility / 3 Returns needing a decision / '
                   '4 Outstanding returns and explained cases / 5 Completed facilities / 6 Unmatched ground names / '
                   '7 Blood banks and counting.', 'small'))

    section(story, 2, 'Team responsibility')
    story.append(p('Counts below cover the master list only. <b>Completed</b> includes identifiable information from either a '
                   'facility-specific return or a consolidated register. <b>Coverage</b> includes every listed facility except '
                   'those in No return; it is not a physical-verification rate. '
                   'The named supervisor owns the follow-up; the full allocation remains in team-distributions.docx.'))
    owner_rows = [['Team', 'Supervisor', 'Listed', 'Completed', 'Coverage', 'No return', 'Review', 'Other*']]
    for team in sorted(int(t) for t in data['teams']):
        records = [r for r in master if int(r['team']) == team]
        tc = Counter(r['status'] for r in records)
        owner = SUPERVISOR_CORRECTIONS.get(team) or next(
            (r.get('supervisor') for r in records if r.get('supervisor')),
            data['teams'][str(team)].get('supervisor', ''),
        )
        owner = re.sub(r'\b\d[\d, /()-]{6,}', '', owner).strip()
        team_completed = tc['Field evidence']
        owner_rows.append([
            number_cell(team, small=True), owner, number_cell(len(records), small=True),
            number_cell(team_completed, small=True),
            number_cell(percentage_text(len(records) - tc['No return'], len(records)), small=True, accent=True),
            number_cell(tc['No return'], small=True), number_cell(tc['Needs review'], small=True),
            number_cell(sum(tc[s] for s in ['Reported absent', 'No UgIFT assets', 'Outside UgIFT', 'Replaced']), small=True),
        ])
    owner_rows.append([
        p('<b>Total</b>', 'table-small'), '', number_cell(len(master), small=True, bold=True),
        number_cell(completed_count, small=True, bold=True), number_cell(percentage_text(coverage_count, len(master)), small=True, accent=True),
        number_cell(counts['No return'], small=True, bold=True), number_cell(counts['Needs review'], small=True, bold=True),
        number_cell(exception_count, small=True, bold=True),
    ])
    owner_table = table(owner_rows, [31, 180, 42, 59, 59, 50, 47, 53], small=True, padding=2.9)
    owner_table.setStyle(TableStyle([
        ('LINEABOVE', (0, -1), (-1, -1), .8, NAVY),
    ]))
    story.append(owner_table)
    story.append(p('*Other = reported absent, no UgIFT assets, outside UgIFT or replaced. A zero means no entry in that status, not confirmation that verification is complete.', 'small'))

    section(story, 3, 'Returns that need a decision')
    review = [r for r in master if r['status'] == 'Needs review']
    story.append(p(f'{len(review)} master entries have conflicting identity, location or verification accounts. '
                   'The supervisor should resolve the point shown, then correct or confirm the return. '
                   '“Team 17,” for example, is the field team responsible for the facility. Full documents and worksheet '
                   'locations are linked by ID in facility-evidence-index.csv.'))
    review_rows = [['Master entry / team and LG', 'Point to resolve']]
    for record in sorted(review, key=lambda r: (int(r['team']), r['lg'], r['name'])):
        marked.append(record['id'])
        label = p(f'<b>{e(display_name(record))}</b><br/>Team {record["team"]} / {e(record["lg"])}<br/><font color="#607077">{e(source_caption(record))}</font>', 'table')
        review_rows.append([label, compact_note(record)])
    story.append(table(review_rows, [185, CONTENT - 185], padding=5))
    ony = next((r for r in unmatched if 'onywako' in r['name'].lower()), None)
    if ony:
        story.append(p('Onywako: return received, physical verification not done', 'sub'))
        story.append(p(f'<b>{e(ony["id"])} / Team {ony["team"]} / {e(ony["lg"])}</b>. '
                       'The form says the assets were reported by the in-charge and could not be physically verified. '
                       'Keep this separate from completed visits. No explicit instruction pairs Onywako with the missing Alik master entry.'))

    section(story, 4, 'Outstanding returns and explained cases')
    no_return = [r for r in master if r['status'] == 'No return']
    disposition = [r for r in master if r['status'] in {'Reported absent', 'No UgIFT assets', 'Outside UgIFT', 'Replaced'}]
    story.append(p(f'<b>{len(disposition)} facilities are excluded from the {len(no_return)} outstanding-return total</b> because a '
                   'specific reason has been documented. They remain in the master reconciliation and are not automatically treated '
                   'as physically verified. The reason for each exclusion is shown below.'))
    disposition_rows = [['Master entry / responsible team', 'Recorded reason']]
    status_labels = {'Replaced': 'Replacement counted elsewhere'}
    for record in sorted(disposition, key=lambda r: (int(r['team']), r['lg'], r['name'])):
        marked.append(record['id'])
        note = compact_note(record)
        if record['id'] in {'H197', 'H195', 'H200'}:
            note = 'Reported nonexistent in the Oyam supervisor message. No one-to-one replacement was specified.'
        elif record['id'] == 'H190':
            note = 'Alik was reported nonexistent. The message names Barlonyo and Onywako but does not say either replaces Alik.'
        status_label = status_labels.get(record['status'], record['status'])
        label = p(f'<b>{e(display_name(record))}</b><br/>Team {record["team"]} / {e(record["lg"])}<br/>'
                  f'<font color="#607077">{e(source_caption(record))}</font>', 'table')
        disposition_rows.append([label, p(f'<b>{e(status_label)}</b><br/>{e(note)}', 'table')])
    story.append(table(disposition_rows, [186, CONTENT - 186], padding=5))
    story.extend([NextPageTemplate('columns'), PageBreak()])
    story.append(p(f'{len(no_return)} returns still outstanding', 'section'))
    story.append(p(f'<b>{len(no_return)} master facilities</b> still have no matched return or usable asset rows. '
                   'Names below are from the master. Naming changes expressly confirmed by a supervisor and linked to field material '
                   'are counted as Completed. Possible aliases without that confirmation remain open in the reconciliation CSV.'))
    names_by_team(story, no_return, marked)

    section(story, 5, 'Completed facilities', columns=True)
    story.append(p(f'<b>{completed_count} completed facility records</b> follow: {facility_return_count} have facility-specific '
                   f'material and {len(register_completed)} have identifiable information in consolidated registers. They share one '
                   'Completed status. The companion CSVs retain the source file, worksheet and row for audit. Completion does not '
                   'certify that every asset was physically inspected.'))
    story.append(p('Supervisor-confirmed naming changes are counted against the relevant master entry when field material is on file. '
                   'This includes Butagaya / Buwala and Mwema / Mutumba. The reconciliation CSV retains the submitted name, '
                   'source file and decision reference.', 'small'))
    names_by_team(story, completed, marked, [p(f'Completed / {completed_count}', 'sub')])

    section(story, 6, 'Unmatched ground names and returns')
    story.append(p(f'<b>{len(unmatched)} submitted facility names could not be linked confidently to a master-list entry.</b> '
                   'They are shown separately and are not included in the 629 master-facility totals. '
                   'Confirm the correct master name, or approve the facility as an addition.'))
    story.append(p('<b>Return received</b> means evidence is on file but the master match is unknown. '
                   '<b>Check identity</b> means the name or local government conflicts with another record. '
                   '<b>Not physically verified</b> means the site visit was not completed.', 'small'))
    ground_rows = [['Submitted name / team and LG', 'What is known / next action']]
    ground_status_labels = {
        'Field evidence': 'Return received',
        'Needs review': 'Check identity',
        'Not verified': 'Not physically verified',
    }
    for record in sorted(unmatched, key=lambda r: (int(r['team']), r['lg'], r['name'])):
        label = p(f'<b>{e(display_name(record))}</b><br/>Team {record["team"]} / {e(record["lg"])}<br/><font color="#607077">{e(source_caption(record))}</font>', 'table')
        note = compact_note(record)
        if note == 'Facility-specific return received; no confirmed master match.':
            note = 'Match this return to a master-list facility, or approve it as an additional facility.'
        status_label = ground_status_labels.get(record['status'], record['status'])
        ground_rows.append([label, p(f'<b>{e(status_label)}</b><br/>{e(note)}', 'table')])
    story.append(table(ground_rows, [215, CONTENT - 215], padding=5))

    section(story, 7, 'Blood banks and counting')
    story.append(p('Regional blood banks', 'sub'))
    story.append(p('These three facilities are allocated in team-distributions.docx and sit outside the school/health-centre master denominator.'))
    bank_rows = [['Allocation', 'Evidence status']]
    for record in sorted(blood, key=lambda r: int(r['team'])):
        if 'arua' in record['name'].lower():
            bank_note = 'A facility-specific asset workbook is on file: ARUA BLOOD BANK-1.xlsx.'
        elif 'soroti' in record['name'].lower():
            bank_note = 'A combined Soroti blood-bank and Kamuda school verification toolkit is on file.'
        elif record.get('folder'):
            bank_note = 'Team 25 supplied the Hoima Regional Blood Bank inventory workbook and photographs on 23 September 2026.'
        else:
            bank_note = 'The team return is outstanding. A programme inventory is on file, but it does not establish team verification.'
        bank_rows.append([p(f'<b>{e(record["name"])}</b><br/>Team {record["team"]} / {e(record["lg"])} / {e(record["id"])}', 'table'),
                          p(f'<b>{e(record["status"])}</b><br/>{e(bank_note)}', 'table')])
    story.append(table(bank_rows, [210, CONTENT - 210], padding=6))
    story.append(p('How the totals were counted', 'sub'))
    story.append(p(f'A repeated facility means the same facility appears more than once within one local government. '
                   f'The master has {data["master_rows"]} rows and {len(master)} distinct facilities after three such facilities are counted once. '
                   'Every retained master ID appears once in the status lists in sections 3-5. '
                   'Construction labels such as Complete and Ongoing describe the project, not asset verification.'))
    duplicate_notes = {
        'S147': ('Kapedo', 'Same school listed for Phase II and Phase III; both source rows are preserved.'),
        'H300': ('Nyamarunda', 'The same health-centre name appears twice.'),
        'H331': ('Kidubuli Health Centre III', 'The same health centre appears twice in the master and is counted once at its upgraded level.'),
    }
    duplicate_rows = [['Facility', 'Local government', 'Source IDs', 'Why counted once']]
    for duplicate in data.get('duplicates', []):
        duplicate_display_name, note = duplicate_notes.get(duplicate['duplicate'], (duplicate['name'], 'Same facility listed twice in the same local government.'))
        duplicate_rows.append([duplicate_display_name, duplicate['lg'], f'{duplicate["retained"]} + {duplicate["duplicate"]}', note])
    story.append(table(duplicate_rows, [100, 85, 88, CONTENT - 273], padding=5))
    roster_counts = Counter(marked)
    expected = {r['id'] for r in master}
    if set(marked) != expected or any(count != 1 for count in roster_counts.values()):
        raise ValueError(f'Master roster coverage failed: missing={expected-set(marked)}, repeated={[k for k,v in roster_counts.items() if v != 1]}')
    output.parent.mkdir(parents=True, exist_ok=True)
    document = Report(output)
    document.build(story)
    audit = {
        'master_records': len(master),
        'master_ids_in_status_rosters': len(marked),
        'master_ids_unique': len(set(marked)),
        'status_counts': dict(counts),
        'percentage_summary': {
            'coverage': percentage_text(coverage_count, len(master)),
            'completed': percentage_text(completed_count, len(master)),
            'no_return': percentage_text(counts['No return'], len(master)),
            'needs_review': percentage_text(counts['Needs review'], len(master)),
            'explained_cases': percentage_text(exception_count, len(master)),
        },
        'completed_source_breakdown': {
            'facility_specific_material': facility_return_count,
            'consolidated_register': len(register_completed),
        },
        'unmatched_ground_records': len(unmatched),
        'blood_banks': len(blood),
        'pages': document.page,
        'section_pages': document.section_pages,
        'output': str(output),
    }
    qa = ROOT / 'tmp/pdfs/status-review'
    qa.mkdir(parents=True, exist_ok=True)
    (qa / 'report-build-audit.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=DEFAULT_INPUT)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build(json.loads(args.input.read_text(encoding='utf-8')), args.output)
