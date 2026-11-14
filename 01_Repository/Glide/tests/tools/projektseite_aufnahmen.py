#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Reproduzierbare Windows-Aufnahmen der echten Glide-Fenster für GitHub.

Lädt den Showcase in eine temporäre Ablage. Aufruf aus 01_Repository/Glide:

    py -3.14 -B tests/tools/projektseite_aufnahmen.py --out assets/marketing

Einzelne Szenen können als name=design:art[:titel] angegeben werden.
"""
from __future__ import annotations

import argparse
from datetime import date, timedelta
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile

from releasedaten import save_windows_screenshot
from showcase import BRIEFING_TITLE, FOCUS_TASK, MAIN_TITLE, PHOTO_TITLE, PIXEL_TITLE

REPO = Path(__file__).resolve().parents[2]
SHOWCASE = REPO / "tests/fixtures/showcase/Glide-Showcase_App.glideapp"
LISTEN_SZENEN = ("list", "board", "table", "split", "item")
ARTEN = ("home", "today", "calendar", "global", "pages", "relief", "locations",
         "settings", "week", *LISTEN_SZENEN)
GALERIE = (
    ("pinnwand", "light", "global", ""),
    ("kalender", "light", "calendar", ""),
    ("liste", "light", "list", "Studioroutinen"),
    ("seite", "light", "list", BRIEFING_TITLE),
    ("geteilt", "light", "split", MAIN_TITLE),
    ("startseite", "light", "home", ""),
    ("pixel", "pixel", "list", PIXEL_TITLE),
    ("heute", "dark", "today", ""),
    ("seitenuebersicht", "light", "pages", ""),
    ("punkt", "light", "item", MAIN_TITLE),
    ("tag-entlasten", "light", "relief", ""),
    ("fundorte", "light", "locations", ""),
    ("wochenrueckblick", "light", "week", ""),
    ("einstellungen", "light", "settings", ""),
    ("raumstudien", "light", "list", PHOTO_TITLE),
)


def szene(text):
    """`name=design:art[:titel]` in ein Tupel zerlegen; Fehler früh melden."""
    name, gleich, rest = text.partition("=")
    design, _, rest = rest.partition(":")
    art, _, titel = rest.partition(":")
    if not gleich or not name or art not in ARTEN or (art in LISTEN_SZENEN and not titel):
        raise argparse.ArgumentTypeError(f"Ungültige Szene: {text}")
    return name, design, art, titel


def lade_app(daten, app_pfad):
    os.environ["GLIDE_DATA_DIR"] = str(daten)
    os.environ.pop("GLIDE_TEST_MODE", None)
    sys.path.insert(0, str(app_pfad.parent))
    loader = importlib.machinery.SourceFileLoader("glide_projektseite", str(app_pfad))
    modul = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = modul
    loader.exec_module(modul)
    return modul


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--showcase", type=Path, default=SHOWCASE)
    parser.add_argument("szenen", nargs="*", type=szene)
    parser.add_argument("--prefix", default="glide-3.60-")
    args = parser.parse_args(argv)
    if sys.platform != "win32":
        raise SystemExit("Aufnahme nur unter Windows; für Linux tests/tools/screenshots.py verwenden.")
    scenes = args.szenen or [(args.prefix + name, design, art, title)
                             for name, design, art, title in GALERIE]
    args.out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="glide-projektseite-") as ordner:
        modul = lade_app(Path(ordner) / "Glide", REPO / "src/glide/app.pyw")
        root = modul.tk.Tk()
        app = modul.ListApp(root)
        if not app.restore_app_backup(str(args.showcase), sections={
                "tasks": True, "settings": True, "templates": True, "activity": True}, show_success=False):
            raise SystemExit("Showcase nicht geladen")
        import interaction_policy
        app.settings[interaction_policy.HINTS_SETTING] = False
        root.geometry("1480x950+24+24")
        manifest = args.showcase.with_name("manifest.json")
        anchor = date.fromisoformat(json.loads(manifest.read_text(encoding="utf-8"))["bearbeitungstag"]) \
            if manifest.is_file() else date.today()
        errors = []

        def callback_error(_kind, error, _traceback):
            errors.append(error)
            root.quit()

        root.report_callback_exception = callback_error
        app.settings["release_notes_seen"] = modul.APP_VERSION
        projektaufgaben = next(entry["items"] for entry in app.lists if entry["title"] == MAIN_TITLE)
        focus_item = next(item for item in projektaufgaben if item.get("text") == FOCUS_TASK)

        def finde(titel):
            treffer = [e["id"] for e in app.lists if (e.get("title") or "").startswith(titel)]
            if len(treffer) != 1:
                raise ValueError(f"Liste {titel!r} nicht eindeutig gefunden")
            return treffer[0]

        def aufnehmen(name, fenster):
            ziel = args.out / f"{name}.png"
            save_windows_screenshot(fenster, ziel)
            print("Aufgenommen", ziel.name, flush=True)

        def modal_aufnehmen(name, art, command):
            run_modal = app.run_modal

            def vorbereiten(dialog, parent=None):
                def aufnehmen_und_schliessen():
                    try:
                        if art == "relief":
                            tree = next(w for w in app.iter_descendants(dialog)
                                        if w.winfo_name() == "day_relief_tasks")
                            druck = next(item for item in projektaufgaben
                                         if item.get("text") == "Druckdatei für den Eingang bauen")
                            tree.selection_set(druck["id"])
                            ziel = next(w for w in app.iter_descendants(dialog)
                                        if isinstance(w, modul.tk.Entry) and
                                        w.cget("textvariable").startswith("PY_VAR"))
                            ziel.delete(0, "end")
                            ziel.insert(0, (anchor + timedelta(days=3)).strftime("%d.%m.%Y"))
                            tree.event_generate("<<TreeviewSelect>>")
                            dialog.update_idletasks()
                        aufnehmen(name, dialog)
                    except Exception as error:
                        errors.append(error)
                    finally:
                        dialog.destroy()

                if art == "relief":
                    dialog.geometry("1000x865")
                elif art == "locations":
                    dialog.geometry("960x630")
                dialog.after(850, aufnehmen_und_schliessen)
                run_modal(dialog, parent)

            app.run_modal = vorbereiten
            try:
                command()
            finally:
                app.run_modal = run_modal

        def schritt(index=0):
            if errors or index >= len(scenes):
                root.quit()
                return
            name, design, art, titel = scenes[index]
            app.close_side_view()
            app.close_task_inspector()
            if design:
                app.set_design(design)
            if art == "home":
                app.set_home_view()
            elif art == "today":
                app.set_plan_day_view(day=anchor.isoformat())
            elif art == "pages":
                app.set_pages_view()
            elif art == "calendar":
                app.settings["week_start"] = "monday"
                app._calendar_anchor = anchor
                app._calendar_selected_day = anchor.isoformat()
                app.open_calendar_view()
            elif art == "week":
                app.settings["week_start"] = "monday"
                app.show_week_review()
            elif art == "global":
                app.open_global_board()
                app.workspace.configure_board("zoom", 90)
            elif art == "relief":
                app.set_plan_day_view(day=anchor.isoformat())
                modal_aufnehmen(name, art, lambda: app.show_day_relief(days=[anchor.isoformat()]))
            elif art == "locations":
                app.open_global_board()
                modal_aufnehmen(name, art, lambda: app.show_usage_locations_dialog(("item", focus_item["id"])))
            elif art == "settings":
                modal_aufnehmen(name, art, app.show_settings_dialog)
            else:
                app.set_active_list(finde(titel))
                if art in ("board", "split"):
                    app.open_board_view()
                    if art == "split":
                        assert app.open_side_view(finde(BRIEFING_TITLE))
                elif art == "table":
                    app.set_table_view()
                elif art == "item":
                    app.workspace.set_mode("list")
                    app.edit_saved_item_details(focus_item["id"])
            if art in ("relief", "locations", "settings"):
                root.after(250, schritt, index + 1)
            else:
                def weiter():
                    aufnehmen(name, root)
                    schritt(index + 1)
                root.after(2200, weiter)

        root.after(2500, schritt)
        root.lift()
        try:
            root.mainloop()
        finally:
            app.cancel_pending_callbacks()
            app.release_data_lock()
            root.destroy()
        if errors:
            raise errors[0]
    return 0


if __name__ == "__main__":
    sys.exit(main())
