# Retiros y Rotacion Manufactura

## Proposito

Este directorio documenta la ubicacion operativa local del informe recurrente `Retiros_y_Rotacion_Manufactura.xlsx`.

El informe consolida informacion derivada del reporte Power BI del proyecto `07_Planeacion_de_Personal` para seguimiento operativo de retiros y rotacion asociados a Manufactura.

## Fuente de informacion

La fuente funcional del informe es Power BI:

- Proyecto: `07_Planeacion_de_Personal`.
- Archivo PBIP: `PBIP/Proyecto7.pbip`.
- Origen del resultado: visuales, tablas o exportaciones controladas desde el reporte Power BI.

Este archivo no debe tratarse como fuente primaria del modelo semantico. Es un resultado derivado del reporte.

## Periodicidad de actualizacion

El informe debe actualizarse durante los primeros 10 dias habiles de cada mes.

La version vigente se conserva en:

```text
Current/Retiros_y_Rotacion_Manufactura.xlsx
```

## Responsable

Responsable funcional: pendiente de confirmar.

Propietario de la copia oficial: pendiente de confirmar en SharePoint privado.

## Procedimiento de actualizacion

1. Abrir el reporte Power BI autorizado.
2. Aplicar los filtros, periodo y criterios definidos para el corte mensual.
3. Exportar o actualizar el informe operativo.
4. Validar que el archivo no incluya datos personales innecesarios para el uso operativo.
5. Guardar la version vigente como:

   ```text
   Current/Retiros_y_Rotacion_Manufactura.xlsx
   ```

6. Si se requiere conservar historico mensual, copiar la version del mes a:

   ```text
   History/YYYY/YYYY-MM_Retiros_y_Rotacion_Manufactura.xlsx
   ```

7. Confirmar que los archivos `.xlsx` no queden versionados en Git.

## Ubicacion de la copia oficial

La copia oficial debe permanecer en un SharePoint privado con propietario definido y permisos controlados.

El repositorio mantiene la estructura, documentacion y reglas de exclusion, pero no debe ser el repositorio oficial de archivos Excel con informacion sensible o potencialmente sensible de Talento Humano.

## Reglas para conservar historicos

- Conservar historicos solo cuando exista una necesidad operativa, de auditoria o trazabilidad.
- Usar carpetas por anio bajo `History/YYYY/`.
- Usar nombres de archivo con formato `YYYY-MM_Retiros_y_Rotacion_Manufactura.xlsx`.
- No versionar archivos `.xlsx` en Git.
- Revisar periodicamente si los historicos siguen siendo necesarios.

## Privacidad y seguridad

Aunque la revision local no evidencio encabezados directos de identificacion personal en el archivo actual, el informe pertenece al dominio de Talento Humano y puede contener informacion sensible o potencialmente sensible.

Por esta razon:

- los archivos Excel se excluyen del versionamiento;
- la copia oficial debe estar en SharePoint privado;
- el acceso debe limitarse a personas autorizadas;
- no se deben publicar datos personales en `README.md`, issues, commits ni evidencias.
