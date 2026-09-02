"""Pruebas de controles criticos de PBIP-008 (sin datos en el repositorio)."""

from __future__ import annotations

import os
import unittest

import pandas as pd

from Scripts.rotacion_proyectada.backtest import compute_metrics
from Scripts.rotacion_proyectada.dataset import (
    build_real_layer,
    load_planta_personal,
    run_quality_rules,
)
from Scripts.rotacion_proyectada.models import POOLED_FUNCS

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(REPO_ROOT, "Data", "HeadCount", "PptovsReal.xlsx")


class QualityControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = load_planta_personal(SOURCE)
        cls.real = build_real_layer(cls.source)

    def test_c9_reconciles_approved_source(self) -> None:
        _, results, _ = run_quality_rules(self.real, self.source)
        c9 = next(r for r in results if r.rule == "C9")
        self.assertEqual("PASS", c9.status)

    def test_c9_fails_after_controlled_perturbation(self) -> None:
        altered = self.real.copy()
        idx = altered.index[0]
        altered.loc[idx, "retiros"] += 1
        altered.loc[idx, "tasa_mensual_retiros"] = altered.loc[idx, "retiros"] / altered.loc[idx, "total_sena"]
        _, results, _ = run_quality_rules(altered, self.source)
        c9 = next(r for r in results if r.rule == "C9")
        self.assertEqual("FAIL", c9.status)
        self.assertIn("1 discrepancia", c9.detail)


class MetricTests(unittest.TestCase):
    def test_mase_is_scaled_inside_each_origin(self) -> None:
        bt = pd.DataFrame({
            "modelo": ["X", "X"], "horizonte": [1, 1],
            "error": [1.0, 3.0], "error_abs": [1.0, 3.0],
            "escala_naive": [1.0, 9.0], "real": [2.0, 4.0],
        })
        metrics = compute_metrics(bt, permitir_mape=False)
        mase = metrics.loc[
            metrics["horizonte"].eq("promedio(1-5)"), "MASE"
        ].iloc[0]
        self.assertAlmostEqual((1.0 / 1.0 + 3.0 / 9.0) / 2.0, mase)

    def test_b1_b3_pool_counts_while_b4_b5_aggregate_monthly_rates(self) -> None:
        import numpy as np

        retiros = np.arange(1.0, 31.0)
        sena = np.arange(101.0, 131.0)
        self.assertAlmostEqual(
            retiros[-12:].sum() / sena[-12:].sum(),
            POOLED_FUNCS["B1_TasaAgrupada12M"](retiros, sena, 5)[0],
        )
        self.assertAlmostEqual(
            retiros.sum() / sena.sum(),
            POOLED_FUNCS["B2_TasaAgrupadaHist"](retiros, sena, 5)[0],
        )
        self.assertAlmostEqual(
            retiros[-24:].sum() / sena[-24:].sum(),
            POOLED_FUNCS["B3_TasaAgrupada24M"](retiros, sena, 5)[0],
        )
        monthly = retiros / sena
        self.assertAlmostEqual(monthly[-12:].mean(), POOLED_FUNCS["B4_MediaTasas12M"](retiros, sena, 5)[0])
        self.assertAlmostEqual(np.median(monthly[-12:]), POOLED_FUNCS["B5_Mediana12M"](retiros, sena, 5)[0])


if __name__ == "__main__":
    unittest.main()
