# Mapeo de campos Contratos Kactus

Fecha: 2026-08-03

Estado: **borrador tecnico**, pendiente de aprobacion funcional. El analisis y el mapeo de campos estan completos y las reglas funcionales estan identificadas y clasificadas, pero ninguna decision de esta Spec esta aprobada todavia. No autoriza iniciar la construccion del programa Python de transformacion.

Nota de rama: este documento se elaboro originalmente en la rama `docs/roadmap-backlog`, que diverge de `origin/main` y no debe fusionarse directamente. Los cambios validos (este archivo y la entrada correspondiente de `Docs/CHANGELOG.md`) se trasladaron mediante cherry-pick controlado a la rama limpia `docs/kactus-mapeo-campos`, creada desde `origin/main`. `origin/main` ya incluye la documentacion de gobierno y validacion de rutas de Contratos Kactus en `Docs/DATA_PIPELINE.md` (commits `e384746`, `612ddc5`); este documento es complementario (mapeo de campos) y no la reemplaza.

No incluye datos personales: nombres, identificaciones, salarios ni valores de fila. Todo lo documentado abajo es estructura (hojas, encabezados, tipos inferidos, formulas de columnas calculadas).

## 1. Fuentes revisadas

| Fuente | Ruta | Alcance de lectura |
|---|---|---|
| 9 archivos Kactus vigentes | `Data/Contratos_Kactus/Insumos_Vigentes/*.xlsx` | Hoja `KactuS - KNmContr`, fila de encabezados y tipos de la fila 2 |
| Consolidador oficial | `Data/Contratos_Kactus/Fuente_Oficial/CONSOLIDADOR_CONTRATOS_V0.0.0.xlsx` | Estructura de hojas, tabla `Fact_Contrataciones` (via metadatos del Data Model / pivot cache, no via valores de celda) |
| Origen INGRESOS/RETIROS | `Data/HeadCount/PptovsReal.xlsx` | Hojas `INGRESOS` y `RETIROS`: encabezados, tipos de la fila 2, formulas de columnas calculadas |
| Spec previa | `Specs/0015_mapeo_campos_contratos_kactus.md` | Version anterior: plantilla vacia con las mismas tablas y la lista de reglas pendientes; se completa en este documento |

`PptovsReal.xlsx` se localizo en `Data/HeadCount/PptovsReal.xlsx` (verificado por busqueda directa en disco; no depende de la rama Git porque `Data/` no esta versionado).

No se recorrio `Data/Contratos_Kactus/Historico/` ni archivos temporales `~$*.xlsx`, conforme al alcance autorizado.

**Hojas adicionales `Tbl_Ingresos` y `Tbl_Retiros` (inspeccionadas por autorización posterior, solo metadatos y encabezados):**

Ambas hojas son **tablas dinámicas de Excel** construidas sobre `INGRESOS` y `RETIROS`, no tablas planas de datos. Evidencia estructural (sin valores personales): no tienen fila de encabezados en el sentido de `INGRESOS`/`RETIROS`; en su lugar muestran los artefactos típicos de una tabla dinámica — `Etiquetas de fila`, `Etiquetas de columna`, `(Varios elementos)`, `(Todas)`, `Suma de Afecta calidad`, `% Calidad`, `Total 2026`, `Total general`. Los filtros de página detectados son: `Años (Fecha Inicio)`, `Grupo Empresarial`, `Descripción Estado Cargo` en `Tbl_Ingresos`; `Cargo`, `Detalle` en `Tbl_Retiros`. Ninguna de las dos define una Tabla Excel (`ws.tables` vacío).

**Conclusión**: son **salidas derivadas** (paneles/resúmenes de reporte agregados por mes y empresa), no fuentes auxiliares, no tablas de homologación y no están referenciadas por ninguna de las fórmulas de columnas calculadas revisadas en las secciones 3 y 4. No son relevantes para el mapeo de campos ni para la futura automatización de carga; se excluyen del alcance de esta Spec.

## 2. Inventario de encabezados

### 2.1 Archivos Kactus vigentes (9 archivos)

Los 9 archivos tienen **estructura identica**: misma hoja (`KactuS - KNmContr`), mismos **138 encabezados**, mismo orden. Confirmado por comparacion directa fila 1 de los 9 libros.

| Archivo | Filas (incl. encabezado) | Columnas |
|---|---:|---:|
| CHALLENGER S.A.S..xlsx | 27.628 | 138 |
| FUNDACION CHALLENGER.xlsx | 6.656 | 138 |
| HABITEL S.A.S..xlsx | 3.180 | 138 |
| LEMCO SAS.xlsx | 475 | 138 |
| OPERADORA HABITEL SAS.xlsx | 139 | 138 |
| SKY ELECTRONICS ZONA FRANCA S.A.S..xlsx | 1 (solo encabezado, sin filas de datos actualmente) | 138 |
| SKY FORWARDER S.A.S..xlsx | 924 | 138 |
| SKY INDUSTRIAL.xlsx | 300 | 138 |
| SKY LOGISTICA INTEGRAL.xlsx | 539 | 138 |

Los 138 encabezados (presentes en las 9 empresas por igual):

```text
Código Empresa, Identificación, Nombres, Apellidos, Nro. Contrato, Tipo Contrato,
Remuneración, % Remuneración, Turnos, Fin de Semana, Código Turno, Grupo Turno,
Tipo Salario, Fecha Contrato, Fecha Inicio, Fecha Vencimiento, Tipo Retención,
Indicador Sindicato, Cargo, Estado Funcionario, Centro de Trabajo, Centro de Costo,
Forma de Pago, Días Parciales, Indicador Actividad, Fecha Nombramiento, Resolución,
Fecha Posesión, Acta / Resolución, Último Movimiento, Resolución Retiro,
Fecha Novedad, Clase de Nómina, Grupo de Prototipos, Tipo Pensión,
Régimen Cesantías, Fecha Cesantías, Fecha Vacaciones, Fecha Antigüedad,
Sueldo Básico, Fecha Sueldo, Sueldo Anterior, Concepto Fijo 1,
Fecha Concepto Fijo 1, Antigüedad Fijo1, Concepto Fijo 2, Fecha Concepto Fijo 2,
Antigüedad Fijo2, Concepto Fijo 3, Fecha Concepto Fijo 3, Antigüedad Fijo3, Árbol,
Aplicación de Árbol, Nivel 1, Nombre Nivel 1, Nivel 2, Nombre Nivel 2, Nivel 3,
Nombre Nivel 3, Nivel 4, Nombre Nivel 4, Nivel 5, Nombre Nivel 5, Nivel 6,
Nombre Nivel 6, Nivel 7, Nombre Nivel 7, Códigos de Nivel, Identificador de Arbol,
Detalle, Secuencial Imagen, Área de Riesgo, Folio Contrato, Compensación Flexible,
Valor Compensación, Funcionario/Reporta, Fecha Resolución,
Tipo de Cotizante/Pensión, Tipo de Pensionado, Pensión Compartida, Estado Pensión,
Subtipo Cotizante, Causal de la suspensión o rectivación del pago de la mesada
pensional, Id Planta, Secuencial WorkFlow, % Invalidez, Fecha Revisión,
Cargo Relacionado, Días Contrato Fijo, Modalidad Pensión, Observaciones,
Sucursal, Consecutivo Suc., Proyecto, Consecutivo Proy., Área, Consecutivo Área,
Fecha Novedad Distribución, Tipo de pago, Sustitución Patronal,
Vinculación Laboral, Tipo de Contrato Fijo,
Extranjero No Obligado a Cotizar en Pensión, Nombre Empresa, Código Interno,
Descripción Grupo de Prototipos, Nombre Funcionario, Apellidos Funcionarios,
Código Reporta, Descripción Estado Cargo, Descripción Cargo, Nombre Centro Costo,
Nombre Centro Trabajo, Nombre Área, Descripción Grupo Prototipos,
Descripción Clase Nómina, Motivo Movimiento, Nombre Turno,
Descripción Grupo Turnos, Nombre Cargo Relacionado, Descripción de Sucursal,
Descripción Proyecto, Descripción de Área, Fecha de Sueldo, % Prima Anti,
Clasificación Catedra, Gastos de Personal, Pago en Dólares,
Cesantías Congeladas, Beneficios Flexibles,
Sentencia Judicial Planilla Integradora, Ejecución del Contrato, Modalidades,
Fuero Laboral, Descripción Fuero Laboral, Otro Fuero Laboral,
Fecha Inicio Fuero Laboral, Fecha Final Fuero Laboral
```

Tipos de dato inferidos (muestra de la fila 2 de cada archivo, no se muestran valores): mezcla de `int`, `str`, `datetime` y campos vacios (`vacio`) segun la empresa — es esperable que varios campos esten sistematicamente vacios en empresas pequenas (p. ej. Operadora Habitel, Sky Industrial) porque corresponden a atributos opcionales de Kactus (pension, beneficios flexibles, fuero laboral, etc.).

### 2.2 Consolidador oficial — `Fact_Contrataciones`

El libro `CONSOLIDADOR_CONTRATOS_V0.0.0.xlsx` no expone `Fact_Contrataciones` como una hoja con celdas planas: las hojas visibles (`Fact_Contrataciones (A)`, `Fact_Contrataciones (I)`) son salidas de tabla dinamica (crosstab por empresa/año), no la tabla plana. Los encabezados reales de `Fact_Contrataciones` se extrajeron de los metadatos del Data Model (`xl/pivotCache/pivotCacheDefinition10.xml`, fuente `ThisWorkbookDataModel`), que confirma **10 tablas cargadas al modelo**: las 9 consultas fuente (una por empresa, mismos 138 campos que la seccion 2.1) mas `Fact_Contrataciones` como tabla propia.

`Fact_Contrataciones` tiene **146 campos**: los mismos 138 de las fuentes Kactus, mas 8 campos de jerarquia de fecha generados automaticamente por Excel al detectar columnas de fecha en el modelo (no son campos de negocio nuevos):

```text
Fecha Inicio (año), Fecha Inicio (trimestre), Fecha Inicio (mes),
Fecha Vencimiento (año), Fecha Vencimiento (trimestre), Fecha Vencimiento (mes),
Fecha Inicio (índice de meses), Fecha Vencimiento (índice de meses)
```

Conclusion tecnica: `Fact_Contrataciones` es consistente con una combinacion (append/Table.Combine) de las 9 consultas fuente sin transformacion de columnas adicional — no agrega ni quita campos de negocio respecto a los archivos vigentes de la seccion 2.1. Esto coincide con lo documentado en `origin/main` (`Docs/DATA_PIPELINE.md`: "Consulta consolidada: Fact_Contrataciones, construida mediante combinacion de las consultas fuente").

Consultas fuente confirmadas (nombres de conexion en `xl/connections.xml`): `CHALLENGER_SAS`, `FUNDACION_CHALLENGER`, `HABITEL_SAS`, `LEMCO_SAS`, `OPERADORA_HABITEL_SAS`, `SKY_ELECTRONICS_ZONA_FRANCA_SAS`, `SKY_FORWARDER_SAS`, `SKY_INDUSTRIAL`, `SKY_LOGISTICA_INTEGRAL`.

### 2.3 `PptovsReal.xlsx` — hoja `INGRESOS`

28 columnas, 4.724 filas (incl. encabezado):

```text
Grupo Empresarial, Empresa, Identificación, Fecha Contrato, Fecha Inicio, Año,
No Mes, Mes, Nombres, Apellidos, Descripción Estado Cargo, Descripción Cargo,
Dependencia, Área, Nombre Centro Costo, Motivo Movimiento, cod, Ind_Calidad,
Ingreso_2025, última fecha de vencimiento_Indicador, última fecha de vencimiento,
Ultimo Detalle, Validación, Meses reales de permanencia, Afecta calidad,
CARGO_CCO, Identificación_Fecha Inicio, %
```

### 2.4 `PptovsReal.xlsx` — hoja `RETIROS`

33 columnas, 3.744 filas (incl. encabezado):

```text
Grupo empresarial, Empresa, Identificación, No. Contrato, Nombres, Apellidos, TC,
Cargo, Nombre Centro Costo, Fecha Inicio, Fecha Vencimiento, Año, Mes Num, Mes,
Meses de permanencia, Detalle, OBSERVACION, Dependencia, Área, Salario,
Clase de nómina, Jefe Inmediato, Centro de Trabajo, [Nombre Nivel 2],
[Nombre Nivel 3], CARGO_CCO, DEPENDENCIA_CONSOLIDADO, AREA_CONSOLIDADO, %,
V_DEPENDENCIA, V_AREA, Nivel, Periodo
```

## 3. Mapeo de INGRESOS

| Campo origen Kactus | Campo destino INGRESOS | Transformación requerida | Obligatorio | Observaciones |
|---|---|---|---|---|
| (sin origen directo — requiere homologación) | Grupo Empresarial | Homologar empresa | Sí | No existe un campo "Grupo Empresarial" en Kactus. Requiere tabla de homologación Empresa→Grupo (patrón similar al usado en Empresas del PBIP). Sin origen identificado en el alcance revisado. |
| Nombre Empresa | Empresa | Normalizar empresa | Sí | Mapeo con transformación (limpieza de espacios/formato de razón social). |
| Identificación | Identificación | Convertir identificación a texto | Sí | Mapeo directo; tipo inferido ya es entero en ambos lados, pero se recomienda forzar texto para evitar pérdida de ceros a la izquierda. |
| Fecha Contrato | Fecha Contrato | Convertir fechas | Sí | Mapeo directo. |
| Fecha Inicio | Fecha Inicio | Convertir fechas | Sí | Mapeo directo. |
| Fecha Inicio | Año | Derivar año | Sí | Campo derivado (`YEAR(Fecha Inicio)`, inferido por convención del archivo; no se confirmó fórmula exacta en la celda inspeccionada). |
| Fecha Inicio | No Mes | Derivar mes | Sí | Campo derivado — fórmula confirmada: `=TEXT(FechaInicio,"mm")`. |
| Fecha Inicio | Mes | Derivar mes | Sí | Campo derivado por convención; no se detectó fórmula en la celda inspeccionada (posible valor pegado o resultado de otro proceso). |
| Nombres | Nombres | — | Sí | Mapeo directo. |
| Apellidos | Apellidos | — | Sí | Mapeo directo. |
| Descripción Estado Cargo | Descripción Estado Cargo | — | Sí | Mapeo directo (coincidencia exacta de nombre). |
| Descripción Cargo | Descripción Cargo | — | Sí | Mapeo directo (coincidencia exacta de nombre). |
| Nombre Nivel 1..7 / Nombre Centro Costo / Nombre Área (candidatos) | Dependencia | Homologar estructura organizacional | Sí | Pendiente de decisión funcional — varios campos candidatos en Kactus (jerarquía de niveles 1-7), sin campo llamado literalmente "Dependencia". |
| Área / Nombre Área | Área | Definir código vs. descripción | Sí | Pendiente de decisión funcional — Kactus tiene ambos "Área" (código) y "Nombre Área" (descripción); no está confirmado cuál alimenta este campo. |
| Nombre Centro Costo | Nombre Centro Costo | — | Sí | Mapeo directo (coincidencia exacta de nombre). |
| Motivo Movimiento | Motivo Movimiento | — | No | Mapeo directo (coincidencia exacta de nombre); en Kactus es un campo de movimiento general, uso específico en INGRESOS por confirmar. |
| Identificación + Año + Nombres | cod | Derivar clave compuesta | Sí | Campo derivado — fórmula confirmada: `=CONCAT(Identificación,"-",Año,"-",Nombres)`. Candidata a clave para evitar duplicados. |
| (cruce con RETIROS) | Ind_Calidad | Control de valores vacíos / cruce | No | Campo derivado — fórmula confirmada: compara `cod` contra una columna de `RETIROS` vía XLOOKUP. Ver riesgo en sección 10 (la columna de RETIROS referenciada es `OBSERVACION`, con un patrón de concatenación distinto al de `cod`; requiere revisión humana). |
| Fecha Inicio | Ingreso_2025 | Derivar año, valor fijo 2025 | No | Campo derivado — fórmula confirmada: `=IF(YEAR(FechaInicio)=2025,1,0)`. **Año hardcodeado**, ver riesgo en sección 10. |
| Identificación + Fecha Inicio + RETIROS | última fecha de vencimiento_Indicador | Cruce condicional con RETIROS | No | Campo derivado — fórmula MAXIFS confirmada, con lista de exclusión de valores de `RETIROS!Cargo` (aprendiz SENA, practicante) y `RETIROS!Detalle` (reingreso, fallecimiento, pensión/jubilación, renuncia, abandono, mutuo acuerdo, cesión, vencimiento, fin de obra, contrato definitivo, terminación contrato/definitivo, sin justa causa). Esta es la regla más completa encontrada para "retiro real" — ver sección 6. |
| Identificación + Fecha Inicio + RETIROS | última fecha de vencimiento | Cruce con RETIROS | No | Campo derivado — fórmula MAXIFS simple confirmada, sin exclusiones. |
| Detalle (candidato) | Ultimo Detalle | Homologar | No | No se detectó fórmula en la celda inspeccionada. Podría relacionarse con Kactus "Detalle" o ser resultado de un cruce externo. Pendiente de decisión funcional. |
| (derivado de última fecha de vencimiento_Indicador) | Validación | Control lógico | No | Campo derivado — fórmula confirmada: compara `última fecha de vencimiento_Indicador >= Fecha Inicio`. |
| (derivado) | Meses reales de permanencia | Cálculo de meses | No | Campo derivado — fórmula confirmada: `DATEDIF(Fecha Inicio, última fecha de vencimiento_Indicador, "m")`. |
| Fecha Inicio (año=2025) | Afecta calidad | Control de calidad, valor fijo 2025 | No | Campo derivado — fórmula confirmada: marca 1 si el ingreso es de 2025 y permaneció ≤4 meses. **Año hardcodeado**, mismo riesgo que Ingreso_2025. |
| Descripción Cargo + Nombre Centro Costo | CARGO_CCO | Derivar clave compuesta | No | Campo derivado — fórmula confirmada: `CONCAT(TRIM(Descripción Cargo)," - ",TRIM(Nombre Centro Costo))`. |
| Identificación + Fecha Inicio | Identificación_Fecha Inicio | Derivar clave compuesta | Sí | Campo derivado — fórmula confirmada: `CONCAT(Identificación,FechaInicio)`. Candidata fuerte a clave para evitar duplicados en INGRESOS. |
| (sin origen identificado) | % | — | No | No se detectó fórmula ni propósito claro en la celda inspeccionada. Sin origen identificado — nombre de columna no autodescriptivo. |

## 4. Mapeo de RETIROS

| Campo origen Kactus | Campo destino RETIROS | Transformación requerida | Obligatorio | Observaciones |
|---|---|---|---|---|
| (sin origen directo — requiere homologación) | Grupo empresarial | Homologar empresa | Sí | Mismo caso que INGRESOS: sin origen identificado en Kactus. |
| Nombre Empresa | Empresa | Normalizar empresa | Sí | Mapeo con transformación. |
| Identificación | Identificación | Convertir identificación a texto | Sí | Mapeo directo. |
| Nro. Contrato | No. Contrato | — | No | Mapeo directo (diferencia menor de nombre: "Nro." vs "No."). |
| Nombres | Nombres | — | Sí | Mapeo directo. |
| Apellidos | Apellidos | — | Sí | Mapeo directo. |
| Tipo Contrato | TC | Homologar tipo de contrato | No | Mapeo con transformación — "TC" se infiere como abreviatura de "Tipo Contrato"; no confirmado por coincidencia exacta de nombre. Pendiente de decisión funcional. |
| Cargo / Descripción Cargo | Cargo | Definir código vs. descripción | Sí | Dos campos candidatos en Kactus ("Cargo" código, "Descripción Cargo" texto); pendiente de decisión funcional. |
| Nombre Centro Costo | Nombre Centro Costo | — | Sí | Mapeo directo (coincidencia exacta de nombre). |
| Fecha Inicio | Fecha Inicio | Convertir fechas | Sí | Mapeo directo. |
| Fecha Vencimiento | Fecha Vencimiento | Convertir fechas | Sí | Mapeo directo. |
| Fecha Inicio o Fecha Vencimiento | Año | Derivar año | Sí | Campo derivado; no se confirmó cuál fecha base usa la fórmula (no se detectó fórmula en la celda inspeccionada). Pendiente de decisión funcional. |
| Fecha Inicio o Fecha Vencimiento | Mes Num | Derivar mes | Sí | Campo derivado; misma observación que Año. |
| Fecha Inicio o Fecha Vencimiento | Mes | Derivar mes | Sí | Campo derivado; no se detectó fórmula en la celda inspeccionada. |
| Fecha Inicio + Fecha Vencimiento | Meses de permanencia | Cálculo de meses | No | Campo derivado — fórmula confirmada: `YEARFRAC(Fecha Inicio, Fecha Vencimiento)*12`. |
| Detalle | Detalle | — | Sí | Mapeo directo (coincidencia exacta de nombre); es el campo más específico para clasificar el motivo real del retiro (ver sección 6). |
| Identificación + Fecha Inicio (derivado) | OBSERVACION | Derivar clave compuesta | No | Campo derivado — fórmula confirmada: `CONCAT(Identificación,"-",YEAR(FechaInicio),"-",MONTH(FechaInicio),".",NombreMes)`. |
| Nombre Nivel 1..7 / Nombre Centro Costo / Nombre Área (candidatos) | Dependencia | Homologar estructura organizacional | Sí | Pendiente de decisión funcional, igual que en INGRESOS. |
| Área / Nombre Área | Área | Definir código vs. descripción | Sí | Pendiente de decisión funcional, igual que en INGRESOS. |
| Sueldo Básico | Salario | — | No | Mapeo directo. **Campo de dato personal sensible** (ver `SECURITY_AND_PRIVACY.md`); no se inspeccionaron valores. |
| Clase de Nómina | Clase de nómina | — | No | Mapeo directo (coincidencia de nombre, solo difiere en mayúsculas). |
| Funcionario/Reporta o Código Reporta | Jefe Inmediato | Homologar | No | Pendiente de decisión funcional — dos campos candidatos en Kactus. |
| Centro de Trabajo | Centro de Trabajo | — | No | Mapeo directo (coincidencia exacta de nombre). |
| Nombre Nivel 2 | [Nombre Nivel 2] | — | No | Mapeo directo (coincidencia exacta de nombre; el destino usa corchetes literales en el encabezado). |
| Nombre Nivel 3 | [Nombre Nivel 3] | — | No | Mapeo directo (coincidencia exacta de nombre). |
| Cargo + Nombre Centro Costo | CARGO_CCO | Derivar clave compuesta | No | Campo derivado — fórmula confirmada: `CONCAT(TRIM(Cargo)," - ",TRIM(Nombre Centro Costo))`. |
| (sin origen identificado en Kactus) | DEPENDENCIA_CONSOLIDADO | — | No | Sin origen identificado en Kactus; se usa como comparador en la fórmula de `V_DEPENDENCIA`, sugiere una fuente de homologación externa (posiblemente `PLANTA DE PERSONAL` u otra tabla del PBIP, fuera del alcance de esta Spec). |
| (sin origen identificado en Kactus) | AREA_CONSOLIDADO | — | No | Igual que DEPENDENCIA_CONSOLIDADO. |
| (sin origen identificado) | % | — | No | No se detectó fórmula ni propósito claro. Sin origen identificado. |
| (derivado, comparación) | V_DEPENDENCIA | Control lógico | No | Campo derivado — fórmula confirmada: compara `AREA_CONSOLIDADO/DEPENDENCIA_CONSOLIDADO` contra `Dependencia`. Es un campo de auditoría, no de negocio. |
| (derivado, comparación) | V_AREA | Control lógico | No | Campo derivado — fórmula confirmada, mismo patrón que V_DEPENDENCIA para Área. |
| Nivel 1..7 (candidato) | Nivel | Homologar | No | Pendiente de decisión funcional — Kactus tiene 7 niveles jerárquicos distintos; no está confirmado cuál alimenta este campo único. |
| Año + Mes (derivado) | Periodo | Derivar periodo | No | Campo derivado por convención; no se detectó fórmula en la celda inspeccionada. |

## 5. Transformaciones necesarias (resumen transversal)

| Transformación | Aplica a | Estado |
|---|---|---|
| Convertir identificación a texto | Identificación (INGRESOS y RETIROS) | Recomendada, no confirmada como obligatoria por el archivo actual (ambos lados ya son tipo entero) |
| Convertir fechas | Fecha Contrato, Fecha Inicio, Fecha Vencimiento | Directa, tipos ya coinciden (`datetime`) |
| Limpiar espacios | Empresa, Cargo, Nombre Centro Costo (usados en claves compuestas) | Confirmada por uso de `TRIM()` en fórmulas existentes (CARGO_CCO) |
| Normalizar empresa | Nombre Empresa → Empresa | Requerida, sin regla de normalización confirmada en el alcance revisado |
| Homologar tipo de contrato | Tipo Contrato → TC | Pendiente de decisión funcional |
| Derivar año / mes | Fecha Inicio o Fecha Vencimiento → Año, Mes, Mes Num, No Mes, Periodo | Parcialmente confirmada (No Mes en INGRESOS); el resto son candidatos por convención |
| Controlar valores vacíos | Identificación, Dependencia, Área, Grupo Empresarial | Pendiente de definir regla (ver sección 8) |

## 6. Campos sin correspondencia directa en Kactus

- `Grupo Empresarial` / `Grupo empresarial` (INGRESOS y RETIROS): no existe en Kactus; requiere tabla de homologación Empresa→Grupo.
- `DEPENDENCIA_CONSOLIDADO` y `AREA_CONSOLIDADO` (RETIROS): sin origen en Kactus; probablemente provienen de una fuente de homologación externa al alcance de esta Spec.
- `Dependencia` (INGRESOS y RETIROS): sin campo literal "Dependencia" en Kactus; los candidatos son los 7 niveles jerárquicos.
- `%` (INGRESOS y RETIROS): sin propósito identificable desde la estructura.
- `Ultimo Detalle` (INGRESOS): sin fórmula confirmada, sin coincidencia exacta de nombre con Kactus.

## 7. Reglas confirmadas por estructura o fórmula existente

1. **Criterio de "retiro real" en INGRESOS** (fórmula `última fecha de vencimiento_Indicador`): busca en `RETIROS` la fecha de vencimiento máxima para la misma Identificación y Fecha Inicio, **excluyendo** cargos que contengan "APRENDIZ SENA" o "PRACTICANTE", y **excluyendo** retiros cuyo `Detalle` contenga: REINGRESO, FALLECIMIENTO, PENSION/JUBILACION, RENUNCIA, ABANDONO, MUTUO ACUERDO, CESION, VENCIMIENTO, FIN DE OBRA, CONTRATO DEFINITIVO, TERMINACION CONTRATO/DEFINITIVO, SIN JUSTA CAUSA.
2. **Clave compuesta ya usada en INGRESOS**: `cod` = Identificación-Año-Nombres; `Identificación_Fecha Inicio` = Identificación+Fecha Inicio. Ambas ya existen como candidatas a evitar duplicados.
3. **Persona con varios contratos**: no hay restricción de unicidad por Identificación en ninguna de las dos hojas; la estructura permite múltiples filas por la misma Identificación.
4. **Cesión y Reingreso ya existen como categorías de negocio**: aparecen como valores esperados dentro de `RETIROS!Detalle` (usados en la exclusión de la regla 1), aunque no hay fórmula que los detecte automáticamente desde Kactus.
5. **Campos de auditoría existentes**: `V_DEPENDENCIA` y `V_AREA` en RETIROS ya comparan los campos consolidados contra los operativos — son un precedente de patrón de validación de homologación.

## 8. Reglas pendientes de aprobación humana

Se documentan **10 reglas pendientes de aprobación humana o propuesta técnica** (Criterio de ingreso, Reingreso, Prórroga, Cambio de contrato, Contrato anulado, Cesión, Retiro sin motivo, Empresa no homologada, Identificación vacía y Clave para evitar duplicados en RETIROS), más 1 fila adicional (Clave para evitar duplicados en INGRESOS) que se incluye en la misma tabla por continuidad temática pero que no es una regla pendiente en sentido estricto: ya tiene precedente confirmado por fórmula existente en el archivo (sección 7). Ninguna de las 11 filas se implementó ni se aprobó en este documento:

| Regla | Clasificación | Propuesta técnica (si aplica) |
|---|---|---|
| Criterio de ingreso | Pendiente de aprobación humana | No se encontró una fórmula que filtre "qué fila cuenta como ingreso"; INGRESOS parece ser la tabla completa de inicios de contrato. |
| Reingreso (detección automática) | Propuesta técnica | Identificación repetida con nueva Fecha Inicio posterior a una Fecha Vencimiento previa de la misma Identificación. |
| Prórroga | Pendiente de aprobación humana | Sin evidencia de fórmula o campo. Propuesta técnica posible: mismo Nro. Contrato con Fecha Vencimiento extendida respecto a un registro previo. |
| Cambio de contrato | Pendiente de aprobación humana | Sin evidencia encontrada. |
| Contrato anulado | Pendiente de aprobación humana | Candidatos "Estado Funcionario" o "Indicador Actividad" en Kactus, sin poder confirmar valores (dato restringido). |
| Cesión (detección automática) | Propuesta técnica | Usar `RETIROS!Detalle = "CESION"` como bandera directa (ya existe como valor esperado, ver sección 7). |
| Retiro sin motivo | Propuesta técnica | Contar filas de RETIROS con `Detalle` vacío como indicador de calidad; no se puede confirmar sin inspeccionar valores. |
| Empresa no homologada | Pendiente de aprobación humana | Depende de que exista y se defina la tabla Empresa→Grupo Empresarial (sección 6). |
| Identificación vacía | Pendiente de aprobación humana | Falta definir tratamiento (excluir, marcar, o bloquear la carga). |
| Clave para evitar duplicados en INGRESOS | Propuesta técnica (con precedente) | Reutilizar `Identificación_Fecha Inicio`, ya existente en el archivo. |
| Clave para evitar duplicados en RETIROS | Propuesta técnica | No existe un campo compuesto equivalente en RETIROS; se propone `Identificación + Fecha Vencimiento`, consistente con el patrón de INGRESOS. |

## 9. Claves candidatas para duplicados

- **INGRESOS**: `Identificación_Fecha Inicio` (ya existe como campo derivado) o `cod` (Identificación-Año-Nombres). Ambas confirmadas por fórmula existente, no por aprobación funcional.
- **RETIROS**: no existe un campo equivalente. Propuesta técnica: `Identificación + Fecha Vencimiento`. Pendiente de aprobación humana.

## 10. Riesgos y limitaciones

1. **Año hardcodeado en dos fórmulas de INGRESOS** (`Ingreso_2025`, `Afecta calidad`): ambas fórmulas fijan el año 2025 de forma literal. Si el archivo se reutiliza para otros años sin actualizar la fórmula, el indicador queda incorrecto de forma silenciosa.
2. **Posible inconsistencia en la fórmula de `Ind_Calidad`**: compara `INGRESOS!cod` (patrón Identificación-Año-Nombres) contra `RETIROS!OBSERVACION` (patrón Identificación-Año-Mes.NombreMes) vía XLOOKUP. Son dos patrones de concatenación distintos; no se confirma que la comparación sea funcionalmente correcta sin revisión humana adicional.
3. **Rama Git divergente**: este análisis se documenta en `docs/roadmap-backlog`, mientras `origin/main` tiene documentación más reciente sobre gobierno de Contratos Kactus (`Docs/DATA_PIPELINE.md`, commits `e384746` y `612ddc5`) no incorporada aquí. Existe riesgo de conflicto o duplicidad al fusionar ramas.
4. **`Fact_Contrataciones` no se inspeccionó por valores**: su estructura se dedujo de metadatos del Data Model (pivot cache), no de una hoja plana legible directamente. Si el Data Model no se ha actualizado desde el último `Refresh All`, los 146 campos documentados podrían no reflejar cambios recientes en las fuentes.
5. **Campos sin propósito identificable** (`%` en ambas hojas, `Ultimo Detalle`): se documentan como observación, no como mapeo, porque no hay evidencia suficiente para clasificarlos sin riesgo de inventar una equivalencia.
6. **No se verificó consumo real de `Fact_Contrataciones` por `Proyecto7.pbip`**: consistente con lo ya documentado en `origin/main` ("no se debe declarar esta carpeta como fuente activa... hasta identificar una consulta Power Query o TMDL que la consuma").
7. **`Tbl_Ingresos` y `Tbl_Retiros`** (hojas adicionales en `PptovsReal.xlsx`) no se inspeccionaron por estar fuera del alcance autorizado explícito; podrían contener información relevante para el mapeo.

## 11. Próximo paso para construir el programa Python

1. Obtener aprobación humana explícita de las reglas listadas en la sección 8, en particular: definición de "Grupo Empresarial" (tabla de homologación), criterio de ingreso, y clave de duplicados para RETIROS.
2. Resolver las ambigüedades de "varios campos candidatos" (Dependencia, Área, Cargo, Nivel, Jefe Inmediato) con una decisión funcional por campo, antes de escribir código de transformación.
3. Confirmar o descartar la inconsistencia señalada en el riesgo 2 (`Ind_Calidad` vs. `OBSERVACION`) con el responsable funcional del archivo.
4. Solo después de 1-3: diseñar el script Python (pandas/openpyxl) que lea `Insumos_Vigentes/` (o `Fact_Contrataciones` si se confirma su vigencia), aplique las transformaciones de la sección 5 y genere las salidas INGRESOS/RETIROS con las claves de deduplicación de la sección 9.
5. Definir dónde vive el programa (`Tools/` o `Scripts/`, pendiente de adopción según `ESTRUCTURA_PROYECTO.md`) y cómo se documenta su ejecución en `Docs/RUNBOOK.md`.
