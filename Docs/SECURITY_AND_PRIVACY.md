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

## Fuentes normativas y gobierno de datos

| Documento | Código | Versión / fecha | Ruta | Propósito | Alcance | Relevancia para el proyecto |
|---|---|---|---|---|---|---|
| [Política de Tratamiento de Datos Versión Web](<20241025 CSP-POL-09 Política de Tratamiento de Datos Version Web (002).pdf>) | `CSP-POL-09` | Versión 8, 25 de octubre de 2024 | `Docs/20241025 CSP-POL-09 Política de Tratamiento de Datos Version Web (002).pdf` | Fuente corporativa oficial para orientar el tratamiento de datos personales. | Aplica a las empresas que conforman el Grupo LEMCO y regula la recolección, almacenamiento, uso, circulación y supresión de datos personales, así como su transferencia y transmisión. | Debe considerarse como referencia de gobierno para este proyecto de Gestión Humana y People Analytics, porque el modelo procesa datos personales, incluidos datos privados y sensibles. |

Esta referencia no reemplaza el análisis técnico de sensibilidad del modelo ni las validaciones de acceso, RLS, credenciales y privacidad de Power BI. Su función es dejar trazabilidad de la política corporativa que gobierna el tratamiento de los datos usados por el proyecto.

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

Las fuentes de datos estan en SharePoint/OneDrive de Microsoft 365. El objetivo de gobierno es usar el sitio corporativo `TalentoHumanoGrupoLemco` y credenciales organizacionales, evitando dependencia de rutas personales.

Estado documentado al 2026-07-17:

| Origen | Estado | Riesgo |
|---|---|---|
| Sitio corporativo `lemcosas.sharepoint.com/sites/TalentoHumanoGrupoLemco` | Ruta objetivo para fuentes gobernadas | Requiere permisos organizacionales y niveles de privacidad consistentes |
| Cuenta personal `edwin_clavijo_challenger_co` | Origen histórico de varias fuentes | Riesgo de continuidad si persisten dependencias |
| Cuenta personal `maria_bohorquez_challenger_co` | Origen histórico de Ausentismos, Estructura y otras fuentes | Riesgo de continuidad y Formula Firewall si se mezcla con sitio corporativo |

**Riesgos identificados:**
1. Las rutas personales remanentes pueden fallar si la cuenta cambia, se desactiva o pierde permisos.
2. Entradas duplicadas de SharePoint con distintos niveles de privacidad pueden activar Formula Firewall.
3. No existe una cuenta de servicio dedicada para el pipeline de datos.
4. No hay documentación final de credenciales, gateway o refresh programado en Power BI Service.

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
2. **Finalizar la migración de archivos fuente a SharePoint corporativo** y eliminar gradualmente dependencias de rutas personales.
3. **Crear parametros de Power Query** para las rutas de los archivos, facilitando migracion sin edicion del codigo M.
4. **Revisar si los campos de datos personales sensibles** (direccion, telefono, email, salario) son necesarios en el modelo o pueden eliminarse/enmascararse.
5. **Documentar y cumplir con la politica de tratamiento de datos** de la organizacion bajo la Ley 1581 de 2012.
6. **Mantener el repositorio Git con staging selectivo** y no versionar `Data/`, `Outputs/` ni archivos con datos personales.
7. **Evaluar el contenido de `Inputs/Base_Rotacion_Atraccion_Seleccion.xlsx`** (agregado 2026-07-03) para confirmar si tiene datos personales; si los tiene, tratarlo como `Data/` y no versionarlo.
