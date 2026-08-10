# Corrección de codificación de “Unión Libre” en Demográfico (Promedio)

Fecha: 2026-08-10

Estado: implementado, validado estáticamente y validado visualmente en vivo (sección 7).

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

## 5. Limitación de validación en vivo (histórica, superada — ver sección 7)

Al momento de la implementación (sección 3-4) no se usó la apertura de un checkout limpio de `main` como criterio de aceptación porque el repositorio mantenía el defecto estructural preexistente documentado en `GOV-005` (medidas duplicadas que impedían cargar un checkout limpio en Power BI Desktop). Esa limitación era ajena a la presente corrección.

La aceptación de ese momento se basó en la inspección estructural del grupo semántico, la conservación de referencias y la revisión del diff exclusivo. **`GOV-005` ya está resuelta y fusionada en `main`** (`Specs/0018`) — la validación visual en vivo de la sección 7 confirma que esta limitación ya no aplica.

## 6. Criterio de aceptación

- Las variantes equivalentes a Unión Libre devuelven exactamente `Unión Libre`.
- Los demás valores de Estado Civil conservan su lógica previa.
- No se modifican visuales ni medidas.
- El cambio queda versionado en un commit exclusivo y publicado en una rama aislada.

## 7. Validación visual en vivo (2026-08-10)

Cierre de la validación final de PR #7, exclusivamente sobre este alcance (no se implementó DATA-012, no se incorporó la migración HeadCount a SharePoint corporativo de forma permanente, no se tocó `Specs/0019` ni DATA-005/DATA-012, no se mezclaron cambios de Kactus, Retiros ni Rotación2).

**Estado de `GOV-005`:** ya estaba resuelta y fusionada en `main` antes de esta validación (`Specs/0018`, merge `4600798`) — confirmado nuevamente en vivo en este GATE: el modelo abrió sin `PFE_TM_OBJECT_NAME_ALREADY_EXISTS`.

**Apertura de `Proyecto7.pbip`:** se abrió correctamente desde un worktree temporal aislado (`.wt/union-libre-validacion-datos`, creado en blanco desde `origin/fix/demografico-union-libre-encoding`, HEAD `cb6d56aa1290b5d4fd95373e0f0c5d1e275bf174` — el HEAD exacto del PR #7). Verificado vía `powerbi-modeling-mcp`: 52 tablas, 66 relaciones, 122 medidas, 0 duplicados.

**Uso temporal de rutas corporativas (SOLO para disponer de datos de validación, NO forman parte del PR #7):** dentro de ese worktree temporal se sustituyeron, sin commitear, las 3 rutas HeadCount que apuntaban a OneDrive personal (`Consolidado2025.tmdl`, `PLANTA DE PERSONAL.tmdl`, `AREAS.tmdl`) por la biblioteca corporativa (`lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/...`), únicamente para poder ejecutar un refresh y disponer de datos con los que validar visualmente Estado Civil. Esta sustitución **no se commiteó ni se incorpora al PR #7** — corresponde al alcance aprobado de DATA-012 (`Specs/0019`, decisión F), no a esta corrección. Tras la validación visual, se descartaron íntegramente con `git checkout --` sobre los 3 archivos; el worktree quedó exactamente en el HEAD del PR #7, confirmado con `git diff origin/main` (solo 2 archivos: `PLANTA DE PERSONAL.tmdl` y este Spec — los mismos que ya formaban parte del PR).

**Refresh:** ejecutado manualmente por el usuario en Power BI Desktop (el servidor `powerbi-modeling-mcp` estaba en modo solo lectura y no pudo ejecutarlo). Completó sin errores de Formula Firewall, autenticación ni privacidad.

**Resultado visual (confirmado por el usuario mediante inspección directa de la página `Demográfico (Promedio)`, visual `Estado Civil`, captura de pantalla, 2026-08-10):**

- **Unión Libre**: se muestra exactamente `Unión Libre` (30 %). **No aparece ninguna variante mojibake** (`UniÃ³n Libre`, `Uniã³N Libre`, `Uni�n Libre`, `Uni�N Libre`).
- **Soltero**: correcto (57 %).
- **Casado**: correcto (12 %).
- **Divorciado**: correcto (1 %).
- **Otro**: correcto (confirmado por el usuario).
- **Viudo**: correcto (0 %).

**Confirmación de alcance funcional:** no se modificaron visuales, medidas, filtros, relaciones ni Power Query como parte funcional de esta validación. El único archivo funcional que integra el PR #7 sigue siendo `PBIP/Proyecto.SemanticModel/definition/tables/PLANTA DE PERSONAL.tmdl` (`EST_CIVIL (grupos)`), sin cambios adicionales — confirmado por `git diff origin/main` (sección anterior).

Con esta validación visual en vivo, el criterio de aceptación de la sección 6 queda completamente satisfecho, incluyendo la parte que antes solo se validaba estáticamente.
