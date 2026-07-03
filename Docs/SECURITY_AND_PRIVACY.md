# Seguridad y Privacidad

> Documento de referencia para la gestion de datos sensibles, control de acceso y riesgos de privacidad en el proyecto.
> No incluye credenciales, contrasenas ni URLs completas con tokens de autenticacion.

---

## Nivel de sensibilidad del proyecto

Este proyecto maneja **datos personales de empleados** del Grupo Empresarial Lemco. Se considera de **sensibilidad ALTA** por contener:

- Nombres completos de colaboradores
- Numeros de identificacion (cedulas)
- Fechas de nacimiento
- Ciudad y direccion de residencia
- Estado civil
- Nivel educativo
- Numero de hijos
- Salario basico (en `PLANTA DE PERSONAL.SUELDO_B`)
- Correo electronico y telefono personal
- Diagnosticos medicos CIE-10 (en `Incapacidades`)
- Datos de accidentalidad laboral individual (en `ACCIDENTALIDAD`)
- Afiliaciones a EPS, AFP, Caja de Compensacion, CCF

---

## Campos con datos personales por tabla

| Tabla | Campos sensibles identificados |
|---|---|
| `PLANTA DE PERSONAL` | `ID`, `NOMBRE EMPLEADO`, `F_INICIO`, `SEXO`, `FECHA NACIMIENTO`, `CIUDAD DE RESIDENCIA`, `DIRECCION RESIDENCIA`, `EST_CIVIL`, `NIVEL EDUCATIVO`, `TELEFONO`, `EMAIL`, `SUELDO_B`, `HIJOS`, `EPS`, `AFP`, `CAJA_COMO`, `CCF`, `AFC` |
| `Ppto Retiros` | `Identificacion`, `Nombres`, `Apellidos`, `Salario`, `TC` (tipo contrato) |
| `Ppto Ingresos` | `Identificacion` (usada para relacionar con `Maestro`) |
| `AUSENTISMOS` | `Identificacion`, `Nombre`, `Fecha de nacimiento`, `Genero`, `Rango de Edad` |
| `Incapacidades` | `Identificacion`, `Diagnostico` (codigo CIE-10 — dato de salud), `Descripcion Diagnostico` |
| `ACCIDENTALIDAD` | `IDENTIFICACION`, `Apellidos y Nombre`, `Edad`, `Genero`, `Salario` |
| `Maestro` | `Identificacion`, `Fecha Nacimiento`, `Sexo` |
| `Seleccion Challenger` | `CARGO`, `JEFE`, `ESTADO`, fechas del proceso |

> Los campos de identificacion personal (cedula, nombre completo, fecha de nacimiento) son datos personales segun la Ley 1581 de 2012 (Colombia — Ley de Proteccion de Datos Personales).
> Los datos de diagnostico medico (CIE-10) son datos sensibles de salud y tienen un nivel de proteccion mas alto.

---

## Control de acceso al reporte

| Aspecto | Estado actual | Riesgo |
|---|---|---|
| Publicacion en Power BI Service | `Pendiente de confirmar` — No documentado en el repositorio | No se conoce quien tiene acceso al reporte publicado |
| Politica de Row-Level Security (RLS) | **No identificada en el modelo** — No hay roles definidos en los archivos TMDL | Todos los usuarios con acceso al reporte ven datos de todas las empresas |
| Exportacion de datos | Configurada como `AllowSummarized` — no permite exportar datos individuales | Mitigacion parcial |
| Filtros de usuario | No hay filtros personalizados por usuario identificados | Un usuario puede ver datos de todas las empresas del grupo |

> La ausencia de Row-Level Security (RLS) es un riesgo significativo dado el nivel de detalle nominal del modelo (nombres, cedulas, salarios).

---

## Gestion de credenciales de fuentes de datos

Las fuentes de datos estan en SharePoint/OneDrive de Microsoft 365. El acceso requiere autenticacion con las cuentas propietarias de los archivos:

| Cuenta | Archivos que gestiona | Riesgo |
|---|---|---|
| Cuenta A (`edwin_clavijo_challenger_co`) | HeadCount, PptovsReal, SST | Si esta cuenta cambia de contrasena o es desactivada, la mitad del modelo falla |
| Cuenta B (`maria_bohorquez_challenger_co`) | Ausentismos, Maestro, Incapacidades, Seleccion, Estructura | Idem |

**Riesgos identificados:**
1. Las credenciales son personales. Si la persona deja la organizacion, el modelo pierde acceso a sus fuentes.
2. No existe una cuenta de servicio dedicada para el pipeline de datos.
3. Los archivos estan en carpetas personales de OneDrive, no en un sitio SharePoint compartido de equipo.

---

## Archivos del repositorio con datos sensibles

Los siguientes archivos del repositorio local **no deben compartirse publicamente** ni incluirse en repositorios Git publicos:

| Archivo | Razon |
|---|---|
| `PBIP/Proyecto.SemanticModel/.pbi/cache.abf` | Cache binario del modelo Analysis Services — puede contener datos en memoria |
| `PBIP/Proyecto.Report/.pbi/localSettings.json` | Configuracion local del editor — puede contener rutas o preferencias de usuario |
| `PBIP/Proyecto.SemanticModel/.pbi/localSettings.json` | Idem |
| Archivos `.xlsx` en `Data/` | Si se agregan datos fuente al repositorio local, podrian contener datos personales |
| **Archivos en `Inputs/`** | **Riesgo ALTO, sin evaluar (agregado 2026-07-03).** La carpeta `Inputs/` contiene hoy `Base_Rotacion_Atraccion_Seleccion.xlsx` (496 KB). Por su nombre ("Rotacion" y "Atraccion y Seleccion"), es probable que incluya datos nominales de colaboradores o candidatos. **No se ha confirmado su contenido.** Tratar como `Data/` (no versionar) hasta que se evalue explicitamente. Ver tambien `Docs/ESTRUCTURA_PROYECTO.md` seccion 11. |

> El archivo `PBIP/.gitignore` ya esta presente en el proyecto. Se recomienda verificar que `cache.abf` y `localSettings.json` esten incluidos en las exclusiones.
>
> `Inputs/` **no esta** en `.gitignore` a nivel de contenido (`Inputs/*`) — solo el nombre de archivo especifico del PDF de marca y la carpeta completa quedan cubiertos tras la actualizacion del 2026-07-03. Ver seccion "Recomendaciones de control" para el detalle de la accion pendiente sobre `Inputs/`.

---

## Recomendaciones de control

Las siguientes son recomendaciones derivadas del analisis. Su implementacion es `Pendiente de decision`:

1. **Implementar Row-Level Security (RLS)** para restringir el acceso por empresa segun el usuario del reporte publicado.
2. **Migrar los archivos fuente a un sitio SharePoint de equipo** (no carpetas personales) con una cuenta de servicio.
3. **Crear parametros de Power Query** para las rutas de los archivos, facilitando migracion sin edicion del codigo M.
4. **Revisar si los campos de datos personales sensibles** (direccion, telefono, email, salario) son necesarios en el modelo o pueden eliminarse/enmascararse.
5. **Documentar y cumplir con la politica de tratamiento de datos** de la organizacion bajo la Ley 1581 de 2012.
6. **Inicializar un repositorio Git privado** con `.gitignore` correcto para versionar el proyecto sin exponer datos.
7. **Evaluar el contenido de `Inputs/Base_Rotacion_Atraccion_Seleccion.xlsx`** (agregado 2026-07-03) para confirmar si tiene datos personales; si los tiene, tratarlo como `Data/` y no versionarlo.
