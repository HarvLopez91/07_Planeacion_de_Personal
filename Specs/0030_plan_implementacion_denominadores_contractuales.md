# 0030 - Plan de implementación: corrección de denominadores contractuales (DAX-003)

- **Iniciativa:** `DAX-003`
- **Estado:** plan preparado — **sin autorización de ejecución**
- **Análisis de impacto:** `Specs/0029_analisis_impacto_denominadores_contractuales.md`
- **Fecha:** 2026-09-02
- **Baseline:** `main` en `1f614e6`
- **Relación con PBIP-008:** independiente. No se ejecuta dentro de PBIP-008.

Este documento existe porque el usuario condicionó cualquier corrección técnica
a la existencia previa de un plan. Registrar el plan **no autoriza ejecutarlo**.

## 1. Medidas afectadas

### Medidas a corregir

| # | Medida | Tabla | Defecto | Severidad |
|---|---|---|---|---|
| 1 | `Tot_Colab-Directos` | `Tbl_Medidas` | Filtra `="CONTRATO FIJO"` y `="CONTRATO INDEFINIDO"`; omite `FIJO` e `INDEFINIDO`. **Vale 0 desde 2025-09** | Crítica |
| 2 | `Tot_Colab-Sena` | `Tbl_Medidas` | Filtra `<>"CONTRATO APRENDIZAJE"`; deja dentro `SENA` y `CONTRATO DE APRENDIZAJE` | Alta |

### Medidas que heredan el defecto (no se reescriben; se revalidan)

| # | Medida | Tabla | Depende de |
|---|---|---|---|
| 3 | `Tasa Ausentismo_EL` | `AUSENTISMOS` | `Tot_Colab-Directos` |
| 4 | `Efic_Emp` | `Tbl_Medidas` | `Tot_Colab-Sena` |
| 5 | `Índice_Retiros` | `Tbl_Medidas` | `Tot_Colab-Sena` |

### Medida fuera de alcance de esta corrección

`Índice_Rotación` referencia `[Tot_ingresos]`, inexistente. Está rota con
independencia del denominador y **no se consume en ningún visual**. Corregirla
o eliminarla es una decisión de gobierno semántico que corresponde al Gate C,
no a `DAX-003`. Se documenta para que no se pierda.

## 2. Dependencias

Cierre transitivo verificado sobre las 122 medidas del modelo. No hay
dependencias de segundo nivel ni bookmarks implicados.

```
Tot_Colab-Sena
├── Efic_Emp              = SUM('Planta Ppto'[Ventas (MM)]) / [Tot_Colab-Sena]
├── Índice_Retiros        = [Tot_Retiros] / [Tot_Colab-Sena]
└── Índice_Rotación       (rota, sin consumo — fuera de alcance)

Tot_Colab-Directos
└── Tasa Ausentismo_EL    = AUSENTISMOS[Ausentismo]
                            / ([Tot_Colab-Directos] * SUM('Días Laborales'[Dias Lab solo fds Domingos]))
```

### Dependencia estructural

Ambas medidas dependen de `PLANTA DE PERSONAL[TIPO_CONTR]`. La columna
calculada `TIPO_CONTR (grupos)` ya existe en la misma tabla y homologa
correctamente las dos eras de vocabulario. **La corrección no requiere crear
objetos nuevos en el modelo**, solo reapuntar el filtro.

Riesgo de dependencia: `TIPO_CONTR (grupos)` es una columna de grupo de Power BI
(`GroupingMetadata`). Debe confirmarse que Power BI Desktop permite filtrarla
desde DAX sin romper la definición del grupo al guardar.

## 3. Impacto en páginas

| Página | Visual | Tipo | Medida | Cambio esperado |
|---|---|---|---|---|
| `Indicadores` | `9a1e3d68a409` | `tableEx` | `Tot_Colab-Directos`, `Tasa Ausentismo_EL` | La tasa pasa de indefinida a un valor finito en 2025-09→2026-08 |
| `Product. (Colaboradores)` | `c3292d5ec044` | `lineChart` | `Efic_Emp` | Sube ~+2,3 % agregado |
| `Product. (Colaboradores)` | `f5dbcb4fe4dc` | `tableEx` | `Efic_Emp` | Sube ~+2,3 % agregado |
| `Rotación2` | `5abcdd8fd1c5` | `pivotTable` | `Tot_Colab-Sena`, `Índice_Retiros` | Sube ~+2,3 % agregado |
| `Rotación2` | `8d3d8ab39e15` | `pivotTable` | `Tot_Colab-Sena`, `Índice_Retiros` | Sube ~+2,3 % agregado |

Cuatro páginas; **dos fuera del alcance de PBIP-008**. Ningún bookmark afectado.

`Indicadores de Rotación` (`f04eef32`) **no se toca**: usa `Indice_Rotacion`
sobre `Planta Ppto` y no depende de ninguna medida de este plan.

## 4. Impacto histórico esperado

### `Tot_Colab-Directos` — no es un sesgo, es una pérdida de medida

| Periodo | Vigente | Esperado tras corrección | Efecto en `Tasa Ausentismo_EL` |
|---|---:|---:|---|
| 2024-01 → 2025-08 | correcto | **sin cambio** | ninguno |
| 2025-09 | 0 | 2.111 | de indefinida a finita |
| 2025-10 | 0 | 2.123 | de indefinida a finita |
| 2025-11 | 0 | 2.172 | de indefinida a finita |
| 2025-12 | 0 | 2.090 | de indefinida a finita |
| 2026-01 | 0 | 2.192 | de indefinida a finita |
| 2026-02 | 0 | 2.252 | de indefinida a finita |
| 2026-03 | 0 | 2.265 | de indefinida a finita |
| 2026-04 | 0 | 2.273 | de indefinida a finita |
| 2026-05 | 0 | 2.333 | de indefinida a finita |
| 2026-06 | 0 | 2.344 | de indefinida a finita |
| 2026-07 | 0 | 2.356 | de indefinida a finita |
| 2026-08 | 0 | 2.392 | de indefinida a finita |
| **Total** | 36.191 | 63.094 | **+26.903 (+74,3 %)** |

**Ningún valor histórico previo a 2025-09 cambia.** Esto reduce mucho el riesgo
de comunicación: no se reescribe la historia divulgada, se recupera un periodo
que hoy no produce resultado.

### `Tot_Colab-Sena` — sesgo real sobre el histórico

| Rango | Sesgo actual | Efecto en `Efic_Emp` e `Índice_Retiros` |
|---|---:|---|
| 2024-01 → 2024-11 | 0,0 % | sin cambio |
| 2024-12 | +4,0 % | suben ~4 % |
| 2025-01 → 2025-04 | +3,7 % a +3,9 % | suben ~4 % |
| 2025-05 → 2025-07 | 0,0 % | sin cambio |
| 2025-08 → 2026-08 | +3,7 % a +4,4 % | suben ~4 % |
| **Agregado** | **+2,4 %** | **×0,9768 → suben +2,3 %** |

Aquí sí cambian valores ya divulgados, de forma no uniforme. **Requiere acuerdo
de comunicación antes de aplicar.**

## 5. Estrategia de validación antes/después

Condición previa vinculante: **capturar la línea base antes de tocar nada**.

### Fase V0 — línea base (antes del cambio)

1. Ejecutar consultas DAX sobre el modelo vigente y guardar en `Outputs/`:
   `Tot_Colab-Sena`, `Tot_Colab-Directos`, `Efic_Emp`, `Índice_Retiros` y
   `Tasa Ausentismo_EL`, desglosadas por Año × Mes y por Grupo Empresa.
2. Capturas de los 5 visuales afectados en su estado actual.
3. Registrar el commit exacto de la línea base.

Sin V0 completo no se autoriza pasar a V1.

### Fase V1 — corrección

Aplicar la opción elegida (ver sección 6) sobre `Tbl_Medidas.tmdl`. Sin tocar
visuales, Power Query, relaciones ni ninguna otra medida.

### Fase V2 — validación comparativa

| # | Criterio | Verificación |
|---|---|---|
| 1 | `Tot_Colab-Directos` distinta de 0 en los 12 periodos 2025-09→2026-08 | Consulta DAX |
| 2 | `Tot_Colab-Directos` **idéntica** a V0 en 2024-01→2025-08 | Diferencia = 0 en todos los periodos |
| 3 | `Tot_Colab-Sena` excluye las 3 etiquetas de aprendizaje | Total 71.065 |
| 4 | `Tasa Ausentismo_EL` finita en todo el rango | Sin `Infinity` ni blanco por división |
| 5 | `Efic_Emp` sube exactamente lo previsto | Contraste contra la tabla de la sección 4 |
| 6 | Ningún otro visual del reporte cambia | Comparación de capturas fuera de las 4 páginas |
| 7 | El modelo abre sin error en Power BI Desktop | Confirmación visual del usuario |

El criterio 2 es el más importante: **si cambia el histórico previo a 2025-09,
la corrección está mal hecha** y debe revertirse.

### Fase V3 — cierre

Documentar el antes/después por periodo en `Docs/METRICS_CATALOG.md`, declarando
la población de origen de cada medida. Actualizar el roadmap con evidencia.

## 6. Validaciones exigidas antes de elegir la opción de corrección

El usuario condicionó la adopción de `TIPO_CONTR (grupos)` —candidata
principal— a cuatro validaciones previas. Dos están cerradas (2026-09-03); la
técnica (#1) sigue bloqueada por falta de modelo vivo.

| # | Validación | Estado | Cómo se cierra |
|---|---|---|---|
| 1 | Diferencia histórica de indicadores | Cuantificada sobre datos (sección 4), **no validada contra el modelo vivo** — bloqueada: Power BI Desktop no está abierto y no hay conexión MCP activa (verificado 2026-09-03) | Consultas DAX en V0 y contraste con los conteos de `Specs/0029`, cuando el usuario abra Power BI Desktop |
| 2 | Impacto en ausentismo | **Cerrada (2026-09-03).** El usuario confirma que `Tasa Ausentismo_EL` (junto con `Efic_Emp` e `Índice_Retiros`) es un indicador de análisis interno del área de Gestión Humana, sin correspondencia en reportes oficiales externos ni información comunicada formalmente | — |
| 3 | Impacto en productividad | **Cerrada (2026-09-03).** El usuario confirma que `Efic_Emp` es un indicador de análisis interno del área de Talento Humano/Gestión Humana y no alimenta reportes externos | — |
| 4 | Necesidad de conservar medidas históricas para trazabilidad | **Cerrada (2026-09-03).** El usuario confirma explícitamente **T3**: corrección en sitio, sin medida histórica duplicada en el modelo, con la tabla antes/después en `Docs/METRICS_CATALOG.md` | Ver sección 7 |

### Nota — secuencia de corrección instruida por el usuario (2026-09-03)

El usuario prioriza expresamente: **1) `Tot_Colab-Directos`** (corrige la
tasa de ausentismo indefinida desde 2025-09), **2) `Tot_Colab-Sena`**
(homologación contractual para evitar inconsistencias históricas). Ambas
correcciones son independientes entre sí en el modelo (no comparten dependencia
directa), por lo que este orden no impone una restricción técnica, solo de
secuencia de trabajo y de comunicación del cambio.

El usuario autoriza avanzar con la **preparación** de la corrección (línea base
V0 y documentación de impacto), pero **no la ejecución**: valida 4 puntos —
(1) validación técnica en el modelo vivo, (2) captura de línea base, (3)
documentación del impacto esperado, (4) ninguna modificación ni commit hasta
completar la validación técnica. Los puntos 1 y 2 siguen bloqueados por falta
de modelo vivo (ver validación 1 arriba); el punto 3 ya está cubierto por esta
Spec y por `Specs/0029`.

### Nota — alcance confirmado de `Efic_Emp` (2026-09-03)

El usuario acota expresamente esta corrección: **no se modifica la fórmula de
`Efic_Emp`** (`SUM('Planta Ppto'[Ventas (MM)]) / [Tot_Colab-Sena]`); la
validación se limita a si `Tot_Colab-Sena` respeta su definición funcional
("colaboradores activos del cierre mensual, excluyendo aprendizaje/SENA" —
`Docs/METRICS_CATALOG.md`, sección "Denominador de rotación — `Total-Sena`") y,
de existir diferencia, el ajuste se restringe a la homologación contractual.
Esto es exactamente el alcance de la **Opción A** (sección 8): la forma de
`Tot_Colab-Sena` (`CALCULATE(COUNT(ID), <exclusión>)`) no cambia, solo el
criterio de exclusión.

Verificación de la definición funcional sobre `Tot_Colab-Sena`:

- **Población (grano y tabla):** correcta. `Tot_Colab-Sena` opera sobre
  `PLANTA DE PERSONAL` (`Consolidado 2024.xlsx` + `Consolidado 2025.xlsx` vía
  `Table.Combine`), la fotografía mensual de activos — la misma población que
  la definición de negocio exige.
- **Criterio de exclusión:** **no** cumple la definición. Filtra únicamente el
  literal `<>"CONTRATO APRENDIZAJE"`, y `Docs/METRICS_CATALOG.md` documenta que
  la exclusión debe cubrir las tres etiquetas de la deriva de vocabulario
  (`CONTRATO DE APRENDIZAJE`, `CONTRATO APRENDIZAJE`, `SENA`) o deja
  ~90-110 personas dentro del denominador desde 2025-09. Esto reconfirma el
  defecto ya cuantificado en `Specs/0029` (+2,4 % agregado); no cambia el
  diagnóstico, lo valida contra la definición canónica de negocio.

**Precisión de linaje (evita una confusión de origen):** `Tot_Colab-Sena` se
calcula en vivo por DAX directamente sobre `PLANTA DE PERSONAL`; **no** pasa
por la hoja `Planta Personal` de `PptovsReal.xlsx`. Esa hoja alimenta una tabla
distinta, `Planta Ppto`, cuya columna `Total-Sena` se transcribe manualmente
(`Total − Sena`, sin vínculo de fórmula hacia `Consolidado 2025.xlsx` —
`Docs/DATA_PIPELINE.md`) y es el denominador oficial de `Tasa_Mensual_Retiros`
e `Indice_Rotacion`, **no** de `Efic_Emp`. La coexistencia de estos dos
denominadores ("Total-Sena" manual en `Planta Ppto` vs. `Tot_Colab-Sena`
automático sobre `PLANTA DE PERSONAL`) ya está registrada como riesgo **R4** en
`Specs/0027`.

La cuantificación de este plan proviene de los archivos fuente, no del modelo
en ejecución. **Debe confirmarse contra el modelo vivo antes de decidir.**

## 7. Conservación de trazabilidad — decisión pendiente

Corregir en sitio hace que los valores históricos cambien sin dejar rastro del
valor anterior. Tres tratamientos posibles:

| Opción | Descripción | Ventaja | Costo |
|---|---|---|---|
| T1 | Corregir en sitio, sin medida histórica | Modelo limpio; sin duplicación | Se pierde la capacidad de reproducir lo divulgado |
| T2 | Corregir en sitio y conservar la versión anterior como medida oculta marcada como obsoleta | Trazabilidad completa | Dos medidas con el mismo nombre conceptual; riesgo de uso accidental |
| T3 | Corregir en sitio y dejar la trazabilidad **solo en documentación** (`Docs/METRICS_CATALOG.md` con la tabla antes/después) | Sin duplicación en el modelo; historia auditable | La reproducción exige leer documentación, no consultar el modelo |

**Recomendación:** T3. La evidencia antes/después de la sección 4 es suficiente
para auditar el cambio, y T2 agravaría precisamente el problema de gobierno
semántico que Gate C busca cerrar.

### Decisión del usuario (2026-09-03) — T3 aprobada

**T3 confirmada.** No se crean medidas históricas duplicadas en el modelo
semántico. La trazabilidad vive en `Docs/METRICS_CATALOG.md`, que debe
registrar, en el momento de ejecutar V1:

1. La fórmula anterior y la nueva de `Tot_Colab-Sena` y `Tot_Colab-Directos`.
2. La tabla antes/después por periodo de la sección 4.
3. La fecha de corrección y la referencia a `Specs/0029` y a esta Spec.
4. La nota de que `Tasa Ausentismo_EL` pasa de indefinida a finita desde
   2025-09, y que `Efic_Emp` cambia de valor sin cambiar de fórmula.

**Consecuencia operativa de T3:** una vez ejecutada la corrección, los valores
anteriores **no serán reproducibles desde el modelo**. Quien necesite
reconstruir una cifra divulgada antes de la corrección deberá acudir a la
documentación, no a Power BI. Esto es aceptado como parte de la decisión.

La tabla antes/después **no se escribe todavía** en `Docs/METRICS_CATALOG.md`:
hacerlo antes de aplicar V1 documentaría un cambio que no ha ocurrido. Se
redacta como parte de la fase V3.

## 8. Opciones de corrección

Reproducidas de `Specs/0029` para que este plan sea autocontenido.

| Opción | Descripción | Ventaja | Riesgo |
|---|---|---|---|
| **A** | Filtrar por `TIPO_CONTR (grupos)` | Reutiliza el patrón sano del modelo; resistente a nueva deriva | Cambia valores históricos; depende de una columna de grupo |
| B | Ampliar la lista de literales | Cambio mínimo | Vuelve a romperse en la próxima deriva |
| C | Crear medidas nuevas y migrar visuales | Permite comparar en paralelo | Duplica medidas; agrava el gobierno semántico |

**Candidata principal: A**, conforme a la instrucción del usuario, condicionada
a las cuatro validaciones de la sección 6.

### Redacción propuesta (borrador, no aplicado)

```dax
Tot_Colab-Sena =
CALCULATE(
    COUNT('PLANTA DE PERSONAL'[ID]),
    'PLANTA DE PERSONAL'[TIPO_CONTR (grupos)] <> "Contrato De Aprendizaje"
)
```

```dax
Tot_Colab-Directos =
CALCULATE(
    COUNT('PLANTA DE PERSONAL'[ID]),
    'PLANTA DE PERSONAL'[TIPO_CONTR (grupos)] IN { "Contrato Fijo", "Contrato Indefinido" }
)
```

Ambas requieren confirmar las etiquetas exactas que produce
`TIPO_CONTR (grupos)` en el modelo vivo antes de escribirse. Si filtrar la
columna de grupo resultara inviable, la alternativa es replicar su lógica con
`SWITCH` dentro de la medida, lo que preserva el resultado pero no la resistencia
a futuras derivas.

## 9. Secuencia de ejecución

| Paso | Acción | Requiere autorización |
|---|---|---|
| 1 | Cerrar las 4 validaciones de la sección 6 contra el modelo vivo | No — es análisis |
| 2 | Decidir opción de corrección (A/B/C) y tratamiento de trazabilidad (T1/T2/T3) | **Sí — usuario** |
| 3 | Acordar la comunicación del cambio de valores históricos | **Sí — usuario** |
| 4 | Capturar línea base V0 | **Sí** |
| 5 | Aplicar corrección V1 en `Tbl_Medidas.tmdl` | **Sí** |
| 6 | Validar V2 contra los 7 criterios | No |
| 7 | Documentar V3 y cerrar en el roadmap | No |

## 10. Riesgos del plan

| # | Riesgo | Severidad | Mitigación |
|---|---|---|---|
| 1 | Aplicar la corrección sin línea base V0 impide demostrar qué cambió | Alta | V0 es condición previa bloqueante |
| 2 | El cambio del histórico de `Efic_Emp` e `Índice_Retiros` sorprende a consumidores | Alta | Paso 3 de la secuencia |
| 3 | `TIPO_CONTR (grupos)` no es filtrable desde DAX o se corrompe al guardar en Desktop | Media | Validar en el modelo vivo antes de comprometer la opción A |
| 4 | Power BI Desktop reserializa archivos ajenos al guardar | Media | Aislar el cambio funcional en el staging, como en `379ea9e` |
| 5 | La corrección se confunde con avance de PBIP-008 | Media | Rama e iniciativa separadas; este plan es de `DAX-003` |
| 6 | `Índice_Retiros` sigue con numerador bruto tras la corrección | Media | Declarar explícitamente que `DAX-003` no lo sanea; queda en Gate C |

## 11. Estado

**Decisiones de diseño cerradas (2026-09-03):** opción de corrección **A**
(filtrar por `TIPO_CONTR (grupos)`) y trazabilidad **T3** (historia en
documentación, sin duplicar medidas). Con esto quedan cerradas 3 de las 4
validaciones de la sección 6.

**Ejecución NO autorizada.** Falta la validación 1 —contraste contra el modelo
vivo— que el propio usuario fijó como condición previa a cualquier
modificación. Permanece bloqueada: Power BI Desktop no está abierto y el
servidor MCP de modelado no conecta (verificado 2026-09-03).

No se ha modificado ninguna medida, visual, consulta Power Query ni archivo del
modelo semántico.

### Qué desbloquea la ejecución

1. Abrir `PBIP/Proyecto7.pbip` en Power BI Desktop (o restablecer el MCP de
   modelado).
2. Ejecutar la línea base **V0**: capturar por periodo `Tot_Colab-Sena`,
   `Tot_Colab-Directos`, `Tasa Ausentismo_EL`, `Efic_Emp` e `Índice_Retiros`.
3. Contrastar V0 contra los conteos de `Specs/0029`. **Criterio de paso:**
   `Tot_Colab-Sena` corregido debe coincidir **exactamente** con
   `Planta Ppto[Total-Sena]` en los 31 meses comunes (2024-01 → 2026-07), según
   la conciliación independiente del 2026-09-03.
4. Con V0 capturada y contrastada, autorizar V1 en el orden ya fijado por el
   usuario: primero `Tot_Colab-Directos`, después `Tot_Colab-Sena`.
