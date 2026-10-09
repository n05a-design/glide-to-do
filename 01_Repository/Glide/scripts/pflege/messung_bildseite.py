#!/usr/bin/env python3
"""Bildlayout einer Seite beim Tippen und Scrollen messen (P04).

Aufruf (aus `01_Repository/Glide`):
    python3 -B scripts/pflege/messung_bildseite.py [--code ORDNER] [--bilder 30] [--runden 21] [--json DATEI]

Eine künstliche Seite mit Absätzen und Bildern (links, rechts, mittig) wird
geöffnet. Gemessen werden je Runde: ein Zeichen fern von jedem Bild tippen,
ein Zeichen im Umflussbereich eines Bildes tippen und einmal scrollen – jeweils
bis das verzögerte Layout gelaufen ist. Gezählt werden vollständige
Layoutläufe (Ränder neu), Bildzeichnungen und Umflussberechnungen; die Zeit
ist die Dauer von `layout_images` (unprofiliert, Median und p95 nach einem
Aufwärmlauf). Künstliche Daten in einem temporären `GLIDE_DATA_DIR`.
"""

import argparse
import json
import os
import statistics
import sys
import time

import _glide_laden as gl


def p95(werte):
    werte = sorted(werte)
    return werte[max(0, round(0.95 * (len(werte) - 1)))] if werte else None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--code")
    parser.add_argument("--bilder", type=int, default=30)
    parser.add_argument("--runden", type=int, default=21)
    parser.add_argument("--json")
    args = parser.parse_args()
    ordner = gl.isolieren("glide-bildseite-")
    mod = gl.glide_laden(args.code)
    root = mod.tk.Tk()
    root.geometry("1280x900+20+20")
    fehler = []
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))

    def ruhe(sekunden=0.2):
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            root.update()
            time.sleep(0.01)

    pfade = []
    for nummer, (breite, hoehe) in enumerate(((160, 120), (300, 180), (900, 300))):
        bild = mod.tk.PhotoImage(master=root, width=breite, height=hoehe)
        bild.put(("#3366CC", "#CC6633", "#33AA66")[nummer], to=(0, 0, breite, hoehe))
        pfad = os.path.join(ordner, f"bild{nummer}.png")
        bild.write(pfad, format="png")
        pfade.append(pfad)
    absatz = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 6
    text = "# Bildseite\n\n" + "\n\n".join(f"Absatz {i}. {absatz}" for i in range(args.bilder * 2))
    app.new_page_from_markdown(text)
    ruhe()
    editor = app.rich_note_editor
    for i in range(args.bilder):
        editor.insert_images([pfade[i % 3]], f"{4 + i * 4}.0")
    ruhe(0.6)

    zaehler = {"layout": 0, "voll": 0, "zeichnen": 0, "umfluss": 0}
    dauer = []
    original_layout, original_render, original_flow = editor.layout_images, editor.render_image, editor.flow_around

    def layout(*a, **k):
        zaehler["layout"] += 1
        umfluss_vorher = zaehler["umfluss"]
        start = time.perf_counter()
        ergebnis = original_layout(*a, **k)
        dauer.append((time.perf_counter() - start) * 1000)
        if zaehler["umfluss"] > umfluss_vorher:
            zaehler["voll"] += 1
        return ergebnis

    def render(*a, **k):
        # Gezählt wird, was tatsächlich neu gezeichnet wurde: Neue Zeichenelemente
        # tragen neue Kennungen (für alte und neue Fassung gleich messbar).
        view = editor.image_view(a[0])
        vorher = view.find_all()
        ergebnis = original_render(*a, **k)
        if view.find_all() != vorher:
            zaehler["zeichnen"] += 1
        return ergebnis

    def flow(*a, **k):
        zaehler["umfluss"] += 1
        return original_flow(*a, **k)

    editor.layout_images, editor.render_image, editor.flow_around = layout, render, flow
    schluessel = editor.image_keys()
    # Ein links umflossenes Bild in der Mitte der Seite: Die Zeile nach dem
    # Anker steht im Umflussbereich.
    links = [key for key in schluessel if editor.images[key]["mode"] == "left"]
    nah = editor.text.index(f"{editor.text.tag_ranges(links[len(links) // 2])[0]} +1l lineend")
    fern = editor.text.index("2.0")
    ergebnisse = {}
    for name, schritt in (
            ("Tippen fern", lambda: editor.text.insert(fern, "x")),
            ("Tippen neben Bild", lambda: editor.text.insert(nah, "x")),
            ("Scrollen", lambda: editor.text.yview_scroll(3, "units"))):
        for schluessel_z in zaehler:
            zaehler[schluessel_z] = 0
        dauer.clear()
        for runde in range(args.runden + 1):
            schritt()
            ruhe(0.25)
            if runde == 0:
                for schluessel_z in zaehler:
                    zaehler[schluessel_z] = 0
                dauer.clear()
        ergebnisse[name] = {**zaehler, "runden": args.runden,
                            "layout_ms_median": round(statistics.median(dauer), 3) if dauer else None,
                            "layout_ms_p95": round(p95(dauer), 3) if dauer else None,
                            "layout_ms_roh": [round(w, 3) for w in dauer]}
        print(f"{name:18} layout={zaehler['layout']:3} voll={zaehler['voll']:3} zeichnen={zaehler['zeichnen']:4} "
              f"umfluss={zaehler['umfluss']:4} median={ergebnisse[name]['layout_ms_median']} ms "
              f"p95={ergebnisse[name]['layout_ms_p95']} ms", flush=True)
    umgebung = gl.umgebung(root)
    root.destroy()
    protokoll = gl.fehlerprotokoll(ordner)
    gl.aufraeumen()
    if args.json:
        with open(args.json, "w", encoding="utf-8") as datei:
            json.dump({"version": mod.APP_VERSION, "umgebung": umgebung, "bilder": args.bilder,
                       "ergebnisse": ergebnisse, "callbackfehler": fehler}, datei, ensure_ascii=False, indent=2)
    if fehler or protokoll.strip():
        print("Fehler:", fehler, protokoll[-2000:], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    raise SystemExit(main())
