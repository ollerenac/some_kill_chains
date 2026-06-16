# Catálogo de Escenarios CTF — Laboratorio Avanzado de Ciberseguridad

Este catálogo presenta 23 escenarios Capture-The-Flag propuestos para estudiantes avanzados de pregrado y posgrado en ciberseguridad. Cada escenario está diseñado para cubrir las brechas temáticas en un marco de laboratorio existente, incorporando dominios de ataque modernos aún no representados: explotación de Active Directory, abuso de protocolos de red, weaponización de CVEs, seguridad en la nube y contenedores, seguridad de LLMs, y cadenas de ataque tipo APT de múltiples pasos. Cada escenario funciona con un máximo de tres máquinas virtuales — esta es una restricción de infraestructura estricta. Los estudiantes deben redactar todo el código de explotación y weaponización por su cuenta; los marcos completamente automatizados como Metasploit están excluidos por diseño.

---

## Active Directory / Windows

### AD-01: Kerberoasting y AS-REP Roasting

**Dificultad:** Fácil
**VMs:** 2

Eres un usuario de dominio con privilegios reducidos en un dominio Windows repleto de cuentas de servicio con SPNs registrados y cuentas de usuario configuradas sin preautenticación Kerberos. Tu objetivo es enumerar ambas superficies de ataque, recolectar tickets de servicio y blobs AS-REP, y craquearlos sin conexión con Hashcat para recuperar las credenciales que desbloquean la bandera. Usando GetUserSPNs.py junto con enumeración dirigida, identificas qué cuentas son vulnerables a cada técnica y recopilas el material de tickets necesario para el análisis offline. La bandera se encuentra dentro del material que recuperas tras un craqueo exitoso.

---

### AD-02: LLMNR/NBT-NS Poisoning y Relay NTLM

**Dificultad:** Medio
**VMs:** 2

Estás posicionado en una red de dominio Windows donde la resolución de nombres por difusión LLMNR y NBT-NS permanece habilitada — una mala configuración que permite a cualquier host del segmento responder a consultas de nombres no resueltos. Usando Responder, envenas las solicitudes de difusión y capturas hashes NTLMv2 de challenge-response de usuarios del dominio que se autentican ante un recurso inexistente. En lugar de craquear el hash capturado, lo canalizas directamente a través de ntlmrelayx para reenviar la credencial a un servicio del dominio, obteniendo ejecución de comandos en una estación de trabajo objetivo y la bandera, sin necesidad de recuperar ninguna contraseña en texto plano.

---

### AD-03: Explotación de Rutas ACL con BloodHound

**Dificultad:** Medio
**VMs:** 2

Has obtenido una cuenta de dominio con privilegios reducidos y necesitas escalar tu acceso hasta Domain Admin. Usando SharpHound para recopilar datos de relaciones de Active Directory y BloodHound para visualizar las rutas de ataque, identificas una cadena de aristas de Access Control List explotables — específicamente un permiso WriteDACL o GenericWrite que posee tu cuenta comprometida sobre un objeto con mayores privilegios. Explotas esta arista para otorgarte los derechos necesarios para una mayor escalada, encadenando los pasos hasta alcanzar Domain Admin y recuperar la bandera.

---

### AD-04: Abuso de Certificados ADCS ESC1

**Dificultad:** Difícil
**VMs:** 2

Tienes una cuenta de dominio con privilegios reducidos y descubres que la organización ha desplegado Active Directory Certificate Services con una plantilla de certificado mal configurada. La plantilla permite la inscripción a usuarios con bajos privilegios, incluye el EKU de Client Authentication y permite que el Subject Alternative Name sea especificado por el solicitante. Usando Certipy, enumeras la plantilla vulnerable, solicitas un certificado falso que suplanta la identidad de una cuenta de Domain Admin, y te autenticas vía PKINIT para obtener un ticket-granting ticket Kerberos de esa cuenta privilegiada — otorgándote acceso de Domain Admin y la bandera.

---

### AD-05: Cadena APT al Estilo Conti  [Multi-paso — 2 banderas]

**Dificultad:** Difícil
**VMs:** 3

Entras a un entorno de dominio Windows de tres máquinas con solo una estación de trabajo atacante y sin credenciales. Desplegando Responder para envenenar las solicitudes de difusión LLMNR en el segmento interno, usas ntlmrelayx para reenviar los hashes capturados por SMB a un servidor miembro del dominio — estableciendo un punto de apoyo que entrega la primera bandera. Con tu posición de pivote asegurada, usas Rubeus para solicitar tickets de servicio de cuentas susceptibles a Kerberoasting, craqueas el ticket offline con Hashcat, y usas las credenciales recuperadas con evil-winrm para moverte lateralmente al controlador de dominio y recuperar la segunda bandera. Cada salto de movimiento lateral usa un protocolo distinto — SMB para el primero, WinRM para el segundo.

---

## Explotación de Protocolos de Red

### NET-01: SMB Relay a través de Recursos Compartidos sin Firma

**Dificultad:** Fácil
**VMs:** 2

Descubres un segmento de red donde la firma SMB no está impuesta en las estaciones de trabajo — una mala configuración común en entornos que nunca han reforzado su configuración predeterminada de Windows. Colocando Responder en modo análisis para evitar el envenenamiento y usando ntlmrelayx para reenviar intentos de autenticación capturados, interceptas la autenticación SMB de un usuario del dominio y la reenvías en tiempo real a un recurso compartido en un host objetivo. La credencial reenviada te otorga acceso de lectura al recurso compartido que contiene la bandera, sin necesidad de craquear ni recuperar ninguna contraseña.

---

### NET-02: DHCPv6 Falso por IPv6 y Relay a LDAP

**Dificultad:** Medio
**VMs:** 2

Observas que el dominio Windows objetivo no tiene gestión IPv6 implementada, dejando a todos los hosts susceptibles a anuncios DHCPv6 falsos. Usando mitm6, levantas un servidor DHCPv6 falso que se asigna a sí mismo como puerta de enlace predeterminada IPv6 y servidor DNS para los hosts del dominio, provocando que envíen solicitudes de autenticación del proxy WPAD a tu máquina atacante. Reenvías estos intentos de autenticación a LDAP mediante ntlmrelayx, aprovechando la credencial reenviada para crear una nueva cuenta de dominio privilegiada — sin ejecución de código, sin malware, sin craqueo de hashes requerido. Usas la cuenta recién creada para autenticarte y recuperar la bandera.

---

### NET-03: Envenenamiento de Caché ARP e Interceptación de Credenciales

**Dificultad:** Fácil
**VMs:** 2

Estás en el mismo segmento de Capa 2 que dos hosts que se comunican y debes interceptar su tráfico. Usando bettercap, envías respuestas ARP gratuitas para envenenar las cachés ARP de ambos objetivos, enrutando su tráfico a través de tu máquina y posicionándote como hombre en el medio. Explotas el proxy HTTPS de bettercap para degradar las conexiones cifradas a HTTP en texto plano, capturando las credenciales transmitidas por los hosts y usándolas para recuperar la bandera.

---

### NET-04: Envenenamiento de Caché DNS

**Dificultad:** Medio
**VMs:** 2

Identificas un resolver DNS desplegado en la red objetivo que está mal configurado para aceptar respuestas sin una adecuada aleatorización del puerto de origen ni validación del ID de consulta. Inyectando respuestas DNS falsificadas que se adelantan al resolver legítimo upstream, corrompres la caché del resolver para que un hostname interno objetivo resuelva a una dirección IP que tú controlas. Cuando un servicio interno legítimo consulta el nombre envenenado y envía su solicitud HTTP a tu máquina, la bandera está embebida en esa solicitud interceptada.

---

## Weaponización de CVEs

### CVE-01: EternalBlue — MS17-010 (CVE-2017-0144)

**Dificultad:** Difícil
**VMs:** 2

Te enfrentas a un objetivo con Windows 7 SP1 que tiene SMBv1 habilitado y ningún parche de seguridad aplicado — el entorno exacto que convirtió a CVE-2017-0144 en una de las vulnerabilidades más destructivas de la historia. En lugar de recurrir a un framework automatizado, redactas un exploit en Python que implementa la configuración de transacción SMBv1, el heap grooming y la puesta en escena del shellcode de DoublePulsar tú mismo, usando el andamiaje de protocolo `mysmb.py` proporcionado como base. Construyes la lista FEA malformada que desencadena el desbordamiento de búfer, introduces tu carga a través del implante DoublePulsar, y obtienes una shell en el objetivo desde la cual recuperas la bandera. Completar este escenario requiere que entiendas el encuadre del protocolo SMBv1 a nivel de paquete — no solo ejecutar una herramienta preconstruida.

---

### CVE-02: Log4Shell — CVE-2021-44228

**Dificultad:** Medio
**VMs:** 2

Identificas una aplicación Java que registra entradas controladas por el atacante usando una versión vulnerable de la biblioteca Apache Log4j. En lugar de usar un kit de exploit preconstruido, redactas una cadena de payload de inyección JNDI y construyes un servidor de cadena de exploit basado en Python que sirve tanto una redirección LDAP como una clase Java maliciosa por HTTP. Cuando la aplicación registra tu entrada elaborada, la biblioteca Log4j inicia una búsqueda JNDI saliente a tu servidor, descarga y ejecuta tu clase, y logras ejecución de comandos del sistema operativo en el objetivo — recuperando la bandera a través de la shell resultante.

---

### CVE-03: Spring4Shell — CVE-2022-22965

**Dificultad:** Medio
**VMs:** 2

Descubres una aplicación web Java construida sobre Spring MVC, desplegada como WAR en un contenedor de servlets, y ejecutándose en Java 9 o posterior — las condiciones previas para CVE-2022-22965. Escribes el exploit: una solicitud HTTP que abusa del mecanismo de vinculación de datos de Spring para recorrer la cadena de propiedades ClassLoader a través de AccessLogValve, manipulando la configuración de registro para escribir un archivo JSP webshell en el directorio de despliegue de la aplicación. Una vez plantado el webshell, lo usas para ejecutar comandos y recuperar la bandera embebida en el servidor objetivo.

---

### CVE-04: PrintNightmare (CVE-2021-1675 / CVE-2021-34527)

**Dificultad:** Medio
**VMs:** 2

Has obtenido una sesión interactiva con privilegios reducidos en un servidor Windows objetivo y necesitas escalar a SYSTEM. El servicio Windows Print Spooler está en ejecución y el objetivo no tiene parches aplicados contra PrintNightmare. Redactas un payload en C o Python que instruye al servicio Windows Print Spooler — que se ejecuta como SYSTEM — para cargar una DLL maliciosa que tú suministras, inyectando tu código en un proceso a nivel SYSTEM. Una vez que tu payload se ejecuta con privilegios elevados, recuperas la bandera desde una ubicación accesible únicamente para SYSTEM. Este escenario ejercita la ruta de escalada de privilegios local, requiriendo un punto de apoyo preexistente en lugar de una posición de red externa.

---

## Seguridad en la Nube y Contenedores

### CC-01: SSRF en IMDS y Robo de Credenciales IAM

**Dificultad:** Fácil
**VMs:** 2

Descubres una aplicación web que realiza solicitudes HTTP del lado del servidor basadas en entradas controladas por el atacante — una superficie SSRF clásica. Elaborando solicitudes que apuntan al endpoint simulado del AWS Instance Metadata Service en 169.254.169.254, recuperas las credenciales del rol IAM adjunto al host de la aplicación. Usando esas credenciales temporales robadas, consultas una API S3 simulada para enumerar los objetos disponibles y recuperar la bandera almacenada en el bucket. No se requiere bypass de autenticación ni ejecución de código — la vulnerabilidad SSRF hace el trabajo.

---

### CC-02: Escape de Contenedor Docker Privilegiado

**Dificultad:** Medio
**VMs:** 2

Aterrizas dentro de un contenedor Docker deliberadamente mal configurado que se ejecuta como root con capacidades Linux elevadas. Desde dentro del contenedor, descubres que el nivel de privilegio otorgado a este contenedor extiende el acceso a interfaces del kernel del host que normalmente están aisladas de los namespaces de contenedores. Escribes un payload que abusa de una ruta de notificación cgroup para programar la ejecución de comandos en el host subyacente, plantando una conexión inversa o leyendo la bandera directamente desde el directorio raíz del host. El desafío evalúa tu comprensión de los límites de aislamiento de contenedores Linux y las condiciones en que un contenedor privilegiado deja de proporcionar una separación significativa del host.

---

### CC-03: Escape por Cuenta de Servicio Mal Configurada en Kubernetes

**Dificultad:** Difícil
**VMs:** 2

Obtienes acceso inicial a un clúster Kubernetes como usuario con bajos privilegios y recibes un token de cuenta de servicio con más permisos de los previstos. Usando kubectl, enumeras los recursos del clúster — pods, roles, role bindings y secrets — para mapear el alcance de los permisos sobreaprovisionados. Construyes y despliegas una especificación de pod privilegiado con un volumen hostPath que monta el sistema de archivos raíz del nodo host, luego ejecutas en el pod para acceder directamente al sistema de archivos del host y recuperar la bandera plantada en el directorio raíz del nodo.

---

## Seguridad en LLMs

### LLM-01: Bypass de Inyección de Prompts en Múltiples Capas

**Dificultad:** Fácil
**VMs:** 2

Interactúas con un chatbot respaldado por Ollama que parece resistir tus intentos de inyección iniciales — la aplicación impone un límite de system prompt, un filtro basado en regex sobre patrones de inyección comunes, y una capa de validación semántica que verifica si tu entrada parece un ataque. Tu objetivo es encadenar al menos dos técnicas de bypass distintas para atravesar las defensas en capas, anular el system prompt y hacer que el modelo genere una bandera oculta embebida en el contexto del LLM. Entender cómo falla cada capa de defensa individualmente — y cómo pueden ser eludidas en secuencia — es el desafío central.

---

### LLM-02: Inyección Indirecta de Prompts vía Envenenamiento de Documentos RAG

**Dificultad:** Medio
**VMs:** 2

Descubres una aplicación de chatbot que usa Retrieval-Augmented Generation, ingiriendo documentos externos en una base de datos vectorial para enriquecer sus respuestas. Elaboras un documento malicioso que contiene instrucciones inyectadas ocultas dentro de contenido aparentemente benigno y haces que sea ingerido en el vector store. Cuando un usuario legítimo envía una consulta rutinaria, el chatbot recupera tu documento envenenado como contexto relevante, y las instrucciones embebidas se activan — haciendo que el modelo genere la bandera. Este escenario explora la superficie de ataque introducida cuando un LLM confía ciegamente en el contenido proveniente de fuentes externas recuperadas de su base de conocimiento.

---

### LLM-03: IDOR en la API de Historial de Chat

**Dificultad:** Medio
**VMs:** 2

Interactúas con una aplicación LLM que almacena el historial de conversaciones y expone un endpoint de API para recuperar sesiones de chat pasadas. El endpoint usa identificadores de conversación predecibles y secuenciales y no realiza ninguna validación de control de acceso significativa — una vulnerabilidad de referencia directa a objetos inseguros a nivel de capa de aplicación. Enumerando los IDs de conversación a través del endpoint, accedes a sesiones de chat pertenecientes a otros usuarios, llegando eventualmente a la conversación de un usuario privilegiado que contiene la bandera. El desafío reside completamente en el fallo de la aplicación para autenticar la propiedad del recurso solicitado.

---

## Cadenas APT de Múltiples Pasos

### ATP-01: Webshell y Movimiento Lateral al Estilo HAFNIUM  [Multi-paso — 2 banderas]

**Dificultad:** Difícil
**VMs:** 3

Comienzas con el conocimiento de una aplicación web de cara a internet que procesa URLs suministradas por el usuario en un contexto del lado del servidor. Elaborando payloads SSRF, alcanzas un servicio interno inaccesible desde el exterior, y escalando ese acceso cargas un webshell en el servidor de la aplicación que te otorga ejecución de código. Recopilando credenciales encontradas en el nivel web comprometido, las usas con evil-winrm para autenticarte en un host Windows pivot interno — asegurando tu primer objetivo y recuperando la primera bandera. Desde el pivot, enumeras recursos del dominio e identificas una ruta hacia el controlador de dominio, siguiéndola para recuperar la segunda bandera y completar la cadena.

---

### ATP-02: Backdoor en Cadena de Suministro al Estilo SolarWinds  [Multi-paso — 2 banderas]

**Dificultad:** Difícil
**VMs:** 3

Se te entrega acceso a un servidor de distribución de actualizaciones de software simulado — la fuente upstream en la que los objetivos downstream confían implícitamente. Modificas un paquete de actualización para incluir un backdoor que se ejecuta silenciosamente cuando el objetivo downstream aplica la actualización, y una vez que la actualización con backdoor se ejecuta en el host downstream recuperas la primera bandera del objetivo comprometido. Con tu punto de apoyo establecido, cambias al segundo objetivo: un objetivo adicional más aislado al que no es posible llegar directamente desde tu posición. Estableces un canal de comando y control encubierto tunelizando las comunicaciones a través de DNS usando dnscat2, eludiendo la segmentación de red, y recuperas la segunda bandera del host aislado.

---

### ATP-03: Cadena de Identidad en la Nube al Estilo LAPSUS$  [Multi-paso — 2 banderas]

**Dificultad:** Difícil
**VMs:** 3

Identificas una vulnerabilidad SSRF en una aplicación alojada en la nube y la usas para consultar el Instance Metadata Service, robando un token de cuenta de servicio de Kubernetes que estaba expuesto inadvertidamente en la respuesta de metadatos. Usando kubectl con el token robado, enumeras los recursos del clúster y descubres un pod privilegiado mal configurado que te otorga acceso al nodo host — escapando del límite del contenedor y asegurando la primera bandera desde el sistema de archivos del nodo. Desde el nodo, consultas directamente el almacén de datos etcd, extrayendo los secrets y credenciales de Kubernetes que contiene. Usando las credenciales recuperadas para autenticarte como administrador en el objetivo interno final, recuperas la segunda bandera y completas la cadena de identidad en la nube.

---

### ATP-04: Cadena Living-Off-the-Land al Estilo Volt Typhoon  [Multi-paso — 2 banderas]

**Dificultad:** Difícil
**VMs:** 3

Operas bajo una restricción de sin-malware — sin payloads compilados, sin shellcode, sin implantes persistentes. Usando mitm6 para desplegar un servidor DHCPv6 falso y reenviando los intentos de autenticación resultantes a LDAP mediante ntlmrelayx, creas una nueva cuenta de dominio privilegiada sin tocar el sistema de archivos de ningún host objetivo. Con la nueva cuenta, usas evil-winrm para autenticarte en un servidor miembro del dominio y recuperar la primera bandera. Desde el pivot, enumeras SPNs de cuentas de servicio con Kerberoasting, craqueas el hash del ticket recuperado offline, y usas la credencial resultante con SMBExec o DCOM para autenticarte en el controlador de dominio y recuperar la bandera final — toda la cadena ejecutada sin soltar un solo archivo malicioso.
