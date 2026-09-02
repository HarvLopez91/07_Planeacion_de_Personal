"""Pipeline reproducible de ciencia de datos para PBIP-008.

Construye REAL, ejecuta controles independientes, selecciona modelos sin usar
los cinco meses finales, evalua una sola vez el holdout y produce el forecast
agosto-diciembre de 2026. No modifica PBIP ni fuentes operativas.
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Scripts.rotacion_proyectada.backtest import (
    compute_metrics, prediction_validity, rolling_origin_backtest, select_winner,
)
from Scripts.rotacion_proyectada.dataset import (
    build_real_layer, clasificar_fiabilidad, hash_fuente, load_planta_personal,
    perfil_grupo, run_quality_rules,
)
from Scripts.rotacion_proyectada.models import MODEL_FUNCS, POOLED_FUNCS

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
XLSX_PATH = os.path.join(REPO_ROOT, "Data", "HeadCount", "PptovsReal.xlsx")
DATA_OUT_DIR = os.path.join(REPO_ROOT, "Data", "HeadCount", "rotacion_proyectada")
OUTPUTS_DIR = os.path.join(REPO_ROOT, "Outputs", "PBIP-008_Rotacion_Proyectada")
HORIZON = 5
HOLDOUT = 5
FORECAST_PERIODOS = [202608, 202609, 202610, 202611, 202612]
Z_80 = 1.2816
BAND_LABEL = "Banda de incertidumbre aproximada (80 %)"


def _forecast(modelo: str, y: np.ndarray, retiros: np.ndarray, sena: np.ndarray) -> np.ndarray:
    if modelo in POOLED_FUNCS:
        return POOLED_FUNCS[modelo](retiros, sena, HORIZON)
    fc = MODEL_FUNCS[modelo](y, HORIZON)
    if fc is None:
        raise ValueError(f"{modelo} no puede ajustarse con {len(y)} observaciones")
    return np.asarray(fc, dtype=float)


def _metric_row(metrics: pd.DataFrame, model: str) -> pd.Series:
    return metrics.loc[
        metrics["modelo"].eq(model) & metrics["horizonte"].eq("promedio(1-5)")
    ].iloc[0]


def _reconcile_retiros(xlsx_path: str, real_layer: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Conciliacion agregada; nunca devuelve identificadores ni filas personales."""
    detail = pd.read_excel(xlsx_path, sheet_name="RETIROS")
    detail["periodo_control"] = (
        pd.to_numeric(detail.iloc[:, 11], errors="coerce") * 100
        + pd.to_numeric(detail.iloc[:, 12], errors="coerce")
    )
    text = (
        detail.iloc[:, 15].fillna("").astype(str) + " "
        + detail.iloc[:, 16].fillna("").astype(str) + " "
        + detail.iloc[:, 7].fillna("").astype(str)
    ).str.upper()
    flags = pd.DataFrame({
        "reingreso": text.str.contains(r"REINGRES", regex=True),
        "cesion": text.str.contains(r"CESI", regex=True),
        "aprendiz_practicante_sena": text.str.contains(r"SENA|APREND|PRACTIC", regex=True),
        "fallecimiento": text.str.contains(r"FALLEC", regex=True),
        "pension_jubilacion": text.str.contains(r"PENSI|JUBIL", regex=True),
        "anulacion_cancelacion": text.str.contains(r"ANUL|CANCEL", regex=True),
    })
    exclude_proxy = flags.any(axis=1)
    kept = detail.loc[~exclude_proxy].copy()
    detail_group = detail.groupby(["periodo_control", detail.iloc[:, 0]], dropna=False).size().rename("registros_retiros")
    kept_group = kept.groupby(["periodo_control", kept.iloc[:, 0]], dropna=False).size().rename("registros_depurados_proxy")
    detail_group.index = detail_group.index.set_names(["periodo", "grupo_empresa"])
    kept_group.index = kept_group.index.set_names(["periodo", "grupo_empresa"])
    source_group = (
        real_layer.loc[real_layer["periodo"].le(202607)]
        .set_index(["periodo", "grupo_empresa"])["retiros"].rename("retiros_planta_personal")
    )
    reconciliation = pd.concat([source_group, detail_group, kept_group], axis=1).fillna(0).reset_index()
    reconciliation["diferencia_bruta"] = reconciliation["registros_retiros"] - reconciliation["retiros_planta_personal"]
    reconciliation["diferencia_residual_proxy"] = reconciliation["registros_depurados_proxy"] - reconciliation["retiros_planta_personal"]
    overview = {
        "retiros_planta_personal": int(source_group.sum()),
        "registros_retiros": int(len(detail)),
        "diferencia": int(len(detail) - source_group.sum()),
        "combinaciones_con_diferencia": int(reconciliation["diferencia_bruta"].ne(0).sum()),
        "conteos_categorias": {k: int(v) for k, v in flags.sum().to_dict().items()},
        "registros_union_categorias": int(exclude_proxy.sum()),
        "duplicados_exactos": int(detail.duplicated().sum()),
        "combinaciones_residuales": int(reconciliation["diferencia_residual_proxy"].ne(0).sum()),
        "diferencia_residual_neta": int(reconciliation["diferencia_residual_proxy"].sum()),
        "diferencia_residual_absoluta": int(reconciliation["diferencia_residual_proxy"].abs().sum()),
    }
    return reconciliation, overview


def run_analysis(xlsx_path: str = XLSX_PATH, write_outputs: bool = True) -> dict:
    version = "rotacion_" + hash_fuente(xlsx_path)
    raw = load_planta_personal(xlsx_path)
    real = build_real_layer(raw, version_dataset=version)
    apto, quality, sparse_groups = run_quality_rules(real, raw)
    all_metrics, all_bt, all_validity = [], [], []
    winners, holdouts, forecasts = [], [], []

    for group in sorted(apto["grupo_empresa"].dropna().unique()):
        sub = apto.loc[apto["grupo_empresa"].eq(group)].sort_values("periodo")
        y = sub["tasa_mensual_retiros"].to_numpy(float)
        r = sub["retiros"].to_numpy(float)
        s = sub["total_sena"].to_numpy(float)
        periods = sub["periodo"].to_numpy(int)
        profile = perfil_grupo(sub)
        allow_mape = profile["pct_meses_cero"] == 0

        full_series = pd.Series(y, index=periods)
        full_bt = rolling_origin_backtest(full_series, r, s)
        full_metrics = compute_metrics(full_bt, allow_mape)
        full_validity = prediction_validity(full_bt)
        full_validity["grupo_empresa"] = group

        train_n = len(y) - HOLDOUT
        select_series = pd.Series(y[:train_n], index=periods[:train_n])
        select_bt = rolling_origin_backtest(select_series, r[:train_n], s[:train_n])
        select_metrics = compute_metrics(select_bt, allow_mape)
        selected = select_winner(select_metrics, select_bt)
        selected_model = selected["ganador"] or "M0_Naive"
        holdout_fc = _forecast(selected_model, y[:train_n], r[:train_n], s[:train_n])
        naive_fc = _forecast("M0_Naive", y[:train_n], r[:train_n], s[:train_n])
        actual = y[train_n:]
        mae_holdout = float(np.mean(np.abs(holdout_fc - actual)))
        rmse_holdout = float(np.sqrt(np.mean((holdout_fc - actual) ** 2)))
        mae_naive_holdout = float(np.mean(np.abs(naive_fc - actual)))
        rmse_naive_holdout = float(np.sqrt(np.mean((naive_fc - actual) ** 2)))
        material_improvement = mae_holdout < mae_naive_holdout * 0.95

        selected_metric = _metric_row(select_metrics, selected_model)
        level, level_reason = clasificar_fiabilidad(profile, float(selected_metric["MAE"]))
        excluded_productive = []
        fallback_model = None
        fallback_mae_holdout = fallback_rmse_holdout = np.nan
        if level == "C_SIN_FORECAST_CONFIABLE":
            final_model, record_type, decision = "SIN_FORECAST", "SIN_FORECAST", "No se publica por fiabilidad C"
        elif level == "B_REFERENCIA_DESCRIPTIVA":
            final_model, record_type, decision = "B3_TasaAgrupada24M", "REFERENCIA_DESCRIPTIVA", "Referencia descriptiva; el holdout no autoriza llamarla forecast"
        elif material_improvement:
            productive_selected = _forecast(selected_model, y, r, s)
            if (productive_selected < 0).any():
                # La seleccion pre-holdout se conserva como evidencia. Tras
                # reentrenar con 43 meses, una salida negativa invalida su uso
                # productivo; la alternativa se vuelve a elegir solo con las
                # metricas pre-holdout y se reporta tambien su holdout.
                excluded_productive.append(selected_model)
                reduced_bt = select_bt.loc[~select_bt["modelo"].isin(excluded_productive)].copy()
                reduced_metrics = select_metrics.loc[~select_metrics["modelo"].isin(excluded_productive)].copy()
                fallback = select_winner(reduced_metrics, reduced_bt)
                fallback_model = fallback["ganador"] or "M0_Naive"
                fallback_fc = _forecast(fallback_model, y[:train_n], r[:train_n], s[:train_n])
                fallback_mae_holdout = float(np.mean(np.abs(fallback_fc - actual)))
                fallback_rmse_holdout = float(np.sqrt(np.mean((fallback_fc - actual) ** 2)))
                fallback_valid = not (_forecast(fallback_model, y, r, s) < 0).any()
                fallback_improves = fallback_mae_holdout < mae_naive_holdout * 0.95
                if fallback_valid and fallback_improves:
                    final_model, record_type = fallback_model, "FORECAST"
                    decision = "Ganador pre-holdout paso el gate, pero su reentrenamiento fue negativo; fallback predefinido valido y supera naive"
                else:
                    final_model, record_type = "M0_Naive", "BASELINE"
                    decision = "Ganador productivo invalido y fallback sin mejora valida; baseline transparente"
            else:
                final_model, record_type, decision = selected_model, "FORECAST", "Ganador supera materialmente a naive en holdout"
        else:
            final_model, record_type, decision = "M0_Naive", "BASELINE", "Ganador no supera razonablemente a naive en holdout; baseline transparente"

        holdouts.append({
            "grupo_empresa": group,
            "periodo_inicio_holdout": int(periods[train_n]), "periodo_fin_holdout": int(periods[-1]),
            "modelo_seleccionado": selected_model,
            "mae_seleccion": float(selected_metric["MAE"]), "rmse_seleccion": float(selected_metric["RMSE"]),
            "mase_seleccion": float(selected_metric["MASE"]),
            "mae_holdout": mae_holdout, "rmse_holdout": rmse_holdout,
            "mae_naive_holdout": mae_naive_holdout, "rmse_naive_holdout": rmse_naive_holdout,
            "supera_naive_5pct": material_improvement, "modelo_final": final_model,
            "modelo_fallback_productivo": fallback_model,
            "mae_fallback_holdout": fallback_mae_holdout,
            "rmse_fallback_holdout": fallback_rmse_holdout,
            "decision_final": decision,
        })
        winners.append({
            "grupo_empresa": group, "modelo_seleccionado_pre_holdout": selected_model,
            "modelo_final": final_model, "tipo_registro_final": record_type,
            "nivel_fiabilidad": level, "motivo_fiabilidad": level_reason,
            "motivo_seleccion": selected["motivo"],
            "modelos_excluidos_prediccion_negativa": selected.get("modelos_excluidos_prediccion_negativa", ""),
            "modelos_excluidos_forecast_productivo_negativo": ", ".join(excluded_productive),
            **profile,
        })

        productive = np.full(HORIZON, np.nan) if final_model == "SIN_FORECAST" else _forecast(final_model, y, r, s)
        model_bt = full_bt.loc[full_bt["modelo"].eq(final_model)].copy()
        coverage_by_h, rmse_by_h = {}, {}
        if not model_bt.empty and record_type in ("FORECAST", "BASELINE"):
            for h, hdf in model_bt.groupby("horizonte"):
                rmse_h = float(np.sqrt(np.mean(hdf["error"] ** 2)))
                lower = np.maximum(0, hdf["forecast"] - Z_80 * rmse_h)
                upper = hdf["forecast"] + Z_80 * rmse_h
                rmse_by_h[int(h)] = rmse_h
                coverage_by_h[int(h)] = float(((hdf["real"] >= lower) & (hdf["real"] <= upper)).mean())
        for idx, period in enumerate(FORECAST_PERIODOS):
            point = float(productive[idx]) if np.isfinite(productive[idx]) else np.nan
            h = idx + 1
            if record_type in ("FORECAST", "BASELINE") and h in rmse_by_h:
                lower, upper = max(0.0, point - Z_80 * rmse_by_h[h]), point + Z_80 * rmse_by_h[h]
                band, coverage = BAND_LABEL, coverage_by_h[h]
            else:
                lower = upper = coverage = np.nan
                band = "NO_APLICA"
            forecasts.append({
                "grupo_empresa": group, "periodo": period, "horizonte": h,
                "tipo_registro": record_type, "modelo": final_model,
                "tasa_mensual_retiros": point, "li_80_aproximado": lower,
                "ls_80_aproximado": upper, "tipo_banda": band,
                "cobertura_historica_observada": coverage,
                "fecha_corte": "2026-07-31", "version_dataset": version,
            })
        full_metrics["grupo_empresa"] = group
        full_bt["grupo_empresa"] = group
        all_metrics.append(full_metrics)
        all_bt.append(full_bt)
        all_validity.append(full_validity)

    metrics_df = pd.concat(all_metrics, ignore_index=True)
    bt_df = pd.concat(all_bt, ignore_index=True)
    validity_df = pd.concat(all_validity, ignore_index=True)
    winners_df, holdout_df, forecast_df = pd.DataFrame(winners), pd.DataFrame(holdouts), pd.DataFrame(forecasts)
    quality_df = pd.DataFrame([{
        "regla": q.rule, "descripcion": q.description, "estado": q.status,
        "detalle": q.detail, "grupos_afectados": ", ".join(q.affected_groups),
    } for q in quality])
    reconciliation_df, reconciliation_overview = _reconcile_retiros(xlsx_path, real)
    result = {
        "real": real, "quality": quality_df, "metrics": metrics_df, "backtest": bt_df,
        "prediction_validity": validity_df, "winners": winners_df, "holdout": holdout_df,
        "forecast": forecast_df, "reconciliation": reconciliation_df,
        "reconciliation_overview": reconciliation_overview, "sparse_groups": sparse_groups,
        "version_dataset": version,
    }
    if write_outputs:
        _write_outputs(result)
    return result


def _write_outputs(result: dict) -> None:
    os.makedirs(DATA_OUT_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    result["real"].to_csv(os.path.join(DATA_OUT_DIR, "dataset_real.csv"), index=False, encoding="utf-8")
    mapping = {
        "quality": "reglas_calidad.csv", "metrics": "backtesting_metricas.csv",
        "backtest": "backtesting_detalle.csv", "prediction_validity": "predicciones_fuera_dominio.csv",
        "winners": "backtesting_ganadores.csv", "holdout": "holdout_final.csv",
        "forecast": "forecast_ago_dic_2026.csv", "reconciliation": "conciliacion_fuentes_agregada.csv",
    }
    for key, filename in mapping.items():
        result[key].to_csv(os.path.join(OUTPUTS_DIR, filename), index=False, encoding="utf-8")


def main() -> None:
    result = run_analysis()
    print("OK", result["version_dataset"], "salidas:", OUTPUTS_DIR)


if __name__ == "__main__":
    main()
