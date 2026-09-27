"""Acoes de sistema: relatorio, update, backup, benchmark, seguranca."""
from __future__ import annotations
import os
import shutil
import tempfile
import time
from datetime import datetime
from pathlib import Path
from .. import config
from ..i18n import T, load_prefs
from ..log import hist_add, log
from ..security.dpapi import dpapi_decrypt, dpapi_encrypt
from ..security.sanitize import sanitize_log
from ..system.av import detect_av
from ..system.info import is_admin
from ..system.process import run
from .context_menu import ctx_is_installed
from .discord import discord_channels
from ..ui.ansi import CY, DM, WH
from ..ui.feedback import confirm, emit, fail, info, ok, spin


def act_export_report() -> None:
    """Gera relatorio de sistema em txt."""
    spin("gerando relatorio")
    inf = config.state.INFO
    if not inf:
        from ..system.info import sys_info
        inf = sys_info()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = config.WORKDIR / f"report_{stamp}.txt"
    lines = [
        "TrixTweaker · relatorio do sistema",
        f"gerado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"versao: {config.VERSION}",
        "",
        f"usuario:    {inf['user']}",
        f"pc:         {inf['pc']}",
        f"os:         {inf['os']} build {inf['build']}",
        f"cpu:        {inf['cpu']}",
        f"ram:        {inf['ram']}",
        f"gpu:        {inf['gpu']}",
        f"admin:      {is_admin()}",
        "",
        "--- antivirus ---",
    ]
    for a in detect_av():
        lines.append(a)
    lines += ["", "--- servicos chave ---"]
    for svc in ("SysMain", "WSearch", "wuauserv", "WinDefend", "Themes"):
        rc, out2 = run(["sc", "query", svc], shell=False, timeout=5)
        state = "?"
        for l in out2.splitlines():
            if "STATE" in l:
                state = l.strip()
                break
        lines.append(f"{svc:12} {state}")
    lines += ["", "--- canais discord ---"]
    for key, label, p in discord_channels():
        lines.append(f"{label:16} {p}")
    lines += ["", "--- menu de contexto ---"]
    lines.append(f"instalado: {ctx_is_installed()}")
    out.write_text("\n".join(lines), encoding="utf-8")
    ok(f"relatorio salvo: {out.name}")
    log("report exported")
    hist_add("export report")


def act_check_update() -> None:
    """Checa atualizacao remota via version.txt."""
    from ..update import check_update
    check_update()


def act_backup_export() -> None:
    """Exporta config cifrada para pasta de backup."""
    spin("exportando config")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = config.WORKDIR / f"config_backup_{stamp}"
    dest.mkdir(parents=True, exist_ok=True)
    try:
        if config.CONFIG_FILE.exists():
            shutil.copy2(config.CONFIG_FILE, dest / "config.enc")
        if config.HISTORY_FILE.exists():
            shutil.copy2(config.HISTORY_FILE, dest / "history.enc")
        ok(f"{T('backup_done')}: {dest.name}")
        hist_add("backup export")
    except Exception as e:
        fail(f"falha: {sanitize_log(str(e))}")


def act_backup_import() -> None:
    """Importa config de um backup anterior."""
    dirs = sorted([p for p in config.WORKDIR.glob("config_backup_*") if p.is_dir()],
                  key=lambda x: x.stat().st_mtime, reverse=True)[:10]
    if not dirs:
        from ..ui.feedback import skip
        skip("nenhum backup")
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
    spin("importando")
    if (sel / "config.enc").exists():
        shutil.copy2(sel / "config.enc", config.CONFIG_FILE)
        load_prefs()
    ok(T("backup_import_done"))
    hist_add("backup import")


def act_benchmark() -> None:
    """Mede desempenho de disco, subprocess e RAM livre."""
    spin("medindo desempenho", 3)
    results = []
    t0 = time.time()
    tmp = Path(tempfile.gettempdir()) / "trix_bench.tmp"
    try:
        with open(tmp, "wb") as f:
            f.write(b"\0" * (1024 * 1024))
        with open(tmp, "rb") as f:
            _ = f.read()
        tmp.unlink(missing_ok=True)
        disk_ms = (time.time() - t0) * 1000
        results.append(("disco 1MB", f"{disk_ms:.1f} ms"))
    except Exception:
        results.append(("disco", "falha"))
    t0 = time.time()
    run(["where", "python"], shell=False, timeout=5)
    proc_ms = (time.time() - t0) * 1000
    results.append(("subprocess", f"{proc_ms:.1f} ms"))
    try:
        rc, out = run('wmic OS get FreePhysicalMemory', shell=True, timeout=5)
        for l in out.splitlines():
            l = l.strip()
            if l.isdigit():
                free_mb = int(l) / 1024
                results.append(("RAM livre", f"{free_mb:.0f} MB"))
                break
    except Exception:
        pass
    emit()
    for name, val in results:
        emit(f" {CY(name):<20} {WH(val)}")
    log("benchmark")
    hist_add("benchmark")


def act_sec_status() -> None:
    """Mostra status da criptografia DPAPI."""
    spin("checando criptografia")
    if os.name != "nt":
        info("DPAPI disponivel apenas no Windows")
        return
    enc_ok = False
    try:
        test = b"trix-test-data"
        enc = dpapi_encrypt(test)
        dec = dpapi_decrypt(enc)
        enc_ok = (enc != test) and (dec == test)
    except Exception:
        pass
    if enc_ok:
        ok("DPAPI ativo — config e historico cifrados")
    else:
        fail("DPAPI indisponivel — arquivos em texto puro")
    emit()
    emit(" " + CY("config:  ") + WH(str(config.CONFIG_FILE)))
    emit(" " + CY("history: ") + WH(str(config.HISTORY_FILE)))
    emit(" " + CY("log:     ") + WH(str(config.LOG_FILE)))
    log("sec status")


def act_sec_wipe() -> None:
    """Apaga config, historico e log do disco."""
    if not confirm("apagar config + history + log?"):
        return
    spin("apagando dados")
    for f in (config.CONFIG_FILE, config.HISTORY_FILE, config.LOG_FILE):
        try:
            if f.exists():
                f.unlink()
        except Exception:
            pass
    ok("dados apagados")
    log("sec wipe")
    hist_add("sec wipe")
