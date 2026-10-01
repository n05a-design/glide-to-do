#!/usr/bin/env python3
"""CI-Grundstufe (D09): schnelle Prüfungen, die auch unter Linux verlässlich gelten.

Aufruf aus `01_Repository/Glide`:
    python3 -B tests/tools/ci_grundstufe.py [--protokoll ORDNER] [--lieferstand-streng]

Läuft in GitHub Actions bei jedem Push und Pull Request auf `main` und lokal
mit demselben Ergebnis. Nutzt die Prüfungen aus `pruefen.py`, statt sie zu
duplizieren:

1. Vorprüfungen: Syntax, Versionskonsistenz, Dokumentationsindex mit Links, Fixtures.
2. Werkzeugtests (`test_standpruefung.py`) und Tk-freie Fachlogik (`tests/unit`).
3. Die fünf Analysen, darunter `standpruefung.py`.
4. Startprobe: Glide startet mit temporärem `GLIDE_DATA_DIR` unter Tk (ohne
   Bildschirm über `xvfb-run`) und wechselt durch sechs Ansichten, ohne
   Callbackfehler und ohne Eintrag im Fehlerprotokoll.
5. Lieferstand: `src/glide` gegen `07_Python-Versionen` per SHA-256. Zwischen
   Prüfkandidat und Auslieferung nur ein Hinweis; mit `--lieferstand-streng`
   ein Fehler.
6. Fremdcode: Jede Datei unter `src/glide/vendor` muss bytegleich zum
   Originalpaket sein, dessen Quelle und SHA-256 `vendor/provenance.json`
   festhält. Das Paket wird von PyPI geladen; ohne Netz nur ein Hinweis.
7. Datenschutz: Keine versionierte Textdatei enthält einen Benutzerpfad
   (`/Users/<Name>/`, `C:\\Users\\<Name>`, `/home/<Name>/`). Das Repository ist
   öffentlich; Rohprotokolle bleiben deshalb seit 01.10.2026 lokal.

Die Integrationssuiten sind auf den Referenz-Mac abgestimmt und gehören nicht
dazu; unter Linux laufen sie über `pruefen.py --modus schnell` (in GitHub
Actions als manuell startbarer Job). Die Vollprüfung ersetzt diese Stufe nicht.

Exitcode 0: alle Schritte bestanden. Exitcode 1: mindestens ein Schritt
fehlgeschlagen oder die Startprobe war nicht ausführbar.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.request
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pruefen  # noqa: E402

REPO = pruefen.REPO
ABLAGE = REPO.parents[1]

STARTPROBE = r'''
import importlib.machinery, importlib.util, os, sys, tempfile
daten = tempfile.mkdtemp(prefix="glide-ci-")
os.environ["GLIDE_DATA_DIR"] = daten
os.environ["GLIDE_TEST_MODE"] = "1"
sys.dont_write_bytecode = True
code = os.path.join(os.getcwd(), "src", "glide")
sys.path.insert(0, code)
loader = importlib.machinery.SourceFileLoader("glide_app", os.path.join(code, "app.pyw"))
mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
sys.modules[loader.name] = mod
loader.exec_module(mod)
root = mod.tk.Tk()
root.geometry("1280x840+0+0")
fehler = []
root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
app = mod.ListApp(root)
root.update()
ansichten = ("set_home_view", "set_today_view", "set_table_view", "set_library_view", "set_pages_view")
for name in ansichten:
    getattr(app, name)()
    root.update()
app.set_active_list(app.lists[0]["id"])
root.update()
pfad = os.path.join(daten, "fehlerprotokoll.txt")
protokoll = open(pfad, encoding="utf-8", errors="replace").read() if os.path.exists(pfad) else ""
tk_stand = root.tk.call("info", "patchlevel")
root.destroy()
if fehler or protokoll.strip():
    print("Callbackfehler:", fehler)
    print(protokoll[-4000:])
    sys.exit(1)
print(f"Glide {mod.APP_VERSION} mit Tk {tk_stand} gestartet; {len(ansichten) + 1} Ansichten ohne Callbackfehler")
'''


def sha256(pfad):
    return hashlib.sha256(pfad.read_bytes()).hexdigest()


def lieferstand_abweichungen():
    """Dateien in 07_Python-Versionen, die nicht bytegleich zu src/glide sind.

    Dieselbe Zuordnung wie `scripts/pflege/abgleich_07.py`, aber nur lesend:
    Hauptdatei mit Versionsnummer, Schnellstart, alle Module und die Ordner
    `resources` und `vendor` ohne Archive.
    """
    quelle = REPO / "src/glide"
    ziel = ABLAGE / "07_Python-Versionen"
    version = (REPO / "VERSION").read_text(encoding="utf-8").strip()
    zuordnung = {"app.pyw": f"Glide-Aufgaben-und-Listen_v{version}.pyw", "glide_start.py": "Schnellstart.pyw"}
    zuordnung.update({modul.name: modul.name for modul in sorted(quelle.glob("*.py")) if modul.name != "glide_start.py"})
    abweichungen = [name for herkunft, name in zuordnung.items()
                    if not (ziel / name).is_file() or sha256(quelle / herkunft) != sha256(ziel / name)]
    for ordner in ("resources", "vendor"):
        for datei in sorted((quelle / ordner).rglob("*")):
            if datei.is_dir() or "__pycache__" in datei.parts or "archiv" in datei.parts:
                continue
            gegenstueck = ziel / datei.relative_to(quelle)
            if not gegenstueck.is_file() or sha256(gegenstueck) != sha256(datei):
                abweichungen.append(str(datei.relative_to(quelle)))
    return abweichungen


# Benutzerpfade verraten Konten- und Personennamen. Platzhalter und die
# Konten der CI-Umgebungen sind erlaubt.
BENUTZERPFAD = re.compile(
    r"/Users/([A-Za-z0-9._-]+)/|[A-Za-z]:(?:\\\\|\\)Users(?:\\\\|\\)([A-Za-z0-9._-]+)|/home/([a-z][a-z0-9._-]*)/")
ERLAUBTE_KONTEN = {"shared", "public", "name", "username", "user", "benutzer", "nutzer", "example", "runner"}
BINAERFORMATE = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".icns", ".ico", ".pdf", ".zip", ".whl",
                 ".glidebackup", ".glideapp", ".lib", ".avif", ".so", ".dll", ".dylib", ".ttf", ".otf", ".docx",
                 ".xlsx", ".afdesign", ".dmg", ".gz"}


def benutzerpfade():
    """Versionierte Textdateien mit Benutzerpfad: Liste von (Datei, Fundstelle)."""
    try:
        dateien = subprocess.run(["git", "ls-files", "-z"], cwd=ABLAGE, capture_output=True,
                                 check=True).stdout.split(b"\0")
    except (OSError, subprocess.CalledProcessError):
        return None
    funde = []
    for roh in filter(None, dateien):
        pfad = ABLAGE / roh.decode("utf-8", "surrogateescape")
        if pfad.suffix.lower() in BINAERFORMATE:
            continue
        try:
            inhalt = pfad.read_bytes()
        except OSError:
            continue
        if b"\0" in inhalt[:8192]:
            continue
        text = inhalt.decode("utf-8", "replace")
        for treffer in BENUTZERPFAD.finditer(text):
            konto = next(gruppe for gruppe in treffer.groups() if gruppe)
            if konto.lower() not in ERLAUBTE_KONTEN:
                funde.append((roh.decode("utf-8", "replace"), treffer.group(0)))
                break
    return funde


def fremdcode_pruefen():
    """Vendor-Dateien gegen das in provenance.json festgehaltene Originalpaket.

    Liefert (Status, Text). Netzfehler sind ein Hinweis, Abweichungen ein Fehler.
    """
    vendor = REPO / "src/glide/vendor"
    herkunft = json.loads((vendor / "provenance.json").read_text(encoding="utf-8"))
    berichte = []
    for paket, angaben in herkunft.items():
        try:
            info = json.load(urllib.request.urlopen(
                f"https://pypi.org/pypi/{paket}/{angaben['version']}/json", timeout=60))
            datei = next(eintrag for eintrag in info["urls"] if eintrag["filename"] == angaben["file"])
            daten = urllib.request.urlopen(datei["url"], timeout=120).read()
        except (OSError, ValueError, KeyError, StopIteration) as exc:
            return "Hinweis", f"{paket}: Originalpaket nicht abrufbar ({exc}); Prüfung ohne Netz nicht möglich"
        summe = hashlib.sha256(daten).hexdigest()
        if summe != angaben["sha256"] or summe != datei["digests"]["sha256"]:
            return "fehlgeschlagen", f"{paket}: SHA-256 des Pakets weicht von provenance.json bzw. PyPI ab"
        archiv = zipfile.ZipFile(io.BytesIO(daten))
        namen = archiv.namelist()
        lokal = vendor / paket
        abweichend, fehlend = [], []
        for eintrag in namen:
            if eintrag.startswith(f"{paket}/") and not eintrag.endswith("/"):
                ziel = lokal / eintrag[len(paket) + 1:]
                if not ziel.is_file():
                    fehlend.append(eintrag)
                elif ziel.read_bytes() != archiv.read(eintrag):
                    abweichend.append(eintrag)
        for datei_lokal in sorted(lokal.rglob("*")):
            if not datei_lokal.is_file() or "__pycache__" in datei_lokal.parts:
                continue
            relativ = datei_lokal.relative_to(lokal).as_posix()
            quellen = [f"{paket}/{relativ}"] + [n for n in namen if ".dist-info/" in n and n.endswith("/" + relativ)]
            if not any(n in namen and archiv.read(n) == datei_lokal.read_bytes() for n in quellen):
                abweichend.append(f"vendor/{paket}/{relativ}")
        if abweichend or fehlend:
            return "fehlgeschlagen", (f"{paket}: {len(abweichend)} abweichend, {len(fehlend)} fehlend – "
                                      + ", ".join((abweichend + fehlend)[:6]))
        anzahl = sum(1 for d in lokal.rglob("*") if d.is_file() and "__pycache__" not in d.parts)
        berichte.append(f"{paket} {angaben['version']}: {anzahl} Dateien bytegleich zum Originalpaket (SHA-256 {summe[:12]}…)")
    return "ausgeführt", "; ".join(berichte)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--protokoll", type=Path, help="Ordner für Logs und ergebnis.json")
    parser.add_argument("--timeout", type=int, default=600, help="Zeitlimit je Schritt in Sekunden")
    parser.add_argument("--lieferstand-streng", action="store_true",
                        help="Abweichungen zwischen src/glide und 07_Python-Versionen als Fehler werten")
    args = parser.parse_args()
    logdir = args.protokoll.expanduser().resolve() if args.protokoll else None
    run = pruefen.Prueflauf(logdir, args.timeout)
    print(f"Glide-CI-Grundstufe · Python {sys.version.split()[0]} · {sys.platform}", flush=True)

    run.funktion("Syntax", pruefen.syntax_pruefen)
    run.funktion("Versionskonsistenz", pruefen.versionen_pruefen)
    run.funktion("Dokumentation", pruefen.dokumentation_pruefen)
    run.funktion("Fixtures", pruefen.fixtures_pruefen)
    run.prozess("Werkzeugtests", [sys.executable, "-B", str(REPO / "tests/tools/test_standpruefung.py")])
    run.prozess("Fachlogik-Unit-Tests", [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(REPO / "tests/unit")])
    for name in pruefen.ANALYSEN:
        run.prozess(Path(name).stem, [sys.executable, "-B", str(REPO / "tests/tools" / name)])

    run.gui_pruefen()
    if run.gui_problem:
        run.meldung("Startprobe", "fehlgeschlagen", f"nicht ausführbar: {run.gui_problem}")
    else:
        run.prozess("Startprobe", [sys.executable, "-B", "-c", STARTPROBE], gui=True)

    abweichungen = lieferstand_abweichungen()
    if not abweichungen:
        run.meldung("Lieferstand", "ausgeführt", "07_Python-Versionen ist bytegleich zu src/glide")
    else:
        text = (f"{len(abweichungen)} Abweichungen zwischen src/glide und 07_Python-Versionen: "
                + ", ".join(abweichungen[:8]) + (" …" if len(abweichungen) > 8 else ""))
        if args.lieferstand_streng:
            run.meldung("Lieferstand", "fehlgeschlagen", text)
        else:
            run.meldung("Lieferstand", "Hinweis",
                        text + " – zulässig zwischen Prüfkandidat und Auslieferung (abgleich_07.py)")
            if os.environ.get("GITHUB_ACTIONS"):
                print(f"::warning title=Lieferstand::{text}", flush=True)

    status, text = fremdcode_pruefen()
    run.meldung("Fremdcode", status, text)
    if status == "Hinweis" and os.environ.get("GITHUB_ACTIONS"):
        print(f"::warning title=Fremdcode::{text}", flush=True)

    funde = benutzerpfade()
    if funde is None:
        run.meldung("Datenschutz", "Hinweis", "kein Git-Arbeitsstand; versionierte Dateien nicht ermittelbar")
    elif funde:
        run.meldung("Datenschutz", "fehlgeschlagen",
                    f"{len(funde)} versionierte Dateien mit Benutzerpfad: "
                    + ", ".join(f"{datei} ({stelle})" for datei, stelle in funde[:5])
                    + ". Pfade durch ~ bzw. %USERPROFILE% ersetzen; Rohprotokolle nicht versionieren")
    else:
        run.meldung("Datenschutz", "ausgeführt", "keine Benutzerpfade in versionierten Textdateien")

    fehlgeschlagen = [zeile["schritt"] for zeile in run.results if zeile["status"] == "fehlgeschlagen"]
    exitcode = 1 if fehlgeschlagen else 0
    if logdir:
        logdir.mkdir(parents=True, exist_ok=True)
        (logdir / "ergebnis.json").write_text(json.dumps({
            "zeitpunkt": datetime.now().isoformat(timespec="seconds"), "stufe": "CI-Grundstufe",
            "python": sys.version, "plattform": sys.platform, "exitcode": exitcode,
            "schritte": run.results}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Ergebnis: " + (f"FEHLGESCHLAGEN ({', '.join(fehlgeschlagen)})" if fehlgeschlagen
                          else "CI-Grundstufe bestanden; Vollprüfung auf dem Referenz-Mac bleibt maßgeblich"),
          flush=True)
    return exitcode


if __name__ == "__main__":
    raise SystemExit(main())
