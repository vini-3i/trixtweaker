"""Checagem e aplicacao de atualizacoes remotas."""
from __future__ import annotations
import hashlib
import re
import shutil
import tempfile
import urllib.request
from pathlib import Path
from . import config
from .i18n import T
from .log import log
from .security.sanitize import sanitize_log
from .ui.feedback import confirm, fail, info, ok, spin

UPDATE_URL = config.UPDATE_URL


def _download_update(url: str, expected_sha256: str) -> None:
    """Baixa o executavel novo e valida sha256."""
    spin("baixando atualizacao", 1)
    try:
        tmp = Path(tempfile.gettempdir()) / "TrixTweaker_new.exe"
        req = urllib.request.Request(url,
                                     headers={"User-Agent": f"TrixTweaker/{config.VERSION}"})
        with urllib.request.urlopen(req, timeout=60) as r, open(tmp, "wb") as f:
            shutil.copyfileobj(r, f)
        if expected_sha256:
            h = hashlib.sha256()
            with open(tmp, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            if h.hexdigest().lower() != expected_sha256.lower():
                fail(T("update_hash_bad"))
                tmp.unlink(missing_ok=True)
                return
            ok(T("update_hash_ok"))
        ok(f"baixado: {tmp}")
        info("feche o TrixTweaker e execute o novo arquivo")
    except Exception as e:
        fail(f"falha no download: {sanitize_log(str(e))}")


def check_update() -> None:
    """Checa version.txt remoto e oferece download."""
    spin(T("update_check"))
    url = config.UPDATE_URL
    if not url:
        from .ui.feedback import skip
        skip(T("update_url_missing"))
        return
    if not url.lower().startswith("https://"):
        fail(T("update_url_invalid"))
        return
    try:
        req = urllib.request.Request(url,
                                     headers={"User-Agent": f"TrixTweaker/{config.VERSION}"})
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode("utf-8", errors="replace").strip().splitlines()
        if not raw:
            fail("resposta vazia")
            return
        remote_ver = raw[0].strip()
        remote_url = raw[1].strip() if len(raw) > 1 else ""
        remote_hash = ""
        remote_notes = ""
        for line in raw[2:]:
            low = line.lower()
            if low.startswith("sha256:"):
                remote_hash = line.split(":", 1)[1].strip()
            elif low.startswith("notas:") or low.startswith("notes:"):
                remote_notes = line.split(":", 1)[1].strip()
        if not re.match(r"^\d+\.\d+\.\d+$", remote_ver):
            fail("versao remota invalida")
            return
        if remote_url and not remote_url.lower().startswith("https://"):
            fail("url de download deve ser https")
            return
        if remote_hash and not re.match(r"^[a-fA-F0-9]{64}$", remote_hash):
            fail("hash invalido")
            return
        if remote_ver == config.VERSION:
            ok(f"{T('update_current')} ({config.VERSION})")
            return
        info(f"{T('update_available')}: {remote_ver} ({config.VERSION})")
        if remote_notes:
            info(f"notas: {remote_notes}")
        if remote_url and confirm(T("update_download")):
            _download_update(remote_url, remote_hash)
    except Exception as e:
        fail(f"falha ao checar: {sanitize_log(str(e))}")
    log("update check")
