# Guia de BI — Reporte Power BI

> Fuente oficial del inventario de paginas, bookmarks, recursos visuales y convenciones del reporte.
> Para el modelo de datos ver [DATA_MODEL.md](DATA_MODEL.md).

---

## Inventario de paginas (19 paginas)

> Actualizado 2026-07-03: verificado contra `PBIP/Proyecto.Report/definition/pages/` (19 carpetas) y `pages.json` (`pageOrder`, `activePageName`). Version anterior de este documento (2026-06-11) listaba 21 paginas, incluyendo 2 que ya no existen — ver "Paginas eliminadas" abajo.

Las paginas estan ordenadas segun `pages.json`. La pagina activa por defecto al abrir el reporte es **Demografico (Promedio)** (`ReportSectionf46593dd92bf9359ceef`) — confirmado en `pages.json → activePageName`.

| # | ID Tecnico | Nombre Display | Visibilidad | Tamano (px) | Dominio | Observaciones |
|---|---|---|---|---|---|---|
| 1 | `ReportSection` | Portada | Visible | 1280×720 | Presentacion | Imagen de fondo `PORTADA.JPG`. Sin visuales interactivos. |
| 2 | `f0fd1eb45022c4c0718e` | Demografico | **Oculta** | 2100×900 | HeadCount | Version original. Reemplazada por "Demografico (Promedio)". |
| 3 | `ReportSectionf46593dd92bf9359ceef` | Demografico (Promedio) | Visible *(activa por defecto)* | 2100×900 | HeadCount | Pagina activa al abrir el reporte. |
| 4 | `e1c2430c70e803cf0105` | Comportamiento_HC_Anual_v2 | **Oculta** | 1600×900 | HeadCount | Version de desarrollo. |
| 5 | `ReportSectionddae17c80e69979c7950` | Comportamiento HC Anual | **Oculta** | 1600×900 | HeadCount | Version original. |
| 6 | `cb53606ab281b70263cd` | Comportamiento_HC_Anual_v3 | **Oculta** | 1600×900 | HeadCount | Version de desarrollo. |
| 7 | `8bac02805d716481a924` | Comportamiento_HC_Anual_v4 | **Oculta** | 1600×900 | HeadCount | Version de desarrollo (posiblemente la mas reciente de este grupo). |
| 8 | `ReportSection65569958420c423d90b1` | Productividad | Visible | 1350×900 | PptovsReal | Eficiencia del gasto laboral vs ventas. |
| 9 | `ReportSection10f83a2531afc6f0ce74` | Comportamiento HC Mensual | Visible | 1300×800 | HeadCount | Evolucion mensual Ppto vs Real. |
| 10 | `ReportSectione5ed8d42954b67ebd207` | Product. (Colaboradores) | Visible | 1400×900 | PptovsReal | Productividad por colaborador. |
| 11 | `ReportSection6a1196bf8c963b709405` | Retiros | Visible | 1800×1000 | HeadCount / Retiros | Analisis de retiros. |
| 12 | `ReportSectiondc346876696ee4cba0ab` | Rotacion2 | Visible | 1600×900 | HeadCount | Rotacion de personal. |
| 13 | `ReportSectionb8786793985340abe503` | Ausentismos | Visible | 1700×900 | Ausentismo | Analisis de ausentismo laboral. |
| 14 | `ReportSection4898baca26ffb5b4ff94` | Seleccion | Visible | 2300×1500 | Seleccion | Gestion de requisiciones. Pagina mas ancha del reporte (2300px). |
| 15 | `3a3097703dd04ce49097` | Indicadores | Visible | 1700×900 | Consolidado | Dashboard de KPIs. |
| 16 | `2ee3ca8f42b01e9a6840` | Gasto Laboral | Visible | 1400×900 | PptovsReal | Analisis del gasto en nomina. |
| 17 | `ReportSection7b0e40b552d4038186ba` | SST | Visible | 2000×1200 | SST | Seguridad y Salud en el Trabajo. |
| 18 | `3ade8360a92289e7b288` | Fecha de Actualizacion | Visible | 1280×720 | Operacional | Muestra la fecha y hora de la ultima actualizacion del modelo. |
| 19 | `18513b73a4b6e3d9d08c` | QA_Demografico | Visible | 2100×900 | QA | Pagina de control de calidad de datos demograficos. **Visible para usuarios finales** — `Pendiente de decision`: si debe ocultarse o mantenerse. |

### Paginas ocultas (HiddenInViewMode)

Existen **5 paginas ocultas** que representan versiones descartadas o en desarrollo:

- `Demografico` (version original)
- `Comportamiento_HC_Anual_v2`, `v3`, `v4`
- `Comportamiento HC Anual` (version original)

> Estas paginas incrementan el tamano del archivo PBIP y pueden confundir a futuros desarrolladores. Se recomienda eliminarlas o documentar su estado en [decisions/README.md](decisions/README.md) antes de hacerlo — ver ADR-005.

### Paginas eliminadas (ya no existen en el proyecto)

Las siguientes 2 paginas figuraban en la version anterior de este documento (2026-06-11) como propuestas de rediseño visibles, pero **no existen hoy** en `PBIP/Proyecto.Report/definition/pages/` (verificado 2026-07-03):

| ID Tecnico (historico) | Nombre Display (historico) | Estado |
|---|---|---|
| `ReportSectiona1b2c3d4e5f6a7b8c9d0` | Demografico (Promedio) - Propuesta 1 | Eliminada |
| `ReportSectiond3m0c0rp20260611` | Demografico (Promedio) - Rediseno LEMCO | Eliminada |

No se encontró un ADR ni entrada de `CHANGELOG.md` que documente cuándo ni por qué se eliminaron — `Pendiente de confirmar`.

---

## Bookmarks (19 bookmarks)

> Reverificado 2026-07-03 contra `PBIP/Proyecto.Report/definition/bookmarks/bookmarks.json`: 6 grupos con 3+3+3+3+4+3 = 19 bookmarks individuales. (Un conteo previo con `ls .../bookmarks | wc -l` daba 20 porque incluía `bookmarks.json`, que es el archivo índice de grupos, no un bookmark — corregido aquí.)

Los bookmarks estan organizados en 6 grupos. Se usan para navegacion o para capturar estados de filtro.

| Grupo (nombre display) | ID del grupo | Bookmarks hijos | Uso inferido |
|---|---|---|---|
| `Analisis AT` | `f3767c3ab9372ab36d49` | 3 bookmarks | Analisis de accidentes de trabajo (AT) en pagina SST |
| `AT_Comp` | `ab189ef284fe549bef33` | 3 bookmarks | Comparativa de accidentes de trabajo |
| `AT_Demo` | `88ac2f912ad465c3accd` | 3 bookmarks | Demografia en contexto de accidentes de trabajo |
| `Demo` | `c5ec4e2934c8e1936ac0` | 3 bookmarks | Vistas demograficas |
| `Retiros` | `7eb37946800d59fec5e8` | 4 bookmarks | Estados de la pagina Retiros |
| `Demo_Prom` | `c5dd471749b83d4390d2` | 3 bookmarks | Demografico con promedios |

> Los bookmarks sin grupo (hijos sin nombre de grupo) corresponden a los 19 archivos individuales `.bookmark.json`.

---

## Recursos visuales embebidos

Almacenados en `PBIP/Proyecto.Report/StaticResources/RegisteredResources/`:

| Archivo | Uso inferido |
|---|---|
| `PORTADA18920577165717556.JPG` | Imagen de fondo de la pagina Portada |
| `EMPLEADOS72156857087858.JPG` | Imagen decorativa (posiblemente en paginas de HeadCount) |
| `mujer04147851821615234.png` | Icono de genero femenino |
| `hombre7095070102732959.png` | Icono de genero masculino |

---

## Tema visual

- **Tema base:** `CY23SU08` (tema estandar de Power BI, version noviembre 2023)
- **Ubicacion:** `StaticResources/SharedResources/BaseThemes/CY23SU08.json`
- **Personalizacion adicional:** `Pendiente de confirmar` (no se identificaron overrides de tema en el reporte)

---

## Configuracion del reporte (`report.json`)

| Configuracion | Valor | Efecto |
|---|---|---|
| `exportDataMode` | `AllowSummarized` | Los usuarios solo pueden exportar datos resumidos, no datos subyacentes |
| `defaultFilterActionIsDataFilter` | `true` | Los filtros actuan como filtros de datos por defecto |
| `defaultDrillFilterOtherVisuals` | `true` | El drill-through filtra los otros visuales de la pagina |
| `useEnhancedTooltips` | `true` | Tooltips mejorados habilitados |
| `customMemoryLimit` | `1048576` KB (1 GB) | Limite de memoria personalizado para el reporte |
| `customTimeoutLimit` | `225` segundos | Timeout de consulta personalizado (3 min 45 s) |
| `useStylableVisualContainerHeader` | `true` | Cabeceras de visuales con estilo personalizable |

---

## Convenciones identificadas en el proyecto

### Nomenclatura de tablas
- Tablas de hechos principales: mayusculas (`PLANTA DE PERSONAL`, `AUSENTISMOS`)
- Tablas de presupuesto: `Ppto` como prefijo (`Planta Ppto`, `Ppto Retiros`)
- Tablas de seleccion: `Seleccion [Empresa]`
- Tablas de SST por empresa: sigla de empresa como sufijo (`SST_CHA`, `SST-HABITELH`, `SST-GSKY`)
- Dimensiones: nombre descriptivo en CamelCase o mayusculas (`Empresas`, `Maestro`, `AREAS`)
- Tablas de medidas: prefijo `Tbl_` o `tbl_` (`Tbl_Medidas`, `tbl_Refresh`)
- Tabla calculada de periodo: prefijo `Dim` (`DimPeriodoYM`)

### Nomenclatura de medidas
- Totales: `Tot_` como prefijo (`Tot_empleados`, `Tot_Fijo`)
- Promedios: `Prom_` como prefijo o `_prom` como sufijo
- Porcentajes: `%` como prefijo (`%FEM`, `%Efiprom`) o sufijo (`Tasa_`)
- Indices/KPI: `Ind_`, `KPI_`, `M_` como prefijos
- Medidas fijas con patron ISINSCOPE: sufijo `_FIX`

### Columnas calculadas (grupos de datos)
Varias columnas usan el patron de **grupos de datos** de Power BI para normalizar valores con multiples variaciones textuales:
- `TIPO_CONTR (grupos)` en `PLANTA DE PERSONAL`
- `EST_CIVIL (grupos)` en `PLANTA DE PERSONAL`
- `Detalle (grupos)` en `Ppto Retiros`
- `Clase de nomina (grupos)` y `Clase de nomina (grupos) 2` en `Ppto Retiros`

### Indicadores de semaforo
Las medidas `KPI_PPTO`, `KPI_REAL` y `KPI_EFI` usan `UNICHAR` para mostrar flechas:
- `UNICHAR(129093)` = flecha hacia arriba
- `UNICHAR(129095)` = flecha hacia abajo

---

## Estándares reutilizables para desarrollo Power BI/PBIP

Esta sección es la fuente canónica para diseñar, construir, corregir y
validar páginas del reporte. Aplica tanto a mejoras de páginas existentes
como a páginas nuevas. La estructura de artefactos se rige por
[ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md), el versionamiento por
[GIT_GOVERNANCE.md](GIT_GOVERNANCE.md) y la protección de información por
[SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md).

### 1. Diseño y construcción de páginas

Antes de construir una página se debe definir:

1. Propósito, audiencia y decisión que apoyará.
2. Pregunta de negocio principal y preguntas secundarias.
3. Contextos de filtro que deben compararse.
4. Indicadores, detalle y nivel de granularidad necesarios.
5. Criterios funcionales, visuales y de aceptación.

Reglas de diseño:

- Usar títulos y subtítulos dinámicos cuando el periodo o contexto de
  negocio cambie la interpretación.
- Diseñar sobre una cuadrícula consistente. Alinear bordes, conservar
  espaciado regular y usar jerarquía visual para distinguir contexto,
  indicadores, tendencias y detalle.
- Mantener colores, tipografías, encabezados, navegación y densidad
  coherentes con las páginas existentes.
- Asignar nombres técnicos identificables a segmentadores, gráficos,
  tablas, botones y visuales que tengan lógica o validaciones relevantes.
- Revisar el orden Z en el panel de selección. Las capas deben seguir un
  orden comprensible y estable: fondo, decoración, contenido y controles.
- Mantener el orden de tabulación alineado con la lectura: contexto,
  filtros, indicadores, gráficos, tablas y acciones.
- Excluir del orden de tabulación fondos, formas, imágenes decorativas y
  elementos sin interacción.
- Revisar la vista móvil cuando la página esté destinada a consumo móvil;
  su orden es independiente del orden Z y del diseño de escritorio.
- No superponer visuales funcionales para simular formatos dinámicos,
  alternar escalas o esconder estados. Debe preferirse un único gráfico o
  tabla resuelto mediante medidas numéricas, formatos dinámicos,
  parámetros o propiedades del visual.
- Una superposición solo es aceptable para decoración no interactiva y
  debe quedar fuera del orden de tabulación.

### 2. Formatos dinámicos y unidades

- Las medidas base deben conservar tipo numérico.
- No usar `FORMAT()` cuando el resultado deba ordenar, agregar, participar
  en cálculos o producir totales numéricos.
- Resolver la presentación con dynamic format strings o
  `formatStringDefinition`. Una medida no puede declarar a la vez
  `formatString` y `formatStringDefinition`.
- Filas y totales deben utilizar la misma medida y la misma regla de
  formato; no crear una medida textual separada para el total.
- Un valor distinto de cero no puede mostrarse como cero por una escala o
  precisión inadecuada.
- Corregir problemas visuales en el formato o en la configuración del
  visual, no alterando el cálculo ni multiplicando o dividiendo la medida.
- Validar unidad, escala, separadores y magnitud contra la fuente. No
  agregar ceros ni factores manuales sin una unidad oficial documentada.
- Separar problemas de formato de problemas de calidad de datos. Un
  resultado bien formateado no demuestra que el dato sea correcto.

Regla de presentación vigente de este proyecto, no regla universal para
otros modelos:

| Contexto | Gráficos | Tablas y matrices |
|---|---|---|
| Challenger o vista consolidada | Millones, una cifra decimal | Millones, una cifra decimal |
| Otros negocios | Unidades automáticas | Valor completo, sin abreviación |

Si otra página necesita una regla diferente, debe justificarla en su Spec
y documentar la unidad de negocio, moneda y escala esperadas.

### 3. Filtros, segmentadores e interacciones

- Usar dimensiones gobernadas para `Año`, `Mes`, `Grupo Empresa` y
  `Empresa`; evitar filtros directos sobre columnas equivalentes de tablas
  de hechos.
- Definir explícitamente si cada segmentador admite selección única o
  múltiple, su estado inicial y si permite seleccionar todo.
- Excluir o tratar valores nulos de forma explícita. No ocultarlos sin
  verificar si representan un problema de calidad de datos.
- Documentar sincronización entre páginas, selecciones persistidas y
  alcance de cada filtro: visual, página o informe.
- Revisar las interacciones de cada segmentador con todos los visuales de
  la página; no asumir que la propagación del modelo garantiza la
  interacción visual correcta.
- Validar por separado la vista consolidada, un grupo y una empresa. Una
  selección de empresa debe ser coherente con su grupo.
- No cambiar relaciones a bidireccionales sin causa raíz, análisis de
  ambigüedad y validación de efectos laterales.
- No introducir `TREATAS`, `REMOVEFILTERS`, `ALL` u otras excepciones de
  contexto para ocultar una relación o propagación defectuosa sin
  evidencia técnica.
- Registrar los filtros persistidos por Power BI Desktop antes del commit,
  porque pueden modificar el estado inicial que verá el usuario.

### 4. Órdenes independientes en Power BI

Los siguientes órdenes resuelven problemas distintos y deben validarse por
separado:

| Orden | Propósito | Ejemplo del proyecto |
|---|---|---|
| Z o capas | Define qué elemento queda delante o detrás | Fondo debajo del gráfico y segmentadores encima |
| Tabulación | Define el recorrido con teclado | Año antes de Mes, Grupo Empresa y Empresa |
| Datos del visual | Ordena categorías o valores mostrados | Meses en secuencia cronológica |
| `sortByColumn` | Ordena una columna por otra columna estable | `Mes[Meses]` por `Mes[Numero]` |
| Campos | Define la secuencia de columnas, ejes o leyendas | Mes, presupuesto, ejecución y cumplimiento |
| Jerarquía de drill | Define los niveles de navegación analítica | Grupo Empresa antes de Empresa |
| Diseño móvil | Define posición y lectura en el lienzo móvil | Indicadores antes de gráficos y detalle |

No se debe corregir un orden modificando otro. Por ejemplo, mover una capa
no corrige la tabulación y ordenar alfabéticamente un visual no reemplaza
`sortByColumn`.

### 5. Validación funcional y visual

Toda mejora o página nueva debe contar con una matriz de pruebas. Como
mínimo:

| Contexto | Qué validar |
|---|---|
| Consolidado | Totales, unidades, título, subtítulo y ausencia de filtros residuales |
| Challenger | Valores y presentación específica del negocio |
| Otro grupo | Propagación de filtros, magnitud y unidades |
| Empresa | Coherencia con el grupo y detalle disponible |
| Dos años | Comparaciones, títulos, acumulados y totales |
| Varios meses | Orden cronológico, rangos y selecciones no consecutivas |

Para cada contexto se debe revisar:

- captura con los filtros visibles;
- título y subtítulo;
- indicadores y etiquetas;
- gráficos y escalas;
- tabla, filas y totales;
- unidades, magnitud y meses;
- ausencia de superposición entre visuales funcionales;
- comparación contra la fuente o una reconciliación aprobada.

Cada resultado se clasifica como:

- **Conforme:** coincide con la regla y la fuente.
- **No conforme:** existe una diferencia reproducible.
- **No concluyente:** falta fuente, acceso, contexto o evidencia; no debe
  presentarse como validación satisfactoria.

La prueba funcional se realiza en Power BI Desktop sobre
`PBIP/Proyecto7.pbip`. Después del commit se debe verificar que la versión
publicada o desplegada corresponde al mismo commit validado; guardar en
Desktop y publicar son acciones distintas.

### 6. Validaciones estáticas PBIP

La profundidad de validación debe ser proporcional al riesgo, pero el
paquete de cierre debe confirmar:

- JSON válido y compatible con el esquema PBIR aplicable.
- TMDL válido.
- DAX válido, evaluado con herramientas del modelo o Power BI Desktop.
- Sin medidas duplicadas.
- Sin referencias colgantes entre visuales, medidas, columnas o tablas.
- UTF-8 sin BOM en `.json` y `.tmdl`.
- Ausencia de mojibake.
- `git diff --check -- <rutas del alcance>` limpio.
- El PBIP abre, refresca y guarda sin errores cuando el alcance requiere
  esas operaciones.

Contar paréntesis no constituye validación suficiente de DAX ni TMDL. Si
no se ejecuta refresh por restricciones del alcance o por un incidente
separado, debe registrarse como **no ejecutado**, no como satisfactorio.

### 7. Cierre y trazabilidad

- Conservar en `Specs/` el análisis de impacto, el plan y los criterios de
  aprobación; en `Outputs/`, la evidencia temporal; y en `Docs/`, el
  estándar o estado oficial. La política completa está en
  [ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md).
- Antes de versionar, revisar el diff PBIP y clasificar el ruido generado
  por Desktop.
- El commit debe incluir solo el bloque lógico aprobado y su documentación
  directamente asociada.
- Las reglas de staging, mensaje, push y preservación de cambios ajenos se
  mantienen exclusivamente en
  [GIT_GOVERNANCE.md](GIT_GOVERNANCE.md).
