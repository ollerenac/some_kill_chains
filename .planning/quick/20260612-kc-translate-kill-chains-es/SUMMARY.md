---
slug: kc-translate-kill-chains-es
status: complete
completed: 2026-06-12
---

# Summary: Translate KILL-CHAINS.md to Spanish

## Outcome
`docs/KILL-CHAINS_ES.md` created and committed (1e5fe4c).

## Verification
- 3778 lines
- 8 H2 sections (Metodología through Verificación de Consistencia)
- 28 `### [FLAG 1]` / `### [FLAG 2]` headings (exact match)
- All 23 scenarios present
- Code blocks, MITRE IDs, OWASP IDs, ALLCAPS placeholders, URLs preserved in English
- Descriptive prose, Action/Expected Output fields, section headers translated

## Approach
Direct in-context translation; each of the 7 major kill-chain sections written to
a numbered temp file (`/tmp/kc-es-0N-*.md`), then concatenated to the main file.
