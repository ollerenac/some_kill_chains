# CTF Propuestos × Currículo — Guía de Contacto

Este documento mapea cada escenario CTF propuesto al curso del plan de estudios con mayor afinidad temática, facilitando la identificación del profesor a contactar para integrar el escenario al laboratorio.

**Criterio de asignación primaria:** coincidencia de *técnica central* del CTF con el contenido del curso, no solo el dominio general.

---

## Tabla 1 — CTF → Cursos relevantes

| CTF | Escenario | Curso primario | Curso secundario | Razón de afinidad |
|-----|-----------|----------------|------------------|-------------------|
| AD-01 | Kerberoasting & AS-REP Roasting | CBN04 — Pentesting en Infraestructura de Red | CBG001 — Fundamentos de Ciberseguridad | Ataque sobre protocolo Kerberos (infraestructura AD/Windows); crackeo de hashes offline |
| AD-02 | LLMNR/NBT-NS Poisoning & NTLM Relay | CBN04 — Pentesting en Infraestructura de Red | CBH03 — Auditoría de Ciberseguridad | Envenenamiento de resolución de nombres en red Windows; mala configuración auditada en revisiones de seguridad |
| AD-03 | BloodHound ACL Abuse Path | CBH03 — Auditoría de Ciberseguridad | CBN04 — Pentesting en Infraestructura de Red | BloodHound es la herramienta estándar de auditoría de permisos AD; el escenario es un ejercicio de mapeo de rutas de ataque |
| AD-04 | ADCS ESC1 Certificate Abuse | CBH03 — Auditoría de Ciberseguridad | CIB01 — Seguridad de Datos | Auditoría de PKI y plantillas de certificados; abuso de cadena de confianza → acceso a datos privilegiados |
| AD-05 | Conti-Style APT Chain | CBH03 — Auditoría de Ciberseguridad | CBN21 — Informática Forense | Cadena de ataque multi-paso; genera artefactos forenses en cada salto (logs, tickets, relay events) |
| NET-01 | SMB Relay via Unsigned Shares | CBN04 — Pentesting en Infraestructura de Red | CBG001 — Fundamentos de Ciberseguridad | Relay de credenciales SMB; mala configuración de firma de paquetes en red |
| NET-02 | IPv6 Rogue DHCPv6 & LDAP Relay | CBN04 — Pentesting en Infraestructura de Red | CBN03 — Seguridad en Redes Industriales I | Explotación de protocolo DHCPv6 en red sin gestión IPv6; abuso de LDAP relay; protocolos de red presentes también en entornos industriales |
| NET-03 | ARP Cache Poisoning & Credential Interception | CBN04 — Pentesting en Infraestructura de Red | CBN03 — Seguridad en Redes Industriales I | MITM a nivel L2 (ARP); presente en redes IT e ICS/OT; ataque clásico de infraestructura de red |
| NET-04 | DNS Cache Poisoning | CBN04 — Pentesting en Infraestructura de Red | CBN03 — Seguridad en Redes Industriales I | Envenenamiento DNS; protocolo crítico tanto en redes corporativas como industriales |
| CVE-01 | EternalBlue — MS17-010 | CBS03 — Sistemas Operativos II | CBN21 — Informática Forense | Vulnerabilidad en SMBv1 a nivel de kernel Windows; análisis de exploit requiere comprensión de manejo de memoria del SO; producción de artefactos forenses analizables |
| CVE-02 | Log4Shell — CVE-2021-44228 | CBN05 — Pentesting en Aplicaciones WEB | CIB02 — Ingeniería de Software | RCE vía dependencia Log4j en aplicación Java/web; explota una librería insegura en el pipeline de software |
| CVE-03 | Apache Struts S2-045 | CBN05 — Pentesting en Aplicaciones WEB | CBH03 — Auditoría de Ciberseguridad | RCE en framework web Java (Struts); vulnerabilidad de manejo de Content-Type en capa de aplicación web |
| CVE-04 | PrintNightmare — CVE-2021-34527 | CBS03 — Sistemas Operativos II | CIB01 — Seguridad de Datos | Escalada de privilegios vía Print Spooler de Windows; carga de DLL maliciosa en contexto de kernel/SO; escalada implica acceso a datos privilegiados |
| CC-01 | IMDS SSRF & IAM Credential Theft | CBN05 — Pentesting en Aplicaciones WEB | CIB01 — Seguridad de Datos | SSRF es una clase de vulnerabilidad web (OWASP); el robo de credenciales IAM es un impacto de control de acceso a datos |
| CC-02 | Privileged Docker Container Escape | CBS03 — Sistemas Operativos II | CIB02 — Ingeniería de Software | Escape de contenedor abusa de aislamiento a nivel SO (namespaces, cgroups); Docker es infraestructura estándar de despliegue de software |
| CC-03 | Kubernetes Misconfigured Service Account Escape | CIB02 — Ingeniería de Software | CBH03 — Auditoría de Ciberseguridad | Kubernetes es la plataforma de orquestación de software moderna; la cuenta de servicio mal configurada es una mala práctica de ingeniería; auditoría de RBAC en K8s |
| LLM-01 | Multi-Layer Prompt Injection Bypass | CBS06 — Inteligencia Artificial II | CBN05 — Pentesting en Aplicaciones WEB | Ataque contra sistemas LLM con múltiples capas de filtrado; requiere comprensión de arquitectura de modelos y sus limitaciones |
| LLM-02 | Indirect Prompt Injection via RAG Poisoning | CBS06 — Inteligencia Artificial II | CBN05 — Pentesting en Aplicaciones WEB | RAG (Retrieval-Augmented Generation) es arquitectura avanzada de IA; el envenenamiento del corpus es un ataque de integridad de datos en sistemas LLM |
| LLM-03 | IDOR in LLM Chat History API | CBN05 — Pentesting en Aplicaciones WEB | CBS06 — Inteligencia Artificial II | IDOR es vulnerabilidad OWASP Top 10 en APIs web; el contexto LLM agrava el impacto (exposición de prompts/datos de otros usuarios) |
| ATP-01 | HAFNIUM-Style Webshell & Lateral Movement | CBN05 — Pentesting en Aplicaciones WEB | CBN21 — Informática Forense | El punto de entrada es un webshell vía vulnerabilidad web (Exchange/OWA); genera artefactos forenses (webshell files, event logs, lateral movement traces) |
| ATP-02 | SolarWinds-Style Supply Chain Backdoor | CIB02 — Ingeniería de Software | CBH03 — Auditoría de Ciberseguridad | El ataque compromete el pipeline de construcción/distribución de software; auditoría de cadena de suministro de software |
| ATP-03 | LAPSUS$-Style Cloud Identity Chain | CBH01 — Ingeniería Social | CBH03 — Auditoría de Ciberseguridad | LAPSUS$ usó ingeniería social (SIM swapping, insider recruitment) como vector inicial; combina identidad cloud con manipulación humana |
| ATP-04 | Volt Typhoon Living-Off-the-Land Chain | CBN21 — Informática Forense | CBS03 — Sistemas Operativos II | LOLBins (Living Off the Land Binaries) son herramientas nativas del SO usadas maliciosamente; detectarlos es el desafío central de forense de endpoints |

---

## Tabla 2 — Curso → CTFs sugeridos

| Código | Curso | Ciclo | CTFs sugeridos | Observaciones |
|--------|-------|-------|----------------|---------------|
| CBN21 | Informática Forense | 10 | ATP-04, AD-05, CVE-01, ATP-01, ATP-02 | Todos generan artefactos forenses relevantes; ATP-04 es el más puro (LOLBins = detección forense) |
| CBH03 | Auditoría de Ciberseguridad | 9 | AD-03, AD-04, CC-03, ATP-02, ATP-03, AD-05 | BloodHound, ADCS, K8s RBAC y supply chain son temas de auditoría; AD-03 es el más directo |
| CBH01 | Ingeniería Social | 7 | ATP-03 | LAPSUS$ es el único escenario donde la ingeniería social es el vector principal |
| CBN05 | Pentesting en Aplicaciones WEB | 7 | CVE-02, CVE-03, CC-01, LLM-01, LLM-02, LLM-03, ATP-01 | El curso con más CTFs relevantes; todos involucran vulnerabilidades de capa de aplicación web |
| CBS06 | Inteligencia Artificial II | 7 | LLM-01, LLM-02, LLM-03 | Dominio LLM completo; los tres escenarios requieren conocimiento de arquitecturas de modelos |
| CBS05 | Inteligencia Artificial I | 6 | LLM-01 | Solo el escenario introductorio (prompt injection simple) encaja en AI I; los otros dos requieren AI II |
| CBN04 | Pentesting en Infraestructura de Red | 6 | AD-01, AD-02, NET-01, NET-02, NET-03, NET-04 | Dominio AD (básico) y dominio NET completo; el curso más directamente alineado con el catálogo |
| CBN03 | Seguridad en Redes Industriales I | 6 | NET-02, NET-03, NET-04 | ARP, DNS y DHCPv6 son protocolos también presentes en redes OT/ICS; ángulo defensivo |
| CIB02 | Ingeniería de Software | 6 | CVE-02, CC-02, CC-03, ATP-02 | Log4Shell (dependencia insegura), Docker/K8s (despliegue) y SolarWinds (supply chain) son fallas de ingeniería de software |
| CIB01 | Seguridad de Datos | 6 | AD-04, CVE-04, CC-01, LLM-03 | ADCS (PKI), PrintNightmare (escalada → datos), SSRF/IAM e IDOR son vectores de acceso no autorizado a datos |
| CBG001 | Fundamentos de Ciberseguridad | 5 | AD-01, NET-01, NET-03 | Escenarios de dificultad Easy con conceptos base (Kerberos, SMB, ARP); buenos como primeros ejercicios |
| CBS03 | Sistemas Operativos II | 4 | CVE-01, CVE-04, CC-02, ATP-04 | EternalBlue y PrintNightmare son vulnerabilidades de kernel/SO Windows; Docker escape y LOLBins abusan del SO |
| CBS02 | Sistemas Operativos I | 2 | — | Ciclo demasiado temprano; los escenarios asumen conocimiento de redes y seguridad que aún no se ha visto |
| CBS08 | Base de Datos II | 8 | — | Ningún CTF propuesto ataca directamente motores de base de datos (SQL injection, etc.); mención posible como contexto de impacto |
| CBS04 | Base de Datos I | 6 | — | Ídem CBS08; los escenarios no cubren ataques a nivel de base de datos |
| BMA20 | Algoritmos y Estructuras de Datos II | 5 | — | Sin afinidad directa; el crackeo de hashes (AD-01) podría mencionarse como aplicación de fuerza bruta, pero es un stretch |

---

## Resumen de prioridades de contacto

| Prioridad | Código | Profesor de | CTFs a presentar |
|-----------|--------|-------------|-----------------|
| ★★★ | CBN04 | Pentesting en Infraestructura de Red | AD-01, AD-02, NET-01–04 (6 CTFs) |
| ★★★ | CBN05 | Pentesting en Aplicaciones WEB | CVE-02, CVE-03, CC-01, LLM-01–03, ATP-01 (7 CTFs) |
| ★★★ | CBH03 | Auditoría de Ciberseguridad | AD-03, AD-04, AD-05, CC-03, ATP-02, ATP-03 (6 CTFs) |
| ★★ | CBS06 | Inteligencia Artificial II | LLM-01, LLM-02, LLM-03 (3 CTFs — dominio completo) |
| ★★ | CBS03 | Sistemas Operativos II | CVE-01, CVE-04, CC-02, ATP-04 (4 CTFs) |
| ★★ | CBN21 | Informática Forense | ATP-04, AD-05, CVE-01, ATP-01 (4 CTFs) |
| ★ | CIB02 | Ingeniería de Software | CVE-02, CC-02, CC-03, ATP-02 (4 CTFs — perspectiva defensiva) |
| ★ | CIB01 | Seguridad de Datos | AD-04, CVE-04, CC-01, LLM-03 (4 CTFs) |
| ★ | CBH01 | Ingeniería Social | ATP-03 (1 CTF — vector inicial del escenario) |
| — | CBS02, CBS04, CBS08, BMA20 | — | Sin CTF con afinidad directa |
