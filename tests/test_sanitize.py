"""Sanitizacao de caminhos e logs."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from trixtweaker import config
from trixtweaker.security.sanitize import safe_path, sanitize_log


def test_safe_path_rejects_outside():
    """safe_path rejeita caminhos fora dos roots."""
    assert safe_path(Path("C:/Windows/System32")) is None
    assert safe_path("C:\\Users\\alguem\\Documents\\x") is None


def test_safe_path_allows_workdir():
    """safe_path permite caminhos dentro do WORKDIR."""
    p = config.WORKDIR / "probe.txt"
    assert safe_path(p) is not None


def test_sanitize_log_removes_user():
    """sanitize_log remove nome de usuario."""
    out = sanitize_log(r"C:\Users\Maria\Documents\arquivo.txt fez algo")
    assert "Maria" not in out
