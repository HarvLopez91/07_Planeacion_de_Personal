# Spec 0011 - Validacion consulta DAX Demografico (Promedio)

Estado: implementado y validado.
Fecha: 2026-07-29.

## 1. Objetivo

Registrar una consulta de Vista de consulta DAX para validar el promedio de colaboradores por estructura organizacional en la pagina `Demografico (Promedio)`.

La consulta devuelve:

- Dependencia.
- Area.
- Cargo.
- Promedio de colaboradores.

La consulta es un artefacto de validacion. No crea tablas fisicas, tablas calculadas, medidas, columnas, visuales, relaciones ni cambios en el modelo semantico.

## 2. Proyecto y ubicacion

- Proyecto: `PBIP/Proyecto7.pbip`.
- Pestaña DAX Query View: `Demográfico (Promedio)`.
- Archivo serializado: `PBIP/Proyecto.SemanticModel/DAXQueries/Demográfico (Promedio).dax`.
- Archivo de orden de pestañas: `PBIP/Proyecto.SemanticModel/DAXQueries/.pbi/daxQueries.json`.

La pestaña existente fue renombrada por el usuario desde `Consulta 1` a `Demográfico (Promedio)`. Por esa razon se versionan tambien el cambio de metadata de pestañas y la eliminacion del archivo anterior `Consulta 1.dax`.

## 3. Consulta DAX final

```DAX
EVALUATE
SUMMARIZECOLUMNS(
    'PLANTA DE PERSONAL'[DEPENDENCIA],
    'PLANTA DE PERSONAL'[AREA],
    'PLANTA DE PERSONAL'[CARGO],
    "Promedio de colaboradores", [Tot_empleados_Promedio]
)
ORDER BY
    'PLANTA DE PERSONAL'[DEPENDENCIA] ASC,
    'PLANTA DE PERSONAL'[AREA] ASC,
    'PLANTA DE PERSONAL'[CARGO] ASC
```

## 4. Campos utilizados

- `'PLANTA DE PERSONAL'[DEPENDENCIA]`.
- `'PLANTA DE PERSONAL'[AREA]`.
- `'PLANTA DE PERSONAL'[CARGO]`.
- `[Tot_empleados_Promedio]`.

La auditoria del modelo mediante `powerbi-modeling-mcp` confirmo que las columnas `DEPENDENCIA`, `AREA`, `CARGO`, `MES` e `ID` existen en `PLANTA DE PERSONAL`.

## 5. Medida reutilizada

La medida existente `Tbl_Medidas[Tot_empleados_Promedio]` fue auditada mediante `powerbi-modeling-mcp`.

Definicion serializada:

```DAX
AVERAGEX(
    VALUES('PLANTA DE PERSONAL'[Mes]),
    CALCULATE( COUNT('PLANTA DE PERSONAL'[ID]) )
)
```

Formato de la medida: `0.00`.

La medida no fue modificada. La consulta solo la reutiliza como valor agregado.

## 6. Comportamiento de SUMMARIZECOLUMNS

`SUMMARIZECOLUMNS` agrupa por Dependencia, Area y Cargo respetando el contexto de filtro aplicado a la consulta. La version final no contiene filtros fijos para permitir validar el resultado completo.

El orden se define por:

1. Dependencia ascendente.
2. Area ascendente.
3. Cargo ascendente.

## 7. Validacion sin filtros

La consulta final fue ejecutada contra el modelo abierto en Power BI Desktop mediante `powerbi-modeling-mcp`.

Resultado:

- Filas devueltas: `1892`.
- Promedio total de colaboradores: `5719,5`.
- Duracion reportada de ejecucion: `32 ms` en la ejecucion completa inicial.
- DirectQuery: `0` consultas.

Muestras ordenadas:

| Muestra | Dependencia | Area | Cargo | Promedio de colaboradores |
|---|---|---|---|---:|
| Primera | *(en blanco)* | *(en blanco)* | ABOGADO SENIOR | 1 |
| Ultima | PROYECTOS ESTRATEGICOS | PROYECTOS ESTRATEGICOS | DIRECTOR DE PROYECTOS | 1 |

Muestras con mayor promedio y estructura completa:

| Dependencia | Area | Cargo | Promedio de colaboradores |
|---|---|---|---:|
| GERENCIA COMERCIAL | VENTAS | VENDEDOR JUNIOR - N10 | 578,0833333333334 |
| DIRECCION DE MANUFACTURA | REFRIGERACION | OPERARIO - N10 | 286,8333333333333 |
| GERENCIA DE OPERACIONES-MANUFACTURA | REFRIGERACION | OPERARIO - N10 | 171,83333333333334 |

Las muestras incluyen valores no enteros, coherentes con la naturaleza no aditiva de `Tot_empleados_Promedio`, que promedia conteos mensuales.

## 8. Validacion con contexto de pagina

La pagina `Demografico (Promedio)` se valido con el contexto visible:

- Año: `2026`.
- Mes: `06.Junio`.

Para comparar bajo el mismo contexto se uso una variante temporal con `TREATAS`. Esa variante no quedo guardada en el archivo `.dax`.

Resultado:

- Promedio total: `2572`.
- Filas de detalle Dependencia-Area-Cargo: `636`.
- Valor visual de referencia en la pagina: `2572` colaboradores.
- Diferencia entre consulta y pagina: `0`.

Muestras del contexto `2026` / `06.Junio`:

| Dependencia | Area | Cargo | Promedio de colaboradores |
|---|---|---|---:|
| GERENCIA COMERCIAL | VENTAS | VENDEDOR JUNIOR - N10 | 273 |
| DIRECCION DE MANUFACTURA | REFRIGERACION | OPERARIO - N10 | 206 |
| DIRECCION DE MANUFACTURA | METALMECANICA (GASODOMESTICOS) | OPERARIO - N10 | 111 |

## 9. Diferencias encontradas

No se encontraron diferencias entre el valor total de la consulta filtrada y el valor visible de la pagina bajo el mismo contexto de Año y Mes.

La consulta sin filtros devuelve mas combinaciones porque DAX Query View no aplica automaticamente los segmentadores de una pagina del reporte.

## 10. Validaciones tecnicas

Validaciones ejecutadas:

- `powerbi-modeling-mcp`: inspeccion de medida, columnas y ejecucion DAX.
- `powerbi-report-author doctor`.
- `python tools/pbip/list_pbip_structure.py . --pretty`.
- `python tools/pbip/audit_semantic_model.py . --pretty`.
- `python tools/pbip/audit_dax_measures.py . --pretty`.
- `python tools/governance/prepare_commit_review.py . --pretty`.
- Validacion UTF-8 sin BOM sobre archivos versionados.
- Revision de diff y staging selectivo.

No se modificaron:

- TMDL del modelo semantico.
- Medidas existentes.
- Visuales o paginas del reporte.
- Relaciones.
- Fuentes de datos.
- Archivos de `Outputs`.

## 11. Archivos versionados

- `PBIP/Proyecto.SemanticModel/DAXQueries/.pbi/daxQueries.json`.
- `PBIP/Proyecto.SemanticModel/DAXQueries/Consulta 1.dax` eliminado por renombre de pestaña.
- `PBIP/Proyecto.SemanticModel/DAXQueries/Demográfico (Promedio).dax`.
- `Specs/0011_validacion_consulta_dax_demografico_promedio.md`.
- `Docs/CHANGELOG.md`.
