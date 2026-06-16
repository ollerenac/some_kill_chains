---
quick_id: 260611-lxt
date: 2026-06-11
status: complete
---

# Overlap Report — Proposed vs Deployed Wargame Exercises

## Verdict: NO OVERLAP ✓

All 23 proposed scenarios in `SCENARIOS.md` are **fully clear** of the 87
exercises already deployed on OFFen EDU. The proposed additions fill genuine
thematic gaps not covered by any existing challenge.

---

## Deployed Catalog Summary

| Category | Count | Representative titles |
|---|---|---|
| WEB_HACKING | 26 | SQL injection (×5), XSS, Path Traversal, SSRF(sendping/easyping) |
| CRYPTOGRAPHY | 13 | RSA, DH, hash collision, encoding weaknesses |
| FORENSIC | 21 | Memory dump, steganography, log analysis, network pcap |
| SYSTEM_HACKING | 12 | Buffer overflow, ROP, UAF, canary bypass |
| REVERSE | 10 | Packing, obfuscation, anti-analysis |
| MALWARE | 3 | DLL injection, registry persistence, scheduled tasks |
| ISMS | 3 | Splunk/Suricata/YARA tool familiarity |

**Deployed CVEs:** None — no challenge currently uses a real CVE identifier.

**Deployed TTPs (MITRE ATT&CK):** Data Encoding, Data from Local System,
Exploit Public-Facing Application, Exploitation for Client/Credential/Defense
Evasion, Hide Artifacts, Obfuscated Files, Weaken Encryption.

---

## Analysis per Proposed Domain

### Active Directory / Windows (AD-01 – AD-05)
No deployed challenge touches Windows domains, Kerberos, NTLM authentication,
BloodHound, ADCS, or any Windows Active Directory component.
**All 5 AD scenarios: ✓ no overlap.**

### Network Protocol Exploitation (NET-01 – NET-04)
The only deployed "network" content is `Network FORENSIC` (FORENSIC category —
packet capture analysis) and `TLS Ninja` (FORENSIC — TLS traffic decoding).
Neither involves active protocol exploitation, ARP/DNS poisoning, SMB relay, or
IPv6 abuse. The `ROBOT` challenge (WEB_HACKING) is a cryptographic web
vulnerability, not network protocol abuse.
**All 4 NET scenarios: ✓ no overlap.**

### CVE Weaponization (CVE-01 – CVE-04)
No deployed challenge references EternalBlue, Log4Shell, Spring4Shell, or
PrintNightmare. Zero CVE IDs exist in the deployed catalog. The deployed
`Exploit Public-Facing Application` TTP appears only in web-hacking challenges
(SQL injection, command injection) — not in CVE-specific exploitation.
**All 4 CVE scenarios: ✓ no overlap.**

### Cloud / Container Security (CC-01 – CC-03)
No deployed challenge involves Docker, Kubernetes, container escape, IMDS, IAM
roles, or cloud metadata. The forensics challenge `Escape Route` (a file-path
recovery puzzle) matches the word "escape" only superficially; the technique
domain is entirely different.
**All 3 CC scenarios: ✓ no overlap.**

### LLM Security (LLM-01 – LLM-03)
No deployed challenge involves AI/LLM systems, prompt injection, RAG pipelines,
or LLM-specific IDOR. The word "injection" appearing in `DLL Injection`
(malware analysis) and `sqlinjection lv5` (SQL injection) is a surface-level
false positive — technique domains are unrelated.
**All 3 LLM scenarios: ✓ no overlap.**

### Mini-APT Lateral Movement Chains (ATP-01 – ATP-04)
No deployed challenge is multi-stage or simulates APT behaviour. The
`DLL Injection` (malware) and `Lateral Movement` technique keyword do not appear
in any deployed description. No deployed challenge uses webshells, supply chain
backdoors, cloud identity chains, or LotL techniques.
**All 4 ATP scenarios: ✓ no overlap.**

---

## False-Positive Review

| Flag | Deployed match | Verdict |
|---|---|---|
| "escape" in CC-02 title | `Escape Route` (FORENSIC — file path puzzle) | False positive — unrelated technique |
| "escape" in CC-03 title | `Escape Route` (FORENSIC — file path puzzle) | False positive — unrelated technique |
| "injection" in LLM-01 title | `DLL Injection` (MALWARE), `sqlinjection lv5` (WEB) | False positive — different injection class |
| "injection" in LLM-02 title | `DLL Injection` (MALWARE), `sqlinjection lv5` (WEB) | False positive — different injection class |

---

## Domain Gap Confirmation

| Deployed domains | Proposed new domains |
|---|---|
| Cryptography, Web Hacking, Forensics, System Hacking, Reversing, Malware, ISMS | **Active Directory, Network Protocol, CVE Exploitation, Cloud/Container, LLM Security, APT Chains** |

The two sets are completely disjoint. Each proposed domain introduces an attack
surface not present anywhere in the current catalog.

---

## Conclusion

The 23 proposed scenarios can proceed to Phase 2 (kill-chain design) with full
confidence that they introduce genuinely new content. No remediation or
de-duplication is required.
