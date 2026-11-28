# SPDX-License-Identifier: MPL-2.0
"""Teil 05B mit echtem Tk und künstlichen Daten.

Sicherheitsübersicht (Bento, echte Werte, „nicht geprüft“), Integritätsprüfung
im Hintergrund mit fehlendem und verwaistem Anhang, Sicherung prüfen (gültig
und beschädigt), Leseposition über Neustart mit Kapitelanker und Vorrang des
ausdrücklichen Ziels, Checklisten- und Kapitelgriff, Anzeigeort per Ziehen mit
Modifikator, negative Archivfälle und abgebrochener Import.
"""
import argparse
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import types
import zipfile

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))

with tempfile.TemporaryDirectory(prefix="glide-05b-", ignore_cleanup_errors=True) as directory:
    os.environ["GLIDE_DATA_DIR"] = directory
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_05b", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    fehler, infos = [], []

    def oeffnen():
        root = mod.tk.Tk()
        root.geometry("1200x800+20+20")
        root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
        app = mod.ListApp(root)
        app.show_error = lambda *a, **k: fehler.append(("error",) + a)
        app.show_warning = lambda *a, **k: fehler.append(("warning",) + a)
        app.show_info = lambda *a, **k: infos.append(a)
        app.ask_yes_no = lambda *a, **k: True
        return root, app

    def ruhe(root, s=0.3):
        frist = time.monotonic() + s
        while time.monotonic() < frist:
            root.update()
            time.sleep(0.01)

    root, app = oeffnen()
    pruefungen = []

    # --- Bestand -----------------------------------------------------------
    zeilen, spans, pos = [], [], 0
    for nr in range(1, 4):
        titel = f"Kapitel {nr}"
        spans.append({"tag": "h1", "start": pos, "end": pos + len(titel) + 1})
        zeilen.append(titel)
        pos += len(titel) + 1
        for z in range(60):
            text = f"Zeile {nr}.{z} mit etwas Text"
            zeilen.append(text)
            pos += len(text) + 1
    seite = app.new_list_object("Lange Seite", [], list_kind="page",
                                rich_note={"text": "\n".join(zeilen) + "\n", "spans": spans, "links": {}})
    ordner = app.new_folder_object("Projekt")
    app.folders.append(ordner)
    aufgabe = app.new_item("Mit Schritten")
    aufgabe["checklist"] = [{"text": "Erster", "done": False}, {"text": "Zweiter", "done": False}]
    liste = app.new_list_object("Arbeit", [aufgabe])
    app.lists.extend([seite, liste])
    assert app.save_items()

    # --- Checklistengriff ----------------------------------------------------
    app.settings["list_detail_mode"] = "checklist"
    app.set_active_list(liste["id"])
    app.refresh_tree()
    ruhe(root)
    app.show_quick_plan_row()
    ruhe(root)
    schritt_iid = f"{aufgabe['id']}{app.CHECKLIST_IID_MARKER}0"
    assert app.tree.exists(schritt_iid), app.tree.get_children(aufgabe["id"])
    griffe = [b for b in app._row_action_buttons if getattr(b, "_row_owner", None) == schritt_iid
              and b.winfo_manager() == "place"]
    assert griffe and griffe[0]._checklist_step == 0, "kein Griff an der Checklistenzeile"
    aufgabengriff = next(b for b in app._row_action_buttons if b._row_owner == aufgabe["id"])
    assert griffe[0].winfo_rootx() == aufgabengriff.winfo_rootx(), "Griffachse"
    menu = app.build_checklist_step_menu(schritt_iid)
    labels = [menu.entrycget(i, "label") for i in range(menu.index("end") + 1)]
    assert labels[1:] == ["Schritt nach oben", "Schritt nach unten"] and menu.entrycget(1, "state") == "disabled"
    assert app.move_checklist_row(schritt_iid, 1)
    assert [c["text"] for c in app.find_item(aufgabe["id"])[0]["checklist"]] == ["Zweiter", "Erster"]
    app.undo_last_change()
    ruhe(root)
    assert [c["text"] for c in app.find_item(aufgabe["id"])[0]["checklist"]] == ["Erster", "Zweiter"]
    assert app.toggle_checklist_row(schritt_iid)
    assert app.find_item(aufgabe["id"])[0]["checklist"][0]["done"] is True
    pruefungen.append("Checklistengriff: gleiche Achse, Menü, Verschieben mit Rückgängig, Abhaken")

    # --- Kapitelgriff ---------------------------------------------------------
    app.set_active_list(seite["id"])
    ruhe(root, 0.5)
    editor = app.rich_note_editor
    kapitel = app.chapter_outline(app.page_entry(seite["id"]))
    assert len(kapitel) == 3 and all(len(k.key) == 32 for k in kapitel)
    assert editor.chapter_at_line(kapitel[1].line).key == kapitel[1].key
    assert editor.chapter_at_line(kapitel[1].line + 1) is None
    gezeigt = []
    original_popup = mod.tk.Menu.tk_popup
    mod.tk.Menu.tk_popup = lambda self, *a, **k: gezeigt.append(self)
    editor._block_handle_line = kapitel[1].line
    editor.block_handle_click()
    mod.tk.Menu.tk_popup = original_popup
    assert gezeigt, "Kapitelmenü nicht gezeigt"
    eintraege = [gezeigt[-1].entrycget(i, "label") for i in range(gezeigt[-1].index("end") + 1)
                 if gezeigt[-1].type(i) == "command"]
    assert eintraege[-1] == "Blockaktionen …" and any("Umbenennen" in e for e in eintraege), eintraege
    pruefungen.append("Kapitelgriff: Kapitelaktionen plus Blockaktionen")

    # --- Leseposition über Neustart --------------------------------------------
    ziel = kapitel[1].start + 40
    editor.text.yview(f"1.0 +{ziel}c")
    editor.text.mark_set("insert", f"1.0 +{ziel + 5}c")
    ruhe(root)
    app.on_close()
    gespeichert = json.loads(Path(directory, "view_positions.json").read_text(encoding="utf-8"))
    eintrag = next(e for e in gespeichert["entries"] if e["key"] == ["page", seite["id"]])
    assert eintrag["position"]["anchor"] == kapitel[1].key, eintrag
    # Vor dem Neustart Text vor Kapitel 2 einfügen (andere Länge, andere Versätze).
    daten = json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
    s = next(e for e in daten["lists"] if e["id"] == seite["id"])
    vorspann = "Neu eingefügt\n" * 30
    s["rich_note"]["text"] = vorspann + s["rich_note"]["text"]
    for span in s["rich_note"]["spans"]:
        span["start"] += len(vorspann)
        span["end"] += len(vorspann)
    Path(mod.SAVE_FILE).write_text(json.dumps(daten, ensure_ascii=False), encoding="utf-8")
    root, app = oeffnen()
    app.set_active_list(seite["id"])
    ruhe(root, 0.6)
    editor = app.rich_note_editor
    oben = editor.offset(editor.text.index("@0,0"))
    neu = [k for k in app.chapter_outline(app.page_entry(seite["id"])) if k.key == kapitel[1].key][0]
    assert neu.start <= oben < neu.section_end, (oben, neu.start, neu.section_end)
    assert editor.offset(editor.text.index("insert")) == neu.start + 45
    # Ausdrückliches Ziel hat Vorrang.
    app.open_chapter(seite["id"], kapitel[2].key)
    ruhe(root, 0.4)
    assert editor.text.index("insert").split(".")[0] == str(app.chapter_outline(app.page_entry(seite["id"]))[2].line)
    pruefungen.append("Leseposition: Anker über Neustart trotz eingefügtem Text, ausdrückliches Ziel vorrangig")

    # --- Anzeigeort per Ziehen (NAV-04) ----------------------------------------
    app.update_sidebar_list()
    ruhe(root)
    folder_iid = f"folder:{ordner['id']}"
    baum = app.sidebar_listbox
    app.sidebar_drag_start_iid = f"list:{seite['id']}"
    app.sidebar_drag_has_moved = True
    app.sidebar_drag_destination = lambda _e: (baum, folder_iid, ("folder", ordner["id"]), None)
    mit = types.SimpleNamespace(state=app.NAV_MODIFIER_MASK, x=5, y=5, x_root=100, y_root=100, widget=baum)
    ohne = types.SimpleNamespace(state=0, x=5, y=5, x_root=100, y_root=100, widget=baum)
    assert "Nur anzeigen" in app.sidebar_drop_hint_text(mit, ("list", seite["id"]), ("folder", ordner["id"]), "into")
    assert "Verschieben" in app.sidebar_drop_hint_text(ohne, ("list", seite["id"]), ("folder", ordner["id"]), "into")
    app.on_sidebar_drag_end(mit)
    ruhe(root)
    eintrag = app.page_entry(seite["id"])
    assert eintrag.get("nav_parent_id") == ordner["id"] and eintrag.get("folder_id") is None, eintrag.get("nav_parent_id")
    assert eintrag["list_kind"] == "page"
    app.undo_last_change()
    ruhe(root)
    assert "nav_parent_id" not in app.page_entry(seite["id"])
    del app.sidebar_drag_destination
    pruefungen.append("Anzeigeort per Ziehen mit Modifikator, Hinweis vorab, Rückgängig")

    # --- Sicherheitsübersicht --------------------------------------------------
    quelle = Path(tempfile.mkdtemp(prefix="glide-05b-quelle-")) / "anhang-05b.bin"
    quelle.write_bytes(b"inhalt")
    anhang = app.store_attachment(str(quelle), "anhang-05b.bin")
    app.page_entry(seite["id"]).setdefault("attachments", []).append(anhang)
    geisterliste = app.new_list_object("Geist", [], attachments=[dict(anhang, storage="attachments/weg_geist.bin", id="g" * 32)])
    app.lists.append(geisterliste)
    assert app.save_items()
    Path(directory, "attachments", "verwaist.bin").write_bytes(b"?")
    dialog = app.show_data_safety_overview()
    ruhe(root)
    texte = []

    def sammeln(w):
        try:
            texte.append(str(w.cget("text")))
        except Exception:
            pass
        for k in w.winfo_children():
            sammeln(k)
    sammeln(dialog)
    gesamt = "\n".join(texte)
    for erwartet in ("Daten und Sicherheit", "Format 27", "nicht geprüft", "Wiederherstellungsprobe dieses Arbeitsbereichs: nicht durchgeführt",
                     "Datenübertragung: keine automatische"):
        assert erwartet in gesamt, erwartet
    def alle(w):
        yield w
        for k in w.winfo_children():
            yield from alle(k)
    karten = [w for w in alle(dialog) if isinstance(w, mod.glide_bento.BentoCard)]
    assert len(karten) == 3, karten
    fertig = []
    app.run_data_integrity_check(on_done=fertig.append)
    frist = time.monotonic() + 20
    while not fertig and time.monotonic() < frist:
        ruhe(root, 0.1)
    assert fertig, "Integritätsprüfung nicht fertig"
    wert = fertig[0]
    assert not wert["ok"] and wert["missing"] == 1 and wert["unreferenced"] == 1 and wert["schema_ok"], wert
    assert Path(directory, "attachments", "verwaist.bin").is_file(), "verwaiste Datei gelöscht"
    app._data_safety_rebuild()  # wie nach dem Knopf „Integrität prüfen“
    ruhe(root, 0.3)
    texte.clear()
    sammeln(dialog)
    assert any("Fehlt: attachments/weg_geist.bin" in t for t in texte), texte
    # Sicherung prüfen: gültig und beschädigt.
    ablage = Path(tempfile.mkdtemp(prefix="glide-05b-ablage-"))
    gut = ablage / "gut-05b.glideapp"
    try:
        app.write_complete_backup(str(gut), app.app_backup_payload())
        raise AssertionError("Sicherung mit fehlendem Anhang als erfolgreich erstellt")
    except FileNotFoundError:
        assert not gut.exists(), "unvollständige Sicherung liegt herum"
    app.lists = [e for e in app.lists if e["id"] != geisterliste["id"]]
    assert app.save_items()
    app.write_complete_backup(str(gut), app.app_backup_payload())
    assert app.verify_backup_file(str(gut))[0] is True
    kaputt = ablage / "kaputt-05b.glideapp"
    kaputt.write_bytes(gut.read_bytes()[:200])
    ok, detail = app.verify_backup_file(str(kaputt))
    assert ok is False and detail
    assert app.data_status_file().get("backup_check")["ok"] is False
    dialog.destroy()
    pruefungen.append("Sicherheitsübersicht: drei Bento-Karten, echte Werte, Integrität im Hintergrund, Sicherungsprüfung")

    # --- Archiv-Negativfälle ---------------------------------------------------
    def archiv(name, eintraege, symlink=None):
        pfad = ablage / name
        with zipfile.ZipFile(pfad, "w") as z:
            for n, inhalt in eintraege:
                z.writestr(n, inhalt)
            if symlink:
                info = zipfile.ZipInfo(symlink)
                info.external_attr = (0o120777 << 16)
                z.writestr(info, "ziel")
        return pfad
    daten_json = json.dumps(app.complete_backup_payload())
    faelle = {
        "pfad_hoch": [("data.json", daten_json), ("attachments/../settings.json", "x")],
        "absolut": [("data.json", daten_json), ("/etc/passwd", "x")],
        "laufwerk": [("data.json", daten_json), ("C:/Windows/x.txt", "x")],
        "fremder_ordner": [("data.json", daten_json), ("skripte/run.py", "print(1)")],
        "ohne_daten": [("attachments/a.bin", "x")],
    }
    for name, inhalt in faelle.items():
        with zipfile.ZipFile(archiv(name + ".glidebackup", inhalt)) as z:
            try:
                app.inspect_backup_archive(z)
                abgelehnt = False
            except (ValueError, OSError):
                abgelehnt = True
        assert abgelehnt, name
    with zipfile.ZipFile(archiv("symlink.glidebackup", [("data.json", daten_json)], symlink="attachments/link")) as z:
        try:
            app.inspect_backup_archive(z)
            raise AssertionError("Symlink angenommen")
        except ValueError:
            pass
    zukunft = json.loads(daten_json)
    zukunft["version"] = 99
    try:
        app.validate_backup_schema(zukunft, portable=True)
        raise AssertionError("Format 99 angenommen")
    except ValueError:
        pass
    pruefungen.append("Archive: Pfad nach oben, absolut, Laufwerk, fremder Ordner, ohne data.json, Symlink, Format 99 abgelehnt")

    # --- Abgebrochener Import --------------------------------------------------
    vorher = Path(mod.SAVE_FILE).read_bytes()
    listen_vorher = [e["id"] for e in app.lists]
    original = app.copy_zip_member_limited
    app.copy_zip_member_limited = lambda *a, **k: (_ for _ in ()).throw(OSError("simulierter Abbruch beim Entpacken"))
    fehler.clear()
    app.import_full_backup(path=str(gut), show_success=False, confirm=False)
    app.copy_zip_member_limited = original
    assert Path(mod.SAVE_FILE).read_bytes() == vorher, "abgebrochener Import änderte die Datei"
    assert [e["id"] for e in app.lists] == listen_vorher
    assert not [n for n in os.listdir(directory) if n.startswith(".glide-import-")], os.listdir(directory)
    fehler.clear()
    pruefungen.append("Abgebrochener Import: Datei und Bestand unverändert, keine Zwischenordner")

    app.on_close()
    assert not fehler, fehler
print("test_teil05b_bedienung: OK\n  " + "\n  ".join(pruefungen))
