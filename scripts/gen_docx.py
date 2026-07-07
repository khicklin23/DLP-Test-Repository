"""
Minimal, dependency-free .docx generator.

This repo's sandbox has no network/pip access, so this builds valid
Office Open XML (.docx) files by hand using only the Python standard
library (zipfile). Good enough to produce realistic-looking Word
documents for DLP test fixtures.

Content is a list of blocks:
    ("h1", "Some Title")
    ("h2", "Some Subheading")
    ("p",  "A normal paragraph of text.")
    ("table", [["Header A", "Header B"], ["row1a", "row1b"], ...])  # first row = header

Usage:
    from gen_docx import make_docx
    make_docx("out.docx", content_blocks)
"""

import zipfile
from xml.sax.saxutils import escape

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>"""

CORE_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>{title}</dc:title>
<dc:creator>DLP-Test-Repository</dc:creator>
<cp:keywords>synthetic-test-data</cp:keywords>
</cp:coreProperties>"""

APP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<Application>DLP-Test-Repository gen_docx.py</Application>
</Properties>"""

DOC_HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>"""

DOC_FOOTER = """<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>
</w:body>
</w:document>"""


def _para(text, style=None, bold=False):
    props = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
    return f'<w:p>{props}<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def _table(rows):
    grid_cols = len(rows[0]) if rows else 1
    tbl = ['<w:tbl>',
           '<w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:color="999999"/>'
           '<w:left w:val="single" w:sz="4" w:color="999999"/>'
           '<w:bottom w:val="single" w:sz="4" w:color="999999"/>'
           '<w:right w:val="single" w:sz="4" w:color="999999"/>'
           '<w:insideH w:val="single" w:sz="4" w:color="999999"/>'
           '<w:insideV w:val="single" w:sz="4" w:color="999999"/>'
           '</w:tblBorders></w:tblPr>',
           f'<w:tblGrid>{"".join("<w:gridCol/>" for _ in range(grid_cols))}</w:tblGrid>']
    for i, row in enumerate(rows):
        tbl.append('<w:tr>')
        for cell in row:
            b = i == 0
            rpr = "<w:rPr><w:b/></w:rPr>" if b else ""
            tbl.append(
                f'<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/></w:tcPr>'
                f'<w:p><w:r>{rpr}<w:t xml:space="preserve">{escape(str(cell))}</w:t></w:r></w:p></w:tc>'
            )
        tbl.append('</w:tr>')
    tbl.append('</w:tbl>')
    # Word requires a paragraph after a table at the end of body content
    tbl.append('<w:p/>')
    return "".join(tbl)


def _render(content):
    parts = []
    for block in content:
        kind = block[0]
        if kind == "h1":
            parts.append(_para(block[1], style="Heading1"))
        elif kind == "h2":
            parts.append(_para(block[1], style="Heading2"))
        elif kind == "p":
            parts.append(_para(block[1]))
        elif kind == "bold":
            parts.append(_para(block[1], bold=True))
        elif kind == "table":
            parts.append(_table(block[1]))
        else:
            raise ValueError(f"unknown block kind: {kind}")
    return "".join(parts)


def make_docx(path, content, title="Document"):
    document_xml = DOC_HEADER + _render(content) + DOC_FOOTER
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("docProps/core.xml", CORE_XML.format(title=escape(title)))
        z.writestr("docProps/app.xml", APP_XML)
        z.writestr("word/document.xml", document_xml)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
