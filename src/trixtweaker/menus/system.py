"""Menu do sistema."""
from __future__ import annotations
import io
import sys
import time
from .. import config
from ..actions.context_menu import ctx_is_installed
from ..actions.system_ops import (
    act_backup_export,
    act_backup_import,
    act_benchmark,
    act_check_update,
    act_export_report,
)
from ..i18n import T
from ..log import hist_add, log
from ..system.av import detect_av
from ..system.process import popen, run
from ..ui.ansi import CY, DM, RD, WH, clear
from ..ui.breadcrumb import crumb_pop, crumb_push
from ..ui.feedback import emit, info, ok, pause, spin
from ..ui.screen import SCREEN, menu_pick


def run() -> None:
    """Loop do menu de sistema."""
    crumb_push("sistema")
    try:
        while True:
            op = menu_pick([
                ("1", "Informacoes do sistema", "", CY),
                ("2", "Exportar relatorio .txt", "", CY),
                ("3", "Criar ponto de restauracao", "", CY),
                ("4", "Checar atualizacao do TrixTweaker", "", CY),
                ("5", "Benchmark de desempenho", "", CY),
                ("6", "Backup de config (export/import)", "", CY),
                ("7", "Abrir pasta do TrixTweaker", "", CY),
                ("8", "Abrir pasta de backups", "", CY),
                ("9", "Abrir Gerenciador de Tarefas", "", CY),
                ("10", "Ver log da sessao", "", CY),
                ("0", T("back"), "", RD),
            ], title="SISTEMA")
            if op == "0":
                return
            if op == "1":
                clear()
                SCREEN.reset()
                buf = io.StringIO()
                SCREEN._render_header(buf)
                sys.stdout.write(buf.getvalue())
                inf = config.state.INFO
                emit(" " + CY("CPU:    ") + WH(inf["cpu"]))
                emit(" " + CY("RAM:    ") + WH(inf["ram"]))
                emit(" " + CY("GPU:    ") + WH(inf["gpu"]))
                emit(" " + CY("OS:     ") + WH(f"{inf['os']} {inf['build']}"))
                emit(" " + CY("User:   ") + WH(inf["user"]))
                emit(" " + CY("PC:     ") + WH(inf["pc"]))
                emit(" " + CY("Log:    ") + WH(str(config.LOG_FILE)))
                emit(" " + CY("Config: ") + WH(str(config.CONFIG_FILE)))
                avs = detect_av()
                emit(" " + CY("AV:     ") + WH(", ".join(avs) if avs else T("av_none")))
                emit(" " + CY("Menu ctx: ") + WH("sim" if ctx_is_installed() else "nao"))
                pause()
                SCREEN.reset()
            elif op == "2":
                act_export_report()
                pause()
            elif op == "3":
                spin("criando ponto de restauracao", 3)
                run('powershell -NoProfile -Command "Checkpoint-Computer -Description TrixTweaker -RestorePointType MODIFY_SETTINGS"',
                    shell=True, timeout=120)
                ok("ok")
                hist_add("restore point")
                pause()
            elif op == "4":
                act_check_update()
                pause()
            elif op == "5":
                act_benchmark()
                pause()
            elif op == "6":
                sub_op = menu_pick([
                    ("1", T("backup_export"), "", CY),
                    ("2", T("backup_import"), "", CY),
                    ("0", T("back"), "", RD),
                ], title=T("menu_backup"))
                if sub_op == "1":
                    act_backup_export()
                    pause()
                elif sub_op == "2":
                    act_backup_import()
                    pause()
            elif op == "7":
                popen(["explorer", str(config.WORKDIR)])
                time.sleep(1)
            elif op == "8":
                popen(["explorer", str(config.BACKUP)])
                time.sleep(1)
            elif op == "9":
                popen(["taskmgr.exe"])
                time.sleep(1)
            elif op == "10":
                clear()
                SCREEN.reset()
                if config.LOG_FILE.exists():
                    lines = config.LOG_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()[-40:]
                    for l in lines:
                        emit(" " + DM(l[:110]))
                else:
                    info("log vazio")
                pause()
                SCREEN.reset()
    finally:
        crumb_pop()
