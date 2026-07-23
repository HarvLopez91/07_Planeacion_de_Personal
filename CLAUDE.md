# CLAUDE.md

@AGENTS.md

## Contexto para Claude Code

Este repositorio corresponde al proyecto Power BI/PBIP `07_Planeación_de_Personal`.

- PBIP principal: `PBIP/Proyecto7.pbip`.
- Documentación oficial: `Docs/`.
- Especificaciones, análisis de impacto, requisitos y planes de implementación: `Specs/`.
- Evidencias temporales: `Outputs/`.
- Datos locales: `Data/`, no versionar.

## Bloque operativo mínimo

1. Trabajar únicamente dentro del alcance aprobado por el usuario.
2. No crear ni conservar intencionalmente artefactos del proyecto fuera de la raíz, salvo autorización; se permiten temporales automáticos no permanentes.
3. No eliminar, descartar, sobrescribir ni revertir cambios existentes del usuario.
4. No usar `git add .` ni `git add -A`.
5. No ejecutar commit ni push sin autorización explícita.
6. Clasificar los archivos según su propósito en `Specs/`, `Outputs/` o `Docs/`.
7. Consultar la fuente canónica correspondiente cuando la tarea involucre estructura, Git o privacidad.

## Fuentes canónicas

- Ubicación o creación de archivos: [Docs/ESTRUCTURA_PROYECTO.md](Docs/ESTRUCTURA_PROYECTO.md)
- Staging, commit, push o exclusiones: [Docs/GIT_GOVERNANCE.md](Docs/GIT_GOVERNANCE.md)
- Datos personales, confidenciales o fuentes sensibles: [Docs/SECURITY_AND_PRIVACY.md](Docs/SECURITY_AND_PRIVACY.md)

## Estado Crítico Vigente

Al `2026-07-17`, la migración de fuentes hacia SharePoint corporativo no está cerrada funcionalmente. Existen bloqueos o riesgos de Formula Firewall asociados a:

- `PLANTA DE PERSONAL`.
- `Selección Grupo Lemco`.
- `SENA UNIDADES`.

No afirmar que `Aplicar cambios` o el refresh local fueron exitosos sin evidencia visual o confirmación explícita del usuario.

## Documentos Clave

- `Docs/PROJECT_STATUS.md`: estado operativo y pendientes.
- `Docs/DATA_PIPELINE.md`: fuentes y migración SharePoint.
- `Docs/GIT_GOVERNANCE.md`: reglas de staging, commit y push.
- `Docs/TROUBLESHOOTING.md`: Formula Firewall y errores de refresh.
- `Docs/SECURITY_AND_PRIVACY.md`: manejo de datos sensibles.
