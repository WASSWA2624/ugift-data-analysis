"""Reviewed recoveries for source layouts that mix asset names with locations.

These repairs run before return reconciliation and quantity expansion. They
preserve the source row, its recorded values and each separately stated group.
"""

from __future__ import annotations

import re
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

NSHWERE_SOURCE = "team-20/Kiruhura/Nshwere-HC-III/NSHWERE HC 3.docx"
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


def repair_nshwere_furniture(assets: list[Any]) -> list[dict[str, Any]]:
    """Replace reviewed mixed-list records in place; return an audit summary.

    The repair is idempotent and restricted to the exact source/table and
    reviewed wording. A changed source layout raises rather than silently
    applying a stale map. No outside file, facility or asset is changed.
    """
    selected: dict[int, Any] = {}
    for asset in assets:
        if asset.source_file != NSHWERE_SOURCE or asset.extras.get("nshwere_furniture_recovered"):
            continue
        match = re.fullmatch(r"Table 11 row (\d+)", asset.source_location)
        if match and int(match.group(1)) in NSHWERE_GROUPS:
            row = int(match.group(1))
            if row in selected:
                raise ValueError(f"Nshwere Table 11 row {row} appears twice before layout recovery")
            selected[row] = asset
    if not selected:
        return []
    if set(selected) != set(NSHWERE_GROUPS):
        raise ValueError("Nshwere furniture layout changed: the reviewed source rows are incomplete")
    for row, asset in selected.items():
        if _normalized(asset.description) != _normalized(NSHWERE_DESCRIPTIONS[row]):
            raise ValueError(f"Nshwere Table 11 row {row} wording changed; review the mixed furniture list again")

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
            asset.source_location = f"Table 11 row {group.row} ({group.department}; {group.item})"
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
                key: deepcopy(getattr(original, key))
                for key in ("item", "department", "description", "status", "remarks", "source_location", *MONEY_FIELDS)
            }
            asset.extras["source_layout_original"]["source_cells"] = deepcopy(original.extras.get("source_cells", []))
            asset.extras["nshwere_furniture_recovered"] = True
            asset.extras["recorded_group_total"] = group.quantity
            asset.extras["source_group_locations"] = [f"Table 11 row {group.row}"]
            asset.extras["quantity_layout_evidence"] = (
                f"Original Nshwere toolkit Table 11 row {group.row} names {group.quantity} {group.item} assets "
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
        "source_file": NSHWERE_SOURCE,
        "source_location": "Table 11 rows 2-16",
        "status": "recovered",
        "source_records": len(selected),
        "named_groups": sum(len(records) for records in replacements.values()),
        "physical_assets": sum(totals.values()),
        "counts_by_item": dict(totals),
        "reason": (
            "Verified mixed furniture lists name 469 furniture units and 3 water tanks. "
            "Room labels are departments; the two 64-stool laboratory groups remain separate. "
            "The unquantified 'chaistool' fragment is retained as unclear source wording without an invented asset. "
            "Rows 12 and 13 do not identify which furniture item was broken."
        ),
    }]
