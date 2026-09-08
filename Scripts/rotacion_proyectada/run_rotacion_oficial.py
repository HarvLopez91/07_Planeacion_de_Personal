"""Rotacion Proyectada oficial agosto-diciembre 2026 (PBIP-008, Compromiso 2).

Construye la version oficial con corte 2026-07-31 por componentes:

    Indice_Rotacion = ((Ingresos + Retiros) / 2) / Total-Sena

No se proyecta `Indice_Rotacion` directamente. Se proyecta cada componente con
el mismo protocolo de backtesting y se compone al final.

Reutiliza integramente `dataset`, `models` y `backtest`; la logica nueva vive en
`rotacion.py`. La metodologia de Retiros no se rehace: aqui se reproduce su
protocolo sobre datos truncados al corte y se verifica contra las decisiones
aprobadas.

Uso:
    python -m Scripts.rotacion_proyectada.run_rotacion_oficial [ULTIMO_PERIODO_REAL]
    python -m Scripts.rotacion_proyectada.run_rotacion_oficial 202607

El corte por defecto es 202607, obligatorio para el Compromiso 2. Se pasa como
parametro y no como constante, para que la llegada de un mes real posterior no
mueva el corte de una version ya publicada.

Salidas: `Outputs/PBIP-008_Rotacion_Oficial/` (ignorado por Git). No escribe en
`Data/**` ni toca `PptovsReal.xlsx`, que se abre solo para lectura.
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Scripts.rotacion_proyectada.contrato import (  # noqa: E402
    construir_contrato, escribir_csv, validar_contrato,
)
from Scripts.rotacion_proyectada.dataset import (  # noqa: E402
    build_real_layer, hash_fuente, load_planta_personal, run_quality_rules,
)
from Scripts.rotacion_proyectada.models import MODEL_FUNCS, POOLED_FUNCS  # noqa: E402
from Scripts.rotacion_proyectada.run_backtesting import run_analysis  # noqa: E402
from Scripts.rotacion_proyectada.rotacion import (  # noqa: E402
    FORECAST_PERIODOS, PERIODO_CORTE, build_ingresos_layer, componer_rotacion,
    control_identidad_planta, evaluar_componente, fecha_corte_de,
    periodos_siguientes, reglas_calidad_ingresos, truncar_al_corte,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
XLSX_PATH = os.path.join(REPO_ROOT, "Data", "HeadCount", "PptovsReal.xlsx")
OUTPUTS_DIR = os.path.join(REPO_ROOT, "Outputs", "PBIP-008_Rotacion_Oficial")

# Decisiones de Retiros ya aprobadas (Specs/0028, Fase 2). Se usan como control
# de reproducibilidad: si el pipeline truncado al corte no las reproduce, hay
# una deriva que debe investigarse antes de publicar.
RETIROS_APROBADOS = {
    "Challenger": ("M3_Tendencia", "FORECAST"),
    "Grupo Sky": ("B3_TasaAgrupada24M", "FORECAST"),
    "Habitel Hotels": ("M0_Naive", "BASELINE"),
    "Lemco": ("B3_TasaAgrupada24M", "REFERENCIA_DESCRIPTIVA"),
    "Fundación Challenger": ("SIN_FORECAST", "SIN_FORECAST"),
}


def real_posterior_al_corte(raw: pd.DataFrame, periodo: int) -> pd.DataFrame:
    """Dato real de un periodo posterior al corte, para Real vs Proyectado.

    Nunca alimenta el entrenamiento: se lee de la misma hoja pero por fuera del
    universo truncado que consumen los modelos.
    """
    real = raw.loc[raw["Ppto/Real"].eq("Real")].copy()
    anio_col = real.columns[1]
    real["periodo"] = (pd.to_numeric(real[anio_col], errors="coerce") * 100
                       + pd.to_numeric(real["Mes Num"], errors="coerce"))
    sub = real.loc[real["periodo"].eq(periodo)]
    agg = (sub.groupby("Grupo Empresa", as_index=False, dropna=False)
              .agg(ingresos_real=("Ingresos", "sum"), retiros_real=("Retiros", "sum"),
                   total_sena_real=("Total-Sena", "sum")))
    agg = agg.rename(columns={"Grupo Empresa": "grupo_empresa"})
    agg = agg.loc[agg["total_sena_real"].gt(0)].copy()
    agg["indice_rotacion_real"] = (
        (agg["ingresos_real"] + agg["retiros_real"]) / 2) / agg["total_sena_real"]
    return agg


def comparar_agosto(forecast: pd.DataFrame, real: pd.DataFrame,
                    periodo: int) -> pd.DataFrame:
    """Real vs Proyectado del primer mes posterior al corte, conservando el
    forecast original.

    El forecast NO se sustituye por el real: ambos coexisten, que es la unica
    forma de medir el error de esta version. El real de ese mes se lee fuera del
    universo truncado, de modo que nunca alimenta seleccion ni entrenamiento.
    """
    fc = forecast.loc[forecast["periodo"].eq(int(periodo))].copy()
    comp = fc.merge(real, on="grupo_empresa", how="left")
    comp["dif_ingresos"] = comp["ingresos_proyectados"] - comp["ingresos_real"]
    comp["dif_retiros"] = comp["retiros_proyectados"] - comp["retiros_real"]
    comp["dif_rotacion_pp"] = (
        comp["indice_rotacion_proyectado"] - comp["indice_rotacion_real"]) * 100
    comp["error_abs_rotacion_pp"] = comp["dif_rotacion_pp"].abs()
    # El error porcentual solo procede con real estrictamente positivo; con
    # denominador cero o nulo se deja vacio en vez de publicar un infinito.
    comp["error_pct_rotacion"] = np.where(
        comp["indice_rotacion_real"].gt(0),
        comp["error_abs_rotacion_pp"] / (comp["indice_rotacion_real"] * 100) * 100,
        np.nan)
    comp["dentro_banda_80"] = np.where(
        comp["li_80_aproximado"].notna(),
        comp["indice_rotacion_real"].between(
            comp["li_80_aproximado"], comp["ls_80_aproximado"]),
        None)
    cols = ["grupo_empresa", "clasificacion", "modelo_ingresos", "modelo_retiros",
            "total_sena_usado", "total_sena_real",
            "ingresos_proyectados", "ingresos_real", "dif_ingresos",
            "retiros_proyectados", "retiros_real", "dif_retiros",
            "indice_rotacion_proyectado", "indice_rotacion_real",
            "dif_rotacion_pp", "error_abs_rotacion_pp", "error_pct_rotacion",
            "li_80_aproximado", "ls_80_aproximado", "dentro_banda_80"]
    return comp[cols]


def run(xlsx_path: str = XLSX_PATH, write_outputs: bool = True,
        ultimo_periodo_real_esperado: int = PERIODO_CORTE) -> dict:
    """Ejecuta la Rotacion Oficial con un corte explicito.

    El Compromiso 2 usa obligatoriamente 202607 (corte 31/07/2026, horizonte
    agosto-diciembre 2026). El corte es un parametro de la corrida y no una
    constante del codigo: la llegada de un mes real posterior no puede moverlo.
    """
    corte = int(ultimo_periodo_real_esperado)
    horizonte = periodos_siguientes(corte)
    fecha_corte = fecha_corte_de(corte)
    primer_real_posterior = horizonte[0]
    if corte == PERIODO_CORTE:
        # Guarda del Compromiso 2: el horizonte oficial es agosto-diciembre 2026.
        assert horizonte == FORECAST_PERIODOS, horizonte

    version = "rotacion_oficial_%s_%d" % (hash_fuente(xlsx_path), corte)
    raw_completo = load_planta_personal(xlsx_path)
    raw = truncar_al_corte(raw_completo, corte)

    # --- Retiros: pipeline aprobado, sobre el universo truncado al corte ------
    real_ret = build_real_layer(raw, version_dataset=version)
    apto_ret, calidad_ret, _ = run_quality_rules(real_ret, raw, corte)
    calidad_ret_df = pd.DataFrame([{
        "regla": q.rule, "descripcion": q.description, "estado": q.status,
        "detalle": q.detail, "grupos_afectados": ", ".join(q.affected_groups),
    } for q in calidad_ret])

    # --- Ingresos: capa nueva, mismo grano y mismo denominador ---------------
    ing = build_ingresos_layer(raw, corte)
    calidad_ing_df = reglas_calidad_ingresos(ing, corte)

    grupos = sorted(set(apto_ret["grupo_empresa"].dropna()) & set(ing["grupo_empresa"].dropna()))

    resumen, metricas, backtests, forecasts = [], [], [], []
    for grupo in grupos:
        sub_ret = apto_ret.loc[apto_ret["grupo_empresa"].eq(grupo)]
        sub_ing = ing.loc[ing["grupo_empresa"].eq(grupo)]

        res_ret = evaluar_componente(sub_ret, "tasa_mensual_retiros", "retiros",
                                     MODEL_FUNCS, POOLED_FUNCS)
        res_ing = evaluar_componente(sub_ing, "tasa_mensual_ingresos", "ingresos",
                                     MODEL_FUNCS, POOLED_FUNCS)

        # Denominador congelado: ultimo Total-Sena observado AL CORTE, arrastrado.
        sena_congelado = float(
            sub_ret.loc[sub_ret["periodo"].eq(corte), "total_sena"].iloc[0])
        forecasts.append(componer_rotacion(
            res_ing, res_ret, sena_congelado, grupo, version, horizonte, fecha_corte))

        aprobado = RETIROS_APROBADOS.get(grupo)
        for componente, res in (("INGRESOS", res_ing), ("RETIROS", res_ret)):
            m = res["metricas_full"].copy()
            m["grupo_empresa"], m["componente"] = grupo, componente
            metricas.append(m)
            b = res["backtest_full"].copy()
            b["grupo_empresa"], b["componente"] = grupo, componente
            backtests.append(b)
            resumen.append({
                "grupo_empresa": grupo, "componente": componente,
                "n_meses": res["perfil"]["n_meses"],
                "planta_promedio": res["perfil"]["planta_promedio"],
                "planta_ultima": res["perfil"]["planta_ultima"],
                "eventos_totales": res["perfil"]["retiros_totales"],
                "pct_meses_cero": res["perfil"]["pct_meses_cero"],
                "n_origenes_seleccion": res["n_origenes_seleccion"],
                "n_origenes_backtest": res["n_origenes_full"],
                "modelo_seleccionado": res["modelo_seleccionado"],
                "motivo_seleccion": res["motivo_seleccion"],
                "mae_seleccion": res["mae_seleccion"],
                "rmse_seleccion": res["rmse_seleccion"],
                "mase_seleccion": res["mase_seleccion"],
                "periodo_holdout": "%d-%d" % (res["periodo_inicio_holdout"],
                                              res["periodo_fin_holdout"]),
                "mae_holdout": res["mae_holdout"],
                "mae_naive_holdout": res["mae_naive_holdout"],
                "supera_naive_5pct": res["supera_naive_5pct"],
                "modelo_fallback_productivo": res["modelo_fallback_productivo"],
                "mae_fallback_holdout": res["mae_fallback_holdout"],
                "modelos_excluidos_forecast_negativo":
                    res["modelos_excluidos_forecast_negativo"],
                "modelo_final": res["modelo_final"],
                "clasificacion": res["clasificacion"],
                "nivel_fiabilidad": res["nivel_fiabilidad"],
                "motivo_fiabilidad": res["motivo_fiabilidad"],
                "decision": res["decision"],
                "reproduce_decision_aprobada": (
                    None if componente == "INGRESOS" or aprobado is None
                    else (res["modelo_final"], res["clasificacion"]) == aprobado),
                "decision_aprobada_historica": (
                    "" if componente == "INGRESOS" or aprobado is None
                    else "%s / %s" % aprobado),
            })

    forecast_df = pd.concat(forecasts, ignore_index=True)
    # Se lee del marco COMPLETO, no del truncado: agosto real solo se usa para
    # evaluar fuera de muestra, nunca para seleccionar ni entrenar.
    real_ago = real_posterior_al_corte(raw_completo, primer_real_posterior)
    comparacion = comparar_agosto(forecast_df, real_ago, primer_real_posterior)
    identidad = control_identidad_planta(ing, apto_ret)

    resultado = {
        "version_dataset": version, "corte": corte, "fecha_corte": fecha_corte,
        "horizonte": horizonte,
        "ingresos_real": ing,
        "retiros_real": apto_ret,
        "calidad_retiros": calidad_ret_df,
        "calidad_ingresos": calidad_ing_df,
        "resumen_modelos": pd.DataFrame(resumen),
        "metricas": pd.concat(metricas, ignore_index=True),
        "backtest": pd.concat(backtests, ignore_index=True),
        "forecast": forecast_df,
        "comparacion_agosto": comparacion,
        "control_identidad_planta": identidad,
    }
    if write_outputs:
        os.makedirs(OUTPUTS_DIR, exist_ok=True)
        for clave, nombre in {
            "ingresos_real": "ingresos_historico.csv",
            "calidad_retiros": "calidad_retiros.csv",
            "calidad_ingresos": "calidad_ingresos.csv",
            "resumen_modelos": "modelos_por_grupo.csv",
            "metricas": "backtesting_metricas.csv",
            "backtest": "backtesting_detalle.csv",
            "forecast": "rotacion_proyectada_ago_dic_2026.csv",
            "comparacion_agosto": "agosto_real_vs_proyectado.csv",
            "control_identidad_planta": "control_identidad_planta.csv",
        }.items():
            resultado[clave].to_csv(os.path.join(OUTPUTS_DIR, nombre),
                                    index=False, encoding="utf-8")
    return resultado


def construir_csv_contrato(xlsx_path: str = XLSX_PATH,
                           ultimo_periodo_real_esperado: int = PERIODO_CORTE,
                           escribir: bool = True) -> tuple[pd.DataFrame, dict, str]:
    """Genera el CSV candidato con el contrato RETIROS + ROTACION.

    Las filas de RETIROS se toman de `run_backtesting.run_analysis`, es decir del
    pipeline ya aprobado, en lugar de volver a derivarlas aqui: asi la ampliacion
    del contrato no puede mover los numeros publicados de Retiros.

    `write_outputs=False` en ambas corridas: no se toca `Data/**` ni las salidas
    aprobadas de la corrida anterior.
    """
    corte = int(ultimo_periodo_real_esperado)
    res_rot = run(xlsx_path, write_outputs=False, ultimo_periodo_real_esperado=corte)
    res_ret = run_analysis(xlsx_path, write_outputs=False,
                           ultimo_periodo_real_esperado=corte)
    df = construir_contrato(res_ret, res_rot)
    checks = validar_contrato(df, corte, res_rot["fecha_corte"], res_rot["horizonte"])
    ruta = os.path.join(OUTPUTS_DIR, "PBIP-008_Rotacion_Proyectada.csv")
    if escribir:
        escribir_csv(df, ruta)
    return df, {"checks": checks, "rotacion": res_rot, "retiros": res_ret}, ruta


def main() -> None:
    corte = int(sys.argv[1]) if len(sys.argv) > 1 else PERIODO_CORTE
    r = run(ultimo_periodo_real_esperado=corte)
    print("OK", r["version_dataset"])
    print("ultimo periodo real esperado:", r["corte"], "| corte:", r["fecha_corte"])
    print("horizonte proyectado:", r["horizonte"])
    print("salidas:", OUTPUTS_DIR)


if __name__ == "__main__":
    main()
