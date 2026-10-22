"""Regression checks for science apparatus mistaken for transport equipment."""

from collections import Counter
import unittest

from build_guideline_registers import ELECTRICAL, MEDICAL, Registers, build_values


class LaboratoryClassificationTests(unittest.TestCase):
    def setUp(self):
        self.registers = Registers([])

    def test_recorded_science_apparatus_names(self):
        for name in (
            "Van de Graaff generator", "Van De Graaf Generator",
            "Van-de-graph Generator", "Van de Graaff generators",
            "Strip cup", "Strip cups", "Strip-cups",
        ):
            with self.subTest(name=name):
                self.assertEqual(self.registers.classify(name), MEDICAL)

    def test_transport_power_and_unrelated_strips_keep_their_classes(self):
        for name in ("Van", "Passenger van", "Delivery vans"):
            with self.subTest(name=name):
                self.assertEqual(self.registers.classify(name)[2], "LIGHT VEHICLES")
        for name in ("Diesel generator", "Power generator"):
            with self.subTest(name=name):
                self.assertEqual(self.registers.classify(name), ELECTRICAL)
        for name in ("Test strips", "Strip board", "Kitchen cups"):
            with self.subTest(name=name):
                self.assertNotEqual(self.registers.classify(name), MEDICAL)

    def test_laboratory_accounts_and_recorded_lives_survive_row_generation(self):
        headers = [
            "ASSET_CATEGORY_MINOR1", "ASSET_CATEGORY_MINOR2",
            "ASSET_EXP_ACCT_ACCOUNT", "ASSET_CLR_ACCT_ACCOUNT",
            "LIFE_IN_MONTHS", "ATTRIBUTE5(Life in Months)",
        ]
        registers = Registers(headers)
        for name in ("Van de Graaff generator", "Strip cup", "Strip cups"):
            for life in (60, 120):
                with self.subTest(name=name, life=life):
                    values = build_values(
                        {"Equipment/Item": name, "Life in Months": life,
                         "Cost": 100000, "Equipment status": "Functional"},
                        registers, borrow=False, costs={}, lives={}, dates={},
                        stats=Counter(),
                    )
                    self.assertEqual(values, [
                        "OTHER MACHINERY AND EQUIPMENT", "MED LAB RESEARCH APPLIANCES",
                        "231233", "513001", (life, None), life,
                    ])


if __name__ == "__main__":
    unittest.main()
