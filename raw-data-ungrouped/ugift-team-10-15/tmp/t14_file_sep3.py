# -*- coding: utf-8 -*-
"""File Team 14 Sept 3 WhatsApp media into facility folders and emit PHOTOS map."""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(r"d:\coding\apps\ugift")
WA = ROOT / "facility-registers/team-14/_wa_unpack"
BASE = ROOT / "facility-registers/team-14"
TMP = ROOT / "tmp"

# (district, facility, name_map_file, start_nn, special moves)
BATCHES = [
    ("Bulambuli", "Bwikhonge HC III", "t14_sep3_names_bwikhonge.json", 54, None),
    ("Bududa", "Bubungi HC III", "t14_sep3_names_bubungi.json", 80, None),
    ("Bududa", "Nakatsi Seed Secondary School", "t14_sep3_names_nakatsi_toolkit.json", 89,
     {"IMG-20260903-WA0052.jpg": ("Bududa", "Bubungi HC III")}),  # misfiled Bubungi challenges
    ("Sironko", "Simu Pondo HC III", "t14_sep3_names_simupondo.json", 48, None),
    ("Bulambuli", "Bunangaka HC III", "t14_sep3_names_bunangaka.json", 59, None),
    ("Sironko", "Bundege HC III", "t14_sep3_names_bundege.json", 27, None),
]

LAB_MAP = json.loads((TMP / "t14_sep3_names_nakatsi_lab.json").read_text(encoding="utf-8"))


def slug_folder(facility):
    return facility.replace(" ", "-").replace("'", "")


def ref_of(img_name):
    m = re.match(r"IMG-(\d{8})-WA(\d+)\.jpg$", img_name, re.I)
    return "ref%s-%s" % (m.group(1), m.group(2).zfill(4))


def folder_for(district, facility):
    return BASE / district / slug_folder(facility)


def next_nn(folder, start):
    nums = []
    for p in folder.glob("*.jpg"):
        m = re.match(r"^(\d+)_", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max([start - 1] + nums) + 1


def main():
    photos = {}  # (district, facility) -> {IMG: (newname, caption)}
    filed = []
    skipped = []

    # Bubungi challenges from Nakatsi batch gets its own NN in Bubungi
    bubungi_extra_nn = None

    for district, facility, map_name, start_nn, moves in BATCHES:
        mapping = json.loads((TMP / map_name).read_text(encoding="utf-8"))
        dest = folder_for(district, facility)
        dest.mkdir(parents=True, exist_ok=True)
        nn = next_nn(dest, start_nn)
        key = (district, facility)
        photos.setdefault(key, {})

        for img, slug_or_full in mapping.items():
            # lab map already has full filenames
            if map_name.endswith("nakatsi_lab.json"):
                continue
            if moves and img in moves:
                # file under the correct facility instead
                md, mf = moves[img]
                mdest = folder_for(md, mf)
                mdest.mkdir(parents=True, exist_ok=True)
                if bubungi_extra_nn is None:
                    bubungi_extra_nn = next_nn(mdest, 90)
                # use next after bubungi toolkit pages — compute after bubungi batch
                # defer: store for later
                photos.setdefault((md, mf), {})
                photos[(md, mf)][img] = (
                    "DEFER_BUBUNGI_CHALLENGES",
                    "Handwritten challenges and recommendations for Bubungi HC III, "
                    "sent in the Nakatsi toolkit batch.",
                )
                continue

            slug = slug_or_full
            if slug.startswith(tuple("0123456789")):
                # already a full name
                newname = slug
            else:
                newname = "%02d_%s_%s.jpg" % (nn, slug, ref_of(img))
                nn += 1

            src = WA / img
            if not src.exists():
                skipped.append(img)
                continue
            out = dest / newname
            if out.exists():
                # already filed
                photos[key][img] = (newname, "Already on file.")
                continue
            # duplicate content check by ref
            ref = ref_of(img)
            existing = list(dest.glob("*%s*" % ref))
            if existing:
                photos[key][img] = (existing[0].name, "Ref already filed.")
                continue
            shutil.copy2(src, out)
            filed.append(str(out.relative_to(BASE)))
            photos[key][img] = (
                newname,
                "Hand-filled toolkit page for %s." % facility,
            )

    # Nakatsi lab inventory photos
    lab_key = ("Bududa", "Nakatsi Seed Secondary School")
    lab_dest = folder_for(*lab_key)
    photos.setdefault(lab_key, {})
    for img, newname in LAB_MAP.items():
        src = WA / img
        out = lab_dest / newname
        if out.exists() or list(lab_dest.glob("*%s*" % ref_of(img))):
            photos[lab_key][img] = (newname, "Already on file.")
            continue
        shutil.copy2(src, out)
        filed.append(str(out.relative_to(BASE)))
        photos[lab_key][img] = (
            newname,
            "Physics Laboratory Stock Taking and Inventory 2025 page for "
            "Nakatsi Seed Secondary School.",
        )

    # Deferred Bubungi challenges (WA0052)
    img = "IMG-20260903-WA0052.jpg"
    src = WA / img
    mdest = folder_for("Bududa", "Bubungi HC III")
    nn = next_nn(mdest, 90)
    newname = "%02d_hand-filled-toolkit-challenges-and-recommendations_%s.jpg" % (
        nn, ref_of(img))
    if src.exists() and not list(mdest.glob("*%s*" % ref_of(img))):
        shutil.copy2(src, mdest / newname)
        filed.append(str((mdest / newname).relative_to(BASE)))
        photos[("Bududa", "Bubungi HC III")][img] = (
            newname,
            "Challenges and recommendations page for Bubungi HC III, sent with "
            "the Nakatsi toolkit batch.",
        )

    # Scanned Bududa issue vouchers -> district documents as page images
    scan_dir = TMP / "t14_sep3_toolkits/scanned_pages"
    lg = BASE / "Bududa" / "_district-documents"
    lg.mkdir(parents=True, exist_ok=True)
    scan_names = [
        ("page-01.png", "05_issue-voucher-521-bubungi-hc-iii_ref20260902-scan01.jpg"),
        ("page-02.png", "06_issue-voucher-522-bupoto-hc-iii_ref20260902-scan02.jpg"),
        ("page-03.png", "07_issue-voucher-523-bubungi-hc-iii_ref20260902-scan03.jpg"),
        ("page-04.png", "08_goods-voucher-634-bukalasi-hc-iii_ref20260902-scan04.jpg"),
    ]
    from PIL import Image
    lg_docs = {}
    for src_name, newname in scan_names:
        src = scan_dir / src_name
        out = lg / newname
        if src.exists() and not out.exists():
            Image.open(src).convert("RGB").save(out, quality=90)
            filed.append(str(out.relative_to(BASE)))
        lg_docs[src_name] = newname

    # Also keep the multipage PDF once at district level under a stable name
    pdf_src = WA / "Scanned_20260902_152229.pdf"
    pdf_out = lg / "Bududa-issue-and-goods-vouchers-scanned.pdf"
    if pdf_src.exists() and not pdf_out.exists():
        shutil.copy2(pdf_src, pdf_out)
        filed.append(str(pdf_out.relative_to(BASE)))

    # Emit photos map for team14_media
    out_map = {}
    for (district, facility), files in photos.items():
        out_map["%s|%s" % (district, facility)] = files
    (TMP / "t14_sep3_filed_photos.json").write_text(
        json.dumps({"filed": filed, "photos": out_map, "lg_docs": lg_docs},
                   indent=2, ensure_ascii=False),
        encoding="utf-8")
    print("filed", len(filed))
    for f in filed:
        print(" ", f)
    print("skipped", skipped)


if __name__ == "__main__":
    main()
