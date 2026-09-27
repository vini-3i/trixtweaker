"""Renderizacao de tela e navegacao por setas."""
from __future__ import annotations
import ctypes
import io
import os
import sys
import time
from .. import config
from ..i18n import T
from ..system.info import is_admin, sys_info
from .ansi import BLD, CY, DM, GR, MG, WH, clear
from .beep import beep
from .breadcrumb import crumb_str

_OLD_CONSOLE_MODE = None


def mouse_enable() -> bool:
    """Habilita input estendido sem processar mouse no menu."""
    global _OLD_CONSOLE_MODE
    if os.name != "nt":
        return False
    try:
        k = ctypes.windll.kernel32
        h = k.GetStdHandle(-10)
        mode = ctypes.c_uint()
        k.GetConsoleMode(h, ctypes.byref(mode))
        _OLD_CONSOLE_MODE = mode.value
        new_mode = mode.value | 0x0080
        new_mode &= ~0x0040
        k.SetConsoleMode(h, new_mode)
        return True
    except Exception:
        return False


def mouse_disable() -> None:
    """Restaura o modo original do console."""
    if os.name != "nt" or _OLD_CONSOLE_MODE is None:
        return
    try:
        k = ctypes.windll.kernel32
        h = k.GetStdHandle(-10)
        k.SetConsoleMode(h, _OLD_CONSOLE_MODE)
    except Exception:
        pass


def read_key(timeout: float = 0.03) -> str:
    """Le apenas teclas; eventos de mouse sao consumidos e ignorados."""
    if os.name != "nt":
        import select
        import termios
        import tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            r, _, _ = select.select([sys.stdin], [], [], timeout)
            if not r:
                return ""
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                r2, _, _ = select.select([sys.stdin], [], [], 0.01)
                if r2:
                    ch2 = sys.stdin.read(2)
                    return {"[A": "UP", "[B": "DOWN", "[C": "RIGHT", "[D": "LEFT"}.get(ch2, "ESC")
                return "ESC"
            if ch in ("\r", "\n"):
                return "ENTER"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    import msvcrt
    if not msvcrt.kbhit():
        time.sleep(timeout)
        return ""
    ch = msvcrt.getch()
    if ch in (b"\x00", b"\xe0"):
        if not msvcrt.kbhit():
            return ""
        ch2 = msvcrt.getch()
        mapping = {
            b"H": "UP", b"P": "DOWN", b"K": "LEFT", b"M": "RIGHT",
            b"I": "PGUP", b"Q": "PGDN", b"G": "HOME", b"O": "END",
        }
        if ch2 in mapping:
            return mapping[ch2]
        if ch2 == b"\x00":
            try:
                deadline = time.time() + 0.03
                while time.time() < deadline and msvcrt.kbhit():
                    msvcrt.getch()
            except Exception:
                pass
        return ""
    if ch in (b"\r", b"\n"):
        return "ENTER"
    if ch == b"\x1b":
        return "ESC"
    if ch == b"\x03":
        raise KeyboardInterrupt
    if ch == b"\x08":
        return "BACKSPACE"
    try:
        return ch.decode("utf-8", errors="ignore")
    except Exception:
        return ""


class Screen:
    """Renderiza menus com reposicionamento de cursor."""

    def __init__(self) -> None:
        self.first_draw = True

    def _render_header(self, buf) -> None:
        """Escreve o cabecalho com infos do sistema."""
        inf = config.state.INFO or sys_info()
        buf.write("\n")
        buf.write(" " + MG("TRIX TWEAKER") + DM(f"  v{config.VERSION}") + DM(f"  ·  {T('app_sub')}") + "\n")
        buf.write(" " + DM("─" * 62) + "\n")
        buf.write(" " + CY(f"{T('user')}: ") + WH(inf["user"]) +
                  DM(" | ") + CY(f"{T('pc')}: ") + WH(inf["pc"]) +
                  DM(" | ") + CY(f"{T('os')}: ") + WH(f"{inf['os']} {inf['build']}") + "\n")
        buf.write(" " + CY("CPU: ") + WH(inf["cpu"][:52]) + "\n")
        admin = GR(T("admin_yes")) if is_admin() else YL(T("admin_no"))
        freed = f"{config.state.SESSION_FREED:.1f} MB" if config.state.SESSION_FREED else "0 MB"
        buf.write(" " + CY("RAM: ") + WH(inf["ram"]) +
                  DM(" | ") + CY("GPU: ") + WH(inf["gpu"][:34]) +
                  DM(" | ") + CY(f"{T('admin')}: ") + admin +
                  DM(" | ") + CY(f"{T('freed')}: ") + WH(freed) + "\n")
        buf.write(" " + DM("─" * 62) + "\n")

    def draw(self, options, title=None, footer=None, idx: int = 0) -> None:
        """Desenha opcoes do menu com destaque no indice atual."""
        buf = io.StringIO()
        self._render_header(buf)
        buf.write("\n")
        buf.write(" " + DM(f"{T('path')}: ") + CY(crumb_str()) + "\n")
        buf.write("\n")
        if title:
            buf.write(" " + MG(title) + "\n")
            buf.write(" " + DM("─" * 62) + "\n")
        for i, (key, label, hint, color) in enumerate(options):
            pointer = "▶" if i == idx else " "
            lbl = BLD(label) if i == idx else WH(label)
            hint_str = DM("  " + hint) if hint else ""
            buf.write(f" {CY(pointer)} {lbl}{hint_str}\n")
        buf.write("\n")
        if footer:
            buf.write(" " + DM(footer) + "\n")
        buf.write("\n")
        buf.write(" " + DM(T("help_bar")) + "\n")
        buf.write("\n")
        text = buf.getvalue()
        if self.first_draw:
            clear()
            self.first_draw = False
        sys.stdout.write("\033[H\033[J")
        sys.stdout.write(text)
        sys.stdout.flush()

    def reset(self) -> None:
        """Forca limpeza total no proximo draw."""
        self.first_draw = True


SCREEN = Screen()


def _menu_pick_impl(options, title=None, footer=None) -> str:
    """Loop de navegacao por setas ate ENTER ou ESC."""
    idx = 0
    n = len(options)
    SCREEN.draw(options, title, footer, idx)
    while True:
        key = read_key(0.03)
        if not key:
            continue
        moved = False
        if key == "UP":
            new = (idx - 1) % n
            if new != idx:
                idx = new
                moved = True
        elif key == "DOWN":
            new = (idx + 1) % n
            if new != idx:
                idx = new
                moved = True
        elif key == "PGUP":
            new = max(0, idx - 5)
            if new != idx:
                idx = new
                moved = True
        elif key == "PGDN":
            new = min(n - 1, idx + 5)
            if new != idx:
                idx = new
                moved = True
        elif key == "HOME":
            if idx != 0:
                idx = 0
                moved = True
        elif key == "END":
            if idx != n - 1:
                idx = n - 1
                moved = True
        elif key == "ENTER":
            beep("open")
            return options[idx][0]
        elif key == "ESC":
            beep("back")
            return "0"
        if moved:
            beep("nav")
            SCREEN.draw(options, title, footer, idx)


def menu_pick(options, title=None, footer=None) -> str:
    """Exibe menu navegavel e retorna a chave escolhida."""
    SCREEN.reset()
    return _menu_pick_impl(options, title, footer)
