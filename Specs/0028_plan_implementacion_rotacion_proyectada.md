# 0028 - Plan de implementación: Retiros Proyectados y Rotación Proyectada (PBIP-008)

> Plan aprobado por el usuario el 2026-09-02 como `PASS con observaciones`.
> Estado actual: `Aprobado; ejecución no iniciada`.
> Análisis de impacto: `Specs/0027_analisis_impacto_rotacion_proyectada.md`.
> Fecha: 2026-09-02. Base: `main` = `origin/main` =
> `379ea9e99218e5a2e2a19e332bd9f7ed391f643f`.

## Contexto y base

- Rama base: `main` (limpia, sincronizada con `origin/main`).
- Checkpoint previo: `379ea9e` — preservación de `Rotación2` y documentación de
  su alcance.
- Rama provisional existente: `feat/pbip-008-rotacion-proyectada-powerbi`
  (worktree `prunable`; ver sección "Rama provisional").
- Este plan **no autoriza implementación**. Cada fase requiere su propio gate.

## Objetivo

Construir **dos indicadores separados que nunca se mezclan**:

| Indicador | Métrica | Estado metodológico |
|---|---|---|
| **Retiros Proyectados** | `Tasa_Mensual_Retiros` = `SUM(Retiros) / SUM(Total-Sena)` | Validado en Fase 2 de PBIP-008 |
| **Rotación Proyectada** | `Indice_Rotacion` = `((SUM(Ingresos)+SUM(Retiros))/2) / [PromediodeTotal-Sena]` | **Requiere metodología propia** |

Ambos desembocan en un contrato único de proyecciones y en una arquitectura de
tres páginas.

**Regla dura:** no se reutilizan automáticamente modelos, ganadores, MASE,
umbrales ni clasificaciones de `Tasa_Mensual_Retiros` para `Indice_Rotacion`.
Difieren en numerador y denominador simultáneamente.

## Ajuste metodológico obligatorio — estrategias a comparar

La Rotación Proyectada **no se construye asumiendo una estrategia**. La Fase 4
debe comparar empíricamente:

| Estrategia | Descripción | Aporta |
|---|---|---|
| **A — Forecast directo** | Modelar `Indice_Rotacion` como serie única | Simplicidad; menos propagación de error |
| **B — Forecast por componentes** | Modelar `Ingresos` y `Retiros` por separado y derivar el índice | Explicabilidad; descomposición; control de coherencia |

La decisión se toma por **backtesting y holdout**, no por preferencia de diseño.
La proyección de Ingresos (Fase 4B) **se evalúa, no se declara obligatoria**
hasta que la comparación concluya.

### Identidad de conservación — control, no supuesto

`Total-Sena(t) ≈ Total-Sena(t-1) + Ingresos(t) - Retiros(t)`

Verificada sobre 42 meses: error medio absoluto **25,2 personas** sobre planta
promedio de **2.126** = **1,2%**; error mediano 18. Los últimos 7 meses oscilan
entre -40 y +51.

Se usa como **control de coherencia**, nunca como igualdad exacta. El residuo
observado se atribuye a movimientos no capturados (cesiones, reingresos,
cambios de tipo de contrato). Cualquier derivación de planta futura debe
reportar el residuo, no ocultarlo.

## Arquitectura definitiva de páginas

El usuario redefinió nombres y roles el 2026-09-02:

| Página | Page ID | Propósito | Cambio |
|---|---|---|---|
| **`Retiros`** | `ReportSection6a1196bf8c963b709405` | Diagnóstico: qué retiros ocurren, dónde, por qué, en qué perfiles | **Reorganizar** |
| **`Rotación`** | `ReportSectiondc346876696ee4cba0ab` | Seguimiento detallado de indicadores | **Renombrar** desde `Rotación2`; preservar `Indicadores de Rotación` |
| **`Rotación Predictiva`** | *(por crear)* | Comparación, tendencias, retiros y rotación proyectados | **Crear** |

**Frontera semántica:** `Retiros` cuenta **eventos**; `Rotación` calcula
**ratios**; `Rotación Predictiva` **compara y proyecta**. Un visual con tasa no
pertenece a `Retiros`.

El renombrado solo altera `displayName`; el GUID interno se conserva, por lo que
bookmarks y navegación (que referencian por GUID) no se rompen. Genera deuda
documental en `Docs/BI_GUIDELINES.md`, `Docs/CHANGELOG.md` y `Specs/0027`.

## Alcance organizacional

| Nivel | Proyectable | Diagnóstico/descriptivo |
|---|---|---|
| Grupo Empresa | Sí | Sí |
| Empresa | Sí, sujeto a validación por serie | Sí |
| Dependencia | No | Sí |
| Área | No | Sí |
| Cargo | No | Sí, con supresión por privacidad |
| Tipo de contrato | No (condicionado) | **Sí — obligatorio** |
| Clase de contrato | No (condicionado) | **Sí — obligatorio** |

Tipo y Clase de contrato son **obligatorios para análisis histórico y
comparativo**. Su proyección se habilitará únicamente si se logra enriquecer y
reconciliar Ingresos y denominadores con esas dimensiones — hoy `INGRESOS` no
contiene ninguna de las dos columnas y no existe denominador por contrato.

**No se diseñan forecasts artificiales** para niveles no proyectables. El plan
deja abierta la ampliación futura si mejoran cobertura, historia y
denominadores.

### Evidencia de viabilidad por granularidad

Umbrales vigentes de Fase 2 (C8 ≥24 meses útiles, C7 ≤25% meses en cero) sobre
43 meses reales:

| Granularidad | Series | C8 ok | C7 ok | Ambas | % apto |
|---|---:|---:|---:|---:|---:|
| Periodo x Grupo Empresa | 5 | 4 | 3 | 3 | 60% |
| Periodo x Empresa | 12 | 9 | 7 | 7 | 58% |
| Periodo x Grupo x Tipo Contrato | 23 | 7 | 5 | 5 | 22% |
| Periodo x Grupo x Dependencia | 54 | 11 | 9 | 9 | 17% |
| Periodo x Grupo x Clase Nómina | 35 | 9 | 3 | 3 | 9% |
| Periodo x Grupo x Dep x Área | 201 | 17 | 12 | 12 | 6% |
| Periodo x Grupo x Cargo | 319 | 17 | 9 | 9 | 3% |

## Gates bloqueantes

| Gate | Bloquea | PASS | FAIL |
|---|---|---|---|
| **A — Calidad de INGRESOS** | Desglose organizacional de rotación | Brecha explicada y acotada; histórico útil declarado | Rotación limitada al agregado o declarada no proyectable en detalle |
| **B — Denominadores organizacionales** | Proyección bajo Empresa | Fuente conciliada y gobernada | Dependencia/Área/Cargo permanecen descriptivos |
| **C — Métricas** | Diseño de páginas | Las 4 medidas desambiguadas y documentadas | No se construye `Rotación Predictiva` |
| **D — Privacidad** | Publicación de desglose fino | Umbrales aprobados por gobierno | No se publica detalle por Cargo/Área |
| **E — Contrato** | Análisis histórico de contrato | Catálogo canónico aprobado y aplicado a 43 meses | Contrato solo como corte anual, sin comparativo |
| **Jerarquías** | Cortes C y D de `Retiros` | Dimensiones gobernadas por tabla única | Se mantienen slicers heterogéneos, con riesgo de propagación incoherente |

### Alcance real del Gate A

`Ppto Ingresos` **es la hoja `INGRESOS`** de `PptovsReal.xlsx` (mismo origen
SharePoint). Distribución del detalle:

| Año | Filas | Distribución |
|---|---:|---|
| 2023 | 1.679 | **1.678 en enero, 1 en mayo** — volcado de backlog, no serie mensual |
| 2024 | 1.278 | Mensual correcta |
| 2025 | 1.286 | Mensual correcta |
| 2026 | 1.032 | Mensual correcta |

Reconciliación detalle vs. agregado: cuadre **perfecto (0)** en 2024-01 →
2025-10 (22 meses); desde 2025-11 el detalle **excede** al agregado (+12 a
+76/mes). Diferencia acumulada 1.714 registros.

**Por tanto Gate A NO bloquea la Rotación Proyectada a nivel Grupo
Empresa/Empresa**: el numerador de ese nivel proviene del agregado de
`Planta Personal`, que conserva Ingresos en los **43 meses**. Gate A bloquea
únicamente el desglose por Dependencia/Área/Cargo, que de todos modos no es
proyectable.

### Origen del Gate E

`TC` **cambia de codificación en 2026**:

| TC | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|
| Directos | 418 | 587 | 671 | 149 |
| Temporales | 636 | 444 | 358 | 96 |
| F | 0 | 0 | 0 | 239 |
| I | 0 | 0 | 0 | 318 |
| S | 0 | 0 | 0 | 44 |

`Clase de nómina` presenta 11 valores con duplicación semántica evidente
(`Fijo` 903 vs `CONTRATO FIJO` 456; `Temporal` 1.299 vs `TEMPORAL` 95 vs
`TEMPORAL EN PROPIEDAD` 201; `Indefinido` 544 vs `INDEFINIDO` 77 vs
`INDEFINIDO EN PROPIEDAD` 300).

Esto explica la discrepancia observada por el usuario entre dos visuales de
"Retiros por Tipo de Contrato" que muestran categorías distintas.

## Plan por fases

| Fase | Objetivo | Actividades | Agente | Usuario | Evidencia | Gate de salida |
|---|---|---|---|---|---|---|
| **0. Gobierno y baseline** | Punto de partida trazable | Estado Git; clasificar churn sin eliminarlo; inventario de medidas y fuentes; proponer tag | Auditoría, clasificación semántica, propuesta | Autorizar tag y destino del churn | Reporte de estado + propuesta de baseline | Baseline reproducible y working tree explicado |
| **1. Calidad de INGRESOS** | Resolver Gate A | Diagnóstico de 2023; anomalía 2023-01; divergencia desde 2025-11; conciliación Periodo x Grupo y Periodo x Empresa | Diagnóstico, scripts, cuantificación | Explicar el origen de la brecha; decidir corregir o acotar | Informe + tabla de diferencias con causa | PASS/FAIL sobre el desglose organizacional |
| **1B. Homologación de contrato** | Resolver Gate E | Auditar `TC`, `Clase de nómina` y equivalentes; catálogo canónico; tratamiento de `CONTRATO APRENDIZAJE` | Propuesta con evidencia por año y fuente | Aprobar catálogo canónico | Tabla de homologación + cobertura anual | Catálogo aprobado y aplicable a 43 meses |
| **2. Retiros Proyectados** | Consolidar y extender | Preservar metodología; parametrizar clave de agrupación; extender a Empresa; backtesting y holdout | Código, backtesting, tests, informe | Aprobar series publicables | Métricas y clasificación por serie | Cada serie clasificada; sin degradar Grupo Empresa |
| **3. Dataset de Rotación** | Target propio | Construir `Indice_Rotacion`; reconciliar Ingresos/Retiros/Total-Sena; reglas C1-C10 rederivadas; control anti-leakage | Dataset, reglas, tests | Validar que el target refleja el concepto de negocio | Dataset + informe + prueba anti-leakage | Reconciliación dentro de umbral; sin leakage |
| **4. Ciencia de datos de Rotación** | Metodología propia | Comparar Estrategia A vs B; baselines rederivados; M0-M6; rolling-origin; holdout; MASE con naive propio | Modelado, métricas, clasificación | Aprobar umbrales y estrategia ganadora | Backtesting + holdout + comparación A/B | Estrategia decidida por evidencia; ninguna serie publicada sin superar naive |
| **4B. Proyección de Ingresos** | Evaluar componente | Serie mensual de ingresos; baselines y modelos; contraste con `Ppto Total-Sena`; validar identidad en el horizonte | Modelado y control de coherencia | Aprobar uso como componente, no como compromiso de contratación | Backtesting + verificación de identidad | Clasificación por serie; coherencia documentada |
| **5. Contrato unificado** | Arquitectura de datos | Tabla normalizada con `Indicador`/`Escenario`; `FechaCorte`; `VersionDataset`; proceso mensual | Diseño, generación, validación de relaciones | Aprobar arquitectura | Esquema + dataset de prueba | Relaciones N:1 unidireccionales; 0 M:M nuevas |
| **6. Modelo semántico y YoY** | Medidas interanuales | YoY vía `IndexAnioMes - 12`; YTD vs YTD; gobierno semántico (Gate C) | Diseño DAX, validación MCP | Aprobar nombres y desambiguación | DAX + validación en modelo vivo | Medidas validadas; ambigüedad resuelta |
| **7A. Diseño funcional de `Retiros`** | Reorganización | Auditoría de los 15 visuales analíticos; matriz de redundancias; jerarquías; layout; filtros; Gate D; renombrado de páginas y actualización documental | Auditoría, matriz, propuesta, documentación | Aprobar mantener/transformar/consolidar/trasladar/retirar; aprobar nombres | Matriz de decisiones + maqueta | Cada visual responde una pregunta única |
| **7B. Diseño funcional de `Rotación Predictiva`** | Narrativa ejecutiva | Layout; anti-duplicación; visualización de confiabilidad | Propuesta de layout | Aprobar maqueta | Maqueta | Sin duplicar matrices operativas |
| **8. Implementación Power BI** | Construir | Reorganizar `Retiros`; renombrar `Rotación2` a `Rotación`; crear `Rotación Predictiva`; tema LEMCO | Autoría PBIR/TMDL autorizada | Validación visual en Desktop | Capturas + validación MCP | Tres páginas coherentes; `Indicadores de Rotación` intacta |
| **9. Validación integral** | Regresión | Datos, modelos, PBIP, privacidad, proceso mensual | Validación automatizable | Confirmar checklist | Checklist + evidencia | Sin regresiones |
| **10. Transferencia** | Sustentación | Guía: validar, probar, actualizar, interpretar, explicar modelos, justificar, presentar evidencia, responder al comité | Redactar guía y material | Ensayo de sustentación | `Docs/` + guion + FAQ | Usuario capaz de sustentar sin asistencia |
| **11. Versionado y cierre** | Publicación | Documentación; commit/PR/merge; refresh; publicación; limpieza de worktrees | Staging selectivo, PR, documentación | Autorizar commit/push/merge/publicación | PR + SHA + evidencia | Merge aprobado |

## Preguntas analíticas de `Retiros`

| # | Pregunta | Corte |
|---|---|---|
| Q1 | ¿Cuántos retiros ocurren y cómo evolucionan? | Mes |
| Q2 | ¿En qué negocios se concentran y cómo evolucionan? | Grupo Empresa → Empresa x Mes |
| Q3 | ¿Por qué se retiran y cómo cambia el motivo? | Tipo/Detalle x Mes |
| Q4 | ¿Qué estructuras concentran salidas? | Dependencia → Área x Mes |
| Q5 | ¿Cuáles son los focos específicos? | Dependencia → Área → Cargo x Mes |
| Q6 | ¿Qué proporción es voluntaria vs no voluntaria? | Tipo de retiro x Mes |
| Q7 | ¿En qué etapa de permanencia se concentran? | Rango de antigüedad |
| Q8 | ¿Qué características contractuales presentan? | Tipo y Clase homologados |

Cualquier visual que no responda una de estas ocho preguntas de forma única es
candidato a consolidar.

## Redundancias a auditar en `Retiros`

De 32 visuales, **15 son analíticos** (el resto: 9 slicers, `pageNavigator`,
`bookmarkNavigator`, 4 shapes, 1 textbox).

| # | Visuales | Solapamiento | Acción a evaluar |
|---|---|---|---|
| R1 | `4368c366` vs `d5143e9d` | Ambos 100% apilado de Clase de nómina; uno usa `(grupos)` y otro `(grupos) 2` | Consolidar tras Gate E |
| R2 | `b72099f8` vs `f702a32d` | Ambos con `Tasa_Mensual`, `Tasa_Acumulada`, `PromedioSena`; el primero es subconjunto | Consolidar y **trasladar a `Rotación`** |
| R3 | `4594ad02` vs `b643ab53` vs `9ba5241b` | Tres visuales de evolución (mes/trimestre/año) | Consolidar con drill temporal |
| R4 | `5fdb6e4b` vs `f7041df0` | Ambos sobre Detalle/motivo | Conservar el que responda Q3 con composición |
| R5 | `7152010273` vs `c240f7297` | Ambos sobre Cargo | Consolidar en el drill de Q5 |
| R6 | `4d0981ed` | Único de Dependencia x Mes | Base del corte C; verificar no duplicar R5 |
| R7 | `ceb3fdd6` | lineChart con `Tasa_Mensual_Retiros` y `Total-Sena` | **Trasladar a `Rotación`** |

**Regla anti-redundancia:** dos visuales no permanecen únicamente porque ya
existen. Pero no se sacrifica capacidad analítica solo para reducir el número de
visuales.

## Jerarquías organizacionales

Los tres slicers organizacionales de `Retiros` provienen de **tablas
distintas**: `AREA` y `CARGO` desde `PLANTA DE PERSONAL`, `DEPENDENCIA` desde
`Estructura`. No forman una jerarquía gobernada y su propagación puede ser
incoherente.

Debe determinarse qué tabla gobierna cada dimensión y si existen jerarquías
confiables `Grupo Empresa → Empresa` y `Dependencia → Área → Cargo`, antes de
construir los cortes C y D. **No se inventan relaciones jerárquicas.**

## Paralelización

| Vía | Fases | Condición |
|---|---|---|
| 1 — Retiros Proyectados | 2 | Puede avanzar de inmediato; independiente de Gate A |
| 2 — Rotación Proyectada | 1 → 3 → 4 (+4B) | Gate A solo condiciona el desglose, no el nivel grupo |
| 3 — Contrato | 1B | Independiente; alimenta ambas vías |
| 4 — Semántica | 6 (Gate C) | No depende de datos |
| 5 — Diseño de `Retiros` | 7A | Depende de 1B, 6 y Gate D; **no** de Gate A ni B |

**Convergencia obligatoria en Fase 5.** Para evitar arquitecturas
incompatibles, el contrato de datos se diseña **antes** de que la Vía 1 congele
su formato de salida. Si la Vía 1 termina antes, su entregable queda como
dataset intermedio, no como contrato.

## Privacidad

Propuesta inicial **a validar por gobierno**, no política definitiva:

- mínimo **5 eventos** por celda publicada;
- población promedio mínima **30** (`MIN_PLANTA_PROMEDIO` ya existente);
- **supresión secundaria** cuando un valor suprimido pueda deducirse por
  diferencia.

Justificación cuantitativa: el 70% de las combinaciones Grupo x Cargo tiene
menos de 5 retiros en todo el histórico (mediana 2); en Área, el 61%. Publicar
ese detalle permitiría reidentificación.

Aplica la política `Docs/20241025 CSP-POL-09 Política de Tratamiento de Datos
Version Web (002).pdf`. No se versionan datos personales.

## Diseño e identidad visual

Fuente: `Assets/Brand/Manual Marca Grupo LEMCO.pdf`.

| Color | Uso |
|---|---|
| `#1B487F` | Azul principal |
| `#1A3059` | Azul profundo |
| `#000032` | Azul casi negro |
| `#0B1C35` | Fondo oscuro |
| `#F7931E` | Naranja — reservado para énfasis |

Tipografía `Outfit` cuando Power BI Desktop/Service sea compatible; fallback
`Segoe UI`. Las tres páginas deben sentirse como una sola aplicación.

## Rollback

| Antes de | Punto seguro | Mecanismo |
|---|---|---|
| Tocar datos | Baseline en `379ea9e` | Tag + hash de fuentes (`hash_fuente` ya existe) |
| Modificar modelo | Commit previo con TMDL intacto | Rama dedicada por fase |
| Modificar DAX | Backup del TMDL fuera del repo + export MCP | Respaldo externo antes de editar |
| Crear páginas | Commit con `Rotación` verificada | Worktree aislado |
| Publicar | Commit + PR aprobado | `git revert` |

**Prohibido:** `reset`, `restore`, `clean`, `stash`, `rebase`, `amend`,
`force push`, `git add .` / `-A`. El rollback se hace por `revert` o por
reaplicación de patch respaldado, verificando recuperabilidad en ambos sentidos
(`git apply --check` directo y `--reverse`) antes de descartar nada.

## Rama provisional `feat/pbip-008-rotacion-proyectada-powerbi`

**Destino recomendado: ARCHIVAR** — no reutilizar, no eliminar todavía.

- **No reutilizar:** su página presenta `Tasa_Mensual_Retiros` etiquetada como
  rotación, el defecto conceptual exacto que este plan corrige. Acumula además
  7 inconsistencias funcionales documentadas en `Specs/0027`.
- **No eliminar:** contiene decisiones de layout aprovechables y es la única
  evidencia de esa iteración. Su worktree está `prunable` bajo una ruta de otro
  perfil de usuario, por lo que su contenido solo es accesible vía la rama
  remota.
- **Acción:** conservar en el remoto con tag descriptivo, documentar el archivo
  y reconstruir la página desde cero en Fase 8. Retirar la rama solo tras poner
  `Rotación Predictiva` en producción, por decisión del usuario en Fase 11.

## Complejidad relativa

| Fase | Complejidad | Comentario |
|---|---|---|
| 0 | Baja | Método ya probado |
| 1 | Alta | Depende de conocimiento operativo externo; puede terminar en FAIL |
| 1B | Media | Mapeo acotado, decisión de negocio |
| 2 | Media | Metodología existente; parametrizar y validar 12 series |
| 3 | Alta | Target nuevo, reglas rederivadas, anti-leakage |
| 4 | Alta | Comparación A/B completa desde cero |
| 4B | Media | Serie adicional; menor forecastabilidad esperada |
| 5 | Media | Riesgo de arquitectura, no de esfuerzo |
| 6 | Media | DAX YoY sin time intelligence + gobierno semántico |
| 7A | Media | Auditoría y decisiones de consolidación |
| 7B | Media | Diseño y confiabilidad |
| 8 | Alta | Autoría PBIR + validación visual iterativa |
| 9 | Media | Amplia pero mecánica |
| 10 | Media | Alto valor, bajo riesgo técnico |
| 11 | Baja | Gobierno ya establecido |

Sin fechas: dependen de la disponibilidad del usuario para los gates y del
resultado de Fase 1.

## Riesgos

**Bloqueantes**

- **R1.** Gate A en FAIL limita el desglose organizacional de rotación.
  Mitigación: declarar `SIN_FORECAST` antes que publicar un número débil.
- **R2.** Reutilizar por inercia umbrales de Fase 2 en rotación. Mitigación:
  Fase 4 no cierra sin naive propio documentado.
- **R3.** Sin homologar contrato, todo comparativo histórico de esa dimensión
  es inválido.

**Importantes**

- **R4.** Dos denominadores conviviendo (`Planta Personal` vs
  `PLANTA DE PERSONAL`) producirían cifras distintas entre páginas.
- **R5.** El paralelismo genera arquitecturas incompatibles. Mitigación: Fase 5
  fija el contrato antes de congelar salidas.
- **R6.** Reidentificación en Cargo/Área.
- **R7.** Churn de Power BI Desktop reintroduce ruido en cada guardado.
- **R8.** Ambigüedad `Indice_Rotacion` / `Índice_Retiros` / `Índice_Rotación`
  llega a las páginas nuevas.
- **R9.** Menor forecastabilidad de Ingresos por ser decisión de gestión más
  que proceso natural.

**Menores**

- **R10.** `.venv311` roto (apunta a `E:\Users\Usuario\...`, inexistente).
- **R11.** Tres worktrees `prunable`.
- **R12.** Filas `Real` de ago-dic 2026 con `Total-Sena = 0`; filtrar solo por
  `Ppto/Real = 'Real'` produce denominadores cero silenciosos.

## Criterios de aceptación de PBIP-008

1. `Tasa_Mensual_Retiros` e `Indice_Rotacion` nunca se presentan como
   equivalentes ni se sustituyen entre sí en un visual.
2. Ningún número se publica como "rotación proyectada" sin backtesting propio.
3. `Indicadores de Rotación` permanece intacta.
4. Cada visual de `Retiros` responde una pregunta distinta de las ocho
   definidas.
5. Tipo y Clase de contrato usan el catálogo canónico aprobado.
6. Ninguna relación many-to-many nueva.
7. El desglose fino respeta los umbrales de privacidad aprobados.
8. El usuario puede sustentar la metodología sin asistencia.

## Estado de versionamiento

Este plan se versiona **antes** de iniciar la Fase 0, para que la trazabilidad
quede completa: análisis de impacto (`Specs/0027`) → plan de implementación
(este documento) → ejecución por fases.

Ninguna fase ha sido ejecutada al momento de registrar este plan.
