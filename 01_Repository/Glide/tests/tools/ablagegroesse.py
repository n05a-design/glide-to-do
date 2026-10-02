#!/usr/bin/env python3
"""Ablagegröße: verhindert, dass das Repository wieder aufgebläht wird.

Aufruf aus `01_Repository/Glide`:
    python3 -B tests/tools/ablagegroesse.py

Prüft alle versionierten Dateien der Ablage (`git ls-files`) gegen vier Regeln.
Anlass: Bis 3.33.6 legten `versionswechsel.py` und `showcase_abgleich.py` bei
jedem Lauf vollständige Kopien des Showcase und der Beispieldaten in
Archivordner, und jede Vollprüfung brachte rund 25 MB Fensterbilder mit. Die
Arbeitskopie wuchs dadurch an einem Tag von 1,2 auf 2,0 GB, obwohl Git alle
Vorfassungen ohnehin vorhält.

1. Fehlreste: keine `*.fetch`-Dateien (Reste abgebrochener Übertragungen).
2. Archivkopien: keine Glide-Datendateien in Archivordnern unter
   `tests/fixtures` und `05_Probelisten_Testdaten/Showcase`.
3. Fensterbilder: Vollprüfungen nach 3.33.6 versionieren nur ihr Ergebnis,
   nicht den Ordner `fenster/` mit den Bildschirmfotos.
4. Einzeldateien bis 50 MB; GitHub warnt ab 50 MB und lehnt ab 100 MB ab.

Liefert Exitcode 1 bei einem Fund. Die Regeln selbst sind Tk-frei und ohne
Git testbar (`test_ablagegroesse.py`).
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
# Einzige bewusst behaltene Archivdatei: die ursprünglichen Beispieldaten vor
# dem Showcase, im Dokumentationsindex als Vorsicherung verlinkt (24 KB).
ERLAUBTE_ARCHIVDATEIEN = {
    QUELLBAUM + "tests/fixtures/beispiele/archiv/glide_beispieldaten_3.32.3_vor_Showcase_2026-10-01.glidebackup",
}
FENSTERBILDER_BIS = (3, 33, 6)
QA_ORDNER = re.compile(r"qa-(\d+)\.(\d+)\.(\d+)")
GRENZE_MB = 50


def befunde(eintraege):
    """Regelverstöße für versionierte Dateien.

    `eintraege`: Folge von (Pfad relativ zur Ablage mit `/`, Größe in Bytes).
    Liefert eine Liste von (Regel, Pfad, Erläuterung).
    """
    funde = []
    for pfad, groesse in eintraege:
        teile = PurePosixPath(pfad).parts
        endung = PurePosixPath(pfad).suffix.lower()
        if endung == ".fetch":
            funde.append(("Fehlrest", pfad, "Rest einer abgebrochenen Übertragung"))
        if (endung in DATENFORMATE and pfad.startswith(ARCHIVBEREICHE)
                and any(teil.lower() == "archiv" for teil in teile) and pfad not in ERLAUBTE_ARCHIVDATEIEN):
            funde.append(("Archivkopie", pfad, "Vorfassungen trägt Git; keine Kopie im Archivordner"))
        if pfad.startswith(QUELLBAUM + "tests/qa-") and "fenster" in teile[:-1] and endung == ".png":
            version = QA_ORDNER.fullmatch(teile[3])
            if version and tuple(map(int, version.groups())) > FENSTERBILDER_BIS:
                funde.append(("Fensterbilder", pfad, "Bildschirmfotos der Vollprüfung bleiben lokal"))
        if groesse > GRENZE_MB * 1024 * 1024:
            funde.append(("Dateigröße", pfad, f"{groesse / 1048576:.0f} MB über {GRENZE_MB} MB"))
    return funde


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
        return text + "; keine Archivkopien, Fehlreste, neuen Fensterbilder oder Dateien über 50 MB"
    regeln = sorted({regel for regel, _, _ in funde})
    return (text + f"; {len(funde)} Funde ({', '.join(regeln)}): "
            + ", ".join(f"{pfad} ({grund})" for _, pfad, grund in funde[:5])
            + (" …" if len(funde) > 5 else ""))


def main():
    eintraege = versionierte_dateien()
    if eintraege is None:
        print("Hinweis: kein Git-Arbeitsstand; versionierte Dateien nicht ermittelbar")
        return 0
    funde = befunde(eintraege)
    print(zusammenfassung(eintraege, funde))
    return 1 if funde else 0


if __name__ == "__main__":
    sys.exit(main())
