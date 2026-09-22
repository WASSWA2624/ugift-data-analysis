# -*- coding: utf-8 -*-
"""One-shot generator for src/team12_media/photos.py from the 31 August chat."""
import os, re, textwrap

CHAT = r"d:\coding\apps\ugift\tmp\team12-wa\WhatsApp Chat with UGIFT TEAM 12 (Mbale,Budaka,Butaleja, Kibuku).txt"
OUT = r"d:\coding\apps\ugift\src\team12_media\photos.py"

# Already filed as toolkit / district pages (or repeats of those).
from team12_media.toolkits import FACILITY_FILES, LG_DOCS, REPEATS  # noqa: E402

taken = set(REPEATS)
for d in LG_DOCS.values():
    taken.update(d)
for facs in FACILITY_FILES.values():
    for files in facs.values():
        taken.update(files)

SKIP = {"IMG-20260831-WA1064.jpg"}  # selfie; no facility, no asset

def nn(i):
    return "%02d" % i if i < 100 else "%03d" % i

def ref(fn):
    m = re.search(r"WA(\d{4})", fn)
    return m.group(1) if m else fn

def burst(files, start, why, special=None):
    special = special or {}
    out = {}
    i = start
    for src in files:
        if src in taken or src in SKIP:
            continue
        stem, desc = special.get(src, (None, None))
        if stem is None:
            stem = "uncaptioned-asset"
            d = why
        else:
            d = why + " " + desc
        ext = src.rsplit(".", 1)[-1].lower()
        out[src] = ("%s_%s_ref%s.%s" % (nn(i), stem, ref(src), ext), d)
        i += 1
    return out, i

# Parse 31 Aug attachments in chat order, tagged by the last caption.
files_by_caption = []
current = None
bucket = []
pat = re.compile(r"((?:IMG|VID)-20260831-WA\d{4}\.\w+)")
with open(CHAT, encoding="utf-8") as f:
    lines = f.readlines()

# Walk after the last 8/28 line
on = False
caption_hint = None
pending = []
for line in lines:
    if line.startswith("8/31/26"):
        on = True
    if not on:
        continue
    m = pat.search(line)
    # caption text on the same line or following
    rest = ""
    if m:
        rest = line[m.end():].strip()
        pending.append(m.group(1))
        if rest and rest != "(file attached)":
            caption_hint = rest.replace("(file attached)", "").strip()
    else:
        text = re.sub(r"^8/31/26, \d+:\d+ - Team 12 [^:]+:\s*", "", line).strip()
        if text and not text.startswith("IMG-") and not text.startswith("VID-"):
            caption_hint = text

# Better: split the chat into captioned batches from known phrases.
text = open(CHAT, encoding="utf-8").read()
# isolate 31 Aug
idx = text.find("8/31/26, 18:34")
chunk = text[idx:]

def grab(after_phrase, until_phrases):
    i = chunk.find(after_phrase)
    if i < 0:
        return []
    end = len(chunk)
    for u in until_phrases:
        j = chunk.find(u, i + len(after_phrase))
        if j > i:
            end = min(end, j)
    return pat.findall(chunk[i:end])

mazimasa = grab("These are for Mazimasa HCIII",
                ["These are photos of Nakwasi"])
nakwasi = grab("These are photos of Nakwasi seed sec sch",
               ["This is Mutual Seed"])
# Nakwasi continues interleaved with Muhula until Bubentsye caption.
# Take Peter's Nakwasi files: WA0816-WA0913 from the caption to Mutual,
# then remaining Peter WA08xx/WA09xx until Bubentsye.
muhula = grab("This is Mutual Seed secondary school",
              ["These are the batch from Bubentsye"])
bubentsye = grab("These are the batch from Bubentsye",
                 ["We found out that the Health centre is Mazimasa"])
docs1845 = grab("8/31/26, 18:45 - Team 12 Butsiba Peter:",
                ["8/31/26, 21:19"])

# Muhula list includes Peter's overlapping Nakwasi files (WA0886+).
# Split by sender ranges we already know:
nakwasi_set = set(nakwasi)
# After Mutual caption the chat interleaves. Peter files 0886-0913 are Nakwasi.
extra_nak = [f for f in muhula if f.startswith("IMG-20260831-WA08") or f.startswith("IMG-20260831-WA09")]
# 0886-0913 are Peter continuing Nakwasi
nakwasi2 = [f for f in extra_nak if f >= "IMG-20260831-WA0886.jpg" and f <= "IMG-20260831-WA0913.jpg"]
muhula_only = [f for f in muhula if f not in nakwasi2]
# Bubentsye list may include files Sophie already sent as Muhula
muhula_set = set(muhula_only)
bub_only = [f for f in bubentsye if f not in muhula_set]

print("mazimasa", len(mazimasa), "nakwasi", len(nakwasi)+len(nakwasi2),
      "muhula", len(muhula_only), "bubentsye", len(bub_only),
      "docs1845", len(docs1845))

PHOTO_FILES = {}
PHOTO_LG = {}
PHOTO_REPEATS = {}

# Mazimasa
m_files, _ = burst(
    mazimasa, 1,
    "Team caption: 'These are for Mazimasa HCIII'. Uncaptioned frame from that batch.",
    special={
        "IMG-20260831-WA1019.jpg":
            ("signboard", "The photograph is the facility signboard, MAZIMASA HEALTH CENTRE III."),
    })
PHOTO_FILES.setdefault("Butaleja", {})["Mazimasa HC III"] = m_files

# Nakwasi
n_files, _ = burst(
    nakwasi + nakwasi2, 1,
    "Team caption: 'These are photos of Nakwasi seed sec sch butaleja district'. "
    "Uncaptioned frame from that batch.",
    special={
        "IMG-20260831-WA0819.jpg":
            ("signboard", "The photograph is the school signboard, NAKWASI SEED SEC SCH."),
    })
PHOTO_FILES.setdefault("Butaleja", {})["Nakwasi Seed Secondary School"] = n_files

# Muhula
h_files, nxt = burst(
    [f for f in muhula_only if f.endswith(".jpg")], 1,
    "Team caption: 'This is Mutual Seed secondary school in Butaleja District'. "
    "The signboard reads MUHULA. Uncaptioned frame from that batch.",
    special={
        "IMG-20260831-WA0808.jpg":
            ("signboard", "The photograph is the school signboard, MUHULA SEED SECONDARY SCHOOL."),
    })
if "VID-20260831-WA0815.mp4" in muhula_only:
    h_files["VID-20260831-WA0815.mp4"] = (
        "%s_video-of-the-compound_ref0815.mp4" % nn(nxt),
        "Sent with the Muhula batch. Moving picture of the school compound.")
PHOTO_FILES.setdefault("Butaleja", {})["Muhula Seed Secondary School"] = h_files

# Bubentsye photos start after toolkit pages 01-07
b_files, _ = burst(
    bub_only, 8,
    "Team caption: 'These are the batch from Bubentsye seed sec school in mbale district'. "
    "Uncaptioned frame from that batch.",
    special={
        "IMG-20260831-WA0714.jpg":
            ("signboard", "Lead frame of the Bubentsye batch."),
    })
PHOTO_FILES.setdefault("Mbale", {})["Bubentsye Seed Secondary School"] = b_files

# 18:45 uncaptioned district papers. WA0616 is already Lwatama.
# WA0629 is the circular. File the rest at Kibuku district (they sit
# between the Kibuku toolkit dump and the later caption).
docs_why = ("Uncaptioned, sent in the late afternoon of 31 August among the "
            "Kibuku toolkit pages. District paper; no facility named.")
lg = {}
n = 14  # Kibuku LG already uses 01-13 in toolkits.py
for src in docs1845:
    if src in taken or src in SKIP:
        continue
    if src == "IMG-20260831-WA0629.jpg":
        lg[src] = (
            "%s_ministry-circular_ref0629.jpg" % nn(n),
            "Ministry of Finance circular. Uncaptioned in the 31 August dump.")
    else:
        lg[src] = (
            "%s_district-document_ref%s.jpg" % (nn(n), ref(src)),
            docs_why)
    n += 1
PHOTO_LG["Kibuku"] = lg

PHOTO_REPEATS["IMG-20260831-WA1064.jpg"] = "selfie-no-asset"

# emit
def emit_dict(name, obj, indent=0):
    lines = ["%s = {" % name]
    if isinstance(list(obj.values())[0], dict) if obj else False:
        # district -> facility -> files  OR district -> files
        for k, v in obj.items():
            if v and isinstance(list(v.values())[0], tuple):
                lines.append("    %r: {" % k)
                for src, (new, why) in v.items():
                    lines.append("        %r:" % src)
                    lines.append("            (%r," % new)
                    wrapped = why.replace("\\", "\\\\").replace("'", "\\'")
                    lines.append("             %r)," % why)
                lines.append("    },")
            else:
                lines.append("    %r: {" % k)
                for fac, files in v.items():
                    lines.append("        %r: {" % fac)
                    for src, (new, why) in files.items():
                        lines.append("            %r:" % src)
                        lines.append("                (%r," % new)
                        lines.append("                 %r)," % why)
                    lines.append("        },")
                lines.append("    },")
    else:
        for src, dest in obj.items():
            lines.append("    %r: %r," % (src, dest))
    lines.append("}")
    return "\n".join(lines)

# count
n_files = sum(len(f) for d in PHOTO_FILES.values() for f in d.values()) + \
          sum(len(v) for v in PHOTO_LG.values())
print("mapped photos", n_files, "repeats", len(PHOTO_REPEATS))

header = '''# -*- coding: utf-8 -*-
"""Asset photographs from the 31 August export, named from the team's
captions and (where a frame was read) from what is in the photograph.

Existing photographs already filed from the first return are left alone.
NN continues from the highest number already in each folder, or from 01
in a new folder. Toolkit pages live in toolkits.py.
"""

'''

body = "\n\n".join([
    emit_dict("PHOTO_FILES", PHOTO_FILES),
    emit_dict("PHOTO_LG", PHOTO_LG),
    emit_dict("PHOTO_REPEATS", PHOTO_REPEATS),
])
open(OUT, "w", encoding="utf-8").write(header + body + "\n")
print("wrote", OUT)
