# ---------------------------------------------------------------------------
# Photographs
# ---------------------------------------------------------------------------

# A photograph is shown whole. Nothing is cropped, because a cropped frame is
# no longer the evidence that was taken: a signboard loses its district line, a
# ward loses the bed at its edge. Instead every frame is scaled to one common
# height, so a row of two still reads as a pair, and a frame too wide for the
# column is held back by its width instead.
PHOTO_H_IN = 1.95
PHOTO_MAX_W_IN = 2.90
CELL_W_IN = 3.10


def normalise(src, dest, long_edge=1400, quality=80):
    """A smaller copy of the whole frame. No crop: the frame is the evidence."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest) and os.path.getmtime(dest) >= os.path.getmtime(src):
        return dest
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode != "RGB":
            im = im.convert("RGB")
        w, h = im.size
        scale = long_edge / float(max(w, h))
        if scale < 1.0:
            im = im.resize((int(w * scale), int(h * scale)),
                           Image.Resampling.LANCZOS)
        im.save(dest, "JPEG", quality=quality, optimize=True)
    return dest


def fitted_size(path):
    """Width and height that show the whole frame inside the column."""
    with Image.open(path) as im:
        w, h = im.size
    aspect = w / float(h)
    height = PHOTO_H_IN
    width = height * aspect
    if width > PHOTO_MAX_W_IN:
        width = PHOTO_MAX_W_IN
        height = width / aspect
    return Inches(width), Inches(height)


def _repeat_header(row):
    """Repeat a table's header row at the top of every page it runs onto."""
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def _no_row_break(row):
    """Keep a row - and so a photograph and its caption - on one page."""
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    trPr.append(el)


def add_photo_row(doc, items, figure):
    """Two photographs side by side, each captioned directly beneath it."""
    table = doc.add_table(rows=1, cols=len(items))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    _no_row_break(table.rows[0])
    for i, (path, caption) in enumerate(items):
        cell = table.cell(0, i)
        cell.width = Inches(CELL_W_IN)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.keep_with_next = True
        width, height = fitted_size(path)
        p.add_run().add_picture(path, width=width, height=height)
        cap = cell.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_before = Pt(1)
        cap.paragraph_format.space_after = Pt(0)
        figure[0] += 1
        r = cap.add_run("Figure %d.  %s" % (figure[0], caption))
        set_run_font(r, size=8, color=GREY)
    add_para(doc, "", space_after=3)


def photos_for(team, lg, folder, figure_pool):
    """Compressed copies of the frames chosen for this facility."""
    tag = tag_of(team, lg, folder)
    chosen = report_photos.PHOTOS.get(tag, [])
    out = []
    src_dir = facility_dir(team, lg, folder)
    for filename, caption in chosen:
        src = os.path.join(src_dir, filename)
        if not os.path.exists(src):
            raise SystemExit("Photograph missing: %s" % src)
        dest = os.path.join(PHOTO_CACHE, tag + "__" + filename)
        out.append((normalise(src, dest), caption))
    return out


