"""Compare two internal PDF/page-image render sets for focused visual QA."""
import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


def digest(value):
    return hashlib.sha256(value).hexdigest()


def inventory(directory):
    pdfs = list(directory.glob("*.pdf"))
    if len(pdfs) != 1:
        raise ValueError(f"Expected one PDF in {directory}, found {len(pdfs)}")
    records = []
    for number, page in enumerate(PdfReader(pdfs[0]).pages, 1):
        text = re.sub(r"\s+", " ", page.extract_text() or "").strip()
        with Image.open(directory / f"page-{number}.png") as image:
            rgb = image.convert("RGB")
            pixel_hash = digest(str(rgb.size).encode() + rgb.tobytes())
        records.append({"page": number, "text_hash": digest(text.encode()),
                        "pixel_hash": pixel_hash, "text": text})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("previous", type=Path)
    parser.add_argument("current", type=Path)
    args = parser.parse_args()
    previous = inventory(args.previous)
    current = inventory(args.current)
    changes = []
    unchanged = []
    for index, new in enumerate(current):
        old = previous[index] if index < len(previous) else None
        if old and old["pixel_hash"] == new["pixel_hash"]:
            unchanged.append(new["page"])
        else:
            changes.append({"page": new["page"],
                            "text_changed": not old or old["text_hash"] != new["text_hash"],
                            "previous_text": old["text"] if old else None,
                            "current_text": new["text"]})
    result = {"previous_pages": len(previous), "current_pages": len(current),
              "pixel_identical_pages": unchanged, "changed_pages": changes,
              "deleted_pages": list(range(len(current) + 1, len(previous) + 1))}
    output = args.current / "page-comparison.json"
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"previous_pages": len(previous), "current_pages": len(current),
                      "pixel_identical_pages": unchanged,
                      "changed_pages": [item["page"] for item in changes],
                      "text_changed_pages": [item["page"] for item in changes if item["text_changed"]],
                      "comparison_file": str(output)}, indent=2))


if __name__ == "__main__":
    main()
