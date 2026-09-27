"""Registra menu de contexto standalone (sem abrir o menu)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from trixtweaker.actions.context_menu import ctx_install
from trixtweaker.system.info import sys_info
from trixtweaker import config


def main():
    """Instala o menu de contexto."""
    config.state.INFO = sys_info()
    print("instalando menu de contexto...")
    print("ok" if ctx_install() else "falha (rode como admin)")


if __name__ == "__main__":
    main()
