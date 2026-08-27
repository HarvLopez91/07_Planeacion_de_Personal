# Roadmap y backlog técnico

## 1. Propósito

Este archivo es la **fuente maestra** para registrar, priorizar y dar seguimiento a mejoras, implementaciones futuras e iniciativas en curso del proyecto `07_Planeación_de_Personal`.

Reglas de interpretación:

- El roadmap **orienta la planeación**; no es un plan de ejecución en sí mismo.
- **Registrar una iniciativa aquí no constituye autorización para ejecutarla.**
- Todo cambio funcional sobre `PBIP/Proyecto7.pbip` (modelo, DAX, Power Query, fuentes, relaciones, visuales, páginas) requiere **aprobación expresa del usuario**, conforme a `AGENTS.md`, `CLAUDE.md` y `Docs/GIT_GOVERNANCE.md`.
- Las implementaciones aprobadas deben contar con **especificaciones independientes** en `Specs/` (análisis de impacto y/o plan de implementación) antes de ejecutarse.
- Este roadmap **no reemplaza** los análisis de impacto ni los planes de implementación existentes en `Specs/`; los enlaza y resume su estado.

## 2. Alcance del proyecto

| Campo | Valor |
|---|---|
| Nombre del proyecto | Dashboard Power BI/PBIP de Planeación de Personal — `07_Planeación_de_Personal` |
| Repositorio | `HarvLopez91/07_Planeacion_de_Personal` |
| PBIP principal | `PBIP/Proyecto7.pbip` |
| Rama base | `main` |
| Área funcional | People Analytics Grupo Empresarial Lemco — HeadCount, Presupuesto (PptovsReal), Selección, Ausentismo/Incapacidades, SST, SENA |
| Estado general | Migración de fuentes a SharePoint corporativo **en curso** (parcial: PptovsReal y SST cerrados; PLANTA DE PERSONAL, Selección Grupo Lemco, SENA UNIDADES con Formula Firewall sin validar). Working tree con cambios PBIP acumulados pendientes de auditar |
| Fecha de última actualización de este roadmap | 2026-08-26 |
| Responsable de mantenimiento documental | Edwin Clavijo |

## 3. Reglas de gobierno

- Cada iniciativa tiene un **ID único y estable** (categoría + número consecutivo). No se renumeran IDs existentes aunque cambie su prioridad o estado.
- Los estados se actualizan **solo con evidencia** verificable (commit, archivo de `Specs/`, resultado de validación) — no por declaración sin respaldo.
- Ningún agente (Codex, Claude Code, Copilot u otro) puede marcar una iniciativa como **Finalizada** sin evidencia de validación enlazada.
- No mezclar mejoras de gobierno documental con cambios funcionales de PBIP en un mismo commit, salvo autorización expresa.
- `Specs/` contiene decisiones, análisis de impacto y planes de implementación oficiales.
- `Docs/` contiene documentación estable del estado vigente del proyecto.
- `Outputs/` contiene evidencias y borradores; **no es fuente oficial** salvo aprobación explícita del usuario.
- `.agents/skills/` contiene las skills del repositorio (propias y vendored — ver sección 11).
- `Tools/` contiene herramientas ejecutables organizadas por dominio (`Tools/governance/`, `Tools/pbip/`, `Tools/automation/`); son de **solo lectura por defecto**.
- Toda iniciativa que pase a **Planificada** o **En curso** debe tener análisis de impacto y/o plan de implementación en `Specs/`, y validación registrada cuando aplique.
- Los cambios funcionales deben conservar trazabilidad completa: iniciativa (ID) → spec(s) → archivos modificados → validación → commit.
- No declarar Formula Firewall resuelto ni refresh exitoso sin evidencia visual confirmada en Power BI Desktop (regla ya vigente en `Docs/TROUBLESHOOTING.md` y `CLAUDE.md`).

## 4. Catálogo de estados

| Estado | Uso |
|---|---|
| Idea | Propuesta inicial sin análisis; puede no llegar a ejecutarse |
| En evaluación | Se está valorando viabilidad, alcance o impacto |
| Priorizada | Evaluada y aceptada como relevante; en espera de turno o recursos |
| Planificada | Cuenta con plan de implementación aprobado, aún sin iniciar ejecución |
| En curso | Implementación activa, con o sin commits parciales |
| Bloqueada | Detenida por una dependencia externa, decisión pendiente o falta de datos |
| En validación | Implementada, pendiente de confirmación funcional o evidencia final |
| Finalizada | Implementada y validada con evidencia verificable |
| Descartada | Evaluada y no se ejecutará; se documenta el motivo |

## 5. Catálogo de prioridades

| Prioridad | Criterio |
|---|---|
| Crítica | Bloquea gobierno, integridad del modelo, Formula Firewall o cumplimiento de datos personales (ver `Docs/SECURITY_AND_PRIVACY.md`); impacto alto y urgencia alta |
| Alta | Impacto relevante para la Dirección de Gestión Humana o para la trazabilidad de fuentes/refresh; esfuerzo razonable |
| Media | Mejora de gobierno, calidad o reutilización sin urgencia inmediata |
| Baja | Ajuste cosmético, exploratorio o de bajo impacto |

La prioridad considera impacto, riesgo, dependencia, urgencia y esfuerzo — no solo preferencia.

## 6. En curso

| ID | Iniciativa | Tipo | Prioridad | Estado | Dependencias | Próximo paso | Criterio de aceptación | Especificación o evidencia |
|---|---|---|---|---|---|---|---|---|
| DATA-001 | Validación de Formula Firewall para consultas raíz `PLANTA DE PERSONAL`, `Selección Grupo Lemco`, `SENA UNIDADES` | Datos / Power Query | Crítica | En evaluación | Sesión interactiva en Power BI Desktop (no automatizable) | Ejecutar el procedimiento manual documentado en `Docs/TROUBLESHOOTING.md` y registrar evidencia visual | Las tres consultas raíz cargan sin bloqueo de Formula Firewall, con evidencia visual adjunta | `CLAUDE.md`, `Docs/TROUBLESHOOTING.md`, `Docs/PROJECT_STATUS.md` |
| DATA-011 | Gobierno y organización de fuentes de contratos Kactus | Datos / Gobierno | Media | En validación | Confirmación de consumidores Power BI y analisis de impacto para migracion de rutas | Auditar consumidores actuales o futuros del consolidador y preparar Spec antes de conectar `PBIP/Proyecto7.pbip` | Estructura física verificada, `Data/` excluido de Git, archivo oficial identificado, origen corporativo confirmado, consultas internas del consolidador validadas, proceso mensual documentado, consumidores identificados e histórico excluido del procesamiento activo | `Docs/ESTRUCTURA_PROYECTO.md`, `Docs/DATA_PIPELINE.md`, `Docs/RUNBOOK.md`, `Docs/SECURITY_AND_PRIVACY.md` |
| GOV-001 | Auditoría del working tree PBIP acumulado (235+ rutas modificadas/eliminadas/sin trackear) | Gobierno / Git | Alta | En evaluación | Ninguna | Clasificar cambios por bloque (bookmarks, páginas, tablas TMDL) antes de cualquier staging | Inventario documentado de qué bloques son ruido de Power BI Desktop vs. cambios funcionales reales | `git status --short --branch` (07_Planeación_de_Personal), README.md §"Próximos Pasos" |
| GOV-002 | Triage de ramas y worktrees activos sin fusionar (`.wt/hotfix-ausentismos`, `.wt/integracion-productividad`, `.wt/prod`, `.wt/Proyecto7_productividad_gasto`, `.wt/sst`) | Gobierno / Git | Media | En evaluación | Ninguna | Confirmar con el usuario cuáles siguen vigentes y cuáles pueden cerrarse | Cada worktree/rama tiene una decisión documentada (fusionar, mantener o descartar) | Ramas locales: `fix/productividad-contexto-negocio`, `harvlopez91-docs-estructura-vigente`, `hotfix/ausentismos-medidas-duplicadas`, `integration/productividad-contexto-negocio`, `refactor/sst-table-names` |
| GOV-006 | Diagnóstico seguro (solo lectura) de worktrees en cuarentena por OneDrive (`HEAD` en todo-ceros tras fallos de `git worktree remove`) | Gobierno / Git / Automatización | Media | En validación | Ninguna | Uso repetido en producción sobre los worktrees en cuarentena reales antes de cerrar la iniciativa | Script clasifica correctamente el corpus de 5 worktrees conocidos, `--help`/`--json` funcionan, sin temporales residuales, búsqueda de operaciones prohibidas en el código no encuentra ninguna, skill documenta el procedimiento completo incluida la advertencia de que `SAFE` no autoriza eliminación automática | `Specs/0021_diagnostico_worktrees_cuarentena_onedrive.md` |
| PBIP-006 | Nueva página `Sociodemográfico por Empresa`: comparación simultánea de indicadores sociodemográficos entre las empresas del Grupo LEMCO, a partir de `Demográfico (Promedio)` | Modelo / Visuales | Media | En curso | Ninguna | Aplicar corrección posterior solicitada por el usuario a partir del checkpoint pre-corrección validado | 7 comparativos (Colaboradores, Tipo de Contrato, Generación, Tipo de Cargo, Género, Antigüedad, Matriz Empresa/Dependencia/Cargo) por `PLANTA DE PERSONAL[GRUPO EMPRESA]`, validados sin `(En blanco)` en sesión interactiva de Power BI Desktop; `Demográfico (Promedio)` sin cambios funcionales; ruido `RESERIALIZATION` reevaluado y excluido del commit | `Specs/0024_analisis_impacto_sociodemografico_por_empresa.md` (sección "Checkpoint pre-corrección"); rama `feat/sociodemografico-por-empresa`, worktree `.wt/sociodemografico-por-empresa` |

Nota: `DATA-002` (refresh completo), `DATA-003` (matriz de retiros por estructura) y `DATA-004` (diagnóstico de brechas de homologación) están activas pero bloqueadas — ver [sección 9](#9-bloqueadas) para evitar duplicar su registro en dos tablas.

## 7. Próximas implementaciones

| ID | Iniciativa | Descripción | Aplica a | Prioridad | Dependencias | Riesgos | Próximo paso |
|---|---|---|---|---|---|---|---|
| DATA-006 | Migración de `AUSENTISMOS` y `Estructura` a fuente corporativa | Persisten como fuentes personales o pendientes de análisis (`Docs/DATA_PIPELINE.md`) | Datos | Media | Ninguna conocida | Riesgo de romper medidas dependientes si el esquema cambia | Analizar impacto y plan de implementación |
| DATA-007 | Evaluar alcance de `REQUISICIONES HABITEL 2026.xlsx` | Declarado "fuera de alcance" en `Docs/DATA_PIPELINE.md`; confirmar si debe incorporarse | Datos | Baja | Ninguna | Ninguno si permanece fuera de alcance | Confirmar con el usuario si se mantiene fuera de alcance o se prioriza |
| GOV-003 | Corregir `Tools/governance/outputs_indexer.py` y `Tools/governance/prepare_commit_review.py` copiados sin adaptar desde `04_Aprendizaje_y_Desarrollo` | Las constantes `DOMINIOS` y `DOCUMENTOS_GOBIERNO` referencian dominios y archivos del proyecto hermano (ej. `ds07_nine_box`, `Docs/BRAND_GUIDELINES.md`) que no existen aquí | Gobierno / Tools | Media | Ninguna | Los reportes que generen hoy no serán confiables para este proyecto | Adaptar dominios y rutas de gobierno al vocabulario real de Planeación de Personal antes de comitear |
| GOV-004 | Corregir el nombre de la skill `pbi-aprendizaje-inventario` | El nombre referencia el dominio del proyecto hermano (Aprendizaje), no Planeación de Personal | Gobierno / Skills | Baja | GOV-003 | Confusión sobre el alcance real de la skill | Renombrar junto con la corrección de `Tools/pbip/list_pbip_structure.py` si aplica |
| DOC-001 | Actualizar `Docs/CHANGELOG.md` | El encabezado más reciente (`2026-07-24`) no refleja el contenido real, que incluye trabajo del 2026-07-29 (Specs 0010–0012); faltan entradas para Specs 0013–0014 | Documentación | Media | Ninguna | Ninguno | Redactar entradas faltantes y corregir encabezado de fecha |
| DOC-002 | Resolver ADR-005, ADR-006 y ADR-007 pendientes | Páginas ocultas obsoletas (ADR-005), ausencia de RLS (ADR-006), encoding HTML en nombre de columna `GENERACIÓN` (ADR-007) | Modelo / Gobierno | Media | Ninguna | ADR-006 tiene implicación de seguridad de datos (todos los usuarios ven todas las empresas) | Revisar `Docs/decisions/README.md` y decidir cada ADR con el usuario |
| QA-001 | Replicar `tools/pbip_validation/` (validador estático PBIP) desde `04_Aprendizaje_y_Desarrollo` | Proyecto 4 ya cuenta con un validador estático (`validate_pbip.py`) que no está replicado aquí | QA / Automatización | Media | Requiere `project_rules.json` propio de este proyecto | Duplicar sin adaptar produciría falsos positivos/negativos | Evaluar junto con GOV-003 como parte de la validación cruzada Proyecto 4 ↔ Proyecto 7 |
| PBIP-005 | Desagregación de indicadores de retiros/rotación por Dependencia, Área y Cargo en `Retiros` | El usuario agregó manualmente 3 slicers (Área/Cargo/Dependencia) en `Retiros` como línea base intencional (2026-08-06/10), pero las matrices/tarjetas de análisis conectadas a esos slicers todavía no se construyeron; además existen 2 visuales legado en `Rotación2` (`5abcdd8fd1c5a1015723`, `8d3d8ab39e15678e422a`) con la medida `Índice_Retiros` (deuda funcional, no equivalente a `Tasa_Mensual_Retiros`, ver `Specs/0016` sección 12) que deberían reconstruirse o documentarse aparte | Modelo / Visuales | Media | DAX-002 (medidas base ya validadas) | Las medidas base (`Indice_Rotacion`, `Tasa_Mensual_Retiros`, `Tasa_Acumulada_Retiros`, `Variacion_Neta_Personal`) requieren repetir el filtro `Planta Ppto[Ppto/Real]="Real"` a nivel de visual — omitirlo duplicaría el riesgo de cifras infladas ya documentado en `Specs/0016` sección 8 | Elaborar análisis de impacto y plan de implementación en una Spec propia antes de construir los visuales; incluye decidir el destino de `Índice_Retiros` |

## 8. Ideas por evaluar

| ID | Idea | Problema u oportunidad | Beneficio esperado | Riesgo o duda | Decisión pendiente |
|---|---|---|---|---|---|
| DATA-008 | Formalizar contrato de datos para `PptovsReal.xlsx` como fuente compartida con `04_Aprendizaje_y_Desarrollo` | `specs/22` de `04_Aprendizaje_y_Desarrollo` propone consumir `FechaRetiro` desde esta fuente | Evita acoplamiento implícito entre proyectos | Cambios en esta fuente podrían romper el consumo del proyecto hermano sin aviso | Definir si se documenta un contrato explícito (ver `contracts/` de Proyecto 4 como referencia) |
| AI-001 | Gobierno formal de las skills vendored `skills-for-fabric` en este repositorio | Mismo paquete y commit de origen (`d79f3393...`) que en Proyecto 4; sin cadencia de actualización documentada más allá de `check-updates` | Mantener skills alineadas con upstream | Actualizaciones podrían chocar con las 7 skills propias locales | Definir responsable y cadencia de revisión |
| PBIP-001 | Corregir medida `Prom_Colaboradores` hardcodeada | `Docs/METRICS_CATALOG.md` advierte que divide siempre entre 7, incorrecta fuera de enero-julio | Corrección de una medida activa con riesgo de dato erróneo en producción | Cambio de DAX en medida ya publicada; requiere validación cuidadosa | Confirmar prioridad con el usuario (impacto en reportes ejecutivos) |
| DOC-003 | Vigencia de `Docs/decisions/README.md` | Único documento del índice de `Docs/README.md` marcado "Pendiente" | Cerrar el índice documental como 100% vigente | Ninguno | Resolver junto con DOC-002 |
| DATA-013 | Saneamiento de valores `#N/A` de origen en `Consolidado 2025.xlsx` (`DEPENDENCIA_PATRON`, `AREA_PATRON`, `FECHA NACIMIENTO`, `EDAD`, `Generación`, `RANGO DE EDAD`, `EST_CIVIL`, `AGRUPADOR`) | Detectado durante el cierre de `DATA-012` (`Specs/0019` sección 14, `Specs/0020` sección 15.4): hasta 295 filas con valores de error nativos de Excel (`#N/A`, típicamente BUSCARV/XLOOKUP sin coincidencia), 6 de 8 columnas afectadas fuera del alcance de `DATA-012`. Para las ~42 filas de `Generación`/`Rango de Edad`, el motor de Analysis Services sustituye el texto literal `"false"` en vez de dejar la celda en blanco | Elimina el texto `"false"` residual en `Generación` y corrige el resto de columnas afectadas para reportes más limpios | Requiere decidir si el saneamiento se hace en el Excel de origen (formulas) o con una transformación explícita y documentada en Power Query (no genérica, per fila/columna) | Confirmar con el usuario la prioridad y si el saneamiento se hace en la fuente Excel o en Power Query |
| DATA-014 | Automatización mensual de `Retiros_y_Rotacion_Manufactura.xlsx` | El corte de julio 2026 se actualizó manualmente (`Specs/0023`): conteo de Colaboradores desde `Consolidado 2025.xlsx`, conteo de Retiros desde `PptovsReal.xlsx`/`RETIROS` con la regla de exclusión de `Specs/0016`, y una regla manual de homologación de Dependencia/Área por prefijo de `CARGO_CCO` (no gobernada, específica de ese corte) | Elimina el trabajo manual mensual y reduce el riesgo de error humano en la homologación de Dependencia/Área | Requiere decidir si la regla de prefijo se formaliza, se reemplaza por una homologación gobernada, o se elimina; depende de que `PptovsReal.xlsx`/`RETIROS` llegue con `Dependencia`/`Área` completos cada mes | Diferida por otros frentes prioritarios del PBIP; retomar como iniciativa independiente con análisis de impacto y plan de implementación antes de crear `.ipynb`/`.py` |

## 9. Bloqueadas

| ID | Iniciativa | Motivo del bloqueo | Dependencia | Responsable de resolución | Condición de desbloqueo |
|---|---|---|---|---|---|
| DATA-002 | Confirmar refresh completo sin errores | Depende de validar Formula Firewall primero | DATA-001 | Edwin Clavijo (sesión interactiva en Power BI Desktop) | DATA-001 cerrada con evidencia |
| DATA-003 | Matriz de retiros por estructura | Nodos de estructura sin homologación inequívoca | DATA-004 | Edwin Clavijo | Homologación completa o decisión de aceptar remanente documentada |
| DATA-004 | Diagnóstico de brechas de homologación de retiros | Universo de 1.351 registros sin asignación no reconstruible con evidencia disponible; `powerbi-modeling-mcp` no tuvo instancia local de Power BI Desktop durante el preflight | Disponibilidad de Power BI Desktop en vivo o evidencia adicional | Edwin Clavijo | Nueva evidencia disponible o decisión de cerrar el diagnóstico con el remanente aceptado |

## 10. Finalizadas

| ID | Iniciativa | Fecha de cierre | Resultado | Evidencia | Commit |
|---|---|---|---|---|---|
| DATA-009 | Cambio de fuente de `PptovsReal.xlsx` a SharePoint corporativo | 2026-07-23 | Cerrado | `Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md`, `Specs/0007_plan_implementacion_cambio_fuente_pptovsreal_sharepoint.md` | `e287657` |
| GOV-005 | Saneamiento estructural de 27 medidas duplicadas entre tablas de dominio y `Tbl_Medidas` (defecto preexistente que impedía abrir un checkout limpio de `main` en Power BI Desktop) | 2026-08-10 | Cerrado — GATE 5 (apertura real en Power BI Desktop) confirmó carga sin `PFE_TM_OBJECT_NAME_ALREADY_EXISTS`; 122 medidas / 66 relaciones / 52 tablas, 0 duplicados en vivo | `Specs/0018_saneamiento_medidas_duplicadas_gov005.md` | Ver historial del PR de `fix/gov-005-saneamiento-medidas-duplicadas` y Specs/0018 |
| PBIP-002 | Corrección de productividad y contexto de negocio | 2026-07-24 | Cerrado (reemplazó el plan original de fases 0-8 por copia directa del PBIP productivo real, documentado explícitamente) | `Specs/0008_plan_implementacion_correccion_productividad_contexto_negocio.md` | `a1dbb62`, `eaefa0e`, `0d524bd`, `f2aa4d59836b73f5162139cdaa03f51c0da2c766` |
| DATA-010 | Migración de 4 consultas SST a `Accidentalidad_Consolidado.xlsx` corporativo | 2026-07-22 | Migrado y documentado como resultado final | `Specs/0009_actualizacion_origen_datos_sst_sharepoint.md` | No especificado en la spec |
| PBIP-003 | Segmentadores de Área/Cargo en panel Demográfico (Promedio) | 2026-07-29 | Implementado | `Specs/0010_segmentadores_area_cargo_demografico_promedio.md` | No especificado en la spec |
| DAX-001 | Validación de consulta DAX del panel Demográfico (Promedio) | 2026-07-29 | Implementado y validado | `Specs/0011_validacion_consulta_dax_demografico_promedio.md` | No especificado en la spec |
| PBIP-004 | Corrección de segmentadores temporales de Retiros | 2026-07-29 | Validado para versionamiento | `Specs/0012_correccion_segmentadores_temporales_retiros.md` | Archivos versionados: 2 `visual.json`, la spec y `Docs/CHANGELOG.md` (commit no confirmado en la spec) |
| AI-002 | Incorporación de skills oficiales de Power BI (`skills-for-fabric`) | 2026-07-29 | 7 skills vendored instaladas en `.agents/skills/` bajo licencia MIT | `.agents/UPSTREAM.md`, `Docs/POWERBI_CODEX_SKILLS.md` | No especificado en la spec |
| DAX-002 | Renombrar medidas de rotación/retiros (`Ind_Rot`, `Ind_Retiros`, `Rotacion_*_Anual_Acumulada`, `Rotacion_Segun_Tipo`) y crear `Indice_Rotacion` | 2026-08-10 | Cerrado — GATE 5 aprobado por el usuario contra el contexto `Planta Ppto[Ppto/Real]="Real"`; subtotal redundante de `f702a32db8dfea04babc` desactivado; desagregación por Dependencia/Área/Cargo y medida legado `Índice_Retiros` trasladadas a PBIP-005 como iniciativa independiente | `Specs/0016_renombramiento_medidas_rotacion_retiros.md` | Ver historial del PR #5 y Specs/0016 |
| DATA-012 | Adaptar HeadCount/`Consolidado 2025.xlsx` a su nueva estructura y migrar `Consolidado2025`/`PLANTA DE PERSONAL`/`AREAS` a SharePoint corporativo (decisiones A-F) | 2026-08-11 | Cerrado — validado en vivo vía `powerbi-modeling-mcp`: 52 tablas/66 relaciones/122 medidas (0 duplicadas); `PLANTA DE PERSONAL[GENERACIÓN]` contiene únicamente categorías generacionales reales; `EXCEPT` bidireccional contra `Generaciones[Generación]` = 0 diferencias; funnel Generación ordenado de mayor a menor (verificado en el modelo cargado, no solo el JSON); tabla generacional completa; colores LEMCO exactos en "Generación por Antigüedad"; Unión Libre (PR #7) intacta; sin duplicación inline de `Consolidado2025`; deuda de calidad de datos de origen registrada como `DATA-013`, fuera de alcance | `Specs/0019_analisis_impacto_adaptacion_headcount_consolidado2025.md`, `Specs/0020_plan_implementacion_adaptacion_headcount_consolidado2025.md` | Ver historial de la rama `fix/data-012-headcount-generacion-rango-edad` |
| DATA-005 | Migración de `AREAS` a fuente corporativa SharePoint | 2026-08-11 | Cerrado como parte de `DATA-012` (decisión F) — las 3 consultas (`Consolidado2025`, `PLANTA DE PERSONAL`, `AREAS`) migraron juntas a la biblioteca corporativa | `Specs/0019` sección 9.8, `Specs/0020` sección 15.3 | Ver historial de la rama `fix/data-012-headcount-generacion-rango-edad` |

## 11. Componentes reutilizables

| Componente | Ruta | Clasificación | Notas |
|---|---|---|---|
| Auditorías PBIP de solo lectura (`list_pbip_structure`, `audit_navigation`, `audit_semantic_model`, `audit_dax_measures`) | `Tools/pbip/` | Reutilizable directamente | Copiadas desde `04_Aprendizaje_y_Desarrollo/tools/pbip/`; sin dependencias del dominio de negocio, pero **aún no comitedas** en este repositorio |
| Linter de gobierno de skills (`skills_lint.py`) | `Tools/governance/skills_lint.py` | Reutilizable directamente | Ya tracked en este repositorio; valida convenciones genéricas |
| Indexador de `Outputs/` y preparación de commit (`outputs_indexer.py`, `prepare_commit_review.py`) | `Tools/governance/` | Reutilizable mediante configuración — **pendiente de adaptar** | Ver GOV-003: copiados sin adaptar desde el proyecto hermano; requieren ajuste de dominios y rutas de gobierno antes de considerarse confiables aquí |
| Skills propias del proyecto (`outputs-governance`, `pbi-aprendizaje-inventario`, `pbi-commit-prep`, `pbi-dax-measures-audit`, `pbi-navigation-audit`, `pbi-semantic-model-audit`, `powerbi-signals`) | `.agents/skills/` | Reutilizable mediante configuración | Adaptadas parcialmente desde `04_Aprendizaje_y_Desarrollo`; el nombre `pbi-aprendizaje-inventario` conserva vocabulario del proyecto hermano (ver GOV-004) |
| Skills vendored oficiales de Microsoft (`skills-for-fabric`) | `.agents/skills/` (check-updates, powerbi-report-authoring, powerbi-report-design, powerbi-report-management, powerbi-report-planning, semantic-model-authoring), `.agents/common/` | Reutilizable directamente | Mismo paquete y commit de origen (`d79f3393...`) que en `04_Aprendizaje_y_Desarrollo`; mantener sincronizadas vía `check-updates` |
| Suite de validación estática PBIP (`tools/pbip_validation/`) | No presente aún en este repositorio | Candidato a reutilizable mediante configuración | Ver QA-001; existe en Proyecto 4 pero no se ha replicado aquí |
| Informes recurrentes derivados del PBI (`Reports/Recurring/`) | `Reports/Recurring/01_Retiros_y_Rotacion_Manufactura/`, `Reports/Recurring/02_Retiros_y_Rotacion_Muebles/` | Específico del proyecto | Patrón de carpeta (`Current/` + `History/` + `README.md`) replicable como convención, aunque el contenido `.xlsx` es específico y no versionado |
| Prototipo de automatización SharePoint (`open_sharepoint_excel_prototype.py`) | `Tools/automation/` | Específico del proyecto | Experimental, no productivo; URL apunta a la Entrevista Corporativa de Retiro (mismo prototipo que en Proyecto 4, sin confirmar si es copia idéntica) |

## 12. Flujo de una iniciativa

```
Idea
 → evaluación
 → priorización
 → análisis de impacto (Specs/)
 → plan de implementación (Specs/)
 → autorización expresa del usuario
 → desarrollo
 → validación
 → documentación (Docs/ y este roadmap)
 → commit y push
 → cierre con evidencia
```

Ningún paso se salta cuando el usuario ha definido un plan secuencial explícito para la iniciativa (ver `AGENTS.md` y `CLAUDE.md`).

## 13. Historial de actualización del roadmap

| Fecha | Cambio | Iniciativas afectadas | Autor o agente |
|---|---|---|---|
| 2026-08-03 | Validacion del archivo oficial `CONSOLIDADOR_CONTRATOS_V0.0.0.xlsx`: consultas internas apuntan a `Insumos_Vigentes/` en SharePoint corporativo y el refresh del consolidador finaliza sin excepcion; integracion PBIP continua pendiente | DATA-011 | Codex |
| 2026-08-03 | Registro de la iniciativa de gobierno y organización de fuentes de contratos Kactus tras verificar la estructura `Data/Contratos_Kactus/` y documentar su procedimiento operativo | DATA-011 | Codex |
| 2026-07-30 | Creación inicial del roadmap y backlog a partir del estado real del repositorio (AGENTS.md, Docs, Specs, Tools, skills, git status) | Todas las registradas en este documento | Claude Code |
| 2026-08-06 | Registro de DAX-002 (renombramiento de medidas de rotación/retiros y nueva medida `Indice_Rotacion`), en validación pendiente de GATE 5 | DAX-002 | Claude Code |
| 2026-08-10 | Cierre de DAX-002 (GATE 5 aprobado en vivo, subtotal redundante desactivado); registro de PBIP-005 (desagregación por Dependencia/Área/Cargo, incluye deuda funcional de `Índice_Retiros`) como iniciativa independiente pendiente | DAX-002, PBIP-005 | Claude Code |
| 2026-08-10 | Auditoría del PR #5 detectó contaminación de alcance en `Tbl_Medidas.tmdl`/`es-ES.tmdl` (corregida en `b5475ef`) y, al intentar el smoke test post-auditoría, un defecto preexistente de `origin/main`: 27 medidas duplicadas entre tablas de dominio y `Tbl_Medidas` (7 con fórmulas divergentes) que impiden abrir un checkout limpio en Power BI Desktop. Registrada `GOV-005` como iniciativa independiente de saneamiento | DAX-002, GOV-005 | Claude Code |
| 2026-08-10 | Implementación de GOV-005 en rama aislada `fix/gov-005-saneamiento-medidas-duplicadas`: eliminadas las 27 copias redundantes (26 de `Tbl_Medidas`, 1 de `ACCIDENTALIDAD`) preservando fórmula y `lineageTag` de la copia canónica en cada caso. GATE 5 (apertura real en Power BI Desktop desde el checkout limpio) confirmó carga sin `PFE_TM_OBJECT_NAME_ALREADY_EXISTS`: 122 medidas / 66 relaciones / 52 tablas, 0 duplicados en vivo. `GOV-005` cerrada; documentado en `Specs/0018_saneamiento_medidas_duplicadas_gov005.md` | GOV-005 | Claude Code |
| 2026-08-10 | Análisis de impacto de adaptación de HeadCount a la nueva estructura de `Consolidado 2025.xlsx` (68 columnas): recuperado y analizado (sin aplicar) un parche local previo con una regresión de codificación de Unión Libre que no debe reaplicarse; identificada causa probable del error `NIVEL_DE_CARGO` (posible desincronización con la copia SharePoint); confirmado que Árbol de Nómina Nivel 2/3 no tiene homologación inequívoca con Nivel/Tipo de Cargo. Registrada `DATA-012`; documentado en `Specs/0019_analisis_impacto_adaptacion_headcount_consolidado2025.md`, sin implementar | DATA-012 | Claude Code |
| 2026-08-10 | Aprobadas las decisiones A-E y F de `DATA-012` (Generación/Rango de Edad 2025, lógica 2024 sin cambios, Árbol de Nómina Nivel 2/3 y `TIPO_DE_CARGO` fuera de alcance, parche local no reutilizable, migración de fuente OneDrive personal → SharePoint corporativo). Migración de fuente verificada empíricamente vía `powerbi-modeling-mcp` (esquema completo, sin error `NIVEL_DE_CARGO`), aún sin commitear. Consolidada `DATA-005` como absorbida por `DATA-012` para evitar dos iniciativas ejecutando la misma migración de `AREAS`; `DATA-005` no se marca Finalizada porque el cambio no está versionado todavía | DATA-005, DATA-012 | Claude Code |
| 2026-08-11 | Implementación y cierre de `DATA-012` en rama aislada `fix/data-012-headcount-generacion-rango-edad`: migradas las 3 fuentes, corregida la falsa equivalencia Generación/Rango de Edad solo para 2025, agregado `Table.RemoveColumns` para evitar que Power BI reincorpore automáticamente columnas fuera de alcance en cada refresh, corregidas 16 referencias obsoletas de medidas en el bookmark "Generación" y aplicados los colores del Manual de Marca LEMCO. Validado en vivo: 52/66/122 (0 duplicadas), funnel ordenado, tabla generacional completa, Unión Libre intacta. Se auditaron y descartaron en su totalidad (sin portar nada) los cambios manuales exploratorios del working tree principal, incluida la tabla `Planta Ppto`, que quedan fuera del alcance de esta rama. Detectada y registrada como `DATA-013` una deuda de calidad de datos preexistente en la fuente (`#N/A` de Excel en 8 columnas, 6 de ellas fuera de alcance de DATA-012) — no corregida, no bloquea el cierre. `DATA-005` cerrada junto con `DATA-012` | DATA-005, DATA-012, DATA-013 | Claude Code |
| 2026-08-14 | Registrada e implementada `GOV-006`: diagnóstico seguro y de solo lectura de worktrees en cuarentena (`HEAD` en todo-ceros tras fallos repetidos de `git worktree remove --force`-free en carpetas OneDrive), observado 5 veces en la sesión que originó la iniciativa. Implementado `Tools/governance/audit_worktree_quarantine.py` (Python estándar, sin dependencias externas) y la skill `.agents/skills/git-worktree-quarantine-diagnostic/SKILL.md`; documentado en `Specs/0021_diagnostico_worktrees_cuarentena_onedrive.md`. Probado contra el corpus de 5 worktrees en cuarentena conocidos más un control sano. Alcance exclusivamente diagnóstico: el script no elimina, repara ni modifica nada; un resultado `SAFE_TO_INVESTIGATE_MANUAL_REMOVAL` no autoriza eliminación automática. `GOV-006` queda `En validación`, no `Finalizada`, hasta acumular uso repetido en producción | GOV-006 | Claude Code |
| 2026-08-26 | Cierre documental de la actualización manual de julio 2026 en `Retiros_y_Rotacion_Manufactura.xlsx`: Colaboradores recalculados desde `Consolidado 2025.xlsx` y Retiros desde `PptovsReal.xlsx`/`RETIROS` aplicando la regla de exclusión ya aprobada en `Specs/0016`; reconciliación exacta contra enero-junio 2026 en 13 de 14 áreas (única excepción: discrepancia histórica preexistente en Mantenimiento Refrigeración de junio, documentada sin corregir); homologación de Dependencia/Área de julio completada por el usuario mediante cruce por `CARGO_CCO` y una regla manual de prefijo no gobernada, específica de este corte. Resultado final julio: 720/36 (Dirección de Manufactura), 150/5 (Gerencia Cadena Muebles Laminados), 870/41 (total). Documentado en `Specs/0023_cierre_actualizacion_manual_retiros_rotacion_manufactura_julio_2026.md`; registrada `DATA-014` (automatización mensual futura, diferida, no autorizada) | DATA-014 | Claude Code |
| 2026-08-26 | Corrección histórica del corte enero-julio 2026 en `Retiros_y_Rotacion_Manufactura.xlsx`, motivada por la completitud posterior de `Dependencia`/`Área` en `PptovsReal.xlsx` para meses anteriores a julio. Recalculadas 98 combinaciones (14 áreas × 7 meses); 18 diferencias corregidas, concentradas en marzo-junio (enero, febrero y julio sin cambios); reconciliación final en 0 diferencias residuales. Resuelta la discrepancia histórica de Mantenimiento Refrigeración/junio (0 → 1). Confirmados 9 retiros válidos en sub-áreas de Gerencia Cadena Muebles Laminados fuera de las 14 áreas del reporte (Almacén, Centro de Distribución, Constructores Instalación, I+D Muebles); quedan fuera del alcance funcional del reporte por decisión del usuario, no como pendiente de incorporar. Documentado en `Specs/0023_cierre_actualizacion_manual_retiros_rotacion_manufactura_julio_2026.md`, sección "Corrección histórica posterior". `DATA-014` sigue diferida y no autorizada | DATA-014 | Claude Code |
| 2026-08-26 | Registrada `PBIP-006`: nueva página `Sociodemográfico por Empresa`, aislada en rama `feat/sociodemografico-por-empresa` (worktree `.wt/sociodemografico-por-empresa` desde `origin/main`). Validada en modo lectura la dimensión `Empresas` (`Empresas[Empresas]`, `Empresas[Grupo Empresa]`) y sus relaciones con `PLANTA DE PERSONAL['Nombre Empresa']` y `'Grupo Empresarial'`, sin modificarlas. Capturada línea base manual (`pbip_triage` no existe en este repositorio) en `Outputs/sociodemografico_por_empresa_baseline_2026-08-26.json`. El usuario duplicó manualmente `Demográfico (Promedio)` en Power BI Desktop y la renombró; comparación SHA-256 completa contra la línea base clasificó 21 archivos modificados y 35 agregados: único `FUNCTIONAL_CHANGE` es la página nueva (31 visuales, registro en `pages.json`); el resto es `RESERIALIZATION` verificada (migración de schema de bookmarks con limpieza de referencias a visuales ya inexistentes, metadata de Q&A, espacios en blanco en TMDL, posición de scroll del diagrama, saltos de línea) — sin cambios funcionales en `Demográfico (Promedio)` ni en el modelo/relaciones | PBIP-006 | Claude Code |
| 2026-08-27 | Checkpoint pre-corrección de `PBIP-006`: implementados 7 comparativos por `PLANTA DE PERSONAL[GRUPO EMPRESA]` (Colaboradores, Tipo de Contrato, Generación, Tipo de Cargo, Distribución de Género, Antigüedad, Matriz Empresa/Dependencia/Cargo — esta última sin columna `%`, retirada por representar participación sobre el total general en vez de dentro de cada empresa, sin crear medida nueva); retirado `Generación por Antigüedad` de esta página por no comparar por empresa; los 9 slicers consolidados en una sola fila. Validado sin `(En blanco)` en sesión interactiva de Power BI Desktop por el usuario — no se documenta Formula Firewall ni diferencias de mayúsculas como causa raíz demostrada de nada, no fue necesario diagnosticar una causa. Estado visual/funcional preservado en commit y push a `feat/sociodemografico-por-empresa`; staging selectivo excluyó los ~20 archivos de `RESERIALIZATION` heredada (bookmarks, `Demográfico (Promedio)`, TMDL, DAX, cultures) verificados sin cambio de contenido. Implementación **no finalizada**: el usuario detiene el desarrollo en este punto para aplicar una corrección posterior a partir de este checkpoint | PBIP-006 | Claude Code |
