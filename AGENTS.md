# AGENTS.md

Instrucciones duraderas para Codex, Claude Code y otros agentes que trabajen en `07_Planeación_de_Personal`.

## Proyecto

Dashboard Power BI/PBIP de People Analytics para Planeación de Personal del Grupo Empresarial Lemco.

- PBIP principal: `PBIP/Proyecto7.pbip`.
- Rama principal: `main`.
- Remoto esperado: `https://github.com/HarvLopez91/07_Planeacion_de_Personal.git`.

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
- Mejoras e implementaciones futuras: [Specs/00_roadmap_y_backlog.md](Specs/00_roadmap_y_backlog.md)

## Roadmap y backlog

- La fuente maestra de mejoras e implementaciones futuras es `Specs/00_roadmap_y_backlog.md`.
- Todo agente debe consultarla antes de proponer una nueva iniciativa o retomar una existente.
- Registrar una iniciativa no autoriza su ejecución.
- Antes de iniciar una implementación, debe existir autorización expresa y, cuando aplique, análisis de impacto y plan de implementación en `Specs/`.
- Al avanzar una iniciativa, actualizar su estado, próximo paso, evidencia y enlaces relacionados en el roadmap.
- Ningún agente debe marcar una iniciativa como finalizada sin pruebas y evidencia verificable.
- No crear documentos duplicados de roadmap o backlog en `Outputs/`.
- Mantener IDs estables y evitar renumerar iniciativas existentes.

## Criterio de entrega

Toda entrega debe reportar:

- objetivo atendido;
- archivos modificados;
- archivos excluidos;
- riesgos;
- validaciones ejecutadas;
- estado de staging/commit/push;
- siguiente paso recomendado.