"""Kapazität und Tagesplanung: Rechenregeln, Ansicht, Aktionen und Dialoge."""
import copy
import importlib.machinery
import importlib.util
import os
import tempfile
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def labels(widget):
    return [str(w.cget("text")) for w in descendants(widget) if w.winfo_class() == "Label"]


with tempfile.TemporaryDirectory(prefix="glide-features315-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features315", str(REPO / "src/glide/app.pyw"))
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
        # --- Einstellung: Vorgabe, Grenzen und Rückfall ----------------------
        assert app.DATA_SCHEMA_VERSION == 20, "Format 20 ergänzt Verweise, Symbole und Archiv."
        assert app.DAILY_CAPACITY_DEFAULT == 0 and app.DAILY_CAPACITY_MAX == 1440
        assert app.daily_capacity_minutes() == 0, "Ohne Angabe gibt es keinen Vergleichswert."
        for value, expected in ((0, 0), (1, 1), (1440, 1440), (2000, 1440), (-5, 0),
                                ("90", 0), (True, 0), (1.5, 0), (None, 0)):
            normalized = app.normalize_personal_settings({"daily_capacity_minutes": value})
            assert normalized["daily_capacity_minutes"] == expected, (value, normalized)
        assert app.normalize_personal_settings({})["daily_capacity_minutes"] == 0
        app.settings["daily_capacity_minutes"] = "kaputt"
        assert app.daily_capacity_minutes() == 0, "Ein beschädigter Wert darf keine Kapazität erfinden."
        app.settings["daily_capacity_minutes"] = 300

        # --- Rechenregeln der Bilanz -----------------------------------------
        tag = "2090-10-05"
        andertag = "2090-10-06"
        liste = app.new_list_object("Kapazitätsprüfung", [])
        konzept = app.new_item("Konzept", due="2090-10-09", planned_date=tag,
                               estimated_minutes=45, importance=1)
        freigabe = app.new_item("Abstimmung", due="2090-10-07", planned_date=tag,
                                estimated_minutes=90, importance=3, kind=app.ITEM_KIND_LONG)
        ohne = app.new_item("Ohne Schätzung", planned_date=tag)
        erledigt = app.new_item("Schon fertig", planned_date=tag, estimated_minutes=60)
        erledigt["done"] = True
        spaeter = app.new_item("Nächster Tag", planned_date=andertag, estimated_minutes=30)
        gruppe = app.new_item("Gruppe", kind=app.ITEM_KIND_GROUP)
        gruppe["children"] = [app.new_item("Unterpunkt", planned_date=tag, estimated_minutes=15)]
        ueberschrift = app.new_item("Abschnitt", kind=app.ITEM_KIND_HEADING)
        liste["items"] = [konzept, freigabe, ohne, erledigt, spaeter, gruppe, ueberschrift]
        app.lists.append(liste)
        app.set_active_list(liste["id"])

        summe = app.planning_summary([konzept, freigabe, ohne, erledigt, gruppe, ueberschrift], capacity=0)
        assert summe["items"] == 4, "Gruppen und Überschriften tragen keine Planung."
        assert summe["minutes"] == 195 and summe["estimated"] == 3
        assert summe["without_estimate"] == 1, "Ein Punkt ohne Schätzung wird gezählt, nicht geraten."
        assert summe["done_minutes"] == 60, "Erledigte bleiben in der Summe und werden ausgewiesen."
        assert summe["remaining"] is None, "Ohne Kapazität gibt es keinen Rest."
        text = app.format_planning_summary(summe)
        assert text == "3 h 15 min geplant · davon 1 h erledigt · 1 ohne Schätzung", text
        assert app.format_planning_summary(app.planning_summary([])) == ""
        assert app.format_planning_summary(app.planning_summary([gruppe])) == ""

        knapp = app.planning_summary([konzept, freigabe], capacity=300)
        assert knapp["remaining"] == 165
        assert "2 h 45 min frei von 5 h" in app.format_planning_summary(knapp)
        voll = app.planning_summary([konzept, freigabe], capacity=135)
        assert voll["remaining"] == 0 and "0 min frei von 2 h 15 min" in app.format_planning_summary(voll)
        ueber = app.planning_summary([konzept, freigabe], capacity=120)
        assert ueber["remaining"] == -15
        assert "15 min über 2 h" in app.format_planning_summary(ueber), app.format_planning_summary(ueber)
        assert app.planning_summary([konzept], capacity=1)["remaining"] == -44
        # Ein ungültiger Aufwand am Punkt verändert die Summe nicht.
        beschaedigt = dict(konzept, estimated_minutes="45")
        assert app.planning_summary([beschaedigt], capacity=0)["without_estimate"] == 1

        # --- Tagesplanung: Menge, Reihenfolge und Filter ----------------------
        app.set_plan_day_view(day=tag)
        root.update()
        assert app.view_mode == app.PLAN_DAY_VIEW and app.plan_day() == tag
        eintraege = app.plan_day_entries(apply_filters=False)
        assert [entry[4]["text"] for entry in eintraege] == [
            "Abstimmung", "Konzept", "Ohne Schätzung", "Schon fertig", "Unterpunkt",
        ], [entry[4]["text"] for entry in eintraege]
        assert app.count_plan_day() == 5
        assert all(app.is_schedulable_item(item) for item in app.plan_day_items())
        assert gruppe["id"] not in [item["id"] for item in app.plan_day_items()]
        assert app.plan_day_items(day=andertag) == [spaeter]
        assert app.plan_day_items(day="2090-10-07") == []

        # Seit 3.22 ist „Mein Tag“ genau diese Ansicht: today_plan_ids liest
        # den Bearbeitungstag und zählt jeden Punkt einmal.
        assert app.today_plan_ids() == [item["id"] for item in app.plan_day_items()]
        assert app.count_today_plan() == app.count_plan_day() == 5
        assert app.planning_summary(app.plan_day_items(), capacity=0)["minutes"] == 210
        assert app.planning_summary(
            [entry[4] for entry in app.today_plan_entries(apply_filters=False)], capacity=0
        )["minutes"] == 210, "Eine Ansicht, eine Summe."
        # Einplanen und Austragen laufen über denselben Befehl wie zuvor,
        # wirken aber auf planned_date und damit auf die Aufgabendatei.
        frei = app.new_item("Später einplanen")
        liste["items"].append(frei)
        app.update_today_plan([frei["id"]], add=True, day=tag)
        assert app.find_item_in_lists(frei["id"])[0]["planned_date"] == tag
        assert frei["id"] in app.today_plan_ids(day=tag)
        app.update_today_plan([frei["id"]], add=False, day=tag)
        assert app.find_item_in_lists(frei["id"])[0]["planned_date"] is None
        liste["items"].remove(frei)

        # --- Statistikzeile, Titel und Leertext ------------------------------
        app.update_stats_label()
        # Seit dem festen Layout (27.09.2026) kürzt die Kopfzeile sichtbar auf
        # drei Zeilen; der vollständige Text steht im Tooltip und hier.
        zeile = app._stats_full_text
        sichtbar = app.stats_label.cget("text")
        assert zeile.startswith(sichtbar.rstrip(" …")), (sichtbar, zeile)
        assert "5 Aufgaben am " in zeile and "05.10.2090" in zeile, zeile
        assert "3 h 30 min geplant" in zeile and "1 h erledigt" in zeile, zeile
        assert "1 ohne Schätzung" in zeile and "30 min frei von 5 h" in zeile, zeile
        assert app.get_display_title() == f"Mein Tag · {app.format_plan_day()}"
        assert "05.10.2090" in app.format_plan_day()
        assert app.format_plan_day(date.today().isoformat()).endswith("· heute")
        assert app.system_listbox.set(app.PLAN_DAY_ROW_ID, "count") == "(5)"

        app.shift_plan_day(1)
        root.update()
        assert app.plan_day() == andertag and app.count_plan_day() == 1
        app.shift_plan_day(-1)
        root.update()
        assert app.plan_day() == tag
        app.set_plan_day_view(day="2090-10-08")
        root.update()
        assert app.tree.exists(app.EMPTY_ROW_ID)
        leer = app.tree.item(app.EMPTY_ROW_ID, "text")
        assert "08.10.2090" in leer and "eingeplant" in leer, leer
        app.set_plan_day_view(day=tag)
        root.update()

        # Seit 3.27 ist der Offenfilter entfernt; der alte Wert ändert nichts.
        app.hide_done_var.set(True)
        assert len(app.plan_day_entries(apply_filters=True)) == 5
        assert len(app.plan_day_entries(apply_filters=False)) == 5
        app.hide_done_var.set(False)
        app.search_var.set("abstimmung")
        app.search_placeholder_active = False
        assert [entry[4]["text"] for entry in app.plan_day_entries(apply_filters=True)] == ["Abstimmung"]
        app.search_var.set("")

        # --- Punktaktionen und Rückgängig ------------------------------------
        app.set_plan_day_view(day=tag)
        root.update()
        assert app.update_in_progress_item(konzept["id"], "planned_date", andertag) == "break"
        konzept = app.find_item_in_lists(konzept["id"])[0]
        assert konzept["planned_date"] == andertag and konzept["due"] == "2090-10-09"
        assert konzept["id"] not in [item["id"] for item in app.plan_day_items(day=tag)]
        app.undo_last_change()
        konzept = app.find_item_in_lists(konzept["id"])[0]
        assert konzept["planned_date"] == tag, "Rückgängig stellt den Bearbeitungstag wieder her."
        vorher = copy.deepcopy(app.data_payload())
        messages.clear()
        app.update_in_progress_item(konzept["id"], "planned_date", "2090-02-30")
        assert messages and app.data_payload() == vorher, "Ein ungültiger Tag ändert nichts."
        app.update_in_progress_item(gruppe["id"], "planned_date", tag)
        assert app.find_item_in_lists(gruppe["id"])[0]["planned_date"] is None
        app.update_in_progress_item(konzept["id"], "planned_date", None)
        assert app.find_item_in_lists(konzept["id"])[0]["planned_date"] is None
        app.undo_last_change()
        konzept = app.find_item_in_lists(konzept["id"])[0]
        assert konzept["planned_date"] == tag

        # Serien: Das Vorrücken leert den Bearbeitungstag, es entsteht kein Folgetag.
        app.set_active_list(liste["id"])
        serie = app.find_item_in_lists(freigabe["id"])[0]
        with app.item_change([serie["id"]]) as change:
            serie["repeat"] = app.normalize_repeat({"art": app.REPEAT_DAILY}, default_start=serie["due"])
            serie["done"] = True
            assert app.advance_repeating_items([serie["id"]]) == 1
            change.mark()
        assert serie["planned_date"] is None and serie["estimated_minutes"] == 90
        assert serie["id"] not in [item["id"] for item in app.plan_day_items(day=tag)]
        assert app.plan_day_items(day=serie["due"]) == []
        app.undo_last_change()
        assert app.find_item_in_lists(freigabe["id"])[0]["planned_date"] == tag

        # --- Tabellensumme folgt den sichtbaren Zeilen -----------------------
        app.set_active_list(liste["id"])
        app.set_table_view()
        root.update()
        app.update_stats_label()
        tabelle = app.stats_label.cget("text")
        assert "in der Tabelle" in tabelle and "geplant" in tabelle, tabelle
        alle = app.planning_summary([item for _order, item in app.table_entries(apply_filters=False)], capacity=0)
        app.hide_done_var.set(True)
        offen = app.planning_summary([item for _order, item in app.table_entries(apply_filters=True)], capacity=0)
        # Seit 3.27 gibt es keinen separaten "nur offene Punkte"-Filter mehr.
        # Die verbliebene Kompatibilitaetsvariable darf die Tabelle daher nicht
        # mehr veraendern.
        assert offen == alle, (offen, alle)
        assert app.planning_summary(app.plan_day_items(day=tag), capacity=0)["minutes"] == alle["minutes"] - 30
        app.hide_done_var.set(False)

        # --- Startseite: Zeile nur bei tatsächlicher Tagesplanung ------------
        app.set_home_view()
        root.update()
        assert not any("Heute geplant" in text for text in labels(app.home_content))
        app.set_active_list(liste["id"])
        heute = app.new_item("Heute einplanen", planned_date=date.today().isoformat(), estimated_minutes=120)
        app.items.append(heute)
        assert app.save_items()
        assert app.plan_day_items(day=date.today().isoformat()) == [heute]
        app.set_home_view()
        root.update()
        geplant = [text for text in labels(app.home_content) if "Heute geplant" in text]
        assert geplant and "1 Aufgabe(n)" in geplant[0] and "2 h geplant" in geplant[0], geplant
        assert "3 h frei von 5 h" in geplant[0], geplant[0]
        assert any(getattr(button, "text", "").endswith("Mein Tag öffnen")
                   for button in descendants(app.home_content) if isinstance(button, mod.RoundedButton))
        assert "today" in [key for _button, key in app.home_quick_actions.entries]
        assert "planday" not in [key for _button, key in app.home_quick_actions.entries]

        # --- Einstellungsdialog in Hell und Dunkel ---------------------------
        root.deiconify()
        root.geometry("1100x780+10+10")
        for theme in ("light", "dark"):
            app.set_design(theme, apply_now=False)
            app.apply_theme()

            def settings_dialog(dialog, parent=None):
                dialog.geometry("780x640")
                dialog.update()
                widgets = list(descendants(dialog))
                feld = next(w for w in widgets if w.winfo_name() == "daily_capacity")
                speichern = next(w for w in widgets if isinstance(w, mod.RoundedButton) and w.text == "Speichern")
                assert speichern.winfo_ismapped()
                assert (speichern.winfo_rooty() + speichern.winfo_height()
                        <= dialog.winfo_rooty() + dialog.winfo_height())
                for ungueltig in ("abc", "-30", "1441", "1,5"):
                    feld.delete(0, mod.tk.END)
                    feld.insert(0, ungueltig)
                    speichern.command()
                    assert dialog.winfo_exists(), ungueltig
                feld.delete(0, mod.tk.END)
                feld.insert(0, "480")
                speichern.command()
            app.run_modal = settings_dialog
            app.show_settings_dialog()
            assert app.daily_capacity_minutes() == 480, app.settings.get("daily_capacity_minutes")
            app.settings["daily_capacity_minutes"] = 300

            app.run_modal = lambda dialog, parent=None: dialog.destroy()
            vorher = copy.deepcopy(app.settings)
            app.show_settings_dialog()
            assert app.settings == vorher, "Abbrechen verändert keine Einstellung."
        assert not callbacks, callbacks
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK: Kapazität, Tagesplanung, Reihenfolge, Filter, Punktaktionen, Serien, Startseite und Einstellungsdialog")
