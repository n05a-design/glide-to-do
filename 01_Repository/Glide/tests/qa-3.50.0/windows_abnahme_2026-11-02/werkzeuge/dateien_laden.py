"""Alle Projektdateien einmal lesen, damit OneDrive sie vor dem Einfrieren lokal bereitstellt.

Lässt 13_TK-Test-Umgebung und .claude/worktrees aus. Exitcode 1, wenn eine Datei nicht lesbar ist.
"""
import os
import sys
import time

root = sys.argv[1]
auslassen = {os.path.join(root, '13_TK-Test-Umgebung'), os.path.join(root, '.claude', 'worktrees')}
dateien = groesse = 0
fehler = []
zuletzt = time.monotonic()
for ordner, unterordner, namen in os.walk(root):
    unterordner[:] = [n for n in unterordner if os.path.join(ordner, n) not in auslassen and n != '__pycache__']
    for name in namen:
        pfad = os.path.join(ordner, name)
        if os.path.islink(pfad):
            continue
        try:
            with open(pfad, 'rb') as datei:
                while block := datei.read(1 << 20):
                    groesse += len(block)
            dateien += 1
        except OSError as exc:
            fehler.append(f'{os.path.relpath(pfad, root)}: {exc.strerror or exc}')
        if time.monotonic() - zuletzt > 15:
            print(f'   ... {dateien} Dateien, {groesse / 1e6:.0f} MB', flush=True)
            zuletzt = time.monotonic()
print(f'{dateien} Projektdateien lokal verfügbar ({groesse / 1e6:.0f} MB)', flush=True)
for zeile in fehler[:10]:
    print('   Fehler:', zeile, flush=True)
sys.exit(1 if fehler else 0)
