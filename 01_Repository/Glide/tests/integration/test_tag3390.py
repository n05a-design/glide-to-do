"""Tagesplanung mit echten Tk-Widgets, Dateischreibfehlern und Vorversionsgegenproben."""
import argparse
import copy
from datetime import date, datetime, timedelta, timezone
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import time
import traceback
from threading import Event


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def run(app_path, cases, report):
    checks, errors, notices = [], [], []
    with tempfile.TemporaryDirectory(prefix="glide3390-") as folder:
        os.environ.update(GLIDE_DATA_DIR=folder, GLIDE_TEST_MODE="1", TZ="Europe/Berlin")
        sys.path.insert(0, str(app_path.parent))
        loader = importlib.machinery.SourceFileLoader("glide_tagesplanung3390", str(app_path))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = mod
        loader.exec_module(mod)
        required = {"hinweise": "process_daily_hints", "kalender": "calendar_grid_blocks",
                    "entlasten": "apply_day_relief", "dialoge": "show_day_relief"}
        for case in cases:
            assert callable(getattr(mod.ListApp, required[case], None)), required[case] + " fehlt"
        root = mod.tk.Tk()
        root.geometry("1280x800+20+20")
        root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
        app = mod.ListApp(root)
        app.show_warning = app.show_error = app.show_info = lambda *a, **k: notices.append(a)
        zone = app._daily_resolver("Europe/Berlin")
        today = date.today()
        day, tomorrow = today.isoformat(), (today+timedelta(days=1)).isoformat()
        source = app.new_list_object("Tagesplanung Test", [
            app.new_item("Geplant", planned_date=day, planned_time="09:30", estimated_minutes=60,
                         due=tomorrow, due_time="17:00", labels=[], importance=2),
            app.new_item("Ohne Schätzung", planned_date=day),
            app.new_item("Vorratsaufgabe", estimated_minutes=30, due=day)])
        app.lists.append(source)
        sid = source["id"]
        identities = [item["id"] for item in source["items"]]
        app.settings.update(daily_capacity_minutes=480, daily_hints={"enabled": False}, busy_calendar={})

        app.settings["daily_capacity_by_weekday"] = [None]*7
        app.save_items()
        app.save_settings()
        app.set_active_list(sid)

        def pump():
            root.update_idletasks()
            root.update()

        def fresh(index):
            return app.find_item_in_lists(identities[index])[0]

        def wait_ready():
            until = time.monotonic()+8
            while time.monotonic()<until:
                pump()
                view = app.busy_view(day)
                if view.status in ("ready", "error"):
                    return view
                time.sleep(.01)
            raise AssertionError("Kalenderdienst bleibt länger als acht Sekunden unbekannt")

        def load_calendar(content):
            path = Path(folder)/"Belegzeiten Test.ics"
            path.write_text(content, encoding="utf-8")
            app.settings["busy_calendar"] = dict(path=str(path), zone="UTC")
            app.save_settings()
            app.init_daily_planning()
            app._daily_zone = zone
            view = wait_ready()
            assert view.status == "ready", view.message
            return path, view

        def calendar_text():
            # Zwei überlappende echte Termine: 08:00 bis 10:00 Ortszeit insgesamt.
            first = datetime.combine(today, datetime.min.time(), zone)+timedelta(hours=8)
            start = first.astimezone(timezone.utc)
            stamp = lambda value: value.strftime("%Y%m%dT%H%M%SZ")
            return ("BEGIN:VCALENDAR\n"
                    "BEGIN:VEVENT\nUID:termin-a\nSUMMARY:Besprechung\nDTSTART:"+stamp(start)+"\n"
                    "DTEND:"+stamp(start+timedelta(minutes=90))+"\nEND:VEVENT\n"
                    "BEGIN:VEVENT\nUID:termin-b\nSUMMARY:Überschneidung\nDTSTART:"+stamp(start+timedelta(minutes=30))+"\n"
                    "DTEND:"+stamp(start+timedelta(minutes=120))+"\nEND:VEVENT\n"
                    "END:VCALENDAR\n")

        def laid_out(dialog):
            footer = getattr(dialog, "_daily_footer", None)
            return bool(dialog.winfo_ismapped() and (footer is None or footer.winfo_ismapped()))

        def modal(title, opener, action):
            failures, observed = [], []
            def perform():
                dialogs = [child for child in root.winfo_children()
                           if isinstance(child, mod.tk.Toplevel) and child.winfo_exists() and child.title()==title]
                if not dialogs:
                    failures.append("Dialog fehlt: "+title)
                    return
                dialog = dialogs[-1]
                observed.append(dialog)
                # Der Takt von 80 ms belegt keine Sichtbarkeit (17.10.2026): Dauert
                # der Aufbau länger – unter Windows 50–96 ms gemessen –, läuft der
                # abgelaufene Zeitgeber in wait_window vor Tks Leerlauf, der den
                # frisch gezeigten Dialog erst anordnet und seine Kinder mappt. Der
                # Dialog steht dann mit 1x1-Inhalt da; „Speichern nicht sichtbar“
                # war dieser Zustand, kein Glide-Fehler. Gewartet wird deshalb auf
                # den angeordneten Dialog, höchstens drei Sekunden.
                until = time.monotonic()+3
                pump()
                while not laid_out(dialog) and time.monotonic()<until:
                    time.sleep(.01)
                    pump()
                if not laid_out(dialog):
                    failures.append("Dialog nach drei Sekunden nicht angeordnet: "+title)
                    dialog.destroy()
                    return
                try:
                    action(dialog)
                except BaseException as exc:
                    failures.append(traceback.format_exc())
                    if dialog.winfo_exists():
                        dialog.destroy()
            def timeout():
                failures.append("Dialogzeitlimit: "+title)
                for child in root.winfo_children():
                    if isinstance(child, mod.tk.Toplevel) and child.winfo_exists() and child.title()==title:
                        child.destroy()
            job = root.after(80, perform)
            watchdog = root.after(6000, timeout)
            try:
                opener()
            finally:
                for handle in (job, watchdog):
                    try: root.after_cancel(handle)
                    except mod.tk.TclError: pass
            assert observed and not failures, failures

        def button(dialog, caption):
            result = [widget for widget in descendants(dialog)
                      if isinstance(widget, mod.RoundedButton) and widget.text==caption]
            assert len(result)==1, (caption, [widget.text for widget in descendants(dialog)
                                             if isinstance(widget, mod.RoundedButton)])
            assert callable(result[0].command), caption
            return result[0]

        click_time = [1000]
        def click(dialog, caption):
            target = button(dialog, caption)
            assert target.winfo_ismapped(), caption+' nicht sichtbar'
            target.focus_set();pump()
            click_time[0] += 1000
            x, y = target.winfo_width()//2, target.winfo_height()//2
            target.event_generate('<ButtonPress-1>', x=x, y=y, time=click_time[0])
            target.event_generate('<ButtonRelease-1>', x=x, y=y, time=click_time[0]+10)
            pump()

        def full_table_values(tree, columns):
            font = app.measurement_font(app.style.lookup("Dialog.Treeview", "font"))
            for column in columns:
                assert tree.column(column, "width") >= font.measure(tree.heading(column, "text")) + 24
            for identity in tree.get_children():
                for column in columns:
                    value = tree.item(identity, "text") if column == "#0" else tree.set(identity, column)
                    assert tree.column(column, "width") >= font.measure(value) + 24, (column, value)
            assert tree.cget("xscrollcommand"), "Vollständige Werte brauchen horizontalen Bildlauf"
            tree.xview_moveto(1);pump()
            assert tree.xview()[1] > .99
            tree.xview_moveto(0);pump()

        try:
            pump()
            if "hinweise" in cases:
                import daily_hints
                assert daily_hints.normalize(None)["enabled"] is False
                moment = datetime.combine(today, datetime.min.time(), zone)+timedelta(hours=9)
                app.daily_now = lambda: moment
                app.settings.update(daily_hints=dict(enabled=True,start="08:30",close="17:30",weekdays=list(range(7))),
                                    daily_hint_state={})
                app.save_settings()
                root.focus_force()
                app.entry.focus_set()
                pump()
                kept, context = root.focus_lastfor(), app.inspector_context()
                dialogs = {str(widget) for widget in root.winfo_children() if isinstance(widget, mod.tk.Toplevel)}
                due = app.process_daily_hints()
                assert len(due)==1 and due[0].kind=="start"
                disk = json.loads(Path(mod.SETTINGS_FILE).read_text())
                assert disk["daily_hint_state"]["receipts"][due[0].identity]["status"]=="presented"
                assert app.process_daily_hints()==()
                # Wie im Kalenderfall: Ohne Vordergrund meldet Tk None; der im
                # Hauptfenster gehaltene Fokus muss bleiben.
                assert root.focus_get() in (kept, None) and root.focus_lastfor() is kept, (
                    root.focus_get(), root.focus_lastfor(), kept)
                assert app.inspector_context()==context
                assert dialogs=={str(widget) for widget in root.winfo_children() if isinstance(widget, mod.tk.Toplevel)}
                assert app._daily_hint_count==1
                checks.append("Tageshinweis: echter gespeicherter Beleg vor Anzeige, Glocke, keine Mehrfachzustellung/kein Zwangswechsel")
                hint = app.daily_hint_pending()[0]
                assert app.save_daily_state(daily_hints.snooze(app.settings["daily_hint_state"],hint,moment,15))
                assert app.process_daily_hints()==()
                moment += timedelta(minutes=15)
                assert len(app.process_daily_hints())==1
                assert app.process_daily_hints()==()
                app.save_daily_state(daily_hints.skip_day(app.settings["daily_hint_state"],today,moment))
                moment = moment.replace(hour=18)
                assert app.process_daily_hints()==()
                checks.append("Später und Hinweistag überspringen: echte Settings-Schreibwege, kein erneuter Hinweis")
                moment += timedelta(days=1)
                before = copy.deepcopy(app.settings)
                disk = Path(mod.SETTINGS_FILE).read_bytes()
                write = app.write_json_atomic
                def fail_settings(path, value):
                    if str(path)==str(mod.SETTINGS_FILE):
                        raise OSError("Absichtlicher Settings-Schreibfehler")
                    return write(path,value)
                app.write_json_atomic = fail_settings
                try:
                    assert app.process_daily_hints()==()
                    assert app.settings==before and Path(mod.SETTINGS_FILE).read_bytes()==disk
                    assert app._daily_hint_error
                finally:
                    app.write_json_atomic = write
                assert len(app.process_daily_hints())==2
                assert app.process_daily_hints()==() and not app._daily_hint_error
                checks.append("Echter Settings-Dateischreibfehler: Belege/Datei unverändert, Retry stellt genau einmal zu")
                moment += timedelta(days=1)
                before = copy.deepcopy(app.settings)
                app._data_read_only = True
                try: assert app.process_daily_hints()==() and app.settings==before
                finally: app._data_read_only=False
                modal_window = mod.tk.Toplevel(root)
                modal_window.grab_set()
                try: assert app.process_daily_hints()==() and app.settings==before
                finally:
                    modal_window.grab_release()
                    modal_window.destroy()
                assert len(app.process_daily_hints())==2
                checks.append("Schreibschutz und echter modaler Grab schieben automatische Zustellung auf")
                def basket(dialog):
                    tree = next(widget for widget in descendants(dialog) if widget.winfo_name()=="daily_hints_tree")
                    full_table_values(tree,("#0","day","at","state"))
                    selected = tree.get_children()[0]
                    tree.selection_set(selected);pump()
                    click(dialog,"15 Min. später")
                    assert app.settings["daily_hint_state"]["receipts"][selected]["status"]=="snoozed"
                    assert tree.exists(selected) and tree.item(selected,"values")[-1]=="Später"
                    tree.selection_set(selected);pump()
                    click(dialog,"Hinweistag überspringen")
                    assert not tree.exists(selected)
                    assert app.settings["daily_hint_state"]["receipts"][selected]["status"]=="skipped"
                    click(dialog,"Schließen")
                modal("Tageshinweise",app.show_daily_hints,basket)
                moment += timedelta(days=1)
                assert len(app.process_daily_hints())==2
                def open_hint(dialog):
                    tree = next(widget for widget in descendants(dialog) if widget.winfo_name()=="daily_hints_tree")
                    selected = next(key for key in tree.get_children() if key.endswith("/start"))
                    tree.selection_set(selected);pump()
                    before = app.inspector_context()
                    assert app.settings["daily_hint_state"]["receipts"][selected]["status"]=="presented"
                    click(dialog,"Heute öffnen")
                    assert app.settings["daily_hint_state"]["receipts"][selected]["status"]=="completed"
                    assert app.home_mode()=="day_review"
                modal("Tageshinweise",app.show_daily_hints,open_hint)
                checks.append("Echter Hinweiskorb: Später, Hinweistag überspringen und ausdrücklich gewählter Tagesbeginn")
                app.settings["daily_hints"]["enabled"]=False
                app.save_settings()
            if "kalender" in cases:
                path, view = load_calendar(calendar_text())
                original = path.read_bytes()
                before_items = copy.deepcopy(app.lists)
                assert len(view.blocks)==2
                summary = app.planning_available(day)
                assert summary["occupied_minutes"]==120 and summary["capacity"]==360
                assert summary["minutes"]==60 and summary["remaining"]==300
                assert app.planning_available(day,[identities[2]])["remaining"]==270
                assert "Kalenderzeit" in app.planning_available_text(day)
                assert app.day_proposal(day)["budget"]==270
                assert path.read_bytes()==original and app.lists==before_items
                app.settings["plan_day_grid"]=True
                app.set_plan_day_view(day=day)
                pump()
                app.draw_plan_grid()
                assert app.plan_grid_canvas.find_withtag("calendar_busy")
                assert set(app._plan_grid_blocks)=={identities[0]}
                assert app._plan_grid_blocks[identities[0]][0]["calendar_overlap"]
                assert len(app.calendar_grid_blocks())==2
                assert app.calendar_free_slots([fresh(0)],day,30)==[("10:30","18:00")]
                checks.append("Belegzeiten: vereinigte Kapazität, Vorschlag/Projektionsbilanz, lesendes Raster und echte freie Zeitfenster")
                app.open_calendar_view()
                pump()
                assert app._calendar_summaries[day]["remaining"]==summary["remaining"]
                week=app.week_review_data()
                assert week["rows"][day]["capacity"]==360 and week["rows"][day]["remaining"]==300
                checks.append("Heute, Woche, Wochenrückblick und Tagesvorschlag verwenden dieselbe Bilanz")
                app.set_active_list(sid)
                assert app.open_task_inspector(identities[0])
                pump()
                title=app._detail_state["fields"]["text"]
                title.delete(0,"end");title.insert(0,"Noch ungespeicherter Kalenderentwurf")
                title.focus_set();pump()
                app._calendar_service.load(path,timezone.utc,today,app._daily_resolver)
                assert app.busy_view(day).status=="loading"
                assert app.planning_available(day)["remaining"] is None
                assert "unbekannt" in app.planning_available_text(day)
                assert wait_ready().status=="ready"
                assert app._detail_state["fields"]["text"] is title and title.get()=="Noch ungespeicherter Kalenderentwurf"
                # Gibt der Desktop einem anderen Programm den Vordergrund (unter
                # Windows bei jeder Eingabe des Inhabers während des Laufs), meldet
                # Tk keinen Fokus: focus_get() ist None. Maßgeblich ist der Fokus,
                # den Glide im Hauptfenster hält; ein Wechsel in ein anderes
                # Glide-Fenster bleibt über focus_get() sichtbar (17.10.2026).
                assert root.focus_get() in (title, None) and title.focus_lastfor() is title, (
                    root.focus_get(), title.focus_lastfor())
                assert fresh(0)["text"]=="Geplant"
                app.close_task_inspector(discard=True)
                checks.append("Hintergrundladen: unbekannte Zwischenbilanz und unveränderter ungespeicherter Inspektor")
                path.unlink()
                assert app.busy_view(day).status=="ready"
                app.init_daily_planning()
                assert wait_ready().status=="error"
                assert app.planning_available(day)["remaining"] is None and "unbekannt" in app.planning_available_text(day)
                load_calendar(calendar_text())
                checks.append("Geladener Stand braucht kein Datei-IO; ausdrücklich neu geladene fehlende Datei meldet unbekannte freie Zeit")
                app.set_plan_day_view(day=day);pump()
                path = Path(folder)/"Belegzeiten Test.ics"
                before_config=copy.deepcopy(app.settings["busy_calendar"])
                before_source=app._calendar_service.source
                def preview_cancel(dialog):
                    tree=next(widget for widget in descendants(dialog) if widget.winfo_name()=="busy_calendar_tree")
                    assert len(tree.get_children())==2
                    full_table_values(tree,("#0","start","end"))
                    click(dialog,"Entfernen")
                    assert not tree.get_children()
                    click(dialog,"Abbrechen")
                modal("Kalender als Belegzeiten",app.show_busy_calendar_dialog,preview_cancel)
                assert app.settings["busy_calendar"]==before_config and app._calendar_service.source is before_source
                def calendar_save(dialog):
                    tree=next(widget for widget in descendants(dialog) if widget.winfo_name()=="busy_calendar_tree")
                    field=next(widget for widget in descendants(dialog) if widget.winfo_name()=="calendar_zone")
                    field.delete(0,"end");field.insert(0,"Europe/Berlin")
                    click(dialog,"Speichern")
                    assert dialog.winfo_exists() and app.settings["busy_calendar"]==before_config
                    click(dialog,"Neu laden")
                    until=time.monotonic()+5
                    while time.monotonic()<until and not tree.get_children():
                        pump();time.sleep(.01)
                    assert len(tree.get_children())==2
                    write=app.write_json_atomic
                    def fail(path,value):
                        if str(path)==str(mod.SETTINGS_FILE):raise OSError("Absichtlicher Kalender-Settings-Schreibfehler")
                        return write(path,value)
                    disk=Path(mod.SETTINGS_FILE).read_bytes()
                    app.write_json_atomic=fail
                    try:
                        click(dialog,"Speichern")
                        assert dialog.winfo_exists() and app.settings["busy_calendar"]==before_config
                        assert Path(mod.SETTINGS_FILE).read_bytes()==disk and app._calendar_service.source is before_source
                    finally:app.write_json_atomic=write
                    click(dialog,"Speichern")
                modal("Kalender als Belegzeiten",app.show_busy_calendar_dialog,calendar_save)
                assert app.settings["busy_calendar"]["zone"]=="Europe/Berlin"
                assert app.busy_view(day).status=="ready" and app.planning_available(day)["remaining"]==300
                checks.append("Echter Kalenderdialog: Vorschau/Abbrechen, Zonenänderung verlangt Neuladen, Settings-Schreibfehler und Retry")
                valid_config=copy.deepcopy(app.settings["busy_calendar"])
                invalid_config={"path":False,"future":{"keep":True}}
                app.settings["busy_calendar"]=copy.deepcopy(invalid_config)
                active_source=app._calendar_service.source
                disk=Path(mod.SETTINGS_FILE).read_bytes()
                assert app.busy_view(day).status=="error"
                def invalid_preview(dialog):
                    labels=[widget.cget("text") for widget in descendants(dialog) if isinstance(widget,mod.tk.Label)]
                    assert any("Kalenderpfad ist ungültig" in text for text in labels),labels
                    click(dialog,"Speichern")
                    assert dialog.winfo_exists() and app.settings["busy_calendar"]==invalid_config
                    assert Path(mod.SETTINGS_FILE).read_bytes()==disk
                    assert app._calendar_service.source is active_source
                    click(dialog,"Abbrechen")
                modal("Kalender als Belegzeiten",app.show_busy_calendar_dialog,invalid_preview)
                assert app.settings["busy_calendar"]==invalid_config
                def remove_corrupt(dialog):
                    click(dialog,"Entfernen");click(dialog,"Speichern")
                modal("Kalender als Belegzeiten",app.show_busy_calendar_dialog,remove_corrupt)
                assert app.settings["busy_calendar"]=={} and app._calendar_service.source is None
                app.settings["busy_calendar"]=valid_config;assert app.save_settings()
                app.init_daily_planning();assert wait_ready().status=="ready"
                checks.append("Beschädigte Kalenderauswahl sichtbar; kein stilles Löschen beim Speichern, Entfernen nur ausdrücklich")
                app.set_home_tile_hidden("stats",False)
                current=app.home_signature()
                reader=app._calendar_service.reader
                started,release=Event(),Event()
                def held_reader(*args):
                    started.set()
                    assert release.wait(8),"Prüfstand hat Kalenderarbeiter nicht freigegeben"
                    return reader(*args)
                app._calendar_service.reader=held_reader
                try:
                    app._calendar_service.load(path,timezone.utc,today,app._daily_resolver)
                    assert started.wait(3)
                    assert app.home_signature()!=current
                    app.set_home_view();pump()
                    visible=[widget.cget("text") for widget in descendants(app.home_content)
                             if isinstance(widget,mod.tk.Label)]
                    assert any("unbekannt" in value for value in visible),visible
                finally:
                    release.set()
                    app._calendar_service.reader=reader
                assert wait_ready().status=="ready"
                app._calendar_service.poll();app.refresh_home();pump()
                assert app.planning_available(day)["remaining"]==300
                checks.append("Startseite invalidiert geladenen Kalenderstand und zeigt unbekannte freie Zeit sichtbar an")
                path,view=load_calendar("BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:ganzer-tag\nDTSTART;VALUE=DATE:"
                                        +today.strftime("%Y%m%d")+"\nEND:VEVENT\nEND:VCALENDAR\n")
                assert app.planning_available(day)["capacity"]==0
                assert app.planning_available(day)["remaining"]==-60
                assert "ganztägig" in app.planning_available_text(day).lower()
                before=copy.deepcopy(app.lists)
                try:
                    for item in source["items"]:item["planned_date"]=tomorrow
                    app.clear_render_cache();app._data_revision+=1
                    app.set_home_view();pump()
                    visible=[widget.cget("text") for widget in descendants(app.home_content)if isinstance(widget,mod.tk.Label)]
                    assert any("ganztägig" in value.lower() for value in visible),visible
                finally:
                    app.lists=before
                    app.items=app.current_list().get("items",[]) if app.lists else []
                    app.clear_render_cache();app._data_revision+=1
                assert app.planning_available(day)["remaining"]==-60
                load_calendar(calendar_text())
                checks.append("Ganztägiges Ortsdatum: bekannte Nullkapazität und sichtbare Startbilanz auch ohne eingeplante Aufgabe")
            if "entlasten" in cases:
                load_calendar(calendar_text())
                before=copy.deepcopy(app.lists)
                before_tasks=[copy.deepcopy(fresh(i)) for i in range(3)]
                plan=app.relief_plan(identities[:2],tomorrow)
                assert len(plan.moves)==2 and plan.before[0]["occupied_minutes"]==120
                depth=len(app.undo_stack)
                assert app.apply_day_relief(plan)
                assert len(app.undo_stack)==depth+1
                assert all(fresh(i)["planned_date"]==tomorrow for i in (0,1))
                assert fresh(0)["planned_time"]=="09:30"
                assert all(fresh(i)["due"]==before_tasks[i]["due"] for i in range(3))
                app.undo_last_change()
                pump()
                assert [fresh(i) for i in range(3)]==before_tasks
                plan=app.relief_plan([identities[0]],None)
                assert app.apply_day_relief(plan) and fresh(0)["planned_date"] is None and fresh(0)["planned_time"] is None
                app.undo_last_change()
                pump()
                checks.append("Explizite Mehrfachauswahl und Vorrat: Fälligkeit unverändert, Uhrzeit erhalten/entfernt, genau ein echtes Undo")
                plan=app.relief_plan(identities[:2],tomorrow)
                before=copy.deepcopy(app.lists);disk=Path(mod.SAVE_FILE).read_bytes()
                undo=list(app.undo_stack);history=copy.deepcopy(app.history);dirty=app.dirty
                write=app.write_json_atomic
                def fail_items(path,value):
                    if str(path)==str(mod.SAVE_FILE):
                        raise OSError("Absichtlicher Aufgaben-Dateischreibfehler")
                    return write(path,value)
                app.write_json_atomic=fail_items
                try:
                    assert app.apply_day_relief(plan) is False
                    assert app.lists==before and Path(mod.SAVE_FILE).read_bytes()==disk
                    assert app.undo_stack==undo and app.history==history and app.dirty==dirty
                finally: app.write_json_atomic=write
                assert app.apply_day_relief(plan) and len(app.undo_stack)==len(undo)+1
                app.undo_last_change();pump()
                checks.append("Echter Dateischreibfehler: vollständiger Modell-/Datei-/Undo-/Verlaufsschutz und erfolgreicher Retry")
                plan=app.relief_plan([identities[0]],tomorrow)
                app.settings["daily_capacity_minutes"]=420
                try:
                    app.apply_day_relief(plan)
                    raise AssertionError("Veraltete Kapazitätsvorschau angenommen")
                except ValueError as exc:
                    assert "geändert" in str(exc)
                assert fresh(0)["planned_date"]==day
                app.settings["daily_capacity_minutes"]=480
                checks.append("Veraltete Bilanz wird vor jeder Änderung vollständig abgewiesen")
            if "dialoge" in cases:
                def settings(dialog):
                    entries={widget.winfo_name():widget for widget in descendants(dialog)
                             if isinstance(widget,mod.tk.Entry)}
                    assert {"hint_start","hint_close"}<=set(entries)
                    entries["hint_start"].delete(0,"end");entries["hint_start"].insert(0,"25:99")
                    before=copy.deepcopy(app.settings)
                    click(dialog,"Speichern")
                    assert dialog.winfo_exists() and app.settings==before
                    entries["hint_start"].delete(0,"end");entries["hint_start"].insert(0,"08:45")
                    click(dialog,"Speichern")
                    assert app.settings["daily_hints"]["start"]=="08:45"
                modal("Tageshinweise einstellen",app.show_daily_hint_settings,settings)
                checks.append("Echte Hinweis-Einstellungen: ungültige Uhrzeit bleibt offen, Speichern übernimmt freie Uhrzeit")
                def relief(dialog):
                    tree=next(widget for widget in descendants(dialog) if widget.winfo_name()=="day_relief_tasks")
                    assert identities[0] in tree.get_children()
                    full_table_values(tree,("#0","day","effort","list"))
                    tree.selection_set(identities[0]);pump()
                    # Ohne Vergleich kann Übernehmen keine Daten ändern.
                    before=copy.deepcopy(app.lists)
                    click(dialog,"Übernehmen")
                    assert dialog.winfo_exists() and app.lists==before
                    click(dialog,"Vergleichen")
                    assert dialog.winfo_exists()
                    dialog.event_generate("<Escape>");pump()
                for opener in (lambda: app.set_plan_day_view(day=day), app.show_week_review, app.start_day_proposal):
                    app._calendar_selected_day=tomorrow
                    opener();pump()
                    modal("Tag entlasten",app.show_day_relief,relief)
                checks.append("Echte Entlasten-Dialoge in Heute/Woche/Vorschlag: Auswahl, Vergleichspflicht, Escape")
                app.set_plan_day_view(day=day);pump()
                before=[copy.deepcopy(fresh(i)) for i in range(3)]
                depth=len(app.undo_stack)
                def apply_stock(dialog):
                    tree=next(widget for widget in descendants(dialog) if widget.winfo_name()=="day_relief_tasks")
                    tree.selection_set(identities[:2]);pump()
                    stock=next(widget for widget in descendants(dialog) if isinstance(widget,mod.tk.Radiobutton)
                               and widget.cget("value")=="stock")
                    stock.invoke();pump()
                    click(dialog,"Vergleichen")
                    balance=next(widget for widget in descendants(dialog) if widget.winfo_name()=="day_relief_balance")
                    assert balance.get_children()
                    full_table_values(balance,("before","after"))
                    assert [fresh(i) for i in range(3)]==before
                    click(dialog,"Übernehmen")
                modal("Tag entlasten",app.show_day_relief,apply_stock)
                assert len(app.undo_stack)==depth+1 and all(fresh(i)["planned_date"] is None for i in (0,1))
                assert all(fresh(i)["due"]==before[i]["due"] for i in range(3))
                app.undo_last_change();pump()
                assert [fresh(i) for i in range(3)]==before
                checks.append("Echter Mehrfachdialog: Vergleich ändert nichts, Vorrat übernimmt ausgewählte Aufgaben, ein Undo stellt alles her")
                for font_stage in ("mittel", "gross"):
                    app.settings["ui_font_size"] = font_stage
                    app.apply_ui_font()
                    app.apply_theme();root.geometry("860x700+20+20");pump()
                    assert app.settings["ui_font_size"] == font_stage
                    assert app.ui_font_size() == app.UI_FONT_SIZE_CHOICES[font_stage]
                    assert mod.tkfont.nametofont("TkDefaultFont",root=root).actual("size") == app.ui_font_size()
                    def geometry(dialog):
                        footer=dialog._daily_footer
                        canvas=dialog._daily_scroll_canvas
                        bounds=lambda widget: (widget.winfo_rootx(),widget.winfo_rooty(),
                                                widget.winfo_width(),widget.winfo_height())
                        measured={"dialog":title,"schrift":font_stage,"fenster":bounds(dialog),
                                  "fuss":bounds(footer),"inhalt":bounds(canvas),
                                  "sichtbar":bool(canvas.winfo_ismapped()),
                                  "tasten":[{"text":widget.text,"grenzen":bounds(widget)}
                                             for widget in descendants(footer)
                                             if isinstance(widget,mod.RoundedButton)]}
                        print("Dialoggeometrie: "+json.dumps(measured,ensure_ascii=False),flush=True)
                        assert footer.winfo_rooty()>=dialog.winfo_rooty(), measured
                        assert footer.winfo_rooty()+footer.winfo_height()<=dialog.winfo_rooty()+dialog.winfo_height(), measured
                        assert canvas.winfo_ismapped(), measured
                        for widget in descendants(footer):
                            if isinstance(widget,mod.RoundedButton):
                                assert widget.winfo_rootx()>=dialog.winfo_rootx(), measured
                                assert widget.winfo_rootx()+widget.winfo_width()<=dialog.winfo_rootx()+dialog.winfo_width(), measured
                        canvas.yview_moveto(1);pump()
                        assert canvas.yview()[1]>.99, {**measured,"bildlauf":canvas.yview()}
                        dialog.event_generate("<Escape>");pump()
                    for title,opener in (("Tageshinweise",app.show_daily_hints),
                                         ("Tageshinweise einstellen",app.show_daily_hint_settings),
                                         ("Kalender als Belegzeiten",app.show_busy_calendar_dialog),
                                         ("Tag entlasten",app.show_day_relief)):
                        modal(title,opener,geometry)
                checks.append("Neue Dialoge bei Mindestfenster und großer Schrift: fester erreichbarer Fuß, Inhalte bis unten scrollbar")
                callbacks = []
                for _index in range(12):
                    previous_jobs = set(app._daily_jobs)
                    previous_service = app._calendar_service
                    app.init_daily_planning()
                    pending = set(root.tk.splitlist(root.tk.call("after", "info")))
                    assert previous_service.closed and not previous_jobs.intersection(pending)
                    assert not previous_jobs.intersection(app._after_ids)
                    assert len(app._daily_jobs) == 1
                dialog, _body, _footer = app._daily_dialog("Timer-Lebensdauer")
                job = app._daily_after(10000, lambda: callbacks.append("veralteter Dialog"), owner=dialog)
                assert job in app._daily_jobs
                dialog.destroy()
                assert job not in app._daily_jobs and job not in app._after_ids
                assert job not in root.tk.splitlist(root.tk.call("after", "info"))
                jobs = set(app._daily_jobs)
                app.close_daily_planning()
                assert not app._daily_jobs and not jobs.intersection(app._after_ids)
                assert not jobs.intersection(root.tk.splitlist(root.tk.call("after", "info")))
                pump()
                assert not callbacks
                checks.append("Zwölf Dienstwechsel und echter Dialogabbau: alle ersetzten Tcl-Timer sofort entfernt, kein später Rückruf")
            assert not errors, errors
            if "hinweise" in cases:
                app.settings["daily_hints"]["enabled"]=True
                assert app.save_settings()
                expected=Path(folder)/"neustart-erwartung.json"
                expected.write_text(json.dumps(app.settings["daily_hint_state"],ensure_ascii=False))
        finally:
            app.cancel_pending_callbacks()
            app.release_data_lock()
            root.destroy()
        if "hinweise" in cases:
            child=subprocess.run([sys.executable,"-B",str(Path(__file__).resolve()),"--app",str(app_path),
                                  "--neustart-daten",folder,"--neustart-zeit",moment.isoformat(),
                                  "--neustart-erwartung",str(expected)],capture_output=True,text=True,
                                 encoding="utf-8",timeout=60)
            assert child.returncode==0,child.stdout+child.stderr
            assert "Tatsächlicher Neustart: keine doppelte Zustellung" in child.stdout
            checks.append("Tatsächlicher neuer App-Prozess: gespeicherte Belege unverändert, keine doppelte Zustellung")
        result=dict(version=mod.APP_VERSION,checks=checks,callback_errors=errors,hinweise=notices,
                    app_sha256=__import__("hashlib").sha256(app_path.read_bytes()).hexdigest())
        if report:
            report.parent.mkdir(parents=True,exist_ok=True)
            report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
        print(json.dumps(result,ensure_ascii=False))



def restart(app_path,folder,moment,expected):
    os.environ.update(GLIDE_DATA_DIR=folder,GLIDE_TEST_MODE="1",TZ="Europe/Berlin")
    sys.path.insert(0,str(app_path.parent))
    loader=importlib.machinery.SourceFileLoader("glide_tagesplanung3390_neustart",str(app_path))
    mod=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader))
    sys.modules[loader.name]=mod
    loader.exec_module(mod)
    root=mod.tk.Tk()
    app=mod.ListApp(root)
    errors=[]
    root.report_callback_exception=lambda *exc:errors.append(repr(exc[1]))
    try:
        now=datetime.fromisoformat(moment).astimezone(app._daily_resolver("Europe/Berlin"))
        app.daily_now=lambda:now
        before=json.loads(expected.read_text())
        assert app.settings["daily_hint_state"]==before
        assert app.process_daily_hints()==()
        assert app.settings["daily_hint_state"]==before
        root.update_idletasks();root.update()
        assert app.process_daily_hints()==() and not errors,errors
        print("Tatsächlicher Neustart: keine doppelte Zustellung")
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--app",type=Path,default=Path(__file__).resolve().parents[2]/"src/glide/app.pyw")
    parser.add_argument("--fall",choices=("hinweise","kalender","entlasten","dialoge"))
    parser.add_argument("--report",type=Path)
    parser.add_argument("--neustart-daten")
    parser.add_argument("--neustart-zeit")
    parser.add_argument("--neustart-erwartung",type=Path)
    args=parser.parse_args()
    if args.neustart_daten:
        restart(args.app.resolve(),args.neustart_daten,args.neustart_zeit,args.neustart_erwartung)
        return
    run(args.app.resolve(),[args.fall] if args.fall else ["hinweise","kalender","entlasten","dialoge"],args.report)


if __name__=="__main__":
    main()
