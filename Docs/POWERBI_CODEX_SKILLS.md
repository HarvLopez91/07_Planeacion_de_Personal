# Skills oficiales de Power BI para Codex

## Objetivo

Documentar la instalacion y el uso de las skills oficiales de Microsoft para trabajar con Power BI, PBIP, PBIR y modelos semanticos desde Codex en el repositorio `07_Planeacion_de_Personal`.

## Alcance

Este documento aplica al uso de las skills copiadas desde `plugins/powerbi-authoring` del repositorio `microsoft/skills-for-fabric`. No autoriza por si solo cambios en medidas, relaciones, consultas, fuentes, visuales, paginas ni publicaciones del informe.

## Skills instaladas

| Skill | Funcion principal |
|---|---|
| `check-updates` | Revisar si el paquete oficial tiene actualizaciones disponibles y orientar el proceso de actualizacion. |
| `semantic-model-authoring` | Guiar cambios controlados en modelos semanticos, TMDL, medidas y metadatos de modelo. |
| `powerbi-report-planning` | Convertir requisitos de negocio en un plan de implementacion para reportes o paginas Power BI. |
| `powerbi-report-design` | Definir lineamientos de diseno visual antes de modificar archivos PBIR. |
| `powerbi-report-authoring` | Autorizar y validar cambios en definiciones PBIR usando herramientas de autoring. |
| `powerbi-report-management` | Gestionar elementos de reportes y definiciones PBIR en Microsoft Fabric cuando el flujo lo requiera. |

## Ubicacion

```text
.agents/
|-- LICENSE
|-- UPSTREAM.md
|-- common/
|-- skills/
    |-- check-updates/
    |-- semantic-model-authoring/
    |-- powerbi-report-planning/
    |-- powerbi-report-design/
    |-- powerbi-report-authoring/
    |-- powerbi-report-management/
```

Cada skill debe conservar su archivo `SKILL.md`. Los recursos compartidos viven en `.agents/common`.

## Requisitos

- Codex CLI disponible en la terminal.
- Node.js 20 o superior.
- `powerbi-report-author`.
- `powerbi-desktop`.
- Acceso local al proyecto `PBIP/Proyecto7.pbip`.
- Power BI Desktop cerrado antes de editar archivos PBIP externamente.

## Comandos de validacion

```powershell
node --version
npm --version
powerbi-report-author --version
powerbi-report-author doctor
powerbi-desktop --version
codex --version
git diff --check -- .agents Docs/POWERBI_CODEX_SKILLS.md
```

Tambien se debe validar que cada carpeta instalada contenga `SKILL.md`:

```powershell
Get-ChildItem .agents/skills -Directory | ForEach-Object {
  [pscustomobject]@{
    Skill = $_.Name
    SkillMd = Test-Path (Join-Path $_.FullName 'SKILL.md')
  }
}
```

## Invocacion desde Codex

Las skills se activan al pedir tareas alineadas con su descripcion o al nombrarlas de forma explicita. Ejemplos:

- `Usa semantic-model-authoring para revisar una medida DAX antes de editarla`.
- `Usa powerbi-report-planning para preparar el cambio de la pagina Productividad`.
- `Usa powerbi-report-design para proponer el diseno visual antes de tocar PBIR`.
- `Usa powerbi-report-authoring para aplicar y validar cambios PBIR`.
- `Usa powerbi-report-management para revisar un reporte en Fabric`.
- `Usa check-updates para validar si las skills oficiales tienen una nueva version`.

## Ejemplos aplicados

### Productividad

Usar `powerbi-report-planning` para delimitar el cambio de un grafico, `powerbi-report-design` para revisar consistencia visual y `powerbi-report-authoring` para validar que el PBIR modificado mantenga campos, medidas, filtros e interacciones.

### Gasto Laboral

Usar `semantic-model-authoring` cuando el ajuste implique medidas de gasto, formato numerico o contexto de filtro. Si el cambio es solo visual, usar `powerbi-report-design` antes de editar el PBIR.

### Demografico (Promedio)

Usar `semantic-model-authoring` para cambios de columnas, grupos semanticos o clasificaciones, y `powerbi-report-authoring` para validar visuales, slicers, tablas y navegacion de la pagina.

## Diferencias de responsabilidad

| Frente | Responsabilidad |
|---|---|
| Diseno del informe | Define jerarquia visual, legibilidad, colores, estados y experiencia de lectura. No sustituye validacion visual en Power BI Desktop. |
| Autoria PBIR | Modifica archivos JSON/PBIR del reporte. Debe validar JSON, esquema, campos, filtros e interacciones antes de abrir o publicar. |
| Modelo semantico | Modifica TMDL, medidas DAX, columnas, relaciones o metadatos. Requiere auditoria semantica y autorizacion especifica. |
| Validacion con Power BI Desktop | Confirma apertura, aplicacion de cambios, refresh, renderizado e interacciones. Es obligatoria cuando el alcance pueda afectar experiencia final o carga de datos. |

## Restricciones y controles

- Las skills de diseno no sustituyen la validacion visual en Power BI Desktop.
- Las modificaciones PBIR deben validarse antes de abrir o publicar el informe.
- No modificar medidas, relaciones, fuentes o logica del modelo sin autorizacion.
- Limitar cada cambio al alcance solicitado por el usuario.
- No agregar archivos sensibles, pesados, temporales, caches, `Data/`, `Outputs/` ni artefactos binarios sin autorizacion expresa.
- No mezclar cambios de skills con cambios funcionales PBIP.
- Usar staging selectivo con rutas explicitas y revisar `git diff --cached`.
- Mantener intactos los cambios locales ajenos.

## Procedimiento de actualizacion

1. Clonar temporalmente `https://github.com/microsoft/skills-for-fabric` fuera del repositorio.
2. Registrar el commit SHA nuevo.
3. Comparar `plugins/powerbi-authoring/skills` y `plugins/powerbi-authoring/common`.
4. Actualizar solamente las skills y recursos aprobados.
5. Conservar `.agents/LICENSE`.
6. Actualizar `.agents/UPSTREAM.md`.
7. Ejecutar las validaciones CLI y de Git.
8. Preparar un commit aislado de `.agents/**` y la documentacion autorizada.

## Origen y licencia

- Repositorio oficial: `https://github.com/microsoft/skills-for-fabric`
- Commit incorporado: `d79f3393cab658d0b12d7215b7df1a069a2463a5`
- Paquete: `plugins/powerbi-authoring`
- Licencia: MIT, conservada en `.agents/LICENSE`

## Validacion manual pendiente

Despues de publicar el cambio, se recomienda reiniciar Codex y comprobar que las skills aparezcan al consultar `/skills` o el mecanismo equivalente de la sesion.
