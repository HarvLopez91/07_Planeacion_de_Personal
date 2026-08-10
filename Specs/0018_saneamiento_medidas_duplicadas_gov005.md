# Saneamiento estructural de medidas duplicadas (GOV-005)

Fecha: 2026-08-10

Estado: Cerrado (2026-08-10). GATE 5 (apertura real en Power BI Desktop desde checkout limpio) confirmó carga sin `PFE_TM_OBJECT_NAME_ALREADY_EXISTS`, 122 medidas / 66 relaciones / 52 tablas, 0 duplicados en vivo. Ver sección 7.

Iniciativa independiente de `Specs/0016_renombramiento_medidas_rotacion_retiros.md` (DAX-002, ya fusionada a `main`) y de `Specs/0017_correccion_codificacion_union_libre_demografico.md` (Unión Libre, en validación). No comparte alcance, archivos ni rama con PR #4 (Contratos Kactus).

## 1. Causa raíz

Al intentar abrir un checkout limpio de `origin/main` en Power BI Desktop (auditoría post-GATE 5 de DAX-002, PR #5), Desktop rechazó cargar el modelo con el error `PFE_TM_OBJECT_NAME_ALREADY_EXISTS`, señalando primero `Tot_Accidentes` y, tras retirarlo temporalmente en un worktree desechable, `ConteoP`. Ambos son **defectos preexistentes de `origin/main`**, no introducidos por DAX-002 ni por esta iniciativa.

## 2. Inventario inicial (confirmado sobre `origin/main` en `96cff2a`, post-merge de PR #5)

- 148 medidas totales en `PBIP/Proyecto.SemanticModel/definition/tables/*.tmdl`.
- **27 nombres de medida declarados dos veces**: una copia en su tabla de dominio (`AUSENTISMOS`, `SST GENERAL`, `Ppto Ingresos`, `Selección Grupo Lemco`, `Selección Challenger`, `SENA UNIDADES`, `ACCIDENTALIDAD`) y otra copia en `Tbl_Medidas`.
- Las 27 comparten el mismo `lineageTag` entre ambas copias (0 discrepancias de lineageTag).
- **20 con fórmula idéntica** entre ambas copias, **7 con fórmula textualmente diferente** bajo el mismo `lineageTag`.

Esta línea base coincide exactamente con la documentada en `Specs/0016` sección 14 (auditoría del PR #5); se reconfirmó de forma independiente sobre el `origin/main` actualizado (post-merge) antes de implementar, sin diferencias.

## 3. Tabla canónica elegida por duplicado

Criterio aplicado: se conserva la copia efectivamente referenciada por visuales del reporte; se elimina la copia con 0 referencias, preservando fórmula y `lineageTag` de la copia conservada. Verificado además que ningún visual, bookmark, medida ni entrada de cultura (`es-ES.tmdl`) depende de la copia eliminada.

| Medida | Tabla conservada | Tabla eliminada | Fórmula | Referencias en la copia conservada |
|---|---|---|---|---|
| `%AusM` | `AUSENTISMOS` | `Tbl_Medidas` | Idéntica | 3 |
| `%Cumplimiento` | `SENA UNIDADES` | `Tbl_Medidas` | Idéntica | 6 |
| `Ausentismo` | `AUSENTISMOS` | `Tbl_Medidas` | Idéntica | 5 |
| `CHombres` | `AUSENTISMOS` | `Tbl_Medidas` | Idéntica | 0 (sin consumidor visual; ver nota) |
| `CMujeres` | `AUSENTISMOS` | `Tbl_Medidas` | Idéntica | 0 (sin consumidor visual; ver nota) |
| `ConteoP` | `AUSENTISMOS` | `Tbl_Medidas` | Idéntica | 15 |
| `DIAS_AUSENTISMO` | `AUSENTISMOS` | `Tbl_Medidas` | Idéntica | 0 (sin consumidor visual; ver nota) |
| `Dias Ausentismo Acc.Lab` | `SST GENERAL` | `Tbl_Medidas` | Idéntica | 0 (sin consumidor visual; ver nota) |
| `Ind_opor` | `Selección Grupo Lemco` | `Tbl_Medidas` | Idéntica | 5 |
| `Ingresos_Calidad` | `Ppto Ingresos` | `Tbl_Medidas` | Idéntica | 6 |
| `MSector` | `SST GENERAL` | `Tbl_Medidas` | Idéntica | 1 |
| `M_Frecuencia` | `SST GENERAL` | `Tbl_Medidas` | Idéntica | 3 |
| `M_Severidad` | `SST GENERAL` | `Tbl_Medidas` | Idéntica | 7 |
| `Ret_Calidad` | `Ppto Ingresos` | `Tbl_Medidas` | Idéntica | 6 |
| `Solicitud` | `Selección Grupo Lemco` | `Tbl_Medidas` | Idéntica | 11 |
| `Solicitudes` | `Selección Challenger` | `Tbl_Medidas` | Idéntica | 0 (sin consumidor visual; referenciada internamente por `Solicitudes2024`, ver sección 5) |
| `Solicitudes2024` | `Selección Challenger` | `Tbl_Medidas` | Idéntica | 0 (sin consumidor visual; ver nota) |
| `Tasa_Acc` | `SST GENERAL` | `Tbl_Medidas` | Idéntica | 1 |
| `Tot_Accidentes` | **`Tbl_Medidas`** | **`ACCIDENTALIDAD`** | Idéntica | 7 (único caso invertido: la copia usada por el reporte es la de `Tbl_Medidas`) |
| `Tot_ingresos` | `Ppto Ingresos` | `Tbl_Medidas` | Idéntica | 0 (sin consumidor visual; referenciada internamente por `Índice_Rotación`, ver sección 5) |
| `Ind_Calidad` | `Ppto Ingresos` | `Tbl_Medidas` | **Diferente** | 9 |
| `Ind_Calidad_2025` | `Ppto Ingresos` | `Tbl_Medidas` | **Diferente** | 4 |
| `Ing_Calidad_2025` | `Ppto Ingresos` | `Tbl_Medidas` | **Diferente** | 2 |
| `Tasa Ausentismo` | `AUSENTISMOS` | `Tbl_Medidas` | **Diferente** | 1 |
| `Tasa Ausentismo_EL` | `AUSENTISMOS` | `Tbl_Medidas` | **Diferente** | 2 |
| `Tasa_Ausent_Anual` | `AUSENTISMOS` | `Tbl_Medidas` | **Diferente** | 2 |
| `ret_Calidad_2025` | `Ppto Ingresos` | `Tbl_Medidas` | **Diferente** | 2 |

Nota sobre las 7 filas sin consumidor visual (`CHombres`, `CMujeres`, `DIAS_AUSENTISMO`, `Dias Ausentismo Acc.Lab`, `Solicitudes`, `Solicitudes2024`, `Tot_ingresos`): ningún visual del reporte referencia ninguna de las dos copias. Se aplicó el mismo criterio general (conservar la tabla de dominio) por consistencia con el resto del inventario, dado que la elección es funcionalmente neutra (ninguna copia está en uso) y mantiene cada medida en su tabla semánticamente propia.

## 4. Auditoría de dependencias cruzadas (antes de eliminar)

Se buscó, en el texto completo de todas las medidas del modelo, toda referencia interna `[NombreMedida]` a cada uno de los 27 nombres, para descartar que alguna medida distinta dependiera específicamente de la copia a eliminar:

- `Solicitudes2024` (ambas copias) referencia `[Solicitudes]` — resuelve igual sin importar cuál copia de `Solicitudes` sobreviva, por ser una referencia no cualificada por tabla.
- `Índice_Rotación` (medida preexistente de `Tbl_Medidas`, distinta de `Indice_Rotacion` de DAX-002) referencia `[Tot_ingresos]` — mismo caso.
- `Ind_Calidad_2025` (ambas copias) referencia `[Ing_Calidad_2025]` y `[ret_Calidad_2025]` — mismo caso, y las tres pertenecen al mismo grupo de duplicados resuelto de forma consistente (las tres se conservan en `Ppto Ingresos`).

No se encontró ninguna referencia cruzada que dependiera exclusivamente de la copia eliminada. Los nombres de medida son objetos de alcance global en el modelo tabular (no se cualifican por tabla en las fórmulas DAX), por lo que estas referencias internas se resuelven correctamente tras la consolidación.

## 5. Tratamiento de las 7 definiciones divergentes

Para cada una de las 7 (`Ind_Calidad`, `Ind_Calidad_2025`, `Ing_Calidad_2025`, `Tasa Ausentismo`, `Tasa Ausentismo_EL`, `Tasa_Ausent_Anual`, `ret_Calidad_2025`) se verificaron las 4 condiciones requeridas antes de proceder:

1. Una de las dos copias es claramente la utilizada — **sí**, la de la tabla de dominio (1-9 referencias cada una).
2. La otra copia tiene 0 consumidores — **sí**, la de `Tbl_Medidas` en los 7 casos.
3. El `lineageTag` es el mismo entre ambas copias — **sí**, confirmado (0 discrepancias en las 27).
4. Eliminar la copia no utilizada preserva todas las dependencias — **sí**, verificado en la sección 4 (sin referencias cruzadas huérfanas).

Cumplidas las 4 condiciones, se determinó la ubicación canónica y se eliminó la copia de `Tbl_Medidas` **sin modificar la fórmula ni el `lineageTag` de la copia conservada** (tabla de dominio). No se intentó unificar ni "corregir" la divergencia textual entre ambas fórmulas — esa divergencia queda resuelta por eliminación de la copia no usada, no por reconciliación de lógica de negocio.

## 6. Garantía de no alteración de fórmulas de negocio

- No se modificó ninguna fórmula DAX de las 27 medidas conservadas.
- No se modificó ningún `lineageTag`.
- No se renombró ninguna medida.
- No se tocó ningún visual, bookmark, relación, columna ni consulta Power Query.
- Los únicos 2 archivos modificados son `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl` (26 bloques de medida eliminados) y `PBIP/Proyecto.SemanticModel/definition/tables/ACCIDENTALIDAD.tmdl` (1 bloque eliminado: `Tot_Accidentes`).

## 7. Validaciones ejecutadas

- Reinventario completo tras el saneamiento: 121 medidas (148 − 27), **0 nombres duplicados**.
- Las 27 medidas canónicas confirmadas presentes con su `lineageTag` original (verificación puntual de `Tot_Accidentes` y `ConteoP`, más barrido completo de coincidencia de nombre único).
- Balance de paréntesis/llaves de `Tbl_Medidas.tmdl` (449/449, 33/33) y `ACCIDENTALIDAD.tmdl`: balanceado.
- Búsqueda de referencias rotas en `PBIP/Proyecto.Report/`: 0 referencias a `Tbl_Medidas.<nombre-eliminado>` para las 26 medidas retiradas de `Tbl_Medidas`, y 0 referencias a `ACCIDENTALIDAD.Tot_Accidentes`.
- `git status` del worktree: únicamente los 2 archivos indicados, sin cambios en `Docs/`, `Specs/` (fuera de esta Spec), visuales, bookmarks ni relaciones.
- **GATE 5 — apertura real en Power BI Desktop desde checkout limpio (2026-08-10): PASS.** Worktree desechable creado exactamente sobre la rama `fix/gov-005-saneamiento-medidas-duplicadas` con el saneamiento aplicado; `Proyecto7.pbip` abrió sin el error `PFE_TM_OBJECT_NAME_ALREADY_EXISTS` (título de ventana "Proyecto7" confirmado, a diferencia de los intentos previos bloqueados). Conteo real observado en vivo vía `powerbi-modeling-mcp`: **122 medidas, 66 relaciones, 52 tablas, 0 nombres duplicados** (verificado con consulta DAX de agrupación por nombre). No se impone el conteo histórico de 129 ni 149 (correspondientes a instancias previas no comparables). Nota de reconciliación: el reinventario estático previo a la apertura había estimado 121 medidas (148 − 27); el conteo en vivo, confirmado también por conteo directo de bloques `measure` en el archivo, es 122 (96 en `Tbl_Medidas` + 26 en tablas de dominio) — la estimación previa de 148 subestimó en 1 el total original; no afecta el resultado del saneamiento, ya verificado como 0 duplicados en ambos métodos. Las tablas cargaron sin filas (0 registros) por tratarse de un checkout limpio sin refresh de datos — comportamiento esperado y fuera de alcance de GOV-005, no relacionado con el saneamiento de medidas. Power BI Desktop cerrado sin guardar al finalizar; `git status` del worktree confirmado sin cambios adicionales tras la apertura.

## 8. Riesgo residual

- Las 7 filas sin consumidor visual actual (sección 3) quedaron en su tabla de dominio por consistencia, no por evidencia de uso — si en el futuro se detecta que alguna de ellas debía vivir en `Tbl_Medidas` por convención de mantenimiento, es una decisión de estilo, no funcional (ninguna estaba en uso).
- No se investigó por qué existían estas 27 duplicidades en primer lugar (probable copia histórica de medidas hacia `Tbl_Medidas` sin retirar el original) — queda fuera de alcance determinar el origen exacto.
- Esta Spec no toca la desagregación pendiente de `PBIP-005` ni la deuda funcional de `Índice_Retiros` documentada en `Specs/0016` sección 12.
