# Validación mensual de `INGRESOS` y `RETIROS`

> **Privacidad.** `PptovsReal.xlsx` y el consolidador Kactus contienen datos
> personales y permanecen en `Data/`, fuera de Git. El validador abre ambos
> libros en modo de solo lectura. Las identificaciones se comparan únicamente en
> memoria y nunca se muestran en consola ni en el reporte agregado.

## Objetivo

Validar cada ingesta mensual de las hojas `INGRESOS` y `RETIROS` de
`PptovsReal.xlsx` contra el consolidador oficial de Kactus antes de actualizar
Power BI. El componente comprueba volumen, identidad de los registros, fechas,
duplicados y homologación de Empresa/Grupo sin modificar ningún Excel.

## Ejecución

La invocación histórica continúa soportada:

```powershell
python Scripts/headcount/validar_ingresos_retiros.py 2026 08.Agosto
```

El mes acepta número, nombre o etiqueta `NN.Nombre`. Si se omiten año y mes, el
script descubre el último periodo que exista simultáneamente en `INGRESOS` y
`RETIROS`:

```powershell
python Scripts/headcount/validar_ingresos_retiros.py
```

Las rutas son configurables para una ingesta futura o un entorno aislado:

```powershell
python Scripts/headcount/validar_ingresos_retiros.py 2027 01.Enero `
  --pptovsreal C:\fuentes\PptovsReal.xlsx `
  --kactus C:\fuentes\CONSOLIDADOR_CONTRATOS.xlsx `
  --empresas-tmdl C:\modelo\Empresas.tmdl `
  --grupos-tmdl "C:\modelo\Grupo Empresarial.tmdl" `
  --output-dir C:\evidencia
```

`--no-report` ejecuta todas las comprobaciones sin escribir el reporte Markdown.
Es útil para automatización y pruebas de preingesta.

## Fuentes y estructura

| Rol | Valor predeterminado | Estructura utilizada |
|---|---|---|
| Destino operativo | `Data/HeadCount/PptovsReal.xlsx` | Hojas `INGRESOS` y `RETIROS`, encabezados en fila 1 |
| Origen oficial | `Data/Contratos_Kactus/Fuente_Oficial/CONSOLIDADOR_CONTRATOS_V0.0.0.xlsx` | Hojas mensuales Kactus, encabezados en fila 3 |
| Empresas | `PBIP/.../tables/Empresas.tmdl` | Catálogo embebido y regla Empresa → Grupo |
| Grupos | `PBIP/.../tables/Grupo Empresarial.tmdl` | Catálogo oficial embebido |

Las hojas Kactus se resuelven por mes y actividad, no mediante una lista anual
fija:

- `<mes>, A`: ingresos;
- `<mes> II` o `<mes>, I`: retiros.

## Contrato de entrada

### `PptovsReal.xlsx`

Columnas obligatorias para ambas hojas:

| Campo lógico | Encabezados admitidos | Uso |
|---|---|---|
| Año | `Año`, `Ano` | Selección del periodo |
| Mes | `Mes` | Selección del periodo |
| Grupo | `Grupo Empresarial`, `Grupo empresarial`, `Grupo Empresa` | Homologación/diagnóstico |
| Empresa | `Empresa` | Unión con el catálogo oficial |
| Identificador | `Identificacion`, `Identificación` | Conciliación privada en memoria |

Además:

- `INGRESOS` requiere `Fecha Inicio`;
- `RETIROS` requiere `Fecha Vencimiento`.

Se admiten fechas Excel, `AAAA-MM-DD`, `DD/MM/AAAA`, `DD-MM-AAAA` y
`AAAA/MM/DD`. Una fecha vacía, ilegible o perteneciente a otro periodo es una
inconsistencia bloqueante.

### Consolidador Kactus

Cada hoja mensual debe conservar tres filas iniciales: título, fila auxiliar y
encabezados. Son obligatorios:

- `Identificación`/`Identificacion`;
- `Fecha Inicio` o `Fecha Contrato` para ingresos;
- `Fecha Vencimiento` para retiros.

El prefijo `Fact_Contrataciones[...]` se acepta y se elimina al interpretar los
encabezados.

### Campos opcionales

Las demás columnas operativas pueden existir y se ignoran. El validador no
depende de cargo, centro de costo, tipo de contrato, motivo ni empresa concreta.

## Reglas

Para cada una de las dos poblaciones se valida:

1. existencia del periodo;
2. total PptovsReal frente al total Kactus;
3. identificadores presentes;
4. ausencia de duplicados dentro del periodo;
5. fechas válidas y coherentes con el periodo solicitado;
6. igualdad de identificadores como multiconjunto entre ambos libros;
7. Empresa presente en el catálogo oficial;
8. Grupo empresarial compatible con la Empresa.

La arquitectura de RETIROS usa efectivamente:

```text
Ppto Retiros[Empresa] → Empresas[Empresas] → Empresas[Grupo Empresa]
```

Por esa razón, una diferencia en la columna redundante
`Ppto Retiros[Grupo empresarial]` genera `WARN`, no `ERROR`, siempre que Empresa
sea válida y permita derivar el grupo oficial. En INGRESOS, la homologación
Grupo/Empresa continúa siendo una condición de paso.

Un grupo que aparece por primera vez frente al periodo anterior se reporta como
`INFO`; no falla automáticamente. Su validez se decide contra el catálogo
oficial y la conciliación con Kactus.

## Salida y códigos de retorno

| Código | Resultado | Significado |
|---:|---|---|
| `0` | `PASS` | No hay errores bloqueantes; puede haber `WARN` o `INFO` |
| `1` | `ERROR / DATOS` | Volumen, identidad, fecha, duplicado u homologación inconsistente |
| `2` | `ERROR / ESTRUCTURA` | Falta hoja/columna o el catálogo no cumple el contrato |
| `3` | `ERROR / TECNICO` | Archivo inexistente, bloqueado o no legible |

El reporte, salvo `--no-report`, se guarda en:

```text
Outputs/validacion_ingresos_retiros_AAAA-MM.md
```

Contiene únicamente estados, conteos y agregaciones por Empresa/Grupo. No
contiene números de documento, nombres de personas ni diferencias identificadas
fila a fila.

## Ejemplo ficticio

Con dos colaboradores sintéticos en ambos libros:

```text
[PASS][DATOS] INGRESOS: total concilia con Kactus — PptovsReal=2; Kactus=2
[PASS][DATOS] INGRESOS: registros concilian por identificacion — faltantes=0; adicionales=0
[PASS][DATOS] RETIROS: Grupo efectivo derivable por Empresa — sin grupo oficial=0

RESULTADO: PASS
```

Los valores ficticios utilizados en pruebas tienen prefijo `TEST-`; las pruebas
no leen ni versionan registros reales.

## Caso de regresión agosto de 2026

La versión estabilizada conserva las correcciones verificadas después de la
carga manual:

- concilia INGRESOS y RETIROS por identificación, no solo por conteo;
- valida Empresa contra el catálogo oficial;
- deriva el grupo efectivo de RETIROS desde Empresa;
- trata la discrepancia de su columna redundante como advertencia;
- trata grupos nuevos frente al mes anterior como diagnóstico, no como fallo;
- nunca publica las identificaciones comparadas.

El script no contiene los totales de agosto ni nombres de empresas codificados.
Los resultados dependen exclusivamente de las fuentes entregadas y del catálogo
vigente.

### Evidencia de cierre F1

Validación ejecutada el 11/09/2026 con las fuentes operativas en modo de solo
lectura:

- **15/15 pruebas específicas:** PASS con datos exclusivamente sintéticos;
- **ejecución real agosto de 2026:** PASS;
- **INGRESOS:** 146 registros, conciliación por identificación PASS y cero
  duplicados;
- **RETIROS:** 94 registros, conciliación por identificación PASS y cero
  duplicados;
- **72 discrepancias** de la columna redundante
  `Ppto Retiros[Grupo empresarial]`: `WARN` no bloqueante. La Empresa está
  homologada y el grupo efectivo se deriva correctamente desde la dimensión;
- **suite general:** 91 pruebas PASS y 3 errores preexistentes de PBIP-008. Los
  tres requieren `Data/HeadCount/PptovsReal.xlsx`, archivo ignorado que no existe
  en el worktree limpio, y no fueron causados por este validador;
- **sintaxis Python y `git diff --check`:** PASS.

Interpretación de estados:

- `PASS` confirma que una regla fue satisfecha;
- `WARN` registra una condición que requiere seguimiento, pero que no invalida
  la ingesta bajo la arquitectura vigente;
- `ERROR` identifica una condición bloqueante y determina un código de salida
  distinto de cero.

## Límites y operación segura

- El consolidador se sigue resolviendo por nombres mensuales de hoja. Si un mismo
  archivo incorporara dos años con hojas de igual nombre, el contrato deberá
  evolucionar antes de procesarlo; las fechas evitan aceptar silenciosamente un
  año incorrecto.
- El catálogo se lee de la implementación TMDL vigente. Si cambia su estructura
  interna, el validador falla cerrado con código `2`.
- No se automatiza la escritura de `PptovsReal.xlsx`: el libro contiene tablas
  dinámicas, cachés, conexiones y fórmulas que no deben reserializarse con
  `openpyxl`.
- Un `WARN` no equivale a aprobación del contenido redundante; indica que la
  segmentación efectiva del modelo sigue siendo segura.

## Pruebas

```powershell
python -m pytest Tests/test_validar_ingresos_retiros.py -v
python -m py_compile Scripts/headcount/validar_ingresos_retiros.py
```

Las pruebas cubren casos válidos, duplicados, identificaciones faltantes,
fechas inválidas, catálogos desconocidos, esquema incompleto, archivo vacío,
múltiples periodos, privacidad y una ingesta futura.

## Referencias

- `Docs/DATA_PIPELINE.md`, flujo de contratos Kactus.
- `Docs/ACTUALIZACION_PLANTA_PERSONAL_DOTACION.md`, cierre mensual de dotación.
- `Docs/METRICS_CATALOG.md`, definición de Ingresos y Retiros.
