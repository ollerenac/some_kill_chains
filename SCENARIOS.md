# CTF Scenario Catalog — Advanced Cybersecurity Lab

This catalog presents 23 proposed Capture-The-Flag scenarios for advanced undergraduate and graduate cybersecurity students. Each scenario is designed to fill thematic gaps in an existing lab framework by covering modern attack domains not yet represented: Active Directory exploitation, network protocol abuse, CVE weaponization, cloud and container security, LLM security, and multi-step APT-style attack chains. Every scenario runs on a maximum of three virtual machines — this is a hard infrastructure constraint. Students are required to author all exploit and weaponization code themselves; fully automated frameworks such as Metasploit are excluded by design.

---

## Active Directory / Windows

### AD-01: Kerberoasting and AS-REP Roasting

**Difficulty:** Easy
**VMs:** 2

You are a low-privileged domain user on a Windows domain littered with service accounts carrying registered SPNs and user accounts configured without Kerberos pre-authentication. Your objective is to enumerate both attack surfaces, collect service tickets and AS-REP blobs, and crack them offline with Hashcat to recover the credentials that unlock the flag. Using GetUserSPNs.py alongside targeted enumeration, you identify which accounts are vulnerable to each technique and gather the ticket material needed for offline analysis. The flag is contained within the material you recover after successful cracking.

[→ Kill-Chain](docs/KILL-CHAINS.md#ad-01-kerberoasting-and-as-rep-roasting)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Impacket (GetUserSPNs / GetNPUsers) | https://github.com/fortra/impacket | Suite de protocolos SMB/Kerberos; `GetUserSPNs.py` y `GetNPUsers.py` recolectan tickets Kerberoastables y blobs AS-REP |
| Hashcat | https://hashcat.net/hashcat/ | Motor de crackeo offline para hashes Kerberos 5 (`-m 13100` para TGS, `-m 18200` para AS-REP) |
| Rubeus | https://github.com/GhostPack/Rubeus | Herramienta .NET para solicitar y manipular tickets Kerberos directamente desde Windows |
| HackTricks — Kerberoast | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/kerberoast | Guía técnica completa de Kerberoasting y AS-REP Roasting con sintaxis de comandos |
| MITRE ATT&CK T1558.003 — Kerberoasting | https://attack.mitre.org/techniques/T1558/003/ | Entrada oficial de la técnica con detecciones y mitigaciones recomendadas |

---

### AD-02: LLMNR/NBT-NS Poisoning and NTLM Relay

**Difficulty:** Medium
**VMs:** 2

You are positioned on a Windows domain network where LLMNR and NBT-NS broadcast name resolution remains enabled — a misconfiguration that lets any host on the segment respond to unresolved name queries. Using Responder, you poison broadcast requests and capture NTLMv2 challenge-response hashes from domain users authenticating to a non-existent resource. Rather than cracking the captured hash, you pipe it directly through ntlmrelayx to relay the credential to a domain service, obtaining command execution on a target workstation and the flag without ever recovering a plaintext password.

[→ Kill-Chain](docs/KILL-CHAINS.md#ad-02-llmnrnbt-ns-poisoning-and-ntlm-relay)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Responder | https://github.com/lgandx/Responder | Herramienta de poisoning LLMNR/NBT-NS/mDNS que captura hashes NTLMv2 en redes Windows |
| Impacket ntlmrelayx | https://github.com/fortra/impacket | `ntlmrelayx.py` reenvía credenciales NTLM capturadas a servicios SMB/LDAP/MSSQL |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Sucesor de CrackMapExec; enumera y ejecuta comandos via SMB, WinRM y LDAP |
| MITRE ATT&CK T1557.001 — LLMNR/NBT-NS Poisoning | https://attack.mitre.org/techniques/T1557/001/ | Técnica oficial: Adversary-in-the-Middle via envenenamiento de resolución de nombres |
| HackTricks — LLMNR/NBT-NS Relay | https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/spoofing-llmnr-nbt-ns-mdns-dns-and-wpad-and-relay-attacks | Guía detallada de ataques de relay NTLM encadenados con Responder y ntlmrelayx |

---

### AD-03: BloodHound ACL Abuse Path

**Difficulty:** Medium
**VMs:** 2

You have obtained a low-privileged domain account and need to escalate your access to Domain Admin. Using SharpHound to collect Active Directory relationship data and BloodHound to visualize attack paths, you identify a chain of abusable Access Control List edges — specifically a WriteDACL or GenericWrite permission held by your compromised account over a higher-privileged object. You exploit this edge to grant yourself the rights needed for further escalation, chaining the steps until you hold Domain Admin and retrieve the flag.

[→ Kill-Chain](docs/KILL-CHAINS.md#ad-03-bloodhound-acl-abuse-path)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| BloodHound Community Edition | https://github.com/SpecterOps/BloodHound | Plataforma de análisis de grafos AD para identificar rutas de ataque (versión CE oficial) |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Enumeración LDAP y SMB para identificar usuarios y permisos del dominio |
| PowerView | https://github.com/PowerShellMafia/PowerSploit/blob/master/Recon/PowerView.ps1 | Script PowerShell para enumerar objetos AD, ACLs y propiedades de cuentas |
| HackTricks — ACL Abuse | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/acl-persistence-abuse | Guía de abuso de ACLs: WriteDACL, GenericWrite, GenericAll y cadenas de escalación |
| MITRE ATT&CK T1098 — Account Manipulation | https://attack.mitre.org/techniques/T1098/ | Técnica de manipulación de cuentas y permisos para mantener acceso en entornos AD |

---

### AD-04: ADCS ESC1 Certificate Abuse

**Difficulty:** Hard
**VMs:** 2

You hold a low-privileged domain account and discover that the organization has deployed Active Directory Certificate Services with a misconfigured certificate template. The template allows low-privileged users to enroll, carries the Client Authentication EKU, and permits the Subject Alternative Name to be specified by the requestor. Using Certipy, you enumerate the vulnerable template, request a rogue certificate impersonating a Domain Admin account, and authenticate via PKINIT to obtain a Kerberos ticket-granting ticket for that privileged account — giving you Domain Admin access and the flag.

[→ Kill-Chain](docs/KILL-CHAINS.md#ad-04-adcs-esc1-certificate-abuse)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Certipy | https://github.com/ly4k/Certipy | Herramienta Python para enumerar y explotar configuraciones erróneas de ADCS (ESC1–ESC16) |
| Impacket (PKINIT / gettgt) | https://github.com/fortra/impacket | `gettgtpkinit.py` y `getnthash.py` para autenticación PKINIT y obtención de TGT mediante certificado |
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Shell WinRM con soporte de certificados para acceso post-explotación a hosts Windows |
| MITRE ATT&CK T1649 — Steal or Forge Auth Certificates | https://attack.mitre.org/techniques/T1649/ | Técnica oficial de abuso de certificados de autenticación en entornos AD CS |
| HackTricks — ADCS ESC1 | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/ad-certificates | Guía técnica de explotación de plantillas ADCS misconfigured con Certipy |

---

### AD-05: Conti-Style APT Chain  [Multi-step — 2 flags]

**Difficulty:** Hard
**VMs:** 3

You enter a three-machine Windows domain environment with only an attacker workstation and no credentials. Deploying Responder to poison LLMNR broadcast requests on the internal segment, you use ntlmrelayx to relay captured hashes over SMB to a domain member server — establishing a foothold that yields the first flag. With your pivot position secured, you use Rubeus to request service tickets for Kerberoastable accounts, crack the ticket offline with Hashcat, and use the recovered credentials with evil-winrm to move laterally to the domain controller and retrieve the second flag. Each lateral movement hop uses a distinct protocol — SMB for the first, WinRM for the second.

[→ Kill-Chain](docs/KILL-CHAINS.md#ad-05-conti-style-apt-chain)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Responder | https://github.com/lgandx/Responder | Primer eslabón: captura hashes NTLMv2 mediante poisoning de broadcast en el segmento interno |
| Rubeus | https://github.com/GhostPack/Rubeus | Kerberoasting de cuentas de servicio para obtener tickets TGS descifrables offline |
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Movimiento lateral al DC mediante WinRM con credenciales crackeadas |
| Hashcat | https://hashcat.net/hashcat/ | Crackeo offline de tickets TGS Kerberoasteados (`-m 13100`) |
| MITRE ATT&CK T1550.002 — Pass the Hash | https://attack.mitre.org/techniques/T1550/002/ | Técnica de reutilización de hashes NTLM para movimiento lateral sin recuperar contraseña |

---

## Network Protocol Exploitation

### NET-01: SMB Relay via Unsigned Shares

**Difficulty:** Easy
**VMs:** 2

You discover a network segment where SMB signing is not enforced on workstations — a common misconfiguration in environments that have never hardened their default Windows settings. Placing Responder in analysis mode to avoid poisoning and using ntlmrelayx to relay captured authentication attempts, you intercept a domain user's SMB authentication and relay it in real time to a file share on a target host. The relayed credential grants you read access to the share containing the flag, with no need to crack or recover any password.

[→ Kill-Chain](docs/KILL-CHAINS.md#net-01-smb-relay-via-unsigned-shares)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Impacket ntlmrelayx | https://github.com/fortra/impacket | `ntlmrelayx.py` intercepta y reenvía autenticaciones SMB a recursos sin firma obligatoria |
| Responder | https://github.com/lgandx/Responder | Modo análisis (`-A`) para captura pasiva sin envenenar; fuente de las credenciales a relayar |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Enumera qué hosts tienen SMB signing deshabilitado: `nxc smb <rango> --gen-relay-list` |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de interposición entre autenticación cliente-servidor para relay de credenciales |
| HackTricks — LLMNR/NBT-NS Relay | https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/spoofing-llmnr-nbt-ns-mdns-dns-and-wpad-and-relay-attacks | Detalle técnico del relay SMB con ntlmrelayx, incluyendo opciones de modo silencioso |

---

### NET-02: IPv6 Rogue DHCPv6 and LDAP Relay

**Difficulty:** Medium
**VMs:** 2

You observe that the target Windows domain has no IPv6 management in place, leaving all hosts susceptible to rogue DHCPv6 advertisements. Using mitm6, you stand up a rogue DHCPv6 server that assigns itself as the IPv6 default gateway and DNS server for domain hosts, causing them to send WPAD proxy authentication requests to your attacker machine. You relay these authentication attempts to LDAP via ntlmrelayx, leveraging the relayed credential to create a new privileged domain account — no code execution, no malware, no hash cracking required. You use the newly created account to authenticate and retrieve the flag.

[→ Kill-Chain](docs/KILL-CHAINS.md#net-02-ipv6-rogue-dhcpv6-and-ldap-relay)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| mitm6 | https://github.com/dirkjanm/mitm6 | Servidor DHCPv6 malicioso que se asigna como DNS IPv6 predeterminado en redes Windows |
| Impacket ntlmrelayx | https://github.com/fortra/impacket | Relay de autenticaciones WPAD capturadas hacia LDAP para crear cuentas privilegiadas |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Verificación post-ataque de la cuenta creada vía `nxc ldap` y `nxc smb` |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de interposición usando DHCPv6/WPAD para capturar y relayar autenticaciones |
| MITRE ATT&CK T1098 — Account Manipulation | https://attack.mitre.org/techniques/T1098/ | Técnica de creación de cuentas privilegiadas mediante relay LDAP autenticado |

---

### NET-03: ARP Cache Poisoning and Credential Interception

**Difficulty:** Easy
**VMs:** 2

You are on the same Layer 2 segment as two communicating hosts and must intercept their traffic. Using bettercap, you send gratuitous ARP replies to poison the ARP caches of both targets, routing their traffic through your machine and positioning yourself as the man-in-the-middle. You exploit bettercap's HTTPS proxy to downgrade encrypted connections to plaintext HTTP, capturing the credentials transmitted by the hosts and using them to retrieve the flag.

[→ Kill-Chain](docs/KILL-CHAINS.md#net-03-arp-cache-poisoning-and-credential-interception)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| bettercap | https://github.com/bettercap/bettercap | Framework MITM con módulos ARP spoof, sniffer y proxy HTTPS para interceptación de tráfico |
| Scapy | https://scapy.readthedocs.io/en/latest/ | Librería Python para crafting de paquetes ARP gratuitous y análisis de tráfico interceptado |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de posicionamiento MITM mediante envenenamiento de caché ARP en capa 2 |
| MITRE ATT&CK T1040 — Network Sniffing | https://attack.mitre.org/techniques/T1040/ | Técnica de captura pasiva de credenciales en tráfico de red interceptado |
| Bettercap — sitio oficial | https://www.bettercap.org/ | Documentación oficial de módulos, capturers y proxy HTTPS de bettercap |

---

### NET-04: DNS Cache Poisoning

**Difficulty:** Medium
**VMs:** 2

You identify a DNS resolver deployed in the target network that is misconfigured to accept responses without adequate source-port randomization or query ID validation. By injecting forged DNS responses that race ahead of the legitimate upstream resolver, you corrupt the resolver's cache so that a targeted internal hostname resolves to an IP address you control. When a legitimate internal service queries the poisoned name and sends its HTTP request to your machine, the flag is embedded in that intercepted request.

[→ Kill-Chain](docs/KILL-CHAINS.md#net-04-dns-cache-poisoning)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Scapy | https://scapy.readthedocs.io/en/latest/ | Crafting de respuestas DNS forjadas con ID de transacción y puerto fuente manipulados |
| bettercap | https://github.com/bettercap/bettercap | Módulo `dns.spoof` para inyección automatizada de respuestas DNS falsas en la red local |
| FRRouting (FRR) | https://frrouting.org/ | Daemon de enrutamiento en el VM víctima; usado para simular el resolver DNS misconfigured |
| MITRE ATT&CK T1568 — Dynamic Resolution | https://attack.mitre.org/techniques/T1568/ | Técnica de manipulación de resolución DNS para redirigir tráfico a infraestructura controlada |
| Scapy OSPF contrib | https://scapy.readthedocs.io/en/latest/api/scapy.contrib.ospf.html | Referencia de la API Scapy para construcción de paquetes de protocolos de red avanzados |

---

## CVE Weaponization

### CVE-01: EternalBlue — MS17-010 (CVE-2017-0144)

**Difficulty:** Hard
**VMs:** 2

You face a Windows 7 SP1 target with SMBv1 enabled and no security patches applied — the exact environment that made CVE-2017-0144 one of the most destructive vulnerabilities in history. Rather than reaching for an automated framework, you author a Python exploit that implements the SMBv1 transaction setup, heap grooming, and DoublePulsar shellcode staging yourself, using the provided `mysmb.py` protocol scaffold as your foundation. You craft the malformed FEA list that triggers the buffer overflow, stage your payload through the DoublePulsar implant, and obtain a shell on the target from which you retrieve the flag. Completing this scenario requires you to understand the SMBv1 protocol framing at the packet level — not just execute a pre-built tool.

[→ Kill-Chain](docs/KILL-CHAINS.md#cve-01-eternalblue-ms17-010)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| NVD — CVE-2017-0144 | https://nvd.nist.gov/vuln/detail/CVE-2017-0144 | Entrada oficial con CVSS 9.3, descripción del fallo SMBv1 y referencias de parches Microsoft |
| worawit/MS17-010 | https://github.com/worawit/MS17-010 | PoC Python original: `checker.py` (verificación) y scripts de explotación manual sin Metasploit |
| AutoBlue-MS17-010 | https://github.com/3ndG4me/AutoBlue-MS17-010 | Variante educativa que incluye `mysmb.py` helper y shellcode stageless sin framework automático |
| MITRE ATT&CK T1190 — Exploit Public-Facing Application | https://attack.mitre.org/techniques/T1190/ | Técnica de explotación remota de servicios expuestos (acceso inicial via SMBv1) |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de comandos mediante el payload inyectado post-explotación |

---

### CVE-02: Log4Shell — CVE-2021-44228

**Difficulty:** Medium
**VMs:** 2

You identify a Java application that logs attacker-controlled input using a vulnerable version of the Apache Log4j library. Rather than using a pre-built exploit kit, you author a JNDI injection payload string and build a Python-based exploit chain server that serves both an LDAP redirect and a malicious Java class over HTTP. When the application logs your crafted input, the Log4j library initiates an outbound JNDI lookup to your server, downloads and executes your class, and you achieve OS command execution on the target — recovering the flag through the resulting shell.

[→ Kill-Chain](docs/KILL-CHAINS.md#cve-02-log4shell-cve-2021-44228)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| NVD — CVE-2021-44228 | https://nvd.nist.gov/vuln/detail/CVE-2021-44228 | Entrada oficial con CVSS 10.0, descripción de la inyección JNDI y versiones afectadas |
| axelcurmi/log4shell-docker-lab | https://github.com/axelcurmi/log4shell-docker-lab | Laboratorio Docker listo para usar con la aplicación vulnerable pinned a Log4j 2.14.1 |
| christophetd/log4shell-vulnerable-app | https://github.com/christophetd/log4shell-vulnerable-app | Imagen Docker de aplicación Spring vulnerable; referencia para construir el servidor LDAP + HTTP |
| MITRE ATT&CK T1190 — Exploit Public-Facing Application | https://attack.mitre.org/techniques/T1190/ | Técnica de explotación remota de aplicaciones Java vía inyección JNDI en headers HTTP |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de código arbitrario mediante la clase Java maliciosa descargada |

---

### CVE-03: Apache Struts S2-045 — CVE-2017-5638 (Equifax Breach Vector)

**Difficulty:** Medium
**VMs:** 2

You face an Apache Struts 2 web application running in a Docker container on the target server. The application processes multipart file upload requests using Jakarta's vulnerable multipart parser — the same misconfiguration that enabled the 2017 Equifax breach. You author a Python exploit script that injects an OGNL expression into the Content-Type header of an HTTP POST request, bypassing Struts2's security restrictions and executing arbitrary OS commands on the server. No JSP webshell is needed — the exploit returns command output directly in the HTTP response. You use this remote command execution to retrieve the flag from the target server.

[→ Kill-Chain](docs/KILL-CHAINS.md#cve-03-apache-struts-s2-045-cve-2017-5638)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| NVD — CVE-2017-5638 | https://nvd.nist.gov/vuln/detail/CVE-2017-5638 | Entrada oficial con CVSS 10.0; describe la inyección OGNL vía Content-Type en Struts 2 |
| Apache Struts Security Bulletin S2-045 | https://cwiki.apache.org/confluence/display/WW/S2-045 | Boletín oficial de Apache con versiones afectadas, vector de ataque y parches disponibles |
| piesecurity/apache-struts2-cve-2017-5638 | https://hub.docker.com/r/piesecurity/apache-struts2-cve-2017-5638/ | Imagen Docker con Struts 2.3.5 vulnerable; entorno reproducible del vector Equifax |
| MITRE ATT&CK T1190 — Exploit Public-Facing Application | https://attack.mitre.org/techniques/T1190/ | Técnica de explotación remota mediante inyección de expresión OGNL en header HTTP |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de comandos del SO retornados directamente en la respuesta HTTP |

---

### CVE-04: PrintNightmare (CVE-2021-1675 / CVE-2021-34527)

**Difficulty:** Medium
**VMs:** 2

You have obtained a low-privileged interactive session on a Windows Server target and need to escalate to SYSTEM. The Windows Print Spooler service is running and the target is unpatched against PrintNightmare. You author a C or Python payload that instructs the Windows Print Spooler service — which runs as SYSTEM — to load a malicious DLL you supply, injecting your code into a SYSTEM-level process. Once your payload executes with elevated privileges, you retrieve the flag from a location accessible only to SYSTEM. This scenario exercises the local privilege escalation path, requiring a pre-existing foothold rather than an external network position.

[→ Kill-Chain](docs/KILL-CHAINS.md#cve-04-printnightmare-lpe-cve-2021-34527)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| NVD — CVE-2021-34527 | https://nvd.nist.gov/vuln/detail/CVE-2021-34527 | Entrada oficial con CVSS 8.8; describe LPE y RCE via Windows Print Spooler |
| cube0x0/CVE-2021-1675 | https://github.com/cube0x0/CVE-2021-1675 | PoC C# y Python; implementación de referencia del LPE por inyección de DLL en Spooler |
| Impacket (rpcdump / rprn) | https://github.com/fortra/impacket | `rpcdump.py` para verificar el servicio Spooler; `rprn` module para explotación via RPC |
| MITRE ATT&CK T1068 — Exploitation for Privilege Escalation | https://attack.mitre.org/techniques/T1068/ | Técnica de escalación de privilegios locales mediante explotación del Spooler de impresión |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de payload DLL con privilegios SYSTEM via Spooler |

---

## Cloud / Container Security

### CC-01: IMDS SSRF and IAM Credential Theft

**Difficulty:** Easy
**VMs:** 2

You discover a web application that makes server-side HTTP requests based on attacker-controlled input — a classic Server-Side Request Forgery surface. By crafting requests that target the simulated AWS Instance Metadata Service endpoint at 169.254.169.254, you retrieve the IAM role credentials attached to the application's host. Using those stolen temporary credentials, you query a simulated S3 API to enumerate available objects and retrieve the flag stored in the bucket. No authentication bypass or code execution is required — the SSRF vulnerability does the work.

[→ Kill-Chain](docs/KILL-CHAINS.md#cc-01-aws-imds-ssrf-and-iam-credential-theft)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| AWS IMDS Documentation | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html | Documentación oficial del endpoint 169.254.169.254; estructura de credenciales IAM temporales |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de robo de credenciales desde el servicio de metadatos de instancia cloud |
| MITRE ATT&CK T1190 — Exploit Public-Facing Application | https://attack.mitre.org/techniques/T1190/ | Técnica de SSRF para alcanzar endpoints internos no expuestos directamente |
| Docker Security Documentation | https://docs.docker.com/engine/security/ | Referencia de configuración segura de contenedores y aislamiento de red |
| HackTricks — Active Directory Methodology | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology | Contexto sobre técnicas de enumeración y explotación aplicables a entornos cloud-AD |

---

### CC-02: Privileged Docker Container Escape

**Difficulty:** Medium
**VMs:** 2

You land inside a deliberately misconfigured Docker container running as root with elevated Linux capabilities. From inside the container, you discover that the privilege level granted to this container extends access to host kernel interfaces that are normally isolated from container namespaces. You write a payload that abuses a cgroup notification path to schedule command execution on the underlying host, planting a reverse connection or reading the flag directly from the host's root directory. The challenge tests your understanding of Linux container isolation boundaries and the conditions under which a privileged container ceases to provide meaningful separation from the host.

[→ Kill-Chain](docs/KILL-CHAINS.md#cc-02-privileged-docker-container-escape)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Trail of Bits — Understanding Docker Container Escapes | https://blog.trailofbits.com/2019/07/19/understanding-docker-container-escapes/ | Investigación original que documenta el escape via `cgroup release_agent` desde contenedor privilegiado |
| Docker Security Documentation | https://docs.docker.com/engine/security/ | Documentación oficial sobre `--privileged`, capabilities y aislamiento de namespaces |
| MITRE ATT&CK T1611 — Escape to Host | https://attack.mitre.org/techniques/T1611/ | Técnica oficial de escape de contenedor para acceder al sistema operativo del host subyacente |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de acceso a secretos y credenciales expuestas en el entorno de contenedor |
| Kubernetes Goat — Container Escape Scenario | https://madhuakula.com/kubernetes-goat/docs/scenarios/scenario-4/container-escape-to-the-host-system-in-kubernetes-containers/welcome/ | Laboratorio interactivo de referencia para técnicas de escape de contenedor en entornos K8s |

---

### CC-03: Kubernetes Misconfigured Service Account Escape

**Difficulty:** Hard
**VMs:** 2

You gain initial access to a Kubernetes cluster as a low-privileged user and receive a service account token with more permissions than intended. Using kubectl, you enumerate cluster resources — pods, roles, role bindings, and secrets — to map the extent of the over-provisioned permissions. You construct and deploy a privileged pod spec with a hostPath volume that mounts the host node's root filesystem, then exec into the pod to access the host filesystem directly and retrieve the flag planted in the node's root directory.

[→ Kill-Chain](docs/KILL-CHAINS.md#cc-03-kubernetes-misconfigured-service-account-escape)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| k3s Official Documentation | https://docs.k3s.io/ | Instalación del clúster K8s single-node para el entorno de laboratorio |
| Kubernetes Goat — Container Escape Scenario | https://madhuakula.com/kubernetes-goat/docs/scenarios/scenario-4/container-escape-to-the-host-system-in-kubernetes-containers/welcome/ | Escenario de referencia: hostPath mount y privesc desde pod al nodo host |
| MITRE ATT&CK T1611 — Escape to Host | https://attack.mitre.org/techniques/T1611/ | Técnica de escape de pod K8s mediante hostPath volume con acceso al filesystem del nodo |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de robo de tokens de service account K8s desde el API server |
| MITRE ATT&CK T1098 — Account Manipulation | https://attack.mitre.org/techniques/T1098/ | Técnica de aprovechamiento de role bindings misconfigured para escalación en el clúster |

---

## LLM Security

### LLM-01: Multi-Layer Prompt Injection Bypass

**Difficulty:** Easy
**VMs:** 2

You interact with an Ollama-backed chatbot that appears to resist your initial injection attempts — the application enforces a system prompt boundary, a regex-based filter on common injection patterns, and a semantic validation layer that checks whether your input looks like an attack. Your objective is to chain at least two distinct bypass techniques to break through the layered defenses, override the system prompt, and cause the model to output a hidden flag embedded in the LLM's context. Understanding how each defense layer fails individually — and how they can be bypassed in sequence — is the core challenge.

[→ Kill-Chain](docs/KILL-CHAINS.md#llm-01-multi-layer-prompt-injection)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| OWASP LLM Top 10 2025 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Referencia oficial: LLM01 (Prompt Injection) y categorías de bypass de defensas en LLMs |
| Ollama | https://github.com/ollama/ollama | Runtime de modelos LLM local (phi3, llama3.2) que sirve como backend del chatbot víctima |
| Bishop Fox LLM CTF Lab | https://bishopfox.com/blog/large-language-models-llm-ctf-lab | Laboratorio CTF de referencia con desafíos multi-capa de bypass de prompt injection |
| garak — LLM Vulnerability Scanner | https://github.com/NVIDIA/garak | Herramienta de fuzzing automatizado de LLMs para detectar vectores de inyección y jailbreak |
| PromptMe — OWASP Project | https://owasp.org/www-project-promptme/ | Aplicación OWASP de chatbot intencionalmente vulnerable alineada con el LLM Top 10 |

---

### LLM-02: Indirect Prompt Injection via RAG Document Poisoning

**Difficulty:** Medium
**VMs:** 2

You discover a chatbot application that uses Retrieval-Augmented Generation, ingesting external documents into a vector database to enrich its responses. You craft a malicious document containing injected instructions hidden within otherwise benign content and cause it to be ingested into the vector store. When a legitimate user submits a routine query, the chatbot retrieves your poisoned document as relevant context, and the embedded instructions trigger — causing the model to output the flag. This scenario explores the attack surface introduced when an LLM blindly trusts externally sourced content retrieved from its knowledge base.

[→ Kill-Chain](docs/KILL-CHAINS.md#llm-02-indirect-prompt-injection-via-rag-poisoning)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| OWASP LLM Top 10 2025 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Referencia oficial: LLM02 (Insecure Output Handling) e inyección indirecta via RAG |
| Damn Vulnerable LLM Agent | https://github.com/ReversecLabs/damn-vulnerable-llm-agent | Agente LangChain con RAG y tool-calling intencionalmente vulnerable a inyección indirecta |
| Ollama | https://github.com/ollama/ollama | Backend LLM local que sirve el modelo para el agente RAG vulnerable |
| garak — LLM Vulnerability Scanner | https://github.com/NVIDIA/garak | Scanner automatizado para validar vectores de inyección indirecta en pipelines RAG |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de instrucciones arbitrarias inyectadas via documentos envenenados |

---

### LLM-03: IDOR in Chat History API

**Difficulty:** Medium
**VMs:** 2

You interact with an LLM application that stores conversation history and exposes an API endpoint for retrieving past chat sessions. The endpoint uses predictable, sequential conversation identifiers and performs no meaningful access control validation — an insecure direct object reference vulnerability at the application layer. By enumerating conversation IDs through the endpoint, you access chat sessions belonging to other users, eventually reaching a privileged user's conversation that contains the flag. The challenge lies entirely in the application's failure to authenticate ownership of the requested resource.

[→ Kill-Chain](docs/KILL-CHAINS.md#llm-03-idor-in-llm-chat-history-api)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| OWASP LLM Top 10 2025 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Referencia oficial: LLM10 (Insecure Plugin Design) e IDOR en APIs de aplicaciones LLM |
| Damn Vulnerable LLM Agent | https://github.com/ReversecLabs/damn-vulnerable-llm-agent | Aplicación con endpoints IDOR-vulnerables en historial de chat (IDs secuenciales sin auth) |
| Ollama | https://github.com/ollama/ollama | Backend LLM que alimenta la aplicación con el historial de conversaciones |
| MITRE ATT&CK T1078 — Valid Accounts | https://attack.mitre.org/techniques/T1078/ | Técnica de acceso a recursos usando credenciales o sesiones de otras cuentas |
| PromptMe — OWASP Project | https://owasp.org/www-project-promptme/ | Proyecto OWASP de referencia para vulnerabilidades en APIs de aplicaciones LLM |

---

## Multi-Step APT Chains

### ATP-01: HAFNIUM-Style Webshell and Lateral Movement  [Multi-step — 2 flags]

**Difficulty:** Hard
**VMs:** 3

You begin with knowledge of an internet-facing web application that processes user-supplied URLs in a server-side context. By crafting SSRF payloads, you reach an internal service inaccessible from the outside, and by escalating that access you upload a webshell to the application server that grants you code execution. Harvesting credentials found on the compromised web tier, you use them with evil-winrm to authenticate to an internal Windows pivot host — securing your first objective and retrieving the first flag. From the pivot, you enumerate domain resources and identify a path to the domain controller, following it to retrieve the second flag and complete the chain.

[→ Kill-Chain](docs/KILL-CHAINS.md#atp-01-hafnium-style-ssrf-pivot-to-domain-controller)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Shell WinRM para movimiento lateral al pivot Windows con credenciales recuperadas del tier web |
| Impacket suite | https://github.com/fortra/impacket | `psexec.py` y `smbexec.py` para ejecución remota en el segundo hop hacia el DC |
| Ligolo-ng | https://github.com/nicocha30/ligolo-ng | Pivoting L3 desde el servidor web comprometido hacia el segmento interno del DC |
| MITRE ATT&CK T1505.003 — Web Shell | https://attack.mitre.org/techniques/T1505/003/ | Técnica de instalación de webshell para persistencia y ejecución de comandos en servidor web |
| MITRE ATT&CK T1021.006 — WinRM | https://attack.mitre.org/techniques/T1021/006/ | Técnica de movimiento lateral via WinRM con credenciales válidas recuperadas del servidor web |

---

### ATP-02: SolarWinds-Style Supply Chain Backdoor  [Multi-step — 2 flags]

**Difficulty:** Hard
**VMs:** 3

You are handed access to a simulated software update distribution server — the upstream source that downstream targets trust implicitly. You modify an update package to include a backdoor that executes silently when the downstream target applies the update, and once the backdoored update runs on the downstream host you retrieve the first flag from the compromised target. With your foothold established, you shift to the second objective: a further-isolated target that is not directly reachable from your position. You establish a covert command-and-control channel by tunneling communications through DNS using dnscat2, bypassing the network segmentation, and retrieving the second flag from the isolated host.

[→ Kill-Chain](docs/KILL-CHAINS.md#atp-02-solarwinds-style-supply-chain-compromise-dns-c2)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| dnscat2 | https://github.com/iagox86/dnscat2 | Framework C2 por DNS tunneling; segundo hop de la cadena para eludir segmentación de red |
| Chisel | https://github.com/jpillora/chisel | Túnel TCP/SOCKS5 sobre HTTP; alternativa de pivoting para el segundo hop de la cadena |
| Ligolo-ng | https://github.com/nicocha30/ligolo-ng | Pivoting L3 para alcanzar el host aislado en el segundo segmento de red |
| MITRE ATT&CK T1195 — Supply Chain Compromise | https://attack.mitre.org/techniques/T1195/ | Técnica de compromiso de cadena de suministro de software (paquete de actualización backdoored) |
| MITRE ATT&CK T1071.004 — DNS | https://attack.mitre.org/techniques/T1071/004/ | Técnica de C2 encubierto mediante tunneling DNS (dnscat2 para eludir segmentación) |

---

### ATP-03: LAPSUS$-Style Cloud Identity Chain  [Multi-step — 2 flags]

**Difficulty:** Hard
**VMs:** 3

You identify an SSRF vulnerability in a cloud-hosted application and use it to query the Instance Metadata Service, stealing a Kubernetes service account token that was inadvertently exposed in the metadata response. Using kubectl with the stolen token, you enumerate cluster resources and discover a misconfigured privileged pod that grants you access to the host node — escaping the container boundary and securing the first flag from the node filesystem. From the node, you query the etcd datastore directly, extracting the stored Kubernetes secrets and credentials it holds. Using the recovered credentials to authenticate as an administrator on the final internal target, you retrieve the second flag and complete the cloud identity chain.

[→ Kill-Chain](docs/KILL-CHAINS.md#atp-03-lapsus-style-ssrf-to-k8s-identity-chain)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| AWS IMDS Documentation | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html | Referencia del endpoint IMDS para robo de token de service account K8s expuesto en metadatos |
| k3s Official Documentation | https://docs.k3s.io/ | Instalación del clúster K8s del laboratorio; contexto de etcd y acceso al datastore del clúster |
| Impacket suite | https://github.com/fortra/impacket | `secretsdump.py` para extracción de credenciales del etcd del clúster K8s comprometido |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de robo de token de service account K8s via IMDS + SSRF |
| MITRE ATT&CK T1602 — Data from Configuration Repository | https://attack.mitre.org/techniques/T1602/ | Técnica de extracción de secretos desde etcd (repositorio de configuración del clúster K8s) |

---

### ATP-04: Volt Typhoon Living-Off-the-Land Chain  [Multi-step — 2 flags]

**Difficulty:** Hard
**VMs:** 3

You operate under a no-malware constraint — no compiled payloads, no shellcode, no persistent implants. Using mitm6 to deploy a rogue DHCPv6 server and relaying the resulting authentication attempts to LDAP via ntlmrelayx, you create a new privileged domain account without touching the filesystem of any target host. With the new account, you use evil-winrm to authenticate to a domain member server and retrieve the first flag. From the pivot, you enumerate service account SPNs with Kerberoasting, crack the recovered ticket hash offline, and use the resulting credential with SMBExec or DCOM to authenticate to the domain controller and retrieve the final flag — the entire chain executed without dropping a single malicious file.

[→ Kill-Chain](docs/KILL-CHAINS.md#atp-04-volt-typhoon-style-ipv6-relay-and-kerberoasting-chain)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| mitm6 | https://github.com/dirkjanm/mitm6 | Primer eslabón: DHCPv6 rogue para creación de cuenta privilegiada via relay LDAP sin tocar disco |
| Impacket ntlmrelayx | https://github.com/fortra/impacket | Relay de autenticaciones WPAD a `ldaps://` para crear cuenta de dominio via LDAP relay |
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Autenticación WinRM al member server con la cuenta creada; recuperación del primer flag |
| Rubeus | https://github.com/GhostPack/Rubeus | Kerberoasting desde el pivot para obtener TGS descifrables de cuentas de servicio |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de relay de autenticaciones via DHCPv6/WPAD sin persistencia en disco |
