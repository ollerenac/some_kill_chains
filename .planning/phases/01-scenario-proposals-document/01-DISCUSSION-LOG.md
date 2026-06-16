# Phase 1: Scenario Proposals Document - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-11
**Phase:** 1-Scenario Proposals Document
**Areas discussed:** Scenario list, Description depth, Metadata per entry, Review format

---

## Scenario list

### Q1: NET-01 vs AD-02 overlap

| Option | Description | Selected |
|--------|-------------|----------|
| Keep both (23 total) | They target different domains — NET covers network-layer protocol abuse, AD covers Windows identity abuse | ✓ |
| Merge into one (22 total) | Consolidate into a single AD scenario | |
| Replace NET-01 with something distinct | Swap NET-01 for a different NET scenario | |

**User's choice:** Keep both
**Notes:** User confirmed they are "distinct enough." After explanation of the technical difference (LLMNR broadcast poisoning vs. SMB signing misconfiguration), user was satisfied both have independent learning value.

---

### Q2: 23 vs ~20 scenario count

| Option | Description | Selected |
|--------|-------------|----------|
| Keep 23 (Recommended) | ~20 was always approximate; extra 3 add domain coverage | ✓ |
| Trim to 20 | Drop 3 lower-priority entries | |

**User's choice:** Keep 23
**Notes:** No specific scenarios flagged for removal.

---

## Description depth

### Q1: What the 3-5 sentences cover

| Option | Description | Selected |
|--------|-------------|----------|
| Attack narrative only | Pure student-facing story: what they see, do, obtain | ✓ |
| Attack + learning objective | Narrative plus why this scenario is in the catalog | |
| Attack + learning objective + VM roles | Narrative, learning objective, VM role line | |

**User's choice:** Attack narrative only

---

### Q2: Person/voice

| Option | Description | Selected |
|--------|-------------|----------|
| Student POV — second person | "You are a red-team operator..." — immersive CTF style | ✓ |
| Neutral — third person | "The student exploits..." — clinical, scannable | |

**User's choice:** Second person (student POV)

---

### Q3: Tool specificity

| Option | Description | Selected |
|--------|-------------|----------|
| Technique-level, no specific tools | Keeps descriptions pitch-clean | |
| Name key tools where they define the scenario | Mention canonical tools only when the tool IS the learning point | ✓ |

**User's choice:** Name key tools where they define the scenario

---

## Metadata per entry

### Q1: Field set per scenario

| Option | Description | Selected |
|--------|-------------|----------|
| Title + description only | Minimal | |
| Title + difficulty + VM count + description | Sufficient for feasibility and difficulty assessment | ✓ |
| Full header: title + difficulty + VM count + standalone/ATP flag + description | Maximum metadata | |

**User's choice:** Title + difficulty + VM count + description

---

### Q2: Multi-step ATP visual distinction

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — label them | Add [Multi-step — 2 flags] tag next to title | ✓ |
| No — let the description convey it | No extra tag needed | |

**User's choice:** Yes — label with [Multi-step — 2 flags]

---

## Review format

### Q1: Review workflow

| Option | Description | Selected |
|--------|-------------|----------|
| Read end-to-end, then approve or request edits | Wholesale review | ✓ |
| Per-scenario approve/revise/drop markers | Mark each scenario before Phase 2 | |
| Grouped domain-by-domain review | Review by domain block | |

**User's choice:** Wholesale review

---

### Q2: Document opening

| Option | Description | Selected |
|--------|-------------|----------|
| Brief intro first | 3-5 line preamble: purpose, VM limit, no-Metasploit | ✓ |
| Scenarios only, no intro | Jump straight into entries | |

**User's choice:** Brief intro first

---

## Claude's Discretion

- Exact wording of the intro section preamble (content locked; phrasing open)
- Ordering of scenarios within each domain section (by ID or narrative flow — either acceptable)

## Deferred Ideas

None — discussion stayed within Phase 1 scope.
