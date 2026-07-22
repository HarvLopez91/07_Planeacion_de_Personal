# Analisis de impacto - correccion de periodo y filtros por negocio en Productividad

Fecha de elaboracion: 2026-07-21

Solicitante: Mateo

Consecutivo: 0004

Proyecto: `07_Planeacion_de_Personal`

Archivo PBIP: `PBIP/Proyecto7.pbip`

Estado: implementado y validado funcionalmente; pendiente de preparacion de commit.

## Objetivo

Corregir la pagina `Productividad` para resolver los sintomas reportados:

- el grafico mensual muestra la serie como `Ejecucion 2025` aunque el usuario seleccione otro anio;
- al seleccionar `Challenger`, la lectura puede confundirse con el consolidado del grupo;
- al seleccionar otros negocios, la tabla inferior puede mostrar valores como cero aunque existan importes distintos de cero.

## Alcance

La revision cubre exclusivamente la pagina `Productividad`, identificada en PBIR como:

| Atributo | Valor |
|---|---|
| Carpeta PBIR | `PBIP/Proyecto.Report/definition/pages/ReportSection65569958420c423d90b1/` |
| Display name | `Productividad` |
| Tamano de pagina | 1350 x 900 |

Se revisaron los segmentadores de `Anio`, `Meses`, `Grupo Empresa` y `Empresas`, los graficos de `Gasto Laboral Vs Ventas`, la tabla inferior y la tarjeta KPI relacionada.

## Fuera de alcance

Quedan fuera de alcance:

- fuentes de datos y Power Query;
- Formula Firewall;
- relaciones generales o bidireccionales;
- otras paginas del reporte;
- navegacion, colores, posiciones, bookmarks y diseno;
- cambios sobre el worktree pausado `refactor/sst-table-names`;
- commit y push en esta fase.

## Contexto funcional y evidencia

La evidencia compartida muestra que la pagina `Productividad` mantiene el texto `Ejecucion 2025` en el grafico aun cuando el analisis debe responder al anio seleccionado. Tambien se reporta que el filtro de negocio no resulta confiable para interpretar Challenger frente al consolidado, y que otros negocios muestran la tabla en cero.

No se incluyeron capturas ni datos personales en esta Spec.

## Estado actual de la pagina Productividad

La pagina contiene 12 objetos PBIR:

| Visual ID | Tipo | Rol |
|---|---|---|
| `218c3d74261421a9024a` | `slicer` | Segmentador de anio (`Años[Año]`). |
| `28f0f8149400696a5db2` | `slicer` | Segmentador de mes (`Mes[Meses]`). |
| `4f443744676093488ca7` | `slicer` | Segmentador de grupo (`Empresas[Grupo Empresa]`). |
| `3dd46d85a9687cb70a8d` | `slicer` | Segmentador de empresa (`Empresas[Empresas]`). |
| `d6010674e3a075647581` | `lineClusteredColumnComboChart` | Grafico mensual de gasto laboral vs ventas. |
| `76fbb82301d3f6b571c3` | `lineClusteredColumnComboChart` | Comparativo anual acumulado. |
| `cba349945ec4b0577321` | `tableEx` | Tabla inferior por mes. |
| `9bcb53c0b346ba0d28c4` | `tableEx` | Tabla KPI gasto vs venta. |
| `285fcb59b2cbc3c988ce` | `card` | Indicador KPI visual. |
| `1f260b8107972119dde2` | `pageNavigator` | Navegador de paginas. |
| `121ca2fd1e1e50039810` | `shape` | Encabezado. |
| `579636f8c0c9cdcb800e` | `shape` | Panel lateral. |

## Inventario de visuales y segmentadores implicados

### Segmentadores

| Visual ID | Campo | Hallazgo |
|---|---|---|
| `218c3d74261421a9024a` | `Años[Año]` | Seleccion persistida 2026; filtros auxiliares no nulos heredados del contexto. |
| `28f0f8149400696a5db2` | `Mes[Meses]` | Modo desplegable; filtros auxiliares no nulos heredados del contexto. |
| `4f443744676093488ca7` | `Empresas[Grupo Empresa]` | Campo correcto para el grupo empresarial; sincronizado como `Grupo Empresa`. |
| `3dd46d85a9687cb70a8d` | `Empresas[Empresas]` | Campo correcto para empresa; sincronizado como `Empresa`. |

### Visuales de productividad

| Visual ID | Tipo | Medidas / campos | Hallazgo |
|---|---|---|---|
| `d6010674e3a075647581` | Combo lineas/columnas | `Mes[Meses]`, `Planta Ppto[Efic]`, `Planta Ppto[%Efiprom]` | La serie `Efic` estaba renombrada literalmente como `Ejecucion 2025`. |
| `76fbb82301d3f6b571c3` | Combo lineas/columnas | `Años[Año]`, `Planta Ppto[Efic]`, `Planta Ppto[%Efiprom]` | No tenia texto fijo `2025`; se conserva. |
| `cba349945ec4b0577321` | Tabla | `Mes[Meses]`, `SUM(Planta Ppto[Gasto Personal])`, `SUM(Planta Ppto[Ventas (MM)])`, `Planta Ppto[Efic]` | Forzaba `labelDisplayUnits = 1000000D` en gasto y ventas; esto puede producir ceros visuales por doble escalado. |
| `9bcb53c0b346ba0d28c4` | Tabla KPI | `Planta Ppto[%Efiprom]`, `Planta Ppto[Efic]` | Formato porcentual con una cifra decimal; sin cambio. |

## Medidas, tablas y relaciones dependientes

Medidas principales:

| Medida | Expresion actual | Observacion |
|---|---|---|
| `Planta Ppto[Efic]` | `SUM('Planta Ppto'[Gasto Personal])/SUM('Planta Ppto'[Ventas (MM)])` | No usa `ALL`, `REMOVEFILTERS` ni filtros fijos a Challenger. |
| `Planta Ppto[%Efiprom]` | `SUM('Planta Ppto'[Ppto Gasto Personal])/SUM('Planta Ppto'[Ppto Ventas (MM)])` | No usa `ALL`, `REMOVEFILTERS` ni filtros fijos a Challenger. |
| `Planta Ppto[KPI_EFI]` | Compara `[Efic]` contra `[%Efiprom]` | Depende de las dos medidas anteriores. |

Relaciones relevantes:

| Relacion | Hallazgo |
|---|---|
| `Planta Ppto[Empresa]` -> `Empresas[Empresas]` | Existe en `relationships.tmdl`. |
| `Planta Ppto[Año]` -> `Años[Año]` | Existe en `relationships.tmdl`. |
| `Planta Ppto[Mes]` -> `Mes[Meses]` | Existe en `relationships.tmdl`. |
| `Empresas[Grupo Empresa]` -> `Grupo Empresarial[Grupo Empresarial]` | Existe; no se cambio. |

No se identifico una medida que elimine indebidamente el contexto empresarial en los calculos de productividad revisados.

## Diagnostico y causa raiz sustentada

La causa raiz confirmada tiene dos frentes:

1. El texto `Ejecucion 2025` no proviene de una medida DAX ni de un filtro persistido; es el `displayName/nativeQueryRef` literal de la serie `Planta Ppto[Efic]` en el visual `d6010674e3a075647581`.
2. La tabla inferior `cba349945ec4b0577321` fuerza unidades de visualizacion en millones (`labelDisplayUnits = 1000000D`) sobre `Gasto Personal` y `Ventas (MM)`. Dado que `Ventas (MM)` ya esta expresada como millones y `Gasto Personal` se usa en la razon de productividad contra ventas en millones, el doble escalado puede mostrar valores pequenos como cero.

Sobre los filtros de negocio:

- los slicers usan `Empresas[Grupo Empresa]` y `Empresas[Empresas]`;
- existe relacion entre `Planta Ppto[Empresa]` y `Empresas[Empresas]`;
- las medidas `Efic` y `%Efiprom` no contienen patrones `ALL`, `REMOVEFILTERS`, `ALLEXCEPT`, `ALLSELECTED` ni filtros fijos a Challenger;
- por lo tanto, no se justifica cambiar relaciones ni introducir bidireccionalidad como primera solucion.

La validacion de datos agregados por negocio queda pendiente de Power BI Desktop, porque el worktree limpio no contiene `Data/` ni cache tabular consultable.

## Alternativas evaluadas

| Alternativa | Evaluacion | Decision |
|---|---|---|
| Corregir interacciones del segmentador | No se encontro archivo de interacciones con `None`; PBIR conserva comportamiento por defecto. | No aplicada. |
| Cambiar slicers a columnas de `Planta Ppto` | Puede resolver empates de claves, pero rompe el patron de dimensiones y sincronizacion. | Descartada sin evidencia de relacion rota. |
| Cambiar medidas con `TREATAS` | Seria una solucion localizada pero redundante si la relacion ya funciona. | No aplicada. |
| Cambiar relacion a bidireccional | Alto riesgo de ambiguedad. | Descartada. |
| Corregir texto fijo y doble escalado visual | Minimo impacto y directamente sustentado por PBIR. | Implementada. |

## Alternativa recomendada

Aplicar una correccion visual y una medida de titulo:

- renombrar la serie mensual de `Ejecucion 2025` a `Ejecucion`;
- usar una medida de titulo dinamico para mostrar el anio seleccionado;
- quitar el escalado forzado a millones en la tabla inferior para evitar ceros visuales;
- conservar los calculos numericos, relaciones, fuentes, colores y layout.

## Implementacion realizada

Se agrego la medida:

`Tbl_Medidas[Titulo_Productividad_Gasto_Laboral]`

Regla:

- un solo anio seleccionado: `Gasto Laboral Vs Ventas - Ejecucion <anio>`;
- seleccion multiple o sin seleccion unica: `Gasto Laboral Vs Ventas - Ejecucion años seleccionados`.

Se modifico el visual mensual:

- `nativeQueryRef/displayName` de `Ejecucion 2025` a `Ejecucion`;
- titulo del visual enlazado a `Tbl_Medidas[Titulo_Productividad_Gasto_Laboral]`.

Se modifico la tabla inferior:

- `Gasto Personal`: `labelDisplayUnits` de `1000000D` a `0D` y `labelPrecision` de `0L` a `1L`;
- `Ingreso Operacional` / `Ventas (MM)`: `labelDisplayUnits` de `1000000D` a `0D` y `labelPrecision` a `1L`.

No se modificaron medidas de calculo, relaciones, fuentes ni otras paginas.

## Analisis de impacto tecnico

| Frente | Impacto | Nivel |
|---|---|---|
| PBIR visual mensual | Corrige etiqueta fija y titulo dinamico. | Bajo |
| PBIR tabla inferior | Corrige unidades visuales y precision. | Bajo |
| Modelo semantico | Agrega una medida de texto para titulo dinamico. | Bajo |
| Relaciones | Sin cambios. | Nulo |
| Medidas numericas | Sin cambios. | Nulo |
| Fuentes | Sin cambios. | Nulo |
| Otras paginas | Sin cambios. | Nulo |

## Archivos potencialmente afectados

Archivos modificados:

- `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl`
- `PBIP/Proyecto.Report/definition/pages/ReportSection65569958420c423d90b1/visuals/d6010674e3a075647581/visual.json`
- `PBIP/Proyecto.Report/definition/pages/ReportSection65569958420c423d90b1/visuals/cba349945ec4b0577321/visual.json`
- `Specs/0004_analisis_impacto_correccion_productividad_filtros_negocio.md`

Archivos excluidos:

- otras paginas;
- `pages.json`;
- bookmarks;
- `diagramLayout.json`;
- `cultures/es-ES.tmdl`;
- fuentes Power Query;
- `Docs/`;
- `Outputs/`;
- `Data/`;
- worktree `refactor/sst-table-names`.

## Riesgos y mitigaciones

| Riesgo | Mitigacion |
|---|---|
| La validacion visual interactiva puede revelar un problema adicional de claves de empresa. | No se cambiaron relaciones; si Desktop muestra que un negocio sigue en cero con datos existentes, revisar valores de `Planta Ppto[Empresa]` vs `Empresas[Empresas]`. |
| El titulo dinamico puede mostrarse largo en espacios estrechos. | Se conserva el mismo visual y formato; validar en Desktop. |
| El cambio de unidades puede aumentar longitud de cifras en la tabla. | Se deja una cifra decimal y se conserva el ancho actual; validar legibilidad. |

## Criterios de aceptacion

- Para 2026, el titulo del grafico mensual debe mostrar `Ejecucion 2026`.
- Para 2025, debe mostrar `Ejecucion 2025`.
- La leyenda ya no debe conservar un anio fijo incorrecto.
- La tabla no debe mostrar como cero importes no nulos por doble escalado.
- `Challenger`, `Fundacion Challenger`, `Grupo Sky`, `Habitel Hotels` y `Lemco` deben responder al filtro de negocio si existen registros en `Planta Ppto`.
- No deben cambiar relaciones, fuentes, layout, bookmarks ni otras paginas.

## Validaciones tecnicas realizadas

- `page.json` valido e identifica `displayName = Productividad`.
- JSON validado para:
  - `d6010674e3a075647581/visual.json`;
  - `cba349945ec4b0577321/visual.json`.
- Busqueda posterior sin coincidencias en la pagina para:
  - `Ejecución 2025`;
  - `Ejecución 2025`;
  - `"Value": "1000000D"`.
- `git diff --check` sin errores en el worktree limpio.
- No hay staging activo.

## Validaciones funcionales pendientes

Debe abrirse `PBIP/Proyecto7.pbip` desde el worktree:

`C:\Users\edwin.clavijo\Worktrees\07_Planeacion_de_Personal\productividad-contexto-negocio`

Escenarios a validar:

- anio 2026: titulo `Ejecucion 2026`;
- anio 2025: titulo `Ejecucion 2025`;
- Challenger;
- Fundacion Challenger;
- Grupo Sky;
- Habitel Hotels;
- Lemco;
- empresa especifica dentro de cada grupo;
- seleccion multiple valida;
- seleccion contradictoria entre grupo y empresa;
- tabla inferior con valores no nulos visibles;
- graficos y tabla reconciliados bajo el mismo contexto.

No se declara refresh completo exitoso ni validacion visual exitosa porque no se ejecuto Power BI Desktop durante esta fase.

## Estrategia de control de cambios

Usar staging selectivo con rutas explicitas:

```powershell
git add -- "Specs/0004_analisis_impacto_correccion_productividad_filtros_negocio.md"
git add -- "PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl"
git add -- "PBIP/Proyecto.Report/definition/pages/ReportSection65569958420c423d90b1/visuals/d6010674e3a075647581/visual.json"
git add -- "PBIP/Proyecto.Report/definition/pages/ReportSection65569958420c423d90b1/visuals/cba349945ec4b0577321/visual.json"
```

No usar `git add .` ni `git add -A`.

Mensaje sugerido:

```text
fix(productividad): corrige periodo y filtros por negocio
```

## Plan de rollback

Rollback por commit:

- revertir la medida `Titulo_Productividad_Gasto_Laboral`;
- restaurar el literal de titulo del visual mensual si fuera necesario;
- restaurar `labelDisplayUnits` y `labelPrecision` de la tabla inferior si negocio prefiere el comportamiento anterior.

No se requiere rollback de modelo relacional ni de fuentes porque no fueron modificados.

## Decision de implementacion

Decision: implementar correccion minima y trazable.

Estado final de esta Spec: implementado, pendiente de validacion visual en Power BI Desktop y pendiente de commit.

## Bloqueo tecnico detectado durante Fase 1

Durante la validacion de apertura del PBIP se detecto el error `PFE_TM_OBJECT_NAME_ALREADY_EXISTS` por dos medidas con nombre `Tot_Accidentes` en el modelo semantico:

- `ACCIDENTALIDAD[Tot_Accidentes]`
- `Tbl_Medidas[Tot_Accidentes]`

Ambas definiciones tenian la misma expresion `COUNT(ACCIDENTALIDAD[Empresa])` y el mismo `lineageTag`. Los visuales SST vigentes referencian `Tbl_Medidas.Tot_Accidentes`, por lo que se conserva `Tbl_Medidas[Tot_Accidentes]` como medida canonica y se elimina unicamente la definicion duplicada en `ACCIDENTALIDAD.tmdl`. La entrada de cultura asociada se redirige a `Tbl_Medidas[Tot_Accidentes]`.

Este ajuste no cambia la logica funcional de Productividad ni diagnostica todavia filtros, relaciones o propagacion empresarial.

## Auditoria model-wide de medidas duplicadas

Posteriormente se detecto un segundo bloqueo de apertura por `ConteoP`. Para evitar correcciones iterativas se ejecuto una auditoria completa de declaraciones `measure` en `PBIP/Proyecto.SemanticModel/definition/tables/*.tmdl`.

Duplicados encontrados:

- `%AusM`
- `%Cumplimiento`
- `Ausentismo`
- `CHombres`
- `CMujeres`
- `ConteoP`
- `Dias Ausentismo Acc.Lab`
- `DIAS_AUSENTISMO`
- `Ind_Calidad`
- `Ind_Calidad_2025`
- `Ind_opor`
- `Ing_Calidad_2025`
- `Ingresos_Calidad`
- `M_Frecuencia`
- `M_Severidad`
- `MSector`
- `Ret_Calidad`
- `ret_Calidad_2025`
- `Solicitud`
- `Solicitudes`
- `Solicitudes2024`
- `Tasa Ausentismo`
- `Tasa Ausentismo_EL`
- `Tasa_Acc`
- `Tasa_Ausent_Anual`
- `Tot_ingresos`

Decision aplicada:

- se conservaron las medidas en sus tablas fuente cuando los visuales vigentes las referenciaban alli;
- se eliminaron las copias redundantes en `Tbl_Medidas.tmdl` para esos nombres;
- `ConteoP` queda como `AUSENTISMOS[ConteoP]`;
- `Tot_Accidentes` queda como `Tbl_Medidas[Tot_Accidentes]`, por referencias SST ya migradas a `Tbl_Medidas.Tot_Accidentes`;
- no se modificaron relaciones, Power Query ni visuales de Productividad durante esta limpieza.

Resultado estatico:

- cero nombres de medidas duplicados en el modelo;
- una sola `ConteoP`;
- una sola `Tot_Accidentes`;
- una sola `Titulo_Productividad_Gasto_Laboral`.

## Reparacion de referencias PBIR rotas posterior a deduplicacion

Despues de eliminar medidas duplicadas, Power BI Desktop abrio el PBIP pero la pagina `Productividad` mostro visuales con el mensaje `Hubo un problema con uno o mas campos`.

Causa raiz confirmada:

- los visuales de Productividad conservaban referencias PBIR a medidas en `Planta Ppto`;
- las medidas canonicas vigentes estan en `Tbl_Medidas`;
- no habia duplicados de medidas, pero si referencias de visual apuntando a la tabla anterior.

Referencias corregidas:

| Visual | Tipo | Referencia anterior | Referencia canonica |
|---|---|---|---|
| `d6010674e3a075647581` | `lineClusteredColumnComboChart` | `Planta Ppto.Efic`, `Planta Ppto.%Efiprom` | `Tbl_Medidas.Efic`, `Tbl_Medidas.%Efiprom` |
| `76fbb82301d3f6b571c3` | `lineClusteredColumnComboChart` | `Planta Ppto.Efic`, `Planta Ppto.%Efiprom` | `Tbl_Medidas.Efic`, `Tbl_Medidas.%Efiprom` |
| `cba349945ec4b0577321` | `tableEx` | `Planta Ppto.Efic` | `Tbl_Medidas.Efic` |
| `9bcb53c0b346ba0d28c4` | `tableEx` | `Planta Ppto.Efic`, `Planta Ppto.%Efiprom` | `Tbl_Medidas.Efic`, `Tbl_Medidas.%Efiprom` |
| `285fcb59b2cbc3c988ce` | `card` | `Planta Ppto.KPI_EFI`, `Planta Ppto.Var_GL` | `Tbl_Medidas.KPI_EFI`, `Tbl_Medidas.Var_GL` |

Tambien se ajustaron los bindings generados en `cultures/es-ES.tmdl` para las mismas medidas, evitando que la cultura conserve referencias a objetos ya eliminados.

Regresion minima:

- `SST`: no se detectaron referencias `SourceRef/Property` rotas en la pagina SST.
- `Ausentismos`: se corrigio `PLANTA DE PERSONAL.Prom_Colaboradores` a `Tbl_Medidas.Prom_Colaboradores` en el visual `eb0f97a29923076c72ba`.
- `Retiros`: permanece una referencia a `Tbl_Medidas[Filtro Trimestre Dinamico]` en el visual `37ed01c30df4dafce226`. No se modifico porque no existe medida canonica con ese nombre ni reemplazo exacto demostrable; la medida existente mas cercana es `Filtro Trimestre Slicer`, pero no se asumio equivalencia funcional.

Validaciones estaticas:

- JSON valido en los visuales modificados.
- Cero nombres de medidas duplicados.
- Una sola `Tot_Accidentes`.
- Una sola `ConteoP`.
- Una sola `Titulo_Productividad_Gasto_Laboral`.
- Sin mojibake en los archivos revisados de Productividad y `Tbl_Medidas.tmdl`.
- `git diff --check` sin errores; solo advertencias LF -> CRLF.

Estado de Fase 1:

- Power BI Desktop inicia `Proyecto7` desde `.wt\prod`.
- No se pudo confirmar visualmente el lienzo de Productividad mediante captura automatizada porque Windows mantuvo el foco sobre el Explorador.
- La validacion funcional 2025, 2026 y seleccion multiple queda pendiente de evidencia visual directa.
- Fase 1 permanece bloqueada hasta confirmar en Desktop que Productividad renderiza sin campos no reconocidos y que Retiros no bloquea la regresion minima.

## Ampliacion Fase 1 - Unidades dinamicas Challenger vs. otros negocios

Estado visual aportado por el usuario:

- Productividad renderiza.
- Para `Año = 2026`, `Grupo Empresa = Habitel Hotels` y `Mes = Enero`, el titulo dinamico muestra `Gasto Laboral Vs Ventas - Ejecucion 2026`.
- La leyenda muestra `Ejecucion`.
- La tabla presenta una cifra decimal y valores distintos de cero.

Patron reutilizado desde Gasto Laboral:

- La pagina `Gasto Laboral` usa dos visuales superpuestos para el grafico monetario:
  - visual Challenger con medidas que devuelven valor solo cuando `Empresas[Grupo Empresa] = "Challenger"` y `labelDisplayUnits = 1000000D`;
  - visual otros negocios con medidas que devuelven valor cuando no hay seleccion unica de Challenger y `labelDisplayUnits = 0D`.
- La tabla de `Gasto Laboral` no se duplica: las columnas monetarias usan `labelDisplayUnits = 1D` y `labelPrecision = 1L`.

Decision aplicada en Productividad:

- No se duplicaron los graficos `d6010674e3a075647581` ni `76fbb82301d3f6b571c3`, porque no muestran importes monetarios sino porcentajes (`Efic` y `%Efiprom`).
- Se conservo el titulo dinamico, la leyenda `Ejecucion`, las referencias canonicas y la precision decimal ya validada.
- Se ajusto solo la tabla mensual `cba349945ec4b0577321` para alinear sus dos columnas monetarias con el criterio de la tabla de Gasto Laboral:
  - `Sum(Planta Ppto.Gasto Personal)`: `labelDisplayUnits = 1D`, `labelPrecision = 1L`.
  - `Sum(Planta Ppto.Ventas (MM))`: `labelDisplayUnits = 1D`, `labelPrecision = 1L`.
- La columna `Tbl_Medidas.Efic` permanece como porcentaje con una cifra decimal.

Medidas auxiliares:

- No se crearon medidas nuevas para esta ampliacion.
- Se reutiliza la logica existente de Gasto Laboral solo como patron de configuracion visual.

Validaciones estaticas:

- JSON valido en los visuales revisados.
- Cero nombres de medidas duplicados.
- Sin mojibake real en los archivos revisados.
- `git diff --check` sin errores; solo advertencias LF -> CRLF.

Validacion Desktop:

- Power BI Desktop abrio `Proyecto7` con ruta absoluta desde `.wt\prod`.
- La captura automatizada no permitio confirmar visualmente Productividad despues del ajuste porque otras ventanas conservaron el foco.
- Queda pendiente validacion visual manual de Challenger, Grupo Sky, Habitel Hotels, Fundacion Challenger, Lemco, seleccion multiple y sin seleccion.

Correccion final de criterio:

- La configuracion fija `labelDisplayUnits = 1D` no demuestra por si sola el comportamiento requerido de unidades dinamicas por `Grupo Empresa`.
- Se reemplaza ese intento por el mismo patron funcional usado en `Gasto Laboral`: medidas numericas auxiliares que devuelven valor o `BLANK()` segun si existe seleccion unica de `Empresas[Grupo Empresa] = "Challenger"` y visuales de tabla superpuestos con unidades distintas.
- La tabla original `cba349945ec4b0577321` queda como version para otros contextos, seleccion multiple o sin seleccion unica, usando `labelDisplayUnits = 1D` como unidad automatica y una cifra decimal en las columnas monetarias.
- Se agrega la tabla superpuesta `f0d2c4b6a8e14c5397bd` como version Challenger, usando `labelDisplayUnits = 1000000D` y una cifra decimal en las columnas monetarias.
- Las medidas nuevas son numericas y no usan `FORMAT()`: `Prod_Gasto_Personal`, `Prod_Ingreso_Operacional`, `Prod_Es_Challenger`, `Prod_Gasto_Personal_Challenger`, `Prod_Ingreso_Operacional_Challenger`, `Prod_Efic_Challenger`, `Prod_Gasto_Personal_Otros`, `Prod_Ingreso_Operacional_Otros` y `Prod_Efic_Otros`.
- Los graficos `d6010674e3a075647581` y `76fbb82301d3f6b571c3` no se duplican por unidades monetarias porque sus series visibles son porcentuales.
- Queda pendiente evidencia visual en Power BI Desktop para Challenger, Fundacion Challenger, Grupo Sky, Habitel Hotels, Lemco, seleccion multiple y sin seleccion.

Subtitulo dinamico del grafico acumulado:

- Hallazgo adicional de Fase 1: el grafico derecho `76fbb82301d3f6b571c3` mantenia el subtitulo literal `Comparativo Acumulado (Ene-Jul) Anual`, aunque el segmentador de meses podia tener solo enero u otros contextos.
- Se crea la medida numerica/textual de presentacion `Subtitulo_Productividad_Comparativo_Acumulado` en `Tbl_Medidas.tmdl`.
- La medida usa `Mes[Meses]` como columna de filtro, `Mes[Numero]` como orden y `Mes[Mes Abrev]` como abreviatura.
- El visual `76fbb82301d3f6b571c3` ahora obtiene `subTitle.text` desde `Tbl_Medidas[Subtitulo_Productividad_Comparativo_Acumulado]`.
- El titulo principal, leyenda, ejes, etiquetas, medidas, posicion, tamano y estilo del visual se conservan.
- Escenarios pendientes de evidencia Desktop: un mes, rango consecutivo, meses no consecutivos, mas de cuatro meses no consecutivos, todos los meses y sin seleccion especifica.

Evidencia Desktop posterior:

- El PBIP abre desde `.wt/prod` y la pagina Productividad renderiza.
- Con `Mes = 01.Enero`, el subtitulo del visual `76fbb82301d3f6b571c3` muestra `Comparativo Acumulado (Ene) Anual`, confirmando que el enlace a la medida funciona para el caso de un mes.
- La tabla mensual mantiene una cifra decimal, pero en el contexto visible sin seleccion unica de negocio sigue mostrando importes completos, por ejemplo `$ 8.687.079.642,3`, en lugar de una escala automatica legible.
- Por tanto, la Fase 1 permanece bloqueada para el criterio de unidades dinamicas de la tabla. La alternativa pendiente es evaluar una cadena de formato dinamica o una arquitectura equivalente que Power BI aplique correctamente en `tableEx`, sin usar `FORMAT()` y sin alterar las medidas base.

## Actualizacion Fase 1 - cierre tecnico pendiente de validacion visual completa

Correcciones aplicadas en esta iteracion:

- El problema `0,0 bill.%` se origino por aplicar unidades de magnitud a etiquetas que corresponden a medidas porcentuales (`Efic` y `%Efiprom`). Se corrigieron los visuales `d6010674e3a075647581` y `76fbb82301d3f6b571c3` para mantener porcentaje con una cifra decimal y sin sufijos de magnitud.
- Las tablas superpuestas `cba349945ec4b0577321` y `f0d2c4b6a8e14c5397bd` se ampliaron de `470,5709564898109` a `570` px de ancho, conservando `x = 389,4988066825776`, `y = 468,80851845052325`, `height = 336,6256655039471`, z-order y tabOrder relativos.
- Los anchos de columnas quedaron controlados en ambas tablas: `Meses = 78`, `Gasto Personal = 145`, `Ingreso Operacional = 180`, `Productividad = 120`.
- Se corrigio la cadena de formato dinamica de las medidas monetarias auxiliares de Productividad. La causa del valor completo con sufijo era que la escala estaba escrita despues del decimal (`#,0.0,,`), por lo que Power BI agregaba el sufijo pero no dividia el valor. Quedo corregida con escala antes del decimal (`#,0,,.0`, `#,0,,,.0`, `#,0,.0`).
- Se mantiene el tipo numerico de las medidas y no se usa `FORMAT()`.
- El modelo requiere `compatibilityLevel = 1601` por el uso de `formatStringDefinition`.

Validacion Desktop observada:

- El PBIP abre desde `.wt/prod`.
- Productividad renderiza sin error visible de campos no reconocidos.
- Con `Ano = 2026`, `Mes = 01.Enero` y sin seleccion unica de negocio, la tabla muestra `$ 8,7 bill.` y `$ 76,5 bill.`, con una cifra decimal y sin importes completos.
- Con `Empresa = Fundacion Challenger`, la tabla muestra `$ 28,0` y `$ 135,0`, con una cifra decimal y sin sufijo innecesario.
- Con `Mes = 01.Enero`, el subtitulo acumulado muestra `Comparativo Acumulado (Ene) Anual`.
- No se pudo evidenciar de forma fiable la seleccion de Challenger desde automatizacion de clics porque Power BI Desktop entro en modo de seleccion de objetos del panel de filtros. Ese escenario queda pendiente de validacion visual manual antes de aprobar la Fase 1.

Estado actualizado:

- Fase 1 permanece bloqueada exclusivamente por falta de evidencia visual completa de Challenger, Grupo Sky, Habitel Hotels, Lemco, seleccion multiple y sin seleccion especifica despues de la correccion final.
- No procede iniciar Fase 2 todavia.

## Actualizacion Fase 1 - regla definitiva de unidades por contexto

Regla funcional definitiva:

- Challenger como unico negocio efectivo: tabla en millones y una cifra decimal.
- Todos los negocios o segmentador limpio: tabla en millones y una cifra decimal.
- Cualquier subconjunto distinto de todos los negocios: tabla automatica y una cifra decimal.

Condicion DAX implementada:

- Se reemplazo la bandera `Prod_Es_Challenger` por `Prod_Usar_Millones`.
- `Prod_Usar_Millones` devuelve `TRUE()` cuando:
  - existe un unico grupo visible y es `Challenger`;
  - todos los grupos estan visibles;
  - no hay filtro directo de `Empresas[Grupo Empresa]` ni de `Empresas[Empresas]`.
- Las medidas de la tabla en millones devuelven valor cuando `[Prod_Usar_Millones]` es `TRUE()`.
- Las medidas de la tabla automatica devuelven valor cuando `[Prod_Usar_Millones]` es `FALSE()`.

Evidencia Desktop:

- Segmentador limpio, `Ano = 2026`, `Mes = 01.Enero`: la tabla muestra `$ 8.687,1 mill.` y `$ 76.517,6 mill.`, sin `bill.`.
- Las evidencias visuales aportadas por el usuario confirman Challenger en millones y Habitel Hotels / Grupo Sky en unidades automaticas antes de este ultimo ajuste.
- La prueba automatizada de otros subconjuntos no fue concluyente porque el clic ingreso en seleccion de objetos o en un filtro de empresa especifica sin datos para el mes visible.

Estado actualizado:

- La regla DAX pendiente quedo implementada.
- Fase 1 requiere validacion visual final manual de Fundacion Challenger, Lemco, seleccion multiple parcial y empresa individual antes de considerarse cerrada.

## Consistencia transversal de unidades entre Productividad y Gasto Laboral

Alcance aplicado:

- Se replica en `Gasto Laboral` la regla definitiva de unidades ya implementada en Productividad.
- Regla final: `Challenger` o consolidado completo -> millones; cualquier contexto parcial distinto -> automatico.

Cambios en medidas `GL_*`:

- Se reemplaza la bandera `GL_Es_Challenger` por `GL_Usar_Millones`.
- `GL_Usar_Millones` evalua:
  - `Challenger` como unico grupo efectivo;
  - todos los grupos visibles;
  - ausencia de filtro directo en `Empresas[Grupo Empresa]` y `Empresas[Empresas]`.
- `GL_Ppto_Visual_Challenger` y `GL_Real_Visual_Challenger` devuelven datos solo cuando `[GL_Usar_Millones]` es `TRUE()`.
- `GL_Ppto_Visual_Otros` y `GL_Real_Visual_Otros` devuelven datos solo cuando `[GL_Usar_Millones]` es `FALSE()`.
- La tabla `ced924c91be19c603ad0` usa las medidas base `GL_Ppto_Gasto_Personal` y `GL_Gasto_Personal`; por tanto, se agregan cadenas de formato dinamicas numericas a esas dos medidas para aplicar la misma regla sin duplicar la tabla.

Evidencia Desktop:

- `Proyecto7.pbip` abre desde `.wt/prod`.
- En `Gasto Laboral`, con segmentador de negocio limpio y `Ano = 2025`, el grafico y la tabla muestran valores en millones, por ejemplo `$ 13.459,3 mill.` y `$ 12.188,0 mill.`.
- En contexto parcial de empresa/grupo Lemco, la pagina muestra valores parciales con escala automatica y una cifra decimal, por ejemplo `$ 1.160,2 mill.`.
- No se observaron lineas duplicadas ni doble tabla visible en los contextos capturados.

Pendiente:

- Validacion visual manual de todos los grupos seleccionados, Challenger individual, Grupo Sky, Habitel Hotels, Fundacion Challenger, seleccion parcial multiple y empresas individuales antes de cerrar definitivamente Fase 1.

## Cierre de Fase 1 - criterio definitivo de unidades por negocio

Se corrige la redaccion funcional para evitar contradicciones:

- `Challenger` como unica seleccion: los importes monetarios se presentan en millones, con una cifra decimal.
- Cualquier negocio diferente de `Challenger` como unica seleccion: los importes se presentan con unidades automaticas segun magnitud, con una cifra decimal.
- Seleccion multiple, incluso si incluye `Challenger`: los importes se presentan con unidades automaticas.
- Todos los negocios o ausencia de seleccion unica: los importes se presentan con unidades automaticas.

Evidencia visual recibida y aceptada:

- Sin seleccion unica: `$ 8,7 bill.` y `$ 76,5 bill.`, comportamiento automatico.
- `Challenger`: `$ 8.687,1 mill.` y `$ 76.517,6 mill.`, comportamiento en millones.
- `Habitel Hotels`: `$ 1,6 mil` y `$ 5,4 mil`, comportamiento automatico.
- `Grupo Sky`: `$ 1,1 mil` y `$ 6,2 mil`, comportamiento automatico.
- En todos los casos se conserva una cifra decimal.

Validaciones complementarias:

- `Fundacion Challenger` usa la rama automatica porque `Prod_Es_Challenger` solo es verdadero con `HASONEVALUE(Empresas[Grupo Empresa])` y `SELECTEDVALUE(Empresas[Grupo Empresa]) = "Challenger"`.
- `Lemco` usa la rama automatica por la misma regla.
- `Challenger` junto con otro negocio usa la rama automatica porque `HASONEVALUE(Empresas[Grupo Empresa])` es falso.
- Dos negocios distintos de `Challenger` usan la rama automatica.
- Todos los negocios seleccionados explicitamente o sin seleccion especifica usan la rama automatica.
- Solo una tabla devuelve datos por contexto: la tabla `f0d2c4b6a8e14c5397bd` devuelve datos para `Challenger` exclusivo; la tabla `cba349945ec4b0577321` devuelve datos para todos los demas contextos.
- Ambas tablas conservan posicion y tamano identicos: `x = 389,4988066825776`, `y = 468,80851845052325`, `width = 570`, `height = 336,6256655039471`.
- Anchos de columna equivalentes: `Meses = 78`, `Gasto Personal = 145`, `Ingreso Operacional = 180`, `Productividad = 120`.

Estado final:

- Fase 1 aprobada: puede iniciarse la Fase 2.

## Cierre complementario Fase 1 - visual roto en Gasto Laboral

Bloqueo detectado:

- En la pagina `Gasto Laboral` persistia un visual inferior derecho con mensaje `Ver detalles / Corregir esto`.
- Visual afectado: `265624db15b1e420a0e6`.
- Tipo: `card`.
- Posicion: `x = 1099,9525133980057`, `y = 668,1771928634422`, `width = 252,03174818533344`, `height = 130,90021029780885`.
- Campo no reconocido: `Planta Ppto[Cump_GL]`.

Causa raiz:

- La medida canonica vigente es `Tbl_Medidas[Cump_GL]`.
- El visual conservaba referencias PBIR a la ubicacion anterior `Planta Ppto.Cump_GL` en proyeccion, ordenamiento y formato condicional de color.

Correccion aplicada:

- Se redirigio el visual `265624db15b1e420a0e6` de `Planta Ppto.Cump_GL` a `Tbl_Medidas.Cump_GL`.
- No se cambio tipo de visual, posicion, tamano, titulo, formato, filtros ni interacciones.
- No se recreo la medida y no se agregaron duplicados.

Validacion:

- El JSON del visual modificado parsea correctamente.
- El modelo conserva cero nombres de medidas duplicados.
- Existe una unica declaracion `Cump_GL`, en `Tbl_Medidas.tmdl`.
- Power BI Desktop abre `Proyecto7.pbip` desde `.wt/prod` y el bloque inferior derecho de `Gasto Laboral` renderiza como tarjeta de cumplimiento, sin el mensaje `Ver detalles / Corregir esto` en la captura revisada.

Pruebas funcionales pendientes de evidencia visual directa:

- Todos los grupos seleccionados explicitamente.
- Seleccion parcial multiple.
- Empresa individual de `Challenger`.
- Empresa individual de otro grupo.

Estado:

- Bloqueo del visual roto resuelto.
- Fase 1 queda pendiente solo de confirmacion visual final de las cuatro ramas anteriores antes de iniciar Fase 2.

## Fase 1 aprobada por validacion acumulada

Decision funcional:

- La Fase 1 se considera aprobada con base en la evidencia acumulada y la validacion visual aportada.
- Los escenarios de seleccion parcial multiple y empresas individuales se trasladan a la Fase 6 - Regresion integral, sin eliminarlos del plan de pruebas.

Evidencia aceptada:

- Productividad abre y renderiza sin visuales rotos.
- El titulo y el subtitulo responden al periodo.
- La leyenda queda como `Ejecucion`.
- Los porcentajes no muestran unidades monetarias ni unidades de magnitud.
- Las tablas son legibles y conservan una cifra decimal.
- `Challenger` utiliza millones.
- El consolidado sin filtro utiliza millones.
- `Fundacion Challenger` y `Grupo Sky` activan la rama de unidades automaticas.
- Gasto Laboral conserva la misma regla y la tarjeta de cumplimiento renderiza correctamente.

## Fase 2 - Diagnostico de propagacion de filtros por Grupo Empresa y Empresa

Objetivo:

- Determinar si los sintomas originales de Productividad se deben a interacciones, relaciones, claves, medidas, filtros persistidos o ausencia real de datos.

Matriz de diagnostico:

| Hipotesis | Evidencia | Resultado |
|---|---|---|
| Interaccion deshabilitada | No se encontro `visualInteractions` en la pagina `ReportSection65569958420c423d90b1`; los visuales funcionales no declaran interacciones `None`. | Descartada |
| Relacion incorrecta | Existen relaciones desde `Planta Ppto[Empresa]` hacia `Empresas[Empresas]`, `Planta Ppto[Año]` hacia `Años[Año]`, `Planta Ppto[Mes]` hacia `Mes[Meses]`, y `Empresas[Grupo Empresa]` hacia `Grupo Empresarial[Grupo Empresarial]`. | Descartada como causa principal |
| Claves sin correspondencia | La tabla `Empresas` contiene la jerarquia esperada de empresas y grupos; la evidencia visual muestra datos para `Challenger`, `Habitel Hotels`, `Grupo Sky` y `Fundacion Challenger`. | Descartada como causa general; pendiente detalle por empresa en Fase 6 |
| Medida elimina filtros | Las medidas funcionales `Efic`, `%Efiprom`, `Prod_Gasto_Personal` y `Prod_Ingreso_Operacional` agregan directamente columnas de `Planta Ppto`; no usan `ALL`, `REMOVEFILTERS` ni filtros fijos de negocio. | Descartada |
| Filtro persistido | Los slicers de `Grupo Empresa` y `Empresas` contienen filtros no nulos e invertidos, no una seleccion fija de negocio. Los visuales funcionales solo mantienen filtros de periodo cuando aplica. | Descartada |
| Ausencia real de datos | La evidencia visual muestra valores distintos de cero para negocios diferentes de `Challenger`. | Descartada como causa general |

Causa raiz demostrada:

- No se confirma un defecto vigente de propagacion de filtros empresariales en la pagina Productividad.
- Los sintomas originales se explican por una combinacion de formato/unidades de visualizacion, visuales con referencias rotas por deduplicacion y lectura visual dominada por la escala del consolidado.
- La propagacion por `Empresas[Grupo Empresa]` funciona para las ramas principales validadas visualmente.

Correccion implementada en Fase 2:

- No se aplican cambios funcionales adicionales en PBIP/TMDL durante esta fase.
- No se modifican relaciones, medidas, interacciones, bookmarks ni fuentes.

Riesgos residuales:

- Las pruebas exhaustivas de seleccion parcial multiple, empresa individual y combinaciones contradictorias quedan trasladadas a Fase 6.
- La herramienta local `Tools/pbip/audit_semantic_model.py` no existe en este worktree, por lo que la auditoria semantica se realizo con inspeccion focalizada de TMDL/PBIR.

Estado:

- Fase 2 completada sin correccion adicional de modelo.
- Puede iniciarse la Fase 4, manteniendo la regresion completa prevista en Fase 6.

## Actualizacion de trazabilidad - Fases 2, 3 y 4

Evidencia detallada:

- `../Outputs/02_2026-07-22_evidencia_fase2_filtros_productividad.md`

Decision:

- La Fase 2 queda cerrada como completada: no se confirmo una falla vigente de propagacion de filtros por `Grupo Empresa` o `Empresas` que requiera correccion funcional adicional.
- La Fase 3 se declara `No aplica`, porque no existe una causa raiz aceptada ni una solucion funcional minima que ejecutar para corregir el contexto de `Grupo Empresa`.
- El siguiente paso de validacion es Fase 4, enfocada en el comportamiento del segmentador `Empresas[Empresas]`, combinaciones compatibles con `Empresas[Grupo Empresa]` y selecciones contradictorias.

Clasificacion documental:

- Las conclusiones, decisiones y riesgos permanecen en `Specs`.
- Las matrices operativas, resultados de pruebas y evidencia temporal se registran en `Outputs`.
- `Docs` no se modifica en esta ejecucion.

## Resultado Fase 4

Estado:

- `Fase 4 aprobada`.

Evidencia:

- La cascada `Grupo Empresa -> Empresa` fue validada con evidencia visual para 2026.
- Cada grupo muestra unicamente las empresas permitidas por la matriz funcional.
- Al limpiar `Grupo Empresa`, el segmentador `Empresa` vuelve al conjunto completo.
- Los graficos, tabla y KPI cambian entre grupos y no presentan campos no reconocidos.
- `Challenger` conserva visualizacion en millones; los demas grupos usan unidades automaticas segun magnitud.

Impacto:

- No se aplicaron cambios funcionales.
- No se modifica la conclusion de Fase 2.
- Las pruebas de empresa individual representativa, cambio de grupo con empresa previa y combinacion contradictoria se trasladan a Fase 6 como regresion residual obligatoria.
- Procede iniciar Fase 5 - Reconciliacion de visuales.

## Resultado Fase 5

Estado:

- `Fase 5 aprobada`.

Criterio funcional vigente:

- `Challenger` como seleccion exclusiva: millones y una cifra decimal.
- Todos los negocios o segmentador limpio: millones y una cifra decimal.
- Cualquier otro negocio o subconjunto parcial: unidades automaticas y una cifra decimal.

Evidencia:

- `../Outputs/03_2026-07-22_evidencia_fase5_reconciliacion_productividad.md`

Resultado por contexto:

- Sin filtro de negocio: pasa.
- `Challenger`: pasa.
- `Fundacion Challenger`: pasa.
- `Grupo Sky`: pasa.
- `Habitel Hotels`: pasa.
- `Lemco`: pasa.

Conclusion:

- Grafico mensual, grafico acumulado, tabla mensual, tabla KPI e indicador de tendencia reconciliaron en los contextos validados.
- No se reportaron discrepancias.
- No se aplicaron correcciones funcionales en Fase 5.
- Puede iniciarse Fase 6 - Regresion integral.

## Resultado Fase 6

Estado:

- `Fase 6 aprobada`.

Evidencia:

- `../Outputs/04_2026-07-22_evidencia_fase6_regresion_productividad.md`

Resumen:

- La Fase 6 fue aprobada por validacion manual del usuario.
- Se ejecutaron escenarios residuales de periodos, meses, empresas individuales, selecciones multiples, jerarquia, combinaciones contradictorias y regresion transversal minima.
- No se reportaron fallas funcionales bloqueantes.
- No se aplicaron correcciones adicionales en PBIP/TMDL durante Fase 6.
- Puede iniciarse Fase 7 - Documentacion y preparacion de commit.

## Estado vigente para preparacion de commit

Regla funcional vigente:

- `Challenger` exclusivo: importes en millones y una cifra decimal.
- Consolidado completo, todos los negocios o filtros de negocio limpios: importes en millones y una cifra decimal.
- Cualquier contexto parcial restante: unidades automaticas y una cifra decimal.
- Las medidas se conservan numericas; no se utiliza `FORMAT()`.

Trazabilidad historica:

- Los apartados anteriores que describen seleccion multiple o filtros limpios como automaticos corresponden a alternativas superadas durante la implementacion.
- La regla vigente es la validada hasta Fase 6 y debe prevalecer para Productividad y Gasto Laboral.

Fase 7:

- Estado: en preparacion.
- El paquete de commit aun requiere aislamiento por archivo y por hunk para separar cambios funcionales aprobados, reparaciones tecnicas necesarias, drift de Power BI Desktop y cambios ya presentes en `origin/main`.
