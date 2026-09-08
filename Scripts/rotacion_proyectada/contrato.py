# -*- coding: utf-8 -*-
"""Contrato publicable de `Rotacion Proyectada`: RETIROS + ROTACION (PBIP-008).

Evoluciona el dataset existente en vez de crear una segunda tabla predictiva.
La tabla pasa a contener dos indicadores y la columna `Indicador` es la que los
separa; el nombre de la tabla ya no significa "retiros".

Contrato (17 columnas). Las 13 primeras conservan nombre, orden y semantica del
contrato legado, de modo que el prefijo siga siendo comparable columna a columna;
las 4 nuevas se agregan al final:

    Periodo, Grupo Empresa, Valor, TipoRegistro, Clasificacion, Modelo,
    FechaCorte, BandaInferior, BandaSuperior, Retiros, Total-Sena,
    CoberturaHistorica, VersionDataset,
    Indicador, Ingresos, ModeloIngresos, ModeloRetiros

Semantica por indicador:

- ``Indicador = "RETIROS"``  -> `Valor` es `Tasa_Mensual_Retiros`. Filas
  identicas en metodologia y numero a las ya aprobadas; provienen del pipeline
  `run_backtesting.run_analysis`, no de una segunda derivacion.
- ``Indicador = "ROTACION"`` -> `Valor` es `Indice_Rotacion`, calculado como
  ``((Ingresos + Retiros) / 2) / Total-Sena``. `Modelo` documenta que es una
  composicion y `ModeloIngresos`/`ModeloRetiros` exhiben los dos metodos, para
  que la composicion no oculte de que depende cada componente.

`TipoRegistro` conserva REAL, FORECAST, BASELINE, REFERENCIA_DESCRIPTIVA y
SIN_FORECAST, y agrega ``REAL_VALIDACION`` para los meses reales posteriores al
corte. Esas filas NO entrenaron nada y NO sustituyen la proyeccion del mismo mes:
existen para que Real y Proyectado convivan y el error sea medible.

No escribe en `Data/**` ni en SharePoint: produce un candidato en `Outputs/`.
"""

from __future__ import annotations

import io
import os

import numpy as np
import pandas as pd

from .rotacion import periodos_siguientes

# Version del contrato. Se incorpora a VersionDataset para que una carga pueda
# distinguir el contrato ampliado del legado sin inspeccionar columnas.
CONTRATO_VERSION = 2

COLUMNAS_LEGADO = [
    "Periodo", "Grupo Empresa", "Valor", "TipoRegistro", "Clasificacion", "Modelo",
    "FechaCorte", "BandaInferior", "BandaSuperior", "Retiros", "Total-Sena",
    "CoberturaHistorica", "VersionDataset",
]
COLUMNAS_NUEVAS = ["Indicador", "Ingresos", "ModeloIngresos", "ModeloRetiros"]
COLUMNAS = COLUMNAS_LEGADO + COLUMNAS_NUEVAS

INDICADORES = ("RETIROS", "ROTACION")
TIPOS_FUTUROS = ("FORECAST", "BASELINE", "REFERENCIA_DESCRIPTIVA", "SIN_FORECAST")
TIPO_VALIDACION = "REAL_VALIDACION"
MODELO_COMPOSICION = "Composicion por componentes"


def _fmt(valor) -> str:
    """Serializa un numero sin inventar precision ni perderla.

    Los conteos reales se escriben como enteros —para que el prefijo legado del
    CSV siga siendo identico— y las componentes proyectadas, que son
    fraccionarias por construccion, conservan toda su precision. Nunca se
    redondea antes de calcular `Indice_Rotacion`.
    """
    if valor is None:
        return ""
    if isinstance(valor, str):
        return valor
    try:
        f = float(valor)
    except (TypeError, ValueError):
        return str(valor)
    if not np.isfinite(f):
        return ""
    if f == int(f) and abs(f) < 1e15:
        return str(int(f))
    return repr(f)


def _fila(periodo, grupo, indicador, valor, tipo, clasificacion, modelo, fecha_corte,
          li, ls, ingresos, retiros, sena, cobertura, modelo_ing, modelo_ret, version):
    return {
        "Periodo": _fmt(periodo), "Grupo Empresa": grupo, "Valor": _fmt(valor),
        "TipoRegistro": tipo, "Clasificacion": clasificacion, "Modelo": modelo or "",
        "FechaCorte": fecha_corte, "BandaInferior": _fmt(li), "BandaSuperior": _fmt(ls),
        "Retiros": _fmt(retiros), "Total-Sena": _fmt(sena),
        "CoberturaHistorica": _fmt(cobertura), "VersionDataset": version,
        "Indicador": indicador, "Ingresos": _fmt(ingresos),
        "ModeloIngresos": modelo_ing or "", "ModeloRetiros": modelo_ret or "",
    }


def construir_contrato(res_retiros: dict, res_rotacion: dict) -> pd.DataFrame:
    """Arma el contrato completo a partir de las dos corridas oficiales.

    `res_retiros` es la salida de `run_backtesting.run_analysis` y `res_rotacion`
    la de `run_rotacion_oficial.run`. Las filas de RETIROS se copian de la
    primera sin recalcular: es lo que garantiza que los numeros aprobados no
    puedan derivar al ampliar el contrato.
    """
    corte = int(res_rotacion["corte"])
    fecha_corte = res_rotacion["fecha_corte"]
    version = "%s_contrato%d" % (res_rotacion["version_dataset"], CONTRATO_VERSION)
    horizonte = list(res_rotacion["horizonte"])
    periodo_validacion = horizonte[0]

    ret_real = res_rotacion["retiros_real"]
    ing_real = res_rotacion["ingresos_real"]
    filas = []

    # ---------- RETIROS ----------
    for _, r in ret_real.sort_values(["grupo_empresa", "periodo"]).iterrows():
        filas.append(_fila(
            r["periodo"], r["grupo_empresa"], "RETIROS", r["tasa_mensual_retiros"],
            "REAL", "REAL", None, fecha_corte, None, None,
            None, r["retiros"], r["total_sena"], None, None, None, version))

    fc_ret = res_retiros["forecast"]
    for _, r in fc_ret.sort_values(["grupo_empresa", "periodo"]).iterrows():
        # `SIN_FORECAST` es un estado, no un metodo: el contrato legado deja
        # `Modelo` vacio en esas filas y esa normalizacion se preserva.
        modelo = "" if r["tipo_registro"] == "SIN_FORECAST" else r["modelo"]
        filas.append(_fila(
            r["periodo"], r["grupo_empresa"], "RETIROS", r["tasa_mensual_retiros"],
            r["tipo_registro"], r["tipo_registro"], modelo, fecha_corte,
            r["li_80_aproximado"], r["ls_80_aproximado"], None, None, None,
            r["cobertura_historica_observada"], None, modelo, version))

    # ---------- ROTACION ----------
    real = ing_real.merge(
        ret_real[["periodo", "grupo_empresa", "retiros"]],
        on=["periodo", "grupo_empresa"], how="inner")
    real["indice"] = ((real["ingresos"] + real["retiros"]) / 2) / real["total_sena"]
    for _, r in real.sort_values(["grupo_empresa", "periodo"]).iterrows():
        filas.append(_fila(
            r["periodo"], r["grupo_empresa"], "ROTACION", r["indice"],
            "REAL", "REAL", None, fecha_corte, None, None,
            r["ingresos"], r["retiros"], r["total_sena"], None, None, None, version))

    fc_rot = res_rotacion["forecast"]
    for _, r in fc_rot.sort_values(["grupo_empresa", "periodo"]).iterrows():
        sin_forecast = r["clasificacion"] == "SIN_FORECAST"
        filas.append(_fila(
            r["periodo"], r["grupo_empresa"], "ROTACION",
            r["indice_rotacion_proyectado"], r["clasificacion"], r["clasificacion"],
            "" if sin_forecast else MODELO_COMPOSICION, fecha_corte,
            r["li_80_aproximado"], r["ls_80_aproximado"],
            r["ingresos_proyectados"], r["retiros_proyectados"],
            None if sin_forecast else r["total_sena_usado"],
            # Cobertura historica: el runner mide cobertura por componente, no de
            # la banda compuesta. No se publica una cifra que no se midio.
            None,
            None if sin_forecast else r["modelo_ingresos"],
            None if sin_forecast else r["modelo_retiros"], version))

    # ---------- REAL_VALIDACION (mes real posterior al corte) ----------
    val = res_rotacion["comparacion_agosto"]
    for _, r in val.sort_values("grupo_empresa").iterrows():
        if not np.isfinite(r.get("total_sena_real", np.nan)):
            continue
        tasa_ret = r["retiros_real"] / r["total_sena_real"] if r["total_sena_real"] else np.nan
        filas.append(_fila(
            periodo_validacion, r["grupo_empresa"], "RETIROS", tasa_ret,
            TIPO_VALIDACION, TIPO_VALIDACION, None, fecha_corte, None, None,
            None, r["retiros_real"], r["total_sena_real"], None, None, None, version))
        filas.append(_fila(
            periodo_validacion, r["grupo_empresa"], "ROTACION",
            r["indice_rotacion_real"], TIPO_VALIDACION, TIPO_VALIDACION, None,
            fecha_corte, None, None, r["ingresos_real"], r["retiros_real"],
            r["total_sena_real"], None, None, None, version))

    df = pd.DataFrame(filas, columns=COLUMNAS)
    df["_p"] = df["Periodo"].astype(int)
    df = (df.sort_values(["Indicador", "Grupo Empresa", "_p", "TipoRegistro"])
            .drop(columns="_p").reset_index(drop=True))
    return df


def escribir_csv(df: pd.DataFrame, ruta: str) -> str:
    """Escribe el candidato con la misma convencion del archivo oficial vigente.

    UTF-8 con BOM y saltos CRLF, porque asi esta hoy el CSV que consume Power
    Query desde SharePoint; cambiar la codificacion seria un cambio de contrato
    encubierto.
    """
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    contenido = df.to_csv(index=False, lineterminator="\r\n")
    io.open(ruta, "w", encoding="utf-8-sig", newline="").write(contenido)
    return ruta


def validar_contrato(df: pd.DataFrame, corte: int, fecha_corte: str,
                     horizonte: list[int]) -> list[tuple[str, bool, str]]:
    """Controles del contrato publicable. Devuelve (nombre, ok, detalle)."""
    out = []

    def chk(nombre, ok, detalle=""):
        out.append((nombre, bool(ok), detalle))

    ind = set(df["Indicador"])
    chk("Indicador solo contiene RETIROS/ROTACION", ind == set(INDICADORES),
        ", ".join(sorted(ind)))

    p = df["Periodo"].astype(int)
    entren = df.loc[df["TipoRegistro"].eq("REAL"), "Periodo"].astype(int)
    chk("El maximo periodo REAL es el corte", int(entren.max()) == corte,
        "maximo REAL %d, corte %d" % (int(entren.max()), corte))
    chk("FechaCorte unica y derivada del corte",
        set(df["FechaCorte"]) == {fecha_corte}, fecha_corte)

    fut = sorted(set(p[df["TipoRegistro"].isin(TIPOS_FUTUROS)]))
    chk("Horizonte proyectado exacto", fut == sorted(horizonte), str(fut))
    chk("Sin enero 2027", 202701 not in set(p), "")

    val = df.loc[df["TipoRegistro"].eq(TIPO_VALIDACION)]
    chk("REAL_VALIDACION solo en el primer mes posterior al corte",
        set(val["Periodo"].astype(int)) in ({horizonte[0]}, set()),
        "%d filas" % len(val))
    chk("REAL_VALIDACION no se mezcla con REAL",
        not val.empty and int(val["Periodo"].iloc[0]) > corte,
        "el mes de validacion es posterior al corte")

    # Unicidad del nuevo grano. Retiros y Rotacion comparten Periodo x Grupo, de
    # modo que sin Indicador la clave colisionaria.
    clave = ["Periodo", "Grupo Empresa", "Indicador", "TipoRegistro"]
    dup = df.duplicated(subset=clave).sum()
    chk("Sin duplicados en Periodo+Grupo+Indicador+TipoRegistro", dup == 0,
        "%d duplicados" % dup)
    dup_sin_ind = df.duplicated(subset=["Periodo", "Grupo Empresa", "TipoRegistro"]).sum()
    chk("La colision sin Indicador es real (justifica la columna)", dup_sin_ind > 0,
        "%d filas colisionarian sin Indicador" % dup_sin_ind)

    rot = df.loc[df["Indicador"].eq("ROTACION") & df["TipoRegistro"].isin(TIPOS_FUTUROS)]
    con_valor = rot.loc[rot["Valor"].ne("")]
    err = 0.0
    for _, r in con_valor.iterrows():
        i, x, s = float(r["Ingresos"]), float(r["Retiros"]), float(r["Total-Sena"])
        err = max(err, abs(((i + x) / 2) / s - float(r["Valor"])))
    chk("ROTACION cumple ((Ingresos+Retiros)/2)/Total-Sena", err < 1e-12,
        "error maximo %.3e" % err)

    sena_fut = rot.loc[rot["Total-Sena"].ne(""), ["Grupo Empresa", "Total-Sena"]]
    variables = sena_fut.groupby("Grupo Empresa")["Total-Sena"].nunique()
    chk("Total-Sena no se proyecta (constante en el horizonte)",
        bool((variables == 1).all()), "grupos con denominador variable: %d"
        % int((variables > 1).sum()))

    chk("Sin PII: solo columnas agregadas",
        list(df.columns) == COLUMNAS, ", ".join(df.columns))
    return out
