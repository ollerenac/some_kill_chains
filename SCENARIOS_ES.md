# Catálogo de Escenarios CTF — Laboratorio Avanzado de Ciberseguridad

Este catálogo presenta 23 escenarios Capture-The-Flag propuestos para estudiantes avanzados de pregrado y posgrado en ciberseguridad. Cada escenario está diseñado para cubrir las brechas temáticas en un marco de laboratorio existente, incorporando dominios de ataque modernos aún no representados: explotación de Active Directory, abuso de protocolos de red, weaponización de CVEs, seguridad en la nube y contenedores, seguridad de LLMs, y cadenas de ataque tipo APT de múltiples pasos. Cada escenario funciona con un máximo de tres máquinas virtuales — esta es una restricción de infraestructura estricta. Los estudiantes deben redactar todo el código de explotación y weaponización por su cuenta; los marcos completamente automatizados como Metasploit están excluidos por diseño.

---

## Active Directory / Windows

### AD-01: Kerberoasting y AS-REP Roasting

**Dificultad:** Fácil
**VMs:** 2

Eres un usuario de dominio con privilegios reducidos en un dominio Windows repleto de cuentas de servicio con SPNs registrados y cuentas de usuario configuradas sin preautenticación Kerberos. Tu objetivo es enumerar ambas superficies de ataque, recolectar tickets de servicio y blobs AS-REP, y craquearlos sin conexión con Hashcat para recuperar las credenciales. Usando GetUserSPNs.py junto con enumeración dirigida, identificas qué cuentas son vulnerables a cada técnica y recopilas el material de tickets necesario para el análisis offline.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#ad-01-kerberoasting-y-as-rep-roasting)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Impacket (GetUserSPNs / GetNPUsers) | https://github.com/fortra/impacket | Suite de protocolos SMB/Kerberos; `GetUserSPNs.py` y `GetNPUsers.py` recolectan tickets Kerberoastables y blobs AS-REP |
| Hashcat | https://hashcat.net/hashcat/ | Motor de crackeo offline para hashes Kerberos 5 (`-m 13100` para TGS, `-m 18200` para AS-REP) |
| Rubeus | https://github.com/GhostPack/Rubeus | Herramienta .NET para solicitar y manipular tickets Kerberos directamente desde Windows |
| HackTricks — Kerberoast | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/kerberoast | Guía técnica completa de Kerberoasting y AS-REP Roasting con sintaxis de comandos |
| MITRE ATT&CK T1558.003 — Kerberoasting | https://attack.mitre.org/techniques/T1558/003/ | Entrada oficial de la técnica con detecciones y mitigaciones recomendadas |

---

### AD-02: LLMNR/NBT-NS Poisoning y Relay NTLM

**Dificultad:** Medio
**VMs:** 2

Estás posicionado en una red de dominio Windows donde la resolución de nombres por difusión LLMNR y NBT-NS permanece habilitada — una mala configuración que permite a cualquier host del segmento responder a consultas de nombres no resueltos. Usando Responder, envenas las solicitudes de difusión y capturas hashes NTLMv2 de challenge-response de usuarios del dominio que se autentican ante un recurso inexistente. En lugar de craquear el hash capturado, lo canalizas directamente a través de ntlmrelayx para reenviar la credencial a un servicio del dominio, obteniendo ejecución de comandos en una estación de trabajo objetivo, sin necesidad de recuperar ninguna contraseña en texto plano.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#ad-02-envenenamiento-llmnrnbt-ns-y-relay-ntlm)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Responder | https://github.com/lgandx/Responder | Herramienta de poisoning LLMNR/NBT-NS/mDNS que captura hashes NTLMv2 en redes Windows |
| Impacket ntlmrelayx | https://github.com/fortra/impacket | `ntlmrelayx.py` reenvía credenciales NTLM capturadas a servicios SMB/LDAP/MSSQL |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Sucesor de CrackMapExec; enumera y ejecuta comandos via SMB, WinRM y LDAP |
| MITRE ATT&CK T1557.001 — LLMNR/NBT-NS Poisoning | https://attack.mitre.org/techniques/T1557/001/ | Técnica oficial: Adversary-in-the-Middle via envenenamiento de resolución de nombres |
| HackTricks — LLMNR/NBT-NS Relay | https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/spoofing-llmnr-nbt-ns-mdns-dns-and-wpad-and-relay-attacks | Guía detallada de ataques de relay NTLM encadenados con Responder y ntlmrelayx |

---

### AD-03: Explotación de Rutas ACL con BloodHound

**Dificultad:** Medio
**VMs:** 2

Has obtenido una cuenta de dominio con privilegios reducidos y necesitas escalar tu acceso hasta Domain Admin. Usando SharpHound para recopilar datos de relaciones de Active Directory y BloodHound para visualizar las rutas de ataque, identificas una cadena de aristas de Access Control List explotables — específicamente un permiso WriteDACL o GenericWrite que posee tu cuenta comprometida sobre un objeto con mayores privilegios. Explotas esta arista para otorgarte los derechos necesarios para una mayor escalada, encadenando los pasos hasta alcanzar Domain Admin.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#ad-03-ruta-de-abuso-acl-con-bloodhound)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| BloodHound Community Edition | https://github.com/SpecterOps/BloodHound | Plataforma de análisis de grafos AD para identificar rutas de ataque (versión CE oficial) |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Enumeración LDAP y SMB para identificar usuarios y permisos del dominio |
| PowerView | https://github.com/PowerShellMafia/PowerSploit/blob/master/Recon/PowerView.ps1 | Script PowerShell para enumerar objetos AD, ACLs y propiedades de cuentas |
| HackTricks — ACL Abuse | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/acl-persistence-abuse | Guía de abuso de ACLs: WriteDACL, GenericWrite, GenericAll y cadenas de escalación |
| MITRE ATT&CK T1098 — Account Manipulation | https://attack.mitre.org/techniques/T1098/ | Técnica de manipulación de cuentas y permisos para mantener acceso en entornos AD |

---

### AD-04: Abuso de Certificados ADCS ESC1

**Dificultad:** Difícil
**VMs:** 2

Tienes una cuenta de dominio con privilegios reducidos y descubres que la organización ha desplegado Active Directory Certificate Services con una plantilla de certificado mal configurada. La plantilla permite la inscripción a usuarios con bajos privilegios, incluye el EKU de Client Authentication y permite que el Subject Alternative Name sea especificado por el solicitante. Usando Certipy, enumeras la plantilla vulnerable, solicitas un certificado falso que suplanta la identidad de una cuenta de Domain Admin, y te autenticas vía PKINIT para obtener un ticket-granting ticket Kerberos de esa cuenta privilegiada — otorgándote acceso de Domain Admin.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#ad-04-abuso-de-certificados-adcs-esc1)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Certipy | https://github.com/ly4k/Certipy | Herramienta Python para enumerar y explotar configuraciones erróneas de ADCS (ESC1–ESC16) |
| Impacket (PKINIT / gettgt) | https://github.com/fortra/impacket | `gettgtpkinit.py` y `getnthash.py` para autenticación PKINIT y obtención de TGT mediante certificado |
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Shell WinRM con soporte de certificados para acceso post-explotación a hosts Windows |
| MITRE ATT&CK T1649 — Steal or Forge Auth Certificates | https://attack.mitre.org/techniques/T1649/ | Técnica oficial de abuso de certificados de autenticación en entornos AD CS |
| HackTricks — ADCS ESC1 | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/ad-certificates | Guía técnica de explotación de plantillas ADCS misconfigured con Certipy |

---

### AD-05: Cadena APT al Estilo Conti  [Multi-paso — 2 banderas]

**Dificultad:** Difícil
**VMs:** 3

Entras a un entorno de dominio Windows de tres máquinas con solo una estación de trabajo atacante y sin credenciales. Desplegando Responder para envenenar las solicitudes de difusión LLMNR en el segmento interno, usas ntlmrelayx para reenviar los hashes capturados por SMB a un servidor miembro del dominio — estableciendo un punto de apoyo y asegurando tu primer objetivo. Con tu posición de pivote asegurada, usas Rubeus para solicitar tickets de servicio de cuentas susceptibles a Kerberoasting, craqueas el ticket offline con Hashcat, y usas las credenciales recuperadas con evil-winrm para moverte lateralmente al controlador de dominio y completar la cadena. Cada salto de movimiento lateral usa un protocolo distinto — SMB para el primero, WinRM para el segundo.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#ad-05-cadena-apt-al-estilo-conti)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Responder | https://github.com/lgandx/Responder | Primer eslabón: captura hashes NTLMv2 mediante poisoning de broadcast en el segmento interno |
| Rubeus | https://github.com/GhostPack/Rubeus | Kerberoasting de cuentas de servicio para obtener tickets TGS descifrables offline |
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Movimiento lateral al DC mediante WinRM con credenciales crackeadas |
| Hashcat | https://hashcat.net/hashcat/ | Crackeo offline de tickets TGS Kerberoasteados (`-m 13100`) |
| MITRE ATT&CK T1550.002 — Pass the Hash | https://attack.mitre.org/techniques/T1550/002/ | Técnica de reutilización de hashes NTLM para movimiento lateral sin recuperar contraseña |

---

## Explotación de Protocolos de Red

### NET-01: SMB Relay a través de Recursos Compartidos sin Firma

**Dificultad:** Fácil
**VMs:** 2

Descubres un segmento de red donde la firma SMB no está impuesta en las estaciones de trabajo — una mala configuración común en entornos que nunca han reforzado su configuración predeterminada de Windows. Colocando Responder en modo análisis para evitar el envenenamiento y usando ntlmrelayx para reenviar intentos de autenticación capturados, interceptas la autenticación SMB de un usuario del dominio y la reenvías en tiempo real a un recurso compartido en un host objetivo. La credencial reenviada te otorga acceso de lectura al recurso compartido, sin necesidad de craquear ni recuperar ninguna contraseña.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#net-01-relay-smb-a-través-de-recursos-compartidos-sin-firma)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Impacket ntlmrelayx | https://github.com/fortra/impacket | `ntlmrelayx.py` intercepta y reenvía autenticaciones SMB a recursos sin firma obligatoria |
| Responder | https://github.com/lgandx/Responder | Modo análisis (`-A`) para captura pasiva sin envenenar; fuente de las credenciales a relayar |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Enumera qué hosts tienen SMB signing deshabilitado: `nxc smb <rango> --gen-relay-list` |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de interposición entre autenticación cliente-servidor para relay de credenciales |
| HackTricks — LLMNR/NBT-NS Relay | https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/spoofing-llmnr-nbt-ns-mdns-dns-and-wpad-and-relay-attacks | Detalle técnico del relay SMB con ntlmrelayx, incluyendo opciones de modo silencioso |

---

### NET-02: DHCPv6 Falso por IPv6 y Relay a LDAP

**Dificultad:** Medio
**VMs:** 2

Observas que el dominio Windows objetivo no tiene gestión IPv6 implementada, dejando a todos los hosts susceptibles a anuncios DHCPv6 falsos. Usando mitm6, levantas un servidor DHCPv6 falso que se asigna a sí mismo como puerta de enlace predeterminada IPv6 y servidor DNS para los hosts del dominio, provocando que envíen solicitudes de autenticación del proxy WPAD a tu máquina atacante. Reenvías estos intentos de autenticación a LDAP mediante ntlmrelayx, aprovechando la credencial reenviada para crear una nueva cuenta de dominio privilegiada — sin ejecución de código, sin malware, sin craqueo de hashes requerido. Usas la cuenta recién creada para autenticarte y completar tu objetivo.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#net-02-dhcpv6-falso-por-ipv6-y-relay-a-ldap)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| mitm6 | https://github.com/dirkjanm/mitm6 | Servidor DHCPv6 malicioso que se asigna como DNS IPv6 predeterminado en redes Windows |
| Impacket ntlmrelayx | https://github.com/fortra/impacket | Relay de autenticaciones WPAD capturadas hacia LDAP para crear cuentas privilegiadas |
| NetExec (nxc) | https://github.com/Pennyw0rth/NetExec | Verificación post-ataque de la cuenta creada vía `nxc ldap` y `nxc smb` |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de interposición usando DHCPv6/WPAD para capturar y relayar autenticaciones |
| MITRE ATT&CK T1098 — Account Manipulation | https://attack.mitre.org/techniques/T1098/ | Técnica de creación de cuentas privilegiadas mediante relay LDAP autenticado |

---

### NET-03: Envenenamiento de Caché ARP e Interceptación de Credenciales

**Dificultad:** Fácil
**VMs:** 2

Estás en el mismo segmento de Capa 2 que dos hosts que se comunican y debes interceptar su tráfico. Usando bettercap, envías respuestas ARP gratuitas para envenenar las cachés ARP de ambos objetivos, enrutando su tráfico a través de tu máquina y posicionándote como hombre en el medio. Explotas el proxy HTTPS de bettercap para degradar las conexiones cifradas a HTTP en texto plano, capturando las credenciales transmitidas por los hosts.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#net-03-envenenamiento-de-caché-arp-e-interceptación-de-credenciales)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| bettercap | https://github.com/bettercap/bettercap | Framework MITM con módulos ARP spoof, sniffer y proxy HTTPS para interceptación de tráfico |
| Scapy | https://scapy.readthedocs.io/en/latest/ | Librería Python para crafting de paquetes ARP gratuitous y análisis de tráfico interceptado |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de posicionamiento MITM mediante envenenamiento de caché ARP en capa 2 |
| MITRE ATT&CK T1040 — Network Sniffing | https://attack.mitre.org/techniques/T1040/ | Técnica de captura pasiva de credenciales en tráfico de red interceptado |
| Bettercap — sitio oficial | https://www.bettercap.org/ | Documentación oficial de módulos, capturers y proxy HTTPS de bettercap |

---

### NET-04: Envenenamiento de Caché DNS

**Dificultad:** Medio
**VMs:** 2

Identificas un resolver DNS desplegado en la red objetivo que está mal configurado para aceptar respuestas sin una adecuada aleatorización del puerto de origen ni validación del ID de consulta. Inyectando respuestas DNS falsificadas que se adelantan al resolver legítimo upstream, corrompres la caché del resolver para que un hostname interno objetivo resuelva a una dirección IP que tú controlas. Cuando un servicio interno legítimo consulta el nombre envenenado, envía su solicitud HTTP a tu máquina — confirmando el éxito del envenenamiento.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#net-04-envenenamiento-de-caché-dns)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Scapy | https://scapy.readthedocs.io/en/latest/ | Crafting de respuestas DNS forjadas con ID de transacción y puerto fuente manipulados |
| bettercap | https://github.com/bettercap/bettercap | Módulo `dns.spoof` para inyección automatizada de respuestas DNS falsas en la red local |
| FRRouting (FRR) | https://frrouting.org/ | Daemon de enrutamiento en el VM víctima; usado para simular el resolver DNS misconfigured |
| MITRE ATT&CK T1568 — Dynamic Resolution | https://attack.mitre.org/techniques/T1568/ | Técnica de manipulación de resolución DNS para redirigir tráfico a infraestructura controlada |
| Scapy OSPF contrib | https://scapy.readthedocs.io/en/latest/api/scapy.contrib.ospf.html | Referencia de la API Scapy para construcción de paquetes de protocolos de red avanzados |

---

## Weaponización de CVEs

### CVE-01: EternalBlue — MS17-010 (CVE-2017-0144)

**Dificultad:** Difícil
**VMs:** 2

Te enfrentas a un objetivo con Windows 7 SP1 que tiene SMBv1 habilitado y ningún parche de seguridad aplicado — el entorno exacto que convirtió a CVE-2017-0144 en una de las vulnerabilidades más destructivas de la historia. En lugar de recurrir a un framework automatizado, redactas un exploit en Python que implementa la configuración de transacción SMBv1, el heap grooming y la puesta en escena del shellcode de DoublePulsar tú mismo, usando el andamiaje de protocolo `mysmb.py` proporcionado como base. Construyes la lista FEA malformada que desencadena el desbordamiento de búfer, introduces tu carga a través del implante DoublePulsar, y obtienes una shell en el objetivo. Completar este escenario requiere que entiendas el encuadre del protocolo SMBv1 a nivel de paquete — no solo ejecutar una herramienta preconstruida.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#cve-01-eternalblue-ms17-010)

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

**Dificultad:** Medio
**VMs:** 2

Identificas una aplicación Java que registra entradas controladas por el atacante usando una versión vulnerable de la biblioteca Apache Log4j. En lugar de usar un kit de exploit preconstruido, redactas una cadena de payload de inyección JNDI y construyes un servidor de cadena de exploit basado en Python que sirve tanto una redirección LDAP como una clase Java maliciosa por HTTP. Cuando la aplicación registra tu entrada elaborada, la biblioteca Log4j inicia una búsqueda JNDI saliente a tu servidor, descarga y ejecuta tu clase, y logras ejecución de comandos del sistema operativo en el objetivo.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#cve-02-log4shell-cve-2021-44228)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| NVD — CVE-2021-44228 | https://nvd.nist.gov/vuln/detail/CVE-2021-44228 | Entrada oficial con CVSS 10.0, descripción de la inyección JNDI y versiones afectadas |
| axelcurmi/log4shell-docker-lab | https://github.com/axelcurmi/log4shell-docker-lab | Laboratorio Docker listo para usar con la aplicación vulnerable pinned a Log4j 2.14.1 |
| christophetd/log4shell-vulnerable-app | https://github.com/christophetd/log4shell-vulnerable-app | Imagen Docker de aplicación Spring vulnerable; referencia para construir el servidor LDAP + HTTP |
| MITRE ATT&CK T1190 — Exploit Public-Facing Application | https://attack.mitre.org/techniques/T1190/ | Técnica de explotación remota de aplicaciones Java vía inyección JNDI en headers HTTP |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de código arbitrario mediante la clase Java maliciosa descargada |

---

### CVE-03: Apache Struts S2-045 — CVE-2017-5638 (Vector de la Brecha Equifax)

**Dificultad:** Medio
**VMs:** 2

Te enfrentas a una aplicación web Apache Struts 2 ejecutándose en un contenedor Docker en el servidor objetivo. La aplicación procesa solicitudes de carga de archivos multiparte usando el parser vulnerable de Jakarta — la misma mala configuración que posibilitó la brecha de Equifax en 2017. Escribes un script de exploit en Python que inyecta una expresión OGNL en el encabezado Content-Type de una solicitud HTTP POST, eludiendo las restricciones de seguridad de Struts 2 y ejecutando comandos arbitrarios del sistema operativo en el servidor. No se necesita un webshell JSP — el exploit devuelve la salida de los comandos directamente en la respuesta HTTP. Usas esta ejecución remota de comandos para completar tu objetivo en el servidor.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#cve-03-apache-struts-s2-045-cve-2017-5638)

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

**Dificultad:** Medio
**VMs:** 2

Has obtenido una sesión interactiva con privilegios reducidos en un servidor Windows objetivo y necesitas escalar a SYSTEM. El servicio Windows Print Spooler está en ejecución y el objetivo no tiene parches aplicados contra PrintNightmare. Redactas un payload en C o Python que instruye al servicio Windows Print Spooler — que se ejecuta como SYSTEM — para cargar una DLL maliciosa que tú suministras, inyectando tu código en un proceso a nivel SYSTEM. Una vez que tu payload se ejecuta con privilegios elevados, completas tu objetivo. Este escenario ejercita la ruta de escalada de privilegios local, requiriendo un punto de apoyo preexistente en lugar de una posición de red externa.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#cve-04-printnightmare-lpe-cve-2021-34527)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| NVD — CVE-2021-34527 | https://nvd.nist.gov/vuln/detail/CVE-2021-34527 | Entrada oficial con CVSS 8.8; describe LPE y RCE via Windows Print Spooler |
| cube0x0/CVE-2021-1675 | https://github.com/cube0x0/CVE-2021-1675 | PoC C# y Python; implementación de referencia del LPE por inyección de DLL en Spooler |
| Impacket (rpcdump / rprn) | https://github.com/fortra/impacket | `rpcdump.py` para verificar el servicio Spooler; `rprn` module para explotación via RPC |
| MITRE ATT&CK T1068 — Exploitation for Privilege Escalation | https://attack.mitre.org/techniques/T1068/ | Técnica de escalación de privilegios locales mediante explotación del Spooler de impresión |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de payload DLL con privilegios SYSTEM via Spooler |

---

## Seguridad en la Nube y Contenedores

### CC-01: SSRF en IMDS y Robo de Credenciales IAM

**Dificultad:** Fácil
**VMs:** 2

Descubres una aplicación web que realiza solicitudes HTTP del lado del servidor basadas en entradas controladas por el atacante — una superficie SSRF clásica. Elaborando solicitudes que apuntan al endpoint simulado del AWS Instance Metadata Service en 169.254.169.254, recuperas las credenciales del rol IAM adjunto al host de la aplicación. Usando esas credenciales temporales robadas, consultas una API S3 simulada para enumerar los objetos disponibles y completar tu objetivo. No se requiere bypass de autenticación ni ejecución de código — la vulnerabilidad SSRF hace el trabajo.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#cc-01-ssrf-en-aws-imds-y-robo-de-credenciales-iam)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| AWS IMDS Documentation | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html | Documentación oficial del endpoint 169.254.169.254; estructura de credenciales IAM temporales |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de robo de credenciales desde el servicio de metadatos de instancia cloud |
| MITRE ATT&CK T1190 — Exploit Public-Facing Application | https://attack.mitre.org/techniques/T1190/ | Técnica de SSRF para alcanzar endpoints internos no expuestos directamente |
| Docker Security Documentation | https://docs.docker.com/engine/security/ | Referencia de configuración segura de contenedores y aislamiento de red |
| HackTricks — Active Directory Methodology | https://book.hacktricks.xyz/windows-hardening/active-directory-methodology | Contexto sobre técnicas de enumeración y explotación aplicables a entornos cloud-AD |

---

### CC-02: Escape de Contenedor Docker Privilegiado

**Dificultad:** Medio
**VMs:** 2

Aterrizas dentro de un contenedor Docker deliberadamente mal configurado que se ejecuta como root con capacidades Linux elevadas. Desde dentro del contenedor, descubres que el nivel de privilegio otorgado a este contenedor extiende el acceso a interfaces del kernel del host que normalmente están aisladas de los namespaces de contenedores. Escribes un payload que abusa de una ruta de notificación cgroup para programar la ejecución de comandos en el host subyacente, plantando una conexión inversa o leyendo datos sensibles directamente desde el directorio raíz del host. El desafío evalúa tu comprensión de los límites de aislamiento de contenedores Linux y las condiciones en que un contenedor privilegiado deja de proporcionar una separación significativa del host.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#cc-02-escape-de-contenedor-docker-privilegiado)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| Trail of Bits — Understanding Docker Container Escapes | https://blog.trailofbits.com/2019/07/19/understanding-docker-container-escapes/ | Investigación original que documenta el escape via `cgroup release_agent` desde contenedor privilegiado |
| Docker Security Documentation | https://docs.docker.com/engine/security/ | Documentación oficial sobre `--privileged`, capabilities y aislamiento de namespaces |
| MITRE ATT&CK T1611 — Escape to Host | https://attack.mitre.org/techniques/T1611/ | Técnica oficial de escape de contenedor para acceder al sistema operativo del host subyacente |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de acceso a secretos y credenciales expuestas en el entorno de contenedor |
| Kubernetes Goat — Container Escape Scenario | https://madhuakula.com/kubernetes-goat/docs/scenarios/scenario-4/container-escape-to-the-host-system-in-kubernetes-containers/welcome/ | Laboratorio interactivo de referencia para técnicas de escape de contenedor en entornos K8s |

---

### CC-03: Escape por Cuenta de Servicio Mal Configurada en Kubernetes

**Dificultad:** Difícil
**VMs:** 2

Obtienes acceso inicial a un clúster Kubernetes como usuario con bajos privilegios y recibes un token de cuenta de servicio con más permisos de los previstos. Usando kubectl, enumeras los recursos del clúster — pods, roles, role bindings y secrets — para mapear el alcance de los permisos sobreaprovisionados. Construyes y despliegas una especificación de pod privilegiado con un volumen hostPath que monta el sistema de archivos raíz del nodo host, luego ejecutas en el pod para acceder directamente al sistema de archivos del host y completar tu objetivo.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#cc-03-escape-de-cuenta-de-servicio-mal-configurada-en-kubernetes)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| k3s Official Documentation | https://docs.k3s.io/ | Instalación del clúster K8s single-node para el entorno de laboratorio |
| Kubernetes Goat — Container Escape Scenario | https://madhuakula.com/kubernetes-goat/docs/scenarios/scenario-4/container-escape-to-the-host-system-in-kubernetes-containers/welcome/ | Escenario de referencia: hostPath mount y privesc desde pod al nodo host |
| MITRE ATT&CK T1611 — Escape to Host | https://attack.mitre.org/techniques/T1611/ | Técnica de escape de pod K8s mediante hostPath volume con acceso al filesystem del nodo |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de robo de tokens de service account K8s desde el API server |
| MITRE ATT&CK T1098 — Account Manipulation | https://attack.mitre.org/techniques/T1098/ | Técnica de aprovechamiento de role bindings misconfigured para escalación en el clúster |

---

## Seguridad en LLMs

### LLM-01: Bypass de Inyección de Prompts en Múltiples Capas

**Dificultad:** Fácil
**VMs:** 2

Interactúas con un chatbot respaldado por Ollama que parece resistir tus intentos de inyección iniciales — la aplicación impone un límite de system prompt, un filtro basado en regex sobre patrones de inyección comunes, y una capa de validación semántica que verifica si tu entrada parece un ataque. Tu objetivo es encadenar al menos dos técnicas de bypass distintas para atravesar las defensas en capas, anular el system prompt y hacer que el modelo produzca la salida objetivo. Entender cómo falla cada capa de defensa individualmente — y cómo pueden ser eludidas en secuencia — es el desafío central.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#llm-01-inyección-de-prompt-multi-capa)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| OWASP LLM Top 10 2025 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Referencia oficial: LLM01 (Prompt Injection) y categorías de bypass de defensas en LLMs |
| Ollama | https://github.com/ollama/ollama | Runtime de modelos LLM local (phi3, llama3.2) que sirve como backend del chatbot víctima |
| Bishop Fox LLM CTF Lab | https://bishopfox.com/blog/large-language-models-llm-ctf-lab | Laboratorio CTF de referencia con desafíos multi-capa de bypass de prompt injection |
| garak — LLM Vulnerability Scanner | https://github.com/NVIDIA/garak | Herramienta de fuzzing automatizado de LLMs para detectar vectores de inyección y jailbreak |
| PromptMe — OWASP Project | https://owasp.org/www-project-promptme/ | Aplicación OWASP de chatbot intencionalmente vulnerable alineada con el LLM Top 10 |

---

### LLM-02: Inyección Indirecta de Prompts vía Envenenamiento de Documentos RAG

**Dificultad:** Medio
**VMs:** 2

Descubres una aplicación de chatbot que usa Retrieval-Augmented Generation, ingiriendo documentos externos en una base de datos vectorial para enriquecer sus respuestas. Elaboras un documento malicioso que contiene instrucciones inyectadas ocultas dentro de contenido aparentemente benigno y haces que sea ingerido en el vector store. Cuando un usuario legítimo envía una consulta rutinaria, el chatbot recupera tu documento envenenado como contexto relevante, y las instrucciones embebidas se activan — demostrando el ataque de envenenamiento. Este escenario explora la superficie de ataque introducida cuando un LLM confía ciegamente en el contenido proveniente de fuentes externas recuperadas de su base de conocimiento.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#llm-02-inyección-indirecta-de-prompt-mediante-envenenamiento-de-rag)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| OWASP LLM Top 10 2025 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Referencia oficial: LLM02 (Insecure Output Handling) e inyección indirecta via RAG |
| Damn Vulnerable LLM Agent | https://github.com/ReversecLabs/damn-vulnerable-llm-agent | Agente LangChain con RAG y tool-calling intencionalmente vulnerable a inyección indirecta |
| Ollama | https://github.com/ollama/ollama | Backend LLM local que sirve el modelo para el agente RAG vulnerable |
| garak — LLM Vulnerability Scanner | https://github.com/NVIDIA/garak | Scanner automatizado para validar vectores de inyección indirecta en pipelines RAG |
| MITRE ATT&CK T1059 — Command and Scripting Interpreter | https://attack.mitre.org/techniques/T1059/ | Técnica de ejecución de instrucciones arbitrarias inyectadas via documentos envenenados |

---

### LLM-03: IDOR en la API de Historial de Chat

**Dificultad:** Medio
**VMs:** 2

Interactúas con una aplicación LLM que almacena el historial de conversaciones y expone un endpoint de API para recuperar sesiones de chat pasadas. El endpoint usa identificadores de conversación predecibles y secuenciales y no realiza ninguna validación de control de acceso significativa — una vulnerabilidad de referencia directa a objetos inseguros a nivel de capa de aplicación. Enumerando los IDs de conversación a través del endpoint, accedes a sesiones de chat pertenecientes a otros usuarios, llegando eventualmente a datos de conversación de un usuario privilegiado. El desafío reside completamente en el fallo de la aplicación para autenticar la propiedad del recurso solicitado.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#llm-03-idor-en-la-api-de-historial-de-chat-del-llm)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| OWASP LLM Top 10 2025 | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | Referencia oficial: LLM10 (Insecure Plugin Design) e IDOR en APIs de aplicaciones LLM |
| Damn Vulnerable LLM Agent | https://github.com/ReversecLabs/damn-vulnerable-llm-agent | Aplicación con endpoints IDOR-vulnerables en historial de chat (IDs secuenciales sin auth) |
| Ollama | https://github.com/ollama/ollama | Backend LLM que alimenta la aplicación con el historial de conversaciones |
| MITRE ATT&CK T1078 — Valid Accounts | https://attack.mitre.org/techniques/T1078/ | Técnica de acceso a recursos usando credenciales o sesiones de otras cuentas |
| PromptMe — OWASP Project | https://owasp.org/www-project-promptme/ | Proyecto OWASP de referencia para vulnerabilidades en APIs de aplicaciones LLM |

---

## Cadenas APT de Múltiples Pasos

### ATP-01: Webshell y Movimiento Lateral al Estilo HAFNIUM  [Multi-paso — 2 banderas]

**Dificultad:** Difícil
**VMs:** 3

Comienzas con el conocimiento de una aplicación web de cara a internet que procesa URLs suministradas por el usuario en un contexto del lado del servidor. Elaborando payloads SSRF, alcanzas un servicio interno inaccesible desde el exterior, y escalando ese acceso cargas un webshell en el servidor de la aplicación que te otorga ejecución de código. Recopilando credenciales encontradas en el nivel web comprometido, las usas con evil-winrm para autenticarte en un host Windows pivot interno — asegurando tu primer objetivo. Desde el pivot, enumeras recursos del dominio e identificas una ruta hacia el controlador de dominio, siguiéndola para completar la cadena.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#atp-01-pivote-ssrf-al-estilo-hafnium-hacia-el-controlador-de-dominio)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Shell WinRM para movimiento lateral al pivot Windows con credenciales recuperadas del tier web |
| Impacket suite | https://github.com/fortra/impacket | `psexec.py` y `smbexec.py` para ejecución remota en el segundo hop hacia el DC |
| Ligolo-ng | https://github.com/nicocha30/ligolo-ng | Pivoting L3 desde el servidor web comprometido hacia el segmento interno del DC |
| MITRE ATT&CK T1505.003 — Web Shell | https://attack.mitre.org/techniques/T1505/003/ | Técnica de instalación de webshell para persistencia y ejecución de comandos en servidor web |
| MITRE ATT&CK T1021.006 — WinRM | https://attack.mitre.org/techniques/T1021/006/ | Técnica de movimiento lateral via WinRM con credenciales válidas recuperadas del servidor web |

---

### ATP-02: Backdoor en Cadena de Suministro al Estilo SolarWinds  [Multi-paso — 2 banderas]

**Dificultad:** Difícil
**VMs:** 3

Se te entrega acceso a un servidor de distribución de actualizaciones de software simulado — la fuente upstream en la que los objetivos downstream confían implícitamente. Modificas un paquete de actualización para incluir un backdoor que se ejecuta silenciosamente cuando el objetivo downstream aplica la actualización, y una vez que la actualización con backdoor se ejecuta en el host downstream completas tu primer objetivo en el host comprometido. Con tu punto de apoyo establecido, cambias al segundo objetivo: un objetivo adicional más aislado al que no es posible llegar directamente desde tu posición. Estableces un canal de comando y control encubierto tunelizando las comunicaciones a través de DNS usando dnscat2, eludiendo la segmentación de red, y completas tu segundo objetivo en el host aislado.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#atp-02-compromiso-de-cadena-de-suministro-al-estilo-solarwinds-c2-dns)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| dnscat2 | https://github.com/iagox86/dnscat2 | Framework C2 por DNS tunneling; segundo hop de la cadena para eludir segmentación de red |
| Chisel | https://github.com/jpillora/chisel | Túnel TCP/SOCKS5 sobre HTTP; alternativa de pivoting para el segundo hop de la cadena |
| Ligolo-ng | https://github.com/nicocha30/ligolo-ng | Pivoting L3 para alcanzar el host aislado en el segundo segmento de red |
| MITRE ATT&CK T1195 — Supply Chain Compromise | https://attack.mitre.org/techniques/T1195/ | Técnica de compromiso de cadena de suministro de software (paquete de actualización backdoored) |
| MITRE ATT&CK T1071.004 — DNS | https://attack.mitre.org/techniques/T1071/004/ | Técnica de C2 encubierto mediante tunneling DNS (dnscat2 para eludir segmentación) |

---

### ATP-03: Cadena de Identidad en la Nube al Estilo LAPSUS$  [Multi-paso — 2 banderas]

**Dificultad:** Difícil
**VMs:** 3

Identificas una vulnerabilidad SSRF en una aplicación alojada en la nube y la usas para consultar el Instance Metadata Service, robando un token de cuenta de servicio de Kubernetes que estaba expuesto inadvertidamente en la respuesta de metadatos. Usando kubectl con el token robado, enumeras los recursos del clúster y descubres un pod privilegiado mal configurado que te otorga acceso al nodo host — escapando del límite del contenedor y asegurando tu primer objetivo. Desde el nodo, consultas directamente el almacén de datos etcd, extrayendo los secrets y credenciales de Kubernetes que contiene. Usando las credenciales recuperadas para autenticarte como administrador en el objetivo interno final, completas la cadena de identidad en la nube.


[→ Kill-Chain](docs/KILL-CHAINS_ES.md#atp-03-cadena-de-identidad-ssrf-a-k8s-al-estilo-lapsus)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| AWS IMDS Documentation | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html | Referencia del endpoint IMDS para robo de token de service account K8s expuesto en metadatos |
| k3s Official Documentation | https://docs.k3s.io/ | Instalación del clúster K8s del laboratorio; contexto de etcd y acceso al datastore del clúster |
| Impacket suite | https://github.com/fortra/impacket | `secretsdump.py` para extracción de credenciales del etcd del clúster K8s comprometido |
| MITRE ATT&CK T1552.007 — Container API | https://attack.mitre.org/techniques/T1552/007/ | Técnica de robo de token de service account K8s via IMDS + SSRF |
| MITRE ATT&CK T1602 — Data from Configuration Repository | https://attack.mitre.org/techniques/T1602/ | Técnica de extracción de secretos desde etcd (repositorio de configuración del clúster K8s) |

---

### ATP-04: Cadena Living-Off-the-Land al Estilo Volt Typhoon  [Multi-paso — 2 banderas]

**Dificultad:** Difícil
**VMs:** 3

Operas bajo una restricción de sin-malware — sin payloads compilados, sin shellcode, sin implantes persistentes. Usando mitm6 para desplegar un servidor DHCPv6 falso y reenviando los intentos de autenticación resultantes a LDAP mediante ntlmrelayx, creas una nueva cuenta de dominio privilegiada sin tocar el sistema de archivos de ningún host objetivo. Con la nueva cuenta, usas evil-winrm para autenticarte en un servidor miembro del dominio y asegurar tu primer objetivo. Desde el pivot, enumeras SPNs de cuentas de servicio con Kerberoasting, craqueas el hash del ticket recuperado offline, y usas la credencial resultante con SMBExec o DCOM para autenticarte en el controlador de dominio y completar la cadena — toda la operación ejecutada sin soltar un solo archivo malicioso.

[→ Kill-Chain](docs/KILL-CHAINS_ES.md#atp-04-cadena-de-relay-ipv6-y-kerberoasting-al-estilo-volt-typhoon)

### Referencias

| Recurso | URL | Propósito |
|---------|-----|-----------|
| mitm6 | https://github.com/dirkjanm/mitm6 | Primer eslabón: DHCPv6 rogue para creación de cuenta privilegiada via relay LDAP sin tocar disco |
| Impacket ntlmrelayx | https://github.com/fortra/impacket | Relay de autenticaciones WPAD a `ldaps://` para crear cuenta de dominio via LDAP relay |
| evil-winrm | https://github.com/Hackplayers/evil-winrm | Autenticación WinRM al member server con la cuenta creada; movimiento lateral al objetivo |
| Rubeus | https://github.com/GhostPack/Rubeus | Kerberoasting desde el pivot para obtener TGS descifrables de cuentas de servicio |
| MITRE ATT&CK T1557 — Adversary-in-the-Middle | https://attack.mitre.org/techniques/T1557/ | Técnica de relay de autenticaciones via DHCPv6/WPAD sin persistencia en disco |

