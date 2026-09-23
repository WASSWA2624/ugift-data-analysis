"""Fill empty non-attribute columns when the guidelines or the row make the value clear."""

import re
import zipfile
from pathlib import Path

PATH = Path(
    r"D:\coding\ugift-data-analysis\outputs\asset-register-2026-09-23"
    r"\REF_ALL_UGIFT_ASSET_REGISTER_MF_TEMPLATE.xlsx"
)
ROW = re.compile(rb"<row r=\"(\d+)\"([^>]*)>(.*?)</row>", re.S)
STRINGS: list[str] = []
CELL = re.compile(rb'<c r="([A-Z]+)(\d+)"[^>]*(?:/>|>.*?</c>)', re.S)

MACHINERY = "MACHINERY AND EQUIPMENT"
OTHER = "OTHER MACHINERY AND EQUIPMENT"
BUILDINGS = "BUILDINGS AND STRUCTURES"


def column_number(letters: str) -> int:
    number = 0
    for character in letters:
        number = number * 26 + ord(character) - 64
    return number


def column_letters(number: int) -> str:
    letters = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def unescape(text: str) -> str:
    return (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&#10;", " ")
    )


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_strings(xml: bytes) -> list[str]:
    strings = []
    for item in re.finditer(rb"<si>(.*?)</si>", xml, re.S):
        parts = re.findall(rb"<t[^>]*>(.*?)</t>", item.group(1), re.S)
        strings.append("".join(unescape(part.decode("utf-8", "replace")) for part in parts))
    return strings


def cell_value(cell: bytes) -> str:
    if b't="s"' in cell[:160]:
        match = re.search(rb"<v>(\d+)</v>", cell)
        if match:
            index = int(match.group(1))
            if index < len(STRINGS):
                return STRINGS[index].strip()
    return cell_text(cell)


def cell_text(cell: bytes) -> str:
    match = re.search(rb"<t[^>]*>(.*?)</t>|<v>(.*?)</v>", cell, re.S)
    if not match:
        return ""
    raw = match.group(1) if match.group(1) is not None else match.group(2)
    return unescape(raw.decode("utf-8", "replace")).strip()


def text_cell(row_number: str, column: int, value: str) -> bytes:
    ref = f"{column_letters(column)}{row_number}"
    return f'<c r="{ref}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'.encode()


def number_cell(row_number: str, column: int, value: int) -> bytes:
    ref = f"{column_letters(column)}{row_number}"
    return f'<c r="{ref}" t="n"><v>{value}</v></c>'.encode()


def equipment(minor2: str, months: int = 60) -> tuple[str, str, str, int | None, bool]:
    return (MACHINERY, OTHER, minor2, months, True)


def ict(minor2: str, months: int = 60) -> tuple[str, str, str, int | None, bool]:
    return (MACHINERY, "ICT EQUIPMENT", minor2, months, True)


def transport(minor2: str, months: int = 60) -> tuple[str, str, str, int | None, bool]:
    return (MACHINERY, "TRANSPORT EQUIPMENT", minor2, months, True)


def structure(minor2: str, months: int) -> tuple[str, str, str, int | None, bool]:
    return (BUILDINGS, "STRUCTURES", minor2, months, True)


def building(minor1: str, minor2: str, months: int = 600) -> tuple[str, str, str, int | None, bool]:
    return (BUILDINGS, minor1, minor2, months, True)


def classify(description: str) -> tuple[str, str, str, int | None, bool] | None:
    """Return major, minor 1, minor 2, life in months, and whether it depreciates."""
    text = description.casefold().strip()
    if not text or text in {"set", "machine", "equipment", "item", "other", "accessory", "accessories", "-", "schools", "hospitals"}:
        return None
    if re.search(r"\b(total|count|requisitioned|delivered)\b", text) or re.fullmatch(r"-?\d+", text):
        return None
    if re.search(r"\b(pack of|single use|surgicle packs?|graph paper)\b", text):
        return None
    if re.search(r"\b(wheelchair|examination|delivery|hospital|patient|maternity|theatre|operating)\b.{0,20}\b(bed|couch|table)\b", text) or re.search(r"\b(bed|couch|table)\b.{0,20}\b(examination|delivery|hospital|patient|theatre|operating)\b", text):
        return equipment("MED LAB RESEARCH APPLIANCES")
    if re.search(r"\b(autoclave|stethoscope|microscope|centrifuge|sphygmomanometer|fetoscope|foetoscope|otoscope|ophthalmoscope|nebuli[sz]er|sterili[sz]er|incubator|ultrasound|x-?ray|glucometer|haemoglobin|hemoglobin|stadiometer|resuscitator|ambu\s*bag|speculum|forceps|otoscope|laryngoscope|cpap|cannula|dressing drum|counting chamber|neubauer|galipot|gallipot|kidney dish|kick bowl|bowl stand|drip stand|infusion stand|iv stand|oxygen|flow\s*meter|vaccine carrier|cold box|cold chain|suction|thermometer|diagnostic set|delivery kit|ent set|instrument set|instrument trolley|medicine trolley|dressing trolley|patient trolley|bed screen|bedside screen|angle poise|weighing scale|infant scale|height (?:board|meter|measure)|measuring rod)\b", text):
        return equipment("MED LAB RESEARCH APPLIANCES")
    if re.search(r"\b(b\.?\s*p\.?\s*machine|blood pressure|bp apparatus)\b", text):
        return equipment("MED LAB RESEARCH APPLIANCES")
    if re.search(r"\btrolleys?\b", text):
        return equipment("MED LAB RESEARCH APPLIANCES")
    if re.search(r"\b(desks?|deks|chairs?|stools?|bench(?:es)?|bookshel(?:f|ves?|ve)|book\s*shel(?:f|ves?|ve)|cupboards?|cabinets?|sofas?|settees?|shelves|lockers?|drawers?|blackboards?|chalkboards?|whiteboards?|notice\s*boards?|noticeboards?|pin\s*boards?|podiums?|lecterns?|pews?|mattresses?|curtains?|blinds?|filing cabinets?|tables?|waste bins?|bins?|pinboards?)\b", text):
        return equipment("FURNITURE AND FITTINGS")
    if re.search(r"\bservers?\b", text):
        return ict("HEAVY ICT HARDWARE")
    if re.search(r"\b(transmitters?|broadcast(?:ing)? equipment)\b", text):
        return ict("TELEVISION RADIO TRANSMITTER")
    if re.search(r"\b(television|televisions|\btvs?\b|radios?|decoders?|amplifiers?|microphones?|loud\s*speakers?|speakers?|public address|pa system|cctv|cameras?|webcams?)\b", text) and not re.search(r"\b(concrete|tyre|tire)\b", text):
        return ict("OTHER ICT EQUIPMENT")
    if re.search(r"network switches?", text) or (re.search(r"\b(laptops?|desktops?|computers?|computer sets?|cpus?|monitors?|printers?|projectors?|scanners?|tablets?|ups|routers?|modems?|keyboards?|mouses?|mice|hard disks?|telephones?|phones?|handsets?)\b", text) and not re.search(r"\b(laboratory|room|block|building)\b", text)):
        return ict("LIGHT ICT HARDWARE")
    if re.search(r"\b(photocopier|photo\s*copier|fax machines?|shredders?|laminators?|binding machines?|typewriters?|calculators?|safes?|cash boxes?|wall clocks?|clocks?)\b", text):
        return equipment("OFFICE EQUIPMENT")
    if re.search(r"\b(binoculars?|telescopes?)\b", text):
        return equipment("PRECISION OPTICAL INSTRUMENTS")
    if re.search(r"\b(pianos?|organs?|guitars?|drums?|trumpets?|flutes?|violins?|xylophones?|tambourines?|musical instruments?)\b", text):
        return equipment("MUSICAL INSTRUMENTS")
    if re.search(r"\b(footballs?|netballs?|volleyballs?|basketballs?|goal posts?|netball posts?|javelins?|discuses?|discus|shot puts?|rackets?|bats?|sports mats?)\b", text):
        return equipment("SPORTS EQUIPMENT")
    if re.search(r"\b(road signs?|sign posts?|guard rails?|crash barriers?)\b", text):
        return equipment("ROAD FURNITURE")
    if re.search(r"\b(tractors?|concrete mixers?|milling machines?|posho mills?|lathes?|grinding machines?|lawn mowers?)\b", text):
        return equipment("PLANT MACHINERY", 120)
    if re.search(r"\b(generators?|inverters?|stabilizers?|transformers?|solar panels?|solar systems?|solar packages?|solar batter(?:y|ies)|ceiling fans?|fans?|air conditioners?|air conditioning|water pumps?|submersible pumps?|pumps?|water dispensers?|dispensers?|cookers?|stoves?|ovens?|kettles?|security lights?|street lights?)\b", text):
        return equipment("ELECTRICAL MACHINERY")
    if re.search(r"\b(refrigerators?|fridges?|freezers?)\b", text):
        return equipment("ELECTRICAL MACHINERY")
    if re.search(r"\bsoftware\b", text):
        return ("OTHER FIXED ASSETS", "INTELLECTUAL PROPERTY PRODUCTS", "COMPUTER SOFTWARE", 60, True)
    if re.search(r"\b(staff houses?|teachers? houses?|residential houses?|dwellings?|dormitories|hostels?)\b", text):
        return building("DWELLINGS", "RESIDENTIAL BUILDINGS")
    if re.search(r"\b(classroom|class room|administration block|admin block|office block|laboratory block|science lab|library block|multipurpose hall|dining hall|assembly hall|kitchen|latrines?|toilets?|bathrooms?|washrooms?|sick bay|wards?|theatre block|store block|opd block)\b", text):
        return building("BUILDINGS OTHER THAN DWELLINGS", "NON RESIDENTIAL BUILDINGS")
    if re.search(r"\b(boreholes?|shallow wells?|protected springs?|water tanks?|rain\s*water|reservoirs?|piped water)\b", text):
        return structure("WATER SUPPLY SYSTEMS", 400)
    if re.search(r"\b(power lines?|electricity lines?|grid extensions?)\b", text):
        return structure("POWER LINES STATIONS PLANTS", 240)
    if re.search(r"\b(roads?|bridges?|culverts?)\b", text) and not re.search(r"\b(road sign|sign post)\b", text):
        return structure("ROADS AND BRIDGES", 300)
    if re.search(r"\b(fences?|gates?|perimeter walls?|compound walls?|incinerators?|placenta pits?|flag poles?)\b", text):
        return structure("OTHER STRUCTURES", 240)
    if re.search(r"\b(ambulances?|pick[\s-]?ups?|double cabins?|motor\s*cycles?|motorvehicles?|motor vehicles?)\b", text):
        return transport("LIGHT VEHICLES")
    if re.search(r"\b(lorr(?:y|ies)|trucks?|buses|minibuses?)\b", text):
        return transport("HEAVY VEHICLES", 120)
    if re.search(r"\b(bicycles?|bikes?)\b", text):
        return transport("CYCLES")
    if re.search(r"\b(patient screens?|penguin suckers?|disinfection buckets?|buckets?|mva kits?|baby cots?|cots?|muac|mid upper arm|glassware|stretchers?|medical air|air cylinders?|examination lights?|esr stands?|hollow ware|pulse oximeters?|pulse oxymeters?|infant warmers?|radiant warmers?|paediatric beds?|pediatric beds?|adult beds?|icu\b|compression boots?|syringe pumps?|pendants?|bag valve|ambu|oxygen cylinders?|nstrument sets?|instrument sets?)\b", text):
        return equipment("MED LAB RESEARCH APPLIANCES")
    if re.search(r"\bbeds?\b", text):
        if re.search(r"\b(paediatric|pediatric|icu|adult|hospital|patient|delivery|maternity)\b", text):
            return equipment("MED LAB RESEARCH APPLIANCES")
        return equipment("FURNITURE AND FITTINGS")
    if re.search(r"\bstop watches?\b", text):
        return equipment("MED LAB RESEARCH APPLIANCES")
    if re.search(r"\b(conical flasks?|beakers?|boiling tubes?|burettes?|burrets?|pipettes?|prisms?|bunsen|lenses|lens holders?|cell holders?|wire gau[sz]e|meter rules?|metre rules?|magnifying)\b", text):
        return equipment("MED LAB RESEARCH APPLIANCES")
    if re.search(r"\b(hand lenses|magnifying lenses)\b", text):
        return equipment("PRECISION OPTICAL INSTRUMENTS")
    if re.search(r"\b(sockets?|switches|bulb holders?|fluorescent tubes?|flourescent tubes?|surge protectors?|power surge|lightning arrestors?|lightening arrestors?|photo\s*cell)\b", text):
        return equipment("ELECTRICAL MACHINERY")
    if re.search(r"\b(key\s*boards?)\b", text):
        return ict("LIGHT ICT HARDWARE")
    if re.search(r"\b(doors?|windows?|pinboards?|sinks?|taps?)\b", text):
        return equipment("FURNITURE AND FITTINGS")
    if re.search(r"\b(fire extinguishers?|air compressors?|air tanks?|dryers?)\b", text):
        return equipment("PLANT MACHINERY", 120)
    if re.search(r"\b(cabins?|staff quarters|office buildings?)\b", text):
        return building("BUILDINGS OTHER THAN DWELLINGS", "NON RESIDENTIAL BUILDINGS")
    if re.search(r"\bnon[-\s]?residential buildings?\b", text):
        return building("BUILDINGS OTHER THAN DWELLINGS", "NON RESIDENTIAL BUILDINGS")
    if re.search(r"\b(residential buildings?|residential|staff quarters)\b", text):
        return building("DWELLINGS", "RESIDENTIAL BUILDINGS")
    if re.search(r"\b(school land|office land)\b", text) or re.fullmatch(r"land|plot of land|plots?", text):
        return ("LAND", "LAND", "LAND", None, False)
    if re.search(r"\b(down pipes?|gutters?)\b", text):
        return structure("OTHER STRUCTURES", 240)
    if re.search(r"\b(antivirus|anti-virus)\b", text):
        return ("OTHER FIXED ASSETS", "INTELLECTUAL PROPERTY PRODUCTS", "COMPUTER SOFTWARE", 60, True)
    if re.search(r"\b(audio visual|school furniture)\b", text):
        return ict("OTHER ICT EQUIPMENT") if "audio" in text else equipment("FURNITURE AND FITTINGS")
    if re.search(r"\b(inspection devices?)\b", text):
        return ict("LIGHT ICT HARDWARE")
    return None


def explicit_token(text: str, kind: str) -> str | None:
    if kind == "model":
        pattern = r"\bmodel\s*(?:no\.?|number|#)?\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9./-]{1,24})"
    elif kind == "serial":
        pattern = r"\b(?:serial(?:\s*(?:no\.?|number))?|s\s*/\s*n)\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9./-]{2,30})"
    else:
        pattern = r"\b(?:made by|manufactured by|manufacturer)\s+([A-Za-z][A-Za-z0-9&.' -]{1,40})"
    found = re.findall(pattern, text, re.I)
    if len(found) != 1:
        return None
    return found[0].strip(" .,-")


def update_row(match: re.Match[bytes], stats: dict[str, int]) -> bytes:
    row_number = match.group(1).decode()
    attrs = match.group(2)
    if row_number == "1":
        return match.group(0)
    cells = list(CELL.finditer(match.group(3)))
    present = {column_number(cell.group(1).decode()): cell.group(0) for cell in cells}
    values = {number: cell_value(xml) for number, xml in present.items()}
    description = values.get(2, "")
    detail = values.get(50, "")
    evidence = f"{description} {detail}".strip()
    additions: list[tuple[int, bytes]] = []

    classified = classify(description or detail)
    if classified and 3 not in present:
        major, minor1, minor2, months, depreciates = classified
        additions.append((3, text_cell(row_number, 3, major)))
        additions.append((4, text_cell(row_number, 4, minor1)))
        additions.append((5, text_cell(row_number, 5, minor2)))
        stats["class"] += 1
        if depreciates:
            if 33 not in present:
                additions.append((33, text_cell(row_number, 33, "YES")))
            if 34 not in present:
                additions.append((34, text_cell(row_number, 34, "STL")))
            if months and 35 not in present:
                additions.append((35, number_cell(row_number, 35, months)))
            if 39 not in present:
                additions.append((39, number_cell(row_number, 39, 0)))
                stats["salvage"] += 1
        elif 33 not in present:
            additions.append((33, text_cell(row_number, 33, "NO")))

    if (classified or 3 in present) and 7 not in present:
        additions.append((7, text_cell(row_number, 7, "CAPITALIZED")))
        stats["type"] += 1

    status = values.get(54, "")
    if 47 not in present and status in {"Functional", "Faulty"}:
        additions.append((47, text_cell(row_number, 47, "YES" if status == "Functional" else "NO")))
        stats["in_use"] += 1

    for column, kind, key in ((45, "model", "model"), (43, "serial", "serial"), (44, "manufacturer", "manufacturer")):
        if column in present:
            continue
        token = explicit_token(evidence, kind)
        if token:
            additions.append((column, text_cell(row_number, column, token)))
            stats[key] += 1

    if not additions:
        return match.group(0)
    merged = list(present.items()) + additions
    merged.sort(key=lambda item: item[0])
    body = b"".join(xml for _, xml in merged)
    return b'<row r="' + match.group(1) + b'"' + attrs + b">" + body + b"</row>"


def text_cell(row_number: str, column: int, value: str) -> bytes:
    ref = f"{column_letters(column)}{row_number}"
    return f'<c r="{ref}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'.encode()


def number_cell(row_number: str, column: int, value: int) -> bytes:
    ref = f"{column_letters(column)}{row_number}"
    return f'<c r="{ref}" t="n"><v>{value}</v></c>'.encode()


def column_letters(number: int) -> str:
    letters = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def main() -> None:
    stats = {"class": 0, "salvage": 0, "in_use": 0, "model": 0, "serial": 0, "manufacturer": 0, "type": 0}
    global STRINGS
    with zipfile.ZipFile(PATH) as source:
        sheet = source.read("xl/worksheets/sheet1.xml")
        STRINGS = load_strings(source.read("xl/sharedStrings.xml"))
        others = [
            (item.filename, source.read(item.filename))
            for item in source.infolist()
            if item.filename != "xl/worksheets/sheet1.xml"
        ]
    sheet = ROW.sub(lambda match: update_row(match, stats), sheet)
    temporary = PATH.with_suffix(".tmp.xlsx")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as target:
        for name, data in others:
            target.writestr(name, data)
        target.writestr("xl/worksheets/sheet1.xml", sheet)
    temporary.replace(PATH)
    print(stats)
    print("size", PATH.stat().st_size)


if __name__ == "__main__":
    main()
