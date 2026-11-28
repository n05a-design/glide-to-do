# SPDX-License-Identifier: MPL-2.0
"""Reproduzierbare Leistungs-Baseline für das Glide Ecosystem (E03–E05).

Misst mit festen, künstlichen Daten in einem temporären `GLIDE_DATA_DIR`:

- Kaltstart: frischer Prozess bis zur leeren Ereignisschleife (`--kalt` Läufe).
- Warmstart: zweites `ListApp` im selben Prozess.
- Ansichtswechsel (Startseite, Heute, Bibliothek, Liste, Tabelle, Seiten) mit großer Liste.
- Themenwechsel (hell ↔ dunkel) über `toggle_theme`.
- Fenstergrößenwechsel: Dauer und Zahl der `<Configure>`-Ereignisse je Wechsel
  (Kaskaden werden als Ereigniszahl sichtbar).
- Komponenten-Galerie öffnen und schließen.
- Bento-Raster mit 60 Karten in einem neutralen Fenster (nur `glide_bento`), Reflow bei drei Breiten.
- Widgetzahl, offene Zeitgeber (`after info`) und Speicher (Arbeitsspeicher des Prozesses,
  `tracemalloc`-Spitze) nach den Läufen.

Je Messgröße: Median, p95, Minimum, Maximum, Stichproben; der erste Durchlauf
(kalt im Prozess) wird getrennt ausgewiesen. Ergebnis als JSON mit Umgebung
(Betriebssystem, Prozessor, Python, Tk, Datenumfang). Kein Latenzversprechen:
Werte gelten nur für den gemessenen Rechner.

    python3 -B scripts/pflege/messung_ecosystem.py --json <Datei> [--items 1000] [--runden 5] [--kalt 3]
"""
from __future__ import annotations

import argparse
import ctypes
import importlib.machinery
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
import time
import tracemalloc

REPO = Path(__file__).resolve().parents[2]


def verteilung(werte):
    s = sorted(werte)
    return {"median_ms": round(statistics.median(s), 2), "p95_ms": round(s[math.ceil(len(s) * .95) - 1], 2),
            "min_ms": round(s[0], 2), "max_ms": round(s[-1], 2), "n": len(s),
            "stichproben_ms": [round(w, 2) for w in werte]}


def arbeitsspeicher_mb():
    """Arbeitsspeicher des Prozesses in MB (Windows: Working Set, sonst Spitzen-RSS)."""
    if sys.platform == "win32":
        class PMC(ctypes.Structure):
            _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong), ("PeakWorkingSetSize", ctypes.c_size_t),
                        ("WorkingSetSize", ctypes.c_size_t), ("a", ctypes.c_size_t), ("b", ctypes.c_size_t),
                        ("c", ctypes.c_size_t), ("d", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t),
                        ("PeakPagefileUsage", ctypes.c_size_t)]
        pmc = PMC()
        pmc.cb = ctypes.sizeof(PMC)
        kernel = ctypes.windll.kernel32
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        psapi = ctypes.WinDLL("psapi")
        psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(PMC), ctypes.c_ulong]
        if psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb):
            return round(pmc.WorkingSetSize / 2 ** 20, 1)
        return None
    import resource
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return round(rss / (2 ** 20 if sys.platform == "darwin" else 2 ** 10), 1)


def umgebung(mod=None, root=None, items=0):
    info = {"os": platform.platform(), "machine": platform.machine(), "processor": platform.processor() or None,
            "cpus": os.cpu_count(), "python": platform.python_version(), "items": items}
    if root is not None:
        info["tk"] = root.tk.call("info", "patchlevel")
        info["windowing"] = root.tk.call("tk", "windowingsystem")
        info["scaling"] = round(float(root.tk.call("tk", "scaling")), 3)
    return info


def laden(app_pfad, ordner, name):
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    sys.path.insert(0, str(Path(app_pfad).resolve().parent))
    loader = importlib.machinery.SourceFileLoader(name, str(app_pfad))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[name] = mod
    loader.exec_module(mod)
    return mod


def kaltstart(app_pfad, runden):
    """Frischer Prozess je Lauf: Import, Fenster, ListApp, bis zur leeren Ereignisschleife."""
    code = ("import os,sys,time,tempfile,importlib.machinery,importlib.util\n"
            "t0=time.perf_counter()\n"
            "d=tempfile.mkdtemp(prefix='glide-kalt-'); os.environ['GLIDE_DATA_DIR']=d; os.environ['GLIDE_TEST_MODE']='1'\n"
            f"p={str(app_pfad)!r}; sys.path.insert(0, os.path.dirname(p))\n"
            "l=importlib.machinery.SourceFileLoader('glide_kalt',p); m=importlib.util.module_from_spec(importlib.util.spec_from_loader(l.name,l)); l.exec_module(m)\n"
            "t1=time.perf_counter(); r=m.tk.Tk(); r.geometry('1280x800+20+20'); a=m.ListApp(r)\n"
            "[r.update() for _ in range(5)]\n"
            "t2=time.perf_counter(); print(f'{(t1-t0)*1000:.2f} {(t2-t0)*1000:.2f}'); a.on_close() if hasattr(a,'on_close') else r.destroy()\n")
    imp, gesamt = [], []
    for _ in range(runden):
        e = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, timeout=300)
        zeile = (e.stdout.strip().splitlines() or ["0 0"])[-1].split()
        imp.append(float(zeile[0]))
        gesamt.append(float(zeile[1]))
    return {"import": verteilung(imp), "bis_bereit": verteilung(gesamt)}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--items", type=int, default=1000)
    parser.add_argument("--runden", type=int, default=5)
    parser.add_argument("--kalt", type=int, default=3)
    parser.add_argument("--marke", default="", help="frei wählbare Kennzeichnung des Stands, z. B. E03-Baseline")
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    tracemalloc.start()
    ergebnis = {"marke": args.marke, "werkzeug": "messung_ecosystem.py", "version": 1}
    ergebnis["kaltstart"] = kaltstart(args.app.resolve(), args.kalt)
    with tempfile.TemporaryDirectory(prefix="glide-eco-", ignore_cleanup_errors=True) as ordner:
        mod = laden(args.app.resolve(), ordner, "glide_eco")
        root = mod.tk.Tk()
        root.geometry("1280x800+20+20")
        fehler = []
        root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))

        def idle(n=3):
            for _ in range(n):
                root.update_idletasks()
                root.update()

        t = time.perf_counter()
        app = mod.ListApp(root)
        idle()
        ergebnis["warmstart_ms"] = round((time.perf_counter() - t) * 1000, 2)
        app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
        app.show_info = lambda *a, **k: None
        # Feste künstliche Daten: zwölf Listen, eine große Liste, Seiten.
        inbox = app.ensure_inbox_list()
        inbox["items"] = []
        app.lists = [inbox]
        app.folders = []
        gross = app.new_list_object("Große Liste", [app.new_item(f"Aufgabe {i:05d}", item_id=f"eco-{i}",
                                    description="Prüftext " * 4) for i in range(args.items)], list_id="eco-gross",
                                    created_at="2026-11-28T08:00:00")
        app.lists.append(gross)
        for n in range(11):
            app.lists.append(app.new_list_object(f"Liste {n:02d}", [app.new_item(f"Punkt {n}-{i}") for i in range(20)],
                                                 list_id=f"eco-l{n}", created_at="2026-11-28T08:00:00"))
        seite = app.new_page_from_markdown("# Messseite\n\n" + "\n\n".join(f"Absatz {i}: " + "Text " * 25 for i in range(40)),
                                           title="Messseite")
        app.save_items()
        app.update_sidebar_list()
        idle()
        ergebnis["umgebung"] = umgebung(mod, root, args.items)

        def liste():
            app.set_active_list("eco-gross")

        def tabelle():
            liste()
            app.set_table_view()
        ansichten = [("startseite", app.set_home_view), ("heute", app.set_today_view), ("bibliothek", app.set_library_view),
                     ("grosse_liste", liste), ("tabelle", tabelle), ("seiten", app.set_pages_view),
                     ("seite", lambda: app.set_active_list(seite["id"]))]
        zeiten = {name: [] for name, _ in ansichten}
        for _ in range(args.runden + 1):
            for name, aktion in ansichten:
                t = time.perf_counter()
                aktion()
                idle()
                zeiten[name].append((time.perf_counter() - t) * 1000)
        ergebnis["ansichtswechsel"] = {n: {"erster_ms": round(w[0], 2), **verteilung(w[1:])} for n, w in zeiten.items()}

        thema = []
        for _ in range(args.runden):
            t = time.perf_counter()
            app.toggle_theme()
            idle()
            thema.append((time.perf_counter() - t) * 1000)
        if len(thema) % 2:
            app.toggle_theme()
            idle()
        ergebnis["themenwechsel"] = verteilung(thema)

        zaehler = {"n": 0}
        bindung = root.bind_all("<Configure>", lambda _e: zaehler.__setitem__("n", zaehler["n"] + 1), add="+")
        app.set_home_view()
        idle()
        groesse, ereignisse = [], []
        for runde in range(args.runden):
            for geo in ("900x700", "1600x950", "1280x800"):
                zaehler["n"] = 0
                t = time.perf_counter()
                root.geometry(geo)
                idle(5)
                groesse.append((time.perf_counter() - t) * 1000)
                ereignisse.append(zaehler["n"])
        root.unbind_all("<Configure>")
        ergebnis["groessenwechsel"] = {**verteilung(groesse), "configure_ereignisse_median": statistics.median(ereignisse),
                                       "configure_ereignisse_max": max(ereignisse)}

        erster, vollstaendig, eintraege, galerie_fehler = [], [], [], []
        if hasattr(app, "show_component_gallery"):
            # Die Galerie ist modal. Während der Messung ersetzt das Werkzeug das modale Warten:
            # erster sichtbarer Inhalt = Rückkehr aus dem Aufbau bis zum ersten gezeichneten Bild;
            # vollständig = alle Vorführungen gebaut (`finish_component_gallery`, sofern vorhanden).
            # Danach schließt das Werkzeug den Dialog selbst; nie wartet ein Lauf auf einen Menschen.
            originales_warten = app.run_modal

            def messwarten(dialog, *_a, **_k):
                dialog.update_idletasks()  # zeichnet den ersten Stapel; Zeitgeber der Folgestapel laufen noch nicht
                stand["erster"] = time.perf_counter()
                if hasattr(app, "finish_component_gallery"):
                    app.finish_component_gallery()
                dialog.update_idletasks()
                dialog.update()
                stand["fertig"] = time.perf_counter()
                stand["eintraege"] = len((getattr(app, "_component_gallery", None) or {}).get("widgets", {}))
                dialog.destroy()
            app.run_modal = messwarten
            try:
                for _ in range(max(2, args.runden // 2)):
                    stand = {}
                    t = time.perf_counter()
                    try:
                        app.show_component_gallery()
                    except Exception as error:  # noqa: BLE001 – Befund festhalten, Messung fortsetzen
                        galerie_fehler.append(repr(error))
                        for w in list(root.winfo_children()):
                            if isinstance(w, mod.tk.Toplevel):
                                w.destroy()
                        idle()
                        continue
                    idle()
                    erster.append((stand.get("erster", time.perf_counter()) - t) * 1000)
                    vollstaendig.append((stand.get("fertig", time.perf_counter()) - t) * 1000)
                    eintraege.append(stand.get("eintraege", 0))
            finally:
                app.run_modal = originales_warten
            if erster:
                ergebnis["galerie_erster_inhalt"] = verteilung(erster)
                ergebnis["galerie_vollstaendig"] = {**verteilung(vollstaendig), "eintraege": max(eintraege)}
            ergebnis["galerie_fehler"] = galerie_fehler

        import glide_bento as b
        fenster = mod.tk.Toplevel(root)
        fenster.geometry("1200x900")
        ctx = b.BentoContext.for_host(theme_provider=lambda: app.theme)
        bento = []
        for _ in range(args.runden):
            t = time.perf_counter()
            grid = b.BentoGrid(fenster, context=ctx)
            grid.pack(fill="both", expand=True)
            for i in range(60):
                karte = b.BentoCard(grid, context=ctx, title=f"Karte {i}", spec=b.BentoCardSpec(f"k{i}", span=2 if i % 7 == 0 else 1))
                b.BentoMetric(karte.body, context=ctx, value=str(i), label="Wert").pack(fill="x")
                grid.add_card(karte)
            fenster.update()
            for breite in (500, 900, 1200):
                fenster.geometry(f"{breite}x900")
                fenster.update()
                grid.reflow()
                fenster.update()
            bento.append((time.perf_counter() - t) * 1000)
            grid.destroy()
            fenster.update()
        fenster.destroy()
        ergebnis["bento_60_karten_3_breiten"] = verteilung(bento)

        def widgets(w):
            return 1 + sum(widgets(k) for k in w.winfo_children())
        ergebnis["ressourcen"] = {"widgets": widgets(root), "after_offen": len(root.tk.call("after", "info").split() if
                                                                                isinstance(root.tk.call("after", "info"), str)
                                                                                else root.tk.call("after", "info")),
                                  "bilder": len(root.tk.call("image", "names")),
                                  "arbeitsspeicher_mb": arbeitsspeicher_mb(),
                                  "tracemalloc_spitze_mb": round(tracemalloc.get_traced_memory()[1] / 2 ** 20, 1)}
        ergebnis["fehler"] = fehler
        try:
            app.on_close()
        except Exception:  # noqa: BLE001
            root.destroy()
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Messung {args.marke or ''}: Kaltstart {ergebnis['kaltstart']['bis_bereit']['median_ms']} ms, "
          f"Warmstart {ergebnis['warmstart_ms']} ms, Themenwechsel {ergebnis['themenwechsel']['median_ms']} ms, "
          f"Bento 60 Karten {ergebnis['bento_60_karten_3_breiten']['median_ms']} ms, Fehler {len(fehler)} → {args.json}")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
