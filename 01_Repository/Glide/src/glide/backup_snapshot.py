"""Unveränderliche Datei-Quelle zwischen Restorevorschau und Übernahme.

Die bestehenden Glide-Schema- und Archivprüfer werden als Funktionen
übergeben. Kein Tk-Import, keine Bestandsmutation, keine Dateiextraktion.
"""
from contextlib import contextmanager
from dataclasses import dataclass, field
import hashlib
import io
import json
import os
from pathlib import Path
import stat
from types import MappingProxyType
import zipfile


def regular_bytes(path, limit):
    if type(limit) is not int or limit < 0:
        raise ValueError("Ungültige Dateigröße für die Sicherungsquelle.")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(Path(path), flags)
    with os.fdopen(fd, "rb") as source:
        info = os.fstat(source.fileno())
        if not stat.S_ISREG(info.st_mode):
            raise ValueError("Die Sicherungsquelle ist keine reguläre Datei.")
        if info.st_size > limit:
            raise ValueError("Die Sicherungsquelle ist zu groß.")
        content = source.read(limit + 1)
        if len(content) > limit:
            raise ValueError("Die Sicherungsquelle ist beim Lesen zu groß geworden.")
    return content


@dataclass(frozen=True)
class Snapshot:
    content: bytes = field(repr=False)
    data: dict
    portable: bool
    referenced: frozenset
    archive_assets: frozenset

    @property
    def sha256(self):
        return hashlib.sha256(self.content).hexdigest()

    def available(self, local_paths=None):
        """Nur Verfügbarkeit zeigen; vollständige Bytes prüft capture_assets."""
        if self.portable:
            return self.archive_assets
        return frozenset(key for key, path in (local_paths or {}).items()
                         if key in self.referenced and path and Path(path).is_file())

    def capture_assets(self, storage_paths, *, max_member_bytes, max_total_bytes, local_paths=None):
        """Gewählte Dateien vor Bestandsänderung vollständig lesen und einfrieren."""
        if type(max_member_bytes) is not int or max_member_bytes < 0:
            raise ValueError("Ungültige Größe eines Sicherungsanhangs.")
        wanted = frozenset(storage_paths)
        if wanted - self.referenced:
            raise ValueError("Ein Seitenanhang gehört nicht zur geprüften Sicherung.")
        if type(max_total_bytes) is not int or max_total_bytes < 0:
            raise ValueError("Ungültige Gesamtgröße für die Sicherungsanhänge.")
        payloads = {}
        total = 0
        if self.portable:
            with zipfile.ZipFile(io.BytesIO(self.content)) as archive:
                for storage in sorted(wanted):
                    if storage not in self.archive_assets:
                        raise ValueError("Ein Seitenanhang fehlt in der Sicherung.")
                    info = archive.getinfo(storage)
                    if info.file_size > max_member_bytes or total + info.file_size > max_total_bytes:
                        raise ValueError("Die Seitenanhänge sind zu groß.")
                    with archive.open(info) as source:
                        content = source.read(max_member_bytes + 1)
                    if len(content) != info.file_size or len(content) > max_member_bytes:
                        raise ValueError("Eine Sicherungsanhangsgröße ist inkonsistent.")
                    payloads[storage] = content
                    total += len(content)
        else:
            for storage in sorted(wanted):
                path = (local_paths or {}).get(storage)
                if not path:
                    raise ValueError("Ein lokaler Anhang für diese JSON-Sicherung fehlt.")
                content = regular_bytes(path, min(max_member_bytes, max_total_bytes - total))
                payloads[storage] = content
                total += len(content)
        return Assets(payloads)


@dataclass(frozen=True)
class Assets:
    payloads: dict = field(repr=False)

    def __post_init__(self):
        if any(not isinstance(value, bytes) for value in self.payloads.values()):
            raise ValueError("Eingefrorene Anhänge müssen vollständige Bytes sein.")
        object.__setattr__(self, "payloads", MappingProxyType(dict(self.payloads)))

    @contextmanager
    def open(self, storage):
        try:
            content = self.payloads[storage]
        except KeyError:
            raise ValueError("Der gewählte Sicherungsanhang wurde nicht eingefroren.") from None
        with io.BytesIO(content) as source:
            yield source


def read(path, *, inspect_archive, validate_data, read_member,
         max_archive_bytes, max_data_bytes):
    content = regular_bytes(path, max_archive_bytes)
    portable = zipfile.is_zipfile(io.BytesIO(content))
    archive_assets = frozenset()
    if portable:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            data_info, attachments = inspect_archive(archive)
            raw = read_member(archive, data_info, max_data_bytes)
            data = json.loads(raw.decode("utf-8"))
            archive_assets = frozenset(attachments)
    else:
        if len(content) > max_data_bytes:
            raise ValueError("Die JSON-Sicherungsquelle ist zu groß.")
        data = json.loads(content.decode("utf-8-sig"))
    referenced = frozenset(validate_data(data, portable=portable))
    if portable and referenced != archive_assets:
        raise ValueError("Die Sicherungsanhänge sind unvollständig oder unerwartet.")
    return Snapshot(content, data, portable, referenced, archive_assets)
