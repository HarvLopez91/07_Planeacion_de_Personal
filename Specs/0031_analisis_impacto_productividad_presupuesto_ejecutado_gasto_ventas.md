# Análisis de impacto — Productividad: presupuesto y ejecutado de gasto y ventas

Fecha: 2026-09-10
Estado: ANÁLISIS COMPLETO — implementación no autorizada; gate de unidad monetaria pendiente
Iniciativa: `PBIP-009`
Página: `Productividad` (`ReportSection65569958420c423d90b1`)

## 1. Objetivo y alcance

Evaluar el impacto de incorporar en `Productividad` presupuesto, ejecutado, diferencia absoluta y variación porcentual de Gasto de Personal y Ventas. Este documento no implementa DAX, visuales, relaciones, Power Query ni cambios en datos.

## 2. Estado de repositorio auditado

- Rama local: `feat/hc-validacion-ingresos-retiros-agosto-2026`.
- `HEAD`: `e73bd71896cc60c9bd8ac395fbdba084aab34cae`.
- `origin/main`: `3bc4f45fa8295dad6e0e0ab59204fdddb66c6698`.
- La rama local tiene un commit propio y está dos commits detrás de `origin/main`.
- El checkout contiene numerosos cambios concurrentes de Power BI Desktop/OneDrive y trabajo PBIP-008 ajeno.
- No existe staging activo.
- La página `Productividad`, `Planta Ppto.tmdl` y `relationships.tmdl` coinciden con `origin/main`.
- `Tbl_Medidas.tmdl` tiene cambios locales ajenos, pero las medidas de Productividad auditadas no presentan diferencias semánticas frente a `origin/main`.

Una fase futura debe usar un worktree limpio desde el `origin/main` vigente y trasladar únicamente el alcance aprobado.

## 3. Fuente, grano y calidad

### 3.1 Fuente efectiva

`Planta Ppto` importa desde SharePoint corporativo:

`Data/HeadCount/PptovsReal.xlsx` → hoja `Planta Personal`.

La consulta M promueve encabezados y tipa como moneda/decimal `Ventas (MM)`, `Gasto Personal`, `Ppto Ventas (MM)` y `Ppto Gasto Personal`. El archivo local sincronizado se inspeccionó solo en lectura.

### 3.2 Grano observado

La hoja contiene 1.072 filas, 21 columnas y 48 periodos entre 2023-01 y 2026-12.

Grano físico único:

`Ppto/Real + Año + Mes + Grupo Empresa + Empresa`

- 1.072 claves únicas y 0 duplicadas;
- 5 grupos y 12 empresas;
- 528 filas `PPTO` y 544 filas `REAL`.

Sin `Ppto/Real` aparecen 520 pares esperados `PPTO`/`REAL`. Sumar sin identificar el estado canónico puede duplicar importes.

### 3.3 Disponibilidad

| Columna | Numéricos | Blancos | Ceros explícitos | Negativos |
|---|---:|---:|---:|---:|
| `Ventas (MM)` | 206 | 866 | 0 | 0 |
| `Gasto Personal` | 273 | 798 | 0 | 0 |
| `Ppto Ventas (MM)` | 199 | 873 | 0 | 0 |
| `Ppto Gasto Personal` | 312 | 760 | 0 | 0 |

Hallazgos:

1. Los cuatro importes están poblados principalmente en filas `REAL`, incluso los presupuestos.
2. Cinco valores de `Ppto Ventas (MM)` de Challenger, enero-mayo de 2026, están poblados tanto en `PPTO` como en la fila `REAL` de la misma clave; un `SUM` sin filtro los cuenta dos veces.
3. `Gasto Personal` contiene una fórmula Excel histórica con valor calculado disponible.
4. En 2023 los cuatro importes están vacíos.
5. En 2026 la ejecución llega hasta julio; presupuestos futuros existen para varios negocios con cobertura desigual.
6. Un `BLANK` no equivale a ejecución cero.

### 3.4 Gate de unidad monetaria

Las columnas no tienen una escala homogénea a través del histórico: conviven importes con orden de magnitud compatible con pesos completos y otros ya expresados en millones, con cambios por grupo y año. Challenger conserva magnitudes de pesos completos en 2024-2026, mientras otros grupos alternan escalas entre años.

`Prod_Usar_Millones` y `GL_Usar_Millones` controlan el formato; no convierten cada fila a una unidad canónica antes de sumar. Por ello:

**las cuatro columnas no pueden sumarse directamente en una vista consolidada hasta gobernar la unidad monetaria por empresa y periodo.**

Dentro de un contexto homogéneo pueden compararse si también se aplica la regla canónica de `Ppto/Real` y se controla la cobertura.

## 4. Medidas existentes y reutilización

| Medida | DAX/dependencia actual | Visuales consumidores | Decisión |
|---|---|---|---|
| `Efic` | `SUM(Gasto Personal) / SUM(Ventas (MM))` | `76f...`, `9bcb...`, `d601...` | Preservar; es una razón, no un importe. Usa `/` y no controla cero. |
| `%Efiprom` | `SUM(Ppto Gasto Personal) / SUM(Ppto Ventas (MM))` | `76f...`, `9bcb...`, `d601...` | Preservar como baseline; no sustituye los presupuestos y hereda el riesgo de cinco filas. |
| `KPI_EFI` | compara `[Efic] > [%Efiprom]` | tarjeta `285f...` | Preservar. |
| `Var_GL` | `[Efic] / [%Efiprom]` | tarjeta `285f...` | No equivale a variación presupuesto-ejecutado. |
| `Cump_GL` | gasto real / presupuesto de gasto | Gasto Laboral | No equivale a la variación requerida. |
| `GL_Ppto_Gasto_Personal` | suma presupuesto de gasto; formato dinámico | tabla Gasto Laboral | Referencia reutilizable solo tras resolver unidad/estado; no modificar por riesgo transversal. |
| `GL_Gasto_Personal` | suma gasto ejecutado; formato dinámico | tabla Gasto Laboral | Misma consideración. |
| `GL_Usar_Millones` | decide formato Challenger/consolidado vs otros | auxiliar | Reutilizar criterio de presentación, no como conversión. |
| `GL_*_Visual_Challenger/Otros` | alternan series de dos gráficos | Gasto Laboral | No usar en nuevos KPIs de Productividad. |
| `Prod_Gasto_Personal` | `SUM(Gasto Personal)` | base de tabla Productividad | Reutilizable en contexto homogéneo. |
| `Prod_Ingreso_Operacional` | `SUM(Ventas (MM))` | base de tabla Productividad | Reutilizable en contexto homogéneo. |
| `Prod_Usar_Millones` | decide formato por negocio | auxiliares | Reutilizar para formato, no normalización. |
| `Prod_Gasto_Personal_Tabla` | base con formato dinámico | `cba...` | Preservar. |
| `Prod_Ingreso_Operacional_Tabla` | base con formato dinámico | `cba...` | Preservar. |
| `Prod_Efic_Tabla` | `[Efic]` | `cba...` | Preservar. |
| `Titulo_Productividad_Gasto_Laboral` | título por año | `d601...` | Preservar. |
| `Subtitulo_Productividad_Comparativo_Acumulado` | texto por meses | `76f...` | Preservar. |

No existe medida explícita y segura para presupuesto de ventas ni medidas de diferencia absoluta/porcentual de ambos dominios.

## 5. Relaciones y filtros

| Hecho | Dimensión | Estado |
|---|---|---|
| `Planta Ppto[Empresa]` | `Empresas[Empresas]` | activa, muchos-a-uno, filtro simple por defecto |
| `Planta Ppto[Año]` | `Años[Año]` | activa, muchos-a-uno, filtro simple por defecto |
| `Planta Ppto[Mes]` | `Mes[Meses]` | activa, muchos-a-uno, filtro simple por defecto |
| `Planta Ppto[IndexAnioMes]` | `DimPeriodoYM[IndexAnioMes]` | activa, muchos-a-uno, filtro simple por defecto |

El grupo se propaga mediante `Grupo Empresarial → Empresas[Grupo Empresa] → Empresas[Empresas] → Planta Ppto[Empresa]`. La página usa `Años[Año]`, `Mes[Meses]`, `Empresas[Grupo Empresa]` y `Empresas[Empresas]`. No se observaron relaciones bidireccionales ni muchos-a-muchos en este recorrido.

Los nuevos visuales deben heredar esas dimensiones; no deben crear relaciones ni usar `Planta Ppto[Grupo Empresa]` como slicer.

## 6. Semántica de diferencias

La misma fórmula es correcta para ambos dominios:

- diferencia absoluta = ejecutado − presupuesto;
- variación % = `(ejecutado − presupuesto) / presupuesto`.

No debe invertirse el signo de gasto. La interpretación se resuelve visualmente:

- Gasto positivo: desfavorable/sobre-ejecución.
- Ventas positivo: favorable/superación del presupuesto.

## 7. Propuesta técnica condicionada

### 7.1 Base canónica

Antes de implementar, las cuatro magnitudes deben expresarse en una unidad común. Se recomienda millones de COP para Productividad, con regla gobernada por empresa y vigencia; nunca inferida por magnitud. La opción preferida es normalizar en el contrato de datos. Una tabla de factores por empresa/periodo solo es aceptable si negocio aprueba su mantenimiento.

Una vez disponibles `[Prod Gasto Presupuesto MM]`, `[Prod Gasto Ejecutado MM]`, `[Prod Ventas Presupuesto MM]` y `[Prod Ventas Ejecutadas MM]`, se proponen:

```DAX
Prod Diferencia Gasto MM =
VAR _Ejecutado = [Prod Gasto Ejecutado MM]
VAR _Presupuesto = [Prod Gasto Presupuesto MM]
RETURN
    IF ( ISBLANK ( _Ejecutado ) || ISBLANK ( _Presupuesto ), BLANK (), _Ejecutado - _Presupuesto )
```

```DAX
Prod Variación Gasto % =
VAR _Presupuesto = [Prod Gasto Presupuesto MM]
RETURN
    IF ( ISBLANK ( _Presupuesto ) || _Presupuesto = 0, BLANK (), DIVIDE ( [Prod Diferencia Gasto MM], _Presupuesto ) )
```

```DAX
Prod Diferencia Ventas MM =
VAR _Ejecutado = [Prod Ventas Ejecutadas MM]
VAR _Presupuesto = [Prod Ventas Presupuesto MM]
RETURN
    IF ( ISBLANK ( _Ejecutado ) || ISBLANK ( _Presupuesto ), BLANK (), _Ejecutado - _Presupuesto )
```

```DAX
Prod Variación Ventas % =
VAR _Presupuesto = [Prod Ventas Presupuesto MM]
RETURN
    IF ( ISBLANK ( _Presupuesto ) || _Presupuesto = 0, BLANK (), DIVIDE ( [Prod Diferencia Ventas MM], _Presupuesto ) )
```

Las medidas base deben aplicar conversión gobernada, filtro canónico de estado con `KEEPFILTERS`, y agregación de importes. Nunca se suman porcentajes.

No se propone DAX de conversión hasta que exista la regla de escalas aprobada; inferirla sería frágil y no auditable.

### 7.2 Blancos, ceros y formato

- Presupuesto o ejecutado `BLANK`: diferencia y variación `BLANK`.
- Presupuesto cero explícito: diferencia válida; variación `BLANK`.
- Ejecutado cero explícito: diferencia `-presupuesto`; variación `-100 %`.
- Importes: `$ #,0.0 "MM"` tras normalización.
- Variación: `0.0 %;-0.0 %;0.0 %`.
- No usar `FORMAT()` sobre medidas numéricas.

## 8. Página Productividad

La página mide 1350×900 y contiene 12 visuales.

| ID | Tipo | Función |
|---|---|---|
| `218c...` | slicer | Año |
| `28f...` | slicer | Mes |
| `4f44...` | slicer | Grupo Empresa |
| `3dd...` | slicer | Empresa |
| `d601...` | combo | Efic vs presupuesto por mes |
| `76fb...` | combo | comparación acumulada por año |
| `cba...` | tabla | gasto, ingreso y eficiencia por mes |
| `9bcb...` | tabla | `Efic` y `%Efiprom` |
| `285f...` | tarjeta | `KPI_EFI`/`Var_GL` |
| restantes | forma/navegación | estructura |

No hay interacciones personalizadas de página. Hay filtros persistidos en slicers/visuales, pero ningún bookmark referencia la página ni sus visuales.

### Alternativa 1 — recomendada

Dos bloques KPI compactos apilados en el espacio inferior derecho:

- `Gasto de Personal`: Presupuesto | Ejecutado | Diferencia | Variación %.
- `Ventas`: Presupuesto | Ejecutado | Diferencia | Variación %.

Cada bloque sería una tarjeta multivalor o matriz de una fila. Mantiene intactos los gráficos y la tabla actuales y evita ocho tarjetas independientes.

### Alternativa 2

Ampliar `cba...` con presupuesto y variaciones por mes, y reservar dos tarjetas para síntesis anual. Aporta detalle, pero aumenta ancho, desplazamiento y carga cognitiva.

## 9. Riesgos y controles

| Nivel | Riesgo | Control |
|---|---|---|
| Crítico | suma consolidada con escalas mixtas | contrato de unidad y normalización previa |
| Alto | cinco presupuestos de ventas contados dos veces | estado canónico con `KEEPFILTERS` y conciliación |
| Alto | meses futuros tratados como ejecución cero | preservar `BLANK` |
| Alto | regresión en `Efic`/`%Efiprom` | capa nueva y pruebas antes/después |
| Medio | cobertura desigual por grupo/año | matriz de completitud y mensaje sin dato |
| Medio | suma de porcentajes | recalcular desde importes agregados |
| Medio | filtros no propagados | dimensiones existentes y pruebas cruzadas |
| Medio | formato confundido con conversión | separar valor canónico y formato |
| Medio | filtros persistidos | prueba visual por contexto |
| Medio | churn/concurrencia | worktree limpio y diff estricto |

## 10. Matriz mínima de pruebas

En cada escenario se concilian los ocho resultados y se verifica que `Efic` y `%Efiprom` no cambian.

| Escenario | Foco adicional |
|---|---|
| Año 2026 | ejecución solo donde exista; futuros sin falsos ceros |
| Mes individual | diferencias y porcentajes exactos |
| Varios meses | suma de importes y razón recalculada |
| Consolidado | unidad común demostrada |
| Challenger | conversión de pesos a MM y polaridad |
| Fundación Challenger | cobertura parcial y `BLANK` |
| Grupo Sky | vigencia de escala por año/empresa |
| Habitel Hotels | cambio histórico de escala |
| Lemco | presupuesto faltante sin variación artificial |
| Empresa individual | coherencia empresa/grupo/periodo |

También deben probarse presupuesto cero/`BLANK`, ejecutado cero/`BLANK`, suma consolidada contra grupos, cero duplicados lógicos y ausencia de cambios en otras páginas.

## 11. Archivos probables de una implementación futura

Mínimo:

- `PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl`;
- uno o dos `visual.json` nuevos bajo la página Productividad;
- pruebas estáticas específicas;
- plan de implementación posterior, solo con autorización.

Condicionado al gate de unidad: contrato/fuente de escalas y, eventualmente, `Planta Ppto.tmdl` si la normalización se resuelve en Power Query.

No deberían tocarse `relationships.tmdl`, otras páginas, `pages.json`, bookmarks, tema global, medidas históricas `Efic`/`%Efiprom`/`KPI_EFI`/`Var_GL`/`Cump_GL`, ni `PptovsReal.xlsx` sin requerimiento separado.

## 12. Decisiones requeridas

1. Definir unidad canónica y regla de conversión por empresa/vigencia.
2. Confirmar que los cinco presupuestos de ventas duplicados se cuentan una vez y que la fila `REAL` es canónica según el patrón actual.
3. Aprobar que ausencia de ejecutado o presupuesto produzca `BLANK`.
4. Aprobar la Alternativa visual 1 y la polaridad: gasto positivo desfavorable; ventas positivo favorable.
5. Decidir si se corrige después el mismo riesgo en `%Efiprom`; incluirlo ahora ampliaría el impacto y exigiría regresión propia.

## 13. Conclusión

La página puede alojar el requerimiento sin relaciones nuevas y sin sustituir indicadores actuales. La aritmética propuesta es válida y la diferencia semántica se resuelve visualmente, no invirtiendo signos.

La implementación no debe comenzar todavía: la escala monetaria mixta impide una suma consolidada confiable y existe una duplicidad localizada en presupuesto de ventas. El siguiente gate es aprobar el contrato de unidad y la fila canónica; después podrá prepararse un plan de implementación controlado.
