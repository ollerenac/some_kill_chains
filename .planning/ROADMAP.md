# Roadmap: CTF Scenario Catalog

**4 phases** | **23 requirements** | Generated: 2026-06-11

---

## Phases

- [x] **Phase 1: Scenario Proposals Document** — Produce the complete catalog of 23 scenario titles and descriptions, organized by domain (completed 2026-06-11)
- [x] **Phase 2: Kill-Chain Methodology + AD/Network Scenarios** — Align on kill-chain methodology, then author detailed kill-chains for AD and Network scenarios (completed 2026-06-12)
- [x] **Phase 3: CVE + Cloud/Container Kill-Chains** — Author detailed kill-chains for CVE weaponization and Cloud/Container scenarios (completed 2026-06-12)
- [ ] **Phase 4: LLM + ATP Chain Kill-Chains + Final Review** — Author kill-chains for LLM and ATP scenarios, then final consistency review across all 23

---

## Phase Details

### Phase 1: Scenario Proposals Document

**Goal:** A single reviewable document (`SCENARIOS.md`) containing all 23 scenario titles and descriptions organized by domain — no kill-chain steps, no TTP codes, no implementation details. This is the artifact the user approves before Phase 2 begins.
**Mode:** mvp
**Depends on:** Nothing
**Requirements:** AD-01, AD-02, AD-03, AD-04, AD-05, NET-01, NET-02, NET-03, NET-04, CVE-01, CVE-02, CVE-03, CVE-04, CC-01, CC-02, CC-03, LLM-01, LLM-02, LLM-03, ATP-01, ATP-02, ATP-03, ATP-04
**Success Criteria:**

1. `SCENARIOS.md` exists and contains all 23 scenarios with title, difficulty rating, VM count, and a 3-5 sentence description for each
2. All six domains are represented with correct scenario counts (AD: 5, NET: 4, CVE: 4, CC: 3, LLM: 3, ATP: 4)
3. No scenario description contains kill-chain steps, MITRE TTP codes, or implementation specifics — descriptions are pitch-level only
4. User can read the document end-to-end and make approve/revise/reject decisions on each scenario without needing additional context

**Plans:** 1/1 plans complete

Plans:

- [x] 01-01-PLAN.md — Author all 23 scenario entries and produce SCENARIOS.md

### Phase 2: Kill-Chain Methodology + AD/Network Scenarios

**Goal:** A methodology section establishing the kill-chain format and TTP notation standard, followed by fully detailed kill-chain write-ups for all 9 AD and Network scenarios (AD-01..05, NET-01..04). These are the most technically mature domains and establish the template all subsequent phases follow.
**Mode:** mvp
**Depends on:** Phase 1 (approved SCENARIOS.md)
**Requirements:** AD-01, AD-02, AD-03, AD-04, AD-05, NET-01, NET-02, NET-03, NET-04
**Success Criteria:**

1. A methodology section defines the kill-chain stage format, MITRE ATT&CK TTP citation style, flag placement conventions, and VM role labeling — all subsequent phases use this format without deviation
2. All 9 AD/Network scenarios have complete kill-chain write-ups: numbered stages, attacker actions, expected outputs, and at least one MITRE TTP code per stage
3. The two multi-step ATP scenarios in this set (AD-05) have Flag 1 and Flag 2 placements explicitly marked at the correct lateral movement boundaries
4. Each kill-chain is internally consistent with the scenario description written in Phase 1

**Plans:** 1/1 plans complete

Plans:

- [x] 02-01-PLAN.md — Kill-chain methodology preamble + kill-chains for AD-01..05, NET-01..04

### Phase 3: CVE + Cloud/Container Kill-Chains

**Goal:** Fully detailed kill-chain write-ups for all 7 CVE weaponization and Cloud/Container scenarios (CVE-01..04, CC-01..03), following the methodology established in Phase 2. CVE scenarios must specify the exact exploit authoring steps students must implement themselves.
**Mode:** mvp
**Depends on:** Phase 2 (methodology established)
**Requirements:** CVE-01, CVE-02, CVE-03, CVE-04, CC-01, CC-02, CC-03
**Success Criteria:**

1. All 4 CVE scenarios have kill-chains that explicitly identify which code the student must author (e.g., the weaponization class, the payload delivery function) versus what is pre-staged as scaffold
2. All 3 Cloud/Container scenarios have kill-chains that trace the full privilege escalation path from initial access to flag retrieval, with cloud-specific TTP codes (e.g., T1552.005 for IMDS credential theft)
3. No CVE scenario kill-chain references Metasploit or automated exploit framework steps at any stage
4. All 7 kill-chains conform to the stage format and TTP citation style defined in Phase 2

**Plans:** 4/4 plans complete

Plans:
**Wave 1**

- [x] 03-01-PLAN.md — D-05 CVE-03 identity correction (Struts S2-045) + KILL-CHAINS.md section anchors

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 03-02-PLAN.md — CVE-01 EternalBlue + CVE-02 Log4Shell kill-chains

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 03-03-PLAN.md — CVE-03 Struts S2-045 + CVE-04 PrintNightmare kill-chains

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 03-04-PLAN.md — CC-01 IMDS SSRF + CC-02 Docker cgroup escape + CC-03 K8s hostPath + consistency table

### Phase 4: LLM + ATP Chain Kill-Chains + Final Review

**Goal:** Fully detailed kill-chain write-ups for all 7 LLM and ATP chain scenarios (LLM-01..03, ATP-01..04), followed by a cross-catalog consistency review that ensures uniform format, difficulty calibration, and TTP coverage across all 23 scenarios.
**Mode:** mvp
**Depends on:** Phase 3
**Requirements:** LLM-01, LLM-02, LLM-03, ATP-01, ATP-02, ATP-03, ATP-04
**Success Criteria:**

1. All 3 LLM scenarios have kill-chains that identify the specific injection technique(s) required and the defense layers the student must bypass (e.g., system prompt + regex filter + semantic validation for LLM-01)
2. All 4 ATP chain scenarios have kill-chains with exactly two flag placements at the specified lateral movement boundaries, with each lateral movement using a distinct protocol as required by the ATP template
3. The complete catalog (all 23 scenarios) passes a consistency check: uniform stage formatting, no missing TTP codes, difficulty ratings that match kill-chain complexity, and no duplicate TTP coverage across scenarios in the same domain
4. The final document is ready for handoff to lab instructors without further editorial work

**Plans:** 5 plans

**Wave 1**

- [x] 04-01-PLAN.md — LLM Security section header + LLM-01 (multi-layer prompt injection) + LLM-02 (RAG indirect injection) kill-chains

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 04-02-PLAN.md — LLM-03 (IDOR in chat history API) kill-chain

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 04-03-PLAN.md — ATP section header + ATP-01 (HAFNIUM-style SSRF pivot) + ATP-02 (SolarWinds-style supply chain + DNS C2) kill-chains

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 04-04-PLAN.md — ATP-03 (LAPSUS$-style cloud identity chain) + ATP-04 (Volt Typhoon-style IPv6 relay chain) kill-chains + Consistency Verification table extension (7 new rows)

**Wave 5** *(blocked on Wave 4 completion)*

- [ ] 04-05-PLAN.md — Cross-catalog consistency review (all 23 scenarios, 4 dimensions per D-17) + REVIEW.md + inline fixes

---

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Scenario Proposals Document | 1/1 | Complete   | 2026-06-11 |
| 2. Kill-Chain Methodology + AD/Network | 1/1 | Complete   | 2026-06-12 |
| 3. CVE + Cloud/Container Kill-Chains | 4/4 | Complete   | 2026-06-12 |
| 4. LLM + ATP Chain Kill-Chains + Final Review | 0/5 | Ready to execute | - |
