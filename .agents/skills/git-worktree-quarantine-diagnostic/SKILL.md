---
name: git-worktree-quarantine-diagnostic
description: Diagnostica en modo solo lectura worktrees de Git en cuarentena (HEAD 000...0), tipicamente causados por fallos de 'git worktree remove' en carpetas sincronizadas por OneDrive. Usar cuando 'git worktree remove' falle con Permission denied, o para auditar periodicamente la salud de los worktrees. No usar para eliminar, reparar o limpiar worktrees.
---

# git-worktree-quarantine-diagnostic

## Proposito

Ejecutar `Tools/governance/audit_worktree_quarantine.py` para diagnosticar de forma segura los worktrees que quedaron en estado de cuarentena (`HEAD 0000000000000000000000000000000000000000` en `git worktree list --porcelain`), sin ejecutar ninguna operacion de eliminacion o reparacion. Ver `Specs/0021_diagnostico_worktrees_cuarentena_onedrive.md` para el contexto completo.

## Usar cuando

- `git worktree remove <ruta>` (sin `--force`) falla con `Permission denied`.
- `git worktree list` muestra una o mas entradas con `HEAD` en todo-ceros.
- Se necesita evidencia objetiva (commit incorporado en `main`, contenido preservado, proceso bloqueante) antes de decidir que hacer con un worktree en ese estado.
- Se quiere auditar periodicamente la salud general de los worktrees del repositorio.

## No usar cuando

- Se busque eliminar, reparar o limpiar un worktree — este skill es exclusivamente diagnostico.
- El worktree tiene un `HEAD` valido (no esta en cuarentena); en ese caso, usar el flujo normal de cierre de frente (`git worktree remove` tras confirmar working tree limpio).

## Flujo

1. Ejecutar `python Tools/governance/audit_worktree_quarantine.py --all` para ver todos los worktrees en cuarentena, o `--worktree <ruta>` para uno especifico.
2. Agregar `--json` si se necesita evidencia estructurada para un reporte o para otro proceso.
3. Interpretar la clasificacion de cada worktree (ver tabla abajo).
4. Si la clasificacion es `NEEDS_REVIEW_UNPRESERVED_WORK` o `CRITICAL_BRANCH_REF_MISSING`, detenerse y reportar al usuario — no continuar con ninguna accion sobre ese worktree.
5. Si la clasificacion es `SAFE_TO_INVESTIGATE_MANUAL_REMOVAL`, reportarlo como tal al usuario. **No eliminar automaticamente.** La decision de investigar una remocion manual (y la remocion misma, si se autoriza) es un paso humano separado y posterior, fuera del alcance de este skill.

## Clasificaciones y su significado

| Clasificacion | Que significa | Que hacer |
|---|---|---|
| `HEALTHY` | El worktree no esta en cuarentena. | Nada; usar el flujo normal de cierre de frente. |
| `SAFE_TO_INVESTIGATE_MANUAL_REMOVAL` | El commit de la rama ya es ancestro de `origin/main` y no se detecto contenido en disco sin preservar. | Reportar al usuario; **no autoriza eliminacion automatica**, solo indica que una remocion manual puede investigarse despues. |
| `NEEDS_REVIEW_UNPRESERVED_WORK` | Hay archivos en disco (nuevos, modificados o distintos) que no corresponden al ultimo commit conocido de la rama. | Detenerse. Requiere revision humana antes de cualquier accion. |
| `NEEDS_REVIEW_COMMIT_NOT_IN_MAIN` | La rama resolvio pero su commit no esta en `origin/main`. | Detenerse. El commit no se pierde (la rama persiste), pero el frente no esta cerrado. |
| `CRITICAL_BRANCH_REF_MISSING` | Ni la referencia de la rama pudo resolverse. | Detenerse. Corrupcion severa, fuera del alcance de esta herramienta; requiere intervencion manual de Git. |

## Restricciones

- Ningun agente puede ejecutar, a partir de un resultado de este diagnostico, ninguno de los siguientes comandos: `git worktree remove --force`, `git worktree prune`, `git worktree repair`, `Remove-Item`, `rmdir`, `os.remove`, `os.unlink`, `shutil.rmtree`, ni escribir o eliminar nada dentro de `.git/worktrees`.
- Ningun agente puede eliminar automaticamente un worktree marcado `SAFE_TO_INVESTIGATE_MANUAL_REMOVAL` sin autorizacion explicita del usuario para ese worktree en particular.
- El script no modifica refs, indice, ramas ni working trees; si se observa que lo hizo, es un defecto del script, no un comportamiento esperado — detenerse y reportarlo.
- El detector de proceso bloqueante es best-effort (Restart Manager de Windows, con heuristica de procesos conocidos como respaldo); un resultado vacio no garantiza que la ruta este libre de bloqueo.

## Resultado esperado

- Lista de worktrees diagnosticados con su clasificacion.
- Evidencia por worktree: metadata administrativa presente/faltante, commit de la rama, si es ancestro de `origin/main`, si la rama remota existe, resumen de diferencias de archivo, resultado del detector de locks.
- Ninguna accion de eliminacion, reparacion o limpieza ejecutada.
- Recomendacion clara de si el caso requiere decision humana o puede investigarse una remocion manual mas adelante.
