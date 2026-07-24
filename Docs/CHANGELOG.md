# Registro de Cambios

Este archivo registra los cambios significativos del proyecto ordenados cronologicamente (mas reciente primero).

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

---

## [Sin version] - 2026-07-24

### Agregado

- `PBIP/00_Referencia_Historica/`: carpeta con versiones historicas del reporte en formato `.pbix` (previas a la migracion a PBIP) y un tema de color (`PaletaAzulProfesional.json`). Documentada en `ESTRUCTURA_PROYECTO.md`. Solo el tema JSON se versiona; los 5 archivos `.pbix` quedan excluidos via `.gitignore` por tratarse de binarios no necesarios para reproducir `Proyecto7.pbip` y por sensibilidad de datos sin verificar (ver `SECURITY_AND_PRIVACY.md`).

### Corregido

- Pagina `Productividad`: la tabla `cba349945ec4b0577321` conserva los importes completos, sin abreviaturas, cuando el contexto corresponde a unidades de negocio diferentes de Challenger.
- Challenger, la vista consolidada y la seleccion de todos los grupos mantienen la presentacion monetaria en millones con una cifra decimal.
- El ajuste usa medidas numericas de presentacion en `Tbl_Medidas`; las expresiones base continuan siendo las sumas de `Gasto Personal` y `Ventas (MM)`, sin cambios en calculos, filtros ni logica de productividad.
- Las etiquetas y totales de la tabla comparten las mismas medidas y cadenas de formato dinamicas. Los graficos conservan sus medidas porcentuales y su comportamiento de unidades.
- Validaciones: escenarios 2025 y 2026 para Challenger, Grupo Sky, Habitel Hotels, Lemco y Fundacion Challenger; parseo JSON/PBIR, auditorias DAX y semantica, UTF-8 sin BOM y revision selectiva del diff Git.

## [Sin version] - 2026-07-21

### Corregido

- Pagina `Gasto Laboral`: se ajustaron las unidades visuales de `Presupuesto Gasto Personal` y `Gasto Personal` en el grafico `Gasto Labora (Ppto vs Ejecucion)` y la tabla mensual para evitar que negocios con valores menores frente a Challenger se mostraran como `$0,0 mill.`.
- Causa identificada: `labelDisplayUnits` estaba forzado a millones (`1000000D`) en las etiquetas/valores monetarios, con precision reducida.
- Solucion aplicada: las unidades de visualizacion quedaron sin escala forzada (`1D`) en las series/columnas monetarias, conservando calculos, medidas, colores, filtros, navegacion y diseno.
- Archivos PBIP modificados: `visuals/b351f0de695056ac18a5/visual.json` y `visuals/ced924c91be19c603ad0/visual.json` dentro de la pagina `2ee3ca8f42b01e9a6840`.
- Validaciones ejecutadas: parseo JSON de ambos visuales, revision de campos usados, revision de diff y `git diff --check`.

## [Sin version] - 2026-07-17

### Agregado

- `Docs/PROJECT_STATUS.md` para consolidar estado operativo, bloqueos vigentes y pendientes del proyecto.
- `Docs/GIT_GOVERNANCE.md` para documentar reglas de staging selectivo, commit y push.
- `Docs/TROUBLESHOOTING.md` para documentar diagnóstico y validación de Formula Firewall, rutas SharePoint y ruido PBIP.

### Modificado

- `README.md`, `AGENTS.md` y `CLAUDE.md` actualizados al estado real del proyecto `Proyecto7.pbip`.
- `Docs/README.md` actualizado como índice oficial de documentación.
- `Docs/PROJECT_CONTEXT.md`, `Docs/ARCHITECTURE.md`, `Docs/DATA_PIPELINE.md`, `Docs/RUNBOOK.md` y `Docs/SECURITY_AND_PRIVACY.md` alineados con Git activo, migración de fuentes a SharePoint corporativo y bloqueo vigente de Formula Firewall.

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

> **Nota:** Este proyecto cuenta con control de versiones Git. Los cambios PBIP deben manejarse con staging selectivo por alcance; no usar `git add .`. El push requiere aprobacion explicita.
