#!/usr/bin/env python3
"""Legt den Glide-3.21.2-Quellstand ab und erneuert die Probedateien.

Aufruf im Ordner "Glide ToDo":

    python3 ablegen_3212.py 50_Ablage/Werkzeuge_3.21.2/quellstand

Wiederholbar: Was schon mit dem richtigen Inhalt am Zielort liegt, wird gemeldet
und nicht angefasst. Es wird nichts geloescht – Vorfassungen werden kopiert oder
verschoben.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import sys
from pathlib import Path

ALT, NEU = "3.21.1", "3.21.2"
REPO_TEIL = "01_Repository/Glide"

# Quelldatei -> Ziel unterhalb von 01_Repository/Glide
ZIELE = (
    ("app.pyw", "src/glide/app.pyw"),
    ("VERSION", "VERSION"),
    ("pruefen.py", "tests/tools/pruefen.py"),
    ("beispieldaten.py", "tests/tools/beispieldaten.py"),
    ("vorlagendaten.py", "tests/tools/vorlagendaten.py"),
    ("test_features320.py", "tests/integration/test_features320.py"),
    ("test_features321.py", "tests/integration/test_features321.py"),
    ("releasedaten.py", "tests/tools/releasedaten.py"),
    ("test_glide.py", "tests/integration/test_glide.py"),
    ("test_glide_36.py", "tests/integration/test_glide_36.py"),
    ("glide_vorlagen.glidetemplates", "src/glide/resources/templates/glide_vorlagen.glidetemplates"),
    ("glide_beispieldaten.glidebackup", "tests/fixtures/beispiele/glide_beispieldaten.glidebackup"),
    (f"glide_releaseplanung_{NEU}.glidebackup",
     f"tests/fixtures/beispiele/glide_releaseplanung_{NEU}.glidebackup"),
)

# Mitgelieferte Datenbestaende: Vorfassung vorher ins archiv/ des Zielordners.
ARCHIVIEREN = {
    "src/glide/resources/templates/glide_vorlagen.glidetemplates":
        f"glide_vorlagen_{ALT}_vor_{NEU}.glidetemplates",
    "tests/fixtures/beispiele/glide_beispieldaten.glidebackup":
        f"glide_beispieldaten_{ALT}_vor_{NEU}.glidebackup",
}

ARBEITSKOPIE = f"07_Python-Versionen/Glide-Aufgaben-und-Listen_v{NEU}.pyw"

# Nutzerkopien in 05_Probelisten_Testdaten: Quelldatei -> Zielname
PROBELISTEN = (
    ("glide_vorlagen.glidetemplates", f"Glide-Praxisvorlagen_{NEU}.glidetemplates"),
    ("glide_beispieldaten.glidebackup", f"Glide-Funktionsvorschau_{NEU}.glidebackup"),
    (f"glide_releaseplanung_{NEU}.glidebackup", f"Glide-Releaseplanung_{NEU}.glidebackup"),
)
PROBEORDNER = "05_Probelisten_Testdaten"

# Ueberholte Testfassungen, die im aktiven Suitenordner lagen.
VERSCHIEBEN = (
    ("tests/integration/test_glide_3.12.0_vor_3.13.0.py",
     "tests/integration/archiv/test_glide_3.12.0_vor_3.13.0.py"),
    ("tests/integration/test_glide_36_3.12.0_vor_3.13.0.py",
     "tests/integration/archiv/test_glide_36_3.12.0_vor_3.13.0.py"),
)


def pruefsumme(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def ablage_wurzel() -> Path:
    for kandidat in (Path.cwd(), *Path.cwd().parents):
        if (kandidat / REPO_TEIL / "VERSION").is_file():
            return kandidat
    raise SystemExit("Kein Ablageordner gefunden: im Ordner \"Glide ToDo\" starten.")


def archivordner(ordner: Path) -> Path:
    """Echte Schreibung des Archivordners verwenden, sonst Archiv/ anlegen."""
    if ordner.is_dir():
        for eintrag in sorted(ordner.iterdir()):
            if eintrag.is_dir() and eintrag.name.lower() == "archiv":
                return eintrag
    return ordner / "Archiv"


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Aufruf: python3 ablegen_3212.py <Ordner mit dem Quellstand>")
    quelle = Path(sys.argv[1]).expanduser()
    if not quelle.is_dir():
        raise SystemExit(f"Quellordner fehlt: {quelle}")

    wurzel = ablage_wurzel()
    repo = wurzel / REPO_TEIL

    fehlend = [n for n, _ in ZIELE if not (quelle / n).is_file()]
    if fehlend:
        raise SystemExit("Im Quellordner fehlen: " + ", ".join(fehlend))

    neu, ersetzt, unveraendert, archiviert, verschoben = [], [], [], [], []

    def ablegen(src: Path, ziel: Path, archivname: str | None = None) -> None:
        soll = pruefsumme(src)
        if ziel.is_file() and pruefsumme(ziel) == soll:
            unveraendert.append(str(ziel.relative_to(wurzel)))
            return
        if ziel.is_file() and archivname:
            kopie = archivordner(ziel.parent) / archivname
            if not kopie.exists():
                kopie.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ziel, kopie)
                archiviert.append(str(kopie.relative_to(wurzel)))
        bestand = ziel.is_file()
        ziel.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, ziel)
        if pruefsumme(ziel) != soll:
            raise SystemExit(f"Pruefsumme nach dem Kopieren falsch: {ziel}")
        (ersetzt if bestand else neu).append(str(ziel.relative_to(wurzel)))

    # 1. Quellstand ins Repository
    for name, ziel_rel in ZIELE:
        ablegen(quelle / name, repo / ziel_rel, ARCHIVIEREN.get(ziel_rel))

    # 2. Startbare Arbeitskopie
    ablegen(quelle / "app.pyw", wurzel / ARBEITSKOPIE)
    # Ressourcen der Arbeitskopie mitziehen, damit sie startfaehig bleibt.
    res_quelle = repo / "src/glide/resources/templates/glide_vorlagen.glidetemplates"
    res_ziel = wurzel / "07_Python-Versionen/resources/templates/glide_vorlagen.glidetemplates"
    if res_ziel.parent.is_dir():
        ablegen(res_quelle, res_ziel, f"glide_vorlagen_{ALT}_vor_{NEU}.glidetemplates")

    # 3. Nutzerkopien in 05_Probelisten_Testdaten; ueberholte aktive Fassungen
    #    wandern vorher ins Archiv. Der Ordner-README behauptete bisher, aeltere
    #    Fassungen lagen dort – tatsaechlich lagen acht davon aktiv daneben.
    probe = wurzel / PROBEORDNER
    archiv = archivordner(probe)
    if probe.is_dir():
        muster = re.compile(r"Glide-(Praxisvorlagen|Funktionsvorschau|Releaseplanung)"
                            r"_\d+\.\d+\.\d+(_LIESMICH)?\.(glidetemplates|glidebackup|md)")
        zielnamen = {z for _, z in PROBELISTEN}
        for eintrag in sorted(probe.iterdir()):
            if not eintrag.is_file() or eintrag.name in zielnamen:
                continue
            if not muster.fullmatch(eintrag.name):
                continue
            ziel = archiv / eintrag.name
            if ziel.exists():
                continue
            archiv.mkdir(parents=True, exist_ok=True)
            shutil.move(str(eintrag), str(ziel))
            verschoben.append(f"{PROBEORDNER}/{eintrag.name} -> {ziel.relative_to(wurzel)}")
        for name, zielname in PROBELISTEN:
            ablegen(quelle / name, probe / zielname)

    # 4. Ueberholte Testfassungen aus dem aktiven Suitenordner
    for alt_rel, neu_rel in VERSCHIEBEN:
        a, z = repo / alt_rel, repo / neu_rel
        if not a.is_file():
            continue
        if z.exists():
            continue
        z.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(a), str(z))
        verschoben.append(f"{REPO_TEIL}/{alt_rel} -> {REPO_TEIL}/{neu_rel}")

    def liste(titel: str, werte: list[str]) -> None:
        print(f"\n{titel} ({len(werte)})")
        for wert in werte:
            print(f"  {wert}")

    print(f"Ablageordner: {wurzel}")
    liste("Neu angelegt", neu)
    liste("Ersetzt", ersetzt)
    liste("Bereits aktuell", unveraendert)
    liste("Vorfassungen archiviert", archiviert)
    liste("Verschoben", verschoben)

    version = (repo / "VERSION").read_text(encoding="utf-8").strip()
    print(f"\nVERSION im Repository: {version}")
    if version != NEU:
        raise SystemExit(f"VERSION steht nicht auf {NEU} – Ablage unvollstaendig")
    print(f"Quellstand abgelegt. Naechster Schritt: fortschreiben_3212.py --probe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
