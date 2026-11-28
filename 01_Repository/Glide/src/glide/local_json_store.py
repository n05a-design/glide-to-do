# SPDX-License-Identifier: MPL-2.0
"""Kleine lokale JSON-Begleitdateien sicher lesen und schreiben, ohne Tk (Teil 05B).

Für Dateien neben den Einstellungen, die keine Nutzerdaten im Sinne der
Speicherdatei sind (Eingabeentwürfe, Lesepositionen). Schreiben: temporäre
Datei im selben Ordner, fsync, Rücklesen, `os.replace`. Ein Fehler lässt den
vorherigen Stand unberührt und wird an den Aufrufer weitergegeben. Lesen:
Größengrenze, Formatkennung, Version; eine unlesbare Datei wird beiseitegelegt,
eine neuere nur gelesen und nie überschrieben.
"""
import json
import os
import time

MAX_BYTES = 2 * 1024 * 1024


class StoreState:
    """Ergebnis des Ladens: Nutzlast oder leer, plus Befund."""

    def __init__(self, payload=None, problem=None, protect=False):
        self.payload = payload
        self.problem = problem
        self.protect = protect

    @property
    def writable(self):
        if self.problem == "newer":
            return False
        # Primärdaten (`quarantine=False`): eine unlesbare Datei bleibt liegen
        # und blockiert jedes Schreiben, statt still durch eine leere ersetzt zu werden.
        return not (self.protect and self.problem)


def read(path, format_name, version, max_bytes=MAX_BYTES, quarantine=True):
    """`quarantine=False` für Primärdaten: Datei bleibt unverändert, Schreiben gesperrt."""
    try:
        size = os.path.getsize(path)
    except OSError:
        return StoreState()
    try:
        if size > max_bytes:
            raise ValueError("zu groß")
        with open(path, "r", encoding="utf-8") as source:
            payload = json.load(source)
        if not isinstance(payload, dict) or payload.get("format") != format_name:
            raise ValueError("fremdes Format")
        found = payload.get("version")
        if type(found) is not int or found < 1:
            raise ValueError("ungültige Version")
        return StoreState(payload, "newer" if found > version else None)
    except (OSError, ValueError, TypeError, UnicodeDecodeError) as exc:
        if quarantine:
            beiseitelegen(path)
        return StoreState(None, f"unreadable: {exc}", protect=not quarantine)


def beiseitelegen(path):
    stamp = time.strftime("%Y%m%d_%H%M%S")
    try:
        os.replace(path, f"{path}.unlesbar_{stamp}")
    except OSError:
        pass


def write_atomic(path, payload):
    """Schreibt vollständig oder gar nicht; wirft OSError bei Fehlern."""
    path = os.fspath(path)
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    temporary = f"{path}.{os.getpid()}.tmp"
    try:
        with open(temporary, "w", encoding="utf-8", newline="\n") as target:
            json.dump(payload, target, ensure_ascii=False, indent=1)
            target.flush()
            os.fsync(target.fileno())
        with open(temporary, "r", encoding="utf-8") as check:
            if json.load(check) != payload:
                raise OSError("Begleitdatei unvollständig geschrieben")
        os.replace(temporary, path)
    finally:
        try:
            os.remove(temporary)
        except OSError:
            pass
