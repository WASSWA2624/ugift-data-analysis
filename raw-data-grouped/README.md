# UgIFT facility records

Updated 25 September 2026 from `raw-data-ungrouped/` and `new-raw-data-221092026-1114/`, including the DATA MANAGEMENT UGIFT WhatsApp export through 25 September 2026 and its attachments. Earlier returns are retained. New files were added only where the content was not already filed.

Start with **facility-data-status.pdf**. It separates records received from facilities still awaiting a return, reported absences, substitutions and conflicting evidence.

## What the reconciliation shows

The school and health-centre master list contains 632 rows representing **629 distinct facilities**. A facility is treated as repeated only when it appears more than once within the same local government. Three facilities meet that rule: Kapedo in Karenga, Nyamarunda in Kibaale and Kidubuli HC II in Kabarole. All original rows and phase information are retained. Arua, Soroti and Hoima regional blood banks are allocated in the team distribution document and are tracked separately.

| Master-list outcome | Facilities | Share |
|---|---:|---:|
| Completed | 621 | 98.7% |
| No return on file | 8 | 1.3% |
| Identity or verification account needs review | 0 | 0.0% |
| Explained cases still outside completed | 0 | 0.0% |
| **Total distinct master facilities** | **629** | **100.0%** |

**Coverage is 621 + 0 + 0 = 621 of 629 master facilities (98.7%).** Percentage coverage = completed + needs review + explained cases. A facility with no return is completed when the case is explained or reconciled, including a submitted name that differs from the master list in the same local government. It is an accountability measure, not a physical-verification rate.

**Completed** means the facility has a return, or the lack of a return is explained or reconciled. Of the 621 completed records, 41 have identifiable data in consolidated asset registers. The remainder are facility returns or documented explanations. The register records share the same Completed category; their workbook, worksheet and row references remain in `facility-evidence-index.csv`. Completion does not certify that every asset was physically inspected. For example, Ntwetwe Seed School has a facility toolkit, while Awei Seed School has identifiable entries in the Team 7 register.

Explained and reconciled facilities with no separate return are included in Completed. Their reasons stay in `facility-reconciliation.csv`. Loinya HC II was replaced by Liko HC III, and Liko is represented by master entry H212. Oweko was replaced by Pamaka. Submitted names that differ from the master list are counted on the master row for the same local government: Busanga for Mantoroba, Nyambuusa for Nyabuswa, Iruhura for Kidubuli, Nakawala for Kabbo, Wamatovu for Kiringente and Rwamabara for Mpumudde. Nyakishenyi in Rukungiri is completed from its own handwritten return. Bikurungu remains a separate unmatched return. Mayanga HC III stays on the Mitooma health-centre register, Sheet1 row 1113. Johnson confirmed on 24 September 2026 that this health centre is in that file and in Mitooma District. The same message says Bumbaire SSS, Kyamuhunga SSS, Kashenshero SSS and Rwamujojo HC III did not benefit from UgIFT, so those four are completed as explained cases. Kishangara Seed Secondary School does not exist in Ibanda. Master entry S216 is kept and completed as an explained case, with no replacement school. The 24 September 2026 handwritten scan supplies returns for Kidukuru Seed Secondary School, counted on Hoima master entry S230 Buhanika, for Kigorobya Seed Secondary School in Hoima, and for Ngwedo Seed School in Buliisa. The 25 September batch adds filled toolkits for Kasoozo, Kirinya, Kireka Nsawo, Mutungo, Kasangati Ngabo, Sumbwe, Bukakata, Nangoma, Kasaali, Kikoma, Bunanywa, Buseregenyu and Mukoora, and a combined handwritten scan for Busunju, Namungo Health Centre III, Nyamarunda and St Maria Goretti Seed School at Manyogaseka. Kyasansuwa and St Mugagga already had toolkits in that scan, so no second form was made. St Catherine Kicucura Seed School in Kagadi is the UgIFT school for master Kiryanga and is counted on that row. The 24 September evening messages also rename Kikoola to Mukoora and Kyakatebe to Namabaale, exclude Kiziranfumbi from UgIFT, record that Butoloogo does not exist in Kasanda, limit Kyabakuza to staff quarters, and explain that Kyera and Ntete could not be verified because the assets were new and in store. Mayanga Seed School, Kasenda, Katoma, Mpongo, Namungo Seed School, Butaaka, Bulwadda and Bussi still have no return and no stated reason.

There are also **29 unmatched ground names or return identities** and **3 separately allocated blood banks**. Unmatched identities include possible aliases and district errors; they are not a count of confirmed additional physical facilities.

**Completed is not a certificate that every asset was physically checked.** Supporting information may be a toolkit, report, photographs, facility register or identifiable rows in a consolidated register. Known contradictions are withheld from the Completed total. In particular, Onywako's form states that physical verification did not take place; Olok's report says the facility was not constructed; the Iceme returns disagree about whether a visit occurred. A master construction status of Complete is not a verification status.

## Files to use

| File | Contents |
|---|---|
| `facility-data-status.pdf` | Summary, supervisor decisions, outstanding cases and facility rosters |
| `facility-reconciliation.csv` | Every distinct master facility, unmatched ground name/return and allocated blood bank, with status, source and explanation |
| `facility-evidence-index.csv` | Links each facility ID to source files and grouped destinations, including archive members and supplementary evidence |
| `supervisor-decisions.csv` | Exact chat wording, speaker, timestamp and treatment of each decision |
| `master-source-rows.csv` | All 632 master-list rows, including construction status and school phase |
| `master-duplicate-rows.csv` | The three repeated facility entries and their retained IDs |
| `_index.csv` | All source entries and filing destinations; 14,712 index rows |

`S001` means school data row 1 in the master document; `H001` means health-centre data row 1. The document's header adds one to the table row number. `X` IDs identify unmatched ground names/returns and `B` IDs identify allocated blood banks. IDs in the PDF can be looked up in the CSV files.

## Filing structure

```
team-NN/
  <Local government>/
    <Facility>/
    _district-documents/
  _team-documents/
_multi-team/
  programme-documents/
  teams-01-04/
  teams-10-15/
  teams-19-21/
  busoga-and-part-of-central/
  bunyoro-tooro-greater-mityana/
```

There are 519 facility folders. Shared documents may be filed under more than one facility. Folder counts therefore differ from master-list counts and must not be used as verification totals.

Team ownership follows `team-distributions.docx`. Master names and submitted names are both retained in the reconciliation. Routine spelling and local-government naming differences are normalized for matching; uncertain replacements and district changes remain open. Confirmed replacement names do not create an extra site: Loinya points to the already-listed Liko, and Kangole is reconciled with Kocheka. Wamatovu is the submitted name for Kiringente in Mpigi, and Rwamabara is the submitted name for Mpumudde in Lyantonde.

## Source handling

Raw files were not edited. Earlier loose-file placements are hard links: editing one of those grouped files can also change its raw original. Work on a separate copy when editing a return. Files added in this update are independent copies.

Archives were inspected, including nested ZIP and RAR archives. Exact duplicates were linked to existing destinations. Office lock files and the Team 10-15 working `tmp` directory were excluded. The WhatsApp archive is retained whole, with its text filed under `_multi-team/programme-documents/data-management-chat/`. Master-list screenshots are filed as reconciliation evidence, not site photographs.

The nested `WEMIS DISTRICT EQUIPMENT.rar` contains 107 readable, image-only PDFs covering 356 pages. Every page was reviewed. These are district equipment handover records for tablets, desktops and UPS units issued to local-government officers; they contain no school or health-facility returns. They are indexed individually as `in-archive` records and do not change the facility totals.

The index retains its original source column for compatibility. **Use the `source root` column** to distinguish the two input folders. `::` separates an archive from a member inside it. `placed`, `duplicate`, `extracted`, `in-archive` and `skipped` describe filing outcomes. New source rows include SHA-256 checksums. Identical files that moved from the 22 September folder to the 24 September folder keep their existing grouped copies.

## Reproducing this update

The scripts in `../scripts/` preserve the reviewed decisions and evidence mappings:

1. `update_grouped_data.py` refreshes source filing and the index. Its `--audit` and `--verify` options check historical and new source content.
2. `reconcile_facilities.py` rebuilds the CSV files and the report data from the master list, grouped index and reviewed mappings in `reconciliation-data/`.
3. `build_facility_status_report.py` rebuilds the PDF from that report data.

The scripts require Python with the document/PDF libraries used by the builders. When another batch arrives, review its new names and supervisor decisions before changing the curated mappings. A missing return alone must never be treated as proof that a facility does not exist.
