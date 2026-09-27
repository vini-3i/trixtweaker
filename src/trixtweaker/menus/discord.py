"""Menu do Discord."""
from __future__ import annotations
from .. import config
from ..actions.discord import (
    act_discord_launch,
    act_discord_optimize_all,
    act_discord_optimize_one,
    act_discord_restore,
    act_discord_update,
    discord_channels,
)
from ..i18n import T
from ..ui.ansi import CY, MG, RD
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import pause
from ..ui.screen import menu_pick


def run() -> None:
    """Loop do menu Discord."""
    crumb_push("discord")
    try:
        while True:
            chans = discord_channels()
            opts = []
            for key, label, _ in chans:
                opts.append((key, f"Otimizar {label}", "", CY))
            opts += [
                ("x", "Otimizar TODOS os canais instalados", "", MG),
                ("l1", "Iniciar Discord (stable)", "", CY),
                ("l2", "Iniciar Discord PTB", "", CY),
                ("l3", "Iniciar Discord Canary", "", CY),
                ("u", "Forcar atualizacao (stable)", "", CY),
                ("r", "Restaurar backup", "", MG),
                ("0", T("back"), "", RD),
            ]
            footer = f"canais: {', '.join(l for _, l, _ in chans) or 'nenhum'}"
            op = menu_pick(opts, title="DISCORD · multi-canal", footer=footer)
            if op == "0":
                return
            if op == "x":
                act_discord_optimize_all()
                pause()
            elif op == "l1":
                act_discord_launch("stable")
                pause()
            elif op == "l2":
                act_discord_launch("ptb")
                pause()
            elif op == "l3":
                act_discord_launch("canary")
                pause()
            elif op == "u":
                act_discord_update("stable")
                pause()
            elif op == "r":
                act_discord_restore()
                pause()
            elif op in config.DISCORD_DIRS:
                act_discord_optimize_one(op)
                pause()
    finally:
        crumb_pop()
