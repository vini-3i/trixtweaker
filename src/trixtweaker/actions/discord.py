"""Acoes de otimizacao do Discord."""
from __future__ import annotations
import json
import shutil
import time
from datetime import datetime
from pathlib import Path
from .. import config
from ..i18n import T
from ..log import hist_add, log
from ..security.sanitize import safe_path
from ..system.process import popen, run
from ..ui.ansi import CY, DM, WH
from ..ui.feedback import emit, fail, ok, skip, spin


def discord_channels() -> list[tuple[str, str, Path]]:
    """Lista canais do Discord instalados."""
    found = []
    for key, path in config.DISCORD_DIRS.items():
        if path.exists():
            label = {"stable": "Discord", "ptb": "Discord PTB", "canary": "Discord Canary"}[key]
            found.append((key, label, path))
    return found


def act_discord_launch(channel: str) -> None:
    """Inicia o Discord do canal informado."""
    label = {"stable": "Discord", "ptb": "Discord PTB", "canary": "Discord Canary"}[channel]
    base = config.DISCORD_DIRS[channel]
    if not base.exists():
        fail(f"{label} nao instalado")
        return
    spin(f"abrindo {label}")
    exe = None
    for d in base.glob("app-*"):
        for e in d.glob("*.exe"):
            n = e.name.lower()
            if "discord" in n and "update" not in n:
                exe = e
                break
        if exe:
            break
    if not exe:
        upd = base / "Update.exe"
        if upd.exists():
            exe_name = {"stable": "Discord.exe", "ptb": "DiscordPTB.exe", "canary": "DiscordCanary.exe"}[channel]
            popen([str(upd), "--processStart", exe_name])
            ok(f"{label} iniciado")
            return
        fail(f"{label}: exe nao encontrado")
        return
    popen([str(exe)])
    ok(f"{label} iniciado")
    log(f"launch {label}")


def act_discord_update(channel: str = "stable") -> None:
    """Forca atualizacao do Discord via Update.exe."""
    base = config.DISCORD_DIRS[channel]
    upd = base / "Update.exe"
    if not upd.exists():
        fail(f"{channel}: Update.exe nao encontrado")
        return
    for exe in ("Discord.exe", "DiscordPTB.exe", "DiscordCanary.exe"):
        run(["taskkill", "/IM", exe, "/F"], shell=False)
    spin(f"atualizando {channel}")
    exe_name = {"stable": "Discord.exe", "ptb": "DiscordPTB.exe", "canary": "DiscordCanary.exe"}[channel]
    popen([str(upd), "--processStart", exe_name]).wait()
    popen([str(upd), "--processStart", exe_name])
    ok(f"{channel} atualizado")
    log(f"update {channel}")
    hist_add(f"discord update {channel}")


def _optimize_one_discord(channel: str, label: str, base: Path, dry: bool = False) -> None:
    """Otimiza um unico canal do Discord."""
    if not base.exists():
        skip(f"{label}: nao encontrado")
        return
    for exe in ("Discord.exe", "DiscordPTB.exe", "DiscordCanary.exe"):
        run(["taskkill", "/IM", exe, "/F"], shell=False)
    time.sleep(1)
    spin(f"{label}: backup", dry=dry)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = config.BACKUP / f"discord_{channel}_{stamp}"
    dest.mkdir(parents=True, exist_ok=True)
    for f in ("settings.json", "Preferences"):
        src = base / f
        if src.exists():
            shutil.copy2(src, dest / f)
    ok(f"{label}: backup em {dest.name}")
    spin(f"{label}: perfil leve", dry=dry)
    settings = base / "settings.json"
    data: dict = {}
    if settings.exists():
        try:
            data = json.loads(settings.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data.update({
        "hardwareAcceleration": False,
        "messageDisplayCompact": True,
        "gifAutoPlay": False,
        "renderEmbeds": False,
        "renderReactions": True,
        "inlineAttachmentMedia": False,
        "inlineEmbedMedia": False,
        "streamerModeEnabled": False,
        "afkTimeout": 300,
        "enableTtsCommand": False,
        "showCurrentGame": False,
        "disableAnimations": True,
        "notifications": {"desktop": "mentions", "unread": True, "taskbar": True,
                          "showBadge": True, "sound": True},
        "sound": {"message": False, "deafen": False, "mute": False,
                  "userJoin": False, "userLeave": False, "callRing": True},
    })
    if not dry:
        settings.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    ok(f"{label}: settings otimizado")
    spin(f"{label}: Preferences", dry=dry)
    prefs = base / "Preferences"
    pdata: dict = {}
    if prefs.exists():
        try:
            pdata = json.loads(prefs.read_text(encoding="utf-8"))
        except Exception:
            pdata = {}
    pdata["hardware_acceleration"] = "disabled"
    if not dry:
        prefs.write_text(json.dumps(pdata, indent=2, ensure_ascii=False), encoding="utf-8")
    ok(f"{label}: Preferences ajustado")
    spin(f"{label}: limpando cache", dry=dry)
    caches = ["Cache", "Code Cache", "GPUCache", "DawnCache", "DawnGraphiteCache",
              "ShaderCache", "GrShaderCache"]
    freed = 0
    for c in caches:
        full = safe_path(base / c)
        if full and full.exists():
            for f in full.rglob("*"):
                try:
                    if f.is_file():
                        freed += f.stat().st_size
                except Exception:
                    pass
            if not dry:
                shutil.rmtree(full, ignore_errors=True)
                full.mkdir(exist_ok=True)
    mb = freed / 1024 / 1024
    config.state.SESSION_FREED += mb
    ok(f"{label}: cache limpo ({mb:.1f} MB)")
    log(f"discord {channel} optimized")
    hist_add(f"discord {channel}")


def act_discord_optimize_all(dry: bool = False) -> None:
    """Otimiza todos os canais do Discord instalados."""
    chans = discord_channels()
    if not chans:
        fail("nenhum Discord instalado")
        return
    for key, label, base in chans:
        _optimize_one_discord(key, label, base, dry=dry)


def act_discord_optimize_one(key: str) -> None:
    """Otimiza um canal especifico do Discord."""
    label = {"stable": "Discord", "ptb": "Discord PTB", "canary": "Discord Canary"}[key]
    _optimize_one_discord(key, label, config.DISCORD_DIRS[key])


def act_discord_restore() -> None:
    """Restaura backup de configuracao do Discord."""
    dirs = sorted([p for p in config.BACKUP.glob("discord_*") if p.is_dir()],
                  key=lambda x: x.stat().st_mtime, reverse=True)[:12]
    if not dirs:
        skip("nenhum backup de Discord")
        return
    emit()
    for i, b in enumerate(dirs, 1):
        emit(f" {CY(f'[{i}]')} {DM(b.name)}")
    emit(f" {CY('[0]')} {DM(T('cancel'))}")
    try:
        c = input(" " + WH(T("choice"))).strip()
    except (EOFError, KeyboardInterrupt):
        return
    if not c or c == "0":
        return
    try:
        idx = int(c) - 1
    except ValueError:
        return
    if idx < 0 or idx >= len(dirs):
        return
    sel = dirs[idx]
    channel = "stable"
    for k in config.DISCORD_DIRS:
        if f"discord_{k}_" in sel.name:
            channel = k
            break
    target_dir = config.DISCORD_DIRS[channel]
    if not target_dir.exists():
        fail(f"{channel} nao instalado")
        return
    spin("restaurando")
    for f in sel.iterdir():
        tgt = target_dir / ("settings.json" if "settings" in f.name else "Preferences")
        shutil.copy2(f, tgt)
    ok(f"backup restaurado em {channel}")
    log("discord restored")
    hist_add(f"discord restore {channel}")
