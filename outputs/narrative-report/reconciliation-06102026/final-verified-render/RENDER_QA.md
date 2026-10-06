# Final repair visual QA

Source: `ugift-working-report-06102026-1344-reconciled.docx`

Source SHA256, unchanged during the read-only Word export:

`129F4C0858AEC3246A175713E25E40577C8052C7E5158A61C939E03F9066476D`

Physical page count: **94** (cover plus printed pages 1–93). Hidden Word COM exported the PDF; bundled Poppler rasterized all pages at 144 dpi. No report source was edited by the render agent.

Compared with `final-reference-render`, **69 pages are pixel-identical and 26 pages changed**. Earlier detailed QA was reused for identical pages only. Every changed page was inspected individually at original PNG detail:

- Render agent: **4, 14–15, 19, 21, 23–25, 40, 42–43**. No clipping, overlap or orphaned captions. Restored protected wording fits. Figure 16A appears below the eight-photo layout on page 42, and the numbered introductory reference fits on page 40. Figure 17 and the Table 24 continuation remain readable on page 43.
- Metrics agent: **80–94**. All clean. Table 52's Printers/Total rows and units/NBV note stay together on page 81 with a repeated header. Later captions, continuations and notes remain paired and readable. Table 68 continues clearly onto page 94 with a repeated header.

This version passes visual QA. Root subsequently restores two remaining protected nonmetric wording spans; the final literal source requires its own render comparison before delivery. Metrics correctness is audited separately. PDF/PNG files are internal QA artifacts.
