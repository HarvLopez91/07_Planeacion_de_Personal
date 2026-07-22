---
name: pbi-navigation-audit
description: Audit PBIP report pages, navigation, and structural report metadata with the local navigation tool. Use when the user asks to review pages, bookmarks, navigation flow, report structure, or broken report interactions. Do not use for semantic model audits, DAX reviews, or commit preparation.
---

# pbi-navigation-audit

## Proposito

Auditar paginas, navegacion y metadatos estructurales del reporte con `Tools/pbip/audit_navigation.py` antes de revisar visuales o proponer cambios de experiencia.

## Usar cuando

- El usuario pida revisar paginas, bookmarks o navegacion.
- Se necesite detectar rutas rotas, paginas huerfanas o inconsistencias de estructura del reporte.
- Se requiera contexto previo para cambios de visuales o experiencia de uso.

## No usar cuando

- La tarea principal sea auditar el modelo semantico.
- La tarea principal sea revisar medidas DAX.
- La tarea principal sea preparar commits.

## Flujo

1. Ejecutar `python Tools/pbip/audit_navigation.py . --pretty`.
2. Usar el JSON como evidencia principal.
3. Leer `PBIP/Proyecto.Report/definition/pages/pages.json` o artefactos puntuales solo si el JSON deja una alerta ambigua.
4. Referenciar `Docs/BI_GUIDELINES.md` si el usuario necesita contraste contra convenciones del reporte.
5. No modificar archivos durante la auditoria.

## Restricciones

- No modificar PBIP, bookmarks ni visuales.
- No hacer staging, commit ni push.
- No interpretar navegacion como valida sin evidencia del JSON o del artefacto puntual.

## Resultado esperado

- Conteo de paginas y elementos de navegacion auditados.
- Hallazgos de estructura, bookmarks o flujo.
- Riesgos confirmados y puntos pendientes de validacion manual.
- Siguiente paso recomendado.
