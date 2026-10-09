"""U10/U19: Titel, Unterzeile, Quellen und bestehende Bedienbindungen.

--observe erfasst den Ausgangsstand ohne neue Anforderungen; Bilder zeigen
ausschließlich das eigene Fenster mit künstlichem Bestand (OB06).
"""
import argparse
import copy
from datetime import date
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
parser.add_argument("--observe", action="store_true")
parser.add_argument("--capture", type=Path)
parser.add_argument("--report", type=Path)
args = parser.parse_args()
sys.path.insert(0, str(REPO / "src/glide"))
sys.path.insert(0, str(REPO / "tests/tools"))

with tempfile.TemporaryDirectory(prefix="glide-titel-") as directory:
    os.environ["GLIDE_DATA_DIR"] = directory
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_titel_test", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1280x800+20+20")
    errors, observations = [], []
    root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **kw: errors.append(repr(a))

    def idle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    try:
        item = app.new_item("Unterlagen für den nächsten Arbeitsschritt prüfen", planned_date=date.today().isoformat())
        second = app.new_item("Entwurf besprechen", due=date.today().isoformat())
        entry = app.new_list_object("Projektplanung und tägliche Aufgaben", [item, second])
        entry["labels"] = []
        app.lists.append(entry)
        app.save_items()
        original = copy.deepcopy(app.lists)
        for size in ("mittel", "gross"):
            for design in ("light", "dark"):
                app.set_design(design, apply_now=False)
                app.settings["ui_font_size"] = size
                app.apply_ui_font()
                app.apply_theme()
                for width, height in ((1280, 800), (860, 700)):
                    root.geometry(f"{width}x{height}+20+20")
                    for view in ("list", "today"):
                        app.set_active_list(entry["id"]) if view == "list" else app.set_today_view()
                        idle()
                        label = app.title_label
                        observation = dict(size=size, design=design, width=width, height=height, view=view,
                                           title=label.cget("text"), title_width=label.winfo_width(),
                                           header_height=app.header_frame.winfo_height(),
                                           stats=app.stats_label.cget("text"))
                        observations.append(observation)
                        if not args.observe:
                            assert label.winfo_width() >= label.winfo_reqwidth(), observation
                            assert label.winfo_rootx() + label.winfo_width() <= app.title_row.winfo_rootx() + app.title_row.winfo_width(), observation
                            assert app.header_meta.master is app.subtitle_row
                            assert app.stats_label.winfo_rooty() >= label.winfo_rooty() + label.winfo_height(), observation
                            assert app.stats_label.cget("wraplength") == 0
                            if view == "today":
                                row = f"in-progress:{entry['id']}:{item['id']}"
                                assert app.tree.item(row, "text").startswith(item["text"])
                                assert app.format_due_column(item["planned_date"]) in app.tree.set(row, "due")
                                assert app.ICONS["calendar"] not in app.tree.set(row, "due"), "Sortierplatzhalter darf keine Fälligkeit anzeigen"
                                due_row = f"in-progress:{entry['id']}:{second['id']}"
                                assert app.format_due_column(second["due"]) in app.tree.set(due_row, "due")
                                assert entry["title"] not in app.tree.item(row, "text")
                                assert app._today_source_titles[row] == entry["title"]
                                shown = app.tree.set(row, "source")
                                assert shown and entry["title"].startswith(shown.rstrip("…"))
                                assert app.tree.column("source", "width") > 0
                                assert app.tree.column("#0", "width") >= 260
                                if int(root.tk.call("package", "require", "Tk").split(".")[0]) >= 9:
                                    assert root.tk.call(str(app.tree), "tag", "cell", "has", "today_source", (row, "source"))
                                assert str(root.tk.call(str(app.tree), "tag", "configure", "today_source", "-foreground")) == app.theme["muted"]
                        if args.capture and size == "mittel":
                            from releasedaten import save_windows_screenshot
                            args.capture.mkdir(parents=True, exist_ok=True)
                            root.tk.call("after", 200, "set", "::glide_title_capture", "1")
                            root.tk.call("vwait", "::glide_title_capture")
                            save_windows_screenshot(root, args.capture / f"{view}_{width}x{height}_{design}.png")
        assert app.lists == original, "Layout verändert den Bestand"
        if not args.observe:
            app.set_today_view()
            idle()
            row = f"in-progress:{entry['id']}:{item['id']}"
            app.tree.see(row)
            idle()
            x, y, w, h = app.tree.bbox(row, "source")
            app.tree.event_generate("<Button-1>", x=x + w // 2, y=y + h // 2)
            app.tree.event_generate("<ButtonRelease-1>", x=x + w // 2, y=y + h // 2)
            idle()
            assert app.tree.focus() == row and row in app.tree.selection()
            assert app.in_progress_item_sources[row] == (entry["id"], item["id"])
            root.focus_force()
            app.tree.focus_set()
            app.tree.event_generate("<Return>")
            idle()
            assert app.view_mode == "list" and app.active_list_id == entry["id"]
            assert "source" not in app.tree.cget("displaycolumns")
            assert app.tree.focus() == item["id"]
            app.tree.focus_set()
            app.tree.event_generate("<space>")
            idle()
            assert app.find_item_in_lists(item["id"])[0]["done"]
            root.event_generate("<Control-z>")
            idle()
            assert not app.find_item_in_lists(item["id"])[0]["done"]
            app.set_in_progress_view()
            idle()
            assert "source" not in app.tree.cget("displaycolumns")
            # Vor dem ersten Layout/bei verborgenem Start gibt es noch keine
            # Messbreite. Volltext erhalten; nach echter Messung kürzen.
            previous = app._stats_full_text
            full = "1000 Aufgaben · 1000 offen · " * 20
            with patch.object(app.subtitle_row, "winfo_width", return_value=1):
                app._set_stats_text(full)
                assert app.stats_label.cget("text") == full
                assert app.stats_label._glide_tooltip["source"] == full
            app.fit_stats_text()
            idle()
            assert app.stats_label.cget("text").endswith("…")
            assert app.stats_label._glide_tooltip["source"] == full
            assert app.stats_label.winfo_width() >= app.stats_label.winfo_reqwidth()
            app._set_stats_text(previous)
            observations.append(dict(initial_width_unknown=True, tooltip_full_text=True))
            # Ein langer Bestand zeigt die Bildlaufleiste. Derselbe Aufbau
            # löste anfangs eine endlose Folge von Breitenänderungen aus.
            layout_events = []
            def bounded_layout(event):
                layout_events.append(event.width)
                if len(layout_events) > 60:
                    raise SystemExit("Heute: Layout stabilisiert sich nicht")
            binding = app.tree.bind("<Configure>", bounded_layout, add="+")
            large = app.new_list_object("Großer Tagesbestand", [app.new_item(f"Arbeitsschritt {n}", planned_date=date.today().isoformat()) for n in range(1000)])
            app.lists.append(large)
            app.set_active_list(large["id"], refresh=False)
            app.set_today_view()
            idle()
            assert len(app.in_progress_item_sources) >= 1000
            assert len(layout_events) < 20, layout_events
            app.tree.unbind("<Configure>", binding)
            observations.append(dict(large_items=1000, tree_layout_events=len(layout_events)))
        assert not errors, errors
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(dict(version=mod.APP_VERSION, source_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(),
                                                  observations=observations, callback_errors=errors, observe=args.observe),
                                              ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"OK Titel: {len(observations)} Kombinationen; observe={args.observe}; keine Callbackfehler")
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
