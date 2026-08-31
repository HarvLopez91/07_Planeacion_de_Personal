# 0024 - Análisis de impacto: Sociodemográfico por Empresa (PBIP-006)

## Objetivo

Crear una nueva página `Sociodemográfico por Empresa` que permita comparar
simultáneamente la distribución de los principales indicadores
sociodemográficos entre las empresas del Grupo LEMCO, reutilizando
`Demográfico (Promedio)` como punto de partida, sin alterar su
funcionamiento ni el modelo semántico.

Este documento analiza el impacto de la duplicación ya realizada y deja
especificado el MVP de 4 visuales antes de implementarlo. No autoriza su
implementación por sí mismo.

> **Nota de vigencia (2026-08-27):** las secciones originales de este
> documento (hasta "Estado de versionamiento") describen el análisis de
> impacto **previo a la implementación**. La implementación avanzó
> sustancialmente más allá del MVP de 4 visuales aquí propuesto — ver
> "Checkpoint pre-corrección" más abajo para el estado real y vigente.

## Checkpoint pre-corrección — Perfil Sociodemográfico por Empresa (2026-08-27)

Este commit representa un **punto de recuperación intermedio**, no una
implementación final. El usuario detiene el desarrollo en este estado para
aplicar una corrección posterior; retomar desde aquí, no desde el MVP
original descrito abajo.

### Página creada

`Sociodemográfico por Empresa` (`1daffd26f7de1c038e95`), derivada de
`Demográfico (Promedio)` (`ReportSectionf46593dd92bf9359ceef`). La página
origen se preserva intacta — ver clasificación `RESERIALIZATION` más abajo.

### Dimensión utilizada

Los comparativos de esta página utilizan actualmente
`PLANTA DE PERSONAL[GRUPO EMPRESA]` como dimensión empresarial funcional
(no `Empresas[Grupo Empresa]`, que era la propuesta original de este
documento — la implementación real usa el campo nativo de la tabla de
hechos, sin necesidad de atravesar la relación con `Empresas`). Validado en
sesión interactiva de Power BI Desktop por el usuario: los 7 comparativos
responden correctamente a esta dimensión, sin `(En blanco)`. No se
documenta Formula Firewall ni diferencias de mayúsculas/minúsculas como
causa raíz demostrada de ningún comportamiento observado — no fue
necesario diagnosticar una causa, el campo ya funciona correctamente.

### Estructura actual

**Filtros**, en una sola fila horizontal:
Año · Mes · Grupo Empresa · Nombre Empresa · Tipo de Contrato · Tipo de
Cargo · Dependencia · Área · Cargo.

**Comparativos** (todos por `PLANTA DE PERSONAL[GRUPO EMPRESA]`, medida
`Tbl_Medidas[Tot_empleados_Promedio]`, sin medidas nuevas):

1. Colaboradores por Empresa
2. Tipo de Contrato por Empresa
3. Generación por Empresa
4. Tipo de Cargo por Empresa
5. Distribución de Género por Empresa
6. Antigüedad por Empresa
7. Colaboradores por Empresa, Dependencia y Cargo

### Decisiones registradas

- `Generación por Antigüedad` fue retirada de esta página (no comparaba por
  empresa, rompía la narrativa comparativa de la página; sin dependencias
  de bookmarks ni otros visuales, verificado antes de eliminar).
- La matriz de colaboradores usa jerarquía de filas `Empresa → Dependencia
  → Cargo`.
- La columna `%` de esa matriz fue retirada: su fórmula
  (`Divide(Tot_empleados_Promedio, ScopedEval(Tot_empleados_Promedio,
  Scope=[]))`) calcula participación sobre el **total general**, no dentro
  de cada empresa — habría inducido a una lectura incorrecta. No se creó
  una medida nueva para corregirlo; un `% dentro de empresa` correcto queda
  como pendiente para una iniciativa posterior.
- Modelo semántico, relaciones, medidas DAX y Power Query **no fueron
  modificados intencionalmente** en ningún punto de esta implementación.

> El desarrollo se detiene en este punto como checkpoint recuperable antes
> de una corrección posterior solicitada por el usuario.

## Corrección estructural priorizada — Dim_Dependencia / Dim_Area (2026-08-28)

La corrección posterior anunciada arriba resultó ser **estructural, no
visual**. Se priorizó sobre la continuación de `Sociodemográfico por
Empresa`: la página queda detenida en el checkpoint `d154b71` hasta cerrar
esta corrección, porque sus visuales de `Dependencia` y `Área` dependen de
un modelado correcto de esas dos entidades.

### Fuente efectiva de `PLANTA DE PERSONAL`

Contrario a lo que sugiere el nombre de la tabla, su partición M **no** lee
una hoja homónima única. Combina dos orígenes de SharePoint corporativo
mediante `Table.Combine`:

| Origen | Archivo (SharePoint) | Hoja | Filas |
|---|---|---|---|
| Histórico | `Data/HeadCount/2024/Consolidado 2024.xlsx` | `PLANTA DE PERSONAL` | 25.536 |
| Vigente | `Data/HeadCount/2025/Consolidado 2025.xlsx` (vía consulta `Consolidado2025`) | `Consolidado2025` | 45.670 |
| **Total combinado** | | | **71.206** |

Pese al nombre `Consolidado 2025`, el segundo archivo contiene tanto 2025
(27.996 filas) como 2026 (17.674 filas).

### Grano de las dimensiones

Ambas dimensiones se derivan de `PLANTA DE PERSONAL` (no de una fuente
externa), filtrando filas con `GRUPO EMPRESA`, `DEPENDENCIA` o `AREA`
vacíos, y normalizando con `Text.Upper(Text.Trim(...))`:

| Dimensión | Grano | Clave | Cardinalidad |
|---|---|---|---|
| `Dim_Dependencia` | `GRUPO EMPRESA` × `DEPENDENCIA` | `Key_Dependencia` = `GRUPO EMPRESA\|DEPENDENCIA` | **67 combinaciones no nulas `GRUPO EMPRESA + DEPENDENCIA`** |
| `Dim_Area` | `GRUPO EMPRESA` × `DEPENDENCIA` × `AREA` | `Key_Area` = `GRUPO EMPRESA\|DEPENDENCIA\|AREA` | **372 combinaciones no nulas `GRUPO EMPRESA + DEPENDENCIA + AREA`** |

La lectura correcta de estas cifras es **combinatoria, no de catálogo**: 67
no es "el número de dependencias" ni 372 "el número de áreas". Son
combinaciones distintas y no nulas de los campos indicados — una misma
`DEPENDENCIA` puede aparecer bajo varios `GRUPO EMPRESA`, y una misma `AREA`
bajo varias dependencias; cada ocurrencia cuenta como una combinación
propia. Interpretarlas como conteos de entidades sobreestimaría el catálogo
real de dependencias y áreas del Grupo.

Ambas cifras fueron confirmadas por dos vías independientes: carga real en
sesión interactiva de Power BI Desktop (`Dim_Dependencia`: 67 filas;
`Dim_Area`: 372 filas) y derivación directa desde los archivos fuente.

`PLANTA DE PERSONAL` expone `Key_Dependencia` y `Key_Area` como columnas
calculadas en M, relacionadas N:1 con sus dimensiones. **No se introdujo
ninguna relación many-to-many.**

### Defecto corregido: orden de `Table.Distinct`

La primera implementación aplicaba `Table.Distinct` sobre el texto **crudo**
(sensible a mayúsculas y espacios) y **después** construía la clave
normalizada. Dos filas que difieren solo en espacios sobreviven al
`Distinct` pero colapsan en la misma clave, rompiendo la unicidad exigida
por el lado "uno" de una relación.

Power BI Desktop lo detectó con el error:

> La columna `'Key_Area'` de la tabla `'Dim_Area'` contiene un valor
> duplicado `'HABITEL HOTELS|DIRECCIÓN OYS|RECEPCIÓN'`

Causa raíz: una única fila de `Consolidado 2024.xlsx` con `AREA` =
`'RECEPCIÓN '` (espacio final) frente a `'RECEPCIÓN'`. La corrección invierte
el orden — construir la clave normalizada primero, luego
`Table.Distinct(..., {"Key_Area"})` sobre la clave final. `Dim_Dependencia`
no presentaba duplicados, pero tenía el mismo defecto estructural y se
corrigió preventivamente.

### Calidad de datos observada — 1.399 registros sin clave dimensional

De las 71.206 filas combinadas, **1.399 tienen `DEPENDENCIA` o `AREA` en
blanco, todas correspondientes a 2026** (0 en 2024 y 0 en 2025).

Estas filas **no fueron inventadas ni eliminadas**. Permanecen íntegras en
`PLANTA DE PERSONAL`: siguen siendo registros válidos del hecho y se cuentan
en cualquier medida que no dependa de estas dimensiones. Lo único que ocurre
es que el filtro de blancos las deja **sin clave dimensional** — su
`Key_Dependencia` y/o `Key_Area` es `null`, por lo que no generan entrada en
`Dim_Dependencia` ni en `Dim_Area` y **no inflan** las cifras de 67 y 372.
Tampoco se les asignó una clave sustituta ni una categoría inventada.

No se corrigen aquí: es una brecha de completitud de la fuente, no un
defecto del modelo. Implica que cualquier visual que cruce hechos de 2026
contra estas dimensiones dejará esos 1.399 registros sin clasificar —
comportamiento esperado y documentado, no una pérdida silenciosa. Pendiente
de decisión del usuario sobre su tratamiento (homologación en origen, o
categoría explícita "Sin asignar" en el modelo).

### Alcance deliberadamente acotado

- **`Estructura` y `AREAS` NO se retiran todavía.** Ambas siguen en el
  modelo y en uso. Su eventual reemplazo por `Dim_Dependencia`/`Dim_Area`
  requiere análisis de impacto propio sobre medidas y visuales
  dependientes, y no forma parte de esta corrección.
- **La migración del resto de tablas de hechos queda para una fase
  posterior.** Esta corrección solo conecta `PLANTA DE PERSONAL` con las
  dos dimensiones nuevas. Ningún otro hecho se repunta.
- La corrección se aísla al mínimo funcional: se excluyen del checkpoint
  las columnas `ID_Jefe_Inmediato` / `Jefe Inmediato (nombre-apellido)` /
  `Descripción Cargo_Jefe Inmediato`, la eliminación de la columna huérfana
  `%`, y todo el ruido de reserialización de bookmarks, visuales, cultures,
  `diagramLayout` y `Tbl_Medidas`.

### Pendiente no resuelto

El refresh completo sigue reportando **6 consultas con errores** (incluida
`Ppto Retiros`), sin relación con esta corrección. `PLANTA DE PERSONAL`
conserva `annotation PBI_ResultType = Exception` desde antes del checkpoint
`d154b71`. Ese frente se revisa por separado y no se mezcla con esta fase.

## Alcance

- Analiza únicamente la creación de la página y el MVP de 4 visuales
  descritos más abajo.
- No incluye crear medidas nuevas, relaciones nuevas, ni modificar
  `Demográfico (Promedio)`.
- No incluye resolver el riesgo de Formula Firewall / caché de
  `PLANTA DE PERSONAL` (ver sección de riesgos).

## Página origen y preservación obligatoria

- Página origen: `Demográfico (Promedio)` (`ReportSectionf46593dd92bf9359ceef`,
  31 visuales).
- Página nueva: `Sociodemográfico por Empresa` (`1daffd26f7de1c038e95`, 31
  visuales duplicados 1:1 en el momento de la creación).
- `Demográfico (Promedio)` **debe permanecer intacta**. La comparación contra
  la línea base (ver más abajo) confirmó que, al momento de la duplicación,
  sus únicos cambios fueron de normalización de salto de línea final (sin
  contenido distinto). Ninguna iteración de implementación de
  `Sociodemográfico por Empresa` debe tocar archivos de la página origen.

## Dimensión corporativa y relaciones reutilizadas

Validado en modo lectura, sin modificar nada:

- `Empresas[Empresas]`: nivel de detalle por empresa individual.
- `Empresas[Grupo Empresa]`: nivel corporativo (agrupa empresas del Grupo
  LEMCO). **Este es el nivel usado en el MVP.**
- Relación activa `'PLANTA DE PERSONAL'.'Nombre Empresa'` → `Empresas.Empresas`
  (`relationships.tmdl`, sin propiedades especiales — dirección simple,
  many-to-one).
- Relación activa `Empresas.'Grupo Empresa'` → `'Grupo Empresarial'.'Grupo Empresarial'`.

No se requiere crear ninguna relación nueva: el modelo ya permite filtrar
`PLANTA DE PERSONAL` (y por extensión las medidas de `Tbl_Medidas` que la
usan) por `Empresas[Grupo Empresa]` a través de la cadena de relaciones
existente.

## Línea base y resultado del diff

- Línea base capturada manualmente (`pbip_triage` no existe en este
  repositorio; existe en el proyecto hermano `10_Indicadores_de_Desempeno`
  con estructura distinta) en
  `Outputs/sociodemografico_por_empresa_baseline_2026-08-26.json`: manifiesto
  SHA-256 de 385 archivos de `PBIP/`, rama `feat/sociodemografico-por-empresa`
  desde `origin/main` (`5f48fc1`), 15 páginas, página origen con 31 visuales.
- Tras la duplicación manual en Power BI Desktop: 385 → 420 archivos (35
  agregados, 0 eliminados, 21 modificados).

## Clasificación FUNCTIONAL_CHANGE / RESERIALIZATION

| Archivo(s) | Clasificación | Evidencia |
|---|---|---|
| `pages/1daffd26f7de1c038e95/` (page.json + 31 visuales) | `FUNCTIONAL_CHANGE` | Página nueva `displayName: "Sociodemográfico por Empresa"`, 31 visuales — mismo conteo que el origen |
| `pages/pages.json` | `FUNCTIONAL_CHANGE` | Agrega el id de la página nueva a `pageOrder` y actualiza `activePageName` (bump de `$schema` 1.0.0→1.1.0 es efecto colateral inevitable) |
| 10 `bookmarks/*.bookmark.json` | `RESERIALIZATION` (verificada) | Migración de schema `1.4.0`→`2.1.0`; elimina referencias a 2 GUIDs de visual que **no existen en ninguna página actual** (confirmado con `grep` sobre todo `PBIP/`) — limpieza de referencias muertas, sin efecto funcional |
| 4 `visuals/*/visual.json` dentro de `Demográfico (Promedio)` | `RESERIALIZATION` | Únicamente `\ No newline at end of file`; cero cambio de contenido |
| `DAXQueries/Demográfico (Promedio).dax` | `RESERIALIZATION` | Cambio de fin de línea únicamente; `git diff` no muestra contenido distinto |
| `cultures/es-ES.tmdl` | `RESERIALIZATION` | Archivo completo es `linguisticMetadata` (sinónimos Q&A), regenerado automáticamente por Desktop al guardar |
| `Consolidado2025.tmdl`, `PLANTA DE PERSONAL.tmdl` | `RESERIALIZATION` | 1 línea en blanco eliminada en cada uno; ninguna fórmula ni propiedad cambiada |
| `Tbl_Medidas.tmdl` | `RESERIALIZATION` | Espacio en blanco agregado a 6 líneas vacías dentro de fórmulas DAX existentes; ninguna fórmula cambiada |
| `diagramLayout.json` | `RESERIALIZATION` | Posición de scroll del lienzo del modelo, diferencia de 0.5 px |
| `.pbi/localSettings.json` ×2, `.pbi/cache.abf` | No aplica a Git | Excluidos por `PBIP/.gitignore` |

Caso verificado en detalle: un visual duplicado (tabla "Generación por
Antigüedad en la Compañía") mostraba menos entradas en
`filterConfig.filters` que el original (5 vs. 1). Se comprobó que las 4
entradas faltantes nunca tuvieron condición de filtro aplicada (placeholders
vacíos del panel de filtros); el único filtro con condición real está
presente e idéntico en ambas. Es el único caso así entre 31 pares de
visuales (30/31 coinciden exactamente). Clasificado `RESERIALIZATION` con
evidencia, no por suposición.

**No se identificó ningún caso `REVIEW_REQUIRED` pendiente.**

## Confirmación del estado sin datos en ambas páginas

El usuario verificó manualmente en Power BI Desktop que **tanto
`Demográfico (Promedio)` como `Sociodemográfico por Empresa` muestran el
mismo aviso** de tablas con datos incompletos o sin datos. Esto confirma que
el estado sin datos:

- no fue provocado por la duplicación de la página;
- es una condición del modelo/caché, no de una página en particular.

## Riesgo conocido de caché/import/Formula Firewall (no se resuelve aquí)

- `PLANTA DE PERSONAL` es una tabla `mode: import` (Power Query, origen
  SharePoint).
- `.pbi/cache.abf` del modelo semántico fue un archivo **nuevo** en la
  comparación contra la línea base: es la primera carga del modelo en este
  worktree, por lo que el caché de datos import está vacío hasta actualizar.
- `CLAUDE.md` de este proyecto ya documenta como riesgo crítico vigente un
  bloqueo de Formula Firewall específicamente sobre `PLANTA DE PERSONAL`.
- Esta iniciativa **no intenta resolver ese riesgo**. La implementación de
  los 4 visuales del MVP puede completarse funcionalmente en su definición
  JSON/TMDL sin necesidad de que el caché esté poblado; la validación visual
  con datos reales queda supeditada a que se resuelva `DATA-001` (Formula
  Firewall) o a que un refresh exitoso se ejecute y valide por separado, con
  evidencia visual, conforme a la regla ya vigente del proyecto.

## Propuesta de MVP — 4 visuales

Medida reutilizada en los 4 casos: `Tbl_Medidas[Tot_empleados_Promedio]`
(ya usada en la página origen, sin cambios). Ninguno de los 4 requiere medida
nueva ni relación nueva.

### 1. Colaboradores por Grupo Empresa

| Campo | Valor |
|---|---|
| Visual actual | `card` (KPI único, campo `Colaboradores`) |
| Visual objetivo | Gráfico de columnas |
| Eje | `Empresas[Grupo Empresa]` |
| Leyenda | No aplica (una serie) |
| Medida | `Tot_empleados_Promedio` |
| Cambio requerido | Reemplazar el visual `card` por `columnChart`; asignar `Empresas[Grupo Empresa]` al eje; mantener la medida existente en Valores |
| Criterio de validación | Una barra por Grupo Empresa, visibles simultáneamente sin depender del slicer de Nombre Empresa/Grupo Empresa |

### 2. Tipo de Contrato por Grupo Empresa

| Campo | Valor |
|---|---|
| Visual actual | `clusteredColumnChart` (categoría = `TIPO_CONTR (grupos)`) |
| Visual objetivo | Mismo tipo (`clusteredColumnChart`) o 100% apilado, a definir en implementación |
| Eje | `Empresas[Grupo Empresa]` |
| Leyenda | `TIPO_CONTR (grupos)` (campo actualmente en el eje, se traslada a leyenda) |
| Medida | `Tot_empleados_Promedio` |
| Cambio requerido | Reasignar campos: eje actual (`TIPO_CONTR (grupos)`) pasa a leyenda; `Empresas[Grupo Empresa]` pasa a eje |
| Criterio de validación | Cada Grupo Empresa muestra su propia composición de tipo de contrato, comparable visualmente contra las demás empresas en el mismo gráfico |

### 3. Generación por Grupo Empresa

| Campo | Valor |
|---|---|
| Visual actual | `funnel` (categoría = `GENERACIÓN`, valor = `%TG Tot_empleados_Promedio`) |
| Visual objetivo | Columnas 100% apiladas (`hundredPercentStackedBarChart` o `hundredPercentStackedColumnChart`) — decidido por el usuario |
| Eje | `Empresas[Grupo Empresa]` |
| Leyenda | `PLANTA DE PERSONAL[GENERACIÓN]` |
| Medida | `Tot_empleados_Promedio` (conteo existente; **sin medida nueva de porcentaje** — decisión del usuario para esta primera iteración) |
| Cambio requerido | Reemplazar `funnel` por columnas 100% apiladas; eje = Grupo Empresa; leyenda = Generación; valores = `Tot_empleados_Promedio`. La comparación porcentual la resuelve la normalización propia del visual 100% apilado, no una medida |
| Criterio de validación | Cada barra de empresa suma 100% visualmente (normalización nativa del visual); composición generacional comparable entre empresas en un solo gráfico |

### 4. Tipo de Cargo por Grupo Empresa

| Campo | Valor |
|---|---|
| Visual actual | `barChart` (categoría = `Tipo de Cargo` + `NIVEL_DE_CARGO`, 2 dimensiones) |
| Visual objetivo | `barChart` o `clusteredColumnChart`, 1 dimensión de detalle |
| Eje | `Empresas[Grupo Empresa]` |
| Leyenda | `Tipo de Cargo` (se deja `NIVEL_DE_CARGO` fuera del MVP para no sobrecargar el gráfico con 5 empresas × 2 dimensiones) |
| Medida | `Tot_empleados_Promedio` |
| Cambio requerido | Simplificar a 1 dimensión de detalle (`Tipo de Cargo`) en leyenda; `Empresas[Grupo Empresa]` en eje; retirar `NIVEL_DE_CARGO` de este visual del MVP |
| Criterio de validación | Composición por tipo de cargo comparable entre las 5 empresas en un solo gráfico, legible sin desbordar categorías |

## Criterio de conciliación futura (para la validación posterior a la implementación)

Para cada uno de los 4 visuales, una vez el caché tenga datos:

> Suma de `Tot_empleados_Promedio` de los Grupos Empresa mostrados = total
> general de `Tot_empleados_Promedio` para el mismo Año/Mes y el mismo
> contexto de filtros (segmentadores de la página).

Esto detecta dobles conteos, filtros mal aplicados, o pérdida de filas por
relaciones inactivas/direccionamiento incorrecto al momento de validar con
datos reales.

## Riesgos y pendientes

- El riesgo de Formula Firewall / caché de `PLANTA DE PERSONAL` (`DATA-001`)
  no se resuelve en esta iniciativa; bloquea únicamente la **validación
  visual con datos reales**, no la implementación de la definición de los
  visuales.
- Componente 3 (Generación): se decidió explícitamente NO crear una medida
  de porcentaje por empresa en esta iteración; si en el futuro se requiere
  un `%` explícito distinto al que normaliza el visual 100% apilado, será
  una iniciativa separada.
- El caso `RESERIALIZATION` de los 10 bookmarks (limpieza de referencias
  muertas por migración de schema) y los demás archivos de ruido deben
  reevaluarse al cierre de la implementación, ya que Power BI Desktop puede
  regenerarlos de nuevo durante las siguientes ediciones — no se limpian
  todavía.

## Estado de versionamiento

> **Actualizado 2026-08-27 — ver "Checkpoint pre-corrección" arriba para el
> estado funcional real.** Lo siguiente describe el estado en el momento en
> que se escribió el análisis de impacto original; ya no es vigente.

Rama de trabajo: `feat/sociodemografico-por-empresa`, creada desde
`origin/main` (`5f48fc1`) en worktree aislado
(`.wt/sociodemografico-por-empresa`).

~~No se ha hecho staging, commit ni push de ningún archivo de esta
iniciativa. No se ha implementado ningún visual del MVP.~~ Este commit
crea el primer checkpoint: staging selectivo, commit y push de la página,
`pages.json` y esta Spec — ver "Checkpoint pre-corrección". La
implementación avanzó más allá del MVP original de 4 visuales (7
comparativos implementados) y **no está cerrada**: el usuario detiene el
desarrollo aquí para aplicar una corrección posterior.

## Cierre técnico PBIP-006 — solución final validada (2026-08-31)

> Esta sección describe el **estado final vigente** de la iniciativa y
> reemplaza funcionalmente a las secciones anteriores, que se conservan por
> trazabilidad histórica.

### Estado

| Dimensión de validación | Estado |
|---|---|
| Funcional | `PASS FUNCIONAL` |
| Visual | `PASS VISUAL` |

Página: `Sociodemográfico por Empresa`
(`PBIP/Proyecto.Report/definition/pages/1daffd26f7de1c038e95`).

### Modelo organizacional

`Dim_Estructura_Organizacional`, catálogo **dinámico** derivado de
`PLANTA DE PERSONAL` mediante Power Query (`Origen = #"PLANTA DE PERSONAL"`
más `Table.Distinct`). No existe catálogo hardcodeado: empresas, dependencias
y áreas nuevas se incorporan automáticamente en el siguiente refresh.

- Grano: `GRUPO EMPRESA + Nombre Empresa + DEPENDENCIA + AREA`.
- Clave técnica: `Key_Estructura`, construida como
  `GRUPO|EMPRESA|DEPENDENCIA|AREA` con normalización `Text.Trim` y `Text.Upper`
  sobre cada componente.
- Se descartan únicamente las filas sin `GRUPO EMPRESA` o sin `Nombre Empresa`.
- Rutas parciales soportadas de forma intencional (`GRUPO|EMPRESA||` y
  `GRUPO|EMPRESA|DEPENDENCIA|`) para admitir registros futuros pendientes de
  clasificación. Su exclusión es **visual** (slicers), nunca del modelo.

Integridad verificada contra el modelo vivo: **0 duplicados**, **0 huérfanos**,
**cobertura 100 %**, **0 claves nulas**.

### Fotografía validada (2026-08-31)

| Métrica | Valor |
|---|---|
| `PLANTA DE PERSONAL` | 71.206 filas |
| Registros pendientes de Dependencia/Área | 0 |
| `Dim_Estructura_Organizacional` | 568 claves |
| `DISTINCTCOUNT(Key_Estructura)` en `PLANTA DE PERSONAL` | 568 |
| `Dim_Dependencia` | 64 |
| `Dim_Area` | 369 |
| Relaciones del modelo | 69 |

Fuente de la fotografía: `Consolidado 2024.xlsx` y `Consolidado 2025.xlsx`
(SharePoint corporativo). Las cifras son **fotografías temporales** de una
versión concreta de la fuente, no constantes del modelo: se documentó el caso
`SOURCE_CHANGED` en el que 585, luego 580 y finalmente 568 claves respondieron
a reclasificaciones manuales del archivo fuente, sin defecto de código.

### Vigencia observada

`Dim_Estructura_Organizacional[Periodo_Min]` y `[Periodo_Max]`, tipo `int64`,
formato **`YYYYMM`**, ocultas, derivadas por `Table.Group` sobre
`Key_Estructura` (`List.Min` y `List.Max`). Sin fechas hardcodeadas.

Representan **VIGENCIA OBSERVADA**, **no** la vigencia oficial del organigrama.
No existe fuente maestra corporativa con `Fecha Desde` y `Fecha Hasta` de
dependencias y áreas; se auditaron `Estructura`, `AREAS`, `Planta Ppto`,
`Ppto Ingresos`, los proyectos hermanos 04 y 10, y el maestro Kactus
`QryBiCargo` (que sí tiene `Fecha de Creación` e `Ind. Actividad`, pero
**solo a nivel de Cargo**, sin Dependencia ni Área).

Regla de visibilidad:

`Periodo_Min <= Periodo seleccionado <= Periodo_Max`

Si una Dependencia o Área aparece **al menos una vez** en `Consolidado
2024.xlsx` o `Consolidado 2025.xlsx`, se considera que existió históricamente.

**Los huecos internos NO implican cierre.** Decisión deliberada: el 29,9 % de
las 568 estructuras (170) presentan huecos intermedios y reaparecen, con un
hueco máximo de 16 meses; 102 desaparecen 3 meses o más y vuelven. La ausencia
temporal de colaboradores no equivale a cierre de la estructura, por lo que
**no se usa `Tot_empleados_Promedio > 0` como criterio de vigencia**.

#### Caso de control — `COORDINACIÓN DE GESTIÓN HUMANA`

`GRUPO SKY`, presente en SKY FORWARDER, SKY INDUSTRIAL y SKY LOGÍSTICA
INTEGRAL. `Periodo_Min` igual a `202401`, `Periodo_Max` igual a `202503`.

| Periodo | Resultado esperado | Verificado |
|---|---|---|
| 2024-06 (hueco interno) | visible | Sí |
| 2025-03 (`Periodo_Max`) | visible | Sí |
| 2026-07 | **no visible** | Sí |
| 2023-12 (antes de `Periodo_Min`) | no visible | Sí |

### Periodo de análisis

Regla funcional de la página: **1 Año más 1 Mes es igual a 1 periodo**.

- `Año` (`'PLANTA DE PERSONAL'[AÑO]`): selección única mediante
  `strictSingleSelect: true` (con `singleSelect: false` y
  `selectAllCheckboxEnabled: false`). **`singleSelect` por sí sola no produce
  selección única en Power BI Desktop**: corresponde a "Selección múltiple con
  CTRL". La propiedad que gobierna "Selección única" es `strictSingleSelect`,
  patrón validado contra el slicer `Años[Año]` de la página `Gasto Laboral`.
- `Mes` (`'PLANTA DE PERSONAL'[MES]`): selección única.
- Ambos **desacoplados** de los `syncGroup` heredados `AÑO` y `MES`: se retiró
  el bloque `syncGroup` de los slicers de esta página, sin modificar los
  miembros de `Demográfico` ni `Demográfico (Promedio)`, que conservan su
  sincronización entre sí.

Todos los KPIs, gráficos, comparativos y matriz calculan **exclusivamente** el
Año-Mes seleccionado. `Periodo_Min` y `Periodo_Max` **no amplían** el periodo
de cálculo: su única función es determinar la disponibilidad de opciones en los
slicers organizacionales.

### Slicers organizacionales

Los cuatro leen de `Dim_Estructura_Organizacional` y aplican el filtro de
visual `Estructura Visible Periodo = 1`:

| Slicer | Visual | Campo |
|---|---|---|
| Grupo Empresa | `a19d9473fbf6256b473b` | `[GRUPO EMPRESA]` |
| Nombre Empresa | `c3b9416c6f44bc63690a` | `[Nombre Empresa]` |
| Dependencia | `5a7168a7f509acada7d2` | `[DEPENDENCIA]` |
| Área | `716620875f71ee0ad121` | `[AREA]` |

Dependencia y Área excluyen visualmente `null` y cadena vacía, conservando esas
rutas parciales en el modelo.

Medida `Estructura Visible Periodo` (`Tbl_Medidas`, carpeta `00 Utilidades`):
lee el periodo seleccionado con `ALLSELECTED` sobre `[AÑO]` y `[MES]` —
necesario porque la relación fluye de la dimensión al hecho y, sin
`ALLSELECTED`, la medida degeneraría en presencia exacta y ocultaría las 170
estructuras con huecos. Devuelve 1 si existe al menos una `Key_Estructura` del
elemento evaluado cuyo intervalo cubre el periodo, por lo que funciona sin
variantes en los cuatro niveles de la cascada
`Grupo → Empresa → Dependencia → Área`.

### Relaciones

Relación nueva:
`'PLANTA DE PERSONAL'[Key_Estructura] → Dim_Estructura_Organizacional[Key_Estructura]`

- Cardinalidad **Many→One**
- **Active**
- **OneDirection**
- **SingleColumn**

**0 relaciones many-to-many nuevas** y **0 bidireccionales nuevas**. Las dos
relaciones especiales preexistentes (`Trimestres` con `Mes`, bidireccional 1:1,
y `AUSENTISMOS` con `Incapacidades`, bidireccional M:M) **no se modifican**.
Total del modelo: 69 relaciones, sin variación.

### Diseño

`PASS VISUAL`. Tipografía **Outfit** en toda la página, incluido el navegador
(se eliminó el remanente de Calibri). Paleta corporativa LEMCO según
`Assets/Brand/Manual Marca Grupo LEMCO.pdf`:

`#1B487F` · `#1A3059` · `#000032` · `#0B1C35` · `#F7931E`

Se eliminaron los colores fuera de identidad que existían (`#17406C`,
`#12294A`, `#094780`, `#2B455E`, `#5A6472`, `#DCE5F0`). Donde una rampa ordinal
exigía más pasos de los que ofrece la paleta principal — `Antigüedad por
Empresa`, 7 categorías — se emplearon secundarios ya validados del proyecto 04
(`#4A7FC0`, `#7EB3E8`), sin introducir variantes nuevas.

Títulos homogéneos: los seis gráficos en Outfit 14D negrita centrada; la
matriz en 13D por densidad. La matriz recibió fondo propio para integrarse con
los demás contenedores. Navegación preservada sin cambios funcionales.

### Fuera de alcance (no bloquea el cierre)

- Tema LEMCO global del reporte y cambio de `report.json` (afectaría a las 16
  páginas; requiere iniciativa propia con validación página por página).
- Dimensión calendario futura.
- Corrección global de `Tot_empleados_Promedio` para escenarios multiaño: la
  medida promedia sobre `[MES]` (nombre del mes, no año-mes), por lo que con
  varios años seleccionados **suma** en vez de promediar. En esta página queda
  acotada por la regla de periodo único; el defecto persiste en `Demográfico`
  y `Demográfico (Promedio)`.
- Refactor del lienzo (banda y grupo declarados a 2300 px sobre una página de
  2100 por 900).
- Retícula, alturas de fila y normalización de anchos de slicers.
- Errores `#N/A` conocidos de Power Query (36 en esta ejecución, variables
  entre refrescos; documentados en `Specs/0020` sección 15.4). No afectan a
  ninguna de las cuatro columnas que construyen `Key_Estructura`.
- Retiro de tablas legacy (`Estructura`, `AREAS`) que todavía tienen
  consumidores en otras páginas.
