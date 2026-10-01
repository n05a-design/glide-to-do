#!/usr/bin/env python3
"""Prüft den Showcase über Import, Editor, Undo, Vorlagen und Neustart.

Alle Schreibzugriffe sind temporär. Optionale Fotos zeigen nur das eigene
Glide-Fenster. Die Datei testet die gelieferten Daten, keine Kopie ihres Builders.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import zipfile

from rundgang import load_module, ruhe

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/showcase"


def settle(root, seconds=.3):
    end = time.monotonic()+seconds
    while time.monotonic() < end:
        ruhe(root, 1)
        time.sleep(.01)


def photo(directory, name):
    if directory is None or sys.platform != "darwin":
        return
    import ctypes
    import ctypes.util
    cf = ctypes.cdll.LoadLibrary(ctypes.util.find_library("CoreFoundation"))
    cg = ctypes.cdll.LoadLibrary(ctypes.util.find_library("CoreGraphics"))
    cf.CFStringCreateWithCString.restype = ctypes.c_void_p
    cf.CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32]
    cf.CFArrayGetCount.restype = ctypes.c_long
    cf.CFArrayGetCount.argtypes = [ctypes.c_void_p]
    cf.CFArrayGetValueAtIndex.restype = ctypes.c_void_p
    cf.CFArrayGetValueAtIndex.argtypes = [ctypes.c_void_p, ctypes.c_long]
    cf.CFDictionaryGetValue.restype = ctypes.c_void_p
    cf.CFDictionaryGetValue.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    cf.CFNumberGetValue.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
    cf.CFRelease.argtypes = [ctypes.c_void_p]
    cg.CGWindowListCopyWindowInfo.restype = ctypes.c_void_p
    cg.CGWindowListCopyWindowInfo.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
    keys = [cf.CFStringCreateWithCString(None, key.encode(), 0x08000100)
            for key in ("kCGWindowOwnerPID", "kCGWindowNumber", "kCGWindowLayer")]
    windows = cg.CGWindowListCopyWindowInfo(1 | 16, 0)
    def number(entry, key):
        result = ctypes.c_int64()
        value = cf.CFDictionaryGetValue(entry, key)
        if value:
            cf.CFNumberGetValue(value, 4, ctypes.byref(result))
        return result.value
    try:
        own = [number(entry, keys[1]) for i in range(cf.CFArrayGetCount(windows))
               if number(entry := cf.CFArrayGetValueAtIndex(windows, i), keys[0]) == os.getpid()
               and number(entry, keys[2]) == 0]
        assert own, "Das eigene Glide-Fenster wurde nicht gefunden."
        directory.mkdir(parents=True, exist_ok=True)
        subprocess.run(["screencapture", "-x", "-o", "-l", str(own[0]), str(directory/(name+".png"))], check=True)
    finally:
        cf.CFRelease(windows)
        for key in keys:
            cf.CFRelease(key)


def entries(app):
    return {entry["title"]:entry for entry in app.lists}


def integrity(app, expected_lists, expected_boards=3):
    assert len(app.lists) == expected_lists
    assert {e["list_kind"] for e in app.lists} == {"tasks", "note", "page", "drawing", "gallery"}
    assert {f["folder_kind"] for f in app.folders} == {"standard", "library", "journal"}
    ids = app.data_item_ids()
    for entry in app.lists:
        for item in app.walk_items(entry.get("items", [])):
            for field in ("links", "blocked_by"):
                assert all(value in ids for value in item.get(field, [])), (entry["title"],field)
        for info in (entry.get("rich_note") or {}).get("images", {}).values():
            attachment = app.page_attachment(entry["id"], info["attachment"])
            assert attachment and Path(app.resolve_attachment_path(attachment)).is_file()
    for storage, source in app.collect_attachment_sources(app.lists, folders=app.folders).items():
        assert Path(source).is_file(), storage
    assert len(app.settings["pinboards"]) == expected_boards
    list_ids = {e["id"] for e in app.lists}
    for board in app.settings["pinboards"].values():
        card_ids = {c["item_id"] for c in board["cards"]}
        for card in board["cards"]:
            assert card["list_id"] in list_ids
            assert card["item_id"] in ids or card["item_id"] == "page:"+card["list_id"]
        for connection in board["connections"]:
            assert connection["from"] in card_ids and connection["to"] in card_ids


def check(fixture, images=None, restart_dir=None):
    with tempfile.TemporaryDirectory(prefix="glide-showcase-pruefen-") as temporary:
        data_dir = Path(restart_dir or temporary)/"Glide"
        mod = load_module(data_dir)
        root = mod.tk.Tk()
        root.geometry("1440x960+20+30")
        errors = []
        root.report_callback_exception = lambda *args: errors.append(repr(args[1]))
        app = mod.ListApp(root)
        app.show_info = lambda *a, **k: None
        app.show_warning = app.show_error = lambda *a, **k: errors.append(str(a))
        try:
            settle(root)
            if restart_dir:
                integrity(app, 11)
                assert len(entries(app)["Parkquartier · Briefing und Freigabe"]["rich_note"]["images"]) == 3
                assert app.settings["profile_name"] == "Atelier Nord · Showcase"
                assert any(t["title"] == "{{Wochentag}} KW {{KW}} · {{Projekt}}" for t in app.templates)
                assert not errors, errors
                print("Neustart: ok")
                return
            manifest = json.loads((fixture/"manifest.json").read_text())
            assert manifest["app_version"] == mod.APP_VERSION
            for name, record in manifest["dateien"].items():
                path = fixture/name
                assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"], name
                if path.suffix in (".glidebackup", ".glideapp"):
                    with zipfile.ZipFile(path) as archive:
                        assert archive.testzip() is None
                        payload = json.loads(archive.read("data.json"))
                        sources = app.validate_backup_schema(payload, portable=True)
                        assert sources and all(s in archive.namelist() for s in sources)
            templates = json.loads((fixture/"Glide-Showcase.glidetemplates").read_text())["templates"]
            for template in templates:
                app.validate_template_payload(template)
            # Hinzufügen muss vorhandene Aufgaben/Einstellungen erhalten und IDs neu vergeben.
            untouched = app.new_list_object("Vorhandenes Testprojekt", [app.new_item("Behalten")])
            app.lists.append(untouched)
            app.settings["profile_name"] = "Vorhandenes Profil"
            before_ids = app.data_item_ids()
            before_count = len(app.lists)
            app.save_items()
            assert app.import_full_backup(additive=True, path=str(fixture/"Glide-Showcase.glidebackup"),
                                          show_success=False, confirm=False)
            settle(root)
            assert len(app.lists) == before_count+10
            assert before_ids <= app.data_item_ids()
            assert app.settings["profile_name"] == "Vorhandenes Profil"
            integrity(app, before_count+10, expected_boards=2)
            # Die Vollvariante setzt nur diesen temporären Arbeitsstand auf die Demo zurück.
            assert app.restore_app_backup(str(fixture/"Glide-Showcase_App.glideapp"),
                sections={"tasks":True,"settings":True,"templates":True,"activity":True}, show_success=False)
            settle(root)
            integrity(app, 11)
            lists = entries(app)
            main = lists["Vermarktung · Umsetzung"]
            briefing = lists["Parkquartier · Briefing und Freigabe"]
            gallery = lists["Bildwelt · Auswahl mit Kommentaren"]
            assert len(gallery["attachments"]) == 6
            assert all(a.get("title") and a.get("note") for a in gallery["attachments"])
            assert set((i.get("repeat") or {}).get("art") for e in app.lists for i in e["items"] if i.get("repeat")) == set(app.REPEAT_KINDS)
            assert {i["reminder"]["mode"] for e in app.lists for i in e["items"] if i.get("reminder")} == {"fixed","relative"}
            assert not app.settings["system_notifications"]
            assert app.settings["pinned_pages"] and app.settings["saved_filters"]
            assert app.day_close_queue(today=manifest["bearbeitungstag"])
            # Alle Dokumentarten real anzeigen; auf macOS müssen Originalmotive Vorschauen bekommen.
            for title, filename in [(briefing["title"],"01_Briefing"), (gallery["title"],"02_Galerie"),
                ("Abstimmung · Entwurf 02","03_Protokoll"), ("Quartier · Pixelskizze","04_Zeichnung")]:
                app.set_active_list(lists[title]["id"])
                settle(root, .65)
                if title == briefing["title"]:
                    editor = app.rich_note_editor
                    assert len(editor.images) == 3
                    assert {info["mode"] for info in editor.images.values()} == {"left","right","center"}
                    if sys.platform == "darwin":
                        assert all(v._photo is not None for v in editor._image_views.values())
                    closed = editor.text.tag_ranges("toggle_closed")
                    assert closed and editor.text.tag_ranges("folded")
                    assert editor.set_toggle_open(str(closed[0]), True)
                    assert not editor.text.tag_ranges("folded")
                    assert editor.set_toggle_open(str(closed[0]), False)
                    editor.flush()
                if title == gallery["title"] and sys.platform == "darwin":
                    assert {key[0] for key in app.gallery_view._images} == {a["storage"] for a in gallery["attachments"]}
                photo(images, filename)
            project = next(f for f in app.folders if f["title"] == "Showcase · Parkquartier")
            app.set_active_folder(project["id"])
            settle(root)
            assert app.workspace.mode == "board" and len(app.workspace.board()["cards"]) == 5
            photo(images, "05_Projektpinnwand")
            app.set_active_list(main["id"])
            settle(root)
            assert app.workspace.board()["layout"] == "columns"
            photo(images, "06_Bearbeitungstage")
            app.workspace.set_mode("list")
            settle(root)
            candidate = next(i for i in main["items"] if i["text"] == "Objektsteckbrief bestätigen")
            original = copy.deepcopy(candidate)
            app.tree.selection_set(candidate["id"])
            app.toggle_done()
            settle(root)
            assert app.find_item(candidate["id"])[0]["done"]
            app.undo_last_change()
            settle(root)
            assert app.find_item(candidate["id"])[0] == original
            # Vorlage mit tatsächlicher Abfrage nur des Projektfeldes, inklusive Anhang.
            template = next(t for t in app.templates if t["title"] == "{{Wochentag}} KW {{KW}} · {{Projekt}}")
            asked = []
            app.ask_template_fields = lambda fields, title="": (asked.append(fields), {"Projekt":"Demo"})[1]
            count = len(app.lists)
            previous_ids = {entry["id"] for entry in app.lists}
            app.create_list_from_template(template["id"])
            settle(root)
            assert asked == [["Projekt"]] and len(app.lists) == count+1
            created = next(entry for entry in app.lists if entry["id"] not in previous_ids)
            assert "{{" not in created["title"] and created["list_kind"] == "note" and created["attachments"]
            # Auf Basisbestand zurücksetzen, dann speichern/exportieren und separaten Prozess starten.
            assert app.restore_app_backup(str(fixture/"Glide-Showcase_App.glideapp"),
                sections={"tasks":True,"settings":True,"templates":True,"activity":True}, show_success=False)
            settle(root)
            app.hide_undo_toast()
            app._open_home_mode("tiles")
            settle(root)
            photo(images,"07_Startseite")
            app.start_day_close()
            settle(root)
            assert app.home_mode() == "day_close"
            photo(images,"08_Tagesabschluss")
            app.set_active_list(briefing["id"])
            for geometry in ("1040x760+20+30", "1440x960+20+30"):
                root.geometry(geometry)
                settle(root)
            app.save_items()
            app.save_settings()
            roundtrip = Path(temporary)/"roundtrip.glideapp"
            app.write_complete_backup(str(roundtrip), app.app_backup_payload())
            with zipfile.ZipFile(roundtrip) as archive:
                assert archive.testzip() is None
            assert not errors, errors
            root.destroy()
            root = None
            child = subprocess.run([sys.executable,"-B",__file__,"--fixture",str(fixture),"--neustart",temporary],
                                   capture_output=True,text=True,timeout=90)
            assert child.returncode == 0, child.stdout+child.stderr
            print(child.stdout.strip())
            print("Showcase: Import, ID-Verweise, 5 Dokumentarten, 3 Ordnertypen, 6 Originalmotive, 3 Seitenbilder, "
                  "2 Pinnwände, Klappblock, Termine, Erinnerungen, Undo, Vorlagen, Export und Neustart: ok")
        finally:
            if root is not None:
                root.destroy()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture",type=Path,default=FIXTURE)
    parser.add_argument("--bilder",type=Path)
    parser.add_argument("--neustart",type=Path)
    args = parser.parse_args()
    check(args.fixture.resolve(),args.bilder,args.neustart)


if __name__ == "__main__":
    main()
