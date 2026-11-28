# SPDX-License-Identifier: MPL-2.0
"""Teil 05B (DS-04): Datensperre mit echten Prozessen und künstlichen Daten.

1. Zwei gleichzeitig laufende Glide-Prozesse auf einem Datenordner: Der zweite
   öffnet nur lesend, Speichern ändert die Datei nicht.
2. Nach regulärem Ende des ersten schreibt ein neuer Start wieder.
3. Veraltete Sperre eines anderen Rechners: schreibgeschützt, keine stille
   Übernahme; Übernahme nur nach Bestätigung.
4. Abgebrochener Besitzer (os._exit): Die Sperre gilt als frei, der Bestand
   startet im Wiederherstellungsmodus und erst nach Freigabe schreibbar.
"""
import argparse
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
parser.add_argument("--halter", type=Path, default=None)
parser.add_argument("--modus", default="halten")
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))


def laden(directory):
    os.environ["GLIDE_DATA_DIR"] = str(directory)
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader(f"glide_sperre_{os.getpid()}", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    return mod


def oeffnen(mod, fehler, fragen=None):
    root = mod.tk.Tk()
    root.geometry("900x600+40+40")
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = lambda *a, **k: fehler.append(repr(a))
    app.show_warning = lambda *a, **k: None
    app.show_info = lambda *a, **k: None
    if fragen is not None:
        app.ask_yes_no = lambda *a, **k: fragen.pop(0) if fragen else False
    for _ in range(15):
        root.update()
        time.sleep(0.02)
    return root, app


def halter(directory):
    """Prozess A: hält den Bestand offen, bis `stop` erscheint oder bricht ab."""
    mod = laden(directory)
    fehler = []
    root, app = oeffnen(mod, fehler)
    assert not app._data_read_only, app._read_only_reason
    entry = app.new_list_object("Gemeinsam", [])
    app.lists.append(entry)
    assert app.save_items()
    (directory / "bereit").write_text(str(os.getpid()), encoding="utf-8")
    if args.modus == "abbrechen":
        os._exit(0)
    frist = time.monotonic() + 120
    while not (directory / "stop").exists() and time.monotonic() < frist:
        root.update()
        time.sleep(0.05)
    app.on_close()
    os._exit(0)


def starte_halter(directory, modus):
    prozess = subprocess.Popen([sys.executable, "-B", __file__, "--app", str(args.app),
                                "--halter", str(directory), "--modus", modus])
    frist = time.monotonic() + 120
    while not (directory / "bereit").exists():
        assert prozess.poll() is None or modus == "abbrechen", "Halter endete vorzeitig"
        assert time.monotonic() < frist, "Halter wurde nicht bereit"
        time.sleep(0.1)
    return prozess


def haupt():
    with tempfile.TemporaryDirectory(prefix="glide-sperre-", ignore_cleanup_errors=True) as tmp:
        directory = Path(tmp)
        mod = laden(directory)
        speicher = Path(mod.SAVE_FILE)
        fehler = []

        # 1. Zwei lebende Prozesse.
        a = starte_halter(directory, "halten")
        vorher = speicher.read_bytes()
        root, app = oeffnen(mod, fehler)
        assert app._data_read_only and app._read_only_reason == "lock", app._read_only_reason
        app.lists.append(app.new_list_object("Darf nicht ankommen", []))
        assert not app.save_items(show_error=False)
        assert speicher.read_bytes() == vorher, "zweiter Prozess hat geschrieben"
        sperre = json.loads(Path(mod.LOCK_FILE).read_text(encoding="utf-8"))
        assert sperre["pid"] == a.pid, sperre
        app.on_close()
        assert json.loads(Path(mod.LOCK_FILE).read_text(encoding="utf-8"))["pid"] == a.pid, "fremde Sperre entfernt"

        # 2. Regulärer Abschluss von A, danach schreibt ein neuer Start.
        (directory / "stop").write_text("1", encoding="utf-8")
        assert a.wait(120) == 0
        root, app = oeffnen(mod, fehler)
        assert not app._data_read_only, app._read_only_reason
        assert app.save_items()
        app.on_close()
        (directory / "stop").unlink()
        (directory / "bereit").unlink()

        # 3. Abgebrochener Besitzer.
        a = starte_halter(directory, "abbrechen")
        a.wait(120)
        root, app = oeffnen(mod, fehler, fragen=[True])
        assert app._read_only_reason == "recovery", app._read_only_reason
        assert app.resume_recovery_session()
        assert not app._data_read_only and app.save_items()
        app.on_close()
        # 4. Veraltete Sperre eines anderen Rechners: kein stilles Übernehmen.
        alt = {"host": "ANDERER-RECHNER", "pid": 4242, "token": "f" * 32,
               "started_at": "2026-11-20T08:00:00+01:00", "refreshed_at": "2026-11-20T08:05:00+01:00"}
        Path(mod.LOCK_FILE).write_text(json.dumps(alt), encoding="utf-8")
        vorher = speicher.read_bytes()
        root, app = oeffnen(mod, fehler, fragen=[False])
        assert app._data_read_only and app._read_only_reason == "lock_defective", app._read_only_reason
        assert app.lock_info.get("stale"), app.lock_info
        app.show_data_lock_warning()
        assert app._data_read_only, "ohne Bestätigung übernommen"
        assert not app.save_items(show_error=False) and speicher.read_bytes() == vorher
        assert json.loads(Path(mod.LOCK_FILE).read_text(encoding="utf-8")) == alt
        app.ask_yes_no = lambda *a, **k: True
        app.show_data_lock_warning()
        assert not app._data_read_only, "Übernahme nach Bestätigung fehlgeschlagen"
        assert json.loads(Path(mod.LOCK_FILE).read_text(encoding="utf-8"))["pid"] == os.getpid()
        app.on_close()

        assert not fehler, fehler
    print("test_sperre_mehrprozess: OK (echte Prozesse, Windows-Tk, künstliche Daten)")


if args.halter is not None:
    halter(args.halter)
else:
    haupt()
