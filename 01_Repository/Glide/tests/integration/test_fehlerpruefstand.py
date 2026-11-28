# SPDX-License-Identifier: MPL-2.0
"""Teil 05B: Fehler- und Katastrophenprüfstand für Migration und Speichern.

Künstliche Daten, kontrollierte Fehlerinjektion; der Abbruch mitten in der
Migration ist ein echter Prozessabbruch (os._exit). Hardware-, Stromausfall-
und echte Datenträgerfüllung werden nicht geprüft.

Fälle: fehlgeschlagene Migrationssicherung, unterbrochene Migration,
wiederholte Migration, voller Datenträger, fehlende Schreibrechte,
beschädigte Hauptdatei, ungültige Verweise.
"""
import argparse
import copy
import errno
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
parser.add_argument("--abbruch", type=Path, default=None)
parser.add_argument("--sicherungsfehler", type=Path, default=None)
parser.add_argument("--verweise", type=Path, default=None)
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))
V26 = (REPO / "tests/fixtures/current_v26/reference_v26.json").read_bytes()
V27 = json.loads((REPO / "tests/fixtures/current_v27/reference_v27.json").read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def laden(directory, name):
    os.environ["GLIDE_DATA_DIR"] = str(directory)
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader(name, str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    return mod


def abbruch_kind(directory):
    """Migration starten und genau beim Schreiben der neuen Hauptdatei hart abbrechen."""
    mod = laden(directory, "glide_abbruch")
    echt = mod.ListApp.write_json_atomic

    def schreiben(path, data, *a, **k):
        if Path(path) == Path(mod.SAVE_FILE) and isinstance(data, dict) and data.get("version") == 27:
            os._exit(0)
        return echt(path, data, *a, **k)
    mod.ListApp.write_json_atomic = staticmethod(schreiben)
    root = mod.tk.Tk()
    mod.ListApp(root)
    for _ in range(40):
        root.update()
        time.sleep(0.02)
    os._exit(3)  # die Migration hätte schreiben müssen


def sicherungsfehler_kind(directory):
    """Vorsicherung scheitert (simuliert voller Datenträger): Start, Speicherversuch, harter Abbruch."""
    import errno as _errno
    import schema_backups
    schema_backups.shutil.copy2 = lambda *a, **k: (_ for _ in ()).throw(OSError(_errno.ENOSPC, "kein Platz (simuliert)"))
    mod = laden(directory, "glide_sicherungsfehler")
    root = mod.tk.Tk()
    app = mod.ListApp(root)
    app.show_error = app.show_warning = app.show_info = lambda *a, **k: None
    for _ in range(30):
        root.update()
        time.sleep(0.02)
    if app.lists:
        app.lists[0]["title"] = "Änderung ohne Sicherung"
    gespeichert = app.save_items(show_error=False)
    os._exit(0 if not gespeichert else 4)


def verweise_kind(d):
    speicher = d / "liste_speicher.json"
    daten = copy.deepcopy(V27)
    seite = next(e for e in daten["lists"] if e["id"] == "fixture-live-page")
    seite["nav_parent_id"] = "gibt-es-nicht"
    seite["rich_note"]["links"]["link:format27"] = "glide://list/fixture-notion-page#" + "e" * 32
    speicher.write_text(json.dumps(daten, ensure_ascii=False), encoding="utf-8")
    mod = laden(d, "glide_verweise")
    meldungen = []
    root = mod.tk.Tk()
    app = mod.ListApp(root)
    app.show_error = lambda *a, **k: meldungen.append(("error",) + a)
    app.show_warning = lambda *a, **k: meldungen.append(("warning",) + a)
    app.show_info = lambda *a, **k: meldungen.append(("info",) + a)
    for _ in range(30):
        root.update()
        time.sleep(0.02)
    eintrag = app.page_entry("fixture-live-page")
    assert eintrag is not None, (app._read_only_reason, meldungen[:3])
    assert eintrag["nav_parent_id"] == "gibt-es-nicht", "unbekanntes Ziel still entfernt"
    assert app.sidebar_parent(eintrag) == eintrag.get("folder_id"), "kein Rückfall auf Heimat"
    assert app.open_object_reference("glide://list/fixture-notion-page#" + "e" * 32)
    assert app.active_list_id == "fixture-notion-page" and any(m[0] == "info" for m in meldungen), meldungen
    assert app.save_items()
    gespeichert = json.loads(speicher.read_text(encoding="utf-8"))
    assert next(e for e in gespeichert["lists"] if e["id"] == "fixture-live-page")["nav_parent_id"] == "gibt-es-nicht"
    app.on_close()


def haupt():
    ergebnisse = []
    with tempfile.TemporaryDirectory(prefix="glide-fehler-", ignore_cleanup_errors=True) as tmp:
        d = Path(tmp)
        speicher = d / "liste_speicher.json"
        sicherungen = d / "backups"

        # 1. Unterbrochene Migration (echter Prozessabbruch).
        speicher.write_bytes(V26)
        kind = subprocess.run([sys.executable, "-B", __file__, "--app", str(args.app), "--abbruch", str(d)], timeout=300)
        assert kind.returncode == 0, kind.returncode
        assert speicher.read_bytes() == V26, "Teilstand aktiviert"
        vor = sorted(sicherungen.glob("liste_vor_format27_*.json"))
        assert vor and vor[0].read_bytes() == V26
        assert not [n for n in os.listdir(d) if n.endswith(".tmp")], os.listdir(d)
        ergebnisse.append("Unterbrochene Migration: Hauptdatei bytegleich Format 26, Vorsicherung vorhanden, keine Zwischendatei")

        mod = laden(d, "glide_fehler")
        meldungen = []

        def oeffnen(fragen=True):
            root = mod.tk.Tk()
            root.geometry("900x600+40+40")
            app = mod.ListApp(root)
            app.show_error = lambda *a, **k: meldungen.append(("error",) + a)
            app.show_warning = lambda *a, **k: meldungen.append(("warning",) + a)
            app.show_info = lambda *a, **k: meldungen.append(("info",) + a)
            app.ask_yes_no = lambda *a, **k: fragen
            for _ in range(30):
                root.update()
                time.sleep(0.02)
            return root, app

        # Nach dem Abbruch: Wiederherstellungsmodus, Freigabe, dann Migration.
        root, app = oeffnen()
        if app._read_only_reason == "recovery":
            assert app.resume_recovery_session()
            for _ in range(20):
                root.update()
        assert json.loads(speicher.read_text(encoding="utf-8"))["version"] == 27
        app.on_close()
        anzahl = len(list(sicherungen.glob("liste_vor_format27_*.json")))
        # 2. Wiederholte Migration: bereits Format 27, keine neue Vorsicherung.
        root, app = oeffnen()
        assert not app._data_read_only, app._read_only_reason
        assert len(list(sicherungen.glob("liste_vor_format27_*.json"))) == anzahl
        app.on_close()
        ergebnisse.append("Wiederholte Migration: kein zweiter Lauf, keine neue Vorsicherung")

        # 3. Fehlgeschlagene Migrationssicherung: Migration beginnt nicht (eigener Prozess).
        for alt in sicherungen.glob("liste_vor_format27_*.json"):
            alt.unlink()
        speicher.write_bytes(V26)
        kind = subprocess.run([sys.executable, "-B", __file__, "--app", str(args.app), "--sicherungsfehler", str(d)],
                              capture_output=True, text=True, timeout=300)
        assert kind.returncode == 0, (kind.stdout[-800:], kind.stderr[-2000:])
        assert speicher.read_bytes() == V26, "Migration ohne Vorsicherung begonnen"
        assert not list(sicherungen.glob("liste_vor_format27_*.json"))
        ergebnisse.append("Fehlgeschlagene Migrationssicherung: keine Umstellung, kein Speichern, Datei bytegleich")

        # Saubere Migration für die folgenden Fälle (nach Freigabe des Kindprozess-Abbruchs).
        root, app = oeffnen()
        if app._read_only_reason == "recovery":
            assert app.resume_recovery_session()
            for _ in range(20):
                root.update()
        assert json.loads(speicher.read_text(encoding="utf-8"))["version"] == 27
        # 4. Voller Datenträger beim Speichern.
        vorher = speicher.read_bytes()
        echt_schreiben = app.write_json_atomic
        app.write_json_atomic = lambda path, data, *a, **k: (_ for _ in ()).throw(OSError(errno.ENOSPC, "No space left on device (simuliert)")) \
            if Path(path) == speicher else echt_schreiben(path, data, *a, **k)
        app.lists[0]["title"] = "Geht nicht"
        app.dirty = True  # wie nach einer Bearbeitung
        meldungen.clear()
        assert not app.save_items()
        assert any(m[0] == "error" for m in meldungen), "Fehler nicht sichtbar"
        assert speicher.read_bytes() == vorher
        assert app.dirty, "ungespeicherte Änderung muss sichtbar bleiben"
        app.write_json_atomic = echt_schreiben
        assert app.save_items()
        ergebnisse.append("Voller Datenträger: Original bytegleich, Änderung bleibt als ungespeichert sichtbar, späteres Speichern gelingt")
        # 5. Fehlende Schreibrechte.
        vorher = speicher.read_bytes()
        os.chmod(speicher, stat.S_IREAD)
        try:
            app.lists[0]["title"] = "Schreibgeschützt"
            ergebnis = app.save_items(show_error=False)
            assert speicher.read_bytes() == vorher or ergebnis, "Teilschreibvorgang"
            if os.name == "nt":
                assert not ergebnis and speicher.read_bytes() == vorher
        finally:
            os.chmod(speicher, stat.S_IREAD | stat.S_IWRITE)
        app.on_close()
        ergebnisse.append("Fehlende Schreibrechte: Speichern abgelehnt, Datei unverändert (Windows: Nur-Lesen-Attribut)")

        # 6. Beschädigte Hauptdatei: bytegenaue Kopie vor jedem Schreiben, Fehler sichtbar.
        kaputt = b'{"version": 27, "lists": [ {"id": "x", '
        speicher.write_bytes(kaputt)
        vorhandene = {p.name for p in d.rglob("*") if p.is_file()}
        meldungen.clear()
        gemeldet = []
        klasse_fehler = mod.ListApp.show_error
        mod.ListApp.show_error = lambda self, *a, **k: gemeldet.append(a)  # Meldung schon beim Start erfassen
        try:
            root, app = oeffnen(fragen=False)
        finally:
            mod.ListApp.show_error = klasse_fehler
        assert gemeldet, "Beschädigung nicht gemeldet"
        kopien = [p for p in d.rglob("*") if p.is_file() and p.name not in vorhandene and p.read_bytes() == kaputt]
        assert kopien or app._data_read_only, "weder Kopie noch Schreibschutz"
        if kopien:
            assert app.save_items()  # erst nach der bytegleichen Kopie zulässig
        app.on_close()
        assert any(p.read_bytes() == kaputt for p in kopien) or speicher.read_bytes() == kaputt
        ergebnisse.append("Beschädigte Hauptdatei: Fehler gemeldet, Original vor jedem Schreiben bytegleich gesichert ("
                          + (kopien[0].name if kopien else "schreibgeschützt") + ")")

        # 7. Ungültige Verweise (eigener Prozess, frischer Datenordner).
        frisch = d.parent / (d.name + "-verweise")
        frisch.mkdir()
        kind = subprocess.run([sys.executable, "-B", __file__, "--app", str(args.app), "--verweise", str(frisch)],
                              capture_output=True, text=True, timeout=300)
        assert kind.returncode == 0, (kind.stdout[-800:], kind.stderr[-2500:])
        ergebnisse.append("Ungültige Verweise: Navigationsort bleibt erhalten und fällt sichtbar zurück, Kapitelverweis öffnet Seite mit Hinweis")
    print("test_fehlerpruefstand: OK (künstliche Daten, Fehlerinjektion, ein echter Prozessabbruch)\n  " + "\n  ".join(ergebnisse))


if args.abbruch is not None:
    abbruch_kind(args.abbruch)
elif args.sicherungsfehler is not None:
    sicherungsfehler_kind(args.sicherungsfehler)
elif args.verweise is not None:
    verweise_kind(args.verweise)
else:
    haupt()
