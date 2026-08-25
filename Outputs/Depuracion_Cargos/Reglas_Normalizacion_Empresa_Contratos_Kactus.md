# Reglas de normalización de Empresa — Kactus ↔ Consolidado 2025

## 1. Encabezado y estado

**Estado:** documentación **VERSIONADA en Git por autorización explícita del
usuario** (cierre documental temporal: **2026-08-25**), como excepción
intencional de gobierno dentro de `Outputs/` — carpeta excluida de Git por
defecto (`.gitignore`, sin modificar). La excepción cubre únicamente este
archivo `.md` y el notebook `01_construccion_tabla_depuracion_cargos.ipynb`.
**`Tabla_Depuracion_Cargos.xlsx` permanece fuera de Git** — sigue siendo
salida operacional local/SharePoint, no se versiona.

**Este es un cierre TEMPORAL de la documentación, no un cierre funcional de
la tarea.** El estado funcional real (qué quedó terminado, QA vigente y
pendientes abiertos) está en las secciones 13 a 15.

**Origen:** confirmado por el usuario en conversación del 2026-08-24/25, como
insumo para la conciliación de `01_construccion_tabla_depuracion_cargos.ipynb`.
**Alcance:** reconstrucción de la `Empresa` Kactus de origen a partir de
`Consolidado 2025.xlsx` (hoja `Consolidado2025`), para las 8 empresas del
Grupo Empresarial Lemco representadas en el Maestro de Cargos-Roles Kactus.

> Cuando se retome la automatización del módulo de contratos, esta lógica
> debe promoverse a documentación versionada definitiva (`Docs/DATA_PIPELINE.md`
> o equivalente) y utilizarse como requisito funcional del proceso de
> normalización. Hoy vive en `Outputs/` como excepción controlada de
> gobierno, no como ubicación definitiva.

---

## 2. Contexto

`Consolidado 2025.xlsx` registra cada mes los colaboradores **activos**
según el cierre mensual de Planeación de Personal. Sus campos
`GRUPO EMPRESA` y `Nombre Empresa` son etiquetas operativas/reporting,
ajustadas manualmente durante la preparación de reportes de contratos de
LEMCO — **no son identificadores legales equivalentes al código `Empresa`**
de los 8 archivos Kactus de
`Data/Maestro_Cargos-Roles_Kactus/Insumos_Vigentes/`.

## 3. Principio general de normalización

`GRUPO EMPRESA` es una **agrupación de reporting/corporativa** (5 valores:
`CHALLENGER`, `FUNDACIÓN CHALLENGER`, `GRUPO SKY`, `HABITEL HOTELS`, `LEMCO`)
y **no** equivale 1:1 al identificador legal/origen Kactus (`Empresa`, 8
códigos: 1, 3, 5, 6, 7, 8, 9, 10). Por ejemplo, `HABITEL HOTELS` agrupa por
sí solo las empresas legales Kactus 6, 7 y 10.

El campo correcto para reconstruir la empresa Kactus de origen es
**`Nombre Empresa`**, resultado de reglas manuales aplicadas durante la
preparación mensual del Consolidado. `Nombre Empresa` **sí** identifica de
forma unívoca la empresa Kactus, bajo el catálogo de reglas confirmado en la
sección 4.

## 4. Catálogo completo de reglas confirmadas

| Archivo Kactus de origen | Empresa Kactus | Nombre Empresa (Kactus) | GRUPO EMPRESA (Consolidado) | Nombre Empresa (Consolidado) | Regla especial |
|---|---|---|---|---|---|
| `CHALLENGER SAS.xlsx` | 1 | CHALLENGER S.A.S. | `CHALLENGER` | `CHALLENGER` | Ninguna |
| `FUNDACION CHALLENGER.xlsx` | 5 | FUNDACION CHALLENGER | `FUNDACIÓN CHALLENGER` | `FUNDACIÓN CHALLENGER` | Ninguna |
| `SKY INDUSTRIAL.xlsx` | 8 | SKY INDUSTRIAL | `GRUPO SKY` | `SKY INDUSTRIAL` | Ninguna |
| `SKY FORWARDER SAS.xlsx` | 3 | SKY FORWARDER S.A.S. | `GRUPO SKY` | `SKY FORWARDER` | Ninguna |
| `SKY LOGISTICA INTEGRAL.xlsx` | 9 | SKY LOGISTICA INTEGRAL | `GRUPO SKY` | `SKY LOGÍSTICA INTEGRAL` | Ninguna |
| `LEMCO SAS.xlsx` | 7 | LEMCO SAS | `LEMCO` | `LEMCO` | Caso A — ver sección 5 |
| `LEMCO SAS.xlsx` (mismo origen legal) | 7 | LEMCO SAS | `HABITEL HOTELS` (etiqueta de reporting, no la empresa legal) | `LEMCO SALVIO` | Caso B — ver sección 5 |
| `OPERADORA HABITEL SAS.xlsx` | 10 | OPERADORA HABITEL SAS | `HABITEL HOTELS` | `OPERADORA` | Ninguna |
| `HABITEL SAS.xlsx` | 6 | HABITEL S.A.S. | `HABITEL HOTELS` | `HABITEL PRIME` | Ver sección 6 |
| `HABITEL SAS.xlsx` | 6 | HABITEL S.A.S. | `HABITEL HOTELS` | `HABITEL SELECT` | Ver sección 6 |
| `HABITEL SAS.xlsx` | 6 | HABITEL S.A.S. | `HABITEL HOTELS` | `HABITEL NÓMINA COMPARTIDA` | Ver sección 6 |

**Validación empírica (julio 2026, 2 572 filas de Consolidado):** para cada
una de las 11 combinaciones anteriores se comparó el `COD. CARGO` de
Consolidado contra el catálogo `Cargo` de la empresa Kactus asignada.
Solapamiento ≈100% en 10 de 11 combinaciones; `CHALLENGER` da 96.8%
(121/125), inconsistencia preexistente y fuera del alcance de esta regla.
Las 11 combinaciones `GRUPO EMPRESA`/`Nombre Empresa` presentes en julio 2026
quedan cubiertas por este mapeo — 0 combinaciones sin resolver.

---

## 5. Regla especial — LEMCO / LEMCO SALVIO (Empresa Kactus 7)

El archivo legal/origen es siempre `LEMCO SAS.xlsx` → Empresa Kactus `7`,
independientemente de cómo se reporte el mes en Consolidado:

- **Caso A:** `GRUPO EMPRESA = LEMCO`, `Nombre Empresa = LEMCO`.
- **Caso B:** `GRUPO EMPRESA = HABITEL HOTELS`, `Nombre Empresa = LEMCO SALVIO`.

`LEMCO SALVIO` debe conciliarse con Empresa Kactus `7`, **no** con
`HABITEL S.A.S.` (6) ni `OPERADORA HABITEL SAS` (10), a pesar de aparecer
bajo el mismo `GRUPO EMPRESA = HABITEL HOTELS` que esas dos.

### Dependencia externa

Según el usuario, el resultado mensual (Caso A vs. Caso B) depende de una
**base suministrada por Planeación de Personal**, en función del **CCO** y
el **cargo** del colaborador. Esta base no forma parte de
`Consolidado 2025.xlsx` ni del Maestro de Cargos-Roles Kactus; **no se
automatiza** en este notebook. Se documenta como regla aún no automatizable
(sección 10).

## 6. Regla especial — HABITEL S.A.S. (Empresa Kactus 6)

`HABITEL S.A.S.` (Empresa Kactus `6`) — el caso más complejo — reparte su
nómina en tres etiquetas `Nombre Empresa` distintas dentro de
`Consolidado 2025.xlsx`, todas bajo `GRUPO EMPRESA = HABITEL HOTELS`:

- `HABITEL PRIME`
- `HABITEL SELECT`
- `HABITEL NÓMINA COMPARTIDA`

Las tres se conciliaron con Empresa Kactus `6` para efectos de esta
depuración (validado por solapamiento de `COD. CARGO`, sección 4) y
cubrieron el 100% de los casos observados en julio 2026. **No se debe
asumir que son las únicas posibles** — si en un cierre futuro aparece una
etiqueta `HABITEL *` nueva, no está cubierta automáticamente por esta tabla.

### Dependencia externa

El usuario confirmó que la asignación real de `Nombre Empresa` depende de:

- **Clase / Tipo de Nómina** del colaborador (ver catálogo, sección 7).
- Una **base adicional suministrada por las Unidades Hoteleras**, no
  presente en `Consolidado 2025.xlsx` ni en el Maestro Kactus.

Por instrucción explícita del usuario, **no se crean reglas adicionales
para otros tipos de nómina** sin evidencia directa — solo se usan las tres
etiquetas confirmadas arriba.

---

## 7. Catálogo Tipo de Nómina (evidencia visual aportada por el usuario)

Catálogo completo aportado como evidencia visual por el usuario. Se deja
documentado en su totalidad; **solo los códigos 2, 3 y 5** (resaltados)
tienen una regla de conciliación confirmada y en uso (sección 6), por
coincidencia de nomenclatura con las etiquetas `Nombre Empresa` de
Consolidado — **este cruce código↔etiqueta es una inferencia por
nomenclatura, no fue validado directamente con datos fila a fila**. Los
demás códigos **no se usan** para inferir `Nombre Empresa` ni
`Empresa Kactus` en este notebook.

| Código | Descripción | ¿Regla de conciliación confirmada? |
|---|---|---|
| 1 | CASINO NORMAL C.M. | No |
| 2 | PRIME | Sí → HABITEL PRIME → Empresa Kactus 6 |
| 3 | SELECT | Sí → HABITEL SELECT → Empresa Kactus 6 |
| 4 | SIN CASINO | No |
| 5 | NOMINA COMPARTIDA | Sí → HABITEL NÓMINA COMPARTIDA → Empresa Kactus 6 |
| 100 | ELECCION TEMPORAL S.A. | No |
| 101 | ASIGNAR | No |
| 102 | TEMPORAL ASERTEMPO | No |
| 103 | ALIANZA TEMPORAL | No |
| 202 | CESION DE LEMCO A HABITEL | No |
| 203 | CESION DE LEMCO A HABITEL TEMPORAL | No |
| 204 | CESION DE HABITEL A LEMCO | No |

---

## 8. Columnas técnicas auditadas y descartadas como identificador legal

Se evaluaron 19 columnas de `Consolidado2025` (`COD`, `CCO`, `CARGO_CCO`,
`TIPO_CONTR`, `Tipo Contrato (Kactus)`, `AGRUPADOR`, `SEGMENTO`,
`DEPARTAMENTO`, `PRESUPUESTO`, `NIVEL_DE_CARGO`, `TIPO_DE_CARGO`,
`Indicador Actividad`, `N_Contrato`, `MOTIVO DE INGRESO`,
`DEPENDENCIA_PATRON`, `AREA_PATRON`, `NOVEDAD`, `ÁRBOL DE NÓMINA NIVEL 2/3`,
`Tipo Identificación`) buscando un campo técnico estable e independiente de
`Nombre Empresa` que permitiera desambiguar HABITEL/OPERADORA/LEMCO SALVIO
sin depender de reglas de negocio. Ninguna cumple ese rol:

- `COD` es una concatenación de `Nombre Empresa` + `Dependencia`, no un
  código propio.
- `CCO` (centro de costo) reutiliza numeración entre `HABITEL SELECT` y
  `HABITEL PRIME`, y usa un esquema totalmente distinto para
  `LEMCO SALVIO` — no correlaciona con la empresa legal Kactus.
- `AGRUPADOR` refleja las mismas etiquetas operativas que `Nombre Empresa`
  (`PRIME`, `SELECT`, `LEMCO SALVIO`, etc.), sin información adicional.

Por eso la resolución final se basó en las reglas de negocio confirmadas por
el usuario (sección 4), no en un campo técnico de Consolidado.

---

## 9. Impacto cuantitativo de este mapeo en la conciliación (julio 2026)

Comparado contra el mapeo anterior (6 empresas: CHALLENGER, FUNDACIÓN
CHALLENGER, LEMCO, SKY FORWARDER, SKY INDUSTRIAL, SKY LOGÍSTICA INTEGRAL,
sin HABITEL/OPERADORA/LEMCO SALVIO), este mapeo de 11 combinaciones:

- **Resuelve los 315 cargos Kactus de Empresa 6 y 10** que antes quedaban en
  la categoría retirada "Empresa no conciliable automáticamente"
  (156 de Empresa 6, 159 de Empresa 10) — 0 quedan sin resolver.
- **Incorpora 70 filas adicionales de julio 2026** (`LEMCO SALVIO`) al
  lookup de Empresa Kactus 7, lo que cambia el estado de conciliación de
  **32 de los 362 cargos de `LEMCO SAS.xlsx`** (validado por reconstrucción
  independiente antes/después):
  - 27 pasan de "Sin presencia" → "Con presencia" (única).
  - 3 pasan de "Con presencia" (única) → "Dependencia/Área múltiple".
  - 2 pasan de "Sin presencia" → "Dependencia/Área múltiple".
- **Eleva la cobertura de `Dependencia`/`Área`** de 10.0% a 13.5% sobre los
  2 004 cargos Kactus.

Detalle completo, cifras por empresa y metodología reproducible: ver
secciones 12 (mapeo Empresa), 13 (construcción del lookup), 13b (resolución
HABITEL/OPERADORA/LEMCO SALVIO), 15 (reclasificación y enriquecimiento),
15b (conciliación Ind. Actividad), 15c (Cargos ocupados vs. activos) y 16b
(recálculo de los 315 cargos previamente ambiguos) de
`01_construccion_tabla_depuracion_cargos.ipynb`.

---

## 10. Reglas aún no automatizables

1. **LEMCO vs. LEMCO SALVIO (Empresa Kactus 7).** Requiere la base de
   Planeación de Personal (CCO + cargo) para determinar, mes a mes, si un
   colaborador se reporta como Caso A o Caso B. No automatizado.
2. **Asignación fina dentro de HABITEL S.A.S. (Empresa Kactus 6).**
   Requiere la base adicional de Unidades Hoteleras y el campo Clase/Tipo
   de Nómina para decidir entre PRIME / SELECT / NÓMINA COMPARTIDA (o
   cualquier otro tipo de nómina del catálogo de la sección 7 que aún no
   tenga regla confirmada). No automatizado.
3. **Códigos de Tipo de Nómina 1, 4, 100–103, 202–204.** Sin regla de
   conciliación confirmada por el usuario — no se infiere su empresa de
   destino.
4. **Variantes adicionales de `Nombre Empresa` para LEMCO SAS.** No se ha
   confirmado si existen más allá de `LEMCO` y `LEMCO SALVIO`.

---

## 11. Consolidado mensual — contexto de negocio

`Consolidado 2025.xlsx` registra cada mes **únicamente colaboradores
ACTIVOS** según el cierre mensual realizado por Planeación de Personal. No es
un catálogo de cargos — es una fotografía de dotación activa por periodo.

A partir de **julio de 2026** se incorporó el campo **`COD. CARGO`**,
específicamente para permitir la conciliación con **`Número de cargo`** del
Maestro de Cargos Kactus. La finalidad de esta conciliación es identificar
qué códigos de cargo tienen realmente colaboradores activos según el cierre
mensual — no es un campo que haya existido siempre en Consolidado.

**`Ind. Actividad = "A"` de Kactus NO se considera una fuente plenamente
actualizada de actividad y NO debe sobrescribirse.** Se conserva siempre como
atributo original de Kactus, y se contrasta (sin modificarlo) contra la
presencia real en el cierre mensual — ver sección 9 y la hoja
`QA_Conciliacion` del Excel operacional.

**La ausencia de un cargo en Consolidado NO implica automáticamente:**

- inactivación del cargo;
- eliminación del cargo;
- error en el dato.

Puede corresponder, entre otras causas, a:

- una vacante;
- un cargo disponible sin colaborador asignado;
- un cargo sin colaborador activo en ese periodo específico;
- un registro que requiere depuración manual.

## 12. Reglas de transformación — módulo Contratos Kactus

Fuente operativa de este módulo (**distinta** del Maestro de Cargos-Roles
usado en esta tarea): `Data/Contratos_Kactus/Insumos_Vigentes`.

> **IMPORTANTE — no confundir fuentes.** Las reglas de esta sección son las
> mismas 11 reglas de normalización de Empresa de la sección 4 (mismo
> catálogo de 8 empresas legales, mismos archivos de origen Kactus), pero
> aplicadas al contexto del **módulo de Contratos Kactus** para su futura
> automatización. Los nombres físicos de archivo de
> `Data/Maestro_Cargos-Roles_Kactus/Insumos_Vigentes/` (usados en esta tarea
> de Depuración de Cargos) **no deben confundirse** con los de
> `Data/Contratos_Kactus/Insumos_Vigentes/` (módulo de contratos, fuera de
> alcance de esta tarea) — aunque ambos módulos comparten el mismo catálogo
> de empresas legales y las mismas reglas de normalización documentadas aquí.

| Archivo Kactus | GRUPO EMPRESA | Nombre Empresa | Notas |
|---|---|---|---|
| `CHALLENGER S.A.S..xlsx` | `CHALLENGER` | `CHALLENGER` | — |
| `FUNDACION CHALLENGER.xlsx` | `FUNDACIÓN CHALLENGER` | `FUNDACIÓN CHALLENGER` | — |
| `SKY INDUSTRIAL.xlsx` | `GRUPO SKY` | `SKY INDUSTRIAL` | — |
| `SKY FORWARDER S.A.S..xlsx` | `GRUPO SKY` | `SKY FORWARDER` | — |
| `SKY LOGISTICA INTEGRAL.xlsx` | `GRUPO SKY` | `SKY LOGÍSTICA INTEGRAL` | — |
| `LEMCO SAS.xlsx` | Caso A: `LEMCO` / Caso B: `HABITEL HOTELS` | Caso A: `LEMCO` / Caso B: `LEMCO SALVIO` | Depende de base de Planeación de Personal + CCO + cargo. Intervención manual actualmente. Preservar esta lógica para la futura automatización del módulo de contratos (ver sección 10, punto 1). |
| `OPERADORA HABITEL SAS.xlsx` | `HABITEL HOTELS` | `OPERADORA` | — |
| `HABITEL S.A.S..xlsx` | `HABITEL HOTELS` | Depende de Clase/Tipo de Nómina + base de Unidades Hoteleras. Valores confirmados: `HABITEL PRIME`, `HABITEL SELECT`, `HABITEL NÓMINA COMPARTIDA` | No inferir automáticamente reglas para otros tipos de nómina sin evidencia directa (ver catálogo Tipo de Nómina, sección 7, y sección 10 punto 2). |

Esta tabla es un resumen orientado a la futura automatización de Contratos
Kactus; la fuente normativa completa y validada empíricamente sigue siendo
la sección 4.

## 13. Estado funcional — Terminado

Lo siguiente quedó implementado y validado en esta tarea:

- Consolidación de los 8 archivos del Maestro de Cargos Kactus.
- 2 004 cargos finales, clave `Empresa + Número de cargo` 100% única, 0
  duplicados.
- `HABITEL SAS.xlsx` corregido y conciliado como Empresa Kactus 6;
  `OPERADORA HABITEL SAS.xlsx` conciliada como Empresa Kactus 10.
- Catálogo de 11 reglas de normalización de Empresa implementado (sección 4).
- 315/315 cargos previamente ambiguos (Empresa 6 y 10) resueltos — 0
  quedaron sin resolver.
- Regla `LEMCO SALVIO` → Empresa Kactus 7 implementada y validada (32/362
  cargos de LEMCO cambiaron de estado — ver sección 9).
- Conciliación contra el cierre de julio 2026 de `Consolidado 2025.xlsx`.
- Excel operacional (`Tabla_Depuracion_Cargos.xlsx`) generado con 3 hojas:
  `Depuracion_Cargos`, `QA_Conciliacion`, `Conflictos_Dependencia_Area`.
- Notebook reproducible, ejecutado de principio a fin sin errores contra las
  fuentes vigentes al 2026-08-24.
- Reglas de negocio consolidadas en este documento.
- Archivos redundantes (`-Mexico`, Excel intermedios) auditados y eliminados
  de `Outputs/Depuracion_Cargos/`.

**Entorno de ejecución usado para generar el Excel vigente (histórico):**
Python 3.11 (entorno temporal fuera del repositorio). **Estado actual del
entorno preparado para retomar la tarea:** el `.venv` propio del proyecto
quedó preparado con Python 3.14.3, pandas 3.0.5, openpyxl 3.1.5, ipykernel
7.3.0 y el kernel `planeacion_personal` ("Python 3.14 - Planeacion
Personal") registrado. Un kernel registrado con `--user` es local al
perfil/máquina donde se registró — al retomar desde otro equipo o perfil de
Windows, puede requerir registrarlo nuevamente. Ver detalle completo en
`Specs/0022_cierre_temporal_depuracion_cargos.md` sección 15.

## 14. Estado funcional — QA conocido (validado contra el Excel vigente, 2026-08-25)

- Cargos totales: **2 004**.
- Dependencia/Área única: **270**.
- Dependencia/Área múltiple: **77** cargos Kactus (80 claves conflictivas en
  el lookup de Consolidado: 77 con match en el catálogo Kactus, 3 sin match
  — ver sección 9 y hoja `Conflictos_Dependencia_Area`).
- Sin presencia en el cierre de julio 2026: **1 657**.
- `Ind. Actividad = A` + presente: **347**.
- `Ind. Actividad = A` + ausente: **144** (ver pendiente 1, sección 15).
- `Ind. Actividad != A` + presente: **0**.
- `Ind. Actividad != A` + ausente: **1 513**.
- Discrepancias `Cargos ocupados` (Kactus) vs. colaboradores activos julio
  2026: **1 001** de 2 004 comparables.
- Casos `Cargos ocupados > Número de cargos`: **68**.
- `Fecha de creación` vacía: **9**.

**Hallazgos funcionales adicionales, detectados y validados el 2026-08-25**
(no reportados en la primera entrega — ver pendientes 3 y 4, sección 15):

- **`Cargos ocupados` NEGATIVO: 96 cargos.** No investigado aún; no se
  modificó ningún valor.
- **`Número de cargos` VACÍO: 28 cargos.** El chequeo de Fase 1
  (`numero_de_cargos_invalido`) no capturó estos casos como inválidos — es
  una brecha de QA identificada, pendiente de corrección en el notebook.

## 15. Pendientes (tarea PAUSADA, no finalizada)

1. **Revisar los 144 cargos `Ind. Actividad = A` sin colaborador activo en
   julio 2026.** No asumir automáticamente que deban inactivarse.
2. **Revisar los 77 cargos Kactus con múltiples combinaciones
   Dependencia/Área.** No elegir una combinación arbitrariamente.
3. **Analizar las discrepancias entre `Cargos ocupados` (Kactus) y
   colaboradores activos del cierre mensual** (1 001 casos).
4. **Investigar el significado funcional de los 96 valores negativos en
   `Cargos ocupados`.**
5. **Revisar los 68 casos `Cargos ocupados > Número de cargos`.**
6. **Revisar los 28 cargos con `Número de cargos` vacío** y corregir el
   chequeo de QA de Fase 1 que no los capturó como inválidos.
7. **Definir si se requiere una fuente adicional** (más allá de Consolidado
   2025) para resolver cargos transversales con múltiples
   Dependencias/Áreas.
8. **Automatizar en el futuro:**
   - LEMCO vs. LEMCO SALVIO (dependencia de Planeación + CCO + cargo);
   - clasificación fina de HABITEL S.A.S. (Clase/Tipo de Nómina + base de
     Unidades Hoteleras).
9. **Parametrizar el notebook para futuros periodos.** Actualmente julio
   2026 está codificado explícitamente como periodo autorizado — no cambiar
   automáticamente a agosto u otro mes sin confirmar antes que sigue siendo
   el periodo máximo disponible en Consolidado.
10. **Diligenciar `Fecha de actualización`** únicamente cuando la depuración
    funcional se cierre realmente — hoy permanece vacía en las 2 004 filas.

---

## 16. Notas de gobierno y futura automatización

- Esta documentación fue LOCAL (`Outputs/Depuracion_Cargos/`) hasta el
  2026-08-25, fecha en la que el usuario autorizó explícitamente
  versionarla como excepción de gobierno — ver sección 1. No se modifica
  `Docs/DATA_PIPELINE.md` mientras el estado de migración a SharePoint siga
  pendiente (ver `CLAUDE.md` — Estado Crítico Vigente).
- `Fecha de actualización` se mantiene vacía en las 2 004 filas de
  `Tabla_Depuracion_Cargos.xlsx` — la tarea de depuración de cargos aún no
  está cerrada funcionalmente (persisten 80 claves con conflicto
  Dependencia/Área, los 10 pendientes de la sección 15 y las reglas no
  automatizables de la sección 10).
- Cuando se retome la automatización del módulo de contratos, esta lógica
  debe promoverse a documentación versionada definitiva y utilizarse como
  requisito funcional del proceso de normalización.
