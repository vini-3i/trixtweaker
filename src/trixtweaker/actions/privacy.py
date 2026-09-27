"""Acoes de privacidade."""
from __future__ import annotations
from ..log import hist_add, log
from ..system.registry import reg_set
from ..ui.feedback import ok, spin


def act_priv_cortana() -> None:
    """Desativa Cortana."""
    spin("desativando Cortana")
    reg_set(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search", "AllowCortana", 0)
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Search", "CortanaConsent", 0)
    ok("Cortana desativada")
    log("cortana off")
    hist_add("cortana off")


def act_priv_ads() -> None:
    """Desativa ID de publicidade."""
    spin("desativando ID de publicidade")
    reg_set(r"HKCU\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo", "Enabled", 0)
    reg_set(r"HKLM\SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo", "DisabledByGroupPolicy", 1)
    ok("publicidade desativada")
    log("ads off")
    hist_add("ads off")


def act_priv_location() -> None:
    """Desativa rastreamento de localizacao."""
    spin("desativando rastreamento de localizacao")
    base = r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location"
    reg_set(base, "Value", "Deny", "SZ")
    ok("localizacao desativada")
    log("location off")
    hist_add("location off")


def act_priv_camera_mic() -> None:
    """Bloqueia camera e microfone para apps."""
    spin("bloqueando camera e microfone")
    base = r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore"
    reg_set(base + r"\webcam", "Value", "Deny", "SZ")
    reg_set(base + r"\microphone", "Value", "Deny", "SZ")
    ok("camera/microfone bloqueados")
    log("cam/mic off")
    hist_add("cam/mic off")
