"""Lesende Bestandsprüfung auf Basis der vollständigen Metadateninventur.

Aufruf aus der Projektwurzel mit python -B. Schreibt nur eigene Nachweise;
ändert weder Git noch die geprüften Dateien und lädt keine Cloud-Platzhalter.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
sys.path.insert(0, str(ROOT / '01_Repository/Glide/tests/tools'))
import ablagegroesse


def write(name, value):
    (A / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def git(*args, cwd=ROOT):
    env = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}
    p = subprocess.run(['git', *args], cwd=cwd, env=env, capture_output=True)
    return p.returncode, p.stdout.decode('utf-8', errors='replace').strip(), p.stderr.decode('utf-8', errors='replace').strip()


def digest(path):
    h = hashlib.sha256()
    name = '\\\\?\\' + str(path.resolve()) if os.name == 'nt' else path
    with open(name, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def stripped(text):
    return re.sub(r'^\s*(`{3,}|~{3,}).*?^\s*\1\s*$', '', text, flags=re.M | re.S)


def anchors(text):
    counts = Counter()
    result = set(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)', text))
    for heading in re.findall(r'^ {0,3}#{1,6}\s+(.+?)\s*#*$', stripped(text), re.M):
        heading = re.sub(r'!?\[([^]]+)\]\([^)]*\)', r'\1', heading)
        slug = ''.join(c for c in heading.lower() if c in '-_ ' or unicodedata.category(c)[0] in 'LN').replace(' ', '-')
        n = counts[slug]
        counts[slug] += 1
        result.add(slug + (f'-{n}' if n else ''))
    return result


def run():
    inventory = json.loads((A / 'inventar_vorher.json').read_text(encoding='utf-8'))
    rows = inventory['dateien']
    main = [r for r in rows if not r['pfad'].startswith(('.git/', '.claude/worktrees/'))]
    hashes = {}
    errors = []
    for r in main:
        if r['inhalt_nicht_vollstaendig_lokal']:
            continue
        try:
            hashes[r['pfad']] = digest(ROOT / r['pfad'])
        except OSError as exc:
            errors.append({'pfad': r['pfad'], 'fehlerklasse': type(exc).__name__})
    write('dateihashes_vorher.json', {'sha256': hashes, 'fehler': errors})
    groups = defaultdict(list)
    bypath = {r['pfad']: r for r in main}
    for path, sha in hashes.items():
        if bypath[path]['bytes']:
            groups[sha].append(path)
    dup = [{'sha256': sha, 'bytes_je_datei': bypath[paths[0]]['bytes'], 'pfade': paths}
           for sha, paths in groups.items() if len(paths) > 1]
    write('inhaltsdubletten.json', sorted(dup, key=lambda d: d['bytes_je_datei'] * (len(d['pfade']) - 1), reverse=True))
    entries = [(r['pfad'], r['bytes']) for r in main]
    versions = ablagegroesse.neueste_versionen(entries, '3.44.0')
    pictures = ablagegroesse.neueste_versionen(entries, '3.44.0', 3)
    findings = ablagegroesse.befunde(entries, '3.44.0')
    # Das Git-Verbot aktueller fenster/-Fotos ist kein lokaler Löschgrund.
    local = [f for f in findings if not (f[0] == 'Fensterbilder' and ablagegroesse.pfadversion(f[1]) in pictures)]
    write('aufbewahrung_lokal.json', {'versionen': sorted(versions, key=ablagegroesse.als_tupel),
         'bildversionen': sorted(pictures, key=ablagegroesse.als_tupel), 'befunde': local,
         'betroffene_bytes': sum(bypath[p]['bytes'] for p in {f[1] for f in local})})

    rc, names, _ = git('ls-files', '--cached', '--others', '--exclude-standard', '-z')
    assert rc == 0
    candidates = sorted(set(names.split('\0')) - {''})
    candidate_md = [p for p in candidates if p.endswith('.md') and not p.startswith(('07_Python-Versionen/', '01_Repository/Glide/build/', '01_Repository/Glide/src/glide/vendor/'))]
    broken = []
    external = defaultdict(set)
    link_count = 0
    texts = {}
    for path in candidate_md:
        try:
            texts[path] = (ROOT / path).read_text(encoding='utf-8-sig')
        except (OSError, UnicodeError):
            errors.append({'pfad': path, 'fehlerklasse': 'Markdown nicht lesbar'})
    for path, text in texts.items():
        historical = '/qa-' in path or '/Featurepaket_UI_UX/AUFTRAG.md' in path
        for n, line in enumerate(stripped(text).splitlines(), 1):
            for target in re.findall(r'!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+["\'][^)]*)?\)', line):
                target = target.strip('<>')
                parts = urlsplit(target)
                if parts.scheme in ('http', 'https'):
                    if not historical and not path.startswith('.claude/'):
                        external[target].add(path)
                    continue
                if parts.scheme or target.startswith('//'):
                    continue
                link_count += 1
                dest = (ROOT / path).parent / unquote(parts.path)
                if not dest.exists():
                    broken.append({'quelle': path, 'zeile_nach_codefilter': n, 'ziel': target, 'historisch': historical, 'art': 'Datei fehlt'})
                elif parts.fragment and dest.suffix.lower() == '.md':
                    fragment = unquote(parts.fragment)
                    try:
                        valid = fragment in anchors(dest.read_text(encoding='utf-8-sig'))
                    except (OSError, UnicodeError):
                        valid = False
                    if not valid:
                        broken.append({'quelle': path, 'zeile_nach_codefilter': n, 'ziel': target, 'historisch': historical, 'art': 'Anker prüfen'})
    write('verweise.json', {'markdown_dateien': len(texts), 'lokale_verweise': link_count, 'befunde': broken,
          'externe_urls': [{'url': u, 'quellen': sorted(p)} for u, p in sorted(external.items())],
          'grenze': 'Markdown-Inline-Links und ATX-Überschriften; Ankerbefunde werden am Ziel manuell validiert.'})

    trees = []
    rc, listing, err = git('worktree', 'list', '--porcelain')
    assert rc == 0, err
    for block in listing.split('\n\n'):
        fields = dict(line.split(' ', 1) if ' ' in line else (line, '') for line in block.splitlines())
        path = fields.get('worktree', '')
        if not path or Path(path).resolve() == ROOT:
            continue
        name = Path(path).name
        row = {'name': name, 'head': fields.get('HEAD'), 'branch': fields.get('branch'),
               'vorhanden': Path(path).is_dir(), 'prunable': 'prunable' in fields}
        if row['vorhanden']:
            code, status, error = git('status', '--porcelain=v1', '--untracked-files=all', cwd=path)
            row['status_exitcode'] = code
            row['aenderungen'] = status.splitlines()
            row['commits_nicht_in_lokalem_HEAD'] = git('rev-list', '--count', f'HEAD..{row["head"]}')[1]
            row['patchvergleich_zum_lokalen_HEAD'] = git('cherry', 'HEAD', row['head'])[1].splitlines()
        trees.append(row)
    write('arbeitskopien.json', trees)
    protected = [r for r in main if r['bereich'] in ('geschützte Nutzerreferenz', 'Prüffixture und Migrationsreferenz', 'Grafikquelle und Master', 'Python-Lieferstand', 'Showcase und Probedaten', 'Paket und Bauartefakt')]
    summary = {'dateien': len(rows), 'ordner': len(inventory['ordner']), 'inventarfehler': inventory['fehler'],
         'bytes_gesamt': sum(r['bytes'] for r in rows), 'bytes_hauptbestand_ohne_git_arbeitskopien': sum(r['bytes'] for r in main),
         'bereiche': inventory['bereiche'], 'vollstaendig_gehasht_hauptbestand': len(hashes), 'hashfehler': errors,
         'cloud_platzhalter_nicht_gehasht': [r['pfad'] for r in main if r['inhalt_nicht_vollstaendig_lokal']],
         'geschuetzte_dateien': len(protected), 'kandidat_dateien': len(candidates),
         'dubletten_gruppen': len(dup), 'dubletten_rohpotential_bytes': sum(d['bytes_je_datei'] * (len(d['pfade']) - 1) for d in dup),
         'aufbewahrung_befunde': len(local), 'verweise_befunde': len(broken),
         'dateien_ueber_50_MiB': [{'pfad': r['pfad'], 'bytes': r['bytes']} for r in main if r['bytes'] > 50 * 1024 ** 2]}
    write('bestandspruefung.json', summary)
    print(json.dumps({k: v for k, v in summary.items() if k not in ('bereiche', 'cloud_platzhalter_nicht_gehasht', 'dateien_ueber_50_MiB')}, ensure_ascii=False))


if __name__ == '__main__':
    run()
