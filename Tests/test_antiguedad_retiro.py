"""Synthetic calendar-boundary and PBIR invariants; no employee data."""
import calendar
import json
import re
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "PBIP/Proyecto.SemanticModel/definition/tables/Ppto Retiros.tmdl"
VISUAL = ROOT / "PBIP/Proyecto.Report/definition/pages/ReportSection6a1196bf8c963b709405/visuals/a7f9d2c14b8e4f65a901/visual.json"
TEXT = TABLE.read_text(encoding="utf-8")
LIMITS = tuple(map(int, re.search(r"Limites = \{([^}]+)\}", TEXT)[1].split(",")))
LABELS = json.loads("[" + re.search(r"Etiquetas = \{([^}]+)\}", TEXT)[1] + "]")


def anniversary(start, months):
    n = start.year * 12 + start.month - 1 + months
    year, month = divmod(n, 12)
    month += 1
    return date(year, month, min(start.day, calendar.monthrange(year, month)[1]))


def classify(start, end):
    if start is None or start == "": return 90
    if end is None or end == "": return 91
    if not isinstance(start, date): return 92
    if not isinstance(end, date): return 93
    if end < start: return 94
    return next((i for i, m in enumerate(LIMITS, 1) if end <= anniversary(start, m)), 11)


class TenureTests(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual(LIMITS, (2, 4, 6, 12, 24, 36, 60, 120, 240, 360))
        self.assertEqual(len(set(LABELS)), 11)
        for start in (date(2023, 1, 31), date(2024, 1, 31), date(2024, 2, 29), date(2023, 12, 30), date(2024, 3, 15)):
            self.assertEqual(classify(start, start), 1)
            for i, months in enumerate(LIMITS, 1):
                edge = anniversary(start, months)
                self.assertEqual(classify(start, edge - timedelta(days=1)), i)
                self.assertEqual(classify(start, edge), i)
                self.assertEqual(classify(start, edge + timedelta(days=1)), i + 1)
        self.assertEqual(anniversary(date(2023, 12, 31), 2), date(2024, 2, 29))
        self.assertEqual(anniversary(date(2022, 12, 31), 2), date(2023, 2, 28))
        self.assertEqual(anniversary(date(2024, 2, 29), 12), date(2025, 2, 28))

    def test_quality(self):
        d = date(2024, 1, 1)
        for a, b, expected in [(None,d,90),(d,None,91),("bad",d,92),(d,"bad",93),(d,d-timedelta(days=1),94)]:
            self.assertEqual(classify(a,b), expected)

    def test_unique_and_complete(self):
        start = date(1990, 1, 31)
        for day in range(0, 12000):
            end = start + timedelta(days=day)
            order = classify(start, end)
            lower = start if order == 1 else anniversary(start, LIMITS[order-2])
            upper = anniversary(start, LIMITS[order-1]) if order <= 10 else None
            self.assertTrue(end >= lower if order == 1 else end > lower)
            self.assertTrue(upper is None or end <= upper)

    def test_relative_frequency_contract(self):
        text = (ROOT / "PBIP/Proyecto.SemanticModel/definition/tables/Tbl_Medidas.tmdl").read_text(encoding="utf-8")
        measure = text.split("measure 'Retiros Frecuencia Relativa Antiguedad' =", 1)[1].split("\n\tmeasure ", 1)[0]
        self.assertIn("DIVIDE (", measure)
        self.assertEqual(measure.count("[Tot_Retiros]"), 2)
        self.assertIn("formatString: 0.00%", measure)
        self.assertEqual(set(re.findall(r"'Ppto Retiros'\[([^]]+)\]", measure)), {"Rango_Antiguedad_Retiro_Estandar", "Orden_Rango_Antiguedad_Retiro_Estandar"})
        self.assertNotIn("ALLSELECTED", measure)
        values = json.loads(VISUAL.read_text(encoding="utf-8"))["visual"]["query"]["queryState"]["Values"]["projections"]
        self.assertEqual(len(values), 2)
        self.assertEqual(values[0]["field"]["Measure"]["Property"], "Tot_Retiros")
        self.assertEqual(values[1]["field"]["Measure"]["Property"], "Retiros Frecuencia Relativa Antiguedad")
        for counts in ([100, 200, 516], [2, 3, 1], [5], [0, 0]):
            total = sum(counts)
            relative = [n / total if total else None for n in counts]
            if total: self.assertAlmostEqual(sum(relative), 1)
            else: self.assertTrue(all(x is None for x in relative))

    def test_model_and_visual(self):
        self.assertIn("each R <= Date.AddMonths(I, _)", TEXT)
        self.assertIn("sortByColumn: Orden_Rango_Antiguedad_Retiro_Estandar", TEXT)
        for name in ("Meses_Antiguedad_Retiro", "Rango_Antiguedad_Retiro", "Orden_Rango_Antiguedad_Retiro"):
            self.assertRegex(TEXT, r"column " + name + r"\s")
        v = json.loads(VISUAL.read_text(encoding="utf-8"))["visual"]
        self.assertEqual(v["visualType"], "pivotTable")
        q = v["query"]["queryState"]
        self.assertEqual(q["Rows"]["projections"][0]["field"]["Column"]["Property"], "Rango_Antiguedad_Retiro_Estandar")
        self.assertEqual(q["Values"]["projections"][0]["field"]["Measure"]["Property"], "Tot_Retiros")


if __name__ == "__main__":
    unittest.main()
