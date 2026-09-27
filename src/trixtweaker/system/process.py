"""Execucao centralizada de subprocessos."""
from __future__ import annotations
import re
import subprocess
from ..security.sanitize import sanitize_log


def run(cmd: str | list[str], shell: bool = False, timeout: int = 30) -> tuple[int, str]:
    """Executa um comando e retorna (returncode, output)."""
    try:
        r = subprocess.run(cmd, shell=shell, capture_output=True,
                           text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, sanitize_log(str(e))


def popen(cmd: list[str]):
    """Inicia processo detached (Explorer, Discord, taskmgr)."""
    return subprocess.Popen(cmd)


def service_exists(name: str) -> bool:
    """Verifica se um servico do Windows existe (whitelist regex)."""
    if not re.match(r"^[A-Za-z0-9_\-]{1,64}$", name or ""):
        return False
    rc, _ = run(["sc", "query", name], shell=False, timeout=5)
    return rc == 0
