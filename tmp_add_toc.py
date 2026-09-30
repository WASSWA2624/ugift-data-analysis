"""Add contents entries for the new per-MDA sections."""
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from tmp_mda_section import DOC_PATH, MDAS, XML_SPACE, next_bookmark_id

PATH = DOC_PATH


def bookmark(paragraph, name, bookmark_id):
    start = OxmlElement("w:bookmarkStart")
    start.set(qn("w:id"), str(bookmark_id))
    start.set(qn("w:name"), name)
    end = OxmlElement("w:bookmarkEnd")
    end.set(qn("w:id"), str(bookmark_id))
    props = paragraph._p.find(qn("w:pPr"))
    if props is None:
        paragraph._p.insert(0, start)
    else:
        props.addnext(start)
    paragraph._p.append(end)


def run(parent, text=None, tab=False, field=None, size="19", no_proof=False):
    node = OxmlElement("w:r")
    props = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), size)
    props.append(sz)
    if no_proof:
        props.append(OxmlElement("w:noProof"))
    node.append(props)
    if text is not None:
        text_node = OxmlElement("w:t")
        if text[:1] == " " or text[-1:] == " ":
            text_node.set(XML_SPACE, "preserve")
        text_node.text = text
        node.append(text_node)
    if tab:
        node.append(OxmlElement("w:tab"))
    if field:
        char = OxmlElement("w:fldChar")
        char.set(qn("w:fldCharType"), field)
        node.append(char)
    parent.append(node)


def contents_entry(title, anchor):
    paragraph = OxmlElement("w:p")
    props = OxmlElement("w:pPr")
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "right")
    tab.set(qn("w:leader"), "dot")
    tab.set(qn("w:pos"), "9965")
    tabs.append(tab)
    props.append(tabs)
    spacing = OxmlElement("w:spacing")
    spacing.set(qn("w:after"), "30")
    spacing.set(qn("w:line"), "245")
    spacing.set(qn("w:lineRule"), "auto")
    props.append(spacing)
    indent = OxmlElement("w:ind")
    indent.set(qn("w:left"), "576")
    props.append(indent)
    align = OxmlElement("w:jc")
    align.set(qn("w:val"), "left")
    props.append(align)
    paragraph.append(props)
    link = OxmlElement("w:hyperlink")
    link.set(qn("w:anchor"), anchor)
    link.set(qn("w:history"), "1")
    run(link, text=title)
    run(link, tab=True)
    run(link, field="begin")
    instr_run = OxmlElement("w:r")
    props = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "19")
    props.append(sz)
    instr_run.append(props)
    instr = OxmlElement("w:instrText")
    instr.set(XML_SPACE, "preserve")
    instr.text = f" PAGEREF {anchor} "
    instr_run.append(instr)
    link.append(instr_run)
    run(link, field="separate")
    run(link, text="0", no_proof=True)
    run(link, field="end")
    paragraph.append(link)
    return paragraph


def main():
    document = Document(PATH)
    bookmark_id = next_bookmark_id(document)
    headings = {}
    for paragraph in document.paragraphs:
        if not (paragraph.style and paragraph.style.name == "Heading 3"):
            continue
        for item in MDAS:
            if paragraph.text == item["heading"]:
                name = f"heading_{item['key']}"
                if name not in paragraph._p.xml:
                    bookmark(paragraph, name, bookmark_id)
                    bookmark_id += 1
                headings[item["key"]] = name
    host = None
    for paragraph in document.paragraphs:
        if paragraph.text.startswith("4.2 Ministries, departments and agencies"):
            host = paragraph._element
            break
    if host is None:
        raise SystemExit("contents entry for 4.2 not found")
    # Drop an earlier copy of these contents lines if the script is run again.
    for paragraph in list(document.paragraphs):
        xml = paragraph._p.xml
        if "PAGEREF heading_mofped" in xml:
            paragraph._element.getparent().remove(paragraph._element)
    host = None
    for paragraph in document.paragraphs:
        if paragraph.text.startswith("4.2 Ministries, departments and agencies"):
            host = paragraph._element
            break
    entries = [contents_entry(item["heading"], f"heading_{item['key']}") for item in MDAS]
    for entry in reversed(entries):
        host.addnext(entry)
    document.save(PATH)
    print("contents entries", len(entries), "bookmarks", len(headings))


if __name__ == "__main__":
    main()
