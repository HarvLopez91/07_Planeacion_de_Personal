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

## Cierre obligatorio de implementaciones y worktrees

Una implementación desarrollada en un worktree (`.wt/` o equivalente) **no se
considera finalizada** solo porque terminó el desarrollo, pasaron las pruebas,
existe un commit, se hizo push, se creó el PR o el PR fue fusionado.

El cierre completo exige:

1. Validación funcional.
2. Validación visual cuando corresponda.
3. Confirmación del alcance exacto versionado.
4. Integración correcta del PR en `main`.
5. Actualización del checkpoint principal desde `origin/main`.
6. Confirmación de que no se perdió trabajo local previo.
7. Apertura y validación del PBIP oficial desde el checkpoint principal cuando
   aplique.
8. Si Power BI Desktop realizó refresh, guardado o publicación, revisar de
   inmediato `git status`, identificar reserialización o ruido, separar cambios
   funcionales de cambios automáticos y decidir explícitamente qué se versiona,
   qué queda pendiente y qué puede descartarse.
9. Auditoría del worktree mediante `git worktree list`, rama, `git status`,
   commits pendientes, archivos tracked modificados y archivos untracked
   relevantes.
10. Si existe trabajo no integrado, **detenerse y no eliminar el worktree**.
11. Si todo quedó integrado, retirar el worktree mediante
    `git worktree remove <ruta>`, sin `--force` salvo autorización explícita.
12. No borrar worktrees manualmente desde Explorer, `rm` o `rmdir`.
13. `git worktree prune` solo puede evaluarse después del retiro correcto y
    cuando existan metadatos obsoletos; no se ejecuta automáticamente ni sin
    auditar los demás worktrees.
14. Las ramas locales ya fusionadas pueden reportarse como candidatas a
    eliminación, pero no se eliminan sin autorización explícita.
15. Documentar el estado final antes de iniciar otro frente.

El procedimiento operativo detallado está en
[Specs/01_plan_gobierno_outputs_skills_tools.md](Specs/01_plan_gobierno_outputs_skills_tools.md)
y el gate resumido está en
[Specs/00_roadmap_y_backlog.md](Specs/00_roadmap_y_backlog.md).

### Checkpoint principal

El checkout principal de `main` es el checkpoint oficial para consolidación,
validación, refresh y publicación. El PBIP oficial del Proyecto 07 es
`PBIP/Proyecto7.pbip`.

Las implementaciones funcionales se realizan en worktrees aislados. El
checkpoint principal no se usa como espacio habitual de desarrollo. Después de
cada apertura con guardado, refresh o publicación desde Power BI Desktop se
debe revisar inmediatamente su estado Git para evitar acumulación de
reserialización o cambios locales sin clasificar.

### Definition of Done

Una implementación solo puede quedar como `DONE`, `CERRADA` o `FINALIZADA`
cuando se cumpla todo lo siguiente:

- validación funcional = `PASS`;
- validación visual = `PASS`, cuando corresponda;
- commit y push correctos;
- PR fusionado en `main`;
- checkpoint principal actualizado;
- PBIP oficial validado;
- ruido posterior a Power BI revisado;
- worktree auditado;
- worktree retirado si ya no es necesario;
- pendientes documentados;
- `main` sincronizada con `origin/main`.

Si falta cualquiera de estos puntos, el estado obligatorio es
`PENDIENTE DE CIERRE`.

## Criterio de entrega

Toda entrega debe reportar:

- objetivo atendido;
- archivos modificados;
- archivos excluidos;
- riesgos;
- validaciones ejecutadas;
- estado de staging/commit/push;
- siguiente paso recomendado.
