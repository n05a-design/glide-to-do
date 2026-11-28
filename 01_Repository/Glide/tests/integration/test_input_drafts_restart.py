# SPDX-License-Identifier: MPL-2.0
"""Teil 05: Inline-Entwurf übersteht Neustart und simulierten Absturz (künstliche Daten)."""
import argparse
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
parser.add_argument("--crash-phase", type=Path, default=None)
parser.add_argument("--crash-mode", default="tippen")
args = parser.parse_args()
import subprocess
sys.path.insert(0, str(args.app.parent))

def run(directory):
    os.environ["GLIDE_DATA_DIR"] = str(directory)
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_drafts_t05", str(args.app))
    global mod
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    errors = []
    toasts = []

    def open_app():
        root = mod.tk.Tk()
        root.geometry("1280x840+20+20")
        root.report_callback_exception = lambda *_exc: errors.append(repr(_exc[1]))
        app = mod.ListApp(root)
        app.show_error = lambda *a, **k: errors.append(repr(a))
        app.show_warning = lambda *a, **k: errors.append(repr(a))
        original = app.show_undo_toast
        app.show_undo_toast = lambda text, restore=None: (toasts.append(text), original(text, restore))
        return root, app

    def settle(root, seconds=0.25):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            root.update()
            time.sleep(0.01)
        assert not errors, errors

    draft_file = Path(directory) / "input_drafts.json"
    if args.crash_phase is not None:
        root, app = open_app()
        entry = app.new_list_object("Entwurf-Test", [])
        app.lists.append(entry)
        assert app.save_items()
        app.set_active_list(entry["id"])
        settle(root)
        app.inline_task_entry.focus_force()
        app.inline_task_entry.insert(0, "Angebot nachfassen")
        settle(root, 1.2)  # verzögertes Schreiben (800 ms)
        (Path(directory) / "list_id.txt").write_text(entry["id"], encoding="utf-8")
        if args.crash_mode == "nach_enter":
            # Teil 05B: Abbruch unmittelbar nach dem Anlegen, ohne jede Wartezeit.
            app.inline_task_entry.event_generate("<Return>")
            root.update_idletasks()
            os._exit(0)
        os._exit(0)  # echter Prozessabbruch: kein on_close, kein Speichern, keine Freigabe
    child = subprocess.run([sys.executable, "-B", __file__, "--app", str(args.app),
                            "--crash-phase", str(directory)], timeout=240)
    assert child.returncode == 0, child.returncode
    list_id = (Path(directory) / "list_id.txt").read_text(encoding="utf-8")
    stored = json.loads(draft_file.read_text(encoding="utf-8"))
    assert [d["text"] for d in stored["drafts"]] == ["Angebot nachfassen"], stored
    toasts.clear()
    root, app = open_app()
    settle(root)
    # Nach dem Absturz startet Glide schreibgeschützt (Wiederherstellungsmodus);
    # der Entwurf bleibt dabei unangetastet erhalten.
    assert app._read_only_reason == "recovery", app._read_only_reason
    assert json.loads(draft_file.read_text(encoding="utf-8")) == stored
    app.ask_yes_no = lambda *a, **k: True
    assert app.resume_recovery_session()
    app.set_active_list(list_id)
    settle(root)
    assert app.inline_task_entry.get() == "Angebot nachfassen", app.inline_task_entry.get()
    assert app.current_list()["items"] == [], "Entwurf darf keine Aufgabe sein"
    assert any("Entwurf" in t or "draft" in t for t in toasts), toasts
    # Übernehmen entfernt den Entwurf dauerhaft, ohne Duplikat.
    app.inline_task_entry.focus_force()
    app.inline_task_entry.event_generate("<Return>")
    settle(root, 1.2)
    assert [i["text"] for i in app.current_list()["items"]] == ["Angebot nachfassen"]
    assert json.loads(draft_file.read_text(encoding="utf-8"))["drafts"] == []
    # Verworfener Entwurf (Escape) kommt nach Neustart nicht wieder.
    app.inline_task_entry.insert(0, "verwerfen")
    settle(root, 1.2)
    app.inline_task_entry.event_generate("<Escape>")
    app.on_close()

    root, app = open_app()
    app.set_active_list(list_id)
    settle(root)
    assert app.inline_task_entry.get() == ""
    assert [i["text"] for i in app.current_list()["items"]] == ["Angebot nachfassen"]
    app.on_close()


def run_nach_enter(directory):
    """Absturz direkt nach Enter: genau eine Aufgabe, kein wiederhergestellter Entwurf."""
    child = subprocess.run([sys.executable, "-B", __file__, "--app", str(args.app),
                            "--crash-phase", str(directory), "--crash-mode", "nach_enter"], timeout=240)
    assert child.returncode == 0, child.returncode
    os.environ["GLIDE_DATA_DIR"] = str(directory)
    loader = importlib.machinery.SourceFileLoader("glide_drafts_t05b", str(args.app))
    m = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = m
    loader.exec_module(m)
    daten = json.loads((Path(directory) / "liste_speicher.json").read_text(encoding="utf-8"))
    list_id = (Path(directory) / "list_id.txt").read_text(encoding="utf-8")
    liste = next(e for e in daten["lists"] if e["id"] == list_id)
    assert [i["text"] for i in liste["items"]] == ["Angebot nachfassen"], liste["items"]
    entwuerfe = json.loads((Path(directory) / "input_drafts.json").read_text(encoding="utf-8"))["drafts"]
    assert entwuerfe == [], entwuerfe


if args.crash_phase is not None:
    run(args.crash_phase)
else:
    with tempfile.TemporaryDirectory(prefix="glide-t05d-", ignore_cleanup_errors=True) as directory:
        run(directory)
    with tempfile.TemporaryDirectory(prefix="glide-t05e-", ignore_cleanup_errors=True) as directory:
        run_nach_enter(directory)
    print("test_input_drafts_restart: OK (echte Prozessabbrüche beim Tippen und direkt nach Enter, künstliche Daten)")
