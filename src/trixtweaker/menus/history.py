"""Menu de historico."""
from __future__ import annotations
import io
import sys
from .. import config
from ..i18n import T
from ..log import hist_get
from ..ui.ansi import CY, DM, RD, clear
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import emit, fail, info, ok, pause
from ..ui.screen import SCREEN, menu_pick


def run() -> None:
    """Loop do menu de historico."""
    crumb_push("historico")
    try:
        while True:
            op = menu_pick([
                ("1", T("history_show"), "", CY),
                ("2", T("history_clear"), "", CY),
                ("0", T("back"), "", RD),
            ], title=T("menu_history"))
            if op == "0":
                return
            if op == "1":
                clear()
                SCREEN.reset()
                buf = io.StringIO()
                SCREEN._render_header(buf)
                sys.stdout.write(buf.getvalue())
                hist = hist_get()
                if not hist:
                    info(T("history_empty"))
                else:
                    for h in hist[-30:]:
                        emit(" " + DM(h.get("ts", "?")) + "  " +
                             CY(h.get("name", "?")) + "  " +
                             DM(h.get("detail", "")))
                pause()
                SCREEN.reset()
            elif op == "2":
                try:
                    if config.HISTORY_FILE.exists():
                        config.HISTORY_FILE.unlink()
                    ok("historico limpo")
                except Exception:
                    fail("falha")
                pause()
    finally:
        crumb_pop()
