# Spec 0001 — Plan de implementación: gobernanza, trazabilidad y arquitectura del proyecto PBIP

> Estado: Propuesto — pendiente de aprobación por fase. Ningún cambio técnico se ejecuta con la creación de este documento.
> Fecha: 2026-07-03. Autor del análisis: Claude Code, a partir de diagnósticos ya aprobados por el usuario.
> Primera Spec formal del proyecto — ver `Docs/ESTRUCTURA_PROYECTO.md` sección 6 y 14 para el criterio de adopción de `Specs/`.

---

## 1. Título

Plan de implementación por fases: cierre de gobernanza documental y de Git, evaluación de riesgos de datos, diagnóstico del PBIP pendiente, y hoja de ruta hacia cambios de mayor impacto (seguridad, escalabilidad, expansión a Desarrollo Organizacional).

---

## 2. Objetivo

Convertir los hallazgos ya diagnosticados y aprobados en un plan de implementación **seguro, por fases pequeñas, con aprobación explícita en cada una**, que:

1. Cierre lo que ya está en curso (sincronización Git, correcciones documentales menores).
2. Resuelva los vacíos de gobernanza pendientes (`AGENTS.md`, `README.md`, PII de `Inputs/`).
3. Diagnostique — sin decidir todavía — los 199 cambios pendientes de `PBIP/`.
4. Deje documentado, pero **no ejecutado**, el camino hacia los cambios de mayor impacto (RLS, cuenta de servicio, parametrización, `Dim_Fecha`, encoding, expansión a competencias/desempeño/sucesión).

---

## 3. Alcance

- Planificación documental de las 7 fases descritas en la sección 11.
- Consolidación de hallazgos ya verificados en `Outputs/00` a `Outputs/05` y en `Docs/`.
- Definición de criterios de aceptación, validaciones, estrategia de commit y rollback para cada fase.
- Clasificación de candidatos a subagentes de Claude Code (sección 18), sin crear ninguno.

---

## 4. Fuera de alcance

- Ejecutar cualquier cambio técnico sobre `PBIP/`, `Docs/`, `Inputs/`, `Data/`, `README.md`, `AGENTS.md`, `CLAUDE.md` o `.gitignore`.
- Diagnosticar en detalle los 199 archivos de `PBIP/` (eso es la Fase 6 misma; aquí solo se planifica cómo hacerlo).
- Implementar RLS, parametrización de Power Query, `Dim_Fecha`, corrección de encoding, o cualquier expansión de modelo (Fase 7 completa: solo se documenta el plan, no se ejecuta nada).
- Crear subagentes o archivos en `.claude/agents/`.
- Evaluar contenido de la Papelera de Reciclaje o cualquier ubicación fuera del repositorio.
- Hacer push de esta Spec (queda pendiente de aprobación explícita, igual que cualquier otro documento).

---

## 5. Diagnósticos usados como entrada

| Fuente | Contenido relevante | Estado |
|---|---|---|
| `Outputs/00_2026-07-03_preflight_git.md` | Estado inicial de Git, identidad, remote, riesgos de sincronización | Local, no versionado |
| `Outputs/01_2026-07-03_diagnostico_codebase.md` | Mapa general del repositorio, primer inventario de brechas | Local, no versionado |
| `Outputs/02_2026-07-03_revision_claude_md.md` | Corrección de datos obsoletos en `CLAUDE.md` (52 tablas, 20 bookmarks — este último ya identificado como pendiente de re-corrección, ver Fase 2) | Local, no versionado |
| `Outputs/03_2026-07-03_auditoria_docs_y_trazabilidad.md` | Auditoría completa de `Docs/`: 9 de 10 documentos sin versionar (ya resuelto), páginas inexistentes en `BI_GUIDELINES.md`, referencias a `Proyecto.pbip` | Local, no versionado |
| `Outputs/04_2026-07-03_saneamiento_docs.md` | Evidencia de las correcciones aplicadas a `Docs/` y el `.gitignore`; incluye la corrección del error de conteo de bookmarks (20→19, verificado con `bookmarks.json`) | Local, no versionado |
| `Outputs/05_2026-07-03_analisis_arquitectura_actual.md` | Análisis de arquitectura PBIP + documental en solo lectura. **Fuente de las 2 discrepancias nuevas** (66 vs. 41 relaciones, 100 vs. 88 medidas), riesgos de rutas hardcodeadas, ausencia de RLS confirmada por estructura, y la conexión con la estrategia de People Analytics 2026–2028 | Local, no versionado |
| `Docs/ESTRUCTURA_PROYECTO.md` | Estándar corporativo de carpetas, política documental, matriz de actualización por tipo de cambio (sección 18) | Versionado (`0cb85bf`, `936bfa8`, `5ffdb24`) |
| `CLAUDE.md` | Instrucciones de Claude Code para el proyecto | Versionado (`cd300b7`) |
| `Docs/README.md`, `DATA_MODEL.md`, `METRICS_CATALOG.md`, `DATA_PIPELINE.md`, `SECURITY_AND_PRIVACY.md`, `RUNBOOK.md`, `CHANGELOG.md`, `decisions/README.md` | Documentación oficial vigente, saneada en esta sesión | Versionados (`d67c8f0`) |
| `AGENTS.md` | Reglas para agentes de IA | **Sin versionar** — leído solo como referencia en esta Spec |

---

## 6. Estado actual resumido

- `Docs/` está saneado y versionado (12 documentos, commit `d67c8f0`). `CLAUDE.md` versionado (`cd300b7`). `.gitignore` protege `Inputs/*` y el PDF de marca (128 MB).
- `origin/main` está sincronizado con `HEAD` hasta el commit `d67c8f0` (verificado en la tarea anterior).
- `AGENTS.md` sigue sin versionar.
- `README.md` (raíz) sigue sin reflejar el estado actual de `Docs/` ni referenciar `Docs/ESTRUCTURA_PROYECTO.md`.
- `Inputs/Base_Rotacion_Atraccion_Seleccion.xlsx` sigue sin evaluar por PII (protegido de versionamiento accidental, pero no evaluado).
- `PBIP/` tiene 199 archivos modificados sin diagnóstico — no tocado desde el inicio de esta línea de trabajo.
- `Specs/` no existía antes de este documento — esta es la primera Spec del proyecto.
- Dos discrepancias verificadas y **no corregidas todavía**: `Docs/DATA_MODEL.md` documenta 41 relaciones (el modelo real tiene 66) y `Docs/METRICS_CATALOG.md`/`CLAUDE.md` documentan 88 medidas (el modelo real tiene 100). `CLAUDE.md` además sigue diciendo "20 bookmarks" (el dato correcto, ya verificado y aplicado en `Docs/BI_GUIDELINES.md`, es 19).
- Riesgos estructurales confirmados y sin resolver: sin RLS (confirmado por ausencia de carpeta de roles en el PBIP), 20 tablas con rutas de SharePoint personales hardcodeadas, 18 `LocalDateTable` sin consolidar, encoding roto en la columna `GENERACIÓN` (ADR-007), 5 páginas ocultas sin decisión (ADR-005).
- No existe ninguna tabla ni fuente de datos para competencias, desempeño, mapa de talento o sucesión.

---

## 7. Problemas detectados

| # | Problema | Fuente | Severidad |
|---|---|---|---|
| P1 | `AGENTS.md` sin versionar | Outputs/01, 03, 04, 05 | Media |
| P2 | `README.md` raíz desactualizado frente a `Docs/` | Outputs/01, 03, 05 | Media |
| P3 | `Inputs/` sin evaluar por PII | Outputs/01, 03, 04, 05; `Docs/SECURITY_AND_PRIVACY.md` | Alta |
| P4 | 199 archivos de `PBIP/` modificados sin diagnóstico | Outputs/00, 01, 05 | Alta |
| P5 | `Docs/DATA_MODEL.md`: 41 relaciones documentadas vs. 66 reales | Outputs/05 (verificado con `grep` sobre `relationships.tmdl`) | Media |
| P6 | `Docs/METRICS_CATALOG.md` y `CLAUDE.md`: 88 medidas documentadas vs. 100 reales | Outputs/05 (verificado con `grep` sobre `Tbl_Medidas.tmdl`) | Media |
| P7 | `CLAUDE.md`: 20 bookmarks documentados vs. 19 reales | Outputs/02, 04 (corrección ya aplicada en `Docs/BI_GUIDELINES.md`, pendiente en `CLAUDE.md`) | Baja |
| P8 | Sin Row-Level Security | ADR-006; Outputs/05 (confirmado por ausencia de carpeta de roles) | Alta |
| P9 | 20 tablas con rutas de SharePoint personales hardcodeadas, sin parámetros | `Docs/DATA_PIPELINE.md`; Outputs/05 | Alta |
| P10 | 18 `LocalDateTable` sin consolidar (riesgo de rendimiento) | `Docs/DATA_MODEL.md` riesgo R1 | Media |
| P11 | Encoding roto en columna `GENERACIÓN` | ADR-007 | Media |
| P12 | 5 páginas ocultas sin decisión de conservar/eliminar | ADR-005 | Baja-Media |
| P13 | Sin gobernanza de datos formal (Ley 1581, ownership, límites de uso en modelos predictivos) | `Docs/SECURITY_AND_PRIVACY.md`; Outputs/05 | Alta (riesgo emergente) |
| P14 | Sin datos ni modelo para competencias, desempeño, mapa de talento, sucesión | Outputs/05 sección 7 | Alta (brecha estratégica, no defecto) |
| P15 | `Data/` vacía sin explicación completa de qué pasó con su contenido histórico | `Docs/PROJECT_CONTEXT.md` (ya documentado como `Pendiente de confirmar`) | Baja |

---

## 8. Análisis de impacto

- **P1–P7 (gobernanza y documentación)**: impacto bajo-medio, totalmente reversible, no tocan `PBIP/`. Pueden ejecutarse en cualquier orden entre sí, pero se recomienda el orden de la sección 19 porque cada corrección reduce el riesgo de que la siguiente se base en datos desactualizados.
- **P3 (Inputs/ PII)**: impacto medio técnico, pero **alto si se maneja mal** — cualquier artefacto generado durante la evaluación (Outputs, mensajes) podría exponer datos personales si no se tiene cuidado. Debe ejecutarse citando solo estructura (columnas), nunca valores.
- **P4 (199 cambios PBIP)**: es el **punto de mayor impacto potencial de todo el plan a corto plazo**. Decidir mal (conservar cambios no intencionales o descartar trabajo real) afecta directamente el reporte que usan las áreas de Talento Humano. Bloquea toda la Fase 7 — ningún cambio de mayor impacto debe tocar `PBIP/` mientras su estado sea ambiguo.
- **P8–P12 (cambios de modelo)**: impacto alto individualmente, cada uno toca el modelo semántico o el reporte en producción. Requieren Spec propia, no se ejecutan con esta Spec.
- **P13–P14 (gobernanza de datos y expansión estratégica)**: impacto organizacional, no solo técnico. P14 en particular es la mayor expansión de alcance posible del proyecto — depende de decisiones que no son solo del equipo de datos (fuentes de Desarrollo Organizacional que hoy no existen documentadas).
- **Interdependencias críticas**: P8 (RLS) debería resolverse **antes** de cualquier avance hacia P14 (competencias/desempeño/sucesión), porque agregar datos aún más sensibles sobre un modelo sin control de acceso multiplica el riesgo de privacidad en vez de mitigarlo. Esta secuencia ya se refleja en la priorización pedida para esta Spec.

---

## 9. Priorización de riesgos

| Prioridad | Riesgo | Por qué primero/después |
|---|---|---|
| 1 | P4 — 199 cambios PBIP sin diagnóstico | Bloquea toda la Fase 7; cada día que pasa sin diagnóstico aumenta la probabilidad de perder contexto sobre qué cambió y por qué |
| 2 | P3 — Inputs/ sin evaluar PII | Riesgo de privacidad activo aunque ya mitigado parcialmente por `.gitignore` |
| 3 | P8 — Sin RLS | El riesgo de privacidad más severo del modelo ya publicado/en uso, pero es un cambio de alto impacto que requiere Spec propia (no se resuelve en esta Spec) |
| 4 | P9 — Rutas hardcodeadas / dependencia de 2 cuentas personales | Riesgo de continuidad operativa; también de alto impacto, Spec propia |
| 5 | P13 — Gobernanza de datos formal | Prerrequisito organizacional para P14; no bloquea el resto del plan pero sí bloquea cualquier avance hacia analítica predictiva |
| 6 | P1, P2, P5, P6, P7 — Brechas documentales | Bajo riesgo individual, pero acumulan deuda de confianza en la documentación si no se cierran pronto |
| 7 | P10, P11, P12 — Deuda técnica del modelo (LocalDateTable, encoding, páginas ocultas) | Riesgo medio, no urgente, pero cada una requiere su propia Spec cuando se aborde |
| 8 | P14 — Expansión a competencias/desempeño/sucesión | Mayor valor estratégico, pero también mayor riesgo si se adelanta sin P8 y P13 resueltos primero |
| 9 | P15 — `Data/` vacía sin explicar | Bajo riesgo, informativo |

---

## 10. Propuesta de solución

Ejecutar el plan en **7 fases secuenciales**, cada una con su propio commit y aprobación explícita, siguiendo el principio ya establecido en `Docs/ESTRUCTURA_PROYECTO.md`: ningún commit mezcla `Docs/`/`Outputs/`/`Specs/` con `PBIP/`, y ninguna migración estructural se ejecuta sin una Spec de migración dedicada con análisis de impacto, validaciones y plan de rollback propios.

Las fases 1 a 5 son de bajo riesgo (documentales/gobernanza) y pueden aprobarse y ejecutarse con relativa rapidez. La fase 6 (diagnóstico de `PBIP/`) es el punto de control obligatorio antes de cualquier cambio técnico. La fase 7 no se ejecuta con esta Spec — cada una de sus 6 subfases requerirá su propia Spec futura (`0002`, `0003`, ...) una vez la fase 6 esté cerrada.

---

## 11. Plan de implementación por fases

### Fase 1 — Cerrar sincronización Git y trazabilidad

- **Objetivo:** dejar registrado formalmente, en la primera Spec del proyecto, que la sincronización Git y la trazabilidad documental están al día antes de continuar.
- **Archivos/carpetas afectados:** `Specs/0001_...md` (este documento), `Outputs/06_...md`.
- **Tareas:** crear esta Spec; verificar que no hay commits pendientes de sincronizar fuera de lo ya conocido (`PBIP/`, que se trata aparte en la Fase 6).
- **Riesgos:** bajo — es documentación, no cambio técnico.
- **Dependencias:** ninguna.
- **Validaciones técnicas:** `git log origin/main..HEAD` y `git log HEAD..origin/main` revisados antes de cerrar la fase.
- **Documentación que debe actualizarse:** ninguna adicional — esta Spec es el registro.
- **Criterio de aceptación:** Spec creada, revisada y comiteada; `git status` sin sorpresas fuera de lo esperado.
- **Estrategia de commit:** 1 commit dedicado exclusivamente a esta Spec.
- **¿Requiere aprobación explícita?:** Sí — antes del commit de esta Spec.

### Fase 2 — Ajustes documentales menores

- **Objetivo:** corregir P5, P6 y P7 (relaciones, medidas, bookmarks en `CLAUDE.md`).
- **Archivos/carpetas afectados:** `Docs/DATA_MODEL.md`, `Docs/METRICS_CATALOG.md`, `CLAUDE.md`.
- **Tareas:** reconfirmar los conteos con `grep` sobre `relationships.tmdl` y `Tbl_Medidas.tmdl` (no reutilizar de memoria sin verificar de nuevo, por si `PBIP/` cambió); actualizar los 3 documentos; agregar entrada en `Docs/CHANGELOG.md`.
- **Riesgos:** bajo — solo texto documental, sin tocar `PBIP/`.
- **Dependencias:** ninguna.
- **Validaciones técnicas:** `git diff --check`; confirmar que los 3 documentos quedan consistentes entre sí tras el cambio.
- **Documentación que debe actualizarse:** `Docs/CHANGELOG.md` (entrada de corrección, según matriz de `Docs/ESTRUCTURA_PROYECTO.md` sección 18).
- **Criterio de aceptación:** los conteos de relaciones, medidas y bookmarks coinciden en `Docs/` y `CLAUDE.md` con el modelo real verificado ese mismo día.
- **Estrategia de commit:** 1 commit dedicado, separado de cualquier otro cambio.
- **¿Requiere aprobación explícita?:** Sí.

### Fase 3 — Versionar o revisar AGENTS.md

- **Objetivo:** resolver P1 — decidir si `AGENTS.md` se versiona ahora o si necesita un ajuste antes.
- **Archivos/carpetas afectados:** `AGENTS.md`.
- **Tareas:** releer `AGENTS.md` contra el estado actual del proyecto (¿sigue vigente tras todos los cambios de gobernanza de esta sesión?); confirmar que no contradice `CLAUDE.md` ni `Docs/ESTRUCTURA_PROYECTO.md`; versionar.
- **Riesgos:** bajo — contenido ya revisado en sesiones anteriores, sin secretos ni rutas locales.
- **Dependencias:** ninguna.
- **Validaciones técnicas:** `git diff --check`; confirmar coherencia con `CLAUDE.md`.
- **Documentación que debe actualizarse:** `Docs/CHANGELOG.md`.
- **Criterio de aceptación:** `AGENTS.md` versionado, o decisión explícita documentada de por qué no (si se detecta algo que corregir primero).
- **Estrategia de commit:** 1 commit dedicado ("Reglas de IA", según matriz de `Docs/ESTRUCTURA_PROYECTO.md` sección 18).
- **¿Requiere aprobación explícita?:** Sí.

### Fase 4 — Actualizar README.md raíz

- **Objetivo:** resolver P2 — que el punto de entrada del repositorio refleje el estado actual.
- **Archivos/carpetas afectados:** `README.md`.
- **Tareas:** actualizar la sección "Estructura del repositorio" y el estado de versionamiento; referenciar `Docs/ESTRUCTURA_PROYECTO.md`.
- **Riesgos:** bajo técnicamente, pero es el archivo más visible del repositorio — cualquier imprecisión se nota.
- **Dependencias:** se recomienda ejecutar después de la Fase 2, para que `README.md` no herede los conteos ya identificados como incorrectos.
- **Validaciones técnicas:** confirmar que el árbol de carpetas mostrado coincide con la estructura real verificada (`Docs/`, `Inputs/`, `Outputs/`, `Data/`, `PBIP/`, `Specs/` ya creada con esta Spec).
- **Documentación que debe actualizarse:** `Docs/CHANGELOG.md`.
- **Criterio de aceptación:** `README.md` sin contradicciones frente a `Docs/ESTRUCTURA_PROYECTO.md`.
- **Estrategia de commit:** 1 commit dedicado.
- **¿Requiere aprobación explícita?:** Sí (instrucción transversal ya vigente en varias tareas anteriores de no tocar `README.md` sin autorización).

### Fase 5 — Evaluar Inputs/ por PII sin exponer valores individuales

- **Objetivo:** resolver P3 — confirmar si `Inputs/Base_Rotacion_Atraccion_Seleccion.xlsx` contiene datos personales.
- **Archivos/carpetas afectados:** ninguno se modifica directamente; el resultado se documenta en `Docs/SECURITY_AND_PRIVACY.md`.
- **Tareas:** inspeccionar únicamente encabezados/nombres de columna del archivo (nunca valores individuales); clasificar como PII o no; actualizar `Docs/SECURITY_AND_PRIVACY.md` con el resultado y la fecha.
- **Riesgos:** medio — manejo de un archivo con datos potencialmente sensibles; el riesgo real es que algún artefacto generado (este mismo proceso, un Output) termine citando un valor individual por error.
- **Dependencias:** ninguna técnica.
- **Validaciones técnicas:** revisión de que ningún documento generado en esta fase cita valores individuales, solo nombres de columna y una conclusión (sí/no contiene PII).
- **Documentación que debe actualizarse:** `Docs/SECURITY_AND_PRIVACY.md`, `Docs/CHANGELOG.md`.
- **Criterio de aceptación:** `Docs/SECURITY_AND_PRIVACY.md` pasa de "sin evaluar" a un estado concluyente, con fecha.
- **Estrategia de commit:** 1 commit dedicado.
- **¿Requiere aprobación explícita?:** Sí — por tratarse de datos potencialmente sensibles.

### Fase 6 — Diagnosticar los 199 cambios pendientes de PBIP/

- **Objetivo:** resolver P4 — determinar cuáles de los 199 archivos modificados son cambios reales y cuáles son reescritura de Power BI Desktop, **sin decidir todavía si se conservan o descartan** (esa decisión es un paso separado, posterior a esta fase, con aprobación propia).
- **Archivos/carpetas afectados:** `PBIP/` — **solo lectura/diagnóstico en esta fase, ninguna modificación.**
- **Tareas:** `git diff` selectivo sobre una muestra representativa por tipo (bookmarks, `visual.json`, tablas `.tmdl`); clasificar cada tipo de cambio (¿reescritura de metadatos vs. cambio de contenido real?); confirmar con el usuario si Power BI Desktop estuvo abierto recientemente y con qué propósito; producir un diagnóstico dedicado en `Outputs/`.
- **Riesgos:** alto — es la fase de mayor riesgo de pérdida de trabajo de todo el plan si se decide mal después. El diagnóstico en sí (esta fase) es de bajo riesgo porque no modifica nada; el riesgo está en la decisión posterior de conservar/descartar.
- **Dependencias:** ninguna técnica de las fases 1-5, pero es **prerrequisito obligatorio de toda la Fase 7**.
- **Validaciones técnicas:** revisión manual de una muestra de diffs por el usuario antes de cualquier decisión de conservar/descartar.
- **Documentación que debe actualizarse:** nuevo archivo en `Outputs/` con el diagnóstico; `Docs/CHANGELOG.md` una vez se resuelva la decisión de conservar/descartar (no en esta fase, que es solo diagnóstico).
- **Criterio de aceptación:** existe un diagnóstico claro, archivo por archivo o por grupo, de qué tipo de cambio es cada uno, y el usuario tiene información suficiente para decidir.
- **Estrategia de commit:** ninguno en esta fase (es solo diagnóstico, sin cambios). La decisión posterior de conservar/descartar tendrá su propia estrategia de commit (commits separados por tipo de cambio si se conservan; `git restore`/`git checkout` explícito y confirmado si se descartan).
- **¿Requiere aprobación explícita?:** Sí — tanto para iniciar el diagnóstico como, de forma separada y más estricta, para la decisión posterior de conservar o descartar cambios.

### Fase 7 — Cambios de mayor impacto (solo después de que la Fase 6 esté cerrada)

Cada subfase requiere su propia Spec de migración (`0002`, `0003`, ...) antes de ejecutarse — esta Spec 0001 solo las documenta como plan, no las autoriza.

#### 7.1 — Parametrización de rutas Power Query

- **Objetivo:** resolver P9 — eliminar rutas de SharePoint hardcodeadas en las 20 tablas identificadas.
- **Archivos/carpetas afectados:** 20 tablas `.tmdl`, `model.tmdl` (parámetros nuevos).
- **Tareas:** definir parámetros de Power Query para las URLs base; actualizar el código M de las 20 tablas para referenciarlos.
- **Riesgos:** alto — puede romper la carga de datos si algún parámetro queda mal referenciado.
- **Dependencias:** Fase 6 cerrada; idealmente en conjunto con 7.3 (misma raíz de acceso a datos).
- **Validaciones técnicas:** actualizar el modelo completo en Power BI Desktop, cero errores en las 20 tablas.
- **Documentación que debe actualizarse:** Spec de migración dedicada, `Docs/DATA_PIPELINE.md`, ADR nuevo.
- **Criterio de aceptación:** ninguna tabla tiene una URL literal en su código M; todas usan parámetros.
- **Estrategia de commit:** 1 commit dedicado, después de validación completa en Power BI Desktop.
- **¿Requiere aprobación explícita?:** Sí, con Spec de migración aprobada primero.

#### 7.2 — Row-Level Security (RLS)

- **Objetivo:** resolver P8 — controlar el acceso a datos nominales por empresa/grupo empresarial.
- **Archivos/carpetas afectados:** nuevo(s) rol(es) en `PBIP/Proyecto.SemanticModel/definition/`, configuración en Power BI Service.
- **Tareas:** definir el modelo de roles (por empresa, por grupo, o mixto — decisión de negocio pendiente); implementar reglas DAX de filtrado; asignar usuarios a roles en el servicio.
- **Riesgos:** alto — mal implementado, puede ocultar datos a quien sí debería verlos o exponerlos a quien no debería.
- **Dependencias:** Fase 6 cerrada; decisión de negocio previa sobre el modelo de roles.
- **Validaciones técnicas:** pruebas de "Ver como rol" para cada perfil definido, antes de publicar.
- **Documentación que debe actualizarse:** ADR-006 (cerrar como "Implementado"), `Docs/SECURITY_AND_PRIVACY.md`, Spec de migración dedicada.
- **Criterio de aceptación:** cada rol ve únicamente los datos que le corresponden, verificado antes de publicar al servicio.
- **Estrategia de commit:** 1 commit dedicado, después de pruebas de rol completas.
- **¿Requiere aprobación explícita?:** Sí, con Spec de migración aprobada primero — es el cambio de mayor sensibilidad de privacidad del plan.

#### 7.3 — Cuenta de servicio

- **Objetivo:** resolver parte de P9 — eliminar la dependencia de las 2 cuentas personales de SharePoint.
- **Archivos/carpetas afectados:** gestión externa (Power BI Service / gateway, fuera del repositorio), `Docs/DATA_PIPELINE.md`, `Docs/RUNBOOK.md`.
- **Tareas:** solicitar cuenta de servicio a TI/Microsoft 365; migrar el sitio de origen de los archivos Excel a un sitio SharePoint de equipo; actualizar credenciales en Power BI Desktop/Service.
- **Riesgos:** alto — depende de recursos organizacionales fuera del control directo del proyecto.
- **Dependencias:** Fase 6 cerrada; se recomienda ejecutar junto con 7.1 por tocar la misma raíz de acceso a datos.
- **Validaciones técnicas:** refresh completo exitoso con las nuevas credenciales antes de descontinuar las personales.
- **Documentación que debe actualizarse:** ADR nuevo, `Docs/DATA_PIPELINE.md`, `Docs/RUNBOOK.md`.
- **Criterio de aceptación:** el modelo se actualiza sin depender de ninguna credencial personal.
- **Estrategia de commit:** 1 commit dedicado a la documentación (el cambio de credenciales en sí ocurre fuera del repositorio, en Power BI Service).
- **¿Requiere aprobación explícita?:** Sí.

#### 7.4 — Dim_Fecha (consolidar 18 LocalDateTable)

- **Objetivo:** resolver P10 — reducir el riesgo de rendimiento de las tablas de calendario locales autogeneradas.
- **Archivos/carpetas afectados:** `model.tmdl`, `relationships.tmdl`, múltiples tablas `.tmdl`.
- **Tareas:** crear una tabla `Dim_Fecha` compartida; migrar las relaciones de columnas de fecha de las 18 `LocalDateTable` hacia la nueva dimensión.
- **Riesgos:** alto — puede romper medidas de inteligencia de tiempo existentes.
- **Dependencias:** Fase 6 cerrada; Spec de migración dedicada.
- **Validaciones técnicas:** pruebas de todas las medidas de inteligencia de tiempo antes y después del cambio.
- **Documentación que debe actualizarse:** Spec de migración, ADR nuevo, `Docs/DATA_MODEL.md`.
- **Criterio de aceptación:** cero `LocalDateTable` autogeneradas remanentes; todas las medidas de tiempo funcionan igual o mejor que antes.
- **Estrategia de commit:** 1 commit dedicado, después de pruebas completas.
- **¿Requiere aprobación explícita?:** Sí, con Spec de migración aprobada primero.

#### 7.5 — Corrección de encoding en GENERACIÓN

- **Objetivo:** resolver P11 (ADR-007) — corregir `GENERACI&#211;N` a `GENERACION` en el nombre de columna fuente.
- **Archivos/carpetas afectados:** `relationships.tmdl`, `PLANTA DE PERSONAL.tmdl`.
- **Tareas:** renombrar la columna fuente; actualizar la relación hacia `Generaciones`; verificar todas las medidas y visuales que la referencian.
- **Riesgos:** medio — es un cambio de nombre de columna, puede romper referencias no evidentes a simple vista.
- **Dependencias:** Fase 6 cerrada.
- **Validaciones técnicas:** `grep` de todas las referencias a la columna en medidas y `visual.json` antes y después del cambio.
- **Documentación que debe actualizarse:** ADR-007 (cerrar como "Implementado"), `Docs/CHANGELOG.md`.
- **Criterio de aceptación:** ninguna referencia rota; el TMDL ya no contiene entidades HTML en nombres de columna.
- **Estrategia de commit:** 1 commit dedicado, después de validar todas las referencias.
- **¿Requiere aprobación explícita?:** Sí.

#### 7.6 — Expansión a competencias, desempeño, mapa de talento y sucesión

- **Objetivo:** resolver P14 — construir la capa de datos que hoy no existe para estos dominios de Desarrollo Organizacional.
- **Archivos/carpetas afectados:** nuevas tablas en `PBIP/Proyecto.SemanticModel/`, nuevas fuentes de datos (no identificadas todavía), posiblemente nuevo grupo de consulta.
- **Tareas:** identificar fuentes de datos existentes de Desarrollo Organizacional (hoy no documentadas en `Docs/DATA_PIPELINE.md`); diseñar el modelo de datos; definir gobernanza de acceso antes de cargar cualquier dato.
- **Riesgos:** alto — es la mayor expansión de alcance de todo el plan, sobre datos de altísima sensibilidad (mapa de talento y sucesión son información individual crítica).
- **Dependencias:** **depende explícitamente de 7.2 (RLS) y de P13 (gobernanza de datos formal) resueltos primero.** No debe iniciarse antes, por el riesgo señalado en la sección 8.
- **Validaciones técnicas:** modelo de datos revisado por el área de Desarrollo Organizacional antes de construir cualquier tabla.
- **Documentación que debe actualizarse:** Spec de migración dedicada (la más extensa del plan), `Docs/PROJECT_CONTEXT.md` (nuevo dominio), `Docs/DATA_MODEL.md`, múltiples ADRs.
- **Criterio de aceptación:** modelo de datos aprobado formalmente por Desarrollo Organizacional antes de cualquier implementación técnica.
- **Estrategia de commit:** múltiples commits pequeños por tabla/fuente, cada uno con su propia validación — nunca un solo commit masivo para toda la expansión.
- **¿Requiere aprobación explícita?:** Sí — la de mayor exigencia de todo el plan, incluyendo revisión legal/de gobernanza antes de tocar cualquier archivo.

---

## 12. (Contenido de cada fase — ver sección 11, integrado por fase según lo solicitado)

---

## 13. Criterios de aceptación generales

- Ningún commit combina archivos de `Docs/`/`Outputs/`/`Specs/` con archivos de `PBIP/`.
- Cada fase tiene exactamente un commit dedicado (salvo la Fase 6, que no genera commit por ser solo diagnóstico, y la Fase 7.6, que se divide en varios commits pequeños por tabla).
- Ninguna fase de la sección 7 inicia sin que la Fase 6 esté formalmente cerrada y su resultado documentado.
- Ninguna fase se ejecuta sin aprobación explícita previa, incluyendo esta misma Spec.
- `git status --short` no muestra cambios inesperados después de cada fase — solo lo que esa fase debía tocar.

---

## 14. Validaciones técnicas generales

- `git status --short` y `git diff --check` antes y después de cada fase.
- Verificación de identidad Git (`EdwinClavijoChallenger <edwin.clavijo@challenger.co>`) antes de cada commit.
- Para cambios que toquen `PBIP/` (fases 6 y 7): apertura en Power BI Desktop y actualización completa del modelo sin errores, antes de comitear.
- Para cambios en `Docs/`: coherencia cruzada verificada contra la matriz de `Docs/ESTRUCTURA_PROYECTO.md` sección 18 ("Criterio de actualización documental por cambio").
- Para cualquier conteo citado en documentación (tablas, relaciones, medidas, páginas, bookmarks): reverificar con el comando correspondiente (`ls`, `grep -c`) en el momento del cambio, nunca reutilizar un número de una sesión anterior sin confirmar.

---

## 15. Plan de rollback

- **Fases 1–5 (documentales):** revertir con `git revert <commit>` del commit específico de la fase. Bajo riesgo, siempre reversible sin pérdida de datos.
- **Fase 6 (diagnóstico):** no genera cambios, por lo que no requiere rollback. La decisión posterior de conservar/descartar cambios de `PBIP/` sí lo requiere: si se descartan cambios con `git restore`/`git checkout`, debe hacerse solo tras confirmación explícita del usuario (acción destructiva sobre archivos no versionados aún); si se conservan y algo falla después, revertir el commit específico de ese grupo de cambios.
- **Fase 7 (todas las subfases):** cada Spec de migración futura debe incluir su propio plan de rollback específico, como ya exige `Docs/ESTRUCTURA_PROYECTO.md` sección 6 para cualquier migración estructural. Regla general aplicable a las 6 subfases: nunca ejecutar un cambio sobre `PBIP/` sin haber confirmado que existe una forma de revertirlo (`git revert`, o respaldo del archivo `.pbip` antes de abrir Power BI Desktop) antes de empezar.

---

## 16. Estrategia de commits

- Un commit por fase (o por subfase en la Fase 7), nunca combinando fases distintas.
- Mensajes en Conventional Commits en español, con cuerpo explicativo cuando el cambio no sea autoevidente.
- Nunca `git add .` — siempre archivos explícitos, listados uno por uno.
- Identidad Git validada antes de cada commit (`EdwinClavijoChallenger <edwin.clavijo@challenger.co>`).
- Mostrar al usuario los archivos exactos y el mensaje propuesto antes de comitear, y esperar aprobación — regla ya vigente en `AGENTS.md` y aplicada consistentemente en toda esta línea de trabajo.
- Sin `Co-Authored-By`, salvo que el usuario indique lo contrario.

---

## 17. Recomendación de push

- **Fases 1–5:** push inmediatamente después de cada commit aprobado — son cambios de bajo riesgo y mantenerlos sincronizados con `origin/main` reduce la ventana de divergencia.
- **Fase 6:** no genera commit, por lo tanto no aplica push en la fase de diagnóstico. Si de la decisión posterior resultan commits (conservar cambios reales), push solo después de que el usuario confirme el resultado del diagnóstico y apruebe explícitamente ese push.
- **Fase 7:** push solo después de validación técnica completa de cada subfase individual (Power BI Desktop sin errores, pruebas de rol si aplica RLS). Nunca agrupar el push de varias subfases en uno solo — cada una se sincroniza por separado para poder aislar un rollback si algo falla en producción.

---

## 18. Decisión sobre subagentes

No se crea ningún subagente con esta Spec. Clasificación de los 5 candidatos propuestos:

| Candidato | Clasificación | Problema que resolvería | Límites | Momento recomendado |
|---|---|---|---|---|
| `pbip-change-inspector` | **Crear después** | Diagnosticar cambios en `PBIP/` (como la Fase 6) de forma repetible cada vez que Power BI Desktop reescribe archivos | No debe tener permiso de escritura sobre `PBIP/` — solo lectura/diagnóstico, la decisión de conservar/descartar sigue siendo del usuario | Cuando el patrón de "diagnosticar cambios PBIP tras abrir Power BI Desktop" se repita en 3+ sesiones distintas, no solo en esta Fase 6 |
| `docs-governance-reviewer` | **Crear después** | Comparar `Docs/` contra el estado real del modelo (como se hizo en `Outputs/03` y `Outputs/05`), detectando discrepancias de conteos y referencias obsoletas | No debe editar `Docs/` sin aprobación — solo detectar y reportar, igual que en esta sesión | Es el candidato más fuerte hoy (ya demostró valor 2 veces), pero se recomienda una tercera repetición antes de formalizarlo, para confirmar que el patrón de verificación (grep de conteos reales) es estable |
| `git-release-guardian` | **Crear después** | Automatizar el patrón preflight → staging explícito → validación de identidad → commit → validación posterior, repetido casi idénticamente en cada tarea de esta sesión | Nunca debe decidir por sí solo qué archivos incluir en un commit — eso requiere aprobación explícita del usuario en cada caso | Es el de mayor repetición demostrada en esta sesión; considerar cuando el volumen de commits por semana crezca más allá de lo manejable manualmente |
| `privacy-pii-guardian` | **No crear todavía** | Evaluar PII en archivos nuevos (como la Fase 5) | El problema que resolvería es puntual hoy (1 archivo, 1 evaluación) — no hay evidencia de volumen recurrente | Reevaluar si el proyecto empieza a recibir archivos nuevos con frecuencia (ej. cada carga anual de datos) |
| `people-analytics-strategist` | **No crear todavía** | Conectar hallazgos técnicos con estrategia de People Analytics (como la sección 7 de `Outputs/05`) | Requiere contexto de negocio externo al repositorio (políticas de RRHH aprobadas, benchmarks de sector) que hoy no existe documentado — sin ese insumo no podría trabajar de forma autónoma | Cuando exista una Spec aprobada para la Fase 7.6 (expansión a Desarrollo Organizacional) y haya al menos una fuente de datos de competencias/desempeño definida |

**Momento recomendado general:** ninguno de los 5 se crea antes de que el proyecto entre en la Fase 7. La razón transversal es que hoy los frentes de trabajo están acoplados (la gobernanza Git depende de lo que encuentra la auditoría documental, que depende de lo que verifica el análisis de `PBIP/`) — dividir en subagentes antes de que ese acoplamiento se resuelva podría fragmentar el hilo de dependencia en vez de simplificarlo, como ya se señaló en `Outputs/05`.

---

## 19. Orden recomendado de ejecución

1. **Fase 1** — Cerrar sincronización Git y trazabilidad (esta Spec)
2. **Fase 2** — Ajustes documentales menores (relaciones, medidas, bookmarks)
3. **Fase 3** — Versionar/revisar `AGENTS.md`
4. **Fase 4** — Actualizar `README.md` raíz
5. **Fase 5** — Evaluar `Inputs/` por PII
6. **Fase 6** — Diagnosticar los 199 cambios de `PBIP/` (sin decidir conservar/descartar todavía)
7. **Fase 7** — Cambios de mayor impacto, solo tras cerrar la Fase 6, en este orden interno sugerido:
   1. 7.3 (cuenta de servicio) + 7.1 (parametrización) — misma raíz de acceso a datos, se benefician de ejecutarse juntas
   2. 7.2 (RLS) — máxima prioridad de riesgo de privacidad restante
   3. 7.5 (encoding GENERACIÓN) — bajo riesgo relativo, cierre rápido de deuda técnica
   4. 7.4 (Dim_Fecha) — mejora de rendimiento, sin urgencia de negocio
   5. 7.6 (expansión a competencias/desempeño/sucesión) — al final, por ser la mayor expansión y depender explícitamente de 7.2 y de gobernanza de datos formal (P13) resuelta

Ninguna fase de la 2 a la 7 se ejecuta sin que el usuario apruebe explícitamente esa fase en particular — esta Spec documenta el plan, no autoriza su ejecución completa de antemano.
