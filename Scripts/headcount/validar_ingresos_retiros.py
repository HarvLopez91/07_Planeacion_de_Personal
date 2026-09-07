#!/usr/bin/env python3
"""Valida las hojas `INGRESOS` y `RETIROS` de PptovsReal.xlsx contra el consolidador Kactus.

SOLO LECTURA: abre los libros con `read_only=True` y nunca llama a `save()`.
No emite datos personales: todas las salidas son totales agregados.
El reporte se escribe en `Outputs/`, ignorado por Git.

Uso:
    python Scripts/headcount/validar_ingresos_retiros.py [ANIO] [NN.Mes]
    python Scripts/headcount/validar_ingresos_retiros.py 2026 08.Agosto
"""
import base64
import collections
import datetime
import io
import json
import os
import re
import sys
import zlib

import openpyxl

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DESTINO = os.path.join(RAIZ, "Data", "HeadCount", "PptovsReal.xlsx")
KACTUS = os.path.join(RAIZ, "Data", "Contratos_Kactus", "Fuente_Oficial",
                      "CONSOLIDADOR_CONTRATOS_V0.0.0.xlsx")
DIM_EMPRESAS = os.path.join(RAIZ, "PBIP", "Proyecto.SemanticModel", "definition",
                            "tables", "Empresas.tmdl")
SALIDA = os.path.join(RAIZ, "Outputs")

# Hojas del consolidador por periodo. "A" = Indicador Actividad A (ingresos),
# "I" = Indicador Actividad I (retiros). Los nombres los define quien mantiene
# el consolidador, por eso se resuelven por patron y no por lista fija.
PAT_INGRESOS = r"^\s*{mes3}\s*,\s*A\s*$"
PAT_RETIROS = r"^\s*{mes3}\s*(II|,\s*I)\s*$"

MESES3 = {"01": "ene", "02": "feb", "03": "mar", "04": "abr", "05": "may", "06": "jun",
          "07": "jul", "08": "ago", "09": "sep", "10": "oct", "11": "nov", "12": "dic"}


def dimension_empresas():
    """Valores validos de la dimension Empresas del modelo semantico."""
    try:
        t = io.open(DIM_EMPRESAS, encoding="utf-8", errors="replace").read()
        m = re.search(r'Binary\.FromText\("([^"]+)", BinaryEncoding\.Base64\)', t)
        data = json.loads(zlib.decompress(base64.b64decode(m.group(1)), -15).decode("utf-8"))
        return set(str(r[0]).strip() for r in data)
    except Exception:
        return set()


def _idx(cab, *nombres):
    for n in nombres:
        for i, c in enumerate(cab):
            if c.strip().lower() == n.lower():
                return i
    return None


def leer_hoja_destino(hoja, anio, mes):
    """Devuelve (registros del periodo, universo de periodos) de una hoja de PptovsReal."""
    wb = openpyxl.load_workbook(DESTINO, read_only=True, data_only=True)
    ws = wb[hoja]
    it = ws.iter_rows(values_only=True)
    cab = [str(c).strip() if c is not None else "" for c in next(it)]
    i_anio = _idx(cab, "Año", "Ano")
    i_mes = _idx(cab, "Mes")
    i_grupo = next((i for i, c in enumerate(cab) if c.lower().startswith("grupo empresa")), None)
    i_emp = _idx(cab, "Empresa")
    i_id = next((i for i, c in enumerate(cab) if "identific" in c.lower()), None)
    reg, periodos = [], collections.Counter()
    for r in it:
        if r[i_anio] is None:
            continue
        periodos[(r[i_anio], str(r[i_mes]).strip())] += 1
        if r[i_anio] == anio and str(r[i_mes]).strip() == mes:
            reg.append({
                "grupo": str(r[i_grupo]).strip() if i_grupo is not None else "",
                "empresa": str(r[i_emp]).strip() if i_emp is not None else "",
                "id": r[i_id] if i_id is not None else None,
            })
    wb.close()
    return reg, periodos


def contar_kactus(anio, mes):
    """Cuenta filas del consolidador para el periodo, por indicador de actividad."""
    mes3 = MESES3.get(mes.split(".")[0], "")
    wb = openpyxl.load_workbook(KACTUS, read_only=True, data_only=True)
    out = {}
    for etiqueta, patron in (("INGRESOS", PAT_INGRESOS), ("RETIROS", PAT_RETIROS)):
        rx = re.compile(patron.format(mes3=mes3), re.I)
        hojas = [h for h in wb.sheetnames if rx.match(h)]
        total, usadas = 0, []
        for h in hojas:
            filas = list(wb[h].iter_rows(values_only=True))
            # fila 1 es el titulo del volcado, fila 2 vacia, fila 3 encabezados
            datos = [r for r in filas[3:] if any(c is not None for c in r)]
            total += len(datos)
            usadas.append("%s (%d)" % (h, len(datos)))
        out[etiqueta] = {"total": total, "hojas": usadas}
    wb.close()
    return out


def validar(anio, mes):
    lineas, fallos = [], []
    dim = dimension_empresas()
    kac = contar_kactus(anio, mes)
    detalle = {}

    def chk(ok, titulo, det=""):
        lineas.append("- [%s] %s%s" % ("PASS" if ok else "FALLA", titulo, ("  -- " + det) if det else ""))
        if not ok:
            fallos.append(titulo)

    for hoja in ("INGRESOS", "RETIROS"):
        reg, periodos = leer_hoja_destino(hoja, anio, mes)
        esperado = kac[hoja]["total"]
        detalle[hoja] = {"reg": reg, "kactus": esperado, "hojas": kac[hoja]["hojas"]}

        chk(bool(reg), "%s: el periodo existe en PptovsReal" % hoja,
            "%d registros" % len(reg))
        chk(len(reg) == esperado, "%s: total cuadra contra el consolidador" % hoja,
            "PptovsReal %d vs Kactus %d %s" % (len(reg), esperado, kac[hoja]["hojas"]))

        ids = [r["id"] for r in reg if r["id"] is not None]
        dup = [k for k, v in collections.Counter(ids).items() if v > 1]
        chk(not dup, "%s: sin identificaciones repetidas en el mes" % hoja,
            "%d repetidas" % len(dup) if dup else "%d identificaciones" % len(ids))

        if dim:
            emp = sorted(set(r["empresa"] for r in reg))
            sin_match = [e for e in emp if e not in dim]
            chk(not sin_match, "%s: Empresa homologada contra la dimension del modelo" % hoja,
                "%d de %d valores sin match: %s" % (len(sin_match), len(emp),
                                                    ", ".join(sin_match[:6])) if sin_match
                else "%d valores" % len(emp))

        # coherencia de nomenclatura contra el mes anterior disponible
        def orden(p):
            return (str(p[0]), str(p[1]))
        antes = sorted([p for p in periodos if orden(p) < (str(anio), mes)],
                       key=orden, reverse=True)
        if antes:
            reg_prev, _ = leer_hoja_destino(hoja, antes[0][0], antes[0][1])
            g_prev = set(r["grupo"] for r in reg_prev)
            g_act = set(r["grupo"] for r in reg)
            nuevos = sorted(g_act - g_prev)
            chk(not nuevos, "%s: Grupo empresarial coherente con %s %s"
                % (hoja, antes[0][0], antes[0][1]),
                "valores nuevos: %s" % ", ".join(nuevos[:6]) if nuevos else "%d grupos" % len(g_act))

    return lineas, fallos, detalle


def main():
    anio = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
    mes = sys.argv[2] if len(sys.argv) > 2 else "08.Agosto"
    lineas, fallos, detalle = validar(anio, mes)
    estado = "PASS" if not fallos else "FALLA"

    rep = ["# Validacion de INGRESOS y RETIROS - %s %s" % (anio, mes), "",
           "Fecha: %s" % datetime.date.today().isoformat(),
           "Resultado: **%s**" % estado, "",
           "Solo lectura. Sin datos personales: unicamente totales agregados.", "",
           "## Validaciones", ""] + lineas
    for hoja in ("INGRESOS", "RETIROS"):
        d = detalle[hoja]
        rep += ["", "## %s - %s %s" % (hoja, anio, mes), "",
                "Registros en PptovsReal: **%d** | Consolidador Kactus: **%d** | Hojas: %s"
                % (len(d["reg"]), d["kactus"], ", ".join(d["hojas"]) or "-"), "",
                "| Grupo empresarial | Empresa | Registros |", "|---|---|---:|"]
        cnt = collections.Counter((r["grupo"], r["empresa"]) for r in d["reg"])
        for (g, e), n in sorted(cnt.items()):
            rep.append("| %s | %s | %d |" % (g, e, n))
        rep.append("| **TOTAL** | | **%d** |" % len(d["reg"]))

    os.makedirs(SALIDA, exist_ok=True)
    ruta = os.path.join(SALIDA, "validacion_ingresos_retiros_%s_%s.md"
                        % (anio, mes.split(".")[0]))
    io.open(ruta, "w", encoding="utf-8", newline="").write("\r\n".join(rep))

    print("\n".join(lineas))
    print()
    print("RESULTADO: %s" % estado)
    print("Reporte: %s" % os.path.relpath(ruta, RAIZ))
    return 0 if estado == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
