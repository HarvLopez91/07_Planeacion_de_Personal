# Runbook Operativo

> Procedimientos para abrir, actualizar, mantener y publicar el modelo Power BI.
> Para el contexto de datos ver [DATA_PIPELINE.md](DATA_PIPELINE.md).

---

## Prerequisitos

- **Power BI Desktop** instalado (version compatible con formato PBIP y TMDL)
- Acceso a las cuentas de SharePoint de las fuentes de datos (ver [DATA_PIPELINE.md — Cuentas](DATA_PIPELINE.md#cuentas-de-sharepoint-identificadas))
- Conexion a internet para acceder a los archivos en SharePoint/OneDrive

---

## 1. Abrir el proyecto

1. Abrir **Power BI Desktop**
2. Seleccionar **Archivo → Abrir → Examinar**
3. Navegar a: `07_Planeacion_de_Personal/PBIP/Proyecto7.pbip`
4. Hacer clic en **Abrir**

> **Alternativa:** Hacer doble clic sobre `Proyecto7.pbip` en el explorador de archivos si Power BI Desktop esta configurado como programa predeterminado.
> Nota: el archivo se llamo `Proyecto.pbip` hasta el 2026-06-17, cuando se reemplazo por `Proyecto7.pbip` (commit `cfb3a15`).

Al abrir, Power BI Desktop cargara tanto el modelo semantico como el reporte. Si solicita credenciales, ingresar las de las cuentas A y B de SharePoint.

---

## 2. Actualizar el modelo (refresh manual)

1. Con el proyecto abierto, ir a la pestaña **Inicio**
2. Hacer clic en **Actualizar** (o `Ctrl+Alt+F5` para actualizar todo)
3. Esperar a que todas las tablas se actualicen
4. Verificar que no haya errores en el panel de **Actualizacion de datos**

### Tablas que requieren credenciales activas

Las siguientes tablas fallaran si las credenciales de SharePoint no estan vigentes:

**Cuenta A:** `PLANTA DE PERSONAL`, `Consolidado2025`, `Planta Ppto`, `Ppto Retiros`, `Ppto Ingresos`, `SST GENERAL`, `SST_CHA`, `SST-HABITELH`, `SST-GSKY`

**Cuenta B:** `AUSENTISMOS`, `Maestro`, `Incapacidades`, `Seleccion Challenger`, `Seleccion Habitel Hotels`, `Seleccion Grupo Sky`, `Seleccion Grupo Lemco`, `Estructura`

### Actualizar credenciales en Power BI Desktop

Si las credenciales expiran:
1. Ir a **Archivo → Opciones y configuracion → Configuracion de origen de datos**
2. Seleccionar la fuente con error
3. Hacer clic en **Editar permisos** o **Borrar permisos**
4. Re-autenticar con la cuenta correcta

---

## 3. Agregar datos del nuevo ano

Cuando se inicia un nuevo ano de datos (ej: 2026):

### Paso 1: Preparar el archivo Excel fuente
- Crear (o recibir) el archivo `Consolidado 2026.xlsx` con la hoja `Consolidado2026` siguiendo el mismo esquema de columnas que `Consolidado 2025.xlsx`
- Subirlo a la misma ruta de SharePoint en la cuenta A

### Paso 2: Crear una nueva tabla de staging en Power Query
- En `Proyecto.SemanticModel/definition/tables/`, crear un nuevo archivo `Consolidado2026.tmdl` con la estructura equivalente a `Consolidado2025.tmdl`
- Actualizar la URL de SharePoint y el nombre de la hoja en el codigo M

### Paso 3: Actualizar la consulta de PLANTA DE PERSONAL
- En `PLANTA DE PERSONAL.tmdl`, actualizar el paso `Table.Combine` para incluir `Consolidado2026`:
  ```
  Table.Combine({#"Tipo cambiado1", Consolidado2025, Consolidado2026})
  ```

### Paso 4: Verificar y actualizar dimensiones de periodo
- Verificar que la tabla `Anos` incluya el ano 2026
- La tabla `DimPeriodoYM` se actualiza automaticamente al ser un `CROSSJOIN`

> **Advertencia:** Actualmente la medida `Prom_Colaboradores` tiene los meses de Enero a Julio hardcodeados. Si se agrega un nuevo ano, esta medida debe revisarse.

---

## 4. Agregar una nueva empresa al grupo

1. Actualizar los datos embebidos en la tabla `Empresas` en Power Query (requiere regenerar el binario comprimido o cambiar el patron de carga a una tabla externa)
2. Agregar la empresa al catalogo de `Grupo Empresarial` si aplica un nuevo grupo
3. Verificar que las tablas de hechos incluyan datos de la nueva empresa
4. Si la empresa tiene procesos de seleccion propios, crear una nueva tabla `Seleccion [NuevaEmpresa]` siguiendo el patron de las existentes

---

## 5. Actualizar el nombre de la hoja en REQUISICIONES_CYL.xlsx

Cada ano, la hoja activa de `REQUISICIONES_CYL.xlsx` cambia de nombre (ej: `"Matriz 2025"` → `"Matriz 2026"`). Para actualizar:

1. Abrir `PBIP/Proyecto.SemanticModel/definition/tables/Seleccion Challenger.tmdl`
2. Localizar la linea:
   ```
   #"Matriz 2024_Sheet" = Origen{[Item="Matriz 2025",Kind="Sheet"]}[Data],
   ```
3. Cambiar `"Matriz 2025"` por `"Matriz 2026"` (o el nombre de la nueva hoja)
4. Guardar el archivo TMDL
5. Reabrir el proyecto en Power BI Desktop y actualizar

> El mismo procedimiento aplica para las tablas de seleccion de las otras empresas si sus archivos fuente tienen el mismo patron de nombre de hoja.

---

## 6. Publicar al servicio Power BI

`Pendiente de confirmar` — El proceso de publicacion al Power BI Service (workspace destino, frecuencia de actualizacion programada) no esta documentado en el repositorio.

Pasos generales:
1. Con el proyecto abierto y actualizado en Power BI Desktop
2. Ir a **Inicio → Publicar**
3. Seleccionar el workspace destino
4. Confirmar la publicacion

Para configurar actualizacion programada en el servicio:
- Ir al workspace en app.powerbi.com
- Dataset → Configuracion de actualizacion programada
- Configurar credenciales de gateway o nube para las dos cuentas de SharePoint

---

## 7. Verificar la fecha de actualizacion

Despues de cada actualizacion, navegar a la pagina **Fecha de Actualizacion** en el reporte para confirmar que la tabla `tbl_Refresh` registro correctamente la hora de la actualizacion en zona horaria Bogota (UTC-5).

---

## 8. Problemas conocidos y soluciones

| Problema | Causa probable | Solucion |
|---|---|---|
| Error al cargar `PLANTA DE PERSONAL` | Credencial de Cuenta A vencida o nombre de hoja cambiado | Renovar credencial o verificar nombre de hoja en el Excel |
| Error al cargar `Consolidado2025` | Mismo archivo o credencial que PLANTA DE PERSONAL | Idem |
| Datos de 2025 no aparecen | `Consolidado2025` no se actualizo o la URL del archivo cambio | Verificar URL en el codigo M de `Consolidado2025.tmdl` |
| Timeout en actualizacion | Modelo muy grande o conexion lenta | El timeout esta configurado en 225 segundos. Verificar conexion a internet |
| Medida `Prom_Colaboradores` muestra valor incorrecto | Hardcoding de 7 meses | Ver [METRICS_CATALOG.md](METRICS_CATALOG.md#1-headcount-y-demografia-planta-de-personal) |
| Pagina QA_Demografico visible para usuarios | Configuracion de visibilidad | Cambiar `visibility` en `page.json` a `HiddenInViewMode` si se decide ocultar |

---

## 9. Estructura de archivos a mantener actualizados

Al realizar cambios en el modelo, los archivos que tipicamente se modifican son:

```
PBIP/Proyecto.SemanticModel/definition/
├── model.tmdl                  -- Si se cambia el orden de tablas o grupos
├── relationships.tmdl          -- Si se agregan o modifican relaciones
└── tables/
    ├── [NombreTabla].tmdl      -- Cada tabla modificada
    └── ...
PBIP/Proyecto.Report/definition/
├── pages/[ID_Pagina]/
│   └── page.json               -- Si se modifica una pagina
└── bookmarks/
    └── bookmarks.json          -- Si se modifican bookmarks
```
