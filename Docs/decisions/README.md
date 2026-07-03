# Registro de Decisiones de Arquitectura (ADR)

Este directorio contiene las decisiones tecnicas significativas tomadas en el proyecto.

Cada decision documenta: el contexto, las opciones consideradas, la decision tomada y las consecuencias.

---

## Indice de decisiones

| ID | Titulo | Estado | Fecha |
|---|---|---|---|
| ADR-001 | Uso de tabla staging `Consolidado2025` oculta | Implementado | `Pendiente de confirmar fecha` |
| ADR-002 | Tablas de Seleccion separadas por empresa | Implementado | `Pendiente de confirmar fecha` |
| ADR-003 | `Empresas` y `Mes` como datos embebidos en binario | Implementado | `Pendiente de confirmar fecha` |
| ADR-004 | `DimPeriodoYM` como tabla calculada (CROSSJOIN) | Implementado | `Pendiente de confirmar fecha` |
| ADR-005 | Paginas ocultas de versiones anteriores (Comportamiento HC Anual) | **Pendiente de decision** | — |
| ADR-006 | Ausencia de Row-Level Security | **Pendiente de decision** | — |
| ADR-007 | Encoding `GENERACI&#211;N` en nombre de columna | **Pendiente de correccion** | — |

---

## ADR-001: Uso de tabla staging `Consolidado2025` oculta

**Contexto:** Los datos de HeadCount 2024 y 2025 provienen de archivos Excel distintos.

**Decision:** Se cargo `Consolidado2025` como tabla oculta (`isHidden = true`) en el modelo y se combino con los datos de 2024 dentro del codigo M de `PLANTA DE PERSONAL` usando `Table.Combine`.

**Consecuencias:**
- (+) La tabla `PLANTA DE PERSONAL` presenta un historico unificado sin duplicacion visible para el usuario.
- (-) `Consolidado2025` ocupa memoria adicional en el modelo aunque sus datos ya estan incluidos en `PLANTA DE PERSONAL`.
- (-) La logica de consolidacion anual esta acoplada dentro de la consulta M de `PLANTA DE PERSONAL`, dificultando la adicion de nuevos anos.

---

## ADR-002: Tablas de Seleccion separadas por empresa

**Contexto:** Los procesos de seleccion de cada empresa del grupo se registran en archivos Excel independientes con estructuras similares.

**Decision:** Se creo una tabla independiente por empresa (`Seleccion Challenger`, `Seleccion Habitel Hotels`, `Seleccion Grupo Sky`, `Seleccion Grupo Lemco`), todas marcadas como `isHidden = true`.

**Consecuencias:**
- (+) Permite carga independiente por empresa.
- (+) Facilita que diferentes personas actualicen sus propios archivos.
- (-) Patron no escalable: agregar una nueva empresa requiere replicar toda la logica de transformacion.
- (-) Genera 12 LocalDateTables adicionales (3 por tabla de seleccion x 4 tablas).

---

## ADR-003: Datos de `Empresas` y `Mes` embebidos en binario

**Contexto:** El catalogo de empresas y la dimension de meses son listas cortas y relativamente estaticas.

**Decision:** Se codificaron como datos binarios comprimidos (Base64 + Deflate) directamente en el codigo M de Power Query, sin archivo externo.

**Consecuencias:**
- (+) Sin dependencias externas para estas tablas.
- (-) Para actualizar el catalogo de empresas se debe regenerar el binario o cambiar el patron de carga, lo que requiere conocimiento tecnico de Power Query.

---

## ADR-004: DimPeriodoYM como tabla calculada con CROSSJOIN

**Contexto:** Se necesitaba una dimension de periodo Ano-Mes con logica de "trimestre actual" y "trimestre anterior" dinamicos.

**Decision:** Se creo `DimPeriodoYM` como tabla calculada DAX: `CROSSJOIN('Anos', 'Mes')`, con columnas calculadas adicionales para `IndexAnioMes`, `EsTrimActual`, `EsTrimAnterior`, `Trimestre actual` y `Trimestre anterior`.

**Consecuencias:**
- (+) La logica de trimestre dinamico se basa en `TODAY()` y es siempre correcta.
- (+) Permite slicers de periodo relativo sin parametros manuales.
- (-) La tabla se recalcula en cada actualizacion del modelo.
- (-) `IndexAnioMes` se calcula tambien en `Planta Ppto` y `Ppto Retiros` como columna calculada independiente — duplicacion de logica.

---

## ADR-005: Paginas ocultas de versiones anteriores — PENDIENTE DE DECISION

**Contexto:** Existen 5 paginas ocultas (`HiddenInViewMode`) que representan versiones iterativas de "Comportamiento HC Anual" y "Demografico".

**Opciones:**
1. Eliminar las paginas ocultas del proyecto.
2. Mantenerlas ocultas indefinidamente.
3. Consolidar la version mas reciente (`_v4`) como la pagina activa visible y eliminar las anteriores.

**Decision:** `Pendiente de decision`

**Impacto de no decidir:** Tamano del archivo PBIP innecesariamente grande; confusion para futuros desarrolladores.

---

## ADR-006: Ausencia de Row-Level Security — PENDIENTE DE DECISION

**Contexto:** El modelo contiene datos nominales de colaboradores de todas las empresas del grupo. No hay roles RLS definidos.

**Opciones:**
1. Implementar RLS por empresa (`Empresas[Empresas]`) segun el usuario del servicio Power BI.
2. Mantener sin RLS, controlando el acceso a nivel de workspace.
3. Implementar RLS parcial solo para campos de datos personales.

**Decision:** `Pendiente de decision`

**Impacto de no decidir:** Cualquier usuario con acceso al reporte publicado puede ver datos de todas las empresas y de todos los colaboradores.

---

## ADR-007: Encoding HTML en nombre de columna GENERACION — PENDIENTE DE CORRECCION

**Contexto:** La columna `GENERACION` de `PLANTA DE PERSONAL` aparece en `relationships.tmdl` como `GENERACI&#211;N` (la O con tilde se encoda como entidad HTML `&#211;`).

**Causa probable:** Incompatibilidad en el proceso de serializacion TMDL al usar caracteres especiales del espanol en nombres de columna.

**Impacto:** Riesgo de quiebre en herramientas de procesamiento TMDL que no interpreten entidades HTML. La relacion con la tabla `Generaciones` puede verse afectada.

**Decision:** `Pendiente de correccion` — Evaluar si el nombre tecnico puede normalizarse a `GENERACION` (sin tilde) en la columna fuente y en la relacion.
