---
status: issues_found
phase: 02-kill-chain-methodology-ad-network
files_reviewed: 1
findings:
  critical: 3
  warning: 1
  info: 0
  total: 4
reviewed: 2026-06-12
---

# Code Review — Phase 02: Kill-Chain Methodology and AD/Network Scenarios

**File reviewed:** `docs/KILL-CHAINS.md`
**Depth:** standard

---

## Summary

3 critical issues found (documentation correctness / student-facing bugs), 1 warning (false self-check claim). No Metasploit references. Flag counts correct (10 total, AD-05 has 2). All stage four-field requirement met. LDAPS, SharpHound CE note, and Responder.conf warnings verified.

---

## Critical Issues

### CR-01 — [Attacker] label description is inverted in methodology table

**File:** `docs/KILL-CHAINS.md:76`
**Severity:** Critical
**Confidence:** 95%

**Issue:** The `[Attacker]` row reads "Only when a stage command runs on the victim; omit the tag if all commands in the stage run on the attacker." This is the inverse of the intended meaning. All other rows say "When the command executes on [role]" — meaning the tag marks where the command runs. As written, the rule tells students to apply `[Attacker]` for victim-side execution and omit it for attacker-side execution, which contradicts the entire purpose of the tag.

**Fix:** Change to: `Only when all commands in the stage run on the attacker VM; omit the tag — the attacker is the default unlabeled execution context.`

---

### CR-02 — AD-05 Stage 8: Wrong VM role label `[MemberSrv]` on attacker-side command

**File:** `docs/KILL-CHAINS.md:868`
**Severity:** Critical
**Confidence:** 90%

**Issue:** Stage heading `#### Stage 8: Hash Exfiltration [MemberSrv]` — but the command (`smbclient \\\\MEMBERSRV_IP\\C$`) runs from the attacker Kali machine pulling a file from MemberSrv, not executing on MemberSrv. Per methodology 1.3, labels appear only when the command executes on the labeled machine. `[MemberSrv]` incorrectly signals that the student should run this on the Windows server.

**Fix:** Remove `[MemberSrv]` from the Stage 8 heading.

---

### CR-03 — AD-05 Stage 8: Wrong TTP — T1041 does not describe SMB file pull

**File:** `docs/KILL-CHAINS.md:887`
**Severity:** Critical
**Confidence:** 88%

**Issue:** `T1041 — Exfiltration Over C2 Channel` describes data exfiltrated through an established C2 channel. The action is a direct `smbclient` pull from a compromised Windows SMB share — no C2 channel exists. NET-01 Stage 5 performs the identical pattern and correctly cites `T1039 — Data from Network Shared Drive`, making this an internal inconsistency as well.

**Fix:** Replace `T1041 — Exfiltration Over C2 Channel` with `[T1039 — Data from Network Shared Drive](https://attack.mitre.org/techniques/T1039/) · Collection`

---

## Warning

### WR-01 — Consistency checklist NET-01 Responder warning claim is inaccurate

**File:** `docs/KILL-CHAINS.md:1540`
**Severity:** Warning
**Confidence:** 85%

**Issue:** Checklist row claims the Responder.conf `SMB=Off/HTTP=Off` warning appears in NET-01. It does not — NET-01's differentiator note describes analysis mode behavior but contains no Responder.conf configuration warning. The warning is not needed in NET-01 (which uses `-A` mode and has no ntlmrelayx relay setup), but the PASS claim is factually false.

**Fix:** Update checklist entry to: `Responder.conf SMB=Off/HTTP=Off warning appears in AD-02 and AD-05 (active poisoning + relay scenarios) | PASS — AD-02 Stage 2, AD-05 Stage 2. NET-01 uses analysis-only mode; warning not required.`

---

## Passing Checks

- No `metasploit`, `msfconsole`, or `msfvenom` references found
- Flag count: 10 total (`grep -c "^### \[FLAG [12]\]"`) — AD-05 has 2, all others have 1
- All 9 scenario kill-chains present (AD-01 through AD-05, NET-01 through NET-04)
- Every stage has all four fields: Action, Command, Expected Output, TTP
- ALLCAPS placeholder convention followed throughout
- All TTP hyperlinks use `https://attack.mitre.org/techniques/T####/` format
- NET-02 Stage 1 uses `ldaps://` not `ldap://`; LDAPS note present
- AD-03 Stage 2 SharpHound CE-only warning correctly placed
- AD-02 Stage 2 and AD-05 Stage 2 carry Responder.conf `SMB=Off/HTTP=Off` warning
- T1222.001 and T1557.001 assumed-mapping notes present with rationale
- AD-04 Stage 2 certipy command uses `-upn` flag
- NET-04 primary path is student-authored Scapy; dnschef documented as verification-only
- VM role labels `[DC]`, `[MemberSrv]`, `[PivotHost]` correctly applied in all stages except CR-02
- Methodology section precedes all kill-chains; document opens with purpose summary
