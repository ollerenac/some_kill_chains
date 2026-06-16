---
phase: 02-kill-chain-methodology-ad-network
verified: 2026-06-12T07:45:00Z
status: human_needed
score: 12/13 must-haves verified
overrides_applied: 0
human_verification:
  - test: "Run each AD kill-chain command on a live lab VM to confirm tool syntax produces the documented Expected Output"
    expected: "Each stage's Expected Output matches what the tool actually prints; no commands fail due to flag changes or API drift in certipy/nxc/impacket"
    why_human: "Documentation-only verification cannot confirm that command syntax is correct against real tool versions installed in the lab"
  - test: "Verify NET-03 single-VM topology works as described"
    expected: "A single Ubuntu 22.04 VM can run both the credential-sending client process (port 8080) and the flag service (port 80) simultaneously, and bettercap ARP poisoning of VICTIM_IP + GATEWAY_IP correctly intercepts inter-process traffic"
    why_human: "The SUMMARY documents a VM count redesign (Victim-A/Victim-B → single VM). The architectural change is plausible but has not been tested in a real lab. The ARP spoof pattern (victim + gateway) must be confirmed to intercept traffic between two processes on the same host — which is non-standard and may require a loopback override."
---

# Phase 2: Kill-Chain Methodology + AD/Network Scenarios — Verification Report

**Phase Goal:** Produce `docs/KILL-CHAINS.md` — a methodology preamble establishing the kill-chain format standard for all phases, followed by full kill-chain write-ups for all 9 AD and Network scenarios (AD-01 through AD-05, NET-01 through NET-04).
**Verified:** 2026-06-12T07:45:00Z
**Status:** human_needed
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `docs/KILL-CHAINS.md` exists and is non-empty | VERIFIED | File at `/home/researcher/Research/cont_adic/docs/KILL-CHAINS.md`, 1550 lines, 49 KB |
| 2 | `## Methodology` section present with 4 convention subsections | VERIFIED | `## Methodology` at line 12; `### 1.1` at line 14, `### 1.2` at line 48, `### 1.3` at line 70, `### 1.4` at line 88 |
| 3 | Kill-chains present for all 9 scenarios: AD-01 through AD-05, NET-01 through NET-04 | VERIFIED | All 9 headings found at lines 106, 247, 394, 570, 712, 962, 1080, 1223, 1337 |
| 4 | AD-05 has exactly two `[FLAG N]` stage headings — FLAG 1 at MemberSrv, FLAG 2 at DC | VERIFIED | `[FLAG 1] Stage 6` at line 826 (MemberSrv), `[FLAG 2] Stage 11` at line 942 (DC) |
| 5 | No other scenario has more than one flag stage | VERIFIED | `grep -c "^### \[FLAG [12]\]"` returns 10; AD-01/02/03/04 and NET-01/02/03/04 each have exactly 1 flag |
| 6 | AD-03 Stage 2 explicitly states: download SharpHound from BloodHound CE UI → Settings → Download Collectors | VERIFIED | Lines 441–442: `navigate to http://localhost:8080 → Settings → Download Collectors → SharpHound` |
| 7 | AD-02 contains Responder.conf SMB=Off/HTTP=Off warning | VERIFIED | Lines 304–307: explicit Warning block in AD-02 Stage 2 |
| 8 | AD-05 contains Responder.conf SMB=Off/HTTP=Off warning | VERIFIED | Lines 764–766: explicit Warning block in AD-05 Stage 2 |
| 9 | NET-01 contains Responder.conf SMB=Off/HTTP=Off warning | PARTIAL — see note | NET-01 has NO Responder.conf warning. The differentiator note (line 968) explains that Responder runs in analysis-only mode (`-A`) and no active poisoning occurs, which technically makes the warning inapplicable. See gap analysis below. |
| 10 | NET-02 Stage 1 ntlmrelayx command uses `ldaps://` not `ldap://` | VERIFIED | Line 1097: `-t ldaps://DC_IP`; note at lines 1119–1123 explains the TLS requirement |
| 11 | NET-04 primary approach is Scapy; dnschef is secondary/verification only | VERIFIED | Stage 3 is titled "DNS Cache Poisoning via Scapy" (line 1392); dnschef explicitly labeled "verification only" at line 1483 |
| 12 | All stage blocks have Action, Command, Expected Output, and TTP fields | VERIFIED | All four field types each appear exactly 55 times, matching the total stage count (43 numbered stages + 10 flag stages + 2 methodology template instances) |
| 13 | No Metasploit references anywhere in the document | VERIFIED | `grep -i "metasploit\|msfconsole\|use exploit/"` returns no matches |

**Score: 12/13** (Truth 9 is PARTIAL — see gap analysis)

---

### Deferred Items

None. All 9 scenarios are in scope for Phase 2 and are present in the document.

---

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `docs/KILL-CHAINS.md` | New file, full kill-chain catalog | VERIFIED | 1550 lines, exists at correct path |

---

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| Phase 2 methodology | Phase 3/4 format inheritance | Explicit statement in preamble (lines 1–8) | VERIFIED | "Phases 3 and 4 inherit the methodology section exactly as written here" |
| AD-03 kill-chain | BloodHound CE UI | Stage 2 Download Collectors instruction | VERIFIED | Lines 441–442 |
| NET-02 kill-chain | LDAPS endpoint | `-t ldaps://DC_IP` in Stage 1 command | VERIFIED | Line 1097 |
| NET-04 kill-chain | Scapy script (student-authored) | Stage 3 provides full script template | VERIFIED | Lines 1399–1460 |

---

### Data-Flow Trace (Level 4)

Not applicable. This is a documentation phase with no runnable software components. The "data" is the kill-chain content itself, verified by direct reading.

---

### Behavioral Spot-Checks

Step 7b: SKIPPED — no runnable entry points. This is a documentation-only phase producing `docs/KILL-CHAINS.md`. No API endpoints, CLI tools, or build scripts to test.

---

### Probe Execution

No probes declared in PLAN.md or SUMMARY.md. No conventional probe files found.

---

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|---------|
| AD-01 | 02-01-PLAN.md | Kerberoasting + AS-REP Roasting kill-chain | SATISFIED | Lines 106–245: 5-stage kill-chain, all MITRE TTPs present (T1087.002, T1558.003, T1558.004, T1110.002) |
| AD-02 | 02-01-PLAN.md | LLMNR/NBT-NS Poisoning and NTLM Relay kill-chain | SATISFIED | Lines 247–392: 6-stage kill-chain, T1557.001, T1021.002, Responder.conf warning present |
| AD-03 | 02-01-PLAN.md | BloodHound ACL Abuse Path kill-chain | SATISFIED | Lines 394–568: 7-stage kill-chain, SharpHound CE instruction, WriteDACL via PowerView, DCSync |
| AD-04 | 02-01-PLAN.md | ADCS ESC1 Certificate Abuse kill-chain | SATISFIED | Lines 570–710: 5-stage kill-chain, `-upn` flag in certipy req, T1649, ESC1 checklist |
| AD-05 | 02-01-PLAN.md | Conti-Style APT Chain, 2 flags | SATISFIED | Lines 712–955: 11-stage kill-chain, 2 flags at correct boundaries, dual-protocol enforcement |
| NET-01 | 02-01-PLAN.md | SMB Relay via Unsigned Shares kill-chain | SATISFIED | Lines 962–1078: 5-stage kill-chain, Responder `-A` mode, T1039 flag retrieval |
| NET-02 | 02-01-PLAN.md | IPv6 Rogue DHCPv6 and LDAP Relay kill-chain | SATISFIED | Lines 1080–1221: 5-stage kill-chain, `ldaps://`, mitm6, T1136.002 |
| NET-03 | 02-01-PLAN.md | ARP Cache Poisoning and Credential Interception kill-chain | SATISFIED | Lines 1223–1335: 4-stage kill-chain, bettercap, SSL strip, HSTS note |
| NET-04 | 02-01-PLAN.md | DNS Cache Poisoning kill-chain | SATISFIED | Lines 1337–1528: 5-stage kill-chain, Scapy script template, T1557 |

---

### SC-4 Cross-Check: Kill-Chains vs SCENARIOS.md

| Scenario | SCENARIOS.md VMs | KILL-CHAINS.md VMs | SCENARIOS.md Difficulty | KILL-CHAINS.md Difficulty | Match |
|----------|-----------------|-------------------|------------------------|--------------------------|-------|
| AD-01 | 2 | 2 (Kali + DC) | Easy | Easy | PASS |
| AD-02 | 2 | 2 (Kali + MemberSrv) | Medium | Medium | PASS |
| AD-03 | 2 | 2 (Kali + DC) | Medium | Medium | PASS |
| AD-04 | 2 | 2 (Kali + DC) | Hard | Hard | PASS |
| AD-05 | 3 | 3 (Kali + MemberSrv + DC) | Hard | Hard | PASS |
| NET-01 | 2 | 2 (Kali + Victim) | Easy | Easy | PASS |
| NET-02 | 2 | 2 (Kali + DC) | Medium | Medium | PASS |
| NET-03 | 2 | 2 (Kali + single Victim VM, two processes) | Easy | Easy | PASS — see note |
| NET-04 | 2 | 2 (Kali + DNS Resolver) | Medium | Medium | PASS |

**NET-03 note:** SCENARIOS.md specifies VMs:2. The PLAN.md template specified 3 logical roles (Attacker, Victim-A, Victim-B). The SUMMARY.md documents an auto-fix: Victim-A and Victim-B were redesigned as two processes on a single Ubuntu victim VM. KILL-CHAINS.md line 1225 explicitly states "two logical endpoints on one VM." VM count matches SCENARIOS.md. The architectural change is documented and internally consistent — but requires human verification that the ARP spoof actually intercepts intra-host traffic (see Human Verification section).

---

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `docs/KILL-CHAINS.md` | 232, 388, 564, 697, 835, 952, 1074, 1217, 1331, 1524 | `CTF{...flag_value_placeholder...}` in Expected Output | INFO | Intentional — these are correct placeholder values for flag stages in a scenario catalog. Not stubs. |

No blocker anti-patterns found. No TBD/FIXME/XXX markers. No `return null`, `return []`, or stub implementation patterns (documentation-only file).

---

### Gap Analysis

**Truth 9 — NET-01 Responder.conf Warning:**

The PLAN acceptance criterion (line 314) states: "AD-02, AD-05, and NET-01 each contain a warning that Responder.conf must have SMB = Off and HTTP = Off before running ntlmrelayx."

The document omits this warning from NET-01. The document's own consistency table (line 1540) records this decision explicitly: "NET-01 uses analysis-only mode (`-A`); warning not required."

**Technical assessment:** The omission is technically correct. Responder's `SMB = Off` / `HTTP = Off` setting in `Responder.conf` is only relevant when Responder is running in active poisoning mode (default, no `-A` flag) simultaneously with ntlmrelayx. In that scenario, Responder's built-in SMB/HTTP servers compete with ntlmrelayx to handle the incoming authentication — Responder.conf must disable them to let ntlmrelayx win the race. In NET-01, Responder runs with `-A` (analysis only), which means Responder never responds to queries and never has SMB/HTTP listeners competing with ntlmrelayx. Including the Responder.conf warning in NET-01 would be misleading to students.

**Verdict:** The PLAN criterion was overcautious and slightly incorrect about NET-01. The document's choice is technically superior. This is a WARNING (plan deviation), not a BLOCKER (implementation error). The differentiator note at line 968 explains the relevant distinction to students.

This deviation is eligible for an override. To accept it formally, add to this file's frontmatter:

```yaml
overrides:
  - must_have: "NET-01 contains Responder.conf SMB=Off/HTTP=Off warning"
    reason: "NET-01 uses Responder -A (analysis-only mode); Responder.conf SMB/HTTP setting is irrelevant when Responder does not respond to queries. The differentiator note at line 968 explains this to students. Including the warning would be technically misleading."
    accepted_by: "oscar.llerena.c@gmail.com"
    accepted_at: "2026-06-12T07:45:00Z"
```

---

### Human Verification Required

#### 1. Lab Command Syntax Validation

**Test:** For each of the 9 kill-chains, run the Stage 1 command against a live lab VM to confirm the expected output matches what the tool actually produces.
**Expected:** Commands execute without errors; Expected Output snippets are representative of real tool output.
**Why human:** This is documentation. Grep and file checks can verify that commands are present and follow the ALLCAPS placeholder convention, but cannot confirm the tool syntax is correct against the specific versions installed in the lab environment. Certipy v5, nxc, impacket, and bettercap all have histories of flag renames between versions.

#### 2. NET-03 Single-VM ARP Topology

**Test:** Deploy the NET-03 scenario with a single Ubuntu 22.04 victim VM running both the credential-sender process (port 8080) and the flag service (port 80). From the Kali attacker VM, execute the bettercap ARP spoof targeting `VICTIM_IP` and `GATEWAY_IP` (line 1270), enable SSL strip, and confirm that the credential POST from the credential-sender process to the flag service is captured.
**Expected:** bettercap `net.sniff` output shows `POST /login ... username=admin&password=FLAG_PASSWORD` from the victim's own process.
**Why human:** The redesign (documented in SUMMARY.md as an "auto-fix") moves from the PLAN's 3-role topology (Attacker + Victim-A + Victim-B) to a 2-VM topology where Victim-A and Victim-B are co-located on one host. ARP cache poisoning of a host vs. its own gateway is well-understood, but capturing inter-process traffic on the same host via ARP-based MITM is an unusual topology that depends on whether the credential-sender and flag service communicate over the network stack (routable through the gateway) or directly on loopback. This requires empirical verification.

---

## Summary

`docs/KILL-CHAINS.md` is substantive, complete, and technically correct. All 9 kill-chains are fully written with the four mandatory fields on every stage. All MITRE TTPs are cited with inline hyperlinks. AD-05 has exactly two flag stages at the correct lateral movement boundaries. No Metasploit references. No debt markers.

One plan acceptance criterion is unmet on its literal terms (NET-01 Responder.conf warning) but the deviation is technically defensible and documented by the author. Two items require human lab verification before the document is ready for instructor handoff: command syntax validation against real tool versions, and NET-03 ARP topology confirmation following the 2-VM redesign.

---

_Verified: 2026-06-12T07:45:00Z_
_Verifier: Claude (gsd-verifier)_
