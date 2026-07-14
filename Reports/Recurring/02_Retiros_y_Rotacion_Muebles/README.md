# Retiros y Rotacion Muebles

## Proposito

Este directorio documenta la ubicacion operativa local del informe recurrente `Retiros_y_Rotacion_Muebles.xlsx`.

El informe corresponde a un resultado operativo derivado de Power BI para seguimiento de retiros y rotacion asociados a Muebles.

## Fuente de informacion

Fuente funcional verificada: informe derivado de Power BI dentro del proyecto `07_Planeacion_de_Personal`.

Detalle pendiente de confirmar:

- pagina, visual o tabla especifica usada para generar el archivo;
- filtros exactos requeridos para el corte mensual;
- si el archivo se genera por exportacion manual o por actualizacion de una plantilla existente.

## Periodicidad de actualizacion

Periodicidad operativa: mensual.

Ventana de actualizacion definida para esta familia de informes: primeros 10 dias habiles de cada mes.

La version vigente se conserva en:

```text
Current/Retiros_y_Rotacion_Muebles.xlsx
```

## Responsable

Responsable funcional: pendiente de confirmar.

Propietario de la copia oficial: pendiente de confirmar en SharePoint privado.

## Procedimiento de actualizacion

Procedimiento minimo recomendado hasta confirmar el flujo operativo exacto:

1. Abrir el reporte Power BI autorizado.
2. Aplicar el periodo y filtros definidos para el corte mensual.
3. Generar o actualizar el informe operativo.
4. Validar que el archivo no incluya datos personales innecesarios para el uso operativo.
5. Guardar la version vigente como:

   ```text
   Current/Retiros_y_Rotacion_Muebles.xlsx
   ```

6. Si se requiere conservar historico mensual, copiar la version del mes a:

   ```text
   History/YYYY/YYYY-MM_Retiros_y_Rotacion_Muebles.xlsx
   ```

7. Confirmar que los archivos `.xlsx` no queden versionados en Git.

## Ubicacion de la copia oficial

La copia oficial debe permanecer en un SharePoint privado con propietario definido y permisos controlados.

La ubicacion exacta del SharePoint oficial queda pendiente de confirmar.

## Tratamiento de historicos

- Conservar historicos solo cuando exista una necesidad operativa, de auditoria o trazabilidad.
- Usar carpetas por anio bajo `History/YYYY/`.
- Usar nombres de archivo con formato `YYYY-MM_Retiros_y_Rotacion_Muebles.xlsx`.
- No versionar archivos `.xlsx` en Git.
- Revisar periodicamente si los historicos siguen siendo necesarios.

## Clasificacion de privacidad

El informe pertenece al dominio de Talento Humano y puede contener informacion sensible o potencialmente sensible.

Por esta razon:

- los archivos Excel se excluyen del versionamiento;
- la copia oficial debe estar en SharePoint privado;
- el acceso debe limitarse a personas autorizadas;
- no se deben publicar datos personales en `README.md`, issues, commits ni evidencias.
