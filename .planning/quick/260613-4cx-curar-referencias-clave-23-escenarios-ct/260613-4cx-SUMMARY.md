---
phase: quick-260613-4cx
plan: 01
subsystem: documentation
tags: [references, ctf, scenarios, documentation, cybersecurity]
dependency_graph:
  requires: []
  provides:
    - docs/REFERENCES.md (master reference catalog for all 23 scenarios)
    - SCENARIOS.md ### Referencias blocks (23 inline reference blocks)
    - docs/KILL-CHAINS.md ## Referencias appendix (23 H3 sections)
  affects:
    - SCENARIOS.md
    - docs/KILL-CHAINS.md
tech_stack:
  added: []
  patterns:
    - Markdown reference tables with Recurso|URL|Propósito columns
    - Bottom-to-top Edit insertion strategy to preserve line numbers
key_files:
  created:
    - docs/REFERENCES.md
  modified:
    - SCENARIOS.md
    - docs/KILL-CHAINS.md
decisions:
  - Used github.com/bettercap/bettercap instead of www.bettercap.org/modules/ (404 on /modules/ path)
  - Used HackTricks LLMNR relay page for NET-01 instead of a standalone SMB relay guide (best available content match)
  - Chose MITRE ATT&CK T1078 (Valid Accounts) for LLM-03 IDOR scenario as closest applicable technique
metrics:
  duration: ~25 minutes
  completed: "2026-06-13"
  tasks_completed: 3
  files_changed: 3
---

# Quick Task 260613-4cx: CTF Scenario Reference Catalog Summary

**One-liner:** Created 294-line master reference catalog (docs/REFERENCES.md) with 23 scenario sections containing verified URLs, then appended 23 ### Referencias blocks to SCENARIOS.md and a 233-line ## Referencias appendix to docs/KILL-CHAINS.md — all URLs verified reachable via HTTP before writing.

## What Was Built

Three reference artifacts were created to give instructors and students clickable, authoritative links for all 23 CTF scenarios:

1. **docs/REFERENCES.md** — New master catalog (294 lines). One H2 per domain, one H3 per scenario, 3–5 reference table rows each. Format: `| Recurso | URL | Propósito |` in Spanish. Covers all 6 domains: AD (5 scenarios), NET (4), CVE (4), CC (3), LLM (3), ATP (4).

2. **SCENARIOS.md** — 230 lines added. A `### Referencias` block inserted before each scenario's trailing `---` separator (or appended at EOF for ATP-04). Worked bottom-to-top to avoid line drift. Zero existing text modified.

3. **docs/KILL-CHAINS.md** — 236 lines appended after line 4044. New `## Referencias` section with 23 H3 subsections. Original body verified intact (final PASS row remains at line 4043).

## Commits

| Hash | Task | Description |
|------|------|-------------|
| c667c0a | Task 1 | feat(quick-260613-4cx-01): create master reference catalog for all 23 CTF scenarios |
| eeb92c9 | Task 2 | feat(quick-260613-4cx-02): append ### Referencias blocks to all 23 scenarios in SCENARIOS.md |
| 7e180b5 | Task 3 | feat(quick-260613-4cx-03): append ## Referencias appendix to docs/KILL-CHAINS.md |

## URL Verification Results

All URLs verified reachable (HTTP 200) before writing. Key verified sources:

- GitHub repos: fortra/impacket, ly4k/Certipy, SpecterOps/BloodHound, lgandx/Responder, GhostPack/Rubeus, Pennyw0rth/NetExec, Hackplayers/evil-winrm, dirkjanm/mitm6, dirkjanm/krbrelayx, tomac/yersinia, jpillora/chisel, iagox86/dnscat2, nicocha30/ligolo-ng, worawit/MS17-010, 3ndG4me/AutoBlue-MS17-010, axelcurmi/log4shell-docker-lab, christophetd/log4shell-vulnerable-app, cube0x0/CVE-2021-1675, ReversecLabs/damn-vulnerable-llm-agent, ollama/ollama, NVIDIA/garak, PowerShellMafia/PowerSploit
- NVD entries: CVE-2017-0144, CVE-2021-44228, CVE-2017-5638, CVE-2021-34527
- MITRE ATT&CK: T1558.003, T1557.001, T1649, T1098, T1190, T1059, T1557, T1040, T1568, T1611, T1552.007, T1602, T1068, T1505.003, T1021.006, T1195, T1071.004, T1606, T1550.002, T1078
- Official docs: frrouting.org, docs.k3s.io, docs.aws.amazon.com/AWSEC2 IMDS, docs.docker.com/engine/security
- Third-party: hashcat.net, blog.trailofbits.com docker escape post, madhuakula.com kubernetes-goat, owasp.org LLM Top 10, owasp.org promptme, bishopfox.com LLM CTF, cwiki.apache.org S2-045, hub.docker.com piesecurity Struts image

## Deviations from Plan

### Auto-resolved URL Issues

**1. [Rule 1 - Bug] bettercap /modules/ URL returned 404**
- **Found during:** Task 1 URL verification
- **Issue:** `https://www.bettercap.org/modules/` returns HTTP 404
- **Fix:** Used `https://github.com/bettercap/bettercap` (GitHub repo, 200) as canonical reference for NET-03 and NET-04 bettercap entries
- **Files modified:** docs/REFERENCES.md (row URL), SCENARIOS.md (NET-03, NET-04 blocks), docs/KILL-CHAINS.md appendix
- **No commit needed:** Applied during initial write, not a post-write fix

**2. [Rule 3 - Approach] HackTricks LLMNR page used for NET-01**
- **Found during:** Task 1 — no standalone HackTricks SMB relay page with 200 status found separate from the LLMNR guide
- **Fix:** The LLMNR/NBT-NS relay guide covers SMB relay detail; used it as the technique reference for NET-01
- **Impact:** None — content is equivalent

## Verification Results

| Check | Command | Result |
|-------|---------|--------|
| REFERENCES.md H3 count | `grep -c "^### " docs/REFERENCES.md` | 23 |
| SCENARIOS.md Referencias blocks | `grep -c "^### Referencias" SCENARIOS.md` | 23 |
| KILL-CHAINS.md line count | `wc -l docs/KILL-CHAINS.md` | 4280 (> 4044) |
| Original body final PASS row | `sed -n '4043p' docs/KILL-CHAINS.md` | PASS row confirmed |
| No broken URL patterns | `grep "http" docs/REFERENCES.md \| grep -v "https\?://" \| wc -l` | 0 |

## Known Stubs

None. All reference blocks contain real, verified URLs pointing to live resources.

## Threat Flags

None. No new network endpoints, auth paths, or schema changes introduced. Files are documentation-only markdown with outbound links to existing public resources.

## Self-Check: PASSED

- docs/REFERENCES.md: FOUND (294 lines, 23 H3 headings)
- SCENARIOS.md: 23 ### Referencias blocks confirmed
- docs/KILL-CHAINS.md: 4280 lines, ## Referencias at line 4047, original body intact
- All commits: c667c0a, eeb92c9, 7e180b5 confirmed in git log
