---
name: pbi-aprendizaje-inventario
description: Inspect the local PBIP project structure with the structure tool. Use when the user asks for a repo map, PBIP inventory, report structure overview, or quick diagnostics. Do not use for semantic model audits, DAX reviews, or commit preparation.
---

# pbi-aprendizaje-inventario

## Proposito

Levantar un inventario rapido y repetible del proyecto PBIP actual usando `Tools/pbip/list_pbip_structure.py` antes de explorar manualmente carpetas, paginas o visuales.

## Usar cuando

- El usuario pida inventario del PBIP o mapa del repositorio.
- El usuario necesite una revision inicial o un diagnostico rapido.
- Se requiera contexto previo para otra auditoria especializada.

## No usar cuando

- La tarea principal sea auditar el modelo semantico.
- La tarea principal sea revisar medidas DAX.
- La tarea principal sea preparar commits.

## Flujo

1. Ejecutar `python Tools/pbip/list_pbip_structure.py . --pretty`.
2. Usar el JSON como evidencia inicial.
3. Revisar primero `archivos_pbip`, `rutas_clave`, `paginas_reporte`, `documentacion.archivos`, `outputs.archivos` y `errores`.
4. Solo si el JSON muestra inconsistencias, hacer lecturas puntuales adicionales.
5. No modificar archivos durante el inventario.

## Restricciones

- No modificar PBIP, Docs, Outputs ni Specs.
- No hacer staging, commit ni push.
- No releer carpetas completas si el JSON ya responde la pregunta.

## Resultado esperado

- Estado general del inventario.
- Conteos de PBIP, paginas y visuales.
- Rutas clave presentes o faltantes.
- Hallazgos concretos y riesgos confirmados.
- Siguiente skill recomendada si se requiere auditoria mas profunda.
