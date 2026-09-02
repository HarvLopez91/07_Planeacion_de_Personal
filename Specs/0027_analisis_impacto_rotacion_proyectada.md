# 0027 - Análisis de impacto: rotación proyectada (PBIP-008)

> **Fase:** análisis de impacto y diseño. **No autoriza implementación.**
> Estado de la iniciativa: `En evaluación`.
> Fecha: 2026-09-01. Base auditada: `main` = `origin/main` =
> `a49ffe195ce48c2e4c98380a787692357f3085ed`.

## Objetivo de negocio

Presentar el comportamiento y las variaciones esperadas de la rotación durante
los próximos cinco meses, vinculadas con el plan de reducción y los planes de
acción de cada negocio.

Compromiso establecido el `2026-07-27`.

## Marco temporal

| Concepto | Valor |
|---|---|
| Último cierre real | **2026-07-31** |
| Horizonte de proyección | **agosto, septiembre, octubre, noviembre y diciembre de 2026** (5 meses) |

No se proyecta desde septiembre ni se usa agosto como dato real inicial: a la
fecha de este análisis, agosto 2026 **no tiene ejecución** en la fuente.

## Decisiones congeladas por el usuario

1. **Métrica objetivo:** `Tasa_Mensual_Retiros` = `Retiros / Total-Sena`.
   `Indice_Rotacion` **no** es la variable objetivo.
2. **Tipo de rotación:** total. La voluntaria queda como dimensión
   complementaria para explicar comportamiento y apoyar los planes de reducción.
3. **Nivel principal:** `Mes × Grupo Empresa`. Empresa solo como apertura
   descriptiva o baseline simple donde el volumen lo permita.
4. **Plan de reducción:** no existe fuente estructurada. No bloquea la
   proyección estadística. Prohibido inventar porcentajes o impactos.
5. **Modelado:** el ganador se decide por backtesting, no por supuesto previo.
6. **Diciembre:** hipótesis de estacionalidad a validar empíricamente, no
   premisa.

## Auditoría de páginas — `Retiros` vs `Rotación2` (PBIP-008)

Auditoría de solo lectura ejecutada el `2026-09-01` sobre las 51 visuales de
ambas páginas (32 en `Retiros`, 19 en `Rotación2`), sus filtros de página,
bookmarks y navegación, más validación en vivo vía MCP contra el modelo
(55 tablas / 123 medidas).

**Hallazgos clave:**

- `Retiros` (`ReportSection6a1196bf8c963b709405`) es la página de
  **diagnóstico**: visible, con `pageNavigator` propio. Responde quién, dónde,
  por qué (motivo/detalle) y antigüedad del retiro.
- `Rotación2` (`ReportSectiondc346876696ee4cba0ab`) es la página de
  **tendencia**: `"visibility": "HiddenInViewMode"`, con botón "Back" pero
  **sin ningún punto de entrada activo** (0 bookmarks, 0 acciones de
  navegación la referencian; solo aparece como entrada cosmética
  `showPage:false` en los 12 `pageNavigator` del reporte). Hoy es
  inalcanzable para un usuario final.
- Ambas páginas comparten prácticamente los mismos filtros de página sobre
  `Ppto Retiros` (excluir Aprendiz/Practicante, Fallecimiento, Pensión,
  Reingreso, Cesión) y duplican 4–5 visuales (Retiros por Cargo, por Clase de
  nómina/Año) con formato distinto pero el mismo dato.
- **Corrección de un hallazgo inicial:** se creyó que a `Rotación2` le
  faltaba la exclusión explícita de `CESION CONTRATO`. Verificado
  directamente en `page.json`: su filtro usa `NOT CONTAINS(Detalle,
  "CESION")` (substring), que ya excluye cualquier valor que contenga
  `CESION CONTRATO`. `Retiros` solo tiene un filtro adicional explícito
  redundante para el mismo caso. **No hay gap real de exclusión en
  `Rotación2`.**
- Confirmado en vivo (MCP): tres medidas de "índice de rotación" con nombres
  casi idénticos y fórmulas distintas conviven en el modelo — `Indice_Rotacion`
  (sin tilde, sobre `Planta Ppto`), `Índice_Retiros` (con tilde, sobre
  `Ppto Retiros`/`PLANTA DE PERSONAL`, usada hoy en 2 de las 3 pivotTables de
  `Rotación2`) e `Índice_Rotación` (con tilde y acento distinto, no usada en
  ninguna de las dos páginas). Para el mismo contexto devuelven valores muy
  distintos (148,0 % / 5,44 % / no evaluada) — confirma la deuda funcional ya
  señalada en `Specs/0016` sección 12.

## Decisión funcional PBIP-008 (aprobada por el usuario, 2026-09-01) — SUPERADA

> **Superada el 2026-09-02.** El usuario decidió conservar `Rotación2` como
> vista de seguimiento y detalle, y crear más adelante una página adicional
> `Rotación` de carácter ejecutivo. Ver
> ["Decisión funcional vigente (2026-09-02)"](#decisión-funcional-vigente-2026-09-02).
> Lo siguiente se conserva como registro histórico; el tercer viñeta ("no se
> crea una tercera página") **ya no aplica**.

- **`Retiros` = diagnóstico**: quién, dónde, por qué, antigüedad, motivo,
  cargo, dependencia, área. Sin cambios de fondo.
- **`Rotación2` = comportamiento y proyección**: histórico real,
  `Tasa_Mensual_Retiros`, tendencia, forecast agosto–diciembre 2026 y,
  posteriormente, meta/plan y escenario ajustado.
- ~~**No se crea una tercera página.** El Compromiso 2 se construye
  evolucionando `Rotación2` (visibilidad, navegación y contenido), no
  `Retiros` ni una página nueva.~~
- Ningún visual ni medida se elimina todavía; ninguna visibilidad ni
  navegación cambia todavía. Esta decisión es de alcance, no de
  implementación.

## Definición vigente de rotación

Fuente: `Docs/METRICS_CATALOG.md` y el TMDL del modelo.

| Medida | Fórmula | Rol en PBIP-008 |
|---|---|---|
| **`Tasa_Mensual_Retiros`** | `DIVIDE(SUM(Retiros), SUM(Total-Sena), 0)` | **Variable objetivo** |
| `Tasa_Acumulada_Retiros` | `DIVIDE([Cantidad_Retiros], [PromediodeTotal-Sena], 0)` | Contexto acumulado |
| `Indice_Rotacion` | `DIVIDE(DIVIDE(Ingresos + Retiros, 2), [PromediodeTotal-Sena], 0)` | Fuera de alcance como objetivo |
| `Variacion_Neta_Personal` | `DIVIDE(Ingresos − Retiros, Total-Sena, 0)` | No es rotación (así lo aclara el catálogo) |

Reglas heredadas que **no se modifican**:

- **Denominador `Total-Sena`**: excluye aprendices SENA.
- **Numerador**: retiros ya depurados en el archivo fuente.
- **Periodicidad**: mensual.
- Las variantes voluntaria e involuntaria se derivan de
  `Planta Personal[Retiros Voluntarios]`.

## Inventario de datos

| Fuente | Contenido | Rol |
|---|---|---|
| `Data/HeadCount/PptovsReal.xlsx` → `Planta Personal` | 1.067 filas; serie mensual agregada con `Retiros`, `Retiros Voluntarios`, `Ingresos`, `Total`, `Total-Sena`, separada por `Ppto/Real` | **Fuente primaria** |
| `Data/HeadCount/PptovsReal.xlsx` → `RETIROS` | 3.960 registros individuales con motivo, tipo de contrato, cargo, dependencia, área, salario y antigüedad | Análisis explicativo |
| `Planta Ppto` (Power BI) | Consume `Planta Personal` | Consumo BI |
| `Ppto Retiros` (Power BI) | Consume `RETIROS` | Consumo BI |

**Histórico real disponible: 43 meses continuos, 2023-01 → 2026-07**, sin huecos
de denominador. Agosto–diciembre 2026 existen únicamente como filas `Ppto`.

### Serie agregada (referencia)

Media `4,03 %`, mediana `3,94 %`, desviación `0,92`, rango `2,76 %` – `8,47 %`.

## Calidad de datos por Grupo Empresa

Medido sobre los 43 meses con denominador válido:

| Grupo Empresa | Meses | Tasa media | Desv. | Mín | Máx | Meses con 0 retiros | Viabilidad estadística |
|---|---|---|---|---|---|---|---|
| Challenger | 43 | 3,63 % | 1,16 | 1,88 | 9,52 | 0 | **Alta** |
| Habitel Hotels | 43 | 7,19 % | 1,98 | 3,10 | 12,39 | 0 | **Alta** |
| Grupo Sky | 43 | 3,80 % | 1,44 | 1,38 | 7,06 | 0 | **Media-alta** |
| Lemco | 43 | 1,71 % | 1,60 | 0,00 | 6,25 | **14** | **Baja** — serie rala |
| Fundación Challenger | 43 | 5,13 % | **10,00** | 0,00 | **40,00** | **33** | **No viable** |

Hallazgo determinante: los cinco grupos tienen denominador en los 43 meses,
pero el **numerador** es muy disperso en dos de ellos. `Fundación Challenger`
tiene 33 de 43 meses en cero y una desviación de 10 puntos sobre una media de
5,13 %: cualquier modelo de series de tiempo produciría intervalos sin sentido.

**Habitel Hotels casi duplica la rotación del resto** (7,19 % frente a ~3,7 %).
Es un argumento fuerte para modelar por grupo y no solo el agregado.

## Dataset analítico propuesto

### Grano

`Periodo (AAAAMM) × Grupo Empresa × tipo_registro`

Un registro por combinación. `tipo_registro` separa explícitamente las capas y
evita mezclar hechos con supuestos.

### Esquema

| Campo | Tipo | Descripción |
|---|---|---|
| `periodo` | int (`AAAAMM`) | Clave temporal |
| `anio`, `mes_num` | int | Derivados, para estacionalidad |
| `grupo_empresa` | texto | Nivel de proyección |
| `empresa` | texto (nullable) | Solo en capa descriptiva |
| **`tipo_registro`** | enum | `REAL`, `BASELINE`, `FORECAST`, `META_PLAN`, `ESCENARIO_AJUSTADO`, `REAL_FUTURO` |
| `retiros` | int | Numerador |
| `retiros_voluntarios` | int | Dimensión complementaria |
| `total_sena` | int | Denominador (`Total-Sena`) |
| `tasa_mensual_retiros` | decimal | Métrica objetivo |
| `modelo` | texto (nullable) | Modelo que generó el valor |
| `li_80`, `ls_80` | decimal (nullable) | Intervalo de predicción |
| `fecha_corte` | fecha | Corte del que parte la proyección (`2026-07-31`) |
| `version_dataset` | texto | Trazabilidad de ejecución |

### Separación de capas

| Capa | Origen | Estado |
|---|---|---|
| `REAL` | `Planta Personal`, `Ppto/Real = Real`, hasta 2026-07 | Disponible |
| `BASELINE` | Naive / último valor, referencia de comparación | Se genera |
| `FORECAST` | Modelo ganador del backtesting | Se genera |
| `META_PLAN` | Meta de reducción por negocio | **Bloqueado — sin fuente** |
| `ESCENARIO_AJUSTADO` | `FORECAST` ajustado por meta y planes | **Bloqueado — depende de `META_PLAN`** |
| `REAL_FUTURO` | Ejecución de ago–dic conforme se cierre cada mes | Futuro |

**Regla de oro:** el dataset nunca sobrescribe `REAL` con `FORECAST`. Al cerrar
cada mes se agrega `REAL_FUTURO` y se conserva el `FORECAST` original para medir
error real fuera de muestra.

### Decisión sobre qué se proyecta

Se proyectan **numerador y denominador por separado**, y la tasa se **deriva**:

- `Total-Sena` crece de forma sostenida (1.801 → 2.465 en 43 meses) y su
  dinámica es más estable y predecible que la del cociente.
- Proyectar la tasa directamente mezcla dos dinámicas distintas y dificulta
  explicar al negocio si una variación viene de más salidas o de más plantilla.

Esta decisión debe validarse en el backtesting: se compara contra proyectar la
tasa directamente, y gana la que menor error produzca.

## Reglas de calidad

Controles a ejecutar antes de modelar; cada uno bloquea o marca el registro.

| # | Regla | Acción si falla |
|---|---|---|
| C1 | `total_sena > 0` en todo periodo-grupo | Excluir del modelado; documentar |
| C2 | `retiros >= 0` y `retiros <= total_sena` | **Bloquear**, revisar fuente |
| C3 | `retiros_voluntarios <= retiros` | **Bloquear** |
| C4 | Continuidad mensual sin huecos entre `periodo_min` y `periodo_max` | Bloquear si hay hueco interno |
| C5 | Solo `Ppto/Real = 'Real'` entra a `REAL` | Bloquear mezcla con `Ppto` |
| C6 | El último periodo `REAL` es `202607` | Bloquear si difiere del corte |
| C7 | Grupos con >25 % de meses en cero → **no aptos para modelo estadístico** | Degradar a baseline simple |
| C8 | Grupos con menos de 24 meses útiles | Degradar a baseline simple |
| C9 | Suma de grupos reconcilia con el agregado (±0,1 %) | Bloquear |
| C10 | Outliers: marcar \|z\| > 3 sobre la serie del grupo | Marcar, **no eliminar** sin decisión |

Por C7, **`Fundación Challenger` (77 % de meses en cero) y `Lemco` (33 %)
quedan fuera del modelado estadístico** y se tratan con baseline simple. Se
documenta explícitamente en el entregable: no se les asigna un forecast con
apariencia de precisión que los datos no sostienen.

## Diseño del backtesting

### Esquema

**Validación de origen móvil (rolling origin) con horizonte fijo de 5 meses**,
replicando exactamente la situación real de negocio.

- Entrenamiento mínimo: 24 meses.
- Horizonte: `h = 1..5`.
- El origen avanza mes a mes: con 43 meses y `h=5` caben **15 orígenes**
  (entrenar hasta el mes 24, 25, … 38).
- Cada origen produce 5 predicciones evaluadas contra el real observado.
- **Sin fuga de información**: en cada origen el modelo solo ve datos anteriores
  a él, incluidos los factores estacionales.

### Métricas

| Métrica | Uso |
|---|---|
| **MAE** | **Principal** — en puntos porcentuales, interpretable por negocio |
| **RMSE** | **Principal** — penaliza errores grandes |
| MAPE | **Complementario y condicionado**: solo se reporta si la serie del grupo no tiene valores cercanos a cero. No se usa en `Lemco` ni `Fundación Challenger` |
| MASE | Complementario; escala el error contra el naive, útil para comparar grupos con niveles distintos |

Se reporta el error **por horizonte** (`h=1` … `h=5`), no solo el promedio: un
modelo puede ser bueno a un mes y malo a cinco, y el compromiso exige cinco.

### Modelos a comparar

Todos compiten en igualdad de condiciones:

| # | Modelo | Notas |
|---|---|---|
| M0 | **Naive** (último valor observado) | Referencia obligatoria |
| M1 | Naive estacional (mismo mes del año anterior) | Prueba la hipótesis de diciembre |
| M2 | Promedio móvil (3, 6 y 12 meses) | |
| M3 | Tendencia (regresión lineal sobre el tiempo) | |
| M4 | Tendencia + estacionalidad (descomposición) | |
| M5 | Suavizamiento exponencial simple / Holt | |
| M6 | Holt-Winters | **Solo si** hay ≥ 2 ciclos completos en la ventana de entrenamiento; con 24 meses está en el límite y debe declararse |

**Excluidos por diseño:** SARIMA (43 puntos, riesgo de sobreajuste) y cualquier
modelo de machine learning. No hay volumen de observaciones ni variables
explicativas que lo justifiquen; se documenta como decisión, no como omisión.

### Criterio objetivo de selección

Se aplica en orden:

1. **Umbral de admisión:** el modelo debe superar a **M0 (naive)** en MAE
   promedio sobre los 15 orígenes. Si ninguno lo supera, **el ganador es M0** y
   así se reporta.
2. **Criterio principal:** menor **MAE promedio** en `h=1..5`.
3. **Desempate 1 (≤ 5 % de diferencia en MAE):** menor **RMSE**.
4. **Desempate 2:** menor error en `h=4` y `h=5` — los meses más lejanos son los
   que más pesan en un compromiso de cinco meses.
5. **Desempate 3 — explicabilidad:** ante desempeño equivalente, gana el modelo
   más simple y explicable ante comité.
6. **Estabilidad:** se descarta el modelo cuya desviación de error entre
   orígenes sea desproporcionada, aunque tenga buena media.

La selección se hace **por grupo**, no global: nada obliga a que Challenger y
Habitel Hotels compartan modelo. Se documenta el ganador y su error por grupo.

**Sobre diciembre:** la estacionalidad se acepta solo si M1 o M4 superan a M0
en el backtesting. El promedio de diciembre (5,89 % frente a ~3,9 %) es una
señal, pero con 3 observaciones no basta para darla por estructural.

## Resultado del backtesting — PRIMERA EJECUCIÓN (SUPERADA por la auditoría)

> **Estado: SUPERADO.** Los resultados de esta sección fueron obtenidos antes
> de la auditoría de código del `2026-09-01`. Se conservan por trazabilidad,
> pero **no deben usarse**. Los resultados vigentes están en la sección
> "Resultado del backtesting — SEGUNDA EJECUCIÓN (vigente)".

Ejecutado el `2026-09-01` con `Scripts/rotacion_proyectada/` (Python,
`.venv`, sin dependencias nuevas — modelos M0-M6 implementados directamente
sobre `numpy`, sin `statsmodels`). Evidencia completa en
`Outputs/PBIP-008_Rotacion_Proyectada/` (`reporte.md`,
`backtesting_metricas.csv`, `backtesting_ganadores.csv`,
`backtesting_detalle.csv`, `forecast_ago_dic_2026.csv`,
`reglas_calidad.csv`). El dataset generado (`dataset_real.csv`, con cifras
reales) se escribe en `Data/HeadCount/rotacion_proyectada/`, fuera de Git.

**Reglas de calidad C1–C10:** las 10 pasan o degradan según lo previsto. C7
confirma en datos reales lo estimado en el análisis: `Fundación Challenger`
76,7 % de meses en cero, `Lemco` 32,6 % — ambos degradados a baseline simple
(M0 naive), sin forecast estadístico. C10 marca 2 outliers puntuales
(Challenger 2023-12, Fundación Challenger 2025-06), no eliminados.

**Modelo ganador por Grupo Empresa** (15 orígenes, horizonte 1–5, MAE
promedio):

| Grupo Empresa | Ganador | MAE naive | MAE ganador | ¿Supera naive? |
|---|---|---|---|---|
| Challenger | `M3_Tendencia` | 0,74 % | 0,56 % | Sí |
| Grupo Sky | `M3_Tendencia` | 1,89 % | 1,43 % | Sí |
| Habitel Hotels | `M2_PromedioMovil` | 2,23 % | 1,94 % | Sí |
| Lemco | `M0_Naive` (baseline por C7/C8) | — | — | N/A |
| Fundación Challenger | `M0_Naive` (baseline por C7/C8) | — | — | N/A |

Los tres grupos aptos superan el umbral de admisión (naive). Ninguno
requirió `M6_HoltWinters` como ganador; `M4` (tendencia+estacionalidad) no
ganó en ningún grupo — la estacionalidad de diciembre **no se confirma
empíricamente** con este corte, consistente con el riesgo ya documentado
("3 observaciones no bastan"). El error no crece de forma anómala entre
`h=1` y `h=5` en ningún grupo apto (ver `backtesting_metricas.csv`).

**Explicación sencilla de cada ganador:**

- **Challenger y Grupo Sky → tendencia lineal simple.** Sus series muestran
  una dirección sostenida en el tiempo (leve descenso) más clara que
  patrones estacionales o el simple "repetir el último mes"; una recta
  ajustada a los últimos meses predice mejor que copiar el dato anterior.
- **Habitel Hotels → promedio móvil.** Su tasa es más alta y algo más
  errática mes a mes; promediar una ventana reciente amortigua el ruido
  mejor que una tendencia o que el último valor aislado.
- **Lemco y Fundación Challenger → naive (sin modelo estadístico).** Con
  tantos meses en cero, cualquier modelo de series de tiempo produciría una
  falsa sensación de precisión; se reporta el último valor observado y se
  declara explícitamente como no modelado.

**Forecast agosto–diciembre 2026** (tasa mensual de retiros, intervalo 80 %
donde aplica): Challenger desciende de 2,81 % a 2,67 %; Grupo Sky de 3,31 %
a 3,22 %; Habitel Hotels plano en 6,94 % (por ser promedio móvil); Lemco y
Fundación Challenger en 0,00 % (último valor real observado, sin intervalo
por tratarse de baseline). Detalle mes a mes en `forecast_ago_dic_2026.csv`.

## Auditoría de código (2026-09-01)

Auditoría integral de `Scripts/rotacion_proyectada/` solicitada antes de
aceptar los resultados. Evidencia reproducible en el notebook
`Notebooks/PBIP-008_rotacion_proyectada.ipynb`.

### Lo que se validó como correcto

| Aspecto | Resultado |
|---|---|
| Fuga de información | **Sin fuga.** Prueba de perturbación: se alteró la última observación y ningún pronóstico de orígenes anteriores cambió (525 comparaciones, 0 diferencias) |
| Separación train/test | Correcta: todo objetivo es estrictamente posterior a su ventana de entrenamiento |
| Origen móvil | 15 orígenes, entrenamientos de 24 a 38 meses |
| Horizonte `h=1..5` | Diseño balanceado: exactamente 15 observaciones por (método, horizonte) |
| Recálculo de parámetros | Confirmado: ventana de promedio móvil, pendiente y coeficientes Holt se reestiman en cada origen |
| MAE y RMSE | Verificados contra cálculo manual independiente |
| Guarda de MAPE | Correcta: devuelve nulo cuando hay reales en cero |
| Determinismo | Dos corridas completas producen salidas **idénticas byte a byte** |
| Consistencia con la fuente | Reconstrucción independiente desde `PptovsReal.xlsx` reproduce las mismas cifras |

### Defectos encontrados y corregidos

| # | Defecto | Impacto | Corrección |
|---|---|---|---|
| D1 | **Conjunto de modelos incompleto.** Solo competían M0–M6, todos operando sobre la *serie de cocientes*, que promedia tasas y da el mismo peso a un mes de planta 4 que a uno de planta 1 800 | **Alto — cambió los ganadores en los 5 grupos** | Se añadió la familia `B1`–`B5` de tasa agrupada (`Σ retiros / Σ planta`) en `models.POOLED_FUNCS` |
| D2 | **Degradación a priori.** `Lemco` y `Fundación Challenger` se forzaban a `M0_Naive` por C7/C8 sin dejarlos competir; como su último mes fue 0 %, el "pronóstico" resultante era 0 % | **Alto — falsa precisión** | Se eliminó la degradación previa. Todos los grupos compiten; la decisión de publicar se toma después con la clasificación de fiabilidad |
| D3 | **MASE contaminada.** El denominador se calculaba con `y_full`, la serie completa, incluidos los períodos de prueba | Medio (métrica, no selección) | La escala se calcula por origen con solo el tramo de entrenamiento (columna `escala_naive`) |
| D4 | **Intervalos de ancho constante.** Se usaba un único RMSE promedio para los 5 meses | Medio — subestimaba la incertidumbre en `h=4/5` | RMSE por horizonte; además el límite inferior se trunca en 0 % |
| D5 | **C1 y C9 no podían fallar.** C1 evaluaba `len(...) >= 0` (siempre verdadero) y C9 tenía `PASS` fijo | Medio — controles decorativos | Ambos convertidos en controles reales |
| D6 | **`version_dataset` no reproducible.** Usaba `datetime.now()` | Bajo | Ahora es el hash SHA-256 del archivo fuente |
| D7 | Banda de empate del 5 % colapsable si `MAE ≈ 0` | Bajo | Se añadió término absoluto de tolerancia |
| D8 | Duplicados inertes: `"Fundación Challenger"` dos veces en un conjunto; `"año"` dos veces en la detección de columna | Nulo | Limpiados |

### Limitación no corregible (se declara)

El modelo ganador se elige con el mismo backtesting con el que se mide su
error. El MAE reportado es por tanto **optimista**; el error real en
producción tenderá a ser algo mayor. Corregirlo exigiría una tercera
partición, inviable con 43 meses.

## Resultado del backtesting — SEGUNDA EJECUCIÓN (vigente)

Ejecutado el `2026-09-01` tras la auditoría. **12 métodos** en competencia
(M0–M6 más B1–B5), mismos 15 orígenes y mismo horizonte. Evidencia en
`Outputs/PBIP-008_Rotacion_Proyectada/` y en el notebook.

**Reglas de calidad:** C1–C6 y C8–C10 en `PASS`; C7 en `DEGRADED`
(`Fundación Challenger` 76,7 % de meses en cero, `Lemco` 32,6 %). C9, ahora
un control real, reconcilia con desvío 0,0000 %.

### Clasificación de fiabilidad

Ganar el backtesting no basta para publicar una cifra. Se aplican tres
umbrales: planta promedio ≥ 30 personas, ≤ 25 % de meses en cero y error
típico ≤ 60 % de la tasa media.

| Nivel | Qué se publica |
|---|---|
| **A — Pronóstico estadístico** | Pronóstico puntual + intervalo 80 % |
| **B — Referencia descriptiva** | Tasa de referencia, explícitamente **no** un pronóstico |
| **C — Sin pronóstico confiable** | **Ninguna tasa.** Solo conteo esperado de retiros |

El umbral de planta 30 no es arbitrario: por debajo, un solo retiro mueve la
tasa más de 3 puntos porcentuales y la métrica pierde resolución.

### Modelo ganador por Grupo Empresa

| Grupo Empresa | Nivel | Ganador | MAE naive | MAE ganador | Mejora | MASE |
|---|---|---|---|---|---|---|
| Challenger | A | `B5_Mediana12M` | 0,743 % | 0,521 % | 30 % | 0,50 |
| Grupo Sky | A | `B3_TasaAgrupada24M` | 1,893 % | 1,295 % | 32 % | 0,80 |
| Habitel Hotels | A | `B2_TasaAgrupadaHist` | 2,229 % | 1,747 % | 22 % | 0,68 |
| Lemco | B | `B3_TasaAgrupada24M` | 1,716 % | 1,407 % | 18 % | 1,02 |
| Fundación Challenger | C | `B5_Mediana12M` | 14,635 % | 9,876 % | 33 % | 1,54 |

**En los cinco grupos ganó un baseline de tasa agrupada.** Ningún modelo de
tendencia, estacionalidad o suavizamiento resultó ganador: la rotación
mensual se comporta como un **nivel estable con ruido**, no como una serie
con dirección o ciclo. Esto confirma —ahora con evidencia directa— que la
estacionalidad de diciembre **no se sostiene empíricamente** con este corte.

### Proyección agosto–diciembre 2026

| Grupo Empresa | Tipo | Tasa mensual | IP 80 % (h=1 → h=5) | Retiros esperados (5 meses) |
|---|---|---|---|---|
| Challenger | FORECAST | 3,241 % | 2,44–4,04 % → 2,40–4,08 % | ≈ 293 |
| Grupo Sky | FORECAST | 3,570 % | 1,46–5,68 % → 1,67–5,47 % | ≈ 43 |
| Habitel Hotels | FORECAST | 7,164 % | 4,58–9,75 % → 4,49–9,84 % | ≈ 114 |
| Lemco | REFERENCIA_DESCRIPTIVA | 1,623 % | 0,00–3,41 % → 0,00–4,02 % | ≈ 7 |
| Fundación Challenger | SIN_FORECAST | — | — | < 1 persona |

Planta de referencia: la del último mes real (202607). En `Lemco` el límite
inferior se trunca en 0 %, señal de que la incertidumbre es del mismo tamaño
que la señal.

### Diferencias frente a la primera ejecución

| Grupo | Antes | Ahora | Causa |
|---|---|---|---|
| Challenger | `M3_Tendencia`, 2,81 %→2,67 % | `B5_Mediana12M`, 3,241 % plano | D1: la mediana agrupada tiene 7 % menos MAE que la tendencia |
| Grupo Sky | `M3_Tendencia`, 3,31 %→3,22 % | `B3_TasaAgrupada24M`, 3,570 % | D1: 9 % menos MAE |
| Habitel Hotels | `M2_PromedioMovil`, 6,94 % | `B2_TasaAgrupadaHist`, 7,164 % | D1: 10 % menos MAE |
| Lemco | `M0_Naive`, **0,00 %** | Referencia descriptiva **1,623 %** | D2: el 0 % era artefacto de forzar el naive sobre un último mes en cero |
| Fundación Challenger | `M0_Naive`, **0,00 %** | **Sin pronóstico** | D2 + planta de 3–7 personas |

Las tasas subieron en los tres grupos de nivel A porque la tendencia lineal
extrapolaba un descenso que el backtesting **no valida**: al medir fuera de
muestra, proyectar el nivel reciente acierta más que proyectar una pendiente.

**Pendiente de decisión del usuario antes de construir la página:** validar
estos resultados; no se ha modificado `Rotación2` ni se ha creado ningún
artefacto visual todavía.

## Estructura prevista para el plan de reducción

Contrato mínimo de datos que se necesitará para habilitar `META_PLAN` y
`ESCENARIO_AJUSTADO`:

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `grupo_empresa` | texto | Sí | Debe conciliar con el catálogo vigente |
| `empresa` | texto | No | Si la meta baja a ese nivel |
| `periodo_inicio` | `AAAAMM` | Sí | Inicio de aplicación |
| `periodo_fin` | `AAAAMM` | Sí | Fin de aplicación |
| `meta_tipo` | enum | Sí | `TASA_OBJETIVO` \| `REDUCCION_PP` \| `REDUCCION_PCT` |
| `meta_valor` | decimal | Sí | Coherente con `meta_tipo` |
| `plan_accion` | texto | Sí | Descripción de la acción |
| `responsable` | texto | Sí | Persona o rol |
| `fecha_inicio`, `fecha_fin` | fecha | Sí | Ejecución del plan |
| `estado` | enum | Sí | `PLANEADO` \| `EN_CURSO` \| `COMPLETADO` \| `CANCELADO` |
| `impacto_esperado_pp` | decimal | No | Solo si el negocio lo cuantifica |
| `supuesto` | texto | No | Base del impacto estimado |
| `fuente` | texto | Sí | Trazabilidad del dato |

Reglas de incorporación:

- `ESCENARIO_AJUSTADO` = `FORECAST` + efecto declarado del plan. **Nunca** se
  deriva de un supuesto inventado por el modelo.
- Si un grupo no tiene meta, su `ESCENARIO_AJUSTADO` queda **vacío**, no igual
  al forecast: la ausencia de plan debe ser visible.
- El efecto se aplica solo dentro de `periodo_inicio`..`periodo_fin`.
- Se conserva el forecast sin ajustar para poder comparar plan contra
  tendencia.

## Entregable previsto

- **Evolución de la página `Rotación2`** para el Compromiso 2 (no se crea
  página nueva — ver sección "Decisión funcional PBIP-008"), con separación
  visual de `Real`, `Forecast`, `Meta/Plan` y `Escenario ajustado`, y con un
  punto de navegación real hacia ella (hoy no existe ninguno).
- **Dataset analítico reproducible** con el esquema de arriba.
- **Script versionado** (`Scripts/`) que genera el dataset y ejecuta el
  backtesting de forma determinista.
- **Salidas de control**: tabla de errores por modelo, grupo y horizonte.

Separación de artefactos:

| Artefacto | ¿Versionado? |
|---|---|
| Script de generación y backtesting | **Sí** |
| Spec, metodología, controles de calidad | **Sí** |
| Definición del dataset y contratos | **Sí** |
| Dataset generado con datos de personal | **No** — `Data/**` fuera de Git |
| Salidas intermedias con datos sensibles | **No** |

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Sobreajuste con 43 observaciones | Backtesting de origen móvil; modelos complejos excluidos por diseño |
| Estacionalidad de diciembre asumida sin evidencia | Se valida empíricamente; si no mejora el error, no se usa |
| Series ralas (`Lemco`, `Fundación Challenger`) | Regla C7/C8: baseline simple y declaración explícita |
| Publicar forecast sin escenario de plan | Capas separadas; ausencia de meta visible, no rellenada |
| Confundir `Tasa_Mensual_Retiros` con `Indice_Rotacion` | Métrica objetivo congelada y documentada |
| Que el forecast se lea como compromiso | Etiquetado explícito e intervalos de predicción |
| Cambio del corte real (nuevo cierre mensual) | `fecha_corte` y `version_dataset` en el dataset; regeneración reproducible |

## Criterios de aceptación

1. Dataset reproducible desde script, con las 6 capas de `tipo_registro`.
2. Los 10 controles de calidad ejecutados y documentados.
3. Backtesting con 15 orígenes y horizonte 1–5 sobre los grupos aptos.
4. Modelo ganador seleccionado por criterio objetivo y **superando a naive**;
   si no lo supera, se reporta naive como ganador.
5. Error documentado por grupo y horizonte (MAE, RMSE y MASE).
6. `Lemco` y `Fundación Challenger` con tratamiento declarado.
7. Proyección de ago–dic 2026 partiendo del corte `2026-07-31`.
8. `Data/**` no versionado; script y metodología sí.
9. Sin cambios en medidas, relaciones ni Power Query existentes.
10. Validación del usuario antes del cierre.

## Fuera de alcance

- Construcción de la página del PBIP (fase posterior).
- `META_PLAN` y `ESCENARIO_AJUSTADO` hasta contar con fuente estructurada.
- Proyección a nivel Empresa con modelos estadísticos.
- Modificación de las medidas de rotación vigentes.
- Automatización del refresh del dataset.

## Cierre técnico de Fase 2 — resultados vigentes (2026-09-01)

Esta sección reemplaza **solo como resultado vigente** las cifras provisionales
anteriores; se conservan arriba para mantener la historia metodológica. No se
modificó el PBIP, DAX, Power Query, relaciones ni navegación.

### Correcciones metodológicas finales

- **C9 independiente:** reconstruye directamente `Planta Personal` y concilia
  `Retiros`, `Total-Sena` y `Tasa_Mensual_Retiros` en las 215 combinaciones
  `Periodo × Grupo Empresa`. Pasa con cero discrepancias. Una prueba negativa
  controlada suma un retiro a una fila analítica y C9 cambia a `FAIL` con una
  discrepancia, demostrando que ya no es tautológico.
- **MASE:** cada error se divide por la escala naive calculada únicamente con el
  entrenamiento de su propio origen y después se promedian los errores
  escalados. Para Fundación Challenger, el MASE de `B5_Mediana12M` cambia del
  valor provisional 1,536 a **1,704730**, sin forzar la cifra.
- **Gate temporal:** marzo–julio de 2026 se reserva como holdout final. La
  selección usa solo enero de 2023–febrero de 2026 mediante rolling-origin; el
  ganador se evalúa una vez en los cinco meses reservados. El método productivo
  aprobado se reentrena después con los 43 meses.
- **Dominio:** las 68 predicciones históricas señaladas son negativas y ninguna
  supera 100 %. Las generan `M3`/`M4`/`M5`/`M6` en Fundación (2/11/15/20), `M5`
  en Habitel (5) y `M4`/`M5`/`M6` en Lemco (5/3/7). Se excluyen, no se truncan.
  El reentrenamiento de `M6_HoltWinters` para Grupo Sky produjo además -0,052 %
  en noviembre; se descartó por dominio y la cascada, reutilizando únicamente
  métricas pre-holdout, definió `B3_TasaAgrupada24M` como fallback productivo.
  No se impuso límite superior de 100 %.

### Holdout final y decisión

Las métricas son tasas absolutas expresadas aquí en puntos porcentuales.

| Grupo | Seleccionado antes del holdout | MAE / RMSE selección | MAE / RMSE holdout | MAE / RMSE naive holdout | Decisión final |
|---|---|---:|---:|---:|---|
| Challenger | `M3_Tendencia` | 0,490 / 0,635 pp | 0,889 / 0,940 pp | 1,581 / 1,605 pp | `FORECAST` con M3 |
| Grupo Sky | `M6_HoltWinters` | 1,295 / 1,608 pp | 2,666 / 2,941 pp | 3,339 / 3,435 pp | Pasa holdout, pero da -0,052 % al reentrenar; fallback B3 (`holdout` 1,017 / 1,264 pp) |
| Habitel Hotels | `B2_TasaAgrupadaHist` | 1,778 / 2,181 pp | 1,913 / 2,315 pp | 1,764 / 2,469 pp | No mejora a naive; `BASELINE` M0 |
| Lemco | `M1_NaiveEstacional` | 1,167 / 1,571 pp | 2,444 / 2,924 pp | 1,993 / 2,957 pp | `REFERENCIA_DESCRIPTIVA` B3, no forecast |
| Fundación Challenger | `M1_NaiveEstacional` | 9,114 / 16,759 pp | 21,048 / 24,876 pp | 0,000 / 0,000 pp | `SIN_FORECAST` |

El holdout confirma que no debe ocultarse la falta de mejora de Habitel, Lemco
y Fundación. Habitel conserva un baseline visible; Lemco conserva una magnitud
descriptiva; Fundación no publica número.

### Resultado productivo agosto–diciembre de 2026

| Grupo | Clasificación | Método final | Ago | Sep | Oct | Nov | Dic |
|---|---|---|---:|---:|---:|---:|---:|
| Challenger | `FORECAST` | `M3_Tendencia` | 2,814 % | 2,777 % | 2,740 % | 2,703 % | 2,666 % |
| Grupo Sky | `FORECAST` | `B3_TasaAgrupada24M` | 3,570 % | 3,570 % | 3,570 % | 3,570 % | 3,570 % |
| Habitel Hotels | `BASELINE` | `M0_Naive` | 6,625 % | 6,625 % | 6,625 % | 6,625 % | 6,625 % |
| Lemco | `REFERENCIA_DESCRIPTIVA` | `B3_TasaAgrupada24M` | 1,623 % | 1,623 % | 1,623 % | 1,623 % | 1,623 % |
| Fundación Challenger | `SIN_FORECAST` | — | — | — | — | — | — |

### Bandas de incertidumbre

La muestra no permite afirmar calibración predictiva. Se conserva la
aproximación por RMSE de cada horizonte con el nombre obligatorio **“Banda de
incertidumbre aproximada (80 %)”**. La cobertura histórica observada se expone
junto con cada banda: Challenger 66,7–73,3 %, Grupo Sky 73,3–80,0 % y Habitel
73,3–86,7 %. No se publican bandas para referencia descriptiva ni sin forecast.

### Conciliación `Planta Personal` vs. `RETIROS`

- `Planta Personal`: **3.632** retiros válidos agregados; `RETIROS`: **3.960**
  registros; diferencia neta **328** en 37 combinaciones grupo-mes.
- En texto autorizado de la fuente detalle aparecen 193 registros asociados a
  reingreso, 38 a cesión, 84 a aprendiz/practicante/SENA, 4 a fallecimiento,
  10 a pensión/jubilación y 2 a anulación/cancelación. Hay solapamientos: la
  unión contiene exactamente 328 registros y no existen duplicados exactos.
- Esa regla proxy reconcilia el total, pero no demuestra la regla operativa
  fila a fila: permanecen 5 combinaciones con diferencia residual neta cero y
  diferencia absoluta 6. Se documenta como **brecha de calidad de asignación
  temporal/grupo**. La fuente primaria sigue siendo `Planta Personal`, ya
  depurada en origen; no se modifican fuentes ni se versiona PII.

### Reproducibilidad y evidencia

- Python acordado: **CPython 3.11.9 x64**; un entorno local por PC, fuera de
  OneDrive. `requirements.txt` declara dependencias directas y
  `requirements-lock.txt` fija las transitivas sin rutas absolutas.
- `.venv`, `.venv311`, otros entornos y caches siguen fuera de Git. No se
  eliminan todavía los entornos existentes.
- El notebook usa kernelspec genérico `python3`, importa `run_analysis` como
  fuente única de lógica, no contiene PII y fue validado con 8 celdas de código
  sin errores. Para versionarlo se limpiaron outputs y contadores, siguiendo el
  patrón vigente del proyecto 10; los resultados reproducibles permanecen en
  scripts, pruebas y esta Spec.
- Pruebas automatizadas: C9 positivo, C9 negativo controlado, MASE por origen y
  distinción matemática B1–B3 (tasas agrupadas) frente a B4–B5
  (media/mediana de tasas mensuales).

**Gate de Fase 2:** `PASS con observaciones`. La ciencia de datos es
reproducible y apta para decisión de diseño, pero Habitel debe mostrarse como
baseline, Lemco como referencia descriptiva y Fundación sin forecast. La Fase 3
requiere aprobación explícita separada.

---

## Decisión funcional vigente (2026-09-02)

Supersede la decisión del 2026-09-01 en su tercer punto.

### `Rotación2` se conserva

La página **se mantiene** como vista de **seguimiento y detalle**. El usuario
la considera especialmente valiosa por su tabla de indicadores (visual
`f04eef32576ba115ab23`, ver inventario abajo). **No se reemplaza** por la
página ejecutiva proyectada y **no se elimina ninguno de sus visuales**.

### Se creará una página adicional `Rotación`

De carácter **analítico, comparativo y ejecutivo**. Debe **complementar** a
`Rotación2`, no duplicarla. **No se crea en esta entrega** — su alcance queda
documentado más abajo y requiere el gate metodológico de la sección siguiente.

## Hallazgo metodológico — la Fase 2 no proyectó el índice de rotación

Este es el hallazgo que bloquea la publicación del forecast como "rotación".

El catálogo oficial (`Docs/METRICS_CATALOG.md`) distingue tres medidas que
**no son intercambiables**:

| Medida | Fórmula (DAX vigente en `Tbl_Medidas`) | Qué representa |
|---|---|---|
| `Tasa_Mensual_Retiros` | `DIVIDE(SUM('Planta Ppto'[Retiros]), SUM('Planta Ppto'[Total-Sena]), 0)` | **Salidas**: proporción de retiros sobre la planta |
| `Indice_Rotacion` | `DIVIDE(DIVIDE(SUM(Ingresos) + SUM(Retiros), 2), [PromediodeTotal-Sena], 0)` | **Movimiento de personal**: entradas y salidas promediadas |
| `Variacion_Neta_Personal` | `DIVIDE(SUM(Ingresos) − SUM(Retiros), SUM(Total-Sena), 0)` | Crecimiento/disminución neta. **No es rotación** (el propio catálogo lo aclara) |

Diferencias estructurales entre las dos primeras: el **numerador**
(`Retiros` vs. `(Ingresos + Retiros) / 2`) y el **denominador**
(`SUM(Total-Sena)` vs. `[PromediodeTotal-Sena]`, que promedia por
`DimPeriodoYM[IndexAnioMes]` en vez de sumar). En periodos multi-mes las dos
diferencias se acumulan.

### Consecuencia sobre los resultados de Fase 2

La Fase 2 modeló, con backtesting y holdout, la variable objetivo
`Tasa_Mensual_Retiros` — así consta en la tabla "Definición vigente de
rotación" de esta misma Spec, que ya clasificaba `Indice_Rotacion` como
*"Fuera de alcance como objetivo"*.

Por tanto los valores productivos agosto–diciembre 2026 (Challenger
2,814 % → 2,666 %; Grupo Sky 3,570 %; Habitel Hotels 6,625 %; Lemco 1,623 %)
son **proyecciones y referencias de la TASA DE RETIROS**, y **no pueden
presentarse como forecast de `Indice_Rotacion`**.

Restricciones que se derivan y quedan en firme:

- **No renombrar** las medidas para hacerlas parecer rotación.
- **No sustituir** simplemente una medida por otra en los visuales: cambiar
  `Tasa_Mensual_Retiros` por `Indice_Rotacion` en un visual de forecast
  produciría un número sin respaldo metodológico.
- **No reinterpretar** los valores existentes como rotación.
- Proyectar `Indice_Rotacion` **requiere una nueva validación metodológica**
  (backtesting, holdout y clasificación de fiabilidad propios) antes de
  publicarse. El trabajo de Fase 2 no es transferible: cambia numerador y
  denominador, luego cambian estacionalidad, varianza y comparabilidad frente
  a los baselines.

La tasa de retiros podrá conservarse como **indicador explicativo o
complementario**, nunca como sustituto del índice oficial de rotación.

## Estado estructural de `Rotación2` (documentación del estado preservado)

**Propósito.** Seguimiento y detalle del comportamiento de retiros y rotación
por periodo, empresa, dependencia, área y cargo.

**Identificación.** `ReportSectiondc346876696ee4cba0ab`, 1600×900, **19
visuales**, **visible** (ver "Cambios manuales preservados").

**Fuente de datos.** `Planta Ppto` (desde `Planta Personal` de
`PptovsReal.xlsx`) y `Ppto Retiros` (desde la hoja `RETIROS`), más las
dimensiones `DimPeriodoYM`, `Empresas`, `Estructura` y `AREAS`. Las medidas
viven en `Tbl_Medidas`.

**Filtros de página (3).** `Ppto Retiros[Cargo]` (categórico),
`Ppto Retiros[Detalle]` (categórico) y `Ppto Retiros[Detalle]` (avanzado).
Todos `howCreated: User`.

### Inventario de visuales

| Visual | Tipo | Contenido |
|---|---|---|
| `f04eef32576ba115ab23` | `pivotTable` | **Indicadores de Rotación** — tabla principal (detalle abajo) |
| `5abcdd8fd1c5a1015723` | `pivotTable` | Rotación por Dependencia — `Estructura[DEPENDENCIA]`, `Tot_Colab-Sena`, `Tot_Retiros`, `Índice_Retiros` |
| `8d3d8ab39e15678e422a` | `pivotTable` | Rotación por Área — `AREAS[AREA]`, `Tot_Colab-Sena`, `Tot_Retiros`, `Índice_Retiros` |
| `172920b6976d1cd47b92` | `pivotTable` | Retiros por año — `DimPeriodoYM[Año]`, `Tot_Retiros` |
| `a380cb1e40a7806c5a5e` | `clusteredBarChart` | Retiros por cargo — `Ppto Retiros[Cargo]`, `Tot_Retiros` |
| `126df9a253d67ad12ad0` | `hundredPercentStackedColumnChart` | Retiros por tipo de contrato — `Ppto Retiros[TC]`, `Tot_Retiros` |
| `4d9cf0b713184989d8d5` | `hundredPercentStackedColumnChart` | Retiros por clase de nómina — `Ppto Retiros[Clase de nómina]` (y grupos), `Tot_Retiros` |
| `a4193576029d03d04cb5` | `slicer` | `Empresas[Grupo Empresa]` |
| `aa15d7f81d0d56286d04` | `slicer` | `Estructura[DEPENDENCIA]` |
| `eaddcfb2c7a678354280` | `slicer` | `DimPeriodoYM[Año]` |
| `b855e2c1dc88207b021d` | `slicer` | `DimPeriodoYM[Meses]` |
| `5bcd7dc40410dd5d77c9` | `slicer` | `DimPeriodoYM[Trimestre actual]` |
| `34921556c2a032901604` | `slicer` | `DimPeriodoYM[Trimestre anterior]` |
| `1245d1b8089ddb136783` | `textbox` | Título "Retiros" |
| `f4f3122dee609a558696` | `textbox` | Título "Retiros por Tipo de Contrato" |
| `bc4c2f83a8002303d32e` | `actionButton` | Navegación interna ("Volver al informe") |
| `8afe56be6a80b0ed0b5d` | `shape` | Elemento de diseño |
| `79fec56357a0d05241c9`, `a266c4a073606ad97006` | (sin `visualType`) | Elementos de diseño/contenedor |

### `Indicadores de Rotación` — tabla que se preserva

Visual `f04eef32576ba115ab23`, `pivotTable`, 13 filtros. Es la tabla que el
usuario señaló como especialmente valiosa. **No se elimina ni se transforma.**

| Rol | Campo / medida | Tabla |
|---|---|---|
| Eje | `Grupo Empresa` | `Empresas` |
| Eje | `Meses`, `MesAnio` | `DimPeriodoYM` |
| Valor | `Ingresos` (agregado) | `Planta Ppto` |
| Valor | `Retiros` (agregado) | `Planta Ppto` |
| Valor | `PromediodeTotal-Sena` | `Tbl_Medidas` |
| Valor | `Variacion_Neta_Personal` | `Tbl_Medidas` |
| Valor | **`Indice_Rotacion`** | `Tbl_Medidas` |
| Valor | `Tasa_Mensual_Retiros` | `Tbl_Medidas` |
| Valor | `Tasa_Acumulada_Retiros_Segun_Tipo` | `Tbl_Medidas` |

Que esta tabla ya exponga **`Indice_Rotacion` y `Tasa_Mensual_Retiros` lado a
lado** es justamente lo que hace visible la diferencia metodológica de la
sección anterior, y es una razón adicional para conservarla.

### Medidas auxiliares usadas en la página

| Medida | Definición | Nota |
|---|---|---|
| `Tot_Retiros` | `COUNT('Ppto Retiros'[Mes])` | Conteo de registros de retiro |
| `Tot_Colab-Sena` | `CALCULATE(COUNT('PLANTA DE PERSONAL'[ID]), 'PLANTA DE PERSONAL'[TIPO_CONTR] <> "CONTRATO APRENDIZAJE")` | Excluye aprendices |
| `Índice_Retiros` | `[Tot_Retiros] / [Tot_Colab-Sena]` | **Distinta** de `Tasa_Mensual_Retiros`: se calcula sobre `Ppto Retiros`/`PLANTA DE PERSONAL`, no sobre `Planta Ppto` |

`Índice_Retiros` es una cuarta medida a no confundir con las tres del catálogo:
comparte el concepto de "retiros sobre planta" con `Tasa_Mensual_Retiros`, pero
usa tablas y granularidad distintas.

### Relación conceptual con `Retiros` y con la futura `Rotación`

- **`Retiros`** (`ReportSection6a1196bf8c963b709405`) = diagnóstico individual:
  quién, por qué, motivo, antigüedad. Sin cambios.
- **`Rotación2`** = seguimiento y detalle agregado por periodo y estructura.
  **Se conserva.**
- **`Rotación`** (futura) = lectura ejecutiva y comparativa. Complementa, no
  duplica: no debe reproducir el detalle por dependencia/área/cargo que ya
  entrega `Rotación2`.

## Cambios manuales preservados en esta entrega

Edición manual del usuario en Power BI Desktop, verificada archivo por archivo
comparando HEAD contra el estado guardado. El criterio fue **semántico**: se
descartaron los archivos cuyo diff, ignorando espacios y el bump de `$schema`,
no altera ningún campo, medida, literal ni propiedad.

| Archivo | Cambio manual |
|---|---|
| `.../ReportSectiondc346876696ee4cba0ab/page.json` | **Se elimina `"visibility": "HiddenInViewMode"`** → la página pasa a ser visible en modo lectura |
| `.../visuals/5abcdd8fd1c5a1015723/visual.json` | Título `'Rotación por Dependencia 2025'` → `'Rotación por Dependencia'` |
| `.../visuals/8d3d8ab39e15678e422a/visual.json` | Se retira el filtro fijo del literal `'2025'` |
| `.../visuals/a380cb1e40a7806c5a5e/visual.json` | Se retiran los filtros fijos `'2024'` y `'2025'`; el slicer pasa a `isInvertedSelectionMode` |

**Patrón de la edición:** desacoplar la página de los años fijos 2024/2025 para
que responda a los segmentadores, y hacerla visible como vista de seguimiento.
Es coherente con la decisión de conservarla.

La visibilidad recupera además la consistencia con
`Docs/BI_GUIDELINES.md`, que ya describía `Rotacion2` como **Visible** mientras
`Docs/CHANGELOG.md` registraba la adición posterior de `HiddenInViewMode`.

### Churn de Desktop excluido — no atribuible al usuario

| Archivo | Por qué se excluye |
|---|---|
| `.../visuals/f04eef32576ba115ab23/visual.json` | 150 líneas de diff pero **cero cambio semántico**: mismas tablas, campos, medidas y literales. Solo reserialización `$schema` 2.4.0 → 2.10.0. **La tabla `Indicadores de Rotación` no fue modificada por el usuario** |
| `cultures/es-ES.tmdl` (1.166 líneas) | Metadata lingüística autogenerada |
| `model.tmdl` | `PBI_QueryOrder` incorpora `Dim_Estructura_Organizacional` (registro automático) |
| `Tbl_Medidas.tmdl`, `Dim_Estructura_Organizacional.tmdl` | Solo espacios / `formatString` idéntico |
| `Dim_Area.tmdl`, `Dim_Dependencia.tmdl` | Línea en blanco final regenerada por Desktop |
| `diagramLayout.json` | Ruido decimal de coordenadas |
| `pages/pages.json` | `activePageName` — estado de UI al guardar |
| 20 archivos con diff nulo tras normalizar | Solo fin de línea o bump de `$schema` |
| ~48 visuales de otras páginas | Churn ajeno a `Rotación2` |

## Página provisional `Rotación proyectada` — problemas abiertos, sin corregir

La página provisional **no existe en `main`**; vive en la rama de trabajo
`feat/pbip-008-rotacion-proyectada-powerbi`. El usuario reportó estas
inconsistencias, que **no se declaran resueltas ni se corrigen todavía**:

1. `Grupo Empresa` muestra Challenger pero la clasificación aparece como TODOS.
2. La síntesis futura sigue mostrando el consolidado.
3. El horizonte dice agosto–diciembre pero el eje termina en julio.
4. No aparecen las series futuras.
5. `Estado de la proyección` está vacío.
6. `Referencia futura` / síntesis es poco interpretable.
7. Los colores no corresponden correctamente a la marca LEMCO.

**Orden de resolución:** primero se cierra el problema metodológico (qué se
proyecta y con qué respaldo); solo después tiene sentido corregir la
presentación. Arreglar los visuales sobre una base metodológica equivocada
consolidaría el error.

## Alcance previsto de la futura página `Rotación` (documentado, no implementado)

### Comparación

- Índice de rotación año actual vs. año anterior.
- Variación interanual.

### Evolución

- Comportamiento mensual, tendencia e identificación de cambios relevantes.

### Contratación

- Análisis por tipo de contrato y clase de contrato.

### Diagnóstico organizacional

- Detalle por Dependencia, Área y Cargo.

### Proyección — condicionada al gate metodológico

Solo cuando exista una metodología validada para `Indice_Rotacion`:

- `REAL`, `FORECAST`, `BASELINE`.
- Bandas de incertidumbre.
- Comparación real vs. esperado.
- Exposición por empresa.

### Identidad visual — marca LEMCO

Fuente principal: `Assets/Brand/Manual Marca Grupo LEMCO.pdf`.

| Color | Uso previsto |
|---|---|
| `#1B487F` | Azul principal |
| `#1A3059` | Azul profundo |
| `#000032` | Azul casi negro |
| `#0B1C35` | Fondo oscuro |
| `#F7931E` | Naranja — **reservado para énfasis** |

Tipografía `Outfit` cuando Power BI Desktop/Service sea compatible; fallback
`Segoe UI`. La página debe sentirse ejecutiva, moderna, sobria y coherente con
el resto del dashboard.

## Gate para construir `Rotación`

Antes de crear la página deben resolverse, en este orden:

1. **Definir la variable objetivo.** Decidir si la página proyecta
   `Indice_Rotacion`, `Tasa_Mensual_Retiros` o ambas con etiquetas separadas.
   Sin esta decisión no se puede diseñar el visual de forecast.
2. **Validar metodológicamente `Indice_Rotacion`** si se elige como objetivo:
   backtesting, holdout y clasificación de fiabilidad propios, con el mismo
   rigor aplicado en Fase 2 a `Tasa_Mensual_Retiros`. No se hereda el
   resultado anterior.
3. **Confirmar el reparto de contenido** entre `Rotación2` y `Rotación` para
   que complementen sin duplicar.
4. **Aprobar la maqueta visual** con la paleta LEMCO antes de crear visuales.
5. **Decidir el destino de la página provisional** de la rama
   `feat/pbip-008-rotacion-proyectada-powerbi`: descartarla o reconstruirla
   sobre la metodología validada.

Mientras el punto 2 siga abierto, cualquier número presentado como "rotación
proyectada" carece de respaldo. La Fase 3 sigue requiriendo aprobación
explícita separada.
