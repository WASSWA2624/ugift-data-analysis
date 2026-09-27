# UgIFT narrative report source log

Final report: `outputs/narrative-report/UgIFT Asset Verification Report.docx`.

## Register scope and counting basis

REF workbook: `outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`; worksheet `Asset Register`, data rows 2 through 225134, columns A:BL (64). All 225133 rows are counted once. The source workbook is unchanged.
MF workbook: `outputs/asset-register-2026-09-23/ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`; Asset Register rows 2:225134, A:BL. SK workbook: `outputs/asset-register-2026-09-23/ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx`; Asset Register rows 2:225134, A:U (21). Row identities and row counts checked across the three workbooks.

Money uses M FIXED_ASSETS_COST and AK DEPRN_RESERVE. NBV is max(cost less reserve, 0) on each row, then summed; absent cost stays outside the value total. Whole-shilling figures are rounded only after summing the source numeric values. Thus the rounded group amounts may differ by UGX 1 from the rounded programme amount. The zero floor means programme NBV need not equal aggregate cost minus aggregate depreciation.

Condition measures count BK ATTRIBUTE14 exactly Functional or Faulty, reproduced as register classifications. No claim is made that the full denominator was physically assessed. Engraving counts nonempty AP TAG_NUMBER not equal to Not engraved, case insensitive; UgIFT marking contains UGIFT or UGFT, case insensitive. IN_USE_FLAG is AU. Facility type is parsed from BL.

Use reason counts require AU=NO. Damage keywords are damaged, broken, faulty, not working and needs repair in SK N Equipment status or O Remarks and REF source-status wording. Storage uses positive stored, in store/box, not yet installed/in use or asset-new wording, excludes negated storage and conflicting damage/replacement/poor-condition wording, and is mutually exclusive with damage. The reviewed row selection is retained in the task analysis files.

Category precedence is buildings (C BUILDINGS AND STRUCTURES), transport (D TRANSPORT EQUIPMENT), health maternity wording (J or AX), health clinical furniture (E FURNITURE AND FITTINGS or named medical beds/couches/trolleys/screens/stands/lockers), other health medical equipment, health ICT, school furniture, school support names, school ICT excluding switches, remaining ICT, remaining furniture, Other assets. Support names are printer, photocopier, camera and projector. Category precedence prevents double counting. Blank minor2 rows are retained under Other recorded items in the class appendix; this is a reporting residual, not a new register class.

National level: the union of Facility type MDA, Hospital or Blood bank and rows held on a national ministry or agency book. This includes 14 Health centre type rows on MOH BK. Other rows follow their local-government region. KCCA rows explicitly have Facility type MDA and are national holdings for this report; no geographic assumption is used for them. Hospitals remain national even when BOOK_TYPE_CODE is a district book.

## Headline values and body repetition

[
  {
    "section": "3 Executive summary",
    "filter": "All REF Asset Register rows 2:225134; count rows, status, tags, cost, reserve and row-level max(cost-reserve,0). Coverage: README / facility-data-status PDF pages 1,5. Fieldwork dates: client draft paragraphs 140:164.",
    "values": {
      "assets": 225133,
      "functional": 211613,
      "nonfunctional": 13520,
      "assessed": 225133,
      "engraved": 50211,
      "ugift": 21023,
      "other_marking": 29188,
      "not_engraved": 174922,
      "in_use": 211613,
      "damaged_unused": 2569,
      "stored_unused": 483,
      "cost": 986778303394,
      "depreciation": 177319698579,
      "nbv": 809473130826,
      "capitalized": 193552,
      "cip": 4,
      "facilities": 899
    }
  }
]

## Tables

### Table 1: Local government field itinerary
Client draft, itinerary table 1, rows 2 to 7.

### Table 2: Programme outputs at closure
Client draft, paragraphs 69 to 75. These are programme outputs at closure.

### Table 3: Programme asset summary
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; all rows; reviewed transfer and storage wording. Appendix 8.1 provides the full regional summary schedule.

### Table 4: Master-list coverage and reconciliation
README, What the reconciliation shows; facility-data-status.pdf pages 1 and 5; facility-reconciliation.csv, scope Master list.

### Table 5: Supported master-list reconciliation outcomes
facility-reconciliation.csv and supervisor-decisions.csv; selected final outcomes, one per master ID. Full identity and decision references are in Appendix 8.6.

### Table 6: MoFPED asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = MOFPED BK; all rows held on this national vote.

### Table 7: MoWT asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = MOWT BK; all rows held on this national vote.

### Table 8: MoES asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = MOES BK; all rows held on this national vote.

### Table 9: MAAIF asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = MAAIF BK; all rows held on this national vote.

### Table 10: MoH asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = MOH BK; all rows held on this national vote.

### Table 11: OPM asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = OPM BK; all rows held on this national vote.

### Table 12: MoWE asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = MOWE BK; all rows held on this national vote.

### Table 13: MoGLSD asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = MGLSD BK; all rows held on this national vote.

### Table 14: NEMA asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = NEMA BK; all rows held on this national vote.

### Table 15: PPDA asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = PPDA BK; all rows held on this national vote.

### Table 16: OAG asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = OAG BK; all rows held on this national vote.

### Table 17: MoLG asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = MOLG BK; all rows held on this national vote.

### Table 18: MoLHUD asset holdings and recorded value
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; BOOK_TYPE_CODE = MOLHUD BK; all rows held on this national vote.

### Table 19: Other national holdings by institution group
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; Hospital, Blood bank, and MDA rows for KCCA BK, MODV BK and UBTS BK.

### Table 20: Central health centre assets by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; region = Central; Facility type = Health centre; report category precedence in section 5.6.

### Table 21: Central school assets by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; region = Central; Facility type = School; report category precedence in section 5.6.

### Table 22: Central sub-region distribution
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; local government level, region = Central; geography crosswalk in sources.md.

### Table 23: Eastern health centre assets by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; region = Eastern; Facility type = Health centre; report category precedence in section 5.6.

### Table 24: Eastern school assets by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; region = Eastern; Facility type = School; report category precedence in section 5.6.

### Table 25: Eastern sub-region distribution
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; local government level, region = Eastern; geography crosswalk in sources.md.

### Table 26: Northern health centre assets by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; region = Northern; Facility type = Health centre; report category precedence in section 5.6.

### Table 27: Northern school assets by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; region = Northern; Facility type = School; report category precedence in section 5.6.

### Table 28: Northern sub-region distribution
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; local government level, region = Northern; geography crosswalk in sources.md.

### Table 29: Western health centre assets by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; region = Western; Facility type = Health centre; report category precedence in section 5.6.

### Table 30: Western school assets by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; region = Western; Facility type = School; report category precedence in section 5.6.

### Table 31: Western sub-region distribution
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; local government level, region = Western; geography crosswalk in sources.md.

### Table 32: Whole programme and regional summary counts
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; count filters and reviewed transfer evidence in sources.md; reconciliation tables by scope and final outcome.

### Table 33: Asset rows by report category and region
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; mutually exclusive report category mapping in section 5.6.

### Table 34: Asset rows by register class and region
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; ASSET_CATEGORY_MINOR2 grouped by region. Other recorded items retain rows outside the listed classes.

### Table 35: Condition classifications by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; ATTRIBUTE14(Equipment status), grouped by category.

### Table 36: Condition classifications by sub-region
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; ATTRIBUTE14(Equipment status), grouped by subregion.

### Table 37: Recorded value and net book value by region
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; FIXED_ASSETS_COST, DEPRN_RESERVE and row-level max(cost less reserve, 0).

### Table 38: National ministry and agency value schedule
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; all rows on national ministry and agency books, plus Hospital holdings; blood banks are included on the UBTS vote.

### Table 39: Use flags and recorded reasons by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; IN_USE_FLAG, SK Equipment status and Remarks; negative and conflicting wording excluded from the stored group.

### Table 40: Engraving by region
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx, Asset Register, rows 2 to 225,134; TAG_NUMBER is not Not engraved; programme marking contains UGIFT or UGFT, ignoring case.

### Table 41: Master-list entries accounted for through reconciliation
facility-reconciliation.csv, selected master IDs; supervisor-decisions.csv, decision references shown; exact CSV record numbers in sources.md.

### Table 42: Ground-return identities outside master-list names
facility-reconciliation.csv, scope Ground return only, X identities. Names are retained as reconciliation identities.

### Table 43: Accompanying register files
The three accompanying workbook Asset Register and Read Me worksheets; data rows 2 to 225,134.

### Table 44: Core sources
Supplied project documents and register files.

### Table 45: Field observation source index
Facility and district reports identified by institution; full source file paths in sources.md.

### Table 46: Photographic source index
Field photographic returns and district reports; complete paths and adjacent caption text in sources.md.

## Charts and photographs

### Figure 1: All 629 master-list records are accounted for
Output file: `outputs/narrative-report/figures/chart_01_coverage.png`.
facility-reconciliation.csv, Master list scope; README coverage definition; 40 explained records included in the 629.

### Figure 2: MoFPED and MoES hold the largest ministry recorded values
Output file: `outputs/narrative-report/figures/chart_06_value_mda.png`.
Source: REF Asset Register, national ministry and agency book codes; all held facility types.

### Figure 3: Science laboratory tables and stools at a seed secondary school, Kalangala District (Buganda)
Output file: `outputs/narrative-report/figures/photo_01_central_laboratory_furniture.jpg`.
Field photographic record P01; Kalangala District; photograph locators in Appendix 8.8 and sources.md.

### Figure 4: Infant radiant warmer at a health centre, Makindye-Ssabagabo Municipal Council (Buganda)
Output file: `outputs/narrative-report/figures/photo_02_central_infant_warmer.jpg`.
Field photographic record P02; Makindye-Ssabagabo Municipal Council; photograph locators in Appendix 8.8 and sources.md.

### Figure 5: Desktop computers and classroom furniture at a seed secondary school, Busia District (Bukedi)
Output file: `outputs/narrative-report/figures/photo_03_eastern_school_computers.jpg`.
Field photographic record P03; Busia District; photograph locators in Appendix 8.8 and sources.md.

### Figure 6: Delivery bed with a torn mattress cover at a health centre, Busia District (Bukedi)
Output file: `outputs/narrative-report/figures/photo_04_eastern_torn_bed_cover.jpg`.
Field photographic record P04; Busia District; photograph locators in Appendix 8.8 and sources.md.

### Figure 7: Buildings at a seed secondary school, Nwoya District (Acholi)
Output file: `outputs/narrative-report/figures/photo_05_northern_school_buildings.jpg`.
Field photographic record P05; Nwoya District; photograph locators in Appendix 8.8 and sources.md.

### Figure 8: Health centre building, Nwoya District (Acholi)
Output file: `outputs/narrative-report/figures/photo_06_northern_health_building.jpg`.
Field photographic record P06; Nwoya District; photograph locators in Appendix 8.8 and sources.md.

### Figure 9: Classroom desks at a seed secondary school, Ntoroko District (Tooro)
Output file: `outputs/narrative-report/figures/photo_08_western_classroom_desks.jpg`.
Field photographic record P08; Ntoroko District; photograph locators in Appendix 8.8 and sources.md.

### Figure 10: Delivery bed and clinical furniture at a health centre, Kabarole District (Tooro)
Output file: `outputs/narrative-report/figures/photo_09_western_delivery_bed.jpg`.
Field photographic record P09; Kabarole District; photograph locators in Appendix 8.8 and sources.md.

### Figure 11: School furniture forms the largest asset category
Output file: `outputs/narrative-report/figures/chart_02_condition_category.png`.
Source: REF Asset Register, all rows; report category and ATTRIBUTE14 condition.

### Figure 12: The Functional classification predominates across sub-regions
Output file: `outputs/narrative-report/figures/chart_03_condition_subregion.png`.
Source: REF Asset Register, local government rows; sub-region mapping and ATTRIBUTE14.

### Figure 13: Recorded use is concentrated in school furniture
Output file: `outputs/narrative-report/figures/chart_07_use_category.png`.
Source: REF Asset Register, IN_USE_FLAG; SK condition and remarks for non-use reasons.

### Figure 14: Boxed computers and related equipment in a seed school store, Nwoya District (Acholi)
Output file: `outputs/narrative-report/figures/photo_07_northern_stored_computers.jpg`.
Field photographic record P07; Nwoya District; photograph locators in Appendix 8.8 and sources.md.

### Figure 15: Most asset rows carry the Not engraved designation
Output file: `outputs/narrative-report/figures/chart_04_engraving.png`.
Source: REF Asset Register, TAG_NUMBER; case-insensitive UGIFT or UGFT matching.

### Figure 16: UgIFT identification on a desk at a seed school, Tororo District (Bukedi)
Output file: `outputs/narrative-report/figures/photo_10_eastern_ugift_marking.jpg`.
Field photographic record P10; Tororo District; photograph locators in Appendix 8.8 and sources.md.

### Figure 17: Eastern holds the largest regional recorded value
Output file: `outputs/narrative-report/figures/chart_05_value_region.png`.
Source: REF Asset Register, cost and depreciation; row net book value floored at zero.

## Narrative sources

- 4.1 Introduction: Client draft, paragraphs 10, 13 and 35 to 48
- 4.2 Background to the verification: Client draft, paragraph 13
- 4.3 Justification: Client draft, paragraphs 13, 35 to 41 and 43 to 49
- 4.4 Objectives of the assignment: Client draft, paragraphs 35 to 41
- 4.5 Scope of work: Client draft, paragraphs 43 to 49 and 161; Government of Uganda Asset Accounting Policies and Guidelines 2023, section 3.3.3, printed page 48, PDF page 60
- 5.1 Inception and preparation: Client draft, paragraphs 95 to 109, 132 and 136 to 137
- 5.2 Verification instruments: Client draft, paragraphs 111 to 129 and 134
- 5.3 Data collection and field itinerary: Client draft, paragraphs 140 to 164; itinerary table 1, rows 2 to 7
- 5.4 Quality assurance: Client draft, paragraphs 197 to 206
- 5.5 Consolidation and reporting: Client draft, paragraphs 172 to 195
- 5.6 Classification and accounting basis: Government of Uganda Asset Accounting Policies and Guidelines 2023, sections 3.2.1, 3.3.3, 5.5 and 5.7 and Annex 1; REF register, Read Me rows 14, 40 to 43
- 6.1 Programme background and design: Client draft, paragraphs 52 and 54
- 6.2 Programme components: Client draft, paragraphs 56 to 67 and 77 to 78
- 6.3 Programme objectives: Client draft, paragraphs 86 to 91
- 6.4 Programme outputs: Client draft, paragraphs 69 to 75

## Field observation evidence

- O01: `raw-data-grouped/team-18/Kayunga/Busaale-HC-III/BUSAALE HC III.docx`; paragraph 41, answering interview table 3. Busaale Health Centre III in Kayunga District uses Primary Health Care funds for maintenance.
- O02: `raw-data-grouped/team-18/Kayunga/Busaale-HC-III/BUSAALE HC III.docx`; paragraph 47. Busaale Health Centre III keeps a physical inventory file and records asset condition quarterly.
- O03: `raw-data-grouped/team-18/Kayunga/Busaale-HC-III/BUSAALE HC III.docx`; paragraphs 56 to 58. At Busaale Health Centre III, the interview identified maternity roof leakage, damaged door hinges and a solar system requiring battery replacement.
- O04: `raw-data-grouped/team-18/Kayunga/Musiitwa-Seed-Secondary-School-Nazigo/MUSIITWA SEED SCHOOL.docx`; paragraphs 7, 13 and 14. Musiitwa Seed Secondary School in Kayunga District checks asset functionality each term and repairs desks, windows, tables and stools as funds permit. Broken furniture stays out of use until repaired.
- O05: `raw-data-grouped/team-18/Kayunga/Musiitwa-Seed-Secondary-School-Nazigo/MUSIITWA SEED SCHOOL.docx`; paragraphs 20 and 23 to 25. The Musiitwa school interview reported wider access to secondary education for the surrounding communities, alongside attendance pressures linked to long walking distances and pupils' engagement in petty trade.
- O06: `raw-data-grouped/team-18/Kayunga/Musiitwa-Seed-Secondary-School-Nazigo/MUSIITWA SEED SCHOOL.docx`; paragraph 61. Musiitwa Seed Secondary School uses its UgIFT irrigation system for teaching demonstrations and food production.
- O07: `raw-data-grouped/team-18/Kamuli/Kagumba-HC-III/KAGUMBA HC III.docx`; paragraph 47. Kagumba Health Centre III in Kamuli District keeps a book recording asset condition.
- O08: `raw-data-grouped/team-18/Kamuli/Kagumba-HC-III/KAGUMBA HC III.docx`; paragraphs 53 and 54. The interview at Kagumba Health Centre III linked the new maternity ward to increased delivery and antenatal services for surrounding communities, including the landing site population.
- O09: `raw-data-grouped/team-18/Kamuli/Kagumba-HC-III/KAGUMBA HC III.docx`; paragraphs 57 to 59. The Kagumba interview identified pressure on staff housing and the need for an outpatient department, store, laboratory and patients' kitchen.
- O10: `raw-data-grouped/team-13/Busia/_district-documents/Busia-local-government-report.docx`; paragraph 13. In Busia District, requisition vouchers record equipment transfers from Bumunji, Buwembe and Majanji health centres to Masafu Hospital.
- O11: `raw-data-grouped/team-13/Busia/_district-documents/Busia-local-government-report.docx`; paragraph 20. The Busia report recorded broken desks and a cracked laboratory stool at Sikuda Seed Secondary School, with the stool still in use.
- O12: `raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`; paragraphs 69 and 70. Lungulu Seed Secondary School in Nwoya District funds minor maintenance from school revenue and seeks technical support from the District Education Officer. It keeps regular records of functionality and breakdowns.
- O13: `raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`; paragraphs 62 and 74. At Lungulu Seed Secondary School, computers and related equipment remained in storage pending a suitable power connection.
- O14: `raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`; paragraphs 135 and 136. Todora Health Centre III in Nwoya District relies on the Gulu Regional Referral Hospital technical team for major medical equipment maintenance. Facility staff maintain breakdown logs and refer them to the District Health Officer and technical team.
- O15: `raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`; paragraphs 125, 145 and 146. Equipment intended for Todora Health Centre III was directed to Paraa Health Centre III while construction was under way at Todora. The district report recommended a formal transfer and corresponding updates to the asset ledgers.
- O16: `raw-data-grouped/team-01/Nebbi/_district-documents/UGIFT Assets Verification Nebbi District Report.docx`; paragraphs 27 and 28. The Pamaka Health Centre III interview in Nebbi District identified a nonfunctional solar system and power constraints that prevented use of oxygen equipment.
- O17: `raw-data-grouped/team-01/Nebbi/_district-documents/UGIFT Assets Verification Nebbi District Report.docx`; paragraphs 17 and 29. Pamaka Health Centre III reported increased patient attendance and greater community confidence in its services. The interview also identified pressure on medical staffing as patient numbers increased.
- O18: `raw-data-grouped/team-10/Moroto/_district-documents/Moroto-local-government-report.docx`; paragraph 14. The Moroto report recorded neonatal respiratory equipment in an unopened carton and treatment trolleys still wrapped at Kalemungole Health Centre III.
- O19: `raw-data-grouped/team-10/Moroto/_district-documents/Moroto-local-government-report.docx`; paragraph 16. Rupa Seed School in Moroto District hired a generator for practical lessons because its ICT rooms lacked an operational power connection. The report also described the library and computer laboratory block being used as dormitories.
- O20: `raw-data-grouped/team-30/Kibaale/Nyamarunda-HC-III/NYAMARUNDA HC III asset verification 24 Sep 2026.docx`; table 2, rows 2 and 3. Nyamarunda Health Centre III in Kibaale District records broken and nonfunctional items, sets them aside and reports them to the District Health Officer for action.
- O21: `raw-data-grouped/team-30/Kibaale/Nyamarunda-HC-III/NYAMARUNDA HC III asset verification 24 Sep 2026.docx`; table 2, rows 4 and 5. The Nyamarunda interview identified poor workmanship in staff quarters, electrical installation concerns, drainage and water security problems, and constrained storage space. It recommended a technical assessment of the staff quarters, window security improvements and better storage facilities.
- O22: `raw-data-grouped/team-25/Buliisa/Avogera-HC-III/AVOGERA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx`; paragraphs 40 to 42 and 50 to 58. Avogera Health Centre III in Buliisa District undertakes some repairs locally and receives support from Hoima Regional Referral Hospital. It keeps items in storage when it cannot repair them and identified a need for technical skills, user orientation and more storage space.
- O23: `raw-data-grouped/team-25/Buliisa/Ngwedo-Seed-Secondary-School/NGWEDO SEED SECONDARY SCHOOL ASSET VERIFICATION 24 Sep 2026.docx`; table 2, rows 3 and 4. Ngwedo Seed Secondary School in Buliisa District engages a caretaker monthly for repairs. The Directorate of Industrial Training undertakes furniture repairs.
- O24: `raw-data-grouped/team-26/Bundibugyo/Bundimulangya-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT 222 BUNDIMULANGYA HEALTH CENTRE III AND BURONDO SEED SCHOOL (1).docx`; paragraphs 41, 50 and 59. Bundimulangya Health Centre III in Bundibugyo District refers maintenance needs to the District Health Officer, who sends a maintenance team. Its interview records regular functionality monitoring and reports that the power house and solar installation support continued operation.
- O25: `raw-data-grouped/team-28/Kyenjojo/Kyankaramata-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT 222 kyankaramata hc iii.docx`; paragraphs 41 and 62. Kyankaramata Health Centre III in Kyenjojo District funds minor repairs from Primary Health Care funds but identifies the cost of major repairs as a constraint. Its interview recommends consultation with facility managers before procurement to match equipment to need and storage capacity.
- O26: `raw-data-grouped/team-25/Hoima/Kigorobya-Seed-Secondary-School/KIGOROBYA SEED SECONDARY SCHOOL ASSET VERIFICATION 24 Sep 2026.docx`; table 2, rows 3 to 5. Kigorobya Seed Secondary School in Hoima District undertakes some maintenance locally and receives ministry support for other work. Its interview describes improved teaching facilities through the equipped ICT room, chemistry laboratory and classrooms, alongside constraints in study materials and staffing.
- O27: `raw-data-grouped/team-31/Buvuma/Lukale-HC-III/LUKALE H.C III (1).docx`; paragraphs 59 and 61. The Lukale Health Centre III interview in Buvuma District reports that the maternity ward allows women to give birth locally instead of crossing water and provides greater privacy.
- O28: `raw-data-grouped/team-18/Kamuli/Kagumba-Seed-Secondary-School/Kagumba Seed school.docx`; paragraph 7. Kagumba Seed Secondary School in Kamuli District reported that broken furniture had been repaired during the second term.
- O29: `raw-data-grouped/team-18/Kamuli/Bubago-HC-III/Bubago HCII.docx`; paragraphs 57 and 61. The Bubago health centre interview in Kamuli District identified limited staff capacity to operate and maintain an oxygen concentrator, and recommended user training and basic maintenance support.

## Every photograph and its source image

### P01
`raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`; `word/media/image9.jpeg`; body block 35; adjacent text: 5. Science laboratory tables and stools | 5. Science laboratory tables and stools
Body block 35: 5. Science laboratory tables and stools. Facility and local government from the containing folder.
Selected image inspected; no identifiable faces, name badges, signatures or personal documents visible.

### P02
`raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`; `word/media/image22.jpeg`; body block 77; adjacent text: 
Body block 77, image22.jpeg, following the Kibiri Health Centre III report; document paragraphs 1, 5 and 6 identify the facility and location.
Selected image inspected; no identifiable faces, name badges, signatures or personal documents visible.

### P03
`raw-data-grouped/team-13/Busia/Sikuda-Seed-Secondary-School/43_ict-room-desktop-computers_ref0257.jpg`; `None`; body block None; adjacent text: None
Loose photograph; source filename identifies ICT room desktop computers; facility and district from source folders.
Selected image inspected; no identifiable faces, name badges, signatures or personal documents visible.

### P04
`raw-data-grouped/team-13/Busia/Majanji-HC-III/050_delivery-bed-with-torn-cover_ref20260827-0646.jpg`; `None`; body block None; adjacent text: None
Loose photograph; source filename identifies delivery bed with torn cover; facility and district from source folders. Caption describes visible condition only.
Selected image inspected; no identifiable faces, name badges, signatures or personal documents visible.

### P05
`raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`; `word/media/image14.jpeg`; body block 107; adjacent text: 
Body block 107, image14.jpeg, under LUNGULU SEED SECONDARY SCHOOL NWOYA DISTRICT LOCAL GOVERNMENT (block 55), with field photographs following block 82. The section runs until Todora HC heading at block 117.
Selected image inspected; no identifiable faces, name badges, signatures or personal documents visible.

### P06
`raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`; `word/media/image37.jpeg`; body block 308; adjacent text: 
Body block 308, image37.jpeg, under GOT APWOYO HEALTH CENTRE III | NWOYA DISTRICT LOCAL GOVERNMENT heading at block 269.
Selected image inspected; no identifiable faces, name badges, signatures or personal documents visible.

### P07
`raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`; `word/media/image9.jpeg`; body block 83; adjacent text: Laboratory stool supply: Procure and deliver an additional cohort of laboratory stools (recommended minimum 66 stools) to meet the standard lab allocation of 74 stools. | Field photos
Body block 83, image9.jpeg, after Field photos block 82 within Lungulu school section. Block 62 states that desktop computers, surge protectors, printer and UPS units are stored in the school store awaiting power connection.
Selected image inspected; no identifiable faces, name badges, signatures or personal documents visible.

### P08
`raw-data-grouped/team-26/Ntoroko/Nombe-Seed-Secondary-School/NTOROKO ASSET NOMBE SEED SECONDARY SCHOOL VERIFICATION AND RECORDING TOOL KIT 222.docx`; `word/media/image4.jpeg`; body block 110; adjacent text: Equipment/ Item | Department | Asset Number | Item | Description | Life in Months | Tag Number  | ( engrave |  no.) | Date Of  | Pur | Date Placed  | In |  Service | Recoverable cost | Cost | Acc Dep Cost | Net Book Value | Ytd |   | Deprn | Equipment status | Remarks | Non residential | Education | Painted cream and white | Good condition | They are in use. They are seven in number. | Residential | Education | Painted cream and white | Good condition | They are all in use. | They are 3 in number. | Kitchen | Education | Not built. | Toilets | Education | Not constructed | Pit latrine | Education | They are painted cream and white. | Good condition | They are all in use. | They are all in use. | 3 are for residential and 3 are not for residential. | Water tanks | Education | They are black in  | colour | One is faulty and  | two are working. | Two in use.  | They re |  three. Not constructed. | Fence | Not constructed.
Body block 110, image4.jpeg, after building inventory table at block 109. Caption at block 111: Main gate, Desks, Classroom. School interview block 54 identifies Nombe school; verification details table at block 29 identifies Western, Tooro, Ntoroko.
Selected image inspected; no identifiable faces, name badges, signatures or personal documents visible.

### P09
`raw-data-grouped/team-26/Kabarole/Iruhura-HC-III/KABAROLE DISTRICT   IRUHURA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222 (1).docx`; `word/media/image10.jpeg`; body block 96; adjacent text: OPD                                           |                               |      | Pit latrine |                               |                       Power House |                       | Weighing scale with a height meter
Body block 96, image10.jpeg; photograph group captions at blocks 100 to 101 include Delivery bed. Verification details table at block 29 identifies Western, Tooro, Kabarole; facility heading at block 38 and checklist heading at block 75 identify Iruhura HC III.
Selected image inspected; no identifiable faces, name badges, signatures or personal documents visible.

### P10
`raw-data-grouped/team-13/Tororo/Malaba-Seed-School/049_desk-engraving-gou-moh-ugift_ref20260829-0338.jpg`; `None`; body block None; adjacent text: None
Loose photograph; source filename identifies desk engraving GOU MOH UGIFT; facility and district from source folders. The visible marking reads GOU/MOH-UGIFT PROJECT, F/Y 2023/2024.
Selected image inspected; no identifiable faces, name badges, signatures or personal documents visible.


# Facility reconciliation and geography source audit

## Coverage

- `raw-data-grouped/README.md`, section "What the reconciliation shows": 632 master rows, 629 distinct records, all 629 accounted for; this is explicitly accountability coverage, not a physical-verification rate.
- `raw-data-grouped/facility-data-status.pdf`, pages 1 and 5: 548 with facility-specific material, 41 with identifiable consolidated-register information, and 40 explained or reconciled without a separate return. Therefore 589 supported by facility materials or consolidated-register entries.
- `raw-data-grouped/facility-reconciliation.csv`, `scope=Master list`: 629 records; `type=Health centre` 371; `type=School` 258. Region/type totals use the geography mapping below.
- 589 filter: `scope=Master list` and `verification != Case explained or reconciled; counted as completed`. Forty-record filter uses equality to that verification text.
- `master-source-rows.csv`: retains 632 source rows. Within-local-government duplicate pairs are S146/S147 Kapedo (Karenga), H299/H300 Nyamarunda (Kibaale), H329/H331 Kidubuli (Kabarole).
- Physical-verification total omitted because these sources do not establish one. Returning materials, desk review and reconciliation must not be relabelled as physical inspection.

## Selected acceptable outcomes

55 distinct master identities were selected for the six requested substantive reasons. This total overlaps entries supported by facility material and must not be subtracted from 629 or described as the total not physically verified.

- Does not exist or was not constructed under the programme: 10.
- Replaced by another facility: 4.
- Operates under another name: 30.
- Not a UgIFT beneficiary: 3.
- Assets relocated to another facility or held at district: 3.
- Exists with no UgIFT assets: 5.

| ID | Local government | Final outcome | Reconciliation locator | Supervisor decision |
|---|---|---|---|---|
| H205 | Pader | Olok Health Centre III was not constructed under the programme. | facility-reconciliation.csv, id=H205, CSV data record 74 | Reconciliation note and receiving source |
| H190 | Lira | The master-list entry Alik HCII does not exist under the programme. | facility-reconciliation.csv, id=H190, CSV data record 83 | supervisor-decisions.csv, id=CHAT11, CSV data record 11 |
| H197 | Oyam | The master-list entry Acimi HC II does not exist under the programme. | facility-reconciliation.csv, id=H197, CSV data record 97 | supervisor-decisions.csv, id=CHAT17, CSV data record 21 |
| H195 | Oyam | The master-list entry Acokara HCII does not exist under the programme. | facility-reconciliation.csv, id=H195, CSV data record 98 | supervisor-decisions.csv, id=CHAT17, CSV data record 21 |
| H200 | Oyam | The master-list entry Ariba HC II does not exist under the programme. | facility-reconciliation.csv, id=H200, CSV data record 101 | supervisor-decisions.csv, id=CHAT17, CSV data record 21 |
| H070 | Busia MC | The master-list entry Busia Eastern Division does not exist under the programme. | facility-reconciliation.csv, id=H070, CSV data record 227 | supervisor-decisions.csv, id=CHAT19, CSV data record 23 |
| S010 | Tororo MC | The master-list entry Eastern Division does not exist under the programme. | facility-reconciliation.csv, id=S010, CSV data record 243 | supervisor-decisions.csv, id=CHAT20, CSV data record 24 |
| S012 | Jinja City | The master-list entry Central Division does not exist under the programme. | facility-reconciliation.csv, id=S012, CSV data record 314 | supervisor-decisions.csv, id=USER01, CSV data record 25 |
| S216 | Ibanda | The master-list entry Kishangara seed school does not exist under the programme. | facility-reconciliation.csv, id=S216, CSV data record 386 | supervisor-decisions.csv, id=USER03, CSV data record 70 |
| H010 | Kasanda | The master-list entry Butoloogo HC II does not exist under the programme. | facility-reconciliation.csv, id=H010, CSV data record 564 | supervisor-decisions.csv, id=CHAT45D, CSV data record 74 |
| H218 | Nebbi | The master-list entry Oweko HC II was replaced by Pamaka Health Centre III. | facility-reconciliation.csv, id=H218, CSV data record 2 | supervisor-decisions.csv, id=CHAT21D, CSV data record 30 |
| H213 | Maracha | The master-list entry Loinya HC II was replaced by Liko Health Centre III (H212). | facility-reconciliation.csv, id=H213, CSV data record 30 | supervisor-decisions.csv, id=CHAT04, CSV data record 4 |
| H150 | Lamwo | The master-list entry Ngomoromo HC II was replaced by Pangira Health Centre III. | facility-reconciliation.csv, id=H150, CSV data record 69 | supervisor-decisions.csv, id=CHAT01, CSV data record 1 |
| H354 | Ntoroko | The master-list entry Musandama HC II was replaced by Butungama Health Centre III. | facility-reconciliation.csv, id=H354, CSV data record 495 | supervisor-decisions.csv, id=CHAT22, CSV data record 31 |
| S167 | Serere | The master-list entry Kadungulu Seed School was reconciled to Kagwara Seed Secondary School. | facility-reconciliation.csv, id=S167, CSV data record 165 | supervisor-decisions.csv, id=CHAT07, CSV data record 7 |
| H125 | Bukedea | The master-list entry Kocheka HC II was reconciled to Kangole / Kocheka Health Centre III. | facility-reconciliation.csv, id=H125, CSV data record 170 | supervisor-decisions.csv, id=CHAT09, CSV data record 9 |
| S103 | Pallisa | The master-list entry Pallisa was reconciled to Akadot Seed Secondary School. | facility-reconciliation.csv, id=S103, CSV data record 184 | supervisor-decisions.csv, id=CHAT05, CSV data record 5 |
| H065 | Busia | The master-list entry Dabani was reconciled to Buwumba Health Centre III. | facility-reconciliation.csv, id=H065, CSV data record 223 | supervisor-decisions.csv, id=CHAT18, CSV data record 22 |
| S127 | Bulambuli | The master-list entry Bunambutye Seed School was reconciled to Bumufuni Seed Secondary School. | facility-reconciliation.csv, id=S127, CSV data record 256 | supervisor-decisions.csv, id=CHAT47B, CSV data record 90 |
| S011 | Bugweri | The master-list entry Igombe was reconciled to Mpiita Seed Secondary School. | facility-reconciliation.csv, id=S011, CSV data record 290 | supervisor-decisions.csv, id=CHAT06, CSV data record 6 |
| S112 | Jinja | The master-list entry Butagaya was reconciled to Buwala Seed Secondary School. | facility-reconciliation.csv, id=S112, CSV data record 311 | supervisor-decisions.csv, id=CHAT12, CSV data record 12 |
| S122 | Namayingo | The master-list entry Mwema Seed School was reconciled to Mutumba Seed Secondary School. | facility-reconciliation.csv, id=S122, CSV data record 327 | supervisor-decisions.csv, id=CHAT13, CSV data record 13 |
| S086 | Mukono | The master-list entry Kimenyedde Seed School was reconciled to St Andrews Ndwaddemutwe Seed Secondary School. | facility-reconciliation.csv, id=S086, CSV data record 341 | supervisor-decisions.csv, id=CHAT08, CSV data record 8 |
| S213 | Buhweju | The master-list entry Nsiika T/C was reconciled to Ndibarema Memorial Seed Secondary School. | facility-reconciliation.csv, id=S213, CSV data record 369 | supervisor-decisions.csv, id=CHAT16, CSV data record 20 |
| S048 | Kagadi | The master-list entry Kagadi was reconciled to King Solomon Seed Secondary School. | facility-reconciliation.csv, id=S048, CSV data record 469 | supervisor-decisions.csv, id=CHAT35K, CSV data record 53 |
| S232 | Kagadi | The master-list entry Kiryanga Seed School was reconciled to St Catherine Kicucura Seed Secondary School. | facility-reconciliation.csv, id=S232, CSV data record 470 | supervisor-decisions.csv, id=CHAT45H, CSV data record 78 |
| S049 | Kagadi | The master-list entry Ruteete was reconciled to Kitegwa Community Seed Secondary School. | facility-reconciliation.csv, id=S049, CSV data record 471 | supervisor-decisions.csv, id=CHAT35L, CSV data record 54 |
| H318 | Bundibugyo | The master-list entry Mantoroba HC II was reconciled to Busanga Health Centre III. | facility-reconciliation.csv, id=H318, CSV data record 479 | Reconciliation note and receiving source |
| H329 | Kabarole | The master-list entry Kidubuli HC II was reconciled to Iruhura Health Centre III. | facility-reconciliation.csv, id=H329, CSV data record 486 | Reconciliation note and receiving source |
| H332 | Kabarole | The master-list entry Nyabuswa HC II was reconciled to Nyambuusa Health Centre III. | facility-reconciliation.csv, id=H332, CSV data record 489 | Reconciliation note and receiving source |
| S252 | Kabarole | The master-list entry Kasenda Seed School was reconciled to St Paul Nyabweya Seed Secondary School. | facility-reconciliation.csv, id=S252, CSV data record 492 | supervisor-decisions.csv, id=CHAT46A, CSV data record 79 |
| S056 | Bunyangabu | The master-list entry Kabonero was reconciled to Katugunda Seed Secondary School. | facility-reconciliation.csv, id=S056, CSV data record 502 | supervisor-decisions.csv, id=CHAT32A, CSV data record 41 |
| S057 | Bunyangabu | The master-list entry Kyamukube Town Council was reconciled to Nsuura Seed Secondary School. | facility-reconciliation.csv, id=S057, CSV data record 504 | supervisor-decisions.csv, id=CHAT32B, CSV data record 42 |
| H036 | Mubende | The master-list entry Kabbo was reconciled to Nakawala Health Centre III. | facility-reconciliation.csv, id=H036, CSV data record 536 | Reconciliation note and receiving source |
| H292 | Kakumiro | The master-list entry Kikoola was reconciled to Mukoora Health Centre III. | facility-reconciliation.csv, id=H292, CSV data record 546 | supervisor-decisions.csv, id=CHAT45A, CSV data record 71 |
| H015 | Kasanda | The master-list entry Kyakatebe HC II was reconciled to Namabaale Health Centre III. | facility-reconciliation.csv, id=H015, CSV data record 567 | supervisor-decisions.csv, id=CHAT45C, CSV data record 73 |
| S066 | Kalangala | The master-list entry Bufumira Seed School was reconciled to Nekemiya Memorial Seed Secondary School. | facility-reconciliation.csv, id=S066, CSV data record 587 | supervisor-decisions.csv, id=CHAT39, CSV data record 59 |
| S084 | Mpigi | The master-list entry Kiringente Seed School was reconciled to Wamatovu Seed Secondary School. | facility-reconciliation.csv, id=S084, CSV data record 600 | Reconciliation note and receiving source |
| H027 | Lwengo | The master-list entry Kagganda HC II was reconciled to Mbirizi Seed Secondary School. | facility-reconciliation.csv, id=H027, CSV data record 612 | supervisor-decisions.csv, id=CHAT40, CSV data record 60 |
| S081 | Lyantonde | The master-list entry Mpumudde seed school was reconciled to Rwamabara Seed Secondary School. | facility-reconciliation.csv, id=S081, CSV data record 619 | Reconciliation note and receiving source |
| H054 | Wakiso | Bussi is the village name for Zinga Health Centre III; the Zinga return is counted once on H052. | facility-reconciliation.csv, id=H054, CSV data record 602 | supervisor-decisions.csv, id=USER04, CSV data record 91 |
| S230 | Hoima | The master-list entry Buhanika was reconciled to Kidukuru Seed Secondary School. | facility-reconciliation.csv, id=S230, CSV data record 461 | Reconciliation note and receiving source |
| S065 | Gomba | The submitted Kyayi Seed School return was reconciled to the master-list Maddu Seed School. | facility-reconciliation.csv, id=S065, CSV data record 595 | supervisor-decisions.csv, id=CHAT38, CSV data record 58 |
| S235 | Kibaale | The master-list entry Mugarama( new facilities for St Mugagga S.S) was reconciled to St Mugagga Vocational Seed Secondary School. | facility-reconciliation.csv, id=S235, CSV data record 574 | supervisor-decisions.csv, id=CHAT30, CSV data record 39 |
| H193 | Oyam | Alira HCII is not a UgIFT beneficiary. | facility-reconciliation.csv, id=H193, CSV data record 100 | supervisor-decisions.csv, id=CHAT17, CSV data record 21 |
| H086 | Kaliro | Buyinda HC II is not a UgIFT beneficiary. | facility-reconciliation.csv, id=H086, CSV data record 316 | supervisor-decisions.csv, id=CHAT14, CSV data record 14 |
| S237 | Kikuube | Kiziranfumbi Seed School is not a UgIFT beneficiary. | facility-reconciliation.csv, id=S237, CSV data record 472 | supervisor-decisions.csv, id=CHAT45B, CSV data record 72 |
| H231 | Zombo | The UgIFT assets for Alangi were relocated to Amwonyo Health Centre III. | facility-reconciliation.csv, id=H231, CSV data record 14 | supervisor-decisions.csv, id=CHAT21A, CSV data record 27 |
| H233 | Zombo | The UgIFT assets for Ther-uru HC II were relocated to Atyak Health Centre III. | facility-reconciliation.csv, id=H233, CSV data record 16 | supervisor-decisions.csv, id=CHAT21B, CSV data record 28 |
| S208 | Zombo | The UgIFT assets for Abanga were relocated to Kango Seed Secondary School. | facility-reconciliation.csv, id=S208, CSV data record 17 | supervisor-decisions.csv, id=CHAT21C, CSV data record 29 |
| H149 | Kitgum MC | Pandwong HC II exists with no UgIFT assets. | facility-reconciliation.csv, id=H149, CSV data record 67 | supervisor-decisions.csv, id=CHAT02, CSV data record 2 |
| S214 | Bushenyi | Bumbaire Seed School exists with no UgIFT assets. | facility-reconciliation.csv, id=S214, CSV data record 345 | supervisor-decisions.csv, id=CHAT44A, CSV data record 65 |
| S215 | Bushenyi | Kyamuhunga exists with no UgIFT assets. | facility-reconciliation.csv, id=S215, CSV data record 346 | supervisor-decisions.csv, id=CHAT44B, CSV data record 66 |
| S221 | Mitooma | Kashenshero exists with no UgIFT assets. | facility-reconciliation.csv, id=S221, CSV data record 351 | supervisor-decisions.csv, id=CHAT44C, CSV data record 67 |
| H282 | Sheema MC | Rwamujojo HC II exists with no UgIFT assets. | facility-reconciliation.csv, id=H282, CSV data record 361 | supervisor-decisions.csv, id=CHAT44D, CSV data record 68 |

## Ground-return identities

- Filter `scope=Ground return only`: 24 return identities, not 24 confirmed additional physical facilities. Filter excludes 11 linked receiving records and 3 separately allocated blood banks.
- Identity counts are 15 health-facility identities and 9 school identities. Rukoki is described as a general hospital in the return even though reconciliation type is Health centre.
- X901 Ekaligo and X902 Liko are independently named facilities according to USER02 but have no separate asset schedules within the combined records. X019 Onywako explicitly records no physical verification.
- Ground identities can include aliases or district errors; the report must not assert all are unique additional physical facilities.

| ID | Local government | Return identity | Locator |
|---|---|---|---|
| X013 | Zombo | Amei Seed Secondary School | facility-reconciliation.csv, id=X013, CSV data record 631 |
| X016 | Maracha | Odupiri Health Centre III | facility-reconciliation.csv, id=X016, CSV data record 635 |
| X901 | Yumbe | Ekaligo Health Centre III | facility-reconciliation.csv, id=X901, CSV data record 636 |
| X902 | Yumbe | Liko Health Centre III | facility-reconciliation.csv, id=X902, CSV data record 637 |
| X017 | Yumbe | Lobe Health Centre III | facility-reconciliation.csv, id=X017, CSV data record 638 |
| X018 | Yumbe | Nyori Health Centre III | facility-reconciliation.csv, id=X018, CSV data record 639 |
| X019 | Lira | Onywako Health Centre III | facility-reconciliation.csv, id=X019, CSV data record 640 |
| X020 | Apac | Arocha Health Centre III | facility-reconciliation.csv, id=X020, CSV data record 641 |
| X021 | Moroto | Rupa Seed Secondary School | facility-reconciliation.csv, id=X021, CSV data record 643 |
| X022 | Karenga | Lokori Seed Secondary School | facility-reconciliation.csv, id=X022, CSV data record 644 |
| X900 | Busia MC | Sofia Health Centre III | facility-reconciliation.csv, id=X900, CSV data record 645 |
| X024 | Sironko | Simu Pondo Health Centre III | facility-reconciliation.csv, id=X024, CSV data record 646 |
| X003 | Bushenyi | Kabushaho Seed Secondary School | facility-reconciliation.csv, id=X003, CSV data record 647 |
| X004 | Mitooma | Kitojo Seed Secondary School | facility-reconciliation.csv, id=X004, CSV data record 648 |
| X005 | Sheema | Migina Health Centre III | facility-reconciliation.csv, id=X005, CSV data record 649 |
| X025 | Rubanda | Kibuzigye Seed Secondary School | facility-reconciliation.csv, id=X025, CSV data record 651 |
| X026 | Kanungu | Bushogye Seed Secondary School | facility-reconciliation.csv, id=X026, CSV data record 652 |
| X027 | Rukungiri | Bikurungu Seed Secondary School | facility-reconciliation.csv, id=X027, CSV data record 653 |
| X007 | Kasese | Rukoki General Hospital | facility-reconciliation.csv, id=X007, CSV data record 659 |
| X030 | Fort-Portal City | Bukuuku Community Seed Secondary School | facility-reconciliation.csv, id=X030, CSV data record 660 |
| X010 | Kakumiro | Silumira Health Centre III | facility-reconciliation.csv, id=X010, CSV data record 662 |
| X032 | Buvuma | Buvuma Health Centre III | facility-reconciliation.csv, id=X032, CSV data record 665 |
| X903 | Wakiso | Buloba Health Centre III | facility-reconciliation.csv, id=X903, CSV data record 666 |
| X033 | Lwengo | Lwengenyi Health Centre III | facility-reconciliation.csv, id=X033, CSV data record 667 |

## Omitted substantive claims

The following explained master cases do not support one of the six requested substantive reasons, so no replacement, absence, outside-programme status or asset relocation was inferred. Their coverage status remains as supplied in the source.

- H227, Yumbe, Lodonga TC: source verification `Case explained or reconciled; counted as completed`, decision `CHAT03`. Consult the exact CSV note; do not convert the case into a substantive reason.
- H044, Nakaseke, Butalangu HC II: source verification `Case explained or reconciled; counted as completed`, decision `CHAT41`. Consult the exact CSV note; do not convert the case into a substantive reason.
- H043, Nakaseke, Semuto HC II: source verification `Case explained or reconciled; counted as completed`, decision `CHAT41`. Consult the exact CSV note; do not convert the case into a substantive reason.
- S087, Nakaseke, Kikamulo: source verification `Case explained or reconciled; counted as completed`, decision `CHAT41`. Consult the exact CSV note; do not convert the case into a substantive reason.
- S088, Nakaseke, Nakaseke Seed School: source verification `Case explained or reconciled; counted as completed`, decision `CHAT41`. Consult the exact CSV note; do not convert the case into a substantive reason.
- S004, Nakaseke, Ngoma: source verification `Case explained or reconciled; counted as completed`, decision `CHAT36`. Consult the exact CSV note; do not convert the case into a substantive reason.
- H045, Nakasongola, Kiralamba HC II: source verification `Case explained or reconciled; counted as completed`, decision `CHAT41`. Consult the exact CSV note; do not convert the case into a substantive reason.
- S089, Nakasongola, Nakitoma: source verification `Case explained or reconciled; counted as completed`, decision `CHAT41`. Consult the exact CSV note; do not convert the case into a substantive reason.
- H370, Bundibugyo, Kyondo HC II: source verification `Case explained or reconciled; counted as completed`, decision `CHAT31`. Consult the exact CSV note; do not convert the case into a substantive reason.
- S059, Kabarole, Kichwamba: source verification `Case explained or reconciled; counted as completed`, decision `none`. Consult the exact CSV note; do not convert the case into a substantive reason.
- H373, Kasese, Kabingo HCII: source verification `Case explained or reconciled; counted as completed`, decision `CHAT27`. Consult the exact CSV note; do not convert the case into a substantive reason.
- S058, Fort-Portal City, Karago TC: source verification `Case explained or reconciled; counted as completed`, decision `none`. Consult the exact CSV note; do not convert the case into a substantive reason.
- S080, Lwengo, Lwengo Seed School: source verification `Case explained or reconciled; counted as completed`, decision `none`. Consult the exact CSV note; do not convert the case into a substantive reason.
- H031, Masaka, Kyabakuza HCII: source verification `Case explained or reconciled; counted as completed`, decision `CHAT45E`. Consult the exact CSV note; do not convert the case into a substantive reason.
- H048, Sembabule, Kyera HCII: source verification `Case explained or reconciled; counted as completed`, decision `CHAT45F`. Consult the exact CSV note; do not convert the case into a substantive reason.
- H047, Sembabule, Ntete HCII: source verification `Case explained or reconciled; counted as completed`, decision `CHAT45G`. Consult the exact CSV note; do not convert the case into a substantive reason.

The report also avoids asserting receiving facilities were physically verified solely because a receiving return exists. Lodonga TC (H227) is only reported not known to the district; it is not included in the nonexistence count. Alira is classified outside UgIFT under the later CHAT17 decision, not nonexistent under earlier CHAT10. Kyakatebe uses the later Namabaale rename. Bussi refers to already-listed Zinga and Loinya to already-listed Liko, without second facilities.

## Geography

- North, East and West labels normalized to Northern, Eastern and Western.
- Book-code case, hyphens and spacing normalized. Kasanda/Kassanda, Luwero/Luweero, Rakia/Rakai and Fortportal/Fort Portal normalized; no geographical change.
- The master Elgon grouping is split to Bugisu and Sebei using explicit consolidated field report table 2 rows 17 to 26. Bududa source Bukedi is corrected to Bugisu using table 2 row 20.
- Kween source schools say Eastern but health list says North. The Eastern placement follows master school table 1 rows 132 to 134 and the explicit Sebei grouping in consolidated field report table 2 row 24.
- Pader master classifications differ between Acholi and Lango. Acholi follows master school table 1 row 179 and roster table 1 row 22.
- Nwoya is assigned Acholi from the original WEMIS equipment archive hierarchy RC1/ACHOLI/Nwoya; the enclosed PDF confirms Nwoya District. The hierarchy, rather than PDF body text, supplies the sub-region. Omoro is assigned Acholi from the Abwoch toolkit table 1 row 3; other Omoro returns corroborate that sub-region.
- The requested separate Rwenzori and Tooro split is not supported by supplied district assignment sources: master uses Toro and roster uses Rwenzori / Tooro jointly. Report combines these groups.
- City and municipal book codes inherit their district region. Hoima City, Masaka City and Mbarara City use district and former municipality source rows. Koboko MC uses Koboko and roster row11. Fort Portal City/Fort Portal use explicit master Toro and roster row145.
- Makindye Ssabagabo MC spelling is matched to master Ssabagabo Makindye MC, table2 rows51 and357. Kiira MC is explicit in master table2 rows359-360.
- Bukomansimbi is absent from the master geography; roster table1 row170 places it under Greater Masaka. Central/Buganda follows the Masaka district master rows.
- KCCA is a national vote under REF Read Me row13 and its register Facility type MDA; no local-government geography extension is used.
- National code classification is subordinate to register Facility type. Hospital and Blood bank records belong to national scope irrespective of geographic city names.

Complete machine-readable mappings and record-specific evidence are in `tmp/narrative-report/reconciliation/geography.json`. CSV logical data record numbers exclude the header; multiline quoted cells mean physical text line numbers differ.


# Selected report photographs

Every selected image was visually inspected. Photographs were copied from the listed source without modifying any source. Cropping removes surplus wall, sky or floor; no retouching or content changes were made. All copies are JPEG, maximum 1600 pixels on the long side, and carry 200 dpi metadata.

## Source checks and exclusions

- No national-MDA photograph could be established from the supplied raw-data-grouped DOCX and loose image path inventories. National-related results were register spreadsheets or correspondence photographs, not safely attributable national asset photographs.
- Excluded KABAROLE LG ASST.VERIFICATION REPORT_105758 (2).docx: its image captions and checklist identify Kidubuli HC III, with Mayuge appearing in the local-government field, despite its Kabarole path. No location inference was made from that file.
- Nwoya photographs use Acholi in their captions. The original WEMIS DISTRICT EQUIPMENT.rar hierarchy places Nwoya under RC1/ACHOLI/Nwoya; the enclosed doc00036920260811110821.pdf, pages 1 to 3, identifies Nwoya District in distribution records and the delivery note. This programme-source location placement supports correction of the supplied school list and roster placement. The district report has a copied Pakwach title, but the individual facility headings and narrative identify the selected Nwoya facilities.
- Buildings are captioned as buildings, without inferring occupation or completion from the image. Medical equipment is captioned by visible type without inferring functionality from its appearance.

## P01: Science laboratory tables and stools at a seed secondary school, Kalangala District (Buganda).
- File: `outputs/narrative-report/figures/photo_01_central_laboratory_furniture.jpg`
- Source: `raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`
- Embedded position: word/media/image9.jpeg; body block 35; table not applicable.
- Source context: Body block 35: 5. Science laboratory tables and stools. Facility and local government from the containing folder.
- Suggested section: 7.3 Central
- Image size: 855 x 549 pixels.

## P02: Infant radiant warmer at a health centre, Makindye-Ssabagabo Municipal Council (Buganda).
- File: `outputs/narrative-report/figures/photo_02_central_infant_warmer.jpg`
- Source: `raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`
- Embedded position: word/media/image22.jpeg; body block 77; table not applicable.
- Source context: Body block 77, image22.jpeg, following the Kibiri Health Centre III report; document paragraphs 1, 5 and 6 identify the facility and location.
- Suggested section: 7.3 Central
- Image size: 963 x 1280 pixels.

## P03: Desktop computers and classroom furniture at a seed secondary school, Busia District (Bukedi).
- File: `outputs/narrative-report/figures/photo_03_eastern_school_computers.jpg`
- Source: `raw-data-grouped/team-13/Busia/Sikuda-Seed-Secondary-School/43_ict-room-desktop-computers_ref0257.jpg`
- Embedded position: Loose image; body block not applicable; table not applicable.
- Source context: Loose photograph; source filename identifies ICT room desktop computers; facility and district from source folders.
- Suggested section: 7.3 Eastern
- Image size: 1080 x 573 pixels.

## P04: Delivery bed with a torn mattress cover at a health centre, Busia District (Bukedi).
- File: `outputs/narrative-report/figures/photo_04_eastern_torn_bed_cover.jpg`
- Source: `raw-data-grouped/team-13/Busia/Majanji-HC-III/050_delivery-bed-with-torn-cover_ref20260827-0646.jpg`
- Embedded position: Loose image; body block not applicable; table not applicable.
- Source context: Loose photograph; source filename identifies delivery bed with torn cover; facility and district from source folders. Caption describes visible condition only.
- Suggested section: 7.5 Asset management practices and risks
- Image size: 1600 x 1200 pixels.

## P05: Buildings at a seed secondary school, Nwoya District (Acholi).
- File: `outputs/narrative-report/figures/photo_05_northern_school_buildings.jpg`
- Source: `raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`
- Embedded position: word/media/image14.jpeg; body block 107; table not applicable.
- Source context: Body block 107, image14.jpeg, under LUNGULU SEED SECONDARY SCHOOL NWOYA DISTRICT LOCAL GOVERNMENT (block 55), with field photographs following block 82. The section runs until Todora HC heading at block 117.
- Suggested section: 7.3 Northern
- Image size: 1040 x 406 pixels.

## P06: Health centre building, Nwoya District (Acholi).
- File: `outputs/narrative-report/figures/photo_06_northern_health_building.jpg`
- Source: `raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`
- Embedded position: word/media/image37.jpeg; body block 308; table not applicable.
- Source context: Body block 308, image37.jpeg, under GOT APWOYO HEALTH CENTRE III | NWOYA DISTRICT LOCAL GOVERNMENT heading at block 269.
- Suggested section: 7.3 Northern
- Image size: 948 x 567 pixels.

## P07: Boxed computers and related equipment in a seed school store, Nwoya District (Acholi).
- File: `outputs/narrative-report/figures/photo_07_northern_stored_computers.jpg`
- Source: `raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`
- Embedded position: word/media/image9.jpeg; body block 83; table not applicable.
- Source context: Body block 83, image9.jpeg, after Field photos block 82 within Lungulu school section. Block 62 states that desktop computers, surge protectors, printer and UPS units are stored in the school store awaiting power connection.
- Suggested section: 7.5 Asset management practices and risks
- Image size: 853 x 663 pixels.

## P08: Classroom desks at a seed secondary school, Ntoroko District (Tooro).
- File: `outputs/narrative-report/figures/photo_08_western_classroom_desks.jpg`
- Source: `raw-data-grouped/team-26/Ntoroko/Nombe-Seed-Secondary-School/NTOROKO ASSET NOMBE SEED SECONDARY SCHOOL VERIFICATION AND RECORDING TOOL KIT 222.docx`
- Embedded position: word/media/image4.jpeg; body block 110; table not applicable.
- Source context: Body block 110, image4.jpeg, after building inventory table at block 109. Caption at block 111: Main gate, Desks, Classroom. School interview block 54 identifies Nombe school; verification details table at block 29 identifies Western, Tooro, Ntoroko.
- Suggested section: 7.3 Western
- Image size: 607 x 508 pixels.

## P09: Delivery bed and clinical furniture at a health centre, Kabarole District (Tooro).
- File: `outputs/narrative-report/figures/photo_09_western_delivery_bed.jpg`
- Source: `raw-data-grouped/team-26/Kabarole/Iruhura-HC-III/KABAROLE DISTRICT   IRUHURA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222 (1).docx`
- Embedded position: word/media/image10.jpeg; body block 96; table not applicable.
- Source context: Body block 96, image10.jpeg; photograph group captions at blocks 100 to 101 include Delivery bed. Verification details table at block 29 identifies Western, Tooro, Kabarole; facility heading at block 38 and checklist heading at block 75 identify Iruhura HC III.
- Suggested section: 7.3 Western
- Image size: 577 x 594 pixels.

## P10: UgIFT identification on a desk at a seed school, Tororo District (Bukedi).
- File: `outputs/narrative-report/figures/photo_10_eastern_ugift_marking.jpg`
- Source: `raw-data-grouped/team-13/Tororo/Malaba-Seed-School/049_desk-engraving-gou-moh-ugift_ref20260829-0338.jpg`
- Embedded position: Loose image; body block not applicable; table not applicable.
- Source context: Loose photograph; source filename identifies desk engraving GOU MOH UGIFT; facility and district from source folders. The visible marking reads GOU/MOH-UGIFT PROJECT, F/Y 2023/2024.
- Suggested section: 7.5 Asset management practices and risks
- Image size: 922 x 518 pixels.

## Independent final-image review

All 10 final JPEG files were reopened at their original pixel sizes. No readable personal names, faces, badges, signatures or personal documents appeared. Computer screens carry no displayed content. The engraving close-up shows only the institutional marking and year. The national-source All WIP Ugift folder was also checked: no DOCX or loose photographs; its 7 PDF documents contain distribution lists, including 10 scanned MoWE pages with signatures, not asset photographs. The district-equipment archive was inventoried and the Nwoya distribution record inspected. See second_photo_qa.json for the PDF inventory.


## Points checked and not asserted in the report

- Physical verification facility total: README and facility-data-status distinguish accountability completion from inspection. 629 is master records accounted for, not a physical inspection count. 589 records have facility materials or consolidated-register entries; 40 are explained or reconciled.
- Extra physical facilities: the 24 X identities are ground-return names/identities, with aliases and district corrections possible. They are not presented as 24 confirmed new physical facilities.
- Condition assessment share: REF Read Me row14 says 37122 rows were classified Functional where no condition was recorded anywhere, and the Faulty class includes idle, stored, unseen, lost and other states. Therefore 94.0% is explicitly a register classification share, not a rate of assets assessed on the ground. The chart labels preserve Functional and Faulty and do not substitute non-functional for Faulty.
- Valuation basis: REF Read Me row41 applies comparators by item and by asset class, makes some price adjustments, and uses a UGX10000 rule; the prompt-only same-item wording is narrower than the workbook. The report uses accounting language that includes comparable asset classes and does not describe values as solely original facility costs. REF Read Me rows9,40,42,43 describe useful lives, dates and depreciation. Work in progress is kept in its stated cost basis.
- Separate Rwenzori and Tooro totals: supplied sources do not establish a defensible split, so the combined source-supported grouping is retained.
- National MDA photographs: inspected programme All WIP documents and asset-distribution scans contain no attributable usable asset photograph meeting the privacy rules. Ten regional photographs are used.
- National maintenance arrangements are included only where specific register remarks support them; the report makes no assumed servicing claims.

- The draft describes 13 MDAs in paragraph 140 but lists 15 in paragraph 146. The report preserves the complete visited list from paragraph 146 and does not repeat the conflicting 13 count.
- The draft itinerary has an empty eighth row, which has no activity and was not reproduced.
- The water and environment outputs sentence in draft paragraph 72 ends with 'in' and provides no geographic qualifier. Only its fully stated numeric outputs were retained.
- The programme output counts in section 6 describe the draft programme context, not the scope or totals of the September asset register. They must not substitute for register or reconciliation totals.
- The draft gives a general two day LG itinerary as well as a 10 working day collection period and the full 24 August to 7 September 2026 field window. These have different meanings and are retained with their stated labels.
- The draft describes six supervisory regions for field management; the report's statistical presentation uses four geographic regions required by the outline.
- The firm name in the draft includes personal names and is replaced by 'the Consultant'. Individual names, phone numbers and supervisor handles are excluded from all report prose.
- The two Kabarole _district-documents files named KABAROLE LG ASST.VERIFICATION REPORT contain Mayuge/Kidubuli narrative and one altered cover facility name. They were not used as Kabarole evidence.
- The Nwoya district report has a Pakwach label in its opening heading. The Nwoya observations cited here occur under named Nwoya facilities and identify Nwoya in the substantive paragraphs.
- No quantitative causal estimate of UgIFT impact is derived from interviews. Reported service changes are attributed to the facility interviews and not presented as independently measured programme effects.

## Geography mapping by book code

- `ABIM BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 142: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 143: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 144: Northern, Karamoja
- `ADJUMANI BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 197: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 198: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 207: Northern, West Nile
- `AGAGO BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 22: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 23: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 24: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 172: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 173: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 143: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 144: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 145: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 146: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 147: Northern, Acholi
- `ALEBTONG BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 180: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 181: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 161: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 162: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 163: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 164: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 165: Northern, Lango
- `AMOLATAR BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 28: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 182: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 183: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 166: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 167: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 168: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 169: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 170: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 171: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 365: Northern, Lango
- `AMUDAT BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 145: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 146: Northern, Karamoja
- `AMURIA BK`: Eastern / Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 158: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 138: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 139: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 140: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 141: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 142: Eastern, Teso
- `AMURU BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 25: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 174: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 148: Northern, Acholi
- `APAC BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 184: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 172: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 173: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 174: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 175: Northern, Lango
- `APAC MC BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 185: Northern, Lango
- `ARUA BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 31: Northern, West Nile
- `ARUA RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `BUDAKA BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 6: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 7: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 95: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 96: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 61: Eastern, Bukedi
- `BUDUDA BK`: Eastern / Bugisu; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 8: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 9: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 62: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 63: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 64: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 65: Eastern, Bukedi; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 20, Region group
- `BUGIRI BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 108: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 241: Eastern, Busoga
- `BUGIRI MC BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 80: Eastern, Busoga
- `BUGWERI BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 12: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 109: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 81: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 82: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 83: Eastern, Busoga
- `BUHWEJU BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 212: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 213: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 214: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 235: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 236: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 237: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 238: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 239: Western, Ankole
- `BUIKWE BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 228: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 56: Central, Buganda
- `BUKEDEA BK`: Eastern / Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 159: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 124: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 125: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 126: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 127: Eastern, Teso
- `BUKOMANSIMBI BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 83: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 32: Central, Buganda
- `BUKWO BK`: Eastern / Sebei; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 15: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 127: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 106: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 107: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 108: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 109: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 110: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 361: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 362: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 363: Eastern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 23, Region group
- `BULAMBULI BK`: Eastern / Bugisu; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 128: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 129: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 111: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 112: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 113: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 114: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 115: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 364: Eastern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 22, Region group
- `BULIISA BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 47: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 230: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 284: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 285: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 286: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 370: Western, Bunyoro
- `BUNDIBUGYO BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 55: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 56: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 251: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 319: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 320: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 321: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 322: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 323: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 324: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 371: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 372: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `BUNYANGABU BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 57: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 58: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 252: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 325: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 326: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 327: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `BUSHENYI BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 215: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 216: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 240: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 241: Western, Ankole
- `BUSIA BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 97: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 66: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 67: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 68: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 69: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 70: Eastern, Bukedi
- `BUTABIKA NRMH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `BUTALEJA BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 10: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 98: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 72: Eastern, Bukedi
- `BUTAMBALA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 46: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 229: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 2: Central, Buganda
- `BUTEBO BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 99: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 59: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 60: Eastern, Bukedi
- `BUVUMA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 65: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 3: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 4: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 5: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 6: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 7: Central, Buganda
- `BUYENDE BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 110: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 84: Eastern, Busoga
- `DOKOLO BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 186: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 187: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 176: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 177: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 178: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 179: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 180: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 181: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 182: Northern, Lango
- `ENTEBBE RH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `FORT PORTAL BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 59: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `FORT PORTAL CITY BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 328: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 329: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `FORT PORTAL RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `GOMBA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 66: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 8: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 9: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 10: Central, Buganda
- `GULU BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 26: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 175: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 149: Northern, Acholi
- `GULU RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `HOIMA BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 231: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 232: Western, Bunyoro
- `HOIMA CITY BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 231: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 232: Western, Bunyoro
- `HOIMA RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `IBANDA BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 39: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 217: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 242: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 243: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 244: Western, Ankole
- `IGANGA BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 111: Eastern, Busoga
- `ISINGIRO BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 218: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 245: Western, Ankole
- `JINJA BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 112: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 113: Eastern, Busoga
- `JINJA CITY BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 13: Eastern, Busoga
- `JINJA RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `KAABONG BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 20: Northern, Karamoja
- `KABALE BK`: Western / Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 242: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 304: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 305: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 306: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 307: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 308: Western, Kigezi
- `KABALE MC BK`: Western / Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 309: Western, Kigezi
- `KABALE RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `KABAROLE BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 60: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 253: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 330: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 331: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 332: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 333: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 334: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 335: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 336: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 373: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `KABERAMAIDO BK`: Eastern / Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 160: Eastern, Teso
- `KAGADI BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 48: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 49: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 50: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 233: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 288: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 289: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 290: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 291: Western, Bunyoro
- `KAKUMIRO BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 234: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 235: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 292: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 293: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 294: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 295: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 296: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 297: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 298: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 299: Western, Bunyoro
- `KALAKI BK`: Eastern / Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 161: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 162: Eastern, Teso
- `KALANGALA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 67: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 68: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 58: Central, Buganda
- `KALIRO BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 14: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 114: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 115: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 86: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 87: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 88: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 89: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 90: Eastern, Busoga
- `KALUNGU BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 69: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 57: Central, Buganda
- `KAMULI BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 116: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 117: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 118: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 91: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 92: Eastern, Busoga
- `KAMULI MC BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 93: Eastern, Busoga
- `KAMWENGE BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 254: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 337: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 338: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 339: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `KANUNGU BK`: Western / Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 243: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 310: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 311: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 312: Western, Kigezi
- `KAPCHORWA BK`: Eastern / Sebei; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 130: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 131: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 116: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 117: Eastern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 25, Region group
- `KAPCHORWA MC BK`: Eastern / Sebei; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 118: Eastern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 26, Region group
- `KAPELEBYONG BK`: Eastern / Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 128: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 129: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 130: Eastern, Teso
- `KARENGA BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 147: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 148: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 158: Northern, Karamoja
- `KASESE BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 61: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 340: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 341: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 342: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 343: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 344: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 374: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `KASSANDA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 70: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 71: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 11: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 12: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 13: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 14: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 15: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 16: Central, Buganda
- `KATAKWI BK`: Eastern / Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 163: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 164: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 131: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 132: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 133: Eastern, Teso
- `KAWEMPE RH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `KAYUNGA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 72: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 17: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 18: Central, Buganda
- `KAYUNGA RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `KAZO BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 40: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 246: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 247: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 248: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 249: Western, Ankole
- `KCCA BK`: National / National; REF workbook Read Me row13 central-government vote list; REF register remarks Facility type MDA
- `KIBAALE BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 236: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 237: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 300: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 301: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 302: Western, Bunyoro
- `KIBOGA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 2: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 73: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 19: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 20: Central, Buganda
- `KIBUKU BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 100: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 101: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 102: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 73: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 74: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 75: Eastern, Bukedi
- `KIIRA MC BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 359: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 360: Central, Buganda
- `KIKUUBE BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 51: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 238: Western, Bunyoro
- `KIRUDDU RH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `KIRUHURA BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 41: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 42: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 219: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 250: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 251: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 252: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 253: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 254: Western, Ankole
- `KIRYANDONGO BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 52: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 239: Western, Bunyoro
- `KISORO BK`: Western / Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 54: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 244: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 313: Western, Kigezi
- `KISORO MC BK`: Western / Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 314: Western, Kigezi
- `KITAGWENDA BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 255: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `KITGUM BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 176: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 177: Northern, Acholi
- `KOBOKO BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 32: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 199: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 208: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 209: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 210: Northern, West Nile
- `KOBOKO MC BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 32: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 199: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 208: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 209: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 210: Northern, West Nile
- `KOLE BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 188: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 189: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 183: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 184: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 185: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 186: Northern, Lango
- `KOTIDO BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 149: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 150: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 159: Northern, Karamoja
- `KUMI BK`: Eastern / Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 165: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 166: Eastern, Teso
- `KWANIA BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 190: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 187: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 188: Northern, Lango
- `KWEEN BK`: Eastern / Sebei; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 132: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 133: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 134: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 153: Northern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 154: Northern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 155: Northern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 156: Northern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 157: Northern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 24, Region group
- `KYANKWANZI BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 74: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 75: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 76: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 21: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 22: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 23: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 24: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 25: Central, Buganda
- `KYEGEGWA BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 256: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 257: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 346: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 347: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `KYENJOJO BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 62: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 258: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 259: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 348: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 349: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 350: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 351: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 352: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 353: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `KYOTERA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 77: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 26: Central, Buganda
- `LAMWO BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 27: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 178: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 151: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 152: Northern, Acholi
- `LIRA BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 191: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 192: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 189: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 190: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 191: Northern, Lango
- `LIRA CITY BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 366: Northern, Lango
- `LIRA RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `LUUKA BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 119: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 120: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 94: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 95: Eastern, Busoga
- `LUWEERO BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 78: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 79: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 27: Central, Buganda
- `LWENGO BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 80: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 81: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 28: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 29: Central, Buganda
- `LYANTONDE BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 3: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 82: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 30: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 31: Central, Buganda
- `MAAIF BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MADI OKOLLO BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 211: Northern, West Nile
- `MAKINDYE SSABAGABO MC BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 51: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 357: Central, Buganda
- `MANAFWA BK`: Eastern / Bugisu; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 16: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 17: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 135: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 136: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 137: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 119: Eastern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 19, Region group
- `MARACHA BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 33: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 200: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 212: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 213: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 214: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 215: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 216: Northern, West Nile
- `MASAKA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 83: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 32: Central, Buganda
- `MASAKA CITY BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 83: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 32: Central, Buganda
- `MASAKA RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MASINDI BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 53: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 240: Western, Bunyoro
- `MASINDI MC BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 303: Western, Bunyoro
- `MAYUGE BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 121: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 122: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 96: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 97: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 98: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 99: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 100: Eastern, Busoga
- `MBALE BK`: Eastern / Bugisu; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 18: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 138: Eastern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 17, Region group
- `MBALE RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MBARARA BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 220: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 221: Western, Ankole
- `MBARARA CITY BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 220: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 221: Western, Ankole
- `MBARARA RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MGLSD BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MITOOMA BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 222: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 223: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 256: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 257: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 258: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 259: Western, Ankole
- `MITYANA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 84: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 34: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 35: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 36: Central, Buganda
- `MODV BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MOES BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MOFPED BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MOH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MOLG BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MOLHUD BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MOROTO BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 151: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 152: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 160: Northern, Karamoja
- `MOROTO RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MOWE BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MOWT BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MOYO BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 201: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 217: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 218: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 367: Northern, West Nile
- `MPIGI BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 85: Central, Buganda
- `MUBENDE BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 4: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 86: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 37: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 38: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 39: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 40: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 41: Central, Buganda
- `MUBENDE MC BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 42: Central, Buganda
- `MUBENDE RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `MUKONO BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 87: Central, Buganda
- `MUKONO MC BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 43: Central, Buganda
- `MULAGO NRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `NABILATUK BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 153: Northern, Karamoja
- `NAGURU RH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `NAKAPIRIPIRIT BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 21: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 154: Northern, Karamoja
- `NAKASEKE BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 5: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 88: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 89: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 44: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 45: Central, Buganda
- `NAKASONGOLA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 90: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 46: Central, Buganda
- `NAMAYINGO BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 123: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 124: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 101: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 102: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 103: Eastern, Busoga
- `NAMISINDWA BK`: Eastern / Bugisu; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 19: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 139: Eastern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 18, Region group
- `NAMUTUMBA BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 125: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 126: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 104: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 105: Eastern, Busoga
- `NANSANA MC BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 356: Central, Buganda
- `NAPAK BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 155: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 156: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 157: Northern, Karamoja
- `NEBBI BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 34: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 35: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 202: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 219: Northern, West Nile
- `NEMA BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `NGORA BK`: Eastern / Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 167: Eastern, Teso
- `NTOROKO BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 63: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 64: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 260: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 354: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 355: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `NTUNGAMO BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 43: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 44: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 224: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 260: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 261: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 262: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 263: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 264: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 265: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 266: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 267: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 268: Western, Ankole
- `NTUNGAMO MC BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 269: Western, Ankole
- `NWOYA BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 36: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 203: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 220: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 221: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 222: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 223: Northern, West Nile; raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/WEMIS DISTRICT EQUIPMENT.rar :: WEMIS DISTRICT EQUIPMENT/RC1/ACHOLI/Nwoya/doc00036920260811110821.pdf, original archive hierarchy ACHOLI/Nwoya; enclosed three-page record identifies Nwoya District
- `OAG BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `OBONGI BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 204: Northern, West Nile
- `OMORO BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 205: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 224: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 225: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 226: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 368: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 369: Northern, West Nile; raw-data-grouped/team-05/Omoro/Abwoch-HC-III/Abwoch HC III_ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx, table 1 row 3: SUB-REGION ACHOLI
- `OPM BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `OTUKE BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 29: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 194: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 192: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 193: Northern, Lango
- `OYAM BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 30: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 195: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 194: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 195: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 196: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 197: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 198: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 199: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 200: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 201: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 202: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 203: Northern, Lango
- `PADER BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 179: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 196: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 204: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 205: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 206: Northern, Lango; raw-data-grouped/team-04/Pader/Lapul-Ocwida-HC-III/1 Lapulocwida HC - Pader District.docx, table 1 row 3: SUB-REGION ACHOLI
- `PAKWACH BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 206: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 207: Northern, West Nile
- `PALLISA BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 103: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 104: Eastern, Bukedi
- `PPDA BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `RAKAI BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 91: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 92: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 47: Central, Buganda
- `RUBANDA BK`: Western / Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 245: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 246: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 315: Western, Kigezi
- `RUBIRIZI BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 45: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 225: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 270: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 271: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 272: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 273: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 274: Western, Ankole
- `RUKIGA BK`: Western / Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 247: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 248: Western, Kigezi
- `RUKUNGIRI BK`: Western / Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 249: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 250: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 316: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 317: Western, Kigezi
- `RUKUNGIRI MC BK`: Western / Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 318: Western, Kigezi
- `RWAMPARA BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 275: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 276: Western, Ankole
- `SEMBABULE BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 93: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 48: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 49: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 50: Central, Buganda
- `SERERE BK`: Eastern / Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 168: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 169: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 134: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 135: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 136: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 137: Eastern, Teso
- `SHEEMA BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 226: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 227: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 277: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 278: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 279: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 280: Western, Ankole
- `SHEEMA MC BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 281: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 282: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 283: Western, Ankole
- `SIRONKO BK`: Eastern / Bugisu; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 140: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 141: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 120: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 121: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 122: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 123: Eastern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 21, Region group
- `SOROTI BK`: Eastern / Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 170: Eastern, Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 171: Eastern, Teso
- `SOROTI RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `TEREGO BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 227: Northern, West Nile
- `TORORO BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 105: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 106: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 107: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 76: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 77: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 79: Eastern, Bukedi
- `TORORO MC BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 11: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 78: Eastern, Bukedi
- `UBTS BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `WAKISO BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 94: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 52: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 53: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 54: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 55: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 358: Central, Buganda
- `YUMBE BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 37: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 38: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 208: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 228: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 229: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 230: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 231: Northern, West Nile
- `YUMBE RRH BK`: National / National; BOOK_TYPE_CODE.md; MDA / Hospital / Blood bank status governs national presentation
- `ZOMBO BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 209: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 210: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 211: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 232: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 233: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 234: Northern, West Nile

## Sharing and custody count evidence

{
  "count": 42,
  "unit": "Distinct BOOK_TYPE_CODE plus facility identities in the asset register",
  "by_region": {
    "Western": 17,
    "Central": 2,
    "Northern": 12,
    "Eastern": 11
  },
  "facilities": [
    {
      "book": "KASESE BK",
      "facility": "Railway Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Transferred to Kasese Municipal Council",
      "rows": [
        2176
      ],
      "source_file": "_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls",
      "source_locator": "UGIFT HEALTH row 4405",
      "evidence": [
        {
          "register_row": 2176,
          "source_file": "_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls",
          "source_locator": "UGIFT HEALTH row 4405",
          "wording": "Functional; Transferred to kasese municipal counsel ii; "
        }
      ]
    },
    {
      "book": "KAKUMIRO BK",
      "facility": "Mukoora Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Asset taken to the district health office",
      "rows": [
        4899
      ],
      "source_file": "_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls",
      "source_locator": "UGIFT HEALTH row 9248",
      "evidence": [
        {
          "register_row": 4899,
          "source_file": "_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls",
          "source_locator": "UGIFT HEALTH row 9248",
          "wording": "Was taken to DHO office; Received one and was requested by the DHO.; Source status: Was taken to DHO office; "
        }
      ]
    },
    {
      "book": "KASESE BK",
      "facility": "Bwesumbu Seed Secondary School",
      "region": "Western",
      "kind": "School",
      "reason": "Held at district stores",
      "rows": [
        5964
      ],
      "source_file": "_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls",
      "source_locator": "IGIFT EDUCATION row 674",
      "evidence": [
        {
          "register_row": 5964,
          "source_file": "_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls",
          "source_locator": "IGIFT EDUCATION row 674",
          "wording": "Functional; All still in good condition at the district stores; "
        }
      ]
    },
    {
      "book": "KYANKWANZI BK",
      "facility": "Mujunza Health Centre III",
      "region": "Central",
      "kind": "Health centre",
      "reason": "Asset taken to district",
      "rows": [
        6604
      ],
      "source_file": "_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls",
      "source_locator": "UGIFT HEALTH 2 row 778",
      "evidence": [
        {
          "register_row": 6604,
          "source_file": "_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls",
          "source_locator": "UGIFT HEALTH 2 row 778",
          "wording": "Functional; Received 2 pieces and 1 was taken to the District during the presidential tour; "
        }
      ]
    },
    {
      "book": "KAKUMIRO BK",
      "facility": "Silumira Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Beds given to Mwangi Health Centre III and held at district store",
      "rows": [
        6821
      ],
      "source_file": "_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls",
      "source_locator": "UGIFT HEALTH 2 row 1092",
      "evidence": [
        {
          "register_row": 6821,
          "source_file": "_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls",
          "source_locator": "UGIFT HEALTH 2 row 1092",
          "wording": "Functional; Found 17 beds in use. The facility gave out 3 beds to Mwangi HC III and 4 beds are still at the District store; "
        }
      ]
    },
    {
      "book": "YUMBE BK",
      "facility": "Amanyiri Health Centre III",
      "region": "Northern",
      "kind": "Health centre",
      "reason": "Held at district",
      "rows": [
        29536,
        29537,
        29538,
        29539,
        29540,
        29541,
        29542,
        29543,
        29544,
        29545,
        29546,
        29547,
        29548,
        29549,
        29550,
        29551,
        29552,
        29553,
        29554,
        29555,
        29556,
        29557,
        29558,
        29559,
        29560,
        29561,
        29562,
        29563,
        29564,
        29565,
        29566,
        29567,
        29568,
        29572,
        29573,
        29574,
        29575,
        29576,
        29577,
        29578,
        29579,
        29580,
        29581,
        29582,
        29583,
        29588,
        29589,
        29590,
        29591,
        29592,
        29593,
        29596,
        29597
      ],
      "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
      "source_locator": "Sheet1 row 2144",
      "evidence": [
        {
          "register_row": 29536,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2144",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29537,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2145",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29538,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2146",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29539,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2147",
          "wording": "Functional; Kept at the District; Engraving: Not engraved -; "
        },
        {
          "register_row": 29540,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2148",
          "wording": "Functional; Kept at the District; Engraving: Not engraved -; "
        },
        {
          "register_row": 29541,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2149",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29542,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2150",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29543,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2151",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29544,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2152",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29545,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2153",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29546,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2154",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29547,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2155",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29548,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2156",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29549,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2157",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29550,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2158",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29551,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2159",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29552,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2160",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29553,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2161",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29554,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2162",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29555,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2163",
          "wording": "Functional; Kept at the District; "
        },
        {
          "register_row": 29556,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2164",
          "wording": "Still in tacked; Kept at the District; Source status: Still in tacked; "
        },
        {
          "register_row": 29557,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2165",
          "wording": "Still in tacked; Kept at the District; Source status: Still in tacked; "
        },
        {
          "register_row": 29558,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2166",
          "wording": "Still packed at the district; Kept at the District; Source status: Still packed at the district; "
        },
        {
          "register_row": 29559,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2167",
          "wording": "Still packed at the district; Kept at the District; Source status: Still packed at the district; "
        },
        {
          "register_row": 29560,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2168",
          "wording": "Still packed at the district; Kept at the District; Source status: Still packed at the district; "
        },
        {
          "register_row": 29561,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2169",
          "wording": "Still packed at the district; Kept at the District; Source status: Still packed at the district; "
        },
        {
          "register_row": 29562,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2170",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29563,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2171",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29564,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2172",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29565,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2173",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29566,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2174",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29567,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx; team-02/Yumbe/Amanyiri-HC-III/1 AMANYIRI HCIII.docx",
          "source_locator": "Sheet1 row 2175",
          "wording": "Functional; Kept at the District; Cost: Not indicated at the records; "
        },
        {
          "register_row": 29568,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx; team-02/Yumbe/Amanyiri-HC-III/1 AMANYIRI HCIII.docx",
          "source_locator": "Sheet1 row 2176",
          "wording": "Functional; Kept at the District; Cost: Not indicated at the records; "
        },
        {
          "register_row": 29572,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2180",
          "wording": "packed; Kept at the District; Source status: packed; "
        },
        {
          "register_row": 29573,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2181",
          "wording": "packed; Kept at the District; Source status: packed; "
        },
        {
          "register_row": 29574,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2182",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29575,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2183",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29576,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2184",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29577,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2185",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29578,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2186",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29579,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2187",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29580,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2188",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29581,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2189",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29582,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2190",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29583,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2191",
          "wording": "Packed; Kept at the District; Source status: Packed; "
        },
        {
          "register_row": 29588,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2196",
          "wording": "Functional; Kept at district; Engraving: Not t engraved; "
        },
        {
          "register_row": 29589,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2197",
          "wording": "Functional; Kept at district; Engraving: Not t engraved; "
        },
        {
          "register_row": 29590,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2198",
          "wording": "Functional; Kept at district; Engraving: Not t engraved; "
        },
        {
          "register_row": 29591,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2199",
          "wording": "Functional; Kept at district; Engraving: Not t engraved; "
        },
        {
          "register_row": 29592,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2200",
          "wording": "Functional; Kept at district; Engraving: Not t engraved; "
        },
        {
          "register_row": 29593,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2201",
          "wording": "Functional; Kept at district; Engraving: Not t engraved; "
        },
        {
          "register_row": 29596,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2204",
          "wording": "Functional; Kept at district; Engraving: Not t engraved; "
        },
        {
          "register_row": 29597,
          "source_file": "_multi-team/teams-01-04/Health 6.xlsx",
          "source_locator": "Sheet1 row 2205",
          "wording": "Functional; Kept at district; Engraving: Not t engraved; "
        }
      ]
    },
    {
      "book": "MITOOMA BK",
      "facility": "Mayanga Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Transferred to Rutookye Health Centre III",
      "rows": [
        30970
      ],
      "source_file": "_multi-team/teams-19-21/data updates - western.xls",
      "source_locator": "Sheet3 row 119",
      "evidence": [
        {
          "register_row": 30970,
          "source_file": "_multi-team/teams-19-21/data updates - western.xls",
          "source_locator": "Sheet3 row 119",
          "wording": "Functional; 10 received 1 transferred to rutookye H/C III; "
        }
      ]
    },
    {
      "book": "ZOMBO BK",
      "facility": "Amei Seed Secondary School",
      "region": "Northern",
      "kind": "School",
      "reason": "Boxed at district store",
      "rows": [
        33281,
        33282,
        33283,
        33284,
        33286,
        33287,
        33288,
        33289,
        33290,
        33291,
        33292,
        33293,
        33294,
        33295,
        33296
      ],
      "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
      "source_locator": "Table 12 row 2",
      "evidence": [
        {
          "register_row": 33281,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 2",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33282,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 3",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33283,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 4",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33284,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 5",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33286,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 6",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33287,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 7",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33288,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 8",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33289,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 9",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33290,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 10",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33291,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 12",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33292,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 13",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33293,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 14",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33294,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 15",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33295,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 16",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 33296,
          "source_file": "team-01/Nwoya/Got-Apwoyo-HC-III/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "source_locator": "Table 12 row 17",
          "wording": "Functional; Still boxed at the district store; "
        }
      ]
    },
    {
      "book": "ZOMBO BK",
      "facility": "Kango Seed Secondary School",
      "region": "Northern",
      "kind": "School",
      "reason": "Boxed at district store",
      "rows": [
        34585,
        34586,
        34587,
        34588,
        34590,
        34591,
        34592,
        34593,
        34594,
        34595,
        34596,
        34597,
        34598,
        34599,
        34600
      ],
      "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
      "source_locator": "Table 12 row 2",
      "evidence": [
        {
          "register_row": 34585,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 2",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34586,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 3",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34587,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 4",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34588,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 5",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34590,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 6",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34591,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 7",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34592,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 8",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34593,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 9",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34594,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 10",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34595,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 12",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34596,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 13",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34597,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 14",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34598,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 15",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34599,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 16",
          "wording": "Functional; Still boxed at the district store; "
        },
        {
          "register_row": 34600,
          "source_file": "team-01/Nwoya/Paraa-HC-III/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx",
          "source_locator": "Table 12 row 17",
          "wording": "Functional; Still boxed at the district store; "
        }
      ]
    },
    {
      "book": "KOBOKO MC BK",
      "facility": "Nyangilia Health Centre III",
      "region": "Northern",
      "kind": "Health centre",
      "reason": "Held at district stores",
      "rows": [
        37838
      ],
      "source_file": "team-02/Koboko MC/Nyangilia-HC-III/1 NYANGILIA HC Koboko Municiplaity.docx",
      "source_locator": "Table 6 row 206",
      "evidence": [
        {
          "register_row": 37838,
          "source_file": "team-02/Koboko MC/Nyangilia-HC-III/1 NYANGILIA HC Koboko Municiplaity.docx",
          "source_locator": "Table 6 row 206",
          "wording": "Functional; 2 IN USE 1 AT DISTRICT STORES; "
        }
      ]
    },
    {
      "book": "KOBOKO BK",
      "facility": "Chakulia Health Centre III",
      "region": "Northern",
      "kind": "Health centre",
      "reason": "Taken to Koboko Hospital",
      "rows": [
        37965
      ],
      "source_file": "team-02/Koboko/Chakulia-HC-III/1 CHAKULIA HC - Padrombu SSS ASSET.docx",
      "source_locator": "Table 6 row 134",
      "evidence": [
        {
          "register_row": 37965,
          "source_file": "team-02/Koboko/Chakulia-HC-III/1 CHAKULIA HC - Padrombu SSS ASSET.docx",
          "source_locator": "Table 6 row 134",
          "wording": "Functional; 1 IN USE I TAKEN TO KOBOKO HOSPITAL; "
        }
      ]
    },
    {
      "book": "MARACHA BK",
      "facility": "Kololo Seed Secondary School",
      "region": "Northern",
      "kind": "School",
      "reason": "Held at district office",
      "rows": [
        40786,
        40814,
        40815,
        40816,
        40826,
        40854,
        40882,
        40883,
        40885,
        40887
      ],
      "source_file": "team-02/Maracha/Kololo-Seed-Secondary-School/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
      "source_locator": "Table 12 row 2",
      "evidence": [
        {
          "register_row": 40786,
          "source_file": "team-02/Maracha/Kololo-Seed-Secondary-School/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
          "source_locator": "Table 12 row 2",
          "wording": "Functional; Kept at District office; "
        },
        {
          "register_row": 40814,
          "source_file": "team-02/Maracha/Kololo-Seed-Secondary-School/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
          "source_locator": "Table 12 row 3",
          "wording": "Functional; Kept at District office; "
        },
        {
          "register_row": 40815,
          "source_file": "team-02/Maracha/Kololo-Seed-Secondary-School/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
          "source_locator": "Table 12 row 4",
          "wording": "Functional; Kept at District office; "
        },
        {
          "register_row": 40816,
          "source_file": "team-02/Maracha/Kololo-Seed-Secondary-School/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
          "source_locator": "Table 12 row 5",
          "wording": "Functional; Kept at District office; "
        },
        {
          "register_row": 40826,
          "source_file": "team-02/Maracha/Kololo-Seed-Secondary-School/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
          "source_locator": "Table 12 row 6",
          "wording": "Functional; Kept at District office; "
        },
        {
          "register_row": 40854,
          "source_file": "team-02/Maracha/Kololo-Seed-Secondary-School/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
          "source_locator": "Table 12 row 7",
          "wording": "Functional; Kept at District office; "
        },
        {
          "register_row": 40882,
          "source_file": "team-02/Maracha/Kololo-Seed-Secondary-School/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
          "source_locator": "Table 12 row 8",
          "wording": "Functional; Kept at District office; "
        },
        {
          "register_row": 40883,
          "source_file": "team-02/Maracha/Kololo-Seed-Secondary-School/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
          "source_locator": "Table 12 row 10",
          "wording": "Functional; Kept at District office; "
        },
        {
          "register_row": 40885,
          "source_file": "team-02/Maracha/Kololo-Seed-Secondary-School/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
          "source_locator": "Table 12 row 11",
          "wording": "Functional; Kept at District office; "
        },
        {
          "register_row": 40887,
          "source_file": "team-02/Maracha/Kololo-Seed-Secondary-School/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
          "source_locator": "Table 12 row 12",
          "wording": "Functional; Kept at District office; "
        }
      ]
    },
    {
      "book": "YUMBE BK",
      "facility": "Kerwa Seed Secondary School",
      "region": "Northern",
      "kind": "School",
      "reason": "Held in district store",
      "rows": [
        42555,
        42556,
        42557,
        42559,
        42560,
        42561,
        42562,
        42563,
        42564,
        42565,
        42566,
        42567,
        42568,
        42569,
        42570
      ],
      "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
      "source_locator": "Table 12 row 2",
      "evidence": [
        {
          "register_row": 42555,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 2",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42556,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 3",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42557,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 4",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42559,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 5",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42560,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 6",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42561,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 7",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42562,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 8",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42563,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 10",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42564,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 11",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42565,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 12",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42566,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 13",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42567,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 14",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42568,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 15",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42569,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 16",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        },
        {
          "register_row": 42570,
          "source_file": "team-02/Yumbe/Kerwa-HC-III/1 Kerwa HC - Kerwa SSS.docx",
          "source_locator": "Table 12 row 17",
          "wording": "Functional; ALL IN DISTRICT STORE; "
        }
      ]
    },
    {
      "book": "AGAGO BK",
      "facility": "Lamiyo Seed Secondary School",
      "region": "Northern",
      "kind": "School",
      "reason": "ICT held at Agago district store",
      "rows": [
        49714
      ],
      "source_file": "team-04/Agago/Lamiyo-HC-III/1 LAMIYO HC III AND LAMIYO SSS.docx",
      "source_locator": "Table 12 row 3",
      "evidence": [
        {
          "register_row": 49714,
          "source_file": "team-04/Agago/Lamiyo-HC-III/1 LAMIYO HC III AND LAMIYO SSS.docx",
          "source_locator": "Table 12 row 3",
          "wording": "good and functional; NB. ALL ICT Equipment Still at district store of agago LG headquarters; Source status: good and functional; "
        }
      ]
    },
    {
      "book": "OMORO BK",
      "facility": "Loyoajonga Health Centre III",
      "region": "Northern",
      "kind": "Health centre",
      "reason": "Transferred to Lalogi Health Centre III",
      "rows": [
        55284
      ],
      "source_file": "team-05/_team-documents/team five hospitals.xlsx",
      "source_locator": "Sheet1 row 3139",
      "evidence": [
        {
          "register_row": 55284,
          "source_file": "team-05/_team-documents/team five hospitals.xlsx",
          "source_locator": "Sheet1 row 3139",
          "wording": "Functional; Transferred to Lalogi HC III 01; "
        }
      ]
    },
    {
      "book": "OMORO BK",
      "facility": "Tekulu Health Centre III",
      "region": "Northern",
      "kind": "Health centre",
      "reason": "Microscope held at district headquarters for repair",
      "rows": [
        55360
      ],
      "source_file": "team-05/_team-documents/team five hospitals.xlsx",
      "source_locator": "Sheet1 row 3272",
      "evidence": [
        {
          "register_row": 55360,
          "source_file": "team-05/_team-documents/team five hospitals.xlsx",
          "source_locator": "Sheet1 row 3272",
          "wording": "Faulty; The microscope was delivered but it was taken to the district headquarters for repair .; "
        }
      ]
    },
    {
      "book": "KAPELEBYONG BK",
      "facility": "Akoromit Health Centre III",
      "region": "Eastern",
      "kind": "Health centre",
      "reason": "Taken to Acowa Health Centre III",
      "rows": [
        75579,
        75786,
        81657
      ],
      "source_file": "team-08/_team-documents/TEAM EIGHT HOSPITAL FACILITIES.xlsx",
      "source_locator": "Sheet1 row 1768",
      "evidence": [
        {
          "register_row": 75579,
          "source_file": "team-08/_team-documents/TEAM EIGHT HOSPITAL FACILITIES.xlsx",
          "source_locator": "Sheet1 row 1768",
          "wording": "4 in use; 1 taken to acowa HCIII and in good state; Source status: 4 in use; "
        },
        {
          "register_row": 75786,
          "source_file": "team-08/_team-documents/TEAM EIGHT HOSPITAL FACILITIES.xlsx",
          "source_locator": "Sheet1 row 1925",
          "wording": "1 in use; 1 taken to acowa hc III; Source status: 1 in use; "
        },
        {
          "register_row": 81657,
          "source_file": "team-08/Kapelebyong/Akoromit-HC-III/AKOROMIT HEALTH CENTRE III ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx",
          "source_locator": "Table 6 row 75",
          "wording": "Functional; 1 taken to acowa HCIII and in good state; "
        }
      ]
    },
    {
      "book": "KABERAMAIDO BK",
      "facility": "Aperikira Seed Secondary School",
      "region": "Eastern",
      "kind": "School",
      "reason": "Held at district stores before school delivery",
      "rows": [
        86796,
        86797,
        86798,
        86799,
        86800,
        86801,
        86802,
        86803,
        86804,
        86805,
        86806,
        86807,
        86808,
        86809,
        86810,
        86811,
        86812,
        86813,
        86814,
        86815,
        86816,
        86817,
        86818,
        86819,
        86820,
        86821,
        86822,
        86823,
        86824,
        86825,
        86826,
        86827,
        86828,
        86829,
        86830,
        86831,
        86832,
        86833,
        86834,
        86835,
        86836,
        86837,
        86838,
        86839,
        86840,
        86841,
        86842,
        86843,
        86844,
        86845,
        86846,
        86847,
        86848,
        86849,
        86850,
        86851,
        86852,
        86853,
        86854,
        86855,
        86856,
        86857,
        86858,
        86859,
        86860,
        86861,
        86862,
        86863,
        86864,
        86865,
        86866,
        86867,
        86868,
        86869,
        86870,
        86871,
        86872,
        86873,
        86874,
        86875,
        86876,
        86877,
        86878,
        86879,
        86880,
        86881,
        86882,
        86883,
        86884,
        86885,
        86886,
        86887,
        86888,
        86889,
        86890,
        86891,
        86892,
        86893,
        86894,
        86895,
        86896,
        86897,
        86898,
        86899,
        86900,
        86901,
        86902,
        86903,
        86904,
        86905,
        86906,
        86907,
        86908,
        86909,
        86910,
        86911,
        86912,
        86913,
        86914,
        86915,
        86916,
        86917,
        86918,
        86919,
        86920,
        86921,
        86922,
        86923,
        86924,
        86925,
        95243,
        95244
      ],
      "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
      "source_locator": "Sheet1 row 2340",
      "evidence": [
        {
          "register_row": 86796,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2340",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86797,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2341",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86798,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2342",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86799,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2343",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86800,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2344",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86801,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2345",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86802,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2346",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86803,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2347",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86804,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2348",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86805,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2349",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86806,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2350",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86807,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2351",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86808,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2352",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86809,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2353",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86810,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2354",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86811,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2355",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86812,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2356",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86813,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2357",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86814,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2358",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86815,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2359",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86816,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2361",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86817,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2362",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86818,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2363",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86819,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2364",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86820,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2365",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86821,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2366",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86822,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2367",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86823,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2368",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86824,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2369",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86825,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2370",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86826,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2371",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86827,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2372",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86828,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2373",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86829,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2374",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86830,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2375",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86831,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2376",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86832,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2377",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86833,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2378",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86834,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2379",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86835,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2380",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86836,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2382",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86837,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2383",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86838,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2384",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86839,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2385",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86840,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2386",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86841,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2387",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86842,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2388",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86843,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2389",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86844,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2390",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86845,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2391",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86846,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2392",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86847,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2393",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86848,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2394",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86849,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2395",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86850,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2396",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86851,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2397",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86852,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2398",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86853,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2399",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86854,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2400",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86855,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2401",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86856,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2403",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86857,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2404",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86858,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2405",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86859,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2406",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86860,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2407",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86861,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2408",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86862,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2409",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86863,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2410",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86864,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2411",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86865,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2412",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86866,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2413",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86867,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2414",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86868,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2415",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86869,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2416",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86870,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2417",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86871,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2418",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86872,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2419",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86873,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2420",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86874,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2421",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86875,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2422",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86876,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2423",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86877,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2424",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86878,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2425",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86879,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2427",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86880,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2429",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86881,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2430",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86882,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2431",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86883,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2432",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86884,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2433",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86885,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2434",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86886,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2435",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86887,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2436",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86888,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2437",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86889,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2438",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86890,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2439",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86891,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2440",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86892,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2441",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86893,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2442",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86894,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2443",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86895,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2444",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86896,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2445",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86897,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2446",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86898,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2447",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86899,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2448",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86900,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2450",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86901,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2451",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86902,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2452",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86903,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2453",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86904,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2454",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86905,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2456",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86906,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2457",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86907,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2458",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86908,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2459",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86909,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2461",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86910,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2462",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86911,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2463",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86912,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2464",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86913,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2465",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86914,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2466",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86915,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2467",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86916,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2468",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86917,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2469",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86918,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2470",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86919,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2471",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86920,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2472",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86921,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2474",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86922,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2475",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86923,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2476",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86924,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2477",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 86925,
          "source_file": "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx",
          "source_locator": "Sheet1 row 2478",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 95243,
          "source_file": "team-09/Kaberamaido/Aperikira-Seed-Secondary-School/APERIKIRA SEED SCHOOL ASSET VERIFICATION.docx",
          "source_locator": "Table 7 row 8",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 95244,
          "source_file": "team-09/Kaberamaido/Aperikira-Seed-Secondary-School/APERIKIRA SEED SCHOOL ASSET VERIFICATION.docx",
          "source_locator": "Table 7 row 19",
          "wording": "Not in use; Not delivered to the school, still at the district stores.; Source status: Not in use; "
        }
      ]
    },
    {
      "book": "AMUDAT BK",
      "facility": "Looro Seed Secondary School",
      "region": "Northern",
      "kind": "School",
      "reason": "ICT held at district headquarters during construction",
      "rows": [
        102950
      ],
      "source_file": "team-10/Amudat/Looro-Seed-Secondary-School/Asset-Verification-Toolkit.docx",
      "source_locator": "Table 12 row 2",
      "evidence": [
        {
          "register_row": 102950,
          "source_file": "team-10/Amudat/Looro-Seed-Secondary-School/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 2",
          "wording": "Functional; The rest of the ICT items are still at the district headquarters since the school is still under construction.; "
        }
      ]
    },
    {
      "book": "NAKAPIRIPIRIT BK",
      "facility": "Moruita Seed Secondary School",
      "region": "Northern",
      "kind": "School",
      "reason": "ICT held at district headquarters",
      "rows": [
        104153
      ],
      "source_file": "team-10/Nakapiripirit/Moruita-Seed-Secondary-School/Asset-Verification-Toolkit.docx",
      "source_locator": "Table 12 row 2",
      "evidence": [
        {
          "register_row": 104153,
          "source_file": "team-10/Nakapiripirit/Moruita-Seed-Secondary-School/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 2",
          "wording": "Functional; Helping the head teacher on office work. Most of the ICT items are still at the district headquarters since the school is opening officially in 2027.; "
        }
      ]
    },
    {
      "book": "BUSIA BK",
      "facility": "Bumunji Health Centre III",
      "region": "Eastern",
      "kind": "Health centre",
      "reason": "Taken to Masafu Hospital",
      "rows": [
        114617,
        114667,
        114674,
        114704,
        114713,
        114742
      ],
      "source_file": "team-13/Busia/Bumunji-HC-III/Asset-Verification-Toolkit.docx",
      "source_locator": "Table 6 row 61",
      "evidence": [
        {
          "register_row": 114617,
          "source_file": "team-13/Busia/Bumunji-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 61",
          "wording": "Functional; They had one but it was taken to Masafu Hospital.; "
        },
        {
          "register_row": 114667,
          "source_file": "team-13/Busia/Bumunji-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 103",
          "wording": "Good working condition; Some are kept in store and others were taken to Masafu. Margin: store.; Source status: Good working condition; "
        },
        {
          "register_row": 114674,
          "source_file": "team-13/Busia/Bumunji-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 111",
          "wording": "Good working condition; Functional in OPD but the other one was taken to Masafu Hospital. Margin quantity written as '2 1'.; Source status: Good working condition; "
        },
        {
          "register_row": 114704,
          "source_file": "team-13/Busia/Bumunji-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 136",
          "wording": "Functional; There were 2 oxygen therapy apparatus and they were taken to Masafu Hospital.; "
        },
        {
          "register_row": 114713,
          "source_file": "team-13/Busia/Bumunji-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 144",
          "wording": "Functional; Was taken to Masafu Hospital; they do not have it.; "
        },
        {
          "register_row": 114742,
          "source_file": "team-13/Busia/Bumunji-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 229",
          "wording": "Functional; It was one and it was taken to Masafu Hospital. Margin: store.; "
        }
      ]
    },
    {
      "book": "BUSIA BK",
      "facility": "Majanji Health Centre III",
      "region": "Eastern",
      "kind": "Health centre",
      "reason": "Taken to Masafu Hospital",
      "rows": [
        115178,
        115223
      ],
      "source_file": "team-13/Busia/Majanji-HC-III/Asset-Verification-Toolkit.docx",
      "source_locator": "Table 6 row 138",
      "evidence": [
        {
          "register_row": 115178,
          "source_file": "team-13/Busia/Majanji-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 138",
          "wording": "Faulty; Not found; taken to Masafu.; "
        },
        {
          "register_row": 115223,
          "source_file": "team-13/Busia/Majanji-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 229",
          "wording": "Functional; Taken to Masafu Hospital.; "
        }
      ]
    },
    {
      "book": "MANAFWA BK",
      "facility": "Butta Seed Secondary School",
      "region": "Eastern",
      "kind": "School",
      "reason": "Procured assets held at district stores pending school completion",
      "rows": [
        115773,
        115774,
        115775,
        115776,
        115777,
        115778,
        115779,
        115780,
        115781
      ],
      "source_file": "team-13/Manafwa/Butta/Asset-Verification-Toolkit.docx",
      "source_locator": "Table 12 row 2",
      "evidence": [
        {
          "register_row": 115773,
          "source_file": "team-13/Manafwa/Butta/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 2",
          "wording": "Functional; All were procured and are being stored at the District stores. They will be distributed upon completion of the construction of the school.; "
        },
        {
          "register_row": 115774,
          "source_file": "team-13/Manafwa/Butta/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 3",
          "wording": "Functional; All were procured and are being stored at the District stores. They will be distributed upon completion of the construction of the school.; "
        },
        {
          "register_row": 115775,
          "source_file": "team-13/Manafwa/Butta/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 4",
          "wording": "Functional; All were procured and are being stored at the District stores. They will be distributed upon completion of the construction of the school.; "
        },
        {
          "register_row": 115776,
          "source_file": "team-13/Manafwa/Butta/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 5",
          "wording": "Functional; All were procured and are being stored at the District stores. They will be distributed upon completion of the construction of the school.; "
        },
        {
          "register_row": 115777,
          "source_file": "team-13/Manafwa/Butta/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 6",
          "wording": "Functional; All were procured and are being stored at the District stores. They will be distributed upon completion of the construction of the school.; "
        },
        {
          "register_row": 115778,
          "source_file": "team-13/Manafwa/Butta/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 7",
          "wording": "Functional; All were procured and are being stored at the District stores. They will be distributed upon completion of the construction of the school.; "
        },
        {
          "register_row": 115779,
          "source_file": "team-13/Manafwa/Butta/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 8",
          "wording": "Functional; All were procured and are being stored at the District stores. They will be distributed upon completion of the construction of the school.; "
        },
        {
          "register_row": 115780,
          "source_file": "team-13/Manafwa/Butta/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 9",
          "wording": "Functional; All were procured and are being stored at the District stores. They will be distributed upon completion of the construction of the school.; "
        },
        {
          "register_row": 115781,
          "source_file": "team-13/Manafwa/Butta/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 10",
          "wording": "Functional; All were procured and are being stored at the District stores. They will be distributed upon completion of the construction of the school.; "
        }
      ]
    },
    {
      "book": "MANAFWA BK",
      "facility": "Sibanga Seed Secondary School",
      "region": "Eastern",
      "kind": "School",
      "reason": "Remaining ICT held at district",
      "rows": [
        117189,
        117217,
        117218
      ],
      "source_file": "team-13/Manafwa/Sibanga-Seed-School/Asset-Verification-Toolkit.docx",
      "source_locator": "Table 12 row 2",
      "evidence": [
        {
          "register_row": 117189,
          "source_file": "team-13/Manafwa/Sibanga-Seed-School/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 2",
          "wording": "Not in use; 10 monitors were stolen from the school. 18 monitors are kept at the district.; Source status: Not in use; "
        },
        {
          "register_row": 117217,
          "source_file": "team-13/Manafwa/Sibanga-Seed-School/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 3",
          "wording": "Not in use; 20 CPUs were stolen from the school. 8 CPUs are kept at the district stores.; Source status: Not in use; "
        },
        {
          "register_row": 117218,
          "source_file": "team-13/Manafwa/Sibanga-Seed-School/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 4",
          "wording": "Not in use; Not in use since the computers were stolen and others are being kept in district stores.; Source status: Not in use; "
        }
      ]
    },
    {
      "book": "MANAFWA BK",
      "facility": "Sisuni Seed Secondary School",
      "region": "Eastern",
      "kind": "School",
      "reason": "ICT held at district during construction",
      "rows": [
        117241
      ],
      "source_file": "team-13/Manafwa/Sisuni/Asset-Verification-Toolkit.docx",
      "source_locator": "Table 12 row 2",
      "evidence": [
        {
          "register_row": 117241,
          "source_file": "team-13/Manafwa/Sisuni/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 12 row 2",
          "wording": "Functional; The ICT computers and others are still kept at the District. The school is still under construction. We were able to take pictures of the computers from the schools at the District store.; "
        }
      ]
    },
    {
      "book": "BUDUDA BK",
      "facility": "Bumusi Health Centre III",
      "region": "Eastern",
      "kind": "Health centre",
      "reason": "Taken to Bududa Health Centre III for emergency use",
      "rows": [
        129935
      ],
      "source_file": "team-14/Bududa/Bumusi-HC-III/Asset-Verification-Toolkit.docx",
      "source_locator": "Table 6 row 136",
      "evidence": [
        {
          "register_row": 129935,
          "source_file": "team-14/Bududa/Bumusi-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 136",
          "wording": "Functional; The facility received two, and both were taken to Bududa HC III for an emergency there.; "
        }
      ]
    },
    {
      "book": "BULAMBULI BK",
      "facility": "Bumugibole Health Centre III",
      "region": "Eastern",
      "kind": "Health centre",
      "reason": "Taken to Bukibologoto; other equipment relocated to Muyembe Health Centre IV",
      "rows": [
        131938,
        132036
      ],
      "source_file": "team-14/Bulambuli/Bumugibole-HC-III/Asset-Verification-Toolkit.docx",
      "source_locator": "Table 6 row 56",
      "evidence": [
        {
          "register_row": 131938,
          "source_file": "team-14/Bulambuli/Bumugibole-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 56",
          "wording": "Functional; 3 in use, 2 taken to Bukibologoto due to an emergency after that facility was washed away; "
        },
        {
          "register_row": 132036,
          "source_file": "team-14/Bulambuli/Bumugibole-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 196",
          "wording": "Not seen; Relocated to Muyembe HC IV by the District Health Officer because it had a lot of work there; Source status: Not seen; "
        }
      ]
    },
    {
      "book": "SIRONKO BK",
      "facility": "Mutufu Health Centre III",
      "region": "Eastern",
      "kind": "Health centre",
      "reason": "Lent to another health centre",
      "rows": [
        133926
      ],
      "source_file": "team-14/Sironko/Mutufu-HC-III/Asset-Verification-Toolkit.docx",
      "source_locator": "Table 6 row 54",
      "evidence": [
        {
          "register_row": 133926,
          "source_file": "team-14/Sironko/Mutufu-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 54",
          "wording": "Not seen; The in-charge says it was lent to another health centre.; Source status: Not seen; "
        }
      ]
    },
    {
      "book": "BUKWO BK",
      "facility": "Mutushet Health Centre III",
      "region": "Eastern",
      "kind": "Health centre",
      "reason": "Taken temporarily to Tulel Health Centre III",
      "rows": [
        136284
      ],
      "source_file": "team-15/Bukwo/Mutushet-HC-III/Asset-Verification-Toolkit.docx",
      "source_locator": "Table 6 row 206",
      "evidence": [
        {
          "register_row": 136284,
          "source_file": "team-15/Bukwo/Mutushet-HC-III/Asset-Verification-Toolkit.docx",
          "source_locator": "Table 6 row 206",
          "wording": "Functional; 1 taken to Tulel H/C III but to be brought back; Engraving: Not yet; "
        }
      ]
    },
    {
      "book": "SHEEMA MC BK",
      "facility": "Kitojo Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Transferred to Migina health centre",
      "rows": [
        150500,
        150504,
        150559
      ],
      "source_file": "team-19/Mitooma/_district-documents/MITOOMA  HCIIIs List.xlsx",
      "source_locator": "Sheet1 row 347",
      "evidence": [
        {
          "register_row": 150500,
          "source_file": "team-19/Mitooma/_district-documents/MITOOMA  HCIIIs List.xlsx",
          "source_locator": "Sheet1 row 347",
          "wording": "Functional; 4 received and 1 transferred to migina h/c; "
        },
        {
          "register_row": 150504,
          "source_file": "team-19/Mitooma/_district-documents/MITOOMA  HCIIIs List.xlsx",
          "source_locator": "Sheet1 row 352",
          "wording": "Functional; Received but transferred to migina h/c; "
        },
        {
          "register_row": 150559,
          "source_file": "team-19/Mitooma/_district-documents/MITOOMA  HCIIIs List.xlsx",
          "source_locator": "Sheet1 row 433",
          "wording": "Functional; 2 received and 1 transferred to migna; "
        }
      ]
    },
    {
      "book": "MITOOMA BK",
      "facility": "Ryengyerero Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Transferred to Mitooma General Hospital",
      "rows": [
        151195
      ],
      "source_file": "team-19/Mitooma/_district-documents/MITOOMA  HCIIIs List.xlsx",
      "source_locator": "Sheet1 row 2197",
      "evidence": [
        {
          "register_row": 151195,
          "source_file": "team-19/Mitooma/_district-documents/MITOOMA  HCIIIs List.xlsx",
          "source_locator": "Sheet1 row 2197",
          "wording": "Functional; 1 One was transferred to Mitooma general hospital; "
        }
      ]
    },
    {
      "book": "SHEEMA BK",
      "facility": "Migina Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Transferred to Kabwohe Health Centre IV",
      "rows": [
        152914,
        152951
      ],
      "source_file": "team-19/Sheema/_district-documents/SHEEMA DC    HCIIIs.xlsx",
      "source_locator": "Sheet1 row 344",
      "evidence": [
        {
          "register_row": 152914,
          "source_file": "team-19/Sheema/_district-documents/SHEEMA DC    HCIIIs.xlsx",
          "source_locator": "Sheet1 row 344",
          "wording": "Functional; 02 received, one in use and one transferred to Kabwohe H/C IV; "
        },
        {
          "register_row": 152951,
          "source_file": "team-19/Sheema/_district-documents/SHEEMA DC    HCIIIs.xlsx",
          "source_locator": "Sheet1 row 446",
          "wording": "Functional; 1 One in use, one transferred to Kabwohe H/C IV; "
        }
      ]
    },
    {
      "book": "SHEEMA BK",
      "facility": "Rugarama Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Transferred to Shuku Health Centre IV",
      "rows": [
        153114
      ],
      "source_file": "team-19/Sheema/_district-documents/SHEEMA DC    HCIIIs.xlsx",
      "source_locator": "Sheet1 row 960",
      "evidence": [
        {
          "register_row": 153114,
          "source_file": "team-19/Sheema/_district-documents/SHEEMA DC    HCIIIs.xlsx",
          "source_locator": "Sheet1 row 960",
          "wording": "Functional; 1 is available and the 3 were transferred to shuku h/c iv; "
        }
      ]
    },
    {
      "book": "KAZO BK",
      "facility": "Engari Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Taken to district",
      "rows": [
        153739,
        153742,
        153756,
        153765
      ],
      "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
      "source_locator": "Sheet4 row 966",
      "evidence": [
        {
          "register_row": 153739,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 966",
          "wording": "1 in use; 2 were supplied but 1 was taken to district; Source status: 1 in use; "
        },
        {
          "register_row": 153742,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 970",
          "wording": "3 still in store; 4 were supplied 1 was taken to the district; Source status: 3 still in store; "
        },
        {
          "register_row": 153756,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 991",
          "wording": "1 still in store good condition; 3 were supplied and 2 taken to the district; Source status: 1 still in store good condition; "
        },
        {
          "register_row": 153765,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 1020",
          "wording": "1 in use; 2 were supplied and 1 was taken to kiruhura district; Source status: 1 in use; "
        }
      ]
    },
    {
      "book": "KAZO BK",
      "facility": "Nkungu Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Taken to Engari health centre",
      "rows": [
        154324
      ],
      "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
      "source_locator": "Sheet4 row 2232",
      "evidence": [
        {
          "register_row": 154324,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 2232",
          "wording": "Functional; 2 were supplied but 1 one in use and the deliver note list show that 1 was taken to engari; "
        }
      ]
    },
    {
      "book": "KIRUHURA BK",
      "facility": "Rwabarata Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Taken to Rwetamu and district",
      "rows": [
        154695,
        154809,
        154841
      ],
      "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
      "source_locator": "Sheet4 row 3005",
      "evidence": [
        {
          "register_row": 154695,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 3005",
          "wording": "Functional; 1 was supplied but report confirms that it was taken to rwetamu; "
        },
        {
          "register_row": 154809,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 3169",
          "wording": "2 are in use; 4 benches were supplied and 2 taken to the district; Source status: 2 are in use; "
        },
        {
          "register_row": 154841,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 3270",
          "wording": "Functional; 5 were supplied only 3 are in use and 2 were taken to the district; "
        }
      ]
    },
    {
      "book": "KIRUHURA BK",
      "facility": "Rweshande Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Taken to Kiruhura local government",
      "rows": [
        154878,
        154896,
        154897,
        154912,
        154933,
        154940,
        154941,
        154960
      ],
      "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
      "source_locator": "Sheet4 row 3354",
      "evidence": [
        {
          "register_row": 154878,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 3354",
          "wording": "One in use and in good condition; 2 were supplied by 1 was taken to the local govt of kiruhura; Source status: One in use and in good condition; "
        },
        {
          "register_row": 154896,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 3389",
          "wording": "Functional; 2were supplied one in use another taken to the local government; "
        },
        {
          "register_row": 154897,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 3392",
          "wording": "2 still in store; 3 were supplied and 1 was taken to the local government; Source status: 2 still in store; "
        },
        {
          "register_row": 154912,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 3408",
          "wording": "Good condition only 6 are in use 4 were taken to the local government; 10 were supplied all in use; Source status: Good condition only 6 are in use 4 were taken to the local government; "
        },
        {
          "register_row": 154933,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 3428",
          "wording": "Not seen; 1 was supplied but taken to the local government; Source status: Not seen; "
        },
        {
          "register_row": 154940,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 3438",
          "wording": "Not seen the delivery list show that it was taken to local govt; 1 was supplied but taken to the local govt; Source status: Not seen the delivery list show that it was taken to local govt; "
        },
        {
          "register_row": 154941,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 3440",
          "wording": "2 are in use and in good condition; 4 were supplied and 2 were taken to the local govt; Source status: 2 are in use and in good condition; "
        },
        {
          "register_row": 154960,
          "source_file": "team-20/_team-documents/TEAM 20 HCIIIS.xls",
          "source_locator": "Sheet4 row 3490",
          "wording": "1 in use and in good condition; 2 were supplied but one was taken to kiruhura local government; Source status: 1 in use and in good condition; "
        }
      ]
    },
    {
      "book": "KIRUHURA BK",
      "facility": "Kitura Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Taken to district",
      "rows": [
        157627,
        157630,
        157644,
        157653
      ],
      "source_file": "team-20/Kiruhura/Kitura-HC-III/KITURA HC 3.docx",
      "source_locator": "Table 6 row 142",
      "evidence": [
        {
          "register_row": 157627,
          "source_file": "team-20/Kiruhura/Kitura-HC-III/KITURA HC 3.docx",
          "source_locator": "Table 6 row 142",
          "wording": "1 in use; 2 were supplied but 1 was taken to district; Source status: 1 in use; "
        },
        {
          "register_row": 157630,
          "source_file": "team-20/Kiruhura/Kitura-HC-III/KITURA HC 3.docx",
          "source_locator": "Table 6 row 146",
          "wording": "3 still in store; 4 were supplied 1 was taken to the district; Source status: 3 still in store; "
        },
        {
          "register_row": 157644,
          "source_file": "team-20/Kiruhura/Kitura-HC-III/KITURA HC 3.docx",
          "source_locator": "Table 6 row 167",
          "wording": "1 still in store good condition; 3 were supplied and 2 taken to the district; Source status: 1 still in store good condition; "
        },
        {
          "register_row": 157653,
          "source_file": "team-20/Kiruhura/Kitura-HC-III/KITURA HC 3.docx",
          "source_locator": "Table 6 row 196",
          "wording": "1 in use; 2 were supplied and 1 was taken to kiruhura district; Source status: 1 in use; "
        }
      ]
    },
    {
      "book": "RUBIRIZI BK",
      "facility": "Munyonyi Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Taken to Rugazi Health Centre IV",
      "rows": [
        161603
      ],
      "source_file": "team-21/Rubirizi/Munyonyi-HC-III/DOC-20260829-WA0051.xlsx",
      "source_locator": "Asset Verification Checklist row 58",
      "evidence": [
        {
          "register_row": 161603,
          "source_file": "team-21/Rubirizi/Munyonyi-HC-III/DOC-20260829-WA0051.xlsx",
          "source_locator": "Asset Verification Checklist row 58",
          "wording": "Transferred / In use; 03 present; 02 taken to Rugazi HC IV; Source status: Transferred / In use; "
        }
      ]
    },
    {
      "book": "RUBIRIZI BK",
      "facility": "Mushumba Health Centre III",
      "region": "Western",
      "kind": "Health centre",
      "reason": "Transferred to Rugazi Health Centre IV",
      "rows": [
        161661,
        161668,
        161678,
        161679
      ],
      "source_file": "team-21/Rubirizi/Mushumba-HC-III/DOC-20260829-WA0056.xlsx",
      "source_locator": "Asset Verification Checklist row 9",
      "evidence": [
        {
          "register_row": 161661,
          "source_file": "team-21/Rubirizi/Mushumba-HC-III/DOC-20260829-WA0056.xlsx",
          "source_locator": "Asset Verification Checklist row 9",
          "wording": "Functional; 1 at facility; 1 transferred to Rugazi H/C IV; "
        },
        {
          "register_row": 161668,
          "source_file": "team-21/Rubirizi/Mushumba-HC-III/DOC-20260829-WA0056.xlsx",
          "source_locator": "Asset Verification Checklist row 12",
          "wording": "Functional; Transferred to Rugazi H/C IV; "
        },
        {
          "register_row": 161678,
          "source_file": "team-21/Rubirizi/Mushumba-HC-III/DOC-20260829-WA0056.xlsx",
          "source_locator": "Asset Verification Checklist row 17",
          "wording": "Functional; Transferred to Rugazi H/C IV; "
        },
        {
          "register_row": 161679,
          "source_file": "team-21/Rubirizi/Mushumba-HC-III/DOC-20260829-WA0056.xlsx",
          "source_locator": "Asset Verification Checklist row 18",
          "wording": "Functional; Transferred to Rugazi H/C IV; "
        }
      ]
    },
    {
      "book": "KABAROLE BK",
      "facility": "Kichwamba Seed Secondary School",
      "region": "Western",
      "kind": "School",
      "reason": "Desktops held at district during construction",
      "rows": [
        188021
      ],
      "source_file": "team-26/Kabarole/Nyantabooma-HC-III/NYANTABOMA HEALTH CENTRE III  - ASSET VERIFICATION AND RECORDING TOOL KIT.docx",
      "source_locator": "Table 12 row 2",
      "evidence": [
        {
          "register_row": 188021,
          "source_file": "team-26/Kabarole/Nyantabooma-HC-III/NYANTABOMA HEALTH CENTRE III  - ASSET VERIFICATION AND RECORDING TOOL KIT.docx",
          "source_locator": "Table 12 row 2",
          "wording": "All desktops are still at district because the facility still under construction; At district stores; Source status: All desktops are still at district because the facility still under construction; "
        }
      ]
    },
    {
      "book": "KYANKWANZI BK",
      "facility": "Sirimula Health Centre III",
      "region": "Central",
      "kind": "Health centre",
      "reason": "Beds given to Mwangi Health Centre III and held at district store",
      "rows": [
        192181
      ],
      "source_file": "team-29/_team-documents/UGIFT SIRIMULA.docx",
      "source_locator": "Table 6 row 80",
      "evidence": [
        {
          "register_row": 192181,
          "source_file": "team-29/_team-documents/UGIFT SIRIMULA.docx",
          "source_locator": "Table 6 row 80",
          "wording": "Functional; Found 17 beds in use. The facility gave out 3 beds to Mwangi HC III and 4 beds are still at the District store; "
        }
      ]
    }
  ],
  "rejected": [
    {
      "book": "KAKUMIRO BK",
      "facility": "Kigando Health Centre III",
      "reason": "Reception is within the same facility.",
      "rows": [
        6347
      ]
    },
    {
      "book": "OYAM BK",
      "facility": "Loro Health Centre III",
      "reason": "Staff quarters are not identified as another facility or district.",
      "rows": [
        55882
      ]
    },
    {
      "book": "BUTALEJA BK",
      "facility": "Nakwasi Seed Secondary School",
      "reason": "ICT library to administration block is internal movement.",
      "rows": [
        112069
      ]
    },
    {
      "book": "KIBUKU BK",
      "facility": "St Johns Kirika Seed Secondary School",
      "reason": "A theft case was taken to police, not an asset transfer.",
      "rows": [
        113335
      ]
    },
    {
      "book": "RUBIRIZI BK",
      "facility": "Ryeru Seed Secondary School",
      "reason": "Repair in Kampala without a named receiving facility or district; excluded from shared/held-at-facility measure.",
      "rows": [
        158462
      ]
    },
    {
      "book": "BULIISA BK",
      "facility": "Kihungya Seed Secondary School",
      "reason": "Secretary house is not a named receiving facility or district.",
      "rows": [
        181185,
        181186,
        181187,
        181188
      ]
    },
    {
      "book": "KIIRA MC BK",
      "facility": "Kirinya Health Centre III",
      "reason": "Own store; no off-site holder identified.",
      "rows": [
        202209
      ]
    }
  ],
  "excluded_rows": {
    "55231": "Ward shared with male patients, no external asset sharing.",
    "114751": "Movement among departments within the facility."
  },
  "notes": [
    "Includes district custody pending completion and temporary off-site holding, not only permanent sharing.",
    "Tekulu district repair custody is included because the receiving district is explicit.",
    "Silumira (Kakumiro) and Sirimula (Kyankwanzi) have separate register identities and source documents; both have the same bed-transfer wording. No unsupported cross-government identity merger has been made. Counts are register facility identities.",
    "Rows represent supporting evidence examples, not the number of assets transferred. Shared remarks about a group must not be multiplied into a transfer-asset count."
  ]
}

## Exact reviewed selection for stored assets in good or new condition

The 483 reported rows require REF AU IN_USE_FLAG = NO and affirmative good/new/sealed condition together with storage wording in SK N Equipment status or O Remarks. They exclude contrary condition and uncertain custody wording. Worksheet row numbers below are inclusive and refer to the aligned Asset Register sheets, data rows 2:225134. The broader storage wording selection is not used as the good-condition count.

```json
{
  "label": "stored_explicit_good",
  "count": 483,
  "row_ranges_inclusive": [
    [
      8964,
      8971
    ],
    [
      8974,
      8975
    ],
    [
      9015,
      9016
    ],
    [
      12913,
      12913
    ],
    [
      13027,
      13027
    ],
    [
      28088,
      28089
    ],
    [
      49873,
      49874
    ],
    [
      59675,
      59675
    ],
    [
      71490,
      71490
    ],
    [
      72048,
      72048
    ],
    [
      72347,
      72348
    ],
    [
      72361,
      72361
    ],
    [
      72363,
      72363
    ],
    [
      72369,
      72369
    ],
    [
      72373,
      72377
    ],
    [
      72385,
      72385
    ],
    [
      72401,
      72401
    ],
    [
      72406,
      72407
    ],
    [
      72409,
      72419
    ],
    [
      73244,
      73249
    ],
    [
      73284,
      73285
    ],
    [
      73288,
      73290
    ],
    [
      73301,
      73303
    ],
    [
      73306,
      73308
    ],
    [
      73312,
      73313
    ],
    [
      73329,
      73329
    ],
    [
      73526,
      73527
    ],
    [
      73590,
      73590
    ],
    [
      73694,
      73704
    ],
    [
      75617,
      75617
    ],
    [
      75619,
      75620
    ],
    [
      75623,
      75630
    ],
    [
      75698,
      75721
    ],
    [
      75724,
      75735
    ],
    [
      75739,
      75741
    ],
    [
      75750,
      75752
    ],
    [
      75754,
      75756
    ],
    [
      75758,
      75760
    ],
    [
      75762,
      75765
    ],
    [
      75767,
      75768
    ],
    [
      75770,
      75771
    ],
    [
      75780,
      75783
    ],
    [
      75790,
      75792
    ],
    [
      75794,
      75799
    ],
    [
      75801,
      75802
    ],
    [
      75815,
      75818
    ],
    [
      76271,
      76272
    ],
    [
      76826,
      76829
    ],
    [
      76833,
      76834
    ],
    [
      76878,
      76878
    ],
    [
      76915,
      76915
    ],
    [
      76930,
      76930
    ],
    [
      77011,
      77020
    ],
    [
      77023,
      77024
    ],
    [
      77045,
      77049
    ],
    [
      77051,
      77051
    ],
    [
      77053,
      77056
    ],
    [
      77059,
      77061
    ],
    [
      77065,
      77069
    ],
    [
      77072,
      77073
    ],
    [
      77082,
      77082
    ],
    [
      81213,
      81215
    ],
    [
      81223,
      81226
    ],
    [
      110557,
      110558
    ],
    [
      110710,
      110829
    ],
    [
      111255,
      111275
    ],
    [
      111308,
      111308
    ],
    [
      112291,
      112292
    ],
    [
      113323,
      113324
    ],
    [
      115315,
      115315
    ],
    [
      135072,
      135073
    ],
    [
      153350,
      153351
    ],
    [
      153367,
      153369
    ],
    [
      153548,
      153555
    ],
    [
      153706,
      153706
    ],
    [
      153709,
      153712
    ],
    [
      153737,
      153738
    ],
    [
      153989,
      154003
    ],
    [
      154016,
      154020
    ],
    [
      154166,
      154169
    ],
    [
      154187,
      154200
    ],
    [
      154248,
      154248
    ],
    [
      154265,
      154265
    ],
    [
      154267,
      154267
    ],
    [
      154279,
      154280
    ],
    [
      154292,
      154293
    ],
    [
      154318,
      154319
    ],
    [
      154325,
      154325
    ],
    [
      154376,
      154377
    ],
    [
      154411,
      154412
    ],
    [
      154631,
      154633
    ],
    [
      154636,
      154644
    ],
    [
      154658,
      154660
    ],
    [
      154705,
      154705
    ],
    [
      154715,
      154715
    ],
    [
      154733,
      154734
    ],
    [
      154770,
      154770
    ],
    [
      154772,
      154773
    ],
    [
      154775,
      154775
    ],
    [
      154850,
      154851
    ],
    [
      154864,
      154864
    ],
    [
      154866,
      154866
    ],
    [
      154881,
      154883
    ],
    [
      154908,
      154909
    ],
    [
      155077,
      155080
    ],
    [
      157594,
      157594
    ],
    [
      157597,
      157600
    ],
    [
      157625,
      157626
    ]
  ],
  "row_column": "Asset Register worksheet row number",
  "storage_regex": "\\bin (?:the |their |a )?stor(?:e|age)\\b|\\b(?:stored|boxed|unopened|uninstalled|unassembled)\\b|\\bin (?:the |their |a )?box(?:es)?\\b|\\bnot yet (?:installed|in use)\\b|\\bnot in use yet\\b|\\bstill (?:packed|new)\\b|\\bnew (?:and |but )?(?:not connected|not in use|in (?:the )?store)\\b",
  "exclusion_regex": "\\bdamag\\w*|\\bbroken\\b|\\bfaulty\\b|\\bspoil[et]\\w*\\b|\\bbeyond repair\\b|\\b(?:needs?|for) repair\\b|\\bpoor (?:condition|state)\\b|\\bnot working\\b|\\bunserviceable\\b|\\bobsolete\\b|\\bshaking\\b|\\bnot in (?:the |their |a )?stor(?:e|age)\\b|\\bnot stored\\b|\\bnot (?:yet )?(?:received|delivered|supplied)\\b|\\b(?:lost|stolen|missing|condemned|disposed)\\b|\\bnot (?:physically )?(?:seen|verified|found|present)\\b|\\bcould not (?:be )?(?:see|verify|find)\\b|\\bunable to (?:see|verify|find)\\b|\\b(?:didn.t|did not) (?:get to )?(?:see|verify|find)\\b",
  "additional_positive_condition_regex": "\\bgood (?:condition|state|status|working condition)\\b|\\bstill new\\b|\\bnew (?:and |but )?(?:not connected|not in use|in (?:the )?store)\\b|\\bbrand new\\b|\\b(?:sealed|unopened)\\b",
  "by_region": {
    "Central": 2,
    "Eastern": 300,
    "Northern": 66,
    "Western": 115
  },
  "note": "Uses REF IN_USE_FLAG=NO. Operational storage wording does not itself establish physical condition; explicit_good subset requires affirmative good/new/sealed wording. Excludes damage, repair, negation, absent/undelivered/uncertain-location and physical-observation exclusions.",
  "additional_contrary_condition_exclusion_regex": "\\bnon[\\s-]*function\\w*|\\bnot\\s*(?:function\\w*|working|good)\\b|\\bnot in good\\b|\\bpoor quality\\b|\\bdefect\\w*\\b|\\bdead\\b",
  "manual_excluded_rows": [
    135068,
    135071
  ],
  "manual_exclusion_reason": "Wording says not locked / not yet locked in the store, so storage status is ambiguous.",
  "actual_SK_review_note": "Reviewed after complete SK extraction. Added12913 and13027 (Nyanja: still New & kept in store),135072 and135073 (Aralam: Brand new, locked in store, Functional). These rows had blank SK status; previous fallback REF Faulty wrongly excluded them."
}
```

## National operations and maintenance evidence

Acquisition warranty clauses describe the terms recorded at purchase, not present warranty coverage. Each observation below gives the REF worksheet row and its underlying source location.

```json
{
  "by_book": {
    "MOFPED BK": [
      {
        "prose": "The acquisition records for desktop computers specify a 1 year warranty.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 210447,
        "item": "Lenovo Desktop Computer",
        "raw_evidence_without_identity": "Room 5.1;  Supplier IT OFFICE (U) LTD; Warranty 1 Year; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT .ASSETS REGISTER-BPED.xls; _multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 7"
      },
      {
        "prose": "The procurement entry for a heavy duty photocopier also specifies a 1 year warranty and describes it as in good working condition.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 210503,
        "item": "Heavy Duty Photocopier",
        "raw_evidence_without_identity": "Room 3rd Floor; Supplier MFI Document Solution Ltd; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT .ASSETS REGISTER-BPED.xls; _multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 100"
      }
    ],
    "MOWT BK": [
      {
        "prose": "The MoWT vehicle return states that MoFPED undertakes repairs and servicing of the Toyota Hilux pickup.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 209567,
        "item": "Toyota Hilux Double Cabin Pickup",
        "raw_evidence_without_identity": "The MoWT Recommend the ministry of Finance for the good work done since the do all the repair and servicing of the vechicle.; Source status: In Good condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
        "source_location": "MoWT row 4"
      },
      {
        "prose": "The acquisition record for a heavy duty photocopier specifies a 1 year warranty.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 214883,
        "item": "Heavy Duty Photocopier",
        "raw_evidence_without_identity": "Supplier MFI Document Solution Ltd; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 445"
      }
    ],
    "MOES BK": [
      {
        "prose": "The acquisition records for laptops specify a 1 year warranty and describe the equipment as in good working condition.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 210553,
        "item": "Lenovo ThinkBook Laptop",
        "raw_evidence_without_identity": "Supplier Converge Systems Ltd; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT ASSETS REGISTER FOR FY2023.2024 FOR AUDITORS.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 6"
      }
    ],
    "MAAIF BK": [
      {
        "prose": "The tablet acquisition records specify a 1 year warranty.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 210942,
        "item": "Computer Tablet",
        "raw_evidence_without_identity": "Supplier Tel Care Ltd; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT ASSETS REGISTER FOR FY2023.2024 FOR AUDITORS.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 468"
      },
      {
        "prose": "The printer entry specifies a 3 year warranty and describes the equipment as in good working condition.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 215269,
        "item": "HP Laserjet Pro MFP 4103fdw",
        "raw_evidence_without_identity": "Supplier Converge Systems Ltd; Warranty 3 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 1398"
      }
    ],
    "MOH BK": [
      {
        "prose": "The acquisition records for laptops specify a 1 year warranty and describe the equipment as in good working condition.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 214539,
        "item": "Lenovo LOQ 16IRH8-i7 Laptop",
        "raw_evidence_without_identity": "Supplier Millenniu Minfosys Ltd; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT ASSETS REGISTER FOR FY2023.2024 FOR AUDITORS.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 4073"
      },
      {
        "prose": "The motorcycle procurement entry also specifies a 1 year warranty.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 214596,
        "item": "Yamaha Xtz",
        "raw_evidence_without_identity": "Supplier CFAO Motors Uganda Ltd; Warranty 1 Year; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "MOTORCYCLES FOR MOH-UGIFT row 5"
      }
    ],
    "OPM BK": [
      {
        "prose": "The equipment return identifies damaged laptops that are not in use.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 209828,
        "item": "HP Laptop Envy i3",
        "raw_evidence_without_identity": "This laptop is not being used; Source status: not functional/ damaged; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx; _multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "OPM row 7"
      }
    ],
    "MOWE BK": [
      {
        "prose": "The tablet acquisition records specify a 1 year warranty and describe the equipment as in good working condition.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 212164,
        "item": "Euron MT8765A Tablets",
        "raw_evidence_without_identity": "Supplier MFI Document Solutions Ltd; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT ASSETS REGISTER FOR FY2023.2024 FOR AUDITORS.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 1022"
      }
    ],
    "MGLSD BK": [
      {
        "prose": "The acquisition records for laptops specify a 1 year warranty and describe the equipment as in good working condition.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 214994,
        "item": "Lenovo ThinkBook Laptop",
        "raw_evidence_without_identity": "Supplier KACO Systems Ltd; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 619"
      }
    ],
    "NEMA BK": [
      {
        "prose": "The acquisition record for a heavy duty photocopier specifies a 1 year warranty and describes the equipment as in good working condition.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 214919,
        "item": "Heavy Duty Photocopier",
        "raw_evidence_without_identity": "Supplier MFI Document Solution Ltd; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 489"
      }
    ],
    "PPDA BK": [],
    "OAG BK": [
      {
        "prose": "The laptop acquisition records specify a 1 year warranty and describe the equipment as in good working condition.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 214536,
        "item": "Dell XPS 15 I7 Laptop",
        "raw_evidence_without_identity": " Supplier TRIO CEO Limited; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT ASSETS REGISTER FOR FY2023.2024 FOR AUDITORS.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 4067"
      }
    ],
    "MOLG BK": [
      {
        "prose": "The acquisition record for a heavy duty photocopier specifies a 1 year warranty and describes the equipment as in good working condition.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 214920,
        "item": "Heavy Duty Photocopier",
        "raw_evidence_without_identity": "Supplier MFI Document Solution Ltd; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 492"
      }
    ],
    "MOLHUD BK": [
      {
        "prose": "The motorcycle acquisition records specify a 1 year warranty.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 214604,
        "item": "Motorcycles Honda XL125 LEX",
        "raw_evidence_without_identity": "Supplier Honda Uganda Ltd; Warranty 1 Year; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "MOTORCYCLES FOR MOH-UGIFT row 20"
      }
    ],
    "KCCA BK": [
      {
        "prose": "The phone acquisition records specify a 1 year warranty.",
        "register": "outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 214618,
        "item": "SamSung Phone",
        "raw_evidence_without_identity": "Supplier CLS Limited; Warranty 1 Year; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 17"
      }
    ]
  },
  "templates": {
    "with_maintenance": "The register contains {asset_count} assets for {mda}, with recorded value of UGX {recorded_value} and net book value of UGX {nbv}. Of these, {engraved_count} carry engraving, including {ugift_count} with UgIFT marking. {supported_maintenance_or_warranty_sentence}",
    "without_maintenance": "The register contains {asset_count} assets for {mda}, with recorded value of UGX {recorded_value} and net book value of UGX {nbv}. It records {functional_count} assets in the Functional class and {faulty_count} in the Faulty class. Engraving is present on {engraved_count} assets, including {ugift_count} with UgIFT marking.",
    "warranty_note": "Warranty periods describe the acquisition terms. They do not establish current warranty eligibility or an active servicing contract."
  },
  "source_notes": [
    "Warranty periods are acquisition terms, not evidence of current cover. Do not write that equipment remains under warranty. No expiry date was inferred.",
    "MOFPED rows with Warranty 80000, 60000 or 150000 were not used as warranty evidence.",
    "MOWT row 214979 names Ministry Of Local Government as an item. It was not used as an equipment or warranty example.",
    "OPM prose is supported by rows 209828, 209830 and 209831 with source locations OPM rows 7, 9 and 10. These are examples rather than a complete damaged-laptop count.",
    "The national template without maintenance evidence makes no claim about a maintenance arrangement; per-book rows with no maintenance evidence should not receive a generic invented arrangement.",
    "National observation candidates were reviewed from main task national_observations.json, including remarks before Facility type. Only specific equipment and explicit terms were retained."
  ]
}
```

## Final geography cross-check

All NWOYA BK local holdings are assigned to Acholi; hospital rows retain national treatment. The Northern sub-region totals used in the report and chart include this placement.

```json
{
  "Nwoya": [
    {
      "region": "National",
      "subregion": "National",
      "level": "National",
      "assets": 60
    },
    {
      "region": "Northern",
      "subregion": "Acholi",
      "level": "Local government",
      "assets": 733
    }
  ],
  "Northern": {
    "Acholi": 9141,
    "Karamoja": 6052,
    "Lango": 19471,
    "West Nile": 17639
  }
}
```
