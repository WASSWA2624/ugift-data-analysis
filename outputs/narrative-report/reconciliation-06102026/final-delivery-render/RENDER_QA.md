# Final delivery visual QA

Source: `ugift-working-report-06102026-1344-reconciled.docx`

Final source SHA256, unchanged during read-only Word PDF export:

`167911FCDFDDB87F069628C94584E3FFC0A7A39D976DD84384CF6AA3675901B7`

Physical page count: **94** (cover plus printed pages 1–93). Hidden Word COM exported the PDF without saving the source; bundled Poppler rendered all pages at 144 dpi. Original report files were not edited by the render agent. The canonical LibreOffice renderer was diagnosed earlier but no bundled Windows LibreOffice exists; the approved read-only Word fallback was used throughout.

Comparison against `final-literal-render` found **91 pixel-identical pages** and three changed physical pages: **21–23**. The render agent inspected all three individually at original PNG detail. Restored source spelling/article/capitalization fits cleanly. Photographic labels, the financial Table 2 continuation with repeated headers, totals/notes, Figure 4 labels, and its below-graph caption remain readable, without clipping or overlap.

All **65 detected section/appendix heading lines remain on identical physical pages**. TOC pages **2–4 are pixel-identical** to the navigation-updated version. No further field/navigation save is needed for these final source wording restorations.

Earlier full-detail visual QA is reused only for pixel-identical pages, through the recorded comparison chain:

- `final-literal-render`: pages 23–24 inspected by the render agent and root; all others pixel-identical to the preceding version.
- `final-verified-render`: all 26 changed pages inspected. Figure 16A is below its eight-photo layout; Table 52's last rows and units/NBV note stay together on page 81. Later table captions and continuations fit through page 94.
- `final-reference-render`: every changed page inspected by the render, structure, metrics and root agents. Objectives use a), b), c), d); numbered references and table captions fit. The two minor photo/note layout issues found then were repaired and verified in the next render.
- `verified-render-latest` and preceding QA: all charts and all report pages inspected at original detail by the team, with corrected chart axes, legends, labels and below-graph captions.

**The final source passes visual QA; no further rendering repair is required.** Metric correctness and protected wording preservation are audited separately by the other agents. PDF/PNG files are internal QA artifacts; the reconciled DOCX is the deliverable. Detailed evidence is in `page-comparison.json` and `heading-page-comparison.json`.
