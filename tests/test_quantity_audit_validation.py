"""Zero-output audit evidence must not shift the physical-asset row sequence."""

import sys
import tempfile
import unittest
from collections import Counter
from contextlib import ExitStack
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from register_audits import AUDIT_FILENAME, write_audit_table
from validate_asset_registers import Findings, QuantityAudit


def evidence(location, quantity, cost=None):
    return {
        "source_file": "source.xlsx", "source_location": location,
        "facility": "Example Health Centre III", "output_rows": quantity,
        "quantity_evidence": "[]", "line_cost": cost,
    }


def asset(location, unit="", cost=None):
    return {
        "Source file": "source.xlsx", "Source location": location,
        "Facility": "Example Health Centre III", "Unit": unit, "Cost": cost,
    }


class QuantityAuditValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.path = Path(self.temporary.name) / AUDIT_FILENAME
        self.errors, self.warnings, self.metrics = Findings(), Findings(), Counter()

    def audit(self, rows):
        write_audit_table(self.path, "quantity", rows)
        return QuantityAudit(self.path, self.stack, self.errors, self.warnings, self.metrics)

    def test_positive_zero_positive_preserves_identity_sequence_and_money_totals(self):
        audit = self.audit([evidence("first", 2, 1200), evidence("excluded", 0, 700), evidence("last", 1, 500)])
        audit.take(asset("first", "item 1 of 2", 600), 2)
        audit.take(asset("first", "item 2 of 2", 600), 3)
        audit.take(asset("last", cost=500), 4)
        audit.finish(False)
        self.assertEqual(self.errors.counts, {})
        self.assertEqual(self.metrics["audited_retained_source_lines"], 2)
        self.assertEqual(self.metrics["audited_zero_output_source_lines"], 1)
        self.assertEqual(self.metrics["audited_physical_rows"], 3)
        self.assertEqual(self.metrics["quantity_audit_expected_rows"], 3)
        self.assertEqual(self.metrics["source_line_Cost_conservation_checks"], 2)
        self.assertEqual(self.metrics["quantity_audit_source_lines_inspected"], 3)

    def test_trailing_zero_evidence_is_counted_without_unexported_sources_error(self):
        audit = self.audit([evidence("first", 1), evidence("excluded", 0), evidence("also excluded", 0)])
        audit.take(asset("first"), 2)
        audit.finish(False)
        self.assertEqual(self.errors.counts, {})
        self.assertEqual(self.metrics["audited_zero_output_source_lines"], 2)
        self.assertEqual(self.metrics["audited_physical_rows"], 1)

    def test_zero_only_audit_matches_an_empty_register(self):
        audit = self.audit([evidence("excluded", 0), evidence("also excluded", 0)])
        audit.finish(False)
        self.assertEqual(self.errors.counts, {})
        self.assertEqual(self.metrics["audited_zero_output_source_lines"], 2)
        self.assertEqual(self.metrics["audited_physical_rows"], 0)

    def test_invalid_and_negative_quantities_report_errors_without_shifting_valid_rows(self):
        audit = self.audit([evidence("invalid", value) for value in ("bad", "1.5", -2, "")] + [evidence("valid", 1)])
        audit.take(asset("valid"), 2)
        audit.finish(False)
        self.assertEqual(self.errors.counts, {"SK.quantity_audit_invalid_quantity": 4})
        self.assertEqual(self.metrics["quantity_audit_invalid_source_lines"], 4)
        self.assertEqual(self.metrics["audited_physical_rows"], 1)
        self.assertEqual(self.metrics["audited_zero_output_source_lines"], 0)

    def test_invalid_trailing_quantities_and_unexported_positive_lines_remain_errors(self):
        audit = self.audit([evidence("excluded", 0), evidence("invalid", -1), evidence("missing", 2)])
        audit.finish(False)
        self.assertEqual(self.errors.counts, {
            "SK.quantity_audit_invalid_quantity": 1,
            "SK.quantity_audit_unexported_sources": 1,
        })
        self.assertEqual(self.errors.examples["SK.quantity_audit_unexported_sources"][0]["detail"], {
            "source_lines": 1, "physical_rows": 2,
        })

    def test_positive_sequence_and_incomplete_group_checks_remain_active(self):
        audit = self.audit([evidence("excluded", 0), evidence("first", 2)])
        audit.take(asset("first", "item 2 of 2"), 2)
        audit.finish(False)
        self.assertEqual(self.errors.counts, {
            "SK.source_line_quantity_sequence": 1,
            "SK.source_line_quantity_incomplete": 1,
        })
        self.assertEqual(self.errors.examples["SK.source_line_quantity_sequence"][0]["detail"]["audit_line"], 3)

    def test_limited_scan_does_not_consume_or_certify_remaining_evidence(self):
        audit = self.audit([evidence("first", 1), evidence("excluded", 0), evidence("remaining", 2)])
        audit.take(asset("first"), 2)
        audit.finish(True)
        self.assertEqual(self.errors.counts, {})
        self.assertEqual(self.metrics["quantity_audit_source_lines_inspected"], 1)
        self.assertEqual(self.metrics["audited_zero_output_source_lines"], 0)


if __name__ == "__main__":
    unittest.main()
