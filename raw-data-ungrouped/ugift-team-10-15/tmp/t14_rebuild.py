# -*- coding: utf-8 -*-
"""Team 14 only: rebuild register from zip, write reports, render, checks."""
import ast
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(r"d:/coding/apps/ugift")
sys.path.insert(0, str(ROOT / "src"))

SRC = ROOT / "src" / "team14_media" / "__init__.py"
mod = ast.parse(SRC.read_text(encoding="utf-8"))
for node in mod.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "PHOTOS" and isinstance(node.value, ast.Dict):
                seen = []
                dups = []
                for k in node.value.keys:
                    key = ast.literal_eval(k)
                    if key in seen:
                        dups.append(key)
                    seen.append(key)
                print("PHOTOS keys", len(node.value.keys), "unique", len(set(seen)), "dups", dups)
                if dups:
                    raise SystemExit("duplicate PHOTOS keys remain: %s" % (dups,))

base = ROOT / "facility-registers" / "team-14"
for leftover in ("_wa_unpack", "_wa_extract", "_unpack"):
    p = base / leftover
    if p.exists():
        shutil.rmtree(p)
        print("removed", p)

import build_team_registers as BT
filed, unfiled = BT.build("team-14")
print("team-14 filed:", filed)
print("team-14 unfiled:", unfiled or "-")

import md_render
import team14_reports
n, logs, lines = team14_reports.main()
print("team 14 documents recorded:", n, "daily logs:", logs, "toolkit lines:", lines)

import build_reports as BR
BR.check_no_clock_times()
BR.check_no_process_words()
BR.check_no_underscores()
BR.check_simple_words()
BR.check_no_team_conduct()
BR.check_process_report_scope()
BR.check_sentences_finished()
print("team-14 report checks passed")

made, failed = md_render.render_recorded(BR.is_report)
if failed:
    raise SystemExit("PDF failed: %s" % failed)
print("rendered", made, "team-14 reports")

import fitz
over = []
ones = twos = 0
for dp, _, fs in os.walk(base):
    for f in fs:
        if f.endswith(".pdf") and BR.is_report(f):
            pages = len(fitz.open(os.path.join(dp, f)))
            if pages > 2:
                over.append("%s %d" % (f, pages))
            elif pages == 2:
                twos += 1
            else:
                ones += 1
if over:
    raise SystemExit("over two pages: %s" % over)
print("page limit ok: %d one-page, %d two-page" % (ones, twos))
