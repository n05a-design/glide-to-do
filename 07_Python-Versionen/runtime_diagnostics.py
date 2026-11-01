"""Begrenzte lokale Start-/Abschlussdiagnose ohne Aufgabeninhalte oder Netzwerk.

Ein Starter kann den Appprozess begleiten: Der Begleiter schreibt den echten
Exitstatus erst nach dessen Ende und liest dabei dessen letzte Phase erneut.
Direkte Appstarts halten dieselben Phasen fest; ein harter Abbruch lässt dort
einen ausdrücklich unvollständigen Abschluss zurück.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
import uuid

CHILD_FLAG = "--glide-diagnostic-child"
SESSION_ENV = "GLIDE_DIAGNOSTIC_SESSION"
PARENT_ENV = "GLIDE_DIAGNOSTIC_PARENT"
MAX_FILES = 8
MAX_BYTES = 32_768
PHASES = frozenset(("startup", "runtime_checked", "imported", "data_loaded",
                    "data_saved", "ui_ready", "closing", "closed", "failed"))
FIELDS = frozenset(("format", "session", "started_at", "process_id", "parent_id", "python",
                    "implementation", "executable", "system", "release", "machine", "version",
                    "build", "last_completed_phase", "phase_at", "completed", "supervised",
                    "exit_code", "ended_at", "supervisor_id", "tk", "start_error"))
_current = None
_warning = ""


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def diagnostic_directory(environment=None):
    """Testisolierung hat Vorrang; normale Diagnose liegt lokal am Gerät."""
    environment = os.environ if environment is None else environment
    override = environment.get("GLIDE_DATA_DIR")
    if override:
        return Path(override).expanduser().absolute() / "diagnostics"
    if sys.platform == "darwin":
        return Path.home() / "Library/Logs/Glide"
    if os.name == "nt":
        return Path(environment.get("LOCALAPPDATA") or Path.home()) / "Glide/Diagnostics"
    return Path(environment.get("XDG_STATE_HOME") or Path.home() / ".local/state") / "glide/diagnostics"


def _safe_version(value):
    value = str(value)
    return value if re.fullmatch(r"[0-9A-Za-z.+-]{0,40}", value) else ""


def _safe_build(value):
    value = str(value)
    return value if re.fullmatch(r"[a-fA-F0-9]{8,64}", value) else ""


def _read(path):
    if path.is_symlink():
        raise ValueError("Diagnosebeleg darf kein Verweis auf eine andere Datei sein.")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("Diagnosebeleg ist zu groß.")
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or document.get("format") != 1:
        raise ValueError("Ungültiger Diagnosebeleg.")
    if any(key not in FIELDS for key in document):
        raise ValueError("Unbekannte Felder im Diagnosebeleg.")
    if document.get("last_completed_phase") not in PHASES:
        raise ValueError("Ungültige Phase im Diagnosebeleg.")
    return document


class Journal:
    """Ein fester Metadatensatz je Sitzung, atomar und ohne Inhaltsfelder."""

    def __init__(self, *, directory=None, session=None, version="", build="", resume=False):
        self.directory = Path(directory) if directory is not None else diagnostic_directory()
        self.session = session or uuid.uuid4().hex
        if not re.fullmatch(r"[a-f0-9]{32}", self.session):
            raise ValueError("Ungültige Diagnosesitzung.")
        self.path = self.directory / (self.session + ".json")
        self.enabled = True
        self.problem = ""
        self.state = dict(format=1, session=self.session, started_at=_now(),
                          process_id=os.getpid(), parent_id=os.getppid(),
                          python=platform.python_version(), implementation=platform.python_implementation(),
                          executable=Path(sys.executable).name, system=platform.system(),
                          release=platform.release(), machine=platform.machine(),
                          version=_safe_version(version), build=_safe_build(build),
                          last_completed_phase="startup", phase_at=_now(), completed=False,
                          supervised=False, exit_code=None)
        try:
            self.directory.mkdir(parents=True, exist_ok=True)
            if resume:
                previous = _read(self.path)
                if previous.get("session") != self.session or previous.get("supervisor_id") != os.getppid():
                    raise ValueError("Diagnosesitzung gehört zu einem anderen Starter.")
                self.state = previous
                self.state["process_id"] = os.getpid()
                self.state["parent_id"] = os.getppid()
                self.state["version"] = _safe_version(version) or self.state.get("version", "")
                self.state["build"] = _safe_build(build) or self.state.get("build", "")
            self._write()
            self._prune()
        except (OSError, ValueError, TypeError) as error:
            self._disable(error)

    def _disable(self, error):
        global _warning
        self.enabled = False
        # Fehlertext kann Dateinamen oder fremde Inhalte enthalten. Nur Typ und
        # eigener Ablageort werden benannt, keine Exception-Nachricht übernommen.
        self.problem = ("Die lokale Startdiagnose kann nicht gespeichert werden: "
                        + str(self.directory) + " (" + type(error).__name__ + ").")
        _warning = self.problem

    def _write(self):
        if not self.enabled:
            return False
        temporary = None
        try:
            payload = (json.dumps(self.state, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            if len(payload) > MAX_BYTES:
                raise ValueError("Diagnosebeleg überschreitet die feste Größe.")
            descriptor, temporary = tempfile.mkstemp(prefix=f".diagnose-{os.getpid()}-", suffix=".tmp", dir=self.directory)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(payload)
            os.replace(temporary, self.path)
            temporary = None
            return True
        except (OSError, ValueError, TypeError) as error:
            self._disable(error)
            return False
        finally:
            if temporary is not None:
                try:
                    os.unlink(temporary)
                except OSError:
                    pass

    def _prune(self):
        """Nur eigene abgeschlossene Sitzungen entfernen; aktive nicht stören."""
        for path in self.directory.glob(".diagnose-*.tmp"):
            match = re.fullmatch(r"\.diagnose-([0-9]+)-[A-Za-z0-9_-]+\.tmp", path.name)
            if match and not _process_exists(int(match.group(1))):
                try:
                    path.unlink()
                except OSError:
                    pass
        records = []
        for path in self.directory.glob("*.json"):
            if re.fullmatch(r"[a-f0-9]{32}\.json", path.name):
                try:
                    records.append((path.stat().st_mtime_ns, path))
                except OSError:
                    continue
        records.sort(reverse=True)
        for _stamp, path in records[MAX_FILES:]:
            if path == self.path:
                continue
            try:
                state = _read(path)
                # Nicht abgeschlossene Sitzungen eines lebenden Prozesses
                # behalten. Nach Prozessende gilt die normale Dateigrenze.
                pid = state.get("supervisor_id") if state.get("supervised") else state.get("process_id")
                if not state.get("completed") and _process_exists(pid):
                    continue
                path.unlink()
            except (OSError, ValueError, TypeError):
                # Beschädigte eigene alte Diagnose ist kein Produktbestand.
                try:
                    path.unlink()
                except OSError:
                    pass

    def record_phase(self, phase, *, tk_version=None):
        if phase not in PHASES:
            raise ValueError("Unbekannte Diagnosephase.")
        changes = self.state.get("last_completed_phase") != phase
        if tk_version is not None:
            value = str(tk_version)
            if not re.fullmatch(r"[0-9.]{1,30}", value):
                raise ValueError("Ungültige Tk-Version.")
            changes = changes or self.state.get("tk") != value
            self.state["tk"] = value
        if not changes:
            return self.enabled
        self.state.update(last_completed_phase=phase, phase_at=_now())
        return self._write()

    def finish(self, exit_code=0):
        if not isinstance(exit_code, int):
            raise ValueError("Exitstatus muss eine Zahl sein.")
        self.state.update(completed=True, exit_code=exit_code, ended_at=_now())
        return self._write()

    def record_child_exit(self, exit_code):
        """Nach dem Warten den letzten Kindstand lesen, niemals überholen."""
        if not self.enabled:
            return False
        try:
            latest = _read(self.path)
            if latest.get("session") != self.session or latest.get("supervisor_id") != os.getpid():
                raise ValueError("Diagnosesitzung wurde ersetzt.")
            self.state = latest
            self.state.update(supervised=True, supervisor_id=os.getpid())
            return self.finish(exit_code)
        except (OSError, ValueError, TypeError) as error:
            self._disable(error)
            return False


def _process_exists(pid):
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        return False
    if os.name == "nt":
        # os.kill(pid, 0) ist unter Windows keine geeignete Existenzprobe.
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        open_process = kernel.OpenProcess
        open_process.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
        open_process.restype = wintypes.HANDLE
        get_exit = kernel.GetExitCodeProcess
        get_exit.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
        get_exit.restype = wintypes.BOOL
        close_handle = kernel.CloseHandle
        close_handle.argtypes = (wintypes.HANDLE,)
        close_handle.restype = wintypes.BOOL
        handle = open_process(0x1000, False, pid)
        if not handle:
            return ctypes.get_last_error() != 87
        try:
            code = wintypes.DWORD()
            return not get_exit(handle, ctypes.byref(code)) or code.value == 259
        finally:
            close_handle(handle)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except (OSError, PermissionError):
        return True
    return True


def child_launch():
    """Umgebungsmarker allein startet keine zweite Überwachung."""
    session = os.environ.get(SESSION_ENV, "")
    parent = os.environ.get(PARENT_ENV, "")
    if not re.fullmatch(r"[a-f0-9]{32}", session) or parent != str(os.getppid()):
        return False
    try:
        state = _read(diagnostic_directory() / (session + ".json"))
        return (state.get("session") == session and state.get("supervised") is True
                and state.get("supervisor_id") == os.getppid() and not state.get("completed"))
    except (OSError, ValueError, TypeError):
        return False


def consume_child_flag():
    if CHILD_FLAG not in sys.argv:
        return False
    # Auch bei nicht schreibbarer Diagnose darf der gestartete Kindprozess
    # nicht erneut einen Begleiter starten. Parent-PID und Schalter reichen
    # für diese Kontrollflussentscheidung; start_session validiert den Beleg.
    parent = os.environ.get(PARENT_ENV, "")
    if parent != str(os.getppid()):
        return False
    sys.argv.remove(CHILD_FLAG)
    return True


def start_session(version="", build=""):
    global _current, _warning
    if (_current is None or _current.state.get("completed")
            or _current.directory.absolute() != diagnostic_directory().absolute()):
        _warning = ""
        inherited = os.environ.get(SESSION_ENV) if child_launch() else None
        _current = Journal(session=inherited, version=version, build=build, resume=bool(inherited))
    else:
        changed = False
        for name, value in (("version", _safe_version(version)), ("build", _safe_build(build))):
            if value and _current.state.get(name) != value:
                _current.state[name] = value
                changed = True
        if changed:
            _current._write()
    return _current


def record_phase(phase, *, tk_version=None):
    # Adapter/isolierte ListApp-Tests dürfen durch eine Speicheraktion keine
    # Diagnose im echten Benutzerordner oder einer alten Testablage beginnen.
    if _current is None or _current.directory.absolute() != diagnostic_directory().absolute():
        return False
    return _current.record_phase(phase, tk_version=tk_version)


def finish(exit_code=0):
    if _current is None or _current.directory.absolute() != diagnostic_directory().absolute():
        return False
    return _current.finish(exit_code)


def warning():
    if _current is not None and _current.directory.absolute() != diagnostic_directory().absolute():
        return ""
    return _warning


def supervise(command, version="", build="", *, env=None):
    """Ein Kind starten, einmal warten, tatsächlichen Status lokal festhalten."""
    environment = dict(os.environ if env is None else env)
    journal = Journal(directory=diagnostic_directory(environment), version=version, build=build)
    journal.state.update(supervised=True, supervisor_id=os.getpid())
    journal._write()
    environment.update({SESSION_ENV: journal.session, PARENT_ENV: str(os.getpid())})
    try:
        completed = subprocess.run(list(command), env=environment)
        code = completed.returncode
    except OSError as error:
        journal.state["start_error"] = type(error).__name__
        journal.finish(1)
        return 1
    journal.record_child_exit(code)
    try:
        journal._prune()
    except OSError as error:
        journal._disable(error)
    return code
