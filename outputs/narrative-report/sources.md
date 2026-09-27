# UgIFT narrative report source log

Final report: `outputs/narrative-report/UgIFT Asset Verification Report.docx`.

## Register scope and counting basis

Historical basis (27 September 2026): this report was calculated from the revision then named `REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx`. The current canonical workbook is listed below. The report figures remain a record of that revision and have not been recertified against the subsequent consolidation.

REF workbook: `outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`; worksheet `Asset Register`, data rows 2 through 225134, columns A:BL (64). All 225133 rows are counted once. The REF values were refreshed for this report; MF and SK retain the source account.
MF workbook: `outputs/asset-register/ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx`; Asset Register rows 2:225134, A:BL. SK workbook: `outputs/asset-register/ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.xlsx`; Asset Register rows 2:225134, A:U (21). Row identities and row counts checked across the three workbooks.

Money uses M FIXED_ASSETS_COST and AK DEPRN_RESERVE. NBV is max(cost less reserve, 0) on each row, then summed; absent cost stays outside the value total. Whole-shilling figures are rounded only after summing the source numeric values. Thus the rounded group amounts may differ by UGX 1 from the rounded programme amount. The zero floor means programme NBV need not equal aggregate cost minus aggregate depreciation.

Condition measures count BK ATTRIBUTE14 exactly Functional or Faulty, reproduced as register classifications. No claim is made that the full denominator was physically assessed. Identification-entry counts exclude buildings, structures and land; within eligible rows, they count nonempty AP TAG_NUMBER not equal to Not engraved, case insensitive. UgIFT marking contains UGIFT or UGFT, case insensitive. IN_USE_FLAG is AU. Facility type is parsed from BL.

Use reason counts require AU=NO. Damage keywords are damaged, broken, faulty, not working and needs repair in SK N Equipment status or O Remarks and REF source-status wording. Storage uses positive stored, in store/box, not yet installed/in use or asset-new wording, excludes negated storage and conflicting damage/replacement/poor-condition wording, and is mutually exclusive with damage. The reviewed row selection is retained in the task analysis files.

Category precedence is fixed structures (C BUILDINGS AND STRUCTURES after removing clearly movable items identified in AX), transport (D TRANSPORT EQUIPMENT), health maternity wording (J or AX), health clinical furniture (including named chairs, tables and related furnishings), other health medical equipment, health ICT, school furniture, school support names, school ICT excluding switches, remaining ICT, remaining furniture, Other assets. Support names are printer, photocopier, camera and projector. Category precedence prevents double counting. Blank minor2 rows are retained under Other recorded items in the class appendix; this is a reporting residual, not a new register class.

National level: the union of Facility type MDA, Hospital or Blood bank and rows held on a national ministry or agency book. This includes 14 Health centre type rows on MOH BK. Other rows follow their local-government region. KCCA rows explicitly have Facility type MDA and are national holdings for this report; no geographic assumption is used for them. Hospitals remain national even when BOOK_TYPE_CODE is a district book.

## Headline values and body repetition

[
  {
    "section": "3 Executive summary",
    "filter": "All REF Asset Register data rows 2:225134, plus facility reconciliation and direct field observations identified in revision_narrative.json.",
    "values": {
      "assets": 225133,
      "functional": 211613,
      "nonfunctional": 13520,
      "assessed": 225133,
      "engraving_eligible": 218715,
      "engraving_ineligible": 6418,
      "engraved": 49836,
      "ugift": 20973,
      "other_marking": 28863,
      "not_engraved": 168879,
      "in_use": 211613,
      "damaged_unused": 2569,
      "stored_unused": 483,
      "cost": 987149478424,
      "depreciation": 177442659553,
      "nbv": 809721344882,
      "capitalized": 194220,
      "cip": 4,
      "facilities": 899
    },
    "coverage": {
      "master_source_rows": 632,
      "master_distinct": 629,
      "master_health_centres": 371,
      "master_schools": 258,
      "accounted_for": 629,
      "facility_specific_material": 548,
      "consolidated_register": 41,
      "explained_or_reconciled_without_separate_return": 40,
      "ground_return_identities": 24,
      "linked_receiving_records": 11,
      "separately_allocated_blood_banks": 3,
      "physical_verified_facility_total": null,
      "definition": "Accountability coverage, not physical-verification coverage. Physical verification total is not supported by supplied reconciliation sources.",
      "locators": [
        "raw-data-grouped/README.md, What the reconciliation shows",
        "raw-data-grouped/facility-data-status.pdf, pages 1 and 5"
      ]
    }
  }
]

## Tables

### Table 1: Local government field itinerary
Client draft, itinerary table 1, rows 2 to 7.

### Table 2: Programme outputs at closure
Client draft, paragraphs 69 to 75, programme outputs at closure.

### Table 3: Facilities on the verification master list
README and facility-reconciliation.csv, Master list scope; 629 distinct records.

### Table 4: Facilities requiring completion or preparation for use
[{"case_id": "F09", "theme": "Incomplete school and equipment awaiting use", "facility": "Got Apwoyo Seed Secondary School", "lg": "Nwoya", "expected": "Got Apwoyo was intended to provide secondary education with completed buildings and installed ICT equipment.", "found": "The team found construction continuing and the school uncommissioned. Its ICT package remained at Nwoya District headquarters, while delivered furniture and structures had not been brought into use.", "gap": "The assets were not yet supporting teaching at the intended school, and custody was divided between the district and the site.", "action": "Nwoya District and the Ministry of Education should set a completion and handover plan, check the stored equipment, and arrange installation, testing and signed transfer when the school is ready."}, {"case_id": "F10", "theme": "Construction damage and displaced service delivery", "facility": "Bukibologoto Health Centre", "lg": "Bulambuli", "expected": "Bukibologoto was listed as complete and was intended to provide care from the constructed health facility.", "found": "The team found that mudslides had damaged the works before completion. A corner was undermined and a wall cracked. Care was being provided at Simu subcounty offices, with equipment held in district stores.", "gap": "The planned facility was unavailable for its intended use, and the temporary service and storage arrangements needed a lasting solution.", "action": "Bulambuli District and the Ministry of Health should obtain an engineering assessment, decide on repair or relocation, inventory the equipment and provide for continuing care."}, {"case_id": "F11", "theme": "Incomplete works and site readiness", "facility": "Kyangwali Seed Secondary School", "lg": "Kikuube", "expected": "Kyangwali school needed completed works, electricity, security and handover to use its assets fully.", "found": "The team recorded continuing construction. The school reported a lack of electricity and an incomplete perimeter fence, and the facility had not been handed over.", "gap": "Finishing the buildings alone would not make the school ready: power, security and responsibility for the assets also remained unresolved.", "action": "Kikuube District, the Ministry of Education and the contractor should close these requirements through one readiness plan, followed by joint testing and handover. The plan should name who will operate, safeguard and maintain the assets."}, {"case_id": "F12", "theme": "Incomplete works and unopened equipment", "facility": "Sidok Seed Secondary School", "lg": "Kaabong", "expected": "Sidok school needed completed buildings and checked equipment before the investment could support full operations.", "found": "The team found blocks, a kitchen and toilets under construction, with termite workings on the plaster of two blocks. The school consignment remained unopened and its contents had not been counted.", "gap": "Both unfinished works and unchecked equipment prevented a complete assessment of readiness for use.", "action": "Kaabong District should secure completion and treatment of the affected works, then arrange a witnessed opening, count and condition check of the equipment. Accepted items should be recorded, assigned to custodians and issued for use."}, {"case_id": "F14", "theme": "Installation and commissioning outstanding", "facility": "Buwagogo Seed Secondary School", "lg": "Manafwa", "expected": "Buwagogo school was intended to use its supplied ICT equipment for teaching.", "found": "The team found the March 2024 ICT consignment still boxed in the store, with contractor installation pending and commissioning delayed.", "gap": "Delivery had not translated into operational ICT capacity. Equipment continued to require secure custody while installation remained outstanding.", "action": "Manafwa District and the Ministry of Education should agree an installation and commissioning date with the contractor, reconcile the stored equipment against delivery records and test it before acceptance. The handover should assign responsibility for operation, maintenance and reporting of faults."}]

### Table 5: Facility reconciliation outcomes
facility-reconciliation.csv and supervisor-decisions.csv, selected final outcomes by distinct master identity.

### Table 6: Expected facilities and the outcomes established during verification
[{"case_id": "F01", "theme": "Listed complete but not constructed", "facility": "Olok Health Centre", "lg": "Pader", "expected": "Olok was listed as a completed health facility intended to serve its catchment in Pader.", "found": "The district health officer confirmed to the verification team that Olok Health Centre had not been constructed and did not exist in the district.", "gap": "The completed entry could not be matched to the intended facility. The reason for non-construction requires a documented resolution.", "action": "Pader District and the Ministry of Health should reconcile the approved project, construction and payment records, correct the beneficiary schedule and decide how the intended health-service need will be met."}, {"case_id": "F02", "theme": "Invalid facility identity", "facility": "Busia Eastern Division health-centre entry", "lg": "Busia Municipal Council", "expected": "The beneficiary schedule should identify the particular health facility supported in Busia Municipality.", "found": "Reconciliation confirmed that no health facility called Busia Eastern Division existed. A separate return identified Sofia Health Centre III within Eastern Division.", "gap": "An administrative division had been used as a facility name. The available confirmation did not identify Sofia as its replacement or establish that the two names referred to the same beneficiary.", "action": "The municipality and Ministry of Health should resolve the original beneficiary identity and document the programme status of Sofia before linking or changing the two entries."}, {"case_id": "F04", "theme": "Beneficiary replacements", "facility": "Ngomoromo, Oweko, Musandama and Loinya health centres", "lg": "Lamwo, Nebbi, Ntoroko and Maracha", "expected": "The beneficiary schedule should name the facility that received each planned investment.", "found": "Supervisors confirmed that Pangira replaced Ngomoromo in Lamwo, Pamaka replaced Oweko in Nebbi, Butungama replaced Musandama in Ntoroko, and Liko replaced Loinya in Maracha. Liko was already listed separately.", "gap": "The programme account needs to link each original entry to its confirmed replacement to prevent duplicate counting and identify the service location.", "action": "The districts and Ministry of Health should attach the replacement decisions, link the original projects to their recipients and retain one active facility identity for each recipient."}, {"case_id": "F05", "theme": "Assets moved to other facilities", "facility": "Alangi, Ther-uru and Abanga", "lg": "Zombo", "expected": "Asset locations and custodians should agree with the facilities holding and using the equipment.", "found": "The supervisor confirmed that Alangi, Ther-uru and Abanga existed, but their UgIFT assets had moved respectively to Amwonyo Health Centre, Atyak Health Centre and Kango Seed Secondary School.", "gap": "The original beneficiary names no longer described where the assets were held. Custody, location and the service arrangements at the original sites needed to be made clear.", "action": "Zombo District should reconcile transfer approvals and signed receipts with both sets of inventories, name the current custodians and confirm how the original catchments are served."}, {"case_id": "F06", "theme": "Facilities outside programme scope", "facility": "Alira Health Centre and Kiziranfumbi Seed Secondary School", "lg": "Oyam and Kikuube", "expected": "The programme beneficiary schedule should include institutions supported under UgIFT.", "found": "The later Oyam clarification confirmed that Alira Health Centre existed but was not among the facilities upgraded under UgIFT. The supervisor also confirmed that Kiziranfumbi Seed Secondary School in Kikuube was outside the programme.", "gap": "The list confused the existence of an institution with its eligibility as a UgIFT beneficiary. Alira had initially been reported absent, but that account was corrected.", "action": "The local governments and sector ministries should approve the scope corrections, remove the institutions from the active UgIFT schedule and preserve the reasons for the changes."}, {"case_id": "F07", "theme": "Existing facilities without UgIFT assets", "facility": "Pandwong Health Centre; Bumbaire, Kyamuhunga and Kashenshero schools; Rwamujojo Health Centre", "lg": "Kitgum Municipal Council, Bushenyi, Mitooma and Sheema Municipal Council", "expected": "Each listed beneficiary should have a supported account of the programme assistance it received.", "found": "Supervisors confirmed that Pandwong Health Centre, Bumbaire and Kyamuhunga schools, Kashenshero school and Rwamujojo Health Centre existed but had not benefited from UgIFT assets.", "gap": "Their appearance on the beneficiary list did not establish delivery. The cause of the difference between the list and the reported benefits needs to be resolved.", "action": "The responsible districts, municipalities and sector ministries should check beneficiary approvals and delivery records, then correct the schedule or record an approved outstanding delivery with an accountable officer and follow-up date."}, {"case_id": "F08", "theme": "Names and aliases", "facility": "Bussi/Zinga and Dabani/Buwumba", "lg": "Wakiso and Busia", "expected": "Each facility should have one stable identity, with local and former names linked to it.", "found": "Bussi was confirmed to be the village name for the already-listed Zinga Health Centre in Wakiso. In Busia, the Buwumba return was reconciled to the master entry named Dabani.", "gap": "Different names could make one facility appear to be two, distort coverage and separate its asset history from the correct institution.", "action": "The districts should adopt the confirmed operating names, retain the old names as aliases and link the beneficiary, project and asset information to one facility identifier. Zinga should be counted once."}]

### Table 7: Examples encountered outside the master-list names
[{"case_id": "F17", "facility": "Rukoki General Hospital", "lg": "Kasese Municipality", "expected": "Confirmed beneficiaries should be included in the programme account.", "found": "The supervisor confirmed that Rukoki General Hospital was a UgIFT beneficiary in Kasese Municipality, although it was absent from the master list used for verification.", "gap": "The programme list omitted a confirmed recipient.", "action": "The Ministry of Health and municipality should approve the beneficiary entry and link its asset information to a stable facility identifier."}, {"case_id": "F17", "facility": "Silumira Health Centre III", "lg": "Kakumiro", "expected": "The beneficiary schedule should include supported health facilities.", "found": "The supervisor confirmed that Silumira Health Centre III had benefited in Kakumiro but was not on the master list.", "gap": "The facility was missing from the list used to plan and account for verification.", "action": "Kakumiro District and the Ministry of Health should approve the addition and connect the beneficiary decision to the facility asset inventory."}, {"case_id": "F16", "facility": "Bukuuku Community Seed Secondary School", "lg": "Fort Portal City", "expected": "Confirmed seed-school beneficiaries should appear in the programme account, with assets handed over for full use.", "found": "Bukuuku was confirmed as an additional beneficiary. The team recorded improved science and computer teaching following laboratory construction, while some asset handover remained pending.", "gap": "The school was omitted from the master list and handover was incomplete.", "action": "The city and Ministry of Education should regularise the beneficiary entry and complete joint handover of the outstanding assets."}]

### Table 8: Asset identification at the listed national ministries and agencies
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; national holdings by vote; buildings, structures and land excluded from marking counts.

### Table 9: Central region: findings and recommended actions
[{"facility": "Busaale Health Centre III", "lg": "Kayunga", "finding": "The facility used Primary Health Care funds for maintenance and kept a quarterly condition record.", "gap": "The maternity roof leaked, door hinges were damaged and the solar battery needed replacement.", "action": "Cost and complete the roof, door and battery repairs, then confirm that the affected rooms and solar system are working.", "source_ids": ["O01", "O02", "O03"], "case_type": "gap"}, {"facility": "Musiitwa Seed Secondary School", "lg": "Kayunga", "finding": "The school checked furniture and fittings each term and repaired them when funds allowed.", "gap": "Broken furniture remained out of use while funding was arranged.", "action": "Prepare a termly repair list and fund repairs in order of their effect on teaching and safety.", "source_ids": ["O04"], "case_type": "gap"}, {"facility": "Musiitwa Seed Secondary School", "lg": "Kayunga", "finding": "The school improved access to secondary education and used irrigation equipment for teaching and food production.", "gap": "Long walking distances and pupils' engagement in petty trade affected attendance.", "action": "Maintain the practical teaching equipment and work with parents and the district education office on attendance barriers.", "source_ids": ["O05", "O06"], "case_type": "gap"}, {"facility": "Lukale Health Centre III", "lg": "Buvuma", "finding": "Staff reported that the maternity ward allowed women to give birth locally and with greater privacy.", "gap": "Benefit to sustain.", "action": "Protect the service through routine care of the maternity building and equipment.", "source_ids": ["O27"], "case_type": "benefit"}, {"id": "AD01", "region": "Central", "facility": "Kijuna Health Centre III", "lg": "Kassanda", "expected": "Patient equipment and basic utilities should be available when care is needed.", "found": "The wheelchairs were not functional, and a failed water pump left the facility with inadequate water. Inadequate power also prevented full use of electronic equipment.", "finding": "Expected: Patient equipment and basic utilities should be available when care is needed. Found: The wheelchairs were not functional, and a failed water pump left the facility with inadequate water. Inadequate power also prevented full use of electronic equipment.", "gap": "The facility faced separate constraints on patient movement, water supply and equipment use.", "action": "Kassanda District should arrange technical assessment and repair of the wheelchairs and pump, restore a dependable power supply and test the affected equipment before returning it to use.", "priority": "High", "source_ids": ["AD01"]}, {"id": "AD02", "region": "Central", "facility": "Kikandwa Health Centre III", "lg": "Kassanda", "expected": "The health facility should provide powered equipment, durable buildings and secure custody of its assets.", "found": "Electronic equipment could not be used because reliable electricity and solar power were unavailable. Storage for damaged assets was inadequate, the facility lacked a perimeter fence, and defects were observed in flooring and skirting.", "finding": "Expected: The health facility should provide powered equipment, durable buildings and secure custody of its assets. Found: Electronic equipment could not be used because reliable electricity and solar power were unavailable. Storage for damaged assets was inadequate, the facility lacked a perimeter fence, and defects were observed in flooring and skirting.", "gap": "Power, secure storage and correction of building defects remained necessary for full and safe use.", "action": "Kassanda District should agree a joint power, security and defects plan, provide secure temporary storage, and have technical staff verify repairs and equipment operation.", "priority": "High", "source_ids": ["AD02"]}, {"id": "AD03", "region": "Central", "facility": "Kyasansuwa Health Centre III", "lg": "Kassanda", "expected": "Computer equipment should support administration and reporting, while floors and bathrooms should remain usable and easy to maintain.", "found": "The facility reported three computers completely damaged following unstable power and surges. Poor floor finishes and defective staff bathroom levels were also observed.", "finding": "Expected: Computer equipment should support administration and reporting, while floors and bathrooms should remain usable and easy to maintain. Found: The facility reported three computers completely damaged following unstable power and surges. Poor floor finishes and defective staff bathroom levels were also observed.", "gap": "Unstable electricity threatened the remaining electronics, while defective finishes and drainage needed correction.", "action": "Kassanda District should stabilise and protect the electrical supply, assess the three computers for repair or replacement, and correct the floor and bathroom defects under technical supervision.", "priority": "High", "source_ids": ["AD03"]}]

### Table 10: Central assets and identification by category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; region=Central; fixed property excluded from marking counts.

### Table 11: Eastern region: findings and recommended actions
[{"facility": "Kagumba Health Centre III", "lg": "Kamuli", "finding": "Staff reported increased maternity and antenatal service use, and the facility kept an asset condition book.", "gap": "Staff housing was under pressure; outpatient, laboratory, storage and kitchen space were identified as needs.", "action": "Assess the supporting space against patient demand and include the agreed works in the district health investment plan.", "source_ids": ["O07", "O08", "O09"], "case_type": "gap"}, {"facility": "Kagumba Seed Secondary School", "lg": "Kamuli", "finding": "The school reported that broken furniture had been repaired during the second term.", "gap": "Practice to sustain.", "action": "Continue condition checks and scheduled furniture repairs before each term.", "source_ids": ["O28"], "case_type": "practice"}, {"facility": "Sikuda Seed Secondary School", "lg": "Busia", "finding": "Broken desks and a cracked laboratory stool were found.", "gap": "The cracked stool was still in use.", "action": "Withdraw unsafe furniture from use and repair or replace it before returning it to classrooms or laboratories.", "source_ids": ["O11"], "case_type": "gap"}, {"facility": "Bubago Health Centre", "lg": "Kamuli", "finding": "Staff identified difficulty operating and maintaining an oxygen concentrator.", "gap": "Equipment use depended on stronger user and basic maintenance skills.", "action": "Arrange practical user training and a technical check, then demonstrate operation with the staff responsible for the equipment.", "source_ids": ["O29"], "case_type": "gap"}, {"facility": "Bumunji, Buwembe and Majanji health centres; Masafu Hospital", "lg": "Busia", "finding": "Equipment had been transferred from the health centres to Masafu Hospital.", "gap": "Allocation and custody require confirmation.", "action": "Confirm the receiving custodian, location and service need, and retain signed transfer and receipt documentation.", "source_ids": ["O10"], "case_type": "custody"}, {"id": "AD06", "region": "Eastern", "facility": "Nansanga Seed Secondary School", "lg": "Budaka", "expected": "The supplied desktop computers should be installed and available for teaching.", "found": "The school lacked reliable power, and twenty-seven of its twenty-eight desktops remained packed.", "finding": "Expected: The supplied desktop computers should be installed and available for teaching. Found: The school lacked reliable power, and twenty-seven of its twenty-eight desktops remained packed.", "gap": "Most of the supplied computer capacity had not reached classroom use because a basic operating requirement was unresolved.", "action": "Budaka District and the school should settle the power connection or suitable alternative, arrange installation and testing, and confirm the number of computers available to learners.", "priority": "High", "source_ids": ["AD06"]}, {"id": "AD07", "region": "Eastern", "facility": "Muhula Seed Secondary School", "lg": "Butaleja", "expected": "The school should receive completed buildings and tested equipment before formal handover and operation.", "found": "The contractor had not handed over the school, and it was not operating. Buildings showed cracks, an air conditioner remained boxed with a missing fan, and the installed water pump was not working.", "finding": "Expected: The school should receive completed buildings and tested equipment before formal handover and operation. Found: The contractor had not handed over the school, and it was not operating. Buildings showed cracks, an air conditioner remained boxed with a missing fan, and the installed water pump was not working.", "gap": "Construction completion, equipment completeness and successful testing had not come together to make the school ready.", "action": "Butaleja District and the Ministry of Education and Sports should agree a defects and handover schedule with the contractor, rectify the works, complete the equipment and witness operational tests before handover.", "priority": "High", "source_ids": ["AD07"]}, {"id": "AD08", "region": "Eastern", "facility": "Sop Sop Health Centre III", "lg": "Tororo", "expected": "Delivered equipment should be accompanied by the skills and accessories needed to use it.", "found": "The facility reported that much of its equipment remained in store because staff did not know how to operate it. Oxygen equipment had arrived without cylinders. Tuberculosis testing and maternity services had nevertheless improved.", "finding": "Expected: Delivered equipment should be accompanied by the skills and accessories needed to use it. Found: The facility reported that much of its equipment remained in store because staff did not know how to operate it. Oxygen equipment had arrived without cylinders. Tuberculosis testing and maternity services had nevertheless improved.", "gap": "Equipment delivery had not been matched consistently with user training and a complete operating package.", "action": "Tororo District and the Ministry of Health should arrange practical training at the facility, confirm the required oxygen components, and check that trained staff can safely use each released item.", "priority": "High", "source_ids": ["AD08"]}, {"id": "AD09", "region": "Eastern", "facility": "Bunamono Health Centre III", "lg": "Bududa", "expected": "The installed water system should supply the staff houses, and supplied clinical equipment should be ready for use.", "found": "The water tank was not working and the solar pump was not connected, leaving the staff houses without water. A supplied laboratory stand remained boxed because staff could not assemble it, and a glucometer lacked test strips.", "finding": "Expected: The installed water system should supply the staff houses, and supplied clinical equipment should be ready for use. Found: The water tank was not working and the solar pump was not connected, leaving the staff houses without water. A supplied laboratory stand remained boxed because staff could not assemble it, and a glucometer lacked test strips.", "gap": "The facility needed installation, demonstration and consumables to turn delivered assets into usable services.", "action": "Bududa District should complete and test the water connection, arrange assembly and user demonstration for the laboratory stand, and establish a supply of compatible glucometer strips.", "priority": "High", "source_ids": ["AD09"]}]

### Table 12: Eastern assets and identification by category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; region=Eastern; fixed property excluded from marking counts.

### Table 13: Northern region: findings and recommended actions
[{"facility": "Got Apwoyo Seed Secondary School", "lg": "Nwoya", "finding": "The school was under construction and had not been commissioned. Delivered furniture was on site and computer equipment was held at district headquarters.", "gap": "Incomplete buildings prevented commissioning and installation.", "action": "Agree a costed completion and handover plan, then move and install the equipment when the rooms and utilities are ready.", "source_ids": ["O30"], "case_type": "gap"}, {"facility": "Ndhew Seed School", "lg": "Nebbi", "finding": "Buildings were incomplete, with computer and science equipment held at district headquarters and furniture not yet installed.", "gap": "Delivery of equipment had not translated into an equipped school.", "action": "Complete the outstanding works and sanitation facilities and coordinate furniture and equipment installation with handover.", "source_ids": ["O31"], "case_type": "gap"}, {"facility": "Mamba Seed School", "lg": "Nebbi", "finding": "Construction was incomplete. Computers were temporarily accommodated in older structures, while science equipment remained at district headquarters.", "gap": "The planned laboratory and computer spaces were not ready for full installation.", "action": "Complete and commission the buildings, install the equipment and confirm safe operation before formal handover.", "source_ids": ["O32"], "case_type": "gap"}, {"facility": "Atego Seed School", "lg": "Nebbi", "finding": "Computers were connected and working in older rooms while construction continued.", "gap": "Staff reported power surges and the planned facilities were not fully commissioned.", "action": "Stabilise the power supply, protect the installed computers and finish the remaining works.", "source_ids": ["O33"], "case_type": "gap"}, {"facility": "Lungulu Seed Secondary School", "lg": "Nwoya", "finding": "The school funded minor repairs and kept breakdown information, but computers remained in storage pending power.", "gap": "The stored equipment included defective desktop units, and the assets were not engraved.", "action": "Provide a suitable power connection, repair defective units, install the usable equipment and apply asset identification markings.", "source_ids": ["O12", "O13", "O34"], "case_type": "gap"}, {"facility": "Todora and Paraa Health Centres III", "lg": "Nwoya", "finding": "Todora used the regional technical maintenance team, while some equipment originally intended for Todora remained at Paraa after redirection during construction.", "gap": "Equipment location and final allocation required a district decision.", "action": "Confirm the service need at both facilities, formally allocate or transfer the equipment and update the named custodians.", "source_ids": ["O14", "O15"], "case_type": "gap"}, {"facility": "Pamaka Health Centre III", "lg": "Nebbi", "finding": "Staff reported increased attendance and community confidence.", "gap": "The solar system was not working, oxygen equipment could not be used because of power constraints, and staffing was under pressure.", "action": "Restore reliable power and demonstrate oxygen equipment operation; review staffing against patient demand.", "source_ids": ["O16", "O17"], "case_type": "gap"}, {"facility": "Kalemungole Health Centre III", "lg": "Moroto", "finding": "Neonatal respiratory equipment remained in an unopened carton and treatment trolleys were still wrapped.", "gap": "Delivered items had not been brought into routine use.", "action": "Check the equipment, confirm the room and staff requirements, and arrange installation and user orientation.", "source_ids": ["O18"], "case_type": "gap"}, {"facility": "Rupa Seed School", "lg": "Moroto", "finding": "The school hired a generator for practical lessons and used its library and computer laboratory block as dormitories.", "gap": "The intended learning spaces and a permanent power connection were unavailable for their planned use.", "action": "Agree a room-use plan and power solution that restores the library and computer laboratory functions.", "source_ids": ["O19"], "case_type": "gap"}, {"id": "AD04", "region": "Northern", "facility": "Alwi Seed Secondary School", "lg": "Pakwach", "expected": "The computer laboratory and security equipment should support teaching and school operation.", "found": "The school reported power surges. Nine monitors and ten system units were not working, as were the server power-backup unit and twenty other power-backup units. Only one of thirteen security cameras was functional.", "finding": "Expected: The computer laboratory and security equipment should support teaching and school operation. Found: The school reported power surges. Nine monitors and ten system units were not working, as were the server power-backup unit and twenty other power-backup units. Only one of thirteen security cameras was functional.", "gap": "The loss of working computer stations and power protection reduced the usable laboratory capacity and left much of the camera system unavailable.", "action": "Pakwach District and the school should first assess the electrical supply and protection, then repair or replace failed equipment and test the whole laboratory and camera system before acceptance.", "priority": "High", "source_ids": ["AD04"]}, {"id": "AD05", "region": "Northern", "facility": "Wadelai Seed Secondary School", "lg": "Pakwach", "expected": "The school should be able to use its computer laboratory reliably and keep water storage structures safe.", "found": "Twenty desktop computers were recorded as working and in use, but the school reported a solar fault that interrupted use of electrical equipment. One water-tank stand was broken and presented a threat to students.", "finding": "Expected: The school should be able to use its computer laboratory reliably and keep water storage structures safe. Found: Twenty desktop computers were recorded as working and in use, but the school reported a solar fault that interrupted use of electrical equipment. One water-tank stand was broken and presented a threat to students.", "gap": "Usable equipment remained dependent on an unreliable power supply, and the damaged tank support required immediate attention.", "action": "The school and Pakwach District should restrict access around the damaged tank support pending an engineering assessment, repair the support, and restore and test the solar system.", "priority": "High", "source_ids": ["AD05"]}]

### Table 14: Northern assets and identification by category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; region=Northern; fixed property excluded from marking counts.

### Table 15: Western region: findings and recommended actions
[{"facility": "Nyamarunda Health Centre III", "lg": "Kibaale", "finding": "The facility identified and set aside broken items and referred them to the District Health Officer.", "gap": "Staff raised concerns about staff-quarter workmanship, electrical installation, drainage, water security and storage.", "action": "Carry out a joint engineering and health inspection, make unsafe installations safe and complete the agreed repairs.", "source_ids": ["O20", "O21"], "case_type": "gap"}, {"facility": "Avogera Health Centre III", "lg": "Buliisa", "finding": "The facility carried out local repairs and received technical support from Hoima Regional Referral Hospital.", "gap": "Items that could not be repaired remained stored; staff identified technical skills, user orientation and storage needs.", "action": "Assess the stored items for repair, give practical user training and agree a suitable storage arrangement.", "source_ids": ["O22"], "case_type": "gap"}, {"facility": "Ngwedo Seed Secondary School", "lg": "Buliisa", "finding": "A caretaker attended monthly for repairs, and the Directorate of Industrial Training repaired furniture.", "gap": "Practice to sustain.", "action": "Continue the repair schedule and record the items returned to use.", "source_ids": ["O23"], "case_type": "practice"}, {"facility": "Bundimulangya Health Centre III", "lg": "Bundibugyo", "finding": "The District Health Officer arranged maintenance support, and staff said the power house and solar installation supported continued operation.", "gap": "Practice to sustain.", "action": "Keep the technical referral arrangement active and include the power and solar systems in routine servicing.", "source_ids": ["O24"], "case_type": "practice"}, {"facility": "Kyankaramata Health Centre III", "lg": "Kyenjojo", "finding": "Primary Health Care funds paid for minor repairs.", "gap": "Major repair costs were a constraint.", "action": "Prepare costed technical referrals for major repairs and agree district funding and follow-up.", "source_ids": ["O25"], "case_type": "gap"}, {"facility": "Kigorobya Seed Secondary School", "lg": "Hoima", "finding": "Equipped classrooms, the computer room and chemistry laboratory supported teaching; the school and ministry shared maintenance work.", "gap": "Staffing and study materials constrained use of the improved facilities.", "action": "Review teaching staff and materials alongside the maintenance plan.", "source_ids": ["O26"], "case_type": "gap"}, {"facility": "Butungama Seed School", "lg": "Ntoroko", "finding": "The school was still under construction at the time of the interview.", "gap": "The construction works required completion.", "action": "Confirm the outstanding works with the district engineer and agree the completion and handover sequence.", "source_ids": ["O35"], "case_type": "gap"}, {"facility": "Butiaba Health Centre III", "lg": "Buliisa", "finding": "The hydraulic delivery bed was not in use because staff needed operating guidance. Staff also reported difficulty obtaining test strips for the supplied glucometers.", "gap": "Equipment use depended on practical training and access to compatible consumables.", "action": "Demonstrate safe operation of the delivery bed with its users and arrange a reliable supply of compatible glucometer strips.", "source_ids": ["O36"], "case_type": "gap"}, {"id": "AD10", "region": "Western", "facility": "Kihungya Seed Secondary School", "lg": "Buliisa", "expected": "The school investment should provide usable science and computer laboratories, staff accommodation, water and secure premises.", "found": "The science block, computer laboratory and library were still under construction, and staff quarters were incomplete. The school reported no electricity for computer sessions, no water for sanitation and no perimeter fence. Its administration block was already in use.", "finding": "Expected: The school investment should provide usable science and computer laboratories, staff accommodation, water and secure premises. Found: The science block, computer laboratory and library were still under construction, and staff quarters were incomplete. The school reported no electricity for computer sessions, no water for sanitation and no perimeter fence. Its administration block was already in use.", "gap": "The school was partly in use while essential teaching spaces, utilities and security remained unfinished.", "action": "Buliisa District and the Ministry of Education and Sports should use one completion plan for the laboratories, staff housing, electricity, water and security, with separate testing and handover of each finished element.", "priority": "High", "source_ids": ["AD10"]}, {"id": "AD11", "region": "Western", "facility": "Kihungya Health Centre III", "lg": "Buliisa", "expected": "Expanded buildings and equipment should support care at the health centre, with responsibility clear for any items kept elsewhere.", "found": "Staff reported more room for patients, easier working arrangements through staff accommodation, and electricity from the new solar power house. Buildings were in use. A gas stove, electric suction apparatus, laboratory stool and electric centrifuge were recorded at the subcounty rather than the health centre.", "finding": "Expected: Expanded buildings and equipment should support care at the health centre, with responsibility clear for any items kept elsewhere. Found: Staff reported more room for patients, easier working arrangements through staff accommodation, and electricity from the new solar power house. Buildings were in use. A gas stove, electric suction apparatus, laboratory stool and electric centrifuge were recorded at the subcounty rather than the health centre.", "gap": "The building and power investment was supporting care, but the intended use and custody of equipment held away from the facility needed confirmation.", "action": "Buliisa District and facility management should preserve the working building and solar arrangements, confirm who holds the off-site equipment, and agree whether it should be deployed to the health centre or remain at its present location.", "priority": "Medium", "source_ids": ["AD11"]}]

### Table 16: Western assets and identification by category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; region=Western; fixed property excluded from marking counts.

### Table 17: Priority actions to protect assets and restore service
[{"priority": "1. Immediate safety and essential service", "action": "Withdraw damaged furniture that presents a safety concern, inspect the electrical concerns at Nyamarunda, and assess the failed solar and oxygen equipment arrangements at Pamaka.", "owner": "Facility managers, district health and education officers, district engineers and regional medical equipment technical teams", "timing": "Proposed: inspect within 30 days of report approval; complete minor corrective work within 60 days.", "completion_evidence": "Unsafe items withdrawn; signed technical assessment; repair record and demonstration of safe operation.", "source_ids": ["O11", "O16", "O21"]}, {"priority": "2. Complete and commission facilities", "action": "Agree completion plans for Got Apwoyo, Ndhew, Mamba and Butungama seed schools. Coordinate the remaining works, utilities, furniture and equipment installation; protect ongoing equipment use at Atego.", "owner": "District Accounting Officers, district engineers, district education officers, contractors and Ministry of Education and Sports", "timing": "Proposed: agree site-specific completion plans within 30 days; track progress monthly against the approved dates.", "completion_evidence": "Outstanding-works schedule; approved completion dates; inspection and handover documents; classrooms or laboratories opened for their intended use.", "source_ids": ["O30", "O31", "O32", "O33", "O35"]}, {"priority": "3. Bring stored equipment into use", "action": "Provide the power required at Lungulu, assess and install the boxed equipment at Kalemungole, and assess the repair needs of stored items at Avogera. Keep damaged and usable stored items on separate action lists.", "owner": "District health and education officers, facility managers, electrical contractors and regional technical teams", "timing": "Proposed: confirm readiness and actions within 30 days; complete installation within 90 days where rooms and utilities are ready.", "completion_evidence": "Equipment location check; power and installation sign-off; named custodian; practical demonstration and date first used.", "source_ids": ["O13", "O18", "O22", "O34"]}, {"priority": "4. Clear priority repairs", "action": "Repair the roof, doors and solar system at Busaale, arrange the major repair support needed at Kyankaramata and assess damaged laptops at the Office of the Prime Minister.", "owner": "Facility managers, district health officers, district engineers and the responsible national institution asset managers", "timing": "Proposed: agree priority work within 30 days and complete funded repairs within 90 days.", "completion_evidence": "Approved repair list; work orders; repairs checked and assets returned to use or assigned a formal disposal decision.", "source_ids": ["O03", "O25", "N02"]}, {"priority": "5. Strengthen user skills", "action": "Provide practical operation and basic maintenance training for oxygen equipment users at Bubago and the staff requiring equipment orientation at Avogera.", "owner": "District health officers, facility in-charges, suppliers and regional medical equipment technical teams", "timing": "Proposed: complete initial training within 60 days and review use after a further 30 days.", "completion_evidence": "Training attendance by role; practical demonstration of equipment use; named technical support contact.", "source_ids": ["O22", "O29"]}, {"priority": "6. Mark assets and confirm custody", "action": "Mark eligible unengraved assets, starting with the identified Lungulu holdings, and confirm the final allocation of transferred equipment at Todora, Paraa and Masafu.", "owner": "Institution asset managers, facility managers and district finance, health and education offices", "timing": "Proposed: confirm allocation within 30 days and complete priority marking and custody checks within 90 days.", "completion_evidence": "Readable identification; item-to-custodian match; signed transfer or receipt and agreed final location.", "source_ids": ["O10", "O15", "O34", "Q01"]}, {"priority": "7. Fund routine maintenance", "action": "Retain the functioning local and regional repair arrangements and prepare annual maintenance plans that separate minor repairs from specialist work. Review unresolved faults each quarter.", "owner": "Facility managers, school governing bodies, district health and education officers and national institution Accounting Officers", "timing": "Proposed: prepare plans within 90 days, include costs in the next budget cycle and review quarterly.", "completion_evidence": "Funded maintenance plan; fault list with responsible roles and due dates; service history and closed repair actions.", "source_ids": ["O01", "O02", "O04", "O07", "O12", "O14", "O20", "O23", "O24", "O25", "O28", "N01"]}, {"priority": "8. Match service capacity to demand", "action": "Review supporting clinical space and staffing at Kagumba and Pamaka, teaching staff and materials at Kigorobya, and attendance barriers at Musiitwa. Include operating needs in future asset planning.", "owner": "District health and education officers, facility managers and the relevant sector ministries", "timing": "Proposed: complete service-needs reviews within 90 days and include agreed measures in the next planning and budget cycle.", "completion_evidence": "Agreed staffing and space priorities; service or teaching plan; funded actions and periodic review of use.", "source_ids": ["O05", "O08", "O09", "O17", "O26", "O27"]}]

### Table 18: Whole programme and regional summary counts
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; count filters and reviewed transfer evidence in sources.md; reconciliation tables by scope and final outcome.

### Table 19: Asset rows by report category and region
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; mutually exclusive report category mapping in section 5.6.

### Table 20: Asset rows by register class and region
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; ASSET_CATEGORY_MINOR2 grouped by region. Other recorded items retain rows outside the listed classes.

### Table 21: Condition classifications by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; ATTRIBUTE14(Equipment status), grouped by category.

### Table 22: Condition classifications by sub-region
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; ATTRIBUTE14(Equipment status), grouped by subregion.

### Table 23: Recorded value and net book value by region
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; FIXED_ASSETS_COST, DEPRN_RESERVE and row-level max(cost less reserve, 0).

### Table 24: National ministry and agency value schedule
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; all rows on national ministry and agency books, plus Hospital holdings; blood banks are included on the UBTS vote.

### Table 25: Use flags and recorded reasons by report category
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; IN_USE_FLAG, SK Equipment status and Remarks; negative and conflicting wording excluded from the stored group.

### Table 26: Identification entries by region
REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE_REVISED.xlsx, Asset Register, rows 2 to 225,134; TAG_NUMBER on movable assets; buildings, structures and land excluded.

### Table 27: Master-list entries accounted for through reconciliation
facility-reconciliation.csv, selected master IDs; supervisor-decisions.csv, decision references shown; exact CSV record numbers in sources.md.

### Table 28: Ground-return identities outside master-list names
facility-reconciliation.csv, scope Ground return only, X identities. Names are retained as reconciliation identities.

### Table 29: Asset information prepared for handover
The three accompanying workbook Asset Register and Read Me worksheets; data rows 2 to 225,134.

## Charts and photographs

### Figure 1: All 629 master-list entries were accounted for
Output file: `outputs/narrative-report/figures/chart_01_coverage.png`.
facility-reconciliation.csv, Master list scope; master_by_region_type counts; README accountability coverage definition.

### Figure 2: Unfinished school block at Got Apwoyo Seed Secondary School, Nwoya District (Acholi)
Output file: `outputs/narrative-report/figures/photo_11_got_apwoyo_construction.jpg`.
UgIFT field photograph P11; raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx; {"embedded_image": "word/media/image1.jpeg", "body_block": 31, "table": null, "adjacent_text": "Nwoya district report body block 7 identifies Got Apwoyo Seed Secondary School. Blocks 10 to 14 describe ongoing construction, no commissioning, and ICT held at the district. Field photographs begin at block 30; image1.jpeg occurs at block 31."}

### Figure 3: Building works at a seed secondary school, Kiboga District (Buganda)
Output file: `outputs/narrative-report/figures/photo_12_lwamata_construction.jpg`.
UgIFT field photograph P12; raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx; {"embedded_image": "word/media/image6.jpeg", "body_block": 79, "table": null, "adjacent_text": "Lwamata school return body block 11 identifies the school, block 33 states that some buildings remain under construction and laboratory equipment was expected after structures were completed. Image6.jpeg is at block 79 after PICTURES OF ASSETS VISITED AND VERIFIED."}

### Figure 4: School block awaiting completion at Butungama Seed Secondary School, Ntoroko District (Tooro)
Output file: `outputs/narrative-report/figures/photo_13_butungama_construction.jpg`.
UgIFT field photograph P13; raw-data-grouped/team-26/_team-documents/Butungama Seed School.pdf; {"embedded_image": "PDF page 7, image 1", "body_block": null, "table": null, "adjacent_text": "Photographic PDF page 7; the school sign appears on page 3. The paired return raw-data-grouped/team-26/Ntoroko/Butungama-Seed-Secondary-School/ASSET VERIFICATION AND RECORDING TOOL KIT 222 BUTUNGAMA HEALTH CENTRE III AND BUTUNGAMA SEED SCHOOL (1).docx, body blocks 113, 119 and 178 identify the school and ongoing construction.", "page": 7}

### Figure 5: School buildings and courtyard at a seed secondary school, Buvuma District (Buganda)
Output file: `outputs/narrative-report/figures/photo_33_buvuma_school_blocks.jpg`.
UgIFT field photograph P33; raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Image 2026-09-12 at 13.47.23 (3).jpeg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph WhatsApp Image 2026-09-12 at 13.47.23 (3).jpeg under Bweema-Seed-Secondary-School/Buvuma. The same source photo collection includes a school sign identifying Bweema and Buvuma."}

### Figure 6: Raised water storage tank at a seed secondary school, Buvuma District (Buganda)
Output file: `outputs/narrative-report/figures/photo_34_buvuma_raised_water_tank.jpg`.
UgIFT field photograph P34; raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Image 2026-09-12 at 13.47.25.jpeg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph WhatsApp Image 2026-09-12 at 13.47.25.jpeg under Bweema-Seed-Secondary-School/Buvuma."}

### Figure 7: Boxed pulse oximeters at a health centre, Makindye-Ssabagabo Municipal Council (Buganda)
Output file: `outputs/narrative-report/figures/photo_21_kibiri_boxed_oximeters.jpg`.
UgIFT field photograph P21; raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx; {"embedded_image": "word/media/image17.jpeg", "body_block": 77, "table": null, "adjacent_text": "Kibiri Health Centre III report image17.jpeg, body block 77. Blocks 1 and 5 identify Kibiri; the packaging explicitly identifies Handheld Pulse Oximeter."}

### Figure 8: Programme and school engraving on a chair at Budde Seed Secondary School, Butambala District (Buganda)
Output file: `outputs/narrative-report/figures/photo_71_budde_seed_secondary_school_programme_and_school_engraving_on_a_chair.jpg`.
UgIFT field photograph P71; raw-data-grouped/team-32/Butambala/Budde-Seed-Secondary-School/BUDDE SEED SCHOOL (BUTAMABALA DISTRICT-BUDDE SEED).docx; {"embedded_image": "word/media/image43.png", "body_block": 102, "table": 8, "adjacent_text": "Budde Seed Secondary School return: PICTORIAL EVIDENCE, body block 102, table 8, word/media/image43.png. The visible mark identifies UGIFT and the school."}

### Figure 9: Desks and chairs bearing asset identification at Budde Seed Secondary School, Butambala District (Buganda)
Output file: `tmp/narrative-report/photos/extended/photo_087.jpg`.
UgIFT field photograph P87; raw-data-grouped/team-32/Butambala/Budde-Seed-Secondary-School/BUDDE SEED SCHOOL (BUTAMABALA DISTRICT-BUDDE SEED).docx; {"embedded_image": "word/media/image42.png", "body_block": 102, "table": 8}

### Figure 10: Laboratory benches and sinks at Bweema Seed Secondary School, Buvuma District (Buganda)
Output file: `outputs/narrative-report/figures/photo_67_bweema_seed_secondary_school_laboratory_benches_and_sinks.jpg`.
UgIFT field photograph P67; raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Image 2026-09-12 at 13.47.22 (2).jpeg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.22 (2).jpeg."}

### Figure 11: Classroom desks at Bweema Seed Secondary School, Buvuma District (Buganda)
Output file: `outputs/narrative-report/figures/photo_68_bweema_seed_secondary_school_classroom_desks.jpg`.
UgIFT field photograph P68; raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Unknown 2026-09-12 at 13.58.16/WhatsApp Image 2026-09-12 at 13.47.17 (2).jpeg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.17 (2).jpeg."}

### Figure 12: Sanitation block at Bweema Seed Secondary School, Buvuma District (Buganda)
Output file: `outputs/narrative-report/figures/photo_69_bweema_seed_secondary_school_sanitation_block.jpg`.
UgIFT field photograph P69; raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Unknown 2026-09-12 at 13.58.16/WhatsApp Image 2026-09-12 at 13.47.20 (1).jpeg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.20 (1).jpeg."}

### Figure 13: Water tank and enclosed service structures at Bweema Seed Secondary School, Buvuma District (Buganda)
Output file: `tmp/narrative-report/photos/extended/photo_099.jpg`.
UgIFT field photograph P99; raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Unknown 2026-09-12 at 13.58.16/WhatsApp Image 2026-09-12 at 13.47.13 (1).jpeg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 14: Science laboratory tables and stools at a seed secondary school, Kalangala District (Buganda)
Output file: `outputs/narrative-report/figures/photo_01_central_laboratory_furniture.jpg`.
UgIFT field photograph P01; raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx; {"embedded_image": "word/media/image9.jpeg", "body_block": 35, "table": null, "adjacent_text": "5. Science laboratory tables and stools | 5. Science laboratory tables and stools"}

### Figure 15: School blocks at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda)
Output file: `tmp/narrative-report/photos/positive/p95_positive.jpg`.
UgIFT field photograph P95; raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx; {"embedded_image": "word/media/image27.jpeg", "body_block": 95, "table": null, "adjacent_text": "12. A | d | ministration block, staffrooms | , classrooms |  and multipurpose hall | 12. A | d | ministration block, staffrooms | , classrooms |  and multipurpose hall"}

### Figure 16: Library shelves and reading tables at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda)
Output file: `tmp/narrative-report/photos/extended/photo_096.jpg`.
UgIFT field photograph P96; raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx; {"embedded_image": "word/media/image15.jpeg", "body_block": 63, "table": null}

### Figure 17: Anatomical teaching model at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda)
Output file: `tmp/narrative-report/photos/extended/photo_097.jpg`.
UgIFT field photograph P97; raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx; {"embedded_image": "word/media/image17.jpeg", "body_block": 71, "table": null}

### Figure 18: Laboratory glassware and equipment at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda)
Output file: `tmp/narrative-report/photos/extended/photo_098.jpg`.
UgIFT field photograph P98; raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx; {"embedded_image": "word/media/image18.jpeg", "body_block": 71, "table": null}

### Figure 19: Oxygen cylinders at Kibiri HC III, Makindye-Ssabagabo Municipality (Buganda)
Output file: `outputs/narrative-report/figures/photo_70_kibiri_hc_iii_oxygen_cylinders.jpg`.
UgIFT field photograph P70; raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx; {"embedded_image": "word/media/image27.jpeg", "body_block": 77, "table": null, "adjacent_text": "Kibiri HC III report: oxygen-cylinder photograph word/media/image27.jpeg in body block 77, within the facility pictorial record."}

### Figure 20: Wooden waiting bench at Kibiri HC III, Makindye-Ssabagabo Municipal Council (Buganda)
Output file: `tmp/narrative-report/photos/extended/photo_088.jpg`.
UgIFT field photograph P88; raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx; {"embedded_image": "word/media/image1.jpeg", "body_block": 77, "table": null}

### Figure 21: Sanitation block with external handwashing basins at Kibiri HC III, Makindye-Ssabagabo Municipal Council (Buganda)
Output file: `tmp/narrative-report/photos/extended/photo_090.jpg`.
UgIFT field photograph P90; raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx; {"embedded_image": "word/media/image10.jpeg", "body_block": 77, "table": null}

### Figure 22: Waste disposal structure at Kibiri HC III, Makindye-Ssabagabo Municipal Council (Buganda)
Output file: `tmp/narrative-report/photos/extended/photo_091.jpg`.
UgIFT field photograph P91; raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx; {"embedded_image": "word/media/image12.jpeg", "body_block": 77, "table": null}

### Figure 23: Infant radiant warmer at a health centre, Makindye-Ssabagabo Municipal Council (Buganda)
Output file: `outputs/narrative-report/figures/photo_02_central_infant_warmer.jpg`.
UgIFT field photograph P02; raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx; {"embedded_image": "word/media/image22.jpeg", "body_block": 77, "table": null, "adjacent_text": ""}

### Figure 24: Office desk and other furniture at Lwamata Town Council Seed Secondary School, Kiboga District (Buganda)
Output file: `tmp/narrative-report/photos/extended/photo_092.jpg`.
UgIFT field photograph P92; raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx; {"embedded_image": "word/media/image2.jpeg", "body_block": 78, "table": null}

### Figure 25: Laboratory tables at Lwamata Town Council Seed Secondary School, Kiboga District (Buganda)
Output file: `tmp/narrative-report/photos/extended/photo_093.jpg`.
UgIFT field photograph P93; raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx; {"embedded_image": "word/media/image4.jpeg", "body_block": 78, "table": null}

### Figure 26: Library shelving at Lwamata Town Council Seed Secondary School, Kiboga District (Buganda)
Output file: `tmp/narrative-report/photos/extended/photo_094.jpg`.
UgIFT field photograph P94; raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx; {"embedded_image": "word/media/image5.jpeg", "body_block": 78, "table": null}

### Figure 27: ICT laboratory interior under construction at Kitawoi Seed Secondary School, Kween District (Sebei)
Output file: `outputs/narrative-report/figures/photo_84_kitawoi_seed_secondary_school_ict_laboratory_interior_under_construction.jpg`.
UgIFT field photograph P84; raw-data-grouped/team-15/Kween/Kitawoi-Seed-Secondary-School/09_ict-lab-under-construction_ref1386.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kween / Kitawoi-Seed-Secondary-School; original filename: 09_ict-lab-under-construction_ref1386.jpg."}

### Figure 28: Unfinished laboratory building at a health centre, Sironko District (Bugisu)
Output file: `outputs/narrative-report/figures/photo_26_sironko_unfinished_health_lab.jpg`.
UgIFT field photograph P26; raw-data-grouped/team-14/Sironko/Simu-Pondo-HC-III/06_unfinished-laboratory-building_ref20260829-0541.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph 06_unfinished-laboratory-building_ref20260829-0541.jpg under Simu-Pondo-HC-III/Sironko."}

### Figure 29: Empty computer laboratory at a seed secondary school, Kween District (Sebei)
Output file: `outputs/narrative-report/figures/photo_35_kween_empty_computer_laboratory.jpg`.
UgIFT field photograph P35; raw-data-grouped/team-15/Kween/Kaptum-Seed-Secondary-School/09_computer-lab-no-power-supply_ref0537.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph 09_computer-lab-no-power-supply_ref0537.jpg under Kaptum-Seed-Secondary-School/Kween. The source filename identifies the computer laboratory and no power supply."}

### Figure 30: Computer sets stacked in a store at Bumufuni Seed Secondary School, Bulambuli District (Bugisu)
Output file: `outputs/narrative-report/figures/photo_76_bumufuni_seed_secondary_school_computer_sets_stacked_in_a_store.jpg`.
UgIFT field photograph P76; raw-data-grouped/team-14/Bulambuli/Bumufuni-Seed-Secondary-School/07_computer-sets-stacked-in-store_ref20260911-0011.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Bulambuli / Bumufuni-Seed-Secondary-School; original filename: 07_computer-sets-stacked-in-store_ref20260911-0011.jpg."}

### Figure 31: Pedal suction unit in packaging at Majanji HC III, Busia District (Bukedi)
Output file: `outputs/narrative-report/figures/photo_75_majanji_hc_iii_pedal_suction_unit_in_packaging.jpg`.
UgIFT field photograph P75; raw-data-grouped/team-13/Busia/Majanji-HC-III/042_pedal-suction-unit-in-its-packing_ref20260827-0637.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Busia / Majanji-HC-III; original filename: 042_pedal-suction-unit-in-its-packing_ref20260827-0637.jpg."}

### Figure 32: Cracked health centre block above collapsed ground, Bulambuli District (Bugisu)
Output file: `outputs/narrative-report/figures/photo_14_bulambuli_structural_damage.jpg`.
UgIFT field photograph P14; raw-data-grouped/team-14/Bulambuli/Bukibologoto-HC-II/08_block-over-collapsed-ground-wide_ref20260911-0005.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph 08_block-over-collapsed-ground-wide_ref20260911-0005.jpg. Facility and local government are established by its Bukibologoto-HC-II/Bulambuli source folders."}

### Figure 33: Stained and peeling ceiling at a health centre, Sironko District (Bugisu)
Output file: `outputs/narrative-report/figures/photo_15_sironko_damaged_ceiling.jpg`.
UgIFT field photograph P15; raw-data-grouped/team-14/Sironko/Bundege-HC-III/15_water-damaged-ceiling_ref20260829-0569.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph 15_water-damaged-ceiling_ref20260829-0569.jpg under Bundege-HC-III/Sironko."}

### Figure 34: Water tank on a cracked base at a seed secondary school, Kibuku District (Bukedi)
Output file: `outputs/narrative-report/figures/photo_16_kibuku_cracked_tank_base.jpg`.
UgIFT field photograph P16; raw-data-grouped/team-12/Kibuku/Kasasira-Seed-Secondary-School/39_water-tank-on-cracked-base_ref0332.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph 39_water-tank-on-cracked-base_ref0332.jpg under Kasasira-Seed-Secondary-School/Kibuku."}

### Figure 35: Broken desk frame at a seed secondary school, Namisindwa District (Bugisu)
Output file: `outputs/narrative-report/figures/photo_27_namisindwa_broken_desk.jpg`.
UgIFT field photograph P27; raw-data-grouped/team-13/Namisindwa/Namboko/032_broken-desk_ref20260902-0126.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph 032_broken-desk_ref20260902-0126.jpg under Namboko/Namisindwa."}

### Figure 36: UgIFT engraving on a health centre bench, Bududa District (Bugisu)
Output file: `outputs/narrative-report/figures/photo_22_bududa_bench_engraving.jpg`.
UgIFT field photograph P22; raw-data-grouped/team-14/Bududa/Bududa-HC-III/09_bench-engraved-gou-moh-ugift-project_ref20260827-0187.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph 09_bench-engraved-gou-moh-ugift-project_ref20260827-0187.jpg under Bududa-HC-III/Bududa. Visible institutional marking reads GOU/MOH-UGIFT PROJECT and F/Y 2023/2024."}

### Figure 37: Engraving on a wheelchair armrest at Bumugibole HC III, Bulambuli District (Bugisu)
Output file: `outputs/narrative-report/figures/photo_77_bumugibole_hc_iii_engraving_on_a_wheelchair_armrest.jpg`.
UgIFT field photograph P77; raw-data-grouped/team-14/Bulambuli/Bumugibole-HC-III/05_wheelchair-armrest-engraving_ref20260831-0202.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Bulambuli / Bumugibole-HC-III; original filename: 05_wheelchair-armrest-engraving_ref20260831-0202.jpg."}

### Figure 38: Institutional engraving on equipment at Moyok HC III, Kween District (Sebei)
Output file: `outputs/narrative-report/figures/photo_85_moyok_hc_iii_institutional_engraving_on_equipment.jpg`.
UgIFT field photograph P85; raw-data-grouped/team-15/Kween/Moyok-HC-III/14_engraving-kwn-med-eq-moyok-hciii_ref0038.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kween / Moyok-HC-III; original filename: 14_engraving-kwn-med-eq-moyok-hciii_ref0038.jpg."}

### Figure 39: Autoclave at Atar HC III, Kween District (Sebei)
Output file: `outputs/narrative-report/figures/photo_81_atar_hc_iii_autoclave.jpg`.
UgIFT field photograph P81; raw-data-grouped/team-15/Kween/Atar-HC-III/07_autoclave-01_ref0458.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kween / Atar-HC-III; original filename: 07_autoclave-01_ref0458.jpg."}

### Figure 40: Solar batteries and control equipment at Atar HC III, Kween District (Sebei)
Output file: `outputs/narrative-report/figures/photo_82_atar_hc_iii_solar_batteries_and_control_equipment.jpg`.
UgIFT field photograph P82; raw-data-grouped/team-15/Kween/Atar-HC-III/21_solar-batteries_ref0444.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kween / Atar-HC-III; original filename: 21_solar-batteries_ref0444.jpg."}

### Figure 41: Kangaroo care chair at Atar HC III, Kween District (Sebei)
Output file: `outputs/narrative-report/figures/photo_83_atar_hc_iii_kangaroo_care_chair.jpg`.
UgIFT field photograph P83; raw-data-grouped/team-15/Kween/Atar-HC-III/36_kangaroo-mother-care-chair-1-not-engraved_ref20260830-0604.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kween / Atar-HC-III; original filename: 36_kangaroo-mother-care-chair-1-not-engraved_ref20260830-0604.jpg."}

### Figure 42: Solar batteries at Bunangaka HC III, Bulambuli District (Bugisu)
Output file: `outputs/narrative-report/figures/photo_78_bunangaka_hc_iii_solar_batteries.jpg`.
UgIFT field photograph P78; raw-data-grouped/team-14/Bulambuli/Bunangaka-HC-III/01_solar-batteries_ref20260830-0421.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Bulambuli / Bunangaka-HC-III; original filename: 01_solar-batteries_ref20260830-0421.jpg."}

### Figure 43: Infant weighing scale at Buwembe HC III, Busia District (Bukedi)
Output file: `outputs/narrative-report/figures/photo_72_buwembe_hc_iii_infant_weighing_scale.jpg`.
UgIFT field photograph P72; raw-data-grouped/team-13/Busia/Buwembe-HC-III/127_baby-weighing-scale-yrbb-20_ref20260828-0082.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Busia / Buwembe-HC-III; original filename: 127_baby-weighing-scale-yrbb-20_ref20260828-0082.jpg."}

### Figure 44: Autoclave above a gas cylinder at Buwembe HC III, Busia District (Bukedi)
Output file: `outputs/narrative-report/figures/photo_73_buwembe_hc_iii_autoclave_above_a_gas_cylinder.jpg`.
UgIFT field photograph P73; raw-data-grouped/team-13/Busia/Buwembe-HC-III/136_autoclave-on-a-gas-cylinder_ref20260828-0091.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Busia / Buwembe-HC-III; original filename: 136_autoclave-on-a-gas-cylinder_ref20260828-0091.jpg."}

### Figure 45: Computer equipment in the school ICT room at Kabeywa Seed Secondary School, Kapchorwa District (Sebei)
Output file: `outputs/narrative-report/figures/photo_79_kabeywa_seed_secondary_school_computer_equipment_in_the_school_ict_room.jpg`.
UgIFT field photograph P79; raw-data-grouped/team-15/Kapchorwa/Kabeywa-Seed-Secondary-School/07_28computers_ref20260830-0271.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kapchorwa / Kabeywa-Seed-Secondary-School; original filename: 07_28computers_ref20260830-0271.jpg."}

### Figure 46: Library shelving and tables at Kabeywa Seed Secondary School, Kapchorwa District (Sebei)
Output file: `outputs/narrative-report/figures/photo_80_kabeywa_seed_secondary_school_library_shelving_and_tables.jpg`.
UgIFT field photograph P80; raw-data-grouped/team-15/Kapchorwa/Kabeywa-Seed-Secondary-School/24_library_ref20260830-0842.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kapchorwa / Kabeywa-Seed-Secondary-School; original filename: 24_library_ref20260830-0842.jpg."}

### Figure 47: Water tanks on a steel tower at Kabweri HC III, Kibuku District (Bukedi)
Output file: `tmp/narrative-report/photos/extended/photo_121.jpg`.
UgIFT field photograph P121; raw-data-grouped/team-12/Kibuku/Kabweri-HC-III/05_water-tank-on-steel-tower_ref1262.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 48: Delivery bed with side rails at Kabweri HC III, Kibuku District (Bukedi)
Output file: `tmp/narrative-report/photos/extended/photo_122.jpg`.
UgIFT field photograph P122; raw-data-grouped/team-12/Kibuku/Kabweri-HC-III/28_delivery-bed-with-side-rails_ref1303.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 49: Anatomical skeleton teaching model at Kamonkoli Seed Secondary School, Budaka District (Bukedi)
Output file: `tmp/narrative-report/photos/extended/photo_116.jpg`.
UgIFT field photograph P116; raw-data-grouped/team-12/Budaka/Kamonkoli-Seed-Secondary-School/50_anatomical-skeleton-on-laboratory-wall_ref0755.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 50: Delivery bed with a torn mattress cover at a health centre, Busia District (Bukedi)
Output file: `outputs/narrative-report/figures/photo_04_eastern_torn_bed_cover.jpg`.
UgIFT field photograph P04; raw-data-grouped/team-13/Busia/Majanji-HC-III/050_delivery-bed-with-torn-cover_ref20260827-0646.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": null}

### Figure 51: Binocular microscope on a trolley at Namusita HC III, Budaka District (Bukedi)
Output file: `tmp/narrative-report/photos/extended/photo_117.jpg`.
UgIFT field photograph P117; raw-data-grouped/team-12/Budaka/Namusita-HC-III/024_microscope-binocular_ref0908.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 52: Infant weighing scales at Namusita HC III, Budaka District (Bukedi)
Output file: `tmp/narrative-report/photos/extended/photo_118.jpg`.
UgIFT field photograph P118; raw-data-grouped/team-12/Budaka/Namusita-HC-III/039_infant-weighing-scales-x2_ref0887.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 53: Laboratory benches, stools and sinks at Nansanga Seed Secondary School, Budaka District (Bukedi)
Output file: `tmp/narrative-report/photos/extended/photo_119.jpg`.
UgIFT field photograph P119; raw-data-grouped/team-12/Budaka/Nansanga-Seed-Secondary-School/035_laboratory-benches-stools-and-sink-run_ref0683.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 54: Library shelving with books at Nansanga Seed Secondary School, Budaka District (Bukedi)
Output file: `tmp/narrative-report/photos/extended/photo_120.jpg`.
UgIFT field photograph P120; raw-data-grouped/team-12/Budaka/Nansanga-Seed-Secondary-School/072_library-shelving-with-books_ref0729.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 55: Desktop computers and classroom furniture at a seed secondary school, Busia District (Bukedi)
Output file: `outputs/narrative-report/figures/photo_03_eastern_school_computers.jpg`.
UgIFT field photograph P03; raw-data-grouped/team-13/Busia/Sikuda-Seed-Secondary-School/43_ict-room-desktop-computers_ref0257.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": null}

### Figure 56: Building works and construction materials at Ndhew Seed Secondary School, Nebbi District (West Nile)
Output file: `outputs/narrative-report/figures/photo_23_ndhew_construction.jpg`.
UgIFT field photograph P23; raw-data-grouped/team-01/Nebbi/_district-documents/UGIFT Assets Verification Nebbi District Report.docx; {"embedded_image": "word/media/image17.jpeg", "body_block": 89, "table": null, "adjacent_text": "Nebbi district report image17.jpeg at body block 89, within the Ndhew school section beginning at block 40 and field photographs beginning at block 63. Block 42 records ongoing construction and ICT/science equipment at district headquarters; block 59 links construction delay with equipment installation delay."}

### Figure 57: Unfinished classroom block at Sidok Seed Secondary School, Kaabong District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_50_sidok_seed_secondary_school_unfinished_classroom_block.jpg`.
UgIFT field photograph P50; raw-data-grouped/team-11/Kaabong/Sidok-Seed-Secondary-School/16_classroom-block-under-construction_ref0316.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kaabong / Sidok-Seed-Secondary-School; original filename: 16_classroom-block-under-construction_ref0316.jpg."}

### Figure 58: Latrine block under construction at Sidok Seed Secondary School, Kaabong District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_51_sidok_seed_secondary_school_latrine_block_under_construction.jpg`.
UgIFT field photograph P51; raw-data-grouped/team-11/Kaabong/Sidok-Seed-Secondary-School/33_latrine-block-under-construction_ref0310.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kaabong / Sidok-Seed-Secondary-School; original filename: 33_latrine-block-under-construction_ref0310.jpg."}

### Figure 59: Computer and library block interior with furniture and stored items at Iriiri Seed Secondary School, Napak District (Karamoja)
Output file: `tmp/narrative-report/photos/extended/photo_112.jpg`.
UgIFT field photograph P112; raw-data-grouped/team-10/Napak/Iriiri-Seed-Secondary-School/30_ict-and-library-block_ref20260827-0466.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 60: Stacked desks, chairs and stools at a seed secondary school, Napak District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_18_napak_stacked_furniture.jpg`.
UgIFT field photograph P18; raw-data-grouped/team-10/Napak/Napak-Seed-Secondary-School/25_furniture-some-broken-none-engraved_ref20260827-0417.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph 25_furniture-some-broken-none-engraved_ref20260827-0417.jpg under Napak-Seed-Secondary-School/Napak."}

### Figure 61: Damaged drip stand at a health centre, Moroto District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_25_moroto_broken_drip_stand.jpg`.
UgIFT field photograph P25; raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/124_broken-drip-stand_ref20260827-0349.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph 124_broken-drip-stand_ref20260827-0349.jpg under Kalemungole-HC-III/Moroto. The stand lacks its supporting base. Crop retains the stand and a gloved hand; no face or identifier is present."}

### Figure 62: Programme engraving on a weighing scale at Kalemungole HC III, Moroto District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_38_kalemungole_hc_iii_programme_engraving_on_a_weighing_scale.jpg`.
UgIFT field photograph P38; raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/10_engraving-weighing-scale_ref20260826-0429.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 10_engraving-weighing-scale_ref20260826-0429.jpg."}

### Figure 63: Programme engraving on a delivery bed at Kalemungole HC III, Moroto District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_39_kalemungole_hc_iii_programme_engraving_on_a_delivery_bed.jpg`.
UgIFT field photograph P39; raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/37_engraving-delivery-bed_ref20260826-0456.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 37_engraving-delivery-bed_ref20260826-0456.jpg."}

### Figure 64: Programme engraving on a table at Kamoru HC III, Kotido District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_53_kamoru_hc_iii_programme_engraving_on_a_table.jpg`.
UgIFT field photograph P53; raw-data-grouped/team-11/Kotido/Kamoru-HC-III/18_engraved-table-top_ref1107.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kotido / Kamoru-HC-III; original filename: 18_engraved-table-top_ref1107.jpg."}

### Figure 65: Classroom furniture with school markings at Rupa Seed School, Moroto District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_44_rupa_seed_school_classroom_furniture_with_school_markings.jpg`.
UgIFT field photograph P44; raw-data-grouped/team-10/Moroto/Rupa-Seed-School/18_classroom-furniture-engraved-rupa-seed_ref20260909-photo-p08.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Moroto / Rupa-Seed-School; original filename: 18_classroom-furniture-engraved-rupa-seed_ref20260909-photo-p08.jpg."}

### Figure 66: Water tanks on a rendered plinth and steel tower at Alerek Seed Secondary School, Abim District (Karamoja)
Output file: `tmp/narrative-report/photos/positive/p47_positive.jpg`.
UgIFT field photograph P47; raw-data-grouped/team-11/Abim/Alerek-Seed-Secondary-School/23_water-tank-on-a-plinth-and-elevated-tank_ref0870.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 67: Laboratory reagent containers at Alerek Seed Secondary School, Abim District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_48_alerek_seed_secondary_school_laboratory_reagent_containers.jpg`.
UgIFT field photograph P48; raw-data-grouped/team-11/Abim/Alerek-Seed-Secondary-School/44_laboratory-chemicals-on-the-bench_ref0859.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Abim / Alerek-Seed-Secondary-School; original filename: 44_laboratory-chemicals-on-the-bench_ref0859.jpg."}

### Figure 68: Health centre building, Nwoya District (Acholi)
Output file: `outputs/narrative-report/figures/photo_06_northern_health_building.jpg`.
UgIFT field photograph P06; raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx; {"embedded_image": "word/media/image37.jpeg", "body_block": 308, "table": null, "adjacent_text": ""}

### Figure 69: Section of the science laboratory exterior at Iriiri Seed Secondary School, Napak District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_45_iriiri_seed_secondary_school_section_of_the_science_laboratory_exterior.jpg`.
UgIFT field photograph P45; raw-data-grouped/team-10/Napak/Iriiri-Seed-Secondary-School/33_science-laboratory_ref20260827-0463.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Napak / Iriiri-Seed-Secondary-School; original filename: 33_science-laboratory_ref20260827-0463.jpg."}

### Figure 70: Refrigerator bearing programme identification at Kalemungole HC III, Moroto District (Karamoja)
Output file: `tmp/narrative-report/photos/extended/photo_110.jpg`.
UgIFT field photograph P110; raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/114_refrigerator-engraved-gou-moh-ugift-project_ref20260827-0359.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 71: Solar panels at Kalemungole HC III, Moroto District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_36_kalemungole_hc_iii_solar_panels.jpg`.
UgIFT field photograph P36; raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/102_water-system-solar-panels-and-tanks_ref20260827-0369.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 102_water-system-solar-panels-and-tanks_ref20260827-0369.jpg."}

### Figure 72: Patient toilet block at Kalemungole HC III, Moroto District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_37_kalemungole_hc_iii_patient_toilet_block.jpg`.
UgIFT field photograph P37; raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/108_patient-toilets_ref20260827-0367.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 108_patient-toilets_ref20260827-0367.jpg."}

### Figure 73: Oxygen concentrator at Kalemungole HC III, Moroto District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_40_kalemungole_hc_iii_oxygen_concentrator.jpg`.
UgIFT field photograph P40; raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/40_oxygen-concentrator_ref20260826-0459.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 40_oxygen-concentrator_ref20260826-0459.jpg."}

### Figure 74: Suction apparatus at Kalemungole HC III, Moroto District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_41_kalemungole_hc_iii_suction_apparatus.jpg`.
UgIFT field photograph P41; raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/50_suction-apparatus_ref20260826-0469.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 50_suction-apparatus_ref20260826-0469.jpg."}

### Figure 75: Wheelchair with programme marking at Kalemungole HC III, Moroto District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_42_kalemungole_hc_iii_wheelchair_with_programme_marking.jpg`.
UgIFT field photograph P42; raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/69_wheelchair-marked-gou-moh-ugift_ref20260826-0488.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 69_wheelchair-marked-gou-moh-ugift_ref20260826-0488.jpg."}

### Figure 76: Instrument trolley with delivery instruments at Kamoru HC III, Kotido District (Karamoja)
Output file: `tmp/narrative-report/photos/extended/photo_114.jpg`.
UgIFT field photograph P114; raw-data-grouped/team-11/Kotido/Kamoru-HC-III/07_instrument-trolley-with-a-delivery-set_ref1176.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 77: Microscope bearing local facility identification at Kamoru HC III, Kotido District (Karamoja)
Output file: `tmp/narrative-report/photos/extended/photo_115.jpg`.
UgIFT field photograph P115; raw-data-grouped/team-11/Kotido/Kamoru-HC-III/28_microscope-marked-kamoru-hc-iii_ref1144.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 78: Oxygen concentrator at Kamoru HC III, Kotido District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_52_kamoru_hc_iii_oxygen_concentrator.jpg`.
UgIFT field photograph P52; raw-data-grouped/team-11/Kotido/Kamoru-HC-III/15_oxygen-concentrator_ref1167.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kotido / Kamoru-HC-III; original filename: 15_oxygen-concentrator_ref1167.jpg."}

### Figure 79: Borehole apron and pipework at Katikekire Seed School, Moroto District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_43_katikekire_seed_school_borehole_apron_and_pipework.jpg`.
UgIFT field photograph P43; raw-data-grouped/team-10/Moroto/Katikekire-Seed-School/02_borehole-apron-and-pipework_ref20260826-0421.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Moroto / Katikekire-Seed-School; original filename: 02_borehole-apron-and-pipework_ref20260826-0421.jpg."}

### Figure 80: Computer and library block at Lopei Seed Secondary School, Napak District (Karamoja)
Output file: `tmp/narrative-report/photos/extended/photo_113.jpg`.
UgIFT field photograph P113; raw-data-grouped/team-10/Napak/Lopei-Seed-Secondary-School/08_ict-and-library-block_ref20260828-0570.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 81: Water storage tanks at Lopei Seed Secondary School, Napak District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_46_lopei_seed_secondary_school_water_storage_tanks.jpg`.
UgIFT field photograph P46; raw-data-grouped/team-10/Napak/Lopei-Seed-Secondary-School/20_water-tanks_ref20260828-0562.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Napak / Lopei-Seed-Secondary-School; original filename: 20_water-tanks_ref20260828-0562.jpg."}

### Figure 82: Buildings at a seed secondary school, Nwoya District (Acholi)
Output file: `outputs/narrative-report/figures/photo_05_northern_school_buildings.jpg`.
UgIFT field photograph P05; raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx; {"embedded_image": "word/media/image14.jpeg", "body_block": 107, "table": null, "adjacent_text": ""}

### Figure 83: Water storage tanks at Rengen Seed School, Kotido District (Karamoja)
Output file: `outputs/narrative-report/figures/photo_54_rengen_seed_school_water_storage_tanks.jpg`.
UgIFT field photograph P54; raw-data-grouped/team-11/Kotido/Rengen-Seed-School/10_water-tanks-x2_ref0642.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kotido / Rengen-Seed-School; original filename: 10_water-tanks-x2_ref0642.jpg."}

### Figure 84: Rainwater tank beside a staff house at Rupa Seed School, Moroto District (Karamoja)
Output file: `tmp/narrative-report/photos/extended/photo_111.jpg`.
UgIFT field photograph P111; raw-data-grouped/team-10/Moroto/Rupa-Seed-School/17_water-tank-beside-a-staff-house_ref20260909-photo-p07.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 85: Laboratory supplies and an anatomical teaching model at Rupa Seed School, Moroto District (Karamoja)
Output file: `tmp/narrative-report/photos/positive/p49_positive.jpg`.
UgIFT field photograph P49; raw-data-grouped/team-10/Moroto/Rupa-Seed-School/33_laboratory-store-shelving-with-chemicals-and-a-skeleton_ref20260909-photo-p23.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 86: Classroom block with earthworks in the foreground at Kihungya Seed Secondary School, Buliisa District (Bunyoro)
Output file: `tmp/narrative-report/photos/extended/photo_102.jpg`.
UgIFT field photograph P102; raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/classroom block.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 87: Biology laboratory under construction at a seed secondary school, Buliisa District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_31_buliisa_laboratory_works.jpg`.
UgIFT field photograph P31; raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/boilogy lab under construction.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph boilogy lab under construction.jpg under Kihungya-Seed-Secondary-School/Buliisa. kihungya seed school.docx body block 107 identifies the science block as not in use and under construction; block 63 states that most structures were not ready and there was no electricity for ICT sessions or water for sanitation."}

### Figure 88: Unfinished laboratory interior at Kihungya Seed Secondary School, Buliisa District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_57_kihungya_seed_secondary_school_unfinished_laboratory_interior.jpg`.
UgIFT field photograph P57; raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/IMG-20260905-WA0028.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Buliisa / Kihungya-Seed-Secondary-School; original filename: IMG-20260905-WA0028.jpg."}

### Figure 89: Library interior under construction at Kihungya Seed Secondary School, Buliisa District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_58_kihungya_seed_secondary_school_library_interior_under_construction.jpg`.
UgIFT field photograph P58; raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/library.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Buliisa / Kihungya-Seed-Secondary-School; original filename: library.jpg."}

### Figure 90: Laboratory benches with cupboard doors detached at King Solomon Seed Secondary School, Kagadi District (Bunyoro)
Output file: `tmp/narrative-report/photos/extended/photo_106.jpg`.
UgIFT field photograph P106; raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_120333_732.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 91: Laboratory stools and other school furniture in storage, Ntoroko District (Tooro)
Output file: `outputs/narrative-report/figures/photo_20_butungama_stored_furniture.jpg`.
UgIFT field photograph P20; raw-data-grouped/team-26/_team-documents/Butungama Seed School.pdf; {"embedded_image": "PDF page 12, image 1", "body_block": null, "table": null, "adjacent_text": "Photographic PDF page 12. The paired return raw-data-grouped/team-26/Ntoroko/Butungama-Seed-Secondary-School/ASSET VERIFICATION AND RECORDING TOOL KIT 222 BUTUNGAMA HEALTH CENTRE III AND BUTUNGAMA SEED SCHOOL (1).docx, body block 162, records laboratory stools, desks, office chairs and tables in good condition but not in use, still stored. Blocks 119 and 178 describe ongoing construction.", "page": 12}

### Figure 92: Clinical equipment packed among cartons at a health centre, Hoima City (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_19_hoima_stored_clinical_equipment.jpg`.
UgIFT field photograph P19; raw-data-grouped/_multi-team/programme-documents/data-management-chat/unpacked/TEAM 25 HEALTH CENTHERA/TEAM 25 HEALTH CENTHERA/KIHUUKYA HEALTH CENTER III/kihuukya photos/stored equipement nort in use.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph in the KIHUUKYA HEALTH CENTER III/kihuukya photos folder. It is byte-identical (SHA256 a76c46aa7f6ab2856ac601a320125dfdf7cb174a6ec0c29eec25dab06232de97) to the team-25/_team-documents copy. The KIHUUKYA HEALTHCENTER III. Edited.docx return, block 29, identifies Hoima City and Bunyoro; block 38 names the facility."}

### Figure 93: Stacked classroom furniture at King Solomon Seed Secondary School, Kagadi District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_59_king_solomon_seed_secondary_school_stacked_classroom_furniture.jpg`.
UgIFT field photograph P59; raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115519_265.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115519_265.jpg."}

### Figure 94: Boxed projector and other equipment at King Solomon Seed Secondary School, Kagadi District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_62_king_solomon_seed_secondary_school_boxed_projector_and_other_equipment.jpg`.
UgIFT field photograph P62; raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_120857_349.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_120857_349.jpg."}

### Figure 95: Hospital beds and screens stacked in storage at a health centre, Kagadi District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_30_kagadi_beds_in_storage.jpg`.
UgIFT field photograph P30; raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/BEDS IN STORAGE .jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph BEDS IN STORAGE .jpg under Kyabasara-HC-III/Kagadi. The source filename and visible stacking identify storage."}

### Figure 96: Flood-affected older health facility at Butiaba, Buliisa District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_32_buliisa_flood_affected_old_facility.jpg`.
UgIFT field photograph P32; raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/butaiba submurged facility.jpeg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose photograph butaiba submurged facility.jpeg under Butiaba-HC-III/Buliisa. The paired butaiba report.docx body block 11 (paragraph 10) explicitly states that the old facility built by UgIFT and its equipment were affected by floods."}

### Figure 97: School engraving on wooden furniture at King Solomon Seed Secondary School, Kagadi District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_61_king_solomon_seed_secondary_school_school_engraving_on_wooden_furniture.jpg`.
UgIFT field photograph P61; raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115836_836.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115836_836.jpg."}

### Figure 98: Programme engraving on a table at Kyabasara HC III, Kagadi District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_64_kyabasara_hc_iii_programme_engraving_on_a_table.jpg`.
UgIFT field photograph P64; raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/IMG-20260908-WA0107.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: IMG-20260908-WA0107.jpg."}

### Figure 99: Blood pressure apparatus on a mobile stand at Butiaba HC III, Buliisa District (Bunyoro)
Output file: `tmp/narrative-report/photos/extended/photo_100.jpg`.
UgIFT field photograph P100; raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/IMG-20260907-WA0094.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 100: Office chairs at Butiaba HC III, Buliisa District (Bunyoro)
Output file: `tmp/narrative-report/photos/extended/photo_101.jpg`.
UgIFT field photograph P101; raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/office chairs.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 101: Medical-waste bins and ward beds at Butiaba HC III, Buliisa District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_55_butiaba_hc_iii_medical_waste_bins_and_ward_beds.jpg`.
UgIFT field photograph P55; raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/dust bins.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Buliisa / Butiaba-HC-III; original filename: dust bins.jpg."}

### Figure 102: Laboratory centrifuge at Butiaba HC III, Buliisa District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_56_butiaba_hc_iii_laboratory_centrifuge.jpg`.
UgIFT field photograph P56; raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/IMG-20260907-WA0097.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Buliisa / Butiaba-HC-III; original filename: IMG-20260907-WA0097.jpg."}

### Figure 103: Delivery bed and clinical furniture at a health centre, Kabarole District (Tooro)
Output file: `outputs/narrative-report/figures/photo_09_western_delivery_bed.jpg`.
UgIFT field photograph P09; raw-data-grouped/team-26/Kabarole/Iruhura-HC-III/KABAROLE DISTRICT   IRUHURA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222 (1).docx; {"embedded_image": "word/media/image10.jpeg", "body_block": 96, "table": null, "adjacent_text": "OPD                                           |                               |      | Pit latrine |                               |                       Power House |                       | Weighing scale with a height meter"}

### Figure 104: Water tank on a masonry support at King Solomon Seed Secondary School, Kagadi District (Bunyoro)
Output file: `tmp/narrative-report/photos/extended/photo_105.jpg`.
UgIFT field photograph P105; raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115648_996.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 105: Elevated water tank on a steel tower at King Solomon Seed Secondary School, Kagadi District (Bunyoro)
Output file: `tmp/narrative-report/photos/extended/photo_107.jpg`.
UgIFT field photograph P107; raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_121530_409.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 106: Classroom desks at King Solomon Seed Secondary School, Kagadi District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_60_king_solomon_seed_secondary_school_classroom_desks.jpg`.
UgIFT field photograph P60; raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115826_769.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115826_769.jpg."}

### Figure 107: Gas cylinders and pipework at King Solomon Seed Secondary School, Kagadi District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_63_king_solomon_seed_secondary_school_gas_cylinders_and_pipework.jpg`.
UgIFT field photograph P63; raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_121503_686.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_121503_686.jpg."}

### Figure 108: Latrine block and paved access at Kyabasara HC III, Kagadi District (Bunyoro)
Output file: `tmp/narrative-report/photos/extended/photo_109.jpg`.
UgIFT field photograph P109; raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/latrines.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 109: Kangaroo care chair at Kyabasara HC III, Kagadi District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_65_kyabasara_hc_iii_kangaroo_care_chair.jpg`.
UgIFT field photograph P65; raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/kangaro chair.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: kangaro chair.jpg."}

### Figure 110: Power house at Kyabasara HC III, Kagadi District (Bunyoro)
Output file: `outputs/narrative-report/figures/photo_66_kyabasara_hc_iii_power_house.jpg`.
UgIFT field photograph P66; raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/power house.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": "Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: power house.jpg."}

### Figure 111: Classroom desks at a seed secondary school, Ntoroko District (Tooro)
Output file: `outputs/narrative-report/figures/photo_08_western_classroom_desks.jpg`.
UgIFT field photograph P08; raw-data-grouped/team-26/Ntoroko/Nombe-Seed-Secondary-School/NTOROKO ASSET NOMBE SEED SECONDARY SCHOOL VERIFICATION AND RECORDING TOOL KIT 222.docx; {"embedded_image": "word/media/image4.jpeg", "body_block": 110, "table": null, "adjacent_text": "Equipment/ Item | Department | Asset Number | Item | Description | Life in Months | Tag Number  | ( engrave |  no.) | Date Of  | Pur | Date Placed  | In |  Service | Recoverable cost | Cost | Acc Dep Cost | Net Book Value | Ytd |   | Deprn | Equipment status | Remarks | Non residential | Education | Painted cream and white | Good condition | They are in use. They are seven in number. | Residential | Education | Painted cream and white | Good condition | They are all in use. | They are 3 in number. | Kitchen | Education | Not built. | Toilets | Education | Not constructed | Pit latrine | Education | They are painted cream and white. | Good condition | They are all in use. | They are all in use. | 3 are for residential and 3 are not for residential. | Water tanks | Education | They are black in  | colour | One is faulty and  | two are working. | Two in use.  | They re |  three. Not constructed. | Fence | Not constructed."}

### Figure 112: Most eligible assets lacked a recorded mark
Output file: `outputs/narrative-report/figures/chart_04_engraving.png`.
Source: REF Asset Register, TAG_NUMBER on movable assets; buildings, structures and land excluded.

### Figure 113: UgIFT identification on a desk at a seed school, Tororo District (Bukedi)
Output file: `outputs/narrative-report/figures/photo_10_eastern_ugift_marking.jpg`.
UgIFT field photograph P10; raw-data-grouped/team-13/Tororo/Malaba-Seed-School/049_desk-engraving-gou-moh-ugift_ref20260829-0338.jpg; {"embedded_image": null, "body_block": null, "table": null, "adjacent_text": null}

### Figure 114: Boxed computers and related equipment in a seed school store, Nwoya District (Acholi)
Output file: `outputs/narrative-report/figures/photo_07_northern_stored_computers.jpg`.
UgIFT field photograph P07; raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx; {"embedded_image": "word/media/image9.jpeg", "body_block": 83, "table": null, "adjacent_text": "Laboratory stool supply: Procure and deliver an additional cohort of laboratory stools (recommended minimum 66 stools) to meet the standard lab allocation of 74 stools. | Field photos"}

### Figure 115: Adult weighing scale with a height meter and waiting benches at Iruhura HC III, Kabarole District (Tooro)
Output file: `tmp/narrative-report/photos/positive/p108_positive.jpg`.
UgIFT field photograph P108; raw-data-grouped/team-26/Kabarole/Iruhura-HC-III/KABAROLE DISTRICT   IRUHURA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222 (1).docx; {"embedded_image": "word/media/image13.jpeg", "body_block": 105, "table": null, "adjacent_text": "Weighing scale with heighmeter & desk |       | Tank |                                 |                                                 Residentials "}

### Figure 116: Maternity block entrance and access ramp at Kamuli HC III, Tororo District (Bukedi)
Output file: `tmp/narrative-report/photos/positive/p29_positive.jpg`.
UgIFT field photograph P29; raw-data-grouped/team-13/Tororo/Kamuli-HC-III/24_maternity-ward-building_ref20260831-0456.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 117: Health centre building at Kibiri HC III, Makindye-Ssabagabo Municipal Council (Buganda)
Output file: `tmp/narrative-report/photos/positive/p86_positive.jpg`.
UgIFT field photograph P86; raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx; {"embedded_image": "word/media/image16.jpeg", "body_block": 77, "table": null, "adjacent_text": ""}

### Figure 118: Health centre buildings and covered walkway at Kihuukya HC III, Hoima City (Bunyoro)
Output file: `tmp/narrative-report/photos/extended/photo_103.jpg`.
UgIFT field photograph P103; raw-data-grouped/team-25/Hoima City/Kihuukya-HC-III/IMG-20260908-WA0045.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 119: Binocular microscope at Kihuukya HC III, Hoima City (Bunyoro)
Output file: `tmp/narrative-report/photos/extended/photo_104.jpg`.
UgIFT field photograph P104; raw-data-grouped/team-25/Hoima City/Kihuukya-HC-III/microscope.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 120: Classroom furnished with desks and a whiteboard at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda)
Output file: `tmp/narrative-report/photos/positive/p89_positive.jpg`.
UgIFT field photograph P89; raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx; {"embedded_image": "word/media/image5.jpeg", "body_block": 19, "table": null, "adjacent_text": "3. Desks | 3. Desks"}

### Figure 121: Books displayed on library shelves at Sibanga Seed School, Manafwa District (Bugisu)
Output file: `tmp/narrative-report/photos/positive/p28_positive.jpg`.
UgIFT field photograph P28; raw-data-grouped/team-13/Manafwa/Sibanga-Seed-School/58_library-shelves-with-books_ref20260904-0059.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 122: ICT laboratory block and entrance ramp at Sisiyi Seed Secondary School, Bulambuli District (Bugisu)
Output file: `tmp/narrative-report/photos/positive/p74_positive.jpg`.
UgIFT field photograph P74; raw-data-grouped/team-14/Bulambuli/Sisiyi-Seed-Secondary-School/15_ict-laboratory-block_ref20260828-0015.jpg; {"embedded_image": null, "body_block": null, "table": null}

### Figure 123: School furniture forms the largest asset category
Output file: `outputs/narrative-report/figures/chart_02_condition_category.png`.
Source: REF Asset Register, all rows; report category and ATTRIBUTE14 condition.

### Figure 124: The Functional classification predominates across sub-regions
Output file: `outputs/narrative-report/figures/chart_03_condition_subregion.png`.
Source: REF Asset Register, local government rows; sub-region mapping and ATTRIBUTE14.

### Figure 125: Eastern holds the largest regional recorded value
Output file: `outputs/narrative-report/figures/chart_05_value_region.png`.
Source: REF Asset Register, cost and depreciation; row net book value floored at zero.

### Figure 126: MoFPED and MoES hold the largest ministry recorded values
Output file: `outputs/narrative-report/figures/chart_06_value_mda.png`.
Source: REF Asset Register, national ministry and agency book codes; all held facility types.

### Figure 127: Recorded use is concentrated in school furniture
Output file: `outputs/narrative-report/figures/chart_07_use_category.png`.
Source: REF Asset Register, IN_USE_FLAG; SK condition and remarks for non-use reasons.

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

### P11
`raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`; `word/media/image1.jpeg`; body block 31; adjacent text: Nwoya district report body block 7 identifies Got Apwoyo Seed Secondary School. Blocks 10 to 14 describe ongoing construction, no commissioning, and ICT held at the district. Field photographs begin at block 30; image1.jpeg occurs at block 31.
Nwoya district report body block 7 identifies Got Apwoyo Seed Secondary School. Blocks 10 to 14 describe ongoing construction, no commissioning, and ICT held at the district. Field photographs begin at block 30; image1.jpeg occurs at block 31.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P12
`raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx`; `word/media/image6.jpeg`; body block 79; adjacent text: Lwamata school return body block 11 identifies the school, block 33 states that some buildings remain under construction and laboratory equipment was expected after structures were completed. Image6.jpeg is at block 79 after PICTURES OF ASSETS VISITED AND VERIFIED.
Lwamata school return body block 11 identifies the school, block 33 states that some buildings remain under construction and laboratory equipment was expected after structures were completed. Image6.jpeg is at block 79 after PICTURES OF ASSETS VISITED AND VERIFIED.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P13
`raw-data-grouped/team-26/_team-documents/Butungama Seed School.pdf`; `PDF page 7, image 1`; body block None; adjacent text: Photographic PDF page 7; the school sign appears on page 3. The paired return raw-data-grouped/team-26/Ntoroko/Butungama-Seed-Secondary-School/ASSET VERIFICATION AND RECORDING TOOL KIT 222 BUTUNGAMA HEALTH CENTRE III AND BUTUNGAMA SEED SCHOOL (1).docx, body blocks 113, 119 and 178 identify the school and ongoing construction.
Photographic PDF page 7; the school sign appears on page 3. The paired return raw-data-grouped/team-26/Ntoroko/Butungama-Seed-Secondary-School/ASSET VERIFICATION AND RECORDING TOOL KIT 222 BUTUNGAMA HEALTH CENTRE III AND BUTUNGAMA SEED SCHOOL (1).docx, body blocks 113, 119 and 178 identify the school and ongoing construction.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P14
`raw-data-grouped/team-14/Bulambuli/Bukibologoto-HC-II/08_block-over-collapsed-ground-wide_ref20260911-0005.jpg`; `None`; body block None; adjacent text: Loose photograph 08_block-over-collapsed-ground-wide_ref20260911-0005.jpg. Facility and local government are established by its Bukibologoto-HC-II/Bulambuli source folders.
Loose photograph 08_block-over-collapsed-ground-wide_ref20260911-0005.jpg. Facility and local government are established by its Bukibologoto-HC-II/Bulambuli source folders.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P15
`raw-data-grouped/team-14/Sironko/Bundege-HC-III/15_water-damaged-ceiling_ref20260829-0569.jpg`; `None`; body block None; adjacent text: Loose photograph 15_water-damaged-ceiling_ref20260829-0569.jpg under Bundege-HC-III/Sironko.
Loose photograph 15_water-damaged-ceiling_ref20260829-0569.jpg under Bundege-HC-III/Sironko.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P16
`raw-data-grouped/team-12/Kibuku/Kasasira-Seed-Secondary-School/39_water-tank-on-cracked-base_ref0332.jpg`; `None`; body block None; adjacent text: Loose photograph 39_water-tank-on-cracked-base_ref0332.jpg under Kasasira-Seed-Secondary-School/Kibuku.
Loose photograph 39_water-tank-on-cracked-base_ref0332.jpg under Kasasira-Seed-Secondary-School/Kibuku.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P18
`raw-data-grouped/team-10/Napak/Napak-Seed-Secondary-School/25_furniture-some-broken-none-engraved_ref20260827-0417.jpg`; `None`; body block None; adjacent text: Loose photograph 25_furniture-some-broken-none-engraved_ref20260827-0417.jpg under Napak-Seed-Secondary-School/Napak.
Loose photograph 25_furniture-some-broken-none-engraved_ref20260827-0417.jpg under Napak-Seed-Secondary-School/Napak.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P19
`raw-data-grouped/_multi-team/programme-documents/data-management-chat/unpacked/TEAM 25 HEALTH CENTHERA/TEAM 25 HEALTH CENTHERA/KIHUUKYA HEALTH CENTER III/kihuukya photos/stored equipement nort in use.jpg`; `None`; body block None; adjacent text: Loose photograph in the KIHUUKYA HEALTH CENTER III/kihuukya photos folder. It is byte-identical (SHA256 a76c46aa7f6ab2856ac601a320125dfdf7cb174a6ec0c29eec25dab06232de97) to the team-25/_team-documents copy. The KIHUUKYA HEALTHCENTER III. Edited.docx return, block 29, identifies Hoima City and Bunyoro; block 38 names the facility.
Loose photograph in the KIHUUKYA HEALTH CENTER III/kihuukya photos folder. It is byte-identical (SHA256 a76c46aa7f6ab2856ac601a320125dfdf7cb174a6ec0c29eec25dab06232de97) to the team-25/_team-documents copy. The KIHUUKYA HEALTHCENTER III. Edited.docx return, block 29, identifies Hoima City and Bunyoro; block 38 names the facility.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P20
`raw-data-grouped/team-26/_team-documents/Butungama Seed School.pdf`; `PDF page 12, image 1`; body block None; adjacent text: Photographic PDF page 12. The paired return raw-data-grouped/team-26/Ntoroko/Butungama-Seed-Secondary-School/ASSET VERIFICATION AND RECORDING TOOL KIT 222 BUTUNGAMA HEALTH CENTRE III AND BUTUNGAMA SEED SCHOOL (1).docx, body block 162, records laboratory stools, desks, office chairs and tables in good condition but not in use, still stored. Blocks 119 and 178 describe ongoing construction.
Photographic PDF page 12. The paired return raw-data-grouped/team-26/Ntoroko/Butungama-Seed-Secondary-School/ASSET VERIFICATION AND RECORDING TOOL KIT 222 BUTUNGAMA HEALTH CENTRE III AND BUTUNGAMA SEED SCHOOL (1).docx, body block 162, records laboratory stools, desks, office chairs and tables in good condition but not in use, still stored. Blocks 119 and 178 describe ongoing construction.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P21
`raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`; `word/media/image17.jpeg`; body block 77; adjacent text: Kibiri Health Centre III report image17.jpeg, body block 77. Blocks 1 and 5 identify Kibiri; the packaging explicitly identifies Handheld Pulse Oximeter.
Kibiri Health Centre III report image17.jpeg, body block 77. Blocks 1 and 5 identify Kibiri; the packaging explicitly identifies Handheld Pulse Oximeter.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P22
`raw-data-grouped/team-14/Bududa/Bududa-HC-III/09_bench-engraved-gou-moh-ugift-project_ref20260827-0187.jpg`; `None`; body block None; adjacent text: Loose photograph 09_bench-engraved-gou-moh-ugift-project_ref20260827-0187.jpg under Bududa-HC-III/Bududa. Visible institutional marking reads GOU/MOH-UGIFT PROJECT and F/Y 2023/2024.
Loose photograph 09_bench-engraved-gou-moh-ugift-project_ref20260827-0187.jpg under Bududa-HC-III/Bududa. Visible institutional marking reads GOU/MOH-UGIFT PROJECT and F/Y 2023/2024.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P23
`raw-data-grouped/team-01/Nebbi/_district-documents/UGIFT Assets Verification Nebbi District Report.docx`; `word/media/image17.jpeg`; body block 89; adjacent text: Nebbi district report image17.jpeg at body block 89, within the Ndhew school section beginning at block 40 and field photographs beginning at block 63. Block 42 records ongoing construction and ICT/science equipment at district headquarters; block 59 links construction delay with equipment installation delay.
Nebbi district report image17.jpeg at body block 89, within the Ndhew school section beginning at block 40 and field photographs beginning at block 63. Block 42 records ongoing construction and ICT/science equipment at district headquarters; block 59 links construction delay with equipment installation delay.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P25
`raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/124_broken-drip-stand_ref20260827-0349.jpg`; `None`; body block None; adjacent text: Loose photograph 124_broken-drip-stand_ref20260827-0349.jpg under Kalemungole-HC-III/Moroto. The stand lacks its supporting base. Crop retains the stand and a gloved hand; no face or identifier is present.
Loose photograph 124_broken-drip-stand_ref20260827-0349.jpg under Kalemungole-HC-III/Moroto. The stand lacks its supporting base. Crop retains the stand and a gloved hand; no face or identifier is present.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P26
`raw-data-grouped/team-14/Sironko/Simu-Pondo-HC-III/06_unfinished-laboratory-building_ref20260829-0541.jpg`; `None`; body block None; adjacent text: Loose photograph 06_unfinished-laboratory-building_ref20260829-0541.jpg under Simu-Pondo-HC-III/Sironko.
Loose photograph 06_unfinished-laboratory-building_ref20260829-0541.jpg under Simu-Pondo-HC-III/Sironko.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P27
`raw-data-grouped/team-13/Namisindwa/Namboko/032_broken-desk_ref20260902-0126.jpg`; `None`; body block None; adjacent text: Loose photograph 032_broken-desk_ref20260902-0126.jpg under Namboko/Namisindwa.
Loose photograph 032_broken-desk_ref20260902-0126.jpg under Namboko/Namisindwa.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P28
`raw-data-grouped/team-13/Manafwa/Sibanga-Seed-School/58_library-shelves-with-books_ref20260904-0059.jpg`; `None`; body block None; adjacent text: 
Books and shelving visibly present only; no quantified outcome or full-commissioning claim.
Full original inspected individually. No people, identifiable records, signatures or phone numbers are visible. Covers show educational book titles; no personal name is legible. No crop needed.

### P29
`raw-data-grouped/team-13/Tororo/Kamuli-HC-III/24_maternity-ward-building_ref20260831-0456.jpg`; `None`; body block None; adjacent text: 
Visible entrance ramp and facility frontage only; avoid a claim of compliance with accessibility standards.
Full original inspected individually. No people, personal records, readable personal names, signatures or contact details are visible. Facility name on fascia is institutional. No crop needed.

### P30
`raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/BEDS IN STORAGE .jpg`; `None`; body block None; adjacent text: Loose photograph BEDS IN STORAGE .jpg under Kyabasara-HC-III/Kagadi. The source filename and visible stacking identify storage.
Loose photograph BEDS IN STORAGE .jpg under Kyabasara-HC-III/Kagadi. The source filename and visible stacking identify storage.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P31
`raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/boilogy lab under construction.jpg`; `None`; body block None; adjacent text: Loose photograph boilogy lab under construction.jpg under Kihungya-Seed-Secondary-School/Buliisa. kihungya seed school.docx body block 107 identifies the science block as not in use and under construction; block 63 states that most structures were not ready and there was no electricity for ICT sessions or water for sanitation.
Loose photograph boilogy lab under construction.jpg under Kihungya-Seed-Secondary-School/Buliisa. kihungya seed school.docx body block 107 identifies the science block as not in use and under construction; block 63 states that most structures were not ready and there was no electricity for ICT sessions or water for sanitation.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P32
`raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/butaiba submurged facility.jpeg`; `None`; body block None; adjacent text: Loose photograph butaiba submurged facility.jpeg under Butiaba-HC-III/Buliisa. The paired butaiba report.docx body block 11 (paragraph 10) explicitly states that the old facility built by UgIFT and its equipment were affected by floods.
Loose photograph butaiba submurged facility.jpeg under Butiaba-HC-III/Buliisa. The paired butaiba report.docx body block 11 (paragraph 10) explicitly states that the old facility built by UgIFT and its equipment were affected by floods.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P33
`raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Image 2026-09-12 at 13.47.23 (3).jpeg`; `None`; body block None; adjacent text: Loose photograph WhatsApp Image 2026-09-12 at 13.47.23 (3).jpeg under Bweema-Seed-Secondary-School/Buvuma. The same source photo collection includes a school sign identifying Bweema and Buvuma.
Loose photograph WhatsApp Image 2026-09-12 at 13.47.23 (3).jpeg under Bweema-Seed-Secondary-School/Buvuma. The same source photo collection includes a school sign identifying Bweema and Buvuma.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P34
`raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Image 2026-09-12 at 13.47.25.jpeg`; `None`; body block None; adjacent text: Loose photograph WhatsApp Image 2026-09-12 at 13.47.25.jpeg under Bweema-Seed-Secondary-School/Buvuma.
Loose photograph WhatsApp Image 2026-09-12 at 13.47.25.jpeg under Bweema-Seed-Secondary-School/Buvuma.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P35
`raw-data-grouped/team-15/Kween/Kaptum-Seed-Secondary-School/09_computer-lab-no-power-supply_ref0537.jpg`; `None`; body block None; adjacent text: Loose photograph 09_computer-lab-no-power-supply_ref0537.jpg under Kaptum-Seed-Secondary-School/Kween. The source filename identifies the computer laboratory and no power supply.
Loose photograph 09_computer-lab-no-power-supply_ref0537.jpg under Kaptum-Seed-Secondary-School/Kween. The source filename identifies the computer laboratory and no power supply.
Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

### P36
`raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/102_water-system-solar-panels-and-tanks_ref20260827-0369.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 102_water-system-solar-panels-and-tanks_ref20260827-0369.jpg.
Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 102_water-system-solar-panels-and-tanks_ref20260827-0369.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P37
`raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/108_patient-toilets_ref20260827-0367.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 108_patient-toilets_ref20260827-0367.jpg.
Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 108_patient-toilets_ref20260827-0367.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P38
`raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/10_engraving-weighing-scale_ref20260826-0429.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 10_engraving-weighing-scale_ref20260826-0429.jpg.
Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 10_engraving-weighing-scale_ref20260826-0429.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P39
`raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/37_engraving-delivery-bed_ref20260826-0456.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 37_engraving-delivery-bed_ref20260826-0456.jpg.
Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 37_engraving-delivery-bed_ref20260826-0456.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P40
`raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/40_oxygen-concentrator_ref20260826-0459.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 40_oxygen-concentrator_ref20260826-0459.jpg.
Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 40_oxygen-concentrator_ref20260826-0459.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P41
`raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/50_suction-apparatus_ref20260826-0469.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 50_suction-apparatus_ref20260826-0469.jpg.
Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 50_suction-apparatus_ref20260826-0469.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P42
`raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/69_wheelchair-marked-gou-moh-ugift_ref20260826-0488.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 69_wheelchair-marked-gou-moh-ugift_ref20260826-0488.jpg.
Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 69_wheelchair-marked-gou-moh-ugift_ref20260826-0488.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P43
`raw-data-grouped/team-10/Moroto/Katikekire-Seed-School/02_borehole-apron-and-pipework_ref20260826-0421.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Moroto / Katikekire-Seed-School; original filename: 02_borehole-apron-and-pipework_ref20260826-0421.jpg.
Loose field photograph filed under Moroto / Katikekire-Seed-School; original filename: 02_borehole-apron-and-pipework_ref20260826-0421.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P44
`raw-data-grouped/team-10/Moroto/Rupa-Seed-School/18_classroom-furniture-engraved-rupa-seed_ref20260909-photo-p08.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Moroto / Rupa-Seed-School; original filename: 18_classroom-furniture-engraved-rupa-seed_ref20260909-photo-p08.jpg.
Loose field photograph filed under Moroto / Rupa-Seed-School; original filename: 18_classroom-furniture-engraved-rupa-seed_ref20260909-photo-p08.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P45
`raw-data-grouped/team-10/Napak/Iriiri-Seed-Secondary-School/33_science-laboratory_ref20260827-0463.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Napak / Iriiri-Seed-Secondary-School; original filename: 33_science-laboratory_ref20260827-0463.jpg.
Loose field photograph filed under Napak / Iriiri-Seed-Secondary-School; original filename: 33_science-laboratory_ref20260827-0463.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P46
`raw-data-grouped/team-10/Napak/Lopei-Seed-Secondary-School/20_water-tanks_ref20260828-0562.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Napak / Lopei-Seed-Secondary-School; original filename: 20_water-tanks_ref20260828-0562.jpg.
Loose field photograph filed under Napak / Lopei-Seed-Secondary-School; original filename: 20_water-tanks_ref20260828-0562.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P47
`raw-data-grouped/team-11/Abim/Alerek-Seed-Secondary-School/23_water-tank-on-a-plinth-and-elevated-tank_ref0870.jpg`; `None`; body block None; adjacent text: 
Water storage infrastructure visibly present; no water delivery, potability or operational claim.
Full original inspected individually. No people, names, personal papers, phone numbers or signatures are visible. The only prominent lettering is a tank brand. No crop needed.

### P48
`raw-data-grouped/team-11/Abim/Alerek-Seed-Secondary-School/44_laboratory-chemicals-on-the-bench_ref0859.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Abim / Alerek-Seed-Secondary-School; original filename: 44_laboratory-chemicals-on-the-bench_ref0859.jpg.
Loose field photograph filed under Abim / Alerek-Seed-Secondary-School; original filename: 44_laboratory-chemicals-on-the-bench_ref0859.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P49
`raw-data-grouped/team-10/Moroto/Rupa-Seed-School/33_laboratory-store-shelving-with-chemicals-and-a-skeleton_ref20260909-photo-p23.jpg`; `None`; body block None; adjacent text: 
Teaching supplies visibly present in a school-provided photograph; no independent test or current-use claim.
Full original inspected individually. No people are present. Crop removes lower packing clutter, shipping label and camera watermark; retained chemical/container labels are product labels and carry no readable personal names or contact details. The anatomical model is a teaching skeleton, not a person.

### P50
`raw-data-grouped/team-11/Kaabong/Sidok-Seed-Secondary-School/16_classroom-block-under-construction_ref0316.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kaabong / Sidok-Seed-Secondary-School; original filename: 16_classroom-block-under-construction_ref0316.jpg.
Loose field photograph filed under Kaabong / Sidok-Seed-Secondary-School; original filename: 16_classroom-block-under-construction_ref0316.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P51
`raw-data-grouped/team-11/Kaabong/Sidok-Seed-Secondary-School/33_latrine-block-under-construction_ref0310.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kaabong / Sidok-Seed-Secondary-School; original filename: 33_latrine-block-under-construction_ref0310.jpg.
Loose field photograph filed under Kaabong / Sidok-Seed-Secondary-School; original filename: 33_latrine-block-under-construction_ref0310.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P52
`raw-data-grouped/team-11/Kotido/Kamoru-HC-III/15_oxygen-concentrator_ref1167.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kotido / Kamoru-HC-III; original filename: 15_oxygen-concentrator_ref1167.jpg.
Loose field photograph filed under Kotido / Kamoru-HC-III; original filename: 15_oxygen-concentrator_ref1167.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P53
`raw-data-grouped/team-11/Kotido/Kamoru-HC-III/18_engraved-table-top_ref1107.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kotido / Kamoru-HC-III; original filename: 18_engraved-table-top_ref1107.jpg.
Loose field photograph filed under Kotido / Kamoru-HC-III; original filename: 18_engraved-table-top_ref1107.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P54
`raw-data-grouped/team-11/Kotido/Rengen-Seed-School/10_water-tanks-x2_ref0642.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kotido / Rengen-Seed-School; original filename: 10_water-tanks-x2_ref0642.jpg.
Loose field photograph filed under Kotido / Rengen-Seed-School; original filename: 10_water-tanks-x2_ref0642.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P55
`raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/dust bins.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Buliisa / Butiaba-HC-III; original filename: dust bins.jpg.
Loose field photograph filed under Buliisa / Butiaba-HC-III; original filename: dust bins.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P56
`raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/IMG-20260907-WA0097.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Buliisa / Butiaba-HC-III; original filename: IMG-20260907-WA0097.jpg.
Loose field photograph filed under Buliisa / Butiaba-HC-III; original filename: IMG-20260907-WA0097.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P57
`raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/IMG-20260905-WA0028.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Buliisa / Kihungya-Seed-Secondary-School; original filename: IMG-20260905-WA0028.jpg.
Loose field photograph filed under Buliisa / Kihungya-Seed-Secondary-School; original filename: IMG-20260905-WA0028.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P58
`raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/library.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Buliisa / Kihungya-Seed-Secondary-School; original filename: library.jpg.
Loose field photograph filed under Buliisa / Kihungya-Seed-Secondary-School; original filename: library.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P59
`raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115519_265.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115519_265.jpg.
Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115519_265.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P60
`raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115826_769.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115826_769.jpg.
Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115826_769.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P61
`raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115836_836.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115836_836.jpg.
Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115836_836.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P62
`raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_120857_349.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_120857_349.jpg.
Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_120857_349.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P63
`raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_121503_686.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_121503_686.jpg.
Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_121503_686.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P64
`raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/IMG-20260908-WA0107.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: IMG-20260908-WA0107.jpg.
Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: IMG-20260908-WA0107.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P65
`raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/kangaro chair.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: kangaro chair.jpg.
Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: kangaro chair.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P66
`raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/power house.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: power house.jpg.
Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: power house.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P67
`raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Image 2026-09-12 at 13.47.22 (2).jpeg`; `None`; body block None; adjacent text: Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.22 (2).jpeg.
Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.22 (2).jpeg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P68
`raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Unknown 2026-09-12 at 13.58.16/WhatsApp Image 2026-09-12 at 13.47.17 (2).jpeg`; `None`; body block None; adjacent text: Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.17 (2).jpeg.
Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.17 (2).jpeg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P69
`raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Unknown 2026-09-12 at 13.58.16/WhatsApp Image 2026-09-12 at 13.47.20 (1).jpeg`; `None`; body block None; adjacent text: Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.20 (1).jpeg.
Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.20 (1).jpeg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P70
`raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`; `word/media/image27.jpeg`; body block 77; adjacent text: Kibiri HC III report: oxygen-cylinder photograph word/media/image27.jpeg in body block 77, within the facility pictorial record.
Kibiri HC III report: oxygen-cylinder photograph word/media/image27.jpeg in body block 77, within the facility pictorial record.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P71
`raw-data-grouped/team-32/Butambala/Budde-Seed-Secondary-School/BUDDE SEED SCHOOL (BUTAMABALA DISTRICT-BUDDE SEED).docx`; `word/media/image43.png`; body block 102; adjacent text: Budde Seed Secondary School return: PICTORIAL EVIDENCE, body block 102, table 8, word/media/image43.png. The visible mark identifies UGIFT and the school.
Budde Seed Secondary School return: PICTORIAL EVIDENCE, body block 102, table 8, word/media/image43.png. The visible mark identifies UGIFT and the school.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P72
`raw-data-grouped/team-13/Busia/Buwembe-HC-III/127_baby-weighing-scale-yrbb-20_ref20260828-0082.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Busia / Buwembe-HC-III; original filename: 127_baby-weighing-scale-yrbb-20_ref20260828-0082.jpg.
Loose field photograph filed under Busia / Buwembe-HC-III; original filename: 127_baby-weighing-scale-yrbb-20_ref20260828-0082.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P73
`raw-data-grouped/team-13/Busia/Buwembe-HC-III/136_autoclave-on-a-gas-cylinder_ref20260828-0091.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Busia / Buwembe-HC-III; original filename: 136_autoclave-on-a-gas-cylinder_ref20260828-0091.jpg.
Loose field photograph filed under Busia / Buwembe-HC-III; original filename: 136_autoclave-on-a-gas-cylinder_ref20260828-0091.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P74
`raw-data-grouped/team-14/Bulambuli/Sisiyi-Seed-Secondary-School/15_ict-laboratory-block_ref20260828-0015.jpg`; `None`; body block None; adjacent text: 
Block and ramp visibly present, with separately reported use; caption limited to observation.
Full original inspected individually. No people, personal records, signatures, contact details or readable personal names are visible. ICT LAB is an institutional room label. No crop needed.

### P75
`raw-data-grouped/team-13/Busia/Majanji-HC-III/042_pedal-suction-unit-in-its-packing_ref20260827-0637.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Busia / Majanji-HC-III; original filename: 042_pedal-suction-unit-in-its-packing_ref20260827-0637.jpg.
Loose field photograph filed under Busia / Majanji-HC-III; original filename: 042_pedal-suction-unit-in-its-packing_ref20260827-0637.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P76
`raw-data-grouped/team-14/Bulambuli/Bumufuni-Seed-Secondary-School/07_computer-sets-stacked-in-store_ref20260911-0011.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Bulambuli / Bumufuni-Seed-Secondary-School; original filename: 07_computer-sets-stacked-in-store_ref20260911-0011.jpg.
Loose field photograph filed under Bulambuli / Bumufuni-Seed-Secondary-School; original filename: 07_computer-sets-stacked-in-store_ref20260911-0011.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P77
`raw-data-grouped/team-14/Bulambuli/Bumugibole-HC-III/05_wheelchair-armrest-engraving_ref20260831-0202.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Bulambuli / Bumugibole-HC-III; original filename: 05_wheelchair-armrest-engraving_ref20260831-0202.jpg.
Loose field photograph filed under Bulambuli / Bumugibole-HC-III; original filename: 05_wheelchair-armrest-engraving_ref20260831-0202.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P78
`raw-data-grouped/team-14/Bulambuli/Bunangaka-HC-III/01_solar-batteries_ref20260830-0421.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Bulambuli / Bunangaka-HC-III; original filename: 01_solar-batteries_ref20260830-0421.jpg.
Loose field photograph filed under Bulambuli / Bunangaka-HC-III; original filename: 01_solar-batteries_ref20260830-0421.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P79
`raw-data-grouped/team-15/Kapchorwa/Kabeywa-Seed-Secondary-School/07_28computers_ref20260830-0271.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kapchorwa / Kabeywa-Seed-Secondary-School; original filename: 07_28computers_ref20260830-0271.jpg.
Loose field photograph filed under Kapchorwa / Kabeywa-Seed-Secondary-School; original filename: 07_28computers_ref20260830-0271.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P80
`raw-data-grouped/team-15/Kapchorwa/Kabeywa-Seed-Secondary-School/24_library_ref20260830-0842.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kapchorwa / Kabeywa-Seed-Secondary-School; original filename: 24_library_ref20260830-0842.jpg.
Loose field photograph filed under Kapchorwa / Kabeywa-Seed-Secondary-School; original filename: 24_library_ref20260830-0842.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P81
`raw-data-grouped/team-15/Kween/Atar-HC-III/07_autoclave-01_ref0458.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kween / Atar-HC-III; original filename: 07_autoclave-01_ref0458.jpg.
Loose field photograph filed under Kween / Atar-HC-III; original filename: 07_autoclave-01_ref0458.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P82
`raw-data-grouped/team-15/Kween/Atar-HC-III/21_solar-batteries_ref0444.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kween / Atar-HC-III; original filename: 21_solar-batteries_ref0444.jpg.
Loose field photograph filed under Kween / Atar-HC-III; original filename: 21_solar-batteries_ref0444.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P83
`raw-data-grouped/team-15/Kween/Atar-HC-III/36_kangaroo-mother-care-chair-1-not-engraved_ref20260830-0604.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kween / Atar-HC-III; original filename: 36_kangaroo-mother-care-chair-1-not-engraved_ref20260830-0604.jpg.
Loose field photograph filed under Kween / Atar-HC-III; original filename: 36_kangaroo-mother-care-chair-1-not-engraved_ref20260830-0604.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P84
`raw-data-grouped/team-15/Kween/Kitawoi-Seed-Secondary-School/09_ict-lab-under-construction_ref1386.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kween / Kitawoi-Seed-Secondary-School; original filename: 09_ict-lab-under-construction_ref1386.jpg.
Loose field photograph filed under Kween / Kitawoi-Seed-Secondary-School; original filename: 09_ict-lab-under-construction_ref1386.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P85
`raw-data-grouped/team-15/Kween/Moyok-HC-III/14_engraving-kwn-med-eq-moyok-hciii_ref0038.jpg`; `None`; body block None; adjacent text: Loose field photograph filed under Kween / Moyok-HC-III; original filename: 14_engraving-kwn-med-eq-moyok-hciii_ref0038.jpg.
Loose field photograph filed under Kween / Moyok-HC-III; original filename: 14_engraving-kwn-med-eq-moyok-hciii_ref0038.jpg.
Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.

### P86
`raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`; `word/media/image16.jpeg`; body block 77; adjacent text: 
Caption describes visible assets; practical use or benefit is supported separately by the cited field evidence.
Full original individually inspected. The selected crop has no identifiable people, readable personal names, signatures, contact details or personal records.

### P87
`raw-data-grouped/team-32/Butambala/Budde-Seed-Secondary-School/BUDDE SEED SCHOOL (BUTAMABALA DISTRICT-BUDDE SEED).docx`; `word/media/image42.png`; body block 102; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P88
`raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`; `word/media/image1.jpeg`; body block 77; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P89
`raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`; `word/media/image5.jpeg`; body block 19; adjacent text: 3. Desks | 3. Desks
Caption describes visible assets; practical use or benefit is supported separately by the cited field evidence.
Full original individually inspected. The selected crop has no identifiable people, readable personal names, signatures, contact details or personal records.

### P90
`raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`; `word/media/image10.jpeg`; body block 77; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P91
`raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`; `word/media/image12.jpeg`; body block 77; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P92
`raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx`; `word/media/image2.jpeg`; body block 78; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P93
`raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx`; `word/media/image4.jpeg`; body block 78; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P94
`raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx`; `word/media/image5.jpeg`; body block 78; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P95
`raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`; `word/media/image27.jpeg`; body block 95; adjacent text: 12. A | d | ministration block, staffrooms | , classrooms |  and multipurpose hall | 12. A | d | ministration block, staffrooms | , classrooms |  and multipurpose hall
Caption describes visible assets; practical use or benefit is supported separately by the cited field evidence.
Full original individually inspected. The selected crop has no identifiable people, readable personal names, signatures, contact details or personal records.

### P96
`raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`; `word/media/image15.jpeg`; body block 63; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P97
`raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`; `word/media/image17.jpeg`; body block 71; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P98
`raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`; `word/media/image18.jpeg`; body block 71; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P99
`raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Unknown 2026-09-12 at 13.58.16/WhatsApp Image 2026-09-12 at 13.47.13 (1).jpeg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P100
`raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/IMG-20260907-WA0094.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P101
`raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/office chairs.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P102
`raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/classroom block.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P103
`raw-data-grouped/team-25/Hoima City/Kihuukya-HC-III/IMG-20260908-WA0045.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P104
`raw-data-grouped/team-25/Hoima City/Kihuukya-HC-III/microscope.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P105
`raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115648_996.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P106
`raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_120333_732.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P107
`raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_121530_409.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P108
`raw-data-grouped/team-26/Kabarole/Iruhura-HC-III/KABAROLE DISTRICT   IRUHURA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222 (1).docx`; `word/media/image13.jpeg`; body block 105; adjacent text: Weighing scale with heighmeter & desk |       | Tank |                                 |                                                 Residentials 
Caption describes visible assets; practical use or benefit is supported separately by the cited field evidence.
Full original individually inspected. The selected crop has no identifiable people, readable personal names, signatures, contact details or personal records.

### P109
`raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/latrines.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P110
`raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/114_refrigerator-engraved-gou-moh-ugift-project_ref20260827-0359.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P111
`raw-data-grouped/team-10/Moroto/Rupa-Seed-School/17_water-tank-beside-a-staff-house_ref20260909-photo-p07.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P112
`raw-data-grouped/team-10/Napak/Iriiri-Seed-Secondary-School/30_ict-and-library-block_ref20260827-0466.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P113
`raw-data-grouped/team-10/Napak/Lopei-Seed-Secondary-School/08_ict-and-library-block_ref20260828-0570.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P114
`raw-data-grouped/team-11/Kotido/Kamoru-HC-III/07_instrument-trolley-with-a-delivery-set_ref1176.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P115
`raw-data-grouped/team-11/Kotido/Kamoru-HC-III/28_microscope-marked-kamoru-hc-iii_ref1144.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P116
`raw-data-grouped/team-12/Budaka/Kamonkoli-Seed-Secondary-School/50_anatomical-skeleton-on-laboratory-wall_ref0755.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P117
`raw-data-grouped/team-12/Budaka/Namusita-HC-III/024_microscope-binocular_ref0908.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P118
`raw-data-grouped/team-12/Budaka/Namusita-HC-III/039_infant-weighing-scales-x2_ref0887.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P119
`raw-data-grouped/team-12/Budaka/Nansanga-Seed-Secondary-School/035_laboratory-benches-stools-and-sink-run_ref0683.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P120
`raw-data-grouped/team-12/Budaka/Nansanga-Seed-Secondary-School/072_library-shelving-with-books_ref0729.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P121
`raw-data-grouped/team-12/Kibuku/Kabweri-HC-III/05_water-tank-on-steel-tower_ref1262.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.

### P122
`raw-data-grouped/team-12/Kibuku/Kabweri-HC-III/28_delivery-bed-with-side-rails_ref1303.jpg`; `None`; body block None; adjacent text: 
Visible asset or condition and facility location only; no operational status inferred.
Full original individually inspected. Composition crops remove peripheral people, forms or excessive empty areas where necessary. No identifiable faces, personal names, signatures, contact details or readable personal records remain.


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
- National MDA photographs: inspected programme All WIP documents and asset-distribution scans contain no attributable usable asset photograph meeting the privacy rules. 120 field photographs are used.
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
- `ARUA RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
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
- `BUTABIKA NRMH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `BUTALEJA BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 10: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 98: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 72: Eastern, Bukedi
- `BUTAMBALA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 46: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 229: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 2: Central, Buganda
- `BUTEBO BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 99: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 59: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 60: Eastern, Bukedi
- `BUVUMA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 65: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 3: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 4: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 5: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 6: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 7: Central, Buganda
- `BUYENDE BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 110: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 84: Eastern, Busoga
- `DOKOLO BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 186: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 187: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 176: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 177: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 178: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 179: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 180: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 181: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 182: Northern, Lango
- `ENTEBBE RH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `FORT PORTAL BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 59: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `FORT PORTAL CITY BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 328: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 329: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `FORT PORTAL RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `GOMBA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 66: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 8: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 9: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 10: Central, Buganda
- `GULU BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 26: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 175: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 149: Northern, Acholi
- `GULU RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `HOIMA BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 231: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 232: Western, Bunyoro
- `HOIMA CITY BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 231: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 232: Western, Bunyoro
- `HOIMA RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `IBANDA BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 39: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 217: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 242: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 243: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 244: Western, Ankole
- `IGANGA BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 111: Eastern, Busoga
- `ISINGIRO BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 218: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 245: Western, Ankole
- `JINJA BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 112: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 113: Eastern, Busoga
- `JINJA CITY BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 13: Eastern, Busoga
- `JINJA RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `KAABONG BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 20: Northern, Karamoja
- `KABALE BK`: Western / Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 242: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 304: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 305: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 306: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 307: Western, Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 308: Western, Kigezi
- `KABALE MC BK`: Western / Kigezi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 309: Western, Kigezi
- `KABALE RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
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
- `KAWEMPE RH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `KAYUNGA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 72: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 17: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 18: Central, Buganda
- `KAYUNGA RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `KAZO BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 40: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 246: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 247: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 248: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 249: Western, Ankole
- `KCCA BK`: National / National; REF workbook Read Me row13 central-government vote list; REF register remarks Facility type MDA
- `KIBAALE BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 236: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 237: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 300: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 301: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 302: Western, Bunyoro
- `KIBOGA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 2: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 73: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 19: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 20: Central, Buganda
- `KIBUKU BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 100: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 101: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 102: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 73: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 74: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 75: Eastern, Bukedi
- `KIIRA MC BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 359: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 360: Central, Buganda
- `KIKUUBE BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 51: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 238: Western, Bunyoro
- `KIRUDDU RH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
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
- `LIRA RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `LUUKA BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 119: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 120: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 94: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 95: Eastern, Busoga
- `LUWEERO BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 78: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 79: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 27: Central, Buganda
- `LWENGO BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 80: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 81: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 28: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 29: Central, Buganda
- `LYANTONDE BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 3: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 82: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 30: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 31: Central, Buganda
- `MAAIF BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MADI OKOLLO BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 211: Northern, West Nile
- `MAKINDYE SSABAGABO MC BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 51: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 357: Central, Buganda
- `MANAFWA BK`: Eastern / Bugisu; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 16: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 17: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 135: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 136: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 137: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 119: Eastern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 19, Region group
- `MARACHA BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 33: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 200: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 212: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 213: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 214: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 215: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 216: Northern, West Nile
- `MASAKA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 83: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 32: Central, Buganda
- `MASAKA CITY BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 83: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 32: Central, Buganda
- `MASAKA RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MASINDI BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 53: Western, Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 240: Western, Bunyoro
- `MASINDI MC BK`: Western / Bunyoro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 303: Western, Bunyoro
- `MAYUGE BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 121: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 122: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 96: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 97: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 98: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 99: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 100: Eastern, Busoga
- `MBALE BK`: Eastern / Bugisu; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 18: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 138: Eastern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 17, Region group
- `MBALE RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MBARARA BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 220: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 221: Western, Ankole
- `MBARARA CITY BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 220: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 221: Western, Ankole
- `MBARARA RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MGLSD BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MITOOMA BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 222: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 223: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 256: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 257: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 258: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 259: Western, Ankole
- `MITYANA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 84: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 34: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 35: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 36: Central, Buganda
- `MODV BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MOES BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MOFPED BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MOH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MOLG BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MOLHUD BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MOROTO BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 151: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 152: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 160: Northern, Karamoja
- `MOROTO RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MOWE BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MOWT BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MOYO BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 201: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 217: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 218: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 367: Northern, West Nile
- `MPIGI BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 85: Central, Buganda
- `MUBENDE BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 4: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 86: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 37: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 38: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 39: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 40: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 41: Central, Buganda
- `MUBENDE MC BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 42: Central, Buganda
- `MUBENDE RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `MUKONO BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 87: Central, Buganda
- `MUKONO MC BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 43: Central, Buganda
- `MULAGO NRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `NABILATUK BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 153: Northern, Karamoja
- `NAGURU RH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `NAKAPIRIPIRIT BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 21: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 154: Northern, Karamoja
- `NAKASEKE BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 5: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 88: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 89: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 44: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 45: Central, Buganda
- `NAKASONGOLA BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 90: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 46: Central, Buganda
- `NAMAYINGO BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 123: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 124: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 101: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 102: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 103: Eastern, Busoga
- `NAMISINDWA BK`: Eastern / Bugisu; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 19: Eastern, Elgon; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 139: Eastern, Elgon; raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx, table 2 row 18, Region group
- `NAMUTUMBA BK`: Eastern / Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 125: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 126: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 104: Eastern, Busoga; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 105: Eastern, Busoga
- `NANSANA MC BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 356: Central, Buganda
- `NAPAK BK`: Northern / Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 155: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 156: Northern, Karamoja; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 157: Northern, Karamoja
- `NEBBI BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 34: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 35: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 202: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 219: Northern, West Nile
- `NEMA BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `NGORA BK`: Eastern / Teso; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 167: Eastern, Teso
- `NTOROKO BK`: Western / Rwenzori and Tooro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 63: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 64: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 260: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 354: Western, Toro; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 355: Western, Toro; team-distributions.docx, table 1 rows 137 to 147: Rwenzori / Tooro
- `NTUNGAMO BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 43: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 44: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 224: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 260: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 261: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 262: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 263: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 264: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 265: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 266: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 267: Western, Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 268: Western, Ankole
- `NTUNGAMO MC BK`: Western / Ankole; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 269: Western, Ankole
- `NWOYA BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 36: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 203: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 220: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 221: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 222: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 223: Northern, West Nile; raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/WEMIS DISTRICT EQUIPMENT.rar :: WEMIS DISTRICT EQUIPMENT/RC1/ACHOLI/Nwoya/doc00036920260811110821.pdf, original archive hierarchy ACHOLI/Nwoya; enclosed three-page record identifies Nwoya District
- `OAG BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `OBONGI BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 204: Northern, West Nile
- `OMORO BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 205: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 224: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 225: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 226: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 368: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 369: Northern, West Nile; raw-data-grouped/team-05/Omoro/Abwoch-HC-III/Abwoch HC III_ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx, table 1 row 3: SUB-REGION ACHOLI
- `OPM BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `OTUKE BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 29: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 194: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 192: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 193: Northern, Lango
- `OYAM BK`: Northern / Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 30: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 195: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 194: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 195: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 196: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 197: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 198: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 199: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 200: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 201: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 202: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 203: Northern, Lango
- `PADER BK`: Northern / Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 179: Northern, Acholi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 196: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 204: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 205: Northern, Lango; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 206: Northern, Lango; raw-data-grouped/team-04/Pader/Lapul-Ocwida-HC-III/1 Lapulocwida HC - Pader District.docx, table 1 row 3: SUB-REGION ACHOLI
- `PAKWACH BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 206: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 207: Northern, West Nile
- `PALLISA BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 103: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 104: Eastern, Bukedi
- `PPDA BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
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
- `SOROTI RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `TEREGO BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 227: Northern, West Nile
- `TORORO BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 105: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 106: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 107: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 76: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 77: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 79: Eastern, Bukedi
- `TORORO MC BK`: Eastern / Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 11: Eastern, Bukedi; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 78: Eastern, Bukedi
- `UBTS BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
- `WAKISO BK`: Central / Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 94: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 52: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 53: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 54: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 55: Central, Buganda; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 358: Central, Buganda
- `YUMBE BK`: Northern / West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 37: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 38: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 1, row 208: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 228: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 229: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 230: Northern, West Nile; SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx table 2, row 231: Northern, West Nile
- `YUMBE RRH BK`: National / National; outputs/asset-register/README.md#book_type_code; MDA / Hospital / Blood bank status governs national presentation
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

## Revision evidence: narrative/revision_narrative.json

```json
{
  "executive_paragraphs": [
    "The verification found that UgIFT buildings and equipment were supporting local services, while unfinished works, power constraints, damage and delayed installation prevented some assets from serving their intended purpose. Health staff described improved access to maternity and antenatal care. Schools described better teaching facilities and wider access to secondary education. The main follow-up is to put unused assets into service and sustain those already working.",
    "The verification and reconciliation accounted for 629 master-list entries: 371 health centres and 258 schools. Outcomes included operating names, replacement facilities, relocated assets and sites not constructed. Section 7.1 explains how the institutions were accounted for.",
    "Construction and service readiness need attention together. Got Apwoyo Seed Secondary School in Nwoya had not been commissioned and its computer equipment remained at district headquarters. At Ndhew and Mamba seed schools in Nebbi, unfinished buildings delayed installation. At Atego in the same district, computers were already working in older rooms while construction continued.",
    "Power and repairs were immediate constraints. Lungulu Seed Secondary School in Nwoya held computers in storage pending a suitable power connection. Pamaka Health Centre III in Nebbi could not use oxygen equipment because of power constraints, and Busaale Health Centre III in Kayunga needed roof, door and solar repairs. Among assets recorded as out of use, 2,569 had damage, fault or repair remarks, while 483 were stored and described as good or new.",
    "Asset identification also needs follow-up. Of 225,133 asset entries, 50,211 carried markings, including 21,023 with UgIFT marking. The findings at Lungulu included unengraved assets. Districts should combine marking with decisions on custody and allocation, particularly where equipment has moved between facilities.",
    "The proposed priorities are to make unsafe items safe, restore essential equipment, complete works and utilities, and install usable stored assets. Facility managers should lead routine checks and minor repairs, supported by district engineers, health and education officers and the relevant technical teams. The action schedule proposes owners, timing and evidence that each action has been completed."
  ],
  "background_sections": [
    {
      "heading": "4.1 Introduction",
      "paragraphs": [
        "UgIFT invested in facilities and equipment to bring education and health services closer to communities and strengthen the institutions that support them. This verification examined where those assets were, how they were being used and what was needed to keep them working. The findings focus on facilities, equipment, custody, maintenance and the services available to the public."
      ],
      "source_note": "Client draft, paragraphs 10, 13 and 35 to 48"
    },
    {
      "heading": "4.2 Background to the verification",
      "paragraphs": [
        "The programme ended on 31 December 2025. The Ministry of Finance, Planning and Economic Development commissioned the verification to support closure and the continued use of programme assets. The exercise covered national institutions, government seed secondary schools and health facilities upgraded from Health Centre II to Health Centre III."
      ],
      "source_note": "Client draft, paragraph 13"
    },
    {
      "heading": "4.3 Justification",
      "paragraphs": [
        "Buildings and equipment need staff, utilities, maintenance and clear responsibility for their care. The verification provided a basis for handover and identified practical actions to bring unused assets into service, repair damaged items and protect assets already in use."
      ],
      "source_note": "Client draft, paragraphs 13, 35 to 41 and 43 to 49"
    },
    {
      "heading": "4.4 Objectives of the assignment",
      "paragraphs": [
        "The assignment was to identify and locate programme assets, check their condition and use, assess how institutions cared for them and recommend action where assets were damaged or unserviceable. It also prepared asset information for government reporting and the Integrated Financial Management Information System (IFMIS)."
      ],
      "source_note": "Client draft, paragraphs 35 to 41"
    },
    {
      "heading": "4.5 Scope of work",
      "paragraphs": [
        "Teams reviewed institutional asset information, inspected facilities and equipment, and spoke with the officers responsible for their use and care. The scope included buildings, furniture, medical equipment, computers, vehicles and motorcycles. Small office items such as staplers and punches and disposable school laboratory items were excluded from physical inspection."
      ],
      "source_note": "Client draft, paragraphs 43 to 49 and 161; Government of Uganda Asset Accounting Policies and Guidelines 2023, section 3.3.3, printed page 48, PDF page 60"
    },
    {
      "heading": "5.1 Preparation",
      "paragraphs": [
        "The entry meeting on 29 May 2026 agreed the scope, approach and work plan. A pilot at Buloba Health Centre III and Sumbwe Seed School in Wakiso District tested the tools and visit arrangements. Teams planned visits with Accounting Officers, district health and education officers, finance staff, head teachers and health centre in-charges."
      ],
      "source_note": "Client draft, paragraphs 95 to 109, 132 and 136 to 137"
    },
    {
      "heading": "5.2 What teams checked",
      "paragraphs": [
        "At each institution, the team checked the assets present, their location, identification markings, condition and use. Interviews covered repairs, servicing, breakdowns, storage, operating constraints and service benefits. Photographs documented selected assets and facilities."
      ],
      "source_note": "Client draft, paragraphs 111 to 129 and 134"
    },
    {
      "heading": "5.3 Fieldwork and itinerary",
      "paragraphs": [
        "National verification began on 24 July 2026 and included 10 working days of collection and repeat visits. Training for the local government teams took place on 20 and 21 August 2026. Local government fieldwork ran from 24 August to 7 September 2026, with 10 working days of collection.",
        "The Consultant deployed 33 teams of 2 to 3 people, comprising 80 research assistants, supported by 6 supervisors and a team leader, across 176 local governments. Teams first met the local government leadership, reviewed the planned investments, visited the facilities and discussed the findings with the responsible officers."
      ],
      "source_note": "Client draft, paragraphs 140 to 164; itinerary table 1, rows 2 to 7",
      "itinerary": [
        [
          "1",
          "Arrival and entry",
          "Register the visit at the Accounting Officer's office and hold the entry meeting with finance and administration."
        ],
        [
          "1",
          "Document review",
          "Review UgIFT documents and the asset register."
        ],
        [
          "2",
          "Physical verification",
          "Inspect identified assets in offices, health centres and schools."
        ],
        [
          "2",
          "Service interviews",
          "Discuss functionality, maintenance and sustainability with institution and facility management."
        ],
        [
          "2",
          "Follow up and debrief",
          "Complete follow up checks, debrief the responsible officers and finalise verification."
        ]
      ]
    },
    {
      "heading": "5.4 Quality assurance",
      "paragraphs": [
        "Regional supervisors checked daily field activity and reviewed the completed tools. The central technical team carried out spot checks and helped resolve operational questions. Teams compared institutional asset information with the items and explanations provided during visits, while supervisors referred matters requiring clarification to the team leader and field coordinator."
      ],
      "source_note": "Client draft, paragraphs 197 to 206"
    },
    {
      "heading": "5.5 Bringing the findings together",
      "paragraphs": [
        "The analysis brought the facility findings, interviews and asset counts together by region, institution and type of asset. Master-list names were reconciled with operating names, replacements and receiving facilities. Section 7.1 explains those outcomes, while the later sections examine use, condition, marking, maintenance and service delivery."
      ],
      "source_note": "Client draft, paragraphs 172 to 195"
    },
    {
      "heading": "5.6 Reading the asset measures",
      "paragraphs": [
        "Asset counts refer to individual entries, while facility counts refer to the master-list institutions and their reconciled identities. Health centre and school assets are grouped separately, with national institutional holdings shown under the responsible ministry or agency. Buildings, furniture, transport, computers and medical equipment are grouped by their purpose and location; maternity equipment is identified by its description or ward.",
        "The condition tables use the classifications assigned to the assets. The discussion of equipment in use, in storage or awaiting repair draws on the stated use and condition of each item and the facility findings. The detailed classification and accounting basis is given in the appendices."
      ],
      "source_note": "Government of Uganda Asset Accounting Policies and Guidelines 2023, sections 3.2.1, 3.3.3, 5.5 and 5.7 and Annex 1; REF register, Read Me rows 14, 40 to 43"
    },
    {
      "heading": "6.1 Programme background and design",
      "paragraphs": [
        "UgIFT began in financial year 2017/18 to improve the financing and delivery of local government services. Initial support focused on education and health. Later support extended the programme to water and environment and agricultural micro scale irrigation, including services for refugees and host communities."
      ],
      "source_note": "Client draft, paragraphs 52 and 54"
    },
    {
      "heading": "6.2 Programme components",
      "paragraphs": [
        "The programme supported a fairer system of grants to local governments, new secondary schools in underserved subcounties, and construction and upgrading of health facilities. School investments included classrooms, laboratories, administration blocks, sanitation and teachers' housing. Health investments included buildings, equipment, staff accommodation and sanitation.",
        "It also supported local government planning, budgeting, procurement and infrastructure management, together with performance assessment and technical support. National institutions received equipment and transport to support programme administration and oversight."
      ],
      "source_note": "Client draft, paragraphs 56 to 67 and 77 to 78"
    },
    {
      "heading": "6.3 Programme objectives",
      "paragraphs": [
        "The programme sought more adequate and predictable support, fairer allocation of resources and stronger oversight of local services. Its intended result was wider access to education, health, water and irrigation services and better management of the facilities and resources used to provide them."
      ],
      "source_note": "Client draft, paragraphs 86 to 91"
    },
    {
      "heading": "6.4 Delivery position at programme closure",
      "paragraphs": [
        "At closure, 196 of the 259 seed schools in the programme output account were complete and 189 were operational. The health output account showed 354 of 373 upgrades and new constructions complete. These closure figures show the delivery position before the later verification visits; section 7 describes the facilities and assets found during those visits."
      ],
      "source_ids": [
        "D01"
      ],
      "source_note": "Client draft, paragraphs 69 to 75",
      "table": [
        [
          "Education",
          "196 of 259 seed schools complete; 189 operational."
        ],
        [
          "Health",
          "354 of 373 health facility upgrades and new constructions complete."
        ],
        [
          "Water and environment",
          "758 piped water systems; 5,398 point water sources; 7,082 water supply systems rehabilitated; 325 designs completed; 256 sanitation facilities."
        ],
        [
          "Micro scale irrigation",
          "More than 6,235 irrigation systems installed, covering 4,843 hectares; 632 demonstration sites in 135 local governments."
        ],
        [
          "Refugee host services",
          "51 primary schools and 35 health facilities transitioned into local government services."
        ],
        [
          "Blood banks",
          "Arua and Hoima regional blood banks completed and commissioned; Soroti Regional Blood Bank rehabilitated."
        ]
      ]
    }
  ],
  "regional_findings": {
    "Central": {
      "paragraphs": [
        "Central region showed both service gains and repair needs. At Lukale Health Centre III in Buvuma, staff said the maternity ward enabled women to give birth locally instead of crossing water and gave them greater privacy. At Musiitwa Seed Secondary School in Kayunga, new facilities improved access to secondary education, and the irrigation system supported practical teaching and food production.",
        "Busaale Health Centre III in Kayunga used Primary Health Care funds for maintenance and reviewed asset condition quarterly. The maternity roof was leaking, door hinges needed repair and the solar system required a replacement battery. At Musiitwa, furniture and fittings were checked each term, but broken items remained out of use until the school could fund repairs.",
        "The immediate actions are to repair Busaale's roof, doors and solar system and clear the furniture repair backlog at Musiitwa. The school also reported attendance pressures linked to long walking distances and pupils' involvement in petty trade. School management and the district education office should address these alongside the physical improvements."
      ],
      "cases": [
        {
          "facility": "Busaale Health Centre III",
          "lg": "Kayunga",
          "finding": "The facility used Primary Health Care funds for maintenance and kept a quarterly condition record.",
          "gap": "The maternity roof leaked, door hinges were damaged and the solar battery needed replacement.",
          "action": "Cost and complete the roof, door and battery repairs, then confirm that the affected rooms and solar system are working.",
          "source_ids": [
            "O01",
            "O02",
            "O03"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Musiitwa Seed Secondary School",
          "lg": "Kayunga",
          "finding": "The school checked furniture and fittings each term and repaired them when funds allowed.",
          "gap": "Broken furniture remained out of use while funding was arranged.",
          "action": "Prepare a termly repair list and fund repairs in order of their effect on teaching and safety.",
          "source_ids": [
            "O04"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Musiitwa Seed Secondary School",
          "lg": "Kayunga",
          "finding": "The school improved access to secondary education and used irrigation equipment for teaching and food production.",
          "gap": "Long walking distances and pupils' engagement in petty trade affected attendance.",
          "action": "Maintain the practical teaching equipment and work with parents and the district education office on attendance barriers.",
          "source_ids": [
            "O05",
            "O06"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Lukale Health Centre III",
          "lg": "Buvuma",
          "finding": "Staff reported that the maternity ward allowed women to give birth locally and with greater privacy.",
          "gap": "Benefit to sustain.",
          "action": "Protect the service through routine care of the maternity building and equipment.",
          "source_ids": [
            "O27"
          ],
          "case_type": "benefit"
        }
      ],
      "sources": [
        "O01",
        "O02",
        "O03",
        "O04",
        "O05",
        "O06",
        "O27"
      ]
    },
    "Eastern": {
      "paragraphs": [
        "At Kagumba Health Centre III in Kamuli, staff linked the new maternity ward to increased use of delivery and antenatal services. The facility kept an asset condition book, but staff identified pressure on housing and a need for outpatient, laboratory, storage and kitchen space. These needs should be assessed against the services now provided at the facility.",
        "Repairs had returned broken furniture to use at Kagumba Seed Secondary School during the second term. In contrast, Sikuda Seed Secondary School in Busia had broken desks and a cracked laboratory stool that was still being used. At Bubago Health Centre in Kamuli, staff needed training to operate and maintain an oxygen concentrator.",
        "Equipment from Bumunji, Buwembe and Majanji health centres in Busia had been transferred to Masafu Hospital. The district should confirm the continuing service need at each location and keep responsibility for the transferred equipment clear. Repairing unsafe furniture and training the oxygen equipment users are immediate priorities."
      ],
      "cases": [
        {
          "facility": "Kagumba Health Centre III",
          "lg": "Kamuli",
          "finding": "Staff reported increased maternity and antenatal service use, and the facility kept an asset condition book.",
          "gap": "Staff housing was under pressure; outpatient, laboratory, storage and kitchen space were identified as needs.",
          "action": "Assess the supporting space against patient demand and include the agreed works in the district health investment plan.",
          "source_ids": [
            "O07",
            "O08",
            "O09"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Kagumba Seed Secondary School",
          "lg": "Kamuli",
          "finding": "The school reported that broken furniture had been repaired during the second term.",
          "gap": "Practice to sustain.",
          "action": "Continue condition checks and scheduled furniture repairs before each term.",
          "source_ids": [
            "O28"
          ],
          "case_type": "practice"
        },
        {
          "facility": "Sikuda Seed Secondary School",
          "lg": "Busia",
          "finding": "Broken desks and a cracked laboratory stool were found.",
          "gap": "The cracked stool was still in use.",
          "action": "Withdraw unsafe furniture from use and repair or replace it before returning it to classrooms or laboratories.",
          "source_ids": [
            "O11"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Bubago Health Centre",
          "lg": "Kamuli",
          "finding": "Staff identified difficulty operating and maintaining an oxygen concentrator.",
          "gap": "Equipment use depended on stronger user and basic maintenance skills.",
          "action": "Arrange practical user training and a technical check, then demonstrate operation with the staff responsible for the equipment.",
          "source_ids": [
            "O29"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Bumunji, Buwembe and Majanji health centres; Masafu Hospital",
          "lg": "Busia",
          "finding": "Equipment had been transferred from the health centres to Masafu Hospital.",
          "gap": "Allocation and custody require confirmation.",
          "action": "Confirm the receiving custodian, location and service need, and retain signed transfer and receipt documentation.",
          "source_ids": [
            "O10"
          ],
          "case_type": "custody"
        }
      ],
      "sources": [
        "O07",
        "O08",
        "O09",
        "O10",
        "O11",
        "O28",
        "O29"
      ]
    },
    "Northern": {
      "paragraphs": [
        "Unfinished construction delayed the use of delivered equipment at several schools. Got Apwoyo Seed Secondary School in Nwoya had not been commissioned; furniture was on site and computer equipment remained at district headquarters. At Ndhew and Mamba Seed Schools in Nebbi, unfinished buildings also delayed installation, with science equipment held at district headquarters. Mamba was using older structures to accommodate its computers.",
        "Conditions differed within Nebbi. Atego Seed School was still under construction, but its computers were connected and working in older rooms. Staff reported power surges. This calls for completion of the planned facilities and a stable electricity supply while protecting the equipment already in use.",
        "Power also restricted use of completed facilities. Lungulu Seed Secondary School in Nwoya kept computers and related equipment in storage pending a suitable power connection; the stored equipment included defective desktop units requiring separate attention. At Pamaka Health Centre III in Nebbi, a nonfunctional solar system and power constraints prevented use of oxygen equipment. Rupa Seed School in Moroto hired a generator for practical lessons and used the library and computer laboratory block as dormitories.",
        "Some equipment had yet to be brought into use. Neonatal respiratory equipment at Kalemungole Health Centre III in Moroto remained in an unopened carton and treatment trolleys were still wrapped. Equipment intended for Todora Health Centre III in Nwoya had been sent to Paraa during construction and had not all been transferred back. Each case needs a clear decision on installation, allocation and custody.",
        "Todora referred major medical equipment repairs through the District Health Officer to the Gulu Regional Referral Hospital technical team. Lungulu funded minor repairs from school revenue and sought district technical support. Its assets also required engraving. At Pamaka, staff reported greater community confidence and patient attendance, alongside pressure on staffing."
      ],
      "cases": [
        {
          "facility": "Got Apwoyo Seed Secondary School",
          "lg": "Nwoya",
          "finding": "The school was under construction and had not been commissioned. Delivered furniture was on site and computer equipment was held at district headquarters.",
          "gap": "Incomplete buildings prevented commissioning and installation.",
          "action": "Agree a costed completion and handover plan, then move and install the equipment when the rooms and utilities are ready.",
          "source_ids": [
            "O30"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Ndhew Seed School",
          "lg": "Nebbi",
          "finding": "Buildings were incomplete, with computer and science equipment held at district headquarters and furniture not yet installed.",
          "gap": "Delivery of equipment had not translated into an equipped school.",
          "action": "Complete the outstanding works and sanitation facilities and coordinate furniture and equipment installation with handover.",
          "source_ids": [
            "O31"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Mamba Seed School",
          "lg": "Nebbi",
          "finding": "Construction was incomplete. Computers were temporarily accommodated in older structures, while science equipment remained at district headquarters.",
          "gap": "The planned laboratory and computer spaces were not ready for full installation.",
          "action": "Complete and commission the buildings, install the equipment and confirm safe operation before formal handover.",
          "source_ids": [
            "O32"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Atego Seed School",
          "lg": "Nebbi",
          "finding": "Computers were connected and working in older rooms while construction continued.",
          "gap": "Staff reported power surges and the planned facilities were not fully commissioned.",
          "action": "Stabilise the power supply, protect the installed computers and finish the remaining works.",
          "source_ids": [
            "O33"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Lungulu Seed Secondary School",
          "lg": "Nwoya",
          "finding": "The school funded minor repairs and kept breakdown information, but computers remained in storage pending power.",
          "gap": "The stored equipment included defective desktop units, and the assets were not engraved.",
          "action": "Provide a suitable power connection, repair defective units, install the usable equipment and apply asset identification markings.",
          "source_ids": [
            "O12",
            "O13",
            "O34"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Todora and Paraa Health Centres III",
          "lg": "Nwoya",
          "finding": "Todora used the regional technical maintenance team, while some equipment originally intended for Todora remained at Paraa after redirection during construction.",
          "gap": "Equipment location and final allocation required a district decision.",
          "action": "Confirm the service need at both facilities, formally allocate or transfer the equipment and update the named custodians.",
          "source_ids": [
            "O14",
            "O15"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Pamaka Health Centre III",
          "lg": "Nebbi",
          "finding": "Staff reported increased attendance and community confidence.",
          "gap": "The solar system was not working, oxygen equipment could not be used because of power constraints, and staffing was under pressure.",
          "action": "Restore reliable power and demonstrate oxygen equipment operation; review staffing against patient demand.",
          "source_ids": [
            "O16",
            "O17"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Kalemungole Health Centre III",
          "lg": "Moroto",
          "finding": "Neonatal respiratory equipment remained in an unopened carton and treatment trolleys were still wrapped.",
          "gap": "Delivered items had not been brought into routine use.",
          "action": "Check the equipment, confirm the room and staff requirements, and arrange installation and user orientation.",
          "source_ids": [
            "O18"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Rupa Seed School",
          "lg": "Moroto",
          "finding": "The school hired a generator for practical lessons and used its library and computer laboratory block as dormitories.",
          "gap": "The intended learning spaces and a permanent power connection were unavailable for their planned use.",
          "action": "Agree a room-use plan and power solution that restores the library and computer laboratory functions.",
          "source_ids": [
            "O19"
          ],
          "case_type": "gap"
        }
      ],
      "sources": [
        "O12",
        "O13",
        "O14",
        "O15",
        "O16",
        "O17",
        "O18",
        "O19",
        "O30",
        "O31",
        "O32",
        "O33",
        "O34"
      ]
    },
    "Western": {
      "paragraphs": [
        "Repair needs affected buildings as well as equipment. At Nyamarunda Health Centre III in Kibaale, staff raised concerns about staff-quarter workmanship, electrical installation, drainage, water security and storage space. The facility recorded broken items, set them aside and referred them to the District Health Officer. A technical inspection should establish the repairs needed and their order of priority.",
        "Avogera Health Centre III in Buliisa carried out some repairs locally and received support from Hoima Regional Referral Hospital. Items that could not be repaired remained in storage, and staff identified a need for technical skills, user orientation and more storage space. Kyankaramata Health Centre III in Kyenjojo funded minor repairs from Primary Health Care funds, but the cost of major repairs was a constraint.",
        "There were practical maintenance arrangements to continue. Ngwedo Seed Secondary School in Buliisa engaged a caretaker monthly and used the Directorate of Industrial Training for furniture repairs. Bundimulangya Health Centre III in Bundibugyo referred maintenance needs to the District Health Officer, who sent a team; staff said the power house and solar installation supported continued operation.",
        "Butungama Seed School in Ntoroko remained under construction. At Kigorobya Seed Secondary School in Hoima, classrooms, the computer room and chemistry laboratory supported teaching, while staffing and study materials remained constraints. These findings call for completion of outstanding works and operating support alongside the assets already supplied."
      ],
      "cases": [
        {
          "facility": "Nyamarunda Health Centre III",
          "lg": "Kibaale",
          "finding": "The facility identified and set aside broken items and referred them to the District Health Officer.",
          "gap": "Staff raised concerns about staff-quarter workmanship, electrical installation, drainage, water security and storage.",
          "action": "Carry out a joint engineering and health inspection, make unsafe installations safe and complete the agreed repairs.",
          "source_ids": [
            "O20",
            "O21"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Avogera Health Centre III",
          "lg": "Buliisa",
          "finding": "The facility carried out local repairs and received technical support from Hoima Regional Referral Hospital.",
          "gap": "Items that could not be repaired remained stored; staff identified technical skills, user orientation and storage needs.",
          "action": "Assess the stored items for repair, give practical user training and agree a suitable storage arrangement.",
          "source_ids": [
            "O22"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Ngwedo Seed Secondary School",
          "lg": "Buliisa",
          "finding": "A caretaker attended monthly for repairs, and the Directorate of Industrial Training repaired furniture.",
          "gap": "Practice to sustain.",
          "action": "Continue the repair schedule and record the items returned to use.",
          "source_ids": [
            "O23"
          ],
          "case_type": "practice"
        },
        {
          "facility": "Bundimulangya Health Centre III",
          "lg": "Bundibugyo",
          "finding": "The District Health Officer arranged maintenance support, and staff said the power house and solar installation supported continued operation.",
          "gap": "Practice to sustain.",
          "action": "Keep the technical referral arrangement active and include the power and solar systems in routine servicing.",
          "source_ids": [
            "O24"
          ],
          "case_type": "practice"
        },
        {
          "facility": "Kyankaramata Health Centre III",
          "lg": "Kyenjojo",
          "finding": "Primary Health Care funds paid for minor repairs.",
          "gap": "Major repair costs were a constraint.",
          "action": "Prepare costed technical referrals for major repairs and agree district funding and follow-up.",
          "source_ids": [
            "O25"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Kigorobya Seed Secondary School",
          "lg": "Hoima",
          "finding": "Equipped classrooms, the computer room and chemistry laboratory supported teaching; the school and ministry shared maintenance work.",
          "gap": "Staffing and study materials constrained use of the improved facilities.",
          "action": "Review teaching staff and materials alongside the maintenance plan.",
          "source_ids": [
            "O26"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Butungama Seed School",
          "lg": "Ntoroko",
          "finding": "The school was still under construction at the time of the interview.",
          "gap": "The construction works required completion.",
          "action": "Confirm the outstanding works with the district engineer and agree the completion and handover sequence.",
          "source_ids": [
            "O35"
          ],
          "case_type": "gap"
        },
        {
          "facility": "Butiaba Health Centre III",
          "lg": "Buliisa",
          "finding": "The hydraulic delivery bed was not in use because staff needed operating guidance. Staff also reported difficulty obtaining test strips for the supplied glucometers.",
          "gap": "Equipment use depended on practical training and access to compatible consumables.",
          "action": "Demonstrate safe operation of the delivery bed with its users and arrange a reliable supply of compatible glucometer strips.",
          "source_ids": [
            "O36"
          ],
          "case_type": "gap"
        }
      ],
      "sources": [
        "O20",
        "O21",
        "O22",
        "O23",
        "O24",
        "O25",
        "O26",
        "O35",
        "O36"
      ]
    }
  },
  "national_findings": {
    "heading": "7.2 National institutions",
    "paragraphs": [
      "National support provided computers, office equipment, furniture and transport for programme administration and oversight. National institutions, hospitals and blood banks held 15,793 recorded assets. The practical follow-up is to keep usable equipment assigned, serviced and marked, and decide what to do with damaged items.",
      "The Ministry of Works and Transport identified an established servicing arrangement for its Toyota Hilux pickup: the Ministry of Finance, Planning and Economic Development undertook repairs and servicing. The Office of the Prime Minister identified damaged laptops that were no longer in use. Those laptops require technical assessment and a decision on repair, replacement or disposal.",
      "At national level, 4,969 items carried identification markings, including 4,805 with UgIFT marking. Institutions should confirm that markings remain readable and linked to the office or officer responsible for each asset."
    ],
    "cases": [
      {
        "facility": "Ministry of Works and Transport",
        "lg": "National",
        "finding": "The Ministry of Finance, Planning and Economic Development undertook repairs and servicing of the Toyota Hilux pickup.",
        "gap": "",
        "action": "Continue scheduled servicing and retain the service history with the vehicle.",
        "source_ids": [
          "N01"
        ],
        "case_type": "practice"
      },
      {
        "facility": "Office of the Prime Minister",
        "lg": "National",
        "finding": "Damaged laptops were identified as no longer in use.",
        "gap": "The laptops were not supporting office work.",
        "action": "Obtain a technical assessment and decide which items to repair and which to process for replacement or disposal.",
        "source_ids": [
          "N02"
        ],
        "case_type": "gap"
      }
    ],
    "source_ids": [
      "N01",
      "N02",
      "Q01"
    ],
    "per_institution_body_template": "{institution} held {count} programme assets, including {supported_asset_types}. {specific_use_or_condition_finding_if_explicitly_supported} {specific_maintenance_finding_if_supported} {engraving_count_sentence} {specific_action_if_supported}",
    "author_note": "Optional sentences must not be filled from acquisition warranty or a generic Functional classification. Leave them out where no specific observation exists. Procurement warranty periods do not demonstrate current cover or servicing."
  },
  "thematic_sections": [
    {
      "heading": "7.4 Condition and use of assets",
      "subsections": [
        {
          "heading": "7.4.1 Equipment in use and items awaiting action",
          "paragraphs": [
            "The visits showed why availability, condition and use need to be considered together. At Lungulu Seed Secondary School, a power connection was needed before stored computers could be installed. At Kalemungole Health Centre III, equipment remained boxed or wrapped. At Sikuda Seed Secondary School, a damaged stool was still being used.",
            "Among assets recorded as out of use, 2,569 had damage, fault or repair remarks, while 483 were stored and described as good or new. These groups require different action: damaged items need technical assessment, while usable stored items need the conditions for safe installation and use."
          ],
          "source_ids": [
            "O11",
            "O13",
            "O18",
            "Q01"
          ]
        },
        {
          "heading": "7.4.2 Complete the setting in which equipment will work",
          "paragraphs": [
            "At Got Apwoyo, Ndhew and Mamba seed schools, unfinished buildings delayed the use or installation of equipment. At Rupa Seed School, the library and computer laboratory block had been put to another use. Completion plans should bring buildings, electricity, furniture, equipment and staffing together so that handover leads to an operating service.",
            "At Atego Seed School, equipment was already working in older rooms while construction continued. Completion should protect this use while the planned facilities are finished and the power supply is stabilised."
          ],
          "source_ids": [
            "O19",
            "O30",
            "O31",
            "O32",
            "O33"
          ]
        }
      ]
    },
    {
      "heading": "7.5 Asset management practices, gaps and actions",
      "subsections": [
        {
          "heading": "7.5.1 Identification and custody",
          "paragraphs": [
            "Across the programme, 50,211 assets carried identification markings, representing 22.3% of the 225,133 entries. Of these, 21,023 had UgIFT marking and 29,188 had other markings. Lungulu Seed Secondary School provided a specific example of assets requiring engraving.",
            "Marking should identify the asset and the institution responsible for it. Where assets have moved, custody needs to move with them: equipment from three Busia health centres had gone to Masafu Hospital, while equipment intended for Todora in Nwoya had gone to Paraa during construction. The district should confirm the continuing allocation and retain signed handover or transfer documentation."
          ],
          "source_ids": [
            "Q01",
            "O10",
            "O15",
            "O34"
          ]
        },
        {
          "heading": "7.5.2 Maintenance and repairs",
          "paragraphs": [
            "Facilities used several practical arrangements. Busaale Health Centre III reviewed condition quarterly and used Primary Health Care funds for repairs. Kagumba Health Centre III kept a condition book, and Kagumba Seed Secondary School had repaired broken furniture during the second term. Ngwedo Seed Secondary School used a monthly caretaker visit and specialist furniture repair support.",
            "Major medical equipment repairs depended on technical support beyond the facility. Todora worked through the District Health Officer and Gulu Regional Referral Hospital; Avogera received support from Hoima Regional Referral Hospital; Bundimulangya obtained a team through the District Health Officer. At Kyankaramata, the cost of major repairs constrained what the facility could do.",
            "Each facility should keep a short list of items requiring action, the responsible person and the agreed completion date. District health and education offices should review unresolved repairs and arrange technical assistance. Completion should mean that the item has been checked and returned to safe use, or formally assigned another outcome."
          ],
          "source_ids": [
            "O01",
            "O02",
            "O07",
            "O14",
            "O22",
            "O23",
            "O24",
            "O25",
            "O28"
          ]
        },
        {
          "heading": "7.5.3 Storage, installation and user skills",
          "paragraphs": [
            "Stored equipment needs a plan for use. Lungulu needed power, Got Apwoyo needed completed buildings, and Avogera needed repair support for items it could not restore locally. Kalemungole had unopened and wrapped equipment requiring a check of readiness for installation and use.",
            "Training should accompany installation. Bubago Health Centre identified limited capacity to operate and maintain an oxygen concentrator, while Avogera asked for user orientation and technical skills. Equipment should be handed over with a practical demonstration to the staff who will use it and a clear route for technical support."
          ],
          "source_ids": [
            "O13",
            "O18",
            "O22",
            "O29",
            "O30"
          ]
        },
        {
          "heading": "7.5.4 Priorities for follow-up",
          "paragraphs": [
            "The first priority is to make unsafe items and installations safe and restore equipment needed for care and teaching. The next is to complete works, provide utilities and install assets that can then be used. Marking, custody checks and routine servicing should form part of the same follow-up, with responsibility assigned to the institution and its supervising office.",
            "Future delivery plans should confirm the room, power, water, storage and staff requirements before equipment arrives. Facility managers should take part in that planning, as recommended at Kyankaramata and Avogera. The action schedule sets out proposed owners, timing and evidence of completion."
          ],
          "source_ids": [
            "O03",
            "O11",
            "O13",
            "O16",
            "O21",
            "O22",
            "O25",
            "O29",
            "O30"
          ]
        }
      ]
    },
    {
      "heading": "7.6 UgIFT support to service delivery",
      "subsections": [
        {
          "heading": "7.6.1 Benefits described by facilities",
          "paragraphs": [
            "Staff at Lukale Health Centre III in Buvuma said women could give birth locally instead of crossing water and had greater privacy. Kagumba Health Centre III in Kamuli reported greater use of maternity and antenatal services. At Pamaka Health Centre III in Nebbi, staff described increased attendance and community confidence.",
            "Schools also described practical gains. Musiitwa Seed Secondary School used the irrigation system for teaching and food production and provided secondary education closer to surrounding communities. Kigorobya Seed Secondary School used its classrooms, computer room and chemistry laboratory to support teaching."
          ],
          "source_ids": [
            "O05",
            "O06",
            "O08",
            "O17",
            "O26",
            "O27"
          ]
        },
        {
          "heading": "7.6.2 Constraints to the intended service",
          "paragraphs": [
            "Equipment could not deliver its intended benefit where buildings, utilities or user skills were not ready. Power restricted oxygen equipment at Pamaka and computer installation at Lungulu. At Rupa, teaching spaces served as dormitories and practical lessons depended on a hired generator.",
            "Demand also brought pressure on staff and space. Kagumba identified needs for staff housing and supporting clinical facilities. Pamaka reported staffing pressure, and Kigorobya identified teaching staff and study-material constraints. Musiitwa's attendance concerns required attention alongside investment in buildings and equipment."
          ],
          "source_ids": [
            "O05",
            "O09",
            "O13",
            "O16",
            "O17",
            "O19",
            "O26"
          ]
        },
        {
          "heading": "7.6.3 Actions to sustain the benefits",
          "paragraphs": [
            "Districts and sector ministries should direct the first round of follow-up to actions that restore or expand a service using assets already supplied. These include reliable electricity, completion of classrooms and laboratories, repair of maternity buildings, practical equipment training and return of damaged furniture to safe use.",
            "Facility managers should report progress in terms of use: rooms opened, equipment installed and demonstrated, repairs completed and staff able to operate the equipment. Future investment should provide for staffing, operating funds and maintenance alongside buildings and equipment."
          ],
          "source_ids": [
            "O03",
            "O11",
            "O13",
            "O16",
            "O22",
            "O25",
            "O29",
            "O30",
            "O31",
            "O32"
          ]
        }
      ]
    }
  ],
  "recommendations_intro": "The following owners and times are proposed for follow-up after report approval. They are recommendations, rather than commitments already made by the institutions.",
  "recommendations": [
    {
      "priority": "1. Immediate safety and essential service",
      "action": "Withdraw damaged furniture that presents a safety concern, inspect the electrical concerns at Nyamarunda, and assess the failed solar and oxygen equipment arrangements at Pamaka.",
      "owner": "Facility managers, district health and education officers, district engineers and regional medical equipment technical teams",
      "timing": "Proposed: inspect within 30 days of report approval; complete minor corrective work within 60 days.",
      "completion_evidence": "Unsafe items withdrawn; signed technical assessment; repair record and demonstration of safe operation.",
      "source_ids": [
        "O11",
        "O16",
        "O21"
      ]
    },
    {
      "priority": "2. Complete and commission facilities",
      "action": "Agree completion plans for Got Apwoyo, Ndhew, Mamba and Butungama seed schools. Coordinate the remaining works, utilities, furniture and equipment installation; protect ongoing equipment use at Atego.",
      "owner": "District Accounting Officers, district engineers, district education officers, contractors and Ministry of Education and Sports",
      "timing": "Proposed: agree site-specific completion plans within 30 days; track progress monthly against the approved dates.",
      "completion_evidence": "Outstanding-works schedule; approved completion dates; inspection and handover documents; classrooms or laboratories opened for their intended use.",
      "source_ids": [
        "O30",
        "O31",
        "O32",
        "O33",
        "O35"
      ]
    },
    {
      "priority": "3. Bring stored equipment into use",
      "action": "Provide the power required at Lungulu, assess and install the boxed equipment at Kalemungole, and assess the repair needs of stored items at Avogera. Keep damaged and usable stored items on separate action lists.",
      "owner": "District health and education officers, facility managers, electrical contractors and regional technical teams",
      "timing": "Proposed: confirm readiness and actions within 30 days; complete installation within 90 days where rooms and utilities are ready.",
      "completion_evidence": "Equipment location check; power and installation sign-off; named custodian; practical demonstration and date first used.",
      "source_ids": [
        "O13",
        "O18",
        "O22",
        "O34"
      ]
    },
    {
      "priority": "4. Clear priority repairs",
      "action": "Repair the roof, doors and solar system at Busaale, arrange the major repair support needed at Kyankaramata and assess damaged laptops at the Office of the Prime Minister.",
      "owner": "Facility managers, district health officers, district engineers and the responsible national institution asset managers",
      "timing": "Proposed: agree priority work within 30 days and complete funded repairs within 90 days.",
      "completion_evidence": "Approved repair list; work orders; repairs checked and assets returned to use or assigned a formal disposal decision.",
      "source_ids": [
        "O03",
        "O25",
        "N02"
      ]
    },
    {
      "priority": "5. Strengthen user skills",
      "action": "Provide practical operation and basic maintenance training for oxygen equipment users at Bubago and the staff requiring equipment orientation at Avogera.",
      "owner": "District health officers, facility in-charges, suppliers and regional medical equipment technical teams",
      "timing": "Proposed: complete initial training within 60 days and review use after a further 30 days.",
      "completion_evidence": "Training attendance by role; practical demonstration of equipment use; named technical support contact.",
      "source_ids": [
        "O22",
        "O29"
      ]
    },
    {
      "priority": "6. Mark assets and confirm custody",
      "action": "Mark eligible unengraved assets, starting with the identified Lungulu holdings, and confirm the final allocation of transferred equipment at Todora, Paraa and Masafu.",
      "owner": "Institution asset managers, facility managers and district finance, health and education offices",
      "timing": "Proposed: confirm allocation within 30 days and complete priority marking and custody checks within 90 days.",
      "completion_evidence": "Readable identification; item-to-custodian match; signed transfer or receipt and agreed final location.",
      "source_ids": [
        "O10",
        "O15",
        "O34",
        "Q01"
      ]
    },
    {
      "priority": "7. Fund routine maintenance",
      "action": "Retain the functioning local and regional repair arrangements and prepare annual maintenance plans that separate minor repairs from specialist work. Review unresolved faults each quarter.",
      "owner": "Facility managers, school governing bodies, district health and education officers and national institution Accounting Officers",
      "timing": "Proposed: prepare plans within 90 days, include costs in the next budget cycle and review quarterly.",
      "completion_evidence": "Funded maintenance plan; fault list with responsible roles and due dates; service history and closed repair actions.",
      "source_ids": [
        "O01",
        "O02",
        "O04",
        "O07",
        "O12",
        "O14",
        "O20",
        "O23",
        "O24",
        "O25",
        "O28",
        "N01"
      ]
    },
    {
      "priority": "8. Match service capacity to demand",
      "action": "Review supporting clinical space and staffing at Kagumba and Pamaka, teaching staff and materials at Kigorobya, and attendance barriers at Musiitwa. Include operating needs in future asset planning.",
      "owner": "District health and education officers, facility managers and the relevant sector ministries",
      "timing": "Proposed: complete service-needs reviews within 90 days and include agreed measures in the next planning and budget cycle.",
      "completion_evidence": "Agreed staffing and space priorities; service or teaching plan; funded actions and periodic review of use.",
      "source_ids": [
        "O05",
        "O08",
        "O09",
        "O17",
        "O26",
        "O27"
      ]
    }
  ],
  "appendix_moves": [
    {
      "content": "Detailed valuation and depreciation methodology from former section 5.6",
      "destination": "Appendix: classification and accounting basis",
      "reason": "Retains actual comparator, useful-life, date and zero-floor rules without making accounting mechanics the field narrative."
    },
    {
      "content": "Regional value and net book value chart and schedules",
      "destination": "Appendix: recorded value schedules",
      "reason": "All monetary figures belong outside executive and main findings."
    },
    {
      "content": "National ministry value rankings, depreciation and net book value tables",
      "destination": "Appendix: national institutional schedules",
      "reason": "Main national prose describes assets and supported use, repair and custody findings."
    },
    {
      "content": "Per-category and per-region financial columns",
      "destination": "Detailed appendix tables",
      "reason": "Main regional tables focus on facility coverage, asset types, use and priority action."
    },
    {
      "content": "Detailed Functional/Faulty definitions, including default Functional and storage/non-use cases",
      "destination": "Appendix: interpretation of condition and use measures",
      "reason": "Classification is not a physical functioning rate. Never call 94.0% a physical test pass rate."
    },
    {
      "content": "Procurement warranty examples",
      "destination": "Appendix only where useful",
      "reason": "Acquisition terms do not establish current warranty cover or maintenance."
    },
    {
      "content": "Programme financing amounts and credit/grant split",
      "destination": "Appendix if retained",
      "reason": "No monetary figures in executive, background or main findings."
    }
  ],
  "editorial_instructions": [
    "Only prose, tables and case/action fields are report content. Keep source_index, source_ids, source_note, author_note and these instructions in private evidence material.",
    "Do not print source filenames, paths, extraction locations or source IDs anywhere in the report, including appendices, captions and source lines. Keep precise provenance in JSON and sources.md.",
    "Preserve the agreed section order and all required national institutions. Optional per-institution sentences must be omitted when no supported specific observation exists.",
    "Case IDs O01 through O29 are all retained. O30 through O35 add specific construction and engraving evidence.",
    "Positive practice and benefit cases have an empty gap. Do not manufacture a defect to fill a table column.",
    "The counts 2,569 and 483 describe items recorded as out of use. The underlying account contains default Functional classifications, so neither 211,613 nor 94.0% is an independently physically assessed functioning total or rate.",
    "Attribute service benefits to the facilities. Do not turn interview descriptions into independently measured causal impacts.",
    "Describe incomplete construction and operational gaps directly. Do not confuse them with incompleteness of the source records.",
    "All recommended timing is proposed and begins after report approval. Do not describe recommendations as undertakings already accepted by institutions.",
    "Acquisition warranty claims were deliberately removed from main prose. Keep the supported MoWT servicing arrangement and OPM damaged-laptop example.",
    "Do not replace concrete field examples with a repeated row-count/value/condition template.",
    "Keep numbered tables and figures, but use their captions to explain the asset or finding rather than the data processing."
  ],
  "source_index": {
    "O01": {
      "file": "raw-data-grouped/team-18/Kayunga/Busaale-HC-III/BUSAALE HC III.docx",
      "locator": "paragraph 41, answering interview table 3",
      "lg": "Kayunga",
      "facility": "Busaale Health Centre III",
      "region": "Central"
    },
    "O02": {
      "file": "raw-data-grouped/team-18/Kayunga/Busaale-HC-III/BUSAALE HC III.docx",
      "locator": "paragraph 47",
      "lg": "Kayunga",
      "facility": "Busaale Health Centre III",
      "region": "Central"
    },
    "O03": {
      "file": "raw-data-grouped/team-18/Kayunga/Busaale-HC-III/BUSAALE HC III.docx",
      "locator": "paragraphs 56 to 58",
      "lg": "Kayunga",
      "facility": "Busaale Health Centre III",
      "region": "Central"
    },
    "O04": {
      "file": "raw-data-grouped/team-18/Kayunga/Musiitwa-Seed-Secondary-School-Nazigo/MUSIITWA SEED SCHOOL.docx",
      "locator": "paragraphs 7, 13 and 14",
      "lg": "Kayunga",
      "facility": "Musiitwa Seed Secondary School Nazigo",
      "region": "Central"
    },
    "O05": {
      "file": "raw-data-grouped/team-18/Kayunga/Musiitwa-Seed-Secondary-School-Nazigo/MUSIITWA SEED SCHOOL.docx",
      "locator": "paragraphs 20 and 23 to 25",
      "lg": "Kayunga",
      "facility": "Musiitwa Seed Secondary School Nazigo",
      "region": "Central"
    },
    "O06": {
      "file": "raw-data-grouped/team-18/Kayunga/Musiitwa-Seed-Secondary-School-Nazigo/MUSIITWA SEED SCHOOL.docx",
      "locator": "paragraph 61",
      "lg": "Kayunga",
      "facility": "Musiitwa Seed Secondary School Nazigo",
      "region": "Central"
    },
    "O07": {
      "file": "raw-data-grouped/team-18/Kamuli/Kagumba-HC-III/KAGUMBA HC III.docx",
      "locator": "paragraph 47",
      "lg": "Kamuli",
      "facility": "Kagumba Health Centre III",
      "region": "Eastern"
    },
    "O08": {
      "file": "raw-data-grouped/team-18/Kamuli/Kagumba-HC-III/KAGUMBA HC III.docx",
      "locator": "paragraphs 53 and 54",
      "lg": "Kamuli",
      "facility": "Kagumba Health Centre III",
      "region": "Eastern"
    },
    "O09": {
      "file": "raw-data-grouped/team-18/Kamuli/Kagumba-HC-III/KAGUMBA HC III.docx",
      "locator": "paragraphs 57 to 59",
      "lg": "Kamuli",
      "facility": "Kagumba Health Centre III",
      "region": "Eastern"
    },
    "O10": {
      "file": "raw-data-grouped/team-13/Busia/_district-documents/Busia-local-government-report.docx",
      "locator": "paragraph 13",
      "lg": "Busia",
      "facility": "Bumunji, Buwembe and Majanji health centres",
      "region": "Eastern"
    },
    "O11": {
      "file": "raw-data-grouped/team-13/Busia/_district-documents/Busia-local-government-report.docx",
      "locator": "paragraph 20",
      "lg": "Busia",
      "facility": "Sikuda Seed Secondary School",
      "region": "Eastern"
    },
    "O12": {
      "file": "raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx",
      "locator": "paragraphs 69 and 70",
      "lg": "Nwoya",
      "facility": "Lungulu Seed Secondary School",
      "region": "Northern"
    },
    "O13": {
      "file": "raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx",
      "locator": "paragraphs 62 and 74",
      "lg": "Nwoya",
      "facility": "Lungulu Seed Secondary School",
      "region": "Northern"
    },
    "O14": {
      "file": "raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx",
      "locator": "paragraphs 135 and 136",
      "lg": "Nwoya",
      "facility": "Todora Health Centre III",
      "region": "Northern"
    },
    "O15": {
      "file": "raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx",
      "locator": "paragraphs 125, 145 and 146",
      "lg": "Nwoya",
      "facility": "Todora Health Centre III and Paraa Health Centre III",
      "region": "Northern"
    },
    "O16": {
      "file": "raw-data-grouped/team-01/Nebbi/_district-documents/UGIFT Assets Verification Nebbi District Report.docx",
      "locator": "paragraphs 27 and 28",
      "lg": "Nebbi",
      "facility": "Pamaka Health Centre III",
      "region": "Northern"
    },
    "O17": {
      "file": "raw-data-grouped/team-01/Nebbi/_district-documents/UGIFT Assets Verification Nebbi District Report.docx",
      "locator": "paragraphs 17 and 29",
      "lg": "Nebbi",
      "facility": "Pamaka Health Centre III",
      "region": "Northern"
    },
    "O18": {
      "file": "raw-data-grouped/team-10/Moroto/_district-documents/Moroto-local-government-report.docx",
      "locator": "paragraph 14",
      "lg": "Moroto",
      "facility": "Kalemungole Health Centre III",
      "region": "Northern"
    },
    "O19": {
      "file": "raw-data-grouped/team-10/Moroto/_district-documents/Moroto-local-government-report.docx",
      "locator": "paragraph 16",
      "lg": "Moroto",
      "facility": "Rupa Seed School",
      "region": "Northern"
    },
    "O20": {
      "file": "raw-data-grouped/team-30/Kibaale/Nyamarunda-HC-III/NYAMARUNDA HC III asset verification 24 Sep 2026.docx",
      "locator": "table 2, rows 2 and 3",
      "lg": "Kibaale",
      "facility": "Nyamarunda Health Centre III",
      "region": "Western"
    },
    "O21": {
      "file": "raw-data-grouped/team-30/Kibaale/Nyamarunda-HC-III/NYAMARUNDA HC III asset verification 24 Sep 2026.docx",
      "locator": "table 2, rows 4 and 5",
      "lg": "Kibaale",
      "facility": "Nyamarunda Health Centre III",
      "region": "Western"
    },
    "O22": {
      "file": "raw-data-grouped/team-25/Buliisa/Avogera-HC-III/AVOGERA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx",
      "locator": "paragraphs 40 to 42 and 50 to 58",
      "lg": "Buliisa",
      "facility": "Avogera Health Centre III",
      "region": "Western"
    },
    "O23": {
      "file": "raw-data-grouped/team-25/Buliisa/Ngwedo-Seed-Secondary-School/NGWEDO SEED SECONDARY SCHOOL ASSET VERIFICATION 24 Sep 2026.docx",
      "locator": "table 2, rows 3 and 4",
      "lg": "Buliisa",
      "facility": "Ngwedo Seed Secondary School",
      "region": "Western"
    },
    "O24": {
      "file": "raw-data-grouped/team-26/Bundibugyo/Bundimulangya-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT 222 BUNDIMULANGYA HEALTH CENTRE III AND BURONDO SEED SCHOOL (1).docx",
      "locator": "paragraphs 41, 50 and 59",
      "lg": "Bundibugyo",
      "facility": "Bundimulangya Health Centre III",
      "region": "Western"
    },
    "O25": {
      "file": "raw-data-grouped/team-28/Kyenjojo/Kyankaramata-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT 222 kyankaramata hc iii.docx",
      "locator": "paragraphs 41 and 62",
      "lg": "Kyenjojo",
      "facility": "Kyankaramata Health Centre III",
      "region": "Western"
    },
    "O26": {
      "file": "raw-data-grouped/team-25/Hoima/Kigorobya-Seed-Secondary-School/KIGOROBYA SEED SECONDARY SCHOOL ASSET VERIFICATION 24 Sep 2026.docx",
      "locator": "table 2, rows 3 to 5",
      "lg": "Hoima",
      "facility": "Kigorobya Seed Secondary School",
      "region": "Western"
    },
    "O27": {
      "file": "raw-data-grouped/team-31/Buvuma/Lukale-HC-III/LUKALE H.C III (1).docx",
      "locator": "paragraphs 59 and 61",
      "lg": "Buvuma",
      "facility": "Lukale Health Centre III",
      "region": "Central"
    },
    "O28": {
      "file": "raw-data-grouped/team-18/Kamuli/Kagumba-Seed-Secondary-School/Kagumba Seed school.docx",
      "locator": "paragraph 7",
      "lg": "Kamuli",
      "facility": "Kagumba Seed Secondary School",
      "region": "Eastern"
    },
    "O29": {
      "file": "raw-data-grouped/team-18/Kamuli/Bubago-HC-III/Bubago HCII.docx",
      "locator": "paragraphs 57 and 61",
      "lg": "Kamuli",
      "facility": "Bubago Health Centre",
      "region": "Eastern"
    },
    "O30": {
      "file": "raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx",
      "locator": "paragraphs 10 to 14 and 25 to 29",
      "lg": "Nwoya",
      "facility": "Got Apwoyo Seed Secondary School",
      "region": "Northern",
      "evidence_note": "The school remained under construction and had not been commissioned. Delivered furniture was on site and computer equipment was held at district headquarters pending completion."
    },
    "O31": {
      "file": "raw-data-grouped/team-01/Nebbi/_district-documents/UGIFT Assets Verification Nebbi District Report.docx",
      "locator": "paragraphs 40 to 61",
      "lg": "Nebbi",
      "facility": "Ndhew Seed School",
      "region": "Northern",
      "evidence_note": "Buildings were incomplete. Computer and science equipment remained at district headquarters and furniture had not been installed."
    },
    "O32": {
      "file": "raw-data-grouped/team-01/Nebbi/_district-documents/UGIFT Assets Verification Nebbi District Report.docx",
      "locator": "paragraphs 129 to 153",
      "lg": "Nebbi",
      "facility": "Mamba Seed School",
      "region": "Northern",
      "evidence_note": "Construction and commissioning were incomplete. Computers were temporarily accommodated in older structures; science equipment remained at district headquarters and furniture had not been installed."
    },
    "O33": {
      "file": "raw-data-grouped/team-01/Nebbi/_district-documents/UGIFT Assets Verification Nebbi District Report.docx",
      "locator": "paragraphs 205 to 233",
      "lg": "Nebbi",
      "facility": "Atego Seed School",
      "region": "Northern",
      "evidence_note": "Construction and commissioning were incomplete, but computers were connected and functioning in older structures. Power surges were reported. Do not describe the school as wholly unused."
    },
    "O34": {
      "file": "raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx",
      "locator": "paragraph 58; stored equipment detail in paragraph 62",
      "lg": "Nwoya",
      "facility": "Lungulu Seed Secondary School",
      "region": "Northern",
      "evidence_note": "The assets were not engraved. Stored computer equipment included two defective desktop units; do not describe every stored item as good."
    },
    "O35": {
      "file": "raw-data-grouped/team-26/Ntoroko/Butungama-Seed-Secondary-School/ASSET VERIFICATION AND RECORDING TOOL KIT 222 BUTUNGAMA HEALTH CENTRE III AND BUTUNGAMA SEED SCHOOL (1).docx",
      "locator": "school section, paragraphs 97, 105, 107 and 111",
      "lg": "Ntoroko",
      "facility": "Butungama Seed School",
      "region": "Western",
      "evidence_note": "The school interview states that it was still under construction. This alone does not establish that teaching had not begun."
    },
    "N01": {
      "file": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "locator": "MoWT row 4; REF Asset Register row 209567",
      "evidence_note": "The Ministry of Finance undertakes repairs and servicing of the Ministry of Works and Transport Toyota Hilux."
    },
    "N02": {
      "file": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "locator": "OPM rows 7, 9 and 10; REF Asset Register rows 209828, 209830 and 209831",
      "evidence_note": "Damaged HP laptops identified as not being used. Examples, not a complete damaged-item count."
    },
    "Q01": {
      "file": "tmp/narrative-report/summary.json",
      "locator": "overall and by_region, underlying REF filters in sources.md",
      "evidence_note": "225133 entries;2569 not in use with damage wording;483 not in use with storage/new wording excluding conflicting negative condition;50211 engraved;21023programme marking;29188other marking."
    },
    "Q02": {
      "file": "raw-data-grouped/facility-reconciliation.csv; raw-data-grouped/master-source-rows.csv; raw-data-grouped/supervisor-decisions.csv",
      "locator": "Final master-list scopes and outcomes as implemented in reconciliation summary",
      "evidence_note": "629 master entries,371health and258school.589 have verification materials/consolidated entries and40are separately reconciled. Do not relabel589as individually physically inspected."
    },
    "D01": {
      "file": "outputs/report-templates/Verification report_ 24092026_Draft_ BB.docx",
      "locator": "paragraphs 69 to 75",
      "evidence_note": "Programme closure outputs differ from later verification scope.196/259schools complete,189operational;354/373health upgrades complete."
    },
    "O36": {
      "region": "Western",
      "lg": "Buliisa",
      "facility": "Butiaba Health Centre III",
      "file": "raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/BUTAIBA HEALTH CENTER.docx",
      "locator": "table 5, row 1, interview question 4, Challenges",
      "evidence_note": "The hydraulic delivery bed was not in use because staff lacked knowledge of its operation. National Medical Stores did not have strips for the supplied glucometers. This establishes an access-to-consumables gap; it does not establish that every glucometer was physically faulty.",
      "exact_source_excerpt": "Lack of training on how to use the new supplied items; for example the Delivery hydralic bed is not use for lack of proper knowledege on how to operate it. NMS does not have the strips for the Glucometers that were supplied"
    },
    "O37": {
      "region": "Western",
      "lg": "Buliisa",
      "facility": "Older Butiaba Health Centre facility",
      "file": "raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/butaiba report.docx",
      "locator": "paragraph 10",
      "evidence_note": "The report explicitly links the older UgIFT-built facility and its equipment to flood damage. Describe the older facility, without implying that all current services or all current buildings are submerged.",
      "exact_source_excerpt": "The old facility built by UGIFT was affected by floods and its equipment"
    }
  },
  "national_institutions_visited": [
    "Ministry of Works and Transport",
    "Ministry of Education and Sports",
    "Ministry of Agriculture, Animal Industry and Fisheries",
    "Ministry of Health",
    "Office of the Prime Minister",
    "Ministry of Water and Environment",
    "Ministry of Gender, Labour and Social Development",
    "Local Government Finance Commission",
    "National Environment Management Authority",
    "Public Procurement and Disposal of Public Assets Authority",
    "Office of the Auditor General",
    "Ministry of Public Service",
    "Ministry of Lands, Housing and Urban Development",
    "Ministry of Local Government",
    "Ministry of Finance, Planning and Economic Development"
  ],
  "national_institutions_visited_source": "Client draft paragraph146, retains15named institutions without conflicting13count.",
  "revision_purpose": "Direct field report narrative focused on intended services, findings, gaps and action; no monetary figures or source filenames in report text.",
  "photo_context_notes": [
    {
      "source_id": "O37",
      "text": "The older UgIFT-built Butiaba facility and its equipment were affected by floods. A photograph should identify the older flood-affected facility, rather than imply that all current services are submerged."
    }
  ]
}
```


## Revision evidence: narrative/additional_cases.json

```json
{
  "purpose": "Additional evidence-backed field content for the expanded narrative report. Only case prose is for publication; source_index and audit notes are private.",
  "editorial_notes": [
    "Expected statements describe the intended service or management outcome; they do not assert a separately verified contractual promise. Actions and priorities are proposed recommendations, not completed interventions.",
    "These cases were checked against the current report text extracted from the 46-page version; none of the eleven local facilities appeared in that text. The national cases add details beyond the existing MoWT vehicle-maintenance and OPM damaged-laptop examples.",
    "Keep institutional and facility names in the report; keep filenames, source IDs, paths, quotations and audit notes outside it.",
    "There are no monetary figures. Do not convert reported conditions, item remarks or user accounts into a claim that every asset was independently tested."
  ],
  "local_cases": [
    {
      "id": "AD01",
      "region": "Central",
      "facility": "Kijuna Health Centre III",
      "lg": "Kassanda",
      "expected": "Patient equipment and basic utilities should be available when care is needed.",
      "found": "The wheelchairs were not functional, and a failed water pump left the facility with inadequate water. Inadequate power also prevented full use of electronic equipment.",
      "finding": "Expected: Patient equipment and basic utilities should be available when care is needed. Found: The wheelchairs were not functional, and a failed water pump left the facility with inadequate water. Inadequate power also prevented full use of electronic equipment.",
      "gap": "The facility faced separate constraints on patient movement, water supply and equipment use.",
      "action": "Kassanda District should arrange technical assessment and repair of the wheelchairs and pump, restore a dependable power supply and test the affected equipment before returning it to use.",
      "priority": "High",
      "source_ids": [
        "AD01"
      ]
    },
    {
      "id": "AD02",
      "region": "Central",
      "facility": "Kikandwa Health Centre III",
      "lg": "Kassanda",
      "expected": "The health facility should provide powered equipment, durable buildings and secure custody of its assets.",
      "found": "Electronic equipment could not be used because reliable electricity and solar power were unavailable. Storage for damaged assets was inadequate, the facility lacked a perimeter fence, and defects were observed in flooring and skirting.",
      "finding": "Expected: The health facility should provide powered equipment, durable buildings and secure custody of its assets. Found: Electronic equipment could not be used because reliable electricity and solar power were unavailable. Storage for damaged assets was inadequate, the facility lacked a perimeter fence, and defects were observed in flooring and skirting.",
      "gap": "Power, secure storage and correction of building defects remained necessary for full and safe use.",
      "action": "Kassanda District should agree a joint power, security and defects plan, provide secure temporary storage, and have technical staff verify repairs and equipment operation.",
      "priority": "High",
      "source_ids": [
        "AD02"
      ]
    },
    {
      "id": "AD03",
      "region": "Central",
      "facility": "Kyasansuwa Health Centre III",
      "lg": "Kassanda",
      "expected": "Computer equipment should support administration and reporting, while floors and bathrooms should remain usable and easy to maintain.",
      "found": "The facility reported three computers completely damaged following unstable power and surges. Poor floor finishes and defective staff bathroom levels were also observed.",
      "finding": "Expected: Computer equipment should support administration and reporting, while floors and bathrooms should remain usable and easy to maintain. Found: The facility reported three computers completely damaged following unstable power and surges. Poor floor finishes and defective staff bathroom levels were also observed.",
      "gap": "Unstable electricity threatened the remaining electronics, while defective finishes and drainage needed correction.",
      "action": "Kassanda District should stabilise and protect the electrical supply, assess the three computers for repair or replacement, and correct the floor and bathroom defects under technical supervision.",
      "priority": "High",
      "source_ids": [
        "AD03"
      ]
    },
    {
      "id": "AD04",
      "region": "Northern",
      "facility": "Alwi Seed Secondary School",
      "lg": "Pakwach",
      "expected": "The computer laboratory and security equipment should support teaching and school operation.",
      "found": "The school reported power surges. Nine monitors and ten system units were not working, as were the server power-backup unit and twenty other power-backup units. Only one of thirteen security cameras was functional.",
      "finding": "Expected: The computer laboratory and security equipment should support teaching and school operation. Found: The school reported power surges. Nine monitors and ten system units were not working, as were the server power-backup unit and twenty other power-backup units. Only one of thirteen security cameras was functional.",
      "gap": "The loss of working computer stations and power protection reduced the usable laboratory capacity and left much of the camera system unavailable.",
      "action": "Pakwach District and the school should first assess the electrical supply and protection, then repair or replace failed equipment and test the whole laboratory and camera system before acceptance.",
      "priority": "High",
      "source_ids": [
        "AD04"
      ]
    },
    {
      "id": "AD05",
      "region": "Northern",
      "facility": "Wadelai Seed Secondary School",
      "lg": "Pakwach",
      "expected": "The school should be able to use its computer laboratory reliably and keep water storage structures safe.",
      "found": "Twenty desktop computers were recorded as working and in use, but the school reported a solar fault that interrupted use of electrical equipment. One water-tank stand was broken and presented a threat to students.",
      "finding": "Expected: The school should be able to use its computer laboratory reliably and keep water storage structures safe. Found: Twenty desktop computers were recorded as working and in use, but the school reported a solar fault that interrupted use of electrical equipment. One water-tank stand was broken and presented a threat to students.",
      "gap": "Usable equipment remained dependent on an unreliable power supply, and the damaged tank support required immediate attention.",
      "action": "The school and Pakwach District should restrict access around the damaged tank support pending an engineering assessment, repair the support, and restore and test the solar system.",
      "priority": "High",
      "source_ids": [
        "AD05"
      ]
    },
    {
      "id": "AD06",
      "region": "Eastern",
      "facility": "Nansanga Seed Secondary School",
      "lg": "Budaka",
      "expected": "The supplied desktop computers should be installed and available for teaching.",
      "found": "The school lacked reliable power, and twenty-seven of its twenty-eight desktops remained packed.",
      "finding": "Expected: The supplied desktop computers should be installed and available for teaching. Found: The school lacked reliable power, and twenty-seven of its twenty-eight desktops remained packed.",
      "gap": "Most of the supplied computer capacity had not reached classroom use because a basic operating requirement was unresolved.",
      "action": "Budaka District and the school should settle the power connection or suitable alternative, arrange installation and testing, and confirm the number of computers available to learners.",
      "priority": "High",
      "source_ids": [
        "AD06"
      ]
    },
    {
      "id": "AD07",
      "region": "Eastern",
      "facility": "Muhula Seed Secondary School",
      "lg": "Butaleja",
      "expected": "The school should receive completed buildings and tested equipment before formal handover and operation.",
      "found": "The contractor had not handed over the school, and it was not operating. Buildings showed cracks, an air conditioner remained boxed with a missing fan, and the installed water pump was not working.",
      "finding": "Expected: The school should receive completed buildings and tested equipment before formal handover and operation. Found: The contractor had not handed over the school, and it was not operating. Buildings showed cracks, an air conditioner remained boxed with a missing fan, and the installed water pump was not working.",
      "gap": "Construction completion, equipment completeness and successful testing had not come together to make the school ready.",
      "action": "Butaleja District and the Ministry of Education and Sports should agree a defects and handover schedule with the contractor, rectify the works, complete the equipment and witness operational tests before handover.",
      "priority": "High",
      "source_ids": [
        "AD07"
      ]
    },
    {
      "id": "AD08",
      "region": "Eastern",
      "facility": "Sop Sop Health Centre III",
      "lg": "Tororo",
      "expected": "Delivered equipment should be accompanied by the skills and accessories needed to use it.",
      "found": "The facility reported that much of its equipment remained in store because staff did not know how to operate it. Oxygen equipment had arrived without cylinders. Tuberculosis testing and maternity services had nevertheless improved.",
      "finding": "Expected: Delivered equipment should be accompanied by the skills and accessories needed to use it. Found: The facility reported that much of its equipment remained in store because staff did not know how to operate it. Oxygen equipment had arrived without cylinders. Tuberculosis testing and maternity services had nevertheless improved.",
      "gap": "Equipment delivery had not been matched consistently with user training and a complete operating package.",
      "action": "Tororo District and the Ministry of Health should arrange practical training at the facility, confirm the required oxygen components, and check that trained staff can safely use each released item.",
      "priority": "High",
      "source_ids": [
        "AD08"
      ]
    },
    {
      "id": "AD09",
      "region": "Eastern",
      "facility": "Bunamono Health Centre III",
      "lg": "Bududa",
      "expected": "The installed water system should supply the staff houses, and supplied clinical equipment should be ready for use.",
      "found": "The water tank was not working and the solar pump was not connected, leaving the staff houses without water. A supplied laboratory stand remained boxed because staff could not assemble it, and a glucometer lacked test strips.",
      "finding": "Expected: The installed water system should supply the staff houses, and supplied clinical equipment should be ready for use. Found: The water tank was not working and the solar pump was not connected, leaving the staff houses without water. A supplied laboratory stand remained boxed because staff could not assemble it, and a glucometer lacked test strips.",
      "gap": "The facility needed installation, demonstration and consumables to turn delivered assets into usable services.",
      "action": "Bududa District should complete and test the water connection, arrange assembly and user demonstration for the laboratory stand, and establish a supply of compatible glucometer strips.",
      "priority": "High",
      "source_ids": [
        "AD09"
      ]
    },
    {
      "id": "AD10",
      "region": "Western",
      "facility": "Kihungya Seed Secondary School",
      "lg": "Buliisa",
      "expected": "The school investment should provide usable science and computer laboratories, staff accommodation, water and secure premises.",
      "found": "The science block, computer laboratory and library were still under construction, and staff quarters were incomplete. The school reported no electricity for computer sessions, no water for sanitation and no perimeter fence. Its administration block was already in use.",
      "finding": "Expected: The school investment should provide usable science and computer laboratories, staff accommodation, water and secure premises. Found: The science block, computer laboratory and library were still under construction, and staff quarters were incomplete. The school reported no electricity for computer sessions, no water for sanitation and no perimeter fence. Its administration block was already in use.",
      "gap": "The school was partly in use while essential teaching spaces, utilities and security remained unfinished.",
      "action": "Buliisa District and the Ministry of Education and Sports should use one completion plan for the laboratories, staff housing, electricity, water and security, with separate testing and handover of each finished element.",
      "priority": "High",
      "source_ids": [
        "AD10"
      ]
    },
    {
      "id": "AD11",
      "region": "Western",
      "facility": "Kihungya Health Centre III",
      "lg": "Buliisa",
      "expected": "Expanded buildings and equipment should support care at the health centre, with responsibility clear for any items kept elsewhere.",
      "found": "Staff reported more room for patients, easier working arrangements through staff accommodation, and electricity from the new solar power house. Buildings were in use. A gas stove, electric suction apparatus, laboratory stool and electric centrifuge were recorded at the subcounty rather than the health centre.",
      "finding": "Expected: Expanded buildings and equipment should support care at the health centre, with responsibility clear for any items kept elsewhere. Found: Staff reported more room for patients, easier working arrangements through staff accommodation, and electricity from the new solar power house. Buildings were in use. A gas stove, electric suction apparatus, laboratory stool and electric centrifuge were recorded at the subcounty rather than the health centre.",
      "gap": "The building and power investment was supporting care, but the intended use and custody of equipment held away from the facility needed confirmation.",
      "action": "Buliisa District and facility management should preserve the working building and solar arrangements, confirm who holds the off-site equipment, and agree whether it should be deployed to the health centre or remain at its present location.",
      "priority": "Medium",
      "source_ids": [
        "AD11"
      ]
    }
  ],
  "national_cases": [
    {
      "id": "AD12",
      "institution": "Ministry of Finance, Planning and Economic Development",
      "facility": "Ministry of Finance, Planning and Economic Development",
      "region": "National",
      "lg": "National",
      "expected": "Staff computers should support their workload, and portable equipment should remain identifiable and accountable.",
      "found": "Most computers were working, but some keyboards and power-backup units had failed, and some older computers were freezing. Laptop losses were supported by police letters. The team also reported difficulty obtaining some laptops for engraving.",
      "finding": "Expected: Staff computers should support their workload, and portable equipment should remain identifiable and accountable. Found: Most computers were working, but some keyboards and power-backup units had failed, and some older computers were freezing. Laptop losses were supported by police letters. The team also reported difficulty obtaining some laptops for engraving.",
      "gap": "Equipment reliability, follow-up of lost assets and completion of identification each required a specific management response.",
      "action": "The ministry should assess the failed accessories and freezing computers, follow up the reported laptop losses, and arrange a supervised exercise to identify and mark all remaining portable equipment.",
      "priority": "High",
      "source_ids": [
        "AD12"
      ]
    },
    {
      "id": "AD13",
      "institution": "Ministry of Finance, Planning and Economic Development",
      "facility": "Ministry of Finance, Planning and Economic Development",
      "region": "National",
      "lg": "National",
      "expected": "Furniture should remain assigned to a location and custodian when offices move.",
      "found": "When programme staff moved to premises already furnished, their earlier furniture was left in the old building. Some remained in store, while staff said other items had gone to different offices.",
      "finding": "Expected: Furniture should remain assigned to a location and custodian when offices move. Found: When programme staff moved to premises already furnished, their earlier furniture was left in the old building. Some remained in store, while staff said other items had gone to different offices.",
      "gap": "The move had split the furniture between storage and other offices, requiring confirmation of its present custody and use.",
      "action": "The ministry should inspect the old store and recipient offices, confirm the condition and custodian of each item, and approve reuse or other appropriate treatment of furniture no longer required.",
      "priority": "Medium",
      "source_ids": [
        "AD13"
      ]
    },
    {
      "id": "AD14",
      "institution": "Office of the Prime Minister",
      "facility": "Office of the Prime Minister",
      "region": "National",
      "lg": "National",
      "expected": "Computers should have enough capacity for the work assigned to their users.",
      "found": "Users reported that the capacity of the HP Envy i3 laptops was below the volume of work handled, although the machines were described as being in fair condition.",
      "finding": "Expected: Computers should have enough capacity for the work assigned to their users. Found: Users reported that the capacity of the HP Envy i3 laptops was below the volume of work handled, although the machines were described as being in fair condition.",
      "gap": "A usable laptop could still be poorly matched to the workload of its user.",
      "action": "The office should assess the requirements of the affected users and decide whether upgrading, reallocating or replacing the laptops would provide suitable capacity.",
      "priority": "Medium",
      "source_ids": [
        "AD14"
      ]
    },
    {
      "id": "AD15",
      "institution": "Ministry of Works and Transport",
      "facility": "Ministry of Works and Transport",
      "region": "National",
      "lg": "National",
      "expected": "Installed office and conferencing equipment should support the secretariat and carry a traceable asset identity.",
      "found": "The secretariat reported that the installed photocopier supported its daily work. The video-conferencing system was installed and functioning, but it had not been engraved or included in the asset list presented for verification.",
      "finding": "Expected: Installed office and conferencing equipment should support the secretariat and carry a traceable asset identity. Found: The secretariat reported that the installed photocopier supported its daily work. The video-conferencing system was installed and functioning, but it had not been engraved or included in the asset list presented for verification.",
      "gap": "An operational system still required clear identification and custody.",
      "action": "The ministry should identify the conferencing system and its components, assign a custodian, and apply a suitable durable identifier without damaging the equipment.",
      "priority": "Medium",
      "source_ids": [
        "AD15"
      ]
    },
    {
      "id": "AD16",
      "institution": "Ministry of Health",
      "facility": "Ministry of Health",
      "region": "National",
      "lg": "National",
      "expected": "Office equipment in use should be identifiable by a durable asset mark.",
      "found": "Two heavy-duty printers, one at the Industrial Area engineering office and one at headquarters, were in use and in good condition but unengraved. One headquarters laptop was also recorded without engraving.",
      "finding": "Expected: Office equipment in use should be identifiable by a durable asset mark. Found: Two heavy-duty printers, one at the Industrial Area engineering office and one at headquarters, were in use and in good condition but unengraved. One headquarters laptop was also recorded without engraving.",
      "gap": "Working equipment at separate offices still lacked the marking needed for straightforward physical identification.",
      "action": "The ministry should mark these items, link the marks to their serial numbers and office locations, and obtain custody confirmation from the receiving units.",
      "priority": "Medium",
      "source_ids": [
        "AD16"
      ]
    },
    {
      "id": "AD17",
      "institution": "National Environment Management Authority",
      "facility": "National Environment Management Authority",
      "region": "National",
      "lg": "National",
      "expected": "Computers and shared office equipment should remain identifiable wherever they are used.",
      "found": "Four Lenovo laptops serving the executive office and environmental audit, together with a heavy-duty printer, were recorded as functional but not engraved.",
      "finding": "Expected: Computers and shared office equipment should remain identifiable wherever they are used. Found: Four Lenovo laptops serving the executive office and environmental audit, together with a heavy-duty printer, were recorded as functional but not engraved.",
      "gap": "The equipment could support work, but lacked a durable identifying mark.",
      "action": "The authority should mark the five items, record their serial numbers and custodians, and include them in regular physical checks.",
      "priority": "Medium",
      "source_ids": [
        "AD17"
      ]
    },
    {
      "id": "AD18",
      "institution": "Ministry of Water and Environment",
      "facility": "Ministry of Water and Environment",
      "region": "National",
      "lg": "National",
      "expected": "Portable tablets should carry an asset identifier and have an assigned custodian.",
      "found": "Ten Apple tablets were recorded without engraving.",
      "finding": "Expected: Portable tablets should carry an asset identifier and have an assigned custodian. Found: Ten Apple tablets were recorded without engraving.",
      "gap": "Portable equipment required an identification method that would allow each unit to be traced to its user and location.",
      "action": "The ministry should apply suitable durable identifiers, link them to serial numbers, and confirm custody before the next physical check.",
      "priority": "Medium",
      "source_ids": [
        "AD18"
      ]
    }
  ],
  "source_index": {
    "AD01": {
      "path": "raw-data-grouped/team-25/_team-documents/KIJUNA HCIII UGIFT Asset Verification - FINAL.docx",
      "excerpts": [
        {
          "locator": "table 1, row 5",
          "text": "Name of Local Government | KASANDA DISTRICT LOCAL GOVERNMENT"
        },
        {
          "locator": "paragraph 154",
          "text": "The facility has inadequate power supply to support the functioning of all electronic assets, resulting in underutilisation of some equipment and potentially affecting effective service delivery."
        },
        {
          "locator": "paragraph 158",
          "text": "The wheelchairs available at the facility were not functional, limiting their effective use in supporting patients who require mobility assistance."
        },
        {
          "locator": "paragraph 174",
          "text": "The facility has inadequate water supply due to a non-performing water pump, affecting the availability of water required for normal facility operations and service delivery."
        }
      ],
      "audit_note": ""
    },
    "AD02": {
      "path": "raw-data-grouped/team-25/_team-documents/KIKANDWA HCIII UGIFT Asset Verification Tool Kit - FINAL.docx",
      "excerpts": [
        {
          "locator": "table 1, row 5",
          "text": "Name of Local Government | KASANDA DISTRICT LOCAL GOVERNMENT"
        },
        {
          "locator": "paragraph 152",
          "text": "Electronic assets are not functioning due to the lack of solar power and reliable electricity, resulting in underutilisation and affecting effective service delivery."
        },
        {
          "locator": "paragraph 154",
          "text": "There is inadequate storage space for damaged and non-functional assets, making proper custody, management and safeguarding of such assets difficult."
        },
        {
          "locator": "paragraph 158",
          "text": "Poor workmanship has been observed, particularly on the building skirting and flooring, which may affect the quality, durability and general condition of the facility."
        },
        {
          "locator": "paragraph 160",
          "text": "The absence of a perimeter fence presents potential security risks to the facility, staff, patients and assets."
        }
      ],
      "audit_note": ""
    },
    "AD03": {
      "path": "raw-data-grouped/team-25/_team-documents/Kyasansuwa HCIII UGIFT Asset Verification Tool Kit - FINAL.docx",
      "excerpts": [
        {
          "locator": "table 1, row 5",
          "text": "Name of Local Government | Kasanda Local Government"
        },
        {
          "locator": "paragraph 159",
          "text": "Concern/Observation: The facility experiences inadequate and unstable power conditions, including power surges, which have affected the functionality of computers. Three computers are reported to be completely damaged. This reduces the facility's capacity to effectively use available information and communication technology for administration, reporting, records management and other health service functions. Continued exposure of electronic equipment to unstable power also presents a risk of further equipment damage."
        },
        {
          "locator": "paragraph 168",
          "text": "Concern/Observation: The facility has areas where the floors have been poorly done. Poor floor finishing and workmanship can affect the durability, cleanliness and general usability of the facility. Where floor surfaces are uneven or poorly finished, they may also create difficulties for cleaning, movement of patients and equipment and the general maintenance of a safe health care environment."
        },
        {
          "locator": "paragraph 174",
          "text": "Concern/Observation: Poor workmanship was observed in relation to the staff bathrooms, particularly the levels and arrangement affecting how water flows and drains. Inadequate levels can result in poor drainage and water stagnation, which may contribute to unhygienic conditions, deterioration of surfaces and inconvenience to users. This reflects the need for closer attention to quality control and finishing of facility construction and improvement works."
        }
      ],
      "audit_note": ""
    },
    "AD04": {
      "path": "raw-data-grouped/team-01/Pakwach/Alwi-Seed-Secondary-School/ZOMBO - ATYAK HC III & ALWI SEED.docx",
      "excerpts": [
        {
          "locator": "table 10, row 1",
          "text": "4 | How has the UgIFT support helped in service delivery in the area, any issues, challenges and any recommendations for better program implementation. | The setup of the school has completely revolutionized l education service delivery. However, there is an issue of power surges, under staffing, the ratio of students to classes and latrines, numbers are high over 1,000 students. ugIFT should support to ensure power stability, recruit more staff."
        },
        {
          "locator": "table 12, row 2",
          "text": "Desktop Computer | Education |  | 28\nDell Optiplex\n3010 Intel \ncore i5, \n19.5 Inch \nDisplay Monitor - Pakwach District – Alwi SC – Alwi Seed School  |  | ALWI SEED S.S |  |  |  |  |  |  |  | Some are functional some are  | In use, 9 monitors and 10 System Units are not working "
        },
        {
          "locator": "table 12, row 7",
          "text": "Server UPS | Education |  | 1 Server UPS - Pakwach District – Alwi SC – Alwi Seed School |  |  |  |  |  |  |  |  |  | Functional  | Not working"
        },
        {
          "locator": "table 12, row 8",
          "text": "UPS | Education |  | 20   \nIntex \nLW UPS 850 - Pakwach District – Alwi SC – Alwi Seed School |  | ALWI SEED S.S |  |  |  |  |  |  |  | Non-Functional | Not working"
        },
        {
          "locator": "table 12, row 11",
          "text": "CCTV Camera | Education |  | 13 CCTV \nCamera - Pakwach District – Alwi SC – Alwi Seed School |  |  |  |  |  |  |  |  |  | Non-Functional  | Only 1 is in use and functional "
        }
      ],
      "audit_note": "The document contains two facilities. Only the school interview and school tables 10 and 12 support this case. Use item-level remarks over the conflicting Functional label on the server power-backup row. Twelve failed cameras is derived from 13 present and only one functional."
    },
    "AD05": {
      "path": "raw-data-grouped/team-01/Pakwach/Wadelai-Seed-Secondary-School/ZOMBO AMWONYO & WADELAI 2.docx",
      "excerpts": [
        {
          "locator": "table 10, row 1",
          "text": "4 | How has the UgIFT support helped in service delivery in the area, any issues, challenges and any recommendations for better program implementation. | The setup of the school structures has created room for academic progress in the community i.e., featuring science labs, staff quarters, and modern sanitation blocks that will completely revolutionize rural education service delivery. However, there is an issue with the solar panel and it has hindered the usage of the electric assets. As well there is a broken water tank stand which poses a threat to students. Need support for a reliable power supply."
        },
        {
          "locator": "table 12, row 2",
          "text": "Desktop Computer | Education |  | 20\nDell Vostro \n3030 Intel \ncore i5, \n19.5 Inch \nDisplay Monitor - Pakwach District – Wadelai SC – Wadelai Seed School  |  | Not engraved | 10/10/25 |  |  | 4,100,000 |  |  |  | Functional  | In use Cost amount is for 1 item"
        },
        {
          "locator": "table 13, row 11",
          "text": "Water tanks | Education |  | 4, (5000) plastic water tanks – Pakwach District, Wadelai SC, Wadelai Seed SS  |  | Not engraved |  |  |  |  |  |  |  | Functional | In use however, 1 the water tank stand is broken"
        }
      ],
      "audit_note": "The document also covers Amwonyo Health Centre. This case uses only the Wadelai school interview and tables. Working computers do not establish continuous use where the interview reports a solar fault."
    },
    "AD06": {
      "path": "raw-data-grouped/team-12/Budaka/_district-documents/Budaka-local-government-report.docx",
      "excerpts": [
        {
          "locator": "paragraph 55",
          "text": "Nansanga Seed Secondary School has no reliable power and 27 of 28 desktops remain packed."
        }
      ],
      "audit_note": ""
    },
    "AD07": {
      "path": "raw-data-grouped/team-12/Butaleja/Muhula-Seed-Secondary-School/Butaleja-school-Muhula-Seed-Secondary-School.docx",
      "excerpts": [
        {
          "locator": "paragraph 5",
          "text": "The school was photographed and a hand-filled toolkit that names it is on file. The guide spells the name MUHUVLA; the schedules spell MUHULA. The programme list names Kachonga. No visitors' register was seen. The contractor has not handed the site over, so the school is not operating."
        },
        {
          "locator": "paragraph 14",
          "text": "The air conditioner set is incomplete, the fan missing, and still in its box. Buildings already show cracks while the contractor claims the works finished."
        },
        {
          "locator": "table 2, row 3",
          "text": "Functionality | Furniture and most ICT items recorded as new and not yet tested. A printer and a projector are recorded as in use. The water pump is installed and not yet working."
        },
        {
          "locator": "table 2, row 4",
          "text": "Usage / performance | Not in use. The contractor has not handed the school over."
        }
      ],
      "audit_note": "The institution is described as not operating, but one printer and projector are separately marked in use. The case does not claim every item was unused. It does not resolve programme naming Kachonga/Muhula; that belongs to reconciliation."
    },
    "AD08": {
      "path": "raw-data-grouped/team-13/Tororo/Sop-Sop-HC-III/Tororo-health-centre-Sop-Sop-HC-III.docx",
      "excerpts": [
        {
          "locator": "paragraph 16",
          "text": "The discussion guide was answered. The informant says much of the equipment delivered is still in the store because staff lack knowledge of how to operate it, and asks for training, more staff and fencing."
        },
        {
          "locator": "table 2, row 4",
          "text": "Usage / performance | Partly established. TB testing and maternity service have improved, but oxygen came without cylinders, staffing is low and the facility is not fenced."
        }
      ],
      "audit_note": ""
    },
    "AD09": {
      "path": "raw-data-grouped/team-14/Bududa/Bunamono-HC-III/Bududa-health-centre-Bunamono-HC-III.docx",
      "excerpts": [
        {
          "locator": "paragraph 16",
          "text": "The discussion guide on the booklet records that the facility holds a record of all the assets provided under the programme, that broken assets go to the store, and that nothing is written down about what has failed. It names the health services being closer to the people and the jobs the support brought, then the want of a water connection, a 5000 litre tank that does not work and a solar installation that is not finished. The assistant asked for the water tank to be put back into service and for the solar pump to be connected, so that the staff houses have water."
        },
        {
          "locator": "table 2, row 3",
          "text": "Functionality | Reported line by line on the hand-filled booklet, which runs the whole checklist. Most lines are working. Both digital blood pressure machines are not, one of the two aneroid machines is not, two of the four stethoscopes are not, one delivery bed and three MVA kits are broken, one examination light is broken, one filing cabinet is faulty and one glucometer has no strips. The water tank is not working and the solar that should pump it is not connected, so the staff houses have no water."
        },
        {
          "locator": "table 2, row 4",
          "text": "Usage / performance | Reported item by item in the remarks beside each line. Some assets are held new in the store rather than in service: the kick bowls, the bowl stands, four wall clocks and the ESR stand, which is still boxed because the staff could not set it up."
        }
      ],
      "audit_note": "The instrument stand is described only as an ESR stand in the source; body wording avoids an unsupported expansion of the abbreviation."
    },
    "AD10": {
      "path": "raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/kihungya seed school.docx",
      "excerpts": [
        {
          "locator": "table 5, row 1",
          "text": "4 | How has the UgIFT support helped in service delivery in the area, any issues, challenges and any recommendations for better program implementation. | It has brought free education services to people within the area.\nOffered jobs to people around the school and market for their agricultural products\nChallenegs \nSchool is under construction and most structures not ready for use.\nNo eletricity to run the ICT sessions\nNo fence\nLack enough learning materials, were given study material for only physics , chemistry, Bisology and math S1 & S2\nNo water which affects sanitation\nRecommendations\nGive gaurds to have safety of the values provided and  a fence (chain link).\nDrill water\n\n\n\n\n"
        },
        {
          "locator": "table 8, row 3",
          "text": "Admin block |  | 1 | Office & staff room |  |  |  |  |  |  |  |  |  | IN USE | "
        },
        {
          "locator": "table 8, row 9",
          "text": "Science block |  | 1 | 2 sections of lab chemisry and Boilogy lab |  |  |  |  |  |  |  |  |  | Not in use | Under construction"
        },
        {
          "locator": "table 8, row 10",
          "text": "Computer and library |  | 1 | 2 sections 1 computer lab\n1 library |  |  |  |  |  |  |  |  |  | Not in use | Under construction"
        },
        {
          "locator": "table 8, row 11",
          "text": "Staff quarters |  | 3 | 2 units on each block with kicthen and toilet |  |  |  |  |  |  |  |  |  | Incomplete | Under construction"
        }
      ],
      "audit_note": "The administration block is marked in use, so the whole school must not be called unopened. The unfinished laboratories and staff quarters are specific."
    },
    "AD11": {
      "path": "raw-data-grouped/team-25/Buliisa/Kihungya-HC-III/BULIISA KIHUNGYA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx",
      "excerpts": [
        {
          "locator": "table 5, row 1",
          "text": "4 | How has the UgIFT support helped in service delivery in the area, any issues, challenges and any recommendations for better program implementation. | The UgIFT support  has helped the facility with good service delivery.\nEfficient health care due to the expansion and renovation of more facilities and new buildings.\nAccommodation of staff member has made work easy for health care workers.\nPatients well being.\nEnough space to take in more patients than before.\nAvailability of electricity due to the construction of the solar power house."
        },
        {
          "locator": "table 6, row 73",
          "text": "Stove, Gas | HEALTH |  | Heats water or sterilizes |  | Not\nEngraved |  |  |  |  |  |  |  | FUNCTIONAL | At the sub- county"
        },
        {
          "locator": "table 6, row 142",
          "text": "Suction Apparatus, (Electric) | \nHEALTH |  | Removes fluid/secretions from airway |  | \nNot\nEngraved |  | \n |  |  |  |  |  | \nFUNCTIONAL | At the sub- county"
        },
        {
          "locator": "table 6, row 186",
          "text": "Stool, Laboratory | \nHEALTH |  | Seating for laboratory staff |  | Not\nEngraved |  |  |  |  |  |  |  | FUNCTIONAL | At the sub- county"
        },
        {
          "locator": "table 6, row 196",
          "text": "Centrifuge (Electric) | \nHEALTH |  | Spins blood samples |  | Not\nEngraved |  | \n |  |  |  |  |  | \nFUNCTIONAL | At the sub- county"
        },
        {
          "locator": "table 6, row 262",
          "text": "Non Residential Buildings | \nHEALTH |  | TOILETS\nPLACENTER PIT\nSOLAR POWER HOUSE |  |  |  |  |  |  |  |  |  | FUNCTIONAL | All in use and good condition"
        },
        {
          "locator": "table 6, row 265",
          "text": "Residential Buildings | \nHEALTH |  | STAFF QUARTERS\nMULTIPURPOSE BUILDING |  |  |  |  |  |  |  |  |  | \nFUNCTIONAL | All are in use and in good condithion"
        }
      ],
      "audit_note": "Interview evidence is reported experience, not measured patient outcomes. Location At the sub-county does not by itself prove loss or diversion; action calls for confirmation and appropriate deployment."
    },
    "AD12": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "MoFPED worksheet, row 3",
          "selected_cells": {
            "2": "Lenovo Desktop Computer",
            "4": "Budget Policy and Evaluation Dep't-UGIFT-MOFPED",
            "6": "V5BYC581",
            "7": "Lenovo Monitor 21.5Inch V50131MB",
            "9": "UGIFT-BPED/MON/21-01",
            "17": "Functioning",
            "18": "Most of the computers are in good condition and working well, expect others where we found out that some of the accessories like keyboard and the UPS are spoilt and other computers have started freezing especially those acquired in the first years of the programme.\n\nSome of the staff lost thier laptops and we managed to get police letter confirming the case number.\n\nsome of the staff intentionally refuse thier gadgets like laptops to be engraved",
            "19": "MOFPED"
          }
        }
      ],
      "audit_note": "A narrative remark summarises several computers and laptops; it must not be treated as a count attached to the single row. The same material is copied into the MoWT worksheet from row 60; the institution field and dedicated MoFPED sheet establish ownership. No claim of intentional misconduct is needed in the report."
    },
    "AD13": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "MoFPED worksheet, row 82",
          "selected_cells": {
            "2": "Office Chair 1400D * 600MM",
            "4": "Budget Policy and Evaluation Dep't-UGIFT-MOFPED",
            "6": "Chair",
            "7": "Office Chairs Dimension W700HX Black",
            "9": "UGIFT-BPED/CHR/23-01",
            "17": "",
            "18": "All furniture was left in the old building since the new building where Ugift staff were transferred had its own new furniture and fixtures.\n\nThe old items were left in store and others distributed to offices were we did not have access to.",
            "19": "MOFPED"
          }
        }
      ],
      "audit_note": "The remark describes furniture collectively. Do not state a total quantity or that all furniture is idle: some was redistributed and access was not obtained. Duplicate text at MoWT row 139 still belongs to MoFPED."
    },
    "AD14": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "OPM worksheet, row 3",
          "selected_cells": {
            "1": "HP Laptop Envy i3",
            "3": "LG M & E",
            "4": "CND1518LXZ",
            "5": "HP Laptop",
            "6": "HP Envy i3-BA1073NE",
            "8": "UGIFT-LGMSD/LT/22-01",
            "16": "fair condition",
            "17": "This laptop though of good quality, its capacity is lower than the volume of work that the officer handles."
          }
        },
        {
          "locator": "OPM worksheet, row 4",
          "selected_cells": {
            "1": "HP Laptop Envy i3",
            "3": "LG M & E",
            "4": "CND1518LX4",
            "5": "HP Laptop",
            "6": "HP Envy i3-BA1073NE",
            "8": "UGIFT-LGMSD/LT/22-02",
            "16": "fair condition",
            "17": "This laptop though of good quality, its capacity is lower than the volume of work that the officer handles."
          }
        },
        {
          "locator": "OPM worksheet, row 5",
          "selected_cells": {
            "1": "HP Laptop Envy i3",
            "3": "LG M & E",
            "4": "CND1518LX6",
            "5": "HP Laptop",
            "6": "HP Envy i3-BA1073NE",
            "8": "UGIFT-LGMSD/LT/22-03",
            "16": "fair condition",
            "17": "This laptop though of good quality, its capacity is lower than the volume of work that the officer handles."
          }
        },
        {
          "locator": "OPM worksheet, row 6",
          "selected_cells": {
            "1": "HP Laptop Envy i3",
            "3": "LG M & E",
            "4": "CND1518LYJ",
            "5": "HP Laptop",
            "6": "HP Envy i3-BA1073NE",
            "8": "UGIFT-LGMSD/LT/22-04",
            "16": "fair condition",
            "17": "This laptop though of good quality, its capacity is lower than the volume of work that the officer handles."
          }
        }
      ],
      "audit_note": "This is a user assessment of capacity relative to workload, separate from the damaged unused laptops already in the report. Do not invent a benchmark test or the particular software involved."
    },
    "AD15": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "MoWT worksheet, row 5",
          "selected_cells": {
            "2": "Kyocera 5054ci Photocopier",
            "4": "MoWT-Department of Public Structures",
            "6": "",
            "7": "Taskalfa 5004i",
            "9": "UGIFT-MOWT/PHC/22-01",
            "17": "Delivered, installed \nand well functioning",
            "18": "The UGIFT secretariat at \nthe MoWT are able to carryout their work smoothly using these Printers",
            "19": "MOWT"
          }
        },
        {
          "locator": "MoWT worksheet, row 34",
          "selected_cells": {
            "2": "Huwaei Video ConferencingEquipment",
            "4": "MoWT-Department of Public Structures",
            "6": "2155151014XHQ6000271",
            "7": "Huawei Video conferencing equipment; 65'' smart screen, microphones, speaker and touch pens",
            "9": "Not engraved",
            "17": "Delivered, Installed and Functioning",
            "18": "The equipment was not recorded in the UGIFT asset register provided by the Ministry of Finance and not engraved because of its appearance and ……..",
            "19": "MOWT"
          }
        }
      ],
      "audit_note": "Use direct delivered/installed/functioning and engraving observations. The apparently future service date on row 5 is not repeated. Do not attribute the MoFPED section copied later in this worksheet to MoWT."
    },
    "AD16": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "MoH worksheet, row 3",
          "selected_cells": {
            "2": "Printer",
            "4": "Engineering",
            "6": "Newly purchased ICT equipment",
            "7": "Kyocera Heavy duty Colour Copier & Printer - MoH - Industrial area office",
            "9": "TASKalfa 4053Ci",
            "17": "In user & good condition",
            "18": "Not engraved",
            "19": "MoH"
          }
        },
        {
          "locator": "MoH worksheet, row 4",
          "selected_cells": {
            "2": "Printer",
            "4": "RBF",
            "6": "Newly purchased ICT equipment",
            "7": "Kyocera Heavy duty Colour Copier & Printer - MoH - H/Q - Mainbuilding",
            "9": "TASKalfa 6003Ci",
            "17": "In user & good condition",
            "18": "Not engraved",
            "19": "MoH"
          }
        },
        {
          "locator": "MoH worksheet, row 16",
          "selected_cells": {
            "2": "Laptop",
            "4": "RBF",
            "6": "Newly purchased ICT equipment",
            "7": "Lenova Laptop - MoH - H/Q - Mainbuilding",
            "9": "No engravement",
            "17": "In user & good condition",
            "18": "",
            "19": "MoH"
          }
        }
      ],
      "audit_note": "The finding is limited to the two identified printers and one laptop. Other laptops have programme engravings. It is not a ministry-wide assertion that all equipment is unmarked."
    },
    "AD17": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "NEMA worksheet, row 2",
          "selected_cells": {
            "1": "Computer",
            "3": "Exective Directors office",
            "4": "Not engraved",
            "5": "Lenovo Think pad i7",
            "6": "Computer",
            "8": "None",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "NEMA worksheet, row 3",
          "selected_cells": {
            "1": "Computer",
            "3": "Environment Audit",
            "4": "Not engraved",
            "5": "Lenovo Think pad i7",
            "6": "Computer",
            "8": "None",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "NEMA worksheet, row 4",
          "selected_cells": {
            "1": "Computer",
            "3": "Environal Audit",
            "4": "Not engraved",
            "5": "Lenovo Think pad i7",
            "6": "Computer",
            "8": "None",
            "16": "Funtional",
            "17": ""
          }
        },
        {
          "locator": "NEMA worksheet, row 5",
          "selected_cells": {
            "1": "Computer",
            "3": "Environmental Audit",
            "4": "Not engraved",
            "5": "Lenovo Think pad i7",
            "6": "Computer",
            "8": "None",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "NEMA worksheet, row 6",
          "selected_cells": {
            "1": "Printer",
            "3": "Nema General",
            "4": "Not engraved",
            "5": "Kyocera TASK 5054ci",
            "6": "Heavy duty printer",
            "8": "None",
            "16": "Funtional",
            "17": ""
          }
        }
      ],
      "audit_note": "The five listed items are four laptops and one printer. The status wording is direct in the inspection return, not the later default condition classification. No claim about all authority holdings is made."
    },
    "AD18": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "MoWE worksheet, row 703",
          "selected_cells": {
            "1": "Apple Tablets",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "8": "Not Engraved",
            "16": "",
            "17": ""
          }
        },
        {
          "locator": "MoWE worksheet, row 704",
          "selected_cells": {
            "1": "Apple Tablets",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "8": "Not Engraved",
            "16": "",
            "17": ""
          }
        },
        {
          "locator": "MoWE worksheet, row 705",
          "selected_cells": {
            "1": "Apple Tablets",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "8": "Not Engraved",
            "16": "",
            "17": ""
          }
        },
        {
          "locator": "MoWE worksheet, row 706",
          "selected_cells": {
            "1": "Apple Tablets",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "8": "Not Engraved",
            "16": "",
            "17": ""
          }
        },
        {
          "locator": "MoWE worksheet, row 707",
          "selected_cells": {
            "1": "Apple Tablets",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "8": "Not Engraved",
            "16": "",
            "17": ""
          }
        },
        {
          "locator": "MoWE worksheet, row 708",
          "selected_cells": {
            "1": "Apple Tablets",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "8": "Not Engraved",
            "16": "",
            "17": ""
          }
        },
        {
          "locator": "MoWE worksheet, row 709",
          "selected_cells": {
            "1": "Apple Tablets",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "8": "Not Engraved",
            "16": "",
            "17": ""
          }
        },
        {
          "locator": "MoWE worksheet, row 710",
          "selected_cells": {
            "1": "Apple Tablets",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "8": "Not Engraved",
            "16": "",
            "17": ""
          }
        },
        {
          "locator": "MoWE worksheet, row 711",
          "selected_cells": {
            "1": "Apple Tablets",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "8": "Not Engraved",
            "16": "",
            "17": ""
          }
        },
        {
          "locator": "MoWE worksheet, row 712",
          "selected_cells": {
            "1": "Apple Tablets",
            "3": "",
            "4": "",
            "5": "",
            "6": "",
            "8": "Not Engraved",
            "16": "",
            "17": ""
          }
        }
      ],
      "audit_note": "Ten separate one-unit Apple tablet rows explicitly say Not Engraved. Their functionality cells are blank, so no assertion about use, performance or condition is supported."
    }
  }
}
```


## Revision evidence: narrative/national_supporting_descriptions.json

```json
{
  "MAAIF BK": {
    "paragraphs": [
      "The ministry had working laptops and printers carrying programme asset identifiers. Keeping those identifiers linked to the equipment and its custodian will support continued accountability after programme closure. Routine condition checks should identify new faults and keep usable equipment in service."
    ],
    "private_audit": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "MAAIF worksheet, row 4",
          "selected_cells": {
            "2": "Laptops",
            "4": "",
            "6": "PF3VD5K3-LAPTOP",
            "7": "LENOVO THINKPAD 11TH GEN INTEL® CORE TM(I7) 2.8GHZ 16GRAM ROM 1T",
            "9": "UGIFT-MAAIF/LT/23-04",
            "17": "Good working condition",
            "18": "",
            "19": "MAAIF"
          }
        },
        {
          "locator": "MAAIF worksheet, row 5",
          "selected_cells": {
            "2": "Laptops",
            "4": "",
            "6": "PF3V8R8L-",
            "7": "LENOVO THINKPAD 11TH GEN INTEL® CORE TM(I7) 2.8GHZ 16GRAM ROM 1T",
            "9": "UGIFT-MAAIF/LT/23-02",
            "17": "Good working condition",
            "18": "",
            "19": "MAAIF"
          }
        },
        {
          "locator": "MAAIF worksheet, row 6",
          "selected_cells": {
            "2": "Laptops",
            "4": "",
            "6": "PF3V8R85",
            "7": "LENOVO THINKPAD 11TH GEN INTEL® CORE TM(I7) 2.8GHZ 16GRAM ROM 1T",
            "9": "UGIFT-MAAIF/LT/23-01",
            "17": "Good working condition",
            "18": "",
            "19": "MAAIF"
          }
        },
        {
          "locator": "MAAIF worksheet, row 7",
          "selected_cells": {
            "2": "Laptops",
            "4": "",
            "6": "PF3TR6E8",
            "7": "LENOVO THINKPAD 11TH GEN INTEL® CORE TM(I7) 2.8GHZ 16GRAM ROM 1T",
            "9": "UGIFT-MAAIF/LT/23-03",
            "17": "Good working condition",
            "18": "",
            "19": "MAAIF"
          }
        },
        {
          "locator": "MAAIF worksheet, row 205",
          "selected_cells": {
            "2": "Printers",
            "4": "",
            "6": "",
            "7": "HP LaserJet Pro MFP 4103fdw - Black",
            "9": "UGIFT-MAAIF/PR/25/001",
            "17": "Good working condition",
            "18": "",
            "19": "MAAIF"
          }
        },
        {
          "locator": "MAAIF worksheet, row 206",
          "selected_cells": {
            "2": "Printers",
            "4": "",
            "6": "",
            "7": "HP LaserJet Pro MFP 4103fdw - Black",
            "9": "UGIFT-MAAIF/PR/25/002",
            "17": "Good working condition",
            "18": "",
            "19": "MAAIF"
          }
        },
        {
          "locator": "MAAIF worksheet, row 207",
          "selected_cells": {
            "2": "Printers",
            "4": "",
            "6": "",
            "7": "HP LaserJet Pro MFP 4103fdw - Black",
            "9": "UGIFT-MAAIF/PR/25/003",
            "17": "Good working condition",
            "18": "",
            "19": "MAAIF"
          }
        },
        {
          "locator": "MAAIF worksheet, row 208",
          "selected_cells": {
            "2": "Printers",
            "4": "",
            "6": "",
            "7": "HP LaserJet Pro MFP 4103fdw - color",
            "9": "UGIFT-MAAIF/PR/25/004",
            "17": "Good working condition",
            "18": "",
            "19": "MAAIF"
          }
        },
        {
          "locator": "MAAIF worksheet, row 209",
          "selected_cells": {
            "2": "Printers",
            "4": "",
            "6": "",
            "7": "HP LaserJet Pro MFP 4103fdw - color",
            "9": "UGIFT-MAAIF/PR/25/005",
            "17": "Good working condition",
            "18": "",
            "19": "MAAIF"
          }
        },
        {
          "locator": "MAAIF worksheet, row 210",
          "selected_cells": {
            "2": "Printers",
            "4": "",
            "6": "",
            "7": "Kyocera Taskalfa 6003i Multifunction Monochrome Printer (Print/Scan/Copy/Fax),",
            "9": "UGIFT-MAAIF/PH/25/01",
            "17": "Good working condition",
            "18": "",
            "19": "MAAIF"
          }
        }
      ],
      "note": "Direct condition and tag fields support this positive example. It is not a claim that every MAAIF asset was tested or that an existing maintenance programme was demonstrated. The first four laptop rows and six printer/copier rows provide examples rather than a total of all holdings."
    }
  },
  "MGLSD BK": {
    "paragraphs": [
      "Laptops serving Finance and Administration were functional and engraved. Two tablets, one for Finance and Administration and the other for Youth and Children Affairs, were functional but unengraved. The ministry should mark the tablets and link their identifiers to the units and officers responsible for them."
    ],
    "private_audit": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "MoGLSD worksheet, row 3",
          "selected_cells": {
            "1": "Computer",
            "3": "Finance and Administration",
            "4": "Engraved",
            "5": "Lenovo ThinkBook Laptop 14 Gi7 IML-21MR",
            "6": "Computer",
            "8": "008/UGIFT/LT/001",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoGLSD worksheet, row 4",
          "selected_cells": {
            "1": "Computer",
            "3": "Finance and Administration",
            "4": "Engraved",
            "5": "Lenovo ThinkBook Laptop 14 Gi7 IML-21MR",
            "6": "Computer",
            "8": "008/UGIFT/LT/002",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoGLSD worksheet, row 5",
          "selected_cells": {
            "1": "Computer",
            "3": "Finance and Administration",
            "4": "Engraved",
            "5": "Lenovo ThinkBook Laptop 14 Gi7 IML-21MR",
            "6": "Computer",
            "8": "008/UGIFT/LT/003",
            "16": "Funtional",
            "17": ""
          }
        },
        {
          "locator": "MoGLSD worksheet, row 6",
          "selected_cells": {
            "1": "Computer",
            "3": "Finance and Administration",
            "4": "Engraved",
            "5": "Lenovo ThinkBook Laptop 14 Gi7 IML-21MR",
            "6": "Computer",
            "8": "008/UGIFT/LT/004",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoGLSD worksheet, row 7",
          "selected_cells": {
            "1": "Tablet",
            "3": "Finance and Administration",
            "4": "Not Engraved",
            "5": "Samsung galaxy Tab A7 light",
            "6": "Tablet",
            "8": "None",
            "16": "Funtional",
            "17": ""
          }
        },
        {
          "locator": "MoGLSD worksheet, row 8",
          "selected_cells": {
            "1": "Tablet",
            "3": "Youth and Children affairs",
            "4": "Not Engraved",
            "5": "Samsung galaxy Tab A7 light",
            "6": "Tablet",
            "8": "None",
            "16": "Funtional",
            "17": ""
          }
        }
      ],
      "note": "Four laptop rows explicitly say Engraved; two tablet rows explicitly say Not Engraved. Both classes have direct functional statuses. Source purchase dates advance by one year per row and include future years; those dates are not used."
    }
  },
  "PPDA BK": {
    "paragraphs": [
      "The authority had functioning laptops, a tablet and a printer assigned to its legal and strategy/planning units. These items carried programme identifiers. The authority should keep the identifiers linked to current custodians and update custody whenever equipment moves between units."
    ],
    "private_audit": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "PPDA worksheet, row 2",
          "selected_cells": {
            "1": "Lenovo Thinkpad Notebook P14s",
            "3": "Legal",
            "4": "",
            "5": "Lenovo Notebook P14s",
            "6": "Computer",
            "8": "UGFT-PPDA/LT/24-01",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "PPDA worksheet, row 3",
          "selected_cells": {
            "1": "Lenovo Thinkpad Notebook P14s",
            "3": "Strategy/Planning",
            "4": "",
            "5": "Lenovonote book P14s",
            "6": "Computer",
            "8": "UGFT-PPDA/LT/24/02",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "PPDA worksheet, row 4",
          "selected_cells": {
            "1": "Lenovo Thinkpad Notebook P14s",
            "3": "Strategy/Planning",
            "4": "",
            "5": "Lenovo Notebook P14s",
            "6": "Computer",
            "8": "UGFT-PPDA/LT/24-03",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "PPDA worksheet, row 5",
          "selected_cells": {
            "1": "Samsung Galaxy Tab S9 Ultra",
            "3": "Strategy/Planning",
            "4": "",
            "5": "Samsung Galaxy Tab S9 Ultra Tablet",
            "6": "Tab",
            "8": "UGFT-PPDA/TB/24-01",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "PPDA worksheet, row 6",
          "selected_cells": {
            "1": "HP Laserjet Pro MFP Printer",
            "3": "Legal",
            "4": "",
            "5": "Printer",
            "6": "HP Laserjet Pro MFP Printer-4103fdw",
            "8": "UGFT-PPDA/PRT/24-01",
            "16": "Functional",
            "17": ""
          }
        }
      ],
      "note": "Three laptops, one tablet and one printer are explicitly functional with UgIFT identifiers in the inspection return. No claim is made about procurement efficiency or other measured service outcomes. This prose describes the items directly rather than the master register category split of three Other and two ICT entries."
    }
  },
  "OAG BK": {
    "paragraphs": [
      "The office had working laptops, printers and two pickup vehicles. The pickups had changed registration numbers. The office should retain the link between the earlier and current registrations, the chassis numbers and the assigned custodians so that each vehicle remains traceable."
    ],
    "private_audit": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "OAG worksheet, row 3",
          "selected_cells": {
            "1": "Laptop",
            "3": "Office of the Auditor General",
            "4": "FM2YR14",
            "5": "Dell XPS 15 I7 Laptop",
            "6": "Dell XPS 15 9530 I7 13TH Gen 32GB 1TB Win 11 PRO",
            "8": "UGIFT-OAG-HQT-LT-24-081",
            "16": "Well Functioning",
            "17": ""
          }
        },
        {
          "locator": "OAG worksheet, row 4",
          "selected_cells": {
            "1": "Laptop",
            "3": "Office of the Auditor General",
            "4": "31WXR14",
            "5": "Dell XPS 15 I7 Laptop",
            "6": "Dell XPS 15 9530 I7 13TH Gen 32GB 1TB Win 11 PRO",
            "8": "UGIFT-OAG-HQT-LT-24-092",
            "16": "Well Functioning",
            "17": ""
          }
        },
        {
          "locator": "OAG worksheet, row 5",
          "selected_cells": {
            "1": "Laptop",
            "3": "Office of the Auditor General",
            "4": "4WTYR14",
            "5": "Dell XPS 15 I7 Laptop",
            "6": "Dell XPS 15 9530 I7 13TH Gen 32GB 1TB Win 11 PRO",
            "8": "UGIFT-OAG-HQT-LT-24-093",
            "16": "Well Functioning",
            "17": ""
          }
        },
        {
          "locator": "OAG worksheet, row 16",
          "selected_cells": {
            "1": "Printer",
            "3": "Office of the Auditor General",
            "4": "CZBBT4J0FH",
            "5": "HP Color Printer",
            "6": "HP Colored Laserjet Printer MFP 5800dn",
            "8": "OAG-HQT-PRT-25-011",
            "16": "Well Functioning",
            "17": ""
          }
        },
        {
          "locator": "OAG worksheet, row 17",
          "selected_cells": {
            "1": "Printer",
            "3": "Office of the Auditor General",
            "4": "CZBBT4618L",
            "5": "HP Color Printer",
            "6": "HP Colored Laserjet Printer MFP 5800dn",
            "8": "OAG-HQT-PRT-25-012",
            "16": "Well Functioning",
            "17": ""
          }
        },
        {
          "locator": "OAG worksheet, row 18",
          "selected_cells": {
            "1": "Vechicle",
            "3": "",
            "4": "GUN126R-D77HX",
            "5": "Toyota Hilux Double Cabin",
            "6": "MROBA3CD300170246 GUN126R-D77HX, Eng. No. 1GD5308162, Yr of Man. 2023 Eng Cap. 2755cc, Color; Grey Metallic",
            "8": "UG2300011",
            "16": "Well Functioning",
            "17": "There was change in the number plate"
          }
        },
        {
          "locator": "OAG worksheet, row 19",
          "selected_cells": {
            "1": "Vechicle",
            "3": "",
            "4": "GUN126R-D77HX",
            "5": "Toyota Hilux Double Cabin",
            "6": "MROBA3CD400169364,GUN126R-D77HX, Eng. No. 1GD5313181, Yr of Man. 2023 Eng Cap. 2755cc, Color; Grey Metallic",
            "8": "UG2300054",
            "16": "Well Functioning",
            "17": "There was change in the number plate"
          }
        }
      ],
      "note": "Rows 3–5 are laptop examples, rows 16–17 printer examples, and rows 18–19 the pickups. Both pickup remarks explicitly record changed number plates. Working condition comes from the direct inspection entries rather than a later default classification. No particular former registration is invented."
    }
  },
  "MOLG BK": {
    "paragraphs": [
      "The District Administration unit had a working pickup, photocopier and computer equipment. Two laptops and a desktop set, including its keyboard and mouse, lacked engraving. The ministry should mark the unengraved equipment and confirm its location and custodian while keeping the working assets in service."
    ],
    "private_audit": {
      "path": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
      "excerpts": [
        {
          "locator": "MoLG worksheet, row 2",
          "selected_cells": {
            "1": "VECHICLES",
            "3": "District Administration",
            "4": "ACVDSCJRXJ4027187",
            "5": "Motor Vechicle",
            "6": "Pick up-Double cabin",
            "8": "UG3400003",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoLG worksheet, row 3",
          "selected_cells": {
            "1": "Copier",
            "3": "District Administration",
            "4": "",
            "5": "Heavy Duty Photocopier",
            "6": "Kyocera Tasklafa Copier 6054CI-MFP",
            "8": "UGIFT-MOLG/PHC/23-01",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoLG worksheet, row 4",
          "selected_cells": {
            "1": "Computer",
            "3": "District Administration",
            "4": "",
            "5": "Lenovo Think Monitor",
            "6": "ThinkVision 27inch M70t Gen3 Monitor",
            "8": "UGFT-MOLG/MON/24-01",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoLG worksheet, row 5",
          "selected_cells": {
            "1": "Computer",
            "3": "District Administration",
            "4": "",
            "5": "Keyboard",
            "6": "Lenovo Kyboard",
            "8": "UGFT-MOLG/KB/24-01",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoLG worksheet, row 6",
          "selected_cells": {
            "1": "Computer",
            "3": "District Administration",
            "4": "",
            "5": "CPU",
            "6": "Lenovo ThinkCentre neo 50t Gen 4 Core i7-13700,1TB, 11 Pro",
            "8": "UGFT-MOLG/CPU/24-01",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoLG worksheet, row 7",
          "selected_cells": {
            "1": "Laptop",
            "3": "District Administration",
            "4": "",
            "5": "Lenovo Notebook Thinkbook-14, Yoga Gen3, Bag, Wireless Mouse",
            "6": "Lenovo Notebook Thinkbook",
            "8": "UGFT-MOLG/LT/24-01",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoLG worksheet, row 8",
          "selected_cells": {
            "1": "Laptop",
            "3": "District Administration",
            "4": "",
            "5": "Lenovo Notebook Thinkbook-14, Yoga Gen3, Bag, Wireless Mouse",
            "6": "Lenovo Notebook Thinkbook",
            "8": "UGFT-MOLG/LT/24-02",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoLG worksheet, row 9",
          "selected_cells": {
            "1": "Laptop",
            "3": "District Administration",
            "4": "",
            "5": "Lenovo Thinkpad",
            "6": "Lenovo Thinkpad Laptop",
            "8": "Not engraved",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoLG worksheet, row 10",
          "selected_cells": {
            "1": "Laptop",
            "3": "District Administration",
            "4": "",
            "5": "HP Spectre X360",
            "6": "HP Spectre X360 Laptop",
            "8": "Not engraved",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoLG worksheet, row 11",
          "selected_cells": {
            "1": "Computer",
            "3": "District Administration",
            "4": "",
            "5": "HP all-in-One Desktop",
            "6": "HP all-in-One Desktop -13th Gen Corei7-1355u, 16GB",
            "8": "Not engraved",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoLG worksheet, row 12",
          "selected_cells": {
            "1": "Computer",
            "3": "District Administration",
            "4": "",
            "5": "Keyboard",
            "6": "HP Keyboard",
            "8": "Not engraved",
            "16": "Functional",
            "17": ""
          }
        },
        {
          "locator": "MoLG worksheet, row 13",
          "selected_cells": {
            "1": "Computer",
            "3": "District Administration",
            "4": "",
            "5": "Mouse",
            "6": "HP Mouse",
            "8": "Not engraved",
            "16": "Functional",
            "17": ""
          }
        }
      ],
      "note": "Rows 2–8 describe working transport/office equipment with identifiers. Rows 9–13 explicitly say Not engraved and Functional: two laptops plus desktop, keyboard and mouse. The finding applies to these five items, not to all ministry assets."
    }
  }
}
```


## Revision evidence: reconciliation/revision_field_cases.json

```json
{
  "purpose": "Report-ready field findings for the user-requested expectations/found/gaps/actions revision. Prose fields contain no raw file references; provenance fields are private source-log material.",
  "overview_paragraphs": [
    "The exercise accounted for all 629 entries on the verification master list: 258 schools and 371 health centres. Facility evidence or identifiable consolidated asset entries supported 589; documented explanations accounted for the remaining 40. Accounting for every entry does not mean that every facility or every asset was physically inspected.",
    "The field findings show why construction, equipment delivery and operational readiness need to be considered separately. Some listed facilities were not constructed or were incorrectly named; others had been replaced or held their assets at another site. At several schools and health centres, unfinished works, delayed installation, defects or incomplete handover prevented the supplied assets from serving their intended purpose.",
    "Reconciliation identified 10 entries reported nonexistent or not constructed, four replacements, 30 name corrections, three institutions outside UgIFT, three cases of relocated assets and five existing facilities without UgIFT assets. These 55 explanations are part of the master-list account and overlap the evidence-backed entries; they are not 55 additional facilities or a separate physical-verification total.",
    "Returns also named 24 facilities outside the matched master list. This is a count of unmatched return identities, not proof of 24 additional physical facilities or completed projects. Rukoki General Hospital, Silumira Health Centre III and Bukuuku Community Seed Secondary School were expressly confirmed as additional beneficiaries. Other returns need their identities and programme scope resolved, and one expressly states that physical verification did not take place.",
    "Engraving needs to identify the individual asset, not only the programme or institution. The teams found both unmarked equipment and programme-marked items without unique numbers. The follow-up should connect every durable mark to an inventory entry and a named custodian, while completing installation, handover and repair actions that bring the assets into use."
  ],
  "coverage_provenance": [
    {
      "source": "raw-data-grouped/README.md",
      "locator": "Master-list coverage and verification-status sections",
      "supports": "632 source rows, 629 distinct master identities; 548 facility material plus 41 consolidated entries; 40 reconciled explanations."
    },
    {
      "source": "raw-data-grouped/facility-data-status.pdf",
      "locator": "pages 1 and 5",
      "supports": "Coverage counts and limitation that return completion is not physical-verification certification."
    },
    {
      "source": "tmp/narrative-report/reconciliation/reconciliation_data.json",
      "locator": "coverage; selected_reconciliation; ground_return_identities",
      "supports": "Deterministic reconciliation extraction and exact record locators."
    }
  ],
  "programme_closure_comparison": {
    "reference_date": "Programme closure in December 2025; not the September 2026 verification date",
    "schools": {
      "programme_total": 259,
      "reported_complete": 196,
      "reported_operational": 189,
      "outside_reported_complete_total_derived": 63,
      "complete_but_not_reported_operational_derived": 7
    },
    "health_facility_works": {
      "programme_total": 373,
      "reported_complete": 354,
      "outside_reported_complete_total_derived": 19
    },
    "verification_scope": {
      "schools": 258,
      "health_centres": 371,
      "total": 629
    },
    "report_ready": "At programme closure in December 2025, 196 of 259 seed schools were reported complete and 189 were operational; 354 of 373 health-facility works were reported complete. This left 63 schools and 19 health works outside the reported completed totals, with seven completed schools not reported operational. Those closure figures describe an earlier programme scope. The subsequent verification used a separate list of 258 schools and 371 health centres; the two sets should not be treated as one denominator or as a September 2026 completion count.",
    "expected": "The programme totals provide the closure-output baseline against which reported completion can be compared.",
    "gap": "Construction completion had not reached the stated programme totals at closure, and completion did not always mean operation. There is no supplied item-level bridge between those totals and the later verification master.",
    "action": "The sector ministries should reconcile the closure-output schedule to the current beneficiary list, confirm the status of each unfinished or non-operational project, and assign dated completion and operational-readiness actions.",
    "arithmetic": [
      "259 - 196 = 63",
      "373 - 354 = 19",
      "196 - 189 = 7"
    ],
    "provenance": [
      {
        "source": "outputs/report-templates/Verification report_ 24092026_Draft_ BB.docx",
        "locator": "paragraph 13",
        "supports": "Programme ended 31 December 2025."
      },
      {
        "source": "outputs/report-templates/Verification report_ 24092026_Draft_ BB.docx",
        "locator": "paragraphs 67 and 70–71",
        "supports": "Introduces outputs accomplished at December 2025 closure and supplies 196/259, 189, and 354/373."
      }
    ],
    "limits": [
      "The supplied draft is the source for the closure summary; underlying completion certificates and a project-by-project bridge were not supplied in these extracts.",
      "Use programme total or closure-output total rather than a contractual completion target unless the approved target instrument is separately cited.",
      "The arithmetic is transparent, but the 63 and 19 are not independently reverified September 2026 counts.",
      "Do not infer that all 63 schools or all 19 health works remained unfinished at the verification date.",
      "Do not reconcile the 259/373 programme totals to 258/371 verification identities merely by subtracting names; scope and deduplication require an item-level bridge."
    ]
  },
  "cases": [
    {
      "case_id": "F01",
      "theme": "Listed complete but not constructed",
      "facility": "Olok Health Centre",
      "lg": "Pader",
      "record_ids": [
        "H205"
      ],
      "expected": "Olok was listed as a completed health facility.",
      "expectation_basis": "Documented programme schedule status: Complete.",
      "found": "The district health officer confirmed to the verification team that Olok Health Centre had not been constructed and did not exist in the district.",
      "gap": "A completed entry could not be matched to the intended health facility. This is a facility-delivery discrepancy, not simply a missing asset return.",
      "action": "Pader District and the Ministry of Health should reconcile the approved project, construction and payment records, document the outcome, and correct the beneficiary schedule. They should decide how the intended service need will be met.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 74; id=H205",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Combined Olok HC / Latanya school report records the DHO saying Olok HC does not exist and was not constructed. Latanya school is separate. Field report says not constructed"
        },
        {
          "source": "raw-data-grouped/team-04/Pader/Olok-HC-III/1 Olok HC -Latanya SSS - Pader District.docx",
          "locator": "paragraphs 61–62; table 2, row 1",
          "supports": "DHO reports that Olok does not exist and was not constructed."
        }
      ],
      "interpretation_limit": "The source is a recorded DHO confirmation. It does not establish the reason for non-construction, expenditure irregularity, or a funding loss."
    },
    {
      "case_id": "F02",
      "theme": "Invalid facility identity",
      "facility": "Busia Eastern Division health-centre entry",
      "lg": "Busia Municipal Council",
      "record_ids": [
        "H070",
        "X900"
      ],
      "expected": "Each beneficiary entry should identify a particular health facility.",
      "expectation_basis": "Intended purpose of the facility schedule; H070 is a listed completed entry.",
      "found": "Reconciliation confirmed that no health facility called Busia Eastern Division existed. A separate return identifies Sofia Health Centre III within Eastern Division.",
      "gap": "The administrative division was used as a facility name. The evidence does not establish that Sofia is an alias or replacement for that entry.",
      "action": "The municipality and Ministry of Health should resolve the beneficiary identity and retain Sofia separately until an approved link is documented.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 227; id=H070",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Does not exist. Sofia Health Centre III is a separately named field return in Eastern Division and is not treated as an alias for this invalid master label. Reported not to exist; programme data-management decision"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 23; id=CHAT19; 2026-09-23 02:39",
          "supports": "The master list shows a health centre called Busia Eastern Division. No such facility exists. Audit: Sofia Health Centre III is a separately named field return in Eastern Division and is not treated as an alias for this invalid master label."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 645; id=X900",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return identifies Sofia Health Centre III in Eastern Division, Busia Municipal Council. It is distinct from the invalid master label Busia Eastern Division."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 23; id=CHAT19; 2026-09-23 02:39",
          "supports": "The master list shows a health centre called Busia Eastern Division. No such facility exists. Audit: Sofia Health Centre III is a separately named field return in Eastern Division and is not treated as an alias for this invalid master label."
        }
      ],
      "interpretation_limit": "Do not substitute Sofia for H070 merely because it lies in Eastern Division; do not describe Sofia as a newly constructed facility solely from this return."
    },
    {
      "case_id": "F03",
      "theme": "Other named facilities not found",
      "facility": "Kishangara Seed Secondary School and Butoloogo Health Centre",
      "lg": "Ibanda and Kasanda",
      "record_ids": [
        "S216",
        "H010"
      ],
      "expected": "The two facilities were listed as completed programme beneficiaries.",
      "expectation_basis": "Documented master schedule statuses: Complete.",
      "found": "Programme reconciliation confirmed that Kishangara Seed Secondary School did not exist in Ibanda and that there was no health facility called Butoloogo in Kasanda.",
      "gap": "Neither listed identity has a confirmed replacement in the supplied evidence.",
      "action": "The responsible local governments and sector ministries should resolve the original project identities, retain the decisions in the closure record, and remove invalid names from the active beneficiary list.",
      "priority": "supporting",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 386; id=S216",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; The programme data manager confirms that Kishangara Seed Secondary School does not exist in Ibanda. Preserve the master row for audit and do not infer a replacement facility. Reported not to exist; programme data-management decision"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 70; id=USER03; 2026-09-24 15:15",
          "supports": "Kishangara Seed Secondary School does not exist in Ibanda. Audit: Direct programme data-management instruction. Preserve master entry S216 as an audit record, mark it reported absent, and do not create or infer a replacement facility."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 564; id=H010",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Depaul said on 24 September 2026 that there is no health facility called Butoloogo Health Centre III in Kasanda. No replacement is inferred. Not established"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 74; id=CHAT45D; 2026-09-24 17:51",
          "supports": "There is no health facility called butoloogo health centre III in kasanda district Audit: Reported absent. No replacement facility is inferred."
        }
      ],
      "interpretation_limit": "These are explicit reconciliation confirmations, not claims that the teams physically searched every possible location."
    },
    {
      "case_id": "F04",
      "theme": "Beneficiary replacements",
      "facility": "Ngomoromo, Oweko, Musandama and Loinya health centres",
      "lg": "Lamwo, Nebbi, Ntoroko and Maracha",
      "record_ids": [
        "H150",
        "H218",
        "H354",
        "H213"
      ],
      "expected": "The programme schedule should identify the facilities that actually received the intended investment.",
      "expectation_basis": "Intended purpose of the beneficiary schedule; original entries are retained for accountability.",
      "found": "Supervisors confirmed that Pangira replaced Ngomoromo, Pamaka replaced Oweko, Butungama replaced Musandama, and Liko replaced Loinya. Liko was already included elsewhere on the master list.",
      "gap": "The original and receiving names were not consistently linked, creating a risk of counting one investment twice or treating a replacement as an unexplained omission.",
      "action": "Attach the approved replacement decisions to the beneficiary schedule, link each original entry to its recipient, and count the receiving facility once.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 69; id=H150",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Replaced. Chat spelling Ngoromoro matched to master Ngomoromo. Replacement decision does not itself prove physical verification."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 1; id=CHAT01; 2026-09-21 16:29",
          "supports": "Ngoromoro HC in Lamwo was replaced by Pangira HC in Lamwo. Audit: Chat spelling Ngoromoro matched to master Ngomoromo. Replacement decision does not itself prove physical verification."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 2; id=H218",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Supervisor confirms that Oweko was replaced by Pamaka Health Centre III. The Pamaka return is retained as the receiving-facility evidence. Supervisor-confirmed asset relocation/replacement; field evidence is counted under the receiving facility"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 30; id=CHAT21D; 2026-09-23 09:36",
          "supports": "Oweko was replaced by Pamaka HC Audit: Oweko was replaced by Pamaka Health Centre III. Count the evidence under Pamaka."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 495; id=H354",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Depaul says Musandama HC III was replaced by Butangama HC III in Ntoroko. The filed return spells the facility Butungama. That return is counted once, on the Musandama master row."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 31; id=CHAT22; 2026-09-23 11:31",
          "supports": "Musandama HCIII was replaced with Butangama HCIII. This was in Ntoroko District Audit: Chat spelling Butangama; the filed return spells Butungama."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 30; id=H213",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Loinya was replaced by Liko, which already has master entry H212. Count Liko once. Already-listed replacement; no second verified facility"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 4; id=CHAT04; 2026-09-21 16:32",
          "supports": "Loinya HC in Maracha District was replaced by Liko HC in Maracha District Audit: Liko HC II is already master row 212 and Loinya row 213. Do not count Liko twice or add it as off-master."
        }
      ],
      "interpretation_limit": "Replacement confirmation does not by itself certify a physical inspection of the recipient."
    },
    {
      "case_id": "F05",
      "theme": "Assets moved to other facilities",
      "facility": "Alangi, Ther-uru and Abanga",
      "lg": "Zombo",
      "record_ids": [
        "H231",
        "H233",
        "S208"
      ],
      "expected": "The location and custodian of programme assets should agree with the receiving facility.",
      "expectation_basis": "Asset-accountability expectation; relocation is documented by the supervisor.",
      "found": "The supervisor confirmed that the three facilities existed, but Alangi assets had moved to Amwonyo Health Centre, Ther-uru assets to Atyak Health Centre, and Abanga school assets to Kango Seed Secondary School.",
      "gap": "The original facility names no longer describe where these assets are held. This is a custody and location issue, not evidence that the assets disappeared.",
      "action": "The district should reconcile the transfer approvals and signed receipts with both the sending and receiving inventories, record the current custodian, and confirm the service arrangements at the original sites.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 14; id=H231",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Supervisor confirms that Alangi exists, but its UgIFT assets were relocated to Amwonyo Health Centre III. Evidence is counted under Amwonyo. Supervisor-confirmed asset relocation/replacement; field evidence is counted under the receiving facility"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 27; id=CHAT21A; 2026-09-23 09:36",
          "supports": "While Alangi HC, Ther-uru HC & Abanga SSS exist, their assets where relocated to Amwonyo HC, Atyak HC & Kango SSS respectively. Audit: Alangi exists, but its UgIFT assets were relocated to Amwonyo Health Centre III. Count the evidence under Amwonyo."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 16; id=H233",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Supervisor confirms that Ther-uru exists, but its UgIFT assets were relocated to Atyak Health Centre III. Evidence is counted under Atyak. Supervisor-confirmed asset relocation/replacement; field evidence is counted under the receiving facility"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 28; id=CHAT21B; 2026-09-23 09:36",
          "supports": "While Alangi HC, Ther-uru HC & Abanga SSS exist, their assets where relocated to Amwonyo HC, Atyak HC & Kango SSS respectively. Audit: Ther-uru exists, but its UgIFT assets were relocated to Atyak Health Centre III. Count the evidence under Atyak."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 17; id=S208",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Supervisor confirms that Abanga Seed Secondary School exists, but its UgIFT assets were relocated to Kango Seed Secondary School. Evidence is counted under Kango. Supervisor-confirmed asset relocation/replacement; field evidence is counted under the receiving facility"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 29; id=CHAT21C; 2026-09-23 09:36",
          "supports": "While Alangi HC, Ther-uru HC & Abanga SSS exist, their assets where relocated to Amwonyo HC, Atyak HC & Kango SSS respectively. Audit: Abanga exists, but its UgIFT assets were relocated to Kango Seed Secondary School. Count the evidence under Kango."
        }
      ],
      "interpretation_limit": "The source confirms relocation but does not establish that transfers were unauthorized or that the original sites have no services."
    },
    {
      "case_id": "F06",
      "theme": "Facilities outside programme scope",
      "facility": "Alira Health Centre and Kiziranfumbi Seed Secondary School",
      "lg": "Oyam and Kikuube",
      "record_ids": [
        "H193",
        "S237"
      ],
      "expected": "The UgIFT beneficiary schedule should include institutions supported by the programme.",
      "expectation_basis": "Documented programme scope reconciliation.",
      "found": "The later Oyam clarification confirmed that Alira existed but was not among the facilities upgraded under UgIFT. Kiziranfumbi Seed Secondary School was also confirmed to be outside UgIFT.",
      "gap": "Programme scope was confused with the existence of the institutions. Alira must not be described as a nonexistent facility.",
      "action": "Remove the two institutions from the active UgIFT beneficiary scope while preserving the original entries and the approved corrections for audit.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 100; id=H193",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; The revised Oyam decision confirms that Alira exists, but it is outside the facilities upgraded under UgIFT. Facility exists but is outside the upgraded UgIFT set"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 21; id=CHAT17; 2026-09-22 17:04",
          "supports": "However on ground the following health centres were upgraded and received UgiFT assets: Ajaga, Icheme (Okwir), Abela, Atura, Loro and Icheme. Whereas Alira HC III exists, it is not part of those that were upgraded to Ugift. Audit: This later clarification supersedes the earlier claim that Alira did not exist. Acimi, Acokara and Ariba remain reported absent; Alira exists but is outside the upgraded UgIFT set. Abeja is corrected to the master-listed Abela."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 472; id=S237",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Depaul said on 24 September 2026 that Kiziranfumbi Seed Secondary School is not under UgIFT and should be excluded. No replacement school is inferred. Not established"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 72; id=CHAT45B; 2026-09-24 16:15",
          "supports": "Kiziranfumbi seed secondary school is not under ugift and so should be excluded from the list Audit: Excluded from the UgIFT list. No replacement school is inferred."
        }
      ],
      "interpretation_limit": "The later Alira clarification supersedes the earlier statement that it did not exist. Do not infer a replacement school for Kiziranfumbi."
    },
    {
      "case_id": "F07",
      "theme": "Existing facilities without UgIFT assets",
      "facility": "Pandwong Health Centre; Bumbaire, Kyamuhunga and Kashenshero schools; Rwamujojo Health Centre",
      "lg": "Kitgum Municipal Council, Bushenyi, Mitooma and Sheema Municipal Council",
      "record_ids": [
        "H149",
        "S214",
        "S215",
        "S221",
        "H282"
      ],
      "expected": "A listed beneficiary should have a supported account of the programme assistance it received.",
      "expectation_basis": "Beneficiary-accountability expectation; all five appear on the master schedule.",
      "found": "Supervisors confirmed that these five institutions existed but had not benefited from UgIFT assets.",
      "gap": "Their presence on the list did not establish asset delivery. The evidence does not show that assets were received and later lost.",
      "action": "The local governments and sector ministries should confirm beneficiary eligibility and delivery records, then either correct the list or document any approved outstanding delivery.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 67; id=H149",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; The supervisor confirms that Pandwong exists but did not receive UgIFT assets. It is therefore excluded from the missing-return count. Facility exists; supervisor reports no UgIFT assets"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 2; id=CHAT02; 2026-09-21 16:29",
          "supports": "Pandwongo HC in Kitgum exists but did not benefit from Ugift assets. Audit: Master identifies Kitgum Mc, chat says Kitgum. Not an absent facility and not verified merely from this message."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 345; id=S214",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Johnson Gumisiriza says Bumbaire SSS did not benefit from UgIFT. The wording is from the 24 September 2026 13:36 screenshot; it is not in the earlier chat export. Facility exists; supervisor reports no UgIFT assets"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 65; id=CHAT44A; 2026-09-24 13:32",
          "supports": "Bumbaire SSS, Kyamuhunga SSS, Kashenshero SSS and Rwamujojo HCIII are did not benefit from Ugift Audit: Johnson Gumisiriza says Bumbaire SSS did not benefit from UgIFT. The wording is from the 24 September 2026 13:36 screenshot; it is not in the earlier chat export."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 346; id=S215",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Johnson Gumisiriza says Kyamuhunga SSS did not benefit from UgIFT. The wording is from the 24 September 2026 13:36 screenshot; it is not in the earlier chat export. Facility exists; supervisor reports no UgIFT assets"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 66; id=CHAT44B; 2026-09-24 13:32",
          "supports": "Bumbaire SSS, Kyamuhunga SSS, Kashenshero SSS and Rwamujojo HCIII are did not benefit from Ugift Audit: Johnson Gumisiriza says Kyamuhunga SSS did not benefit from UgIFT. The wording is from the 24 September 2026 13:36 screenshot; it is not in the earlier chat export."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 351; id=S221",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Johnson Gumisiriza says Kashenshero SSS did not benefit from UgIFT. The wording is from the 24 September 2026 13:36 screenshot; it is not in the earlier chat export. Facility exists; supervisor reports no UgIFT assets"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 67; id=CHAT44C; 2026-09-24 13:32",
          "supports": "Bumbaire SSS, Kyamuhunga SSS, Kashenshero SSS and Rwamujojo HCIII are did not benefit from Ugift Audit: Johnson Gumisiriza says Kashenshero SSS did not benefit from UgIFT. The wording is from the 24 September 2026 13:36 screenshot; it is not in the earlier chat export."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 361; id=H282",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Johnson Gumisiriza says Rwamujojo HC III did not benefit from UgIFT. The wording is from the 24 September 2026 13:36 screenshot; it is not in the earlier chat export. Facility exists; supervisor reports no UgIFT assets"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 68; id=CHAT44D; 2026-09-24 13:32",
          "supports": "Bumbaire SSS, Kyamuhunga SSS, Kashenshero SSS and Rwamujojo HCIII are did not benefit from Ugift Audit: Johnson Gumisiriza says Rwamujojo HC III did not benefit from UgIFT. The wording is from the 24 September 2026 13:36 screenshot; it is not in the earlier chat export."
        }
      ],
      "interpretation_limit": "Report non-receipt of programme benefits as confirmed; do not describe theft, missing delivered assets, or a quantified asset shortfall without delivery evidence."
    },
    {
      "case_id": "F08",
      "theme": "Names and aliases",
      "facility": "Bussi/Zinga and Dabani/Buwumba",
      "lg": "Wakiso and Busia",
      "record_ids": [
        "H054",
        "H065"
      ],
      "expected": "One physical facility should have one stable identity, with former or local names linked to it.",
      "expectation_basis": "Identity-control expectation supported by final reconciliation.",
      "found": "Bussi was confirmed to be the village name for the already-listed Zinga Health Centre. The Buwumba return was reconciled to the master entry named Dabani.",
      "gap": "Different names could be mistaken for additional facilities. These corrections explain identity differences; they do not establish additional construction or service-delivery failures.",
      "action": "Use the confirmed operating name, retain the old name as an alias, and link all asset and project records to one facility identifier.",
      "priority": "supporting",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 602; id=H054",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Direct programme data-management instruction. Bussi is the village; its health centre is Zinga Health Centre III, master entry H052, whose return is filed in team-32/Wakiso/Zinga-HC-III. Keep master entry H054 as an audit record and count the Zinga return once, on H052. No separate Bussi facility is created. Village name for already-listed Zinga Health Centre III (H052); no second facility"
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 91; id=USER04; 2026-09-26",
          "supports": "The master lists indicates: \"Bussi Health Centre III\" but Bussi is the village and the health centre is Zinga Health Centre III whose information is already provided in raw-data-grouped/team-32/Wakiso/Zinga-HC-III Audit: Direct programme data-management instruction. Bussi is the village; its health centre is Zinga Health Centre III, master entry H052, whose return is filed in team-32/Wakiso/Zinga-HC-III. Keep master entry H054 as an audit record and count the Zinga return once, on H052. No separate Bussi facility is created."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 223; id=H065",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; Name corrected. Reconcile the existing Buwumba field return to master entry H065 and do not retain a second off-master Buwumba facility."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 22; id=CHAT18; 2026-09-23 02:31",
          "supports": "Dabani HCIII which is recorded as (Dabani) on the facilities' master list, exists as Buwumba HC III on ground. Audit: Reconcile the existing Buwumba field return to master entry H065 and do not retain a second off-master Buwumba facility."
        }
      ],
      "interpretation_limit": "The older consolidated field statement that Buwumba was off-list is superseded by the Dabani/Buwumba reconciliation. Zinga must be counted once."
    },
    {
      "case_id": "F09",
      "theme": "Incomplete school and equipment awaiting use",
      "facility": "Got Apwoyo Seed Secondary School",
      "lg": "Nwoya",
      "record_ids": [
        "S035"
      ],
      "expected": "The school buildings and supplied ICT equipment were intended to support secondary education at Got Apwoyo.",
      "expectation_basis": "Intended service use; the master schedule already described the works as Ongoing, so this is not a contradiction of a recorded Complete status.",
      "found": "The team found the school under construction and not commissioned. Its ICT package remained in the education department stores at Nwoya District headquarters awaiting completion; delivered furniture and structures had not been brought into use.",
      "gap": "Delivered equipment was not yet supporting teaching at the intended school, and custody remained split between the district and the site.",
      "action": "Nwoya District and the Ministry of Education should agree a dated completion and handover plan, maintain a checked district-store inventory, and arrange installation, testing and signed transfer to the school when it is ready.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 10; id=S035",
          "supports": "Master/return identity, LG, recorded project status (Ongoing), final reconciliation outcome; team-01 / Nwoya / Got-Apwoyo-Seed-Secondary-School"
        },
        {
          "source": "raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx",
          "locator": "paragraphs 10, 13 and 28",
          "supports": "Under construction and uncommissioned; ICT held at district headquarters; recommendation to expedite civil works."
        },
        {
          "source": "raw-data-grouped/team-01/Nwoya/Got-Apwoyo-Seed-Secondary-School/NWOYA GOT APWOYO SEED.docx",
          "locator": "paragraph 91; table 13, rows 2–13",
          "supports": "Facility and major civil structures still under construction."
        }
      ],
      "interpretation_limit": "The supplied evidence does not provide a contractual completion deadline, so do not quantify lateness."
    },
    {
      "case_id": "F10",
      "theme": "Construction damage and displaced service delivery",
      "facility": "Bukibologoto Health Centre",
      "lg": "Bulambuli",
      "record_ids": [
        "H112"
      ],
      "expected": "Bukibologoto was listed as complete and was intended to provide health services from the constructed facility.",
      "expectation_basis": "Documented master schedule Complete status plus intended use.",
      "found": "The field team found that mudslides had damaged the works before completion. Ground had fallen away below a corner of the block and a wall was cracked. The catchment was receiving care at the Simu subcounty offices, while the supplied equipment remained in district stores.",
      "gap": "The planned facility was not available for its intended use. The alternative service location and stored equipment require a clear, sustainable arrangement.",
      "action": "The district and Ministry of Health should commission an engineering assessment, decide on repair or relocation, secure and inventory the equipment, and document how services will continue while the permanent facility is resolved.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 251; id=H112",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; team-14 / Bulambuli / Bukibologoto-HC-II"
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 552–553 and 736",
          "supports": "Works damaged by mudslides before completion; care at subcounty offices; equipment unlisted in district stores; decision needed."
        }
      ]
    },
    {
      "case_id": "F11",
      "theme": "Incomplete works and site readiness",
      "facility": "Kyangwali Seed Secondary School",
      "lg": "Kikuube",
      "record_ids": [
        "S050"
      ],
      "expected": "The completed school should be ready to receive and safely use its equipment.",
      "expectation_basis": "Intended service use; master status is ongoing, not complete.",
      "found": "The team recorded continuing construction. The school also reported a lack of electricity and an incomplete perimeter fence, and handover had not taken place.",
      "gap": "Building completion alone will not make the assets ready for use unless power, security and handover are resolved.",
      "action": "The district, education ministry and contractor should close the remaining works, electricity and security requirements in one readiness plan, followed by joint testing, handover and allocation of operating responsibilities.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 473; id=S050",
          "supports": "Master/return identity, LG, recorded project status (ongoing), final reconciliation outcome; The Team 25 archive contains the Kyangwali Seed Secondary School toolkit and photographs. The return says the facility had not yet been handed over because construction was continuing."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 55; id=CHAT35M; 2026-09-23 15:09",
          "supports": "Kyangwali SSS Audit: Kyangwali Seed Secondary School, Kikuube."
        },
        {
          "source": "raw-data-grouped/team-25/Kikuube/Kyangwali-Seed-Secondary-School/KYANGWALI  SEED S.S REPORT.docx",
          "locator": "paragraphs 4 and 17",
          "supports": "Construction continuing; lack of electricity and complete fence; assets not safe."
        }
      ],
      "interpretation_limit": "No contractual due date is supplied; no quantified loss should be inferred from the security concern."
    },
    {
      "case_id": "F12",
      "theme": "Incomplete works and unopened equipment",
      "facility": "Sidok Seed Secondary School",
      "lg": "Kaabong",
      "record_ids": [
        "S019"
      ],
      "expected": "Completed buildings and checked equipment were intended to support school operations.",
      "expectation_basis": "Intended use; master schedule status is Ongoing.",
      "found": "The team found blocks, a kitchen and toilets still under construction, with termite workings on the plaster of two blocks. The school consignment remained unopened and its contents had not been counted against the delivery information.",
      "gap": "The works were unfinished and the condition and completeness of the packaged equipment had not been established by opening it.",
      "action": "The district should secure completion and treatment of the affected works, then arrange a witnessed opening, count, condition check and asset registration before equipment is issued.",
      "priority": "supporting",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 199; id=S019",
          "supports": "Master/return identity, LG, recorded project status (Ongoing), final reconciliation outcome; team-11 / Kaabong / Sidok-Seed-Secondary-School"
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 197–198, 729 and 735",
          "supports": "Incomplete works, termite workings and unopened consignment; recommended unpacking and defect correction."
        }
      ],
      "interpretation_limit": "Delivery-note identifiers are not evidence that the team read the serial numbers from the equipment."
    },
    {
      "case_id": "F13",
      "theme": "Additional return and unfinished school",
      "facility": "Lokori Seed Secondary School",
      "lg": "Karenga",
      "record_ids": [
        "X022"
      ],
      "expected": "The school needs completed accommodation and secure storage before its equipment can be used on site.",
      "expectation_basis": "Intended service use; the return has no confirmed master-list match.",
      "found": "The team found Lokori under construction, with about one block built and no store of its own. Its assets were being held at Kapedo Seed Secondary School and remained unopened.",
      "gap": "School readiness and custody of its equipment were unresolved. The return also requires confirmation against the approved beneficiary scope.",
      "action": "The district should confirm the programme identity, complete the required works and secure storage, reconcile the equipment held at Kapedo, and arrange a signed transfer when Lokori is ready.",
      "priority": "supporting",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 644; id=X022",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 211–212",
          "supports": "School under construction; no store; equipment at Kapedo unopened."
        }
      ],
      "interpretation_limit": "A submitted return and a direct site observation do not by themselves establish a newly approved additional UgIFT beneficiary."
    },
    {
      "case_id": "F14",
      "theme": "Installation and commissioning outstanding",
      "facility": "Buwagogo Seed Secondary School",
      "lg": "Manafwa",
      "record_ids": [
        "S134"
      ],
      "expected": "Supplied ICT equipment was intended to be installed and used for teaching.",
      "expectation_basis": "Intended use; the master schedule lists the facility as Complete, but that status does not separately certify equipment commissioning.",
      "found": "The team found the March 2024 ICT consignment still boxed in the store, with contractor installation pending and commissioning delayed.",
      "gap": "Delivery had not translated into operational ICT capacity at the school.",
      "action": "The district and Ministry of Education should require an installation and commissioning date, reconcile the stored equipment against delivery records, test it, and assign responsibility for its operation and maintenance.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 230; id=S134",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; team-13 / Manafwa / Buwagogo-Seed-School"
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 411–412",
          "supports": "March 2024 ICT consignment boxed; installation pending; commissioning delayed."
        }
      ],
      "interpretation_limit": "The same paragraph reports an earlier computer theft through a school letter; the present case focuses on installation and does not combine theft allegations with the stored consignment."
    },
    {
      "case_id": "F15",
      "theme": "Inspection of packaged equipment incomplete",
      "facility": "Kapedo Seed Secondary School",
      "lg": "Karenga",
      "record_ids": [
        "S146"
      ],
      "expected": "Delivered equipment should be opened, counted and matched to its identifiers before the school accepts it into accountable custody and use.",
      "expectation_basis": "Recommended receiving and asset-control practice, not a cited breach of a particular contractual clause.",
      "found": "The team saw sealed cartons of computers, network equipment, air conditioners and fittings. The store could not be opened on the visit, so the contents were not counted or checked against the delivery note.",
      "gap": "The presence of cartons did not establish the quantity, identity or working condition of the equipment inside.",
      "action": "Arrange access with the custodian and conduct a witnessed opening, count, serial-number check and functional test; update the school inventory and document any delivery differences.",
      "priority": "supporting",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 201; id=S146",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; team-11 / Karenga / Kapedo-Seed-Secondary-School"
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 205–206 and 729",
          "supports": "Cartons sealed; keys unavailable; nothing inside opened, counted or read against delivery note."
        }
      ],
      "interpretation_limit": "Do not include this consignment in a claimed count of individually physically verified or function-tested equipment."
    },
    {
      "case_id": "F16",
      "theme": "Confirmed beneficiary omitted from the master list; handover pending",
      "facility": "Bukuuku Community Seed Secondary School",
      "lg": "Fort Portal City",
      "record_ids": [
        "X030"
      ],
      "expected": "All confirmed programme beneficiaries should appear on the approved beneficiary schedule, and completed assets should be handed over for full use.",
      "expectation_basis": "Programme scope confirmation and intended handover/accountability practice.",
      "found": "Bukuuku was confirmed as an additional seed school outside the master list. The team recorded improved science and computer teaching following laboratory construction, while handover of some assets remained pending.",
      "gap": "The programme list omitted a confirmed beneficiary, and incomplete handover limited full accountability and use of the assets.",
      "action": "The city and Ministry of Education should regularise the beneficiary entry and complete a joint handover covering the outstanding items, defects, inventories and operating responsibilities.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 660; id=X030",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Depaul confirmed on 25 September 2026 that Bukuuku is not on the master list but is an additional seed secondary school in Fort Portal City. The existing return is kept. No master row is added."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 88; id=CHAT46J; 2026-09-25 13:24",
          "supports": "Bukuuku is not on master list ,but additional seed secondary school done in fort portal city Audit: Confirms the existing unmatched Bukuuku return. Do not add a master row."
        },
        {
          "source": "raw-data-grouped/team-28/Fort-Portal City/Bukuuku-Community-Secondary-School/GAYAZA AND BUKUUKU.docx",
          "locator": "paragraphs 130, 132 and 136; table 11, row 14",
          "supports": "Benefits to teaching; contractor urged to hand over; administration-block tables unfinished/work in progress."
        }
      ],
      "interpretation_limit": "Do not say the entire school was non-operational: the same source describes teaching benefits from its laboratories."
    },
    {
      "case_id": "F17",
      "theme": "Confirmed beneficiaries omitted from the master list",
      "facility": "Rukoki General Hospital and Silumira Health Centre III",
      "lg": "Kasese Municipality and Kakumiro",
      "record_ids": [
        "X007",
        "X010"
      ],
      "expected": "Confirmed UgIFT beneficiaries should be included in the authoritative programme account.",
      "expectation_basis": "Explicit supervisor confirmation of programme beneficiary status outside the master list.",
      "found": "The supervisor confirmed that Rukoki General Hospital was a UgIFT beneficiary in Kasese Municipality and that Silumira Health Centre III was an additional beneficiary in Kakumiro. Neither appeared on the master list used for verification.",
      "gap": "The programme scope omitted confirmed recipients. Their submitted asset information must be linked to approved beneficiary decisions without silently changing the original verification denominator.",
      "action": "The sector ministry and local governments should approve the additions, assign stable facility identifiers, and connect the beneficiary decisions to their asset schedules.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 659; id=X007",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Depaul confirmed on 25 September 2026 that Rukoki General Hospital is not on the master list but is a UgIFT beneficiary in Kasese Municipality. The existing register return is kept. No master row is added."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 86; id=CHAT46H; 2026-09-25 13:14",
          "supports": "Rukoki general hospital is not on the master list but a beneficiary of UgIFT, in kasese Municipality Audit: Confirms the existing unmatched Rukoki return. Do not add a master row."
        },
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 662; id=X010",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Depaul confirmed on 25 September 2026 that Silumira HC III is not on the master list but was done in Kakumiro. The existing register return is kept. No master row is added."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 87; id=CHAT46I; 2026-09-25 13:23",
          "supports": "Silumira HCIII not on master list but was done in kakumiro district Audit: Confirms the existing unmatched Silumira return. Do not add a master row."
        }
      ],
      "interpretation_limit": "Their evidence is held in consolidated returns. Confirmation of beneficiary status is not a certificate of physical inspection or construction completion."
    },
    {
      "case_id": "F18",
      "theme": "Assets without engraved identifiers",
      "facility": "Bulaago Health Centre",
      "lg": "Bulambuli",
      "record_ids": [
        "H114"
      ],
      "expected": "Equipment should carry durable identifiers that can be matched to the facility inventory.",
      "expectation_basis": "Recommended asset-control practice; consolidated field report paragraphs 724–725 call for a common unique marking system.",
      "found": "The team found that Bulaago equipment had no engraved or serialised identifiers.",
      "gap": "Identical items could not be reliably distinguished during movement, maintenance or later verification.",
      "action": "The district should assign unique numbers, mark suitable items durably, link each number to the inventory, and record responsibility for completing and checking the work.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 252; id=H114",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; team-14 / Bulambuli / Bulaago-HC-III"
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 528–529 and 724–725",
          "supports": "No equipment engraved or serialised; recommended common unique marking system."
        }
      ]
    },
    {
      "case_id": "F19",
      "theme": "Programme marks without unique asset numbers",
      "facility": "Bumugibole Health Centre",
      "lg": "Bulambuli",
      "record_ids": [
        "H111"
      ],
      "expected": "An asset mark should distinguish the individual item as well as its programme and facility.",
      "expectation_basis": "Recommended identification standard; the source explicitly distinguishes programme marking from item numbering.",
      "found": "The team found programme and financial-year marks on items that could take an engraving, but the marks did not include individual asset numbers.",
      "gap": "Visible programme branding did not provide a unique link between each item and its inventory entry.",
      "action": "Retain the existing programme mark and add a unique asset number linked to the district inventory and the responsible custodian.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 253; id=H111",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; team-14 / Bulambuli / Bumugibole-HC-III"
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 546–547 and 724",
          "supports": "BUMU/2020-2021/UGIFT marks without asset number; common unique-number recommendation."
        }
      ],
      "interpretation_limit": "Do not classify all existing programme marks as absent engraving; this is a quality-of-identification gap."
    },
    {
      "case_id": "F20",
      "theme": "Defects affecting intended use",
      "facility": "Bumugibole Health Centre staff house and water tanks",
      "lg": "Bulambuli",
      "record_ids": [
        "H111"
      ],
      "expected": "Staff accommodation and water assets were intended to remain safe and usable for health-service delivery.",
      "expectation_basis": "Intended asset use; not a structural-engineering certification.",
      "found": "The team recorded deep cracks in the staff house. Medical staff had left it because they considered it unsafe, and only one of three water tanks was reported to be working.",
      "gap": "The staff house was not serving its intended occupants, and water-storage capacity was reduced.",
      "action": "The district should arrange a qualified structural assessment, safeguard occupants, pursue applicable defect remedies, and restore the non-working water tanks after a technical assessment.",
      "priority": "high",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 253; id=H111",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; team-14 / Bulambuli / Bumugibole-HC-III"
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 546–547 and 735",
          "supports": "Cracked staff house, medical staff moved out, one of three tanks working; recommendation to pursue defect remedies."
        }
      ],
      "interpretation_limit": "Do not present the verification team as certifying structural safety or assume that contractor defect liability remains open; confirm the contract dates."
    }
  ],
  "incomplete_facilities": [
    {
      "case_id": "F09",
      "facility": "Got Apwoyo Seed Secondary School",
      "lg": "Nwoya",
      "record_ids": [
        "S035"
      ],
      "expected": "The school buildings and supplied ICT equipment were intended to support secondary education at Got Apwoyo.",
      "expectation_basis": "Intended service use; the master schedule already described the works as Ongoing, so this is not a contradiction of a recorded Complete status.",
      "found": "The team found the school under construction and not commissioned. Its ICT package remained in the education department stores at Nwoya District headquarters awaiting completion; delivered furniture and structures had not been brought into use.",
      "gap": "Delivered equipment was not yet supporting teaching at the intended school, and custody remained split between the district and the site.",
      "action": "Nwoya District and the Ministry of Education should agree a dated completion and handover plan, maintain a checked district-store inventory, and arrange installation, testing and signed transfer to the school when it is ready.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 10; id=S035",
          "supports": "Master/return identity, LG, recorded project status (Ongoing), final reconciliation outcome; team-01 / Nwoya / Got-Apwoyo-Seed-Secondary-School"
        },
        {
          "source": "raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx",
          "locator": "paragraphs 10, 13 and 28",
          "supports": "Under construction and uncommissioned; ICT held at district headquarters; recommendation to expedite civil works."
        },
        {
          "source": "raw-data-grouped/team-01/Nwoya/Got-Apwoyo-Seed-Secondary-School/NWOYA GOT APWOYO SEED.docx",
          "locator": "paragraph 91; table 13, rows 2–13",
          "supports": "Facility and major civil structures still under construction."
        }
      ]
    },
    {
      "case_id": "F10",
      "facility": "Bukibologoto Health Centre",
      "lg": "Bulambuli",
      "record_ids": [
        "H112"
      ],
      "expected": "Bukibologoto was listed as complete and was intended to provide health services from the constructed facility.",
      "expectation_basis": "Documented master schedule Complete status plus intended use.",
      "found": "The field team found that mudslides had damaged the works before completion. Ground had fallen away below a corner of the block and a wall was cracked. The catchment was receiving care at the Simu subcounty offices, while the supplied equipment remained in district stores.",
      "gap": "The planned facility was not available for its intended use. The alternative service location and stored equipment require a clear, sustainable arrangement.",
      "action": "The district and Ministry of Health should commission an engineering assessment, decide on repair or relocation, secure and inventory the equipment, and document how services will continue while the permanent facility is resolved.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 251; id=H112",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; team-14 / Bulambuli / Bukibologoto-HC-II"
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 552–553 and 736",
          "supports": "Works damaged by mudslides before completion; care at subcounty offices; equipment unlisted in district stores; decision needed."
        }
      ]
    },
    {
      "case_id": "F11",
      "facility": "Kyangwali Seed Secondary School",
      "lg": "Kikuube",
      "record_ids": [
        "S050"
      ],
      "expected": "The completed school should be ready to receive and safely use its equipment.",
      "expectation_basis": "Intended service use; master status is ongoing, not complete.",
      "found": "The team recorded continuing construction. The school also reported a lack of electricity and an incomplete perimeter fence, and handover had not taken place.",
      "gap": "Building completion alone will not make the assets ready for use unless power, security and handover are resolved.",
      "action": "The district, education ministry and contractor should close the remaining works, electricity and security requirements in one readiness plan, followed by joint testing, handover and allocation of operating responsibilities.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 473; id=S050",
          "supports": "Master/return identity, LG, recorded project status (ongoing), final reconciliation outcome; The Team 25 archive contains the Kyangwali Seed Secondary School toolkit and photographs. The return says the facility had not yet been handed over because construction was continuing."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 55; id=CHAT35M; 2026-09-23 15:09",
          "supports": "Kyangwali SSS Audit: Kyangwali Seed Secondary School, Kikuube."
        },
        {
          "source": "raw-data-grouped/team-25/Kikuube/Kyangwali-Seed-Secondary-School/KYANGWALI  SEED S.S REPORT.docx",
          "locator": "paragraphs 4 and 17",
          "supports": "Construction continuing; lack of electricity and complete fence; assets not safe."
        }
      ]
    },
    {
      "case_id": "F12",
      "facility": "Sidok Seed Secondary School",
      "lg": "Kaabong",
      "record_ids": [
        "S019"
      ],
      "expected": "Completed buildings and checked equipment were intended to support school operations.",
      "expectation_basis": "Intended use; master schedule status is Ongoing.",
      "found": "The team found blocks, a kitchen and toilets still under construction, with termite workings on the plaster of two blocks. The school consignment remained unopened and its contents had not been counted against the delivery information.",
      "gap": "The works were unfinished and the condition and completeness of the packaged equipment had not been established by opening it.",
      "action": "The district should secure completion and treatment of the affected works, then arrange a witnessed opening, count, condition check and asset registration before equipment is issued.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 199; id=S019",
          "supports": "Master/return identity, LG, recorded project status (Ongoing), final reconciliation outcome; team-11 / Kaabong / Sidok-Seed-Secondary-School"
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 197–198, 729 and 735",
          "supports": "Incomplete works, termite workings and unopened consignment; recommended unpacking and defect correction."
        }
      ]
    },
    {
      "case_id": "F13",
      "facility": "Lokori Seed Secondary School",
      "lg": "Karenga",
      "record_ids": [
        "X022"
      ],
      "expected": "The school needs completed accommodation and secure storage before its equipment can be used on site.",
      "expectation_basis": "Intended service use; the return has no confirmed master-list match.",
      "found": "The team found Lokori under construction, with about one block built and no store of its own. Its assets were being held at Kapedo Seed Secondary School and remained unopened.",
      "gap": "School readiness and custody of its equipment were unresolved. The return also requires confirmation against the approved beneficiary scope.",
      "action": "The district should confirm the programme identity, complete the required works and secure storage, reconcile the equipment held at Kapedo, and arrange a signed transfer when Lokori is ready.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 644; id=X022",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 211–212",
          "supports": "School under construction; no store; equipment at Kapedo unopened."
        }
      ]
    },
    {
      "case_id": "F14",
      "facility": "Buwagogo Seed Secondary School",
      "lg": "Manafwa",
      "record_ids": [
        "S134"
      ],
      "expected": "Supplied ICT equipment was intended to be installed and used for teaching.",
      "expectation_basis": "Intended use; the master schedule lists the facility as Complete, but that status does not separately certify equipment commissioning.",
      "found": "The team found the March 2024 ICT consignment still boxed in the store, with contractor installation pending and commissioning delayed.",
      "gap": "Delivery had not translated into operational ICT capacity at the school.",
      "action": "The district and Ministry of Education should require an installation and commissioning date, reconcile the stored equipment against delivery records, test it, and assign responsibility for its operation and maintenance.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 230; id=S134",
          "supports": "Master/return identity, LG, recorded project status (Complete), final reconciliation outcome; team-13 / Manafwa / Buwagogo-Seed-School"
        },
        {
          "source": "raw-data-grouped/_multi-team/teams-10-15/final-UGiFT-report-karamojja-6-teams/UGiFT-consolidated-field-report.docx",
          "locator": "paragraphs 411–412",
          "supports": "March 2024 ICT consignment boxed; installation pending; commissioning delayed."
        }
      ]
    },
    {
      "case_id": "F16",
      "facility": "Bukuuku Community Seed Secondary School",
      "lg": "Fort Portal City",
      "record_ids": [
        "X030"
      ],
      "expected": "All confirmed programme beneficiaries should appear on the approved beneficiary schedule, and completed assets should be handed over for full use.",
      "expectation_basis": "Programme scope confirmation and intended handover/accountability practice.",
      "found": "Bukuuku was confirmed as an additional seed school outside the master list. The team recorded improved science and computer teaching following laboratory construction, while handover of some assets remained pending.",
      "gap": "The programme list omitted a confirmed beneficiary, and incomplete handover limited full accountability and use of the assets.",
      "action": "The city and Ministry of Education should regularise the beneficiary entry and complete a joint handover covering the outstanding items, defects, inventories and operating responsibilities.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 660; id=X030",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Depaul confirmed on 25 September 2026 that Bukuuku is not on the master list but is an additional seed secondary school in Fort Portal City. The existing return is kept. No master row is added."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 88; id=CHAT46J; 2026-09-25 13:24",
          "supports": "Bukuuku is not on master list ,but additional seed secondary school done in fort portal city Audit: Confirms the existing unmatched Bukuuku return. Do not add a master row."
        },
        {
          "source": "raw-data-grouped/team-28/Fort-Portal City/Bukuuku-Community-Secondary-School/GAYAZA AND BUKUUKU.docx",
          "locator": "paragraphs 130, 132 and 136; table 11, row 14",
          "supports": "Benefits to teaching; contractor urged to hand over; administration-block tables unfinished/work in progress."
        }
      ]
    }
  ],
  "ground_only_examples": [
    {
      "id": "X901",
      "facility": "Ekaligo Health Centre III",
      "lg": "Yumbe",
      "evidence_class": "Independent facility confirmed; no separate asset schedule identified",
      "finding": "The programme data manager confirms that Ekaligo and Amanyiri are independent facilities. The combined file names Ekaligo in the interview, while the asset schedule separately names Amanyiri.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 636; id=X901",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; The programme data manager confirms that Ekaligo and Amanyiri are independent facilities. The combined file names Ekaligo in the interview, while the asset schedule separately names Amanyiri."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 26; id=USER02; 2026-09-23",
          "supports": "For team 2, use the facility names on file over the ones in the master list. Amanyiri Health Centre III, Ekaligo, Liko, Lodonga Seed Secondary School all exist independently. Audit: Treat the combined returns as evidence for the names written in their sections. Amanyiri and Lodonga retain their explicitly named asset schedules. Ekaligo and Liko remain separate ground facilities; no replacement or alias relationship is inferred."
        },
        {
          "source": "raw-data-grouped/team-02/Yumbe/Amanyiri-HC-III/1 AMANYIRI HCIII.docx",
          "locator": "Health-centre interview: Name of Health EKALIGO HCIII",
          "supports": "Facility named in submitted return; no separate Ekaligo asset schedule identified"
        }
      ]
    },
    {
      "id": "X902",
      "facility": "Liko Health Centre III",
      "lg": "Yumbe",
      "evidence_class": "Independent facility confirmed; no separate asset schedule identified",
      "finding": "The programme data manager confirms that Liko and Lodonga Seed Secondary School are independent facilities. The combined file names Liko in the health-centre interview and Lodonga in the school asset schedules.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 637; id=X902",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; The programme data manager confirms that Liko and Lodonga Seed Secondary School are independent facilities. The combined file names Liko in the health-centre interview and Lodonga in the school asset schedules."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 26; id=USER02; 2026-09-23",
          "supports": "For team 2, use the facility names on file over the ones in the master list. Amanyiri Health Centre III, Ekaligo, Liko, Lodonga Seed Secondary School all exist independently. Audit: Treat the combined returns as evidence for the names written in their sections. Amanyiri and Lodonga retain their explicitly named asset schedules. Ekaligo and Liko remain separate ground facilities; no replacement or alias relationship is inferred."
        },
        {
          "source": "raw-data-grouped/team-02/Yumbe/Lodonga-Seed-Secondary-School/LODONGA SEED SS (2).docx",
          "locator": "Health-centre interview: Name of Health Centre Liko Health center iii",
          "supports": "Facility named in submitted return; no separate Liko asset schedule identified"
        }
      ]
    },
    {
      "id": "X019",
      "facility": "Onywako Health Centre III",
      "lg": "Lira",
      "evidence_class": "Physical verification explicitly not performed",
      "finding": "Form states that assets were reported by the in-charge and were not physically verified. Chat names Onywako on ground, but gives no one-to-one replacement for Alik.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 640; id=X019",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Form states that assets were reported by the in-charge and were not physically verified. Chat names Onywako on ground, but gives no one-to-one replacement for Alik."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 11; id=CHAT11; 2026-09-21 16:56",
          "supports": "In Lira Lg - Alik HC 111 does not exist. The Lg has two facilities namely \n1.Barlonyo Hc111\n2.Onywako HC 111. Audit: No explicit one-to-one Alik-to-Onywako replacement. Master additionally contains Punuluru; omission from this list alone is not an explicit nonexistence decision. Onywako form explicitly excludes physical verification."
        },
        {
          "source": "raw-data-grouped/team-05/Lira/Onywako-HC-III/ONYWAKO HEALTH CENTRE 3.docx",
          "locator": "Facility-specific return",
          "supports": "Physical verification explicitly not performed"
        }
      ]
    },
    {
      "id": "X022",
      "facility": "Lokori Seed Secondary School",
      "lg": "Karenga",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 644; id=X022",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-11/Karenga/Lokori-Seed-Secondary-School/Asset-Verification-Toolkit.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X900",
      "facility": "Sofia Health Centre III",
      "lg": "Busia MC",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return identifies Sofia Health Centre III in Eastern Division, Busia Municipal Council. It is distinct from the invalid master label Busia Eastern Division.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 645; id=X900",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return identifies Sofia Health Centre III in Eastern Division, Busia Municipal Council. It is distinct from the invalid master label Busia Eastern Division."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 23; id=CHAT19; 2026-09-23 02:39",
          "supports": "The master list shows a health centre called Busia Eastern Division. No such facility exists. Audit: Sofia Health Centre III is a separately named field return in Eastern Division and is not treated as an alias for this invalid master label."
        },
        {
          "source": "raw-data-grouped/team-13/Busia MC/Sofia-Health-Centre-III/Sofia health centre 111 eastern division busia MC.pdf",
          "locator": "Pages 1-20",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X007",
      "facility": "Rukoki General Hospital",
      "lg": "Kasese",
      "evidence_class": "Explicitly confirmed additional programme beneficiary",
      "finding": "Depaul confirmed on 25 September 2026 that Rukoki General Hospital is not on the master list but is a UgIFT beneficiary in Kasese Municipality. The existing register return is kept. No master row is added.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 659; id=X007",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Depaul confirmed on 25 September 2026 that Rukoki General Hospital is not on the master list but is a UgIFT beneficiary in Kasese Municipality. The existing register return is kept. No master row is added."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 86; id=CHAT46H; 2026-09-25 13:14",
          "supports": "Rukoki general hospital is not on the master list but a beneficiary of UgIFT, in kasese Municipality Audit: Confirms the existing unmatched Rukoki return. Do not add a master row."
        },
        {
          "source": "raw-data-grouped/_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT.xls",
          "locator": "UGIFT HEALTH!row 4737",
          "supports": "Completed from consolidated register; physical inspection not certified"
        }
      ]
    },
    {
      "id": "X030",
      "facility": "Bukuuku Community Seed Secondary School",
      "lg": "Fort-Portal City",
      "evidence_class": "Explicitly confirmed additional programme beneficiary",
      "finding": "Depaul confirmed on 25 September 2026 that Bukuuku is not on the master list but is an additional seed secondary school in Fort Portal City. The existing return is kept. No master row is added.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 660; id=X030",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Depaul confirmed on 25 September 2026 that Bukuuku is not on the master list but is an additional seed secondary school in Fort Portal City. The existing return is kept. No master row is added."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 88; id=CHAT46J; 2026-09-25 13:24",
          "supports": "Bukuuku is not on master list ,but additional seed secondary school done in fort portal city Audit: Confirms the existing unmatched Bukuuku return. Do not add a master row."
        },
        {
          "source": "raw-data-grouped/team-28/Fort-Portal City/Bukuuku-Community-Secondary-School/GAYAZA AND BUKUUKU.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X010",
      "facility": "Silumira Health Centre III",
      "lg": "Kakumiro",
      "evidence_class": "Explicitly confirmed additional programme beneficiary",
      "finding": "Depaul confirmed on 25 September 2026 that Silumira HC III is not on the master list but was done in Kakumiro. The existing register return is kept. No master row is added.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 662; id=X010",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Depaul confirmed on 25 September 2026 that Silumira HC III is not on the master list but was done in Kakumiro. The existing register return is kept. No master row is added."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 87; id=CHAT46I; 2026-09-25 13:23",
          "supports": "Silumira HCIII not on master list but was done in kakumiro district Audit: Confirms the existing unmatched Silumira return. Do not add a master row."
        },
        {
          "source": "raw-data-grouped/_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT.xls",
          "locator": "UGIFT HEALTH 2!row 966",
          "supports": "Completed from consolidated register; physical inspection not certified"
        }
      ]
    }
  ],
  "ground_only_all_24": [
    {
      "id": "X013",
      "facility": "Amei Seed Secondary School",
      "lg": "Zombo",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 631; id=X013",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-01/Zombo/Amei-Seed-Secondary-School/ZOMBO - GOT APWOYO HC & AMEI SEED ZOMBO 2.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X016",
      "facility": "Odupiri Health Centre III",
      "lg": "Maracha",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 635; id=X016",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-02/Maracha/Odupiri-HC-III/1 ODUPIRI HC - Kololo SSS MARACHA  district.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X901",
      "facility": "Ekaligo Health Centre III",
      "lg": "Yumbe",
      "evidence_class": "Independent facility confirmed; no separate asset schedule identified",
      "finding": "The programme data manager confirms that Ekaligo and Amanyiri are independent facilities. The combined file names Ekaligo in the interview, while the asset schedule separately names Amanyiri.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 636; id=X901",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; The programme data manager confirms that Ekaligo and Amanyiri are independent facilities. The combined file names Ekaligo in the interview, while the asset schedule separately names Amanyiri."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 26; id=USER02; 2026-09-23",
          "supports": "For team 2, use the facility names on file over the ones in the master list. Amanyiri Health Centre III, Ekaligo, Liko, Lodonga Seed Secondary School all exist independently. Audit: Treat the combined returns as evidence for the names written in their sections. Amanyiri and Lodonga retain their explicitly named asset schedules. Ekaligo and Liko remain separate ground facilities; no replacement or alias relationship is inferred."
        },
        {
          "source": "raw-data-grouped/team-02/Yumbe/Amanyiri-HC-III/1 AMANYIRI HCIII.docx",
          "locator": "Health-centre interview: Name of Health EKALIGO HCIII",
          "supports": "Facility named in submitted return; no separate Ekaligo asset schedule identified"
        }
      ]
    },
    {
      "id": "X902",
      "facility": "Liko Health Centre III",
      "lg": "Yumbe",
      "evidence_class": "Independent facility confirmed; no separate asset schedule identified",
      "finding": "The programme data manager confirms that Liko and Lodonga Seed Secondary School are independent facilities. The combined file names Liko in the health-centre interview and Lodonga in the school asset schedules.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 637; id=X902",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; The programme data manager confirms that Liko and Lodonga Seed Secondary School are independent facilities. The combined file names Liko in the health-centre interview and Lodonga in the school asset schedules."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 26; id=USER02; 2026-09-23",
          "supports": "For team 2, use the facility names on file over the ones in the master list. Amanyiri Health Centre III, Ekaligo, Liko, Lodonga Seed Secondary School all exist independently. Audit: Treat the combined returns as evidence for the names written in their sections. Amanyiri and Lodonga retain their explicitly named asset schedules. Ekaligo and Liko remain separate ground facilities; no replacement or alias relationship is inferred."
        },
        {
          "source": "raw-data-grouped/team-02/Yumbe/Lodonga-Seed-Secondary-School/LODONGA SEED SS (2).docx",
          "locator": "Health-centre interview: Name of Health Centre Liko Health center iii",
          "supports": "Facility named in submitted return; no separate Liko asset schedule identified"
        }
      ]
    },
    {
      "id": "X017",
      "facility": "Lobe Health Centre III",
      "lg": "Yumbe",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 638; id=X017",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-02/Yumbe/Lobe-HC-III/LOBE HC[YUMBE]ASSET VERIFICATION AND RECORDING TOOL KIT 222(3)(1).docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X018",
      "facility": "Nyori Health Centre III",
      "lg": "Yumbe",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 639; id=X018",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-02/Yumbe/Nyori-HC-III/NYORI HCIII.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X019",
      "facility": "Onywako Health Centre III",
      "lg": "Lira",
      "evidence_class": "Physical verification explicitly not performed",
      "finding": "Form states that assets were reported by the in-charge and were not physically verified. Chat names Onywako on ground, but gives no one-to-one replacement for Alik.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 640; id=X019",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Form states that assets were reported by the in-charge and were not physically verified. Chat names Onywako on ground, but gives no one-to-one replacement for Alik."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 11; id=CHAT11; 2026-09-21 16:56",
          "supports": "In Lira Lg - Alik HC 111 does not exist. The Lg has two facilities namely \n1.Barlonyo Hc111\n2.Onywako HC 111. Audit: No explicit one-to-one Alik-to-Onywako replacement. Master additionally contains Punuluru; omission from this list alone is not an explicit nonexistence decision. Onywako form explicitly excludes physical verification."
        },
        {
          "source": "raw-data-grouped/team-05/Lira/Onywako-HC-III/ONYWAKO HEALTH CENTRE 3.docx",
          "locator": "Facility-specific return",
          "supports": "Physical verification explicitly not performed"
        }
      ]
    },
    {
      "id": "X020",
      "facility": "Arocha Health Centre III",
      "lg": "Apac",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 641; id=X020",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-06/Apac/Arocha-HC-III/ARONCHA HC III.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X021",
      "facility": "Rupa Seed Secondary School",
      "lg": "Moroto",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 643; id=X021",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-10/Moroto/Rupa-Seed-Secondary-School/_supporting-documents/IMG_20260922_0002.pdf",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X022",
      "facility": "Lokori Seed Secondary School",
      "lg": "Karenga",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 644; id=X022",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-11/Karenga/Lokori-Seed-Secondary-School/Asset-Verification-Toolkit.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X900",
      "facility": "Sofia Health Centre III",
      "lg": "Busia MC",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return identifies Sofia Health Centre III in Eastern Division, Busia Municipal Council. It is distinct from the invalid master label Busia Eastern Division.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 645; id=X900",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return identifies Sofia Health Centre III in Eastern Division, Busia Municipal Council. It is distinct from the invalid master label Busia Eastern Division."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 23; id=CHAT19; 2026-09-23 02:39",
          "supports": "The master list shows a health centre called Busia Eastern Division. No such facility exists. Audit: Sofia Health Centre III is a separately named field return in Eastern Division and is not treated as an alias for this invalid master label."
        },
        {
          "source": "raw-data-grouped/team-13/Busia MC/Sofia-Health-Centre-III/Sofia health centre 111 eastern division busia MC.pdf",
          "locator": "Pages 1-20",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X024",
      "facility": "Simu Pondo Health Centre III",
      "lg": "Sironko",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 646; id=X024",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-14/Sironko/Simu-Pondo-HC-III/Asset-Verification-Toolkit.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X003",
      "facility": "Kabushaho Seed Secondary School",
      "lg": "Bushenyi",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Workbook is filed under Mitooma, but its facility heading explicitly says Bushenyi. No exact master-list school match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 647; id=X003",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Workbook is filed under Mitooma, but its facility heading explicitly says Bushenyi. No exact master-list school match."
        },
        {
          "source": "raw-data-grouped/team-19/Mitooma/_district-documents/MITOOMA DISTRICT  SEED SCHS.xlsx",
          "locator": "Sheet1!row 1",
          "supports": "Completed from consolidated register; physical inspection not certified"
        }
      ]
    },
    {
      "id": "X004",
      "facility": "Kitojo Seed Secondary School",
      "lg": "Mitooma",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Named in submitted register; no confirmed master match. Asset section: Name of LG:  MITOOMA DISTRICT  Name of SCHOOL: KITOJO SEED SCHOOL",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 648; id=X004",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Named in submitted register; no confirmed master match. Asset section: Name of LG:  MITOOMA DISTRICT  Name of SCHOOL: KITOJO SEED SCHOOL"
        },
        {
          "source": "raw-data-grouped/team-19/Mitooma/_district-documents/MITOOMA DISTRICT  SEED SCHS.xlsx",
          "locator": "Sheet1!row 129",
          "supports": "Completed from consolidated register; physical inspection not certified"
        }
      ]
    },
    {
      "id": "X005",
      "facility": "Migina Health Centre III",
      "lg": "Sheema",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Named in submitted register; no confirmed master match. Asset section: MIGINA HCIII,   SHEEMA DC",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 649; id=X005",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Named in submitted register; no confirmed master match. Asset section: MIGINA HCIII,   SHEEMA DC"
        },
        {
          "source": "raw-data-grouped/team-19/Sheema/_district-documents/SHEEMA DC    HCIIIs.xlsx",
          "locator": "Sheet1!row 2",
          "supports": "Completed from consolidated register; physical inspection not certified"
        }
      ]
    },
    {
      "id": "X025",
      "facility": "Kibuzigye Seed Secondary School",
      "lg": "Rubanda",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 651; id=X025",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-22/Rubanda/Kibuzigye-Secondary-School/RUBANDA -LG FIELD TEMPLATE  MPUNGUHCIII,Nyamweru ss,Ruija ss, and Kibuzigye ss2.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X026",
      "facility": "Bushogye Seed Secondary School",
      "lg": "Kanungu",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 652; id=X026",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-23/Kanungu/Bushogye-Seed-Secondary-School/KINAABA HCIII and BUSHOGYE Seed School Kanungu LG.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X027",
      "facility": "Bikurungu Seed Secondary School",
      "lg": "Rukungiri",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 653; id=X027",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-23/Rukungiri/Bikurungu-Seed-Secondary-School/KITIMBA HCIII and BIKURUNGU SEED SCHOOL RUKUNGIRI LG.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X007",
      "facility": "Rukoki General Hospital",
      "lg": "Kasese",
      "evidence_class": "Explicitly confirmed additional programme beneficiary",
      "finding": "Depaul confirmed on 25 September 2026 that Rukoki General Hospital is not on the master list but is a UgIFT beneficiary in Kasese Municipality. The existing register return is kept. No master row is added.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 659; id=X007",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Depaul confirmed on 25 September 2026 that Rukoki General Hospital is not on the master list but is a UgIFT beneficiary in Kasese Municipality. The existing register return is kept. No master row is added."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 86; id=CHAT46H; 2026-09-25 13:14",
          "supports": "Rukoki general hospital is not on the master list but a beneficiary of UgIFT, in kasese Municipality Audit: Confirms the existing unmatched Rukoki return. Do not add a master row."
        },
        {
          "source": "raw-data-grouped/_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT.xls",
          "locator": "UGIFT HEALTH!row 4737",
          "supports": "Completed from consolidated register; physical inspection not certified"
        }
      ]
    },
    {
      "id": "X030",
      "facility": "Bukuuku Community Seed Secondary School",
      "lg": "Fort-Portal City",
      "evidence_class": "Explicitly confirmed additional programme beneficiary",
      "finding": "Depaul confirmed on 25 September 2026 that Bukuuku is not on the master list but is an additional seed secondary school in Fort Portal City. The existing return is kept. No master row is added.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 660; id=X030",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Depaul confirmed on 25 September 2026 that Bukuuku is not on the master list but is an additional seed secondary school in Fort Portal City. The existing return is kept. No master row is added."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 88; id=CHAT46J; 2026-09-25 13:24",
          "supports": "Bukuuku is not on master list ,but additional seed secondary school done in fort portal city Audit: Confirms the existing unmatched Bukuuku return. Do not add a master row."
        },
        {
          "source": "raw-data-grouped/team-28/Fort-Portal City/Bukuuku-Community-Secondary-School/GAYAZA AND BUKUUKU.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X010",
      "facility": "Silumira Health Centre III",
      "lg": "Kakumiro",
      "evidence_class": "Explicitly confirmed additional programme beneficiary",
      "finding": "Depaul confirmed on 25 September 2026 that Silumira HC III is not on the master list but was done in Kakumiro. The existing register return is kept. No master row is added.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 662; id=X010",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Depaul confirmed on 25 September 2026 that Silumira HC III is not on the master list but was done in Kakumiro. The existing register return is kept. No master row is added."
        },
        {
          "source": "raw-data-grouped/supervisor-decisions.csv",
          "locator": "CSV data record 87; id=CHAT46I; 2026-09-25 13:23",
          "supports": "Silumira HCIII not on master list but was done in kakumiro district Audit: Confirms the existing unmatched Silumira return. Do not add a master row."
        },
        {
          "source": "raw-data-grouped/_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT.xls",
          "locator": "UGIFT HEALTH 2!row 966",
          "supports": "Completed from consolidated register; physical inspection not certified"
        }
      ]
    },
    {
      "id": "X032",
      "facility": "Buvuma Health Centre III",
      "lg": "Buvuma",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 665; id=X032",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-31/Buvuma/Buvuma-HC-III/BUVUMA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X903",
      "facility": "Buloba Health Centre III",
      "lg": "Wakiso",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "The 26 September photographs show two Buloba HC III equipment lists with quantities and costs, one stamped by the Wakiso District Health Office. Buloba is not on the Wakiso master list and no message links it to a master facility, so it stays a separate return.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 666; id=X903",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; The 26 September photographs show two Buloba HC III equipment lists with quantities and costs, one stamped by the Wakiso District Health Office. Buloba is not on the Wakiso master list and no message links it to a master facility, so it stays a separate return."
        },
        {
          "source": "raw-data-grouped/team-32/Wakiso/Buloba-HC-III/Buloba HC III asset verification.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    },
    {
      "id": "X033",
      "facility": "Lwengenyi Health Centre III",
      "lg": "Lwengo",
      "evidence_class": "Separate return identity without a confirmed master match",
      "finding": "Facility-specific return received; no confirmed master match.",
      "provenance": [
        {
          "source": "raw-data-grouped/facility-reconciliation.csv",
          "locator": "CSV data record 667; id=X033",
          "supports": "Master/return identity, LG, recorded project status (not supplied), final reconciliation outcome; Facility-specific return received; no confirmed master match."
        },
        {
          "source": "raw-data-grouped/team-33/Lwengo/Lwengenyi-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT 222 (1) LWENGENYI HEALTH CENTRE III& KATOVU SEED SECONDARY SCHOOL.docx",
          "locator": "Facility-specific return",
          "supports": "Verification records received; physical completion not certified"
        }
      ]
    }
  ],
  "ground_only_count_interpretation": {
    "return_identities": 24,
    "explicit_additional_programme_beneficiaries": 3,
    "independent_facilities_but_no_separate_asset_schedule": 2,
    "explicitly_not_physically_verified": 1,
    "other_unmatched_return_identities": 18,
    "explanation": "The four groups are disjoint evidence descriptions and sum to 24. Three is a conservative count of expressly confirmed additional programme beneficiaries in the reconciliation messages, not a claim that only three of the 24 are real or eligible facilities. Known aliases such as Dabani/Buwumba and Bussi/Zinga are already reconciled to master entries and must not be added to the 24. Eleven linked receiving records are a separate reconciliation group, not extra ground-only facilities."
  },
  "source_native_reason_counts": [
    {
      "reason": "Does not exist or was not constructed under the programme",
      "count": 10
    },
    {
      "reason": "Replaced by another facility",
      "count": 4
    },
    {
      "reason": "Operates under another name",
      "count": 30
    },
    {
      "reason": "Not a UgIFT beneficiary",
      "count": 3
    },
    {
      "reason": "Assets relocated to another facility or held at district",
      "count": 3
    },
    {
      "reason": "Exists with no UgIFT assets",
      "count": 5
    }
  ],
  "editorial_guidance": [
    "Use teams found for observations explicitly recorded as field observations. Use the DHO confirmed or the supervisor confirmed for interview/reconciliation evidence. Do not turn message confirmation into a physical inspection.",
    "Expectations based on intended use or recommended controls are explicitly labelled; do not turn them into an undocumented procurement specification or contractual deadline.",
    "Priority high cases can support the main findings. Supporting cases may be placed in an annex to control length.",
    "Do not call every name correction a service-delivery gap; some are identity clean-up with no evidence of failed service delivery.",
    "The 629 accountability total counts master facility identities, not necessarily 629 unique physical sites. Do not add replacements, receiving records, aliases or 24 unmatched returns to it without a reconciled scope decision.",
    "The 589 evidence-backed count is not a physical-verification numerator; the 40 explanations include telephone information, access limitations and storage/commissioning explanations beyond the six selected substantive reasons.",
    "Avoid generic file-led prose in the report. Keep exact paths, chat references, CSV record numbers and extraction details in sources.md only.",
    "Master Complete/Ongoing labels are recorded programme statuses, not independent certificates of condition at the visit.",
    "Additional construction and handover cases are examples, not an exhaustive or statistically representative total of incomplete facilities."
  ],
  "compact_ready": {
    "overview_paragraphs": [
      "The exercise accounted for 629 entries on the verification master list: 258 schools and 371 health centres. Follow-up established which facilities retained their original names, which had replacements or relocated assets, and which listed institutions had not received programme support. These distinctions matter because a name on the list does not, by itself, demonstrate that the intended facility and its assets are available for service.",
      "The findings identified 10 entries reported nonexistent or not constructed, four replacements, 30 name corrections, three institutions outside UgIFT, three cases of relocated assets and five existing facilities without UgIFT assets. The cases below explain the differences and the action needed. Identity corrections should be settled alongside decisions on incomplete works, custody, handover and operational readiness so that the programme account reflects where services and assets are actually located."
    ],
    "cases": [
      {
        "case_id": "F01",
        "theme": "Listed complete but not constructed",
        "facility": "Olok Health Centre",
        "lg": "Pader",
        "expected": "Olok was listed as a completed health facility intended to serve its catchment in Pader.",
        "found": "The district health officer confirmed to the verification team that Olok Health Centre had not been constructed and did not exist in the district.",
        "gap": "The completed entry could not be matched to the intended facility. The reason for non-construction requires a documented resolution.",
        "action": "Pader District and the Ministry of Health should reconcile the approved project, construction and payment records, correct the beneficiary schedule and decide how the intended health-service need will be met."
      },
      {
        "case_id": "F02",
        "theme": "Invalid facility identity",
        "facility": "Busia Eastern Division health-centre entry",
        "lg": "Busia Municipal Council",
        "expected": "The beneficiary schedule should identify the particular health facility supported in Busia Municipality.",
        "found": "Reconciliation confirmed that no health facility called Busia Eastern Division existed. A separate return identified Sofia Health Centre III within Eastern Division.",
        "gap": "An administrative division had been used as a facility name. The available confirmation did not identify Sofia as its replacement or establish that the two names referred to the same beneficiary.",
        "action": "The municipality and Ministry of Health should resolve the original beneficiary identity and document the programme status of Sofia before linking or changing the two entries."
      },
      {
        "case_id": "F04",
        "theme": "Beneficiary replacements",
        "facility": "Ngomoromo, Oweko, Musandama and Loinya health centres",
        "lg": "Lamwo, Nebbi, Ntoroko and Maracha",
        "expected": "The beneficiary schedule should name the facility that received each planned investment.",
        "found": "Supervisors confirmed that Pangira replaced Ngomoromo in Lamwo, Pamaka replaced Oweko in Nebbi, Butungama replaced Musandama in Ntoroko, and Liko replaced Loinya in Maracha. Liko was already listed separately.",
        "gap": "The original and replacement names were not consistently linked. Leaving both active could count one investment twice or leave its location unclear.",
        "action": "The districts and Ministry of Health should attach the replacement decisions, link the original projects to their recipients and retain one active facility identity for each recipient."
      },
      {
        "case_id": "F05",
        "theme": "Assets moved to other facilities",
        "facility": "Alangi, Ther-uru and Abanga",
        "lg": "Zombo",
        "expected": "Asset locations and custodians should agree with the facilities holding and using the equipment.",
        "found": "The supervisor confirmed that Alangi, Ther-uru and Abanga existed, but their UgIFT assets had moved respectively to Amwonyo Health Centre, Atyak Health Centre and Kango Seed Secondary School.",
        "gap": "The original beneficiary names no longer described where the assets were held. Custody, location and the service arrangements at the original sites needed to be made clear.",
        "action": "Zombo District should reconcile transfer approvals and signed receipts with both sets of inventories, name the current custodians and confirm how the original catchments are served."
      },
      {
        "case_id": "F06",
        "theme": "Facilities outside programme scope",
        "facility": "Alira Health Centre and Kiziranfumbi Seed Secondary School",
        "lg": "Oyam and Kikuube",
        "expected": "The programme beneficiary schedule should include institutions supported under UgIFT.",
        "found": "The later Oyam clarification confirmed that Alira Health Centre existed but was not among the facilities upgraded under UgIFT. The supervisor also confirmed that Kiziranfumbi Seed Secondary School in Kikuube was outside the programme.",
        "gap": "The list confused the existence of an institution with its eligibility as a UgIFT beneficiary. Alira had initially been reported absent, but that account was corrected.",
        "action": "The local governments and sector ministries should approve the scope corrections, remove the institutions from the active UgIFT schedule and preserve the reasons for the changes."
      },
      {
        "case_id": "F07",
        "theme": "Existing facilities without UgIFT assets",
        "facility": "Pandwong Health Centre; Bumbaire, Kyamuhunga and Kashenshero schools; Rwamujojo Health Centre",
        "lg": "Kitgum Municipal Council, Bushenyi, Mitooma and Sheema Municipal Council",
        "expected": "Each listed beneficiary should have a supported account of the programme assistance it received.",
        "found": "Supervisors confirmed that Pandwong Health Centre, Bumbaire and Kyamuhunga schools, Kashenshero school and Rwamujojo Health Centre existed but had not benefited from UgIFT assets.",
        "gap": "Their appearance on the beneficiary list did not establish delivery. The cause of the difference between the list and the reported benefits needs to be resolved.",
        "action": "The responsible districts, municipalities and sector ministries should check beneficiary approvals and delivery records, then correct the schedule or record an approved outstanding delivery with an accountable officer and follow-up date."
      },
      {
        "case_id": "F08",
        "theme": "Names and aliases",
        "facility": "Bussi/Zinga and Dabani/Buwumba",
        "lg": "Wakiso and Busia",
        "expected": "Each facility should have one stable identity, with local and former names linked to it.",
        "found": "Bussi was confirmed to be the village name for the already-listed Zinga Health Centre in Wakiso. In Busia, the Buwumba return was reconciled to the master entry named Dabani.",
        "gap": "Different names could make one facility appear to be two, distort coverage and separate its asset history from the correct institution.",
        "action": "The districts should adopt the confirmed operating names, retain the old names as aliases and link the beneficiary, project and asset information to one facility identifier. Zinga should be counted once."
      }
    ],
    "incomplete_facilities": [
      {
        "case_id": "F09",
        "theme": "Incomplete school and equipment awaiting use",
        "facility": "Got Apwoyo Seed Secondary School",
        "lg": "Nwoya",
        "expected": "Got Apwoyo was intended to provide secondary education with completed buildings and installed ICT equipment.",
        "found": "The team found construction continuing and the school uncommissioned. Its ICT package remained at Nwoya District headquarters, while delivered furniture and structures had not been brought into use.",
        "gap": "The assets were not yet supporting teaching at the intended school, and custody was divided between the district and the site.",
        "action": "Nwoya District and the Ministry of Education should set a completion and handover plan, check the stored equipment, and arrange installation, testing and signed transfer when the school is ready."
      },
      {
        "case_id": "F10",
        "theme": "Construction damage and displaced service delivery",
        "facility": "Bukibologoto Health Centre",
        "lg": "Bulambuli",
        "expected": "Bukibologoto was listed as complete and was intended to provide care from the constructed health facility.",
        "found": "The team found that mudslides had damaged the works before completion. A corner was undermined and a wall cracked. Care was being provided at Simu subcounty offices, with equipment held in district stores.",
        "gap": "The planned facility was unavailable for its intended use, and the temporary service and storage arrangements needed a lasting solution.",
        "action": "Bulambuli District and the Ministry of Health should obtain an engineering assessment, decide on repair or relocation, inventory the equipment and provide for continuing care."
      },
      {
        "case_id": "F11",
        "theme": "Incomplete works and site readiness",
        "facility": "Kyangwali Seed Secondary School",
        "lg": "Kikuube",
        "expected": "Kyangwali school needed completed works, electricity, security and handover to use its assets fully.",
        "found": "The team recorded continuing construction. The school reported a lack of electricity and an incomplete perimeter fence, and the facility had not been handed over.",
        "gap": "Finishing the buildings alone would not make the school ready: power, security and responsibility for the assets also remained unresolved.",
        "action": "Kikuube District, the Ministry of Education and the contractor should close these requirements through one readiness plan, followed by joint testing and handover. The plan should name who will operate, safeguard and maintain the assets."
      },
      {
        "case_id": "F12",
        "theme": "Incomplete works and unopened equipment",
        "facility": "Sidok Seed Secondary School",
        "lg": "Kaabong",
        "expected": "Sidok school needed completed buildings and checked equipment before the investment could support full operations.",
        "found": "The team found blocks, a kitchen and toilets under construction, with termite workings on the plaster of two blocks. The school consignment remained unopened and its contents had not been counted.",
        "gap": "Both unfinished works and unchecked equipment prevented a complete assessment of readiness for use.",
        "action": "Kaabong District should secure completion and treatment of the affected works, then arrange a witnessed opening, count and condition check of the equipment. Accepted items should be recorded, assigned to custodians and issued for use."
      },
      {
        "case_id": "F14",
        "theme": "Installation and commissioning outstanding",
        "facility": "Buwagogo Seed Secondary School",
        "lg": "Manafwa",
        "expected": "Buwagogo school was intended to use its supplied ICT equipment for teaching.",
        "found": "The team found the March 2024 ICT consignment still boxed in the store, with contractor installation pending and commissioning delayed.",
        "gap": "Delivery had not translated into operational ICT capacity. Equipment continued to require secure custody while installation remained outstanding.",
        "action": "Manafwa District and the Ministry of Education should agree an installation and commissioning date with the contractor, reconcile the stored equipment against delivery records and test it before acceptance. The handover should assign responsibility for operation, maintenance and reporting of faults."
      }
    ],
    "ground_only_paragraphs": [
      "Teams submitted information under 24 facility names that had no confirmed match to the verification master list. Follow-up expressly confirmed Rukoki General Hospital, Silumira Health Centre III and Bukuuku Community Seed Secondary School as additional programme beneficiaries. Their inclusion in the approved programme account should be regularised.",
      "The remaining names should be resolved through the same checks of facility identity, programme approval and asset custody. Some entries came from combined returns, and Onywako was expressly reported without a physical inspection. All 24 return names are shown separately from the 629 master-list entries while the outstanding identity and scope decisions are completed."
    ],
    "ground_only_examples": [
      {
        "case_id": "F17",
        "facility": "Rukoki General Hospital",
        "lg": "Kasese Municipality",
        "expected": "Confirmed beneficiaries should be included in the programme account.",
        "found": "The supervisor confirmed that Rukoki General Hospital was a UgIFT beneficiary in Kasese Municipality, although it was absent from the master list used for verification.",
        "gap": "The programme list omitted a confirmed recipient.",
        "action": "The Ministry of Health and municipality should approve the beneficiary entry and link its asset information to a stable facility identifier."
      },
      {
        "case_id": "F17",
        "facility": "Silumira Health Centre III",
        "lg": "Kakumiro",
        "expected": "The beneficiary schedule should include supported health facilities.",
        "found": "The supervisor confirmed that Silumira Health Centre III had benefited in Kakumiro but was not on the master list.",
        "gap": "The facility was missing from the list used to plan and account for verification.",
        "action": "Kakumiro District and the Ministry of Health should approve the addition and connect the beneficiary decision to the facility asset inventory."
      },
      {
        "case_id": "F16",
        "facility": "Bukuuku Community Seed Secondary School",
        "lg": "Fort Portal City",
        "expected": "Confirmed seed-school beneficiaries should appear in the programme account, with assets handed over for full use.",
        "found": "Bukuuku was confirmed as an additional beneficiary. The team recorded improved science and computer teaching following laboratory construction, while some asset handover remained pending.",
        "gap": "The school was omitted from the master list and handover was incomplete.",
        "action": "The city and Ministry of Education should regularise the beneficiary entry and complete joint handover of the outstanding assets."
      }
    ]
  }
}
```


## Revision evidence: reconciliation/stored_explicit_good.json

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


## Revision evidence: narrative/national_maintenance.json

```json
{
  "by_book": {
    "MOFPED BK": [
      {
        "prose": "The acquisition records for desktop computers specify a 1 year warranty.",
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 210447,
        "item": "Lenovo Desktop Computer",
        "raw_evidence_without_identity": "Room 5.1;  Supplier IT OFFICE (U) LTD; Warranty 1 Year; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT .ASSETS REGISTER-BPED.xls; _multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT CONSOLIDATED FIXED ASSETS REGISTER FOR FY2020.2021. 2021.2022.2023.2024 AND 2024.2025.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 7"
      },
      {
        "prose": "The procurement entry for a heavy duty photocopier also specifies a 1 year warranty and describes it as in good working condition.",
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 209567,
        "item": "Toyota Hilux Double Cabin Pickup",
        "raw_evidence_without_identity": "The MoWT Recommend the ministry of Finance for the good work done since the do all the repair and servicing of the vechicle.; Source status: In Good condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/MDA status register.xlsx",
        "source_location": "MoWT row 4"
      },
      {
        "prose": "The acquisition record for a heavy duty photocopier specifies a 1 year warranty.",
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 210942,
        "item": "Computer Tablet",
        "raw_evidence_without_identity": "Supplier Tel Care Ltd; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT ASSETS REGISTER FOR FY2023.2024 FOR AUDITORS.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 468"
      },
      {
        "prose": "The printer entry specifies a 3 year warranty and describes the equipment as in good working condition.",
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
        "sheet": "Asset Register",
        "row": 214539,
        "item": "Lenovo LOQ 16IRH8-i7 Laptop",
        "raw_evidence_without_identity": "Supplier Millenniu Minfosys Ltd; Warranty 1 Year; Source status: Good working condition; ",
        "source_file": "raw-data-grouped/_multi-team/programme-documents/All WIP Ugift/All WIP Ugift/fwdugiftassets/UGIFT ASSETS REGISTER FOR FY2023.2024 FOR AUDITORS.xls",
        "source_location": "COMPUTERS AND IT EQUIPMENT row 4073"
      },
      {
        "prose": "The motorcycle procurement entry also specifies a 1 year warranty.",
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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
        "register": "outputs/asset-register/REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx",
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


## Revision evidence: geography_final_check.json

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


# Supplemental report photographs

Source files remain unchanged. Each full source photograph was visually inspected; copies use only rotation, cropping and resizing, with JPEG output at at most 1600 pixels on the long side. No retouching was applied. User authorized additional photographs beyond the original maximum.

National source review: central-government programme documents contained distribution records, spreadsheets and correspondence rather than an attributable asset photograph. No national photograph was added.

## P11: Unfinished school block at Got Apwoyo Seed Secondary School, Nwoya District (Acholi).
- Copy: `outputs/narrative-report/figures/photo_11_got_apwoyo_construction.jpg`
- Source: `raw-data-grouped/team-01/Nwoya/_district-documents/UGIFT_Asset_Verification_Nwoya Report.docx`
- Locator: word/media/image1.jpeg; body block 31.
- Context: Nwoya district report body block 7 identifies Got Apwoyo Seed Secondary School. Blocks 10 to 14 describe ongoing construction, no commissioning, and ICT held at the district. Field photographs begin at block 30; image1.jpeg occurs at block 31.
- Field point: Construction and commissioning were pending; ICT was held by the district education department.
- Theme: construction; dimensions: 1008 x 636 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P12: Building works at a seed secondary school, Kiboga District (Buganda).
- Copy: `outputs/narrative-report/figures/photo_12_lwamata_construction.jpg`
- Source: `raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx`
- Locator: word/media/image6.jpeg; body block 79.
- Context: Lwamata school return body block 11 identifies the school, block 33 states that some buildings remain under construction and laboratory equipment was expected after structures were completed. Image6.jpeg is at block 79 after PICTURES OF ASSETS VISITED AND VERIFIED.
- Field point: Construction remained in progress; the ICT and chemistry laboratories had furniture while equipment delivery was expected after construction.
- Theme: construction; dimensions: 472 x 476 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P13: School block awaiting completion at Butungama Seed Secondary School, Ntoroko District (Tooro).
- Copy: `outputs/narrative-report/figures/photo_13_butungama_construction.jpg`
- Source: `raw-data-grouped/team-26/_team-documents/Butungama Seed School.pdf`
- Locator: PDF page 7, image 1; body block not applicable.
- Context: Photographic PDF page 7; the school sign appears on page 3. The paired return raw-data-grouped/team-26/Ntoroko/Butungama-Seed-Secondary-School/ASSET VERIFICATION AND RECORDING TOOL KIT 222 BUTUNGAMA HEALTH CENTRE III AND BUTUNGAMA SEED SCHOOL (1).docx, body blocks 113, 119 and 178 identify the school and ongoing construction.
- Field point: The return records buildings under construction, with school equipment still stored.
- Theme: construction; dimensions: 810 x 518 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P14: Cracked health centre block above collapsed ground, Bulambuli District (Bugisu).
- Copy: `outputs/narrative-report/figures/photo_14_bulambuli_structural_damage.jpg`
- Source: `raw-data-grouped/team-14/Bulambuli/Bukibologoto-HC-II/08_block-over-collapsed-ground-wide_ref20260911-0005.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 08_block-over-collapsed-ground-wide_ref20260911-0005.jpg. Facility and local government are established by its Bukibologoto-HC-II/Bulambuli source folders.
- Field point: Visible cracking and ground loss beneath a health centre building illustrate structural and site-maintenance risks; no engineering cause is inferred.
- Theme: damage; dimensions: 940 x 550 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P15: Stained and peeling ceiling at a health centre, Sironko District (Bugisu).
- Copy: `outputs/narrative-report/figures/photo_15_sironko_damaged_ceiling.jpg`
- Source: `raw-data-grouped/team-14/Sironko/Bundege-HC-III/15_water-damaged-ceiling_ref20260829-0569.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 15_water-damaged-ceiling_ref20260829-0569.jpg under Bundege-HC-III/Sironko.
- Field point: The visible ceiling damage illustrates a need for building maintenance. The source image is labelled water-damaged ceiling.
- Theme: damage; dimensions: 1080 x 729 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P16: Water tank on a cracked base at a seed secondary school, Kibuku District (Bukedi).
- Copy: `outputs/narrative-report/figures/photo_16_kibuku_cracked_tank_base.jpg`
- Source: `raw-data-grouped/team-12/Kibuku/Kasasira-Seed-Secondary-School/39_water-tank-on-cracked-base_ref0332.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 39_water-tank-on-cracked-base_ref0332.jpg under Kasasira-Seed-Secondary-School/Kibuku.
- Field point: Visible cracking in the tank support illustrates a utility-asset maintenance concern; cause and structural safety are not inferred.
- Theme: damage; dimensions: 912 x 999 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P17: Boxed desktop computers at a seed secondary school, Karenga District (Karamoja).
- Copy: `outputs/narrative-report/figures/photo_17_karenga_boxed_computers.jpg`
- Source: `raw-data-grouped/team-11/Karenga/Kapedo-Seed-Secondary-School/08_boxed-desktop-computers-stacked_ref20260829-0159.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 08_boxed-desktop-computers-stacked_ref20260829-0159.jpg under Kapedo-Seed-Secondary-School/Karenga.
- Field point: Computer cartons are stacked at the school. The image supports boxed storage but does not establish the reason or duration.
- Theme: storage; dimensions: 787 x 1600 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P18: Stacked desks, chairs and stools at a seed secondary school, Napak District (Karamoja).
- Copy: `outputs/narrative-report/figures/photo_18_napak_stacked_furniture.jpg`
- Source: `raw-data-grouped/team-10/Napak/Napak-Seed-Secondary-School/25_furniture-some-broken-none-engraved_ref20260827-0417.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 25_furniture-some-broken-none-engraved_ref20260827-0417.jpg under Napak-Seed-Secondary-School/Napak.
- Field point: The source describes some furniture as broken and none engraved. The caption confines itself to the visible stacked school furniture.
- Theme: storage; dimensions: 563 x 690 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P19: Clinical equipment packed among cartons at a health centre, Hoima City (Bunyoro).
- Copy: `outputs/narrative-report/figures/photo_19_hoima_stored_clinical_equipment.jpg`
- Source: `raw-data-grouped/_multi-team/programme-documents/data-management-chat/unpacked/TEAM 25 HEALTH CENTHERA/TEAM 25 HEALTH CENTHERA/KIHUUKYA HEALTH CENTER III/kihuukya photos/stored equipement nort in use.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph in the KIHUUKYA HEALTH CENTER III/kihuukya photos folder. It is byte-identical (SHA256 a76c46aa7f6ab2856ac601a320125dfdf7cb174a6ec0c29eec25dab06232de97) to the team-25/_team-documents copy. The KIHUUKYA HEALTHCENTER III. Edited.docx return, block 29, identifies Hoima City and Bunyoro; block 38 names the facility.
- Field point: The source file identifies stored equipment not in use. Cropping removes manufacturer contact details at the left edge.
- Theme: storage; dimensions: 526 x 983 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P20: Laboratory stools and other school furniture in storage, Ntoroko District (Tooro).
- Copy: `outputs/narrative-report/figures/photo_20_butungama_stored_furniture.jpg`
- Source: `raw-data-grouped/team-26/_team-documents/Butungama Seed School.pdf`
- Locator: PDF page 12, image 1; body block not applicable.
- Context: Photographic PDF page 12. The paired return raw-data-grouped/team-26/Ntoroko/Butungama-Seed-Secondary-School/ASSET VERIFICATION AND RECORDING TOOL KIT 222 BUTUNGAMA HEALTH CENTRE III AND BUTUNGAMA SEED SCHOOL (1).docx, body block 162, records laboratory stools, desks, office chairs and tables in good condition but not in use, still stored. Blocks 119 and 178 describe ongoing construction.
- Field point: Good furniture had been delivered but remained stored while the school was under construction.
- Theme: storage; dimensions: 810 x 907 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P21: Boxed pulse oximeters at a health centre, Makindye-Ssabagabo Municipal Council (Buganda).
- Copy: `outputs/narrative-report/figures/photo_21_kibiri_boxed_oximeters.jpg`
- Source: `raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`
- Locator: word/media/image17.jpeg; body block 77.
- Context: Kibiri Health Centre III report image17.jpeg, body block 77. Blocks 1 and 5 identify Kibiri; the packaging explicitly identifies Handheld Pulse Oximeter.
- Field point: The photographed clinical equipment remained in packaging at the time of the photograph. The image alone does not establish functionality or duration of storage.
- Theme: storage; dimensions: 963 x 729 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P22: UgIFT engraving on a health centre bench, Bududa District (Bugisu).
- Copy: `outputs/narrative-report/figures/photo_22_bududa_bench_engraving.jpg`
- Source: `raw-data-grouped/team-14/Bududa/Bududa-HC-III/09_bench-engraved-gou-moh-ugift-project_ref20260827-0187.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 09_bench-engraved-gou-moh-ugift-project_ref20260827-0187.jpg under Bududa-HC-III/Bududa. Visible institutional marking reads GOU/MOH-UGIFT PROJECT and F/Y 2023/2024.
- Field point: A close view documents programme identification on furniture; engraving does not establish current functionality.
- Theme: engraving; dimensions: 1000 x 435 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P23: Building works and construction materials at Ndhew Seed Secondary School, Nebbi District (West Nile).
- Copy: `outputs/narrative-report/figures/photo_23_ndhew_construction.jpg`
- Source: `raw-data-grouped/team-01/Nebbi/_district-documents/UGIFT Assets Verification Nebbi District Report.docx`
- Locator: word/media/image17.jpeg; body block 89.
- Context: Nebbi district report image17.jpeg at body block 89, within the Ndhew school section beginning at block 40 and field photographs beginning at block 63. Block 42 records ongoing construction and ICT/science equipment at district headquarters; block 59 links construction delay with equipment installation delay.
- Field point: Unfinished construction prevented equipment installation, with ICT and science equipment held at district headquarters.
- Theme: construction; dimensions: 1280 x 691 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P24: Unfinished brickwork at a seed secondary school, Karenga District (Karamoja).
- Copy: `outputs/narrative-report/figures/photo_24_lokori_brickwork.jpg`
- Source: `raw-data-grouped/team-11/Karenga/Lokori-Seed-Secondary-School/01_brickwork-under-construction_ref20260829-0980.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 01_brickwork-under-construction_ref20260829-0980.jpg under Lokori-Seed-Secondary-School/Karenga.
- Field point: Exposed brickwork and foundation courses show the stage of building works photographed; the image does not establish the completion timetable.
- Theme: construction; dimensions: 1600 x 1200 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P25: Damaged drip stand at a health centre, Moroto District (Karamoja).
- Copy: `outputs/narrative-report/figures/photo_25_moroto_broken_drip_stand.jpg`
- Source: `raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/124_broken-drip-stand_ref20260827-0349.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 124_broken-drip-stand_ref20260827-0349.jpg under Kalemungole-HC-III/Moroto. The stand lacks its supporting base. Crop retains the stand and a gloved hand; no face or identifier is present.
- Field point: A broken clinical support item illustrates the maintenance needs of health equipment.
- Theme: damage; dimensions: 365 x 972 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P26: Unfinished laboratory building at a health centre, Sironko District (Bugisu).
- Copy: `outputs/narrative-report/figures/photo_26_sironko_unfinished_health_lab.jpg`
- Source: `raw-data-grouped/team-14/Sironko/Simu-Pondo-HC-III/06_unfinished-laboratory-building_ref20260829-0541.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 06_unfinished-laboratory-building_ref20260829-0541.jpg under Simu-Pondo-HC-III/Sironko.
- Field point: The laboratory shell was photographed before roofing and finishing.
- Theme: construction; dimensions: 1080 x 672 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P27: Broken desk frame at a seed secondary school, Namisindwa District (Bugisu).
- Copy: `outputs/narrative-report/figures/photo_27_namisindwa_broken_desk.jpg`
- Source: `raw-data-grouped/team-13/Namisindwa/Namboko/032_broken-desk_ref20260902-0126.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 032_broken-desk_ref20260902-0126.jpg under Namboko/Namisindwa.
- Field point: The bent and detached desk frame documents damaged school furniture.
- Theme: damage; dimensions: 1228 x 648 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P28: Cracked desk surface bearing a school marking, Tororo District (Bukedi).
- Copy: `outputs/narrative-report/figures/photo_28_tororo_cracked_desktop.jpg`
- Source: `raw-data-grouped/team-13/Tororo/Iyolwa/107_desk-marked-iyolwa-seed-ss-cracked-corner_ref20260830-0799.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 107_desk-marked-iyolwa-seed-ss-cracked-corner_ref20260830-0799.jpg under Iyolwa/Tororo. The institutional school name appears on the wood; no personal name is present.
- Field point: Identification and physical condition are separate concerns: the desk is marked and its wooden surface is cracked.
- Theme: damage; dimensions: 590 x 1088 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P29: Damaged chair back joint at a seed secondary school, Budaka District (Bukedi).
- Copy: `outputs/narrative-report/figures/photo_29_budaka_damaged_chair.jpg`
- Source: `raw-data-grouped/team-12/Budaka/Nansanga-Seed-Secondary-School/086_chair-back-rail-broken-at-the-joint_ref0700.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 086_chair-back-rail-broken-at-the-joint_ref0700.jpg under Nansanga-Seed-Secondary-School/Budaka.
- Field point: The photograph documents damage at the chair back joint.
- Theme: damage; dimensions: 591 x 998 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P30: Hospital beds and screens stacked in storage at a health centre, Kagadi District (Bunyoro).
- Copy: `outputs/narrative-report/figures/photo_30_kagadi_beds_in_storage.jpg`
- Source: `raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/BEDS IN STORAGE .jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph BEDS IN STORAGE .jpg under Kyabasara-HC-III/Kagadi. The source filename and visible stacking identify storage.
- Field point: Beds and privacy screens occupied a storage area; the photograph alone does not establish the reason for storage.
- Theme: storage; dimensions: 705 x 1015 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P31: Biology laboratory under construction at a seed secondary school, Buliisa District (Bunyoro).
- Copy: `outputs/narrative-report/figures/photo_31_buliisa_laboratory_works.jpg`
- Source: `raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/boilogy lab under construction.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph boilogy lab under construction.jpg under Kihungya-Seed-Secondary-School/Buliisa. kihungya seed school.docx body block 107 identifies the science block as not in use and under construction; block 63 states that most structures were not ready and there was no electricity for ICT sessions or water for sanitation.
- Field point: Construction and utility provision affected readiness of teaching facilities; the science block was recorded as not in use.
- Theme: construction; dimensions: 1040 x 780 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P32: Flood-affected older health facility at Butiaba, Buliisa District (Bunyoro).
- Copy: `outputs/narrative-report/figures/photo_32_buliisa_flood_affected_old_facility.jpg`
- Source: `raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/butaiba submurged facility.jpeg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph butaiba submurged facility.jpeg under Butiaba-HC-III/Buliisa. The paired butaiba report.docx body block 11 (paragraph 10) explicitly states that the old facility built by UgIFT and its equipment were affected by floods.
- Field point: The older UgIFT health facility was affected by flooding. The photograph does not imply that all current facilities or services are submerged.
- Theme: damage; dimensions: 1242 x 557 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P33: School buildings and courtyard at a seed secondary school, Buvuma District (Buganda).
- Copy: `outputs/narrative-report/figures/photo_33_buvuma_school_blocks.jpg`
- Source: `raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Image 2026-09-12 at 13.47.23 (3).jpeg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph WhatsApp Image 2026-09-12 at 13.47.23 (3).jpeg under Bweema-Seed-Secondary-School/Buvuma. The same source photo collection includes a school sign identifying Bweema and Buvuma.
- Field point: The school photographs document the physical facilities provided. The caption does not infer occupation or current service status.
- Theme: service delivery; dimensions: 1280 x 596 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P34: Raised water storage tank at a seed secondary school, Buvuma District (Buganda).
- Copy: `outputs/narrative-report/figures/photo_34_buvuma_raised_water_tank.jpg`
- Source: `raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Image 2026-09-12 at 13.47.25.jpeg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph WhatsApp Image 2026-09-12 at 13.47.25.jpeg under Bweema-Seed-Secondary-School/Buvuma.
- Field point: The elevated tank and support frame document water-storage infrastructure. Supply availability and functionality are not inferred from the photograph.
- Theme: service delivery; dimensions: 624 x 1280 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.

## P35: Empty computer laboratory at a seed secondary school, Kween District (Sebei).
- Copy: `outputs/narrative-report/figures/photo_35_kween_empty_computer_laboratory.jpg`
- Source: `raw-data-grouped/team-15/Kween/Kaptum-Seed-Secondary-School/09_computer-lab-no-power-supply_ref0537.jpg`
- Locator: Loose photograph; body block not applicable.
- Context: Loose photograph 09_computer-lab-no-power-supply_ref0537.jpg under Kaptum-Seed-Secondary-School/Kween. The source filename identifies the computer laboratory and no power supply.
- Field point: The photograph documents an empty computer laboratory. The no-power finding comes from the supplied source label, rather than being inferred visually.
- Theme: service delivery; dimensions: 1280 x 816 pixels.
- Privacy: Full source image inspected. Selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses.


# Expanded field photograph sources

50 additional photographs; IDs P36 onward. Karenga excluded. No generated photographs. Original source data unchanged. Cropping, rotation and downscaling only.

All source paths and technical locators are audit material, not report captions. Loose photographs are attributed through the supplied district/facility folder. Captions describe visible assets and do not establish functionality, duration, causation or programme funding by appearance alone.

## P36 — Solar panels at Kalemungole HC III, Moroto District (Karamoja).
- Source: `raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/102_water-system-solar-panels-and-tanks_ref20260827-0369.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 102_water-system-solar-panels-and-tanks_ref20260827-0369.jpg.'}
- Field point: Solar panels. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: utilities; crop fractions: [0.05, 0.23, 0.64, 0.9]; rotation: 0°; output: (637, 543).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_36_kalemungole_hc_iii_solar_panels.jpg`

## P37 — Patient toilet block at Kalemungole HC III, Moroto District (Karamoja).
- Source: `raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/108_patient-toilets_ref20260827-0367.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 108_patient-toilets_ref20260827-0367.jpg.'}
- Field point: Patient toilet block. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: sanitation; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (810, 1080).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_37_kalemungole_hc_iii_patient_toilet_block.jpg`

## P38 — Programme engraving on a weighing scale at Kalemungole HC III, Moroto District (Karamoja).
- Source: `raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/10_engraving-weighing-scale_ref20260826-0429.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 10_engraving-weighing-scale_ref20260826-0429.jpg.'}
- Field point: Programme engraving on a weighing scale. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: engraving; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1280, 720).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_38_kalemungole_hc_iii_programme_engraving_on_a_weighing_scale.jpg`

## P39 — Programme engraving on a delivery bed at Kalemungole HC III, Moroto District (Karamoja).
- Source: `raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/37_engraving-delivery-bed_ref20260826-0456.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 37_engraving-delivery-bed_ref20260826-0456.jpg.'}
- Field point: Programme engraving on a delivery bed. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: engraving; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1280, 720).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_39_kalemungole_hc_iii_programme_engraving_on_a_delivery_bed.jpg`

## P40 — Oxygen concentrator at Kalemungole HC III, Moroto District (Karamoja).
- Source: `raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/40_oxygen-concentrator_ref20260826-0459.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 40_oxygen-concentrator_ref20260826-0459.jpg.'}
- Field point: Oxygen concentrator. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: clinical equipment; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (540, 960).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_40_kalemungole_hc_iii_oxygen_concentrator.jpg`

## P41 — Suction apparatus at Kalemungole HC III, Moroto District (Karamoja).
- Source: `raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/50_suction-apparatus_ref20260826-0469.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 50_suction-apparatus_ref20260826-0469.jpg.'}
- Field point: Suction apparatus. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: clinical equipment; crop fractions: [0, 0.12, 1, 0.87]; rotation: 0°; output: (540, 720).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_41_kalemungole_hc_iii_suction_apparatus.jpg`

## P42 — Wheelchair with programme marking at Kalemungole HC III, Moroto District (Karamoja).
- Source: `raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/69_wheelchair-marked-gou-moh-ugift_ref20260826-0488.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Moroto / Kalemungole-HC-III; original filename: 69_wheelchair-marked-gou-moh-ugift_ref20260826-0488.jpg.'}
- Field point: Wheelchair with programme marking. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: clinical equipment; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (540, 960).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_42_kalemungole_hc_iii_wheelchair_with_programme_marking.jpg`

## P43 — Borehole apron and pipework at Katikekire Seed School, Moroto District (Karamoja).
- Source: `raw-data-grouped/team-10/Moroto/Katikekire-Seed-School/02_borehole-apron-and-pipework_ref20260826-0421.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Moroto / Katikekire-Seed-School; original filename: 02_borehole-apron-and-pipework_ref20260826-0421.jpg.'}
- Field point: Borehole apron and pipework. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: utilities; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (810, 1080).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_43_katikekire_seed_school_borehole_apron_and_pipework.jpg`

## P44 — Classroom furniture with school markings at Rupa Seed School, Moroto District (Karamoja).
- Source: `raw-data-grouped/team-10/Moroto/Rupa-Seed-School/18_classroom-furniture-engraved-rupa-seed_ref20260909-photo-p08.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Moroto / Rupa-Seed-School; original filename: 18_classroom-furniture-engraved-rupa-seed_ref20260909-photo-p08.jpg.'}
- Field point: Classroom furniture with school markings. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: engraving; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1240, 930).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_44_rupa_seed_school_classroom_furniture_with_school_markings.jpg`

## P45 — Section of the science laboratory exterior at Iriiri Seed Secondary School, Napak District (Karamoja).
- Source: `raw-data-grouped/team-10/Napak/Iriiri-Seed-Secondary-School/33_science-laboratory_ref20260827-0463.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Napak / Iriiri-Seed-Secondary-School; original filename: 33_science-laboratory_ref20260827-0463.jpg.'}
- Field point: Section of the science laboratory exterior. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: buildings; crop fractions: [0.48, 0.28, 0.91, 0.73]; rotation: 0°; output: (430, 338).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_45_iriiri_seed_secondary_school_section_of_the_science_laboratory_exterior.jpg`

## P46 — Water storage tanks at Lopei Seed Secondary School, Napak District (Karamoja).
- Source: `raw-data-grouped/team-10/Napak/Lopei-Seed-Secondary-School/20_water-tanks_ref20260828-0562.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Napak / Lopei-Seed-Secondary-School; original filename: 20_water-tanks_ref20260828-0562.jpg.'}
- Field point: Water storage tanks. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: utilities; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (810, 1080).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_46_lopei_seed_secondary_school_water_storage_tanks.jpg`

## P47 — Boxed desktop computers at Alerek Seed Secondary School, Abim District (Karamoja).
- Source: `raw-data-grouped/team-11/Abim/Alerek-Seed-Secondary-School/07_boxed-desktop-computers-in-the-store_ref0769.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Abim / Alerek-Seed-Secondary-School; original filename: 07_boxed-desktop-computers-in-the-store_ref0769.jpg.'}
- Field point: Boxed desktop computers. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: storage; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1600, 1200).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_47_alerek_seed_secondary_school_boxed_desktop_computers.jpg`

## P48 — Laboratory reagent containers at Alerek Seed Secondary School, Abim District (Karamoja).
- Source: `raw-data-grouped/team-11/Abim/Alerek-Seed-Secondary-School/44_laboratory-chemicals-on-the-bench_ref0859.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Abim / Alerek-Seed-Secondary-School; original filename: 44_laboratory-chemicals-on-the-bench_ref0859.jpg.'}
- Field point: Laboratory reagent containers. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: laboratory; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1600, 1200).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_48_alerek_seed_secondary_school_laboratory_reagent_containers.jpg`

## P49 — Boxed printer and equipment at Sidok Seed Secondary School, Kaabong District (Karamoja).
- Source: `raw-data-grouped/team-11/Kaabong/Sidok-Seed-Secondary-School/05_boxed-printer-and-equipment_ref0317.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kaabong / Sidok-Seed-Secondary-School; original filename: 05_boxed-printer-and-equipment_ref0317.jpg.'}
- Field point: Boxed printer and equipment. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: storage; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1600, 1200).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_49_sidok_seed_secondary_school_boxed_printer_and_equipment.jpg`

## P50 — Unfinished classroom block at Sidok Seed Secondary School, Kaabong District (Karamoja).
- Source: `raw-data-grouped/team-11/Kaabong/Sidok-Seed-Secondary-School/16_classroom-block-under-construction_ref0316.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kaabong / Sidok-Seed-Secondary-School; original filename: 16_classroom-block-under-construction_ref0316.jpg.'}
- Field point: Unfinished classroom block. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: construction; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1600, 1200).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_50_sidok_seed_secondary_school_unfinished_classroom_block.jpg`

## P51 — Latrine block under construction at Sidok Seed Secondary School, Kaabong District (Karamoja).
- Source: `raw-data-grouped/team-11/Kaabong/Sidok-Seed-Secondary-School/33_latrine-block-under-construction_ref0310.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kaabong / Sidok-Seed-Secondary-School; original filename: 33_latrine-block-under-construction_ref0310.jpg.'}
- Field point: Latrine block under construction. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: construction; crop fractions: [0, 0, 1, 0.68]; rotation: 0°; output: (1600, 816).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_51_sidok_seed_secondary_school_latrine_block_under_construction.jpg`

## P52 — Oxygen concentrator at Kamoru HC III, Kotido District (Karamoja).
- Source: `raw-data-grouped/team-11/Kotido/Kamoru-HC-III/15_oxygen-concentrator_ref1167.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kotido / Kamoru-HC-III; original filename: 15_oxygen-concentrator_ref1167.jpg.'}
- Field point: Oxygen concentrator. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: clinical equipment; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1200, 1600).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_52_kamoru_hc_iii_oxygen_concentrator.jpg`

## P53 — Programme engraving on a table at Kamoru HC III, Kotido District (Karamoja).
- Source: `raw-data-grouped/team-11/Kotido/Kamoru-HC-III/18_engraved-table-top_ref1107.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kotido / Kamoru-HC-III; original filename: 18_engraved-table-top_ref1107.jpg.'}
- Field point: Programme engraving on a table. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: engraving; crop fractions: (0, 0, 1, 1); rotation: 180°; output: (1600, 1200).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_53_kamoru_hc_iii_programme_engraving_on_a_table.jpg`

## P54 — Water storage tanks at Rengen Seed School, Kotido District (Karamoja).
- Source: `raw-data-grouped/team-11/Kotido/Rengen-Seed-School/10_water-tanks-x2_ref0642.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kotido / Rengen-Seed-School; original filename: 10_water-tanks-x2_ref0642.jpg.'}
- Field point: Water storage tanks. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: utilities; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1600, 900).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_54_rengen_seed_school_water_storage_tanks.jpg`

## P55 — Medical-waste bins and ward beds at Butiaba HC III, Buliisa District (Bunyoro).
- Source: `raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/dust bins.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Buliisa / Butiaba-HC-III; original filename: dust bins.jpg.'}
- Field point: Medical-waste bins and ward beds. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: clinical equipment; crop fractions: (0, 0.18, 1, 1); rotation: 0°; output: (1600, 984).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_55_butiaba_hc_iii_medical_waste_bins_and_ward_beds.jpg`

## P56 — Laboratory centrifuge at Butiaba HC III, Buliisa District (Bunyoro).
- Source: `raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/IMG-20260907-WA0097.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Buliisa / Butiaba-HC-III; original filename: IMG-20260907-WA0097.jpg.'}
- Field point: Laboratory centrifuge. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: laboratory; crop fractions: (0.08, 0.01, 1, 0.79); rotation: 0°; output: (1416, 1600).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_56_butiaba_hc_iii_laboratory_centrifuge.jpg`

## P57 — Unfinished laboratory interior at Kihungya Seed Secondary School, Buliisa District (Bunyoro).
- Source: `raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/IMG-20260905-WA0028.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Buliisa / Kihungya-Seed-Secondary-School; original filename: IMG-20260905-WA0028.jpg.'}
- Field point: Unfinished laboratory interior. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: construction; crop fractions: (0, 0.08, 1, 1); rotation: 0°; output: (1040, 718).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_57_kihungya_seed_secondary_school_unfinished_laboratory_interior.jpg`

## P58 — Library interior under construction at Kihungya Seed Secondary School, Buliisa District (Bunyoro).
- Source: `raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/library.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Buliisa / Kihungya-Seed-Secondary-School; original filename: library.jpg.'}
- Field point: Library interior under construction. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: construction; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1040, 780).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_58_kihungya_seed_secondary_school_library_interior_under_construction.jpg`

## P59 — Stacked classroom furniture at King Solomon Seed Secondary School, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115519_265.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115519_265.jpg.'}
- Field point: Stacked classroom furniture. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: storage; crop fractions: (0, 0.12, 1, 1); rotation: 0°; output: (1600, 1056).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_59_king_solomon_seed_secondary_school_stacked_classroom_furniture.jpg`

## P60 — Classroom desks at King Solomon Seed Secondary School, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115826_769.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115826_769.jpg.'}
- Field point: Classroom desks. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: school furniture; crop fractions: (0, 0.12, 1, 1); rotation: 0°; output: (1600, 1056).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_60_king_solomon_seed_secondary_school_classroom_desks.jpg`

## P61 — School engraving on wooden furniture at King Solomon Seed Secondary School, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115836_836.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_115836_836.jpg.'}
- Field point: School engraving on wooden furniture. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: engraving; crop fractions: (0, 0.18, 1, 1); rotation: 0°; output: (1600, 984).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_61_king_solomon_seed_secondary_school_school_engraving_on_wooden_furniture.jpg`

## P62 — Boxed projector and other equipment at King Solomon Seed Secondary School, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_120857_349.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_120857_349.jpg.'}
- Field point: Boxed projector and other equipment. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: storage; crop fractions: (0.15, 0, 1, 0.96); rotation: 0°; output: (1600, 1355).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_62_king_solomon_seed_secondary_school_boxed_projector_and_other_equipment.jpg`

## P63 — Gas cylinders and pipework at King Solomon Seed Secondary School, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_121503_686.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kagadi / King-Solomon-Seed-Secondary-School; original filename: IMG_20260901_121503_686.jpg.'}
- Field point: Gas cylinders and pipework. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: utilities; crop fractions: (0, 0.08, 1, 0.98); rotation: 0°; output: (1333, 1600).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_63_king_solomon_seed_secondary_school_gas_cylinders_and_pipework.jpg`

## P64 — Programme engraving on a table at Kyabasara HC III, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/IMG-20260908-WA0107.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: IMG-20260908-WA0107.jpg.'}
- Field point: Programme engraving on a table. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: engraving; crop fractions: (0, 0.43, 1, 0.84); rotation: 0°; output: (810, 443).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_64_kyabasara_hc_iii_programme_engraving_on_a_table.jpg`

## P65 — Kangaroo care chair at Kyabasara HC III, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/kangaro chair.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: kangaro chair.jpg.'}
- Field point: Kangaroo care chair. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: clinical equipment; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (810, 1080).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_65_kyabasara_hc_iii_kangaroo_care_chair.jpg`

## P66 — Power house at Kyabasara HC III, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/power house.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kagadi / Kyabasara-HC-III; original filename: power house.jpg.'}
- Field point: Power house. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: utilities; crop fractions: (0.05, 0.1, 0.95, 0.76); rotation: 0°; output: (730, 713).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_66_kyabasara_hc_iii_power_house.jpg`

## P67 — Laboratory benches and sinks at Bweema Seed Secondary School, Buvuma District (Buganda).
- Source: `raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Image 2026-09-12 at 13.47.22 (2).jpeg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.22 (2).jpeg.'}
- Field point: Laboratory benches and sinks. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: laboratory; crop fractions: (0, 0.04, 1, 0.68); rotation: 0°; output: (1280, 615).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_67_bweema_seed_secondary_school_laboratory_benches_and_sinks.jpg`

## P68 — Classroom desks at Bweema Seed Secondary School, Buvuma District (Buganda).
- Source: `raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Unknown 2026-09-12 at 13.58.16/WhatsApp Image 2026-09-12 at 13.47.17 (2).jpeg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.17 (2).jpeg.'}
- Field point: Classroom desks. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: school furniture; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1280, 960).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_68_bweema_seed_secondary_school_classroom_desks.jpg`

## P69 — Sanitation block at Bweema Seed Secondary School, Buvuma District (Buganda).
- Source: `raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Unknown 2026-09-12 at 13.58.16/WhatsApp Image 2026-09-12 at 13.47.20 (1).jpeg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Buvuma / Bweema-Seed-Secondary-School; original filename: WhatsApp Image 2026-09-12 at 13.47.20 (1).jpeg.'}
- Field point: Sanitation block. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: sanitation; crop fractions: (0.06, 0.18, 1, 0.78); rotation: 0°; output: (1203, 576).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_69_bweema_seed_secondary_school_sanitation_block.jpg`

## P70 — Oxygen cylinders at Kibiri HC III, Makindye-Ssabagabo Municipality (Buganda).
- Source: `raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`
- Locator: {'embedded_image': 'word/media/image27.jpeg', 'body_block': 77, 'table': None, 'adjacent_text': 'Kibiri HC III report: oxygen-cylinder photograph word/media/image27.jpeg in body block 77, within the facility pictorial record.'}
- Field point: Oxygen cylinders. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: clinical equipment; crop fractions: (0.02, 0.08, 0.85, 0.58); rotation: 0°; output: (800, 640).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_70_kibiri_hc_iii_oxygen_cylinders.jpg`

## P71 — Programme and school engraving on a chair at Budde Seed Secondary School, Butambala District (Buganda).
- Source: `raw-data-grouped/team-32/Butambala/Budde-Seed-Secondary-School/BUDDE SEED SCHOOL (BUTAMABALA DISTRICT-BUDDE SEED).docx`
- Locator: {'embedded_image': 'word/media/image43.png', 'body_block': 102, 'table': 8, 'adjacent_text': 'Budde Seed Secondary School return: PICTORIAL EVIDENCE, body block 102, table 8, word/media/image43.png. The visible mark identifies UGIFT and the school.'}
- Field point: Programme and school engraving on a chair. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: engraving; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (408, 306).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_71_budde_seed_secondary_school_programme_and_school_engraving_on_a_chair.jpg`

## P72 — Infant weighing scale at Buwembe HC III, Busia District (Bukedi).
- Source: `raw-data-grouped/team-13/Busia/Buwembe-HC-III/127_baby-weighing-scale-yrbb-20_ref20260828-0082.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Busia / Buwembe-HC-III; original filename: 127_baby-weighing-scale-yrbb-20_ref20260828-0082.jpg.'}
- Field point: Infant weighing scale. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: clinical equipment; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1080, 1080).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_72_buwembe_hc_iii_infant_weighing_scale.jpg`

## P73 — Autoclave above a gas cylinder at Buwembe HC III, Busia District (Bukedi).
- Source: `raw-data-grouped/team-13/Busia/Buwembe-HC-III/136_autoclave-on-a-gas-cylinder_ref20260828-0091.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Busia / Buwembe-HC-III; original filename: 136_autoclave-on-a-gas-cylinder_ref20260828-0091.jpg.'}
- Field point: Autoclave above a gas cylinder. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: clinical equipment; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1080, 1080).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_73_buwembe_hc_iii_autoclave_above_a_gas_cylinder.jpg`

## P74 — Examination lamp in protective wrapping at Buwumba HC III, Busia District (Bukedi).
- Source: `raw-data-grouped/team-13/Busia/Buwumba-HC-III/006_examination-lamp-still-wrapped_ref20260828-0285.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Busia / Buwumba-HC-III; original filename: 006_examination-lamp-still-wrapped_ref20260828-0285.jpg.'}
- Field point: Examination lamp in protective wrapping. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: storage; crop fractions: [0.08, 0, 1, 1]; rotation: 0°; output: (994, 1080).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_74_buwumba_hc_iii_examination_lamp_in_protective_wrapping.jpg`

## P75 — Pedal suction unit in packaging at Majanji HC III, Busia District (Bukedi).
- Source: `raw-data-grouped/team-13/Busia/Majanji-HC-III/042_pedal-suction-unit-in-its-packing_ref20260827-0637.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Busia / Majanji-HC-III; original filename: 042_pedal-suction-unit-in-its-packing_ref20260827-0637.jpg.'}
- Field point: Pedal suction unit in packaging. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: storage; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (960, 1280).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_75_majanji_hc_iii_pedal_suction_unit_in_packaging.jpg`

## P76 — Computer sets stacked in a store at Bumufuni Seed Secondary School, Bulambuli District (Bugisu).
- Source: `raw-data-grouped/team-14/Bulambuli/Bumufuni-Seed-Secondary-School/07_computer-sets-stacked-in-store_ref20260911-0011.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Bulambuli / Bumufuni-Seed-Secondary-School; original filename: 07_computer-sets-stacked-in-store_ref20260911-0011.jpg.'}
- Field point: Computer sets stacked in a store. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: storage; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1280, 576).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_76_bumufuni_seed_secondary_school_computer_sets_stacked_in_a_store.jpg`

## P77 — Engraving on a wheelchair armrest at Bumugibole HC III, Bulambuli District (Bugisu).
- Source: `raw-data-grouped/team-14/Bulambuli/Bumugibole-HC-III/05_wheelchair-armrest-engraving_ref20260831-0202.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Bulambuli / Bumugibole-HC-III; original filename: 05_wheelchair-armrest-engraving_ref20260831-0202.jpg.'}
- Field point: Engraving on a wheelchair armrest. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: engraving; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1280, 960).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_77_bumugibole_hc_iii_engraving_on_a_wheelchair_armrest.jpg`

## P78 — Solar batteries at Bunangaka HC III, Bulambuli District (Bugisu).
- Source: `raw-data-grouped/team-14/Bulambuli/Bunangaka-HC-III/01_solar-batteries_ref20260830-0421.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Bulambuli / Bunangaka-HC-III; original filename: 01_solar-batteries_ref20260830-0421.jpg.'}
- Field point: Solar batteries. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: utilities; crop fractions: [0.13, 0.3, 0.81, 0.88]; rotation: 0°; output: (735, 470).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_78_bunangaka_hc_iii_solar_batteries.jpg`

## P79 — Computer equipment in the school ICT room at Kabeywa Seed Secondary School, Kapchorwa District (Sebei).
- Source: `raw-data-grouped/team-15/Kapchorwa/Kabeywa-Seed-Secondary-School/07_28computers_ref20260830-0271.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kapchorwa / Kabeywa-Seed-Secondary-School; original filename: 07_28computers_ref20260830-0271.jpg.'}
- Field point: Computer equipment in the school ICT room. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: ICT; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1280, 960).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_79_kabeywa_seed_secondary_school_computer_equipment_in_the_school_ict_room.jpg`

## P80 — Library shelving and tables at Kabeywa Seed Secondary School, Kapchorwa District (Sebei).
- Source: `raw-data-grouped/team-15/Kapchorwa/Kabeywa-Seed-Secondary-School/24_library_ref20260830-0842.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kapchorwa / Kabeywa-Seed-Secondary-School; original filename: 24_library_ref20260830-0842.jpg.'}
- Field point: Library shelving and tables. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: school furniture; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1080, 810).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_80_kabeywa_seed_secondary_school_library_shelving_and_tables.jpg`

## P81 — Autoclave at Atar HC III, Kween District (Sebei).
- Source: `raw-data-grouped/team-15/Kween/Atar-HC-III/07_autoclave-01_ref0458.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kween / Atar-HC-III; original filename: 07_autoclave-01_ref0458.jpg.'}
- Field point: Autoclave. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: clinical equipment; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (960, 1280).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_81_atar_hc_iii_autoclave.jpg`

## P82 — Solar batteries and control equipment at Atar HC III, Kween District (Sebei).
- Source: `raw-data-grouped/team-15/Kween/Atar-HC-III/21_solar-batteries_ref0444.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kween / Atar-HC-III; original filename: 21_solar-batteries_ref0444.jpg.'}
- Field point: Solar batteries and control equipment. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: utilities; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1280, 720).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_82_atar_hc_iii_solar_batteries_and_control_equipment.jpg`

## P83 — Kangaroo care chair at Atar HC III, Kween District (Sebei).
- Source: `raw-data-grouped/team-15/Kween/Atar-HC-III/36_kangaroo-mother-care-chair-1-not-engraved_ref20260830-0604.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kween / Atar-HC-III; original filename: 36_kangaroo-mother-care-chair-1-not-engraved_ref20260830-0604.jpg.'}
- Field point: Kangaroo care chair. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: clinical equipment; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1280, 720).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_83_atar_hc_iii_kangaroo_care_chair.jpg`

## P84 — ICT laboratory interior under construction at Kitawoi Seed Secondary School, Kween District (Sebei).
- Source: `raw-data-grouped/team-15/Kween/Kitawoi-Seed-Secondary-School/09_ict-lab-under-construction_ref1386.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kween / Kitawoi-Seed-Secondary-School; original filename: 09_ict-lab-under-construction_ref1386.jpg.'}
- Field point: ICT laboratory interior under construction. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: construction; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1280, 720).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_84_kitawoi_seed_secondary_school_ict_laboratory_interior_under_construction.jpg`

## P85 — Institutional engraving on equipment at Moyok HC III, Kween District (Sebei).
- Source: `raw-data-grouped/team-15/Kween/Moyok-HC-III/14_engraving-kwn-med-eq-moyok-hciii_ref0038.jpg`
- Locator: {'embedded_image': None, 'body_block': None, 'table': None, 'adjacent_text': 'Loose field photograph filed under Kween / Moyok-HC-III; original filename: 14_engraving-kwn-med-eq-moyok-hciii_ref0038.jpg.'}
- Field point: Institutional engraving on equipment. The image illustrates the asset or visible condition; operational status and causes require separate field evidence.
- Theme: engraving; crop fractions: (0, 0, 1, 1); rotation: 0°; output: (1280, 720).
- Privacy: Full original inspected individually; selected crop excludes identifiable faces, personal names, signatures, name badges, personal documents, telephone numbers and email addresses. Northern and Eastern originals received independent review.
- Output: `outputs/narrative-report/figures/photo_85_moyok_hc_iii_institutional_engraving_on_equipment.jpg`


# Additional field photographs P86 to P122

37 originals individually inspected. Source files are unchanged. Only lossless orientation changes, rectangular composition/privacy crops and JPEG output preparation were used. Karenga is excluded. Captions identify the visible item and facility; they make no functionality claim. This private index is not report content.

## P86 Water tank beside school buildings at Budde Seed Secondary School, Butambala District (Buganda).
- Source: `raw-data-grouped/team-32/Butambala/Budde-Seed-Secondary-School/BUDDE SEED SCHOOL (BUTAMABALA DISTRICT-BUDDE SEED).docx`
- Locator: {"embedded_image": "word/media/image16.png", "body_block": 102, "table": 8}
- Candidate: E79
- Crop: None; rotation: 0 degrees.
- Original SHA256: 5a506e1069f91b95bcfee8267d4f3e87fa8a58f870614a14d0ae2ab9490f4792

## P87 Desks and chairs bearing asset identification at Budde Seed Secondary School, Butambala District (Buganda).
- Source: `raw-data-grouped/team-32/Butambala/Budde-Seed-Secondary-School/BUDDE SEED SCHOOL (BUTAMABALA DISTRICT-BUDDE SEED).docx`
- Locator: {"embedded_image": "word/media/image42.png", "body_block": 102, "table": 8}
- Candidate: E105
- Crop: None; rotation: 0 degrees.
- Original SHA256: 4da210aa8f52e1fd3b5501b88734724369044925799abfb413e8472e41f7902a

## P88 Wooden waiting bench at Kibiri HC III, Makindye-Ssabagabo Municipal Council (Buganda).
- Source: `raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`
- Locator: {"embedded_image": "word/media/image1.jpeg", "body_block": 77, "table": null}
- Candidate: E108
- Crop: (0, 0.15, 0.83, 0.92); rotation: 0 degrees.
- Original SHA256: ae7233647e0135b61620b4d77d629207b5ab7f80a0f4da889b1dce3d933136de

## P89 Patient trolley beside stacked furniture at Kibiri HC III, Makindye-Ssabagabo Municipal Council (Buganda).
- Source: `raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`
- Locator: {"embedded_image": "word/media/image2.jpeg", "body_block": 77, "table": null}
- Candidate: E109
- Crop: (0, 0.09, 0.96, 0.9); rotation: 0 degrees.
- Original SHA256: d4b9b37e576b2ea37d460c033441122cb131530fe174c74daec212ff6b326682

## P90 Sanitation block with external handwashing basins at Kibiri HC III, Makindye-Ssabagabo Municipal Council (Buganda).
- Source: `raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`
- Locator: {"embedded_image": "word/media/image10.jpeg", "body_block": 77, "table": null}
- Candidate: E117
- Crop: (0, 0.15, 1, 1); rotation: 0 degrees.
- Original SHA256: baf0b79b7bd109508bc1418a0717926ff84fb491d9022e6cc71fb7f2cd99446a

## P91 Waste disposal structure at Kibiri HC III, Makindye-Ssabagabo Municipal Council (Buganda).
- Source: `raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`
- Locator: {"embedded_image": "word/media/image12.jpeg", "body_block": 77, "table": null}
- Candidate: E119
- Crop: None; rotation: 0 degrees.
- Original SHA256: 738069118886c0f6cf686feb51314ff1606b720fb22a4c0c6d98addc4894a21a

## P92 Office desk and other furniture at Lwamata Town Council Seed Secondary School, Kiboga District (Buganda).
- Source: `raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx`
- Locator: {"embedded_image": "word/media/image2.jpeg", "body_block": 78, "table": null}
- Candidate: E162
- Crop: None; rotation: -90 degrees.
- Original SHA256: 68cd4283c7cc8cbd0a328b42153c76551743b42ecd0dd391941f75f199fba99a

## P93 Laboratory tables at Lwamata Town Council Seed Secondary School, Kiboga District (Buganda).
- Source: `raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx`
- Locator: {"embedded_image": "word/media/image4.jpeg", "body_block": 78, "table": null}
- Candidate: E164
- Crop: None; rotation: -90 degrees.
- Original SHA256: 644a50085f1fceb2bf0e91acb038e1075fb11eba1bfbc1a9ac5d544aa0797194

## P94 Library shelving at Lwamata Town Council Seed Secondary School, Kiboga District (Buganda).
- Source: `raw-data-grouped/team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH.docx`
- Locator: {"embedded_image": "word/media/image5.jpeg", "body_block": 78, "table": null}
- Candidate: E165
- Crop: None; rotation: -90 degrees.
- Original SHA256: f9ff1409ff7c9e1aee20211026f17e2ea6afc3f35768216142900a7924e0b9e9

## P95 Office tables and chair at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda).
- Source: `raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`
- Locator: {"embedded_image": "word/media/image1.jpeg", "body_block": 1, "table": null}
- Candidate: E189
- Crop: (0, 0.29, 1, 1); rotation: 0 degrees.
- Original SHA256: 3a9ef20a336cf918136718a54c15cc374bbf0aa31aa549256858c0ecbd130c26

## P96 Library shelves and reading tables at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda).
- Source: `raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`
- Locator: {"embedded_image": "word/media/image15.jpeg", "body_block": 63, "table": null}
- Candidate: E196
- Crop: None; rotation: 0 degrees.
- Original SHA256: 9c619fc9323ce6ee79a6f3dd451a4c68d9e9f5c014abf6a60640ee1b9e957ac5

## P97 Anatomical teaching model at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda).
- Source: `raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`
- Locator: {"embedded_image": "word/media/image17.jpeg", "body_block": 71, "table": null}
- Candidate: E197
- Crop: None; rotation: 0 degrees.
- Original SHA256: 8996679554147d418dd4142523164a04a03ffc58ee1e404e8bcf8791393c1a02

## P98 Laboratory glassware and equipment at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda).
- Source: `raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`
- Locator: {"embedded_image": "word/media/image18.jpeg", "body_block": 71, "table": null}
- Candidate: E198
- Crop: None; rotation: 0 degrees.
- Original SHA256: fd9197620925d20b1c108084bd19574295cef1c976bba8a7b2a86ad39ab39421

## P99 Water tank and enclosed service structures at Bweema Seed Secondary School, Buvuma District (Buganda).
- Source: `raw-data-grouped/team-31/Buvuma/Bweema-Seed-Secondary-School/WhatsApp Unknown 2026-09-12 at 13.58.16/WhatsApp Image 2026-09-12 at 13.47.13 (1).jpeg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: B19
- Crop: None; rotation: 0 degrees.
- Original SHA256: 25f3d5285d8fbd5f5c500f2025b10d47a22cd714fa2cac48fd3e634470789793

## P100 Blood pressure apparatus on a mobile stand at Butiaba HC III, Buliisa District (Bunyoro).
- Source: `raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/IMG-20260907-WA0094.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: W6
- Crop: None; rotation: 0 degrees.
- Original SHA256: 1c5aac50d346c6dc6a8fbe55cae736b0cf3786e8b85690d828947393cf09b5ba

## P101 Office chairs at Butiaba HC III, Buliisa District (Bunyoro).
- Source: `raw-data-grouped/team-25/Buliisa/Butiaba-HC-III/office chairs.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: W11
- Crop: None; rotation: 0 degrees.
- Original SHA256: 5612561c6f12561ee5ca8ef36349ecf46b36febd245354d7bd13494ff1e97e74

## P102 Classroom block with earthworks in the foreground at Kihungya Seed Secondary School, Buliisa District (Bunyoro).
- Source: `raw-data-grouped/team-25/Buliisa/Kihungya-Seed-Secondary-School/classroom block.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: W18
- Crop: (0, 0.2, 1, 0.96); rotation: 0 degrees.
- Original SHA256: f345cb2f20d357ab9e6f1efaf6a92a5df97b3305d9ff598273495116d6436595

## P103 Health centre buildings and covered walkway at Kihuukya HC III, Hoima City (Bunyoro).
- Source: `raw-data-grouped/team-25/Hoima City/Kihuukya-HC-III/IMG-20260908-WA0045.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: W30
- Crop: (0, 0.16, 0.83, 0.95); rotation: 0 degrees.
- Original SHA256: 7c6da328ef81f64ed1955b3c6fb984f0837ee24e45e6b668dbb77854f9b5b9ba

## P104 Binocular microscope at Kihuukya HC III, Hoima City (Bunyoro).
- Source: `raw-data-grouped/team-25/Hoima City/Kihuukya-HC-III/microscope.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: W34
- Crop: (0, 0.08, 1, 0.89); rotation: 0 degrees.
- Original SHA256: 9f2ca2d2d19e5d373e5efaa020f62bc3c519fe78a73f557ba7b6797b0b08803d

## P105 Water tank on a masonry support at King Solomon Seed Secondary School, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_115648_996.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: W41
- Crop: None; rotation: 0 degrees.
- Original SHA256: a82561ff7fe06e6dc6a3bb01a088fe245d4061a83afd546f3e8cf1a9449ee462

## P106 Laboratory benches with cupboard doors detached at King Solomon Seed Secondary School, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_120333_732.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: W45
- Crop: (0, 0.1, 1, 0.91); rotation: 0 degrees.
- Original SHA256: 7b13f46e671fc2e86dca146a90cb4d1861f45b5772f9ae20e130d823ced774c8

## P107 Elevated water tank on a steel tower at King Solomon Seed Secondary School, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/King-Solomon-Seed-Secondary-School/IMG_20260901_121530_409.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: W55
- Crop: None; rotation: 0 degrees.
- Original SHA256: 69a82c7ad52795ef1f38dfbbce763c4b6502d72bc60cfe6544f67a177fff5531

## P108 Ceiling surface and finish at Kyabasara HC III, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/cracked ceiling due to shoddy work.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: W56
- Crop: (0, 0.32, 1, 0.81); rotation: 0 degrees.
- Original SHA256: e9bde83abc229258c1e0916c9f3103d3012b50a7431bba0d8f47bdf2732504d3

## P109 Latrine block and paved access at Kyabasara HC III, Kagadi District (Bunyoro).
- Source: `raw-data-grouped/team-25/Kagadi/Kyabasara-HC-III/latrines.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: W63
- Crop: (0, 0.22, 1, 0.94); rotation: 0 degrees.
- Original SHA256: 184bc82550c01a0b1510af3a6c46969dfb0f6b083f466709b72afcbd16a46fae

## P110 Refrigerator bearing programme identification at Kalemungole HC III, Moroto District (Karamoja).
- Source: `raw-data-grouped/team-10/Moroto/Kalemungole-HC-III/114_refrigerator-engraved-gou-moh-ugift-project_ref20260827-0359.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G15
- Crop: (0.12, 0.08, 0.71, 0.96); rotation: 0 degrees.
- Original SHA256: 506dfd7b81bfcf447867338d4217f43c6d12cbd5b87382f1c58da61cc624a726

## P111 Rainwater tank beside a staff house at Rupa Seed School, Moroto District (Karamoja).
- Source: `raw-data-grouped/team-10/Moroto/Rupa-Seed-School/17_water-tank-beside-a-staff-house_ref20260909-photo-p07.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G24
- Crop: (0, 0.13, 1, 0.84); rotation: 0 degrees.
- Original SHA256: ee077a2a95f1fa1414d374916f3b7344f7a4ffc9859ffa17a7094f1527e3af51

## P112 Computer and library block interior with furniture and stored items at Iriiri Seed Secondary School, Napak District (Karamoja).
- Source: `raw-data-grouped/team-10/Napak/Iriiri-Seed-Secondary-School/30_ict-and-library-block_ref20260827-0466.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G38
- Crop: None; rotation: 0 degrees.
- Original SHA256: ccd6a7f9039e47a0bed7229ac9642dbb0a778479ce4e402f48d06416250560d9

## P113 Computer and library block at Lopei Seed Secondary School, Napak District (Karamoja).
- Source: `raw-data-grouped/team-10/Napak/Lopei-Seed-Secondary-School/08_ict-and-library-block_ref20260828-0570.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G43
- Crop: (0, 0.2, 1, 0.95); rotation: 0 degrees.
- Original SHA256: eeff6c1f12e85e10757a28396a305d3be3a7b0085e7bb68cc28c1907f0f26eb8

## P114 Instrument trolley with delivery instruments at Kamoru HC III, Kotido District (Karamoja).
- Source: `raw-data-grouped/team-11/Kotido/Kamoru-HC-III/07_instrument-trolley-with-a-delivery-set_ref1176.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G62
- Crop: (0, 0, 1, 0.94); rotation: 0 degrees.
- Original SHA256: 082129d3cca416c7da80cb026876339b4dbd476c83d72c22be7abb0488dc96d4

## P115 Microscope bearing local facility identification at Kamoru HC III, Kotido District (Karamoja).
- Source: `raw-data-grouped/team-11/Kotido/Kamoru-HC-III/28_microscope-marked-kamoru-hc-iii_ref1144.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G68
- Crop: None; rotation: 0 degrees.
- Original SHA256: 355b7178b3d75b271abef3dbb22798939f780cfa6d2088a0a2107ce5672d9617

## P116 Anatomical skeleton teaching model at Kamonkoli Seed Secondary School, Budaka District (Bukedi).
- Source: `raw-data-grouped/team-12/Budaka/Kamonkoli-Seed-Secondary-School/50_anatomical-skeleton-on-laboratory-wall_ref0755.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G85
- Crop: None; rotation: 0 degrees.
- Original SHA256: 4224027d60b49aa7ec575b13524f54beca5f77688b6a5109a2d711095015e66a

## P117 Binocular microscope on a trolley at Namusita HC III, Budaka District (Bukedi).
- Source: `raw-data-grouped/team-12/Budaka/Namusita-HC-III/024_microscope-binocular_ref0908.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G92
- Crop: (0, 0.17, 0.9, 0.88); rotation: 0 degrees.
- Original SHA256: 687384ed8cd04872619d8361266c2c3cedf81f2b21a98e91a0444765ca824e70

## P118 Infant weighing scales at Namusita HC III, Budaka District (Bukedi).
- Source: `raw-data-grouped/team-12/Budaka/Namusita-HC-III/039_infant-weighing-scales-x2_ref0887.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G95
- Crop: None; rotation: 0 degrees.
- Original SHA256: 829f58d356e6d5a0737902f39658b2efa5f2c493673c7452b52d14f787ff9124

## P119 Laboratory benches, stools and sinks at Nansanga Seed Secondary School, Budaka District (Bukedi).
- Source: `raw-data-grouped/team-12/Budaka/Nansanga-Seed-Secondary-School/035_laboratory-benches-stools-and-sink-run_ref0683.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G103
- Crop: (0.22, 0, 1, 1); rotation: 0 degrees.
- Original SHA256: 1e3e6541cd719a9701846767ec5b1d9e7b55328bf79b4bfcfca2c06d1497c69b

## P120 Library shelving with books at Nansanga Seed Secondary School, Budaka District (Bukedi).
- Source: `raw-data-grouped/team-12/Budaka/Nansanga-Seed-Secondary-School/072_library-shelving-with-books_ref0729.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G104
- Crop: None; rotation: 0 degrees.
- Original SHA256: 2c3346f187396b1476ce48ae4d6e9685e7147ebc21a54c15d6b90a251392e5eb

## P121 Water tanks on a steel tower at Kabweri HC III, Kibuku District (Bukedi).
- Source: `raw-data-grouped/team-12/Kibuku/Kabweri-HC-III/05_water-tank-on-steel-tower_ref1262.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G110
- Crop: (0.2, 0, 1, 0.77); rotation: 0 degrees.
- Original SHA256: 49ff9d0ff0b89e4d3b86fc17b0bcdf3495bdc5a5282c81042d00fa82dc01ccd1

## P122 Delivery bed with side rails at Kabweri HC III, Kibuku District (Bukedi).
- Source: `raw-data-grouped/team-12/Kibuku/Kabweri-HC-III/28_delivery-bed-with-side-rails_ref1303.jpg`
- Locator: {"embedded_image": null, "body_block": null, "table": null}
- Candidate: G118
- Crop: None; rotation: 0 degrees.
- Original SHA256: 3dedd8efdd278ee212fed8f6af4f31601c3786d655f3359a2e53f1988f1912e8


# Positive programme benefit photo replacements

Nine photographs replaced weaker, repetitive or problem-focused selections. Final total remains 120. The eight gallery images are paired to practical-benefit field evidence; captions describe visible observations. Rupa is a school-supplied follow-up photograph, not a room independently entered by the team. Alerek tank functionality is not asserted.

Gallery: P28, P29, P74, P86, P89, P103, P104, P108

## P86
- Previous: Water tank beside school buildings at Budde Seed Secondary School, Butambala District (Buganda).
- New: Health centre building at Kibiri HC III, Makindye-Ssabagabo Municipal Council (Buganda).
- Image source: `raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`
- Image locator: {"embedded_image": "word/media/image16.jpeg", "body_block": 77, "table": null, "adjacent_text": ""}
- Benefit source: `raw-data-grouped/team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/KIBIRI HC III report.docx`; Paragraphs 11, 21 and 40 (1-based Document.paragraphs)
- Recorded evidence: The facility commenced formal operations on 31 August 2026. Paragraph 43 notes that some equipment was still being arranged as it transitioned into full operation.

## P89
- Previous: Patient trolley beside stacked furniture at Kibiri HC III, Makindye-Ssabagabo Municipal Council (Buganda).
- New: Classroom furnished with desks and a whiteboard at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda).
- Image source: `raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`
- Image locator: {"embedded_image": "word/media/image5.jpeg", "body_block": 19, "table": null, "adjacent_text": "3. Desks | 3. Desks"}
- Benefit source: `raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school.docx`; Paragraph 78 (1-based Document.paragraphs)
- Recorded evidence: This is the only secondary school available 35km from Kalangala town in Bujumba. This has improve availability of education to the area including for workers at the Oil palm factory.

## P95
- Previous: Office tables and chair at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda).
- New: School blocks at Gyagenda Memorial Seed Secondary School, Kalangala District (Buganda).
- Image source: `raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school pictures.docx`
- Image locator: {"embedded_image": "word/media/image27.jpeg", "body_block": 95, "table": null, "adjacent_text": "12. A | d | ministration block, staffrooms | , classrooms |  and multipurpose hall | 12. A | d | ministration block, staffrooms | , classrooms |  and multipurpose hall"}
- Benefit source: `raw-data-grouped/team-31/Kalangala/Gyagenda-Memorial-Seed-Secondary-School/Gyagenda memorial seed secondary school.docx`; Paragraphs 77â€“78 (1-based Document.paragraphs)
- Recorded evidence: The school is also sometimes used by the community for village political meetings about service delivery. It is the only secondary school available 35km from Kalangala town in Bujumba and has improved availability of education.

## P108
- Previous: Ceiling surface and finish at Kyabasara HC III, Kagadi District (Bunyoro).
- New: Adult weighing scale with a height meter and waiting benches at Iruhura HC III, Kabarole District (Tooro).
- Image source: `raw-data-grouped/team-26/Kabarole/Iruhura-HC-III/KABAROLE DISTRICT   IRUHURA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222 (1).docx`
- Image locator: {"embedded_image": "word/media/image13.jpeg", "body_block": 105, "table": null, "adjacent_text": "Weighing scale with heighmeter & desk |       | Tank |                                 |                                                 Residentials "}
- Benefit source: `raw-data-grouped/team-26/Kabarole/Iruhura-HC-III/KABAROLE DISTRICT   IRUHURA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222 (1).docx`; Table 6, row 75 (1-based tables/rows)
- Recorded evidence: Weighing Scale with Height Meter, Adult | Good condition | 2 are in use
- Benefit source: `raw-data-grouped/team-26/Kabarole/Iruhura-HC-III/KABAROLE DISTRICT   IRUHURA HC III ASSET VERIFICATION AND RECORDING TOOL KIT 222 (1).docx`; Table 6, row 152 (1-based tables/rows)
- Recorded evidence: Bench | Good condition | 4 in use

## P47
- Previous: Boxed desktop computers at Alerek Seed Secondary School, Abim District (Karamoja).
- New: Water tanks on a rendered plinth and steel tower at Alerek Seed Secondary School, Abim District (Karamoja).
- Image source: `raw-data-grouped/team-11/Abim/Alerek-Seed-Secondary-School/23_water-tank-on-a-plinth-and-elevated-tank_ref0870.jpg`
- Image locator: {"embedded_image": null, "body_block": null, "table": null}
- Benefit source: `D:\coding\ugift-data-analysis\raw-data-grouped\team-11\Abim\Alerek-Seed-Secondary-School\Abim-school-Alerek-Seed-Secondary-School.docx`; Table 2, row 4, column 2 (Usage / performance); 1-based document tables/rows/cells
- Recorded evidence: Settled in part. The head teacher answered that the support has brought education to Alerek, work for teachers and a market for the community's food. Against that the ICT is wholly unused: the school has no power, nothing has been connected and no technician has come.

## P49
- Previous: Boxed printer and equipment at Sidok Seed Secondary School, Kaabong District (Karamoja).
- New: Laboratory supplies and an anatomical teaching model at Rupa Seed School, Moroto District (Karamoja).
- Image source: `raw-data-grouped/team-10/Moroto/Rupa-Seed-School/33_laboratory-store-shelving-with-chemicals-and-a-skeleton_ref20260909-photo-p23.jpg`
- Image locator: {"embedded_image": null, "body_block": null, "table": null}
- Benefit source: `D:\coding\ugift-data-analysis\raw-data-grouped\team-10\Moroto\Rupa-Seed-School\Moroto-school-Rupa-Seed-School.docx`; Table 2, row 4, column 2 (Usage / performance); 1-based document tables/rows/cells
- Recorded evidence: Established on the same register and on the school's return to the ministry, which agree. The library and the computer laboratory block are both in use as dormitories; the three staff house blocks, their kitchens and their latrines have been redirected to hold all the staff at the school. The school opened with 500 students and reports that all 41 of its pioneer candidates scored first grade at the Uganda Certificate of Education in 2024.
- Benefit source: `D:\coding\ugift-data-analysis\raw-data-grouped\team-10\Moroto\Rupa-Seed-School\Moroto-school-Rupa-Seed-School.docx`; Paragraph 21 (1-based Document.paragraphs)
- Recorded evidence: The support has been of immense service, the school opening with 500 students.

## P28
- Previous: Cracked desk surface bearing a school marking, Tororo District (Bukedi).
- New: Books displayed on library shelves at Sibanga Seed School, Manafwa District (Bugisu).
- Image source: `raw-data-grouped/team-13/Manafwa/Sibanga-Seed-School/58_library-shelves-with-books_ref20260904-0059.jpg`
- Image locator: {"embedded_image": null, "body_block": null, "table": null}
- Benefit source: `D:\coding\ugift-data-analysis\raw-data-grouped\team-13\Manafwa\Sibanga-Seed-School\Manafwa-school-Sibanga-Seed-School.docx`; Table 2, row 4, column 2 (Usage / performance); 1-based document tables/rows/cells
- Recorded evidence: Partly established. The guide says the school shortened the distance learners used to walk, reduced teenage pregnancy and reduced dropout.

## P29
- Previous: Damaged chair back joint at a seed secondary school, Budaka District (Bukedi).
- New: Maternity block entrance and access ramp at Kamuli HC III, Tororo District (Bukedi).
- Image source: `raw-data-grouped/team-13/Tororo/Kamuli-HC-III/24_maternity-ward-building_ref20260831-0456.jpg`
- Image locator: {"embedded_image": null, "body_block": null, "table": null}
- Benefit source: `D:\coding\ugift-data-analysis\raw-data-grouped\team-13\Tororo\Kamuli-HC-III\Tororo-health-centre-Kamuli-HC-III.docx`; Table 2, row 4, column 2 (Usage / performance); 1-based document tables/rows/cells
- Recorded evidence: Partly established. Service delivery has improved and equipment quality is good, but staffing is low, the facility is not fenced and staff accommodation is short.

## P74
- Previous: Examination lamp in protective wrapping at Buwumba HC III, Busia District (Bukedi).
- New: ICT laboratory block and entrance ramp at Sisiyi Seed Secondary School, Bulambuli District (Bugisu).
- Image source: `raw-data-grouped/team-14/Bulambuli/Sisiyi-Seed-Secondary-School/15_ict-laboratory-block_ref20260828-0015.jpg`
- Image locator: {"embedded_image": null, "body_block": null, "table": null}
- Benefit source: `D:\coding\ugift-data-analysis\raw-data-grouped\team-14\Bulambuli\Sisiyi-Seed-Secondary-School\Bulambuli-school-Sisiyi-Seed-Secondary-School.docx`; Table 2, row 4, column 2 (Usage / performance); 1-based document tables/rows/cells
- Recorded evidence: Reported line by line on the hand-filled booklet, which records every furniture, ICT and buildings line as in use except the water tanks. The school also said its computers are too few for the number of learners it has.
- Benefit source: `D:\coding\ugift-data-analysis\raw-data-grouped\team-14\Bulambuli\Sisiyi-Seed-Secondary-School\Bulambuli-school-Sisiyi-Seed-Secondary-School.docx`; Paragraph 31 (1-based Document.paragraphs)
- Recorded evidence: The discussion guide on the hand-filled booklet adds that the school does hold a record of the assets provided under UgIFT, that the contractor's one-year guarantee covers any asset needing repair, and that the school records any breakdown. It names easy access to secondary education in Sisiyi and the neighbouring community, and jobs for thirty staff, as what the support has done.

Rupa P49 is retained in the regional selection but excluded from the benefit gallery: the team did not enter the photographed room.


# Private source audit: additional field cases

This note and the `source_index` in `additional_cases.json` are working provenance only. Neither filenames nor these source identifiers should appear in the report, its appendices or photograph captions.

The addition contains 11 local cases (three Central, four Eastern, two Northern and two Western) and seven national cases. All eleven local facility names were absent from the text extracted from the then-current 46-page report. National cases add specific observations beyond the existing Works and Transport vehicle-servicing example and damaged Prime Minister's Office laptops.

Every locator was resolved against its original document or worksheet. Word paragraph, table and row numbers are one-based and include empty paragraphs/rows. The JSON retains excerpts from the resolved locations. Expected outcomes and actions are editorial recommendations; they are not assertions of a separately checked contract or completed follow-up.

Material source distinctions preserved:

- AD01–AD03: Local-government identity is confirmed by table 1 row 5. The three facilities are in Kassanda; sources spell the name Kasanda. Buseregenyu was excluded because its identity table says Mityana while its later prose says Kasanda.
- AD04: The combined Atyak/Alwi document contains two facilities. Only the Alwi interview and school equipment tables support the case. The server power-backup row has conflicting status and remark fields; the explicit “Not working” remark is used. Camera failure is stated as only one of thirteen functioning, avoiding unnecessary derived totals. The case reports the power-surge problem without asserting an independently established cause of every failed item.
- AD05: The combined Amwonyo/Wadelai document also covers two facilities. Only the school interview and school tables are used. The twenty desktops being marked in use does not imply uninterrupted availability; the interview separately identifies a solar fault.
- AD06: The power and packed-desktop statement is explicit in the district report, paragraph 55. No unboxing or independent performance test is claimed.
- AD07: Muhula was not handed over and the school was described as not operating. A printer and projector were separately marked in use, so the case does not say that every item was unused. The Kachonga/Muhula beneficiary-name question is left to reconciliation.
- AD08–AD09: Staff training, missing operating accessories, consumables and connection problems are explicit field findings. Actions do not imply that every stored item is damaged. The unexplained abbreviation ESR is avoided by using “laboratory stand.”
- AD10: Kihungya's administration block was in use while its laboratories and staff quarters remained unfinished. The case does not describe the whole school as unopened.
- AD11: Kihungya Health Centre's service benefits are attributed to staff. “At the subcounty” establishes a location, not theft, diversion or permanent loss. The recommendation asks managers to confirm custody and appropriate deployment.
- AD12–AD13: The MoWT worksheet contains a copied MoFPED section beginning at row 59. The dedicated MoFPED worksheet and institution fields establish the correct institution. Shared narrative remarks concern several items, so no total number of losses, failed accessories or stored furniture is asserted. Police letters support reported laptop losses; refusal or difficulty obtaining engraving is not elevated into a finding of theft or intentional misconduct.
- AD14: OPM's concern is the user's assessment that laptop capacity is below workload. It is distinct from a hardware-failure assessment or a performance benchmark.
- AD15: Works and Transport's equipment was described directly as delivered, installed and functioning. Its photocopier row has an apparently future service date, which is omitted. The case does not reuse the later MoFPED material as a Works finding.
- AD16–AD17: Direct inspection entries support the condition and engraving findings. The findings apply to the specified items, not to all ministry or authority holdings.
- AD18: Ten one-unit Apple tablet rows explicitly say “Not Engraved.” Blank functionality cells do not support an assertion about use or performance, and none is made.

No monetary figures, source filenames or personal names are included in publishable case prose. The cases do not treat procurement warranties as present maintenance arrangements, or the reconciled master register's default classifications as physical tests.
