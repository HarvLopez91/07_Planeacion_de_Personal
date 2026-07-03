# Documentacion Tecnica — Planeacion de Personal

Indice de toda la documentacion tecnica del proyecto Power BI de People Analytics del Grupo Empresarial Lemco.

## Proposito

Esta carpeta centraliza el conocimiento tecnico del proyecto: arquitectura, modelo de datos, metricas, fuentes de informacion, procedimientos operativos y decisiones de diseno.

La documentacion fue generada el **2026-06-11** a partir del analisis directo de los archivos TMDL, M (Power Query) y JSON del proyecto PBIP.

---

## Indice de documentos

| Documento | Descripcion | Estado | Ultima revision |
|---|---|---|---|
| [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | Contexto de negocio, empresas del grupo, proposito del reporte y alcance | Vigente | 2026-06-11 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Estructura PBIP, capas del modelo, grupos de consulta y diagrama general | Vigente | 2026-06-11 |
| [DATA_MODEL.md](DATA_MODEL.md) | Tablas, columnas relevantes, relaciones y cardinalidades. Fuente oficial del modelo | Vigente | 2026-06-11 |
| [METRICS_CATALOG.md](METRICS_CATALOG.md) | Catalogo completo de medidas DAX clasificadas por dominio. Fuente oficial de metricas | Vigente | 2026-06-11 |
| [DATA_PIPELINE.md](DATA_PIPELINE.md) | Fuentes de datos, cuentas SharePoint, transformaciones Power Query y actualizacion | Vigente | 2026-06-11 |
| [BI_GUIDELINES.md](BI_GUIDELINES.md) | Inventario de paginas, bookmarks, recursos visuales y convenciones del reporte | Vigente | 2026-07-03 |
| [SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md) | Campos con datos personales, cuentas de acceso, riesgos y controles recomendados | Vigente | 2026-07-03 |
| [RUNBOOK.md](RUNBOOK.md) | Procedimientos operativos: apertura, actualizacion, publicacion y mantenimiento | Vigente | 2026-07-03 |
| [CHANGELOG.md](CHANGELOG.md) | Registro de cambios del proyecto | Vigente | 2026-07-03 |
| [decisions/README.md](decisions/README.md) | Registro de decisiones de arquitectura (ADRs) | Pendiente | 2026-06-11 |
| [ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md) | Estandar corporativo de carpetas, politica de archivos .md, nomenclatura y criterio de actualizacion documental | Vigente | 2026-07-03 |

### Documentos que no aplican

| Documento | Razon |
|---|---|
| `REQUIREMENTS.md` | No existen requisitos formales documentados en el repositorio |
| `DEVELOPMENT_GUIDE.md` | No hay proceso de compilacion ni entorno de desarrollo local estandarizado |
| `TESTING.md` | No existen pruebas automatizadas. Hay una pagina QA en el reporte (ver [BI_GUIDELINES.md](BI_GUIDELINES.md)) |
| `DEPLOYMENT.md` | El despliegue al servicio Power BI no esta documentado en el repositorio (`Pendiente de confirmar`) |
| `API_REFERENCE.md` | El proyecto no expone ni consume APIs programaticas |
| `AUTOMATIONS.md` | No se identificaron automatizaciones en el repositorio |
| `CONTRIBUTING.md` | No existe proceso de contribucion definido. No hay control de versiones activo |
| `UI_UX_GUIDELINES.md` | No aplica a proyectos Power BI; sustituido por `BI_GUIDELINES.md` |

---

## Regla para crear nuevos documentos en `Docs/`

Solo crear un nuevo archivo `.md` en `Docs/` si:

1. Existe evidencia verificable en el repositorio que justifica el documento.
2. No hay un documento existente que ya cubra el tema (evitar duplicación).
3. Se registra en la tabla de índice con estado, fecha y propósito.
4. El contenido es oficial, vigente y mantenible — no diagnósticos ni borradores (estos van en `Outputs/documentation/`).

---

## Temas pendientes de confirmar

- Proceso de publicacion al servicio Power BI (workspace destino, frecuencia de actualizacion programada)
- Propietario formal del proyecto y responsables de cada fuente de datos
- Existencia de reglas de negocio documentadas externamente
- Si la carpeta `Data/` tiene un uso especifico o es un espacio de trabajo temporal
- Politica de actualizacion del historico (si se mantienen archivos Excel anuales o se consolidan)

---

## Guia rapida de navegacion

```
Pregunta                          → Documento
─────────────────────────────────────────────────────────
¿Que hace este proyecto?          → PROJECT_CONTEXT.md
¿Como esta organizado?            → ARCHITECTURE.md
¿Que tablas y relaciones hay?     → DATA_MODEL.md
¿Que mide X metrica?              → METRICS_CATALOG.md
¿De donde vienen los datos?       → DATA_PIPELINE.md
¿Que paginas tiene el reporte?    → BI_GUIDELINES.md
¿Hay datos sensibles?             → SECURITY_AND_PRIVACY.md
¿Como actualizo el modelo?        → RUNBOOK.md
```
