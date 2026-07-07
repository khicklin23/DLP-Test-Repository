"""
Minimal, dependency-free .xlsx generator (single worksheet).

Same rationale as gen_docx.py: no pip/pandoc in this sandbox, so this hand-
builds a valid Office Open XML spreadsheet using only the stdlib (zipfile).
Cells are written as inline strings (t="inlineStr") to avoid needing a
sharedStrings.xml part, and numeric-looking values are written as numbers
so they don't get Excel's "number stored as text" warning.

Usage:
    from gen_xlsx import make_xlsx
    make_xlsx("out.xlsx", header_row, data_rows, sheet_name="Sheet1")
"""

import zipfile
from xml.sax.saxutils import escape

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

WORKBOOK_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="2">
<font><sz val="11"/><name val="Calibri"/></font>
<font><sz val="11"/><name val="Calibri"/><b/></font>
</fonts>
<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="2">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>
</cellXfs>
</styleSheet>"""

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
<Application>DLP-Test-Repository gen_xlsx.py</Application>
</Properties>"""


def _col_letter(idx: int) -> str:
    """0-indexed column number -> Excel column letters (0 -> A, 25 -> Z, 26 -> AA)."""
    letters = ""
    idx += 1
    while idx > 0:
        idx, rem = divmod(idx - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def _is_number(v) -> bool:
    if isinstance(v, bool):
        return False
    return isinstance(v, (int, float))


def _cell_xml(col_idx, row_idx, value, style_idx=0):
    ref = f"{_col_letter(col_idx)}{row_idx}"
    s_attr = f' s="{style_idx}"' if style_idx else ""
    if _is_number(value):
        return f'<c r="{ref}"{s_attr}><v>{value}</v></c>'
    text = escape(str(value))
    return f'<c r="{ref}"{s_attr} t="inlineStr"><is><t xml:space="preserve">{text}</t></is></c>'


def _sheet_xml(header, rows):
    parts = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
             '<sheetData>']

    header_cells = "".join(_cell_xml(i, 1, h, style_idx=1) for i, h in enumerate(header))
    parts.append(f'<row r="1">{header_cells}</row>')

    for r, row in enumerate(rows, start=2):
        cells = "".join(_cell_xml(i, r, v) for i, v in enumerate(row))
        parts.append(f'<row r="{r}">{cells}</row>')

    parts.append('</sheetData>')
    parts.append('</worksheet>')
    return "".join(parts)


def _workbook_xml(sheet_name):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets>'
        f'<sheet name="{escape(sheet_name)}" sheetId="1" r:id="rId1"/>'
        '</sheets>'
        '</workbook>'
    )


def make_xlsx(path, header, rows, sheet_name="Sheet1", title="Spreadsheet"):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("docProps/core.xml", CORE_XML.format(title=escape(title)))
        z.writestr("docProps/app.xml", APP_XML)
        z.writestr("xl/workbook.xml", _workbook_xml(sheet_name))
        z.writestr("xl/_rels/workbook.xml.rels", WORKBOOK_RELS)
        z.writestr("xl/styles.xml", STYLES)
        z.writestr("xl/worksheets/sheet1.xml", _sheet_xml(header, rows))
