# Numbered-reference revision visual QA

Source: `ugift-working-report-06102026-1344-reconciled.docx`

Exact source SHA256, unchanged during read-only Word export:

`FAA13685213D29252B710FF1EF01DBCB8DF4AEF3B102E2A35F8C05302B730ED2`

Physical page count: **93** (cover plus printed pages 1–92). Hidden Word COM PDF export and bundled Poppler rasterization at 144 dpi were used; original report files were not edited by the render agent.

Comparison with `verified-render-latest` found **30 pixel-identical pages and 63 changed pages**. Earlier full-detail QA was reused only for pixel-identical pages. Every changed page was individually inspected at original PNG detail:

- Root: physical pages **2–4 and 8**. TOC is clean and refreshed through printed page 92; objectives visibly use a), b), c), d), with no clipping or wording changes.
- Render agent: physical pages **14–15, 19, 21, 23–28, 30–40, 47, 50–52, 60–61**. No clipping, overlap or orphaned chart/table captions found. Chart axes/legends remain readable and titles stay below graphs. Numbered references fit cleanly.
- Structure agent: physical pages **62–77**. Tables 38–48 captions stay with table starts; table values and continuing headings are readable; whole new sections retain green highlighting. No repair required.
- Metrics agent: physical pages **78–93**. Tables 49–68 captions remain green and paired with tables. Values are readable, without clipping or overlap. One minor issue: Table 52's units/NBV note begins on physical page 81 after its table ends on page 80.

Root plans to keep Table 52's last row with the units/NBV note and replace the remaining “photos below” sentence after section 3.2 with a numbered composite photograph reference. These subsequent edits require a targeted re-render and comparison before final delivery.

Metric correctness is audited separately. This record covers rendering and visual layout only. PDF/PNG outputs are internal QA artifacts; deliver the reconciled DOCX. Exact comparison details are in `page-comparison.json`.
