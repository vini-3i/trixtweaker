"""Log em texto e historico cifrado de tweaks."""
from __future__ import annotations
import shutil
from datetime import datetime, timedelta
from . import config
from .security.dpapi import secure_read, secure_write
from .security.sanitize import sanitize_log


def log(msg: object) -> None:
    """Anexa mensagem sanitizada ao log."""
    if config.state.SILENT:
        return
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean = sanitize_log(str(msg))
    try:
        with open(config.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{stamp}] [v{config.VERSION}] {clean}\n")
    except Exception:
        pass


def hist_add(name: object, detail: object = "") -> None:
    """Registra tweak aplicado no historico cifrado."""
    try:
        data = secure_read(config.HISTORY_FILE)
        hist = data.get("items", []) if isinstance(data, dict) else []
        hist.append({
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ver": config.VERSION,
            "name": sanitize_log(str(name))[:120],
            "detail": sanitize_log(str(detail))[:200],
        })
        secure_write(config.HISTORY_FILE, {"items": hist[-500:]})
    except Exception:
        pass


def hist_get() -> list:
    """Retorna lista de itens do historico."""
    data = secure_read(config.HISTORY_FILE)
    return data.get("items", []) if isinstance(data, dict) else []


def cleanup_old_logs() -> None:
    """Rotaciona log grande e limpa backups de registry antigos."""
    try:
        if config.LOG_FILE.exists() and config.LOG_FILE.stat().st_size > 5 * 1024 * 1024:
            bak = config.LOG_FILE.with_suffix(".log.old")
            if bak.exists():
                bak.unlink()
            shutil.move(str(config.LOG_FILE), str(bak))
    except Exception:
        pass
    cutoff = datetime.now() - timedelta(days=30)
    try:
        files = list(config.BACKUP.glob("reg_*.reg"))
    except Exception:
        return
    for f in files:
        try:
            if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                f.unlink()
        except Exception:
            pass
