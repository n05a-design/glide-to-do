"""Verbindliche native Kernprüfung ab Glide 4, ohne Tk-/App-Import."""
import re


def native_zugangspruefung(version, *, angefordert=False):
    match = re.fullmatch(r'(\d+)\.(\d+)\.(\d+)', version)
    if match is None:
        raise ValueError('Eindeutige Glide-Version für den Zugangsprüfvertrag erforderlich.')
    return angefordert or int(match[1]) >= 4
