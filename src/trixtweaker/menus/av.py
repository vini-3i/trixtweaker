"""Menu de antivirus."""
from __future__ import annotations
import io
import sys
from ..i18n import T
from ..system.av import av_is_active, detect_av
from ..ui.ansi import CY, RD, WH, clear
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import emit, info, ok, pause, spin
from ..ui.screen import SCREEN, menu_pick


def run() -> None:
    """Loop do menu de antivirus."""
    crumb_push("av")
    try:
        while True:
            op = menu_pick([
                ("1", T("av_list"), "", CY),
                ("2", T("av_check_tweak"), "", CY),
                ("0", T("back"), "", RD),
            ], title=T("menu_av"))
            if op == "0":
                return
            if op == "1":
                clear()
                SCREEN.reset()
                buf = io.StringIO()
                SCREEN._render_header(buf)
                sys.stdout.write(buf.getvalue())
                avs = detect_av()
                if avs:
                    ok(f"{T('av_found')}:")
                    for a in avs:
                        emit(" " + WH(" • ") + CY(a))
                else:
                    info(T("av_none"))
                emit()
                info(T("av_warn"))
                pause()
                SCREEN.reset()
            elif op == "2":
                spin(T("av_checking"))
                if av_is_active():
                    info(T("av_ok"))
                    info(T("av_risky"))
                else:
                    info(T("av_none"))
                pause()
    finally:
        crumb_pop()
