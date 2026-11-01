#!/usr/bin/env python3
"""CI-Grundstufe (D09): schnelle Prüfungen, die auch unter Linux verlässlich gelten.

Aufruf aus `01_Repository/Glide`:
    python3 -B tests/tools/ci_grundstufe.py [--protokoll ORDNER] [--lieferstand-streng]

Läuft in GitHub Actions bei Push auf `main`, `claude/**` und `codex/**`, bei Pull Requests
auf `main` sowie lokal. Nutzt die Prüfungen aus `pruefen.py`, statt sie zu
duplizieren:

1. Vorprüfungen: Syntax, Versionskonsistenz, Dokumentationsindex mit Links, Fixtures.
2. Werkzeugtests (`tests/tools/test_*.py`) und Tk-freie Fachlogik (`tests/unit`),
   diese zusätzlich ohne Systemzeitzonen wie unter Windows.
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
   (`/Users/<Name>/`, `C:\\Users\\<Name>`, `/home/<Name>/`, auch JSON-maskiert).
   Das Repository ist öffentlich; Rohprotokolle bleiben deshalb seit
   01.10.2026 lokal.
8. Ablagegröße (`ablagegroesse.py`): keine Archivkopien von Glide-Daten,
   keine `*.fetch`-Reste, Archive und Nachweise nur der sieben neuesten
   Versionen, Fensterbilder nur der drei neuesten, keine Datei über 50 MB.
9. Synchronisation (`synchronisationswaechter.py`, seit 08.10.2026): keine
   Konfliktkopien `<Name>-<Gerätename>` neben ihrem Original und kein
   Hauptdokument, das ohne Vermerk mehr als 40 % seiner Zeilen verliert.

Die Integrationssuiten gehören nicht zu dieser Grundstufe. GitHub Actions
führt anschließend die vollständige sachlich ausführbare Linux-Matrix und
danach die native Windows-Vollprüfung verpflichtend aus (D35/D42/D44).
Kalibrierte Linux-Erwartungen brauchen passende Defekt-Gegenproben; native
Sicht- und Screenreaderabnahmen bleiben eigene Tore. Die Vollprüfung ersetzt
diese Grundstufe nicht.

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
import ablagegroesse  # noqa: E402
import synchronisationswaechter  # noqa: E402
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
# Auch JSON-maskiert (`\/Users\/<Name>\/`): So schreibt etwa Swifts JSONEncoder
# Pfade; ein solcher Fund rutschte bis 03.10.2026 durch.
BENUTZERPFAD = re.compile(
    r"\\?/Users\\?/([A-Za-z0-9._-]+)\\?/|[A-Za-z]:(?:\\\\|\\)Users(?:\\\\|\\)([A-Za-z0-9._-]+)"
    r"|\\?/home\\?/([a-z][a-z0-9._-]*)\\?/")
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


def lieferstand_pruefen(streng=False):
    differences = lieferstand_abweichungen()
    if not differences:
        return "ausgeführt", "07_Python-Versionen ist bytegleich zu src/glide"
    message = (f"{len(differences)} Abweichungen zwischen src/glide und 07_Python-Versionen: "
               + ", ".join(differences[:8]) + (" …" if len(differences) > 8 else ""))
    return (("fehlgeschlagen", message) if streng else ("Hinweis", message
            + " – zulässig zwischen Prüfkandidat und Auslieferung (abgleich_07.py)"))


def datenschutz_pruefen():
    findings = benutzerpfade()
    if findings is None:
        return "Hinweis", "kein Git-Arbeitsstand; versionierte Dateien nicht ermittelbar"
    if findings:
        return "fehlgeschlagen", (f"{len(findings)} versionierte Dateien mit Benutzerpfad: "
            + ", ".join(f"{name} ({match})" for name, match in findings[:5])
            + ". Pfade durch ~ bzw. %USERPROFILE% ersetzen; Rohprotokolle nicht versionieren")
    return "ausgeführt", "keine Benutzerpfade in versionierten Textdateien"


def ablage_pruefen():
    entries = ablagegroesse.versionierte_dateien()
    if entries is None:
        return "Hinweis", "kein Git-Arbeitsstand; versionierte Dateien nicht ermittelbar"
    findings = ablagegroesse.befunde(entries, ablagegroesse.aktuelle_version())
    return ("fehlgeschlagen" if findings else "ausgeführt"), ablagegroesse.zusammenfassung(entries, findings)


def synchronisation_pruefen():
    result = synchronisationswaechter.arbeitsstand_pruefen(ABLAGE)
    if result is None:
        return "Hinweis", "kein Git-Arbeitsstand; Dateien nicht ermittelbar"
    copies, reduced = result
    findings = ([f"Konfliktkopie {copy} neben {original}" for copy, original in copies]
                + [f"{path}: {before} → {after} Zeilen ohne Vermerk" for path, before, after in reduced])
    message = (("; ".join(findings[:6]) + (" …" if len(findings) > 6 else "")) if findings else
               "keine Synchronisationskopien, kein Hauptdokument ohne Vermerk stark gekürzt")
    return ("fehlgeschlagen" if findings else "ausgeführt"), message


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--protokoll", type=Path, help="Ordner für Logs und ergebnis.json")
    parser.add_argument("--timeout", type=int, default=600, help="Zeitlimit je Schritt in Sekunden")
    parser.add_argument("--arbeitsablage", type=Path, help="Kurze lokale Prüfablage außerhalb OneDrive/System-Temp")
    parser.add_argument("--lieferstand-streng", action="store_true",
                        help="Abweichungen zwischen src/glide und 07_Python-Versionen als Fehler werten")
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout muss positiv sein")
    guard = pruefen.Pruefablauf(REPO, args.arbeitsablage)
    logdir = args.protokoll.expanduser().resolve() if args.protokoll else guard.root / "protokoll"
    run = pruefen.Prueflauf(logdir, args.timeout, waechter=guard)
    print(f"Glide-CI-Grundstufe · Python {sys.version.split()[0]} · {sys.platform}", flush=True)
    print(f"Dauerhafter WA-42-Nachweis: {guard.root}", flush=True)

    run.funktion("Syntax", pruefen.syntax_pruefen)
    run.funktion("Versionskonsistenz", pruefen.versionen_pruefen)
    run.funktion("Dokumentation", pruefen.dokumentation_pruefen)
    run.funktion("Fixtures", pruefen.fixtures_pruefen)
    run.prozess("Werkzeugtests", [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(REPO / "tests/tools"),
                                  "-p", "test_*.py"])
    run.prozess("Fachlogik-Unit-Tests", [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(REPO / "tests/unit")])
    # Zusätzlich die Windows-Situation ohne System-IANA-Daten nachstellen.
    run.prozess("Fachlogik ohne Systemzeitzonen", [sys.executable, "-B", "-m", "unittest", "discover", "-s",
                                                   str(REPO / "tests/unit")], umgebung={"PYTHONTZPATH": ""})
    for name in pruefen.ANALYSEN:
        run.prozess(Path(name).stem, [sys.executable, "-B", str(REPO / "tests/tools" / name)])
    run.gui_pruefen()
    if guard.stopped:
        run.meldung("Startprobe", "übersprungen", "Prüffolge nach Fehler/Integritätsbefund gestoppt")
    elif run.gui_problem:
        run.meldung("Startprobe", "fehlgeschlagen", f"nicht ausführbar: {run.gui_problem}")
    else:
        run.prozess("Startprobe", [sys.executable, "-B", "-c", STARTPROBE], gui=True)
    for name, action in (("Lieferstand", lambda: lieferstand_pruefen(args.lieferstand_streng)),
                         ("Fremdcode", fremdcode_pruefen), ("Datenschutz", datenschutz_pruefen),
                         ("Ablagegröße", ablage_pruefen), ("Synchronisation", synchronisation_pruefen)):
        run.funktion(name, action)
        if run.results[-1]["status"] == "Hinweis" and os.environ.get("GITHUB_ACTIONS"):
            print(f"::warning title={name}::{run.results[-1]['grund']}", flush=True)
    failed = [row['schritt'] for row in run.results if row['status'] == 'fehlgeschlagen']
    exitcode = int(bool(failed or guard.stopped))
    logdir.mkdir(parents=True, exist_ok=True)
    (logdir / "ergebnis.json").write_text(json.dumps({
        "zeitpunkt": datetime.now().isoformat(timespec="seconds"), "stufe": "CI-Grundstufe",
        "python": sys.version, "plattform": sys.platform, "exitcode": exitcode,
        "pruefablauf": str(guard.root / "pruefablauf.json"), "schritte": run.results},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print("Ergebnis: " + (f"FEHLGESCHLAGEN ({', '.join(failed)})" if exitcode else
          "CI-Grundstufe bestanden; Vollprüfung auf dem Referenz-Mac bleibt maßgeblich"), flush=True)
    return exitcode


if __name__ == "__main__":
    raise SystemExit(main())
