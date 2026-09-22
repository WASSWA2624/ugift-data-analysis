# -*- coding: utf-8 -*-
"""Patch the consolidated field report so every section reports asset engraving.

Does not rebuild photographs. Facility narratives are rewritten from the
on-disk facility reports. Then Word COM refreshes TOC/page numbers and PDF.
"""
from __future__ import annotations

import os
import sys
from copy import deepcopy

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.text.paragraph import Paragraph

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import build_consolidated_final_report as B
import paths

DOCX = os.path.join(paths.ROOT, "final-UGiFT-report-karamojja-6-teams",
                    "UGiFT-consolidated-field-report.docx")


def set_para_text(para, text, *, size=11, bold=False, color=None,
                  align=None, space_after=None):
    if para.runs:
        para.runs[0].text = text
        for run in para.runs[1:]:
            run.text = ""
        run = para.runs[0]
    else:
        run = para.add_run(text)
    B.set_run_font(run, size=size, bold=bold, color=color)
    if align is not None:
        para.alignment = align
    if space_after is not None:
        para.paragraph_format.space_after = Pt(space_after)
    return para


def clone_after(para, text, *, space_after=None):
    new_el = deepcopy(para._element)
    texts = new_el.findall(".//" + qn("w:t"))
    if texts:
        texts[0].text = text
        for t in texts[1:]:
            t.text = ""
    para._element.addnext(new_el)
    new_para = Paragraph(new_el, para._parent)
    if space_after is not None:
        new_para.paragraph_format.space_after = Pt(space_after)
    return new_para


def starts(para, prefix):
    return para.text.strip().startswith(prefix)


def facility_index():
    idx = {}
    for team, _region, lgs in B.SPINE:
        for lg, folders in lgs:
            for folder in folders:
                kind = ("health-centre" if B.is_health_folder(folder)
                        else "school")
                kind_label = "School" if kind == "school" else "Health centre"
                label = "%s (%s)" % (B.display_name(folder), kind_label)
                idx[label] = (team, lg, folder, kind)
    return idx


def main():
    doc = Document(DOCX)
    paras = list(doc.paragraphs)
    idx = facility_index()

    intro = (
        "This report presents the findings of the UgIFT asset verification "
        "exercise carried out by six field teams (Teams 10 to 15) in eastern "
        "and north-eastern Uganda. UgIFT has financed seed secondary schools "
        "and upgraded or newly constructed health centres. The purpose of the "
        "exercise was to establish, for each facility, what was built or "
        "supplied, whether those assets are present, whether they work, "
        "whether they are in use, and whether they are engraved so they can "
        "be identified again.")
    method_visit = (
        "At each facility the team signed the visitors' book where one was "
        "available, spoke with the head teacher, in-charge or other staff on "
        "duty, walked the grounds and rooms that could be opened, recorded "
        "what was seen, and took photographs of buildings and equipment. "
        "Teams recorded whether assets carried an engraved number, a serial "
        "number, or no mark, and photographed the mark where it could be "
        "read. Where a hand-filled verification booklet was completed on "
        "site, that booklet is the detailed asset schedule for the facility.")
    method_returns = (
        "After the visits, each team prepared facility notes, local "
        "government briefs and a short process report. This consolidated "
        "document draws on those returns: a brief narrative for every "
        "facility that has a folder on file, including what the visit "
        "established about engraving, with photographs chosen by "
        "looking at the images themselves: two that identify the facility "
        "(name board or buildings) and two from the verification visit, "
        "shown side by side.")
    summary_engraving = (
        "Asset engraving is reported for every facility in this document. "
        "Across the four regions it is incomplete and inconsistent: some "
        "items carry a UgIFT or ministry mark, some carry only the facility "
        "name, and many carry no engraved or serial number. That finding is "
        "set out facility by facility below, then drawn together after the "
        "chapters.")
    summary_themes = (
        "The other themes that recur are incomplete district lists of "
        "programme assets; equipment still boxed where buildings are "
        "unfinished; and occasional mismatches between the name on the "
        "programme list and the name on the ground. Those themes, with "
        "engraving, are set out after the facility chapters, together with "
        "recommendations aimed at districts, municipal councils and the "
        "responsible ministries.")
    summary_chapters = (
        "The chapters that follow are organised by team and local "
        "government. Inside each local government, schools are presented "
        "first, then health centres. Each facility has about four sentences "
        "of narrative, including engraving, and four photographs where the "
        "return allows: two that identify the facility, and two from the "
        "verification visit, shown side by side.")
    field_intro = (
        "Each local government below is a separate chapter. Municipal "
        "councils are not combined with their neighbouring districts. For "
        "every facility the note records whether assets were found engraved, "
        "and with what mark, where the visit established it.")
    findings_intro = (
        "The points below recur across regions. They concern the assets and "
        "the people who hold them - not the logistics of the field teams. "
        "Engraving is reported first because identifying each asset again "
        "is a purpose of this exercise.")
    recs_intro = (
        "These recommendations are addressed to local governments, the "
        "Ministry of Health, the Ministry of Education and Sports, and the "
        "UgIFT programme. The first of them is to settle and complete "
        "engraving, so that every UgIFT asset can be identified again.")
    signoff = (
        "This consolidated field report is submitted under the supervision "
        "of the officer named below. It records, for each facility reached, "
        "what the visit established about the presence, use and engraving "
        "of UgIFT assets.")
    appendix = (
        "Six teams carried out the visits summarised in this report. All "
        "worked under %s. Each team's notes include what the visit "
        "established about asset engraving at the facilities it reached."
        % B.SUPERVISOR)
    cover_line = (
        "The visits record whether assets are engraved so they can be "
        "identified again")

    counts = {
        "cover": 0, "intro": 0, "method": 0, "summary": 0, "field": 0,
        "findings_intro": 0, "findings": 0, "recs_intro": 0, "recs": 0,
        "signoff": 0, "appendix": 0, "facilities": 0, "missing_h4": 0,
    }

    section = None
    finding_i = 0
    rec_i = 0
    rec_last = None
    inserted_cover = False
    inserted_summary = False
    inserted_rec = False

    # Walk a live list; insertions change the XML tree but not this snapshot,
    # which is what we want for sequential replacement. Extra bullets are
    # cloned from the last rec bullet after the loop.
    for para in paras:
        style = para.style.name if para.style else ""
        text = para.text.strip()

        if style == "Heading 1":
            section = text
            continue

        if not inserted_cover and text.startswith("24 local governments"):
            para.paragraph_format.space_after = Pt(8)
            clone_after(para, cover_line, space_after=28)
            # Keep the clone centred like the counts line.
            nxt = para._element.getnext()
            if nxt is not None:
                Paragraph(nxt, para._parent).alignment = WD_ALIGN_PARAGRAPH.CENTER
            inserted_cover = True
            counts["cover"] += 1
            continue

        if section == "1. Introduction" and starts(
                para, "This report presents the findings of the UgIFT"):
            set_para_text(para, intro)
            counts["intro"] += 1
            continue

        if section == "2. Methodology" and starts(
                para, "At each facility the team signed"):
            set_para_text(para, method_visit)
            counts["method"] += 1
            continue
        if section == "2. Methodology" and starts(
                para, "After the visits, each team prepared"):
            set_para_text(para, method_returns)
            counts["method"] += 1
            continue

        if section == "3. Summary" and starts(
                para, "Across the four regions the same themes"):
            set_para_text(para, summary_themes)
            if not inserted_summary:
                clone_after(para, summary_engraving)
                # clone_after inserts AFTER this para; we wanted engraving
                # BEFORE the themes paragraph. Move the clone in front.
                cloned = para._element.getnext()
                para._element.addprevious(cloned)
                inserted_summary = True
            counts["summary"] += 1
            continue
        if section == "3. Summary" and starts(
                para, "The chapters that follow are organised"):
            set_para_text(para, summary_chapters)
            counts["summary"] += 1
            continue

        if section == "4. Field reports by local government" and starts(
                para, "Each local government below is a separate chapter"):
            set_para_text(para, field_intro)
            counts["field"] += 1
            continue

        if style == "Heading 4":
            info = idx.get(text)
            if not info:
                counts["missing_h4"] += 1
                print("UNMAPPED heading:", text)
                continue
            team, lg, folder, kind = info
            report_path, found_kind = B.find_facility_report(team, lg, folder)
            if found_kind:
                kind = found_kind
            field_note = B.find_field_note(team, lg, folder)
            narrative = B.build_narrative(
                team, lg, folder, kind, report_path, field_note)
            nxt = para._element.getnext()
            if nxt is None:
                counts["missing_h4"] += 1
                continue
            nxt_para = Paragraph(nxt, para._parent)
            set_para_text(nxt_para, narrative, space_after=8)
            counts["facilities"] += 1
            continue

        if section == "5. Cross-cutting findings":
            if style == "Normal" and starts(para, "The points below recur"):
                set_para_text(para, findings_intro)
                counts["findings_intro"] += 1
            elif style == "List Bullet" and finding_i < len(B.FINDINGS):
                set_para_text(para, B.FINDINGS[finding_i], space_after=6)
                finding_i += 1
                counts["findings"] += 1
            continue

        if section == "6. Recommendations":
            if style == "Normal" and starts(
                    para, "These recommendations are addressed"):
                set_para_text(para, recs_intro)
                counts["recs_intro"] += 1
            elif style == "List Bullet" and rec_i < len(B.RECOMMENDATIONS):
                set_para_text(para, B.RECOMMENDATIONS[rec_i], space_after=6)
                rec_last = para
                rec_i += 1
                counts["recs"] += 1
            continue

        if section == "7. Sign-off" and starts(
                para, "This consolidated field report is submitted"):
            set_para_text(para, signoff)
            counts["signoff"] += 1
            continue

        if section == "Appendix. Field teams" and starts(
                para, "Six teams carried out the visits"):
            set_para_text(para, appendix)
            counts["appendix"] += 1
            continue

    if rec_last is not None and rec_i < len(B.RECOMMENDATIONS):
        clone_after(rec_last, B.RECOMMENDATIONS[rec_i], space_after=6)
        inserted_rec = True
        counts["recs"] += 1

    doc.save(DOCX)
    print("Saved", DOCX)
    print("Counts:", counts)
    print("Inserted extra recommendation:", inserted_rec)
    if counts["facilities"] != 96:
        raise SystemExit("Expected 96 facility narratives, got %d"
                         % counts["facilities"])
    if counts["intro"] != 1 or counts["method"] != 2 or counts["summary"] < 2:
        raise SystemExit("Static section patch incomplete: %s" % counts)
    if counts["findings"] != 6 or counts["recs"] != 7:
        raise SystemExit("Bullet counts off: findings=%d recs=%d"
                         % (counts["findings"], counts["recs"]))
    if not inserted_cover:
        raise SystemExit("Cover engraving line was not inserted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
