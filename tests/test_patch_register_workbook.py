"""Review checks for safe, narrowly scoped register cell updates."""

import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from patch_register_workbook import apply_updates, worksheet_parts

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
WORKBOOK = (
    f'<workbook xmlns="{NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<sheets><sheet name="Asset Register" sheetId="1" r:id="rId1"/></sheets></workbook>'
).encode()
RELATIONSHIPS = (
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Target="worksheets/sheet1.xml" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"/>'
    '</Relationships>'
).encode()


class ChunkedStream(io.BytesIO):
    def __init__(self, content, size):
        super().__init__(content)
        self.chunk_size = size

    def read(self, size=-1):
        return super().read(min(size, self.chunk_size) if size >= 0 else self.chunk_size)


class PatchRegisterWorkbookTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source.xlsx"
        self.destination = self.root / "updated.xlsx"

    def workbook(self, row=None, suffix=b""):
        row = row or (
            b'<row r="2" ht="18"><c r="A2" t="s"><v>0</v></c>'
            b'<c r="B2" s="7"><v>42</v></c><c r="D2" t="inlineStr">'
            b'<is><t xml:space="preserve">  unchanged &amp; quoted  </t></is></c></row>'
        )
        sheet = (
            f'<worksheet xmlns="{NS}"><dimension ref="A1:E3"/><sheetData>'.encode()
            + b'<row r="1"><c r="A1" t="inlineStr"><is><t>Header</t></is></c></row>'
            + row + b'<row r="3"/>' + b'</sheetData>' + suffix
            + b'<autoFilter ref="A1:E3"/></worksheet>'
        )
        parts = {
            "xl/workbook.xml": WORKBOOK,
            "xl/_rels/workbook.xml.rels": RELATIONSHIPS,
            "xl/worksheets/sheet1.xml": sheet,
            "xl/sharedStrings.xml": f'<sst xmlns="{NS}"><si><t>Shared label</t></si></sst>'.encode(),
            "xl/styles.xml": b'<styles>preserve exact style content</styles>',
            "customXml/evidence.xml": b'\x00unchanged evidence\xff',
        }
        with ZipFile(self.source, "w") as workbook:
            for name, content in parts.items():
                workbook.writestr(name, content)
        return parts

    def test_chunk_boundaries_preserve_every_byte_and_identify_only_complete_rows(self):
        raw = (
            b'<?xml version="1.0"?><worksheet><sheetData>'
            b'<row r="1"><c r="A1"><v>123</v></c></row>'
            b'<row r="2"/><row r="3"><c r="A3" t="inlineStr"><is><t>'
            + "é".encode() + b'</t></is></c></row></sheetData><autoFilter ref="A1:A3"/></worksheet>'
        )
        for size in (1, 3, 7, 8, 13, 32, 1024 * 1024):
            with self.subTest(chunk_size=size):
                parts = list(worksheet_parts(ChunkedStream(raw, size)))
                self.assertEqual(b"".join(content for _, content in parts), raw)
                self.assertEqual(len([content for is_row, content in parts if is_row]), 3)

    def test_row_break_suffix_is_preserved_without_treating_it_as_an_incomplete_row(self):
        parts = self.workbook(suffix=b'<rowBreaks count="1" manualBreakCount="1"><brk id="2" max="16383" man="1"/></rowBreaks>')
        result = apply_updates(self.source, self.destination, [{"sheet": "Asset Register", "cell": "B2", "expected": 42, "value": 43}])
        self.assertEqual(result["updates_applied"], 1)
        with ZipFile(self.destination) as workbook:
            self.assertIn(b'<rowBreaks count="1"', workbook.read("xl/worksheets/sheet1.xml"))
        self.assert_source_unchanged(parts)

    def assert_source_unchanged(self, parts):
        with ZipFile(self.source) as source:
            self.assertEqual({name: source.read(name) for name in source.namelist()}, parts)

    def test_updates_preserve_other_cells_package_parts_styles_and_xml_suffix(self):
        parts = self.workbook()
        result = apply_updates(self.source, self.destination, [
            {"sheet": "Asset Register", "cell": "A2", "expected": "Shared label", "value": 'new <label> & "text"'},
            {"sheet": "Asset Register", "cell": "B2", "expected": 42, "value": 43},
            {"sheet": "Asset Register", "cell": "C2", "expected": None, "value": "", "style": 5},
            {"sheet": "Asset Register", "cell": "E3", "expected": None, "value": True, "style": 9},
        ])
        self.assertEqual(result["updates_applied"], 4)
        with ZipFile(self.destination) as target:
            self.assertEqual(set(target.namelist()), set(parts))
            for name, data in parts.items():
                if name != "xl/worksheets/sheet1.xml":
                    self.assertEqual(target.read(name), data)
            sheet = target.read("xl/worksheets/sheet1.xml")
        self.assert_source_unchanged(parts)
        unchanged_cell = b'<c r="D2" t="inlineStr"><is><t xml:space="preserve">  unchanged &amp; quoted  </t></is></c>'
        self.assertIn(unchanged_cell, sheet)
        self.assertTrue(sheet.endswith(b'<autoFilter ref="A1:E3"/></worksheet>'))
        cells = {node.get("r"): node for node in ET.fromstring(sheet).iter(f"{{{NS}}}c")}
        self.assertEqual(cells["B2"].get("s"), "7")
        self.assertEqual(cells["C2"].get("s"), "5")
        self.assertEqual(cells["E3"].get("s"), "9")
        self.assertEqual("".join(cells["A2"].itertext()), 'new <label> & "text"')

    def test_stale_precondition_and_incomplete_plan_fail_without_destination_or_temporary_files(self):
        parts = self.workbook()
        for updates, message in (
            ([{"sheet": "Asset Register", "cell": "B2", "expected": 99, "value": 43}], "expected 99"),
            ([{"sheet": "Asset Register", "cell": "B99", "expected": None, "value": 43}], "Missing target rows"),
            ([{"sheet": "Unknown", "cell": "B2", "expected": None, "value": 43}], "Unknown sheets"),
        ):
            with self.subTest(error=message), self.assertRaisesRegex(ValueError, message):
                apply_updates(self.source, self.destination, updates)
            self.assertFalse(self.destination.exists())
            self.assertEqual(list(self.root.iterdir()), [self.source])
            self.assert_source_unchanged(parts)

    def test_formula_overwrite_is_refused_without_modifying_original(self):
        parts = self.workbook(row=b'<row r="2"><c r="B2" s="7"><f>SUM(A1:A2)</f><v>42</v></c></row>')
        with self.assertRaisesRegex(ValueError, "Cannot overwrite formula B2"):
            apply_updates(self.source, self.destination, [{"sheet": "Asset Register", "cell": "B2", "expected": 42, "value": 43}])
        self.assertFalse(self.destination.exists())
        self.assertEqual(list(self.root.iterdir()), [self.source])
        self.assert_source_unchanged(parts)

    def test_asset_identity_prevents_applying_a_blank_fill_to_a_different_asset(self):
        parts = self.workbook()
        updates = [{"sheet": "Asset Register", "cell": "C2", "expected": None,
                    "value": "serial", "identity": {"A": "Different asset"}}]
        with self.assertRaisesRegex(ValueError, "asset identity"):
            apply_updates(self.source, self.destination, updates)
        self.assertFalse(self.destination.exists())
        self.assert_source_unchanged(parts)

    def test_reviewed_long_identifier_wrap_and_height_preserve_other_row_attributes(self):
        self.workbook()
        apply_updates(self.source, self.destination, [{"sheet": "Asset Register", "cell": "C2",
            "expected": None, "value": "A-long-serial-number", "style": 10, "row_height": 30}])
        with ZipFile(self.destination) as book:
            xml = book.read("xl/worksheets/sheet1.xml")
        row = ET.fromstring(xml).find(f"{{{NS}}}sheetData/{{{NS}}}row[@r='2']")
        self.assertEqual(row.get("ht"), "30")
        self.assertEqual(row.get("customHeight"), "1")
        self.assertEqual(row.find(f"{{{NS}}}c[@r='C2']").get("s"), "10")

    def test_self_closing_blank_cell_does_not_consume_its_populated_neighbor(self):
        row = b'<row r="2"><c r="B2" s="7"/><c r="C2"><v>99</v></c></row>'
        parts = self.workbook(row=row)
        apply_updates(self.source, self.destination, [{"sheet": "Asset Register", "cell": "B2", "expected": None, "value": 43}])
        with ZipFile(self.destination) as target:
            sheet = target.read("xl/worksheets/sheet1.xml")
        self.assertIn(b'<c r="C2"><v>99</v></c>', sheet)
        self.assertIn(b'<c r="B2" s="7" t="n"><v>43</v></c>', sheet)
        self.assert_source_unchanged(parts)

    def test_existing_destination_and_duplicate_updates_are_refused(self):
        parts = self.workbook()
        update = {"sheet": "Asset Register", "cell": "B2", "expected": 42, "value": 43}
        with self.assertRaisesRegex(ValueError, "Duplicate update"):
            apply_updates(self.source, self.destination, [update, update])
        self.destination.write_bytes(b"preserve existing destination")
        with self.assertRaises(FileExistsError):
            apply_updates(self.source, self.destination, [update])
        self.assertEqual(self.destination.read_bytes(), b"preserve existing destination")
        self.assert_source_unchanged(parts)

    def test_failed_final_replace_cleans_temporary_and_preserves_original(self):
        parts = self.workbook()
        with patch("patch_register_workbook.os.replace", side_effect=OSError("disk refused")):
            with self.assertRaisesRegex(OSError, "disk refused"):
                apply_updates(self.source, self.destination, [{"sheet": "Asset Register", "cell": "B2", "expected": 42, "value": 43}])
        self.assertEqual(list(self.root.iterdir()), [self.source])
        self.assert_source_unchanged(parts)


if __name__ == "__main__":
    unittest.main()
