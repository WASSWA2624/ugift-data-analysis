# UgIFT asset register

[UGIFT-ASSET-REGISTER-21102026.xlsx](UGIFT-ASSET-REGISTER-21102026.xlsx) is the sole current asset register in this folder.

It contains 228,638 assets on the `Asset Register` worksheet. This is the final reconciled workbook, including standardized asset-status remarks, restored hospital assets and the final scope corrections. The 21 October cleanup changed its filename without changing workbook contents, formulas or formatting.

| File | Purpose |
|---|---|
| `UGIFT-ASSET-REGISTER-21102026.xlsx` | Current reconciled asset register. |
| `UGIFT-ASSET-REGISTER-21102026-AUDIT.zip` | Consolidated audit history, source exceptions and final verification evidence. |
| `README.md` | Current package guide. |

## Engraving from the asset number (21 October 2026)

Where `TAG_NUMBER` read `Not engraved` but the field return's Asset Number column held an asset identifier, that identifier was written into `TAG_NUMBER` and `ATTRIBUTE6(Tag Number (engrave no.))`. No other cell changed.

| Asset number held | Rows | Treatment |
|---|---:|---|
| TELA inspection tablet codes (`E_INSPECTION_DES_nnnn`) | 976 | Written to the tag (other markings) |
| UgIFT codes: Ministry of Finance `UGIFT-BPED/...` and `008/UGF/...` series, Mazimasa `GOU/MOH/UGIFT-PROJECT FY 2023/2024` | 42 | Written to the tag (UgIFT markings) |
| Institutional asset codes: Busota HC III LG register numbers, Arinyapi HC III A-/C-/E- inventory codes, Ministry of Health vehicle registrations, Owiny HC III `009-INV-` codes, Bukakata and Buteza school number ranges | 130 | Written to the tag (other markings) |
| Row numbers of the return's lists | 5,114 | Unchanged |
| Quantities, block or stance counts, capacities | 718 | Unchanged |
| Manufacturer serial, model, lot or catalogue numbers | 523 | Unchanged |
| Descriptions, materials, rooms and placeholders | 297 | Unchanged |

Each value was read against its facility's raw return under `raw-data-grouped/` and independently re-checked. TELA phones carry no asset or tag number (the TELA master list gives IMEIs only) and remain `Not engraved`; the other 218,168 assets had no asset number in their return (`UGIFT-nnnnnn` is the register's own reference).

The register now records 22,138 assets with UgIFT markings (9.7%), 29,168 with other markings (12.8%) and 177,332 not engraved (77.6%).

The audit archive's `manifest.json` records the workbook SHA-256 and checksums for every preserved audit file. The latest scope verification is in `verification/hospital-restoration-work/`; `history/` and the other verification folders retain earlier evidence and may describe superseded asset populations. The archive contains no duplicate workbooks.

Superseded workbooks, Excel temporary files and completed work folders have been removed. Original source deliveries remain in the repository's source-data folders.

To refresh the book-code index without editing the workbook, run `python scripts/list_book_codes.py` from the repository root. Historical generation scripts rebuild an earlier multi-workbook package and do not replay every subsequent reconciliation.
