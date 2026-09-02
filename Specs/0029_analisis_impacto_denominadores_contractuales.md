# 0029 - Análisis de impacto: denominadores contractuales defectuosos (DAX-003)

- **Iniciativa:** `DAX-003`
- **Estado:** análisis de impacto abierto — **sin autorización de corrección**
- **Origen:** auditoría del estado actual del Power BI registrada en
  `Specs/0028_plan_implementacion_rotacion_proyectada.md`, sección
  "Auditoría del estado actual del Power BI — 2026-09-02"
- **Fecha:** 2026-09-02
- **Baseline auditado:** `main` en `523a793`
- **Relación con PBIP-008:** independiente. Se separa deliberadamente porque el
  alcance cruzó hacia páginas ajenas a PBIP-008.

## Por qué es una iniciativa independiente

Las medidas `Tot_Colab-Sena` y `Tot_Colab-Directos` se detectaron durante la
Fase 1B de PBIP-008, pero **no son deuda de PBIP-008**: alimentan indicadores
en uso hoy en páginas que PBIP-008 no toca, incluido ausentismo y
productividad. Corregirlas dentro de PBIP-008 mezclaría dos alcances y
ocultaría el impacto real bajo un cambio de rotación.

## Causa raíz

Ambas medidas filtran sobre el valor **crudo** de `PLANTA DE PERSONAL[TIPO_CONTR]`
con literales de texto, sin homologar la deriva de vocabulario ocurrida en
**2025-09**, cuando el origen pasó de `CONTRATO INDEFINIDO` / `CONTRATO FIJO` /
`CONTRATO APRENDIZAJE` a `INDEFINIDO` / `FIJO` / `SENA`.

El modelo **ya contiene la solución**: la columna calculada
`TIPO_CONTR (grupos)` homologa correctamente ambas eras. Las medidas
simplemente no la usan.

### Vocabulario observado (73.803 filas, 2024-01 → 2026-08)

| `TIPO_CONTR` | 2024 | 2025 | 2026 | Total |
|---|---:|---:|---:|---:|
| `CONTRATO APRENDIZAJE` | 790 | 263 | 0 | 1.053 |
| `CONTRATO DE APRENDIZAJE` | 84 | 422 | 0 | 506 |
| `CONTRATO FIJO` | 5.995 | 3.964 | 0 | 9.959 |
| `CONTRATO INDEFINIDO` | 14.606 | 11.626 | 0 | 26.232 |
| `FIJO` | 0 | 1.690 | 3.078 | 4.768 |
| `INDEFINIDO` | 0 | 6.806 | 15.329 | 22.135 |
| `SENA` | 0 | 366 | 813 | 1.179 |
| `TEMPORAL` | 4.061 | 2.859 | 1.051 | 7.971 |
| **Total** | **25.536** | **27.996** | **20.271** | **73.803** |

## Medidas afectadas

### Defecto 1 — `Tot_Colab-Sena` (`Tbl_Medidas`)

```dax
Tot_Colab-Sena =
CALCULATE(
    COUNT('PLANTA DE PERSONAL'[ID]),
    'PLANTA DE PERSONAL'[TIPO_CONTR] <> "CONTRATO APRENDIZAJE"
)
```

Excluye una sola etiqueta de aprendizaje de las tres existentes. Deja dentro
del denominador `SENA` (1.179) y `CONTRATO DE APRENDIZAJE` (506).

| | Vigente | Correcto | Error |
|---|---:|---:|---:|
| Conteo total | 72.750 | 71.065 | **+1.685 (+2,4 %)** |

El sesgo **no es uniforme**: 0,0 % en 2024-01→2024-11 y en 2025-05→2025-07;
entre +3,7 % y +4,4 % en el resto. Al ser un denominador inflado, las métricas
derivadas quedan **subestimadas** en un factor agregado de ×0,9768 (−2,3 %).

### Defecto 2 — `Tot_Colab-Directos` (`Tbl_Medidas`) — severidad máxima

```dax
Tot_Colab-Directos =
CALCULATE(COUNT('PLANTA DE PERSONAL'[ID]), 'PLANTA DE PERSONAL'[TIPO_CONTR] = "CONTRATO FIJO")
+ CALCULATE(COUNT('PLANTA DE PERSONAL'[ID]), 'PLANTA DE PERSONAL'[TIPO_CONTR] = "CONTRATO INDEFINIDO")
```

Omite `FIJO` e `INDEFINIDO`. **El agregado −42,6 % subestima la gravedad real:
la medida vale exactamente 0 desde 2025-09**, doce meses consecutivos.

| Periodo | Vigente | Correcto | Efecto |
|---|---:|---:|---|
| 2024-01 → 2025-08 | correcto | correcto | sin sesgo |
| 2025-09 | **0** | 2.111 | división por cero |
| 2025-10 | **0** | 2.123 | división por cero |
| 2025-11 | **0** | 2.172 | división por cero |
| 2025-12 | **0** | 2.090 | división por cero |
| 2026-01 | **0** | 2.192 | división por cero |
| 2026-02 | **0** | 2.252 | división por cero |
| 2026-03 | **0** | 2.265 | división por cero |
| 2026-04 | **0** | 2.273 | división por cero |
| 2026-05 | **0** | 2.333 | división por cero |
| 2026-06 | **0** | 2.344 | división por cero |
| 2026-07 | **0** | 2.356 | división por cero |
| 2026-08 | **0** | 2.392 | división por cero |
| **Total** | **36.191** | **63.094** | **−26.903 (−42,6 %)** |

No es un sesgo porcentual: es una **pérdida total de la medida** en el periodo
más reciente, justo el que se consulta a diario.

## Traza de dependencias (cierre transitivo sobre 122 medidas)

```
Tot_Colab-Sena
├── Efic_Emp              = SUM('Planta Ppto'[Ventas (MM)]) / [Tot_Colab-Sena]
├── Índice_Retiros        = [Tot_Retiros] / [Tot_Colab-Sena]
└── Índice_Rotación       = ([Tot_ingresos] - [Tot_Retiros]) / [Tot_Colab-Sena]

Tot_Colab-Directos
└── Tasa Ausentismo_EL    = AUSENTISMOS[Ausentismo]
                            / ([Tot_Colab-Directos] * SUM('Días Laborales'[Dias Lab solo fds Domingos]))
```

Sin dependencias de segundo nivel. Ningún bookmark referencia estas medidas.

## Impacto por visual y página

| Página | Visual | Tipo | Medida consumida | Efecto |
|---|---|---|---|---|
| `Indicadores` | `9a1e3d68a409` | `tableEx` | `Tot_Colab-Directos`, `Tasa Ausentismo_EL` | **Crítico** — la tasa de ausentismo divide por 0 desde 2025-09 |
| `Product. (Colaboradores)` | `c3292d5ec044` | `lineChart` | `Efic_Emp` | Productividad subestimada −2,3 % |
| `Product. (Colaboradores)` | `f5dbcb4fe4dc` | `tableEx` | `Efic_Emp` | Productividad subestimada −2,3 % |
| `Rotación2` | `5abcdd8fd1c5` | `pivotTable` | `Tot_Colab-Sena`, `Índice_Retiros` | Índice subestimado; numerador además bruto |
| `Rotación2` | `8d3d8ab39e15` | `pivotTable` | `Tot_Colab-Sena`, `Índice_Retiros` | Índice subestimado; numerador además bruto |

**Cuatro páginas afectadas**, de las cuales dos (`Indicadores` y
`Product. (Colaboradores)`) están **fuera del alcance de PBIP-008**.

## Efecto agregado sobre las métricas derivadas

| Métrica | Fórmula | Factor vigente/correcto | Lectura |
|---|---|---:|---|
| `Índice_Retiros` | `Tot_Retiros / Tot_Colab-Sena` | ×0,9768 | subestima −2,3 % |
| `Efic_Emp` | `Ventas (MM) / Tot_Colab-Sena` | ×0,9768 | subestima −2,3 % |
| `Tasa Ausentismo_EL` | `Ausentismo / (Tot_Colab-Directos × días)` | ×1,7434 | **sobreestima +74,3 % en el agregado; indefinida desde 2025-09** |

## Hallazgo secundario — `Índice_Rotación` rota

```dax
Índice_Rotación = ([Tot_ingresos] - [Tot_Retiros]) / [Tot_Colab-Sena]
```

`[Tot_ingresos]` **no existe** en el modelo (0 definiciones entre 122 medidas).
La medida no se consume en ningún visual ni bookmark. Se registra por
completitud; prioridad menor que los dos denominadores, porque no contamina
resultados actualmente visibles.

Nota de desambiguación: `Índice_Rotación` (con tildes, rota) es distinta de
`Indice_Rotacion` (sin tildes, correcta, sobre `Planta Ppto`, consumida por
`Indicadores de Rotación`). La coexistencia de ambos nombres es en sí un riesgo
de gobierno semántico y corresponde al Gate C.

## Riesgos

| # | Riesgo | Severidad | Mitigación propuesta |
|---|---|---|---|
| 1 | Decisiones tomadas sobre ausentismo desde 2025-09 con una tasa indefinida o inflada | Alta | Verificar si la página se usó para reportes de comité; comunicar antes de corregir |
| 2 | Corregir el denominador cambia valores históricos ya divulgados | Alta | Documentar el antes/después por periodo y acordar comunicación del cambio |
| 3 | La corrección toca `AUSENTISMOS`, fuera del alcance de PBIP-008 | Media | Iniciativa independiente (este documento); autorización propia |
| 4 | `Índice_Retiros` tiene además numerador bruto (`COUNT('Ppto Retiros'[Mes])`) | Media | Tratar en Gate C, no aquí; corregir el denominador no lo sanea |
| 5 | Nueva deriva de vocabulario futura vuelve a romper las medidas | Media | Filtrar por `TIPO_CONTR (grupos)`, no por literales crudos |

## Opciones de corrección (no autorizadas, para decisión)

| Opción | Descripción | Ventaja | Riesgo |
|---|---|---|---|
| A | Reescribir ambas medidas para filtrar por `TIPO_CONTR (grupos)` | Reutiliza el patrón sano ya existente; resistente a nueva deriva | Cambia valores históricos |
| B | Ampliar los literales de la lista actual | Cambio mínimo | Vuelve a romperse en la próxima deriva |
| C | Crear medidas nuevas y migrar los visuales gradualmente | Permite comparar antes/después | Duplica medidas; agrava el gobierno semántico |

**Recomendación técnica:** opción A. Es la única que elimina la causa raíz y es
coherente con el criterio de Gate C. Requiere acordar previamente la
comunicación del cambio de valores históricos.

## Criterios de aceptación

1. `Tot_Colab-Directos` distinto de 0 en todos los periodos 2025-09 → 2026-08.
2. `Tot_Colab-Sena` excluye las tres etiquetas de aprendizaje en todos los periodos.
3. `Tasa Ausentismo_EL` produce valores finitos en todo el rango.
4. Validación con datos reales, no con supuestos, antes de cerrar.
5. Documentar el antes/después por periodo en `Docs/METRICS_CATALOG.md`.

## Estado

Análisis de impacto **abierto**. **No se autoriza corrección** de medidas,
visuales ni Power Query. Este documento es diagnóstico; la ejecución requiere
autorización expresa del usuario conforme a `AGENTS.md`.

## Validaciones ejecutadas

- Inventario completo: 122 medidas del modelo semántico parseadas desde TMDL.
- Cierre transitivo de dependencias sobre las 122 medidas.
- Barrido de los visuales de todas las páginas de `Proyecto.Report` y de los
  bookmarks.
- Conteos por periodo sobre 73.803 filas reales
  (`Data/HeadCount/2024/Consolidado 2024.xlsx` hoja `PLANTA DE PERSONAL`,
  `Data/HeadCount/2025/Consolidado 2025.xlsx` hoja `Consolidado2025`).
- Sin datos personales versionados; las copias temporales de trabajo se
  eliminaron.
