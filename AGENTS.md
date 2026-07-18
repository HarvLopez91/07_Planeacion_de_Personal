# AGENTS.md

Instrucciones duraderas para Codex, Claude Code y otros agentes que trabajen en `07_Planeación_de_Personal`.

## Proyecto

Dashboard Power BI/PBIP de People Analytics para Planeación de Personal del Grupo Empresarial Lemco.

- PBIP principal: `PBIP/Proyecto7.pbip`.
- Rama principal: `main`.
- Remoto esperado: `https://github.com/HarvLopez91/07_Planeacion_de_Personal.git`.
- Documentación oficial: `Docs/README.md`.

## Fuentes de Verdad

Consultar en este orden:

1. Estado real del repositorio y `git status`.
2. Instrucciones explícitas del usuario.
3. `Docs/`.
4. `Specs/`.
5. `Outputs/` recientes.
6. Definiciones PBIP/TMDL en modo solo lectura.

`Outputs/` es evidencia temporal, no documentación oficial. `Docs/` es la fuente estable.

## Reglas Git Obligatorias

- Ejecutar `git status -sb` antes de modificar.
- Nunca usar `git add .`.
- Nunca mezclar cambios PBIP, documentación, Specs, Tools o Assets en un mismo commit salvo aprobación explícita.
- Hacer staging solo con rutas explícitas.
- Validar identidad antes de commit:
  `EdwinClavijoChallenger <edwin.clavijo@challenger.co>`.
- No hacer push sin autorización explícita del prompt vigente.
- No usar `reset`, `restore`, `checkout`, `clean`, `stash`, `rebase`, `cherry-pick`, `commit --amend` ni `push --force` sin autorización específica.

Validaciones mínimas:

```powershell
git status -sb
git diff --cached --name-status
git diff --check
git log --oneline origin/main..HEAD
git log --oneline HEAD..origin/main
```

## Reglas PBIP

- No editar Power BI Desktop y TMDL manualmente al mismo tiempo.
- Auditar siempre el ruido generado por Power BI Desktop.
- Separar commits de modelo, reporte, visuales, documentación y herramientas.
- No modificar `PBI_ResultType` para ocultar errores.
- No tocar `diagramLayout.json`, `pages.json`, bookmarks, cultures o visuales no relacionados sin justificación.
- Validar JSON/TMDL después de cualquier edición manual.

## Carpetas

| Carpeta | Regla |
|---|---|
| `PBIP/` | Proyecto Power BI; modificar solo con alcance aprobado |
| `Docs/` | Documentación oficial versionada |
| `Specs/` | Análisis y planes aprobables |
| `Outputs/` | Evidencia temporal; no versionar |
| `Data/` | Datos locales; no versionar |
| `Reports/` | Informes recurrentes, si están aprobados |
| `Tools/` | Utilidades; no mezclar con PBIP |
| `Assets/` | Recursos; revisar alcance antes de versionar |

## Datos y Privacidad

El proyecto puede contener datos personales y sensibles de talento humano. No imprimir, copiar ni documentar registros individuales, nombres, identificaciones, salarios, diagnósticos médicos ni credenciales.

## Estado Operativo Actual

Al `2026-07-17`, la migración de fuentes a SharePoint corporativo está en validación parcial. Persisten riesgos de **Formula Firewall** en consultas raíz como `PLANTA DE PERSONAL`, `Selección Grupo Lemco` y `SENA UNIDADES`. No afirmar que el refresh es exitoso sin evidencia interactiva.

Ver:

- `Docs/PROJECT_STATUS.md`
- `Docs/DATA_PIPELINE.md`
- `Docs/TROUBLESHOOTING.md`

## Criterio de Entrega

Toda entrega debe reportar:

- objetivo atendido;
- archivos modificados;
- archivos excluidos;
- riesgos;
- validaciones ejecutadas;
- estado de staging/commit/push;
- siguiente paso recomendado.
