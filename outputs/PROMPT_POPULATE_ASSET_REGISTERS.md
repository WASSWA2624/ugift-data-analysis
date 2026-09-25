# Prompt: build the UgIFT asset registers

You are populating three workbooks. Do the stages in order. Read `GOU Asset Accounting Policies and Guidelines 2023.pdf` from start to finish before filling the MF or REF workbook, including the recognition, measurement, depreciation, and small-asset sections and Annex 1. For every column in the sample header, fill it when that reading or the source states the value. Leave it blank only after that check shows neither source applies. A class, an Annex 1 life, a nil residual, straight-line depreciation, `CAPITALIZED`, and `Not Engraved` are guideline values. Do not guess a code, life, or class the guidelines do not state.

Read these before writing any row:

- `raw-data-grouped/`
- `GOU Asset Accounting Policies and Guidelines 2023.pdf` (April 2023), especially sections 3.2.1, 3.2.2, 3.3.3, 3.3.5, and 5, and Annex 1
- `Sample Header of Asset Register..xlsx`
- `outputs/asset-register-2026-09-22/UgIFT Asset Register Data Dictionary.xlsx` for the one-row-per-asset rule already used on existing assets

Outputs:

1. `outputs/asset-register-2026-09-23/ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx`
2. `outputs/asset-register-2026-09-23/ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx` filled from the SK workbook
3. `outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`, a sanitized copy of the MF workbook with missing purchase costs filled by the borrowing rules below

Health centres and seed schools are rows in one workbook, not separate files. Keep header filters and a frozen header row. On the Read Me sheet, record the guideline sections used and, for any sample-header column left blank, the reason it did not apply.

## Stage 1. SK register from `raw-data-grouped`

Build one shared register. Columns follow the health-centre and seed-school templates:

Equipment/Item, Department, Asset Number, Item Description, Life in Months, Tag Number (engrave no.), Date Of Purchase, Date Placed In Service, Recoverable cost, Cost, Acc Dep Cost, Net Book Value, Ytd Deprn, Equipment status, Remarks, Local Government, Facility, Facility type, Unit, Source file, Source location.

### Which files to read

Read `.xls`, `.xlsx`, and `.docx` under `raw-data-grouped`.

Leave out `_multi-team/programme-documents`, except `data-management-chat`. Skip lock files (`~$`). Skip photographs, narrative reports, and reconciliation lists. A Word or Excel file is an asset source only when it has an asset table (an Equipment/Item header, or a description column together with condition, quantity, tag, or cost).

In one folder, if the same file stem exists as both a spreadsheet and a Word file, keep the spreadsheet. Drop exact byte-for-byte duplicates. Skip draft sheets named like `Table 1` or `Sheet 1` when that workbook already has a consolidated sheet with local-government and facility columns.

Facility and local government come from the row, then from a banner on the sheet, then from the folder path `team-NN/<Local government>/<Facility>/`.

### Union per facility

A facility may have been submitted more than once. Treat two returns as the same facility when the normalised local government and facility name match.

Keep every distinct item. When the same line appears in more than one return, keep it once, from the return with the larger stated count. A line that appears in only one return is kept. Identity is the engraved tag plus item name when a real tag exists. Otherwise identity is item name, description, status, and department. Ignore a tag that is blank, `N/A`, `none`, `nil`, or `not engraved`. Ignore a trailing count or a quantity in brackets when comparing item names (`Desks 120` and `Desks` are the same item).

### One row per physical asset

This is the rule already used in `outputs/asset-register-2026-09-22`. Each source quantity becomes that many rows. `Unit` is `item 1 of 100`, `item 2 of 100`, and so on. A line that is already one item stays one row.

Read a quantity only from a stated count:

- a quantity column, when the number is from 2 to 500
- a number in brackets on the item name, such as `B.P. Machine, Digital(2)`
- a trailing count on the item name, such as `Examination Couch 2` or `School desks 120`
- a bare integer in Asset Number, when that is the only line for that item and the tag is blank or not engraved, such as 286 office chairs
- a bare integer, or a leading count, in the description or Asset Number, such as `2 microscopes, white`
- a count written in status or remarks, such as `116 verified as good then 4 damaged`, `39 desks were supplied`, or `2 functional and one in the store`

Do not treat these as quantities:

- model numbers: LaserJet 1320, Laptop 840, EliteBook, ProBook, Latitude, and a trailing number whose last word is laserjet, laptop, printer, monitor, cpu, inch, gen, or core
- a measure: `15 inch`, `20 liters`
- a calendar year from 1990 to 2035
- a number above 500
- a trailing count above 40 unless the item is a bulk item (desk, chair, stool, table, shelf, bench, bed, cupboard, couch, cylinder)
- an Asset Number that sits on a row which already has a real engraved tag
- the same item text repeated on many rows that are already one asset each

When Asset Number or the description was only the count, clear that field on the exploded rows. When a phrase such as `2 microscopes, white` was the count, keep `microscopes, white` as the description. Where the grouped line has one numeric cost, recoverable cost, accumulated depreciation, net book value, or year-to-date depreciation, treat it as the line total and divide it by the quantity so each row holds its share.

## Stage 2. MF register from the SK workbook

Copy `Sample Header of Asset Register..xlsx` headers into columns A–BL (64 columns). Fill each SK row into one MF row. Do not change the SK workbook. After the mapping below, apply the guidelines to every column they cover.

Map an SK column into A–AW only when the sample header and the 2023 guidelines give that column a meaning the source can fill:

| SK column | MF column | Rule |
|---|---|---|
| Local Government | BOOK_TYPE_CODE | Strip district wording, keep MC or City, append ` BK`. Example: `MADI OKOLLO BK`. |
| Local Government | LOCATION_SEGMENT1 | Vote form. Example: `MADI\-OKOLLO DLG`. |
| Equipment/Item, else Item Description | DESCRIPTION | If Unit is set, append it: `Desks [item 1 of 100]`. |
| Department | LOCATION_SEGMENT2 | |
| Facility | LOCATION_SEGMENT3 | |
| Cost, after the per-item division | FIXED_ASSETS_COST | |
| Date Placed In Service | DATE_PLACED_IN_SERVICE | |
| Acc Dep Cost | DEPRN_RESERVE | Only the amount written on the source. |
| Ytd Deprn | YTD_DEPRN | Only the amount written on the source. |
| Asset Number | ASSET_NUMBER | Blank when that cell was the quantity. |
| Tag Number | TAG_NUMBER | |
| Life in Months, when greater than 0 | LIFE_IN_MONTHS, DEPRECIATE_FLAG `YES`, DEPRN_METHOD_CODE `STL` | Section 5.5: straight line. |
| Equipment status | IN_USE_FLAG | `YES` for in use, functional, functioning, working well, available, or good condition. `NO` for not in use, not received, obsolete, unserviceable, disposed, lost, or missing. Otherwise blank. |

`FIXED_ASSETS_UNITS` is 1 on every row.

`ATTRIBUTE1`–`ATTRIBUTE15` keep the sample headers. Fill each one when the guidelines’ attribute guide for that asset class defines it and the source states the fact. Do not rename those headers to SK column names. An SK field with no column in A–BL and no class attribute is written in Remarks, labelled with the source column name.

Fill `PRORATE_CONVENTION_CODE` when the guidelines state the convention. Fill an expense-account or clearing-account segment only when the guidelines state that segment, including account 221012 for small office equipment and loose tools that are not capitalized. Leave `LOCATION_SEGMENT4`, `ASSET_KEY_SEGMENT1`, `EMPLOYEE_NUMBER`, `AMORTIZATION_START_DATE`, `AMORTIZE_NBV_FLAG`, and `ASSET_CATEGORY_MINOR3` blank unless the guidelines or the source state them. Recoverable cost is not salvage value. The guidelines use salvage as the residual in a class life, and recoverable amount as an impairment test.

### Columns the SK workbook does not provide

Open the 2023 guidelines and fill only what they decide.

**Classification.** Set ASSET_CATEGORY_MAJOR, ASSET_CATEGORY_MINOR1, and ASSET_CATEGORY_MINOR2 from the asset description, using the classes in the guidelines and Annex 1. Leave all three blank when the name is generic (`equipment`, `item`, `set`, `machine`) or is a total, a count, or a consumable pack. Do not guess a class from the facility type alone.

**Useful life and depreciation.** If the source life is blank and Annex 1 gives a life for the class you assigned, use that life in months, set DEPRECIATE_FLAG to `YES` and DEPRN_METHOD_CODE to `STL`. The guidelines depreciate ICT and other equipment over 5 years (60 months) in the photocopier illustration. Land does not depreciate: DEPRECIATE_FLAG `NO`, no life. Work in progress and assets held under an operating lease do not depreciate (section 5.5). Section 5.7: residual value is nil, so SALVAGE_VALUE is 0 only on a row you have marked depreciable. If the source already recorded a residual, keep it.

**Serial, model, manufacturer.** Fill SERIAL_NUMBER, MODEL_NUMBER, or MANUFACTURER_NAME only when the description states one explicit value (`serial`, `s/n`, `model`, `made by`). A product name such as LaserJet 1320 may be the model; do not also treat it as a quantity.

### Which assets are capitalized

Set ASSET_TYPE to `CAPITALIZED` only when every condition in section 3.2.1 holds:

1. The vote or facility controls the asset: it can use it, benefit from it, charge for it, or deny its use to others.
2. Future economic benefits or service potential are expected, with at least a 50 percent chance, and the benefit lasts more than one year (section 3.2.1.2). That is the non-current-asset test. There is no monetary capitalization threshold (section 3.2.2.1).
3. The asset exists because of a past purchase, transfer, donation, or verified delivery. An intention to buy is not an asset.
4. Cost can be measured from the source line or, later, from a borrowed comparable price on the REF workbook. If no cost can be measured, leave ASSET_TYPE blank.

Do not capitalize, and leave ASSET_TYPE blank, when section 3.3.3 applies. Small office equipment and loose tools are expensed on account 221012 and treated as inventories. The guidelines name kettles, spoons, forks, calculators, stapling machines, pen-holders, punches, paper trays, pin and staple holders, and typewriters. Also leave ASSET_TYPE blank for single-use packs, graph paper, and other consumables.

Section 3.3.5 allows a vote to capitalize a group of similar low-value units as one group asset, with subsidiary records for each unit. This register is that subsidiary record. Keep one row per physical asset. Mark each of those rows `CAPITALIZED` when the conditions above hold. Do not collapse 100 desks back into one row.

A repair or spare that only restores the asset is not a new capitalized asset (section 3.2.3). A major replacement that extends life or service potential is added to the existing asset, not entered as a second asset, unless the source listed it as its own asset.

Land is capitalized and is not depreciated. Natural resources are not capitalized (section 3.2.1.4).

## Sanitize the MF and REF workbooks

Sanitize `ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx` after Stage 2. Copy that sanitized workbook to `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`, then apply the same rules again so a borrowed-cost edit cannot put raw source wording back. Do not change a recorded cost, life, or depreciation figure while sanitizing. Keep the `[item 1 of 100]` suffix.

**Every column.** Sanitize every filled cell in MF and again in REF. Trim text, collapse repeated spaces, and remove line breaks. Use one spelling for the same fact on every row. Clear a cell whose whole value is a placeholder (`N/A`, `NA`, `nil`, `nill`, `none`, `null`, `-`, `not applicable`). Do not clear a real engraved tag. Do not change a recorded amount while cleaning text.

**BOOK_TYPE_CODE.** This column is cleaned on every row. One local government has one code. Uppercase. Remove `District`, `Local Government`, `DLG`, and backslashes. Turn a hyphen into a space. Keep `MC` or `CITY` where that is the vote. Append ` BK`. Examples: `Hoima District` becomes `HOIMA BK`; `Madi-Okollo` becomes `MADI OKOLLO BK`; `Kiira Municipal Council` becomes `KIIRA MC BK`. Do not leave a raw district name in this column. `LOCATION_SEGMENT1` is the same government in vote form, such as `MADI\-OKOLLO DLG`.

**Facility name** (`LOCATION_SEGMENT3`). A school ends with `Seed Secondary School`. A health centre ends with `Health Centre III`, including a master Health Centre II that was upgraded. Spell the words in full. Do not write `HCII`, `HC III`, `H/C`, `H.C`, or `Health Center`. Do not add the suffix twice. Keep a longer official name that already contains those words, such as `St Mugagga Vocational Seed Secondary School`.

**Facility type.** Where the facility type is written, it is only `School` or `Health centre`.

**Condition.** Equipment status is only `Functional` or `Faulty`. `Functional` covers in use, functioning, working well, available, verified, and good condition. `Faulty` covers damaged, broken, not in use, not functioning, not received, obsolete, unserviceable, disposed, lost, and missing. Move any longer status wording into Remarks. If the source does not say which, leave the status blank. Set `IN_USE_FLAG` to `YES` for Functional and `NO` for Faulty.

**Tag.** A blank tag, or a placeholder tag, is `Not Engraved`. Keep a real engraved number as written.

**Amounts.** Show cost, depreciation, reserve, and net book value with thousands separators (`#,##0.##`). Do not recalculate them in this step.

## Stage 3. REF workbook: borrowed purchase costs

Start from the sanitized MF workbook. Then fill missing purchase costs. Do not change a price that is already recorded. After borrowing, the facility name, facility type, status, and tag rules above still hold.

Existing purchase prices keep a **white** background.

Borrow only for a specific asset name. Do not borrow for a generic name such as equipment, furniture, medical equipment, item, set, machine, buildings, or land. Compare assets with the same normalised name. Where both rows have an asset class, the class must match. The borrowed price is the median of the matching prices, in Uganda shillings.

Search in this order:

1. **Same local government.** Use assets purchased in the same year. If none, use the closest year. Colour the cost cell **blue** (`#9DC3E6`).
2. **Other local governments.** Use the same year, or the nearest period. Colour the cost cell **orange** (`#F4B183`).
3. **The whole workbook.** Use this only when steps 1 and 2 find no price. Colour the cost cell **green** (`#C6EFCE`).

Do not write a borrowed price or a borrowed life in Remarks, or in `ATTRIBUTE6(Remarks)`. That column must never say the cost or life came from another asset, local government, year, or median. The cell colour on the cost or life is the only marker. A life already on the row stays white and unchanged.

A missing useful life may be borrowed in the same order and with the same colours. Use the most common life of the matching assets, and only where life is at least 12 months and the asset is not marked out of use.

Where cost, a nil residual (section 5.7), life in months, and the month placed in service are known, and the asset is in use, calculate straight-line depreciation to 30 September 2026. Monthly charge = (cost − residual) / life in months. Accumulated depreciation runs from the placed-in-service month through September 2026 and stops at the end of useful life. Year-to-date depreciation is the July–September 2026 portion. Net book value is cost minus accumulated depreciation. Leave any of those amounts unchanged when the source already recorded them.

After a borrowed cost makes measurement possible, set ASSET_TYPE to `CAPITALIZED` if the Stage 2 tests are met and the row is not small office equipment or a loose tool.
