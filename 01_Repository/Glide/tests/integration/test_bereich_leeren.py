# SPDX-License-Identifier: MPL-2.0
"""Teil 05B (NAV-02C): Bereich sicher leeren, mit künstlichen Daten und Windows-Tk."""
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
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))

with tempfile.TemporaryDirectory(prefix="glide-leeren-", ignore_cleanup_errors=True) as directory:
    os.environ["GLIDE_DATA_DIR"] = directory
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_leeren", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    fehler = []

    def oeffnen():
        root = mod.tk.Tk()
        root.geometry("1100x760+30+30")
        root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
        app = mod.ListApp(root)
        app.show_error = lambda *a, **k: fehler.append(("error",) + a)
        app.show_warning = lambda *a, **k: fehler.append(("warning",) + a)
        app.show_info = lambda *a, **k: None
        app.ask_yes_no = lambda *a, **k: True
        return root, app

    def ruhe(root, s=0.3):
        frist = time.monotonic() + s
        while time.monotonic() < frist:
            root.update()
            time.sleep(0.01)

    root, app = oeffnen()
    buch = app.new_folder_object("Handbuch", folder_kind="library")
    kapitel = app.new_folder_object("Teil A", folder_kind="library", parent_id=buch["id"])
    projekt = app.new_folder_object("Projekt")
    app.folders.extend([buch, kapitel, projekt])
    s1 = app.new_list_object("Seite eins", [], folder_id=buch["id"], list_kind="page",
                             rich_note={"text": "Kapitel\nText\n", "spans": [{"tag": "h1", "start": 0, "end": 8}], "links": {}})
    s2 = app.new_list_object("Seite zwei", [], folder_id=kapitel["id"], list_kind="page")
    lose = app.new_list_object("Lose Seite", [], list_kind="page")
    # Heimat im Buch, angezeigt im Projektordner: wird mit gelöscht.
    s3 = app.new_list_object("Anderswo gezeigt", [], folder_id=buch["id"], list_kind="page", nav_parent_id=projekt["id"])
    # Heimat ohne Ordner (Seitenbereich-Wurzel nicht), angezeigt im Buch: bleibt.
    gast = app.new_list_object("Gast", [], folder_id=projekt["id"], list_kind="page", nav_parent_id=buch["id"])
    aufgaben = app.new_list_object("Aufgaben", [app.new_item("Bleibt") if hasattr(app, "new_item") else {"text": "Bleibt"}][:0])
    app.lists.extend([s1, s2, lose, s3, gast, aufgaben])
    assert app.save_items()
    app.update_sidebar_list()
    ruhe(root)
    umfang = app.sidebar_section_clear_scope("pages")
    heim = {e["id"] for e in umfang["lists"]}
    assert heim == {s1["id"], s2["id"], lose["id"], s3["id"]}, heim
    assert [e["id"] for e in umfang["only_shown"]] == [gast["id"]]
    assert [e["id"] for e in umfang["shown_elsewhere"]] == [s3["id"]]
    assert umfang["folder_ids"] == {buch["id"], kapitel["id"]}

    # Fehlerfall 1: Sicherung schlägt fehl → nichts geändert.
    vorher = Path(mod.SAVE_FILE).read_bytes()
    original = app.write_complete_backup
    app.write_complete_backup = lambda *a, **k: (_ for _ in ()).throw(OSError("simulierter Schreibfehler"))
    assert not app.clear_sidebar_section("pages")
    app.write_complete_backup = original
    assert Path(mod.SAVE_FILE).read_bytes() == vorher and fehler and fehler[-1][0] == "error"
    fehler.clear()

    # Fehlerfall 2: Papierkorb zu voll → nichts geändert, keine Verdrängung.
    platz = app.MAX_TRASH_ENTRIES
    app.MAX_TRASH_ENTRIES = len(app.trash) + 2
    assert not app.clear_sidebar_section("pages")
    app.MAX_TRASH_ENTRIES = platz
    assert Path(mod.SAVE_FILE).read_bytes() == vorher and fehler[-1][0] == "warning"
    fehler.clear()

    # Abbruch durch den Nutzer.
    app.ask_yes_no = lambda *a, **k: False
    assert not app.clear_sidebar_section("pages")
    assert Path(mod.SAVE_FILE).read_bytes() == vorher
    app.ask_yes_no = lambda *a, **k: True

    # Erfolgsfall.
    papierkorb_vorher = len(app.trash)
    assert app.clear_sidebar_section("pages")
    ruhe(root)
    ids = {e["id"] for e in app.lists}
    assert not ids & heim, ids & heim
    assert gast["id"] in ids and aufgaben["id"] in ids
    assert not {f["id"] for f in app.folders} & {buch["id"], kapitel["id"]}
    assert projekt["id"] in {f["id"] for f in app.folders}
    assert len(app.trash) == papierkorb_vorher + 6, len(app.trash)
    sicherung = Path(app._last_section_clear_backup)
    assert sicherung.is_file()
    daten, _ = app.read_app_backup_file(str(sicherung))
    assert heim <= {e["id"] for e in daten["lists"]}
    # Der Gast steht wieder an seiner Heimat (Navigationsort zeigt ins Leere).
    assert app.sidebar_parent(next(e for e in app.lists if e["id"] == gast["id"])) == projekt["id"]

    # Rückgängig stellt alles her, mit Kapitelanker.
    anker = [k.key for k in app.chapter_outline(s1)]
    app.undo_last_change()
    ruhe(root)
    assert heim <= {e["id"] for e in app.lists}
    assert {buch["id"], kapitel["id"]} <= {f["id"] for f in app.folders}
    assert len(app.trash) == papierkorb_vorher
    assert [k.key for k in app.chapter_outline(app.page_entry(s1["id"]))] == anker
    assert next(e for e in app.lists if e["id"] == s3["id"])["nav_parent_id"] == projekt["id"]

    # Erneut leeren, Neustart: Zustand bleibt, Papierkorb trägt alles.
    assert app.clear_sidebar_section("pages")
    app.on_close()
    root, app = oeffnen()
    ruhe(root)
    assert not heim & {e["id"] for e in app.lists}
    assert len(app.trash) == papierkorb_vorher + 6
    app.on_close()
    assert not fehler, fehler
print("test_bereich_leeren: OK (Umfang, Sicherung, Fehler, Abbruch, Rückgängig, Neustart; Windows-Tk, künstliche Daten)")
