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

- Migración de la URL de origen de Power Query de `lemcosas-my.sharepoint.com/personal/...` (OneDrive personal) a `lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/...` (SharePoint corporativo), tanto para `Consolidado2025` como para `PLANTA DE PERSONAL` (fuente 2024). Coherente con la migración a SharePoint corporativo ya documentada como en curso en `CLAUDE.md`/`Docs/DATA_PIPELINE.md`.
- Registro en TMDL de 19 columnas nuevas en `Consolidado2025` y de las mismas columnas en `PLANTA DE PERSONAL` (para que sobrevivan el `Table.Combine`): `IDMESAÑO`, `ID_Jefe_Inmediato`, `'Jefe Inmediato (nombre-apellido)'`, `'Descripción Cargo_Jefe Inmediato'`, `NOMBRE`, `APELLIDO`, `'NOMBRE EMPLEADO (Apellidos-nombres)'`, `'NOMBRE EMPLEADO (nombre-apellido)'`, `'MANO DE OBRA'`, `CLASIFICACION`, `FLEX`, `F_INGRESO`, `'ÁRBOL DE NÓMINA NIVEL 2'`, `'ÁRBOL DE NÓMINA NIVEL 3'`, `'Tipo Identificación'`, `'COD. CARGO'`, `'Tipo Contrato (Kactus)'`, `'Indicador Actividad'`, `'Año Nac'`, `Generación`/`'Generación 2'`, `'Correo Corporativo'`, `PCD`. Todos con `lineageTag` nuevo asignado (no colisionan con columnas existentes).
- Eliminación de columnas obsoletas del esquema anterior: `'NOMBRE EMPLEADO'` (reemplazada por las 2 variantes nuevas), columna `%` (sin uso identificado).

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

`origin/main`, `PLANTA DE PERSONAL.tmdl`, partición `Consolidado2025` (tabla independiente):

```
Origen = Excel.Workbook(Web.Contents("https://.../Data/HeadCount/2025/Consolidado%202025.xlsx"), null, true),
...
#"Columnas con nombre cambiado" = Table.RenameColumns(#"Encabezados promovidos",{{"RANGO DE EDAD", "GENERACIÓN"}}),
#"Tipo cambiado1" = Table.TransformColumnTypes(#"Columnas con nombre cambiado",{{"MES", type text}, {"NIVEL_DE_CARGO", type text}, {"TIPO_DE_CARGO", type text}})
```

**Confirmado con evidencia local:** el archivo Excel del repositorio contiene `NIVEL_DE_CARGO` y `TIPO_DE_CARGO` con nombre exacto, sin caracteres ocultos — el paso `Table.TransformColumnTypes` debería encontrarlas sin problema si Power Query leyera *este* archivo.

**Hipótesis principal (no verificable sin refresh, explícitamente fuera de alcance de esta sesión):** el paso `Origen` no lee el archivo local del repositorio — lee la copia publicada en SharePoint corporativo vía `Web.Contents(...)`. Si esa copia remota no está sincronizada con la estructura ya restructurada del archivo local (por ejemplo, si la subida a SharePoint quedó pendiente o se hizo desde una versión anterior del archivo), el motor de Power Query fallaría exactamente con "No se encontró la columna 'NIVEL_DE_CARGO' de la tabla" al intentar tipificarla, aunque la columna exista en la copia local. Esto es coherente con el estado ya documentado en `CLAUDE.md`: *"la migración de fuentes hacia SharePoint corporativo no está cerrada funcionalmente"*.

**Hallazgo secundario que agrava el problema, independiente de la hipótesis anterior:** el paso `Table.RenameColumns(..., {{"RANGO DE EDAD", "GENERACIÓN"}})` sigue vigente aunque la hoja ahora tiene una columna real `Generación` (posición 38) **además** de `RANGO DE EDAD` (posición 39). Tras el renombrado, la tabla tendría simultáneamente una columna `Generación` original y una `GENERACIÓN` producida por el renombrado — un choque de nombres (case-insensitive en M) que puede producir un sufijo automático (`Generación.1`) o un comportamiento no determinista, y que en cualquier caso es conceptualmente incorrecto: ya no hace falta *fingir* Generación a partir de Rango de Edad cuando la fuente ya trae el dato real.

**No se puede confirmar cuál de las dos causas (o ambas) provoca el error exacto sin abrir Power BI Desktop y observar el paso que falla o sin verificar el contenido real del archivo publicado en SharePoint** — ninguna de las dos acciones se ejecutó en esta sesión (refresh y resolución de Formula Firewall están explícitamente fuera de alcance).

## 5. Generación vs. Rango de Edad — diferencia conceptual

Son dos atributos demográficos **distintos y complementarios**, no intercambiables:

- **Generación**: cohorte generacional (p. ej. Millennials, Generación X) — hoy poblada al 100 % de las 45.670 filas de `Consolidado2025` mediante la columna real `Generación`.
- **Rango de Edad**: bandas etarias — poblada solo en 17.674 de 45.670 filas (~39 %) en la fuente 2025 actual; es un atributo independiente, no una fuente para derivar Generación.

La lógica histórica (`Table.RenameColumns(..., {{"RANGO DE EDAD","GENERACIÓN"}})`) fue una aproximación válida **solo cuando la fuente 2024 no tenía una columna real de Generación** — se usaba Rango de Edad como sustituto. Con la columna real disponible en 2025, esa sustitución ya no es necesaria y produce una falsa equivalencia.

## 6. Comportamiento esperado 2024 vs. 2025

| | 2024 (histórico, `PLANTA DE PERSONAL`) | 2025 (`Consolidado2025`) |
|---|---|---|
| Generación | Proviene de `RANGO DE EDAD` (sustituto histórico) — **no se debe inventar** un valor real que la fuente 2024 nunca tuvo | Proviene de la columna real `Generación` |
| Rango de Edad | Puede quedar nulo si la fuente histórica no trae un rango de edad real independiente de la sustitución | Proviene de la columna real `RANGO DE EDAD` (con cobertura parcial, ~39 %) |
| `GENERACIÓN` → `GENERACI&#211;N` | Se conserva sin cambios (paso posterior al `Table.Combine`, ADR-007, no se toca en esta iniciativa) | Igual — el `Table.Combine` unifica antes de este paso, por lo que aplica a ambas fuentes por igual |
| Relación con `Generaciones[Generación]` | Se conserva sin cambios | Igual |

No se verificó en esta sesión (sin abrir Desktop) si la fuente 2024 tiene una columna `Rango de Edad`/`RANGO DE EDAD` real independiente de la que hoy se usa como sustituto de Generación — es una decisión pendiente (sección 10).

## 7. ÁRBOL DE NÓMINA NIVEL 2/3 vs. NIVEL_DE_CARGO/TIPO_DE_CARGO

**No existe homologación inequívoca. Me detengo en esta decisión — ver sección 10.**

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

### 9.1 `Consolidado2025` — Power Query
- Eliminar `Table.RenameColumns(..., {{"RANGO DE EDAD","GENERACIÓN"}})`.
- Normalizar el nombre real de `Generación` al que espera el modelo aguas abajo (a definir junto con la decisión de la sección 10).
- Conservar `Rango de Edad` como columna independiente, sin transformarla.
- Resolver el contrato de `NIVEL_DE_CARGO`/`TIPO_DE_CARGO` según la decisión de la sección 7/10 (mínimo: no forzar tipo sobre una columna cuya existencia remota no está confirmada sin antes verificar la fuente publicada).

### 9.2 `Consolidado2025` — TMDL
- Conservar `Generación` (ya presente en el parche local, sección 2).
- Agregar `Rango de Edad` como columna independiente (pendiente en el parche local).
- Confirmar cuáles de las 8 columnas de la sección 8 se incorporan (ninguna por defecto, salvo Rango de Edad).

### 9.3 `PLANTA DE PERSONAL` — Power Query
- Conservar la lógica histórica de 2024 (Rango de Edad → Generación como sustituto, solo para esa fuente).
- Conservar `Table.Combine`, **referenciando la consulta `Consolidado2025` como tabla** (sin duplicar sus pasos en línea, corrigiendo el hallazgo de la sección 2.2).
- Asegurar que el resultado combinado tenga `Generación` y `Rango de Edad` coexistiendo, con la semántica de la sección 6 (histórico puede tener `Rango de Edad` nulo; no inventar valores).

### 9.4 `PLANTA DE PERSONAL` — TMDL
- Mantener `GENERACI&#211;N` y su `lineageTag` sin cambios (ADR-007 fuera de alcance).
- Mantener la relación existente con `Generaciones[Generación]` sin cambios.
- Agregar `Rango de Edad` como atributo independiente.
- No corregir ADR-007 ni renombrar `GENERACI&#211;N` en esta iniciativa.

### 9.5 Visuales
- La columna calculada `'Tipo de Cargo'` (2 referencias en `Demográfico (Promedio)`) no requiere cambios si `NIVEL_DE_CARGO` se sigue poblando igual que hoy.
- No se identificó ningún visual que dependa de `Rango de Edad`, `Generación 2` u otras columnas nuevas — no se anticipan cambios de visuales para el alcance mínimo (Rango de Edad). Confirmar en la implementación.

## 10. Decisiones humanas pendientes

1. **¿La copia de `Consolidado 2025.xlsx` en SharePoint corporativo ya tiene la estructura restructurada (68 columnas, incluida `NIVEL_DE_CARGO`)?** Determina si la causa del error es de sincronización de fuente o hay otra causa. Requiere verificación directa en SharePoint o un refresh controlado (fuera de alcance de esta sesión).
2. **Nombre final de la columna `Generación` en `Consolidado2025`** tras eliminar la falsa equivalencia — ¿se normaliza a `GENERACIÓN` (mayúsculas, como espera el `Table.Combine`) o se ajusta el `Table.Combine` para aceptar `Generación`?
3. **¿La fuente histórica 2024 tiene una columna real de Rango de Edad**, distinta de la que hoy se usa como sustituto de Generación, o debe quedar nula para todo 2024?
4. **Destino funcional de `ÁRBOL DE NÓMINA NIVEL 2/3`**: ¿reemplazan a futuro `Dependencia`/`Área` (ya presentes en el modelo), los complementan, o son exclusivos de la iniciativa de Contratos Kactus? Sin esta definición no se puede proponer un mapeo.
5. **Destino funcional de `TIPO_DE_CARGO` (crudo)** una vez esté completamente poblado: ¿reemplaza la lógica calculada `'Tipo de Cargo'`, o coexisten?
6. **Confirmación de que el parche local descrito en la sección 2 debe descartarse tal cual** (por la regresión de Unión Libre) y reconstruirse sobre `main` + PR #7 ya fusionado, no reutilizarse directamente.

## 11. Riesgo de Formula Firewall (asunto separado)

`PLANTA DE PERSONAL` está en la lista de fuentes con riesgo documentado de Formula Firewall (`CLAUDE.md`, `Docs/TROUBLESHOOTING.md`). Cualquier implementación futura de esta Spec requerirá una sesión interactiva en Power BI Desktop para resolverlo, gestionada como su propio paso — no se intenta resolver ni diagnosticar en esta Spec.

## 12. Criterio de aceptación (para una futura implementación, no para esta Spec)

- `Proyecto7.pbip` carga sin el error `NIVEL_DE_CARGO`/`TIPO_DE_CARGO`.
- `Generación` y `Rango de Edad` coexisten como atributos independientes en `PLANTA DE PERSONAL` y `Consolidado2025`.
- 2024 conserva su Generación histórica (vía Rango de Edad como sustituto) sin inventar Rango de Edad donde no existe.
- 2025 usa la Generación real de la fuente.
- `GENERACI&#211;N` y su relación con `Generaciones[Generación]` no cambian.
- 0 duplicidad de lógica `Consolidado2025` (una sola consulta, referenciada, no duplicada en línea).
- No se reintroduce la regresión de codificación de Unión Libre.
- Ninguna columna de la sección 8 se incorpora al modelo salvo decisión humana explícita.

## 13. Siguiente paso

1. Obtener respuesta del usuario a las 6 decisiones de la sección 10.
2. Verificar (el usuario o en una sesión interactiva futura) el estado real de la copia SharePoint de `Consolidado 2025.xlsx`.
3. Con esas respuestas, elaborar el plan de implementación (`Specs/00XX_plan_implementacion_...md`, consecutivo a determinar en su momento) — no antes.
4. No reutilizar el parche local de la sección 2 sin antes reconstruirlo sobre `main` + PR #7 fusionado.
