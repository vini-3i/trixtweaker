"""Sons de navegacao em thread separada."""
from __future__ import annotations
import threading
import time
from .. import config


def beep(kind: str = "nav") -> None:
    """Emite beep conforme preferencia de som."""
    if config.state.SILENT:
        return
    if not config.PREFS.get("sound", True):
        return

    def _p() -> None:
        try:
            import winsound
            if kind == "nav":
                winsound.Beep(1200, 25)
            elif kind == "ok":
                winsound.Beep(1600, 40)
                time.sleep(0.05)
                winsound.Beep(2000, 40)
            elif kind == "back":
                winsound.Beep(800, 40)
            elif kind == "err":
                winsound.Beep(400, 80)
            elif kind == "open":
                winsound.Beep(1800, 30)
        except Exception:
            pass

    threading.Thread(target=_p, daemon=True).start()
