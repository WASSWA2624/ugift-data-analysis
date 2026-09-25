"""File queued source changes into raw-data-grouped without repeating work.

The first run records every snapshot file in changes.csv as added. A file
already present in _index.csv is marked applied and is not copied again.
"""

from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from track_source_changes import CHANGES, CHANGE_FIELDS, SNAPSHOT

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "raw-data-grouped" / "_index.csv"
APPLIED = ROOT / "raw-data-grouped" / "_change-tracker" / "applied.csv"
APPLIED_FIELDS = ("source", "path", "modified", "size", "applied", "note")
SOURCE_COLUMN = "source (in raw-data-ungrouped)"
DONE = {"placed", "duplicate", "extracted", "in-archive", "skipped"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        writer.writerows(rows)


def seed_queue(snapshot: list[dict[str, str]]) -> list[dict[str, str]]:
    existing = read_csv(CHANGES)
    seen = {(row.get("source"), row.get("path"), row.get("change")) for row in existing}
    detected = now()
    added = []
    for row in snapshot:
        key = (row["source"], row["path"], "added")
        if key in seen:
            continue
        added.append({
            "detected": detected,
            "change": "added",
            "source": row["source"],
            "path": row["path"],
            "modified": row["modified"],
            "size": row["size"],
        })
    if added:
        write_csv(CHANGES, CHANGE_FIELDS, existing + added)
    return read_csv(CHANGES)


def indexed_sources() -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for row in read_csv(INDEX):
        if row.get("status") not in DONE:
            continue
        root = row.get("source root") or ""
        relative = (row.get(SOURCE_COLUMN) or "").replace("\\", "/")
        found.add((root, relative))
        if "::" in relative:
            found.add((root, relative.split("::", 1)[0]))
    return found


def main() -> None:
    snapshot = read_csv(SNAPSHOT)
    if not snapshot:
        raise SystemExit(f"missing snapshot: {SNAPSHOT}")
    queue = seed_queue(snapshot)
    done = indexed_sources()
    already = {(row["source"], row["path"]) for row in read_csv(APPLIED)}
    applied_at = now()
    applied = read_csv(APPLIED)
    pending = []
    for row in queue:
        if row.get("change") not in {"added", "modified"}:
            continue
        key = (row.get("source") or "", row.get("path") or "")
        if key in already:
            continue
        if key in done:
            applied.append({
                "source": key[0],
                "path": key[1],
                "modified": row.get("modified") or "",
                "size": row.get("size") or "",
                "applied": applied_at,
                "note": "already filed in _index.csv",
            })
            already.add(key)
            continue
        pending.append(key)
    write_csv(APPLIED, APPLIED_FIELDS, applied)
    print(f"queue {len(queue):,}; applied {len(applied):,}; still to file {len(pending):,}")
    for source, path in pending:
        print(f"pending  {source}  {path}")


if __name__ == "__main__":
    main()
