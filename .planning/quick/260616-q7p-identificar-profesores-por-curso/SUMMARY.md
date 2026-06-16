---
quick_id: 260616-q7p
slug: identificar-profesores-por-curso
status: complete
completed: 2026-06-16
---

# Summary

Cruzado horario 2026-1 con lista de cursos de interés para identificar profesores a contactar.

## Qué se hizo
- Leído `horario2026.xlsx` (797 filas, columnas: COD, CURSO, DOCENTE)
- Matched 21 de 23 cursos target con el horario (CBH03 y CBN21 no están en 2026-1)
- Creado `docs/PROFESORES-CONTACTO.md` con:
  - Tabla curso → profesor(es)
  - Lista deduplicada de 19 profesores únicos
  - Tabla de prioridad de contacto con CTFs relevantes por profesor

## Hallazgos
- CBH03 (Auditoría) y CBN21 (Forense) no aparecen en horario 2026-1
- QUILLAS FIESTAS dicta 3 cursos de la lista (CBD01, CBN02, BMA09)
- SANTILLAN RAMOS cubre tanto SO II como Redes Industriales I
- COMINA JARA cubre Fundamentos de Ciberseguridad e IA I
