"""Misst Ansichtswechsel in Glide: Zeit je Wechsel und die teuersten Funktionen.

Aufruf (im Repository): GLIDE_QA_HINTERGRUND=1 PYTHONPATH=tests/tools/hintergrund \
    python3 -B scripts/pflege/messung_ansichtswechsel.py [pfad/zu/app.pyw]

Arbeitet auf einer Kopie der Beispieldaten in einem temporären GLIDE_DATA_DIR.
"""
import cProfile
import importlib.machinery
import importlib.util
import io
import os
import pstats
import statistics
import sys
import tempfile
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
APP = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "src/glide/app.pyw"
sys.dont_write_bytecode = True
sys.path.insert(0, str(APP.parent))
with tempfile.TemporaryDirectory(prefix="glide-profil-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_profil", str(APP))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1300x860+30+30")
    app = mod.ListApp(root)

    def ruhe(runden=4):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    ruhe(8)
    listen = [e for e in app.lists if not app.is_page_list(e) and e.get("list_kind") not in ("note", "drawing")]
    groesste = max(listen, key=lambda e: app.count_items(e.get("items", [])))
    seite = next((e for e in app.lists if app.is_page_list(e)), None)
    notiz = next((e for e in app.lists if e.get("list_kind") == "note"), None)

    def liste():
        app.set_active_list(groesste["id"])

    def tabelle():
        app.set_active_list(groesste["id"]); app.set_table_view()

    def pinnwand():
        app.set_active_list(groesste["id"]); app.workspace.set_mode("board")

    wechsel = [("Startseite", app.set_home_view), ("Listen und Ordner", app.set_library_view),
               ("Liste", liste), ("Tabelle", tabelle), ("Pinnwand", pinnwand),
               ("Heute", app.set_today_view), ("Vorlagen", app.set_template_view)]
    if seite:
        wechsel.append(("Seite", lambda: app.set_active_list(seite["id"])))
    if notiz:
        wechsel.append(("Notiz", lambda: app.set_active_list(notiz["id"])))
    zeiten = {name: [] for name, _ in wechsel}
    profil = cProfile.Profile()
    for runde in range(4):
        for name, schritt in wechsel:
            if getattr(app, "workspace", None) is not None and app.workspace.mode == "board" and name != "Pinnwand":
                app.workspace.set_mode("list")
                ruhe(2)
            start = time.perf_counter()
            if runde:
                profil.enable()
            schritt()
            ruhe(3)
            if runde:
                profil.disable()
            zeiten[name].append((time.perf_counter() - start) * 1000)
    root.destroy()

for name, werte in zeiten.items():
    print(f"{name:18s} {statistics.median(werte[1:]):7.1f} ms (erster Wechsel {werte[0]:.0f} ms)")
puffer = io.StringIO()
pstats.Stats(profil, stream=puffer).sort_stats("tottime").print_stats(22)
print("\n".join(line for line in puffer.getvalue().splitlines()[6:40]))
