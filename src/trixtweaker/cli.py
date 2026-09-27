"""CLI com argparse: --action/--profile/--install-ctx."""
from __future__ import annotations
import argparse
import sys
from . import config
from .actions import run_action
from .actions.context_menu import ctx_install, ctx_uninstall
from .actions.discord import act_discord_optimize_all
from .i18n import T, load_prefs, load_prefs_lang, save_prefs
from .log import log
from .menus.main_menu import run as run_menu
from .profiles import run_profile
from .security.sanitize import sanitize_log
from .system.info import sys_info
from .ui.ansi import RD, YL, set_title, resize_console
from .ui.feedback import emit
from .ui.screen import mouse_disable


def build_parser() -> argparse.ArgumentParser:
    """Constroi o parser de argumentos."""
    p = argparse.ArgumentParser(prog="trixtweaker", description="TrixTweaker - otimizador geral")
    p.add_argument("--action", help="executa acao direta")
    p.add_argument("--profile", help="executa perfil (gaming/performance/experience/discord/cleanup/privacy/network)")
    p.add_argument("--lang", help="define idioma (pt/en)")
    p.add_argument("--version", "-v", action="store_true", help="mostra versao")
    p.add_argument("--install-ctx", action="store_true", help="instala menu de contexto")
    p.add_argument("--uninstall-ctx", action="store_true", help="remove menu de contexto")
    p.add_argument("--dry-run", action="store_true", help="simula otimizacao do Discord")
    p.add_argument("--silent", action="store_true", help="modo silencioso")
    return p


def main(argv: list[str] | None = None) -> None:
    """Ponto de entrada principal."""
    set_title(f"TrixTweaker · v{config.VERSION}")
    resize_console(112, 42)
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.silent:
        config.state.SILENT = True
    if args.action:
        load_prefs()
        try:
            config.state.INFO = sys_info()
        except Exception:
            config.state.INFO = {}
        rc = run_action(args.action)
        sys.exit(rc)
    if args.version:
        emit(f"TrixTweaker {config.VERSION}")
        return
    if args.install_ctx:
        emit("instalando menu de contexto...")
        emit("ok" if ctx_install() else "falha (rode como admin)")
        return
    if args.uninstall_ctx:
        emit("removendo menu de contexto...")
        emit("ok" if ctx_uninstall() else "falha")
        return
    if args.dry_run:
        config.state.DRY = True
        load_prefs()
        from .menus.main_menu import loader
        loader()
        act_discord_optimize_all(dry=True)
        return
    if args.profile:
        load_prefs()
        from .menus.main_menu import loader
        loader()
        run_profile(args.profile)
        return
    if args.lang:
        load_prefs()
        config.PREFS["lang"] = args.lang
        load_prefs_lang()
        save_prefs()
        emit(f"lang: {config.state.LANG}")
        return
    try:
        config.state.INFO = sys_info()
    except Exception:
        config.state.INFO = {}
    try:
        run_menu()
    except KeyboardInterrupt:
        emit("\n " + YL(T("interrupted")))
        sys.exit(0)
    except Exception as e:
        emit("\n " + RD("[!] ") + f"{T('fatal')}: {sanitize_log(str(e))}")
        log(f"fatal: {sanitize_log(str(e))}")
        try:
            input(" ENTER")
        except Exception:
            pass
        sys.exit(1)
    finally:
        mouse_disable()
