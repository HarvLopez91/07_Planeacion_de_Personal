# -*- coding: utf-8 -*-
"""Pruebas del contrato ampliado de `Rotacion Proyectada` (RETIROS + ROTACION).

Dos familias:

- las de datos construyen marcos sinteticos con la forma de las dos corridas
  oficiales, de modo que no dependen de `Data/**` ni de Excel;
- las de TMDL leen el modelo semantico como texto y protegen los invariantes que
  no se pueden verificar sin Power BI Desktop: que la carga no ancle el numero de
  columnas, que exista el puente de compatibilidad con el CSV legado y que
  ninguna medida de Retiros quede expuesta a las filas de Rotacion.
"""

from __future__ import annotations

import io
import os
import re
import unittest

import numpy as np
import pandas as pd

from Scripts.rotacion_proyectada.contrato import (
    COLUMNAS, COLUMNAS_LEGADO, COLUMNAS_NUEVAS, MODELO_COMPOSICION, TIPO_VALIDACION,
    construir_contrato, validar_contrato,
)
from Scripts.rotacion_proyectada.dataset import fecha_corte_de

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMDL_TABLA = os.path.join(RAIZ, "PBIP", "Proyecto.SemanticModel", "definition",
                          "tables", "Rotacion Proyectada.tmdl")
TMDL_MEDIDAS = os.path.join(RAIZ, "PBIP", "Proyecto.SemanticModel", "definition",
                            "tables", "Tbl_Medidas.tmdl")

CORTE = 202607
HORIZONTE = [202608, 202609, 202610, 202611, 202612]
GRUPOS = ["Alfa", "Beta"]


def _res_sinteticas():
    """Emula las salidas de `run_analysis` y de `run` con dos grupos."""
    periodos = [202605, 202606, 202607]
    ret_real = pd.DataFrame([
        {"periodo": p, "grupo_empresa": g, "retiros": 10, "total_sena": 200,
         "tasa_mensual_retiros": 0.05}
        for g in GRUPOS for p in periodos])
    ing_real = pd.DataFrame([
        {"periodo": p, "grupo_empresa": g, "ingresos": 20, "total_sena": 200,
         "tasa_mensual_ingresos": 0.10}
        for g in GRUPOS for p in periodos])
    fc_ret = pd.DataFrame([
        {"periodo": p, "grupo_empresa": g, "tasa_mensual_retiros": 0.05,
         "tipo_registro": "BASELINE", "modelo": "M0_Naive",
         "li_80_aproximado": 0.02, "ls_80_aproximado": 0.08,
         "cobertura_historica_observada": 0.8}
        for g in GRUPOS for p in HORIZONTE])
    fc_rot = pd.DataFrame([
        {"periodo": p, "grupo_empresa": g, "horizonte": i + 1,
         "ingresos_proyectados": 20.0, "retiros_proyectados": 10.0,
         "total_sena_usado": 200.0, "indice_rotacion_proyectado": 0.075,
         "li_80_aproximado": 0.05, "ls_80_aproximado": 0.10,
         "modelo_ingresos": "M0_Naive", "modelo_retiros": "M0_Naive",
         "clasificacion": "BASELINE"}
        for g in GRUPOS for i, p in enumerate(HORIZONTE)])
    # El indice real se calcula, no se transcribe: una constante redondeada aqui
    # haria fallar la verificacion de la formula por una diferencia inventada.
    comp = pd.DataFrame([
        {"grupo_empresa": g, "ingresos_real": 22.0, "retiros_real": 9.0,
         "total_sena_real": 205.0,
         "indice_rotacion_real": ((22.0 + 9.0) / 2) / 205.0}
        for g in GRUPOS])
    res_rot = {"corte": CORTE, "fecha_corte": fecha_corte_de(CORTE),
               "horizonte": HORIZONTE, "version_dataset": "prueba",
               "retiros_real": ret_real, "ingresos_real": ing_real,
               "forecast": fc_rot, "comparacion_agosto": comp}
    return {"forecast": fc_ret}, res_rot


class ContratoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res_ret, cls.res_rot = _res_sinteticas()
        cls.df = construir_contrato(cls.res_ret, cls.res_rot)

    def test_columnas_del_contrato(self):
        self.assertEqual(list(self.df.columns), COLUMNAS)
        self.assertEqual(len(COLUMNAS), 17)

    def test_el_prefijo_legado_conserva_nombre_y_orden(self):
        """Las 13 columnas del contrato anterior no se reordenan ni se renombran."""
        self.assertEqual(list(self.df.columns)[:13], COLUMNAS_LEGADO)
        self.assertEqual(list(self.df.columns)[13:], COLUMNAS_NUEVAS)

    def test_indicador_separa_las_dos_series(self):
        self.assertEqual(set(self.df["Indicador"]), {"RETIROS", "ROTACION"})
        for ind in ("RETIROS", "ROTACION"):
            self.assertGreater(len(self.df[self.df["Indicador"].eq(ind)]), 0)

    def test_sin_indicador_las_claves_colisionarian(self):
        """Justifica la columna: Retiros y Rotacion comparten Periodo x Grupo."""
        clave = ["Periodo", "Grupo Empresa", "TipoRegistro"]
        self.assertGreater(self.df.duplicated(subset=clave).sum(), 0)

    def test_unicidad_del_nuevo_grano(self):
        clave = ["Periodo", "Grupo Empresa", "Indicador", "TipoRegistro"]
        self.assertEqual(self.df.duplicated(subset=clave).sum(), 0)

    def test_rotacion_cumple_la_formula_por_componentes(self):
        rot = self.df[self.df["Indicador"].eq("ROTACION") & self.df["Valor"].ne("")]
        self.assertGreater(len(rot), 0)
        for _, r in rot.iterrows():
            i, x, s = float(r["Ingresos"]), float(r["Retiros"]), float(r["Total-Sena"])
            self.assertAlmostEqual(((i + x) / 2) / s, float(r["Valor"]), places=12)

    def test_rotacion_no_se_proyecta_como_tasa_de_retiros(self):
        fut = self.df[self.df["TipoRegistro"].eq("BASELINE")]
        rot = float(fut[fut["Indicador"].eq("ROTACION")]["Valor"].iloc[0])
        ret = float(fut[fut["Indicador"].eq("RETIROS")]["Valor"].iloc[0])
        self.assertNotAlmostEqual(rot, ret)

    def test_los_dos_modelos_quedan_visibles_en_rotacion(self):
        rot = self.df[self.df["Indicador"].eq("ROTACION")
                      & self.df["TipoRegistro"].eq("BASELINE")]
        self.assertEqual(set(rot["Modelo"]), {MODELO_COMPOSICION})
        self.assertTrue((rot["ModeloIngresos"] != "").all())
        self.assertTrue((rot["ModeloRetiros"] != "").all())

    def test_retiros_conserva_su_semantica(self):
        ret = self.df[self.df["Indicador"].eq("RETIROS")
                      & self.df["TipoRegistro"].eq("BASELINE")]
        self.assertEqual(set(ret["Modelo"]), {"M0_Naive"})
        self.assertTrue((ret["Ingresos"] == "").all())
        self.assertTrue((ret["ModeloIngresos"] == "").all())

    def test_agosto_real_y_proyectado_coexisten(self):
        ago = self.df[self.df["Periodo"].eq(str(HORIZONTE[0]))
                      & self.df["Indicador"].eq("ROTACION")]
        tipos = set(ago["TipoRegistro"])
        self.assertIn(TIPO_VALIDACION, tipos)
        self.assertIn("BASELINE", tipos)
        proy = ago[ago["TipoRegistro"].eq("BASELINE")]["Valor"].iloc[0]
        real = ago[ago["TipoRegistro"].eq(TIPO_VALIDACION)]["Valor"].iloc[0]
        self.assertNotEqual(proy, real)

    def test_real_validacion_no_entra_como_real(self):
        real = self.df[self.df["TipoRegistro"].eq("REAL")]
        self.assertEqual(int(real["Periodo"].astype(int).max()), CORTE)
        val = self.df[self.df["TipoRegistro"].eq(TIPO_VALIDACION)]
        self.assertTrue((val["Periodo"].astype(int) > CORTE).all())

    def test_fecha_corte_derivada_y_unica(self):
        self.assertEqual(set(self.df["FechaCorte"]), {"2026-07-31"})

    def test_horizonte_sin_enero_2027(self):
        self.assertNotIn(202701, set(self.df["Periodo"].astype(int)))

    def test_denominador_constante_en_el_horizonte(self):
        rot = self.df[self.df["Indicador"].eq("ROTACION")
                      & self.df["TipoRegistro"].eq("BASELINE")]
        self.assertEqual(rot.groupby("Grupo Empresa")["Total-Sena"].nunique().max(), 1)

    def test_validaciones_del_contrato_pasan(self):
        checks = validar_contrato(self.df, CORTE, "2026-07-31", HORIZONTE)
        fallidas = [c[0] for c in checks if not c[1]]
        self.assertEqual(fallidas, [])

    def test_los_conteos_reales_no_ganan_decimales(self):
        """El prefijo legado debe seguir escribiendo enteros donde antes los habia."""
        real = self.df[self.df["TipoRegistro"].eq("REAL")]
        self.assertTrue((real["Retiros"] == "10").all())
        self.assertTrue((real["Total-Sena"] == "200").all())


class TmdlContratoTests(unittest.TestCase):
    """Invariantes del modelo semantico que no se pueden probar sin Desktop."""

    @classmethod
    def setUpClass(cls):
        cls.tabla = io.open(TMDL_TABLA, encoding="utf-8").read()
        cls.medidas = io.open(TMDL_MEDIDAS, encoding="utf-8").read()

    def test_la_carga_no_ancla_el_numero_de_columnas(self):
        """`Columns = 13` impediria cargar el contrato ampliado."""
        self.assertNotIn("Columns = 13", self.tabla)
        self.assertNotIn("Columns =", self.tabla)

    def test_existe_el_puente_de_compatibilidad_con_el_csv_legado(self):
        for pieza in ("ColumnasAmpliadas", "List.Difference", "List.Accumulate",
                      "Indicador legado"):
            self.assertIn(pieza, self.tabla, pieza)

    def test_el_legado_se_interpreta_como_retiros(self):
        self.assertIn('then "RETIROS"', self.tabla)

    def test_las_cuatro_columnas_nuevas_estan_declaradas_y_tipadas(self):
        for col in COLUMNAS_NUEVAS:
            self.assertIn("\tcolumn %s" % col, self.tabla, col)
            self.assertIn('{"%s", type' % col, self.tabla, col)

    def test_retiros_admite_componentes_fraccionarias(self):
        bloque = self.tabla.split("\tcolumn Retiros")[1].split("\tcolumn")[0]
        self.assertIn("dataType: double", bloque)
        self.assertIn('{"Retiros", type number}', self.tabla)

    def test_las_relaciones_no_se_tocaron(self):
        rel = io.open(os.path.join(RAIZ, "PBIP", "Proyecto.SemanticModel",
                                   "definition", "relationships.tmdl"),
                      encoding="utf-8").read()
        self.assertIn("relationship PBIP008_Rotacion_Grupo", rel)
        self.assertIn("relationship PBIP008_Rotacion_Periodo", rel)

    def test_las_medidas_de_retiros_filtran_por_indicador(self):
        """Sin este filtro, las filas de ROTACION cambiarian los numeros de Retiros."""
        criticas = ["PBIP008 Tasa Futura", "PBIP008 Banda Inferior",
                    "PBIP008 Banda Superior", "PBIP008 Clasificacion",
                    "PBIP008 Modelo", "PBIP008 Resumen Clasificacion",
                    "PBIP008 Control Desviacion Real", "PBIP008 Fecha Corte"]
        for nombre in criticas:
            bloque = self._bloque(nombre)
            self.assertIn('[Indicador] = "RETIROS"', bloque, nombre)

    def test_las_medidas_de_rotacion_filtran_por_su_indicador(self):
        for nombre in ["PBIP008 Rotacion Futura", "PBIP008 Rotacion Clasificacion",
                       "PBIP008 Rotacion Banda Inferior", "PBIP008 Rotacion Banda Superior",
                       "PBIP008 Rotacion Ingresos Proyectados",
                       "PBIP008 Rotacion Retiros Proyectados",
                       "PBIP008 Rotacion Denominador", "PBIP008 Rotacion Real Validacion"]:
            self.assertIn('[Indicador] = "ROTACION"', self._bloque(nombre), nombre)

    def test_real_validacion_no_contamina_la_seleccion_futura(self):
        """Clasificacion y Modelo usan lista blanca, no `<> REAL`."""
        for nombre in ("PBIP008 Clasificacion", "PBIP008 Modelo"):
            bloque = self._bloque(nombre)
            self.assertNotIn('[TipoRegistro] <> "REAL"', bloque, nombre)
            self.assertIn('"SIN_FORECAST"', bloque, nombre)
        self.assertNotIn('"REAL_VALIDACION"', self._bloque("PBIP008 Rotacion Futura"))

    def test_la_rotacion_real_reutiliza_la_medida_oficial(self):
        self.assertIn("[Indice_Rotacion]", self._bloque("PBIP008 Rotacion Real"))

    def _bloque(self, nombre):
        i = self.medidas.index("measure '%s'" % nombre)
        j = self.medidas.find("\tmeasure ", i + 1)
        return self.medidas[i:j if j > 0 else len(self.medidas)]


if __name__ == "__main__":
    unittest.main(verbosity=2)
