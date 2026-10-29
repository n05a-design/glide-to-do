"""Dokumentabschluss aus vorhandenen Inventaren; keine Anwendungstests."""
import ast
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
spec = importlib.util.spec_from_file_location('glide_document_audit', HERE / 'pruefen.py')
audit_helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_helpers)
anchors, digest, without_code, write = (audit_helpers.anchors, audit_helpers.digest,
    audit_helpers.without_code, audit_helpers.write)


def load(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


before = {r['path']: r for r in load('inventar_vorher.json')['files']}
after = {r['path']: r for r in load('inventar_nachher.json')['files']}
audit = load('ergebnis_nachher.json')
packages = load('pakete_und_belege.json')
errors = []
for key in ('errors', 'stand_errors', 'python_syntax_errors', 'json_errors', 'active_link_findings',
            'historical_link_findings', 'reference_image_errors', 'delivery_errors', 'cloud_placeholders'):
    if audit[key]:
        errors.append(dict(check=key, findings=audit[key]))
if packages['errors']:
    errors.append(dict(check='packages', findings=packages['errors']))
expected_doc = ['01_Repository/Glide/tests/fixtures/showcase/README.md']
if audit['changed_source'] != dict(worktree=expected_doc, frozen=[]):
    errors.append(dict(check='source_changes', findings=audit['changed_source']))
for names in audit['changed_source_executable_or_data'].values():
    if names:
        errors.append(dict(check='executable_or_data_changed', findings=names))
changes = []
for name, old in before.items():
    new = after.get(name)
    if new is None:
        errors.append(dict(check='file_removed', path=name))
    elif old.get('sha256') and old['sha256'] != new.get('sha256'):
        changes.append(dict(path=name, before_sha256=old['sha256'], after_sha256=new.get('sha256'),
            kind='Dokumentkorrektur' if name.endswith('.md') else 'andere Aenderung'))
        if not name.endswith('.md'):
            errors.append(dict(check='non_document_mutation', path=name))
write('dokumentkorrekturen.json', dict(changed_files=changes,
    new_files=[r for name, r in after.items() if name not in before],
    own_audit_directory_excluded=True, executable_or_data_changes=False))
retention = []
for rule, name, reason in audit['retention_findings']:
    row = after[name]
    retention.append(dict(path=name, sha256=row.get('sha256'), bytes=row['bytes'],
        rule=rule, reason=reason, status='offener lokaler Bereinigungskandidat; nicht geloescht'))
write('aufbewahrung_offen.json', dict(files=len(retention), bytes=sum(r['bytes'] for r in retention),
    categories=dict(Counter(r['rule'] for r in retention)), files_detail=retention, deletion_performed=False))
# Seit dem Inventarlauf keine stillen Fremdaenderungen uebersehen. Geaenderte
# Metadaten erzwingen einen erneuten Hash, unveraenderte Dateien wurden bereits
# vollstaendig im Inventar gelesen.
drift, rehashed = [], 0
for name, row in after.items():
    path = ROOT / name
    try:
        meta = path.lstat()
        if 'sha256' not in row:
            continue
        from datetime import datetime, timezone
        mtime = datetime.fromtimestamp(meta.st_mtime, timezone.utc).isoformat()
        if meta.st_size != row['bytes'] or mtime != row['mtime_utc']:
            rehashed += 1
            if digest(path) != row['sha256']:
                drift.append(name)
    except OSError as exc:
        drift.append(dict(path=name, error=type(exc).__name__))
if drift:
    errors.append(dict(check='drift_after_inventory', findings=drift))
own_hashes, own_links, own_syntax, own_json = {}, 0, 0, 0
for path in sorted(HERE.iterdir()):
    if not path.is_file() or path.name == 'abschluss.json' or path.suffix == '.log':
        continue
    if path.suffix == '.py':
        ast.parse(path.read_bytes(), filename=str(path.name))
        own_syntax += 1
    if path.suffix == '.json':
        json.loads(path.read_text(encoding='utf-8-sig'))
        own_json += 1
    if path.suffix == '.md':
        for target in re.findall(r'!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+["\'][^)]*)?\)', without_code(path.read_text(encoding='utf-8'))):
            target = target.strip('<>')
            parts = urlsplit(target)
            if parts.scheme:
                continue
            own_links += 1
            dest = path.parent / unquote(parts.path)
            if dest == HERE / 'abschluss.json':
                continue  # Wird abschliessend geschrieben, keine zyklische Selbsthashung.
            if not dest.exists():
                errors.append(dict(check='own_link', target=target))
            elif parts.fragment and dest.suffix == '.md' and unquote(parts.fragment) not in anchors(dest.read_text(encoding='utf-8')):
                errors.append(dict(check='own_anchor', target=target))
    own_hashes[path.name] = digest(path)
for argv in (['git', 'diff', '--check'], ['git', 'diff', '--cached', '--check']):
    check = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if check.returncode:
        errors.append(dict(check='git_diff_check', output=check.stdout + check.stderr))
ignored = subprocess.run(['git', 'check-ignore', '--',
    '01_Repository/Glide/tests/qa-3.48.0/lokale_belege/minidumps/python.exe.66596.dmp',
    '01_Repository/Glide/tests/qa-3.48.0/lokale_belege/eingang/initial.json'],
    cwd=ROOT, capture_output=True, text=True)
if ignored.returncode or len(ignored.stdout.splitlines()) != 2:
    errors.append(dict(check='evidence_git_ignore'))
result = dict(date='2026-10-27', files=audit['files'], regular_files_hashed=audit['hashed'],
    documentation_files=audit['documentation_files'], active_documents=audit['active_documentation_files'],
    corrected_documents=len(changes), application_tests_started=False,
    source_reference_files=470, source_reference_documentation_changes=expected_doc,
    executable_or_data_changes=False, frozen_reference_changed=False,
    old_python_delivery_files_verified=audit['delivery_files'], native_archives_equal=True,
    local_saved_evidence_files=packages['saved_evidence_files'],
    local_retention_candidates=len(retention), external_backup_confirmed=False,
    own_audit_files_sha256=own_hashes, own_syntax_files=own_syntax, own_json_files=own_json,
    own_local_links=own_links, inventory_metadata_changes_rehashed=rehashed,
    git_diff_check_passed=not any(r.get('check') == 'git_diff_check' for r in errors),
    private_evidence_git_ignored=ignored.returncode == 0,
    release_ready=False, errors=errors)
write('abschluss.json', result)
print(json.dumps({k: v for k, v in result.items() if k != 'own_audit_files_sha256'}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
