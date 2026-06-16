# CTF Scenario Catalog — Advanced Cybersecurity Lab

## What This Is

A catalog of ~20 Capture-The-Flag scenarios designed for advanced undergraduate and graduate cybersecurity students. The scenarios fill the thematic gaps in an existing lab framework (which already covers Cryptography, Web-Hacking, Forensics, System-Hacking, Malware, ISMS, and Reversing) by adding modern attack domains: Active Directory exploitation, cloud/container security, network protocol abuse, LLM security, mini-APT chains with lateral movement, and hands-on CVE weaponization.

## Core Value

Students must deeply understand each attack technique by building and executing it themselves — not by running point-and-click tools.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] ~20 CTF scenario proposals covering modern attack domains absent from the existing library
- [ ] Each scenario uses at most 3 VMs (1 attacker workstation + up to 2 victim servers)
- [ ] Scenario mix: ~10 standalone (1 flag, 1 skill) + ~10 multi-step ATP-style (2 flags, lateral movement)
- [ ] Difficulty distribution: 5 easy / 10 medium / 5 hard
- [ ] CVE-based scenarios require students to author exploit code — no Metasploit / full-framework shortcuts
- [ ] Phase 1 deliverable: concise document with scenario titles and descriptions only
- [ ] Phase 2 deliverable: full kill-chain stages per scenario with MITRE ATT&CK TTP codes
- [ ] Kill-chain methodology agreed before Phase 2 implementation begins

### Out of Scope

- Cryptography challenges — already covered in existing lab
- General web-hacking (SQLi, XSS, basic auth bypass) — already covered
- Forensics / disk/memory analysis challenges — already covered
- Malware analysis / reverse engineering — already covered
- ISMS / policy exercises — already covered
- Metasploit-driven solutions — pedagogically excluded by design

## Context

The scenarios run inside an existing lab framework deployed on a local server. The user interface is a two-panel canvas: left panel contains the challenge description, hints, and flag-submission input; right panel (larger) shows the VM desktop. Students interact with the attacker workstation VM directly in the browser.

**ATP-style scenario template (for multi-step challenges):**
1. Attacker workstation → perform recon, discovery, or credential-access TTPs
2. Lateral movement to a pivot server → first flag is found here
3. In-host actions on pivot server (privilege escalation, data extraction)
4. Second lateral movement (different protocol than step 2) → final server with final flag

**Exploit authoring constraint:** For CVE-based scenarios, students must write the exploit themselves. Hidden helper files (payloads, partial code modules) may be pre-staged on the VM, but the student must write the execution/weaponization code. This applies to: EternalBlue/MS17-010, SMB relay attacks, web-server CVEs (Apache/IIS/Nginx), and similar.

**LLM security:** Cover both prompt injection / OWASP LLM Top-10 attacks and attacks against insecure LLM infrastructure (exposed APIs, IDOR in chat history, etc.).

## Constraints

- **VM count**: Max 3 VMs per scenario — hard infrastructure constraint
- **Tooling**: No Metasploit or fully automated exploit frameworks — manual/scripted exploitation required
- **Existing library**: Avoid duplicating topics already in the lab (Crypto, Web-Hacking, Forensics, System-Hacking, Malware, ISMS, Reversing)
- **Academic rigor**: Scenarios must be medium-to-high difficulty for advanced undergrad/grad students
- **Phase sequencing**: Phase 1 (proposals doc) must be approved before Phase 2 (kill-chains) begins

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| No Metasploit / full frameworks | Forces deep understanding vs. point-and-click; better learning outcomes | — Pending |
| Mix of standalone + ATP scenarios | Allows focused single-skill exercises alongside complex chained challenges | — Pending |
| ATP template: two lateral movements with different protocols | Teaches protocol diversity in pivoting (e.g., SMB then WinRM, or SSH then Redis) | — Pending |
| LLM hacking included | Reflects 2024-2025 threat landscape; understudied in most academic CTF libraries | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-06-11 after initialization*
