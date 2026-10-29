"""Vorhandene Lieferarchive/Inspektionskopien lesen; kein Bau oder Appstart."""
import hashlib
import json
import os
from pathlib import Path
import tarfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
REPO = ROOT / '01_Repository/Glide'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


result = dict(application_tests_started=False, errors=[], native_version='3.45.0',
    package_execution=False, package_build=False)
old = json.loads((REPO / 'tests/qa-3.45.0/paketabschluss_2026-10-26/lieferung.json').read_text(encoding='utf-8'))
for key in ('windows_zip', 'mac_tar'):
    path = ROOT / old[key]
    actual = digest(path)
    result[key] = dict(path=old[key], sha256=actual, matches=actual == old[key + '_sha256'])
    if actual != old[key + '_sha256']:
        result['errors'].append(key + ': Archivhash abweichend')
windows_count = 0
with zipfile.ZipFile(ROOT / old['windows_zip']) as z:
    for member in z.infolist():
        if member.is_dir():
            continue
        path = REPO / 'build/windows' / member.filename
        if not path.is_file() or digest(path) != hashlib.sha256(z.read(member)).hexdigest():
            result['errors'].append('Windows-Paketdatei: ' + member.filename)
        windows_count += 1
mac_count, link_count = 0, 0
with tarfile.open(ROOT / old['mac_tar'], 'r:gz') as t:
    for member in t.getmembers():
        path = REPO / 'build/macos' / member.name
        if member.isfile():
            with t.extractfile(member) as f:
                expected = hashlib.sha256(f.read()).hexdigest()
            if not path.is_file() or digest(path) != expected:
                result['errors'].append('Mac-Inspektionsdatei: ' + member.name)
            mac_count += 1
        elif member.issym():
            try:
                actual = os.readlink(path).replace('\\', '/')
                if actual != member.linkname:
                    result['errors'].append('Mac-Linkziel: ' + member.name)
            except OSError:
                result['errors'].append('Mac-Link nicht lesbar: ' + member.name)
            link_count += 1
result.update(windows_files=windows_count, mac_files=mac_count, mac_links=link_count)
showcase = []
for directory in (REPO / 'tests/fixtures/showcase', ROOT / '05_Probelisten_Testdaten/Showcase'):
    manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
    for name, row in manifest['dateien'].items():
        path = directory / name
        if path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
            result['errors'].append('Showcase-Manifest: ' + str(path.relative_to(ROOT)))
    showcase.append(dict(path=directory.relative_to(ROOT).as_posix(), app_version=manifest['app_version'],
        schema=manifest['format_version'], files=len(manifest['dateien'])))
result['showcase'] = showcase
saved = json.loads((HERE / 'beweissicherung_lokal.json').read_text(encoding='utf-8'))
result['saved_evidence_files'] = len(saved['files'])
for row in saved['files']:
    path = HERE.parent / row['path']
    if digest(path) != row['sha256']:
        result['errors'].append('Lokaler WA-41-Beleg: ' + row['path'])
external = Path(os.environ['USERPROFILE']) / 'OneDrive - Ebner GmbH/Dokumente/WA41_Beweissicherung_20261027_162505'
result['reported_external_backup_exists'] = external.exists()
(HERE / 'pakete_und_belege.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(result['errors']))
