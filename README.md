# Planeación de Personal - People Analytics

Repositorio del dashboard **Planeación de Personal** del Grupo Empresarial Lemco, construido como **Power BI Desktop Project (PBIP)**.

El proyecto centraliza indicadores de Gestión Humana para headcount, presupuesto vs real, ingresos, retiros, selección, ausentismo, incapacidades, SST y gasto laboral. El público principal es la Gerencia Corporativa de Gestión Humana y equipos directivos que consumen analítica agregada.

## Estado Actual

Estado documentado: `2026-07-17`.

- PBIP principal: `PBIP/Proyecto7.pbip`.
- Rama principal: `main`.
- Repositorio remoto: `https://github.com/HarvLopez91/07_Planeacion_de_Personal.git`.
- El proyecto usa Git y requiere staging selectivo por alcance.
- La migración de fuentes a SharePoint corporativo está en curso.
- La validación de **Formula Firewall** sigue pendiente de evidencia interactiva en Power BI Desktop.
- No debe avanzarse a validación funcional de páginas hasta confirmar que `Aplicar cambios` y el refresh completo terminan sin errores.
- El working tree puede contener cambios PBIP acumulados fuera de alcance; no limpiarlo ni mezclarlo con documentación.

## Estructura Principal

```text
07_Planeacion_de_Personal/
├── PBIP/        # Proyecto Power BI Desktop Project
├── Docs/        # Documentación oficial versionada
├── Specs/       # Análisis de impacto y planes aprobables
├── Outputs/     # Evidencia temporal local, no versionada
├── Data/        # Datos locales, no versionados
├── Reports/     # Informes recurrentes versionables
├── Tools/       # Utilidades de soporte, si están aprobadas
├── Assets/      # Recursos de apoyo, si están aprobados
├── README.md
├── AGENTS.md
└── CLAUDE.md
```

`Outputs/` y `Data/` no deben incluirse en commits. `Specs/` no se mezcla con commits técnicos salvo aprobación explícita.

## Requisitos de Trabajo

- Power BI Desktop compatible con PBIP y TMDL.
- Git.
- VS Code u otro editor seguro para UTF-8.
- Acceso organizacional al sitio SharePoint corporativo.
- Cuenta con permisos para abrir las fuentes de datos del modelo.

Para validar el bloqueo actual de Formula Firewall, usar Power BI Desktop de julio de 2026 o posterior y revisar la opción preliminar de particiones de privacidad. Ver [Docs/TROUBLESHOOTING.md](Docs/TROUBLESHOOTING.md).

## Cómo Abrir el PBIP

1. Cerrar otras sesiones de Power BI Desktop sobre este proyecto.
2. Abrir Power BI Desktop.
3. Usar `Archivo > Abrir`.
4. Seleccionar `PBIP/Proyecto7.pbip`.
5. No guardar si Power BI Desktop abre con errores no diagnosticados.

## Flujo de Desarrollo

1. Diagnosticar el alcance.
2. Crear o revisar Spec si el cambio es funcional, de modelo, fuente o visual.
3. Implementar solo los archivos autorizados.
4. Validar en Power BI Desktop cuando aplique.
5. Auditar `git diff` y clasificar ruido de Desktop.
6. Hacer staging selectivo con rutas explícitas.
7. Commit separado por bloque.
8. Push solo con aprobación explícita.

Comandos base:

```powershell
git status -sb
git diff --cached --name-status
git diff --check
git log --oneline origin/main..HEAD
git log --oneline HEAD..origin/main
```

Nunca usar `git add .`.

## Documentación Oficial

El índice de documentación vive en [Docs/README.md](Docs/README.md).

Documentos clave:

- [Contexto del proyecto](Docs/PROJECT_CONTEXT.md)
- [Estado y roadmap](Docs/PROJECT_STATUS.md)
- [Arquitectura](Docs/ARCHITECTURE.md)
- [Modelo de datos](Docs/DATA_MODEL.md)
- [Fuentes y pipeline](Docs/DATA_PIPELINE.md)
- [Guía BI](Docs/BI_GUIDELINES.md)
- [Runbook operativo](Docs/RUNBOOK.md)
- [Gobierno Git](Docs/GIT_GOVERNANCE.md)
- [Troubleshooting](Docs/TROUBLESHOOTING.md)
- [Seguridad y privacidad](Docs/SECURITY_AND_PRIVACY.md)

## Reglas Críticas

- No exponer datos personales ni registros individuales.
- No versionar `Data/` ni `Outputs/`.
- No mezclar cambios PBIP, Docs, Specs y Tools en un mismo commit.
- No editar TMDL mientras Power BI Desktop mantiene cambios pendientes.
- No modificar `PBI_ResultType` para ocultar errores.
- No afirmar refresh exitoso sin evidencia visual o confirmación explícita.

## Próximos Pasos

1. Validar Formula Firewall en Power BI Desktop actualizado.
2. Confirmar `Aplicar cambios` y refresh completo sin errores.
3. Auditar cambios PBIP pendientes por bloque.
4. Tratar por separado los pendientes de `AREAS`, `REQUISICIONES HABITEL 2026.xlsx`, `AUSENTISMOS` y `Estructura`.
