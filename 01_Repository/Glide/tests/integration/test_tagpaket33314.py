"""Tagespaket: echte Bedienung, Wechselwirkungen, Speicherfehler und Neustart."""
import argparse
import copy
from datetime import date, datetime, timedelta
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
parser.add_argument("--report", type=Path)
parser.add_argument("--capture", type=Path)
parser.add_argument("--measure", action="store_true")
parser.add_argument("--counterprobe", action="store_true")
args = parser.parse_args()
sys.path.insert(0, str(REPO / "tests/tools"))


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


with tempfile.TemporaryDirectory(prefix="glide-tagpaket-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_tagpaket", str(args.app.resolve()))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    checks, timings, errors, messages = [], [], [], []
    availability = {name: hasattr(mod.ListApp, name) for name in
                    ("start_day_proposal", "start_focus", "choose_time_block", "open_day_grid")}
    if args.counterprobe:
        result = dict(version=mod.APP_VERSION, available=availability,
                      expected_missing=True, exitcode=0 if all(availability.values()) else 1)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result))
        raise SystemExit(result["exitcode"])
    assert all(availability.values()), availability
    root = mod.tk.Tk()
    root.geometry("1280x800+20+20")
    root.report_callback_exception = lambda *exc: errors.append(str(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = app.show_info = lambda *a, **kw: messages.append(a)
    today, tomorrow = date.today().isoformat(), (date.today() + timedelta(days=1)).isoformat()

    def idle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    def fresh(identity):
        return app.find_item_in_lists(identity)[0]

    def button(parent, text):
        return next(w for w in descendants(parent) if isinstance(w, mod.RoundedButton) and w.text == text)

    def press(widget, key="<Return>"):
        widget.focus_force()
        idle()
        widget.event_generate(key)
        idle()

    def select(ids):
        app.set_today_view()
        app.settings["plan_day_grid"] = False
        app.sync_plan_day_grid()
        idle()
        rows = [row for identity in ids for row, source in app.in_progress_item_sources.items()
                if source[1] == identity and app.tree.exists(row)]
        assert len(rows) == len(ids), (ids, rows)
        app.tree.selection_set(rows)
        app.tree.focus(rows[0])
        app.tree.focus_force()
        idle()
        return rows

    def restart_check(identity, expected, journal=False):
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.withdraw()
        code = """
import importlib.machinery, importlib.util, sys
loader=importlib.machinery.SourceFileLoader('glide_restart',sys.argv[1])
mod=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader));loader.exec_module(mod)
root=mod.tk.Tk();app=mod.ListApp(root)
for _ in range(3): root.update()
item=app.find_item_in_lists(sys.argv[2])[0]
assert (item.get('time_spent_minutes') or 0)==int(sys.argv[3]), item
if sys.argv[4]=='journal':
    assert app.settings.get('time_booking') is None
    assert app.running_timer() is None
    assert app.stop_time_tracking()==0
else:
    assert app.running_timer()['focus'] and app.running_timer()['started_at'] is None
    assert app.timer_minutes()==int(sys.argv[5])
app.on_close()
"""
        result = subprocess.run([sys.executable, "-B", "-c", code, str(args.app.resolve()), identity,
                                 str(expected), "journal" if journal else "paused", str(app.timer_minutes())],
                                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
        assert result.returncode == 0, result.stderr
        assert app.acquire_data_lock() is None and not app._data_read_only, "Test muss seine isolierte Ablage wieder belegen"
        app.settings = app.load_settings()
        app.load_items()
        root.deiconify()
        app.update_timer_indicator()
        idle()

    try:
        idle()
        planned = app.new_item("Schon eingeplant", planned_date=today, estimated_minutes=60)
        complete = app.new_item("Schon erledigt", planned_date=today, estimated_minutes=30, done=True)
        unknown = app.new_item("Plan ohne Schätzung", planned_date=today)
        urgent = app.new_item("Dringende Freigabe", due=(date.today()-timedelta(days=2)).isoformat(), estimated_minutes=40)
        small = app.new_item("Kurzer Anruf", due=today, estimated_minutes=20)
        large = app.new_item("Langes Konzept", importance=3, estimated_minutes=120)
        missing = app.new_item("Noch ohne Aufwand", importance=2)
        blocked = app.new_item("Wartet auf Freigabe", importance=3, blocked_by=[urgent["id"]])
        future = app.new_item("Bewusst später", importance=3, planned_date=tomorrow)
        archived_item = app.new_item("Archiviertes", importance=3)
        first = app.new_list_object("Projekt Nord", [planned, complete, urgent, large])
        second = app.new_list_object("Projekt Süd", [unknown, small, missing, blocked, future])
        archived = app.new_list_object("Archiv", [archived_item]); archived["archived"] = True
        app.lists = [entry for entry in app.lists if app.is_inbox_list(entry)] + [first, second, archived]
        app.active_list_id = first["id"]
        app.items = first["items"]
        app.app_title = first["title"]
        app.set_active_list(first["id"])
        app.settings.update(daily_capacity_minutes=180, daily_capacity_by_weekday=[180]*7)
        app.save_settings(); app.save_items(); idle()
        original = copy.deepcopy(app.lists)
        depth = len(app.undo_stack)
        app.start_day_review(); idle()
        press(button(app.home_content, "Was passt heute?"))
        state = app._day_proposal
        rows = state["proposal"]["rows"]
        assert state["proposal"]["budget"] == 60, (state["proposal"]["budget"], app.planning_available(today))
        assert {row["item_id"] for row in rows} == {urgent["id"], small["id"], large["id"], missing["id"]}
        assert state["selected"] == {(first["id"], urgent["id"]), (second["id"], small["id"])}
        assert app.lists == original and len(app.undo_stack) == depth
        text = " ".join(w.cget("text") for w in descendants(app.home_content) if "text" in w.keys())
        assert "überfällig" in text and "heute fällig" in text and "30 Minuten" in text
        # Native checkbox invocation changes only the preview selection.
        check = next(w for w in descendants(app.home_content) if getattr(w, "_proposal_identity", None) ==
                     (second["id"], small["id"]))
        check.invoke(); idle(); assert len(state["selected"]) == 1 and app.lists == original
        check.invoke(); idle()
        # Capacity and day changes invalidate the whole preview before any mutation.
        app.settings["daily_capacity_by_weekday"] = [181]*7
        app.apply_day_proposal(); idle()
        assert app.lists == original and messages[-1][0] == "Tagesvorschlag aktualisiert"
        app.settings["daily_capacity_by_weekday"] = [180]*7
        app.start_day_proposal(); idle()
        real_date = mod.date
        class NextDay(real_date):
            @classmethod
            def today(cls): return real_date.today() + timedelta(days=1)
        with patch.object(mod, "date", NextDay): app.apply_day_proposal()
        assert app.lists == original
        app.start_day_proposal(); idle()
        # A deleted or archived source cannot be overwritten by a stale checkbox.
        first["archived"] = True
        app.apply_day_proposal(); idle()
        assert urgent["planned_date"] is None
        first["archived"] = False
        app.start_day_proposal(); idle()
        apply_button = button(app.template_actions, "Übernehmen & Raster")
        assert apply_button.winfo_ismapped()
        press(apply_button)
        assert fresh(urgent["id"])["planned_date"] == fresh(small["id"])["planned_date"] == today
        assert fresh(urgent["id"])["due"] == (date.today()-timedelta(days=2)).isoformat()
        assert fresh(missing["id"])["estimated_minutes"] is None
        assert len(app.undo_stack) == depth+1 and app.plan_grid_applicable()
        press(app.plan_grid_canvas, "<Control-z>")
        assert app.lists == original
        checks.append("Vorschau, Gründe, Kapazität/Tageswechsel/Archiv, Mehrfachquellen, ein Undo")

        # Keyboard targets share the existing date/time dialog and actual mutation entry.
        select([urgent["id"], small["id"]])
        depth = len(app.undo_stack)
        with patch.object(app, "themed_due_dialog", return_value=(today, "11:00")) as dialog:
            press(app.tree, "<Control-Shift-T>")
            assert dialog.call_args.kwargs["title"] == "Zeitblock"
        assert fresh(urgent["id"])["planned_time"] == "11:00"
        assert fresh(small["id"])["planned_time"] == "11:40"
        assert len(app.undo_stack) == depth+1
        app.undo_last_change(); idle()
        select([urgent["id"]])
        before, depth = copy.deepcopy(app.lists), len(app.undo_stack)
        with patch.object(app, "themed_due_dialog", return_value=None): press(app.tree, "<Control-Shift-T>")
        assert app.lists == before and len(app.undo_stack) == depth
        with patch.object(app, "themed_due_dialog", return_value=(today, "23:50")):
            press(app.tree, "<Control-Shift-T>")
        assert app.lists == before
        app.set_active_list(first["id"]); idle()
        app.entry.focus_force(); idle()
        assert app.current_focus_widget() is app.entry
        with patch.object(app, "themed_due_dialog") as dialog:
            press(app.entry, "<Control-Shift-T>")
            assert not dialog.called
        app.open_day_grid(); idle()
        press(app.plan_grid_canvas, "<Tab>")
        identity = app._plan_grid_focus_id
        with patch.object(app, "themed_due_dialog", return_value=(today, "10:00")):
            press(app.plan_grid_canvas)
        assert fresh(identity)["planned_time"] == "10:00"
        press(app.plan_grid_canvas, "<Alt-Down>")
        assert fresh(identity)["planned_time"] == "10:15"
        assert app.plan_grid_canvas.find_withtag("keyboard_focus")
        press(app.plan_grid_canvas, "<Delete>")
        assert fresh(identity)["planned_time"] is None and fresh(identity)["planned_date"] == today
        app.undo_last_change(); idle()
        assert fresh(identity)["planned_time"] == "10:15"
        press(app.plan_grid_canvas,"<Escape>")
        assert app.current_focus_widget() is app.plan_day_grid_button
        checks.append("Kürzel, Kalender/Escape, Mehrfach-Zeitblöcke, Raster-Tab/Pfeile/Entf, Editorfokus")

        # Focus: the real start shortcut and pause button, then controlled elapsed time.
        select([planned["id"]])
        press(app.tree, "<Control-Shift-F>")
        assert app.running_timer()["focus"] and app.focus_panel.winfo_ismapped()
        press(button(app.focus_panel, "Pause"))
        assert app.running_timer()["started_at"] is None
        assert app.timer_minutes(now=datetime.now().astimezone()+timedelta(hours=5)) == app.timer_minutes()
        app.stop_time_tracking(); idle()
        base = datetime.now().astimezone() + timedelta(minutes=10)
        assert app.start_focus(planned["id"], now=base)
        app.toggle_focus_pause(now=base+timedelta(seconds=125))
        assert app.timer_minutes(now=base+timedelta(hours=1)) == 3
        app.toggle_focus_pause(now=base+timedelta(hours=1))
        depth = len(app.undo_stack)
        spent_before = fresh(planned["id"]).get("time_spent_minutes") or 0
        app.finish_focus(complete=True, next_task=True, now=base+timedelta(hours=1, seconds=55)); idle()
        assert fresh(planned["id"])["done"]
        assert fresh(planned["id"])["time_spent_minutes"] == spent_before+3
        assert app.running_timer()["item_id"] != planned["id"] and len(app.undo_stack) == depth+1
        app.stop_time_tracking(now=base+timedelta(hours=1,seconds=55))
        app.undo_last_change(); idle()
        assert not fresh(planned["id"])["done"] and (fresh(planned["id"]).get("time_spent_minutes") or 0)==spent_before
        assert app.stop_time_tracking()==0
        checks.append("Fokusstart/Pause, Pause zählt nicht, genau einmal buchen, erledigen/weiter, gemeinsames Undo")

        # A capped booking changes no task time and must not absorb an older undo.
        capped = fresh(planned["id"])
        capped["time_spent_minutes"] = app.MAX_TIME_SPENT_MINUTES
        app.save_items()
        prior_clock = fresh(small["id"]).get("planned_time")
        app.apply_clock_assignments([(small["id"], today, "14:00")])
        depth = len(app.undo_stack)
        app.start_focus(planned["id"], now=base)
        app.finish_focus(complete=True, now=base+timedelta(seconds=125))
        assert fresh(planned["id"])["done"] and len(app.undo_stack) == depth+1
        app.undo_last_change(); idle()
        assert not fresh(planned["id"])["done"]
        assert fresh(planned["id"])["time_spent_minutes"] == app.MAX_TIME_SPENT_MINUTES
        assert fresh(small["id"])["planned_time"] == "14:00"
        app.undo_last_change(); idle()
        assert fresh(small["id"]).get("planned_time") == prior_clock
        fresh(planned["id"])["time_spent_minutes"] = spent_before
        app.save_items()
        checks.append("Zeitobergrenze: Abschluss-Undo erhält den vorherigen unabhängigen Zeitblock")

        # Storage failure before journal, before task commit and after task commit.
        base = datetime.now().astimezone()+timedelta(minutes=10)
        app.start_focus(planned["id"], now=base)
        with patch.object(app, "save_settings", return_value=False):
            assert app.stop_time_tracking(now=base+timedelta(seconds=125))==0
        assert app.settings.get("time_booking") is None and app.running_timer()
        depth = len(app.undo_stack)
        with patch.object(app, "save_items", return_value=False):
            assert app.stop_time_tracking(now=base+timedelta(seconds=125))==0
            assert (fresh(planned["id"]).get("time_spent_minutes") or 0)==spent_before
            assert app.settings["time_booking"] and len(app.undo_stack)==depth
            assert not app.start_focus(small["id"], now=base)
        assert app.stop_time_tracking(now=base+timedelta(seconds=300))==3
        assert fresh(planned["id"])["time_spent_minutes"]==spent_before+3
        app.start_focus(planned["id"], now=base)
        original_write = app.write_json_atomic
        def fail_clear(path, payload):
            if Path(path).name=="settings.json" and payload.get("time_booking") is None:
                raise OSError("controlled journal-clear failure")
            return original_write(path, payload)
        with patch.object(app, "write_json_atomic", side_effect=fail_clear):
            assert app.stop_time_tracking(now=base+timedelta(seconds=125))==0
            assert fresh(planned["id"])["time_spent_minutes"]==spent_before+6
            assert app.settings["time_booking"]
            app.undo_last_change()
            assert fresh(planned["id"])["time_spent_minutes"]==spent_before+6
            try: app.apply_clock_assignments([(planned["id"],today,"12:00")])
            except mod.glide_focus.PendingBookingError: pass
            else: raise AssertionError("Ungeklärte Buchung muss weitere Mutation sperren")
        restart_check(planned["id"], spent_before+6, journal=True)
        assert fresh(planned["id"])["time_spent_minutes"]==spent_before+6
        # Crash before task commit: prepared journal exists, tasks still have the old value.
        app.settings["time_booking"] = dict(item_id=planned["id"],before=spent_before+6,after=spent_before+9,minutes=3)
        app.save_settings()
        restart_check(planned["id"], spent_before+9, journal=True)
        assert fresh(planned["id"])["time_spent_minutes"]==spent_before+9
        app.settings["time_booking"] = dict(item_id=planned["id"],before=1,after=2,minutes=1)
        assert not app.recover_time_booking() and fresh(planned["id"])["time_spent_minutes"]==spent_before+9
        app.settings["time_booking"] = None
        app.save_settings()
        checks.append("Schreibfehler an drei Grenzen, Retry, Mutationssperre, beide Crashfenster, Konflikt verweigert")

        # Paused session survives a process restart without billing the gap.
        base = datetime.now().astimezone()+timedelta(minutes=10)
        app.start_focus(planned["id"], now=base)
        app.toggle_focus_pause(now=base+timedelta(seconds=125))
        restart_check(planned["id"], spent_before+9)
        assert app.timer_minutes(now=base+timedelta(days=1))==3
        app.stop_time_tracking()
        checks.append("Persistente Pause und Neustart ohne doppelte Buchung oder Pausenzeit")

        assert app.start_focus(planned["id"], now=datetime.now().astimezone()-timedelta(minutes=26))
        idle()
        assert app.running_timer()["started_at"] is None and app.timer_minutes()==25
        assert "Zeit für eine Pause" in app.focus_clock_label.cget("text")
        app.set_in_progress_view(); idle()
        assert not app.focus_panel.winfo_ismapped() and app.running_timer()
        app.set_today_view(); idle()
        assert app.focus_panel.winfo_ismapped()
        app.stop_time_tracking()
        app.start_day_proposal(); idle()
        before = copy.deepcopy(app.lists)
        app._data_read_only = True
        try:
            app.apply_day_proposal()
            assert app.apply_clock_assignments([(planned["id"],today,"12:00")])==0
            assert not app.start_focus(planned["id"])
            assert app.lists==before
        finally:
            app._data_read_only = False
        checks.append("Intervallende/Pausenhinweis, Ansichtswechsel und schreibgeschützter Bestand")

        # Real light/dark, font and geometry combinations; own-window captures only.
        for width,height in ((860,700),(1280,800)):
            for design in ("light","dark"):
                for size in ("mittel","gross"):
                    app.settings["ui_font_size"] = size
                    app.set_design(design,apply_now=False);app.apply_ui_font();app.apply_theme()
                    root.geometry(f"{width}x{height}+20+20");idle()
                    app.start_day_proposal();idle()
                    assert app.home_content.winfo_width()>200
                    assert button(app.template_actions,"Übernehmen & Raster").winfo_ismapped()
                    for check in descendants(app.home_content):
                        if isinstance(check,mod.tk.Checkbutton):
                            assert check.winfo_width()<=app.home_content.winfo_width()
                    if args.capture and size=="gross":
                        from releasedaten import save_windows_screenshot
                        args.capture.mkdir(parents=True,exist_ok=True)
                        save_windows_screenshot(root,args.capture/f"proposal_{width}x{height}_{design}.png")
                    app.start_focus(planned["id"]);idle()
                    assert not app.timer_button.winfo_ismapped(), "Fokus darf den Titel nicht doppelt mit einem Timer belegen"
                    assert app.focus_panel.winfo_height()<root.winfo_height()/2
                    for widget in descendants(app.focus_panel):
                        if isinstance(widget,mod.RoundedButton):
                            assert widget.winfo_rootx()+widget.winfo_width() <= root.winfo_rootx()+width
                    if args.capture and size=="gross":
                        save_windows_screenshot(root,args.capture/f"focus_{width}x{height}_{design}.png")
                    app.stop_time_tracking();idle()
        checks.append("16 Oberflächenkombinationen: Vorschlag/Fokus, Mindest-/Referenzgröße, Schrift, hell/dunkel")

        # Der echte modale Dialog reagiert auf Escape. Er steht am Ende, weil die
        # Prüf-App unter macOS im Hintergrundmodus nach einem nativen modalen
        # Fenster kein Schlüsselfenster und damit keinen Tk-Fokus mehr hat; alle
        # tastaturgetriebenen Prüfungen laufen deshalb vorher (Mac-Vollprüfung
        # 08.10.2026: bis dahin brach die Suite dort nach dem Dialog ab).
        root.geometry("1280x800+20+20"); app.set_design("light", apply_now=False); app.apply_theme(); idle()
        letzter = app.new_item("Escape-Prüfung")
        letzter["planned_date"] = today
        first_now = next(entry for entry in app.lists if entry["id"] == first["id"])
        first_now["items"].append(letzter); app.save_items(); idle()
        select([letzter["id"]])
        before, depth = copy.deepcopy(app.lists), len(app.undo_stack)

        def cancel_dialog(attempt=0):
            windows = [w for w in root.winfo_children() if isinstance(w, mod.tk.Toplevel) and w.title()=="Zeitblock"]
            if windows:
                windows[0].event_generate("<Escape>")
            elif attempt < 40:
                root.after(25, lambda: cancel_dialog(attempt+1))
        root.after(25, cancel_dialog)
        press(app.tree, "<Control-Shift-T>")
        assert app.lists == before and len(app.undo_stack) == depth
        checks.append("Echter Zeitblockdialog: Escape lässt Bestand und Undo unverändert")

        if args.measure:
            for count in (1000,10000):
                large_list = app.new_list_object("Messbestand", [app.new_item(f"Aufgabe {i}",importance=1,
                                                  estimated_minutes=(i%5+1)*10) for i in range(count)])
                app.lists.append(large_list)
                app._render_cache = {}
                samples=[]
                for repeat in range(6):
                    started=time.perf_counter(); proposal=app.day_proposal();elapsed=(time.perf_counter()-started)*1000
                    if repeat: samples.append(elapsed)
                ordered=sorted(samples)
                timings.append(dict(items=count,warm_ms=samples,median_ms=statistics.median(samples),
                                    p95_ms=ordered[-1],candidates=len(proposal["rows"])))
                app.lists.remove(large_list)
        idle()
        assert not errors,errors
        if args.report:
            args.report.parent.mkdir(parents=True,exist_ok=True)
            args.report.write_text(json.dumps(dict(version=mod.APP_VERSION,exitcode=0,checks=checks,
                app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(),timings=timings,callback_errors=errors,
                data="artificial; isolated GLIDE_DATA_DIR",manual_acceptance="open"),ensure_ascii=False,indent=2)+"\n",
                encoding="utf-8")
        print("test_tagpaket33314: OK; "+"; ".join(checks))
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        try: root.destroy()
        except mod.tk.TclError: pass
