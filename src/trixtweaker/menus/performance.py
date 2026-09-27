"""Menu de desempenho."""
from __future__ import annotations
from ..actions.performance import (
    act_animacoes,
    act_apps_bg,
    act_efeitos,
    act_energia,
    act_memoria,
    act_power_ultimate,
    act_search,
    act_sysmain,
    act_telemetria,
    act_visual_compact,
)
from ..i18n import T
from ..ui.ansi import CY, MG, RD
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import ok, pause
from ..ui.screen import menu_pick


def run() -> None:
    """Loop do menu de desempenho."""
    crumb_push("desempenho")
    try:
        while True:
            op = menu_pick([
                ("1", "Plano de energia alto desempenho", "", CY),
                ("2", "Habilitar plano Ultimate", "", CY),
                ("3", "Desativar telemetria e coleta", "", CY),
                ("4", "Desativar animacoes do Windows", "", CY),
                ("5", "Efeitos visuais para performance", "", CY),
                ("6", "Desativar SysMain / Superfetch", "", CY),
                ("7", "Desativar Windows Search", "", CY),
                ("8", "Otimizar memoria e cache", "", CY),
                ("9", "Desativar apps em segundo plano", "", CY),
                ("10", "Modo compacto do Explorer", "", CY),
                ("11", T("apply_all"), "", MG),
                ("0", T("back"), "", RD),
            ], title="DESEMPENHO DO PC")
            if op == "0":
                return
            if op == "1":
                act_energia()
                pause()
            elif op == "2":
                act_power_ultimate()
                pause()
            elif op == "3":
                act_telemetria()
                pause()
            elif op == "4":
                act_animacoes()
                pause()
            elif op == "5":
                act_efeitos()
                pause()
            elif op == "6":
                act_sysmain()
                pause()
            elif op == "7":
                act_search()
                pause()
            elif op == "8":
                act_memoria()
                pause()
            elif op == "9":
                act_apps_bg()
                pause()
            elif op == "10":
                act_visual_compact()
                pause()
            elif op == "11":
                for fn in (act_energia, act_telemetria, act_animacoes, act_efeitos,
                           act_sysmain, act_memoria, act_apps_bg):
                    fn()
                ok("pacote de desempenho aplicado")
                pause()
    finally:
        crumb_pop()
