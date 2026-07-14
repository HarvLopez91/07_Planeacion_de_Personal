# Plan de implementacion - Matriz de antiguedad al retiro

Fecha: 2026-07-14

Proyecto: `07_Planeacion_de_Personal`

PBIP: `PBIP/Proyecto7.pbip`

Pagina objetivo: `Retiros`

Spec base aprobada: `Specs/0002_analisis_impacto_matriz_antiguedad_retiros.md`

Estado: plan de implementacion. No implementa cambios en PBIP.

## 1. Titulo

Plan de implementacion para incorporar una matriz de antiguedad del personal retirado en la pagina `Retiros`.

## 2. Objetivo

Definir una ruta de implementacion segura, trazable y por fases para agregar en la pagina `Retiros` una matriz con:

- Filas: rango de antiguedad al retiro.
- Columnas: anio.
- Valores: total de retiros o personas retiradas, segun validacion funcional.

El plan evita modificar PBIP en esta fase y deja listas las decisiones, validaciones, riesgos y criterios de aceptacion que deben cumplirse antes de implementar.

## 3. Alcance

Este plan cubre:

- Validacion funcional de la antiguedad al retiro.
- Diseno de logica de modelo para clasificar rangos.
- Implementacion futura minima del modelo, si se aprueba.
- Implementacion futura de la matriz en la pagina `Retiros`.
- Validacion visual y funcional en Power BI Desktop.
- Documentacion, trazabilidad, estrategia de commits y rollback.

## 4. Fuera de alcance

Queda fuera de alcance en esta fase:

- Modificar `PBIP/`.
- Modificar archivos TMDL.
- Crear o modificar `visual.json`.
- Modificar `pages.json`, bookmarks, slicers, filtros o `activePageName`.
- Crear la visual de matriz.
- Modificar `Docs/`, `Outputs/`, `README.md`, `AGENTS.md` o `CLAUDE.md`.
- Exponer datos personales o registros individuales.
- Hacer push.
- Usar comandos destructivos.

## 5. Insumo aprobado

La base aprobada es la Spec `0002`, que establece:

- La matriz debe ubicarse en la pagina `Retiros`.
- La referencia visual es la matriz existente en `Demografico (Promedio)`, solo como guia de diseno compacto.
- No debe usarse directamente `PLANTA DE PERSONAL[Rango Antigüedad]` para explicar retiros.
- Debe validarse si `Ppto Retiros[Meses de permanencia]` representa de forma confiable la antiguedad al retiro.
- Tipo de retiro, empresa, dependencia, area o unidad de negocio deben operar como filtros o segmentadores, no como columnas principales.

## 6. Decisiones funcionales pendientes

Antes de implementar se deben aprobar estas decisiones:

| Decision | Opciones | Responsable sugerido | Bloquea fase |
|---|---|---|---|
| Definicion de antiguedad al retiro | `Meses de permanencia` o calculo desde fechas | People Analytics / Gestion Humana | Fase 2 |
| Grano de conteo | Eventos de retiro o personas retiradas unicas | People Analytics / Gestion Humana | Fase 3 |
| Fecha oficial de retiro | `Fecha Vencimiento` u otra fecha validada | People Analytics / fuente funcional | Fase 2 |
| Medida de valores | `[Tot_Retiros]` o nueva medida `Personas_Retiradas` | Arquitectura Power BI | Fase 3 |
| Ubicacion exacta del visual | Zona disponible en pagina `Retiros` | UX dashboard / usuario funcional | Fase 4 |
| Manejo de nulos o permanencias invalidas | Excluir, agrupar o mostrar como `Sin clasificar` | People Analytics | Fase 3 |

## 7. Plan por fases

### Fase 1 - Validacion funcional de antiguedad al retiro

**Objetivo:** confirmar si `Ppto Retiros[Meses de permanencia]` representa antiguedad al retiro y si el grano de conteo debe ser eventos o personas.

**Tareas:**

- Revisar definicion funcional de `Meses de permanencia`.
- Validar si el campo esta calculado al momento del retiro.
- Revisar nulos, textos no numericos, valores negativos, ceros, valores extremos y formatos inconsistentes.
- Validar si cada fila de `Ppto Retiros` representa un evento de retiro.
- Confirmar si hay personas con mas de un retiro o mas de una fila.
- Definir si el valor de la matriz sera `[Tot_Retiros]` o conteo distinto de personas retiradas.

**Archivos afectados:** ninguno en esta fase. Solo diagnostico de datos/modelo.

**Riesgos:**

- Confundir permanencia historica con antiguedad actual.
- Contar eventos cuando el usuario espera personas unicas.
- Excluir o incluir nulos sin criterio funcional.

**Validaciones:**

- Perfilamiento agregado del campo, sin exponer registros individuales.
- Comparacion de conteo total contra `[Tot_Retiros]`.
- Revision de duplicados por identificacion de forma agregada.

**Criterio de aceptacion:**

- Queda documentado si `Meses de permanencia` es valido para antiguedad al retiro.
- Queda aprobado el grano de conteo: eventos o personas unicas.
- Queda definido el tratamiento de nulos y atipicos.

**Decision requerida antes de avanzar:**

- Aprobacion funcional de la fuente de antiguedad y de la medida base.

### Fase 2 - Diseno de logica de modelo

**Objetivo:** definir la logica de modelo que se implementara, sin modificar todavia TMDL ni Power Query.

**Tareas:**

- Definir si la antiguedad al retiro se calculara desde `Meses de permanencia` o desde fechas.
- Proponer columna `Rango_Antiguedad_Retiro`.
- Proponer columna `Orden_Rango_Antiguedad_Retiro`, si se requiere ordenamiento independiente.
- Definir etiquetas de rangos con nombres tecnicos estables y sin caracteres especiales.
- Definir medida de valor para la matriz.
- Confirmar si se requiere categoria `Sin clasificar`.

**Archivos afectados:** ninguno en esta fase. Se prepara diseno, no implementacion.

**Riesgos:**

- Crear logica duplicada respecto a la existente en `PLANTA DE PERSONAL`.
- Diseñar rangos que no coincidan con la lectura corporativa vigente.
- Omitir ordenamiento y dejar la matriz ordenada alfabeticamente.

**Validaciones:**

- Revision del diseno contra la Spec 0002.
- Confirmacion de rangos esperados.
- Confirmacion de que no se usara directamente `PLANTA DE PERSONAL[Rango Antigüedad]`.

**Criterio de aceptacion:**

- Logica de rangos aprobada.
- Medida objetivo aprobada.
- Tratamiento de valores invalidos aprobado.

**Decision requerida antes de avanzar:**

- Aprobacion del diseno de columna/rango y de la medida a implementar.

### Fase 3 - Implementacion minima de modelo

**Objetivo:** implementar solo lo necesario en el modelo para soportar la matriz, si las fases 1 y 2 quedan aprobadas.

**Tareas:**

- Crear rango de antiguedad al retiro en `Ppto Retiros`.
- Crear columna de orden del rango, si aplica.
- Crear o validar la medida de valor para la matriz.
- Validar que los totales por anio coincidan con `[Tot_Retiros]` o con la medida aprobada.
- Validar que filtros de anio, mes, empresa, area, dependencia y tipo de retiro sigan funcionando.

**Archivos potencialmente afectados:**

- `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl`
- `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl`, si se crea nueva medida.
- `PBIP/Proyecto.SemanticModel/definition/cultures/**`, solo si Power BI genera metadata necesaria.

**Riesgos:**

- Error de parseo TMDL.
- Conversion incorrecta de texto a numero o fecha.
- Cambios automaticos en culturas o metadata no relacionados.

**Validaciones:**

- Abrir `Proyecto7.pbip` en Power BI Desktop sin errores.
- Validar totales por anio.
- Validar orden de rangos.
- Ejecutar `git diff --check`.
- Revisar diff exacto de los TMDL modificados.

**Criterio de aceptacion:**

- El modelo soporta la matriz sin usar `PLANTA DE PERSONAL[Rango Antigüedad]`.
- Los totales por anio coinciden con la medida validada.
- No hay cambios no relacionados en el modelo.

**Decision requerida antes de avanzar:**

- Aprobacion de diagnostico posterior al cambio de modelo y autorizacion para crear la visual.

### Fase 4 - Implementacion visual en pagina Retiros

**Objetivo:** crear la matriz en la pagina `Retiros` sin afectar visuales existentes.

**Tareas:**

- Crear visual tipo matriz/pivotTable en la pagina `Retiros`.
- Configurar filas con `Rango_Antiguedad_Retiro`.
- Configurar columnas con anio.
- Configurar valores con la medida aprobada.
- Aplicar estilo compacto similar a la matriz de `Demografico (Promedio)`.
- Ubicar el visual en una zona validada de la pagina.
- Evitar cambios en slicers, bookmarks, `pages.json`, `activePageName` y visuales no relacionados.

**Archivos potencialmente afectados:**

- `PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405/visuals/<nuevo_visual>/visual.json`
- `PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405/page.json`, solo si Power BI lo modifica de forma necesaria.

**Riesgos:**

- Saturar la pagina `Retiros`.
- Power BI Desktop puede modificar visuales o bookmarks no relacionados.
- La matriz puede no heredar correctamente filtros existentes.

**Validaciones:**

- Comparar visualmente contra referencia de `Demografico (Promedio)`.
- Validar que no se desplacen visuales existentes.
- Revisar diff PBIR y separar ruido.
- Validar que solo el nuevo visual y metadata necesaria queden candidatos para commit.

**Criterio de aceptacion:**

- La matriz muestra filas por rango, columnas por anio y valores aprobados.
- El estilo es compacto y legible.
- No se rompen visuales existentes.

**Decision requerida antes de avanzar:**

- Aprobacion visual del usuario y autorizacion para preparar staging selectivo.

### Fase 5 - Validacion visual y funcional

**Objetivo:** confirmar que la implementacion funciona en Power BI Desktop y respeta la experiencia del dashboard.

**Tareas:**

- Abrir `PBIP/Proyecto7.pbip` en Power BI Desktop.
- Validar filtros de anio, mes, empresa, area, dependencia y tipo de retiro.
- Validar que los totales por anio coincidan con la medida aprobada.
- Validar que los rangos se ordenen correctamente.
- Validar que no se rompieron visuales existentes.
- Validar que no se agregaron cambios accidentales de slicers o bookmarks.

**Archivos afectados:** ninguno adicional esperado. Esta fase revisa cambios ya generados.

**Riesgos:**

- Detectar diferencias entre totales del modelo y lectura visual.
- Encontrar ruido PBIR mezclado con el cambio real.
- Requerir ajuste de layout.

**Validaciones:**

- Revision visual en Power BI Desktop.
- `git status --short -- PBIP/`
- `git diff --stat -- PBIP/`
- `git diff --check`

**Criterio de aceptacion:**

- El usuario confirma que la visual responde al requerimiento funcional.
- Se identifican los archivos minimos para commit.
- No se incluyen cambios no relacionados.

**Decision requerida antes de avanzar:**

- Aprobacion del set de archivos candidatos para staging.

### Fase 6 - Documentacion y trazabilidad

**Objetivo:** cerrar la implementacion con documentacion, evidencia y commits separados.

**Tareas:**

- Actualizar `Docs/DATA_MODEL.md` si se crea columna o medida.
- Actualizar `Docs/PROJECT_CONTEXT.md` si aplica.
- Actualizar `Docs/CHANGELOG.md` si aplica y existe convencion vigente.
- Crear output de diagnostico posterior, si el usuario lo solicita.
- Preparar commits separados por alcance.

**Archivos potencialmente afectados:**

- `Docs/DATA_MODEL.md`
- `Docs/PROJECT_CONTEXT.md`
- `Docs/CHANGELOG.md`, si existe y aplica.
- `Outputs/<diagnostico>.md`, si se solicita como evidencia no versionada o temporal.

**Riesgos:**

- Documentar mas de lo implementado.
- Mezclar documentacion con cambios PBIP pendientes.
- Versionar evidencia temporal no aprobada.

**Validaciones:**

- Revisar que la documentacion refleje solo cambios aprobados.
- Validar staging selectivo.
- Validar `git diff --cached --name-status`.
- Validar `git diff --cached --check`.

**Criterio de aceptacion:**

- Documentacion coherente con la implementacion aprobada.
- Commits separados y trazables.
- No hay archivos ajenos al alcance en staging.

**Decision requerida antes de avanzar:**

- Aprobacion de commit y, en una decision separada, aprobacion de push.

## 8. Archivos potencialmente afectados

| Fase | Archivos | Tipo de impacto |
|---|---|---|
| 1 | Ninguno | Diagnostico funcional solamente. |
| 2 | Ninguno | Diseno tecnico solamente. |
| 3 | `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl` | Columna de rango y posible columna de orden. |
| 3 | `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl` | Nueva medida si se aprueba conteo distinto o porcentaje. |
| 3 | `PBIP/Proyecto.SemanticModel/definition/cultures/**` | Metadata generada por Power BI, solo si es necesaria. |
| 4 | `PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405/visuals/<nuevo_visual>/visual.json` | Nueva matriz en pagina `Retiros`. |
| 4 | `PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405/page.json` | Metadata de pagina, solo si Power BI la modifica de forma necesaria. |
| 5 | Ninguno adicional esperado | Validacion visual y funcional. |
| 6 | `Docs/DATA_MODEL.md`, `Docs/PROJECT_CONTEXT.md`, `Docs/CHANGELOG.md` | Documentacion, si aplica. |

Archivos que deben evitarse salvo evidencia y aprobacion explicita:

- `PBIP/Proyecto.Report/definition/bookmarks/**`
- `PBIP/Proyecto.Report/definition/pages/pages.json`
- `PBIP/Proyecto.SemanticModel/diagramLayout.json`
- Visuales no relacionados de otras paginas.
- Slicers de anio/mes.
- `activePageName`.

## 9. Validaciones por fase

| Fase | Validaciones minimas |
|---|---|
| 1 | Perfil agregado de permanencia, nulos, atipicos, duplicados y grano de retiro. |
| 2 | Revision de logica propuesta contra Spec 0002 y aprobacion funcional. |
| 3 | Apertura en Power BI Desktop, totales por anio, orden de rangos, `git diff --check`. |
| 4 | Validacion visual, no desplazamiento de visuales existentes, diff PBIR acotado. |
| 5 | Filtros de anio, mes, empresa, area, dependencia y tipo de retiro; totales por anio. |
| 6 | Staging selectivo, commits separados, documentacion coherente. |

## 10. Criterios de aceptacion

La implementacion completa se considerara aceptada si:

- La matriz esta en la pagina `Retiros`.
- Las filas corresponden a rango de antiguedad al retiro.
- Las columnas corresponden a anio.
- Los valores corresponden a `[Tot_Retiros]` o a la medida aprobada de personas retiradas.
- Los totales por anio coinciden con la medida validada bajo los mismos filtros.
- Los rangos estan ordenados correctamente.
- La visual responde a filtros de anio, mes, empresa, area, dependencia y tipo de retiro.
- No se usa directamente `PLANTA DE PERSONAL[Rango Antigüedad]`.
- No se mezclan cambios de bookmarks, slicers, `activePageName`, `diagramLayout` o visuales no relacionados.
- Power BI Desktop abre el PBIP sin errores.
- El cambio queda separado en commits controlados.

## 11. Estrategia de commits

Estrategia recomendada:

1. Commit 1 - documentacion de planeacion:
   - `Specs/0002_analisis_impacto_matriz_antiguedad_retiros.md`
   - `Specs/0003_plan_implementacion_matriz_antiguedad_retiros.md`
2. Commit 2 futuro - modelo:
   - cambios minimos en `Ppto Retiros.tmdl`, `Tbl_Medidas.tmdl` y metadata estrictamente necesaria.
3. Commit 3 futuro - visual:
   - nuevo visual de matriz en pagina `Retiros` y metadata de pagina estrictamente necesaria.
4. Commit 4 futuro - documentacion:
   - `Docs/DATA_MODEL.md`, `Docs/PROJECT_CONTEXT.md`, `Docs/CHANGELOG.md`, si aplica.

Reglas:

- No usar `git add .`.
- No mezclar PBIP con Specs o Docs salvo aprobacion expresa.
- Validar `git diff --cached --name-status` antes de cada commit.
- Mantener push como aprobacion separada.

## 12. Plan de rollback

| Alcance | Rollback recomendado |
|---|---|
| Specs | Revertir el commit documental si el plan deja de estar aprobado. |
| Modelo | Revertir el commit de modelo y validar reapertura de PBIP. |
| Visual | Revertir el commit visual y validar que la pagina `Retiros` vuelva al estado anterior. |
| Documentacion | Revertir o corregir la documentacion afectada. |
| Ruido PBIP no stageado | No incluirlo en commits; mantenerlo fuera del alcance. |

Si hay cambios acumulados en PBIP, evitar comandos destructivos globales. Cualquier rollback debe hacerse por commit o por archivo aprobado.

## 13. Recomendacion de push

No hacer push en esta fase sin aprobacion explicita posterior.

Recomendacion:

1. Crear el commit documental de Specs.
2. Mantenerlo local.
3. Solicitar aprobacion del usuario para push cuando se decida publicar la trazabilidad del plan.
4. Antes del push, revisar cuantas confirmaciones locales estan pendientes frente a `origin/main`.

## 14. Riesgos y mitigaciones

| Riesgo | Nivel | Mitigacion |
|---|---|---|
| `Meses de permanencia` no representa antiguedad al retiro | Alto | Validar funcionalmente antes de disenar el modelo. |
| Conteo incorrecto por duplicados de persona | Alto | Definir si la matriz cuenta eventos o personas unicas. |
| Uso indebido de `PLANTA DE PERSONAL[Rango Antigüedad]` | Alto | Crear rango propio en `Ppto Retiros`. |
| Ruido de Power BI Desktop en PBIP | Alto | Diagnosticar diff despues de cada guardado y stagear rutas exactas. |
| Saturacion visual de pagina `Retiros` | Medio | Validar ubicacion y legibilidad antes de commit visual. |
| Orden incorrecto de rangos | Medio | Crear columna de orden o prefijos estables. |
| Documentacion desalineada | Medio | Actualizar Docs solo despues de implementacion aprobada. |
| Push prematuro | Medio | Mantener push como decision separada. |

## 15. Siguiente paso recomendado

Ejecutar la Fase 1 como diagnostico funcional y tecnico de datos, sin modificar PBIP:

```text
Diagnostica si Ppto Retiros[Meses de permanencia] representa antiguedad al retiro, valida nulos, formatos, atipicos y duplicados agregados, y recomienda si la matriz debe usar Tot_Retiros o personas retiradas unicas. No modifiques PBIP ni hagas staging.
```
