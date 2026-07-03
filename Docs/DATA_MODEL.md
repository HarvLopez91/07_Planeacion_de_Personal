# Modelo de Datos

> Fuente oficial para tablas, columnas, relaciones y cardinalidades del modelo semantico.
> Para las fuentes de origen de cada tabla ver [DATA_PIPELINE.md](DATA_PIPELINE.md).
> Para las medidas DAX ver [METRICS_CATALOG.md](METRICS_CATALOG.md).

---

## Clasificacion de tablas

### Tablas de Hechos (visibles)

| Tabla (nombre TMDL) | Grupo | Descripcion |
|---|---|---|
| `PLANTA DE PERSONAL` | HeadCount | Planta de personal activa, historico mensual 2024+2025. Incluye datos demograficos y contractuales del colaborador. |
| `Planta Ppto` | PptovsReal | Datos mensuales de planta presupuestada y real, con ingresos, retiros, ventas y gasto laboral. |
| `Ppto Retiros` | PptovsReal | Registro nominal de retiros con motivo, tipo de contrato y periodo. |
| `Ppto Ingresos` | PptovsReal | Registro nominal de ingresos (contrataciones). |
| `AUSENTISMOS` | *(sin grupo)* | Registro de ausencias laborales con concepto, dias reales y datos demograficos del empleado. |
| `Incapacidades` | Incapacidades | Incapacidades medicas con diagnostico CIE-10, fechas de inicio/fin y empresa. |
| `ACCIDENTALIDAD` | SST | Consolidacion de accidentes laborales de SST_CHA + SST-HABITELH + SST-GSKY (tabla derivada via `Table.Combine`). |
| `SST GENERAL` | SST | Resumen mensual de indicadores SST por empresa: accidentes, dias de ausentismo, frecuencia, severidad. |
| `SST_CHA` | SST | Detalle de accidentalidad Challenger. Fuente de `ACCIDENTALIDAD`. |
| `SST-HABITELH` | SST | Detalle de accidentalidad Habitel Hotels. Fuente de `ACCIDENTALIDAD`. |
| `SST-GSKY` | SST | Detalle de accidentalidad Grupo Sky. Fuente de `ACCIDENTALIDAD`. |
| `Seleccion Challenger` | Seleccion | Requisiciones de seleccion de Challenger (tabla oculta en el modelo). |
| `Seleccion Habitel Hotels` | Seleccion | Requisiciones de seleccion de Habitel Hotels (tabla oculta). |
| `Seleccion Grupo Sky` | Seleccion | Requisiciones de seleccion de Grupo Sky (tabla oculta). |
| `Seleccion Grupo Lemco` | Seleccion | Requisiciones de seleccion de Lemco (tabla oculta). |
| `SENA_CYL` | *(sin grupo)* | Datos de aprendices SENA para Challenger y Lemco. |
| `SENA UNIDADES` | *(sin grupo)* | Cupo de aprendices SENA por unidad y empresa. |

### Tabla de Staging (oculta)

| Tabla | Descripcion |
|---|---|
| `Consolidado2025` | Tabla intermedia `isHidden = true`. Carga el archivo 2025 de HeadCount y es consumida por `PLANTA DE PERSONAL` mediante `Table.Combine` en Power Query. No tiene relaciones propias en el modelo. |

### Dimensiones

| Tabla | Descripcion |
|---|---|
| `Empresas` | Catalogo de empresas del grupo con su agrupacion. Datos embebidos en binario comprimido dentro de la consulta M. |
| `Grupo Empresarial` | Catalogo de grupos de empresas (Challenger, Habitel Hotels, Grupo Sky, Lemco, Fundacion Challenger). |
| `Anos` | Dimension de anos (lista de anos validos del modelo). |
| `Mes` | Dimension de meses con numero ordinal, nombre formateado (`01.Enero`...) y abreviatura. Datos embebidos. |
| `Trimestres` | Meses agrupados por trimestre para filtrado. |
| `Estructura` | Catalogo de dependencias/gerencias. Una sola columna `DEPENDENCIA`. |
| `AREAS` | Catalogo de areas. |
| `Generaciones` | Clasificacion generacional: Baby Boomers, Generacion X, Millennials, Centennials. |
| `General_Ausentismos` | Catalogo de conceptos de ausentismo (ej: Licencia de Maternidad, Incapacidad EPS). |
| `CIE-10` | Clasificacion Internacional de Enfermedades, codigo nivel 3. Usada para relacionar `Incapacidades`. |
| `Maestro` | Maestro de empleados: Identificacion, Fecha Nacimiento, Sexo, Ano de nacimiento. Fuente: `Maestro.xlsx`. |
| `Dias Laborales` | Dias laborables por mes y ano. Usado como denominador en tasas de ausentismo. |

### Tablas calculadas / auxiliares

| Tabla | Descripcion |
|---|---|
| `DimPeriodoYM` | Tabla calculada: `CROSSJOIN('Anos', 'Mes')`. Genera el producto cartesiano Ano x Mes. Incluye columnas calculadas para `IndexAnioMes`, trimestre actual, trimestre anterior y etiqueta `MesAnio`. |
| `tbl_Refresh` | Tabla de una sola fila generada en M con la fecha y hora de la ultima actualizacion del modelo (zona horaria Bogota, UTC-5). |
| `Tbl_Medidas` | Tabla vacia usada exclusivamente como contenedor de medidas globales/transversales. Patron comun en Power BI para organizar medidas que no pertenecen a ninguna tabla de datos. |
| `DateTableTemplate_*` | Plantilla de calendario autogenerada por Power BI. No editar. |
| `LocalDateTable_*` (x18) | Tablas de calendario locales autogeneradas por Power BI para cada columna de tipo fecha. No editar. |

---

## Columnas principales por tabla de hechos

### PLANTA DE PERSONAL

| Columna | Tipo | Descripcion |
|---|---|---|
| `ID` | string | Identificador del colaborador |
| `NOMBRE EMPLEADO` | string | Nombre completo |
| `GRUPO EMPRESA` | string | Grupo empresarial |
| `Nombre Empresa` | string | Nombre de la empresa |
| `DEPENDENCIA` | string | Gerencia/dependencia |
| `AREA` | string | Area funcional |
| `CARGO` | string | Cargo del colaborador |
| `TIPO_CONTR` | string | Tipo de contrato (Fijo, Indefinido, Contrato Aprendizaje, etc.) |
| `TIPO_CONTR (grupos)` | col. calculada | Normalizacion de tipos de contrato en 4 categorias |
| `F_INICIO` | date | Fecha de inicio del contrato |
| `F_CENCIM` | dateTime | Fecha de vencimiento del contrato (relacionada con LocalDateTable) |
| `SEXO` | string | Genero del colaborador |
| `GENERACION` | string | Rango generacional |
| `EDAD` | string | Edad (almacenada como texto) |
| `EST_CIVIL` | string | Estado civil |
| `EST_CIVIL (grupos)` | col. calculada | Normalizacion del estado civil en 6 categorias |
| `NIVEL EDUCATIVO` | string | Nivel de educacion |
| `CIUDAD DE RESIDENCIA` | string | Ciudad de residencia |
| `SUELDO_B` | string | Salario basico (almacenado como texto — riesgo) |
| `MES` | string | Mes del registro (ej: `"01.Enero"`) |
| `ANO` | string | Ano del registro |
| `Antiguedad` | string | Antiguedad calculada |
| `Rango Antiguedad` | string | Rango de antiguedad |
| `PRESUPUESTO` | string | Indicador de si el cargo esta en presupuesto |
| `CCO` | string | Centro de costos |
| `DEPARTAMENTO` | string | Departamento geografico |

> Nota: La columna `GENERACION` tiene un error de encoding HTML en el TMDL de relaciones (`GENERACI&#211;N`). Ver [decisiones/README.md](decisions/README.md).
>
> Criterio de normalizacion `es-CO`: los nombres y valores visibles para usuario final deben conservar la ortografia canonica en espanol de Colombia, incluyendo tildes y eñe correctas en etiquetas y filtros como `Año`, `Generación`, `Rango Antigüedad`, `Sin Información En Kactus` y `Relación de Hijos`. No se admiten variantes mojibake como `AÃ±o` o `GeneraciÃ³n`, ni duplicados semanticos como `Millenials`; el valor canonico es `Millennials`.

### Planta Ppto (columnas de datos principales)

| Columna | Tipo | Descripcion |
|---|---|---|
| `Ppto/Real` | string | Indicador `"Ppto"` o `"Real"` |
| `Ano` | string | Ano |
| `Mes` | string | Nombre del mes |
| `Mes Num` | string | Numero del mes |
| `Empresa` | string | Nombre de la empresa |
| `Grupo Empresa` | string | Grupo empresarial |
| `Indefinidos` | int64 | Cantidad de contratos indefinidos |
| `Fijos` | int64 | Cantidad de contratos fijos |
| `Temporales` | int64 | Cantidad de temporales |
| `Sena` | int64 | Cantidad de aprendices SENA |
| `Total` | int64 | Total planta |
| `Total-Sena` | int64 | Total excluyendo SENA |
| `Ingresos` | int64 | Ingresos del mes |
| `Retiros` | int64 | Retiros del mes |
| `Ventas (MM)` | decimal | Ventas en millones |
| `Gasto Personal` | decimal | Gasto laboral real |
| `Ppto Ventas (MM)` | decimal | Ventas presupuestadas |
| `Ppto Gasto Personal` | decimal | Gasto laboral presupuestado |
| `IndexAnioMes` | col. calculada | `Ano * 12 + Mes Num` (indice ordinal para ordenamiento) |

---

## Relaciones (41 relaciones explicitas)

### Eje temporal (muchos hechos → Anos y Mes)

| Tabla Hecho | Columna | → | Dimension | Columna |
|---|---|---|---|---|
| `PLANTA DE PERSONAL` | `ANO` | → | `Anos` | `Ano` |
| `PLANTA DE PERSONAL` | `MES` | → | `Mes` | `Meses` |
| `Planta Ppto` | `Ano` | → | `Anos` | `Ano` |
| `Planta Ppto` | `Mes` | → | `Mes` | `Meses` |
| `Ppto Retiros` | `Ano` | → | `Anos` | `Ano` |
| `Ppto Retiros` | `Mes` | → | `Mes` | `Meses` |
| `Ppto Ingresos` | `Ano` | → | `Anos` | `Ano` |
| `Ppto Ingresos` | `Mes` | → | `Mes` | `Meses` |
| `AUSENTISMOS` | `ANO` | → | `Anos` | `Ano` |
| `AUSENTISMOS` | `Mes` | → | `Mes` | `Meses` |
| `ACCIDENTALIDAD` | `AÑO` | → | `Anos` | `Ano` |
| `ACCIDENTALIDAD` | `MES` | → | `Mes` | `Meses` |
| `SST GENERAL` | `Ano` | → | `Anos` | `Ano` |
| `SST GENERAL` | `Mes` | → | `Mes` | `Meses` |
| `Dias Laborales` | `Ano` | → | `Anos` | `Ano` |
| `Dias Laborales` | `Mes` | → | `Mes` | `Numero` |
| `SENA UNIDADES` | `Ano` | → | `Anos` | `Ano` |
| `SENA UNIDADES` | `Mes` | → | `Mes` | `Meses` |

### Eje de empresa

| Tabla Hecho | Columna | → | Dimension | Columna |
|---|---|---|---|---|
| `PLANTA DE PERSONAL` | `Nombre Empresa` | → | `Empresas` | `Empresas` |
| `Planta Ppto` | `Empresa` | → | `Empresas` | `Empresas` |
| `Ppto Retiros` | `Empresa` | → | `Empresas` | `Empresas` |
| `Ppto Ingresos` | `Empresa` | → | `Empresas` | `Empresas` |
| `AUSENTISMOS` | `Empresa` | → | `Empresas` | `Empresas` |
| `ACCIDENTALIDAD` | `Empresa` | → | `Empresas` | `Empresas` |
| `SST GENERAL` | `Empresa` | → | `Empresas` | `Empresas` |
| `Seleccion Grupo Lemco` | `Empresa` | → | `Empresas` | `Empresas` |
| `SENA UNIDADES` | `EMPRESA` | → | `Empresas` | `Empresas` |
| `Empresas` | `Grupo Empresa` | → | `Grupo Empresarial` | `Grupo Empresarial` |

### Eje organizacional (estructura y areas)

| Tabla Hecho | Columna | → | Dimension | Columna |
|---|---|---|---|---|
| `PLANTA DE PERSONAL` | `DEPENDENCIA` | → | `Estructura` | `DEPENDENCIA` |
| `PLANTA DE PERSONAL` | `AREA` | → | `AREAS` | `AREA` |
| `AUSENTISMOS` | `DEPENDENCIA` | → | `Estructura` | `DEPENDENCIA` |
| `Seleccion Challenger` | `DEPENDENCIA` | → | `Estructura` | `DEPENDENCIA` |
| `Ppto Ingresos` | `Dependencia` | → | `Estructura` | `DEPENDENCIA` |
| `Ppto Ingresos` | `Area` | → | `AREAS` | `AREA` |
| `Ppto Retiros` | `Dependencia` | → | `Estructura` | `DEPENDENCIA` |
| `Ppto Retiros` | `Area` | → | `AREAS` | `AREA` |
| `Consolidado2025` | `DEPENDENCIA` | → | `Estructura` | `DEPENDENCIA` |
| `PLANTA DE PERSONAL` | `GENERACION` | → | `Generaciones` | `Generacion` |

### Dimensiones especializadas

| Tabla Hecho | Columna | → | Dimension | Columna |
|---|---|---|---|---|
| `AUSENTISMOS` | `Nombre Concepto` | → | `General_Ausentismos` | `Concepto_Ausentismo` |
| `Incapacidades` | `CIE10` (calculada) | → | `CIE-10` | `cie-10` |
| `Ppto Retiros` | `Identificacion` | → | `Maestro` | `Identificacion` |
| `Ppto Ingresos` | `Identificacion` | → | `Maestro` | `Identificacion` |

### Relaciones de periodo ordinal

| Tabla | Columna | → | Tabla | Columna |
|---|---|---|---|---|
| `Planta Ppto` | `IndexAnioMes` | → | `DimPeriodoYM` | `IndexAnioMes` |
| `Ppto Retiros` | `IndexAnioMes` | → | `DimPeriodoYM` | `IndexAnioMes` |

### Relaciones de fecha con LocalDateTable (datePartOnly)

| Tabla | Columna | Proposito |
|---|---|---|
| `PLANTA DE PERSONAL` | `F_CENCIM` | Navegacion de fecha de vencimiento |
| `Seleccion Challenger` | `FECHA RQ SELECCION` | Fecha de requisicion |
| `Seleccion Challenger` | `FECHA META CIERRE` | Meta de cierre |
| `Seleccion Challenger` | `FECHA TERMIN PROCESO` | Terminacion del proceso |
| `Seleccion Habitel Hotels` | (las 3 fechas analogas) | Idem |
| `Seleccion Grupo Sky` | (las 3 fechas analogas) | Idem |
| `Seleccion Grupo Lemco` | (las 4 fechas: incluye FECHA RQ SELECCION INICIAL) | Idem |
| `Incapacidades` | `Fecha Desde`, `Fecha Hasta` | Rango de incapacidad |
| `Maestro` | `Fecha Nacimiento` | Edad y generacion |
| `tbl_Refresh` | `FechaActualizacion` | Control de actualizacion |

### Relaciones con cardinalidad especial

| Relacion | Cardinalidad | Direccion | Riesgo |
|---|---|---|---|
| `AUSENTISMOS.codigo1` → `Incapacidades.Codigo-1` | Many-to-Many | BothDirections | **ALTO**: puede generar filtros cruzados no esperados |
| `Trimestres.Meses` → `Mes.Meses` | One-to-One | BothDirections | Medio: ambiguedad potencial en multiples hechos |

---

## Riesgos del modelo

### R1 — 18 LocalDateTables
Cada columna de fecha no conectada a un calendario compartido genera una tabla calendario independiente. Impacto en memoria y rendimiento. Se recomienda evaluar la creacion de una tabla `Dim_Fecha` compartida.

### R2 — Joins por string en dimensiones temporales
Las relaciones con `Anos` y `Mes` se hacen por columnas `string` (`"2024"`, `"01.Enero"`), no por enteros. Menor compresion en VertiPaq y fragilidad ante cambios de formato en las fuentes.

### R3 — Relacion M:M con BothDirections (AUSENTISMOS ↔ Incapacidades)
Alta probabilidad de contextos de filtro ambiguos en medidas que cruzan ambas tablas.

### R4 — Encoding HTML en nombre de columna
La columna `GENERACION` de `PLANTA DE PERSONAL` aparece en el TMDL de relaciones como `GENERACI&#211;N`. Riesgo de quiebre en herramientas que procesen el TMDL como texto puro.

### R5 — SUELDO_B almacenado como string
El salario basico en `PLANTA DE PERSONAL` se carga como texto, impidiendo calculos directos sobre el.

### R6 — IndexAnioMes duplicado
La expresion `Ano * 12 + MesNum` aparece como columna calculada independiente en `Planta Ppto`, `Ppto Retiros` y `DimPeriodoYM`. Cualquier cambio debe replicarse en los tres lugares.
