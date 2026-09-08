"""Capa de Ingresos y composicion de Rotacion Proyectada oficial (PBIP-008).

Extiende el pipeline ya validado de Retiros sin duplicarlo: reutiliza
`dataset.build_real_layer`, `dataset.perfil_grupo`, `dataset.clasificar_fiabilidad`,
`models` y `backtest` tal como estan. Aqui solo se agrega lo que faltaba:

1. la serie historica de Ingresos al mismo grano Periodo x Grupo Empresa;
2. el congelamiento del corte 2026-07-31;
3. la composicion de `Indice_Rotacion` por componentes.

Decisiones metodologicas (Specs/0027, Specs/0028 y autorizacion del 2026-09-08):

- Corte congelado. Todo el entrenamiento se trunca en 202607. Agosto 2026 ya
  tiene dato real, pero NO entra al ajuste: se reserva para comparar Real vs
  Proyectado. Reentrenar con agosto produciria otra version, no esta.
- Ingresos se modelan como tasa, `ingresos / total_sena`, igual que Retiros.
  No es una eleccion estetica: permite usar la misma familia M0-M6 y los mismos
  baselines agrupados B1-B5, y como el denominador del horizonte esta congelado,
  tasa y conteo son equivalentes salvo un factor constante.
- Denominador congelado. Para agosto-diciembre 2026 se usa el ultimo
  `Total-Sena` observado al 2026-07-31 y se arrastra. No se proyecta planta.
  La identidad Planta(t) ~ Planta(t-1) + Ingresos - Retiros se calcula solo como
  control de coherencia.
- Conteos derivados. El pipeline almacena tasas; los conteos proyectados se
  derivan como `tasa * total_sena_usado` y se redondean solo para presentacion.

No modifica Data/**, PBIP/** ni fuentes operativas.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .backtest import HORIZON, MIN_TRAIN, compute_metrics, rolling_origin_backtest, select_winner
from .dataset import clasificar_fiabilidad, fecha_corte_de, perfil_grupo

PERIODO_CORTE = 202607
# Derivada, nunca escrita a mano: `fecha_corte_de` en dataset.py es la unica
# fuente de verdad de la fecha de corte.
FECHA_CORTE = fecha_corte_de(PERIODO_CORTE)
PERIODO_PRIMER_REAL_POSTERIOR = 202608
FORECAST_PERIODOS = [202608, 202609, 202610, 202611, 202612]
HOLDOUT = 5
Z_80 = 1.2816

# Umbral de mejora material sobre naive, identico al de run_backtesting.py.
UMBRAL_MEJORA_NAIVE = 0.95


def periodos_siguientes(corte: int, n: int = HORIZON) -> list[int]:
    """Los `n` periodos AAAAMM que siguen al corte.

    El horizonte se deriva del corte en lugar de estar escrito aparte, para que
    no puedan desincronizarse. Con corte 202607 devuelve exactamente
    `FORECAST_PERIODOS` (agosto-diciembre 2026, sin enero 2027).
    """
    corte = int(corte)
    anio, mes = corte // 100, corte % 100
    out = []
    for _ in range(n):
        mes += 1
        if mes > 12:
            anio, mes = anio + 1, 1
        out.append(anio * 100 + mes)
    return out


def _periodo_col(df: pd.DataFrame) -> pd.Series:
    """La cabecera de anio de `Planta Personal` llega con mojibake segun la
    exportacion; su posicion 1 es parte del contrato vigente de la hoja."""
    anio_col = df.columns[1]
    return (pd.to_numeric(df[anio_col], errors="coerce") * 100
            + pd.to_numeric(df["Mes Num"], errors="coerce"))


def truncar_al_corte(raw: pd.DataFrame, corte: int = PERIODO_CORTE) -> pd.DataFrame:
    """Devuelve la hoja cruda limitada a periodos <= corte.

    Se aplica ANTES de construir la capa REAL para que el pipeline de Retiros ya
    validado vea exactamente el universo que vio cuando se aprobo, aunque la
    fuente haya avanzado con meses posteriores.
    """
    out = raw.copy()
    out["__periodo"] = _periodo_col(out)
    out = out.loc[out["__periodo"].le(corte) | out["__periodo"].isna()]
    return out.drop(columns="__periodo")


def build_ingresos_layer(raw: pd.DataFrame, corte: int = PERIODO_CORTE) -> pd.DataFrame:
    """Serie historica de Ingresos a grano Periodo x Grupo Empresa.

    Misma hoja, mismo filtro `Ppto/Real == 'Real'` y mismo denominador
    `Total-Sena` que usa la capa de Retiros, de modo que ambas componentes de
    `Indice_Rotacion` compartan poblacion.
    """
    real = raw.loc[raw["Ppto/Real"].eq("Real")].copy()
    real["periodo"] = _periodo_col(real)
    real = real.loc[real["periodo"].le(corte)]
    agg = (real.groupby(["periodo", "Grupo Empresa"], as_index=False, dropna=False)
                .agg(ingresos=("Ingresos", "sum"), total_sena=("Total-Sena", "sum")))
    agg = agg.loc[agg["total_sena"].gt(0)].copy()
    agg["periodo"] = agg["periodo"].astype(int)
    agg = agg.rename(columns={"Grupo Empresa": "grupo_empresa"})
    agg["tasa_mensual_ingresos"] = agg["ingresos"] / agg["total_sena"]
    return agg.sort_values(["grupo_empresa", "periodo"]).reset_index(drop=True)


def reglas_calidad_ingresos(ing: pd.DataFrame, corte: int = PERIODO_CORTE) -> pd.DataFrame:
    """Controles I1-I6, espejo de C1-C8 de Retiros aplicados a Ingresos."""
    filas = []

    def add(regla, descripcion, ok, detalle, grupos=()):
        filas.append({"regla": regla, "descripcion": descripcion,
                      "estado": "PASS" if ok else "FAIL", "detalle": detalle,
                      "grupos_afectados": ", ".join(sorted(grupos))})

    nulos = int(ing["ingresos"].isna().sum())
    add("I1", "Ingresos sin nulos en periodos con planta > 0", nulos == 0,
        "%d valor(es) nulo(s)" % nulos)

    neg = ing.loc[ing["ingresos"].lt(0)]
    add("I2", "Ingresos >= 0", neg.empty,
        "%d fila(s) con ingresos negativos" % len(neg) if len(neg) else "Sin valores negativos",
        neg["grupo_empresa"].unique())

    huecos = []
    for g, sub in ing.groupby("grupo_empresa"):
        idx = sorted(p // 100 * 12 + p % 100 for p in sub["periodo"])
        faltan = sorted(set(range(idx[0], idx[-1] + 1)) - set(idx))
        if faltan:
            huecos.append(g)
    add("I3", "Continuidad mensual sin huecos por grupo", not huecos,
        "Grupos con huecos: %s" % huecos if huecos else "Sin huecos internos", huecos)

    maxp = int(ing["periodo"].max())
    add("I4", "El ultimo periodo de entrenamiento es %d" % corte, maxp == corte,
        "Maximo periodo en la capa de Ingresos: %d" % maxp)

    n_meses = ing.groupby("grupo_empresa")["periodo"].nunique()
    minimo = MIN_TRAIN + HOLDOUT + HORIZON
    cortos = n_meses[n_meses < minimo].index.tolist()
    add("I5", "Meses suficientes para seleccionar y validar (%d+%d+%d)"
        % (MIN_TRAIN, HOLDOUT, HORIZON), not cortos,
        "Meses por grupo: %s" % n_meses.to_dict(), cortos)

    pct0 = ing.groupby("grupo_empresa")["ingresos"].apply(lambda s: (s == 0).mean() * 100)
    ralos = pct0[pct0 > 25].index.tolist()
    filas.append({"regla": "I6",
                  "descripcion": "Grupos con >25% de meses sin ingresos degradan a baseline",
                  "estado": "DEGRADED" if ralos else "PASS",
                  "detalle": "%% meses en cero: %s" % pct0.round(1).to_dict(),
                  "grupos_afectados": ", ".join(sorted(ralos))})
    return pd.DataFrame(filas)


def _forecast_tasa(modelo, y, num, den, funcs_modelo, funcs_pooled, h=HORIZON):
    if modelo in funcs_pooled:
        return np.asarray(funcs_pooled[modelo](num, den, h), dtype=float)
    fc = funcs_modelo[modelo](y, h)
    if fc is None:
        raise ValueError("%s no puede ajustarse con %d observaciones" % (modelo, len(y)))
    return np.asarray(fc, dtype=float)


def evaluar_componente(sub: pd.DataFrame, col_tasa: str, col_evento: str,
                       funcs_modelo, funcs_pooled) -> dict:
    """Backtesting rolling-origin + holdout para una componente (Ingresos o Retiros).

    Protocolo identico al de run_backtesting.py, para que las dos componentes de
    `Indice_Rotacion` se elijan con el mismo criterio:

    1. se aparta el holdout final (5 meses) y NO se usa para elegir;
    2. rolling origin sobre el resto elige un ganador por MAE con desempates;
    3. el ganador se evalua una sola vez contra el holdout;
    4. solo si mejora a naive en mas de 5% se publica como FORECAST; si no,
       se degrada a BASELINE (M0_Naive), que es transparente y auditable;
    5. si al reentrenar con toda la serie el ganador produce tasas negativas, se
       excluye y se vuelve a elegir SOLO con las metricas pre-holdout; el
       fallback se publica unicamente si tambien es valido y supera a naive;
    6. `clasificar_fiabilidad` puede degradar antes a referencia descriptiva o a
       SIN_FORECAST por tamano de planta o series ralas.

    El paso 5 no es un detalle: es el que hizo que Grupo Sky quedara en
    `B3_TasaAgrupada24M` y no en `M0_Naive` en la corrida aprobada de Retiros.
    """
    sub = sub.sort_values("periodo")
    y = sub[col_tasa].to_numpy(float)
    ev = sub[col_evento].to_numpy(float)
    den = sub["total_sena"].to_numpy(float)
    periodos = sub["periodo"].to_numpy(int)

    perfil_src = sub.rename(columns={col_evento: "retiros"})
    perfil = perfil_grupo(perfil_src)
    permitir_mape = perfil["pct_meses_cero"] == 0

    bt_full = rolling_origin_backtest(pd.Series(y, index=periodos), ev, den)
    met_full = compute_metrics(bt_full, permitir_mape)

    n_sel = len(y) - HOLDOUT
    bt_sel = rolling_origin_backtest(pd.Series(y[:n_sel], index=periodos[:n_sel]),
                                     ev[:n_sel], den[:n_sel])
    met_sel = compute_metrics(bt_sel, permitir_mape)
    sel = select_winner(met_sel, bt_sel)
    modelo_sel = sel["ganador"] or "M0_Naive"

    fc_sel = _forecast_tasa(modelo_sel, y[:n_sel], ev[:n_sel], den[:n_sel],
                            funcs_modelo, funcs_pooled)
    fc_naive = _forecast_tasa("M0_Naive", y[:n_sel], ev[:n_sel], den[:n_sel],
                              funcs_modelo, funcs_pooled)
    real_hold = y[n_sel:]
    mae_hold = float(np.mean(np.abs(fc_sel - real_hold)))
    mae_naive_hold = float(np.mean(np.abs(fc_naive - real_hold)))
    rmse_hold = float(np.sqrt(np.mean((fc_sel - real_hold) ** 2)))
    mejora = mae_hold < mae_naive_hold * UMBRAL_MEJORA_NAIVE

    fila_sel = met_sel.loc[met_sel["modelo"].eq(modelo_sel)
                           & met_sel["horizonte"].eq("promedio(1-5)")].iloc[0]
    nivel, motivo = clasificar_fiabilidad(perfil, float(fila_sel["MAE"]))

    modelo_fallback = None
    mae_fallback = np.nan
    excluidos_productivo = []

    if nivel == "C_SIN_FORECAST_CONFIABLE":
        modelo_final, clasificacion = "SIN_FORECAST", "SIN_FORECAST"
        decision = "Planta demasiado pequena; ninguna tasa es interpretable"
    elif nivel == "B_REFERENCIA_DESCRIPTIVA":
        modelo_final, clasificacion = "B3_TasaAgrupada24M", "REFERENCIA_DESCRIPTIVA"
        decision = "Serie rala; se publica referencia descriptiva, no pronostico"
    elif mejora:
        prueba = _forecast_tasa(modelo_sel, y, ev, den, funcs_modelo, funcs_pooled)
        if (prueba < 0).any():
            # La seleccion pre-holdout se conserva como evidencia. Tras reentrenar
            # con la serie completa, una salida negativa invalida su uso productivo;
            # la alternativa se vuelve a elegir solo con las metricas pre-holdout.
            excluidos_productivo.append(modelo_sel)
            bt_red = bt_sel.loc[~bt_sel["modelo"].isin(excluidos_productivo)].copy()
            met_red = met_sel.loc[~met_sel["modelo"].isin(excluidos_productivo)].copy()
            alterno = select_winner(met_red, bt_red)
            modelo_fallback = alterno["ganador"] or "M0_Naive"
            fc_fb = _forecast_tasa(modelo_fallback, y[:n_sel], ev[:n_sel], den[:n_sel],
                                   funcs_modelo, funcs_pooled)
            mae_fallback = float(np.mean(np.abs(fc_fb - real_hold)))
            fb_valido = not (_forecast_tasa(modelo_fallback, y, ev, den,
                                            funcs_modelo, funcs_pooled) < 0).any()
            fb_mejora = mae_fallback < mae_naive_hold * UMBRAL_MEJORA_NAIVE
            if fb_valido and fb_mejora:
                modelo_final, clasificacion = modelo_fallback, "FORECAST"
                decision = ("Ganador pre-holdout paso el gate, pero su reentrenamiento "
                            "fue negativo; fallback predefinido valido y supera naive")
            else:
                modelo_final, clasificacion = "M0_Naive", "BASELINE"
                decision = ("Ganador productivo invalido y fallback sin mejora valida; "
                            "baseline transparente")
        else:
            modelo_final, clasificacion = modelo_sel, "FORECAST"
            decision = "Supera a naive en holdout por mas del 5%"
    else:
        modelo_final, clasificacion = "M0_Naive", "BASELINE"
        decision = "No supera materialmente a naive en holdout; baseline transparente"

    if modelo_final == "SIN_FORECAST":
        tasa_fut = np.full(HORIZON, np.nan)
    else:
        tasa_fut = _forecast_tasa(modelo_final, y, ev, den, funcs_modelo, funcs_pooled)

    rmse_h = {}
    bt_modelo = bt_full.loc[bt_full["modelo"].eq(modelo_final)]
    if not bt_modelo.empty and clasificacion in ("FORECAST", "BASELINE"):
        for h, hdf in bt_modelo.groupby("horizonte"):
            rmse_h[int(h)] = float(np.sqrt(np.mean(hdf["error"] ** 2)))

    return {
        "perfil": perfil, "metricas_full": met_full, "metricas_seleccion": met_sel,
        "backtest_full": bt_full, "modelo_seleccionado": modelo_sel,
        "motivo_seleccion": sel["motivo"], "modelo_final": modelo_final,
        "modelo_fallback_productivo": modelo_fallback,
        "mae_fallback_holdout": mae_fallback,
        "modelos_excluidos_forecast_negativo": ", ".join(excluidos_productivo),
        "clasificacion": clasificacion, "decision": decision,
        "nivel_fiabilidad": nivel, "motivo_fiabilidad": motivo,
        "mae_seleccion": float(fila_sel["MAE"]), "rmse_seleccion": float(fila_sel["RMSE"]),
        "mase_seleccion": float(fila_sel["MASE"]),
        "mae_holdout": mae_hold, "rmse_holdout": rmse_hold,
        "mae_naive_holdout": mae_naive_hold, "supera_naive_5pct": bool(mejora),
        "periodo_inicio_holdout": int(periodos[n_sel]),
        "periodo_fin_holdout": int(periodos[-1]),
        "tasa_futura": tasa_fut, "rmse_por_horizonte": rmse_h,
        "n_origenes_full": int(bt_full["origen"].nunique()),
        "n_origenes_seleccion": int(bt_sel["origen"].nunique()),
    }


# Jerarquia de clasificacion: la componente mas debil gobierna la rotacion.
_ORDEN = {"FORECAST": 0, "BASELINE": 1, "REFERENCIA_DESCRIPTIVA": 2, "SIN_FORECAST": 3}


def clasificacion_combinada(clas_ing: str, clas_ret: str) -> str:
    """La rotacion no puede ser mas confiable que su componente mas debil."""
    return max((clas_ing, clas_ret), key=lambda c: _ORDEN[c])


def componer_rotacion(res_ing: dict, res_ret: dict, total_sena_congelado: float,
                      grupo: str, version: str, periodos: list[int] | None = None,
                      fecha_corte: str | None = None) -> pd.DataFrame:
    """Aplica `Indice_Rotacion = ((Ingresos + Retiros)/2) / Total-Sena` mes a mes.

    El denominador es el `Total-Sena` observado al corte, arrastrado por el
    horizonte. Al ser constante, la banda se propaga desde las bandas de cada
    componente; se etiqueta como aproximada porque asume que los errores de
    Ingresos y Retiros se mueven juntos, que es el supuesto conservador (banda
    mas ancha), no una estimacion conjunta.
    """
    clas = clasificacion_combinada(res_ing["clasificacion"], res_ret["clasificacion"])
    periodos = FORECAST_PERIODOS if periodos is None else list(periodos)
    fecha_corte = FECHA_CORTE if fecha_corte is None else fecha_corte
    filas = []
    for i, periodo in enumerate(periodos):
        h = i + 1
        t_ing, t_ret = res_ing["tasa_futura"][i], res_ret["tasa_futura"][i]
        ing = t_ing * total_sena_congelado
        ret = t_ret * total_sena_congelado
        rot = ((ing + ret) / 2) / total_sena_congelado if total_sena_congelado else np.nan

        li = ls = np.nan
        if clas in ("FORECAST", "BASELINE"):
            r_i = res_ing["rmse_por_horizonte"].get(h)
            r_r = res_ret["rmse_por_horizonte"].get(h)
            if r_i is not None and r_r is not None:
                li = max(0.0, (max(0.0, t_ing - Z_80 * r_i)
                               + max(0.0, t_ret - Z_80 * r_r)) / 2)
                ls = ((t_ing + Z_80 * r_i) + (t_ret + Z_80 * r_r)) / 2

        filas.append({
            "grupo_empresa": grupo, "periodo": periodo, "horizonte": h,
            "ingresos_proyectados": ing, "retiros_proyectados": ret,
            "total_sena_usado": total_sena_congelado,
            "tasa_ingresos": t_ing, "tasa_retiros": t_ret,
            "indice_rotacion_proyectado": rot,
            "li_80_aproximado": li, "ls_80_aproximado": ls,
            "modelo_ingresos": res_ing["modelo_final"],
            "modelo_retiros": res_ret["modelo_final"],
            "clasificacion_ingresos": res_ing["clasificacion"],
            "clasificacion_retiros": res_ret["clasificacion"],
            "clasificacion": clas,
            "fecha_corte": fecha_corte, "version_dataset": version,
        })
    return pd.DataFrame(filas)


def control_identidad_planta(ing: pd.DataFrame, ret: pd.DataFrame) -> pd.DataFrame:
    """Control de coherencia Planta(t) ~ Planta(t-1) + Ingresos(t) - Retiros(t).

    NO es la metodologia del denominador: la planta no se proyecta. Se calcula
    solo para exhibir cuanto se aparta la hoja de esa identidad en el historico,
    y asi dimensionar el supuesto de arrastre.
    """
    base = ing[["periodo", "grupo_empresa", "ingresos", "total_sena"]].merge(
        ret[["periodo", "grupo_empresa", "retiros"]],
        on=["periodo", "grupo_empresa"], how="inner")
    out = []
    for g, sub in base.groupby("grupo_empresa"):
        sub = sub.sort_values("periodo").reset_index(drop=True)
        esperado = sub["total_sena"].shift(1) + sub["ingresos"] - sub["retiros"]
        d = sub.assign(planta_esperada=esperado,
                       desvio=sub["total_sena"] - esperado).dropna(subset=["desvio"])
        out.append({
            "grupo_empresa": g, "meses_comparados": len(d),
            "desvio_medio": float(d["desvio"].mean()),
            "desvio_abs_medio": float(d["desvio"].abs().mean()),
            "desvio_abs_medio_pct_planta": float(
                (d["desvio"].abs() / d["total_sena"]).mean() * 100),
            "desvio_max_abs": float(d["desvio"].abs().max()),
        })
    return pd.DataFrame(out)
