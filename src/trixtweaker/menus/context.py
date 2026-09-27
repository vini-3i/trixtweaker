"""Menu de contexto do Explorer."""
from __future__ import annotations
from ..actions.context_menu import act_ctx_install, act_ctx_uninstall, ctx_is_installed
from ..i18n import T
from ..ui.ansi import CY, RD
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import pause
from ..ui.screen import menu_pick


def run() -> None:
    """Loop do menu de contexto."""
    crumb_push("contexto")
    try:
        while True:
            status = "instalado" if ctx_is_installed() else "nao instalado"
            op = menu_pick([
                ("1", T("ctx_install"), "adiciona submenu TrixTweaker no botao direito", CY),
                ("2", T("ctx_uninstall"), "remove as chaves do registry", RD),
                ("0", T("back"), "", RD),
            ], title=f"{T('menu_ctx')} · {status}")
            if op == "0":
                return
            if op == "1":
                act_ctx_install()
                pause()
            elif op == "2":
                act_ctx_uninstall()
                pause()
    finally:
        crumb_pop()
