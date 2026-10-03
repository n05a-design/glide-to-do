#!/usr/bin/env python3
"""Ablagegröße: verhindert, dass das Repository wieder aufgebläht wird.

Aufruf aus `01_Repository/Glide`:
    python3 -B tests/tools/ablagegroesse.py

Prüft alle versionierten Dateien der Ablage (`git ls-files`) gegen fünf Regeln.
Anlass: Bis 3.33.6 legten `versionswechsel.py` und `showcase_abgleich.py` bei
jedem Lauf vollständige Kopien des Showcase und der Beispieldaten in
Archivordner, und jede Vollprüfung brachte rund 25 MB Fensterbilder mit. Die
Arbeitskopie wuchs dadurch an einem Tag von 1,2 auf 2,0 GB, obwohl Git alle
Vorfassungen ohnehin vorhält. Am 03.10.2026 hat der Inhaber Archive und
Nachweise auf die sieben neuesten Versionen und Bildschirmfotos auf die drei
neuesten begrenzt.

1. Fehlreste: keine `*.fetch`-Dateien (Reste abgebrochener Übertragungen).
2. Archivkopien: keine Glide-Datendateien in Archivordnern unter
   `tests/fixtures` und `05_Probelisten_Testdaten/Showcase`.
3. Archivalter: Hauptdateien in `07_Python-Versionen/Archiv`, Nachweisordner
   `tests/qa-<Version>` und Releaseplanungen in `tests/fixtures/beispiele`
   gehören zu den sieben neuesten Versionen. Ausgenommen sind die
   Releaseplanungen in `DAUERHAFT`.
4. Fensterbilder: nur in den drei neuesten Versionen, und Vollprüfungen nach
   3.33.6 versionieren den Ordner `fenster/` gar nicht mehr.
5. Einzeldateien bis 50 MB; GitHub warnt ab 50 MB und lehnt ab 100 MB ab.

Liefert Exitcode 1 bei einem Fund. Die Regeln selbst sind Tk-frei und ohne
Git testbar (`test_ablagegroesse.py`); `scripts/pflege/ablage_kuerzen.py`
entfernt, was die Regeln 3 und 4 melden.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

ABLAGE = Path(__file__).resolve().parents[4]
QUELLBAUM = "01_Repository/Glide/"
DATENFORMATE = {".glidebackup", ".glideapp", ".glidetemplates"}
ARCHIVBEREICHE = (QUELLBAUM + "tests/fixtures/", "05_Probelisten_Testdaten/Showcase/")
ARCHIV_VERSIONEN = 7
BILDER_VERSIONEN = 3
FENSTERBILDER_BIS = (3, 33, 6)
GRENZE_MB = 50
_V = r"(\d+\.\d+\.\d+)"
# Pfade, deren Version die Aufbewahrung bestimmt.
VERSIONIERT = (
    # Bis 03.10.2026 mit Endung „_Z“ abgelegt; beide Schreibweisen zählen.
    re.compile(r"07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v" + _V + r"(?:_Z)?\.pyw"),
    re.compile(re.escape(QUELLBAUM) + r"tests/qa-" + _V + r"/.+"),
    re.compile(re.escape(QUELLBAUM) + r"tests/fixtures/beispiele/glide_releaseplanung_" + _V + r"\.glidebackup"),
)
QA_ORDNER = re.compile(re.escape(QUELLBAUM) + r"tests/qa-" + _V + r"/")
# Bleiben außerhalb der sieben Versionen: je Datenformat die letzte
# Releaseplanung (11–19) als Lesbarkeitsbeleg der Fixtureprüfung und 3.30.0,
# die test_tempo330 als feste Messgrundlage liest.
DAUERHAFT = frozenset(
    QUELLBAUM + f"tests/fixtures/beispiele/glide_releaseplanung_{version}.glidebackup"
    for version in ("3.6.0", "3.7.0", "3.13.0", "3.18.0", "3.21.4", "3.25.0", "3.26.0",
                    "3.28.0", "3.29.0", "3.30.0"))


def als_tupel(version):
    return tuple(int(teil) for teil in version.split("."))


def pfadversion(pfad):
    """Version, an der die Aufbewahrung eines Pfads hängt, sonst None."""
    for muster in VERSIONIERT:
        treffer = muster.fullmatch(pfad)
        if treffer:
            return treffer.group(1)
    return None


def neueste_versionen(eintraege, aktuell=None, anzahl=ARCHIV_VERSIONEN):
    """Die `anzahl` neuesten Versionen aus versionierten Pfaden und `aktuell`."""
    versionen = {pfadversion(pfad) for pfad, _ in eintraege} - {None}
    if aktuell:
        versionen.add(aktuell)
    return set(sorted(versionen, key=als_tupel)[-anzahl:])


def befunde(eintraege, aktuell=None):
    """Regelverstöße für versionierte Dateien.

    `eintraege`: Folge von (Pfad relativ zur Ablage mit `/`, Größe in Bytes).
    `aktuell`: Inhalt von VERSION; zählt mit, auch wenn noch nichts dazu liegt.
    Liefert eine Liste von (Regel, Pfad, Erläuterung).
    """
    eintraege = list(eintraege)
    archiv = neueste_versionen(eintraege, aktuell)
    bilder = neueste_versionen(eintraege, aktuell, BILDER_VERSIONEN)
    funde = []
    for pfad, groesse in eintraege:
        teile = PurePosixPath(pfad).parts
        endung = PurePosixPath(pfad).suffix.lower()
        version = pfadversion(pfad)
        if endung == ".fetch":
            funde.append(("Fehlrest", pfad, "Rest einer abgebrochenen Übertragung"))
        if (endung in DATENFORMATE and pfad.startswith(ARCHIVBEREICHE)
                and any(teil.lower() == "archiv" for teil in teile)):
            funde.append(("Archivkopie", pfad, "Vorfassungen trägt Git; keine Kopie im Archivordner"))
        if version and version not in archiv and pfad not in DAUERHAFT:
            funde.append(("Archivalter", pfad, f"{version} liegt vor den {ARCHIV_VERSIONEN} neuesten Versionen"))
        elif QA_ORDNER.match(pfad) and "fenster" in teile[:-1] and endung == ".png":
            if als_tupel(version) > FENSTERBILDER_BIS:
                funde.append(("Fensterbilder", pfad, "Bildschirmfotos der Vollprüfung bleiben lokal"))
            elif version not in bilder:
                funde.append(("Fensterbilder", pfad,
                              f"{version} liegt vor den {BILDER_VERSIONEN} neuesten Versionen"))
        if groesse > GRENZE_MB * 1024 * 1024:
            funde.append(("Dateigröße", pfad, f"{groesse / 1048576:.0f} MB über {GRENZE_MB} MB"))
    return funde


def aktuelle_version(ablage=ABLAGE):
    pfad = ablage / QUELLBAUM / "VERSION"
    return pfad.read_text(encoding="utf-8").strip() if pfad.is_file() else None


def versionierte_dateien(ablage=ABLAGE):
    """(Pfad, Größe) aller versionierten Dateien; None ohne Git-Arbeitsstand."""
    try:
        roh = subprocess.run(["git", "ls-files", "-z"], cwd=ablage, capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    eintraege = []
    for name in filter(None, roh.split(b"\0")):
        pfad = name.decode("utf-8", "surrogateescape")
        datei = ablage / pfad
        if datei.is_file():
            eintraege.append((pfad, datei.stat().st_size))
    return eintraege


def zusammenfassung(eintraege, funde):
    gesamt = sum(groesse for _, groesse in eintraege) / 1048576
    text = f"{len(eintraege)} versionierte Dateien, {gesamt:.0f} MB"
    if not funde:
        return (text + f"; keine Archivkopien, Fehlreste, Dateien über {GRENZE_MB} MB, Archive und "
                f"Nachweise nur der {ARCHIV_VERSIONEN} neuesten, Fensterbilder nur der "
                f"{BILDER_VERSIONEN} neuesten Versionen")
    regeln = sorted({regel for regel, _, _ in funde})
    return (text + f"; {len(funde)} Funde ({', '.join(regeln)}): "
            + ", ".join(f"{pfad} ({grund})" for _, pfad, grund in funde[:5])
            + (" …" if len(funde) > 5 else "")
            + ("; kürzen mit scripts/pflege/ablage_kuerzen.py"
               if {"Archivalter", "Fensterbilder"} & set(regeln) else ""))


def main():
    eintraege = versionierte_dateien()
    if eintraege is None:
        print("Hinweis: kein Git-Arbeitsstand; versionierte Dateien nicht ermittelbar")
        return 0
    funde = befunde(eintraege, aktuelle_version())
    print(zusammenfassung(eintraege, funde))
    return 1 if funde else 0


if __name__ == "__main__":
    sys.exit(main())
