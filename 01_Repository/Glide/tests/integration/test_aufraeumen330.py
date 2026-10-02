"""Aufräumen, Seitenbereich und Galerie (27.09.2026).

- Kopfzeile nur mit Symbolen: ⌘ Aktionen, ✎ Schnellerfassung, ⍾ Benachrichtigungen.
- Keine Knöpfe unter dem Listenbaum; „+“ neben „Listen“ öffnet das
  Anlegen-Menü, Listenzeilen zeigen beim Überfahren „…“.
- Auswahlleiste nur mit markierten Punkten; Ansichtsumschalter Liste ·
  Tabelle · Pinnwand mit hervorgehobener Ansicht.
- Kennzahlen nur einmal; Seite ohne Eingabe- und Suchzeile, auch nach einer
  Zeichnung; Textlogo in der Akzentfarbe; Gismo ohne eigenes Rechteck;
  Fahne „Erledigt!“ unten statt über dem Suchfeld; „Startseite anpassen“
  ohne Kästen hinter Text.
- Pinnwand: Aktionen und Schalter in einer Zeile, Spalten teilen sich die
  Breite.
- Seitenbereich „Seiten +“, Seitenvorlagen, eigenes Seitenformat `.glidepage`;
  Aufgabenmarken folgen neuen Kennungen.
- Galerie: Bilder als Anhänge, Kacheln, Titel und Notiz, Entfernen und
  Rückgängig, Speichern.
"""
import importlib.machinery
import importlib.util
import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True

with tempfile.TemporaryDirectory(prefix="glide-aufraeumen-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_aufraeumen", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1300x860+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    app.show_info = app.show_warning = lambda *args, **kwargs: None
    app.show_error = lambda *args, **kwargs: fehler.append(args)
    # Die Beispieldaten verweisen auf Anhänge, deren Dateien hier fehlen; der
    # Import legt vorher eine Sicherung an und bräuchte sie.
    for halter in app.lists + app.folders:
        halter["attachments"] = []
        for punkt in app.walk_items(halter.get("items", [])):
            punkt["attachments"] = []

    def ruhe(runden=6):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    try:
        normal = next(entry for entry in app.lists
                      if entry.get("list_kind") in (None, "", "list", "tasks") and len(entry.get("items", [])) > 5)
        zeichnung = next(entry for entry in app.lists if entry.get("list_kind") == "drawing")

        # --- Kopfzeile ---------------------------------------------------------
        app.set_active_list(normal["id"])
        ruhe()
        assert app.actions_button.text == app.ICONS["actions"] == "⌘"
        assert app.capture_button.text == app.ICONS["capture"] == "↯"
        assert len({app.ICONS[key] for key in ("capture", "edit", "actions", "list", "history", "notifications")}) == 6
        assert app.notifications_button.text.startswith(app.ICONS["notifications"])
        assert app.ICONS["actions"] != app.ICONS["list"], "ein Zeichen, eine Bedeutung"
        assert "Benachrichtigungen" not in app.notifications_button.text
        # Kennzahlen nur einmal: unter dem Titel, nicht rechts daneben.
        assert app.page_chips() and app._stats_full_text == ""
        app.set_active_list(zeichnung["id"])
        ruhe()
        assert "Noch keine Aufgaben" not in app._stats_full_text

        # --- Seitenleiste ------------------------------------------------------
        for veraltet in ("import_list_button", "add_folder_button", "rename_list_button", "delete_list_button",
                         "sidebar_actions_frame"):
            assert not hasattr(app, veraltet), veraltet
        menue = app.folder_quick_add_menu(None)
        eintraege = [menue.entrycget(index, "label") for index in range(menue.index("end") + 1)
                     if menue.type(index) == "command"]
        # Seit 3.33.1 nimmt „Listen“ jede Art auf, also auch Buch und Notizbuch
        # (Vertrag 74); gleiche Reihenfolge wie im Ordnermenü (test_features330).
        assert eintraege == ["Neue Liste …", "Neue Seite", "Neue Notiz …", "Neue Pinnwand …", "Neue Galerie",
                             "Neue Zeichnung", "Neuer Ordner …", "Neues Buch …", "Neues Notizbuch …",
                             "Listen importieren …"], eintraege
        listen_iid = f"list:{normal['id']}"
        app.sidebar_listbox.see(listen_iid)
        ruhe()
        box = app.sidebar_listbox.bbox(listen_iid)
        app.on_sidebar_quick_motion(SimpleNamespace(x=20, y=box[1] + box[3] // 2))
        assert app.sidebar_quick_kind == "list" and app.sidebar_quick_more_button.winfo_manager() == "place"
        assert app.sidebar_quick_add_button.winfo_manager() == ""
        app.hide_sidebar_quick_actions()

        # --- Auswahlleiste und Ansichtsumschalter -----------------------------
        app.set_active_list(normal["id"])
        app.open_list_view()
        ruhe()
        assert not app.selection_bar.winfo_ismapped()
        # Seit 29.09.2026 teilen sich Hinweis und Leiste den Kartenfuß.
        assert app.card_foot_mode() == "hint" and app.hint_label.winfo_ismapped(), "ohne Auswahl der Hinweis"
        zeilen = [iid for iid in app.tree.get_children("") if app.find_item(iid)]
        app.tree.selection_set(zeilen[:2])
        ruhe()
        assert app.selection_bar.winfo_ismapped()
        assert app.selection_count_label.cget("text") == "2 Punkte"
        assert [knopf.color_key for knopf in app.selection_buttons] == ["muted"] * 4 + ["delete"]
        app.tree.selection_set(())
        ruhe()
        assert not app.selection_bar.winfo_ismapped()
        assert app.list_view_button.active_fill == app.theme["selection"]
        assert app.table_button.active_fill is None and app.board_button.active_fill is None
        app.set_table_view()
        ruhe()
        assert app.table_button.active_fill == app.theme["selection"]
        app.set_trash_view()
        ruhe()
        assert app.button_frame.winfo_manager() == "" and app.card_foot_mode() == "hint"

        # --- Seite nach Zeichnung ohne Eingabe und Suche ------------------------
        seite = app.new_page_from_markdown("# Bericht\n\nText\n\n- [ ] Aufgabe eins\n")
        ruhe()
        app.set_active_list(zeichnung["id"])
        ruhe()
        app.set_active_list(seite["id"])
        ruhe()
        assert app.input_frame.winfo_manager() == "" and app.search_frame.winfo_manager() == ""
        app.set_active_list(normal["id"])
        ruhe()
        assert app.input_frame.winfo_manager() == "pack" and app.search_frame.winfo_manager() == "pack"
        assert app.input_frame.winfo_y() < app.search_frame.winfo_y() < app.list_frame_outer.winfo_y()

        # --- Textlogo, Gismo, Fahne, Startseite anpassen ----------------------
        app.settings["accent_color"] = "confirm"
        app.apply_theme()
        ruhe()
        grund = app.theme["ui_accent"]
        erwartet = (mod.mix_to_luminance(grund, "#000000", app.LABEL_CHIP_DARK_FILL_LUMINANCE)
                    if app.theme_name == "dark" else
                    mod.mix_to_luminance(grund, "#FFFFFF", app.LABEL_CHIP_LIGHT_FILL_LUMINANCE))
        assert app.monogram_colors()[0] == erwartet, "Logo in der Akzentfarbe"
        app.settings["accent_color"] = "accent"
        app.apply_theme()
        rahmen = mod.tk.Frame(root, bg="#123456")
        figur = mod.MascotCanvas(rahmen, app, size=40)
        figur.redraw()
        assert str(figur.cget("bg")).lower() == "#123456", "Gismo steht auf der Farbe seiner Fläche"
        rahmen.destroy()
        app.settings["animations_enabled"] = True
        ruhe()
        # Direkt nach dem Auslösen geprüft: Die Fahne lebt nur eine halbe Sekunde.
        app.play_celebration("Test")
        fahnen = [kind for kind in app.main_area.winfo_children()
                  if isinstance(kind, mod.tk.Label) and kind.winfo_manager() == "place"]
        assert fahnen, "Fahne im Arbeitsbereich"
        assert float(fahnen[0].place_info()["rely"]) == 1.0 and fahnen[0].place_info()["anchor"] == "s", \
            fahnen[0].place_info()
        for fahne in fahnen:
            fahne.destroy()
        app.set_home_view()
        ruhe()
        app.toggle_home_editing()
        ruhe()
        stapel, kaesten = [app.home_content], []
        while stapel:
            widget = stapel.pop()
            stapel.extend(widget.winfo_children())
            if widget.winfo_class() == "Label" and widget.master in (app.home_content,) + tuple(
                    kind for kind in app.home_content.winfo_children() if isinstance(kind, mod.tk.Frame)):
                if str(widget.cget("bg")).lower() == app.theme["bg"].lower():
                    kaesten.append(widget.cget("text"))
        assert not kaesten, kaesten
        app.toggle_home_editing()
        ruhe()

        # --- Pinnwand: eine Zeile, Spalten füllen die Breite ------------------
        flaeche = app.workspace
        app.set_active_list(normal["id"])
        app.open_board_view()
        ruhe()
        root.geometry("2400x900+0+30")
        ruhe(10)
        stufe, einzeilig, _kurz, _anzahl = flaeche._board_controls_narrow
        if flaeche.bar.winfo_width() >= 1800:
            assert einzeilig, "Aktionen und Schalter in einer Zeile"
        assert "Anheften" in [getattr(kind, "text", "") for kind in flaeche.bar.winfo_children()]
        root.geometry("1300x860+0+30")
        ruhe(10)
        flaeche.configure_board("layout", "columns")
        ruhe()
        breite_vorher = flaeche.board()["width"]
        flaeche.canvas.winfo_width = lambda: 5 * (breite_vorher + flaeche.CARD_GAP) - 200
        flaeche.draw_columns()
        breiten = {box[2] for box in flaeche.column_boxes.values()}
        spalten = len(flaeche.column_boxes)
        if spalten == 5:
            assert max(breiten) < breite_vorher, "fünf Spalten passen durch schmalere Spalten"
        del flaeche.canvas.winfo_width
        flaeche.configure_board("layout", "free")
        app.open_list_view()
        ruhe()

        # --- Seitenbereich -----------------------------------------------------
        bibliothek = app.new_folder_object("Bücher", folder_kind="library")
        app.folders.append(bibliothek)
        buch = app.new_page_from_markdown("# Hobbit\n\n- [ ] Lesen\n")
        buch["folder_id"] = bibliothek["id"]
        app.save_items()
        app.update_sidebar_list()
        ruhe()
        baum = app.pages_listbox
        assert baum.exists(f"list:{seite['id']}") and baum.exists(f"folder:{bibliothek['id']}")
        assert baum.exists(f"list:{buch['id']}")
        assert not app.sidebar_listbox.exists(f"folder:{bibliothek['id']}")
        assert not app.system_listbox.exists(app.PAGES_ROW_ID)
        assert app.pages_title_row.winfo_y() > app.system_listbox.winfo_y()
        assert app.pages_title_row.winfo_y() < app.sidebar_title_row.winfo_y()
        app.set_active_list(buch["id"])
        ruhe()
        assert baum.selection() == (f"list:{buch['id']}",)
        # Seitenvorlagen: mitgeliefert und eigene.
        besprechung = app.create_page_from_template("besprechung")
        ruhe()
        assert besprechung["list_kind"] == "page" and besprechung["title"].startswith("Besprechung ")
        vorlage = app.capture_template(list_id=seite["id"])
        assert vorlage["id"] in [eintrag["id"] for eintrag in app.page_templates()]
        aus_vorlage = app.create_list_from_template(vorlage["id"])
        ruhe()
        punkte = {punkt["id"] for punkt in aus_vorlage["items"]}
        marken = [span["tag"][5:] for span in aus_vorlage["rich_note"]["spans"] if span["tag"].startswith("item:")]
        assert marken and set(marken) <= punkte, "Aufgabenmarken folgen den neuen Kennungen"
        # Duplikat: ebenso.
        app.duplicate_list(seite["id"])
        kopie = app.current_list()
        marken = [span["tag"][5:] for span in kopie["rich_note"]["spans"] if span["tag"].startswith("item:")]
        assert marken and set(marken) <= {punkt["id"] for punkt in kopie["items"]}
        # Eigenes Seitenformat.
        pfad = os.path.join(ordner, "buecher.glidepage")
        mod.filedialog.asksaveasfilename = lambda **kwargs: pfad
        app.export_glide_pages([], [bibliothek["id"]])
        assert json.loads(zipfile.ZipFile(pfad).read("data.json"))["content"] == "pages"
        neu = app.import_glide_pages(pfad)
        ruhe()
        assert [eintrag["title"] for eintrag in neu] == ["Hobbit"]
        marken = [span["tag"][5:] for span in neu[0]["rich_note"]["spans"] if span["tag"].startswith("item:")]
        assert marken and set(marken) <= {punkt["id"] for punkt in neu[0]["items"]}
        fremd = os.path.join(ordner, "liste.glidepage")
        app.write_complete_backup(fremd, app.partial_backup_payload([normal["id"]], []))
        vorher = len(fehler)
        assert app.import_glide_pages(fremd) is None and len(fehler) == vorher + 1, "Listen gehören nicht hinein"
        del fehler[vorher:]

        # --- Galerie -----------------------------------------------------------
        assert app.LIST_KINDS["gallery"]["label"] == "Galerie"
        bilder = []
        for name, farbe in (("rot", "#D04040"), ("blau", "#4060D0")):
            bild = mod.tk.PhotoImage(width=80, height=60)
            bild.put(farbe, to=(0, 0, 80, 60))
            bildpfad = os.path.join(ordner, f"{name}.png")
            bild.write(bildpfad, format="png")
            bilder.append(bildpfad)
        galerie = app.create_new_gallery()
        ruhe()
        app.add_gallery_images(galerie["id"], bilder)
        ruhe()
        ansicht = app.gallery_view
        assert isinstance(ansicht, mod.GalleryView) and len(ansicht.hits) == 2
        assert app.page_chips() == ["2 Bilder"]
        assert app.input_frame.winfo_manager() == "" and not app.view_switch.winfo_ismapped()
        assert app.sidebar_listbox.set(f"list:{galerie['id']}", "count") == "(2)"
        assert not app.require_list_view(message=False), "Eine Galerie nimmt keine Punkte auf"
        ansicht.open_detail(0)
        ruhe()
        assert ansicht.detail_index == 0
        erstes = galerie["attachments"][0]["id"]
        assert app.set_gallery_caption(galerie["id"], erstes, "Rotes Bild", "Notiz")
        ansicht.close_detail()
        app.remove_gallery_image(galerie["id"], galerie["attachments"][1]["id"])
        ruhe()
        galerie = next(eintrag for eintrag in app.lists if eintrag["id"] == galerie["id"])
        assert len(galerie["attachments"]) == 1
        app.undo_last_change()
        ruhe()
        galerie = next(eintrag for eintrag in app.lists if eintrag["id"] == galerie["id"])
        assert len(galerie["attachments"]) == 2
        app.save_items()
        with open(mod.SAVE_FILE, encoding="utf-8") as datei:
            roh = next(eintrag for eintrag in json.load(datei)["lists"] if eintrag["id"] == galerie["id"])
        assert roh["list_kind"] == "gallery" and roh["attachments"][0]["title"] == "Rotes Bild"
        assert app.normalize_attachments(roh["attachments"])[0]["note"] == "Notiz"
        bereinigt = app.normalize_personal_settings({"gallery_tile_size": {"a": "large", "b": "riesig", 3: "small"}})
        assert bereinigt["gallery_tile_size"] == {"a": "large"}
        assert not fehler, fehler[:1]
    finally:
        app.dirty = False
        root.destroy()

print("test_aufraeumen330: OK; Kopfzeile aus Symbolen, Seitenleiste ohne Fußknöpfe, Auswahlleiste, "
      "Ansichtsumschalter, Seite ohne Eingabe, Textlogo, Gismo, Fahne, Startseite ohne Kästen, Pinnwandzeile, "
      "Spaltenbreite, Seitenbereich, Seitenvorlagen, Seitenformat und Galerie geprüft.")
