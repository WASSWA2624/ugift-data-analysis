# -*- coding: utf-8 -*-
"""Write Team 14 reports, check voice against the other teams, render only team-14."""
import os
import sys

sys.path.insert(0, r"d:\coding\apps\ugift\src")

import md_render
import build_reports as BR
import team10_reports
import team11_reports
import team12_reports
import team13_reports
import team14_reports
import paths

ROOT = os.path.join(paths.ROOT, "facility-registers")


def drop_legacy_team14():
    gone = 0
    base = os.path.join(ROOT, "team-14")
    for dp, _, fs in os.walk(base):
        for f in fs:
            stem, ext = os.path.splitext(f)
            if ext == ".md" or (stem in BR.LEGACY and ext in (".md", ".docx", ".pdf")):
                os.remove(os.path.join(dp, f))
                gone += 1
    return gone


def render_team14():
    made, failed = 0, []
    for name, stem, md in md_render.recorded():
        if "team-14" not in stem.replace("\\", "/"):
            continue
        blocks = md_render.parse(md)
        title = next((b for k, b in blocks if k == "h1"), name)
        d = os.path.dirname(stem)
        if d:
            os.makedirs(d, exist_ok=True)
        md_render.to_docx(blocks, stem + ".docx", title)
        if not md_render.to_pdf(md_render.to_html(blocks, title), stem + ".pdf"):
            failed.append(name)
        made += 1
    return made, failed


def main():
    t14, t14_logs = team14_reports.main()
    drop_legacy_team14()
    BR.check_no_clock_times()
    BR.check_no_process_words()
    BR.check_no_underscores()
    BR.check_simple_words()
    BR.check_no_team_conduct()
    BR.check_process_report_scope()
    BR.check_sentences_finished()

    import build_registers as B15
    photos, notes = BR.read_export()
    kinds = B15.KIND_OF
    for fac in sorted(photos):
        BR.facility_report(fac, kinds.get(fac, "health-centres"),
                           photos[fac], notes.get(fac, []))
    for lg in B15.DISTRICTS:
        here = {f: ps for f, ps in photos.items() if B15.DISTRICT_OF[f] == lg}
        BR.daily_log(lg, here)
        BR.lg_report(lg, here, kinds)
        BR.lg_courtesy_call(lg)
    BR.lg_asset_record_review()
    BR.process_report(photos, kinds)
    team10_reports.main()
    team11_reports.main()
    team12_reports.main()
    team13_reports.main()
    BR.check_own_voice()

    made, failed = render_team14()
    if failed:
        raise SystemExit("PDF not produced for: " + ", ".join(failed))
    ones, twos = BR.check_page_limit()
    print("team 14 documents recorded:", t14, "daily logs:", t14_logs)
    print("rendered team-14:", made)
    print("page check (all teams on disk): 1-page", ones, "2-page", twos)


if __name__ == "__main__":
    main()
