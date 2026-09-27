"""IFMS source rows may name their facility in Description instead of a site column."""

import unittest

from merge_shared_asset_registers import Asset, facility_from_description, in_scope, resolve_places


class DistrictDescriptionFacilityTests(unittest.TestCase):
    def test_explicit_school_building_keeps_source_values(self):
        row = Asset(item="Libraries", description="KABWERI SEED SCHOOL", lg="Kibuku",
                    tag="862-BULD-0269", cost=50000000,
                    source_file="team-12/Kibuku/_district-documents/register.xlsx")
        row.facility = facility_from_description(row)
        resolve_places(row, [("Kibuku", "")], row.source_file)
        self.assertTrue(in_scope(row))
        self.assertIn("Kabweri", row.facility)
        self.assertEqual(row.cost, 50000000)
        self.assertEqual(row.tag, "862-BULD-0269")

    def test_payment_and_waterworks_mentions_are_not_new_assets(self):
        for item, description in (
            ("Water works_Acquire", "KOBWIN SEED SCHOOL"),
            ("Build other than dwell_Acquire", "PAYMENT OF CONSTRUCTION OF WORKS FOR KABWERI SEED SECONDARY SCHOOL"),
            ("Schools", "Insurance for KABWERI SEED SCHOOL"),
        ):
            self.assertEqual(facility_from_description(Asset(item=item, description=description, lg="Kibuku")), "")

    def test_health_centre_requires_reconciled_identity(self):
        self.assertEqual(facility_from_description(Asset(item="Hospitals", description="Unlisted Test Facility HC III", lg="Kibuku")), "")
        self.assertEqual(facility_from_description(Asset(item="Hospitals", description="NALUBEMBE HCIII", lg="Kibuku")), "NALUBEMBE HCIII")

    def test_existing_facility_and_named_seed_scope_are_preserved(self):
        self.assertEqual(facility_from_description(Asset(item="Schools", description="KABWERI SEED SCHOOL", facility="Existing School", lg="Kibuku")), "")
        self.assertEqual(facility_from_description(Asset(item="Schools", description="New Example Seed Secondary School", lg="Kibuku")), "New Example Seed Secondary School")


if __name__ == "__main__":
    unittest.main()
