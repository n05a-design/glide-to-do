#!/usr/bin/env python3
"""Glide mit einem Aufruf prüfen; benötigt ausschließlich die Standardbibliothek.

Schnell: Syntax, Versionen, Dokumentverweise, Fixtures, alle Integrationssuiten und zwei Analysen.
Voll: zusätzlich Beispiel-/Releasedaten erneut erzeugen/vergleichen und Bilder erzeugen.
Eine tatsächliche Sichtprüfung bleibt eine ausdrücklich benannte manuelle Aufgabe.
"""

from __future__ import annotations

import argparse
import ast
from datetime import date, datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile

REPO = Path(__file__).resolve().parents[2]
APP = REPO / "src/glide/app.pyw"
SUITEN = ("test_glide.py", "test_datenintegritaet.py", "audit_app.py",
          "test_dialog_theme.py", "test_ui_updates.py", "test_glide_36.py", "test_release36.py", "test_ui_polish36.py",
          "test_ui_followup36.py", "test_release37.py", "test_template_workflows.py", "test_reminders.py", "test_ui39.py", "test_workspace310.py", "test_features311.py", "test_features312.py", "test_features313.py", "test_features314.py", "test_features315.py", "test_features316.py", "test_features317.py", "test_features318.py", "test_features319.py", "test_features320.py", "test_features321.py")
# standpruefung.py ist seit 3.21.3 dabei: Sieben Dokumente standen zwei
# Versionssprünge lang auf 3.21.0, weil nichts die Standzeilen gegen VERSION
# geprüft hat. Index- und Linkprüfung finden das nicht – ein Dokument kann
# vollständig verlinkt und dennoch inhaltlich überholt sein.
ANALYSEN = ("analyse_statisch.py", "analyse_erreichbarkeit.py", "standpruefung.py")


def quelltext(path):
    return path.read_text(encoding="utf-8-sig")


def konstanten(tree):
    result = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    result[target.id] = node.value.value
    return result


def syntax_pruefen():
    files = sorted(set(REPO.glob("src/**/*.py")) | set(REPO.glob("src/**/*.pyw"))
                   | set(REPO.glob("tests/**/*.py")))
    for path in files:
        if "archiv" not in path.parts and "__pycache__" not in path.parts:
            ast.parse(quelltext(path), filename=str(path))
    return f"{len(files)} Python-Quelldateien gelesen; keine Bytecode-Dateien erzeugt"


def versionen_pruefen():
    version = quelltext(REPO / "VERSION").strip()
    values = konstanten(ast.parse(quelltext(APP)))
    if values.get("APP_VERSION") != version:
        raise ValueError("VERSION und APP_VERSION stimmen nicht überein")
    test = ast.parse(quelltext(REPO / "tests/integration/test_glide.py"))
    expected = []
    for node in ast.walk(test):
        if isinstance(node, ast.Assert) and isinstance(node.test, ast.Compare):
            comparison = node.test
            if (isinstance(comparison.left, ast.Attribute)
                    and comparison.left.attr == "APP_VERSION"
                    and len(comparison.ops) == 1 and isinstance(comparison.ops[0], ast.Eq)
                    and isinstance(comparison.comparators[0], ast.Constant)):
                expected.append(comparison.comparators[0].value)
    if expected != [version]:
        raise ValueError(f"Versionsprüfung der Hauptsuite: {expected!r}, erwartet {version}")
    changelog = re.search(r"(?m)^##\s+\[?(\d+\.\d+\.\d+)", quelltext(REPO / "CHANGELOG.md"))
    if not changelog or changelog.group(1) != version:
        raise ValueError("Oberster nummerierter CHANGELOG-Eintrag passt nicht zu VERSION")
    return f"VERSION, App, Hauptsuite und CHANGELOG: {version}; Datenformat {values['DATA_SCHEMA_VERSION']}"


def dokumentation_pruefen():
    index = quelltext(REPO / "docs/00_INDEX.md")
    missing = []
    checked = 0
    for path in sorted((REPO / "docs").rglob("*.md")):
        relative = path.relative_to(REPO / "docs").as_posix()
        if path.name != "00_INDEX.md" and relative not in index:
            missing.append(f"Im Dokumentationsindex fehlt: {relative}")
        if "archiv" in path.parts:
            continue
        # Markdown-Dateilinks prüfen; Fließtext, Codebeispiele, Weblinks und
        # bewusst historische Aussagen sind keine maschinell sicheren Pfadangaben.
        text = re.sub(r"```.*?```", "", quelltext(path), flags=re.S)
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = target.strip().strip("<>").split(' "', 1)[0]
            if not target or urlsplit(target).scheme or target.startswith("#"):
                continue
            target = unquote(target.split("#", 1)[0])
            checked += 1
            if not (path.parent / target).exists():
                missing.append(f"{relative}: fehlendes Linkziel {target}")
    if missing:
        raise ValueError("; ".join(missing))
    return f"Alle Dokumente einschließlich Archiv im Index; {checked} lokale Markdown-Dateilinks aktueller Dokumente geprüft. Inhaltliche Prüfung bleibt manuell."


def backup_lesen(path):
    with zipfile.ZipFile(path) as archive:
        if archive.testzip():
            raise ValueError(f"Beschädigte ZIP-Datei: {path.name}")
        return json.loads(archive.read("data.json"))


def fixtures_pruefen():
    values = konstanten(ast.parse(quelltext(APP)))
    count = 0
    for path in sorted((REPO / "tests/fixtures").rglob("*.glidebackup")):
        if "archiv" in path.parts:
            continue
        payload = backup_lesen(path)
        versioned_name = re.fullmatch(r"glide_releaseplanung_(\d+\.\d+\.\d+)\.glidebackup", path.name)
        expected_version = versioned_name.group(1) if versioned_name else values["APP_VERSION"]
        version_tuple = tuple(map(int, expected_version.split(".")))
        expected_schema = (11 if versioned_name and version_tuple <= (3, 6, 0) else
                           12 if versioned_name and version_tuple == (3, 7, 0) else
                           13 if versioned_name and version_tuple <= (3, 13, 0) else
                           14 if versioned_name and version_tuple <= (3, 18, 0) else
                           values["DATA_SCHEMA_VERSION"])
        if payload.get("version") != expected_schema:
            raise ValueError(f"{path.name}: Datenformat passt nicht zur Erzeugerversion")
        if payload.get("app_version") != expected_version:
            raise ValueError(f"{path.name}: Erzeugerversion stimmt nicht mit der App überein")
        count += 1
    for schema in range(4, values["DATA_SCHEMA_VERSION"] + 1):
        path = REPO / f"tests/fixtures/current_v{schema}/reference_v{schema}.json"
        if not path.is_file() or json.loads(quelltext(path)).get("version") != schema:
            raise ValueError(f"Fehlendes oder falsch versioniertes Referenz-Fixture: {path.name}")
    if not (REPO / "tests/fixtures/legacy_v2/probelisten_5_listen_v2.json").is_file():
        raise ValueError("Das historische Format-2-Fixture fehlt")
    return f"{count} aktuelle bzw. explizit versionierte Backups und alle historischen Referenzformate vorhanden; echte Importprüfung folgt in der Hauptsuite"


def inhalt_normalisieren(payload, relative_fristen=True):
    """Zufällige IDs/Zeitstempel ausblenden; relative Fristen und Inhalt bewahren."""
    identities = {}

    def collect(value):
        if isinstance(value, dict):
            if isinstance(value.get("id"), str):
                identities.setdefault(value["id"], f"id-{len(identities)}")
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(payload)
    origin = date.fromisoformat(payload["exported_at"][:10])

    def verlauf_bereinigen(eintraege):
        """Änderungsverlauf ohne seine Uhrzeiten vergleichen.

        Der Verlauf aus 3.19 entsteht beim Speichern und trägt den echten
        Zeitpunkt in ``at``. Der ist so unreproduzierbar wie ``exported_at``
        und muss deshalb genauso draußen bleiben – sonst kann dieser
        Abgleich niemals gleich ausfallen. Art, Aktion, Ziel, Liste und
        Anzahl bleiben Inhalt und werden weiterhin verglichen.
        """
        if not isinstance(eintraege, list):
            return clean(eintraege, "history")
        return [{k: clean(v, k) for k, v in eintrag.items() if k != "at"}
                if isinstance(eintrag, dict) else clean(eintrag)
                for eintrag in eintraege]

    def clean(value, key=None):
        if isinstance(value, dict):
            return {k: (verlauf_bereinigen(v) if k == "history" else clean(v, k))
                    for k, v in value.items()
                    if k not in ("exported_at", "deleted_at", "added_at")}
        if isinstance(value, list):
            return [clean(child) for child in value]
        if isinstance(value, str):
            if relative_fristen and key in ("due", "planned_date", "start", "ende") and value:
                return (date.fromisoformat(value) - origin).days
            if key == "storage":
                for old, new in identities.items():
                    value = value.replace(old, new)
            return identities.get(value, value)
        return value

    return clean(payload)


class Prueflauf:
    def __init__(self, logdir, timeout):
        self.results = []
        self.logdir = logdir
        self.timeout = timeout
        self.gui_prefix = []
        self.gui_problem = None
        self.env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
        # Suiten laufen absichtlich in einer Zone mit Versatz, wenn der
        # Aufrufer keine vorgibt. In UTC ist jeder Zeitzonenfehler unsichtbar,
        # weil der Versatz null ist: Der UNTIL-Fehler aus 3.21.0 war in einer
        # UTC-Vorabumgebung grün und fiel erst im macOS-Lauf auf. Ein
        # gesetztes TZ der Umgebung bleibt unangetastet, damit sich jede Zone
        # gezielt nachstellen lässt.
        self.env.setdefault("TZ", "Europe/Berlin")
        if logdir:
            logdir.mkdir(parents=True, exist_ok=True)

    def meldung(self, name, state, reason):
        self.results.append({"schritt": name, "status": state, "grund": reason})
        print(f"[{state}] {name}: {reason}", flush=True)

    def funktion(self, name, action):
        try:
            reason = action()
        except (OSError, ValueError, SyntaxError, KeyError, zipfile.BadZipFile) as exc:
            self.meldung(name, "fehlgeschlagen", str(exc))
        else:
            self.meldung(name, "ausgeführt", reason)

    def prozess(self, name, command, gui=False):
        if gui and self.gui_problem:
            self.meldung(name, "übersprungen", self.gui_problem)
            return False
        try:
            result = subprocess.run((self.gui_prefix if gui else []) + command,
                                    cwd=REPO, env=self.env, capture_output=True,
                                    text=True, encoding="utf-8", errors="replace",
                                    timeout=self.timeout)
        except (OSError, subprocess.TimeoutExpired) as exc:
            self.meldung(name, "fehlgeschlagen", str(exc))
            return False
        output = result.stdout + result.stderr
        if self.logdir:
            (self.logdir / f"{name}.log").write_text(output, encoding="utf-8")
        # Frühere Auditfassungen konnten Befunde trotz Exitcode 0 melden.
        has_findings = name == "audit_app" and re.search(r"(?m)^BEFUNDE\s*\([1-9]\d*\)", output)
        ok = result.returncode == 0 and not has_findings
        if not ok:
            print(output[-8000:], flush=True)
        elif not self.logdir:
            print(output.rstrip(), flush=True)
        self.meldung(name, "ausgeführt" if ok else "fehlgeschlagen",
                     f"Exitcode {result.returncode}" + ("; Audit meldet Befunde" if has_findings else ""))
        return ok

    def gui_pruefen(self):
        if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
            executable = shutil.which("xvfb-run")
            if executable:
                self.gui_prefix = [executable, "-a", "--server-args=-screen 0 1400x1100x24"]
            else:
                self.gui_problem = "Kein DISPLAY und xvfb-run nicht vorhanden"
        if not self.gui_problem:
            try:
                result = subprocess.run(self.gui_prefix + [sys.executable, "-c",
                    "import tkinter as tk; r=tk.Tk(); r.withdraw(); r.update(); print(r.tk.call('info','patchlevel')); r.destroy()"],
                    env=self.env, capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=30)
                if result.returncode:
                    self.gui_problem = "Tk nicht betriebsbereit: " + (result.stderr.strip().splitlines()[-1] if result.stderr else str(result.returncode))
            except (OSError, subprocess.TimeoutExpired) as exc:
                self.gui_problem = str(exc)
        self.meldung("Tk-Voraussetzung", "übersprungen" if self.gui_problem else "ausgeführt",
                     self.gui_problem or "Tk-Fenster im gewählten Python gestartet und geschlossen")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modus", choices=("schnell", "voll"), default="schnell")
    parser.add_argument("--protokoll", type=Path, help="Ordner für vollständige Logs und ergebnis.json")
    parser.add_argument("--screenshots", type=Path, help="Bildordner im Vollmodus; Standard: Protokollordner/screenshots")
    parser.add_argument("--timeout", type=int, default=300, help="Zeitlimit je Suite/Werkzeug in Sekunden")
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout muss positiv sein")
    logdir = args.protokoll.expanduser().resolve() if args.protokoll else None
    run = Prueflauf(logdir, args.timeout)
    print(f"Glide-Prüflauf ({args.modus}) · Python {sys.version.split()[0]} · {sys.platform}", flush=True)
    run.funktion("Syntax", syntax_pruefen)
    run.funktion("Versionskonsistenz", versionen_pruefen)
    run.funktion("Dokumentation", dokumentation_pruefen)
    run.funktion("Fixtures", fixtures_pruefen)
    run.gui_pruefen()
    for name in SUITEN:
        run.prozess(Path(name).stem, [sys.executable, str(REPO / "tests/integration" / name)], gui=True)
    for name in ANALYSEN:
        run.prozess(Path(name).stem, [sys.executable, str(REPO / "tests/tools" / name)])
    if args.modus == "voll":
        target = args.screenshots or (logdir / "screenshots" if logdir else None)
        with tempfile.TemporaryDirectory(prefix="glide-reproduktion-") as tempdir:
            generated = Path(tempdir) / "beispieldaten.glidebackup"
            if run.prozess("Beispieldaten-erzeugen", [sys.executable, str(REPO / "tests/tools/beispieldaten.py"), "--ziel", str(generated)], gui=True):
                def vergleichen():
                    original = REPO / "tests/fixtures/beispiele/Glide_Beispieldaten.glidebackup"
                    if inhalt_normalisieren(backup_lesen(original)) != inhalt_normalisieren(backup_lesen(generated)):
                        raise ValueError("Beispieldaten unterscheiden sich vom Erzeuger; Fixture gezielt neu erzeugen und prüfen")
                    return "Inhalt, Verknüpfungen und relative Fristen gleich; IDs und Erzeugungszeit sind ausgenommen"
                run.funktion("Beispieldaten-Abgleich", vergleichen)
            # Der Planungsstichtag ist Bestandteil des Release-Inhalts. Anders
            # als bei allgemeinen Beispielen muss genau dieser Tag wieder gelten.
            version = quelltext(REPO / "VERSION").strip()
            release_path = REPO / f"tests/fixtures/beispiele/glide_releaseplanung_{version}.glidebackup"
            try:
                release_payload = backup_lesen(release_path)
                notes = "\n".join(str(entry.get("note", "")) for entry in release_payload.get("lists", []))
                dates = set(re.findall(r"Planungsstichtag (\d{4}-\d{2}-\d{2})", notes))
                if len(dates) != 1:
                    raise ValueError("Release-Fixture enthält keinen eindeutigen Planungsstichtag")
                stichtag = dates.pop()
                date.fromisoformat(stichtag)
            except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
                run.meldung("Release-Reproduktion", "fehlgeschlagen", str(exc))
            else:
                release_generated = Path(tempdir) / "release.glidebackup"
                command = [sys.executable, str(REPO / "tests/tools/releasedaten.py"),
                           "--ziel", str(release_generated), "--stichtag", stichtag]
                if run.prozess("Release-erzeugen", command, gui=True):
                    def release_vergleichen():
                        if inhalt_normalisieren(release_payload, False) != inhalt_normalisieren(backup_lesen(release_generated), False):
                            raise ValueError("Release-Fixture unterscheidet sich bei gleichem Planungsstichtag vom Erzeuger")
                        return f"Inhalt, Fristen und Verknüpfungen zum Planungsstichtag {stichtag} gleich"
                    run.funktion("Release-Abgleich", release_vergleichen)
                    if sys.platform == "win32" and target:
                        run.prozess("Screenshots", command + ["--screenshot", str(target.resolve() / "release_hell.png")], gui=True)
        reason = ("Release-Erzeugung nicht erfolgreich; keine Windows-Aufnahme möglich" if sys.platform == "win32" and target else
                  "Kein Bildziel: --screenshots oder --protokoll angeben" if sys.platform == "win32" else
                  "screenshots.py unterstützt nur Linux/X11; releasedaten.py zusätzlich Windows" if not sys.platform.startswith("linux") else
                  "ImageMagick import fehlt" if not shutil.which("import") else
                  "Kein dauerhafter Bildordner: --screenshots oder --protokoll angeben" if not target else None)
        if reason:
            if not any(row["schritt"] == "Screenshots" for row in run.results):
                run.meldung("Screenshots", "übersprungen", reason)
        else:
            run.prozess("Screenshots", [sys.executable, str(REPO / "tests/tools/screenshots.py"), "--out", str(target.resolve())], gui=True)
    else:
        run.meldung("Beispieldaten-Reproduktion", "übersprungen", "Schnellmodus; für Erzeugerabgleich --modus voll verwenden")
        run.meldung("Screenshots", "übersprungen", "Schnellmodus; für Bilder --modus voll verwenden")
    run.meldung("Sichtprüfung", "übersprungen", "Bilder müssen von einer Person angesehen werden; native Plattformprüfung bleibt offen")
    failed = any(row["status"] == "fehlgeschlagen" for row in run.results)
    exitcode = 1 if failed else 2 if run.gui_problem else 0
    if logdir:
        (logdir / "ergebnis.json").write_text(json.dumps({"zeitpunkt": datetime.now().isoformat(timespec="seconds"),
            "modus": args.modus, "python": sys.version, "plattform": sys.platform,
            "exitcode": exitcode, "schritte": run.results}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Ergebnis: {'FEHLGESCHLAGEN' if exitcode == 1 else 'UNVOLLSTÄNDIG' if exitcode == 2 else 'automatisierte Prüfungen erfolgreich'}; manuelle Restprüfung siehe oben.", flush=True)
    return exitcode


if __name__ == "__main__":
    raise SystemExit(main())
