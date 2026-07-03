@AGENTS.md

---

## Proyecto

Power BI PBIP — People Analytics del Grupo Empresarial Lemco (Challenger, Habitel Hotels, Grupo Sky, Lemco, Fundación Challenger).
Propietario: Edwin Clavijo · People Analytics
Formato: PBIP (texto versionable) — SemanticModel en TMDL + Report en JSON.
Remote: `https://github.com/HarvLopez91/07_Planeacion_de_Personal.git`

**Documentación oficial:** consultar `Docs/` antes de asumir estructura, métricas o comportamiento. El estándar completo de carpetas, nomenclatura y versionamiento vive en [`Docs/ESTRUCTURA_PROYECTO.md`](Docs/ESTRUCTURA_PROYECTO.md) — es la fuente de verdad para todo lo de este documento que no sea específico de Claude Code.

---

## Estructura real del repositorio

```text
PBIP/Proyecto.SemanticModel/definition/
  tables/          → 52 archivos .tmdl (tablas, medidas, Power Query M)
  cultures/        → es-ES.tmdl (localización)

PBIP/Proyecto.Report/definition/
  pages/           → 19 páginas (page.json + visuals/*.json por página)
  bookmarks/       → 20 bookmarks

Docs/     → Documentación oficial, versionada (fuente de verdad)
Outputs/  → Evidencia y diagnósticos locales, NO versionados
Inputs/   → Archivos de entrada puntuales, sin evaluar PII — no versionar sin revisión
Data/     → Datos fuente locales, nunca versionar (contiene PII)
Specs/    → No existe todavía — solo se crea cuando haya un plan que valga versionar antes de implementar
```

---

## Política Docs / Outputs / Specs

- **`Docs/`** = documentación oficial, vigente, **versionada**.
- **`Outputs/`** = evidencia y diagnósticos de trabajo, **local, no versionada**. Nombrar `NN_AAAA-MM-DD_descripcion_corta.md` (`00`=preflight, `01`=diagnóstico base, `02+`=siguientes de la misma línea de trabajo; el contador reinicia por línea de trabajo, no por proyecto completo).
- **`Specs/`** = planes aprobables antes de implementar, solo al adoptarse la carpeta. No crearla sin necesidad real.
- Detalle completo: secciones 9 y 10 de `Docs/ESTRUCTURA_PROYECTO.md`.

---

## Reglas Git

- **Nunca `git add .`** — solo archivos explícitos, ya revisados y aprobados por el usuario.
- Antes de cualquier commit: mostrar `git status`, el/los archivo(s) a incluir y el mensaje propuesto; esperar aprobación explícita.
- Validar identidad antes de comitear: debe quedar `EdwinClavijoChallenger <edwin.clavijo@challenger.co>`.
- Conventional Commits en español: `tipo(alcance): descripción breve`.
- Nunca `git push` sin autorización explícita; nunca force push.
- No usar `--amend`, no saltar hooks, no descartar cambios sin revisar `git status` primero.

---

## PBIP — no tocar sin diagnóstico

- No modificar `relationships.tmdl`, `model.tmdl`, nombres de columnas fuente en tablas de hechos, ni IDs de páginas existentes, sin análisis previo documentado en `Outputs/`.
- Es normal que `PBIP/` aparezca con decenas de archivos modificados solo por abrir/guardar Power BI Desktop — nunca asumir que son cambios funcionales intencionales. Diagnosticar antes de incluir cualquiera en un commit.
- Encoding UTF-8 **sin BOM** obligatorio en `.tmdl` y `.json`.
- Columna `Año` con ñ minúscula en tabla `Años` — nunca `AÑO`.
- Todas las medidas viven en `Tbl_Medidas`; referencias cruzadas: `Tbl_Medidas[NombreMedida]`.

---

## Inputs/ y Data/ — datos personales

- `Data/` nunca se versiona — contiene archivos Excel con datos personales.
- `Inputs/` no se versiona hasta confirmar que su contenido no tiene PII (nombre, cédula, salario, diagnóstico médico). Evaluar caso a caso antes de cualquier `git add` sobre esa carpeta.

---

## Seguridad y privacidad de Talento Humano

Este proyecto maneja datos personales de colaboradores (cédulas, salarios, diagnósticos CIE-10, direcciones, afiliaciones EPS/AFP). Ver `Docs/SECURITY_AND_PRIVACY.md` para el inventario completo por tabla.

- **Sin Row-Level Security (RLS) configurado** — riesgo activo, documentado y no resuelto.
- No exponer, imprimir ni citar datos personales reales en respuestas, commits o documentación.
- Cualquier archivo con PII sigue la regla de `Data/`: no se versiona por defecto.

---

## Idioma

Respuestas, documentación y nombres de medidas/columnas visibles al usuario en **Español de Colombia**, con tildes y eñe correctas (`Año`, `Generación`, `Rango Antigüedad`). No usar variantes mojibake ni anglicismos innecesarios.

---

## Flujo de trabajo

**Diagnóstico → Propuesta → Aprobación → Implementación.**

- No implementar cambios funcionales sin diagnóstico previo.
- Diagnósticos y evidencia van en `Outputs/` (ver convención de nombres arriba).
- Presentar la propuesta y esperar aprobación explícita antes de escribir en `Docs/`, `PBIP/`, o hacer staging/commit/push.
- Actualizar `Docs/` cuando un cambio funcional quede aprobado e implementado.

---

## Validaciones mínimas antes de cerrar una tarea

- `git status --short` revisado — solo lo esperado aparece modificado o staged.
- `git diff --check` sin errores de espacios en blanco.
- Identidad Git confirmada antes de cualquier commit.
- Encoding UTF-8 sin BOM en cualquier `.tmdl`/`.json` tocado.
- `Docs/` actualizado si el cambio es funcional.

---

## Páginas del informe

| ID de página | Nombre | Estado |
| --- | --- | --- |
| ReportSection | Portada | Visible |
| f0fd1eb45022c4c0718e | Demográfico | Oculta |
| ReportSectionf46593dd92bf9359ceef | Demográfico (Promedio) | Visible |
| e1c2430c70e803cf0105 | Comportamiento_HC_Anual_v2 | Oculta |
| ReportSectionddae17c80e69979c7950 | Comportamiento HC Anual | Oculta |
| cb53606ab281b70263cd | Comportamiento_HC_Anual_v3 | Oculta |
| 8bac02805d716481a924 | Comportamiento_HC_Anual_v4 | Oculta |
| ReportSection65569958420c423d90b1 | Productividad | Visible |
| ReportSection10f83a2531afc6f0ce74 | Comportamiento HC Mensual | Visible |
| ReportSectione5ed8d42954b67ebd207 | Product. (Colaboradores) | Visible |
| ReportSection6a1196bf8c963b709405 | Retiros | Visible |
| ReportSectiondc346876696ee4cba0ab | Rotación2 | Visible |
| ReportSectionb8786793985340abe503 | Ausentismos | Visible |
| ReportSection4898baca26ffb5b4ff94 | Selección | Visible |
| 3a3097703dd04ce49097 | Indicadores | Visible |
| 2ee3ca8f42b01e9a6840 | Gasto Laboral | Visible |
| ReportSection7b0e40b552d4038186ba | SST | Visible |
| 3ade8360a92289e7b288 | Fecha de Actualización | Visible |
| 18513b73a4b6e3d9d08c | QA_Demográfico | Visible |

---

## Tablas clave y visuals personalizados

| Tabla | Rol |
| --- | --- |
| `Tbl_Medidas` | Todas las medidas DAX del proyecto |
| `PLANTA DE PERSONAL` | Fact principal — headcount histórico 2024+ |
| `Planta Ppto` | Presupuesto vs real mensual |
| `AUSENTISMOS` | Ausentismo laboral |
| `Incapacidades` | Incapacidades médicas con CIE-10 |
| `Empresas` | Dim — empresas por grupo empresarial |
| `DimPeriodoYM` | Dim calculada — cruce año×mes |

Visuals HTML personalizados (`report.json → publicCustomVisuals`): usar `htmlContent443BE3AD55E043BF878BED274D3A6855` para contenido HTML.

---

## Lo que NO debe tocar Claude Code

- Estructura de relaciones entre tablas (`relationships.tmdl`)
- Nombres de columnas fuente en tablas de hechos
- IDs de páginas existentes
- Cualquier carpeta del estándar corporativo (`Specs/`, `.github/`, etc.) sin aprobación explícita — ver `Docs/ESTRUCTURA_PROYECTO.md` sección 14
