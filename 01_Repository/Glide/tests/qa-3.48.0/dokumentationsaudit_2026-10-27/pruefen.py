"""Lesender Datei-/Dokumentabgleich; startet keine Glide-App oder Testsuite.

Schreibt ausschließlich eigene Inventare. --stand vorher/nachher trennt die
Bestandsaufnahme von der Schlussprüfung. Private Arbeitsdaten, Git-Interna,
separate Checkouts und Cloud-Platzhalter werden nicht inhaltlich geöffnet.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
REPO = ROOT / '01_Repository/Glide'
sys.path.insert(0, str(REPO / 'tests/tools'))
import ablagegroesse
import ci_grundstufe as ci
import pruefen as checks
import standpruefung as stand


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT,
        env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}).decode('utf-8', 'surrogateescape')


def category(name):
    if '/Arbeitsstand/' in name or Path(name).name in {'fehlerprotokoll.txt', 'liste_speicher.json', 'window.conf', 'datenordner.json'}:
        return 'private Arbeitsdaten (nur Metadaten)'
    if name.startswith('13_TK-Test-Umgebung/'):
        return 'lokale Tk-Pruefumgebung'
    if name.startswith('00_Arbeitsvorbereitung/Featurepaket_UI_UX/bilder/'):
        return 'geschuetzte Originalreferenz'
    if name.startswith('01_Repository/Glide/build/'):
        return 'Paket/Bauartefakt'
    if name.startswith('07_Python-Versionen/'):
        return 'Python-Lieferstand/Archiv'
    if name.startswith('05_Probelisten_Testdaten/'):
        return 'Showcase/Probedaten'
    if name.startswith('20_Grafik_Master/'):
        return 'Grafikmaster'
    if '__pycache__' in name.split('/') or Path(name).suffix in {'.pyc', '.pyo'}:
        return 'erzeugter Cache'
    if '/tests/qa-' in name:
        return 'QA-Beleg'
    if '/tests/fixtures/' in name:
        return 'Prueffixture/Migrationsbeleg'
    if Path(name).suffix == '.md':
        return 'Dokumentation/Arbeitsregeln'
    return 'Quelle/Ressource/Projektverwaltung'


def historical(name):
    return ('/tests/qa-' in name or '/Archiv/' in name or '/vendor/' in name
        or '/build/' in name or name.endswith('/Featurepaket_UI_UX/AUFTRAG.md')
        or name.endswith('packaging/paket/lizenzen/macos/Glide-Lizenzstatus.md'))


def without_code(text):
    return re.sub(r'^\s*(`{3,}|~{3,}).*?^\s*\1\s*$', '', text, flags=re.M | re.S)


def anchors(text):
    used = Counter()
    result = set(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)', text))
    for title in re.findall(r'^ {0,3}#{1,6}\s+(.+?)\s*#*$', without_code(text), re.M):
        title = re.sub(r'!?\[([^]]+)\]\([^)]*\)', r'\1', title)
        slug = ''.join(c for c in title.lower() if c in '-_ ' or unicodedata.category(c)[0] in 'LN').replace(' ', '-')
        n = used[slug]
        used[slug] += 1
        result.add(slug + (f'-{n}' if n else ''))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stand', choices=('vorher', 'nachher'), required=True)
    args = parser.parse_args()
    own = HERE.relative_to(ROOT).as_posix() + '/'
    rows, errors, excluded = [], [], []
    for parent, dirs, files in os.walk(ROOT, followlinks=False):
        parent = Path(parent)
        for child in list(dirs):
            path = parent / child
            rel = path.relative_to(ROOT).as_posix()
            if child == '.git' or rel == '.claude/worktrees' or path.is_symlink() or path.is_junction() or (path / '.git').exists():
                dirs.remove(child)
                excluded.append(dict(path=rel, reason='Git-Verwaltung, separate Arbeitskopie oder Verknuepfung'))
        for file in files:
            path = parent / file
            name = path.relative_to(ROOT).as_posix()
            if name.startswith(own):
                continue  # Eigene sich aendernde Berichte nicht selbst hashen.
            try:
                meta = path.lstat()
                attrs = getattr(meta, 'st_file_attributes', 0)
                cloud = bool(attrs & (0x1000 | 0x40000 | 0x400000))
                row = dict(path=name, bytes=meta.st_size,
                    mtime_utc=datetime.fromtimestamp(meta.st_mtime, timezone.utc).isoformat(),
                    category=category(name), cloud_placeholder=cloud, attributes=attrs)
                if path.is_symlink():
                    row['link_target'] = os.readlink(path)
                    row['link_target_sha256'] = hashlib.sha256(os.fsencode(row['link_target'])).hexdigest()
                elif not cloud and row['category'] != 'private Arbeitsdaten (nur Metadaten)':
                    row['sha256'] = digest(path)
                rows.append(row)
            except (OSError, ValueError) as exc:
                errors.append(dict(path=name, error=type(exc).__name__, message=str(exc)))
    rows.sort(key=lambda r: r['path'])
    write(f'inventar_{args.stand}.json', dict(files=rows, excluded=excluded, errors=errors,
        own_report_directory_excluded=own, application_tests_started=False))
    indexed = set(git('ls-files', '--cached', '-z').split('\0')) - {''}
    candidates = set(git('ls-files', '--cached', '--others', '--exclude-standard', '-z').split('\0')) - {''}
    ignored = set(git('ls-files', '--others', '--ignored', '--exclude-standard', '-z').split('\0')) - {''}
    doc_rows, texts = [], {}
    for row in rows:
        name = row['path']
        if Path(name).suffix != '.md' or name not in candidates or not row.get('sha256'):
            continue
        if row['category'] in {'lokale Tk-Pruefumgebung', 'Paket/Bauartefakt'} or '/vendor/' in name:
            continue
        try:
            text = (ROOT / name).read_text(encoding='utf-8-sig')
            texts[name] = text
            doc_rows.append(dict(path=name, sha256=row['sha256'], historical=historical(name),
                tracked=name in indexed, stand_lines=[l for l in text.splitlines() if re.match(r'^(?:\*\*)?Stand\b', l)][:4],
                headings=re.findall(r'^#{1,6}\s+(.+)$', text, re.M),
                version_mentions=sorted(set(re.findall(r'\b\d+\.\d+\.\d+\b', text))),
                review='Inhaltsabgleich der aktuellen Standaussagen; historische Einzelbefunde bleiben datiert'))
        except (OSError, UnicodeError) as exc:
            errors.append(dict(path=name, error=type(exc).__name__))
    write(f'dokumentregister_{args.stand}.json', doc_rows)
    links, broken = 0, []
    for name, text in texts.items():
        for n, line in enumerate(without_code(text).splitlines(), 1):
            for target in re.findall(r'!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+["\'][^)]*)?\)', line):
                target = target.strip('<>')
                parts = urlsplit(target)
                if parts.scheme or target.startswith('//'):
                    continue
                links += 1
                dest = (ROOT / name).parent / unquote(parts.path)
                issue = None
                if not dest.exists():
                    issue = 'Datei fehlt'
                elif parts.fragment and dest.suffix.lower() == '.md':
                    if unquote(parts.fragment) not in anchors(dest.read_text(encoding='utf-8-sig')):
                        issue = 'Anker pruefen'
                if issue:
                    broken.append(dict(source=name, filtered_line=n, target=target, historical=historical(name), issue=issue))
    write(f'verweise_{args.stand}.json', dict(markdown_files=len(texts), local_links=links, findings=broken,
        external_web_pages_revalidated=False))
    formats = stand.app_konstanten()
    checked = stand.lauf([ROOT], (REPO / 'VERSION').read_text().strip())
    syntax_errors, syntax_count, json_errors, json_count = [], 0, [], 0
    for row in rows:
        name = row['path']
        if not row.get('sha256') or name not in candidates:
            continue
        if row['category'] in {'private Arbeitsdaten (nur Metadaten)', 'lokale Tk-Pruefumgebung', 'Paket/Bauartefakt'} or '/vendor/' in name:
            continue
        path = ROOT / name
        if path.suffix in {'.py', '.pyw'} and '/Archiv/' not in name and not name.startswith('07_Python-Versionen/'):
            try:
                ast.parse(path.read_bytes(), filename=name)
                syntax_count += 1
            except (SyntaxError, ValueError, UnicodeError) as exc:
                syntax_errors.append(dict(path=name, error=str(exc)))
        if path.suffix == '.json':
            try:
                json.loads(path.read_text(encoding='utf-8-sig'))
                json_count += 1
            except (ValueError, UnicodeError) as exc:
                json_errors.append(dict(path=name, error=str(exc)))
    proof = json.loads((HERE.parent / 'dreierpaket_2026-10-27/quellstand.json').read_text(encoding='utf-8'))
    changed = {place: [name for name, sha in proof['sha256'].items()
        if not (root / name).is_file() or digest(root / name) != sha]
        for place, root in [('worktree', ROOT), ('frozen', Path(os.environ['TEMP']) / 'glide-348-phase-3pgpevbo/projekt')]}
    old = json.loads((REPO / 'tests/qa-3.47.0/folgepakete_2026-10-27/quellstand.json').read_text(encoding='utf-8'))
    delivery_errors, delivery_count = [], 0
    for name, sha in {**old['runtime'], **old['resources']}.items():
        if name == 'drawing_prototype.pyw':
            continue
        target = {'app.pyw': 'Glide-Aufgaben-und-Listen_v3.47.0.pyw', 'glide_start.py': 'Schnellstart.pyw'}.get(name, name)
        if digest(ROOT / '07_Python-Versionen' / target) != sha:
            delivery_errors.append(target)
        delivery_count += 1
    entries = [(r['path'], r['bytes']) for r in rows]
    picture_versions = ablagegroesse.neueste_versionen(entries, '3.48.0', 3)
    retention = [f for f in ablagegroesse.befunde(entries, '3.48.0')
        if not (f[0] == 'Fensterbilder' and ablagegroesse.pfadversion(f[1]) in picture_versions)]
    grouped = defaultdict(list)
    for r in rows:
        if r.get('sha256') and r['bytes']:
            grouped[r['sha256']].append(r['path'])
    write(f'inhaltsgruppen_{args.stand}.json', [dict(sha256=h, paths=p) for h, p in grouped.items() if len(p) > 1])
    screenshots = json.loads((ROOT / '00_Arbeitsvorbereitung/Featurepaket_UI_UX/screenshots.json').read_text(encoding='utf-8'))
    image_errors = []
    for row in screenshots['bilder']:
        path = ROOT / '00_Arbeitsvorbereitung/Featurepaket_UI_UX' / row['datei']
        if not path.is_file() or digest(path) != row['sha256']:
            image_errors.append(row['id'])
    docs_result, fixtures_result, versions_result = None, None, None
    for what, func in [('documentation', checks.dokumentation_pruefen), ('fixtures', checks.fixtures_pruefen), ('versions', checks.versionen_pruefen)]:
        try:
            value = func()
            if what == 'documentation':
                docs_result = value
            elif what == 'fixtures':
                fixtures_result = value
            else:
                versions_result = value
        except Exception as exc:
            errors.append(dict(check=what, error=str(exc)))
    summary = dict(stand=args.stand, date='2026-10-27', version='3.48.0', schema=formats,
        git_head=git('rev-parse', 'HEAD').strip(), branch=git('branch', '--show-current').strip(),
        files=len(rows), bytes=sum(r['bytes'] for r in rows), hashed=sum('sha256' in r for r in rows),
        cloud_placeholders=[r['path'] for r in rows if r['cloud_placeholder']],
        categories=dict(Counter(r['category'] for r in rows)),
        tracked_present=sum(r['path'] in indexed for r in rows), ignored_present=sum(r['path'] in ignored for r in rows),
        documentation_files=len(doc_rows), active_documentation_files=sum(not r['historical'] for r in doc_rows),
        registered_stand_documents=checked.fortgeschrieben + checked.festgeschrieben + checked.ohne_stand,
        stand_errors=checked.fehler, documentation=docs_result, fixtures=fixtures_result, versions=versions_result,
        local_links=links, active_link_findings=[r for r in broken if not r['historical']],
        historical_link_findings=[r for r in broken if r['historical']],
        python_syntax_files=syntax_count, python_syntax_errors=syntax_errors,
        json_files=json_count, json_errors=json_errors,
        source_files=len(proof['sha256']), changed_source=changed,
        changed_source_documentation={place: [n for n in names if n.endswith('.md')] for place, names in changed.items()},
        changed_source_executable_or_data={place: [n for n in names if not n.endswith('.md')] for place, names in changed.items()},
        delivery_files=delivery_count, delivery_errors=delivery_errors,
        delivery_differences=ci.lieferstand_abweichungen(),
        reference_images=len(screenshots['bilder']), reference_image_errors=image_errors,
        retention_findings=retention, errors=errors, application_tests_started=False,
        symbolic_links=[dict(path=r['path'], target=r['link_target']) for r in rows if 'link_target' in r],
        native_dump_analysis_performed=False, release_ready=False,
        limitations=['Metadaten und Hashes fuer alle lesbaren lokalen Hauptcheckoutdateien; Git-Interna und separate Checkouts abgegrenzt.',
            'Private Arbeitsdaten nur Metadaten; Cloud-Platzhalter nicht nachgeladen.',
            'Syntax/JSON/Links/Versionen sind keine vollstaendige semantische Neuanalyse jeder Codezeile oder jedes Altprotokolls.',
            'Externe Webseiten und Marktfakten nicht neu recherchiert; datierte Quellen bleiben datiert.',
            'Keine Anwendung, GUI, Lastsuite oder Produktionsmutation ausgefuehrt.'])
    write(f'ergebnis_{args.stand}.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    fatal = (errors or checked.fehler or broken or syntax_errors or json_errors
        or delivery_errors or image_errors
        or changed['frozen'] or any(not n.endswith('.md') for n in changed['worktree']))
    raise SystemExit(int(bool(fatal)))


if __name__ == '__main__':
    main()
