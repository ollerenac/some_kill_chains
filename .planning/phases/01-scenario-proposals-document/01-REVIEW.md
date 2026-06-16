---
phase: 01-scenario-proposals-document
reviewed: 2026-06-11T16:45:00Z
depth: standard
files_reviewed: 1
files_reviewed_list:
  - SCENARIOS.md
findings:
  critical: 2
  warning: 4
  info: 2
  total: 8
status: issues_found
---

# Phase 01: Code Review Report

**Reviewed:** 2026-06-11T16:45:00Z
**Depth:** standard
**Files Reviewed:** 1
**Status:** issues_found

---

## Summary

SCENARIOS.md delivers all 23 required scenario entries across the 6 mandated domains with correct per-domain counts (AD: 5, NET: 4, CVE: 4, CC: 3, LLM: 3, ATP: 4). All structural acceptance criteria pass mechanically: exactly 23 H3 headers, 23 `**Difficulty:**` lines, 23 `**VMs:**` lines, 5 multi-step tags on the correct entries, zero MITRE TTP codes, zero `release_agent` occurrences, both CVE-2021-1675 and CVE-2021-34527 present in the CVE-04 title, and Metasploit mentioned only in the intro constraint statement.

Two content-accuracy defects require correction before instructor approval: ATP-04 makes a factually false "living-off-the-land" claim while naming tools that are the antithesis of LotL, and NET-03 asserts TLS stripping over connections already described as HTTP — a self-contradictory statement that would confuse students. Four warnings cover a Phase 2 implementation detail exposed in CVE-04, a kill-chain-stage structure in AD-05, a technical imprecision in NET-03's transport description, and an ATP/APT acronym inconsistency. Two info items cover a minor inline-code formatting inconsistency and a sentence-count edge case.

---

## Critical Issues

### CR-01: ATP-04 "Living-Off-the-Land" Claim Is Factually Incorrect

**File:** `SCENARIOS.md:222`
**Issue:** The narrative opens with "no malware, no custom binaries, no lateral tooling beyond what the environment provides" and closes with "without executing a single piece of malware from start to finish." It then explicitly names mitm6, ntlmrelayx, and evil-winrm — all external attacker-side Python/Ruby tools that are not native to any Windows domain environment. Living-off-the-land (LotL) in the Volt Typhoon context means using operating-system-native administration tools (WMI, netsh, PowerShell built-ins, certutil) to avoid dropping foreign binaries. Students who read this scenario and research Volt Typhoon's actual TTPs will immediately see the contradiction. The claim is not just imprecise — it is directly falsified by the tools named in the same sentence.

**Fix:** Replace the LotL framing with accurate language that describes what the scenario actually constrains: no malware, no shellcode, no compiled payloads. Example reframing:

> You operate under a no-malware constraint — no compiled payloads, no shellcode, no persistent implants. Using mitm6 to deploy a rogue DHCPv6 server and relaying the resulting authentication attempts to LDAP via ntlmrelayx, you create a new privileged domain account without touching the filesystem of any target host. With the new account, you use evil-winrm to authenticate to a domain member server and retrieve the first flag. From the pivot, you enumerate service account SPNs with Kerberoasting, crack the recovered ticket hash offline, and use the resulting credential with a second lateral movement protocol to authenticate to the domain controller and retrieve the final flag — the entire chain executed without dropping a single malicious file.

---

### CR-02: NET-03 Describes TLS Stripping Over HTTP — Self-Contradictory

**File:** `SCENARIOS.md:79`
**Issue:** The narrative states "You strip transport-layer protection from HTTP connections." HTTP connections carry no transport-layer protection; stripping is the technique used to downgrade HTTPS to HTTP. The sentence as written is technically meaningless — you cannot strip protection that is not present. A student reading this will either be confused about what the scenario requires or will conclude the scenario involves HTTPS (which the rest of the narrative does not confirm). The REQUIREMENTS.md entry for NET-03 specifies "strips HTTPS via sslstrip or SSLsplit," which is the correct technique — HTTPS downgrade to HTTP. The narrative dropped HTTPS and the explicit sslstrip/SSLsplit tool reference, producing an inaccurate description.

**Fix:** Restore the correct HTTPS-downgrade framing and name the stripping mechanism:

> You are on the same Layer 2 segment as two communicating hosts and must intercept their traffic. Using bettercap, you send gratuitous ARP replies to poison the ARP caches of both targets, routing their traffic through your machine and positioning yourself as the man-in-the-middle. You exploit bettercap's HTTPS proxy to downgrade encrypted connections to plaintext HTTP, capturing the credentials transmitted by the hosts and using them to retrieve the flag.

---

## Warnings

### WR-01: CVE-04 Narrative Exposes Win32 API Name — Phase 2 Implementation Detail

**File:** `SCENARIOS.md:126`
**Issue:** The narrative names the specific Windows API function ``RpcAddPrinterDriverEx`` in backtick code formatting. The plan's authoring rules explicitly state "No commands or syntax" in Phase 1 narratives, and the rationale for the proposals document is to describe what the student does and obtains — not how at the API level. Naming the precise RPC call crosses the line from "attack narrative" into "implementation specification." An instructor reviewer cannot distinguish this from Phase 2 kill-chain content. The plan's scenario-specific note for CVE-04 mentions this function name as the mechanism to convey, but does not require it to be rendered as inline code in the proposal.

**Fix:** Replace the API-level specification with mechanism-level language, and remove the backtick code formatting:

> You author a C or Python payload that instructs the Windows Print Spooler service — which runs as SYSTEM — to load a malicious DLL you supply, injecting your code into a SYSTEM-level process.

---

### WR-02: AD-05 Uses Explicit Phase/Stage Labels That Mirror Kill-Chain Structure

**File:** `SCENARIOS.md:50`
**Issue:** The narrative uses "In the first phase" and "you shift to the second phase" as structural labels dividing the two flag segments. The authoring rules prohibit "numbered steps, bullet points, or kill-chain stages." While these labels are not numbered (no "1." or "2."), the explicit "first phase / second phase" division is functionally equivalent to a two-stage kill-chain breakdown and is the only scenario narrative in the document that uses this structural device. The plan's preferred midpoint language is "securing your first objective on the pivot host" or "your initial foothold yields the first flag" — narrative markers that communicate the dual-flag structure without labeling execution stages.

**Fix:** Replace stage labels with narrative midpoint language consistent with how ATP-01 through ATP-04 handle the same structure:

> You enter a three-machine Windows domain environment with only an attacker workstation and no credentials. Deploying Responder to poison LLMNR broadcast requests on the internal segment, you use ntlmrelayx to relay captured hashes over SMB to a domain member server — establishing a foothold that yields the first flag. With your pivot position secured, you use Rubeus to request service tickets for Kerberoastable accounts, crack the ticket offline with Hashcat, and use the recovered credentials with evil-winrm to move laterally to the domain controller and retrieve the second flag. Each lateral movement hop uses a distinct protocol — SMB for the first, WinRM for the second.

---

### WR-03: ATP-04 Kerberoasting Step Names No Second Lateral Movement Protocol — Ambiguity

**File:** `SCENARIOS.md:222`
**Issue:** The narrative ends with "use the resulting credential with a second lateral movement protocol to authenticate to the domain controller." The REQUIREMENTS.md entry for ATP-04 specifies the second protocol as "SMBExec/DCOM" — concrete options the student should recognize. Without naming either, the narrative leaves the second hop completely undefined, which may make it impossible for an instructor to evaluate whether the scenario design is coherent, or for a student to understand what tool knowledge is being tested. All other multi-step scenarios name both hop protocols in the narrative (SMB then WinRM for AD-05; WinRM named in ATP-01; dnscat2 named in ATP-02).

**Fix:** Name the second lateral movement option to match the REQUIREMENTS.md specification:

> ...use the resulting credential with SMBExec or DCOM to authenticate to the domain controller and retrieve the final flag...

---

### WR-04: Section Header "Multi-Step ATP Chains" Uses Acronym Inconsistent With Document Body

**File:** `SCENARIOS.md:188`
**Issue:** The section header reads "Multi-Step ATP Chains." The intro paragraph (line 3) calls them "multi-step APT-style attack chains." The AD-05 title (line 45) reads "Conti-Style APT Chain." APT (Advanced Persistent Threat) is the standard cybersecurity term for the named threat actors the scenarios emulate (Conti, HAFNIUM, SolarWinds attackers, LAPSUS$, Volt Typhoon). ATP is not a standard abbreviation in this context. The acronym inconsistency (APT in prose, ATP in headers and IDs) will cause confusion for any student or instructor who looks up the referenced threat groups. The scenario IDs (ATP-0x) are locked by REQUIREMENTS.md and cannot be changed, but the section header is free text.

**Fix:** The section header should use the same term as the prose and the AD-05 title:

```
## Multi-Step APT Chains
```

Note: The scenario ID prefix (ATP-) is inherited from REQUIREMENTS.md and should remain unchanged; only the section heading needs correction.

---

## Info

### IN-01: CVE-01 Inline Code Formatting Inconsistency

**File:** `SCENARIOS.md:99`
**Issue:** The CVE-01 narrative uses `` `mysmb.py` `` with backtick code formatting for the helper scaffold name. CVE-04 also uses `` `RpcAddPrinterDriverEx` `` in backticks (addressed in WR-01). No other scenario uses backtick formatting. If WR-01 is applied and the CVE-04 backtick is removed, `mysmb.py` will be the only backtick-formatted item in the document. The plan's authoring spec for CVE-01 explicitly includes the backtick form in its example language (`mysmb.py` protocol scaffold), so this formatting was intentional. It is inconsistent but not incorrect given the plan's explicit wording.

**Fix:** If code formatting is removed from CVE-04 per WR-01, consider also removing the backtick from `mysmb.py` in CVE-01 for visual consistency: change "the provided `mysmb.py` protocol scaffold" to "the provided mysmb.py protocol scaffold."

---

### IN-02: NET-03 Difficulty Rating — Easy vs Student Effort to Configure bettercap HTTPS Interception

**File:** `SCENARIOS.md:76`
**Issue:** If NET-03 is corrected per CR-02 to include HTTPS downgrade (as REQUIREMENTS.md specifies), the difficulty may warrant reconsideration. bettercap's HTTPS proxy configuration requires installing a CA certificate on target hosts, which in a lab context requires either pre-staging or student effort beyond simple ARP poisoning. The REQUIREMENTS.md assigns Easy difficulty, and this review does not override that, but the discrepancy is worth noting for the instructor's approval decision.

**Fix:** No change required at this stage. Flag for instructor review when approving the NET-03 scenario, particularly if HTTPS downgrade is confirmed as the target technique.

---

_Reviewed: 2026-06-11T16:45:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
