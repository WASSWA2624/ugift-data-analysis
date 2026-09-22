# -*- coding: utf-8 -*-
"""Write gallery_captions.py from what was read off the contact sheets."""
import json
import os

MANIFEST = json.load(open("tmp/gallery/sheets/manifest.json"))

READ = {}

READ["Kapchorwa__Chemosong-HC-III"] = [
    "Boxed equipment in an opened carton, with its instruction leaflet",
    "Ward block, with an elevated steel water tower alongside",
    "Facility block seen across the compound, with a water tank at its end",
    "Plastic water tanks on a plinth, with an elevated steel tank behind",
    "Facility buildings behind the compound fence",
    "Paediatric cot with side rails, on castors",
]

READ["Kween__Atar-HC-III"] = [
    "Visitors' register open at a signed page",
    "Facility block frontage, with solar panels on the roof",
    "Two-door steel cabinet",
    "Carton marked manual resuscitator, adult silicone, still boxed",
    "Kween District Local Government letter, stamped and signed",
    "Documents on a desk; the frame is out of focus",
    "Office swivel chair at a desk",
]

READ["Kapchorwa__Kaptanya-Seed-Secondary-School"] = [
    "Air conditioner outdoor unit mounted on a wall",
    "Staff house 2, frontage",
    "Staff house 2, gable end",
]

READ["Kapchorwa-Mc__Kaplelko-HC-III"] = [
    "Stainless steel instrument tray among stored ware",
]

READ["Butaleja__Mazimasa-HC-III"] = [
    "Facility signboard above the entrance",
    "Wooden slatted waiting bench",
    "Wooden slatted waiting bench in a corridor",
    "Wooden slatted waiting bench beside a ventilation-block wall",
    "Boxed Littmann Classic II S.E. stethoscope, held up for the record",
    "Stainless steel tray of plastic specula",
    "Store corner with cartons, a lidded bucket and a chair",
    "Boxed equipment carton standing beside a desk",
    "Cartons and disinfection buckets stored in a corner",
    "Medicines and supplies set out on a table over stored cartons",
    "Medicines and supplies on a wooden desk",
    "Glass-front instrument cupboard, with a wheelchair beside it",
    "Cartons stacked in a room",
    "Cartons stacked against a wall",
    "Cartons stacked beside a cabinet",
    "Wheelchair",
    "Refrigerator, with cartons and a sharps container beside it",
    "Carton marked manual resuscitator, standing beside an autoclave",
    "Autoclave standing beside stored cartons",
    "Autoclave and a plastic container in a corner",
    "Autoclave lid on the floor",
    "Two-burner gas stove",
    "Patient trolley with mattress",
    "Examination couches with blue upholstery",
    "Delivery couch",
    "Drip stand",
    "Stretcher trolley, folded",
    "Wall clock above a stainless steel instrument tray",
    "Digital baby weighing scale",
    "Infant warmer above a cot",
    "Stainless steel dressing trolley",
    "Kick-bowl stands with stainless steel bowls",
    "Instrument trolley loaded with trays and supplies",
    "Autoclave drum beside sharps containers",
    "Examination couch with a drip stand",
    "Kidney dish on an examination couch",
    "Column weighing scale",
    "Examination couch",
    "Waiting bench, with plastic basins beside it",
    "Plastic basins in a corridor",
    "Office desk and swivel chair",
    "Column weighing scale standing against a wall",
    "Mesh-back office chair",
    "High-back office chair",
    "Hospital bed",
    "Hospital beds and a ward screen",
    "Hospital bed with the mattress rolled back",
    "Paediatric cot beside a ward screen",
    "Hospital bed beside a ward screen",
    "Hospital bed",
    "Hospital bed, head end",
    "Hospital bed with mattress",
    "Hospital bed",
    "Mesh-back swivel chair beside paediatric cots",
    "Swivel chair beside a paediatric cot",
    "Paediatric cots in a ward",
    "Dressing trolley with supplies",
    "Office table",
    "Mesh-back office chair",
    "Wheelchair",
    "Stainless steel trolley",
    "Examination couch",
    "Hospital bed",
    "Hospital bed in a ward",
    "Hospital bed",
    "Ward screen, folded",
    "Waste bin on a stand, with a lined waste bag",
    "Drip stand beside a bed",
    "Test-tube racks with specimen tubes",
    "Test-tube rack with specimen tubes",
    "Laboratory stool",
    "Laboratory stool with backrest, at a bench",
    "Refrigerator standing on a pallet",
    "Filing cabinet with a drawer open",
    "Laboratory bench with reagents, and a kick bowl beneath",
    "Kick-bowl stand with stainless steel bowl",
    "Foot-operated waste bin",
    "Steel cupboard",
    "Steel cupboard with the door part open",
    "Glass-front instrument cupboard",
    "Desk with a three-drawer pedestal",
    "Desk pedestal drawers",
    "Mesh-back swivel chair",
    "Wooden slatted waiting bench",
    "Wooden desk top carrying an engraved marking",
    "Wooden double-pedestal office desk",
    "Engraved marking on a wooden desk top",
    "Wooden office desk",
    "Wooden office desk",
    "High-back office chair",
    "Chair base carrying a GoU / MoH UgIFT project label",
    "Mobile ward screen",
    "Mobile ward screen",
    "Examination couch",
    "Examination couch",
]

READ["Butaleja__Muhula-Seed-Secondary-School"] = [
    "Page of the school's compiled report, stamped and signed",
    "Report page listing external works and defects",
    "Report page carrying the schedule of defects and outstanding works",
    "Latrine stance with a squat pan",
    "Classroom with a table and a stacked desk top",
    "Wooden desk tops stacked against a wall",
    "Long tables and chairs in a hall",
    "Wall-mounted wooden lockers",
    "Room with desks and wall shelving",
    "Chain-link fence at the playing field",
    "Concrete slab",
    "Steel shelving and a table in a store",
    "Desks stacked in a room",
    "Room with desks, chairs and shelving",
    "Steel shelving unit",
    "Room with desks along the wall",
    "Desktop computers on a bench",
    "Desktop computer with monitor, keyboard and mouse",
    "Roof trusses over a hall",
    "Flat screen mounted high on a wall",
    "Epson projector",
    "HP multifunction printer",
    "ICT room with computers on benches",
    "ICT room with computers along the wall",
    "Window grille and doorway",
    "Row of computers and stools in the ICT room",
    "School block frontage",
    "School compound",
    "School block seen across the compound",
    "Laboratory benches and stools",
    "Laboratory bench top",
    "Laboratory bench with a cupboard beneath",
    "Laboratory bench cupboards beneath the worktop",
    "Laboratory worktop with a sink and cupboards below",
    "Laboratory sink and tap, with wall shelving above",
    "Sink set into a bench in front of a blackboard",
    "Laboratory stool",
    "Laboratory benches and stools",
    "Laboratory stools",
    "Concrete apron beside a building",
    "Water valve chamber, open",
    "Plastic water tank on a masonry plinth",
    "Water tank on a steel tower beside a block",
    "Plastic water tank on a plinth",
    "Small outbuilding in the compound",
    "Stainless steel sink set in a worktop",
    "Bare room with a tiled floor",
    "Corner shelving",
    "Empty room",
    "Classroom block frontage",
    "School block, gable end",
    "School block, gable end",
    "School compound seen from a veranda",
    "School blocks seen from a veranda",
    "Hall with tables, benches and a blackboard",
    "Block veranda",
    "Desks and stools",
    "Desks and wall shelving",
    "Wall shelving",
]

READ["Butaleja__Nakwasi-Seed-Secondary-School"] = [
    "Desktop computer tower and cabling on an office desk",
    "Back of an HP monitor, showing the maker's label",
    "Back of an HP monitor beside a desktop tower",
    "Back of a desktop computer tower",
    "Back of a desktop computer tower with cabling",
    "Room sign reading Classroom Block 3",
    "Room sign reading Classroom Block 2",
    "Room sign reading Classroom Block 1",
    "Room sign reading Administration Block",
    "Office chair beside a desk",
    "Upholstered chairs stacked in a corner",
    "Upholstered chair at a desk",
    "Coiled cabling and cartons",
    "Monitors stacked beside a carton of keyboards and mice",
    "Desktop computer towers stacked in a store",
    "Monitors stacked in a store",
    "Office with desk and chairs",
    "Desk with a keyboard and computer",
    "Stacked desks with a keyboard",
    "Open register on a desk beneath a monitor",
    "Office with a printer and stacked chairs",
    "Upholstered chairs stacked against a wall",
    "Compound path beside a building",
    "Building corner with a ventilation block",
    "Plastic water tank on a masonry plinth",
    "Path alongside a block",
    "Outbuilding beside a compound path",
    "Compound with a clothes-line pole",
    "Outbuilding with ventilation blocks",
    "Compound path",
    "Block behind planting in the compound",
    "Block alongside a compound path",
    "Block frontage",
    "Room with tables and chairs",
    "Water tank on a steel tower",
    "Compound path and grounds",
    "Corridor through a block",
    "Library with shelving, tables and chairs",
    "Library shelving and tables",
    "Library reading tables and shelving",
    "Table and chair by a window",
    "Upholstered chair at a desk",
    "Upholstered chairs stacked above a bookcase",
    "Tables and chairs",
    "Laboratory stools stacked in a corner, with a fire extinguisher",
    "Fire extinguisher beside stacked stools",
    "Room with tables and desks",
    "Room with tables",
    "Room sign reading ICT Library",
    "School block seen across the field",
    "Room sign reading Science Laboratory",
    "Classroom block frontage",
    "Room sign on a block wall",
    "Classroom block frontage",
    "Wooden bench top on the floor",
    "Classroom desks and benches",
    "Classroom desks and blackboard",
    "Classroom desks and benches",
    "Doorway with a bench",
    "School block seen across the field",
    "Classroom desks",
    "Steel desk frame",
    "Desks stacked against a wall",
    "Chair and desk in a classroom",
    "Block wall with peeling paint",
    "Desks stacked in a classroom",
    "Bench tops leaning against desks",
    "Classroom desks and wall shelving",
    "Classroom desks and benches",
    "Tables and chairs before a blackboard",
    "Chairs and desks",
    "Tables and chairs",
    "Desks and chairs",
    "Chairs and tables in a classroom",
    "Stools, chairs and desks in a hall",
    "Desk and chair beside a cupboard",
    "Stool and desk in a classroom",
    "Stools and chairs",
    "Stools before a blackboard",
    "Chair and bench",
    "Steel cupboard with shelving",
    "Tables and chairs by a window",
    "Chair and stool",
    "Chairs and stools",
    "Table and bench by a window",
    "Bench top and frame",
    "Stool",
    "Hall with benches and wall shelving",
    "Rows of classroom desks",
    "Rows of classroom desks",
    "Classroom with benches, tables and a notice board",
    "Room with tables, chairs and wall shelving",
    "Commissioning plaque on the school building",
    "School blocks across the compound",
    "School blocks and compound",
    "Administration block",
    "Completed asset assessment template for the school, stamped and signed",
]

READ["Mbale__Bubentsye-Seed-Secondary-School"] = [
    "Wooden desk and bench",
    "Wooden desk; the frame is underexposed",
    "Classroom desks and benches",
    "Classroom desks",
    "Rows of classroom desks",
    "Tables and desks",
    "Library shelving with books",
    "Library tables and shelving",
    "Library shelving and reading tables",
    "Grounds and hillside beyond the school",
    "School roof, with hills behind",
    "School roofline and hills",
    "Path between school blocks",
    "Block gable and path",
    "Block veranda",
    "Block corner with a ventilation panel",
    "Water tank on a masonry plinth",
    "Latrine block seen from above",
    "Latrine block with ventilation panels",
    "Latrine blocks on the slope",
    "Path between blocks",
    "Retaining wall behind a block",
    "Retaining wall and walkway",
    "Laboratory benches and stools",
    "Laboratory benches and stools",
    "Laboratory bench and stools",
    "Laboratory benches before a blackboard",
    "Test-tube rack on a stool in the laboratory",
    "Laboratory worktop with cupboards below",
    "Wall shelving with reagent bottles",
    "Stool beside a laboratory cupboard",
    "Laboratory worktop with cupboards",
    "Laboratory worktop, shelving and cupboards",
    "Laboratory benches and stools",
    "Laboratory bench and stool",
    "Stool at a laboratory bench",
    "Laboratory stool",
    "Laboratory benches and stools",
    "Laboratory benches",
    "Block roof and handrail on the slope",
    "Water tank on a steel tower",
    "Water tank on a masonry plinth",
    "School blocks on the hillside",
    "School blocks along the slope",
    "School blocks along the slope",
    "School blocks on the slope",
    "School block and grounds",
    "Measuring a veranda with a tape during the verification",
    "Classroom with tables",
    "Table in a classroom",
    "Rows of classroom desks",
    "Classroom desks and benches",
    "Desk and chairs by a window",
    "Chairs against a wall",
    "Rows of desks and chairs in a hall",
    "Classroom block",
    "Classroom block frontage",
    "School block on the slope",
    "Classroom desks and a table before a blackboard",
    "Classroom desks and benches",
    "Classroom with desks and a blackboard",
    "Classroom desks and wall shelving",
    "Classroom with desks and a blackboard",
    "Desks stacked in a classroom",
    "Room with wall shelving and benches",
    "Room with wall shelving and a bench",
    "Desk and bench; the frame is blurred",
    "Classroom desks, with a class seated behind",
    "Classroom desks with a class seated",
    "Desk top and frame",
    "Steel cupboard with the door open",
    "Desk and bench",
    "Hall with wall shelving and benches",
    "Chair",
    "Pedestal desk with drawers",
    "Desk and bench in a classroom",
    "Handwritten count of rooms and furniture, recorded during the visit",
]


HEADER = '''# -*- coding: utf-8 -*-
"""Captions read off the photographs themselves.

Most frames carry the field team's own description in their file name, and the
gallery prints that. Three hundred and forty-five reached the chat with no
caption at all, and were renamed `uncaptioned asset` because nothing in the
record said what they showed. They fall in eight facilities, four of them in
Team 3's Butaleja and Mbale returns.

This file holds what a reading of those images established. Every entry was
written after looking at the frame, from contact sheets of each affected
facility, and says only what is visible in it - the object, and where in the
facility it stands when the frame shows that. Nothing here is inferred from a
delivery note or a toolkit, because the point of a photograph in this gallery
is to say what was on the ground. Where a frame is unreadable - underexposed,
out of focus - the caption says so rather than guessing at it.

Keys are paths relative to `facility-registers/`, which is how
`gallery_index.Frame.rel` names a frame. Written by
`tmp/gallery/write_captions.py` against the contact sheets in
`tmp/gallery/sheets/`; edit there and regenerate rather than by hand, so a
caption always traces back to the frame it was read from.
"""
from __future__ import annotations

READ = {
'''


def main():
    lines = []
    total = 0
    for key, captions in READ.items():
        rels = MANIFEST[key]
        if len(rels) != len(captions):
            raise SystemExit("%s: %d frames, %d captions"
                             % (key, len(rels), len(captions)))
        lines.append("    # %s" % key.replace("__", " / ").replace("-", " "))
        for rel, caption in zip(rels, captions):
            lines.append('    %r:\n        %r,' % (rel, caption))
        lines.append("")
        total += len(rels)
    missing = set(MANIFEST) - set(READ)
    if missing:
        raise SystemExit("no captions for %s" % sorted(missing))
    with open("src/gallery_captions.py", "w", encoding="utf-8") as fh:
        fh.write(HEADER)
        fh.write("\n".join(lines).rstrip() + "\n}\n")
    print("wrote %d captions across %d facilities" % (total, len(READ)))


if __name__ == "__main__":
    main()
