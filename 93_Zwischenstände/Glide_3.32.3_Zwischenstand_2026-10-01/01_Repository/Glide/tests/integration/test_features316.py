"""Vollständiges App-Backup: Rundlauf, Teilbereiche, Vorschau und Grenzen."""
import copy
import importlib.machinery
import importlib.util
import json
import os
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def rejects(action, hinweis="Ungültiges Archiv wurde angenommen"):
    try:
        action()
    except ValueError:
        return
    raise AssertionError(hinweis)


with tempfile.TemporaryDirectory(prefix="glide-features316-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features316", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    callbacks = []
    root.report_callback_exception = lambda *args: callbacks.append(args)
    app = mod.ListApp(root)
    messages = []
    app.show_warning = app.show_error = lambda *args, **kwargs: messages.append(args)
    app.show_info = lambda *args, **kwargs: None
    app.ask_yes_no = lambda *args, **kwargs: True
    try:
        assert app.APP_BACKUP_FORMAT_VERSION == 1 and app.APP_BACKUP_EXTENSION == ".glideapp"
        assert app.DATA_SCHEMA_VERSION == 20, "Format 20 ergänzt Verweise, Symbole und Archiv."

        # --- Ausgangsbestand -------------------------------------------------
        liste = app.new_list_object("Archivprobe", [])
        aufgabe = app.new_item("Konzept sichern", due="2090-11-05",
                               planned_date="2090-11-02", estimated_minutes=75)
        gruppe = app.new_item("Abschnitt", kind=app.ITEM_KIND_GROUP)
        gruppe["children"] = [app.new_item("Unterpunkt")]
        liste["items"] = [aufgabe, gruppe]
        app.lists.append(liste)
        app.set_active_list(liste["id"])
        app.settings["daily_capacity_minutes"] = 420
        app.settings["daily_goal"] = 7
        app.settings["profile_name"] = "Archivprobe"
        app.settings["completion_history"] = {"2026-09-11": 2, "2026-09-12": 3}
        app.settings["activity_history"] = {"2026-09-12": 5}
        # Seit 3.22 ist „Mein Tag“ der Bearbeitungstag am Punkt selbst; eine
        # eigene Auswahl in den Einstellungen gibt es nicht mehr.
        assert app.today_plan_ids(day="2090-11-02") == [aufgabe["id"]]
        assert app.save_items() and app.save_settings()
        eigene_vorlage = app.capture_template(list_id=liste["id"])
        assert eigene_vorlage and app.template_by_id(eigene_vorlage["id"])
        vorlagen_vorher = len(app.templates)

        # --- Aufbau des Archivs ---------------------------------------------
        payload = app.app_backup_payload()
        section = payload["app_backup"]
        assert section["format_version"] == 1
        assert section["settings"]["daily_capacity_minutes"] == 420
        assert section["settings"]["profile_name"] == "Archivprobe"
        assert section["settings"]["theme"] == app.theme_name
        assert all(key not in section["settings"] for key in app.APP_BACKUP_ACTIVITY_KEYS), \
            "Aktivitätsdaten stehen im eigenen Abschnitt, nicht in den Einstellungen."
        assert section["activity"]["completion_history"] == {"2026-09-11": 2, "2026-09-12": 3}
        assert section["templates"]["format_version"] == app.TEMPLATE_FORMAT_VERSION
        assert len(section["templates"]["templates"]) == vorlagen_vorher
        assert payload["version"] == app.DATA_SCHEMA_VERSION and payload["app"] == mod.APP_NAME

        archiv = os.path.join(folder, "vollstaendig.glideapp")
        assert app.write_complete_backup(archiv, payload) == 0
        assert zipfile.is_zipfile(archiv)
        with zipfile.ZipFile(archiv) as pruef:
            assert pruef.namelist() == ["data.json"]

        # Dasselbe Archiv bleibt ein gültiges Aufgabenbackup für ältere Fassungen.
        daten, gelesen = app.read_app_backup_file(archiv)
        assert app.validate_backup_schema(daten, portable=True) == set()
        assert gelesen["format_version"] == 1

        # --- Inhaltsvorschau -------------------------------------------------
        vorschau = app.describe_app_backup(daten, gelesen)
        assert vorschau["app_version"] == mod.APP_VERSION and vorschau["schema"] == 20
        # Zwei echte Aufgaben (eine davon im Gruppenzweig), eine Gruppe.
        assert vorschau["tasks"] == 2 and vorschau["structural"] == 1, vorschau
        assert vorschau["lists"] == len(daten["lists"]) and vorschau["templates"] == vorlagen_vorher
        assert vorschau["activity_days"] == 2 and vorschau["has_settings"] and vorschau["has_templates"]
        text = app.format_app_backup_preview(vorschau)
        for teil in (mod.APP_VERSION, "Aufgaben: 2", "Vorlagen im Archiv", "2 erfasste Tage"):
            assert teil in text, (teil, text)
        # Anhänge werden über alle Träger gezählt, auch an Listen und Ordnern.
        kuenstlich = {
            "app_version": "3.15.0", "version": 14, "exported_at": "2026-09-13T10:00:00",
            "folders": [{"id": "f", "attachments": [{"storage": "a"}]}],
            "labels": [], "trash": [{"kind": "list"}],
            "lists": [{"id": "l", "attachments": [{"storage": "b"}],
                       "items": [{"id": "i", "kind": "task", "attachments": [{"storage": "c"}]}]}],
        }
        gezaehlt = app.describe_app_backup(kuenstlich)
        assert gezaehlt["attachments"] == 3 and gezaehlt["trash"] == 1
        assert not gezaehlt["has_settings"] and not gezaehlt["has_templates"]

        # --- Ungültige Zusatzabschnitte --------------------------------------
        for kaputt in ({"format_version": 0}, {"format_version": 2}, {"format_version": "1"},
                       {"format_version": True},
                       {"format_version": 1, "settings": []},
                       {"format_version": 1, "templates": {"templates": {}}},
                       {"format_version": 1, "activity": {"completion_history": []}}):
            rejects(lambda wert=kaputt: app.app_backup_section({"app_backup": wert}))
        assert app.app_backup_section({"lists": []}) is None, "Ein reines Aufgabenbackup hat keinen Zusatzteil."
        assert app.app_backup_section(None) is None

        # Kein Archiv, beschädigtes Archiv, fremdes Archiv.
        klartext = os.path.join(folder, "kein_archiv.glideapp")
        Path(klartext).write_text("{}", encoding="utf-8")
        rejects(lambda: app.read_app_backup_file(klartext), "Eine Nicht-ZIP-Datei wurde akzeptiert")
        fremd = os.path.join(folder, "fremd.glideapp")
        with zipfile.ZipFile(fremd, "w") as archive:
            archive.writestr("data.json", json.dumps({"app": "Andere App", "version": 14, "lists": []}))
        rejects(lambda: app.read_app_backup_file(fremd), "Ein fremdes Archiv wurde akzeptiert")

        # --- Wiederherstellung einzelner Bereiche ----------------------------
        vor_restore = copy.deepcopy(app.data_payload())
        app.settings["daily_capacity_minutes"] = 0
        app.settings["daily_goal"] = 1
        app.settings["completion_history"] = {}
        app.settings["activity_history"] = {}
        app.templates = []
        assert app.save_settings() and app.save_templates()

        # Nur Vorlagen: Einstellungen und Aufgaben bleiben unberührt.
        assert app.restore_app_backup(path=archiv, sections={"templates": True}, show_success=False)
        assert len(app.templates) == vorlagen_vorher
        assert app.daily_capacity_minutes() == 0, "Ohne Auswahl darf keine Einstellung wandern."
        assert app.data_payload()["lists"] == vor_restore["lists"]

        # Nur Aktivitätsdaten.
        assert app.restore_app_backup(path=archiv, sections={"activity": True}, show_success=False)
        assert app.settings["completion_history"] == {"2026-09-11": 2, "2026-09-12": 3}
        assert app.daily_goal() == 1, "Die Aktivitätsauswahl verändert keine weiteren Einstellungen."

        # Nur Einstellungen, ohne Aufgaben: Ansichtsverweise werden verworfen.
        assert app.restore_app_backup(path=archiv, sections={"settings": True}, show_success=False)
        assert app.daily_capacity_minutes() == 420 and app.daily_goal() == 7
        assert app.settings["profile_name"] == "Archivprobe"
        # Seit 3.22 steht „Mein Tag“ am Punkt selbst: Werden nur Einstellungen
        # zurückgespielt, verändert das die Tagesplanung nicht.
        vor_tagesplan = app.today_plan_ids()
        assert app.restore_app_backup(path=archiv, sections={"settings": True}, show_success=False)
        assert app.today_plan_ids() == vor_tagesplan

        # Alles zusammen: Aufgaben laufen durch den geprüften Importpfad.
        app.settings["daily_capacity_minutes"] = 0
        assert app.save_settings()
        vorher_backups = set(Path(mod.BACKUP_DIR).glob("vor_import_*.glidebackup"))
        assert app.restore_app_backup(
            path=archiv,
            sections={"tasks": True, "settings": True, "templates": True, "activity": True},
            show_success=False,
        )
        assert app.daily_capacity_minutes() == 420
        wieder = next((entry for entry in app.lists if entry.get("title") == "Archivprobe"), None)
        assert wieder is not None
        punkte = [item for item in app.walk_items(wieder.get("items", [])) if app.is_schedulable_item(item)]
        assert len(punkte) == 2
        gesichert = next(item for item in punkte if item["text"] == "Konzept sichern")
        assert gesichert["estimated_minutes"] == 75
        assert gesichert["planned_date"] == "2090-11-02"
        assert app.today_plan_ids(day="2090-11-02") == [gesichert["id"]], \
            "Mit den Aufgaben wandert der Bearbeitungstag mit."
        neue_backups = set(Path(mod.BACKUP_DIR).glob("vor_import_*.glidebackup")) - vorher_backups
        assert neue_backups, "Vor dem Ersetzen muss ein Komplettbackup entstehen."
        assert list(Path(mod.BACKUP_DIR).glob("settings_vor_restore_*.json")), "Einstellungen wurden nicht gesichert."
        assert list(Path(mod.BACKUP_DIR).glob("vorlagen_vor_restore_*.json")), "Vorlagen wurden nicht gesichert."

        # Kein Bereich gewählt: Warnung, keine Änderung.
        messages.clear()
        unveraendert = copy.deepcopy(app.data_payload())
        assert app.restore_app_backup(path=archiv, sections={}, show_success=False) is None
        assert messages and app.data_payload() == unveraendert

        # Ein Aufgabenbackup ohne Zusatzteil bleibt lesbar; Extras fehlen.
        nur_aufgaben = os.path.join(folder, "nur_aufgaben.glidebackup")
        app.write_complete_backup(nur_aufgaben, app.complete_backup_payload())
        daten2, gelesen2 = app.read_app_backup_file(nur_aufgaben)
        assert gelesen2 is None
        vorschau2 = app.describe_app_backup(daten2, gelesen2)
        assert not vorschau2["has_settings"] and not vorschau2["has_templates"] and not vorschau2["has_activity"]
        assert "nicht enthalten" in app.format_app_backup_preview(vorschau2)

        # --- Vorschaudialog in Hell und Dunkel -------------------------------
        root.deiconify()
        root.geometry("1100x780+10+10")
        for theme in ("light", "dark"):
            app.set_design(theme, apply_now=False)
            app.apply_theme()

            def dialog_pruefen(dialog, parent=None):
                dialog.geometry("780x640")
                dialog.update()
                widgets = list(descendants(dialog))
                anzeige = next(w for w in widgets if w.winfo_name() == "app_backup_preview")
                assert "Aufgaben: 2" in anzeige.cget("text"), anzeige.cget("text")
                haken = {name: next(w for w in widgets if w.winfo_name() == "section_" + name)
                         for name in app.APP_BACKUP_SECTIONS}
                assert all(str(w.cget("state")) == "normal" for w in haken.values())
                knopf = next(w for w in widgets if isinstance(w, mod.RoundedButton) and w.text == "Wiederherstellen")
                assert knopf.winfo_ismapped()
                assert (knopf.winfo_rooty() + knopf.winfo_height()
                        <= dialog.winfo_rooty() + dialog.winfo_height())
                for name in ("tasks", "settings", "activity"):
                    haken[name].invoke()
                knopf.command()
            app.run_modal = dialog_pruefen
            app.templates = []
            assert app.save_templates()
            assert app.restore_app_backup(path=archiv, show_success=False)
            assert len(app.templates) == vorlagen_vorher, "Nur der angehakte Bereich wird übernommen."

            def abbrechen(dialog, parent=None):
                dialog.update()
                widgets = list(descendants(dialog))
                next(w for w in widgets if isinstance(w, mod.RoundedButton) and w.text == "Abbrechen").command()
            app.run_modal = abbrechen
            zustand = copy.deepcopy(app.data_payload())
            einstellungen = copy.deepcopy(app.settings)
            assert app.restore_app_backup(path=archiv, show_success=False) is None
            assert app.data_payload() == zustand and app.settings == einstellungen

            # Ohne Zusatzteil sind die drei Extrabereiche gesperrt.
            def gesperrt_pruefen(dialog, parent=None):
                dialog.update()
                widgets = list(descendants(dialog))
                for name in ("settings", "templates", "activity"):
                    check = next(w for w in widgets if w.winfo_name() == "section_" + name)
                    assert str(check.cget("state")) == "disabled", name
                next(w for w in widgets if isinstance(w, mod.RoundedButton) and w.text == "Abbrechen").command()
            app.run_modal = gesperrt_pruefen
            assert app.restore_app_backup(path=nur_aufgaben, show_success=False) is None
        assert not callbacks, callbacks
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK: App-Backup mit Einstellungen, Vorlagen und Aktivität, Teilbereiche, Vorschau, Grenzen und Dialoge")
