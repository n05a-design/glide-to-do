"""Jedes Fenster über den Weg, den der Nutzer nimmt (Befunde R10 und R11, 29.09.2026).

Die Suite öffnet alle Fenster über Menüleiste, Kontextmenüs, „+“-Menüs und die
Knöpfe mit Fensterfolge – nicht über den direkten Funktionsaufruf. Einträge
mit „…“ laufen dabei wie in der App erst nach dem Schließen des Menüs.

Für jedes Fenster wird geprüft:

- es erscheint sichtbar und liegt ganz auf dem Bildschirm;
- jeder Knopf ist sichtbar und liegt im Fenster;
- Esc schließt es.

Mit `GLIDE_FENSTER_FOTOS=<Ordner>` legt die Suite unter macOS von jedem
Fenster ein Foto nur dieses Fensters ab (`screencapture -l`).
"""
import importlib.machinery
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
BILD = REPO / "src/glide/resources/logo/glide-app-icon.png"
FOTOS = os.environ.get("GLIDE_FENSTER_FOTOS")

with tempfile.TemporaryDirectory(prefix="glide-fenster-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_fenster", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)

    # Dateiauswahl: Öffnen liefert ein Testbild, Speichern bricht ab. Jeder
    # Aufruf zählt als geöffnetes Systemfenster.
    systemfenster = []
    mod.filedialog.askopenfilename = lambda *a, **k: (systemfenster.append("öffnen"), str(BILD))[1]
    mod.filedialog.askopenfilenames = lambda *a, **k: (systemfenster.append("öffnen"), (str(BILD),))[1]
    mod.filedialog.asksaveasfilename = lambda *a, **k: (systemfenster.append("speichern"), "")[1]
    mod.filedialog.askdirectory = lambda *a, **k: (systemfenster.append("ordner"), "")[1]
    mod.messagebox.askyesno = lambda *a, **k: False
    mod.messagebox.askokcancel = lambda *a, **k: False

    befunde = []
    fenster = []
    offene_wege = []
    root_holder = {}

    def fenster_foto(dialog, name):
        if not FOTOS or sys.platform != "darwin":
            return
        try:
            import ctypes
            import ctypes.util
            cf = ctypes.cdll.LoadLibrary(ctypes.util.find_library("CoreFoundation"))
            cg = ctypes.cdll.LoadLibrary(ctypes.util.find_library("CoreGraphics"))
            cf.CFStringCreateWithCString.restype = ctypes.c_void_p
            cf.CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32]
            cf.CFArrayGetCount.restype = ctypes.c_long
            cf.CFArrayGetCount.argtypes = [ctypes.c_void_p]
            cf.CFArrayGetValueAtIndex.restype = ctypes.c_void_p
            cf.CFArrayGetValueAtIndex.argtypes = [ctypes.c_void_p, ctypes.c_long]
            cf.CFDictionaryGetValue.restype = ctypes.c_void_p
            cf.CFDictionaryGetValue.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
            cf.CFNumberGetValue.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
            cg.CGWindowListCopyWindowInfo.restype = ctypes.c_void_p
            cg.CGWindowListCopyWindowInfo.argtypes = [ctypes.c_uint32, ctypes.c_uint32]

            def schluessel(text):
                return cf.CFStringCreateWithCString(None, text.encode(), 0x08000100)

            def zahl(eintrag, key):
                wert = cf.CFDictionaryGetValue(eintrag, key)
                ergebnis = ctypes.c_int64()
                if wert:
                    cf.CFNumberGetValue(wert, 4, ctypes.byref(ergebnis))
                return ergebnis.value
            liste = cg.CGWindowListCopyWindowInfo(1 | 16, 0)
            k_pid, k_nr, k_ebene = schluessel("kCGWindowOwnerPID"), schluessel("kCGWindowNumber"), \
                schluessel("kCGWindowLayer")
            eigene = [zahl(cf.CFArrayGetValueAtIndex(liste, i), k_nr) for i in range(cf.CFArrayGetCount(liste))
                      if zahl(cf.CFArrayGetValueAtIndex(liste, i), k_pid) == os.getpid()
                      and zahl(cf.CFArrayGetValueAtIndex(liste, i), k_ebene) == 0]
            if eigene:
                os.makedirs(FOTOS, exist_ok=True)
                sicher = "".join(z if z.isalnum() else "_" for z in name)[:60]
                subprocess.run(["screencapture", "-x", "-o", "-l", str(eigene[0]),
                                os.path.join(FOTOS, f"{len(fenster):03d}_{sicher}.png")], check=False)
        except Exception as exc:  # Fotos sind ein Zusatz, kein Prüfschritt.
            befunde.append(("Foto", name, str(exc)))

    def in_scroll_flaeche(widget, dialog):
        """Liegt der Knopf in einem scrollbaren Formular (Leinwand)? Dann darf er außerhalb stehen."""
        w = widget.master
        while w is not None and w is not dialog:
            if isinstance(w, mod.tk.Canvas) and not isinstance(w, mod.RoundedButton):
                return True
            w = w.master
        return False

    def pruefen_und_schliessen(self, dialog, parent=None):
        """Ersetzt `run_modal`: Fenster prüfen, fotografieren, mit Esc schließen."""
        root = root_holder["root"]
        titel = ""
        try:
            self.bring_dialog_to_front(dialog)
            for _ in range(4):
                dialog.update_idletasks()
                dialog.update()
            titel = dialog.title() or dialog.winfo_name()
            fenster.append(titel)
            if not dialog.winfo_ismapped():
                befunde.append(("nicht sichtbar", titel, ""))
            x, y = dialog.winfo_rootx(), dialog.winfo_rooty()
            b, h = dialog.winfo_width(), dialog.winfo_height()
            sb, sh = dialog.winfo_screenwidth(), dialog.winfo_screenheight()
            if x < -2 or y < -2 or x + b > sb + 2 or y + h > sh + 2:
                befunde.append(("außerhalb des Bildschirms", titel, (x, y, b, h, sb, sh)))
            stapel = [dialog]
            while stapel:
                w = stapel.pop()
                stapel.extend(w.winfo_children())
                if isinstance(w, mod.RoundedButton) and w.winfo_manager() and not in_scroll_flaeche(w, dialog):
                    rx, ry = w.winfo_rootx() - x, w.winfo_rooty() - y
                    if not w.winfo_ismapped() and w.winfo_manager() != "place":
                        # Überlauf in scrollbaren Formularen ist erlaubt, wenn die
                        # Fläche scrollt; ein unsichtbarer Knopf der Fußzeile nicht.
                        if ry > h:
                            befunde.append(("Knopf nicht erreichbar", titel, w.text))
                    elif rx + w.winfo_width() > b + 2 or ry + w.winfo_height() > h + 2:
                        befunde.append(("Knopf ragt heraus", titel, w.text))
            fenster_foto(dialog, titel)
            dialog.focus_force()
            dialog.event_generate("<Escape>")
            for _ in range(3):
                root.update()
            if dialog.winfo_exists():
                befunde.append(("Esc schließt nicht", titel, ""))
                dialog.destroy()
        except mod.tk.TclError:
            pass

    mod.ListApp.run_modal = pruefen_und_schliessen
    popups = []
    mod.tk.Menu.tk_popup = lambda self, *a, **k: popups.append(self)

    root = mod.tk.Tk()
    root_holder["root"] = root
    root.geometry("1300x900+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    meldungen = []
    for name in ("show_info", "show_warning", "show_error"):
        setattr(app, name, lambda *a, _n=name, **k: meldungen.append((_n, a)))
    app.ask_yes_no = lambda *a, **k: False
    app.ask_yes_no_cancel = lambda *a, **k: None
    app.open_path_external = getattr(app, "open_path_external", None) and (lambda *a, **k: None)

    def ruhe(runden=4):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    AUSGENOMMEN = ("Beenden", "leeren", "löschen", "Löschen", "Datenordner wechseln", "Papierkorb",
                   "Zurücksetzen", "entfernen", "Entfernen")

    def zustand():
        """Was sich nach einem Klick zeigen kann: Fenster, Meldung, Systemfenster, Ansicht."""
        return (len(fenster), len(meldungen), len(systemfenster), app.view_mode,
                getattr(app, "_quick_open", None) is not None, app.home_mode() if hasattr(app, "home_mode") else None)

    def menue_durchlaufen(menu, weg):
        """Ruft jeden Eintrag mit „…“ auf; Untermenüs rekursiv."""
        try:
            ende = menu.index("end")
        except mod.tk.TclError:
            return
        if ende is None:
            return
        for index in range(ende + 1):
            try:
                art = menu.type(index)
            except mod.tk.TclError:
                continue
            if art == "cascade":
                try:
                    menue_durchlaufen(root.nametowidget(menu.entrycget(index, "menu")),
                                      weg + [menu.entrycget(index, "label")])
                except (KeyError, mod.tk.TclError):
                    pass
                continue
            if art != "command":
                continue
            label = str(menu.entrycget(index, "label"))
            if not label.rstrip().endswith(("…", "...")) or any(wort in label for wort in AUSGENOMMEN):
                continue
            if str(menu.entrycget(index, "state")) == "disabled":
                continue
            vorher = zustand()
            try:
                menu.invoke(index)
                ruhe()
            except Exception as exc:  # noqa: BLE001 – jeder Fehler ist ein Befund
                befunde.append(("Fehler beim Öffnen", " › ".join(weg + [label]), repr(exc)))
            if zustand() == vorher:
                offene_wege.append(" › ".join(weg + [label]))
            if getattr(app, "_quick_open", None) is not None:
                app.close_quick_open()
            app.set_active_list(liste["id"])
            ruhe(2)

    try:
        time.sleep(0.4)
        ruhe()
        liste = next(e for e in app.lists if len(e.get("items", [])) > 5)
        app.set_active_list(liste["id"])
        ruhe()
        # 1. Menüleiste
        leiste = root.nametowidget(root.cget("menu"))
        menue_durchlaufen(leiste, [])
        anzahl_leiste = len(fenster)
        # 2. „+“-Menüs der Seitenleiste
        for knopf, befehl in ((app.add_list_button, app.show_sidebar_add_menu),
                              (app.add_pages_button, app.show_pages_add_menu),
                              (app.add_notes_button, app.show_notes_add_menu)):
            popups.clear()
            app._popup_at_widget = lambda menu, widget: popups.append(menu)
            befehl()
            for menu in list(popups):
                menue_durchlaufen(menu, [knopf.text if hasattr(knopf, "text") else "+"])
        del app._popup_at_widget
        # 3. Kontextmenüs von Liste und Ordner
        ordner_id = next(f["id"] for f in app.folders)
        for menu, name in ((app.build_list_menu(liste["id"]), "Liste"),
                           (app.build_folder_menu(ordner_id), "Ordner")):
            if menu is not None:
                menue_durchlaufen(menu, [f"Kontextmenü {name}"])
        # 4. Zeichnung: Knopf „Referenz“ und „Mehr“
        app.create_new_drawing()
        ruhe()
        zeichnung = app.drawing_editor
        vorher = len(fenster)
        zeichnung.toggle_reference()
        ruhe(6)
        if len(fenster) == vorher:
            offene_wege.append("Zeichnung › Knopf Referenz")
        popups.clear()
        app.show_drawing_menu(zeichnung, zeichnung.more_button)
        for menu in list(popups):
            menue_durchlaufen(menu, ["Zeichnung › Mehr"])

        print(f"{len(fenster)} Fenster geöffnet und geprüft ({anzahl_leiste} über die Menüleiste).")
        if offene_wege:
            print("Ohne Fenster oder Meldung:", "; ".join(offene_wege[:12]))
        if befunde:
            print("Befunde:", json.dumps(befunde[:20], ensure_ascii=False, default=str))
        assert len(fenster) >= 40, len(fenster)
        # Ein Menüeintrag mit „…“ öffnet ein Fenster oder sagt, warum nicht.
        assert not offene_wege, offene_wege
        assert not [b for b in befunde if b[0] != "Foto"], befunde[:10]
        assert not fehler, fehler[:1]
    finally:
        try:
            root.destroy()
        except Exception:
            pass

print("OK: Fenster über Menüs und Knöpfe geöffnet, sichtbar, im Bildschirm, Knöpfe erreichbar, Esc schließt.")
