"""Constantes, caminhos e estado mutavel global."""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path

VERSION = "0.47.0"
UPDATE_URL = "https://raw.githubusercontent.com/vini-3i/trixtweaker/refs/heads/main/version.txt"

APPDATA = Path(os.environ.get("APPDATA", str(Path.home())))
LOCALAPPDATA = Path(os.environ.get("LOCALAPPDATA", str(Path.home())))
WORKDIR = APPDATA / "TrixTweaker"
BACKUP = WORKDIR / "backups"
LOG_FILE = WORKDIR / "trix.log"
CONFIG_FILE = WORKDIR / "config.enc"
HISTORY_FILE = WORKDIR / "history.enc"

DISCORD_DIRS: dict[str, Path] = {
    "stable": APPDATA / "discord",
    "ptb": APPDATA / "discordptb",
    "canary": APPDATA / "discordcanary",
}

PREFS: dict = {"lang": "pt", "sound": True, "mouse": True}


@dataclass
class State:
    """Estado mutavel global da aplicacao."""

    SESSION_FREED: float = 0.0
    DRY: bool = False
    INFO: dict = field(default_factory=dict)
    SILENT: bool = False
    LANG: str = "pt"


state = State()

try:
    WORKDIR.mkdir(parents=True, exist_ok=True)
    BACKUP.mkdir(parents=True, exist_ok=True)
except Exception:
    pass
