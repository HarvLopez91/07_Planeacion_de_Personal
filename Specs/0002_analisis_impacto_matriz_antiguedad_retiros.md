# 1. Titulo

Analisis de impacto para incorporar una matriz de antiguedad en la pagina Retiros del proyecto Power BI PBIP `Proyecto7.pbip`.

Fecha de elaboracion: 2026-07-14

Proyecto: `07_Planeacion_de_Personal`

Archivo PBIP: `PBIP/Proyecto7.pbip`

Estado: especificacion de diagnostico. No implementa cambios en PBIP.

## 2. Objetivo

Evaluar el impacto funcional, tecnico y de control de cambios de agregar una matriz en la pagina `Retiros` que permita analizar los retiros por rango de antiguedad al retiro y por anio, tomando como referencia visual la matriz creada en `Demografico (Promedio)` para antiguedad de colaboradores.

La matriz requerida debe tener esta estructura funcional:

- Filas: rango de antiguedad al retiro.
- Columnas: anio.
- Valores: total de retiros o personas retiradas, segun validacion funcional.

El objetivo de esta Spec es dejar una base de decision antes de modificar el reporte, el modelo semantico o los visuales PBIR.

## 3. Alcance

Esta especificacion cubre:

- Identificacion de la pagina `Retiros`.
- Identificacion de la matriz de referencia en `Demografico (Promedio)`.
- Revision conceptual de campos y medidas candidatos en el modelo semantico.
- Evaluacion de alternativas para calcular antiguedad de personas retiradas.
- Recomendacion de diseno para una futura matriz con filas por rango de antiguedad al retiro, columnas por anio y valores de retiros o personas retiradas.
- Analisis de impacto tecnico, riesgos, criterios de aceptacion, validaciones y estrategia de commits.

## 4. Fuera de alcance

Queda explicitamente fuera de alcance en esta fase:

- Crear, mover o modificar visuales en `PBIP/`.
- Editar `visual.json`, `pages.json`, bookmarks, slicers, filtros, `activePageName` o `diagramLayout`.
- Modificar archivos TMDL o el modelo semantico.
- Crear medidas, columnas calculadas o pasos Power Query.
- Exponer datos personales o registros individuales.
- Preparar staging, commit o push.
- Definir valores finales de negocio sin validacion funcional.

## 5. Contexto funcional

La pagina `Retiros` consolida analitica de retiros, rotacion y participacion por tipo de retiro, dependencia, area, cargo, nivel, empresa y periodo. La necesidad planteada es agregar una matriz que permita responder como se distribuyen los retiros por rango de antiguedad.

La matriz de referencia existente en `Demografico (Promedio)` analiza antiguedad de colaboradores activos o poblacion promedio, no retiros. Por lo tanto, debe reutilizarse como referencia de diseno visual, pero no necesariamente como referencia directa de calculo.

Para People Analytics, el concepto correcto debe distinguir entre:

- Antiguedad de colaboradores activos en un periodo.
- Antiguedad al momento del retiro.
- Permanencia acumulada segun fuente historica de retiros.

La decision funcional pendiente es si la matriz debe contar eventos de retiro, personas retiradas unicas o participacion porcentual por rango.

## 6. Estado actual de la pagina Retiros

Pagina identificada:

| Atributo | Valor |
|---|---|
| Carpeta PBIR | `PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405/` |
| Display name | `Retiros` |
| Tamano de pagina | 1800 x 1000 |
| Visuales identificados | 33 |
| Estado tecnico | Pagina con alto volumen de visuales y cambios PBIP acumulados en el repositorio |

Visuales relevantes revisados en modo solo lectura:

| Visual | Archivo | Hallazgo |
|---|---|---|
| Retiros por Dependencia / Cargo / Nivel | `visuals/7152010273d50604a972/visual.json` | Usa `Ppto Retiros[Nivel]`, `Ppto Retiros[Cargo]` y `Tbl_Medidas[Tot_Retiros]`. |
| Retiros por Area | `visuals/c240f7297edc1325fa6d/visual.json` | Usa `Ppto Retiros[Area]`, `Tbl_Medidas[Tot_Retiros]` y `Tbl_Medidas[Retiros_Voluntarios]`. |
| Retiros por Dependencia | `visuals/4d0981eda8a981c39b17/visual.json` | Usa `Ppto Retiros[Dependencia]` y `Tbl_Medidas[Tot_Retiros]`. |
| Retiros por Tipo de Contratacion | `visuals/4368c3663556095b3416/visual.json` | Usa `Ppto Retiros[Clase de nomina (grupos)]`, `Tbl_Medidas[Tot_Retiros]` y calculo de participacion. |
| Comparativo Retiros Mensual | `visuals/4594ad02ed09260c2d80/visual.json` | Usa `Planta Ppto[Retiros]`. |
| Comparativo Retiros Trimestre | `visuals/b643ab53000f0588a188/visual.json` | Usa `Planta Ppto[Retiros]`. |
| Retiros segun tipo / cargo / nivel | `visuals/b72099f821538078c4a0/visual.json` | Usa `Tbl_Medidas[Retiros_Segun_Tipo]`, `Tbl_Medidas[Ind_Retiros]`, `Ppto Retiros[Cargo]` y `Ppto Retiros[Nivel]`. |

Lectura de impacto:

- La pagina ya esta densa y debe validarse visualmente antes de agregar una matriz.
- El nuevo visual podria competir con graficos existentes de dependencia, tipo de contratacion o comparativos.
- Si se implementa desde Power BI Desktop, es probable que Power BI genere ruido adicional en `visual.json`, bookmarks, `activePageName` o metadata de pagina.

## 7. Matriz de referencia en Demografico (Promedio)

Matriz identificada:

| Atributo | Valor |
|---|---|
| Pagina | `Demografico (Promedio)` |
| Carpeta pagina | `PBIP/Proyecto.Report/definition/pages/ReportSectionf46593dd92bf9359ceef/` |
| Archivo visual | `visuals/c195409a3a3b26b35df7/visual.json` |
| Tipo de visual | `pivotTable` |
| Posicion aproximada | X 18.01, Y 696.14, W 709.01, H 191.73 |
| Campo de filas | `PLANTA DE PERSONAL[Rango Antigüedad]` |
| Medida de valores | `Tbl_Medidas[Tot_empleados_Promedio]` |
| Uso recomendado | Referencia de formato compacto, no referencia directa de calculo para retiros |

La matriz de referencia esta asociada a poblacion activa/promedio y no a retiros. Por eso, copiarla sin adaptar el origen de datos produciria una lectura funcional incorrecta para la pagina `Retiros`.

Esta matriz debe mantenerse solo como referencia visual de formato compacto. No debe usarse directamente `PLANTA DE PERSONAL[Rango Antigüedad]` para explicar retiros, porque ese campo describe antiguedad de planta activa o snapshot y no necesariamente antiguedad del personal al momento de retiro.

## 8. Estado actual del modelo de datos

Tablas relevantes:

| Tabla | Rol actual | Hallazgos |
|---|---|---|
| `Ppto Retiros` | Fuente principal de eventos o registros de retiros | Contiene campos de persona, empresa, fecha inicio, fecha vencimiento, anio, mes, dependencia, area, nivel, cargo, tipo de retiro y meses de permanencia. |
| `PLANTA DE PERSONAL` | Fuente de planta activa / snapshot mensual | Contiene `Antigüedad` y `Rango Antigüedad`, pero su semantica corresponde a planta, no necesariamente a retiro. |
| `Planta Ppto` | Fuente agregada de presupuestos/reales y conteos de retiros | Se usa en comparativos mensuales y trimestrales de retiros. |
| `Tbl_Medidas` | Tabla tecnica de medidas | Contiene medidas actuales para retiros, rotacion y participacion. |
| `Años`, `Mes`, `Empresas`, `Estructura`, `AREAS`, `DimPeriodoYM` | Dimensiones de filtrado | Ya existen relaciones con `Ppto Retiros`. |

Relaciones relevantes:

| Origen | Destino | Observacion |
|---|---|---|
| `Ppto Retiros[Mes]` | `Mes[Meses]` | Permite filtrado mensual. |
| `Ppto Retiros[Empresa]` | `Empresas[Empresas]` | Permite analisis por empresa. |
| `Ppto Retiros[Año]` | `Años[Año]` | Permite filtrado anual. |
| `Ppto Retiros[Dependencia]` | `Estructura[DEPENDENCIA]` | Permite analisis organizacional. |
| `Ppto Retiros[Área]` | `AREAS[AREA]` | Permite analisis por area. |
| `Ppto Retiros[Identificación]` | `Maestro[Identificación]` | Permite cruce con maestro, con riesgo de traer atributos actuales y no historicos. |
| `Ppto Retiros[IndexAnioMes]` | `DimPeriodoYM[IndexAnioMes]` | Permite analisis por periodo ordenado. |

Advertencia: la consola muestra algunos nombres con problemas de codificacion, pero la revision logica identifica los campos por su rol y ubicacion. Cualquier edicion futura debe preservar UTF-8 sin BOM y validarse en Power BI Desktop.

## 9. Campos y medidas candidatos

Campos candidatos en `Ppto Retiros`:

| Campo | Uso candidato | Riesgo |
|---|---|---|
| `Identificación` | Conteo distinto de personas retiradas | Puede contener duplicados por persona o multiple contrato. |
| `Mes` | Conteo actual de `[Tot_Retiros]` | Mide registros con mes, no necesariamente personas unicas. |
| `Año` | Filtro temporal | Debe validar tipo de dato y relacion con dimension `Años`. |
| `Empresa` | Corte por unidad/empresa | Ya existe relacion con `Empresas`. |
| `Fecha Inicio` | Base para antiguedad al retiro | En TMDL aparece como texto; requiere conversion controlada. |
| `Fecha Vencimiento` | Fecha potencial de retiro o fin de contrato | En TMDL aparece como texto; requiere confirmar semantica. |
| `Meses de permanencia` | Alternativa para calcular rango de antiguedad al retiro | En TMDL aparece como texto; requiere validar si representa antiguedad al retiro, unidad, limpieza y nulos. |
| `Tipo de retiro` | Segmentacion voluntario/involuntario | Ya existe como columna calculada. |

Medidas candidatas existentes:

| Medida | Uso candidato | Observacion |
|---|---|---|
| `Tbl_Medidas[Tot_Retiros]` | Valor base de la matriz | Actualmente `COUNT('Ppto Retiros'[Mes])`. Requiere validar grano. |
| `Tbl_Medidas[Retiros_Voluntarios]` | Corte opcional por tipo de retiro | Usa `Tipo de retiro = Voluntario`. |
| `Tbl_Medidas[Retiros_Involuntarios]` | Corte opcional por tipo de retiro | Usa `Tipo de retiro = Involuntario`. |
| `Tbl_Medidas[Retiros_Segun_Tipo]` | Valor dependiente de slicer/tipo seleccionado | Puede ser util si ya existe segmentacion por tipo. |
| Nueva medida `Personas_Retiradas` | Conteo distinto por identificacion | Recomendable solo si negocio confirma que se requieren personas unicas y no eventos. |
| Nueva medida `% Retiros por Rango Antiguedad` | Participacion del rango sobre el total filtrado | Recomendable como apoyo, no como primera version si se busca claridad ejecutiva. |

## 10. Alternativas de calculo de antiguedad

| Alternativa | Descripcion | Ventaja | Riesgo | Evaluacion |
|---|---|---|---|---|
| A. Usar `PLANTA DE PERSONAL[Rango Antigüedad]` via relaciones existentes | Cruza retiros con atributos de planta o maestro | Evita modelado nuevo | Puede representar antiguedad actual o del snapshot, no antiguedad al retiro | No recomendada como base funcional. |
| B. Calcular rango desde `Ppto Retiros[Meses de permanencia]` | Convierte meses de permanencia a rangos | Es la opcion mas directa si el campo esta limpio | Campo aparece como texto; requiere validar unidad, nulos y origen | Recomendada con validacion previa. |
| C. Calcular rango desde `Fecha Inicio` y `Fecha Vencimiento` | Calcula antiguedad al momento del retiro | Trazable y conceptualmente solida | Fechas aparecen como texto; requiere parseo regional y confirmar que `Fecha Vencimiento` es fecha de retiro | Recomendada si se valida semantica de fechas. |
| D. Crear tabla desconectada de rangos y medida DAX | Evita columna en hecho y controla orden visual | Flexible | Mayor complejidad DAX; puede complicar filtros | Posible para una fase posterior. |
| E. Matriz solo visual con campo existente de `PLANTA DE PERSONAL` | Replica referencia de Demografico | Rapida en Desktop | Riesgo alto de conclusion errada | Descartar salvo aprobacion funcional explicita. |

## 11. Alternativa recomendada

Recomendacion principal: crear una clasificacion de antiguedad propia para retiros en `Ppto Retiros`, no reutilizar directamente `PLANTA DE PERSONAL[Rango Antigüedad]`.

Antes de implementar, es obligatorio validar si `Ppto Retiros[Meses de permanencia]` representa efectivamente la antiguedad al retiro. Si esa validacion no es concluyente, no debe usarse como base de la matriz.

Ruta recomendada:

1. Validar en la fuente si `Meses de permanencia` representa permanencia al momento del retiro.
2. Si es confiable, crear una columna de rango en Power Query o TMDL para `Ppto Retiros`, basada en meses.
3. Si no es confiable, calcular antiguedad desde `Fecha Inicio` y la fecha efectiva de retiro/fin validada por negocio.
4. Usar como valor inicial `Tbl_Medidas[Tot_Retiros]` solo si se confirma que cada fila de `Ppto Retiros` representa un retiro.
5. Si hay multiples filas por persona, crear y validar una medida de conteo distinto de personas retiradas.

Rangos sugeridos, alineados con el patron existente:

| Orden | Etiqueta tecnica sugerida |
|---:|---|
| 1 | `a. Menos de 1 ano` |
| 2 | `b. Entre 1 y 2 anos` |
| 3 | `c. Entre 3 y 5 anos` |
| 4 | `d. Entre 6 y 9 anos` |
| 5 | `e. Entre 10 y 19 anos` |
| 6 | `f. Entre 20 y 29 anos` |
| 7 | `g. 30 anos o mas` |

## 12. Diseno propuesto de la matriz

Diseno recomendado para la pagina `Retiros`:

| Elemento | Recomendacion |
|---|---|
| Tipo de visual | Matriz / pivotTable |
| Titulo | `Retiros por antiguedad` o `Antiguedad al retiro` |
| Filas | Rango de antiguedad al retiro |
| Columnas obligatorias | Anio |
| Valores | `Tot_Retiros` o `Personas_Retiradas`, segun definicion funcional |
| Formato | Compacto, mismo lenguaje visual de la matriz de `Demografico (Promedio)` |
| Orden | Orden numerico por prefijo `a.` a `g.` |
| Interaccion | Respetar filtros existentes de anio, mes, empresa, area, dependencia y tipo de retiro |

Tipo de retiro, empresa, dependencia, area o unidad de negocio no deben ser columnas principales de esta matriz. Deben operar como filtros, segmentadores o contexto de pagina para no desviar el requerimiento confirmado: antiguedad del personal retirado por rango y anio.

Primera version recomendada:

| Filas | Columnas | Valores |
|---|---|---|
| Rango de antiguedad al retiro | Anio | Total de retiros o personas retiradas |

Version posterior, si negocio la requiere:

| Filas | Columnas | Valores adicionales |
|---|---|---|
| Rango de antiguedad al retiro | Anio | Participacion porcentual del rango dentro del anio |

## 13. Analisis de impacto tecnico

| Frente | Impacto esperado | Nivel |
|---|---|---|
| PBIR visual | Se agregaria un nuevo `visual.json` bajo la pagina `Retiros`. | Medio |
| Modelo semantico | Probable necesidad de nueva columna en `Ppto Retiros` y posiblemente nueva medida. | Alto |
| Power Query | Puede requerir conversion de texto a fecha o numero para permanencia. | Alto |
| Relaciones | No se anticipan nuevas relaciones si el rango vive en `Ppto Retiros`. | Bajo |
| Ordenamiento | Puede requerir columna de orden o prefijo en etiqueta. | Medio |
| Documentacion | Debe actualizarse si se crea nueva logica de antiguedad. | Medio |
| Control de cambios | Requiere staging selectivo por la cantidad de cambios PBIP acumulados. | Alto |
| Validacion visual | Obligatoria en Power BI Desktop. | Alto |

## 14. Archivos potencialmente afectados

| Archivo | Motivo potencial | Se debe tocar en implementacion futura |
|---|---|---|
| `PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405/visuals/<nuevo_visual>/visual.json` | Nuevo visual de matriz en pagina `Retiros`. | Si |
| `PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405/page.json` | Puede registrar cambios de layout de pagina. | Con cautela |
| `PBIP/Proyecto.Report/definition/pages/pages.json` | Power BI puede cambiar metadata o pagina activa. | Evitar salvo cambio necesario validado |
| `PBIP/Proyecto.Report/definition/bookmarks/**` | Power BI puede actualizar bookmarks por interacciones. | No incluir salvo evidencia funcional |
| `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl` | Nueva columna de rango de antiguedad al retiro o transformacion de tipos. | Probable |
| `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl` | Nueva medida si se define conteo distinto o porcentaje. | Posible |
| `PBIP/Proyecto.SemanticModel/definition/cultures/**` | Puede actualizar traducciones/metadata de columnas o medidas nuevas. | Con cautela |
| `PBIP/Proyecto.SemanticModel/diagramLayout.json` | Power BI puede registrar ruido de layout del modelo. | No incluir salvo decision expresa |
| `Docs/DATA_MODEL.md` | Documentar nueva logica si se crea columna/medida. | Si aplica |
| `Docs/PROJECT_CONTEXT.md` | Documentar cambio funcional relevante en pagina `Retiros`. | Si aplica |
| `Specs/0002_analisis_impacto_matriz_antiguedad_retiros.md` | Esta especificacion. | Ya creado en esta fase |

## 15. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Nivel | Mitigacion |
|---|---|---|---|---|
| Usar antiguedad de planta activa para explicar retiros | Media | Alto | Alto | Calcular rango dentro de `Ppto Retiros` con fecha/permanencia de retiro. |
| Contar eventos cuando negocio espera personas unicas | Media | Alto | Alto | Validar grano de `Ppto Retiros` y decidir entre `[Tot_Retiros]` y `DISTINCTCOUNT`. |
| Fechas o meses de permanencia en formato texto | Alta | Medio | Alto | Validar conversion regional y nulos antes de modelar. |
| Ruido masivo de Power BI Desktop en PBIR | Alta | Alto | Alto | Diagnostico posterior al guardado y staging selectivo por archivo/hunk. |
| Saturacion visual de la pagina `Retiros` | Media | Medio | Medio | Validar espacio disponible y jerarquia visual antes de publicar. |
| Duplicar logica de rangos de antiguedad | Media | Medio | Medio | Reutilizar criterios de rangos existentes, pero con campo propio para retiros. |
| Cambios no deseados en bookmarks o slicers | Media | Medio | Medio | No incluir bookmarks/slicers salvo evidencia funcional y aprobacion. |
| Publicacion con resultado no validado | Baja | Alto | Medio | Exigir validacion en Power BI Desktop con filtros de negocio antes del commit final. |

## 16. Criterios de aceptacion

La implementacion futura deberia aceptarse solo si cumple:

- La matriz aparece en la pagina `Retiros` sin desplazar ni romper visuales existentes.
- La matriz usa una definicion aprobada de antiguedad al retiro.
- La matriz muestra los anios como columnas principales.
- Los rangos se muestran en el orden correcto.
- El total por anio coincide con la medida validada de retiros bajo los mismos filtros.
- El valor mostrado corresponde al grano funcional aprobado: eventos de retiro o personas retiradas.
- La matriz responde correctamente a filtros de anio, mes, empresa, area, dependencia y tipo de retiro.
- No se incluyen cambios de slicers, bookmarks, `activePageName`, `diagramLayout` o visuales no relacionados.
- Power BI Desktop abre `Proyecto7.pbip` sin errores.
- El diff final permite separar modelo, visual y documentacion en commits controlados.

## 17. Validaciones tecnicas

Antes de implementar:

```powershell
git status --short
git status --short -- PBIP/
git diff --stat -- PBIP/
```

Durante la implementacion:

- Validar que Power BI Desktop este cerrado antes de ediciones manuales.
- Preferir Power BI Desktop para crear visuales complejos PBIR.
- Si se edita TMDL, validar estructura, indentacion y codificacion UTF-8 sin BOM.
- Si se edita JSON, validar parseo de cada archivo modificado.

Despues de guardar en Power BI Desktop:

```powershell
git status --short -- PBIP/
git diff --stat -- PBIP/
git diff -- PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl
git diff -- PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl
git diff -- PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405/
git diff --check
```

Validaciones funcionales:

- Comparar total de matriz contra total de retiros bajo los mismos filtros.
- Validar resultados por un anio y mes conocidos.
- Confirmar si la suma por rangos coincide con `[Tot_Retiros]` o con la medida aprobada.
- Validar nulos, fechas faltantes y permanencias negativas o atipicas.

## 18. Documentacion a actualizar

Si se aprueba e implementa el cambio, evaluar actualizacion de:

| Documento | Motivo |
|---|---|
| `Docs/DATA_MODEL.md` | Nueva columna o medida de antiguedad al retiro. |
| `Docs/PROJECT_CONTEXT.md` | Nueva capacidad analitica en pagina `Retiros`. |
| `Docs/COMMIT_GUIDELINES.md` | Solo si se formaliza una regla nueva de commits PBIP. |
| `Docs/FOLDER_STRUCTURE.md` | No aplica salvo cambios estructurales. |
| `README.md` | Solo si el cambio altera descripcion general del proyecto. |
| Nueva evidencia en `Outputs/` | Diagnostico posterior al guardado, si el usuario lo solicita. |

## 19. Estrategia de commits

No se debe mezclar esta funcionalidad con cambios PBIP pendientes.

Estrategia recomendada:

1. Commit de modelo, si se crea columna o medida:
   - `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl`
   - `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl`, si aplica
   - culturas solo si el diff es necesario y validado
2. Commit de visual:
   - nuevo `visual.json` de la matriz en pagina `Retiros`
   - archivos de pagina estrictamente necesarios
3. Commit documental:
   - documentos actualizados y Spec si se decide versionar cierre de decisiones

Mensaje tentativo para implementacion visual:

```text
feat(retiros): agrega matriz de antiguedad al retiro
```

Mensaje tentativo para modelo:

```text
feat(model): calcula rango de antiguedad al retiro
```

Regla de control: no usar `git add .`; preparar staging selectivo y validar `git diff --cached --name-status` antes de cualquier commit.

## 20. Plan de rollback

Rollback recomendado por alcance:

| Alcance | Accion de rollback |
|---|---|
| Solo visual | Revertir el commit que agregue el visual de matriz y cualquier metadata estrictamente asociada. |
| Modelo semantico | Revertir columnas/medidas nuevas en TMDL y validar reapertura en Power BI Desktop. |
| Documentacion | Revertir o actualizar la documentacion para reflejar decision anulada. |
| Ruido PBIP no stageado | No incluir en commit; mantener separado del cambio aprobado. |

No se recomienda usar `git restore` o `git checkout` en la fase de diagnostico ni sin aprobacion expresa, debido al backlog de cambios manuales acumulados.

## 21. Decisiones pendientes de aprobacion

Antes de implementar, el usuario debe aprobar:

- Si la matriz contara eventos de retiro o personas retiradas unicas.
- Si la antiguedad debe calcularse desde `Meses de permanencia` o desde fechas.
- Si `Ppto Retiros[Meses de permanencia]` representa de forma verificable la antiguedad al retiro.
- Cual es la fecha oficial de retiro: `Fecha Vencimiento`, otra fecha de la fuente o una regla de negocio externa.
- Si se requiere mostrar solo total de retiros o tambien porcentaje de participacion por rango.
- Ubicacion visual exacta dentro de la pagina `Retiros`.
- Si el cambio se implementara primero en Power BI Desktop y luego se diagnosticara el diff PBIP.
- Si se permite modificar el modelo semantico o si se exige una solucion solo visual con campos existentes.

Recomendacion final: avanzar por fases. Primero validar la regla de antiguedad al retiro y el grano de conteo. Luego implementar el modelo minimo. Finalmente agregar la matriz y preparar staging selectivo.
