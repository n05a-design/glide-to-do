"""Ansichtsprobe: künstliche Beispieldaten anlegen und Hauptansichten fotografieren.

Aufruf:
    xvfb-run -a -s "-screen 0 1280x860x24" python3 ansichten_probe.py --ausgabe ../bilder

Fotografiert ausschließlich die Xvfb-Anzeige, auf der nur Glide läuft.
Der modale Kalender wird bewusst ausgelassen: `run_modal` blockiert bis zum
Schließen des Dialogs.
"""

import argparse
import json
import os
import time
import traceback
from datetime import date, timedelta

import _glide_laden as gl


def beispieldaten(app):
    heute = date.today()
    eintraege = [
        ("Angebot an Kunde schicken", 3, heute, heute),
        ("Präsentation vorbereiten", 2, heute + timedelta(days=3), heute),
        ("Steuerunterlagen sortieren", 1, heute - timedelta(days=2), None),
        ("Website-Texte prüfen", 2, None, heute + timedelta(days=1)),
        ("Zahnarzttermin vereinbaren", 0, heute + timedelta(days=7), None),
        ("Rechnung 2026-117 bezahlen", 3, heute, heute),
    ]
    punkte = [app.new_item(text, importance=wichtig, due=f.isoformat() if f else None,
                           planned_date=b.isoformat() if b else None, estimated_minutes=30)
              for text, wichtig, f, b in eintraege]
    punkte[0]["children"] = [app.new_item("Preise aktualisieren"), app.new_item("PDF erzeugen", done=True)]
    app.lists[0]["items"].extend(punkte)
    app.save_items()
    app.ask_template_fields = lambda offen, _titel: {name: "Beispiel" for name in offen}
    for vorlage in [t.get("id") for t in app.templates][:3]:
        app.create_list_from_template(vorlage)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", default=None)
    parser.add_argument("--ausgabe", required=True)
    args = parser.parse_args()
    os.makedirs(args.ausgabe, exist_ok=True)
    daten = gl.isolieren("glide-ansichten-")
    modul = gl.glide_laden(args.code)
    import tkinter as tk
    root = tk.Tk()
    root.geometry("1280x840+0+0")
    app = modul.ListApp(root)
    root.update()
    protokoll = {"umgebung": gl.umgebung(root), "ms": {}, "fehler": {}}
    beispieldaten(app)
    root.update()
    schritte = [
        ("liste", lambda: app.set_active_list(app.lists[0]["id"])),
        ("startseite", app.set_home_view),
        ("mein_tag", app.set_today_view),
        ("tabelle", app.set_table_view),
        ("bibliothek", app.set_library_view),
        ("seiten", app.set_pages_view),
        ("neue_seite", app.create_new_page),
        ("pinnwand", lambda: (app.set_active_list(app.lists[0]["id"]), app.open_board_view())),
    ]

    def ausfuehren(index=0):
        if index >= len(schritte):
            protokoll["fehlerprotokoll"] = gl.fehlerprotokoll(daten)
            print(json.dumps(protokoll, indent=1, ensure_ascii=False))
            root.destroy()
            return
        name, aktion = schritte[index]
        start = time.perf_counter()
        try:
            aktion()
            root.update()
        except Exception:
            protokoll["fehler"][name] = traceback.format_exc()[-800:]
        protokoll["ms"][name] = round((time.perf_counter() - start) * 1000)

        def foto():
            os.system(f"import -window root '{os.path.join(args.ausgabe, f'{index:02d}_{name}.png')}'")
            ausfuehren(index + 1)

        root.after(700, foto)

    root.after(500, ausfuehren)
    root.mainloop()


if __name__ == "__main__":
    main()
