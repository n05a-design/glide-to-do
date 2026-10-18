"""Datensperre `glide.lock` ohne Tk (WA-30, Befund A36).

Die Sperre ist eine kleine JSON-Datei mit Rechner, Prozess, Kennung und
Zeitstempel; sie schützt einen Datenordner, auch über einen Cloudordner
zwischen zwei Rechnern. Bis 18.10.2026 galt eine defekte oder unlesbare
Sperre als frei, der Erwerb las und ersetzte ohne exklusive Anlage, eine
verschwundene Sperre wurde beim Erneuern nicht neu angelegt, und Einstellungen
schrieben ohne Prüfung der Kennung.

Jetzt gilt:

- `read` unterscheidet fehlend, gültig, defekt (kein lesbares Objekt mit
  Rechner und Zeitstempel) und unlesbar (Betriebssystemfehler). Defekt und
  unlesbar sind nie frei.
- `classify` entscheidet über eine gültige Sperre: fremd, oder frei, weil
  älter als die Frist, auf diesem Rechner ohne lebenden Prozess oder vom
  eigenen Prozess.
- `create_exclusive` legt eine fehlende Sperre exklusiv an (fertiger Inhalt
  per Hardlink, sonst `O_EXCL`); von zwei gleichzeitigen Starts gewinnt genau
  einer.

Die App bleibt Adapter (D17): Sie hält die eigene Kennung, setzt den
Schreibschutz und zeigt Meldungen.
"""

import ctypes
import contextlib
import json
import os
import sys
import tempfile
import uuid
from datetime import datetime

MISSING = "missing"
VALID = "valid"
DEFECTIVE = "defective"
UNREADABLE = "unreadable"

FOREIGN = "foreign"
FREE = "free"

# Eine Sperre ist wenige hundert Byte groß; mehr ist kein Glide-Inhalt.
MAX_BYTES = 64 * 1024


class LockState:
    """Ergebnis von `read`: Art, Inhalt (nur bei gültiger Sperre) und Grund."""

    __slots__ = ("kind", "record", "detail")

    def __init__(self, kind, record=None, detail=""):
        self.kind = kind
        self.record = record
        self.detail = detail

    def __repr__(self):
        return f"LockState({self.kind!r}, {self.record!r}, {self.detail!r})"


def host_name(environ=None):
    environ = os.environ if environ is None else environ
    return environ.get("COMPUTERNAME") or environ.get("HOSTNAME") or "unbekannt"


def new_record(host, pid, now):
    """Neuer Sperrinhalt mit frischer Kennung; `now` als ISO-Zeichenkette."""
    return {"host": host, "pid": pid, "token": uuid.uuid4().hex, "started_at": now, "refreshed_at": now}


def stamp(record):
    """Zeitpunkt der letzten Erneuerung; ValueError, wenn keiner lesbar ist."""
    value = datetime.fromisoformat(str(record.get("refreshed_at") or record.get("started_at")))
    return value if value.tzinfo is not None else value.astimezone()


def parse(raw):
    """Prüft den Inhalt einer Sperrdatei; ValueError, wenn sie defekt ist.

    Gültig ist ein JSON-Objekt mit Rechnername und lesbarem Zeitstempel.
    Kennung und Prozess sind optional: Ältere Fassungen schrieben anfangs nur
    `started_at`.
    """
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    try:
        record = json.loads(raw)
    except (ValueError, RecursionError) as exc:
        raise ValueError(f"kein lesbares JSON ({exc.__class__.__name__})") from None
    if not isinstance(record, dict):
        raise ValueError("kein JSON-Objekt")
    if not isinstance(record.get("host"), str) or not record.get("host"):
        raise ValueError("Rechnername fehlt")
    try:
        stamp(record)
    except (ValueError, TypeError, OverflowError):
        raise ValueError("Zeitstempel fehlt oder ist ungültig") from None
    return record


def read(path):
    """Liest die Sperrdatei ohne Ausnahme; siehe `LockState`."""
    try:
        with open(path, "rb") as file:
            raw = file.read(MAX_BYTES + 1)
    except FileNotFoundError:
        return LockState(MISSING)
    except OSError as exc:
        return LockState(UNREADABLE, detail=str(exc) or exc.__class__.__name__)
    if len(raw) > MAX_BYTES:
        return LockState(DEFECTIVE, detail="zu groß für eine Sperrdatei")
    try:
        return LockState(VALID, parse(raw))
    except (ValueError, UnicodeDecodeError) as exc:
        return LockState(DEFECTIVE, detail=str(exc))


def process_alive(pid):
    """Ob ein Prozess dieses Rechners noch läuft; im Zweifel ja."""
    if sys.platform.startswith("win"):
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_bool, ctypes.c_ulong]
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
        kernel.CloseHandle.argtypes = [ctypes.c_void_p]
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            # Zugriff verweigert heißt: Der Prozess existiert.
            return ctypes.get_last_error() == 5
        try:
            code = ctypes.c_ulong()
            if kernel.GetExitCodeProcess(handle, ctypes.byref(code)) and code.value != 259:
                return False
        finally:
            kernel.CloseHandle(handle)
        return True
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    return True


def classify(record, *, host, pid, now, max_age_seconds, alive=process_alive):
    """FOREIGN oder FREE für eine gültige Sperre, die nicht die eigene Kennung trägt."""
    if (now - stamp(record)).total_seconds() > max_age_seconds:
        return FREE
    if record.get("host") != host:
        return FOREIGN
    try:
        other = int(record.get("pid", 0))
    except (TypeError, ValueError):
        other = 0
    if other <= 0 or other == pid:
        return FREE
    return FOREIGN if alive(other) else FREE


def defective_question(detail):
    """Frage beim Start, wenn die Sperre defekt oder unlesbar ist."""
    grund = f": {detail}" if detail else ""
    return (f"Die Sperrdatei dieses Datenordners (glide.lock) ist beschädigt oder unlesbar{grund}.\n\n"
            "Glide hat den Bestand deshalb schreibgeschützt geöffnet. Ist Glide sicher auf keinem anderen "
            "Rechner und in keinem anderen Fenster mit diesem Datenordner geöffnet, kann dieser Start die "
            "Sperre übernehmen und wieder speichern.\n\nSperre jetzt übernehmen?")


def takeover_failed(detail):
    return f"Die Datensperre ließ sich nicht übernehmen:\n{detail}\n\nDieser Start bleibt schreibgeschützt."


def _content(record):
    return json.dumps(record, ensure_ascii=False, indent=4).encode("utf-8")


def create_exclusive(path, record):
    """Legt die Sperre nur an, wenn noch keine existiert; True bei Erfolg.

    Der Inhalt entsteht vollständig in einer Zwischendatei und wird per
    Hardlink unter dem Sperrnamen eingehängt; das scheitert atomar, sobald die
    Datei existiert. Kennt das Dateisystem keine Hardlinks, legt `O_EXCL` die
    Datei exklusiv an. Andere Fehler gehen weiter.
    """
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    data = _content(record)
    fd, temp = tempfile.mkstemp(prefix=".glide-lock-", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "wb") as file:
            file.write(data)
            file.flush()
            os.fsync(file.fileno())
        try:
            os.link(temp, path)
            return True
        except FileExistsError:
            return False
        except (OSError, NotImplementedError):
            if os.path.lexists(path):
                return False
        try:
            handle = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0))
        except FileExistsError:
            return False
        with os.fdopen(handle, "wb") as file:
            file.write(data)
            file.flush()
            os.fsync(file.fileno())
        return True
    finally:
        try:
            os.remove(temp)
        except OSError:
            pass


@contextlib.contextmanager
def acquisition(path):
    """Serialisiert Prüfen und Ersetzen auch einer verwaisten Sperre.

    Das Betriebssystem gibt die kurze Erwerbssperre bei einem Prozessabbruch
    frei. Die Hilfsdatei bleibt bestehen: Löschen würde wartende Prozesse auf
    unterschiedliche Dateien sperren lassen. Cloud-Abgleich über zwei Rechner
    ist damit weiterhin keine verteilte Sperre.
    """
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fd = os.open(os.fspath(path) + ".acquire", os.O_CREAT | os.O_RDWR, 0o600)
    locked = False
    try:
        if os.fstat(fd).st_size == 0:
            os.write(fd, b"\0")
        os.lseek(fd, 0, os.SEEK_SET)
        try:
            if sys.platform.startswith("win"):
                import msvcrt
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            locked = True
        except OSError:
            pass
        yield locked
    finally:
        if locked:
            os.lseek(fd, 0, os.SEEK_SET)
            if sys.platform.startswith("win"):
                import msvcrt
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
