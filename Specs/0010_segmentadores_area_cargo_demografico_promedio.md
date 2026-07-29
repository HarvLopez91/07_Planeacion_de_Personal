# Segmentadores Area y Cargo en Demografico (Promedio)

Fecha: 2026-07-29

## Objetivo

Incorporar dos segmentadores adicionales en el panel lateral izquierdo de la
pagina `Demografico (Promedio)` para permitir el filtrado jerarquico por:

- Dependencia
- Area
- Cargo

El ajuste mantiene el diseno existente del panel y no modifica medidas,
relaciones, fuentes, consultas ni paginas diferentes.

## Alcance

- Proyecto: `PBIP/Proyecto7.pbip`
- Pagina: `Demografico (Promedio)`
- Page ID: `ReportSectionf46593dd92bf9359ceef`
- Grupo principal del panel: `20644d3047b208148676`

## Estado anterior

El panel lateral contaba con segmentadores de ano, mes, tipo de contrato, grupo
empresa, nombre empresa, tipo de cargo y dependencia. El segmentador de
dependencia estaba configurado como desplegable con busqueda, seleccion multiple
y opcion `Seleccionar todo`.

Geometria anterior de `Dependencia`:

| Visual | X | Y | W | H |
|---|---:|---:|---:|---:|
| `a58d5b2e9f6c4a21b103` | 17.94 | 686.99 | 240.03 | 72.13 |

## Campos utilizados

| Segmentador | Campo |
|---|---|
| Dependencia | `Estructura[DEPENDENCIA]` |
| Area | `PLANTA DE PERSONAL[AREA]` |
| Cargo | `PLANTA DE PERSONAL[CARGO]` |

Se usa `PLANTA DE PERSONAL[AREA]` y `PLANTA DE PERSONAL[CARGO]` para conservar
las combinaciones existentes dentro de la planta y permitir que el contexto de
dependencia reduzca naturalmente las opciones disponibles. No se crearon ni
modificaron relaciones.

## Configuracion

Los nuevos segmentadores replican el patron de `Dependencia`:

- tipo visual `slicer`;
- modo `Dropdown`;
- busqueda habilitada mediante `selfFilterEnabled = true`;
- seleccion multiple (`singleSelect = false`);
- opcion `Seleccionar todo` habilitada;
- sin seleccion predeterminada;
- filtro visual para excluir valores `null` o cadena vacia;
- estilo, fondo, tipografia y proporcion equivalentes a los segmentadores
  existentes.

## Visuales incorporados

| Segmentador | Visual ID | Campo | X | Y | W | H | Tab order |
|---|---|---|---:|---:|---:|---:|---:|
| Area | `a93404e0eabc48bb9e8e` | `PLANTA DE PERSONAL[AREA]` | 18.38 | 734.99 | 239.15 | 72.17 | 15001 |
| Cargo | `83a053e3e767d88dd07a` | `PLANTA DE PERSONAL[CARGO]` | 16.98 | 815.85 | 239.15 | 72.17 | 15002 |

Ambos visuales pertenecen al grupo `20644d3047b208148676`.

## Reorganizacion del panel

Para dar cabida a los nuevos segmentadores sin ampliar el panel lateral ni
invadir el area principal, se ajusto la distribucion vertical de los
segmentadores existentes. La secuencia final queda:

1. Ano
2. Mes
3. Tipo de Contrato
4. Grupo Empresa
5. Nombre Empresa
6. Tipo de Cargo
7. Dependencia
8. Area
9. Cargo

Geometria final de los segmentadores de cierre del panel:

| Segmentador | Visual ID | X | Y | W | H |
|---|---|---:|---:|---:|---:|
| Tipo de Cargo | `479a1c96957f434bd013` | 17.94 | 572.16 | 240.03 | 73.31 |
| Dependencia | `a58d5b2e9f6c4a21b103` | 17.94 | 654.17 | 240.03 | 72.13 |
| Area | `a93404e0eabc48bb9e8e` | 18.38 | 734.99 | 239.15 | 72.17 |
| Cargo | `83a053e3e767d88dd07a` | 16.98 | 815.85 | 239.15 | 72.17 |

## Interacciones y pruebas

Validaciones funcionales esperadas y revisadas en Power BI Desktop:

- Sin filtros: la pagina conserva su linea base visual y los segmentadores
  muestran valores disponibles.
- Dependencia: al seleccionar una dependencia, Area y Cargo se reducen al
  contexto disponible.
- Area: al seleccionar un area dentro del contexto, Cargo se reduce a cargos
  pertenecientes a esa area.
- Cargo: permite seleccionar uno o varios cargos y actualiza los visuales de
  datos de la pagina.
- Seleccionar todo: disponible en Area y Cargo para restaurar el contexto del
  slicer.
- Busqueda: disponible en los desplegables de Area y Cargo.
- Limpieza: al limpiar filtros, los resultados vuelven al contexto general.

Las formas, fondos, textos decorativos y navegacion no requieren interacciones
de filtrado.

## Validaciones tecnicas

- `powerbi-report-author doctor`.
- `powerbi-report-author --version`.
- `powerbi-desktop --version`.
- Parseo JSON de `page.json` y de los nuevos `visual.json`.
- Auditoria semantica local con `alertas_altas: 0`.
- Auditoria de navegacion sin alertas criticas.
- `git diff --check` focalizado sobre el alcance.
- Verificacion de UTF-8 sin BOM en archivos versionados.

La validacion global de PBIR presenta advertencias y errores historicos en
otras paginas del reporte; esos hallazgos no pertenecen a este cambio y quedan
fuera del staging.

## Archivos versionados

- Visuales nuevos de Area y Cargo.
- Reubicacion focalizada de los segmentadores del panel izquierdo necesarios
  para evitar superposiciones.
- Esta Spec.
- Nota breve en `Docs/PROJECT_CONTEXT.md`.
- Entrada en `Docs/CHANGELOG.md`.

## Exclusiones

No se incluyen:

- cambios de modelo semantico;
- relaciones;
- medidas DAX;
- Power Query;
- otras paginas;
- bookmarks;
- `Outputs/`;
- `Data/`;
- cambios PBIP concurrentes o ruido de Power BI Desktop no relacionado.
