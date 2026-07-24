# Plan de implementacion - correccion de Productividad por periodo y contexto de negocio

Fecha: 2026-07-21

Estado: CERRADO el 2026-07-24. Productividad y Gasto Laboral corresponden a la version final validada y aprobada por el usuario. Los defectos registrados el 2026-07-23 fueron corregidos y el paquete tecnico final quedo versionado en `f2aa4d59836b73f5162139cdaa03f51c0da2c766`.

Spec de origen: `Specs/0004_analisis_impacto_correccion_productividad_filtros_negocio.md`

Nota sobre trazabilidad: los archivos `Specs/0004_analisis_impacto_correccion_productividad_filtros_negocio.md` y `Specs/0005_plan_implementacion_correccion_productividad_contexto_negocio.md` referenciados arriba y en las fases siguientes no existen en el repositorio principal con esos numeros (los numeros 0004 y 0005 ya estaban asignados a un requerimiento distinto). Este documento (0008) es el unico Spec vigente para el requerimiento de Productividad/Gasto Laboral y concentra el cierre. Las fases 0-8 descritas abajo, basadas en el worktree `.wt\prod` y la rama `fix/productividad-contexto-negocio`, fueron reemplazadas por una estrategia distinta autorizada por el usuario: construir el candidato por copia directa del PBIP productivo real (no desde `origin/main` ni desde un worktree Git), debido a que el repositorio principal diverge ampliamente de la produccion real. Las fases no se ejecutaron tal como estan escritas; ver "Cierre del requerimiento" a continuacion para el resultado real.

## Cierre definitivo (2026-07-24)

### Decision

Plan cerrado. El usuario confirmo que las paginas `Productividad` y `Gasto Laboral` representan la version final funcionalmente validada y aprobada.

### Commits asociados en `main`

- `a1dbb62`: excluye valores en blanco del segmentador de meses de Productividad.
- `eaefa0e`: muestra valores completos por negocio en la tabla de Productividad.
- `0d524bd`: ajusta el formato monetario por negocio en Gasto Laboral.
- `f2aa4d59836b73f5162139cdaa03f51c0da2c766`: consolida el estado PBIR final de ambas paginas, incorpora el titulo y subtitulo dinamicos y corrige la incompatibilidad entre `FormatString` y `FormatStringDefinition`.

El commit `16161c6` fue revisado como antecedente en otra referencia Git, pero no se considero un cierre publicado en `main`: contenia una implementacion anterior y un alcance distinto. El commit final se construyo a partir del estado aprobado y del diff real frente a `origin/main`, no solo de los mensajes del historial.

### Estado final implementado

- Productividad (`ReportSection65569958420c423d90b1`): 12 visuales visibles versionados con el estado final aprobado.
- Gasto Laboral (`2ee3ca8f42b01e9a6840`): 9 visuales versionados con el estado final aprobado.
- `Titulo_Productividad_Gasto_Laboral`: titulo del grafico mensual dependiente del contexto de ano.
- `Subtitulo_Productividad_Comparativo_Acumulado`: texto anual o por meses seleccionados, con orden por `Mes[Numero]`, exclusion de blancos y tratamiento separado de rangos continuos y selecciones no consecutivas.
- `GL_Ppto_Gasto_Personal` y `GL_Gasto_Personal`: conservan sus sumas DAX y su formato dinamico; se retiro el formato estatico duplicado que impedia abrir el PBIP.
- Challenger, consolidado o todos los grupos: millones con una cifra decimal.
- Otros negocios: unidades automaticas en graficos y valores completos en tablas, sin modificar calculos ni logica de negocio.

### Validaciones de cierre

- Apertura correcta de `PBIP/Proyecto7.pbip` en Power BI Desktop despues de corregir el conflicto TMDL.
- Validacion funcional de Productividad y Gasto Laboral confirmada por el usuario.
- 21 archivos `visual.json` parseados correctamente y sin BOM UTF-8.
- Referencias exactas de los visuales `76fbb82301d3f6b571c3` y `d6010674e3a075647581` a las medidas dinamicas.
- Auditoria semantica: 0 alertas altas; las alertas medias y bajas son preexistentes y generales del modelo.
- Auditoria de navegacion: 0 alertas criticas.
- Auditoria DAX: la alerta alta por divisiones con `/` corresponde a medidas historicas fuera del cambio; ninguna medida incorporada por este cierre usa ese patron.
- `git diff --cached --check` y `git show --check` sin errores.
- Revision de historial y comparacion con `origin/main` para evitar duplicidad.

### Archivos y cambios excluidos

- Visual oculto y no versionado `f0d2c4b6a8e14c5397bd`, asociado a una variante anterior ya reemplazada por las medidas de tabla dinamicas.
- Medidas auxiliares legado `Prod_*_Challenger` y `Prod_*_Otros`, utilizadas unicamente por ese visual oculto.
- Bookmarks, paginas distintas, cultures, fuentes, Data, Outputs, herramientas y demas cambios locales ajenos.

### Observaciones residuales

- El working tree conserva cambios locales ajenos y el visual oculto legado; no forman parte de la version visible aprobada ni del paquete de cierre.
- La alerta baja por ausencia de `displayFolder` en `Subtitulo_Productividad_Comparativo_Acumulado` es organizativa y no funcional.
- Los errores conocidos de Formula Firewall o refresh pertenecen al proceso de fuentes y permanecen fuera de este plan.
- No quedan cambios aprobados de los visuales visibles de Productividad o Gasto Laboral pendientes de commit.

## Registro historico del intento de cierre (2026-07-23; reemplazado)

> Las secciones desde este punto documentan el proceso anterior y se conservan por trazabilidad. Sus estados, pendientes, rutas de worktree e instrucciones operativas no representan el estado vigente. El cierre definitivo y canónico es el registrado al inicio de este documento.

### Candidato aprobado

- Construido por copia directa del PBIP productivo (`PBIP/Proyecto7.pbip`), no de `origin/main`.
- Validado estaticamente y luego visualmente por el usuario en Power BI Desktop, sobre el candidato y despues sobre el archivo oficial.

### Respaldo utilizado

`C:\Users\edwin.clavijo\Documents\Backups\Proyecto7_antes_aplicar_productividad_gasto_20260723_160541\PBIP` (tomado antes de aplicar el diferencial al archivo oficial).

### Aplicacion al PBIP oficial

Aplicado a `PBIP\Proyecto7.pbip` (archivo oficial) mediante edicion quirurgica de hunks, preservando el resto del working tree (cambios ajenos preexistentes no se tocaron).

### Cinco cambios funcionales finales

1. `Tbl_Medidas.tmdl`: medida `GL_Usar_Millones` (reemplaza `GL_Es_Challenger`) y redireccion de `GL_Ppto_Visual_Challenger`, `GL_Real_Visual_Challenger`, `GL_Ppto_Visual_Otros`, `GL_Real_Visual_Otros`; mas 10 medidas nuevas de Productividad (`Titulo_Productividad_Gasto_Laboral`, `Prod_Gasto_Personal`, `Prod_Ingreso_Operacional`, `Prod_Usar_Millones`, `Prod_Gasto_Personal_Challenger`, `Prod_Ingreso_Operacional_Challenger`, `Prod_Efic_Challenger`, `Prod_Gasto_Personal_Otros`, `Prod_Ingreso_Operacional_Otros`, `Prod_Efic_Otros`).
2. Visual `d6010674e3a075647581` (Productividad): titulo dinamico ligado a `Titulo_Productividad_Gasto_Laboral`.
3. Visual `76fbb82301d3f6b571c3` (Productividad): migracion de `Efic`/`%Efiprom` a `Tbl_Medidas`, `labelDisplayUnits` a una cifra decimal.
4. Visual `cba349945ec4b0577321` (Productividad): variante "otros negocios" (escala automatica, una cifra decimal).
5. Visual nuevo `f0d2c4b6a8e14c5397bd` (Productividad): variante "Challenger/consolidado" superpuesta a la anterior (millones, una cifra decimal).

### Regla definitiva de unidades (Productividad y Gasto Laboral)

1. Challenger como seleccion exclusiva: millones, una cifra decimal.
2. Todos los negocios seleccionados explicitamente: millones, una cifra decimal.
3. Filtros Grupo Empresa y Empresa completamente limpios (consolidado): millones, una cifra decimal.
4. Cualquier otro negocio/empresa/subconjunto parcial: escala automatica en graficos; tablas y matrices sin abreviacion; una cifra decimal.

### Resultado de validacion

- Productividad: validacion visual exitosa sobre el archivo oficial, confirmada por el usuario.
- Gasto Laboral: validacion visual exitosa sobre el archivo oficial, confirmada por el usuario.
- Paginas fuera de alcance: preservadas sin cambios funcionales (confirmado por diff contra respaldo).

### Hallazgo diferido (fuera de este cierre)

Discrepancia `Cump_GL`: la tarjeta `265624db15b1e420a0e6` muestra 41,2 % y la tabla `ced924c91be19c603ad0` muestra 70,8 %, por un filtro Enero-Julio persistido en la tabla y ausente en la tarjeta. No se modifica hasta confirmar con negocio la intencion del filtro. Detalle en `Outputs/49_2026-07-23_validacion_funcional_productividad_gasto_laboral.md`.

### Pendiente historico (resuelto el 2026-07-24)

La preparacion y autorizacion de staging/commit que estaban pendientes se resolvieron con el commit tecnico `f2aa4d59836b73f5162139cdaa03f51c0da2c766` y el commit documental de cierre que versiona este plan.

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

Validaciones: staging exacto, identidad correcta, rama correcta, sin remotos pendientes.

Pruebas funcionales: evidencia ya aprobada.

Evidencia esperada: hash y push exitoso.

Criterio de aceptacion: origin actualizado solo con el commit aprobado.

Condicion para detenerse: commits remotos pendientes, staging inesperado o identidad incorrecta.

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

## Condicion de cierre del requerimiento

El requerimiento se cierra solo cuando:

- Fase 6 queda validada visualmente;
- Fase 7 presenta paquete de commit limpio;
- Fase 8 se ejecuta con aprobacion explicita;
- el push queda confirmado;
- el repositorio principal conserva `.wt/**` ignorado localmente y sin versionarse.
