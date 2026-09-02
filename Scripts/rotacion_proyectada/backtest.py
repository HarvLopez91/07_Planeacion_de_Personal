"""Backtesting de origen movil (rolling origin) para PBIP-008.

Sigue el diseno de Specs/0027: entrenamiento minimo 24 meses, horizonte fijo
h=1..5, origen avanza mes a mes. Con 43 meses caben 15 origenes (entrenar
hasta el mes 24..38 inclusive, sobran 5 para evaluar cada uno).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .models import MODEL_FUNCS, POOLED_FUNCS

MIN_TRAIN = 24
HORIZON = 5


def rolling_origin_backtest(
    serie: pd.Series,
    retiros: np.ndarray | None = None,
    sena: np.ndarray | None = None,
) -> pd.DataFrame:
    """serie: index = periodo (AAAAMM) ordenado ascendente, values = tasa_mensual_retiros.

    Si se pasan `retiros` y `sena` (alineados con la serie), tambien se evaluan
    los baselines de tasa agrupada B1-B5 de models.POOLED_FUNCS.

    Devuelve un DataFrame largo con una fila por (origen, horizonte, modelo).
    La columna `escala_naive` guarda el MAE naive 1-paso calculado UNICAMENTE
    sobre el tramo de entrenamiento de ese origen; es el denominador de MASE y
    de este modo la metrica no se contamina con periodos de prueba.
    """
    y = serie.values.astype(float)
    periodos = serie.index.to_numpy()
    n = len(y)
    n_origenes = n - MIN_TRAIN - HORIZON + 1
    rows = []
    for origen_i in range(n_origenes):
        train_end = MIN_TRAIN + origen_i  # cantidad de observaciones de entrenamiento
        y_train = y[:train_end]
        escala = np.mean(np.abs(np.diff(y_train))) if train_end > 1 else np.nan

        pronosticos: dict[str, np.ndarray] = {}
        for model_name, func in MODEL_FUNCS.items():
            fc = func(y_train, HORIZON)
            if fc is None:
                continue  # M6 sin condiciones suficientes en este origen
            pronosticos[model_name] = fc
        if retiros is not None and sena is not None:
            r_tr = np.asarray(retiros, dtype=float)[:train_end]
            s_tr = np.asarray(sena, dtype=float)[:train_end]
            for base_name, func in POOLED_FUNCS.items():
                pronosticos[base_name] = func(r_tr, s_tr, HORIZON)

        for model_name, forecast in pronosticos.items():
            for h_i in range(HORIZON):
                target_idx = train_end + h_i
                if target_idx >= n:
                    continue
                real_val = y[target_idx]
                pred_val = forecast[h_i]
                rows.append({
                    "origen": origen_i + 1,
                    "periodo_origen": int(periodos[train_end - 1]),
                    "horizonte": h_i + 1,
                    "periodo_objetivo": int(periodos[target_idx]),
                    "modelo": model_name,
                    "real": real_val,
                    "forecast": pred_val,
                    "error": pred_val - real_val,
                    "error_abs": abs(pred_val - real_val),
                    "escala_naive": escala,
                })
    return pd.DataFrame(rows)


def compute_metrics(bt_df: pd.DataFrame, permitir_mape: bool) -> pd.DataFrame:
    """Calcula MAE, RMSE, MAPE (si aplica) y MASE por modelo y horizonte.

    MASE escala cada error dentro de su propio origen temporal y luego agrega
    esos errores escalados. Asi, cada denominador usa exclusivamente el tramo
    de entrenamiento disponible en ese origen y no informacion futura.
    """

    def _agg(g: pd.DataFrame) -> pd.Series:
        mae = g["error_abs"].mean()
        rmse = np.sqrt((g["error"] ** 2).mean())
        valid_scale = g["escala_naive"].notna() & g["escala_naive"].gt(0)
        mase = (g.loc[valid_scale, "error_abs"] / g.loc[valid_scale, "escala_naive"]).mean()
        if not valid_scale.any():
            mase = np.nan
        if permitir_mape and (g["real"].abs() > 1e-6).all():
            mape = (g["error_abs"] / g["real"].abs()).mean() * 100
        else:
            mape = np.nan
        return pd.Series({"MAE": mae, "RMSE": rmse, "MAPE": mape, "MASE": mase, "n_obs": len(g)})

    por_horizonte = bt_df.groupby(["modelo", "horizonte"]).apply(_agg, include_groups=False).reset_index()
    promedio = bt_df.groupby("modelo").apply(_agg, include_groups=False).reset_index()
    promedio["horizonte"] = "promedio(1-5)"
    return pd.concat([por_horizonte, promedio], ignore_index=True)


def prediction_validity(bt_df: pd.DataFrame) -> pd.DataFrame:
    """Audita predicciones fuera del dominio documentado.

    Solo las predicciones negativas son invalidas. No se presume un maximo de
    100% para una tasa de eventos Retiros/Total-Sena. Un metodo con al menos una
    prediccion negativa queda fuera de la seleccion, pero sus resultados se
    conservan como evidencia de inestabilidad.
    """
    return (
        bt_df.groupby("modelo", as_index=False)
        .agg(
            n_predicciones=("forecast", "size"),
            n_negativas=("forecast", lambda s: int((s < 0).sum())),
            n_superiores_100=("forecast", lambda s: int((s > 1).sum())),
            prediccion_min=("forecast", "min"),
            prediccion_max=("forecast", "max"),
        )
        .assign(admisible=lambda x: x["n_negativas"].eq(0))
    )


def select_winner(metrics_promedio: pd.DataFrame, bt_df: pd.DataFrame) -> dict:
    """Aplica la cascada de criterios de Specs/0027 seccion 'Criterio objetivo
    de seleccion'. metrics_promedio: filas con horizonte == 'promedio(1-5)'."""
    m = metrics_promedio[metrics_promedio["horizonte"] == "promedio(1-5)"].copy()
    validity = prediction_validity(bt_df)
    invalidos = validity.loc[~validity["admisible"], "modelo"].tolist()
    m = m[~m["modelo"].isin(invalidos)].copy()
    if "M0_Naive" not in m["modelo"].values:
        return {"ganador": None, "motivo": "M0_Naive no evaluado, no se puede aplicar el umbral de admision"}
    mae_naive = m.loc[m["modelo"] == "M0_Naive", "MAE"].iloc[0]

    admitidos = m[m["MAE"] <= mae_naive].copy()
    if admitidos.empty or (len(admitidos) == 1 and admitidos["modelo"].iloc[0] == "M0_Naive"):
        return {"ganador": "M0_Naive", "motivo": "Ningun modelo supera a naive en MAE promedio; naive es el ganador por regla de umbral"}

    admitidos = admitidos.sort_values("MAE")
    mejor_mae = admitidos["MAE"].iloc[0]
    # Banda de empate del 5%. El termino absoluto evita que una serie casi
    # constante (mejor_mae ~ 0) colapse la banda y declare un ganador espurio.
    banda = mejor_mae * 1.05 + 1e-12
    empatados = admitidos[admitidos["MAE"] <= banda]

    if len(empatados) == 1:
        ganador = empatados["modelo"].iloc[0]
        motivo = "Menor MAE promedio, sin empate dentro del 5%"
    else:
        empatados = empatados.sort_values("RMSE")
        mejor_rmse = empatados["RMSE"].iloc[0]
        empatados2 = empatados[empatados["RMSE"] <= mejor_rmse * 1.05]
        if len(empatados2) == 1:
            ganador = empatados2["modelo"].iloc[0]
            motivo = "Empate en MAE (<=5%); desempatado por menor RMSE"
        else:
            h45 = bt_df[bt_df["horizonte"].isin([4, 5])]
            err_h45 = h45.groupby("modelo")["error_abs"].mean()
            candidatos = empatados2["modelo"].tolist()
            err_h45_candidatos = err_h45.reindex(candidatos).sort_values()
            ganador = err_h45_candidatos.index[0]
            motivo = "Empate en MAE y RMSE; desempatado por menor error en h=4 y h=5 (los meses mas lejanos del horizonte de 5 meses)"

    return {
        "ganador": ganador,
        "motivo": motivo,
        "mae_naive": mae_naive,
        "mae_ganador": m.loc[m["modelo"] == ganador, "MAE"].iloc[0],
        "supera_naive": bool(m.loc[m["modelo"] == ganador, "MAE"].iloc[0] <= mae_naive),
        "modelos_excluidos_prediccion_negativa": ", ".join(invalidos),
    }
