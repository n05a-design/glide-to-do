"""Schlussbeleg für die Dokumentpflege; keine App-/Lastprüfung."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
REPO = ROOT / '01_Repository/Glide'
sys.path.insert(0, str(REPO / 'tests/tools'))
import ci_grundstufe as ci
import ablagegroesse


def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    before = {r['path']: r for r in read('inventar_vorher.json')['files']}
    after = {r['path']: r for r in read('inventar_nachher.json')['files']}
    deleted = sorted(set(before) - set(after))
    added = sorted(set(after) - set(before))
    changed = [n for n, r in before.items() if n in after and r.get('sha256') != after[n].get('sha256')]
    assert not deleted and not added, (deleted, added)
    journal = {r['path']: r for r in read('dokumentkorrekturen.json')}
    for n in changed:
        p = ROOT / n
        assert digest(p) == after[n]['sha256'], n
        if n not in journal:
            journal[n] = {'path': n, 'before_sha256': before[n]['sha256'],
                          'reasons': ['Weitere aktuelle Liefer-/Prüfeinstiege mit Quelle 3.49.0 und Abnahmebefund abgeglichen']}
        journal[n]['after_sha256'] = after[n]['sha256']
        assert journal[n]['before_sha256'] == before[n]['sha256']
    assert set(journal) == set(changed)
    (OUT / 'dokumentkorrekturen.json').write_text(json.dumps(list(journal.values()), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    result = read('ergebnis_nachher.json')
    for field in ['errors', 'stand_errors', 'active_link_findings', 'historical_link_findings',
                  'python_syntax_errors', 'json_errors', 'reference_image_errors', 'archive_errors',
                  'unexpected_non_document_changes']:
        assert not result[field], (field, result[field])
    assert len(result['tool_docstring_only_ast_verified']) == 1
    packages = read('pakete_und_ressourcen.json')
    assert not packages['errors']
    assert packages['runtime_files'] == 90
    assert packages['python_delivery_files'] == 235
    assert packages['protected_wa41_files'] == 9
    original_audit = [n for n in before if '/abnahme_2026-10-28/' in n]
    original_changes = [n for n in original_audit if before[n].get('sha256') != after[n].get('sha256')]
    assert not original_changes
    runtime_changes = [n for n in changed if n.startswith('01_Repository/Glide/src/glide/') and not n.endswith('.md')]
    tests_changed = [n for n in changed if '/tests/' in n and not n.endswith('.md')]
    delivery_changes = [n for n in changed if n.startswith(('07_Python-Versionen/', '05_Probelisten_Testdaten/',
                                                         '01_Repository/Glide/build/')) and not n.endswith('.md')]
    assert not runtime_changes and not tests_changed and not delivery_changes
    privacy = ci.benutzerpfade()
    assert privacy == [], privacy
    retention = ablagegroesse.befunde(ablagegroesse.versionierte_dateien(), '3.49.0')
    assert not retention, retention
    actual_retention = ablagegroesse.befunde([(n, r['bytes']) for n, r in after.items()], '3.49.0')
    candidates = [dict(rule=rule, path=n, reason=reason, sha256=after[n].get('sha256'),
                       status='nur dokumentiert; kein Loeschauftrag') for rule, n, reason in actual_retention]
    (OUT / 'ablagehinweise.json').write_text(json.dumps(candidates,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    checked_links = 0
    for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', (OUT/'README.md').read_text(encoding='utf-8')):
        url = urlsplit(raw)
        if url.scheme:
            continue
        target = (OUT / unquote(url.path)).resolve()
        if target != OUT / 'abschluss.json':
            assert target.is_file(), raw
        if url.fragment:
            assert any(url.fragment.startswith(prefix) for prefix in ['1320-', '2129-']), raw
        checked_links += 1
    for path in OUT.glob('*.py'):
        ast.parse(path.read_bytes(), filename=path.name)
    diff = subprocess.run(['git', 'diff', '--check', '--', *changed], cwd=ROOT,
                          capture_output=True, text=True, encoding='utf-8')
    assert diff.returncode == 0, diff.stdout+diff.stderr
    summary = {
        'date': '2026-10-29', 'documentation_checks_ok': True, 'global_acceptance': False,
        'files_in_main_checkout': result['files'], 'hashed_files': result['hashed'],
        'symbolic_links': result['links'], 'registered_stand_documents': result['registered_stand_documents'],
        'registered_markdown_files': result['documents'], 'active_markdown_files': result['active_documents'],
        'local_file_and_section_links': result['local_links'], 'own_report_links': checked_links,
        'python_syntax_files': result['python_syntax_files'], 'json_files': result['json_files'],
        'changed_files': sorted(changed), 'changed_markdown_files': len([n for n in changed if n.endswith('.md')]),
        'tool_docstring_only_ast_verified': result['tool_docstring_only_ast_verified'],
        'runtime_changes': runtime_changes, 'test_code_changes': tests_changed, 'delivery_changes': delivery_changes,
        'original_acceptance_audit_files_unchanged': len(original_audit),
        'original_acceptance_audit_changes': original_changes, 'deleted_files': deleted,
        'privacy_findings': privacy, 'versioned_retention_findings': retention,
        'local_retention_observations': len(candidates),
        'local_retention_by_rule': dict(Counter(c['rule'] for c in candidates)),
        'git_diff_check_ok': True, 'application_or_stress_tests_started': False,
        'current_source_version': '3.49.0', 'python_delivery_version': '3.47.0', 'native_delivery_version': '3.45.0',
        'app_sha256': digest(REPO/'src/glide/app.pyw'),
        'evidence_sha256': {p.name:digest(p) for p in OUT.glob('*.json') if p.name!='abschluss.json'},
        'open_boundaries': ['A01 FP-01 Originalsuite 8/9; zwölf Folgesuiten nicht ausgeführt',
                            'A02 P8/4.0 und technische Restumfänge', 'A03 WA-41A/B',
                            'A04 aktuelle Lieferung und native/Menschenabnahmen'],
        'limitations': result['limits']
    }
    (OUT/'abschluss.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ['documentation_checks_ok','files_in_main_checkout',
          'changed_markdown_files','local_file_and_section_links','original_acceptance_audit_changes',
          'runtime_changes','local_retention_observations','global_acceptance']},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
