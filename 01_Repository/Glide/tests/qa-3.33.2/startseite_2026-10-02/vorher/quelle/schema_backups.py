"""Bytegenaue Formatsicherungen mit einem Leselauf je Dateistand, ohne Tk."""
from datetime import datetime
import json
import os
import shutil


def file_signature(stat):
    return (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)


class SchemaBackups:
    """Merkt nur Format und Dateisignatur; ein ersetzter Bestand invalidiert beides."""

    def __init__(self):
        self._key = None
        self._version = None

    def observe(self, path, payload, stat):
        """Der Ladeweg hat den Inhalt schon gelesen: keinen zweiten JSON-Parse machen."""
        self._key = (os.path.abspath(path), file_signature(stat))
        self._version = payload.get('version', 0) if isinstance(payload, dict) else 0

    def version(self, path):
        signature = file_signature(os.stat(path))
        if self._key != (os.path.abspath(path), signature):
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
