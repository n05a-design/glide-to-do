"""Inhaltskarte bis ganz unten und saubere Ansichtswechsel (Auftrag vom 29.09.2026).

- Die Inhaltskarte endet in jeder Ansicht auf der Unterkante der Seitenleiste.
  Hinweis und Auswahlleiste stehen im Kartenfuß fester Höhe; beim Markieren
  ändert sich weder die Karte noch die Liste darin.
- Pinnwand, Seite, Notiz, Zeichnung und Galerie haben keinen Kartenfuß; ihre
  Bedienhinweise stehen in der Werkzeugleiste bzw. in der Pinnwandzeile.
- Die Startseite zeigt nach keinem Wechsel eine Listenzeile. Bis 29.09.2026
  stand nach „Mein Tag“ die Eingabezeile unter den Kacheln (Rückmeldung mit
  Bildschirmfoto); nach dem Papierkorb und einer Seite ebenso.
- Zurück in der Liste stehen Eingabe, Suche und Karte wieder in dieser Folge.
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

with tempfile.TemporaryDirectory(prefix="glide-kartenfuss-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_kartenfuss", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1280x860+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *args, **kwargs: None

    def ruhe(runden=8):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    def unterkante(widget):
        return widget.winfo_rooty() + widget.winfo_height()

    def lage(widget):
        if not widget.winfo_ismapped():
            return None
        return (widget.winfo_rootx() - root.winfo_rootx(), widget.winfo_rooty() - root.winfo_rooty(),
                widget.winfo_width(), widget.winfo_height())

    try:
        ruhe()
        notiz = app.new_list_object("Notiz", [], list_kind="note")
        zeichnung = app.new_list_object("Zeichnung", [], list_kind="drawing")
        galerie = app.new_list_object("Galerie", [], list_kind="gallery")
        app.lists += [notiz, zeichnung, galerie]
        seite = app.new_page_from_markdown("# Seite\n\nText\n\n- [ ] Aufgabe")
        app.save_items()
        ruhe()
        aufgaben = max((eintrag for eintrag in app.lists if eintrag.get("list_kind", "tasks") == "tasks"
                        and not app.is_inbox_list(eintrag)), key=lambda eintrag: len(eintrag.get("items", [])))
        ordner_eintrag = next(eintrag for eintrag in app.folders if not eintrag.get("parent_id"))

        def liste():
            app.set_active_list(aufgaben["id"])
            app.open_list_view()

        def tabelle():
            app.set_active_list(aufgaben["id"])
            app.set_table_view()

        def pinnwand():
            app.set_active_list(aufgaben["id"])
            app.open_board_view()

        # Ansicht → erwarteter Kartenfuß ("hint" = Hinweis, None = kein Fuß,
        # "seite" = Seitenansicht ohne Listenoberfläche).
        ansichten = {
            "Startseite": (app.set_home_view, "seite"),
            "Mein Tag": (app.set_today_view, "hint"),
            "In Bearbeitung": (app.set_in_progress_view, "hint"),
            "Labels": (app.set_labels_view, "hint"),
            "Papierkorb": (app.set_trash_view, "hint"),
            "Vorlagen": (app.set_template_view, "seite"),
            "Bibliothek": (app.set_library_view, "seite"),
            "Seitenübersicht": (app.set_pages_view, "seite"),
            "Verlauf": (app.open_history_view, "seite"),
            "Globale Pinnwand": (app.open_global_board, None),
            "Liste": (liste, "hint"),
            "Tabelle": (tabelle, "hint"),
            "Pinnwand": (pinnwand, None),
            "Notiz": (lambda: app.set_active_list(notiz["id"]), None),
            "Zeichnung": (lambda: app.set_active_list(zeichnung["id"]), None),
            "Seite": (lambda: app.set_active_list(seite["id"]), None),
            "Galerie": (lambda: app.set_active_list(galerie["id"]), None),
            "Ordner": (lambda: app.set_active_folder(ordner_eintrag["id"]), "hint"),
        }
        reihe = ["input_frame", "tool_band", "search_frame", "list_frame_outer"]

        def zeilen():
            namen = {str(getattr(app, name)): name for name in reihe + ["home_frame", "template_actions"]
                     if getattr(app, name, None) is not None}
            koerper = getattr(app.workspace, "body", None)
            if koerper is not None:
                namen[str(koerper)] = "workspace_body"
            return [namen.get(str(widget), str(widget)) for widget in app.content_frame.pack_slaves()]

        def pruefen(von, nach):
            _oeffnen, erwartet = ansichten[nach]
            stand = zeilen()
            if erwartet == "seite":
                rest = [name for name in stand if name not in ("home_frame", "template_actions")]
                assert not rest, f"{von} → {nach}: Listenzeilen in einer Seitenansicht {stand}"
                return
            assert "home_frame" not in stand, f"{von} → {nach}: Startseite steht noch {stand}"
            folge = [reihe.index(name) for name in stand if name in reihe]
            assert folge == sorted(folge), f"{von} → {nach}: Zeilenfolge {stand}"
            assert not [name for name in stand if name not in reihe + ["workspace_body"]], (von, nach, stand)
            assert app.card_foot_mode() == erwartet, (von, nach, app.card_foot_mode(), erwartet)
            assert abs(unterkante(app.list_frame_outer) - unterkante(app.sidebar_shell)) <= 1, \
                (von, nach, "Karte endet auf der Unterkante der Seitenleiste",
                 unterkante(app.list_frame_outer), unterkante(app.sidebar_shell))
            if erwartet is None:
                assert app.card_foot.winfo_manager() == "", (von, nach, "ohne Aufgabe kein Fuß")
            else:
                assert app.card_foot.winfo_height() == app.card_foot_height(), (von, nach)
                assert app.hint_label.winfo_ismapped() and app.hint_label.cget("text"), (von, nach)

        wechsel = 0
        for name, (oeffnen, _erwartet) in ansichten.items():
            for von, nach in ((name, "Startseite"), ("Startseite", name), (name, "Liste")):
                if von == nach:
                    continue
                ansichten[von][0]()
                ruhe(4)
                ansichten[nach][0]()
                ruhe()
                pruefen(von, nach)
                wechsel += 1
        assert wechsel >= 50, wechsel

        # --- Markieren ändert weder Karte noch Liste; Fuß tauscht nur den Inhalt --
        for groesse in ("1280x860", "860x700"):
            root.geometry(groesse + "+0+30")
            ruhe(14)
            liste()
            ruhe()
            karte, baum, fuss = lage(app.list_frame_outer), lage(app.tree), lage(app.card_foot)
            assert app.card_foot_mode() == "hint" and not app.selection_bar.winfo_ismapped()
            erster = next(iid for iid in app.tree.get_children("") if app.find_item(iid))
            app.tree.selection_set(erster)
            ruhe()
            assert app.card_foot_mode() == "bar" and app.selection_bar.winfo_ismapped(), groesse
            assert not app.hint_label.winfo_ismapped(), "Leiste ersetzt den Hinweis"
            assert (lage(app.list_frame_outer), lage(app.tree), lage(app.card_foot)) == (karte, baum, fuss), \
                (groesse, "Markieren verschiebt etwas")
            knoepfe = [knopf for knopf in app.selection_buttons if knopf.winfo_ismapped()]
            assert knoepfe and all(knopf.winfo_height() == app.SELECTION_BUTTON_HEIGHT for knopf in knoepfe)
            assert all(unterkante(knopf) <= unterkante(app.card_foot) for knopf in knoepfe), "Leiste im Fuß"
            app.tree.selection_set(())
            ruhe()
            assert app.card_foot_mode() == "hint" and app.hint_label.winfo_ismapped()
            assert (lage(app.list_frame_outer), lage(app.tree)) == (karte, baum)
            # Der Hinweis passt in zwei Zeilen; der volle Text steht im Tooltip.
            assert app.hint_label.text_size()[1] <= app.hint_line_height(app.HINT_MAX_LINES) + 2

        # --- Hinweise der Flächen in der Werkzeugleiste bzw. Pinnwandzeile ------
        root.geometry("1280x860+0+30")
        ruhe(14)
        for eintrag in (seite, zeichnung, galerie):
            app.set_active_list(eintrag["id"])
            ruhe()
            text = app.tool_band_hint.cget("text")
            assert app.tool_band.winfo_ismapped() and text, eintrag["title"]
            assert app.tool_band_hint.text_size()[1] <= app.hint_line_height(1, app.tool_band_hint) + 2, \
                "eine Zeile"
            assert unterkante(app.tool_band_hint) <= app.list_frame_outer.winfo_rooty(), "über der Karte"
        pinnwand()
        ruhe()
        assert "Doppelklick: öffnen" in app.workspace._board_notice_text
        liste()
        ruhe()
        assert not app.tool_band.winfo_ismapped() and not app.tool_band_hint.cget("text")
        assert not fehler, fehler[:1]
    finally:
        try:
            root.destroy()
        except Exception:
            pass

print(f"test_kartenfuss330: OK; {wechsel} Ansichtswechsel ohne Listenzeile auf der Startseite und in "
      "fester Folge, Karte bis zur Unterkante, Kartenfuß mit Hinweis oder Auswahlleiste ohne Verschieben, "
      "Flächenhinweise in der Werkzeugleiste.")
