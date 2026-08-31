# 0026 - Plan de implementación: referencias obsoletas en visuales (PBIP-007)

> **Fase:** plan de implementación. **Esta fase sigue siendo documentación:
> no se modifica ningún archivo de `PBIP/` todavía.**
> Análisis de impacto: `Specs/0025_analisis_impacto_referencias_obsoletas_visuales.md`.
> Fecha: 2026-08-31.

## Contexto y base

- Rama: `fix/pbip-007-referencias-obsoletas`
- Worktree aislado: `.wt/pbip-007-referencias-obsoletas`
- Base: `origin/main` = `5b65661f6af201640f9ccba2079664cebb8f21a0`
- Auditoría base: 295 visuales en 16 páginas, **33 rotos en 7 páginas**.

`PBIP-006` está descartado como causa con evidencia reproducible (ver `0025`).
Este plan **no reabre** esa iniciativa.

## Decisiones del usuario que gobiernan este plan

1. **Aprobado:** re-enlace de las medidas obsoletas a su tabla real
   `Tbl_Medidas`.
2. **Aprobado conceptualmente:** `Filtro Trimestre Dinamico` →
   `Filtro Trimestre Slicer`, a implementar como **bloque independiente** con
   validación manual en Power BI Desktop.
3. **No autorizado todavía:** `Planta Presupuestada` → `Planta Ppto`. Esas
   referencias viven únicamente en selectores de formato/color y no parecen
   causar el error de render. Se evaluará **después** de reparar los bindings
   funcionales.

## Principios de ejecución

- **No se modifica el modelo semántico.** Ni DAX, ni tablas, ni columnas, ni
  medidas, ni relaciones. Solo archivos `visual.json` del reporte.
- **Power BI Desktop cerrado** durante toda edición de archivos
  (`PBIDesktop.exe` y `msmdsrv.exe` ausentes). Verificar antes de cada bloque.
- **No guardar el PBIP** desde Desktop durante la validación: al guardar,
  Desktop reescribe archivos y genera churn indistinguible del cambio
  intencional.
- **Resolución individual, nunca sustitución global.** Cada medida se resuelve
  contra el inventario TMDL vigente. Está prohibido un `sed` masivo de
  `PLANTA DE PERSONAL` → `Tbl_Medidas`: esas tablas siguen siendo válidas para
  columnas reales.
- **Staging explícito por bloque.** Sin `git add .` ni `git add -A`.
- **No se copia nada** desde `rescue/gov-001-working-tree-20260831`.

## Distribución del trabajo por bloque

| Bloque | Patrón | Visuales | Páginas |
|---|---|---|---|
| A | Medidas mal enlazadas | **31** | Demográfico (12), C. HC Anual (7), C. HC Mensual (5), Indicadores (4), Product. Colaboradores (2), Ausentismos (1) |
| B | `Filtro Trimestre Dinamico` | **2** | Product. Colaboradores (1), Retiros (1) |
| C | `Planta Presupuestada` (color) | **10** | C. HC Anual (5), C. HC Mensual (5) |

---

## Bloque A — Bindings de medidas

### Alcance

31 visuales. Para cada referencia de tipo `Measure` cuya `Entity` sea
`PLANTA DE PERSONAL` o `Planta Ppto` y cuya medida resida realmente en
`Tbl_Medidas`, actualizar:

- `field.Measure.Expression.SourceRef.Entity` → `Tbl_Medidas`
- el `queryRef` correspondiente → `Tbl_Medidas.<medida>`
- las entradas equivalentes dentro de `sortDefinition`, `filterConfig` y
  cualquier `From[].Entity` asociado a esa medida

**No** se modifican: `name` del visual, `position`, `objects` de formato,
`nativeQueryRef`, `displayName`, ni ninguna referencia a **columnas** reales de
`PLANTA DE PERSONAL` o `Planta Ppto`, que siguen siendo tablas válidas.

### Medidas a re-enlazar

| Medida | Entity actual en el visual | Entity correcta |
|---|---|---|
| `Tot_empleados` (13 visuales) | `PLANTA DE PERSONAL` | `Tbl_Medidas` |
| `Prom_Colaboradores` | `PLANTA DE PERSONAL` | `Tbl_Medidas` |
| `Tot_Colab-Directos` | `PLANTA DE PERSONAL` | `Tbl_Medidas` |
| `Efic_Emp` (2 visuales) | `Planta Ppto` | `Tbl_Medidas` |
| `KPI_REAL`, `Var_Real` | `Planta Ppto` | `Tbl_Medidas` |
| `KPI_PPTO`, `Var_Ppto` | `Planta Ppto` | `Tbl_Medidas` |
| `Prom_Anual_Real`, `_Fijo`, `_Indef`, `_Sena`, `_Temp` | `Planta Ppto` | `Tbl_Medidas` |
| `tot_Año_prom`, `tot_Año_{Fijo,Indef,Sena,Temp}_PromEmpresas_FIX` | `Planta Ppto` | `Tbl_Medidas` |
| `Tot_Año`, `Tot_Fijo`, `Tot_Indef`, `Tot_Sena`, `Tot_Temp` | `Planta Ppto` | `Tbl_Medidas` |
| `Prom_Colab`, `Prom_Colab_Directo` | `Planta Ppto` | `Tbl_Medidas` |

Antes de cada sustitución debe reconfirmarse la tabla propietaria contra el
TMDL vigente; la tabla del plan es el estado a `5b65661`, no una autoridad
permanente.

### Gate A — criterios de salida

**Estático (bloqueante):**

1. Los 31 `visual.json` son JSON parseables y UTF-8 sin BOM.
2. Re-auditoría: **0 referencias con `RENAMED_REFERENCE`** en las 16 páginas.
3. Los únicos hallazgos restantes son los 2 de Bloque B y los 10 de Bloque C.
4. `git diff --check` sin errores; staging vacío antes de preparar el commit.
5. El diff contiene **exclusivamente** cambios de `Entity` y `queryRef`. Ningún
   cambio en `position`, `objects`, `name`, `filterConfig` no relacionado, ni
   en `PBIP/Proyecto.SemanticModel/`.
6. Conteo de archivos modificados ≤ 31, todos bajo
   `PBIP/Proyecto.Report/definition/pages/`.

**Funcional en Power BI Desktop (bloqueante):**

7. Abrir el PBIP del worktree y **actualizar datos**.
8. Verificar que **desaparece el error** en las 6 páginas del Bloque A:
   `Demográfico`, `Comportamiento HC Anual`, `Comportamiento HC Mensual`,
   `Indicadores`, `Product. (Colaboradores)` y `Ausentismos`.
9. Comprobar que los valores mostrados son **coherentes** con los esperados: el
   re-enlace no debe alterar cifras, solo resolver el binding.
10. Verificar que **no hay regresión** en las 7 páginas sanas (ver sección
    "Alcance de validación").
11. **No guardar** el PBIP. Cerrar Desktop y confirmar que `git status` sigue
    mostrando solo los archivos intencionales.

Si tras el Gate A siguen apareciendo errores de render en visuales del Bloque
A, **detenerse** y reabrir diagnóstico antes de continuar.

---

## Bloque B — Filtro de trimestre

### Alcance

2 visuales, ambos slicers de `Mes[Meses]` con filtro de nivel de visual:

| Página | Visual | Acción |
|---|---|---|
| Product. (Colaboradores) | `8257c3fc27f928312499` | `Tbl_Medidas[Filtro Trimestre Dinamico]` → `Tbl_Medidas[Filtro Trimestre Slicer]` |
| Retiros | `37ed01c30df4dafce226` | ídem |

`Filtro Trimestre Dinamico` **nunca existió** en ningún commit del modelo; no
es un renombrado trazable sino una referencia colgante. `Filtro Trimestre
Slicer` existe, ya se usa en la página `Retiros`, y su DAX (`SWITCH` sobre
`DimPeriodoYM[Trimestre anterior]` devolviendo `EsTrimActual` /
`EsTrimAnterior`, y `1` sin selección) corresponde al propósito de acotar los
meses según el trimestre seleccionado.

### Gate B — criterios de salida

**Estático:**

1. JSON parseable, UTF-8 sin BOM, en los 2 archivos.
2. Re-auditoría: **0 `BROKEN_MEASURE_REFERENCE`** en las 16 páginas.
3. `git diff --check` limpio; diff acotado a los 2 archivos.

**Funcional — validación manual obligatoria de los tres estados:**

4. **Trimestre actual:** el slicer de `Mes` muestra solo los meses del
   trimestre en curso.
5. **Trimestre anterior:** muestra solo los meses del trimestre previo.
6. **Sin selección:** muestra **todos** los meses (la medida devuelve `1`).
7. Confirmar el comportamiento en **ambas** páginas, ya que comparten la
   medida y un cambio afecta a las dos.
8. Verificar que los visuales dependientes de esos slicers responden
   correctamente al cambio de trimestre.

Si el comportamiento difiere de lo esperado en cualquiera de los tres estados,
**revertir el bloque** y consultar antes de insistir: significaría que la
equivalencia semántica no se sostiene.

---

## Bloque C — Formato y color (NO autorizado)

`Planta Presupuestada` **no se modifica en esta fase.**

Las 10 referencias viven exclusivamente en
`visual/objects/dataPoint[*]/selector/data[*]/scopeId`, es decir, en los
selectores de color condicional por punto de dato, nunca en la consulta. Un
`scopeId` colgante normalmente solo impide aplicar esa regla de color.

### Condición de activación

Este bloque se analizará **solo si**, completados A y B:

- los 10 visuales de `Comportamiento HC Anual` y `Comportamiento HC Mensual`
  **ya renderizan** correctamente, **y**
- sus colores o formatos condicionales **siguen siendo incorrectos**.

Si ambos se cumplen, se elaborará una propuesta específica para sustituir
`Planta Presupuestada` por `Planta Ppto` en los selectores (columnas `Año` y
`Ppto/Real`, homónimas en ambas), que requerirá **aprobación explícita del
usuario** antes de ejecutarse.

Si los colores son correctos, el bloque se cierra sin cambios y las
referencias colgantes se documentan como deuda cosmética conocida.

---

## Alcance de validación

### Páginas a corregir y validar (7)

| Página | Bloque | Visuales |
|---|---|---|
| Demográfico | A | 12 |
| Comportamiento HC Anual | A (+C diferido) | 7 |
| Comportamiento HC Mensual | A (+C diferido) | 5 |
| Indicadores | A | 4 |
| Product. (Colaboradores) | A + B | 3 |
| Ausentismos | A | 1 |
| Retiros | B | 1 |

### Páginas a verificar sin regresión (7 + 2)

`Demográfico (Promedio)`, `Sociodemográfico por Empresa`, `Rotación2`,
`Productividad`, `Gasto Laboral`, `SST`, `Selección`, más `Portada` y
`Fecha de Actualización`.

Hoy tienen **0 visuales rotos**. Criterio: deben seguir con 0 tras cada bloque,
tanto en la re-auditoría estática como en la revisión visual. Atención especial
a `Demográfico (Promedio)` y `Gasto Laboral`, que usan medidas de
`Tbl_Medidas` y comparten tablas con las páginas intervenidas.

---

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Sustitución global rompe columnas válidas | Resolución individual por medida; prohibido `sed` masivo |
| Desktop reescribe archivos al guardar | Desktop cerrado al editar; no guardar al validar; `git status` tras cerrar |
| `Demográfico` es la página más afectada (12) | Validarla aisladamente antes de dar por bueno el Gate A |
| La equivalencia del Bloque B no se sostiene | Validar los tres estados del trimestre; revertir el bloque si falla |
| Corregir el Bloque C sin necesidad altera colores | Bloque C condicionado a evidencia posterior a A y B |
| Bloqueos de OneDrive al manipular el worktree | Procedimiento seguro de `Specs/0021`; reportar antes de eliminación manual |

## Criterios de aceptación de PBIP-007

1. **0 visuales** con `Hubo un problema con uno o más campos` en las 16
   páginas, verificado en Power BI Desktop.
2. Re-auditoría estática: 0 referencias a tablas, columnas o medidas
   inexistentes y 0 medidas mal enlazadas contra el TMDL de `main`.
3. Las 295 referencias resuelven contra el modelo vigente.
4. **Ningún cambio** en `PBIP/Proyecto.SemanticModel/`.
5. Las 9 páginas hoy sanas sin regresión.
6. Formato condicional preservado, o su desviación documentada de forma
   explícita en el Bloque C.
7. Documentación actualizada: cierre en `0025`/`0026` y estado de `PBIP-007`
   en `Specs/00_roadmap_y_backlog.md`.
8. Validación visual del usuario antes del cierre.

## Secuencia operativa propuesta

1. **Fase actual — documentación.** Este plan y `0025`. Sin tocar `PBIP/`.
2. Autorización del usuario para ejecutar el **Bloque A**.
3. Bloque A → **Gate A** (estático + visual) → commit del bloque.
4. Autorización para el **Bloque B**.
5. Bloque B → **Gate B** (los tres estados del trimestre) → commit del bloque.
6. Evaluación de la condición de activación del **Bloque C** y, si procede,
   propuesta específica para aprobación.
7. Re-auditoría final de las 16 páginas, actualización documental, PR en
   `Draft` y validación visual del usuario antes del merge.

Cada paso requiere autorización expresa. Este plan **no autoriza** por sí mismo
ninguna modificación de `PBIP/`.
