# Estado del Proyecto

Fecha de referencia: `2026-07-17`.

## Resumen Ejecutivo

`07_Planeación_de_Personal` es un dashboard Power BI/PBIP activo para analítica de gestión humana del Grupo Empresarial Lemco. El repositorio ya cuenta con Git, Specs, Outputs, documentación oficial y prácticas de staging selectivo.

El frente documental queda actualizado para reflejar que el proyecto está en operación y evolución, pero con un bloqueo técnico vigente: la validación final de refresh depende de resolver o confirmar los errores de **Formula Firewall** en Power BI Desktop.

## Estado Git

- Rama principal: `main`.
- Remoto esperado: `origin/main`.
- Identidad esperada para commits: `EdwinClavijoChallenger <edwin.clavijo@challenger.co>`.
- Staging requerido: selectivo y por rutas explícitas.
- `git add .` está prohibido.
- El working tree puede mantener cambios PBIP acumulados fuera de alcance; no deben mezclarse con documentación ni con commits técnicos.

## Estado PBIP

- PBIP principal: `PBIP/Proyecto7.pbip`.
- Formato: Power BI Desktop Project.
- Modelo semántico: TMDL en `PBIP/Proyecto.SemanticModel/definition/`.
- Reporte: JSON/PBIR en `PBIP/Proyecto.Report/definition/`.

## Estado de Fuentes

La estrategia vigente busca mover fuentes desde rutas personales de SharePoint/OneDrive hacia SharePoint corporativo.

Estado documentado:

- `PptovsReal.xlsx` ya está en ruta corporativa para `Planta Ppto`, `Ppto Retiros` y `Ppto Ingresos`.
- Selección y SENA fueron revisadas para apuntar a rutas corporativas aprobadas.
- `SENA UNIDADES` debe conservar navegación `Item="SENA", Kind="Sheet"`.
- Persisten rutas personales o pendientes de análisis en fuentes como `AUSENTISMOS` y `Estructura`.
- `AREAS` sigue construyéndose desde `Consolidado 2024.xlsx`; se documenta como requerimiento de análisis posterior.
- `REQUISICIONES HABITEL 2026.xlsx` es una fuente nueva pendiente de análisis de impacto; no está incorporada.

## Bloqueo Técnico Vigente

No hay evidencia documental suficiente para declarar exitosos `Aplicar cambios` y refresh local completo.

Consultas raíz que requieren validación:

- `PLANTA DE PERSONAL`.
- `Selección Grupo Lemco`.
- `SENA UNIDADES`.

Síntoma observado: múltiples consultas bloqueadas por niveles de privacidad incompatibles en Power Query.

La validación definitiva requiere Power BI Desktop de julio de 2026 o posterior, configuración de privacidad consistente como `Organizacional` y evidencia interactiva de refresh.

## Pendientes Funcionales y Técnicos

| Pendiente | Tipo | Estado |
|---|---|---|
| Validar Formula Firewall con Power BI Desktop actualizado | Técnico | Pendiente |
| Confirmar refresh local completo sin errores | Técnico | Pendiente |
| Auditar cambios PBIP acumulados por bloque | Git / PBIP | Pendiente |
| Analizar cambio de origen de `AREAS` hacia consolidado más actual | Modelo | Pendiente |
| Analizar incorporación de `REQUISICIONES HABITEL 2026.xlsx` | Fuente | Pendiente |
| Migrar rutas personales restantes de `AUSENTISMOS` y `Estructura` | Fuente | Pendiente |
| Definir publicación y refresh programado en Power BI Service | Operación | Pendiente |

## Criterio para Avanzar a Validación Funcional

Se puede avanzar a validación funcional de páginas solo cuando:

1. Power BI Desktop abra `PBIP/Proyecto7.pbip` sin errores.
2. `Aplicar cambios` termine sin consultas bloqueadas.
3. El refresh local completo termine sin errores de credenciales, privacidad, hoja, clave, columna o tipo.
4. Los cambios PBIP generados por Desktop estén auditados y clasificados.
5. No haya staging accidental.
