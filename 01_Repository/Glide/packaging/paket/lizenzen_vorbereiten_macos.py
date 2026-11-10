# SPDX-License-Identifier: MPL-2.0
"""Geprüften Mac-Lizenzbestand für die tatsächliche Baulaufzeit bereitstellen.

Die eingecheckten Originaltexte gelten für ihre belegten Komponentenversionen.
Eine abweichende Laufzeit braucht einen neuen Bestand und neue Originalbelege.
"""
import argparse
import copy
import ctypes
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import sys
from project_license import stage_project_license

BUILD = {'pyinstaller': 'PyInstaller', 'pyinstaller-hooks-contrib': 'PyInstaller-Hooks',
         'altgraph': 'altgraph', 'macholib': 'macholib', 'packaging': 'packaging',
         'setuptools': 'setuptools'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verified_basis(basis, runtime, versions):
    basis = basis.resolve()
    document = json.loads((basis / 'manifest.json').read_text(encoding='utf-8'))
    if document.get('runtime') != runtime:
        raise ValueError('Lizenzbasis und tatsächliche Baulaufzeit unterscheiden sich; neue Originalbelege erforderlich.')
    components = document.get('components', [])
    records = {record['name']: record for record in components}
    if len(records) != len(components):
        raise ValueError('Doppelte Lizenzkomponente.')
    for distribution, component in BUILD.items():
        if records.get(component, {}).get('version') != versions.get(distribution):
            raise ValueError('Abweichende Bauabhängigkeit: ' + distribution)
    for record in components:
        if not record.get('source') or not record.get('files'):
            raise ValueError('Unvollständige Lizenzkomponente.')
        for name, digest in record['files'].items():
            path = basis / name
            if Path(name).name != name or '\\' in name or path.is_symlink() or not path.is_file():
                raise ValueError('Ungültiger Lizenzpfad: ' + name)
            if sha(path) != digest or not path.read_bytes().strip():
                raise ValueError('Lizenzbeleg stimmt nicht: ' + name)
    return copy.deepcopy(document)


def copy_external_licenses(document, basis, destination):
    """Keep the pinned basis for build dependencies, not obsolete Glide licenses."""
    for record in document['components']:
        if record['name'] == 'Glide':
            continue
        for name in record['files']:
            shutil.copy2(basis / name, destination / name)


def native_versions():
    import _decimal
    import _lzma
    import sqlite3
    import ssl
    zstd = ctypes.CDLL(str(Path(sys.base_prefix) / 'lib/libzstd.1.dylib'))
    zstd.ZSTD_versionString.restype = ctypes.c_char_p
    lzma = ctypes.CDLL(_lzma.__file__)
    lzma.lzma_version_string.restype = ctypes.c_char_p
    return {'OpenSSL': ssl.OPENSSL_VERSION.split()[1],
            'Zstandard': zstd.ZSTD_versionString().decode('ascii'),
            'liblzma': lzma.lzma_version_string().decode('ascii'),
            'SQLite': sqlite3.sqlite_version, 'libmpdec': _decimal.__libmpdec_version__}


def prepare(source, repo, destination, basis):
    from baue_paket import check_native
    runtime = check_native('macos-arm64')
    versions = {name: importlib.metadata.version(name) for name in BUILD}
    document = verified_basis(basis, runtime, versions)
    records = {record['name']: record for record in document['components']}
    for name, version in native_versions().items():
        if records.get(name, {}).get('version') != version:
            raise ValueError('Abweichende native Bibliothek: ' + name)
    destination.mkdir(parents=True, exist_ok=False)
    copy_external_licenses(document, basis, destination)
    # Projektbelege kommen aus genau dem anschließend gebauten Quellstand.
    current = {'tkinterdnd2-LICENSE': source / 'vendor/tkinterdnd2/LICENSE',
               'DejaVu-LICENSE': source / 'resources/fonts/LICENSE',
               'PixelifySans-OFL.txt': source / 'resources/fonts/OFL-PixelifySans.txt',
               'DMMono-OFL.txt': source / 'resources/fonts/OFL-DMMono.txt',
               'Rubik-OFL.txt': source / 'resources/fonts/OFL-Rubik.txt',
               'DMSerifDisplay-OFL.txt': source / 'resources/fonts/OFL-DMSerifDisplay.txt',
               'CharisSIL-OFL.txt': source / 'resources/fonts/OFL-CharisSIL.txt',
               'IANA-LICENSE.txt': source / 'resources/timezones/LICENSE-iana.txt',
               'CLDR-LICENSE.txt': source / 'resources/timezones/LICENSE-CLDR.txt'}
    for name, original in current.items():
        shutil.copy2(original, destination / name)
    for record in document['components']:
        for name in record['files']:
            record['files'][name] = sha(destination / name)
    # Die Basis ist ein unveränderter historischer Fremdcodebeleg. Nur der
    # neu erzeugte Bestand erhält Glides heute geltende Lizenz und Quellen.
    document['components'] = [record for record in document['components'] if record['name'] != 'Glide']
    document['components'].append(stage_project_license(repo, destination, source))
    document.update(bauabhaengigkeiten=versions,
                    abnahme='Originalbelege und Baulaufzeit abgeglichen; native Paketzuordnung und Start separat.')
    (destination / 'manifest.json').write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(len(document['components']), 'Komponenten passend zur tatsächlichen Mac-Baulaufzeit bereitgestellt.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quelle', type=Path, required=True)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--ziel', type=Path, required=True)
    parser.add_argument('--basis', type=Path, default=Path(__file__).with_name('lizenzen') / 'macos')
    args = parser.parse_args()
    prepare(args.quelle.resolve(), args.repo.resolve(), args.ziel.resolve(), args.basis.resolve())
