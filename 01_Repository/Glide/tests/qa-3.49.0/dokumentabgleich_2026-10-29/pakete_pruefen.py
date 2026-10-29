"""Lesender Liefer-/Ressourcenabgleich; kein Bau, Appstart oder Entpacken."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tarfile
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
REPO = ROOT / '01_Repository/Glide'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


errors = []
result = {'date': '2026-10-29', 'errors': errors, 'package_build': False, 'package_execution': False}
old = read(REPO / 'tests/qa-3.45.0/paketabschluss_2026-10-26/lieferung.json')
for key in ['windows_zip', 'mac_tar']:
    actual = digest(ROOT / old[key])
    result[key] = {'path': old[key], 'sha256': actual, 'matches': actual == old[key + '_sha256']}
    if not result[key]['matches']:
        errors.append(key + ': Hash abweichend')
windows_count = mac_count = link_count = 0
with zipfile.ZipFile(ROOT / old['windows_zip']) as archive:
    for member in archive.infolist():
        if member.is_dir():
            continue
        path = REPO / 'build/windows' / member.filename
        if not path.is_file() or digest(path) != hashlib.sha256(archive.read(member)).hexdigest():
            errors.append('Windows-Inspektionsdatei: ' + member.filename)
        windows_count += 1
with tarfile.open(ROOT / old['mac_tar'], 'r:gz') as archive:
    for member in archive.getmembers():
        path = REPO / 'build/macos' / member.name
        if member.isfile():
            with archive.extractfile(member) as stream:
                wanted = hashlib.sha256(stream.read()).hexdigest()
            if not path.is_file() or digest(path) != wanted:
                errors.append('Mac-Inspektionsdatei: ' + member.name)
            mac_count += 1
        elif member.issym():
            try:
                if os.readlink(path).replace('\\', '/') != member.linkname:
                    errors.append('Mac-Linkziel: ' + member.name)
            except OSError:
                errors.append('Mac-Link nicht lesbar: ' + member.name)
            link_count += 1
result.update(windows_files=windows_count, mac_files=mac_count, mac_links=link_count)

delivery = read(REPO / 'tests/qa-3.47.0/folgepakete_2026-10-27/quellstand.json')
delivery_count = 0
for name, wanted in {**delivery['runtime'], **delivery['resources']}.items():
    if name == 'drawing_prototype.pyw':
        continue
    target = {'app.pyw': 'Glide-Aufgaben-und-Listen_v3.47.0.pyw', 'glide_start.py': 'Schnellstart.pyw'}.get(name, name)
    path = ROOT / '07_Python-Versionen' / target
    if not path.is_file() or digest(path) != wanted:
        errors.append('Python-Lieferung 3.47.0: ' + target)
    delivery_count += 1
result['python_delivery_files'] = delivery_count
result['python_delivery_version'] = '3.47.0'
result['native_delivery_version'] = '3.45.0'
showcases = []
for folder in [REPO / 'tests/fixtures/showcase', ROOT / '05_Probelisten_Testdaten/Showcase']:
    manifest = read(folder / 'manifest.json')
    for name, row in manifest['dateien'].items():
        path = folder / name
        if not path.is_file() or path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
            errors.append('Showcase-Manifest: ' + (folder / name).relative_to(ROOT).as_posix())
    showcases.append({'path': folder.relative_to(ROOT).as_posix(), 'version': manifest['app_version'],
                      'schema': manifest['format_version'], 'files': len(manifest['dateien'])})
result['showcases'] = showcases

source = REPO / 'src/glide'
runtime = {p.name for p in source.iterdir() if p.is_file() and (p.name == 'app.pyw' or p.suffix == '.py')}
result['runtime_files'] = len(runtime)
mac_tree = ast.parse((REPO / 'packaging/macos/baue_app.py').read_bytes())
mac_list = next(ast.literal_eval(node.value) for node in mac_tree.body if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'DATEIEN' for t in node.targets))
if set(mac_list) != runtime:
    errors.append('Mac-Vorstufe: Quellliste abweichend')
python_tree = ast.parse((REPO / 'scripts/pflege/abgleich_07.py').read_bytes())
python_list = {'app.pyw', 'glide_start.py'}
for node in python_tree.body:
    if isinstance(node, ast.For) and isinstance(node.target, ast.Name) and node.target.id == 'modul':
        python_list.update(ast.literal_eval(node.iter))
if python_list != runtime:
    errors.append('Python-Abgleicher: Quellliste abweichend')
spec = importlib.util.spec_from_file_location('glide_package_sources_audit', REPO / 'packaging/paket/package_sources.py')
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)
result['package_source_manifests'] = {}
for target in ['windows-x64', 'macos-arm64']:
    manifest = package.manifest(source, target)
    top = {p for p in manifest if '/' not in p}
    if top != runtime:
        errors.append(target + ': Quellliste abweichend')
    result['package_source_manifests'][target] = {'files': len(manifest), 'runtime_files': len(top),
                                               'sha256': hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()}
protected = read(REPO / 'tests/qa-3.48.0/dokumentationsaudit_2026-10-27/beweissicherung_lokal.json')
for row in protected['files']:
    path = REPO / 'tests/qa-3.48.0' / row['path']
    if not path.is_file() or digest(path) != row['sha256']:
        errors.append('WA-41-Originalbeleg: ' + row['path'])
result['protected_wa41_files'] = len(protected['files'])
result['native_signatures_rechecked'] = False
result['native_starts_rechecked'] = False
(OUT / 'pakete_und_ressourcen.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
