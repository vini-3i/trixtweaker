"""Acoes de inicializacao do Windows."""
from __future__ import annotations
from ..log import hist_add, log
from ..system.process import run
from ..system.registry import reg_set
from ..ui.ansi import DM
from ..ui.feedback import emit, ok, spin


def act_boot_listar() -> None:
    """Lista programas de inicializacao."""
    spin("lendo programas de inicializacao")
    rc, out = run('wmic startup get Caption,Command,Location', shell=True, timeout=15)
    emit()
    for line in out.splitlines():
        line = line.strip()
        if line and not line.startswith("Caption"):
            emit(f" {DM(line[:100])}")
    log("startup listed")


def act_boot_disable_onedrive() -> None:
    """Remove OneDrive da inicializacao."""
    spin("desativando OneDrive da inicializacao")
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run", "OneDrive", "")
    ok("OneDrive removido do boot")
    log("onedrive off")
    hist_add("onedrive off")


def act_boot_disable_teams() -> None:
    """Remove Teams da inicializacao."""
    spin("desativando Teams da inicializacao")
    for k in ("com.squirrel.Teams.Teams", "Teams", "MicrosoftTeams"):
        reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run", k, "")
    ok("Teams removido do boot")
    log("teams off")
    hist_add("teams off")
