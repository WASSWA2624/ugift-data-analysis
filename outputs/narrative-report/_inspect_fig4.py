import zipfile
from lxml import etree

src = r"d:\coding\ugift-data-analysis\outputs\narrative-report\adjust-this-copy-07102026-1425.docx"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
C = "{http://schemas.openxmlformats.org/drawingml/2006/chart}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
with zipfile.ZipFile(src) as z:
    doc = etree.fromstring(z.read("word/document.xml"))
    rels = etree.fromstring(z.read("word/_rels/document.xml.rels"))
paras = doc.findall(".//" + W + "p")
for i, p in enumerate(paras):
    text = "".join(t.text or "" for t in p.findall(".//" + W + "t"))
    if "Figure 4" in text or "UgIFT Assets available" in text:
        print("PARA", i, text[:300])
        prev = paras[i - 1]
        charts = prev.findall(".//" + C + "chart")
        print(" prev charts", [c.get(R + "id") for c in charts])
        print(" prev text", "".join(t.text or "" for t in prev.findall(".//" + W + "t"))[:200])
        nxt = paras[i + 1]
        print(" next", "".join(t.text or "" for t in nxt.findall(".//" + W + "t"))[:200])
relmap = {rel.get("Id"): rel.get("Target") for rel in rels}
print("need targets later")
# print all figure 4 nearby chart targets by scanning drawings with descr
for d in doc.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr"):
    descr = d.get("descr") or ""
    name = d.get("name") or ""
    if "MDA" in descr or "MDA" in name or "Figure 4" in descr or "available" in descr.lower():
        print("DOCPR", name, descr[:400])
