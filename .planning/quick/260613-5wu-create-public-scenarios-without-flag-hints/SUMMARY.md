---
quick_id: 260613-5wu
slug: create-public-scenarios-without-flag-hints
status: complete
completed: 2026-06-13
commit: a005daa
---

# Summary

Sanitized both public SCENARIOS files to remove all flag-spoiling language.

## What was done
- **SCENARIOS_INTERNAL.md** and **SCENARIOS_ES_INTERNAL.md** created as instructor copies (full flag hints, added to .gitignore)
- **SCENARIOS.md** and **SCENARIOS_ES.md** sanitized in-place (24 line changes each):
  - Removed "The flag is contained within…" sentences
  - Replaced "retrieve/recover the flag" → "complete your objective"
  - Replaced "first/second flag" → "first/second objective" in all multi-flag chains (AD-05, ATP-01-04)
  - Replaced LLM flag output phrases with neutral equivalents
  - Sanitized ATP-04 Referencias table entry ("recuperación del primer flag" → "movimiento lateral al objetivo")
- **.gitignore** updated to exclude both `*_INTERNAL.md` files

## Verification
Python checker confirmed zero flag-revealing phrases in both public files after sanitization.
