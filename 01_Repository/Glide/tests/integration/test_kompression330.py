"""Kompression und Antworten vom 27.09.2026.

- Titel von Listen, Seiten und Ordnern höchstens 40 Zeichen; zu lange Titel
  werden beim Laden gekürzt, vorher sichert Glide die Originaldatei.
- Beschreibung nur unter 50 Zeichen, in der Kennzahlenzeile; keine eigene
  Zeile unter dem Titel.
- Seiten- und Listenbereich mit Klapppfeilen statt Symbolen, kleinerer
  Abstand.
- Bibliothek als Tabelle: Titel, Beschreibung, Farbe, Labels, Aufgaben,
  Erstellt.
- „Tagebuch“ heißt „Notizbuch“.
- Gleicher Innenrand für Notiz, Seite, Zeichnung und Galerie.
- Hinweise: eine Anmeldung je Element, höchstens einer sichtbar.
"""
import glob
import importlib.machinery
import importlib.util
import json
import os
import sys
import tempfile
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
LANG = "2. ✓ Objektdaten aus onOffice ziehen und auf Vollständigkeit prüfen"

with tempfile.TemporaryDirectory(prefix="glide-kompression-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        daten = json.loads(archiv.read("data.json"))
    daten["lists"][1]["title"] = LANG
    Path(ordner, "liste_speicher.json").write_text(json.dumps(daten, ensure_ascii=False), encoding="utf-8")
    loader = importlib.machinery.SourceFileLoader("glide_kompression", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    meldungen = []
    mod.ListApp.show_info = lambda self, *args, **kwargs: meldungen.append(args)
    root = mod.tk.Tk()
    root.geometry("1300x860+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    app.show_warning = app.show_error = lambda *args, **kwargs: fehler.append(args)

    def ruhe(runden=6):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    try:
        # --- Titelgrenze -------------------------------------------------------
        time.sleep(0.8)
        ruhe()
        gekuerzt = app.lists[1]["title"]
        assert len(gekuerzt) == 40 and gekuerzt.endswith("…"), gekuerzt
        assert glob.glob(os.path.join(ordner, "backups", "liste_vor_titelkuerzung_*.json")), "Sicherung vorher"
        sicherung = glob.glob(os.path.join(ordner, "backups", "liste_vor_titelkuerzung_*.json"))[0]
        assert LANG in Path(sicherung).read_text(encoding="utf-8"), "Original in der Sicherung"
        assert any(meldung[0] == "Titel gekürzt" for meldung in meldungen)
        with open(mod.SAVE_FILE, encoding="utf-8") as datei:
            assert json.load(datei)["lists"][1]["title"] == gekuerzt
        assert app.new_folder_object("x" * 60)["title"] == "x" * 39 + "…"
        feld = mod.tk.Entry(root)
        app.limit_title_entry(feld)
        feld.insert(0, "y" * 45)
        assert feld.get() == "", "zu lange Eingabe wird abgewiesen"
        feld.insert(0, "y" * 40)
        assert len(feld.get()) == 40
        feld.destroy()

        # --- Beschreibung in der Kennzahlenzeile -------------------------------
        liste = next(entry for entry in app.lists if len(entry.get("items", [])) > 5)
        liste["note"] = "Kurz und klar"
        app.set_active_list(liste["id"])
        # Sechs Kennzahlen plus Beschreibung brauchen mit den nativen
        # Windows-Schriftmetriken mehr Platz als die bisherige Mac-Breite.
        root.geometry("1600x860+0+30")
        ruhe()
        assert app.header_note_text() == "Kurz und klar"
        assert not hasattr(app, "note_preview_label"), "keine eigene Beschreibungszeile"
        texte = [kind.cget("text") for kind in app.page_chip_row.winfo_children()
                 if isinstance(kind, mod.CanvasLabel)]
        assert any(text.endswith("Kurz und klar") for text in texte), texte
        liste["note"] = "Eine Beschreibung, die deutlich länger als fünfzig Zeichen ist."
        app.update_page_note_preview()
        assert app.header_note_text() == ""

        # --- Klapppfeile und Abstand -------------------------------------------
        assert app.pages_heading_icon.cget("text") == app.SIDEBAR_SECTION_ARROWS[True]
        assert app.sidebar_heading_icon.cget("text") == app.SIDEBAR_SECTION_ARROWS[True]
        app.new_page_from_markdown("# Bericht\n\nText\n")
        ruhe()
        assert app.pages_listbox.winfo_manager() == "pack"
        app.toggle_sidebar_section("pages")
        ruhe()
        assert app.pages_listbox.winfo_manager() == "" and app.pages_heading_icon.cget("text") == "▷"
        app.toggle_sidebar_section("lists")
        ruhe()
        assert app.sidebar_listbox.winfo_manager() == ""
        app.toggle_sidebar_section("lists")
        app.toggle_sidebar_section("pages")
        ruhe()
        assert app.sidebar_listbox.winfo_manager() == "pack" and app.pages_listbox.winfo_manager() == "pack"
        assert int(app.sidebar_title_row.pack_info()["pady"][0]) == app.SIDEBAR_LISTS_GAP
        assert app.SIDEBAR_LISTS_GAP < app.SIDEBAR_SECTION_GAP
        assert app.normalize_personal_settings({"sidebar_sections_closed": ["pages", "lists", "folders"]})[
            "sidebar_sections_closed"] == ["pages", "lists"]

        # --- Bibliothek als Tabelle --------------------------------------------
        bibliothek = app.new_folder_object("Bücher", folder_kind="library")
        app.folders.append(bibliothek)
        seite = app.new_page_from_markdown("# Hobbit\n\n- [ ] Lesen\n- [x] Kaufen\n")
        seite["folder_id"] = bibliothek["id"]
        seite["note"] = "Klassiker"
        app.save_items()
        app.update_sidebar_list()
        app.set_active_folder(bibliothek["id"])
        ruhe()
        assert app.is_library_view()
        assert tuple(app.tree.cget("columns")) == app.LIBRARY_COLUMNS[1:]
        zeile = f"folder-list:{seite['id']}"
        assert app.tree.item(zeile, "text") == "Hobbit"
        werte = dict(zip(app.LIBRARY_COLUMNS[1:], app.tree.item(zeile, "values")))
        assert werte["note"] == "Klassiker" and werte["tasks"] == "1 von 2"
        assert app.tree.heading("#0", "text").startswith("Titel")
        app.sort_library_by("created")
        ruhe()
        assert app._library_sort == ("created", False)
        app.set_active_list(liste["id"])
        ruhe()
        assert "headings" not in str(app.tree.cget("show")), "Listen zeigen wieder den Baum"

        # --- Notizbuch statt Tagebuch ------------------------------------------
        titel = {vorlage["id"]: vorlage["title"] for vorlage in app.templates}
        assert titel.get("journal-note") == "Notizbuch – Tagesnotiz"
        eintrag = app.create_list_from_template("journal-note")
        assert eintrag["title"].startswith("Tagesnotiz · ")
        assert all("Tagebuch" not in abschnitt for abschnitt, _zeilen in app.MANUAL_SECTIONS)

        # --- Innenrand ---------------------------------------------------------
        notiz = app.new_list_object("Notiz", [], list_kind="note")
        app.lists.append(notiz)
        app.set_active_list(notiz["id"])
        ruhe()
        karte = app.list_frame_outer
        links = app.rich_note_editor.winfo_rootx() - karte.winfo_rootx()
        baum = app.tree.winfo_rootx() - karte.winfo_rootx()
        assert links == baum, (links, baum)
        unten = karte.winfo_rooty() + karte.winfo_height() - (
            app.rich_note_editor.winfo_rooty() + app.rich_note_editor.winfo_height())
        assert unten == links, (unten, links)

        # --- Hinweise ----------------------------------------------------------
        for _ in range(4):
            app.sync_detail_button()
            app.apply_reminder_badge()
        knopf = app.detail_button
        assert getattr(knopf, "_glide_tooltip", None) is not None
        app.set_active_list(liste["id"])
        ruhe()
        knopf.event_generate("<Enter>")
        time.sleep(0.7)
        ruhe()
        hinweise = [kind for kind in knopf.winfo_children() if isinstance(kind, mod.tk.Toplevel)]
        assert len(hinweise) <= 1, len(hinweise)
        knopf.event_generate("<ButtonPress-1>")
        ruhe()
        assert not [kind for kind in knopf.winfo_children() if isinstance(kind, mod.tk.Toplevel)]
        assert not fehler, fehler[:1]
    finally:
        app.dirty = False
        root.destroy()

print("test_kompression330: OK; Titelgrenze mit Sicherung, Beschreibung in der Kennzahlenzeile, Klapppfeile, "
      "Bibliothekstabelle, Notizbuch, Innenrand und Hinweise geprüft.")
