---
quick_id: 260611-lxt
slug: overlap-check-verify-proposed-scenarios-
date: 2026-06-11
status: complete
---

# Summary: Overlap Check

## Outcome
All 23 proposed scenarios in SCENARIOS.md are clear of the 87 deployed OFFen EDU
wargame challenges. Zero true overlaps found.

## What was done
1. Authenticated to OFFen EDU API and fetched full detail for all 87 deployed challenges
   (including CVE IDs, MITRE ATT&CK TTPs, and descriptions).
2. Generated `offen_wargame_catalog.pdf` — a landscape PDF table of all deployed exercises.
3. Compared each of the 23 proposed scenarios against deployed data on 4 dimensions:
   - Domain/category presence
   - CVE ID collision
   - MITRE TTP technique name overlap
   - Description-level keyword matching
4. 4 false-positive flags resolved (surface word match "escape" / "injection" across
   unrelated technique domains).

## Key finding
Deployed catalog covers 7 original domains only (Cryptography, Web Hacking, Forensics,
System Hacking, Reversing, Malware, ISMS). The 6 proposed new domains (AD, Network,
CVE, Cloud/Container, LLM, APT) are entirely absent from the deployed library.

## Artefacts produced
- `offen_wargame_catalog.pdf` — full deployed exercise catalog
- `scripts/scrape_offen.py` — scraper that generated the catalog
- `.planning/quick/260611-lxt-overlap-check-verify-proposed-scenarios-/OVERLAP-REPORT.md`
