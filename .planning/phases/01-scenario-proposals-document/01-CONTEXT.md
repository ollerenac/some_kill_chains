# Phase 1: Scenario Proposals Document - Context

**Gathered:** 2026-06-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Produce `SCENARIOS.md` — a single, self-contained proposals document containing all 23 scenario entries organized by domain. Each entry has a title, difficulty rating, VM count, multi-step flag (where applicable), and a 3–5 sentence attack narrative written in second person. No kill-chain steps, no MITRE TTP codes, no implementation details. This document is the artifact the user reads end-to-end and approves before Phase 2 begins.

</domain>

<decisions>
## Implementation Decisions

### Scenario List
- **D-01:** Keep all 23 scenarios — no trimming. The original brief said ~20; the extra 3 add domain coverage without violating VM constraints.
- **D-02:** NET-01 (SMB relay) and AD-02 (LLMNR poisoning → relay) are distinct enough to coexist. NET-01 emphasizes network-layer SMB signing misconfiguration; AD-02 emphasizes LLMNR/NBT-NS broadcast poisoning in an AD identity context. Keep both as written.

### Description Depth
- **D-03:** Each scenario description is **attack narrative only** — no learning objectives, no VM role labels inside the description text. 3–5 sentences describing what the student sees, does, and obtains.
- **D-04:** Write descriptions in **second person** ("You are a red-team operator. Your objective is to..."). Immersive CTF challenge style, not a clinical third-person summary.
- **D-05:** **Name key tools when the tool IS the learning point** (e.g., "using Responder", "with BloodHound", "via Certipy"). Skip generic/universal tools (nmap, curl, netcat) — they don't define the scenario.

### Metadata Per Entry
- **D-06:** Each scenario entry shows: **title + difficulty rating + VM count + description**. That is the complete entry structure.
- **D-07:** Multi-step ATP scenarios (those with 2 flags and lateral movement) are visually tagged with `[Multi-step — 2 flags]` adjacent to the title so reviewers immediately recognize the more complex structure.

### Document Structure
- **D-08:** The document opens with a **brief intro section** (3–5 lines) stating the catalog purpose, the max-3-VM constraint, and the no-Metasploit constraint. Makes the document self-contained for any reviewer who hasn't read REQUIREMENTS.md.
- **D-09:** Scenarios are **organized by domain** (same as REQUIREMENTS.md): Active Directory / Windows, Network Protocol Exploitation, CVE Weaponization, Cloud / Container Security, LLM Security, Multi-Step ATP Chains.

### Review Workflow
- **D-10:** Review is **wholesale** — user reads end-to-end and then approves or requests targeted edits. No per-scenario status markers, checkboxes, or inline annotation fields needed. Phase 2 starts only after explicit approval.

### Claude's Discretion
- Exact wording of the intro section preamble (content is locked by D-08; phrasing is open).
- Ordering of scenarios within each domain section (alphabetical by ID or narrative flow order — either is fine).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Scenario Definitions
- `.planning/REQUIREMENTS.md` — Authoritative list of all 23 scenarios with their ID, difficulty, VM count, and 1-sentence requirement descriptions. The executor expands each entry into the 3–5 sentence narrative format defined by D-03–D-05. Do not invent new scenarios or drop existing ones.

### Phase Goal and Success Criteria
- `.planning/ROADMAP.md` — Phase 1 success criteria: all 23 scenarios present, correct domain counts (AD: 5, NET: 4, CVE: 4, CC: 3, LLM: 3, ATP: 4), no kill-chain steps in any description, user can make approve/revise/reject decisions per scenario without additional context.

### Project Constraints
- `.planning/PROJECT.md` — Core constraints: max 3 VMs per scenario, no Metasploit, no duplication of existing lab topics (Crypto, Web-Hacking, Forensics, System-Hacking, Malware, ISMS, Reversing).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None — this is a new documentation project with no prior artifacts to reuse.

### Established Patterns
- None yet — SCENARIOS.md is the first deliverable. Its structure becomes the pattern all subsequent scenario documents follow.

### Integration Points
- `SCENARIOS.md` must be self-consistent with `.planning/REQUIREMENTS.md` (same 23 scenario IDs, same difficulty/VM-count metadata). If any scenario is revised during authoring, REQUIREMENTS.md must be updated to match.

</code_context>

<specifics>
## Specific Ideas

- The student-POV framing comes from the CTF challenge writing style used in the existing lab framework — match that register.
- For CVE scenarios, the description should convey that the student *authors* the exploit code (not runs a tool) — this is the key differentiator and pedagogical hook for those entries.
- For ATP multi-step scenarios, the description should convey the chain structure (first hop → flag 1 → second hop → flag 2) without naming specific TTPs.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 1-Scenario Proposals Document*
*Context gathered: 2026-06-11*
