---
name: pbi-commit-prep
description: Prepare a controlled commit review for this PBIP repository using git evidence and the local governance rules. Use when the user asks to review changes, define commit scope, or prepare explicit staging. Do not use for broad repo cleanup or unrelated PBIP edits.
---

# pbi-commit-prep

## Proposito

Preparar commits controlados usando `Tools/governance/prepare_commit_review.py` como evidencia principal y `Docs/GIT_GOVERNANCE.md` como regla canonica.

## Usar cuando

- El usuario pida revisar cambios antes de versionar.
- El usuario quiera separar alcance de commit.
- El usuario autorice staging o commit y se necesite validar que no entren archivos ajenos.

## No usar cuando

- La tarea principal sea diagnosticar el modelo o el reporte.
- El usuario quiera limpiar el working tree completo.
- El alcance aun no este definido.

## Flujo

1. Ejecutar `git status -sb`.
2. Ejecutar `python Tools/governance/prepare_commit_review.py . --pretty`.
3. Revisar `Docs/GIT_GOVERNANCE.md` y, si hay cambios PBIP, `Docs/PROJECT_STATUS.md`.
4. Separar archivos incluidos y excluidos segun el alcance aprobado.
5. Solo si el usuario autoriza staging, usar rutas explicitas con `git add -- ruta`.
6. No hacer commit ni push sin aprobacion explicita.

## Restricciones

- No usar `git add .` ni `git add -A`.
- No incluir `Outputs/` salvo autorizacion explicita.
- No mezclar PBIP, Docs, Specs, Tools o skills en un mismo commit sin aprobacion explicita.
- No modificar archivos durante la preparacion del commit.

## Resultado esperado

- Archivos modificados.
- Archivos incluidos y excluidos.
- Riesgos de mezcla de alcance.
- Documentacion canonica a revisar, si aplica.
- Mensaje de commit propuesto.
- Comandos de staging explicito.
- Confirmacion de que no se hizo staging, commit ni push sin autorizacion.
