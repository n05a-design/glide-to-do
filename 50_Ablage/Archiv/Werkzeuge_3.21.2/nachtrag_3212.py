#!/usr/bin/env python3
"""Nachtrag zu 3.21.2: Stellen, die die Tokenregeln nicht erfassen konnten.

Gefunden bei der Endkontrolle nach dem Fortschreiben:

* Der Wurzel-README stand noch auf 3.21.0 – die Schreibweise
  „**3.21.0 vom 14.09.2026**" fehlte schon in den Regeln fuer 3.21.1, deshalb
  konnte das 3.21.2-Muster (das 3.21.1 erwartete) sie nicht treffen.
* Fuenf Dokumente verwiesen auf die Probedateien in ihren alten Fassungen
  (3.14.0 beziehungsweise 3.17.0). Die liegen seit dem Ablegen im Archiv – die
  Verweise waren also tote Links.
* Drei READMEs behaupteten „Glide 3.14.0" beziehungsweise „App-Stand 3.14.0"
  als den aktuellen Stand.
* Zwei Angaben zu Datenformaten und zum laufenden Pruefordner waren ueberholt.

Aufruf im Ordner "Glide ToDo":

    python3 nachtrag_3212.py --probe
    python3 nachtrag_3212.py

Wiederholbar: Steht das Ergebnis schon da, wird die Stelle uebersprungen.
Vorfassungen gehen ins Archiv desselben Ordners, sonst ins Sammelarchiv.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

NEU = "3.21.2"
REPO_TEIL = "01_Repository/Glide"
SAMMELARCHIV = f"50_Ablage/Archiv/Vorfassungen_vor_{NEU}"

# (pflicht, alt, neu)
REGELN: dict[str, tuple] = {
    "README.md": (
        (True, "**3.21.0 vom 14.09.2026**", f"**{NEU} vom 14.09.2026**"),
        # Der Vorspann nennt die Funktion, nicht den Stand – er bleibt. Die
        # Aufzaehlung bekommt den erweiterten Pruefbestand.
        (True, "Reiter und Pinnwände.",
         "Reiter und Pinnwände. Der mitgelieferte Beispielbestand deckt diese "
         "Funktionen seit 3.21.2 testbar ab: "
         "[Probedaten und Prüfwege](05_Probelisten_Testdaten/README.md)."),
    ),
    "20_Grafik_Master/README.md": (
        (True, "## Stand 13.09.2026 · Glide 3.14.0",
         f"## Stand 14.09.2026 · Glide {NEU}"),
    ),
    "50_Ablage/README.md": (
        (True, "Der aktuelle App- und QA-Stand ist Glide 3.14.0.",
         f"Der aktuelle App- und QA-Stand ist Glide {NEU}."),
        (True, "die\nlaufende Prüfung liegt unter `01_Repository/Glide/tests/qa-3.14.0/`.",
         f"die\nlaufende Prüfung liegt unter `01_Repository/Glide/tests/qa-{NEU}/`."),
    ),
    "90_Testdaten_Extern/README.md": (
        (True, "`Glide-Funktionsvorschau_3.14.0.glidebackup`",
         f"`Glide-Funktionsvorschau_{NEU}.glidebackup`"),
        (True, "für die Datenformate 4 bis 13 sowie Legacy 2",
         "für die Datenformate 4 bis 15 sowie Legacy 2"),
        (True, "## Stand 13.09.2026 · aktueller App-Stand 3.14.0",
         f"## Stand 14.09.2026 · aktueller App-Stand {NEU}"),
    ),
    f"{REPO_TEIL}/docs/27_VORLAGEN_PRAXISANLEITUNG.md": (
        (True, "**Glide-Praxisvorlagen_3.14.0.glidetemplates**",
         f"**Glide-Praxisvorlagen_{NEU}.glidetemplates**"),
        (True, "**Glide-Funktionsvorschau_3.14.0.glidebackup**",
         f"**Glide-Funktionsvorschau_{NEU}.glidebackup**"),
        (True, "**Glide-Releaseplanung_3.14.0.glidebackup**",
         f"**Glide-Releaseplanung_{NEU}.glidebackup**"),
        (True, "Ausprobieren von Ansichten, Wiederholungen, Labels und Anhängen.",
         "Ausprobieren von Ansichten, Wiederholungen, Labels und Anhängen. Die Liste "
         "„Kalender, Erinnerungen und Tagesplanung“ deckt zusätzlich Erinnerungen, "
         "Tagesplanung und den Kalenderrundlauf ab."),
    ),
    "10_Dokumentation/Vorlagen_Praxisanleitung_3.21.2.md": (
        (True, "**Glide-Praxisvorlagen_3.17.0.glidetemplates**",
         f"**Glide-Praxisvorlagen_{NEU}.glidetemplates**"),
        (True, "**Glide-Funktionsvorschau_3.17.0.glidebackup**",
         f"**Glide-Funktionsvorschau_{NEU}.glidebackup**"),
        (True, "**Glide-Releaseplanung_3.17.0.glidebackup**",
         f"**Glide-Releaseplanung_{NEU}.glidebackup**"),
        # Der Vorspann bewarb noch die Neuerung aus 3.14.
        (True, "Neu in 3.14: freiwilliger Bearbeitungstag und geschätzter Aufwand in Minuten, getrennt von Fälligkeit und „Mein Tag“. Beide Angaben stehen in Punktdetails, Mehrfachbearbeitung, Tabelle und Reitern und werden in Backups und Vorlagen mitgeführt. [Bedienung und Datenregeln](../01_Repository/Glide/docs/37_PLANUNG_UND_AUFWAND_3.14.0.md).",
         "Neu in 3.21.2: Der mitgelieferte Beispielbestand deckt die Funktionen seit 3.14 "
         "testbar ab – beide Erinnerungsarten, sechs Punkte auf einem Bearbeitungstag mit "
         "270 Minuten und alle sechs Wiederholungsarten. "
         "[Probedaten und Prüfwege](../05_Probelisten_Testdaten/README.md)."),
    ),
}


def ablage_wurzel() -> Path:
    for kandidat in (Path.cwd(), *Path.cwd().parents):
        if (kandidat / REPO_TEIL / "VERSION").is_file():
            return kandidat
    raise SystemExit("Kein Ablageordner gefunden: im Ordner \"Glide ToDo\" starten.")


def vorhandenes_archiv(ordner: Path) -> Path | None:
    if ordner.is_dir():
        for eintrag in sorted(ordner.iterdir()):
            if eintrag.is_dir() and eintrag.name.lower() == "archiv":
                return eintrag
    return None


def main() -> int:
    p = argparse.ArgumentParser(description=f"Nachtrag zu {NEU}")
    p.add_argument("--probe", action="store_true")
    args = p.parse_args()
    wurzel = ablage_wurzel()
    geschrieben, archiviert, fehler, uebersprungen = [], [], [], []

    for rel, regeln in REGELN.items():
        datei = wurzel / rel
        if not datei.is_file():
            fehler.append(f"Datei fehlt: {rel}")
            continue
        alt = datei.read_text(encoding="utf-8")
        neu = alt
        for pflicht, muster, ersatz in regeln:
            if ersatz in neu:
                uebersprungen.append(f"{rel}: steht schon richtig")
                continue
            if muster in neu:
                neu = neu.replace(muster, ersatz, 1)
            elif pflicht:
                fehler.append(f"{rel}: Pflichtstelle fehlt – {muster[:70]!r}")
        if neu == alt:
            continue
        eigenes = vorhandenes_archiv(datei.parent)
        if eigenes is not None:
            ziel = eigenes / f"{datei.stem}_vor_{NEU}_nachtrag{datei.suffix}"
        else:
            pfad = datei.relative_to(wurzel).parent.as_posix()
            vorsatz = (pfad.replace("/", "__") + "__") if pfad not in ("", ".") else ""
            ziel = wurzel / SAMMELARCHIV / f"{vorsatz}{datei.stem}_vor_{NEU}_nachtrag{datei.suffix}"
        if not ziel.exists():
            if not args.probe:
                ziel.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(datei, ziel)
            archiviert.append(str(ziel.relative_to(wurzel)) + ("   (Probe)" if args.probe else ""))
        if not args.probe:
            datei.write_text(neu, encoding="utf-8")
        geschrieben.append(rel + ("   (Probe)" if args.probe else ""))

    def liste(titel: str, werte: list[str]) -> None:
        print(f"\n{titel} ({len(werte)})")
        for wert in werte:
            print(f"  {wert}")

    print(f"Ablageordner: {wurzel}")
    print(f"Modus: {'PROBE' if args.probe else 'schreiben'}")
    liste("Richtiggestellt", geschrieben)
    liste("Vorfassungen archiviert", archiviert)
    liste("Bereits richtig", uebersprungen)
    if fehler:
        liste("NICHT ERLEDIGT", fehler)
        print("\nAbgebrochen: Die genannten Stellen passen nicht zur Erwartung.")
        return 1
    print("\nNachtrag vollständig" if not args.probe else "\nProbe beendet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
