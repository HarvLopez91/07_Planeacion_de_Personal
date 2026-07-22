---
name: powerbi-signals
description: Generate a small daily signals package from the local PBIP project. Use only when the user explicitly asks for Power BI signals, recurring findings, or a structured findings log. Do not use for general diagnostics, one-off audits, or commit preparation.
---

# powerbi-signals

## Proposito

Generar un paquete pequeno de senales diarias a partir del proyecto PBIP local, con maximo 5 hallazgos accionables y evidencia verificable.

## Usar cuando

- El usuario pida senales diarias o hallazgos estructurados recurrentes.
- El usuario necesite un log breve y reutilizable de hallazgos del proyecto.

## No usar cuando

- La tarea sea una auditoria puntual de modelo, DAX o navegacion.
- El usuario solo quiera un diagnostico conversacional.
- La tarea principal sea preparar commits.

## Flujo

1. Ejecutar `git status --short`.
2. Reunir evidencia local minima con las tools necesarias para el alcance:
   - `python Tools/pbip/list_pbip_structure.py . --pretty`
   - `python Tools/pbip/audit_navigation.py . --pretty`
   - `python Tools/pbip/audit_semantic_model.py . --pretty`
   - `python Tools/pbip/audit_dax_measures.py . --pretty` solo si hay hallazgos de medidas.
3. Seleccionar maximo 5 hallazgos accionables con evidencia concreta.
4. Guardar el JSON en `Outputs/signals/YYYY-MM-DD_powerbi-signals.json`.
5. Guardar el log breve en `Outputs/signals/YYYY-MM-DD_powerbi-signals.md`.
6. Si el archivo diario ya existe, no sobrescribir sin confirmar alcance.
7. Validar que el JSON parsea y que cada senal tiene `id`, `area`, `source`, `evidence`, `impact`, `action` y `related_files`.

## Restricciones

- No crear carpetas funcionales nuevas fuera de `Outputs/`.
- No modificar archivos del PBIP.
- No hacer commit ni push.
- No inventar evidencia ni duplicar hallazgos equivalentes.

## Resultado esperado

- Rutas generadas.
- Cantidad de senales.
- Hallazgos descartados por falta de evidencia.
- Validaciones ejecutadas.
- Estado Git final de los archivos creados.
