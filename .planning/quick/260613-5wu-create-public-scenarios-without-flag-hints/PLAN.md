---
quick_id: 260613-5wu
slug: create-public-scenarios-without-flag-hints
date: 2026-06-13
status: in_progress
---

# Quick Task: Create Public SCENARIOS Versions Without Flag Hints

## Objective
Create sanitized public versions of SCENARIOS.md and SCENARIOS_ES.md that describe
each CTF scenario without revealing where or how the flags are obtained.
Keep full-detail internal versions locally (gitignored).

## Deliverables
1. SCENARIOS_INTERNAL.md — copy of SCENARIOS.md with all flag hints (gitignored)
2. SCENARIOS_ES_INTERNAL.md — copy of SCENARIOS_ES.md with all flag hints (gitignored)
3. SCENARIOS.md (overwritten) — sanitized: flag-revealing phrases removed/replaced
4. SCENARIOS_ES.md (overwritten) — sanitized: Spanish equivalents removed/replaced
5. .gitignore updated — SCENARIOS_INTERNAL.md and SCENARIOS_ES_INTERNAL.md excluded

## Sanitization Rules

### English replacements
- "recover the credentials that unlock the flag" → "recover the credentials"
- "The flag is contained within the material you recover after successful cracking." → remove sentence
- "obtaining command execution on a target workstation and the flag without ever recovering a plaintext password" → remove "and the flag"
- "chaining the steps until you hold Domain Admin and retrieve the flag" → remove "and retrieve the flag"
- "giving you Domain Admin access and the flag" → remove "and the flag"
- "establishing a foothold that yields the first flag" → "establishing a foothold and securing your first objective"
- "retrieve the second flag" → "secure your second objective"
- "the flag, with no need to crack or recover any password" → remove "the flag,"
- "retrieve the flag" → "complete your objective"
- "recover the flag" → "complete your objective"
- "the flag is embedded in that intercepted request" → remove this clause
- "obtain a shell on the target from which you retrieve the flag" → "obtain a shell on the target"
- "recovering the flag through the resulting shell" → remove clause
- "you retrieve the flag from the target server" → "complete your objective on the target server"
- "retrieve the flag from a location accessible only to SYSTEM" → "complete your objective"
- "retrieve the flag stored in the bucket" → "complete your objective"
- "reading the flag directly from the host's root directory" → "reading sensitive data directly from the host's root directory"
- "the flag planted in the node's root directory" → "your target in the node's root directory"
- "cause the model to output a hidden flag embedded in the LLM's context" → "cause the model to produce the target output"
- "causing the model to output the flag" → "demonstrating the poisoning attack"
- "contains the flag" → "contains your objective"
- "securing your first objective and retrieving the first flag" → "securing your first objective"
- "following it to retrieve the second flag and complete the chain" → "following it to complete the chain"
- "retrieve the first flag from the compromised target" → "complete your first objective on the compromised target"
- "retrieving the second flag from the isolated host" → "completing your second objective on the isolated host"
- "securing the first flag from the node filesystem" → "securing your first objective"
- "retrieve the second flag and complete the cloud identity chain" → "complete the cloud identity chain"
- "retrieve the final flag" / "retrieve the first flag" → "secure your objective" / "secure your first objective"

### Spanish equivalents (same logic)
- "desbloquean la bandera" / "que desbloquean la bandera" → remove clause
- "La bandera se encuentra dentro del material que recuperas tras un craqueo exitoso." → remove
- "y la bandera" (when appended to an action) → remove
- "y recuperar la bandera" → remove
- "y la bandera, sin necesidad de recuperar ninguna contraseña en texto plano" → remove "y la bandera"
- "retrieve flag" equivalents → "completar tu objetivo"
- "primera bandera" → "primer objetivo"
- "segunda bandera" → "segundo objetivo"
- "bandera final" → "objetivo final"
- "la bandera plantada en" → "tu objetivo en"
- "leyendo la bandera directamente" → "leyendo datos sensibles directamente"
- "que contiene la bandera" → "que contiene tu objetivo"
- "recuperar la bandera" → "completar el desafío"
- "recuperas la bandera" → "completas el desafío"

## Tasks
1. [ ] Copy SCENARIOS.md → SCENARIOS_INTERNAL.md
2. [ ] Copy SCENARIOS_ES.md → SCENARIOS_ES_INTERNAL.md
3. [ ] Sanitize SCENARIOS.md (EN)
4. [ ] Sanitize SCENARIOS_ES.md (ES)
5. [ ] Update .gitignore
6. [ ] Commit
7. [ ] Write SUMMARY.md
