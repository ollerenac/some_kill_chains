---
id: 260617-pde
slug: generar-pdf-en-ingles-del-catalogo-ctf
status: complete
completed: "2026-06-17"
---

# Summary: English PDF Generator

## What was done

Created `scripts/generate_pdf_en.py` — an English counterpart to `scripts/generate_pdf_es.py`.
Running it produces `propuesta_escenarios.pdf` (15 pages, ~90KB) from `SCENARIOS.md`.

Also committed `scripts/generate_pdf_es.py` alongside it (it was previously untracked).

## Output

- `scripts/generate_pdf_en.py` — new English PDF generator
- `scripts/generate_pdf_es.py` — Spanish generator (was untracked, now committed)
- `propuesta_escenarios.pdf` — generated output (gitignored via *.pdf rule)

## Changes from Spanish generator

- Source: `SCENARIOS.md` (English); output: `propuesta_escenarios.pdf`
- Difficulty badges: Easy / Medium / Hard (colors identical to Fácil / Medio / Difícil)
- Domain map keys adapted to English section headers
- Cover and all UI strings translated to English
- Reference table column headers rendered as Resource / URL / Purpose
  (source file still uses Spanish `| Recurso | URL | Propósito |` — not translated)

## Regenerate

```bash
python3 scripts/generate_pdf_en.py              # → propuesta_escenarios.pdf
python3 scripts/generate_pdf_es.py              # → propuesta_escenarios_es.pdf
```
