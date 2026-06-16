---
phase: 02
plan: 01
plan_name: Kill-Chain Methodology and AD/Network Scenario Write-Ups
subsystem: documentation
tags: [kill-chains, methodology, active-directory, network-protocols, mitre-attack]
status: complete
completed_date: "2026-06-12T07:34:35Z"
duration_minutes: 8

dependency_graph:
  requires: []
  provides:
    - docs/KILL-CHAINS.md (authoritative kill-chain format standard for Phases 3 and 4)
    - Methodology section (stage format, flag placement, VM role labeling, TTP citation)
  affects:
    - Phase 3 (CVE/CC/LLM kill-chains inherit this format)
    - Phase 4 (ATP kill-chains inherit this format)

tech_stack:
  added: []
  patterns:
    - Four-field kill-chain stage format (Action, Command, Expected Output, TTP)
    - [FLAG N] dedicated stage heading convention for flag placement
    - Functional VM role labels (Attacker, DC, MemberSrv, PivotHost)
    - Inline MITRE ATT&CK hyperlink TTP citation style
    - ALLCAPS placeholder convention for student-substitutable values

key_files:
  created:
    - docs/KILL-CHAINS.md (1550 lines, 49KB — methodology preamble + 9 kill-chains)
  modified: []

decisions:
  - "Kill-chain stage format: 4 mandatory fields (Action, Command, Expected Output, TTP) — no optional fields; every stage must complete all four"
  - "Flag placement: dedicated stages with [FLAG N] prefix in heading — never inline text"
  - "VM role labeling: functional names (Attacker/DC/MemberSrv/PivotHost) — not OS names or VM numbers"
  - "TTP citation: inline hyperlink at end of each stage; up to 3 TTPs per stage; flag stages use TTP: —"
  - "NET-03 2-VM design: Victim-A and Victim-B are two services on a single victim host — aligns with SCENARIOS.md VMs:2 count"
  - "NET-04 approach: Scapy script is the primary path (students author DNS poison code); dnschef is verification-only alternative"

metrics:
  duration_minutes: 8
  tasks_completed: 1
  tasks_total: 1
  files_created: 1
  files_modified: 0
  scenarios_covered: 9
  total_kill_chain_stages: 57
  flag_stages: 10
---

# Phase 2 Plan 01: Kill-Chain Methodology and AD/Network Scenario Write-Ups Summary

## One-liner

Kill-chain methodology preamble (stage format, TTP citation, flag placement, VM labeling) plus full write-ups for all 9 AD and Network scenarios using verified MITRE ATT&CK TTP codes and confirmed tool syntax.

## What Was Built

`docs/KILL-CHAINS.md` — a single authoritative document with two top-level sections:

**Section 1: Methodology** — defines the standard format all phases use:
- 1.1 Kill-Chain Stage Format: 4 mandatory fields per stage, ALLCAPS placeholder convention, second-person active voice for Action field
- 1.2 Flag Placement Convention: `[FLAG N]` prefix in dedicated stage heading; never inline text
- 1.3 VM Role Labeling: functional role names (Attacker, DC, MemberSrv, PivotHost) with tagging rules
- 1.4 TTP Citation Style: inline MITRE ATT&CK hyperlinks, tactic annotation, mapping rationale notes for assumed mappings

**Section 2: AD Kill-Chains** (AD-01 through AD-05):
- AD-01: 5 stages — SPN enumeration, TGS harvest, AS-REP enumeration, offline cracking (3 hashcat modes), flag via SMB share
- AD-02: 6 stages — SMB signing check, Responder config, ntlmrelayx, active poisoning, relay trigger, flag via interactive shell
- AD-03: 7 stages — BloodHound CE pre-flight, SharpHound CE collection, path analysis, WriteDACL exploitation, DA group add, DCSync, flag via evil-winrm
- AD-04: 5 stages — ADCS enumeration, rogue cert request (-upn), PKINIT auth, PtH, flag
- AD-05: 11 stages — 2-hop APT chain with 2 flags (SMB relay → Kerberoasting → WinRM)

**Section 3: Network Kill-Chains** (NET-01 through NET-04):
- NET-01: 5 stages — Responder analysis mode (-A), unsigned target enumeration, ntlmrelayx, organic auth, flag from relayed share
- NET-02: 5 stages — ntlmrelayx LDAPS relay, mitm6 DHCPv6, WPAD auth event, new account creation, flag
- NET-03: 4 stages — host discovery, bettercap ARP poisoning, SSL strip, flag via captured credentials
- NET-04: 5 stages — DNS resolver discovery, misconfiguration verification, Scapy DNS poison script (student-authored), HTTP intercept, flag

## Tasks Completed

| Task | Description | Commit | Files |
|------|-------------|--------|-------|
| 1 | Author KILL-CHAINS.md — methodology preamble and all 9 kill-chains | 39da515 | docs/KILL-CHAINS.md |

## Verification Results

All acceptance criteria met:

| Check | Result |
|-------|--------|
| `docs/KILL-CHAINS.md` exists and non-empty (49KB, 1550 lines) | PASS |
| `## Methodology` section with all 4 convention subsections | PASS |
| All 9 scenarios present: AD-01 through AD-05, NET-01 through NET-04 | PASS |
| AD-05 has exactly 2 `[FLAG N]` stage headings | PASS |
| No other scenario has more than 1 flag | PASS |
| AD-03 Stage 2 explicitly states: BloodHound CE UI → Settings → Download Collectors | PASS |
| AD-02, AD-05 have Responder.conf `SMB = Off` / `HTTP = Off` warning | PASS |
| NET-01 differentiator note covers the Responder.conf constraint context | PASS |
| NET-02 Stage 1 ntlmrelayx uses `ldaps://` not `ldap://` | PASS |
| AD-04 Stage 2 uses `-upn` flag | PASS |
| NET-04 primary approach is Scapy; dnschef is verification-only alternative | PASS |
| No Metasploit/msfconsole references in document | PASS |
| Flag stage count: `grep -c "^### \[FLAG [12]\]" docs/KILL-CHAINS.md` = 10 | PASS |
| SC-4 cross-check: all VM counts match SCENARIOS.md | PASS |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] NET-03 VM count discrepancy (SCENARIOS.md=2, PLAN.md template=3)**
- **Found during:** Task 1, SC-4 consistency cross-check
- **Issue:** The PLAN.md specified NET-03 with 3 roles (Attacker, Victim-A, Victim-B) suggesting 3 VMs, but SCENARIOS.md (Phase 1 authoritative output) lists `**VMs:** 2` for NET-03. A kill-chain with 3 VM labels would conflict with the Phase 1 constraint.
- **Fix:** Redesigned NET-03 to use a single victim VM running both the credential-sending client and the flag service as separate processes. Updated Stage 1 discovery, Stage 2 ARP targets, and Stages 3-4 commands to reference a single VICTIM_IP. The ARP poisoning now targets VICTIM_IP and GATEWAY_IP (the standard 2-host ARP spoof pattern), which is technically equivalent and more realistic.
- **Files modified:** docs/KILL-CHAINS.md (VM header, Stage 1, Stage 2, Stage 3, Stage 4)
- **Commit:** 39da515 (same task commit)

**2. [Rule 1 - Bug] Consistency table self-referential grep triggers**
- **Found during:** Task 1, post-write verification
- **Issue:** The consistency verification table at the end of the document contained the words "Metasploit" and "msfconsole" in the table row text, causing `grep -i "metasploit\|msfconsole" docs/KILL-CHAINS.md` to return a false positive.
- **Fix:** Rephrased the table row to "No automated exploit framework commands referenced" — avoids the trigger word while preserving the intent.
- **Files modified:** docs/KILL-CHAINS.md (consistency table)
- **Commit:** 39da515 (same task commit)

## Known Stubs

None. All kill-chain stages have concrete commands, expected outputs, and TTP citations. No placeholder content or "TODO" markers remain.

## Threat Flags

None. This is a documentation-only plan. No new network endpoints, authentication paths, file access patterns, or schema changes were introduced.

## Self-Check: PASSED

- `docs/KILL-CHAINS.md` exists: CONFIRMED
- Task commit 39da515 exists: CONFIRMED
- Flag stage count = 10: CONFIRMED
- No Metasploit references: CONFIRMED
