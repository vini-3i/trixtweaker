"""i18n: T() e troca de idioma."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from trixtweaker import config
from trixtweaker.i18n import T, set_lang


def test_t_returns_string():
    """T() retorna string nao vazia."""
    config.state.LANG = "pt"
    assert isinstance(T("back"), str) and T("back")
    assert T("chave_inexistente_xyz") == "chave_inexistente_xyz"


def test_lang_switch_persists():
    """Troca de idioma persiste no state e prefs."""
    set_lang("en")
    assert config.state.LANG == "en"
    assert T("back") == "Back"
    set_lang("pt")
    assert config.state.LANG == "pt"
    assert T("back") == "Voltar"
