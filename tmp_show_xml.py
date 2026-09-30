import re
from pathlib import Path

root = Path(r"D:\coding\ugift-data-analysis")
for name in ("tmp_lof_fig46.xml", "tmp_cap_fig46.xml", "tmp_toc_42.xml"):
    text = (root / name).read_text(encoding="utf-8")
    text = re.sub(r" xmlns:[^=]+=\"[^\"]+\"", "", text)
    text = re.sub(r" xmlns=\"[^\"]+\"", "", text)
    print("====", name, "====")
    print(text)
    print()
