#!/usr/bin/env python3
"""Dauer- und Belastungslauf mit echten Tk-Zyklen und synthetischen Daten.

Warum es das braucht: Der vollständige Prüflauf stellt sicher, dass jede
Funktion einmal richtig arbeitet. Er sagt nichts darüber, was nach Stunden
passiert – und genau dort sitzen die Fehler, die im Alltag weh tun: ein Timer,
der bei jedem Durchgang einen neuen hinterlässt, ein Undo-Stapel, der nie
beschnitten wird, ein Zustellbeleg, der sich nach dem hundertsten Prüflauf doch
wiederholt. Seit 3.8.0 tickt die Erinnerungsprüfung alle 15 Sekunden; damit
läuft zum ersten Mal etwas dauerhaft im Hintergrund.

Der Lauf baut einen großen Bestand auf, lässt die Uhr echt weiterlaufen und
bedient die App dabei fortlaufend. Gemessen wird nicht die Geschwindigkeit –
dafür gibt es `leistungspruefung.py` – sondern ob etwas wächst, das nicht
wachsen darf, und ob der Bestand danach unversehrt ist.

Aufruf:

    python3 tests/tools/dauerlauf.py --minuten 10 --aufgaben 4000 \
        --ziel tests/qa-3.8.0/dauerlauf/ergebnis.json

Kurzer Rauchtest: `--minuten 1 --aufgaben 500`. Ein voller Nachweis braucht
mindestens zehn Minuten, damit der 15-Sekunden-Takt oft genug feuert.
Exitcode 1 bei einem Befund. Es werden ausschließlich synthetische Daten in
einem isolierten `GLIDE_DATA_DIR` verwendet.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import platform
import statistics
import tempfile
import time
import tracemalloc

REPO = Path(__file__).resolve().parents[2]


def bestand_aufbauen(app, mod, aufgaben):
    """Ordner, Listen, Gruppen, Serien und Erinnerungen in realistischer Mischung."""
    jetzt = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    faellig = (jetzt - timedelta(minutes=5)).isoformat(timespec="seconds")
    pro_liste = max(50, aufgaben // 20)
    erzeugt = 0
    listen = 0
    while erzeugt < aufgaben:
        punkte = []
        for i in range(min(pro_liste, aufgaben - erzeugt)):
            nummer = erzeugt + i
            # Jede zwanzigste Aufgabe ist eine Gruppe mit drei Unterpunkten,
            # jede zehnte trägt eine bereits fällige Erinnerung, jede
            # fünfundzwanzigste wiederholt sich täglich.
            if nummer % 20 == 19:
                punkte.append(app.new_item(
                    f"Sammlung {nummer:05}", kind=app.ITEM_KIND_GROUP,
                    children=[app.new_item(f"Schritt {nummer:05}-{k}") for k in range(3)]))
                continue
            punkte.append(app.new_item(
                f"Aufgabe {nummer:05}",
                importance=nummer % 3,
                due="2090-09-14" if nummer % 4 == 0 else None,
                due_time="12:00" if nummer % 8 == 0 else None,
                repeat={"art": app.REPEAT_DAILY} if nummer % 25 == 0 else None,
                reminder={"mode": "fixed", "at": faellig} if nummer % 10 == 0 else
                         ({"mode": "relative", "minutes": 60} if nummer % 13 == 0 else None)))
        ordner = None
        if listen % 3 == 0:
            ordner = app.new_folder_object(title=f"Vorhaben {listen:02}")
            app.folders.append(ordner)
        eintrag = app.new_list_object(f"Liste {listen:02}", punkte,
                                      folder_id=ordner["id"] if ordner else None)
        app.lists.append(eintrag)
        erzeugt += sum(1 for _ in app.walk_items(eintrag["items"]))
        listen += 1
    app.set_active_list(app.lists[-1]["id"])
    return {"listen": listen, "ordner": len(app.folders), "punkte": erzeugt}


def punkte_zaehlen(app):
    return sum(1 for eintrag in app.lists for _ in app.walk_items(eintrag.get("items", [])))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--minuten", type=float, default=10.0, help="Laufzeit in Minuten")
    parser.add_argument("--aufgaben", type=int, default=4000, help="Größe des synthetischen Bestands")
    parser.add_argument("--ziel", type=Path, help="Pfad für den JSON-Bericht")
    parser.add_argument("--runde-sekunden", type=float, default=5.0,
                        help="Abstand zwischen zwei Messrunden")
    args = parser.parse_args()
    if args.minuten <= 0 or args.aufgaben < 1 or args.runde_sekunden <= 0:
        parser.error("Laufzeit, Bestandsgröße und Rundenabstand müssen positiv sein")

    with tempfile.TemporaryDirectory(prefix="glide-dauerlauf-") as temp:
        os.environ["GLIDE_DATA_DIR"] = temp
        os.environ["GLIDE_TEST_MODE"] = "1"
        loader = importlib.machinery.SourceFileLoader("glide_dauerlauf", str(REPO / "src/glide/app.pyw"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        mod = importlib.util.module_from_spec(spec)
        loader.exec_module(mod)

        tracemalloc.start()
        root = mod.tk.Tk()
        root.withdraw()
        fehler = []
        root.report_callback_exception = lambda *a: fehler.append(repr(a))
        app = mod.ListApp(root)
        app.show_error = lambda *a, **kw: fehler.append(("show_error",) + a)
        app.show_warning = lambda *a, **kw: fehler.append(("show_warning",) + a)
        app.show_info = lambda *a, **kw: None
        app.ask_yes_no = lambda *a, **kw: True
        root.geometry("1280x900+20+20")
        root.deiconify()

        bericht = {
            "version": mod.APP_VERSION,
            "python": platform.python_version(),
            "plattform": platform.platform(),
            "tk": root.tk.call("info", "patchlevel"),
            "laufzeit_minuten": args.minuten,
            "runden": [],
            "grenzen": ("Synthetische Daten ohne Anhänge in isoliertem Datenordner. "
                        "Kein Ersatz für Ruhezustand, Mehrmonitor- oder Screenreader-Abnahme."),
        }
        aufbau_start = time.perf_counter()
        bericht["bestand"] = bestand_aufbauen(app, mod, args.aufgaben)
        assert app.save_items(), "Ausgangsbestand ließ sich nicht speichern"
        app.refresh_tree()
        root.update()
        bericht["aufbau_ms"] = round((time.perf_counter() - aufbau_start) * 1000, 2)
        punkte_vorher = punkte_zaehlen(app)

        ende = time.perf_counter() + args.minuten * 60
        runde = 0
        while time.perf_counter() < ende:
            runde += 1
            rundenschluss = min(time.perf_counter() + args.runde_sekunden, ende)
            # Echte Zeit vergehen lassen, damit die registrierten Tk-Callbacks
            # von selbst feuern – der 15-Sekunden-Takt der Erinnerungen ebenso
            # wie Autosave und Uhr.
            while time.perf_counter() < rundenschluss:
                root.update()
                time.sleep(0.02)

            # Bedienung: Liste wechseln, neu zeichnen, eine Aufgabe abschließen
            # und wieder zurücknehmen. Das erzeugt Undo-Stände und Speicherlast.
            ziel_liste = app.lists[runde % len(app.lists)]
            app.set_active_list(ziel_liste["id"])
            start = time.perf_counter()
            app.refresh_tree()
            root.update_idletasks()
            refresh_ms = round((time.perf_counter() - start) * 1000, 2)

            offen = next((p for p in app.walk_items(ziel_liste["items"])
                          if p.get("kind") == app.ITEM_KIND_TASK and not p.get("done")), None)
            if offen is not None:
                with app.item_change([offen["id"]]) as change:
                    offen["done"] = True
                    change.mark()
                app.undo_last_change()

            start = time.perf_counter()
            gespeichert = app.save_items()
            save_ms = round((time.perf_counter() - start) * 1000, 2)
            if not gespeichert:
                fehler.append(("save_items", f"Runde {runde}"))

            aktuell, spitze = tracemalloc.get_traced_memory()
            bericht["runden"].append({
                "runde": runde,
                "sekunden": round(time.perf_counter() - (ende - args.minuten * 60), 1),
                "after_callbacks": len(getattr(app, "_after_ids", ())),
                "undo_staende": len(app.undo_stack),
                "offene_erinnerungen": sum(r["state"] == "Offen / verpasst" for r in app.reminder_rows()),
                "python_speicher_mb": round(aktuell / 1048576, 2),
                "python_spitze_mb": round(spitze / 1048576, 2),
                "refresh_ms": refresh_ms,
                "save_ms": save_ms,
                "datei_kb": round(Path(mod.SAVE_FILE).stat().st_size / 1024, 1),
                "punkte": punkte_zaehlen(app),
            })

        # Unversehrtheit nach dem Lauf: Speichern, neu laden, Bestand vergleichen.
        assert app.save_items()
        vor_neuladen = {p["id"] for eintrag in app.lists for p in app.walk_items(eintrag.get("items", []))}
        app.load_items()
        nach_neuladen = {p["id"] for eintrag in app.lists for p in app.walk_items(eintrag.get("items", []))}
        bericht["integritaet"] = {
            "punkte_vorher": punkte_vorher,
            "punkte_nachher": len(nach_neuladen),
            "identitaeten_gleich": vor_neuladen == nach_neuladen,
            "verlorene_punkte": sorted(vor_neuladen - nach_neuladen)[:10],
        }

        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
        tracemalloc.stop()

    # Befunde: Was nach dem Einschwingen noch wächst, wächst zu Unrecht.
    runden = bericht["runden"]
    befunde = []
    if len(runden) < 3:
        befunde.append("Zu wenige Messrunden für eine Aussage; Laufzeit erhöhen.")
    else:
        eingeschwungen = runden[max(1, len(runden) // 5):]
        erste, letzte = eingeschwungen[0], eingeschwungen[-1]
        if letzte["after_callbacks"] > erste["after_callbacks"] + 2:
            befunde.append(f"Offene Tk-Callbacks wachsen: {erste['after_callbacks']} → {letzte['after_callbacks']}")
        if letzte["undo_staende"] > erste["undo_staende"] + 5:
            befunde.append(f"Undo-Stände wachsen: {erste['undo_staende']} → {letzte['undo_staende']}")
        grund = max(erste["python_speicher_mb"], 1.0)
        zuwachs = (letzte["python_speicher_mb"] - erste["python_speicher_mb"]) / grund * 100
        bericht["speicherzuwachs_prozent"] = round(zuwachs, 1)
        if zuwachs > 25:
            befunde.append(f"Python-Speicher wächst um {zuwachs:.1f} % nach dem Einschwingen")
        if letzte["punkte"] != erste["punkte"]:
            befunde.append(f"Bestandsgröße verändert sich: {erste['punkte']} → {letzte['punkte']}")
        bericht["refresh_median_ms"] = statistics.median(r["refresh_ms"] for r in eingeschwungen)
        bericht["save_median_ms"] = statistics.median(r["save_ms"] for r in eingeschwungen)
    if not bericht["integritaet"]["identitaeten_gleich"]:
        befunde.append("Nach dem Neuladen fehlen Punkte oder haben andere Identitäten")
    if fehler:
        befunde.append(f"{len(fehler)} gemeldete Fehler während des Laufs")
    bericht["fehler"] = [str(f)[:300] for f in fehler[:20]]
    bericht["befunde"] = befunde

    if args.ziel:
        args.ziel.parent.mkdir(parents=True, exist_ok=True)
        args.ziel.write_text(json.dumps(bericht, ensure_ascii=False, indent=2), encoding="utf-8")

    letzte_runde = runden[-1] if runden else {}
    print(f"Dauerlauf {bericht['version']} · {len(runden)} Runden über {args.minuten} Minuten")
    print(f"Bestand: {bericht['bestand']['punkte']} Punkte in {bericht['bestand']['listen']} Listen, "
          f"{bericht['bestand']['ordner']} Ordner; Aufbau {bericht['aufbau_ms']} ms")
    if runden:
        print(f"Zuletzt: {letzte_runde['after_callbacks']} offene Callbacks, "
              f"{letzte_runde['undo_staende']} Undo-Stände, "
              f"{letzte_runde['python_speicher_mb']} MB, "
              f"Neuzeichnen {bericht.get('refresh_median_ms')} ms, "
              f"Speichern {bericht.get('save_median_ms')} ms")
    print("Unversehrt nach Neuladen:", "ja" if bericht["integritaet"]["identitaeten_gleich"] else "NEIN")
    if befunde:
        print("BEFUNDE:")
        for eintrag in befunde:
            print("  -", eintrag)
        return 1
    print("OK: keine Befunde")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
