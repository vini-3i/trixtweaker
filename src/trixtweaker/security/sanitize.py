"""Sanitizacao de caminhos e mensagens de log."""
from __future__ import annotations
import os
import re
from pathlib import Path
from .. import config


def safe_path(p) -> Path | None:
    """Resolve e valida caminho contra roots permitidos."""
    try:
        rp = Path(p).resolve()
    except Exception:
        return None
    try:
        allowed_roots = [config.WORKDIR.resolve(),
                         config.APPDATA.resolve(),
                         config.LOCALAPPDATA.resolve()]
    except Exception:
        return None
    win_roots: list[Path] = []
    for cand in (r"C:\Windows\Temp",
                 r"C:\Windows\SoftwareDistribution",
                 r"C:\Windows\Prefetch"):
        try:
            win_roots.append(Path(cand).resolve())
        except Exception:
            pass
    for root in allowed_roots + win_roots:
        try:
            rp.relative_to(root)
            return rp
        except ValueError:
            continue
    return None


def sanitize_log(msg: str) -> str:
    """Remove nome de usuario e trunca mensagem de log."""
    if not isinstance(msg, str):
        msg = str(msg)
    msg = re.sub(r"C:\\Users\\[^\\]+", r"C:\\Users\\<user>", msg, flags=re.I)
    msg = re.sub(r"[A-Za-z]:\\\\?[^\s]+", lambda m: os.path.basename(m.group(0)), msg)
    return msg[:500]
