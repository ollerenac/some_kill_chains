#!/usr/bin/env python3
"""Generate PDF from SCENARIOS_ES.md using reportlab."""

import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
FONT_DIR = Path("/usr/share/fonts/truetype/noto")
pdfmetrics.registerFont(TTFont("Noto", str(FONT_DIR / "NotoSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Noto-Bold", str(FONT_DIR / "NotoSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Noto-Italic", str(FONT_DIR / "NotoSans-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Noto-BoldItalic", str(FONT_DIR / "NotoSans-BoldItalic.ttf")))
pdfmetrics.registerFontFamily(
    "Noto",
    normal="Noto",
    bold="Noto-Bold",
    italic="Noto-Italic",
    boldItalic="Noto-BoldItalic",
)

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
C_RED    = colors.HexColor("#C0392B")
C_DARK   = colors.HexColor("#1A1A2E")
C_MID    = colors.HexColor("#2C3E50")
C_LIGHT  = colors.HexColor("#ECF0F1")
C_ACCENT = colors.HexColor("#E74C3C")
C_TABLE_HDR = colors.HexColor("#2C3E50")
C_TABLE_ALT = colors.HexColor("#F8F9FA")
C_LINK   = colors.HexColor("#2980B9")
C_BADGE  = {
    "Fácil":   colors.HexColor("#27AE60"),
    "Medio":   colors.HexColor("#F39C12"),
    "Difícil": colors.HexColor("#C0392B"),
}

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def make_styles():
    base = dict(fontName="Noto", leading=14)
    return {
        "doc_title": ParagraphStyle("doc_title", fontName="Noto-Bold", fontSize=22,
                                    textColor=colors.white, alignment=TA_CENTER, leading=28,
                                    spaceAfter=6),
        "doc_sub":   ParagraphStyle("doc_sub", fontName="Noto", fontSize=11,
                                    textColor=colors.HexColor("#BDC3C7"), alignment=TA_CENTER,
                                    leading=16),
        "intro":     ParagraphStyle("intro", **base, fontSize=9.5, textColor=C_MID,
                                    alignment=TA_JUSTIFY, spaceAfter=6),
        "domain":    ParagraphStyle("domain", fontName="Noto-Bold", fontSize=14,
                                    textColor=colors.white, leading=18),
        "scenario_id": ParagraphStyle("sid", fontName="Noto-Bold", fontSize=10,
                                      textColor=C_RED, leading=13),
        "scenario_title": ParagraphStyle("stitle", fontName="Noto-Bold", fontSize=13,
                                         textColor=C_DARK, leading=16, spaceAfter=4),
        "badge_label": ParagraphStyle("badge", fontName="Noto", fontSize=8.5,
                                      textColor=colors.white, alignment=TA_CENTER, leading=11),
        "body":      ParagraphStyle("body", **base, fontSize=9.5, textColor=C_MID,
                                    alignment=TA_JUSTIFY, spaceAfter=4),
        "killchain": ParagraphStyle("kc", fontName="Noto-Italic", fontSize=8.5,
                                    textColor=C_LINK, leading=12, spaceAfter=6),
        "ref_hdr":   ParagraphStyle("rhdr", fontName="Noto-Bold", fontSize=8,
                                    textColor=colors.white, leading=10),
        "ref_cell":  ParagraphStyle("rcell", fontName="Noto", fontSize=7.5,
                                    textColor=C_DARK, leading=10),
        "ref_url":   ParagraphStyle("rurl", fontName="Noto-Italic", fontSize=7,
                                    textColor=C_LINK, leading=10),
        "ref_section": ParagraphStyle("rsect", fontName="Noto-Bold", fontSize=9,
                                      textColor=C_MID, leading=12, spaceBefore=8, spaceAfter=2),
        "toc_domain": ParagraphStyle("tocd", fontName="Noto-Bold", fontSize=10,
                                     textColor=C_DARK, leading=14, spaceAfter=1),
        "toc_item":  ParagraphStyle("toci", fontName="Noto", fontSize=9,
                                    textColor=C_MID, leading=13, leftIndent=12),
    }

S = make_styles()

# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------
DOMAIN_MAP = {
    "Active Directory": "AD",
    "Explotación de Protocolos": "NET",
    "Exploits de CVE": "CVE",
    "Seguridad en la Nube": "CC",
    "Seguridad de LLMs": "LLM",
    "Cadenas de Ataque APT": "ATP",
}

def parse_md(text):
    """Return (doc_title, intro_text, domains) where domains is a list of dicts."""
    lines = text.splitlines()
    domains = []
    cur_domain = None
    cur_scenario = None
    state = "pre"         # pre | intro | domain | scenario | refs
    intro_lines = []

    def flush_scenario():
        if cur_scenario and cur_domain:
            cur_domain["scenarios"].append(cur_scenario)

    i = 0
    doc_title = ""
    while i < len(lines):
        line = lines[i]

        # Document title
        if line.startswith("# ") and state == "pre":
            doc_title = line[2:].strip()
            state = "intro"
            i += 1
            continue

        # Intro paragraph (lines before first ##)
        if state == "intro":
            if line.startswith("## "):
                state = "domain"
                # don't increment — reprocess as domain
                continue
            if line.strip() and line.strip() != "---":
                intro_lines.append(line.strip())
            i += 1
            continue

        # H2 — domain header
        if line.startswith("## "):
            flush_scenario()
            cur_scenario = None
            label = line[3:].strip()
            # find short key
            short = next((v for k, v in DOMAIN_MAP.items() if k in label), label[:3].upper())
            cur_domain = {"label": label, "short": short, "scenarios": []}
            domains.append(cur_domain)
            state = "domain"
            i += 1
            continue

        # H3 — scenario or Referencias
        if line.startswith("### "):
            header = line[4:].strip()
            if header == "Referencias":
                state = "refs"
                cur_scenario["refs"] = []
                i += 1
                continue
            # new scenario
            flush_scenario()
            cur_scenario = {
                "raw_title": header,
                "difficulty": "",
                "vms": "",
                "body_lines": [],
                "killchain": "",
                "refs": [],
                "multi": "Multi-paso" in header or "2 banderas" in header,
            }
            state = "scenario"
            i += 1
            continue

        # Inside scenario
        if state == "scenario" and cur_scenario is not None:
            if line.startswith("**Dificultad:**"):
                cur_scenario["difficulty"] = line.split("**Dificultad:**")[-1].strip()
            elif line.startswith("**VMs:**"):
                cur_scenario["vms"] = line.split("**VMs:**")[-1].strip()
            elif line.startswith("[→ Kill-Chain]"):
                cur_scenario["killchain"] = line.strip()
            elif line.strip() == "---":
                pass
            elif line.strip() and not line.startswith("#"):
                cur_scenario["body_lines"].append(line.strip())
            i += 1
            continue

        # Inside references table
        if state == "refs" and cur_scenario is not None:
            if line.startswith("|") and "---" not in line:
                cols = [c.strip() for c in line.split("|")[1:-1]]
                if len(cols) >= 3 and cols[0] != "Recurso":
                    cur_scenario["refs"].append(cols)
            elif line.strip() == "---":
                # end of refs block, next section coming
                flush_scenario()
                cur_scenario = None
                state = "domain"
            i += 1
            continue

        i += 1

    flush_scenario()
    return doc_title, " ".join(intro_lines), domains

# ---------------------------------------------------------------------------
# Build helpers
# ---------------------------------------------------------------------------
def badge(text, bg_color):
    """Small coloured rectangle with text, as a 1-cell Table."""
    p = Paragraph(text, S["badge_label"])
    t = Table([[p]], colWidths=[2.2*cm], rowHeights=[0.55*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg_color),
        ("ROUNDEDCORNERS", [3]),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING",   (0,0), (-1,-1), 4),
        ("RIGHTPADDING",  (0,0), (-1,-1), 4),
    ]))
    return t

def difficulty_color(d):
    return C_BADGE.get(d, C_MID)

def ref_table(refs):
    if not refs:
        return []
    hdr = [
        Paragraph("Recurso", S["ref_hdr"]),
        Paragraph("URL", S["ref_hdr"]),
        Paragraph("Propósito", S["ref_hdr"]),
    ]
    rows = [hdr]
    for idx, r in enumerate(refs):
        bg = C_TABLE_ALT if idx % 2 == 0 else colors.white
        rows.append([
            Paragraph(r[0] if len(r) > 0 else "", S["ref_cell"]),
            Paragraph(f'<font color="#2980B9">{r[1]}</font>' if len(r) > 1 else "", S["ref_url"]),
            Paragraph(r[2] if len(r) > 2 else "", S["ref_cell"]),
        ])
    page_w = A4[0] - 3.4*cm   # total available (margins 1.7 each)
    col_w = [page_w * f for f in (0.22, 0.30, 0.48)]
    t = Table(rows, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), C_TABLE_HDR),
        ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_TABLE_ALT, colors.white]),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#DEE2E6")),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    return [t, Spacer(1, 0.25*cm)]

# ---------------------------------------------------------------------------
# Cover page
# ---------------------------------------------------------------------------
def cover_page(doc_title):
    W, H = A4
    from reportlab.platypus import FrameBreak
    from reportlab.platypus.flowables import Flowable

    class ColorRect(Flowable):
        def __init__(self, w, h, color):
            self.w, self.h, self.color = w, h, color
        def draw(self):
            self.canv.setFillColor(self.color)
            self.canv.rect(0, 0, self.w, self.h, fill=1, stroke=0)
        def wrap(self, *args):
            return self.w, self.h

    class LogoBanner(Flowable):
        """Full-width dark header block."""
        def __init__(self, width, title, subtitle):
            self.width = width
            self.title = title
            self.subtitle = subtitle
            self.height = 8*cm
        def draw(self):
            c = self.canv
            # dark background
            c.setFillColor(C_DARK)
            c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
            # red accent bar
            c.setFillColor(C_RED)
            c.rect(0, self.height - 0.35*cm, self.width, 0.35*cm, fill=1, stroke=0)
            # title
            from reportlab.pdfbase.pdfmetrics import stringWidth
            c.setFillColor(colors.white)
            c.setFont("Noto-Bold", 22)
            tw = stringWidth(self.title, "Noto-Bold", 22)
            c.drawString((self.width - tw) / 2, self.height - 2.5*cm, self.title)
            # subtitle
            c.setFont("Noto", 11)
            c.setFillColor(colors.HexColor("#BDC3C7"))
            sw = stringWidth(self.subtitle, "Noto", 11)
            c.drawString((self.width - sw) / 2, self.height - 3.6*cm, self.subtitle)
        def wrap(self, *args):
            return self.width, self.height

    usable_w = W - 3.4*cm
    items = [
        LogoBanner(usable_w, "Catálogo de Escenarios CTF",
                   "Laboratorio Avanzado de Ciberseguridad"),
        Spacer(1, 1.2*cm),
        Paragraph("23 escenarios propuestos · 6 dominios de ataque", S["doc_sub"]),
        Spacer(1, 0.5*cm),
        Paragraph("Active Directory · Protocolos de Red · CVE · Nube · LLM · APT", S["doc_sub"]),
        Spacer(1, 2*cm),
        HRFlowable(width="100%", thickness=1, color=C_RED),
        Spacer(1, 0.4*cm),
        Paragraph("Propuesta de Escenarios — Versión Pública", S["intro"]),
        PageBreak(),
    ]
    return items

# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------
def build_pdf(src_path: Path, out_path: Path):
    text = src_path.read_text(encoding="utf-8")
    doc_title, intro, domains = parse_md(text)

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=1.7*cm, rightMargin=1.7*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="Catálogo de Escenarios CTF",
        author="Laboratorio Avanzado de Ciberseguridad",
    )

    story = []

    # Cover
    story += cover_page(doc_title)

    # Intro
    if intro:
        story.append(Paragraph(intro, S["intro"]))
        story.append(Spacer(1, 0.5*cm))

    # Domains
    for domain in domains:
        # Domain header strip
        hdr_text = f"{domain['short']} — {domain['label']}"
        hdr_p = Paragraph(hdr_text, S["domain"])
        hdr_table = Table([[hdr_p]], colWidths=[A4[0] - 3.4*cm])
        hdr_table.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), C_MID),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ]))
        story.append(Spacer(1, 0.4*cm))
        story.append(hdr_table)
        story.append(Spacer(1, 0.3*cm))

        for sc in domain["scenarios"]:
            # Parse scenario ID and clean title
            raw = sc["raw_title"]
            # e.g. "AD-01: Kerberoasting y AS-REP Roasting"  or  "AD-05: ... [Multi-paso — 2 banderas]"
            m = re.match(r"^([A-Z]+-\d+):\s*(.+?)(\s*\[.+?\])?$", raw)
            if m:
                sc_id = m.group(1)
                sc_title = m.group(2).strip()
                sc_tag = (m.group(3) or "").strip(" []")
            else:
                sc_id = ""
                sc_title = raw
                sc_tag = ""

            diff = sc["difficulty"]
            diff_color = difficulty_color(diff)

            # Header row: [ID+title block] [badges]
            id_p = Paragraph(sc_id, S["scenario_id"])
            title_p = Paragraph(sc_title, S["scenario_title"])
            left_cell = Table([[id_p], [title_p]], colWidths=[None])
            left_cell.setStyle(TableStyle([
                ("TOPPADDING",    (0,0), (-1,-1), 0),
                ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                ("LEFTPADDING",   (0,0), (-1,-1), 0),
                ("RIGHTPADDING",  (0,0), (-1,-1), 0),
            ]))

            diff_badge = badge(diff, diff_color)
            vms_badge  = badge(f"VMs: {sc['vms']}", C_MID)

            badge_col = Table([[diff_badge], [vms_badge]], colWidths=[2.4*cm])
            badge_col.setStyle(TableStyle([
                ("TOPPADDING",    (0,0), (-1,-1), 1),
                ("BOTTOMPADDING", (0,0), (-1,-1), 1),
                ("LEFTPADDING",   (0,0), (-1,-1), 0),
                ("RIGHTPADDING",  (0,0), (-1,-1), 0),
            ]))

            usable_w = A4[0] - 3.4*cm
            hdr = Table([[left_cell, badge_col]],
                        colWidths=[usable_w - 2.6*cm, 2.6*cm])
            hdr.setStyle(TableStyle([
                ("VALIGN",        (0,0), (-1,-1), "TOP"),
                ("TOPPADDING",    (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 4),
                ("LEFTPADDING",   (0,0), (-1,-1), 0),
                ("RIGHTPADDING",  (0,0), (-1,-1), 0),
                ("LINEBELOW",     (0,0), (-1,-1), 0.5, colors.HexColor("#DEE2E6")),
            ]))
            story.append(hdr)

            # Multi-step tag
            if sc_tag:
                story.append(Paragraph(f"<i>{sc_tag}</i>", S["body"]))

            # Body
            body = " ".join(sc["body_lines"])
            if body:
                story.append(Spacer(1, 0.15*cm))
                story.append(Paragraph(body, S["body"]))

            # Kill-chain link
            if sc["killchain"]:
                kc_clean = re.sub(r"\[→ Kill-Chain\]\(([^)]+)\)", r"→ Kill-Chain: \1", sc["killchain"])
                story.append(Paragraph(kc_clean, S["killchain"]))

            # Referencias
            if sc["refs"]:
                story.append(Paragraph("Referencias", S["ref_section"]))
                story += ref_table(sc["refs"])

            story.append(Spacer(1, 0.4*cm))

    doc.build(story)
    print(f"PDF generado: {out_path}")

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    repo = Path(__file__).parent.parent
    src = repo / "SCENARIOS_ES.md"
    out = repo / "scenarios_es.pdf"
    if len(sys.argv) > 1:
        out = Path(sys.argv[1])
    build_pdf(src, out)
