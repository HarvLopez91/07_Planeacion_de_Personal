# Catalogo de Metricas y Medidas DAX

> Fuente oficial de todas las medidas DAX del modelo.
> Las expresiones completas se encuentran en los archivos `.tmdl` de cada tabla en `PBIP/Proyecto.SemanticModel/definition/tables/`.

---

## Organizacion por dominio

Las medidas del modelo estan centralizadas en la tabla contenedora `Tbl_Medidas`. Se conservaron los nombres, expresiones DAX, formatos y `lineageTag` de las medidas; la organizacion funcional se realiza mediante carpetas de visualizacion.

| Tabla contenedora | Carpeta display | Medidas | Dominio |
|---|---|---:|---|
| `Tbl_Medidas` | `00 Utilidades` | 1 | Filtros y soporte transversal |
| `Tbl_Medidas` | `01 HeadCount HC` | 10 | HeadCount general |
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

### Presentacion monetaria de Productividad

| Medida | Formato | Descripcion |
|---|---|---|
| `Prod_Gasto_Personal` | Moneda numerica | `SUM('Planta Ppto'[Gasto Personal])`; conserva el calculo base para la pagina Productividad. |
| `Prod_Ingreso_Operacional` | Moneda numerica | `SUM('Planta Ppto'[Ventas (MM)])`; conserva el calculo base de ingreso operacional. |
| `Prod_Usar_Millones` | Booleano | Activa millones para Challenger exclusivo, vista sin filtro o seleccion de todos los grupos; otros negocios usan valor completo. |
| `Prod_Gasto_Personal_Tabla` | Dinamico | Reutiliza `[Prod_Gasto_Personal]`; millones para Challenger/consolidado y valor entero completo para otros negocios. |
| `Prod_Ingreso_Operacional_Tabla` | Dinamico | Reutiliza `[Prod_Ingreso_Operacional]` con la misma regla de presentacion. |
| `Prod_Efic_Tabla` | `0.0 %` | Reutiliza `[Efic]` para mantener la productividad y los totales sin alterar su logica. |

### Rotacion e Indice de Retiros

| Medida | Formato | Descripcion |
|---|---|---|
| `Ind_Rot` | `0 %` | `(Ingresos - Retiros) / Total-Sena` |
| `Ind_Retiros` | `0.00 %` | `SUM(Retiros) / SUM(Total-Sena)` |

### Medidas de periodo con `DimPeriodoYM`

| Medida | Descripcion |
|---|---|
| `Total-Sena YTD Ano Seleccionado` | Suma YTD de `Total-Sena` para el ano seleccionado en el slicer de `DimPeriodoYM` |

---

## 3. Retiros (`Ppto Retiros`)

| Medida | Formato | Descripcion |
|---|---|---|
| `Tot_Retiros` | `#,0` | Conteo de registros de retiros en el contexto (`COUNT([Mes])`) |
| `Indice_Rotacion` | `0.00 %` | `([Tot_ingresos] - [Tot_Retiros]) / [Tot_Colab-Sena]` (referencia cruzada con `Ppto Ingresos` y `PLANTA DE PERSONAL`) |
| `Indice_Retiros` | `0.00 %` | `[Tot_Retiros] / [Tot_Colab-Sena]` |

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
| `Rotacion_Anual_Acumulada` | `0.00 %` | `DIVIDE([Cantidad_Retiros], [PromediodeTotal-Sena], 0)` |
| `Filtro Trimestre Slicer` | `0` | Medida booleana (0/1) que filtra segun la seleccion del slicer "Trimestre actual" o "Trimestre anterior" usando `DimPeriodoYM`. Retorna 1 si el periodo esta dentro del rango seleccionado, 1 si no hay seleccion (no filtra). |

---

## Dependencias cruzadas entre tablas

Algunas medidas referencian tablas distintas a la que las contiene:

| Medida | Tabla contenedora | Referencia cruzada |
|---|---|---|
| `Tasa Ausentismo` | `AUSENTISMOS` | `PLANTA DE PERSONAL[Tot_empleados]`, `Dias Laborales[Dias Lab solo fds Domingos]` |
| `Tasa_Acc` | `SST GENERAL` | `Planta Ppto` via `[tot_Ano_prom]` |
| `Indice_Rotacion` | `Ppto Retiros` | `PLANTA DE PERSONAL[Tot_Colab-Sena]` |
| `Rotacion_Anual_Acumulada` | `Tbl_Medidas` | `Planta Ppto[Retiros]`, `Planta Ppto[PromediodeTotal-Sena]` |
| `%AusM` | `AUSENTISMOS` | `PLANTA DE PERSONAL[Prom_Colaboradores]` |

> Las dependencias cruzadas son funcionales pero aumentan el acoplamiento entre tablas y deben tenerse en cuenta al hacer cambios en los modelos de datos de origen.
