# Origen de las skills oficiales de Power BI

## Repositorio oficial

- Repositorio: `https://github.com/microsoft/skills-for-fabric`
- Commit de origen: `d79f3393cab658d0b12d7215b7df1a069a2463a5`
- Fecha de incorporacion: `2026-07-29`
- Paquete copiado: `plugins/powerbi-authoring`
- Licencia: MIT, conservada en `.agents/LICENSE`

## Skills incluidas

- `check-updates`
- `semantic-model-authoring`
- `powerbi-report-planning`
- `powerbi-report-design`
- `powerbi-report-authoring`
- `powerbi-report-management`

## Recursos compartidos

Los recursos comunes del paquete se copiaron desde:

```text
plugins/powerbi-authoring/common
```

hacia:

```text
.agents/common
```

## Adaptaciones locales

El contenido funcional de las skills y referencias se conserva igual al paquete oficial. Como adaptacion de compatibilidad con las validaciones Git del repositorio, se normalizaron espacios finales, lineas en blanco sobrantes al final de archivo y codificacion UTF-8 sin BOM en los archivos copiados.

## Metodo de actualizacion

1. Clonar temporalmente `https://github.com/microsoft/skills-for-fabric`.
2. Registrar el nuevo commit SHA de origen.
3. Comparar `plugins/powerbi-authoring/skills` y `plugins/powerbi-authoring/common`.
4. Actualizar exclusivamente las skills oficiales y recursos compartidos aprobados.
5. Mantener la licencia MIT y actualizar este archivo con el nuevo SHA.
6. Validar `SKILL.md` en cada carpeta, las herramientas CLI y el diff Git antes del commit.

No se deben mezclar actualizaciones de skills con cambios PBIP, datos, Specs, Outputs ni ajustes funcionales del informe.
