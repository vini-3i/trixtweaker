"""Deteccao de antivirus instalado."""
from __future__ import annotations
from .process import run

KNOWN_AV: dict[str, str] = {
    "avast": "Avast", "avg": "AVG", "kaspersky": "Kaspersky",
    "bitdefender": "Bitdefender", "malwarebytes": "Malwarebytes",
    "norton": "Norton", "mcafee": "McAfee", "eset": "ESET",
    "trend": "Trend Micro", "sophos": "Sophos",
    "windows defender": "Windows Defender", "defender": "Windows Defender",
    "crowdstrike": "CrowdStrike", "sentinelone": "SentinelOne",
    "webroot": "Webroot",
}

_AV_CACHE: list | None = None


def detect_av() -> list[str]:
    """Detecta antivirus via SecurityCenter2, Defender ou tasklist."""
    global _AV_CACHE
    if _AV_CACHE is not None:
        return _AV_CACHE
    found: list[str] = []
    try:
        cmd = ('powershell -NoProfile -Command '
               '"Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct '
               '| Select-Object -ExpandProperty displayName"')
        rc, out = run(cmd, shell=True, timeout=12)
        if rc == 0:
            for line in out.splitlines():
                line = line.strip()
                if line and line not in found:
                    found.append(line)
    except Exception:
        pass
    if not found:
        rc, out = run('powershell -NoProfile -Command '
                      '"Get-MpComputerStatus | Select-Object -ExpandProperty AMRunningMode"',
                      shell=True, timeout=10)
        if rc == 0 and "Normal" in out:
            found.append("Windows Defender")
    if not found:
        rc, out = run("tasklist", shell=True, timeout=8)
        low = out.lower()
        for key, label in KNOWN_AV.items():
            if key in low and label not in found:
                found.append(label)
    _AV_CACHE = found
    return found


def av_is_active() -> bool:
    """Retorna True se algum antivirus foi detectado."""
    return len(detect_av()) > 0
