"""Unveränderte Lastkriterien; bei Abweichung nur begrenzte Felddifferenzen sichern.

Zusätzlicher Diagnoselauf, kein Ersatz für den originalen roten Lastnachweis.
Die App und die eingefrorene Testdatei werden nicht verändert.
"""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
FROZEN = Path((HERE / 'freeze_ort.log').read_text(encoding='utf-8')) / '01_Repository/Glide'
TEST = FROZEN / 'tests/integration/test_speicherlast330.py'
differences = []


def compare(before, after, path=''):
    if len(differences) >= 20 or before == after:
        return
    if type(before) is type(after) is dict:
        for key in sorted(set(before) | set(after)):
            compare(before.get(key, '<fehlt>'), after.get(key, '<fehlt>'), path + '/' + key)
    elif type(before) is type(after) is list and len(before) == len(after):
        for number, (left, right) in enumerate(zip(before, after)):
            compare(left, right, path + '/' + str(number))
    else:
        differences.append({'path': path, 'saved': repr(before)[:300], 'loaded': repr(after)[:300]})


def diagnose(saved, loaded, iteration):
    compare(json.loads(saved), json.loads(loaded))
    (HERE / 'lastdifferenz.json').write_text(json.dumps({'iteration': iteration, 'differences': differences},
        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(differences, ensure_ascii=False), flush=True)


source = TEST.read_text(encoding='utf-8')
old = '            assert bestand() == auf_platte, f"Runde {runde}: geladen ≠ gespeichert"'
new = ('            diagnostic_actual = bestand()\n'
       '            if diagnostic_actual != auf_platte:\n'
       '                diagnose(auf_platte, diagnostic_actual, runde)\n'
       '                raise AssertionError(f"Runde {runde}: geladen ≠ gespeichert")')
assert source.count(old) == 1
scope = {'__file__': str(TEST), '__name__': '__main__', 'diagnose': diagnose}
exec(compile(source.replace(old, new), str(TEST), 'exec'), scope)
