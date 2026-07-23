# Plan de implementacion - Migracion de PptovsReal.xlsx a SharePoint corporativo

## 1. Estado

Estado: cerrado.
Fecha de cierre: 2026-07-23.
Fecha: 2026-07-16.
Proyecto: `07_Planeacion_de_Personal`.
PBIP: `PBIP/Proyecto7.pbip`.
Spec base: `Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md`.

Este documento no implementa cambios en PBIP, Data, Docs ni Outputs. Define fases, controles, prompts de ejecucion y criterios de aprobacion.

## 2. Objetivo

Planificar la migracion controlada de las tablas que aun consumen `PptovsReal.xlsx` desde la ruta personal antigua de SharePoint/OneDrive hacia la ruta corporativa de SharePoint.

Tablas objetivo:

- `Ppto Retiros`.
- `Ppto Ingresos`.

Tabla a validar, pero no necesariamente modificar:

- `Planta Ppto`.

## 3. Alcance

- Definir fases secuenciales de preflight, validacion, decision tecnica, implementacion, refresh, validacion funcional, auditoria, commit, push y documentacion posterior.
- Separar claramente cambios de fuente, ruido de Power BI Desktop, documentacion oficial y evidencia temporal.
- Redactar prompts autosuficientes para ejecutar cada fase con Codex, Claude Code o GitHub Copilot.
- Mantener el cambio tecnico futuro enfocado en Power Query/TMDL.

## 4. Fuera de alcance

En esta tarea no se permite:

- Modificar `PBIP/`.
- Modificar `Data/`.
- Modificar `Docs/`.
- Modificar `Outputs/`.
- Modificar `README.md`, `AGENTS.md`, `CLAUDE.md` o `.gitignore`.
- Abrir Power BI Desktop.
- Cambiar credenciales.
- Refrescar el modelo.
- Publicar.
- Hacer staging.
- Hacer commit.
- Hacer push.
- Usar `git add .`.
- Ejecutar `git restore`, `git checkout`, `git reset` o comandos destructivos.

## 5. Insumo base

La Spec base es:

```text
Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md
```

Rutas evaluadas:

Ruta antigua personal:

```text
https://lemcosas-my.sharepoint.com/personal/edwin_clavijo_challenger_co/Documents/Documentos/Anal%C3%ADtica%20del%20Grupo%20Empresarial%20Lemco/03_Fuentes_Datos/01_Talento_Humano/02_HeadCount/PptovsReal.xlsx
```

Ruta nueva corporativa:

```text
https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/Documentos%20compartidos/5.%20People%20analytics/07_Planeaci%C3%B3n_de_Personal/Data/HeadCount/PptovsReal.xlsx
```

Sitio corporativo recomendado para evaluar con `SharePoint.Contents`:

```text
https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco
```

## 6. Validacion inicial del entorno

Comandos ejecutados para crear este plan:

```powershell
git status -sb
git status --short
git diff --cached --name-status
git log --oneline origin/main..HEAD
git log --oneline HEAD..origin/main
git branch --show-current
git diff --check
```

Resultado resumido:

| Validacion | Resultado |
|---|---|
| Rama actual | `main` |
| Relacion con remoto | `main...origin/main` sin ahead/behind reportado |
| Commits locales pendientes | No se reportaron commits en `origin/main..HEAD` |
| Commits remotos pendientes | No se reportaron commits en `HEAD..origin/main` |
| Staging activo | No hay staging activo |
| `git diff --check` | Sin errores |
| Working tree | Sucio, con muchos cambios PBIP preexistentes fuera de alcance |
| Spec 0006 | Existe en `Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md` |
| Specs no rastreadas | `0004`, `0005` y `0006` aparecen no rastreadas; no deben mezclarse con commits tecnicos futuros |

Esta tarea solo crea la nueva Spec `0007`.

## 7. Resumen de hallazgos de Spec 0006

1. `Planta Ppto` ya usa la ruta corporativa nueva.
2. `Ppto Retiros` sigue usando la ruta personal antigua.
3. `Ppto Ingresos` sigue usando la ruta personal antigua.
4. El patron actual de conexion es:

   ```powerquery
   Excel.Workbook(Web.Contents("<url directa a PptovsReal.xlsx>"), null, true)
   ```

5. No existe actualmente `PBIP/Proyecto.SemanticModel/definition/expressions.tmdl`.
6. No se identifico uso actual de `SharePoint.Contents` ni `SharePoint.Files` para estas tres tablas.
7. Hojas esperadas en el Excel:
   - `Planta Personal`.
   - `RETIROS`.
   - `INGRESOS`.
8. Si el archivo corporativo mantiene hojas, columnas y tipos, no deberian requerirse visuales ni medidas.
9. Archivos necesarios futuros:
   - `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl`.
   - `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Ingresos.tmdl`.
10. `Planta Ppto.tmdl` debe validarse, pero no necesariamente modificarse.

## 8. Decisiones pendientes

| Decision | Opciones | Responsable / aprobacion |
|---|---|---|
| Conector final | `SharePoint.Contents`, `SharePoint.Files` o reemplazo directo de URL con `Web.Contents` | Usuario / responsable tecnico |
| Copia oficial | Confirmar que el archivo corporativo es la fuente oficial | Responsable funcional |
| Permisos | Confirmar acceso local y refresh de Power BI Service | Responsable tecnico / propietario del sitio |
| `Planta Ppto.tmdl` | Mantener como esta o reescribir al mismo patron elegido | Usuario, solo si aplica |
| Parametros | Crear o no parametros/funciones compartidas | Usuario, por mayor alcance |
| Documentacion oficial | Actualizar Docs en fase posterior | Usuario, luego de validar y publicar |

## 9. Fases de implementacion

| Fase | Nombre | Resultado | Cambia PBIP | Staging | Commit |
|---:|---|---|---|---|---|
| 0 | Preflight y congelamiento de alcance | Output diagnostico | No | No | No |
| 1 | Validacion de acceso y estructura del archivo corporativo | Output evidencia | No | No | No |
| 2 | Decision tecnica de conector | Output decision | No | No | No |
| 3 | Implementacion controlada en Power Query/TMDL | TMDL ajustados + Output | Si, solo TMDL aprobados | No | No |
| 4 | Refresh local y validacion de tablas | Output refresh | Posible ruido Desktop | No | No |
| 5 | Validacion funcional de paginas impactadas | Output funcional | No intencional | No | No |
| 6 | Auditoria PBIP post-refresh | Output auditoria | No | No | No |
| 7 | Commit del cambio de fuente | Commit local | No adicional | Si | Si |
| 8 | Cierre y decision de push | Recomendacion / push con aprobacion | No | No | No nuevo |
| 9 | Documentacion oficial posterior | Docs actualizados, si se aprueba | No PBIP | Si | Si |

## 10. Fase 0 - Preflight y congelamiento de alcance

### Objetivo

Validar estado Git, confirmar referencias a `PptovsReal.xlsx`, confirmar tablas afectadas y generar evidencia en `Outputs/` sin modificar PBIP.

### Archivos candidatos

- Solo nuevo output de diagnostico en `Outputs/`.

### Archivos excluidos

- `PBIP/`.
- `Data/`.
- `Docs/`.
- `Specs/`.
- `README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`.

### Prompt de ejecucion

```text
Actua como arquitecto Power BI/PBIP, auditor Git y analista de impacto.

Objetivo:
Ejecutar la Fase 0 - Preflight y congelamiento de alcance para migrar PptovsReal.xlsx desde ruta personal a SharePoint corporativo, sin modificar PBIP.

Contexto:
Proyecto: 07_Planeacion_de_Personal
Ruta local: c:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal
PBIP: PBIP/Proyecto7.pbip
Spec base: Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md
Plan: Specs/0007_plan_implementacion_cambio_fuente_pptovsreal_sharepoint.md

Ruta antigua:
https://lemcosas-my.sharepoint.com/personal/edwin_clavijo_challenger_co/Documents/Documentos/Anal%C3%ADtica%20del%20Grupo%20Empresarial%20Lemco/03_Fuentes_Datos/01_Talento_Humano/02_HeadCount/PptovsReal.xlsx

Ruta nueva:
https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/Documentos%20compartidos/5.%20People%20analytics/07_Planeaci%C3%B3n_de_Personal/Data/HeadCount/PptovsReal.xlsx

Instrucciones obligatorias:
- No modificar PBIP/.
- No modificar Data/.
- No modificar Docs/.
- No modificar Specs/.
- No usar git add .
- No hacer staging.
- No hacer commit.
- No hacer push.
- No ejecutar restore, checkout, reset ni comandos destructivos.
- No abrir Power BI Desktop.
- No exponer datos personales ni registros individuales.
- Crear solo un Output nuevo de evidencia.
- Clasificacion documental: Specs para planes y analisis; Outputs para evidencia temporal; Docs para documentacion oficial estable.

Comandos permitidos:
git status -sb
git status --short
git diff --cached --name-status
git log --oneline origin/main..HEAD
git log --oneline HEAD..origin/main
git branch --show-current
git diff --check
rg
Get-Content
Get-ChildItem

Tareas:
1. Validar estado Git.
2. Confirmar que existen la Spec 0006, PBIP/Proyecto7.pbip y los TMDL de Planta Ppto, Ppto Retiros y Ppto Ingresos.
3. Buscar referencias a PptovsReal.xlsx y a la ruta personal antigua.
4. Confirmar que Planta Ppto ya usa ruta corporativa.
5. Confirmar que Ppto Retiros y Ppto Ingresos siguen usando ruta personal.
6. Crear Output con el siguiente consecutivo disponible: XX_2026-07-16_preflight_migracion_pptovsreal_sharepoint.md.

Validaciones finales:
git status --short
git status --short -- Outputs/
git diff --check
git diff --cached --name-status

Entrega esperada:
- Output creado.
- Tablas afectadas.
- Archivos candidatos futuros.
- Archivos excluidos.
- Riesgos.
- Recomendacion: procede Fase 1 o bloquear.

Condicion para pasar a Fase 1:
Referencias y alcance confirmados sin staging ni cambios en PBIP.

Condicion de bloqueo:
Staging activo, commits remotos pendientes, Spec base ausente o referencias inconsistentes.
```

## 11. Fase 1 - Validacion de acceso y estructura del archivo corporativo

### Objetivo

Confirmar acceso al archivo corporativo, existencia del archivo, hojas esperadas y estructura basica antes de editar TMDL.

### Archivos candidatos

- Solo nuevo output de evidencia en `Outputs/`.

### Archivos excluidos

- `PBIP/`.
- `Data/`.
- `Docs/`.
- `Specs/`.

### Prompt de ejecucion

```text
Actua como especialista Power BI/PBIP, auditor de fuentes SharePoint y analista de datos agregado.

Objetivo:
Ejecutar la Fase 1 - Validacion de acceso y estructura del archivo corporativo PptovsReal.xlsx, sin modificar PBIP.

Contexto:
Proyecto: 07_Planeacion_de_Personal
Ruta local: c:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal
PBIP: PBIP/Proyecto7.pbip
Spec base: Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md
Plan: Specs/0007_plan_implementacion_cambio_fuente_pptovsreal_sharepoint.md

Ruta nueva corporativa:
https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/Documentos%20compartidos/5.%20People%20analytics/07_Planeaci%C3%B3n_de_Personal/Data/HeadCount/PptovsReal.xlsx

Sitio recomendado:
https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco

Instrucciones obligatorias:
- No modificar PBIP/.
- No modificar Data/.
- No modificar Docs/.
- No modificar Specs/.
- No cambiar credenciales.
- No refrescar modelo.
- No publicar.
- No usar git add .
- No hacer staging, commit ni push.
- No exponer registros individuales.
- Crear solo un Output nuevo.

Comandos permitidos:
git status -sb
git status --short
git diff --cached --name-status
git diff --check
rg
Get-ChildItem
Get-Content

Tareas:
1. Validar Git y ausencia de staging.
2. Confirmar si existe una copia local segura del Excel en Data/ sin abrir ni modificar Data/.
3. Si el acceso al enlace corporativo debe validarse fuera de CLI, pedir al usuario confirmacion de acceso en navegador y no asumir.
4. Confirmar, con evidencia disponible, que las hojas esperadas son Planta Personal, RETIROS e INGRESOS.
5. Confirmar columnas esperadas solo a nivel agregado/metadatos si hay fuente local accesible; no mostrar registros individuales.
6. Crear Output: XX_2026-07-16_validacion_acceso_estructura_pptovsreal_sharepoint.md.

Validaciones finales:
git status --short
git status --short -- Outputs/
git diff --check
git diff --cached --name-status

Entrega esperada:
- Estado de acceso.
- Hojas esperadas confirmadas o pendientes.
- Riesgos de permisos y estructura.
- Recomendacion: procede Fase 2 o bloquear.

Condicion para pasar a Fase 2:
Acceso y estructura del archivo corporativo confirmados, o decision explicita de usar validacion manual antes de editar.

Condicion de bloqueo:
No hay acceso al archivo, no se puede confirmar existencia, faltan hojas esperadas o hay staging activo.
```

## 12. Fase 2 - Decision tecnica de conector

### Objetivo

Decidir si la implementacion usara `SharePoint.Contents`, `SharePoint.Files` o reemplazo directo de URL con `Web.Contents`.

### Archivos candidatos

- Solo nuevo output de decision en `Outputs/`.

### Prompt de ejecucion

```text
Actua como arquitecto Power BI/PBIP, especialista en Power Query M y responsable de gobernanza de fuentes.

Objetivo:
Ejecutar la Fase 2 - Decision tecnica de conector para migrar PptovsReal.xlsx.

Contexto:
Proyecto: 07_Planeacion_de_Personal
Ruta local: c:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal
PBIP: PBIP/Proyecto7.pbip
Spec base: Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md
Plan: Specs/0007_plan_implementacion_cambio_fuente_pptovsreal_sharepoint.md

Opciones:
A. SharePoint.Contents sobre https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco
B. SharePoint.Files filtrando por Folder Path y Name = PptovsReal.xlsx
C. Reemplazo directo de URL con Web.Contents, alineado con Planta Ppto

Instrucciones obligatorias:
- No modificar PBIP/.
- No modificar Data/.
- No modificar Docs/.
- No modificar Specs/.
- No usar git add .
- No hacer staging, commit ni push.
- No abrir Power BI Desktop.
- No cambiar credenciales.
- Crear solo un Output nuevo.
- Clasificacion documental: Specs para planes y analisis; Outputs para evidencia temporal; Docs para documentacion oficial estable.

Comandos permitidos:
git status -sb
git status --short
git diff --cached --name-status
git diff --check
rg
Get-Content

Tareas:
1. Revisar Spec 0006 y outputs previos si existen.
2. Comparar opciones A, B y C por riesgo, complejidad, diff esperado, refresh, credenciales, rollback y consistencia con Planta Ppto.
3. Recomendar una opcion principal y una contingencia.
4. Explicar si Planta Ppto debe permanecer sin cambios o si requiere alineacion posterior.
5. Crear Output: XX_2026-07-16_decision_conector_pptovsreal_sharepoint.md.

Validaciones finales:
git status --short
git status --short -- Outputs/
git diff --check
git diff --cached --name-status

Entrega esperada:
- Decision tecnica recomendada.
- Alternativa de contingencia.
- Archivos que se tocarian en Fase 3.
- Riesgos.

Condicion para pasar a Fase 3:
Decision tecnica aprobada por el usuario.

Condicion de bloqueo:
No existe aprobacion clara de conector o aparecen riesgos no resueltos de acceso/credenciales.
```

## 13. Fase 3 - Implementacion controlada en Power Query/TMDL

### Objetivo

Modificar unicamente las queries M aprobadas en:

- `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl`.
- `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Ingresos.tmdl`.

### Archivos candidatos

| Archivo | Uso |
|---|---|
| `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl` | Necesario |
| `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Ingresos.tmdl` | Necesario |
| `PBIP/Proyecto.SemanticModel/definition/tables/Planta Ppto.tmdl` | Solo si se aprueba explicitamente |
| `PBIP/Proyecto.SemanticModel/definition/model.tmdl` | Solo si se aprueban parametros |
| `PBIP/Proyecto.SemanticModel/definition/expressions.tmdl` | Solo si se aprueba crear expresion/parametro |

### Prompt de ejecucion

```text
Actua como arquitecto Power BI/PBIP, especialista en Power Query M y auditor Git.

Objetivo:
Ejecutar la Fase 3 - Implementacion controlada en TMDL para migrar Ppto Retiros y Ppto Ingresos desde la ruta personal a SharePoint corporativo.

Contexto:
Proyecto: 07_Planeacion_de_Personal
Ruta local: c:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal
PBIP: PBIP/Proyecto7.pbip
Spec base: Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md
Plan: Specs/0007_plan_implementacion_cambio_fuente_pptovsreal_sharepoint.md

Ruta antigua:
https://lemcosas-my.sharepoint.com/personal/edwin_clavijo_challenger_co/Documents/Documentos/Anal%C3%ADtica%20del%20Grupo%20Empresarial%20Lemco/03_Fuentes_Datos/01_Talento_Humano/02_HeadCount/PptovsReal.xlsx

Ruta nueva:
https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/Documentos%20compartidos/5.%20People%20analytics/07_Planeaci%C3%B3n_de_Personal/Data/HeadCount/PptovsReal.xlsx

Archivos permitidos:
- PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl
- PBIP/Proyecto.SemanticModel/definition/tables/Ppto Ingresos.tmdl
- Outputs/XX_2026-07-16_implementacion_tmdl_pptovsreal_sharepoint.md

Archivos prohibidos:
- PBIP/Proyecto.Report/**
- PBIP/Proyecto.SemanticModel/diagramLayout.json
- PBIP/Proyecto.SemanticModel/definition/cultures/es-ES.tmdl
- PBIP/Proyecto.Report/definition/pages/pages.json
- PBIP/Proyecto.Report/definition/bookmarks/**
- Data/**
- Docs/**
- Specs/**
- README.md
- AGENTS.md
- CLAUDE.md
- .gitignore

Instrucciones obligatorias:
- Implementar solo la opcion tecnica aprobada en Fase 2.
- Migrar Ppto Retiros y Ppto Ingresos en conjunto.
- No modificar Planta Ppto.tmdl salvo aprobacion explicita.
- No mezclar cambios visuales con cambios de fuente.
- No usar git add .
- No hacer staging.
- No hacer commit.
- No hacer push.
- No ejecutar restore, checkout, reset ni comandos destructivos.
- No abrir Power BI Desktop en esta fase.

Comandos permitidos:
git status -sb
git status --short
git diff --cached --name-status
git diff --check
git diff -- PBIP/Proyecto.SemanticModel/definition/tables/Ppto` Retiros.tmdl
git diff -- PBIP/Proyecto.SemanticModel/definition/tables/Ppto` Ingresos.tmdl
rg
Get-Content

Tareas:
1. Validar Git y ausencia de staging.
2. Confirmar que Ppto Retiros y Ppto Ingresos contienen la ruta antigua.
3. Aplicar el cambio aprobado solo en los bloques M de ambas tablas.
4. Mantener hojas RETIROS e INGRESOS y transformaciones existentes.
5. Validar que no se alteren columnas calculadas no relacionadas.
6. Validar sintaxis basica TMDL y ausencia de doble codificacion nueva.
7. Crear Output de implementacion.

Validaciones finales:
git status --short
git status --short -- PBIP/Proyecto.SemanticModel/definition/tables/
git status --short -- Outputs/
git diff --check
git diff --cached --name-status

Entrega esperada:
- Archivos modificados.
- Opcion tecnica aplicada.
- Confirmacion de que no se tocaron visuales ni Docs.
- Riesgos pendientes para refresh.

Condicion para pasar a Fase 4:
Diff limitado a TMDL aprobados y sin errores de `git diff --check`.

Condicion de bloqueo:
Necesidad de modificar model.tmdl, expressions.tmdl o Planta Ppto.tmdl sin aprobacion previa; o cambio colateral fuera de alcance.
```

## 14. Fase 4 - Refresh local y validacion de tablas

### Objetivo

Abrir Power BI Desktop, ejecutar refresh local y validar tablas afectadas con evidencia agregada.

### Prompt de ejecucion

```text
Actua como validador Power BI Desktop, auditor de refresh y analista de datos agregado.

Objetivo:
Ejecutar la Fase 4 - Refresh local y validacion de tablas despues de migrar PptovsReal.xlsx.

Contexto:
Proyecto: 07_Planeacion_de_Personal
Ruta local: c:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal
PBIP: PBIP/Proyecto7.pbip
Spec base: Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md
Plan: Specs/0007_plan_implementacion_cambio_fuente_pptovsreal_sharepoint.md

Tablas a validar:
- Planta Ppto
- Ppto Retiros
- Ppto Ingresos

Instrucciones obligatorias:
- No modificar visuales.
- No modificar Docs/.
- No modificar Specs/.
- No hacer staging, commit ni push.
- No usar git add .
- No publicar.
- No exponer registros individuales.
- Si Power BI Desktop genera ruido automatico, documentarlo y no incluirlo en commit.
- Crear solo un Output de evidencia.

Comandos permitidos antes/despues:
git status -sb
git status --short
git diff --cached --name-status
git diff --check
git diff --stat -- PBIP/
git diff -- PBIP/Proyecto.SemanticModel/definition/tables/Ppto` Retiros.tmdl
git diff -- PBIP/Proyecto.SemanticModel/definition/tables/Ppto` Ingresos.tmdl

Tareas:
1. Validar Git antes de abrir Desktop.
2. Abrir PBIP/Proyecto7.pbip.
3. Ejecutar refresh local.
4. Validar que no haya errores de credenciales, privacidad o archivo no encontrado.
5. Validar conteos agregados antes/despues, si estan disponibles.
6. Validar columnas y tipos de Planta Ppto, Ppto Retiros y Ppto Ingresos.
7. Cerrar Power BI Desktop guardando solo si el refresh y cambios aprobados lo requieren.
8. Crear Output: XX_2026-07-16_refresh_validacion_tablas_pptovsreal_sharepoint.md.

Validaciones finales:
git status --short
git status --short -- PBIP/
git status --short -- Outputs/
git diff --check
git diff --cached --name-status

Entrega esperada:
- Resultado de refresh.
- Conteos agregados.
- Errores encontrados o ausencia de errores.
- Ruido Desktop detectado.
- Recomendacion: procede Fase 5 o bloquear.

Condicion para pasar a Fase 5:
Refresh exitoso y tablas afectadas validas.

Condicion de bloqueo:
Errores de credenciales, privacidad, archivo inexistente, hoja faltante, columnas faltantes o cambios no controlados.
```

## 15. Fase 5 - Validacion funcional de paginas impactadas

### Objetivo

Validar paginas relacionadas con `PptovsReal.xlsx` despues del refresh.

### Prompt de ejecucion

```text
Actua como validador funcional Power BI/PBIP, especialista People Analytics y auditor visual.

Objetivo:
Ejecutar la Fase 5 - Validacion funcional de paginas impactadas por PptovsReal.xlsx.

Contexto:
Proyecto: 07_Planeacion_de_Personal
Ruta local: c:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal
PBIP: PBIP/Proyecto7.pbip
Spec base: Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md
Plan: Specs/0007_plan_implementacion_cambio_fuente_pptovsreal_sharepoint.md

Paginas minimas:
- Productividad
- Product. (Colaboradores)
- Retiros
- Gasto Laboral
- Comportamiento HC o vistas relacionadas
- Corte junio 2026

Instrucciones obligatorias:
- No modificar PBIP de forma intencional.
- No crear visuales.
- No crear medidas.
- No modificar modelo.
- No modificar Docs/ ni Specs/.
- No hacer staging, commit ni push.
- No usar git add .
- No exponer datos personales.
- Crear solo un Output nuevo.

Comandos permitidos:
git status -sb
git status --short
git diff --cached --name-status
git diff --check
git diff --stat -- PBIP/

Tareas:
1. Validar Git.
2. Abrir Proyecto7.pbip.
3. Revisar paginas impactadas.
4. Validar indicadores de presupuesto vs real, ingresos, retiros, rotacion, productividad y gasto laboral.
5. Validar corte junio 2026.
6. Documentar cualquier visual rota, medida en blanco o error de credenciales.
7. No guardar cambios si no se hicieron ajustes intencionales.
8. Crear Output: XX_2026-07-16_validacion_funcional_pptovsreal_sharepoint.md.

Validaciones finales:
git status --short
git status --short -- Outputs/
git diff --check
git diff --cached --name-status

Entrega esperada:
- Paginas validadas.
- Indicadores clave revisados.
- Hallazgos.
- Riesgos.
- Recomendacion: procede Fase 6 o bloquear.

Condicion para pasar a Fase 6:
Paginas criticas sin errores funcionales derivados del cambio de fuente.

Condicion de bloqueo:
Visuales rotas, medidas inconsistentes, refresh parcial o diferencia no explicada de datos.
```

## 16. Fase 6 - Auditoria PBIP post-refresh

### Objetivo

Separar cambios reales de fuente frente a ruido de Power BI Desktop y cambios preexistentes.

### Prompt de ejecucion

```text
Actua como auditor PBIP, analista de impacto y responsable de control de cambios Git.

Objetivo:
Ejecutar la Fase 6 - Auditoria PBIP post-refresh para separar cambios reales de fuente vs ruido.

Contexto:
Proyecto: 07_Planeacion_de_Personal
Ruta local: c:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal
PBIP: PBIP/Proyecto7.pbip
Spec base: Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md
Plan: Specs/0007_plan_implementacion_cambio_fuente_pptovsreal_sharepoint.md

Archivos candidatos esperados:
- PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl
- PBIP/Proyecto.SemanticModel/definition/tables/Ppto Ingresos.tmdl

Archivos a excluir salvo aprobacion explicita:
- PBIP/Proyecto.SemanticModel/definition/tables/Planta Ppto.tmdl
- PBIP/Proyecto.SemanticModel/definition/model.tmdl
- PBIP/Proyecto.SemanticModel/definition/expressions.tmdl
- PBIP/Proyecto.SemanticModel/definition/cultures/es-ES.tmdl
- PBIP/Proyecto.SemanticModel/diagramLayout.json
- PBIP/Proyecto.Report/**
- Data/**
- Docs/**
- Specs/**
- Outputs/**

Instrucciones obligatorias:
- No modificar archivos.
- No hacer staging, commit ni push.
- No usar git add .
- No ejecutar restore, checkout, reset ni comandos destructivos.
- Crear solo un Output nuevo.

Comandos permitidos:
git status -sb
git status --short
git status --short -- PBIP/
git diff --cached --name-status
git diff --check
git diff --stat -- PBIP/
git diff -- PBIP/Proyecto.SemanticModel/definition/tables/Ppto` Retiros.tmdl
git diff -- PBIP/Proyecto.SemanticModel/definition/tables/Ppto` Ingresos.tmdl
git diff -- PBIP/Proyecto.SemanticModel/definition/cultures/es-ES.tmdl
git diff -- PBIP/Proyecto.SemanticModel/diagramLayout.json
rg

Tareas:
1. Validar Git y staging vacio.
2. Clasificar cambios reales de fuente.
3. Identificar ruido de Desktop.
4. Identificar cambios preexistentes fuera de alcance.
5. Proponer lista exacta de archivos candidatos para commit.
6. Crear Output: XX_2026-07-16_auditoria_pbip_post_refresh_pptovsreal_sharepoint.md.

Validaciones finales:
git status --short
git status --short -- Outputs/
git diff --check
git diff --cached --name-status

Entrega esperada:
- Candidatos para commit.
- Archivos excluidos.
- Riesgos.
- Recomendacion: procede Fase 7 o bloquear.

Condicion para pasar a Fase 7:
Lista de archivos candidatos exacta y aprobada por el usuario.

Condicion de bloqueo:
Cambios fuera de alcance inseparables, staging activo o diff con errores.
```

## 17. Fase 7 - Commit del cambio de fuente

### Objetivo

Hacer staging selectivo solo de los TMDL aprobados y crear commit local.

### Prompt de ejecucion

```text
Actua como auditor Git, responsable de staging selectivo y arquitecto PBIP.

Objetivo:
Ejecutar la Fase 7 - Commit del cambio de fuente PptovsReal.xlsx a SharePoint corporativo.

Contexto:
Proyecto: 07_Planeacion_de_Personal
Ruta local: c:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal
PBIP: PBIP/Proyecto7.pbip
Spec base: Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md
Plan: Specs/0007_plan_implementacion_cambio_fuente_pptovsreal_sharepoint.md

Archivos permitidos para staging:
- PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl
- PBIP/Proyecto.SemanticModel/definition/tables/Ppto Ingresos.tmdl

Archivos prohibidos:
- PBIP/Proyecto.Report/**
- PBIP/Proyecto.SemanticModel/diagramLayout.json
- PBIP/Proyecto.SemanticModel/definition/cultures/es-ES.tmdl
- PBIP/Proyecto.Report/definition/pages/pages.json
- PBIP/Proyecto.Report/definition/bookmarks/**
- Data/**
- Docs/**
- Specs/**
- Outputs/**
- README.md
- AGENTS.md
- CLAUDE.md
- .gitignore

Instrucciones obligatorias:
- No usar git add .
- No hacer push.
- No modificar archivos antes del commit.
- No incluir Outputs, Specs ni Docs en el commit tecnico.
- No incluir visuales ni ruido Desktop.
- Validar identidad Git antes del commit.

Comandos permitidos:
git status -sb
git status --short
git diff --cached --name-status
git diff --check
git diff -- PBIP/Proyecto.SemanticModel/definition/tables/Ppto` Retiros.tmdl
git diff -- PBIP/Proyecto.SemanticModel/definition/tables/Ppto` Ingresos.tmdl
git config --local --get user.name
git config --local --get user.email
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
git add "PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl"
git add "PBIP/Proyecto.SemanticModel/definition/tables/Ppto Ingresos.tmdl"
git diff --cached --name-status
git diff --cached --stat
git diff --cached --check
git commit -m "fix(data): migra PptovsReal a SharePoint corporativo"
git log --oneline -1
git show --stat --oneline HEAD

Tareas:
1. Validar Git, staging vacio e identidad.
2. Revisar diffs de los dos TMDL.
3. Hacer staging solo de rutas autorizadas.
4. Validar que el staging contiene exclusivamente los TMDL aprobados.
5. Crear commit local con mensaje aprobado.
6. No hacer push.

Entrega esperada:
- Hash del commit.
- Archivos incluidos.
- Confirmacion de exclusiones.
- Estado final.

Condicion para pasar a Fase 8:
Commit local creado y sin archivos fuera de alcance.

Condicion de bloqueo:
Staging contiene archivos no autorizados, identidad Git incorrecta, errores de diff o dudas sobre alcance.
```

## 18. Fase 8 - Cierre y decision de push

### Objetivo

Validar commits locales, estado frente a `origin/main` y preparar push solo con aprobacion explicita.

### Prompt de ejecucion

```text
Actua como auditor Git y responsable de cierre de implementacion PBIP.

Objetivo:
Ejecutar la Fase 8 - Cierre y decision de push para el cambio de fuente PptovsReal.xlsx.

Contexto:
Proyecto: 07_Planeacion_de_Personal
Ruta local: c:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal
PBIP: PBIP/Proyecto7.pbip
Plan: Specs/0007_plan_implementacion_cambio_fuente_pptovsreal_sharepoint.md

Instrucciones obligatorias:
- No modificar archivos.
- No hacer staging.
- No hacer commit.
- No usar git add .
- No hacer push sin aprobacion explicita del usuario.
- No usar push --force.
- No limpiar working tree.

Comandos permitidos:
git branch --show-current
git status -sb
git diff --cached --name-status
git fetch origin
git log --oneline origin/main..HEAD
git log --oneline HEAD..origin/main
git show --stat --oneline HEAD

Tareas:
1. Validar rama main.
2. Validar staging vacio.
3. Validar commits locales pendientes.
4. Validar que no hay commits remotos pendientes.
5. Confirmar que los cambios no commiteados no se subiran.
6. Entregar recomendacion de push.

Entrega esperada:
- Commits locales pendientes.
- Estado frente a origin/main.
- Confirmacion de que no se subiran cambios no commiteados.
- Prompt separado para push si el usuario aprueba.

Condicion para push:
Usuario aprueba explicitamente y los commits locales son exactamente los aprobados.

Condicion de bloqueo:
Commits remotos pendientes, commits locales no aprobados, staging activo o rama distinta de main.
```

## 19. Fase 9 - Documentacion oficial posterior

### Objetivo

Actualizar documentacion oficial solo si la migracion queda validada y publicada.

### Archivos potenciales

- `Docs/ARCHITECTURE.md`.
- `Docs/DATA_PIPELINE.md`.
- `Docs/DATA_MODEL.md`.
- `Docs/PROJECT_CONTEXT.md`.
- `Docs/BI_GUIDELINES.md`.

### Prompt de ejecucion

```text
Actua como responsable de gobernanza documental, arquitecto Power BI/PBIP y auditor Git.

Objetivo:
Ejecutar la Fase 9 - Documentacion oficial posterior de la migracion PptovsReal.xlsx a SharePoint corporativo.

Contexto:
Proyecto: 07_Planeacion_de_Personal
Ruta local: c:\Users\edwin.clavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal
Spec base: Specs/0006_analisis_impacto_cambio_fuente_pptovsreal_sharepoint.md
Plan: Specs/0007_plan_implementacion_cambio_fuente_pptovsreal_sharepoint.md

Archivos permitidos:
- Docs/ARCHITECTURE.md
- Docs/DATA_PIPELINE.md
- Docs/DATA_MODEL.md
- Docs/PROJECT_CONTEXT.md
- Docs/BI_GUIDELINES.md

Archivos prohibidos:
- PBIP/**
- Data/**
- Outputs/**
- Specs/**
- README.md
- AGENTS.md
- CLAUDE.md
- .gitignore

Instrucciones obligatorias:
- Ejecutar solo si la migracion tecnica ya fue validada y publicada.
- No modificar PBIP.
- No mezclar Docs con TMDL.
- No usar git add .
- No hacer push sin aprobacion.

Comandos permitidos:
git status -sb
git status --short
git diff --cached --name-status
git diff --check
rg
Get-Content
git add Docs/ARCHITECTURE.md
git add Docs/DATA_PIPELINE.md
git add Docs/DATA_MODEL.md
git add Docs/PROJECT_CONTEXT.md
git add Docs/BI_GUIDELINES.md
git diff --cached --name-status
git diff --cached --check
git commit -m "docs(data): actualiza fuente PptovsReal SharePoint corporativo"

Tareas:
1. Identificar menciones obsoletas a ruta personal o cuenta personal para PptovsReal.
2. Actualizar solo documentacion aplicable.
3. Validar diff.
4. Hacer staging explicito solo de Docs modificados.
5. Crear commit documental separado.
6. No hacer push.

Entrega esperada:
- Docs actualizados.
- Commit documental local, si aplica.
- Confirmacion de no modificar PBIP.

Condicion de cierre:
Documentacion refleja la fuente corporativa sin mezclar cambios tecnicos.

Condicion de bloqueo:
Migracion tecnica no publicada, cambios PBIP detectados o falta de aprobacion documental.
```

## 20. Riesgos y mitigaciones

| Riesgo | Nivel | Mitigacion |
|---|---|---|
| Permisos insuficientes en SharePoint corporativo | Alto | Validar acceso antes de editar TMDL. |
| Diferencia entre ruta URL y navegacion de conector | Alto | Evaluar `SharePoint.Contents`, `SharePoint.Files` y reemplazo directo antes de implementar. |
| Hoja o columnas faltantes en archivo corporativo | Alto | Validar hojas `Planta Personal`, `RETIROS`, `INGRESOS` y columnas antes de refresh. |
| Ruido de Power BI Desktop | Medio/Alto | Auditar `git diff` y excluir `cultures`, `diagramLayout`, `pages`, bookmarks y visuales. |
| Working tree sucio | Alto | Staging explicito por rutas; no usar `git add .`. |
| Mezcla de documentacion y TMDL | Medio | Commit tecnico separado de commit documental. |
| Cambio de credenciales en Power BI Service | Medio/Alto | Validar credenciales despues de refresh local y antes de publicar. |
| `Planta Ppto` queda con patron distinto | Medio | Validar consistencia; no modificar salvo aprobacion. |

## 21. Validaciones previas

Antes de implementar Fase 3:

1. Fase 0 completada sin staging.
2. Fase 1 confirma acceso y estructura.
3. Fase 2 define conector aprobado.
4. Usuario aprueba la opcion tecnica.
5. Working tree revisado y cambios fuera de alcance identificados.
6. No hay commits remotos pendientes.
7. No hay staging activo.

## 22. Validaciones posteriores

Despues de implementar:

1. `git diff --check`.
2. Refresh local exitoso.
3. Conteos antes/despues documentados.
4. Tablas `Ppto Retiros`, `Ppto Ingresos` y `Planta Ppto` validadas.
5. Paginas impactadas revisadas.
6. Ruido de Desktop clasificado.
7. Staging selectivo auditado con `git diff --cached --name-status`.
8. Commit tecnico creado sin Docs, Specs, Outputs ni visuales.

## 23. Estrategia de commits

Commit tecnico:

```text
fix(data): migra PptovsReal a SharePoint corporativo
```

Debe incluir solo:

- `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl`.
- `PBIP/Proyecto.SemanticModel/definition/tables/Ppto Ingresos.tmdl`.

Solo se incluirian otros archivos si la Fase 2 y el usuario lo aprueban explicitamente.

Commit documental posterior, si aplica:

```text
docs(data): actualiza fuente PptovsReal SharePoint corporativo
```

## 24. Plan de rollback

1. Si el refresh falla antes de commit, no hacer staging ni commit; diagnosticar y corregir o volver al plan.
2. Si el commit tecnico ya existe y falla validacion posterior, revertir el commit con un commit de revert aprobado.
3. Mantener evidencia de conteos antes/despues en `Outputs/`.
4. Si la urgencia operativa lo requiere, restaurar temporalmente la ruta anterior solo con aprobacion.
5. No mezclar rollback con cambios visuales ni documentacion.

## 25. Condicion de cierre

El plan queda cerrado cuando:

- `Ppto Retiros` y `Ppto Ingresos` consumen `PptovsReal.xlsx` desde ubicacion corporativa aprobada.
- Refresh local funciona.
- Paginas impactadas funcionan.
- Commit tecnico esta creado.
- Push fue aprobado y ejecutado, si corresponde.
- Documentacion oficial fue actualizada en fase separada, si se aprueba.

## 26. Criterios para autorizar push

Antes de push:

1. Rama actual `main`.
2. `git diff --cached --name-status` vacio.
3. `git log --oneline HEAD..origin/main` vacio.
4. `git log --oneline origin/main..HEAD` contiene solo commits aprobados.
5. El working tree puede estar sucio, pero los cambios no commiteados no se suben.
6. Usuario aprueba explicitamente `git push origin main`.
7. No usar `push --force`.

## 27. Decision de documentacion oficial posterior

La documentacion oficial debe actualizarse solo despues de validar y publicar el cambio tecnico. Los archivos `Docs/` no deben mezclarse con el commit tecnico de TMDL.

Prioridad documental futura:

1. `Docs/DATA_PIPELINE.md`.
2. `Docs/ARCHITECTURE.md`.
3. `Docs/DATA_MODEL.md`.
4. `Docs/PROJECT_CONTEXT.md`.
5. `Docs/BI_GUIDELINES.md`.

## 28. Cierre de implementacion

### Resultado general

La migracion de `PptovsReal.xlsx` quedo completada y publicada. La fuente corporativa fue validada mediante refresh y revision funcional confirmada por el usuario.

### Consultas finales

| Consulta | Hoja consumida |
|---|---|
| `Planta Ppto` | `Planta Personal` |
| `Ppto Ingresos` | `INGRESOS` |
| `Ppto Retiros` | `RETIROS` |

### Decision tecnica

- Se conservo el patron `Excel.Workbook(Web.Contents(...), null, true)`.
- Se reemplazo la ubicacion personal anterior por SharePoint corporativo.
- No se crearon parametros, funciones M ni cambios visuales.

### Ajuste de alcance

`Planta Ppto.tmdl` fue incluido mediante aprobacion explicita del usuario. Su cambio correspondio exclusivamente al mismo reemplazo de URL aplicado a `Ppto Ingresos.tmdl` y `Ppto Retiros.tmdl`.

### Fases ejecutadas

| Fase | Resultado |
|---:|---|
| 0 a 3 | Analisis, decision tecnica e implementacion controlada. |
| 4 y 5 | Cerradas mediante refresh y validacion funcional confirmados por el usuario. |
| 6 | Auditoria PBIP y aislamiento del diff. |
| 7 | Commit tecnico del cambio de fuente. |
| 8 | Publicacion del commit tecnico. |
| 9 | Actualizacion y publicacion de documentacion oficial. |

### Commits publicados

| Tipo | Commit |
|---|---|
| Tecnico | `e287657acc948672b274d7907b736a455428a258` |
| Documental | `a72e1e96b174261251af0ad9f111ef4b4ca0b612` |

### Validaciones de cierre

- Refresh correcto.
- Paginas dependientes sin errores reportados.
- Diff tecnico limitado a tres sustituciones de URL.
- Documentacion oficial actualizada y publicada.
- Cambios locales ajenos preservados fuera de los commits.

### Estado de pendientes

No quedan pendientes dentro del alcance de `PptovsReal.xlsx`. Las migraciones de otras familias de fuentes quedan fuera del alcance de esta Spec.

### Resultado

Plan cerrado satisfactoriamente.
