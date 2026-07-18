# Troubleshooting Power BI / PBIP

Fecha de referencia: `2026-07-17`.

## Formula Firewall en Power Query

### Síntomas

Power BI Desktop puede mostrar mensajes como:

- `La consulta está obteniendo acceso a orígenes de datos con niveles de privacidad que no se pueden utilizar juntos`.
- `Vuelva a generar esta combinación de datos`.
- Varias consultas bloqueadas aunque solo tres consultas raíz muestren error visible.

Consultas raíz documentadas:

- `PLANTA DE PERSONAL`.
- `Selección Grupo Lemco`.
- `SENA UNIDADES`.

### Causas Probables

- Mezcla de rutas personales y corporativas de SharePoint.
- Entradas duplicadas del mismo sitio con distintos niveles de privacidad.
- Consultas que combinan otras consultas y además acceden directamente a un origen externo.
- Credenciales antiguas guardadas para rutas personales.
- Diferencias entre niveles `Privado`, `Organizacional` y `Público`.

### Validaciones en TMDL

Antes de abrir Power BI Desktop, validar en modo solo lectura:

- `Ppto Retiros`, `Ppto Ingresos` y `Planta Ppto` usan la ruta corporativa de `PptovsReal.xlsx`.
- `SENA UNIDADES` mantiene `Item="SENA", Kind="Sheet"`.
- `SENA_CYL`, `Selección Challenger`, `Selección Habitel Hotels` y `Selección Grupo Sky` usan rutas corporativas aprobadas.
- No se reintroduce `Item="SENA 2025"`.
- No se modificó manualmente `PBI_ResultType`.

### Validación Manual en Power BI Desktop

1. Actualizar Power BI Desktop a julio de 2026 o posterior.
2. Reiniciar Power BI Desktop.
3. Abrir `PBIP/Proyecto7.pbip`.
4. Ir a `Archivo > Opciones y configuración > Configuración de origen de datos`.
5. Revisar orígenes del archivo actual y permisos globales.
6. Localizar entradas asociadas con:
   - `lemcosas-my.sharepoint.com`.
   - `lemcosas.sharepoint.com`.
   - `https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco`.
7. Configurar fuentes corporativas como `Organizacional`.
8. Usar cuenta organizacional.
9. No usar `Ignorar niveles de privacidad` como solución permanente.
10. No borrar permisos personales sin autorización.
11. Verificar si existe la característica preliminar:
    `Permitir que las particiones del firewall de privacidad que hacen referencia a otras particiones también accedan a orígenes de datos`.
12. Documentar la versión exacta de Power BI Desktop.

### Validación de Carga

En Power Query Editor:

1. Validar vista previa de `PLANTA DE PERSONAL`.
2. Validar vista previa de `Selección Grupo Lemco`.
3. Validar vista previa de `SENA UNIDADES`.
4. Validar consultas base relacionadas.
5. Ejecutar `Aplicar cambios`.
6. Si `Aplicar cambios` termina correctamente, ejecutar refresh completo.

No declarar la validación como exitosa sin evidencia visual o confirmación explícita.

## Error de Clave no Encontrada

Mensaje típico:

```text
La clave no coincidió con ninguna fila de la tabla.
```

Causa frecuente: Power Query navega un Excel con un `Item` o `Kind` que ya no existe.

Ejemplo validado:

```powerquery
Origen{[Item="SENA", Kind="Sheet"]}[Data]
```

No inventar nombres de hoja. Revisar la tabla de navegación en Power Query Editor y documentar `Name`, `Item` y `Kind`.

## Ruido de Power BI Desktop

Después de abrir o guardar el PBIP, revisar si Power BI modificó:

- `pages.json`.
- `page.json`.
- `bookmarks/**`.
- `diagramLayout.json`.
- `cultures/es-ES.tmdl`.
- visuales fuera de alcance.
- `.pbi/unappliedChanges.json`.
- `DAXQueries/**`.

Clasificar estos cambios antes de staging.

## Comandos de Auditoría

```powershell
git status -sb
git status --short
git diff --check
git diff --cached --name-status
git diff --stat -- PBIP/
```
