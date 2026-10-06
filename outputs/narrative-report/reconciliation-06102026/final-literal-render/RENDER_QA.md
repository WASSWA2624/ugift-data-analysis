# Literal wording restoration visual QA

Source: `ugift-working-report-06102026-1344-reconciled.docx`

Source SHA256, unchanged during read-only Word export:

`125293B7C47A45A1E8E506070F775292E31B093474A88881F745A6569954FDD1`

Physical page count: **94**. Hidden Word COM exported the PDF; bundled Poppler rendered every page at 144 dpi. No report source was edited by the render agent.

Compared with `final-verified-render`, **92 pages are pixel-identical**. Only physical pages **23–24** changed, in both text and pixels. The render agent inspected both at original PNG detail: restored PPDA equipment names and the exact phrase “The figure 5 below shows” fit cleanly; chart labels, legends and below-chart captions are readable, with no clipping or overlap. The existing final-verified QA passes are reused for the 92 identical pages.

This source version passes visual QA. Root subsequently restores three additional source spelling/article/capitalization spans identified by the completed preservation audit. That final source needs a read-only render comparison before delivery. Metric correctness is audited separately.
