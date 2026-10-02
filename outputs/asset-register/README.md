# UgIFT asset registers

Use `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx` as the canonical REF register. It contains 234,351 asset rows. The IFMIS update of 28 September 2026 had brought the registers to 234,613 asset rows; KCCA and MoDVA were removed on 29 September 2026. The package retains three stages so recorded source facts remain distinguishable from mapped and completed values.

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

194 unique values in `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`.

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
| 12 | ARUA RRH BK | 251 |
| 13 | BUDAKA BK | 2,383 |
| 14 | BUDUDA BK | 2,413 |
| 15 | BUGIRI BK | 1,082 |
| 16 | BUGIRI MC BK | 313 |
| 17 | BUGWERI BK | 2,700 |
| 18 | BUHWEJU BK | 2,224 |
| 19 | BUIKWE BK | 1,774 |
| 20 | BUKEDEA BK | 2,666 |
| 21 | BUKOMANSIMBI BK | 1 |
| 22 | BUKWO BK | 2,068 |
| 23 | BULAMBULI BK | 1,544 |
| 24 | BULIISA BK | 1,714 |
| 25 | BUNDIBUGYO BK | 2,170 |
| 26 | BUNYANGABU BK | 628 |
| 27 | BUSHENYI BK | 266 |
| 28 | BUSIA BK | 1,739 |
| 29 | BUTABIKA NRMH BK | 288 |
| 30 | BUTALEJA BK | 1,640 |
| 31 | BUTAMBALA BK | 232 |
| 32 | BUTEBO BK | 1,023 |
| 33 | BUVUMA BK | 423 |
| 34 | BUYENDE BK | 1,832 |
| 35 | DOKOLO BK | 2,806 |
| 36 | ENTEBBE RH BK | 269 |
| 37 | FORT PORTAL BK | 1 |
| 38 | FORT PORTAL CITY BK | 521 |
| 39 | FORT PORTAL RRH BK | 203 |
| 40 | GOMBA BK | 534 |
| 41 | GULU BK | 323 |
| 42 | GULU RRH BK | 301 |
| 43 | HOIMA BK | 974 |
| 44 | HOIMA CITY BK | 354 |
| 45 | HOIMA RRH BK | 223 |
| 46 | IBANDA BK | 424 |
| 47 | IGANGA BK | 766 |
| 48 | ISINGIRO BK | 1,202 |
| 49 | JINJA BK | 1,285 |
| 50 | JINJA CITY BK | 154 |
| 51 | JINJA RRH BK | 305 |
| 52 | KAABONG BK | 66 |
| 53 | KABALE BK | 664 |
| 54 | KABALE MC BK | 71 |
| 55 | KABALE RRH BK | 347 |
| 56 | KABAROLE BK | 1,380 |
| 57 | KABERAMAIDO BK | 1,818 |
| 58 | KAGADI BK | 753 |
| 59 | KAKUMIRO BK | 2,600 |
| 60 | KALAKI BK | 3,192 |
| 61 | KALANGALA BK | 2,752 |
| 62 | KALIRO BK | 2,970 |
| 63 | KALUNGU BK | 918 |
| 64 | KAMULI BK | 3,895 |
| 65 | KAMULI MC BK | 234 |
| 66 | KAMWENGE BK | 642 |
| 67 | KANUNGU BK | 374 |
| 68 | KAPCHORWA BK | 1,038 |
| 69 | KAPCHORWA MC BK | 165 |
| 70 | KAPELEBYONG BK | 823 |
| 71 | KARENGA BK | 20 |
| 72 | KASESE BK | 981 |
| 73 | KASSANDA BK | 1,819 |
| 74 | KATAKWI BK | 2,324 |
| 75 | KAWEMPE RH BK | 196 |
| 76 | KAYUNGA BK | 775 |
| 77 | KAYUNGA RRH BK | 172 |
| 78 | KAZO BK | 909 |
| 79 | KIBAALE BK | 1,194 |
| 80 | KIBOGA BK | 890 |
| 81 | KIBUKU BK | 1,286 |
| 82 | KIIRA MC BK | 231 |
| 83 | KIKUUBE BK | 494 |
| 84 | KIRUDDU RH BK | 283 |
| 85 | KIRUHURA BK | 1,473 |
| 86 | KIRYANDONGO BK | 2,985 |
| 87 | KISORO BK | 1,964 |
| 88 | KISORO MC BK | 79 |
| 89 | KITAGWENDA BK | 61 |
| 90 | KITGUM BK | 1,084 |
| 91 | KOBOKO BK | 1,320 |
| 92 | KOBOKO MC BK | 326 |
| 93 | KOLE BK | 1,488 |
| 94 | KOTIDO BK | 49 |
| 95 | KUMI BK | 2,732 |
| 96 | KWANIA BK | 1,782 |
| 97 | KWEEN BK | 1,038 |
| 98 | KYANKWANZI BK | 3,554 |
| 99 | KYEGEGWA BK | 881 |
| 100 | KYENJOJO BK | 2,357 |
| 101 | KYOTERA BK | 292 |
| 102 | LAMWO BK | 1,495 |
| 103 | LIRA BK | 542 |
| 104 | LIRA CITY BK | 1,115 |
| 105 | LIRA RRH BK | 214 |
| 106 | LUUKA BK | 2,680 |
| 107 | LUWEERO BK | 3,110 |
| 108 | LWENGO BK | 1,475 |
| 109 | LYANTONDE BK | 835 |
| 110 | MAAIF BK | 2,045 |
| 111 | MADI OKOLLO BK | 247 |
| 112 | MAKINDYE SSABAGABO MC BK | 315 |
| 113 | MANAFWA BK | 1,637 |
| 114 | MARACHA BK | 3,013 |
| 115 | MASAKA BK | 35 |
| 116 | MASAKA CITY BK | 89 |
| 117 | MASAKA RRH BK | 363 |
| 118 | MASINDI BK | 1,072 |
| 119 | MASINDI MC BK | 149 |
| 120 | MAYUGE BK | 4,547 |
| 121 | MBALE BK | 564 |
| 122 | MBALE RRH BK | 229 |
| 123 | MBARARA BK | 1,662 |
| 124 | MBARARA CITY BK | 171 |
| 125 | MBARARA RRH BK | 271 |
| 126 | MGLSD BK | 10 |
| 127 | MITOOMA BK | 1,943 |
| 128 | MITYANA BK | 936 |
| 129 | MOES BK | 10,783 |
| 130 | MOFPED BK | 458 |
| 131 | MOH BK | 264 |
| 132 | MOLG BK | 13 |
| 133 | MOLHUD BK | 27 |
| 134 | MOROTO BK | 927 |
| 135 | MOROTO RRH BK | 368 |
| 136 | MOWE BK | 2,939 |
| 137 | MOWT BK | 88 |
| 138 | MOYO BK | 1,113 |
| 139 | MPIGI BK | 317 |
| 140 | MUBENDE BK | 1,853 |
| 141 | MUBENDE MC BK | 189 |
| 142 | MUBENDE RRH BK | 220 |
| 143 | MUKONO BK | 1,929 |
| 144 | MUKONO MC BK | 464 |
| 145 | MULAGO NRH BK | 138 |
| 146 | NABILATUK BK | 248 |
| 147 | NAGURU RH BK | 248 |
| 148 | NAKAPIRIPIRIT BK | 454 |
| 149 | NAKASEKE BK | 60 |
| 150 | NAKASONGOLA BK | 60 |
| 151 | NAMAYINGO BK | 2,063 |
| 152 | NAMISINDWA BK | 1,292 |
| 153 | NAMUTUMBA BK | 1,823 |
| 154 | NANSANA MC BK | 288 |
| 155 | NAPAK BK | 3,021 |
| 156 | NEBBI BK | 1,251 |
| 157 | NEMA BK | 6 |
| 158 | NGORA BK | 1,110 |
| 159 | NTOROKO BK | 341 |
| 160 | NTUNGAMO BK | 730 |
| 161 | NTUNGAMO MC BK | 76 |
| 162 | NWOYA BK | 793 |
| 163 | OAG BK | 20 |
| 164 | OBONGI BK | 700 |
| 165 | OMORO BK | 1,094 |
| 166 | OPM BK | 10 |
| 167 | OTUKE BK | 1,006 |
| 168 | OYAM BK | 1,528 |
| 169 | PADER BK | 1,171 |
| 170 | PAKWACH BK | 1,559 |
| 171 | PALLISA BK | 6,030 |
| 172 | PPDA BK | 5 |
| 173 | RAKAI BK | 611 |
| 174 | RUBANDA BK | 4,381 |
| 175 | RUBIRIZI BK | 1,780 |
| 176 | RUKIGA BK | 833 |
| 177 | RUKUNGIRI BK | 143 |
| 178 | RUKUNGIRI MC BK | 75 |
| 179 | RWAMPARA BK | 204 |
| 180 | SEMBABULE BK | 454 |
| 181 | SERERE BK | 2,418 |
| 182 | SHEEMA BK | 670 |
| 183 | SHEEMA MC BK | 278 |
| 184 | SIRONKO BK | 1,711 |
| 185 | SOROTI BK | 1,930 |
| 186 | SOROTI RRH BK | 214 |
| 187 | TEREGO BK | 183 |
| 188 | TORORO BK | 9,823 |
| 189 | TORORO MC BK | 1,012 |
| 190 | UBTS BK | 273 |
| 191 | WAKISO BK | 1,596 |
| 192 | YUMBE BK | 3,858 |
| 193 | YUMBE RRH BK | 112 |
| 194 | ZOMBO BK | 2,296 |
<!-- book-type-code:end -->
