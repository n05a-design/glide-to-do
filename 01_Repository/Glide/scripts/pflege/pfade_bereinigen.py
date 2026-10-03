#!/usr/bin/env python3
"""Ersetzt Benutzerpfade in Textdateien, bevor sie ins öffentliche Repository kommen.

Aufruf aus `01_Repository/Glide`:
    python3 -B scripts/pflege/pfade_bereinigen.py PFAD [PFAD …] [--pruefen]

PFAD ist eine Datei oder ein Ordner (rekursiv). Ersetzt werden
`/Users/<Name>/` durch `~/` und `C:\\Users\\<Name>` (beide auch JSON-maskiert) durch
`%USERPROFILE%`. Binärdateien bleiben unberührt; Zeilenenden und Kodierung
bleiben erhalten, weil auf Bytes gearbeitet wird. JSON-Dateien müssen danach
gültig bleiben, sonst bricht das Werkzeug ab, ohne die Datei zu schreiben.

`--pruefen` ändert nichts und meldet nur Fundstellen (Exitcode 1 bei Funden).
Dieselbe Regel prüft die CI-Grundstufe im Schritt „Datenschutz“.
"""

import argparse
import json
from pathlib import Path
import re
import sys

MAC = re.compile(rb"(\\?/)Users\1(?!Shared\\?/)[A-Za-z0-9._-]+\1")
WINDOWS = re.compile(rb"[A-Za-z]:(\\{1,2})Users\1(?!Public\b)[A-Za-z0-9._-]+")


def dateien(pfade):
    for pfad in pfade:
        pfad = Path(pfad)
        if pfad.is_dir():
            yield from (datei for datei in sorted(pfad.rglob("*")) if datei.is_file() and ".git" not in datei.parts)
        elif pfad.is_file():
            yield pfad


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pfade", nargs="+")
    parser.add_argument("--pruefen", action="store_true", help="nur melden, nichts ändern")
    args = parser.parse_args()
    gefunden = 0
    for datei in dateien(args.pfade):
        alt = datei.read_bytes()
        if b"\0" in alt[:8192]:
            continue
        neu, mac = MAC.subn(lambda treffer: b"~" + treffer.group(1), alt)
        neu, win = WINDOWS.subn(b"%USERPROFILE%", neu)
        if not mac + win:
            continue
        gefunden += 1
        if args.pruefen:
            print(f"{datei}: {mac + win} Benutzerpfade")
            continue
        if datei.suffix.lower() == ".json":
            try:
                json.loads(neu.decode("utf-8"))
            except ValueError as exc:
                sys.exit(f"{datei}: nach dem Ersetzen kein gültiges JSON mehr ({exc}); nicht geschrieben")
        datei.write_bytes(neu)
        print(f"{datei}: {mac + win} Benutzerpfade ersetzt")
    if not gefunden:
        print("Keine Benutzerpfade gefunden.")
    return 1 if args.pruefen and gefunden else 0


if __name__ == "__main__":
    raise SystemExit(main())
