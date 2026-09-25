# Prompt: update grouped facility returns

Update `raw-data-grouped/` from `raw-data-ungrouped/` and `new-raw-data-221092026-1114/`. Do not edit either source. Some grouped files are hard links to raw originals, so write a new copy when you change a return.

## Change tracker

`scripts/track_source_changes.py` watches both source folders. `raw-data-grouped/_change-tracker/snapshot.csv` stores each file’s modified time and size. `raw-data-grouped/_change-tracker/changes.csv` is the only queue.

On the first grouped update, write one `added` row for every file in the snapshot. After that, the script appends `added`, `modified`, or `removed` only when a file’s time or size changes. Run `python scripts/track_source_changes.py --watch` to keep the log current.

Read a file only when `changes.csv` lists it as `added` or `modified` and it has not yet been applied. Open archives, WhatsApp chats, attachments, photographs, and PDF scans that are in that queue, including every page of a queued scan. Skip Office lock files and `ugift-team-10-15/tmp/`.

When a source has been filed, record its modified time and size as applied. Ignore it on the next run unless that time or size changes.

## Where to file

Use `facility-reconciliation.csv`, `supervisor-decisions.csv`, and `team-distributions.docx` to match a submitted name to one master facility in the same local government. Confirmed renames and replacements stay on the existing facility. Do not create a facility the reconciliation says does not exist. A WhatsApp caption, filename, or form heading is enough to place an attachment when it names the facility and local government.

If the team submitted a toolkit or register, copy that file into the facility folder and leave its layout unchanged.

If the only new evidence is a scan, photo, or handwritten PDF, copy `ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx` and fill that copy. Keep its interview questions and its 15-column asset tables: Equipment/Item, Department, Asset Number, Item Description, Life in Months, Tag Number (engrave no.), Date Of Purchase, Date Placed In Service, Recoverable cost, Cost, Acc Dep Cost, Net Book Value, Ytd Deprn, Equipment status, Remarks. Enter only what the image shows. Leave unused template rows blank. Name the copy `<Facility> asset verification.docx` in that facility folder.

## Union

`raw-data-grouped/` holds the union of both source folders. Add a file or fact that is not already there. When the same line was submitted more than once, keep it once, at the larger stated count. Do not drop an item that appears in only one return. Do not file a second copy of a file already present byte for byte. Do not merge these returns into another register.
