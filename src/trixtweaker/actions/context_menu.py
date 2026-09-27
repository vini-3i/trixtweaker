"""Menu de contexto do Explorer (Win10 + Win11)."""
from __future__ import annotations
import sys
from pathlib import Path
from .. import config
from ..i18n import T
from ..system.registry import reg_delete_tree, reg_exists, reg_set
from ..log import hist_add, log
from ..ui.feedback import fail, info, ok, spin

CTX_ITEMS = [
    ("01_cleanup", "Limpeza rapida", "cleanup"),
    ("02_temp", "Limpar temp", "temp"),
    ("03_logs", "Limpar logs", "logs"),
    ("04_dns", "Limpar DNS", "dns"),
    ("05_trash", "Esvaziar lixeira", "trash"),
    ("06_shaders", "Limpar shader cache", "shaders"),
    ("07_discord", "Otimizar Discord", "discord"),
    ("08_exp", "Aplicar experiencia", "experience"),
]

CTX_STORE = r"TrixTweakerContextMenu"
CTX_BASES = [
    r"Directory\Background\shell\TrixTweaker",
    r"Directory\shell\TrixTweaker",
    r"DesktopBackground\Shell\TrixTweaker",
]


def _self_exe() -> str:
    """Retorna o executavel atual (ou script em modo dev)."""
    if getattr(sys, "frozen", False):
        return str(Path(sys.executable).resolve())
    return str(Path(__file__).resolve().parents[3] / "trixtweaker.py")


def ctx_is_installed() -> bool:
    """Verifica se o menu de contexto esta instalado."""
    return reg_exists(f"HKCR\\{CTX_BASES[0]}")


def ctx_install() -> bool:
    """Instala menu de contexto via ExtendedSubCommandsKey."""
    try:
        exe = _self_exe()
        ok_flag = True

        def _set(path: str, name: str, value: str) -> None:
            nonlocal ok_flag
            good, _ = reg_set(path, name, value, "SZ")
            if not good:
                ok_flag = False

        store_path = f"HKCR\\{CTX_STORE}\\shell"
        for key, label, action in CTX_ITEMS:
            sub = f"{store_path}\\{key}"
            _set(sub, "", label)
            _set(sub, "Icon", exe)
            _set(f"{sub}\\command", "", f'"{exe}" --action {action} --silent')
        for base in CTX_BASES:
            full = f"HKCR\\{base}"
            _set(full, "MUIVerb", "TrixTweaker")
            _set(full, "Icon", exe)
            _set(full, "ExtendedSubCommandsKey", CTX_STORE)
            _set(full, "SubCommands", "")
        return ok_flag
    except Exception:
        return False


def ctx_uninstall() -> bool:
    """Remove o menu de contexto do registry."""
    try:
        ok_flag = True
        for base in CTX_BASES:
            if not reg_delete_tree(f"HKCR\\{base}"):
                ok_flag = False
        if not reg_delete_tree(f"HKCR\\{CTX_STORE}"):
            ok_flag = False
        return ok_flag
    except Exception:
        return False


def act_ctx_install() -> None:
    """Instala o menu de contexto com feedback."""
    spin("instalando menu de contexto")
    if ctx_install():
        ok(T("ctx_installed"))
        info(T("ctx_hint"))
        if config.state.INFO.get("build", 0) >= 22000:
            info(T("ctx_win11_note"))
        hist_add("ctx install")
        log("ctx install")
    else:
        fail("falha (precisa admin)")


def act_ctx_uninstall() -> None:
    """Remove o menu de contexto com feedback."""
    spin("removendo menu de contexto")
    if ctx_uninstall():
        ok(T("ctx_removed"))
        hist_add("ctx uninstall")
        log("ctx uninstall")
    else:
        fail("falha")
