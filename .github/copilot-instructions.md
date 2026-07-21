# Instrucciones para GitHub Copilot

Este archivo define reglas operativas para Copilot dentro de este repositorio. Para lineamientos completos del proyecto, usar las referencias oficiales en lugar de duplicar contenido.

## Principios de trabajo

- Analizar antes de modificar.
- Realizar cambios mínimos y trazables.
- Respetar estrictamente el alcance solicitado por el usuario.
- No modificar archivos no relacionados con la tarea.
- Explicar impacto y riesgos antes de cambios estructurales.

## Fuentes de referencia obligatorias

Copilot debe consultar y seguir estos documentos según el tipo de tarea:

- Gobierno general del repositorio: [AGENTS.md](../AGENTS.md)
- Índice y ubicación de documentación oficial: [Docs/README.md](../Docs/README.md)
- Reglas de staging, commit y push: [Docs/GIT_GOVERNANCE.md](../Docs/GIT_GOVERNANCE.md)
- Estado operativo vigente y riesgos funcionales: [Docs/PROJECT_STATUS.md](../Docs/PROJECT_STATUS.md)

## Alcance de este archivo

Este archivo contiene únicamente reglas generales del repositorio.

Las reglas específicas por dominio o tecnología deben evolucionar a archivos dedicados en `.github/instructions/`, por ejemplo:

- pbip.instructions.md
- docs.instructions.md
- python.instructions.md

Mientras esos archivos se formalizan, usar como fuente de detalle [AGENTS.md](../AGENTS.md), [Docs/GIT_GOVERNANCE.md](../Docs/GIT_GOVERNANCE.md) y [Docs/PROJECT_STATUS.md](../Docs/PROJECT_STATUS.md).

## Respuesta esperada de Copilot

En tareas de implementación o revisión, la respuesta debe incluir en este orden:

1. Diagnóstico inicial.
2. Archivos a modificar.
3. Archivos excluidos.
4. Riesgos y validaciones propuestas.
5. Confirmación para continuar con acciones sensibles.

Regla de control:

- Esperar aprobación explícita del usuario antes de commit o push.

## Reglas Git críticas (resumen operativo)

Estas reglas se aplican siempre y se complementan con [Docs/GIT_GOVERNANCE.md](../Docs/GIT_GOVERNANCE.md):

- Prohibido usar `git add .`
- Prohibido usar `git add -A`
- No realizar commit sin aprobación explícita.
- No realizar push sin aprobación explícita.
- Evitar mezclar cambios de PBIP, Docs, Specs, Tools o Assets en un mismo commit salvo autorización explícita.

## Restricciones Power BI y PBIP/TMDL

Para reglas específicas de PBIP/TMDL, usar referencias oficiales y preparar su separación en archivos dedicados dentro de `.github/instructions/`.

Reglas generales que se mantienen en este archivo:

- Aplicar cambios mínimos y estrictamente en alcance.
- No ocultar errores funcionales ni técnicos.
- Mantener trazabilidad de cada ajuste.
- Evitar intervención manual simultánea que comprometa consistencia.

Referencias de detalle:

- Estándares PBIP y restricciones operativas: [AGENTS.md](../AGENTS.md)
- Estado técnico y riesgos de refresh/Formula Firewall: [Docs/PROJECT_STATUS.md](../Docs/PROJECT_STATUS.md)

## Testing

Antes de considerar terminada una tarea PBIP/TMDL, validar como mínimo:

1. Apertura correcta del PBIP en Power BI Desktop.
2. Aplicar cambios sin errores bloqueantes.
3. Refresh local conforme al contexto operativo vigente.
4. Revisión de riesgos activos documentados en [Docs/PROJECT_STATUS.md](../Docs/PROJECT_STATUS.md).
5. Verificación de staging selectivo según [Docs/GIT_GOVERNANCE.md](../Docs/GIT_GOVERNANCE.md).

## Control de commit y push

- Si no existe evidencia de validación mínima, Copilot debe advertir el riesgo y detener commit/push.
- No realizar commit sin aprobación explícita del usuario.
- No realizar push sin aprobación explícita del usuario.
