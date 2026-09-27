"""Menu de experiencia do Windows."""
from __future__ import annotations
from ..actions.experience import (
    act_exp_ads,
    act_exp_anim,
    act_exp_ctx,
    act_exp_explorer_open,
    act_exp_ext,
    act_exp_lockscreen,
    act_exp_seconds,
    act_exp_start_rec,
    act_exp_start_tips,
    act_exp_timeline,
    act_exp_widgets,
)
from ..i18n import T
from ..ui.ansi import CY, MG, RD
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import ok, pause
from ..ui.screen import menu_pick


def run() -> None:
    """Loop do menu de experiencia."""
    crumb_push("experiencia")
    try:
        while True:
            op = menu_pick([
                ("1", T("exp_anim"), "", CY),
                ("2", T("exp_widgets"), "", CY),
                ("3", T("exp_explorer_open"), "", CY),
                ("4", T("exp_ext"), "", CY),
                ("5", T("exp_ctx"), "", CY),
                ("6", T("exp_start_rec"), "", CY),
                ("7", T("exp_start_tips"), "", CY),
                ("8", T("exp_ads"), "", CY),
                ("9", T("exp_timeline"), "", CY),
                ("10", T("exp_lockscreen"), "", CY),
                ("11", T("exp_seconds"), "", CY),
                ("12", T("exp_all"), "", MG),
                ("0", T("back"), "", RD),
            ], title=T("menu_experience"))
            if op == "0":
                return
            if op == "1":
                act_exp_anim()
                pause()
            elif op == "2":
                act_exp_widgets()
                pause()
            elif op == "3":
                act_exp_explorer_open()
                pause()
            elif op == "4":
                act_exp_ext()
                pause()
            elif op == "5":
                act_exp_ctx()
                pause()
            elif op == "6":
                act_exp_start_rec()
                pause()
            elif op == "7":
                act_exp_start_tips()
                pause()
            elif op == "8":
                act_exp_ads()
                pause()
            elif op == "9":
                act_exp_timeline()
                pause()
            elif op == "10":
                act_exp_lockscreen()
                pause()
            elif op == "11":
                act_exp_seconds()
                pause()
            elif op == "12":
                for fn in (act_exp_anim, act_exp_widgets, act_exp_explorer_open,
                           act_exp_ext, act_exp_ctx, act_exp_start_rec,
                           act_exp_start_tips, act_exp_ads, act_exp_timeline,
                           act_exp_lockscreen, act_exp_seconds):
                    fn()
                ok("pacote de experiencia aplicado")
                pause()
    finally:
        crumb_pop()
