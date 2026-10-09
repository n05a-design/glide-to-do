"""Befunde der Rückmeldung vom 29.09.2026 (R1–R5, R7–R11, B3).

- R11: Menüeinträge mit „…“ laufen erst nach dem Schließen des Menüs; Dialoge
  kommen nach vorn; ein Rekursionsfehler steht mit Ablaufspur im Protokoll.
- R1: Nach dem Einklappen zeichnet die Seitenleiste neu.
- R2: Der waagrechte Anteil einer Trackpad-Geste schiebt die Pinnwand quer.
- R3: Die Suche ist ein Rahmen mit Rand in der Akzentfarbe; ein Klick daneben
  schließt sie, ein Klick hinein nicht.
- R7: Beim Größeziehen eines Seitenbilds rechnet Glide das Bild nicht bei jeder
  Mausbewegung neu.
- R9: Die Farbleiste der Zeichnung zeigt höchstens sieben Farben.
- R10: „Referenz“ ohne Referenz öffnet die Bildauswahl; JPEG und SVG werden zu
  PNG.
- R4: Rechtsklick in Seiten (Bearbeiten, Formatieren, Umwandeln, Zeilen),
  Formatleiste über einer Markierung.
- R5 und B3: Notizen nutzen den Seiteneditor ohne Aufgabenzeilen; eine Notiz
  ohne Punkte zeigt keine leere Punktliste.
- R8: Jeder Knopf im Quelltext trägt die Farbe seiner Bedeutung.
"""
import importlib.machinery
import importlib.util
import os
import sys
import tempfile
import time
import zipfile
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
LOGO = REPO / "src/glide/resources/logo"

with tempfile.TemporaryDirectory(prefix="glide-befunde-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_befunde", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    meldungen = []
    for name in ("show_info", "show_warning", "show_error"):
        setattr(mod.ListApp, name, lambda self, *a, _n=name, **k: meldungen.append((_n, a)))
    root = mod.tk.Tk()
    root.geometry("1300x900+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)

    def ruhe(runden=6):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    try:
        time.sleep(0.4)
        ruhe()

        # --- R11 und Hänger vom 30.09.2026: jeder Menübefehl läuft nach dem Menü -
        aufrufe = []
        menu = mod.tk.Menu(root, tearoff=0)
        wahl = mod.tk.BooleanVar(master=root, value=False)
        menu.add_command(label="Fenster öffnen …", command=lambda: aufrufe.append("fenster"))
        menu.add_command(label="Über Glide", command=lambda: aufrufe.append("ueber"))
        menu.insert_command(0, label="Auch ein Fenster ...", command=lambda: aufrufe.append("punkte"))
        menu.add_checkbutton(label="Häkchen", variable=wahl, command=lambda: aufrufe.append("haken"))
        menu.invoke(1)
        menu.invoke(2)
        menu.invoke(0)
        menu.invoke(3)
        assert aufrufe == ["haken"], "kein Befehl läuft innerhalb der Menüverfolgung; Häkchen sofort"
        assert wahl.get() is True, "das Häkchen selbst wechselt sofort"
        ruhe(2)
        assert sorted(aufrufe) == ["fenster", "haken", "punkte", "ueber"], aufrufe
        menu.destroy()
        # Rekursionsfehler: vollständiger, gekürzter Bericht statt einer Zeile.

        def tief(n):
            return tief(n + 1)
        try:
            tief(0)
        except RecursionError as exc:
            bericht = app.format_error_report(type(exc), exc, exc.__traceback__)
        assert "in tief" in bericht and "RecursionError" in bericht and "weitere Aufrufe" in bericht, bericht[:300]
        assert len(bericht.splitlines()) < 70
        # Dialoge kommen nach vorn, auch wenn sie ausgeblendet entstehen.
        dialog = mod.tk.Toplevel(root)
        dialog.withdraw()
        app.bring_dialog_to_front(dialog)
        ruhe()
        assert dialog.state() == "normal"
        dialog.destroy()

        # --- R1: Neu zeichnen nach dem Einklappen -------------------------------
        notiz = app.new_list_object("Tagebuch", [], list_kind="note")
        app.lists.append(notiz)
        app.save_items()
        app.update_sidebar_list()
        ruhe()
        gerufen = []
        original = app.repaint_sidebar
        app.repaint_sidebar = lambda: (gerufen.append(1), original())
        app.notes_heading_icon.event_generate("<Button-1>")
        app.sidebar_heading_icon.event_generate("<Button-1>")
        ruhe()
        assert app.notes_listbox.winfo_manager() == "" and app.sidebar_listbox.winfo_manager() == ""
        assert len(gerufen) >= 2, gerufen
        del app.repaint_sidebar
        app.toggle_sidebar_section("notes")
        app.toggle_sidebar_section("lists")
        ruhe()
        # R1 zweiter Teil (30.09.2026): Das „…“ beim Überfahren einer Notiz
        # verschwindet mit dem Einklappen.
        app.create_new_note()
        app.set_home_view()
        ruhe()
        baum = app.notes_listbox
        zeile = baum.get_children("")[0]
        bx, by, _bb, bh = baum.bbox(zeile)
        baum.event_generate("<Motion>", x=bx + 40, y=by + bh // 2)
        ruhe()
        knoepfe = [k for paar in app.sidebar_quick_buttons.values() for k in paar]
        assert any(k.winfo_manager() for k in knoepfe), "Knöpfe erscheinen beim Überfahren"
        app.notes_heading_icon.event_generate("<Button-1>")
        ruhe()
        assert not baum.winfo_manager() and not any(k.winfo_manager() for k in knoepfe)
        app.toggle_sidebar_section("notes")
        ruhe()

        # --- R2: Trackpad quer auf der Pinnwand ---------------------------------
        liste = next(e for e in app.lists if len(e.get("items", [])) > 5)
        app.set_active_list(liste["id"])
        app.workspace.set_mode("board")
        ruhe()
        flaeche = app.workspace.canvas
        flaeche.configure(scrollregion=(0, 0, 6000, 4000))
        flaeche.xview_moveto(0.3)
        vorher = flaeche.xview()[0]

        def geste(dx, dy):
            return ((dx & 0xffff) << 16) | (dy & 0xffff)
        app._on_mousewheel(SimpleNamespace(delta=geste(-40, 0)), flaeche, precise=True)
        assert flaeche.xview()[0] > vorher, (vorher, flaeche.xview())
        vorher_y = flaeche.yview()[0]
        app._on_mousewheel(SimpleNamespace(delta=geste(0, -30)), flaeche, precise=True)
        ruhe()  # senkrechtes Scrollen sammelt sich seit R6 bis zum nächsten Leerlauf
        assert flaeche.yview()[0] != vorher_y or flaeche.yview() == (0.0, 1.0)
        app.workspace.set_mode("list")
        ruhe()

        # --- R3: Suche ohne Schatten, Klick außerhalb schließt ------------------
        app.set_home_view()
        ruhe()
        app.show_quick_open()
        ruhe()
        buehne = app._quick_open["stage"]
        assert isinstance(buehne, mod.tk.Frame) and not isinstance(buehne, mod.tk.Canvas)
        assert int(buehne.cget("highlightthickness")) == app.QUICK_OPEN_BORDER
        assert buehne.cget("highlightbackground") == app.theme["ui_accent"]
        # Eigene, vom Design abgesetzte Fläche (Empfehlung a in R3).
        assert buehne.cget("bg").lower() != app.theme["card"].lower()
        assert buehne.cget("bg").lower() == mod.mix_hex_colors(app.theme["card"], app.theme["text"],
                                                               app.QUICK_OPEN_SURFACE_MIX).lower()
        app._quick_open["entry"].event_generate("<ButtonPress-1>", x=3, y=3)
        ruhe()
        assert app._quick_open is not None, "Klick ins Feld schließt nicht"
        app.home_canvas.event_generate("<ButtonPress-1>", x=3, y=3)
        ruhe()
        assert app._quick_open is None, "Klick daneben schließt"
        # Ein weiterer Klick irgendwo stört nichts mehr (Bindung entfernt).
        app.home_canvas.event_generate("<ButtonPress-1>", x=3, y=3)
        ruhe()

        # --- R7: Bild ziehen ohne ständiges Neurechnen ---------------------------
        seite = app.new_page_from_markdown("# Bilder\n\nText davor\n\nText danach\n")
        ruhe()
        app.set_active_list(seite["id"])
        ruhe()
        editor = app.rich_note_editor
        editor.insert_images([str(LOGO / "glide-app-icon.png")])
        ruhe(10)
        schluessel = next(iter(editor.images))
        ansicht = editor._image_views[schluessel]
        zaehler = {"n": 0}
        echt = app.previews.image
        app.previews.image = lambda *a, **k: (zaehler.__setitem__("n", zaehler["n"] + 1), echt(*a, **k))[1]
        breite = editor.images[schluessel].get("width") or 200
        editor._image_drag = {"key": schluessel, "art": "groesse", "x": 0, "y": 0, "breite": breite,
                              "hoehe": breite, "dx": 0, "dy": 0}
        for schritt in range(20):
            editor.image_motion(schluessel, SimpleNamespace(x_root=-schritt * 3, y_root=0))
        assert zaehler["n"] == 0, "beim Ziehen kein sofortes Neurechnen"
        time.sleep(0.2)
        ruhe()
        assert zaehler["n"] <= 2, zaehler  # vorher je Mausbewegung eine, also 20
        editor.image_release(schluessel, SimpleNamespace(x_root=-60, y_root=0))
        ruhe()
        app.previews.image = echt
        assert editor.images[schluessel]["width"] < breite

        # --- R9: höchstens sieben Farben ---------------------------------------
        app.create_new_drawing()
        ruhe()
        zeichnung = app.drawing_editor
        farben = [f"#{wert:02X}{wert:02X}10" for wert in range(10, 250, 12)]
        for index, farbe in enumerate(farben):
            zeichnung.model.set_cell(index, 0, farbe)
        assert len(zeichnung.model.used_colors()) >= 15
        gruppen = zeichnung.strip_groups()
        assert all(len(farben_) <= zeichnung.STRIP_COLOR_LIMIT for titel, farben_ in gruppen
                   if titel == "Zuletzt"), gruppen
        if app.drawing_tool_settings().get("palette") in (None, "drawing"):
            assert len(gruppen) == 1, "ohne feste Palette nur eine Reihe"

        # --- R10: Referenz öffnen, JPEG und SVG ---------------------------------
        geoeffnet = []
        app.drawing_load_reference = lambda editor: geoeffnet.append(editor)
        zeichnung.toggle_reference()
        ruhe(2)
        assert geoeffnet == [zeichnung], "Referenz ohne Bild öffnet die Auswahl"
        del app.drawing_load_reference
        svg = app.reference_png_path(str(LOGO / "glide-logo.svg"))
        assert svg.endswith(".png") and app.read_reference_png(svg).width() > 0
        assert app.reference_png_path(str(LOGO / "glide-logo.png")).endswith("glide-logo.png")
        if app.previews.can_convert():
            jpeg = os.path.join(ordner, "probe.jpg")
            import subprocess
            if sys.platform == "darwin":
                subprocess.run(["sips", "-s", "format", "jpeg", str(LOGO / "glide-app-icon.png"), "--out", jpeg],
                               capture_output=True, check=False)
            if os.path.isfile(jpeg):
                umgewandelt = app.reference_png_path(jpeg)
                assert umgewandelt.endswith(".png") and app.read_reference_png(umgewandelt).width() > 0
        try:
            app.reference_png_path(os.path.join(ordner, "text.txt"))
        except mod.glide_drawing.DrawingFormatError:
            pass
        else:
            raise AssertionError("Textdatei muss abgelehnt werden")

        # --- R4: Rechtsklick, Umwandeln, Zeilen, Formatleiste in Seiten ----------
        seite = app.new_page_from_markdown("# Titel\n\nErste Zeile\n\nZweite Zeile\n\nDritte Zeile\n")
        ruhe()
        app.set_active_list(seite["id"])
        ruhe()
        ed = app.rich_note_editor
        text = ed.text
        menues = []
        original_popup = ed.popup
        ed.popup = lambda menu: menues.append(menu)
        zeile = next(i for i in range(1, 12) if text.get(f"{i}.0", f"{i}.end") == "Zweite Zeile")
        text.mark_set("insert", f"{zeile}.2")
        ed.show_context_menu(None)
        menu = menues.pop()
        stelle = {menu.entrycget(i, "label"): i for i in range(menu.index("end") + 1) if menu.type(i) != "separator"}
        labels = list(stelle)
        for erwartet in ("Ausschneiden", "Kopieren", "Einfügen", "Als reinen Text einfügen", "Alles markieren",
                         "Formatieren", "Umwandeln in", "Zeile nach oben", "Zeile nach unten",
                         "Zeile duplizieren", "Zeile löschen"):
            assert erwartet in labels, (erwartet, labels)
        assert menu.entrycget(stelle["Kopieren"], "state") == "disabled", "ohne Markierung"
        umwandeln = root.nametowidget(menu.entrycget(stelle["Umwandeln in"], "menu"))
        arten = [umwandeln.entrycget(i, "label").strip("✓ ").strip() for i in range(umwandeln.index("end") + 1)]
        assert arten == ["Text", "Überschrift 1", "Überschrift 2", "Überschrift 3", "Überschrift 4", "Aufzählung",
                         "Nummerierung", "Aufgabe", "Aufklappliste", "Aufklappüberschrift", "Zitat",
                         "Hinweisblock", "Code"], arten
        ed.convert_block("h2")
        assert "h2" in ed.line_blocks(f"{zeile}.0")
        ed.convert_block("text")
        assert not ed.line_blocks(f"{zeile}.0")
        ed.convert_block("quote")
        ed.move_line(-1)
        ruhe()
        oben = int(text.index("insert").split(".")[0])
        assert text.get(f"{oben}.0", f"{oben}.end") == "Zweite Zeile" and "quote" in ed.line_blocks(f"{oben}.0")
        assert oben < zeile, "Zeile samt Zitatformat eine Zeile höher"
        ed.move_line(1)
        ruhe()
        assert text.get("insert linestart", "insert lineend") == "Zweite Zeile"
        vorher = text.get("1.0", "end")
        ed.duplicate_line()
        assert text.get("1.0", "end").count("Zweite Zeile") == 2
        ed.delete_line()
        assert text.get("1.0", "end").count("Zweite Zeile") == 1
        assert "Zweite Zeile" in text.get("1.0", "end") and len(vorher) > 0
        # Formatleiste über einer Markierung
        start = text.search("Dritte", "1.0")
        text.tag_add("sel", start, f"{start} +6c")
        ed.sync_format_bar()
        ruhe()
        assert ed._format_bar is not None and ed._format_bar.winfo_manager() == "place"
        knoepfe = [w.text for w in ed._format_bar.winfo_children() if isinstance(w, mod.RoundedButton)]
        assert knoepfe[:2] == ["Text ▾", "B"] and "Link" in knoepfe, knoepfe
        ed.format("bold")
        assert "bold" in text.tag_names(start)
        ed.clear_format()
        assert "bold" not in text.tag_names(start)
        text.tag_remove("sel", "1.0", "end")
        ed.sync_format_bar()
        assert ed._format_bar.winfo_manager() == "", "ohne Markierung keine Leiste"
        ed.popup = original_popup

        # --- R5 und B3: Notizen schreiben wie Seiten ---------------------------
        notiz = app.new_list_object("Schreibprobe", [], list_kind="note")
        app.lists.append(notiz)
        app.save_items()
        app.set_active_list(notiz["id"])
        ruhe()
        ned = app.rich_note_editor
        assert isinstance(ned, mod.NoteEditor) and ned.ALLOW_TASKS
        assert app.list_frame.winfo_manager() == "", "leere Notiz ohne Punktliste"
        assert ned.winfo_manager() == "pack"
        assert any(tag == "task" for _l, tag in ned.block_choices())
        ned.insert_markdown("## Plan\n\n- [ ] Einkaufen\n- [x] Putzen\n")
        ruhe()
        assert len(notiz.get("items", [])) == 2, "Markdown-Aufgaben sind seit 3.33.15 echte Notizpunkte"
        assert "Einkaufen" in ned.text.get("1.0", "end") and ned.text.tag_ranges("task")
        ned.text.insert("end", "\n- ")
        ned.text.mark_set("insert", "end -1c")
        app.flush_rich_note()
        # Mit dem ersten Punkt erscheint die Liste über dem Text.
        app.entry.delete(0, "end") if hasattr(app, "entry") else None
        notiz_neu = next(e for e in app.lists if e["id"] == notiz["id"])
        notiz_neu.setdefault("items", []).append(app.new_item("Erster Punkt"))
        app.refresh_tree()
        ruhe()
        assert app.list_frame.winfo_manager() == "pack"
        kinder = app.list_frame_outer.inner.pack_slaves()
        assert kinder.index(app.rich_note_editor) < kinder.index(app.list_frame), "Text behält Vorrang"

        # --- R4 c und F1: neue Blockarten, Aufklappen, Gliederung --------------
        seite = app.new_page_from_markdown("# Oben\n\n#### Klein\n\nListe\n\nDanach\n")
        ruhe()
        app.set_active_list(seite["id"])
        ruhe()
        ed = app.rich_note_editor
        text = ed.text
        finde = lambda inhalt: next(i for i in range(1, 30) if text.get(f"{i}.0", f"{i}.end").endswith(inhalt))
        assert "h4" in ed.line_blocks(f"{finde('Klein')}.0"), "#### wird Überschrift 4"
        z = finde("Liste")
        text.mark_set("insert", f"{z}.end")
        ed.set_block("toggle")
        assert text.get(f"{z}.0", f"{z}.end") == "▾ Liste"
        ed.newline()
        text.insert("insert", "Kind eins")
        ed.spread_line_tags()  # beim Tippen erledigt das KeyRelease
        ed.newline()  # normale Zeile im Einzug: bleibt Kind
        text.insert("insert", "Kind zwei")
        ed.spread_line_tags()
        ed.flush()
        kind = finde("Kind eins")
        assert ed.line_level(f"{kind}.0") == 1, ed.line_blocks(f"{kind}.0")
        # Zuklappen per Klick auf den Pfeil, Zustand übersteht Speichern und Laden.
        text.see(f"{z}.0")
        ruhe()
        x, y, _b, h = text.bbox(f"{z}.0")
        ed.click_toggle_arrow(type("E", (), {"x": x + 2, "y": y + h // 2})())
        assert text.get(f"{z}.0", f"{z}.2") == "▸ "
        assert "folded" in text.tag_names(f"{kind}.0")
        assert "folded" not in text.tag_names(f"{finde('Danach')}.0"), "Zeile ohne Einzug gehört nicht dazu"
        dokument = ed.document()
        assert any(s["tag"] == "toggle_closed" for s in dokument["spans"])
        ed.load(dokument)
        assert "folded" in text.tag_names(f"{finde('Kind eins')}.0"), "zu bleibt zu"
        ed.set_toggle_open(f"{z}.0", True)
        assert "folded" not in text.tag_names(f"{finde('Kind eins')}.0")
        # Hinweisblock und Aufklappüberschrift
        dz = finde("Danach")
        text.mark_set("insert", f"{dz}.0")
        ed.set_block("callout")
        assert "callout" in ed.line_blocks(f"{dz}.0")
        text.mark_set("insert", f"{finde('Kind zwei')}.0")
        ed.set_block("toggle_h2")
        bloecke = ed.line_blocks(f"{finde('Kind zwei')}.0")
        assert "toggle" in bloecke and "h2" in bloecke, bloecke
        # Markdown: Pfeile fallen weg, Überschrift 4 bleibt.
        md = mod.glide_page_markdown.page_to_markdown(ed.document())
        assert "#### Klein" in md and "- Liste" in md and "▾" not in md and "▸" not in md, md
        assert "> Danach" in md, md
        # F1: Gliederung im Mehr-Menü springt zur Überschrift, auch aus einer
        # zugeklappten Liste heraus.
        ed.set_toggle_open(f"{z}.0", False)
        eintraege = ed.outline()
        assert [e[1] for e in eintraege] == ["Klein", "Kind zwei"], eintraege
        menues = []
        ed.popup = lambda menu: menues.append(menu)
        ed.show_page_menu()
        mehr = menues.pop()
        stelle = {mehr.entrycget(i, "label"): i for i in range(mehr.index("end") + 1) if mehr.type(i) != "separator"}
        gliederung = root.nametowidget(mehr.entrycget(stelle["Gliederung"], "menu"))
        assert gliederung.index("end") == 1
        gliederung.invoke(1)
        ruhe()
        assert text.index("insert").split(".")[0] == str(finde("Kind zwei"))
        assert "folded" not in text.tag_names("insert"), "Sprung klappt auf"

        # --- R8: Farben nach Bedeutung für jeden Knopf im Quelltext -------------
        import re
        quelle = (REPO / "src/glide/app.pyw").read_text(encoding="utf-8")
        muster = re.compile(r'(?:make_button|_make_dialog_button)\(\s*[^,]+,\s*(?:text=)?("[^"]*")\s*,\s*[^,]*?,'
                            r'\s*(?:color_key=)?["\'](\w+)["\']', re.S)
        leiste = re.compile(r'\(\s*("[^"]+")\s*,\s*[\w\.\(\)\s,=\-:]+?,\s*"(\w+)"\s*,\s*\d+\)')
        gesehen = 0
        for treffer in list(muster.finditer(quelle)) + list(leiste.finditer(quelle)):
            text, wunsch = treffer.group(1).strip('"'), treffer.group(2)
            rolle = app.button_color_key(wunsch, text)
            gesehen += 1
            if rolle == "delete":
                assert re.search(r"[Ll]öschen|[Ee]ntfernen|[Ll]eeren|endgültig", text) and text != "Suche löschen", text
            if rolle == "confirm":
                assert not text.endswith("…") and not re.search(r"öffnen|Öffnen|Pinnwand|^Heute$|Filtern", text), text
            if re.search(r"hinzufügen|^Neue[rs]? |^\+", text):
                assert rolle == "add", (text, rolle)
        assert gesehen > 100, gesehen

        assert not fehler, fehler[:1]
    finally:
        try:
            root.destroy()
        except Exception:
            pass

print("OK: Befunde R1–R5, R7–R11, B3 sowie Blockarten und Gliederung vom 29.09.2026 geprüft.")
