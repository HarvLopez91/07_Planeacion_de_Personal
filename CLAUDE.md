# CLAUDE.md

@AGENTS.md

## Contexto para Claude Code

Este repositorio corresponde al proyecto Power BI/PBIP `07_Planeación_de_Personal`.

- PBIP principal: `PBIP/Proyecto7.pbip`.
- Documentación oficial: `Docs/`.
- Specs aprobables: `Specs/`.
- Evidencias temporales: `Outputs/`.
- Datos locales: `Data/`, no versionar.

## Reglas Operativas

1. Leer `AGENTS.md` antes de actuar.
2. Consultar `Docs/README.md` para ubicar la documentación oficial.
3. Ejecutar `git status -sb` antes de cualquier cambio.
4. No usar `git add .`.
5. No hacer commit ni push sin autorización explícita.
6. No limpiar, revertir ni descartar cambios del usuario.
7. No modificar PBIP sin alcance aprobado y evidencia previa.
8. No exponer datos personales ni registros individuales.

## Estado Crítico Vigente

Al `2026-07-17`, la migración de fuentes hacia SharePoint corporativo no está cerrada funcionalmente. Existen bloqueos o riesgos de Formula Firewall asociados a:

- `PLANTA DE PERSONAL`.
- `Selección Grupo Lemco`.
- `SENA UNIDADES`.

No afirmar que `Aplicar cambios` o el refresh local fueron exitosos sin evidencia visual o confirmación explícita del usuario.

## Staging y Commits

Usar staging selectivo con rutas explícitas. El working tree puede estar sucio por cambios PBIP preexistentes y no relacionados.

Antes de cualquier commit:

```powershell
git status -sb
git diff --cached --name-status
git diff --check
git config --local --get user.name
git config --local --get user.email
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
```

Identidad esperada:

```text
EdwinClavijoChallenger <edwin.clavijo@challenger.co>
```

## Documentos Clave

- `Docs/PROJECT_STATUS.md`: estado operativo y pendientes.
- `Docs/DATA_PIPELINE.md`: fuentes y migración SharePoint.
- `Docs/GIT_GOVERNANCE.md`: reglas de staging, commit y push.
- `Docs/TROUBLESHOOTING.md`: Formula Firewall y errores de refresh.
- `Docs/SECURITY_AND_PRIVACY.md`: manejo de datos sensibles.
