"""Helpers de cor ANSI e controle do console."""
from __future__ import annotations
import ctypes
import os
import sys

if sys.platform == "win32":
    os.system("")
    try:
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7
        )
    except Exception:
        pass

E = "\033["


def C(c, t) -> str:
    """Envolve texto em codigo ANSI."""
    return f"{E}{c}m{t}{E}0m"


def CY(t) -> str:
    """Ciano."""
    return C("96", t)


def MG(t) -> str:
    """Magenta."""
    return C("95", t)


def GR(t) -> str:
    """Verde."""
    return C("92", t)


def YL(t) -> str:
    """Amarelo."""
    return C("93", t)


def RD(t) -> str:
    """Vermelho."""
    return C("91", t)


def DM(t) -> str:
    """Cinza escuro."""
    return C("90", t)


def WH(t) -> str:
    """Branco."""
    return C("97", t)


def BLD(t) -> str:
    """Branco negrito."""
    return C("97;1", t)


def set_title(t: str) -> None:
    """Define o titulo da janela do console."""
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(t)
    except Exception:
        pass


def resize_console(cols: int = 112, lines: int = 42) -> None:
    """Redimensiona a janela do console."""
    try:
        os.system(f"mode con: cols={cols} lines={lines}")
    except Exception:
        pass


def clear() -> None:
    """Limpa a tela do console."""
    os.system("cls" if os.name == "nt" else "clear")
