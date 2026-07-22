---
name: outputs-governance
description: Audit and classify Outputs evidence with the local indexer. Use when the user asks to audit, index, consolidate, or clean Outputs without deleting files. Do not use for PBIP edits, commit preparation, or destructive cleanup.
---

# outputs-governance

## Proposito

Gobernar `Outputs/` en modo solo lectura con `Tools/governance/outputs_indexer.py` como evidencia principal.

## Usar cuando

- El usuario pida auditar, indexar o consolidar `Outputs/`.
- El usuario quiera preparar un lote de limpieza sin ejecutar borrados.
- El usuario necesite un resumen versionable de evidencia temporal.

## No usar cuando

- La tarea principal sea modificar PBIP, TMDL o DAX.
- La tarea principal sea preparar un commit.
- El usuario ya autorizo borrar o mover archivos; eso debe resolverse en una accion separada.

## Flujo

1. Ejecutar `python Tools/governance/outputs_indexer.py . --pretty`.
2. Usar el JSON como evidencia primaria.
3. Solo si hay candidatos de limpieza, verificar referencias cruzadas con `rg -n "Outputs/|Outputs\\" -g "!Outputs/**" -g "!Data/**" .`.
4. Si el usuario pide un resumen versionable, usar `Docs/README.md` como referencia de gobierno y proponer `Docs/outputs_index/` solo con aprobacion explicita.
5. No modificar `Outputs/` durante la auditoria.

## Restricciones

- No borrar, mover ni renombrar archivos sin aprobacion explicita.
- No modificar PBIP, Docs, Specs ni Tools durante esta skill.
- No hacer staging, commit ni push.
- No duplicar contenido completo de `Outputs/` en la respuesta.

## Resultado esperado

- Resumen ejecutivo.
- Conteos por extension y clasificacion.
- Evidencias criticas a mantener.
- Candidatos a consolidar o revisar.
- Candidatos a eliminar sin ejecutar, con riesgo y motivo.
- Confirmacion de que `Outputs/` no fue modificado.
