# 0033 - Cierre de la actualización de HeadCount (septiembre 2026)

## Objetivo

Dejar documentado el cierre operativo del corte de septiembre de 2026 de
HeadCount: la carga del bloque mensual en `Consolidado 2025.xlsx`, las reglas de
negocio aplicadas, la generación y validación de los cuatro archivos mensuales
`Sin Salario`, las validaciones ejecutadas, las excepciones vigentes y el estado
real de Power BI, de forma reproducible para los cortes siguientes.

Esta spec es **documental**. No introduce cambios en `Data/`, `PBIP/`, el modelo
semántico, scripts ni pruebas.

## 1. Alcance

- Fuente principal: `Data/HeadCount/2025/Consolidado 2025.xlsx`, hoja
  `Consolidado2025`.
- Periodo: `AÑO = 2026`, `MES = 09.Septiembre`.
- Bloque final del periodo: filas `48269:50873`.
- Total de colaboradores del corte: **2.605**.

Distribución final por `GRUPO EMPRESA`:

| `GRUPO EMPRESA` | Colaboradores |
|---|---:|
| CHALLENGER | 1.924 |
| HABITEL HOTELS | 326 |
| GRUPO SKY | 254 |
| LEMCO | 97 |
| FUNDACIÓN CHALLENGER | 4 |
| **Control** | **2.605** |

Fuera de alcance de esta spec:

- INGRESOS y RETIROS de septiembre en `Data/HeadCount/PptovsReal.xlsx`. Ese
  frente continúa separado y no está cerrado.
- Automatización del procedimiento mensual.
- Corrección de la deuda heredada de plantilla descrita en la sección 9.

## 2. Fuentes utilizadas

### 2.1 Contratos Kactus

- Archivo: `Data/Contratos_Kactus/Fuente_Oficial/CONSOLIDADOR_CONTRATOS_V0.0.0.xlsx`.
- Campos tomados: `N_Contrato`, `COD. CARGO`, `Tipo Contrato (Kactus)`,
  `Indicador Actividad`, `SEGMENTO`, estructura organizacional auxiliar e
  identificador del jefe inmediato, además del resto de campos contractuales
  utilizados en el corte.
- Regla de búsqueda contractual validada para este corte: **prioridad `A`
  (activo) y fallback `I` (inactivo) cuando no exista registro `A`** para la
  identificación buscada. Con esta prioridad el cruce alcanzó 2.605 de 2.605
  registros sin ambigüedades utilizadas.

> Esta regla de prioridad `A`/`I` queda documentada **únicamente en el contexto
> del HeadCount mensual**. No debe generalizarse al frente de
> INGRESOS/RETIROS, cuyas reglas de población son distintas y se analizan por
> separado.

### 2.2 Maestro de Empleados Kactus

- Familia: `Data/Maestro_Empleados_Kactus/` (consolidador oficial de
  `Fuente_Oficial/`).
- Campos tomados: fecha de nacimiento, estado civil, `Tipo Identificación` y el
  resto de campos demográficos y administrativos requeridos por la plantilla.

### 2.3 Datos Familiares Kactus

- Familia: `Data/Datos_Familiares_Kactus/`.
- Campo tomado: `HIJOS`.

### 2.4 Cuentas de Empleados Kactus

- Familia: `Data/Cuentas_Empleados_Kactus/`.
- Campos tomados: `AFC`, `AFP`, `CCF`, `EPS`.

Ninguna sección de esta spec incluye registros individuales de estas fuentes.

## 3. Carga base de septiembre

El bloque de septiembre se originó en el listado mensual de empleados:

`Data/HeadCount/01_Administración_de_Personal/2026/9 LISTADO DE EMPLEADOS X ANTIGUEDAD 30 DE SEPTIEMBRE 2026.xlsx`

Se cargaron 15 campos base con el siguiente mapeo conceptual:

| Origen (listado mensual) | Destino (`Consolidado2025`) |
|---|---|
| CEDULA | `ID` |
| NOMBRES | `NOMBRE` |
| APELLIDOS | `APELLIDO` |
| TIPO CONTRATO | `TIPO_CONTR` |
| FECHA INICIO | `F_INICIO` |
| FECHA FINAL | `F_VENCIM` |
| FECHA INGRESO | `F_INGRESO` |
| SUELDO BASICO | `SUELDO_B` |
| MANO DE OBRA | `MANO DE OBRA` |
| GENERO | `SEXO` |
| CARGO | `CARGO` |
| CENTRO DE COSTOS | `CCO` |
| EMPRESA | `GRUPO EMPRESA` (origen de la homologación) |
| CLASIFICACION | `CLASIFICACION` |
| FLEX | `FLEX` |

Campos de periodo del bloque: `MES = 09.Septiembre`, `AÑO = 2026`.

No se documentan salarios ni valores individuales. `SUELDO_B` existe en el
consolidado pero **no** se distribuye en los archivos mensuales (sección 8).

## 4. Reglas derivadas confirmadas

### 4.1 `ID_F_INICIO`

Llave de trazabilidad del registro contractual:

```
ID_F_INICIO = ID + F_INICIO
```

Validación final del corte: **2.605 / 2.605**, sin vacíos. En los archivos
mensuales la columna equivalente de `tblData` quedó completa hasta la última
fila (ver sección 9).

### 4.2 `SEGMENTO`

- Se obtuvo desde Contratos Kactus y quedó poblado **2.605 / 2.605**.
- Equivalencia hacia los archivos mensuales:
  `Consolidado2025[SEGMENTO]` → `Data[SEGMENTO- LEMCO]`.

### 4.3 Jefe inmediato

La correspondencia se resuelve en dos pasos:

1. tomar el **identificador del jefe** desde el origen contractual;
2. resolver sus datos descriptivos contra el catálogo correspondiente.

No se documentan nombres de jefes ni de colaboradores.

### 4.4 `HIJOS`

Resultado final conciliado contra la fuente de Datos Familiares y contra las
tablas dinámicas dependientes de los archivos mensuales. Agregado del corte:
1.197 colaboradores con hijos y 1.408 sin hijos, control 2.605.

### 4.5 `NIVEL_DE_CARGO` y `TIPO_DE_CARGO`

Se resolvieron con las tablas de homologación ya existentes en el proyecto.
Durante septiembre se incorporaron **4 cargos nuevos** a esa homologación:

| Cargo de origen | Homologación |
|---|---|
| COORDINADOR DE AUTOMATIZACION DE MARKETI | Coordinador |
| JEFE JURIDICO | Jefe |
| JEFE DE SERVICIO I | Jefe |
| COORDINADOR DE COMERCIO EXTERIOR | Coordinador |

Resultado del corte: **2.605 / 2.605**.

### 4.6 `DEPENDENCIA` y `AREA`

Regla principal: buscar primero la **combinación histórica exacta de
`CARGO_CCO`** y heredar su `DEPENDENCIA`/`AREA`.

Resultado de septiembre:

- 2.584 registros resueltos por histórico exacto;
- 21 registros correspondientes a **18 combinaciones nuevas** de `CARGO_CCO`,
  revisadas y decididas manualmente.

> Las decisiones manuales de estas 18 combinaciones son específicas de este
> corte. **No deben convertirse en reglas generales automáticas**; cada
> combinación nueva de un mes futuro requiere su propia revisión.

## 5. Homologación de empresa

Reglas aprobadas y aplicadas sobre `GRUPO EMPRESA` y `Nombre Empresa`:

| Origen | `GRUPO EMPRESA` | `Nombre Empresa` |
|---|---|---|
| CHALLENGER S.A.S. | CHALLENGER | CHALLENGER |
| FUNDACIÓN CHALLENGER | FUNDACIÓN CHALLENGER | FUNDACIÓN CHALLENGER |
| SKY FORWARDER | GRUPO SKY | SKY FORWARDER |
| SKY INDUSTRIAL | GRUPO SKY | SKY INDUSTRIAL |
| SKY LOGISTICA | GRUPO SKY | SKY LOGÍSTICA INTEGRAL |
| LEMCO SAS | LEMCO | LEMCO |
| LEMCO SALVIO | HABITEL HOTELS | LEMCO SALVIO |
| OPERADORA HABITEL SAS | HABITEL HOTELS | OPERADORA |

Para el origen `HABITEL SAS` la unidad hotelera se deriva de la clasificación
presente en el registro:

| Clasificación en origen | `Nombre Empresa` |
|---|---|
| PRIME | HABITEL PRIME |
| SELECT | HABITEL SELECT |
| NOMINA COMPARTIDA | HABITEL NÓMINA COMPARTIDA |

`LEMCO SAS` **no** se homologa como `HABITEL HOTELS`.

### Pendiente no bloqueante

**15 registros conservan `Nombre Empresa = 100`** hasta recibir la fuente
oficial de clasificación hotelera. No se infiere su unidad: `GRUPO EMPRESA` sí
quedó correctamente homologado como `HABITEL HOTELS`, de modo que ningún total
por grupo depende de este pendiente.

Resultado final por `GRUPO EMPRESA`: CHALLENGER 1.924, HABITEL HOTELS 326,
GRUPO SKY 254, LEMCO 97, FUNDACIÓN CHALLENGER 4. Control 2.605.

## 6. Correo corporativo

Fuente adicional del corte:

`Data/Correos_Corporativos/2026/09_Septiembre/Correos Grupo LEMCO.xlsx`

Regla aplicada, en orden:

1. match **exacto normalizado** del nombre del colaborador contra la fuente
   Office 365;
2. si no hay match, se conserva el **último correo corporativo real disponible**
   en el histórico del colaborador;
3. si no existe correo real, se asigna `N/R`;
4. los casos ambiguos se resolvieron manualmente, uno por uno;
5. cuando el colaborador conserva **dos cuentas autorizadas**, se registran
   separadas por `;` **sin espacios**.

No se usó coincidencia aproximada de nombres ni inferencia de identidades.

Resultado agregado del corte:

| Concepto | Registros |
|---|---:|
| Correo desde la fuente nueva o resolución manual | 766 |
| Correos reales recuperados del histórico | 59 |
| **Total con correo real** | **825** |
| `N/R` | 1.780 |
| Vacíos | 0 |

`N/R` no cuenta como correo corporativo válido.

> `Correo Corporativo` se **elimina actualmente en Power Query** dentro del
> modelo semántico. Mientras esa exclusión siga vigente, actualizar este campo
> no altera el reporte publicado.

Esta spec no incluye direcciones de correo.

## 7. `CM` y `PCD`

Estos dos campos **no bloquean el cierre** del corte.

Cierre provisional aplicado: se cruzó septiembre contra agosto de 2026 por `ID`,
con coincidencia exacta, usando agosto como última información disponible.

Regla:

- si la identificación existe en agosto, se conserva exactamente el valor de
  agosto;
- si el valor de agosto está vacío, septiembre queda vacío;
- si la identificación **no** existe en agosto, ambos campos quedan vacíos;
- no se usa `N/R`, ni valores por defecto, ni coincidencia aproximada, ni
  inferencia alguna de condición médica o de discapacidad.

Resultado agregado:

| Concepto | Registros |
|---|---:|
| Identificaciones de septiembre con antecedente en agosto | 2.496 |
| Identificaciones sin antecedente en agosto | 109 |
| `CM` con valor | 79 |
| `PCD` con valor | 28 |

Los 109 ingresos sin antecedente quedaron vacíos en ambos campos.

**Estado: PROVISIONAL.** La fuente oficial posterior podrá sustituir esta
fotografía sin reprocesar el resto del corte.

Tratamiento: son datos sensibles. No se documentan identidades ni valores
individuales, las fuentes no se versionan y `Data/` permanece ignorado por Git.

## 8. Archivos mensuales generados

Ruta: `Data/HeadCount/2026/09_Septiembre/`

| Archivo | Registros |
|---|---:|
| `HC_Septiembre_2026_Grupo Lemco - Sin Salario.xlsx` | 2.605 |
| `HC_Septiembre_2026_Lemco_Challenger_Fundacion - Sin Salario.xlsx` | 2.025 |
| `HC_Septiembre_2026_Grupo SKY - Sin Salario.xlsx` | 254 |
| `HC_Septiembre_2026_Unidad Hotelera - Sin Salario.xlsx` | 326 |

Control de partición: `2.025 + 254 + 326 = 2.605`.

Los tres archivos por unidad forman una **partición exacta** del archivo
completo, verificada por identificación:

- intersecciones entre unidades: **0**
- identificaciones faltantes: **0**
- identificaciones adicionales: **0**

La suma de las distribuciones de los tres archivos reproduce la del archivo
completo en `HIJOS`, `TIPO_CONTR`, `SEXO`, `RANGO DE EDAD`,
`RANGO ANTIGÜEDAD`, `GENERACIÓN` y `AGRUPACIÓN EMPRESA`.

## 9. Contrato estructural de los archivos mensuales

Estructura heredada del mes anterior, sin cambios:

- **6 hojas**: `Helper`, `Listas`, `Informe`, `Tbls_Hijos`,
  `Tbls_Dependencia_Area`, `Data`.
- **56 columnas** en la hoja `Data`, dentro de la tabla estructurada `tblData`.
- Archivos `Sin Salario`: `SUELDO_B` **no** se distribuye en estos HC.
- Encabezados de `tblData` idénticos en nombre y orden a los del mes anterior.

Columnas calculadas propias de `tblData`:

| Columna | Naturaleza |
|---|---|
| `Antigüedad` | fórmula |
| `Rango Antigüedad` | fórmula |
| `EDAD` | fórmula |
| `RANGO DE EDAD` | fórmula |
| `Año Nac` | fórmula |
| `Generación` | fórmula |
| `ID_F_INICIO` | fórmula (`ID` + `F_INICIO`) |
| `CARGO_CCO` | fórmula |

Validación final: las ocho columnas quedaron **completas hasta la última fila**
en los cuatro archivos, sin celdas vacías ni valores estáticos intercalados.

### Deuda heredada de plantilla (no corregida en este cierre)

1. `Antigüedad` y `EDAD` se calculan con `TODAY()`: **el corte no queda
   congelado** en estos archivos y sus rangos derivados se desplazan con el
   tiempo.
2. La fecha visual del `Informe` también usa `TODAY()`, por lo que no muestra la
   fecha de corte del periodo.
3. El gráfico de rango de edad del `Informe` no incluye la categoría
   `Menores De 18 Años`; hoy no se nota porque vale cero, pero quedaría fuera
   del gráfico si algún mes deja de serlo.
4. El título del `Informe` es genérico y heredado: muestra el nombre del grupo
   completo en los cuatro archivos.

Estas observaciones **no bloquearon septiembre** y **no se corrigieron** en este
cierre. Su corrección requiere decisión y alcance propios.

## 10. Auditoría de `Informe` y `Tbls_Hijos`

Resultado: **PASS** en los cuatro archivos.

Validaciones ejecutadas:

- `tblData` termina en la última fila real; **0 filas huérfanas** por debajo de
  la tabla.
- **0 identificaciones duplicadas** por archivo.
- **0 errores estructurales** y 0 celdas en error en las hojas auditadas.
- Fórmulas completas en las ocho columnas calculadas.
- `Tbls_Hijos` reconciliado contra `Data`: la dinámica no contiene fórmulas, su
  origen es `tblData` y su total general coincide con el conteo de `Data`.
- `Informe` validado de forma **independiente**: cada indicador se recalculó
  directamente desde `Data` en lugar de aceptarlo por coincidir con una tabla
  dinámica. **0 diferencias** en los cuatro archivos.
- Totales y participaciones cierran: cada distribución suma el total del archivo
  y los porcentajes suman 1.
- Partición entre unidades reconciliada (sección 8).

Agregado del corte, a título de control: `HIJOS` cierra en 2.605 con 1.197 «con
hijos» y 1.408 «sin hijos»; `TIPO_CONTR`, `SEXO` y `RANGO DE EDAD` también
cierran en 2.605 por archivo.

## 11. Estado de Power BI

Power BI **fue actualizado y publicado** con el HeadCount de septiembre.

Validación funcional realizada sobre el reporte publicado:

- septiembre = **2.605**;
- distribución por `GRUPO EMPRESA` coincidente con la fuente;
- visuales cargados sin errores;
- fecha de actualización visible: **05/10/2026**.

Aclaraciones necesarias para no sobredeclarar el estado:

- `Correo Corporativo` **no entra** actualmente al modelo: Power Query lo
  elimina.
- `PCD` **se elimina** actualmente en Power Query.
- `CM` **sí existe** en el modelo, pero la actualización provisional de `CM` y
  `PCD` descrita en la sección 7 se ejecutó **después** de la publicación.

Por decisión funcional del usuario, esa actualización posterior **no bloquea
este cierre** y podrá publicarse más adelante junto con su fuente oficial.

> No debe afirmarse que el Power BI publicado contiene el último cruce
> provisional de `CM`.

## 12. Respaldos

Política aplicada durante el corte:

- se creó un respaldo temporal **antes de cada bloque crítico** de escritura,
  verificando SHA-256 entre origen y copia;
- los respaldos viven **fuera de Git**, bajo
  `C:\Respaldos\HeadCount_Septiembre_2026\`;
- funcionan como puntos de recuperación del corte;
- **no deben convertirse en artefactos versionados** ni moverse al repositorio;
- su eliminación queda pendiente de una limpieza posterior **explícitamente
  autorizada**, una vez el corte esté definitivamente cerrado.

Aprendizaje operativo confirmado en este corte: con **AutoSave** activo sobre
OneDrive, el respaldo previo es el único punto real de recuperación, porque
Excel puede persistir cambios aunque el proceso cierre el libro sin guardar.

## 13. Privacidad

Aplica `Docs/SECURITY_AND_PRIVACY.md`.

Esta spec no contiene identificaciones, nombres, correos, salarios, datos
familiares individuales, información médica individual ni información de
discapacidad individual. Solo agregados y reglas.

Controles vigentes:

- `Data/` permanece ignorado por Git; ninguna de las fuentes del corte se
  versiona.
- Los diagnósticos y validaciones del corte se ejecutaron sobre metadatos,
  encabezados, tipos y conteos agregados.
- `CM` y `PCD` se tratan como datos sensibles: ni los valores ni las identidades
  asociadas se documentan.

## 14. Pendientes y excepciones vigentes

| Pendiente | Tipo | Bloquea el cierre |
|---|---|---|
| 15 registros con `Nombre Empresa = 100`, a la espera de la fuente oficial de clasificación hotelera | Datos | No |
| `CM` y `PCD` en estado provisional heredado de agosto | Datos sensibles | No |
| Publicar el cruce provisional de `CM`/`PCD` en Power BI | Operación | No |
| Deuda de plantilla: `TODAY()` en `Antigüedad`/`EDAD`/fecha visual, categoría `Menores De 18 Años`, título genérico | Plantilla | No |
| INGRESOS y RETIROS de septiembre en `PptovsReal.xlsx` | Datos | Fuera de alcance de esta spec |
| Automatización del procedimiento mensual | Automatización | No autorizada |

## 15. Procedimiento reutilizable

El procedimiento mensual, en orden ejecutable y sin depender de septiembre como
caso particular, quedó documentado en
[Docs/RUNBOOK.md](../Docs/RUNBOOK.md#11-procedimiento-mensual-de-actualización-de-headcount).
