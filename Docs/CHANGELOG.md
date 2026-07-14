# Registro de Cambios

Este archivo registra los cambios significativos del proyecto ordenados cronologicamente (mas reciente primero).

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

---

## [Sin version] - 2026-07-14

### Agregado

- Matriz de antiguedad al retiro en la pagina Retiros, con filas por `Ppto Retiros[Rango_Antiguedad_Retiro]`, columnas por `Anos[Ano]` y valores de `Tbl_Medidas[Tot_Retiros]`.
- Columnas tecnicas en `Ppto Retiros` para calcular antiguedad al retiro desde `Fecha Inicio` y `Fecha Vencimiento`: `Meses_Antiguedad_Retiro`, `Rango_Antiguedad_Retiro` y `Orden_Rango_Antiguedad_Retiro`.

### Modificado

- La clasificacion de antiguedad al retiro deja de usar `Meses de permanencia` como base funcional y pasa a calcularse desde las fechas reales del retiro.

## [Sin version] — 2026-07-03

### Agregado

- `Docs/ESTRUCTURA_PROYECTO.md`: estandar corporativo de carpetas, politica de archivos `.md`, nomenclatura de `Outputs/` (`NN_AAAA-MM-DD_descripcion_corta.md`) y criterio de actualizacion documental por tipo de cambio (commits `0cb85bf`, `936bfa8`, `5ffdb24`).
- `CLAUDE.md` versionado por primera vez, alineado con la estructura real del proyecto (commit `cd300b7`).
- Indice de `Docs/README.md` actualizado para incluir `ESTRUCTURA_PROYECTO.md`.

### Corregido

- `Docs/ARCHITECTURE.md` y `Docs/RUNBOOK.md`: referencias a `Proyecto.pbip` actualizadas a `Proyecto7.pbip` (archivo renombrado el 2026-06-17, commit `cfb3a15`).
- `Docs/BI_GUIDELINES.md`: inventario de paginas corregido de 21 a 19 (2 paginas de propuesta/rediseno ya no existen en el proyecto), pagina activa por defecto corregida a `Demografico (Promedio)`, conteo de bookmarks reverificado en 19 (no 20).
- `Docs/SECURITY_AND_PRIVACY.md`: agregada `Inputs/` como carpeta de riesgo pendiente de evaluar por datos personales.

## [Sin version] — 2026-06-17

### Modificado

- Renombrado el archivo principal del proyecto de `Proyecto.pbip` a `Proyecto7.pbip` (commit `cfb3a15`).
- Separado el rango de antiguedad demografico en dos categorias (commit `e8bb853`).

### Agregado

- Rotacion voluntaria por tipo de retiro en la pagina Retiros (commit `be55a2a`).

## [Trabajo en curso] - 2026-06-11

### Agregado

- Nueva pagina `Demografico (Promedio) - Rediseno LEMCO` (`ReportSectiond3m0c0rp20260611`) como propuesta visual adicional basada en un shell de HTML Content y visuales nativos de Power BI.
- Nueva medida `HTML Demografico Promedio Shell` en `Tbl_Medidas`, dentro de la carpeta `11 HTML Content`.
- Inventario tecnico de reorganizacion de medidas en `Outputs/documentation/inventario_medidas_reorganizadas_2026-06-11.csv`.

### Modificado

- Centralizacion de 88 medidas en `Tbl_Medidas`, organizadas por carpetas de visualizacion segun dominio funcional.
- Actualizacion de referencias de medidas en culturas, visuales y bookmarks para apuntar a la tabla contenedora `Tbl_Medidas`.
- Actualizacion del inventario de paginas y del catalogo de metricas.

### Validado

- Parseo correcto de 434 archivos JSON del reporte.
- 275 proyecciones de medidas revisadas en visuales/bookmarks sin referencias simples heredadas a tablas anteriores.
- 88 medidas declaradas unicamente en `Tbl_Medidas`, sin duplicados de nombre.

## [Sin version] — Estado actual al 2026-06-11

Estado del proyecto al momento del primer analisis tecnico documentado.

### Identificado como presente

- 19 paginas de reporte (10 visibles, 5 ocultas, 1 portada, 1 actualizacion, 1 QA, 1 demografico promedio)
- 53 tablas en el modelo semantico
- 41 relaciones explicitas
- Datos historicos desde 2024 hasta mayo 2026 (carpeta `Data/2026/05_Mayo/`)
- Consolidacion de HeadCount 2024 + 2025 via `Table.Combine` en `PLANTA DE PERSONAL`
- Tabla `DimPeriodoYM` calculada para soporte de logica de trimestres dinamicos
- Medidas de eficiencia de gasto laboral vs ventas
- Indicadores SST con indices de frecuencia y severidad
- Bookmarks para navegacion en SST y demografico

---

## Como usar este registro

Al realizar cambios en el proyecto, agregar una nueva entrada con el siguiente formato:

```markdown
## [vX.Y.Z o descripcion] — YYYY-MM-DD

### Agregado
- Nueva tabla / pagina / medida

### Modificado
- Descripcion del cambio y razon

### Corregido
- Bug corregido y descripcion del problema

### Eliminado
- Elemento eliminado y razon
```

> **Nota:** Este proyecto no tiene control de versiones Git activo. Se recomienda inicializar un repositorio Git para complementar este registro con un historial de commits. Ver [SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md) para consideraciones de privacidad antes de hacer el repositorio publico.
