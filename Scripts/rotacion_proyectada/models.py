"""Modelos de pronostico M0-M6 para el backtesting de PBIP-008.

Implementados directamente sobre numpy (sin statsmodels, no disponible en
.venv sin autorizacion de instalacion adicional). Cada funcion recibe una
serie de entrenamiento (array 1D, orden cronologico) y un horizonte h, y
devuelve un array de h pronosticos puntuales.

Todas las funciones son deterministas (sin aleatoriedad), tal como exige
Specs/0027.
"""

from __future__ import annotations

import numpy as np

SEASONAL_PERIOD = 12


def m0_naive(y: np.ndarray, h: int) -> np.ndarray:
    return np.full(h, y[-1], dtype=float)


def m1_seasonal_naive(y: np.ndarray, h: int) -> np.ndarray:
    n = len(y)
    out = np.empty(h, dtype=float)
    for i in range(h):
        idx = n - SEASONAL_PERIOD + i
        out[i] = y[idx] if 0 <= idx < n else y[-1]
    return out


def m2_moving_average(y: np.ndarray, h: int, window: int) -> np.ndarray:
    w = min(window, len(y))
    return np.full(h, y[-w:].mean(), dtype=float)


def _best_moving_average(y: np.ndarray, h: int) -> tuple[np.ndarray, int]:
    """Elige la ventana {3,6,12} con menor error 1-paso-adelante in-sample."""
    best_w, best_err = 3, float("inf")
    for w in (3, 6, 12):
        if len(y) <= w:
            continue
        errs = []
        for t in range(w, len(y)):
            pred = y[t - w:t].mean()
            errs.append(abs(y[t] - pred))
        err = np.mean(errs) if errs else float("inf")
        if err < best_err:
            best_err, best_w = err, w
    return m2_moving_average(y, h, best_w), best_w


def _linear_trend_fit(y: np.ndarray) -> tuple[float, float]:
    t = np.arange(len(y), dtype=float)
    b, a = np.polyfit(t, y, 1)  # y = b*t + a
    return a, b


def m3_trend(y: np.ndarray, h: int) -> np.ndarray:
    a, b = _linear_trend_fit(y)
    n = len(y)
    t_future = np.arange(n, n + h, dtype=float)
    return a + b * t_future


def m4_trend_seasonal(y: np.ndarray, h: int) -> np.ndarray:
    n = len(y)
    a, b = _linear_trend_fit(y)
    t = np.arange(n, dtype=float)
    trend_fit = a + b * t
    resid = y - trend_fit
    seasonal_idx = np.zeros(SEASONAL_PERIOD)
    for m in range(SEASONAL_PERIOD):
        vals = resid[m::SEASONAL_PERIOD]
        seasonal_idx[m] = vals.mean() if len(vals) else 0.0
    seasonal_idx -= seasonal_idx.mean()  # centrar (aditivo, suma ~0)

    t_future = np.arange(n, n + h, dtype=float)
    trend_future = a + b * t_future
    seasonal_future = np.array([seasonal_idx[(n + i) % SEASONAL_PERIOD] for i in range(h)])
    return trend_future + seasonal_future


def _holt_fit(y: np.ndarray, alpha: float, beta: float) -> tuple[float, float, np.ndarray]:
    level = y[0]
    trend = y[1] - y[0] if len(y) > 1 else 0.0
    fitted = np.empty(len(y))
    fitted[0] = level
    for t in range(1, len(y)):
        prev_level, prev_trend = level, trend
        level = alpha * y[t] + (1 - alpha) * (prev_level + prev_trend)
        trend = beta * (level - prev_level) + (1 - beta) * prev_trend
        fitted[t] = prev_level + prev_trend
    return level, trend, fitted


def m5_holt(y: np.ndarray, h: int) -> np.ndarray:
    """Suavizamiento exponencial con tendencia (Holt). Grid search de
    alpha/beta minimizando SSE 1-paso-adelante in-sample."""
    grid = (0.1, 0.3, 0.5, 0.7, 0.9)
    best = None
    for alpha in grid:
        for beta in grid:
            level, trend, fitted = _holt_fit(y, alpha, beta)
            sse = np.sum((y[1:] - fitted[1:]) ** 2)
            if best is None or sse < best[0]:
                best = (sse, level, trend)
    _, level, trend = best
    return np.array([level + (i + 1) * trend for i in range(h)])


def _holt_winters_fit(y: np.ndarray, alpha: float, beta: float, gamma: float, m: int = SEASONAL_PERIOD):
    n = len(y)
    level = y[:m].mean()
    trend = (y[m:2 * m].mean() - y[:m].mean()) / m if n >= 2 * m else 0.0
    seasonal = [y[i] - level for i in range(m)]
    fitted = np.empty(n)
    for t in range(n):
        s_idx = t % m
        if t < m:
            fitted[t] = level + seasonal[s_idx]
            continue
        prev_level, prev_trend = level, trend
        seas = seasonal[t - m] if (t - m) < len(seasonal) else seasonal[s_idx]
        level = alpha * (y[t] - seas) + (1 - alpha) * (prev_level + prev_trend)
        trend = beta * (level - prev_level) + (1 - beta) * prev_trend
        new_seasonal = gamma * (y[t] - level) + (1 - gamma) * seas
        seasonal.append(new_seasonal)
        fitted[t] = prev_level + prev_trend + seas
    return level, trend, seasonal, fitted


def m6_holt_winters(y: np.ndarray, h: int) -> np.ndarray | None:
    """Holt-Winters aditivo. Requiere >= 2 ciclos completos (24 meses);
    devuelve None si no aplica (el llamador debe excluir el modelo)."""
    m = SEASONAL_PERIOD
    if len(y) < 2 * m:
        return None
    grid = (0.2, 0.5, 0.8)
    best = None
    for alpha in grid:
        for beta in grid:
            for gamma in grid:
                level, trend, seasonal, fitted = _holt_winters_fit(y, alpha, beta, gamma, m)
                sse = np.sum((y[m:] - fitted[m:]) ** 2)
                if best is None or sse < best[0]:
                    best = (sse, level, trend, seasonal)
    _, level, trend, seasonal = best
    n = len(y)
    out = np.empty(h)
    for i in range(h):
        out[i] = level + (i + 1) * trend + seasonal[n - m + (i % m)]
    return out


MODEL_FUNCS = {
    "M0_Naive": lambda y, h: m0_naive(y, h),
    "M1_NaiveEstacional": lambda y, h: m1_seasonal_naive(y, h),
    "M2_PromedioMovil": lambda y, h: _best_moving_average(y, h)[0],
    "M3_Tendencia": lambda y, h: m3_trend(y, h),
    "M4_Tendencia_Estacional": lambda y, h: m4_trend_seasonal(y, h),
    "M5_Holt": lambda y, h: m5_holt(y, h),
    "M6_HoltWinters": lambda y, h: m6_holt_winters(y, h),
}


# ---------------------------------------------------------------------------
# Baselines de tasa agrupada (B1-B5)
#
# Los modelos M0-M6 operan sobre la SERIE DE TASAS y por tanto promedian
# cocientes: un mes con planta pequena pesa igual que uno con planta grande.
# B1-B3 reconstruyen la tasa agrupando numerador y denominador
# (sum(retiros) / sum(planta)). B4 y B5 son deliberadamente otros estimadores:
# media y mediana, respectivamente, de las tasas mensuales de los ultimos 12
# meses. Sus nombres distinguen las dos familias para evitar llamarlas a todas
# "tasa agrupada".
#
# Firma distinta a MODEL_FUNCS: reciben (retiros_train, sena_train, h).
# ---------------------------------------------------------------------------


def _pooled(retiros: np.ndarray, sena: np.ndarray, h: int, ventana: int | None) -> np.ndarray:
    r = retiros if ventana is None else retiros[-ventana:]
    s = sena if ventana is None else sena[-ventana:]
    total = s.sum()
    tasa = r.sum() / total if total > 0 else 0.0
    return np.full(h, tasa, dtype=float)


POOLED_FUNCS = {
    "B1_TasaAgrupada12M": lambda r, s, h: _pooled(r, s, h, 12),
    "B2_TasaAgrupadaHist": lambda r, s, h: _pooled(r, s, h, None),
    "B3_TasaAgrupada24M": lambda r, s, h: _pooled(r, s, h, 24),
    "B4_MediaTasas12M": lambda r, s, h: np.full(h, np.mean((r / s)[-12:]), dtype=float),
    "B5_Mediana12M": lambda r, s, h: np.full(h, np.median((r / s)[-12:]), dtype=float),
}
