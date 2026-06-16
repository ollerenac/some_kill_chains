#!/usr/bin/env python3
"""
Regenerate Spanish-labeled PDF from the existing English offen_wargame_catalog.pdf.
No VM connection required — parses the existing PDF text with pdftotext.

Usage:
  python3 scripts/pdf_to_es.py
  python3 scripts/pdf_to_es.py [input.pdf] [output.pdf]
"""

import subprocess
import sys
import re
import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Column positions detected from pdftotext -layout header ──────────────────
# "No  Title  Category  Challenge Type  Environment  CVE  TTP  Scope  Description"
COL_STARTS = {
    "No":              0,
    "Title":           5,
    "Category":       31,
    "Challenge Type": 53,
    "Environment":    71,
    "CVE":            86,
    "TTP":           105,
    "Scope":         138,
    "Description":   193,
}
COL_ORDER = ["No", "Title", "Category", "Challenge Type",
             "Environment", "CVE", "TTP", "Scope", "Description"]

HEADER_RE = re.compile(r"^No\s+Title\s+Category")
ROW_START_RE = re.compile(r"^\s{0,4}(\d+)\s")

# Known category values — used to anchor Title/Category boundary when title overflows
CAT_RE = re.compile(
    r'\b(Cryptography|Web Hacking|Forensics|System Hacking|Reversing|Malware|ISMS)\b'
)

# ── PDF layout labels (Spanish) ────────────────────────────────────────────────
COLS_ES = [
    ("No",            0.7 * cm),
    ("Titulo",        3.5 * cm),
    ("Categoria",     2.8 * cm),
    ("Tipo de Reto",  2.2 * cm),
    ("Entorno",       2.0 * cm),
    ("CVE",           2.5 * cm),
    ("TTP",           3.5 * cm),
    ("Alcance",       5.0 * cm),
    ("Descripcion",   7.0 * cm),
]


def extract_text(pdf_path: str) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True, check=True
    )
    return result.stdout


def slice_col(line: str, col: str) -> str:
    start = COL_STARTS[col]
    idx = COL_ORDER.index(col)
    end = COL_STARTS[COL_ORDER[idx + 1]] if idx + 1 < len(COL_ORDER) else len(line)
    return line[start:end].strip() if len(line) > start else ""


def parse_first_line(line: str, num: str) -> dict:
    row = {col: "" for col in COL_ORDER}
    row["No"] = num

    # Use known Category value to anchor the Title/Category boundary.
    # This handles titles longer than the 26-char column width.
    cat_match = CAT_RE.search(line, 5)
    if cat_match:
        row["Title"] = line[5:cat_match.start()].strip()
        row["Category"] = cat_match.group(0)
        # Parse remaining columns by position (they are consistent after Category)
        for col in ["Challenge Type", "Environment", "CVE", "TTP", "Scope", "Description"]:
            row[col] = slice_col(line, col)
    else:
        # Fallback: pure positional slicing
        for col in COL_ORDER[1:]:
            row[col] = slice_col(line, col)

    return row


def parse_rows(text: str) -> list[dict]:
    rows = []
    current = None

    for raw_line in text.splitlines():
        if HEADER_RE.match(raw_line):
            continue

        m = ROW_START_RE.match(raw_line)
        if m:
            if current:
                rows.append(current)
            current = parse_first_line(raw_line, m.group(1))
        elif current is not None:
            # Continuation line — only non-empty column fragments
            for col in COL_ORDER[1:]:
                frag = slice_col(raw_line, col)
                if frag:
                    current[col] = (current[col] + " " + frag).strip()

    if current:
        rows.append(current)

    return rows


def build_pdf_es(rows: list[dict], out_path: str) -> None:
    doc = SimpleDocTemplate(
        out_path,
        pagesize=landscape(A4),
        leftMargin=1 * cm, rightMargin=1 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
    )

    cell_style = ParagraphStyle(
        "cell", fontName="Helvetica", fontSize=6.5, leading=8,
        spaceAfter=0, alignment=TA_LEFT,
    )
    header_style = ParagraphStyle(
        "hdr", fontName="Helvetica-Bold", fontSize=7, leading=9,
        alignment=TA_CENTER, textColor=colors.white,
    )

    col_names_es = [c[0] for c in COLS_ES]
    col_widths    = [c[1] for c in COLS_ES]

    header_row = [Paragraph(n, header_style) for n in col_names_es]
    table_data = [header_row]

    for r in rows:
        table_data.append([
            Paragraph(r["No"],              cell_style),
            Paragraph(r["Title"],           cell_style),
            Paragraph(r["Category"],        cell_style),
            Paragraph(r["Challenge Type"],  cell_style),
            Paragraph(r["Environment"],     cell_style),
            Paragraph(r["CVE"] or "—",      cell_style),
            Paragraph(r["TTP"] or "—",      cell_style),
            Paragraph(r["Scope"],           cell_style),
            Paragraph(r["Description"],     cell_style),
        ])

    tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
        ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
        ("ALIGN",         (0, 0), (-1, 0), "CENTER"),
        ("VALIGN",        (0, 0), (-1, 0), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, 0), 4),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4f8")]),
        ("ALIGN",         (0, 1), (0, -1), "CENTER"),
        ("VALIGN",        (0, 1), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 1), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 3),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 3),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#c0c8d0")),
        ("LINEBELOW",     (0, 0), (-1, 0),  0.8, colors.HexColor("#1a3a5c")),
    ]))

    title_para = Paragraph(
        "OFFen EDU — Ejercicios de Wargame Desplegados",
        ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=14, spaceAfter=6),
    )
    subtitle = Paragraph(
        f"Total: {len(rows)} desafios  |  Categorias: Criptografia, Forense, SGSI, "
        "Malware, Reversing, Hacking de Sistemas, Hacking Web",
        ParagraphStyle("sub", fontName="Helvetica", fontSize=8, spaceAfter=10,
                       textColor=colors.grey),
    )

    doc.build([title_para, subtitle, tbl])
    print(f"✓ PDF escrito → {out_path}")


if __name__ == "__main__":
    os.chdir("/home/researcher/Research/cont_adic")

    in_pdf  = sys.argv[1] if len(sys.argv) > 1 else "offen_wargame_catalog.pdf"
    out_pdf = sys.argv[2] if len(sys.argv) > 2 else "offen_wargame_catalog_es.pdf"

    if not os.path.exists(in_pdf):
        sys.exit(f"ERROR: {in_pdf} no encontrado")

    print(f"Extrayendo texto de {in_pdf}...")
    text = extract_text(in_pdf)

    print("Parseando filas...")
    rows = parse_rows(text)
    print(f"  → {len(rows)} filas encontradas")

    if len(rows) < 80:
        print(f"ADVERTENCIA: se esperaban ~87 filas, se encontraron {len(rows)}")

    build_pdf_es(rows, out_pdf)
