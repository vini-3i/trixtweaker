"""Feedback visual: spin, ok, fail, confirm, pause."""
from __future__ import annotations
import sys
import time
from .. import config
from ..i18n import T
from .ansi import CY, DM, GR, MG, RD, WH, YL
from .beep import beep

SPIN = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def spin(text: str, seconds: float = 2.0, dry: bool = False) -> None:
    """Exibe spinner animado durante operacoes."""
    if config.state.SILENT:
        return
    if dry:
        tag = T("dry")
        print(f" {MG(f'[{tag}]')} {DM(text)}")
        return
    end = time.time() + seconds
    i = 0
    while time.time() < end:
        f = SPIN[i % len(SPIN)]
        sys.stdout.write(f"\r {CY(f)} {DM(text)}      ")
        sys.stdout.flush()
        time.sleep(0.06)
        i += 1
    tag = T("ok")
    sys.stdout.write(f"\r {GR(f'[{tag}]')} {WH(text)}                    \n")
    sys.stdout.flush()


def ok(t) -> None:
    """Imprime mensagem de sucesso."""
    if config.state.SILENT:
        return
    tag = T("ok")
    print(f" {GR(f'[{tag}]')} {WH(t)}")
    beep("ok")


def skip(t) -> None:
    """Imprime mensagem de item pulado."""
    if config.state.SILENT:
        return
    tag = T("skipped")
    print(f" {YL(f'[{tag}]')} {DM(t)}")


def fail(t) -> None:
    """Imprime mensagem de falha."""
    if config.state.SILENT:
        return
    tag = T("failed")
    print(f" {RD(f'[{tag}]')} {WH(t)}")
    beep("err")


def info(t) -> None:
    """Imprime mensagem informativa."""
    if config.state.SILENT:
        return
    print(f" {CY('[..]')} {DM(t)}")


def dry(t) -> None:
    """Imprime mensagem de dry-run."""
    if config.state.SILENT:
        return
    tag = T("dry")
    print(f" {MG(f'[{tag}]')} {DM(t)}")


def emit(text: str = "") -> None:
    """Imprime texto cru sem formato (listagens e relatorios)."""
    if config.state.SILENT:
        return
    print(text)


def line(char: str = "─", n: int = 62, color=DM) -> None:
    """Imprime linha separadora."""
    print(" " + color(char * n))


def pause(msg=None) -> None:
    """Aguarda ENTER do usuario."""
    if config.state.SILENT:
        return
    if msg is None:
        msg = T("pause")
    print()
    try:
        input(" " + DM(msg))
    except (EOFError, KeyboardInterrupt):
        pass


def confirm(msg=None) -> bool:
    """Pede confirmacao s/N ao usuario."""
    if msg is None:
        msg = T("confirm")
    try:
        prompt = "[s/N]" if config.state.LANG == "pt" else "[y/N]"
        r = input(f" {YL('?')} {WH(msg)} {DM(prompt)} ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    if config.state.LANG == "pt":
        return r in ("s", "sim", "y", "yes")
    return r in ("y", "yes", "s", "sim")
