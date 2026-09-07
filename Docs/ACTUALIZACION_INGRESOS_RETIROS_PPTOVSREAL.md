# Actualizacion mensual de `INGRESOS` y `RETIROS` en `PptovsReal.xlsx`

> **Confidencialidad.** Este documento contiene unicamente totales agregados. Los
> libros `PptovsReal.xlsx` y `CONSOLIDADOR_CONTRATOS_V0.0.0.xlsx` contienen datos
> personales de colaboradores y **no se versionan**: viven en `Data/`, excluido por
> `.gitignore`. Los reportes de validacion se escriben en `Outputs/`, tambien
> ignorado. Ningun extracto con detalle individual debe subirse a Git.

## Objetivo

Dejar las hojas `INGRESOS` y `RETIROS` de `PptovsReal.xlsx` actualizadas con los
movimientos del mes cerrado, de modo que las tablas `Ppto Ingresos` y `Ppto Retiros`
del modelo Power BI reflejen el periodo.

## Archivos involucrados

| Rol | Ruta | Hojas |
|---|---|---|
| Origen oficial | `Data/Contratos_Kactus/Fuente_Oficial/CONSOLIDADOR_CONTRATOS_V0.0.0.xlsx` | `<mes>, A` (ingresos), `<Mes> II` o `<mes>, I` (retiros) |
| Destino | `Data/HeadCount/PptovsReal.xlsx` | `INGRESOS`, `RETIROS` |
| Validacion | `Scripts/headcount/validar_ingresos_retiros.py` | — |

El consolidador agrupa las descargas de **Kactus**. Sus hojas mensuales son
**volcados de tabla dinamica**: la fila 1 es el titulo del volcado, la fila 2 esta
vacia y **los encabezados reales estan en la fila 3**; los datos empiezan en la 4.
Las columnas llegan con el prefijo `Fact_Contrataciones[...]`.

La particula del nombre de hoja indica el `Indicador Actividad`:

- **`A`** = activo, corresponde a **ingresos** (por ejemplo `ago, A`).
- **`I`** o **`II`** = inactivo, corresponde a **retiros** (por ejemplo `Ago II`, `jul, I`).

## Columnas clave

**`INGRESOS`** (28 columnas): `Grupo Empresarial`, `Empresa`, `Identificacion`,
`Fecha Contrato`, `Fecha Inicio`, `Anio`, `No Mes`, `Mes`, `Descripcion Cargo`,
`Dependencia`, `Area`, `Nombre Centro Costo`, `Motivo Movimiento`, `CARGO_CCO`.
El periodo se determina por **`Fecha Inicio`**.

**`RETIROS`** (33 columnas): `Grupo empresarial`, `Empresa`, `Identificacion`,
`No. Contrato`, `TC`, `Cargo`, `Nombre Centro Costo`, `Fecha Inicio`,
`Fecha Vencimiento`, `Anio`, `Mes Num`, `Mes`, `Meses de permanencia`, `Detalle`,
`OBSERVACION`, `Clase de nomina`, `CARGO_CCO`. El periodo se determina por
**`Fecha Vencimiento`**; `Detalle` sostiene la clasificacion de retiro voluntario
o involuntario.

En el consolidador las columnas equivalentes son `Codigo Empresa`, `Fecha Contrato`,
`Fecha Inicio`, `Fecha Vencimiento` e `Indicador Actividad`. **El consolidador no
trae el nombre de la empresa ni el grupo empresarial**: solo el codigo. La
homologacion a los nombres del modelo ocurre al cargar en `PptovsReal.xlsx`.

## Regla critica: homologacion de empresa y grupo

Los valores que se cargan en `Grupo empresarial` y `Empresa` **deben coincidir
exactamente con la dimension `Empresas` del modelo semantico**, porque ambas hojas
tienen relacion activa hacia ella:

```
'Ppto Ingresos'.Empresa  -> Empresas.Empresas
'Ppto Retiros'.Empresa   -> Empresas.Empresas
```

Valores validos de `Empresa` (12): `Challenger`, `Fundacion Challenger`,
`Habitel Nomina Compartida`, `Habitel Prime`, `Habitel Select`, `Lemco`,
`Lemco Inmobiliaria`, `Lemco Salvio`, `Operadora`, `Sky Forwarder`,
`Sky Industrial`, `Sky Logistica Integral`.

Valores validos de `Grupo empresarial` (5): `Challenger`, `Fundacion Challenger`,
`Grupo Sky`, `Habitel Hotels`, `Lemco`.

**Cargar la nomenclatura cruda de Kactus rompe la relacion.** Los registros quedan
fuera de la dimension y aparecen en blanco en cualquier visual segmentado por
empresa, sin que el total general lo evidencie.

## Validaciones obligatorias

Ejecutar `Scripts/headcount/validar_ingresos_retiros.py <ANIO> <NN.Mes>`. Cubre,
para cada hoja:

1. El periodo existe en `PptovsReal.xlsx`.
2. El total del mes cuadra contra el consolidador Kactus.
3. Sin identificaciones repetidas dentro del mes.
4. Todos los valores de `Empresa` hacen match con la dimension `Empresas`.
5. Los valores de `Grupo empresarial` son coherentes con el mes anterior.

Las validaciones 4 y 5 son las que detectan el fallo silencioso descrito arriba.

## Resultado de la validacion de agosto 2026

**Estado: FALLA.** Los volumenes son correctos; la homologacion no.

| Validacion | INGRESOS | RETIROS |
|---|---|---|
| Periodo presente | PASS (146) | PASS (94) |
| Total vs Kactus | PASS (146 vs 146, hoja `ago, A`) | PASS (94 vs 94, hoja `Ago II`) |
| Sin identificaciones repetidas | PASS | PASS |
| `Empresa` homologada | **FALLA** (0 de 11 con match) | **FALLA** (0 de 10 con match) |
| `Grupo empresarial` coherente | **FALLA** | **FALLA** |

Agosto 2026 quedo cargado con la nomenclatura cruda de Kactus:

| Campo | Junio y julio 2026 | Agosto 2026 |
|---|---|---|
| `Grupo empresarial` | `Challenger`, `Grupo Sky`, `Habitel Hotels`, `Lemco` | `CHALLENGER S.A.S.`, `HABITEL S.A.S.`, `LEMCO SAS`, `SKY INDUSTRIAL`, `SKY LOGISTICA INTEGRAL` |
| `Empresa` en `RETIROS` | `Challenger`, `Habitel Prime`, `Lemco Salvio`... | `1`, `2`, `3`, `4`, `100`, `103`, `104`, `202`, `203`, `204` |
| `Empresa` en `INGRESOS` | nombres del catalogo | `CASINO NORMAL C.M.`, `SIN CASINO`, `ELECCION TEMPORAL S.A.`, `PRIME`, `SELECT`, `LEMCO S.A` |

Consecuencias:

- **240 registros** (146 ingresos + 94 retiros) quedan fuera de la relacion con
  `Empresas` y apareceran en blanco al segmentar por empresa.
- **`Grupo Sky` desaparece como grupo** en agosto: se divide en `SKY INDUSTRIAL` y
  `SKY LOGISTICA INTEGRAL` como si fueran grupos independientes. Afecta
  directamente la vista por empresa que solicito Gestion Humana de Grupo SKY.
- En `RETIROS` los codigos numericos impiden identificar la empresa sin un mapeo
  externo.

**Correccion requerida antes de refrescar Power BI:** reemplazar en Excel los
valores de `Grupo empresarial` y `Empresa` de agosto 2026 por los del catalogo
homologado, y volver a ejecutar el validador hasta obtener `PASS`.

## Automatizar primero la validacion, no la escritura

`PptovsReal.xlsx` **no debe editarse con scripts** (`openpyxl` u equivalentes): el
libro contiene 12 tablas dinamicas, 9 caches, 1 conexion y decenas de miles de
formulas, entre ellas 68.365 en `INGRESOS` y 24.136 en `RETIROS`. `openpyxl` no
preserva las tablas dinamicas y al guardar obliga a elegir entre conservar las
formulas perdiendo los valores en cache, o conservar los valores destruyendo las
formulas. La escritura es manual en Excel.

Ruta sugerida:

1. **Validacion automatizada (implementado).** Ejecutar el validador despues de
   cada carga manual. Habria detectado la nomenclatura cruda de agosto antes de
   llegar al modelo.
2. **Tabla de homologacion explicita.** Publicar el mapeo
   `Codigo Empresa -> Empresa -> Grupo empresarial` en una hoja de referencia del
   propio libro, para que la carga no dependa de la memoria de quien la ejecuta.
3. **Power Query dentro del libro.** Una consulta que lea el consolidador, aplique
   el mapeo del punto 2 y genere las filas del mes. Elimina la transcripcion manual
   conservando el libro y sus tablas dinamicas.

## Referencias

- `Docs/DATA_PIPELINE.md`, seccion "Flujo de contratos Kactus".
- `Docs/ACTUALIZACION_PLANTA_PERSONAL_DOTACION.md`, corte mensual de dotacion.
- `Docs/METRICS_CATALOG.md`, seccion "Poblacion de origen de `Ingresos` y `Retiros`".
