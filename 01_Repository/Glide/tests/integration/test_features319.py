"""Änderungsverlauf: Migration, erfasste Vorgänge, Grenzen, Backups, Filter, Dialog."""
import copy
import importlib.machinery
import importlib.util
import json
import os
import tempfile
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


with tempfile.TemporaryDirectory(prefix="glide-features319-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features319", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    callbacks = []
    root.report_callback_exception = lambda *args: callbacks.append(args)
    app = mod.ListApp(root)
    meldungen = []
    app.show_warning = app.show_error = lambda *args, **kwargs: meldungen.append(args)
    infos = []
    app.show_info = lambda *args, **kwargs: infos.append(args)
    app.ask_yes_no = lambda *args, **kwargs: True
    A = mod.ListApp

    def vorgaenge(kind=None, action=None):
        """Verlaufseinträge als (Art, Vorgang, Objekt)-Tripel, optional gefiltert."""
        return [(e["kind"], e["action"], e["target"]) for e in app.history
                if (kind is None or e["kind"] == kind) and (action is None or e["action"] == action)]

    def letzte(anzahl=1):
        return app.history[-anzahl:]

    try:
        assert A.DATA_SCHEMA_VERSION == 23
        assert A.MAX_HISTORY_ENTRIES == 15 and A.HISTORY_GROUP_THRESHOLD == 25

        # --- 1. Migration von Format 14 --------------------------------------
        liste = app.new_list_object("Verlaufsprobe", [])
        app.lists.append(liste)
        app.set_active_list(liste["id"])
        assert app.save_items()
        alt = json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
        alt["version"] = 14
        alt.pop("history", None)
        original = json.dumps(alt, ensure_ascii=False).encode()
        Path(mod.SAVE_FILE).write_bytes(original)
        app._schema15_backup_checked = False
        app.load_items()
        assert app.history == [], "Ein Bestand ohne Verlauf startet mit leerem Protokoll."
        assert app.save_items()
        sicherungen = list(Path(mod.BACKUP_DIR).glob("liste_vor_format15_*.json"))
        assert len(sicherungen) == 1 and sicherungen[0].read_bytes() == original
        gespeichert = json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
        assert gespeichert["version"] == 23 and gespeichert["history"] == []
        assert app.save_items() and len(list(Path(mod.BACKUP_DIR).glob("liste_vor_format15_*.json"))) == 1
        # Das Laden selbst ist keine Änderung.
        assert app.history == [], app.history
        liste = next(entry for entry in app.lists if entry["title"] == "Verlaufsprobe")
        app.set_active_list(liste["id"])

        # --- 2. Punktvorgänge einzeln ----------------------------------------
        punkt = app.new_item("Angebot schreiben")
        app.items.append(punkt)
        assert app.save_items()
        assert vorgaenge("item", "created") == [("item", "created", "Angebot schreiben")]
        assert letzte()[0]["list"] == "Verlaufsprobe"

        punkt["done"] = True
        assert app.save_items()
        assert letzte()[0]["action"] == "done"
        punkt["done"] = False
        assert app.save_items()
        assert letzte()[0]["action"] == "reopened"

        punkt["due"] = "2026-10-01"
        punkt["importance"] = 3
        punkt["estimated_minutes"] = 45
        assert app.save_items()
        eintrag = letzte()[0]
        assert eintrag["action"] == "updated"
        assert set(eintrag["fields"]) == {"Wichtigkeit", "Fälligkeit", "Aufwand"}, eintrag

        punkt["text"] = "Angebot schreiben und senden"
        assert app.save_items()
        assert letzte()[0]["fields"] == ["Text"]
        assert letzte()[0]["target"] == "Angebot schreiben und senden"

        # Beschreibung wird als Änderung erfasst, ihr Inhalt nicht gespeichert.
        punkt["description"] = "Vertraulicher Innentext"
        assert app.save_items()
        assert letzte()[0]["fields"] == ["Beschreibung"]
        assert "Vertraulicher" not in json.dumps(app.history, ensure_ascii=False)

        # Ohne Änderung entsteht kein Eintrag.
        anzahl = len(app.history)
        assert app.save_items() and len(app.history) == anzahl

        # --- 3. Verschieben in drei Varianten --------------------------------
        gruppe = app.new_item("Sammelmappe", kind=A.ITEM_KIND_GROUP)
        app.items.append(gruppe)
        assert app.save_items()
        app.items.remove(punkt)
        gruppe["children"] = [punkt]
        assert app.save_items()
        assert letzte()[0]["action"] == "moved", letzte()

        zweite = app.new_list_object("Zweite Liste", [])
        app.lists.append(zweite)
        assert app.save_items()
        assert letzte()[0] == {**letzte()[0], "kind": "list", "action": "created"}
        gruppe["children"] = []
        zweite["items"].append(punkt)
        assert app.save_items()
        umzug = letzte()[0]
        assert umzug["action"] == "moved" and umzug["list"] == "Zweite Liste"

        ordner = app.new_folder_object("Projekte", color="accent")
        app.folders.append(ordner)
        assert app.save_items()
        assert letzte()[0]["kind"] == "folder" and letzte()[0]["action"] == "created"
        zweite["folder_id"] = ordner["id"]
        assert app.save_items()
        assert letzte()[0]["kind"] == "list" and letzte()[0]["action"] == "moved"
        zweite["title"] = "Zweite Wohnung"
        assert app.save_items()
        assert letzte()[0] == {**letzte()[0], "kind": "list", "action": "renamed",
                               "target": "Zweite Wohnung"}
        ordner["title"] = "Objekte"
        assert app.save_items()
        assert letzte()[0]["kind"] == "folder" and letzte()[0]["action"] == "renamed"

        # --- 4. Papierkorb: drei verschiedene Vorgänge -----------------------
        app.set_active_list(zweite["id"])
        app.move_item_to_trash(punkt["id"])
        assert app.save_items()
        assert letzte()[0]["action"] == "trashed" and letzte()[0]["kind"] == "item"
        eintrag = next(e for e in app.trash if e.get("kind") == A.TRASH_KIND_ITEM)
        app.restore_trash_entry(eintrag["id"])
        assert app.save_items()
        assert letzte()[0]["action"] == "restored", letzte()
        app.move_item_to_trash(punkt["id"])
        assert app.save_items()
        eintrag = next(e for e in app.trash if e.get("kind") == A.TRASH_KIND_ITEM)
        app.trash = [e for e in app.trash if e.get("id") != eintrag["id"]]
        assert app.save_items()
        assert letzte()[0]["action"] == "purged", letzte()

        # Eine gelöschte Liste meldet sich selbst – nicht jeder ihrer Punkte.
        voll = app.new_list_object("Wird gelöscht", [app.new_item(f"Punkt {n}") for n in range(8)])
        app.lists.append(voll)
        assert app.save_items()
        vor_loeschung = {e["id"] for e in app.history}
        app.trash.insert(0, app.new_trash_entry(A.TRASH_KIND_LIST, copy.deepcopy(voll)))
        app.lists = [entry for entry in app.lists if entry["id"] != voll["id"]]
        app.set_active_list(liste["id"])
        assert app.save_items()
        neu_dazu = [e for e in app.history if e["id"] not in vor_loeschung]
        assert [e["action"] for e in neu_dazu] == ["trashed"], neu_dazu
        assert neu_dazu[0]["kind"] == "list" and neu_dazu[0]["target"] == "Wird gelöscht"

        # --- 5. Sammeleinträge ------------------------------------------------
        vor_masse = {e["id"] for e in app.history}
        masse = app.new_list_object("Massenprobe", [app.new_item(f"Zeile {n}") for n in range(60)])
        app.lists.append(masse)
        assert app.save_items()
        neu_dazu = [e for e in app.history if e["id"] not in vor_masse]
        sammel = [e for e in neu_dazu if e.get("count")]
        assert len(sammel) == 1 and sammel[0]["count"] == 60, neu_dazu
        assert sammel[0]["kind"] == "item" and sammel[0]["action"] == "created"
        assert "60" in sammel[0]["target"]
        assert len([e for e in neu_dazu if e["kind"] == "item" and not e.get("count")]) == 0
        # Unterhalb der Schwelle bleibt jedes Ereignis einzeln stehen.
        vor_wenig = {e["id"] for e in app.history}
        wenig = app.new_list_object("Wenige", [app.new_item(f"Kurz {n}") for n in range(5)])
        app.lists.append(wenig)
        assert app.save_items()
        neu_dazu = [e for e in app.history if e["id"] not in vor_wenig]
        assert len([e for e in neu_dazu if e["kind"] == "item"]) == 5

        # --- 6. Obergrenze ----------------------------------------------------
        app.history = [{"id": f"alt{n}", "at": datetime.now().isoformat(timespec="seconds"), "kind": "item",
                        "action": "created", "target": f"Alt {n}", "list": ""}
                       for n in range(A.MAX_HISTORY_ENTRIES)]
        app.items.append(app.new_item("Ein Punkt über der Grenze"))
        assert app.save_items()
        assert len(app.history) == A.MAX_HISTORY_ENTRIES
        assert app.history[-1]["target"] == "Ein Punkt über der Grenze"
        assert app.history[0]["target"] != "Alt 0", "Die ältesten Einträge fallen weg."
        app.history = []
        assert app.save_items()

        # --- 7. Defekte und fremde Verlaufsfelder ----------------------------
        assert A.normalize_history_entries("kaputt") == []
        assert A.normalize_history_entries([{"kind": "unbekannt", "action": "created", "at": datetime.now().isoformat(timespec="seconds")}]) == []
        assert A.normalize_history_entries([{"kind": "item", "action": "erfunden", "at": datetime.now().isoformat(timespec="seconds")}]) == []
        assert A.normalize_history_entries([{"kind": "item", "action": "created"}]) == []
        gekuerzt = A.normalize_history_entries([{"kind": "item", "action": "created",
                                                 "at": datetime.now().isoformat(timespec="seconds"), "target": "x" * 400}])
        assert len(gekuerzt) == 1 and len(gekuerzt[0]["target"]) == A.HISTORY_TARGET_MAX_LENGTH
        zu_viele = A.normalize_history_entries([{"kind": "item", "action": "created",
                                                 "at": datetime.now().isoformat(timespec="seconds"), "target": str(n)}
                                                for n in range(A.MAX_HISTORY_ENTRIES + 50)])
        assert len(zu_viele) == A.MAX_HISTORY_ENTRIES
        kaputt = json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
        kaputt["history"] = {"nicht": "eine Liste"}
        Path(mod.SAVE_FILE).write_text(json.dumps(kaputt, ensure_ascii=False), encoding="utf-8")
        app.load_items()
        assert app.history == [] and app.lists, "Ein defektes Protokoll lässt die Aufgaben unberührt."
        liste = next(entry for entry in app.lists if entry["title"] == "Verlaufsprobe")
        app.set_active_list(liste["id"])

        # --- 8. Backups tragen den Verlauf ------------------------------------
        app.items.append(app.new_item("Vor dem Backup"))
        assert app.save_items()
        merker = copy.deepcopy(app.history)
        assert merker
        archiv = os.path.join(folder, "voll.glidebackup")
        app.write_complete_backup(archiv, app.complete_backup_payload())
        inhalt = json.loads(zipfile.ZipFile(archiv).read("data.json"))
        assert len(inhalt["history"]) == len(merker), "Das Komplettbackup führt den Verlauf mit."
        app.history = []
        assert app.save_items()
        assert app.import_full_backup(path=archiv, show_success=False, confirm=False)
        assert len(app.history) == min(A.MAX_HISTORY_ENTRIES, len(merker) + 2), app.history[-3:]
        assert app.history[-2]["action"] == "replaced"
        assert app.history[-1]["kind"] == "data" and app.history[-1]["action"] == "imported"
        assert "voll.glidebackup" in app.history[-1]["target"]
        # Ein Teilbackup ist ein Auszug und trägt kein Protokoll.
        teil = os.path.join(folder, "teil.glidebackup")
        auszug = app.new_list_object("Auszug", [app.new_item("Aus dem Auszug")])
        app.lists.append(auszug)
        assert app.save_items()
        app.write_complete_backup(teil, app.partial_backup_payload([auszug["id"]], []))
        assert "history" not in json.loads(zipfile.ZipFile(teil).read("data.json"))
        # Hinzufügen ersetzt den Bestand nicht: Das eigene Protokoll bleibt
        # vollständig stehen und es entsteht kein „Bestand ersetzt".
        bestand_vorher = copy.deepcopy(app.history)
        assert bestand_vorher
        kennungen = {e["id"] for e in bestand_vorher}
        assert app.import_full_backup(additive=True, path=teil, show_success=False, confirm=False)
        assert app.history[-1]["id"] not in kennungen, "Der Import wird erfasst; ältere Einträge unterliegen der Grenze."
        assert all(e["action"] != "replaced" for e in app.history
                   if e["id"] not in kennungen), [e for e in app.history if e["id"] not in kennungen]
        liste = next((entry for entry in app.lists if entry["title"] == "Verlaufsprobe"), app.lists[0])
        app.set_active_list(liste["id"])

        # --- 9. Abschaltbar und leerbar ---------------------------------------
        app.settings["history_enabled"] = False
        assert app.save_settings()
        assert not app.history_enabled()
        bestand = copy.deepcopy(app.history)
        app.items.append(app.new_item("Ohne Protokoll"))
        assert app.save_items()
        assert app.history == bestand, "Ausgeschaltet entstehen keine neuen Einträge."
        app.settings["history_enabled"] = True
        assert app.save_settings() and app.history_enabled()
        app.items.append(app.new_item("Wieder mit Protokoll"))
        assert app.save_items()
        assert app.history[-1]["target"] == "Wieder mit Protokoll"
        punkte_vorher = app.count_items(app.items, include_groups=True)
        listen_vorher = len(app.lists)
        entfernt = app.clear_history()
        assert entfernt and app.history == []
        assert json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))["history"] == []
        assert app.count_items(app.items, include_groups=True) == punkte_vorher
        assert len(app.lists) == listen_vorher, "Leeren lässt den Bestand unverändert."
        app.items.append(app.new_item("Nach dem Leeren"))
        assert app.save_items()
        assert [e["target"] for e in app.history] == ["Nach dem Leeren"]

        # --- 10. Suche, Zeitraum, Art -----------------------------------------
        # Chronologisch aufsteigend gespeichert – die Ansicht dreht sie um.
        app.history = [
            {"id": "d", "at": (datetime.now() - timedelta(days=60)).isoformat(timespec="seconds"),
             "kind": "folder", "action": "created", "target": "Uralt", "list": ""},
            {"id": "c", "at": (datetime.now() - timedelta(days=12)).isoformat(timespec="seconds"),
             "kind": "item", "action": "trashed", "target": "Weggeworfen", "list": "Verlaufsprobe"},
            {"id": "b", "at": (datetime.now() - timedelta(days=3)).isoformat(timespec="seconds"),
             "kind": "list", "action": "renamed", "target": "Alte Liste", "list": ""},
            {"id": "a", "at": datetime.now().isoformat(timespec="seconds"), "kind": "item",
             "action": "created", "target": "Heutiger Punkt", "list": "Verlaufsprobe"},
        ]
        assert [e["id"] for e in app.filtered_history()] == ["a", "b", "c"], "Neueste zuerst."
        assert [e["id"] for e in app.filtered_history(zeitraum="today")] == ["a"]
        assert {e["id"] for e in app.filtered_history(zeitraum="7")} == {"a", "b"}
        assert {e["id"] for e in app.filtered_history(zeitraum="30")} == {"a", "b", "c"}
        assert {e["id"] for e in app.filtered_history(art="item")} == {"a", "c"}
        assert {e["id"] for e in app.filtered_history(art="container")} == {"b"}
        assert {e["id"] for e in app.filtered_history(art="trash")} == {"c"}
        assert [e["id"] for e in app.filtered_history("weggeworfen")] == ["c"]
        assert [e["id"] for e in app.filtered_history("umbenannt")] == ["b"]
        assert [e["id"] for e in app.filtered_history("Verlaufsprobe", zeitraum="today")] == ["a"]
        assert app.filtered_history("gibtesnicht") == []
        assert "Heutiger Punkt" in app.history_entry_line(app.history[-1])

        # --- 11. Dialog in Hell und Dunkel ------------------------------------
        root.deiconify()
        root.geometry("1100x780+10+10")
        for theme in ("light", "dark"):
            app.set_design(theme, apply_now=False)
            app.apply_theme()
            gesehen = {}

            def ansehen(dialog, parent=None):
                dialog.geometry("780x640")
                dialog.update()
                widgets = list(descendants(dialog))
                baum = next(w for w in widgets if w.winfo_name() == "history_tree")
                suchfeld = next(w for w in widgets if w.winfo_name() == "history_search")
                gesehen["zeilen"] = len(baum.get_children())
                suchfeld.insert(0, "Weggeworfen")
                dialog.update()
                gesehen["gefiltert"] = len(baum.get_children())
                knopf = next(w for w in widgets if isinstance(w, mod.RoundedButton)
                             and w.text == "Als TXT speichern")
                assert knopf.winfo_ismapped()
                assert (knopf.winfo_rooty() + knopf.winfo_height()
                        <= dialog.winfo_rooty() + dialog.winfo_height())
                next(w for w in widgets if isinstance(w, mod.RoundedButton)
                     and w.text == "Schließen").command()
            app.run_modal = ansehen
            zustand = copy.deepcopy(app.data_payload())
            assert app.show_history_dialog() == "break"
            assert gesehen["zeilen"] == 3 and gesehen["gefiltert"] == 1, gesehen
            assert app.data_payload() == zustand, "Ansehen ändert nichts."

            # Ausgabe als Textdatei über den Dialog.
            ziel = os.path.join(folder, f"verlauf_{theme}.txt")
            mod.filedialog.asksaveasfilename = lambda *args, **kwargs: ziel

            def speichern(dialog, parent=None):
                dialog.update()
                next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)
                     and w.text == "Als TXT speichern").command()
                next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)
                     and w.text == "Schließen").command()
            app.run_modal = speichern
            app.show_history_dialog()
            text = Path(ziel).read_text(encoding="utf-8")
            assert "Änderungsverlauf" in text and "Heutiger Punkt" in text and "Uralt" not in text

            # Leeren über den Dialog.
            def leeren(dialog, parent=None):
                dialog.update()
                next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)
                     and w.text == "Verlauf leeren").command()
                next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)
                     and w.text == "Schließen").command()
            app.run_modal = leeren
            listen_vorher = len(app.lists)
            app.show_history_dialog()
            assert app.history == [] and len(app.lists) == listen_vorher
            # Für den zweiten Theme-Durchlauf dieselben vier Einträge wieder herstellen.
            app.history = [
                {"id": "d3", "at": (datetime.now() - timedelta(days=60)).isoformat(timespec="seconds"),
                 "kind": "folder", "action": "created", "target": "Uralt", "list": ""},
                {"id": "c3", "at": (datetime.now() - timedelta(days=12)).isoformat(timespec="seconds"),
                 "kind": "item", "action": "trashed", "target": "Weggeworfen", "list": "Verlaufsprobe"},
                {"id": "b3", "at": (datetime.now() - timedelta(days=3)).isoformat(timespec="seconds"),
                 "kind": "list", "action": "renamed", "target": "Alte Liste", "list": ""},
                {"id": "a3", "at": datetime.now().isoformat(timespec="seconds"), "kind": "item",
                 "action": "created", "target": "Heutiger Punkt", "list": "Verlaufsprobe"},
            ]

        # --- 12. Nutzdatendatei ist kein Ausgabeziel ---------------------------
        try:
            app.validate_backup_target(mod.SAVE_FILE)
        except ValueError:
            pass
        else:
            raise AssertionError("Die Nutzdatendatei wurde als Ausgabeziel akzeptiert")
        assert not callbacks, callbacks
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK: Änderungsverlauf mit Migration, Vorgängen, Sammeleinträgen, Grenzen, Backups, Filtern und Dialog")
