# 0025 - Análisis de impacto: referencias obsoletas en visuales del reporte (PBIP-007)

> **Fase:** análisis de impacto. **No autoriza implementación.**
> Estado de la iniciativa: `En evaluación`.
> Fecha: 2026-08-31. Base auditada: `main` = `origin/main` =
> `5b65661f6af201640f9ccba2079664cebb8f21a0`.

## Objetivo

Documentar el diagnóstico completo de los visuales del reporte que muestran
`Hubo un problema con uno o más campos` en Power BI Desktop, determinar la
causa raíz, delimitar el alcance real y proponer una estrategia de corrección
para una fase posterior.

## PBIP-006 NO es la causa

Queda descartado con evidencia reproducible:

1. **El defecto ya existía en el commit base.** Se auditó `5f48fc1` — el punto
   desde el que se ramificó `feat/sociodemografico-por-empresa` — y arroja
   exactamente los mismos conteos de visuales rotos que `main` hoy en las
   cuatro páginas reportadas por el usuario: **7 / 5 / 3 / 4**.
2. **PBIP-006 no tocó esas páginas.** `git diff 5f48fc1 5b65661` sobre cada
   carpeta de página devuelve **0 archivos modificados** para
   `Comportamiento HC Anual`, `Comportamiento HC Mensual`,
   `Product. (Colaboradores)` e `Indicadores`.
3. **Los cambios de PBIP-006 en el modelo fueron aditivos:** `Dim_Area`,
   `Dim_Dependencia`, `Dim_Estructura_Organizacional`, la columna
   `Key_Estructura` en `PLANTA DE PERSONAL` y la medida
   `Estructura Visible Periodo` en `Tbl_Medidas`. No renombró ni movió ningún
   objeto preexistente.
4. **La página creada por PBIP-006 (`Sociodemográfico por Empresa`) tiene
   0 visuales rotos.**

El refresh posterior al checkpoint no introdujo el problema: solo lo hizo
visible, al evaluar por primera vez esos visuales con datos cargados.

## Alcance real — auditoría de las 16 páginas

Se auditaron **295 visuales** contrastando cada referencia (`Column`,
`Measure`, `HierarchyLevel`, `GroupRef`, incluidos alias `From`/`SourceRef`)
contra el inventario TMDL vigente de `main` (55 tablas, 122 medidas,
658 columnas).

| Página | Visuales | Rotos | Causa principal |
|---|---|---|---|
| Ausentismos | 17 | 1 | `RENAMED_REFERENCE` |
| Comportamiento HC Anual | 20 | 7 | `RENAMED_REFERENCE` |
| Comportamiento HC Mensual | 13 | 5 | `RENAMED_REFERENCE` |
| Demográfico | 29 | 12 | `RENAMED_REFERENCE` |
| Demográfico (Promedio) | 31 | 0 | — |
| Fecha de Actualización | 1 | 0 | — |
| Gasto Laboral | 11 | 0 | — |
| Indicadores | 13 | 4 | `RENAMED_REFERENCE` |
| Portada | 2 | 0 | — |
| Product. (Colaboradores) | 9 | 3 | `RENAMED_REFERENCE` |
| Productividad | 12 | 0 | — |
| Retiros | 32 | 1 | `BROKEN_MEASURE_REFERENCE` |
| Rotación2 | 19 | 0 | — |
| SST | 34 | 0 | — |
| Selección | 32 | 0 | — |
| Sociodemográfico por Empresa | 20 | 0 | — |
| **TOTAL** | **295** | **33** | |

**33 visuales rotos en 7 páginas.** Las páginas `Demográfico` (12),
`Ausentismos` (1) y `Retiros` (1) **no habían sido reportadas por el usuario**
y amplían el alcance respecto de las cuatro observadas inicialmente.

## Causa raíz

### Patrón 1 — Medidas enlazadas a una tabla que ya no las contiene (31 visuales)

Es la causa dominante y la que efectivamente rompe el renderizado, porque la
referencia vive en la **consulta** del visual.

El visual ancla la medida a `PLANTA DE PERSONAL` o `Planta Ppto`, pero en el
modelo vigente **todas** esas medidas residen en `Tbl_Medidas`. Se verificó
medida por medida: no hay ningún caso que resuelva a una tabla distinta de
`Tbl_Medidas`.

| Referencia actual | Referencia válida en `main` | Visuales |
|---|---|---|
| `PLANTA DE PERSONAL[Tot_empleados]` | `Tbl_Medidas[Tot_empleados]` | 13 |
| `Planta Ppto[Efic_Emp]` | `Tbl_Medidas[Efic_Emp]` | 2 |
| `PLANTA DE PERSONAL[Prom_Colaboradores]` | `Tbl_Medidas[Prom_Colaboradores]` | 1 |
| `PLANTA DE PERSONAL[Tot_Colab-Directos]` | `Tbl_Medidas[Tot_Colab-Directos]` | 1 |
| `Planta Ppto[KPI_REAL]`, `[Var_Real]` | `Tbl_Medidas[…]` | 1 |
| `Planta Ppto[KPI_PPTO]`, `[Var_Ppto]` | `Tbl_Medidas[…]` | 1 |
| `Planta Ppto[Prom_Anual_Real]`, `[_Fijo]`, `[_Indef]`, `[_Sena]`, `[_Temp]` | `Tbl_Medidas[…]` | 5 |
| `Planta Ppto[tot_Año_prom]`, `[tot_Año_*_PromEmpresas_FIX]` | `Tbl_Medidas[…]` | 5 |
| `Planta Ppto[Tot_Año]`, `[Tot_Fijo]`, `[Tot_Indef]`, `[Tot_Sena]`, `[Tot_Temp]` | `Tbl_Medidas[…]` | 5 |
| `Planta Ppto[Prom_Colab]`, `[Prom_Colab_Directo]` | `Tbl_Medidas[…]` | 2 |

### Patrón 2 — Referencia a la tabla inexistente `Planta Presupuestada` (10 visuales)

Afecta a `Comportamiento HC Anual` (5) y `Comportamiento HC Mensual` (5).

**Hallazgo relevante sobre su severidad:** la referencia aparece
**exclusivamente** en
`visual/objects/dataPoint[*]/selector/data[*]/scopeId`, es decir, en los
**selectores de color condicional por punto de dato**, nunca en la consulta.
Un `scopeId` colgante normalmente solo impide aplicar esa regla de color; **no
es, por sí solo, la causa del mensaje de error**. Los 10 visuales afectados
presentan además el Patrón 1, que sí es bloqueante. Ningún visual del reporte
está roto únicamente por este patrón.

`Planta Presupuestada` **nunca existió como tabla versionada**
(`git log --all -S "table 'Planta Presupuestada'"` → 0 commits). Los mismos
visuales ya referencian `Planta Ppto`, que contiene las columnas `Año` y
`Ppto/Real` con nombre idéntico. La hipótesis más sólida es un renombrado
hecho en Power BI Desktop cuyas referencias de color no se actualizaron.

### Patrón 3 — Medida inexistente `Filtro Trimestre Dinamico` (2 visuales)

En `Product. (Colaboradores)` (`8257c3fc27f928312499`) y `Retiros`
(`37ed01c30df4dafce226`). Ambos son slicers de `Mes[Meses]` con un filtro de
nivel de visual que invoca `Tbl_Medidas[Filtro Trimestre Dinamico]`.

**No es un renombrado documentado:** la medida **nunca existió en ningún
commit** del modelo semántico. El modelo sí define
`Tbl_Medidas[Filtro Trimestre Slicer]`, ya utilizada en la página `Retiros`,
cuya lógica (`SWITCH` sobre `DimPeriodoYM[Trimestre anterior]` devolviendo
`EsTrimActual`/`EsTrimAnterior`, y `1` sin selección) corresponde exactamente
al propósito de acotar meses según el trimestre elegido.

## Comparación con el snapshot GOV-001 (evidencia, no fuente)

`rescue/gov-001-working-tree-20260831` (`510a3be`) se usó **solo como
evidencia**. No debe copiarse.

- Sus visuales **sí** contienen el re-apuntado de medidas hacia `Tbl_Medidas`,
  lo que confirma conceptualmente la dirección de la corrección.
- Pero su modelo **difiere del de `main`**: 128 medidas y 52 tablas frente a
  122 y 55, con **26 medidas ubicadas en tablas distintas** (en `rescue`
  consolidadas en `Tbl_Medidas`; en `main` distribuidas en `AUSENTISMOS`,
  `SST GENERAL`, `Ppto Ingresos`, `Selección Challenger`,
  `Selección Grupo Lemco`, `SENA UNIDADES`).
- **Prueba decisiva:** al evaluar las páginas de `rescue` contra el modelo de
  `main`, quedan **15 visuales rotos** frente a los 19 actuales en esas cuatro
  páginas. Repararía 4 y **cambiaría** el error en `Indicadores` en lugar de
  resolverlo (`Tbl_Medidas[Ausentismo]` no existe en `main`; allí vive en
  `AUSENTISMOS`).

**Conclusión: copiar páginas desde `rescue` no es una solución viable.** Toda
corrección debe resolverse contra el inventario vigente de `main`.

## Equivalencias confirmadas

| Referencia rota | Equivalente | Base de la confirmación |
|---|---|---|
| Medidas ancladas a `PLANTA DE PERSONAL` / `Planta Ppto` | La misma medida en `Tbl_Medidas` | Inventario TMDL de `main`: la medida existe con nombre idéntico y `Tbl_Medidas` es su única tabla propietaria |

## Equivalencias que requieren decisión del usuario

| Referencia rota | Equivalente propuesto | Por qué requiere aprobación |
|---|---|---|
| `Planta Presupuestada[Año]` / `[Ppto/Real]` | `Planta Ppto[Año]` / `[Ppto/Real]` | Alta confianza (columnas homónimas, el mismo visual ya usa `Planta Ppto`), pero la tabla nunca existió versionada: no hay renombrado trazable que lo demuestre |
| `Tbl_Medidas[Filtro Trimestre Dinamico]` | `Tbl_Medidas[Filtro Trimestre Slicer]` | La medida original nunca existió. La equivalencia es semántica y plausible, no documentada. Afecta a `Product. (Colaboradores)` y `Retiros` |

## Riesgos

- **Corrección masiva sobre archivos PBIR:** 33 visuales en 7 páginas. Un
  error de sustitución puede romper visuales hoy funcionales.
- **Reescritura por Power BI Desktop:** guardar el PBIP durante la
  implementación puede regenerar archivos y generar churn difícil de separar
  del cambio intencional.
- **`Demográfico` es la página más afectada (12 visuales)** y no había sido
  reportada; requiere validación visual propia.
- **El Patrón 2 puede ser cosmético.** Corregir los `scopeId` sin verificar
  antes si el visual ya renderiza tras aplicar el Patrón 1 podría introducir
  cambios de color no deseados.
- **Sin fuente maestra de trazabilidad:** ni `Planta Presupuestada` ni
  `Filtro Trimestre Dinamico` existieron versionados, por lo que ambas
  equivalencias son inferencias, no hechos documentados.
- **Alcance transversal:** `Retiros` y `Product. (Colaboradores)` comparten el
  Patrón 3; un cambio en la medida afecta a ambas páginas.

## Estrategia propuesta (no autorizada aún)

Tres bloques independientes, en orden de menor a mayor incertidumbre, cada uno
con validación visual antes de pasar al siguiente:

1. **Bloque A — Re-enlace de medidas a `Tbl_Medidas` (31 visuales).**
   Equivalencia confirmada contra el modelo. Sustitución de `Entity` y
   `queryRef` resolviendo cada medida individualmente contra el inventario,
   nunca por regla global. Es el bloque que debería restaurar el renderizado.
2. **Bloque B — `Filtro Trimestre Dinamico` → `Filtro Trimestre Slicer`
   (2 visuales).** Requiere confirmación funcional previa del usuario.
3. **Bloque C — `Planta Presupuestada` → `Planta Ppto` (10 visuales).**
   Ejecutar **solo si**, tras el Bloque A, esos visuales siguen mostrando
   error o pierden su formato condicional de color.

Condiciones de trabajo: worktree aislado, Power BI Desktop cerrado durante la
edición, validación visual página por página, y staging explícito por bloque.

## Criterios de aceptación

- 0 visuales con `Hubo un problema con uno o más campos` en las 16 páginas.
- Re-auditoría estática: 0 referencias a tablas, columnas o medidas
  inexistentes, y 0 medidas mal enlazadas, contra el TMDL de `main`.
- Las 295 referencias de visuales resuelven contra el modelo vigente.
- Ningún cambio en el modelo semántico: no se crean, renombran ni mueven
  tablas, columnas, medidas ni relaciones.
- Las páginas hoy sanas (`Demográfico (Promedio)`, `Gasto Laboral`,
  `Productividad`, `Rotación2`, `SST`, `Selección`, `Portada`,
  `Fecha de Actualización`, `Sociodemográfico por Empresa`) permanecen sin
  cambios.
- Formato condicional de color preservado o corregido de forma explícita.
- Validación visual del usuario en Power BI Desktop antes del cierre.

## Fuera de alcance

- Cualquier cambio en el modelo semántico, relaciones o DAX.
- Consolidación o reorganización de medidas entre tablas.
- Copia de páginas o TMDL desde `rescue/gov-001-working-tree-20260831`.
- Tema LEMCO global y demás pendientes visuales heredados de PBIP-006.
- Saneamiento del working tree acumulado, que pertenece a GOV-001.
