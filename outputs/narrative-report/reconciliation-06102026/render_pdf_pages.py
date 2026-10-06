"""Rasterize a read-only Microsoft Word PDF export using bundled Poppler."""
import argparse
from pathlib import Path
from pdf2image import convert_from_path, pdfinfo_from_path

POPPLER = Path(r"C:\Users\WASSWA WILSON\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--dpi", type=int, default=144)
    args = parser.parse_args()
    args.output_directory.mkdir(parents=True, exist_ok=True)
    info = pdfinfo_from_path(str(args.input_pdf), poppler_path=str(POPPLER))
    print("PDF pages:", info["Pages"], flush=True)
    paths = convert_from_path(str(args.input_pdf), dpi=args.dpi, fmt="png", thread_count=4,
                              output_folder=str(args.output_directory), paths_only=True,
                              output_file="page", poppler_path=str(POPPLER))
    for file in paths:
        source = Path(file)
        page = int(source.stem.rsplit("-", 1)[-1])
        source.replace(args.output_directory / f"page-{page}.png")
    print(f"Rendered {len(paths)} pages to {args.output_directory}", flush=True)

if __name__ == "__main__":
    main()
