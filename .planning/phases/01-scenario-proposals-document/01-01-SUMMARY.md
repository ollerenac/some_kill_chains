---
phase: 01-scenario-proposals-document
plan: 01
subsystem: documentation
tags: [ctf, scenarios, active-directory, network-protocols, cve, cloud, container, llm, atp, kerberoasting, bloodhound, certipy, responder, mitm6, eternalblue, log4shell, spring4shell, printnightmare, docker, kubernetes, prompt-injection]

# Dependency graph
requires: []
provides:
  - "SCENARIOS.md — complete 23-scenario CTF catalog for user review and approval"
  - "Second-person attack narratives for all 6 domains (AD:5, NET:4, CVE:4, CC:3, LLM:3, ATP:4)"
  - "Multi-step tagging on AD-05 and all four ATP chains"
affects: [02-kill-chains, 03-cve-kill-chains, 04-llm-atp-kill-chains]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Entry format: ### [ID]: [Title] / **Difficulty:** / **VMs:** / 3-5 sentence second-person narrative"
    - "Multi-step tag: [Multi-step — 2 flags] appended to H3 heading for ATP scenarios and AD-05"
    - "CVE narrative pattern: frames student as exploit author, not tool runner"
    - "ATP narrative pattern: midpoint sentence signals Flag 1, second half describes continuation to Flag 2"

key-files:
  created:
    - SCENARIOS.md
  modified: []

key-decisions:
  - "CVE-04 title references both CVE-2021-1675 (LPE) and CVE-2021-34527 (RCE) per RESEARCH.md Pitfall 1 Option C — describes LPE path for 2-VM standalone design"
  - "CC-02 narrative avoids naming 'release_agent' per RESEARCH.md Pitfall 4 — frames as privileged container + host kernel interfaces + cgroup notification path"
  - "OWASP LLM category numbers excluded from all narratives per RESEARCH.md Pitfall 2 — attack mechanisms described in plain language only"
  - "Metasploit mentioned once in intro as exclusion constraint — not in any scenario narrative"

patterns-established:
  - "SCENARIOS.md entry format: H3 heading with ID, optional multi-step tag, Difficulty, VMs, 3-5 sentence second-person narrative"
  - "Scenario narrative rule: name key tools (Responder, BloodHound, Certipy, Rubeus, Hashcat, mitm6, evil-winrm, kubectl) when the tool IS the learning point; omit generic tools (nmap, curl)"
  - "CVE authorship framing: 'you author a Python exploit', 'you write the weaponization function', 'rather than reaching for an automated framework, you craft'"

requirements-completed:
  - AD-01
  - AD-02
  - AD-03
  - AD-04
  - AD-05
  - NET-01
  - NET-02
  - NET-03
  - NET-04
  - CVE-01
  - CVE-02
  - CVE-03
  - CVE-04
  - CC-01
  - CC-02
  - CC-03
  - LLM-01
  - LLM-02
  - LLM-03
  - ATP-01
  - ATP-02
  - ATP-03
  - ATP-04

# Metrics
duration: 8min
completed: 2026-06-11
---

# Phase 1 Plan 01: Scenario Proposals Document Summary

**23 CTF scenario proposals authored across 6 domains with second-person attack narratives, correct CVE numbers, multi-step tagging, and all content guards satisfied**

## Performance

- **Duration:** ~8 min
- **Started:** 2026-06-11T16:25:00Z
- **Completed:** 2026-06-11T16:33:32Z
- **Tasks:** 1/1
- **Files modified:** 1

## Accomplishments

- Authored SCENARIOS.md with all 23 scenario entries across 6 domains (AD:5, NET:4, CVE:4, CC:3, LLM:3, ATP:4) in the locked D-06 entry format
- Applied correct multi-step tag on exactly 5 entries: AD-05 and ATP-01 through ATP-04
- Applied all RESEARCH.md pitfall mitigations: CVE-04 references both CVE-2021-1675 and CVE-2021-34527 with LPE framing; CC-02 avoids "release_agent"; no OWASP LLM category numbers in any narrative

## Task Commits

Each task was committed atomically:

1. **Task 1: Author all 23 scenario entries and write SCENARIOS.md** - `3030b44` (feat)

**Plan metadata:** (this commit)

## Files Created/Modified

- `SCENARIOS.md` — Complete 23-scenario CTF catalog with intro section, 6 domain sections, all entries in D-06 format; self-contained for any reviewer who has not read REQUIREMENTS.md

## Decisions Made

- Applied RESEARCH.md Pitfall 1 Option C for CVE-04: title references both "CVE-2021-1675 / CVE-2021-34527" and narrative describes the LPE path (low-privileged session → SYSTEM via RpcAddPrinterDriverEx), consistent with 2-VM standalone design
- Applied RESEARCH.md Pitfall 4 for CC-02: narrative uses "cgroup notification path" rather than naming "release_agent", keeping the description platform-agnostic at the proposals stage
- Applied RESEARCH.md Pitfall 2 for LLM scenarios: no OWASP LLM Top 10 category numbers cited in any narrative; attack mechanisms described in plain language
- NET-03 uses bettercap as the named tool anchor (per plan spec "pick one as the tool anchor")
- ATP-02 uses dnscat2 as the DNS tunneling tool anchor (per plan spec "pick one")

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None. All 23 acceptance criteria assertions passed:
- `grep -c "^### " SCENARIOS.md` → 23
- `grep -c "^### AD-" SCENARIOS.md` → 5
- `grep -c "^### NET-" SCENARIOS.md` → 4
- `grep -c "^### CVE-" SCENARIOS.md` → 4
- `grep -c "^### CC-" SCENARIOS.md` → 3
- `grep -c "^### LLM-" SCENARIOS.md` → 3
- `grep -c "^### ATP-" SCENARIOS.md` → 4
- `grep -c "Multi-step" SCENARIOS.md` → 5
- `grep -cP "T\d{4}" SCENARIOS.md` → 0 (no MITRE TTP codes)
- `grep -c "release_agent" SCENARIOS.md` → 0 (CC-02 pitfall avoided)
- `grep -c "CVE-2021-1675" SCENARIOS.md` → 1
- `grep -c "CVE-2021-34527" SCENARIOS.md` → 1
- `grep -c "Metasploit" SCENARIOS.md` → 1 (intro section only)
- `grep -c "\*\*Difficulty:\*\*" SCENARIOS.md` → 23
- `grep -c "\*\*VMs:\*\*" SCENARIOS.md` → 23
- `grep -cP "^\d+\." SCENARIOS.md` → 0 (no numbered kill-chain steps)

## User Setup Required

None — no external service configuration required. This is a documentation phase.

## Next Phase Readiness

- SCENARIOS.md is ready for end-to-end user review and approval
- User reads the document and approves, revises, or rejects individual entries
- Phase 2 (kill-chain authoring) begins only after explicit user approval of SCENARIOS.md
- No blockers; all 23 scenario entries meet the acceptance criteria defined in the plan

## Known Stubs

None — SCENARIOS.md is a complete proposals document. All 23 entries have title, metadata, and full 3-5 sentence narratives. No placeholder text or TODO markers present.

## Threat Flags

None — this phase produces a static Markdown document with no new network endpoints, auth paths, file access patterns, or schema changes at trust boundaries.

## Self-Check: PASSED

- SCENARIOS.md exists: FOUND at `/home/researcher/Research/cont_adic/SCENARIOS.md` (worktree copy)
- Task commit 3030b44: confirmed in git log
- All 16 grep-based acceptance criteria assertions: PASSED (verified above)

---
*Phase: 01-scenario-proposals-document*
*Completed: 2026-06-11*
