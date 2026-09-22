# Field register rules

These rules govern everything under `facility-registers/` — which facilities appear here,
what each team must produce, how every file is named, and how the tree is mirrored to
Google Drive (section 7). They apply to every team.

They exist because the exercise has several sources that look interchangeable and are not.
Confuse them and the register reports assets as verified when nobody has seen them.

## 1. What each source proves

| Source | Proves | Never use it to show |
|---|---|---|
| **Hand-filled asset register** — the UgIFT toolkit filled in on site by the team | The facility's assets **have been verified**; the official name, quantity and condition of each | — |
| **Delivery note, invoice, any financial document** | What was **supplied**, and an item's official name. At district level it also stands as the record of assets (2.1) | What is **on the ground**. Supplied is not found |
| **Programme supply worksheets** — `source-documents/assets-supplied-by-ugift/` | Official equipment names and, where the sheet carries them, unit costs of what UgIFT procured | What is **on the ground**. A worksheet quantity is not a found quantity |
| **The team's field report** | What the team **reported** seeing, in their words, with the date and who recorded it | That a facility has been verified |
| **The photograph** | What the asset physically is — make, model, type, labels, plates | Quantity or condition beyond what is visible |
| **External reference** — maker's documentation, product listings | The make, model or specification of an item already photographed | Anything about this facility |

Supplied and found are never merged. They may agree; they may not, and that difference is
the point of the exercise.

## 2. Which facilities are included

**A facility is verified only once a hand-filled asset register for it is on file.** Nothing
else does it: a delivery note shows assets were supplied, the field report shows the team
reported, and a visitors' register shows the team signed in.

### 2.1 District and facility are held to different standards

| Level | Acceptable record of assets |
|---|---|
| **District** | A financial document will do — delivery note, invoice, IFMS listing. This is what facility holdings are checked against |
| **Facility** | Only its **own asset register, filled in on site**. A delivery note naming it is not enough, however detailed |

Each is asked a different question. The district is asked what it procured, which is a
financial fact. A facility is asked what it holds today, which no financial document can
answer: an item can be supplied and never arrive, arrive and be moved, or arrive and break.

### 2.2 The three states

| State | Test | What it gets |
|---|---|---|
| **Verified** | A hand-filled register is on file | A folder, a toolkit written up from that register (3.1), a facility report |
| **Reported, not verified** | The team went and returned evidence, but no register | A folder with its photographs and its facility report, and **no toolkit** (3.1) |
| **Pending** | No field return yet | No folder. Named, with the reason, in the local government report's coverage (3.2) |

**The third state is *Pending*, never *not reached*.** The exercise is not closed: a facility
with no return is outstanding work needing an owner and a date. *Pending* asks who is going
and when; *not reached* asks nothing.

**Where a facility is Pending, every other status for it is Pending too.** In the local
government coverage table, in the four dimensions if the facility is named, and anywhere else
a status is recorded — incomplete, photographs, ownership, functionality, usage/performance,
location — each reads *Pending*. Nothing mixes *Pending* with *not reported*, a count, *no
record* or *yes*/*no* for a visit that never happened.

Where a whole local government has no return it has no folder, so its Pending facilities are
named in the team's process report (3.3) instead.

A folder means a return exists, not that anything is verified. Evidence the team gathered is
never deleted for want of the register that should have come with it.

**When the team reached a facility but could not work it through**, the visit still counts.
The team may find the school closed, nobody on site, a store or laboratory locked, keys held
by someone who does not answer, the works under construction, or the facility finished but
not yet commissioned. Those are the facility's circumstances, not a failure to go. Where the
record shows the team was there — a facility report, photographs, a field note, a dated
entry — the facility gets a folder (2.2), counts as **reported on** in the reconciliation,
and earns its unit in the progress score (3). It is **not** *Pending*.

In the local government coverage table, such a facility's **state** reads **complete**. The
**incomplete** column names what could not be done — no register, outside frames only, store
inaccessible, under construction — and the queries say who must act next. *Complete* means
the visit is closed for this exercise; it does not mean a hand-filled register is on file
and it does not mean every item was counted. Only a register on file makes a facility
**verified** in the sense of section 2 and earns a toolkit (3.1).

### 2.3 An incomplete return is marked, never left to inference

A facility can have a folder, photographs and a report and still fall well short. **Every
facility whose return falls short is marked by name** — in the local government report's
coverage. A return is incomplete if any of these is true:

| What is missing | Why it matters |
|---|---|
| No hand-filled register naming the facility | Nothing at it is verified (section 2) |
| No photograph of any asset | The status of every item is unevidenced |
| The discussion guide unanswered | How the facility records and maintains its assets is unknown |
| No quantity against any item | Nothing can be set against what was supplied |
| No engraved number or serial number recorded | No item can be identified again |
| Any of the four dimensions unreported | Ownership, functionality, usage or location was not established |
| A source in hand that cannot be read | The line exists and its value does not |

Each is also a query with an owner (3.4). The mark says at a glance that the facility is not
finished; the query says what to do and who does it.

### 2.4 How many, and which

Two documents answer two different questions, and neither answers the other's:

| Question | Authority |
|---|---|
| **How many** facilities a team owes in a local government | `source-documents/Updated Team distribution by sub region-Names-Transport.docx` |
| **Which** facilities those are | The schools and health centres list, as `src/facilities.py` |

So a reconciliation counts against the **allocation**, and names facilities from the **list**.

Where the two disagree, neither is corrected from the other. The allocation governs the
count, the list governs the names, and **the difference is stated and carried as a query**.
A local government allocated three schools where the list names two is short one school by
name; that is a finding for the district education officer, not an arithmetic error to
smooth over.

## 3. Reporting documents required for each team

Every team owes the same set for every local government it covers, plus one document for the
assignment as a whole. The set comes from `source-documents/`: the verification process
deck, the quality assurance deck, the toolkit, and the process report template.

A district folder is **not complete** until the documents it owes exist, and whatever is
missing is named in that local government's report, under coverage and under outstanding
queries (3.2). The team documents folder is held to the same standard; belonging to no one
district, its gaps are named in the report of every local government the team worked.

**Progress score.** Completion percentages (`facility-registers/progress-report.pdf`,
`src/progress_report.py`) count **four** reporting documents per local government:

1. `LG-asset-register-review.docx`
2. `LG-report.docx` (the local government report)
3. the team's daily log for that local government
4. the team's process report

and **three** units for each allocated facility:

1. a folder (the team reached it)
2. the hand-filled toolkit — photographed or scanned pages that name the facility
3. `Asset-Verification-Toolkit.docx` written up from that copy (3.1)

A folder follows a return of any kind (2.2), so a facility the team reached but could
not enter — closed, keys missing, under construction, not yet commissioned — still
earns the folder unit. The hand-filled copy and the Word toolkit are the team's own
to produce; a missing one marks the team down.

**The courtesy call, officer interviews and debrief are outside the algorithm.** They
are not scored units, they do not fill a missing scored document, and they do not add
or subtract from the percentage whether they exist, are late, or are absent.

### 3.1 Per facility

Lives in `<team>/<district>/<facility>/`.

| Document | Required by | Scored |
|---|---|---|
| Hand-filled toolkit — photographed or scanned pages that name the facility | The toolkit | **Yes** |
| `Asset-Verification-Toolkit.docx` — the programme toolkit, filled from that copy | The toolkit | **Yes** |
| The facility report, named per 3.9 | House format (3.5) | No |
| Photographs showing the **status** of each asset | Process deck, slide 5 | No |

**The toolkit is written up from the hand-filled copy, not compiled.** Every verified
facility gets its own `Asset-Verification-Toolkit.docx`, filled from
`source-documents/ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx` using the toolkit the
team filled in by hand on site, as photographed. That copy is the source of truth for every
**line that exists** — which items were found, in what quantity and condition. Names,
descriptions and prices on those lines may then be completed from the sources in 3.1a.
It follows that:

- A toolkit may **not** be built from the field report, a delivery note, a supply
  worksheet, or any reconstruction of them. Those answer different questions (section 1).
  They may complete a line the hand-filled copy already carries, as 3.1a allows; they may
  not invent a line.
- With no hand-filled copy on file, **no toolkit is produced**. The folder holds the
  photographs and nothing more, and the absence is a query.
- An illegible quantity, status, tag, date or other verification fact is left blank and
  raised as a query, never inferred. An unclear name, a missing description or a missing
  price is completed from 3.1a, not left empty for want of a clear hand.

Use the right path: **health centre** — discussion guide (1a, 1b, 2, 3, 4) then the health
centre checklist; **school** — the same five questions then three schedules, furniture, ICT
items and buildings.

The interview must actually be held: the toolkit says *"proceed to verification after this
discussion"*. An unanswered guide is an incomplete return, not a formality.

**A filled toolkit carries, in order:**

1. **Verification details** — region · sub-region · local government · verifier full
   name · verifier contact · supervisor name · supervisor contact · date of submission.
   Filled for every facility per 3.15.
2. **Discussion guide**, answered — *1a* does the facility hold a record of all UgIFT assets
   (obtain it; check costs and numbers supplied); *1b* if not, how many were supplied and
   when; *2* how it maintains them; *3* whether functionality and breakdown are recorded;
   *4* how the support has helped service delivery, with issues and recommendations.
3. **Asset schedules** — the health centre checklist, or a school's three schedules. Every
   schedule has the same fifteen columns:

   ```
   Equipment/Item · Department · Asset Number · Item Description · Life in Months ·
   Tag Number (engrave no.) · Date of Purchase · Date Placed in Service ·
   Recoverable cost · Cost · Acc Dep Cost · Net Book Value · Ytd Deprn ·
   Equipment status · Remarks
   ```

   Department, asset number, life in months, dates of purchase and of placing in service,
   recoverable cost, and the three depreciation columns stay blank unless the hand-filled
   copy or the LG asset register gives them (section 5). **Cost**, **Equipment/Item** and
   **Item Description** are completed per 3.1a. A unit price is Cost, not recoverable cost,
   and is never spread into depreciation.

**Where the hand-filled pages are on file as photographs, the Word toolkit
(`Asset-Verification-Toolkit.docx` only — no PDF of the toolkit) is written up from those
pages and placed in the facility folder.** Until that write-up is done the photographs stay
on file and the facility is still verified by the named hand-filled copy (section 2); the
Word file is what the supervisor opens.

**3.1a Completing names, descriptions and prices.**

The hand-filled copy says what was found. These three columns may be finished from other
sources **on a line that copy already carries**. Nothing here adds a line, a quantity or a
status.

**Equipment/Item.** If the hand-filled name is clear, it stands (4.1). If it is abbreviated,
misspelt, colloquial, only partly readable, or does not identify the item, use the official
name from, in this order: the programme supply worksheets in
`source-documents/assets-supplied-by-ugift/`; then any applicable document that names the
same item — a delivery note, invoice, IFMS listing, the facility's own asset register, or
the LG asset register. Match the item, not the facility's guess at the name. Record the
substitution (4.3).

**Item Description.** Fill from, in this order: the hand-filled copy; the facility's own
asset register; the LG asset register; the photograph of that asset. A photograph may
supply only what it shows — make, model, type, labels, serial plates, signage. It does not
fill quantity, condition or any other column (section 1).

**Cost.** Fill from, in this order: the hand-filled copy; the LG asset register; a unit
cost on the programme supply worksheets in `source-documents/assets-supplied-by-ugift/`.
Match the official equipment name. Prefer the worksheet that names this facility, then
this local government, then the financial year the tag or the hand-filled heading carries
(upgraded against upgraded, newly constructed against newly constructed). Write the unit
cost into Cost. If the sheet gives only a total and no unit cost, leave Cost blank. If two
worksheets give different unit costs for the same item, use the one that matches this
facility's year or lot and raise the difference as a query. Where no worksheet prices the
item, Cost stays blank.

The four workbooks in that folder are the programme's own procurement and distribution
lists. A quantity on them is what was **supplied**. It is never written in as found.

**The facility report** carries what the form cannot — what the visit found. Eight sections:

1. **Identification** — facility and type, local government, region and sub-region, date of
   visit, members present, who was interviewed and their role, supervisor and supervisor's
   contact (3.15), date of submission (3.15).
2. **Entry** — visitors' register signed, and any access problem.
3. **Condition and status** — the four things the exercise establishes, each answered:
   **ownership**, **functionality**, **usage/performance**, **location**.
4. **Supplied against found** — what the record says was supplied, what was seen, and every
   difference, item by item. Never a merged figure.
5. **Engraving and identification** — which assets carry engraved or serial numbers.
6. **Obsolete, unserviceable or for disposal** — with the reason.
7. **Operation and maintenance** — what the facility reported about functionality and
   maintenance.
8. **Queries** — anything unresolved, illegible or contradictory, each with an owner.

No report carries a photographic index. The photographs sit beside it, named for what they
show.

### 3.2 Per local government

Lives in `<team>/<district>/_district-documents/`. One local government is one folder.

| Document | What it records | Source | Scored |
|---|---|---|---|
| `LG-asset-register-review.docx` | Review of the record of assets held at the LG — a financial document is acceptable (2.1). **Written for every visited local government**: if the district produced a record, that record is reviewed; if it produced nothing, the review says so | Process deck, slides 4–5 | **Yes** |
| `LG-report.docx` | The report for the LG, **with photos**, to the supervisor: general issues found and the challenges of asset management | Process deck, slide 5 | **Yes** |
| `LG-courtesy-call.docx` | The call on the LG leadership, purpose of visit, and the visitors' book signed at the CAO's or Town Clerk's office | Process deck, slide 4 | No |
| `LG-officer-interviews.docx` | Interviews with the CFO, DEO and DHO on asset management practice and challenges | Process deck, slide 4 | No |
| `LG-debrief-note.docx` | The debrief given to the LG on key findings | Process deck, slide 5 | No |

**The scored set is the four local-government documents** (asset-register review,
local government report, daily log, process report) **plus the hand-filled toolkit
and the Word toolkit for each allocated facility** (3, 3.1). The courtesy call,
officer interviews and debrief may still be written when the record supports them;
they are never counted into completion percentages, never used as substitutes for
a scored document, and a missing one does not mark the team down.

**The local government report is a brief**, not a retelling of every facility. The detail
lives in the facility reports. Eight sections:

1. **Identification** — local government, region and sub-region, team and members,
   supervisor and supervisor's contact (3.15), dates worked, date of submission (3.15).
2. **Coverage** — one row per facility: type, state, whether the return is **incomplete**
   (2.3), photographs. Facilities still **Pending** are listed with the rest (2.2); every
   column for a Pending facility reads *Pending* (2.2). A facility the team reached but
   found closed, inaccessible, under construction or not yet commissioned reads **complete**
   in the state column (2.2), not *Pending* and not *reported, not verified* unless nothing
   on file shows the team was there. Then the reconciliation in one line: allocated,
   reported on, verified — where *reported on* is every facility with a folder and
   *verified* in that line is the count of those whose state is **complete** or that carry
   a hand-filled register, not the register count alone (2.2, 2.4).
3. **The local government record** — rows for the documents that exist: record of assets
   (always), and courtesy call, officer interviews or debrief only when written. Present
   or no record, nothing more.
4. **Key findings** — the brief itself, in a handful of bullets.
5. **Supplied against found** — which facilities can be compared and which cannot, in a
   short paragraph.
6. **Obsolete, unserviceable or for disposal** — one line each.
7. **Outstanding queries** — one line each.
8. **Sign-off** — verifier, supervisor, supervisor's contact, date of submission (3.15).

It carries no per-facility narrative, no photographic index, and no restatement of the
standalone LG documents.

### 3.3 Per team

Lives in `<team>/_team-documents/`.

| Document | What it records | Source |
|---|---|---|
| `daily-log.docx` | Each researcher's daily activities: local governments covered and assets verified that day | QA deck, slide 5 |
| The process report, named per 3.9 | The team's field report on the assignment | The process report template |

**The process report is one per team, not one per district.** A team covering four local
governments writes one report covering all four. It is the only document in this section
whose scope is the team.

Its structure is **mandated** (3.5), from the template the central technical team issued. It
opens with the template's title, *Field report on UgIFT asset verification*, and the team
and dates beneath. Four sections:

1. **Introduction** — the exercise, the sub-region and local governments allocated, the
   dates worked.
2. **Process/methodology** — what was done and how. The template requires two things by
   name: **the team members**, and **the local governments verified**. Verified means what
   section 1 means, so a local government where no facility has a register on file is named
   as covered, not verified.
3. **Emerging issues/challenges** — what the exercise ran into **in the assets, and in the
   local government and facility personnel who hold them**.
4. **Recommendations** — what should be done, and by whom.

**Those last two sections are about the assets** and the people who hold and manage them:
how assets are documented at district and facility, identified, counted and engraved,
maintained and repaired, what they are used for, and how the officers and staff answerable
for them are managing them.

**They are not about the verification team.** Its staffing, travel, funding and fortunes are
not asset findings, and a recommendation addressed to the team belongs in the daily log or
with the supervisor. What a team's own difficulty earns is its consequence for the assets:
where a custodian was absent, the finding is that the discussion guide is unanswered and
practice unknown — not that a journey was wasted.

The process report is not a second LG report: no per-facility narrative, no coverage table,
no asset findings. It does name facilities still **Pending** (2.2), because for a local
government with no return this is the only document that can.

Everything governing other reports governs this one — 3.6 to 3.13.

- **Nothing is recommended that the record does not support.**
- **A thin return makes a short report, not an invented one.**

Enforced: `src/build_reports.py` fails the build if the issues or recommendations mention
the team, a researcher, a member or the supervisor.

### 3.4 Completeness and follow-up

Incompleteness is chased, not recorded and left. A missing or half-filled document is an
open item with an owner, and belongs in that local government's report under *Outstanding
queries* (3.2) until closed.

### 3.5 Mandated versus house format

**Mandated by `source-documents/`** — the filled toolkit and its structure; the asset
register review; the LG report with photos; the brief on issues and asset-management
challenges; each researcher's daily log; the four dimensions — ownership, functionality,
usage/performance, location — and listing assets obsolete, unserviceable or for disposal;
the process report's title and four sections; and the allocation counts (2.4).

The courtesy call, officer interviews and debrief remain useful when the record supports
them; they are **not** part of the progress score and they never enter the score
calculation (3, 3.2). The hand-filled toolkit and the Word toolkit **are** part of
the progress score (3, 3.1).

**House format, defined here** — the section structure of the facility report and the LG
report, the file names, the folder layout, the dates rule in 3.6, and the particulars in
3.15.

`source-documents/Presentation Template -UGFT 2.pptx` is **not** a report template despite
its name: it is the training deck, on stock slide layouts, with no report placeholders.
`source-documents/Process report template.docx` is the real thing, and governs the process
report (3.3) and nothing else.

If the supervisor or the central technical team issues a house format, theirs governs. That
has happened once, for the process report, and it replaced nothing else.

### 3.6 Dates, not clock times

- **Dates are kept.** Date of visit, of purchase, of placing in service. Write them ISO —
  `2026-08-25`.
- **Date of submission is left blank** on every report and on every filled toolkit until a
  person submits it (3.15). It is not written as *Not submitted* and it is not back-dated
  from the visit.
- **Clock times are never written into any document here** — no report, no note, no
  query. Not "posted at 20:29", not "the 15:55 upload".
- **Where a time would place an event, use plain words**: *the late afternoon of 25 August*,
  *earlier that day*, *late on 25 August*.
- **Nothing is lost.** Every photograph keeps its reference (4.2), which resolves through
  the untouched export to the exact entry, its timestamp and its sender.

A timestamp is an artefact of how the evidence reached us, not a fact about the assets. In a
report it reads as a finding and turns a verification record into a message log.

Enforced: `src/build_reports.py` reads every report it has written and fails on a clock
time. This file is the one exemption — a rule must be able to quote what it forbids — and
it is not a generated document, so the check never sees it.

### 3.7 Two formats for every report, and no Markdown in the tree

| Format | Purpose |
|---|---|
| `.docx` | For the supervisor and the local government, who work in Word |
| `.pdf` | For submission, where the layout must not move |

- **The master is Markdown and the master is never a file.** A generator records the
  Markdown in `src/md_render.py` as it writes; the checks in 3.6 and 3.10 to 3.14 read it
  back from there; and only once they pass is it rendered to Word and PDF.
- **Both are rendered from that one text**, so they cannot drift apart, and neither is ever
  edited by hand.
- **This applies to every report** — facility report, LG report, daily log, process report.
- PDF goes through headless Chrome, the route `src/build.py` already uses.

**`RULES.md` is the only Markdown file in this folder.** No report, manifest or note is
written as Markdown anywhere under it. A report that failed a check reaches no format at
all, so a document present in the tree is one that passed.

Enforced: `src/build_reports.py` renders after the checks, fails the build if a PDF is
missing, and deletes any Markdown file it finds in the tree but this one.

### 3.8 Reports name no files and no photographs

A report is read by a supervisor, an LG officer or an auditor. None has this repository open.

- **No file or folder name appears in a report** — no path, no source file. Name the *thing*:
  "the district delivery note", "the individual facility reports".
- **No photograph is called by its stored name or number.** Describe what it shows — "a steel
  cupboard engraved CHEP HCIII UGIFT".
- **No generator, script or tooling is named**, and no report carries a "written by" preamble.

The same applies to queries: a query is written to be actioned by someone standing in the
facility.

### 3.9 Report file naming

```
[district]-[facility-type]-[facility-name].[extension]
```

`[facility-type]` is `school` or `health-centre`; `[facility-name]` is the facility as the
programme list names it. So `Bukwo-health-centre-Mutushet-HC-III.docx`, with the `.pdf`
beside it (3.7).

| Document | Name |
|---|---|
| Local government report | `[district]-local-government-report.[ext]` |
| Daily log | `[district]-team-[n]-daily-log.[ext]` |
| The four standalone LG documents | `[district]-LG-[document].[ext]` |
| Process report | `team-[n]-process-report.[ext]` |

The process report takes the team analogue because it is about no single district. A
district prefix would name one local government it covers and imply the others were owed one
of their own.

### 3.10 How a report is written

A report is the record of a visit, written for someone who was not there. Five qualities,
in this order when they compete:

| Quality | What it means here |
|---|---|
| **Clear** | One idea per sentence. The finding first, the detail after |
| **Complete** | Every section answered, every open item raised. Where nothing was established, the report says *not reported* |
| **Brief** | Two pages at most, one preferred (3.11) |
| **Concise** | No sentence that carries no finding. No throat-clearing, no restatement |
| **Simple** | Short, everyday words. Write *use*, not *utilise*; *start*, not *commence*; *before*, not *prior to*; *about*, not *with regard to* |

Simple does not mean vague. The team's own asset names stand, and so do the official terms
an asset actually carries — *net book value*, *bubble CPAP*, *Chief Administrative Officer*
— because those are the words for the things.

**No process vocabulary.** These describe how a record was handled, not what was found:

| Never | Write instead |
|---|---|
| transcribe, transcription | gone through, checked, written up |
| export, the export | on file, obtained, the record |
| upload, uploaded | recorded, counted, sent in |
| caption, captioned | recorded as, noted as |
| posted, sender, message, entry id | recorded by, the member who recorded it |
| field return, dataset, source file | the record, what was found here |
| auto-generated, parsed, output | written, prepared |

Ordinary English keeps its meaning: a district may *produce* a delivery note. What is banned
is describing **this document** as generated, or the evidence as data.

**No underscores.** `_not signed_` is markup where a value belongs, and Word and PDF pass it
through as the underscores themselves. Write the words: Not signed, not reported, Pending.
Nothing else in a report needs the character. Date of submission is left blank, not written
as Not submitted (3.15).

This does **not** license adding findings:

- **Nothing is asserted that was not established on site.** Reading well is a matter of
  wording, never of adding.
- **The sign-off block names the supervisor; only the verifier signs.** Verifier reads
  *Not signed* until a person signs it. Supervisor is always **Kassim Luminsa** with contact
  **+256 702 806116** (3.15). Date of submission is left blank.

Enforced: the build fails on any banned word, any underscore, and any of the long words the
Simple row replaces.

### 3.11 Length

**Two pages at most. One preferred.**

- **The report carries the finding; the register carries the inventory.** A facility with
  fifty-six items recorded and one engraved is reported as exactly that.
- **In a comparison, show only what differs.** Matching lines are a number, not a table.
- **One line per query**, with the full wording kept in the district record.

Enforced: the build fails if a rendered report runs past two pages.

### 3.12 Every line finishes its sentence

Nothing trails off. A reader of a brief gets one line per open item, and that line is the
whole of what the report says about it.

- **A short line is written short**, not cut short — a sentence in its own right, asserting
  nothing the full wording does not.
- **No line ends in an ellipsis** unless the evidence itself is illegible there.
- **Wording recorded on site is quoted whole** and given the full stop it lacks.
- **The stop belongs against the last word.** `UGIFT .` is what a cut line leaves behind.

Headings and table cells are not sentences. Enforced.

### 3.13 A report does not adjudicate the team's own conduct

Deployment instructions — how many researchers work a facility, whether they travel
together, where they are to meet — are between the team and its supervisor.

- **Which member covered which local government is recorded, and nothing is built on it.**
- **Whether the members were together, met, or were meant to meet is not written** — not as
  a finding, a challenge, a recommendation or a query.
- **The record could not settle it anyway.** It shows who recorded what and when, not where
  anyone was in between, so either claim breaks 3.10.

How a facility was staffed on the day stays: a facility report may say one researcher worked
it and that the discussion guide went unanswered for want of anyone to hold it with. It may
not turn that into a finding about the team. Enforced.

### 3.14 Each team's reports read in that team's own voice

Six teams did six separate pieces of fieldwork. Their reports should read that way, and
today they do not: the recurring sentences are identical across teams, so nine documents
about nine different districts open the same section with the same words. That uniformity
is the tell 3.10 exists to remove — it marks the set as assembled centrally rather than
written by the people who made the visits.

So **each team keeps its own wording for the sentences that recur**: the lead-in to a
section, the line that says nothing was established, the line that says nothing is on file,
the way a query is introduced. Draw on the team's own words from its field report where it
gave any (4.1).

Two limits, and they matter more than the rule:

- **The wording varies; the findings never do.** Two teams meeting the same fact write it
  differently and state the same thing. Varying a phrase to soften, widen or hedge a finding
  is not a voice, it is a different claim, and 3.10 forbids it.
- **No document claims an author.** 3.8 already bars a "written by" preamble, and nothing
  here licenses inventing a hand. A report reads as one team's because that team's words are
  in it, not because it says so.

Mandated wording does not vary. *Not reported*, *Not signed*, *Pending*, *complete*,
*reported, not verified* and the section headings are fixed terms (2.2, 3.1, 3.2, 3.10,
3.15); they mean the same thing everywhere and a reader compares on them.

Enforced: `src/build_reports.py` collects every sentence of forty characters or more from
the reports of each team brought under this rule and fails the build if one of them also
appears in another team's reports. Teams are brought under it one at a time, and 6.3 records
which are done.

### 3.15 Particulars on every report and toolkit

The same names, contacts and dates everywhere. Nothing invents a supervisor or a submission
date.

**Every report** — facility report, local government report, daily log and process report:

| Field | Value |
|---|---|
| Supervisor | Kassim Luminsa |
| Supervisor's contact | +256 702 806116 |
| Date of submission | Blank |

The supervisor and contact appear in **Identification** wherever that section names the
supervisor, and again in **Sign-off** on the local government report. Date of submission is
an empty cell or an empty table row — not *Not submitted*, not a visit date, not today's
date.

**Filled toolkit** — `Asset-Verification-Toolkit.docx` from
`source-documents/ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx`, verification details
table:

| Field on the form | Value |
|---|---|
| Full name (verifier particulars) | The team members who did the work at this facility, comma-separated |
| Contact / email and telephone | Their contact on the record, if any; otherwise blank |
| Supervisor / Sub team leader · Name | Kassim Luminsa |
| Supervisor · Contact | +256 702 806116 |
| Date of submission | Blank |

Region, sub-region and local government still come from the hand-filled copy or its headings
(3.1). The verifier full name is never the supervisor and never a single member where more
than one worked the facility.

**Pending facilities** (2.2). Where state is *Pending*, incomplete, photographs and the four
dimensions — ownership, functionality, usage/performance, location — each read *Pending*.
Nothing else is written for a facility nobody has reached. Where state is *complete* (2.2),
the visit is recorded and the incomplete column carries what could not be done; the four
dimensions read *Not reported* or what the day established, never *Pending*.

## 4. Naming

### 4.1 Precedence for the wording

1. **The hand-filled asset register**, where the name is clear. If it names the asset
   legibly, that name wins.
2. **The programme supply worksheets** in `source-documents/assets-supplied-by-ugift/`,
   where the hand-filled name is not clear — official equipment names as the programme
   procured them.
3. **A delivery note, invoice, facility or LG asset register, or any other applicable
   document** — use its official nomenclature, `Bowl, lotion`, not a colloquial rendering.
4. **The team's own caption**, where they wrote one. Correct only spelling, case and
   punctuation.
5. **A description read off the photograph**, where they wrote none. Read labels, serial
   plates and signage; use external reference where it settles what an item is.

Where two sources disagree the higher governs the name **and the disagreement becomes a
query**. A caption that contradicts its photograph is a finding, not a typo. An unclear
hand-filled name completed from (2) or (3) is a substitution (4.3), not a disagreement.

### 4.2 Filename grammar

```
<NN>_<description>_<ref id>.<ext>
```

- `<NN>` — the order the photograph reached the field report, zero-padded to at least two
  digits, and to more where a folder holds more than ninety-nine.
- `<description>` — lower case, hyphenated. A count is `x4`, never `(4)`.
- `<ref id>` — the reference the export gave the file, complete enough to be unique, so any
  photograph traces back to the entry that carried it and through it to the date and the
  member who sent it. Where a four-digit tail recurs across days, the date is part of the
  reference and is kept.

Nothing is repeated between a folder and the files in it: the folder names the facility and
the facility report records the date of visit. Documents covering more than one facility
live once, at district level, in `_district-documents/`.

### 4.3 Recording a substitution

Any name, description or cost that is not taken from the hand-filled copy is recorded with
its reason and its source in the generator, so the substitution is auditable and survives a
rebuild: `src/build_registers.py` for Team 15, `src/team_registers.py` for Teams 10 to 14,
and the per-team toolkit modules (`src/team10_toolkit.py`, `src/team11_toolkit.py`,
`src/team13_toolkit.py`). **The tree is generated: change the generator, never the files
alone.**

## 5. What is left blank

Anything the sources do not state stays empty. Asset number, department, life in months,
dates of purchase and of placing in service, recoverable cost, and depreciation stay blank
unless the hand-filled copy or the LG asset register gives them.

**Cost is the exception in 3.1a:** where neither of those sources prices the line, a unit
cost from `source-documents/assets-supplied-by-ugift/` is written in. Where that folder
does not price the item either, Cost stays blank. A unit cost is never turned into
recoverable cost, accumulated depreciation, net book value or year-to-date depreciation.

Handwritten annotations on a scan are queries, not facts. A supply-worksheet quantity is
not a found quantity and is not written onto the schedule.

## 6. Current state

Six teams: 10 to 15. Twenty-two local governments with a return, 88 facilities with a
folder, about 5,000 photographs on file.

### 6.1 Asset registers

**A facility is verified when a hand-filled register names it, and every such copy on
file has a Word toolkit in that facility's folder.** Thirty-nine facilities are verified.
The Word file is `Asset-Verification-Toolkit.docx` only — no PDF of the toolkit is
written (3.1). It is filled from
`source-documents/ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx` using the
photographed hand-filled pages, and of nothing else.

- **Team 15** — all 23 facilities. Each booklet names its own facility. The earlier nine
  Bukwo checklist sheets that named the local government only sit under Mutushet HC III
  as photographs; they are superseded by the 31 August booklet that names Mutushet, and
  they are not used to write anyone's toolkit.
- **Team 13** — ten facilities in Busia, Tororo and Tororo Municipal Council, including
  Sikuda Seed Secondary School (discussion guide and all three schedules, furniture
  tagged `SIKUDA UGIFT`).
- **Team 10** — Kalemungole HC III and Katikekire Seed School in Moroto, and Lopei Seed
  Secondary School in Napak. Katikekire's copy carries the guide and one buildings line
  (borehole). Several Moroto cells remain unreadable; those stay blank and are queried.
- **Team 11** — Alerek Seed Secondary School, Sidok Seed Secondary School and Kalimon
  HC III.
- **Teams 12 and 14** — no named hand-filled copy, so no toolkit. Team 12 was asked for
  photographs of the toolkit it filled at Kasasira and never sent them.

**A facility's own asset register is not one of these.** Napak Seed Secondary School
keeps a bound ASSET REGISTER and eleven pages are on file; Kalita Seed School handed over
its own inventory. Both are the facility's record of what it holds — the answer to the
toolkit's first discussion question — and neither is the toolkit the team must fill in on
site. So neither verifies its school. A facility register may complete an Item Description
on a line the hand-filled copy already carries (3.1a); it may not add a line.

The other forty-nine facilities are *reported, not verified*: the team was there and
returned evidence, but no hand-filled register names the facility. A folder follows from a
return of any kind, photographs or not — Team 14's Buyobo HC III was visited, written up
and never photographed, and it keeps a folder with the absence carried as a query.

### 6.2 Where each team stands

Allocated counts are from the team distribution document (2.4); *named* is what the
programme list carries. *Verified* is the count of folders that hold a named hand-filled
copy written up as `Asset-Verification-Toolkit.docx`.

| Team | Allocated | List names | Districts with returns | Facilities worked | Photographs | Verified |
|---|---|---|---|---|---|---|
| 10 | 12 | 11 | Nakapiripirit, Moroto, Napak, Amudat, Nabilatuk | 11 | 470 | **3** |
| 11 | 10 | 10 | Abim, Kotido, Kaabong, Karenga | 10 | 248 | **3** |
| 12 | 16 | 16 | Kibuku, Budaka, Butaleja | 11 | 839 | 0 |
| 13 | 22 | 20 | Busia, Tororo, Tororo Mc | 13 | 1535 | **10** |
| 14 | 20 | 20 | Sironko, Bulambuli, Bududa | 20 | 610 | 0 |
| 15 | 23 | 22 | Bukwo, Kween, Kapchorwa, Kapchorwa Mc | 23 | 1264 | **23** |

Three teams are allocated more facilities than the list names — Team 10 by one, Team 13 by
two, Team 15 by one. Each difference is a query for the district, not an error to correct
(2.4).

Team 11's return covers all four Karamoja local governments on its route. All ten allocated
facilities have a folder; three carry a hand-filled register (Alerek Seed Secondary School,
Sidok Seed Secondary School and Kalimon HC III). Magamaga Seed School, Nakwae Seed School,
Panyangara Seed Secondary School, Rengen Seed School, Kapedo Seed Secondary School and
Lokori Seed Secondary School were reached but found closed, inaccessible, under construction
or not yet commissioned, and each counts as **complete** in coverage (2.2) while the
incomplete column and the queries carry what could not be done.

Team 14's later WhatsApp export filled all three local governments on its route.
Twenty facilities have a folder; one allocated facility, Bukibologoto HC II, remains
**Pending** (mudslides swept the works; the equipment sits in the district stores). None
is verified. Buteza Seed Secondary School, Bushiribo Seed Secondary School and Bumufuni
Seed Secondary School count as **complete** in coverage (2.2) — closed, under construction
and head teacher away. Buyobo HC III still has a folder and no photograph.

Team 15's return covers all four local governments on its route. All twenty-three
allocated facilities have a folder and a named hand-filled booklet written up as a Word
toolkit. The five toolkits once compiled from field-report captions were withdrawn under
3.1; every current Team 15 toolkit is a transcription of the photographed pages.

### 6.3 Documents outstanding

Against section 3, across six teams and twenty-two local governments with a return. The
courtesy call, officer interviews and debrief appear here only as a record of what was
written; **they are not scored and they never enter the progress algorithm** (3, 3.2).

| Required | Status |
|---|---|
| Per-facility toolkit | **39 written.** Every named hand-filled copy on file has `Asset-Verification-Toolkit.docx` (no toolkit PDF) in its folder — Team 15 all 23, Team 13 ten, Team 10 three, Team 11 three. Remaining folders have no named hand-filled copy, so no toolkit is produced (3.1). Team 12 was asked for photographs of the toolkit it filled at Kasasira and never sent them |
| Facility report | **88 of 88** folders. Ownership and usage remain unreported at many of them; each report says so rather than filling it in |
| Photographic evidence | Still missing at a few visited sites, including Team 14's Buyobo HC III |
| `LG-courtesy-call.docx` | Written when the record supports it. **Not scored — never in the algorithm.** On file for Nakapiripirit, Moroto, Napak, Amudat, Nabilatuk, Kotido, Kibuku, Busia, Tororo, Sironko, Bulambuli, Bududa and Kween; others have none |
| `LG-asset-register-review.docx` | **Scored.** Written for every visited local government. Where the district produced a financial document that document is reviewed (Bukwo, Moroto, Kibuku, Busia, Bulambuli, Abim, Kaabong, Karenga, Kotido). Where it produced nothing, the review records that finding |
| `LG-officer-interviews.docx` | Written when the record supports it. **Not scored — never in the algorithm.** Nakapiripirit, Busia, Sironko, Bulambuli and Bududa among those that have one |
| `LG-debrief-note.docx` | Written when the record supports it. **Not scored — never in the algorithm.** None on file |
| `LG-report.docx` | **Scored. 22 of 22** local governments with a return |
| Daily log | **Scored.** All six teams. Team 12 is short the log for one of its three local governments |
| Process report | **Scored. 6 of 6 teams.** |
| Own voice (3.14) | **4 of 6 teams.** Teams 10, 11, 14 and 15. The other two still carry the common wording and are converted one team at a time |

Gaps that remain are gaps in what the teams returned, not in the handling of a named
hand-filled copy. A toolkit cannot be written where no booklet names the facility, and
a missing booklet or Word toolkit marks the team down (3). The asset-register review
is generated for every visited local government, so a missing one is a build gap, not
a field gap. A missing local government report, daily log or process report still
marks the team down. A missing courtesy call, officer interview or debrief does not.

## 7. Google Drive mirror

The working tree under `facility-registers/` is mirrored to **`G:\My Drive\UgIFT`** so the
supervisor and teams see the same documents without opening this repository.

### 7.1 When it runs

**Whenever files or folders under `facility-registers/` change**, the Drive mirror is brought
into line — after a rebuild, after photographs or reports are added or renamed, and after any
other edit that alters what should be shared. Do not wait for a separate sync request when
the tree has already moved.

### 7.2 What is mirrored

Mirror the contents of `facility-registers/` into `G:\My Drive\UgIFT`, preserving the same
relative paths (team → district → facility, `_district-documents/`, `_team-documents/`, and
root files such as the progress report).

### 7.3 What never goes to Drive

These stay in the repository only. They are never created, updated or left behind under
`G:\My Drive\UgIFT`:

| Exclude | Form |
|---|---|
| **This rules file** | `facility-registers/RULES.md` |
| **WhatsApp chat archives** | Each team's `WhatsApp Chat with *.zip` (and any folder unpacked from one) |
| **Field-report transcripts** | Every `field-report-transcript.txt` (and any file named as a field-report transcript) |

If a copy of any of these already exists on Drive from an earlier upload, remove it on the
next sync. The exclusion is permanent, not a one-time skip.

### 7.4 Only changes

**Update what changed; leave the rest alone.** Compare source to Drive and:

- **Add** files and folders that exist here and not on Drive (and are not excluded)
- **Replace** files whose content or size has changed
- **Remove** from Drive only what was deleted here, or what 7.3 forbids
- **Do not** re-copy an unchanged file, and do not wipe and rebuild the Drive tree

A full re-upload is not the default. It is used only if the mirror is known to be corrupt or
the comparison cannot be trusted.

### 7.5 Scope of this section

Section 7 governs the Drive copy only. It does not change what belongs in the repository,
how reports are written, or which facilities are verified. `RULES.md` itself remains the
sole Markdown file under `facility-registers/` (3.7) and is never part of the mirror.
