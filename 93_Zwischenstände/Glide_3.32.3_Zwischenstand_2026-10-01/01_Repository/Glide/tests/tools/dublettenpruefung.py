#!/usr/bin/env python3
"""Findet wiederholte Codeblöcke – die Vorstufe jeder Zusammenfassung.

Punkt 3 (5. Prüfung, 3.25.0) fragt, ob sich ähnliche, sich wiederholende
Vorgänge durch gemeinsame Bausteine ersetzen lassen. Diese Frage beantwortet
man nicht aus dem Gedächtnis: `app.pyw` hat über dreißigtausend Zeilen, und
eine Wiederholung fällt beim Lesen erst auf, wenn man beide Stellen zufällig
nebeneinander hat.

Verfahren: Jede Zeile wird auf ihren Kern reduziert – Einrückung, Kommentare
und Leerzeilen fallen weg. Über die verbleibende Folge läuft ein Fenster von
`--laenge` Zeilen; identische Fenster werden gesammelt. Gemeldet wird je
Fundstelle die längste Wiederholung, damit nicht dieselbe Dublette in zehn
Varianten erscheint.

Was das Werkzeug NICHT tut: Es bewertet nicht. Zwei gleiche Blöcke können
richtig sein – eine Tabelle, ein bewusst ausgeschriebener Sonderfall, zwei
Zweige, die nur heute gleich aussehen. Die Entscheidung, ob eine Wiederholung
zu einem gemeinsamen Baustein wird, bleibt eine Entscheidung.

Aufruf aus dem Quellordner:

    python tests/tools/dublettenpruefung.py
    python tests/tools/dublettenpruefung.py --laenge 8 --top 20

Braucht ausschließlich die Standardbibliothek und keine Anzeige.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import re
import sys

REPO = Path(__file__).resolve().parents[2]
QUELLEN = ("src/glide/app.pyw",)
# Zeilen, die überall gleich aussehen und als Dublette nichts aussagen.
RAUSCHEN = re.compile(r"^(try:|except.*:|finally:|pass|return|return \"break\"|else:|continue)$")


def kernzeilen(pfad):
    """Zeilennummern und normalisierte Zeilen einer Datei."""
    zeilen = []
    for nummer, roh in enumerate(pfad.read_text(encoding="utf-8-sig").splitlines(), 1):
        text = roh.split("#", 1)[0].strip() if not roh.strip().startswith("#") else ""
        if not text or RAUSCHEN.match(text):
            continue
        zeilen.append((nummer, text))
    return zeilen


def finde(quellen, laenge):
    """Sammelt identische Fenster von `laenge` Kernzeilen."""
    fenster = defaultdict(list)
    for pfad in quellen:
        zeilen = kernzeilen(pfad)
        for start in range(len(zeilen) - laenge + 1):
            block = tuple(text for _nummer, text in zeilen[start:start + laenge])
            fenster[block].append((pfad, zeilen[start][0], zeilen[start + laenge - 1][0]))
    return {block: stellen for block, stellen in fenster.items() if len(stellen) > 1}


def zusammenfassen(treffer, laenge):
    """Fasst überlappende Fundstellen zu je einer Meldung zusammen."""
    belegt = set()
    meldungen = []
    for block, stellen in sorted(treffer.items(), key=lambda paar: -len(paar[1])):
        schluessel = tuple(sorted((str(pfad), start) for pfad, start, _ende in stellen))
        if any((pfad, start) in belegt for pfad, start in
               ((s[0], s[1]) for s in stellen)):
            continue
        for pfad, start, ende in stellen:
            for zeile in range(start, ende + 1):
                belegt.add((pfad, zeile))
        meldungen.append((len(stellen), laenge, stellen))
        del schluessel
    return meldungen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--laenge", type=int, default=10,
                        help="Zeilen je Fenster (Vorgabe 10)")
    parser.add_argument("--top", type=int, default=15,
                        help="Wie viele Fundstellen gemeldet werden (Vorgabe 15)")
    parser.add_argument("--grenze", type=int, default=0,
                        help="Rückgabewert 1, wenn mehr Fundstellen gefunden werden")
    args = parser.parse_args()

    quellen = [REPO / name for name in QUELLEN]
    for pfad in quellen:
        if not pfad.is_file():
            raise SystemExit(f"Quelle fehlt: {pfad}")

    treffer = finde(quellen, args.laenge)
    meldungen = zusammenfassen(treffer, args.laenge)
    gesamt = sum(len(stellen) - 1 for _anzahl, _laenge, stellen in meldungen)

    print(f"DUBLETTEN  Fenster {args.laenge} Zeilen  ·  "
          f"{len(meldungen)} Fundstellen  ·  {gesamt} vermeidbare Wiederholungen")
    if not meldungen:
        print("Keine Wiederholung dieser Länge.")
        return 0
    for anzahl, laenge, stellen in meldungen[:args.top]:
        orte = ", ".join(f"{pfad.name}:{start}-{ende}" for pfad, start, ende in stellen)
        print(f"  {anzahl}× {laenge} Zeilen  →  {orte}")
    if len(meldungen) > args.top:
        print(f"  … und {len(meldungen) - args.top} weitere")
    print("\nEine Wiederholung ist ein Hinweis, kein Befund. Ob daraus ein "
          "gemeinsamer Baustein wird, entscheidet der Inhalt.")
    if args.grenze and len(meldungen) > args.grenze:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
