"""Gezielte Runtimekorrekturen ausschließlich auf gepinnte Baukopien anwenden."""
import hashlib
import json
from pathlib import Path
import subprocess

from runtime_contract import PINS


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def apply_patches(source, system, *, definitions=None):
    definitions = Path(definitions) if definitions else Path(__file__).with_name('patches.json')
    base = definitions.resolve().parent
    manifest = json.loads(definitions.read_text(encoding='utf-8'))
    if manifest['tk_pin'] != PINS['tk']:
        raise ValueError('Runtimepatch und Tk-Originalpin stimmen nicht überein.')
    source = Path(source).resolve()
    records = []
    for entry in manifest['patches']:
        if entry['platform'] not in (system, 'all'):
            continue
        target = (source / entry['file']).resolve()
        patch = (base / entry['patch']).resolve()
        if not target.is_relative_to(source) or not patch.is_relative_to(base):
            raise ValueError('Runtimepatch liegt außerhalb seiner Bau-/Werkzeugquelle.')
        if digest(target) != entry['before_sha256'] or digest(patch) != entry['patch_sha256']:
            raise ValueError('Runtimepatch benötigt die exakten Original- und Diffbytes.')
        # Git for Windows erbt häufig autocrlf; ein Baupatch muss dagegen
        # exakt seine belegten Bytes erzeugen, ohne globale Git-Änderungen.
        command = ['git', '-c', 'core.autocrlf=false', '-c', 'core.eol=lf', 'apply', '--whitespace=nowarn']
        subprocess.run([*command, '--check', str(patch)], cwd=source, check=True)
        subprocess.run([*command, str(patch)], cwd=source, check=True)
        if digest(target) != entry['after_sha256']:
            raise ValueError('Runtimepatch hat nicht die geprüften Ergebnisbytes erzeugt.')
        records.append(dict(entry))
    return records
