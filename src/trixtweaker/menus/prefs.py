"""Menu de preferencias."""
from __future__ import annotations
from .. import config
from ..i18n import T, load_prefs_lang, save_prefs
from ..ui.ansi import CY, RD
from ..ui.beep import beep
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.screen import menu_pick, mouse_disable, mouse_enable


def run() -> None:
    """Loop do menu de preferencias."""
    crumb_push("prefs")
    try:
        while True:
            snd = T("sound_on") if config.PREFS["sound"] else T("sound_off")
            mou = T("enable") if config.PREFS["mouse"] else T("disable")
            lng = "PT-BR" if config.PREFS["lang"] == "pt" else "EN-US"
            op = menu_pick([
                ("1", f"{T('prefs_sound')}: {snd}", "", CY),
                ("2", f"{T('prefs_lang')}: {lng}", "", CY),
                ("3", f"{T('prefs_mouse')}: {mou}", "", CY),
                ("0", T("back"), "", RD),
            ], title=T("menu_prefs"))
            if op == "0":
                return
            if op == "1":
                config.PREFS["sound"] = not config.PREFS["sound"]
                save_prefs()
                beep("open")
            elif op == "2":
                config.PREFS["lang"] = "en" if config.PREFS["lang"] == "pt" else "pt"
                load_prefs_lang()
                save_prefs()
                beep("open")
            elif op == "3":
                config.PREFS["mouse"] = not config.PREFS["mouse"]
                save_prefs()
                if config.PREFS["mouse"]:
                    mouse_enable()
                else:
                    mouse_disable()
                beep("open")
    finally:
        crumb_pop()
