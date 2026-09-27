"""Registry em sandbox HKCU e backup."""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from trixtweaker import config
from trixtweaker.system.registry import _split_hive, reg_backup, reg_set


def test_split_hive():
    """_split_hive separa hive corretamente."""
    if os.name != "nt":
        return
    import winreg
    hive, sub = _split_hive(r"HKCU\Software\TrixTweakerTest")
    assert hive == winreg.HKEY_CURRENT_USER
    assert sub == r"Software\TrixTweakerTest"


def test_set_get_sandbox():
    """reg_set escreve valor em sandbox HKCU."""
    if os.name != "nt":
        return
    import winreg
    ok, _ = reg_set(r"HKCU\Software\TrixTweakerTest", "Probe", 1)
    assert ok
    k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\TrixTweakerTest")
    val, _ = winreg.QueryValueEx(k, "Probe")
    winreg.CloseKey(k)
    assert val == 1
    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\TrixTweakerTest")


def test_backup_creates_file():
    """reg_backup cria arquivo .reg."""
    if os.name != "nt":
        return
    reg_backup(r"HKCU\Software", "testtag")
    files = list(config.BACKUP.glob("reg_testtag_*.reg"))
    assert len(files) >= 1
