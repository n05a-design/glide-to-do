"""„Mein Tag“ seit 3.22: eine Ansicht über den Bearbeitungstag."""
import copy
import importlib.machinery
import importlib.util
import json
import os
import tempfile
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

with tempfile.TemporaryDirectory(prefix="glide-features312-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features312", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)

    root = mod.tk.Tk()
    root.withdraw()
    errors = []
    root.report_callback_exception = lambda *error: errors.append(error)
    app = mod.ListApp(root)
    app.show_warning = lambda *args, **kwargs: None
    app.show_error = lambda *args, **kwargs: None
    app.show_info = lambda *args, **kwargs: None
    heute = date.today().isoformat()
    morgen = (date.today() + timedelta(days=1)).isoformat()
    try:
        # --- Die beiden früheren Ansichten sind eine geworden ----------------
        assert app.TODAY_PLAN_VIEW == app.PLAN_DAY_VIEW == "planday"
        assert app.TODAY_PLAN_ROW_ID == app.PLAN_DAY_ROW_ID
        assert app.TASK_OVERVIEW_VIEWS.count(app.PLAN_DAY_VIEW) == 1

        first = app.new_list_object("Planung", [])
        second = app.new_list_object("Produktion", [])
        app.lists.extend([first, second])
        first_item = app.new_item("Konzept prüfen", due=None)
        second_item = app.new_item("Text freigeben", due=heute)
        first["items"].append(first_item)
        second["items"].append(second_item)
        app.save_items()

        # --- Einplanen schreibt den Bearbeitungstag an den Punkt -------------
        app.update_today_plan([second_item["id"], first_item["id"]], add=True, day=heute)
        assert first_item["planned_date"] == heute and second_item["planned_date"] == heute
        assert set(app.today_plan_ids()) == {first_item["id"], second_item["id"]}
        # Die Planung steht in der Aufgabendatei, nicht in den Einstellungen.
        gespeichert = json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
        geplant = [item["planned_date"] for liste in gespeichert["lists"]
                   for item in app.walk_items(liste.get("items", []))
                   if item["id"] in (first_item["id"], second_item["id"])]
        assert geplant == [heute, heute], geplant
        assert "today_plan" not in app.load_settings()

        app.set_today_view()
        root.update()
        assert app.view_mode == app.PLAN_DAY_VIEW and app.plan_day() == heute
        assert app.get_display_title().startswith("Mein Tag · ")
        assert app.count_today_plan() == 2
        assert app.system_listbox.exists(app.PLAN_DAY_ROW_ID)
        assert not app.system_listbox.exists("smart:today")
        assert app.tree.exists(f"in-progress:{second['id']}:{second_item['id']}")

        # --- Die Planung überlebt Mitternacht --------------------------------
        # Vor 3.22 verfiel die Auswahl mit dem Datumsstempel in den
        # Einstellungen. Jetzt steht sie am Punkt und bleibt erhalten.
        app.update_today_plan([first_item["id"]], add=True, day=morgen)
        assert first_item["planned_date"] == morgen
        assert app.today_plan_ids(day=morgen) == [first_item["id"]]
        assert app.today_plan_ids(day=heute) == [second_item["id"]]

        # --- Austragen lässt die Aufgabe unberührt ---------------------------
        before = copy.deepcopy(second_item)
        app.update_today_plan([second_item["id"]], add=False, day=heute)
        assert second_item["planned_date"] is None
        assert {k: v for k, v in second_item.items() if k != "planned_date"} == \
               {k: v for k, v in before.items() if k != "planned_date"}
        assert app.today_plan_ids(day=heute) == []

        # --- Gliederung und Unbekanntes werden nie eingeplant ----------------
        group = app.new_item("Abschnitt", kind=app.ITEM_KIND_GROUP)
        first["items"].append(group)
        app.update_today_plan([group["id"], "missing"], add=True, day=heute)
        assert group.get("planned_date") is None
        assert app.today_plan_ids(day=heute) == []

        # --- Tag leeren ------------------------------------------------------
        app.update_today_plan([second_item["id"]], add=True, day=heute)
        assert app.today_plan_ids(day=heute) == [second_item["id"]]
        app.clear_today_plan(day=heute)
        assert app.today_plan_ids(day=heute) == []
        assert second_item["planned_date"] is None

        # --- Eingangsblock: offene Punkte ohne Tag ---------------------------
        inbox = app.ensure_inbox_list()
        neu = app.new_item("Frisch erfasst")
        erledigt = app.new_item("Schon fertig")
        erledigt["done"] = True
        mit_tag = app.new_item("Schon geplant", planned_date=heute)
        inbox["items"] = [neu, erledigt, mit_tag]
        app.save_items()
        eingang = [item for _quelle, item in app.plan_inbox_items(apply_filters=False)]
        assert eingang == [neu], [item["text"] for item in eingang]
        app.set_today_view()
        root.update()
        assert app.tree.exists(app.PLAN_INBOX_HEADING_ROW_ID)
        assert app.tree.exists(f"in-progress:{inbox['id']}:{neu['id']}")
        kopf = app.tree.item(app.PLAN_INBOX_HEADING_ROW_ID, "text")
        assert "Eingang" in kopf and "1" in kopf, kopf
        app.update_stats_label()
        assert "im Eingang ohne Tag" in app.stats_label.cget("text")

        # Aus dem Block heraus einplanen setzt den betrachteten Tag.
        app.update_today_plan([neu["id"]], add=True)
        assert neu["planned_date"] == heute
        app.set_today_view()
        root.update()
        assert not app.tree.exists(app.PLAN_INBOX_HEADING_ROW_ID)

        # --- Migration einer 3.21-Auswahl ------------------------------------
        app.settings["today_plan_migrated"] = False
        app.settings["today_plan"] = {"date": heute, "item_ids": [second_item["id"], "unbekannt"]}
        assert app.migrate_today_plan_setting() is True
        assert second_item["planned_date"] == heute
        assert app.settings["today_plan_migrated"] is True
        assert "today_plan" not in app.settings
        # Ein zweiter Lauf ändert nichts mehr.
        assert app.migrate_today_plan_setting() is False
        assert not errors, errors
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK: Mein Tag über den Bearbeitungstag, Tageswechsel, Eingangsblock und Migration")
