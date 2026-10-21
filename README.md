# UgIFT data analysis

Source records, reconciliation scripts and asset registers for UgIFT verification.

| Location | Contents |
|---|---|
| `raw-data-grouped/` | Filed source records and facility reconciliation. |
| `raw-data-ungrouped/`, `new-raw-data-221092026-1114/` | Original source deliveries retained for traceability. |
| `new-templates-to-follow/`, `reference/` | Register layouts and accounting reference data. |
| `scripts/`, `tests/` | Register generation, reconciliation and checks. |
| [Current asset registers](outputs/asset-register/README.md) | SK source register, MF mapping and canonical completed REF register, with package status and book-code index. |
| `outputs/asset-register-baseline/` | Earlier register, data dictionary and facility book directory. |
| [Current draft report](outputs/narrative-report/UGIFT-DRAFT-REPORT-21102026.docx) | Sole retained draft report, fully editable, with its historical source log in the same directory. |
| `outputs/report-templates/` | Reference report templates. |
| `tmp/` | Historical review evidence, analysis scripts and pre-review backups. |

Run scripts from the repository root with Python and the required libraries (`openpyxl`, `xlrd` and `python-docx` for the main register pipeline). Close the output workbooks in Excel before regeneration.

```bash
python scripts/merge_shared_asset_registers.py
python scripts/build_guideline_registers.py
python scripts/list_book_codes.py
```

See [register population rules](outputs/PROMPT_POPULATE_ASSET_REGISTERS.md) for source-selection and completion rules, and [the current package README](outputs/asset-register/README.md) for its validation status. Rebuilding replaces generated workbooks; preserve reviewed amendments before running it. Source deliveries and audit evidence must be preserved when removing duplicate or superseded outputs.

The legacy `raw-data-ungrouped/ugift-team-10-15/tmp/` folder retains 48 original photographs and one earlier chat that were not preserved elsewhere. Source intake and change tracking exclude this folder. Obsolete helpers, duplicate extractions, bytecode, older render outputs and completed workbook staging files were removed during the October 2026 cleanup; source documents, reviewer comments, published audits and pre-review backups remain available.
