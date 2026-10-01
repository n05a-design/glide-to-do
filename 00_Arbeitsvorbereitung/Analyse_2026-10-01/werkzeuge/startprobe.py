"""Startprobe: Glide in isolierter Ablage starten, Aufbau messen, Fehler prüfen.

Aufruf (Linux ohne Anzeige):
    xvfb-run -a -s "-screen 0 1280x860x24" python3 startprobe.py [--bild start.png]

Ergebnis als JSON auf stdout. Prüft nur Start und Grundaufbau – keine Bedienung.
"""

import argparse
import json
import os
import time

import _glide_laden as gl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", default=None, help="Ordner mit der Glide-Hauptdatei")
    parser.add_argument("--bild", default=None, help="Bildschirmfoto der Xvfb-Anzeige (ImageMagick import)")
    args = parser.parse_args()
    daten = gl.isolieren("glide-startprobe-")
    t0 = time.perf_counter()
    modul = gl.glide_laden(args.code)
    t1 = time.perf_counter()
    import tkinter as tk
    root = tk.Tk()
    root.geometry("1280x840+0+0")
    modul.ListApp(root)
    root.update()
    t2 = time.perf_counter()

    def zaehlen(widget):
        return 1 + sum(zaehlen(kind) for kind in widget.winfo_children())

    ergebnis = {
        "glide_version": modul.APP_VERSION,
        "datenformat": modul.ListApp.DATA_SCHEMA_VERSION,
        "import_s": round(t1 - t0, 3),
        "aufbau_s": round(t2 - t1, 3),
        "widgets": zaehlen(root),
        "umgebung": gl.umgebung(root),
        "dateien_im_datenordner": sorted(os.listdir(daten)),
    }

    def abschluss():
        ergebnis["fehlerprotokoll"] = gl.fehlerprotokoll(daten)
        if args.bild:
            os.system(f"import -window root '{args.bild}'")
        print(json.dumps(ergebnis, indent=1, ensure_ascii=False))
        root.destroy()

    root.after(1500, abschluss)
    root.mainloop()


if __name__ == "__main__":
    main()
