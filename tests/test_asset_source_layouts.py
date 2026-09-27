"""Regression for the independently reviewed Nshwere mixed furniture table."""

import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from asset_source_layouts import NSHWERE_SOURCE, repair_nshwere_furniture
from merge_shared_asset_registers import Asset, explode, read_workbook


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


if __name__ == "__main__":
    unittest.main()
