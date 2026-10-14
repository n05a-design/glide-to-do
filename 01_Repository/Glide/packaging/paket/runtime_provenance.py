"""Geprüfte eigene Tk-9.1-Eingaben vor dem Paketbau, ohne App-/Tk-Import."""
import hashlib
import json
from pathlib import Path, PurePosixPath


def validate_runtime_proof(manifest, runtime, extension, *, pins, patches):
    manifest = Path(manifest).resolve()
    root = manifest.parent
    proof = json.loads(manifest.read_text(encoding='utf-8'))
    if (runtime['tcl'] != '9.1.0' or runtime['tk_compiled'] != '9.1' or
            any(proof.get(key) != runtime[key] for key in ('python', 'platform', 'machine')) or
            proof.get('quellpins') != pins or proof.get('runtime_patches') != patches):
        raise ValueError('Eigene Laufzeit, Quellpins und Runtimekorrekturen stimmen nicht überein.')
    extension = Path(extension).resolve()
    if (Path(proof['extension']).resolve() != extension or
            not extension.is_relative_to(root / 'python-extension') or
            Path(proof['runtime']).resolve() != root / 'runtime'):
        raise ValueError('Paketbau verwendet nicht die ausdrücklich geprüfte eigene _tkinter-Laufzeit.')
    hashes = proof.get('sha256', {})
    if not hashes or extension.relative_to(root).as_posix() not in hashes:
        raise ValueError('Vollständige Runtime-Prüfsummen einschließlich _tkinter fehlen.')
    for relative, expected in hashes.items():
        path = PurePosixPath(relative)
        if (not path.parts or path.is_absolute() or path.as_posix() != relative or '..' in path.parts or
                '\\' in relative or path.parts[0] not in ('runtime', 'python-extension')):
            raise ValueError('Ungültiger Runtime-Prüfpfad.')
        actual = root / relative
        if (not actual.resolve().is_relative_to(root) or not actual.is_file() or
                hashlib.sha256(actual.read_bytes()).hexdigest() != expected):
            raise ValueError('Eigene Runtime wurde nach ihrer nativen Prüfung verändert: '+relative)
    actual_files = {path.relative_to(root).as_posix()
                    for folder in ('runtime', 'python-extension') for path in (root / folder).rglob('*')
                    if path.is_file()}
    if actual_files != set(hashes):
        raise ValueError('Der Dateibestand der geprüften Runtime wurde verändert.')
    return dict(quellpins=pins, runtime_patches=patches, dateien=len(hashes),
                manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest())
