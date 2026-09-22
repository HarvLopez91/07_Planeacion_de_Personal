# Plan de gobierno de Outputs, skills, tools y cierre de implementaciones

## 1. Propósito

Este documento define el procedimiento operativo de gobierno para ejecutar y
cerrar iniciativas del Proyecto 07 sin mezclar frentes, perder trabajo local ni
acumular ruido de Power BI Desktop.

La regla obligatoria para agentes está en `AGENTS.md`. El gate resumido que
determina si una iniciativa puede pasar a `Finalizada` está en
`Specs/00_roadmap_y_backlog.md`.

## 2. Roles de los espacios de trabajo

- `.wt/` es el espacio temporal de desarrollo aislado. Cada iniciativa debe
  usar una rama y un worktree identificables.
- El checkout principal de `main` es el checkpoint oficial de consolidación,
  validación, refresh y publicación.
- `PBIP/Proyecto7.pbip` es el PBIP oficial del Proyecto 07.
- El checkpoint principal no debe utilizarse como espacio habitual de
  desarrollo funcional.
- `Outputs/` conserva evidencia temporal o diagnóstica según sus reglas de
  gobierno; no reemplaza la documentación oficial en `Docs/` o `Specs/`.
- Las skills y tools apoyan el proceso, pero no amplían autorizaciones ni
  sustituyen los gates humanos, funcionales o visuales.

## 3. Flujo oficial de una implementación

El flujo obligatorio es:

`main` limpio → crear worktree → implementar → validar → commit selectivo →
push → PR → merge → actualizar checkpoint principal → validar PBIP oficial →
refresh/publicación cuando corresponda → revisar ruido de Power BI → auditar
worktree → retirar worktree → documentar estado final → iniciar siguiente
frente.

### 3.1 Preparación

1. Actualizar referencias remotas y verificar `origin/main`.
2. Confirmar el estado del checkout principal y preservar cualquier trabajo
   existente.
3. Crear la rama y el worktree dentro de `.wt/`, salvo una excepción temporal
   expresamente autorizada.
4. Registrar iniciativa, alcance, dependencias y criterios de aceptación.

### 3.2 Desarrollo y validación

1. Implementar solo el alcance autorizado.
2. Ejecutar las pruebas técnicas pertinentes.
3. Obtener validación funcional y, para cambios de reporte, validación visual.
4. Revisar `git status`, el diff completo y `git diff --check`.
5. Stagear rutas explícitas; nunca usar `git add .` ni `git add -A`.
6. Confirmar qué archivos quedan incluidos y cuáles se excluyen.

### 3.3 Integración

1. Crear commit y push solo con autorización.
2. Abrir el PR contra `main` y revisar archivos, diff, validaciones y
   conflictos.
3. Fusionar únicamente después de cumplir los gates del frente.
4. Confirmar que `origin/main` contiene el commit o merge esperado.
5. Actualizar el checkpoint principal de `main` sin perder trabajo local
   previo. Si el checkpoint no puede actualizarse de forma segura, la
   iniciativa permanece `PENDIENTE DE CIERRE`.

### 3.4 Validación del checkpoint oficial

1. Abrir `PBIP/Proyecto7.pbip` desde el checkpoint principal actualizado.
2. Validar carga, medidas, filtros, navegación y presentación según el alcance.
3. Ejecutar refresh y publicación cuando correspondan y estén autorizados.
4. Confirmar que la versión publicada corresponde al commit integrado en
   `main`.

### 3.5 Control del ruido de Power BI Desktop

Después de cualquier apertura con guardado, refresh o publicación:

1. Ejecutar inmediatamente `git status`.
2. Inventariar rutas modificadas, eliminadas y untracked.
3. Separar cambios funcionales de reserialización, selecciones persistidas,
   metadatos, orden de propiedades, cambios de esquema, EOL y otros cambios
   automáticos.
4. Comparar contra `origin/main` y contra el alcance aprobado.
5. Documentar la decisión para cada cambio relevante: versionar, mantener como
   pendiente o descartar de forma autorizada.
6. No limpiar ni revertir cambios ambiguos. Si hay trabajo sin clasificar, el
   cierre se detiene.

## 4. Auditoría y retiro del worktree

Antes de retirar el worktree, verificar como mínimo:

```bash
git worktree list
git -C <ruta> branch --show-current
git -C <ruta> status --short --branch
git -C <ruta> log --oneline origin/main..HEAD
git -C <ruta> ls-files --others --exclude-standard
```

El retiro solo está permitido cuando:

- el working tree está limpio;
- no existe staging;
- no hay archivos untracked relevantes;
- no existen commits pendientes de integrar;
- la rama está contenida correctamente en `main`;
- `origin/main` contiene el trabajo;
- el checkpoint principal está actualizado e íntegro;
- no queda evidencia única ni trabajo pendiente dentro del worktree.

Si cualquiera de estos controles falla, **detenerse y conservar el worktree**.

Cuando todos los controles pasan:

```bash
git worktree remove <ruta>
```

No usar `--force` sin autorización explícita. No borrar la carpeta manualmente
desde Explorer, `rm` o `rmdir`. `git worktree prune` solo puede considerarse
después de un retiro correcto, si quedaron metadatos obsoletos y tras auditar
que no afectará otros worktrees. Las ramas fusionadas se reportan como
candidatas a eliminación, pero no se eliminan sin autorización explícita.

## 5. Registro de cierre

Antes de iniciar otro frente debe quedar evidencia de:

- validaciones funcional y visual;
- alcance exacto versionado y archivos excluidos;
- commit, PR y merge;
- SHA final de `origin/main` y sincronización de `main`;
- validación del PBIP oficial;
- resultado del refresh/publicación, si aplicó;
- clasificación del ruido generado por Power BI Desktop;
- auditoría y resultado del retiro del worktree;
- pendientes, riesgos y decisiones humanas restantes.

Mientras falte cualquier evidencia, la iniciativa conserva el estado
`PENDIENTE DE CIERRE`.
