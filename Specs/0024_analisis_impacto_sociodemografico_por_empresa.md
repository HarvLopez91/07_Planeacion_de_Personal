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
