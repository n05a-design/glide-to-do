"""Gleicht 07_Python-Versionen mit src/glide ab – ohne zu löschen – und prüft SHA-256.

Aufruf: python3 scripts/pflege/abgleich_07.py

- Hauptdatei als `Glide-Aufgaben-und-Listen_v<VERSION>.pyw`, Module, `Schnellstart.pyw`,
  `resources` und `vendor` (ohne Archive).
- Ältere Hauptdateien wandern mit Endung `_Z` nach `07_Python-Versionen/Archiv`;
  vorher den vollständigen Stand als Ordner archivieren.
- Danach `python3 packaging/macos/baue_app.py --ziel build/macos` für das Bundle.
"""
import hashlib
import pathlib
import shutil
import sys

# Ablage-Wurzel: scripts/pflege → Glide → 01_Repository → Ablage
ABLAGE = pathlib.Path(__file__).resolve().parents[4]
SRC = ABLAGE / "01_Repository/Glide/src/glide"
ZIEL = ABLAGE / "07_Python-Versionen"
VERSION = (ABLAGE / "01_Repository/Glide/VERSION").read_text().strip()

DATEIEN = {"app.pyw": f"Glide-Aufgaben-und-Listen_v{VERSION}.pyw", "glide_start.py": "Schnellstart.pyw"}
for modul in ("drawing.py", "drawing_image.py", "backdrop.py", "page_markdown.py", "image_preview.py", "logo.py", "schema_backups.py"):
    DATEIEN[modul] = modul


def sha(pfad):
    return hashlib.sha256(pfad.read_bytes()).hexdigest()


# Ältere startbare Fassungen aus dem Ordner nehmen, damit Schnellstart eindeutig ist.
for alt in ZIEL.glob("Glide-Aufgaben-und-Listen_v*.pyw"):
    if alt.name != DATEIEN["app.pyw"]:
        ziel = ZIEL / "Archiv" / (alt.stem + "_Z" + alt.suffix)
        if ziel.exists():
            sys.exit(f"{ziel} existiert schon")
        shutil.move(str(alt), str(ziel))
        print("ins Archiv (Endung _Z):", ziel.name)

fehler = []
for quelle, name in DATEIEN.items():
    shutil.copy2(SRC / quelle, ZIEL / name)
    if sha(SRC / quelle) != sha(ZIEL / name):
        fehler.append(name)
anzahl = 0
for ordner in ("resources", "vendor"):
    for datei in sorted((SRC / ordner).rglob("*")):
        if datei.is_dir() or "__pycache__" in datei.parts or "archiv" in datei.parts:
            continue
        ziel = ZIEL / datei.relative_to(SRC)
        ziel.parent.mkdir(parents=True, exist_ok=True)
        if not ziel.exists() or sha(ziel) != sha(datei):
            shutil.copy2(datei, ziel)
        if sha(ziel) != sha(datei):
            fehler.append(str(ziel))
        anzahl += 1
print(f"{len(DATEIEN)} Code-Dateien und {anzahl} Ressourcen abgeglichen; Abweichungen: {fehler or 'keine'}")
