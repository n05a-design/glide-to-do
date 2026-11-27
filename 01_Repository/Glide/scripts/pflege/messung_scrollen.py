#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Scrollkosten in Seite und Liste messen (PERF-01, 27.11.2026).

Aufruf (aus `01_Repository/Glide`):
    python3 -B scripts/pflege/messung_scrollen.py [--code ORDNER] [--groessen 10,100,500,1000]
                                                  [--schritte 40] [--json DATEI]

Je Größe wird eine künstliche Seite (Überschriften, Absätze, Aufzählungen,
Aufgabenzeilen) und eine Liste mit ebenso vielen Punkten geöffnet. Gescrollt
wird mit echten Mausradereignissen (`<MouseWheel>` bzw. Button-4/5 unter X11),
jeder Schritt bis die Ereignisschleife leer ist. Gemessen: Dauer je Schritt
(Median, p95, Maximum, unprofiliert, nach einem Aufwärmlauf), Zahl der
`yscrollcommand`-Rückrufe je Schritt und die darin verbrachte Zeit.
Künstliche Daten in einem temporären `GLIDE_DATA_DIR`. Die Zahlen gelten nur
für den gemessenen Rechner, Python und Tk; Trackpad-Ereignisse und macOS sind
damit nicht abgedeckt.
"""

import argparse
import json
import statistics
import sys
import time

import _glide_laden as gl


def p95(werte):
    werte = sorted(werte)
    return werte[max(0, round(0.95 * (len(werte) - 1)))] if werte else None


def seite_markdown(bloecke):
    zeilen = ["# Messseite", ""]
    for i in range(bloecke):
        art = i % 6
        if art == 0:
            zeilen += [f"## Abschnitt {i}", ""]
        elif art in (1, 2):
            zeilen += [f"Absatz {i}. " + "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 3, ""]
        elif art in (3, 4):
            zeilen.append(f"- Punkt {i} mit **fettem** Text und [Link](https://example.org/{i})")
        else:
            zeilen.append(f"- [ ] Aufgabe {i}")
    return "\n".join(zeilen)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--code")
    parser.add_argument("--groessen", default="10,100,500,1000")
    parser.add_argument("--schritte", type=int, default=40)
    parser.add_argument("--json")
    args = parser.parse_args()
    ordner = gl.isolieren("glide-scrollen-")
    mod = gl.glide_laden(args.code)
    root = mod.tk.Tk()
    root.geometry("1280x900+20+20")
    fehler = []
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
    app.show_info = lambda *a, **k: None
    x11 = root.tk.call("tk", "windowingsystem") == "x11"

    def ruhe(sekunden=0.2):
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            root.update()
            time.sleep(0.01)

    def rad(widget, richtung):
        if x11:
            widget.event_generate("<Button-5>" if richtung > 0 else "<Button-4>", x=200, y=200)
        else:
            widget.event_generate("<MouseWheel>", delta=-120 * richtung, x=200, y=200)

    def messen(widget, ziel, zaehler):
        dauer, rueckrufe, rueckrufzeit, stellen = [], [], [], []
        for runde in range(args.schritte * 2 + 2):
            richtung = 1 if (runde // (args.schritte + 1)) % 2 == 0 else -1
            zaehler["n"], zaehler["t"] = 0, 0.0
            start = time.perf_counter()
            rad(widget, richtung)
            root.update()
            dauer.append((time.perf_counter() - start) * 1000)
            rueckrufe.append(zaehler["n"])
            rueckrufzeit.append(zaehler["t"] * 1000)
            stellen.append(ziel())
        dauer, rueckrufe, rueckrufzeit = dauer[2:], rueckrufe[2:], rueckrufzeit[2:]  # Aufwärmen
        return {"ms_median": round(statistics.median(dauer), 3), "ms_p95": round(p95(dauer), 3),
                "ms_max": round(max(dauer), 3),
                "rueckrufe_je_schritt": round(statistics.mean(rueckrufe), 2),
                "rueckruf_ms_median": round(statistics.median(rueckrufzeit), 3),
                "bewegt": max(stellen) > 0}

    ergebnisse = {}
    for groesse in [int(g) for g in args.groessen.split(",") if g.strip()]:
        app.new_page_from_markdown(seite_markdown(groesse))
        ruhe(0.8)
        editor = app.rich_note_editor
        zaehler = {"n": 0, "t": 0.0}
        original = editor.text.cget("yscrollcommand")
        befehl = original

        def mitzaehlen(*werte, _b=befehl):
            start = time.perf_counter()
            zaehler["n"] += 1
            ergebnis = root.tk.call(_b, *werte)
            zaehler["t"] += time.perf_counter() - start
            return ergebnis

        editor.text.configure(yscrollcommand=root.register(mitzaehlen))
        editor.text.focus_force()
        ruhe(0.3)
        seite = messen(editor.text, lambda: editor.text.yview()[0], zaehler)
        editor.text.configure(yscrollcommand=original)

        liste = app.new_list_object(f"Messliste {groesse}", [])
        app.lists.append(liste)
        liste["items"] = [app.create_item(f"Punkt {i}") for i in range(groesse)] if hasattr(app, "create_item") \
            else [{"id": f"m{groesse}-{i}", "text": f"Punkt {i}", "done": False, "children": []} for i in range(groesse)]
        app.set_active_list(liste["id"])
        ruhe(0.8)
        lz = {"n": 0, "t": 0.0}
        baum_befehl = app.tree.cget("yscrollcommand")

        def baum_zaehlen(*werte, _b=baum_befehl):
            start = time.perf_counter()
            lz["n"] += 1
            ergebnis = root.tk.call(_b, *werte)
            lz["t"] += time.perf_counter() - start
            return ergebnis

        app.tree.configure(yscrollcommand=root.register(baum_zaehlen))
        listen = messen(app.tree, lambda: app.tree.yview()[0], lz)
        app.tree.configure(yscrollcommand=baum_befehl)
        ergebnisse[groesse] = {"seite": seite, "liste": listen}
        for name, wert in (("Seite", seite), ("Liste", listen)):
            print(f"{groesse:5} {name:5} median={wert['ms_median']:8.3f} ms p95={wert['ms_p95']:8.3f} ms "
                  f"max={wert['ms_max']:8.3f} ms rückrufe/schritt={wert['rueckrufe_je_schritt']:5} "
                  f"rückruf_median={wert['rueckruf_ms_median']:7.3f} ms bewegt={wert['bewegt']}", flush=True)
    umgebung = gl.umgebung(root)
    root.destroy()
    protokoll = gl.fehlerprotokoll(ordner)
    gl.aufraeumen()
    if args.json:
        with open(args.json, "w", encoding="utf-8") as datei:
            json.dump({"version": mod.APP_VERSION, "umgebung": umgebung, "schritte": args.schritte,
                       "ergebnisse": ergebnisse, "callbackfehler": fehler}, datei, ensure_ascii=False, indent=2)
    if fehler or protokoll.strip():
        print("Fehler:", fehler, protokoll[-2000:], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
