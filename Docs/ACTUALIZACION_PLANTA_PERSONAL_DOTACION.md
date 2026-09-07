# Actualizacion mensual de dotacion en `Planta Personal`

> **Confidencialidad.** Este documento contiene unicamente totales agregados. Los
> libros `Consolidado 2025.xlsx` y `PptovsReal.xlsx` contienen datos personales de
> colaboradores y **no se versionan**: viven en `Data/`, excluido por `.gitignore`.
> Ningun respaldo, extracto ni derivado con detalle individual debe subirse a Git.
> Los reportes de validacion se escriben en `Outputs/`, tambien ignorado.

## Objetivo

Dejar la hoja `Planta Personal` de `PptovsReal.xlsx` actualizada con el corte mensual
de **dotacion** disponible en `Consolidado 2025.xlsx`, de modo que la tabla
`Planta Ppto` del modelo Power BI refleje el periodo cerrado.

Este procedimiento cubre la **dotacion** (Fijos, Indefinidos, Sena, Temporales,
Total, Total-Sena). El corte de **gasto laboral y ventas** se documenta aparte en
[`ACTUALIZACION_PLANTA_PERSONAL_PPTOVSREAL.md`](ACTUALIZACION_PLANTA_PERSONAL_PPTOVSREAL.md),
que actualiza la misma hoja desde `Gasto Laboral <ANIO>.xlsx`.

## Archivos involucrados

| Rol | Ruta | Hoja |
|---|---|---|
| Origen | `Data/HeadCount/2025/Consolidado 2025.xlsx` | `Consolidado2025` |
| Destino | `Data/HeadCount/PptovsReal.xlsx` | `Planta Personal` |
| Respaldo | `Outputs/backups/PptovsReal_<AAAAMMDD_HHMMSS>_pre_actualizacion_<periodo>.xlsx` | — |
| Validacion | `Scripts/headcount/validar_planta_personal.py` | — |

`Consolidado2025` es **nivel persona**: una fila por colaborador y mes.
`Planta Personal` es una **capa calculada agregada**: una fila por
`Ppto/Real x Anio x Mes x Grupo Empresa x Empresa`.

## Por que la escritura debe hacerse manualmente en Excel

`PptovsReal.xlsx` **no debe editarse con scripts de Python** (`openpyxl` u
equivalentes). Su estructura interna contiene:

| Componente | Cantidad |
|---|---:|
| Tablas dinamicas | 12 |
| Caches de tabla dinamica | 9 |
| Conexiones de datos | 1 |
| Tablas estructuradas (ListObject) | 1 |
| Formulas en la hoja `Planta Personal` | 4.031 |
| Formulas en todo el libro | ~94.000 |

`openpyxl` no preserva de forma fiable las tablas dinamicas ni sus caches, y al
guardar obliga a elegir entre conservar las formulas perdiendo los valores en cache,
o conservar los valores destruyendo las formulas. Cualquiera de las dos rompe el
libro para Power BI, que lee valores, y para quien mantiene la hoja.

**Regla:** la escritura es manual en Excel; la validacion es automatizada.

## Pasos de la actualizacion mensual

1. Confirmar que `Consolidado 2025.xlsx` ya tiene el mes cerrado.
2. Crear respaldo del destino en `Outputs/backups/` antes de abrir el libro.
3. Abrir `PptovsReal.xlsx` en Excel y ubicar la hoja `Planta Personal`.
4. Para el periodo nuevo, cargar una fila `Ppto/Real = Real` por cada empresa,
   con la agregacion del origen segun la homologacion de la seccion siguiente.
5. Cerrar el libro y ejecutar el script de validacion.
6. Corregir en Excel lo que el script reporte y repetir hasta obtener `PASS`.
7. Refrescar el modelo en Power BI Desktop.

## Homologacion de `TIPO_CONTR`

El origen usa dos vocabularios segun la epoca; hay que cubrir ambos:

| Categoria destino | Valores de `TIPO_CONTR` que agrupa |
|---|---|
| `Fijos` | `FIJO`, `CONTRATO FIJO` |
| `Indefinidos` | `INDEFINIDO`, `CONTRATO INDEFINIDO` |
| `Sena` | `SENA`, `CONTRATO APRENDIZAJE`, `CONTRATO DE APRENDIZAJE` |
| `Temporales` | `TEMPORAL` |

`Total-Sena` = `Total` - `Sena`. Es el denominador oficial de
`Tasa_Mensual_Retiros` e `Indice_Rotacion`. Filtrar solo por `APRENDIZ` deja fuera
la etiqueta `SENA`, vigente desde 2025-09.

Solo se actualizan las filas `Ppto/Real = Real`. Las filas `Ppto` son presupuesto y
no se tocan.

## Empresas faltantes y empresas sin registros

**Empresas nuevas en el origen:** si `Consolidado2025` reporta una empresa que no
tiene fila en el periodo, hay que crearla. El catalogo no es fijo: en agosto 2026 el
origen reporto 11 empresas y la hoja manejaba 12.

**Empresas sin registros en el mes:** se dejan **con fila en cero**, no se omiten.
Decision aplicada a `Lemco Inmobiliaria` en agosto 2026: figura con `Total = 0` y
`Total-Sena = 0`. Mantener la fila preserva la continuidad de la serie y evita que
un hueco se confunda con un dato faltante.

## Validaciones obligatorias

Ejecutar `Scripts/headcount/validar_planta_personal.py <ANIO> <NN.Mes>`. Cubre:

1. El periodo existe como `Real` **y con dotacion** (no basta con que exista la fila).
2. Todas las empresas del origen estan en el destino.
3. Las empresas sin registros en el origen figuran en cero.
4. Total y `Total-Sena` del periodo cuadran contra el origen.
5. Coherencia interna: `Fijos + Indefinidos + Sena + Temporales = Total`
   y `Total - Sena = Total-Sena`.
6. Sin diferencias por empresa en ningun periodo comparable.
7. Sin duplicados por `Anio / Mes / Ppto-Real / Grupo Empresa / Empresa`.

La validacion 6 es la mas importante y la que motivo este documento: **los totales
por Grupo Empresa pueden cuadrar mientras dos empresas del mismo grupo estan
intercambiadas entre si.**

## Hallazgo: inversion Sky Industrial / Sky Logistica Integral

En mayo, junio y julio de 2026, `Sky Industrial` y `Sky Logistica Integral`
estaban intercambiadas entre si en `Planta Personal`:

| Periodo | Origen (Ind / Log) | Destino antes | Estado tras correccion |
|---|---|---|---|
| 2026-05 | 60 / 177 | 177 / 60 | Corregido |
| 2026-06 | 55 / 174 | 174 / 55 | Corregido |
| 2026-07 | 57 / 174 | 174 / 57 | Corregido |

El total de `Grupo Sky` cuadraba en los tres meses (2.572 en julio), por eso la
conciliacion a nivel grupo nunca lo detecto. Los otros 16 periodos comparables
estaban correctos, asi que fue un error de transcripcion acotado, no sistematico.

Relevancia: Gestion Humana de Grupo SKY solicito precisamente la vista por empresa,
de modo que el error habria sido visible para el cliente interno.

## Diferencia pendiente, ajena a este procedimiento

Persiste una discrepancia de **1 persona entre `Habitel Hotels` y `Lemco`** en
enero, abril, mayo y junio de 2026: el origen la atribuye a un Grupo Empresa y el
destino al otro. Es un error de atribucion de compania, neto cero en el total de la
organizacion, anterior a esta actualizacion y no corregido aqui.

Aparte, entre 2025-09 y 2026-05 la hoja consolida `Lemco Inmobiliaria` dentro de
`Lemco` en varios meses. Conviene definir si esa agregacion es deliberada.

## Automatizar primero la validacion, no la escritura

El objetivo no es que un script escriba el `.xlsx`, sino eliminar la transcripcion
manual, que es donde se originan los errores.

1. **Validacion automatizada (implementado).**
   `Scripts/headcount/validar_planta_personal.py` compara ambos libros en solo
   lectura y emite el reporte a `Outputs/`. Ejecutado despues de cada carga manual,
   habria detectado la inversion de Sky en mayo, tres meses antes de que Grupo SKY
   preguntara por la vista por empresa.
2. **Power Query dentro del libro (siguiente paso).**
   Una consulta en `PptovsReal.xlsx` que lea `Consolidado 2025.xlsx`, aplique la
   homologacion de `TIPO_CONTR` y genere la agregacion. Elimina el paso manual
   conservando el libro y sus tablas dinamicas.
3. **Agregacion en el modelo semantico (objetivo final).**
   `Planta Ppto` podria derivarse de `PLANTA DE PERSONAL`, que ya esta en el modelo
   con detalle por persona. Eliminaria la capa intermedia y con ella la coexistencia
   de dos poblaciones distintas, registrada como riesgo **R4** en `Specs/0027`.
   Requiere Spec propia: cambia el grano de una tabla que alimenta varias paginas.

## Referencias

- `Docs/DATA_PIPELINE.md`, seccion "Arquitectura de fuentes de HeadCount".
- `Docs/METRICS_CATALOG.md`, seccion "Denominador de rotacion - `Total-Sena`".
- `Docs/ACTUALIZACION_PLANTA_PERSONAL_PPTOVSREAL.md`, corte de gasto laboral.
- `Specs/0027_analisis_impacto_rotacion_proyectada.md`, riesgo R4.
