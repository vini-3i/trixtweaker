"""Menu de seguranca."""
from __future__ import annotations
from ..actions.system_ops import act_sec_status, act_sec_wipe
from ..i18n import T
from ..ui.ansi import CY, RD
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import pause
from ..ui.screen import menu_pick


def run() -> None:
    """Loop do menu de seguranca."""
    crumb_push("seguranca")
    try:
        while True:
            op = menu_pick([
                ("1", T("sec_status"), "", CY),
                ("2", T("sec_wipe"), "", RD),
                ("0", T("back"), "", RD),
            ], title=T("sec_title"))
            if op == "0":
                return
            if op == "1":
                act_sec_status()
                pause()
            elif op == "2":
                act_sec_wipe()
                pause()
    finally:
        crumb_pop()
