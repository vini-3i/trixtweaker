"""Menu principal interativo."""
from __future__ import annotations
import time
from .. import config
from ..i18n import T, load_prefs
from ..log import cleanup_old_logs, log
from ..system.info import is_admin
from ..ui.ansi import CY, DM, MG, RD, WH, YL, clear
from ..ui.feedback import emit, line, spin
from ..ui.screen import menu_pick, mouse_disable, mouse_enable
from . import av, cleanup, context, discord, experience, games, history, network, performance, prefs, privacy, security, startup, system


def loader() -> None:
    """Exibe sequencia de inicializacao."""
    if config.state.SILENT:
        return
    clear()
    emit()
    emit(" " + MG("TRIX TWEAKER") + DM(f"  ·  v{config.VERSION}") + DM("  ·  inicializando"))
    line("═")
    emit()
    steps = [
        "verificando privilegios",
        "coletando informacoes do sistema",
        "detectando antivirus",
        "preparando pastas de trabalho",
        "verificando criptografia",
        "detectando instalacoes do Discord",
        "carregando modulos de otimizacao",
        "pronto",
    ]
    for s in steps:
        spin(s, 0.4)
    cleanup_old_logs()
    time.sleep(0.3)


MAIN_MENU = {
    "1": ("performance", performance.run),
    "2": ("games", games.run),
    "3": ("discord", discord.run),
    "4": ("experience", experience.run),
    "5": ("cleanup", cleanup.run),
    "6": ("network", network.run),
    "7": ("privacy", privacy.run),
    "8": ("startup", startup.run),
    "9": ("system", system.run),
    "10": ("av", av.run),
    "11": ("history", history.run),
    "12": ("context", context.run),
    "13": ("prefs", prefs.run),
    "14": ("security", security.run),
}


def run() -> None:
    """Loop principal do menu interativo."""
    load_prefs()
    if config.PREFS.get("mouse", True):
        mouse_enable()
    loader()
    if not is_admin() and not config.state.SILENT:
        emit(" " + YL("[!] ") + WH(T("no_admin_warn")))
        emit(" " + DM("    " + T("no_admin_hint")))
        emit(" " + DM("    " + T("no_admin_hint2")))
        emit()
        time.sleep(1.5)
    log("=== sessao iniciada ===")
    try:
        while True:
            lang = config.state.LANG
            op = menu_pick([
                ("1", "DESEMPENHO" if lang == "pt" else "PERFORMANCE",
                 "otimizacoes gerais" if lang == "pt" else "general tweaks", CY),
                ("2", "JOGOS" if lang == "pt" else "GAMES",
                 "menos lag, mais FPS" if lang == "pt" else "less lag, more FPS", CY),
                ("3", "DISCORD", "multi-canal" if lang == "pt" else "multi-channel", CY),
                ("4", T("menu_experience"),
                 "windows mais agradavel" if lang == "pt" else "friendlier windows", CY),
                ("5", "LIMPEZA" if lang == "pt" else "CLEANUP", "temp, cache, logs", CY),
                ("6", "REDE" if lang == "pt" else "NETWORK", "reset, DNS", CY),
                ("7", "PRIVACIDADE" if lang == "pt" else "PRIVACY", "telemetria, ads", CY),
                ("8", "INICIALIZACAO" if lang == "pt" else "STARTUP", "apps do boot", CY),
                ("9", "SISTEMA" if lang == "pt" else "SYSTEM",
                 "info, restore, update, backup", CY),
                ("10", T("menu_av"), "deteccao" if lang == "pt" else "detection", CY),
                ("11", T("menu_history"),
                 "tweaks aplicados" if lang == "pt" else "applied tweaks", CY),
                ("12", T("menu_ctx"),
                 "botao direito no Explorer", CY),
                ("13", T("menu_prefs"), "sound · lang", CY),
                ("14", T("sec_title"), "criptografia" if lang == "pt" else "encryption", CY),
                ("0", "SAIR" if lang == "pt" else "EXIT", "", RD),
            ], title=f"TrixTweaker v{config.VERSION} · " + T("select_cat"),
               footer=f"{T('session_freed')}: {config.state.SESSION_FREED:.1f}")
            if op == "0":
                clear()
                emit(" " + CY(T("bye") + f" · {config.state.SESSION_FREED:.1f} MB"))
                log(f"=== sessao encerrada · freed={config.state.SESSION_FREED:.1f}MB ===")
                time.sleep(0.7)
                return
            entry = MAIN_MENU.get(op)
            if entry:
                entry[1]()
    finally:
        mouse_disable()
