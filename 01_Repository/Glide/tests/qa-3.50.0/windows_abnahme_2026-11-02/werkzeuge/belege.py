"""Flache Belege eines Windows-Abnahmelaufs nach 13_TK-Test-Umgebung/PC-01-AMD/<Lauf> kopieren.

Nur Berichte, Logs, Manifeste und Fensterbilder – keine Projektkopie, keine Prüfdaten, kein Paket
(Pfadlängenregel in CLAUDE.md). Jede Kopie wird per SHA-256 geprüft; kopiermanifest.json führt die Herkunft.
Aufruf: python -B belege.py <Laufordner> <Zielordner>
"""
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

MAX_PFAD = 240
AUSSCHLUSS = {'projekt', 'daten', 'temp', '.git', '__pycache__', 'cache', 'venv', 'dist', 'arbeit',
              'build', 'lizenzen', 'jpeg_diagnose', 'session_diagnose'}
ENDUNGEN = {'.json', '.log', '.txt', '.md', '.png', '.csv'}

quelle = Path(sys.argv[1]).resolve()
ziel = Path(sys.argv[2])
eintraege, uebersprungen = [], []
for ordner, unterordner, namen in os.walk(quelle):
    unterordner[:] = [n for n in unterordner if n not in AUSSCHLUSS]
    for name in namen:
        datei = Path(ordner) / name
        if datei.suffix.lower() not in ENDUNGEN:
            continue
        kopie = ziel / datei.relative_to(quelle)
        if len(str(kopie)) > MAX_PFAD:
            uebersprungen.append({'datei': datei.relative_to(quelle).as_posix(), 'grund': f'Zielpfad > {MAX_PFAD} Zeichen'})
            continue
        inhalt = datei.read_bytes()
        pruefsumme = hashlib.sha256(inhalt).hexdigest()
        kopie.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(datei, kopie)
        if hashlib.sha256(kopie.read_bytes()).hexdigest() != pruefsumme:
            raise SystemExit(f'Kopierprüfung fehlgeschlagen: {kopie}')
        eintraege.append({'quelle': datei.relative_to(quelle).as_posix(), 'bytes': len(inhalt), 'sha256': pruefsumme})
(ziel / 'kopiermanifest.json').write_text(json.dumps({
    'art': 'Bytegleiche Berichte, Logs und Fensterbilder eines Windows-Abnahmelaufs; keine zusätzlichen Prüfläufe.',
    'laufordner': str(quelle), 'dateien': eintraege, 'uebersprungen': uebersprungen},
    ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'{len(eintraege)} Belege abgelegt ({sum(e["bytes"] for e in eintraege)} Bytes), {len(uebersprungen)} übersprungen')
