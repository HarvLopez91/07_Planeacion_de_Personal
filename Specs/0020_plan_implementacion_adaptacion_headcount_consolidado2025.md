# Plan de implementación — DATA-012: HeadCount / Generación en Demográfico (Promedio)

Fecha: 2026-08-10

Estado: **implementado y validado técnicamente** (sección 15). Fuente de verdad: `Specs/0019_analisis_impacto_adaptacion_headcount_consolidado2025.md` (decisiones A-F, todas aprobadas).

Rama: `fix/data-012-headcount-generacion-rango-edad`. Worktree final: `.wt/data-012-headcount-generacion-clean` (ver sección 15.1 para la razón del cambio de nombre respecto al worktree original `.wt/data-012-headcount-generacion`). Base: `origin/main` en `f9e15a7ed194b62e49ecd1435fd4b14ac350e4c5` (incluye PR #7/Unión Libre y GOV-005 ya fusionados).

## 1. Alcance

Incluido:

1. Migración permanente (commiteada) de las 3 fuentes HeadCount aprobadas (decisión F) de OneDrive personal a SharePoint corporativo.
2. Corrección de la falsa equivalencia `RANGO DE EDAD → GENERACIÓN` únicamente para 2025 (decisión A).
3. Conservación intacta de la lógica histórica 2024 (decisión B) — cero cambios de código en esa rama del Power Query.
4. Adición de `Rango de Edad` como atributo independiente en `Consolidado2025` y `PLANTA DE PERSONAL` (decisiones A/B/9).
5. Alineación de colores de "Generación por Antigüedad en la compañía" con el Manual de Marca LEMCO.

Explícitamente fuera de alcance (no se toca en esta implementación):

- GOV-005 (ya cerrada, solo se verifica que sigue íntegra).
- El archivo Excel (`Data/HeadCount/*.xlsx`), no versionado, no se modifica.
- `ÁRBOL DE NÓMINA NIVEL 2/3`, `Tipo Identificación`, `COD. CARGO`, `Tipo Contrato (Kactus)`, `Indicador Actividad`, `Año Nac` (decisión C — permanecen en la fuente, sin mapear).
- `TIPO_DE_CARGO` crudo y la columna calculada `Tipo de Cargo` (decisión D — sin cambios).
- El parche local histórico y el worktree temporal `.wt/data012-verificacion-fuente` (decisión E — no se reutilizan).
- Contratos Kactus, Retiros, Rotación2.
- Formula Firewall como corrección estructural (solo se documenta si aparece durante el refresh de este plan).
- ADR-007 (encoding HTML de `GENERACI&#211;N`) — no se renombra ni se corrige.

## 2. Consultas afectadas

| Consulta | Archivo | Cambio |
|---|---|---|
| `Consolidado2025` | `PBIP/Proyecto.SemanticModel/definition/tables/Consolidado2025.tmdl` | URL `Origen` (F) + M de Generación/Rango de Edad (A) + nueva columna TMDL |
| `PLANTA DE PERSONAL` | `PBIP/Proyecto.SemanticModel/definition/tables/PLANTA DE PERSONAL.tmdl` | URL `Origen` (F) + nueva columna TMDL `Rango de Edad` (sin cambios de M, ver sección 4.3) |
| `AREAS` | `PBIP/Proyecto.SemanticModel/definition/tables/AREAS.tmdl` | Solo URL `Origen` (F) |

## 3. Columnas afectadas

| Columna | Tabla(s) | Cambio |
|---|---|---|
| `GENERACIÓN` (TMDL, `sourceColumn: GENERACIÓN`) | `Consolidado2025` | Sin cambio de TMDL — su fuente M pasa de ser el renombrado de `RANGO DE EDAD` a ser el renombrado de la columna real `Generación` |
| `Rango de Edad` (nueva) | `Consolidado2025` | Nueva columna, `sourceColumn: RANGO DE EDAD`, nuevo `lineageTag`, no oculta |
| `Rango de Edad` (nueva) | `PLANTA DE PERSONAL` | Nueva columna, `sourceColumn: RANGO DE EDAD`, nuevo `lineageTag`, no oculta — llega nula para 2024 vía `Table.Combine` (2024 no aporta esa columna) |
| `GENERACI&#211;N` | `PLANTA DE PERSONAL` | Sin cambios — mismo `lineageTag`, misma relación con `Generaciones[Generación]`; se beneficia indirectamente del fix en `Consolidado2025` |

Ninguna de las otras 18 columnas genuinamente nuevas del parche histórico (`Specs/0019` sección 2.1) se incorpora — ver `Specs/0019` sección 9.2/9.6.

## 4. Cambios exactos de código (verificados contra el TMDL y el Excel real, no supuestos)

### 4.1 URLs (decisión F, GATE 6)

En los 3 archivos, sustituir textualmente:

```
https://lemcosas-my.sharepoint.com/personal/edwin_clavijo_challenger_co/Documents/Documentos/Anal%C3%ADtica%20del%20Grupo%20Empresarial%20Lemco/03_Fuentes_Datos/01_Talento_Humano/02_HeadCount/2025/Consolidado%202025.xlsx
```
→
```
https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/Documentos%20compartidos/5.%20People%20analytics/07_Planeaci%C3%B3n_de_Personal/Data/HeadCount/2025/Consolidado%202025.xlsx
```

Y (2024, en `PLANTA DE PERSONAL.tmdl` y `AREAS.tmdl`):

```
https://lemcosas-my.sharepoint.com/personal/edwin_clavijo_challenger_co/Documents/Documentos/Anal%C3%ADtica%20del%20Grupo%20Empresarial%20Lemco/03_Fuentes_Datos/01_Talento_Humano/02_HeadCount/2024/Consolidado%202024.xlsx
```
→
```
https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/Documentos%20compartidos/5.%20People%20analytics/07_Planeaci%C3%B3n_de_Personal/Data/HeadCount/2024/Consolidado%202024.xlsx
```

### 4.2 `Consolidado2025.tmdl` — M query (decisión A, GATE 7)

Encabezados reales confirmados en `Data/HeadCount/2025/Consolidado 2025.xlsx` hoja `Consolidado2025` (verificado byte a byte, sin asumir mayúsculas/minúsculas):

- Columna 38 = `Generación` (UTF-8 correcto: `Generaci\xc3\xb3n`).
- Columna 39 = `RANGO DE EDAD`.

M actual (partición `Consolidado2025`):

```
#"Columnas con nombre cambiado" = Table.RenameColumns(#"Encabezados promovidos",{{"RANGO DE EDAD", "GENERACIÓN"}}),
#"Tipo cambiado1" = Table.TransformColumnTypes(#"Columnas con nombre cambiado",{{"MES", type text}, {"NIVEL_DE_CARGO", type text}, {"TIPO_DE_CARGO", type text}})
```

M nuevo:

```
#"Columnas con nombre cambiado" = Table.RenameColumns(#"Encabezados promovidos",{{"Generación", "GENERACIÓN"}}),
#"Tipo cambiado1" = Table.TransformColumnTypes(#"Columnas con nombre cambiado",{{"MES", type text}, {"NIVEL_DE_CARGO", type text}, {"TIPO_DE_CARGO", type text}, {"GENERACIÓN", type text}, {"RANGO DE EDAD", type text}})
```

Efecto: `GENERACIÓN` queda alimentada por la columna real `Generación` (no por `RANGO DE EDAD`); `RANGO DE EDAD` queda intacta con su nombre original, lista para exponerse como `Rango de Edad` en TMDL. No se crea `Generación 2`. Ambas quedan tipadas como texto.

### 4.3 `PLANTA DE PERSONAL.tmdl` — M query (decisión B, GATE 8)

**Cero cambios de código.** Verificado en el M actual:

- La línea `Table.RenameColumns(#"Tipo cambiado",{{"RANGO DE EDAD", "GENERACIÓN"}, {"OBSERVACION", "NIVEL_DE_CARGO"}}, MissingField.Ignore)` (2024) se conserva intacta.
- `#"Consulta anexada" = Table.Combine({#"Tipo cambiado1", Consolidado2025})` combina por nombre de columna; `Table.Combine` rellena con `null` las columnas que un lado no tiene. Como el lado 2024 ya no tiene `RANGO DE EDAD` (se renombró en su propia rama), y el lado 2025 (`Consolidado2025`, tras 4.2) sí, el resultado combinado deja `RANGO DE EDAD` nula para 2024 y poblada para 2025 — automáticamente, sin lógica adicional.
- El paso posterior `Table.RenameColumns(#"Consulta anexada",{{"GENERACIÓN", "GENERACI&#211;N"}})` y el `Table.ReplaceValue(...,"Millenials","Millennials",...,{"GENERACI&#211;N"})` se aplican **después** del combine, por lo que benefician automáticamente a los datos 2025 ya corregidos, sin duplicar la normalización (ya existe, confirmado — no se repite, ver GATE 8).

### 4.4 TMDL — nuevas columnas (GATE 9)

`Consolidado2025.tmdl`, agregar junto a la columna `GENERACIÓN` existente:

```
	column 'Rango de Edad'
		dataType: string
		lineageTag: <nuevo-GUID>
		summarizeBy: none
		sourceColumn: RANGO DE EDAD

		annotation SummarizationSetBy = Automatic
```

`PLANTA DE PERSONAL.tmdl`, agregar junto a `'Rango Antigüedad'` (mismo estilo: no oculta):

```
	column 'Rango de Edad'
		dataType: string
		lineageTag: <nuevo-GUID-distinto>
		summarizeBy: none
		sourceColumn: RANGO DE EDAD

		annotation SummarizationSetBy = Automatic
```

No se toca `column GENERACI&#211;N` (línea 128 de `PLANTA DE PERSONAL.tmdl`, `lineageTag: 01cc54fd-bc1b-441d-8c2b-75142a180df5`) ni su relación con `Generaciones[Generación]` (`lineageTag: 4508a53f-a2a8-4817-8576-a639f1306cd7`).

### 4.5 Etiquetas canónicas de Generación (GATE 8, verificado)

`Generaciones[Generación]` contiene exactamente 4 valores (decodificado del M embebido): `Baby Boomers`, `Generación X`, `Millennials` (tras su propia corrección interna `Millenials→Millennials`), `Centennials`. `PLANTA DE PERSONAL` normaliza el mismo typo (`Millenials→Millennials`) en su propio M, post-combine (sección 4.3) — ya coinciden, no se duplica la corrección.

## 5. Visuales afectados (auditoría previa confirmada, GATE 10)

Los 3 visuales de `Demográfico (Promedio)` (página `ReportSectionf46593dd92bf9359ceef`) usan referencias conceptualmente correctas — **no se cambian campos**:

| Visual | ID | Campos | Cambio |
|---|---|---|---|
| Funnel Generación | `b07ca4a549be0e60b2c6` | `PLANTA DE PERSONAL[GENERACIÓN]`, `Tbl_Medidas[Tot_empleados_Promedio]` | Ninguno |
| Tabla Generacional | `30f11733eea2697476d4` | `Generaciones[Generación]`, `Generaciones[Rango Años de Nacimiento]`, `Generaciones[Edades]`, medidas | Ninguno |
| Generación por Antigüedad | `f87ec4295cc979e1a3b0` | Category: `PLANTA DE PERSONAL[Rango Antigüedad]`; Series: `PLANTA DE PERSONAL[GENERACIÓN]` | Solo colores (sección 6) |

Estas 3 visuales hoy no muestran datos correctos porque su **fuente** (`GENERACIÓN`) está mal poblada — el fix de la sección 4.2 corrige el dato, no el visual.

## 6. Colores — Manual de Marca LEMCO (GATE 11)

Único archivo a tocar: `PBIP/Proyecto.Report/definition/pages/ReportSectionf46593dd92bf9359ceef/visuals/f87ec4295cc979e1a3b0/visual.json`, bloque `objects.dataPoint` (5 entradas, verificadas):

| Entrada | Selector actual | Color actual | Color nuevo |
|---|---|---|---|
| 1 (default, sin selector) | — | `#F7931E` | `#0B1C35` (reservado para una 5ª categoría real futura) |
| 2 | `GENERACIÓN = 'Baby Boomers'` | `#1A3059` | `#000032` |
| 3 | `GENERACIÓN = 'Generación X'` | `#F7931E` | `#1A3059` |
| 4 | `GENERACIÓN = 'Centennials'` | `#B3B3B3` (fuera de marca) | `#F7931E` |
| 5 | `GENERACIÓN = 'Millennials'` | `#00A5E2` (fuera de marca) | `#1B487F` |

No se toca `objects.totals[0].backgroundColor` (`#F7931E`, ya de marca, no es color de serie generacional). No se toca el funnel Generación (`#F7931E`, ya de marca). No se toca el encabezado de la tabla generacional (`#1B487F`, ya de marca).

## 7. Pasos de implementación

1. Editar las 3 URLs (sección 4.1).
2. Editar el M de `Consolidado2025.tmdl` (sección 4.2).
3. Agregar columna `Rango de Edad` en `Consolidado2025.tmdl` y `PLANTA DE PERSONAL.tmdl` (sección 4.4).
4. Editar colores en `f87ec4295cc979e1a3b0/visual.json` (sección 6).
5. Validación estática (sección 8).
6. Abrir `Proyecto7.pbip` desde este worktree, validar estructura, ejecutar refresh (sección 9).
7. Validaciones de datos vía MCP/DAX (sección 10).
8. Validación visual manual — detenerse para aprobación del usuario (sección 11).
9. Tras aprobación: cerrar Desktop, clasificar churn, actualizar documentación, commits, push.

## 8. Validaciones estáticas (antes de abrir Desktop)

- `git diff` completo revisado línea por línea.
- `git diff --check` (sin conflictos residuales ni espacios en blanco corruptos).
- Sintaxis TMDL: indentación con tabs preservada; bloques `column`/`partition` bien formados.
- Sintaxis M: paréntesis/llaves balanceados en los `let...in` editados.
- 0 ocurrencias de `lemcosas-my.sharepoint.com/personal` en las 3 consultas tras el cambio.
- `Generación` y `Rango de Edad` quedan como atributos independientes en el M de `Consolidado2025`.
- 0 cambios de código en la rama 2024 de `PLANTA DE PERSONAL.tmdl` (diff exclusivo a: URL, y las líneas nuevas de columna `Rango de Edad`).
- `lineageTag` de `GENERACI&#211;N` (`01cc54fd-...`) y de la relación con `Generaciones` (`4508a53f-...`) sin cambios.
- La corrección de Unión Libre (`EST_CIVIL (grupos)`, `lineageTag: b7226dd5-5031-4aa4-a301-ef77c36bc9f1`) permanece intacta — 0 diff en ese bloque.
- 0 medidas nuevas o renombradas en `Tbl_Medidas.tmdl` (GOV-005 no debe reaparecer con duplicados).
- Solo se modifica `visual.json` de `f87ec4295cc979e1a3b0` — 0 diff en los otros 2 visuales ni en ningún otro visual del reporte.

## 9. Power BI / refresh

Abrir `PBIP/Proyecto7.pbip` desde `.wt/data-012-headcount-generacion`. Confirmar antes del refresh: apertura sin `PFE_TM_OBJECT_NAME_ALREADY_EXISTS`, 52 tablas, 66 relaciones, 122 medidas, 0 duplicadas (mismo patrón verificado en la validación de PR #7).

Ejecutar refresh sobre las 3 consultas migradas (y las que dependan de ellas). Si aparece una solicitud de credenciales, autenticación o nivel de privacidad: detenerse, no cambiar configuración automáticamente, indicar al usuario exactamente qué seleccionar.

Tras el refresh, confirmar: `Consolidado2025` Ready, `PLANTA DE PERSONAL` Ready, `AREAS` Ready; `NIVEL_DE_CARGO`, `TIPO_DE_CARGO`, `Generación`/`GENERACIÓN`, `Rango de Edad` presentes.

## 10. Validaciones de datos (MCP/DAX, solo lectura, sin PII)

1. `DISTINCT(PLANTA DE PERSONAL[GENERACIÓN])` — debe contener solo categorías generacionales reales; 0 valores que empiecen con "Entre" o "Mayor de".
2. `DISTINCT(PLANTA DE PERSONAL[Rango de Edad])` — debe contener los intervalos de edad de 2025 (`Entre 18-29 Años`, etc.) para las filas 2025; nulo para 2024.
3. Confirmar que la relación `PLANTA DE PERSONAL[GENERACI&#211;N] → Generaciones[Generación]` vuelve a resolver (sin filas huérfanas para las 4 categorías).
4. Confirmar que el total de colaboradores (`Tbl_Medidas[Tot_empleados_Promedio]` o conteo base) no cambia como efecto de separar Generación de Rango de Edad — comparar antes/después del refresh.

## 11. Validación visual manual (el usuario debe aprobar antes de continuar)

En `Demográfico (Promedio)`, botón `Generación`, con las 3 visualizaciones visibles simultáneamente:

- Funnel Generación: categorías generacionales reales.
- Tabla Generacional: filas de `Generación`/`Año Nacimiento`/`Edades` no vacías.
- Generación por Antigüedad: eje = antigüedad, leyenda = generaciones reales, colores LEMCO (sección 6).
- Ninguna de las tres muestra rangos de edad como si fueran generación.

No se continúa (cierre, documentación, commits) sin la aprobación explícita del usuario sobre esta validación.

## 12. Criterios de aceptación

Los de `Specs/0019` sección 12, más:

- Colores de "Generación por Antigüedad" coinciden exactamente con la tabla de la sección 6 de este plan.
- `git diff` final contra `main` no incluye ninguna de las 18 columnas del parche histórico fuera de alcance (sección 3).
- DATA-005 se cierra como absorbida solo si la migración de `AREAS` (sección 4.1) quedó incluida y verificada.

## 13. Rollback

- Mientras no haya push: `git checkout -- .` en el worktree, o descartar el worktree sin commitear.
- Tras push sin merge: la rama `fix/data-012-headcount-generacion-rango-edad` puede eliminarse o corregirse con nuevos commits; `main` no se ve afectado porque no hay merge.
- Si el refresh en Desktop falla de forma no recuperable: cerrar sin guardar, revertir los archivos del worktree a su estado pre-refresh (`git checkout -- .`), documentar el bloqueo en `Specs/0019`/este plan sin marcar DATA-012 como Finalizada.
- No existe rollback sobre el Excel ni sobre la biblioteca SharePoint corporativa — este plan no los modifica.

## 14. Control de archivos modificados (esperado al cierre)

- `PBIP/Proyecto.SemanticModel/definition/tables/Consolidado2025.tmdl`
- `PBIP/Proyecto.SemanticModel/definition/tables/PLANTA DE PERSONAL.tmdl`
- `PBIP/Proyecto.SemanticModel/definition/tables/AREAS.tmdl`
- `PBIP/Proyecto.Report/definition/pages/ReportSectionf46593dd92bf9359ceef/visuals/f87ec4295cc979e1a3b0/visual.json`
- `Specs/0019_analisis_impacto_adaptacion_headcount_consolidado2025.md` (cierre)
- `Specs/0020_plan_implementacion_adaptacion_headcount_consolidado2025.md` (este archivo, cierre)
- `Specs/00_roadmap_y_backlog.md` (DATA-012 Finalizada, DATA-005 absorbida confirmada)
- `Docs/CHANGELOG.md`

Cualquier otro archivo modificado por Power BI Desktop durante la sesión (bookmarks, `diagramLayout.json`, otras tablas) se clasifica como churn no intencional y se descarta antes del commit (GATE 16), salvo que se determine que es un efecto necesario y se documente explícitamente por qué se conserva.

## 15. Resultado de la implementación y validación (ejecutado)

### 15.1 Reconciliación con cambios manuales del working tree principal — descartados en su totalidad

Durante la implementación, el usuario realizó ajustes manuales en el **working tree principal** (`C:\...\07_Planeación_de_Personal\PBIP`, rama `docs/roadmap-backlog`) sobre tres frentes distintos: (a) la tabla/funnel de Generación, (b) la tabla `Planta Ppto` (frente operativo independiente, no relacionado con DATA-012), y (c) exploración adicional no especificada. Se auditó ese working tree en modo **solo lectura** y se determinó, con evidencia de diff línea por línea, que los cambios manuales de Generación/funnel **no eran una corrección limpia**: reintroducían la regresión de codificación de Unión Libre (`"UniÃ³n Libre"`), duplicaban en línea la lógica de `Consolidado2025` dentro de `PLANTA DE PERSONAL` (el defecto ya documentado en `Specs/0019` sección 2.2), y una cascada de renombrado (`GENERACI&#211;N` → `'RANGO DE EDAD'`, mismo `lineageTag`) que rompió el visual "Generación por Antigüedad" (que nunca había tenido ese problema).

**Decisión:** no se portó ningún cambio del working tree principal al worktree de DATA-012. El working tree principal —incluidos los cambios de `Planta Ppto`— se dejó completamente intacto, sin `git checkout`, sin `reset`, sin copiar archivos. La implementación de DATA-012 se completó exclusivamente con la solución propia ya validada (bookmark corregido con referencias mínimas a `Tbl_Medidas`, sección 4.4/9.8 de `Specs/0019`), no con ninguna pieza del working tree principal.

### 15.2 Contaminación del worktree de DATA-012 durante el refresh — causa raíz y corrección

Independientemente del punto 15.1, el propio worktree de DATA-012 mostró el mismo patrón de contaminación (columnas del parche histórico reapareciendo: `ÁRBOL DE NÓMINA NIVEL 2/3`, `NOMBRE`, `APELLIDO`, etc.) después de ejecutar "Actualizar todo". Investigación:

- **Causa raíz confirmada:** el M de `Consolidado2025` nunca restringía explícitamente las columnas de salida — `Table.PromoteHeaders` expone las 68 columnas reales del Excel restructurado, y solo un subconjunto tenía columna TMDL declarada. Al ejecutar un refresh completo, Power BI Desktop detecta las columnas del query no mapeadas en el TMDL y las **auto-agrega** al modelo, reintroduciendo exactamente las columnas que las decisiones C/D (`Specs/0019`) dicen que deben permanecer solo en la fuente.
- **No fue un problema de caché de ruta de worktree** (hipótesis inicial descartada): se comprobó abriendo un worktree nuevo (`.wt/data-012-headcount-generacion-clean`, sección 15.1 encabezado) que el problema persistía igual tras un refresh completo, aunque no tras solo abrir/parcial-refrescar.
- **Corrección aplicada:** se agregó un paso explícito `Table.RemoveColumns(#"Tipo cambiado1", {lista de 18 columnas fuera de alcance}, MissingField.Ignore)` al final del M de `Consolidado2025`, antes del `in`. Esto impide que Desktop vuelva a auto-agregarlas en cualquier refresh futuro, sin depender de que el TMDL simplemente "no las mencione". Verificado con dos refrescos completos posteriores: 0 reaparición de las 18 columnas.
- El worktree original (`.wt/data-012-headcount-generacion`) quedó con un commit inicial (`7a55d71`, los 4 commits documentales cherry-pickeados) pero **detached** de la rama (se liberó la rama para poder recrearla limpia en `.wt/data-012-headcount-generacion-clean`, que es el worktree final usado para todo el trabajo de código y el commit/push). El worktree original permanece en disco, sin usar, no se eliminó (no se solicitó su limpieza en esta tarea).

### 15.3 Resultado de las validaciones técnicas (todas PASS)

Ejecutadas vía `powerbi-modeling-mcp` sobre el modelo en vivo, tras refresh completo ejecutado manualmente por el usuario (el servidor MCP permaneció en modo solo lectura durante toda la sesión):

- **Estructura:** 52 tablas, 66 relaciones, 122 medidas, 122 nombres únicos (0 duplicadas). `PLANTA DE PERSONAL` 71.206 filas, `Consolidado2025` 45.670 filas — coinciden exactamente con el diálogo de Power BI Desktop.
- **`PLANTA DE PERSONAL[GENERACIÓN]` (excluyendo el valor `"false"` de la sección 15.4):** únicamente `Millennials`, `Centennials`, `Generación X`, `Baby Boomers` — 0 valores tipo "Entre X-Y Años".
- **`EXCEPT` bidireccional** entre `PLANTA DE PERSONAL[GENERACIÓN]` (válido) y `Generaciones[Generación]`: 0 diferencias en ambas direcciones.
- **Tabla generacional:** devuelve las 4 generaciones reales con `Rango Años de Nacimiento`, `Edades` y medidas pobladas, más 1 fila en blanco correspondiente a la deuda de calidad de datos (sección 15.4) — no filas vacías masivas como el bug original.
- **Funnel Generación (orden real, no solo el `sortDefinition` del JSON):** confirmado con `ORDER BY [Empleados] DESC` sobre el modelo cargado — `Millennials` (3333.75) > `Centennials` (1429.33) > `Generación X` (1133.33) > `Baby Boomers` (33.9).
- **Bookmark `98c9f8d36c940a908787` ("Generación"):** 0 referencias a `RANGO DE EDAD` como sustituto de `GENERACIÓN`; las 16 referencias corregidas a medidas apuntan a `Tbl_Medidas`, no a `PLANTA DE PERSONAL`.
- **"Generación por Antigüedad" (`f87ec4295cc979e1a3b0`):** Category = `Rango Antigüedad`, Series = `GENERACIÓN` (nunca `RANGO DE EDAD`); colores exactos: Baby Boomers `#000032`, Generación X `#1A3059`, Millennials `#1B487F`, Centennials `#F7931E`; sin `#B3B3B3` ni `#00A5E2`.
- **Unión Libre:** `lineageTag: b7226dd5-5031-4aa4-a301-ef77c36bc9f1` sin cambios; 0 diff en el bloque `EST_CIVIL (grupos)`.
- **Sin duplicación inline de `Consolidado2025`** en `PLANTA DE PERSONAL` (sigue referenciada como consulta vía `Table.Combine`); **sin columna `Generación` paralela** innecesaria; relación `GENERACI&#211;N → Generaciones[Generación]` conserva su `lineageTag` (`4508a53f-...`) sin cambios.
- **Churn tras cerrar Desktop:** 0 — el diff final coincide exactamente con los 5 archivos y líneas intencionales (URLs migradas ×3, columna `Rango de Edad` ×2, `Table.RemoveColumns` ×1, colores ×5, bookmark ×16).

**PASS técnico determinado por Claude Code**, sin solicitar aprobación funcional del usuario, conforme a la instrucción explícita de la sesión.

### 15.4 Deuda de calidad de datos de la fuente (fuera de alcance de DATA-012)

Durante la validación se detectaron errores de refresco (`DataFormat.Error: Valor de celda '#N/A' no válido`) en `Consolidado2025`/`PLANTA DE PERSONAL`. El conteo exacto reportado por Power BI Desktop **varió entre distintas ejecuciones de "Actualizar todo"**: se observaron al menos 295 errores en una ejecución temprana, 36 en una ejecución intermedia, y **67 errores en la evidencia más reciente aportada por el usuario** (ambas consultas, `Consolidado2025` y `PLANTA DE PERSONAL`, con 45.670 y 71.206 filas cargadas respectivamente — coincidentes en todas las ejecuciones). Esta variabilidad es atribuible al estado de cálculo de las fórmulas del Excel vivo en SharePoint (recalculo asíncrono de BUSCARV/XLOOKUP entre aperturas), no a un defecto determinístico del código de DATA-012 ni a un patrón nuevo introducido por esta iniciativa. El perfilado de solo lectura contra el Excel (`Data/HeadCount/2025/Consolidado 2025.xlsx`) realizado durante la investigación coincidió exactamente con el total de 295 reportado por Power BI Desktop en esa ejecución específica, confirmando que en todos los casos el origen es el mismo patrón de valores `#N/A` preexistentes de la fuente, con el siguiente desglose máximo observado por columna:

| Columna | Filas con `#N/A` de origen | ¿En alcance DATA-012? |
|---|---|---|
| `DEPENDENCIA_PATRON` | hasta 226 | No |
| `AREA_PATRON` | hasta 88 | No |
| `FECHA NACIMIENTO` | hasta 42 | No |
| `EDAD` | hasta 42 | No |
| `Generación` | hasta 42 | **Sí** |
| `RANGO DE EDAD` | hasta 42 | **Sí** |
| `EST_CIVIL` | hasta 32 | No |
| `AGRUPADOR` | hasta 4 | No |

**Causa confirmada:** valores de error nativos de Excel (`#N/A`, típicamente resultado de una fórmula BUSCARV/XLOOKUP sin coincidencia) presentes en la fuente, para un subconjunto pequeño de empleados (los mismos ~42 en `Generación`/`RANGO DE EDAD`/`FECHA NACIMIENTO`/`EDAD`, sugiriendo un único dato faltante — probablemente fecha de nacimiento — del que se derivan los demás por fórmula). **6 de las 8 columnas afectadas nunca son tocadas por el M de DATA-012**, lo que prueba que el problema es de la fuente, no del código de esta iniciativa.

**Síntoma observado en el modelo cargado:** para las filas afectadas de `GENERACIÓN`, el motor de Analysis Services no deja la celda en blanco sino que sustituye el texto literal `"false"` (comportamiento del motor al no poder convertir un valor de error de Excel al tipo declarado `string`) — visualmente esto se resuelve como un grupo separado sin coincidencia en `Generaciones` (fila en blanco en la tabla generacional, excluido del funnel), no como una generación real incorrecta.

**Decisión de alcance (confirmada por el usuario):** DATA-012 **no** corrige estos errores de origen. No se aplicó `ReplaceErrorValues`, `try...otherwise`, eliminación de filas, ni conversión general a texto. Las 45.670/71.206 filas se preservan íntegras. El saneamiento de estos `#N/A` queda como **deuda de calidad de datos**, registrada en el roadmap, para una iniciativa futura de limpieza de fuente — no bloquea el cierre técnico de DATA-012 porque **todas las filas con información válida** (99,9 % en `Generación`/`Rango de Edad`) quedan correctamente configuradas.

### 15.5 Fuera de alcance — no tocado por DATA-012

- `Ppto Retiros`: 38 errores de refresco preexistentes, ajenos a DATA-012 — no diagnosticados ni corregidos.
- Formula Firewall / niveles de privacidad en otras consultas (`Selección Grupo Lemco`, `SENA UNIDADES`, etc.): riesgo ya documentado en `Specs/0019` sección 11, sin cambios.
- `Planta Ppto` y cualquier otro ajuste manual del working tree principal (sección 15.1): explícitamente preservados sin tocar, fuera del alcance de esta rama.

### 15.6 Control de archivos modificados (real, reemplaza la lista "esperada" de la sección 14)

Únicamente estos 5 archivos de código/reporte, más las actualizaciones de documentación de este cierre:

- `PBIP/Proyecto.SemanticModel/definition/tables/Consolidado2025.tmdl`
- `PBIP/Proyecto.SemanticModel/definition/tables/PLANTA DE PERSONAL.tmdl`
- `PBIP/Proyecto.SemanticModel/definition/tables/AREAS.tmdl`
- `PBIP/Proyecto.Report/definition/pages/ReportSectionf46593dd92bf9359ceef/visuals/f87ec4295cc979e1a3b0/visual.json`
- `PBIP/Proyecto.Report/definition/bookmarks/98c9f8d36c940a908787.bookmark.json` (no estaba en la lista original de la sección 14; fue necesario para corregir las referencias obsoletas de medidas que impedían el orden correcto del funnel — ver `Specs/0019` sección 9.8 y GATE 14 de esta sesión)
- `Specs/0019_analisis_impacto_adaptacion_headcount_consolidado2025.md`
- `Specs/0020_plan_implementacion_adaptacion_headcount_consolidado2025.md` (este archivo)
- `Specs/00_roadmap_y_backlog.md`
- `Docs/CHANGELOG.md`

0 churn adicional (bookmarks ajenos, `diagramLayout.json`, otras tablas) en el commit final.

### 15.7 Corrección post-merge de presentación — ocultar blancos en Demográfico (Promedio)

Después del merge del PR #8 se confirmó un gap de presentación en la página `Demográfico (Promedio)` (`ReportSectionf46593dd92bf9359ceef`): Power BI podía volver a mostrar el miembro `(En blanco)` al aplicar el bookmark `Generación`, aunque los filtros correctos ya existieran en los archivos base de los visuales.

La corrección se limita a filtros de visual y estado persistido del bookmark; no elimina filas ni modifica Power Query, TMDL, relaciones, medidas DAX o archivos Excel:

- Se conserva sin duplicar `PLANTA DE PERSONAL[GENERACIÓN] != null` en el funnel `b07ca4a549be0e60b2c6`, junto con su orden descendente por `Tbl_Medidas[Tot_empleados_Promedio]`.
- Se conserva sin duplicar `Generaciones[Generación] != null` en la tabla `30f11733eea2697476d4`.
- Se amplía el filtro del funnel Estado Civil `1da9f64d870519b6bffa` para excluir conjuntamente `"Sin Información En Kactus"` y `null`; el rótulo visual `(En blanco)` no se trata como texto literal.
- En el bookmark `98c9f8d36c940a908787` (`Generación`) se persisten el filtro `Generaciones[Generación] != null` de la tabla y la exclusión de `null` en Estado Civil, porque este bookmark no usa `suppressData` y puede restaurar el estado de datos de los visuales objetivo.
- El bookmark `9470280b116096d60ab0` (`Estado Civil`) y el bookmark Hijos `092fbe75ecb89d30748c` conservan `suppressData: true`; se auditaron y no requieren cambios para mantener los filtros.
- La deuda `DATA-013` (`#N/A`, `false` y demás valores de origen) permanece fuera de alcance y sin cambios.

Archivos PBIR modificados por esta corrección:

- `PBIP/Proyecto.Report/definition/pages/ReportSectionf46593dd92bf9359ceef/visuals/1da9f64d870519b6bffa/visual.json`
- `PBIP/Proyecto.Report/definition/bookmarks/98c9f8d36c940a908787.bookmark.json`

Los visuales `b07ca4a549be0e60b2c6` y `30f11733eea2697476d4` se validan como parte del resultado, pero no se reescriben porque `origin/main` ya contiene sus predicados correctos.

Validación ejecutada el 2026-08-11 desde `.wt/demografico-ocultar-blancos`:

- Power BI Desktop abrió el PBIP aislado y mostró datos en la página objetivo.
- Flujo `Estado Civil → Hijos → Generación → Estado Civil → Generación`: PASS en capturas consecutivas.
- Estado Civil: sin `(En blanco)` y sin `Sin Información En Kactus`; `Unión Libre` visible y correcta.
- Generación: sin `(En blanco)`, orden descendente preservado y tabla poblada con las cuatro generaciones, año de nacimiento y edades.
- El valor `false` asociado a DATA-013 permaneció sin saneamiento, conforme al alcance aprobado.
- `powerbi-report-author validate` conservó exactamente la línea base preexistente de `origin/main` (74 errores y 157 advertencias ajenos a esta corrección), sin aumento tras el parche.
- Las capturas se conservaron únicamente como evidencia local ignorada en `Outputs/`; no forman parte del commit.
