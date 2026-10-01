#!/usr/bin/env python3
"""Legt den Glide-3.21.1-Quellstand im Repository ab.

Aufruf im Ordner "Glide ToDo":

    python3 ablegen_3211.py 50_Ablage/Werkzeuge_3.21.1/quellstand

Das Skript ist absichtlich wiederholbar: Jede Datei, die schon mit dem
richtigen Inhalt am Zielort liegt, wird gemeldet und nicht angefasst. Es
loescht nichts – Vorfassungen werden nur kopiert oder verschoben.
"""

from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

# Quelldatei -> Ziel unterhalb von 01_Repository/Glide
ZIELE = (
    ("app.pyw", "src/glide/app.pyw"),
    ("VERSION", "VERSION"),
    ("pruefen.py", "tests/tools/pruefen.py"),
    ("releasedaten.py", "tests/tools/releasedaten.py"),
    ("test_features320.py", "tests/integration/test_features320.py"),
    ("test_features321.py", "tests/integration/test_features321.py"),
    ("test_glide.py", "tests/integration/test_glide.py"),
    ("test_glide_36.py", "tests/integration/test_glide_36.py"),
    ("glide_vorlagen.glidetemplates", "src/glide/resources/templates/glide_vorlagen.glidetemplates"),
    ("glide_beispieldaten.glidebackup", "tests/fixtures/beispiele/glide_beispieldaten.glidebackup"),
    ("glide_releaseplanung_3.21.1.glidebackup",
     "tests/fixtures/beispiele/glide_releaseplanung_3.21.1.glidebackup"),
    )

# Ziel -> Name der Vorfassung im Unterordner "archiv" desselben Ordners.
# Nur fuer mitgelieferte Datenbestaende; Quelltext und Tests werden
# ueber die Arbeitskopien in 07_Python-Versionen historisiert.
ARCHIVIEREN = {
    "src/glide/resources/templates/glide_vorlagen.glidetemplates":
        "glide_vorlagen_3.21.0_vor_3.21.1.glidetemplates",
    "tests/fixtures/beispiele/glide_beispieldaten.glidebackup":
        "glide_beispieldaten_3.21.0_vor_3.21.1.glidebackup",
}

ARBEITSKOPIE = "07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.21.1.pyw"
REPO_TEIL = "01_Repository/Glide"


def pruefsumme(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def ablage_wurzel() -> Path:
    """Der Ordner "Glide ToDo" – erkennbar am Repository darunter."""
    for kandidat in (Path.cwd(), *Path.cwd().parents):
        if (kandidat / REPO_TEIL / "VERSION").is_file():
            return kandidat
    raise SystemExit(
        "Kein Ablageordner gefunden: Dieses Skript im Ordner \"Glide ToDo\" starten "
        f"(dort muss {REPO_TEIL}/VERSION liegen)."
    )


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Aufruf: python3 ablegen_3211.py <Ordner mit dem Quellstand>")
    quelle = Path(sys.argv[1]).expanduser()
    if not quelle.is_dir():
        raise SystemExit(f"Quellordner fehlt: {quelle}")

    wurzel = ablage_wurzel()
    repo = wurzel / REPO_TEIL

    fehlend = [name for name, _ in ZIELE if not (quelle / name).is_file()]
    if fehlend:
        raise SystemExit("Im Quellordner fehlen: " + ", ".join(fehlend))

    neu, ersetzt, unveraendert, archiviert = [], [], [], []

    for name, ziel_rel in ZIELE:
        src = quelle / name
        ziel = repo / ziel_rel
        soll = pruefsumme(src)

        if ziel.is_file() and pruefsumme(ziel) == soll:
            unveraendert.append(ziel_rel)
            continue

        if ziel.is_file() and ziel_rel in ARCHIVIEREN:
            archiv = ziel.parent / "archiv"
            archiv.mkdir(parents=True, exist_ok=True)
            kopie = archiv / ARCHIVIEREN[ziel_rel]
            if not kopie.exists():
                shutil.copy2(ziel, kopie)
                archiviert.append(str(kopie.relative_to(wurzel)))

        bestand = ziel.is_file()
        ziel.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, ziel)
        if pruefsumme(ziel) != soll:
            raise SystemExit(f"Pruefsumme nach dem Kopieren falsch: {ziel_rel}")
        (ersetzt if bestand else neu).append(ziel_rel)

    # Arbeitskopie des Quelltexts
    kopie_ziel = wurzel / ARBEITSKOPIE
    soll = pruefsumme(quelle / "app.pyw")
    if kopie_ziel.is_file() and pruefsumme(kopie_ziel) == soll:
        unveraendert.append(ARBEITSKOPIE)
    else:
        kopie_ziel.parent.mkdir(parents=True, exist_ok=True)
        bestand = kopie_ziel.is_file()
        shutil.copy2(quelle / "app.pyw", kopie_ziel)
        if pruefsumme(kopie_ziel) != soll:
            raise SystemExit("Pruefsumme der Arbeitskopie falsch")
        (ersetzt if bestand else neu).append(ARBEITSKOPIE)

    def liste(titel: str, werte: list[str]) -> None:
        print(f"\n{titel} ({len(werte)})")
        for wert in werte:
            print(f"  {wert}")

    print(f"Ablageordner: {wurzel}")
    liste("Neu angelegt", neu)
    liste("Ersetzt", ersetzt)
    liste("Bereits aktuell", unveraendert)
    liste("Vorfassungen archiviert", archiviert)

    version = (repo / "VERSION").read_text(encoding="utf-8").strip()
    print(f"\nVERSION im Repository: {version}")
    if version != "3.21.1":
        raise SystemExit("VERSION steht nicht auf 3.21.1 – Ablage unvollstaendig")
    print("Quellstand abgelegt. Naechster Schritt: fortschreiben_3211.py --probe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
