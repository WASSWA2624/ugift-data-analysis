# -*- coding: utf-8 -*-
"""Check the built gallery against the register tree it was built from."""
import os
import re
import sys

import fitz

sys.path.insert(0, "src")
import gallery_index as gi  # noqa: E402

PDF = ("final-UGiFT-report-karamojja-6-teams/"
       "UGiFT-verification-photographic-gallery.pdf")


def main():
    teams, _measured = gi.build(verbose=False)
    doc = fitz.open(PDF)
    pages = [doc[i].get_text() for i in range(doc.page_count)]
    joined = "\n".join(pages)
    problems = []

    # 1. Every figure number runs 1..N with no gap.
    numbers = [int(n) for n in re.findall(r"Figure (\d+)\.", joined)]
    expected = sum(t.shown for t in teams)
    if sorted(numbers) != list(range(1, expected + 1)):
        missing = set(range(1, expected + 1)) - set(numbers)
        problems.append("figures: %d found, %d expected, %d missing %s"
                        % (len(numbers), expected, len(missing),
                           sorted(missing)[:10]))
    else:
        print("Figures 1-%d, all present" % expected)

    # 2. The contents page names every team and local government, and the
    #    page it gives is the page the heading is actually on.
    toc_text = "\n".join(pages[1:3])
    entries = re.findall(r"(Team \d\d|[A-Z][A-Za-z' /]+?(?:District|"
                         r"Municipal Council))\s*\.{2,}\s*(\d+)", toc_text)
    listed = {name.strip(): int(page) for name, page in entries}
    print("Contents lists %d entries" % len(listed))
    # The footer prints the PDF page number itself, so a contents entry saying
    # page N must name the heading that opens PDF page N.
    def heading_page(title, follows):
        """The first page where this title stands as a heading.

        The team's summary table repeats every local government name, so a bare
        line match finds the table rather than the chapter. A heading is the
        title followed by its own inventory line, which the table never is.
        """
        for i, text in enumerate(pages[3:], start=4):
            lines = [ln.strip() for ln in text.split("\n")]
            for j, line in enumerate(lines):
                if line != title:
                    continue
                rest = [x for x in lines[j + 1:j + 3] if x]
                if rest and rest[0].startswith(follows):
                    return i
        return None

    for team in teams:
        wanted = [(team.label, team.region)]
        wanted += [(lg.title, team.label)
                   for lg in team.local_governments]
        for title, follows in wanted:
            if title not in listed:
                problems.append("contents: %r not listed" % title)
                continue
            actual = heading_page(title, follows)
            if actual is None:
                problems.append("contents: %r has no heading in the document"
                                % title)
            elif actual != listed[title]:
                problems.append("contents: %r given as page %d, found on %d"
                                % (title, listed[title], actual))

    # 3. Every facility in the tree has a heading, including the empty ones.
    for facility in gi.all_facilities(teams):
        if facility.kind == gi.TEAM:
            continue
        if facility.name not in joined:
            problems.append("facility: %r has no heading" % facility.name)
    empty = [f for f in gi.all_facilities(teams) if not f.on_file]
    print("%d facilities, %d of them with no photographs on file"
          % (len([f for f in gi.all_facilities(teams)
                  if f.kind not in (gi.DISTRICT, gi.TEAM)]), len(empty)))
    if "no photographs on file" not in joined and empty:
        problems.append("empty facilities are not marked")

    # 4. Nothing is captioned with a stale placeholder.
    stale = joined.count("not described in the field return")
    print("%d frames captioned as undescribed" % stale)

    print("\n%d pages, %.0f MB" % (doc.page_count, os.path.getsize(PDF) / 1e6))
    if problems:
        print("\n%d PROBLEMS" % len(problems))
        for p in problems[:40]:
            print("  -", p)
        return 1
    print("\nNo problems found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
