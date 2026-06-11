# Planeacion de Personal — People Analytics

Reporte de People Analytics del **Grupo Empresarial Lemco** construido en formato **Power BI Project (PBIP)**.

Cubre los dominios de HeadCount, Presupuesto vs Real, Seleccion, Ausentismo, Incapacidades y Seguridad y Salud en el Trabajo (SST) para las empresas del grupo: Challenger, Habitel Hotels, Grupo Sky, Lemco y Fundacion Challenger.

## Documentacion tecnica

La documentacion detallada del proyecto se encuentra en la carpeta [`Docs/`](Docs/README.md).

| Documento | Descripcion |
|---|---|
| [Contexto del Proyecto](Docs/PROJECT_CONTEXT.md) | Proposito, dominio de negocio y empresas del grupo |
| [Arquitectura](Docs/ARCHITECTURE.md) | Estructura PBIP, modelo semantico y reporte |
| [Modelo de Datos](Docs/DATA_MODEL.md) | Tablas, columnas, relaciones y cardinalidades |
| [Catalogo de Metricas](Docs/METRICS_CATALOG.md) | Medidas DAX clasificadas por dominio |
| [Pipeline de Datos](Docs/DATA_PIPELINE.md) | Fuentes, Power Query y proceso de actualizacion |
| [Guia de BI](Docs/BI_GUIDELINES.md) | Paginas del reporte, bookmarks y convenciones |
| [Seguridad y Privacidad](Docs/SECURITY_AND_PRIVACY.md) | Datos sensibles, accesos y riesgos |
| [Runbook Operativo](Docs/RUNBOOK.md) | Procedimientos de mantenimiento y actualizacion |
| [Registro de Cambios](Docs/CHANGELOG.md) | Historial de versiones |

## Estructura del repositorio

```
07_Planeacion_de_Personal/
├── Data/               # Datos locales de referencia (actualmente 2026/05_Mayo/)
├── Docs/               # Documentacion tecnica del proyecto
└── PBIP/               # Proyecto Power BI en formato PBIP
    ├── Proyecto.pbip               # Archivo de entrada del proyecto
    ├── Proyecto.Report/            # Definicion del reporte
    └── Proyecto.SemanticModel/     # Modelo semantico (TMDL + DAX + Power Query)
```

## Estado actual

- **Formato:** Power BI Project (PBIP) v1.0
- **Control de versiones:** No configurado (`Pendiente de confirmar`)
- **Ultima actualizacion del modelo:** visible en la pagina *Fecha de Actualizacion* del reporte
- **Cultura del modelo:** `es-ES` / `es-CO`
