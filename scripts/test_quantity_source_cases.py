"""Source-proven quantity regressions: specifications describe assets, not counts."""

import unittest

from merge_shared_asset_registers import Asset, decide_groups, explode, mark_unit_records


class SourceQuantityTests(unittest.TestCase):
    def count(self, expected, **values):
        asset = Asset(**values)
        result = decide_groups(asset, True)
        self.assertEqual(sum(count for count, _ in result[1]), expected, (values, asset.extras))

    def test_serial_model_and_date_descriptions(self):
        for description in (
            "TRANSTEK SN: 2003374231006234", "S/N 110166495026", "S.N 02350005212",
            "Digital display rechargeable battery YK-820MiniA 250104080402049",
            "MD25031 30440078", "Plusmed Lot: 24083332", "CAT No.1103",
            "2 door, CHiQ brand Type: CTM150DSK3 NUMBER: 25W 1360151",
            "MZJ1OD 144789 Lot No: 23L 1498", "HP Office Jet Pro 8745",
            "Catalyst 2960", "Dell Remaining monitors after theft dec 2023",
            "LW UPS 850", "Serial number 1146352501240400", "Acquired June 2018",
        ):
            with self.subTest(description=description):
                self.count(3, item="BP machine (03)", description=description)
        self.count(1, item="DVR TURBO HD 7200", tag="SSUGU SEED/DVR/01")
        self.count(1, item="Air conditioner", description="0000624", tag="BDSS/ar/SS/001")

    def test_asset_number_only_fallback(self):
        self.count(1, item="Oxygen Concentrator", asset_number="20210722263",
                   description="1 white electronic machine that takes in normal room air and delivers pure oxygen. AB055")
        self.count(3, item="Haemoglobin Meter, Digital 3", asset_number="310030", description="white")
        self.count(1, item="1 Server processor", asset_number="6639010420")
        self.count(20, item="UPS", asset_number="2107 AB0745", remarks="20 not functional")
        self.count(1, item="Refrigerator, Basic (1)", asset_number="2031 NX10K650")
        self.count(28, item="UPS 28 pcs", asset_number="850 VA")
        self.count(1, item="Motorcycle", asset_number="125 cc")
        self.count(286, item="Chair", asset_number="286")
        self.count(3, item="Stove, Gas (1 green; 2 maroon; margin: one gas not found)",
                   description="78 green okibya; 79 maroon okibya/andalon", remarks="All three are functional in labour ward.",
                   source_file="team-13/Busia/Sikuda-HC-III/Asset-Verification-Toolkit.docx", source_location="Table 6 row 73")

    def test_component_counts_do_not_override_assets(self):
        self.count(1, item="Suction apparatus", description="Machine has 2 jars, suction tubing, foot pedal")
        self.count(2, item="Suction apparatus", description="Machine has 2 jars, suction tubing, foot pedal",
                   status="1 in use", remarks="1 in store")
        self.count(2, item="Patient Trolley", explicit_qty=2, description="4 wheels with a black sponge and 2 handles")
        self.count(2, item="Patient Trolley", description="4 white wheels with a black soft sponge mattress, 2 handles and 2 rails", remarks="2 verified and functioning")
        self.count(1, item="Laboratory stool", description="it has 5 wheels and can rotate", remarks="Only 1 verified")
        self.count(1, item="Instrument cupboard", description="White in color with 3 shelves")
        self.count(1, item="Suction apparatus", description="electric suction apparatus with 2 pcs spare bottles, 2 pcs PVC tubing")
        self.count(1, item="Residential building", description="block with 2 bed rooms.units.", remarks="1 received")
        self.count(2, item="Cupboard", description="2 Pieces Received. Steel, two-door, lockable")
        self.count(3, item="Shelves", description="3 shelves")
        for code in ("CE0197", "CE 0197", "CE0123"):
            self.count(2, item="BP machine", description=f"White in color {code}", remarks="2 were supplied")
        self.count(1, item="Sports field", description="Sports Field-provisional sum Ushs 50,000,000")
        self.count(1, item="Air conditioner", description="24,000 BTU Unit")
        for item, description, expected in (
            ("Examination couch", "4 silver stands with a black mattress", 2),
            ("Examination couch", "5 stainless steel legs with a mattress", 3),
            ("Filing Cabinet (2 pcs)", "four lock metallic equipment", 2),
            ("Stretcher", "Four wheeler equipment", 1),
            ("Patient Screen", "4 fold metallic equipment", 3),
            ("Bowl Stand", "Three silver leg stand", 2),
            ("Printer", "2 sided printer", 1),
            ("Gas stove (1)", "2 Burner gas stove", 1),
            ("Hall", "2 big rooms", 1),
            ("Science laboratory", "A two roomed block", 1),
        ):
            self.count(expected, item=item, description=description, remarks=f"{expected} supplied")

    def test_date_column_retains_its_context(self):
        for count in (1, 2, 4, 5):
            self.count(count, item="BP machine", asset_number=f"0{count}", service="2021 In use",
                       status="Functional", extras={"source_cells": ["2021 In use", "Functional"]})
        self.count(2021, item="BP machine", service="2021 units", extras={"source_cells": ["2021 units"]})

    def test_building_properties_and_explicit_units(self):
        self.count(1, item="Computer and library", asset_number="1", description="2 sections 1 computer lab 1 library")
        self.count(1, item="Science block", asset_number="1", description="2 sections of lab chemistry and Biology lab")
        self.count(1, item="2 Sitting rooms 4 Bedrooms (2 staff)", description="4 Bedrooms")
        self.count(6, item="Staff quarters", description="3 blocks 6 units")
        source = "_multi-team/busoga-and-part-of-central/Health Center Updated Asset Register  222.xlsx"
        rows = [Asset(item="Residential Buildings", department="1 Block; 2 Units.", description="2 Sitting rooms", source_file=source, source_location="Health Center row 4550")]
        for number, description in enumerate(("4 Bedrooms", "2 Dining rooms", "2 Kitchens", "2 Toilets + Bathroom", "2 Pit latrines", "1 Outside bathroom"), 4551):
            rows.append(Asset(item=description, description=description, source_file=source, source_location=f"Health Center row {number}"))
        mark_unit_records(rows)
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(rows[0].extras["source_group_locations"]), 7)
        self.assertEqual(len(explode(rows)), 2)

    def test_large_and_duplicate_legitimate_quantities(self):
        self.count(745, item="Bags and Covers", explicit_qty=745)
        self.count(900, item="Textbooks", remarks="Received 900 textbooks")
        self.count(120, item="BP machine", description="Serial: 9999999; quantity: 120")
        self.assertEqual(len(explode([Asset(item="BP machine (120)"), Asset(item="BP machine (120)")])), 240)

    def test_wrapped_group_totals_and_real_blank_tag_units(self):
        conflict = Asset(item="Office Chair", description="4 Black Office Chairs", remarks="6 still usable and one is broken need replacement")
        self.assertEqual(sum(count for count, _ in decide_groups(conflict, True)[1]), 7)
        self.assertTrue(any(label.startswith("source count conflict:") for _, label in conflict.extras["quantity_evidence"]))
        self.count(10, item="Adult patient bed", explicit_qty=10,
                   remarks="7 out of 10 are in use in staff homes due to space constraints Not in use (03)")
        for item, total, parts in (("Bed", 10, 2), ("Bed", 20, 2), ("MVA Kit", 4, 2),
                                   ("Disinfection Buckets", 6, 2), ("Tanks", 8, 5)):
            rows = [Asset(item=item, explicit_qty=total if index == 0 else None,
                          department="maternity" if index == 0 else "store", description="white",
                          source_location=f"Sheet1 row {index + 2}",
                          remarks="In use (04" if item == "Disinfection Buckets" and index == 0 else "In store (04)" if item == "Disinfection Buckets" else "",
                          extras={"has_unit_rows" if index == 0 else "unit_row": True}) for index in range(parts)]
            mark_unit_records(rows)
            self.assertEqual(len(rows), 1)
            self.assertEqual(len(rows[0].extras["source_group_locations"]), parts)
            self.assertEqual(len(explode(rows)), 8 if item == "Disinfection Buckets" else total)
        # Three complete untagged rows match the source total and stay units.
        rows = [Asset(item="Diagnostic equipment set", explicit_qty=3 if index == 0 else None,
                      description="white", tag="N/A" if index == 0 else "Not engraved",
                      extras={"has_unit_rows" if index == 0 else "unit_row": True}) for index in range(3)]
        self.assertEqual(len(explode(rows)), 3)

    def test_burondo_numbered_list_is_five_units(self):
        source = "team-26/Bundibugyo/Burondo-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT BURONDO HEALTH CENTRE III AND KISUBA SEED SCHOOL.docx"
        rows = [Asset(item="UPS", description="Black in color", source_file=source, source_location="Table 12 row 2")]
        for ordinal, number in enumerate((4, 10, 14, 17, 20), 1):
            rows.append(Asset(item="AP-700VA", description=f"0058{ordinal}", explicit_qty=ordinal,
                              source_file=source, source_location=f"Table 12 row {number}"))
        mark_unit_records(rows)
        self.assertEqual(len(rows), 5)
        self.assertTrue(all(row.item == "UPS" and row.explicit_qty == 1 for row in rows))
        mark_unit_records(rows)
        self.assertEqual(len(explode(rows)), 5)

    def test_kungu_incomplete_fragment_and_separate_device(self):
        source = "team-06/_team-documents/TEAM SIX HOSPITALS DTB1.xlsx"
        rows = [Asset(item="Examination Couch", tag="APA/KHCIII/EC/2021-04", description="BLACK AND CREAM", service="2022-03-01", status="Good", source_file=source, source_location="Sheet1 row 1821", extras={"unit_row": True}),
                Asset(item="Examination Couch", department="Health", description="BLACK AND CREAM", life=60, source_file=source, source_location="Sheet1 row 1822", extras={"unit_row": True}),
                Asset(item="Instrument Trolley", tag="APA/KHCIII/ML/2021-01", description="WHITE IN COLOR", remarks="Non Functional-Low resolution power lens.", source_file=source, source_location="Sheet1 row 1844", extras={"unit_row": True})]
        for number, tag in ((1827, "APA/KHCIII/GLU/2021-01"), (1831, "APA/KHCIII/GLU/2021-02"), (1832, "")):
            rows.append(Asset(item="Glucometer", explicit_qty=1 if number == 1827 else None, tag=tag, service="2022-03-01", status="Good", source_file=source, source_location=f"Sheet1 row {number}", extras={"unit_row": True}))
        mark_unit_records(rows)
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[1].item, "Low resolution power lens")
        self.assertEqual(rows[1].remarks, "Non Functional-Low resolution power lens.")
        self.assertTrue(all("Source count conflict" in row.extras["quantity_layout_evidence"] for row in rows[2:]))
        mark_unit_records(rows)
        self.assertEqual(len(explode(rows)), 5)


if __name__ == "__main__":
    unittest.main()
