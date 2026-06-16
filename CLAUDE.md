<!-- GSD:project-start source:PROJECT.md -->
## Project

**CTF Scenario Catalog — Advanced Cybersecurity Lab**

A catalog of ~20 Capture-The-Flag scenarios designed for advanced undergraduate and graduate cybersecurity students. The scenarios fill the thematic gaps in an existing lab framework (which already covers Cryptography, Web-Hacking, Forensics, System-Hacking, Malware, ISMS, and Reversing) by adding modern attack domains: Active Directory exploitation, cloud/container security, network protocol abuse, LLM security, mini-APT chains with lateral movement, and hands-on CVE weaponization.

**Core Value:** Students must deeply understand each attack technique by building and executing it themselves — not by running point-and-click tools.

### Constraints

- **VM count**: Max 3 VMs per scenario — hard infrastructure constraint
- **Tooling**: No Metasploit or fully automated exploit frameworks — manual/scripted exploitation required
- **Existing library**: Avoid duplicating topics already in the lab (Crypto, Web-Hacking, Forensics, System-Hacking, Malware, ISMS, Reversing)
- **Academic rigor**: Scenarios must be medium-to-high difficulty for advanced undergrad/grad students
- **Phase sequencing**: Phase 1 (proposals doc) must be approved before Phase 2 (kill-chains) begins
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

## Attacker VM
### Recommended OS: Kali Linux (rolling release, currently 2025.4+)
### Pre-installed Tools by Domain
#### All Scenarios (Core Baseline)
| Tool | Package / Source | Purpose |
|------|-----------------|---------|
| nmap | `apt install nmap` | Port/service discovery |
| Wireshark / tshark | pre-installed Kali | Traffic analysis |
| Burp Suite Community | pre-installed Kali | HTTP interception |
| Python 3 + pip | pre-installed | Scripting, PoC authoring |
| Netcat (ncat) | pre-installed | Shells, port forwarding |
| Chisel | GitHub `jpillora/chisel` | TCP tunneling / pivoting |
| Ligolo-ng | GitHub `nicocha30/ligolo-ng` | Layer-3 tunneling for pivot chains |
#### AD / Windows Domain
| Tool | Package / Source | Purpose |
|------|-----------------|---------|
| NetExec (nxc) | `apt install netexec` | SMB/WinRM/LDAP enumeration, execution |
| Impacket suite | `apt install python3-impacket` | secretsdump, psexec, GetTGT, ntlmrelayx |
| evil-winrm | `gem install evil-winrm` | WinRM shell with PowerShell |
| BloodHound CE | Docker Compose (SpecterOps) | AD graph / attack path analysis |
| SharpHound | Pre-stage binary on attacker VM | BloodHound data collector (Windows .exe) |
| Rubeus | Pre-stage binary | Kerberoasting, ASREPRoast, ticket operations |
| Certipy | `pip install certipy-ad` | ADCS ESC1-ESC16 enumeration and exploitation |
| pypykatz | `pip install pypykatz` | Python Mimikatz — offline LSASS parsing |
| Responder | `apt install responder` | LLMNR/NBT-NS/mDNS poisoning |
| hashcat | `apt install hashcat` | Offline hash cracking (NTLMv2, Kerberos tickets) |
| kerbrute | GitHub `ropnop/kerbrute` | Kerberos user enumeration and brute-force |
| mitm6 | `pip install mitm6` | IPv6 rogue DHCPv6 for NTLM relay |
| krbrelayx | GitHub `dirkjanm/krbrelayx` (in Kali 2025.3+) | Kerberos relay attacks |
| PowerView (PS1) | Pre-stage on attacker | AD enumeration via PowerShell |
#### Cloud / Container Security
| Tool | Package / Source | Purpose |
|------|-----------------|---------|
| Docker CLI | `apt install docker.io` | Manage containers on victim |
| kubectl | Official install script | K8s cluster interaction |
| curl / jq | pre-installed | Query IMDS endpoints, parse JSON |
| aws-cli v2 | Official installer | Interact with simulated/real AWS metadata |
| trivy | `apt install trivy` | Container image vulnerability scanning |
| kube-hunter | `pip install kube-hunter` | K8s cluster security scanning |
#### Network Protocol Exploitation
| Tool | Package / Source | Purpose |
|------|-----------------|---------|
| Scapy | `pip install scapy` | Raw packet crafting — ARP, OSPF, BGP inject |
| Responder | `apt install responder` | Protocol poisoning (LLMNR, mDNS, WPAD) |
| impacket/ntlmrelayx | Impacket suite | NTLM relay chain |
| FRRouting (FRR) | Victim-side daemon | Routing protocol target |
| bettercap | `apt install bettercap` | ARP spoof, DNS spoof, MITM automation |
| tcpdump | pre-installed | Protocol capture and analysis |
| yersinia | `apt install yersinia` | STP, CDP, HSRP, VTP attacks |
#### LLM Security
| Tool | Package / Source | Purpose |
|------|-----------------|---------|
| curl / Postman | pre-installed (curl) | Interact with LLM API endpoints |
| Python + requests | pre-installed | Automate prompt injection attempts |
| Burp Suite | pre-installed | Intercept LLM API calls over HTTP |
| jq | pre-installed | Parse JSON API responses |
| garak | `pip install garak` | Automated LLM vulnerability probing |
#### CVE Exploitation (Manual Code Authoring)
| Tool | Package / Source | Purpose |
|------|-----------------|---------|
| Python 3 + impacket | pre-installed | EternalBlue PoC, SMB interaction |
| mysmb.py | Pre-staged helper | Required by MS17-010 manual exploit |
| pwntools | `pip install pwntools` | Binary exploitation helpers for CVE PoCs |
| gcc / make | pre-installed | Compile C-based PoC code |
| Metasploit | Available but forbidden | Pedagogy constraint — document as excluded |
| searchsploit | `apt install exploitdb` | Local CVE/exploit reference |
## Victim VM Profiles
### Profile 1: Windows Server 2019 — Domain Controller (AD scenarios)
- SMB signing disabled on member servers (default on non-DCs)
- Service accounts with weak passwords and registered SPNs (Kerberoasting)
- One or more user accounts with "Do not require Kerberos preauthentication" (ASREPRoasting)
- ADCS installed with a misconfigured certificate template (ESC1: low-priv enroll, client auth EKU, SAN controllable)
- LLMNR and NBT-NS enabled (default in older configs)
- WinRM enabled (TCP 5985)
- Domain: `corp.local` or `sevenkingdoms.local`
- Domain admin: known credential used as scenario starting point or discovered via spray
- At least one low-priv user and one service account with SPN
### Profile 2: Windows Server 2019 — Member Server (AD lateral movement scenarios)
- IIS 10 with a web application (for ADCS ESC8 relay or webshell upload)
- SMB shares with misconfigured ACLs
- WinRM enabled
- Local admin account reusing domain password (for Pass-the-Hash path)
- Windows Defender: disabled (for lab reproducibility) or configured with specific exclusions
### Profile 3: Ubuntu 22.04 LTS — Linux Pivot / Service Host
- Scenario-specific: Redis (unauthenticated, for lateral movement via Redis RCE), or
- FRRouting daemon (OSPF/BGP target), or
- Flask/Gunicorn app exposing LLM API or vulnerable web app, or
- Docker daemon (for container escape scenario)
- SSH (for pivot chains — second lateral movement hop)
### Profile 4: Ubuntu 22.04 LTS — Container/K8s Host
- Docker installed with a privileged container running as the challenge entry point
- The `cgroup release_agent` escape path (CVE class: Docker privileged misconfig)
- The `hostPath` mount escape path (Kubernetes scenario)
- For K8s: Minikube or k3s (lightweight single-node K8s) pre-installed
- Intentional misconfigs: privileged pod spec, default service account with cluster-admin binding, hostPath mount to `/`
### Profile 5: Ubuntu 22.04 LTS — LLM Application Server
- Ollama (latest release, CPU-only mode is viable for phi3/llama3.2:1b)
- phi3 (3.8B, ~2.2 GB RAM in Q4 quantization) or llama3.2:1b (1B, ~0.8 GB) as the model
- PromptMe (Flask + Ollama wrapper, fully local, no API keys) as the vulnerable chatbot UI
- OR: Damn Vulnerable LLM Agent (ReversecLabs, LangChain ReAct agent with tool-calling)
- Exposed on HTTP (port 8080 or 3000) without authentication (intentional misconfig)
- IDOR-vulnerable endpoints (chat history accessible by incrementing user ID)
### Profile 6: Windows 7 SP1 / Windows Server 2008 R2 — Legacy CVE Target
- SMBv1 enabled, SMB signing off
- No patches applied (pre-MS17-010 patch state)
- No Windows Defender (or disabled)
- NetBIOS over TCP/IP enabled
## Domain-Specific Stack Details
### AD / Windows Attacking
- VM1: Windows Server 2019 DC — `corp.local`, ADCS installed, LLMNR/NBT-NS on, SMB signing off on non-DC interfaces, SPNs registered on service accounts
- VM2: Attacker (Kali XFCE) — full AD toolchain pre-installed
- NetExec (nxc) replaces CrackMapExec — use `nxc smb`, `nxc winrm`, `nxc ldap`
- BloodHound CE (Docker Compose) replaces legacy BloodHound — uses Neo4j + Go API + React UI
- Certipy v5+ covers ESC1-ESC16; ESC1 and ESC8 are the canonical beginner-to-intermediate scenarios
- Step 1 (recon): nmap, nxc enumeration, Responder poisoning
- Step 2 (lateral → pivot): Pass-the-Hash via psexec to member server → Flag 1 on member server
- Step 3 (in-host): privilege escalation, ADCS ESC1 cert → DA impersonation
- Step 4 (second lateral → DC): evil-winrm to DC via forged certificate → Flag 2 in Administrator desktop
### Cloud / Container Security
- VM1: Ubuntu 22.04 with Docker CE. A deliberately misconfigured privileged Docker container runs automatically on boot — student lands inside the container as root.
- VM2: Attacker Kali (or the container is the only "VM" for standalone scenarios, with Kali as the attacker side)
- k3s installed: `curl -sfL https://get.k3s.io | sh -`
- Challenge pod deployed with intentional misconfig: `privileged: true` and `hostPath` mount
- student receives kubeconfig with limited rights; must enumerate pods, find misconfigured one, exec in, escape to node
- Tools on attacker: `kubectl`, `kube-hunter`
### Network Protocol Exploitation
- VM1: Ubuntu 22.04 running FRRouting (FRR) daemon — acts as a router/switch in a small simulated network
- VM2: Kali attacker with Scapy, Responder, bettercap, yersinia
- `scapy`: canonical packet crafting; supports OSPF, BGP, ARP, DNS, IPv6 RA layers
- `FRRouting (FRR)`: production-grade, runs on Ubuntu, supports OSPF/BGP/RIP/IS-IS; `apt install frr`
- `yersinia`: Layer 2 attacks (STP root bridge takeover, HSRP active router takeover)
- `bettercap`: higher-level MITM orchestration; useful for scenario setup/teardown scripts
### LLM Security
- VM1: Ubuntu 22.04 — Ollama + vulnerable chatbot application (LLM server)
- VM2: Kali attacker (or web browser from attacker VM to LLM server's HTTP UI)
| App | Stack | OWASP LLM Mapping | CTF Suitability |
|-----|-------|-------------------|-----------------|
| PromptMe (OWASP project) | Python Flask + Ollama | LLM01-LLM10, direct mapping | Best for structured OWASP-aligned labs |
| Bishop Fox LLM CTF Lab | Go + Ollama + phi3 | LLM01 (prompt injection), LLM07 (system prompt leakage) | Best for multi-stage gatekeeper bypass |
| Damn Vulnerable LLM Agent (ReversecLabs) | Python + LangChain ReAct + Ollama | LLM02 (insecure output), LLM08 (plugin misuse) | Best for agent/tool-calling IDOR scenarios |
| AI Goat | Docker Compose, e-commerce chatbot | LLM01-LLM09, 9 labs | Best for a full suite but heavier deployment |
### Mini-APT Lateral Movement Chains
- VM1: Windows Server 2019 DC or Ubuntu pivot server
- VM2: Kali attacker
| First Hop | Second Hop | Victim VM 1 | Victim VM 2 |
|-----------|-----------|-------------|-------------|
| SMB (psexec/smbexec) | WinRM (evil-winrm) | Win Server member server | DC or another Windows host |
| SSH | Redis RCE | Ubuntu pivot (SSH) | Ubuntu with Redis unauthenticated |
| NTLM relay → shell | MSSQL xp_cmdshell | Ubuntu Samba host | Win Server with MSSQL |
| WinRM | DCOM/WMI | Win Server workstation | DC |
- Ligolo-ng: set up TUN interface on attacker, route traffic to internal subnet through the pivot
- Chisel: SOCKS5 proxy through pivot for tools that don't support proxychains natively
- proxychains4: route Impacket / nxc calls through SSH or Chisel SOCKS proxy
- evil-winrm, nxc, impacket: post-pivot lateral movement tools
### CVE Exploitation (Manual, No Metasploit)
#### EternalBlue (MS17-010)
#### Log4Shell (CVE-2021-44228)
#### Apache Struts S2-045 (CVE-2017-5638)
# Skeleton provided to students:
#### ProxyLogon (CVE-2021-26855 + CVE-2021-27065)
## Confidence Notes
| Area | Confidence | Basis | Caveats |
|------|------------|-------|---------|
| Kali as attacker OS | HIGH | Industry standard, HTB/OSCP ecosystem, Kali.org official docs | Parrot is a viable lighter alternative if RAM is critically constrained |
| NetExec replacing CME | HIGH | GitHub `Pennyw0rth/NetExec`, Kali package tracker, multiple community sources | `cme` command may still work as alias in some installs; use `nxc` |
| BloodHound CE vs Legacy | HIGH | SpecterOps official announcement, GitHub BloodHound-Legacy archived | Legacy collectors incompatible with CE — do not mix |
| GOAD as AD lab reference | HIGH | Orange Cyberdefense official docs, active GitHub | Full GOAD/GOAD-Light need 3-5 VMs; use MINILAB (1 DC + 1 workstation) for 2-VM budget |
| Certipy v5 (ESC1-ESC16) | HIGH | Multiple 2024-2025 blog posts cross-referencing official tool changelog | ESC15 (CVE-2024-49019) requires unpatched CA; verify Server 2019 patch level |
| Ollama phi3 CPU-only viability | MEDIUM | localaimaster.com specs guide, confirmed by multiple 2025 hardware guides | Response speed (~3-5 tok/s) is acceptable for labs but must be tested on actual lab hardware |
| Docker cgroup release_agent escape | HIGH | Trail of Bits original research, HackTricks, Rapid7 module, well-documented | Requires `--privileged` or `CAP_SYS_ADMIN`; patch status of Docker version matters |
| k3s for single-VM K8s | MEDIUM | k3s.io official docs, community guides | Nested virtualization may be required if Ubuntu VM is itself virtualized; verify hypervisor support |
| Redis lateral movement | MEDIUM | HackTricks, ired.team, multiple HTB writeups | Redis 7+ has auth by default; victim must be deliberately misconfigured with no auth (`requirepass ""`) |
| EternalBlue manual PoC structure | HIGH | worawit/MS17-010 GitHub (original), AutoBlue project, Null Byte tutorial | Windows 10/Server 2016+ are patched and won't be vulnerable; must use Win7/2008R2 victim |
| Log4Shell Docker lab | HIGH | axelcurmi/log4shell-docker-lab GitHub, christophetd vulnerable app image, Snyk advisory | log4j 2.15.0+ patched; victim image must be pinned to vulnerable version |
| IMDS simulation via loopback | MEDIUM | General Linux networking knowledge, cross-referenced with AWS IMDS docs | Requires `ip addr add 169.254.169.254/32 dev lo` to work; some hypervisors intercept 169.254/16 range |
| PromptMe as OWASP LLM CTF framework | MEDIUM | OWASP official project page, IBM Security Medium post, GitHub README | Project activity should be verified before depending on it; check last commit date |
| LLM security domain overall | MEDIUM | Multiple 2024-2025 blog posts and open source projects; rapidly evolving space | OWASP LLM Top 10 v2 released late 2024 — confirm mapping aligns with current version |
| Network protocol (OSPF Scapy) | MEDIUM | Scapy documentation, microlab.red blog, academic papers | Scapy's OSPF layer requires `from scapy.contrib.ospf import *`; not auto-imported; test before deployment |
| Exchange/ProxyLogon as victim | LOW | CVE is well-documented but Exchange Server is resource-heavy; not validated in 2-VM budget | Recommend deprioritising in favor of lighter web CVE targets (Struts, Log4j) |
## Sources
- [Kali Linux official tools list](https://www.kali.org/tools/)
- [NetExec GitHub (CrackMapExec successor)](https://github.com/Pennyw0rth/NetExec)
- [BloodHound Community Edition announcement](https://securityboulevard.com/2023/08/bloodhound-community-edition-a-new-era/)
- [GOAD official documentation](https://orange-cyberdefense.github.io/GOAD/)
- [GOAD-Light VM config](https://orange-cyberdefense.github.io/GOAD/labs/GOAD-Light/)
- [Certipy ADCS ESC1/ESC8 guide](https://hivesecurity.gitlab.io/blog/adcs-abuse-certipy-esc1-esc8-attack-chains/)
- [Kubernetes Goat container escape scenario](https://madhuakula.com/kubernetes-goat/docs/scenarios/scenario-4/container-escape-to-the-host-system-in-kubernetes-containers/welcome/)
- [Docker privileged escape — Trail of Bits](https://blog.trailofbits.com/2019/07/19/understanding-docker-container-escapes/)
- [Bishop Fox LLM CTF Lab](https://bishopfox.com/blog/large-language-models-llm-ctf-lab)
- [PromptMe — OWASP project](https://owasp.org/www-project-promptme/)
- [Damn Vulnerable LLM Agent (ReversecLabs)](https://github.com/ReversecLabs/damn-vulnerable-llm-agent)
- [Ollama system requirements 2026](https://localaimaster.com/blog/ollama-system-requirements)
- [worawit/MS17-010 manual exploit](https://github.com/worawit/MS17-010)
- [AutoBlue-MS17-010 (no Metasploit)](https://github.com/3ndG4me/AutoBlue-MS17-010)
- [Log4Shell Docker lab](https://github.com/axelcurmi/log4shell-docker-lab)
- [Apache Struts CVE-2017-5638 Docker image](https://hub.docker.com/r/piesecurity/apache-struts2-cve-2017-5638/)
- [ProxyLogon PoC (Python)](https://github.com/praetorian-inc/proxylogon-exploit)
- [OWASP LLM Top 10 2025](https://aembit.io/blog/owasp-top-10-llm-risks-explained/)
- [Scapy packet crafting](https://scapy.net/)
- [FRRouting (FRR) documentation](https://frrouting.org/)
- [Kali Linux vs Parrot OS 2025 comparison](https://pentescope.com/kali-vs-parrot-pentesting/)
- [NTLM relay and Responder — HackTricks](https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/spoofing-llmnr-nbt-ns-mdns-dns-and-wpad-and-relay-attacks)
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
