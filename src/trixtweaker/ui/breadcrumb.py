"""Breadcrumb de navegacao dos menus."""
from __future__ import annotations

_CRUMB: list[str] = ["inicio"]


def crumb_push(name: str) -> None:
    """Empilha um nivel no breadcrumb."""
    _CRUMB.append(name)


def crumb_pop() -> None:
    """Desempilha um nivel do breadcrumb."""
    if len(_CRUMB) > 1:
        _CRUMB.pop()


def crumb_str() -> str:
    """Retorna o breadcrumb como string."""
    return " › ".join(_CRUMB)
