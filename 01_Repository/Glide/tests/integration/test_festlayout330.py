"""Feste Bestandteile bleiben fest (Entscheidung des Nutzers vom 27.09.2026).

Beim Wechsel zwischen Aufgabenliste, Liste im Unterordner, Notiz, Zeichnung,
Seite, Galerie, Ordner und „Mein Tag“ verschieben sich weder Seitenleiste,
Kopfzeile, Kopfknöpfe, Suchzeile noch die Inhaltsfläche – auch nicht beim
Markieren eines Punkts und auch nicht bei Mindestgröße. Über dem Titel steht
kein Ordnerpfad mehr. Seite, Zeichnung und Galerie tragen ihre Werkzeuge in
der festen Leiste über der Fläche.
"""
import importlib.machinery
import importlib.util
import os
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True

with tempfile.TemporaryDirectory(prefix="glide-fest-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_fest", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1280x860+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    # Geprüft wird hier ausdrücklich der aufgeklappte Hinweiszustand (U02).
    app.settings["view_hints"] = {key: True for key in ("list", "folder", "trash", "in_progress", app.TABLE_VIEW, app.PLAN_DAY_VIEW, app.LABELS_VIEW)}
    app.show_info = app.show_warning = app.show_error = lambda *args, **kwargs: None

    def ruhe(runden=10):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    try:
        ruhe()
        kunden = app.new_folder_object("Kunden")
        nord = app.new_folder_object("Nord", parent_id=kunden["id"])
        app.folders += [kunden, nord]
        tief = app.new_list_object("Angebote Nord", [app.new_item("Angebot")], folder_id=nord["id"])
        notiz = app.new_list_object("Notiz", [], list_kind="note")
        zeichnung = app.new_list_object("Zeichnung", [], list_kind="drawing")
        galerie = app.new_list_object("Galerie", [], list_kind="gallery")
        app.lists += [tief, notiz, zeichnung, galerie]
        seite = app.new_page_from_markdown("# Seite\n\nText")
        app.save_items()
        ruhe()
        aufgaben = next(entry for entry in app.lists if not entry.get("folder_id")
                        and entry.get("list_kind", "tasks") == "tasks" and not app.is_inbox_list(entry)
                        and entry.get("items"))
        faelle = [
            ("Aufgaben", lambda: app.set_active_list(aufgaben["id"])),
            ("Liste im Unterordner", lambda: app.set_active_list(tief["id"])),
            ("Notiz", lambda: app.set_active_list(notiz["id"])),
            ("Zeichnung", lambda: app.set_active_list(zeichnung["id"])),
            ("Seite", lambda: app.set_active_list(seite["id"])),
            ("Galerie", lambda: app.set_active_list(galerie["id"])),
            ("Ordner", lambda: app.set_active_folder(kunden["id"])),
            ("Mein Tag", app.set_today_view),
            ("zurück zu Aufgaben", lambda: app.set_active_list(aufgaben["id"])),
        ]
        teile = {"Seitenleiste": app.sidebar_frame, "Kopfzeile": app.header_frame,
                 "Kopfknöpfe": app.header_controls, "Inhaltsfläche": app.list_frame_outer}

        def mass(widget):
            if not widget.winfo_ismapped():
                return None
            return (widget.winfo_rootx() - root.winfo_rootx(), widget.winfo_rooty() - root.winfo_rooty(),
                    widget.winfo_width(), widget.winfo_height())

        for groesse in ("1280x860", "860x700"):
            root.geometry(groesse + "+0+30")
            ruhe(14)
            basis = None
            suche = None
            for name, oeffnen in faelle:
                oeffnen()
                ruhe()
                werte = {teil: mass(widget) for teil, widget in teile.items()}
                assert all(werte.values()), (groesse, name, werte)
                if basis is None:
                    basis = werte
                    suche = mass(app.search_frame)
                abweichung = {teil: (basis[teil], wert) for teil, wert in werte.items() if wert != basis[teil]}
                assert not abweichung, f"{groesse} · {name} verschiebt: {abweichung}"
                if app.search_frame.winfo_ismapped():
                    assert mass(app.search_frame)[1] == suche[1], f"{groesse} · {name}: Suchzeile verschoben"
                assert not app.path_row.winfo_children(), "kein Ordnerpfad über dem Titel"
            # Markieren eines Punkts ändert die Fläche nicht.
            app.set_active_list(aufgaben["id"])
            ruhe()
            vorher = mass(app.list_frame_outer)
            erster = app.tree.get_children()[0]
            app.tree.selection_set(erster)
            ruhe()
            assert app.selection_bar.winfo_ismapped(), "Auswahlleiste sichtbar"
            assert mass(app.list_frame_outer) == vorher, (groesse, "Auswahl verschiebt die Fläche")
            app.tree.selection_set(())
            ruhe()
            assert mass(app.list_frame_outer) == vorher
            # Bei schmaler Liste weicht der Hinweis ohnehin (update_hint_visibility).
            if getattr(app, "_hint_visible", True):
                assert app.hint_label.winfo_ismapped(), (groesse, "ohne Auswahl steht wieder der Hinweis da")

        # Werkzeuge der Seite, Zeichnung und Galerie liegen in der festen Leiste.
        root.geometry("1280x860+0+30")
        ruhe(14)
        for liste in (seite, zeichnung, galerie):
            app.set_active_list(liste["id"])
            ruhe()
            assert app.tool_band.winfo_ismapped() and app.tool_band_inner.winfo_children(), liste["title"]
            unten = app.tool_band.winfo_rooty() + app.tool_band.winfo_height()
            assert unten <= app.list_frame_outer.winfo_rooty(), "Leiste über der Fläche"
        app.set_active_list(aufgaben["id"])
        ruhe()
        assert not app.tool_band.winfo_ismapped() and not app.tool_band_inner.winfo_children(), \
            "Werkzeuge verschwinden mit ihrer Ansicht"
        assert not fehler, fehler
    finally:
        try:
            root.destroy()
        except Exception:
            pass

print("test_festlayout330: OK; Seitenleiste, Kopf, Suche und Fläche fest in 9 Ansichten, "
      "mit Auswahl und bei Mindestgröße.")
