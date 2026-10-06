# Final internal render QA

Source: `D:\coding\ugift-data-analysis\outputs\narrative-report\ugift-working-report-06102026-1344-reconciled.docx`

Source SHA256 unchanged during read-only export:

`0E60324464482F931C0DC12D4358D17D2774D43D78438FC98DA3AC2B1365058E`

Physical page count: **92** (cover plus printed pages 1–91).

## Rendering setup

The canonical Documents renderer was diagnosed against the bundled Windows dependency runtime. No bundled LibreOffice binary is available; the renderer's Windows fallback would search for an installed `soffice.exe`, which the skill prohibits using. Its safely restricted-PATH attempt failed with `FileNotFoundError: LibreOffice soffice.exe was not found on PATH`. See `baseline-render/canonical-render.log` and `baseline-render/RENDER_QA.md`.

The approved fallback used a hidden Microsoft Word COM instance, opened the source read-only, repaginated, exported PDF, closed without saving and confirmed source hashes matched. Bundled Poppler rasterized every PDF page to a 144-dpi PNG for full-detail inspection. No installed LibreOffice or desktop UI automation was used.

Reusable commands:

```powershell
& 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\render_word_fallback.ps1' -InputDocx 'D:\coding\ugift-data-analysis\outputs\narrative-report\ugift-working-report-06102026-1344-reconciled.docx' -OutputDirectory 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\verified-render-latest'
& 'C:\Users\WASSWA WILSON\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\render_pdf_pages.py' 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\verified-render-latest\ugift-working-report-06102026-1344-reconciled.pdf' 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\verified-render-latest' --dpi 144
```

## Verification coverage

- All 92 pages in the original reconciled draft were individually inspected at original PNG detail by the team: 83 by the render agent and nine chart pages by the root agent.
- After chart/axis, caption, Total-row and Appendix C fixes, comparison found 60 changed pages. The render agent inspected all 37 changed non-chart pages (**3–4, 15, 19, 48–51, 64–92**). Root undertook the 23 changed chart pages (**14, 16, 20, 23–24, 26–30, 32–37, 43–45, 54–57**).
- The latest TOC-heading repair changed only physical pages **2–4**. These three pages were inspected individually at original detail. Every other page was pixel-identical to the previous verified render, including all charts; earlier detailed QA remains valid for those pages.

## Results

Latest non-chart layout QA passes. The original “Table of Contents” title is visible again on physical page 2. TOC entries are readable and have no broken bookmark error. Tables 29 and 32 keep their final Total rows with a data row. Appendix C's clarification and all appendix tables fit inside page margins. Photographs and captions remain paired and visible. No text, table cell, photo or caption clipping or overlap was found.

Whole new sections retain readable green highlighting. Sparse layout in the protected front portion was preserved. Some long-table continuation pages start with data rows without repeating column headings, a minor readability observation already reported to root; no values are obscured or clipped.

The root agent confirmed all chart pages are clean. Team visual QA passes for this source hash. This read-only rendering subtask does not audit metric correctness; that is handled separately by the root and metric auditors.

After this QA pass, the user requested numbered references in place of “above”/“below” prose. That subsequent edit must be rendered and compared separately before final delivery; this QA record remains tied to the exact source hash above.

PNG and PDF files are internal QA outputs. Deliver the reconciled DOCX rather than these intermediate images. Exact page text and pixel comparisons are recorded in `page-comparison.json`.
