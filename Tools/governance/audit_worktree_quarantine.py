#!/usr/bin/env python
"""Diagnostica en modo solo lectura los worktrees de Git en cuarentena
(HEAD 000...0), causados tipicamente por fallos de 'git worktree remove'
en carpetas sincronizadas por OneDrive. Ver Specs/0021 para el contexto
completo.

GUARDRAILS (ver tambien Specs/0021 seccion 7 y la skill asociada):
Este script NO elimina, repara ni modifica worktrees, refs, el indice ni
ningun archivo bajo .git/worktrees. No debe agregarse aqui ninguna llamada
a 'git worktree remove', '--force', 'git worktree prune',
'git worktree repair', Remove-Item, rmdir, os.remove, os.unlink ni
shutil.rmtree. Las unicas escrituras permitidas son archivos temporales
dentro de tempfile.TemporaryDirectory() (carpeta temporal del sistema,
%TEMP% en Windows), que se limpian automaticamente al finalizar.

Un resultado SAFE_TO_INVESTIGATE_MANUAL_REMOVAL no autoriza una
eliminacion automatica: solo indica que no se detecto contenido en disco
sin preservar en el commit conocido de la rama. La decision y ejecucion
de cualquier remocion sigue siendo manual y humana.
"""

from __future__ import annotations

import argparse
import ctypes
import csv
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import time
from ctypes import wintypes
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional


ZERO_SHA = "0" * 40
EXPECTED_ADMIN_ENTRIES = ["HEAD", "commondir", "gitdir", "index", "ORIG_HEAD"]
KNOWN_LOCK_CANDIDATES = ["OneDrive.exe", "PBIDesktop.exe", "msmdsrv.exe"]

CLASSIFICATION_HEALTHY = "HEALTHY"
CLASSIFICATION_SAFE = "SAFE_TO_INVESTIGATE_MANUAL_REMOVAL"
CLASSIFICATION_UNPRESERVED = "NEEDS_REVIEW_UNPRESERVED_WORK"
CLASSIFICATION_NOT_IN_MAIN = "NEEDS_REVIEW_COMMIT_NOT_IN_MAIN"
CLASSIFICATION_CRITICAL = "CRITICAL_BRANCH_REF_MISSING"


# --------------------------------------------------------------------------
# Utilidades Git (solo lectura: rev-parse, merge-base, ls-remote, archive)
# --------------------------------------------------------------------------

def run_git(args: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, proc.stdout, proc.stderr


def find_repo_root(start: Optional[Path] = None) -> Path:
    start = start or Path.cwd()
    rc, out, _err = run_git(["rev-parse", "--show-toplevel"], start)
    if rc != 0:
        raise RuntimeError("no se pudo determinar la raiz del repositorio Git desde el directorio actual")
    return Path(out.strip())


def list_worktrees(repo_root: Path) -> list[dict[str, Any]]:
    rc, out, err = run_git(["worktree", "list", "--porcelain"], repo_root)
    if rc != 0:
        raise RuntimeError(f"'git worktree list --porcelain' fallo: {err.strip()}")

    entries: list[dict[str, Any]] = []
    current: dict[str, Any] = {}
    for line in out.splitlines():
        if not line.strip():
            if current:
                entries.append(current)
                current = {}
            continue
        if line.startswith("worktree "):
            if current:
                entries.append(current)
            current = {"worktree": line[len("worktree "):]}
        elif line.startswith("HEAD "):
            current["head"] = line[len("HEAD "):]
        elif line.startswith("branch "):
            current["branch"] = line[len("branch "):]
        elif line == "detached":
            current["detached"] = True
        elif line == "bare":
            current["bare"] = True
        elif line == "locked" or line.startswith("locked "):
            current["locked"] = True
        elif line == "prunable" or line.startswith("prunable "):
            current["prunable"] = True
    if current:
        entries.append(current)
    return entries


def find_admin_dir_for_worktree(repo_root: Path, worktree_path: Path) -> Optional[Path]:
    """Localiza .git/worktrees/<nombre> correspondiente a worktree_path,
    cruzando el archivo 'gitdir' cuando existe (mas confiable que asumir
    que el nombre administrativo coincide con el nombre de la carpeta)."""
    admin_root = repo_root / ".git" / "worktrees"
    if not admin_root.is_dir():
        return None

    target = str(worktree_path).replace("\\", "/").rstrip("/") + "/.git"
    for child in admin_root.iterdir():
        gitdir_file = child / "gitdir"
        if gitdir_file.is_file():
            try:
                content = gitdir_file.read_text(encoding="utf-8", errors="replace").strip()
            except OSError:
                continue
            if content.replace("\\", "/").rstrip("/") == target:
                return child

    fallback = admin_root / worktree_path.name
    if fallback.is_dir():
        return fallback
    return None


def inspect_admin_metadata(admin_dir: Optional[Path]) -> dict[str, Any]:
    if admin_dir is None or not admin_dir.exists():
        return {"admin_dir": None, "present": [], "missing": list(EXPECTED_ADMIN_ENTRIES)}
    present = []
    missing = []
    for name in EXPECTED_ADMIN_ENTRIES:
        if (admin_dir / name).exists():
            present.append(name)
        else:
            missing.append(name)
    return {"admin_dir": str(admin_dir), "present": present, "missing": missing}


def resolve_branch_sha(repo_root: Path, branch_ref: Optional[str]) -> Optional[str]:
    if not branch_ref:
        return None
    rc, out, _err = run_git(["rev-parse", branch_ref], repo_root)
    if rc == 0:
        return out.strip()
    return None


def check_is_ancestor(repo_root: Path, sha: str, main_ref: str) -> Optional[bool]:
    rc, _out, _err = run_git(["merge-base", "--is-ancestor", sha, main_ref], repo_root)
    if rc == 0:
        return True
    if rc == 1:
        return False
    return None  # sha o main_ref invalidos / error de git, no asumir nada


def check_remote_branch_exists(repo_root: Path, branch_name: Optional[str]) -> Optional[bool]:
    if not branch_name:
        return None
    rc, out, _err = run_git(["ls-remote", "--heads", "origin", branch_name], repo_root)
    if rc != 0:
        return None
    return bool(out.strip())


# --------------------------------------------------------------------------
# Analisis de contenido fisico no preservado (todo dentro de %TEMP%)
# --------------------------------------------------------------------------

def archive_commit_to_temp(repo_root: Path, sha: str, temp_root: Path) -> Path:
    target = temp_root / f"archive_{sha[:12]}"
    target.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(["git", "archive", sha], cwd=str(repo_root), capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"'git archive {sha}' fallo: {proc.stderr.decode('utf-8', 'replace')}")
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tf:
        try:
            tf.extractall(path=target, filter="data")  # Python >= 3.12 / backport
        except TypeError:
            tf.extractall(path=target)  # Python sin soporte de 'filter' (contenido propio y confiable)
    return target


def compare_worktree_to_commit(worktree_path: Path, commit_extract_path: Path) -> dict[str, Any]:
    worktree_files: dict[str, Path] = {}
    for root, dirs, files in os.walk(worktree_path):
        root_path = Path(root)
        if root_path == worktree_path:
            # '.git' es un ARCHIVO (no un directorio) dentro de un worktree
            # (contiene 'gitdir: <ruta>'), asi que debe excluirse de ambas
            # listas, no solo de 'dirs' como si siempre fuera un directorio.
            if ".git" in dirs:
                dirs.remove(".git")
            files = [f for f in files if f != ".git"]
        for fn in files:
            full = root_path / fn
            rel = full.relative_to(worktree_path).as_posix()
            worktree_files[rel] = full

    commit_files: dict[str, Path] = {}
    for root, _dirs, files in os.walk(commit_extract_path):
        for fn in files:
            full = Path(root) / fn
            rel = full.relative_to(commit_extract_path).as_posix()
            commit_files[rel] = full

    only_in_worktree: list[str] = []
    only_in_commit: list[str] = []
    differing: list[str] = []
    identical_count = 0

    for rel in sorted(set(worktree_files) | set(commit_files)):
        wpath = worktree_files.get(rel)
        cpath = commit_files.get(rel)
        if wpath is None:
            only_in_commit.append(rel)
        elif cpath is None:
            only_in_worktree.append(rel)
        else:
            try:
                same = wpath.read_bytes() == cpath.read_bytes()
            except OSError as exc:
                differing.append(f"{rel} (error de lectura: {exc})")
                continue
            if same:
                identical_count += 1
            else:
                differing.append(rel)

    return {
        "identical_count": identical_count,
        "only_in_worktree": only_in_worktree,
        "only_in_commit": only_in_commit,
        "differing": differing,
    }


# --------------------------------------------------------------------------
# Deteccion best-effort del proceso que bloquea la ruta (Windows)
# --------------------------------------------------------------------------

class _FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]


class _RM_UNIQUE_PROCESS(ctypes.Structure):
    _fields_ = [("dwProcessId", wintypes.DWORD), ("ProcessStartTime", _FILETIME)]


_CCH_RM_MAX_APP_NAME = 255
_CCH_RM_MAX_SVC_NAME = 63


class _RM_PROCESS_INFO(ctypes.Structure):
    _fields_ = [
        ("Process", _RM_UNIQUE_PROCESS),
        ("strAppName", wintypes.WCHAR * (_CCH_RM_MAX_APP_NAME + 1)),
        ("strServiceShortName", wintypes.WCHAR * (_CCH_RM_MAX_SVC_NAME + 1)),
        ("ApplicationType", wintypes.DWORD),
        ("AppStatus", wintypes.ULONG),
        ("TSSessionId", wintypes.DWORD),
        ("bRestartable", wintypes.BOOL),
    ]


def _restart_manager_query(paths: list[str]) -> list[dict[str, Any]]:
    """Implementacion real de la consulta Restart Manager. Puede lanzar
    cualquier excepcion; el llamador (find_locking_processes) la atrapa y
    degrada a heuristica. Es puramente de consulta: RmRegisterResources y
    RmGetList no bloquean, reparan ni liberan nada."""
    rstrtmgr = ctypes.WinDLL("rstrtmgr")

    RmStartSession = rstrtmgr.RmStartSession
    RmStartSession.argtypes = [ctypes.POINTER(wintypes.DWORD), wintypes.DWORD, ctypes.c_wchar_p]
    RmStartSession.restype = wintypes.DWORD

    RmRegisterResources = rstrtmgr.RmRegisterResources
    RmRegisterResources.argtypes = [
        wintypes.DWORD,
        wintypes.UINT,
        ctypes.POINTER(ctypes.c_wchar_p),
        wintypes.UINT,
        ctypes.c_void_p,
        wintypes.UINT,
        ctypes.c_void_p,
    ]
    RmRegisterResources.restype = wintypes.DWORD

    RmGetList = rstrtmgr.RmGetList
    RmGetList.restype = wintypes.DWORD

    RmEndSession = rstrtmgr.RmEndSession
    RmEndSession.argtypes = [wintypes.DWORD]
    RmEndSession.restype = wintypes.DWORD

    session_handle = wintypes.DWORD()
    session_key = ctypes.create_unicode_buffer(64)
    rc = RmStartSession(ctypes.byref(session_handle), 0, session_key)
    if rc != 0:
        raise OSError(f"RmStartSession devolvio {rc}")

    try:
        n_files = len(paths)
        file_arr = (ctypes.c_wchar_p * n_files)(*paths)
        rc = RmRegisterResources(session_handle, n_files, file_arr, 0, None, 0, None)
        if rc != 0:
            raise OSError(f"RmRegisterResources devolvio {rc}")

        pn_needed = wintypes.UINT(0)
        pn_info = wintypes.UINT(0)
        reboot_reasons = wintypes.DWORD(0)
        rc = RmGetList(session_handle, ctypes.byref(pn_needed), ctypes.byref(pn_info), None, ctypes.byref(reboot_reasons))
        needed = pn_needed.value
        if needed == 0:
            return []

        arr = (_RM_PROCESS_INFO * needed)()
        pn_info = wintypes.UINT(needed)
        rc = RmGetList(session_handle, ctypes.byref(pn_needed), ctypes.byref(pn_info), arr, ctypes.byref(reboot_reasons))
        if rc != 0:
            raise OSError(f"RmGetList (segunda llamada) devolvio {rc}")

        results = []
        for i in range(pn_info.value):
            info = arr[i]
            results.append({"pid": info.Process.dwProcessId, "app_name": info.strAppName})
        return results
    finally:
        RmEndSession(session_handle)


def find_locking_processes_restart_manager(paths: list[str]) -> Optional[list[dict[str, Any]]]:
    """None = API no disponible o fallo (degradar a heuristica).
    [] = API respondio pero no encontro procesos.
    [...] = procesos encontrados."""
    if os.name != "nt":
        return None
    try:
        return _restart_manager_query(paths)
    except Exception:
        return None


def heuristic_process_scan() -> list[dict[str, Any]]:
    if os.name != "nt":
        return []
    try:
        proc = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
    except Exception:
        return []
    if proc.returncode != 0:
        return []
    found = []
    try:
        reader = csv.reader(io.StringIO(proc.stdout))
        for row in reader:
            if not row:
                continue
            name = row[0]
            if any(name.lower() == candidate.lower() for candidate in KNOWN_LOCK_CANDIDATES):
                pid = row[1] if len(row) > 1 else None
                found.append({"name": name, "pid": pid})
    except Exception:
        return []
    return found


def detect_lock(path: Path, admin_dir: Optional[Path]) -> dict[str, Any]:
    candidates = [p for p in [str(path) if path.exists() else None,
                               str(admin_dir) if admin_dir and admin_dir.exists() else None] if p]
    restart_manager_result = find_locking_processes_restart_manager(candidates) if candidates else None
    return {
        "restart_manager": restart_manager_result,
        "heuristic": heuristic_process_scan(),
    }


# --------------------------------------------------------------------------
# Diagnostico por worktree
# --------------------------------------------------------------------------

@dataclass
class WorktreeDiagnosis:
    path: str
    branch_ref: Optional[str]
    head: Optional[str]
    classification: str
    admin_metadata: dict[str, Any] = field(default_factory=dict)
    branch_sha: Optional[str] = None
    branch_sha_error: Optional[str] = None
    is_ancestor_of_main: Optional[bool] = None
    remote_branch_exists: Optional[bool] = None
    unpreserved_work: Optional[dict[str, Any]] = None
    lock_info: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


def diagnose_entry(repo_root: Path, entry: dict[str, Any], main_ref: str, temp_root: Path) -> WorktreeDiagnosis:
    path = Path(entry["worktree"])
    head = entry.get("head")
    branch_ref = entry.get("branch")

    if head and head != ZERO_SHA:
        return WorktreeDiagnosis(
            path=str(path), branch_ref=branch_ref, head=head,
            classification=CLASSIFICATION_HEALTHY,
            notes=["HEAD valido; no esta en estado de cuarentena"],
        )

    notes: list[str] = []
    admin_dir = find_admin_dir_for_worktree(repo_root, path)
    admin_metadata = inspect_admin_metadata(admin_dir)

    branch_sha_error: Optional[str] = None
    branch_sha = resolve_branch_sha(repo_root, branch_ref)
    if branch_sha is None:
        branch_sha_error = (
            f"no se pudo resolver '{branch_ref}' desde el repositorio sano" if branch_ref
            else "sin referencia de rama en 'git worktree list --porcelain'"
        )
        return WorktreeDiagnosis(
            path=str(path), branch_ref=branch_ref, head=head,
            classification=CLASSIFICATION_CRITICAL,
            admin_metadata=admin_metadata,
            branch_sha_error=branch_sha_error,
            lock_info=detect_lock(path, admin_dir),
            notes=notes,
        )

    ancestor = check_is_ancestor(repo_root, branch_sha, main_ref)
    branch_name = branch_ref.split("refs/heads/", 1)[-1] if branch_ref else None
    remote_exists = check_remote_branch_exists(repo_root, branch_name)

    unpreserved: Optional[dict[str, Any]] = None
    if path.exists():
        try:
            extract_dir = archive_commit_to_temp(repo_root, branch_sha, temp_root)
            unpreserved = compare_worktree_to_commit(path, extract_dir)
        except Exception as exc:
            notes.append(f"no se pudo comparar contenido fisico contra el commit: {exc}")
    else:
        notes.append("la ruta del worktree ya no existe en disco")

    if ancestor is True:
        if unpreserved is None:
            classification = CLASSIFICATION_UNPRESERVED
            notes.append("no se pudo verificar el contenido fisico; se marca para revision por precaucion")
        elif unpreserved["only_in_worktree"] or unpreserved["differing"]:
            # Contenido en disco que no coincide con el commit conocido:
            # riesgo real de trabajo no preservado.
            classification = CLASSIFICATION_UNPRESERVED
        else:
            # 'only_in_commit' (archivos presentes en el commit pero
            # ausentes en disco) NO bloquea SAFE: ese contenido ya esta
            # preservado de forma segura en el commit (empujado a origin),
            # su ausencia en disco solo refleja el borrado parcial que dejo
            # el intento fallido de 'git worktree remove'. No hay nada que
            # perder al completar esa eliminacion.
            classification = CLASSIFICATION_SAFE
            if unpreserved["only_in_commit"]:
                notes.append(
                    f"{len(unpreserved['only_in_commit'])} archivo(s) del commit ya no estan en disco "
                    "(residuo del intento fallido de eliminacion); no representan trabajo en riesgo "
                    "porque el commit ya esta preservado"
                )
    elif ancestor is False:
        classification = CLASSIFICATION_NOT_IN_MAIN
    else:
        classification = CLASSIFICATION_UNPRESERVED
        notes.append(f"no se pudo determinar si {branch_sha} es ancestro de {main_ref}; se marca para revision por precaucion")

    return WorktreeDiagnosis(
        path=str(path), branch_ref=branch_ref, head=head,
        classification=classification,
        admin_metadata=admin_metadata,
        branch_sha=branch_sha,
        branch_sha_error=branch_sha_error,
        is_ancestor_of_main=ancestor,
        remote_branch_exists=remote_exists,
        unpreserved_work=unpreserved,
        lock_info=detect_lock(path, admin_dir),
        notes=notes,
    )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def print_human(payload: dict[str, Any]) -> None:
    print(f"Diagnostico de worktrees en cuarentena - {payload['timestamp']}")
    print(f"Repositorio: {payload['repo_root']}")
    print(f"Referencia principal: {payload['main_ref']}")
    print()
    for r in payload["results"]:
        print(f"- {r['path']}")
        print(f"  rama: {r['branch_ref']}")
        print(f"  HEAD: {r['head']}")
        print(f"  clasificacion: {r['classification']}")
        if r["classification"] == CLASSIFICATION_HEALTHY:
            print()
            continue
        print(f"  metadata admin ({r['admin_metadata'].get('admin_dir')}):")
        print(f"    presentes: {r['admin_metadata'].get('present')}")
        print(f"    faltantes: {r['admin_metadata'].get('missing')}")
        print(f"  commit de la rama: {r['branch_sha'] or '(no resuelto)'}")
        if r.get("branch_sha_error"):
            print(f"  error resolviendo rama: {r['branch_sha_error']}")
        print(f"  ancestro de {payload['main_ref']}: {r['is_ancestor_of_main']}")
        print(f"  rama remota existe: {r['remote_branch_exists']}")
        uw = r.get("unpreserved_work")
        if uw:
            print(f"  archivos identicos al commit: {uw['identical_count']}")
            print(f"  solo en disco (posible trabajo no preservado): {len(uw['only_in_worktree'])}")
            print(f"  con contenido distinto: {len(uw['differing'])}")
            print(f"  solo en el commit (ausentes en disco): {len(uw['only_in_commit'])}")
        li = r.get("lock_info", {})
        print(f"  lock (Restart Manager): {li.get('restart_manager')}")
        print(f"  lock (heuristica de procesos conocidos): {li.get('heuristic')}")
        for note in r.get("notes", []):
            print(f"  nota: {note}")
        print()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Diagnostica en modo solo lectura los worktrees de Git en cuarentena "
            "(HEAD 000...0). No elimina, repara ni modifica nada. Ver Specs/0021."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Diagnostica todos los worktrees en cuarentena detectados")
    group.add_argument("--worktree", metavar="RUTA", help="Diagnostica un unico worktree por ruta")
    parser.add_argument("--main-ref", default="origin/main", help="Referencia contra la que verificar ancestro (default: origin/main)")
    parser.add_argument("--json", action="store_true", help="Salida en JSON en vez de texto legible")
    parser.add_argument("--repo", default=None, help="Ruta del repositorio (default: se detecta desde el directorio actual)")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    # Fuerza UTF-8 en stdout/stderr: en Windows, al redirigir a archivo,
    # Python puede usar el codepage de consola en vez de UTF-8 y corromper
    # rutas/nombres con acentos (proyecto y contenido son en espanol).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    parser = build_arg_parser()
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo).resolve() if args.repo else find_repo_root()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")

    try:
        entries = list_worktrees(repo_root)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.worktree:
        target = str(Path(args.worktree).resolve())
        entries = [e for e in entries if str(Path(e["worktree"]).resolve()) == target]
        if not entries:
            print(f"error: no se encontro ese worktree en 'git worktree list': {args.worktree}", file=sys.stderr)
            return 2

    with tempfile.TemporaryDirectory(prefix="gov006_audit_") as tmp:
        temp_root = Path(tmp)
        results = [diagnose_entry(repo_root, e, args.main_ref, temp_root) for e in entries]

    payload = {
        "timestamp": timestamp,
        "repo_root": str(repo_root),
        "main_ref": args.main_ref,
        "results": [asdict(r) for r in results],
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_human(payload)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
