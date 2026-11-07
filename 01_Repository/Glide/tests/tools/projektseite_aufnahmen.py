#!/usr/bin/env python3
"""Aufnahmen für die GitHub-Projektseite aus dem künstlichen Showcase (06.11.2026).

Lädt das Showcase-App-Backup in einen frischen temporären Datenordner, schaltet
die ergänzenden Bedienhinweise wie in der Vorgabe aus, öffnet die genannten
Ansichten bei 1440 × 900 und nimmt jeweils den Fensterinhalt als PNG auf.
Echte Nutzerdaten werden nie berührt: `GLIDE_DATA_DIR` zeigt vor dem Import
auf den temporären Ordner, der danach gelöscht wird.

Aufnahme nur unter Windows (PowerShell/System.Drawing); für Linux-Sichtprüfungen
gibt es `screenshots.py`. Aufruf aus `01_Repository/Glide`:

    py -3.14 -B tests/tools/projektseite_aufnahmen.py --out <Ordner> \\
        glide-3.50.5-startseite=:home glide-3.50.5-heute=:today \\
        glide-3.50.5-spaltenboard=:board:Vermarktung glide-3.50.5-pinnwand=:global \\
        glide-3.50.5-pixel-werkstatt=:list:Quartier glide-3.50.5-seite=:list:Parkquartier \\
        glide-3.50.5-heute-dunkel=dark:today glide-3.50.5-pinnwand-dunkel=dark:global

Jede Szene lautet `name=design:art[:titelanfang]`; ein leeres Design behält das
gespeicherte. Arten: home, today, calendar, global, list, board, table.
"""
from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[2]
SHOWCASE = REPO / "tests/fixtures/showcase/Glide-Showcase_App.glideapp"
ARTEN = ("home", "today", "calendar", "global", "list", "board", "table")


def szene(text):
    """`name=design:art[:titel]` in ein Tupel zerlegen; Fehler früh melden."""
    name, gleich, rest = text.partition("=")
    design, _, rest = rest.partition(":")
    art, _, titel = rest.partition(":")
    if not gleich or not name or art not in ARTEN or (art in ("list", "board", "table") and not titel):
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


def aufnehmen(root, ziel):
    for _ in range(4):
        root.update_idletasks()
        root.update()
    x, y, w, h = root.winfo_rootx(), root.winfo_rooty(), root.winfo_width(), root.winfo_height()
    befehl = ("Add-Type -AssemblyName System.Drawing;"
              f"$b=New-Object System.Drawing.Bitmap {w},{h};"
              "$g=[System.Drawing.Graphics]::FromImage($b);"
              f"$g.CopyFromScreen({x},{y},0,0,$b.Size);"
              f"$b.Save('{ziel}',[System.Drawing.Imaging.ImageFormat]::Png);")
    subprocess.run(["powershell", "-NoProfile", "-Command", befehl], check=True)
    print("aufgenommen", ziel, f"{w}x{h}", flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--showcase", type=Path, default=SHOWCASE)
    parser.add_argument("szenen", nargs="+", type=szene)
    args = parser.parse_args(argv)
    if sys.platform != "win32":
        raise SystemExit("Aufnahme nur unter Windows; für Linux tests/tools/screenshots.py verwenden.")
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
        root.geometry("1440x900+40+30")

        def finde(titel):
            treffer = [e["id"] for e in app.lists if (e.get("title") or "").startswith(titel)]
            if len(treffer) != 1:
                raise SystemExit(f"Liste {titel!r} nicht eindeutig gefunden")
            return treffer[0]

        def schritt(index=0):
            if index >= len(args.szenen):
                root.after(300, root.destroy)
                return
            name, design, art, titel = args.szenen[index]
            if design:
                app.set_design(design)
            if art == "home":
                app.set_home_view()
            elif art == "today":
                app.set_today_view()
            elif art == "calendar":
                app.open_calendar_view()
            elif art == "global":
                app.open_global_board()
            else:
                app.set_active_list(finde(titel))
                if art == "board":
                    app.open_board_view()
                elif art == "table":
                    app.set_table_view()
            root.after(1800, lambda: (aufnehmen(root, args.out / f"{name}.png"), schritt(index + 1)))

        root.after(2500, schritt)
        root.lift()
        root.attributes("-topmost", True)
        root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
