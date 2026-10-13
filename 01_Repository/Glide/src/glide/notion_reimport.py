"""Quellenzustand mit dem zuletzt übernommenen und dem lokalen Stand vergleichen.

Aus diesem Modul folgt niemals eine automatische Bestandsänderung. Selbst
konfliktfreie Quelländerungen brauchen eine ausdrückliche Auswahl; Konflikte
zusätzlich die ausdrückliche Wahl, den lokalen Stand zu ersetzen.
"""
from dataclasses import dataclass
import hashlib
import json
import re

_KEY = re.compile(r"(?:notion:[a-f0-9]{32}|path:[a-f0-9]{64})\Z")
_HASH = re.compile(r"[a-f0-9]{64}\Z")


def is_source_key(value):
    return isinstance(value, str) and bool(_KEY.fullmatch(value))


def content_fingerprint(entry, asset_hashes=None):
    if not isinstance(entry, dict):
        raise ValueError("Der lokale Seitenstand muss ein Objekt sein.")
    ignored = {"id", "created_at", "updated_at", "notion_source"}
    document = {key: value for key, value in entry.items() if key not in ignored}
    if asset_hashes is not None:
        def holders(holder):
            yield holder
            for key in ("items", "children"):
                for child in holder.get(key, []):
                    yield from holders(child)
        ids = {value["id"] for holder in holders(entry) for value in holder.get("attachments", [])}
        if not ids.issubset(asset_hashes):
            raise ValueError("Die aktuelle Anhangsprüfung ist unvollständig.")
        document = {"page": document, "asset_hashes": {key: asset_hashes[key] for key in sorted(ids)}}
    text = json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class SourceRecord:
    key: str
    target_id: str
    source_hash: str
    local_hash: str
    source_path: str

    def __post_init__(self):
        if not is_source_key(self.key):
            raise ValueError("Ungültige Notion-Quellenkennung.")
        if (not isinstance(self.target_id, str) or not 1 <= len(self.target_id) <= 256
                or any(ord(char) < 32 for char in self.target_id)):
            raise ValueError("Ungültige Glide-Zielkennung.")
        if any(not isinstance(value, str) or not _HASH.fullmatch(value)
               for value in (self.source_hash, self.local_hash)):
            raise ValueError("Ungültiger Hash im Quellenstand.")
        if not isinstance(self.source_path, str) or not 1 <= len(self.source_path) <= 4096:
            raise ValueError("Ungültiger Archivpfad im Quellenstand.")

    def to_document(self):
        return {"format_version": 1, "key": self.key, "target_id": self.target_id,
                "source_hash": self.source_hash, "local_hash": self.local_hash,
                "source_path": self.source_path}

    @classmethod
    def from_document(cls, raw):
        if (not isinstance(raw, dict) or set(raw) != {"format_version", "key", "target_id", "source_hash", "local_hash", "source_path"}
                or type(raw["format_version"]) is not int or raw["format_version"] != 1):
            raise ValueError("Unbekannte oder unvollständige Notion-Quellenmetadaten.")
        return cls(*(raw[field] for field in ("key", "target_id", "source_hash", "local_hash", "source_path")))


@dataclass(frozen=True, slots=True)
class Comparison:
    page: object
    target_id: str | None
    status: str


@dataclass(frozen=True, slots=True)
class ReimportPlan:
    rows: tuple[Comparison, ...]
    absent_source_keys: tuple[str, ...]


def compare(export, records, current_hashes):
    by_key, target_ids = {}, set()
    for record in records:
        if not isinstance(record, SourceRecord) or record.key in by_key or record.target_id in target_ids:
            raise ValueError("Doppelte oder ungültige Quellenzuordnung.")
        by_key[record.key] = record
        target_ids.add(record.target_id)
    rows, seen = [], set()
    for page in export.pages:
        if page.key in seen:
            raise ValueError("Quellenkennung im Export ist nicht eindeutig.")
        seen.add(page.key)
        record = by_key.get(page.key)
        if record is None:
            rows.append(Comparison(page, None, "new"))
            continue
        current_hash = current_hashes.get(record.target_id)
        if current_hash is None:
            status = "missing-target"
        else:
            if not isinstance(current_hash, str) or not _HASH.fullmatch(current_hash):
                raise ValueError("Ungültiger Hash des aktuellen Seitenstands.")
            remote_changed = page.source_hash != record.source_hash
            local_changed = current_hash != record.local_hash
            status = ("conflict" if local_changed else "changed") if remote_changed else (
                "local-only" if local_changed else "unchanged")
        rows.append(Comparison(page, record.target_id, status))
    return ReimportPlan(tuple(rows), tuple(sorted(set(by_key) - seen)))


def selected_changes(plan, selected_keys, overwrite_local_keys=()):
    selected, overwrite = set(selected_keys), set(overwrite_local_keys)
    rows = {row.page.key: row for row in plan.rows}
    if selected - rows.keys() or overwrite - selected:
        raise ValueError("Die Auswahl passt nicht mehr zum Importvergleich.")
    result = []
    for row in plan.rows:
        if row.page.key not in selected:
            continue
        if row.status in ("unchanged", "local-only"):
            raise ValueError("Unveränderte Quellen werden nicht erneut übernommen.")
        if row.status == "conflict" and row.page.key not in overwrite:
            raise ValueError("Der lokale Konflikt braucht eine ausdrückliche Entscheidung.")
        if row.status not in ("new", "changed", "conflict", "missing-target"):
            raise ValueError("Unbekannter Zustand im Importvergleich.")
        result.append(row)
    return tuple(result)
