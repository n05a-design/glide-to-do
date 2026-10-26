"""Versionswechsel für Glide: Nummern, Fixtures und Standangaben.

Aufruf: python3 scripts/pflege/versionswechsel.py 3.33.0 01.10.2026
Legt keine Archivkopien an: Vorfassungen von Fixtures, Showcase, Vorlagen und
Dokumenten trägt Git (docs/DOKUMENTENPFLEGE.md). Bis 3.33.6 entstand hier je
Versionswechsel rund 75 MB Kopien; die CI-Grundstufe weist neue Archivkopien
zurück (tests/tools/ablagegroesse.py). Zum Schluss kürzt `ablage_kuerzen.py`
Archive und Nachweise auf die sieben neuesten Versionen und Fensterbilder auf
die drei neuesten (Entscheidung des Inhabers vom 03.10.2026).
"""
import pathlib
import argparse
import os
import tempfile
import re
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("version")
parser.add_argument("datum")
parser.add_argument("--ohne-git-index", action="store_true",
                    help="Aufbewahrung nur in Arbeitsdateien kürzen; den Git-Index nicht ändern")
args = parser.parse_args()
NEU, DATUM = args.version, args.datum
# Ablage-Wurzel: scripts/pflege → Glide → 01_Repository → Ablage
ABLAGE = pathlib.Path(__file__).resolve().parents[4]
REPO = ABLAGE / "01_Repository/Glide"
ALT = (REPO / "VERSION").read_text().strip()


def schreibe(pfad, text):
    """LF erhalten und einen Fehler beim Öffnen der Zieldatei nicht truncierend behandeln."""
    fd, name = tempfile.mkstemp(prefix=".glide-version-", suffix=".tmp", dir=pfad.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as file:
            file.write(text)
            file.flush()
            os.fsync(file.fileno())
        os.replace(name, pfad)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def ersetze(pfad, alt, neu, anzahl=1):
    text = pfad.read_text(encoding="utf-8")
    assert text.count(alt) == anzahl, (pfad, alt, text.count(alt))
    schreibe(pfad, text.replace(alt, neu))


ersetze(REPO / "src/glide/app.pyw", f'APP_VERSION = "{ALT}"', f'APP_VERSION = "{NEU}"')
schreibe(REPO / "VERSION", NEU + "\n")
ersetze(REPO / "tests/tools/releasedaten.py", f'APP_VERSION = "{ALT}"', f'APP_VERSION = "{NEU}"')
for name in ("test_glide.py", "test_glide_36.py", "test_features329.py"):
    ersetze(REPO / "tests/integration" / name, f'APP_VERSION == "{ALT}"', f'APP_VERSION == "{NEU}"')

beispiele = REPO / "tests/fixtures/beispiele"
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
    schreibe(pfad, "\n".join(text))
print(f"{len(ziele)} Standangaben angepasst")
kuerzen = subprocess.run([sys.executable, "-B", str(REPO / "scripts/pflege/ablage_kuerzen.py"),
                         *(["--ohne-git-index"] if args.ohne_git_index else [])],
                         capture_output=True, text=True, cwd=REPO)
assert kuerzen.returncode == 0, kuerzen.stderr[-2000:]
print(kuerzen.stdout.strip().splitlines()[-1])
