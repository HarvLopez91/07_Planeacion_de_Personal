# -*- coding: utf-8 -*-
"""Pruebas de la capa de Ingresos y de la composicion de Rotacion Proyectada.

No dependen de `Data/**`: construyen marcos sinteticos con la forma de la hoja
`Planta Personal`. Asi corren en cualquier checkout, incluido un worktree sin
las fuentes operativas.
"""

from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from Scripts.rotacion_proyectada.models import MODEL_FUNCS, POOLED_FUNCS
from Scripts.rotacion_proyectada.rotacion import (
    FORECAST_PERIODOS, PERIODO_CORTE, build_ingresos_layer, clasificacion_combinada,
    componer_rotacion, control_identidad_planta, evaluar_componente, fecha_corte_de,
    periodos_siguientes, reglas_calidad_ingresos, truncar_al_corte,
)


def hoja_sintetica(periodos, grupos=("Alfa",), ingresos=5, retiros=4, sena=200):
    """Replica el contrato posicional de `Planta Personal`: la columna 1 es el anio."""
    filas = []
    for p in periodos:
        for g in grupos:
            filas.append({
                "Ppto/Real": "Real", "Anio": p // 100, "Mes Num": p % 100,
                "Grupo Empresa": g, "Ingresos": ingresos, "Retiros": retiros,
                "Retiros Voluntarios": 0, "Total-Sena": sena, "Total": sena,
            })
    return pd.DataFrame(filas)


PERIODOS_43 = [a * 100 + m for a in (2023, 2024, 2025) for m in range(1, 13)] + \
              [202601, 202602, 202603, 202604, 202605, 202606, 202607]


class CorteCongeladoTests(unittest.TestCase):
    def test_truncar_elimina_meses_posteriores_al_corte(self):
        df = hoja_sintetica([202606, 202607, 202608, 202612])
        out = truncar_al_corte(df, PERIODO_CORTE)
        self.assertEqual(len(out), 2)

    def test_agosto_real_no_entra_a_la_capa_de_entrenamiento(self):
        """Agosto ya tiene dato real; el horizonte aprobado es inamovible."""
        df = hoja_sintetica([202607, 202608])
        ing = build_ingresos_layer(df, PERIODO_CORTE)
        self.assertEqual(ing["periodo"].max(), PERIODO_CORTE)
        self.assertNotIn(202608, set(ing["periodo"]))

    def test_horizonte_es_agosto_a_diciembre_sin_enero_2027(self):
        self.assertEqual(FORECAST_PERIODOS, [202608, 202609, 202610, 202611, 202612])
        self.assertNotIn(202701, FORECAST_PERIODOS)


class CorteParametrizadoTests(unittest.TestCase):
    """El corte es un parametro de la corrida, no una constante del codigo."""

    def test_el_corte_oficial_del_compromiso_2_es_202607(self):
        self.assertEqual(PERIODO_CORTE, 202607)

    def test_el_horizonte_se_deriva_del_corte(self):
        self.assertEqual(periodos_siguientes(202607), FORECAST_PERIODOS)

    def test_el_horizonte_cruza_el_fin_de_anio(self):
        self.assertEqual(periodos_siguientes(202611),
                         [202612, 202701, 202702, 202703, 202704])

    def test_la_fecha_de_corte_es_fin_de_mes(self):
        self.assertEqual(fecha_corte_de(202607), "2026-07-31")
        self.assertEqual(fecha_corte_de(202602), "2026-02-28")
        self.assertEqual(fecha_corte_de(202411), "2024-11-30")

    def test_otro_corte_no_requiere_editar_codigo(self):
        ing = build_ingresos_layer(hoja_sintetica([202605, 202606, 202607]), 202606)
        self.assertEqual(ing["periodo"].max(), 202606)
        r = reglas_calidad_ingresos(ing, 202606)
        self.assertEqual(r.loc[r["regla"].eq("I4"), "estado"].iloc[0], "PASS")

    def test_componer_acepta_horizonte_y_fecha_derivados(self):
        res = {"tasa_futura": np.full(5, 0.02), "clasificacion": "BASELINE",
               "modelo_final": "M0_Naive", "rmse_por_horizonte": {h: 0.01 for h in range(1, 6)}}
        out = componer_rotacion(res, res, 100.0, "Alfa", "v",
                                periodos_siguientes(202606), fecha_corte_de(202606))
        self.assertEqual(list(out["periodo"]), [202607, 202608, 202609, 202610, 202611])
        self.assertEqual(out["fecha_corte"].iloc[0], "2026-06-30")

    def test_por_defecto_conserva_el_horizonte_oficial(self):
        res = {"tasa_futura": np.full(5, 0.02), "clasificacion": "BASELINE",
               "modelo_final": "M0_Naive", "rmse_por_horizonte": {h: 0.01 for h in range(1, 6)}}
        out = componer_rotacion(res, res, 100.0, "Alfa", "v")
        self.assertEqual(list(out["periodo"]), FORECAST_PERIODOS)
        self.assertEqual(out["fecha_corte"].iloc[0], "2026-07-31")


class CapaIngresosTests(unittest.TestCase):
    def test_excluye_periodos_sin_planta(self):
        df = pd.concat([hoja_sintetica([202606]), hoja_sintetica([202607], sena=0)])
        self.assertEqual(len(build_ingresos_layer(df, PERIODO_CORTE)), 1)

    def test_tasa_es_ingresos_sobre_total_sena(self):
        ing = build_ingresos_layer(hoja_sintetica([202607], ingresos=10, sena=200))
        self.assertAlmostEqual(ing["tasa_mensual_ingresos"].iloc[0], 0.05)

    def test_agrega_empresas_dentro_del_grupo(self):
        df = pd.concat([hoja_sintetica([202607], ingresos=3, sena=100),
                        hoja_sintetica([202607], ingresos=7, sena=100)])
        ing = build_ingresos_layer(df)
        self.assertEqual(len(ing), 1)
        self.assertEqual(ing["ingresos"].iloc[0], 10)
        self.assertEqual(ing["total_sena"].iloc[0], 200)

    def test_reglas_de_calidad_detectan_hueco_mensual(self):
        ing = build_ingresos_layer(hoja_sintetica([202601, 202602, 202604, 202607]))
        r = reglas_calidad_ingresos(ing)
        self.assertEqual(r.loc[r["regla"].eq("I3"), "estado"].iloc[0], "FAIL")

    def test_reglas_de_calidad_exigen_corte_en_202607(self):
        ing = build_ingresos_layer(hoja_sintetica([202605, 202606]))
        r = reglas_calidad_ingresos(ing)
        self.assertEqual(r.loc[r["regla"].eq("I4"), "estado"].iloc[0], "FAIL")


class ClasificacionTests(unittest.TestCase):
    def test_la_componente_mas_debil_gobierna(self):
        self.assertEqual(clasificacion_combinada("FORECAST", "BASELINE"), "BASELINE")
        self.assertEqual(clasificacion_combinada("FORECAST", "SIN_FORECAST"), "SIN_FORECAST")
        self.assertEqual(
            clasificacion_combinada("BASELINE", "REFERENCIA_DESCRIPTIVA"),
            "REFERENCIA_DESCRIPTIVA")

    def test_dos_forecast_siguen_siendo_forecast(self):
        self.assertEqual(clasificacion_combinada("FORECAST", "FORECAST"), "FORECAST")


class ComposicionTests(unittest.TestCase):
    """La rotacion se compone; nunca se proyecta `Indice_Rotacion` directamente."""

    def _res(self, tasa, clas, rmse=0.01):
        return {"tasa_futura": np.full(5, tasa), "clasificacion": clas,
                "modelo_final": "M0_Naive", "rmse_por_horizonte": {h: rmse for h in range(1, 6)}}

    def test_aplica_la_formula_oficial(self):
        out = componer_rotacion(self._res(0.04, "FORECAST"), self._res(0.02, "FORECAST"),
                                100.0, "Alfa", "v")
        # ((4 + 2) / 2) / 100 = 3%
        self.assertAlmostEqual(out["indice_rotacion_proyectado"].iloc[0], 0.03)
        self.assertAlmostEqual(out["ingresos_proyectados"].iloc[0], 4.0)
        self.assertAlmostEqual(out["retiros_proyectados"].iloc[0], 2.0)

    def test_denominador_congelado_se_repite_en_todo_el_horizonte(self):
        out = componer_rotacion(self._res(0.04, "FORECAST"), self._res(0.02, "FORECAST"),
                                317.0, "Alfa", "v")
        self.assertEqual(out["total_sena_usado"].nunique(), 1)
        self.assertEqual(out["total_sena_usado"].iloc[0], 317.0)
        self.assertEqual(len(out), 5)

    def test_sin_forecast_no_publica_banda(self):
        out = componer_rotacion(self._res(np.nan, "SIN_FORECAST"),
                                self._res(np.nan, "SIN_FORECAST"), 3.0, "Alfa", "v")
        self.assertTrue(out["li_80_aproximado"].isna().all())
        self.assertTrue(out["indice_rotacion_proyectado"].isna().all())

    def test_referencia_descriptiva_no_publica_banda(self):
        out = componer_rotacion(self._res(0.02, "BASELINE"),
                                self._res(0.02, "REFERENCIA_DESCRIPTIVA"), 92.0, "Alfa", "v")
        self.assertEqual(out["clasificacion"].iloc[0], "REFERENCIA_DESCRIPTIVA")
        self.assertTrue(out["li_80_aproximado"].isna().all())

    def test_banda_inferior_nunca_es_negativa(self):
        out = componer_rotacion(self._res(0.001, "BASELINE"), self._res(0.001, "BASELINE"),
                                100.0, "Alfa", "v")
        self.assertTrue((out["li_80_aproximado"] >= 0).all())


class ProtocoloSeleccionTests(unittest.TestCase):
    def test_serie_constante_termina_en_baseline_no_en_forecast(self):
        """Sin senal que superar, naive gana: la salida honesta es BASELINE."""
        ing = build_ingresos_layer(hoja_sintetica(PERIODOS_43, ingresos=5, sena=200))
        res = evaluar_componente(ing, "tasa_mensual_ingresos", "ingresos",
                                 MODEL_FUNCS, POOLED_FUNCS)
        self.assertIn(res["clasificacion"], ("BASELINE", "FORECAST"))
        self.assertEqual(res["modelo_final"], "M0_Naive")
        self.assertEqual(res["clasificacion"], "BASELINE")

    def test_planta_pequena_degrada_a_sin_forecast(self):
        ing = build_ingresos_layer(hoja_sintetica(PERIODOS_43, ingresos=1, sena=5))
        res = evaluar_componente(ing, "tasa_mensual_ingresos", "ingresos",
                                 MODEL_FUNCS, POOLED_FUNCS)
        self.assertEqual(res["nivel_fiabilidad"], "C_SIN_FORECAST_CONFIABLE")
        self.assertEqual(res["clasificacion"], "SIN_FORECAST")

    def test_el_holdout_no_se_usa_para_elegir(self):
        ing = build_ingresos_layer(hoja_sintetica(PERIODOS_43))
        res = evaluar_componente(ing, "tasa_mensual_ingresos", "ingresos",
                                 MODEL_FUNCS, POOLED_FUNCS)
        # 43 meses: 38 para seleccionar (10 origenes) y 43 en el backtest completo (15).
        self.assertEqual(res["n_origenes_seleccion"], 10)
        self.assertEqual(res["n_origenes_full"], 15)
        self.assertEqual(res["periodo_fin_holdout"], PERIODO_CORTE)


class ControlIdentidadTests(unittest.TestCase):
    def test_identidad_exacta_da_desvio_cero(self):
        filas = []
        sena = 200
        for p in [202601, 202602, 202603]:
            filas.append({"Ppto/Real": "Real", "Anio": p // 100, "Mes Num": p % 100,
                          "Grupo Empresa": "Alfa", "Ingresos": 10, "Retiros": 4,
                          "Retiros Voluntarios": 0, "Total-Sena": sena, "Total": sena})
            sena += 6  # +Ingresos -Retiros
        df = pd.DataFrame(filas)
        ing = build_ingresos_layer(df)
        ret = ing.rename(columns={"ingresos": "x"}).assign(retiros=4)
        out = control_identidad_planta(ing, ret)
        self.assertAlmostEqual(out["desvio_abs_medio"].iloc[0], 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
