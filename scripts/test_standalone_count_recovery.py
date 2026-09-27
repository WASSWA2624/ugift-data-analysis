"""Source-grid checks for explicitly counted rows lost as empty template lines."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from docx import Document
import merge_shared_asset_registers as registers


class StandaloneCountRecoveryTests(unittest.TestCase):
    def source(self, folder, names):
        document = Document()
        table = document.add_table(rows=1, cols=15)
        for cell, text in zip(table.rows[0].cells, registers.HEADERS[:15]):
            cell.text = text
        for name, description in names:
            cells = table.add_row().cells
            cells[0].text = name
            cells[3].text = description
        document.save(Path(folder) / "source.docx")

    def anchor(self, item, row, **kwargs):
        return registers.Asset(item=item, source_file="source.docx", source_location=f"Table 1 row {row}",
                               facility="Named HC III", lg="Named district", facility_type="Health centre", **kwargs)

    def test_separate_counted_rows_restore_identity_and_keep_anchor_facts(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(registers, "GROUPED", Path(folder)):
            self.source(folder, [("Cupboard (6)", "Metallic"), ("Drip stand (9)", "")])
            cupboard = self.anchor("Cupboard (6)", 2, description="Metallic Drip stand (9)", cost=600000, service="2025")
            parsed = {"source.docx": [cupboard]}
            audit = registers.recover_standalone_count_rows(parsed)
            self.assertEqual(len(audit), 1)
            self.assertEqual(cupboard.description, "Metallic")
            self.assertEqual((cupboard.cost, cupboard.service), (600000, "2025"))
            self.assertEqual([(a.item, a.source_location) for a in parsed["source.docx"]],
                             [("Cupboard (6)", "Table 1 row 2"), ("Drip stand (9)", "Table 1 row 3")])
            self.assertEqual(len(registers.explode(parsed["source.docx"])), 15)
            self.assertEqual(registers.recover_standalone_count_rows(parsed), [])

    def test_initial_count_rows_recovered_but_model_suffix_and_empty_name_omitted(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(registers, "GROUPED", Path(folder)):
            self.source(folder, [("Benches (120)", ""), ("HP LaserJet (1320)", ""), ("Empty template chair", ""), ("Cupboard (6)", "Metallic"), ("(88)", ""), ("Not in use(3)", ""), ("Store(2)", "")])
            parsed = {"source.docx": [self.anchor("Cupboard (6)", 5)]}
            audit = registers.recover_standalone_count_rows(parsed)
            self.assertEqual([row["item"] for row in audit], ["Benches (120)"])
            self.assertEqual(parsed["source.docx"][0].explicit_qty, 120)

    def test_ambiguous_table_facility_is_reported_without_guessing(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(registers, "GROUPED", Path(folder)):
            self.source(folder, [("Cupboard", "Metallic"), ("Bench (3)", ""), ("Other cupboard", "Wooden")])
            second = self.anchor("Other cupboard", 4)
            second.facility = "Other HC III"
            parsed = {"source.docx": [self.anchor("Cupboard", 2), second]}
            audit = registers.recover_standalone_count_rows(parsed)
            self.assertEqual(audit[0]["status"], "skipped")
            self.assertEqual(len(parsed["source.docx"]), 2)

    def test_standalone_prefix_suffix_compact_and_worded_counts(self):
        for item in ("BP machines 120", "120 BP machines", "BP machines 120pcs", "One hundred twenty BP machines"):
            with self.subTest(item=item), tempfile.TemporaryDirectory() as folder, patch.object(registers, "GROUPED", Path(folder)):
                self.source(folder, [(item, ""), ("Cupboard", "Metallic")])
                parsed = {"source.docx": [self.anchor("Cupboard", 3)]}
                audit = registers.recover_standalone_count_rows(parsed)
                self.assertEqual(audit[0]["quantity"], 120)
                self.assertEqual(len(registers.explode(parsed["source.docx"])), 121)

    def test_nalugai_and_tajar_mirror_fragments_fold_to_six_cupboards(self):
        for facility, source_row, fragments in (
            ("Nalugai", 551, ["Drip Stand (09)"]),
            ("Tajar", 814, ["Drip Stand (09)", "ESR Stand (01)"]),
        ):
            with self.subTest(facility=facility):
                primary_source = f"team-09/Bukedea/{facility}-HC-III/{facility.upper()} HC III.docx"
                mirror_source = "team-09/_team-documents/TEAM NINE HOSPITALS EXCELL DTB.xlsx"
                old_description = "Metallic " + " ".join(fragments)
                primary = registers.Asset(item="Cupboard Steel, Lockable (06)", description="Metallic",
                                          department="Health", status="Functional", tag="NOT engraved",
                                          lg="Bukedea", facility=facility, source_file=primary_source, source_location="Table 6 row 19")
                mirror = registers.Asset(**{**vars(primary), "description": old_description, "source_file": mirror_source,
                                             "source_location": f"Sheet1 row {source_row}", "cost": 600000,
                                             "extras": {"source_cells": [primary.item, "Health", "Metallic", "Functional"]}})
                originals = [primary]
                corrections = []
                for index, fragment in enumerate(fragments, 22):
                    description = registers.clean(old_description.replace(fragment, "", 1))
                    corrections.append((primary, old_description, description, fragment))
                    old_description = description
                    originals.append(registers.Asset(item=fragment, lg="Bukedea", facility=facility,
                                                     source_file=primary_source, source_location=f"Table 6 row {index}"))
                parsed = {primary_source: originals, mirror_source: [mirror]}
                audit = registers.propagate_count_fragment_repairs(parsed, corrections)
                self.assertEqual(len(audit), len(fragments))
                self.assertEqual(mirror.description, "Metallic")
                self.assertEqual(mirror.cost, 600000)
                combined, _ = registers.union_facility_submissions(originals + [mirror])
                rows = registers.explode(combined)
                self.assertEqual(sum(row.item == "Cupboard Steel, Lockable" for row in rows), 6)
                self.assertEqual(len(rows), 15 if facility == "Nalugai" else 16)

    def test_mirror_correction_preserves_physical_duplicates_and_real_source_lists(self):
        primary = self.anchor("Cupboard (6)", 2, description="Metallic")
        old = "Metallic Drip Stand (9)"
        mirrors = [registers.Asset(**{**vars(primary), "description": old, "source_file": "mirror.xlsx",
                                       "source_location": f"Sheet row {row}",
                                       "extras": {"source_cells": ["Cupboard (6)", "Metallic"]}})
                   for row in (2, 3)]
        recorded_list = registers.Asset(**{**vars(primary), "description": old, "source_file": "other.xlsx",
                                          "extras": {"source_cells": ["Cupboard (6)", old]}})
        parsed = {"source.docx": [primary], "mirror.xlsx": mirrors, "other.xlsx": [recorded_list]}
        audit = registers.propagate_count_fragment_repairs(parsed, [(primary, old, "Metallic", "Drip Stand (9)")])
        self.assertEqual(len(audit), 2)
        self.assertEqual(len(mirrors), 2)
        self.assertEqual(recorded_list.description, old)
        self.assertEqual(registers.propagate_count_fragment_repairs(parsed, [(primary, old, "Metallic", "Drip Stand (9)")]), [])
        combined, _ = registers.union_facility_submissions([primary, *mirrors])
        self.assertEqual(len(registers.explode(combined)), 12)

    def test_receipt_continuations_dates_units_and_zero_are_not_new_assets(self):
        ignored = ["Received 20 computers", "Received 150", "2 were received", "3 were receuvef",
                   "1 eeceived", "Remaining monitors after theft dec 2023", "1 SET", "Fetoscope, Dopplar(0)"]
        with tempfile.TemporaryDirectory() as folder, patch.object(registers, "GROUPED", Path(folder)):
            self.source(folder, [("Computers", "Desktop computers"), *((item, "") for item in ignored),
                                 ("Received 900 textbooks", "")])
            original = self.anchor("Computers", 2, description="Desktop computers Received 20 computers")
            parsed = {"source.docx": [original]}
            audit = registers.recover_standalone_count_rows(parsed)
            self.assertEqual([entry["item"] for entry in audit], ["Received 900 textbooks"])
            self.assertEqual(registers.represented_count(original), 20)
            self.assertEqual(parsed["source.docx"][1].explicit_qty, 900)

    def test_named_kit_and_set_contents_are_one_asset_each(self):
        names = ("Cork borer set of 6", "Dissecting kit (14 pieces)")
        with tempfile.TemporaryDirectory() as folder, patch.object(registers, "GROUPED", Path(folder)):
            self.source(folder, [("Wire", "Copper"), *((item, "") for item in names)])
            wire = self.anchor("Wire", 2, description="Copper " + " ".join(names))
            parsed = {"source.docx": [wire]}
            audit = registers.recover_standalone_count_rows(parsed)
            self.assertEqual([entry["quantity"] for entry in audit], [1, 1])
            self.assertEqual(wire.description, "Copper")
            output = registers.explode(parsed["source.docx"])
            self.assertEqual(len(output), 3)
            self.assertEqual([row.item for row in output], ["Wire", "Cork borer set", "Dissecting kit"])
            self.assertEqual([row.description for row in output[1:]], list(names))

    def test_reviewed_zero_omissions_keep_separate_positive_model(self):
        source = "team-14/Bududa/Nakatsi-Seed-Secondary-School/Asset-Verification-Toolkit.docx"
        rows = [registers.Asset(item=item, source_file=source, source_location=f"Table 11 row {row}",
                                status="Available in good condition", remarks="Available in good condition and serialised")
                for row, item in ((22, "Human ear model (1)"), (23, "Human Ear chart (0)"),
                                  (26, "U-tube manometer (0)"), (28, "Mortar and pestle (0)"))]
        audit = registers.exclude_reviewed_zero_rows({source: rows})
        self.assertEqual(len(audit), 3)
        self.assertEqual([row.item for row in rows], ["Human ear model (1)"])
        self.assertTrue(all("Source count conflict" in entry["reason"] for entry in audit))


if __name__ == "__main__":
    unittest.main()
