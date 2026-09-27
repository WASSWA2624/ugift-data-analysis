"""Lossless audit migration and safe updates to the consolidated archive."""

import csv
import gzip
import json
import sys
import tempfile
import unittest
from collections import Counter
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from register_audits import (
    AUDIT_FILENAME, LEGACY_FILENAMES, make_audit_table, read_audit_rows,
    publish_audit_archive, read_audit_table, write_audit_table, write_audit_tables,
)
from list_book_codes import INDEX_END, INDEX_START, book_code_index_counts
from validate_asset_registers import Findings, QuantityAudit


class RegisterAuditTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.archive = self.root / AUDIT_FILENAME

    def write_csv(self, name, fieldnames, rows):
        path = self.root / name
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle, quoting=csv.QUOTE_ALL)
            writer.writerow(fieldnames)
            writer.writerows(rows)
        return path

    def test_all_tables_migrate_with_exact_headers_and_field_strings(self):
        fieldnames = [" Identifier ", "blank", "evidence", "amount", "flag", "unicode"]
        rows = [
            ["000012", "", 'Quoted "evidence", with\r\na newline', "1.2300", "False", "Kampala – café"],
            ["  space  ", "", '[[],,"x"]', "-0", "TRUE", ""],
        ]
        expected = {}
        for section, name in LEGACY_FILENAMES.items():
            path = self.write_csv(name, fieldnames, rows)
            expected[section] = read_audit_table(path, section)
            self.assertEqual(expected[section], {"fieldnames": fieldnames, "rows": rows})
        write_audit_tables(self.archive, expected)
        for section, table in expected.items():
            self.assertEqual(read_audit_table(self.archive, section), table)
            self.assertEqual(list(read_audit_rows(self.archive, section)), [dict(zip(fieldnames, row)) for row in rows])
        with gzip.open(self.archive, "rt", encoding="utf-8") as handle:
            self.assertEqual(json.load(handle), {"version": 1, "tables": expected})

    def test_section_update_preserves_other_tables_and_all_generated_fields(self):
        original = {
            "source": make_audit_table([{"source_file": "return.xlsx", "asset_rows": 12}]),
            "source_layout": make_audit_table([{"reason": "", "count": 0}]),
        }
        write_audit_tables(self.archive, original)
        write_audit_table(self.archive, "quantity", [
            {"output_rows": 2, "conflicting_counts": False, "line_cost": None},
            {"output_rows": 1, "line_cost": 1.25, "source_location": "Sheet1 row 2"},
        ])
        for section, table in original.items():
            self.assertEqual(read_audit_table(self.archive, section), table)
        self.assertEqual(read_audit_table(self.archive, "quantity"), {
            "fieldnames": ["output_rows", "conflicting_counts", "line_cost", "source_location"],
            "rows": [["2", "False", "", ""], ["1", "", "1.25", "Sheet1 row 2"]],
        })
        write_audit_table(self.archive, "quantity", [], fieldnames=["output_rows"])
        self.assertEqual(read_audit_table(self.archive, "quantity"), {"fieldnames": ["output_rows"], "rows": []})
        self.assertEqual(read_audit_table(self.archive, "source"), original["source"])

    def test_legacy_reader_and_validator_support_csv_and_archive_paths(self):
        legacy = self.write_csv(LEGACY_FILENAMES["quantity"], ["output_rows", "line_cost"], [["2", "1.00"]])
        expected = [{"output_rows": "2", "line_cost": "1.00"}]
        self.assertEqual(list(read_audit_rows(legacy, "quantity")), expected)
        self.assertEqual(list(read_audit_rows(self.archive, "quantity")), expected)
        with ExitStack() as stack:
            self.assertEqual(list(QuantityAudit(legacy, stack, Findings(), Findings(), Counter()).reader), expected)
        write_audit_table(self.archive, "quantity", expected)
        with ExitStack() as stack:
            self.assertEqual(list(QuantityAudit(self.archive, stack, Findings(), Findings(), Counter()).reader), expected)

    def test_failed_replace_preserves_existing_archive_and_removes_temporary_file(self):
        write_audit_table(self.archive, "source", [{"source_file": "original.xlsx"}])
        original = self.archive.read_bytes()
        with patch.object(Path, "replace", side_effect=OSError("replacement failed")):
            with self.assertRaisesRegex(OSError, "replacement failed"):
                write_audit_table(self.archive, "source", [{"source_file": "new.xlsx"}])
        self.assertEqual(self.archive.read_bytes(), original)
        self.assertEqual(list(self.root.iterdir()), [self.archive])

    def test_unknown_section_or_unlisted_fields_do_not_silently_discard_data(self):
        write_audit_table(self.archive, "source", [{"source_file": "original.xlsx"}])
        with self.assertRaisesRegex(ValueError, "no 'quantity' section"):
            read_audit_table(self.archive, "quantity")
        with self.assertRaisesRegex(ValueError, "absent from fieldnames"):
            write_audit_table(self.archive, "source", [{"source_file": "file.xlsx", "extra": "kept"}], fieldnames=["source_file"])
        self.assertEqual(list(read_audit_rows(self.archive, "source")), [{"source_file": "original.xlsx"}])

    def test_partial_build_preserves_canonical_until_all_sections_are_published(self):
        old = {section: make_audit_table([{"generation": "old"}]) for section in LEGACY_FILENAMES}
        write_audit_tables(self.archive, old)
        original = self.archive.read_bytes()
        staging = self.root / ".audits.in-progress.json.gz"
        write_audit_table(staging, "source", [{"generation": "new"}])
        with self.assertRaisesRegex(ValueError, "Incomplete audit build"):
            publish_audit_archive(staging, self.archive)
        self.assertEqual(self.archive.read_bytes(), original)
        for section in ("source_layout", "quantity"):
            write_audit_table(staging, section, [{"generation": "new"}])
        publish_audit_archive(staging, self.archive)
        self.assertFalse(staging.exists())
        for section in LEGACY_FILENAMES:
            self.assertEqual(list(read_audit_rows(self.archive, section)), [{"generation": "new"}])

    def test_book_index_ignores_unrelated_tables_and_requires_ordered_markers(self):
        markdown = (
            "| 1 | Before | 999 |\n" + INDEX_START + "\n"
            "| 1 | FIRST BK | 1,234 |\n| 2 | SECOND \\| BK | 5 |\n"
            + INDEX_END + "\n| 1 | After | 777 |\n"
        )
        self.assertEqual(book_code_index_counts(markdown), {"FIRST BK": 1234, "SECOND | BK": 5})
        for malformed in ("", INDEX_START, INDEX_END, INDEX_END + INDEX_START, INDEX_START + markdown):
            with self.subTest(markdown=malformed), self.assertRaises(ValueError):
                book_code_index_counts(malformed)


if __name__ == "__main__":
    unittest.main()
