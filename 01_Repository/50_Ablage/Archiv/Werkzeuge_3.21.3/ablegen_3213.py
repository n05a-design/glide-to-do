#!/usr/bin/env python3
"""Legt den Glide-3.21.3-Quellstand ab und raeumt zwei Archivluecken auf.

Aufruf im Ordner "Glide ToDo":

    python3 ablegen_3213.py 50_Ablage/Werkzeuge_3.21.3/quellstand

Wiederholbar: Was schon mit dem richtigen Inhalt am Zielort liegt, wird gemeldet
und nicht angefasst. Es wird nichts geloescht - Vorfassungen werden kopiert oder
verschoben.

Neu gegenueber 3.21.2:

* `tests/tools/standpruefung.py` kommt hinzu, `pruefen.py` haengt sie als dritte
  Analyse ein.
* `tests/README.md` und `tests/fixtures/README.md` werden mitgeliefert statt von
  Fortschreibungsregeln geflickt. Eine Datei, die als Ganzes ueber den
  SHA-256-Abgleich geht, kann nicht teilweise ueberholt sein.
* Neun ueberholte startbare Fassungen (3.14.0 bis 3.21.2) wandern ins Archiv von
  `07_Python-Versionen`. Dort reichte das Archiv nur bis 3.13.0: Seit 3.14 hatte
  niemand nachgezogen.
* Die drei Uebertragungspakete aus `Claude outputs` wandern nach
  `50_Ablage/Archiv/Uebertragungspakete`.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import sys
from pathlib import Path

ALT, NEU = "3.21.2", "3.21.3"
REPO_TEIL = "01_Repository/Glide"

# Quelldatei -> Ziel unterhalb von 01_Repository/Glide
ZIELE = (
    ("app.pyw", "src/glide/app.pyw"),
    ("VERSION", "VERSION"),
    ("pruefen.py", "tests/tools/pruefen.py"),
    ("standpruefung.py", "tests/tools/standpruefung.py"),
    ("beispieldaten.py", "tests/tools/beispieldaten.py"),
    ("releasedaten.py", "tests/tools/releasedaten.py"),
    ("test_glide.py", "tests/integration/test_glide.py"),
    ("test_glide_36.py", "tests/integration/test_glide_36.py"),
    ("tests_README.md", "tests/README.md"),
    ("fixtures_README.md", "tests/fixtures/README.md"),
    ("glide_vorlagen.glidetemplates", "src/glide/resources/templates/glide_vorlagen.glidetemplates"),
    ("glide_beispieldaten.glidebackup", "tests/fixtures/beispiele/glide_beispieldaten.glidebackup"),
    (f"glide_releaseplanung_{NEU}.glidebackup",
     f"tests/fixtures/beispiele/glide_releaseplanung_{NEU}.glidebackup"),
)

# Mitgelieferte Datenbestaende: Vorfassung vorher ins archiv/ des Zielordners.
# Die versionierten Releaseplanungen bleiben ausdruecklich aktiv - die
# Fixtureprueufung erwartet bei versioniertem Dateinamen genau dessen Version
# und belegt damit jede Formatstufe.
ARCHIVIEREN = {
    "src/glide/resources/templates/glide_vorlagen.glidetemplates":
        f"glide_vorlagen_{ALT}_vor_{NEU}.glidetemplates",
    "tests/fixtures/beispiele/glide_beispieldaten.glidebackup":
        f"glide_beispieldaten_{ALT}_vor_{NEU}.glidebackup",
    "tests/README.md": f"README_{ALT}_vor_{NEU}.md",
    "tests/fixtures/README.md": f"README_{ALT}_vor_{NEU}.md",
}

ARBEITSKOPIE = f"07_Python-Versionen/Glide-Aufgaben-und-Listen_v{NEU}.pyw"
PYTHON_ORDNER = "07_Python-Versionen"

# Nutzerkopien in 05_Probelisten_Testdaten: Quelldatei -> Zielname
PROBELISTEN = (
    ("glide_vorlagen.glidetemplates", f"Glide-Praxisvorlagen_{NEU}.glidetemplates"),
    ("glide_beispieldaten.glidebackup", f"Glide-Funktionsvorschau_{NEU}.glidebackup"),
    (f"glide_releaseplanung_{NEU}.glidebackup", f"Glide-Releaseplanung_{NEU}.glidebackup"),
)
PROBEORDNER = "05_Probelisten_Testdaten"

# Uebertragungspakete der Sitzung: aus 3.21.2 offen, jetzt entschieden.
PAKETORDNER = "Claude outputs"
PAKETZIEL = "50_Ablage/Archiv/Uebertragungspakete"


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


def als_tupel(wert: str) -> tuple[int, ...]:
    return tuple(int(t) for t in wert.split("."))


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Aufruf: python3 ablegen_3213.py <Ordner mit dem Quellstand>")
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

    def schieben(a: Path, z: Path) -> None:
        """Verschieben mit Quellpruefung. `mv -n` schweigt, wenn das Ziel schon
        existiert, und wer danach nur das Archiv prueft, haelt das Verschieben
        fuer erfolgreich, waehrend die Datei noch aktiv daneben liegt."""
        if not a.is_file():
            return
        if z.exists():
            verschoben.append(f"{a.relative_to(wurzel)} -> Ziel existiert schon, "
                              f"Quelle bleibt liegen: {z.relative_to(wurzel)}")
            return
        z.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(a), str(z))
        if a.exists():
            raise SystemExit(f"Quelle liegt nach dem Verschieben noch da: {a}")
        verschoben.append(f"{a.relative_to(wurzel)} -> {z.relative_to(wurzel)}")

    # 1. Quellstand ins Repository
    for name, ziel_rel in ZIELE:
        ablegen(quelle / name, repo / ziel_rel, ARCHIVIEREN.get(ziel_rel))

    # 2. Startbare Arbeitskopie samt Ressourcen
    ablegen(quelle / "app.pyw", wurzel / ARBEITSKOPIE)
    res_quelle = repo / "src/glide/resources/templates/glide_vorlagen.glidetemplates"
    res_ziel = wurzel / f"{PYTHON_ORDNER}/resources/templates/glide_vorlagen.glidetemplates"
    if res_ziel.parent.is_dir():
        ablegen(res_quelle, res_ziel, f"glide_vorlagen_{ALT}_vor_{NEU}.glidetemplates")

    # 3. Ueberholte startbare Fassungen ins Archiv. Bis 3.13.0 war das gepflegt,
    #    seit 3.14 nicht mehr: Neun Fassungen lagen aktiv neben der aktuellen.
    pyordner = wurzel / PYTHON_ORDNER
    if pyordner.is_dir():
        pyarchiv = archivordner(pyordner)
        muster = re.compile(r"Glide-Aufgaben-und-Listen_v(\d+\.\d+\.\d+)\.pyw")
        for eintrag in sorted(pyordner.iterdir()):
            if not eintrag.is_file():
                continue
            treffer = muster.fullmatch(eintrag.name)
            if not treffer or als_tupel(treffer.group(1)) >= als_tupel(NEU):
                continue
            schieben(eintrag, pyarchiv / eintrag.name)

    # 4. Nutzerkopien in 05_Probelisten_Testdaten; ueberholte aktive Fassungen
    #    wandern vorher ins Archiv.
    probe = wurzel / PROBEORDNER
    if probe.is_dir():
        archiv = archivordner(probe)
        muster = re.compile(r"Glide-(Praxisvorlagen|Funktionsvorschau|Releaseplanung)"
                            r"_\d+\.\d+\.\d+(_LIESMICH)?\.(glidetemplates|glidebackup|md)")
        zielnamen = {z for _, z in PROBELISTEN}
        for eintrag in sorted(probe.iterdir()):
            if not eintrag.is_file() or eintrag.name in zielnamen:
                continue
            if not muster.fullmatch(eintrag.name):
                continue
            schieben(eintrag, archiv / eintrag.name)
        for name, zielname in PROBELISTEN:
            ablegen(quelle / name, probe / zielname)

    # 5. Uebertragungspakete aus der Sitzungsablage
    pakete = wurzel / PAKETORDNER
    if pakete.is_dir():
        for eintrag in sorted(pakete.iterdir()):
            if eintrag.is_file() and eintrag.suffix.lower() == ".zip":
                schieben(eintrag, wurzel / PAKETZIEL / eintrag.name)

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
        raise SystemExit(f"VERSION steht nicht auf {NEU} - Ablage unvollstaendig")
    print("Quellstand abgelegt. Naechster Schritt: fortschreiben_3213.py --probe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
