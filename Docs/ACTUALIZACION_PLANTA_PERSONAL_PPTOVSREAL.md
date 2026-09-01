# Actualización de Planta Personal en PptovsReal

## Propósito

Este procedimiento actualiza el corte mensual de gasto laboral y ventas en
`PptovsReal.xlsx`, hoja `Planta Personal`, a partir del archivo operativo
`Gasto Laboral 2026.xlsx`. No modifica Power BI, Power Query, DAX ni el modelo
semántico.

Los Excel contienen información sensible y permanecen en `Data/`, fuera de
Git. Solo se versionan este procedimiento y la herramienta de apoyo.

## Archivos

Fuente mensual:

```text
Data/Gasto Laboral/<AÑO>/<NN_MES>/Gasto Laboral 2026.xlsx
```

Destino:

```text
Data/HeadCount/PptovsReal.xlsx
```

Hoja destino:

```text
Planta Personal
```

## Prerrequisitos

1. Confirmar el año y mes desde los encabezados y valores del archivo fuente;
   la carpeta no basta como evidencia.
2. Cerrar `PptovsReal.xlsx` y comprobar que permite acceso exclusivo.
3. Calcular SHA-256 de fuente y destino.
4. Crear y abrir un backup verificable en `Data/HeadCount/Backups/`.
5. Confirmar que la fila del periodo ya existe y que la llave es única.
6. No ejecutar la actualización si cambiaron hojas, encabezados, empresas o
   reglas de escala.
7. La automatización está validada exclusivamente para la estructura 2026. Si
   se procesa otro año, primero debe comprobarse el nombre y la estructura real
   de las hojas fuente; no se debe inferir una convención anual.

## Estructura fuente

### Gasto Laboral Ppto 2026

- Fila 3: encabezados mensuales.
- Bloque izquierdo: presupuesto de gasto.
- Bloque derecho: ejecución de gasto.
- Filas 4 a 12: empresas consideradas por el procedimiento.
- El bloque `HeadCount` de la misma hoja no alimenta las columnas de planta del
  destino y no debe copiarse.

### Gastos Operacio-Ventas

- Fila 3: encabezados mensuales.
- Bloque izquierdo: presupuesto de ventas o gasto operacional.
- Bloque derecho: ejecución.
- Filas 4 a 11: empresas con información de ventas.

Las columnas mensuales deben localizarse por encabezado, no por letra fija.

## Estructura destino y contrato con Power BI

`Planta Personal` conserva una fila por la llave:

```text
Ppto/Real + Año + Mes Num + Grupo Empresa + Empresa
```

La consulta `Planta Ppto` promueve la primera fila como encabezados y espera,
entre otras, estas columnas:

- `Ventas (MM)` como moneda;
- `Gasto Personal` como moneda;
- `Ppto Ventas (MM)` como moneda;
- `Ppto Gasto Personal` como moneda.

No deben renombrarse columnas, agregarse encabezados ni alterarse las hojas
`INGRESOS`, `Tbl_Ingresos`, `RETIROS` o `Tbl_Retiros`.

## Matriz de mapeo

| Columna destino | Hoja fuente | Bloque | Transformación | Regla |
|---|---|---|---|---|
| `Gasto Personal` | `Gasto Laboral Ppto 2026` | Ejecución | Copia directa, excepto Challenger | Solo valores no nulos del mes |
| `Ventas (MM)` | `Gastos Operacio-Ventas` | Ejecución | Copia directa, excepto Challenger | Solo empresas presentes en el bloque |
| `Ppto Ventas (MM)` | `Gastos Operacio-Ventas` | Presupuesto | Copia directa, excepto Challenger | No sobrescribir un valor diferente sin revisión |
| `Ppto Gasto Personal` | `Gasto Laboral Ppto 2026` | Presupuesto | Validación, sin escritura en el corte de julio | Julio ya estaba cargado en el destino |

La fuente expresa las cifras de Challenger en millones para gasto y ventas,
mientras el destino las almacena en unidades monetarias. Para esa empresa se
aplica el factor `1.000.000`. Las demás empresas se copian sin escala.

### Homologación de empresas

| Empresa fuente | Grupo Empresa destino | Empresa destino |
|---|---|---|
| Lemco | Lemco | Lemco |
| Habitel | Habitel Hotels | Habitel Nómina Compartida |
| Lemco Salvio | Habitel Hotels | Lemco Salvio |
| Operadora | Habitel Hotels | Operadora |
| Fundación | Fundación Challenger | Fundación Challenger |
| Challenger | Challenger | Challenger |
| Sky Logistica | Grupo Sky | Sky Logística Integral |
| Sky Industrial | Grupo Sky | Sky Industrial |
| Sky Forwarder | Grupo Sky | Sky Forwarder |

`Habitel Prime`, `Habitel Select` y `Lemco Inmobiliaria` no tienen fila fuente
equivalente en estos bloques y se dejan intactas. Operadora no aparece en el
bloque de ventas y sus campos de ventas no se inventan.

## Estrategia de actualización

La estrategia demostrada es `UPDATE_COLUMNS`:

- las filas del mes ya existen;
- no se agregan ni eliminan filas;
- se actualizan exclusivamente las columnas mapeadas;
- los nulos de la fuente se conservan como nulos;
- una celda no vacía y diferente exige revisión antes de reemplazarla.

La herramienta [actualizar_planta_personal.ps1](../Scripts/actualizar_planta_personal.ps1)
implementa `-DryRun`, valida el esquema y la unicidad y escribe siempre sobre
un `OutputPath` nuevo. Nunca reconstruye el workbook con pandas. El script
rechaza defensivamente cualquier `-Year` distinto de `2026`, porque el nombre
`Gasto Laboral Ppto 2026` y su estructura son literales demostrados para ese
año, no una convención generalizable.

Ejemplo de análisis:

```powershell
./Scripts/actualizar_planta_personal.ps1 `
  -SourcePath '<ruta fuente>' `
  -TargetPath '<ruta PptovsReal.xlsx>' `
  -Year 2026 -Month 7 -ExpectedChanges 21 -DryRun
```

Ejemplo de generación de candidato:

```powershell
./Scripts/actualizar_planta_personal.ps1 `
  -SourcePath '<ruta fuente>' `
  -TargetPath '<ruta PptovsReal.xlsx>' `
  -OutputPath '<ruta temporal nueva>' `
  -Year 2026 -Month 7 -ExpectedChanges 21
```

Si el `-DryRun` detecta una celda no vacía y diferente, el script se detiene
por defecto. El reemplazo solo puede autorizarse después de:

1. ejecutar `-DryRun`;
2. revisar y aprobar cada diferencia reportada;
3. fijar `-ExpectedChanges` al conteo aprobado;
4. generar el candidato con `-AllowReplaceExisting`.

Ejemplo para diferencias existentes previamente validadas:

```powershell
./Scripts/actualizar_planta_personal.ps1 `
  -SourcePath '<ruta fuente>' `
  -TargetPath '<ruta PptovsReal.xlsx>' `
  -OutputPath '<ruta temporal nueva>' `
  -Year 2026 -Month 7 `
  -ExpectedChanges 21 `
  -AllowReplaceExisting
```

`-AllowReplaceExisting` no sustituye el dry-run ni la revisión: solamente
habilita la escritura de diferencias ya aprobadas. `-ExpectedChanges` sigue
siendo un control obligatorio recomendado para abortar si cambia el alcance.

## Procedimiento manual sin scripts

1. Crear y abrir el backup del destino.
2. Abrir la fuente y confirmar el mes en la fila 3 de ambas hojas fuente.
3. En `Planta Personal`, filtrar `Ppto/Real = Real`, año y número de mes.
4. Confirmar una sola fila por Grupo Empresa y Empresa.
5. Trasladar la ejecución de gasto a `Gasto Personal` usando la homologación.
6. Trasladar ejecución y presupuesto de ventas a `Ventas (MM)` y
   `Ppto Ventas (MM)`.
7. Aplicar `×1.000.000` solamente a Challenger.
8. No escribir sobre valores fuente vacíos ni sobre empresas sin equivalente.
9. No modificar `Ppto Gasto Personal` sin un análisis separado.
10. Guardar primero una copia candidata, cerrarla y volverla a abrir.
11. Conciliar celdas, filas, fórmulas, hojas, conexiones y pivots.
12. Reemplazar el destino solamente tras obtener PASS.

## Checklist QA

- [ ] ZIP/CRC válido y apertura correcta en Excel.
- [ ] Mismas cinco hojas, orden y visibilidad.
- [ ] `Planta Personal` conserva `A1:U1068` mientras no cambie su estructura.
- [ ] Cero filas agregadas o eliminadas.
- [ ] Llave del periodo sin duplicados.
- [ ] Coincidencia completa de valores fuente no nulos.
- [ ] Nulos de fuente preservados y explicados.
- [ ] `Ppto Gasto Personal` sin cambios cuando esté fuera del alcance.
- [ ] Conteo de fórmulas sin variación.
- [ ] Hojas no objetivo sin diferencias lógicas.
- [ ] Tablas, nombres definidos, conexiones y pivots preservados.
- [ ] Encabezados compatibles con `Planta Ppto`.

## Rollback

1. Cerrar Excel y Power BI Desktop.
2. Confirmar el SHA-256 del backup documentado.
3. Reemplazar `Data/HeadCount/PptovsReal.xlsx` por el backup verificado.
4. Abrir el archivo restaurado y repetir el checklist estructural.

## Errores frecuentes

- Copiar el bloque `HeadCount` como si fuera la planta mensual.
- Escalar todas las empresas como Challenger.
- Crear filas nuevas cuando el periodo ya existe.
- Sobrescribir nulos de fuente con estimaciones.
- Guardar el libro con una librería que elimine conexiones o pivots.
- Versionar `Data/**` mediante `git add -f`.

## Privacidad

No incluir nombres de colaboradores, identificaciones, correos ni muestras de
datos personales en Git, documentación o mensajes de commit. Los diagnósticos
detallados permanecen en ubicaciones ignoradas.

## Evidencia del corte julio de 2026

- Fuente SHA-256: `D6257709340B500FED1E45B4E401EABA13C2FB0008C7D0BC2C809BC7154F54CE`.
- Destino antes SHA-256: `7D999B333E928B39AE67C1451DC6C4F3A1274DF8775C59B177478BA37AC53FFF`.
- Destino después SHA-256: `5A358C3DD175A460A51C9BA35C679F7E5E77AD09F6283403B8DA1A6FB866B269`.
- Filas del periodo en destino: 12.
- Filas agregadas, eliminadas o reemplazadas: 0.
- Filas con al menos una celda modificada: 8.
- Celdas modificadas: 21.
- Coincidencias fuente/destino tras actualizar: 22.
- Nulos fuente preservados: 3, todos asociados a la ejecución/presupuesto de
  ventas de Challenger y su ejecución de gasto.
- Hojas no objetivo con diferencias lógicas: 0.
- Resultado: PASS.
