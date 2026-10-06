# Internal draft render QA

Source: `ugift-working-report-06102026-1344-reconciled.docx`

This render is an intermediate QA artifact, not a deliverable. The document was exported through a hidden Microsoft Word COM instance opened read-only, then rasterized to 144-dpi PNGs with the bundled Poppler runtime. The source SHA256 remained unchanged during rendering:

`04D191C120EC0045D5A5B49B32C31521DF82AECD496F89224AFEB0016FA80D3A`

Physical page count: **92** (cover plus printed pages 1–91).

The render agent inspected physical pages **1–13, 15, 17–19, 21–22, 25–53, 58–92** individually at original PNG detail. The root agent inspected chart pages **14, 16, 20, 23–24, 54–57**. All 92 pages were therefore visually reviewed by the team.

Findings sent to the root agent for correction:

- The original “Table of Contents” heading was missing on physical page 2 after the field update. TOC entries otherwise had no broken bookmark error.
- Numeric axis labels were too dense on physical pages 43 and 45; page 44 was also tight. Major-unit spacing should be increased.
- Table 29 and Table 32 isolated their final Total rows on physical pages 49 and 51. Keep the preceding data row with the Total row where possible.
- Native charts had thin gray chart-area outlines. Root could remove these if unwanted.

Root subsequently reported planned fixes for these findings and other chart details. The updated report must be rendered to a separate `verified-render` folder, compared against this draft, and changed pages reviewed again before final delivery.

Other observations: long appendix tables repeated headers and stayed inside page margins; Appendix L on physical pages 91–92 fit cleanly; photos and their caption pairs fit without overlap; retained whole-section green highlighting was consistently readable. Sparse pages inherited from the protected front portion were left unchanged. No table cell, image, or paragraph clipping was found outside the axis-label issues above.
