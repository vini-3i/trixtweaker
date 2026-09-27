"""Camada pura de acesso ao registry do Windows."""
from __future__ import annotations
import os
import re
from datetime import datetime
from .. import config
from ..security.sanitize import sanitize_log


def _split_hive(path: str):
    """Separa hive e subchave de um caminho de registry."""
    import winreg
    if path.startswith("HKCU"):
        return winreg.HKEY_CURRENT_USER, path[5:].lstrip("\\")
    if path.startswith("HKLM"):
        return winreg.HKEY_LOCAL_MACHINE, path[5:].lstrip("\\")
    if path.startswith("HKCR"):
        return winreg.HKEY_CLASSES_ROOT, path[5:].lstrip("\\")
    if path.startswith("HKU"):
        return winreg.HKEY_USERS, path[4:].lstrip("\\")
    raise ValueError("hive desconhecido")


def reg_set(path: str, name: str, value, vtype: str = "DWORD", dry: bool = False) -> tuple[bool, str | None]:
    """Define um valor no registry."""
    if dry:
        return True, None
    try:
        import winreg
        hive, sub = _split_hive(path)
        key = winreg.CreateKeyEx(hive, sub, 0, winreg.KEY_SET_VALUE)
        if vtype == "DWORD":
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, int(value))
        elif vtype == "SZ":
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, str(value))
        elif vtype == "EXPAND_SZ":
            winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, str(value))
        elif vtype == "BINARY":
            winreg.SetValueEx(key, name, 0, winreg.REG_BINARY, value)
        elif vtype == "QWORD":
            winreg.SetValueEx(key, name, 0, winreg.REG_QWORD, int(value))
        winreg.CloseKey(key)
        return True, None
    except PermissionError:
        return False, "sem permissao"
    except Exception as e:
        return False, sanitize_log(str(e))


def reg_backup(path: str, tag: str) -> None:
    """Exporta uma chave do registry para a pasta de backups."""
    if os.name != "nt":
        return
    from .process import run
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = re.sub(r"[^A-Za-z0-9_]", "_", path)[:80]
    out = config.BACKUP / f"reg_{tag}_{safe}_{stamp}.reg"
    try:
        run(["reg", "export", path, str(out), "/y"], timeout=10)
    except Exception:
        pass


def reg_exists(path: str) -> bool:
    """Retorna True se a chave do registry existe."""
    try:
        import winreg
        hive, sub = _split_hive(path)
        k = winreg.OpenKey(hive, sub, 0, winreg.KEY_READ)
        winreg.CloseKey(k)
        return True
    except Exception:
        return False


def reg_delete_tree(path: str) -> bool:
    """Apaga chave do registry e subchaves recursivamente."""
    try:
        import winreg
        hive, sub = _split_hive(path)
    except Exception:
        return False

    def _del(hive, subpath: str) -> bool:
        try:
            k = winreg.OpenKey(hive, subpath, 0, winreg.KEY_READ | winreg.KEY_WRITE)
            subkeys = []
            i = 0
            while True:
                try:
                    subkeys.append(winreg.EnumKey(k, i))
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(k)
            for s in subkeys:
                _del(hive, f"{subpath}\\{s}")
            winreg.DeleteKey(hive, subpath)
            return True
        except FileNotFoundError:
            return True
        except Exception:
            return False

    return _del(hive, sub)


def reg_enum_subkeys(path: str) -> list[str]:
    """Lista nomes das subchaves imediatas de uma chave."""
    try:
        import winreg
        hive, sub = _split_hive(path)
        k = winreg.OpenKey(hive, sub, 0, winreg.KEY_READ)
        names: list[str] = []
        i = 0
        while True:
            try:
                names.append(winreg.EnumKey(k, i))
            except OSError:
                break
            i += 1
        winreg.CloseKey(k)
        return names
    except Exception:
        return []
