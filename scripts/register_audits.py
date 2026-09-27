"""Compact, lossless storage for the register's source and quantity audit tables.

The gzip JSON archive stores ordered headers and ordered rows of strings, just
as CSV readers expose them. Quoted blanks, leading zeros, embedded newlines and
JSON evidence strings therefore survive migration without type inference.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import os
import tempfile
from collections.abc import Iterable, Iterator, Mapping, Sequence
from pathlib import Path
from typing import TypedDict

AUDIT_FILENAME = "asset-register-audits.json.gz"
LEGACY_FILENAMES = {
    "source": "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.source-audit.csv",
    "source_layout": "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.source-layout-audit.csv",
    "quantity": "ALL_UGIFT_ASSET_REGISTER_SK_TEMPLATE.quantity-audit.csv",
}


class AuditTable(TypedDict):
    fieldnames: list[str]
    rows: list[list[str]]


def _validate_table(table: object) -> None:
    if not isinstance(table, dict) or set(table) != {"fieldnames", "rows"}:
        raise ValueError("An audit table must contain fieldnames and rows")
    if not isinstance(table["fieldnames"], list) or not all(isinstance(value, str) for value in table["fieldnames"]):
        raise ValueError("Audit fieldnames must be a list of strings")
    if not isinstance(table["rows"], list) or not all(
        isinstance(row, list) and all(isinstance(value, str) for value in row)
        for row in table["rows"]
    ):
        raise ValueError("Audit rows must be lists of strings")


def _read_tables(path: Path) -> dict[str, AuditTable]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        archive = json.load(handle)
    if not isinstance(archive, dict) or archive.get("version") != 1 or not isinstance(archive.get("tables"), dict):
        raise ValueError(f"Unsupported audit archive: {path}")
    for table in archive["tables"].values():
        _validate_table(table)
    return archive["tables"]


def read_audit_table(path: Path, section: str) -> AuditTable:
    """Read an archive section, or a legacy CSV without changing its strings.

    If the standard archive does not exist yet, a matching legacy CSV beside
    it is accepted. An existing archive must contain the requested section.
    """
    path = Path(path)
    if not path.exists() and path.name == AUDIT_FILENAME and section in LEGACY_FILENAMES:
        path = path.with_name(LEGACY_FILENAMES[section])
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            return {"fieldnames": next(reader, []), "rows": list(reader)}
    tables = _read_tables(path)
    if section not in tables:
        raise ValueError(f"Audit archive {path} has no {section!r} section")
    return tables[section]


def read_audit_rows(path: Path, section: str) -> Iterator[dict[str, str]]:
    """Expose a table as records for consumers such as quantity validation."""
    table = read_audit_table(path, section)
    headers = table["fieldnames"]
    if len(set(headers)) != len(headers):
        raise ValueError("Audit records require unique fieldnames")
    for index, row in enumerate(table["rows"], start=2):
        if len(row) != len(headers):
            raise ValueError(f"Audit row {index} has {len(row)} values for {len(headers)} fieldnames")
        yield dict(zip(headers, row))


def make_audit_table(rows: Iterable[Mapping[str, object]], fieldnames: Sequence[str] | None = None) -> AuditTable:
    """Convert generated records to the same strings written by csv.DictWriter."""
    records = list(rows)
    headers = list(fieldnames) if fieldnames is not None else list(dict.fromkeys(key for row in records for key in row))
    if len(set(headers)) != len(headers):
        raise ValueError("Generated audit records require unique fieldnames")
    fields = set(headers)
    if any(set(row) - fields for row in records):
        raise ValueError("Audit records contain fields absent from fieldnames")
    table: AuditTable = {
        "fieldnames": headers,
        "rows": [["" if row.get(name) is None else str(row[name]) for name in headers] for row in records],
    }
    _validate_table(table)
    return table


def write_audit_tables(path: Path, tables: Mapping[str, AuditTable]) -> None:
    """Atomically update archive sections, preserving every other section."""
    path = Path(path)
    merged = _read_tables(path) if path.exists() else {}
    for section, table in tables.items():
        if not isinstance(section, str) or not section:
            raise ValueError("Audit section names must be nonempty strings")
        _validate_table(table)
        merged[section] = table
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w+b", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            with gzip.GzipFile(filename="", fileobj=handle, mode="wb", mtime=0) as compressed:
                with io.TextIOWrapper(compressed, encoding="utf-8", newline="\n") as text:
                    json.dump({"version": 1, "tables": merged}, text, ensure_ascii=False, separators=(",", ":"))
                    text.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_audit_table(path: Path, section: str, rows: Iterable[Mapping[str, object]], fieldnames: Sequence[str] | None = None) -> None:
    """Write generated records to one section without discarding other audits."""
    write_audit_tables(path, {section: make_audit_table(rows, fieldnames)})


def publish_audit_archive(staging: Path, destination: Path) -> None:
    """Promote a completed build only when all three current audits are present."""
    staging, destination = Path(staging), Path(destination)
    missing = set(LEGACY_FILENAMES) - _read_tables(staging).keys()
    if missing:
        raise ValueError(f"Incomplete audit build; missing sections: {', '.join(sorted(missing))}")
    staging.replace(destination)
