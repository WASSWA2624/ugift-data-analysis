"""Reviewed recoveries for source layouts that mix asset names with locations.

These repairs run before return reconciliation and quantity expansion. They
preserve the source row, its recorded values and each separately stated group.
"""

from __future__ import annotations

import re
import zipfile
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

NSHWERE_SOURCE = "team-20/Kiruhura/Nshwere-HC-III/NSHWERE HC 3.docx"
NSHWERE_CONSOLIDATED_SOURCE = "team-20/_team-documents/TEAM 20 SSSs.xls"
NYAMARWA_SOURCE = "team-30/_team-documents/NYAMARWA SEED SCHOOL UGIFT ASSET VERIFICATION AND RECORDING TOOL KIT - FINAL.docx"
MONEY_FIELDS = ("recoverable", "cost", "acc_dep", "nbv", "ytd")


@dataclass(frozen=True)
class FurnitureGroup:
    row: int
    item: str
    quantity: int
    department: str
    description: str = ""
    broken: int = 0
    status: str | None = None
    remarks: str | None = None


@dataclass(frozen=True)
class FurnitureLayout:
    source_file: str
    table: str
    row_offset: int = 0
    laboratory_list_in_tag: bool = False

    def location(self, row: int) -> str:
        return f"{self.table} row {row + self.row_offset}"


NSHWERE_LAYOUTS = (
    FurnitureLayout(NSHWERE_SOURCE, "Table 11"),
    # The consolidated spreadsheet repeats the same 13 physical source rows.
    # Its laboratory list was entered in Tag Number rather than Description.
    FurnitureLayout(NSHWERE_CONSOLIDATED_SOURCE, "Sheet4", 494, True),
)


@dataclass(frozen=True)
class ReviewedUnitBlock:
    source: str
    first: int
    last: int
    primary: str
    primary_location: str
    primary_quantity: int
    primary_item: str
    unit_item: str
    primary_description: str
    unit_description: str


_SCHOOLS_7 = "team-07/_team-documents/SCHOOLS FOR TEAM SEVEN DTB.xlsx"
_SCHOOLS_8 = "team-08/_team-documents/TEAM EIGHT SCHOOLS DTB 2.xlsx"
_SCHOOLS_9 = "team-09/_team-documents/TEAM NINE SCHOOLS DTB.xlsx"
_AWEI = "team-07/Alebtong/Abia-HC-III/ABIA HC III.docx"
_ADEKNINO = "team-07/Dokolo/Abalang-HC-III/ABALANG HEALTH CENTER III $ ADEKNINO SEED.docx"
_OGORO = "team-07/Otuke/Alango-HC-III/ALANGO (1) HC 111.docx"
_BATTA = "team-07/Dokolo/Te-Tugu-HC-III/TE-TUGU HC III ..docx"
_ASAMUK = "team-08/Amuria/Asamuk-Seed-Secondary-School/asamuk,wera  ASSET VERIFICATION AND RECORDING TOOL KIT 222-1edit.docx"
_ASURET = "team-08/Soroti/Asuret-Seed-Secondary-School/ASURET SEED SS ASSET VERIFICATION AND RECORDING TOOL KIT 222.docx"
_KAGWARA = "team-08/Serere/Kagwara-HC-III/kagwara HC III and school-2.docx"
_KANGINIMA = "team-09/Butebo/Kanginima-Seed-Secondary-School/KANGINIMA SEED SECONDRY SCHOOL.docx"
_APAPAI = "team-09/Kalaki/Apapai-Seed-Secondary-School/apapai seed secondary school.docx"
_APERIKIRA = "team-09/Kaberamaido/Aperikira-Seed-Secondary-School/APERIKIRA SEED SCHOOL ASSET VERIFICATION.docx"

# Each range was checked against the original spreadsheet and the named
# primary toolkit. These are expanded statements of the same physical list,
# not a heuristic based on repeated names or a matching number of rows.
REVIEWED_UNIT_BLOCKS = (
    ReviewedUnitBlock(_SCHOOLS_7, 132, 254, _ADEKNINO, "Table 11 row 33", 122, "Laboratory stools(122)", "Laboratory stools(122)", "Wooden", "Wooden"),
    ReviewedUnitBlock(_SCHOOLS_7, 258, 273, _ADEKNINO, "Table 11 row 47", 15, "Bookshelves (15)", "Bookshelves (15)", "Metallic", "Metallic"),
    ReviewedUnitBlock(_SCHOOLS_7, 328, 448, _OGORO, "Table 11 row 2", 120, "School Desk 120", "School Desk 120", "Wooden", "Wooden"),
    ReviewedUnitBlock(_SCHOOLS_7, 450, 470, _OGORO, "Table 11 row 16", 20, "Office Chairs (20)", "Office Chairs (20)", "Metallic with cushion", "Metallic with cushion"),
    ReviewedUnitBlock(_SCHOOLS_7, 473, 665, _OGORO, "Table 11 row 19", 192, "Laboratory stools (192)", "Laboratory stools (192)", "Wooden and metallic in nature", "Wooden and metallic in nature"),
    ReviewedUnitBlock(_SCHOOLS_7, 672, 721, _OGORO, "Table 12 row 2", 48, "Desktop Computer (48)", "Desktop Computer (48)", "Digital S", "Digital"),
    ReviewedUnitBlock(_SCHOOLS_7, 914, 1180, _AWEI, "Table 11 row 5", 266, "OFFICE CHAIRS 266", "OFFICE CHAIRS 266", "WOODEN AND METALLIC BROWM IN COLOUR", "WOODEN AND METALLIC BROWM IN COLOUR"),
    ReviewedUnitBlock(_SCHOOLS_7, 1183, 1281, _AWEI, "Table 11 row 7", 98, "LABARATORY STOOLS 98", "LABARATORY STOOLS 98", "WOODEN IN NATURE", "WOODEN IN NATURE"),
    ReviewedUnitBlock(_SCHOOLS_7, 1284, 1303, _AWEI, "Table 11 row 10", 19, "BOOK SHELVES 19 19", "BOOK SHELVES 19", "2 BIG ONES 17 SMALL ONES", "2 BIG ONES"),
    ReviewedUnitBlock(_SCHOOLS_7, 2350, 2378, _BATTA, "Table 13 row 2", 28, "DESKTOP COMPUTERS (28)", "DESKTOP COMPUTERS (28)", "", ""),
    ReviewedUnitBlock(_SCHOOLS_7, 2384, 2413, _BATTA, "Table 13 row 6", 28, "UPS (28)", "UPS (28)", "MODEL APC 650YK", "MODEL APC 650YK"),
    ReviewedUnitBlock(_SCHOOLS_8, 5, 113, _ASAMUK, "Table 11 row 2", 107, "Desks 107", "Desks 107", "Metallic & wood", "Metallic & wood"),
    ReviewedUnitBlock(_SCHOOLS_8, 875, 1177, _ASURET, "Table 11 row 3", 302, "Chairs with hard seat 302", "Chairs with hard seat 302", "Single chair with hard seats", "Single chair with hard seats"),
    ReviewedUnitBlock(_SCHOOLS_8, 1598, 1618, _KAGWARA, "Table 11 row 2", 20, "office chair 20", "office chair", "metallic red cushion", "metallic red cushion"),
    ReviewedUnitBlock(_SCHOOLS_8, 1628, 1932, _KAGWARA, "Table 11 row 4", 305, "Chairs 305", "Chairs", "metallic & Hard wood", "metallic & Hard wood"),
    ReviewedUnitBlock(_SCHOOLS_9, 1233, 1266, _KANGINIMA, "Table 6 row 3", 32, "Chairs (32)", "Chairs", "Cushioned top, metallic stands", "Cushioned top, metallic stands"),
    ReviewedUnitBlock(_SCHOOLS_9, 1268, 1559, _KANGINIMA, "Table 6 row 4", 292, "Laboratory stools (292)", "Laboratory stools", "Round wooden top, metallic stand", "Round wooden top, metallic stand"),
    ReviewedUnitBlock(_SCHOOLS_9, 1609, 1637, _KANGINIMA, "Table 8 row 2", 28, "Monitors (28)", "Monitors", "", ""),
    ReviewedUnitBlock(_SCHOOLS_9, 1668, 1695, _KANGINIMA, "Table 8 row 4", 28, "Keyboards (28)", "Keyboards", "", ""),
    ReviewedUnitBlock(_SCHOOLS_9, 1697, 1724, _KANGINIMA, "Table 8 row 5", 28, "Mouse (28)", "Mouse", "", ""),
    ReviewedUnitBlock(_SCHOOLS_9, 2681, 2684, _APERIKIRA, "Table 7 row 43", 4, "Filter paper 4 boxes (400 pcs)", "Filter paper box (400 pcs)", "", ""),
    ReviewedUnitBlock(_SCHOOLS_9, 3656, 3677, _APAPAI, "Table 7 row 2", 21, "Monitors (21)", "Monitors", "Lenovo", "Lenovo"),
    ReviewedUnitBlock(_SCHOOLS_9, 3682, 3702, _APAPAI, "Table 7 row 3", 21, "CPU (21)", "CPU", "Lenovo", "Lenovo"),
)


# Verified against the original DOCX table and its XML. This table is headed
# SCHOOL FURNITURE for Nyakashashara Seed School; the first column mostly holds
# rooms, while the description holds the furniture and its physical quantities.
NSHWERE_GROUPS: dict[int, tuple[FurnitureGroup, ...]] = {
    2: (FurnitureGroup(2, "Desk", 12, "Classroom 1"), FurnitureGroup(2, "Chair", 12, "Classroom 1"),
        FurnitureGroup(2, "Stool", 9, "Classroom 1", broken=2)),
    3: (FurnitureGroup(3, "Desk", 7, "Classroom 2"), FurnitureGroup(3, "Stool", 8, "Classroom 2", broken=1),
        FurnitureGroup(3, "Chair", 9, "Classroom 2", broken=2)),
    4: (FurnitureGroup(4, "Table", 1, "Block 2"), FurnitureGroup(4, "Desk", 17, "Block 2"),
        FurnitureGroup(4, "Chair", 12, "Block 2"), FurnitureGroup(4, "Stool", 1, "Block 2")),
    5: (FurnitureGroup(5, "Desk", 14, "Block 2"), FurnitureGroup(5, "Table", 1, "Block 2")),
    7: (FurnitureGroup(7, "Table", 14, "1st laboratory"), FurnitureGroup(7, "Stool", 64, "1st laboratory"),
        FurnitureGroup(7, "Stool", 64, "2nd laboratory"), FurnitureGroup(7, "Chair", 2, "2nd laboratory"),
        FurnitureGroup(7, "Table", 13, "2nd laboratory")),
    8: (FurnitureGroup(8, "Table", 13, "Staff room"), FurnitureGroup(8, "Chair", 35, "Staff room")),
    10: (FurnitureGroup(10, "Table", 1, "Askaris gate"), FurnitureGroup(10, "Chair", 1, "Askaris gate"),
         FurnitureGroup(10, "Stool", 1, "Askaris gate")),
    11: (FurnitureGroup(11, "Desk", 64, "Multipurpose hall"), FurnitureGroup(11, "Chair", 52, "Multipurpose hall")),
    12: (FurnitureGroup(12, "Table", 6, "Block 3"), FurnitureGroup(12, "Chair", 12, "Block 3")),
    13: (FurnitureGroup(13, "Desk", 2, "Classroom 2"), FurnitureGroup(13, "Chair", 19, "Classroom 2"),
         FurnitureGroup(13, "Stool", 3, "Classroom 2")),
    # The old parser joined these three physical source rows onto row 14.
    14: (FurnitureGroup(14, "Water tank", 1, "Multipurpose hall", "5000 litres water tank", status="function", remarks="In use"),
         FurnitureGroup(15, "Water tank", 1, "Classroom", "10000 litres water tank", status="", remarks=""),
         FurnitureGroup(16, "Water tank", 1, "Administration block", "5000 litres Crescent tank", status="", remarks="the tap needs replacement")),
}

NSHWERE_DESCRIPTIONS = {
    2: "Desks 12,chairs 12,stools 09",
    3: "Desks 07,stool 08,chairs 09",
    4: "1 table, desks 17,chairs 12,stools 1",
    5: "Desks 14,chaistool 1 table",
    7: "Tables 14,stools 64,stools 64,chairs 2,tables 13",
    8: "Tables 13,chairs 35",
    10: "1 table,1 chair,1 stool",
    11: "Multi purpose hall 64, chairs 52",
    12: "Tables 06,chairs 12",
    13: "Desks 02,chairs19,stools 03",
    14: "1 tank(5000litres 1 tank (10000litres 5000litres cresent tank",
}


def _normalized(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def repair_reviewed_unit_blocks(parsed: dict[str, list[Any]]) -> list[dict[str, Any]]:
    """Keep source-proven physical rows once and fold their primary statement.

    Only the reviewed source coordinates and matching primary facts qualify.
    An ordinary first row is never discarded as a guessed group header, even
    where the consolidated unit count differs from the primary printed total.
    """
    plans = []
    for block in REVIEWED_UNIT_BLOCKS:
        if block.source not in parsed or block.primary not in parsed:
            continue
        locations = {f"Sheet1 row {number}" for number in range(block.first, block.last + 1)}
        units = [asset for asset in parsed[block.source] if asset.source_location in locations]
        if units and all(asset.extras.get("reviewed_unit_block") for asset in units):
            continue
        if len(units) != len(locations) or {asset.source_location for asset in units} != locations:
            raise ValueError(f"Reviewed unit block changed: {block.source} rows {block.first}-{block.last}")
        primaries = [asset for asset in parsed[block.primary] if asset.source_location == block.primary_location]
        if len(primaries) != 1:
            raise ValueError(f"Reviewed primary row missing or repeated: {block.primary} {block.primary_location}")
        primary = primaries[0]
        if (_normalized(primary.item) != _normalized(block.primary_item)
                or _normalized(primary.description) != _normalized(block.primary_description)):
            raise ValueError(f"Reviewed primary asset facts changed: {block.primary} {block.primary_location}")
        place = (_normalized(primary.lg), _normalized(primary.facility), primary.facility_type)
        if any((_normalized(asset.lg), _normalized(asset.facility), asset.facility_type) != place
               or _normalized(asset.item) != _normalized(block.unit_item)
               or _normalized(asset.description) != _normalized(block.unit_description) for asset in units):
            raise ValueError(f"Reviewed unit identity changed: {block.source} rows {block.first}-{block.last}")
        # These reviewed lists contain no money. A new priced aggregate needs
        # reconciliation of its amounts before it can be folded into units.
        if any(getattr(asset, name) not in (None, "") for asset in [primary, *units] for name in MONEY_FIELDS):
            raise ValueError(f"Reviewed unit block now has monetary facts: {block.source} rows {block.first}-{block.last}")
        plans.append((block, units, primary))

    audit = []
    for block, units, primary in plans:
        location = f"Sheet1 rows {block.first}-{block.last}"
        count = len(units)
        discrepancy = (
            f" Source count conflict: the primary states {block.primary_quantity}, while the consolidation has {count} ordinary unit rows. "
            "No first row is independently identified as a group header; all individual rows are retained."
            if count != block.primary_quantity else ""
        )
        proof = (
            f"Reviewed original {block.primary} ({block.primary_location}) states one group of {block.primary_quantity}: "
            f"'{primary.item}', description '{primary.description}', status '{primary.status}', remarks '{primary.remarks}', tag '{primary.tag}'. "
            f"The same facility and asset facts appear as an expanded unit list in {block.source} ({location}). "
            f"Each of its {count} physical rows is retained once; the repeated aggregate statement from the primary return is folded in."
            + discrepancy
            + " Individual Functional/Broken/Spoilt/Spoiled remarks control only the stated unit's status. "
            "Other repeated aggregate condition or loss wording is preserved without assigning unidentified lost units."
        )
        primary_snapshot = {key: deepcopy(value) for key, value in vars(primary).items() if key != "extras"}
        primary_snapshot["source_cells"] = deepcopy(primary.extras.get("source_cells", []))
        for asset in units:
            asset.extras["reviewed_unit_block"] = {
                "consolidated_source": block.source, "consolidated_rows": location,
                "primary_source": block.primary, "primary_location": block.primary_location,
                "primary_quantity": block.primary_quantity, "retained_unit_rows": count,
                "primary_facts": deepcopy(primary_snapshot),
                "original_status": asset.status, "original_explicit_qty": asset.explicit_qty,
            }
            asset.extras["proven_unit_row"] = True
            asset.extras["source_group_locations"] = [asset.source_location]
            asset.extras["quantity_layout_evidence"] = proof
            asset.extras["quantity_evidence"] = [(1, "reviewed primary statement and expanded physical unit layout")]
            asset.explicit_qty = 1
            # Preserve original wording in Remarks. Only a standalone unit
            # condition overrides the repeated aggregate status on that row.
            if _normalized(asset.remarks) in {"functional", "broken", "spoilt", "spoiled"}:
                asset.status = asset.remarks
            # The same source statement may supply an omitted recorded fact,
            # but never an aggregate tag, description or condition for a unit.
            for name in ("life", "purchase", "service"):
                if getattr(asset, name) in (None, "") and getattr(primary, name) not in (None, ""):
                    setattr(asset, name, deepcopy(getattr(primary, name)))
            asset.extras.setdefault("filled_from", set()).add(block.primary)
        parsed[block.primary][:] = [asset for asset in parsed[block.primary] if asset is not primary]
        audit.append({
            "source_file": block.source,
            "source_location": location,
            "status": "reviewed_unit_records",
            "source_records": count + 1,
            "named_groups": count,
            "physical_assets": count,
            "counts_by_item": {block.unit_item: count},
            "reason": proof,
        })
    return audit


def repair_nyamarwa_air_conditioner(assets: list[Any]) -> list[dict[str, Any]]:
    """Restore the reviewed name/quantity pair appended to the video recorder."""
    source_assets = [asset for asset in assets if asset.source_file == NYAMARWA_SOURCE]
    if not source_assets or any(asset.extras.get("nyamarwa_air_conditioner_recovered") for asset in source_assets):
        return []
    recorders = [asset for asset in source_assets if asset.source_location == "Table 12 row 21"]
    if (len(recorders) != 1 or _normalized(recorders[0].item) != "video recorder"
            or _normalized(recorders[0].description) != "air conditoner 1 set"):
        raise ValueError("Nyamarwa air-conditioner layout changed; review Table 12 rows 21-25 again")
    if any(asset.source_location in {"Table 12 row 24", "Table 12 row 25"} for asset in source_assets):
        raise ValueError("Nyamarwa name/quantity continuation was already emitted as a separate row")

    # Unlike a named asset with its own numeric suffix, '1 SET' is a separate
    # quantity row. Check the original cells before assigning it to its name.
    path = Path(__file__).resolve().parents[1] / "raw-data-grouped" / NYAMARWA_SOURCE
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(path) as archive:
        body = ElementTree.fromstring(archive.read("word/document.xml")).find(f"{namespace}body")
    rows = body.findall(f"{namespace}tbl")[11].findall(f"{namespace}tr")
    original_rows = {
        number: ["".join(node.text or "" for node in cell.iter(f"{namespace}t"))
                 for cell in rows[number - 1].findall(f"{namespace}tc")]
        for number in (21, 24, 25)
    }
    for number, expected in ((21, "VIDEO RECORDER"), (24, "AIR CONDITONER"), (25, "1 SET")):
        cells = original_rows[number]
        if not cells or _normalized(cells[0]) != _normalized(expected) or any(_normalized(cell) for cell in cells[1:]):
            raise ValueError(f"Nyamarwa Table 12 row {number} changed; review the original cells again")

    recorder = recorders[0]
    recovered = type(recorder)()
    for name in ("lg", "facility", "facility_type", "source_file"):
        setattr(recovered, name, getattr(recorder, name))
    recovered.item = "Air conditioner"
    recovered.description = original_rows[24][0]
    recovered.explicit_qty = 1
    recovered.source_location = "Table 12 rows 24-25"
    recovered.extras = {
        key: deepcopy(recorder.extras[key]) for key in ("lg_key", "facility_key", "central", "facility_raw")
        if key in recorder.extras
    }
    proof = (
        "Original Table 12 row 24 names AIR CONDITONER and row 25 states 1 SET. "
        "These two rows describe one air conditioner; the parser had appended them to VIDEO RECORDER row 21."
    )
    recovered.extras.update({
        "nyamarwa_air_conditioner_recovered": True,
        "recorded_group_total": 1,
        "source_group_locations": ["Table 12 row 24", "Table 12 row 25"],
        "quantity_layout_evidence": proof,
        "source_cells": [original_rows[24][0], original_rows[25][0]],
        "source_layout_original": {
            "source_file": NYAMARWA_SOURCE,
            "source_rows": {f"Table 12 row {number}": original_rows[number] for number in (24, 25)},
        },
    })
    recorder.extras["nyamarwa_air_conditioner_fragment"] = recorder.description
    recorder.description = ""
    assets[:] = [record for asset in assets for record in ([asset, recovered] if asset is recorder else [asset])]
    return [{
        "source_file": NYAMARWA_SOURCE,
        "source_location": "Table 12 rows 24-25",
        "status": "recovered",
        "source_records": 2,
        "named_groups": 1,
        "physical_assets": 1,
        "counts_by_item": {"Air conditioner": 1},
        "reason": proof,
    }]


def repair_nshwere_furniture(assets: list[Any]) -> list[dict[str, Any]]:
    """Replace reviewed mixed-list records in place; return an audit summary.

    The repair is idempotent and restricted to the exact source/table and
    reviewed wording in the toolkit and its consolidated copy. A changed
    source layout raises rather than silently applying a stale map. Matching
    groups in the two returns reconcile through the normal facility union.
    """
    audit = []
    for layout in NSHWERE_LAYOUTS:
        audit.extend(_repair_nshwere_return(assets, layout))
    return audit


def _repair_nshwere_return(assets: list[Any], layout: FurnitureLayout) -> list[dict[str, Any]]:
    selected: dict[int, Any] = {}
    source_rows = {layout.location(row): row for row in NSHWERE_GROUPS}
    for asset in assets:
        if asset.source_file != layout.source_file or asset.extras.get("nshwere_furniture_recovered"):
            continue
        row = source_rows.get(asset.source_location)
        if row is not None:
            if row in selected:
                raise ValueError(f"{layout.source_file}: {layout.location(row)} appears twice before layout recovery")
            selected[row] = asset
    if not selected:
        return []
    if set(selected) != set(NSHWERE_GROUPS):
        raise ValueError(f"{layout.source_file}: Nshwere furniture layout changed; the reviewed source rows are incomplete")
    for row, asset in selected.items():
        text = asset.description
        if row == 7 and layout.laboratory_list_in_tag:
            if _normalized(asset.description):
                raise ValueError(f"{layout.source_file}: laboratory column layout changed; review it again")
            text = asset.tag
        if _normalized(text) != _normalized(NSHWERE_DESCRIPTIONS[row]):
            raise ValueError(f"{layout.source_file}: {layout.location(row)} wording changed; review the mixed furniture list again")

    replacements: dict[int, list[Any]] = {}
    totals: Counter[str] = Counter()
    for row, original in selected.items():
        groups = NSHWERE_GROUPS[row]
        total = sum(group.quantity for group in groups)
        recovered = []
        for group in groups:
            asset = deepcopy(original)
            asset.item = group.item
            asset.department = group.department
            asset.description = group.description or group.item
            asset.explicit_qty = group.quantity
            asset.source_location = f"{layout.location(group.row)} ({group.department}; {group.item})"
            if row == 7 and layout.laboratory_list_in_tag:
                asset.tag = ""
            if group.status is not None:
                asset.status = group.status
            if group.remarks is not None:
                asset.remarks = group.remarks
            if group.broken:
                asset.status = f"{group.quantity - group.broken} functional and {group.broken} broken"
            for field in MONEY_FIELDS:
                amount = getattr(original, field)
                if isinstance(amount, (int, float)) and not isinstance(amount, bool):
                    # A monetary figure on a mixed line belongs to that whole
                    # physical group, not separately to every named subgroup.
                    if field != "cost" or not original.extras.get("unit_cost"):
                        setattr(asset, field, amount * group.quantity / total)
            for flag in ("has_unit_rows", "unit_row", "proven_unit_row", "unit_item", "quantity_evidence", "unit"):
                asset.extras.pop(flag, None)
            asset.extras["source_layout_original"] = {
                key: deepcopy(value) for key, value in vars(original).items() if key != "extras"
            }
            asset.extras["source_layout_original"]["source_cells"] = deepcopy(original.extras.get("source_cells", []))
            asset.extras["nshwere_furniture_recovered"] = True
            asset.extras["recorded_group_total"] = group.quantity
            asset.extras["source_group_locations"] = [layout.location(group.row)]
            asset.extras["quantity_layout_evidence"] = (
                f"Reviewed Nshwere return {layout.location(group.row)} names {group.quantity} {group.item} assets "
                f"at {group.department}; the item-column room label is their location. "
                "Separately stated laboratory stool groups are retained independently."
            )
            # Keep the original mixed list in the audit metadata above. Reusing
            # it as each subgroup's count evidence would expand every subgroup
            # by another item's count (for example 64 tables instead of 14).
            asset.extras["source_cells"] = [asset.item, asset.department, asset.description,
                                             f"Quantity: {group.quantity}", asset.status, asset.remarks]
            recovered.append(asset)
            totals[group.item] += group.quantity
        replacements[id(original)] = recovered
    assets[:] = [record for asset in assets for record in replacements.get(id(asset), [asset])]
    return [{
        "source_file": layout.source_file,
        "source_location": f"{layout.table} rows {2 + layout.row_offset}-{16 + layout.row_offset}",
        "status": "recovered",
        "source_records": len(selected),
        "named_groups": sum(len(records) for records in replacements.values()),
        "physical_assets": sum(totals.values()),
        "counts_by_item": dict(totals),
        "reason": (
            "Verified mixed furniture lists name 469 furniture units and 3 water tanks. "
            "Room labels are departments; the two 64-stool laboratory groups remain separate. "
            "The unquantified 'chaistool' fragment is retained as unclear source wording without an invented asset. "
            f"{layout.location(12)} and {layout.location(13)} do not identify which furniture item was broken. "
            "The toolkit and consolidated spreadsheet repeat the same groups and reconcile as one return. "
            + ("The laboratory list was recorded under Tag Number; it is retained in original metadata, not treated as an asset tag."
               if layout.laboratory_list_in_tag else "")
        ),
    }]
