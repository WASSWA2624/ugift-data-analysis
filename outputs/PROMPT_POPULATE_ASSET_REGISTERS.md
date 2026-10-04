# Prompt: build the UgIFT asset registers

You are populating three workbooks. Do the stages in order. Read `GOU Asset Accounting Policies and Guidelines 2023.pdf` from start to finish before filling the MF or REF workbook, including the recognition, measurement, depreciation and small-asset sections and Annex 1. You are the accountant for this register. You already know how each calculated column on `outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx` is derived. Calculate those columns on every REF row. Do not leave a calculated amount blank when its inputs can be read or borrowed.

Every physical asset must have its own row in SK, MF and REF. Expand a stated quantity of N assets into exactly N rows, even when the resulting entries are otherwise identical. This applies wherever the quantity is stated: the description, item name, quantity column, or any other column.

For every other column in the sample header, fill it when the guidelines or a source state the value. If a value is unclear, or a field is empty, go back to the source and read it again before you leave the cell blank. Scan every file and every folder that can state that fact. Start in `raw-data-grouped/`, which holds the union of `raw-data-ungrouped/` and `new-raw-data-221092026-1114/` (see `raw-data-grouped/README.md`), so no separate file scan of those two folders is needed. Use `new-templates-to-follow/` for the column layout and as a source of facts for a facility already on the register. Leave a non-calculated cell blank only when that full scan and the guidelines still do not apply. A class, an Annex 1 life, a nil residual, straight-line depreciation, `CAPITALIZED`, and `Not engraved` are guideline values. Do not guess a code, life, or class the guidelines do not state.

## How the registers are reproduced

The three scripts under `scripts/` implement every rule in this prompt. Running them in this order from the repository root rebuilds the three workbooks and the book-code index:

```bash
python scripts/merge_shared_asset_registers.py
python scripts/build_guideline_registers.py
python scripts/list_book_codes.py
```

The first script is Stage 1 (about an hour), the second is Stages 2 and 3 (it reads the whole SK workbook twice to index donors, then writes MF and REF; about forty minutes), the third rewrites the `BOOK_TYPE_CODE` section of `outputs/asset-register/README.md`. Close any of the output workbooks in Excel before running; a `~$` lock file in the output folder makes the save fail. `python scripts/build_guideline_registers.py --limit 6000 --sk <copy of the SK> --out <folder>` runs a sample against a copy. When a rule in this prompt changes, change the script that implements it, then rebuild.

Read these before writing any row:

- `raw-data-grouped/`, including `facility-reconciliation.csv` (the master list, the reconciled facility names, the local government of each facility) and `supervisor-decisions.csv` (the supervisor's rulings on names and governments)
- `new-templates-to-follow/` (`Health Center Updated Asset Register.xlsx` and `Seed School Updated Asset Register.xlsx`) for the column layout and for facts about a facility already on the register
- `GOU Asset Accounting Policies and Guidelines 2023.pdf` (April 2023), especially sections 3.2.1, 3.2.2, 3.2.3, 3.3.3, 3.3.5, 5.5, 5.7 and 5.14, and Annex 1 and Annex 2
- `Sample Header of Asset Register..xlsx` (the 64 headers and one example row)
- `Location(3)2.xlsx`, the IFMS location master: the vote codes and departments IFMS accepts
- `outputs/asset-register-baseline/UgIFT Asset Register Data Dictionary.xlsx` for the one-row-per-asset rule already used on existing assets

Outputs:

1. `outputs/asset-register/ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx`
2. `outputs/asset-register/ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx` filled from the SK workbook
3. `outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`, a sanitized copy of the MF workbook with missing purchase costs, dates and lives filled by the borrowing rules below, every calculated column computed, and every column of the not-blank list filled
4. `outputs/asset-register/README.md#book_type_code`, every distinct `BOOK_TYPE_CODE` in the REF workbook with its row count (the header cell is not a code)

Health centres, seed schools, ministries and hospitals are rows in one workbook, not separate files. Keep header filters, a frozen header row and column widths. On the Read Me sheet, record the guideline sections used, every derivation rule applied with the number of rows it touched, and, for any sample-header column left blank on every row, the reason it did not apply.

## Stage 1. SK register from `raw-data-grouped`

Build one shared register. Columns follow the health-centre and seed-school templates:

Equipment/Item, Department, Asset Number, Item Description, Life in Months, Tag Number (engrave no.), Date Of Purchase, Date Placed In Service, Recoverable cost, Cost, Acc Dep Cost, Net Book Value, Ytd Deprn, Equipment status, Remarks, Local Government, Facility, Facility type, Unit, Source file, Source location.

### Which files to read

Read `.xls`, `.xlsx`, and `.docx` under `raw-data-grouped`.

Leave out `_multi-team/programme-documents`, except `data-management-chat` and the central-government sources named below. Leave out `_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams` (later copies of the team returns and programme supply lists) except the hospital and inspectorate rows of its consolidated MDA status register named below, and leave out `_multi-team/teams-10-15/pdf-to-excel` (distribution lists). Skip lock files (`~$`). Skip photographs, narrative reports, and reconciliation lists. A Word or Excel file is an asset source only when it has an asset table (an Equipment/Item header, or a description column together with condition, quantity, tag, or cost).

In one folder, if the same file stem exists as both a spreadsheet and a Word file, keep the spreadsheet. Drop exact byte-for-byte duplicates. A workbook whose lines are all (98 percent or more) in another workbook is a re-saved copy and is read once, the copy filed under the facility folder being the one read; a file whose name is filed both under a facility folder and at team level (`_team-documents`) is one return saved twice, and the facility-filed copy is read. Skip draft sheets named like `Table 1` or `Sheet 1` when that workbook already has a consolidated sheet with local-government and facility columns. A team-wide or district-wide register contributes only the rows that name a UgIFT health centre or seed school; district offices, sub-counties, primary schools and water schemes are outside this register.

### Central government

Ministries, agencies and Uganda Blood Transfusion Services keep their UgIFT assets on their own votes and stay on the register. The Hoima, Arua and Soroti regional blood banks stay. Referral hospitals are left out, with Kampala Capital City Authority and the Ministry of Defence and Veteran Affairs. A general hospital held by a district stays on that district's vote. Read, by name:

- `_multi-team/programme-documents/MDA status register.xlsx`: the ministries' verification returns, one toolkit-layout sheet per MDA (MoH, MAAIF, MoWT, MoFPED, OPM, MoGLSD, MoLG, NEMA, PPDA, OAG, MoWE). The vote is the MDA column, else the sheet's MDA. A vehicle a ministry handed to a district is that district's asset, kept at its headquarters.
- `_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/*.xls`: the programme's fixed-asset registers (vehicles, motorcycles, ICT, furniture, software). The vote is the ministry the Location column or the section label names, else MoFPED, the register's owner. A row located at a local government office is that government's asset and outside this register.
- `Ugift  Inventory collection HOIMA blood bank.xlsx` and `Ugift Arua bb chemmart inventory.xlsx` in the same folder: the Hoima and Arua regional blood banks, vote Uganda Blood Transfusion Services. They stay.
- `UGiFT-WIP-consolidated-MDA-status-register.xlsx` in the Karamoja report folder: the MoES inspection tablets held at district inspectorates, a general hospital held on a district vote, and blood-bank rows. Referral hospitals and national referral hospitals are left out. Its local-government facility rows (field returns already read from the team folders, and programme supply lists), its ministry ICT rows (read from the registers above) and its total lines are left out. Soroti Regional Blood Bank stays on the Soroti vote.

A central vote's code and vote form come from `Location(3)2.xlsx`: MOFPED, MOH, MOES, MOLG, MOLHUD, MGLSD, MAAIF, MOWE, MOWT, NEMA, PPDA, OAG, OPM, UBTS. KCCA, MODV and the referral hospitals (ARUA RRH, MULAGO NRH, BUTABIKA NRMH, NAGURU RH, ENTEBBE RH, KAWEMPE RH, KIRUDDU RH and the other regional referral hospitals) are recognised and left out. The site (Finance Building, Embassy House, a district inspectorate or a blood bank) is the Facility; Facility type is MDA, Hospital or Blood bank. A general hospital on a district vote keeps Facility type Hospital.

### Empty or unclear fields

When a cell is empty or the wording is unclear, do not guess and do not stop at the first file. Open every file and subfolder for that facility under `raw-data-grouped/`. Photographs, narrative reports, and reconciliation lists do not add a new asset row. They may fill a date, cost, tag, serial, model, quantity, or status that the asset table left empty or unclear.

A fact another statement of the same line records fills the empty cell, and nothing is guessed:

1. When the same line appears in two returns of one facility, the kept line takes a life, date, cost, accumulated depreciation, net book value, year-to-date depreciation, department or description the folded line states. A money figure is taken only from a statement that counted the same number of units.
2. After the quantity split, the rows of one item at one facility take a fact that every stating row of that item agrees on. A money figure is copied only from a return that priced every unit of the item, or from at least two rows, so one line total is never spread over the units of another line.
3. The two template workbooks in `new-templates-to-follow/` supply a fact for a facility already on the register in the same way, and never a new row. Do not add a sample facility from a template banner as a new asset.

Where a fact comes from another file, list that file after the row's own file in `Source file`. Do not describe a borrowed cost, life, or date there.

Facility and local government come from the row, then from a banner on the sheet, then from the folder path `team-NN/<Local government>/<Facility>/`, then from the reconciliation's link between the file and one facility of that kind. The vote the source states stands: a facility is moved to another government only when the reconciliation lists it, by its exact name, under one other government (a district carried onto the wrong block of a consolidation sheet), never on a fuzzy name match (Kaukura is not Kakure) and never into the sibling vote of the same name (Lira City is not folded into Lira). A supervisor's ruling in `supervisor-decisions.csv` that a facility is in another district or local government (`District corrected`, `Local government corrected`) decides over the label on the return.

### Union per facility

A facility may have been submitted more than once. Treat two returns as the same facility when the normalised local government and facility name match.

Keep every distinct item. When the same line appears in more than one return, keep it once, from the return with the larger stated count. A line that appears in only one return is kept. Identity is the engraved tag plus item name when a real tag exists. Otherwise identity is item name, description, status, and department. Ignore a tag that is blank, `N/A`, `none`, `nil`, or `not engraved`. Ignore a trailing count or a quantity in brackets when comparing item names (`Desks 120` and `Desks` are the same item).

These matching rules reconcile repeated submissions of the same assets; they do not make each item name or combination of field values a single asset. Preserve the full number of physical units from the kept return, including identical source rows, and expand every retained grouped line by its quantity. Never deduplicate the resulting unit rows in SK, MF or REF.

### One row per physical asset

Each retained source line representing N physical assets must produce exactly N rows, with one asset on each row. `Unit` is `item 1 of N`, `item 2 of N`, and so on through `item N of N`. A line that is already one item stays one row. Identical units listed one per row are one row each, and rows are never merged within a return. Duplicate-looking entries are required when they represent separate physical assets; do not remove them because their names, descriptions, tags, costs, departments or other values match.

For example, a single source row for a BP machine with a quantity of 120 must become **120 separate asset rows** in each register, even if all 120 rows share the same source details. This applies to `Quantity: 120`, `BP machines (120)`, `BP machines 120`, `120 BP machines`, or `120 units` in the description or any other column. Set `Unit` from `item 1 of 120` through `item 120 of 120`; `FIXED_ASSETS_UNITS` is 1 on every MF and REF row.

Read the entire source row for a stated count, regardless of the column heading. Accept any explicitly stated positive whole-number quantity, with no upper limit and no restriction to particular asset types. Sources of a count include:

- a quantity column
- a number in brackets on the item name, such as `B.P. Machine, Digital(2)`
- a trailing count on the item name, such as `Examination Couch 2` or `School desks 120`
- a bare integer in Asset Number, when that is the only line for that item and the tag is blank or not engraved, such as 286 office chairs
- a bare integer, or a leading count, in the description or Asset Number, such as `2 microscopes, white`
- a bare count in the item cell beside a blank tag when the description names the asset (`10 | Bed, Adult Patient with Mattress`)
- a count written in status or remarks, such as `116 verified as good then 4 damaged`, `39 desks were supplied`, or `2 functional and one in the store`
- an explicit count in any other column, including a count written in words

Count the same quantity stated in several cells only once. Add counts for separate subsets of the same group, such as 116 good plus 4 damaged = 120 assets, without adding a separately stated group total again. If the counts conflict or a number's meaning is unclear, reread the source and related facility files before deciding; do not silently reduce a stated quantity to one row.

Do not treat these as quantities:

- model numbers, such as LaserJet 1320 or Laptop 840, or model references for EliteBook, ProBook or Latitude; distinguish a model number from an explicitly stated count
- a measure: `15 inch`, `20 liters`, `24 port`, `3 seater`, `2 stance`
- a calendar year, date, monetary amount, serial number or asset identifier; a number's size alone does not make it a year, identifier or invalid quantity
- a bare Asset Number on a row with a real engraved tag, unless the source explicitly identifies that value as a quantity
- a group total repeated on rows that the source already lists one per physical unit. Do not expand an already expanded group a second time. Confirm this from the source layout or unit-level records; matching text or the number of repeated rows alone is not enough to discard a line's stated quantity. Repeated grouped lines each retain their own quantity, even when their descriptions and quantities are identical. For example, `Solid flush doors` 14, 7 and 6 per building block produce 27 rows in total.

When Asset Number or the description was only the count, clear that field on the exploded rows. When a phrase such as `2 microscopes, white` was the count, keep `microscopes, white` as the description. Where the grouped line has one numeric cost, recoverable cost, accumulated depreciation, net book value, or year-to-date depreciation, treat it as the line total and divide it by the quantity so each row holds its share. A unit price is not divided.

A line whose item cell holds only a number or a placeholder, and whose description names nothing, is a count or an unedited template line and names no asset: leave it out. Where the description names the asset, the description becomes the item name.

## Stage 2. MF register from the SK workbook

Copy `Sample Header of Asset Register..xlsx` headers into columns A to BL (64 columns), with the fifteen `ATTRIBUTE` headers renamed to carry the SK column they hold: `ATTRIBUTE1(Equipment/ Item)`, `ATTRIBUTE2(Department)`, `ATTRIBUTE3(Asset Number)`, `ATTRIBUTE4(Item Description)`, `ATTRIBUTE5(Life in Months)`, `ATTRIBUTE6(Tag Number (engrave no.))`, `ATTRIBUTE7(Date Of Purchase)`, `ATTRIBUTE8(Date Placed In Service)`, `ATTRIBUTE9(Recoverable cost)`, `ATTRIBUTE10(Cost)`, `ATTRIBUTE11(Acc Dep Cost)`, `ATTRIBUTE12(Net Book Value)`, `ATTRIBUTE13(Ytd Deprn)`, `ATTRIBUTE14(Equipment status)`, `ATTRIBUTE15(Remarks)`. Fill each SK row into one MF row, in SK order. Do not change the SK workbook. After the mapping below, apply the guidelines to every column they cover.

Map an SK column into A to AW only when the sample header and the 2023 guidelines give that column a meaning the source can fill:

| SK column                             | MF column                                                         | Rule                                                                                                                                                                                                |
| ------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Local Government                      | BOOK_TYPE_CODE                                                    | Strip district wording, keep MC or City, append ` BK`. Example: `MADI OKOLLO BK`. A ministry, agency or blood bank is its `Location(3)2.xlsx` code plus ` BK`: `MOFPED BK`, `UBTS BK`. Referral-hospital codes are left out. |
| Local Government                      | LOCATION_SEGMENT1                                                 | Vote form as `Location(3)2.xlsx` spells the vote, so the row loads in IFMS: `MADI\-OKOLLO DLG`, `BUSIA MC`, `HOIMA CC`, `MOFPED`; the master's `BULISA DLG`, `LUWERO DLG`, `KASANDA DLG`, `NTUNGUMO DLG`, `NAKAPIRIPIRI DLG` and `KIRA MC` are kept where they differ from the gazetted spelling used in `BOOK_TYPE_CODE`. |
| Equipment/Item, else Item Description | DESCRIPTION                                                       | If Unit is set, append it: `Desks [item 1 of 100]`.                                                                                                                                                |
| Department                            | LOCATION_SEGMENT2                                                 | Upper case, one spelling. A count typed after a department (`OPD 02; MATERNITY 01`) is dropped; a facility name or a category word (`FURNITURE`, `ALL`) typed in the cell names no department. Where the source names no department, the department of the vote a facility of that kind belongs to: `HEALTH` for a health centre, `EDUCATION` for a seed school, `HOSPITAL SERVICES` for a hospital, `ADMINISTRATION AND MANAGEMENT` for a local government office, `UNSPECIFIED` for a ministry or blood bank. |
| Facility                              | LOCATION_SEGMENT3                                                 | A ministry site, hospital, blood bank or local government office keeps its own name; a ministry row with no site named takes `UNSPECIFIED`.                                                    |
| Cost, after the per-item division     | FIXED_ASSETS_COST                                                 | Only the amount written on the source.                                                                                                                                                              |
| Date Placed In Service                | DATE_PLACED_IN_SERVICE                                            | Only a date the source states.                                                                                                                                                                      |
| Acc Dep Cost                          | DEPRN_RESERVE                                                     | Only the amount written on the source.                                                                                                                                                              |
| Ytd Deprn                             | YTD_DEPRN                                                         | Only the amount written on the source.                                                                                                                                                              |
| Asset Number                          | ASSET_NUMBER                                                      | Blank when that cell was the quantity. Where the source stated no number, the register's own reference `UGIFT-<SK row number>`, so every row can be cited; it is not an IFMS asset number.  |
| Tag Number                            | TAG_NUMBER                                                        | A real engraved number as written. A blank tag, or any placeholder for one (`Not engraved`, `Nor engraved`, `Not`, `N/A`, wording within two letters of `not engraved`), is `Not engraved`.  |
| Life in Months, when 12 or more       | LIFE_IN_MONTHS, DEPRECIATE_FLAG `YES`, DEPRN_METHOD_CODE `STL` | Section 5.5: straight line. `7 yrs` reads as 84 months. A stated life under 12 months is unclear wording (a non-current asset serves beyond one year, 3.2.1.2): the class life applies and the stated figure stays in ATTRIBUTE5 on the MF workbook. |
| Equipment status                      | IN_USE_FLAG                                                       | `YES` for Functional and `NO` for Faulty, never blank (see Condition below).                                                                                                                       |

`FIXED_ASSETS_UNITS` is 1 on every row. `LOCATION_SEGMENT4` is `UNSPECIFIED` on every row, the fourth segment of every location combination in `Location(3)2.xlsx` and of the sample row. `ASSET_EXP_ACCT_FUND` is `01` on every row, the fund segment the sample row carries (the Consolidated Fund). `PRORATE_CONVENTION_CODE` is `GOU PRO CO` on every row: section 3.3.5.2 states that depreciation begins on the first day of the month the asset is available for use, the sample row codes that convention, and the book applies one convention. `SALVAGE_VALUE` is 0 on every row (section 5.7). `ASSET_CATEGORY_MINOR3` is the item name, the item-master level below Annex 1 (its footnote 5), as the sample row writes it (`Laptop` for `HP Laptop silver`).

The ATTRIBUTE columns carry the SK columns in order. On the MF workbook they hold the source values as sanitized, except that `ATTRIBUTE2(Department)` holds the department written to LOCATION_SEGMENT2, `ATTRIBUTE3(Asset Number)` the number or register reference written to ASSET_NUMBER, `ATTRIBUTE4(Item Description)` the field description trimmed to one spacing with a capital first letter (empty where the cell held only a count, a unit word or a placeholder), `ATTRIBUTE5(Life in Months)` the source life as a number, `ATTRIBUTE6` the tag as TAG_NUMBER writes it, `ATTRIBUTE7(Date Of Purchase)` the date as yyyy-mm-dd, or a year or financial year the source wrote, and nothing where the wording could not be read as a date, `ATTRIBUTE8(Date Placed In Service)` the source date and nothing where it wrote words, `ATTRIBUTE14(Equipment status)` the condition, and `ATTRIBUTE15(Remarks)` what the field recorded and nothing else: the source Remarks, the status wording moved out of Equipment status (`Source status`), words typed into an amount column under that column's name, wording in the tag cell beyond a placeholder (`Engraving`), and the SK fields with no column in A to BL, each labelled with its source column name (`Facility type`, `Source file`, `Source location`; the file path keeps its spelling on disk). Nothing in Remarks is written by the register itself, and it never says a cost, life or date was borrowed.

Fill an expense-account or clearing-account segment only when the guidelines or the sample row state that segment: account 221012 for small office equipment and loose tools, the Annex 2 depreciation expense account of the class (2312xx, 2311xx) for a capitalized asset, and clearing account 513001 on every CAPITALIZED or CIP row (the account the guidelines credit when an asset is brought into the register, 3.2.2 illustration). Leave `ASSET_KEY_SEGMENT1`, `EMPLOYEE_NUMBER`, `AMORTIZATION_START_DATE`, and `AMORTIZE_NBV_FLAG` blank unless the guidelines or the source state them. Recoverable cost is not salvage value. The guidelines use salvage as the residual in a class life, and recoverable amount as an impairment test.

### Columns the SK workbook does not provide

Open the 2023 guidelines and fill only what they decide.

**Classification.** Set ASSET_CATEGORY_MAJOR, ASSET_CATEGORY_MINOR1, and ASSET_CATEGORY_MINOR2 from the asset description, using the classes in the guidelines and Annex 1, reading the field's spellings (`cap boards` are cupboards, `lap top` a laptop, `staff quaters` staff quarters, `sterilization drum` a medical appliance, `LAN` an ICT network line, a motorcycle a cycle, a pick-up a light vehicle). Leave all three blank when the name is generic (`equipment`, `item`, `set`, `machine`) or is a total, a count, a service, or a consumable pack. Do not guess a class from the facility type alone.

**Useful life and depreciation.** LIFE_IN_MONTHS is never blank: the source life where stated and 12 months or more; else the Annex 1 life of the class (ICT and other equipment 60 months; land 600 months although it does not depreciate); else, for an asset Annex 1 does not class, the guidelines' general equipment life of 60 months; 0 on a line that is no non-current asset (a total, a repair, a service, a consumable, a loose tool). DEPRECIATE_FLAG is `YES` with DEPRN_METHOD_CODE `STL` where a life applies and `NO` on every other row: land (5.14), work in progress and operating leases (5.5), and lines that are no asset. Section 5.7: residual value is nil, so SALVAGE_VALUE is 0 on every row. If the source already recorded a residual, keep it.

**Serial, model, manufacturer.** Fill SERIAL_NUMBER, MODEL_NUMBER, or MANUFACTURER_NAME only when the description states one explicit value (`serial`, `s/n`, `model`, `made by`). A product name such as LaserJet 1320 may be the model; do not also treat it as a quantity.

### Which assets are capitalized

The guidelines set no capitalization threshold (3.2.2.1): every non-current asset is capitalized whatever its value, and similar low-value units acquired in one transaction (desks, laboratory stools, surgical instruments, computers in a laboratory) are a group asset (3.3.5) whose subsidiary records are the unit rows of this register.

Set ASSET_TYPE to `CAPITALIZED` only when every condition in section 3.2.1 holds:

1. The vote or facility controls the asset: it can use it, benefit from it, charge for it, or deny its use to others. An asset held for the facility at its district store is controlled by the vote.
2. Future economic benefits or service potential are expected, with at least a 50 percent chance, and the benefit lasts more than one year (section 3.2.1.2). That is the non-current-asset test. There is no monetary capitalization threshold.
3. The asset exists because of a past purchase, transfer, donation, or verified delivery. An intention to buy is not an asset. A line marked not received, not delivered, missing, lost, stolen, disposed of, written off or condemned does not exist, nor does one the verification team could not see, find or verify. A remark about another item, or about part of a group (`18 were stolen, 10 in use`, `not lost`), does not deny the row.
4. Cost can be measured from the source line or, later, from a borrowed comparable price on the REF workbook. If no cost can be measured, leave ASSET_TYPE blank.

Do not capitalize, and leave ASSET_TYPE blank, when section 3.3.3 applies. Small office equipment and loose tools are expensed on account 221012 and treated as inventories, whatever their value. The guidelines name kettles, spoons, forks, calculators, stapling machines, pen-holders, punches, paper trays, pin and staple holders, and typewriters, and items of the same nature follow them: cutlery and kitchen ware, clocks and stop watches, scissors, spatulas, rulers, measuring and MUAC tapes, buckets, bins, mops, hand tools, keyboards, mice, cables, chargers, surge protectors, penguin suckers. These carry no class, life or depreciation. Also leave ASSET_TYPE blank for single-use packs, graph paper, laboratory glassware and other consumables, and for a service or subscription (internet connectivity for a period, engraving, testing and commissioning, installation as a line of its own), which is not a controlled resource with service potential beyond a year (3.2.1.2).

Section 3.3.5 allows a vote to capitalize a group of similar low-value units as one group asset, with subsidiary records for each unit. This register is that subsidiary record. Keep one row per physical asset. Mark each of those rows `CAPITALIZED` when the conditions above hold. Do not collapse 100 desks back into one row.

A repair or spare that only restores the asset is not a new capitalized asset (section 3.2.3). A major replacement that extends life or service potential is added to the existing asset, not entered as a second asset, unless the source listed it as its own asset.

Land is capitalized and is not depreciated. Natural resources are not capitalized (3.2.1.4). A building the source says is still under construction is work in progress: ASSET_TYPE `CIP` at the cost the source states, not depreciated (5.5, 5.14), with no placed-in-service date or price borrowed for it.

## Sanitize the MF and REF workbooks

Sanitize `ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx` after Stage 2. Copy that sanitized workbook to `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`, then apply the same rules again so a borrowed-cost edit cannot put raw source wording back. Do not change a recorded cost, life, or depreciation figure while sanitizing. Keep the `[item 1 of 100]` suffix.

Preserve every individual asset row during mapping, sanitizing, borrowing and calculation. Never group, merge or remove rows because their cleaned values are identical. Each SK asset row must remain one MF row and one REF row.

**Every column.** Sanitize every filled cell in MF and again in REF. Trim text, collapse repeated spaces, and remove line breaks (a file path after `Source file:` keeps its spelling on disk). Use one spelling for the same fact on every row. Clear a cell whose whole value is a placeholder (`N/A`, `NA`, `nil`, `nill`, `none`, `null`, `-`, `not applicable`); `UNSPECIFIED` in a location segment is the master's own value, not a placeholder. Do not clear a real engraved tag. Do not change a recorded amount while cleaning text.

**BOOK_TYPE_CODE.** This column is cleaned on every row. One local government has one code. Uppercase. Remove `District`, `Local Government`, `DLG`, and backslashes. Turn a hyphen into a space. Keep `MC` or `CITY` where that is the vote. Append ` BK`. Examples: `Hoima District` becomes `HOIMA BK`; `Madi-Okollo` becomes `MADI OKOLLO BK`; `Kiira Municipal Council` becomes `KIIRA MC BK`. Drop a number that sits immediately before `BK`: `AGAGO 2 BK` becomes `AGAGO BK`. Do not leave a raw district name in this column. `LOCATION_SEGMENT1` is the same government in the vote form `Location(3)2.xlsx` spells, such as `MADI\-OKOLLO DLG`.

**Facility name** (`LOCATION_SEGMENT3`). A school ends with `Seed Secondary School`. A health centre ends with `Health Centre III`, including a master Health Centre II that was upgraded. Spell the words in full. Do not write `HCII`, `HC III`, `H/C`, `H.C`, or `Health Center`. Do not add the suffix twice. Keep a longer official name that already contains those words, such as `St Mugagga Vocational Seed Secondary School`. A hospital, blood bank, ministry site or local government office keeps its own name.

**Facility type.** Where the facility type is written, it is `School`, `Health centre`, `MDA`, `Hospital`, `Blood bank` or `Local government office`.

**Condition.** Equipment status is `Functional` or `Faulty` on every row. `Functional` covers in use (also `in use but in poor condition`), functioning, working well, available, verified, good condition and new. `Faulty` covers damaged, broken, not in use, not functioning, in store (not in use), not received, not seen, obsolete, unserviceable, disposed, lost, and missing. Words run together or dashed in the source (`goodandfunctional`, `non - functional`) are read as the words they spell. Where the status cell is empty the Remarks decide; where the wording splits the group the larger stated count decides; an asset the team recorded with no condition anywhere is taken as `Functional`. Move any longer status wording into Remarks. Set `IN_USE_FLAG` to `YES` for Functional and `NO` for Faulty.

**Tag.** A blank tag, or a placeholder tag, is `Not engraved`. Keep a real engraved number as written. Wording in the tag cell beyond a placeholder goes to Remarks as `Engraving`.

**Amounts.** Show cost, depreciation, reserve, recoverable amount and net book value with thousands separators and a nil amount as `-` (format `#,##0.##;-#,##0.##;"-"`). Do not recalculate them in this step.

## Stage 3. REF workbook: borrowed purchase costs

Start from the sanitized MF workbook. Then fill missing purchase costs. Do not change a price that is already recorded unless it is wrongly priced (below). After borrowing, the facility name, facility type, status, and tag rules above still hold.

Existing purchase prices keep a **white** background.

Borrow only for a specific asset name. Do not borrow for a generic name such as equipment, furniture, medical equipment, item, set, machine, buildings, or land. Compare assets with the same normalised name, matched in the singular (`Desks` borrow from `Desk`). Where both rows have an asset class, the class must match. The borrowed price is the median of the matching prices, in Uganda shillings.

Search in this order:

1. **Same local government.** Use assets purchased in the same year. If none, use the closest year. Colour the cost cell **blue** (`#9DC3E6`).
2. **Other local governments.** Use the same year, or the nearest period. Colour the cost cell **orange** (`#F4B183`).
3. **The whole workbook.** Use this only when steps 1 and 2 find no price. Colour the cost cell **green** (`#C6EFCE`).
4. **The Annex 1 class.** Where no asset of the same name carries a price anywhere, the median price of the class, same local government (blue) then other local governments (orange).

**Wrongly priced items.** Use the workbook's own prices to find them. A stated price more than twenty times above or below the median stated price of that name across the workbook (three or more prices) is a block total typed on one unit, a divided line total, or a slip; where the name has fewer than three prices, a price fifty times above or below the median of its Annex 1 class is treated the same way. Such a price is left out of the donors, and on a row it is replaced by the borrowed unit price in the search order above, coloured; the recorded figure stays in `ATTRIBUTE10(Cost)` on the MF workbook.

**Immaterial costs.** A unit cost under UGX 10,000, stated or borrowed, is carried at 0, which the amount format shows as `-`; such a row is not capitalized and carries no depreciation. A line that is no asset (a total, a repair, a service, a consumable, a loose tool), and works with no cost stated, carry 0. An asset with neither a priced namesake nor a priced class remains without a cost, and the Read Me counts these rows.

Do not write a borrowed price or a borrowed life in Remarks, or in `ATTRIBUTE15(Remarks)`. That column must never say the cost or life came from another asset, local government, year, or median. The cell colour on the cost or life is the only marker. A life already on the row stays white and unchanged.

A missing useful life may be borrowed in the same order and with the same colours. Use the most common life of the matching assets, and only where life is at least 12 months and the asset is not marked out of use.

### Calculated columns

On `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`, calculate every row. The calculated columns are `FIXED_ASSETS_COST` (only when the source cost is missing or wrongly priced), `SALVAGE_VALUE`, `LIFE_IN_MONTHS` (when the source life is missing), `DEPRECIATE_FLAG`, `DEPRN_METHOD_CODE`, `PRORATE_CONVENTION_CODE`, `DATE_PLACED_IN_SERVICE` (when the source date is missing), `DEPRN_RESERVE`, and `YTD_DEPRN`. There is no net-book-value column in A to AW. Net book value is the check: cost minus `DEPRN_RESERVE`, never below `SALVAGE_VALUE`; it is written in `ATTRIBUTE12(Net Book Value)` where the source states none.

Treat an empty date the way an empty cost is treated. Finish `DATE_PLACED_IN_SERVICE` before you close the cost and depreciation columns. Read the purchase date and the placed-in-service date from the source scan above. If the placed-in-service date is empty, use the purchase date on the same row (the asset was available for use from its purchase), else the first month of the year, or 1 July of the financial year, the row states (white). If the row states no date at all, borrow the placed-in-service month in the same order and with the same colours as a borrowed cost (same asset name; same year, else the nearest year, taking the most common month), and where no asset of the same name carries a date, the month the other assets of the same facility were placed in service (blue), else of the same government (blue), else the whole workbook's most common month (green). Work in progress keeps no placed-in-service date. A borrowed date is marked only by that cell colour. Do not describe the borrowed date in Remarks or in `ATTRIBUTE15`.

Then calculate straight-line depreciation to 30 September 2026 for every depreciable row that exists and whose cost, life and placed-in-service month are known, whether in use or not (an idle asset still consumes its life). Section 5.7: residual value is nil, so `SALVAGE_VALUE` is 0 unless the source recorded a residual. Monthly charge = (`FIXED_ASSETS_COST` minus `SALVAGE_VALUE`) / `LIFE_IN_MONTHS`. `DEPRN_RESERVE` runs from the placed-in-service month through September 2026 and stops at the end of useful life. `YTD_DEPRN` is the July to September 2026 portion of that charge; against a reserve the source recorded, it cannot exceed the depreciation still to be charged. Keep a source cost, and keep a source depreciation figure when that cell is already filled (even where it exceeds the cost; the net book value then shows the residual). Calculate every calculated cell that is blank. Where there is nothing to charge (no depreciation, no cost, or an asset that does not exist) `DEPRN_RESERVE` and `YTD_DEPRN` are 0.

Do not skip a cost or a depreciation amount because the date cell started empty. Finish the date first, then the cost, then the depreciation. Leave a non-calculated column empty only after the source scan and the guidelines still give it nothing to write.

After a borrowed cost makes measurement possible, set ASSET_TYPE to `CAPITALIZED` if the Stage 2 tests are met and the row is not small office equipment or a loose tool.

### Columns that are not blank on the REF workbook

These columns hold a value on every REF row, the derivation being the rule named: `FIXED_ASSETS_COST` (stated, borrowed, or 0; except an asset with no comparable at all), `ASSET_EXP_ACCT_FUND` (01), `DATE_PLACED_IN_SERVICE` (except work in progress), `DEPRECIATE_FLAG`, `LIFE_IN_MONTHS`, `PRORATE_CONVENTION_CODE`, `DEPRN_RESERVE`, `YTD_DEPRN`, `SALVAGE_VALUE`, `TAG_NUMBER`, `IN_USE_FLAG`, `ATTRIBUTE1(Equipment/ Item)`, `ATTRIBUTE2(Department)`, `ATTRIBUTE3(Asset Number)`, `ATTRIBUTE9(Recoverable cost)` (the amount the source states, else the carrying amount, cost less `DEPRN_RESERVE`, since no impairment was recorded), `ATTRIBUTE10(Cost)`, `ATTRIBUTE11(Acc Dep Cost)`, `ATTRIBUTE12(Net Book Value)`, `ATTRIBUTE13(Ytd Deprn)`, `ATTRIBUTE14(Equipment status)`, `ATTRIBUTE15(Remarks)`. On the REF workbook `ATTRIBUTE5`, `ATTRIBUTE8`, `ATTRIBUTE10`, `ATTRIBUTE11`, `ATTRIBUTE12` and `ATTRIBUTE13` show the finished value, the same as the main column, with the same cell colour. `ATTRIBUTE4(Item Description)`, `ATTRIBUTE7(Date Of Purchase)` and, on the MF workbook, `ATTRIBUTE8` stay blank where the field gave nothing readable.

## Checks before the registers are final

Reconcile each retained source line's physical-asset count to its generated rows. A BP-machine line with a stated quantity of 120 must have exactly 120 rows in SK, MF and REF, with `Unit` covering `item 1 of 120` through `item 120 of 120` and `FIXED_ASSETS_UNITS` equal to 1 on every MF and REF row. Verify quantities found outside the quantity column, quantities above 500, repeated identical grouped lines and existing one-per-unit rows. Confirm that duplicate-looking unit rows survive every stage, no group is expanded twice, and the per-unit amounts sum to the original line totals after expansion. Record these checks on the Read Me.

Run a rule check over the full MF and REF workbooks and record the outcome on the Read Me: 64 headers in sample order; a frozen header row and filter; every `BOOK_TYPE_CODE` a real vote spelt one way; `LOCATION_SEGMENT3` names ending as the facility rule requires; `ATTRIBUTE14` only Functional or Faulty, matching `IN_USE_FLAG`; no placeholder or double-spaced text; every depreciable row with method, prorate convention and salvage; depreciation recomputed on a sample; borrowed cells coloured and never described in Remarks; the not-blank columns filled; the row count equal in SK, MF and REF. Then have independent reviewers read the workbooks against this prompt and the guidelines, and refute each finding before acting on it.
