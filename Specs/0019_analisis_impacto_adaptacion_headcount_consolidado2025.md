# Análisis de impacto — Adaptación de HeadCount a la nueva estructura de Consolidado 2025.xlsx

Fecha: 2026-08-10

Estado: análisis de impacto. **No implementado.** No modifica PBIP, Power Query, TMDL ni el archivo Excel.

Iniciativa independiente de GOV-005 (`Specs/0018`, cerrada y fusionada en `main`), de PR #7/Unión Libre (`Specs/0017`, en validación) y de Contratos Kactus (PR #4, `Specs/0015`). No comparte alcance, archivos ni rama con ninguna de ellas.

## 1. Origen del cambio manual del Excel

`Data/HeadCount/2025/Consolidado 2025.xlsx`, hoja `Consolidado2025`, fue actualizado manualmente por el usuario para incorporar nuevas columnas de estructura organizacional y datos de contrato, ampliando el esquema que consume actualmente el modelo semántico. El cambio ya está reflejado en el archivo Excel del repositorio; el modelo semántico (`PBIP/Proyecto.SemanticModel`) todavía no está adaptado a él.

## 2. Evidencia de un parche local previo (working tree principal, sin publicar)

El working tree principal (rama `docs/roadmap-backlog`) contiene, **sin commitear ni empujar**, modificaciones no aplicadas de esta iniciativa en:

- `PBIP/Proyecto.SemanticModel/definition/tables/Consolidado2025.tmdl`
- `PBIP/Proyecto.SemanticModel/definition/tables/PLANTA DE PERSONAL.tmdl`

**No se aplicó ni se modificó nada de este parche en esta Spec** — se extrajo y comparó su diff contra `origin/main` únicamente con fines de análisis.

### 2.1 Qué contiene y sigue siendo aplicable

**Fuente real actualmente consumida por `origin/main` (verificado, no asumido):** ambas consultas (`Consolidado2025` y `PLANTA DE PERSONAL`) leen hoy, en `origin/main`, desde OneDrive **personal**:

```
https://lemcosas-my.sharepoint.com/personal/edwin_clavijo_challenger_co/Documents/Documentos/...
```

**Actualización — migración a SharePoint corporativo APROBADA (decisión del usuario) y validada manualmente:** la migración de las 3 consultas que leen HeadCount (`Consolidado2025`, `PLANTA DE PERSONAL`, `AREAS`) desde OneDrive personal hacia la biblioteca corporativa `https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/Documentos%20compartidos/5.%20People%20analytics/07_Planeaci%C3%B3n_de_Personal/Data/HeadCount/{2024,2025}/...` queda **aprobada como parte del alcance de DATA-012** (ya no es una opción potencial). El usuario aplicó esta migración manualmente en Power BI Desktop, sobre un worktree temporal aislado (`.wt/data012-verificacion-fuente`, creado en blanco desde `origin/main` en `4600798`, sin ningún otro cambio), editando el paso `Origen` de las 3 consultas. Verificado por Claude Code vía `powerbi-modeling-mcp` tras el refresh que el propio usuario ejecutó en Desktop:

- Las 52 tablas del modelo, incluidas las 3 migradas, cargaron en estado `Ready`, sin errores de partición.
- `Consolidado2025` expone **68 columnas** — coincide exactamente con el Excel local (sección 3), incluidas `NIVEL_DE_CARGO` y `TIPO_DE_CARGO`.
- `PLANTA DE PERSONAL` expone 74 columnas (53 propias de 2024 + columnas aportadas por `Consolidado2025` vía `Table.Combine`), también con `NIVEL_DE_CARGO`/`TIPO_DE_CARGO` presentes.
- `AREAS` expone su única columna esperada (`AREA`), sin error.

Este cambio de origen **sigue sin estar commiteado** — vive únicamente en el worktree temporal `.wt/data012-verificacion-fuente` (no en `origin/main`, no en el working tree principal salvo lo ya indicado abajo). No se commitea ni se reaplica como parte de esta Spec (ver decisión E, sección 9.6): ese worktree mezcla la edición de rutas válida con el ruido de reserialización habitual de Desktop (bookmarks, `Tbl_Medidas.tmdl`, `diagramLayout.json`, un archivo `.dax`) y no debe tomarse como base de implementación tal cual.

**Nota sobre el working tree principal:** en él, `Consolidado2025.tmdl` y `PLANTA DE PERSONAL.tmdl` ya traían la URL corporativa desde antes (como parte del parche local original descrito en esta sección); `AREAS.tmdl` aparece ahora también modificado con la misma URL corporativa — no se determinó en esta sesión si ese cambio en `AREAS.tmdl` es intencional o un efecto colateral de una edición separada del usuario en esa copia; no se tocó ni se investigó más a fondo por estar fuera del worktree temporal usado para esta verificación.

**Conteo reconciliado de columnas del parche** (comparado contra `origin/main`, no contra el archivo Excel):

- **19 columnas genuinamente nuevas** en `Consolidado2025.tmdl` (nombre y `lineageTag` que no existían en `origin/main`): `IDMESAÑO`, `NOMBRE`, `APELLIDO`, `'NOMBRE EMPLEADO (Apellidos-nombres)'`, `'NOMBRE EMPLEADO (nombre-apellido)'`, `'MANO DE OBRA'`, `CLASIFICACION`, `FLEX`, `F_INGRESO`, `'ÁRBOL DE NÓMINA NIVEL 2'`, `'ÁRBOL DE NÓMINA NIVEL 3'`, `'Tipo Identificación'`, `'COD. CARGO'`, `'Tipo Contrato (Kactus)'`, `'Indicador Actividad'`, `'Año Nac'`, `'Generación 2'` (alias de la columna real `Generación`), `'Correo Corporativo'`, `PCD`.
- **3 columnas reposicionadas, NO nuevas** (mismo nombre y mismo `lineageTag` en el diff, solo movidas de lugar dentro del archivo): `ID_Jefe_Inmediato` (`2b961dd8-...`), `'Jefe Inmediato (nombre-apellido)'` (`9e1ed1f2-...`), `'Descripción Cargo_Jefe Inmediato'` (`39d439da-...`). Ya existían en `origin/main`; el parche solo las desplaza de posición (efecto colateral habitual de que Desktop reordene columnas según el orden de la fuente).
- **2 columnas eliminadas** del esquema anterior: `'NOMBRE EMPLEADO'` (reemplazada conceptualmente por las 2 variantes nuevas de nombre) y la columna `%` (sin uso identificado).
- **0 renombres reales** de columnas existentes en `Consolidado2025.tmdl` (`'Generación 2'` es una columna TMDL nueva que apunta a `sourceColumn: Generación`, no un renombre de una columna TMDL previa).
- En `PLANTA DE PERSONAL.tmdl` el parche agrega **22 columnas** (las mismas 19 + las 3 "reposicionadas" en `Consolidado2025`, que para esta tabla sí son genuinamente nuevas, porque `PLANTA DE PERSONAL` nunca las tuvo) para que sobrevivan el `Table.Combine`, y elimina 1 (`%`).

### 2.2 Qué quedó obsoleto o es un regresión que NO debe reaplicarse

- **Regresión de codificación en `EST_CIVIL (grupos)`**: el parche local tiene la variante `"Unión Libre"` escrita como **`"UniÃ³n Libre"` (mojibake)**, tanto en el `SWITCH` como en `GroupingDesignState`. Esto es el estado *anterior* a la corrección ya validada en PR #7 (`Specs/0017`, commit `d73aef62`/`cb6d56a`). Si este parche se reaplicara tal cual sobre el `main` actual (que ya incluye la corrección de GOV-005 pero **no** la de Unión Libre, porque PR #7 sigue sin fusionar), **revertiría silenciosamente la codificación a su forma dañada**. Cualquier implementación futura debe partir de `main` + PR #7 ya fusionado, no de este parche.
- **Lógica de `Consolidado2025` duplicada en línea dentro de `PLANTA DE PERSONAL`**: en `origin/main`, el paso `Table.Combine` de `PLANTA DE PERSONAL` referencia la consulta `Consolidado2025` como tabla (`Table.Combine({#"Tipo cambiado1", Consolidado2025})`). El parche local sustituye esa referencia por una **copia completa e independiente** de los pasos de `Consolidado2025` (`Origen2025`, `Consolidado2025_Sheet`, ..., `#"Tipo cambiado 2025"`), duplicando la lectura del mismo archivo Excel dos veces y duplicando el mismo defecto (ver sección 4) en dos lugares en vez de uno. Parece un artefacto de depuración, no una solución intencional — no debe conservarse así.
- El paso `Table.RenameColumns(..., {{"RANGO DE EDAD", "GENERACIÓN"}})` sigue presente sin cambios en ambos lugares (ver sección 4) — el parche **no resuelve** el problema reportado, solo agrega columnas alrededor de él.
- No se agregó ninguna columna `Rango de Edad` independiente al modelo — sigue pendiente (ver sección 7).

## 3. Encabezados exactos de `Consolidado2025` (lectura de solo lectura, sin PII)

68 columnas confirmadas en la hoja `Consolidado2025` (fila de encabezado, sin abrir el archivo en Excel, sin guardar cambios). Extracto de las columnas relevantes para esta iniciativa:

| # | Encabezado exacto |
|---|---|
| 9 | `ÁRBOL DE NÓMINA NIVEL 2` |
| 10 | `ÁRBOL DE NÓMINA NIVEL 3` |
| 12 | `Tipo Identificación` |
| 19 | `COD. CARGO` |
| 23 | `Tipo Contrato (Kactus)` |
| 24 | `Indicador Actividad` |
| 36 | `Año Nac` |
| 38 | `Generación` |
| 39 | `RANGO DE EDAD` |
| 52 | `NIVEL_DE_CARGO` |
| 53 | `TIPO_DE_CARGO` |

Verificado byte a byte: `NIVEL_DE_CARGO` y `TIPO_DE_CARGO` son cadenas ASCII limpias, sin espacios, mayúsculas/minúsculas o caracteres ocultos que expliquen un fallo de coincidencia de nombre. **Ambas columnas existen en el archivo Excel local del repositorio.**

No se leyó ni se muestra ninguna identificación, nombre, salario, email, teléfono ni dato personal por fila.

## 4. Causa del error `NIVEL_DE_CARGO`

`origin/main`, `Consolidado2025.tmdl` (partición propia; URL aún vigente en `origin/main` y en el working tree principal — la migración solo se aplicó, sin commitear, en el worktree temporal de verificación, sección 2.1):

```
Origen = Excel.Workbook(Web.Contents("https://lemcosas-my.sharepoint.com/personal/.../Consolidado%202025.xlsx"), null, true),
...
#"Columnas con nombre cambiado" = Table.RenameColumns(#"Encabezados promovidos",{{"RANGO DE EDAD", "GENERACIÓN"}}),
#"Tipo cambiado1" = Table.TransformColumnTypes(#"Columnas con nombre cambiado",{{"MES", type text}, {"NIVEL_DE_CARGO", type text}, {"TIPO_DE_CARGO", type text}})
```

**Confirmado con evidencia local:** el archivo Excel del repositorio (`Data/HeadCount/2025/Consolidado 2025.xlsx`) contiene `NIVEL_DE_CARGO` y `TIPO_DE_CARGO` con nombre exacto, sin caracteres ocultos.

**Evidencia histórica del error reportado por el usuario (previa a esta Spec):** al refrescar contra la fuente antigua (OneDrive personal), `Consolidado2025` producía el error de Power Query: *"No se encontró la columna 'NIVEL_DE_CARGO' de la tabla."*

**Causa CONFIRMADA (ya no es hipótesis):** la fuente remota antigua (OneDrive personal) estaba desincronizada frente a la estructura del Excel local reestructurado. Verificación directa: el usuario migró manualmente el paso `Origen` de `Consolidado2025`, `PLANTA DE PERSONAL` y `AREAS` hacia la biblioteca corporativa (`https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/...`, sección 2.1) en un worktree temporal aislado basado en `origin/main` (`.wt/data012-verificacion-fuente`, SHA `4600798`) y ejecutó el refresh en Power BI Desktop. Claude Code verificó el resultado vía `powerbi-modeling-mcp`: las 52 tablas cargaron en estado `Ready`; `Consolidado2025` expone sus 68 columnas reales, incluidas `NIVEL_DE_CARGO` y `TIPO_DE_CARGO`, sin error. **La migración de fuente por sí sola resuelve el error `NIVEL_DE_CARGO` reportado.**

**Hallazgo independiente que persiste sin cambios (no lo resuelve la migración de fuente):** el paso `Table.RenameColumns(..., {{"RANGO DE EDAD", "GENERACIÓN"}})` sigue vigente aunque la hoja 2025 ahora tiene una columna real `Generación` (posición 38) **además** de `RANGO DE EDAD` (posición 39). Verificado en el mismo refresh: el modelo migrado sigue exponiendo `GENERACIÓN` (poblada por el renombrado histórico, con bandas de edad de 2025) y, por separado, `Generación 2` (alias de la columna real `Generación`, sin usar) — confirma que la falsa equivalencia de la sección 4-bis **sigue presente** y requiere la decisión A (sección 9.1) para resolverse; la migración de fuente no la corrige por sí sola.

## 4-bis. Evidencia visual de la falsa equivalencia Generación (observada por el usuario)

En Power BI Desktop, página `Demográfico (Promedio)`, al seleccionar el visual titulado **"Generación"**, este muestra como categorías:

- Entre 18-29 Años
- Entre 30-39 Años
- Entre 40-49 Años
- Entre 50-56 Años
- Mayor de 57 Años

En vez de categorías generacionales reales (Millennials, Generación X, Centennials, Baby Boomers). La tabla/matriz generacional asociada aparece **vacía**.

**Explicación confirmada con datos (sección 6-bis):** el paso `RANGO DE EDAD → GENERACIÓN` se aplica igual a 2024 y 2025, pero el contenido real de `RANGO DE EDAD` es distinto en cada fuente — en 2024 contiene cohortes generacionales (ver sección 6-bis), en 2025 contiene bandas de edad literales. Al combinarse ambas fuentes bajo el mismo nombre `GENERACIÓN`, los registros 2025 aportan valores tipo "Entre 18-29 Años" a una columna que el resto del modelo trata como generación. La tabla `Generaciones` (dimensión) solo contiene las 4 etiquetas generacionales reales, por lo que la relación no resuelve para los registros 2025 afectados — de ahí que la tabla generacional aparezca vacía para ese contexto.

Esta es la evidencia funcional directa de la falsa equivalencia descrita en la sección 5, independiente de la hipótesis no confirmada de la sincronización con SharePoint/OneDrive (sección 4).

## 5. Generación vs. Rango de Edad — diferencia conceptual

Son dos atributos demográficos **distintos y complementarios**, no intercambiables:

- **Generación**: cohorte generacional (p. ej. Millennials, Generación X) — hoy poblada al 100 % de las 45.670 filas de `Consolidado2025` mediante la columna real `Generación`.
- **Rango de Edad**: bandas etarias — poblada solo en 17.674 de 45.670 filas (~39 %) en la fuente 2025 actual; es un atributo independiente, no una fuente para derivar Generación.

La lógica histórica (`Table.RenameColumns(..., {{"RANGO DE EDAD","GENERACIÓN"}})`) fue, y **sigue siendo, una transformación válida para la fuente 2024** — confirmado empíricamente en la sección 6-bis mediante perfilado de solo lectura, no solo asumido. Con la columna real `Generación` disponible en 2025, esa misma sustitución deja de ser válida para esa fuente y produce la falsa equivalencia documentada en la sección 4-bis.

## 6. Comportamiento esperado 2024 vs. 2025

| | 2024 (histórico, `PLANTA DE PERSONAL`) | 2025 (`Consolidado2025`) |
|---|---|---|
| Generación | Proviene de `RANGO DE EDAD` (sustituto histórico, **confirmado válido para 2024** — sección 6-bis) — no se toca en el alcance mínimo (decisión B) | Proviene de la columna real `Generación`, normalizada a `GENERACIÓN` antes del `Table.Combine` (decisión A) |
| Rango de Edad | Nula para todo 2024 — la fuente 2024 **no tiene** una columna de rango de edad independiente de la que se usa como sustituto de Generación (confirmado, sección 6-bis); **no se inventa** un valor que la fuente nunca tuvo | Proviene de la columna real `RANGO DE EDAD` (con cobertura parcial, ~39 %), conservada como atributo independiente (decisión A) |
| `GENERACIÓN` → `GENERACI&#211;N` | Se conserva sin cambios (paso posterior al `Table.Combine`, ADR-007, no se toca en esta iniciativa) | Igual — el `Table.Combine` unifica antes de este paso, por lo que aplica a ambas fuentes por igual |
| Relación con `Generaciones[Generación]` | Se conserva sin cambios | Igual |

## 6-bis. Evidencia de perfilado 2024 (contenido real de `RANGO DE EDAD`)

Lectura de solo lectura, sin PII, de `Data/HeadCount/2024/Consolidado 2024.xlsx`, hoja `PLANTA DE PERSONAL` (40 encabezados confirmados). Hallazgos:

- **No existe ninguna columna `Generación` en la fuente 2024** — la única columna relacionada con edad/generación es `RANGO DE EDAD` (posición 22).
- **`RANGO DE EDAD` en 2024 contiene cohortes generacionales reales, no bandas de edad literales**, confirmado sobre las 25.536 filas de datos:

| Valor real de `RANGO DE EDAD` (2024) | Filas |
|---|---|
| `Millenials` | 14.450 |
| `Centennials` | 5.528 |
| `Generación X` | 5.375 |
| `Baby Boomers` | 183 |

Esto confirma con evidencia directa (no solo por inferencia) que el renombrado histórico `RANGO DE EDAD → GENERACIÓN` es semánticamente correcto para 2024 — la columna ya contiene generaciones, no bandas etarias — y que 2024 no tiene una fuente real de "Rango de Edad" (bandas de edad) independiente. Por eso el alcance mínimo (decisión B, sección 10) mantiene la lógica 2024 sin cambios y deja `Rango de Edad` nula para 2024 en vez de inventar un valor que la fuente nunca tuvo.

## 7. ÁRBOL DE NÓMINA NIVEL 2/3 vs. NIVEL_DE_CARGO/TIPO_DE_CARGO

**No existe homologación inequívoca.** Para el alcance mínimo de DATA-012, esto ya no es una decisión bloqueante: se resuelve manteniendo estas columnas en la fuente sin mapearlas (decisión C, sección 10) y difiriendo la homologación a una iniciativa futura.

Evidencia (perfilado agregado, sin PII, 45.670 filas):

- `NIVEL_DE_CARGO`: poblada al 100 %. Alimenta la columna calculada `'Tipo de Cargo'` en `PLANTA DE PERSONAL.tmdl` (`SWITCH` que agrupa `Analista`/`Analista Profesional`/`Aprendiz-Practicante`/`Base Administrativa` → *Administrativos*; `Director`/`Gerente`/`Presidente` → *Estratégicos*; `Auxiliar`/`Base Operativa`/`N/R`/`Operario`/`Operario Calificado`/`Supervisor` → *Operativos*; `Coordinador`/`Jefe` → *Tácticos*). Referenciada en 2 visuales de `Demográfico (Promedio)`.
- `ÁRBOL DE NÓMINA NIVEL 2`/`NIVEL 3`: pobladas solo en 2.572 de 45.670 filas (~5,6 %) — el mismo subconjunto exacto de filas en ambas, y coincide con el conteo de filas pobladas de `TIPO_DE_CARGO`. Sugiere que las 3 columnas se incorporaron juntas para un subconjunto reciente de registros (posiblemente ligado a la integración de Contratos Kactus — **fuera de alcance de esta Spec**, solo se deja anotado como observación).
- **Semánticamente son dimensiones distintas**: `ÁRBOL DE NÓMINA NIVEL 2` contiene valores de estructura organizacional/centro de costo (`DIRECCION MANUFACTURA`, `GERENCIA COMERCIAL`, `PRESIDENCIA`, `GERENCIA FINANCIERA`...); `NIVEL_DE_CARGO` contiene niveles de seniority/rol (`Analista`, `Director`, `Auxiliar`, `Coordinador`...). Son ejes ortogonales (departamento × nivel de cargo), no sinónimos.
- **Cruce empírico confirma la falta de correspondencia 1:1**: por ejemplo, `DIRECCION MANUFACTURA` aparece con `NIVEL_DE_CARGO` = `Base Operativa` (618 filas), `Auxiliar` (107), `Analista` (25) — un mismo valor de `ÁRBOL DE NÓMINA NIVEL 2` combina múltiples niveles de cargo.
- **Hallazgo adicional relevante**: los valores reales de `TIPO_DE_CARGO` (`Operativos`, `Administrativos`, `Tácticos`, `Estratégicos`) coinciden exactamente con las 4 categorías de salida que hoy produce la columna calculada `'Tipo de Cargo'` a partir de `NIVEL_DE_CARGO`. Esto sugiere que, una vez `TIPO_DE_CARGO` esté completamente poblado en la fuente, podría convertirse en la fuente autoritativa de esa clasificación en lugar de derivarla por `SWITCH` — pero hoy, con 94 % de filas sin dato, no puede reemplazar la lógica calculada existente.

## 8. Clasificación de las 8 columnas nuevas señaladas

| Columna | Clasificación | Justificación |
|---|---|---|
| Rango de Edad | **A — requerida** | Necesaria para separar Generación de Rango de Edad y eliminar la falsa equivalencia (secciones 5-6) |
| ÁRBOL DE NÓMINA NIVEL 2 | C — permanece en la fuente por ahora | Sin homologación inequívoca con el modelo actual; solo 5,6 % poblada; requiere decisión funcional (sección 7) |
| ÁRBOL DE NÓMINA NIVEL 3 | C — permanece en la fuente por ahora | Igual que Nivel 2 |
| Tipo Identificación | C — permanece en la fuente por ahora | Sin necesidad funcional identificada en esta sesión |
| COD. CARGO | C — permanece en la fuente por ahora | Sin necesidad funcional identificada; posible relevancia futura para homologación con Contratos Kactus (fuera de alcance) |
| Tipo Contrato (Kactus) | C — permanece en la fuente por ahora | Explícitamente ligada a la iniciativa de Contratos Kactus, fuera de alcance de esta sesión |
| Indicador Actividad | C — permanece en la fuente por ahora | Sin necesidad funcional identificada en esta sesión |
| Año Nac | C — permanece en la fuente por ahora | Redundante con `FECHA NACIMIENTO`/`EDAD` ya presentes; valor futuro como alternativa de menor exposición de PII, sin solicitud actual |

Ninguna columna se agregó automáticamente al modelo; esta clasificación es una propuesta, no una implementación.

## 9. Propuesta técnica mínima (NO implementada)

Las siguientes decisiones (A-E) están **recomendadas para el alcance mínimo de DATA-012**; requieren confirmación humana antes de implementarse (sección 10), pero ya no se presentan como opciones abiertas sin rumbo — cada una tiene una recomendación concreta.

### 9.1 `Consolidado2025` — Power Query (decisión A — 2025)

- Usar la columna real `Generación` de la fuente 2025; **no** derivarla de `RANGO DE EDAD`.
- Normalizar el nombre `Generación` → `GENERACIÓN` (mayúsculas) **antes** del `Table.Combine`, para que coincida con el nombre que ya produce la rama 2024 y con el que espera `Generaciones[Generación]` aguas abajo.
- Eliminar `Table.RenameColumns(..., {{"RANGO DE EDAD","GENERACIÓN"}})` **únicamente en la rama 2025** — esta eliminación no aplica a 2024 (ver 9.3).
- Conservar `RANGO DE EDAD` de 2025 como atributo independiente (`Rango de Edad`), sin transformarla ni fusionarla con Generación.
- **Generación no se agrega como columna paralela**: se usa la columna real `Generación` de 2025 para alimentar directamente el atributo generacional ya existente (`GENERACIÓN`/`Generaciones[Generación]`). No se crea una segunda columna tipo `Generación 2` (el parche local sí la agrega como alias sin uso, sección 2.1 — esa columna del parche específicamente **no se reconstruye**, ver 9.6).
- No tocar el contrato de `NIVEL_DE_CARGO`/`TIPO_DE_CARGO` en esta propuesta — la causa del error `NIVEL_DE_CARGO` (sección 4) ya está **confirmada** y se resuelve mediante la migración de fuente (decisión F, sección 9.8), no mediante un cambio adicional de código en estos dos pasos.

### 9.2 `Consolidado2025` — TMDL

- Conservar `Generación` (ya presente en el parche local, sección 2) apuntando a la columna real de la fuente, no a un alias.
- Agregar `Rango de Edad` como columna independiente — **no forma parte de las 19 columnas nuevas del parche local** (sección 2.1/2.2, confirmado: el parche nunca la agregó), debe crearse de cero, no reconstruirse desde el parche.
- **Alcance mínimo explícito — que el parche tenga 19 columnas genuinamente nuevas NO autoriza incorporarlas todas al modelo.** Para DATA-012, `Rango de Edad` es la **única** columna nueva obligatoria por requerimiento funcional (clasificación A, sección 8). Las 7 columnas clasificadas C en la sección 8 (`ÁRBOL DE NÓMINA NIVEL 2`, `ÁRBOL DE NÓMINA NIVEL 3`, `Tipo Identificación`, `COD. CARGO`, `Tipo Contrato (Kactus)`, `Indicador Actividad`, `Año Nac`) **permanecen en la fuente** — no se agregan al TMDL en esta iniciativa. Cualquier otra columna del parche (p. ej. `IDMESAÑO`, `NOMBRE`, `APELLIDO`, las variantes de nombre de empleado, `MANO DE OBRA`, `CLASIFICACION`, `FLEX`, `F_INGRESO`, `Correo Corporativo`, `PCD`) solo se incorpora si es **estrictamente necesaria para preservar un contrato ya existente del modelo** (p. ej. si `Table.Combine` o una relación ya vigente dejara de resolver sin ella) y debe **justificarse individualmente** en el futuro plan de implementación — nunca por el solo hecho de venir incluida en el parche.
- `ÁRBOL DE NÓMINA NIVEL 2/3` (decisión C): permanecen disponibles en la fuente si se agregan al TMDL, pero **no se mapean** a `NIVEL_DE_CARGO`, `TIPO_DE_CARGO`, `Área` ni `Dependencia` en este alcance — se tratan como dimensiones organizacionales complementarias para una iniciativa futura.
- `TIPO_DE_CARGO` crudo (decisión D): permanece en la fuente sin uso en el modelo mientras tenga cobertura parcial (~5,6 %); no reemplaza la columna calculada `'Tipo de Cargo'`.

### 9.3 `PLANTA DE PERSONAL` — Power Query (decisión B — 2024, sin cambios)

- **No modificar la lógica 2024.** Conservar `Table.RenameColumns(..., {{"RANGO DE EDAD","GENERACIÓN"}})` tal cual para la rama 2024 — confirmado válido por el perfilado de la sección 6-bis (2024 no tiene columna real de Generación; `RANGO DE EDAD` ya contiene cohortes generacionales).
- Dejar `Rango de Edad` nula para todo 2024 — no inventar un valor que la fuente nunca tuvo.
- Conservar `Table.Combine`, **referenciando la consulta `Consolidado2025` como tabla** (sin duplicar sus pasos en línea, corrigiendo el hallazgo de la sección 2.2).
- Asegurar que el resultado combinado tenga `Generación`/`GENERACIÓN` y `Rango de Edad` coexistiendo, con la semántica de la sección 6 (2024: Generación histórica vía sustituto, Rango de Edad nula; 2025: Generación real, Rango de Edad real parcial).

### 9.4 `PLANTA DE PERSONAL` — TMDL

- Mantener `GENERACI&#211;N` y su `lineageTag` sin cambios (ADR-007 fuera de alcance).
- Mantener la relación existente con `Generaciones[Generación]` sin cambios.
- Agregar `Rango de Edad` como atributo independiente.
- No corregir ADR-007 ni renombrar `GENERACI&#211;N` en esta iniciativa.
- `ÁRBOL DE NÓMINA NIVEL 2/3` y `TIPO_DE_CARGO` crudo: mismo tratamiento que en 9.2 (decisión C/D) — permanecen en la fuente, sin mapeo ni reemplazo de lógica existente.

### 9.5 Visuales

- La columna calculada `'Tipo de Cargo'` (2 referencias en `Demográfico (Promedio)`) **no requiere cambios** — decisión D mantiene su lógica `SWITCH` sobre `NIVEL_DE_CARGO` sin alteración.
- El visual **"Generación"** (evidencia sección 4-bis) debe volver a mostrar categorías generacionales reales para 2025 una vez aplicada la decisión A; validar visualmente tras implementación (no se puede confirmar sin refresh, fuera de alcance de esta Spec).
- No se identificó ningún otro visual que dependa de `Rango de Edad`, `Generación 2` u otras columnas nuevas — no se anticipan cambios adicionales de visuales para el alcance mínimo. Confirmar en la implementación.

### 9.6 Parche local (decisión E)

- El parche local descrito en la sección 2 **no debe reaplicarse tal cual**: contiene la regresión de codificación de Unión Libre (sección 2.2) y la duplicación en línea de `Consolidado2025` dentro de `PLANTA DE PERSONAL` (sección 2.2).
- Una futura implementación debe **reconstruir selectivamente** sobre una base limpia (`main` + PR #7 ya fusionado — sección 9.7), no partir del parche completo.
- **Aclaración explícita de alcance:** que el parche contenga 19 columnas genuinamente nuevas (sección 2.1) es una constatación sobre el diff, **no una autorización para incorporarlas todas al modelo**. La reconstrucción selectiva para el alcance mínimo de DATA-012 se limita a: (1) el cambio de `Origen` de las 3 consultas (decisión F, sección 9.8); (2) la columna `Rango de Edad`, que de hecho **no** forma parte de las 19 columnas del parche y debe crearse de cero (sección 9.2); (3) la lógica de Generación de la decisión A (sección 9.1), que reutiliza la columna real `Generación` ya existente en la fuente — no la columna `Generación 2` (alias) que sí trae el parche, la cual **no se reconstruye**. Ninguna de las otras 18 columnas genuinamente nuevas del parche (sección 2.1) se incorpora por el solo hecho de estar en el parche — solo bajo el criterio de excepción individual de la sección 9.2.

### 9.7 Dependencia obligatoria: PR #7 (Unión Libre)

Cualquier implementación futura de DATA-012 **debe partir de un `main` que ya incluya la corrección de Unión Libre de PR #7** (`Specs/0017`, branch `fix/demografico-union-libre-encoding`, commit `cb6d56a`), o de una base equivalente que preserve explícitamente esa corrección. El parche local analizado en la sección 2 predata esa corrección y la revierte silenciosamente si se reaplica sin ajuste (sección 2.2) — esta Spec no modifica ni mezcla PR #7, solo registra la dependencia de orden para la implementación.

### 9.8 Migración de fuente OneDrive personal → SharePoint corporativo (decisión F — APROBADA y verificada)

- **Aprobada como parte del alcance de DATA-012**: las 3 consultas que leen HeadCount (`Consolidado2025`, `PLANTA DE PERSONAL`, `AREAS`) deben migrar su paso `Origen` de OneDrive personal a la biblioteca corporativa `https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/Documentos%20compartidos/5.%20People%20analytics/07_Planeaci%C3%B3n_de_Personal/Data/HeadCount/{2024,2025}/...` — 2025 para `Consolidado2025`, 2024 para `PLANTA DE PERSONAL` y `AREAS`.
- **Verificada empíricamente** (sección 2.1/4): el usuario aplicó esta migración manualmente en un worktree temporal aislado y el refresh resultante cargó las 3 tablas sin error, con el esquema completo (68/74/1 columnas respectivamente, incluidas `NIVEL_DE_CARGO`/`TIPO_DE_CARGO`).
- **No implementada de forma reutilizable todavía**: el cambio vive solo en el worktree temporal `.wt/data012-verificacion-fuente`, mezclado con ruido de reserialización de Desktop (sección 2.1) — una futura implementación debe aplicar el cambio de `Origen` limpiamente sobre una base `main` + PR #7, no reutilizar ese worktree tal cual.
- **No garantiza por sí sola** el resto del alcance de DATA-012 (decisiones A-E siguen aplicando: la falsa equivalencia de Generación, sección 4-bis, persiste sin cambios tras la migración de fuente — requiere la decisión A).

## 10. Decisiones humanas pendientes

**Estado: APROBADAS.** El usuario aprobó explícitamente las decisiones A-E (sección 9.1-9.6) como base funcional para el alcance mínimo de DATA-012, y adicionalmente aprobó la decisión F (migración de fuente, sección 9.8), verificada empíricamente. Las 6 decisiones originalmente abiertas quedan así:

- **A-E: aprobadas**, sin verificación adicional pendiente — quedan como base para el plan de implementación.
- **F (migración de fuente): aprobada y verificada empíricamente** (sección 2.1/4) — ya no es una verificación pendiente, es un hecho confirmado: la fuente antigua (OneDrive personal) estaba desincronizada; la fuente corporativa nueva carga el esquema completo sin error `NIVEL_DE_CARGO`.

No quedan decisiones humanas pendientes de aprobación para el alcance mínimo documentado en esta Spec. Lo que sigue pendiente es de **ejecución**, no de decisión (ver sección 13): aplicar el cambio de `Origen` (F) limpiamente sobre una base `main` + PR #7 (no reutilizar el worktree temporal de verificación) y, sobre esa base, implementar A-E.

## 11. Riesgo de Formula Firewall / niveles de privacidad (asunto separado)

`PLANTA DE PERSONAL`, `Selección Grupo Lemco` y `SENA UNIDADES` están en la lista de fuentes con riesgo documentado de Formula Firewall (`CLAUDE.md`, `Docs/TROUBLESHOOTING.md`). El refresh verificado en la sección 2.1/4 (worktree temporal, tras la migración de fuente) completó sin errores de partición para las 52 tablas del modelo — pero el usuario reporta directamente que, en su vista de Power BI Desktop, varias consultas siguen mostrando advertencias de niveles de privacidad bloqueadas. Ambas observaciones se registran sin contradicción: el refresh puntual verificado no encontró el bloqueo, pero el riesgo de Formula Firewall/privacidad **sigue vigente como asunto separado y no resuelto** para el conjunto completo de consultas. Cualquier implementación futura de esta Spec requerirá una sesión interactiva en Power BI Desktop para resolverlo, gestionada como su propio paso — no se intenta resolver ni diagnosticar en esta Spec.

## 12. Criterio de aceptación (para una futura implementación, no para esta Spec)

- `Proyecto7.pbip` carga sin el error `NIVEL_DE_CARGO`/`TIPO_DE_CARGO` — **ya verificado empíricamente tras la migración de fuente (decisión F, sección 9.8)**; la implementación real debe reproducir esta misma condición sobre una base limpia (`main` + PR #7), no solo confiar en el worktree temporal de verificación.
- `Generación` y `Rango de Edad` coexisten como atributos independientes en `PLANTA DE PERSONAL` y `Consolidado2025`.
- 2024 conserva su Generación histórica (vía Rango de Edad como sustituto, confirmado válido en sección 6-bis) sin inventar Rango de Edad donde no existe.
- 2025 usa la Generación real de la fuente, normalizada a `GENERACIÓN` antes del `Table.Combine`.
- `GENERACI&#211;N` y su relación con `Generaciones[Generación]` no cambian.
- 0 duplicidad de lógica `Consolidado2025` (una sola consulta, referenciada, no duplicada en línea).
- No se reintroduce la regresión de codificación de Unión Libre.
- Ninguna columna de la sección 8 se incorpora al modelo salvo decisión humana explícita.
- **El visual "Generación" (evidencia sección 4-bis) muestra categorías generacionales reales** (Millennials, Generación X, Centennials, Baby Boomers), no rangos de edad.
- **El visual "Generación" nunca muestra intervalos de edad** (p. ej. "Entre 18-29 Años") como si fueran generaciones, para ninguna de las dos fuentes (2024 o 2025).
- **`Rango de Edad` existe como atributo separado y consultable**, independiente de `Generación`, visible en el modelo aunque no tenga visual dedicado en el alcance mínimo.
- **La dimensión `Generaciones` vuelve a resolver correctamente** (relación no vacía) para todos los registros con Generación válida, incluidos los de 2025.

## 13. Siguiente paso

**Actualización — implementación completada:** las decisiones A-E y F, aprobadas en la sección 10, fueron implementadas y validadas técnicamente en `Specs/0020_plan_implementacion_adaptacion_headcount_consolidado2025.md` (sección 15), rama `fix/data-012-headcount-generacion-rango-edad`. El PR #7 (punto 1 original) ya estaba fusionado a `main` (`f9e15a7`) antes de iniciar. El parche local y el worktree temporal de verificación (punto 3 original) no se reutilizaron — se reconstruyó selectivamente sobre `main` + PR #7, confirmado en `Specs/0020` sección 15.2. El riesgo de Formula Firewall/privacidad (punto 4, sección 11) **no se resolvió** — sigue vigente sin cambios, no bloqueó el cierre porque las 3 fuentes migradas cargaron sin ese bloqueo en esta sesión.

## 14. Deuda de calidad de datos detectada durante la implementación (post-análisis)

Durante la validación de la implementación (`Specs/0020` sección 15.4) se detectó, con perfilado de solo lectura del Excel y conteo exacto verificado contra los errores reportados por Power BI Desktop, que **8 columnas de la fuente 2025 contienen valores de error nativos de Excel (`#N/A`)** para un subconjunto pequeño de filas: `DEPENDENCIA_PATRON` (hasta 226 filas), `AREA_PATRON` (hasta 88), `FECHA NACIMIENTO` (hasta 42), `EDAD` (hasta 42), `Generación` (hasta 42), `RANGO DE EDAD` (hasta 42), `EST_CIVIL` (hasta 32), `AGRUPADOR` (hasta 4).

- **6 de las 8 columnas nunca son tocadas por el código de DATA-012** — prueba directa de que es un problema de calidad de la fuente (fórmulas tipo BUSCARV/XLOOKUP sin coincidencia para ciertos empleados), no un defecto introducido por esta iniciativa.
- Las 2 columnas restantes (`Generación`, `RANGO DE EDAD`) sí están en el alcance de DATA-012 — para esas ~42 filas (99,9 % de las filas quedan correctas), el motor de Analysis Services sustituye el texto literal `"false"` en lugar de dejar la celda en blanco, por no poder convertir un valor de error de Excel al tipo `string` declarado. El efecto visual es una fila sin coincidencia en `Generaciones` (blanco), no una generación incorrecta.
- **DATA-012 no corrige estos `#N/A` de origen** — decisión de alcance confirmada explícitamente por el usuario. No se aplicó ningún tipo de manipulación de datos (sin `ReplaceErrorValues`, sin `try...otherwise`, sin eliminar filas). Las 45.670/71.206 filas se preservan íntegras.
- Queda registrado como **deuda de calidad de datos** en `Specs/00_roadmap_y_backlog.md`, pendiente de una iniciativa futura de saneamiento de fuente — no bloquea el cierre técnico de DATA-012.
