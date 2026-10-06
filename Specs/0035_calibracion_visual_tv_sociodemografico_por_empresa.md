# 0035 - PBIP-010: Calibración visual para TV de «Sociodemográfico por Empresa»

## Objetivo

Hacer legible la página `Sociodemográfico por Empresa` cuando se proyecta en
televisores y pantallas grandes, sin alterar su lógica funcional.

El cierre de `PBIP-006` (2026-08-31) dejó la página en PASS funcional y PASS
visual **para uso en monitor**. Esta iniciativa no lo invalida: responde a un
**requisito de uso posterior** —lectura ejecutiva a distancia— que el PASS
anterior no evaluaba.

## 1. Alcance

- Página objetivo: `Sociodemográfico por Empresa`, id `1daffd26f7de1c038e95`.
- Solo propiedades de formato: tipografía, tamaños, colores de categoría, color
  de etiqueta y el ancho de la banda de encabezado.
- 20 de los 21 `visual.json` de la página.

Fuera de alcance:

- Medidas, relaciones, Power Query, modelo semántico y reglas de negocio.
- El tema global del reporte (`CY23SU08`), que no se tocó.
- Otras páginas, incluida `Demográfico (Promedio)`.
- Reconstruir la página o regenerar el PBIP.

## 2. Diagnóstico medido

### 2.1 Tipografía

Conteo de declaraciones `fontFamily` en las 17 páginas del reporte:

| Tipografía | Páginas |
|---|---|
| `Calibri` | **13** |
| `Segoe UI` | 1 (`Retiros y Rotación Predictiva`) |
| `Outfit` | **1 — solo esta página** (47 declaraciones) |
| hereda del tema | 2 |

Además, `Outfit` **no está instalada** en el equipo de autoría: de 235 familias
disponibles, no aparece. Una fuente ausente se sustituye por una de reserva con
métricas distintas, lo que explica que la página se percibiera diferente al
resto del proyecto.

### 2.2 Color

Los cuatro azules en uso tenían contraste insuficiente entre sí. El umbral para
elementos no textuales es **3:1** (WCAG 1.4.11):

| Par | Contraste |
|---|---|
| `#000032` vs `#0B1C35` | 1,18:1 |
| `#0B1C35` vs `#1A3059` | 1,31:1 |
| `#1A3059` vs `#1B487F` | 1,42:1 |

En `Antigüedad por Empresa`, con 7 categorías, el peor par adyacente era
**1,04:1** y había **3 pares perceptualmente indistinguibles**.

### 2.3 Contraste de las etiquetas de datos

Las etiquetas heredaban un color del tema (`ColorId 1` = `#12239E`):

| Fondo de barra | Contraste de la etiqueta |
|---|---|
| `#1B487F` | 1,30:1 |
| `#000032` | 1,68:1 |

Muy por debajo del mínimo de 4,5:1 para texto. Este defecto afectaba la lectura
incluso de cerca.

### 2.4 Tamaños

Títulos de visual en 14 pt; ejes, leyendas y etiquetas entre 8 y 11 pt; matriz
en 10/13 pt; slicers en 10–12 pt. Suficiente en monitor, insuficiente a
distancia.

### 2.5 Lienzo

Página de 2100 × 900 con `displayOption: FitToPage`. La banda de encabezado
medía 2299,5 px de ancho, de modo que se recortaba en el borde del lienzo.
`FitToPage` escala el lienzo declarado y **recorta** lo que sobresale; no reduce
la escala del contenido.

## 3. Decisiones aplicadas

### 3.1 Tipografía: `Calibri`

Motivo: es el estándar de hecho del proyecto (13 de 17 páginas), **está
instalada** y viaja con Office, por lo que su renderizado es idéntico en
Power BI Desktop y en el Service. Se reemplazaron las 49 declaraciones de la
página.

### 3.2 Paleta final

| Visual | Asignación |
|---|---|
| Colaboradores por Empresa | `#1B487F` (serie única, sin cambio) |
| Tipo de Contrato por Empresa | Indefinido `#1B487F` · Fijo `#4A7FC0` · Temporal `#7EB3E8` · Aprendizaje `#F7931E` |
| Tipo de Cargo por Empresa | Estratégicos `#000032` · Tácticos `#F7931E` · Administrativos `#4A7FC0` · Operativos `#7EB3E8` |
| Generación por Empresa | Baby Boomers `#000032` · Generación X `#1B487F` · Millennials `#4A7FC0` · Centennials `#F7931E` |
| Distribución de Género por Empresa | `#F7931E` / `#1B487F` (sin cambio, ya tenía contraste máximo) |
| Antigüedad por Empresa | a `#000032` · b `#1B487F` · c `#4A7FC0` · d `#7EB3E8` · e `#2E8C9A` · f `#B9C4CF` · g `#F7931E` |

- Salen de uso `#0B1C35` y `#1A3059`, los dos responsables de la confusión.
- Se conservan los colores ya aprobados `#000032`, `#1B487F`, `#4A7FC0` y
  `#7EB3E8`.
- `#F7931E` se mantiene como **acento**: una sola categoría por gráfico.
- `#2E8C9A` y `#B9C4CF` son **tonos derivados nuevos**, usados exclusivamente en
  `Antigüedad por Empresa`. Con 7 categorías una rampa monocroma deja pasos
  contiguos en 1,34:1; con estos dos tonos el conjunto baja de 3 pares
  confundibles a 1 par borderline. **No se consultó el manual de marca porque no
  está versionado en el repositorio**: se derivaron de la rampa azul aprobada.

### 3.3 Color de etiqueta por categoría

Se añadieron 19 entradas de `labels` con color explícito según el fondo de su
barra: blanco sobre `#000032` y `#1B487F`; `#000032` sobre los cinco tonos
claros. Cada entrada reutiliza el **selector exacto** de la entrada `dataPoint`
de esa misma categoría, de modo que no se construyó ninguna referencia a mano.

Contraste resultante: **4,86:1 en el peor caso**, todos cumplen AA.

### 3.4 Tamaños

| Rol | Antes | Después |
|---|---:|---:|
| Título de página | 20 pt | **28 pt** |
| Subtítulo de página | 11 pt | **14 pt** |
| Título de visual | 14 pt | **17 pt** |
| Ejes y leyendas | 8–11 pt | **12 pt** |
| Etiquetas de datos | 9–11 pt | **11–12 pt** |
| Matriz: encabezados / valores | 10 / 13 pt | **13 / 15 pt** |
| Slicers: items / encabezado | 10–12 / 12 pt | **13 / 14 pt** |
| Navegación: inactivo / activo | 12 / 16 pt | **14 / 18 pt** |

No se aplicó un valor único: cada rol se ajustó según su jerarquía y el espacio
disponible.

### 3.5 Lienzo

La banda de encabezado pasó de 2299,5 a **2100 px**, el ancho útil declarado.

El grupo `Grupo 3` (`89f626bb1de245191d62`) **no se modificó**: es un
`visualGroup` en `ScaleMode` con 10 hijos, y redimensionarlo escalaría a sus
hijos. Power BI Desktop puede recalcular sus límites al guardar; esa línea sería
ruido de re-serialización, no un defecto.

## 4. Cambios locales preservados

La página tenía dos cambios funcionales sin commit en el checkpoint principal.
Ambos son **intencionales** y se integraron en este cierre:

### 4.1 Último periodo vigente

El slicer de Mes (`8f50e5635a2bab2a9092`) conserva **`09.Septiembre`**, no
`07.Julio`. Se verificó contra la fuente del modelo antes de integrar: el último
periodo cargado en `Consolidado2025` es `AÑO = 2026`, `MES = 09.Septiembre`, con
2.605 registros. No se asumió ni se fijó un mes anterior.

> Nota detectada, fuera de alcance: las páginas `Demográfico` y
> `Demográfico (Promedio)` conservan `07.Julio` en su slicer de Mes. No se
> modificaron porque pertenecen a otra página y a otro alcance.

### 4.2 Ocultamiento de `Retiros y Rotación Predictiva`

El navegador (`b838e768742356bba69e`) conserva `showPage: false` para la página
`b7f3a91c2d4e60582a1f`, `Retiros y Rotación Predictiva`.

Es una **decisión funcional del responsable**, no ruido: se solicitó
expresamente ocultar esa pestaña en el BI publicado. Con esta entrada, el
navegador oculta 17 páginas.

## 5. Validaciones ejecutadas

| Control | Resultado |
|---|---|
| JSON parseable | 21/21 |
| `git diff --check` | limpio |
| CRLF e indentación originales | preservados; diff línea por línea, sin re-serialización |
| `query`, campos, `queryRef`, `nativeQueryRef` | **0 cambios** |
| `filterConfig`, `drillFilterOtherVisuals`, `parentGroupName`, `columnProperties` | **0 cambios** |
| `page.json`, `pages.json`, `report.json` | sin cambios |
| Modelo semántico, Power Query, DAX, relaciones | **0 cambios** |
| Otras páginas | **0 archivos** |
| `Data/`, `Outputs/` | **0 archivos** |
| Tema global | sin cambios |
| Contraste de etiquetas | peor caso 4,86:1 (AA) |
| Suite de pruebas del repositorio | 91 PASS |

Los nodos añadidos tienen exclusivamente la forma
`{properties: {color}, selector}`, verificada uno por uno.

### Validación visual

**PASS del usuario** sobre la página proyectada en televisor, 2026-10-06. Este
es el criterio de aceptación de la iniciativa: «legibilidad ejecutiva en pantalla
grande».

No se generó captura automatizada: la sesión no dispone de MCP de inspección de
reporte, Desktop Bridge ni captura de página. La verificación de render se hizo
en Power BI Desktop por el usuario.

## 6. Limitaciones conocidas

- `Antigüedad por Empresa` conserva 1 par de tonos borderline (`#7EB3E8` vs
  `#B9C4CF`, 1,30:1 de luminancia pero 22° de diferencia de matiz). Siete
  categorías están en el límite recomendado para una paleta categórica.
- `Tools/governance/skills_lint.py` no pudo ejecutarse: falta el módulo `yaml`
  en el entorno. No se instaló nada.
- 3 pruebas de `Tests/test_rotacion_proyectada.py` fallan por archivos de `Data/`
  no versionados. Se confirmó que fallan igual en un checkout limpio sin estos
  cambios.

## 7. Antecedente

`PBIP-006` — creación de la página `Sociodemográfico por Empresa`, cerrada el
2026-08-31 con PASS funcional y visual para uso en monitor
(`Specs/0024_analisis_impacto_sociodemografico_por_empresa.md`). Esta iniciativa
**no lo reescribe ni lo invalida**: lo complementa con una calibración posterior
para pantallas grandes.
