"""Gleicht 07_Python-Versionen mit src/glide ab – ohne zu löschen – und prüft SHA-256.

Aufruf: python3 scripts/pflege/abgleich_07.py

- Hauptdatei als `Glide-Aufgaben-und-Listen_v<VERSION>.pyw`, Module, `Schnellstart.pyw`,
  `resources` und `vendor` (ohne Archive).
- Ältere Hauptdateien wandern unter ihrem Namen nach `07_Python-Versionen/Archiv`
  (bis 03.10.2026 mit Endung `_Z`; sie werden aber behalten, nicht vorgemerkt).
  Das Archiv hält mit der aktuellen Fassung die sieben neuesten Versionen;
  ältere entfernt `ablage_kuerzen.py` beim Versionswechsel. Vollständige
  Vorstände trägt Git, keine Ordnerkopien.
- Danach `python3 packaging/macos/baue_app.py --ziel build/macos` für das Bundle.
- Exitcode 1 bei jeder Abweichung, auch wenn `07_Python-Versionen/README.md` die
  gelieferte Hauptdatei nicht nennt (der Lieferabsatz wird von Hand nachgeführt).
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
for modul in ("drawing.py", "drawing_image.py", "backdrop.py", "page_markdown.py", "image_preview.py", "logo.py", "schema_backups.py", "sidebar_policy.py", "svg_geometry.py", "home_tiles.py", "capture_parser.py", "eisenhower.py", "today_view.py", "content_search.py", "save_comparison.py", "view_metrics.py", "action_catalog.py", "ui_design.py", "planning.py", "day_proposal.py", "focus_timer.py", "task_references.py", "interaction_policy.py", "object_references.py", "week_planning.py", "page_features.py", "repeat_rules.py", "routines.py", "runtime_check.py", "release_notes.py", "appearance.py", "preview_tools.py", "filter_explain.py", "exchange_patch.py", "backup_diff.py", "render_retention.py", "logo_raster.py", "symbol_policy.py"):
    DATEIEN[modul] = modul


def sha(pfad):
    return hashlib.sha256(pfad.read_bytes()).hexdigest()


# Ältere startbare Fassungen aus dem Ordner nehmen, damit Schnellstart eindeutig ist.
for alt in ZIEL.glob("Glide-Aufgaben-und-Listen_v*.pyw"):
    if alt.name != DATEIEN["app.pyw"]:
        ziel = ZIEL / "Archiv" / alt.name
        if ziel.exists():
            sys.exit(f"{ziel} existiert schon")
        shutil.move(str(alt), str(ziel))
        print("ins Archiv:", ziel.name)

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
# Der Lieferabsatz der README beschreibt die Hauptdatei von Hand; der
# Versionswechsel führt nur die Standzeile nach (W12, Befund A15 vom 09.10.2026).
readme = ZIEL / "README.md"
if readme.exists() and DATEIEN["app.pyw"] not in readme.read_text(encoding="utf-8"):
    fehler.append(f"README.md nennt nicht {DATEIEN['app.pyw']} – Lieferabsatz nachführen")
print(f"{len(DATEIEN)} Code-Dateien und {anzahl} Ressourcen abgeglichen; Abweichungen: {fehler or 'keine'}")
if fehler:
    sys.exit(1)
