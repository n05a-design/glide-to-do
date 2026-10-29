"""Lesendes lokales Datei-/Dokumentaudit; schreibt nur eigene datierte Nachweise."""
import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit, unquote

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
REPO = ROOT / '01_Repository/Glide'
sys.path.insert(0, str(REPO / 'tests/tools'))
import standpruefung as stand
import ci_grundstufe as ci


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


old = module('audit_helpers', REPO / 'tests/qa-3.48.0/dokumentationsaudit_2026-10-27/pruefen.py')
checks = module('formal_checks', REPO / 'tests/tools/pruefen.py')


def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stand', choices=['vorher', 'nachher'], required=True)
    phase = parser.parse_args().stand
    rows, errors, excluded = [], [], []
    own = OUT.relative_to(ROOT).as_posix() + '/'
    for parent, dirs, files in os.walk(ROOT, followlinks=False):
        parent = Path(parent)
        for child in list(dirs):
            p = parent / child
            rel = p.relative_to(ROOT).as_posix()
            if child == '.git' or rel == '.claude/worktrees' or p.is_symlink() or p.is_junction() or (p / '.git').exists():
                dirs.remove(child)
                excluded.append({'path': rel, 'reason': 'Git-Verwaltung, separater Checkout oder Verknuepfung'})
        for file in files:
            p = parent / file
            name = p.relative_to(ROOT).as_posix()
            if name.startswith(own):
                continue
            try:
                meta = p.lstat()
                attrs = getattr(meta, 'st_file_attributes', 0)
                cloud = bool(attrs & (0x1000 | 0x40000 | 0x400000))
                row = {'path': name, 'bytes': meta.st_size, 'attributes': attrs,
                       'category': old.category(name), 'cloud_placeholder': cloud}
                if p.is_symlink():
                    row['link_target'] = os.readlink(p)
                elif not cloud and row['category'] != 'private Arbeitsdaten (nur Metadaten)':
                    row['sha256'] = old.digest(p)
                rows.append(row)
            except (OSError, ValueError) as exc:
                errors.append({'path': name, 'error': type(exc).__name__, 'message': str(exc).replace(str(Path.home()), '%USERPROFILE%')})
    rows.sort(key=lambda row: row['path'])
    write(f'inventar_{phase}.json', {'files': rows, 'excluded': excluded, 'errors': errors})
    candidates = set(old.git('ls-files', '--cached', '--others', '--exclude-standard', '-z').split('\0')) - {''}
    docs, texts = [], {}
    syntax_count = json_count = 0
    syntax_errors, json_errors = [], []
    for row in rows:
        n = row['path']
        if not row.get('sha256') or n not in candidates or '/vendor/' in n or row['category'] in {'lokale Tk-Pruefumgebung', 'Paket/Bauartefakt'}:
            continue
        p = ROOT / n
        if p.suffix == '.md':
            try:
                text = p.read_text(encoding='utf-8-sig')
                texts[n] = text
                docs.append({'path': n, 'sha256': row['sha256'], 'historical': old.historical(n),
                             'stand': [line for line in text.splitlines() if line.startswith('Stand ')][:2]})
            except UnicodeError as exc:
                errors.append({'path': n, 'error': str(exc)})
        if p.suffix in {'.py', '.pyw'} and not n.startswith('07_Python-Versionen/') and '/Archiv/' not in n:
            try:
                ast.parse(p.read_bytes(), filename=n)
                syntax_count += 1
            except (SyntaxError, ValueError, UnicodeError) as exc:
                syntax_errors.append({'path': n, 'error': str(exc)})
        if p.suffix == '.json':
            try:
                json.loads(p.read_text(encoding='utf-8-sig'))
                json_count += 1
            except (ValueError, UnicodeError) as exc:
                json_errors.append({'path': n, 'error': str(exc)})
    write(f'dokumentregister_{phase}.json', docs)
    links, broken = 0, []
    for n, text in texts.items():
        for num, line in enumerate(old.without_code(text).splitlines(), 1):
            for target in re.findall(r'!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+["\'][^)]*)?\)', line):
                target = target.strip('<>')
                parts = urlsplit(target)
                if parts.scheme or target.startswith('//'):
                    continue
                links += 1
                dest = (ROOT / n).parent / unquote(parts.path)
                issue = None
                if not dest.exists():
                    issue = 'Datei fehlt'
                elif parts.fragment and dest.suffix.lower() == '.md' and unquote(parts.fragment) not in old.anchors(dest.read_text(encoding='utf-8-sig')):
                    issue = 'Anker fehlt'
                if issue:
                    broken.append({'source': n, 'filtered_line': num, 'target': target,
                                   'historical': old.historical(n), 'issue': issue})
    write(f'verweise_{phase}.json', {'local_links': links, 'findings': broken})
    result_checks = {}
    for name in ['dokumentation', 'fixtures', 'versionen']:
        try:
            result_checks[name] = getattr(checks, name + '_pruefen')()
        except Exception as exc:
            errors.append({'check': name, 'error': str(exc)})
    checked = stand.lauf([ROOT], (REPO / 'VERSION').read_text().strip())
    screenshots = json.loads((ROOT / '00_Arbeitsvorbereitung/Featurepaket_UI_UX/screenshots.json').read_text(encoding='utf-8'))
    bad_images = [r['id'] for r in screenshots['bilder'] if old.digest(ROOT / '00_Arbeitsvorbereitung/Featurepaket_UI_UX' / r['datei']) != r['sha256']]
    baseline = json.loads((REPO / 'tests/qa-3.49.0/abnahme_2026-10-28/eingefroren.json').read_text(encoding='utf-8'))
    changed = [n for n, h in baseline['source_sha256'].items() if not (ROOT / n).is_file() or old.digest(ROOT / n) != h]
    delivery = json.loads((REPO / 'tests/qa-3.49.0/abnahme_2026-10-28/lieferstand.json').read_text(encoding='utf-8'))
    archive_errors = [r['path'] for r in delivery['packages'] if old.digest(ROOT / r['path']) != r['sha256']]
    docstring_only = []
    allowed_tool = '01_Repository/Glide/scripts/pflege/abgleich_07.py'
    if allowed_tool in changed:
        frozen = Path(baseline['copy'].replace('%USERPROFILE%', str(Path.home()))) / 'projekt' / allowed_tool
        assert old.digest(frozen) == baseline['source_sha256'][allowed_tool]
        before_tree, after_tree = ast.parse(frozen.read_bytes()), ast.parse((ROOT / allowed_tool).read_bytes())
        before_tree.body[0].value.value = after_tree.body[0].value.value = ''
        if ast.dump(before_tree) == ast.dump(after_tree):
            docstring_only.append(allowed_tool)
    result = {
        'date': '2026-10-29', 'version': '3.49.0', 'files': len(rows),
        'hashed': sum('sha256' in r for r in rows), 'links': sum('link_target' in r for r in rows),
        'categories': dict(Counter(r['category'] for r in rows)),
        'documents': len(docs), 'active_documents': sum(not r['historical'] for r in docs),
        'registered_stand_documents': checked.fortgeschrieben + checked.festgeschrieben + checked.ohne_stand,
        'local_links': links, 'active_link_findings': [r for r in broken if not r['historical']],
        'historical_link_findings': [r for r in broken if r['historical']],
        'stand_errors': checked.fehler, 'python_syntax_files': syntax_count,
        'python_syntax_errors': syntax_errors, 'json_files': json_count, 'json_errors': json_errors,
        'formal_checks': result_checks, 'source_changes_since_audit': changed,
        'tool_docstring_only_ast_verified': docstring_only,
        'unexpected_non_document_changes': [n for n in changed if not n.endswith('.md') and n not in docstring_only],
        'archive_errors': archive_errors, 'delivery_differences': ci.lieferstand_abweichungen(),
        'reference_images': len(screenshots['bilder']), 'reference_image_errors': bad_images,
        'cloud_placeholders': [r['path'] for r in rows if r['cloud_placeholder']], 'errors': errors,
        'application_tests_started': False, 'external_web_pages_revalidated': False,
        'release_approved': False,
        'limits': ['Private Arbeitsdaten nur Metadaten; Git und weitere Checkouts ausgegrenzt.',
                   'Syntax, Hashes, Formate und Dokumentabgleich ersetzen keine neue Voll-/Native-/Menschenabnahme.']}
    write(f'ergebnis_{phase}.json', result)
    print(json.dumps({'phase': phase, 'files': len(rows), 'documents': len(docs), 'local_links': links,
                      'active_link_findings': [r for r in broken if not r['historical']],
                      'historical_link_findings': len([r for r in broken if r['historical']]),
                      'errors': errors, 'stand_errors': checked.fehler,
                      'syntax_errors': syntax_errors, 'json_errors': json_errors}, ensure_ascii=False, indent=2))
    fatal = (errors or checked.fehler or broken or syntax_errors or json_errors or archive_errors
             or bad_images or result['unexpected_non_document_changes'])
    raise SystemExit(bool(fatal))


if __name__ == '__main__':
    main()
