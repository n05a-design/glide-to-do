"""Unprofilierte Messung der Suche (P07): Eingabe in der Palette bis zur gezeichneten Trefferliste.

Legt künstliche Daten an (Standard: 10.000 Punkte in 50 Listen mit
Beschreibungen, dazu 200 Seiten mit je rund 2.000 Zeichen Text), öffnet die
eingebettete Palette und misst je Suchbegriff die Zeit vom Setzen des Textes
bis nach `update_idletasks()` – also Treffer berechnen, Liste füllen und
zeichnen. Entscheidungsregel des Entwicklungsplans: Liegt der Median aller
Begriffe unter 100 ms, wird kein FTS5-Index gebaut.

Temporärer Datenordner, keine echten Nutzerdaten. --app wählt den Quellstand.
"""
import argparse
import importlib.machinery
import importlib.util
import json
import math
import os
import platform
import statistics
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BEGRIFFE = ("b", "be", "Bericht", "größe", "Quartal 3", "Lieferkette", "zzzyx")
WOERTER = ("Bericht", "Angebot", "Rechnung", "Termin", "Größe", "Lieferkette", "Quartal", "Kunde", "Projekt",
           "Entwurf", "Prüfung", "Übergabe", "Notiz", "Planung", "Abstimmung", "Budget")


def verteilung(werte):
    sortiert = sorted(werte)
    return {"median_ms": round(statistics.median(werte), 3),
            "p95_ms": round(sortiert[math.ceil(len(sortiert) * .95) - 1], 3),
            "stichproben_ms": [round(w, 3) for w in werte]}


def text(nummer, laenge):
    worte, i = [], nummer
    while sum(len(w) + 1 for w in worte) < laenge:
        worte.append(WOERTER[i % len(WOERTER)] + (f" {i % 97}" if i % 5 == 0 else ""))
        i = i * 31 + 7
    return " ".join(worte)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--items", type=int, default=10000)
    parser.add_argument("--pages", type=int, default=200)
    parser.add_argument("--rounds", type=int, default=9)
    args = parser.parse_args()
    sys.path.insert(0, str(args.app.parent))
    with tempfile.TemporaryDirectory(prefix="glide-messung-suche-") as ordner:
        os.environ["GLIDE_DATA_DIR"] = ordner
        os.environ["GLIDE_TEST_MODE"] = "1"
        loader = importlib.machinery.SourceFileLoader("glide_messung_suche", str(args.app))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = mod
        loader.exec_module(mod)
        root = mod.tk.Tk()
        root.geometry("1280x840+20+20")
        fehler = []
        root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
        app = mod.ListApp(root)
        app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
        try:
            je_liste = max(1, args.items // 50)
            for nummer in range(50):
                app.lists.append(app.new_list_object(
                    f"Liste {nummer} {WOERTER[nummer % len(WOERTER)]}",
                    [app.new_item(f"{text(nummer * je_liste + i, 30)}", description=text(i, 80))
                     for i in range(je_liste)]))
            for nummer in range(args.pages):
                seite = app.new_list_object(f"Seite {nummer}", [], list_kind=app.LIST_KIND_PAGE)
                seite["rich_note"] = {"text": text(nummer + 1000, 2000), "spans": [], "links": {}}
                app.lists.append(seite)
            app.save_items()
            app.set_home_view()
            root.update()
            app.show_quick_open()
            root.update()
            eingabe = next(w for w in _alle(root) if str(w).endswith("quick_open_entry"))
            ergebnisse = {}
            for begriff in BEGRIFFE:
                werte = []
                for runde in range(args.rounds + 1):
                    eingabe.delete(0, "end")
                    root.update_idletasks()
                    start = time.perf_counter()
                    eingabe.insert(0, begriff)
                    root.update_idletasks()
                    dauer = (time.perf_counter() - start) * 1000
                    if runde:
                        werte.append(dauer)
                ergebnisse[begriff] = verteilung(werte)
            alle = [w for e in ergebnisse.values() for w in e["stichproben_ms"]]
            bericht = {
                "werkzeug": "messung_suche.py", "app_version": mod.APP_VERSION,
                "punkte": je_liste * 50, "seiten": args.pages, "runden_warm": args.rounds,
                "umgebung": {"python": platform.python_version(), "tk": str(root.tk.call("info", "patchlevel")),
                             "plattform": platform.platform()},
                "begriffe": ergebnisse, "gesamt": verteilung(alle),
                "regel": "Median aller Begriffe unter 100 ms: kein FTS5-Index (Entwicklungsplan P07)",
                "callbackfehler": fehler,
            }
            args.json.parent.mkdir(parents=True, exist_ok=True)
            args.json.write_text(json.dumps(bericht, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({k: v["median_ms"] for k, v in ergebnisse.items()}, ensure_ascii=False))
            print("gesamt", bericht["gesamt"]["median_ms"], "ms Median,", bericht["gesamt"]["p95_ms"], "ms p95")
        finally:
            try:
                app.cancel_pending_callbacks()
                app.release_data_lock()
            except Exception:
                pass
            root.destroy()


def _alle(widget):
    for kind in widget.winfo_children():
        yield kind
        yield from _alle(kind)


if __name__ == "__main__":
    main()
