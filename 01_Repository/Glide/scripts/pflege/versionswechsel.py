"""Versionswechsel für Glide: Nummern, Fixtures und Standangaben.

Aufruf: python3 scripts/pflege/versionswechsel.py 3.33.0 01.10.2026
Löscht nichts. Überschriebene Fixtures liegen vorher im benachbarten Archiv;
Dokumente bekommen seit der Löschfreigabe vom 01.10.2026 keine Kopie mehr,
ihre Historie trägt Git (docs/DOKUMENTENPFLEGE.md).
"""
import pathlib
import re
import shutil
import subprocess
import sys

NEU, DATUM = sys.argv[1], sys.argv[2]
# Ablage-Wurzel: scripts/pflege → Glide → 01_Repository → Ablage
ABLAGE = pathlib.Path(__file__).resolve().parents[4]
REPO = ABLAGE / "01_Repository/Glide"
ALT = (REPO / "VERSION").read_text().strip()
E = f"_{ALT}_vor_{NEU}"


def archiv(pfad):
    ordner = pfad.parent
    ziel_ordner = next((ordner / n for n in ("archiv", "Archiv") if (ordner / n).is_dir()), ordner / "archiv")
    ziel_ordner.mkdir(exist_ok=True)
    ziel = ziel_ordner / f"{pfad.stem}{E}{pfad.suffix}"
    if not ziel.exists():
        shutil.copy2(pfad, ziel)
    return ziel


def ersetze(pfad, alt, neu, anzahl=1):
    text = pfad.read_text(encoding="utf-8")
    assert text.count(alt) == anzahl, (pfad, alt, text.count(alt))
    pfad.write_text(text.replace(alt, neu), encoding="utf-8")


(REPO / "VERSION").write_text(NEU + "\n")
ersetze(REPO / "src/glide/app.pyw", f'APP_VERSION = "{ALT}"', f'APP_VERSION = "{NEU}"')
ersetze(REPO / "tests/tools/releasedaten.py", f'APP_VERSION = "{ALT}"', f'APP_VERSION = "{NEU}"')
for name in ("test_glide.py", "test_glide_36.py", "test_features329.py"):
    ersetze(REPO / "tests/integration" / name, f'APP_VERSION == "{ALT}"', f'APP_VERSION == "{NEU}"')

beispiele = REPO / "tests/fixtures/beispiele"
for name in ("glide_beispieldaten.glidebackup", "glide_rundgang.glidebackup"):
    archiv(beispiele / name)
vorlagen = REPO / "src/glide/resources/templates/glide_vorlagen.glidetemplates"
archiv(vorlagen)
showcase = REPO / "tests/fixtures/showcase"
for name in ("Glide-Showcase.glidebackup", "Glide-Showcase_App.glideapp", "Glide-Showcase.glidetemplates", "manifest.json"):
    if (showcase / name).exists():
        archiv(showcase / name)
for werkzeug, argumente in (("beispieldaten.py", []), ("rundgang.py", []), ("showcase.py", []), ("vorlagendaten.py", []),
                            ("releasedaten.py", ["--ziel", str(beispiele / f"glide_releaseplanung_{NEU}.glidebackup")])):
    lauf = subprocess.run([sys.executable, "-B", str(REPO / "tests/tools" / werkzeug), *argumente],
                          capture_output=True, text=True, timeout=900)
    assert lauf.returncode == 0, (werkzeug, lauf.stderr[-2000:])
    print("erzeugt:", werkzeug)

befund = subprocess.run([sys.executable, "-B", str(REPO / "tests/tools/standpruefung.py")],
                        capture_output=True, text=True, cwd=ABLAGE).stdout
ziele = {}
for zeile in befund.splitlines():
    treffer = re.match(r"- (.+?\.md):(\d+): ", zeile)
    if treffer:
        ziele.setdefault(treffer.group(1), set()).add(int(treffer.group(2)))
for datei, zeilen in sorted(ziele.items()):
    pfad = ABLAGE / datei
    text = pfad.read_text(encoding="utf-8").split("\n")
    for nummer in zeilen:
        z = text[nummer - 1].replace(ALT, NEU)
        z = re.sub(r"(Stand:? |Stand der Dokumentationspflege: |Stand der Ablagebeschreibung |Entwicklungsstand )"
                   r"\d\d\.\d\d\.2026", rf"\g<1>{DATUM}", z)
        text[nummer - 1] = z
    pfad.write_text("\n".join(text), encoding="utf-8")
print(f"{len(ziele)} Standangaben angepasst; Archivendung {E}")
