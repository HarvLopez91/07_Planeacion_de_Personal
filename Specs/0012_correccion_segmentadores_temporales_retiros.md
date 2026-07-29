# Correccion de segmentadores temporales en Retiros

Estado: validado para versionamiento.
Fecha de validacion: 2026-07-29.

## 1. Objetivo

Corregir la propagacion de los segmentadores de Ano y Mes en la pagina
`Retiros`, sin modificar el modelo semantico, relaciones, medidas, Power Query
ni otras paginas.

Pagina:

`PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405`

## 2. Causa raiz

La pagina `Retiros` usaba segmentadores temporales basados en
`DimPeriodoYM[Año]` y `DimPeriodoYM[Meses]`.

`DimPeriodoYM` filtra tablas como `Ppto Retiros` y `Planta Ppto` mediante
`IndexAnioMes`, pero no filtra directamente `PLANTA DE PERSONAL`. Por esa
razon, la medida `Tot_empleados_Promedio`, calculada sobre `PLANTA DE PERSONAL`,
no recibia el mismo contexto temporal que en `Demografico (Promedio)`.

El proyecto ya cuenta con las dimensiones `Años` y `Mes`, relacionadas con
`PLANTA DE PERSONAL` y `Ppto Retiros`. La correccion usa esas dimensiones
existentes y evita crear una nueva dimension calendario.

## 3. Cambios aplicados

Segmentador Ano:

- Visual ID: `907c7c33165ac7186806`.
- Campo anterior: `DimPeriodoYM[Año]`.
- Campo nuevo: `Años[Año]`.
- Se conservo la seleccion base `2026`.
- Se elimino un filtro residual del propio visual que permitia
  simultaneamente `2024`, `2025` y `2026`.

Segmentador Mes:

- Visual ID: `37ed01c30df4dafce226`.
- Campo anterior: `DimPeriodoYM[Meses]`.
- Campo nuevo: `Mes[Meses]`.
- Se elimino un filtro residual del propio visual sobre `Planta Ppto[Año]`.
- La seleccion fija usada durante las pruebas se limpio; el estado base queda
  en todos los meses.

## 4. Alcance preservado

No se modificaron:

- medidas DAX;
- relaciones;
- tablas TMDL;
- Power Query;
- fuentes de datos;
- segmentadores de `Demografico (Promedio)`;
- otras paginas.

## 5. Validacion funcional

La validacion manual en Power BI Desktop fue satisfactoria comparando
`Retiros` contra `Demografico (Promedio)` bajo filtros equivalentes.

| Escenario | Retiros | Demografico (Promedio) | Resultado |
|---|---:|---:|---|
| Ano 2026, todos los meses | 2524,86 | 2525 por redondeo | Coincide |
| Ano 2026, Mes 06.Junio | 2572 | 2572 | Coincide |
| Ano 2026, Mes 07.Julio | 2572 | 2572 | Coincide |

Medida sin aprendices validada en Retiros:

- Ano 2026: `2423,71`.
- Mes 06.Junio de 2026: `2465`.
- Mes 07.Julio de 2026: `2465`.

## 6. Observacion sobre julio

`PLANTA DE PERSONAL` ya contiene julio de 2026, por lo que los promedios de
colaboradores responden correctamente a ese periodo.

Los visuales de retiros para julio muestran cero o quedan vacios porque
`Ppto Retiros` no presenta todavia informacion equivalente para ese periodo o
permanece en proceso de carga. Esto no corresponde a un fallo de propagacion
del filtro hacia `Tot_empleados_Promedio`.

## 7. Interacciones y sincronizacion

Se valido funcionalmente que los segmentadores `Años[Año]` y `Mes[Meses]`
filtran la matriz y los visuales de datos revisados en `Retiros`.

No se modifico la sincronizacion de segmentadores. Se conserva la diferencia
actual entre paginas:

- `Demografico (Promedio)` usa campos directos de `PLANTA DE PERSONAL`.
- `Retiros` usa las dimensiones compartidas `Años` y `Mes`.

## 8. Limitacion MCP

La validacion DAX mediante `powerbi-modeling-mcp` no pudo completarse por una
conexion local de Power BI Desktop no disponible o no abierta para consulta.
La validacion funcional se cerro con evidencia manual en Desktop aportada por
el usuario.

## 9. Archivos versionados

- `PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405/visuals/907c7c33165ac7186806/visual.json`
- `PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405/visuals/37ed01c30df4dafce226/visual.json`
- `Specs/0012_correccion_segmentadores_temporales_retiros.md`
- `Docs/CHANGELOG.md`

## 10. Decision

Validacion exitosa: `Años[Año]` y `Mes[Meses]` filtran correctamente la matriz
de `Retiros` y los resultados coinciden con `Demografico (Promedio)` bajo el
mismo contexto temporal.
