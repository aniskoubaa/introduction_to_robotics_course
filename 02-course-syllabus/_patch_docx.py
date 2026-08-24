#!/usr/bin/env python3
"""
Post-process the pandoc output so it actually renders inside the AU template.

TWO fixes, both required:

  1. TABLE STYLE. Pandoc writes <w:tblStyle w:val="Table"/> on every table, but
     the AU template defines no style with that id -- it has TableNormal and
     TableGrid. The reference is dangling, and Word/LibreOffice fall back to
     something that renders the cells collapsed and empty. Point them at
     TableGrid, which the template does define.

  2. DANGLING PARAGRAPH STYLES. Pandoc styles table-cell paragraphs with its
     own "Compact" style and normally ships that style in the output. With
     --reference-doc it takes styles.xml wholesale from the template instead,
     so "Compact" is referenced everywhere and defined nowhere. Word tolerates
     that; LibreOffice does not -- it renders every table cell EMPTY and spills
     the runs into the body as loose paragraphs, which looks like the table
     lost its content. Any pStyle whose id is not in styles.xml is stripped so
     the paragraph falls back to Normal.

  3. PAGE HEADER. The template's header carries the placeholders "Course Code,
     Title" / "Department Name" / "College Name" / "Term and Year". The middle
     two are single runs and substitute cleanly; "Course Code, Title" is split
     across two runs ("Course " + "Code, Title") because of how it was typed,
     so a plain string replace silently misses it.

Run after every pandoc build. Idempotent.
"""
import re
import shutil
import sys
import zipfile

DOC = sys.argv[1] if len(sys.argv) > 1 else "ee414-syllabus-fall2026.docx"

HEADER_SINGLE_RUN = {
    "Department Name": "Electrical Engineering Department",
    "College Name": "College of Engineering",
    "Term and Year": "Fall 2026",
}
# The split run, handled as an ordered pair so the second half is emptied.
HEADER_SPLIT = [
    ('>Course </w:t>', '>EE 414 — Introduction to Robotics</w:t>'),
    ('<w:t>Code, Title</w:t>', '<w:t xml:space="preserve"></w:t>'),
]

zin = zipfile.ZipFile(DOC)
defined_styles = set(
    re.findall(r'w:styleId="([^"]+)"', zin.read("word/styles.xml").decode("utf-8"))
)
zout = zipfile.ZipFile(DOC + ".tmp", "w", zipfile.ZIP_DEFLATED)
touched = []

for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == "word/document.xml":
        text = data.decode("utf-8")
        n = text.count('<w:tblStyle w:val="Table" />')
        text = text.replace('<w:tblStyle w:val="Table" />',
                            '<w:tblStyle w:val="TableGrid" />')
        text = text.replace('<w:tblStyle w:val="Table"/>',
                            '<w:tblStyle w:val="TableGrid"/>')
        if n:
            touched.append(f"document.xml: {n} table style refs -> TableGrid")

        dangling = {
            sid for sid in set(re.findall(r'<w:pStyle w:val="([^"]+)"\s*/>', text))
            if sid not in defined_styles
        }
        for sid in dangling:
            text = re.sub(r'<w:pStyle w:val="%s"\s*/>' % re.escape(sid), "", text)
        if dangling:
            touched.append(
                "document.xml: stripped undefined paragraph styles "
                + ", ".join(sorted(dangling))
            )
        data = text.encode("utf-8")
    elif item.filename.startswith("word/header"):
        text = data.decode("utf-8")
        before = text
        for old, new in HEADER_SINGLE_RUN.items():
            text = text.replace(old, new)
        for old, new in HEADER_SPLIT:
            text = text.replace(old, new)
        if text != before:
            touched.append(f"{item.filename}: header placeholders filled")
        data = text.encode("utf-8")
    zout.writestr(item, data)

zout.close()
zin.close()
shutil.move(DOC + ".tmp", DOC)
print("\n".join(touched) if touched else "nothing to patch (already done?)")
