"""Smoke: importa ACTIONS e executa em DRY+SILENT."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from trixtweaker import config
from trixtweaker.actions import ACTIONS


def test_actions_import():
    """ACTIONS nao vazio e valores chamaveis."""
    assert len(ACTIONS) >= 10
    for name, fn in ACTIONS.items():
        assert callable(fn), name


def test_actions_smoke():
    """Roda cada acao em SILENT+DRY sem excecao."""
    config.state.SILENT = True
    config.state.DRY = True
    for name, fn in ACTIONS.items():
        try:
            fn()
        except Exception as e:
            raise AssertionError(f"acao {name} falhou: {e}")
    config.state.SILENT = False
    config.state.DRY = False
