# Instrucciones para GitHub Copilot

Este archivo define reglas operativas mínimas para Copilot dentro de este repositorio. Las políticas detalladas se mantienen en las fuentes canónicas.

## Bloque operativo mínimo

1. Trabajar únicamente dentro del alcance aprobado por el usuario.
2. No crear ni conservar intencionalmente artefactos del proyecto fuera de la raíz, salvo autorización; se permiten temporales automáticos no permanentes.
3. No eliminar, descartar, sobrescribir ni revertir cambios existentes del usuario.
4. No usar `git add .` ni `git add -A`.
5. No ejecutar commit ni push sin autorización explícita.
6. Clasificar los archivos según su propósito en `Specs/`, `Outputs/` o `Docs/`.
7. Consultar la fuente canónica correspondiente cuando la tarea involucre estructura, Git o privacidad.

## Fuentes canónicas

- Ubicación o creación de archivos: [Docs/ESTRUCTURA_PROYECTO.md](../Docs/ESTRUCTURA_PROYECTO.md)
- Staging, commit, push o exclusiones: [Docs/GIT_GOVERNANCE.md](../Docs/GIT_GOVERNANCE.md)
- Datos personales, confidenciales o fuentes sensibles: [Docs/SECURITY_AND_PRIVACY.md](../Docs/SECURITY_AND_PRIVACY.md)

## Alcance de este archivo

Este documento no reemplaza la documentación oficial ni duplica toda la política. Su función es asegurar un comportamiento mínimo consistente para Copilot.