# Registro de Cambios

Este archivo registra los cambios significativos del proyecto ordenados cronologicamente (mas reciente primero).

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

---

## [Sin version] - 2026-10-06 (3)

### Corregido

- Hotfix de `PBIP-010`: la pagina `Retiros y Rotacion Predictiva`
  (`b7f3a91c2d4e60582a1f`) ahora se oculta realmente en modo lectura mediante
  `"visibility": "HiddenInViewMode"` en su `page.json`.
- El `showPage: false` que PBIP-010 dejo en el navegador de
  `Sociodemografico por Empresa` solo ocultaba la pagina del **navegador
  personalizado**: la pestana real seguia visible en Power BI Desktop. Ambos
  mecanismos se conservan, porque cubren cosas distintas.
- Se replico el patron ya usado en el reporte: la pagina `Demografico`
  (`f0fd1eb45022c4c0718e`) declara esa misma propiedad.
- Cambio minimo: 1 archivo, 1 propiedad agregada. Sin tocar visuales, medidas,
  DAX, Power Query, modelo, relaciones, slicers, colores, tipografias, otras
  paginas ni `Data/`.
---

## [Sin version] - 2026-10-06 (2)

### Cambiado

- `PBIP-010`: calibracion visual de la pagina `Sociodemografico por Empresa`
  para lectura en televisores y pantallas grandes. **PASS visual del usuario**
  sobre la pagina proyectada. No invalida el cierre de `PBIP-006`, cuyo PASS
  evaluaba uso en monitor.
- **Tipografia**: `Outfit` -> `Calibri` en las 49 declaraciones de la pagina.
  Era la unica pagina del reporte con `Outfit` (13 de 17 usan `Calibri`) y esa
  fuente no esta instalada, por lo que el motor la sustituia en render.
- **Paleta**: salen de uso `#0B1C35` y `#1A3059`. Sus pares de contraste iban de
  1,04:1 a 1,42:1 frente al minimo de 3:1 para marcas graficas. Se conservan los
  aprobados `#000032`, `#1B487F`, `#4A7FC0` y `#7EB3E8`; `#F7931E` sigue como
  acento, una categoria por grafico. `Antiguedad por Empresa` suma dos tonos
  derivados, `#2E8C9A` y `#B9C4CF`, por tener 7 categorias.
- **Color de etiqueta por categoria**: 19 entradas nuevas con color explicito
  segun el fondo de su barra. El contraste pasa de 1,30:1 en el peor caso a
  **4,86:1**, cumpliendo AA.
- **Tamanos por rol**: titulo de pagina 20 -> 28 pt, titulos de visual 14 -> 17 pt,
  ejes y leyendas 8-11 -> 12 pt, matriz 10/13 -> 13/15 pt, slicers 10-12/12 ->
  13/14 pt, navegacion 12/16 -> 14/18 pt.
- **Lienzo**: la banda de encabezado pasa de 2299,5 a 2100 px, el ancho util.

### Preservado

- El slicer de Mes conserva **`09.Septiembre`**, el ultimo periodo vigente
  verificado contra la fuente del modelo (2.605 registros). No se revirtio a
  `07.Julio`.
- El navegador conserva `showPage: false` para `Retiros y Rotacion Predictiva`:
  es una decision funcional del responsable, no ruido de serializacion.

### No modificado

- **0 cambios** en consultas, campos, filtros, interacciones, modelo semantico,
  Power Query, DAX, relaciones, tema global y otras paginas. `Data/` y
  `Outputs/` quedan fuera del commit.
---

## [Sin version] - 2026-10-06

### Agregado

- Cierre documental de INGRESOS y RETIROS de septiembre de 2026:
  `Specs/0034_cierre_ingresos_retiros_septiembre_2026.md`.
- `Docs/RUNBOOK.md` incorpora la seccion 12, **Procedimiento mensual de
  actualizacion de PptovsReal (INGRESOS/RETIROS)**, con sus controles.

### Estado del cierre

- `INGRESOS`: agosto 2026 **147/147** y septiembre 2026 **127/127** contra
  Kactus; se incorporaron 128 registros (1 ingreso tardio de agosto y 127 de
  septiembre). `Tabla6` queda en 5.549 filas y 27 columnas.
- `RETIROS`: agosto 2026 **113/113** y septiembre 2026 **102/102**; se
  incorporaron los 102 de septiembre y agosto no se modifico.
- Conciliacion por clave de evento en las cuatro combinaciones: **0 faltantes,
  0 adicionales, 0 duplicados**.
- Homologacion de empresa resuelta al 100% con la jerarquia vigente y tres
  reglas especiales aprobadas (`LEMCO SALVIO`, `HABITEL SELECT`,
  `HABITEL PRIME`). `Dependencia`/`Area` y `Nivel` resueltos 102/102 en los
  retiros de septiembre.
- `EDAD` y `Grupo_Edad` de `RETIROS` corrigen su fecha de corte heredada:
  agosto al 31/08/2026 (94 filas) y septiembre al 30/09/2026 (102 filas).
  Ninguna fila de esos periodos conserva `DATE(2026,7,31)`.
- Power BI: refresh y publicacion realizados y validados por el usuario en
  Proyecto 04 y Proyecto 07. **No se modifico `PBIP/`**.

### Cambiado

- `Docs/ACTUALIZACION_INGRESOS_RETIROS_PPTOVSREAL.md` registra que la referencia
  operativa es **`Fact_Contrataciones`** y que las hojas mensuales del
  consolidador son exportaciones manuales, no fuente canonica. El caso de agosto
  lo demuestra: `Ago II` (94) era una extraccion incompleta y la poblacion real
  de retiros de agosto es 113.
- `Docs/PROJECT_STATUS.md` refleja el estado cerrado de ambas hojas.
- `Specs/00_roadmap_y_backlog.md` registra el cierre operativo y abre `DATA-016`.

### Aprendizaje operativo

- Se comprobo que **AutoSave de OneDrive puede persistir cambios aunque Excel se
  cierre con `SaveChanges=False`**. Dos intentos abortados por errores de tipo de
  dato dejaron filas parciales en el archivo vivo; ambos se detectaron por
  SHA-256 y se restauraron desde respaldos verificados, sin perdida de datos.
- Procedimiento seguro adoptado: respaldo con SHA-256, construccion y validacion
  de los datos **antes** de abrir Excel, trabajo sobre una **copia fuera de
  OneDrive**, escritura con Excel COM, validacion completa de la copia y
  promocion al archivo oficial solo tras el PASS.

### Pendientes no bloqueantes

- 10 fechas de nacimiento de los retiros de septiembre quedan en `#N/A` y las
  completara el usuario cuando Kactus vuelva a estar disponible. No se invento
  ninguna fecha ni se consulto otra fuente.
- `DATA-016`: modernizar `Scripts/headcount/validar_ingresos_retiros.py` para
  derivar ambas poblaciones de `Fact_Contrataciones` y conciliar por clave de
  evento. Hasta entonces no es autoridad unica para un cierre.
- 19 filas manuales de agosto siguen sin formula de `EDAD`/`Grupo_Edad` ni fecha
  de nacimiento; no se retrocorrigieron.

### No modificado

- **No se modifico `PBIP/`**, ni Power Query, ni DAX, ni el modelo, ni scripts,
  ni pruebas, ni `Outputs/`. `Data/` permanece ignorado por Git, igual que los
  respaldos y los temporales del cierre.
---

## [Sin version] - 2026-10-05

### Agregado

- Cierre documental de la actualizacion de HeadCount de septiembre de 2026:
  `Specs/0033_cierre_actualizacion_headcount_septiembre_2026.md` registra alcance,
  fuentes, reglas derivadas, homologaciones, validaciones, privacidad y pendientes.
- `Docs/RUNBOOK.md` incorpora la seccion 11, **Procedimiento mensual de actualizacion
  de HeadCount**: 26 pasos reutilizables para cualquier mes, con sus controles de
  privacidad, uso de Excel COM y manejo de dinamicas.

### Estado del corte

- `Consolidado2025`, bloque `09.Septiembre` de 2026: **2.605 colaboradores**
  (CHALLENGER 1.924, HABITEL HOTELS 326, GRUPO SKY 254, LEMCO 97, FUNDACION
  CHALLENGER 4).
- Cuatro archivos mensuales `Sin Salario` generados en
  `Data/HeadCount/2026/09_Septiembre/`: 2.605 / 2.025 / 254 / 326. Los tres archivos
  por unidad forman una particion exacta del archivo completo
  (`2.025 + 254 + 326 = 2.605`), con 0 intersecciones, 0 faltantes y 0 adicionales.
- Homologacion de empresa aplicada sobre `GRUPO EMPRESA` y `Nombre Empresa` con el
  catalogo aprobado; 4 cargos nuevos incorporados a la homologacion de
  `NIVEL_DE_CARGO`/`TIPO_DE_CARGO`; `DEPENDENCIA`/`AREA` resueltas por combinacion
  historica exacta de `CARGO_CCO` (2.584 automaticas, 21 registros de 18
  combinaciones nuevas revisadas manualmente).
- Fuentes Kactus complementarias utilizadas con reglas ya validadas: Contratos
  (datos contractuales, `SEGMENTO`, jefe, con prioridad `A` y fallback `I`), Maestro
  de Empleados (fecha de nacimiento, estado civil, `Tipo Identificacion`), Datos
  Familiares (`HIJOS`) y Cuentas de Empleados (`AFC`, `AFP`, `CCF`, `EPS`).
- `Correo Corporativo` actualizado desde la fuente Office 365 del mes: 825 registros
  con correo real, 1.780 en `N/R`, 0 vacios. El campo se elimina en Power Query, de
  modo que su actualizacion no altera el reporte publicado.
- `CM` y `PCD` cerrados de forma **provisional** heredando agosto por identificacion
  exacta: 79 y 28 registros con valor, 109 ingresos sin antecedente quedaron vacios.
  No se infirio ninguna condicion medica ni de discapacidad.
- Auditoria de `Informe` y `Tbls_Hijos` en los cuatro archivos: **PASS**, con cada
  indicador recalculado de forma independiente contra la hoja `Data` y 0 diferencias.
- Power BI fue actualizado y publicado con este corte: septiembre = 2.605,
  distribucion por `GRUPO EMPRESA` coincidente, visuales sin errores y fecha de
  actualizacion visible 05/10/2026. `Correo Corporativo` y `PCD` no entran al modelo;
  `CM` si existe, pero el cruce provisional de `CM`/`PCD` se ejecuto **despues** de
  la publicacion y aun no esta publicado.

### Cambiado

- `Docs/PROJECT_STATUS.md` deja de declarar que las reglas funcionales de las fuentes
  Kactus complementarias para HeadCount estan sin definir: quedaron definidas y
  validadas operativamente, el proceso sigue manual y asistido y la automatizacion
  integral continua pendiente.
- `Specs/00_roadmap_y_backlog.md`: `DATA-015` pasa a **finalizada** con fecha
  2026-10-05 y se agrega la entrada de bitacora del cierre mensual.

### Pendientes no bloqueantes

- 15 registros conservan `Nombre Empresa = 100` hasta recibir la fuente oficial de
  clasificacion hotelera; su `GRUPO EMPRESA` si quedo homologado.
- Publicar en Power BI el cruce provisional de `CM`/`PCD` cuando llegue su fuente
  oficial.
- Deuda heredada de plantilla en los HC mensuales: `Antiguedad`, `EDAD` y la fecha
  visual usan `TODAY()`, el grafico de rango de edad omite `Menores De 18 Anos` y el
  titulo del `Informe` es generico. No se corrigieron en este cierre.
- INGRESOS y RETIROS de septiembre en `PptovsReal.xlsx` continuan como frente
  separado; **no** forman parte de este cierre.

### No modificado

- **No se modifico `PBIP/`**, ni el modelo semantico, ni scripts, ni pruebas, ni
  `Outputs/`. `Data/` permanece ignorado por Git, igual que los respaldos temporales
  del corte.
---

## [Sin version] - 2026-10-04

### Agregado

- Gobierno documental de tres familias Kactus complementarias:
  `Maestro_Empleados_Kactus`, `Datos_Familiares_Kactus` y `Cuentas_Empleados_Kactus`,
  organizadas bajo el patron `Fuente_Oficial/`, `Historico/` e `Insumos_Vigentes/`.

### Cambiado

- Los tres consolidadores oficiales dejaron de depender del OneDrive personal y
  pasaron a consumir el sitio corporativo `TalentoHumanoGrupoLemco` mediante
  `Web.Contents`. Consultas migradas: 9 de 9 en Maestro de Empleados, 9 de 9 en
  Datos Familiares y 8 de 8 en Cuentas de Empleados. La unica diferencia funcional
  en el codigo M fue la expresion de origen.
- `Docs/DATA_PIPELINE.md`, `Docs/ESTRUCTURA_PROYECTO.md`, `Docs/RUNBOOK.md`,
  `Docs/SECURITY_AND_PRIVACY.md` y `Docs/PROJECT_STATUS.md` incorporan estas
  familias. El procedimiento mensual del runbook pasa a cubrir cuatro familias.

### Estado validado y pendientes

- `RefreshAll` y QA posteriores finalizaron correctamente en los tres libros, con
  conteos agregados coincidentes entre cada consulta fuente y su archivo vigente.
- `Dim_Hijos_Empleados` de Datos Familiares fue validada de forma independiente
  reproduciendo su logica fuera de Excel: resultado identico al del libro.
- Se registro un aprendizaje operativo: no invocar `PivotTable.RefreshTable()` de
  forma explicita cuando `RefreshAll` ya actualizo las dinamicas del modelo.
- **No se modifico `PBIP/`**, ni Power Query del modelo, ni `Data/`, ni `Outputs/`.
- Queda pendiente definir las reglas de negocio para usar estas fuentes en la
  actualizacion mensual de HeadCount.

---

## [Sin version] - 2026-09-23

### Cambiado

- Pagina `Retiros`: agregadas como exclusiones de pagina las causales
  `SUSTITUCION PATRONAL` y `CESACION EFECTOS REINTEGRO`, conservando las
  exclusiones anteriores. La depuracion sigue dependiendo de filtros de pagina;
  no se centralizo en DAX.
- Modelo `Ppto Retiros`: incorporada la columna auxiliar `Retiro valido` desde
  `PptovsReal.xlsx`. Se conserva temporalmente como texto y todavia no gobierna
  las medidas.

### Estado validado y pendientes

- `Tbl_Medidas[Tot_Retiros]` permanece sin cambios como
  `COUNT('Ppto Retiros'[Mes])` y, sin filtros adicionales, cuenta registros
  brutos.
- Challenger enero-agosto de 2026 permanece en 470 retiros elegibles. El control
  futuro esperado es 472; dos eventos con motivo operativo desactualizado
  explican la diferencia, pero sus correcciones no forman parte de este cierre.
- Quedan pendientes dos correcciones de fecha, sin impacto en el total elegible;
  la carga parcial de septiembre; la
  actualizacion de `INGRESOS`; y la alineacion de la pagina `Rotacion` con las
  dos exclusiones nuevas.
- Fuera de alcance: cambiar `Tot_Retiros`, tipar `Retiro valido` como entero,
  modificar Power Query o convertir la columna auxiliar en regla canonica.

Los archivos operativos bajo `Data/**` no se versionan.

## [Sin version] - 2026-09-01

### Actualizado

- Actualizado localmente `Data/HeadCount/PptovsReal.xlsx`, hoja `Planta
  Personal`, con el corte julio de 2026 proveniente de `Data/Gasto
  Laboral/2026/07_Julio/Gasto Laboral 2026.xlsx`: 21 celdas en 8 filas, sin
  agregar ni eliminar registros. Se conciliaron `Gasto Personal`, `Ventas
  (MM)` y `Ppto Ventas (MM)`; `Ppto Gasto Personal` permaneció intacto.
- QA PASS: 22 valores fuente no nulos coinciden después de la actualización,
  se preservaron los 3 nulos de Challenger, 0 diferencias lógicas en hojas no
  objetivo y sin cambios en fórmulas, conexiones ni pivots.

### Agregado

- `Docs/ACTUALIZACION_PLANTA_PERSONAL_PPTOVSREAL.md`: runbook reproducible,
  matriz de mapeo, procedimiento manual, controles y rollback.
- `Scripts/actualizar_planta_personal.ps1`: herramienta parametrizada con
  `-DryRun`, validación de esquema/llave y escritura sobre copia de salida.

Los Excel, backups y evidencia operativa permanecen excluidos de Git. Sin
cambios en PBIP, Power Query, DAX, modelo semántico ni visuales.

## [Sin version] - 2026-08-31

### Documentado

- `PBIP-007`: Gate A funcional validado manualmente en Power BI Desktop sobre
  31 visuales / 6 páginas (render y cifras correctos, sin error de campos ni
  regresiones relacionadas). Bloque B aplicado en 2 visuales sustituyendo la
  medida inexistente `Filtro Trimestre Dinamico` por `Filtro Trimestre Slicer`;
  Gate B estático PASS sobre 16 páginas / 295 visuales, con 0 referencias rotas,
  0 bindings incorrectos, 0 JSON inválidos, 0 cambios en SemanticModel y
  `git diff --check` limpio. Bloque C no ejecutado: 10 visuales conservan deuda
  cosmética `scopeId` no bloqueante porque el Gate A confirmó colores y formato.
  Gate B funcional validado manualmente con PASS: en `Product.
  (Colaboradores)` el visual `8257c3fc27f928312499` es el slicer de
  `Mes[Meses]` y usa la medida solo como filtro interno, sin requerir un slicer
  visible de Trimestre; en `Retiros` pasaron trimestre actual, trimestre
  anterior y sin selección. El worktree previo con 93 cambios tracked
  permaneció aislado y sin staging. La corrección independiente de
  `AUSENTISMOS[Tasa Ausentismo]` se excluyó íntegramente del alcance y del diff
  neto de PBIP-007.

## [Sin version] - 2026-08-14

### Agregado

- Nuevo slicer de `Mes[Meses]` en la página `Gasto Laboral` (visual `6996b7b903807dc80edb`, modo Dropdown, alto `76px`): permite filtrar la página por mes. El slicer queda restringido al corte de datos actualmente habilitado y validado — `01.Enero` a `06.Junio` — mediante un prefiltro explícito (`In {01.Enero..06.Junio}`); no lista `Julio`–`Diciembre` ni `(En blanco)`. Este rango deberá ampliarse manualmente cuando se actualice y valide `PptovsReal.xlsx`, hoja `Planta Personal`, con los meses siguientes. No es una lista dinámica: no se basa en la fecha actual ni infiere automáticamente el último mes cerrado. Filtro adicional conservado: exclusión de `Meses = null` (`Filter0519748e1e5b43367ce239`, identificador único, sin colisión con otros filtros del reporte).

### Cambiado

- Slicer `Empresas` (visual `bb8fdf3117578ada1101`) de la página `Gasto Laboral`: modo cambiado de `Basic` a `Dropdown` y redimensionado (alto `398.75→76px`) para hacer espacio al nuevo slicer de Mes.
- Reposicionado el visual contiguo `60ceb14b900b312c82be` (sin cambios de campos/medidas) como consecuencia del reacomodo de layout anterior.

### Corregido

- Retirada del nuevo slicer de Mes una referencia inerte a la medida `Tbl_Medidas[Filtro Trimestre Dinamico]` (no existe como medida vigente en el modelo — la medida real es `Filtro Trimestre Slicer`). La referencia no tenía cláusula de filtro activa ni participaba en `query`/`projections`/`objects`; su eliminación no altera el comportamiento del slicer. No se creó la medida `Filtro Trimestre Dinamico` ni se sustituyó por `Filtro Trimestre Slicer`.

Sin cambios en modelo semántico, DAX, Power Query, bookmarks ni otras páginas.

## [Sin version] - 2026-08-11 (DATA-012)

### Cambiado

- Migradas las 3 consultas que leen HeadCount (`Consolidado2025`, `PLANTA DE PERSONAL`, `AREAS`) de OneDrive personal a la biblioteca corporativa SharePoint (`lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/...`), resolviendo el error `NIVEL_DE_CARGO` reportado por el usuario (causa: la fuente antigua estaba desincronizada frente a la reestructuración manual del Excel).
- Corregida la falsa equivalencia `RANGO DE EDAD → GENERACIÓN` únicamente para la fuente 2025: ahora `GENERACIÓN` se alimenta de la columna real `Generación` del Excel, y `RANGO DE EDAD` queda como atributo `Rango de Edad` independiente en `Consolidado2025` y `PLANTA DE PERSONAL`. La lógica histórica 2024 (`RANGO DE EDAD → GENERACIÓN` como sustituto) se conserva sin cambios, confirmada válida mediante perfilado de solo lectura.
- Agregado un paso explícito de exclusión de columnas (`Table.RemoveColumns`) en `Consolidado2025` para las 18 columnas del Excel restructurado que quedan fuera del alcance mínimo (Árbol de Nómina Nivel 2/3, Tipo Identificación, COD. CARGO, Tipo Contrato (Kactus), Indicador Actividad, Año Nac, variantes de nombre, etc.) — evita que Power BI Desktop las reincorpore automáticamente al modelo en cada refresh completo.
- Corregidas 16 referencias obsoletas a medidas (`PLANTA DE PERSONAL[Tot_empleados_Promedio/Tot_empleados]` → `Tbl_Medidas[...]`) en el bookmark "Generación", que impedían el orden descendente correcto del funnel tras el saneamiento de medidas de GOV-005.
- Alineados los colores del visual "Generación por Antigüedad en la compañía" con el Manual de Marca Grupo LEMCO: Baby Boomers `#000032`, Generación X `#1A3059`, Millennials `#1B487F`, Centennials `#F7931E` (antes usaba `#B3B3B3` y `#00A5E2`, fuera de marca).

### Documentado

- `Specs/0019_analisis_impacto_adaptacion_headcount_consolidado2025.md` y `Specs/0020_plan_implementacion_adaptacion_headcount_consolidado2025.md`: análisis de impacto, decisiones A-F aprobadas, plan de implementación y resultado de validación técnica completa (52 tablas / 66 relaciones / 122 medidas, 0 duplicadas; verificación en vivo de `GENERACIÓN`, tabla generacional, orden del funnel, colores y que Unión Libre permanece intacta).
- Registrada `DATA-013` en `Specs/00_roadmap_y_backlog.md`: deuda de calidad de datos preexistente en la fuente (valores de error `#N/A` de Excel en 8 columnas — `DEPENDENCIA_PATRON`, `AREA_PATRON`, `FECHA NACIMIENTO`, `EDAD`, `Generación`, `RANGO DE EDAD`, `EST_CIVIL`, `AGRUPADOR`), confirmada como ajena al código de `DATA-012` (6 de 8 columnas nunca son tocadas por esta iniciativa) y no corregida, per decisión explícita de alcance del usuario.
- `DATA-012` y `DATA-005` (absorbida en `DATA-012`) actualizadas en `Specs/00_roadmap_y_backlog.md` de "próxima implementación" a "Finalizadas".

## [Sin version] - 2026-08-10 (GOV-005)

### Corregido

- Saneadas 27 medidas declaradas dos veces en el modelo (una copia en su tabla de dominio — `AUSENTISMOS`, `SST GENERAL`, `Ppto Ingresos`, `Selección Grupo Lemco`, `Selección Challenger`, `SENA UNIDADES`, `ACCIDENTALIDAD` — y otra en `Tbl_Medidas`), defecto preexistente en `origin/main` que impedía abrir un checkout limpio de `Proyecto7.pbip` en Power BI Desktop (`PFE_TM_OBJECT_NAME_ALREADY_EXISTS`). Se eliminó en cada caso la copia sin consumidores reales, preservando fórmula y `lineageTag` de la copia conservada: 26 medidas mantenidas en su tabla de dominio (eliminada la copia de `Tbl_Medidas`) y 1 (`Tot_Accidentes`) mantenida en `Tbl_Medidas` (eliminada la copia de `ACCIDENTALIDAD`), por ser la efectivamente referenciada por el reporte. No se modificó ninguna fórmula ni `lineageTag` de las medidas conservadas.
- Modelo tras el saneamiento: 122 medidas (149 − 27), 0 duplicados, 0 referencias rotas.

### Documentado

- `Specs/0018_saneamiento_medidas_duplicadas_gov005.md`: inventario completo, criterio de ubicación canónica, tratamiento de las 7 definiciones con fórmula divergente bajo el mismo `lineageTag`, y validaciones.
- `GOV-005` actualizada en `Specs/00_roadmap_y_backlog.md` de "próxima implementación" a "Finalizada" tras GATE 5 aprobado.

## [Sin version] - 2026-08-10

### Cambiado

- Desactivado el subtotal de fila (`rowSubtotals: false`) del visual `f702a32db8dfea04babc` (matriz principal de `Retiros`): la fila de "Total general" solo repetia la fila del año 2026 (unico año en el contexto de filtro) y no aportaba informacion adicional. No se creo ninguna medida nueva para este ajuste.

### Agregado

- Cerrado `DAX-002` en `Specs/00_roadmap_y_backlog.md` (movido de "En curso" a "Finalizadas"): GATE 5 ejecutado en vivo via `powerbi-modeling-mcp` conectado a la instancia abierta de `Proyecto7.pbip`, y aprobado por el usuario contra el contexto `Planta Ppto[Ppto/Real] = "Real"`. Cifras acumuladas enero-julio 2026 validadas: 2.423 colaboradores promedio sin SENA, 828 ingresos, 627 retiros, Variacion Neta 1,19 %, Indice de Rotacion 30,03 %, Tasa Mensual de Retiros 3,70 %, Tasa Acumulada de Retiros 25,88 % (mas validacion puntual de Challenger enero y acumulado).
- Registrada `PBIP-005` en `Specs/00_roadmap_y_backlog.md`: desagregacion de indicadores de retiros/rotacion por Dependencia, Area y Cargo en `Retiros`, iniciativa independiente y pendiente de analisis de impacto propio.

### Documentado (sin corregir, deuda funcional trasladada a PBIP-005)

- Las medidas basadas en `Total-Sena` (`SumadeTotal-Sena`, `PromediodeTotal-Sena`, `Variacion_Neta_Personal`, `Tasa_Mensual_Retiros`, `Indice_Rotacion`, `Tasa_Acumulada_Retiros*`) no filtran `Planta Ppto[Ppto/Real] = "Real"` internamente; hoy son correctas porque cada visual que las usa repite ese filtro a nivel de visual. Riesgo documentado en `Specs/0016` seccion 8 para cualquier visual futuro que las use sin ese filtro.
- Diagnosticada la medida legado `Índice_Retiros` (no tocada): formula sin proteccion `DIVIDE`, y los valores `Infinito`/inconsistentes reportados por el usuario se deben a filtros de visual obsoletos (`Años[Año] = '2025'` en `8d3d8ab39e15678e422a`, y una unica `Dependencia` fija en `5abcdd8fd1c5a1015723`), no a la formula en si bajo un contexto limpio. Confirmado que **no es equivalente** a `Tasa_Mensual_Retiros` (1,21 % vs. 3,70 % bajo el mismo contexto de control) — no se migra ni se elimina, queda como deuda funcional de `PBIP-005`.

## [Sin version] - 2026-08-06

### Cambiado

- Renombradas 6 medidas de rotacion/retiros en `Tbl_Medidas` para que el nombre tecnico represente la formula que calculan: `Ind_Rot`->`Variacion_Neta_Personal`, `Ind_Retiros`->`Tasa_Mensual_Retiros`, `Rotacion_Anual_Acumulada`->`Tasa_Acumulada_Retiros`, `Rotacion_Voluntaria_Anual_Acumulada`->`Tasa_Acumulada_Retiros_Voluntarios`, `Rotacion_Involuntaria_Anual_Acumulada`->`Tasa_Acumulada_Retiros_Involuntarios`, `Rotacion_Segun_Tipo`->`Tasa_Acumulada_Retiros_Segun_Tipo`. Se conservo el `lineageTag` de cada medida. Se actualizaron todas las referencias dependientes (5 visuales, 4 bookmarks, sinonimos Q&A en `cultures/es-ES.tmdl`, `Docs/METRICS_CATALOG.md`).
- Corregida en `Docs/METRICS_CATALOG.md` una entrada obsoleta que documentaba una medida `Indice_Rotacion` distinta (contexto `Ppto Retiros`) que ya no existe en el modelo.

### Agregado

- Nueva medida `Indice_Rotacion` en `Tbl_Medidas`: `((Ingresos + Retiros) / 2) / Promedio de Total-Sena`. Agregada a la matriz principal de `Rotación2` junto a Ingresos, Retiros, Variacion Neta Mensual, Tasa Mensual y Tasa Acumulada de Retiros.
- `Specs/0016_renombramiento_medidas_rotacion_retiros.md`: documenta el problema, la definicion funcional de cada indicador, la formula de origen de `Ingresos`/`Retiros` en el archivo fuente, el uso de `Total-Sena`, las medidas renombradas y la nueva medida, con GATE 5 (conciliacion numerica en Power BI Desktop) pendiente de ejecutar.
- Iniciativa `DAX-002` registrada en `Specs/00_roadmap_y_backlog.md`, estado "En validacion".

### Corregido

- Restaurado el filtro `Generaciones[Generacion] <> null` en el visual `30f11733eea2697476d4` de la pagina `Demografico (Promedio)`, perdido por un guardado previo de Power BI Desktop (regresion no solicitada).
- Eliminada la relacion autodetectada `Consolidado2025[Generacion 2] -> Generaciones[Generacion]`, no solicitada. Verificado que su eliminacion no genero errores de referencia (recarga del modelo via MCP: 0 errores).

### Conservado (decisiones explicitas del usuario)

- Eliminacion intencional del filtro `Empresas[Grupo Empresa] = 'Habitel Hotels'` en el visual `a4193576029d03d04cb5` de `Rotacion2`.
- `"visibility": "HiddenInViewMode"` en el `page.json` de `Rotacion2` (pagina de detalle con navegacion interna "Volver al informe").

## [Sin version] - 2026-08-03

### Agregado

- `Data/Contratos_Kactus/`: estructura operativa organizada manualmente con separacion entre `Fuente_Oficial`, `Historico` e `Insumos_Vigentes`.
- Documentacion del procedimiento mensual para fuentes de contratos Kactus, incluyendo controles para evitar que respaldos historicos entren al proceso activo.
- Registro de sensibilidad alta para la fuente de contratos Kactus y confirmacion de exclusion total de `Data/` en Git.
- Roadmap actualizado para dar seguimiento a la validacion de consumidores, archivo oficial y rutas de Power BI asociadas a contratos Kactus.

### Validado

- `CONSOLIDADOR_CONTRATOS_V0.0.0.xlsx`: archivo oficial identificado en `Data/Contratos_Kactus/Fuente_Oficial/`.
- Consultas Power Query internas del consolidador validadas: 9 consultas fuente apuntan a `Data/Contratos_Kactus/Insumos_Vigentes/` en SharePoint corporativo y `Fact_Contrataciones` combina esas fuentes.
- Refresh del consolidador ejecutado desde Excel Desktop sin excepcion capturada y sin consultas pendientes de actualizacion.

### Sin cambios

- No se modificaron PBIP, Power Query del PBIP, TMDL, DAX, relaciones ni visuales.
- No se declaro `Fuente_Oficial/` como fuente activa de `PBIP/Proyecto7.pbip` porque no se encontro evidencia de consumo en consultas o TMDL versionados.
- No se versiono `CONSOLIDADOR_CONTRATOS_V0.0.0.xlsx`; el archivo permanece excluido por la regla `Data/`.

## [Sin version] - 2026-07-24

### Agregado

- Medida `Tot_empleados_Promedio_Sin_Aprendices`: promedio mensual de colaboradores excluyendo los tipos de contrato auditados como aprendizaje o SENA, sin modificar la medida base `Tot_empleados_Promedio`.
- Consulta DAX `Demografico (Promedio)`: se limita a 2026, agrega un resultado total anual y prepara el detalle Dependencia-Area-Cargo para copiar a Excel con coma decimal mediante `FORMAT(..., "es-CO")`.
- Consulta DAX `Demografico (Promedio)`: se documenta la validacion cruzada contra `Retiros`, confirmando `2524,8571428571427` para 2026, `2423,714285714286` sin aprendices y `2572` / `2465` para junio y julio de 2026 bajo filtros equivalentes.
- Consulta DAX `Demografico (Promedio)`: se revalida contra el modelo abierto con la carga vigente de `PLANTA DE PERSONAL`, registrando `2524,8571428571427` como promedio total 2026, `2423,714285714286` como promedio sin aprendices y `1040` filas de detalle Dependencia-Area-Cargo.
- Consulta DAX `Demografico (Promedio)`: se agrega una validacion en DAX Query View para devolver Dependencia, Area, Cargo y el promedio de colaboradores reutilizando `Tbl_Medidas[Tot_empleados_Promedio]`, sin crear objetos nuevos en el modelo ni modificar visuales del reporte.
- Pagina `Demografico (Promedio)`: se agregan segmentadores de Area y Cargo en el panel lateral izquierdo, debajo de Dependencia, usando campos de `PLANTA DE PERSONAL` y conservando el patron desplegable con busqueda, seleccion multiple y opcion `Seleccionar todo`.
- `PBIP/00_Referencia_Historica/`: carpeta con versiones historicas del reporte en formato `.pbix` (previas a la migracion a PBIP) y un tema de color (`PaletaAzulProfesional.json`). Documentada en `ESTRUCTURA_PROYECTO.md`. Solo el tema JSON se versiona; los 5 archivos `.pbix` quedan excluidos via `.gitignore` por tratarse de binarios no necesarios para reproducir `Proyecto7.pbip` y por sensibilidad de datos sin verificar (ver `SECURITY_AND_PRIVACY.md`).

### Corregido

- Pagina `Retiros`: los segmentadores temporales pasan de `DimPeriodoYM` a las dimensiones compartidas `Años` y `Mes`, corrigiendo la propagacion hacia `PLANTA DE PERSONAL` y reconciliando `Tot_empleados_Promedio` con `Demografico (Promedio)` para 2026, junio y julio.
- Cierre funcional de las paginas `Productividad` y `Gasto Laboral`: se consolida en PBIR el estado final validado por el usuario, incluidos filtros y selecciones visuales, unidades monetarias por contexto de negocio, titulos dinamicos y referencias a medidas centralizadas en `Tbl_Medidas`.
- `Productividad`: el grafico mensual usa `Titulo_Productividad_Gasto_Laboral`; el comparativo acumulado usa `Subtitulo_Productividad_Comparativo_Acumulado`, que diferencia ausencia de filtro, un mes, rango continuo, meses no consecutivos y todos los meses.
- `Gasto Laboral`: se conserva la presentacion aprobada en millones para Challenger/consolidado y en unidades automaticas o valores completos para otros negocios, sin cambios en los calculos.
- Se elimina el formato estatico de `GL_Ppto_Gasto_Personal` y `GL_Gasto_Personal` porque ya cuentan con `formatStringDefinition`; esto evita que Power BI Desktop rechace el proyecto por definir simultaneamente `FormatString` y `FormatStringDefinition`.
- Validaciones de cierre: apertura correcta de `Proyecto7.pbip` sin conflicto TMDL, aprobacion funcional del usuario para ambas paginas, parseo JSON/PBIR, auditorias DAX, semantica y navegacion, UTF-8 sin BOM y revision selectiva del diff Git.
- Pagina `Gasto Laboral`: el grafico mensual conserva millones con una cifra decimal para Challenger, vista consolidada y seleccion de todos los grupos; los demas negocios usan unidades automaticas.
- La tabla mensual presenta esos mismos contextos consolidados en millones y muestra para otros negocios los importes completos con una cifra decimal, incluidos filas y totales, sin convertir valores distintos de cero en cero visual.
- La tarjeta `Cumplimiento Gasto Laboral` referencia `Tbl_Medidas[Cump_GL]` y conserva una cifra decimal; no se modifico su formula ni el contexto de filtros.
- La implementacion reutiliza las sumas numericas existentes y limita el cambio a formato y seleccion de la variante visual, sin modificar calculos, relaciones, fuentes ni logica de negocio.
- Validaciones: Challenger, consolidado, todos los grupos y negocios distintos de Challenger; etiquetas, grafico, tabla, totales y tarjeta; parseo JSON/PBIR, auditorias DAX, semantica y navegacion, UTF-8 sin BOM y revision selectiva del diff Git.
- Pagina `Productividad`: la tabla `cba349945ec4b0577321` conserva los importes completos, sin abreviaturas, cuando el contexto corresponde a unidades de negocio diferentes de Challenger.
- Challenger, la vista consolidada y la seleccion de todos los grupos mantienen la presentacion monetaria en millones con una cifra decimal.
- El ajuste usa medidas numericas de presentacion en `Tbl_Medidas`; las expresiones base continuan siendo las sumas de `Gasto Personal` y `Ventas (MM)`, sin cambios en calculos, filtros ni logica de productividad.
- Las etiquetas y totales de la tabla comparten las mismas medidas y cadenas de formato dinamicas. Los graficos conservan sus medidas porcentuales y su comportamiento de unidades.
- Validaciones: escenarios 2025 y 2026 para Challenger, Grupo Sky, Habitel Hotels, Lemco y Fundacion Challenger; parseo JSON/PBIR, auditorias DAX y semantica, UTF-8 sin BOM y revision selectiva del diff Git.

## [Sin version] - 2026-07-21

### Corregido

- Pagina `Gasto Laboral`: se ajustaron las unidades visuales de `Presupuesto Gasto Personal` y `Gasto Personal` en el grafico `Gasto Labora (Ppto vs Ejecucion)` y la tabla mensual para evitar que negocios con valores menores frente a Challenger se mostraran como `$0,0 mill.`.
- Causa identificada: `labelDisplayUnits` estaba forzado a millones (`1000000D`) en las etiquetas/valores monetarios, con precision reducida.
- Solucion aplicada: las unidades de visualizacion quedaron sin escala forzada (`1D`) en las series/columnas monetarias, conservando calculos, medidas, colores, filtros, navegacion y diseno.
- Archivos PBIP modificados: `visuals/b351f0de695056ac18a5/visual.json` y `visuals/ced924c91be19c603ad0/visual.json` dentro de la pagina `2ee3ca8f42b01e9a6840`.
- Validaciones ejecutadas: parseo JSON de ambos visuales, revision de campos usados, revision de diff y `git diff --check`.

## [Sin version] - 2026-07-17

### Agregado

- `Docs/PROJECT_STATUS.md` para consolidar estado operativo, bloqueos vigentes y pendientes del proyecto.
- `Docs/GIT_GOVERNANCE.md` para documentar reglas de staging selectivo, commit y push.
- `Docs/TROUBLESHOOTING.md` para documentar diagnóstico y validación de Formula Firewall, rutas SharePoint y ruido PBIP.

### Modificado

- `README.md`, `AGENTS.md` y `CLAUDE.md` actualizados al estado real del proyecto `Proyecto7.pbip`.
- `Docs/README.md` actualizado como índice oficial de documentación.
- `Docs/PROJECT_CONTEXT.md`, `Docs/ARCHITECTURE.md`, `Docs/DATA_PIPELINE.md`, `Docs/RUNBOOK.md` y `Docs/SECURITY_AND_PRIVACY.md` alineados con Git activo, migración de fuentes a SharePoint corporativo y bloqueo vigente de Formula Firewall.

## [Sin version] - 2026-07-14

### Agregado

- Matriz de antiguedad al retiro en la pagina Retiros, con filas por `Ppto Retiros[Rango_Antiguedad_Retiro]`, columnas por `Anos[Ano]` y valores de `Tbl_Medidas[Tot_Retiros]`.
- Columnas tecnicas en `Ppto Retiros` para calcular antiguedad al retiro desde `Fecha Inicio` y `Fecha Vencimiento`: `Meses_Antiguedad_Retiro`, `Rango_Antiguedad_Retiro` y `Orden_Rango_Antiguedad_Retiro`.

### Modificado

- La clasificacion de antiguedad al retiro deja de usar `Meses de permanencia` como base funcional y pasa a calcularse desde las fechas reales del retiro.

## [Sin version] — 2026-07-03

### Agregado

- `Docs/ESTRUCTURA_PROYECTO.md`: estandar corporativo de carpetas, politica de archivos `.md`, nomenclatura de `Outputs/` (`NN_AAAA-MM-DD_descripcion_corta.md`) y criterio de actualizacion documental por tipo de cambio (commits `0cb85bf`, `936bfa8`, `5ffdb24`).
- `CLAUDE.md` versionado por primera vez, alineado con la estructura real del proyecto (commit `cd300b7`).
- Indice de `Docs/README.md` actualizado para incluir `ESTRUCTURA_PROYECTO.md`.

### Corregido

- `Docs/ARCHITECTURE.md` y `Docs/RUNBOOK.md`: referencias a `Proyecto.pbip` actualizadas a `Proyecto7.pbip` (archivo renombrado el 2026-06-17, commit `cfb3a15`).
- `Docs/BI_GUIDELINES.md`: inventario de paginas corregido de 21 a 19 (2 paginas de propuesta/rediseno ya no existen en el proyecto), pagina activa por defecto corregida a `Demografico (Promedio)`, conteo de bookmarks reverificado en 19 (no 20).
- `Docs/SECURITY_AND_PRIVACY.md`: agregada `Inputs/` como carpeta de riesgo pendiente de evaluar por datos personales.

## [Sin version] — 2026-06-17

### Modificado

- Renombrado el archivo principal del proyecto de `Proyecto.pbip` a `Proyecto7.pbip` (commit `cfb3a15`).
- Separado el rango de antiguedad demografico en dos categorias (commit `e8bb853`).

### Agregado

- Rotacion voluntaria por tipo de retiro en la pagina Retiros (commit `be55a2a`).

## [Trabajo en curso] - 2026-06-11

### Agregado

- Nueva pagina `Demografico (Promedio) - Rediseno LEMCO` (`ReportSectiond3m0c0rp20260611`) como propuesta visual adicional basada en un shell de HTML Content y visuales nativos de Power BI.
- Nueva medida `HTML Demografico Promedio Shell` en `Tbl_Medidas`, dentro de la carpeta `11 HTML Content`.
- Inventario tecnico de reorganizacion de medidas en `Outputs/documentation/inventario_medidas_reorganizadas_2026-06-11.csv`.

### Modificado

- Centralizacion de 88 medidas en `Tbl_Medidas`, organizadas por carpetas de visualizacion segun dominio funcional.
- Actualizacion de referencias de medidas en culturas, visuales y bookmarks para apuntar a la tabla contenedora `Tbl_Medidas`.
- Actualizacion del inventario de paginas y del catalogo de metricas.

### Validado

- Parseo correcto de 434 archivos JSON del reporte.
- 275 proyecciones de medidas revisadas en visuales/bookmarks sin referencias simples heredadas a tablas anteriores.
- 88 medidas declaradas unicamente en `Tbl_Medidas`, sin duplicados de nombre.

## [Sin version] — Estado actual al 2026-06-11

Estado del proyecto al momento del primer analisis tecnico documentado.

### Identificado como presente

- 19 paginas de reporte (10 visibles, 5 ocultas, 1 portada, 1 actualizacion, 1 QA, 1 demografico promedio)
- 53 tablas en el modelo semantico
- 41 relaciones explicitas
- Datos historicos desde 2024 hasta mayo 2026 (carpeta `Data/2026/05_Mayo/`)
- Consolidacion de HeadCount 2024 + 2025 via `Table.Combine` en `PLANTA DE PERSONAL`
- Tabla `DimPeriodoYM` calculada para soporte de logica de trimestres dinamicos
- Medidas de eficiencia de gasto laboral vs ventas
- Indicadores SST con indices de frecuencia y severidad
- Bookmarks para navegacion en SST y demografico

---

## Como usar este registro

Al realizar cambios en el proyecto, agregar una nueva entrada con el siguiente formato:

```markdown
## [vX.Y.Z o descripcion] — YYYY-MM-DD

### Agregado
- Nueva tabla / pagina / medida

### Modificado
- Descripcion del cambio y razon

### Corregido
- Bug corregido y descripcion del problema

### Eliminado
- Elemento eliminado y razon
```

> **Nota:** Este proyecto cuenta con control de versiones Git. Los cambios PBIP deben manejarse con staging selectivo por alcance; no usar `git add .`. El push requiere aprobacion explicita.
