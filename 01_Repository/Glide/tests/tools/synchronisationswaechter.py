#!/usr/bin/env python3
"""Wächter gegen Synchronisationskopien und stark geschrumpfte Hauptdokumente (W04).

Anlass: Mit 3.33.8 gelangten aus der OneDrive-Arbeitskopie sechs Konfliktkopien
(`<Name>-<Gerätename>.md`) und vier gekürzte Hauptdokumente ins Repository. Die
CI-Grundstufe prüfte damals weder das eine noch das andere.

Zwei Prüfungen, beide ohne Netz und ohne Schreibzugriff:

1. `synchronisationskopien`: eine Text- oder Codedatei `<Stamm>-<Zusatz><Endung>`,
   neben der `<Stamm><Endung>` im selben Ordner liegt. Schriften und Grafiken
   zählen nicht (`DejaVuSans-Bold.ttf`, `Glide-Logo-01.svg` sind gewollt), ein
   rein numerischer Zusatz ebenfalls nicht.
2. `geschrumpfte_dokumente`: ein Hauptdokument hat gegenüber der Vorfassung in
   Git mehr als `GRENZE` seiner Zeilen verloren und trägt in den ersten zwölf
   Zeilen keinen Vermerk („gekürzt“ oder „zusammengeführt“ mit dem Datum seiner
   Standzeile). Zusammenführen und Kürzen sind erlaubt (Dokumentenpflege),
   sie müssen aber im Dokument stehen.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath
import re
import subprocess

TEXTENDUNGEN = {".md", ".py", ".pyw", ".json", ".txt", ".ps1", ".cmd", ".yml", ".yaml", ".toml", ".cfg"}
GRENZE = 0.40
HAUPTDOKUMENTE = (
    "00_Arbeitsvorbereitung/Glide_Uebergabe.md",
    "00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md",
    "00_Arbeitsvorbereitung/Glide_Analyse.md",
    "00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md",
    "00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md",
    "01_Repository/Glide/AGENTS.md",
    "01_Repository/Glide/CHANGELOG.md",
    "01_Repository/Glide/docs/*.md",
    "01_Repository/Glide/docs/decisions/*.md",
)
STANDZEILE = re.compile(r"Stand (\d{2}\.\d{2}\.\d{4})")


def synchronisationskopien(pfade):
    """Paare (Kopie, Original) aus einer Liste relativer Pfade mit `/`."""
    bestand = {str(PurePosixPath(p)) for p in pfade}
    funde = []
    for pfad in sorted(bestand):
        teil = PurePosixPath(pfad)
        if teil.suffix.lower() not in TEXTENDUNGEN or "-" not in teil.stem:
            continue
        # Gerätenamen enthalten selbst Bindestriche („DESKTOP-4KQ2“,
        # „Name-MacBook-Pro“): jede Trennstelle prüfen, die kürzeste zuerst.
        teile = teil.stem.split("-")
        for schnitt in range(1, len(teile)):
            stamm, zusatz = "-".join(teile[:schnitt]), "-".join(teile[schnitt:])
            if not stamm or not zusatz or zusatz.replace("-", "").isdigit():
                continue
            original = str(teil.with_name(stamm + teil.suffix))
            if original in bestand:
                funde.append((pfad, original))
                break
    return funde


def ist_hauptdokument(pfad):
    teil = PurePosixPath(pfad)
    return any(teil.match(muster) for muster in HAUPTDOKUMENTE)


def hat_vermerk(text):
    kopf = text.splitlines()[:12]
    stand = None
    for zeile in kopf:
        treffer = STANDZEILE.search(zeile)
        if treffer:
            stand = treffer.group(1)
            break
    if not stand:
        return False
    return any(("gekürzt" in zeile.lower() or "zusammengeführt" in zeile.lower()) and stand in zeile
               for zeile in kopf)


def geschrumpft(vorher, nachher, grenze=GRENZE):
    """True, wenn `nachher` mehr als `grenze` der Zeilen von `vorher` verloren hat."""
    alt = len(vorher.splitlines())
    neu = len(nachher.splitlines())
    return alt > 0 and (alt - neu) / alt > grenze


def geschrumpfte_dokumente(paare):
    """Paare (Pfad, Vorfassung, aktuelle Fassung) → Liste (Pfad, Zeilen vorher, Zeilen jetzt)."""
    funde = []
    for pfad, vorher, nachher in paare:
        if vorher is None or nachher is None or not ist_hauptdokument(pfad):
            continue
        if geschrumpft(vorher, nachher) and not hat_vermerk(nachher):
            funde.append((pfad, len(vorher.splitlines()), len(nachher.splitlines())))
    return funde


def _git(ablage, *argumente):
    return subprocess.run(["git", *argumente], cwd=ablage, capture_output=True, check=False)


def arbeitsstand_pruefen(ablage: Path):
    """Prüft den Git-Arbeitsstand. Liefert (Kopien, geschrumpfte) oder None ohne Git."""
    liste = _git(ablage, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    if liste.returncode:
        return None
    pfade = [p for p in liste.stdout.decode("utf-8", "replace").split("\0") if p]
    kopien = synchronisationskopien(pfade)
    paare = []
    for pfad in pfade:
        if not ist_hauptdokument(pfad):
            continue
        datei = ablage / pfad
        if not datei.is_file():
            continue
        alt = _git(ablage, "show", f"HEAD:{pfad}")
        if alt.returncode:
            continue
        aktuell = datei.read_text(encoding="utf-8", errors="replace")
        vorher = alt.stdout.decode("utf-8", "replace")
        if aktuell == vorher:
            # In der CI ist der Arbeitsstand der Commit selbst; dann gegen den
            # Vorgänger vergleichen, falls er im Klon vorhanden ist.
            vorgaenger = _git(ablage, "show", f"HEAD~1:{pfad}")
            if vorgaenger.returncode:
                continue
            vorher = vorgaenger.stdout.decode("utf-8", "replace")
        paare.append((pfad, vorher, aktuell))
    return kopien, geschrumpfte_dokumente(paare)
