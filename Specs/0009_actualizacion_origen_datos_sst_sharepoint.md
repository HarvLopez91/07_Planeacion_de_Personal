# Actualizacion de origen de datos SST a SharePoint corporativo

## 1. Objetivo

Documentar y validar la actualizacion del origen de datos de las consultas SST desde una ruta personal de SharePoint/OneDrive hacia el archivo corporativo `Accidentalidad_Consolidado.xlsx` en el sitio `TalentoHumanoGrupoLemco`.

## 2. Fecha del cambio

Fecha de documentacion: 2026-07-22.
Proyecto: `07_Planeacion_de_Personal`.
PBIP: `PBIP/Proyecto7.pbip`.

## 3. Consultas afectadas

| Consulta | Archivo TMDL | Conector | Hoja / elemento |
|---|---|---|---|
| `SST_CHA` | `PBIP/Proyecto.SemanticModel/definition/tables/SST_CHA.tmdl` | `Excel.Workbook(Web.Contents(...), null, true)` | `Item="SST_CH", Kind="Sheet"` |
| `SST-HABITELH` | `PBIP/Proyecto.SemanticModel/definition/tables/SST-HABITELH.tmdl` | `Excel.Workbook(Web.Contents(...), null, true)` | `Item="SST-HABITEL", Kind="Sheet"` |
| `SST-GSKY` | `PBIP/Proyecto.SemanticModel/definition/tables/SST-GSKY.tmdl` | `Excel.Workbook(Web.Contents(...), null, true)` | `Item="SST-SKY", Kind="Sheet"` |
| `SST GENERAL` | `PBIP/Proyecto.SemanticModel/definition/tables/SST GENERAL.tmdl` | `Excel.Workbook(Web.Contents(...), null, true)` | `Item="SST GENERAL", Kind="Sheet"` |

## 4. Origen anterior

```text
https://lemcosas-my.sharepoint.com/personal/edwin_clavijo_challenger_co/Documents/Documentos/Gerencia%20G.%20Humana/6.%20Informaci%C3%B3n/Power%20BI/SST/Accidentalidad.xlsx
```

Tipo de riesgo: dependencia de ruta personal de SharePoint/OneDrive.

## 5. Nuevo sitio, carpeta y archivo

Sitio:

```text
https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco
```

Biblioteca y carpeta:

```text
Documentos compartidos/5. People analytics/09_SST_GA/Data/
```

Archivo:

```text
Accidentalidad_Consolidado.xlsx
```

URL directa usada por las consultas:

```text
https://lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco/Documentos%20compartidos/5.%20People%20analytics/09_SST_GA/Data/Accidentalidad_Consolidado.xlsx
```

## 6. Justificacion del cambio

El cambio reduce la dependencia de una ubicacion personal y alinea la fuente SST con una ubicacion corporativa de SharePoint, mas adecuada para continuidad operativa, gobierno documental, permisos organizacionales y refresh administrado.

## 7. Archivos PBIP/TMDL modificados

Archivos con cambio de origen validado:

- `PBIP/Proyecto.SemanticModel/definition/tables/SST_CHA.tmdl`
- `PBIP/Proyecto.SemanticModel/definition/tables/SST-HABITELH.tmdl`
- `PBIP/Proyecto.SemanticModel/definition/tables/SST-GSKY.tmdl`
- `PBIP/Proyecto.SemanticModel/definition/tables/SST GENERAL.tmdl`

Observacion de control de cambios: `SST GENERAL.tmdl` contiene cambios adicionales preexistentes sobre medidas. Para el commit de esta actualizacion solo debe incluirse el hunk de cambio de URL; las eliminaciones de medidas quedan fuera de alcance.

## 8. Validaciones ejecutadas

- Busqueda focalizada de `Accidentalidad.xlsx`, `Accidentalidad_Consolidado.xlsx`, `Web.Contents`, `SharePoint.Files` y `SharePoint.Contents` en las cuatro consultas SST.
- Revision de diff de cada archivo TMDL afectado.
- Confirmacion de que las cuatro consultas conservan el patron `Excel.Workbook(Web.Contents(...), null, true)`.
- Confirmacion de que las hojas consumidas siguen siendo `SST_CH`, `SST-HABITEL`, `SST-SKY` y `SST GENERAL`.
- Confirmacion de que los pasos de promocion de encabezados y cambio de tipos permanecen sin cambios en los hunks de ruta.

## 9. Confirmacion de esquema

La revision de los hunks de origen confirma que no se cambiaron nombres de hojas, columnas, tipos de datos ni transformaciones funcionales como parte del cambio de ruta. El esquema esperado permanece:

- Campos de grupo y empresa.
- Campos de periodo.
- Campos de accidentalidad, dias perdidos, cargo, area, ubicacion y clasificaciones SST.
- Tipos enteros, texto y numericos ya definidos en `Table.TransformColumnTypes`.

## 10. Riesgos y dependencias

| Riesgo | Mitigacion |
|---|---|
| Permisos insuficientes sobre el sitio corporativo | Validar acceso con cuenta organizacional en Power BI Desktop y Power BI Service. |
| Credenciales anteriores asociadas al dominio personal | Revisar configuracion de origen de datos y privacidad en Desktop/Service. |
| Formula Firewall por mezcla de origenes SharePoint | Mantener niveles de privacidad consistentes como Organizacional. |
| Cambios no relacionados acumulados en el working tree | Usar staging selectivo por rutas y, en `SST GENERAL.tmdl`, por hunk. |
| Cambios de estructura no visibles sin refresh | Validar vista previa o refresh de las cuatro consultas en Power BI Desktop. |

## 11. Resultado final

Las cuatro consultas SST evaluadas apuntan al archivo corporativo `Accidentalidad_Consolidado.xlsx` usando `Web.Contents` dentro de `Excel.Workbook`. La ruta personal anterior no permanece como origen activo en estas cuatro consultas.

## 12. Plan de reversion

Si la validacion en Power BI Desktop o Power BI Service falla por permisos, archivo no encontrado o estructura incompatible:

1. Revertir el commit especifico de esta actualizacion.
2. Restaurar temporalmente la URL anterior solo si se requiere continuidad operativa inmediata.
3. Validar nuevamente credenciales, privacidad y permisos del sitio corporativo.
4. No mezclar el rollback con cambios visuales, DAX, relaciones o transformaciones SST.
