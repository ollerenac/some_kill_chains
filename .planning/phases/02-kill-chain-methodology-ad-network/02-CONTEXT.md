---
phase: 02
phase_name: Kill-Chain Methodology + AD/Network Scenarios
mode: mvp
status: planning
---

# Phase 2 Context

## Goal

A methodology section establishing the kill-chain format and TTP notation standard,
followed by fully detailed kill-chain write-ups for all 9 AD and Network scenarios
(AD-01..05, NET-01..04). These are the most technically mature domains and establish
the template all subsequent phases follow.

## Output Artifact

`docs/KILL-CHAINS.md` — a single document containing:
1. A methodology preamble (kill-chain stage format, TTP citation style, flag
   placement conventions, VM role labeling)
2. Full kill-chain write-ups for: AD-01, AD-02, AD-03, AD-04, AD-05, NET-01,
   NET-02, NET-03, NET-04

## Requirements in Scope

AD-01, AD-02, AD-03, AD-04, AD-05, NET-01, NET-02, NET-03, NET-04

## Success Criteria (from ROADMAP.md)

1. A methodology section defines the kill-chain stage format, MITRE ATT&CK TTP
   citation style, flag placement conventions, and VM role labeling — all subsequent
   phases use this format without deviation
2. All 9 AD/Network scenarios have complete kill-chain write-ups: numbered stages,
   attacker actions, expected outputs, and at least one MITRE TTP code per stage
3. The two multi-step ATP scenarios in this set (AD-05) have Flag 1 and Flag 2
   placements explicitly marked at the correct lateral movement boundaries
4. Each kill-chain is internally consistent with the scenario description written
   in Phase 1

## Locked Decisions (Inherited from Phase 1)

| ID | Decision | Impact on Phase 2 |
|----|----------|-------------------|
| D-CVE04 | CVE-04 uses LPE path (CVE-2021-1675 / CVE-2021-34527 in title) | Phase 3 concern — but establishes the "dual-CVE title" pattern if used in Phase 2 methodology examples |
| D-CC02 | CC-02 escape uses "cgroup notification path"; cgroup v1 required | Phase 3 concern — no impact on Phase 2 AD/NET kill-chains |
| D-ATP04 | ATP-04 is NOT true LotL; mitm6/ntlmrelayx/evil-winrm are external attacker tools | Phase 4 concern — methodology must not define these as LotL |
| D-BLOODHOUND | BloodHound CE only; CE-compatible SharpHound collectors required | AD-03 kill-chain must specify CE-compatible SharpHound |
| D-OWASP | OWASP LLM Top 10 2025 IDs for citation | Phase 4 concern — not in Phase 2 scope |

## Phase 2 Decisions to Define

The researcher and planner must converge on:

1. **Kill-chain stage format**: What fields each stage entry contains
   - Candidates: Stage number + name, attacker action, command(s), expected output,
     MITRE TTP code(s), notes
2. **TTP citation style**: How MITRE ATT&CK codes are cited
   - Candidates: inline (T1558.003), parenthetical at end of stage, dedicated TTP
     table per scenario
3. **Flag placement convention**: How flags are marked in kill-chains
   - Candidates: `[FLAG 1]` inline marker, dedicated "Flag" field per stage, end-of-
     kill-chain summary table
4. **VM role labeling**: How VMs are referenced
   - Candidates: Attacker/Victim, VM1/VM2/VM3, role names (Kali/DC/Member)

## Constraints

- No Metasploit at any stage — even in examples
- Max 3 VMs per scenario
- All tool references must use current tools (nxc not cme, BloodHound CE not legacy)
- AD-05 is the only multi-step scenario in this phase; Flag 1 at SMB relay foothold,
  Flag 2 at DC via WinRM
- Kill-chain format established here is the standard for Phases 3 and 4 — get it right

## Deferred Ideas (Out of Scope)

- Kill-chains for CVE, CC, LLM, ATP scenarios → Phase 3 and 4
- VM build specifications → Phase 3
- Student-facing lab guides → out of roadmap scope entirely
