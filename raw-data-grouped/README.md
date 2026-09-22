# UgIFT verification data, grouped

Every file from `raw-data-ungrouped/` is filed here by **team → local government → facility**.
The content of the files is unchanged, and `raw-data-ungrouped/` was not modified.

```
team-NN/
  <Local government>/
    <Facility>/                    one folder per health centre or school
    _district-documents/           LG-level reports, district registers, CAO correspondence
  _team-documents/                 team-wide registers (DTB sheets), process reports, WhatsApp exports
_multi-team/                       material that spans several teams
  programme-documents/             toolkit, templates, programme lists, supply worksheets
  teams-01-04/  teams-10-15/       consolidated registers and reports for those teams
  busoga-and-part-of-central/      consolidated Busoga / Central asset registers
  bunyoro-tooro-greater-mityana/   DEPAUL consolidated register (Teams 24–30 area)
_index.csv                         every source file and where it went
facility-data-status.pdf           which facilities have sent data and which are missing,
                                   by team, with supervisors and team members
```

## Conventions

- **Teams and local governments** follow `team-distributions.docx`. LG folder names are the
  names used there, such as `Koboko MC`, `Lira City` and `Fort-Portal City`.
- **Facilities** follow the programme list (`SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx`),
  or the teams' own names where the list only gives a sub-county. Names are written as
  `Name-HC-III` or `Name-Seed-Secondary-School`. Teams 10–15 keep the folder names they
  already had.
- **One document covering several facilities** (for example *"Kerwa HC – Kerwa SSS"*) is
  filed in **each** facility's folder.
- **Sub-folders are kept** where the teams made them (for example `PICTURES`,
  `DELIVERY NOTES`).

## How the files were brought across

- **Loose files are hard links**, so they take no extra disk space. Each one is the same
  file as its original in `raw-data-ungrouped/`, which means **editing one changes the
  other**. Copy a file somewhere else before you work on it.
- **Zip archives were opened** and their contents filed individually, byte for byte, with
  the archive's original dates. Nested zips were opened as well.
- **WhatsApp chat exports** (`WhatsApp Chat with ….zip`) and the Kigaragara bid-document
  zip are kept **as whole archives**. Teams 10–15 have already filed that media
  photo by photo.
- **Exact duplicates are stored once per folder.** Examples: `team2530.zip` and
  `team2530_2.zip` are identical, the three copies of the Team 23 set, and
  `Kaberamaido.zip`, which repeats the Team 9 folders. When two different files share a
  name in one folder, the second gets ` (2)`.
- **Not brought across:** Office lock files (`~$…`, 162-byte temporary files), one
  Python script, and the Team 10–15 working folder `ugift-team-10-15/tmp/` (crops, OCR
  output and intermediate photos derived from the originals).

`_index.csv` lists all 12,222 source entries (loose files and every file inside every
zip), with the destination and status of each:

| Status | Meaning |
|---|---|
| placed | filed at the destination shown |
| duplicate | identical content already filed at the destination shown |
| extracted | an archive; its contents are listed individually |
| in-archive | inside a WhatsApp or bid-document zip that was kept whole |
| skipped | lock file or script; see note |

## Coverage

482 facility folders in total. Allocations are from `team-distributions.docx`.

| Team | Local governments allocated | With data on file | Facility folders |
|---|---|---|---|
| 1 | Madi-Okollo, Nwoya, Zombo, Nebbi MC, Nebbi, Pakwach | Madi-Okollo, Nwoya, Zombo, Nebbi, Pakwach | 19 |
| 2 | Yumbe, Arua, Koboko, Koboko MC, Maracha, Terego | Yumbe, Arua, Koboko, Koboko MC, Maracha, Terego | 23 |
| 3 | Obongi, Adjumani, Moyo, Gulu, Amuru | Obongi, Adjumani, Moyo, Gulu, Amuru | 14 |
| 4 | Lamwo, Pader, Agago, Kitgum MC, Kitgum | Lamwo, Pader, Agago, Kitgum | 21 |
| 5 | Lira, Lira City, Kole, Omoro, Oyam | Lira, Lira City, Kole, Omoro, Oyam | 27 |
| 6 | Apac, Apac MC, Kwania, Amolatar | Apac, Apac MC, Kwania, Amolatar | 20 |
| 7 | Alebtong, Otuke, Dokolo | Alebtong, Otuke, Dokolo | 15 |
| 8 | Amuria, Kapelebyong, Katakwi, Soroti, Serere | Amuria, Kapelebyong, Katakwi, Soroti, Serere | 22 |
| 9 | Kaberamaido, Kalaki, Kumi, Butebo, Pallisa, Bukedea, Ngora | Kaberamaido, Kalaki, Kumi, Butebo, Pallisa, Bukedea, Ngora | 16 |
| 10 | Moroto, Moroto MC, Nakapiripirit, Nabilatuk, Napak, Amudat | Moroto, Nakapiripirit, Nabilatuk, Napak, Amudat | 11 |
| 11 | Kotido, Kotido MC, Kaabong, Karenga, Abim | Kotido, Kaabong, Karenga, Abim | 10 |
| 12 | Kibuku, Budaka, Butaleja, Mbale | Kibuku, Budaka, Butaleja, Mbale | 16 |
| 13 | Tororo MC, Tororo, Busia, Busia MC, Manafwa, Namisindwa | Tororo MC, Tororo, Busia, Busia MC, Manafwa, Namisindwa | 21 |
| 14 | Bududa, Sironko, Bulambuli | Bududa, Sironko, Bulambuli | 21 |
| 15 | Kween, Kapchorwa, Kapchorwa MC, Bukwo | Kween, Kapchorwa, Kapchorwa MC, Bukwo | 23 |
| 16 | Namutumba, Luuka, Mayuge, Bugweri | Namutumba, Luuka, Mayuge, Bugweri | 20 |
| 17 | Bugiri, Bugiri MC, Namayingo, Iganga, Iganga MC, Kaliro, Jinja City, Jinja | Bugiri, Bugiri MC, Namayingo, Iganga, Kaliro, Jinja City, Jinja | 18 |
| 18 | Lugazi MC, Mukono MC, Mukono, Buikwe, Njeru MC, Kayunga, Buyende, Kamuli MC, Kamuli | Mukono MC, Buikwe, Kayunga, Buyende, Kamuli | 14 |
| 19 | Bushenyi, Bushenyi-Ishaka MC, Mitooma, Sheema, Sheema MC | Mitooma, Sheema | 0 |
| 20 | Kazo, Kiruhura, Buhweju | Kazo, Kiruhura, Buhweju | 20 |
| 21 | Isingiro, Rwampara, Mbarara, Mbarara City, Rubirizi, Ibanda, Ibanda MC | Isingiro, Rwampara, Mbarara, Mbarara City, Rubirizi, Ibanda | 17 |
| 22 | Kabale, Kabale MC, Kisoro, Kisoro MC, Rubanda, Rukiga | Kabale, Kabale MC, Kisoro, Kisoro MC, Rubanda, Rukiga | 17 |
| 23 | Ntungamo, Ntungamo MC, Rukungiri, Rukungiri MC, Kanungu | Ntungamo, Ntungamo MC, Rukungiri, Rukungiri MC, Kanungu | 23 |
| 24 | Masindi, Masindi MC, Kiryandongo, Luweero, Nakasongola, Nakaseke | Masindi, Masindi MC, Kiryandongo, Luweero | 8 |
| 25 | Buliisa, Hoima, Hoima City, Kikuube, Kagadi | — | 0 |
| 26 | Bundibugyo, Kabarole, Ntoroko | Bundibugyo, Kabarole, Ntoroko | 21 |
| 27 | Kasese, Kasese MC, Bunyangabu, Kamwenge, Kitagwenda | — | 0 |
| 28 | Fort-Portal City, Kyegegwa, Kyenjojo, Mubende, Mubende MC | Fort-Portal City, Kyegegwa, Kyenjojo, Mubende, Mubende MC | 22 |
| 29 | Kiboga, Kakumiro, Kyankwanzi | — | 0 |
| 30 | Kibaale, Kasanda, Mityana MC, Mityana | — | 0 |
| 31 | Buvuma, Kalangala | Buvuma, Kalangala | 9 |
| 32 | Kiira MC, Wakiso, Entebbe MC, Nansana MC, Makindye-Ssabagabo MC, Mpigi, Butambala, Gomba | Butambala, Gomba | 3 |
| 33 | Kalungu, Lwengo, Lyantonde, Bukomansimbi, Sembabule, Masaka City, Masaka, Kyotera, Rakai | Kalungu, Lwengo, Sembabule, Rakai | 11 |

Teams 25, 27, 29 and 30 sent no facility files of their own. Their work appears only in the
consolidated DEPAUL register in `_multi-team/bunyoro-tooro-greater-mityana/`, which has rows
for Buliisa, Hoima City and Kagadi (Team 25); Bunyangabu, Kamwenge, Kasese and Kitagwenda
(Team 27); Kakumiro, Kiboga and Kyankwanzi (Team 29); and Kasanda, Kibaale and Mityana
(Team 30). Team 19 sent only district-level lists for Mitooma and Sheema.

## Judgement calls worth knowing

- **Filed by what the file says, not the folder it arrived in.** `team2530.zip` holds
  Team 26 work (Bundibugyo, Kabarole, Ntoroko). The *"toolkits from central team"* zip
  holds Teams 24, 31, 32 and 33. `Guma teams.zip` holds Teams 19–23.
- **Team 1 file names mix districts.** *"ZOMBO – ATYAK HC III & ALWI SEED"* puts Atyak in
  Zombo and Alwi in Pakwach. *"ZOMBO – GOT APWOYO HC"* and *"… NWOYA PARAA HC"* go to Nwoya.
  Each facility is filed under the district the programme list gives it.
- **Local government from the programme list where the teams differ:** Aduku Seed →
  Kwania; Iceme HC III → Oyam (it arrived in an "OMORO DISTRICT" folder); Onywako HC III →
  Lira; Kimaka HC III → Jinja City; Bugiri Municipal HC III → Bugiri MC; Katasenywa HC III →
  Masindi MC; Lasanga and Nyangilia → Koboko MC; Kitimba HC III → Rukungiri MC.
- **Identified from content, because the file name gives nothing:** the six
  `DOC-2026…-WA00xx.xlsx` sheets in Team 21's "part of team 21" zip (Kyarwabuganda, Kashozi,
  Ruborogota, Munyonyi, St Kizito Magambo, Mushumba); `KABAROLE DISTRICT ASSET VERIFICATION
  … 222.docx` (Nyambuusa HC III); `Team 20.docx` in the Team 23 folder, which is really the
  Kisoro field template (Maregamo, Mwumba, Nyakinama); `NAKAWALA HCIII` (Mubende).
- **File name and content disagree, filed by file name.** The team probably reused a
  template. `1 AMANYIRI HCIII.docx` reads "Ekaligo HC III" inside.
  `LODONGA SEED SS (2).docx` reads "Liko". `ARWOTCEK HC III.docx` reads "Kyankaramata".
  `BUWALA SEED.docx` reads "Bumaya". `MUTUMBA SEED SS.docx` reads "Buhemba". Team 28's
  Kabweza and Kataraza process reports describe Kyankaramata. Check these before relying
  on them.
- **Kalangala** has no team number in the distribution document. It sits with Buvuma under
  "Islands" (Team 31), so it is filed under `team-31`.
