# Prompt: correct supplied BOOK_TYPE_CODE values

Correct `BOOK_TYPE_CODE` in `outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx` for the codes supplied in the request. A supplied code is the exact cell text, including spaces. `outputs/asset-register/README.md#book_type_code` is only an index of those texts. Do not correct a code that was not supplied.

Read these before changing a cell:

- `GOU Asset Accounting Policies and Guidelines 2023.pdf`, sections 1.3, 1.5, 1.6, 3.2.1.3, 3.7.1, 3.7.2, and 3.8.1 to 3.8.2
- `outputs/PROMPT_POPULATE_ASSET_REGISTERS.md`, the `BOOK_TYPE_CODE` and `LOCATION_SEGMENT1` rules
- `raw-data-grouped/facility-reconciliation.csv` (`lg`, `master_lg`, `folder`, `source`)

The guidelines do not define the letters `BK`. They decide which vote the register belongs to. Sections 1.3, 1.5, and 1.6: the Accounting Officer records the assets of that vote, and the guidelines apply to ministries, agencies, departments, and local governments. Section 3.2.1.3: control is the vote that can use the asset, benefit from it, charge for it, or deny its use. Sections 3.7 and 3.8: that vote keeps the asset register and enters its assets in its own Fixed Assets Module. For a facility return, that vote is the local government named by the source, not the facility, a cost, a condition, or an item name.

## Which rows

On the Asset Register sheet, select every row whose `BOOK_TYPE_CODE` equals the supplied text. Update every selected row that a source can place. Leave a row unchanged when its source cannot be read, and list it.

One supplied text can come from more than one local government. A cost, a count, a condition, an item name, a region, or the header `BOOK_TYPE_CODE` is not evidence of a government. Trace each distinct source. Where every traced row belongs to one local government, write that code on all of them. Where they belong to more than one, write each row from its own source. Do not give the whole set one government.

## Trace

Read `ATTRIBUTE15` on the selected rows. It carries `Source file:` and `Source location:`. Open that file under `raw-data-grouped/`. Do not edit it.

Take the local government in this order, and stop at the first one that names a vote:

1. The local-government cell on the source row named by `Source location`.
2. A local-government banner on that sheet.
3. The folder `team-NN/<Local government>/<Facility>/` that holds the file.
4. `facility-reconciliation.csv`, matched on that folder or source path. Use `master_lg` when it is filled, otherwise `lg`.
5. When the source names a facility, match that name to a folder `team-NN/<Local government>/<Facility>/` or to `facility-reconciliation.csv` on `name` or `field_name`. The vote is the local government in that path. Use `master_lg` when it is filled, otherwise `lg`.

Ignore the supplied `BOOK_TYPE_CODE` as evidence. Do not write a facility name, a department, a cost, a quantity, a condition, or the words Central, Eastern, Northern, Western, District, and Municipality standing alone as the vote. A facility name is used only to find the folder that holds the vote. A city and a municipal council are their own votes: do not fold `Fort Portal City` into Kabarole, or a municipal council into its parent district. A ministry name in the bad cell does not move a facility filed under a local government onto that ministry. Use a ministry book only when the source file is a ministry return and no local government controls the asset.

Spell the government from the folder or from `master_lg` / `lg`. Do not pick a nearby code already in the workbook because the letters look alike.

## Write the code

Change only `BOOK_TYPE_CODE` and, on those same rows, `LOCATION_SEGMENT1`, so both name the government just traced. Leave every other column as it is. Do not change the SK workbook, the MF workbook, or a source file.

`BOOK_TYPE_CODE`: uppercase. Remove `District`, `Local Government`, `DLG`, and backslashes. Turn a hyphen into a space. Keep `MC` or `CITY` where that is the vote. Drop a number that sits immediately before `BK`. Append ` BK`. Examples: `Hoima District` becomes `HOIMA BK`; `Madi-Okollo` becomes `MADI OKOLLO BK`; `Kiira Municipal Council` becomes `KIIRA MC BK`.

`LOCATION_SEGMENT1` is that same government in vote form: a district ends in `DLG`, a municipal council in `MC`, a city in `CITY`. A hyphen inside the name is written `\-`, as in `MADI\-OKOLLO DLG`.

If the trace confirms the code already on the row, leave the cell unchanged.

Keep the header filter and the frozen header row. On the Read Me sheet, add one line per supplied code: the text supplied, the number of rows, the government written, the guideline sections used, and the count of rows left unchanged because the source could not be read.
