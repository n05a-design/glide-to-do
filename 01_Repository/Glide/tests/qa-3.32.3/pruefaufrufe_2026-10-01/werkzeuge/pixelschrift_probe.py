"""W3: Wie oft fragt das Pixel-Design Tk nach „Pixelify Sans“?

Aufruf (aus diesem Ordner):
    xvfb-run -a -s "-screen 0 1280x860x24" python3 -B pixelschrift_probe.py --json ../ergebnisse/pixelschrift_<python>.json

Zählt je Ansichtswechsel die neu angelegten Tk-Schriften mit der Familie der
Pixelschrift. Mit gefundener Schrift (Tk mit Xft, macOS) bleibt es bei der
ersten Abfrage; ohne Schrift fragt jeder Aufbau erneut. Künstliche Daten in
einem temporären `GLIDE_DATA_DIR`.
"""

import argparse
import json
import os
import platform
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                "analyse_planung_2026-10-01", "werkzeuge"))
import _glide_laden as gl  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--code", default=None)
    parser.add_argument("--json", required=True)
    args = parser.parse_args()
    daten = gl.isolieren("glide-pixelschrift-")
    modul = gl.glide_laden(args.code)
    import tkinter as tk
    import tkinter.font as tkfont
    root = tk.Tk()
    root.geometry("1280x840+0+0")
    app = modul.ListApp(root)
    root.update()
    schluessel = next(k for k, v in app.DESIGNS.items() if v.get("layer") == "pixel")
    app.set_design(schluessel)
    root.update()
    zaehler = {"abfragen": 0}
    original = tkfont.Font.__init__

    def zaehlend(self, *a, **k):
        if k.get("family") == app.PIXEL_FONT_FAMILY:
            zaehler["abfragen"] += 1
        original(self, *a, **k)
    tkfont.Font.__init__ = zaehlend
    ergebnis = {"werkzeug": "pixelschrift_probe.py", "python": platform.python_version(),
                "tk": root.tk.call("info", "patchlevel"), "design": schluessel, "schritte": {}}
    for name, aktion in (("startseite", app.set_home_view),
                         ("liste", lambda: app.set_active_list(app.lists[0]["id"])),
                         ("startseite_2", app.set_home_view)):
        zaehler["abfragen"] = 0
        start = time.perf_counter()
        aktion()
        root.update()
        ergebnis["schritte"][name] = {"ms": round((time.perf_counter() - start) * 1000),
                                      "tk_abfragen_pixelschrift": zaehler["abfragen"],
                                      "schrift_gefunden": bool(app._pixel_font_found)}
    ergebnis["fehlerprotokoll"] = gl.fehlerprotokoll(daten)
    root.destroy()
    with open(args.json, "w", encoding="utf-8") as datei:
        json.dump(ergebnis, datei, ensure_ascii=False, indent=1)
    print(json.dumps(ergebnis["schritte"], ensure_ascii=False))


if __name__ == "__main__":
    main()
