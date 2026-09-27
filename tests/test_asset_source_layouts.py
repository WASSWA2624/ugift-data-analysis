"""Regression for the independently reviewed Nshwere mixed furniture table."""

import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from asset_source_layouts import (
    NSHWERE_CONSOLIDATED_SOURCE, NSHWERE_SOURCE, NYAMARWA_SOURCE,
    REVIEWED_UNIT_BLOCKS, repair_nshwere_furniture, repair_nyamarwa_air_conditioner,
    repair_reviewed_unit_blocks,
)
from merge_shared_asset_registers import Asset, explode, read_workbook, union_facility_submissions


class NshwereFurnitureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = read_workbook(Path(__file__).resolve().parents[1] / "raw-data-grouped" / NSHWERE_SOURCE)

    def test_verified_source_groups_survive_expansion(self):
        from copy import deepcopy

        assets = deepcopy(self.original)
        unrelated = [(a.source_location, a.item) for a in assets if not a.source_location.startswith("Table 11 row ")]
        audit = repair_nshwere_furniture(assets)
        recovered = [a for a in assets if a.extras.get("nshwere_furniture_recovered")]
        self.assertEqual(len(recovered), 32)
        self.assertEqual(audit[0]["physical_assets"], 472)
        self.assertEqual(audit[0]["counts_by_item"], {"Desk": 116, "Chair": 154, "Stool": 150, "Table": 49, "Water tank": 3})
        self.assertEqual(unrelated, [(a.source_location, a.item) for a in assets if not a.source_location.startswith("Table 11 row ")])
        stools = [a for a in recovered if a.item == "Stool" and a.explicit_qty == 64]
        self.assertEqual([a.department for a in stools], ["1st laboratory", "2nd laboratory"])
        self.assertNotEqual(stools[0].source_location, stools[1].source_location)
        self.assertTrue(any("chaistool" in a.extras["source_layout_original"]["description"] for a in recovered))
        for asset in recovered:
            original = asset.extras["source_layout_original"]
            if original["source_location"] in {"Table 11 row 5", "Table 11 row 12", "Table 11 row 13"}:
                self.assertEqual(asset.remarks, original["remarks"])
        self.assertEqual(repair_nshwere_furniture(assets), [])
        units = explode(recovered)
        self.assertEqual(len(units), 472)
        self.assertEqual(Counter(a.item for a in units), {"Desk": 116, "Chair": 154, "Stool": 150, "Table": 49, "Water tank": 3})
        self.assertEqual(sum("broken" in a.status.casefold() for a in units), 5)

    def test_mixed_line_totals_and_original_provenance_are_preserved(self):
        from copy import deepcopy

        assets = deepcopy(self.original)
        source = next(a for a in assets if a.source_location == "Table 11 row 7")
        for name in ("cost", "recoverable", "acc_dep", "nbv", "ytd"):
            setattr(source, name, 157000)
        repair_nshwere_furniture(assets)
        recovered = [a for a in assets if a.source_location.startswith("Table 11 row 7 (")]
        self.assertEqual(len(recovered), 5)
        for name in ("cost", "recoverable", "acc_dep", "nbv", "ytd"):
            self.assertAlmostEqual(sum(getattr(a, name) for a in recovered), 157000)
        self.assertTrue(all(a.extras["source_layout_original"]["source_location"] == "Table 11 row 7" for a in recovered))
        self.assertTrue(all(a.source_file == NSHWERE_SOURCE for a in recovered))
        recovered[0].extras["source_cells"].append("isolated test edit")
        self.assertNotIn("isolated test edit", recovered[1].extras["source_cells"])

    def test_consolidated_mirror_reconciles_to_one_physical_return(self):
        from copy import deepcopy

        consolidated = read_workbook(Path(__file__).resolve().parents[1] / "raw-data-grouped" / NSHWERE_CONSOLIDATED_SOURCE)
        untouched = deepcopy([a for a in consolidated if a.source_location not in {
            f"Sheet4 row {row}" for row in (496, 497, 498, 499, 501, 502, 504, 505, 506, 507, 508)
        }])
        assets = deepcopy(self.original) + consolidated
        audit = repair_nshwere_furniture(assets)
        self.assertEqual([a["physical_assets"] for a in audit], [472, 472])
        recovered = [a for a in assets if a.extras.get("nshwere_furniture_recovered")]
        self.assertEqual(len(recovered), 64)
        mirror = [a for a in recovered if a.source_file == NSHWERE_CONSOLIDATED_SOURCE]
        self.assertEqual(len(mirror), 32)
        self.assertEqual(sum(a.explicit_qty for a in mirror), 472)
        laboratory = [a for a in mirror if a.source_location.startswith("Sheet4 row 501 (")]
        self.assertEqual(len(laboratory), 5)
        for asset in laboratory:
            self.assertEqual(asset.tag, "")
            self.assertEqual(asset.extras["source_layout_original"]["tag"],
                             "Tables 14,stools 64,stools 64,chairs 2,tables 13")
            self.assertEqual(asset.extras["source_layout_original"]["source_location"], "Sheet4 row 501")
            self.assertEqual(asset.extras["source_group_locations"], ["Sheet4 row 501"])
        self.assertEqual({a.extras["source_group_locations"][0] for a in mirror if a.item == "Water tank"},
                         {"Sheet4 row 508", "Sheet4 row 509", "Sheet4 row 510"})
        self.assertEqual(untouched, [a for a in assets if a.source_file == NSHWERE_CONSOLIDATED_SOURCE
                                    and not a.extras.get("nshwere_furniture_recovered")])
        self.assertEqual(repair_nshwere_furniture(assets), [])
        combined, notes = union_facility_submissions(recovered)
        self.assertTrue(notes)
        self.assertEqual(len(combined), 32)
        units = explode(combined)
        self.assertEqual(len(units), 472)
        self.assertEqual(Counter(a.item for a in units),
                         {"Desk": 116, "Chair": 154, "Stool": 150, "Table": 49, "Water tank": 3})
        self.assertEqual(sum("broken" in a.status.casefold() for a in units), 5)


class NyamarwaLayoutTests(unittest.TestCase):
    def test_air_conditioner_quantity_continuation_keeps_its_asset_name(self):
        assets = read_workbook(Path(__file__).resolve().parents[1] / "raw-data-grouped" / NYAMARWA_SOURCE)
        recorder = next(a for a in assets if a.source_location == "Table 12 row 21")
        original_rows = len(assets)
        recorder.cost = 120000  # A recorder's amount must not transfer to the adjacent asset.
        audit = repair_nyamarwa_air_conditioner(assets)
        self.assertEqual(audit[0]["physical_assets"], 1)
        self.assertEqual(len(assets), original_rows + 1)
        recovered = next(a for a in assets if a.extras.get("nyamarwa_air_conditioner_recovered"))
        self.assertEqual(recovered.item, "Air conditioner")
        self.assertEqual(recovered.description, "AIR CONDITONER")
        self.assertEqual(recovered.explicit_qty, 1)
        self.assertEqual(recovered.source_location, "Table 12 rows 24-25")
        self.assertEqual(recovered.extras["source_group_locations"], ["Table 12 row 24", "Table 12 row 25"])
        self.assertEqual(recovered.extras["source_cells"], ["AIR CONDITONER", "1 SET"])
        self.assertEqual(recovered.facility, recorder.facility)
        self.assertEqual(recovered.remarks, "")
        self.assertIsNone(recovered.cost)
        self.assertEqual(recorder.cost, 120000)
        self.assertEqual(recorder.description, "")
        self.assertFalse(any(a.item == "1 SET" for a in assets))
        self.assertEqual(len(explode([recovered])), 1)
        self.assertEqual(repair_nyamarwa_air_conditioner(assets), [])


class ReviewedUnitBlockTests(unittest.TestCase):
    def test_original_returns_prove_units_and_preserve_count_discrepancies(self):
        from copy import deepcopy

        sources = {block.source for block in REVIEWED_UNIT_BLOCKS} | {block.primary for block in REVIEWED_UNIT_BLOCKS}
        root = Path(__file__).resolve().parents[1] / "raw-data-grouped"
        parsed = {source: read_workbook(root / source) for source in sorted(sources)}
        # Two independent, identical grouped source lines still represent 240
        # assets. No normalization is inferred from their repetition alone.
        unrelated = Asset(item="Chairs (120)", source_file="unreviewed.docx", source_location="Table 1 row 2")
        parsed["unreviewed.docx"] = [unrelated, deepcopy(unrelated)]
        before = sum(map(len, parsed.values()))
        audit = repair_reviewed_unit_blocks(parsed)
        self.assertEqual(len(audit), len(REVIEWED_UNIT_BLOCKS))
        self.assertEqual(sum(map(len, parsed.values())), before - len(REVIEWED_UNIT_BLOCKS))
        for block in REVIEWED_UNIT_BLOCKS:
            records = [a for a in parsed[block.source] if a.extras.get("reviewed_unit_block", {}).get("primary_location") == block.primary_location
                       and a.extras.get("reviewed_unit_block", {}).get("primary_source") == block.primary]
            expected = block.last - block.first + 1
            self.assertEqual(len(records), expected)
            self.assertEqual(len(explode(records)), expected)
            self.assertTrue(all(a.extras["proven_unit_row"] for a in records))
            self.assertFalse(any(a.source_location == block.primary_location for a in parsed[block.primary]))
            self.assertTrue(all(block.primary in a.extras["filled_from"] for a in records))
            if expected != block.primary_quantity:
                self.assertTrue(all("Source count conflict" in a.extras["quantity_layout_evidence"] for a in records))
        bad_by_block = {}
        for assets in parsed.values():
            for asset in assets:
                block = asset.extras.get("reviewed_unit_block")
                if block and asset.remarks.casefold() in {"broken", "spoilt", "spoiled"}:
                    self.assertEqual(asset.status, asset.remarks)
                    key = block["consolidated_rows"]
                    bad_by_block[key] = bad_by_block.get(key, 0) + 1
        self.assertEqual(bad_by_block["Sheet1 rows 875-1177"], 3)
        self.assertEqual(bad_by_block["Sheet1 rows 473-665"], 3)
        self.assertEqual(bad_by_block["Sheet1 rows 328-448"], 10)
        self.assertEqual(bad_by_block["Sheet1 rows 1628-1932"], 4)
        self.assertEqual(len(explode(parsed["unreviewed.docx"])), 240)
        self.assertEqual(repair_reviewed_unit_blocks(parsed), [])


if __name__ == "__main__":
    unittest.main()
