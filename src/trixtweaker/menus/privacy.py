"""Menu de privacidade."""
from __future__ import annotations
from ..actions.privacy import (
    act_priv_ads,
    act_priv_camera_mic,
    act_priv_cortana,
    act_priv_location,
)
from ..i18n import T
from ..ui.ansi import CY, MG, RD
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import ok, pause
from ..ui.screen import menu_pick


def run() -> None:
    """Loop do menu de privacidade."""
    crumb_push("privacidade")
    try:
        while True:
            op = menu_pick([
                ("1", "Desativar Cortana", "", CY),
                ("2", "Desativar ID de publicidade", "", CY),
                ("3", "Desativar rastreamento de localizacao", "", CY),
                ("4", "Bloquear camera e microfone p/ apps", "", CY),
                ("5", T("apply_all"), "", MG),
                ("0", T("back"), "", RD),
            ], title="PRIVACIDADE")
            if op == "0":
                return
            if op == "1":
                act_priv_cortana()
                pause()
            elif op == "2":
                act_priv_ads()
                pause()
            elif op == "3":
                act_priv_location()
                pause()
            elif op == "4":
                act_priv_camera_mic()
                pause()
            elif op == "5":
                for fn in (act_priv_cortana, act_priv_ads, act_priv_location, act_priv_camera_mic):
                    fn()
                ok("pacote de privacidade aplicado")
                pause()
    finally:
        crumb_pop()
