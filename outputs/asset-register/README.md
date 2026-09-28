# UgIFT asset registers

Use `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx` as the canonical REF register. It contains 234,613 asset rows following the IFMIS update of 28 September 2026. The package retains three stages so recorded source facts remain distinguishable from mapped and completed values.

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

## IFMIS update — 28 September 2026

All three registers now contain **234,613 physical assets**. The update added **9,481** identified assets, enriched **2,087** existing records, and removed **one proven duplicate** where the two IMEIs of a TELA handset had been recorded as separate assets. Existing rows were preserved except for documented cell updates, that duplicate removal and resulting row-number shifts.

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

### 27 September 2026 — partial-column gap fill

Blank cells were filled only in columns that already had values, where the 2023 guidelines or the source register state the value. 2,869 rows gained an Annex 1 class from a field spelling (for example a manual resuscitator or a hydraulic delivery bed). 2,176 missing costs were borrowed from the same asset name or, where the name had no price, from its class (203 in the same local government, 1,235 in other local governments, 738 from the class). 445 lines that are not assets were carried at nil. 259 placed-in-service dates were borrowed for rows that are not work in progress. 2,776 rows were then capitalized, 3,068 expense or loose-tool accounts were filled, and straight-line depreciation to 30 September 2026 was calculated on 2,543 rows. Borrowed costs and dates are marked only by the cell colour. Generic names with no comparable price, work in progress, source serials and purchase dates that were not stated, and account segments the guidelines do not use, stay blank.

### 27 September 2026 — revision before consolidation

The earlier revision was saved as `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx` because the original REF workbook was open in Excel and could not be replaced. It contained 225,133 asset rows. Cost entries were completed on 668 rows, together with their related classification, account and depreciation fields. Focused checks passed all 668 cost and amount mirrors, including cost less accumulated depreciation equalling net book value.

The historical full validator reported quantity matching stopping after 39,197 rows. The cause was a validator defect at a source row that produced no output assets, rather than a truncated quantity audit. That defect was corrected, and the subsequent quantity reconciliation covered all 225,133 rows. The original validation results remain in the audit archive's `validation_history`; facility-name, provenance, date and other review findings remain visible in the current validation report.

### 27 September 2026 — package consolidation

The dated output folders were replaced with descriptive names: `outputs/asset-register-baseline/` for the earlier register, data dictionary and facility book directory, and `outputs/asset-register/` for the current SK, MF and REF package. The original and revised REF files were merged into the canonical REF workbook. This README combined the former generation status and book-code index, and the three CSV audit files were consolidated into the lossless compressed audit archive.

<!-- book-type-code:start -->
## BOOK_TYPE_CODE

196 unique values in `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`.

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
| 79 | KCCA BK | 51 |
| 80 | KIBAALE BK | 1,194 |
| 81 | KIBOGA BK | 890 |
| 82 | KIBUKU BK | 1,286 |
| 83 | KIIRA MC BK | 231 |
| 84 | KIKUUBE BK | 494 |
| 85 | KIRUDDU RH BK | 283 |
| 86 | KIRUHURA BK | 1,473 |
| 87 | KIRYANDONGO BK | 2,985 |
| 88 | KISORO BK | 1,964 |
| 89 | KISORO MC BK | 79 |
| 90 | KITAGWENDA BK | 61 |
| 91 | KITGUM BK | 1,084 |
| 92 | KOBOKO BK | 1,320 |
| 93 | KOBOKO MC BK | 326 |
| 94 | KOLE BK | 1,488 |
| 95 | KOTIDO BK | 49 |
| 96 | KUMI BK | 2,732 |
| 97 | KWANIA BK | 1,782 |
| 98 | KWEEN BK | 1,038 |
| 99 | KYANKWANZI BK | 3,554 |
| 100 | KYEGEGWA BK | 881 |
| 101 | KYENJOJO BK | 2,357 |
| 102 | KYOTERA BK | 292 |
| 103 | LAMWO BK | 1,495 |
| 104 | LIRA BK | 542 |
| 105 | LIRA CITY BK | 1,115 |
| 106 | LIRA RRH BK | 214 |
| 107 | LUUKA BK | 2,680 |
| 108 | LUWEERO BK | 3,110 |
| 109 | LWENGO BK | 1,475 |
| 110 | LYANTONDE BK | 835 |
| 111 | MAAIF BK | 2,045 |
| 112 | MADI OKOLLO BK | 247 |
| 113 | MAKINDYE SSABAGABO MC BK | 315 |
| 114 | MANAFWA BK | 1,637 |
| 115 | MARACHA BK | 3,013 |
| 116 | MASAKA BK | 35 |
| 117 | MASAKA CITY BK | 89 |
| 118 | MASAKA RRH BK | 363 |
| 119 | MASINDI BK | 1,072 |
| 120 | MASINDI MC BK | 149 |
| 121 | MAYUGE BK | 4,547 |
| 122 | MBALE BK | 564 |
| 123 | MBALE RRH BK | 229 |
| 124 | MBARARA BK | 1,662 |
| 125 | MBARARA CITY BK | 171 |
| 126 | MBARARA RRH BK | 271 |
| 127 | MGLSD BK | 10 |
| 128 | MITOOMA BK | 1,943 |
| 129 | MITYANA BK | 936 |
| 130 | MODV BK | 183 |
| 131 | MOES BK | 10,783 |
| 132 | MOFPED BK | 458 |
| 133 | MOH BK | 264 |
| 134 | MOLG BK | 13 |
| 135 | MOLHUD BK | 27 |
| 136 | MOROTO BK | 927 |
| 137 | MOROTO RRH BK | 368 |
| 138 | MOWE BK | 2,939 |
| 139 | MOWT BK | 88 |
| 140 | MOYO BK | 1,113 |
| 141 | MPIGI BK | 317 |
| 142 | MUBENDE BK | 1,853 |
| 143 | MUBENDE MC BK | 189 |
| 144 | MUBENDE RRH BK | 220 |
| 145 | MUKONO BK | 1,929 |
| 146 | MUKONO MC BK | 464 |
| 147 | MULAGO NRH BK | 138 |
| 148 | NABILATUK BK | 248 |
| 149 | NAGURU RH BK | 248 |
| 150 | NAKAPIRIPIRIT BK | 454 |
| 151 | NAKASEKE BK | 60 |
| 152 | NAKASONGOLA BK | 60 |
| 153 | NAMAYINGO BK | 2,063 |
| 154 | NAMISINDWA BK | 1,292 |
| 155 | NAMUTUMBA BK | 1,823 |
| 156 | NANSANA MC BK | 288 |
| 157 | NAPAK BK | 3,021 |
| 158 | NEBBI BK | 1,251 |
| 159 | NEMA BK | 6 |
| 160 | NGORA BK | 1,110 |
| 161 | NTOROKO BK | 341 |
| 162 | NTUNGAMO BK | 730 |
| 163 | NTUNGAMO MC BK | 76 |
| 164 | NWOYA BK | 793 |
| 165 | OAG BK | 20 |
| 166 | OBONGI BK | 700 |
| 167 | OMORO BK | 1,094 |
| 168 | OPM BK | 10 |
| 169 | OTUKE BK | 1,006 |
| 170 | OYAM BK | 1,528 |
| 171 | PADER BK | 1,171 |
| 172 | PAKWACH BK | 1,559 |
| 173 | PALLISA BK | 6,030 |
| 174 | PPDA BK | 5 |
| 175 | RAKAI BK | 611 |
| 176 | RUBANDA BK | 4,381 |
| 177 | RUBIRIZI BK | 1,780 |
| 178 | RUKIGA BK | 833 |
| 179 | RUKUNGIRI BK | 143 |
| 180 | RUKUNGIRI MC BK | 75 |
| 181 | RWAMPARA BK | 204 |
| 182 | SEMBABULE BK | 454 |
| 183 | SERERE BK | 2,418 |
| 184 | SHEEMA BK | 670 |
| 185 | SHEEMA MC BK | 278 |
| 186 | SIRONKO BK | 1,711 |
| 187 | SOROTI BK | 1,930 |
| 188 | SOROTI RRH BK | 214 |
| 189 | TEREGO BK | 183 |
| 190 | TORORO BK | 9,823 |
| 191 | TORORO MC BK | 1,012 |
| 192 | UBTS BK | 273 |
| 193 | WAKISO BK | 1,596 |
| 194 | YUMBE BK | 3,858 |
| 195 | YUMBE RRH BK | 112 |
| 196 | ZOMBO BK | 2,296 |
<!-- book-type-code:end -->
