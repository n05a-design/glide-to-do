# SPDX-License-Identifier: MPL-2.0
"""Typregel und verständliche Rückfrage für aktive Anhänge, ohne Tk."""
from pathlib import PurePath
import os
import i18n as glide_i18n

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
        return glide_i18n.t("mod.attachment_policy.origin_text.glide_data_storage_may", 'Glide-Datenablage; kann auch aus einer Sicherung oder Vorlage stammen')
    return glide_i18n.t("mod.attachment_policy.origin_text.local_file_outside_the", 'Lokale Datei außerhalb der Glide-Datenablage')


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
    origin = origin or glide_i18n.t("mod.attachment_policy.question.glide_data_storage_may", 'Glide-Datenablage; kann auch aus einer Sicherung oder Vorlage stammen')
    return (glide_i18n.t("mod.attachment_policy.question.has_the_executable_or", '„{display}“ hat den ausführbaren oder skriptfähigen Dateityp {suffix}.\n\nHerkunft: {origin}\nDatei: {path}\n\nBeim Öffnen kann das Betriebssystem Programme oder Skripte ausführen. Öffne die Datei nur, wenn du ihrer Herkunft vertraust.\n\nDiesen Anhang jetzt öffnen?', display=display, suffix=suffix, origin=origin, path=path))
