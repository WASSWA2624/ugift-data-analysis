# Prompt: update grouped facility returns

Update `raw-data-grouped/` from `raw-data-ungrouped/` and `new-raw-data-221092026-1114/`. Do not edit either source. Some grouped files are hard links to raw originals, so write a new copy when you change a return.

## Change tracker

`scripts/track_source_changes.py` watches both source folders. It keeps the last modified time and size of every file in `raw-data-grouped/_change-tracker/snapshot.csv`. Whenever a file is added, modified, or removed, it appends that event to `raw-data-grouped/_change-tracker/changes.csv`. Run `python scripts/track_source_changes.py --watch` so the log updates as files change. The first run only writes the snapshot.

Read a source only when `changes.csv` lists it as added or modified since the last grouped update. Rewrite a facility workbook only when one of its sources is in that list. Change only the rows from those sources, then union them with the rows already in the workbook. Leave every other workbook and row unchanged.

## Scan

Open every file, including nested ZIP and RAR archives, WhatsApp exports (the chat text and every attachment), photographs of forms, and PDF scans. Read each scanned page. Skip Office lock files and `ugift-team-10-15/tmp/`.

Use `facility-reconciliation.csv`, `supervisor-decisions.csv`, and `team-distributions.docx` to match a submitted name to one master facility in the same local government. Confirmed renames and replacements stay on the existing facility. Do not create a facility the reconciliation says does not exist. A WhatsApp caption, filename, or form heading is enough to place an attachment when it names the facility and local government.

## Union

`raw-data-grouped/` holds the union of both source folders. Add an asset, file, or fact that is not already there. When the same line was submitted more than once, keep it once, at the larger stated count. Do not drop an item that appears in only one return. Do not file a second copy of a file already present byte for byte.

File the facility workbook at:

`team-NN/<Local government>/<Facility>/<Facility> asset register.xlsx`

One workbook per facility. Shared registers, Word toolkits, and scans may remain as evidence. Their asset lines still go into that one workbook.

## Workbook

Row 1 is exactly the header row of `Sample Header of Asset Register..xlsx`, columns A–BL:

BOOK_TYPE_CODE, DESCRIPTION, ASSET_CATEGORY_MAJOR, ASSET_CATEGORY_MINOR1, ASSET_CATEGORY_MINOR2, ASSET_CATEGORY_MINOR3, ASSET_TYPE, FIXED_ASSETS_UNITS, LOCATION_SEGMENT1, LOCATION_SEGMENT2, LOCATION_SEGMENT3, LOCATION_SEGMENT4, FIXED_ASSETS_COST, ASSET_EXP_ACCT_FUND, ASSET_EXP_ACCT_FUND_SOURCE, ASSET_EXP_ACCT_PROGRAMME, ASSET_EXP_ACCT_COST_CENTER, ASSET_EXP_ACCT_PROJECT, ASSET_EXP_ACCT_BUDGET_OUTPUTS, ASSET_EXP_ACCT_SPARE, ASSET_EXP_ACCT_GEO_LOCATION, ASSET_EXP_ACCT_ACCOUNT, ASSET_CLR_ACCT_FUND, ASSET_CLR_ACCT_FUND_SOURCE, ASSET_CLR_ACCT_PROGRAMME, ASSET_CLR_ACCT_COST_CENTER, ASSET_CLR_ACCT_PROJECT, ASSET_CLR_ACCT_BUDGET_OUTPUTS, ASSET_CLR_ACCT_SPARE, ASSET_CLR_ACCT_GEO_LOCATION, ASSET_CLR_ACCT_ACCOUNT, DATE_PLACED_IN_SERVICE, DEPRECIATE_FLAG, DEPRN_METHOD_CODE, LIFE_IN_MONTHS, PRORATE_CONVENTION_CODE, DEPRN_RESERVE, YTD_DEPRN, SALVAGE_VALUE, ASSET_NUMBER, ASSET_KEY_SEGMENT1, TAG_NUMBER, SERIAL_NUMBER, MANUFACTURER_NAME, MODEL_NUMBER, EMPLOYEE_NUMBER, IN_USE_FLAG, AMORTIZATION_START_DATE, AMORTIZE_NBV_FLAG, ATTRIBUTE1, ATTRIBUTE2, ATTRIBUTE3, ATTRIBUTE4, ATTRIBUTE5, ATTRIBUTE6, ATTRIBUTE7, ATTRIBUTE8, ATTRIBUTE9, ATTRIBUTE10, ATTRIBUTE11, ATTRIBUTE12, ATTRIBUTE13, ATTRIBUTE14, ATTRIBUTE15.

One physical asset per row. A source line that states a quantity, in a quantity column, the description, the asset number, or another column, becomes that many rows. `FIXED_ASSETS_UNITS` is 1. Put `item 1 of 100` in ATTRIBUTE1. Divide a single line cost by the quantity. Do not treat a model number (LaserJet 1320, Laptop 840), a measure (`15 inch`), or a year as a quantity. Ignore counts above 500.

Fill only cells the source states. School names end with `Seed Secondary School`. Health centres end with `Health Centre III`. Facility type in ATTRIBUTE2 is `School` or `Health centre`. Status in ATTRIBUTE3 is `Functional` or `Faulty`; put any longer wording in ATTRIBUTE4. A missing tag is `Not Engraved`. Clear a cell whose whole value is `N/A`, `nil`, `none`, or `-`.

Leave the register uncreated when the only evidence is that the facility has no return.
