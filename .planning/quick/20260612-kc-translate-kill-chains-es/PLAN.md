---
slug: kc-translate-kill-chains-es
status: in-progress
created: 2026-06-12
---

# Quick Task: Translate KILL-CHAINS.md to Spanish

## Goal
Produce `docs/KILL-CHAINS_ES.md` — a full Spanish translation of `docs/KILL-CHAINS.md`.

## Translation Rules
- **Preserve in English**: everything inside triple-backtick code blocks, inline `code`, MITRE technique IDs (T####.###), OWASP IDs (LLM01..LLM10), ALLCAPS placeholders, URLs, scenario IDs (AD-01, NET-01…), flag IDs, CTF flag values, stage structural abbreviations ([FLAG N], [Attacker], [DC], [MemberSrv], [PivotHost])
- **Translate**: Action field content, Expected Output prose (not code blocks), section intro paragraphs, table text, stage/section headings (structural words; keep technique names like "Kerberoasting" as-is), field labels (**Acción:**, **Comando:**, **Salida esperada:**, **TTP:**)

## Sections (line ranges)
1. Header + intro (1-11)
2. Methodology (12-101)
3. AD Kill-Chains (102-957)
4. Network Protocol Kill-Chains (958-1529)
5. CVE Weaponization Kill-Chains (1530-2300)
6. Cloud/Container Kill-Chains (2301-2801)
7. LLM Security Kill-Chains (2802-3163)
8. Multi-Step ATP Kill-Chains (3164-3991)
9. Consistency Verification (3992-4044)

## Output
`docs/KILL-CHAINS_ES.md`

## Acceptance Criteria
- All 23 scenarios present with the same structure
- All 28 flags present
- Code blocks unchanged
- No MITRE IDs altered
