# Plan de implementacion - correccion de Productividad por periodo y contexto de negocio

Fecha: 2026-07-21

Estado: plan ejecutable por fases. No implementa cambios funcionales adicionales.

Spec de origen: `Specs/0004_analisis_impacto_correccion_productividad_filtros_negocio.md`

Worktree operativo: `C:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal\.wt\prod`

Rama esperada: `fix/productividad-contexto-negocio`

## Objetivo

Completar el requerimiento de Mateo en la pagina `Productividad`:

1. corregir el texto fijo `Ejecucion 2025`;
2. validar y corregir que `Challenger` no muestre el consolidado si debe filtrar solo Challenger;
3. validar y corregir que otros negocios no dejen la tabla en cero cuando existen datos;
4. terminar con evidencia funcional, diff controlado y preparacion de commit.

## Alcance

El alcance se limita a:

- pagina `Productividad`;
- carpeta PBIR `PBIP/Proyecto.Report/definition/pages/ReportSection65569958420c423d90b1/`;
- medidas estrictamente necesarias en `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl`;
- relaciones solo si la evidencia demuestra una relacion activa faltante o incorrecta;
- Spec 0004 y este plan.

## Fuera de alcance

No incluye:

- fuentes Power Query;
- Formula Firewall;
- SST ni el worktree `.wt\sst`;
- otras paginas;
- navegacion global;
- colores, posiciones, tamanos o diseno;
- `Docs/`, `Outputs/`, `Data/`, bookmarks, `pages.json`, `diagramLayout.json` o `cultures/es-ES.tmdl`;
- commit o push sin aprobacion explicita.

## Estado de implementacion actual

El worktree `.wt\prod` contiene cuatro cambios pendientes:

| Archivo | Estado | Proposito |
|---|---|---|
| `Specs/0004_analisis_impacto_correccion_productividad_filtros_negocio.md` | nuevo | Analisis de impacto inicial. |
| `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl` | modificado | Medida `Titulo_Productividad_Gasto_Laboral`. |
| `PBIP/Proyecto.Report/definition/pages/ReportSection65569958420c423d90b1/visuals/d6010674e3a075647581/visual.json` | modificado | Leyenda `Ejecucion` y titulo dinamico. |
| `PBIP/Proyecto.Report/definition/pages/ReportSection65569958420c423d90b1/visuals/cba349945ec4b0577321/visual.json` | modificado | Unidades visibles sin escalado forzado a millones y una cifra decimal. |

Estos cambios no han sido validados visualmente en Power BI Desktop.

## Supuestos confirmados

- La pagina `Productividad` esta en `ReportSection65569958420c423d90b1`.
- Los segmentadores usan:
  - `Años[Año]`;
  - `Mes[Meses]`;
  - `Empresas[Grupo Empresa]`;
  - `Empresas[Empresas]`.
- Las medidas principales revisadas son `Efic`, `%Efiprom`, `KPI_EFI` y `Var_GL`.
- Existe relacion `Planta Ppto[Empresa]` -> `Empresas[Empresas]`.
- Existe relacion `Planta Ppto[Año]` -> `Años[Año]`.
- Existe relacion `Planta Ppto[Mes]` -> `Mes[Meses]`.
- No se encontro uso directo de `ALL`, `REMOVEFILTERS`, `ALLEXCEPT` ni filtro fijo a Challenger en `Efic` o `%Efiprom`.

## Asuntos aun no demostrados

- Que la seleccion de `Grupo Empresa` filtre correctamente cada visual de Productividad.
- Que la seleccion de `Empresas` sea compatible con `Grupo Empresa`.
- Que las claves de `Planta Ppto[Empresa]` empaten con `Empresas[Empresas]` para todos los negocios.
- Que existan datos reales por negocio para los escenarios reportados.
- Que los cambios parciales funcionen en Power BI Desktop.
- Que no haya bookmarks o estados persistidos que alteren la lectura.

## Dependencias

- Power BI Desktop debe abrir el PBIP desde `.wt\prod`, no desde el repositorio principal.
- Las busquedas desde el repositorio principal deben excluir `.wt/**`.
- El worktree `.wt\sst` permanece bloqueado y fuera de alcance.
- La validacion puede usar datos ya cargados si Formula Firewall impide refresh completo.

## Estrategia por fases

Las fases son secuenciales. Una fase no inicia hasta que la anterior tenga evidencia suficiente. Si aparece un fallo localizado, se regresa solo a la fase responsable. No se repite un diagnostico ya aceptado y no se hace commit parcial antes de la fase de control de cambios.

## Criterios globales de aceptacion

- El titulo responde al ano seleccionado: 2025 muestra `Ejecucion 2025`, 2026 muestra `Ejecucion 2026`.
- La leyenda no queda fija a `Ejecucion 2025`.
- Challenger filtra solo Challenger, salvo evidencia de datos que demuestre igualdad con el consolidado.
- Fundacion Challenger, Grupo Sky, Habitel Hotels y Lemco filtran sus propios datos cuando existen registros.
- Una empresa individual filtra solo esa empresa.
- Selecciones contradictorias no muestran datos de otro negocio.
- Graficos, tabla y tarjetas reconciliados bajo el mismo contexto.
- No se ocultan errores con ceros o `BLANK()`.
- No se modifican fuentes, relaciones generales, otras paginas ni diseno.

## Estrategia Git

- Trabajar solo en `.wt\prod`.
- No usar `git add .` ni `git add -A`.
- No hacer staging, commit o push hasta la fase autorizada.
- Preparar staging solo con rutas explicitas.
- Mantener `.wt/**` excluido del repositorio principal mediante `.git/info/exclude`.

## Estrategia de validacion Power BI Desktop

- Abrir `PBIP/Proyecto7.pbip` desde `.wt\prod`.
- No abrir simultaneamente el PBIP del repositorio principal.
- Validar con datos cargados existentes si el refresh completo esta bloqueado por Formula Firewall.
- Registrar evidencia por fase: resultado observado, filtros aplicados, visuales afectados, errores exactos.

## Riesgos y mitigaciones

| Riesgo | Mitigacion |
|---|---|
| Validar el PBIP equivocado desde el repositorio principal. | Usar ruta absoluta de `.wt\prod` en cada prompt. |
| Mezclar cambios de SST o del arbol principal. | Excluir `.wt\sst` y no trabajar fuera de `.wt\prod`. |
| Repetir diagnosticos y consumir tiempo. | Fase 2 es el unico diagnostico completo de propagacion empresarial. |
| Cambiar relaciones sin necesidad. | Priorizar interacciones, campos y medidas localizadas antes de relaciones. |
| Formula Firewall impide refresh. | No confundir refresh con validacion visual de datos cargados. |

## Plan de rollback

- Si falla la validacion del titulo, revertir solo la medida `Titulo_Productividad_Gasto_Laboral` y el enlace del titulo en `d6010674e3a075647581`.
- Si falla la tabla, revertir solo `labelDisplayUnits` y `labelPrecision` en `cba349945ec4b0577321`.
- Si una correccion posterior de filtros falla, revertir el archivo exacto modificado en esa fase mediante un parche controlado; no usar `git reset` ni `git restore` sobre cambios ajenos.

## Matriz de trazabilidad

| Requerimiento | Fase responsable | Prueba |
|---|---|---|
| Titulo no fijo a 2025 | Fase 1 | Cambiar ano 2025/2026 y observar titulo. |
| Challenger no igual al consolidado por error | Fase 2 y 3 | Comparar sin filtro vs Challenger. |
| Otros negocios no quedan en cero si hay datos | Fase 2, 3 y 4 | Validar Grupo Sky, Habitel Hotels, Lemco y Fundacion Challenger. |
| Empresa individual filtra correctamente | Fase 4 | Seleccionar empresa y reconciliar tabla/graficos. |
| Todos los visuales responden al mismo contexto | Fase 5 | Comparar graficos, tabla y tarjetas. |
| Regresion general | Fase 6 | Casos 2025, 2026, seleccion unica, multiple y sin seleccion. |
| Commit limpio | Fase 7 y 8 | Staging selectivo y diff revisado. |

## Fase 0 - Baseline y preservacion

Objetivo: confirmar el estado exacto del worktree, revisar el diff existente y documentar el punto de partida sin modificar funcionalidad.

Condicion de entrada: `.wt\prod` existe, rama `fix/productividad-contexto-negocio`, sin staging.

Archivos permitidos: Spec 0004 y este plan solo para actualizar evidencia.

Archivos excluidos: todo `PBIP/`, `Docs/`, `Outputs/`, `Data/`, `.wt\sst`.

Actividades: ejecutar preflight, listar cambios, revisar diff, confirmar que los cuatro cambios esperados siguen presentes.

Comandos permitidos: `git status -sb`, `git diff --cached --name-status`, `git diff --name-status`, `git diff --stat`, `git diff --check`, `git worktree list --verbose`, `rg --glob '!.wt/**'`.

Validaciones: staging vacio, rama correcta, sin cambios inesperados.

Pruebas funcionales: no aplica.

Evidencia esperada: estado Git y lista de archivos.

Criterio de aceptacion: baseline documentado y sin drift.

Condicion para detenerse: staging activo, rama incorrecta o cambios no esperados.

Riesgos: confundir worktree con repositorio principal.

Rollback: no aplica, fase sin cambios funcionales.

Entregables: resumen de baseline.

Condicion para avanzar: baseline aprobado.

### Instruccion para IA - Fase 0

```text
Actua como auditor Git y PBIP. Trabaja solo en:
C:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal\.wt\prod

Rama esperada: fix/productividad-contexto-negocio.

Objetivo exclusivo: ejecutar baseline y preservar el alcance. No modifiques funcionalidad.

Archivos que puedes modificar: ninguno, salvo agregar evidencia al final de Specs/0005_plan_implementacion_correccion_productividad_contexto_negocio.md si el usuario lo autoriza en esta fase.

Archivos prohibidos: PBIP/**, Docs/**, Outputs/**, Data/**, .wt/sst/**, bookmarks, pages.json, diagramLayout.json, cultures/es-ES.tmdl.

Preflight unico:
- git status -sb
- git diff --cached --name-status
- git diff --name-status
- git diff --stat
- git diff --check
- git worktree list --verbose

Acciones:
1. Confirma rama, HEAD, staging y archivos modificados.
2. Confirma que existen exactamente los cambios esperados: Spec 0004, Tbl_Medidas.tmdl, visual d6010674e3a075647581 y visual cba349945ec4b0577321.
3. No revises diagnosticos funcionales aun.

Validaciones: staging vacio, sin commit, sin push, sin cambios fuera del alcance.

Criterio de aceptacion: baseline claro y sin drift.

Detente si: hay staging activo, rama distinta, o cambios inesperados.

Entrega: estado Git, archivos modificados, riesgos y decision de si procede Fase 1.

No uses git add ., no uses git add -A, no hagas commit ni push. No avances a Fase 1 automaticamente.
```

## Fase 1 - Validacion de cambios parciales

Objetivo: validar en Power BI Desktop los cambios ya implementados: titulo dinamico, leyenda sin 2025, tabla con una cifra decimal y sin escalado forzado.

Condicion de entrada: Fase 0 aprobada.

Archivos permitidos: `Tbl_Medidas.tmdl`, `d6010674e3a075647581/visual.json`, `cba349945ec4b0577321/visual.json`, Spec 0004 y este plan.

Archivos excluidos: otras paginas, relaciones, fuentes, bookmarks, `pages.json`, `diagramLayout.json`, `cultures/es-ES.tmdl`.

Actividades: abrir PBIP desde `.wt\prod`, validar titulo con 2025/2026, revisar tabla y leyenda, corregir solo si falla lo ya implementado.

Comandos permitidos: comandos Git de solo lectura, validadores JSON, busquedas `rg --glob '!.wt/**'`.

Validaciones: JSON valido, TMDL parseable visualmente, `git diff --check`.

Pruebas funcionales: ano 2025, ano 2026, sin seleccion unica de ano.

Evidencia esperada: resultado visual de Power BI Desktop.

Criterio de aceptacion: titulo y tabla funcionan segun lo implementado.

Condicion para detenerse: PBIP no abre, error de TMDL/PBIR o cambio parcial no funciona y no se puede corregir localmente.

Riesgos: Power BI Desktop genera ruido al guardar.

Rollback: revertir por parche solo los tres archivos funcionales si el cambio parcial rompe la pagina.

Entregables: resultado de validacion y archivos tocados.

Condicion para avanzar: cambios parciales validados.

### Instruccion para IA - Fase 1

```text
Actua como validador Power BI Desktop y auditor PBIP. Trabaja solo en:
C:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal\.wt\prod

Rama esperada: fix/productividad-contexto-negocio.

Estado previo esperado: Fase 0 aprobada; existen cambios pendientes en Spec 0004, Tbl_Medidas.tmdl y los visuales d6010674e3a075647581 y cba349945ec4b0577321.

Objetivo exclusivo: validar los cambios parciales ya implementados. No diagnostiques todavia la propagacion empresarial.

Puedes modificar solo:
- PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl
- PBIP/Proyecto.Report/definition/pages/ReportSection65569958420c423d90b1/visuals/d6010674e3a075647581/visual.json
- PBIP/Proyecto.Report/definition/pages/ReportSection65569958420c423d90b1/visuals/cba349945ec4b0577321/visual.json
- Specs/0004_analisis_impacto_correccion_productividad_filtros_negocio.md
- Specs/0005_plan_implementacion_correccion_productividad_contexto_negocio.md

No puedes modificar otras paginas, relaciones, fuentes, bookmarks, pages.json, diagramLayout.json, cultures/es-ES.tmdl, Docs, Outputs, Data ni .wt/sst.

Preflight unico:
- git status -sb
- git diff --cached --name-status
- git diff --check

Acciones:
1. Abre PBIP/Proyecto7.pbip desde este worktree.
2. En Productividad valida ano 2026 y ano 2025.
3. Confirma que el titulo cambia con el ano.
4. Confirma que la leyenda no diga Ejecucion 2025.
5. Confirma que la tabla muestra una cifra decimal y no fuerza millones.
6. Si falla solo lo implementado, corrige el archivo exacto.

Validaciones:
- JSON valido en los visuales modificados.
- git diff --check.
- no cambios de Desktop fuera del alcance.

Criterio de aceptacion: cambios parciales validados en Desktop.

Detente si: el PBIP no abre, hay error de TMDL/PBIR, o Power BI genera cambios masivos.

Entrega: evidencias, archivos modificados, limitaciones y decision de si procede Fase 2.

No uses git add ., no uses git add -A, no hagas staging, commit ni push. No avances a Fase 2 automaticamente.
```

## Fase 2 - Diagnostico unico de propagacion empresarial

Objetivo: determinar con evidencia la causa real de Challenger como consolidado y otros negocios en cero.

Condicion de entrada: Fase 1 validada.

Archivos permitidos: Spec 0004 y este plan para evidencia; no modificar PBIP en esta fase salvo aprobacion expresa al cierre.

Archivos excluidos: cambios funcionales PBIP, fuentes, relaciones y visuales.

Actividades: revisar slicers, relaciones, claves, valores sin correspondencia, interacciones, filtros, bookmarks, medidas DAX, existencia real de datos.

Comandos permitidos: `rg --glob '!.wt/**'`, `git grep`, scripts de lectura, `git diff`, validadores de JSON/TMDL.

Validaciones: matriz de causa raiz con evidencia.

Pruebas funcionales: revisar en Desktop los filtros por Grupo Empresa y Empresas sin aplicar correcciones.

Evidencia esperada: causa clasificada: interaccion, campo incorrecto, relacion, clave, medida, filtro persistido, bookmark o ausencia real de datos.

Criterio de aceptacion: una causa raiz demostrada o bloqueo claro.

Condicion para detenerse: dos interpretaciones funcionales igualmente validas o datos ausentes sin evidencia.

Riesgos: repetir busquedas amplias innecesarias.

Rollback: no aplica si no hay cambios funcionales.

Entregables: matriz diagnostica.

Condicion para avanzar: causa raiz aceptada.

### Instruccion para IA - Fase 2

```text
Actua como arquitecto Power BI/PBIP, auditor DAX y analista de relaciones. Trabaja solo en:
C:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal\.wt\prod

Rama esperada: fix/productividad-contexto-negocio.

Estado previo esperado: Fase 1 validada; no hay staging.

Objetivo exclusivo: diagnosticar una sola vez la propagacion empresarial en Productividad.

Puedes modificar solo:
- Specs/0004_analisis_impacto_correccion_productividad_filtros_negocio.md
- Specs/0005_plan_implementacion_correccion_productividad_contexto_negocio.md

No puedes modificar PBIP, Docs, Outputs, Data, .wt/sst ni archivos de otras paginas.

Preflight unico:
- git status -sb
- git diff --cached --name-status
- git diff --check

Acciones:
1. Identifica visuales y slicers de Productividad ya listados en Spec 0004.
2. Revisa relaciones de Planta Ppto, Empresas, Años y Mes.
3. Revisa si Grupo Empresa y Empresas filtran graficos, tabla y tarjetas.
4. Revisa filtros de pagina/visual y bookmarks relacionados.
5. Revisa medidas Efic, %Efiprom, KPI_EFI, Var_GL y totales de tabla.
6. Valida si existen datos por Challenger, Fundacion Challenger, Grupo Sky, Habitel Hotels y Lemco con datos cargados en Desktop si es posible.
7. Clasifica la causa raiz y no implementes la correccion.

Validaciones: evidencia por cada hipotesis descartada o confirmada.

Criterio de aceptacion: causa raiz unica demostrada o bloqueo documentado.

Detente si: se requiere remodelacion amplia o no se puede determinar la fuente oficial de empresa.

Entrega: causa raiz, evidencia, archivos potenciales de correccion y decision de si procede Fase 3.

No uses git add ., no uses git add -A, no hagas staging, commit ni push. No repitas este diagnostico en fases posteriores. No avances a Fase 3 automaticamente.
```

## Fase 3 - Correccion del contexto de Grupo Empresa

Objetivo: implementar la solucion minima demostrada para que cada Grupo Empresa filtre su informacion.

Condicion de entrada: Fase 2 con causa raiz aceptada.

Archivos permitidos: solo los archivos que Fase 2 identifique como necesarios.

Archivos excluidos: otras paginas, fuentes, cambios masivos de relaciones, bidireccionalidad sin evidencia.

Actividades: aplicar correccion minima en interacciones, campos, relaciones activas o medidas localizadas.

Comandos permitidos: edicion controlada, `rg`, validadores, `git diff`.

Validaciones: JSON/TMDL valido y comportamiento por cada grupo.

Pruebas funcionales: Challenger, Fundacion Challenger, Grupo Sky, Habitel Hotels, Lemco.

Evidencia esperada: cada grupo filtra sus datos.

Criterio de aceptacion: no hay consolidado indebido ni ceros artificiales por grupo.

Condicion para detenerse: solucion exige bidireccionalidad o refactor no aprobado.

Riesgos: corregir un grupo y romper otro.

Rollback: parche inverso del archivo modificado en esta fase.

Entregables: archivos modificados y pruebas por grupo.

Condicion para avanzar: filtros de Grupo Empresa validados.

### Instruccion para IA - Fase 3

```text
Actua como implementador Power BI/PBIP y auditor de control de cambios. Trabaja solo en:
C:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal\.wt\prod

Rama esperada: fix/productividad-contexto-negocio.

Estado previo esperado: Fase 2 cerrada con causa raiz documentada.

Objetivo exclusivo: corregir el contexto de Grupo Empresa segun la causa demostrada en Fase 2.

Puedes modificar solo los archivos identificados por Fase 2. Si Fase 2 no autoriza un archivo, no lo modifiques.

No puedes modificar otras paginas, fuentes Power Query, bookmarks, pages.json, diagramLayout.json, cultures/es-ES.tmdl, Docs, Outputs, Data ni .wt/sst.

Preflight unico:
- git status -sb
- git diff --cached --name-status
- git diff --check

Acciones:
1. Lee la conclusion de Fase 2 en Specs/0004 y Specs/0005.
2. Implementa la correccion minima: interaccion, campo de visual, relacion activa o medida localizada.
3. No habilites bidireccionalidad salvo aprobacion explicita registrada.
4. No uses FORMAT() ni conviertas medidas numericas en texto.
5. Valida en Desktop: Challenger, Fundacion Challenger, Grupo Sky, Habitel Hotels y Lemco.

Validaciones:
- JSON/TMDL valido.
- git diff --check.
- diff limitado a archivos autorizados.

Criterio de aceptacion: cada Grupo Empresa filtra exclusivamente su informacion.

Detente si: la correccion requiere remodelacion amplia o cambia resultados fuera de Productividad.

Entrega: solucion aplicada, evidencia por grupo, archivos modificados y decision de si procede Fase 4.

No uses git add ., no uses git add -A, no hagas staging, commit ni push. No repitas el diagnostico de Fase 2. No avances a Fase 4 automaticamente.
```

## Fase 4 - Correccion y validacion del filtro Empresas

Objetivo: validar seleccion individual de empresa, coherencia con Grupo Empresa y selecciones contradictorias.

Condicion de entrada: Fase 3 validada.

Archivos permitidos: solo archivos identificados para correccion de Empresa.

Archivos excluidos: fuentes, otras paginas y cambios generales de modelo.

Actividades: probar empresa individual, limpiar filtro, combinar Grupo Empresa y Empresas, corregir si hay contradiccion.

Comandos permitidos: Git lectura, validadores, edicion minima si causa demostrada.

Validaciones: empresa individual no trae datos de otro negocio.

Pruebas funcionales: una empresa por cada grupo con datos.

Evidencia esperada: matriz de seleccion empresa/grupo.

Criterio de aceptacion: filtros compatibles muestran datos correctos; contradictorios no muestran datos ajenos.

Condicion para detenerse: no hay datos para validar empresas individuales.

Riesgos: sincronizacion de slicers persistida.

Rollback: parche inverso local.

Entregables: resultado por empresa.

Condicion para avanzar: filtros de Empresa validados.

### Instruccion para IA - Fase 4

```text
Actua como validador funcional Power BI y auditor PBIP. Trabaja solo en:
C:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal\.wt\prod

Rama esperada: fix/productividad-contexto-negocio.

Estado previo esperado: Fase 3 aprobada.

Objetivo exclusivo: validar y corregir el filtro Empresas en Productividad.

Puedes modificar solo archivos autorizados por evidencia de Fase 4. Preferir no modificar si la validacion pasa.

No puedes modificar otras paginas, fuentes, relaciones generales, bookmarks, pages.json, diagramLayout.json, cultures/es-ES.tmdl, Docs, Outputs, Data ni .wt/sst.

Preflight unico:
- git status -sb
- git diff --cached --name-status
- git diff --check

Acciones:
1. Abre PBIP/Proyecto7.pbip desde .wt/prod.
2. Valida una empresa dentro de Challenger, Fundacion Challenger, Grupo Sky, Habitel Hotels y Lemco cuando haya datos.
3. Limpia el slicer Empresas y valida regreso al grupo.
4. Prueba una seleccion compatible Grupo Empresa + Empresa.
5. Prueba una seleccion contradictoria y confirma que no muestra datos de otro negocio.
6. Corrige solo si hay evidencia exacta.

Validaciones: JSON/TMDL valido si se edita, git diff --check, sin cambios fuera del alcance.

Criterio de aceptacion: Empresas y Grupo Empresa son coherentes.

Detente si: faltan datos para validar o la correccion requiere cambio de modelo amplio.

Entrega: matriz de pruebas, cambios si aplica y decision de si procede Fase 5.

No uses git add ., no uses git add -A, no hagas staging, commit ni push. No repitas Fase 2. No avances a Fase 5 automaticamente.
```

## Fase 5 - Reconciliacion de visuales

Objetivo: validar graficos, tabla y tarjetas bajo el mismo contexto.

Condicion de entrada: Fase 4 validada.

Archivos permitidos: solo visuales o medidas de Productividad si aparece una discrepancia demostrada.

Archivos excluidos: fuentes, otras paginas, modelo no relacionado.

Actividades: comparar gasto laboral, ventas, ingreso operacional, productividad, porcentajes y KPI.

Comandos permitidos: Git lectura, validadores, edicion minima.

Validaciones: los visuales reconcilian bajo el mismo filtro.

Pruebas funcionales: sin seleccion, seleccion unica, seleccion multiple.

Evidencia esperada: tabla de conciliacion por visual.

Criterio de aceptacion: no hay visual que ignore el contexto o muestre datos incoherentes.

Condicion para detenerse: discrepancia sin medida fuente identificable.

Riesgos: confundir redondeo visual con calculo.

Rollback: parche inverso del visual/medida tocada.

Entregables: reconciliacion.

Condicion para avanzar: visuales reconciliados.

### Instruccion para IA - Fase 5

```text
Actua como especialista Power BI, DAX y validacion funcional. Trabaja solo en:
C:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal\.wt\prod

Rama esperada: fix/productividad-contexto-negocio.

Estado previo esperado: Fase 4 aprobada.

Objetivo exclusivo: reconciliar visuales de Productividad bajo el mismo contexto.

Puedes modificar solo visuales o medidas de Productividad si una discrepancia queda demostrada.

No puedes modificar fuentes, relaciones amplias, otras paginas, bookmarks, pages.json, diagramLayout.json, cultures/es-ES.tmdl, Docs, Outputs, Data ni .wt/sst.

Preflight unico:
- git status -sb
- git diff --cached --name-status
- git diff --check

Acciones:
1. Valida graficos superiores, grafico mensual, tabla inferior, tabla KPI y tarjeta KPI.
2. Compara ventas, gasto laboral, ingreso operacional, productividad y porcentajes.
3. Prueba sin seleccion, Challenger, otros grupos y seleccion multiple.
4. Corrige solo si un visual usa campos, filtros o medidas inconsistentes.
5. No sustituyas errores con ceros o BLANK().

Validaciones: JSON/TMDL valido, git diff --check, diff limitado.

Criterio de aceptacion: todos los visuales responden al mismo contexto.

Detente si: hay discrepancia que requiere definicion funcional de negocio.

Entrega: reconciliacion por visual, cambios si aplica y decision de si procede Fase 6.

No uses git add ., no uses git add -A, no hagas staging, commit ni push. No repitas Fase 2. No avances a Fase 6 automaticamente.
```

## Fase 6 - Regresion y validacion integral

Objetivo: probar escenarios completos y registrar evidencia de Power BI Desktop.

Condicion de entrada: Fase 5 validada.

Archivos permitidos: Specs para evidencia; no modificar PBIP salvo correccion puntual aprobada.

Archivos excluidos: cambios funcionales nuevos no relacionados.

Actividades: validar anos, grupos, empresas, meses, seleccion multiple y paginas relacionadas.

Comandos permitidos: Git lectura, validadores.

Validaciones: JSON, TMDL, diff y Desktop.

Pruebas funcionales: todos los escenarios globales.

Evidencia esperada: matriz de regresion.

Criterio de aceptacion: requerimiento completo validado.

Condicion para detenerse: error funcional nuevo.

Riesgos: Formula Firewall se confunde con validacion visual.

Rollback: regresar a fase responsable.

Entregables: evidencia integral.

Condicion para avanzar: validacion integral aprobada.

### Instruccion para IA - Fase 6

```text
Actua como auditor funcional Power BI Desktop y PBIP. Trabaja solo en:
C:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal\.wt\prod

Rama esperada: fix/productividad-contexto-negocio.

Estado previo esperado: Fase 5 aprobada.

Objetivo exclusivo: ejecutar regresion integral de Productividad. No implementar nuevas funciones.

Puedes modificar solo Specs/0004 y Specs/0005 para registrar evidencia. Si aparece un error funcional, detente y remite a la fase responsable.

No puedes modificar PBIP, Docs, Outputs, Data ni .wt/sst sin aprobacion especifica.

Preflight unico:
- git status -sb
- git diff --cached --name-status
- git diff --check

Acciones:
1. Abre PBIP/Proyecto7.pbip desde .wt/prod.
2. Valida anos 2025 y 2026.
3. Valida cada Grupo Empresa.
4. Valida empresas individuales.
5. Valida seleccion unica, multiple y sin seleccion.
6. Valida meses, graficos, tabla, tarjetas y paginas relacionadas.
7. Documenta Formula Firewall solo como limitacion preexistente si aparece.

Validaciones: matriz de pruebas completa y sin errores de campos no reconocidos.

Criterio de aceptacion: todos los escenarios pasan o quedan limitaciones claras no bloqueantes.

Detente si: un escenario falla y requiere correccion.

Entrega: matriz de regresion, limitaciones y decision de si procede Fase 7.

No uses git add ., no uses git add -A, no hagas staging, commit ni push. No avances a Fase 7 automaticamente.
```

## Fase 7 - Documentacion y preparacion de commit

Objetivo: actualizar Specs con resultados finales, validar diff y preparar staging propuesto.

Condicion de entrada: Fase 6 aprobada.

Archivos permitidos: Spec 0004, Spec 0005 y archivos funcionales ya validados.

Archivos excluidos: todo cambio no relacionado.

Actividades: actualizar estado final, validar JSON/TMDL, ejecutar diff y proponer staging.

Comandos permitidos: Git lectura, validadores, edicion documental.

Validaciones: `git diff --check`, `git diff --cached --name-status` debe seguir vacio.

Pruebas funcionales: no nuevas, usar evidencia Fase 6.

Evidencia esperada: diff final resumido.

Criterio de aceptacion: paquete listo para aprobacion de commit.

Condicion para detenerse: diff incluye archivos ajenos.

Riesgos: incluir ruido de Desktop.

Rollback: retirar del paquete cualquier archivo no aprobado mediante no-staging; no revertir cambios ajenos.

Entregables: staging propuesto y mensaje.

Condicion para avanzar: aprobacion explicita del usuario.

### Instruccion para IA - Fase 7

```text
Actua como auditor Git/PBIP y responsable de staging selectivo. Trabaja solo en:
C:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal\.wt\prod

Rama esperada: fix/productividad-contexto-negocio.

Estado previo esperado: Fase 6 aprobada.

Objetivo exclusivo: preparar el paquete de commit, sin hacer staging ni commit.

Puedes modificar:
- Specs/0004_analisis_impacto_correccion_productividad_filtros_negocio.md
- Specs/0005_plan_implementacion_correccion_productividad_contexto_negocio.md

No puedes modificar funcionalidad nueva, otras paginas, Docs, Outputs, Data ni .wt/sst.

Preflight unico:
- git status -sb
- git diff --cached --name-status
- git diff --check

Acciones:
1. Actualiza Specs con resultados finales.
2. Valida JSON de visuales modificados.
3. Valida TMDL de Tbl_Medidas.
4. Revisa diff completo.
5. Propone staging con rutas explicitas.
6. Propone mensaje: fix(productividad): corrige periodo y filtros por negocio.

Validaciones:
- git diff --check sin errores.
- git diff --cached --name-status vacio.
- no hay archivos ajenos en el paquete propuesto.

Criterio de aceptacion: usuario puede aprobar commit con evidencia suficiente.

Detente si: hay ruido de Desktop o archivos no relacionados.

Entrega: archivos candidatos, archivos excluidos, diff resumido y mensaje propuesto.

No uses git add ., no uses git add -A, no hagas staging, commit ni push. No avances a Fase 8 automaticamente.
```

## Fase 8 - Commit y push controlados

Objetivo: ejecutar commit y push solo con aprobacion explicita.

Condicion de entrada: aprobacion del usuario despues de Fase 7.

Archivos permitidos: los aprobados explicitamente.

Archivos excluidos: todo lo demas.

Actividades: verificar identidad, staging selectivo, commit unico y push.

Comandos permitidos: Git de staging explicito, commit y push normal.

Validaciones: staging exacto, identidad correcta, rama correcta y revision de divergencia frente a remotos.

Pruebas funcionales: evidencia ya aprobada.

Evidencia esperada: hash y push exitoso.

Criterio de aceptacion: origin actualizado solo con el commit aprobado.

Condicion para detenerse: divergencia inesperada con la rama remota de la propia feature, hunks no resueltos frente a `origin/main`, conflictos conocidos, staging inesperado o identidad incorrecta. La existencia de commits nuevos en `origin/main` se registra, pero no bloquea por si sola el commit de la rama de trabajo; la integracion definitiva permanece en Fase 9.

Riesgos: mezclar cambios no aprobados.

Rollback: revert posterior del commit si se aprueba; no usar reset.

Entregables: hash, archivos incluidos y estado final.

Condicion para cierre: push exitoso y rama alineada.

### Instruccion para IA - Fase 8

```text
Actua como auditor Git y responsable de publicacion. Trabaja solo en:
C:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal\.wt\prod

Rama esperada: fix/productividad-contexto-negocio.

Estado previo esperado: usuario aprobo explicitamente el commit despues de Fase 7.

Objetivo exclusivo: crear un unico commit y hacer push de los archivos aprobados.

Puedes stagear solo rutas aprobadas por el usuario en Fase 7.

No puedes incluir archivos ajenos, .wt/sst, Docs, Outputs, Data, bookmarks no aprobados, pages.json, diagramLayout.json ni cultures/es-ES.tmdl salvo aprobacion textual exacta.

Preflight unico:
- git status -sb
- git diff --cached --name-status
- git config --local --get user.name
- git config --local --get user.email
- git fetch origin
- git log --oneline HEAD..origin/main
- git log --oneline origin/main..HEAD

Acciones:
1. Verifica identidad Git esperada.
2. Stagea con rutas explicitas; no uses git add . ni git add -A.
3. Ejecuta git diff --cached --name-status, git diff --cached --check y git diff --cached --stat.
4. Si staging es exacto, commit: fix(productividad): corrige periodo y filtros por negocio.
5. Push normal a la rama remota acordada, sin --force.

Validaciones posteriores:
- git status -sb
- git log --oneline -1
- git log --oneline HEAD..origin/<rama>
- git log --oneline origin/<rama>..HEAD

Criterio de aceptacion: commit y push exitosos sin archivos ajenos.

Detente si: identidad incorrecta, remotos pendientes, staging inesperado o rama distinta.

Entrega: hash, archivos incluidos, rama, resultado del push y confirmacion de exclusiones.
```

## Fase 9 - Integracion controlada en main

Objetivo: integrar de manera segura el commit aprobado de `fix/productividad-contexto-negocio` en `main`.

Condiciones de entrada:

- Fase 8 completada.
- Commit y push de la rama confirmados.
- Fase 6 aprobada.
- Paquete de archivos validado.
- Identidad Git correcta.
- Staging vacio.
- Cambios de `origin/main` identificados.
- Cambios manuales del worktree principal protegidos.

Actividades:

1. Ejecutar `fetch` de `origin`.
2. Comparar `origin/main` frente a la rama de Productividad.
3. Comparar la rama de Productividad frente a `origin/main`.
4. Integrar primero los cambios recientes de `main` en un entorno seguro.
5. Resolver conflictos conservando:
   - cambios aprobados de Productividad;
   - cambios recientes validos de `main`;
   - `compatibilityLevel 1601`;
   - visual superpuesto `f0d2c4b6a8e14c5397bd`;
   - logica de unidades aprobada.
6. Validar nuevamente JSON, TMDL y ausencia de medidas duplicadas.
7. Integrar la rama en `main` mediante Pull Request o merge controlado.
8. Hacer push normal de `main`, sin force.
9. Actualizar el worktree principal sin destruir cambios locales.
10. Abrir desde el proyecto principal: `PBIP/Proyecto7.pbip`.
11. Validar apertura, pagina Productividad, titulo, subtitulo, filtros empresariales, unidades, tabla, graficos, KPI y ausencia de campos no reconocidos.

Restricciones:

- No usar `git add .` ni `git add -A`.
- No usar `--force`.
- No usar `reset`, `clean` o `restore` sobre cambios ajenos.
- No tocar `.wt/sst`.
- No reemplazar manualmente carpetas completas.
- No ejecutar esta fase sin aprobacion explicita.

Criterio de aceptacion:

- `main` contiene el commit de Productividad.
- `origin/main` esta actualizado.
- El PBIP principal abre.
- Productividad conserva el comportamiento aprobado.
- No se pierden cambios externos.

### Instruccion para IA - Fase 9

```text
Actua como auditor Git e integrador PBIP. Trabaja segun la ruta aprobada para la integracion y no ejecutes esta fase sin autorizacion explicita del usuario.

Ramas esperadas:
- origen funcional: fix/productividad-contexto-negocio
- destino: main

Objetivo exclusivo: integrar de forma controlada el commit aprobado de Productividad en main y validar el PBIP principal.

No puedes modificar .wt/sst, no puedes usar git add ., git add -A, reset, restore, clean, push --force ni reemplazar carpetas completas.

Preflight:
- git status -sb
- git diff --cached --name-status
- git fetch origin
- git log --oneline origin/main..HEAD
- git log --oneline HEAD..origin/main
- git branch --show-current

Acciones:
1. Confirma que Fase 8 esta completada y aprobada.
2. Identifica commits recientes de origin/main.
3. Integra cambios recientes de main en entorno seguro.
4. Resuelve conflictos conservando compatibilityLevel 1601, visual f0d2c4b6a8e14c5397bd y logica de unidades aprobada.
5. Valida JSON, TMDL y cero medidas duplicadas.
6. Integra a main mediante PR o merge controlado, segun autorizacion.
7. Haz push normal de main.
8. Actualiza el worktree principal sin destruir cambios locales.
9. Abre PBIP/Proyecto7.pbip desde el proyecto principal y valida Productividad.

Criterio de aceptacion: main y origin/main contienen el cambio, PBIP principal abre y Productividad conserva el comportamiento aprobado.

Entrega: commits integrados, conflictos resueltos, validaciones, estado de main y resultado de apertura del PBIP principal.
```

## Fase 10 - Publicacion y validacion en Power BI

Objetivo: publicar la version integrada y validada del PBIP principal en el espacio de trabajo correspondiente.

Condiciones de entrada:

- Fase 9 aprobada.
- `main` actualizado.
- PBIP principal validado.
- Espacio de trabajo e informe de destino confirmados.
- Autorizacion explicita para publicar.

Actividades:

1. Abrir `PBIP/Proyecto7.pbip` desde `main`.
2. Confirmar que corresponde a la version integrada.
3. Identificar:
   - espacio de trabajo;
   - informe existente;
   - modelo semantico asociado;
   - impacto de reemplazo.
4. Publicar desde Power BI Desktop o mediante el proceso de despliegue autorizado.
5. Confirmar que el informe y el modelo semantico correctos fueron actualizados.
6. Abrir el informe en Power BI Service.
7. Validar pagina Productividad, titulo, subtitulo, filtros `Grupo Empresa` y `Empresa`, unidades, graficos, tablas, KPI y ausencia de errores.
8. Confirmar que Mateo puede consultar la version actualizada.

Restricciones:

- No publicar sin autorizacion explicita.
- No seleccionar un espacio de trabajo por suposicion.
- No reemplazar otro informe o modelo semantico.
- No ejecutar refresh ni modificar credenciales sin autorizacion.

Criterio de aceptacion:

- Informe publicado en el destino correcto.
- Version visible y funcional.
- Validacion posterior satisfactoria.
- Confirmacion de publicacion documentada.

### Instruccion para IA - Fase 10

```text
Actua como responsable de publicacion Power BI. No ejecutes esta fase sin autorizacion explicita del usuario.

Ubicacion esperada: proyecto principal en main, despues de Fase 9 aprobada.

Objetivo exclusivo: publicar y validar en Power BI Service la version integrada de Proyecto7.

No puedes publicar por suposicion, cambiar credenciales, ejecutar refresh, reemplazar otro informe o modelo semantico ni modificar Docs/PBIP sin autorizacion.

Preflight:
- confirmar main actualizado
- confirmar PBIP principal validado
- confirmar espacio de trabajo, informe y modelo semantico destino
- confirmar autorizacion explicita de publicacion

Acciones:
1. Abrir PBIP/Proyecto7.pbip desde main.
2. Confirmar que es la version integrada.
3. Publicar al destino confirmado.
4. Abrir Power BI Service.
5. Validar Productividad, filtros, unidades, visuales y ausencia de errores.
6. Confirmar que Mateo puede consultar la version actualizada.

Criterio de aceptacion: publicacion correcta, informe visible, Productividad funcional y confirmacion de acceso del usuario final.

Entrega: destino publicado, resultado de validacion, confirmacion de acceso y riesgos pendientes.
```

## Condicion de cierre del requerimiento

El requerimiento se cierra solo cuando:

- Fase 6 queda validada;
- Fase 7 presenta un paquete limpio;
- Fase 8 crea y publica el commit de la rama;
- Fase 9 integra los cambios en `main` y valida el PBIP principal;
- Fase 10 publica y valida el informe en Power BI, cuando la publicacion forme parte del alcance autorizado;
- se confirma que no se perdieron cambios ajenos;
- `Outputs` permanece fuera de Git;
- `.wt/sst` permanece intacto.

## Incidencia tecnica Fase 1 - medida duplicada Tot_Accidentes

Antes de completar la validacion visual de Fase 1, Power BI Desktop bloqueo la apertura del PBIP por `PFE_TM_OBJECT_NAME_ALREADY_EXISTS`: existian dos medidas `Tot_Accidentes` en el modelo.

Decision de desbloqueo:

- conservar `Tbl_Medidas[Tot_Accidentes]`, porque los visuales SST vigentes apuntan a `Tbl_Medidas.Tot_Accidentes`;
- eliminar solo la definicion duplicada en `PBIP/Proyecto.SemanticModel/definition/tables/ACCIDENTALIDAD.tmdl`;
- redirigir la entrada de cultura de `ACCIDENTALIDAD[Tot_Accidentes]` a `Tbl_Medidas[Tot_Accidentes]`;
- no cambiar la expresion DAX, relaciones, consultas, visuales de Productividad ni visuales SST.

Condicion para retomar Fase 1: confirmar que el PBIP abre sin el error de medida duplicada y que SST no muestra campos no reconocidos en los visuales que usan `Tot_Accidentes`.

## Incidencia tecnica Fase 1 - auditoria completa de medidas duplicadas

Despues de resolver `Tot_Accidentes`, Power BI Desktop reporto otro bloqueo por medida duplicada `ConteoP`. Se ejecuto una auditoria model-wide sobre `PBIP/Proyecto.SemanticModel/definition/tables/*.tmdl` y se identificaron 26 nombres duplicados.

Resolucion:

- `ConteoP` queda canonicamente en `AUSENTISMOS[ConteoP]`, porque las referencias PBIR activas apuntan a `AUSENTISMOS.ConteoP`.
- `Tot_Accidentes` queda canonicamente en `Tbl_Medidas[Tot_Accidentes]`, porque las referencias SST vigentes apuntan a `Tbl_Medidas.Tot_Accidentes`.
- Para el resto de duplicados, se conservaron las medidas en la tabla fuente que ya usan los visuales y se eliminaron las copias redundantes en `Tbl_Medidas`.

Validacion estatica:

- no quedan nombres de medidas duplicados;
- no quedan referencias PBIR a las copias eliminadas en `Tbl_Medidas`;
- `git diff --check` no reporta errores, solo advertencias LF -> CRLF.

Estado de apertura:

- Power BI Desktop abre una ventana `Proyecto7` desde `.wt\prod`;
- no se observo un cuadro `PFE_TM_OBJECT_NAME_ALREADY_EXISTS` en la enumeracion de ventanas;
- queda pendiente confirmacion visual de lienzo/Productividad y pruebas 2025, 2026 y seleccion multiple antes de aprobar Fase 1.

## Incidencia tecnica Fase 1 - referencias PBIR rotas posterior a deduplicacion

Al retomar Fase 1, la pagina Productividad seguia bloqueada por visuales con campos no reconocidos. La causa no era una nueva duplicidad de medidas, sino referencias PBIR que seguian apuntando a la tabla anterior de medidas.

Resolucion aplicada:

- `d6010674e3a075647581`: `Planta Ppto.Efic` y `Planta Ppto.%Efiprom` se redirigen a `Tbl_Medidas.Efic` y `Tbl_Medidas.%Efiprom`.
- `76fbb82301d3f6b571c3`: `Planta Ppto.Efic` y `Planta Ppto.%Efiprom` se redirigen a `Tbl_Medidas.Efic` y `Tbl_Medidas.%Efiprom`.
- `cba349945ec4b0577321`: `Planta Ppto.Efic` se redirige a `Tbl_Medidas.Efic`.
- `9bcb53c0b346ba0d28c4`: `Planta Ppto.Efic` y `Planta Ppto.%Efiprom` se redirigen a `Tbl_Medidas.Efic` y `Tbl_Medidas.%Efiprom`.
- `285fcb59b2cbc3c988ce`: `Planta Ppto.KPI_EFI` y `Planta Ppto.Var_GL` se redirigen a `Tbl_Medidas.KPI_EFI` y `Tbl_Medidas.Var_GL`.
- `cultures/es-ES.tmdl`: bindings generados para `Efic`, `%Efiprom`, `KPI_EFI`, `Var_GL` y `Prom_Colaboradores` se redirigen a `Tbl_Medidas`.
- Regresion minima de `Ausentismos`: `eb0f97a29923076c72ba` se corrige de `PLANTA DE PERSONAL.Prom_Colaboradores` a `Tbl_Medidas.Prom_Colaboradores`.

Validacion estatica:

- Productividad no conserva referencias `SourceRef/Property` rotas.
- SST no conserva referencias `SourceRef/Property` rotas en su pagina.
- Ausentismos no conserva referencias `SourceRef/Property` rotas en su pagina.
- Retiros conserva `Tbl_Medidas[Filtro Trimestre Dinamico]` en `37ed01c30df4dafce226`; no se corrige porque no existe medida canonica exacta ni equivalencia demostrada.
- No hay nombres de medidas duplicados.
- JSON valido en los visuales modificados.

Resultado de validacion Desktop:

- Power BI Desktop abre el proceso `Proyecto7` desde `.wt\prod`.
- No se pudo obtener evidencia visual fiable del lienzo porque la captura automatizada mantuvo el foco en el Explorador de Windows.
- Quedan pendientes las pruebas funcionales de Fase 1: 2025, 2026, seleccion multiple, leyenda `Ejecucion` y decimal visible en tabla.

Estado de fase:

- Fase 1 sigue bloqueada por falta de evidencia visual y por la referencia no resuelta de Retiros sin medida canonica demostrable.
- No iniciar Fase 2 hasta cerrar esta validacion.

## Ampliacion Fase 1 - Unidades dinamicas Challenger vs. otros negocios

Objetivo de la ampliacion:

- reproducir en Productividad el criterio de unidades ya aplicado en `Gasto Laboral`;
- Challenger debe leerse con escala de millones cuando el visual sea monetario;
- otros negocios, seleccion multiple o ausencia de seleccion unica deben conservar escala automatica o el criterio equivalente ya usado en Gasto Laboral.

Fuente de verdad revisada:

- `PBIP/Proyecto.Report/definition/pages/2ee3ca8f42b01e9a6840/visuals/2a3dbb237d2b4914b4f7/visual.json`
- `PBIP/Proyecto.Report/definition/pages/2ee3ca8f42b01e9a6840/visuals/b351f0de695056ac18a5/visual.json`
- `PBIP/Proyecto.Report/definition/pages/2ee3ca8f42b01e9a6840/visuals/ced924c91be19c603ad0/visual.json`
- medidas `GL_*` en `Tbl_Medidas.tmdl`

Resultado tecnico:

- Los graficos de Productividad `d6010674e3a075647581` y `76fbb82301d3f6b571c3` no se duplican ni se modifican para unidades monetarias, porque sus series son porcentuales (`Efic` y `%Efiprom`).
- La tabla `cba349945ec4b0577321` se alinea con la tabla de Gasto Laboral:
  - `Gasto Personal`: `labelDisplayUnits = 1D`, `labelPrecision = 1L`.
  - `Ingreso Operacional`: `labelDisplayUnits = 1D`, `labelPrecision = 1L`.
  - `Productividad`: se mantiene como porcentaje con `labelPrecision = 1L`.
- No se crean medidas auxiliares nuevas.
- No se cambia `compatibilityLevel`.
- No se usa `FORMAT()`.
- No se modifican relaciones, Power Query, bookmarks, navegacion ni otras paginas.

Validacion:

- JSON valido en los tres visuales de Productividad revisados.
- Cero nombres de medidas duplicados.
- Sin mojibake real en los archivos revisados.
- `git diff --check` sin errores, solo advertencias LF -> CRLF.
- Power BI Desktop abre `Proyecto7` desde `.wt\prod` con ruta absoluta.

Pendiente:

- Validacion visual manual posterior al ajuste de unidades para Challenger, Grupo Sky, Habitel Hotels, Fundacion Challenger, Lemco, seleccion multiple y sin seleccion.
- La incidencia separada `Tbl_Medidas[Filtro Trimestre Dinamico]` en Retiros sigue fuera del alcance de esta ampliacion.

Correccion final de la ampliacion:

- Se descarta como evidencia suficiente la configuracion fija `labelDisplayUnits = 1D`, porque no alterna por segmentador entre Challenger y los demas contextos.
- Se replica el patron funcional de `Gasto Laboral` mediante medidas numericas auxiliares y visuales superpuestos:
  - `cba349945ec4b0577321`: tabla para otros negocios, seleccion multiple o sin seleccion unica, con `labelDisplayUnits = 1D` como unidad automatica y una cifra decimal.
  - `f0d2c4b6a8e14c5397bd`: tabla Challenger, con `labelDisplayUnits = 1000000D` y una cifra decimal.
- Medidas agregadas en `Tbl_Medidas.tmdl`: `Prod_Gasto_Personal`, `Prod_Ingreso_Operacional`, `Prod_Es_Challenger`, `Prod_Gasto_Personal_Challenger`, `Prod_Ingreso_Operacional_Challenger`, `Prod_Efic_Challenger`, `Prod_Gasto_Personal_Otros`, `Prod_Ingreso_Operacional_Otros` y `Prod_Efic_Otros`.
- No se usa `FORMAT()`, no se cambia `compatibilityLevel`, no se modifican relaciones ni Power Query.
- La evidencia estatica valida JSON y ausencia de medidas duplicadas; la Fase 1 solo podra cerrarse cuando Power BI Desktop confirme visualmente Challenger, Fundacion Challenger, Grupo Sky, Habitel Hotels, Lemco, seleccion multiple y sin seleccion.

Subtitulo dinamico agregado en Fase 1:

- Se confirma que el visual derecho `76fbb82301d3f6b571c3` corresponde al grafico acumulado `Gasto Laboral Vs Ventas`.
- El subtitulo literal `Comparativo Acumulado (Ene-Jul) Anual` se reemplaza por una expresion de medida.
- Medida creada: `Tbl_Medidas[Subtitulo_Productividad_Comparativo_Acumulado]`.
- Columnas usadas: `Mes[Meses]` para seleccion, `Mes[Numero]` para orden y `Mes[Mes Abrev]` para texto corto.
- La medida cubre un mes, rangos consecutivos, meses no consecutivos, mas de cuatro meses no consecutivos, todos los meses y sin filtro especifico.
- Queda pendiente validar visualmente en Power BI Desktop todos los escenarios de mes y confirmar que no hay textos superpuestos ni campos no reconocidos.

Resultado Desktop parcial:

- Apertura: `Proyecto7.pbip` abre desde `.wt/prod`.
- Productividad renderiza sin error visible de campos no reconocidos en la captura revisada.
- Subtitulo: con `Mes = 01.Enero`, el visual `76fbb82301d3f6b571c3` muestra `Comparativo Acumulado (Ene) Anual`.
- Tabla: conserva una cifra decimal, pero el contexto visible sin seleccion unica de negocio muestra valores completos y no una escala automatica legible.
- Estado: Fase 1 bloqueada para el criterio de unidades dinamicas de tabla. No iniciar Fase 2 hasta resolver o aprobar una alternativa tecnica compatible con `tableEx`.

Actualizacion de cierre tecnico de Fase 1:

- Se corrigio el formato porcentual de los graficos `d6010674e3a075647581` y `76fbb82301d3f6b571c3`; las etiquetas de `Efic` y `%Efiprom` quedan como porcentaje con una cifra decimal y sin sufijos `bill.`, `mill.` o `mil`.
- Se corrigio la geometria de las tablas superpuestas `cba349945ec4b0577321` y `f0d2c4b6a8e14c5397bd`: ancho final `570`, alto `336,6256655039471`, `x = 389,4988066825776`, `y = 468,80851845052325`. Ambas conservan superposicion exacta.
- Anchos finales de columna en ambas tablas: `Meses = 78`, `Gasto Personal = 145`, `Ingreso Operacional = 180`, `Productividad = 120`.
- Se implemento `formatStringDefinition` corregido para las medidas monetarias auxiliares de Productividad. La escala se ubica antes del decimal (`#,0,,.0`, `#,0,,,.0`, `#,0,.0`) para que Power BI divida el valor y no solo agregue el sufijo.
- `compatibilityLevel` queda en `1601`, minimo requerido para cadenas de formato dinamicas en medidas.
- No se usa `FORMAT()` y las medidas principales permanecen numericas.

Evidencia Desktop obtenida:

- `Proyecto7.pbip` abre desde `.wt/prod`.
- Productividad renderiza.
- Sin seleccion unica de negocio, `Ano = 2026` y `Mes = 01.Enero`, la tabla muestra `$ 8,7 bill.` y `$ 76,5 bill.`, con una cifra decimal.
- Con `Empresa = Fundacion Challenger`, la tabla muestra `$ 28,0` y `$ 135,0`, con una cifra decimal.
- El subtitulo del grafico acumulado para `Mes = 01.Enero` muestra `Comparativo Acumulado (Ene) Anual`.

Pendiente para aprobar Fase 1:

- Validacion visual manual de Challenger exclusivo en millones.
- Validacion visual de Grupo Sky, Habitel Hotels, Lemco, seleccion multiple y sin seleccion especifica despues de la correccion final.
- Mientras estas evidencias no esten completas, no iniciar Fase 2.

Actualizacion de regla definitiva:

- Se ajusto la bandera de activacion de tablas a `Prod_Usar_Millones`.
- Regla aplicada:
  - `Challenger` unico -> millones.
  - todos los grupos visibles -> millones.
  - sin filtro de negocio -> millones.
  - cualquier subconjunto distinto de todos -> automatico.
- Las medidas `Prod_Gasto_Personal_Challenger`, `Prod_Ingreso_Operacional_Challenger` y `Prod_Efic_Challenger` usan `[Prod_Usar_Millones]`.
- Las medidas `Prod_Gasto_Personal_Otros`, `Prod_Ingreso_Operacional_Otros` y `Prod_Efic_Otros` usan `NOT [Prod_Usar_Millones]`.

Evidencia nueva:

- Con segmentador de negocio limpio, `Ano = 2026` y `Mes = 01.Enero`, la tabla muestra valores en millones (`$ 8.687,1 mill.` y `$ 76.517,6 mill.`).
- Las imagenes aportadas por el usuario validan Challenger en millones y Habitel Hotels / Grupo Sky en unidades automaticas.

Pendiente:

- Fundacion Challenger, Lemco, seleccion multiple parcial y empresa individual aun requieren validacion visual final antes de aprobar la Fase 1.

Consistencia transversal con Gasto Laboral:

- Se actualiza `Gasto Laboral` para usar la misma regla de unidades definida para Productividad:
  - `Challenger` unico -> millones.
  - todos los negocios o segmentador limpio -> millones.
  - cualquier subconjunto parcial -> automatico.
- Se reemplaza la bandera `GL_Es_Challenger` por `GL_Usar_Millones`.
- Los graficos superpuestos de Gasto Laboral conservan su arquitectura:
  - `2a3dbb237d2b4914b4f7`: variante millones.
  - `b351f0de695056ac18a5`: variante automatica.
- La tabla `ced924c91be19c603ad0` no se duplica. Se conserva una sola tabla y se agregan cadenas de formato dinamicas a `GL_Ppto_Gasto_Personal` y `GL_Gasto_Personal` para aplicar la regla final manteniendo las medidas numericas.

Evidencia nueva:

- Segmentador de negocio limpio en `Gasto Laboral`: valores en millones, sin `bill.`.
- Contexto parcial Lemco: escala automatica con una cifra decimal.

Pendiente:

- Validar manualmente todos seleccionados, Challenger individual, Grupo Sky, Habitel Hotels, Fundacion Challenger, seleccion parcial multiple y empresas individuales en Gasto Laboral antes de aprobar Fase 1.

Decision final de Fase 1:

- Se aclara el criterio definitivo: `Challenger` exclusivo usa millones; cualquier otro negocio, seleccion multiple, todos los negocios o ausencia de seleccion unica usan unidades automaticas.
- La evidencia visual recibida confirma:
  - sin seleccion unica: `$ 8,7 bill.` y `$ 76,5 bill.`;
  - `Challenger`: `$ 8.687,1 mill.` y `$ 76.517,6 mill.`;
  - `Habitel Hotels`: `$ 1,6 mil` y `$ 5,4 mil`;
  - `Grupo Sky`: `$ 1,1 mil` y `$ 6,2 mil`;
  - una cifra decimal en todos los casos.
- Validacion logica complementaria:
  - `Fundacion Challenger`, `Lemco`, dos negocios no Challenger y todos los negocios usan la tabla automatica porque `Prod_Es_Challenger` solo se activa con una unica seleccion exacta de `Empresas[Grupo Empresa] = "Challenger"`.
  - `Challenger` junto con otro negocio tambien usa la tabla automatica porque no hay `HASONEVALUE`.
  - La tabla Challenger y la tabla automatica son mutuamente excluyentes por las medidas `Prod_*_Challenger` y `Prod_*_Otros`.
- Validacion geometrica:
  - `cba349945ec4b0577321` y `f0d2c4b6a8e14c5397bd` conservan la misma posicion y tamano: `x = 389,4988066825776`, `y = 468,80851845052325`, `width = 570`, `height = 336,6256655039471`.
  - Los anchos de columna equivalentes son `78`, `145`, `180` y `120`.

Estado:

- Fase 1 aprobada: puede iniciarse la Fase 2.
- No se realizo staging, commit ni push.

Actualizacion complementaria de cierre:

- Se identifico un bloqueo visual adicional en `Gasto Laboral`: tarjeta `265624db15b1e420a0e6`, ubicada en el bloque inferior derecho.
- Referencia rota: `Planta Ppto.Cump_GL`.
- Medida canonica vigente: `Tbl_Medidas[Cump_GL]`.
- Correccion aplicada: redireccion PBIR local del visual hacia `Tbl_Medidas.Cump_GL`, incluyendo proyeccion, ordenamiento y reglas de color.
- No se modificaron medidas, relaciones, filtros, diseno ni otras paginas por esta correccion.
- Validacion estatica: JSON valido, cero nombres de medidas duplicados y una unica declaracion `Cump_GL`.
- Validacion Desktop: `Proyecto7.pbip` abre desde `.wt/prod`; en `Gasto Laboral` el bloque inferior derecho renderiza como tarjeta de cumplimiento y no como `Ver detalles / Corregir esto`.
- La Fase 1 no debe avanzar a Fase 2 hasta completar la confirmacion visual final de:
  - todos los grupos seleccionados explicitamente;
  - seleccion parcial multiple;
  - empresa individual de `Challenger`;
  - empresa individual de otro grupo.

Actualizacion por decision funcional:

- La Fase 1 queda aprobada con evidencia acumulada.
- Las pruebas de seleccion parcial multiple y empresas individuales se trasladan a Fase 6 - Regresion integral.
- No se debe repetir en Fase 2 el diagnostico de titulo, leyenda, subtitulo, unidades, geometria de tablas, medidas duplicadas ni visuales rotos.

## Evidencia ejecutada - Fase 2

Nombre operativo:

- Fase 2 - Diagnostico de propagacion de filtros por Grupo Empresa y Empresa.

Diagnostico:

- Interacciones: no se encontro configuracion `visualInteractions` ni interacciones `None` persistidas para la pagina `ReportSection65569958420c423d90b1`.
- Relaciones: existen rutas activas esperadas entre `Empresas`, `Planta Ppto`, `Años` y `Mes`; no se introducen relaciones bidireccionales.
- Claves: la evidencia visual acumulada confirma datos para `Challenger`, `Habitel Hotels`, `Grupo Sky` y `Fundacion Challenger`; no hay evidencia de ausencia general de datos por negocio.
- Medidas: `Efic`, `%Efiprom`, `Prod_Gasto_Personal`, `Prod_Ingreso_Operacional` y medidas `Prod_*` no eliminan indebidamente el contexto empresarial funcional; `REMOVEFILTERS` solo aparece en la bandera de unidades para calcular el total de grupos.
- Filtros persistidos: los slicers de negocio contienen filtros no nulos, no una seleccion fija; los visuales funcionales conservan filtros de periodo.
- Bookmarks: no se encontraron bookmarks de la pagina Productividad con referencias directas a los visuales funcionales revisados.

Causa raiz de los sintomas:

- Los sintomas originales no se atribuyen a una falla vigente de propagacion empresarial.
- La causa demostrada corresponde a escala/formato de unidades, referencias rotas por deduplicacion de medidas y lectura del consolidado dominada por `Challenger`.

Correccion:

- No se aplica correccion funcional adicional en Fase 2.
- Se conserva intacta la implementacion de Fase 1.

Validacion:

- Power BI Desktop abre `Proyecto7.pbip` desde `.wt/prod`.
- Gasto Laboral mantiene la tarjeta de cumplimiento reparada.
- La validacion automatizada por DAX contra el modelo local no fue posible porque el proveedor `MSOLAP` no esta disponible en el entorno.

Decision:

- Fase 2 completada sin cambio adicional.
- Puede iniciarse Fase 4; Fase 6 conserva las pruebas exhaustivas de empresas individuales, seleccion parcial multiple y seleccion contradictoria.

## Cierre documental Fase 2 y decision Fase 3

Clasificacion documental:

- `Specs`: conserva requisitos, decisiones tecnicas, riesgos, criterios de aceptacion y estado resumido de fases.
- `Outputs`: conserva matrices operativas, resultados de comandos, evidencias visuales e inventarios temporales.
- `Docs`: no se modifica en esta ejecucion; solo se actualizara cuando la solucion este validada integralmente e integrada.

Evidencia detallada asociada:

- `../Outputs/02_2026-07-22_evidencia_fase2_filtros_productividad.md`

### Fase 2 - Completada

Resultado:

- No se confirmo una falla vigente de propagacion de filtros por `Grupo Empresa` o `Empresas`.
- No se requirio correccion funcional adicional en PBIP, TMDL, relaciones, interacciones ni medidas.
- Las hipotesis de interaccion deshabilitada, relacion incorrecta como causa principal, eliminacion indebida de contexto, filtro persistido y ausencia general de datos fueron descartadas con la evidencia disponible.
- Las mejoras funcionales implementadas permanecen asociadas a Fase 1.

### Fase 3 - No aplica

Justificacion:

- La Fase 3 tenia como condicion de entrada una causa raiz aceptada y una solucion minima identificada para corregir el contexto de `Grupo Empresa`.
- La Fase 2 no identifico una falla vigente que requiera corregir el contexto de `Grupo Empresa`.
- No se identificaron archivos funcionales autorizados para una correccion en esta fase.
- Ejecutar cambios adicionales implicaria modificar el modelo sin evidencia.

Nueva condicion de entrada de Fase 4:

- `Fase 2 completada y Fase 3 declarada No aplica`.

## Fase 4 - Validacion del filtro Empresas

Estado:

- Fase 4 aprobada por evidencia visual aportada por el usuario.

Ejecucion realizada:

- Se abrio `PBIP/Proyecto7.pbip` desde `.wt/prod`.
- Se navego a la pagina `Productividad`.
- La pagina renderizo con el titulo dinamico, subtitulo, leyenda y tabla ya validados en Fase 1.
- El segmentador `Empresas` se encuentra como desplegable y no respondio de forma confiable a la automatizacion de clics en Desktop.

Resultado:

- La cascada `Grupo Empresa -> Empresa` quedo validada para 2026.
- `Challenger` muestra unicamente `Challenger`.
- `Fundacion Challenger` muestra unicamente `Fundacion Challenger`.
- `Grupo Sky` muestra `Sky Forwarder`, `Sky Industrial` y `Sky Logistica Integral`.
- `Habitel Hotels` muestra `Habitel Nomina Compartida`, `Habitel Prime`, `Habitel Select`, `Lemco Salvio` y `Operadora`.
- `Lemco` muestra `Lemco` y `Lemco Inmobiliaria`.
- Al limpiar `Grupo Empresa`, `Empresa` vuelve a mostrar el conjunto completo.
- Graficos, tabla y KPI cambian entre grupos sin campos no reconocidos.
- No se aplico ninguna correccion funcional en Fase 4.
- No se modificaron relaciones, medidas, visuales, bookmarks ni fuentes por Fase 4.
- La seleccion individual de empresa representativa, cambio de grupo con empresa previa y combinacion contradictoria se trasladan a Fase 6 como regresion residual obligatoria.

Decision:

- `Fase 4 aprobada`: puede iniciarse Fase 5.

## Fase 5 - Reconciliacion de visuales

Estado:

- Aprobada por matriz compacta de validacion funcional.

Objetivo:

- Confirmar que grafico mensual, grafico acumulado, tabla mensual, tabla KPI e indicador de tendencia presenten resultados coherentes bajo el mismo contexto de filtros.

Contextos minimos:

- Sin filtro de negocio.
- `Challenger`.
- `Fundacion Challenger`.
- `Grupo Sky`.
- `Habitel Hotels`.
- `Lemco`.

Criterios:

- La productividad mensual de la tabla debe coincidir con la serie de ejecucion del grafico mensual.
- El total de productividad debe coincidir con el valor de ejecucion del grafico acumulado.
- El KPI ejecutado debe coincidir con el total ejecutado.
- El KPI presupuestado debe coincidir con el total presupuestado.
- La flecha debe ser coherente con la comparacion ejecutado vs presupuestado.
- No deben aparecer ceros artificiales, campos no reconocidos ni visuales duplicados.

Evidencia detallada:

- `../Outputs/03_2026-07-22_evidencia_fase5_reconciliacion_productividad.md`

Resultado:

- Sin filtro de negocio: pasa.
- `Challenger`: pasa.
- `Fundacion Challenger`: pasa.
- `Grupo Sky`: pasa.
- `Habitel Hotels`: pasa.
- `Lemco`: pasa.

Discrepancias:

- No se reportaron discrepancias.

Correcciones:

- No se aplicaron correcciones en Fase 5.

Decision:

- `Fase 5 aprobada`: puede iniciarse Fase 6.

## Fase 6 - Regresion integral

Estado:

- `Fase 6 aprobada`.

Evidencia:

- `../Outputs/04_2026-07-22_evidencia_fase6_regresion_productividad.md`

Resultado:

- La Fase 6 fue aprobada por validacion manual del usuario.
- Se ejecutaron los escenarios residuales de periodos, meses, empresas individuales, selecciones multiples, jerarquia, combinaciones contradictorias y regresion transversal minima.
- No se reportaron fallas funcionales bloqueantes.
- No se aplicaron correcciones adicionales en PBIP/TMDL durante Fase 6.

Decision:

- `Fase 6 aprobada`: puede iniciarse Fase 7.

## Fase 7 - Aislamiento del paquete de commit

Estado:

- `Fase 7 bloqueada` hasta aislar por hunks los archivos mixtos.

Resultado preliminar:

- La Fase 6 esta aprobada y no requiere mas pruebas funcionales antes de preparar el paquete.
- El working tree conserva 74 archivos pendientes, con staging vacio.
- `compatibilityLevel 1601` es esperado y debe conservarse.
- El visual `f0d2c4b6a8e14c5397bd` es intencional y pertenece a Productividad.
- `Outputs` permanece excluido de Git.
- La rama esta detras de `origin/main` por commits conocidos; esto se registra y se difiere a Fase 9, no bloquea por si solo la preparacion del commit de la rama.

Bloqueos para aprobacion de Fase 7:

- `Tbl_Medidas.tmdl` y `cultures/es-ES.tmdl` contienen hunks funcionales aprobados mezclados con drift de Power BI Desktop y cambios de codificacion no relacionados.
- Algunos visuales de Gasto Laboral y Ausentismos contienen reparaciones tecnicas legitimas mezcladas con cambios de esquema, z-order o filtros persistidos.
- El manifiesto operativo del paquete debe completarse antes de autorizar staging.

Evidencia:

- `../Outputs/05_2026-07-22_manifest_paquete_commit_productividad.md`
