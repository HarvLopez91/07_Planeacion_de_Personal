---
name: pbi-semantic-model-audit
description: Audit the PBIP semantic model with the local TMDL audit tool. Use when the user asks to review tables, relationships, model risks, or pre-change semantic context. Do not use for report navigation audits, commit preparation, or direct model edits.
---

# pbi-semantic-model-audit

## Proposito

Auditar el modelo semantico PBIP/TMDL con `Tools/pbip/audit_semantic_model.py` antes de revisar o proponer cambios de tablas, relaciones o medidas.

## Usar cuando

- El usuario pida auditar tablas, relaciones o alertas del modelo.
- Se necesite contexto tecnico antes de cambios DAX o TMDL.
- Se quiera confirmar riesgos de tablas desconectadas, naming tecnico o relaciones ambiguas.

## No usar cuando

- La tarea principal sea revisar navegacion del reporte.
- La tarea principal sea preparar commits.
- El usuario ya autorizo una edicion concreta y no se necesita auditoria previa.

## Flujo

1. Ejecutar `python Tools/pbip/audit_semantic_model.py . --pretty`.
2. Usar el JSON como evidencia principal.
3. Solo si el JSON deja una alerta ambigua, leer archivos puntuales en `PBIP/Proyecto.SemanticModel/definition/`.
4. Si la solicitud es solo sobre medidas, preferir la skill `pbi-dax-measures-audit`.
5. No modificar archivos durante la auditoria.

## Restricciones

- No modificar PBIP, TMDL ni DAX.
- No imprimir datos sensibles.
- No hacer staging, commit ni push.

## Resultado esperado

- Estado general del modelo y nivel de riesgo.
- Conteos de tablas, medidas y relaciones.
- Alertas altas, medias, bajas y pendientes por validar.
- Riesgos concretos con evidencia puntual.
- Siguiente auditoria recomendada.
