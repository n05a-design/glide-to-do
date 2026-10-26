"""Typregel und verständliche Rückfrage für aktive Anhänge, ohne Tk."""
from pathlib import PurePath
import os

ACTIVE_TYPES = frozenset({'.exe', '.com', '.bat', '.cmd', '.ps1', '.psm1', '.psd1',
    '.vbs', '.vbe', '.js', '.jse', '.msi', '.msp', '.scr', '.lnk', '.url', '.hta',
    '.reg', '.cpl', '.msc', '.wsf', '.wsh', '.scf', '.jar', '.py', '.pyw', '.sh',
    '.bash', '.zsh', '.fish', '.command', '.desktop', '.app', '.workflow'})


def origin_text(path, data_folder):
    try:
        base = os.path.normcase(os.path.realpath(data_folder))
        stored = os.path.commonpath((base, os.path.normcase(os.path.realpath(path)))) == base
    except (OSError, ValueError):
        stored = False
    if stored:
        return 'Glide-Datenablage; kann auch aus einer Sicherung oder Vorlage stammen'
    return 'Lokale Datei außerhalb der Glide-Datenablage'


def active_type(path, name=''):
    """Auch die tatsächliche Speicherendung prüfen, wenn der Anzeigename abweicht."""
    for value in (path, name):
        suffix = PurePath(str(value or '').rstrip(' .')).suffix.casefold()
        if suffix in ACTIVE_TYPES:
            return suffix
    return None


def question(path, name='', origin=None):
    suffix = active_type(path, name)
    if suffix is None:
        return None
    display = str(name or PurePath(str(path)).name)
    origin = origin or 'Glide-Datenablage; kann auch aus einer Sicherung oder Vorlage stammen'
    return (f'„{display}“ hat den ausführbaren oder skriptfähigen Dateityp {suffix}.\n\n'
            f'Herkunft: {origin}\nDatei: {path}\n\n'
            'Beim Öffnen kann das Betriebssystem Programme oder Skripte ausführen. '
            'Öffne die Datei nur, wenn du ihrer Herkunft vertraust.\n\n'
            'Diesen Anhang jetzt öffnen?')
