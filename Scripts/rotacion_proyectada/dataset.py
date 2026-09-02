"""Construccion del dataset analitico REAL para PBIP-008 (rotacion proyectada).

Lee 'Data/HeadCount/PptovsReal.xlsx' hoja 'Planta Personal', agrega a grano
Periodo (AAAAMM) x Grupo Empresa, y aplica las reglas de calidad C1-C10
definidas en Specs/0027_analisis_impacto_rotacion_proyectada.md.

No modifica Data/**. No escribe fuera de las rutas explicitas pasadas por el
llamador (ver run_backtesting.py).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

FECHA_CORTE = "2026-07-31"
ULTIMO_PERIODO_REAL_ESPERADO = 202607

# Umbrales de fiabilidad para decidir si un grupo admite pronostico estadistico.
# Ver Specs/0027, seccion de tratamiento de series ralas.
MIN_PLANTA_PROMEDIO = 30    # denominador minimo para que una tasa mensual sea interpretable
MAX_PCT_MESES_CERO = 25.0   # por encima de esto la serie es rala (regla C7)
MAX_ERROR_RELATIVO = 60.0   # MAE del ganador como % de la tasa media del grupo


def _periodo(anio: int, mes_num: int) -> int:
    return int(anio) * 100 + int(mes_num)


def load_planta_personal(xlsx_path: str) -> pd.DataFrame:
    df = pd.read_excel(xlsx_path, sheet_name="Planta Personal")
    df.columns = [str(c).strip() for c in df.columns]
    return df


def hash_fuente(xlsx_path: str) -> str:
    """SHA-256 (12 primeros caracteres) del archivo fuente.

    Se usa para construir un `version_dataset` reproducible: dos ejecuciones
    sobre la misma fuente producen la misma version, y un cambio en la fuente
    la cambia. Antes se usaba datetime.now(), lo que impedia verificar que dos
    corridas hubieran partido del mismo insumo.
    """
    h = hashlib.sha256()
    with open(xlsx_path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def build_real_layer(df: pd.DataFrame, version_dataset: str | None = None) -> pd.DataFrame:
    """Agrega Planta Personal (grano Empresa) a Grupo Empresa x Periodo,
    filtra Ppto/Real == 'Real', y arma el esquema REAL de Specs/0027."""
    version_dataset = version_dataset or "rotacion_sin_version"

    real = df[df["Ppto/Real"] == "Real"].copy()
    anio_col = [c for c in real.columns if c.strip().lower() in ("año", "ano")][0]
    real["periodo"] = real.apply(lambda r: _periodo(r[anio_col], r["Mes Num"]), axis=1)

    agg = (
        real.groupby(["periodo", "Grupo Empresa"], as_index=False)
        .agg(
            retiros=("Retiros", "sum"),
            retiros_voluntarios=("Retiros Voluntarios", "sum"),
            total_sena=("Total-Sena", "sum"),
        )
    )
    agg["anio"] = agg["periodo"] // 100
    agg["mes_num"] = agg["periodo"] % 100
    agg["grupo_empresa"] = agg["Grupo Empresa"]
    agg["empresa"] = None
    agg["tipo_registro"] = "REAL"
    agg["tasa_mensual_retiros"] = np.where(
        agg["total_sena"] > 0, agg["retiros"] / agg["total_sena"], np.nan
    )
    agg["modelo"] = None
    agg["li_80"] = np.nan
    agg["ls_80"] = np.nan
    agg["fecha_corte"] = FECHA_CORTE
    agg["version_dataset"] = version_dataset

    cols = [
        "periodo", "anio", "mes_num", "grupo_empresa", "empresa", "tipo_registro",
        "retiros", "retiros_voluntarios", "total_sena", "tasa_mensual_retiros",
        "modelo", "li_80", "ls_80", "fecha_corte", "version_dataset",
    ]
    return agg[cols].sort_values(["grupo_empresa", "periodo"]).reset_index(drop=True)


def reconstruct_source_control(df_source: pd.DataFrame) -> pd.DataFrame:
    """Reconstruye C9 directamente desde la hoja aprobada ``Planta Personal``.

    Esta ruta es deliberadamente independiente de :func:`build_real_layer`: no
    reutiliza el dataset analitico ni sus agregaciones. El control conserva solo
    registros Real hasta el corte, agrega Periodo x Grupo Empresa y calcula la
    tasa desde numerador y denominador de fuente.
    """
    source = df_source.loc[df_source["Ppto/Real"].eq("Real")].copy()
    # La exportacion historica puede traer el encabezado Año con mojibake. La
    # posicion 1 forma parte del contrato vigente de Planta Personal.
    anio_col = source.columns[1]
    source["periodo"] = (
        pd.to_numeric(source[anio_col], errors="coerce") * 100
        + pd.to_numeric(source["Mes Num"], errors="coerce")
    )
    source = source.loc[source["periodo"].le(ULTIMO_PERIODO_REAL_ESPERADO)]
    control = (
        source.groupby(["periodo", "Grupo Empresa"], as_index=False, dropna=False)
        .agg(retiros_fuente=("Retiros", "sum"), total_sena_fuente=("Total-Sena", "sum"))
        .rename(columns={"Grupo Empresa": "grupo_empresa"})
    )
    control = control.loc[control["total_sena_fuente"].gt(0)].copy()
    control["tasa_fuente"] = control["retiros_fuente"] / control["total_sena_fuente"]
    return control.sort_values(["grupo_empresa", "periodo"]).reset_index(drop=True)


@dataclass
class QualityResult:
    rule: str
    description: str
    status: str  # PASS, FAIL, DEGRADED
    detail: str
    affected_groups: list = field(default_factory=list)


def run_quality_rules(
    real_df: pd.DataFrame,
    source_df: pd.DataFrame,
) -> tuple[pd.DataFrame, list[QualityResult], list[str]]:
    """Aplica C1-C10. Devuelve (dataframe_filtrado, resultados, grupos_degradados_a_baseline).

    C1 excluye filas con total_sena <= 0 o nulo (p.ej. los meses Ago-Dic 2026
    que existen como placeholder 'Real' vacio en la fuente).
    C7/C8 degradan grupos a 'baseline simple' marcandolos en el resultado, sin
    eliminarlos del dataframe (la decision de que modelo usar se aplica despues,
    en el backtesting).
    """
    results: list[QualityResult] = []
    df = real_df.copy()

    # C1: total_sena > 0.
    # Las exclusiones legitimas son los placeholders de meses posteriores al
    # corte (periodo > ULTIMO_PERIODO_REAL_ESPERADO). Si se excluye un periodo
    # ANTERIOR al corte hay un hueco real en la fuente y el control debe fallar.
    mask_c1 = (df["total_sena"] > 0) & df["total_sena"].notna()
    excluidos_c1 = df.loc[~mask_c1, ["grupo_empresa", "periodo"]]
    df = df.loc[mask_c1].copy()
    exc_dentro = excluidos_c1[excluidos_c1["periodo"] <= ULTIMO_PERIODO_REAL_ESPERADO]
    results.append(QualityResult(
        "C1", "total_sena > 0 en todo periodo-grupo hasta el corte",
        "FAIL" if len(exc_dentro) else "PASS",
        f"{len(excluidos_c1)} fila(s) excluidas por total_sena<=0 o nulo; "
        f"{len(exc_dentro)} de ellas ANTES del corte {ULTIMO_PERIODO_REAL_ESPERADO} "
        f"(el resto son placeholders de meses futuros, exclusion esperada)",
        sorted(excluidos_c1["grupo_empresa"].unique().tolist()),
    ))

    # C2: los eventos de retiro no pueden ser negativos. No se impone un
    # limite superior de 100%: Retiros/Total-Sena es una tasa de eventos y la
    # regla de negocio no establece que un individuo solo pueda aportar un
    # evento durante el mes.
    bad_c2 = df[df["retiros"] < 0]
    results.append(QualityResult(
        "C2", "retiros >= 0; sin limite superior no documentado",
        "FAIL" if len(bad_c2) else "PASS",
        f"{len(bad_c2)} fila(s) tienen retiros negativos" if len(bad_c2)
        else "Sin valores negativos; no se presume que la tasa este acotada en 100%",
        sorted(bad_c2["grupo_empresa"].unique().tolist()),
    ))

    # C3: retiros_voluntarios <= retiros
    bad_c3 = df[df["retiros_voluntarios"] > df["retiros"]]
    results.append(QualityResult(
        "C3", "retiros_voluntarios <= retiros",
        "FAIL" if len(bad_c3) else "PASS",
        f"{len(bad_c3)} fila(s) violan la regla" if len(bad_c3) else "Sin violaciones",
        sorted(bad_c3["grupo_empresa"].unique().tolist()),
    ))

    # C4: continuidad mensual sin huecos por grupo
    huecos = []
    for g, sub in df.groupby("grupo_empresa"):
        periodos = sorted(sub["periodo"].unique())
        meses_idx = [p // 100 * 12 + p % 100 for p in periodos]
        esperado = list(range(meses_idx[0], meses_idx[-1] + 1))
        faltantes = sorted(set(esperado) - set(meses_idx))
        if faltantes:
            huecos.append((g, len(faltantes)))
    results.append(QualityResult(
        "C4", "Continuidad mensual sin huecos entre periodo_min y periodo_max",
        "FAIL" if huecos else "PASS",
        f"Huecos: {huecos}" if huecos else "Sin huecos internos",
        [h[0] for h in huecos],
    ))

    # C5: ya filtrado por construccion (build_real_layer solo toma Ppto/Real == 'Real')
    results.append(QualityResult(
        "C5", "Solo Ppto/Real = 'Real' entra a REAL", "PASS",
        "Filtro aplicado en build_real_layer antes de esta validacion", [],
    ))

    # C6: ultimo periodo REAL == 202607
    max_periodo = int(df["periodo"].max())
    results.append(QualityResult(
        "C6", "El ultimo periodo REAL es 202607",
        "PASS" if max_periodo == ULTIMO_PERIODO_REAL_ESPERADO else "FAIL",
        f"Maximo periodo encontrado: {max_periodo}", [],
    ))

    # C7: grupos con >25% de meses en cero -> no aptos para modelo estadistico
    pct_ceros = df.groupby("grupo_empresa")["retiros"].apply(lambda s: (s == 0).mean() * 100)
    grupos_no_aptos_c7 = pct_ceros[pct_ceros > 25].index.tolist()
    results.append(QualityResult(
        "C7", "Grupos con >25% de meses en cero degradan a baseline simple",
        "DEGRADED" if grupos_no_aptos_c7 else "PASS",
        f"% meses en cero por grupo: {pct_ceros.round(1).to_dict()}",
        grupos_no_aptos_c7,
    ))

    # C8: grupos con menos de 24 meses utiles
    n_meses = df.groupby("grupo_empresa")["periodo"].nunique()
    grupos_no_aptos_c8 = n_meses[n_meses < 24].index.tolist()
    results.append(QualityResult(
        "C8", "Grupos con menos de 24 meses utiles degradan a baseline simple",
        "DEGRADED" if grupos_no_aptos_c8 else "PASS",
        f"Meses utiles por grupo: {n_meses.to_dict()}",
        grupos_no_aptos_c8,
    ))

    # C9: conciliacion independiente contra una segunda reconstruccion directa
    # de Planta Personal, al grano minimo Periodo x Grupo Empresa.
    control = reconstruct_source_control(source_df)
    analytic = df[["periodo", "grupo_empresa", "retiros", "total_sena", "tasa_mensual_retiros"]].copy()
    joined = analytic.merge(control, on=["periodo", "grupo_empresa"], how="outer", indicator=True)
    present = joined["_merge"].eq("both")
    ok_retiros = present & np.isclose(joined["retiros"], joined["retiros_fuente"], atol=1e-9, rtol=0)
    ok_sena = present & np.isclose(joined["total_sena"], joined["total_sena_fuente"], atol=1e-9, rtol=0)
    ok_tasa = present & np.isclose(joined["tasa_mensual_retiros"], joined["tasa_fuente"], atol=1e-12, rtol=1e-10)
    discrepancias = joined.loc[~(ok_retiros & ok_sena & ok_tasa)].copy()
    grupos_c9 = sorted(discrepancias["grupo_empresa"].dropna().astype(str).unique().tolist())
    faltantes = int(joined["_merge"].ne("both").sum())
    results.append(QualityResult(
        "C9", "Dataset analitico reconcilia con Planta Personal en Periodo x Grupo Empresa",
        "PASS" if discrepancias.empty else "FAIL",
        f"{len(joined)} combinaciones comparadas; {len(discrepancias)} discrepancia(s); "
        f"{faltantes} clave(s) ausentes en uno de los lados. Se validaron Retiros, "
        "Total-Sena y Tasa_Mensual_Retiros mediante reconstruccion independiente",
        grupos_c9,
    ))

    # C10: outliers |z| > 3 sobre la serie del grupo (marcar, no eliminar)
    outliers = []
    for g, sub in df.groupby("grupo_empresa"):
        serie = sub.sort_values("periodo")["tasa_mensual_retiros"]
        z = (serie - serie.mean()) / serie.std(ddof=0) if serie.std(ddof=0) else serie * 0
        marcados = sub.loc[z.abs() > 3, "periodo"].tolist()
        if marcados:
            outliers.append((g, marcados))
    results.append(QualityResult(
        "C10", "Outliers |z|>3 marcados, no eliminados",
        "PASS",
        f"Outliers detectados: {outliers}" if outliers else "Ningun outlier |z|>3",
        [o[0] for o in outliers],
    ))

    grupos_no_aptos = sorted(set(grupos_no_aptos_c7) | set(grupos_no_aptos_c8))
    return df, results, grupos_no_aptos


def perfil_grupo(sub: pd.DataFrame) -> dict:
    """Estadisticos descriptivos de un grupo, usados para clasificar fiabilidad."""
    retiros = sub["retiros"].to_numpy(dtype=float)
    sena = sub["total_sena"].to_numpy(dtype=float)
    return {
        "n_meses": len(sub),
        "planta_promedio": float(sena.mean()),
        "planta_ultima": float(sena[-1]),
        "retiros_totales": float(retiros.sum()),
        "pct_meses_cero": float((retiros == 0).mean() * 100),
        "tasa_agrupada_hist": float(retiros.sum() / sena.sum()) if sena.sum() else float("nan"),
        "tasa_agrupada_12m": float(retiros[-12:].sum() / sena[-12:].sum()) if sena[-12:].sum() else float("nan"),
    }


def clasificar_fiabilidad(perfil: dict, mae_ganador: float) -> tuple[str, str]:
    """Decide si un grupo admite pronostico estadistico, solo una referencia
    descriptiva, o ningun numero.

    Devuelve (nivel, motivo) con nivel en:
      A_FORECAST_ESTADISTICO  - serie densa y error acotado; se publica pronostico.
      B_REFERENCIA_DESCRIPTIVA- serie rala pero planta interpretable; se publica una
                                tasa de referencia, NO un pronostico.
      C_SIN_FORECAST_CONFIABLE- planta demasiado pequena; no se publica ninguna tasa.

    El criterio evita el problema de la falsa precision: un grupo cuyo ultimo
    mes fue 0% no tiene por que tener rotacion esperada de 0%.
    """
    tasa = perfil["tasa_agrupada_hist"]
    err_rel = (mae_ganador / tasa * 100) if (tasa and tasa == tasa and mae_ganador == mae_ganador) else float("nan")

    if perfil["planta_promedio"] < MIN_PLANTA_PROMEDIO:
        return ("C_SIN_FORECAST_CONFIABLE",
                f"Planta promedio de {perfil['planta_promedio']:.1f} personas (< {MIN_PLANTA_PROMEDIO}): "
                f"una tasa mensual sobre este denominador salta en escalones de "
                f"{100 / perfil['planta_promedio']:.0f} puntos porcentuales por cada retiro, "
                f"por lo que ninguna cifra de tasa es interpretable")

    fallas = []
    if perfil["pct_meses_cero"] > MAX_PCT_MESES_CERO:
        fallas.append(f"{perfil['pct_meses_cero']:.1f}% de meses sin retiros (> {MAX_PCT_MESES_CERO}%)")
    if err_rel == err_rel and err_rel > MAX_ERROR_RELATIVO:
        fallas.append(f"el error tipico equivale al {err_rel:.0f}% de la tasa media (> {MAX_ERROR_RELATIVO}%)")

    if fallas:
        return ("B_REFERENCIA_DESCRIPTIVA",
                "Serie rala: " + "; ".join(fallas) +
                ". Se publica una tasa de referencia descriptiva, no un pronostico estadistico")

    return ("A_FORECAST_ESTADISTICO",
            f"Serie densa ({perfil['pct_meses_cero']:.0f}% de meses en cero) y error tipico "
            f"equivalente al {err_rel:.0f}% de la tasa media")
