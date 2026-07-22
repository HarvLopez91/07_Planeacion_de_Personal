#!/usr/bin/env python
"""Valida el gobierno local de skills del proyecto."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


RAICES_SKILLS = {
    "oficial": ".agents/skills",
    "codex_local": ".codex/skills",
    "legacy": "Skills",
}

REFERENCIAS_LEGACY = [
    "tools/list_pbip_structure.py",
    "tools/prepare_commit_review.py",
    "Skills/",
]

PATRON_NOMBRE_TECNICO = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PATRON_TOOL = re.compile(r"(tools/[A-Za-z0-9_./-]+\.py)")
PATRON_RUTA_CODIGO = re.compile(r"`([A-Za-z0-9_.\\/-]+\.(?:py|md|json|ya?ml|txt))`")


def ruta_relativa(ruta: Path, raiz: Path) -> str:
    """Devuelve una ruta relativa con separadores estables."""
    try:
        return ruta.relative_to(raiz).as_posix()
    except ValueError:
        return ruta.as_posix()


def leer_texto_seguro(ruta: Path) -> tuple[str | None, str | None]:
    """Lee un archivo de texto sin detener toda la ejecucion si falla."""
    try:
        return ruta.read_text(encoding="utf-8-sig"), None
    except FileNotFoundError:
        return None, "El archivo no existe."
    except OSError as error:
        return None, f"No se pudo leer el archivo: {error}."
    except UnicodeDecodeError as error:
        return None, f"No se pudo decodificar como UTF-8: {error}."


def parsear_front_matter(contenido: str) -> tuple[dict[str, str], str | None]:
    """Parsea front matter YAML con un parser real y valida que sea un objeto."""
    lineas = contenido.splitlines()
    if not lineas or lineas[0].strip() != "---":
        return {}, "No se encontro front matter YAML inicial."

    cierre = None
    for indice, linea in enumerate(lineas[1:], start=1):
        if linea.strip() == "---":
            cierre = indice
            break

    if cierre is None:
        return {}, "El front matter YAML no tiene cierre."

    bloque = "\n".join(lineas[1:cierre])
    try:
        datos = yaml.safe_load(bloque)
    except yaml.YAMLError as error:
        return {}, f"El front matter YAML no es valido: {error}."

    if datos is None:
        return {}, "El front matter YAML esta vacio."
    if not isinstance(datos, dict):
        return {}, "El front matter YAML debe ser un objeto/mapa."

    return {str(clave): valor for clave, valor in datos.items()}, None


def nombre_tecnico_valido(nombre: str | None) -> bool:
    """Valida nombres tecnicos ASCII sin tildes ni caracteres problematicos."""
    if not nombre:
        return False
    try:
        nombre.encode("ascii")
    except UnicodeEncodeError:
        return False
    return bool(PATRON_NOMBRE_TECNICO.fullmatch(nombre))


def normalizar_ruta_referenciada(texto: str) -> str:
    """Normaliza rutas referenciadas dentro de una skill para validacion local."""
    return texto.strip().replace("\\", "/").lstrip("./")


def es_ruta_plantilla(ruta: str) -> bool:
    """Detecta placeholders de rutas de ejemplo que no deben validar existencia fisica."""
    marcadores = ("YYYY", "MM", "DD", "{", "}", "<", ">")
    return any(marcador in ruta for marcador in marcadores)


def listar_carpetas_skill(raiz: Path, carpeta_relativa: str) -> list[Path]:
    """Lista carpetas candidatas de skills sin fallar si la raiz no existe."""
    carpeta = raiz / carpeta_relativa
    if not carpeta.exists() or not carpeta.is_dir():
        return []
    return sorted([ruta for ruta in carpeta.iterdir() if ruta.is_dir()], key=lambda ruta: ruta.as_posix().lower())


def listar_skill_md(raiz: Path, carpeta_relativa: str) -> list[Path]:
    """Lista SKILL.md dentro de una raiz de skills sin fallar si no existe."""
    carpeta = raiz / carpeta_relativa
    if not carpeta.exists() or not carpeta.is_dir():
        return []
    return sorted(carpeta.glob("*/SKILL.md"), key=lambda ruta: ruta.as_posix().lower())


def detectar_referencias_tools(contenido: str, raiz: Path) -> list[dict[str, Any]]:
    """Detecta rutas tools/*.py mencionadas en una skill y valida existencia."""
    referencias: list[dict[str, Any]] = []
    vistas: set[str] = set()
    for coincidencia in PATRON_TOOL.finditer(contenido.replace("\\", "/")):
        ruta = coincidencia.group(1).rstrip("`.,);")
        if ruta in vistas:
            continue
        vistas.add(ruta)
        referencias.append(
            {
                "ruta": ruta,
                "existe": (raiz / ruta).exists(),
            }
        )
    return referencias


def detectar_rutas_referenciadas(contenido: str, raiz: Path) -> list[dict[str, Any]]:
    """Detecta rutas de archivos referenciadas entre comillas invertidas y valida existencia."""
    referencias: list[dict[str, Any]] = []
    vistas: set[str] = set()

    for coincidencia in PATRON_RUTA_CODIGO.finditer(contenido):
        ruta = normalizar_ruta_referenciada(coincidencia.group(1))
        if not ruta or ruta in vistas:
            continue
        vistas.add(ruta)
        es_plantilla = es_ruta_plantilla(ruta)
        referencias.append(
            {
                "ruta": ruta,
                "es_plantilla": es_plantilla,
                "existe": True if es_plantilla else (raiz / ruta).exists(),
            }
        )

    return referencias


def detectar_referencias_legacy(contenido: str, ruta_skill: Path, raiz: Path) -> list[dict[str, str]]:
    """Busca referencias a rutas legacy dentro de una skill."""
    hallazgos: list[dict[str, str]] = []
    for patron in REFERENCIAS_LEGACY:
        if patron in contenido:
            hallazgos.append(
                {
                    "ruta_skill": ruta_relativa(ruta_skill, raiz),
                    "referencia": patron,
                    "motivo": "Referencia legacy encontrada en SKILL.md.",
                }
            )
    return hallazgos


def evaluar_skill(carpeta_skill: Path, raiz: Path, ubicacion: str) -> dict[str, Any]:
    """Evalua una skill individual a partir de su carpeta contenedora."""
    ruta_skill = carpeta_skill / "SKILL.md"
    nombre_carpeta = carpeta_skill.name
    alertas: list[str] = []

    front_matter: dict[str, str] = {}
    error_front_matter: str | None = None
    referencias_tools: list[dict[str, Any]] = []
    referencias_archivos: list[dict[str, Any]] = []
    referencias_legacy: list[dict[str, str]] = []
    contenido: str | None = None
    error_lectura: str | None = None

    if not ruta_skill.exists():
        alertas.append("Falta SKILL.md en la carpeta de la skill.")
    else:
        contenido, error_lectura = leer_texto_seguro(ruta_skill)

    if error_lectura:
        alertas.append(error_lectura)
    elif contenido is not None:
        front_matter, error_front_matter = parsear_front_matter(contenido)
        if error_front_matter:
            alertas.append(error_front_matter)
        referencias_tools = detectar_referencias_tools(contenido, raiz)
        referencias_archivos = detectar_rutas_referenciadas(contenido, raiz)
        referencias_legacy = detectar_referencias_legacy(contenido, ruta_skill, raiz)

    nombre = front_matter.get("name")
    descripcion = front_matter.get("description")
    nombre_es_cadena = isinstance(nombre, str)
    descripcion_es_cadena = isinstance(descripcion, str)
    nombre_limpio = nombre.strip() if nombre_es_cadena else ""
    descripcion_limpia = descripcion.strip() if descripcion_es_cadena else ""

    if ubicacion != "oficial":
        alertas.append("La skill no esta en la ubicacion oficial .agents/skills/.")
    if not nombre_es_cadena:
        alertas.append("name debe ser una cadena.")
    if not descripcion_es_cadena:
        alertas.append("description debe ser una cadena.")
    if not nombre_limpio:
        alertas.append("Falta name en front matter.")
    if not descripcion_limpia:
        alertas.append("Falta description en front matter o esta vacia.")
    if nombre_es_cadena and not (1 <= len(nombre_limpio) <= 64):
        alertas.append("name debe tener entre 1 y 64 caracteres.")
    if descripcion_es_cadena and not (1 <= len(descripcion_limpia) <= 1024):
        alertas.append("La description debe tener entre 1 y 1024 caracteres.")
    if nombre_es_cadena and not nombre_tecnico_valido(nombre_limpio):
        alertas.append("El name debe cumplir kebab-case estricto: ^[a-z0-9]+(?:-[a-z0-9]+)*$.")
    if not nombre_tecnico_valido(nombre_carpeta):
        alertas.append("La carpeta de la skill debe cumplir kebab-case estricto.")
    if nombre_es_cadena and nombre_limpio != nombre_carpeta:
        alertas.append("El campo name debe coincidir exactamente con la carpeta padre.")

    for referencia in referencias_tools:
        if not referencia["existe"]:
            alertas.append(f"La tool referenciada no existe: {referencia['ruta']}.")

    for referencia in referencias_archivos:
        if not referencia["existe"]:
            alertas.append(f"El archivo referenciado no existe: {referencia['ruta']}.")

    for referencia in referencias_legacy:
        alertas.append(
            f"Referencia legacy detectada: {referencia['referencia']}."
        )

    return {
        "ubicacion": ubicacion,
        "ruta": ruta_relativa(ruta_skill, raiz),
        "carpeta": nombre_carpeta,
        "name": nombre,
        "description": descripcion,
        "front_matter_valido": error_front_matter is None and bool(nombre) and bool(descripcion),
        "nombre_tecnico_valido": nombre_tecnico_valido(nombre_limpio) if nombre_es_cadena else False,
        "descripcion_valida": 1 <= len(descripcion_limpia) <= 1024,
        "referencias_tools": referencias_tools,
        "referencias_archivos": referencias_archivos,
        "referencias_legacy": referencias_legacy,
        "alertas": alertas,
        "valida": ubicacion == "oficial" and not alertas,
    }


def detectar_duplicados(skills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Detecta skills duplicadas por name o carpeta entre raices."""
    indice: dict[str, list[dict[str, Any]]] = {}
    for skill in skills:
        claves = {f"name:{skill.get('name')}" if skill.get("name") else None, f"carpeta:{skill.get('carpeta')}"}
        for clave in claves:
            if clave:
                indice.setdefault(clave, []).append(skill)

    duplicados: list[dict[str, Any]] = []
    for clave, elementos in sorted(indice.items()):
        if len(elementos) > 1:
            ubicaciones = {elemento["ubicacion"] for elemento in elementos}
            duplicados.append(
                {
                    "clave": clave,
                    "rutas": [elemento["ruta"] for elemento in elementos],
                    "ubicaciones": sorted(ubicaciones),
                    "motivo": "Se detecto duplicidad de name o carpeta entre skills.",
                }
            )
    return duplicados


def inspeccionar_skills(ruta_repo: Path) -> dict[str, Any]:
    """Construye la salida JSON de gobierno de skills."""
    raiz = ruta_repo.expanduser().resolve()
    skills: list[dict[str, Any]] = []
    advertencias_raices: list[dict[str, Any]] = []

    for ubicacion, carpeta_relativa in RAICES_SKILLS.items():
        carpeta = raiz / carpeta_relativa
        existe = carpeta.exists()
        tiene_skills = bool(listar_skill_md(raiz, carpeta_relativa))
        advertencia = None
        if ubicacion == "legacy" and existe:
            advertencia = "Skills/ existe y debe tratarse como legacy."
        if ubicacion == "codex_local" and tiene_skills:
            advertencia = ".codex/skills/ tiene skills locales; no es ubicacion oficial del proyecto."
        advertencias_raices.append(
            {
                "ubicacion": ubicacion,
                "ruta": carpeta_relativa,
                "existe": existe,
                "tiene_skills": tiene_skills,
                "advertencia": advertencia,
            }
        )

        for carpeta_skill in listar_carpetas_skill(raiz, carpeta_relativa):
            skills.append(evaluar_skill(carpeta_skill, raiz, ubicacion))

    duplicados = detectar_duplicados(skills)
    referencias_legacy = [
        referencia
        for skill in skills
        for referencia in skill.get("referencias_legacy", [])
    ]

    for duplicado in duplicados:
        for skill in skills:
            if skill["ruta"] in duplicado["rutas"]:
                skill["alertas"].append(duplicado["motivo"])
                skill["valida"] = False

    skills_validas = [skill for skill in skills if skill["valida"]]
    skills_con_alertas = [skill for skill in skills if skill["alertas"]]

    return {
        "repo": raiz.as_posix(),
        "raices_revisadas": advertencias_raices,
        "skills_detectadas": skills,
        "skills_validas": skills_validas,
        "skills_con_alertas": skills_con_alertas,
        "duplicados": duplicados,
        "referencias_legacy": referencias_legacy,
        "resumen": {
            "total_skills": len(skills),
            "validas": len(skills_validas),
            "alertas": len(skills_con_alertas),
            "duplicados": len(duplicados),
            "referencias_legacy": len(referencias_legacy),
        },
    }


def crear_parser() -> argparse.ArgumentParser:
    """Define argumentos de linea de comandos."""
    parser = argparse.ArgumentParser(
        description="Valida gobierno de skills locales y devuelve JSON."
    )
    parser.add_argument("ruta_repo", help="Ruta del repositorio a revisar.")
    parser.add_argument("--pretty", action="store_true", help="Imprime JSON indentado.")
    return parser


def main() -> int:
    """Punto de entrada CLI."""
    parser = crear_parser()
    argumentos = parser.parse_args()
    resultado = inspeccionar_skills(Path(argumentos.ruta_repo))
    print(json.dumps(resultado, ensure_ascii=False, indent=2 if argumentos.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
