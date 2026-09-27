"""Menu de jogos."""
from __future__ import annotations
from ..actions.games import (
    JOGOS,
    act_dvr,
    act_game_mode,
    act_gpu,
    act_jogo,
    act_nagle,
    act_prioridade,
    act_shaders,
    act_tcp,
)
from ..i18n import T
from ..ui.ansi import CY, MG, RD
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import ok, pause
from ..ui.screen import menu_pick


def run_list() -> None:
    """Loop da lista de jogos."""
    crumb_push("lista")
    try:
        while True:
            opts = [(k, v[0], "", CY) for k, v in JOGOS.items()]
            opts.append(("0", T("back"), "", RD))
            op = menu_pick(opts, title="LISTA DE JOGOS")
            if op == "0":
                return
            if op in JOGOS:
                nome, exes = JOGOS[op]
                act_jogo(nome, exes)
                pause()
    finally:
        crumb_pop()


def run() -> None:
    """Loop do menu de jogos."""
    crumb_push("jogos")
    try:
        while True:
            op = menu_pick([
                ("1", "Game Mode + Game Bar", "", CY),
                ("2", "Desativar DVR / gravacao", "", CY),
                ("3", "Ajustar rede p/ ping baixo", "", CY),
                ("4", "Desativar Nagle (TCPNoDelay)", "", CY),
                ("5", "Prioridade alta p/ jogos", "", CY),
                ("6", "Otimizar GPU / overlays", "", CY),
                ("7", "Limpar cache de shaders", "", CY),
                ("8", "Lista de jogos para otimizar", "", MG),
                ("9", T("apply_all"), "", MG),
                ("0", T("back"), "", RD),
            ], title="JOGOS · menos lag, mais FPS")
            if op == "0":
                return
            if op == "1":
                act_game_mode()
                pause()
            elif op == "2":
                act_dvr()
                pause()
            elif op == "3":
                act_tcp()
                pause()
            elif op == "4":
                act_nagle()
                pause()
            elif op == "5":
                act_prioridade()
                pause()
            elif op == "6":
                act_gpu()
                pause()
            elif op == "7":
                act_shaders()
                pause()
            elif op == "8":
                run_list()
            elif op == "9":
                for fn in (act_game_mode, act_dvr, act_tcp, act_nagle,
                           act_prioridade, act_gpu):
                    fn()
                ok("pacote de jogos aplicado")
                pause()
    finally:
        crumb_pop()
