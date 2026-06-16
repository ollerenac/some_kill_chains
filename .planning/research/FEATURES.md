# Features Research: CTF Scenario Domains

**Project:** CTF Scenario Catalog — Advanced Cybersecurity Lab
**Researched:** 2026-06-11
**Mode:** Ecosystem / Feature Landscape

---

## Active Directory / Windows

### Context

Active Directory attacks form the core of most enterprise breach scenarios. The GOAD (Game of Active Directory) lab is the community standard reference implementation, covering attacks across multi-domain environments. ADCS (AD Certificate Services) research by SpecterOps (2021, extended through 2025 with ESC9–ESC16) massively expanded the attack surface. All techniques below have been validated against current AD configurations and widely documented tooling (Impacket, Certipy, BloodHound CE).

### Table Stakes — Must-know for any security professional

| Technique | MITRE ATT&CK | Why Table Stakes | Lab Complexity |
|-----------|--------------|-----------------|----------------|
| LDAP Enumeration | T1087.002 | Entry point to every AD engagement; no credentials needed for anonymous bind on misconfigured DCs | Low (1 VM) |
| Kerberoasting | T1558.003 | Present in >90% of real AD pentests; requesting TGS tickets for SPN accounts is trivial, offline cracking teaches hash mechanics | Low–Medium (2 VM) |
| AS-REP Roasting | T1558.004 | Requires no credentials; targets accounts with pre-auth disabled — extremely common in legacy environments | Low (2 VM) |
| Pass-the-Hash (PtH) | T1550.002 | Fundamental lateral movement; demonstrates NTLM's design flaw; every AD attacker needs this | Medium (2 VM) |
| DCSync | T1003.006 | Demonstrates replication abuse to dump all hashes including krbtgt — the "game over" technique | Medium (2–3 VM) |
| BloodHound path-finding | T1482 | Graph-based attack path discovery is now industry-standard; teaches attackers to read trust relationships | Medium (2 VM) |

**Rationale for ordering:** Enumeration is always first; Kerberoasting and AS-REP Roasting are standalone credential-access scenarios before lateral movement; BloodHound feeds all subsequent privilege escalation paths.

### Differentiators — Advanced / cutting-edge

| Technique | MITRE ATT&CK | Why Differentiating | Lab Complexity |
|-----------|--------------|---------------------|----------------|
| ADCS ESC1 (misconfigured certificate template, Enrollee Supplies Subject) | T1649 | ESC1 is the most impactful and most common ADCS misconfiguration; Certipy makes enumeration trivial but students must understand *why* the template is abusable | Medium (2 VM) |
| ADCS ESC4 (weak ACL on template — WriteDACL/WriteProperty) | T1649 | ESC4 is the "gateway" — attacker with low-priv rights modifies a template to make it vulnerable to any other ESC technique; chains into ESC1 | High (2–3 VM) |
| ADCS ESC8 (NTLM relay to HTTP enrollment endpoint) | T1649 + T1557.001 | Combines network-level NTLM relay with certificate abuse; teaches compound protocol interaction | High (3 VM) |
| ACL Abuse (WriteDACL / GenericAll on user/group) | T1222 | Misconfigured ACEs are ubiquitous and hard to detect; BloodHound surfaces them but students must script the exploit with Impacket/PowerView | Medium–High (2 VM) |
| GPO Abuse (GPO link on OU with WriteProperty) | T1484.001 | GPOs as persistence and lateral-movement vehicle; teaches policy-level thinking beyond individual host | High (2–3 VM) |
| Pass-the-Ticket / Silver Ticket | T1550.003 | Demonstrates forgeability of Kerberos service tickets without DA; Silver Ticket requires understanding of service account keying | High (2–3 VM) |
| Golden Ticket (post-DCSync) | T1558.001 | Ultimate persistence technique; best placed as the *final objective* in a multi-step scenario after DCSync | High (3 VM) |

### Anti-Features — Techniques to deliberately avoid

| Technique | Why Avoid |
|-----------|-----------|
| Pass-the-Hash with Metasploit psexec | Project constraint: no Metasploit; also teaches nothing about the underlying NTLM handshake |
| Basic LDAP anonymous dump (ldapsearch one-liner) | Too trivial for grad-level students; already appears in entry-level security courses |
| Simple password spraying without domain context | Covered in Web-Hacking module (auth brute-force); not AD-specific enough |
| Unconstrained delegation | Complex to set up correctly in a 2-VM lab, and ESC scenarios cover certificate delegation more cleanly |
| AS-REP roasting with Rubeus GUI | Use Impacket GetNPUsers.py instead — forces understanding of Kerberos packet structure |

### Recommended Scenario Count: 4–5 scenarios

- 1 standalone: Kerberoasting (Medium — offline hash cracking chain)
- 1 standalone: AS-REP Roasting (Easy — no-cred entry point)
- 1 standalone: ADCS ESC1 via Certipy + certificate authentication to DA (Medium)
- 1 multi-step ATP: BloodHound → ACL abuse → DCSync → Golden Ticket (Hard)
- 1 multi-step ATP: NTLM relay (ESC8) → ADCS certificate abuse → lateral movement (Hard)

---

## Cloud / Container Security

### Context

Cloud attack simulation in a local lab is feasible via two routes: (1) Kubernetes/container-native attacks using minikube or kind — no cloud account needed, full local isolation; (2) AWS/cloud simulation via LocalStack or mock IMDS endpoints. Route 1 is strongly preferred for infrastructure reasons (the lab runs on a local server). SSRF → IMDS → IAM credential theft is the canonical cloud attack chain and is well-documented in CloudGoat and flaws.cloud.

### Table Stakes

| Technique | MITRE ATT&CK | Why Table Stakes | Feasibility in Local Lab |
|-----------|--------------|-----------------|--------------------------|
| Privileged container escape (hostPath + nsenter) | T1611 | The simplest container boundary defeat: `privileged: true` + `hostPath: /` + `chroot /host` gives immediate node root. Teaches container isolation fundamentals | HIGH — minikube, single VM |
| IMDS credential theft via SSRF | T1552.005 | SSRF → metadata endpoint (169.254.169.254) → IAM role credentials is the most common cloud initial-access pattern; mock IMDS via Flask or LocalStack | HIGH — mock endpoint on attacker VM |
| Kubernetes service account token abuse | T1528 | Default service account tokens mounted at `/var/run/secrets/kubernetes.io/serviceaccount/token`; students query kube-apiserver with `kubectl --token` | HIGH — minikube |
| S3 bucket misconfiguration (public read/write) | T1530 | Exposed object storage is OWASP Cloud Top 10 #1; flaws.cloud is the reference; mockable with MinIO locally | HIGH — MinIO container |

### Differentiators

| Technique | MITRE ATT&CK | Why Differentiating | Feasibility |
|-----------|--------------|---------------------|-------------|
| Kubernetes RBAC privilege escalation (create pod in privileged namespace) | T1078.003 | Requires understanding of RBAC role binding chains; attacker enumerates permissions with `can-i --list`, then creates privileged pod to escape | HIGH — minikube |
| Docker socket escape (/var/run/docker.sock mounted) | T1611 | Classic container escape via exposed Docker daemon; teaches daemon trust boundary | HIGH — single VM with Docker-in-Docker |
| cgroup v1 release_agent escape | T1611 | Kernel-level container escape technique; demonstrates how cgroup primitives are abused; well-documented PoC exists | MEDIUM — requires specific kernel version in lab |
| Kubernetes secret theft from etcd (unauthenticated etcd) | T1552 | etcd stores all cluster secrets unencrypted by default in older configs; direct API attack against :2379 | HIGH — minikube |
| Cloud IAM privilege escalation (iam:CreatePolicyVersion) | T1098 | IAM misconfiguration chains; mockable with LocalStack; demonstrates "confused deputy" class bugs | MEDIUM — LocalStack complexity |

### Anti-Features

| Technique | Why Avoid |
|-----------|-----------|
| Real AWS account required for attack | Infrastructure constraint — lab runs on local server only |
| Docker image pull attacks / registry poisoning | Supply chain category; overlaps with Malware module's supply chain scope |
| Terraform misconfiguration scanning | IaC scanning is a tool exercise, not an active attack; insufficient hands-on |
| Kubernetes network policy bypass (advanced CNI exploits) | Too dependent on specific CNI plugin; not reproducible across lab configurations |

### Recommended Scenario Count: 2–3 scenarios

- 1 standalone: Privileged container escape → node root (Easy–Medium)
- 1 standalone: SSRF → mock IMDS → IAM token abuse → S3 exfiltration (Medium)
- 1 multi-step ATP: K8s RBAC misconfiguration → service account token → privileged pod escape → etcd secret dump (Hard)

---

## Network Protocol Exploitation

### Context

Network protocol attacks are the most classroom-compatible domain. They require only 2–3 VMs, operate over standard Ethernet/IP, and Responder + Impacket toolchain is well-documented. The Responder → NTLM relay → ntlmrelayx chain is the definitive "initial access via network position" scenario and appears in virtually every enterprise pentest. IPv6 attacks via mitm6 are underappreciated but extremely effective since most networks have IPv6 enabled with no DHCPv6 guards.

### Table Stakes

| Technique | MITRE ATT&CK | Why Table Stakes | Lab Complexity |
|-----------|--------------|-----------------|----------------|
| LLMNR/NBT-NS poisoning with Responder | T1557.001 | Entry-level network attack; Windows fallback resolution protocols leak NTLMv2 hashes; demonstrates why broadcast protocols are dangerous | Low (2 VM) |
| NTLMv2 hash capture → offline cracking | T1110.002 | Follows from Responder; teaching hashcat/john for NTLMv2 is foundational | Low (2 VM) |
| SMB relay via ntlmrelayx (NTLM capture without signing) | T1557.001 | Relay captured NTLM auth to second host; demonstrates signing enforcement as defense; requires SMB signing disabled | Medium (3 VM) |
| ARP spoofing + MITM (intercept cleartext protocols) | T1557.002 | Classical MITM; demonstrates Ethernet trust model weakness; captures cleartext credentials over HTTP/FTP/Telnet | Medium (2–3 VM) |

### Differentiators

| Technique | MITRE ATT&CK | Why Differentiating | Lab Complexity |
|-----------|--------------|---------------------|----------------|
| IPv6 mitm6 + WPAD (DHCPv6 spoof → DNS takeover → NTLM relay) | T1557.001 + T1557 | Modern enterprises forget to disable IPv6; mitm6 spoofs DHCPv6, poisons DNS, feeds WPAD to capture hashes from every machine that queries for a proxy | High (3 VM) |
| DNS poisoning (authoritative response spoofing) | T1565.002 | Demonstrates how DNS cache can be poisoned without Kaminsky-style attacks using misconfigured resolvers | Medium (2–3 VM) |
| NTLM relay to LDAP (LDAPS without signing → add user to Domain Admins) | T1557.001 | Relay not just to SMB but to LDAP; result is direct domain compromise via account manipulation, not code execution | High (3 VM) |
| LDAP injection against web app front-end to AD | T1190 + T1556 | Web app queries AD via LDAP with unsanitized input; demonstrates that AD is exposed via application layer, not just network layer | Medium (2 VM) |

### Anti-Features

| Technique | Why Avoid |
|-----------|-----------|
| Basic Wireshark packet capture tutorial | Captures, not an attack; too passive for CTF format |
| SSL stripping (sslstrip) | Largely neutralized by HSTS preloading in modern browsers; low real-world relevance in 2025 |
| Raw 802.11 WiFi deauth attacks | Requires physical wireless hardware; not reproducible in the VM lab |
| BGP hijacking / route injection | Requires full routing infrastructure; far outside 3-VM constraint |
| DNS Kaminsky attack | Theoretically important but patched in all modern resolvers; better as a theory lecture than CTF |

### Recommended Scenario Count: 3–4 scenarios

- 1 standalone: LLMNR poisoning → NTLMv2 capture → crack (Easy)
- 1 standalone: ARP spoofing → MITM → cleartext credential capture (Easy–Medium)
- 1 multi-step ATP: Responder capture → SMB relay → shell on victim → lateral to second host (Medium)
- 1 multi-step ATP: mitm6 DHCPv6 spoof → WPAD poisoning → NTLM relay to LDAP → DA account creation (Hard)

---

## LLM Security

### Context

OWASP released the LLM Top 10 v2025 (finalized November 2024), with 10 categories. Two are new: LLM07 System Prompt Leakage and LLM08 Vector and Embedding Weaknesses (RAG poisoning). LLM06 Excessive Agency was substantially expanded. For CTF design, the challenge is operationalizing abstract risks as concrete flag-finding exercises. The strongest candidates are direct/indirect prompt injection (clear win/loss condition), system prompt extraction, RAG poisoning (manipulate retrieval to change model output), and excessive agency (tool-call hijacking). Infrastructure-level attacks (IDOR on chat history, exposed API endpoints) are highly teachable and largely absent from existing CTF libraries.

### OWASP LLM Top 10 2025 — Full Mapping

| ID | Risk | CTF Teachability | Notes |
|----|------|-----------------|-------|
| LLM01 | Prompt Injection (direct + indirect) | EXCELLENT | Clearest win condition: extract secret from system prompt |
| LLM02 | Sensitive Information Disclosure | GOOD | Model regurgitates PII/credentials from training/context |
| LLM03 | Supply Chain | POOR for CTF | Requires compromising upstream model/dataset; too infrastructural |
| LLM04 | Data and Model Poisoning | GOOD | RAG knowledge-base poisoning; inject malicious docs to manipulate responses |
| LLM05 | Improper Output Handling | GOOD | LLM output fed to shell/SQL without sanitization → code injection |
| LLM06 | Excessive Agency | EXCELLENT | Agent with tool access hijacked into performing unintended actions |
| LLM07 | System Prompt Leakage | EXCELLENT | Extract system prompt via jailbreak techniques |
| LLM08 | Vector and Embedding Weaknesses | GOOD | Poison vector DB; mislead RAG pipeline |
| LLM09 | Misinformation | POOR for CTF | Factual error generation; no clear security-flag win condition |
| LLM10 | Unbounded Consumption | POOR for CTF | DoS-class attack; not flag-based |

### Table Stakes

| Technique | OWASP ID | Why Table Stakes | Implementation |
|-----------|----------|-----------------|----------------|
| Direct prompt injection (extract secret from system prompt) | LLM01 | The foundational LLM attack; secret in system prompt, user tries jailbreak strings to leak it | Deploy small local model (Ollama + llama3 or mistral) with system prompt containing flag |
| System prompt leakage via role confusion | LLM07 | "Repeat your instructions verbatim" style attacks; teaches that system prompts are not access-controlled | Same local model setup |
| Insecure output handling (LLM output → unsanitized shell exec) | LLM05 | LLM generates code/commands that get executed; students craft input so LLM produces malicious command | Flask app wrapping model, executes LLM-generated shell commands |

### Differentiators

| Technique | OWASP ID | Why Differentiating | Implementation |
|-----------|----------|---------------------|----------------|
| Indirect prompt injection (malicious content in RAG-retrieved document) | LLM01 + LLM08 | Model retrieves attacker-controlled document containing hidden instructions; no direct user-model communication | RAG pipeline with ChromaDB/FAISS; attacker uploads poisoned PDF to knowledge base |
| RAG knowledge-base poisoning (embed adversarial document to bias answers) | LLM04 + LLM08 | Attacker poisons vector store so all users get manipulated answers; demonstrates long-term persistence in AI systems | Pre-stage poisoned doc in vector DB; flag is in the manipulated answer |
| Excessive agency / tool-call hijacking (agent triggered to exfiltrate via email tool) | LLM06 | Agentic LLM with email/file tools; indirect injection in processed email causes agent to exfiltrate data using its own tools | LangChain/CrewAI agent with file-read and HTTP-call tools; malicious instruction in processed file |
| LLM infrastructure IDOR (access other users' chat history via manipulated session/ID) | LLM02 + general web | Breaks "LLM security is only prompt injection" assumption; chat history API with predictable IDs leaks other users' conversations | Custom chatbot API; flag hidden in another user's chat session |
| Sensitive info disclosure (model trained/fine-tuned on PII, extracts via prompt) | LLM02 | Demonstrates memorization risk; model regurgitates credential-like strings from training context | Fine-tuned or context-stuffed local model with embedded flag |

### Anti-Features

| Technique | Why Avoid |
|-----------|-----------|
| "Jailbreak to generate harmful content" scenarios | Pedagogically unclear win condition; focuses on policy violation not security vulnerability |
| Model denial-of-service (token flooding) | LLM10; no meaningful skill; student just sends long string; not flag-based |
| LLM supply chain attacks (poisoned model weights) | LLM03; requires model training infrastructure; completely outside lab VM constraints |
| Adversarial ML (model evasion via perturbation) | Overlaps with ML security subdomain; not covered by OWASP LLM framing; requires ML expertise beyond scope |

### Recommended Scenario Count: 2–3 scenarios

- 1 standalone: Direct prompt injection + system prompt leakage (Easy–Medium)
- 1 standalone: Indirect prompt injection via RAG-retrieved document (Medium–Hard)
- 1 multi-step ATP: Agentic LLM with tools → indirect injection via external data → tool-call hijack → exfiltrate flag via HTTP tool (Hard)

---

## CVE Weaponization

### Context

The project constraint is explicit: students must author exploit code — no Metasploit, no full-framework shortcuts. This shapes which CVEs are appropriate. The best CVEs for exploit-authoring exercises are those where: (a) the vulnerability mechanism is conceptually clear, (b) public PoC reference code exists in Python/C (not just Metasploit modules), (c) the exploit requires non-trivial coding (network socket handling, binary packing, HTTP manipulation), and (d) a Docker or VM-based vulnerable environment is trivially reproducible.

### Table Stakes

| CVE | Vulnerability Class | Why Table Stakes | Authoring Difficulty | Notes |
|-----|--------------------|-----------------|--------------------|-------|
| Log4Shell (CVE-2021-44228) | JNDI injection → RCE | Defines a generation of vulnerability disclosure; JNDI lookup is conceptually clean; students write Python LDAP redirect server + payload crafter | Medium | Requires: malicious LDAP server (Python ldap3), Log4j-vulnerable Java app in Docker; no binary exploitation |
| EternalBlue (MS17-010) | SMBv1 buffer overflow → RCE | Seminal NSA exploit; teaches SMB protocol structure, Windows memory layout, shellcode staging; Python exploit (Impacket + mysmb.py) well-documented | Hard | Requires: Python Impacket, understanding of SMB transaction malformation; students write send-and-execute wrapper around public PoC |
| PrintNightmare (CVE-2021-34527) | Windows Print Spooler LPE/RCE | Teaches DLL injection via Windows print driver mechanism; LPE variant is clean for local privilege escalation; students write DLL payload and exploit script | Medium–Hard | Two variants: LPE (easier, single VM) and RCE (harder, requires network access to Spooler) |
| Spring4Shell (CVE-2022-22965) | ClassLoader manipulation → RCE via data binding | Teaches Java class hierarchy exploitation; students craft HTTP POST with malicious data-binding parameters to write JSP webshell | Medium | Docker image (spring-boot + Spring Framework 5.3.17 / JDK 9+) trivially available; HTTP-only exploit |

### Differentiators

| CVE | Vulnerability Class | Why Differentiating | Authoring Difficulty |
|-----|--------------------|--------------------|---------------------|
| Apache Struts RCE (CVE-2017-5638) | OGNL expression injection via Content-Type header | Classic enterprise Java RCE; teaches OGNL expression language as attack vector; conceptually different from Log4Shell (expression evaluator vs. JNDI) | Medium |
| Shellshock (CVE-2014-6271) | Bash function definition parsing → env var injection | Teaches OS-level environment variable attack surface; CGI-based exploitation; students write raw HTTP request with malicious User-Agent/Referer | Easy–Medium |
| DirtyPipe (CVE-2022-0847) | Linux kernel pipe splice race → arbitrary file overwrite | Modern Linux kernel LPE; teaches pipe/splice syscall internals; students write C exploit overwriting SUID binary | Hard |
| Apache HTTPD path traversal / RCE (CVE-2021-41773 / CVE-2021-42013) | Path normalization bypass → RCE via mod_cgi | Teaches URL normalization bugs; two CVEs chain together cleanly; Python PoC is short and comprehensible | Easy–Medium |

### Anti-Features

| CVE/Technique | Why Avoid |
|---------------|-----------|
| Dirty COW (CVE-2016-5195) | Kernel race condition is too old (Linux 2.6–4.8); modern kernels patched; unreliable timing makes it a poor CTF exercise |
| Heartbleed (CVE-2014-0160) | Already appears in most existing CTF libraries; explicitly covered in Web-Hacking adjacent content |
| Spectre/Meltdown | Requires bare-metal or near-native VM access; timing channels unreliable in hypervisor; more theory than practice |
| Full Metasploit module re-implementation | Defeat the purpose; students must understand the mechanism, not re-implement a framework |
| Any CVE from 2023+ requiring current-year patch bypass | Risk of lab environment being auto-patched; prefer CVEs with stable, reproducible vulnerable environments |

### Recommended Scenario Count: 3–4 scenarios

- 1 standalone: Log4Shell — write JNDI redirect server + trigger LDAP callback RCE (Medium)
- 1 standalone: Spring4Shell — write data-binding exploit to deploy webshell (Medium)
- 1 standalone: PrintNightmare LPE — write DLL payload + exploit script for privilege escalation (Medium–Hard)
- 1 multi-step ATP: EternalBlue initial foothold → PtH lateral movement → DCSync (Hard) — bridges CVE exploitation into AD domain

---

## Mini-APT Scenario Templates

### Design Principles

Multi-step ATP scenarios follow the project's defined template: (1) recon/credential-access on attacker VM, (2) lateral movement to pivot server (flag 1), (3) in-host privilege escalation on pivot, (4) second lateral movement via *different protocol* to final server (flag 2). Two lateral movements with different protocols is the pedagogically critical constraint — it prevents students from memorizing a single tool.

The best APT campaign templates are those with:
- Public post-mortems or MITRE ATT&CK group pages documenting the kill chain
- Realistic 2–3 VM topologies
- Distinct TTPs at each stage (not just "credential abuse everywhere")
- A teachable "aha moment" — one technique that uniquely characterizes the campaign

---

### Template 1: Conti-Style AD Takeover

**Based on:** Conti ransomware operator TTPs (MITRE G0080), Conti playbook leak (2021)
**Theme:** Credential access → SMB lateral movement → AD compromise → ransomware deployment gate

**Kill Chain:**
1. LLMNR/NBT-NS poisoning → capture NTLMv2 hash → crack password (T1557.001)
2. Lateral to Windows server via PsExec/SMB with cracked credentials (T1021.002) → **Flag 1** (file on server)
3. Kerberoasting from pivot → crack service account hash
4. BloodHound path → ACL abuse (WriteDACL on domain object) → DCSync → dump krbtgt hash → **Flag 2** (domain secret)

**Protocols used:** LLMNR (step 1) → SMB (step 2) → Kerberos/LDAP (step 4)
**Difficulty:** Hard
**VM count:** 3 (attacker + Windows workstation + Windows DC)
**Unique teaching moment:** Conti operators relied on cracked credentials + SMB propagation, not sophisticated exploits — basic credential hygiene would have stopped them.

---

### Template 2: HAFNIUM-Style Exchange Chain

**Based on:** HAFNIUM (MITRE G0125), Exchange ProxyLogon/ProxyShell chaining
**Theme:** Web-facing service exploitation → webshell → credential dump → domain escalation

**Kill Chain:**
1. SSRF + auth bypass on Exchange-like web service → deploy webshell (T1190 + T1505.003)
2. Webshell → dump LSASS credentials via comsvcs.dll (T1003.001) → **Flag 1** (NTLM hash in memory dump)
3. Pass-the-Hash with domain admin account via WinRM (T1550.002 + T1021.006)
4. DCSync from DC → extract all domain hashes → **Flag 2** (krbtgt NTLM hash)

**Protocols used:** HTTPS/SSRF (step 1) → WinRM (step 3) — distinct protocol change enforced
**Difficulty:** Hard
**VM count:** 3 (attacker + Exchange/web server + DC)
**Unique teaching moment:** HAFNIUM combined CVE exploitation with living-off-the-land (comsvcs.dll, legitimate admin tools) — no custom malware needed.
**Note:** Replace real ProxyLogon CVE with a custom-built SSRF + auth-bypass web app to avoid dependency on specific Exchange versions.

---

### Template 3: SolarWinds-Style Supply Chain / Trusted Tool Abuse

**Based on:** SolarWinds SUNBURST (MITRE G0016 / APT29 UNC2452)
**Theme:** Trusted update mechanism as initial access → stealthy long-term persistence → credential harvest

**Kill Chain:**
1. Attacker compromises a "software update server" (pre-staged backdoored update binary) — students discover the trojanized update and understand the delivery mechanism (T1195.002)
2. Backdoor phones home via DNS (DoH-style covert channel) → students must decode DNS TXT record to get C2 command → **Flag 1** (C2 decoded instruction)
3. C2 instructs token theft from running processes → Kerberos ticket extraction → Pass-the-Ticket to admin share (T1550.003 + T1021.002)
4. Final exfiltration via HTTPS to simulated C2 → **Flag 2** (exfiltrated secret)

**Protocols used:** HTTP update channel (step 1) → DNS covert channel (step 2) → SMB (step 3)
**Difficulty:** Hard
**VM count:** 3 (attacker/C2 + victim workstation + update server)
**Unique teaching moment:** Detection is the key lesson — SUNBURST's covert channel used DNS to evade network monitoring; students learn to read DNS traffic for anomalies.

---

### Template 4: LAPSUS$-Style Social/Cloud Pivot

**Based on:** LAPSUS$ TTPs (MITRE G1004) — identity provider abuse, cloud credential theft
**Theme:** Cloud credential theft → container escape → internal service access

**Kill Chain:**
1. SSRF vulnerability in web app → query mock IMDS endpoint → steal IAM role credentials (T1552.005)
2. Use credentials to enumerate K8s service account tokens from cloud storage → **Flag 1** (service account token)
3. Deploy privileged pod via misconfigured RBAC → escape to node host filesystem (T1611)
4. Read etcd secrets → extract admin kubeconfig → access internal app with flag → **Flag 2**

**Protocols used:** HTTP/SSRF (step 1) → K8s API (step 2–4)
**Difficulty:** Hard
**VM count:** 2–3 (attacker + K8s node + optional separate "cloud storage" VM)
**Unique teaching moment:** LAPSUS$ attacked identity infrastructure, not endpoints — cloud and container IAM is the new AD.

---

### Template 5: Volt Typhoon-Style Living-off-the-Land

**Based on:** Volt Typhoon (MITRE G1017) — LOLBins, minimal footprint, network pivot via SOHO devices
**Theme:** Network-level attack with no custom malware — only built-in OS tools

**Kill Chain:**
1. mitm6 DHCPv6 spoofing → DNS takeover → capture NTLMv2 hash via WPAD (T1557.001)
2. Relay hash to LDAP → create new domain account (no code execution; pure protocol relay) → **Flag 1** (created account name/hash found in LDAP)
3. Authenticate as new account via WinRM → enumerate with built-in tools (whoami, net, nltest) → find secondary target
4. Kerberoast secondary service account → crack → access second server → **Flag 2**

**Protocols used:** DHCPv6/DNS (step 1) → LDAP relay (step 2) → WinRM (step 3) → Kerberos (step 4)
**Difficulty:** Hard
**VM count:** 3 (attacker + Windows workstation + Windows server)
**Unique teaching moment:** Volt Typhoon used *no malware* — entire chain is protocol abuse and OS-native tools. Defense requires protocol hardening, not just AV.

---

## Coverage Summary

### Recommended 20-Scenario Allocation

| Domain | Standalone | Multi-step ATP | Total | Difficulty Distribution |
|--------|------------|---------------|-------|------------------------|
| Active Directory | 3 | 2 | 5 | 1 Easy, 2 Medium, 2 Hard |
| Cloud / Container | 2 | 1 | 3 | 1 Easy, 1 Medium, 1 Hard |
| Network Protocol | 2 | 2 | 4 | 2 Easy, 1 Medium, 1 Hard |
| LLM Security | 2 | 1 | 3 | 1 Easy, 1 Medium, 1 Hard |
| CVE Weaponization | 3 | 1 | 4 | 1 Easy, 2 Medium, 1 Hard |
| **Totals** | **12** | **7** | **19** | 5E / 9M / 5H *(+1 flex)* |

*Note: One scenario slot is flexible — recommended for a cross-domain bonus scenario combining CVE exploitation with AD post-exploitation (e.g., EternalBlue → PtH → DCSync)*

### Priority Ranking (if fewer than 20 scenarios are ultimately built)

**Tier 1 — Build first (highest signal, most novel vs. existing library):**
1. ADCS ESC1 certificate abuse → DA (AD, Medium)
2. Log4Shell exploit authoring → RCE (CVE, Medium)
3. Conti-style ATP: LLMNR → SMB → Kerberoast → DCSync (AD+Net, Hard)
4. Direct + indirect prompt injection (LLM, Medium)
5. Privileged container escape + RBAC (Cloud, Medium)

**Tier 2 — High value, slightly more overlap with common CTF content:**
6. AS-REP Roasting (AD, Easy)
7. LLMNR → NTLM crack (Network, Easy)
8. Spring4Shell exploit authoring (CVE, Medium)
9. mitm6 → NTLM relay to LDAP → DA creation (Network, Hard)
10. SSRF → IMDS → S3 exfiltration (Cloud, Medium)

**Tier 3 — Advanced / differentiating for top students:**
11. ADCS ESC4 + ESC8 chain (AD, Hard)
12. Agentic LLM tool-call hijacking (LLM, Hard)
13. K8s RBAC → privileged pod → etcd (Cloud, Hard)
14. EternalBlue exploit authoring (CVE, Hard)
15. LAPSUS$-style cloud ATP (Cloud+AD, Hard)

### Technique Reuse Across Scenarios (watch for overlap)

- **DCSync** appears as end-stage in both Conti ATP and HAFNIUM ATP — ensure different paths reach it
- **NTLMv2 hash capture** appears in standalone LLMNR scenario and Conti ATP — standalone teaches cracking; ATP teaches relaying
- **Kerberoasting** appears standalone and embedded in Conti ATP — standalone teaches the mechanics; ATP treats it as a step
- **Privileged container escape** appears standalone and in LAPSUS$ ATP — standalone is pure escape; ATP chains it

---

## Sources

- [OWASP Top 10 for LLM Applications 2025 — Official](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [ADCS ESC1–ESC16 Reference — Certipy Wiki](https://github.com/ly4k/Certipy/wiki/06-%E2%80%90-Privilege-Escalation)
- [ADCS Domain Escalation — HackTricks](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/ad-certificates/domain-escalation)
- [ESC1 & ESC8 Pentesting ADCS](https://abrictosecurity.com/pentesting-active-directory-certificate-services-adcs-esc1-esc8/)
- [ESC4 — Weak ACLs on Certificate Templates](https://www.redfoxsec.com/blog/exploiting-weak-acls-on-active-directory-certificate-templates-esc4-explained)
- [GOAD — Game of Active Directory](https://github.com/Orange-Cyberdefense/GOAD)
- [BloodHound CE: AD Attack Paths](https://hivesecurity.gitlab.io/blog/bloodhound-practical-guide-ad-attack-paths/)
- [LLMNR/NBT-NS Poisoning — MITRE ATT&CK T1557.001](https://attack.mitre.org/techniques/T1557/001/)
- [AD Attack Lab: LLMNR, SMB relay, IPv6](https://bohansec.medium.com/ad-attack-lab-part-two-llmnr-poisoning-smb-relay-and-ipv6-attack-63c3bd5a47c9)
- [Kubernetes CTF — minik8s-ctf](https://github.com/quarkslab/minik8s-ctf)
- [K8s Container Escape and Cluster Breakout](https://github.com/KimberleyMsengezi/Kubernetes-Container-Escape-Cluster-Breakout)
- [SSRF → IMDS → IAM Attack Chain](https://medium.com/legionhunters/ssrf-imds-iam-breaking-down-a-real-cloud-attack-chain-in-aws-f28c04421512)
- [CloudGoat EC2 SSRF Scenario](https://rhinosecuritylabs.com/cloud-security/cloudgoat-aws-scenario-ec2_ssrf/)
- [Log4Shell — ZeroPath Deep Dive](https://zeropath.com/blog/cve-2021-44228-log4shell-log4j-rce)
- [EternalBlue Python Manual Exploit — Null Byte](https://null-byte.wonderhowto.com/how-to/manually-exploit-eternalblue-windows-server-using-ms17-010-python-exploit-0195414/)
- [Spring4Shell — HTB Explained](https://www.hackthebox.com/blog/spring4shell-explained-cve-2022-22965)
- [PrintNightmare — CISA Alert](https://www.cisa.gov/news-events/alerts/2021/06/30/printnightmare-critical-windows-print-spooler-vulnerability)
- [AS-REP Roasting — R3d Buck3T](https://medium.com/r3d-buck3t/kerberos-attacks-as-rep-roasting-2549fd757b5)
- [HAFNIUM APT — CyberDefenders CTF](https://cyberdefenders.org/blueteam-ctf-challenges/hafnium-apt/)
- [APT29 / SolarWinds TTPs — MITRE](https://attack.mitre.org/groups/G0016/)
- [Conti TTPs — Lateral Movement](https://www.elisity.com/blog/lateral-movement-techniques)
- [OWASP LLM Top 10 2025 — Lasso Security Analysis](https://www.lasso.security/blog/owasp-top-10-for-llm-applications-generative-ai-key-updates-for-2025)
- [Indirect Prompt Injection in Agentic AI](https://christian-schneider.net/blog/prompt-injection-agentic-amplification/)
- [LLM CTF — SaTML 2024 Competition Dataset](https://arxiv.org/pdf/2406.07954)
- [Active Directory Attack Playbook 2026](https://www.redfoxsec.com/blog/active-directory-attack-playbook-for-red-teamers)
