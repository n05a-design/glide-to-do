# SPDX-License-Identifier: MPL-2.0
"""Zusammengehörige PNG-/Manifestdateien mit rückrollbarem Dateiaustausch."""
import os
from pathlib import Path
import shutil
import tempfile
import i18n as glide_i18n


class ExportRecoveryError(OSError):
    """Die vorherigen Dateien bleiben im genannten Sicherungsordner erhalten."""


def write_files(directory, files, *, replace=False):
    """Eine vorbereitete Ausgabe vollständig schreiben oder zurücknehmen.

    Der Aufrufer bestätigt vorhandene Zieldateien vor replace=True. Nur
    einfache Namen sind erlaubt; alle Dateien werden im selben Dateisystem
    vorbereitet. Ein fehlgeschlagener Rückweg darf seine Sicherungen behalten.
    """
    directory = Path(directory).resolve(strict=True)
    if not directory.is_dir() or not isinstance(files, dict) or not files:
        raise ValueError(glide_i18n.t("mod.animation_export.write_files.the_image_output_needs", "Die Bildausgabe braucht einen Ordner und Dateien."))
    for name, content in files.items():
        if (not isinstance(name, str) or not name or name in ('.', '..')
                or Path(name).name != name or '/' in name or '\\' in name
                or not isinstance(content, bytes)):
            raise ValueError(glide_i18n.t("mod.animation_export.write_files.invalid_output_file", "Ungültige Ausgabedatei."))
        target = directory / name
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError(glide_i18n.t("mod.animation_export.write_files.the_output_target_is", 'Das Ausgabeziel ist keine gewöhnliche Datei: {name}', name=name))
        if target.exists() and not replace:
            raise FileExistsError(glide_i18n.t("mod.animation_export.write_files.the_output_file_already", 'Die Ausgabedatei existiert bereits: {name}', name=name))
    stage = Path(tempfile.mkdtemp(prefix='.glide-animation-', dir=directory))
    prepared = stage / 'neu'
    backup = stage / 'vorher'
    prepared.mkdir()
    backup.mkdir()
    moved, written, reserved = [], [], []
    keep = False
    try:
        for name, content in files.items():
            with (prepared / name).open('xb') as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
        for name in files:
            target = directory / name
            if target.is_symlink() or (target.exists() and not target.is_file()):
                raise ValueError(glide_i18n.t("mod.animation_export.write_files.the_output_target_was", 'Das Ausgabeziel wurde verändert: {name}', name=name))
            if target.exists():
                if not replace:
                    raise FileExistsError(glide_i18n.t("mod.animation_export.write_files.the_output_file_already", 'Die Ausgabedatei existiert bereits: {name}', name=name))
                os.replace(target, backup / name)
                moved.append(name)
            else:
                # Ein zwischenzeitlich neu entstandenes Ziel nicht überschreiben.
                with target.open('xb'):
                    pass
                reserved.append(name)
            os.replace(prepared / name, target)
            written.append(name)
    except BaseException as cause:
        errors = []
        for name in reversed(tuple(dict.fromkeys(written + reserved))):
            try:
                (directory / name).unlink(missing_ok=True)
            except OSError as exc:
                errors.append(exc)
        for name in reversed(moved):
            try:
                os.replace(backup / name, directory / name)
            except OSError as exc:
                errors.append(exc)
        if errors:
            keep = True
            raise ExportRecoveryError(
                glide_i18n.t("mod.animation_export.write_files.the_output_failed_and", 'Die Ausgabe ist fehlgeschlagen und konnte nicht vollständig zurückgenommen werden. Die vorherigen Dateien bleiben hier erhalten: {str}', str=str(stage))) from cause
        raise
    finally:
        if not keep:
            shutil.rmtree(stage)
    return tuple(directory / name for name in files)
