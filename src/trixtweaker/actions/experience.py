"""Acoes de experiencia do Windows."""
from __future__ import annotations
from ..i18n import T
from ..log import hist_add, log
from ..system.process import run
from ..system.registry import reg_set
from ..ui.feedback import fail, ok, spin


def act_exp_anim() -> None:
    """Desativa animacoes e transparencia."""
    spin(T("exp_anim"))
    reg_set(r"HKCU\Control Panel\Desktop\WindowMetrics", "MinAnimate", "0", "SZ")
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "TaskbarAnimations", 0)
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            "EnableTransparency", 0)
    reg_set(r"HKCU\Control Panel\Desktop", "UserPreferencesMask",
            bytes([0x90, 0x12, 0x03, 0x80, 0x10, 0x00, 0x00, 0x00]), "BINARY")
    ok(T("exp_anim"))
    log("exp anim")
    hist_add("exp anim")


def act_exp_widgets() -> None:
    """Desativa widgets, noticias e Copilot."""
    spin(T("exp_widgets"))
    reg_set(r"HKLM\SOFTWARE\Policies\Microsoft\Dsh", "AllowNewsAndInterests", 0)
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "TaskbarDa", 0)
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "ShowCopilotButton", 0)
    reg_set(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot", 1)
    ok(T("exp_widgets"))
    log("exp widgets")
    hist_add("exp widgets")


def act_exp_explorer_open() -> None:
    """Explorer abre em Este Computador."""
    spin(T("exp_explorer_open"))
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "LaunchTo", 1)
    ok(T("exp_explorer_open"))
    log("exp explorer open")
    hist_add("exp explorer open")


def act_exp_ext() -> None:
    """Mostra extensoes de arquivo."""
    spin(T("exp_ext"))
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "HideFileExt", 0)
    ok(T("exp_ext"))
    log("exp ext")
    hist_add("exp ext")


def act_exp_ctx() -> None:
    """Restaura menu de contexto classico no Win11."""
    spin(T("exp_ctx"))
    rc, _ = run(["reg", "add",
                 r"HKLM\SOFTWARE\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32",
                 "/f", "/ve", "/d", ""], shell=False)
    if rc == 0:
        ok(T("exp_ctx"))
        log("exp ctx")
        hist_add("exp ctx")
    else:
        fail("falha (admin)")


def act_exp_start_rec() -> None:
    """Remove recomendados do menu Iniciar."""
    spin(T("exp_start_rec"))
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "Start_TrackDocs", 0)
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "Start_TrackProgs", 0)
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "ShowRecent", 0)
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "ShowFrequent", 0)
    ok(T("exp_start_rec"))
    log("exp start rec")
    hist_add("exp start rec")


def act_exp_start_tips() -> None:
    """Remove dicas e sugestoes do Iniciar."""
    spin(T("exp_start_tips"))
    for sub in ("SubscribedContent-338388Enabled", "SubscribedContent-338389Enabled",
                "SubscribedContent-310093Enabled", "SoftLandingEnabled"):
        reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager", sub, 0)
    ok(T("exp_start_tips"))
    log("exp start tips")
    hist_add("exp start tips")


def act_exp_ads() -> None:
    """Desativa ID de publicidade."""
    spin(T("exp_ads"))
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo", "Enabled", 0)
    reg_set(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo", "DisabledByGroupPolicy", 1)
    ok(T("exp_ads"))
    log("exp ads")
    hist_add("exp ads")


def act_exp_timeline() -> None:
    """Desativa historico de atividades."""
    spin(T("exp_timeline"))
    reg_set(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System", "EnableActivityFeed", 0)
    reg_set(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System", "PublishUserActivities", 0)
    reg_set(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\System", "UploadUserActivities", 0)
    ok(T("exp_timeline"))
    log("exp timeline")
    hist_add("exp timeline")


def act_exp_lockscreen() -> None:
    """Desativa tela de bloqueio."""
    spin(T("exp_lockscreen"))
    reg_set(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Personalization", "NoLockScreen", 1)
    ok(T("exp_lockscreen"))
    log("exp lockscreen")
    hist_add("exp lockscreen")


def act_exp_seconds() -> None:
    """Exibe segundos no relogio do sistema."""
    spin(T("exp_seconds"))
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "ShowSecondsInSystemClock", 1)
    ok(T("exp_seconds"))
    log("exp seconds")
    hist_add("exp seconds")
