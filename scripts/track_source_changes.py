"""Record file changes under the two UgIFT source folders.

The snapshot is the last seen modified time of each file. A later run, or
--watch, appends only files whose modified time or size changed.
"""

from __future__ import annotations

import argparse
import csv
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("raw-data-ungrouped", "new-raw-data-221092026-1114")
TRACKER = ROOT / "raw-data-grouped" / "_change-tracker"
SNAPSHOT = TRACKER / "snapshot.csv"
CHANGES = TRACKER / "changes.csv"
SNAPSHOT_FIELDS = ("source", "path", "modified", "size")
CHANGE_FIELDS = ("detected", "change", "source", "path", "modified", "size")


def stamp(modified: float) -> str:
    return datetime.fromtimestamp(modified, timezone.utc).isoformat(timespec="seconds")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def skipped(relative: str) -> bool:
    name = relative.rsplit("/", 1)[-1]
    lowered = name.casefold()
    if name.startswith("~$") or name.startswith("._"):
        return True
    if lowered in {".ds_store", "desktop.ini", "thumbs.db"}:
        return True
    return relative.casefold().startswith("ugift-team-10-15/tmp/")


def scan() -> dict[tuple[str, str], tuple[str, int]]:
    found: dict[tuple[str, str], tuple[str, int]] = {}
    for source in SOURCES:
        root = ROOT / source
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if skipped(relative):
                continue
            stat = path.stat()
            found[(source, relative)] = (stamp(stat.st_mtime), stat.st_size)
    return found


def read_snapshot() -> dict[tuple[str, str], tuple[str, int]]:
    if not SNAPSHOT.is_file():
        return {}
    saved: dict[tuple[str, str], tuple[str, int]] = {}
    with SNAPSHOT.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            saved[(row["source"], row["path"])] = (row["modified"], int(row["size"]))
    return saved


def write_snapshot(current: dict[tuple[str, str], tuple[str, int]]) -> None:
    TRACKER.mkdir(parents=True, exist_ok=True)
    with SNAPSHOT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, SNAPSHOT_FIELDS)
        writer.writeheader()
        for (source, path) in sorted(current):
            modified, size = current[(source, path)]
            writer.writerow({"source": source, "path": path, "modified": modified, "size": size})


def append_changes(rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    TRACKER.mkdir(parents=True, exist_ok=True)
    new_file = not CHANGES.is_file()
    with CHANGES.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, CHANGE_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerows(rows)


def compare(current: dict[tuple[str, str], tuple[str, int]]) -> list[dict[str, object]]:
    previous = read_snapshot()
    detected = now()
    rows: list[dict[str, object]] = []
    for key, (modified, size) in sorted(current.items()):
        old = previous.get(key)
        if old is None:
            kind = "added"
        elif old != (modified, size):
            kind = "modified"
        else:
            continue
        rows.append({
            "detected": detected,
            "change": kind,
            "source": key[0],
            "path": key[1],
            "modified": modified,
            "size": size,
        })
    for key in sorted(set(previous) - set(current)):
        rows.append({
            "detected": detected,
            "change": "removed",
            "source": key[0],
            "path": key[1],
            "modified": "",
            "size": "",
        })
    return rows


def update() -> tuple[int, int]:
    current = scan()
    if not SNAPSHOT.is_file():
        write_snapshot(current)
        return len(current), 0
    rows = compare(current)
    append_changes(rows)
    write_snapshot(current)
    return len(current), len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true", help="Keep scanning and append each change.")
    parser.add_argument("--interval", type=int, default=30, help="Seconds between scans when watching.")
    args = parser.parse_args()
    files, changes = update()
    print(f"tracking {files:,} files; {changes:,} changes", flush=True)
    if not args.watch:
        return
    while True:
        time.sleep(max(args.interval, 5))
        files, changes = update()
        if changes:
            print(f"{now()} {changes:,} changes; {files:,} files", flush=True)


if __name__ == "__main__":
    main()
