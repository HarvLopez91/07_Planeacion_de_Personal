# Gobierno Git

Fecha de referencia: `2026-07-17`.

## Principio General

Este repositorio se trabaja con control de cambios estricto porque Power BI Desktop puede modificar muchos archivos PBIP no relacionados con el objetivo de una tarea. Todo cambio debe separarse por alcance y validarse antes de staging.

## Reglas Obligatorias

- No usar `git add .`.
- No hacer staging sin rutas explícitas.
- No hacer commit sin validar identidad Git.
- No hacer push sin autorización explícita.
- No usar `push --force`.
- No usar `reset`, `restore`, `checkout`, `clean`, `stash`, `rebase`, `cherry-pick` ni `commit --amend` salvo aprobación específica.
- No limpiar el working tree para “ordenar” cambios PBIP acumulados.
- No mezclar PBIP con documentación, Specs, Outputs, Tools o Assets en un mismo commit salvo aprobación explícita.

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
- Commits separados para modelo, visuales, documentación, Specs o herramientas.

### Prohibido

- `Outputs/` salvo aprobación explícita.
- `Data/`.
- Ruido de Power BI Desktop no relacionado.
- `diagramLayout.json`, `pages.json`, bookmarks o cultures sin justificación explícita.
- Archivos PBIP de otras páginas o tablas fuera de alcance.

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

Ejemplos:

- `docs: actualiza documentación y gobierno del proyecto PBIP`
- `fix(data): migra fuentes a SharePoint corporativo`
- `feat(visuals): agrega slicer de dependencia en demografico promedio`

No incluir coautores si el usuario no lo solicita.

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

Después de push:

```powershell
git status -sb
git log --oneline origin/main..HEAD
git log --oneline HEAD..origin/main
```
