"""Bytegenaue Formatsicherungen mit einem JSON-Parse je Dateistand, ohne Tk."""
from datetime import datetime
import hashlib
import json
import os
import shutil


def file_signature(stat):
    # Unter Windows liefern stat und fstat in Python 3.12 unterschiedliche
    # ctime-Werte nach Überschreiben: Erstellzeit bzw. Änderungszeit.
    # Die explizite Erstellzeit ist dort konsistent; POSIX behält die ctime.
    changed = getattr(stat, 'st_birthtime_ns', None) if os.name == 'nt' else stat.st_ctime_ns
    return (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, changed)


class SchemaBackups:
    """Merkt Format und Dateistand; Änderungen invalidieren den Formatcache."""

    def __init__(self):
        self._key = None
        self._version = None

    @staticmethod
    def _file_key(path, stat):
        signature = file_signature(stat)
        if os.name == 'nt':
            # Gleich große Überschreibungen innerhalb eines Windows-Ticks
            # können identische Metadaten haben, auch native ChangeTime.
            # Der vollständige Inhalt erkennt Formatwerte an jeder Position.
            # Der JSON-Parse bleibt bei unverändertem Inhalt zwischengespeichert.
            with open(path, 'rb') as source:
                signature += (hashlib.file_digest(source, 'sha256').digest(),)
        return os.path.abspath(path), signature

    def observe(self, path, payload, stat):
        """Der Ladeweg hat den Inhalt schon gelesen: keinen zweiten JSON-Parse machen."""
        self._key = self._file_key(path, stat)
        self._version = payload.get('version', 0) if isinstance(payload, dict) else 0

    def version(self, path):
        key = self._file_key(path, os.stat(path))
        if self._key != key:
            with open(path, 'r', encoding='utf-8') as source:
                payload = json.load(source)
                self.observe(path, payload, os.fstat(source.fileno()))
        return self._version

    def ensure(self, path, backup_dir, target):
        """Ohne erfolgreiche Kopie muss der Aufrufer das Überschreiben abbrechen."""
        if not os.path.isfile(path):
            return None
        version = self.version(path)
        valid = isinstance(version, int) if target == 12 else type(version) is int
        if valid and version >= target:
            return None
        os.makedirs(backup_dir, exist_ok=True)
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        destination = os.path.join(backup_dir, f'liste_vor_format{target}_{stamp}.json')
        shutil.copy2(path, destination)
        return destination
