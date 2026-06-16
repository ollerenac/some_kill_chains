# Requirements: CTF Scenario Catalog — Advanced Cybersecurity Lab

**Defined:** 2026-06-11
**Core Value:** Students must deeply understand each attack technique by building and executing it themselves — not by running point-and-click tools.

---

## v1 Requirements

23 scenarios total (~20 as requested, slightly over due to ATP chain selections). Difficulty: 5 easy / 10 medium / 8 hard.

> **Global constraint — CVE & exploit scenarios:** Students must author all exploit code. No Metasploit or full-framework automation. Payloads and helper scaffolding (e.g., `mysmb.py`, struct templates) may be pre-staged as hidden files on the attacker VM, but execution code is student-authored.

---

### Active Directory / Windows (5 scenarios)

- [ ] **AD-01** *(Easy, Standalone, 2 VMs)*: Student performs Kerberoasting and AS-REP Roasting against a misconfigured Windows domain — enumerates SPNs with `nxc`/`GetUserSPNs.py`, requests service tickets, and cracks them offline with Hashcat to obtain the flag.

- [ ] **AD-02** *(Medium, Standalone, 2 VMs)*: Student exploits LLMNR/NBT-NS poisoning with Responder to capture NTLMv2 hashes and relays them via ntlmrelayx to SMB/LDAP to execute commands on a domain workstation without cracking credentials.

- [ ] **AD-03** *(Medium, Standalone, 2 VMs)*: Student uses BloodHound/SharpHound to enumerate an Active Directory environment, identifies an ACL abuse path (WriteDACL or GenericWrite), and chains privilege escalation steps to achieve Domain Admin.

- [ ] **AD-04** *(Hard, Standalone, 2 VMs)*: Student exploits Active Directory Certificate Services (ADCS) via ESC1 — enumerates certificate templates with Certipy, requests a rogue certificate for a privileged user, and authenticates as Domain Admin via PKINIT to obtain the flag.

- [ ] **AD-05** *(Hard, Multi-step ATP, 3 VMs, 2 flags)*: Conti-style APT chain. Student performs: (1) LLMNR poisoning → SMB relay → foothold on pivot server [Flag 1]; (2) Kerberoasting from pivot → offline crack → lateral movement via WinRM to DC [Flag 2]. Two distinct lateral movement protocols enforced.

---

### Network Protocol Exploitation (4 scenarios)

- [ ] **NET-01** *(Easy, Standalone, 2 VMs)*: Student captures NTLMv2 credentials via SMB Relay using Responder in analysis mode combined with ntlmrelayx — obtains access to a target share containing the flag without cracking the captured hash.

- [ ] **NET-02** *(Medium, Standalone, 2 VMs)*: Student performs an IPv6 + mitm6 + LDAP relay attack — sets up a rogue DHCPv6 server (mitm6), forces WPAD authentication, relays credentials to LDAP to create a new privileged domain account, and uses it to retrieve the flag. Zero code execution required.

- [ ] **NET-03** *(Easy, Standalone, 2 VMs)*: Student performs ARP cache poisoning to position as MITM between two hosts, strips HTTPS via sslstrip or SSLsplit, and intercepts plaintext credentials transmitted over HTTP/S to obtain the flag.

- [ ] **NET-04** *(Medium, Standalone, 2 VMs)*: Student exploits a DNS resolver misconfiguration to perform cache poisoning — injects a forged DNS response to redirect an internal service request, intercepts the subsequent HTTP request, and captures the flag embedded in the request.

---

### CVE Weaponization (4 scenarios)

> All CVE scenarios: no Metasploit. Students write exploit code from scratch or implement the weaponization class/function of a provided modular scaffold.

- [ ] **CVE-01** *(Hard, Standalone, 2 VMs)*: EternalBlue (MS17-010). Student authors a Python exploit against a Windows 7 SP1 target using the provided `mysmb.py` protocol scaffold and struct templates. Must implement SMBv1 transaction setup, double-pulsar payload staging, and shellcode execution to pop a shell and retrieve the flag.

- [ ] **CVE-02** *(Medium, Standalone, 2 VMs)*: Log4Shell (CVE-2021-44228). Student authors a JNDI injection payload string and a Python-based LDAP/HTTP exploit chain server to deliver and execute a command injection against an Apache Log4j 2.x Java application, resulting in OS command execution and flag retrieval.

- [ ] **CVE-03** *(Medium, Standalone, 2 VMs)*: Spring4Shell (CVE-2022-22965). Student crafts an HTTP exploit for the Spring MVC ClassLoader deserialization vulnerability — authors a Python script that sends the crafted multi-part request to deploy a JSP webshell, then uses the webshell to retrieve the flag.

- [ ] **CVE-04** *(Medium, Standalone, 2 VMs)*: PrintNightmare LPE (CVE-2021-34527). Student implements the DLL injection technique for the Windows Print Spooler — authors a C/Python payload that exploits `AddPrinterDriverEx` to load a malicious DLL with SYSTEM privileges, escalating from a low-privileged user to retrieve the flag.

---

### Cloud / Container Security (3 scenarios)

- [ ] **CC-01** *(Easy, Standalone, 2 VMs)*: Student exploits a simulated AWS IMDS endpoint (169.254.169.254 mock on a Flask server) via SSRF in a vulnerable web application — crafts SSRF requests to steal IAM role credentials, then uses the credentials to query a fake S3 API and retrieve the flag.

- [ ] **CC-02** *(Medium, Standalone, 2 VMs)*: Student escapes a privileged Docker container using the cgroup release_agent technique — mounts the host filesystem from inside the container, writes a reverse shell via the cgroup notification path, and retrieves a flag planted in the host's `/root/` directory.

- [ ] **CC-03** *(Hard, Standalone, 2 VMs)*: Student enumerates a misconfigured Kubernetes cluster (k3s) — identifies an over-privileged service account token, uses `kubectl` with stolen credentials to create a privileged pod with hostPath volume mount, escapes to the host node, and retrieves the flag.

---

### LLM Security (3 scenarios)

- [ ] **LLM-01** *(Easy, Standalone, 2 VMs)*: Student performs direct prompt injection against a locally-deployed Ollama chatbot (multi-layer defenses: system prompt + regex filter + semantic validation). Must chain at least two bypass techniques to override the system prompt and exfil a hidden flag embedded in the LLM's system context.

- [ ] **LLM-02** *(Medium, Standalone, 2 VMs)*: Student performs indirect prompt injection via a RAG-enabled chatbot — crafts a malicious document that is ingested into the vector database knowledge base, triggers the injected instruction via a benign user query, and causes the LLM to output the flag.

- [ ] **LLM-03** *(Medium, Standalone, 2 VMs)*: Student exploits an insecure LLM API infrastructure — uses IDOR in an unauthenticated or weakly-authenticated chat history endpoint to enumerate other users' conversation IDs and retrieve a flag embedded in a privileged user's chat session.

---

### Multi-Step ATP Chains (4 scenarios)

- [ ] **ATP-01** *(Hard, Multi-step ATP, 3 VMs, 2 flags)*: HAFNIUM-style. Student exploits a web application SSRF vulnerability to reach an internal service, elevates to code execution via a webshell upload, pivots to an internal Windows host via WinRM using harvested credentials [Flag 1 on pivot], then enumerates domain resources to reach the DC [Flag 2].

- [ ] **ATP-02** *(Hard, Multi-step ATP, 3 VMs, 2 flags)*: SolarWinds-style supply chain. Student compromises a software update server (simulated), plants a backdoored update that executes on a downstream target [Flag 1 on pivot], then establishes a covert C2 channel via DNS tunneling (iodine/dnscat2) to reach an isolated final target and retrieve [Flag 2].

- [ ] **ATP-03** *(Hard, Multi-step ATP, 3 VMs, 2 flags)*: LAPSUS$-style cloud identity chain. Student exploits a web application SSRF to steal a Kubernetes service account token from IMDS, uses the token to enumerate K8s cluster resources, escapes to a privileged pod [Flag 1], then queries etcd directly for stored secrets to authenticate as admin on the final internal target [Flag 2].

- [ ] **ATP-04** *(Hard, Multi-step ATP, 3 VMs, 2 flags)*: Volt Typhoon-style living-off-the-land. Student: (1) deploys mitm6 + LDAP relay to create a privileged domain account (zero malware); (2) uses new account to WinRM into pivot [Flag 1]; (3) from pivot, performs Kerberoasting, cracks service hash offline, and uses ticket for lateral movement to DC via a second protocol (e.g., SMBExec/DCOM) [Flag 2].

---

## v2 Requirements

Deferred to future release — not in current roadmap.

### Scenarios Deferred

- **ProxyLogon/Exchange Server (MS Exchange RCE chain)** — Exchange Server image too resource-heavy (8+ GB RAM); Windows evaluation ISO licensing concerns. Reconsider if dedicated Exchange VM resources become available.
- **BGP/OSPF routing protocol injection** — Requires FRR/Quagga on victim routers; lab hardware compatibility unconfirmed. High feasibility risk.
- **Supply chain attack via npm/PyPI package** — Requires internet access from lab VMs for realistic simulation; impractical in isolated lab network.
- **AI model backdoor / adversarial examples** — Requires GPU resources; not mature enough for reliable lab deployment.
- **Firmware/IoT exploitation** — Requires specialized hardware emulation (QEMU MIPS/ARM); outside current lab infrastructure.

---

## Out of Scope

| Feature | Reason |
|---------|--------|
| Cryptography challenges | Already in existing lab library |
| General web-hacking (SQLi, XSS, basic auth bypass) | Already in existing lab library |
| Forensics / disk and memory analysis | Already in existing lab library |
| Malware analysis and AV evasion | Already in existing lab library |
| ISMS / policy and governance exercises | Already in existing lab library |
| Reverse engineering | Already in existing lab library |
| Metasploit-based solutions | Pedagogically excluded — students must author exploit code |
| Scenarios requiring internet access from lab VMs | Isolated lab network constraint |
| Scenarios requiring >3 VMs | Hard infrastructure limit |
| Single-layer prompt injection (no defenses) | Trivially solvable with external LLM; no learning value |

---

## Phase 1 Deliverable Note

**Phase 1 output:** A clean document containing only scenario titles and descriptions for the 23 scenarios above. No kill-chain steps, no TTP codes, no implementation details. The user will review and refine this document before Phase 2 begins.

**Phase 2 deliverable:** Full kill-chain stages per scenario with MITRE ATT&CK TTP codes. Preceded by a methodology alignment discussion.

---

## Traceability

*Updated: 2026-06-11 after roadmap creation.*

Each REQ-ID is assigned to the phase where its primary deliverable is produced. Phase 1 produces the proposal entry for all 23 scenarios. Phases 2-4 produce the kill-chain write-up for each scenario's domain group.

| Requirement | Phase 1 (Proposal) | Kill-Chain Phase | Status |
|-------------|-------------------|-----------------|--------|
| AD-01 | Phase 1 | Phase 2 | Pending |
| AD-02 | Phase 1 | Phase 2 | Pending |
| AD-03 | Phase 1 | Phase 2 | Pending |
| AD-04 | Phase 1 | Phase 2 | Pending |
| AD-05 | Phase 1 | Phase 2 | Pending |
| NET-01 | Phase 1 | Phase 2 | Pending |
| NET-02 | Phase 1 | Phase 2 | Pending |
| NET-03 | Phase 1 | Phase 2 | Pending |
| NET-04 | Phase 1 | Phase 2 | Pending |
| CVE-01 | Phase 1 | Phase 3 | Pending |
| CVE-02 | Phase 1 | Phase 3 | Pending |
| CVE-03 | Phase 1 | Phase 3 | Pending |
| CVE-04 | Phase 1 | Phase 3 | Pending |
| CC-01 | Phase 1 | Phase 3 | Pending |
| CC-02 | Phase 1 | Phase 3 | Pending |
| CC-03 | Phase 1 | Phase 3 | Pending |
| LLM-01 | Phase 1 | Phase 4 | Pending |
| LLM-02 | Phase 1 | Phase 4 | Pending |
| LLM-03 | Phase 1 | Phase 4 | Pending |
| ATP-01 | Phase 1 | Phase 4 | Pending |
| ATP-02 | Phase 1 | Phase 4 | Pending |
| ATP-03 | Phase 1 | Phase 4 | Pending |
| ATP-04 | Phase 1 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 23 total
- Mapped to phases: 23
- Unmapped: 0 ✓

---
*Requirements defined: 2026-06-11*
*Last updated: 2026-06-11 after roadmap creation*
