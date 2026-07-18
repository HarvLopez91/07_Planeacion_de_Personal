# Documentación Técnica - Planeación de Personal

Índice de documentación oficial del proyecto Power BI/PBIP `07_Planeación_de_Personal`.

Fecha de revisión documental: `2026-07-17`.

## Propósito

Esta carpeta centraliza la documentación estable del proyecto: contexto, arquitectura, modelo de datos, métricas, fuentes de información, operación, seguridad, gobierno Git y solución de problemas.

Los diagnósticos temporales, evidencias de fases y capturas de trabajo pertenecen a `Outputs/`. Las especificaciones y planes de implementación pertenecen a `Specs/`.

## Índice de Documentos

| Documento | Descripción | Estado | Última revisión |
|---|---|---|---|
| [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | Contexto de negocio, dominios cubiertos y limitaciones conocidas | Vigente | 2026-07-17 |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Estado operativo, bloqueos y pendientes vigentes | Vigente | 2026-07-17 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Estructura PBIP, modelo semántico y reporte | Vigente | 2026-07-17 |
| [DATA_MODEL.md](DATA_MODEL.md) | Tablas, columnas relevantes, relaciones y cardinalidades | Vigente | 2026-07-14 |
| [METRICS_CATALOG.md](METRICS_CATALOG.md) | Catálogo de medidas DAX clasificadas por dominio | Vigente | 2026-06-11 |
| [DATA_PIPELINE.md](DATA_PIPELINE.md) | Fuentes, Power Query, SharePoint y actualización | Vigente | 2026-07-17 |
| [BI_GUIDELINES.md](BI_GUIDELINES.md) | Inventario de páginas, bookmarks, recursos visuales y convenciones | Vigente | 2026-07-03 |
| [SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md) | Datos personales, accesos, privacidad y riesgos | Vigente | 2026-07-17 |
| [RUNBOOK.md](RUNBOOK.md) | Procedimientos operativos de apertura, refresh y publicación | Vigente | 2026-07-17 |
| [GIT_GOVERNANCE.md](GIT_GOVERNANCE.md) | Reglas de staging, commit y push | Vigente | 2026-07-17 |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Formula Firewall, errores Power Query y ruido PBIP | Vigente | 2026-07-17 |
| [CHANGELOG.md](CHANGELOG.md) | Registro de cambios significativos | Vigente | 2026-07-17 |
| [ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md) | Estándar documental y estructura corporativa | Vigente con notas históricas | 2026-07-17 |
| [decisions/README.md](decisions/README.md) | Registro de decisiones de arquitectura | Pendiente | 2026-06-11 |

## Estado Actual Resumido

- El repositorio sí tiene Git configurado.
- El trabajo PBIP requiere staging selectivo por alcance.
- `PBIP/` puede presentar cambios acumulados o ruido de Power BI Desktop; no mezclar con documentación.
- La migración de fuentes a SharePoint corporativo está parcialmente implementada y pendiente de validación final de refresh.
- Formula Firewall sigue como riesgo activo hasta validar `Aplicar cambios` y refresh completo en Power BI Desktop.
- No versionar `Outputs/` ni `Data/`.

## Documentos que No Aplican o Siguen Pendientes

| Documento | Razón |
|---|---|
| `REQUIREMENTS.md` | Los requerimientos se gestionan mediante `Specs/` por iniciativa aprobada |
| `DEVELOPMENT_GUIDE.md` | No hay proceso de compilación; el desarrollo se realiza en Power BI Desktop y edición controlada de PBIP |
| `TESTING.md` | No existen pruebas automatizadas; la validación se documenta en Outputs y Specs |
| `DEPLOYMENT.md` | La publicación al servicio Power BI sigue pendiente de documentación formal |
| `API_REFERENCE.md` | El proyecto no expone APIs programáticas |
| `AUTOMATIONS.md` | No hay automatización estable aprobada para refresh o despliegue |
| `CONTRIBUTING.md` | El flujo está cubierto por `GIT_GOVERNANCE.md`, `AGENTS.md` y `CLAUDE.md` |
| `UI_UX_GUIDELINES.md` | Sustituido por `BI_GUIDELINES.md` |

## Regla para Crear Nuevos Documentos en `Docs/`

Crear un nuevo archivo `.md` en `Docs/` solo si:

1. Existe evidencia verificable que justifica el documento.
2. No hay un documento existente que ya cubra el tema.
3. El contenido es oficial, vigente y mantenible.
4. El documento queda registrado en este índice.

Diagnósticos, evidencias de fases, capturas, comparativos y borradores van en `Outputs/`.

## Guía Rápida

| Pregunta | Documento |
|---|---|
| ¿Qué hace el proyecto? | `PROJECT_CONTEXT.md` |
| ¿Cuál es el estado actual? | `PROJECT_STATUS.md` |
| ¿Cómo está organizado el PBIP? | `ARCHITECTURE.md` |
| ¿Qué tablas y relaciones hay? | `DATA_MODEL.md` |
| ¿Qué mide una métrica? | `METRICS_CATALOG.md` |
| ¿De dónde vienen los datos? | `DATA_PIPELINE.md` |
| ¿Qué páginas tiene el reporte? | `BI_GUIDELINES.md` |
| ¿Cómo actualizo o valido el modelo? | `RUNBOOK.md` |
| ¿Qué hago con Formula Firewall? | `TROUBLESHOOTING.md` |
| ¿Cómo hago staging/commit/push? | `GIT_GOVERNANCE.md` |
| ¿Hay datos sensibles? | `SECURITY_AND_PRIVACY.md` |
