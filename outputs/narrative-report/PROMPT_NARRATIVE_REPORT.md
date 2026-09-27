# Prompt: write the UgIFT asset verification narrative report

You are writing the end-of-programme asset verification report for the UgIFT programme, as a Word document and a PDF. It is a high-level narrative for senior readers at the Ministry and its partners. Everything in it must come from the files listed below. Where a file does not state something, say that the verification records do not state it, and cite the file you checked. Do not fill a gap with an assumption.

## Outputs

Write into `outputs/narrative-report/`:

1. `UgIFT Asset Verification Report.docx`
2. `UgIFT Asset Verification Report.pdf` (converted from the Word file; open the PDF and confirm every page rendered, tables did not split badly, and every figure and photo is visible)
3. `figures/` holding every chart as a PNG at 200 dpi and every photograph used, as copied and resized
4. `sources.md` listing, for every table, chart, photograph and headline number in the report: the file, sheet or table, and the row range or filter used

Do not change any file under `raw-data-grouped/`, `outputs/asset-register-2026-09-23/` or `outputs/report-templates/`.

## Read these before writing

- `outputs/report-templates/Report outline _ BB input.docx`: the agreed structure. Follow its sections and order.
- `outputs/report-templates/Verification report_ 24092026_Draft_ BB.docx`: the client's draft. Reuse its background, objectives, scope, project context and methodology content, rewritten in the style rules below and with every personal name removed.
- `outputs/report-templates/WhatsApp Image 2026-09-25 at 15.07.09.jpeg`: a handwritten list of the counts the client wants. Every item on it becomes a row of the summary table in the findings (see "Required summary counts").
- `outputs/asset-register-2026-09-23/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`: the register the numbers come from (sheet `Asset Register`, one row per physical asset, 64 columns; the `Read Me` sheet explains every column). Use `ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx` when you need the wording the field team wrote, and `BOOK_TYPE_CODE.md` for the list of votes.
- `outputs/asset-register-2026-09-23/ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`: the same rows with only the values the field records state. Use it when the report must say what was recorded on the ground rather than valued.
- `raw-data-grouped/README.md`, `raw-data-grouped/facility-data-status.pdf`, `raw-data-grouped/facility-reconciliation.csv`, `raw-data-grouped/master-source-rows.csv`, `raw-data-grouped/supervisor-decisions.csv`: facility coverage, facilities on the master list that were not found or were renamed, facilities found on the ground that were not on the list, and the decisions taken on them.
- `SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx` (columns Region, Sub-region, District, School or sub-county, Phase, Status) and `team-distributions.docx` (Region, Local Government, numbers of schools and health facilities): the region and sub-region of every local government, and the number of facilities per local government.
- `GOU Asset Accounting Policies and Guidelines 2023.pdf`, sections 3.2.1, 3.3.3, 5.5 and 5.7 and Annex 1: the recognition, useful-life and depreciation basis the register applied. Cite the section when the report explains a valuation.
- Photographs: `raw-data-grouped/team-NN/<Local government>/<Facility>/*.jpg|jpeg|png` and `raw-data-grouped/team-NN/_team-documents/`. Their folder names give the local government and facility.
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
   - 7.1 Introduction to the findings: coverage (facilities on the master list, facilities with a return, facilities counted as explained cases, facilities found on the ground that were not on the list) from the reconciliation files.
   - 7.2 National level: one sub-section per MDA in the order the outline lists them (MoFPED, MoWT, MoES, MAAIF, MoH, OPM, MoWE, MoGLSD, NEMA, PPDA, OAG, MoLG, MoLHUD, LGFC, MoPS). For each: a table with asset category, quantity, total recorded cost, accumulated depreciation, net book value and status, then two to four sentences on engraving and operations and maintenance. Where the register holds no rows for an MDA, write that no UgIFT assets were recorded for it in the verification records and cite `BOOK_TYPE_CODE.md`.
   - 7.3 Local government level by region and sub-region: Central; Eastern (Bugisu, Bukedi, Busoga, Teso, Sebei); Northern (Acholi, West Nile, Lango, Karamoja); Western (Ankole, Bunyoro, Rwenzori, Tooro, Kigezi). For each region: the number of health centres and seed schools covered, then health centre assets by the outline's categories (clinical equipment; clinical furniture; maternity ward equipment; ICT equipment; building blocks) and school assets by its categories (building blocks; furniture, meaning desks, tables, chairs and stools; computers and related equipment excluding network switches; support equipment, meaning printers and cameras and projectors). For each category give number, status and recorded value, then a brief on maintenance arrangements drawn from the remarks and interviews. Give the sub-region breakdown as a table or chart under each region. List the facilities on the master list not found on the ground and the facilities found that were not on the list, per region, from `facility-reconciliation.csv`.
   - 7.4 Functionality of assets: functional and non-functional counts by category and by sub-region, as charts, with the underlying table in an appendix.
   - 7.5 Asset management practices and risks: observations on storage, utilisation, records, breakdowns and maintenance with specific local-government examples (the local government, not the person); the risks and challenges; then recommendations on identification (engraving), registration and maintenance, and future programming.
   - 7.6 UgIFT support to service delivery: issues, challenges and recommendations, from the interview and remark records.
8. Appendices: the summary count table in full; the functionality tables behind the charts; the list of facilities not found and facilities not on the list; a note on the IFMIS-ready registers (file names, row counts, columns) that the client receives with this report; the sources list.

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
| Total assets verified by category | count of rows by `ASSET_CATEGORY_MINOR2`, and by the report categories above |
| Facilities which had shared assets out with others | facilities whose remarks say an asset was shared with, lent to, moved to or kept at another facility or the district |
| Facilities not on the master list but found in the local governments | `facility-reconciliation.csv` rows whose scope is a ground return only (X ids) |
| Facilities on the master list but not on the ground, including changed names | `facility-reconciliation.csv` and `supervisor-decisions.csv` rows recording non-existence, replacement or renaming |
| Total number by category | facilities and assets by category and by region |

Count rows, not lines: the register already holds one row per physical asset. Where a row's status is blank, count it as "status not stated" and show that column too; do not fold it into functional or non-functional.

## Mapping the register to the report's categories

- Buildings: `ASSET_CATEGORY_MAJOR` = `BUILDINGS AND STRUCTURES`; work in progress is `ASSET_TYPE` = `CIP`.
- Furniture: `ASSET_CATEGORY_MINOR2` = `FURNITURE AND FITTINGS`. School furniture is that class at a seed school; clinical furniture is that class at a health centre plus beds, couches, trolleys, screens, stands and lockers from `MED LAB RESEARCH APPLIANCES` whose name says so.
- Vehicles and motorcycles: `ASSET_CATEGORY_MINOR1` = `TRANSPORT EQUIPMENT`.
- ICT: `ASSET_CATEGORY_MINOR1` = `ICT EQUIPMENT`; "computers and related equipment excluding network switches" leaves out names containing switch; "support equipment" is printers, photocopiers, cameras and projectors.
- Clinical equipment: `MED LAB RESEARCH APPLIANCES` at a health centre, less the clinical furniture above.
- Maternity ward equipment: rows whose `LOCATION_SEGMENT2` or item name says maternity, delivery, labour, antenatal, postnatal, kangaroo or neonatal.
- Health centre or school: `Facility type:` in `ATTRIBUTE15(Remarks)` (Health centre, School); the MDA rows have Facility type MDA, Hospital or Blood bank and belong to the national level.
- Value: `FIXED_ASSETS_COST` is the recorded cost, `DEPRN_RESERVE` the accumulated depreciation to 30 September 2026, and net book value is cost less accumulated depreciation, floored at zero. Sum by group; show UGX with thousands separators and no decimals.
- Region and sub-region: join `BOOK_TYPE_CODE` (the local government) to the district's Region and Sub-region in `SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx`; a city or municipal council takes its district's region. Record any local government you could not place in `sources.md` and show it under "Not placed" rather than guessing.

State the mapping you applied in one paragraph of the methodology and in `sources.md`.

## What the report must not say

- No personal names anywhere: not officials, not field staff, not chat participants, not head teachers or in-charges, not in photo captions, not in the acknowledgements. Refer to roles: the Accounting Officer, the health centre in-charge, the head teacher, the district health officer, the Consultant, the Client, the field team, the supervisor.
- No telephone numbers, chat handles or email addresses.
- Do not describe any figure as fabricated, generated, auto-generated, synthetic, simulated, invented, borrowed, imputed by software, or produced by AI or by a model. Do not mention prompts, scripts, pipelines, agents or colour codes. State the valuation basis once, in the methodology, in accounting language: assets are carried at the cost the facility records state; where a facility record carries no cost, the unit cost recorded for the same item elsewhere in the programme is applied; depreciation is straight line over the useful lives in Annex 1 of the Government of Uganda Asset Accounting Policies and Guidelines 2023 with nil residual value. Then leave it there.
- Do not present a value the register does not hold. A blank stays out of the total, and the table shows how many assets carry no recorded value.
- Do not invent maintenance arrangements, dates, counts or reasons. If the records do not say, write that they do not say and cite the file.

## Photographs

Use photographs where they carry the point: an unengraved item, equipment still in its box in a store, a damaged desk, a completed and occupied block, a well-kept register at a facility. Rules:

- Choose sharp, well-lit, straight images where the asset fills the frame. Skip blurred, dark or cluttered photographs.
- Prefer photographs without people. Never use a photograph that shows an identifiable face, a name badge, a signature or a document with personal names. Crop when needed.
- Caption each photograph with what it shows, the facility type, the local government and the sub-region, for example "Figure 4: Delivery bed in use, maternity ward, health centre, Busia District (Bukedi)". No facility-level names are needed in the caption unless the point depends on it.
- Resize to at most 1600 pixels on the long side and save a copy in `figures/`; keep the Word file under 30 MB.
- Record the source path of every photograph in `sources.md`.
- Use between eight and sixteen photographs across the report; one or two per region and per theme is enough.

## Charts

Draw charts with matplotlib, one message per chart, and save them to `figures/` before inserting. Required charts:

1. Facilities covered by region and type (health centres, seed schools), with facilities not found on the ground shown separately.
2. Assets verified by report category (stacked by functional, non-functional, status not stated).
3. Functional and non-functional assets by sub-region.
4. Engraved with UgIFT marking, engraved with other marking, not engraved, by region.
5. Recorded value and net book value by region and by MDA.
6. Assets in use, not in use due to damage, and not in use but in good condition, by category.

Chart rules: a title that states the finding, labelled axes with units, data labels on bars, a legend only when there is more than one series, one consistent colour palette with the same colour for the same status on every chart, no 3D, no pie charts with more than four slices, and a source line under each chart naming the register and the filter. Put the table behind every chart in the appendix.

## Style

- Professional, plain English, in the past tense for what was done and the present tense for what the register shows. Short paragraphs, three to five sentences. Active voice.
- No em dashes or en dashes anywhere, in text, tables or captions; use a comma, a full stop, a colon, or the word "to" for ranges. No emoji, no exclamation marks, no rhetorical questions.
- Do not use these words and phrases: delve, robust, leverage, seamless, holistic, cutting-edge, comprehensive overview, in conclusion, it is important to note, it is worth noting, moreover, furthermore, additionally, as previously mentioned, in today's world, a testament to, tapestry, landscape (except a physical one), navigate, unlock, harness, elevate, journey, crucial, vital, pivotal, game-changer.
- Do not open paragraphs with "Overall", "Notably", "Importantly" or "Interestingly". Do not end sections with a summary sentence that restates the section.
- Use numerals for counts and money, with thousands separators; write UGX before the amount (UGX 3,500,000). Percentages to one decimal place. Dates as 24 August 2026.
- Number tables and figures (Table 1, Figure 1) and refer to them by number in the text. Every table has a caption above and a source line below.
- Spell each acronym out at first use and list it in the acronyms table.
- Be complete and concise: every section of the outline is present and says what the records support, and nothing is padded. Aim for 35 to 55 pages including appendices, with the executive summary at most two pages.

## When something is unclear

Go back to the source before writing. If the register and a template disagree, the register is the record and the report says what the register shows. If the source itself is unclear, say so plainly and cite it, for example "The return for this facility records the asset as received but does not state its condition (facility return, table 6)". Never resolve an unclear point by choosing the more favourable reading.

## Building the files

- Build the Word document with python-docx (or the document skill available in the session): Calibri or a similar clean typeface, 11 point body, 1.15 line spacing, headings in the built-in Heading styles so the table of contents works, page numbers in the footer, tables in a light grid style with header rows repeated, figures centred with captions.
- Insert a table of contents field and update it, or write the contents list from the headings.
- Convert to PDF with the tool available on the machine (Word automation via docx2pdf, or LibreOffice headless). Open the PDF and check page count, that no table runs off the page, and that every figure is present.

## Final checks before you finish

1. Run a text scan over the Word document: zero em dashes or en dashes; zero personal names (check against the speaker column of `supervisor-decisions.csv`, the field-team names in `team-distributions.docx`, and the names in the draft report); zero occurrences of the banned words and of fabricated, generated, auto, synthetic, simulated, AI, model, prompt, script, borrowed, colour.
2. Every number in the executive summary appears in the body with a source.
3. Every table and chart total reconciles to a filter on the REF register that you can restate in `sources.md`.
4. Every acronym is in the list; every figure and table is numbered and referenced.
5. The PDF opens and matches the Word file page for page.
6. `sources.md` is complete.

Report what you produced, the page count, the headline numbers, and anything the records could not support, in a short note at the end of your reply.
