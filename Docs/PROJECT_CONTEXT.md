# Contexto del Proyecto

> Fuente oficial del contexto de negocio. Ver el modelo tecnico en [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Descripcion general

**Planeacion de Personal** es un reporte de People Analytics construido en Power BI (formato PBIP) para el **Grupo Empresarial Lemco**. Su proposito es centralizar los indicadores de gestion de talento humano de todas las empresas del grupo en un unico instrumento analitico.

El reporte es operado por el area de **Gerencia Corporativa de Gestion Humana** y su consumo es interno.

---

## Grupo Empresarial Lemco

El modelo gestiona datos de las siguientes empresas, agrupadas segun la tabla `Empresas` del modelo semantico:

| Empresa | Grupo |
|---|---|
| Challenger | Challenger |
| Fundacion Challenger | Fundacion Challenger |
| Lemco | Lemco |
| Lemco Inmobiliaria | Lemco |
| Lemco Salvio | Habitel Hotels |
| Operadora | Habitel Hotels |
| Habitel Prime | Habitel Hotels |
| Habitel Select | Habitel Hotels |
| Habitel Nomina Compartida | Habitel Hotels |
| Sky Forwarder | Grupo Sky |
| Sky Industrial | Grupo Sky |
| Sky Logistica Integral | Grupo Sky |

> Evidencia: `PBIP/Proyecto.SemanticModel/definition/tables/Empresas.tmdl` (tabla `Empresas`, columna calculada `Grupo Empresa`).

---

## Dominios cubiertos

El reporte cubre seis dominios funcionales de gestion humana:

### 1. HeadCount
Planta de personal activa por mes y empresa. Incluye datos historicos desde 2024. Permite analizar composicion por tipo de contrato, genero, generacion, area, dependencia, estado civil y nivel educativo.

### 2. Presupuesto vs Real (PptovsReal)
Comparacion entre la planta presupuestada y la planta real ejecutada. Incluye indicadores de variacion interanual, eficiencia de gasto laboral frente a ventas, ingresos y retiros.

Las consultas `Planta Ppto`, `Ppto Retiros` y `Ppto Ingresos` consumen `PptovsReal.xlsx` desde SharePoint corporativo mediante `Excel.Workbook(Web.Contents(...), null, true)`. Esta migracion fue validada por refresh y revision funcional del usuario, y quedo publicada en el commit tecnico `e287657acc948672b274d7907b736a455428a258`.

En la pagina Retiros se incorpora una matriz de antiguedad del personal retirado por ano. Su proposito es analizar la distribucion de retiros segun el rango de antiguedad al retiro, calculado desde `Fecha Inicio` y `Fecha Vencimiento` en `Ppto Retiros`.

### 3. Seleccion
Seguimiento de procesos de seleccion (requisiciones) por empresa. Registra fechas de requerimiento, meta de cierre, terminacion del proceso, tiempos de seleccion y origen de la vacante.

### 4. Ausentismo e Incapacidades
Registro de ausencias laborales con clasificacion por concepto de ausentismo, y registro de incapacidades medicas con diagnostico CIE-10.

### 5. Seguridad y Salud en el Trabajo (SST)
Accidentalidad laboral con indicadores de frecuencia, severidad y tasa de accidentes. Datos por empresa, mes y ano.

### 6. SENA
Cupo de aprendices SENA por empresa y unidad. Supuesto: hace parte del cumplimiento legal de cuota de aprendizaje (`Pendiente de confirmar`).

---

## Clasificaciones transversales

El modelo usa las siguientes clasificaciones que aplican a multiples dominios:

- **Tipo de contrato:** Indefinido, Fijo, Temporal, Contrato de Aprendizaje (SENA)
- **Generaciones:** Baby Boomers (1946-1964), Generacion X (1964-1980), Millennials (1981-1996), Centennials (1997-2010)
- **Periodos:** Ano / Mes / Trimestre (actual y anterior dinamicos via `DimPeriodoYM`)

---

## Alcance temporal

- **Dato mas antiguo identificado:** 2024 (`Consolidado 2024.xlsx`)
- **Dato mas reciente en uso funcional:** 2026, con corte de trabajo junio 2026 en páginas operativas del reporte (`Pendiente de validación final de refresh`)
- **Fuentes históricas identificadas:** `Consolidado 2024.xlsx`, `Consolidado 2025.xlsx` y archivos de presupuesto/real usados para 2026
- **Cobertura futura:** requiere validar fuentes 2026 adicionales y refresh completo

> Nota (verificado 2026-07-03): la carpeta `Data/` esta **vacia** en el repositorio local — no existe la subcarpeta `Data/2026/05_Mayo/` mencionada en versiones anteriores de este documento y de `Docs/CHANGELOG.md`. No se ha confirmado si ese contenido se elimino, se movio, o nunca se llego a versionar localmente; `Pendiente de confirmar` con el usuario. `Data/` esta excluida de Git por `.gitignore`, por lo que su historial no es recuperable desde el repositorio.

---

## Audiencia del reporte

- **Audiencia primaria:** Gerencia Corporativa de Gestion Humana, directores de area
- **Audiencia secundaria:** No identificada en el repositorio (`Pendiente de confirmar`)
- **Audiencia tecnica:** Desarrollador/analista responsable del modelo (propietario de archivos: cuenta `edwin_clavijo_challenger_co`)

---

## Tecnologias utilizadas

| Tecnologia | Rol |
|---|---|
| Power BI Desktop (formato PBIP) | Herramienta de desarrollo y visualizacion |
| DAX | Lenguaje de medidas y columnas calculadas |
| Power Query (M) | Transformacion e integracion de datos |
| SharePoint / OneDrive | Almacenamiento de archivos fuente (Excel) |
| Microsoft Excel | Formato de los archivos fuente de datos |
| TMDL (Tabular Model Definition Language) | Formato de definicion del modelo semantico |

---

## Limitaciones conocidas

1. Existe control de versiones Git, pero el repositorio mantiene cambios PBIP acumulados pendientes de saneamiento y requiere staging selectivo por alcance.
2. La migración de rutas personales a SharePoint corporativo está en curso para el repositorio en general; `PptovsReal.xlsx` ya fue migrado y publicado para `Planta Ppto`, `Ppto Retiros` y `Ppto Ingresos`, pero aún existen otras fuentes personales o pendientes de análisis.
3. Persisten riesgos de Formula Firewall en Power Query hasta validar `Aplicar cambios` y refresh completo en Power BI Desktop.
4. No hay parámetros de Power Query: las rutas están hardcodeadas en el código M.
5. No hay evidencia documental de RLS configurado en el modelo.
6. La publicación al servicio Power BI y refresh programado siguen pendientes de documentación formal.

> Ver detalles en [PROJECT_STATUS.md](PROJECT_STATUS.md), [SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md), [DATA_PIPELINE.md](DATA_PIPELINE.md) y [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
