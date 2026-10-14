"""Reale Bauquellen und native Startbelege der eigenständigen Pakete prüfen.

Die Vollmatrix prüft die Eingaben beider Zielpakete. Die tatsächlichen nativen
Bau-/Sperrproben bleiben eigene Pflichtnachweise und werden hier nicht ersetzt.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path


def run(repo, report=None, native=None):
    repo = repo.resolve()
    source = repo / 'src/glide'
    tools = repo / 'packaging/paket'
    required = ('baue_paket.py', 'start_glide.py', 'package_sources.py',
                'compiled_contract.py', 'license_contract.py',
                'pruefe_start_macos.py', 'pruefe_start_windows.py')
    assert all((tools / name).is_file() for name in required), 'Eigenständige Bau- und Startwege fehlen.'
    spec = importlib.util.spec_from_file_location('glide_package_sources_test', tools / 'package_sources.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    version = (repo / 'VERSION').read_text(encoding='utf-8').strip()
    product = module.identity((source / 'app.pyw').read_text(encoding='utf-8'), version)
    local_modules = {p.stem: p for p in source.glob('*.py') if p.name != 'drawing_prototype.py'}
    imports = set()
    for path in [source / 'app.pyw', *local_modules.values()]:
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split('.')[0])
    selected = {}
    for target, (_system, _machine, dnd) in module.TARGETS.items():
        files = module.manifest(source, target)
        assert set(local_modules) <= {Path(name).stem for name in files if '/' not in name}
        assert {name + '.py' for name in imports & local_modules.keys()} <= files.keys()
        assert all(hashlib.sha256((source / name).read_bytes()).hexdigest() == digest
                   for name, digest in files.items())
        native_dnd = [name for name in files if name.startswith('vendor/tkinterdnd2/tkdnd/')]
        assert native_dnd and all('/' + dnd + '/' in name for name in native_dnd)
        for resource in ('resources/fonts/provenance.json', 'resources/logo/glide-app-icon.svg',
                         'resources/timezones/provenance.json', 'vendor/provenance.json'):
            assert resource in files, resource
        requirements = repo / ('requirements/build-macos.txt' if target == 'macos-arm64'
                               else 'requirements/build-windows.txt')
        pins = [line.strip() for line in requirements.read_text(encoding='utf-8').splitlines()
                if line.strip() and not line.lstrip().startswith('#')]
        assert 'pyinstaller==6.22.3' in pins, 'Das gewählte Bauwerkzeug muss fest gepinnt bleiben.'
        assert all('==' in pin for pin in pins), 'Alle Bauabhängigkeiten brauchen eine feste Version.'
        selected[target] = len(files)
    result = dict(version=version, product=product, quellmodule=len(local_modules) + 1,
                  paketdateien=selected, exitcode=0,
                  native_abnahme='Separater nativer Bau, isolierter Start und Signatur-/Integritätsbeleg erforderlich.')
    if native is not None:
        proof = json.loads(native.read_text(encoding='utf-8'))
        assert proof.get('exitcode') == 0 and proof.get('paketprozess_exitcode') == 0
        package = proof.get('paket', {})
        assert package.get('exitcode') == 0 and package.get('app_version') == version
        assert package.get('eigenstaendiger_pruefstart') and package.get('daten_isoliert')
        assert not package.get('externe_python_suchpfade') and not package.get('callbackfehler')
        assert package.get('anlegen_abhaken_undo') and package.get('logo_geladen')
        assert package.get('dateilesen') and package.get('app_backup_rundlauf')
        if proof.get('plattform') == 'Windows x64':
            assert proof.get('nur_vergaenglicher_hosted_ci_runner')
            assert proof.get('externes_python_gegenprobe') != 0
            assert proof.get('externes_python_nach_restaurierung_exitcode') == 0
            assert proof.get('externe_quellen_lesegegenproben') == [True] * 4
            assert proof.get('acl_entsperrung_exitcodes') == [0] * 4
            assert proof.get('acl_restaurierung_exitcodes') == [0] * 4
            assert proof.get('acl_originale_wiederhergestellt') == [True] * 4
        result['nativer_startbeleg'] = dict(plattform=proof['plattform'], version=version, exitcode=0)
    if report:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Eigenständige Pakete: vollständige reale Bauquellen und Pins für beide Ziele grün;'
          + (' nativer Startbeleg geprüft.' if native else ' native Abnahme separat verpflichtend.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--report', type=Path)
    parser.add_argument('--startnachweis', type=Path)
    args = parser.parse_args()
    run(args.repo, args.report, args.startnachweis)
