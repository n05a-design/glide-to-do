"""Kürzt Archive und Nachweise auf die Aufbewahrungsregeln der Ablage.

Aufruf aus `01_Repository/Glide`:
    python3 -B scripts/pflege/ablage_kuerzen.py              # entfernen
    python3 -B scripts/pflege/ablage_kuerzen.py --anzeigen   # nur auflisten

Entfernt, was `tests/tools/ablagegroesse.py` als „Archivalter“ oder
„Fensterbilder“ meldet: Hauptdateien in `07_Python-Versionen/Archiv`,
Nachweisordner `tests/qa-<Version>` und Releaseplanungen außerhalb der sieben
neuesten Versionen sowie Fensterbilder außerhalb der drei neuesten
(Entscheidung des Inhabers vom 03.10.2026). Versionierte Dateien gehen über
`git rm`, die Vorfassungen bleiben in der Git-Historie; danach werden leere
Ordner entfernt. `versionswechsel.py` ruft das Werkzeug nach jedem
Versionswechsel auf.
"""
import argparse
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tests/tools"))
import ablagegroesse  # noqa: E402

REGELN = {"Archivalter", "Fensterbilder"}


def kandidaten():
    eintraege = ablagegroesse.versionierte_dateien()
    if eintraege is None:
        sys.exit("kein Git-Arbeitsstand; nichts gekürzt")
    funde = ablagegroesse.befunde(eintraege, ablagegroesse.aktuelle_version())
    return sorted({pfad for regel, pfad, _ in funde if regel in REGELN})


def leere_ordner_entfernen(ordner):
    for pfad in sorted(ordner, key=lambda p: len(p.parts), reverse=True):
        while pfad != ablagegroesse.ABLAGE and pfad.is_dir() and not any(pfad.iterdir()):
            pfad.rmdir()
            pfad = pfad.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--anzeigen", action="store_true", help="nur auflisten, nichts entfernen")
    args = parser.parse_args()
    pfade = kandidaten()
    for pfad in pfade:
        print(("würde entfernen: " if args.anzeigen else "entfernt: ") + pfad)
    if pfade and not args.anzeigen:
        for start in range(0, len(pfade), 200):
            subprocess.run(["git", "rm", "-q", "--", *pfade[start:start + 200]],
                           cwd=ablagegroesse.ABLAGE, check=True)
        leere_ordner_entfernen({(ablagegroesse.ABLAGE / pfad).parent for pfad in pfade})
    print(f"{len(pfade)} Dateien {'zu kürzen' if args.anzeigen else 'gekürzt'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
