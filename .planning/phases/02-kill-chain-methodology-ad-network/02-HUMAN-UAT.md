---
status: partial
phase: 02-kill-chain-methodology-ad-network
source: [02-VERIFICATION.md]
started: 2026-06-12T07:50:00Z
updated: 2026-06-12T07:50:00Z
---

## Current Test

[awaiting human testing]

## Tests

### 1. Command syntax validation — all 9 kill-chains

expected: Each stage's Expected Output matches what the tool actually prints on the lab VM; no commands fail due to flag changes or API drift in certipy v5, nxc, impacket, evil-winrm, hashcat
result: [pending]

### 2. NET-03 single-VM ARP topology confirmation

expected: A single Ubuntu 22.04 VM can run both the credential-sending client process (port 8080) and the flag service (port 80) simultaneously, and bettercap ARP poisoning (VICTIM_IP + GATEWAY_IP) correctly intercepts inter-process traffic routed through the gateway
result: [pending]

## Summary

total: 2
passed: 0
issues: 0
pending: 2
skipped: 0
blocked: 0

## Gaps
