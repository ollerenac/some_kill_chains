# CTF Scenario Catalog — Advanced Cybersecurity Lab

This catalog presents 23 proposed Capture-The-Flag scenarios for advanced undergraduate and graduate cybersecurity students. Each scenario is designed to fill thematic gaps in an existing lab framework by covering modern attack domains not yet represented: Active Directory exploitation, network protocol abuse, CVE weaponization, cloud and container security, LLM security, and multi-step APT-style attack chains. Every scenario runs on a maximum of three virtual machines — this is a hard infrastructure constraint. Students are required to author all exploit and weaponization code themselves; fully automated frameworks such as Metasploit are excluded by design.

---

## Active Directory / Windows

### AD-01: Kerberoasting and AS-REP Roasting

**Difficulty:** Easy
**VMs:** 2

You are a low-privileged domain user on a Windows domain littered with service accounts carrying registered SPNs and user accounts configured without Kerberos pre-authentication. Your objective is to enumerate both attack surfaces, collect service tickets and AS-REP blobs, and crack them offline with Hashcat to recover the credentials that unlock the flag. Using GetUserSPNs.py alongside targeted enumeration, you identify which accounts are vulnerable to each technique and gather the ticket material needed for offline analysis. The flag is contained within the material you recover after successful cracking.

---

### AD-02: LLMNR/NBT-NS Poisoning and NTLM Relay

**Difficulty:** Medium
**VMs:** 2

You are positioned on a Windows domain network where LLMNR and NBT-NS broadcast name resolution remains enabled — a misconfiguration that lets any host on the segment respond to unresolved name queries. Using Responder, you poison broadcast requests and capture NTLMv2 challenge-response hashes from domain users authenticating to a non-existent resource. Rather than cracking the captured hash, you pipe it directly through ntlmrelayx to relay the credential to a domain service, obtaining command execution on a target workstation and the flag without ever recovering a plaintext password.

---

### AD-03: BloodHound ACL Abuse Path

**Difficulty:** Medium
**VMs:** 2

You have obtained a low-privileged domain account and need to escalate your access to Domain Admin. Using SharpHound to collect Active Directory relationship data and BloodHound to visualize attack paths, you identify a chain of abusable Access Control List edges — specifically a WriteDACL or GenericWrite permission held by your compromised account over a higher-privileged object. You exploit this edge to grant yourself the rights needed for further escalation, chaining the steps until you hold Domain Admin and retrieve the flag.

---

### AD-04: ADCS ESC1 Certificate Abuse

**Difficulty:** Hard
**VMs:** 2

You hold a low-privileged domain account and discover that the organization has deployed Active Directory Certificate Services with a misconfigured certificate template. The template allows low-privileged users to enroll, carries the Client Authentication EKU, and permits the Subject Alternative Name to be specified by the requestor. Using Certipy, you enumerate the vulnerable template, request a rogue certificate impersonating a Domain Admin account, and authenticate via PKINIT to obtain a Kerberos ticket-granting ticket for that privileged account — giving you Domain Admin access and the flag.

---

### AD-05: Conti-Style APT Chain  [Multi-step — 2 flags]

**Difficulty:** Hard
**VMs:** 3

You enter a three-machine Windows domain environment with only an attacker workstation and no credentials. Deploying Responder to poison LLMNR broadcast requests on the internal segment, you use ntlmrelayx to relay captured hashes over SMB to a domain member server — establishing a foothold that yields the first flag. With your pivot position secured, you use Rubeus to request service tickets for Kerberoastable accounts, crack the ticket offline with Hashcat, and use the recovered credentials with evil-winrm to move laterally to the domain controller and retrieve the second flag. Each lateral movement hop uses a distinct protocol — SMB for the first, WinRM for the second.

---

## Network Protocol Exploitation

### NET-01: SMB Relay via Unsigned Shares

**Difficulty:** Easy
**VMs:** 2

You discover a network segment where SMB signing is not enforced on workstations — a common misconfiguration in environments that have never hardened their default Windows settings. Placing Responder in analysis mode to avoid poisoning and using ntlmrelayx to relay captured authentication attempts, you intercept a domain user's SMB authentication and relay it in real time to a file share on a target host. The relayed credential grants you read access to the share containing the flag, with no need to crack or recover any password.

---

### NET-02: IPv6 Rogue DHCPv6 and LDAP Relay

**Difficulty:** Medium
**VMs:** 2

You observe that the target Windows domain has no IPv6 management in place, leaving all hosts susceptible to rogue DHCPv6 advertisements. Using mitm6, you stand up a rogue DHCPv6 server that assigns itself as the IPv6 default gateway and DNS server for domain hosts, causing them to send WPAD proxy authentication requests to your attacker machine. You relay these authentication attempts to LDAP via ntlmrelayx, leveraging the relayed credential to create a new privileged domain account — no code execution, no malware, no hash cracking required. You use the newly created account to authenticate and retrieve the flag.

---

### NET-03: ARP Cache Poisoning and Credential Interception

**Difficulty:** Easy
**VMs:** 2

You are on the same Layer 2 segment as two communicating hosts and must intercept their traffic. Using bettercap, you send gratuitous ARP replies to poison the ARP caches of both targets, routing their traffic through your machine and positioning yourself as the man-in-the-middle. You exploit bettercap's HTTPS proxy to downgrade encrypted connections to plaintext HTTP, capturing the credentials transmitted by the hosts and using them to retrieve the flag.

---

### NET-04: DNS Cache Poisoning

**Difficulty:** Medium
**VMs:** 2

You identify a DNS resolver deployed in the target network that is misconfigured to accept responses without adequate source-port randomization or query ID validation. By injecting forged DNS responses that race ahead of the legitimate upstream resolver, you corrupt the resolver's cache so that a targeted internal hostname resolves to an IP address you control. When a legitimate internal service queries the poisoned name and sends its HTTP request to your machine, the flag is embedded in that intercepted request.

---

## CVE Weaponization

### CVE-01: EternalBlue — MS17-010 (CVE-2017-0144)

**Difficulty:** Hard
**VMs:** 2

You face a Windows 7 SP1 target with SMBv1 enabled and no security patches applied — the exact environment that made CVE-2017-0144 one of the most destructive vulnerabilities in history. Rather than reaching for an automated framework, you author a Python exploit that implements the SMBv1 transaction setup, heap grooming, and DoublePulsar shellcode staging yourself, using the provided `mysmb.py` protocol scaffold as your foundation. You craft the malformed FEA list that triggers the buffer overflow, stage your payload through the DoublePulsar implant, and obtain a shell on the target from which you retrieve the flag. Completing this scenario requires you to understand the SMBv1 protocol framing at the packet level — not just execute a pre-built tool.

---

### CVE-02: Log4Shell — CVE-2021-44228

**Difficulty:** Medium
**VMs:** 2

You identify a Java application that logs attacker-controlled input using a vulnerable version of the Apache Log4j library. Rather than using a pre-built exploit kit, you author a JNDI injection payload string and build a Python-based exploit chain server that serves both an LDAP redirect and a malicious Java class over HTTP. When the application logs your crafted input, the Log4j library initiates an outbound JNDI lookup to your server, downloads and executes your class, and you achieve OS command execution on the target — recovering the flag through the resulting shell.

---

### CVE-03: Spring4Shell — CVE-2022-22965

**Difficulty:** Medium
**VMs:** 2

You discover a Java web application built on Spring MVC, deployed as a WAR on a servlet container, and running on Java 9 or later — the prerequisite conditions for CVE-2022-22965. You write the exploit: an HTTP request that abuses the Spring data-binding mechanism to traverse the ClassLoader property chain via the AccessLogValve, manipulating the logging configuration to write a JSP webshell file to the application's deployment directory. Once the webshell is planted, you use it to execute commands and retrieve the flag embedded on the target server.

---

### CVE-04: PrintNightmare (CVE-2021-1675 / CVE-2021-34527)

**Difficulty:** Medium
**VMs:** 2

You have obtained a low-privileged interactive session on a Windows Server target and need to escalate to SYSTEM. The Windows Print Spooler service is running and the target is unpatched against PrintNightmare. You author a C or Python payload that instructs the Windows Print Spooler service — which runs as SYSTEM — to load a malicious DLL you supply, injecting your code into a SYSTEM-level process. Once your payload executes with elevated privileges, you retrieve the flag from a location accessible only to SYSTEM. This scenario exercises the local privilege escalation path, requiring a pre-existing foothold rather than an external network position.

---

## Cloud / Container Security

### CC-01: IMDS SSRF and IAM Credential Theft

**Difficulty:** Easy
**VMs:** 2

You discover a web application that makes server-side HTTP requests based on attacker-controlled input — a classic Server-Side Request Forgery surface. By crafting requests that target the simulated AWS Instance Metadata Service endpoint at 169.254.169.254, you retrieve the IAM role credentials attached to the application's host. Using those stolen temporary credentials, you query a simulated S3 API to enumerate available objects and retrieve the flag stored in the bucket. No authentication bypass or code execution is required — the SSRF vulnerability does the work.

---

### CC-02: Privileged Docker Container Escape

**Difficulty:** Medium
**VMs:** 2

You land inside a deliberately misconfigured Docker container running as root with elevated Linux capabilities. From inside the container, you discover that the privilege level granted to this container extends access to host kernel interfaces that are normally isolated from container namespaces. You write a payload that abuses a cgroup notification path to schedule command execution on the underlying host, planting a reverse connection or reading the flag directly from the host's root directory. The challenge tests your understanding of Linux container isolation boundaries and the conditions under which a privileged container ceases to provide meaningful separation from the host.

---

### CC-03: Kubernetes Misconfigured Service Account Escape

**Difficulty:** Hard
**VMs:** 2

You gain initial access to a Kubernetes cluster as a low-privileged user and receive a service account token with more permissions than intended. Using kubectl, you enumerate cluster resources — pods, roles, role bindings, and secrets — to map the extent of the over-provisioned permissions. You construct and deploy a privileged pod spec with a hostPath volume that mounts the host node's root filesystem, then exec into the pod to access the host filesystem directly and retrieve the flag planted in the node's root directory.

---

## LLM Security

### LLM-01: Multi-Layer Prompt Injection Bypass

**Difficulty:** Easy
**VMs:** 2

You interact with an Ollama-backed chatbot that appears to resist your initial injection attempts — the application enforces a system prompt boundary, a regex-based filter on common injection patterns, and a semantic validation layer that checks whether your input looks like an attack. Your objective is to chain at least two distinct bypass techniques to break through the layered defenses, override the system prompt, and cause the model to output a hidden flag embedded in the LLM's context. Understanding how each defense layer fails individually — and how they can be bypassed in sequence — is the core challenge.

---

### LLM-02: Indirect Prompt Injection via RAG Document Poisoning

**Difficulty:** Medium
**VMs:** 2

You discover a chatbot application that uses Retrieval-Augmented Generation, ingesting external documents into a vector database to enrich its responses. You craft a malicious document containing injected instructions hidden within otherwise benign content and cause it to be ingested into the vector store. When a legitimate user submits a routine query, the chatbot retrieves your poisoned document as relevant context, and the embedded instructions trigger — causing the model to output the flag. This scenario explores the attack surface introduced when an LLM blindly trusts externally sourced content retrieved from its knowledge base.

---

### LLM-03: IDOR in Chat History API

**Difficulty:** Medium
**VMs:** 2

You interact with an LLM application that stores conversation history and exposes an API endpoint for retrieving past chat sessions. The endpoint uses predictable, sequential conversation identifiers and performs no meaningful access control validation — an insecure direct object reference vulnerability at the application layer. By enumerating conversation IDs through the endpoint, you access chat sessions belonging to other users, eventually reaching a privileged user's conversation that contains the flag. The challenge lies entirely in the application's failure to authenticate ownership of the requested resource.

---

## Multi-Step APT Chains

### ATP-01: HAFNIUM-Style Webshell and Lateral Movement  [Multi-step — 2 flags]

**Difficulty:** Hard
**VMs:** 3

You begin with knowledge of an internet-facing web application that processes user-supplied URLs in a server-side context. By crafting SSRF payloads, you reach an internal service inaccessible from the outside, and by escalating that access you upload a webshell to the application server that grants you code execution. Harvesting credentials found on the compromised web tier, you use them with evil-winrm to authenticate to an internal Windows pivot host — securing your first objective and retrieving the first flag. From the pivot, you enumerate domain resources and identify a path to the domain controller, following it to retrieve the second flag and complete the chain.

---

### ATP-02: SolarWinds-Style Supply Chain Backdoor  [Multi-step — 2 flags]

**Difficulty:** Hard
**VMs:** 3

You are handed access to a simulated software update distribution server — the upstream source that downstream targets trust implicitly. You modify an update package to include a backdoor that executes silently when the downstream target applies the update, and once the backdoored update runs on the downstream host you retrieve the first flag from the compromised target. With your foothold established, you shift to the second objective: a further-isolated target that is not directly reachable from your position. You establish a covert command-and-control channel by tunneling communications through DNS using dnscat2, bypassing the network segmentation, and retrieving the second flag from the isolated host.

---

### ATP-03: LAPSUS$-Style Cloud Identity Chain  [Multi-step — 2 flags]

**Difficulty:** Hard
**VMs:** 3

You identify an SSRF vulnerability in a cloud-hosted application and use it to query the Instance Metadata Service, stealing a Kubernetes service account token that was inadvertently exposed in the metadata response. Using kubectl with the stolen token, you enumerate cluster resources and discover a misconfigured privileged pod that grants you access to the host node — escaping the container boundary and securing the first flag from the node filesystem. From the node, you query the etcd datastore directly, extracting the stored Kubernetes secrets and credentials it holds. Using the recovered credentials to authenticate as an administrator on the final internal target, you retrieve the second flag and complete the cloud identity chain.

---

### ATP-04: Volt Typhoon Living-Off-the-Land Chain  [Multi-step — 2 flags]

**Difficulty:** Hard
**VMs:** 3

You operate under a no-malware constraint — no compiled payloads, no shellcode, no persistent implants. Using mitm6 to deploy a rogue DHCPv6 server and relaying the resulting authentication attempts to LDAP via ntlmrelayx, you create a new privileged domain account without touching the filesystem of any target host. With the new account, you use evil-winrm to authenticate to a domain member server and retrieve the first flag. From the pivot, you enumerate service account SPNs with Kerberoasting, crack the recovered ticket hash offline, and use the resulting credential with SMBExec or DCOM to authenticate to the domain controller and retrieve the final flag — the entire chain executed without dropping a single malicious file.
