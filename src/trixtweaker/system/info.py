"""Informacoes do sistema com cache."""
from __future__ import annotations
import ctypes
import os
import sys
from .. import config
from .process import run


def sys_info(refresh: bool = False) -> dict:
    """Coleta e cacheia informacoes do sistema."""
    if config.state.INFO and not refresh:
        return config.state.INFO
    info = {"user": os.environ.get("USERNAME", "?"),
            "pc": os.environ.get("COMPUTERNAME", "?"),
            "cpu": "?", "ram": "?", "gpu": "?", "os": "?", "build": 0}
    try:
        rc, out = run(["wmic", "cpu", "get", "name"], timeout=8)
        if rc == 0:
            info["cpu"] = next((l.strip() for l in out.splitlines() if l.strip() and l.strip() != "Name"), "?")
    except Exception:
        pass
    try:
        rc, out = run(["wmic", "computersystem", "get", "TotalPhysicalMemory"], timeout=8)
        if rc == 0:
            raw = next((l.strip() for l in out.splitlines() if l.strip().isdigit()), "0")
            info["ram"] = f"{int(raw) / 1024 ** 3:.1f} GB" if raw.isdigit() else "?"
    except Exception:
        pass
    try:
        rc, out = run(["wmic", "path", "win32_videocontroller", "get", "name"], timeout=8)
        if rc == 0:
            info["gpu"] = next((l.strip() for l in out.splitlines() if l.strip() and l.strip() != "Name"), "?")
    except Exception:
        pass
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                           r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        info["build"] = int(winreg.QueryValueEx(k, "CurrentBuildNumber")[0])
        info["os"] = "Windows 11" if info["build"] >= 22000 else "Windows 10"
    except Exception:
        pass
    config.state.INFO = info
    return info


def is_admin() -> bool:
    """Retorna True se o processo tem privilegios de admin."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def elevate() -> bool:
    """Reinicia o processo elevado via UAC."""
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)
    except Exception:
        return False
