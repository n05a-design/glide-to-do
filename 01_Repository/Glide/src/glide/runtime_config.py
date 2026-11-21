# SPDX-License-Identifier: MPL-2.0
"""Laufzeitpfade und Konfiguration ohne Tk-Import oder vorzeitige Dateisystemmutationen (WA-49 / WA-39).

Trennt die Pfadauflösung und Konfigurationsprüfung strikt von der Dateisystem-
Erzeugung und dem App-Start. Ermöglicht Tests und Analysen ohne Seiteneffekte
im Benutzerprofil. Die Auflösungsmechanik (Plattformordner, Umgebung,
Zeiger, Reihenfolge) liegt seit V1.69 in `glide_shell.runtime_paths` (D98);
hier bleiben Produktname, Variablen- und Dateinamen, der Pfadvertrag und
die Meldungen.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
import sys

from glide_shell import runtime_paths as _paths

APP_NAME = "Glide"
IS_MACOS = sys.platform == "darwin"
IS_WINDOWS = os.name == "nt"
IS_LINUX = sys.platform.startswith("linux")


def _platform() -> str:
    # Zur Aufrufzeit gelesen, damit Tests `IS_MACOS`/`IS_WINDOWS` und `os` ersetzen können.
    return "darwin" if IS_MACOS else ("win32" if IS_WINDOWS else "linux")


def resolve_default_data_dir() -> str:
    """Standard-Speicherort für Nutzerdaten nach Plattformkonvention."""
    return _paths.platform_data_dir(APP_NAME, platform=_platform(), environ=os.environ, path=os.path)


def resolve_default_cache_dir() -> str:
    """Standard-Speicherort für Cache und Bytecode nach Plattformkonvention."""
    return _paths.platform_cache_dir(APP_NAME, platform=_platform(), environ=os.environ, path=os.path,
                                     windows_subdir="Cache", linux_name="glide")


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
    cache_dir: str
    is_overridden: bool = False

    def ensure_dirs(self) -> None:
        """Erzeugt die benötigten Verzeichnisse bewusst und kontrolliert.

        Wird beim regulären App-Start oder vor Schreiboperationen aufgerufen,
        niemals allein durch den Import eines Moduls.
        """
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.attachments_dir, exist_ok=True)


UNREACHABLE_TITLE = "Datenordner nicht erreichbar"


def prepare_data_dir(paths: RuntimePaths, origin: RuntimePaths | None = None) -> tuple[str, str] | None:
    """Legt die Ordner an; ein nicht erreichbares Ziel ergibt (Titel, Meldung) statt einer Ausnahme.

    `origin` ist die Auflösung beim Start ohne ausdrücklichen Pfad. Nur sie
    weiß, ob der Ordner aus `GLIDE_DATA_DIR`, dem Zeiger oder dem Standard
    stammt; die Meldung nennt diese Quelle.
    """
    try:
        paths.ensure_dirs()
    except OSError as error:
        return UNREACHABLE_TITLE, unreachable_message(origin or paths, error)
    return None


def unreachable_message(paths: RuntimePaths, error: OSError | None = None) -> str:
    """Meldung für einen Datenordner, der sich nicht anlegen oder öffnen lässt."""
    teile = [f"Glide erreicht den Datenordner nicht:\n{paths.base_dir}"]
    if paths.is_overridden:
        teile.append("Der Ordner ist über die Umgebungsvariable GLIDE_DATA_DIR gesetzt.")
    elif os.path.normcase(paths.base_dir) != os.path.normcase(paths.default_dir):
        teile.append(f"Der Ordner ist eingetragen in:\n{paths.pointer_file}")
    teile.append("Binde das Laufwerk oder den Ordner ein und starte Glide erneut. "
                 "Glide beendet sich jetzt, ohne den Bestand zu ändern.")
    grund = getattr(error, "strerror", None)
    if grund:
        teile.append(f"Systemmeldung: {grund}")
    return "\n\n".join(teile)


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

    base_dir, overridden = _paths.resolve_base(data_dir, env, "GLIDE_DATA_DIR", default_dir, pointer_file)
    cache_dir = _paths.env_dir(env, "GLIDE_CACHE_DIR") or resolve_default_cache_dir()

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
        cache_dir=cache_dir,
        is_overridden=overridden,
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
