# Catalogo de Metricas y Medidas DAX

> Fuente oficial de todas las medidas DAX del modelo.
> Las expresiones completas se encuentran en los archivos `.tmdl` de cada tabla en `PBIP/Proyecto.SemanticModel/definition/tables/`.

---

## Organizacion por dominio

Las medidas del modelo estan centralizadas en la tabla contenedora `Tbl_Medidas`. Se conservaron los nombres, expresiones DAX, formatos y `lineageTag` de las medidas; la organizacion funcional se realiza mediante carpetas de visualizacion.

| Tabla contenedora | Carpeta display | Medidas | Dominio |
|---|---|---:|---|
| `Tbl_Medidas` | `00 Utilidades` | 1 | Filtros y soporte transversal |
| `Tbl_Medidas` | `01 HeadCount HC` | 11 | HeadCount general |
| `Tbl_Medidas` | `01 HeadCount HC - Demografico` | 3 | KPIs demograficos |
| `Tbl_Medidas` | `02 Ppto vs Real` | 38 | Presupuesto, real, eficiencia y productividad |
| `Tbl_Medidas` | `03 Ingresos y Retiros` | 12 | Ingresos, retiros, rotacion e indices |
| `Tbl_Medidas` | `04 Ausentismos` | 9 | Ausentismo laboral |
| `Tbl_Medidas` | `05 SST` | 6 | Seguridad y Salud en el Trabajo |
| `Tbl_Medidas` | `06 Seleccion` | 4 | Procesos de seleccion |
| `Tbl_Medidas` | `07 SENA` | 1 | Unidades SENA |
| `Tbl_Medidas` | `11 HTML Content` | 4 | Medidas que devuelven HTML para visual HTML Content |

> Inventario detallado: `Outputs/documentation/inventario_medidas_reorganizadas_2026-06-11.csv`.

---

## 1. HeadCount y Demografia (`PLANTA DE PERSONAL`)

| Medida | Formato | Descripcion | Expresion simplificada |
|---|---|---|---|
| `Tot_empleados` | `#,0` | Total de colaboradores activos en el contexto de filtro | `COUNT([ID])` |
| `Tot_Fem` | `#,0` | Colaboradoras de sexo femenino | `CALCULATE([Tot_empleados], [SEXO]="FEMENINO")` |
| `Tot_Mas` | `#,0` | Colaboradores de sexo masculino | `CALCULATE([Tot_empleados], [SEXO]="MASCULINO")` |
| `%FEM` | `0 %` | Participacion femenina sobre el total | `[Tot_Fem]/[Tot_empleados]` |
| `%MASC` | `0 %` | Participacion masculina sobre el total | `[Tot_Mas]/[Tot_empleados]` |
| `Tot_Colab-Sena` | `#,0` | Total excluyendo contratos de aprendizaje SENA | `CALCULATE(COUNT([ID]), [TIPO_CONTR]<>"CONTRATO APRENDIZAJE")` |
| `Tot_Colab-Directos` | `#,0` | Total con contrato fijo o indefinido | `CALCULATE(..., TIPO_CONTR="CONTRATO FIJO") + CALCULATE(..., TIPO_CONTR="CONTRATO INDEFINIDO")` |
| `Tot_empleados_Promedio` | general | Promedio de colaboradores iterando por valores de mes | `AVERAGEX(VALUES([Mes]), CALCULATE(COUNT([ID])))` |
| `Tot_empleados_Promedio_Sin_Aprendices` | `0.00` | Promedio mensual de colaboradores excluyendo tipos de contrato de aprendizaje y SENA normalizados en la medida | `AVERAGEX(VALUES([MES]), CALCULATE(COUNT([ID]), KEEPFILTERS(...)))` |
| `Prom_Colaboradores` | `0` | Promedio hardcodeado de Enero a Julio (7 meses fijos) | Suma de 7 meses / 7 — **ADVERTENCIA: valor hardcodeado, no dinamico** |
| `orden` | — | Medida vacia sin expresion DAX. Placeholder sin uso confirmado | — |

> **Atencion:** La medida `Prom_Colaboradores` divide siempre entre 7 independientemente del contexto. Es incorrecta para cualquier periodo fuera de enero-julio. Ver [DATA_MODEL.md — Riesgos](DATA_MODEL.md#riesgos-del-modelo).

---

## 2. Presupuesto vs Real (`Planta Ppto`)

### Totales por tipo de contrato

| Medida | Formato | Descripcion |
|---|---|---|
| `Resumen` | `0` | Suma de columna `Total` (planta total) |
| `Tot_Ano` | `#,0` | Suma de todos los tipos: `[Tot_Fijo]+[Tot_Indef]+[Tot_Temp]+[Tot_Sena]` |
| `Tot_Indef` | `#,0` | Suma de colaboradores indefinidos |
| `Tot_Fijo` | `0` | Suma de colaboradores con contrato fijo |
| `Tot_Temp` | `0` | Suma de temporales |
| `Tot_Sena` | `0` | Suma de aprendices SENA |
| `SumadeTotal-Sena` | `0` | Suma de `Total-Sena` |

### Promedios YTD (hasta el mes seleccionado)

| Medida | Formato | Descripcion | Patron |
|---|---|---|---|
| `tot_Ano_prom` | `#,0.00` | Promedio YTD del total de planta | `DIVIDE(SUM_hasta_mes, DISTINCTCOUNT_meses)` |
| `tot_Ano_Indef_Prom` | `#,0` | Promedio YTD de indefinidos | Mismo patron |
| `tot_Ano_Fijo_Prom` | general | Promedio YTD de fijos | Mismo patron |
| `tot_Ano_Temp_prom` | general | Promedio YTD de temporales | Mismo patron |
| `tot_Ano_Sena_prom` | `0` | Promedio YTD de SENA | Mismo patron |
| `PromediodeTotal-Sena` | general | Promedio de `Total-Sena` iterando por `IndexAnioMes` via `DimPeriodoYM` | `AVERAGEX(VALUES(DimPeriodoYM[IndexAnioMes]), CALCULATE([SumadeTotal-Sena]))` |

### Promedios YTD con soporte de desglose por empresa (ISINSCOPE)

| Medida | Descripcion |
|---|---|
| `tot_Ano_Indef_PromEmpresas_FIX` | Promedio YTD de indefinidos: muestra promedio por empresa cuando hay drill-down, total cuando no |
| `tot_Ano_Fijo_PromEmpresas_FIX` | Idem para fijos |
| `tot_Ano_Sena_PromEmpresas_FIX` | Idem para SENA |
| `tot_Ano_Temp_PromEmpresas_FIX` | Idem para temporales |

> Estas medidas usan `ISINSCOPE('Planta Ppto'[Empresa])` para detectar el nivel de jerarquia y devolver el calculo apropiado.

### Promedios anuales reales (serie temporal)

| Medida | Descripcion |
|---|---|
| `Prom_Anual_Real` | Promedio anual real del total (AVERAGEX por mes) |
| `Prom_Anual_Real_Linea` | Devuelve `[Prom_Anual_Real]` solo cuando el contexto es "Real" (para linea de referencia en graficos) |
| `Prom_Anual_Real_Indef` | Promedio anual real de indefinidos |
| `Prom_Anual_Real_Fijo` | Promedio anual real de fijos |
| `Prom_Anual_Real_Temp` | Promedio anual real de temporales |
| `Prom_Anual_Real_Sena` | Promedio anual real de SENA |
| `Prom_Colab` | `CALCULATE(AVERAGE([Total]), [Ppto/Real]="REAL")` |
| `Prom_Colab_Directo` | Promedio de indefinidos + fijos reales |

### KPI Ppto vs Real (variaciones interanuales)

| Medida | Formato | Descripcion |
|---|---|---|
| `Var_Ppto` | `0 %` | Variacion del presupuesto 2025 vs 2024: `(Ppto2025/Ppto2024) - 1` |
| `Var_Real` | `0 %` | Variacion de la planta real 2025 vs 2024 |
| `KPI_PPTO` | icono | Flecha arriba/abajo segun `[Var_Ppto] > 0` (UNICHAR 129093/129095) |
| `KPI_REAL` | icono | Flecha arriba/abajo segun `[Var_Real] > 0` |

### Eficiencia y Gasto Laboral

| Medida | Formato | Descripcion |
|---|---|---|
| `Efic` | `0.00 %` | Gasto Personal / Ventas (MM) |
| `%Efiprom` | `0.00 %` | Ppto Gasto Personal / Ppto Ventas (MM) — indice objetivo |
| `KPI_EFI` | icono | Flecha: si `[Efic] > [%Efiprom]` el gasto supera lo presupuestado |
| `Var_GL` | general | `[Efic] / [%Efiprom]` — cociente de eficiencia |
| `Cump_GL` | `0.00 %` | Gasto Personal real / Gasto Personal presupuestado |
| `Efic_Emp` | moneda COP | Ventas (MM) / colaboradores sin SENA (productividad por empleado) |

### Presentacion monetaria de Gasto Laboral

| Medida | Formato | Descripcion |
|---|---|---|
| `GL_Ppto_Gasto_Personal` | Dinamico | Conserva `SUM('Planta Ppto'[Ppto Gasto Personal])`; millones con una cifra decimal para Challenger/consolidado y valor completo con una cifra decimal para otros negocios. |
| `GL_Gasto_Personal` | Dinamico | Conserva `SUM('Planta Ppto'[Gasto Personal])` y aplica la misma regla de presentacion. |
| `GL_Usar_Millones` | Booleano | Activa la variante en millones para Challenger exclusivo, vista sin filtro o seleccion de todos los grupos. |
| `GL_Ppto_Visual_Challenger` | Moneda numerica | Presupuesto visible exclusivamente en la variante de grafico configurada en millones. |
| `GL_Real_Visual_Challenger` | Moneda numerica | Ejecucion visible exclusivamente en la variante de grafico configurada en millones. |
| `GL_Ppto_Visual_Otros` | Moneda numerica | Presupuesto visible exclusivamente en la variante de grafico con unidades automaticas. |
| `GL_Real_Visual_Otros` | Moneda numerica | Ejecucion visible exclusivamente en la variante de grafico con unidades automaticas. |

### Presentacion monetaria de Productividad

| Medida | Formato | Descripcion |
|---|---|---|
| `Prod_Gasto_Personal` | Moneda numerica | `SUM('Planta Ppto'[Gasto Personal])`; conserva el calculo base para la pagina Productividad. |
| `Prod_Ingreso_Operacional` | Moneda numerica | `SUM('Planta Ppto'[Ventas (MM)])`; conserva el calculo base de ingreso operacional. |
| `Prod_Usar_Millones` | Booleano | Activa millones para Challenger exclusivo, vista sin filtro o seleccion de todos los grupos; otros negocios usan valor completo. |
| `Prod_Gasto_Personal_Tabla` | Dinamico | Reutiliza `[Prod_Gasto_Personal]`; millones para Challenger/consolidado y valor entero completo para otros negocios. |
| `Prod_Ingreso_Operacional_Tabla` | Dinamico | Reutiliza `[Prod_Ingreso_Operacional]` con la misma regla de presentacion. |
| `Prod_Efic_Tabla` | `0.0 %` | Reutiliza `[Efic]` para mantener la productividad y los totales sin alterar su logica. |
| `Titulo_Productividad_Gasto_Laboral` | Texto | Genera el titulo del grafico mensual con el ano seleccionado; si hay varios anos, indica que existen anos seleccionados. |
| `Subtitulo_Productividad_Comparativo_Acumulado` | Texto | Genera el subtitulo del comparativo acumulado con los meses ordenados por `Mes[Numero]`; distingue un mes, rangos continuos, selecciones no consecutivas y contexto anual. |

### Rotacion e Indice de Retiros

Renombradas el 2026-08-06 para que el nombre tecnico represente la formula que calculan (ver `Specs/0016_renombramiento_medidas_rotacion_retiros.md`). Los retiros ya vienen depurados desde el archivo fuente (`PptovsReal.xlsx`, hoja `Planta Personal`, columna `Retiros`); las medidas DAX no duplican esas exclusiones.

| Medida | Nombre anterior | Formato | Descripcion |
|---|---|---|---|
| `Variacion_Neta_Personal` | `Ind_Rot` | `0 %` | `DIVIDE(SUM(Ingresos) - SUM(Retiros), SUM(Total-Sena), 0)`. Variacion neta de planta (crecimiento o disminucion), no es un indice de rotacion. |
| `Tasa_Mensual_Retiros` | `Ind_Retiros` | `0.00 %` | `DIVIDE(SUM(Retiros), SUM(Total-Sena), 0)` |
| `Indice_Rotacion` | *(medida nueva)* | `0.00 %` | `DIVIDE(DIVIDE(SUM(Ingresos) + SUM(Retiros), 2), [PromediodeTotal-Sena], 0)`. Indice de rotacion (movimiento de personal); para periodos de varios meses el denominador usa el promedio de `Total-Sena`, no la suma. |

### Poblacion de origen de `Ingresos` y `Retiros` (reglas de exclusion)

Documentado el 2026-09-02 al cerrar el Gate A de `PBIP-008`. Ver
`Specs/0028_plan_implementacion_rotacion_proyectada.md`.

`Planta Ppto[Ingresos]` y `[Retiros]` **no son conteos brutos**: provienen de
formulas `COUNTIFS` en la hoja `Planta Personal` de `PptovsReal.xlsx` que
excluyen poblacion. Toda medida que los consuma
(`Tasa_Mensual_Retiros`, `Indice_Rotacion`, `Variacion_Neta_Personal`) hereda
esas exclusiones.

| Exclusion | Campo | `Ingresos` | `Retiros` |
|---|---|---|---|
| `APRENDIZ SENA` | `Cargo` / `Descripcion Cargo` | Si | Si |
| `PRACTICANTE` | `Cargo` / `Descripcion Cargo` | Si | Si |
| `*REINGRESO*` | `Detalle` / `Motivo Movimiento` | Si | Si |
| `*FALLECIMIENTO*` | `Detalle` | No | Si |
| `PENSION POR JUBILACION` | `Detalle` | No | Si |
| `CESION DE CONTRATO` / `CESION CONTRATO` | `Detalle` | No | Si |

Las cuatro exclusiones que no aplican a ingresos son **causales de salida**;
su ausencia es correcta y verificada (0 ocurrencias en la hoja `INGRESOS`).

> **Advertencia de comparabilidad.** `Indice_Retiros` (seccion 3, sobre
> `Ppto Retiros`) usa el conteo **bruto** de registros, sin estas exclusiones.
> No es comparable con `Tasa_Mensual_Retiros` pese a la similitud de nombre:
> en 2025-2026 la poblacion bruta supera a la depurada en ~21 %.

> **Deuda conocida.** Las formulas no fueron homogeneas historicamente. En
> `Ingresos` las exclusiones estan ausentes en 2023-01 a 2024-12 y en
> 2025-05 a 2025-10; en `Retiros`, ausentes hasta 2024-12. El impacto medido
> es 26 registros en ingresos (0,78 %) y 3 en retiros (0,1 %). Cualquier serie
> destinada a modelamiento debe reconstruirse aplicando las exclusiones de
> forma uniforme en todos los periodos.

### Denominador de rotacion — `Total-Sena`

`Total-Sena` es el **denominador oficial** de `Tasa_Mensual_Retiros` e
`Indice_Rotacion` (este ultimo via `[PromediodeTotal-Sena]`).

Corresponde a los **colaboradores activos del cierre mensual excluyendo la
poblacion de aprendizaje SENA** — el mismo criterio que aplica la pagina
`Sociodemografico` al excluir `Contrato de Aprendizaje` en su slicer.

Validado contra `Consolidado 2025.xlsx` en 19 meses (2025-01 a 2026-07):
excluyendo aprendices **y** el valor `SENA` la diferencia acumulada es 18
registros, con 16 de 19 meses exactos. Excluyendo solo `*APRENDIZ*` la
diferencia sube a 1.092, porque desde 2025-09 esa poblacion se etiqueta como
`SENA`. Ver [DATA_PIPELINE.md](DATA_PIPELINE.md), seccion "Arquitectura de
fuentes de HeadCount".

No se debe usar `Total` como denominador de rotacion: incluye aprendices.

### Medidas de periodo con `DimPeriodoYM`

| Medida | Descripcion |
|---|---|
| `Total-Sena YTD Ano Seleccionado` | Suma YTD de `Total-Sena` para el ano seleccionado en el slicer de `DimPeriodoYM` |

---

## 3. Retiros (`Ppto Retiros`)

| Medida | Formato | Descripcion |
|---|---|---|
| `Tot_Retiros` | `#,0` | Conteo de registros de retiros en el contexto (`COUNT([Mes])`) |
| `Indice_Retiros` | `0.00 %` | `[Tot_Retiros] / [Tot_Colab-Sena]` |

> Nota de correccion documental (2026-08-06): esta seccion citaba una medida `Indice_Rotacion` con formula `([Tot_ingresos] - [Tot_Retiros]) / [Tot_Colab-Sena]` en el contexto de `Ppto Retiros`. Esa medida no existe en el modelo actual (no se encontro en ningun archivo `.tmdl` ni `Tot_ingresos` como medida real); se trataba de documentacion desactualizada. La medida `Indice_Rotacion` vigente vive en `Tbl_Medidas` (ver seccion "Rotacion e Indice de Retiros" arriba) con una formula distinta, basada en `Planta Ppto[Ingresos]`/`[Retiros]`/`[Total-Sena]`.

---

## 4. Ausentismo (`AUSENTISMOS`)

| Medida | Formato | Descripcion |
|---|---|---|
| `ConteoP` | `#,0` | Personas con ausentismo: `DISTINCTCOUNT([Identificacion])` |
| `CMujeres` | `0 %` | Porcentaje de personas con ausentismo de sexo femenino sobre `[ConteoP]` |
| `CHombres` | `0 %` | Porcentaje de personas con ausentismo de sexo masculino sobre `[ConteoP]` |
| `%AusM` | `0 %` | `[ConteoP] / [Prom_Colaboradores]` — Tasa de personas ausentes |
| `Ausentismo` | `#,0` | Total dias: `IF(ISBLANK(SUM([Cantidad Real])), 0, SUM([Cantidad Real]))` |
| `DIAS_AUSENTISMO` | `0` | `SUM([Cantidad Real])` — Version sin tratamiento de blancos |
| `Tasa Ausentismo` | `0.00 %` | `[Ausentismo] / ([Tot_empleados] * SUM([Dias Lab solo fds Domingos]))` |
| `Tasa Ausentismo_EL` | `0.00 %` | `[Ausentismo] / ([Tot_Colab-Directos] * SUM([Dias Lab solo fds Domingos]))` — Solo empleados directos |
| `Tasa_Ausent_Anual` | `0.00 %` | `[Ausentismo] / ([Prom_Colab] * SUM([Dias Lab solo fds Domingos]))` — Con promedio anual real |

> Las tasas de ausentismo usan `Dias Laborales[Dias Lab solo fds Domingos]` como denominador de dias habiles.

---

## 5. SST (Seguridad y Salud en el Trabajo)

### Tabla `SST GENERAL`

| Medida | Formato | Descripcion |
|---|---|---|
| `M_Frecuencia` | `0.00` | `(SUM(#Accidentes) / SUM(Empleados)) * 100` |
| `M_Severidad` | `0.00` | `((SUM(Dias de Ausentismo) + SUM(Dias Cargados)) / SUM(Empleados)) * 100` |
| `MSector` | `0.00` | `AVERAGE(Indice Accidentalidad del Sector)` — promedio del indice sectorial de referencia |
| `Tasa_Acc` | `0.00` | `(SUM(#Accidentes) / CALCULATE([tot_Ano_prom], [Ppto/Real]="Real")) * 100` — Referencia cruzada con `Planta Ppto` |
| `Dias Ausentismo Acc.Lab` | `0` | `SUM(Dias de Ausentismo) + SUM(Dias Cargados)` |

### Tabla `ACCIDENTALIDAD`

| Medida | Formato | Descripcion |
|---|---|---|
| `Tot_Accidentes` | `0` | `COUNT([Empresa])` — Conteo de registros de accidentes |

---

## 6. Seleccion (medidas ocultas en `Seleccion Challenger`)

| Medida | Formato | Descripcion |
|---|---|---|
| `Solicitudes` | `0` | `COUNT([Empresa])` — Requisiciones de seleccion |
| `Solicitudes2024` | `0` | `CALCULATE([Solicitudes], [Ano_Met]=2024)` — Filtrado por ano de meta |

> Estas medidas estan marcadas como `isHidden = true`. No son visibles directamente en el panel de campos.

---

## 7. Medidas transversales (`Tbl_Medidas`)

| Medida | Formato | Descripcion |
|---|---|---|
| `Cantidad_Retiros` | `0` | `SUM('Planta Ppto'[Retiros])` — Retiros desde tabla `Planta Ppto` |
| `Cantidad_Retiros_Voluntarios` | `0` | `SUM('Planta Ppto'[Retiros Voluntarios])` |
| `Cantidad_Retiros_Involuntarios` | `0` | `[Cantidad_Retiros] - [Cantidad_Retiros_Voluntarios]` |
| `Tasa_Acumulada_Retiros` | `0.00 %` | `DIVIDE([Cantidad_Retiros], [PromediodeTotal-Sena], 0)`. Antes `Rotacion_Anual_Acumulada`. |
| `Tasa_Acumulada_Retiros_Voluntarios` | `0.00 %` | `DIVIDE([Cantidad_Retiros_Voluntarios], [PromediodeTotal-Sena], 0)`. Antes `Rotacion_Voluntaria_Anual_Acumulada`. |
| `Tasa_Acumulada_Retiros_Involuntarios` | `0.00 %` | `DIVIDE([Cantidad_Retiros_Involuntarios], [PromediodeTotal-Sena], 0)`. Antes `Rotacion_Involuntaria_Anual_Acumulada`. |
| `Tasa_Acumulada_Retiros_Segun_Tipo` | `0.00 %` | Conmuta entre `[Tasa_Acumulada_Retiros_Voluntarios]`, `[Tasa_Acumulada_Retiros_Involuntarios]` o `[Tasa_Acumulada_Retiros]` segun `'Ppto Retiros'[Tipo de retiro]`. Antes `Rotacion_Segun_Tipo`. |
| `Filtro Trimestre Slicer` | `0` | Medida booleana (0/1) que filtra segun la seleccion del slicer "Trimestre actual" o "Trimestre anterior" usando `DimPeriodoYM`. Retorna 1 si el periodo esta dentro del rango seleccionado, 1 si no hay seleccion (no filtra). |

---

## Dependencias cruzadas entre tablas

Algunas medidas referencian tablas distintas a la que las contiene:

| Medida | Tabla contenedora | Referencia cruzada |
|---|---|---|
| `Tasa Ausentismo` | `AUSENTISMOS` | `PLANTA DE PERSONAL[Tot_empleados]`, `Dias Laborales[Dias Lab solo fds Domingos]` |
| `Tasa_Acc` | `SST GENERAL` | `Planta Ppto` via `[tot_Ano_prom]` |
| `Indice_Retiros` | `Ppto Retiros` | `PLANTA DE PERSONAL[Tot_Colab-Sena]` |
| `Indice_Rotacion` | `Tbl_Medidas` | `Planta Ppto[Ingresos]`, `Planta Ppto[Retiros]`, `[PromediodeTotal-Sena]` |
| `Tasa_Acumulada_Retiros` | `Tbl_Medidas` | `Planta Ppto[Retiros]` via `[Cantidad_Retiros]`, `[PromediodeTotal-Sena]` |
| `%AusM` | `AUSENTISMOS` | `PLANTA DE PERSONAL[Prom_Colaboradores]` |

> Las dependencias cruzadas son funcionales pero aumentan el acoplamiento entre tablas y deben tenerse en cuenta al hacer cambios en los modelos de datos de origen.
