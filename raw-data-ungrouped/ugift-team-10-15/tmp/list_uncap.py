from pathlib import Path
from collections import defaultdict

root = Path(r"d:/coding/apps/ugift/facility-registers/team-14")
out_dir = Path(r"d:/coding/apps/ugift/tmp/t14_uncap")
out_dir.mkdir(parents=True, exist_ok=True)
by = defaultdict(list)
for p in sorted(root.rglob("*.jpg")):
    if "uncaptioned" in p.name.lower():
        rel = p.parent.relative_to(root).as_posix()
        by[rel].append(str(p))
for k, v in sorted(by.items(), key=lambda x: -len(x[1])):
    slug = k.replace("/", "__")
    (out_dir / f"{slug}.txt").write_text("\n".join(v), encoding="utf-8")
    print(f"{k}\t{len(v)}")
print("wrote", len(by), "lists")
