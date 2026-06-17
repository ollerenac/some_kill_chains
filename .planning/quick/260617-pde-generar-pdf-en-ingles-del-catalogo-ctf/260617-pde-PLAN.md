---
id: 260617-pde
slug: generar-pdf-en-ingles-del-catalogo-ctf
status: in_progress
created: "2026-06-17"
---

# Quick Task: Generate English PDF of CTF Catalog

## Objective

Create `scripts/generate_pdf_en.py` — an English counterpart to `scripts/generate_pdf_es.py`
that reads `SCENARIOS.md` and outputs `propuesta_escenarios.pdf`.

## Source of Truth

- Input:  `SCENARIOS.md` (23 English scenarios, public/sanitized)
- Output: `propuesta_escenarios.pdf`
- Model:  `scripts/generate_pdf_es.py` (adapt, not rewrite)

## Changes from Spanish Generator

| Item | Spanish | English |
|------|---------|---------|
| Source file | `SCENARIOS_ES.md` | `SCENARIOS.md` |
| Output file | `propuesta_escenarios_es.pdf` | `propuesta_escenarios.pdf` |
| Difficulty field | `**Dificultad:**` | `**Difficulty:**` |
| Difficulty badges | Fácil / Medio / Difícil | Easy / Medium / Hard |
| Multi-step tag | `Multi-paso`, `2 banderas` | `Multi-step`, `2 flags` |
| Domain map keys | Spanish domain names | English domain names |
| Cover title | "Catálogo de Escenarios CTF" | "CTF Scenario Catalog" |
| Cover subtitle | "Laboratorio Avanzado..." | "Advanced Cybersecurity Lab" |
| Scenario count line | "23 escenarios propuestos..." | "23 proposed scenarios..." |
| Domain subtitle | Spanish domain list | English domain list |
| Footer label | "Propuesta de Escenarios..." | "Scenario Proposal..." |
| References label | "Referencias" | "References" |
| Doc metadata | Spanish | English |

## Notes

- `### Referencias` and `| Recurso | URL | Propósito |` in SCENARIOS.md are still in Spanish
  (appended by quick task 260613-4cx, never translated). The parser handles them as-is;
  only the section heading in the rendered PDF is changed to "References".
- The intro paragraph and all scenario body text are already in English in SCENARIOS.md.

## Steps

1. Write `scripts/generate_pdf_en.py`
2. Run script → verify `propuesta_escenarios.pdf` generates without errors
3. Commit both script + PDF output
4. Update STATE.md
