# CTF Scenario Reference Catalog

Master reference list for all 23 scenarios. Each section contains 3–5 curated links to
official documentation, tool repositories, CVE advisories, and technique guides.

Reference format: markdown table with columns Recurso | URL | Propósito

---

## Dominio: Active Directory / Windows

### AD-01: Kerberoasting and AS-REP Roasting

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Impacket (GetUserSPNs / GetNPUsers) | https://github.com/fortra/impacket | Suite de protocolos SMB/Kerberos; `GetUserSPNs.py` y `GetNPUsers.py` recolectan tickets Kerberoastables y blobs AS-REP |
| Hashcat | https://hashcat.net/hashcat/ | Motor de crackeo offline para hashes Kerberos 5 (`-m 13100` para TGS, `-m 18200` para AS-REP) |
| Rubeus | https://github.com/GhostPack/Rubeus | Herramienta .NET para solicitar y manipular tickets Kerberos directamente desde Windows |
| HackTricks — Kerberoast | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/kerberoast | Guía técnica completa de Kerberoasting y AS-REP Roasting con sintaxis de comandos |
| MITRE ATT&CK T1558.003 — Kerberoasting | https://attack.mitre.org/techniques/T1558/003/ | Entrada oficial de la técnica con detecciones y mitigaciones recomendadas |

---

### AD-02: LLMNR/NBT-NS Poisoning and NTLM Relay

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Responder | https://github.com/lgandx/Responder | Herramienta de poisoning LLMNR/NBT-NS/mDNS que captura hashes NTLMv2 en redes Windows |
| Impacket ntlmrelayx | https://github.com/fortra/impacket | `ntlmrelayx.py` reenvía credenciales NTLM capturadas a servicios SMB/LDAP/MSSQL |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Sucesor de CrackMapExec; enumera y ejecuta comandos via SMB, WinRM y LDAP |
| MITRE ATT&CK T1557.001 — LLMNR/NBT-NS Poisoning | https://attack.mitre.org/techniques/T1557/001/ | Técnica oficial: Adversary-in-the-Middle via envenenamiento de resolución de nombres |
| HackTricks — LLMNR/NBT-NS Relay | https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/spoofing-llmnr-nbt-ns-mdns-dns-and-wpad-and-relay-attacks | Guía detallada de ataques de relay NTLM encadenados con Responder y ntlmrelayx |

---

### AD-03: BloodHound ACL Abuse Path

| Recurso | URL | Propósito |
|---------|-----|-----------|
| BloodHound Community Edition | https://github.com/SpecterOps/BloodHound | Plataforma de análisis de grafos AD para identificar rutas de ataque (versión CE oficial) |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Enumeración LDAP y SMB para identificar usuarios y permisos del dominio |
| PowerView | https://github.com/PowerShellMafia/PowerSploit/blob/master/Recon/PowerView.ps1 | Script PowerShell para enumerar objetos AD, ACLs y propiedades de cuentas |
| HackTricks — ACL Abuse | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/acl-persistence-abuse | Guía de abuso de ACLs: WriteDACL, GenericWrite, GenericAll y cadenas de escalación |
| MITRE ATT&CK T1098 — Account Manipulation | https://attack.mitre.org/techniques/T1098/ | Técnica de manipulación de cuentas y permisos para mantener acceso en entornos AD |

---

### AD-04: ADCS ESC1 Certificate Abuse

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Certipy | https://github.com/ly4k/Certipy | Herramienta Python para enumerar y explotar configuraciones erróneas de ADCS (ESC1–ESC16) |
| Impacket (PKINIT / gettgt) | https://github.com/fortra/impacket | `gettgtpkinit.py` y `getnthash.py` para autenticación PKINIT y obtención de TGT mediante certificado |
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Shell WinRM con soporte de certificados para acceso post-explotación a hosts Windows |
| MITRE ATT&CK T1649 — Steal or Forge Auth Certificates | https://attack.mitre.org/techniques/T1649/ | Técnica oficial de abuso de certificados de autenticación en entornos AD CS |
| HackTricks — ADCS ESC1 | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/ad-certificates | Guía técnica de explotación de plantillas ADCS misconfigured con Certipy |

---

### AD-05: Conti-Style APT Chain

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Responder | https://github.com/lgandx/Responder | Primer eslabón: captura hashes NTLMv2 mediante poisoning de broadcast en el segmento interno |
| Rubeus | https://github.com/GhostPack/Rubeus | Kerberoasting de cuentas de servicio para obtener tickets TGS descifrables offline |
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Movimiento lateral al DC mediante WinRM con credenciales crackeadas |
| Hashcat | https://hashcat.net/hashcat/ | Crackeo offline de tickets TGS Kerberoasteados (`-m 13100`) |
| MITRE ATT&CK T1550.002 — Pass the Hash | https://attack.mitre.org/techniques/T1550/002/ | Técnica de reutilización de hashes NTLM para movimiento lateral sin recuperar contraseña |

---

## Dominio: Network Protocol Exploitation

### NET-01: SMB Relay via Unsigned Shares

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Impacket ntlmrelayx | https://github.com/fortra/impacket | `ntlmrelayx.py` intercepta y reenvía autenticaciones SMB a recursos sin firma obligatoria |
| Responder | https://github.com/lgandx/Responder | Modo análisis (`-A`) para captura pasiva sin envenenar; fuente de las credenciales a relayar |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Enumera qué hosts tienen SMB signing deshabilitado: `nxc smb <rango> --gen-relay-list` |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de interposición entre autenticación cliente-servidor para relay de credenciales |
| HackTricks — LLMNR/NBT-NS Relay | https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/spoofing-llmnr-nbt-ns-mdns-dns-and-wpad-and-relay-attacks | Detalle técnico del relay SMB con ntlmrelayx, incluyendo opciones de modo silencioso |

---

### NET-02: IPv6 Rogue DHCPv6 and LDAP Relay

| Recurso | URL | Propósito |
|---------|-----|-----------|
| mitm6 | https://github.com/dirkjanm/mitm6 | Servidor DHCPv6 malicioso que se asigna como DNS IPv6 predeterminado en redes Windows |
| Impacket ntlmrelayx | https://github.com/fortra/impacket | Relay de autenticaciones WPAD capturadas hacia LDAP para crear cuentas privilegiadas |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Verificación post-ataque de la cuenta creada vía `nxc ldap` y `nxc smb` |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de interposición usando DHCPv6/WPAD para capturar y relayar autenticaciones |
| MITRE ATT&CK T1098 — Account Manipulation | https://attack.mitre.org/techniques/T1098/ | Técnica de creación de cuentas privilegiadas mediante relay LDAP autenticado |

---

### NET-03: ARP Cache Poisoning and Credential Interception

| Recurso | URL | Propósito |
|---------|-----|-----------|
| bettercap | https://github.com/bettercap/bettercap | Framework MITM con módulos ARP spoof, sniffer y proxy HTTPS para interceptación de tráfico |
| Scapy | https://scapy.readthedocs.io/en/latest/ | Librería Python para crafting de paquetes ARP gratuitous y análisis de tráfico interceptado |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de posicionamiento MITM mediante envenenamiento de caché ARP en capa 2 |
| MITRE ATT&CK T1040 — Network Sniffing | https://attack.mitre.org/techniques/T1040/ | Técnica de captura pasiva de credenciales en tráfico de red interceptado |
| Bettercap — sitio oficial | https://www.bettercap.org/ | Documentación oficial de módulos, capturers y proxy HTTPS de bettercap |

---

### NET-04: DNS Cache Poisoning

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Scapy | https://scapy.readthedocs.io/en/latest/ | Crafting de respuestas DNS forjadas con ID de transacción y puerto fuente manipulados |
| bettercap | https://github.com/bettercap/bettercap | Módulo `dns.spoof` para inyección automatizada de respuestas DNS falsas en la red local |
| FRRouting (FRR) | https://frrouting.org/ | Daemon de enrutamiento en el VM víctima; usado para simular el resolver DNS misconfigured |
| MITRE ATT&CK T1568 — Dynamic Resolution | https://attack.mitre.org/techniques/T1568/ | Técnica de manipulación de resolución DNS para redirigir tráfico a infraestructura controlada |
| Scapy OSPF contrib | https://scapy.readthedocs.io/en/latest/api/scapy.contrib.ospf.html | Referencia de la API Scapy para construcción de paquetes de protocolos de red avanzados |

---

## Dominio: CVE Weaponization

### CVE-01: EternalBlue — MS17-010 (CVE-2017-0144)

| Recurso | URL | Propósito |
|---------|-----|-----------|
| NVD — CVE-2017-0144 | https://nvd.nist.gov/vuln/detail/CVE-2017-0144 | Entrada oficial con CVSS 9.3, descripción del fallo SMBv1 y referencias de parches Microsoft |
| worawit/MS17-010 | https://github.com/worawit/MS17-010 | PoC Python original: `checker.py` (verificación) y scripts de explotación manual sin Metasploit |
| AutoBlue-MS17-010 | https://github.com/3ndG4me/AutoBlue-MS17-010 | Variante educativa que incluye `mysmb.py` helper y shellcode stageless sin framework automático |
| MITRE ATT&CK T1190 — Exploit Public-Facing Application | https://attack.mitre.org/techniques/T1190/ | Técnica de explotación remota de servicios expuestos (acceso inicial via SMBv1) |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de comandos mediante el payload inyectado post-explotación |

---

### CVE-02: Log4Shell — CVE-2021-44228

| Recurso | URL | Propósito |
|---------|-----|-----------|
| NVD — CVE-2021-44228 | https://nvd.nist.gov/vuln/detail/CVE-2021-44228 | Entrada oficial con CVSS 10.0, descripción de la inyección JNDI y versiones afectadas |
| axelcurmi/log4shell-docker-lab | https://github.com/axelcurmi/log4shell-docker-lab | Laboratorio Docker listo para usar con la aplicación vulnerable pinned a Log4j 2.14.1 |
| christophetd/log4shell-vulnerable-app | https://github.com/christophetd/log4shell-vulnerable-app | Imagen Docker de aplicación Spring vulnerable; referencia para construir el servidor LDAP + HTTP |
| MITRE ATT&CK T1190 — Exploit Public-Facing Application | https://attack.mitre.org/techniques/T1190/ | Técnica de explotación remota de aplicaciones Java vía inyección JNDI en headers HTTP |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de código arbitrario mediante la clase Java maliciosa descargada |

---

### CVE-03: Apache Struts S2-045 — CVE-2017-5638 (Equifax Breach Vector)

| Recurso | URL | Propósito |
|---------|-----|-----------|
| NVD — CVE-2017-5638 | https://nvd.nist.gov/vuln/detail/CVE-2017-5638 | Entrada oficial con CVSS 10.0; describe la inyección OGNL vía Content-Type en Struts 2 |
| Apache Struts Security Bulletin S2-045 | https://cwiki.apache.org/confluence/display/WW/S2-045 | Boletín oficial de Apache con versiones afectadas, vector de ataque y parches disponibles |
| piesecurity/apache-struts2-cve-2017-5638 | https://hub.docker.com/r/piesecurity/apache-struts2-cve-2017-5638/ | Imagen Docker con Struts 2.3.5 vulnerable; entorno reproducible del vector Equifax |
| MITRE ATT&CK T1190 — Exploit Public-Facing Application | https://attack.mitre.org/techniques/T1190/ | Técnica de explotación remota mediante inyección de expresión OGNL en header HTTP |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de comandos del SO retornados directamente en la respuesta HTTP |

---

### CVE-04: PrintNightmare (CVE-2021-1675 / CVE-2021-34527)

| Recurso | URL | Propósito |
|---------|-----|-----------|
| NVD — CVE-2021-34527 | https://nvd.nist.gov/vuln/detail/CVE-2021-34527 | Entrada oficial con CVSS 8.8; describe LPE y RCE via Windows Print Spooler |
| cube0x0/CVE-2021-1675 | https://github.com/cube0x0/CVE-2021-1675 | PoC C# y Python; implementación de referencia del LPE por inyección de DLL en Spooler |
| Impacket (rpcdump / rprn) | https://github.com/fortra/impacket | `rpcdump.py` para verificar el servicio Spooler; `rprn` module para explotación via RPC |
| MITRE ATT&CK T1068 — Exploitation for Privilege Escalation | https://attack.mitre.org/techniques/T1068/ | Técnica de escalación de privilegios locales mediante explotación del Spooler de impresión |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de payload DLL con privilegios SYSTEM via Spooler |

---

## Dominio: Cloud / Container Security

### CC-01: IMDS SSRF and IAM Credential Theft

| Recurso | URL | Propósito |
|---------|-----|-----------|
| AWS IMDS Documentation | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html | Documentación oficial del endpoint 169.254.169.254; estructura de credenciales IAM temporales |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de robo de credenciales desde el servicio de metadatos de instancia cloud |
| MITRE ATT&CK T1190 — Exploit Public-Facing Application | https://attack.mitre.org/techniques/T1190/ | Técnica de SSRF para alcanzar endpoints internos no expuestos directamente |
| Docker Security Documentation | https://docs.docker.com/engine/security/ | Referencia de configuración segura de contenedores y aislamiento de red |
| HackTricks — Active Directory Methodology | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology | Contexto sobre técnicas de enumeración y explotación aplicables a entornos cloud-AD |

---

### CC-02: Privileged Docker Container Escape

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Trail of Bits — Understanding Docker Container Escapes | https://blog.trailofbits.com/2019/07/19/understanding-docker-container-escapes/ | Investigación original que documenta el escape via `cgroup release_agent` desde contenedor privilegiado |
| Docker Security Documentation | https://docs.docker.com/engine/security/ | Documentación oficial sobre `--privileged`, capabilities y aislamiento de namespaces |
| MITRE ATT&CK T1611 — Escape to Host | https://attack.mitre.org/techniques/T1611/ | Técnica oficial de escape de contenedor para acceder al sistema operativo del host subyacente |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de acceso a secretos y credenciales expuestas en el entorno de contenedor |
| Kubernetes Goat — Container Escape Scenario | https://madhuakula.com/kubernetes-goat/docs/scenarios/scenario-4/container-escape-to-the-host-system-in-kubernetes-containers/welcome/ | Laboratorio interactivo de referencia para técnicas de escape de contenedor en entornos K8s |

---

### CC-03: Kubernetes Misconfigured Service Account Escape

| Recurso | URL | Propósito |
|---------|-----|-----------|
| k3s Official Documentation | https://docs.k3s.io/ | Documentación de k3s; instalación de clúster K8s single-node para el entorno de laboratorio |
| Kubernetes Goat — Container Escape Scenario | https://madhuakula.com/kubernetes-goat/docs/scenarios/scenario-4/container-escape-to-the-host-system-in-kubernetes-containers/welcome/ | Escenario de referencia: hostPath mount y privesc desde pod al nodo host |
| MITRE ATT&CK T1611 — Escape to Host | https://attack.mitre.org/techniques/T1611/ | Técnica de escape de pod K8s mediante hostPath volume con acceso al filesystem del nodo |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de robo de tokens de service account K8s desde el API server |
| MITRE ATT&CK T1098 — Account Manipulation | https://attack.mitre.org/techniques/T1098/ | Técnica de aprovechamiento de role bindings misconfigured para escalación en el clúster |

---

## Dominio: LLM Security

### LLM-01: Multi-Layer Prompt Injection Bypass

| Recurso | URL | Propósito |
|---------|-----|-----------|
| OWASP LLM Top 10 2025 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Referencia oficial: LLM01 (Prompt Injection) y categorías de bypass de defensas en LLMs |
| Ollama | https://github.com/ollama/ollama | Runtime de modelos LLM local (phi3, llama3.2) que sirve como backend del chatbot víctima |
| Bishop Fox LLM CTF Lab | https://bishopfox.com/blog/large-language-models-llm-ctf-lab | Laboratorio CTF de referencia con desafíos multi-capa de bypass de prompt injection |
| garak — LLM Vulnerability Scanner | https://github.com/NVIDIA/garak | Herramienta de fuzzing automatizado de LLMs para detectar vectores de inyección y jailbreak |
| PromptMe — OWASP Project | https://owasp.org/www-project-promptme/ | Aplicación OWASP de chatbot intencionalmente vulnerable alineada con el LLM Top 10 |

---

### LLM-02: Indirect Prompt Injection via RAG Document Poisoning

| Recurso | URL | Propósito |
|---------|-----|-----------|
| OWASP LLM Top 10 2025 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Referencia oficial: LLM02 (Insecure Output Handling) e inyección indirecta via RAG |
| Damn Vulnerable LLM Agent | https://github.com/ReversecLabs/damn-vulnerable-llm-agent | Agente LangChain con RAG y tool-calling intencionalmente vulnerable a inyección indirecta |
| Ollama | https://github.com/ollama/ollama | Backend LLM local que sirve el modelo para el agente RAG vulnerable |
| garak — LLM Vulnerability Scanner | https://github.com/NVIDIA/garak | Scanner automatizado para validar vectores de inyección indirecta en pipelines RAG |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de instrucciones arbitrarias inyectadas via documentos envenenados |

---

### LLM-03: IDOR in Chat History API

| Recurso | URL | Propósito |
|---------|-----|-----------|
| OWASP LLM Top 10 2025 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Referencia oficial: LLM10 (Insecure Plugin Design) e IDOR en APIs de aplicaciones LLM |
| Damn Vulnerable LLM Agent | https://github.com/ReversecLabs/damn-vulnerable-llm-agent | Aplicación con endpoints IDOR-vulnerables en historial de chat (IDs secuenciales sin auth) |
| Ollama | https://github.com/ollama/ollama | Backend LLM que alimenta la aplicación con el historial de conversaciones |
| MITRE ATT&CK T1078 — Valid Accounts | https://attack.mitre.org/techniques/T1078/ | Técnica de acceso a recursos usando credenciales o sesiones de otras cuentas |
| PromptMe — OWASP Project | https://owasp.org/www-project-promptme/ | Proyecto OWASP de referencia para vulnerabilidades en APIs de aplicaciones LLM |

---

## Dominio: Multi-Step APT Chains

### ATP-01: HAFNIUM-Style Webshell and Lateral Movement

| Recurso | URL | Propósito |
|---------|-----|-----------|
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Shell WinRM para movimiento lateral al pivot Windows con credenciales recuperadas del tier web |
| Impacket suite | https://github.com/fortra/impacket | `psexec.py` y `smbexec.py` para ejecución remota en el segundo hop hacia el DC |
| Ligolo-ng | https://github.com/nicocha30/ligolo-ng | Pivoting L3 desde el servidor web comprometido hacia el segmento interno del DC |
| MITRE ATT&CK T1505.003 — Web Shell | https://attack.mitre.org/techniques/T1505/003/ | Técnica de instalación de webshell para persistencia y ejecución de comandos en servidor web |
| MITRE ATT&CK T1021.006 — WinRM | https://attack.mitre.org/techniques/T1021/006/ | Técnica de movimiento lateral via WinRM con credenciales válidas recuperadas del servidor web |

---

### ATP-02: SolarWinds-Style Supply Chain Backdoor

| Recurso | URL | Propósito |
|---------|-----|-----------|
| dnscat2 | https://github.com/iagox86/dnscat2 | Framework C2 por DNS tunneling; segundo hop de la cadena para eludir segmentación de red |
| Chisel | https://github.com/jpillora/chisel | Túnel TCP/SOCKS5 sobre HTTP; alternativa de pivoting para el segundo hop de la cadena |
| Ligolo-ng | https://github.com/nicocha30/ligolo-ng | Pivoting L3 para alcanzar el host aislado en el segundo segmento de red |
| MITRE ATT&CK T1195 — Supply Chain Compromise | https://attack.mitre.org/techniques/T1195/ | Técnica de compromiso de cadena de suministro de software (paquete de actualización backdoored) |
| MITRE ATT&CK T1071.004 — DNS | https://attack.mitre.org/techniques/T1071/004/ | Técnica de C2 encubierto mediante tunneling DNS (dnscat2 para eludir segmentación) |

---

### ATP-03: LAPSUS$-Style Cloud Identity Chain

| Recurso | URL | Propósito |
|---------|-----|-----------|
| AWS IMDS Documentation | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html | Referencia del endpoint IMDS para robo de token de service account K8s expuesto en metadatos |
| k3s Official Documentation | https://docs.k3s.io/ | Instalación del clúster K8s del laboratorio; contexto de etcd y acceso al datastore del clúster |
| Impacket suite | https://github.com/fortra/impacket | `secretsdump.py` para extracción de credenciales del etcd del clúster K8s comprometido |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de robo de token de service account K8s via IMDS + SSRF |
| MITRE ATT&CK T1602 — Data from Configuration Repository | https://attack.mitre.org/techniques/T1602/ | Técnica de extracción de secretos desde etcd (repositorio de configuración del clúster K8s) |

---

### ATP-04: Volt Typhoon Living-Off-the-Land Chain

| Recurso | URL | Propósito |
|---------|-----|-----------|
| mitm6 | https://github.com/dirkjanm/mitm6 | Primer eslabón: DHCPv6 rogue para creación de cuenta privilegiada via relay LDAP sin tocar disco |
| Impacket ntlmrelayx | https://github.com/fortra/impacket | Relay de autenticaciones WPAD a `ldaps://` para crear cuenta de dominio via LDAP relay |
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Autenticación WinRM al member server con la cuenta creada; recuperación del primer flag |
| Rubeus | https://github.com/GhostPack/Rubeus | Kerberoasting desde el pivot para obtener TGS descifrables de cuentas de servicio |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de relay de autenticaciones via DHCPv6/WPAD sin persistencia en disco |
