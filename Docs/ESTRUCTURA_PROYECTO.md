# Estándar Corporativo de Estructura — Proyectos Power BI/PBIP de People Analytics

> Documento generado el **2026-07-03** y actualizado el **2026-07-03** a partir del análisis directo del repositorio (`git status`, inventario de carpetas verificado con `ls -d */` y búsqueda recursiva). Complementa [ARCHITECTURE.md](ARCHITECTURE.md) (arquitectura interna del PBIP) con la organización del **repositorio completo** y define el estándar corporativo objetivo para proyectos PBIP de People Analytics del Grupo Empresarial Lemco.

---

## Nota de vigencia 2026-07-17

Este documento conserva el análisis estructural realizado el 2026-07-03 y debe leerse como estándar corporativo y referencia histórica de adopción. El estado real del repositorio evolucionó después de esa fecha:

- El proyecto sí cuenta con Git activo.
- `Docs/` está versionado como documentación oficial.
- `Specs/` existe y contiene análisis de impacto y planes aprobables.
- `Outputs/` se usa como evidencia temporal local y no debe versionarse por defecto.
- `AGENTS.md` y `CLAUDE.md` son parte de las instrucciones operativas versionables.
- `Tools/`, `Assets/` y otras carpetas pueden existir como cambios pendientes o componentes no necesariamente aprobados para commit.
- El repositorio mantiene cambios PBIP acumulados fuera de alcance, por lo que se exige staging selectivo.

Para estado operativo vigente usar [PROJECT_STATUS.md](PROJECT_STATUS.md). Para reglas de Git usar [GIT_GOVERNANCE.md](GIT_GOVERNANCE.md).

---

## 1. Propósito

Este documento define el **estándar corporativo obligatorio** de estructura de carpetas para proyectos Power BI/PBIP de People Analytics, y documenta cómo se compara la estructura **actual y real** de `07_Planeación_de_Personal` contra ese estándar. Sirve como referencia para el propietario del proyecto y para agentes de IA (Claude Code, Codex, GitHub Copilot) que trabajen en él o en otros proyectos PBIP del área.

No reemplaza a [ARCHITECTURE.md](ARCHITECTURE.md), que describe la arquitectura interna del proyecto PBIP (Report/SemanticModel). Este documento cubre el nivel del repositorio: todo lo que está alrededor y encima del PBIP.

---

## 2. Alcance y carácter obligatorio

- La **estructura de 16 carpetas** definida en la sección 5 ("Estándar corporativo de carpetas") es el objetivo obligatorio para todo proyecto PBIP nuevo o migrado de People Analytics.
- Para `07_Planeación_de_Personal` específicamente, este documento **no ejecuta ninguna migración**: no se renombra, mueve, elimina ni crea ninguna carpeta en esta fase. Solo se documenta el estado actual, el estándar objetivo y el mapa de migración preliminar (sección 6).
- Cualquier migración real hacia el estándar requiere primero una **Spec de migración** aprobada (ver sección 6) — no se asume que este documento autorice ejecutar cambios.

---

## 3. Principios de organización

1. **Separar lo oficial de lo temporal.** `Docs/` es la fuente canónica de la documentación oficial, estable y mantenible del proyecto. Los archivos PBIP, scripts y demás artefactos técnicos son la fuente de verdad de la implementación ejecutable.
2. **Versionamiento con criterio.** No versionar datos personales ni archivos binarios, pesados, derivados o temporales que no sean necesarios para el funcionamiento, reproducción o documentación oficial del repositorio. Las excepciones y criterios detallados se rigen por [GIT_GOVERNANCE.md](GIT_GOVERNANCE.md).
3. **Cada carpeta tiene un dueño de propósito único.** Si un archivo no encaja claramente en una carpeta del estándar, es señal de que falta una regla o de que el archivo está mal ubicado.
4. **Reutilizar antes de crear.** Antes de crear una carpeta nueva, verificar si ya existe una ubicación destinada al mismo propósito.
5. **Evitar duplicaciones.** No deben duplicarse estructuras ni crearse ubicaciones innecesarias.
6. **Alcance del sistema de archivos.** No crear, copiar, descargar ni conservar intencionalmente artefactos del proyecto fuera de la raíz del repositorio, salvo autorización expresa del usuario. Se permiten archivos temporales administrados automáticamente por las herramientas cuando sean necesarios para la ejecución, siempre que no se conviertan en entregables, fuentes permanentes ni archivos versionados.
7. **Clasificación por propósito.** La clasificación depende del propósito principal del archivo, no únicamente de su formato.
8. **Adopción gradual, no big-bang.** El estándar define 16 carpetas; un proyecto no necesita tenerlas todas pobladas desde el día uno. Se crean cuando hay contenido real que las justifique (ver sección 14).
9. **Ninguna migración sin Spec.** Pasar de la estructura actual de un proyecto al estándar corporativo es un cambio estructural — requiere análisis de impacto documentado antes de tocar una sola carpeta.
10. **Trazabilidad ante todo.** Todo cambio funcional relevante debe quedar documentado en `Docs/` (oficial), `Specs/` (plan de implementación) u `Outputs/` (huella del proceso).

---

## 4. Estructura actual detectada (verificada)

```text
07_Planeación_de_Personal/
├── .claude/                    # Config local de Claude Code (settings.local.json) — no versionado
├── .git/
├── .gitignore
├── AGENTS.md                   # Reglas para agentes de IA
├── CLAUDE.md                   # Adaptador de AGENTS.md para Claude Code
├── README.md                   # Punto de entrada del repositorio
├── Data/                       # Vacía actualmente — excluida de Git por .gitignore
├── Inputs/                     # 1 archivo: Base_Rotacion_Atraccion_Seleccion.xlsx — sin trackear en Git
├── Docs/                       # Documentación oficial versionada
│   ├── README.md               # Índice y gobierno de Docs/
│   ├── PROJECT_CONTEXT.md
│   ├── ARCHITECTURE.md
│   ├── DATA_MODEL.md
│   ├── METRICS_CATALOG.md
│   ├── DATA_PIPELINE.md
│   ├── BI_GUIDELINES.md
│   ├── SECURITY_AND_PRIVACY.md
│   ├── RUNBOOK.md
│   ├── CHANGELOG.md
│   ├── decisions/README.md     # ADRs (7 decisiones, 3 pendientes)
│   └── Manual Marca Grupo LEMCO.pdf
├── Outputs/                    # Diagnósticos y propuestas generados — excluida de Git por .gitignore
│   ├── documentation/          # Inventarios y diagnósticos de la documentación misma
│   └── *.md                    # Propuestas y registros puntuales de cambios (ver sección 9)
└── PBIP/
    ├── Proyecto7.pbip          # Manifiesto del proyecto (renombrado 2026-06-17, ver commit cfb3a15)
    ├── .gitignore               # Excluye .pbi/cache.abf y .pbi/localSettings.json
    ├── Proyecto.Report/         # Ver ARCHITECTURE.md
    ├── Proyecto.SemanticModel/  # Ver ARCHITECTURE.md
    └── 00_Referencia_Historica/ # Agregada 2026-07 — ver nota abajo
```

**Nota sobre `PBIP/00_Referencia_Historica/` (agregada la semana del 2026-07-17, sin trackear en Git al momento de este análisis):**

Contiene versiones anteriores del reporte en formato `.pbix` (binario, previas a la migración a PBIP) y un tema de color:

| Archivo | Tamaño | Descripción inferida |
|---|---|---|
| `PaletaAzulProfesional.json` | 262 B | Tema/paleta de colores de Power BI Desktop (JSON de tema, sin datos) |
| `Tablero Gerencia Corporativa GH.pbix` | 1,5 MB | Versión histórica de un tablero para Gerencia Corporativa de Gestión Humana (coincide con la audiencia primaria descrita en `PROJECT_CONTEXT.md`) |
| `Tableros_Gestión Humana - Challenger Colombia_V0.0.0.pbix` / `_V1.0.0.pbix` | 3,8 MB / 5,3 MB | Versiones históricas previas a la migración a `Proyecto7.pbip`, específicas de Challenger Colombia |
| `Tableros_Gestión Humana_V0.0.0.pbix` / `_V1.0.0.pbix` | 11 MB / 7,6 MB | Versiones históricas previas a la migración, alcance general del grupo |

**Decisión de versionamiento:**

- `PaletaAzulProfesional.json`: **versionado**. Archivo de texto pequeño, sin datos, sin riesgo.
- Los 5 archivos `.pbix`: **no versionados**, agregados a `.gitignore`. A diferencia de PBIP (que separa definición de datos), un `.pbix` embebe el modelo de datos completo, incluyendo filas importadas. Dado que este proyecto está clasificado como sensibilidad **ALTA** (`SECURITY_AND_PRIVACY.md`) y estos archivos no se abrieron para confirmar su contenido, aplica la misma cautela ya usada para `Inputs/`: la ausencia de datos personales no se asume, se verifica. Además, la regla de `GIT_GOVERNANCE.md` ("no versionar... binarios o archivos pesados que no sean necesarios para el funcionamiento, reproducción o documentación oficial del repositorio") aplica directamente — son referencia histórica, no necesarios para reproducir `Proyecto7.pbip`. Incluirlos requeriría autorización expresa y específica, idealmente después de confirmar en Power BI Desktop que no contienen datos personales sin enmascarar.

**Hallazgos relevantes de este análisis (2026-07-03), verificados con `ls -d */` y búsqueda recursiva de carpetas numeradas (`find . -maxdepth 3 -type d -iname "0*_*"` → sin resultados):**

- La estructura raíz de este proyecto es **plana y sin numeración interna**: `Data/`, `Docs/`, `Inputs/`, `Outputs/`, `PBIP/`. No existen subcarpetas del tipo `00_Fuentes`, `01_PBIP`, `02_Modelo_Datos`, `03_Documentacion`, etc. dentro de este proyecto.
- `Docs/`, `AGENTS.md`, `CLAUDE.md` e `Inputs/` aparecen como `??` (sin trackear) en `git status`. La documentación oficial actual todavía no está versionada.
- `Data/` está vacía hoy, aunque el `README.md` raíz la describe con contenido histórico (`2026/05_Mayo/`). Verificar si ese contenido se movió, se eliminó o nunca se versionó — no se asume nada sin confirmación del usuario.
- No existen las carpetas `Specs/`, `Scripts/`, `Tools/`, `Assets/`, `Tests/`, `Archive/`, `.codex/`, `.agents/`, `.github/`, `.vscode/`.
- No hay `.github/copilot-instructions.md`; las instrucciones de IA viven en `AGENTS.md` (fuente) y `CLAUDE.md` (adaptador).

> **Nota sobre el esquema numerado de origen:** en la solicitud que originó este documento se planteó un mapa de migración partiendo de un esquema numerado (`00_Fuentes`, `01_PBIP`, `02_Modelo_Datos`, `03_Documentacion`, `04_Outputs`, `05_Assets`, `06_Validaciones`). Ese esquema **no corresponde a la estructura real verificada de `07_Planeación_de_Personal`** — puede tratarse de una convención propuesta a futuro para proyectos nuevos, o del esquema de numeración del workspace padre (`01_`…`07_` para los sub-proyectos de People Analytics, ver `CLAUDE.md` raíz del workspace), que es un nivel distinto (numera proyectos completos, no carpetas dentro de un proyecto). La sección 6 usa la estructura real verificada como punto de partida.

---

## 5. Estándar corporativo de carpetas

Estructura **objetivo obligatoria** para proyectos Power BI/PBIP de People Analytics:

```text
PBIP/
Data/
Inputs/
Outputs/
Docs/
Specs/
Scripts/
Tools/
Assets/
Tests/
Archive/
.github/
.claude/
.codex/
.agents/
.vscode/
```

| Carpeta | Propósito | Estado en `07_Planeación_de_Personal` |
|---|---|---|
| `PBIP/` | Proyecto Power BI en formato texto (Report + SemanticModel) | **Existe y se usa** |
| `Data/` | Datos fuente locales de referencia, no versionados | **Existe** (vacía actualmente, ver hallazgo sección 4) |
| `Inputs/` | Archivos de entrada puntuales para análisis | **Existe** |
| `Outputs/` | Diagnósticos, propuestas y evidencias generadas | **Existe y se usa activamente** |
| `Docs/` | Documentación oficial y vigente | **Existe y se usa activamente** |
| `Specs/` | Especificaciones de cambios antes de implementarlos, incl. specs de migración | **Existe y se usa activamente** |
| `Scripts/` | Automatizaciones reutilizables (PowerShell, Python) | **No existe** — pendiente de adopción |
| `Tools/` | Utilidades de soporte al desarrollo, no parte del producto | **No existe** — pendiente de adopción |
| `Assets/` | Recursos gráficos fuente fuera del PBIP | **No existe** — pendiente de adopción |
| `Tests/` | Evidencia de pruebas manuales o checklists de QA | **No existe** — pendiente de adopción |
| `Archive/` | Versiones descontinuadas conservadas fuera del árbol activo | **No existe** — pendiente de adopción |
| `.github/` | Configuración de GitHub (Actions, plantillas, `copilot-instructions.md`) | **No existe** — pendiente de adopción |
| `.claude/` | Configuración local de Claude Code | **Existe** |
| `.codex/` | Configuración específica de Codex, si la herramienta lo exige | **No existe** — hoy Codex lee `AGENTS.md` directamente, sin carpeta propia |
| `.agents/` | Configuración específica de otros agentes, si la herramienta lo exige | **No existe** — mismo criterio que `.codex/` |
| `.vscode/` | Configuración de workspace de VS Code | **No existe** — pendiente de adopción |

**7 de 16 carpetas del estándar ya existen y están en uso** (`PBIP/`, `Data/`, `Inputs/`, `Outputs/`, `Docs/`, `Specs/`, `.claude/`). Las restantes no se crean por adelantado — ver criterio de activación en sección 14.

---

## 6. Mapa de migración desde la estructura actual

**Este mapa es preliminar y exclusivamente informativo.** No autoriza ni ejecuta ningún renombramiento, movimiento, eliminación o creación de carpetas. Toda migración real requiere primero una Spec de migración (ver requisitos al final de esta sección).

Mapa corregido con base en la estructura **real verificada** (no en el esquema numerado hipotético):

| Carpeta real actual | Carpeta objetivo corporativo | Estado / acción |
|---|---|---|
| `Data/` | `Data/` | Ya alineada — sin acción |
| `Inputs/` | `Inputs/` | Ya alineada — sin acción (pendiente evaluar si su contenido debe tratarse como dato personal, ver sección 11) |
| `Outputs/` | `Outputs/` | Ya alineada — sin acción |
| `Docs/` | `Docs/` | Ya alineada — sin acción. `Docs/DATA_MODEL.md` ya cubre la documentación del modelo de datos como archivo dentro de `Docs/`; no se requiere una subcarpeta `Docs/Modelo_Datos/` separada ni mover nada a `Data/` |
| `PBIP/` | `PBIP/` | Ya alineada — sin acción |
| `.claude/` | `.claude/` | Ya alineada — sin acción |
| `Specs/` | `Specs/` | Ya alineada — contiene análisis de impacto y planes aprobables |
| *(no existe)* | `Scripts/` | Pendiente de adopción |
| *(no existe)* | `Tools/` | Pendiente de adopción |
| *(no existe)* | `Assets/` | Pendiente de adopción |
| *(no existe)* | `Tests/` | Pendiente de adopción |
| *(no existe)* | `Archive/` | Pendiente de adopción |
| *(no existe)* | `.github/` | Pendiente de adopción |
| *(no existe)* | `.codex/` | Pendiente de adopción — evaluar primero si Codex realmente necesita carpeta propia además de `AGENTS.md` |
| *(no existe)* | `.agents/` | Pendiente de adopción — mismo criterio que `.codex/` |
| *(no existe)* | `.vscode/` | Pendiente de adopción |

**Sobre el mapa numerado originalmente propuesto** (`00_Fuentes → Inputs/`, `01_PBIP → PBIP/`, `02_Modelo_Datos → Docs/Modelo_Datos/ o Data/`, `03_Documentacion → Docs/`, `04_Outputs → Outputs/`, `05_Assets → Assets/`, `06_Validaciones → Tests/`): se deja registrado aquí como referencia, pero **no aplica a este proyecto** porque `07_Planeación_de_Personal` nunca tuvo subcarpetas numeradas — su estructura interna ya usa nombres directos. Si otro proyecto del workspace (`01_`…`06_`) sí usa subcarpetas numeradas internamente, ese mapa debería verificarse y documentarse en el `ESTRUCTURA_PROYECTO.md` de ese proyecto específico, no en este.

**Antes de ejecutar cualquier migración real** se debe producir una **Spec de migración** que incluya:

1. Análisis de impacto (qué se mueve, qué queda igual).
2. Lista de archivos afectados.
3. Riesgos identificados (incl. referencias rotas dentro del PBIP, enlaces en `Docs/`, rutas usadas por agentes de IA).
4. Validaciones PBIP requeridas (abrir en Power BI Desktop, confirmar que el modelo carga, confirmar `git status` limpio después).
5. Comandos Git exactos a ejecutar (`git mv`, no `mv` + `git add`, para preservar historial).
6. Plan de rollback (cómo revertir si algo falla).

Esa Spec vive en `Specs/`; `Outputs/` se reserva para evidencia, diagnósticos y resultados temporales de la ejecución.

---

## 7. Tabla de carpetas — propósito, contenido, versionamiento y riesgos

| Carpeta | Propósito | Ejemplos de contenido | ¿Versionar? | Riesgos |
|---|---|---|---|---|
| `PBIP/` | Proyecto Power BI en formato texto | `.tmdl`, `.json`, `.pbip` | **Sí** (excepto `.pbi/cache.abf` y `.pbi/localSettings.json`) | Power BI Desktop puede reescribir archivos al guardar; revisar `git status` antes/después de abrir |
| `Docs/` | Documentación oficial y vigente | `ARCHITECTURE.md`, `DATA_MODEL.md`, ADRs | **Sí** | Que se cuele contenido temporal o especulativo (regla en `Docs/README.md`) |
| `Data/` | Datos fuente locales de referencia (Excel con datos personales) | Consolidados anuales, bases crudas | **No** (`.gitignore`) | Contiene PII — nunca forzar el versionamiento |
| `Inputs/` | Archivos de entrada puntuales para análisis o cargas específicas | `Base_Rotacion_Atraccion_Seleccion.xlsx` | **No** recomendado si contiene datos personales — evaluar caso a caso | Hoy no está en `.gitignore` (ver sección 12) |
| `Outputs/` | Diagnósticos, propuestas y evidencias generadas (por IA o manualmente) | Registros pre-commit, inventarios, capturas, pruebas y auditorías | **No** por defecto; solo con aprobación explícita | Puede acumular archivos obsoletos sin fecha de expiración clara |
| `Specs/` | Especificaciones de cambios antes de implementarlos, incl. migraciones estructurales | Plan de una migración de medidas, spec de migración de carpetas | **Sí** | Confundirse con `Outputs/` si no se define el límite (sección 9) |
| `Scripts/` | Automatizaciones reutilizables | Scripts de validación de encoding TMDL | Sí, cuando se adopte | Que contengan credenciales embebidas |
| `Tools/` | Utilidades de soporte al desarrollo, no parte del producto | Conversores, linters propios | Sí, cuando se adopte | Duplicar con `Scripts/` sin criterio claro |
| `Assets/` | Recursos gráficos fuente fuera del PBIP | Logos en alta resolución, plantillas de marca | Sí, cuando se adopte | Duplicar con `PBIP/.../StaticResources/` |
| `Tests/` | Evidencia de pruebas manuales o checklists de QA | Checklist de validación de la página QA_Demográfico | Sí, cuando se adopte | Confundir "evidencia de prueba" con "documentación oficial" |
| `Archive/` | Versiones descontinuadas conservadas fuera del árbol activo | Páginas de reporte eliminadas, versiones anteriores de medidas | Sí, cuando se adopte | Crecer sin límite si no hay política de retención |
| `.github/` | Configuración de GitHub | `copilot-instructions.md`, workflows | Sí, cuando se adopte | — |
| `.claude/` | Configuración local de Claude Code | `settings.local.json` | **No** (config de máquina/usuario) | Puede contener rutas o permisos específicos del equipo local |
| `.codex/` | Configuración específica de Codex | Configuración de herramienta | Evaluar al adoptar | Duplicar instrucciones ya cubiertas por `AGENTS.md` |
| `.agents/` | Configuración específica de otros agentes | Configuración de herramienta | Evaluar al adoptar | Mismo riesgo que `.codex/` |
| `.vscode/` | Configuración de workspace de VS Code | `extensions.json`, `settings.json` | Sí (sin datos sensibles), cuando se adopte | Que incluya rutas absolutas del equipo local |

---

## 8. Reglas por tipo de carpeta

- **PBIP/**: no modificar `relationships.tmdl`, `model.tmdl` ni nombres de columnas fuente sin análisis previo (ver "Lo que NO debe tocar Claude Code" en `CLAUDE.md`). Encoding UTF-8 sin BOM obligatorio.
- **Data/**: nunca versionar. Si se necesita compartir un snapshot, documentar en `Docs/DATA_PIPELINE.md` dónde vive realmente (SharePoint/OneDrive), no copiarlo al repo.
- **Inputs/**: usar solo para archivos de entrada de un análisis puntual y en curso. Si el archivo contiene datos personales, tratarlo igual que `Data/` (no versionar). Revisar y limpiar cuando el análisis concluya.
- **Outputs/**: cada archivo debe tener fecha en el nombre (`AAAA-MM-DD`) y ser prescindible — es huella de proceso, no fuente de verdad.
- **Docs/**: solo contenido vigente, verificable y mantenible. Toda adición pasa la regla ya definida en `Docs/README.md`.
- **Specs/**: describe **qué se va a hacer antes de hacerlo** (análisis de impacto, decisiones pendientes, fases futuras, criterios de aprobación y planes). Se diferencia de `Outputs/` (documenta evidencia o resultados temporales) y de `Docs/` (documenta el estado **vigente**).
- **Scripts/ y Tools/** *(al adoptarse)*: código idempotente, con cabecera de una línea explicando su propósito; nunca credenciales embebidas.
- **Assets/** *(al adoptarse)*: solo recursos fuente; los assets ya integrados al PBIP siguen viviendo en `StaticResources/`.
- **Tests/** *(al adoptarse)*: evidencia de validación manual, no reemplaza pruebas automatizadas (el proyecto no tiene ninguna).
- **Archive/** *(al adoptarse)*: todo archivo movido aquí debe indicar por qué se archivó y desde cuándo.
- **.claude/, .codex/, .agents/**: configuración de herramienta, no documentación de proyecto. `AGENTS.md` en la raíz sigue siendo la fuente única de instrucciones para cualquier agente.
- **.github/** *(al adoptarse)*: cualquier workflow que toque el PBIP debe ser solo de validación (lint de JSON/TMDL), nunca de publicación automática sin aprobación humana.
- **.vscode/** *(al adoptarse)*: no incluir rutas absolutas ni credenciales.

---

## 9. Política de archivos `.md`

Reglas base:

- **`Specs/`** = especificaciones, requisitos, análisis de impacto, diseños técnicos y planes de implementación.
- **`Outputs/`** = resultados temporales, diagnósticos, evidencias, exportaciones y archivos generados durante la ejecución.
- **`Docs/`** = documentación oficial, estable, mantenible y vigente del proyecto.
- **Runbooks y ADRs pertenecen a `Docs/`** — no son una categoría aparte de esta política: `Docs/RUNBOOK.md` y `Docs/decisions/` ya son documentación oficial y siguen la misma regla que cualquier otro documento de `Docs/`.

| Tipo | Dónde vive | Características |
|---|---|---|
| **Documentación oficial** (incl. runbooks y ADRs) | `Docs/` | Vigente, verificable, versionada, mantenida. `Docs/RUNBOOK.md` y `Docs/decisions/` son documentación oficial, no una categoría distinta. Pasa la regla de `Docs/README.md` |
| **Diagnósticos y evidencia operativa** | `Outputs/` (raíz) | Local, no versionada. Snapshot de un análisis o validación puntual, con fecha en el nombre. No se actualiza — se reemplaza por uno nuevo. Sigue la convención `NN_` de la sección 10 |
| **Specs** | `Specs/` | Análisis de impacto, requisitos, decisiones pendientes, fases futuras, criterios de aprobación y planes antes de implementar; una vez implementado, el estado estable relevante pasa a `Docs/` o al ADR correspondiente |
| **Resultados de prompts / registros de sesión** | `Outputs/` (raíz) | Registros de una sesión de trabajo con IA, con fecha |
| **Análisis temporales** | `Outputs/` (raíz) | Cualquier `.md` generado para responder una pregunta puntual que no se vuelve referencia permanente |

**Ubicación de diagnósticos dentro de `Outputs/` (actualizado 2026-07-03):** los diagnósticos operativos (preflight Git, diagnóstico de codebase y similares) se guardan en la **raíz de `Outputs/`**, siguiendo la convención `NN_` de la sección 10 — así quedaron `Outputs/00_2026-07-03_preflight_git.md` y `Outputs/01_2026-07-03_diagnostico_codebase.md`. `Outputs/documentation/` queda como ubicación **opcional e histórica**: solo se retoma si en el futuro se decide agrupar un volumen alto de documentos de diagnóstico documental en una subcarpeta dedicada. No es obligatoria ni es la ubicación por defecto actual.

Regla simple: **si el archivo define requisitos, diseño o plan antes de implementar → `Specs/`; si documenta evidencia o resultado temporal de ejecución → `Outputs/`; si documenta el estado oficial y mantenible del proyecto → `Docs/`.**

Ejemplos:

- Análisis de impacto de un cambio de fuente → `Specs/`.
- Diagnóstico generado por un script → `Outputs/`.
- Arquitectura oficial implementada → `Docs/`.

---

## 10. Reglas de nombres

| Elemento | Convención | Ejemplo |
|---|---|---|
| Carpetas de dominio (nivel workspace) | `NN_Nombre_Con_Guion_Bajo` | `07_Planeación_de_Personal` |
| Carpetas internas del proyecto (estándar corporativo) | Nombre directo, sin numeración | `Docs/`, `Inputs/`, `Outputs/`, `Specs/` |
| Documentación oficial en `Docs/` | `MAYUSCULAS_CON_GUION_BAJO.md`, en inglés técnico | `DATA_MODEL.md`, `SECURITY_AND_PRIVACY.md` |
| **Archivos en `Outputs/` (convención oficial vigente)** | `NN_AAAA-MM-DD_descripcion_corta.md`, usando el siguiente consecutivo disponible | `00_2026-07-03_preflight_git.md`, `01_2026-07-03_diagnostico_codebase.md` |
| Archivos en `Outputs/` (convención alternativa/histórica) | `descripcion_corta_en_minusculas_AAAA-MM-DD.md` | `ajuste_antiguedad_demografico_promedio_2026-06-17.md` — válida para registros puntuales que no forman parte de una línea de trabajo numerada |
| Specs | `NNNN_tipo_descripcion_corta.md`, usando el siguiente consecutivo disponible | `0008_plan_implementacion_correccion_productividad_contexto_negocio.md` |
| Scripts *(al adoptarse)* | `verbo_objeto.ps1` / `.py`, minúsculas con guion bajo | `validar_encoding_tmdl.ps1` |
| Assets *(al adoptarse)* | minúsculas con guion, sin espacios | `logo-lemco-horizontal.png` |
| Tablas y medidas TMDL | Ver `CLAUDE.md` del proyecto (ej. columna `Año` con ñ minúscula) | — |

### Significado del prefijo `NN_` en `Outputs/`

`NN_` es un contador de dos dígitos asignado con el **siguiente consecutivo
disponible en `Outputs/`** al momento de crear el archivo:

| `NN_` | Significado |
|---|---|
| `00` | Primer archivo histórico de la secuencia |
| `01` | Segundo archivo histórico de la secuencia |
| `02` en adelante | Evidencias o resultados posteriores, en orden de creación |

El consecutivo no se reinicia por sesión ni por línea de trabajo. Antes de
crear un Output se debe inventariar `Outputs/`, identificar el mayor prefijo
`NN_` existente y usar el siguiente valor. La fecha y la descripción
conservan el contexto funcional; el número evita colisiones y mantiene una
secuencia única. Si se supera `99`, se amplía el ancho del prefijo sin
renumerar archivos existentes.

Evitar espacios en nombres de archivo nuevos cuando sea posible (los existentes con espacio, como `Selección Challenger.tmdl`, se mantienen — no renombrar sin autorización).

---

## 11. Reglas de versionamiento Git

**Sí versionar:**
- `PBIP/` completo (excepto `.pbi/cache.abf` y `.pbi/localSettings.json`)
- `Docs/` completo
- `README.md`, `AGENTS.md`, `CLAUDE.md`
- `.gitignore`

**No versionar:**
- `Data/` — contiene archivos Excel con datos personales
- `Outputs/` — salidas temporales, solo con aprobación explícita y justificación de trazabilidad formal
- Cachés de Power BI (`**/.pbi/cache.abf`)
- Configuración local (`**/.pbi/localSettings.json`, `.claude/settings.local.json`)
- Archivos temporales del sistema operativo y de Office (`Thumbs.db`, `~$*.xlsx`, `desktop.ini`)

**Archivos sensibles / datos personales:** cualquier archivo con nombres, cédulas, salarios o datos de incapacidades médicas debe evaluarse contra `Docs/SECURITY_AND_PRIVACY.md` antes de considerarse para versionar. Por defecto, no se versiona.

**Pendiente de decisión del usuario:** `Inputs/` no está hoy en `.gitignore` y contiene un archivo Excel (`Base_Rotacion_Atraccion_Seleccion.xlsx`) sin trackear. Si ese archivo tiene datos personales, debería tratarse como `Data/` (ver sección 12).

---

## 12. Recomendaciones para `.gitignore`

El `.gitignore` actual ya cubre lo esencial:

```gitignore
Data/
Outputs/
**/.pbi/cache.abf
**/.pbi/localSettings.json
Thumbs.db
desktop.ini
.DS_Store
*.tmp
*.bak
~$*.xlsx
~$*.docx
```

**Recomendación (no aplicada — requiere confirmación del usuario):** evaluar agregar `Inputs/` si los archivos que contiene tienen datos personales, siguiendo el mismo criterio que `Data/`. Hoy `Inputs/Base_Rotacion_Atraccion_Seleccion.xlsx` aparece como sin trackear y podría versionarse por accidente en el próximo `git add`.

Si en el futuro se adoptan `Scripts/` o `Tools/`, agregar reglas para no versionar credenciales (`*.env`, `secrets.*`).

---

## 13. Buenas prácticas para trabajo con IA

- **Claude Code / Codex / GitHub Copilot** leen `AGENTS.md` (fuente) y `CLAUDE.md` (adaptador específico) en la raíz del proyecto — mantenerlos sincronizados si se actualiza uno.
- **No implementar sin diagnóstico.** Antes de un cambio funcional, generar o consultar el diagnóstico correspondiente en `Outputs/` o la Spec aplicable.
- **No mover archivos sin análisis de impacto.** Especialmente en `PBIP/` — un archivo movido puede romper referencias internas del modelo o del reporte. Para migraciones estructurales, ver requisito de Spec en sección 6.
- **Documentar resultados en `Outputs/`**, nunca en `Docs/` directamente; la promoción a `Docs/` es una decisión explícita del usuario.
- **Documentar planes en `Specs/`** cuando el cambio requiera análisis aprobable antes de implementar. Los diagnósticos y evidencias de ejecución se guardan en `Outputs/`.
- **Confirmar antes de commit/push.** Ningún agente ejecuta `git commit`, `git push` ni publica sin aprobación explícita (regla ya vigente en `AGENTS.md` y `CLAUDE.md`).

---

## 14. Plan de adopción gradual del estándar corporativo

Ninguna de las 10 carpetas pendientes se crea por adelantado. Criterio de activación:

| Carpeta | Se crea cuando... |
|---|---|
| `Specs/` | Ya existe; mantenerla para análisis de impacto y planes aprobables antes de implementar |
| `Scripts/` | Se escriba el primer script reutilizable (hoy no hay ninguno en el repo) |
| `Tools/` | Se necesite una utilidad de soporte que no es un script de un solo uso |
| `Assets/` | Se gestionen recursos gráficos fuente fuera del propio PBIP |
| `Tests/` | Se formalice un proceso de QA manual más allá de la página `QA_Demográfico` ya existente en el reporte |
| `Archive/` | Se decida conservar fuera del árbol activo algo que hoy se maneja como "página oculta" dentro del PBIP (ver ADR-005 en `Docs/decisions/README.md`) |
| `.github/` | Se activen GitHub Actions o se formalicen plantillas de PR/Issue |
| `.codex/` | Se confirme que Codex requiere configuración propia más allá de `AGENTS.md` |
| `.agents/` | Se confirme que algún otro agente requiere configuración propia más allá de `AGENTS.md` |
| `.vscode/` | El equipo crezca y se necesite configuración de workspace compartida |

Este documento se debe actualizar cada vez que se active una de estas carpetas, moviéndola de "pendiente" a "existente" en las secciones 4, 5, 6 y 7.

---

## 15. Checklist antes de crear, mover o eliminar carpetas

- [ ] ¿Hay contenido real que justifique la carpeta hoy (no "por si acaso")?
- [ ] ¿Ya existe una carpeta del estándar que cubra este propósito? (revisar sección 5)
- [ ] ¿Es una migración estructural (renombrar/mover una carpeta existente)? Si es así, ¿existe una Spec de migración aprobada con análisis de impacto, archivos afectados, riesgos, validaciones PBIP, comandos Git y plan de rollback? (sección 6)
- [ ] ¿Se documentó el motivo en `Outputs/`, `Specs/` o en la conversación con el usuario?
- [ ] ¿Se tiene autorización explícita del usuario para crear/mover/eliminar/renombrar? (regla transversal de `AGENTS.md`)
- [ ] ¿Se actualizó este documento (secciones 4, 5, 6, 7) si la carpeta es nueva o cambió de estado?
- [ ] ¿El `.gitignore` necesita ajuste por la carpeta nueva?

---

## 16. Checklist antes de commit

- [ ] `git status` revisado — ningún archivo de `Data/` ni de `Outputs/` (sin aprobación) en el stage
- [ ] Si el commit toca `PBIP/`, confirmar que Power BI Desktop está cerrado y que los cambios son intencionales (no reescritura automática)
- [ ] Encoding UTF-8 sin BOM verificado en `.tmdl`/`.json` modificados
- [ ] Documentación oficial (`Docs/`) actualizada si el cambio es funcional
- [ ] Mensaje de commit en Conventional Commits en español (`tipo(alcance): descripción`)
- [ ] Aprobación explícita del usuario obtenida antes de ejecutar el commit

---

## 17. Próximos pasos recomendados

1. Confirmar con el usuario si `Docs/`, `AGENTS.md`, `CLAUDE.md` e `Inputs/` deben incorporarse al próximo commit (hoy están sin trackear).
2. Confirmar el estado real de `Data/` (vacía actualmente) frente a lo descrito en `README.md` raíz — puede requerir actualizar ese README o recuperar el contenido esperado.
3. Decidir si `Inputs/Base_Rotacion_Atraccion_Seleccion.xlsx` contiene datos personales; si es así, agregar `Inputs/` al `.gitignore`.
4. Revisar los ~150 archivos modificados en `PBIP/` (bookmarks, visuals, tablas) para confirmar si son cambios intencionales o reescritura de Power BI Desktop, antes de cualquier commit.
5. Cuando el usuario lo apruebe, referenciar este documento desde `Docs/README.md` y desde la sección "Estructura del repositorio" de `README.md` (raíz) — pendiente, no incluido en esta entrega por decisión explícita del usuario.
6. Si se decide avanzar con la migración real hacia el estándar corporativo (sección 6), elaborar primero la Spec de migración correspondiente antes de ejecutar cualquier `git mv`.
7. Evaluar si este documento debe replicarse (adaptado) en otros proyectos PBIP del workspace de People Analytics para que el estándar corporativo sea consistente en todos ellos.

---

## 18. Criterio de actualización documental por cambio

Matriz de referencia para decidir **qué documento actualizar** según el tipo de cambio realizado en el proyecto. Úsala antes de cerrar cualquier tarea (ver checklist de la sección 16 y la regla equivalente en `CLAUDE.md`).

| Tipo de cambio | Documento que debe actualizarse | Evidencia esperada | ¿Requiere commit separado? | Observación |
|---|---|---|---|---|
| Estructura de carpetas | `Docs/ESTRUCTURA_PROYECTO.md` (secciones 4-7) | Árbol y tabla de carpetas con el nuevo estado | Sí, si coexiste con otros cambios funcionales | Nunca ejecutar la migración sin Spec previa (sección 6) |
| Modelo semántico (orden de tablas, grupos de consulta, cultura) | `Docs/ARCHITECTURE.md` | Diagrama de capas y tabla de grupos de consulta actualizados | Sí | Diagnosticar antes de tocar `PBIP/` (ver `CLAUDE.md`) |
| Tablas (agregar, quitar, renombrar) | `Docs/DATA_MODEL.md` (+ `Docs/ARCHITECTURE.md` si cambia el conteo total) | Fila nueva/actualizada en la clasificación de tablas | Sí | Verificar el conteo real con `ls` antes de escribir un número — no asumir |
| Relaciones | `Docs/DATA_MODEL.md` (sección Relaciones) | Fila nueva en la tabla del eje correspondiente | Sí | Evaluar cardinalidad y riesgo; actualizar "Riesgos del modelo" si aplica |
| Medidas DAX | `Docs/METRICS_CATALOG.md` | Medida documentada con fórmula simplificada, formato y dominio | No necesariamente | Si es un cambio relevante, agregar también entrada en `Docs/CHANGELOG.md` |
| Power Query (transformaciones M) | `Docs/DATA_PIPELINE.md` | Paso de transformación agregado al flujo correspondiente | No necesariamente | Si cambia una fuente o ruta, revisar también `Docs/SECURITY_AND_PRIVACY.md` |
| Fuentes de datos (nuevo archivo, nueva cuenta SharePoint) | `Docs/DATA_PIPELINE.md` (+ `Docs/SECURITY_AND_PRIVACY.md` si aplica) | Fila nueva en el inventario de fuentes | Sí | Evaluar PII antes de documentar nombres de archivo o cuentas |
| Visuales / páginas | `Docs/BI_GUIDELINES.md` | Fila actualizada en el inventario de páginas o bookmarks | Sí | Verificar conteo real (`ls pages/`, `ls bookmarks/`) antes de escribir un número |
| Seguridad / PII / RLS | `Docs/SECURITY_AND_PRIVACY.md` (+ ADR en `Docs/decisions/` si es una decisión) | Campo o tabla agregado al inventario de PII, o estado de RLS actualizado | Sí, commit propio | Máxima prioridad — nunca diferir |
| Operación / publicación / refresh | `Docs/RUNBOOK.md` | Procedimiento actualizado o problema conocido agregado | No necesariamente | Verificar que cualquier nombre de archivo o ruta citada siga vigente (ej. `Proyecto7.pbip`) |
| Decisiones técnicas | `Docs/decisions/README.md` (nuevo ADR) | ADR con contexto, opciones, decisión y consecuencias | Sí, commit propio | Actualizar también el índice de decisiones en el mismo archivo |
| Cambios funcionales relevantes | `Docs/CHANGELOG.md` | Entrada nueva con fecha y descripción | No necesariamente | Es el resumen ejecutivo del historial — no reemplaza los documentos específicos |
| Diagnósticos temporales | `Outputs/` (`NN_AAAA-MM-DD_descripcion_corta.md`) | Archivo de diagnóstico con fecha en el nombre | No (`Outputs/` no se versiona por defecto) | Nunca en `Docs/` — regla ya definida en `Docs/README.md` |
| Planes de implementación | `Specs/` | Plan con análisis de impacto, criterios de aprobación y fases | Sí, cuando el plan deba conservar trazabilidad | Ver secciones 6 y 14 de este documento |
| Reglas de IA | `AGENTS.md` (fuente) + `CLAUDE.md` (adaptador) | Regla nueva documentada en ambos si aplica a todos los agentes, o solo en `CLAUDE.md` si es específica de Claude Code | Sí, commit propio | Mantener sincronizados — ver sección 13 |
| Cambios en `README.md` | `README.md` (raíz) | Sección o tabla actualizada | Sí | Requiere autorización explícita separada del resto del cambio |
| Cambios en `.gitignore` | `.gitignore` (+ sección 12 de este documento si cambia la política) | Regla nueva en `.gitignore` y su justificación documentada | Sí, commit propio | Nunca agregar una regla sin documentar el riesgo que mitiga |

Regla simple: **si terminaste una tarea y no sabes si falta actualizar algo, busca el tipo de cambio en esta tabla antes de cerrarla.**
