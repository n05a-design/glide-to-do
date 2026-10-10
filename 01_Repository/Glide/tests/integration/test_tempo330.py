"""Tempo beim Scrollen, gemessen gegen reines Tk (Befund R6, 29.09.2026).

Absolute Zeiten hängen am Rechner. Deshalb misst die Suite zuerst, wie lange
reines Tk braucht, um eine Liste mit 85 Zeilen einen Schritt zu scrollen, und
vergleicht Glide damit. Gemessen wird dauerhaftes Scrollen wie mit einem
Trackpad: ein Ereignis, dann darf Tk zeichnen. Liste, Tabelle und Seite
bekommen Schritte von drei Zeilen, damit jedes Bild wirklich scrollt.

Grenzen (großzügig, damit Last auf dem Prüfrechner nicht stört):

- Liste, Tabelle und Seite: höchstens das Dreifache von reinem Tk;
- Startseite und „Listen und Ordner“ mit Farbverlauf: höchstens das
  Sechsfache; vor dem 29.09.2026 lag die Übersicht beim Zwölffachen.

Die Messwerte stehen in der Ausgabe und gehören in den QA-Bericht.
"""
import importlib.machinery
import importlib.util
import os
import statistics
import sys
import tempfile
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True

with tempfile.TemporaryDirectory(prefix="glide-tempo-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_releaseplanung_3.30.0.glidebackup") as archiv:
        fixture_bytes = archiv.read("data.json")
        Path(ordner, "liste_speicher.json").write_bytes(fixture_bytes)
    loader = importlib.machinery.SourceFileLoader("glide_tempo", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    # Die historische Format-20-Fixture migriert vor der Scrollmessung.
    # Nur diesen erwarteten Hinweis abfangen; unerwartete Meldungen bleiben Fehler.
    migration_notices = []

    def accept_fixture_migration(app, title, message, **options):
        assert title == "Bestand umgestellt", (title, message)
        assert "Datenformat 20" in message and f"Format {app.DATA_SCHEMA_VERSION}" in message
        backups = list(Path(mod.BACKUP_DIR).glob(f"liste_vor_format{app.DATA_SCHEMA_VERSION}_*.json"))
        assert any(path.read_bytes() == fixture_bytes for path in backups), "Historische Fixture muss bytegleich gesichert sein"
        migration_notices.append(title)

    mod.ListApp.show_info = accept_fixture_migration
    tk, ttk = mod.tk, mod.ttk
    root = tk.Tk()
    root.geometry("1400x950+20+20")
    touchpad_supported = int(root.tk.call("info", "patchlevel").split(".")[0]) >= 9
    callback_errors = []
    root.report_callback_exception = lambda *error: callback_errors.append(error)

    def ruhe(runden=6):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    def bildzeit(widget, sekunden=1.2, schritt=-6, packed=True, require_scroll=False):
        """Mittlere Zeit je Bild beim dauerhaften Scrollen in ms."""
        widget.update()
        x, y = widget.winfo_width() // 2, widget.winfo_height() // 2
        zeiten, runde = [], 0
        positions = {widget.yview()}
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            richtung = schritt if (runde // 25) % 2 == 0 else -schritt
            start = time.perf_counter()
            if packed and touchpad_supported:
                widget.event_generate("<TouchpadScroll>", delta=richtung & 0xffff, x=x, y=y)
            elif sys.platform.startswith("linux"):
                widget.event_generate("<Button-5>" if richtung < 0 else "<Button-4>", x=x, y=y)
            else:
                widget.event_generate("<MouseWheel>", delta=-120 if richtung < 0 else 120, x=x, y=y)
            root.update()
            positions.add(widget.yview())
            zeiten.append((time.perf_counter() - start) * 1000)
            runde += 1
        if require_scroll:
            assert len(positions) > 1, "Scrollereignisse bewegen die lange Prüfansicht nicht"
        return statistics.mean(zeiten)

    # --- Vergleich: reines Tk --------------------------------------------------
    rein = tk.Toplevel(root)
    rein.geometry("1400x950+20+20")
    baum = ttk.Treeview(rein)
    baum.pack(fill="both", expand=True)
    for nummer in range(85):
        baum.insert("", "end", text=f"Zeile {nummer} " + "Text " * 10)
    baum.bind("<MouseWheel>", lambda e: baum.yview_scroll(-1 if e.delta > 0 else 1, "units") or "break")
    rein.update()
    time.sleep(0.3)
    grund = bildzeit(baum, packed=False, require_scroll=True)
    rein.destroy()

    app = mod.ListApp(root)
    werte = {}
    try:
        time.sleep(0.4)
        ruhe()
        groesste = max(app.lists, key=lambda e: app.count_items(e.get("items", [])))
        app.set_active_list(groesste["id"])
        ruhe()
        werte["Liste"] = bildzeit(app.tree, schritt=-48, require_scroll=True)
        app.set_table_view()
        ruhe()
        werte["Tabelle"] = bildzeit(app.tree, schritt=-48, require_scroll=True)
        seite = app.new_page_from_markdown("# Tempo\n\n" + "\n\n".join(
            f"Absatz {i} " + "Text " * 40 for i in range(200)))
        ruhe()
        app.set_active_list(seite["id"])
        ruhe()
        werte["Seite"] = bildzeit(app.rich_note_editor.text, schritt=-48, require_scroll=True)
        app.set_design("dark")
        ruhe()
        import backdrop as glide_backdrop  # noqa: E402 – liegt neben app.pyw
        app.set_backdrop_choice(glide_backdrop.presets_for(app.design_name())[1].key)
        ruhe()
        time.sleep(0.3)
        app.set_home_view()
        ruhe()
        werte["Startseite mit Verlauf"] = bildzeit(app.home_canvas)
        app.set_library_view()
        ruhe()
        werte["Listen und Ordner mit Verlauf"] = bildzeit(app.home_canvas)
        # Nach dem Scrollen sitzt der Verlauf wieder (Abgleich nach der Ruhe).
        time.sleep(0.4)
        ruhe()
        assert not getattr(app, "_backdrop_settle_job", None)
    finally:
        root.destroy()

    assert not callback_errors, callback_errors

    print(f"Reines Tk: {grund:.1f} ms je Bild")
    for name, wert in werte.items():
        print(f"{name}: {wert:.1f} ms je Bild ({wert / max(grund, 1):.1f}× reines Tk)")
    for name in ("Liste", "Tabelle", "Seite"):
        assert werte[name] <= 3 * grund + 20, (name, werte[name], grund)
    for name in ("Startseite mit Verlauf", "Listen und Ordner mit Verlauf"):
        assert werte[name] <= 6 * grund + 40, (name, werte[name], grund)

print("OK: Scrolltempo gegen reines Tk gemessen.")
