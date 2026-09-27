# Prompt: write the UgIFT asset verification narrative report

You are writing the end-of-programme asset verification report for the UgIFT programme, as a Word document and a PDF. It is a high-level narrative for senior readers at the Ministry and its partners. Everything in it must come from the files listed below. The report treats the field verification as complete and diligent: it presents what the teams found and recorded. Where a file does not state something, leave that point out of the report. Do not write that a record is silent, blank, missing, incomplete, unverified or inconsistent, and do not fill the gap with an assumption either. Keep your own note of what you checked in `sources.md`, not in the report.

The one place the report speaks about facilities that were not verified on the ground is the reconciliation of the master list (section 7.1 and its appendix). A facility appears there only when the supervisor's reconciliation records an acceptable reason, and it is written as an outcome of the verification and reconciliation process, never as a shortfall of the field teams. The reader should close the report trusting that every facility on the master list was either verified or accounted for.

## Outputs

Write into `outputs/narrative-report/`:

1. `UgIFT Asset Verification Report.docx`
2. `UgIFT Asset Verification Report.pdf` (converted from the Word file; open the PDF and confirm every page rendered, tables did not split badly, and every figure and photo is visible)
3. `figures/` holding every chart as a PNG at 200 dpi and every photograph used, as copied and resized
4. `sources.md` listing, for every table, chart, photograph and headline number in the report: the file, sheet or table, and the row range or filter used. This is an internal audit log, not an appendix to reproduce in the Word or PDF report.

Do not change any file under `raw-data-grouped/`, `outputs/asset-register/` or `outputs/report-templates/`.

## Report terminology and source presentation

The files under `outputs/asset-register/` are repositories of asset records used for analysis. Do not directly reference these files in the Word or PDF report, including the body, tables, chart labels, captions, footnotes, headers, footers, appendices, source lists or hyperlinks. Keep their filenames, paths, workbook abbreviations (REF, MF and SK), worksheet names, column codes and row locators in this working prompt and `sources.md` only. Describe the evidence in the report as "UgIFT asset verification records" or the relevant field records, and cite the underlying policy or field evidence where appropriate.

Refer to the physical items and their counts as "assets", not spreadsheet "rows", "records", "entries" or "lines". For example, write "225,133 assets" and "assets with a recorded condition". A description of the recordkeeping process may still use "records", and "row" may still describe the layout of a table; neither term should replace "asset" when discussing the items being counted. Retain exact worksheet rows, columns and filters in `sources.md` so every reported asset count remains reproducible.

## Read these before writing

- `outputs/report-templates/Report outline _ BB input.docx`: the agreed structure. Follow its sections and order, with the user's requested Recommendations and Conclusion added as final sections 9 and 10 after the appendices.
- `outputs/report-templates/Verification report_ 24092026_Draft_ BB.docx`: the client's draft. Reuse its background, objectives, scope, project context and methodology content, rewritten in the style rules below and with every personal name removed.
- `outputs/report-templates/WhatsApp Image 2026-09-25 at 15.07.09.jpeg`: a handwritten list of the counts the client wants. Every item on it becomes a row of the summary table in the findings (see "Required summary counts").
- `outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`: the register the numbers come from (sheet `Asset Register`, one row per physical asset, 64 columns; the `Read Me` sheet explains every column). Use `ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx` when you need the wording the field team wrote, and the `BOOK_TYPE_CODE` section of `outputs/asset-register/README.md` for the list of votes.
- `outputs/asset-register/ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`: the same rows with only the values the field records state. Use it when the report must say what was recorded on the ground rather than valued.
- `raw-data-grouped/README.md`, `raw-data-grouped/facility-data-status.pdf`, `raw-data-grouped/facility-reconciliation.csv`, `raw-data-grouped/master-source-rows.csv`, `raw-data-grouped/supervisor-decisions.csv`: facility coverage, facilities on the master list that were not found or were renamed, facilities found on the ground that were not on the list, and the decisions taken on them.
- `SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx` (columns Region, Sub-region, District, School or sub-county, Phase, Status) and `team-distributions.docx` (Region, Local Government, numbers of schools and health facilities): the region and sub-region of every local government, and the number of facilities per local government.
- `GOU Asset Accounting Policies and Guidelines 2023.pdf`, sections 3.2.1, 3.3.3, 5.5 and 5.7 and Annex 1: the recognition, useful-life and depreciation basis the register applied. Cite the section when the report explains a valuation.
- Photographs: loose image files under `raw-data-grouped/team-NN/<Local government>/<Facility>/` and `raw-data-grouped/team-NN/_team-documents/` (their folder names give the local government and facility), and the photographs embedded in the documents the teams produced: 671 of the Word returns under `raw-data-grouped/` carry embedded images (about 10,900 in all), the district reports under `team-NN/<Local government>/_district-documents/` carry 50 to 140 each, `_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-verification-photographic-gallery.docx` holds about 5,400 and `UGiFT-consolidated-field-report.docx` about 670, and 322 PDF scans hold photographed forms and assets. See "Photographs" for how to extract them.
- `raw-data-grouped/_multi-team/programme-documents/data-management-chat/` and the `Remarks`, `Equipment status` and interview tables in the facility returns: the operations, maintenance and asset-management observations. Quote the substance, never the speaker.

## Structure

Follow the outline document. Use numbered headings. The report has these parts:

1. Cover page: title, the programme, the reporting date, the client. No personal names, no logos you do not have.
2. Table of contents, list of tables, list of figures, list of acronyms (every acronym used, spelled out once).
3. Executive summary, at most two pages: what was verified, where, when; the headline counts (facilities covered, assets verified, share functional, share engraved, total recorded value and net book value); the main risks; the main recommendations. Every number here must appear again in the body with its source.
4. Introduction and background: introduction, background to the verification, justification, objectives, scope of work. Take the substance from the draft.
5. Approach and methodology: the three phases (inception, data collection, reporting), the verification tool and its fields, the pilot, notification of local governments, the field itinerary table, quality assurance, data consolidation and the IFMIS-ready register. Take the substance from the draft; state dates and durations as the draft gives them; where the draft leaves a blank (for example "Table ..."), number the table yourself.
6. Project context: programme design, components, objectives and the programme outputs as the draft lists them.
7. Findings.
   - 7.1 Introduction to the findings: coverage and reconciliation of the master list. State the number of facilities on the master list and the number verified on the ground, then present the reconciliation statement: every master-list facility not verified on the ground is accounted for by a reason the supervisor's reconciliation records. Group them by reason and give the count and the facilities for each: the facility does not exist or was not constructed under the programme; the facility was replaced by another facility (name the receiving facility, which was verified); the facility operates under another name (give both names); the facility is not a UgIFT beneficiary; the assets were relocated to another facility or are held at the district pending completion; the facility exists but holds no UgIFT assets. Then list the facilities found on the ground that were not on the master list, with their local government. Take every reason from the `decision` and `note` columns of `supervisor-decisions.csv` and the `status`, `verification` and `note` columns of `facility-reconciliation.csv`, and take the coverage totals from `raw-data-grouped/README.md`. Write each item as the reconciled outcome ("the master-list entry X was confirmed on the ground as Y Seed Secondary School"), never as a failure to verify. Do not list a facility as unverified where those files record no reason, and do not state or imply a rate of facilities that could not be verified; the closing sentence of the section is that every master-list facility was verified or accounted for through reconciliation.
   - 7.2 National level: one sub-section per MDA that holds assets in the records, in the order the outline lists them (MoFPED, MoWT, MoES, MAAIF, MoH, OPM, MoWE, MoGLSD, NEMA, PPDA, OAG, MoLG, MoLHUD, LGFC, MoPS). For each: a table with asset category, quantity, total recorded cost, accumulated depreciation, net book value and status, then two to four sentences on engraving and operations and maintenance. An MDA with no assets in the records is not given a sub-section and is not commented on; it stays in the methodology's list of MDAs visited, as the draft gives it.
   - 7.3 Local government level by region and sub-region: Central; Eastern (Bugisu, Bukedi, Busoga, Teso, Sebei); Northern (Acholi, West Nile, Lango, Karamoja); Western (Ankole, Bunyoro, Rwenzori, Tooro, Kigezi). For each region: the number of health centres and seed schools covered, then health centre assets by the outline's categories (clinical equipment; clinical furniture; maternity ward equipment; ICT equipment; building blocks) and school assets by its categories (building blocks; furniture, meaning desks, tables, chairs and stools; computers and related equipment excluding network switches; support equipment, meaning printers and cameras and projectors). For each category give number, status and recorded value, then a brief on maintenance arrangements drawn from the remarks and interviews. Give the sub-region breakdown as a table or chart under each region. List the facilities on the master list not found on the ground and the facilities found that were not on the list, per region, from `facility-reconciliation.csv`.
   - 7.4 Functionality of assets: functional and non-functional counts by category and by sub-region, as charts, with the underlying table in an appendix.
   - 7.5 Asset management practices and risks: observations on storage, utilisation, records, breakdowns and maintenance with specific local-government examples (the local government, not the person); the risks and challenges; then recommendations on identification (engraving), registration and maintenance, and future programming.
   - 7.6 UgIFT support to service delivery: issues, challenges and recommendations, from the interview and remark records.
   - 7.7 Summary of findings: draw together the field observations and follow-up priorities without labelling this earlier subsection as the report's conclusion.
8. Appendices: the summary count table in full; the functionality tables behind the charts; the master-list reconciliation table (each facility accounted for through reconciliation, with its master-list entry, its local government, the reconciled outcome and the reconciliation record it rests on) and the list of facilities found that were not on the list; a brief note on the asset records prepared for IFMIS, describing the assets covered and the recordkeeping purpose without naming register files or presenting spreadsheet row counts or column codes; a sources list describing the field evidence and policies used. Keep the technical register inventory and detailed calculation locators in `sources.md` only.
9. Recommendations: place this section after all appendices. Consolidate the evidence-based priorities already established in the findings and priority action plan: safety and repairs, completion and installation, user skills, identification and custody, maintenance, and service readiness. Identify responsible institutions using the existing action plan. Any timeframes remain proposed, use the same report-approval basis as that plan, and do not create new mandatory deadlines. Refer to the action plan for detailed owners, timing and evidence of completion; do not introduce new findings or unsupported totals.
10. Conclusion: make this the final section of the report. State the programme benefits and practical constraints established by the verification, then explain the need to protect existing services and bring remaining assets into safe, intended use. Keep it concise and grounded in the findings. Do not introduce new figures, direct register-file references or claims that follow-up work has already been completed.

## Required summary counts

Produce this table for the whole programme and repeat it per region. Each row is one line of the handwritten list:

| Measure | How to count it in the REF register |
|---|---|
| Assets which are engraved | `TAG_NUMBER` is not `Not Engraved` |
| Assets engraved with UgIFT marking | engraved and the tag contains `UGIFT` or `UGFT` (any case) |
| Assets engraved with other marking | engraved and the tag does not contain those letters |
| Assets in use | `IN_USE_FLAG` = `YES` |
| Assets not in use due to damage | `IN_USE_FLAG` = `NO` and `ATTRIBUTE15(Remarks)` or the SK `Equipment status` wording says damaged, broken, faulty, not working or needs repair |
| Assets not in use but in good condition (stored, in box) | `IN_USE_FLAG` = `NO` and the wording says in store, stored, in box, not yet installed, not yet in use, new |
| Assets in good condition (functional) | `ATTRIBUTE14(Equipment status)` = `Functional` |
| Total assets verified by category | count of assets by `ASSET_CATEGORY_MINOR2`, and by the report categories above |
| Facilities which had shared assets out with others | facilities whose remarks say an asset was shared with, lent to, moved to or kept at another facility or the district |
| Facilities not on the master list but found in the local governments | `facility-reconciliation.csv` rows whose scope is a ground return only (X ids) |
| Facilities on the master list accounted for through reconciliation, by reason (does not exist; replaced; operates under another name; not a UgIFT beneficiary; assets relocated or held at the district; exists with no UgIFT assets) | `supervisor-decisions.csv` decisions such as Does not exist, Replaced, Renamed, Name corrected, Location name corrected, Assets relocated, Exists no UgIFT assets, Not UgIFT, and the matching `facility-reconciliation.csv` rows; count each facility once under its final outcome |
| Total number by category | facilities and assets by category and by region |

Count each physical asset once; the underlying register holds one worksheet row per asset. Use "assets" for these counts throughout the report. Where an asset's status is blank, leave it out of the functional and non-functional counts; do not add a "not stated" column and do not mention unassessed assets. Compute a functional share over the assets with a recorded condition and label it "of assets assessed for condition".

## Mapping the register to the report's categories

- Buildings: `ASSET_CATEGORY_MAJOR` = `BUILDINGS AND STRUCTURES`; work in progress is `ASSET_TYPE` = `CIP`.
- Furniture: `ASSET_CATEGORY_MINOR2` = `FURNITURE AND FITTINGS`. School furniture is that class at a seed school; clinical furniture is that class at a health centre plus beds, couches, trolleys, screens, stands and lockers from `MED LAB RESEARCH APPLIANCES` whose name says so.
- Vehicles and motorcycles: `ASSET_CATEGORY_MINOR1` = `TRANSPORT EQUIPMENT`.
- ICT: `ASSET_CATEGORY_MINOR1` = `ICT EQUIPMENT`; "computers and related equipment excluding network switches" leaves out names containing switch; "support equipment" is printers, photocopiers, cameras and projectors.
- Clinical equipment: `MED LAB RESEARCH APPLIANCES` at a health centre, less the clinical furniture above.
- Maternity ward equipment: rows whose `LOCATION_SEGMENT2` or item name says maternity, delivery, labour, antenatal, postnatal, kangaroo or neonatal.
- Health centre or school: `Facility type:` in `ATTRIBUTE15(Remarks)` (Health centre, School); the MDA rows have Facility type MDA, Hospital or Blood bank and belong to the national level.
- Value: `FIXED_ASSETS_COST` is the recorded cost, `DEPRN_RESERVE` the accumulated depreciation to 30 September 2026, and net book value is cost less accumulated depreciation, floored at zero. Sum by group; show UGX with thousands separators and no decimals.
- Region and sub-region: join `BOOK_TYPE_CODE` (the local government) to the district's Region and Sub-region in `SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx`; a city or municipal council takes its district's region. For a local government that document does not list, take its region from `team-distributions.docx`, which lists every local government by region, and its sub-region from the district it was carved out of. Record each such placement in `sources.md`.

State the mapping you applied in one paragraph of the methodology and in `sources.md`.

## What the report must not say

- No personal names anywhere: not officials, not field staff, not chat participants, not head teachers or in-charges, not in photo captions, not in the acknowledgements. Refer to roles: the Accounting Officer, the health centre in-charge, the head teacher, the district health officer, the Consultant, the Client, the field team, the supervisor.
- No telephone numbers, chat handles or email addresses.
- Do not describe any figure as fabricated, generated, auto-generated, synthetic, simulated, invented, borrowed, imputed by software, or produced by AI or by a model. Do not mention prompts, scripts, pipelines, agents or colour codes. State the valuation basis once, in the methodology, in accounting language: assets are carried at the cost the facility records state; where a facility record carries no cost, the unit cost recorded for the same item elsewhere in the programme is applied; depreciation is straight line over the useful lives in Annex 1 of the Government of Uganda Asset Accounting Policies and Guidelines 2023 with nil residual value. Then leave it there.
- Do not present a value the register does not hold. A blank stays out of the total; label totals "recorded value" and do not add a column or sentence counting assets without a value.
- Do not invent maintenance arrangements, dates, counts or reasons. Where the records do not say, leave the point out.
- Do not comment on the completeness, quality or consistency of the field records, the returns or the register, and do not describe how gaps were handled. The quality-assurance section of the methodology describes the controls that were applied, as the draft gives them, and that is the only place the subject arises.
- Facilities that were not verified on the ground appear only in the reconciliation of the master list (7.1 and its appendix), each with the reason the supervisor's reconciliation records, in neutral wording. Write "was confirmed on the ground as", "was replaced by", "does not exist under the programme", "is not a UgIFT beneficiary", "was reconciled to". Do not write "failed to", "did not visit", "could not be reached", "no return was received", "was omitted", "the team did not" or any wording that assigns the outcome to the field teams. The reconciliation is presented as part of a verification process that accounted for every facility.

## Photographs

Use photographs where they carry the point: an unengraved item, equipment still in its box in a store, a damaged desk, a completed and occupied block, a well-kept register at a facility. Take them from the loose image files and from the documents the teams generated:

- Word returns and district reports: extract the embedded images from `word/media/` (open the `.docx` as a zip, or use python-docx `document.part.related_parts` to keep the order in which they appear). Read the paragraph or table cell next to each image for its caption, item name and facility, since the file name inside the document is only `image12.jpeg`. The district reports in `_district-documents/` and the Karamoja photographic gallery are the richest sources for well-composed photographs of buildings, furniture and equipment; the facility returns give close-ups of tags, engraving and condition.
- PDF scans: extract page images with PyMuPDF (`page.get_images` and `Document.extract_image`) or render the page at 200 dpi where the photograph is part of a scanned page; crop to the photograph.
- Loose files: use as they are.
- Choose sharp, well-lit, straight images where the asset fills the frame. Skip blurred, dark or cluttered photographs, screenshots of chats, and photographs of filled forms or registers that show names or signatures.
- Prefer photographs without people. Never use a photograph that shows an identifiable face, a name badge, a signature or a document with personal names. Crop when needed.
- Caption each photograph with what it shows, the facility type, the local government and the sub-region, for example "Figure 4: Delivery bed in use, maternity ward, health centre, Busia District (Bukedi)". No facility-level names are needed in the caption unless the point depends on it.
- Resize to at most 1600 pixels on the long side and save a copy in `figures/`; keep the Word file under 30 MB.
- Record the source of every photograph in `sources.md`: the file path, and for an embedded image the document path with the image's position (for example `image12`, table 6, the caption text beside it) so it can be found again.
- Use between eight and sixteen photographs across the report; one or two per region and per theme is enough. Spread them across regions and across both facility types, and include at least one from a national-level MDA where the documents provide it.

## Charts

Draw charts with matplotlib, one message per chart, and save them to `figures/` before inserting. Required charts:

1. Facilities covered by region and type (health centres, seed schools), with facilities not found on the ground shown separately.
2. Assets verified by report category (stacked by functional and non-functional, over the assets assessed for condition).
3. Functional and non-functional assets by sub-region.
4. Engraved with UgIFT marking, engraved with other marking, not engraved, by region.
5. Recorded value and net book value by region and by MDA.
6. Assets in use, not in use due to damage, and not in use but in good condition, by category.

Chart rules: a title that states the finding, labelled axes with units, data labels on bars, a legend only when there is more than one series, one consistent colour palette with the same colour for the same status on every chart, no 3D, no pie charts with more than four slices, and a source line under each chart describing the evidence in plain language, such as "Source: UgIFT asset verification records." Explain any scope or denominator in asset terms. Keep the workbook name and exact filter in `sources.md`. Put the table behind every chart in the appendix.

## Style

- Professional, plain English, in the past tense for what was done and the present tense for what the register shows. Short paragraphs, three to five sentences. Active voice.
- No em dashes or en dashes anywhere, in text, tables or captions; use a comma, a full stop, a colon, or the word "to" for ranges. No emoji, no exclamation marks, no rhetorical questions.
- Do not use these words and phrases: delve, robust, leverage, seamless, holistic, cutting-edge, comprehensive overview, in conclusion, it is important to note, it is worth noting, moreover, furthermore, additionally, as previously mentioned, in today's world, a testament to, tapestry, landscape (except a physical one), navigate, unlock, harness, elevate, journey, crucial, vital, pivotal, game-changer.
- Do not open paragraphs with "Overall", "Notably", "Importantly" or "Interestingly". Do not end sections with a summary sentence that restates the section.
- Use numerals for counts and money, with thousands separators; write UGX before the amount (UGX 3,500,000). Percentages to one decimal place. Dates as 24 August 2026.
- Number tables and figures (Table 1, Figure 1) and refer to them by number in the text. Every table has a caption above and a source line below, using the source-presentation rules above.
- Spell each acronym out at first use and list it in the acronyms table.
- Be complete and concise: every section of the outline is present and says what the records support, and nothing is padded. Aim for 35 to 55 pages including appendices, with the executive summary at most two pages.

## When something is unclear

Go back to the source before writing. If the register and a template disagree, the register is the record and the report says what the register shows. If the source itself is unclear on a point, leave that point out of the report and note in `sources.md` what you checked. Never resolve an unclear point by choosing the more favourable reading, and never qualify a statement in the report with words such as "not stated", "not recorded", "could not be verified", "unclear" or "unknown".

## Building the files

- Build the Word document with python-docx (or the document skill available in the session): Calibri or a similar clean typeface, 11 point body, 1.15 line spacing, headings in the built-in Heading styles so the table of contents works, page numbers in the footer, tables in a light grid style with header rows repeated, figures centred with captions.
- Insert a table of contents field and update it, or write the contents list from the headings.
- Convert to PDF with the tool available on the machine (Word automation via docx2pdf, or LibreOffice headless). Open the PDF and check page count, that no table runs off the page, and that every figure is present.

## Final checks before you finish

1. Run a text scan over the Word document: zero em dashes or en dashes; zero personal names (check against the speaker column of `supervisor-decisions.csv`, the field-team names in `team-distributions.docx`, and the names in the draft report); zero occurrences of the banned words and of fabricated, generated, auto, synthetic, simulated, AI, model, prompt, script, borrowed, colour; zero occurrences of not stated, not recorded, no record, not available, could not be verified, unverified, unclear, unknown, missing data, incomplete, inconsistent, gap, failed to, did not visit, no return (the client's own category "not in use" is allowed, and in section 7.1 and its appendix the reconciled outcomes "does not exist", "was replaced by", "was confirmed on the ground as", "is not a UgIFT beneficiary" and "found on the ground but not on the master list" are allowed).
2. Every number in the executive summary appears in the body with a source.
3. Every table and chart total reconciles to a filter on the REF register that you can restate in `sources.md`.
4. Every acronym is in the list; every figure and table is numbered and referenced.
5. The PDF opens and matches the Word file page for page.
6. `sources.md` is complete and retains exact filenames, worksheet ranges and filters for internal traceability.
7. Scan the Word document and PDF text, tables, captions, notes, appendices and hyperlink targets for direct references to files under `outputs/asset-register/`, including register filenames, paths and REF/MF/SK workbook labels. Remove these from the report while retaining their provenance in `sources.md`. Review uses of "row", "record", "entry" and "line" and use "asset" wherever they refer to a physical item or its count. Confirm that these wording changes leave all asset counts and monetary amounts unchanged.

In your reply (not in the report), give a short note of what you produced, the page count, the headline numbers, and the points you left out because the records did not support them.
