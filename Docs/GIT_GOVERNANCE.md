# Gobierno Git

Fecha de referencia: `2026-07-17`.

## Principio General

Este repositorio se trabaja con control de cambios estricto porque Power BI Desktop puede modificar muchos archivos PBIP no relacionados con el objetivo de una tarea. Todo cambio debe separarse por alcance y validarse antes de staging.

## Reglas Obligatorias

- No usar `git add .`.
- No usar `git add -A`.
- No hacer staging sin rutas explícitas.
- No incluir cambios fuera del alcance autorizado.
- No hacer commit sin validar identidad Git.
- No hacer push sin autorización explícita.
- No usar `push --force`.
- No descartar, eliminar, sobrescribir ni revertir cambios existentes del usuario.
- No usar `reset`, `restore` (cuando pueda descartar cambios), `checkout` (cuando pueda reemplazar archivos o ramas), `clean`, `stash`, `rebase`, `cherry-pick`, `commit --amend` ni `push --force` salvo aprobación específica.
- No limpiar el working tree para “ordenar” cambios PBIP acumulados.
- No mezclar cambios funcionalmente diferentes o no relacionados en un mismo commit salvo aprobación explícita.
- No versionar datos, fuentes operativas, respaldos, archivos temporales, cachés, exportaciones, archivos derivados, binarios o archivos pesados que no sean necesarios para el funcionamiento, reproducción o documentación oficial del repositorio. Cualquier excepción requiere autorización expresa y específica.
- No omitir ni forzar exclusiones definidas en `.gitignore` sin autorización explícita y específica del usuario.

Se permite incluir en un mismo commit una implementación y su documentación directamente asociada cuando constituyan un único bloque lógico aprobado.

## Comandos Git

### Permitidos para inspección

- `git status`
- `git diff`
- `git log`
- `git show`
- `git branch`
- `git ls-files`
- `git remote -v`

### No ejecutar sin autorización específica

- `git reset`
- `git restore` cuando pueda descartar cambios
- `git checkout` cuando pueda reemplazar archivos o ramas
- `git clean`
- `git stash`
- `git rebase`
- `git cherry-pick`
- `git commit --amend`
- `git push --force`

## Preflight Recomendado

```powershell
git status -sb
git status --short
git diff --cached --name-status
git log --oneline origin/main..HEAD
git log --oneline HEAD..origin/main
git branch --show-current
git diff --check
```

## Identidad Esperada

```powershell
git config --local --get user.name
git config --local --get user.email
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
```

Identidad esperada:

```text
EdwinClavijoChallenger <edwin.clavijo@challenger.co>
```

## Criterios de Staging

### Permitido

- Rutas explícitas aprobadas por el prompt.
- Archivos pertenecientes al mismo bloque lógico.
- Implementación y documentación directamente asociada cuando formen un único bloque lógico aprobado.
- Commits separados para modelo, visuales, documentación, Specs o herramientas.

### Prohibido

- `Outputs/` salvo aprobación explícita.
- `Data/`.
- Archivos temporales, cachés, exportaciones y binarios no necesarios para Git.
- Ruido de Power BI Desktop no relacionado.
- `diagramLayout.json`, `pages.json`, bookmarks o cultures sin justificación explícita.
- Archivos PBIP de otras páginas o tablas fuera de alcance.
- Uso de `git add .` o `git add -A`.

## Validación de Staging

Antes de commit:

```powershell
git diff --cached --name-status
git diff --cached --stat
git diff --cached --check
```

Si aparece un archivo fuera de alcance, detenerse. No hacer commit.

## Commits

Usar Conventional Commits en español:

```text
tipo(alcance): descripción breve
```

La descripción debe redactarse en imperativo y cada commit debe representar
un único cambio lógico. No mezclar requerimientos, páginas, medidas,
documentación, Specs, Outputs o herramientas que no formen parte del mismo
bloque aprobado.

Ejemplos:

- `docs: actualiza documentación y gobierno del proyecto PBIP`
- `fix(data): migra fuentes a SharePoint corporativo`
- `feat(visuals): agrega slicer de dependencia en demografico promedio`

No incluir coautores si el usuario no lo solicita.

### Cuerpo detallado

El cuerpo del commit debe permitir auditar el cambio sin depender de la
conversación que lo originó. Debe incluir:

```text
Objetivo:
- Resultado que se buscaba.

Cambios realizados:
- Implementación o documentación incorporada.

Motivo:
- Problema funcional, técnico o de gobierno resuelto.

Archivos incluidos:
- Rutas o componentes versionados.

Validaciones:
- Pruebas funcionales, estáticas, visuales y Git ejecutadas.

Exclusiones:
- Archivos, ruido PBIP y cambios locales dejados fuera.

Pendientes o riesgos:
- Validaciones no ejecutadas, hallazgos diferidos o riesgos residuales.
```

No declarar como ejecutada una validación que no tenga evidencia.

### Staging preexistente y cambios ajenos

- Revisar el índice antes de agregar archivos.
- No retirar, reescribir ni confirmar staging ajeno.
- Si existe staging preexistente de otro requerimiento, usar un mecanismo
  de aislamiento previamente aprobado que no altere el índice normal, o
  detenerse si no puede garantizarse el contenido exacto del commit.
- Validar por separado cambios staged y unstaged cuando comparten una ruta.
- No incluir ruido de Power BI Desktop, selecciones persistidas,
  `diagramLayout.json`, cultures, bookmarks, `pages.json` ni visuales fuera
  de alcance sin justificación funcional explícita.

## Push

Antes de push:

```powershell
git fetch origin
git log --oneline origin/main..HEAD
git log --oneline HEAD..origin/main
git diff --cached --name-status
```

Hacer push solo si:

1. La rama actual es `main`.
2. No hay staging activo.
3. No hay commits remotos pendientes.
4. Los commits locales pendientes son exactamente los aprobados.
5. El usuario autorizó el push.

La versión publicada, desplegada o entregada debe corresponder al commit
validado. Si una publicación se realiza desde Power BI Desktop o Power BI
Service, registrar el hash de origen y comprobar que no existan cambios
locales posteriores dentro del alcance publicado.

Después de push:

```powershell
git status -sb
git log --oneline origin/main..HEAD
git log --oneline HEAD..origin/main
```
