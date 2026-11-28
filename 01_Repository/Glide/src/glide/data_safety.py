# SPDX-License-Identifier: MPL-2.0
"""Daten- und Sicherheitsübersicht: Status sammeln und Prüfergebnisse merken, ohne Tk (DS-10).

Schnell verfügbar sind nur Dateimetadaten (Größe, Zeit, freier Speicher).
Vollständige Prüfungen laufen auf Anforderung; ihr Ergebnis steht in
`data_status.json` neben den Einstellungen, damit die Übersicht beim Öffnen
nichts Teures erzwingt. Was Glide nicht geprüft hat, heißt „nicht geprüft“ –
ein grüner Zustand beruht nur auf einem tatsächlichen Prüfergebnis.
"""
from dataclasses import dataclass
import datetime as _dt
import os
import shutil

import local_json_store

FILE_NAME = "data_status.json"
FORMAT = "glide-data-status"
VERSION = 1
FULL_BACKUP_SUFFIXES = (".glideapp", ".glidebackup")


@dataclass(frozen=True)
class FileInfo:
    count: int
    bytes: int
    newest: float | None


def scan_flat(directory, suffixes=None, prefix=None):
    """Anzahl, Größe, neueste Änderung – nur Metadaten, eine Ebene tief."""
    count = size = 0
    newest = None
    try:
        with os.scandir(directory) as eintraege:
            for eintrag in eintraege:
                if not eintrag.is_file(follow_symlinks=False):
                    continue
                name = eintrag.name
                if suffixes and not name.endswith(tuple(suffixes)):
                    continue
                if prefix and not name.startswith(prefix):
                    continue
                info = eintrag.stat(follow_symlinks=False)
                count += 1
                size += info.st_size
                newest = info.st_mtime if newest is None else max(newest, info.st_mtime)
    except OSError:
        pass
    return FileInfo(count, size, newest)


def file_info(path):
    try:
        info = os.stat(path)
    except OSError:
        return FileInfo(0, 0, None)
    return FileInfo(1, info.st_size, info.st_mtime)


def free_bytes(path):
    try:
        return shutil.disk_usage(path).free
    except OSError:
        return None


def snapshot(*, base_dir, save_file, backup_dir, attachments_dir, schema_version, dirty,
             read_only_reason, lock_held):
    """Alle schnellen Kennzahlen in einem Wörterbuch; keine Inhaltsprüfung."""
    return {
        "base_dir": base_dir,
        "schema_version": schema_version,
        "data": file_info(save_file),
        "dirty": bool(dirty),
        "read_only_reason": read_only_reason,
        "lock_held": bool(lock_held),
        "auto_backups": scan_flat(backup_dir, (".json",)),
        "full_backups": scan_flat(backup_dir, FULL_BACKUP_SUFFIXES),
        "attachments": scan_flat(attachments_dir),
        "free": free_bytes(base_dir),
    }


class StatusFile:
    """Zuletzt gespeicherte Prüfergebnisse je Speicherdatei."""

    def __init__(self, path, save_file):
        self.path = os.fspath(path)
        self.save_file = str(save_file)
        self.state = local_json_store.read(self.path, FORMAT, VERSION)
        self.payload = self.state.payload or {"format": FORMAT, "version": VERSION, "workspaces": {}}

    def get(self, key):
        return ((self.payload.get("workspaces") or {}).get(self.save_file) or {}).get(key)

    def record(self, key, value):
        """Ergebnis mit Zeitstempel merken; Schreibfehler werden weitergegeben."""
        if not self.state.writable:
            return False
        eintrag = dict(value, at=_dt.datetime.now().astimezone().isoformat(timespec="seconds"))
        bereiche = self.payload.setdefault("workspaces", {})
        bereiche.setdefault(self.save_file, {})[key] = eintrag
        local_json_store.write_atomic(self.path, self.payload)
        return True


def human_bytes(value):
    if value is None:
        return None
    for einheit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or einheit == "TB":
            return f"{value:.0f} {einheit}" if einheit == "B" else f"{value:.1f} {einheit}"
        value /= 1024
