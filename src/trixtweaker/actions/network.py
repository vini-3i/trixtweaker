"""Acoes de rede: reset, DNS e diagnostico."""
from __future__ import annotations
import re
from ..log import hist_add, log
from ..system.process import run
from ..ui.ansi import DM
from ..ui.feedback import emit, ok, spin


def _list_ifaces() -> list[str]:
    """Lista interfaces de rede habilitadas."""
    rc, out = run(["netsh", "interface", "show", "interface"], shell=False, timeout=10)
    ifaces = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[0] == "Enabled":
            name = " ".join(parts[3:])
            if re.match(r"^[A-Za-z0-9_\-\. ]{1,64}$", name):
                ifaces.append(name)
    return ifaces or ["Ethernet", "Wi-Fi"]


def act_rede_reset() -> None:
    """Reseta stack de rede winsock/IP."""
    spin("resetando stack de rede")
    for c in [["netsh", "winsock", "reset"], ["netsh", "int", "ip", "reset"],
              ["ipconfig", "/release"], ["ipconfig", "/renew"]]:
        run(c, shell=False, timeout=30)
    ok("stack de rede resetado (reinicie)")
    log("net reset")
    hist_add("net reset")


def act_rede_dns_cloudflare() -> None:
    """Aplica DNS Cloudflare 1.1.1.1."""
    spin("aplicando DNS Cloudflare")
    for iface in _list_ifaces():
        run(["netsh", "interface", "ip", "set", "dns", f"name={iface}", "static", "1.1.1.1"], shell=False)
        run(["netsh", "interface", "ip", "add", "dns", f"name={iface}", "1.0.0.1", "index=2"], shell=False)
    run(["ipconfig", "/flushdns"], shell=False)
    ok("DNS Cloudflare aplicado")
    log("dns cloudflare")
    hist_add("dns cloudflare")


def act_rede_dns_google() -> None:
    """Aplica DNS Google 8.8.8.8."""
    spin("aplicando DNS Google")
    for iface in _list_ifaces():
        run(["netsh", "interface", "ip", "set", "dns", f"name={iface}", "static", "8.8.8.8"], shell=False)
        run(["netsh", "interface", "ip", "add", "dns", f"name={iface}", "8.8.4.4", "index=2"], shell=False)
    run(["ipconfig", "/flushdns"], shell=False)
    ok("DNS Google aplicado")
    log("dns google")
    hist_add("dns google")


def act_rede_dns_dhcp() -> None:
    """Volta DNS para automatico via DHCP."""
    spin("voltando DNS para automatico")
    for iface in _list_ifaces():
        run(["netsh", "interface", "ip", "set", "dns", f"name={iface}", "source=dhcp"], shell=False)
    run(["ipconfig", "/flushdns"], shell=False)
    ok("DNS voltou para DHCP")
    log("dns dhcp")
    hist_add("dns dhcp")


def act_rede_info() -> None:
    """Exibe informacoes de rede via ipconfig."""
    spin("coletando info de rede", 1)
    rc, out = run(["ipconfig", "/all"], shell=False, timeout=10)
    emit()
    for l in out.splitlines()[:40]:
        emit(" " + DM(l[:110]))
    log("net info")
