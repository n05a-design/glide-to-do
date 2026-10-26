"""Sicherungsinventar und Auswahlmodell ohne Tk oder Inhaltsänderungen."""
from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path

TYPES = {'.json': 'Aufgaben (JSON)', '.glidebackup': 'Aufgabensicherung',
         '.glideapp': 'App-Sicherung'}


@dataclass(frozen=True)
class Entry:
    path: str
    name: str
    modified: float
    size: int
    kind: str

    @property
    def date_text(self):
        return datetime.fromtimestamp(self.modified).strftime('%d.%m.%Y %H:%M')

    @property
    def size_text(self):
        if self.size < 1024:
            return f'{self.size} B'
        if self.size < 1024 * 1024:
            return f'{self.size / 1024:.1f} KiB'.replace('.', ',')
        return f'{self.size / (1024 * 1024):.1f} MiB'.replace('.', ',')


def inspect(path):
    """Nur Metadaten; der tatsächliche Inhalt wird gesondert geprüft."""
    path = Path(path).absolute()
    kind = TYPES.get(path.suffix.lower())
    if kind is None or not path.is_file() or path.is_symlink():
        raise ValueError('Bitte eine JSON-, Aufgaben- oder App-Sicherung wählen.')
    info = path.stat()
    return Entry(str(path), path.name, info.st_mtime, info.st_size, kind)


def scan(directory, extra=(), limit=500):
    """Neueste Sicherungsdateien zuerst, doppelte Pfade nur einmal."""
    paths, errors = list(extra), []
    try:
        with os.scandir(directory) as entries:
            paths.extend(entry.path for entry in entries
                         if Path(entry.name).suffix.lower() in TYPES
                         and entry.is_file(follow_symlinks=False))
    except FileNotFoundError:
        pass  # Vor der ersten Sicherung ist ein fehlender Ordner normal.
    except OSError:
        errors.append('Der Sicherungsordner konnte nicht vollständig gelesen werden.')
    found = {}
    for path in paths:
        try:
            entry = inspect(path)
            found[os.path.normcase(entry.path)] = entry
        except (OSError, ValueError):
            errors.append(f'{Path(path).name}: Datei nicht verfügbar.')
    ordered = sorted(found.values(), key=lambda entry: (-entry.modified, entry.path.casefold()))
    if len(ordered) > limit:
        errors.append(f'Angezeigt werden die neuesten {limit} Sicherungen.')
    return ordered[:limit], errors


def filtered(entries, query):
    parts = str(query).casefold().split()
    return [entry for entry in entries if all(
        part in f'{entry.name} {entry.kind} {entry.date_text}'.casefold() for part in parts)]


def choice_label(sources, path):
    """Gleichnamige Dateien verschiedener Ordner erhalten getrennte Einträge."""
    key = os.path.normcase(os.path.abspath(path))
    for name, existing in sources:
        if existing is not None and os.path.normcase(os.path.abspath(existing)) == key:
            return name
    base = f'Datei: {Path(path).name}'
    label, number = base, 2
    names = {name for name, _ in sources}
    while label in names:
        label = f'{base} · {number}'
        number += 1
    return label


def describe(data):
    """Listen-/Punktzahlen eines bereits begrenzt eingelesenen Sicherungsstands."""
    stack = list(data.get('lists', ()))
    lists = len(stack)
    stack = [item for entry in stack if isinstance(entry, dict)
             for item in (entry.get('items') or ())]
    count, completed = 0, 0
    while stack:
        item = stack.pop()
        if not isinstance(item, dict):
            continue
        count += 1
        completed += bool(item.get('done'))
        stack.extend(item.get('children') or ())
    version = data.get('version', data.get('data_version', data.get('schema_version', 'nicht angegeben')))
    return f'{lists} Listen · {count} Punkte · {completed} erledigt · Speicherstufe {version}'
