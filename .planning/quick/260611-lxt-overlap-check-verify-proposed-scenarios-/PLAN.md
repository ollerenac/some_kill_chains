---
quick_id: 260611-lxt
slug: overlap-check-verify-proposed-scenarios-
date: 2026-06-11
status: in_progress
---

# Quick Task: Overlap Check — Proposed vs Deployed Wargame Exercises

## Goal
Verify that none of the 23 proposed scenarios in SCENARIOS.md duplicate or
substantially overlap with the 87 exercises already deployed on OFFen EDU.

## Inputs
- `SCENARIOS.md` — 23 proposed scenarios across 6 new domains
- `/tmp/deployed_challenges.json` — 87 live challenges scraped from OFFen EDU
- `offen_wargame_catalog.pdf` — full metadata table (CVE, TTP, description)

## Tasks
1. Enumerate proposed scenario IDs, titles, and domains from SCENARIOS.md
2. Enumerate deployed challenge titles, categories, and techniques
3. Check for overlap by: category/domain, technique name, CVE IDs, description keywords
4. Write OVERLAP-REPORT.md summarising findings

## Deliverable
`.planning/quick/260611-lxt-overlap-check-verify-proposed-scenarios-/OVERLAP-REPORT.md`
