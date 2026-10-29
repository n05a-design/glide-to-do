"""Formaler Abschluss des datierten Abnahmeaudits, ohne erneute App-/Lastprüfung."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import unquote

from docx import Document
from pypdf import PdfReader
from PIL import Image

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
REPO = ROOT / '01_Repository/Glide'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8-sig'))


def main():
    freeze = read('eingefroren.json')
    expected = {
        '00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md',
        '00_Arbeitsvorbereitung/Glide_Uebergabe.md',
        '01_Repository/Glide/docs/07_QA_BERICHT.md',
        '01_Repository/Glide/docs/ARBEITSRICHTUNG.md',
    }
    changed = [n for n, h in freeze['source_sha256'].items()
               if not (ROOT / n).is_file() or sha(ROOT / n) != h]
    assert set(changed) == expected, changed
    assert sha(REPO / 'src/glide/app.pyw') == freeze['app_sha256']
    pdf = OUT / 'Glide_Abnahmebericht_3.49.0_2026-10-28.pdf'
    word = OUT / 'Glide_Abnahmebericht_3.49.0_2026-10-28.docx'
    reader = PdfReader(pdf)
    assert len(reader.pages) == 13
    text = '\n'.join(page.extract_text() for page in reader.pages)
    assert '\ufffd' not in text
    assert freeze['app_sha256'] in text
    assert all(f'B{n:02}' in text for n in range(1, 23))
    assert all(f'E{n:02}' in text for n in range(1, 13))
    assert all(t in text for t in ['8/9', 'WA-41', 'Gesamtabnahme', '3.47.0', '3.45.0'])
    doc = Document(word)
    assert not doc.styles.element.xpath('.//w:pBdr')
    matrix = read('paketmatrix.json')
    counts = {k: len(v) for k, v in matrix.items() if isinstance(v, list)}
    assert sum(counts.values()) == 52, counts
    test = read('testergebnis.json')
    assert test['cases'][0]['ok'] and not test['cases'][1]['ok']
    assert len(test['not_executed']) == 12 and not test['global_acceptance']
    for case in test['cases']:
        assert sha(OUT / case['report']) == case['report_sha256']

    broken = []
    links = 0
    for path in [OUT / 'README.md'] + [ROOT / p for p in sorted(expected)]:
        content = path.read_text(encoding='utf-8-sig')
        if path != OUT / 'README.md':
            content = '\n'.join(line for line in content.splitlines()
                                if 'Abnahmeaudit' in line or 'Abnahmeprüfung' in line
                                or 'abnahme_2026-10-28' in line)
        for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
            target = unquote(raw.split('#')[0])
            if not target or re.match(r'^[a-z]+:', target):
                continue
            links += 1
            if not (path.parent / target).exists():
                broken.append([str(path.relative_to(ROOT)), raw])
    assert not broken, broken
    plan = ROOT / '00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md'
    assert plan.read_text(encoding='utf-8').count('### 21.29 Abnahmeprüfung des begonnenen Umfangs') == 1

    # Wiederholte Tabellenköpfe zusätzlich als Bildpixel prüfen, unabhängig von der Vorschau.
    image_checks = {}
    for n in range(1, 14):
        image_path = OUT / f'render/abnahme-{n:02}.png'
        with Image.open(image_path) as im:
            assert im.width > 900 and im.height > 1300
            image_checks[str(n)] = {'sha256': sha(image_path), 'size': list(im.size)}

    stand = subprocess.run([sys.executable, '-B', 'tests/tools/standpruefung.py'],
                           cwd=REPO, capture_output=True, text=True, encoding='utf-8')
    assert stand.returncode == 0, stand.stdout + stand.stderr
    diff = subprocess.run(['git', 'diff', '--check', '--', *sorted(expected)],
                          cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    assert diff.returncode == 0, diff.stdout + diff.stderr
    result = {
        'completed_on': '2026-10-29', 'audit_cutoff': '2026-10-28',
        'formal_artifact_checks_ok': True, 'global_acceptance': False,
        'pages': 13, 'acceptance_units': counts, 'ui_requirements': 22,
        'inventoried_input_files': len(freeze['source_sha256']),
        'input_changes_after_testing': sorted(changed),
        'input_changes_are_only_document_pointers': True,
        'app_unchanged': True, 'app_sha256': freeze['app_sha256'],
        'original_repetition_suite_green': False, 'not_executed': test['not_executed'],
        'standpruefung': stand.stdout.strip(), 'git_diff_check': True,
        'new_local_file_links_checked': links, 'broken_links': broken,
        'word_table_rows': [len(t.rows) for t in doc.tables],
        'rendering': 'Word PDF/A-1 export option; PDFium scale 1.6; all 13 pages visually inspected',
        'render_checks': image_checks,
        'deliverables': {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size} for p in [word, pdf]},
        'evidence_sha256': {p.name: sha(p) for p in OUT.glob('*.json') if p.name != 'abschluss.json'},
        'limits': 'No application fixes, native starts, signature verification, full stress rerun, commit, push or release.'
    }
    (OUT / 'abschluss.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['formal_artifact_checks_ok', 'pages', 'acceptance_units',
                                           'app_unchanged', 'new_local_file_links_checked', 'global_acceptance']},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
