#!/usr/bin/env python3.12
"""Bildschirmaufnahmen der Oberflaeche fuer die Sichtpruefung.

Kein Test, sondern ein Werkzeug: Es baut eine Beispiel-Ablage auf, oeffnet
nacheinander die interessanten Ansichten und legt zu jeder eine PNG-Datei ab.
Damit laesst sich nach einer Layoutaenderung nachsehen, ob Abstaende, Hoehen
und Ausrichtungen stimmen, ohne die App von Hand zu bedienen.

Das Werkzeug liegt bewusst im Repository und nicht in einem Arbeitsordner:
Aufnahmen, deren Erzeuger nur lokal existiert, lassen sich spaeter nicht
wiederholen.

Aufruf (Linux, benoetigt ImageMagick):

    xvfb-run -a --server-args="-screen 0 1400x1100x24" \\
        python3.12 tests/tools/screenshots.py --out /tmp/shots

Unter Windows und macOS ist keine Aufnahme vorgesehen; dort wird von Hand
geprueft (siehe Arbeitsvorbereitung, Manuelle_Pruefung).
"""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import os
import pathlib
import subprocess
import sys
import tempfile
from datetime import date, timedelta

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
APP_PATH = REPOSITORY_ROOT / "src" / "glide" / "app.pyw"


def load_module(temp_root):
    """Laedt app.pyw mit isoliertem Datenverzeichnis.

    GLIDE_DATA_DIR muss vor dem Import gesetzt sein: Die echten Nutzerdaten
    duerfen von einem Aufnahmelauf niemals beruehrt werden.
    """
    os.environ["GLIDE_DATA_DIR"] = str(pathlib.Path(temp_root) / "Glide")
    # Ein SourceFileLoader ist nötig: Die Endung .pyw erkennt der Importmechanismus
    # nicht von selbst als Quelltext.
    loader = importlib.machinery.SourceFileLoader("glide_app", str(APP_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules["glide_app"] = module
    loader.exec_module(module)
    return module


def capture(target):
    """Nimmt den X-Bildschirm auf. Gibt zurueck, ob eine Datei entstanden ist."""
    try:
        subprocess.run(
            ["import", "-window", "root", str(target)],
            check=True, capture_output=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return target.is_file()


class Recorder:
    """Haelt Ziel und Zaehler, damit die Dateinamen ihre Reihenfolge tragen."""

    def __init__(self, root, out_dir):
        self.root = root
        self.out_dir = out_dir
        self.index = 0
        self.failures = []

    def settle(self, rounds=3):
        for _ in range(rounds):
            self.root.update_idletasks()
            self.root.update()

    def take(self, name):
        self.index += 1
        self.settle()
        target = self.out_dir / f"{self.index:02d}_{name}.png"
        ok = capture(target)
        print(f"  {'OK ' if ok else 'FEHLT'} {target.name}")
        if not ok:
            self.failures.append(target.name)
        return ok

    def take_dialog(self, name, opener, before_shot=None, delay=600):
        """Oeffnet einen modalen Dialog, nimmt ihn auf und schliesst ihn wieder.

        Der Dialog blockiert bis zum Schliessen; die Aufnahme muss deshalb aus
        einem after-Aufruf heraus geschehen.
        """
        def run():
            self.settle()
            dialog = self._topmost()
            if dialog is None:
                self.failures.append(name)
                return
            if before_shot is not None:
                try:
                    before_shot(dialog)
                except Exception as error:  # Werkzeug: Lauf nicht abbrechen
                    print(f"  Hinweis: {name}: {error}")
            self.take(name)
            for window in self._all_tops():
                try:
                    window.destroy()
                except Exception:
                    pass

        self.root.after(delay, run)
        opener()

    def _all_tops(self):
        import glide_app as mod

        found = []

        def walk(widget):
            for child in widget.winfo_children():
                if isinstance(child, mod.tk.Toplevel):
                    found.append(child)
                walk(child)

        walk(self.root)
        return found

    def _topmost(self):
        tops = self._all_tops()
        return tops[-1] if tops else None


def build_demo(app, mod):
    """Beispielinhalt mit Labels, Arten, Fristen und einer zweiten Liste."""
    today = date.today()
    for name, color in (("Kunde", "accent"), ("Intern", "flag"), ("Druck", "export")):
        app.labels.append(app.new_label_object(name, None, color))
    kunde, intern, druck = app.labels[-3:]

    def item(text, **kwargs):
        return app.new_item(text, **kwargs)

    briefing = app.current_list()
    briefing["title"] = "01 Briefing & Zielbild"
    briefing["note"] = (
        "Was hier nicht geklärt wird, kostet in Phase 5 das Dreifache. "
        "Diese Liste ist erst fertig, wenn das Zielbild steht."
    )
    briefing["labels"] = [kunde["id"]]

    group = item("Freigaben", kind=app.ITEM_KIND_GROUP)
    group["children"] = [
        item("Korrekturabzug an die Geschäftsführung",
             due=(today + timedelta(days=3)).isoformat(), due_time="10:30",
             importance=2, labels=[intern["id"]]),
        item("Freigabe dokumentieren", done=True),
    ]
    # In-place, damit app.items dieselbe Liste bleibt.
    briefing["items"][:] = [
        item("Beschaffung", kind=app.ITEM_KIND_HEADING),
        item("Farbmessgerät für die Druckkontrolle anschaffen",
             due=(today + timedelta(days=30)).isoformat(), labels=[druck["id"]]),
        item("Zweiten Monitor für den Arbeitsplatz Reinzeichnung",
             due=(today - timedelta(days=2)).isoformat(), importance=3),
        group,
        item("Langtext, der über mehrere Zeilen läuft und deshalb als Long-Task "
             "geführt wird, damit die Liste ihn vollständig zeigt",
             kind=app.ITEM_KIND_LONG, labels=[kunde["id"], intern["id"]]),
        item("Bildauswahl mit der Redaktion abstimmen", done=True),
    ]

    second = app.new_list_object("02 Produktion", [], None, None, None, "", None, [intern["id"]])
    second["items"][:] = [item("Reinzeichnung"), item("Belichtung prüfen", importance=1)]
    app.lists.append(second)

    # Ein Ordner mit Inhalt: An ihm zeigt sich das Klappdreieck der Seitenleiste.
    folder = app.new_folder_object("Projekte")
    app.folders.append(folder)
    inside = app.new_list_object("Neubau Nordseite", [], None, None, None, "", None, [])
    inside["items"][:] = [item("Grundriss prüfen"), item("Fassade abstimmen")]
    inside["folder_id"] = folder["id"]
    app.lists.append(inside)

    # Eine dritte Liste ganz ohne Labels: An ihr zeigt sich, ob der Kopfbereich
    # beim Wechsel springt.
    third = app.new_list_object("03 Ohne Labels", [], None, None, None, "", None, [])
    third["items"][:] = [item("Nachbereitung")]
    app.lists.append(third)

    app.save_items()
    app.update_sidebar_list()
    # Erst der Wechsel auf die Liste bindet app.items neu an ihren Inhalt.
    app.set_active_list(briefing["id"])
    return briefing["items"][1]


def main():
    parser = argparse.ArgumentParser(description="Aufnahmen der Glide-Oberflaeche")
    parser.add_argument("--out", default="/tmp/glide-shots", help="Zielordner der PNG-Dateien")
    args = parser.parse_args()
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_root:
        mod = load_module(temp_root)
        for name in ("showinfo", "showwarning", "showerror"):
            setattr(mod.messagebox, name, lambda *a, **k: None)
        mod.messagebox.askyesno = lambda *a, **k: True

        root = mod.tk.Tk()
        app = mod.ListApp(root)
        # Nach dem Aufbau: ListApp setzt im Konstruktor selbst 1000x800.
        root.geometry("1180x860+0+0")
        detail_item = build_demo(app, mod)
        rec = Recorder(root, out_dir)

        print(f"Aufnahmen nach {out_dir}:")
        for theme in ("hell", "dunkel"):
            wanted = "light" if theme == "hell" else "dark"
            if app.theme_name != wanted:
                app.toggle_theme()
            app.refresh_tree()
            rec.take(f"hauptfenster_{theme}")

            # Ansicht "Labels": Gruppen in Labelfarbe, Punkte darunter.
            app.set_labels_view()
            rec.take(f"labelansicht_{theme}")
            app.set_active_list(app.lists[0]["id"])

            # Liste ohne Labels: Der Kopfbereich darf nicht springen.
            app.set_active_list(app.lists[-1]["id"])
            rec.take(f"kopf_ohne_labels_{theme}")
            app.set_active_list(app.lists[0]["id"])

            rec.take_dialog(
                f"punktdetails_{theme}",
                lambda item=detail_item: app.themed_item_details_dialog(item),
            )

            # Dieselbe Maske mit aufgeklappter Labelauswahl.
            def open_labels(dialog):
                for child in _walk(dialog):
                    if isinstance(child, mod.LabelDropdown):
                        child._open_popup()
                        rec.settle()
                        return
                raise RuntimeError("Labelauswahl nicht gefunden")

            rec.take_dialog(
                f"labelauswahl_offen_{theme}",
                lambda item=detail_item: app.themed_item_details_dialog(item),
                before_shot=open_labels,
            )

            rec.take_dialog(
                f"kalenderfenster_{theme}",
                lambda: app.themed_due_dialog("2026-10-03", "09:30"),
            )

        root.destroy()

    if rec.failures:
        print("Nicht erzeugt:", ", ".join(rec.failures))
        return 1
    print("Alle Aufnahmen erzeugt.")
    return 0


def _walk(widget):
    for child in widget.winfo_children():
        yield child
        yield from _walk(child)


if __name__ == "__main__":
    sys.exit(main())
