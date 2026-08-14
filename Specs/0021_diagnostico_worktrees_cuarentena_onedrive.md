# Diagnóstico seguro de worktrees en cuarentena por OneDrive (GOV-006)

Fecha: 2026-08-14

Estado: En validación. Herramienta implementada y probada contra el corpus conocido; pendiente de uso repetido en producción antes de considerarse cerrada.

Iniciativa independiente de `Specs/0018_saneamiento_medidas_duplicadas_gov005.md` (GOV-005, cerrada) y de cualquier frente PBIP en curso (Demográfico, Gasto Laboral, Retiros, Kactus). No modifica modelo semántico, DAX, Power Query, bookmarks ni visuales.

## 1. Problema observado

`git worktree remove <ruta>` (sin `--force`) falla repetidamente con `Permission denied` cuando la ruta del worktree vive dentro de una carpeta sincronizada por OneDrive. La eliminación queda a medias: `git worktree list --porcelain` reporta `HEAD 0000000000000000000000000000000000000000` para esa entrada, y `.git/worktrees/<nombre>/` pierde archivos de metadata (típicamente `commondir`), dejando el worktree en un estado que no es ni "activo" ni "eliminado".

Este patrón se observó de forma independiente **5 veces** en la sesión que originó esta iniciativa, cada vez exigiendo el mismo procedimiento manual de auditoría antes de decidir qué hacer. Ejecutar `git worktree repair` no restaura `commondir` de forma confiable (confirmado empíricamente en dos intentos separados). El objetivo de GOV-006 es sistematizar ese procedimiento manual en una herramienta reutilizable, **sin automatizar la eliminación**.

## 2. Alcance

**Exclusivamente diagnóstico y de solo lectura.** Esta iniciativa:

- Identifica worktrees en el estado corrupto descrito.
- Determina si el commit de la rama asociada ya está incorporado en `origin/main`.
- Determina si existe contenido en disco que no esté preservado en ningún commit.
- Intenta identificar, de forma best-effort, qué proceso de Windows mantiene bloqueada la ruta.

**No incluye:** eliminación de worktrees (automática ni asistida), reparación de metadata Git, ni ninguna escritura sobre el repositorio principal o sus worktrees. La decisión y ejecución de una eliminación sigue siendo, en todos los casos, un paso manual y humano, posterior y separado de esta herramienta.

## 3. Corpus de prueba conocido

Cinco worktrees en cuarentena, confirmados manualmente durante la sesión que originó esta iniciativa, sirven como corpus de validación (la respuesta correcta para varios de ellos ya se conocía por auditoría manual antes de escribir el script):

| Worktree | Rama | Estado esperado (conocido por auditoría manual previa) |
|---|---|---|
| `.wt/data-012-postmerge-visuales-generacion` | `fix/data-012-postmerge-visuales-generacion` | Commit único útil ya rescatado a `main` en otro commit; cuarentena declarada permanente por el usuario |
| `.wt/docs-contratos-kactus-data` | `docs/contratos-kactus-data` | Sin verificar en profundidad; corpus de prueba general |
| `.wt/demografico-estado-civil-null-origen` | `fix/demografico-estado-civil-null-origen` | Corrupción independiente, posiblemente por intento fallido de otro agente |
| `.wt/demografico-promedio-tabla-cco` | `feat/demografico-promedio-tabla-cco` | Commit `4ecc238` confirmado como ancestro de `origin/main` (PR #14 fusionado); sin trabajo pendiente |
| `.wt/demografico-eliminar-qa` | `fix/demografico-eliminar-pagina-qa` | Commit `164edb67` confirmado como ancestro de `origin/main` (PR #15 fusionado); sin trabajo pendiente |

Los dos últimos casos tienen una respuesta ya verificada a mano (`SAFE_TO_INVESTIGATE_MANUAL_REMOVAL` esperado, sin diferencias de archivo), lo que permite validar el script contra un resultado conocido sin depender solo de inspección visual de su salida.

## 4. Arquitectura: script + skill

- **Script** (`Tools/governance/audit_worktree_quarantine.py`): lógica mecánica y determinística — enumerar, comparar, verificar ancestro, detectar locks. Python + biblioteca estándar, siguiendo el único patrón de gobierno ya presente en `origin/main` (`Tools/governance/skills_lint.py`: `argparse`, `pathlib.Path`, salida estructurada). Reutilizable por cualquier agente o directamente por el usuario desde terminal.
- **Skill** (`.agents/skills/git-worktree-quarantine-diagnostic/SKILL.md`): procedimiento y guardrails. Fija cuándo invocar el script, cómo interpretar cada clasificación, y — sobre todo — la lista explícita de operaciones prohibidas, para que ningún agente necesite re-derivar el procedimiento seguro bajo presión (como ocurrió 5 veces antes de esta iniciativa).

## 5. Clasificación de resultados

| Clasificación | Significado |
|---|---|
| `HEALTHY` | El worktree no está en el estado corrupto (`HEAD` distinto de todo-ceros); no requiere diagnóstico adicional. |
| `SAFE_TO_INVESTIGATE_MANUAL_REMOVAL` | El commit de la rama es ancestro de `origin/main` y no se detectó contenido en disco que difiera del commit. **No es una autorización de eliminación automática** — solo indica que una investigación manual de remoción es razonable. |
| `NEEDS_REVIEW_UNPRESERVED_WORK` | Se detectó contenido en disco (archivos nuevos, modificados o con diferencias) que no corresponde al último commit conocido de la rama. Requiere revisión humana antes de cualquier acción. |
| `NEEDS_REVIEW_COMMIT_NOT_IN_MAIN` | La rama resolvió correctamente pero su commit no es ancestro de `origin/main`. El commit no se pierde al eliminar el worktree (la rama persiste), pero el frente no está cerrado. |
| `CRITICAL_BRANCH_REF_MISSING` | Ni siquiera la referencia de la rama pudo resolverse desde el repositorio sano. Corrupción más severa; fuera del alcance de esta herramienta, requiere intervención manual de Git. |

## 6. Procedimiento de validación

1. Ejecutar el script contra los 5 worktrees del corpus conocido (sección 3) y comparar el veredicto contra la evidencia ya verificada manualmente para los dos últimos casos.
2. Ejecutar el script contra un repositorio/worktree sano (sin la corrupción) para confirmar que clasifica `HEALTHY` y no produce falsos positivos.
3. Confirmar `--help` funcional, salida JSON válida (`--json`), y que no queden temporales residuales tras cada ejecución (todo dentro de `%TEMP%`, limpiado al finalizar cada corrida).
4. Búsqueda automática en el propio código fuente para confirmar ausencia de las operaciones prohibidas (sección 7).
5. `git diff --check` sobre los archivos del frente antes de cualquier commit.

## 7. Guardrails obligatorios

El script **no puede ejecutar ni contener lógica de remoción**. Prohibido en todo el código: `git worktree remove --force`, `git worktree prune`, `git worktree repair`, `Remove-Item`, `rmdir`, `os.remove`, `os.unlink`, `shutil.rmtree`, y cualquier escritura o eliminación dentro de `.git/worktrees`. Tampoco puede modificar refs, índices, ramas ni working trees del repositorio principal o de ningún worktree. Las únicas escrituras permitidas son archivos temporales/evidencia dentro de `%TEMP%`, que el propio script debe limpiar al finalizar.

## 8. Criterio de aceptación

- El script ejecuta contra los 5 worktrees del corpus y produce una clasificación por cada uno, con evidencia (commit/ref, ancestro de `origin/main`, diferencias de archivo, resultado del detector de locks).
- El script ejecuta contra al menos un caso sano sin falsos positivos.
- `--help`, modo texto y modo `--json` funcionan sin error.
- No quedan temporales residuales tras la ejecución.
- Búsqueda de las operaciones prohibidas en el código fuente no encuentra ninguna.
- La skill documenta el procedimiento completo, incluida la advertencia explícita de que ningún agente puede eliminar automáticamente un worktree marcado `SAFE_TO_INVESTIGATE_MANUAL_REMOVAL` — esa clasificación **no autoriza eliminación automática**, solo indica que no se detectó trabajo no preservado y que una remoción manual puede investigarse después.
- El roadmap registra `GOV-006` sin alterar el registro ya cerrado de `GOV-005`.

Mientras no se acumule evidencia de uso repetido en producción (varias corridas reales posteriores a esta implementación), el estado permanece `En validación`, no `Finalizada`.
