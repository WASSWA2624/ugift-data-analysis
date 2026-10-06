# Internal verified render QA

Read-only Word PDF export of `ugift-working-report-06102026-1344-reconciled.docx`, rasterized with bundled Poppler at 144 dpi. Source SHA256 remained unchanged during export:

`574772B54A16828BDFF7C0D27516E5B2E07F5E9DFD0AD8CDB66161733ACF722E`

Physical page count: **92**.

Comparison with `final-render` found 32 pixel-identical pages and 60 changed pages. The render agent reused prior detailed QA for pixel-identical pages and individually inspected changed non-chart pages **3–4, 15, 19, 48–51, 64–92** at original detail. The root agent undertook chart review for **14, 16, 20, 23–24, 26–30, 32–37, 43–45, 54–57**.

Changed non-chart pages had no paragraph, cell, photo, or table clipping or overlap. Tables 29 and 32 now keep their final Total rows with the last data row. Appendix C's new condition-code clarification and the shifted appendix schedules fit inside page margins. Whole-section green highlighting remained readable.

The TOC title was still not visible in this PDF. The root agent reported a subsequent repair that created a plain paragraph outside the field; that newer source is exported separately to `verified-render-latest` for final verification.

Minor readability observation: some continuation pages (67, 70, 71, 77 and 80) start with table data without repeated column headings. Other continuation pages repeat their headings. No data clipping resulted.

`page-comparison.json` records exact normalized PDF text hashes and image pixel comparisons.
