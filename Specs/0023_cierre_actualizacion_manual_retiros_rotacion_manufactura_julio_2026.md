# 0023 - Cierre de actualización manual de Retiros y Rotación Manufactura (julio 2026)

## Objetivo

Actualizar manualmente el corte de julio de 2026 en
`Reports/Recurring/01_Retiros_y_Rotacion_Manufactura/Current/Retiros_y_Rotacion_Manufactura.xlsx`
preservando estructura y formato, y dejar documentada la lógica utilizada de
forma reproducible para una eventual automatización futura (no autorizada
todavía).

## Alcance

- Actualización puntual de un único corte mensual (julio 2026).
- No se modificó `PBIP/`, el modelo semántico, medidas ni visuales.
- Claude no modificó `Consolidado 2025.xlsx` ni `PptovsReal.xlsx` como parte
  de este cierre documental. `PptovsReal.xlsx` sí fue actualizado, pero por el
  usuario, de forma manual y directamente en el archivo fuente, para
  completar `Dependencia`/`Área` en la hoja `RETIROS` (ver sección
  "Homologación").
- No se creó notebook (`.ipynb`) ni script (`.py`) de automatización.

## Fuentes utilizadas

### Colaboradores

- Archivo: `Data/HeadCount/2025/Consolidado 2025.xlsx`, hoja `Consolidado2025`.
- Filtro: `AÑO = 2026`, `MES = 07.Julio`.
- Agrupación: conteo de filas por `DEPENDENCIA` + `AREA`.
- Validación: la misma lógica de conteo reprodujo **exactamente** los valores
  ya existentes en el reporte para 9 de 10 áreas de Dirección de Manufactura y
  3 de 4 áreas de Gerencia Cadena Muebles Laminados en enero-junio 2026 (una
  diferencia de 1 colaborador en abril entre `MUEBLES LAMINADOS` y
  `PROTOTIPOS`, sin afectar el subtotal del grupo).

### Retiros

- Archivo: `Data/HeadCount/PptovsReal.xlsx`, hoja `RETIROS`.
- Filtro: `Año = 2026`, `Mes = 07.Julio`.
- Agrupación: conteo de filas por `Dependencia` + `Área`, aplicando la regla
  de exclusión validada (ver siguiente sección).
- El modelo semántico de Power BI (`PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl`,
  `Planta Ppto.tmdl`) confirma que esta hoja —no `Consolidado 2025.xlsx`— es
  la fuente real de `Retiros` en el modelo.

## Regla validada de Retiros

Un registro de `RETIROS` cuenta como retiro válido si **no** cumple ninguna
de estas condiciones de exclusión:

- `Cargo = APRENDIZ SENA`
- `Cargo = PRACTICANTE`
- `Detalle` contiene `REINGRESO`
- `Detalle` contiene `FALLECIMIENTO`
- `Detalle = PENSION POR JUBILACION`
- `Detalle = CESION DE CONTRATO`
- `Detalle = CESION CONTRATO`

Esta regla ya estaba documentada y aprobada en
`Specs/0014_diagnostico_brechas_homologacion_retiros.md` y
`Specs/0016_renombramiento_medidas_rotacion_retiros.md`; no se definió de
nuevo en esta iniciativa, se reutilizó y se validó contra el corte de julio.

## Homologación de Dependencia y Área para julio 2026

Al momento del diagnóstico inicial, las 126 filas de julio 2026 en `RETIROS`
tenían `Dependencia` y `Área` vacías en todo el archivo (no solo en
Manufactura/Muebles Laminados), lo que impedía calcular Retiros por área para
ese corte.

El usuario actualizó manualmente `PptovsReal.xlsx`, completando esos campos
directamente en el archivo fuente. Esa modificación no fue realizada por
Claude ni forma parte de este cierre documental; el procedimiento reportado
por el usuario fue:

1. Cruce por `CARGO_CCO` (`BUSCARX`) contra `Consolidado 2025.xlsx`, filtrado
   primero a julio 2026 y, si no había coincidencia, a junio 2026.
2. Para los casos sin cruce en ninguno de los dos meses, una **regla manual
   por prefijo del código de centro de costo** dentro de `CARGO_CCO`:
   - `P1` → Dirección de Manufactura / Metalmecánica (Gasodomésticos)
   - `P2` → Gerencia Cadena Muebles Laminados / Muebles Laminados
   - `P3` → Dirección de Manufactura / Refrigeración
   - `P4` → Dirección de Manufactura / Electrónica
   - `P6` → Gerencia Cadena Muebles Laminados / Prototipos

**Esta regla de prefijo se usó exclusivamente para completar el corte de
julio 2026 y no queda aprobada como regla automática permanente.** Debe
revalidarse explícitamente antes de incorporarse a cualquier automatización
futura (ver `DATA-014`).

### Trazabilidad verificada (sin PII)

Se reconstruyó objetivamente, por coincidencia de `CARGO_CCO` contra
`Consolidado 2025.xlsx` (julio 2026), qué método originó cada uno de los 20
retiros válidos de `REFRIGERACIÓN` en julio (el área con el valor más alto y,
por tanto, la más señalada para verificación):

| Origen | Cantidad |
|---|---:|
| Cruce `BUSCARX` exitoso contra julio 2026 (Dependencia/Área devuelta consistente) | 19 |
| Cruce `BUSCARX` exitoso contra junio 2026 | 0 |
| Sin cruce en julio ni junio → regla manual por prefijo (`P3`) | 1 |

Las celdas `Dependencia`/`Área` de `RETIROS` ya estaban guardadas como
valores fijos (no fórmulas vivas) al momento de esta verificación, por lo que
la trazabilidad se reconstruyó por coincidencia de clave, no leyendo fórmulas
en la celda.

## Reconciliación enero-junio 2026 (validación de la regla)

Aplicando la regla de exclusión de Retiros y la agrupación por
Dependencia+Área sobre `RETIROS`, se comparó el recálculo contra los valores
ya existentes en el reporte para las 14 áreas × 6 meses (84 celdas):

- 13 de 14 áreas coincidieron exactamente en los 6 meses.
- Única discrepancia: `MANTENIMIENTO REFRIGERACIÓN`, junio 2026 — el reporte
  registra 0, el recálculo con la regla aprobada da 1 (un retiro válido que
  no cae en ninguna exclusión documentada). Ver "Hallazgo histórico fuera de
  alcance".

## Resultado final julio 2026

| Dependencia | Colaboradores | Retiros |
|---|---:|---:|
| Dirección de Manufactura (10 áreas) | 720 | 36 |
| Gerencia Cadena Muebles Laminados (4 áreas) | 150 | 5 |
| **Total conjunto** | **870** | **41** |

Detalle por área (Colaboradores / Retiros), julio 2026:

- Refrigeración: 333 / 20
- Metalmecánica (Gasodomésticos): 209 / 9
- Electrónica: 80 / 7
- Taller de Herramientas: 43 / 0
- Mantenimiento Refrigeración: 14 / 0
- Mantenimiento Metalmecánica: 13 / 0
- Ingeniería de Planta Metalmecánica: 9 / 0
- Dirección de Manufactura (área): 8 / 0
- Ingeniería de Planta Refrigeración: 10 / 0
- Ingeniería de Planta Electrónica: 1 / 0
- Muebles Laminados: 118 / 4
- Prototipos: 21 / 1
- Mantenimiento Muebles: 6 / 0
- Ingeniería de Planta Muebles Laminados: 5 / 0

## Cambios aplicados al archivo

Archivo: `Reports/Recurring/01_Retiros_y_Rotacion_Manufactura/Current/Retiros_y_Rotacion_Manufactura.xlsx`
(no versionado en Git; excluido por `.gitignore`).

Hoja `Retiros (2026)`:

- Columna `H` (Colaboradores, julio) y columna `U` (Retiros, julio): valores
  fijos escritos en las filas 5-14 (Dirección de Manufactura, 10 áreas) y
  16-19 (Gerencia Cadena Muebles Laminados, 4 áreas).
- Fórmulas de subtotal agregadas, siguiendo el mismo patrón `SUM` ya usado en
  las columnas C-G y O-T de las mismas filas:
  - `H4 = =SUM(H5:H14)`, `U4 = =SUM(U5:U14)` (subtotal Dirección de
    Manufactura).
  - `H15 = =SUM(H16:H19)`, `U15 = =SUM(U16:U19)` (subtotal Gerencia Cadena
    Muebles Laminados).
- No se modificaron fórmulas existentes: `N` (promedio), `AA` (total anual),
  `AB:AM` (% retiros mensual) y `AN:AO` (indicadores anuales) ya estaban
  pre-construidas para los 12 meses y recalculan automáticamente al abrir el
  archivo en Excel (`fullCalcOnLoad = True`).
- Hoja `Retiros (2025)` y columnas enero-junio de `Retiros (2026)`: sin
  cambios **al momento de este cierre de julio**. Este estado fue temporal:
  ver "Corrección histórica posterior — agosto 26 de 2026" para el estado
  vigente de enero-junio.

Se creó y luego se eliminó (tras validación funcional del usuario) un
respaldo temporal previo a la escritura:
`Retiros_y_Rotacion_Manufactura_backup_2026-08-26_pre-julio.xlsx`.

## Hallazgo histórico fuera de alcance (al cierre de julio)

`MANTENIMIENTO REFRIGERACIÓN`, junio 2026: el reporte tenía 0 retiros; la
regla de exclusión aprobada, aplicada sobre `RETIROS`, producía 1. En este
cierre de julio no se corrigió porque estaba fuera de alcance y porque
corregir un periodo histórico requería autorización y validación
independientes.

**Estado vigente**: esta discrepancia quedó resuelta el 26 de agosto de 2026
(ver "Corrección histórica posterior — agosto 26 de 2026"). Esta sección se
conserva sin reescribir para preservar el registro de lo que se sabía y se
decidió en el momento del cierre de julio.

## Validaciones ejecutadas

- Reapertura del archivo `.xlsx` actualizado sin errores; integridad del ZIP
  confirmada.
- Verificación de que `Retiros (2025)` no cambió (spot-check de 6 celdas).
- Verificación de que enero-junio de `Retiros (2026)` no cambió (spot-check
  de 6 celdas, incluida la discrepancia histórica de junio, intacta **en ese
  momento** — corregida posteriormente, ver sección de corrección histórica).
- Verificación de dimensiones de hoja y celdas combinadas sin cambios
  (`A1:AO19` / `A1:AO38`, 0 merges en ambas hojas, antes y después).
- Comparación de formato (formato numérico, fuente, borde, relleno) entre
  cada celda nueva y su celda hermana del mismo mes/fila: idéntico.
- Recalculo en Python de los subtotales tras guardar el archivo: 720/36
  (Manufactura), 150/5 (Muebles Laminados), 870/41 (total) — coincide con lo
  solicitado.
- Validación visual y funcional del archivo abierto en Excel por el usuario:
  **PASS**.

## Automatización futura — diferida

Se considera conveniente automatizar esta actualización mensual, pero se
difiere porque existen otros frentes prioritarios del PBIP en curso. Se
registra como iniciativa independiente `DATA-014` en
`Specs/00_roadmap_y_backlog.md`, sección "Ideas por evaluar", sin autorización
de implementación.

Cuando se retome, deberá incluir al menos:

- Preflight de fuentes (`Consolidado 2025.xlsx`, `PptovsReal.xlsx`).
- Selección parametrizada de año/mes.
- Validación de columnas esperadas antes de procesar.
- Homologación gobernada de Dependencia/Área (decidir si la regla de prefijo
  se formaliza, se reemplaza o se elimina).
- Aplicación de las exclusiones de Retiros ya documentadas.
- Conciliación contra el periodo anterior antes de escribir.
- Backup temporal antes de escribir y eliminación controlada tras validación.
- Escritura puntual con `openpyxl` (u equivalente) preservando formato y
  fórmulas existentes.
- Reapertura y validación de totales tras guardar.
- Copia opcional a `History/YYYY/` según el procedimiento del `README.md` del
  reporte.
- No modificar los archivos fuente ni versionar datos `.xlsx`.

## Riesgos y pendientes

- La regla de prefijo (`P1`/`P2`/`P3`/`P4`/`P6`) usada para completar julio es
  manual, específica de este corte, y no está gobernada; no debe asumirse
  válida para meses futuros sin revalidación.
- `PptovsReal.xlsx` sigue dependiendo de completitud manual de
  `Dependencia`/`Área` en la hoja `RETIROS`; no hay garantía de que meses
  futuros lleguen ya completos.
- ~~La discrepancia histórica de junio en `MANTENIMIENTO REFRIGERACIÓN` sigue
  sin resolver (fuera de alcance).~~ Resuelta el 26 de agosto de 2026 (ver
  "Corrección histórica posterior").
- Los 9 retiros válidos identificados en la corrección histórica de agosto,
  en áreas de Gerencia Cadena Muebles Laminados fuera de las 4 áreas que
  rastrea este reporte (Almacén, Centro de Distribución, Constructores
  Instalación, I+D Muebles), quedan fuera del alcance funcional del reporte
  por decisión del usuario — no son un error ni un pendiente de incorporar.
- Riesgo general de Formula Firewall y migración de fuentes ya documentado en
  `CLAUDE.md` y `Docs/TROUBLESHOOTING.md` no se vio afectado por este cierre
  (no se tocó `PBIP/`).

## Archivos incluidos en este cierre documental

- `Specs/0023_cierre_actualizacion_manual_retiros_rotacion_manufactura_julio_2026.md`
  (este archivo).
- `Reports/Recurring/01_Retiros_y_Rotacion_Manufactura/README.md`.
- `Specs/00_roadmap_y_backlog.md`.

## Archivos explícitamente excluidos de este commit

- `Reports/Recurring/01_Retiros_y_Rotacion_Manufactura/Current/Retiros_y_Rotacion_Manufactura.xlsx`
  (ya actualizado localmente; excluido de Git por `.gitignore`).
- `Data/HeadCount/PptovsReal.xlsx`, `Data/HeadCount/2025/Consolidado 2025.xlsx`
  (fuentes de datos; excluidas de Git).
- Cualquier archivo `PBIP/` (no se tocó el modelo, medidas ni visuales).
- Los 254 cambios preexistentes y no relacionados detectados en la rama
  `docs/roadmap-backlog` (`Docs/`, `PBIP/`) — este cierre se aisló
  deliberadamente en un worktree nuevo desde `origin/main` para no mezclarlos.

## Estado de versionamiento

Rama de trabajo: `docs/cierre-retiros-manufactura-julio-2026`, creada desde
`origin/main` en un worktree aislado (`.wt/cierre-retiros-manufactura-julio-2026`)
para no mezclar los 254 cambios ajenos pendientes en `docs/roadmap-backlog`.

No se hizo merge a `main` en esta iniciativa; el cierre queda sujeto a
revisión (PR) antes de integrarse.

## Corrección histórica posterior — agosto 26 de 2026

### Motivo

Después del cierre de julio se completaron en `PptovsReal.xlsx` los campos
`Dependencia` y `Área` que estaban vacíos en registros de meses anteriores de
2026 (no solo en julio). Esto hizo necesario recalcular el histórico
enero-julio de las 14 áreas que forman parte de
`Retiros_y_Rotacion_Manufactura.xlsx`.

### Regla funcional confirmada

Solo se consideran las Dependencias/Áreas que ya existen en
`Retiros_y_Rotacion_Manufactura.xlsx` (las mismas 14 áreas de siempre: 10 de
Dirección de Manufactura, 4 de Gerencia Cadena Muebles Laminados). No se
agregan nuevas áreas aunque existan retiros válidos en `PptovsReal.xlsx`
correspondientes a otras subáreas.

En esta revisión se encontraron 9 retiros válidos en áreas fuera del alcance
del reporte, todas dentro de Gerencia Cadena Muebles Laminados:

- Almacén Muebles Laminados
- Centro de Distribución / Centro de Distribución Muebles
- Constructores Instalación
- I+D Muebles

Estos registros **no son errores ni quedan pendientes de incorporar**: quedan
fuera del alcance funcional de este reporte por decisión del usuario, porque
el reporte rastrea únicamente el subconjunto de áreas de manufactura de esa
dependencia, no la Gerencia Cadena Muebles Laminados completa.

### Reconciliación

- 846 registros de 2026 revisados en `RETIROS`.
- 0 registros con `Dependencia`/`Área` vacías después de la actualización del
  usuario.
- 98 combinaciones revisadas (14 áreas × 7 meses, enero-julio 2026).
- 18 diferencias históricas encontradas y corregidas.
- Enero, febrero y julio: sin diferencias.
- Diferencias concentradas en marzo-junio.
- Reconciliación posterior a la corrección: **0 diferencias residuales** en
  las 98 combinaciones.

### Correcciones aplicadas

Se modificaron únicamente **18 celdas** de `Retiros` en la hoja
`Retiros (2026)`, columnas `Q` (marzo) a `T` (junio). No se modificó
`Colaboradores`, no se modificó la hoja `Retiros (2025)`, y enero, febrero y
julio permanecieron sin cambios.

Subtotales corregidos (Actual → Recalculado):

#### Dirección de Manufactura

- Marzo: 18 → 22
- Abril: 28 → 34
- Mayo: 16 → 23
- Junio: 21 → 36

#### Gerencia Cadena Muebles Laminados

- Marzo: 4 → 5
- Abril: 5 → 8
- Mayo: 1 → 2
- Junio: 4 → 5

Caso puntual: `MANTENIMIENTO REFRIGERACIÓN` / junio 2026: **0 → 1**. La
discrepancia histórica documentada en el cierre de julio queda **resuelta**.

Se creó y luego se eliminó (tras validación funcional del usuario) un
respaldo temporal previo a esta corrección:
`Retiros_y_Rotacion_Manufactura_backup_2026-08-26_pre-correccion-historica.xlsx`.

Las fórmulas de subtotal de las columnas corregidas (`Q4:T4`, `Q15:T15`) ya
existían con el patrón `SUM` desde el diseño original del workbook; no se
modificaron, solo recalcularon al abrir el archivo con los nuevos valores de
las celdas base.

### Validación final

- Integridad del `.xlsx`: **PASS**.
- Formato y estructura (dimensiones de hoja, celdas combinadas, formato
  numérico/fuente/borde/relleno de cada celda corregida frente a sus celdas
  vecinas): preservados.
- Fórmulas existentes (`N`, `AA`, `AB:AM`, `AN:AO`, subtotales `Q4:T4` y
  `Q15:T15`): preservadas, sin modificar.
- `Colaboradores`: sin cambios (spot-check).
- Hoja `Retiros (2025)`: sin cambios (spot-check).
- Archivo abierto manualmente en Excel por el usuario: **PASS**, sin mensajes
  de reparación.
- 0 diferencias residuales frente a `PptovsReal.xlsx` para las 14 áreas del
  reporte, en los 7 meses consolidados.

### Estado de versionamiento de esta corrección

Rama de trabajo: `docs/correccion-historica-retiros-manufactura-2026`, creada
desde `origin/main` en un worktree aislado
(`.wt/correccion-historica-retiros-manufactura-2026`) para no mezclar los
cambios ajenos preexistentes en `docs/roadmap-backlog`.

No se implementó `DATA-014` como parte de esta corrección. No se hizo merge a
`main`; queda sujeto a revisión (PR) antes de integrarse.
