"""Lesender Inventar-/Lieferabgleich für den ausdrücklich angeforderten Abnahmebericht."""
import ast
import hashlib
import json
from pathlib import Path
import re
import tarfile
import zipfile

REPO = Path(__file__).resolve().parents[3]
ROOT = REPO.parents[1]
OUT = Path(__file__).resolve().parent


def sha(path):
    hasher = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            hasher.update(block)
    return hasher.hexdigest()


def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    plan = ROOT / '00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md'
    sections = {}
    section = ''
    for number, line in enumerate(plan.read_text(encoding='utf-8').splitlines(), 1):
        if line.startswith('#'):
            section = line.lstrip('# ').strip()
        if line.startswith('|') and not re.match(r'^\|[ :|\-]+\|$', line):
            cells = [value.strip() for value in re.split(r'(?<!\\)\|', line)[1:-1]]
            sections.setdefault(section, []).append(dict(line=number, cells=cells))
    write('planregister.json', sections)
    code = REPO / 'src/glide/app.pyw'
    tree = ast.parse(code.read_text(encoding='utf-8'))
    app = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'ListApp')
    methods = {node.name: {'line': node.lineno, 'end': node.end_lineno}
               for node in app.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    modules = {path.name: sha(path) for path in (REPO / 'src/glide').glob('*.py')}
    missing = []
    for key, rows in sections.items():
        if not key.startswith(('18.2 ', '18.3 ')):
            continue
        for row in rows:
            for name in re.findall(r'`([\w_]+\.py)`', ' '.join(row['cells'])):
                if not (REPO / 'src/glide' / name).is_file() and not any(REPO.rglob(name)):
                    missing.append(dict(name=name, line=row['line'], section=key))
    write('codeinventar.json', {'version': (REPO / 'VERSION').read_text().strip(),
          'app_sha256': sha(code), 'app_lines': len(code.read_text().splitlines()),
          'listapp_methods': methods, 'direct_python_modules': modules,
          'missing_legacy_module_references': missing})
    historic = json.loads((REPO / 'tests/qa-3.45.0/paketabschluss_2026-10-26/lieferung.json').read_text())
    packages = []
    for kind, path_key, sha_key in [('windows', 'windows_zip', 'windows_zip_sha256'),
                                    ('macos', 'mac_tar', 'mac_tar_sha256')]:
        path = ROOT / historic[path_key]
        actual = sha(path) if path.is_file() else None
        row = {'kind': kind, 'path': historic[path_key], 'exists': path.is_file(),
               'sha256': actual, 'historical_sha256': historic[sha_key],
               'historical_bytes_equal': actual == historic[sha_key]}
        metadata = []
        if kind == 'windows' and actual:
            with zipfile.ZipFile(path) as archive:
                for name in archive.namelist():
                    if name.endswith('glide-input.json') and archive.getinfo(name).file_size < 1024*1024:
                        metadata.append(json.loads(archive.read(name)))
        elif actual:
            with tarfile.open(path, 'r:gz') as archive:
                for member in archive:
                    if member.name.endswith('glide-input.json') and member.isfile() and member.size < 1024*1024:
                        metadata.append(json.load(archive.extractfile(member)))
        row['embedded_versions'] = sorted({value.get('version', '') for value in metadata})
        packages.append(row)
    python_files = sorted((ROOT / '07_Python-Versionen').glob('Glide*.pyw'))
    deliveries = []
    for path in python_files:
        text = path.read_text(encoding='utf-8-sig')
        version = re.search(r'^APP_VERSION\s*=\s*[\"\']([^\"\']+)', text, re.M)
        schema = re.search(r'^\s+DATA_SCHEMA_VERSION\s*=\s*(\d+)', text, re.M)
        deliveries.append({'path': str(path.relative_to(ROOT)), 'sha256': sha(path),
                           'version': version.group(1) if version else None,
                           'schema': schema.group(1) if schema else None})
    write('lieferstand.json', {'packages': packages, 'python': deliveries,
                              'native_signatures_rechecked': False,
                              'native_starts_rechecked': False})
    print('Inventar:', len(methods), 'ListApp-Methoden,', len(modules), 'Module; alte Modulverweise:',
          [entry['name'] for entry in missing])
    print('Lieferung:', [(entry['kind'], entry['embedded_versions'], entry['historical_bytes_equal'])
                         for entry in packages], [(entry['version'],entry['schema']) for entry in deliveries])


if __name__ == '__main__':
    main()
