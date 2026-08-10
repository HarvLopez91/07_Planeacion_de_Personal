# Corrección de codificación de “Unión Libre” en Demográfico (Promedio)

Fecha: 2026-08-10

Estado: implementado y validado estáticamente.

## 1. Solicitud

Corregir el valor de Estado Civil correspondiente a **“Unión Libre”** en la página **Demográfico (Promedio)** para que se visualice correctamente en español (Colombia), sin alterar los demás valores de Estado Civil ni la configuración de las visualizaciones.

## 2. Diagnóstico

La visual `1da9f64d870519b6bffa` de la página `ReportSectionf46593dd92bf9359ceef` (`Demográfico (Promedio)`) no contiene etiquetas de Estado Civil hardcodeadas. Su categoría referencia `PLANTA DE PERSONAL[EST_CIVIL (grupos)]`.

La columna agrupada ya homologaba `U` y `Unión Libre` al texto correcto `Unión Libre`, pero cualquier variante de mojibake no incluida en el grupo caía al último caso del `SWITCH` y se devolvía sin corregir. Esto explica que una variante mal codificada proveniente de `EST_CIVIL` pudiera mostrarse literalmente en la visual.

La consulta Power Query aplica `Text.Proper` a `EST_CIVIL`; por ello, una cadena mojibake puede llegar al modelo con una variante de mayúsculas/minúsculas diferente a la cadena originalmente dañada.

## 3. Implementación

Se modifica exclusivamente `PBIP/Proyecto.SemanticModel/definition/tables/PLANTA DE PERSONAL.tmdl` en la definición de `EST_CIVIL (grupos)`.

La categoría **Unión Libre** conserva como entradas válidas:

- `U`
- `Unión Libre`

Y agrega únicamente variantes de codificación equivalentes al mismo estado civil para devolver siempre:

- `Unión Libre`

Se actualiza en paralelo `GroupingDesignState` para mantener consistente la metadata de agrupación de Power BI.

No se modifica:

- la columna fuente `EST_CIVIL`;
- la consulta Power Query;
- medidas DAX;
- filtros;
- relaciones;
- visuales JSON;
- bookmarks;
- otras categorías de Estado Civil.

## 4. Validación de impacto

Validación estática sobre el PBIP versionado:

- La visual de Estado Civil en `Demográfico (Promedio)` continúa referenciando `PLANTA DE PERSONAL[EST_CIVIL (grupos)]` y `Tbl_Medidas[Tot_empleados_Promedio]`.
- No se modifica ningún archivo `visual.json`.
- Las homologaciones de `(En blanco)`, `Casado`, `Divorciado`, `Otro`, `Soltero` y `Viudo` permanecen sin cambios.
- El `lineageTag` de `EST_CIVIL (grupos)` se conserva: `b7226dd5-5031-4aa4-a301-ef77c36bc9f1`.
- Las otras visuales que reutilizan el mismo grupo semántico mantienen sus referencias; el único efecto esperado es que las variantes dañadas equivalentes a Unión Libre se agrupen bajo la etiqueta correcta `Unión Libre`.
- No se introduce ninguna modificación en archivos ajenos al alcance.

## 5. Limitación de validación en vivo

No se usa la apertura de un checkout limpio de `main` como criterio de aceptación porque el repositorio mantiene el defecto estructural preexistente documentado en `GOV-005` (medidas duplicadas que impiden cargar un checkout limpio en Power BI Desktop). Esta limitación es ajena a la presente corrección.

La aceptación de este ajuste se basa en la inspección estructural del grupo semántico, la conservación de referencias y la revisión del diff exclusivo.

## 6. Criterio de aceptación

- Las variantes equivalentes a Unión Libre devuelven exactamente `Unión Libre`.
- Los demás valores de Estado Civil conservan su lógica previa.
- No se modifican visuales ni medidas.
- El cambio queda versionado en un commit exclusivo y publicado en una rama aislada.
