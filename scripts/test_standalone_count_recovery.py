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


if __name__ == "__main__":
    unittest.main()
