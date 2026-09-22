# -*- coding: utf-8 -*-
import ast
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

base = Path(r"d:/coding/apps/ugift/facility-registers/team-14")
zip_path = base / "WhatsApp Chat with TEAM 14 UGIFT (BUDDUDA,SORONKO,BULAMBULI).zip"
src_path = Path(r"d:/coding/apps/ugift/src/team14_media/__init__.py")
src = src_path.read_text(encoding="utf-8")

print("=== Duplicate PHOTOS keys (AST) ===")
mod = ast.parse(src)
photos = None
lg_docs = None
facility_docs = None
for node in mod.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "PHOTOS" and isinstance(node.value, ast.Dict):
                photos = node.value
            if isinstance(t, ast.Name) and t.id == "LG_DOCS":
                lg_docs = node.value
            if isinstance(t, ast.Name) and t.id == "FACILITY_DOCS":
                facility_docs = node.value

def dict_key_dups(node, label):
    if node is None:
        print(label, "not found")
        return
    seen = {}
    dups = []
    for k in node.keys:
        try:
            key = ast.literal_eval(k)
        except Exception:
            key = ast.dump(k)
        if key in seen:
            dups.append(key)
        seen[key] = True
    print(label, "keys", len(node.keys), "unique", len(seen), "dups", dups)

dict_key_dups(photos, "PHOTOS")
dict_key_dups(lg_docs, "LG_DOCS")
dict_key_dups(facility_docs, "FACILITY_DOCS")

# Nested IMG keys under duplicate facility
print("\n=== Nested IMG keys per facility in PHOTOS source ===")
if photos:
    for k, v in zip(photos.keys, photos.values):
        try:
            key = ast.literal_eval(k)
        except Exception:
            key = ast.dump(k)
        n = len(v.keys) if isinstance(v, ast.Dict) else "?"
        print(" ", key, n)

with zipfile.ZipFile(zip_path) as z:
    zip_files = set(Path(n).name for n in z.namelist() if not n.endswith("/"))

sys.path.insert(0, r"d:/coding/apps/ugift/src")
import team14_media as m

mapped = set()
for dist, docs in m.LG_DOCS.items():
    mapped.update(docs)
for files in m.PHOTOS.values():
    mapped.update(files)
for files in m.FACILITY_DOCS.values():
    mapped.update(files)
mapped.update(m.TEAM_DOCS)

skip = set()
for n in zip_files:
    low = n.lower()
    if low.endswith(".txt"):
        skip.add(n)
    if n.startswith("CAOs"):
        skip.add(n)
    if low.endswith(".pdf") and "local-government-report" in low:
        skip.add(n)

print("\n=== Zip files not in team14_media mappings ===")
unmapped = sorted(zip_files - mapped - skip)
for u in unmapped:
    print(" ", u)
print("unmapped", len(unmapped), "zip", len(zip_files), "mapped", len(mapped))

print("\n=== Mapped files missing from this zip ===")
for u in sorted(mapped - zip_files):
    print(" ", u)

expected = {}
for dist, docs in m.LG_DOCS.items():
    for fn, (new, why) in docs.items():
        expected[fn] = base / dist / "_district-documents" / new
for (dist, fac), files in m.PHOTOS.items():
    slug = fac.replace(" ", "-")
    for fn, (new, why) in files.items():
        expected[fn] = base / dist / slug / new
for (dist, fac), files in m.FACILITY_DOCS.items():
    slug = fac.replace(" ", "-")
    for fn, (new, why) in files.items():
        expected[fn] = base / dist / slug / new

print("\n=== Expected dest missing on disk ===")
missing = []
for fn, dest in expected.items():
    if not dest.exists():
        missing.append((fn, dest))
        print(" ", fn, "->", dest)
print("expected", len(expected), "missing", len(missing))

print("\n=== Duplicate destination names ===")
by_dest = defaultdict(list)
for fn, dest in expected.items():
    by_dest[str(dest)].append(fn)
for d, fns in by_dest.items():
    if len(fns) > 1:
        print(d, fns)

print("\n=== Duplicate NN or ref in facility folders ===")
for dist in ["Sironko", "Bulambuli", "Bududa"]:
    for fac in (base / dist).iterdir():
        if not fac.is_dir() or fac.name.startswith("_"):
            continue
        nns = defaultdict(list)
        refs = defaultdict(list)
        for f in list(fac.glob("*.jpg")) + list(fac.glob("*.pdf")):
            name = f.name
            nn = name.split("_")[0]
            nns[nn].append(name)
            if "_ref" in name:
                ref = name.rsplit("_ref", 1)[-1]
                refs[ref].append(name)
        for nn, files in nns.items():
            if len(files) > 1:
                print(" NN dup", fac.name, files)
        for ref, files in refs.items():
            if len(files) > 1:
                print(" REF dup", fac.name, files)

print("\n=== README ===")
for p in base.rglob("README*"):
    print(" ", p)

print("\n=== Sep3 refs on disk ===")
sep3 = [p for p in base.rglob("*") if p.is_file() and "ref20260903" in p.name]
print("count", len(sep3))
for p in sorted(sep3):
    print(" ", p.relative_to(base))

print("\n=== District voucher scans ===")
for p in (base / "Bududa" / "_district-documents").iterdir():
    print(" ", p.name)
