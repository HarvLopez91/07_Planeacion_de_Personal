# 0032 — Plan de implementación: Productividad, presupuesto vs ejecutado de gasto y ventas

**Iniciativa:** PBIP-009
**Análisis de impacto previo:** [`0031`](0031_analisis_impacto_productividad_presupuesto_ejecutado_gasto_ventas.md)
**Fecha:** 2026-09-10
**Estado:** implementado y validado — Fases 0 a 5 cerradas con PASS funcional y visual en Power BI Desktop el 2026-09-11; Fase 6 (versionamiento e integración a `main`) en ejecución

---

## 1. Objetivo

Incorporar en la tabla principal de la página `Productividad` el presupuesto y el
ejecutado de Gasto de Personal y de Ventas, con su diferencia absoluta y su
variación porcentual, sin alterar la semántica de los indicadores vigentes.

**Alcance físico:** un visual y una tabla de medidas.

| Objeto | Ruta |
|---|---|
| Página | `ReportSection65569958420c423d90b1` — `Productividad` |
| Visual | `.../visuals/cba349945ec4b0577321/visual.json` |
| Medidas | `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl` |

**Fuera de alcance:** `PptovsReal.xlsx`, las fuentes Excel de Gasto Laboral,
`Planta Ppto` como consulta M, las relaciones del modelo, otras páginas y el
tema global.

### Layout objetivo

```
Mes | Ppto. Gasto | Gasto Real | Dif. Gasto | Var. Gasto %
    | Ppto. Ventas | Ventas Real | Dif. Ventas | Var. Ventas %
    | %Efiprom | Productividad
```

### Indicadores cuya semántica se preserva sin cambios

`Prod_Gasto_Personal_Tabla` · `Prod_Ingreso_Operacional_Tabla` ·
`Prod_Efic_Tabla` · `Efic` · `%Efiprom` · `KPI_EFI` · `Var_GL` · `Cump_GL`

---

## 2. Advertencia de gobierno: el orden se alteró

`0031` concluye que **la implementación no debía comenzar** hasta cerrar el gate
de unidad monetaria y la fila canónica de `Ppto/Real`. La implementación de las
Fases 1 y 2 se ejecutó antes de ese cierre.

Consecuencias que este plan asume de forma explícita:

1. ~~Las medidas construidas no aplican conversión monetaria gobernada.~~ **Resuelto
   el 2026-09-10** con la capa `Prod_*_MM` (`0031` §3.6). Redacción original: suman
   los importes tal como están almacenados y delegan la escala al formato
   (`Prod_Usar_Millones`). Es exactamente el riesgo que `0031` §3.4 y §7.1
   señalan: **la vista consolidada multi-grupo no es confiable** hasta gobernar
   la unidad.
2. La fila canónica sí quedó resuelta: las seis medidas filtran
   `KEEPFILTERS('Planta Ppto'[Ppto/Real] = "Real")`, conforme a `0031` §3.3 y a
   la reconciliación de §3.5.

**Ninguna fase se declara cerrada por haberse ejecutado; se declara cerrada por
tener evidencia.** Fase 4 y Fase 5 son las que gobiernan la aceptación.

---

## 3. Fases

### Fase 0 — Recuperación y saneamiento del estado parcial

**Estado: CERRADA** · evidencia: auditoría de solo lectura del 2026-09-10.

| Verificación | Resultado |
|---|---|
| Worktree y rama | `.wt/pbip-009-productividad` sobre `feat/pbip-009-productividad-presupuesto-ejecutado` |
| HEAD | `3bc4f45`, idéntico a `origin/main`; **0 commits propios** |
| Staging | vacío; sin archivos sin versionar; `git diff --check` limpio |
| Archivos con contenido modificado | **2** |

Cambios reales:

```
M  .../visuals/cba349945ec4b0577321/visual.json      +552 / -16
M  .../definition/tables/Tbl_Medidas.tmdl            +106 / -0
```

**Los cuatro TMDL colaterales no son cambios.** `Dim_Area.tmdl`,
`Dim_Dependencia.tmdl`, `Dim_Estructura_Organizacional.tmdl` y
`PBIP008 Selector Indicador.tmdl` figuran como modificados en `git status`, pero
`git diff --name-status` no los lista y su contenido es idéntico tras normalizar
saltos de línea. El delta de tamaño coincide exactamente con el número de líneas
de cada archivo (+51 sobre 52 líneas en `Dim_Area.tmdl`; +19 sobre 20 en
`PBIP008 Selector Indicador.tmdl`): es reescritura LF → CRLF, compatible con la
firma de Power BI Modeling MCP.

**Acción:** excluirlos del commit. No requieren reversión ni corrección.

---

### Fase 1 — Medidas y reglas de datos

**Estado: CERRADA** · evidencia: simulación sobre el dato real del 2026-09-11 (`0031` §3.8) y auditoría estática del TMDL.

Seis medidas creadas en `Tbl_Medidas.tmdl`, carpeta `05 Productividad\PBIP-009`.
La nomenclatura sigue el patrón `Prod_*` ya vigente en la página, no los nombres
genéricos del requerimiento:

| Requerimiento | Medida implementada |
|---|---|
| Presupuesto Gasto Personal | `Prod_Ppto_Gasto_Personal_Tabla` |
| Presupuesto Ventas | `Prod_Ppto_Ventas_Tabla` |
| Diferencia Gasto | `Prod_Diferencia_Gasto_Tabla` |
| Variación Gasto % | `Prod_Variacion_Gasto_Pct` |
| Diferencia Ventas | `Prod_Diferencia_Ventas_Tabla` |
| Variación Ventas % | `Prod_Variacion_Ventas_Pct` |

Reglas verificadas sobre el DAX:

| Regla | Cumple |
|---|:--:|
| Diferencia = ejecutado − presupuesto | Sí |
| Variación = `DIVIDE(Diferencia, Presupuesto)` | Sí |
| Falta ejecutado o presupuesto → `BLANK` | Sí |
| Presupuesto = 0 → variación `BLANK` | Sí |
| Ejecutado 0 con presupuesto → diferencia `−presupuesto`, variación −100 % | Sí, por construcción |
| Nunca suma porcentajes | Sí — recalcula desde importes agregados |
| Total recalculado desde agregados | Sí |
| Preserva Año, Mes, Grupo Empresa y Empresa | Sí — `KEEPFILTERS` solo sobre `Ppto/Real` |

Las cuatro dependencias (`Prod_Usar_Millones`, `Prod_Gasto_Personal_Tabla`,
`Prod_Ingreso_Operacional_Tabla`, `Prod_Efic_Tabla`) **ya existían**: no se
modificaron. **Cero bindings rotos.**

**Deuda declarada:** sin conversión monetaria gobernada (§2.1).

---

### Fase 2 — Modificación de la tabla Productividad

**Estado: CERRADA.** Once columnas en el orden objetivo; presentación completada en Fase 3.

El visual `cba349945ec4b0577321` (`tableEx`) pasa de 4 a 11 columnas, en el
orden objetivo exacto. **Ninguna proyección preexistente fue eliminada** y las
diez medidas referenciadas resuelven contra el modelo. JSON válido, CRLF, sin BOM.

Pendiente de esta fase: revisar si el ancho total de las 11 columnas cabe en los
1.024 px del visual sin scroll horizontal, o si procede ajustar el ancho del
visual dentro del lienzo sin desplazar otros objetos de la página.

---

### Fase 3 — Presentación y formato gerencial

**Estado: CERRADA** · PASS visual humano el 2026-09-11.

Aplicado: nombres gerenciales en las once columnas, anchos al 95,9 % del ancho
disponible (982 px de 1.024), encabezado a dos líneas, semáforos de círculo en las
dos variaciones con polaridad inversa y **unidad visual única `$ X.XXX mill.`**
tras la normalización de `0031` §3.6.

Las flechas direccionales se descartaron: no renderizaron de forma confiable y
`ColoredArrowDownGreen` / `ColoredArrowUpRed` no pertenecen a ningún juego estándar
de Power BI. Se usa la familia de círculos, que sí renderizó.

Situación previa: solo 3 de 11 columnas tienen formato condicional —las tres
preexistentes— y 4 tienen ancho definido. Las siete columnas nuevas están sin
formato semántico. La paleta ya está sembrada en el visual
(`#2E7D32` favorable, `#A15C00` intermedio, `#B42318` desfavorable, sobre
`#1A3059` / `#24384B` / `#F3F6F8`).

Requisitos:

1. **Polaridad invertida entre dominios.** Es el punto crítico de esta fase:
   - **Gasto**: ejecutado **por debajo** del presupuesto = favorable.
   - **Ventas**: ejecutado **por encima** del presupuesto = favorable.

   Aplicar la misma escala de color a ambos comunicaría lo contrario en la mitad
   de la tabla.

2. Porcentajes con **una decimal**; importes legibles y alineados a la derecha.
3. Encabezados cortos y explícitos; jerarquía visual que agrupe visualmente el
   bloque de gasto y el de ventas.
4. Uso moderado de color e iconos nativos. Sin saturación.
5. Evitar scroll horizontal si es razonablemente posible.

**Tolerancia de visualización.** Si se emplea un umbral de ±5 % para escalonar el
color, debe documentarse **como tolerancia de presentación, no como meta
corporativa**. No existe evidencia de que ±5 % sea un KPI oficial del Grupo.

**Nota de linaje.** Conviene que la tabla o su tooltip declare que el presupuesto
de gasto de personal no tiene origen demostrado (`0031` §3.5).

---

### Fase 3 bis — Ratios Gasto/Ventas normalizados y coherencia de página

**Estado: CERRADA** · PASS humano el 2026-09-11. Decisión humana aprobada el
2026-09-10, posterior al cierre de la normalización de importes.

1. Creadas `Prod_Ratio_Gasto_Ventas_Ppto` y `Prod_Ratio_Gasto_Ventas_Real` sobre
   la capa MM, con `BLANK` ante denominador ausente o cero y formato porcentual
   de una decimal. Detalle en `0031` §3.7.
2. Reconectados los cuatro visuales visibles de la página que representan el
   concepto Gasto/Ventas: la tabla `cba349945ec4b0577321`, la tarjeta
   `9bcb53c0b346ba0d28c4` y los dos combos `76fbb82301d3f6b571c3` y
   `d6010674e3a075647581`. Solo cambió la medida referenciada; nombres mostrados,
   anchos, formato, iconos, posición y títulos quedaron intactos.
3. `Efic`, `%Efiprom`, `KPI_EFI`, `Var_GL` y `Cump_GL` verificadas byte a byte
   contra `HEAD`: sin cambios.
4. Validación sobre el dato real: consolidado «Todos» de enero 2026 en
   13.734 / 12.114 / 90.375 / 90.377 MM, ratios 15,2 % y 13,4 %, identidad
   consolidado = suma de grupos exacta y no aditividad de porcentajes confirmada.

Dos defectos anteriores de esta implementación —indentación TMDL huérfana y
comparación Text vs Integer en `Prod_Factor_MM`— quedaron corregidos, y se añadió
una auditoría específica de ambos patrones que esta fase supera sin hallazgos.

---

### Fase 3 ter — Período comparable y formato de brechas

**Estado: CERRADA** · PASS humano el 2026-09-11.
Decisión humana aprobada el 2026-09-11. Detalle y cifras en `0031` §3.8.

1. Formato fijo `$ #,0 "mill."` en `Prod_Diferencia_Gasto_Tabla` y
   `Prod_Diferencia_Ventas_Tabla`; se retira el `formatStringDefinition` basado en
   `Prod_Usar_Millones`. DAX sin cambios.
2. Tres medidas ocultas de corte: `Prod_Mes_Corte_Gasto`, `Prod_Mes_Corte_Ventas`
   y `Prod_Mes_Corte_Ratio`, calculadas por Grupo Empresa × Año.
3. Las cuatro bases `_Tabla` aplican el corte de su métrica cuando hay varios
   meses en contexto y devuelven su valor normal con un solo mes. Brechas y
   variaciones lo heredan.
4. Los dos ratios aplican la ventana común `Prod_Mes_Corte_Ratio` sobre la capa MM.
5. La capa MM y las medidas históricas quedan intactas.

---

### Fase 4 — Pruebas funcionales y regresión

**Estado: CERRADA.** Los escenarios se evaluaron el 2026-09-11 reproduciendo la
semántica DAX sobre una copia de solo lectura de `PptovsReal.xlsx` (`0031` §3.8)
y se confirmaron en el motor durante el PASS de la Fase 5.

Controles de referencia verificados manualmente por el usuario para
**Habitel Hotels, julio 2026** (aproximados; **no se codifican en ninguna parte**):

| Magnitud | Referencia |
|---|---:|
| Ppto. Gasto Personal | ≈ 1.944,6 MM |
| Gasto Personal | ≈ 1.857 MM |
| Ppto. Ventas | ≈ 7.391 MM |
| Ventas reales | ≈ 5.933 MM |
| %Efiprom | ≈ 26,3 % |
| Productividad | ≈ 31,3 % |
| Dif. Gasto | ≈ −87,6 MM |
| Var. Gasto | ≈ −4,5 % |
| Dif. Ventas | ≈ −1.458 MM |
| Var. Ventas | ≈ −19,7 % |

Escenarios mínimos:

| # | Escenario | Qué debe comprobar |
|---|---|---|
| 1 | Julio 2026, Habitel Hotels | Reproduce los controles de referencia |
| 2 | Varios meses de 2026 | Totales recalculados, no sumas de porcentajes |
| 3 | Challenger | Comportamiento con escala de pesos completos |
| 4 | Otro grupo empresarial | Sin regresión |
| 5 | Empresa individual | Filtro empresa propaga correctamente |
| 6 | `Habitel Prime` / `Habitel Select` | Importes en blanco por consolidación (`0031` §3.5) |
| 7 | Consolidado multi-grupo | Consolidado = suma de grupos en importes (`0031` §3.6) |
| 8 | Mes futuro sin ejecutado | Diferencia y variación en `BLANK`, no en cero |
| 9 | Presupuesto cero, si existe | Diferencia válida; variación `BLANK` |
| 10 | Sin filtro de negocio | Sin doble conteo de los cinco presupuestos duplicados |
| 11 | Año completo o varios meses con meses futuros | Presupuesto y real limitados al período comparable; sin falsa brecha (`0031` §3.8) |

Regresión obligatoria: `Efic`, `%Efiprom`, `KPI_EFI`, `Var_GL`, `Cump_GL` y el
resto de visuales de la página deben conservar sus valores.

**La validez JSON, TMDL y DAX no constituye evidencia de esta fase.**

---

### Fase 5 — PASS visual end to end en Power BI Desktop

**Estado: CERRADA — PASS humano funcional y visual el 2026-09-11.** En Power BI
Desktop, los totales de enero a junio de 2026 para «Todos», Challenger y Habitel
Hotels coinciden exactamente con la simulación de `0031` §3.8: por ejemplo,
«Todos» muestra 82.509 / 80.933 / −1.576 MM (−1,9 %) en gasto, 634.855 /
589.187 / −45.667 MM (−7,2 %) en ventas y ratios de 13,0 % y 13,7 %.

Cadena a validar: fuente → `Planta Ppto` → DAX → filtros → visual →
presentación → regresión.

Aprobación manual sobre: cifras, totales, formatos, colores, iconos, ancho de
columnas, legibilidad, alineación, ausencia de solapamientos, comportamiento de
los filtros y equilibrio visual de la página completa.

---

### Fase 6 — Versionamiento

**Estado: EN EJECUCIÓN** · autorizada por el usuario el 2026-09-11.

Alcance previsto del commit:

```
M  .../visuals/cba349945ec4b0577321/visual.json
M  .../visuals/9bcb53c0b346ba0d28c4/visual.json
M  .../visuals/76fbb82301d3f6b571c3/visual.json
M  .../visuals/d6010674e3a075647581/visual.json
M  .../definition/tables/Tbl_Medidas.tmdl
```

Los cuatro TMDL con solo cambio de fin de línea se restauran a `HEAD` tras
verificar que su contenido normalizado es idéntico (autorizado 2026-09-11) y no
entran en el commit. Staging por rutas explícitas, sin `git add .` ni
`git add -A`. Push, PR y merge autorizados el 2026-09-11, sin force push ni
rebase.

---

## 4. Riesgos vigentes

| # | Riesgo | Severidad | Mitigación |
|---|---|---|---|
| R1 | Escala monetaria de 2027+ sin evidencia | Media | Mitigado 2024-2026 con la capa MM por Grupo × Año (`0031` §3.6). Para 2027+ la capa devuelve `BLANK` en lugar de adivinar; hay que validar la escala antes de cargar ese ejercicio o gobernar la unidad en el contrato de datos |
| R2 | `Ppto Gasto Personal` sin linaje demostrado | Media | Declararlo en la página; no automatizar la carga |
| R4 | `Habitel Prime` / `Select` sin importes propios | Baja | El dato viene vacío y se muestra `BLANK`; falta decidir cómo comunicarlo (§6, dependencia 3) |
| R6 | Truncamiento a millones desde marzo 2026 | Baja | Comparar con tolerancia, nunca por igualdad estricta |
| R9 | Huecos legítimos de presupuesto dentro de meses ejecutados: Lemco jul-2026 sin Ppto Gasto; Lemco 2024 sin Ppto Ventas | Media | Cuantificados en `0031` §3.8. Completar la fuente o ampliar la regla a emparejamiento por celda; requiere decisión humana |
| R10 | Ventas de 2025 ausentes en presupuesto y real desde jul/ago en cuatro grupos | Baja | Hueco simétrico de la fuente, sin falsa brecha; los ratios usan la ventana común. Completar la fuente |
| R11 | La tarjeta KPI (`KPI_EFI`, `Var_GL`) y el subtítulo del acumulado no adoptan el período comparable | Media | Dependen de medidas históricas compartidas, fuera de alcance; pueden no coincidir con la tabla en vistas anuales |

Retirados: R5 (ancho de columnas) y R7 (gasto «sin outsourcing») por obsoletos;
R3 (polaridad de color) y R8 (cambio de base de filas de los visuales no
tabulares) quedan resueltos por el PASS humano del 2026-09-11.

Los errores generales de refresh observados en otras consultas del modelo **no
se atribuyen a PBIP-009**: su causa no se diagnosticó, y esta iniciativa no
modificó consultas, particiones, fuentes ni relaciones.

---

## 5. Criterios de aceptación

1. Las once columnas se muestran en el orden objetivo, sin scroll horizontal
   dentro del ancho disponible.
2. Los diez controles de Habitel julio 2026 se reproducen dentro de tolerancia.
3. Diferencias y variaciones respetan las reglas de `BLANK`, cero y −100 %.
4. Los totales se recalculan desde importes agregados.
5. `Efic`, `%Efiprom`, `KPI_EFI`, `Var_GL` y `Cump_GL` no cambian de
   definición ni de valor en el resto del modelo. En la página
   Productividad los ratios Gasto/Ventas pasan a leerse de
   `Prod_Ratio_Gasto_Ventas_Ppto` y `Prod_Ratio_Gasto_Ventas_Real`
   (`0031` §3.7).
6. Ningún otro visual de la página presenta regresión.
7. La polaridad de color es correcta e inversa entre gasto y ventas.
8. Las limitaciones conocidas (R1, R2, R4, R9, R10, R11) están declaradas para el usuario.
9. El usuario otorga PASS visual manual en Power BI Desktop.

Ninguna fase se marca cerrada sin evidencia verificable.

---

## 6. Dependencias abiertas

Del gate de `0031` §12, siguen sin resolver y condicionan el cierre:

1. ~~Unidad monetaria canónica y regla de conversión.~~ **Cerrada el 2026-09-10**: MM COP, normalizando por Grupo × Año antes de agregar. Queda pendiente gobernar la unidad en el contrato de datos para ejercicios futuros.
2. Aceptación de publicar `Ppto Gasto Personal` sin linaje demostrado.
3. Forma de comunicar la consolidación de Prime y Select.
4. ~~Elección entre gasto «sin outsourcing» y gasto total de la Unidad Hotelera.~~ **Cerrada el 2026-09-10**: se conserva el gasto «sin outsourcing» de `PptovsReal.xlsx`, sin modificar la definición vigente de `Gasto Personal`.

---

## 7. Cierre (2026-09-11)

PBIP-009 quedó implementado y validado con PASS funcional y visual del usuario en
Power BI Desktop. Lo entregado:

1. **Normalización monetaria a MM COP por Grupo Empresa × Año**, aplicada antes de
   agregar (`0031` §3.6). El consolidado «Todos» equivale a la suma de los cinco
   grupos.
2. **Presupuesto vs ejecutado de gasto de personal y ventas** en la tabla
   `cba349945ec4b0577321`: once columnas con importes, brechas absolutas y
   variaciones porcentuales recalculadas desde importes agregados.
3. **Ratios Gasto/Ventas normalizados** (`Prod_Ratio_Gasto_Ventas_Ppto` y
   `_Real`) en los cuatro visuales de la página, sin modificar `Efic` ni
   `%Efiprom` (`0031` §3.7).
4. **Período comparable** con cortes por métrica (`Prod_Mes_Corte_Gasto`,
   `_Ventas` y `_Ratio`), calculados por Grupo × Año (`0031` §3.8).
5. **Formato definitivo** `$ #,0 "mill."` en importes y brechas, semáforos de
   círculos con polaridad inversa entre gasto y ventas y banda ±5 % como ayuda
   visual provisional, no como meta corporativa.

Pendientes para iniciativas futuras: R1, R2, R9, R10, R11 y las dependencias 2 y 3
de §6.
