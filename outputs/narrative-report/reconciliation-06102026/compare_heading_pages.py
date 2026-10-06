"""Compare section/appendix heading locations in read-only Word PDF exports."""
import argparse
import json
import re
from pathlib import Path

from pypdf import PdfReader


def inventory(path):
    result = {}
    for number, page in enumerate(PdfReader(path).pages, 1):
        if number <= 4:  # Cover and table of contents are compared as page pixels.
            continue
        for line in (page.extract_text() or "").splitlines():
            line = re.sub(r"\s+", " ", line).strip()
            if re.match(r"^(?:\d+(?:\.\d+)+\s+[A-Za-z]|Appendix [A-Z]\s+[A-Z])", line):
                result.setdefault(line, []).append(number)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("previous", type=Path)
    parser.add_argument("current", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    previous, current = inventory(args.previous), inventory(args.current)
    changes = {
        name: {"previous": previous.get(name), "current": current.get(name)}
        for name in previous.keys() | current.keys()
        if previous.get(name) != current.get(name)
    }
    result = {"previous_heading_lines": len(previous),
              "current_heading_lines": len(current),
              "changed_heading_pages": changes,
              "current_heading_pages": current}
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items()
                      if key != "current_heading_pages"}, indent=2))


if __name__ == "__main__":
    main()
