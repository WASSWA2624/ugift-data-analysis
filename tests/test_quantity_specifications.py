"""Verified source specifications and package contents are not asset counts."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from merge_shared_asset_registers import Asset, decide_groups


class QuantitySpecificationTests(unittest.TestCase):
    def check(self, expected, **values):
        asset = Asset(**values)
        result = decide_groups(asset, True)
        self.assertEqual(sum(n for n, _ in result[1]), expected, asset.extras)
        self.assertEqual(asset.item, values["item"])
        return asset

    def test_original_wire_sizes_keep_physical_piece_counts(self):
        for item, description, expected in (
            ("Constantin wires, 28 gauge", "3 pieces", 3),
            ("30 gauge", "2 pieces", 2),
            ("26 gauge", "1 piece", 1),
            ("Constantine Wire SWG 28", "2 pcs", 2),
        ):
            with self.subTest(item=item):
                self.check(expected, item=item, description=description)
        self.check(4, item="Micrometer screw gauge", description="4 pcs")

    def test_oxygen_plant_capacity_does_not_override_one_plant(self):
        self.check(1, item="70 Nm3/hr Oxygen plant", explicit_qty=1, cost=1500000000)
        self.check(1, item="70 Nm³/hr Oxygen plant", explicit_qty=1)
        self.check(70, item="Oxygen plant", explicit_qty=70)

    def test_package_contents_do_not_multiply_packs(self):
        for item, qty in (
            ("Cork borers set of 6", 2),
            ("Microscope cover slip 22×22 pack of 100", 1),
            ("Microscope slides pack of 72", 5),
            ("Optical pins PACK OF 50", 10),
            ("Rubber bungs for conical flasks PACK OF 100", 10),
            ("Wooden Corks (Assorted sizes) PACK OF 50", 1),
            ("Test tubes 15X125MM BOROSILICATE GLASS PACK OF 100", 2),
        ):
            with self.subTest(item=item):
                self.check(qty, item=item, explicit_qty=qty)
        self.check(2, item="Cork Borers, set of 6", description="2 pcs")
        self.check(4, item="Filter paper 4 boxes (400 pcs)")
        self.check(1, item="Filter paper box (400 pcs)")
        self.check(10, item="Mass Hangers 50 gm (capacity 16 pcs)", description="10 pcs")
        self.check(120, item="BP machine", description="120 units")
        self.check(900, item="Received 900 textbooks")
        self.check(3, item="Delivery kit", description="3 kits containing 14 items")

    def test_plain_parenthetical_package_counts_remain_asset_quantities(self):
        for item, expected in (
            ("Instrument Set(20)", 20),
            ("Diagnostic Equipment Set(2)", 2),
            ("Delivery Kit (2)", 2),
            ("Storage Box [20]", 20),
            ("Hollow Ware Set, Ward(03)", 3),
        ):
            with self.subTest(item=item):
                self.check(expected, item=item)
        self.check(1, item="Dissecting kit (14 pieces)")
        self.check(1, item="Instrument set (20 items)")

    def test_mutushet_original_three_sets_retains_conflict(self):
        asset = self.check(3, item="Hollow Ware Set, Hospital", asset_number="3",
                           description="one set containing 11 items of the ward", tag="Not yet",
                           source_file="team-15/Bukwo/Mutushet-HC-III/Asset-Verification-Toolkit.docx",
                           source_location="Table 6 row 103")
        self.assertTrue(any(label.startswith("source count conflict:")
                            for _, label in asset.extras["quantity_evidence"]))
        self.assertEqual(asset.description, "one set containing 11 items of the ward")


if __name__ == "__main__":
    unittest.main()
