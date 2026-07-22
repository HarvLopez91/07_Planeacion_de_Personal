---
name: pbi-dax-measures-audit
description: Audit DAX measures with the local measures tool. Use when the user asks to review measures, naming, measure table placement, or DAX risks before editing formulas. Do not use for relationship audits, report navigation, or commit preparation.
---

# pbi-dax-measures-audit

## Proposito

Auditar medidas DAX con `Tools/pbip/audit_dax_measures.py` antes de proponer cambios de formulas, naming o ubicacion de medidas.

## Usar cuando

- El usuario pida revisar medidas DAX.
- Se necesite detectar naming inconsistente, medidas huerfanas o ubicacion incorrecta.
- Se requiera contexto previo antes de editar formulas.

## No usar cuando

- La tarea principal sea auditar relaciones o tablas.
- La tarea principal sea revisar navegacion del reporte.
- La tarea principal sea preparar commits.

## Flujo

1. Ejecutar `python Tools/pbip/audit_dax_measures.py . --pretty`.
2. Usar el JSON como evidencia principal.
3. Leer medidas concretas solo si el JSON reporta alertas que requieran confirmacion puntual.
4. Referenciar `Docs/METRICS_CATALOG.md` solo cuando el usuario necesite contraste funcional.
5. No modificar DAX ni TMDL durante la auditoria.

## Restricciones

- No modificar PBIP.
- No hacer staging, commit ni push.
- No inventar criterios de negocio ausentes en la evidencia.

## Resultado esperado

- Conteo de medidas auditadas.
- Alertas altas, medias y bajas.
- Medidas fuera de la tabla esperada, si aplica.
- Riesgos concretos de naming o mantenibilidad.
- Siguiente paso recomendado.
