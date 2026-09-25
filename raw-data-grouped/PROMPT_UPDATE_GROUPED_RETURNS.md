# Prompt: update grouped facility returns

Update `raw-data-grouped/` from `raw-data-ungrouped/` and `new-raw-data-221092026-1114/`. Do not edit either source. Some grouped files are hard links to raw originals, so write a new copy when you change a return.

## Change tracker

`scripts/track_source_changes.py` watches both source folders. It keeps the last modified time and size of every file in `raw-data-grouped/_change-tracker/snapshot.csv`. Whenever a file is added, modified, or removed, it appends that event to `raw-data-grouped/_change-tracker/changes.csv`. Run `python scripts/track_source_changes.py --watch` so the log updates as files change. The first run only writes the snapshot.

Read a source only when `changes.csv` lists it as added or modified since the last grouped update. Rewrite a facility workbook only when one of its sources is in that list. Change only the rows from those sources, then union them with the rows already in the workbook. Leave every other workbook and row unchanged.

## Scan

Open every file, including nested ZIP and RAR archives, WhatsApp exports (the chat text and every attachment), photographs of forms, and PDF scans. Read each scanned page. Skip Office lock files and `ugift-team-10-15/tmp/`.

Use `facility-reconciliation.csv`, `supervisor-decisions.csv`, and `team-distributions.docx` to match a submitted name to one master facility in the same local government. Confirmed renames and replacements stay on the existing facility. Do not create a facility the reconciliation says does not exist. A WhatsApp caption, filename, or form heading is enough to place an attachment when it names the facility and local government.

## Which form to use

If the team submitted a toolkit or register, file that file and read it. Do not rewrite it into another layout.

If the new evidence is only a scan, photo, or handwritten PDF, copy `ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx` and fill that copy. Keep its interview questions and its 15-column asset tables: Equipment/Item, Department, Asset Number, Item Description, Life in Months, Tag Number (engrave no.), Date Of Purchase, Date Placed In Service, Recoverable cost, Cost, Acc Dep Cost, Net Book Value, Ytd Deprn, Equipment status, Remarks. Enter only what the image shows. Leave unused template rows blank. Name the copy `<Facility> asset verification.docx` in that facility folder.

## Union

`raw-data-grouped/` holds the union of both source folders. Add an asset, file, or fact that is not already there. When the same line was submitted more than once, keep it once, at the larger stated count. Do not drop an item that appears in only one return. Do not file a second copy of a file already present byte for byte.
