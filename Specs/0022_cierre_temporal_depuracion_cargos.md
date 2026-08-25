# Cierre temporal — Depuración de Cargos (Maestro Kactus + Consolidado 2025)

Fecha: 2026-08-25

Estado: **PAUSADO / CIERRE TEMPORAL.** Cierre documental y de versionamiento
únicamente — el estado funcional (QA, pendientes) permanece abierto. No
declarar esta iniciativa como `Finalizada` en el roadmap sin evidencia de que
los pendientes de la sección 10 se resolvieron.

Rama: `feat/cierre-temporal-depuracion-cargos-2026`. Worktree:
`C:\tmp\wt07-cierre-depuracion-cargos` (fuera de OneDrive, ver sección 12).
Base: `origin/main` en `7d26cf1f3c096ff74b37e1973e6d4ea3b9217fe4`.

---

## 1. Objetivo original de la tarea

Construir una tabla operativa de **cargos** (no de empleados) a partir de los
8 archivos Excel del Maestro de Cargos-Roles Kactus, enriquecida con
`Dependencia`/`Área` desde `Consolidado 2025.xlsx` (periodo julio 2026), de
forma reproducible, documentada y auditable — insumo para una tarea de
depuración de cargos por parte de Planeación de Personal.

## 2. Fuentes

| Fuente | Ruta | Uso |
|---|---|---|
| Maestro de Cargos-Roles Kactus (8 archivos) | `Data/Maestro_Cargos-Roles_Kactus/Insumos_Vigentes/` | Catálogo base de cargos (Fase 1) |
| Consolidado mensual | `Data/HeadCount/2025/Consolidado 2025.xlsx`, hoja `Consolidado2025` | Enriquecimiento Dependencia/Área, periodo julio 2026 (Fase 2) |

Ambas quedan fuera de Git (`Data/` excluida por `.gitignore`), no se
modifican ni se versionan.

`Data/Contratos_Kactus/Insumos_Vigentes/` es una fuente **distinta**, de un
módulo relacionado pero fuera de alcance de esta tarea (ver sección 8 y
`Reglas_Normalizacion_Empresa_Contratos_Kactus.md` sección 12). No se leyó
ni se procesó en esta tarea.

## 3. Granularidad

`Empresa + Número de cargo` — validada empíricamente como clave 100% única
sobre las 2 004 filas consolidadas de los 8 archivos Kactus (0 duplicados
exactos, 0 claves repetidas con atributos distintos).

## 4. Notebook

`Outputs/Depuracion_Cargos/01_construccion_tabla_depuracion_cargos.ipynb`
(versionado en este cierre, ver sección 11). 50 celdas (25 de código),
organizado en dos fases:

- **Fase 1** (secciones 1-9 del notebook): consolidación de los 8 archivos
  Kactus como DataFrame en memoria. No exporta ningún Excel intermedio.
- **Fase 2** (secciones 10-19): enriquecimiento con `Consolidado 2025.xlsx`
  (julio 2026), aplicación de las 11 reglas de normalización de Empresa
  (sección 5), y exportación del único Excel del pipeline.

## 5. Excel operacional (NO versionado)

`Outputs/Depuracion_Cargos/Tabla_Depuracion_Cargos.xlsx` — salida local,
excluida de Git. 3 hojas:

1. `Depuracion_Cargos` — tabla final, 2 004 filas, 11 columnas exactas
   (`Número de cargo`, `Fecha de creación`, `Ind. Actividad`,
   `Nombre del cargo`, `Número de cargos`, `Cargos ocupados`, `Dependencia`,
   `Área`, `Fecha de actualización`, `Empresa`, `Nombre Empresa`).
2. `QA_Conciliacion` — control por `Empresa + Número de cargo`: presencia en
   el cierre julio 2026, colaboradores activos, estado de conciliación,
   número de Dependencias/Áreas distintas, observación QA.
3. `Conflictos_Dependencia_Area` — evidencia de las 80 claves conflictivas
   del lookup de Consolidado, con columna `Existe en catálogo Kactus`
   (Sí/No) para distinguir las 77 con match Kactus de las 3 sin match.

## 6. Reglas de negocio — Empresa

Documentadas íntegramente en
`Outputs/Depuracion_Cargos/Reglas_Normalizacion_Empresa_Contratos_Kactus.md`
(versionado en este cierre, ver sección 11): catálogo de 11 reglas
`Nombre Empresa (Consolidado) → Empresa Kactus`, casos especiales LEMCO/LEMCO
SALVIO y HABITEL S.A.S., catálogo Tipo de Nómina, columnas técnicas
descartadas como identificador legal, e impacto cuantitativo del mapeo.

## 7. Periodo

**Julio de 2026**, confirmado como el periodo máximo disponible en
`Consolidado 2025.xlsx` al momento de esta ejecución (rango completo: enero
2025 → julio 2026, 2 572 filas en julio 2026). Codificado explícitamente en
el notebook (`PERIODO_AUTORIZADO = (2026, "07.Julio")`) — no cambia
automáticamente a un mes posterior sin confirmación previa (ver pendiente 9,
sección 10).

## 8. Reglas de transformación — módulo Contratos Kactus (contexto adicional)

El usuario confirmó que el mismo catálogo de 11 reglas de normalización de
Empresa (sección 6) aplica también al módulo, distinto y fuera de alcance,
de `Data/Contratos_Kactus/Insumos_Vigentes/` (ver DATA-011 en
`Specs/00_roadmap_y_backlog.md`). Se documentó como referencia para su
futura automatización en
`Reglas_Normalizacion_Empresa_Contratos_Kactus.md` sección 12, con
advertencia explícita de no confundir los nombres físicos de archivo entre
ambos módulos.

## 9. Metodología de conciliación

1. Consolidar los 8 archivos Kactus (Fase 1), sin deduplicar, con QA
   completo de calidad de dato.
2. Cargar `Consolidado 2025.xlsx`, filtrar julio 2026, y reconstruir
   `Empresa Kactus` desde `Nombre Empresa` usando el catálogo de 11 reglas
   (validado empíricamente por solapamiento de `COD. CARGO` contra el
   catálogo Kactus — 96.8%-100%).
3. Construir el lookup `Empresa + COD. CARGO → Dependencia/Área`; si una
   clave tiene una única combinación, se asigna; si tiene varias, queda como
   conflicto documentado (hoja `Conflictos_Dependencia_Area`), nunca elegida
   arbitrariamente.
4. Clasificar cada uno de los 2 004 cargos Kactus en un estado de
   conciliación: `Con presencia en cierre julio-2026`,
   `Sin presencia en cierre julio-2026`, `Dependencia/Área múltiple`, o
   `Empresa no conciliable automáticamente` (0 casos con las reglas
   actuales).
5. `Ind. Actividad` de Kactus se conserva intacto; se contrasta (sin
   sobrescribir) contra la presencia real en el cierre — ver
   `Reglas_Normalizacion_Empresa_Contratos_Kactus.md` sección 11.

## 10. QA final (validado contra el Excel vigente, 2026-08-25)

| Métrica | Valor |
|---|---|
| Cargos totales | 2 004 |
| Dependencia/Área única | 270 |
| Dependencia/Área múltiple (cargos Kactus) | 77 |
| Claves conflictivas del lookup (total / con match Kactus / sin match Kactus) | 80 / 77 / 3 |
| Sin presencia en cierre julio 2026 | 1 657 |
| Empresa no conciliable automáticamente | 0 |
| `Ind. Actividad = A` + presente | 347 |
| `Ind. Actividad = A` + ausente | 144 |
| `Ind. Actividad != A` + presente | 0 |
| `Ind. Actividad != A` + ausente | 1 513 |
| Discrepancias `Cargos ocupados` vs. colaboradores activos julio 2026 | 1 001 de 2 004 comparables |
| Casos `Cargos ocupados > Número de cargos` | 68 |
| `Fecha de creación` vacía | 9 |
| **`Cargos ocupados` negativo** (hallazgo nuevo, 2026-08-25) | **96** |
| **`Número de cargos` vacío** (hallazgo nuevo, 2026-08-25; no capturado por el QA de Fase 1) | **28** |
| `Fecha de actualización` | Vacía en las 2 004 filas (intencional — ver sección 13) |
| Duplicados `Empresa + Número de cargo` | 0 |

## 11. Terminado

- Consolidación de los 8 archivos Kactus, 2 004 cargos, clave única, 0
  duplicados.
- `HABITEL SAS.xlsx` conciliado como Empresa Kactus 6, `OPERADORA HABITEL
  SAS.xlsx` como Empresa Kactus 10 — los 315 cargos previamente ambiguos
  quedaron resueltos (0 sin resolver).
- Regla `LEMCO SALVIO → Empresa Kactus 7` implementada y validada: 32 de los
  362 cargos de `LEMCO SAS.xlsx` cambiaron de estado de conciliación (27
  "Sin presencia" → "Con presencia"; 3 "Con presencia" → "Múltiple"; 2 "Sin
  presencia" → "Múltiple").
- Excel operacional con 3 hojas generado y verificado.
- Notebook reproducible ejecutado de principio a fin sin errores contra las
  fuentes vigentes al 2026-08-24.
- Archivos redundantes (copias de conflicto de OneDrive `-Mexico`, Excel
  intermedios `Tabla_Depuracion_Cargos_Base_Kactus.xlsx` y
  `Conflictos_Dependencia_Area.xlsx` independientes) auditados y eliminados
  de `Outputs/Depuracion_Cargos/` — la carpeta operativa contiene únicamente
  los 3 archivos canónicos.

## 12. Pendientes (tarea PAUSADA, no finalizada)

1. Revisar los 144 cargos `Ind. Actividad = A` sin colaborador activo en
   julio 2026 — no asumir inactivación automática.
2. Revisar los 77 cargos Kactus con múltiples combinaciones
   Dependencia/Área — no elegir una arbitrariamente.
3. Analizar las 1 001 discrepancias `Cargos ocupados` (Kactus) vs.
   colaboradores activos del cierre mensual.
4. Investigar el significado funcional de los 96 valores negativos en
   `Cargos ocupados`.
5. Revisar los 68 casos `Cargos ocupados > Número de cargos`.
6. Revisar los 28 cargos con `Número de cargos` vacío y corregir el chequeo
   de QA de Fase 1 que no los capturó como inválidos.
7. Definir si se requiere una fuente adicional para resolver cargos
   transversales con múltiples Dependencias/Áreas.
8. Automatizar en el futuro: LEMCO vs. LEMCO SALVIO (Planeación + CCO +
   cargo) y clasificación fina de HABITEL (Clase/Tipo de Nómina + base de
   Unidades Hoteleras).
9. Parametrizar el notebook para futuros periodos — julio 2026 está
   codificado explícitamente; no cambiar de mes sin confirmar antes que
   sigue siendo el máximo disponible en Consolidado.
10. Diligenciar `Fecha de actualización` únicamente cuando la depuración
    funcional se cierre realmente.
11. Registrar esta iniciativa con un ID estable en
    `Specs/00_roadmap_y_backlog.md` (no se hizo en este cierre — fuera del
    alcance del diff autorizado, ver sección 14).
12. Actualizar `Docs/DATA_PIPELINE.md` cuando se decida promover las reglas
    de Empresa a documentación oficial versionada (hoy viven intencionalmente
    en `Outputs/` como excepción de gobierno).

## 13. Riesgos

- **Cobertura de Dependencia/Área es baja (13.5%)** porque Kactus es un
  catálogo de plantillas de cargo (activos e inactivos, ocupados o no)
  mientras que Consolidado solo refleja empleados activos en un mes puntual
  — riesgo de interpretación errónea si se lee la baja cobertura como
  defecto de calidad en vez de como hallazgo esperado de depuración.
- **96 `Cargos ocupados` negativos y 28 `Número de cargos` vacíos** no
  investigados — riesgo de arrastrar un problema de calidad de dato no
  diagnosticado si se usa esta tabla sin revisar antes esos casos.
- **Sincronización de OneDrive**: la carpeta operativa vive dentro de
  OneDrive y ya generó copias de conflicto (`-Mexico`) y resurrección de
  archivos eliminados durante esta tarea (ver historial de esta sesión). Se
  mitigó pausando OneDrive manualmente durante las operaciones de limpieza;
  el riesgo reaparece si se opera sobre `Outputs/Depuracion_Cargos/` con
  OneDrive activo y sincronización concurrente desde otra máquina/perfil.
- **Entorno histórico de generación distinto del entorno actual preparado.**
  El Excel `Tabla_Depuracion_Cargos.xlsx` vigente (con las cifras de la
  sección 10) se generó originalmente con un entorno temporal Python 3.11
  fuera del repositorio, no con el `.venv` del proyecto — ver sección 15
  para el detalle histórico completo. Posteriormente se dejó preparado el
  `.venv` del proyecto (Python 3.14.3, `ipykernel` 7.3.0, kernel
  `planeacion_personal` registrado) como entorno para retomar la tarea. Un
  kernel registrado con `--user` es local al perfil/máquina donde se
  registró — si se retoma desde otra máquina o perfil de Windows, puede
  requerir registrarlo nuevamente (ver sección 15).

## 14. Reglas no automatizables

1. LEMCO vs. LEMCO SALVIO — depende de una base externa de Planeación de
   Personal (CCO + cargo) no presente en el repositorio.
2. Asignación fina dentro de HABITEL S.A.S. — depende de Clase/Tipo de
   Nómina y una base adicional de Unidades Hoteleras no presente en el
   repositorio.
3. Códigos de Tipo de Nómina 1, 4, 100-103, 202-204 — sin regla de
   conciliación confirmada.
4. Variantes adicionales de `Nombre Empresa` para LEMCO SAS más allá de
   `LEMCO` y `LEMCO SALVIO` — no confirmadas.

## 15. Kernel / entorno necesario

Dos hechos distintos, que no deben mezclarse:

### A. Histórico — entorno con el que se generó el Excel vigente

El Excel `Tabla_Depuracion_Cargos.xlsx` y las cifras QA de la sección 10 de
esta Spec se generaron y validaron con un entorno **temporal fuera del
repositorio** (`C:\tmp\dcvenv`, Python 3.11.0, `pandas==3.0.5`,
`openpyxl==3.1.5`, `nbformat`, `nbclient`), **no con el `.venv` del
proyecto**. Este es un hecho histórico de cómo se produjo la entrega
vigente — no describe el estado actual del `.venv`.

### B. Estado actual — entorno preparado para retomar la tarea

Posteriormente se dejó preparado el `.venv` del proyecto
(`.venv\Scripts\python.exe`) con:

- Python **3.14.3**
- `pandas` **3.0.5**
- `openpyxl` **3.1.5**
- `ipykernel` **7.3.0**
- Kernel Jupyter registrado: name `planeacion_personal`, display name
  `Python 3.14 - Planeacion Personal`

Esta es la configuración que debe seleccionarse para **retomar** la
ejecución del notebook (metadata `kernelspec`/`language_info` del notebook
ya está alineada con este entorno). **El Excel vigente no fue regenerado
bajo este entorno** — quien retome la tarea deberá ejecutar el notebook
completo con este kernel para producir una nueva entrega verificada bajo
Python 3.14.3, y solo entonces las cifras de la sección 10 quedarán
confirmadas también bajo este entorno.

Un kernel registrado con `--user` (como se hizo con `planeacion_personal`)
es **local al perfil de Windows y a la máquina donde se registró**. Si se
retoma esta tarea desde otra máquina o perfil distinto, verificar primero:

```powershell
jupyter kernelspec list
```

Si `planeacion_personal` no aparece, registrarlo de nuevo desde ese
perfil/máquina:

```powershell
.venv\Scripts\python.exe -m pip show ipykernel
.venv\Scripts\python.exe -m ipykernel install --user --name planeacion_personal --display-name "Python 3.14 - Planeacion Personal"
```

Si el `.venv` no existe o apunta a una ruta inválida en la máquina actual,
recrearlo con el Python 3.14.x disponible localmente e instalar
`requirements.txt` antes de intentar ejecutar el notebook.

## 16. Advertencia OneDrive

`Outputs/Depuracion_Cargos/` vive dentro de una carpeta sincronizada por
OneDrive compartida entre al menos dos perfiles de Windows del mismo
usuario (`eclavijo` y `edwin.clavijo`). Durante esta tarea se observaron:
copias de conflicto con sufijo `-Mexico`, y reaparición de archivos
eliminados con contenido de una versión anterior. **Antes de operar sobre
esa carpeta (editar, eliminar, regenerar), pausar la sincronización de
OneDrive manualmente en la máquina activa**, y no asumir que un archivo
recién eliminado permanecerá eliminado si OneDrive sigue sincronizando.

## 17. Advertencia de versionamiento — Excel y Data

`Tabla_Depuracion_Cargos.xlsx` y todas las fuentes en `Data/` (Maestro de
Cargos Kactus, `Consolidado 2025.xlsx`, `Data/Contratos_Kactus/`) **no se
versionan bajo ninguna circunstancia** en esta iniciativa. Contienen datos
operativos y potencialmente sensibles (ver `Docs/SECURITY_AND_PRIVACY.md`).
Solo se versionan las dos excepciones controladas de la sección 11 más esta
Spec.

## 18. Estado Git histórico — separado de esta tarea

El checkout principal sincronizado por OneDrive
(`C:\Users\eclavijo\OneDrive - CHALLENGER S.A.S\5. People analytics\07_Planeación_de_Personal`)
permanece en la rama `docs/roadmap-backlog`, con working tree sucio (~150
archivos PBIP modificados/eliminados sin commitear, Specs sin trackear,
`Tools/`/`Assets/`/`.vscode/` sin trackear) y desincronizado de `origin/main`
(5 commits propios no fusionados, 43 commits de `origin/main` no
incorporados localmente). Esta deuda —registrada como GOV-001 y relacionada
con GOV-006 (`Specs/0021`)— **no se resuelve en este frente**. Este cierre
se ejecuta desde un worktree limpio, aislado, creado directamente desde
`origin/main`, precisamente para no depender de ese checkout histórico ni
mezclarse con su deuda acumulada.

---

## 19. Cómo retomar esta tarea

1. Leer esta Spec completa.
2. Leer
   `Outputs/Depuracion_Cargos/Reglas_Normalizacion_Empresa_Contratos_Kactus.md`
   (versionado — disponible en cualquier checkout de `main` tras el merge de
   este PR).
3. Revisar si julio de 2026 sigue siendo el periodo máximo disponible en
   `Consolidado 2025.xlsx`, o si ya existe un periodo posterior — si existe,
   NO cambiar automáticamente el periodo autorizado del notebook sin
   confirmarlo explícitamente.
4. Actualizar/confirmar que las fuentes Kactus en
   `Data/Maestro_Cargos-Roles_Kactus/Insumos_Vigentes/` siguen siendo 8
   archivos con la misma estructura.
5. Actualizar/confirmar `Data/HeadCount/2025/Consolidado 2025.xlsx`.
6. Seleccionar el kernel `planeacion_personal` ("Python 3.14 - Planeacion
   Personal") en Jupyter/VS Code (ver sección 15-B); si no aparece
   registrado en la máquina actual, registrarlo de nuevo siguiendo esa
   misma sección.
7. Ejecutar el notebook completo de principio a fin.
8. Revisar la hoja `QA_Conciliacion` y contrastarla contra la tabla de la
   sección 10 de esta Spec.
9. Resolver los pendientes funcionales de la sección 12, en particular los
   hallazgos de `Cargos ocupados` negativos/vacíos (pendientes 4 y 6).
10. Solo al finalizar la depuración funcional completa, diligenciar
    `Fecha de actualización` en el notebook (variable `FECHA_ACTUALIZACION`)
    y volver a ejecutar de principio a fin.
