# UgIFT asset registers

Use `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx` as the canonical REF register. It contains 229,032 asset rows. The IFMIS update of 28 September 2026 had brought the registers to 234,613 asset rows; KCCA and MoDVA were removed on 29 September 2026. Referral hospitals were removed on 4 October 2026. The Hoima, Arua and Soroti regional blood banks stay. The package retains three stages so recorded source facts remain distinguishable from mapped and completed values.

| File | Purpose |
|---|---|
| `ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx` | Source register with one row per physical asset and source locations. |
| `ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx` | The same asset rows mapped to the MF template. |
| `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx` | Canonical consolidated REF register with supported missing fields completed. |
| `README.md` | Package status, revision history, rebuild instructions and book-code index. |
| `asset-register-audits.json.gz` | Lossless preservation of the three original audit tables, plus revision changes, field fills, documentation changes, validation history and raw-source verification. |
| `consolidation-report.json` | Merge and preservation results, completed fields, and explanations for remaining unsupported or nonapplicable blanks by column. |
| `validation-report.json` | Current IFMIS checks and preserved historical validation findings. |
| `ifmis-review.csv` | Unresolved IFMIS identities and conflicting recorded facts. |

## Referral hospitals removed — 4 October 2026

Removed 5,215 referral-hospital rows from the SK, MF and REF registers. Uganda Blood Transfusion Services stays, including the Hoima and Arua regional blood banks on `UBTS BK`. Soroti Regional Blood Bank stays on `SOROTI BK`. General hospitals held on a district vote were kept. The REF register now contains 229,032 asset rows. The SK and MF registers now contain 229,164 asset rows.

## Comparable-cost follow-up — 2 October 2026

Filled **78** additional unit costs from matched recorded items and treated **16** identified expensed items at nil fixed-asset cost. Recalculated applicable depreciation, July–September YTD, net book value and linked attributes to **30 September 2026**. Remaining **1,540** costs are true blank cells, as requested; no `Pending valuation` text remains in `FIXED_ASSETS_COST` or its matching cost attribute. This supersedes the earlier nonblank-cost requirement. Unknown costs are not treated as zero in financial calculations.

See [cost-borrowing-review.json](cost-borrowing-review.json) and [unpriced-costs.csv](unpriced-costs.csv). The audit archive preserves all before/after cells and donor evidence; prior priced costs and all asset rows remain unchanged.

## Required-column and accounting review — 2 October 2026

Reviewed all **234,351** current REF rows and applied **788,587** cell changes, including dependent financial attributes. All ten requested mandatory columns are nonblank. Standardized **218,901** department entries, clarified Remarks, restored 489 source-confirmed item identities, and supplied **976** comparable cost estimates.

Unresolved facts are explicit: **1,634** costs still require valuation evidence, **1,834** classifications need a clearer item identity, and **298** items have supported unfinished-work status. These review labels do not constitute valid IFMIS load codes. Depreciation is reconciled to **30 September 2026**, with YTD measured from 30 June 2026. Whole-shilling cumulative rounding is capped at the depreciable base; linked cost, life, service-date, depreciation and net-book-value attributes agree. Independent recoverable amounts are retained except demonstrated misplaced entries.

[required-field-review.json](required-field-review.json) gives the exact changes, validation scope and limitations. [required-field-exceptions.csv](required-field-exceptions.csv) lists unresolved review rows. Original and revised cells, donor rows and source-identity evidence are retained in `asset-register-audits.json.gz`. All existing asset identities, unrelated cells, formatting and worksheet controls were preserved; the pre-review workbook is in `tmp/register-revision-20261002/before/`. Earlier dated reviews below are historical.

## Blank-field review — 1 October 2026

Completed **3,443 blank cells on 3,410 existing assets**: 3,341 manufacturer names and 101 product models stated in recorded item descriptions. One missing source-reference note was recovered from the exact MF asset number and its description with the quantity removed. Source facts were checked through stable asset numbers, book codes, descriptions and exact file/row references. Mixed-brand descriptions, compatibility references, sizes and processor generations were excluded.

Every previously populated asset cell, all 234,351 current REF assets, existing formatting and worksheet controls were preserved. Costs, dates and depreciation retain the existing 30 September 2026 convention. The SK and MF source workbooks retain 234,379 rows. This review preserves the existing REF row set; its 28-row difference from the source registers remains a separate reconciliation item.

Unsupported identifiers and purchase facts, inapplicable fields, and financial fills that would require revising populated depreciation values remain for review. [gap-fill-report.json](gap-fill-report.json) gives the current blank counts and verification results. `asset-register-audits.json.gz` retains every fill and its evidence in `gap_fills_20261001`, alongside all prior audit tables.

## IFMIS update — 28 September 2026

The IFMIS update left all three registers with **234,613 physical assets**. The update added **9,481** identified assets, enriched **2,087** existing records, and removed **one proven duplicate** where the two IMEIs of a TELA handset had been recorded as separate assets. Existing rows were preserved except for documented cell updates, that duplicate removal and resulting row-number shifts.

The IFMIS source contains **9,323 TELA handsets**: 9,322 were added and one matched an existing asset. All are **MDA assets under the Ministry of Education and Sports**, with no assignment to existing facilities. A previously recorded TELA asset without an identifier was also reclassified as MDA and remains separately recorded because no exact handset match was available. All ministry-owned additions use the MDA classification. The TELA distribution list supports IMEI reconciliation only; it does not assign the handsets to facilities in this update. DES inspection tablets retain Ministry of Education ownership.

Exact serials, engraved tags and inspection-asset identifiers were compared before insertion. A full scan of all 225,133 baseline REF rows found **zero identifier collisions with the 9,481 proposed additions**. Added records also have no repeated serials or real tags. Fourteen repeated IFMIS identifiers were recorded once. Existing ambiguous matches were not collapsed by item name or description.

**655 source rows require review**, including repeated untagged GNSS component lists, conflicting serial/tag identities and multiple existing matches. They were not inserted as uncertain duplicates. **73 conflicting recorded facts** were preserved rather than overwritten. See `ifmis-review.csv` for these cases and `asset-register-audits.json.gz` for every IFMIS source row, its decision, before/after cell values and duplicate-removal evidence. Historical multiple matches still require review; this update does not certify the entire legacy register as duplicate-free.

New source facts fill gaps and replace identified borrowed values where supported. Related REF depreciation and net book values were refreshed using the existing 30 September 2026 convention. All changed cells, added rows, row sequences and package preservation checks passed. The previous full validator's unrelated findings remain preserved and have not been rerun; `validation-report.json` distinguishes the passing IFMIS checks from that historical result.

The pre-update files are retained in `tmp/ifmis-update-20260928/before/`. The archive also preserves the previous quantity, consolidation and validation records. The standard full rebuild commands below do not replay this incremental IFMIS reconciliation: retain the reviewed update and its audit before regenerating the package.

## Consolidation and validation (27 September baseline)

The original and revised REF workbooks were consolidated under the canonical REF filename. The revised workbook contributed changes on 668 asset rows: 4,918 previously blank cells were filled and 3,206 existing values were revised. A further 2,764 missing fields were recovered through exact source provenance: 2,627 manufacturers, 109 serial numbers, 2 models and 26 purchase dates. In total, 7,682 blank cells were filled.

The additional fields were checked against their original source records and matching physical-asset quantities. Ambiguous serial entries were excluded. Remaining unsupported or nonapplicable blanks are explained by column in `consolidation-report.json`.

Quantity reconciliation covered all 225,133 physical asset rows, and 20,893 amount-conservation checks passed. Full validation still recorded 2,924 findings and 3,260 warnings for review; these are retained in `validation-report.json`.

The original files and cleanup manifests were preserved in `D:/coding/ugift-data-analysis-backups/cleanup-2026-09-27/`. The compressed audit archive retains the original source, source-layout and quantity tables without loss, alongside `revision_changes`, `field_fills`, `documentation_changes`, `validation_history` and `raw_source_verification`.

## Rebuild

Run the pipeline from the repository root; close the output workbooks in Excel before replacing them:

```bash
python scripts/merge_shared_asset_registers.py
python scripts/build_guideline_registers.py
python scripts/list_book_codes.py
```

The rules are documented in [the register population instructions](../PROMPT_POPULATE_ASSET_REGISTERS.md). Regeneration overwrites the generated registers. Preserve reviewed amendments before rebuilding. The book-code command refreshes only the marked index section below.

## Revision history

### 4 October 2026 — referral hospitals removed

5,215 referral-hospital rows were removed from the SK, MF and REF registers. The Hoima, Arua and Soroti regional blood banks stay. The REF register now contains 229,032 asset rows, and the SK and MF registers contain 229,164.

### 29 September 2026 — KCCA and MoDVA removed

51 Kampala Capital City Authority rows and 183 Ministry of Defence and Veteran Affairs rows were removed from the SK, MF and REF registers. The registers now contain 234,379 asset rows.

### 27 September 2026 — partial-column gap fill

Blank cells were filled only in columns that already had values, where the 2023 guidelines or the source register state the value. 2,869 rows gained an Annex 1 class from a field spelling (for example a manual resuscitator or a hydraulic delivery bed). 2,176 missing costs were borrowed from the same asset name or, where the name had no price, from its class (203 in the same local government, 1,235 in other local governments, 738 from the class). 445 lines that are not assets were carried at nil. 259 placed-in-service dates were borrowed for rows that are not work in progress. 2,776 rows were then capitalized, 3,068 expense or loose-tool accounts were filled, and straight-line depreciation to 30 September 2026 was calculated on 2,543 rows. Borrowed costs and dates are marked only by the cell colour. Generic names with no comparable price, work in progress, source serials and purchase dates that were not stated, and account segments the guidelines do not use, stay blank.

### 27 September 2026 — revision before consolidation

The earlier revision was saved as `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx` because the original REF workbook was open in Excel and could not be replaced. It contained 225,133 asset rows. Cost entries were completed on 668 rows, together with their related classification, account and depreciation fields. Focused checks passed all 668 cost and amount mirrors, including cost less accumulated depreciation equalling net book value.

The historical full validator reported quantity matching stopping after 39,197 rows. The cause was a validator defect at a source row that produced no output assets, rather than a truncated quantity audit. That defect was corrected, and the subsequent quantity reconciliation covered all 225,133 rows. The original validation results remain in the audit archive's `validation_history`; facility-name, provenance, date and other review findings remain visible in the current validation report.

### 27 September 2026 — package consolidation

The dated output folders were replaced with descriptive names: `outputs/asset-register-baseline/` for the earlier register, data dictionary and facility book directory, and `outputs/asset-register/` for the current SK, MF and REF package. The original and revised REF files were merged into the canonical REF workbook. This README combined the former generation status and book-code index, and the three CSV audit files were consolidated into the lossless compressed audit archive.

<!-- book-type-code:start -->
## BOOK_TYPE_CODE

173 unique values in `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`.

| No. | Book code | Rows |
|---:|---|---:|
| 1 | ABIM BK | 502 |
| 2 | ADJUMANI BK | 1,706 |
| 3 | AGAGO BK | 1,998 |
| 4 | ALEBTONG BK | 1,985 |
| 5 | AMOLATAR BK | 4,328 |
| 6 | AMUDAT BK | 870 |
| 7 | AMURIA BK | 1,764 |
| 8 | AMURU BK | 1,303 |
| 9 | APAC BK | 2,585 |
| 10 | APAC MC BK | 427 |
| 11 | ARUA BK | 455 |
| 12 | BUDAKA BK | 2,383 |
| 13 | BUDUDA BK | 2,413 |
| 14 | BUGIRI BK | 1,082 |
| 15 | BUGIRI MC BK | 313 |
| 16 | BUGWERI BK | 2,700 |
| 17 | BUHWEJU BK | 2,224 |
| 18 | BUIKWE BK | 1,774 |
| 19 | BUKEDEA BK | 2,666 |
| 20 | BUKOMANSIMBI BK | 1 |
| 21 | BUKWO BK | 2,068 |
| 22 | BULAMBULI BK | 1,544 |
| 23 | BULIISA BK | 1,714 |
| 24 | BUNDIBUGYO BK | 2,170 |
| 25 | BUNYANGABU BK | 628 |
| 26 | BUSHENYI BK | 266 |
| 27 | BUSIA BK | 1,739 |
| 28 | BUTALEJA BK | 1,640 |
| 29 | BUTAMBALA BK | 232 |
| 30 | BUTEBO BK | 1,023 |
| 31 | BUVUMA BK | 423 |
| 32 | BUYENDE BK | 1,832 |
| 33 | DOKOLO BK | 2,806 |
| 34 | FORT PORTAL BK | 1 |
| 35 | FORT PORTAL CITY BK | 521 |
| 36 | GOMBA BK | 534 |
| 37 | GULU BK | 323 |
| 38 | HOIMA BK | 974 |
| 39 | HOIMA CITY BK | 354 |
| 40 | IBANDA BK | 424 |
| 41 | IGANGA BK | 766 |
| 42 | ISINGIRO BK | 1,202 |
| 43 | JINJA BK | 1,285 |
| 44 | JINJA CITY BK | 154 |
| 45 | KAABONG BK | 66 |
| 46 | KABALE BK | 664 |
| 47 | KABALE MC BK | 71 |
| 48 | KABAROLE BK | 1,380 |
| 49 | KABERAMAIDO BK | 1,818 |
| 50 | KAGADI BK | 753 |
| 51 | KAKUMIRO BK | 2,600 |
| 52 | KALAKI BK | 3,192 |
| 53 | KALANGALA BK | 2,752 |
| 54 | KALIRO BK | 2,970 |
| 55 | KALUNGU BK | 918 |
| 56 | KAMULI BK | 3,895 |
| 57 | KAMULI MC BK | 234 |
| 58 | KAMWENGE BK | 614 |
| 59 | KANUNGU BK | 374 |
| 60 | KAPCHORWA BK | 1,038 |
| 61 | KAPCHORWA MC BK | 165 |
| 62 | KAPELEBYONG BK | 823 |
| 63 | KARENGA BK | 20 |
| 64 | KASESE BK | 981 |
| 65 | KASSANDA BK | 1,819 |
| 66 | KATAKWI BK | 2,324 |
| 67 | KAYUNGA BK | 775 |
| 68 | KAZO BK | 909 |
| 69 | KIBAALE BK | 1,094 |
| 70 | KIBOGA BK | 890 |
| 71 | KIBUKU BK | 1,286 |
| 72 | KIIRA MC BK | 231 |
| 73 | KIKUUBE BK | 494 |
| 74 | KIRUHURA BK | 1,473 |
| 75 | KIRYANDONGO BK | 2,985 |
| 76 | KISORO BK | 1,964 |
| 77 | KISORO MC BK | 79 |
| 78 | KITAGWENDA BK | 61 |
| 79 | KITGUM BK | 1,084 |
| 80 | KOBOKO BK | 1,320 |
| 81 | KOBOKO MC BK | 326 |
| 82 | KOLE BK | 1,488 |
| 83 | KOTIDO BK | 49 |
| 84 | KUMI BK | 2,732 |
| 85 | KWANIA BK | 1,782 |
| 86 | KWEEN BK | 1,038 |
| 87 | KYANKWANZI BK | 3,554 |
| 88 | KYEGEGWA BK | 881 |
| 89 | KYENJOJO BK | 2,357 |
| 90 | KYOTERA BK | 292 |
| 91 | LAMWO BK | 1,495 |
| 92 | LIRA BK | 542 |
| 93 | LIRA CITY BK | 1,115 |
| 94 | LUUKA BK | 2,680 |
| 95 | LUWEERO BK | 3,110 |
| 96 | LWENGO BK | 1,475 |
| 97 | LYANTONDE BK | 835 |
| 98 | MAAIF BK | 2,045 |
| 99 | MADI OKOLLO BK | 247 |
| 100 | MAKINDYE SSABAGABO MC BK | 315 |
| 101 | MANAFWA BK | 1,637 |
| 102 | MARACHA BK | 3,013 |
| 103 | MASAKA BK | 35 |
| 104 | MASAKA CITY BK | 89 |
| 105 | MASINDI BK | 1,072 |
| 106 | MASINDI MC BK | 149 |
| 107 | MAYUGE BK | 4,547 |
| 108 | MBALE BK | 564 |
| 109 | MBARARA BK | 1,662 |
| 110 | MBARARA CITY BK | 171 |
| 111 | MGLSD BK | 10 |
| 112 | MITOOMA BK | 1,943 |
| 113 | MITYANA BK | 936 |
| 114 | MOES BK | 10,783 |
| 115 | MOFPED BK | 458 |
| 116 | MOH BK | 264 |
| 117 | MOLG BK | 13 |
| 118 | MOLHUD BK | 27 |
| 119 | MOROTO BK | 927 |
| 120 | MOWE BK | 2,939 |
| 121 | MOWT BK | 88 |
| 122 | MOYO BK | 1,113 |
| 123 | MPIGI BK | 317 |
| 124 | MUBENDE BK | 1,853 |
| 125 | MUBENDE MC BK | 189 |
| 126 | MUKONO BK | 1,929 |
| 127 | MUKONO MC BK | 464 |
| 128 | NABILATUK BK | 248 |
| 129 | NAKAPIRIPIRIT BK | 454 |
| 130 | NAKASEKE BK | 60 |
| 131 | NAKASONGOLA BK | 60 |
| 132 | NAMAYINGO BK | 2,063 |
| 133 | NAMISINDWA BK | 1,292 |
| 134 | NAMUTUMBA BK | 1,823 |
| 135 | NANSANA MC BK | 288 |
| 136 | NAPAK BK | 3,021 |
| 137 | NEBBI BK | 1,251 |
| 138 | NEMA BK | 6 |
| 139 | NGORA BK | 1,110 |
| 140 | NTOROKO BK | 341 |
| 141 | NTUNGAMO BK | 730 |
| 142 | NTUNGAMO MC BK | 76 |
| 143 | NWOYA BK | 793 |
| 144 | OAG BK | 20 |
| 145 | OBONGI BK | 700 |
| 146 | OMORO BK | 1,094 |
| 147 | OPM BK | 10 |
| 148 | OTUKE BK | 1,006 |
| 149 | OYAM BK | 1,528 |
| 150 | PADER BK | 1,171 |
| 151 | PAKWACH BK | 1,559 |
| 152 | PALLISA BK | 6,029 |
| 153 | PPDA BK | 5 |
| 154 | RAKAI BK | 611 |
| 155 | RUBANDA BK | 4,381 |
| 156 | RUBIRIZI BK | 1,780 |
| 157 | RUKIGA BK | 833 |
| 158 | RUKUNGIRI BK | 143 |
| 159 | RUKUNGIRI MC BK | 75 |
| 160 | RWAMPARA BK | 204 |
| 161 | SEMBABULE BK | 454 |
| 162 | SERERE BK | 2,418 |
| 163 | SHEEMA BK | 670 |
| 164 | SHEEMA MC BK | 278 |
| 165 | SIRONKO BK | 1,711 |
| 166 | SOROTI BK | 1,930 |
| 167 | TEREGO BK | 183 |
| 168 | TORORO BK | 9,823 |
| 169 | TORORO MC BK | 1,012 |
| 170 | UBTS BK | 270 |
| 171 | WAKISO BK | 1,596 |
| 172 | YUMBE BK | 3,858 |
| 173 | ZOMBO BK | 2,296 |
<!-- book-type-code:end -->
