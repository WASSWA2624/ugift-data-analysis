# ---------------------------------------------------------------------------
# Photographs
# ---------------------------------------------------------------------------

# A photograph is shown whole. Nothing is cropped, because a cropped frame is
# no longer the evidence that was taken: a signboard loses its district line, a
# ward loses the bed at its edge.
#
# Frames are therefore laid out the way a picture editor lays out a plate: the
# frames on a line are scaled to one common height chosen so that the line
# fills the text column exactly. Every line runs margin to margin, every frame
# on a line stands the same height, and a tall frame no longer leaves the white
# gutter beside it that a fixed width forces. Line heights are picked for the
# whole plate at once, so one facility's frames read as a set rather than as
# unrelated pictures that happen to sit together.

TEXT_W_IN = 6.77                 # the text column, margin to margin
PLATE_W_IN = 6.70                # what a line of frames is allowed to occupy
GUTTER_IN = 0.11                 # white between two frames on a line
TARGET_ROW_H_IN = 1.85           # the height a line is aimed at
MIN_ROW_H_IN = 1.42              # below this a frame stops being evidence
MAX_ROW_H_IN = 2.50              # above this one facility swamps the page
MAX_PER_ROW = 4                  # more than four and nothing can be read
CAPTION_PT = 8


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


def aspect_of(path):
    with Image.open(path) as im:
        w, h = im.size
    return w / float(h)


def row_height(aspects):
    """The common height at which these frames exactly fill the text column."""
    usable = PLATE_W_IN - len(aspects) * GUTTER_IN
    return usable / sum(aspects)


def row_cost(height, count):
    """How far a line is from the height a line should be.

    A line outside the band is not forbidden - a facility whose only frame is a
    tall one has to be shown somehow - but it is charged heavily, so the layout
    reaches for it only when nothing else will do.
    """
    cost = (height - TARGET_ROW_H_IN) ** 2
    if height < MIN_ROW_H_IN:
        cost += 40 + 20 * (MIN_ROW_H_IN - height) ** 2
    elif height > MAX_ROW_H_IN:
        cost += 40 + 20 * (height - MAX_ROW_H_IN) ** 2
    if count == 1:
        cost += 0.05          # a line of one is a last resort, not a habit
    return cost


def _plan_in_order(aspects):
    """The best way to break this sequence into lines without reordering it.

    Exact, not greedy: the same dynamic programme a typesetter uses to break a
    paragraph into lines, so a bad line is never forced on a later one.
    """
    n = len(aspects)
    best = [0.0] + [float("inf")] * n
    cut = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(max(0, j - MAX_PER_ROW), j):
            cost = best[i] + row_cost(row_height(aspects[i:j]), j - i)
            if cost < best[j]:
                best[j] = cost
                cut[j] = i
    rows, j = [], n
    while j > 0:
        rows.append(list(range(cut[j], j)))
        j = cut[j]
    rows.reverse()
    return rows, best[n]


def _plan_regrouped(aspects):
    """The best lines when frames may be regrouped, keeping order inside a line.

    A very tall frame cannot share a line with a second very tall frame - the
    pair would stand three inches high - but it sits happily beside a wide one.
    Regrouping lets that pairing happen; the caption travels with its frame, so
    nothing is mislabelled by the move.
    """
    remaining = list(range(len(aspects)))
    rows = []
    while remaining:
        row = [remaining.pop(0)]
        while len(row) < MAX_PER_ROW and remaining:
            here = row_cost(row_height([aspects[i] for i in row]), len(row))
            pick = None
            for pos, idx in enumerate(remaining[:6]):
                trial = row + [idx]
                cost = row_cost(row_height([aspects[i] for i in trial]),
                                len(trial))
                if pick is None or cost < pick[0]:
                    pick = (cost, pos, idx)
            if pick is None or pick[0] >= here:
                break
            remaining.pop(pick[1])
            row.append(pick[2])
        rows.append(sorted(row))
    total = sum(row_cost(row_height([aspects[i] for i in r]), len(r))
                for r in rows)
    return rows, total


def plan_plate(aspects):
    """Break a facility's frames into full-width lines.

    The sequence is kept if it lays out well, because it is the order the
    frames were chosen in - the site, then what is in it, then what is wrong
    with it. It is regrouped only where keeping it would leave a line short or
    a frame overbearing.
    """
    if not aspects:
        return []
    rows, cost = _plan_in_order(aspects)
    if any(not MIN_ROW_H_IN <= row_height([aspects[i] for i in r])
           <= MAX_ROW_H_IN for r in rows):
        alt, alt_cost = _plan_regrouped(aspects)
        if alt_cost < cost:
            rows = alt
    return rows


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


def _exact_widths(table, inches):
    """Take the widths python-docx wrote at face value: no autofit, no padding.

    Word will otherwise pad each cell and rebalance the row, and a line planned
    to the hundredth of an inch stops filling the column.
    """
    tblPr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    width = OxmlElement("w:tblW")
    width.set(qn("w:w"), str(int(round(inches * 1440))))
    width.set(qn("w:type"), "dxa")
    tblPr.append(width)
    margins = OxmlElement("w:tblCellMar")
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement("w:" + side)
        el.set(qn("w:w"), "0")
        el.set(qn("w:type"), "dxa")
        margins.append(el)
    tblPr.append(margins)


def add_photo_plate(doc, items, figure):
    """A facility's frames, laid out as full-width lines under its entry."""
    aspects = [aspect_of(path) for path, _caption in items]
    for row in plan_plate(aspects):
        height = row_height([aspects[i] for i in row])
        height = min(max(height, MIN_ROW_H_IN), MAX_ROW_H_IN)
        widths = [aspects[i] * height for i in row]
        table = doc.add_table(rows=1, cols=len(row))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        _exact_widths(table, sum(widths) + len(row) * GUTTER_IN)
        _no_row_break(table.rows[0])
        for column, idx in enumerate(row):
            path, caption = items[idx]
            cell = table.cell(0, column)
            cell.width = Inches(widths[column] + GUTTER_IN)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.keep_with_next = True
            p.add_run().add_picture(path, width=Inches(widths[column]),
                                    height=Inches(height))
            cap = cell.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap.paragraph_format.space_before = Pt(1)
            cap.paragraph_format.space_after = Pt(0)
            figure[0] += 1
            run = cap.add_run("Figure %d.  %s" % (figure[0], caption))
            set_run_font(run, size=CAPTION_PT, color=GREY)
        add_para(doc, "", space_after=0, size=4)
    add_para(doc, "", space_after=3, size=4)


def photos_for(team, lg, folder):
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


