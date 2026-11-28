# SPDX-License-Identifier: MPL-2.0
"""Teil 05: Migration 26 → 27 mit Tk und künstlichen Daten.

Sicherung vor dem ersten Schreiben, stabile Kapitelanker über Umbenennen und
Neustart, Kapitelverweis, Navigationsort mit Rückgängig, Rundlauf der festen
Format-27-Referenz, Rückweg über die Formatsicherung und Schutz vor einem
neueren Format.
"""
import argparse
import copy
import hashlib
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

V26 = json.loads((REPO / "tests/fixtures/current_v26/reference_v26.json").read_text(encoding="utf-8"))
V27 = json.loads((REPO / "tests/fixtures/current_v27/reference_v27.json").read_text(encoding="utf-8"))
PAGE, OTHER, FOLDER = "fixture-notion-page", "fixture-live-page", "fixture-project"


def legacy_with_headings():
    data = copy.deepcopy(V26)
    page = next(e for e in data["lists"] if e["id"] == PAGE)
    page["rich_note"] = {"text": "Planung\nZiele\nText\nFragen\nmehr\n",
                         "spans": [{"tag": "h1", "start": 0, "end": 8}, {"tag": "h2", "start": 8, "end": 14},
                                   {"tag": "h2", "start": 19, "end": 26}], "links": {}}
    return data


with tempfile.TemporaryDirectory(prefix="glide-t05f-", ignore_cleanup_errors=True) as directory:
    os.environ["GLIDE_DATA_DIR"] = directory
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_format27", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    assert mod.ListApp.DATA_SCHEMA_VERSION == 27
    save = Path(mod.SAVE_FILE)
    backups = Path(mod.BACKUP_DIR)
    errors, infos = [], []

    def open_app():
        root = mod.tk.Tk()
        root.geometry("1280x840+20+20")
        root.report_callback_exception = lambda *_exc: errors.append(repr(_exc[1]))
        app = mod.ListApp(root)
        app.show_error = lambda *a, **k: errors.append(repr(a))
        app.show_warning = lambda *a, **k: errors.append(repr(a))
        app.show_info = lambda *a, **k: infos.append(a)
        return root, app

    def settle(root, seconds=0.3):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            root.update()
            time.sleep(0.01)
        assert not errors, errors

    def stored():
        return json.loads(save.read_text(encoding="utf-8"))

    def entry(data, list_id):
        return next(e for e in data["lists"] if e["id"] == list_id)

    def keys(app, list_id):
        return [k.key for k in mod.glide_chapters.outline(app.page_entry(list_id)["rich_note"])]

    # 1. Format-26-Bestand: Start stellt um, sichert vorher bytegenau.
    original = json.dumps(legacy_with_headings(), ensure_ascii=False, indent=2).encode("utf-8")
    save.write_bytes(original)
    root, app = open_app()
    settle(root, 1.0)
    data = stored()
    assert data["version"] == 27, data["version"]
    sicherung = sorted(backups.glob("liste_vor_format27_*.json"))
    assert len(sicherung) == 1, list(backups.iterdir())
    assert hashlib.sha256(sicherung[0].read_bytes()).digest() == hashlib.sha256(original).digest()
    # Glide ergänzt beim ersten Start nur den Eingang (Systemliste).
    eigene = [e for e in data["lists"] if e.get("system_role") != "inbox"]
    assert sorted(e["id"] for e in eigene) == sorted(e["id"] for e in V26["lists"])
    erst = keys(app, PAGE)
    assert len(erst) == 3 and all(len(k) == 32 for k in erst), erst
    assert [k.key for k in mod.glide_chapters.outline(entry(data, PAGE)["rich_note"])] == erst

    # 2. Umbenennen behält den Anker; Rückgängig stellt den Titel wieder her.
    assert app.change_chapter(PAGE, erst[1], "rename", "Neue Ziele")
    settle(root)
    assert keys(app, PAGE) == erst
    assert mod.glide_chapters.find(mod.glide_chapters.outline(app.page_entry(PAGE)["rich_note"]), erst[1]).title == "Neue Ziele"

    # 3. Kapitelverweis folgen; ein fehlender Anker öffnet die Seite mit Hinweis.
    assert app.open_object_reference(mod.glide_objects.chapter_uri(PAGE, erst[2]))
    settle(root)
    assert app.active_list_id == PAGE and app._chapter_jump == (PAGE, erst[2])
    # Offener Seiteneditor: Export ist stabil, neue Überschrift erhält genau einen Anker.
    editor = app.rich_note_editor
    assert editor.entry_id == PAGE
    assert [k.key for k in mod.glide_chapters.outline(editor.document())] == erst
    assert [k.key for k in mod.glide_chapters.outline(editor.document())] == erst
    editor.text.insert("end", chr(10) + "Neu im Editor")
    editor.text.tag_add("h2", "end-1c linestart", "end-1c")
    eins = [k.key for k in mod.glide_chapters.outline(editor.document())]
    assert eins[:3] == erst and len(eins) == 4
    assert [k.key for k in mod.glide_chapters.outline(editor.document())] == eins
    editor.text.delete("end-1c linestart -1c", "end-1c")
    assert [k.key for k in mod.glide_chapters.outline(editor.document())] == erst
    infos.clear()
    assert app.open_object_reference(mod.glide_objects.chapter_uri(PAGE, "f" * 32))
    settle(root)
    assert app.active_list_id == PAGE and infos, infos
    choices = dict(app.object_reference_choices(("list", OTHER), chapters=True))
    assert mod.glide_objects.chapter_uri(PAGE, erst[2]) in choices

    # 4. Navigationsort: Seite erscheint unter dem Projektordner, Heimat bleibt; Undo.
    heimat = app.page_entry(OTHER).get("folder_id")
    app.set_list_navigation(OTHER, FOLDER)
    settle(root)
    assert app.page_entry(OTHER)["nav_parent_id"] == FOLDER and app.page_entry(OTHER).get("folder_id") == heimat
    baum = app.sidebar_tree_for_entry(app.page_entry(OTHER))
    assert baum.parent(f"list:{OTHER}") == f"folder:{FOLDER}", baum.parent(f"list:{OTHER}")
    assert sum(1 for e in app.lists if e["id"] == OTHER) == 1, "keine Kopie"
    assert entry(stored(), OTHER)["nav_parent_id"] == FOLDER
    app.undo_last_change()
    settle(root)
    assert "nav_parent_id" not in app.page_entry(OTHER)
    app.set_list_navigation(OTHER, FOLDER)
    settle(root)
    app.on_close()

    # 5. Neustart: Anker, Titel und Navigationsort bleiben.
    root, app = open_app()
    settle(root, 0.6)
    assert keys(app, PAGE) == erst
    assert app.page_entry(OTHER)["nav_parent_id"] == FOLDER
    assert app.sidebar_tree_for_entry(app.page_entry(OTHER)).parent(f"list:{OTHER}") == f"folder:{FOLDER}"
    # Duplizieren vergibt neue Anker.
    app.duplicate_list(PAGE)
    settle(root)
    kopie = next(e for e in app.lists if e["id"] not in {x["id"] for x in V26["lists"]}
                 and e.get("system_role") != "inbox")
    kopie_keys = [k.key for k in mod.glide_chapters.outline(kopie["rich_note"])]
    assert len(kopie_keys) == 3 and not set(kopie_keys) & set(erst), kopie_keys
    app.on_close()

    # 6. Rückweg: die Formatsicherung zurückgelegt ergibt wieder den Format-26-Bestand.
    save.write_bytes(sicherung[0].read_bytes())
    assert json.loads(save.read_text(encoding="utf-8"))["version"] == 26
    for old in backups.glob("liste_vor_format27_*.json"):
        old.unlink()
    root, app = open_app()
    settle(root, 1.0)
    assert stored()["version"] == 27 and len(list(backups.glob("liste_vor_format27_*.json"))) == 1
    app.on_close()

    # 7. Feste Format-27-Referenz: Laden und Speichern verliert nichts.
    save.write_text(json.dumps(V27, ensure_ascii=False), encoding="utf-8")
    root, app = open_app()
    settle(root, 0.6)
    assert app.save_items()
    data = stored()
    seite, andere = entry(data, PAGE), entry(data, OTHER)
    assert [s for s in seite["rich_note"]["spans"] if s["tag"].startswith("anchor:")] == \
        [s for s in entry(V27, PAGE)["rich_note"]["spans"] if s["tag"].startswith("anchor:")]
    assert andere["nav_parent_id"] == FOLDER
    assert andere["rich_note"]["links"]["link:format27"] == entry(V27, OTHER)["rich_note"]["links"]["link:format27"]
    app.on_close()

    # 8. Neueres Format: nur lesend, Datei bleibt bytegleich.
    neuer = dict(V27, version=28)
    roh = json.dumps(neuer, ensure_ascii=False).encode("utf-8")
    save.write_bytes(roh)
    root, app = open_app()
    settle(root, 0.6)
    assert app._data_read_only and app._read_only_reason == "newer_format", app._read_only_reason
    app.save_items(show_error=False)
    app.on_close()
    assert save.read_bytes() == roh
print("test_format27_migration: OK (Windows-Tk, künstliche Daten)")
