"""Acoes de limpeza de disco e cache."""
from __future__ import annotations
import os
import re
from pathlib import Path
from .. import config
from ..log import hist_add, log
from ..security.sanitize import safe_path
from ..system.process import run
from ..ui.feedback import ok, spin


def _del_tree_size(base) -> int:
    """Apaga conteudo de um diretorio e retorna bytes liberados."""
    sp = safe_path(base)
    if not sp or not sp.exists():
        return 0
    total = 0
    for f in sp.rglob("*"):
        try:
            if f.is_file():
                total += f.stat().st_size
                f.unlink()
        except Exception:
            pass
    return total


def act_temp() -> None:
    """Limpa arquivos temporarios."""
    spin("limpando temporarios")
    total = 0
    for base in [Path(os.environ.get("TEMP", "")), Path(r"C:\Windows\Temp")]:
        total += _del_tree_size(base)
    mb = total / 1024 / 1024
    config.state.SESSION_FREED += mb
    ok(f"temporarios limpos ({mb:.1f} MB)")
    log(f"temp {total}")
    hist_add("temp")


def act_wu_cache() -> None:
    """Limpa cache do Windows Update."""
    spin("limpando cache do Windows Update")
    run(["net", "stop", "wuauserv"], shell=False)
    total = _del_tree_size(Path(r"C:\Windows\SoftwareDistribution\Download"))
    run(["net", "start", "wuauserv"], shell=False)
    mb = total / 1024 / 1024
    config.state.SESSION_FREED += mb
    ok(f"cache WU limpo ({mb:.1f} MB)")
    log(f"wu {total}")
    hist_add("wu cache")


def act_logs() -> None:
    """Limpa logs de eventos do Windows."""
    spin("limpando logs de eventos")
    rc, out = run("wevtutil el", shell=True, timeout=60)
    count = 0
    for line in out.splitlines():
        line = line.strip()
        if line and re.match(r"^[A-Za-z0-9_\-\\\/\. ]+$", line):
            run(["wevtutil", "cl", line], shell=False, timeout=15)
            count += 1
    ok(f"{count} logs limpos")
    log(f"event logs {count}")
    hist_add("event logs")


def act_lixeira() -> None:
    """Esvazia a lixeira."""
    spin("esvaziando lixeira")
    run('powershell -NoProfile -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"',
        shell=True, timeout=60)
    ok("lixeira vazia")
    log("recycle")
    hist_add("lixeira")


def act_dns() -> None:
    """Limpa cache DNS."""
    spin("limpando DNS", 1)
    run(["ipconfig", "/flushdns"], shell=False)
    ok("cache DNS limpo")
    log("dns")
    hist_add("dns flush")


def act_prefetch() -> None:
    """Limpa pasta prefetch."""
    spin("limpando prefetch")
    p = Path(r"C:\Windows\Prefetch")
    total = 0
    sp = safe_path(p)
    if sp and sp.exists():
        for f in sp.glob("*.pf"):
            try:
                total += f.stat().st_size
                f.unlink()
            except Exception:
                pass
    mb = total / 1024 / 1024
    config.state.SESSION_FREED += mb
    ok(f"prefetch limpo ({mb:.1f} MB)")
    log(f"prefetch {total}")
    hist_add("prefetch")


def act_thumbnails() -> None:
    """Limpa cache de miniaturas do Explorer."""
    spin("limpando cache de miniaturas")
    p = config.LOCALAPPDATA / "Microsoft" / "Windows" / "Explorer"
    total = 0
    sp = safe_path(p)
    if sp and sp.exists():
        for pat in ("thumbcache_*.db", "iconcache_*.db"):
            for f in sp.glob(pat):
                try:
                    total += f.stat().st_size
                    f.unlink()
                except Exception:
                    pass
    mb = total / 1024 / 1024
    config.state.SESSION_FREED += mb
    ok(f"cache de miniaturas limpo ({mb:.1f} MB)")
    log(f"thumbs {total}")
    hist_add("thumbs")


def act_delivery_optimization() -> None:
    """Limpa arquivos de Delivery Optimization."""
    spin("limpando Delivery Optimization")
    p = Path(r"C:\Windows\SoftwareDistribution\DeliveryOptimization")
    total = _del_tree_size(p)
    mb = total / 1024 / 1024
    config.state.SESSION_FREED += mb
    ok(f"delivery optimization limpo ({mb:.1f} MB)")
    log(f"do {total}")
    hist_add("delivery")
