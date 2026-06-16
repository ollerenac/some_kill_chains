# Architecture Research: CTF Lab VM Topology

**Project:** CTF Scenario Catalog — Advanced Cybersecurity Lab
**Researched:** 2026-06-11
**Confidence:** HIGH (network isolation mechanics, flag format conventions), MEDIUM (ATP progression design), HIGH (CTFd integration)

---

## Standalone Scenario (2-VM) Patterns

### Network Layout

The canonical 2-VM standalone layout used by HackTheBox, TryHackMe, and VirtualBox-based labs:

```
[VM1 — Attacker: Kali/Parrot]
  NIC1: NAT  (internet access for tool updates only)
  NIC2: Internal Network "lab-net" — 10.10.10.0/24 — e.g., 10.10.10.5

[VM2 — Target]
  NIC1: Internal Network "lab-net" — 10.10.10.0/24 — e.g., 10.10.10.10
  (no NAT adapter — fully isolated)
```

VirtualBox "Internal Network" mode is the right primitive: VMs on the same named internal network can communicate with each other but cannot reach the host machine or the internet. This is strictly stronger than "Host-Only" (which allows host-to-VM traffic) and the correct choice for a self-contained lab scenario.

The attacker VM's NAT adapter exists solely to allow students to run `apt update` or download tools; target VMs must never have a NAT adapter. Verified against standard VirtualBox network documentation and community lab guides.

### Flag Placement — Standalone

HackTheBox's published machine submission requirements define the de facto industry standard for 2-flag Linux/Windows standalone machines:

| Flag name | Location (Linux) | Location (Windows) | Owned by | Permission |
|-----------|------------------|--------------------|----------|------------|
| `user.txt` | `/home/<username>/user.txt` | `C:\Users\<username>\Desktop\user.txt` | root / relevant group | 644 |
| `root.txt` | `/root/root.txt` | `C:\Administrator\Desktop\root.txt` | root | 640 |

For this project's **standalone scenarios (1 flag each)**, the single flag should be the equivalent of `root.txt` — proving full compromise of the objective. The HTB pattern is worth following even for single-flag boxes because students immediately recognize the convention.

**Flag content:** HTB uses 32-character MD5 hashes as flag values. For CTFd static flags, a human-readable format `LAB{...}` with a meaningful suffix is preferable for academic settings because it self-documents the challenge topic (e.g., `LAB{kerberoast_svc_ticket_cracked}`).

### Common Standalone Configurations

**Web + PrivEsc (most common easy/medium pattern)**
- Target VM: Linux web server (Apache/Nginx) with one intentional vulnerability (SSRF, file upload, command injection, deserialization)
- Initial foothold: limited shell as `www-data` or equivalent
- Flag 1 (user): obtained after horizontal move to a user account (credential in config file, cron job abuse)
- Flag 2 (root): obtained after vertical privilege escalation (SUID binary, sudo misconfiguration, kernel exploit)
- For a 1-flag variant: place only root flag — forces students to complete full chain

**Service Exploitation (easy pattern)**
- Target VM: runs a single vulnerable service (FTP with anonymous upload, Redis no-auth, memcached, ElasticSearch)
- Flag placed where the service process has access: config directory, home directory of service account
- No privilege escalation required — teaches one focused technique

**CVE weaponization (medium/hard pattern)**
- Target VM: specific vulnerable software version pinned (Apache 2.4.49, IIS with specific misconfig)
- Student must write exploit code against the running service
- Flag placed at a path that requires code execution, not just read access (e.g., `/root/root.txt` behind a root-only process)

---

## ATP-Style Scenario (3-VM) Patterns

### The Core Isolation Problem

The central architectural question for ATP scenarios: how do you ensure VM3 (final target) is unreachable directly from VM1 (attacker)?

The answer is two separate internal networks combined with a dual-homed VM2:

```
NETWORK A: "dmz-net"    10.10.10.0/24
NETWORK B: "corp-net"   10.10.20.0/24

[VM1 — Attacker: Kali]
  NIC1: NAT (internet)
  NIC2: dmz-net  — 10.10.10.5

[VM2 — Pivot Server]
  NIC1: dmz-net  — 10.10.10.10   (reachable from VM1)
  NIC2: corp-net — 10.10.20.10   (route to VM3)

[VM3 — Final Target]
  NIC1: corp-net — 10.10.20.20   (unreachable from VM1 directly)
```

This topology is validated by the cocomelonc.github.io pivot lab writeup (10.9.1.0/24 + 7.7.1.0/24), GOAD's multi-subnet AD deployments, and the HTB Academy Pivoting & Tunneling course. It is the standard pattern across the entire industry.

**Why this enforces isolation without firewall rules:**
VirtualBox Internal Network mode creates a layer-2 segment. VM1's NIC2 is on `dmz-net`; it has no physical or virtual interface on `corp-net`. Without routing through VM2, there is no path. No explicit firewall rules are needed — the topology itself is the enforcement mechanism.

**If routing needs hardening:** Disable IP forwarding on VM2 by default (`net.ipv4.ip_forward = 0`). Students must enable it as part of the exploitation chain (demonstrates T1599 - Network Boundary Bridging awareness). This also prevents accidental bypass.

### Flag Placement — ATP

```
Flag 1 ("foothold flag")  — placed on VM2
  Location: /home/<compromised_user>/flag1.txt  OR  in a running service's data
  Proof of: initial lateral movement from VM1 to VM2
  Gate: requires successful exploitation of VM2's exposed service

Flag 2 ("objective flag") — placed on VM3
  Location: /root/flag2.txt  OR  C:\Administrator\Desktop\flag2.txt
  Proof of: second lateral movement from VM2 to VM3, plus privilege escalation on VM3
  Gate: requires pivoting through VM2 (proxychains/chisel/SSH dynamic forward)
```

**Progressive difficulty via flag gating:** Flag 2 must be physically unreachable without flag 1's artifacts. The ideal implementation: flag 1 is a credential hash, a Kerberos ticket, or a private key that is then the literal authentication material needed to reach VM3. This creates natural dependency without platform-level gating.

### ATP Network Progression Structure

Following the PROJECT.md template: two lateral movements using **different protocols**. Designed topology for protocol diversity:

| ATP Variant | VM1→VM2 technique | VM2→VM3 technique | Domain |
|-------------|-------------------|--------------------|--------|
| AD/Kerberos | SMB relay / AS-REP roasting → PTH | WinRM with stolen NTLM | Active Directory |
| Service chain | SSH with credential from web app | Redis SLAVEOF / replication abuse | Linux services |
| Mixed OS | SMB with anonymous read + cred leak | RDP pass-the-hash | Windows mixed |
| Container escape | Docker socket abuse → host shell | kubectl with leaked service token | Cloud/container |
| Network protocol | SNMP community string → device config | SSH with extracted private key | Network protocol |

Protocol diversity is the key pedagogical point: students must understand that lateral movement is not one tool but a family of techniques selected based on what the pivot host exposes.

---

## Domain-Specific Topology Notes

### Active Directory Scenarios (2-VM: Attacker + DC/Workstation)

The GOAD (Game of Active Directory) MINILAB configuration is the best reference for a minimal-VM AD lab: 2 VMs, 1 forest, 1 domain — one DC (Windows Server 2019) + one Workstation (Windows 10).

**Recommended standalone AD layout:**
```
[VM1 — Attacker: Kali]
  NIC2: ad-net — 192.168.56.5

[VM2 — DC + Workstation combined OR just DC]
  NIC1: ad-net — 192.168.56.10
  AD Domain: corp.local
  Services: DNS (53), Kerberos (88), LDAP (389), SMB (445)
```

Use the 192.168.56.0/24 range — this is the VirtualBox default host-only subnet and students recognize it from GOAD/community resources.

For a 2-VM AD scenario, the DC itself acts as both the Domain Controller and the workstation-equivalent. Attack paths that work well with just a DC:
- Kerberoasting (requires service account with SPN registered on DC)
- AS-REP Roasting (requires user account with pre-auth disabled)
- LDAP enumeration + password spraying
- DCSync (end-state: secretsdump with DA privileges)
- ADCS ESC1/ESC3 template abuse (requires AD CS role installed on DC)

For the **ATP 3-VM AD variant**, split roles: VM2 = workstation (domain-joined, user-level account), VM3 = DC (domain admin required). This creates a realistic attack path: phish/exploit workstation user → escalate to local admin → dump NTLM hash → PTH or Kerberoast → domain admin → DCSync on DC.

**Key AD network detail:** The DC must be the DNS server for the domain. Set VM2's NIC to use VM3's IP as DNS resolver. Without this, Kerberos authentication and domain join break.

### Cloud / Container Scenarios (2-VM)

```
[VM1 — Attacker: Kali with kubectl, docker client]
  NIC2: container-net — 172.16.0.5

[VM2 — Container host: Ubuntu + Docker/K3s]
  NIC1: container-net — 172.16.0.10
  Runs: Docker daemon (potentially exposed), misconfigured K3s cluster
```

Container escape scenarios do not require a third VM for the initial standalone design. The "inner container" is a process on VM2, not a separate VM. The flag placement models two levels:
- Flag 1: inside the container (obtained by compromising the containerized app)
- Flag 2: on the host VM2 filesystem at `/root/flag.txt` (obtained by escaping the container)

For ATP variants, VM3 can be an internal K8s node (only reachable via the K8s overlay network, not the lab network directly).

### Network Protocol Attack Scenarios (2-VM)

```
[VM1 — Attacker: Kali with scapy, wireshark]
  NIC2: protocol-net — 10.0.0.5

[VM2 — Target: Router/switch simulator or service host]
  NIC1: protocol-net — 10.0.0.10
  Runs: BGP (FRRouting), OSPF, SNMP, or BFD daemon
```

For BGP/routing protocol attacks, VM2 runs FRRouting on Ubuntu. Flag placed in a route advertisement (hidden community value) or as a file only accessible after routing table manipulation grants access to a "protected" service bound to a loopback interface.

---

## Flag Design Patterns

### Flag Format Recommendation

**Use:** `LAB{<descriptive_token>}` for this project.

Rationale: Platform-namespaced, self-documenting, case-sensitive (CTFd static flag default). Example: `LAB{smb_relay_ntlm_captured}`. Avoid pure MD5 hashes — they provide no pedagogical reinforcement of what was accomplished.

For multi-scenario deployments where flag sharing between students is a concern, use CTFd's HTTP flag delegation or GZ::CTF's per-team HMAC flags (`LAB{<team_hash>_<scenario_id>}`).

### Flag Location by Pedagogical Intent

| Intent | Placement | What it tests |
|--------|-----------|---------------|
| Proof of code execution | Written by exploit payload to `/tmp/flag.txt` | Exploit works and achieves RCE |
| Proof of credential access | In `/etc/shadow` readable only after escalation | Student obtained root |
| Proof of service compromise | In service response / DB record / config file | Service-layer exploitation |
| Proof of memory access | In a running process's mapped memory (readable via `/proc/PID/mem` as root) | Memory forensics / ptrace privilege |
| Proof of lateral movement | On VM2/VM3 only (unreachable without pivoting) | Pivoting technique correct |
| Proof of domain compromise | In NTDS.dit or lsass dump | Full AD compromise |

### Intermediate vs. Final Flags

**Intermediate flag (Flag 1 in ATP):** Should be findable *at the moment of initial shell*, not requiring further escalation on VM2. If students must also escalate on VM2 before getting flag 1, the scenario has three stages on two machines — too many gates. Place flag 1 as the **landing user's** flag on VM2 (owned by the compromised service account, readable without root).

**Final flag (Flag 2 in ATP):** Should require both pivoting AND privilege escalation on VM3. The two actions should be sequential, not simultaneous: get a foothold on VM3 at low privilege, then escalate. This teaches both skills.

**Anti-pattern to avoid:** Placing both flags on the same VM, forcing escalation between them. This is a privilege-escalation exercise, not an ATP scenario. Flags must be on separate VMs with a network boundary between them.

### Flag Placement by Attack Domain

**Active Directory:**
- Flag 1: `/home/svc_account/flag1.txt` (readable by service account, obtained via Kerberoasting + crack)
- Flag 2: `C:\Users\Administrator\Desktop\flag2.txt` (requires DA / DCSync)

**Web + LFI/RCE:**
- Flag 1: `/var/www/config/flag1.txt` (readable by `www-data`, obtained via RCE)
- Flag 2: `/root/flag2.txt` (requires privesc from www-data to root)

**Container Escape:**
- Flag 1: `/app/flag1.txt` inside the container
- Flag 2: `/root/flag2.txt` on the host (requires container escape)

**Network Protocol:**
- Flag 1: embedded in a BGP community string or SNMP OID (obtained by passive sniff or active query)
- Flag 2: in a file on a "management interface" loopback only routable after injecting a malicious route

**CVE Exploitation:**
- Single flag placed at a path requiring code execution (not just read): the file permission itself is part of the proof that the CVE was exploited, not just reached

---

## Build Order Implications

### Design Order for Scenario Authors

1. **Define the flag locations first.** Before writing challenge description or configuring VMs, decide exactly where each flag lives and what access level is required to read it. This anchors the attack chain and prevents post-hoc flag placement that fits poorly.

2. **Design the network topology second.** Draw the subnet diagram. Confirm VM3 (ATP) has no path from VM1 without going through VM2. This is a load-bearing decision that cannot easily be changed after VM configuration begins.

3. **Build VM2 (pivot / sole target) before VM1 and VM3.** VM2 has the most complex configuration in ATP scenarios (dual NIC, exposed service, flag 1, internal credentials for VM3). Build and test it in isolation first.

4. **Configure VM3 (final target) before connecting it to the network.** Install the OS, configure the service, place the flag, set permissions — all offline — then attach the corp-net NIC. This prevents accidental exposure during build.

5. **Build VM1 (attacker) last.** Kali/Parrot is generic; it only needs the two NICs attached and any pre-staged helper files. Build it last to validate the complete attack chain works end-to-end.

6. **Test the negative path.** From VM1, attempt to reach VM3 directly (ping, nmap to corp-net range). It must fail. Confirming isolation is a required build step, not optional.

### Dependencies Between Scenario Types

- **Standalone scenarios** are independent of each other. Build them in any order.
- **ATP scenarios** have an internal VM dependency: VM2's flag/credentials must be consistent with VM3's authentication configuration. These two VMs must be built as a pair.
- **AD scenarios** require DNS configuration to work. Build the DNS/DC configuration before testing any AD attack paths — Kerberos will silently fail without proper DNS resolution.
- **Container scenarios** require the container runtime pre-installed and the vulnerable image pre-loaded. Image pull on student start is too slow for a lab environment; bake images into the VM snapshot.

### Scenario Mix Build Order Recommendation

Build in this order to validate infrastructure choices early and minimize rework:

1. One standalone Linux web+privesc scenario (validates 2-VM internal network isolation)
2. One ATP scenario with SMB lateral movement (validates 3-VM dual-subnet topology)
3. One AD standalone scenario (validates DNS + Kerberos service configuration)
4. Remaining scenarios in parallel once the three network patterns are confirmed working

### Flag Sharing Prevention

For an academic lab where multiple student pairs run the same scenario simultaneously:

- Use CTFd HTTP flag delegation if the lab infrastructure supports per-team VM instances
- Use GZ::CTF's HMAC-based dynamic flags if running competitive/timed variants
- For static deployments where each student gets their own VM set: static `LAB{...}` flags are sufficient — no sharing risk since each student has their own isolated environment
- Never use the same flag string across different scenarios even if the technique is similar — collision prevention for the scoreboard

---

## Sources

- HackTheBox Machine Submission Requirements (flag placement standard): https://help.hackthebox.com/en/articles/5307061-machine-submission-requirements
- GOAD (Game of Active Directory) — MINILAB config, subnet ranges: https://github.com/Orange-Cyberdefense/GOAD
- cocomelonc.github.io — Three-VM pivot topology (10.9.1.0/24 + 7.7.1.0/24 dual-subnet): https://cocomelonc.github.io/pentest/2021/11/04/pivoting-1.html
- CTFd HTTP Flag Delegation docs: https://docs.ctfd.io/docs/flags/http/
- GZ::CTF Dynamic Per-Team Flags: https://gzctf.gzti.me/guide/features/dynamic-flag
- VirtualBox Internal Network mode (isolation mechanics): https://www.nakivo.com/blog/virtualbox-network-setting-guide/
- HTB Academy — Pivoting, Tunneling, and Port Forwarding course: https://academy.hackthebox.com/course/preview/pivoting-tunneling-and-port-forwarding
- MITRE ATT&CK T1021 Remote Services (lateral movement protocol taxonomy): https://attack.mitre.org/techniques/T1021/
- MITRE ATT&CK TA0008 Lateral Movement tactic: https://attack.mitre.org/tactics/TA0008/
- t3l3machus/pentest-pivoting (proxychains + SSH dynamic forward lab patterns): https://github.com/t3l3machus/pentest-pivoting
- INE Community — Lateral Movement & Pivoting CTF 1 (flag gating discussion): https://legacy-community.ine.com/t/lateral-movement-pivoting-ctf-1-can-only-get-flag-1/6027
- TryHackMe Lateral Movement & Pivoting room (multi-flag network segmentation): https://tryhackme.com/room/lateralmovementandpivoting
