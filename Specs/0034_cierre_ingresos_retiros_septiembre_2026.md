# 0034 - Cierre de INGRESOS y RETIROS de septiembre 2026 (PptovsReal)

## Objetivo

Dejar documentado el cierre operativo de las hojas `INGRESOS` y `RETIROS` de
`Data/HeadCount/PptovsReal.xlsx` para el periodo de septiembre de 2026,
incluyendo la fuente canónica real de la población mensual, las reglas de
población y de homologación aplicadas, los controles ejecutados, el incidente
operativo con AutoSave y su procedimiento seguro resultante, y los pendientes
que no bloquean el cierre.

Esta spec es **documental**. No modifica `Data/`, `PBIP/`, el modelo semántico,
Power Query, DAX, scripts ni pruebas.

## 1. Alcance

- Destino operativo: `Data/HeadCount/PptovsReal.xlsx`, hojas `INGRESOS` y
  `RETIROS`.
- Periodos intervenidos: **agosto de 2026** (un ingreso faltante tardío) y
  **septiembre de 2026** (población completa de ingresos y retiros).
- No se modificó ningún otro periodo ni ninguna otra hoja del libro.

Fuera de alcance:

- Refactorizar `Scripts/headcount/validar_ingresos_retiros.py` (ver sección 8).
- Completar las 10 fechas de nacimiento pendientes (ver sección 7).
- Incorporar fórmulas a las 19 filas manuales de agosto que nunca las tuvieron.
- Cualquier cambio en `PBIP/`, Power Query, DAX o el modelo semántico.

## 2. Fuente canónica de la población mensual

La referencia operativa es **`Fact_Contrataciones`** del consolidador oficial:

`Data/Contratos_Kactus/Fuente_Oficial/CONSOLIDADOR_CONTRATOS_V0.0.0.xlsx`

`Fact_Contrataciones` es la unión literal de las nueve fuentes de
`Data/Contratos_Kactus/Insumos_Vigentes/`. La equivalencia se verificó por
conteo: la suma de las nueve fuentes coincide exactamente con el número de
registros de la tabla del modelo.

### Las hojas mensuales no son fuente canónica

Las hojas `<mes>, A`, `<mes> II`, `<mes> III`, `<mes>, I` del consolidador son
**exportaciones *drill-through* manuales** (`Tabla_DatosExternos_N`), no
consultas del flujo. Cada una refleja el momento en que alguien la extrajo, y la
fila 1 conserva el texto de la consulta que la generó, incluido su filtro.

El caso de agosto de 2026 lo demuestra:

| Hoja | Registros | Naturaleza |
|---|---:|---|
| `Ago II` | 94 | extracción **temprana e incompleta** |
| `Ago III` | 113 | extracción **posterior y completa** |

Ambas declaran la misma población (`Indicador Actividad = I`), `Ago II` es
subconjunto estricto de `Ago III`, y los 19 registros de diferencia son eventos
de cierre de mes (vencimientos del 26 al 31 de agosto). La población definitiva
de retiros de agosto es **113**, no 94. Julio replica el patrón: `jul, I` (126)
⊂ `jul, II` (146).

El sufijo `I`/`II`/`III` **no codifica la regla de población**: indica el orden
de las extracciones sucesivas. Derivar la población directamente de
`Fact_Contrataciones` elimina esta ambigüedad.

## 3. Reglas de población

### INGRESOS

- `Fecha Inicio` dentro del periodo.
- **No** se filtra por `Indicador Actividad`.

Verificación: la hoja de ingresos de agosto mezcla `A` e `I`, lo que confirma
que el indicador no participa en la población de ingresos.

### RETIROS

- `Indicador Actividad = I`.
- `Fecha Vencimiento` dentro del periodo.

Esta regla reproduce agosto de forma **set-idéntica** (113 = 113, 0 faltantes,
0 adicionales) contra la hoja `RETIROS` ya cerrada.

> `Indicador Actividad` es un **estado puntual**, no un atributo del evento: se
> sobrescribe cuando la persona cambia de situación. Por eso el corte de un mes
> debe extraerse **después** del cierre de ese mes, y una re-extracción
> posterior puede alterar los conteos.

### Clave de evento

| Población | Clave |
|---|---|
| INGRESOS | `Identificación` + `Fecha Inicio` |
| RETIROS | `Identificación` + `Fecha Vencimiento` |

Ambas claves resultaron **únicas** en origen y destino para los dos periodos, de
modo que no fue necesario incorporar `Nro. Contrato` ni descartar filas.

## 4. Resultados del cierre

### INGRESOS

| Periodo | Kactus | PptovsReal | Faltantes | Adicionales |
|---|---:|---:|---:|---:|
| agosto 2026 | 147 | **147** | 0 | 0 |
| septiembre 2026 | 127 | **127** | 0 | 0 |

- Se incorporaron **128 registros**: 1 ingreso tardío de agosto y los 127 de
  septiembre.
- El ingreso tardío de agosto existía en la fuente actual pero no en la
  exportación con la que se cerró el mes: mismo fenómeno de extracción temprana
  descrito en la sección 2.
- Duplicados por clave de evento: **0**.
- `Tabla6` quedó en **5.549 filas y 27 columnas**, con sus **12 columnas
  calculadas** extendidas.

### RETIROS

| Periodo | Kactus | PptovsReal | Faltantes | Adicionales |
|---|---:|---:|---:|---:|
| agosto 2026 | 113 | **113** | 0 | 0 |
| septiembre 2026 | 102 | **102** | 0 | 0 |

- Se incorporaron **102 registros** de septiembre. Agosto no se modificó.
- Duplicados por clave de evento: **0**.
- La hoja no tiene tabla estructurada: es un rango plano, por lo que las
  fórmulas se replicaron explícitamente desde una fila completa del bloque
  normal de agosto.

Distribución de los retiros de septiembre:

| Grupo empresarial | Empresa | Retiros |
|---|---|---:|
| Challenger | Challenger | 62 |
| Habitel Hotels | Habitel Select | 11 |
| Habitel Hotels | Lemco Salvio | 11 |
| Habitel Hotels | Habitel Prime | 8 |
| Grupo Sky | Sky Logística Integral | 7 |
| Lemco | Lemco | 2 |
| Grupo Sky | Sky Forwarder | 1 |
| **Total** | | **102** |

Campos derivados de septiembre: `Dependencia`/`Área` **102/102** por combinación
histórica exacta de `CARGO_CCO`, y `Nivel` **102/102** por la homologación
vigente de `NIVEL_DE_CARGO`.

## 5. Homologación de empresa

La jerarquía aplicada, en orden de precedencia:

1. **reglas especiales aprobadas** por el usuario para este corte;
2. **lógica vigente del `Consolidado 2025`**: unión por `ID` tomando el registro
   del periodo más reciente y traducción al catálogo oficial
   (`Empresas.tmdl` + `Grupo Empresarial.tmdl`);
3. **homologación previamente validada** para los orígenes con destino único,
   usada solo cuando las dos anteriores no aplican.

### Reglas especiales aprobadas

| Origen Kactus | Clase de nómina | Grupo empresarial | Empresa |
|---|---|---|---|
| `LEMCO SAS` | `LEMCO SALVIO` | Habitel Hotels | Lemco Salvio |
| `HABITEL S.A.S.` | `SELECT` | Habitel Hotels | Habitel Select |
| `HABITEL S.A.S.` | `PRIME` | Habitel Hotels | Habitel Prime |

`LEMCO SAS` **no** se homologa en bloque como `Habitel Hotels`: solo el caso
`LEMCO SALVIO`. El resto de `LEMCO SAS` conserva la homologación que le
corresponda.

Un caso de septiembre mostraba `SELECT` en Kactus y `Habitel Prime` en el
histórico del `Consolidado 2025` (foto de julio). Por decisión funcional
prevalece la clase de nómina actual: **`SELECT` → `Habitel Select`**.

### Reparto por origen de la decisión

| Población | Lógica vigente del Consolidado | Reglas especiales | Homologación validada | Sin resolver |
|---|---:|---:|---:|---:|
| INGRESOS (128) | 98 | 28 | 2 | **0** |
| RETIROS (102) | 74 | 25 | 3 | **0** |

Los registros resueltos por «homologación validada» son personas que ingresaron
y se retiraron dentro del mismo mes, por lo que no figuran en el
`Consolidado 2025` (una fotografía de planta activa, no una fuente de eventos).
Sus orígenes tienen destino único en todo el histórico de la hoja.

Toda empresa resultante existe en `Empresas.tmdl` con el grupo que declara
`Grupo Empresarial.tmdl`, y toda combinación tiene precedente en la propia hoja.

## 6. `EDAD` y `Grupo_Edad` en RETIROS

Las fórmulas de ambas columnas usaban una fecha de corte fija heredada,
`DATE(2026,7,31)`, también en las filas de agosto y septiembre. Regla aprobada y
aplicada:

| Periodo | Fecha de corte |
|---|---|
| retiros de agosto 2026 | `DATE(2026,8,31)` |
| retiros de septiembre 2026 | `DATE(2026,9,30)` |

Resultado:

- agosto: **94 filas** actualizadas al 31/08/2026;
- septiembre: **102/102** con corte 30/09/2026;
- **ninguna fila** de agosto o septiembre que tenga estas fórmulas conserva
  `DATE(2026,7,31)`.

Se conservó íntegra la lógica de ambas fórmulas: solo cambió la fecha de corte,
y no se sustituyó ninguna fórmula por un valor.

### Las 19 filas manuales de agosto

19 filas de agosto —las del delta `Ago II` → `Ago III`, cargadas manualmente—
**nunca tuvieron fórmula** en `EDAD` ni en `Grupo_Edad`, y tampoco tienen fecha
de nacimiento. No se corrigieron en este cierre: agregarles la fórmula las
llevaría de «sin dato» a «edad 0» por el `IFERROR` de la propia fórmula. Queda
como deuda menor, a resolver preferentemente después de completar sus fechas de
nacimiento.

## 7. Pendiente no bloqueante: fechas de nacimiento

De los 102 retiros de septiembre, **92 obtuvieron `FECHA NACIMIENTO`** desde el
`Consolidado 2025` por identificación, y **10 quedaron en `#N/A`** por no existir
allí.

- Se escribieron como valor de error estático, igual que las filas históricas que
  ya presentan `#N/A` en esa columna.
- **No se inventó ninguna fecha ni se consultó otra fuente.**
- El usuario completará esos 10 casos manualmente cuando Kactus vuelva a estar
  disponible.

**Este pendiente no bloquea el cierre de la implementación.** Las fórmulas
dependientes (`EDAD`, `Grupo_Edad`) propagan su comportamiento normal para esos
registros.

## 8. Deuda técnica: el validador vigente

`Scripts/headcount/validar_ingresos_retiros.py` resuelve la población de origen
**a partir de las hojas mensuales del consolidador**, con un patrón atado al
sufijo del nombre de hoja:

- INGRESOS: `^\s*<mes>\s*,\s*A\s*$`
- RETIROS: `^\s*<mes>\s*(?:II|,\s*I)\s*$`

Por eso **no representa la metodología validada en este cierre**:

- en agosto resuelve `Ago II` (94) en vez de la población real (113);
- en julio resuelve `jul, I` (126) en vez de `jul, II` (146);
- para septiembre no encuentra hoja alguna, porque esas exportaciones no se
  generaron.

### Migración futura requerida

- Derivar INGRESOS y RETIROS directamente de `Fact_Contrataciones`, con las
  reglas de la sección 3.
- Conciliar por clave de evento: `Identificación + Fecha Inicio` para INGRESOS y
  `Identificación + Fecha Vencimiento` para RETIROS.
- Hasta entonces, **el validador no debe usarse como autoridad única** para
  declarar un cierre mensual.

Registrado en `Specs/00_roadmap_y_backlog.md` como `DATA-016`. No se refactorizó
en este cierre: requiere su propio análisis de impacto, plan y pruebas.

## 9. Incidente operativo y procedimiento seguro

Durante la actualización se comprobó que **AutoSave de OneDrive puede persistir
cambios aunque Excel se cierre con `SaveChanges=False`**. Dos intentos fallidos
—ambos abortados por errores de tipo de dato antes de cualquier `Save()`—
dejaron filas parcialmente escritas en el archivo vivo.

Los dos casos se **detectaron comparando el SHA-256 del archivo contra el
respaldo** y se **restauraron desde respaldos verificados**, sin pérdida de
información. El estado parcial descartado se conservó fuera de Git como
evidencia.

### Procedimiento seguro resultante

Patrón recomendado para toda actualización futura de `PptovsReal.xlsx`:

1. respaldo previo del archivo, verificando **SHA-256** origen = copia;
2. **construir y validar todos los datos en memoria antes de abrir Excel**, de
   modo que ningún error de datos pueda dejar el libro a medias;
3. trabajar sobre una **copia temporal fuera de OneDrive**, donde AutoSave no
   interviene;
4. escribir exclusivamente con **Excel Desktop / COM**, nunca con `openpyxl`,
   que destruye tablas, dinámicas, formatos y fórmulas estructuradas;
5. validar la copia por completo: conteos, conciliación por clave de evento,
   fórmulas presentes, columnas no intervenidas intactas;
6. **promover la copia al archivo oficial solo después del PASS**;
7. verificar SHA-256 copia = destino y reabrir el libro para confirmar.

Aprendizaje adicional: en libros sin tabla estructurada, el patrón de fórmulas
debe tomarse de una **fila completa y representativa**, nunca de «la última fila
física». En `RETIROS` el orden no es cronológico: las últimas filas de la hoja
pertenecen a julio y presentan fórmulas incompletas.

## 10. Controles ejecutados

Para los dos periodos y las dos poblaciones:

- conciliación contra `Fact_Contrataciones` por clave de evento: **0 faltantes,
  0 adicionales, 0 duplicados**;
- columnas calculadas completas: 12/12 en `INGRESOS`, 9/9 en las filas nuevas de
  `RETIROS`;
- **0 celdas vacías** en `Grupo empresarial`, `Empresa`, `Dependencia`, `Área`,
  `Nivel`, `CARGO_CCO`, `Salario` e `Identificación_Fecha Inicio`;
- histórico no intervenido verificado por firma de contenido antes y después;
- `INGRESOS` conserva 5.549 filas y la firma de sus columnas de valor y fórmulas
  tras la carga de `RETIROS`;
- estructura del libro intacta: 7 hojas y 8 tablas dinámicas;
- sin errores de fórmula en las filas nuevas, salvo los `#N/A` intencionales de
  `FECHA NACIMIENTO`.

> Los **valores calculados** de `INGRESOS` sí cambian al cargar `RETIROS`,
> porque `Ind_Calidad`, `última fecha de vencimiento`, `Ultimo Detalle`,
> `Validación`, `Meses reales de permanencia` y `Afecta calidad` leen esa hoja.
> Es el efecto esperado de la carga, no una alteración: se verificó que las
> columnas de valor y las fórmulas de `Tabla6` quedaron idénticas.

Observaciones heredadas que se preservaron sin cambio:

- `Ultimo Detalle` de `INGRESOS` mantiene rangos fijos hacia `RETIROS` que ya no
  cubren toda la hoja;
- los `#NUM!` de `Meses reales de permanencia` siguen apareciendo mientras un
  ingreso no tenga retiro emparejado;
- `Motivo Movimiento` y `Detalle` son campos de estado: se copian tal como están
  en Kactus, de modo que una persona ya retirada puede mostrar su motivo de
  retiro en la fila de ingreso. Es el comportamiento histórico de la hoja.

## 11. Validación de Power BI

El usuario confirma validación humana y operativa, posterior a este cierre de
fuentes:

- **Proyecto 04**: refresh realizado y publicado.
- **Proyecto 07**: refresh realizado y publicado.

No se modificó `PBIP/` en este bloque.

## 12. Privacidad

Aplica `Docs/SECURITY_AND_PRIVACY.md`. Esta spec contiene únicamente conteos,
reglas, estructura y resultados agregados.

No se versionan identificaciones, nombres, fechas de nacimiento individuales,
salarios, datos médicos, archivos Excel operativos, respaldos, temporales ni
diagnósticos con datos personales. `Data/` permanece ignorado por Git.

## 13. Pendientes

| Pendiente | Tipo | Bloquea |
|---|---|---|
| 10 fechas de nacimiento de septiembre, a completar cuando Kactus esté disponible | Datos | No |
| Modernizar el validador para derivar de `Fact_Contrataciones` (`DATA-016`) | Automatización | No |
| 19 filas manuales de agosto sin fórmula de `EDAD`/`Grupo_Edad` ni fecha de nacimiento | Datos | No |
| Rangos fijos de `Ultimo Detalle` en `INGRESOS` | Plantilla | No |

## 14. Referencias

- [Docs/ACTUALIZACION_INGRESOS_RETIROS_PPTOVSREAL.md](../Docs/ACTUALIZACION_INGRESOS_RETIROS_PPTOVSREAL.md)
- [Docs/RUNBOOK.md](../Docs/RUNBOOK.md), procedimiento mensual de `PptovsReal`
- [Specs/0033_cierre_actualizacion_headcount_septiembre_2026.md](0033_cierre_actualizacion_headcount_septiembre_2026.md)
- [Docs/SECURITY_AND_PRIVACY.md](../Docs/SECURITY_AND_PRIVACY.md)
