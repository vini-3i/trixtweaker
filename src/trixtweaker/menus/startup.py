"""Menu de inicializacao."""
from __future__ import annotations
from ..actions.startup import (
    act_boot_disable_onedrive,
    act_boot_disable_teams,
    act_boot_listar,
)
from ..i18n import T
from ..ui.ansi import CY, RD
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import pause
from ..ui.screen import menu_pick


def run() -> None:
    """Loop do menu de inicializacao."""
    crumb_push("inicializacao")
    try:
        while True:
            op = menu_pick([
                ("1", "Listar programas de inicializacao", "", CY),
                ("2", "Remover OneDrive do boot", "", CY),
                ("3", "Remover Teams do boot", "", CY),
                ("0", T("back"), "", RD),
            ], title="INICIALIZACAO")
            if op == "0":
                return
            if op == "1":
                act_boot_listar()
                pause()
            elif op == "2":
                act_boot_disable_onedrive()
                pause()
            elif op == "3":
                act_boot_disable_teams()
                pause()
    finally:
        crumb_pop()
