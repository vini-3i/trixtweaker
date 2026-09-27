"""Acoes de otimizacao para jogos."""
from __future__ import annotations
import re
from .. import config
from ..log import hist_add, log
from ..security.sanitize import safe_path, sanitize_log
from ..system.process import run
from ..system.registry import reg_enum_subkeys, reg_set
from ..ui.feedback import fail, ok, skip, spin


def act_game_mode() -> None:
    """Ativa o Game Mode do Windows."""
    spin("configurando Game Mode")
    reg_set(r"HKCU\Software\Microsoft\GameBar", "AllowAutoGameMode", 1)
    reg_set(r"HKCU\Software\Microsoft\GameBar", "AutoGameModeEnabled", 1)
    ok("game mode ativado")
    log("game mode")
    hist_add("game mode")


def act_dvr() -> None:
    """Desativa Game DVR e gravacao em segundo plano."""
    spin("desativando DVR")
    reg_set(r"HKCU\System\GameConfigStore", "GameDVR_Enabled", 0)
    reg_set(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR", "AllowGameDVR", 0)
    ok("DVR desativado")
    log("dvr off")
    hist_add("dvr off")


def act_tcp() -> None:
    """Ajusta parametros TCP para ping baixo."""
    spin("ajustando TCP")
    for c in ["netsh int tcp set global autotuninglevel=normal",
              "netsh int tcp set global rss=enabled",
              "netsh int tcp set heuristics disabled",
              "netsh int tcp set global chimney=enabled",
              "netsh int tcp set global ecncapability=enabled"]:
        run(c, shell=True)
    ok("TCP ajustado")
    log("tcp")
    hist_add("tcp")


def act_nagle() -> None:
    """Desativa algoritmo de Nagle em todas as interfaces."""
    spin("desativando Nagle")
    try:
        base = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
        subs = reg_enum_subkeys(f"HKLM\\{base}")
        count = 0
        for sub in subs:
            full = f"{base}\\{sub}"
            reg_set(f"HKLM\\{full}", "TcpAckFrequency", 1)
            reg_set(f"HKLM\\{full}", "TCPNoDelay", 1)
            count += 1
        ok(f"Nagle desativado em {count} interfaces")
        log(f"nagle {count}")
        hist_add(f"nagle {count}")
    except Exception as e:
        fail(f"falha: {sanitize_log(str(e))}")


def act_prioridade() -> None:
    """Define prioridade alta para processos de jogos."""
    spin("prioridade de jogos")
    base = r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games"
    reg_set(base, "GPU Priority", 8)
    reg_set(base, "Priority", 6)
    reg_set(base, "Scheduling Category", "High", "SZ")
    reg_set(base, "SFIO Priority", "High", "SZ")
    ok("prioridade ajustada")
    log("game priority")
    hist_add("prioridade jogo")


def act_gpu() -> None:
    """Otimiza configuracoes de GPU."""
    spin("otimizando GPU")
    reg_set(r"HKCU\Software\Microsoft\DirectX\UserGpuPreferences",
            "DirectXUserGlobalSettings", "VRROptimizeEnable=0;", "SZ")
    reg_set(r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode", 2)
    ok("GPU otimizada")
    log("gpu")
    hist_add("gpu")


def act_shaders() -> None:
    """Limpa caches de shader de GPU."""
    spin("limpando shader cache")
    paths = [config.LOCALAPPDATA / "D3DSCache",
             config.LOCALAPPDATA / "NVIDIA" / "DXCache",
             config.LOCALAPPDATA / "NVIDIA" / "GLCache",
             config.LOCALAPPDATA / "AMD" / "DxCache",
             config.LOCALAPPDATA / "Intel" / "ShaderCache"]
    total = 0
    for p in paths:
        sp = safe_path(p)
        if sp and sp.exists():
            for f in sp.rglob("*"):
                try:
                    if f.is_file():
                        total += f.stat().st_size
                        f.unlink()
                except Exception:
                    pass
    mb = total / 1024 / 1024
    config.state.SESSION_FREED += mb
    ok(f"shader cache limpo ({mb:.1f} MB)")
    log(f"shader {total}")
    hist_add("shader cache")


JOGOS: dict[str, tuple[str, list[str]]] = {
    "1": ("VALORANT", ["VALORANT.exe", "RiotClientServices.exe"]),
    "2": ("CS2", ["cs2.exe"]),
    "3": ("Fortnite", ["FortniteClient-Win64-Shipping.exe"]),
    "4": ("League of Legends", ["LeagueClient.exe", "League of Legends.exe"]),
    "5": ("GTA V / FiveM", ["GTA5.exe", "FiveM.exe"]),
    "6": ("Roblox", ["RobloxPlayerBeta.exe"]),
    "7": ("Minecraft", ["javaw.exe"]),
    "8": ("Apex Legends", ["r5apex.exe"]),
    "9": ("Free Fire", ["FreeFire.exe"]),
    "A": ("Overwatch 2", ["Overwatch.exe"]),
    "B": ("Rocket League", ["RocketLeague.exe"]),
    "C": ("Dota 2", ["dota2.exe"]),
}


def act_jogo(nome: str, exes: list[str]) -> None:
    """Aplica flags de compatibilidade aos executaveis de um jogo."""
    spin(f"otimizando {nome}")
    path = r"HKCU\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
    found = 0
    for exe in exes:
        if not re.match(r"^[A-Za-z0-9_\-\.]{1,64}$", exe):
            continue
        rc, out = run(f'where {exe}', shell=True, timeout=8)
        if rc == 0 and out.strip():
            real = out.strip().splitlines()[0].strip()
            reg_set(path, real, "~ HIGHDPIAWARE DISABLEDXMAXIMIZEDWINDOWEDMODE", "SZ")
            found += 1
    if found:
        ok(f"{nome} otimizado ({found} exe)")
        log(f"game {nome}")
        hist_add(f"jogo {nome}")
    else:
        skip(f"{nome}: exe nao encontrado no PATH")
