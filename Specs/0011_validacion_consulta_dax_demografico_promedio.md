# Spec 0011 - Validacion consulta DAX Demografico (Promedio)

Estado: implementado y validado.
Fecha: 2026-07-29.

## 1. Objetivo

Registrar una consulta de Vista de consulta DAX para validar el promedio de
colaboradores por estructura organizacional en la pagina `Demografico
(Promedio)`.

La consulta actualizada devuelve dos resultados:

- Resultado 1: total 2026 de colaboradores, total 2026 sin aprendices y
  diferencia excluida.
- Resultado 2: Dependencia, Area, Cargo, promedio de colaboradores y promedio
  sin aprendices preparado para Excel.

La consulta es un artefacto de validacion. No crea tablas fisicas, tablas
calculadas, columnas, visuales ni relaciones. La version 2026 reutiliza
`Tot_empleados_Promedio` e incorpora la medida permanente
`Tot_empleados_Promedio_Sin_Aprendices` en `Tbl_Medidas`.

## 2. Proyecto y ubicacion

- Proyecto: `PBIP/Proyecto7.pbip`.
- Pestaña DAX Query View: `Demografico (Promedio)`.
- Archivo serializado: `PBIP/Proyecto.SemanticModel/DAXQueries/Demográfico (Promedio).dax`.
- Archivo de orden de pestañas: `PBIP/Proyecto.SemanticModel/DAXQueries/.pbi/daxQueries.json`.

La pestaña existente fue renombrada por el usuario desde `Consulta 1` a
`Demografico (Promedio)`. Por esa razon se versionaron el cambio de metadata de
pestañas y la eliminacion del archivo anterior `Consulta 1.dax` en el commit
inicial de esta consulta.

## 3. Consulta DAX final

```DAX
DEFINE
    VAR FiltroAnioDimPeriodo =
        TREATAS(
            { "2026" },
            'DimPeriodoYM'[Año]
        )

    VAR FiltroAnioPlanta =
        TREATAS(
            { "2026" },
            'PLANTA DE PERSONAL'[AÑO]
        )

EVALUATE
ROW(
    "Contexto",
        "Año 2026",
    "Promedio total de colaboradores",
        CALCULATE(
            [Tot_empleados_Promedio],
            FiltroAnioDimPeriodo,
            FiltroAnioPlanta
        ),
    "Promedio total sin aprendices",
        CALCULATE(
            [Tot_empleados_Promedio_Sin_Aprendices],
            FiltroAnioDimPeriodo,
            FiltroAnioPlanta
        ),
    "Diferencia excluida",
        CALCULATE(
            [Tot_empleados_Promedio],
            FiltroAnioDimPeriodo,
            FiltroAnioPlanta
        )
            - CALCULATE(
                [Tot_empleados_Promedio_Sin_Aprendices],
                FiltroAnioDimPeriodo,
                FiltroAnioPlanta
            )
)

EVALUATE
VAR Detalle =
    SUMMARIZECOLUMNS(
        'PLANTA DE PERSONAL'[DEPENDENCIA],
        'PLANTA DE PERSONAL'[AREA],
        'PLANTA DE PERSONAL'[CARGO],
        FiltroAnioDimPeriodo,
        FiltroAnioPlanta,
        "__Promedio", [Tot_empleados_Promedio],
        "__PromedioSinAprendices", [Tot_empleados_Promedio_Sin_Aprendices]
    )
RETURN
    SELECTCOLUMNS(
        Detalle,
        "Dependencia",
            'PLANTA DE PERSONAL'[DEPENDENCIA],
        "Área",
            'PLANTA DE PERSONAL'[AREA],
        "Cargo",
            'PLANTA DE PERSONAL'[CARGO],
        "Promedio de colaboradores",
            FORMAT(
                [__Promedio],
                "0.###############",
                "es-CO"
            ),
        "Promedio sin aprendices",
            FORMAT(
                [__PromedioSinAprendices],
                "0.###############",
                "es-CO"
            )
    )
ORDER BY
    [Dependencia] ASC,
    [Área] ASC,
    [Cargo] ASC
```

## 4. Campos y medidas utilizados

- `'PLANTA DE PERSONAL'[DEPENDENCIA]`.
- `'PLANTA DE PERSONAL'[AREA]`.
- `'PLANTA DE PERSONAL'[CARGO]`.
- `[Tot_empleados_Promedio]`.
- `[Tot_empleados_Promedio_Sin_Aprendices]`.

La auditoria del modelo mediante `powerbi-modeling-mcp` confirmo que las
columnas `DEPENDENCIA`, `AREA`, `CARGO`, `MES`, `AÑO`, `TIPO_CONTR` e `ID`
existen en `PLANTA DE PERSONAL`.

## 5. Medida reutilizada

La medida existente `Tbl_Medidas[Tot_empleados_Promedio]` fue auditada mediante
`powerbi-modeling-mcp`.

Definicion serializada:

```DAX
AVERAGEX(
    VALUES('PLANTA DE PERSONAL'[Mes]),
    CALCULATE( COUNT('PLANTA DE PERSONAL'[ID]) )
)
```

Formato de la medida: `0.00`.

La medida original no fue modificada. La consulta la reutiliza como valor
agregado y la compara contra la medida nueva sin aprendices.

## 6. Medida nueva sin aprendices

La medida `Tbl_Medidas[Tot_empleados_Promedio_Sin_Aprendices]` conserva la
logica mensual de `Tot_empleados_Promedio` y excluye tipos de contrato
normalizados mediante `COALESCE`, `SUBSTITUTE(UNICHAR(160))`, `TRIM` y `UPPER`.

Valores reales auditados en `PLANTA DE PERSONAL[TIPO_CONTR]`:

| Valor original | Valor normalizado | Registros | Años |
|---|---|---:|---|
| Contrato Aprendizaje | CONTRATO APRENDIZAJE | 1053 | 2024, 2025 |
| Contrato De Aprendizaje | CONTRATO DE APRENDIZAJE | 506 | 2024, 2025 |
| Contrato Fijo | CONTRATO FIJO | 9959 | 2024, 2025 |
| Contrato Indefinido | CONTRATO INDEFINIDO | 26232 | 2024, 2025 |
| Fijo | FIJO | 3931 | 2025, 2026 |
| Indefinido | INDEFINIDO | 18224 | 2025, 2026 |
| Sena | SENA | 967 | 2025, 2026 |
| Temporal | TEMPORAL | 7762 | 2024, 2025, 2026 |

Exclusiones aplicadas:

- `CONTRATO APRENDIZAJE`.
- `CONTRATO DE APRENDIZAJE`.
- `SENA`.

No se encontro `PRACTICANTE` como valor de `TIPO_CONTR`. En 2026, los cargos
`PRACTICANTE` y `APRENDIZ SENA` aparecen bajo `TIPO_CONTR = Sena`, por lo que
quedan excluidos por el tipo de contrato auditado.

Definicion DAX:

```DAX
VAR TiposExcluidos =
    {
        "CONTRATO APRENDIZAJE",
        "CONTRATO DE APRENDIZAJE",
        "SENA"
    }
RETURN
    AVERAGEX(
        VALUES('PLANTA DE PERSONAL'[MES]),
        CALCULATE(
            COUNT('PLANTA DE PERSONAL'[ID]),
            KEEPFILTERS(
                FILTER(
                    VALUES('PLANTA DE PERSONAL'[TIPO_CONTR]),
                    VAR TipoOriginal =
                        COALESCE(
                            'PLANTA DE PERSONAL'[TIPO_CONTR],
                            ""
                        )
                    VAR TipoNormalizado =
                        UPPER(
                            TRIM(
                                SUBSTITUTE(
                                    TipoOriginal,
                                    UNICHAR(160),
                                    " "
                                )
                            )
                        )
                    RETURN
                        NOT (
                            TipoNormalizado IN TiposExcluidos
                        )
                )
            )
        )
    )
```

## 7. Comportamiento de SUMMARIZECOLUMNS y filtros

`SUMMARIZECOLUMNS` agrupa por Dependencia, Area y Cargo respetando el contexto
de filtro aplicado a la consulta. La version actual contiene un filtro fijo de
año 2026 para validar el corte publicado.

`DimPeriodoYM[Año]` es texto y no filtra directamente `PLANTA DE PERSONAL`. Por
esa razon se aplican dos filtros:

- `TREATAS({ "2026" }, 'DimPeriodoYM'[Año])`.
- `TREATAS({ "2026" }, 'PLANTA DE PERSONAL'[AÑO])`.

El orden se define por:

1. Dependencia ascendente.
2. Area ascendente.
3. Cargo ascendente.

## 8. Resultados 2026

La consulta final fue ejecutada contra el modelo abierto en Power BI Desktop
mediante `powerbi-modeling-mcp`.

| Contexto | Promedio total | Promedio sin aprendices | Diferencia |
|---|---:|---:|---:|
| Año 2026 | 2524,8571428571427 | 2423,714285714286 | 101,14285714285688 |
| Año 2026 / 06.Junio | 2572 | 2465 | 107 |

La ejecución del 2026 completo devolvió `1040` filas de detalle
Dependencia-Area-Cargo, con `49` dependencias, `148` áreas y `326` cargos. El
valor anual se actualizó contra el modelo abierto el 2026-07-29 después de la
carga más reciente de `PLANTA DE PERSONAL`.

Para 2026, el unico `TIPO_CONTR` excluido con registros es `Sena`:

| Valor original | Valor normalizado | Registros 2026 | Meses 2026 |
|---|---|---:|---:|
| Sena | SENA | 601 | 6 |

Validacion de cargos excluidos en 2026:

| Tipo contrato | Cargo | Registros |
|---|---|---:|
| Sena | PRACTICANTE | 108 |
| Sena | APRENDIZ SENA | 493 |

## 9. Exportacion a Excel

Al copiar desde DAX Query View hacia Excel, valores como
`1.1666666666666667` podian pegarse como `11666666666666667` porque Excel
interpretaba el punto como separador de miles. Para evitarlo, las columnas de
detalle se formatean con `FORMAT(..., "0.###############", "es-CO")`.

Las columnas `Promedio de colaboradores` y `Promedio sin aprendices` del
detalle son texto para exportacion. Si se requiere convertirlas en Excel, usar:

```excel
=VALOR.NUMERO(D2;",";".")
```

La suma de los promedios por Dependencia-Area-Cargo no debe usarse para
reconstruir el total anual. `Tot_empleados_Promedio` es no aditiva porque
evalua `AVERAGEX` nuevamente dentro de cada contexto organizacional.

Muestras con coma decimal:

| Dependencia | Area | Cargo | Promedio | Promedio sin aprendices |
|---|---|---|---:|---:|
| 01 OPERACIONALES | APRENDICES Y PRACTICANTES | APRENDIZ SENA | 5 | *(blank)* |
| 02 NO DISTRIBUIDOS O DE APOYO | COSTOS | COORDINADOR | 1 | 1 |
| COORDINACION DE GESTION HUMANA | COORDINACION DE GESTION HUMANA | ANALISTA PROFESIONAL GESTION HUMANA | 2 | 2 |
| COORDINACION DE GESTION HUMANA | COORDINACION DE GESTION HUMANA | JEFE DE GESTION HUMANA | 1 | 1 |

## 10. Validacion con contexto de pagina

La pagina `Demografico (Promedio)` se valido previamente con el contexto
visible:

- Año: `2026`.
- Mes: `06.Junio`.

Para comparar bajo el mismo contexto se uso una variante temporal con
`TREATAS`. Esa variante no quedo guardada en el archivo `.dax`.

Resultado:

- Promedio total: `2572`.
- Filas de detalle Dependencia-Area-Cargo: `636`.
- Valor visual de referencia en la pagina: `2572` colaboradores.
- Diferencia entre consulta y pagina: `0`.

## 11. Validaciones tecnicas

Validaciones ejecutadas:

- `powerbi-modeling-mcp`: inspeccion de medida, columnas y ejecucion DAX.
- `powerbi-modeling-mcp`: creacion y lectura de la medida nueva.
- `powerbi-modeling-mcp`: auditoria de `TIPO_CONTR`.
- `powerbi-modeling-mcp`: ejecucion de consulta anual 2026 y junio 2026.
- Validacion de formato `FORMAT(..., "0.###############", "es-CO")` con
  muestras decimales.
- Confirmacion de que `Tot_empleados_Promedio` permanece intacta.
- Validacion UTF-8 sin BOM sobre archivos versionados.
- Revision de diff y staging selectivo.

No se modificaron:

- Tablas fisicas.
- Columnas.
- Relaciones.
- Visuales o paginas del reporte.
- Fuentes de datos.
- Archivos de `Outputs`.

## 12. Archivos versionados

- `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl`.
- `PBIP/Proyecto.SemanticModel/DAXQueries/Demográfico (Promedio).dax`.
- `Specs/0011_validacion_consulta_dax_demografico_promedio.md`.
- `Docs/METRICS_CATALOG.md`.
- `Docs/CHANGELOG.md`.
