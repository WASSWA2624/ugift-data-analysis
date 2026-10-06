# Baseline render record

Source: `ugift-working-report-06102026-1344.docx`.

Read-only Microsoft Word export produced 90 physical pages, including the cover. The report footer numbering runs 1–89 after the cover. Section 3.2 starts on physical page 22 (printed page 21).

Source SHA256 before and after export was unchanged: `174C656399FF4389B4B7B197D002F5AF0EA5B5CC1ACA6058F75BC368D600BF19`.

## Renderer diagnosis

The authoritative dependency runtime is `C:\Users\WASSWA WILSON\.cache\codex-runtimes\codex-primary-runtime\dependencies`.

This Windows dependency bundle contains no LibreOffice. The canonical `render_docx.py` was invoked with PATH limited to bundled Poppler and Windows System32 so the user's desktop LibreOffice could not be used. It failed with `FileNotFoundError: LibreOffice soffice.exe was not found on PATH`. Full diagnostic output is retained in `canonical-render.log`.

The verified fallback exports PDF using a hidden Microsoft Word COM application, opens the source read-only, disables macro automation, repaginates, exports, closes without saving, and validates the unchanged source hash. Rasterization uses only bundled Poppler (`dependencies/native/poppler/Library/bin`) at 144 dpi through bundled Python and pdf2image.

## Reusable commands

Run in PowerShell using the full paths and argument quoting below.

```powershell
& 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\render_word_fallback.ps1' -InputDocx 'D:\coding\ugift-data-analysis\outputs\narrative-report\ugift-working-report-06102026-1344.docx' -OutputDirectory 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\baseline-render'

& 'C:\Users\WASSWA WILSON\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\render_pdf_pages.py' 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\baseline-render\ugift-working-report-06102026-1344.pdf' 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\baseline-render' --dpi 144

& 'C:\Users\WASSWA WILSON\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\render_contact_sheets.py' 'D:\coding\ugift-data-analysis\outputs\narrative-report\reconciliation-06102026\baseline-render'
```

For the final report, replace the source path and use a separate `final-render` output directory. Do not use installed desktop LibreOffice.

## Baseline visual findings

All 90 pages were reviewed in contact-sheet overviews; physical pages 2, 14, 15, 19–23, 42, 56, 74 and 75 were inspected individually at render resolution. There are no obvious page-wide clipping or overlap failures in the baseline.

- Physical page 2 (printed page 1) has `Error! Bookmark not defined.` beside the Table of Contents entry for section 2.6.1 Review of service dates. This defect exists in the supplied source and is before the protected section 3.2 boundary.
- Figure captions for the charts on physical pages 14, 15, 19, 22, and 23 are above their charts. Later chart captions are generally beneath their charts. Many chart image files also contain a thin bright-green right edge.
- The condition table on physical pages 14–15 repeats its header correctly. Financial Table 2 splits across physical pages 20–21, leaving only two body rows plus its note on page 21 and a large blank lower page. Other baseline sparse pages include physical pages 13 and 57. These are baseline layout conditions, not defects introduced by reconciliation.
- The original uses dense green replacement text mixed with red struck-through revisions, notably physical pages 20 and 22 onward. Full added appendix sections beginning on physical page 60 are consistently green.
- Appendix tables generally repeat headers across pages and retain visible grid borders; no clipped table cells were observed in the reviewed detail pages. The longer land-table explanations on physical pages 74–75 wrap within their cells.

Generated PDF, PNG pages, contact sheets and the JSON page inventory are internal QA intermediates.
