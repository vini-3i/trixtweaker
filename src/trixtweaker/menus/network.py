"""Menu de rede."""
from __future__ import annotations
from ..actions.network import (
    act_rede_dns_cloudflare,
    act_rede_dns_dhcp,
    act_rede_dns_google,
    act_rede_info,
    act_rede_reset,
)
from ..i18n import T
from ..ui.ansi import CY, RD
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import pause
from ..ui.screen import menu_pick


def run() -> None:
    """Loop do menu de rede."""
    crumb_push("rede")
    try:
        while True:
            op = menu_pick([
                ("1", "Resetar stack de rede", "", CY),
                ("2", "Aplicar DNS Cloudflare (1.1.1.1)", "", CY),
                ("3", "Aplicar DNS Google (8.8.8.8)", "", CY),
                ("4", "Voltar DNS para DHCP", "", CY),
                ("5", "Ver informacoes de rede", "", CY),
                ("0", T("back"), "", RD),
            ], title="REDE")
            if op == "0":
                return
            if op == "1":
                act_rede_reset()
                pause()
            elif op == "2":
                act_rede_dns_cloudflare()
                pause()
            elif op == "3":
                act_rede_dns_google()
                pause()
            elif op == "4":
                act_rede_dns_dhcp()
                pause()
            elif op == "5":
                act_rede_info()
                pause()
    finally:
        crumb_pop()
