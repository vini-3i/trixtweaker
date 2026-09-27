"""Menu de limpeza."""
from __future__ import annotations
from ..actions.cleanup import (
    act_delivery_optimization,
    act_dns,
    act_lixeira,
    act_logs,
    act_prefetch,
    act_temp,
    act_thumbnails,
    act_wu_cache,
)
from ..i18n import T
from ..ui.ansi import CY, MG, RD
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import ok, pause
from ..ui.screen import menu_pick


def run() -> None:
    """Loop do menu de limpeza."""
    crumb_push("limpeza")
    try:
        while True:
            op = menu_pick([
                ("1", "Limpar arquivos temporarios", "", CY),
                ("2", "Limpar cache do Windows Update", "", CY),
                ("3", "Limpar logs de eventos", "", CY),
                ("4", "Esvaziar lixeira", "", CY),
                ("5", "Limpar cache DNS", "", CY),
                ("6", "Limpar prefetch", "", CY),
                ("7", "Limpar cache de miniaturas", "", CY),
                ("8", "Limpar Delivery Optimization", "", CY),
                ("9", T("apply_all"), "", MG),
                ("0", T("back"), "", RD),
            ], title="LIMPEZA")
            if op == "0":
                return
            if op == "1":
                act_temp()
                pause()
            elif op == "2":
                act_wu_cache()
                pause()
            elif op == "3":
                act_logs()
                pause()
            elif op == "4":
                act_lixeira()
                pause()
            elif op == "5":
                act_dns()
                pause()
            elif op == "6":
                act_prefetch()
                pause()
            elif op == "7":
                act_thumbnails()
                pause()
            elif op == "8":
                act_delivery_optimization()
                pause()
            elif op == "9":
                for fn in (act_temp, act_wu_cache, act_logs, act_lixeira,
                           act_dns, act_prefetch, act_thumbnails, act_delivery_optimization):
                    fn()
                ok("pacote de limpeza aplicado")
                pause()
    finally:
        crumb_pop()
