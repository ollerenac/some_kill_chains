#!/usr/bin/env python3
"""
OFFen EDU Wargame Scraper — Spanish Edition
Fetches all deployed CTF exercises and exports a metadata table to PDF
with Spanish structural labels. Attempts ES API content first, falls back
to EN if the API has no Spanish content for a challenge.

Auth:    POST /api/auth/login  {loginId, password}  → sid session cookie
List:    GET  /api/challenge/all/wargame-challenge?pageNum=1&pageSize=200&...&language=ES
Detail:  GET  /api/challenge/{challengeUuid}/wargame-challenge
"""

import os
import sys
import requests
import re
import time
from html.parser import HTMLParser
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Config ──────────────────────────────────────────────────────────────────
BASE_URL = os.environ.get("OFFEN_BASE_URL", "http://192.168.22.28")
LOGIN_ID = os.environ.get("OFFEN_LOGIN_ID", "")
PASSWORD = os.environ.get("OFFEN_PASSWORD", "")
OUT_PDF  = os.environ.get("OFFEN_OUT_PDF", "offen_wargame_catalog_es.pdf")

if not LOGIN_ID or not PASSWORD:
    sys.exit(
        "ERROR: Set OFFEN_LOGIN_ID and OFFEN_PASSWORD environment variables.\n"
        "  export OFFEN_LOGIN_ID=user1\n"
        "  export OFFEN_PASSWORD=<password>"
    )

LIST_URL  = (
    BASE_URL
    + "/api/challenge/all/wargame-challenge"
    + "?pageNum=1&pageSize=200&sortBy=TITLE&enabledStatus=ENABLED&language=ES"
)
DETAIL_URL = BASE_URL + "/api/challenge/{uuid}/wargame-challenge"

# ── HTML → plain text ────────────────────────────────────────────────────────

class _StripHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []

    def handle_data(self, data):
        self._parts.append(data)

    def get_text(self):
        return re.sub(r'\s+', ' ', ' '.join(self._parts)).strip()


def strip_html(html: str) -> str:
    p = _StripHTML()
    p.feed(html or "")
    return p.get_text()


def derive_scope(description_html: str) -> str:
    """Return a 1-2 sentence plain-text summary from the HTML description."""
    text = strip_html(description_html)
    # Drop "Challenge N" header lines
    text = re.sub(r'^Challenge\s+\d+\s*', '', text, flags=re.IGNORECASE).strip()
    # Take first two sentences (split on .  !  ?)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    summary = ' '.join(sentences[:2]).strip()
    return summary or text[:200]


# ── API helpers ──────────────────────────────────────────────────────────────

def login(session: requests.Session) -> None:
    resp = session.post(
        BASE_URL + "/api/auth/login",
        json={"loginId": LOGIN_ID, "password": PASSWORD},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"Login failed: {data}")
    print("✓ Logged in")


def fetch_list(session: requests.Session) -> list[dict]:
    resp = session.get(LIST_URL, timeout=15)
    resp.raise_for_status()
    items = resp.json()["data"]["list"]
    print(f"✓ {len(items)} challenges in list")
    return items


def fetch_detail(session: requests.Session, challenge_uuid: str) -> dict:
    url = DETAIL_URL.format(uuid=challenge_uuid)
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()["data"]


def fmt_cves(cve_list: list) -> str:
    if not cve_list:
        return "—"
    ids = []
    for c in cve_list:
        # cve objects may carry {cveId, ...} or just be strings
        ids.append(c.get("cveId") or c.get("id") or str(c))
    return ", ".join(ids)


def fmt_ttps(ttp_dto_list: list) -> str:
    if not ttp_dto_list:
        return "—"
    names = [t.get("techniqueName") or t.get("name", "?") for t in ttp_dto_list]
    return ", ".join(names)


def normalize_category(cats: list) -> str:
    mapping = {
        "CRYPTOGRAPHY": "Cryptography",
        "WEB_HACKING": "Web Hacking",
        "FORENSIC": "Forensics",
        "SYSTEM_HACKING": "System Hacking",
        "MALWARE": "Malware",
        "ISMS": "ISMS",
        "REVERSE": "Reversing",
    }
    return ", ".join(mapping.get(c, c.replace("_", " ").title()) for c in cats)


def normalize_type(t: str) -> str:
    return {"TEXT_MATCH": "Text Match"}.get(t, t.replace("_", " ").title())


def normalize_platform(plat_list: list) -> str:
    if not plat_list:
        return "—"
    return ", ".join(p.title() for p in plat_list)


# ── Main scrape ──────────────────────────────────────────────────────────────

def scrape_all() -> list[dict]:
    session = requests.Session()
    login(session)

    challenges = fetch_list(session)
    rows = []
    es_hits = 0

    for i, ch in enumerate(challenges, 1):
        uuid = ch.get("challengeUuid") or ch.get("uuid")
        detail = fetch_detail(session, uuid)

        # Try ES first; fall back to EN if ES content is absent or blank
        lang_block_es = next(
            (d for d in detail.get("detailByLanguage", []) if d["language"] == "ES"),
            None,
        )
        if lang_block_es and lang_block_es.get("title", "").strip():
            lang_block = lang_block_es
            es_hits += 1
        else:
            lang_block = next(
                (d for d in detail.get("detailByLanguage", []) if d["language"] == "EN"),
                (detail.get("detailByLanguage") or [{}])[0],
            )

        title       = lang_block.get("title", "—")
        description = lang_block.get("description", "")
        scope       = derive_scope(description)
        desc_plain  = strip_html(description)

        rows.append({
            "No":              i,
            "Title":           title,
            "Category":        normalize_category(detail.get("categories", [])),
            "Challenge Type":  normalize_type(detail.get("type", "")),
            "Environment":     normalize_platform(detail.get("platformRequired", [])),
            "CVE":             fmt_cves(detail.get("cves", [])),
            "TTP":             fmt_ttps(detail.get("ttpDtoList", [])),
            "Scope":           scope,
            "Description":     desc_plain,
            "Difficulty":      detail.get("difficulty", "—").title(),
        })

        print(f"  [{i:3d}/{len(challenges)}] {title}")
        time.sleep(0.1)   # gentle throttle

    print(f"✓ Scraped {len(rows)} challenges")
    print(f"  Contenido ES encontrado en API: {es_hits}/{len(challenges)} desafios")
    return rows


# ── PDF generation ───────────────────────────────────────────────────────────

COLS = [
    ("No",              0.7 * cm),
    ("Titulo",          3.5 * cm),
    ("Categoria",       2.8 * cm),
    ("Tipo de Reto",    2.2 * cm),
    ("Entorno",         2.0 * cm),
    ("CVE",             2.5 * cm),
    ("TTP",             3.5 * cm),
    ("Alcance",         5.0 * cm),
    ("Descripcion",     7.0 * cm),
]


def build_pdf(rows: list[dict], out_path: str) -> None:
    doc = SimpleDocTemplate(
        out_path,
        pagesize=landscape(A4),
        leftMargin=1 * cm,
        rightMargin=1 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()
    h1 = styles["h1"]

    cell_style = ParagraphStyle(
        "cell",
        fontName="Helvetica",
        fontSize=6.5,
        leading=8,
        spaceAfter=0,
        alignment=TA_LEFT,
    )
    header_style = ParagraphStyle(
        "hdr",
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=9,
        alignment=TA_CENTER,
        textColor=colors.white,
    )

    col_names = [c[0] for c in COLS]
    col_widths = [c[1] for c in COLS]

    header_row = [Paragraph(n, header_style) for n in col_names]

    table_data = [header_row]
    for r in rows:
        table_data.append([
            Paragraph(str(r["No"]),          cell_style),
            Paragraph(r["Title"],            cell_style),
            Paragraph(r["Category"],         cell_style),
            Paragraph(r["Challenge Type"],   cell_style),
            Paragraph(r["Environment"],      cell_style),
            Paragraph(r["CVE"],              cell_style),
            Paragraph(r["TTP"],              cell_style),
            Paragraph(r["Scope"],            cell_style),
            Paragraph(r["Description"],      cell_style),
        ])

    tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        # Header
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("ALIGN",        (0, 0), (-1, 0), "CENTER"),
        ("VALIGN",       (0, 0), (-1, 0), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, 0), 4),
        ("BOTTOMPADDING",(0, 0), (-1, 0), 4),
        # Body rows — alternating shade
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4f8")]),
        ("ALIGN",        (0, 1), (0, -1), "CENTER"),   # No column
        ("VALIGN",       (0, 1), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 1), (-1, -1), 3),
        ("BOTTOMPADDING",(0, 1), (-1, -1), 3),
        ("LEFTPADDING",  (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        # Grid
        ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#c0c8d0")),
        ("LINEBELOW",    (0, 0), (-1, 0),  0.8, colors.HexColor("#1a3a5c")),
    ]))

    title_para = Paragraph(
        "OFFen EDU — Ejercicios de Wargame Desplegados",
        ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=14, spaceAfter=6),
    )
    subtitle = Paragraph(
        f"Total: {len(rows)} desafios  |  Fuente: {BASE_URL}  |  "
        "Categorias: Criptografia, Forense, SGSI, Malware, Reversing, "
        "Hacking de Sistemas, Hacking Web",
        ParagraphStyle("sub", fontName="Helvetica", fontSize=8, spaceAfter=10,
                       textColor=colors.grey),
    )

    doc.build([title_para, subtitle, tbl])
    print(f"✓ PDF written → {out_path}")


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os
    os.chdir("/home/researcher/Research/cont_adic")
    rows = scrape_all()
    build_pdf(rows, OUT_PDF)
