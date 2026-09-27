"""Acoes de desempenho do PC."""
from __future__ import annotations
from ..log import hist_add, log
from ..system.process import run, service_exists
from ..system.registry import reg_backup, reg_set
from ..ui.feedback import fail, ok, skip, spin


def act_energia() -> None:
    """Ativa plano de energia de alto desempenho."""
    spin("ativando plano de alto desempenho")
    rc, _ = run("powercfg /setactive SCHEME_MIN", shell=True)
    if rc == 0:
        ok("plano de energia: alto desempenho")
        log("powercfg MIN")
        hist_add("energia alto desempenho")
    else:
        fail("falha ao mudar plano")


def act_power_ultimate() -> None:
    """Habilita o plano de energia Ultimate Performance."""
    spin("habilitando plano Ultimate")
    run("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True)
    ok("plano Ultimate habilitado")
    log("ultimate")
    hist_add("plano ultimate")


def act_telemetria() -> None:
    """Desativa telemetria e coleta de dados."""
    spin("desativando telemetria")
    pairs = [
        (r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry", 0),
        (r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection", "AllowTelemetry", 0),
        (r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Privacy", "TailoredExperiencesWithDiagnosticDataEnabled", 0),
        (r"HKLM\SOFTWARE\Policies\Microsoft\Windows\CloudContent", "DisableWindowsConsumerFeatures", 1),
    ]
    for p, n, v in pairs:
        reg_backup(p, "telemetry")
        reg_set(p, n, v)
    ok("telemetria desativada")
    log("telemetry")
    hist_add("telemetria off")


def act_animacoes() -> None:
    """Desativa animacoes do Windows."""
    spin("desativando animacoes")
    reg_set(r"HKCU\Control Panel\Desktop\WindowMetrics", "MinAnimate", "0", "SZ")
    reg_set(r"HKCU\Control Panel\Desktop", "UserPreferencesMask",
            bytes([0x90, 0x12, 0x03, 0x80, 0x10, 0x00, 0x00, 0x00]), "BINARY")
    ok("animacoes desativadas")
    log("animations off")
    hist_add("animacoes off")


def act_efeitos() -> None:
    """Ajusta efeitos visuais para performance."""
    spin("ajustando efeitos visuais")
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
            "VisualFXSetting", 2)
    ok("efeitos visuais: performance")
    log("visual fx")
    hist_add("efeitos visuais")


def act_sysmain() -> None:
    """Desativa o servico SysMain/Superfetch."""
    if not service_exists("SysMain"):
        skip("servico SysMain nao existe")
        return
    spin("desativando SysMain")
    run(["sc", "stop", "SysMain"], shell=False)
    rc, _ = run(["sc", "config", "SysMain", "start=", "disabled"], shell=False)
    if rc == 0:
        ok("SysMain desativado")
        log("sysmain off")
        hist_add("sysmain off")
    else:
        fail("falha (admin)")


def act_search() -> None:
    """Desativa o servico Windows Search."""
    if not service_exists("WSearch"):
        skip("servico WSearch nao existe")
        return
    spin("desativando Windows Search")
    run(["sc", "stop", "WSearch"], shell=False)
    rc, _ = run(["sc", "config", "WSearch", "start=", "disabled"], shell=False)
    if rc == 0:
        ok("Windows Search desativado")
        log("wsearch off")
        hist_add("wsearch off")
    else:
        fail("falha (admin)")


def act_memoria() -> None:
    """Otimiza parametros de memoria do sistema."""
    spin("otimizando memoria")
    base = r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management"
    reg_set(base, "LargeSystemCache", 0)
    reg_set(base, "DisablePagingExecutive", 1)
    ok("memoria otimizada")
    log("memory")
    hist_add("memoria")


def act_apps_bg() -> None:
    """Desativa apps rodando em segundo plano."""
    spin("desativando apps em background")
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications",
            "GlobalUserDisabled", 1)
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Search",
            "BackgroundAppGlobalToggle", 0)
    reg_set(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\AppPrivacy",
            "LetAppsRunInBackground", 2)
    ok("apps em segundo plano desativados")
    log("bg apps")
    hist_add("apps bg off")


def act_visual_compact() -> None:
    """Ativa modo compacto do Explorer."""
    spin("modo compacto do Explorer")
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "TaskbarSmallIcons", 1)
    ok("explorer compacto")
    log("compact")
    hist_add("explorer compacto")
