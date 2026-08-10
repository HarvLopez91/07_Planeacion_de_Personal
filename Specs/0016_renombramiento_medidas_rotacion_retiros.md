# Renombramiento de medidas de rotación y retiros + nuevo Índice de Rotación

Fecha: 2026-08-06

Estado: implementación técnica completa. GATE 5 (conciliación numérica en vivo con Power BI Desktop) ejecutado y aprobado por el usuario el 2026-08-10 (sección 10). Auditoría remota del PR #5 detectó y corrigió contaminación de alcance en `Tbl_Medidas.tmdl`/`es-ES.tmdl` (commit `b5475ef`); el smoke test post-auditoría quedó **no ejecutable** por un defecto estructural preexistente de `origin/main`, ajeno a DAX-002 — ver sección 14.

Iniciativa independiente de `Specs/0015_mapeo_campos_contratos_kactus.md` y del PR #4 (Contratos Kactus). No comparte alcance, archivos ni rama.

## 1. Problema identificado

Las etiquetas visibles de las matrices de `Retiros` y `Rotación2` no coincidían con los nombres técnicos de las medidas DAX que las alimentaban, y los nombres técnicos tampoco representaban correctamente la fórmula que calculan:

- `Ind_Rot` (nombre sugiere "índice de rotación") en realidad calculaba una **variación neta** de personal, no un índice de rotación.
- `Ind_Retiros` (nombre sugiere un índice general) en realidad calculaba una **tasa mensual** de retiros.
- `Rotacion_Segun_Tipo` (nombre sugiere segmentación por tipo únicamente) en realidad devuelve el **acumulado anual**, con o sin segmentación por tipo.
- No existía ninguna medida que calculara un verdadero índice de rotación (movimiento de personal considerando ingresos y retiros).
- `Docs/METRICS_CATALOG.md` documentaba además una medida `Indice_Rotacion` en el contexto de `Ppto Retiros` que ya no existe en el modelo actual (documentación obsoleta, corregida en esta iniciativa — ver sección 6).

## 2. Definición funcional de cada indicador

| Indicador visible | Definición funcional |
|---|---|
| Variación Neta Mensual (%) | Crecimiento o disminución neta de la planta en el período: `(Ingresos - Retiros) / Total-Sena`. No es un índice de rotación. |
| Índice de Rotación (%) | Movimiento de personal (entradas y salidas) respecto a la población base: `((Ingresos + Retiros) / 2) / Promedio de Total-Sena`. |
| Tasa Mensual de Retiros (%) | Retiros del período sobre la población base del mismo período: `Retiros / Total-Sena`. |
| Tasa Acumulada de Retiros (%) | Retiros acumulados sobre el promedio de población base de los meses incluidos: `Retiros acumulados / Promedio de Total-Sena` (nunca la suma de `Total-Sena`). Con variantes voluntaria, involuntaria y "según tipo" (conmuta según el filtro de tipo de retiro activo). |

## 3. Fórmula de origen de `Retiros` (y de `Ingresos`)

En `PptovsReal.xlsx`, hoja `Planta Personal`, ambas columnas se calculan con `CONTAR.SI.CONJUNTO`/`COUNTIFS` sobre las hojas `RETIROS`/`INGRESOS`, **en el archivo fuente, no en el modelo semántico**:

- `Retiros` excluye: aprendices SENA, practicantes, reingresos, fallecimientos, pensión por jubilación, cesiones de contrato (fórmula provista por el usuario, confirmada además con una fórmula viva equivalente en `Retiros` filas 1028-1038 de la hoja).
- `Ingresos` excluye: aprendices SENA, practicantes, reingresos (confirmado con fórmula viva encontrada en las mismas filas). Las demás exclusiones de `Retiros` no aplican semánticamente a un evento de ingreso.
- Existe además una columna `Ingresos-Temporal`, con la misma fórmula más una exclusión adicional de contratos "TEMPORAL". El modelo semántico consume `Ingresos` (no `Ingresos-Temporal`); se deja registrado por si en el futuro se requiere esa variante.

**Consecuencia de diseño**: las medidas DAX de rotación y retiros **no duplican** estas exclusiones. Usan `Planta Ppto[Ingresos]` y `Planta Ppto[Retiros]` directamente como cifras ya depuradas.

## 4. Uso de `Total-Sena`

`Total-Sena` = Total de colaboradores excluyendo aprendices SENA. Es la población base que LEMCO usa para los indicadores de rotación y retiros, porque los aprendices SENA no forman parte de esa población.

- Para un único mes: se usa el valor de `Total-Sena` de ese mes.
- Para una selección de varios meses (acumulado): el denominador es el **promedio** de `Total-Sena` de los meses incluidos (medida `PromediodeTotal-Sena`, ya existente, basada en `AVERAGEX` sobre `DimPeriodoYM[IndexAnioMes]`), nunca la suma.

## 5. Medidas renombradas

Se conservó el `lineageTag` de cada medida (mismo objeto interno, solo cambia el nombre técnico) y su `displayFolder` original.

| Nombre anterior | Nombre nuevo | lineageTag | Cambio de fórmula |
|---|---|---|---|
| `Ind_Rot` | `Variacion_Neta_Personal` | `19650ba2-b55d-4486-b176-fac7bc1c9a97` | Se envolvió en `DIVIDE(..., 0)` (antes división directa sin protección de cero). |
| `Ind_Retiros` | `Tasa_Mensual_Retiros` | `725f6b0b-d70f-4ace-8f20-6772c3ab0771` | Igual, se envolvió en `DIVIDE(..., 0)`. |
| `Rotacion_Anual_Acumulada` | `Tasa_Acumulada_Retiros` | `8d79992a-eb85-4e9f-a0e6-dfd3d639cd62` | Sin cambio (ya usaba `DIVIDE` con promedio). |
| `Rotacion_Voluntaria_Anual_Acumulada` | `Tasa_Acumulada_Retiros_Voluntarios` | `b00930f2-cbe1-4463-82fb-c621b9e2448e` | Sin cambio. |
| `Rotacion_Involuntaria_Anual_Acumulada` | `Tasa_Acumulada_Retiros_Involuntarios` | `673428f2-6c06-4627-a29b-81260884d917` | Sin cambio. |
| `Rotacion_Segun_Tipo` | `Tasa_Acumulada_Retiros_Segun_Tipo` | `e2d3c4b5-a6f7-8e9d-0c1b-2a3f4e5d6c7b` | Sin cambio de lógica; se actualizaron las referencias internas a las 3 medidas renombradas de la fila anterior. |

Referencias dependientes actualizadas (sin dejar ninguna referencia activa a los nombres anteriores):

- `Tbl_Medidas.tmdl`: la fórmula de `Tasa_Acumulada_Retiros_Segun_Tipo` referenciaba internamente a las otras 3 medidas renombradas — actualizada.
- Visuales: `b72099f821538078c4a0`, `ceb3fdd6c5499b35e5b8`, `f702a32db8dfea04babc`, `f04eef32576ba115ab23`, `c240f7297edc1325fa6d` (esta última tenía una referencia de formato de columna huérfana, sin proyección activa, corregida por completitud).
- Bookmarks: `1470a84b0dbff32f11c9`, `173ee601b10926d5ea06`, `1cc1f0829d849c47a6e8`, `8de456dcf36bd2ae1f2a` (capturaban el estado del visual `f04eef32576ba115ab23`, incluida la referencia a `Ind_Rot`/`Ind_Retiros`).
- `PBIP/Proyecto.SemanticModel/definition/cultures/es-ES.tmdl`: entradas de sinónimos Q&A generadas por Desktop (`ConceptualProperty` y términos de mismo nombre exacto). Las claves de diccionario en minúscula (p. ej. `tbl_medida.ind_rot`) quedaron con el nombre anterior porque son cosméticas; Desktop las regenera automáticamente al guardar.
- `Docs/METRICS_CATALOG.md`: ver sección 6.

## 6. Nueva medida `Indice_Rotacion`

```dax
measure Indice_Rotacion =
    VAR IngresosPeriodo = SUM('Planta Ppto'[Ingresos])
    VAR RetirosPeriodo = SUM('Planta Ppto'[Retiros])
    VAR PromedioColaboradoresSinSena = [PromediodeTotal-Sena]
    RETURN
        DIVIDE(
            DIVIDE(IngresosPeriodo + RetirosPeriodo, 2),
            PromedioColaboradoresSinSena,
            0
        )
```

- Tabla: `Tbl_Medidas`. `displayFolder`: `02 Ppto vs Real`. Formato: `0.00\ %;-0.00\ %;0.00\ %`.
- `lineageTag` nuevo: `c4a1f2e3-7b9d-4a5f-8c6e-1d2b3e4f5a6c` (no existía una medida con este nombre en el modelo actual).
- **Corrección documental**: `Docs/METRICS_CATALOG.md` citaba una medida `Indice_Rotacion` distinta, en el contexto de `Ppto Retiros`, con fórmula `([Tot_ingresos] - [Tot_Retiros]) / [Tot_Colab-Sena]`. Se verificó que esa medida no existe en ningún archivo `.tmdl` del modelo actual (ni `Tot_ingresos` como medida real) — era documentación obsoleta. Se corrigió con una nota explícita en el catálogo, sin eliminar el rastro histórico.
- **Auditoría previa de `Ingresos`** (requerida antes de aprobar esta medida): ver sección 3. Se encontró que `Ingresos` sí tiene reglas de exclusión propias en el archivo fuente (SENA, practicante, reingreso), coherentes con `Retiros`. No se encontraron casos problemáticos que debieran excluirse adicionalmente en DAX. No se requiere decisión humana adicional sobre exclusiones.

Ubicación en visuales: agregada únicamente en `f04eef32576ba115ab23` (matriz principal de `Rotación2`), la única matriz que ya mostraba juntas Variación Neta Mensual, Tasa Mensual de Retiros y Tasa Acumulada de Retiros. Orden resultante: Colaboradores*, Ingresos*, Retiros*, Variación Neta Mensual (%), Índice de Rotación (%), Tasa Mensual de Retiros (%), Tasa Acumulada de Retiros (%). No se modificó ningún otro visual ni se eliminó ningún indicador existente.

## 7. Dependencias afectadas

- `Tasa_Acumulada_Retiros_Segun_Tipo` depende de `Tasa_Acumulada_Retiros_Voluntarios`, `Tasa_Acumulada_Retiros_Involuntarios` y `Tasa_Acumulada_Retiros` (referencias internas actualizadas).
- `Indice_Rotacion` depende de `PromediodeTotal-Sena` (sin cambios, ya existente).
- Ningún otro visual del proyecto referenciaba las 6 medidas renombradas fuera de las páginas `Retiros` y `Rotación2` (confirmado por búsqueda en todo `PBIP/Proyecto.Report/`).
- No se tocaron relaciones, columnas de origen ni consultas Power Query.

## 8. Riesgos

1. **`es-ES.tmdl` con claves de diccionario parcialmente desactualizadas** (cosmético, solo afecta sinónimos de Q&A; Desktop las regenera al guardar).
2. ~~GATE 5 (conciliación numérica) todavía no ejecutado~~ — **resuelto**: ejecutado y aprobado el 2026-08-10 (sección 10).
3. **Definición de "índice de rotación" nueva para el negocio**: es una medida nueva, sin precedente visual previo; su interpretación (movimiento de personal, no neto) fue validada con el usuario en el GATE 5 (sección 10) — **PASS**.
4. **Filtros previamente corregidos** (filtro de `Generaciones` restaurado, relación autodetectada eliminada, exclusión de Habitel Hotels conservada, `Rotación2` oculta en modo lectura) deben permanecer intactos — revalidados en la ronda final de validaciones (sección 9).
5. **Fragilidad estructural de las medidas basadas en `Total-Sena`** (`SumadeTotal-Sena`, `PromediodeTotal-Sena`, `Variacion_Neta_Personal`, `Tasa_Mensual_Retiros`, `Indice_Rotacion`, `Tasa_Acumulada_Retiros*`): ninguna filtra `'Planta Ppto'[Ppto/Real] = "Real"` internamente; hoy solo producen cifras correctas porque cada visual que las usa repite ese filtro a nivel de visual (ver sección 10). Cualquier visual nuevo que las use sin ese filtro (incluida la futura desagregación por Dependencia/Área/Cargo, sección 11) mostrará cifras infladas sin error visible. **No se corrige en esta Spec** — queda documentado para que la próxima iniciativa que construya sobre estas medidas replique el filtro o, alternativamente, se evalúe envolver el filtro dentro de las medidas base en una iteración futura con su propio análisis de impacto.
6. **`Índice_Retiros` como deuda funcional** (sección 12): medida preexistente con fórmula sin protección de división y 2 visuales con filtros fijos obsoletos (año 2025, una única Dependencia). No se corrige en esta Spec; queda documentada para la futura iniciativa de desagregación.

## 9. Pruebas realizadas

**Nota (2026-08-10, post-auditoría):** todos los conteos de "129 medidas" de esta sección corresponden a la instancia de Power BI Desktop usada para el GATE 5 **original** (commit `e914c77`, antes de que la auditoría del PR #5 detectara contaminación de alcance en `Tbl_Medidas.tmdl`). No representan el estado final del checkout limpio (`b5475ef`) ni fueron reconfirmados mediante apertura real de Power BI Desktop sobre ese commit — ver sección 14 para el conteo correcto y el motivo por el que no pudo revalidarse en vivo.

- Recarga completa del modelo vía MCP (`powerbi-modeling-mcp`, conexión offline sobre TMDL) tras cada cambio: 52 tablas, 129 medidas, 66 relaciones, 0 errores de carga.
- Confirmación individual de las 7 medidas (6 renombradas + `Indice_Rotacion`) vía `measure_operations.Get`: las 7 en estado `Ready`, sin `errorMessage`.
- Búsqueda exhaustiva de referencias a los 6 nombres anteriores en todo `PBIP/`: 0 referencias funcionales activas restantes tras las correcciones.
- Validación JSON de los 5 visuales y 4 bookmarks modificados: sin errores.
- Balance de paréntesis/llaves de `Tbl_Medidas.tmdl` y `es-ES.tmdl`: balanceado.
- Auditoría de duplicados de nombre de medida en todo el modelo: 0 duplicados.

**Ronda final (2026-08-10, tras GATE 5 y desactivación del subtotal de `f702a32db8dfea04babc`):**

- JSON válido del visual modificado (`f702a32db8dfea04babc`), `rowSubtotals: false` confirmado, `columnSubtotals` sin cambio (`false`).
- Conexión MCP en vivo a `Proyecto7` (Desktop abierto, instancia del GATE 5 original, commit `e914c77`): `INFO.MEASURES()` = 129, `INFO.RELATIONSHIPS()` = 66, `INFO.TABLES()` = 52 — sin cambios respecto a la última recarga, 0 errores. **Este conteo no corresponde al checkout limpio `b5475ef`** (ver nota al inicio de esta sección y sección 14).
- Auditoría de duplicados de nombre de medida vía consulta DAX en vivo (`INFO.MEASURES()` agrupado): 0 duplicados.
- 0 referencias activas a los 6 nombres anteriores en `PBIP/Proyecto.Report/` (excluidas las claves de diccionario cosméticas de `es-ES.tmdl`, ya documentadas).
- Filtro `Generaciones[Generación] <> null` presente en `30f11733eea2697476d4` (Demográfico Promedio).
- Selección persistida `Empresas[Grupo Empresa] = 'Habitel Hotels'` sigue ausente en `a4193576029d03d04cb5` (Rotación2) — exclusión intencional conservada.
- `Rotación2` (`ReportSectiondc346876696ee4cba0ab`) con `visibility: HiddenInViewMode` y `showPage: false` en el `pageNavigator` — confirmado.
- Relación autodetectada `AutoDetected_7787d46a...` sigue en 0 ocurrencias en `relationships.tmdl`.
- Cifras del GATE 5 (sección 10) no se ven afectadas por la desactivación del subtotal: es un cambio de presentación del visual (`rowSubtotals`), no toca ninguna medida ni relación.
- **Nota de riesgo operativo**: la desactivación del subtotal se aplicó editando el archivo directamente mientras Power BI Desktop tenía `Proyecto7.pbip` abierto (requerido para el GATE 5 en vivo). Si Desktop guarda el reporte antes de que este cambio se confirme en disco, podría revertirlo. Se recomienda no guardar en Desktop hasta confirmar que el commit de esta iniciativa se completó (sección 14).

## 10. Resultados de conciliación (GATE 5) — APROBADO 2026-08-10

Ejecutado mediante `powerbi-modeling-mcp` conectado a la instancia en vivo de `Proyecto7.pbip` (Power BI Desktop abierto, PID detectado vía `ListLocalInstances`, conexión `PBIDesktop-Proyecto7-60278`).

### Contexto de filtro obligatorio: `Planta Ppto[Ppto/Real] = "Real"`

`Planta Ppto` contiene dos poblaciones de filas por mes/empresa: `Ppto` (objetivo presupuestado de dotación) y `Real` (dotación y movimientos reales). Las columnas `Ingresos`/`Retiros` solo están pobladas en las filas `Real` (las filas `Ppto` devuelven `null`), pero `Total-Sena` está poblada en **ambas**. Por eso:

- Las medidas base (`SumadeTotal-Sena`, `PromediodeTotal-Sena`, `Variacion_Neta_Personal`, `Tasa_Mensual_Retiros`, `Indice_Rotacion`, `Tasa_Acumulada_Retiros` y variantes) **no incluyen internamente** el filtro `Ppto/Real = "Real"` en su DAX.
- Los 3 visuales matriz que usan estas medidas (`f702a32db8dfea04babc` en Retiros, `b72099f821538078c4a0` en Retiros, `f04eef32576ba115ab23` en Rotación2) **sí llevan ese filtro aplicado a nivel de visual** (`filterConfig.filters`, cards `6975b4e85f7925501456`, `12217f5c6e90d9aed7a1`, `659d373f6b09b714b77e` respectivamente, los tres con `Values: ['Real']`). Por eso lo que se ve en el reporte hoy es correcto.
- **Riesgo documentado, no corregido en esta iniciativa** (ver sección 8, riesgo 5): cualquier visual futuro que use estas medidas sin repetir ese filtro (p. ej. tarjetas nuevas, la futura desagregación por Dependencia/Área/Cargo — sección 11) mostrará cifras infladas (~1.96×) en `Colaboradores*` y proporcionalmente reducidas en los porcentajes, sin ningún error visible.

### Cifras aprobadas — acumulado enero-julio 2026 (todos los grupos, `Ppto/Real = "Real"`)

| Indicador | Valor DAX (MCP) | Valor esperado (usuario) | Diferencia | Resultado |
|---|---:|---:|---:|---|
| Promedio colaboradores sin SENA | 2.422,57 | 2.423 (2.422,57) | 0,00 | **PASS** |
| Ingresos | 828 | 828 | 0 | **PASS** |
| Retiros válidos | 627 | 627 | 0 | **PASS** |
| Variación Neta (`Variacion_Neta_Personal`) | 1,19 % | 1,19 % | 0,00 pp | **PASS** |
| Índice de Rotación (`Indice_Rotacion`) | 30,03 % | 30,03 % | 0,00 pp | **PASS** |
| Tasa Mensual de Retiros (`Tasa_Mensual_Retiros`) | 3,70 % | 3,70 % | 0,00 pp | **PASS** |
| Tasa Acumulada de Retiros (`Tasa_Acumulada_Retiros`) | 25,88 % | 25,88 % | 0,00 pp | **PASS** |

Validación puntual adicional (Grupo Empresa = Challenger, `Ppto/Real = "Real"`):

| Corte | Variación Neta | Índice de Rotación | Tasa Mensual | Tasa Acumulada | Resultado |
|---|---:|---:|---:|---:|---|
| Enero 2026 | 2,03 % | 4,45 % | 3,43 % | 3,43 % | **PASS** (coincide con captura) |
| Acumulado ene-jul 2026 | — | 25,70 % | — | 22,66 % | **PASS** (coincide con captura) |

Conciliaciones mensuales (7 meses × total y × 5 Grupo Empresa = 35 filas) y acumuladas por Grupo Empresa obtenidas vía MCP durante la sesión del GATE 5 quedan como evidencia válida; no se transcriben fila a fila en esta Spec para no duplicar el detalle ya generado.

### Explicación: Tasa Mensual vs. Tasa Acumulada de Retiros

Ambas usan el mismo numerador (`Retiros` del período), pero denominadores distintos:

- **Tasa Mensual de Retiros** = `Retiros / SUM(Total-Sena)` del período filtrado. Si el período incluye varios meses, el denominador **suma** la exposición de cada mes — por eso, evaluada sobre un rango de 7 meses, da un valor pequeño (ej. Challenger acumulado: 3,24 %) porque compara retiros del período contra una exposición acumulada mucho más grande que la de un solo mes. Es la métrica correcta para un **único mes** (donde suma = valor del mes).
- **Tasa Acumulada de Retiros** = `Retiros / PromediodeTotal-Sena` del período filtrado (`AVERAGEX` sobre los meses distintos en contexto). El denominador es el **promedio** de dotación sin SENA de esos meses, no la suma — por eso da un valor mucho mayor y comparable entre períodos de distinta longitud (ej. Challenger acumulado: 22,66 %). Es la métrica correcta para **períodos de varios meses**.

Para un único mes ambas coinciden exactamente (promedio de un solo valor = ese valor), como se ve en la fila "Enero 2026" de Challenger (3,43 % en ambas).

### Reproducibilidad

Todas las cifras de esta sección fueron generadas con `dax_query_operations.Execute` sobre la conexión en vivo, filtrando `DimPeriodoYM[Año]="2026" && DimPeriodoYM[Numero]<=7` y `'Planta Ppto'[Ppto/Real]="Real"`. No se repiten las consultas DAX en esta actualización de la Spec; se referencian como evidencia ya obtenida y aprobada por el usuario.

## 11. Desarrollo pendiente — desagregación por Dependencia, Área y Cargo (fuera de alcance de esta Spec)

El usuario confirmó (2026-08-10) que los 3 slicers nuevos en la página `Retiros` (`779a007f8c95502c3105` Área, `7f9c16551d9422019d6e` Cargo, `8523f1c3d93305035cd2` Dependencia) y el reflujo de posiciones/tamaños derivado en el resto de visuales de esa página son **intencionales y quedan como línea base aprobada** — no se revierten. Forman parte de una implementación pendiente, no completada, para construir indicadores de retiros y rotación desagregados por Dependencia, Área y Cargo.

- **Esta Spec (0016) no incluye ese desarrollo.** Los 3 slicers quedan en la página sin visuales de análisis conectados a ellos todavía.
- El desarrollo completo (matrices/tarjetas por Dependencia/Área/Cargo usando las medidas validadas en la sección 10, ver también sección 12) debe registrarse como iniciativa independiente en `Specs/00_roadmap_y_backlog.md`, con su propia Spec de análisis de impacto/plan de implementación antes de ejecutarse.
- `Rotación2` permanece `HiddenInViewMode`, excluida de las 12 copias del visual `pageNavigator` (`showPage: false`), y sin ningún botón/bookmark que navegue hacia ella desde el resto del reporte — sin acceso para usuario final. La reorganización de `Retiros`/`Rotación` (inventario y propuesta ya entregados en `Outputs/51_2026-08-06_inventario_retiros_rotacion_y_gate5_estructural.md`) también queda pendiente como Spec independiente, no incluida aquí.

## 12. `Índice_Retiros` — deuda funcional documentada, sin migración automática

Medida preexistente, no tocada por esta iniciativa: `Índice_Retiros = [Tot_Retiros] / [Tot_Colab-Sena]` (`Tbl_Medidas.tmdl`, lineageTag `d7064b38-6c9b-46f9-b269-4757284bd27f`), usada en 2 visuales de `Rotación2`: `5abcdd8fd1c5a1015723` (por Dependencia) y `8d3d8ab39e15678e422a` (por Área).

**Diagnóstico (GATE 5, evidencia en vivo):**

- **A. Fórmula**: división directa (`/`), sin protección `DIVIDE`. Numerador `Tot_Retiros = COUNT('Ppto Retiros'[Mes])` (conteo de eventos sin las exclusiones que sí tiene `Planta Ppto[Retiros]` — ej. bajo el contexto acumulado ene-jul 2026 total, `Tot_Retiros` = 846 eventos vs. `Cantidad_Retiros` = 627 retiros válidos). Denominador `Tot_Colab-Sena = COUNT('PLANTA DE PERSONAL'[ID])`, una tabla de roster distinta de `Planta Ppto`, sin promediar entre meses (suma acumulada de conteos mensuales, no promedio — bajo el mismo contexto total da 70.153, un valor sin significado de "dotación promedio").
- **B. Por qué produce `Infinito`**: no es un problema general de la fórmula bajo un contexto limpio (una consulta DAX de control por las 15 Dependencias con mayor valor, y un filtro explícito de "denominador cero", no reprodujo ningún caso de `Tot_Colab-Sena = 0` para el corte ene-jul 2026 sin restricciones adicionales). La causa confirmada es que **ambos visuales tienen filtros de nivel de visual obsoletos, no relacionados con esta iniciativa**:
  - `8d3d8ab39e15678e422a` ("Rotación por Área"): filtro fijo `Años[Año] = '2025'` — de ahí que el título siga mostrando 2025 aunque el resto del reporte esté en 2026.
  - `5abcdd8fd1c5a1015723` ("Rotación por Dependencia"): filtro fijo residual `PLANTA DE PERSONAL[DEPENDENCIA] = 'GERENCIA CADENA MUEBLES LAMINADOS'`, aparentemente un filtro de prueba que quedó guardado en el visual.
  - Combinados con la selección de slicers activa en cada sesión de Desktop, estos filtros fijos producen intersecciones vacías (`Tot_Colab-Sena = 0` con `Tot_Retiros > 0`), y como la fórmula usa `/` sin `DIVIDE`, el resultado es `Infinito` en vez de blanco o `0`.
- **C. Por qué se comporta distinto entre Dependencia y Área**: por los dos filtros fijos distintos descritos en B (una fija el año a 2025, la otra fija una única dependencia), no por una diferencia en la lógica de la medida.
- **D. ¿Es equivalente a `Tasa_Mensual_Retiros`?** **No.** Bajo el mismo contexto limpio (ene-jul 2026 total, sin los filtros fijos obsoletos): `Índice_Retiros` (`DIVIDE` de control) = 846 / 70.153 = **1,21 %**, mientras que `Tasa_Mensual_Retiros` (con `Ppto/Real="Real"`) = **3,70 %** y `Tasa_Acumulada_Retiros` = **25,88 %**. Las tres difieren en tabla de origen (`Ppto Retiros`/`PLANTA DE PERSONAL` vs. `Planta Ppto`), en granularidad (eventos individuales sin depurar vs. cifras mensuales ya depuradas en el archivo fuente) y en el tratamiento del denominador (suma de conteos vs. promedio). **No son la misma métrica.**

**Decisión (por instrucción del usuario, 2026-08-10): no se reemplaza automáticamente `Índice_Retiros` por `Tasa_Mensual_Retiros`.** Se documenta como deuda funcional perteneciente a la futura iniciativa de desagregación por Dependencia/Área/Cargo (sección 11), donde deberá decidirse si esos 2 visuales se reconstruyen sobre las medidas ya validadas en esta Spec (`Indice_Rotacion`/`Tasa_Mensual_Retiros`/`Tasa_Acumulada_Retiros`, con el filtro `Ppto/Real="Real"` correspondiente) o si `Índice_Retiros` se conserva con un nombre técnico no ambiguo (ej. `Indice_Retiros_Legado_PptoRetiros`) documentando explícitamente su alcance distinto. No se aplica ningún cambio a esta medida ni a estos visuales en esta Spec.

## 13. Fila de Total general — decisión aplicada

Sobre la matriz `f702a32db8dfea04babc` (Retiros): la fila de total general, con el filtro de corte ene-jul 2026 activo, únicamente repite la fila del año 2026 (no aporta información adicional porque solo hay un año en el contexto de filtro). Por instrucción del usuario, se desactivó el subtotal de fila (`rowSubtotals: false`) de este visual — no se creó ninguna medida nueva para este propósito. Detalle de la corrección estructural aplicada y su validación en la sección 9 (actualizada) y en el reporte de cierre.

Nota de transparencia: la evidencia en vivo del GATE 5 (sección 10) no reprodujo el síntoma original de "Colaboradores en blanco" en la fila de total bajo el contexto ene-jul 2026 — `PromediodeTotal-Sena` devolvió un valor válido (2.422,57) en todos los niveles de agregación probados. La desactivación del subtotal se aplica igualmente por instrucción expresa del usuario, dado que la fila resultaba redundante independientemente de ese punto.

## 14. Auditoría remota del PR #5, saneamiento de alcance y smoke test post-auditoría (2026-08-10)

### 14.1 Hallazgo de la auditoría

La auditoría remota del PR #5 en GitHub detectó que el diff de `Tbl_Medidas.tmdl` y `es-ES.tmdl` (commit `e914c77`) incorporaba, además de los 7 cambios de DAX-002, medidas y metadatos lingüísticos de iniciativas concurrentes ajenas: `Cantidad_Retiros_Validos`, 6 medidas `Prod_*_Challenger`/`Prod_*_Otros`, y reordenamiento/whitespace de `Tot_empleados_Promedio_Sin_Aprendices`, `AnioActual_Comparado`, `AnioAnterior_Comparado`, `Titulo_Var_Ppto`, `Titulo_Var_Real` y medidas `GL_*`/Productividad. La causa fue una copia de archivo completo desde un working tree compartido con esas otras iniciativas.

### 14.2 Corrección (commit `b5475ef`)

Se reconstruyeron ambos archivos desde `origin/main`, reaplicando exclusivamente los 6 renombres + `Indice_Rotacion` (`Tbl_Medidas.tmdl`: 48 líneas de diff, antes 398) y las 6 entradas Q&A correspondientes (`es-ES.tmdl`: 12 líneas de diff, antes ~12.293). Verificado: 0 ocurrencias de las 7 medidas ajenas, 0 referencias rotas a los 6 nombres anteriores, 7 `lineageTag` preservados, 0 dependencia DAX entre las medidas de DAX-002 y las medidas retiradas.

### 14.3 Intento de smoke test post-auditoría sobre `b5475ef`

Para revalidar el estado exacto que se fusionaría, se creó un worktree desechable en modo detached exactamente sobre `b5475ef226af306ac0857a8a4b7b4522e53a1dd1` y se abrió `Proyecto7.pbip` desde ahí (dos intentos independientes). **En ambos intentos, Power BI Desktop no pudo cargar el modelo**, mostrando el diálogo "Se encontraron problemas": primero por `Tot_Accidentes` duplicado, y tras retirarlo temporalmente (solo en el worktree desechable, sin staging/commit), por `ConteoP` duplicado.

### 14.4 Inventario de duplicados (causa raíz)

Se auditaron todas las medidas declaradas en `PBIP/Proyecto.SemanticModel/definition/tables/*.tmdl`: **27 nombres de medida están declarados dos veces** — una copia en su tabla de dominio (`AUSENTISMOS`, `SST GENERAL`, `Ppto Ingresos`, `Selección Grupo Lemco`, `Selección Challenger`, `SENA UNIDADES`, `ACCIDENTALIDAD`) y otra copia en `Tbl_Medidas`, **compartiendo el mismo `lineageTag`** en los 27 casos:

- **20 duplicados con fórmula idéntica** entre ambas copias: `%AusM`, `%Cumplimiento`, `Ausentismo`, `CHombres`, `CMujeres`, `ConteoP`, `DIAS_AUSENTISMO`, `Dias Ausentismo Acc.Lab`, `Ind_opor`, `Ingresos_Calidad`, `MSector`, `M_Frecuencia`, `M_Severidad`, `Ret_Calidad`, `Solicitud`, `Solicitudes`, `Solicitudes2024`, `Tasa_Acc`, `Tot_Accidentes`, `Tot_ingresos`.
- **7 duplicados con fórmula textualmente DIFERENTE** bajo el mismo `lineageTag` (inconsistencia estructural más profunda que un nombre repetido): `Ind_Calidad`, `Ind_Calidad_2025`, `Ing_Calidad_2025`, `Tasa Ausentismo`, `Tasa Ausentismo_EL`, `Tasa_Ausent_Anual`, `ret_Calidad_2025`.

**Confirmado que ninguna de las 27 duplicidades fue introducida por DAX-002**: las 7 tablas de dominio involucradas son byte a byte idénticas a `origin/main` (0 diferencias), y el único cambio de `Tbl_Medidas.tmdl` frente a `origin/main` en toda esta rama son los 7 cambios de DAX-002 ya documentados (sección 5-6) — ninguno de los 27 nombres duplicados. Es un defecto estructural **preexistente del baseline `origin/main`**.

### 14.5 Conclusión — smoke test NO EJECUTABLE (no es FAIL de DAX-002)

Por instrucción expresa del usuario, no se continuó parcheando duplicado por duplicado (la presencia de 7 definiciones textualmente divergentes bajo el mismo `lineageTag` hace ambigua la resolución automática) ni se volvió a intentar abrir Power BI Desktop. El smoke test post-auditoría queda registrado como **NO EJECUTABLE por un defecto preexistente del baseline `origin/main`, ajeno por completo a esta iniciativa** — no como un FAIL de las medidas de DAX-002.

**Evidencia funcional que permanece válida para el cierre de esta Spec:**
- El GATE 5 original en vivo (sección 10), ejecutado y aprobado por el usuario contra la instancia que reportó 129 medidas / 66 relaciones / 52 tablas (commit `e914c77`, antes del saneamiento de alcance).
- La equivalencia formal de las 7 medidas de DAX-002 tras el saneamiento (`b5475ef`): DAX idéntico byte a byte al validado en el GATE 5 original, 0 dependencia de cualquier medida ajena o duplicada, 7 `lineageTag` preservados.

No se generó ningún conteo en vivo final para el checkout limpio `b5475ef` porque el modelo no llegó a cargar en Power BI Desktop; no debe inferirse ni afirmarse un conteo de "129" ni "149" medidas como validado en vivo para ese commit.

### 14.6 Saneamiento estructural — fuera de alcance de esta Spec

La resolución de las 27 duplicidades (10 de ellas con fórmulas divergentes) queda registrada como iniciativa independiente `GOV-005` en `Specs/00_roadmap_y_backlog.md` (sección 7). No se resuelve en esta Spec ni bloquea su cierre.
