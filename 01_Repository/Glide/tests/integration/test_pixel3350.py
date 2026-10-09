"""Paket Pixel (3.35.0): G19 Palettenfarbe ändern mit Vorschau, G-03 Symbolvorschau vor dem ICO-Export.

G19: Doppelklick auf eine Farbe der Farbleiste öffnet „ersetzen durch …“; die
Zeichnung zeigt das Ergebnis schon während der Rückfrage. Ablehnen lässt Zellen,
Palette und Rückgängig-Verlauf unverändert, Übernehmen ist ein Rückgängig-Schritt.
G-03: Mehr › „Als Symbol exportieren (ICO)“ zeigt vor dem Speichern 16, 32 und
48 px auf hellem und dunklem Grund; jedes Vorschaubild ist pixelgleich zum Bild
derselben Größe in der geschriebenen ICO-Datei. Abbrechen schreibt nichts.

--app wählt den Quellstand; mit der unveränderten 3.34.0 muss die Suite rot sein
(Gegenprobe). Künstliche Daten in einem temporären GLIDE_DATA_DIR.
"""
import argparse
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import struct
import sys
import tempfile
import time
import zlib

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def eintraege(menu):
    ende = menu.index("end")
    return {menu.entrycget(i, "label"): i for i in range((ende if ende is not None else -1) + 1)
            if menu.type(i) in ("command", "cascade")}


def ico_bilder(daten):
    """{Größe: RGBA-Zeilen} einer ICO-Datei mit PNG-Bildern."""
    _r, _t, anzahl = struct.unpack("<HHH", daten[:6])
    bilder = {}
    for nummer in range(anzahl):
        _b, _h, _f, _x, _p, _bit, laenge, start = struct.unpack("<BBBBHHII", daten[6 + 16 * nummer:22 + 16 * nummer])
        png = daten[start:start + laenge]
        groesse = struct.unpack(">I", png[16:20])[0]
        idat, pos = b"", 8
        while pos < len(png):
            n = struct.unpack(">I", png[pos:pos + 4])[0]
            if png[pos + 4:pos + 8] == b"IDAT":
                idat += png[pos + 8:pos + 8 + n]
            pos += 12 + n
        roh = zlib.decompress(idat)
        zeile = groesse * 4 + 1
        bilder[groesse] = [[tuple(roh[y * zeile + 1 + 4 * x:y * zeile + 5 + 4 * x]) for x in range(groesse)]
                           for y in range(groesse)]
    return bilder


with tempfile.TemporaryDirectory(prefix="glide-pixel-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_pixel_test", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    fehler = []
    root = mod.tk.Tk()
    root.geometry("1280x840+20+20")
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
    app.show_info = lambda *a, **k: None
    pruefungen = []

    def ruhe(sekunden=0.15):
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            root.update()
            time.sleep(0.01)

    try:
        eintrag = app.create_new_drawing(size=16)
        app.set_active_list(eintrag if isinstance(eintrag, str) else eintrag["id"])
        ruhe(0.3)
        editor = app.drawing_editor
        modell = editor.model
        modell.paint_cells([(x, y) for x in range(4, 12) for y in range(4, 12)], "#C43BFF")
        modell.paint_cells([(0, 0), (15, 15)], "#0072B2")
        modell.clear_history()
        editor.render_full()
        editor.flush()
        ruhe(0.2)

        # --- G19: Doppelklick auf die Farbe, Vorschau, ablehnen und übernehmen ----
        editor.draw_strip()
        ruhe()
        treffer = next((links, rechts) for links, rechts, farbe in editor._strip_hits if farbe == "#C43BFF")
        x = (treffer[0] + treffer[1]) // 2 - int(editor.strip.canvasx(0))
        y = editor.strip.winfo_height() // 2
        zellen, palette, schritte = bytes(modell.cells), list(modell.palette), modell.undo_count
        gesehen = []
        app.drawing_color_dialog = lambda *a, **k: "#22813A"

        def rueckfrage(antwort):
            def frage(titel, text, **_k):
                # Während der Rückfrage zeigt die Zeichnung bereits das Ergebnis.
                gesehen.append((titel, text, editor.model.color_at(5, 5),
                                "#{:02X}{:02X}{:02X}".format(*editor._base.get(5, 5))))
                return antwort
            return frage

        uhr = [100000]

        def doppelklick():
            # Zwei echte Klicks an derselben Stelle mit Zeitstempeln: Ohne sie zählt Tk alle
            # erzeugten Klicks als eine Folge (Dreifach-, Vierfachklick …).
            uhr[0] += 5000
            for versatz in (0, 120):
                editor.strip.event_generate("<ButtonPress-1>", x=x, y=y, time=uhr[0] + versatz)
                editor.strip.event_generate("<ButtonRelease-1>", x=x, y=y, time=uhr[0] + versatz + 40)

        app.ask_yes_no = rueckfrage(False)
        doppelklick()
        ruhe(0.2)
        titel, text, farbe, pixel = gesehen[-1]
        assert titel == "Farbe ersetzen" and "64 Zelle(n)" in text and "#C43BFF" in text, text
        assert farbe == pixel == "#22813A", (farbe, pixel)
        assert (bytes(modell.cells), modell.palette, modell.undo_count) == (zellen, palette, schritte)
        assert "#{:02X}{:02X}{:02X}".format(*editor._base.get(5, 5)) == "#C43BFF"
        app.ask_yes_no = rueckfrage(True)
        doppelklick()
        ruhe(0.2)
        assert modell.color_at(5, 5) == "#22813A" and modell.color_at(0, 0) == "#0072B2"
        assert modell.undo_count == schritte + 1, (modell.undo_count, schritte)
        # Ein weiterer Klick gleich danach (Dreifachklick) öffnet keinen zweiten Dialog.
        anzahl = len(gesehen)
        editor.strip.event_generate("<ButtonPress-1>", x=x, y=y, time=uhr[0] + 240)
        editor.strip.event_generate("<ButtonRelease-1>", x=x, y=y, time=uhr[0] + 280)
        ruhe()
        assert len(gesehen) == anzahl and modell.undo_count == schritte + 1
        modell.undo()
        editor.render_full()
        assert bytes(modell.cells) == zellen
        modell.redo()
        editor.render_full()
        editor.flush()
        pruefungen.append("G19: Doppelklick auf die Farbleiste, Ergebnis während der Rückfrage sichtbar; "
                          "Ablehnen ohne Spur in Zellen, Palette und Verlauf; Übernehmen ein Rückgängig-Schritt; Dreifachklick "
                          "öffnet keinen zweiten Dialog")

        # --- G-03: Symbolvorschau über das echte Mehr-Menü ------------------------
        menues = []
        original_popup = mod.tk.Menu.tk_popup
        mod.tk.Menu.tk_popup = lambda self, *a: menues.append(self)
        try:
            editor.show_more_menu()
        finally:
            mod.tk.Menu.tk_popup = original_popup
        mehr = menues[-1]
        symbol = mehr.nametowidget(mehr.entrycget(eintraege(mehr)["Als Symbol exportieren (ICO)"], "menu"))
        ziel = os.path.join(ordner, "symbol.ico")
        gespeichert = []
        mod.filedialog.asksaveasfilename = lambda **k: gespeichert.append(k) or ziel
        vorschauen = {}

        def vorschau(knopf):
            def run_modal(dialog, *a, **k):
                for _ in range(5):
                    dialog.update()
                vorschauen.clear()
                vorschauen.update(dialog._glide_icon_previews)
                next(w for w in descendants(dialog)
                     if isinstance(w, mod.RoundedButton) and w.text == knopf).command()
            return run_modal

        app.run_modal = vorschau("Abbrechen")
        symbol.invoke(eintraege(symbol)["Grund durchsichtig …"])
        ruhe()
        assert vorschauen and not gespeichert and not os.path.exists(ziel)
        app.run_modal = vorschau("Exportieren")
        symbol.invoke(eintraege(symbol)["Grund durchsichtig …"])
        ruhe()
        daten = Path(ziel).read_bytes()
        assert daten == modell.to_ico(transparent_background=True)
        bilder = ico_bilder(daten)
        geprueft = 0
        for grund in ("#FFFFFF", "#1C1C1E"):
            for groesse in (16, 32, 48):
                bild = vorschauen[(grund, groesse)]
                doppelt = vorschauen[(grund, groesse, 2)]
                assert (bild.width(), bild.height(), doppelt.width()) == (groesse, groesse, 2 * groesse)
                for yy in range(groesse):
                    for xx in range(groesse):
                        r, g, b, a = bilder[groesse][yy][xx]
                        erwartet = grund if a == 0 else f"#{r:02X}{g:02X}{b:02X}"
                        ist = "#{:02X}{:02X}{:02X}".format(*bild.get(xx, yy))
                        assert ist == erwartet, (grund, groesse, xx, yy, ist, erwartet)
                        assert doppelt.get(2 * xx + 1, 2 * yy + 1) == bild.get(xx, yy)
                        geprueft += 1
        menues[-1].destroy()
        pruefungen.append(f"G-03: Vorschau vor dem Speichern, {geprueft} Pixel auf hellem und dunklem Grund gleich "
                          "der geschriebenen ICO-Datei (16/32/48), doppelte Ansicht ohne Glättung; Abbrechen "
                          "schreibt nichts")

        ruhe(0.2)
        assert not fehler, fehler
        print("test_pixel3350: OK; " + "; ".join(pruefungen))
    finally:
        try:
            app.cancel_pending_callbacks()
            app.release_data_lock()
        except Exception:
            pass
        try:
            root.destroy()
        except mod.tk.TclError:
            pass
