# Análisis de impacto — Productividad: presupuesto y ejecutado de gasto y ventas

Fecha: 2026-09-10
Estado: ANÁLISIS COMPLETO — implementación no autorizada; gate de unidad monetaria pendiente
Iniciativa: `PBIP-009`
Página: `Productividad` (`ReportSection65569958420c423d90b1`)

## 1. Objetivo y alcance

Evaluar el impacto de incorporar en `Productividad` presupuesto, ejecutado, diferencia absoluta y variación porcentual de Gasto de Personal y Ventas. Este documento no implementa DAX, visuales, relaciones, Power Query ni cambios en datos.

## 2. Estado de repositorio auditado

- Rama local: `feat/hc-validacion-ingresos-retiros-agosto-2026`.
- `HEAD`: `e73bd71896cc60c9bd8ac395fbdba084aab34cae`.
- `origin/main`: `3bc4f45fa8295dad6e0e0ab59204fdddb66c6698`.
- La rama local tiene un commit propio y está dos commits detrás de `origin/main`.
- El checkout contiene numerosos cambios concurrentes de Power BI Desktop/OneDrive y trabajo PBIP-008 ajeno.
- No existe staging activo.
- La página `Productividad`, `Planta Ppto.tmdl` y `relationships.tmdl` coinciden con `origin/main`.
- `Tbl_Medidas.tmdl` tiene cambios locales ajenos, pero las medidas de Productividad auditadas no presentan diferencias semánticas frente a `origin/main`.

Una fase futura debe usar un worktree limpio desde el `origin/main` vigente y trasladar únicamente el alcance aprobado.

## 3. Fuente, grano y calidad

### 3.1 Fuente efectiva

`Planta Ppto` importa desde SharePoint corporativo:

`Data/HeadCount/PptovsReal.xlsx` → hoja `Planta Personal`.

La consulta M promueve encabezados y tipa como moneda/decimal `Ventas (MM)`, `Gasto Personal`, `Ppto Ventas (MM)` y `Ppto Gasto Personal`. El archivo local sincronizado se inspeccionó solo en lectura.

### 3.2 Grano observado

La hoja contiene 1.072 filas, 21 columnas y 48 periodos entre 2023-01 y 2026-12.

Grano físico único:

`Ppto/Real + Año + Mes + Grupo Empresa + Empresa`

- 1.072 claves únicas y 0 duplicadas;
- 5 grupos y 12 empresas;
- 528 filas `PPTO` y 544 filas `REAL`.

Sin `Ppto/Real` aparecen 520 pares esperados `PPTO`/`REAL`. Sumar sin identificar el estado canónico puede duplicar importes.

### 3.3 Disponibilidad

| Columna | Numéricos | Blancos | Ceros explícitos | Negativos |
|---|---:|---:|---:|---:|
| `Ventas (MM)` | 206 | 866 | 0 | 0 |
| `Gasto Personal` | 273 | 798 | 0 | 0 |
| `Ppto Ventas (MM)` | 199 | 873 | 0 | 0 |
| `Ppto Gasto Personal` | 312 | 760 | 0 | 0 |

Hallazgos:

1. Los cuatro importes están poblados principalmente en filas `REAL`, incluso los presupuestos.
2. Cinco valores de `Ppto Ventas (MM)` de Challenger, enero-mayo de 2026, están poblados tanto en `PPTO` como en la fila `REAL` de la misma clave; un `SUM` sin filtro los cuenta dos veces.
3. `Gasto Personal` contiene una fórmula Excel histórica con valor calculado disponible.
4. En 2023 los cuatro importes están vacíos.
5. En 2026 la ejecución llega hasta julio; presupuestos futuros existen para varios negocios con cobertura desigual.
6. Un `BLANK` no equivale a ejecución cero.

### 3.4 Gate de unidad monetaria

Las columnas no tienen una escala homogénea a través del histórico: conviven importes con orden de magnitud compatible con pesos completos y otros ya expresados en millones, con cambios por grupo y año. Challenger conserva magnitudes de pesos completos en 2024-2026, mientras otros grupos alternan escalas entre años.

`Prod_Usar_Millones` y `GL_Usar_Millones` controlan el formato; no convierten cada fila a una unidad canónica antes de sumar. Por ello:

**las cuatro columnas no pueden sumarse directamente en una vista consolidada hasta gobernar la unidad monetaria por empresa y periodo.**

Dentro de un contexto homogéneo pueden compararse si también se aplica la regla canónica de `Ppto/Real` y se controla la cobertura.

### 3.5 Conciliación de julio 2026 contra las fuentes originales

Se contrastó `PptovsReal.xlsx` con las dos fuentes financieras de la Unidad
Hotelera para el corte de julio de 2026:

- `Data/Gasto Laboral/2026/07_Julio/2.0 Analisis Gasto Laboral U.H..xlsx`
- `Data/Gasto Laboral/2026/07_Julio/Gasto laboral empresas_Julio2026.xlsx`

**Fuente híbrida por indicador.** `Planta Ppto` no es una única fuente
homogénea: la planta proviene del consolidado de personal, mientras los cuatro
importes financieros provienen del circuito contable de Gasto Laboral. Ambos
conviven en la misma fila sin que el modelo lo declare. La consecuencia práctica
es que un indicador que mezcle planta e importes está cruzando dos linajes
distintos y hay que decirlo explícitamente.

**Prime + Select se consolidan como `Habitel Nómina Compartida`.** En
`Planta Personal` el gasto de la unidad hotelera Habitel se carga íntegramente
contra la empresa `Habitel Nómina Compartida`, mientras `Habitel Prime` y
`Habitel Select` conservan su planta con los importes financieros en blanco. Es
un criterio de consolidación, no un vacío de datos.

Implicación directa para PBIP-009: **cualquier vista de Productividad filtrada a
`Habitel Prime` o `Habitel Select` mostrará presupuesto y ejecutado en blanco**,
aunque esas empresas sí tengan planta. La tabla debe interpretarse a nivel de
Grupo Empresa o de `Habitel Nómina Compartida`, y esa limitación debe quedar
visible para el usuario final.

**Conversión COP → MM demostrada para Habitel.** Para el corte de julio de 2026,
las ventas ejecutadas y el presupuesto de ventas de Habitel concilian con las
fuentes originales tras convertir de pesos completos a millones. La demostración
es específica de ese grupo y ese corte: **no se generaliza a los demás grupos ni
a otros años**, y no sustituye el gate de unidad monetaria de la sección 3.4.

**Truncamiento observado.** Los importes de `Planta Personal` conservan decimales
en enero y febrero de 2026 y desde marzo se almacenan redondeados a millones
enteros. La pérdida es inferior a un millón por fila, suficiente para que la
conciliación exacta contra el origen contable no cierre al peso. Cualquier
control de igualdad debe usar tolerancia, no comparación estricta.

**Convención financiera en filas `Real`.** La conciliación confirma lo anticipado
en la sección 3.3: los importes financieros operativos —incluidos los
presupuestos— viven en las filas `Ppto/Real = "Real"`. Filtrar los presupuestos a
ese estado evita el doble conteo de los cinco presupuestos de ventas que
aparecen en ambos estados y reproduce el corte de julio de Habitel.

**`Ppto Gasto Personal` sin linaje demostrado.** A diferencia de las ventas y del
gasto ejecutado, **no se logró demostrar de qué fuente proviene el presupuesto de
gasto de personal**. Concilia en orden de magnitud, pero no se identificó el
archivo ni el proceso que lo alimenta. Se mantiene como fuente operativa vigente
y **no debe automatizarse su carga** hasta demostrar el origen.

Consecuencia: la tabla de Productividad publicará una columna de presupuesto de
gasto cuyo linaje no está probado. Es aceptable como continuidad operativa, pero
debe declararse como tal.

**Gasto U.H. total frente a TH «sin outsourcing».** El gasto ejecutado
almacenado en `PptovsReal` concilia aproximadamente con el archivo de Talento
Humano en su variante «sin outsourcing», no con el gasto total de la Unidad
Hotelera. La diferencia corresponde al gasto de personal temporal. Dos lecturas
legítimas del mismo mes conviven según se incluya o no el outsourcing, y la
tabla de Productividad refleja la primera.

> **Decisión aprobada el 2026-09-10.** Se conserva el gasto «sin outsourcing» como
> definición vigente de `Gasto Personal` para Productividad. Ver §12, decisión 8.

**Ninguna de estas conclusiones autoriza modificar `PptovsReal.xlsx` ni las
fuentes Excel dentro de PBIP-009.**


### 3.6 Matriz de unidades demostrada y normalización aprobada (2026-09-10)

**Decisión aprobada:** la unidad canónica de PBIP-009 es **MM COP**, y la
conversión ocurre **antes de agregar**.

La escala almacenada **no depende solo del grupo: depende del grupo y del año**, y
cambió dos veces en tres ejercicios. Matriz demostrada sobre filas `Ppto/Real = "Real"`:

| Grupo Empresa | 2024 | 2025 | 2026 |
|---|---|---|---|
| Challenger | COP | COP | **COP** |
| Fundación Challenger | MM | COP | **MM** |
| Grupo Sky | MM | COP | **MM** |
| Habitel Hotels | COP | COP | **MM** |
| Lemco | COP | COP | **MM** |

**Evidencia, sin inferir por el tamaño del número:**

1. **Gasto por colaborador** (`Gasto Personal / Total`), independiente de la
   magnitud: da ~5.000.000 en Challenger 2026 —lectura en COP— y entre 5 y 11 en
   los demás grupos —lectura en MM—. Ningún resultado quedó indeterminado.
2. **Ratio Gasto/Ventas dentro de la misma fila**: coherente entre 0,07 y 0,44 en
   los cuatro grupos con operación comercial, lo que confirma que las cuatro
   columnas comparten unidad dentro de la fila. Un desajuste entre columnas
   habría producido un ratio del orden de 10⁶.
3. **Ratio Ppto/Real del gasto**: entre 0,94 y 2,07 en las quince combinaciones;
   ningún salto de escala entre presupuesto y ejecutado.
4. **Conciliación de julio 2026** ya registrada en §3.5.
5. **Lógica de `Prod_Usar_Millones`**: aplica el divisor de millones solo cuando
   Challenger está solo o cuando están todos los grupos, lo que corrobora que
   Challenger es el que está en COP.

**Uniformidad**: cero combinaciones Grupo × Año con mezcla interna entre empresas,
de modo que la clave de normalización es Grupo Empresa × Año y no requiere bajar
a empresa.

**Fundación Challenger** presenta un ratio Gasto/Ventas de 3,4 en 2026. Se
verificó que **no es un desajuste de escala** sino una característica del negocio:
gasto y ventas están en el mismo orden de magnitud (decenas de MM).

**Combinaciones sin evidencia.** 2023 no tiene importes y **2027 en adelante no
tiene ninguna evidencia disponible**. Dado que el patrón cambió en 2025 y volvió a
cambiar en 2026, **no es extrapolable**. La normalización devuelve `BLANK` fuera
de las quince combinaciones demostradas: es preferible una tabla vacía a una
cifra silenciosamente equivocada.

**Riesgo R1 — parcialmente resuelto.** El consolidado «Todos» ya es
matemáticamente válido para 2024-2026. Permanece abierto para ejercicios futuros
mientras la unidad no se gobierne en el contrato de datos.

**Limitación resuelta el 2026-09-10.** `Efic` y `%Efiprom` leen las columnas
crudas sin normalizar y, en la vista «Todos», arrastraban el mismo problema de
unidades mixtas. La decisión aprobada no las modifica —siguen sirviendo al resto
del modelo— sino que crea ratios normalizados propios de PBIP-009. Ver §3.7.



### 3.7 Ratios Gasto/Ventas normalizados (decisión aprobada 2026-09-10)

**Decisión humana.** Crear ratios Gasto/Ventas normalizados exclusivos de
PBIP-009 y usarlos en los visuales de la página Productividad que representan ese
concepto, manteniendo `Efic` y `%Efiprom` intactas para el resto del modelo.

El motivo es que un ratio es seguro solo si numerador y denominador comparten
unidad. Dentro de un grupo-año eso se cumple siempre, así que `Efic` y `%Efiprom`
eran correctas en las vistas segmentadas. Dejaban de serlo al consolidar varios
grupos con escalas distintas, porque la suma cruda del numerador y la del
denominador ya no eran comparables entre sí.

**Medidas creadas.** Ambas en `Tbl_Medidas`, carpeta
`05 Productividad\PBIP-009\Normalizacion`, formato `0.0%;-0.0%;0.0%`:

| Medida | Definición | Concepto |
|---|---|---|
| `Prod_Ratio_Gasto_Ventas_Ppto` | `DIVIDE([Prod_Ppto_Gasto_MM], [Prod_Ppto_Ventas_MM])` | Gasto/Ventas presupuestado |
| `Prod_Ratio_Gasto_Ventas_Real` | `DIVIDE([Prod_Gasto_MM], [Prod_Ventas_MM])` | Gasto/Ventas ejecutado |

Ambas devuelven `BLANK` si falta cualquiera de los dos importes o si el
denominador es cero, y se recalculan siempre desde importes agregados: nunca
suman ni promedian porcentajes.

**Coherencia de toda la página.** Los cuatro visuales visibles que representan
este concepto se reconectaron a las medidas nuevas, para que tabla, gráficos y
tarjeta muestren el mismo resultado bajo el mismo contexto de filtros:

| Visual | Tipo | Rol |
|---|---|---|
| `cba349945ec4b0577321` | tabla | columnas `Gasto/Ventas Ppto.` y `Gasto/Ventas Real` |
| `9bcb53c0b346ba0d28c4` | tabla | tarjeta «Gasto vs Venta Presupuestado / Ejecutado» |
| `76fbb82301d3f6b571c3` | combo | «Gasto Laboral Vs Ventas» por año |
| `d6010674e3a075647581` | combo | gasto laboral por mes |

**Efecto colateral que debe conocerse.** Las medidas nuevas heredan de la capa MM
el filtro `KEEPFILTERS('Planta Ppto'[Ppto/Real] = "Real")`, la fila financiera
canónica de §3.1. `Efic` y `%Efiprom` no aplicaban ese filtro. Por tanto, en los
tres visuales distintos de la tabla el cambio no es solo de unidades: también
alinea la base de filas con la de la tabla. Eso es lo que persigue el requisito de
coherencia, pero significa que sus cifras pueden moverse respecto a lo que
mostraban antes, y ese movimiento es esperado, no una regresión.

**Validación numérica sobre el dato real.** Consolidado «Todos», enero 2026:

| Concepto | Valor |
|---|---|
| Ppto Gasto | 13.734 MM |
| Gasto Real | 12.114 MM |
| Ppto Ventas | 90.375 MM |
| Ventas Reales | 90.377 MM |
| **Gasto/Ventas Ppto.** | **15,2 %** |
| **Gasto/Ventas Real** | **13,4 %** |

El consolidado equivale exactamente a la suma de los cinco grupos en los cuatro
importes. La prueba de no aditividad confirma que el ratio se recalcula y no se
suma: el ratio del consolidado es 0,1520 frente a 1,3359 que daría la suma de los
ratios por grupo.

**Combinaciones sin factor demostrado.** El dato contiene además filas de **2023**
en los cinco grupos. Están íntegramente en cero en los cuatro importes —son filas
solo de headcount—, de modo que la ausencia de factor para 2023 no oculta ninguna
cifra: la capa devuelve `BLANK` donde antes habría un cero.

**Vacío real del dato, no defecto.** Lemco 2024 no tiene ventas presupuestadas
—cero en todas sus filas—, por lo que `Gasto/Ventas Ppto.` devuelve `BLANK` en esa
combinación. Es un vacío de la fuente y debe reportarse como tal, no corregirse en
el modelo.


### 3.8 Período comparable y formato de brechas (decisión aprobada 2026-09-11)

**Decisión humana.** Presupuesto y ejecución se comparan usando exactamente el
mismo período. En vistas de año completo o acumuladas, presupuesto y real se
limitan al corte efectivo de ejecución; con meses seleccionados se respeta la
selección, pero el agregado usa solo meses comparables. Un mes futuro sin
ejecución no genera una falsa brecha desfavorable.

**Reutilización evaluada antes de crear lógica nueva.** La página no tiene un
corte gobernado. `Subtitulo_Productividad_Comparativo_Acumulado` solo describe los
meses seleccionados en texto; `Titulo_Productividad_Gasto_Laboral` solo el año; los
filtros de visual sobre `Años[Año]` no tienen condición; y `PBIP008 Fecha Corte`
pertenece a la rotación (`'Rotacion Proyectada'[FechaCorte]`), no a la ejecución
financiera. Por eso se crearon medidas PBIP-009 específicas.

**Por qué el corte es por métrica y no único.** El dato del 2026-09-11 muestra que
gasto y ventas tienen cobertura independiente: en 2025 las ventas faltan en
presupuesto **y** real desde julio o agosto para Fundación Challenger, Grupo Sky,
Habitel Hotels y Lemco, mientras el gasto está completo los doce meses. Un corte
que exigiera gasto y ventas a la vez habría recortado gasto perfectamente
comparable y reescrito el histórico de 2025. La regla aplicada es:

| Medida | Ventana cuando hay varios meses en contexto |
|---|---|
| Gasto Ppto. y Gasto Real | meses ≤ `Prod_Mes_Corte_Gasto` (último mes con gasto real) |
| Ventas Ppto. y Ventas Reales | meses ≤ `Prod_Mes_Corte_Ventas` (último mes con ventas reales) |
| Gasto/Ventas Ppto. y Gasto/Ventas Real | meses ≤ `Prod_Mes_Corte_Ratio` (el menor de ambos), para que numerador y denominador cubran los mismos meses |

El corte se calcula por Grupo Empresa × Año —el mismo grano en que ya itera la
capa MM—, ignora la selección de meses y respeta Grupo, Empresa y Año. Con **un
solo mes** en contexto cada medida devuelve su valor normal. Brechas y
variaciones heredan el período sin cambiar su DAX, y los totales se recalculan
desde los importes del período comparable. Las tres medidas de corte están
ocultas en `05 Productividad\PBIP-009\Periodo`.

**Cortes resultantes (gasto / ventas / ratio):**

| Año | Challenger | Fundación Challenger | Grupo Sky | Habitel Hotels | Lemco |
|---|---|---|---|---|---|
| 2024 | 12 / 12 / 12 | 12 / 12 / 12 | 12 / 12 / 12 | 12 / 12 / 12 | 12 / 12 / 12 |
| 2025 | 12 / 12 / 12 | 12 / 7 / 7 | 11 / 5 / 5 | 12 / 7 / 7 | 12 / 7 / 7 |
| 2026 | 7 / 6 / 6 | 7 / 7 / 7 | 7 / 7 / 7 | 7 / 7 / 7 | 7 / 7 / 7 |

**Formato definitivo de brechas.** `Prod_Diferencia_Gasto_Tabla` y
`Prod_Diferencia_Ventas_Tabla` pierden el `formatStringDefinition` basado en
`Prod_Usar_Millones`, cuyas `,,` volvían a dividir por un millón valores que ya
estaban en MM y producían `-$ 0 mill.` en «Todos». Usan ahora el mismo formato
fijo que las cuatro bases: `$ #,0 "mill."`. Su DAX no cambió.

**Resultado de las pruebas** (simulación de la semántica DAX sobre una copia de
solo lectura de `PptovsReal.xlsx` del 2026-09-11):

Los controles de un mes no cambian, verificado por aserción:

| Control | Ppto Gasto | Gasto Real | Ppto Ventas | Ventas Reales | G/V Ppto. | G/V Real |
|---|---:|---:|---:|---:|---:|---:|
| Todos, enero 2026 | 13.734 | 12.114 | 90.375 | 90.377 | 15,2 % | 13,4 % |
| Challenger, enero 2026 | 9.605 | 8.687 | 74.151 | 76.518 | 13,0 % | 11,4 % |
| Habitel Hotels, julio 2026 | 1.945 | 1.857 | 7.391 | 5.933 | 26,3 % | 31,3 % |

Efecto en los totales multi-mes de «Todos» (MM COP):

| Vista | Brecha Gasto antes | Brecha Gasto después | G/V Ppto. antes → después |
|---|---:|---:|---:|
| 2026 año completo | −66.531 (−41,3 %) | −986 (−1,0 %) | 24,6 % → 13,1 % |
| 2026 ene–jun (vista por defecto) | −1.576 (−1,9 %) | sin cambio | 13,0 % sin cambio |
| 2026 jun–sep | −25.353 (−47,9 %) | +535 (+2,0 %) | 38,4 % → 12,6 % |
| 2026 ago–dic (solo futuro) | presupuesto 65.545 sin real | todo `BLANK` | — |
| 2025 año completo | −3.535 (−2,3 %) | −2.379 (−1,6 %) | 15,3 % → 13,8 % |
| 2024 año completo | sin cambio | sin cambio | sin cambio |

En 2025 el único cambio de importes es diciembre de Grupo Sky, que tenía
presupuesto de gasto sin gasto real. La identidad consolidado = suma de grupos se
cumple en los seis escenarios, y la variación del total se recalcula: −1,0 % en
2026 frente a −44,3 % que daría sumar las variaciones por grupo.

**Residuos que el corte por ejecución no corrige.** Son huecos de presupuesto
dentro de meses ya ejecutados, no presupuesto futuro:

- **Lemco, julio 2026**: gasto real sin presupuesto de gasto. En 2026 año
  completo, la brecha de gasto de Lemco (+1.112 MM) incluye 1.052 MM de julio sin
  presupuesto; sin esa celda, la brecha de «Todos» sería de unos −2.038 MM en
  lugar de −986 MM.
- **Lemco, 2024**: ventas reales (39.712 MM) sin presupuesto de ventas en todo el
  año. La brecha de ventas 2024 de «Todos» incluye esas ventas sin contrapartida.

Corregirlos exige completar la fuente o ampliar la regla a emparejamiento por
celda; ambas opciones requieren decisión humana.

**Lo que no cambió.** La capa MM, `Efic`, `%Efiprom`, `KPI_EFI`, `Var_GL`,
`Cump_GL`, `Prod_Usar_Millones` y los títulos de la página. La tarjeta KPI
(`KPI_EFI`, `Var_GL`) y el subtítulo del acumulado no adoptan el período
comparable porque dependen de medidas históricas compartidas.

## 4. Medidas existentes y reutilización

| Medida | DAX/dependencia actual | Visuales consumidores | Decisión |
|---|---|---|---|
| `Efic` | `SUM(Gasto Personal) / SUM(Ventas (MM))` | `76f...`, `9bcb...`, `d601...` | Preservar; es una razón, no un importe. Usa `/` y no controla cero. |
| `%Efiprom` | `SUM(Ppto Gasto Personal) / SUM(Ppto Ventas (MM))` | `76f...`, `9bcb...`, `d601...` | Preservar como baseline; no sustituye los presupuestos y hereda el riesgo de cinco filas. |
| `KPI_EFI` | compara `[Efic] > [%Efiprom]` | tarjeta `285f...` | Preservar. |
| `Var_GL` | `[Efic] / [%Efiprom]` | tarjeta `285f...` | No equivale a variación presupuesto-ejecutado. |
| `Cump_GL` | gasto real / presupuesto de gasto | Gasto Laboral | No equivale a la variación requerida. |
| `GL_Ppto_Gasto_Personal` | suma presupuesto de gasto; formato dinámico | tabla Gasto Laboral | Referencia reutilizable solo tras resolver unidad/estado; no modificar por riesgo transversal. |
| `GL_Gasto_Personal` | suma gasto ejecutado; formato dinámico | tabla Gasto Laboral | Misma consideración. |
| `GL_Usar_Millones` | decide formato Challenger/consolidado vs otros | auxiliar | Reutilizar criterio de presentación, no como conversión. |
| `GL_*_Visual_Challenger/Otros` | alternan series de dos gráficos | Gasto Laboral | No usar en nuevos KPIs de Productividad. |
| `Prod_Gasto_Personal` | `SUM(Gasto Personal)` | base de tabla Productividad | Reutilizable en contexto homogéneo. |
| `Prod_Ingreso_Operacional` | `SUM(Ventas (MM))` | base de tabla Productividad | Reutilizable en contexto homogéneo. |
| `Prod_Usar_Millones` | decide formato por negocio | auxiliares | Reutilizar para formato, no normalización. |
| `Prod_Gasto_Personal_Tabla` | base con formato dinámico | `cba...` | Preservar. |
| `Prod_Ingreso_Operacional_Tabla` | base con formato dinámico | `cba...` | Preservar. |
| `Prod_Efic_Tabla` | `[Efic]` | `cba...` | Preservar. |
| `Titulo_Productividad_Gasto_Laboral` | título por año | `d601...` | Preservar. |
| `Subtitulo_Productividad_Comparativo_Acumulado` | texto por meses | `76f...` | Preservar. |

No existe medida explícita y segura para presupuesto de ventas ni medidas de diferencia absoluta/porcentual de ambos dominios.

## 5. Relaciones y filtros

| Hecho | Dimensión | Estado |
|---|---|---|
| `Planta Ppto[Empresa]` | `Empresas[Empresas]` | activa, muchos-a-uno, filtro simple por defecto |
| `Planta Ppto[Año]` | `Años[Año]` | activa, muchos-a-uno, filtro simple por defecto |
| `Planta Ppto[Mes]` | `Mes[Meses]` | activa, muchos-a-uno, filtro simple por defecto |
| `Planta Ppto[IndexAnioMes]` | `DimPeriodoYM[IndexAnioMes]` | activa, muchos-a-uno, filtro simple por defecto |

El grupo se propaga mediante `Grupo Empresarial → Empresas[Grupo Empresa] → Empresas[Empresas] → Planta Ppto[Empresa]`. La página usa `Años[Año]`, `Mes[Meses]`, `Empresas[Grupo Empresa]` y `Empresas[Empresas]`. No se observaron relaciones bidireccionales ni muchos-a-muchos en este recorrido.

Los nuevos visuales deben heredar esas dimensiones; no deben crear relaciones ni usar `Planta Ppto[Grupo Empresa]` como slicer.

## 6. Semántica de diferencias

La misma fórmula es correcta para ambos dominios:

- diferencia absoluta = ejecutado − presupuesto;
- variación % = `(ejecutado − presupuesto) / presupuesto`.

No debe invertirse el signo de gasto. La interpretación se resuelve visualmente:

- Gasto positivo: desfavorable/sobre-ejecución.
- Ventas positivo: favorable/superación del presupuesto.

## 7. Propuesta técnica condicionada

### 7.1 Base canónica

Antes de implementar, las cuatro magnitudes deben expresarse en una unidad común. Se recomienda millones de COP para Productividad, con regla gobernada por empresa y vigencia; nunca inferida por magnitud. La opción preferida es normalizar en el contrato de datos. Una tabla de factores por empresa/periodo solo es aceptable si negocio aprueba su mantenimiento.

Una vez disponibles `[Prod Gasto Presupuesto MM]`, `[Prod Gasto Ejecutado MM]`, `[Prod Ventas Presupuesto MM]` y `[Prod Ventas Ejecutadas MM]`, se proponen:

```DAX
Prod Diferencia Gasto MM =
VAR _Ejecutado = [Prod Gasto Ejecutado MM]
VAR _Presupuesto = [Prod Gasto Presupuesto MM]
RETURN
    IF ( ISBLANK ( _Ejecutado ) || ISBLANK ( _Presupuesto ), BLANK (), _Ejecutado - _Presupuesto )
```

```DAX
Prod Variación Gasto % =
VAR _Presupuesto = [Prod Gasto Presupuesto MM]
RETURN
    IF ( ISBLANK ( _Presupuesto ) || _Presupuesto = 0, BLANK (), DIVIDE ( [Prod Diferencia Gasto MM], _Presupuesto ) )
```

```DAX
Prod Diferencia Ventas MM =
VAR _Ejecutado = [Prod Ventas Ejecutadas MM]
VAR _Presupuesto = [Prod Ventas Presupuesto MM]
RETURN
    IF ( ISBLANK ( _Ejecutado ) || ISBLANK ( _Presupuesto ), BLANK (), _Ejecutado - _Presupuesto )
```

```DAX
Prod Variación Ventas % =
VAR _Presupuesto = [Prod Ventas Presupuesto MM]
RETURN
    IF ( ISBLANK ( _Presupuesto ) || _Presupuesto = 0, BLANK (), DIVIDE ( [Prod Diferencia Ventas MM], _Presupuesto ) )
```

Las medidas base deben aplicar conversión gobernada, filtro canónico de estado con `KEEPFILTERS`, y agregación de importes. Nunca se suman porcentajes.

No se propone DAX de conversión hasta que exista la regla de escalas aprobada; inferirla sería frágil y no auditable.

### 7.2 Blancos, ceros y formato

- Presupuesto o ejecutado `BLANK`: diferencia y variación `BLANK`.
- Presupuesto cero explícito: diferencia válida; variación `BLANK`.
- Ejecutado cero explícito: diferencia `-presupuesto`; variación `-100 %`.
- Importes: `$ #,0.0 "MM"` tras normalización.
- Variación: `0.0 %;-0.0 %;0.0 %`.
- No usar `FORMAT()` sobre medidas numéricas.

## 8. Página Productividad

La página mide 1350×900 y contiene 12 visuales.

| ID | Tipo | Función |
|---|---|---|
| `218c...` | slicer | Año |
| `28f...` | slicer | Mes |
| `4f44...` | slicer | Grupo Empresa |
| `3dd...` | slicer | Empresa |
| `d601...` | combo | Efic vs presupuesto por mes |
| `76fb...` | combo | comparación acumulada por año |
| `cba...` | tabla | gasto, ingreso y eficiencia por mes |
| `9bcb...` | tabla | `Efic` y `%Efiprom` |
| `285f...` | tarjeta | `KPI_EFI`/`Var_GL` |
| restantes | forma/navegación | estructura |

No hay interacciones personalizadas de página. Hay filtros persistidos en slicers/visuales, pero ningún bookmark referencia la página ni sus visuales.

### Alternativa 1 — recomendada

Dos bloques KPI compactos apilados en el espacio inferior derecho:

- `Gasto de Personal`: Presupuesto | Ejecutado | Diferencia | Variación %.
- `Ventas`: Presupuesto | Ejecutado | Diferencia | Variación %.

Cada bloque sería una tarjeta multivalor o matriz de una fila. Mantiene intactos los gráficos y la tabla actuales y evita ocho tarjetas independientes.

### Alternativa 2

Ampliar `cba...` con presupuesto y variaciones por mes, y reservar dos tarjetas para síntesis anual. Aporta detalle, pero aumenta ancho, desplazamiento y carga cognitiva.

## 9. Riesgos y controles

| Nivel | Riesgo | Control |
|---|---|---|
| Crítico | suma consolidada con escalas mixtas | contrato de unidad y normalización previa |
| Alto | cinco presupuestos de ventas contados dos veces | estado canónico con `KEEPFILTERS` y conciliación |
| Alto | meses futuros tratados como ejecución cero | preservar `BLANK` |
| Alto | regresión en `Efic`/`%Efiprom` | capa nueva y pruebas antes/después |
| Medio | cobertura desigual por grupo/año | matriz de completitud y mensaje sin dato |
| Medio | suma de porcentajes | recalcular desde importes agregados |
| Medio | filtros no propagados | dimensiones existentes y pruebas cruzadas |
| Medio | formato confundido con conversión | separar valor canónico y formato |
| Medio | filtros persistidos | prueba visual por contexto |
| Medio | churn/concurrencia | worktree limpio y diff estricto |

## 10. Matriz mínima de pruebas

En cada escenario se concilian los ocho resultados y se verifica que `Efic` y `%Efiprom` no cambian.

| Escenario | Foco adicional |
|---|---|
| Año 2026 | ejecución solo donde exista; futuros sin falsos ceros |
| Mes individual | diferencias y porcentajes exactos |
| Varios meses | suma de importes y razón recalculada |
| Consolidado | unidad común demostrada |
| Challenger | conversión de pesos a MM y polaridad |
| Fundación Challenger | cobertura parcial y `BLANK` |
| Grupo Sky | vigencia de escala por año/empresa |
| Habitel Hotels | cambio histórico de escala |
| Lemco | presupuesto faltante sin variación artificial |
| Empresa individual | coherencia empresa/grupo/periodo |

También deben probarse presupuesto cero/`BLANK`, ejecutado cero/`BLANK`, suma consolidada contra grupos, cero duplicados lógicos y ausencia de cambios en otras páginas.

## 11. Archivos probables de una implementación futura

Mínimo:

- `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl`;
- uno o dos `visual.json` nuevos bajo la página Productividad;
- pruebas estáticas específicas;
- plan de implementación posterior, solo con autorización.

Condicionado al gate de unidad: contrato/fuente de escalas y, eventualmente, `Planta Ppto.tmdl` si la normalización se resuelve en Power Query.

No deberían tocarse `relationships.tmdl`, otras páginas, `pages.json`, bookmarks, tema global, medidas históricas `Efic`/`%Efiprom`/`KPI_EFI`/`Var_GL`/`Cump_GL`, ni `PptovsReal.xlsx` sin requerimiento separado.

## 12. Decisiones requeridas

1. Definir unidad canónica y regla de conversión por empresa/vigencia.
2. Confirmar que los cinco presupuestos de ventas duplicados se cuentan una vez y que la fila `REAL` es canónica según el patrón actual.
3. Aprobar que ausencia de ejecutado o presupuesto produzca `BLANK`.
4. Aprobar la Alternativa visual 1 y la polaridad: gasto positivo desfavorable; ventas positivo favorable.
5. Decidir si se corrige después el mismo riesgo en `%Efiprom`; incluirlo ahora ampliaría el impacto y exigiría regresión propia.
6. Aceptar o rechazar que se publique `Ppto Gasto Personal` sin linaje demostrado, declarándolo como continuidad operativa y sin automatizar su carga.
7. Confirmar cómo se comunica al usuario que `Habitel Prime` y `Habitel Select` no tienen importes propios por consolidarse en `Habitel Nómina Compartida`.
8. **APROBADA (2026-09-10, decisión humana).** Productividad conserva como gasto ejecutado el valor vigente de `PptovsReal.xlsx`, equivalente al gasto de TH «sin outsourcing». **No se modifica la definición vigente de `Gasto Personal`** y **no se sustituye** por el gasto total de Planeación Financiera de la Unidad Hotelera. Toda evaluación del gasto total U.H. queda **fuera del alcance de PBIP-009** y exigiría una iniciativa y un análisis propios.

## 13. Conclusión

La página puede alojar el requerimiento sin relaciones nuevas y sin sustituir indicadores actuales. La aritmética propuesta es válida y la diferencia semántica se resuelve visualmente, no invirtiendo signos.

La implementación no debe comenzar todavía: la escala monetaria mixta impide una suma consolidada confiable y existe una duplicidad localizada en presupuesto de ventas. El siguiente gate es aprobar el contrato de unidad y la fila canónica; después podrá prepararse un plan de implementación controlado.
