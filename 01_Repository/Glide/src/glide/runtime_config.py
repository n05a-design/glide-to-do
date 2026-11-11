# SPDX-License-Identifier: MPL-2.0
"""Laufzeitpfade und Konfiguration ohne Tk-Import oder vorzeitige Dateisystemmutationen (WA-49 / WA-39).

Trennt die Pfadauflösung und Konfigurationsprüfung strikt von der Dateisystem-
Erzeugung und dem App-Start. Ermöglicht Tests und Analysen ohne Seiteneffekte
im Benutzerprofil.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
import sys

APP_NAME = "Glide"
IS_MACOS = sys.platform == "darwin"
IS_WINDOWS = os.name == "nt"
IS_LINUX = sys.platform.startswith("linux")


def resolve_default_data_dir() -> str:
    """Standard-Speicherort für Nutzerdaten nach Plattformkonvention."""
    if IS_MACOS:
        base = os.path.join(os.path.expanduser("~/Library/Application Support"), APP_NAME)
    elif IS_WINDOWS:
        base = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), APP_NAME)
    else:
        base_dir = os.environ.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share")
        base = os.path.join(base_dir, APP_NAME)
    return os.path.abspath(base)


@dataclass(frozen=True)
class RuntimePaths:
    """Zentraler, unveränderlicher Pfadvertrag für eine Glide-Laufzeitumgebung."""
    base_dir: str
    default_dir: str
    pointer_file: str
    save_file: str
    settings_file: str
    backup_dir: str
    attachments_dir: str
    templates_file: str
    lock_file: str
    error_log_file: str

    def ensure_dirs(self) -> None:
        """Erzeugt die benötigten Verzeichnisse bewusst und kontrolliert.

        Wird beim regulären App-Start oder vor Schreiboperationen aufgerufen,
        niemals allein durch den Import eines Moduls.
        """
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.attachments_dir, exist_ok=True)


def resolve_paths(data_dir: str | None = None, env: dict | None = None) -> RuntimePaths:
    """Löst alle Pfade rein rechnerisch und seiteneffektfrei auf.

    Reihenfolge:
    1. Explizit übergebenes `data_dir` (höchste Priorität, z. B. in Tests).
    2. Umgebungsvariable `GLIDE_DATA_DIR`.
    3. Benutzerzeiger in `datenordner.json` (sofern vorhanden und gültig).
    4. Plattform-Standardverzeichnis.

    Erzeugt keinerlei Verzeichnisse oder Dateien auf der Festplatte.
    """
    if env is None:
        env = os.environ

    default_dir = resolve_default_data_dir()
    pointer_file = os.path.join(default_dir, "datenordner.json")

    override = data_dir or env.get("GLIDE_DATA_DIR")
    if override:
        base_dir = os.path.abspath(os.path.expanduser(override))
    else:
        base_dir = default_dir
        if os.path.isfile(pointer_file):
            try:
                with open(pointer_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                selected = data.get("path") if isinstance(data, dict) else None
                if isinstance(selected, str) and selected.strip():
                    base_dir = os.path.abspath(os.path.expanduser(selected.strip()))
            except (OSError, ValueError, TypeError):
                pass

    return RuntimePaths(
        base_dir=base_dir,
        default_dir=default_dir,
        pointer_file=pointer_file,
        save_file=os.path.join(base_dir, "liste_speicher.json"),
        settings_file=os.path.join(base_dir, "settings.json"),
        backup_dir=os.path.join(base_dir, "backups"),
        attachments_dir=os.path.join(base_dir, "attachments"),
        templates_file=os.path.join(base_dir, "vorlagen.json"),
        lock_file=os.path.join(base_dir, "glide.lock"),
        error_log_file=os.path.join(base_dir, "fehlerprotokoll.txt"),
    )


@dataclass(frozen=True)
class RuntimeConfig:
    """Vollständige, Tk-freie Laufzeitkonfiguration."""
    paths: RuntimePaths
    app_name: str = APP_NAME
    is_macos: bool = IS_MACOS
    is_windows: bool = IS_WINDOWS
    is_linux: bool = IS_LINUX
    read_only: bool = False
    test_mode: bool = False

    @classmethod
    def create(cls, data_dir: str | None = None, read_only: bool = False, env: dict | None = None) -> RuntimeConfig:
        if env is None:
            env = os.environ
        paths = resolve_paths(data_dir=data_dir, env=env)
        test_mode = bool(env.get("GLIDE_TEST_MODE"))
        return cls(paths=paths, read_only=read_only, test_mode=test_mode)
