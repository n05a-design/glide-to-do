"""Wiederholte Prüf- und Messaufrufe je Bedienschritt zählen und Einsparung abschätzen.

Aufruf (aus diesem Ordner):
    xvfb-run -a -s "-screen 0 1280x860x24" python3 -B pruefaufrufe_probe.py \
        --variante basis --json ../ergebnisse/basis_1000.json
    … --variante einmal --json ../ergebnisse/einmal_1000.json

`basis` misst den unveränderten Stand. `einmal` ersetzt vier Stellen nur im
laufenden Prozess durch ihre einmal berechnete Fassung (W1, W2, W4, W5 der
Auswertung). Der Quellcode bleibt unverändert; die Variante belegt nur die
Größenordnung der Einsparung, sie ist keine Produktionsänderung.

Künstliche Daten in einem temporären `GLIDE_DATA_DIR`; echte Daten werden nie
berührt.
"""

import argparse
import cProfile
import functools
import json
import os
import pstats
import statistics
import math
import sys
import time
import types
from datetime import date, datetime, timedelta

import _glide_laden as gl  # noqa: E402

# Funktionen, deren Aufrufzahl je Schritt erfasst wird: (Datei, Funktionsname)
ZAEHLEN = (
    ("font.py", "__init__"), ("font.py", "measure"), ("font.py", "metrics"), ("font.py", "families"),
    ("app.pyw", "ui_font_family"), ("app.pyw", "available_font_families"),
    ("app.pyw", "pixel_heading_family"), ("app.pyw", "content_column_widths"),
    ("app.pyw", "hint_line_height"), ("app.pyw", "page_chips"), ("app.pyw", "_page_chips"),
    ("app.pyw", "due_status"), ("view_metrics.py", "summarize"),
    ("_strptime.py", "_strptime"), ("app.pyw", "has_active_filter"),
    ("app.pyw", "mix_hex_colors"), ("app.pyw", "contrast_ratio"),
)


def einmal_variante(app, modul, root):
    """Vier wiederholte Berechnungen nur für diese Probe durch einmalige ersetzen."""
    import tkinter.font as tkfont

    # W1: Die Tabellenansicht verwirft das Ergebnis ohnehin (sync_task_tree_columns).
    original_breiten = app.content_column_widths

    def content_column_widths(self):
        if self.view_mode == self.TABLE_VIEW or self.is_library_view():
            return None
        return original_breiten()
    app.content_column_widths = types.MethodType(content_column_widths, app)

    # W2: Zeilenhöhe je Schrift einmal ermitteln.
    zeilenhoehe = {}

    def hint_line_height(self, zeilen, label=None):
        hinweis = label or self.hint_label
        schluessel = str(hinweis.cget("font"))
        hoehe = zeilenhoehe.get(schluessel)
        if hoehe is None:
            hoehe = zeilenhoehe[schluessel] = tkfont.Font(root=self.root, font=hinweis.cget("font")).metrics("linespace")
        rand = 2 * (int(float(hinweis.cget("pady") or 0)) + modul.CanvasLabel.LABEL_INSET_Y)
        return zeilen * hoehe + rand
    app.hint_line_height = types.MethodType(hint_line_height, app)

    # W4: Kennzahlen einmal je Aktualisierung (bis zum nächsten Leerlauf).
    original_chips = app.page_chips
    zwischen = {}

    def page_chips(self):
        if "wert" not in zwischen:
            zwischen["wert"] = original_chips()
            root.after_idle(zwischen.clear)
        return zwischen["wert"]
    app.page_chips = types.MethodType(page_chips, app)

    # W5: Datum einmal je Zeichenkette lesen statt strptime je Aufruf.
    @functools.lru_cache(maxsize=4096)
    def datum(wert):
        try:
            return datetime.strptime(wert, "%Y-%m-%d").date()
        except ValueError:
            return None

    def due_status(self, item):
        wert = item.get("due")
        if not wert:
            return ""
        faellig = datum(wert)
        if faellig is None:
            return ""
        if item.get("done"):
            return "future"
        delta = (faellig - date.today()).days
        return "overdue" if delta < 0 else "today" if delta == 0 else "soon" if delta <= 2 else "future"
    app.due_status = types.MethodType(due_status, app)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--code", default=None, help="Codeordner (Standard src/glide)")
    parser.add_argument("--punkte", type=int, default=1000)
    parser.add_argument("--runden", type=int, default=9)
    parser.add_argument("--variante", choices=("basis", "einmal"), default="basis")
    parser.add_argument("--json", required=True)
    args = parser.parse_args()

    daten = gl.isolieren("glide-pruefaufrufe-")
    modul = gl.glide_laden(args.code)
    import tkinter as tk
    root = tk.Tk()
    root.geometry("1280x840+0+0")
    fehler = []
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))

    profil_start = cProfile.Profile()
    profil_start.enable()
    app = modul.ListApp(root)
    root.update()
    profil_start.disable()

    heute = date.today()
    liste = app.lists[0]
    for i in range(args.punkte):
        liste["items"].append(app.new_item(
            f"Aufgabe {i} mit etwas Text", importance=i % 4,
            due=(heute + timedelta(days=i % 9 - 2)).isoformat() if i % 3 == 0 else None,
            planned_date=heute.isoformat() if i % 5 == 0 else None))
    app.save_items()
    root.update()
    if args.variante == "einmal":
        einmal_variante(app, modul, root)
    punkt = liste["items"][0]["id"]

    schritte = [
        ("liste", lambda: app.set_active_list(liste["id"])),
        ("startseite", app.set_home_view),
        ("mein_tag", app.set_today_view),
        ("tabelle", app.set_table_view),
        ("liste_abhaken", lambda: (app.set_active_list(liste["id"]), root.update(),
                                   app.toggle_item_done_anywhere(punkt))),
    ]

    def zaehlen(profil):
        stats = pstats.Stats(profil).stats
        ergebnis = {}
        for (datei, _zeile, name), (_cc, aufrufe, _tt, _ct, _callers) in stats.items():
            for z_datei, z_name in ZAEHLEN:
                basis = os.path.basename(datei)
                passend = basis == z_datei or (z_datei == "app.pyw" and basis.startswith("Glide-") and basis.endswith(".pyw"))
                if passend and name == z_name:
                    ergebnis[f"{z_datei}:{z_name}"] = ergebnis.get(f"{z_datei}:{z_name}", 0) + aufrufe
        return ergebnis

    ergebnis = {
        "werkzeug": "pruefaufrufe_probe.py", "variante": args.variante, "punkte": args.punkte,
        "runden_warm": args.runden, "umgebung": gl.umgebung(root), "app_version": modul.APP_VERSION,
        "start_aufrufe": zaehlen(profil_start), "schritte": {},
    }
    for name, aktion in schritte:
        start_kalt = time.perf_counter()
        aktion()
        root.update()  # erster Durchlauf; danach warme Runden
        kalt_ms = (time.perf_counter() - start_kalt) * 1000
        werte = []
        for _ in range(args.runden):
            start = time.perf_counter()
            aktion()
            root.update()
            werte.append((time.perf_counter() - start) * 1000)
        profil = cProfile.Profile()
        profil.enable()
        aktion()
        root.update()
        profil.disable()
        werte.sort()
        ergebnis["schritte"][name] = {
            "median_ms": round(statistics.median(werte), 1),
            "erster_ms": round(kalt_ms, 3),
            "p95_ms": round(werte[math.ceil(len(werte) * .95) - 1], 3),
            "max_ms": round(werte[-1], 1),
            "roh_ms": [round(w, 1) for w in werte],
            "aufrufe": zaehlen(profil),
        }
    app.set_active_list(liste["id"])
    root.update()
    ergebnis["kennzahlen_liste"] = app.page_chips()
    ergebnis["callbackfehler"] = fehler
    ergebnis["fehlerprotokoll"] = gl.fehlerprotokoll(daten)
    root.destroy()
    gl.aufraeumen()
    with open(args.json, "w", encoding="utf-8") as datei:
        json.dump(ergebnis, datei, ensure_ascii=False, indent=1)
    print(json.dumps({k: v["median_ms"] for k, v in ergebnis["schritte"].items()}))
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
