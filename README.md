# UgIFT data analysis

Source records, reconciliation scripts and asset registers for UgIFT verification.

| Location | Contents |
|---|---|
| `raw-data-grouped/` | Filed source records and facility reconciliation. |
| `raw-data-ungrouped/`, `new-raw-data-221092026-1114/` | Original source deliveries retained for traceability. |
| `new-templates-to-follow/`, `reference/` | Register layouts and accounting reference data. |
| `scripts/`, `tests/` | Register generation, reconciliation and checks. |
| [Current asset register](outputs/asset-register/UGIFT-ASSET-REGISTER-21102026.xlsx) | Sole updated register, with a package guide and consolidated audit archive in the same directory. |
| `outputs/asset-register-baseline/` | Earlier register, data dictionary and facility book directory. |
| [Current draft report](outputs/narrative-report/UGIFT-DRAFT-REPORT-21102026.docx) | Sole retained draft report, fully editable, with its historical source log in the same directory. |
| `outputs/report-templates/` | Reference report templates. |
| `tmp/` | Historical review evidence, analysis scripts and pre-review backups. |

Run the book-code index command from the repository root to update the current register's package guide without editing the workbook:

```bash
python scripts/list_book_codes.py
```

See [the current package README](outputs/asset-register/README.md) for the retained register and audit evidence. Historical build scripts generate an earlier multi-workbook package and do not replay every later reconciliation. Source deliveries and audit evidence are preserved when removing duplicate or superseded outputs.

The legacy `raw-data-ungrouped/ugift-team-10-15/tmp/` folder retains 48 original photographs and one earlier chat that were not preserved elsewhere. Source intake and change tracking exclude this folder. Obsolete helpers, duplicate extractions, bytecode, older render outputs and completed workbook staging files were removed during the October 2026 cleanup; source documents, reviewer comments, published audits and pre-review backups remain available.
