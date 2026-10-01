#!/usr/bin/env python3
"""Glide mit einem Aufruf prüfen; benötigt ausschließlich die Standardbibliothek.

Schnell: Syntax, Versionen, Dokumentverweise, Fixtures, Zeitzone, alle Integrationssuiten und die Analysen.
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
SUITEN = ("test_glide.py", "test_datenintegritaet.py", "test_drawing.py", "test_drawing_prototype.py", "audit_app.py",
          "test_dialog_theme.py", "test_ui_updates.py", "test_glide_36.py", "test_release36.py", "test_ui_polish36.py",
          "test_ui_followup36.py", "test_release37.py", "test_template_workflows.py", "test_reminders.py", "test_ui39.py", "test_workspace310.py", "test_features311.py", "test_features312.py", "test_features313.py", "test_features314.py", "test_features315.py", "test_features316.py", "test_features317.py", "test_features318.py", "test_features319.py", "test_features320.py", "test_features321.py", "test_features322.py", "test_features323.py", "test_features324.py", "test_features325.py", "test_features326.py", "test_features328.py", "test_features329.py", "test_drawing330.py", "test_features330.py", "test_mindestgroesse330.py", "test_kontrast330.py", "test_paketierung330.py", "test_hintergrund330.py", "test_rueckmeldung330.py", "test_seiten330.py", "test_aufraeumen330.py", "test_kompression330.py", "test_bilder330.py", "test_festlayout330.py", "test_logo330.py", "test_kartenfuss330.py", "test_speicherlast330.py", "test_notizbereich330.py", "test_befunde330.py", "test_fenster330.py", "test_tempo330.py", "test_etappe1_332.py", "test_klappmechanismen3321.py", "test_drag_performance3322.py", "test_library_performance3323.py", "test_fundament333.py", "test_bereiche3331.py", "test_vollpruefung325.py")
# standpruefung.py ist seit 3.21.3 dabei: Sieben Dokumente standen zwei
# Versionssprünge lang auf 3.21.0, weil nichts die Standzeilen gegen VERSION
# geprüft hat. Index- und Linkprüfung finden das nicht – ein Dokument kann
# vollständig verlinkt und dennoch inhaltlich überholt sein.
# attributpruefung.py ist seit 3.23.0 dabei: Der Spaltendialog öffnete sich
# zwei Versionen lang als leeres Fenster, weil eine einzige Zeile eine Methode
# der falschen Klasse rief. Tk verschluckt den AttributeError im Callback –
# sichtbar war nur ein Fenster ohne Inhalt.
# dublettenpruefung.py ist seit 3.25.0 dabei: Punkt 3 der Prüfung fragt nach
# sich wiederholenden Vorgängen. Ein Mensch findet sie in dreißigtausend Zeilen
# nicht; das Werkzeug meldet sie, bewertet aber nicht – die Entscheidung, ob
# aus einer Wiederholung ein gemeinsamer Baustein wird, bleibt eine
# Entscheidung.
ANALYSEN = ("analyse_statisch.py", "analyse_erreichbarkeit.py", "standpruefung.py",
            "attributpruefung.py", "dublettenpruefung.py")


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
                           # Format 16 kam mit 3.22.0 (Checkliste); die
                           # Releaseplanungen bis 3.21.4 tragen weiterhin 15.
                           15 if versioned_name and version_tuple <= (3, 21, 4) else
                           16 if versioned_name and version_tuple <= (3, 25, 0) else
                           # Format 17 (Notizlisten) kam mit 3.26.0, Format 18
                           # (Tagebuch) mit 3.28.0.
                           17 if versioned_name and version_tuple <= (3, 27, 0) else
                           18 if versioned_name and version_tuple <= (3, 28, 0) else
                           # Format 19 (Zeichnungsseite) mit 3.29.0, Format 20
                           # (Beziehungen, Zeit, Symbole, Archiv) mit 3.30.0.
                           19 if versioned_name and version_tuple <= (3, 29, 0) else
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
            if relative_fristen and key == "reminder" and value.get("mode") == "fixed":
                # Beispieldaten setzen feste Erinnerungen relativ zum Erzeugungstag.
                # Ortszeit erhält auch bei einem Sommerzeitwechsel den Abstand.
                moment = datetime.fromisoformat(value["at"]).astimezone()
                return {k: (((moment.date() - origin).days, moment.time().isoformat())
                            if k == "at" else clean(v, k)) for k, v in value.items()}
            # Seit 3.26 tragen Listen Erzeugungs- und Änderungszeitpunkte. Sie
            # entstehen beim Erzeugen wie `exported_at` und sind kein Inhalt.
            return {k: (verlauf_bereinigen(v) if k == "history" else clean(v, k))
                    for k, v in value.items()
                    # 3.30: `done_at` und `archived_at` entstehen ebenso beim Erzeugen.
                    if k not in ("exported_at", "deleted_at", "added_at", "created_at", "updated_at",
                                 "done_at", "archived_at")}
        if isinstance(value, list):
            return [clean(child) for child in value]
        if isinstance(value, str):
            if key == "moment_date" and value:
                # Das Momentdatum einer gewöhnlichen Liste ist ihr Anlagetag und
                # entsteht beim Erzeugen wie `exported_at`. Auch der Releaseabgleich
                # mit festem Planungsstichtag vergleicht es deshalb relativ zum
                # Exporttag – sonst scheitert er an jedem Tag nach der Erzeugung
                # (gefunden, als ein Lauf am 25./26.09.2026 über Mitternacht ging).
                return (date.fromisoformat(value) - origin).days
            if relative_fristen and key in ("due", "planned_date", "start", "ende") and value:
                return (date.fromisoformat(value) - origin).days
            if key == "storage":
                for old, new in identities.items():
                    value = value.replace(old, new)
            return identities.get(value, value)
        return value

    return clean(payload)


def kurzwert(wert, grenze=70):
    """Einen Wert so anzeigen, dass die Meldung lesbar bleibt."""
    text = repr(wert)
    return text if len(text) <= grenze else text[:grenze - 1] + "…"


def unterschiede(fixture, erzeugt, pfad="Bestand"):
    """Die Stellen benennen, an denen zwei normalisierte Bestände auseinandergehen.

    Ein Abgleich, der nur „unterscheidet sich" meldet, kostet jedes Mal
    dieselbe Suche von Hand – und der Bestand hat mehrere tausend Felder. Der
    Befund im ersten Windows-Vollprüflauf blieb aus genau diesem Grund
    unerklärt: Die Meldung nannte den Umstand, nicht die Stelle.
    """
    if type(fixture) is not type(erzeugt):
        yield f"{pfad}: {kurzwert(fixture)} statt {kurzwert(erzeugt)}"
    elif isinstance(fixture, dict):
        for schluessel in sorted(set(fixture) | set(erzeugt), key=str):
            if schluessel not in fixture:
                yield f"{pfad}.{schluessel}: fehlt im Fixture, Erzeuger hat {kurzwert(erzeugt[schluessel])}"
            elif schluessel not in erzeugt:
                yield f"{pfad}.{schluessel}: nur im Fixture, {kurzwert(fixture[schluessel])}"
            else:
                yield from unterschiede(fixture[schluessel], erzeugt[schluessel],
                                        f"{pfad}.{schluessel}")
    elif isinstance(fixture, list):
        if len(fixture) != len(erzeugt):
            yield f"{pfad}: {len(fixture)} Einträge im Fixture, {len(erzeugt)} beim Erzeuger"
        for index, (links, rechts) in enumerate(zip(fixture, erzeugt)):
            yield from unterschiede(links, rechts, f"{pfad}[{index}]")
    elif fixture != erzeugt:
        yield f"{pfad}: Fixture {kurzwert(fixture)}, Erzeuger {kurzwert(erzeugt)}"


def fundstellen(fixture, erzeugt, grenze=5):
    """Die ersten Unterschiede als ein Satz; mehr verdecken nur den Anfang."""
    gefunden = []
    for stelle in unterschiede(fixture, erzeugt):
        gefunden.append(stelle)
        if len(gefunden) >= grenze:
            gefunden.append("…weitere möglich")
            break
    return "; ".join(gefunden) if gefunden else "kein benennbarer Unterschied gefunden"


class Prueflauf:
    def __init__(self, logdir, timeout):
        self.results = []
        self.logdir = logdir
        self.timeout = timeout
        self.gui_prefix = []
        self.gui_problem = None
        self.zone_problem = None
        self.env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
        # Suiten laufen absichtlich in einer Zone mit Versatz, wenn der
        # Aufrufer keine vorgibt. In UTC ist jeder Zeitzonenfehler unsichtbar,
        # weil der Versatz null ist: Der UNTIL-Fehler aus 3.21.0 war in einer
        # UTC-Vorabumgebung grün und fiel erst im macOS-Lauf auf. Ein
        # gesetztes TZ der Umgebung bleibt unangetastet, damit sich jede Zone
        # gezielt nachstellen lässt.
        #
        # Unter Windows richtet diese Zuweisung Schaden an, statt zu helfen:
        # Die dortige Laufzeit kennt das IANA-Format nicht und liest aus
        # ``Europe/Berlin`` eine erfundene Zone ohne Sommerzeitregel – im
        # ersten Windows-Lauf meldete sie sich als „ope" mit +01:00, während in
        # Berlin an diesem Tag +02:00 galt. Jede Umrechnung in Ortszeit lag
        # damit eine Stunde daneben, und der Beispieldaten-Abgleich, der feste
        # Erinnerungen über die Ortszeit vergleicht, konnte nicht gleich
        # ausfallen. Die Systemzeitzone ist dort die verlässliche Quelle.
        if sys.platform != "win32":
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
                result = subprocess.run(self.gui_prefix + [sys.executable, "-B", str(REPO / "tests/tools/pruefe_tk.py")],
                    env=self.env, capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=30)
                if result.returncode:
                    self.gui_problem = "Tk nicht betriebsbereit: " + (result.stderr.strip().splitlines()[-1] if result.stderr else str(result.returncode))
            except (OSError, subprocess.TimeoutExpired) as exc:
                self.gui_problem = str(exc)
        self.meldung("Tk-Voraussetzung", "übersprungen" if self.gui_problem else "ausgeführt",
                     self.gui_problem or "Tk-Fenster im gewählten Python gestartet und geschlossen")

    def zone_pruefen(self):
        """Den Zeitzonenversatz messen, der für die Suiten tatsächlich gilt.

        Bis 3.23.0 setzte der Prüfstand ``TZ`` und verließ sich darauf. Das ist
        eine Absicht, kein Nachweis: Unter Windows bleibt die Variable
        wirkungslos, und ein Lauf auf einem Rechner in UTC wäre gegen
        Zeitzonenfehler genauso blind wie die Vorabumgebung, in der der
        ``UNTIL``-Fehler aus 3.21.0 grün blieb – hätte aber im Protokoll
        behauptet, in Europe/Berlin geprüft zu haben.

        Gemessen wird im Kindprozess mit derselben Umgebung, die auch die
        Suiten bekommen; nur die zählt. Ein Versatz von null ist kein Fehler
        der Anwendung, sondern eine fehlende Absicherung: Der Lauf gilt
        deshalb als unvollständig, nicht als fehlgeschlagen.

        Mitgemessen wird, ob die Zone überhaupt eine Sommerzeitregel kennt.
        Die Fehlerklasse aus 3.21.0 – ein Serienende, das den Rundlauf um
        einen Tag verschiebt – hängt genau daran, und eine Zone ohne diese
        Regel kann sie nicht zeigen.
        """
        code = ("import datetime;m=datetime.datetime.now().astimezone();"
                "o=m.utcoffset();print(int(o.total_seconds()) if o else 0);"
                "print(1 if datetime.datetime(m.year, 1, 15).astimezone().utcoffset()"
                " != datetime.datetime(m.year, 7, 15).astimezone().utcoffset() else 0);"
                "print(m.tzname() or '?')")
        try:
            result = subprocess.run([sys.executable, "-c", code], env=self.env,
                                    capture_output=True, text=True, encoding="utf-8",
                                    errors="replace", timeout=30)
            if result.returncode:
                raise ValueError(result.stderr.strip().splitlines()[-1] if result.stderr
                                 else f"Exitcode {result.returncode}")
            zeilen = result.stdout.splitlines()
            versatz = int(zeilen[0].strip())
            sommerzeit = zeilen[1].strip() == "1"
            zone = zeilen[2].strip() if len(zeilen) > 2 else "?"
        except (OSError, ValueError, IndexError, subprocess.TimeoutExpired) as exc:
            self.zone_problem = f"Zeitzonenversatz nicht ermittelbar: {exc}"
            self.meldung("Zeitzone", "übersprungen", self.zone_problem)
            return
        vorzeichen = "+" if versatz >= 0 else "-"
        stunden, rest = divmod(abs(versatz), 3600)
        gemessen = f"{vorzeichen}{stunden:02d}:{rest // 60:02d}"
        befund = f"{zone}, Versatz {gemessen}, " + (
            "mit Sommerzeitregel" if sommerzeit else "ohne Sommerzeitregel")
        if not versatz:
            self.zone_problem = (
                f"{befund}: In einer Zone ohne Versatz ist jeder Zeitzonenfehler "
                f"unsichtbar. Dieser Lauf weist Zeitzonenverhalten nicht nach"
                + (". Windows richtet sich nach der Systemzeitzone; TZ hilft dort nicht"
                   if sys.platform == "win32" else
                   f". Gesetzt war TZ={self.env.get('TZ', '(nicht gesetzt)')}"))
        elif sys.platform == "win32" and os.environ.get("TZ"):
            # Ein selbst gesetztes TZ bleibt unangetastet – aber unter Windows
            # entsteht daraus keine echte Zone, sondern eine ohne
            # Sommerzeitregel und mit einem Versatz, den es an diesem Tag nicht
            # gibt. Das ist schlimmer als keine Vorgabe, weil es plausibel
            # aussieht.
            self.zone_problem = (
                f"{befund}: TZ={os.environ['TZ']} ist gesetzt, und Windows liest daraus "
                f"keine benannte Zone, sondern eine erfundene ohne Sommerzeitregel. "
                f"Für eine andere Zone die Systemzeitzone umstellen und TZ leeren")
        if self.zone_problem:
            self.meldung("Zeitzone", "übersprungen", self.zone_problem)
        else:
            self.meldung("Zeitzone", "ausgeführt",
                         f"{befund}; Zeitzonenfehler bleiben sichtbar")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modus", choices=("schnell", "voll"), default="schnell")
    parser.add_argument("--protokoll", type=Path, help="Ordner für vollständige Logs und ergebnis.json")
    parser.add_argument("--screenshots", type=Path, help="Bildordner im Vollmodus; Standard: Protokollordner/screenshots")
    parser.add_argument("--timeout", type=int, default=300, help="Zeitlimit je Suite/Werkzeug in Sekunden")
    parser.add_argument("--vordergrund", action="store_true",
                        help="macOS: Prüffenster dürfen Fokus und Vordergrund nehmen (Standard: Hintergrund)")
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout muss positiv sein")
    logdir = args.protokoll.expanduser().resolve() if args.protokoll else None
    run = Prueflauf(logdir, args.timeout)
    if sys.platform == "darwin" and not args.vordergrund:
        # Seit 30.09.2026 laufen die Prüffenster im Hintergrund: Sie nehmen
        # weder Fokus noch Tastatur, man kann nebenher weiterarbeiten
        # (tests/tools/hintergrund/sitecustomize.py).
        hintergrund = str(REPO / "tests/tools/hintergrund")
        run.env["PYTHONPATH"] = os.pathsep.join(filter(None, (hintergrund, run.env.get("PYTHONPATH"))))
        run.env["GLIDE_QA_HINTERGRUND"] = "1"
    if args.modus == "voll" and logdir:
        # Fotos aller Fenster aus test_fenster330 (nur macOS, 29.09.2026).
        run.env["GLIDE_FENSTER_FOTOS"] = str(logdir / "fenster")
    print(f"Glide-Prüflauf ({args.modus}) · Python {sys.version.split()[0]} · {sys.platform}"
          + (" · im Hintergrund" if run.env.get("GLIDE_QA_HINTERGRUND") else ""), flush=True)
    run.funktion("Syntax", syntax_pruefen)
    run.funktion("Versionskonsistenz", versionen_pruefen)
    run.funktion("Dokumentation", dokumentation_pruefen)
    run.funktion("Fixtures", fixtures_pruefen)
    run.prozess("Fachlogik-Unit-Tests", [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(REPO / "tests/unit")])
    run.gui_pruefen()
    run.zone_pruefen()
    for name in SUITEN:
        run.prozess(Path(name).stem, [sys.executable, str(REPO / "tests/integration" / name)], gui=True)
    run.prozess("Showcase", [sys.executable, str(REPO / "tests/tools/pruefe_showcase.py")], gui=True)
    for name in ANALYSEN:
        run.prozess(Path(name).stem, [sys.executable, str(REPO / "tests/tools" / name)])
    if args.modus == "voll":
        target = args.screenshots or (logdir / "screenshots" if logdir else None)
        with tempfile.TemporaryDirectory(prefix="glide-reproduktion-") as tempdir:
            generated = Path(tempdir) / "beispieldaten.glidebackup"
            if run.prozess("Beispieldaten-erzeugen", [sys.executable, str(REPO / "tests/tools/beispieldaten.py"), "--ziel", str(generated)], gui=True):
                def vergleichen():
                    original = REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup"
                    fixture = inhalt_normalisieren(backup_lesen(original))
                    erzeugt = inhalt_normalisieren(backup_lesen(generated))
                    if fixture != erzeugt:
                        # Der Hinweis nennt bewusst beide Richtungen: Eine
                        # Abweichung, die nur auf einer Plattform auftritt,
                        # gehört in den Erzeuger. Wer in diesem Fall die
                        # Fixture neu erzeugt, dreht den Fehlschlag nur auf
                        # die andere Plattform.
                        raise ValueError("Beispieldaten unterscheiden sich vom Erzeuger – "
                                         + fundstellen(fixture, erzeugt)
                                         + "; erst klären, ob der Erzeuger plattformabhängig "
                                           "arbeitet, sonst die Fixture gezielt neu erzeugen")
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
                        fixture = inhalt_normalisieren(release_payload, False)
                        erzeugt = inhalt_normalisieren(backup_lesen(release_generated), False)
                        if fixture != erzeugt:
                            raise ValueError("Release-Fixture unterscheidet sich bei gleichem "
                                             "Planungsstichtag vom Erzeuger – "
                                             + fundstellen(fixture, erzeugt))
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
    exitcode = 1 if failed else 2 if run.gui_problem or run.zone_problem else 0
    if logdir:
        (logdir / "ergebnis.json").write_text(json.dumps({"zeitpunkt": datetime.now().isoformat(timespec="seconds"),
            "modus": args.modus, "python": sys.version, "plattform": sys.platform,
            "exitcode": exitcode, "schritte": run.results}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Ergebnis: {'FEHLGESCHLAGEN' if exitcode == 1 else 'UNVOLLSTÄNDIG' if exitcode == 2 else 'automatisierte Prüfungen erfolgreich'}; manuelle Restprüfung siehe oben.", flush=True)
    return exitcode


if __name__ == "__main__":
    raise SystemExit(main())
