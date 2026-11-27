# SPDX-License-Identifier: MPL-2.0
"""Befunde und Editorpaket vom 26./27.11.2026 über echte Einstiege.

- PAGE-04: Strg/Cmd+C, +V und +A im Seiteneditor oder einem anderen Textfeld
  lösen nicht zusätzlich die fensterweiten Listenkürzel aus (vorher:
  „Zuerst einen Punkt auswählen“ bzw. überschriebene Zwischenablage).
- PAGE-05: Die gewählte Blockart erneut wählen macht die Zeile wieder zu Text.
- PAGE-03: „Block kopieren“ ohne Markierung; Einfügen auf einer anderen Seite
  erhält Blockart und Inlineformat.
- PAGE-01: Der Schreibhinweis einer leeren Seite steht auf der Schreibmarke
  (vorher unter Tk 9 um den Innenabstand versetzt).
- Anhang umbenennen: Der Hinweis im Eingabedialog bricht um; der Dialog wird
  nicht bildschirmbreit.
- Dateiablage: Der Drop wird sofort quittiert, die Ablage (die modal nach
  einem Namen fragen kann) folgt im Leerlauf (Hänger unter macOS).

--app wählt den Quellstand (Gegenprobe gegen den Stand vor dem Paket).
Künstliche Daten in einem temporären GLIDE_DATA_DIR.
"""
import argparse
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import time
from types import SimpleNamespace
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))
sys.dont_write_bytecode = True

with tempfile.TemporaryDirectory(prefix="glide-1127-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_befunde_1127", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    mod.ListApp.system_is_dark = lambda self: False
    fehler, warnungen = [], []
    root = mod.tk.Tk()
    root.geometry("1280x840+20+20")
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = lambda *a, **k: fehler.append(repr(a))
    app.show_warning = lambda *a, **k: warnungen.append(a)
    app.show_info = lambda *a, **k: warnungen.append(a)
    pruefungen = []
    mod_key = "Command" if mod.IS_MACOS else "Control"

    def ruhe(sekunden=0.15):
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            root.update()
            time.sleep(0.01)

    def neue_seite(titel):
        seite = app.new_list_object(titel, [], list_kind=app.LIST_KIND_PAGE)
        app.lists.append(seite)
        app.save_items()
        app.set_active_list(seite["id"])
        ruhe(0.4)
        editor = app.rich_note_editor
        assert isinstance(editor, mod.PageEditor), type(editor)
        return seite, editor

    try:
        # --- PAGE-01: Schreibhinweis auf der Schreibmarke -------------------
        seite_a, editor = neue_seite("Seite A")
        editor.text.focus_force()
        ruhe(0.3)
        assert editor._placeholder.winfo_manager() == "place"
        zeile = editor.text.dlineinfo("1.0")
        assert zeile, "erste Zeile nicht dargestellt"
        hinweis_x = editor._placeholder.winfo_rootx() - editor.text.winfo_rootx()
        hinweis_y = editor._placeholder.winfo_rooty() - editor.text.winfo_rooty()
        assert abs(hinweis_x - zeile[0]) <= 2, (hinweis_x, zeile)
        assert abs(hinweis_y - zeile[1]) <= int(float(editor.text.cget("spacing1"))) + 2, (hinweis_y, zeile)
        pruefungen.append(f"PAGE-01: Hinweis bei x={hinweis_x}/y={hinweis_y}, Zeilenanfang {zeile[0]}/{zeile[1]}")

        # --- PAGE-05: Blockart erneut wählen ergibt Text --------------------
        editor.text.insert("1.0", "Fett und Link")
        editor.text.mark_set("insert", "1.3")
        editor.flush()
        for art in ("bullet", "h2", "quote", "number", "toggle", "toggle_h2"):
            editor.convert_block(art)
            assert editor.block_choice_active(art, editor.line_blocks()), (art, editor.line_blocks())
            editor.convert_block(art)
            assert not set(editor.line_blocks()) - set(mod.PAGE_INDENT_TAGS), (art, editor.line_blocks())
            assert editor.text.get("1.0", "1.end") == "Fett und Link", (art, editor.text.get("1.0", "1.end"))
        editor.convert_block("bullet")
        editor.convert_block("h2")
        assert "h2" in editor.line_blocks() and "bullet" not in editor.line_blocks(), "Wechsel bleibt Wechsel"
        editor.convert_block("text")
        assert not editor.line_blocks()
        editor.convert_block("text")
        assert not editor.line_blocks(), "Text erneut bleibt Text"
        menu = editor.build_context_menu()
        stelle = {menu.entrycget(i, "label"): i for i in range(menu.index("end") + 1) if menu.type(i) != "separator"}
        umwandeln = root.nametowidget(menu.entrycget(stelle["Umwandeln in"], "menu"))
        haken = [umwandeln.entrycget(i, "label") for i in range(umwandeln.index("end") + 1)
                 if umwandeln.entrycget(i, "label").startswith("✓")]
        assert len(haken) == 1 and "Text" in haken[0], haken
        pruefungen.append("PAGE-05: sechs Blockarten hin und zurück, Text bleibt, ein Haken")

        # --- PAGE-03: Block kopieren / ausschneiden -------------------------
        assert "Block kopieren" in stelle and "Block ausschneiden" in stelle, list(stelle)
        menu.destroy()
        editor.convert_block("bullet")
        editor.text.tag_add("bold", "1.2", "1.6")
        editor.flush()
        editor.text.mark_set("insert", "1.4")
        assert not editor.has_selection()
        editor.copy_block()
        kopiert = root.clipboard_get()
        assert kopiert == "- **Fett** und Link\n", repr(kopiert)
        seite_b, editor_b = neue_seite("Seite B")
        editor_b.text.insert("1.0", "Davor")
        editor_b.text.mark_set("insert", "1.end")
        editor_b.flush()
        editor_b.paste()
        ruhe(0.2)
        inhalt = editor_b.text.get("1.0", "end-1c").split("\n")
        zeile = next(i for i, z in enumerate(inhalt, start=1) if "Fett und Link" in z)
        assert "bullet" in editor_b.line_blocks(f"{zeile}.0"), editor_b.line_blocks(f"{zeile}.0")
        fett = editor_b.text.tag_ranges("bold")
        assert fett and editor_b.text.get(fett[0], fett[1]) == "Fett", fett
        assert inhalt[0] == "Davor", inhalt
        # Ausschneiden entfernt den Block und lässt den Rest stehen.
        editor_b.text.mark_set("insert", f"{zeile}.3")
        editor_b.copy_block(cut=True)
        assert "Fett und Link" not in editor_b.text.get("1.0", "end"), editor_b.text.get("1.0", "end")
        assert "Davor" in editor_b.text.get("1.0", "end")
        assert root.clipboard_get() == "- **Fett** und Link\n"
        pruefungen.append("PAGE-03: Block ohne Markierung kopiert, auf Seite B als Aufzählung mit Fett eingefügt, "
                          "Ausschneiden entfernt nur den Block")

        # --- PAGE-04: Kürzel im Textfeld lösen keine Listenaktion aus --------
        liste = app.new_list_object("Liste", [])
        app.lists.append(liste)
        app.set_active_list(liste["id"])
        ruhe(0.3)
        app.entry.delete(0, "end")
        app.entry.insert(0, "Punkt eins")
        app.add_item()
        ruhe(0.2)
        punkt = app.items[-1]["id"]
        app.tree.selection_set(punkt)
        notiz = mod.tk.Text(root)
        notiz.place(x=10, y=10, width=200, height=60)
        notiz.insert("1.0", "Markierter Text")
        notiz.tag_add("sel", "1.0", "1.9")
        notiz.focus_force()
        ruhe(0.2)
        root.clipboard_clear()
        root.clipboard_append("vorher")
        warnungen.clear()
        anzahl = len(app.items)
        notiz.event_generate(f"<{mod_key}-c>")
        ruhe(0.1)
        assert root.clipboard_get() == "Markierte", repr(root.clipboard_get())
        assert not warnungen, warnungen
        notiz.event_generate(f"<{mod_key}-v>")
        ruhe(0.1)
        assert len(app.items) == anzahl, "Einfügen im Textfeld legte Listenpunkte an"
        notiz.event_generate(f"<{mod_key}-a>")
        ruhe(0.1)
        assert tuple(app.tree.selection()) == (punkt,), app.tree.selection()
        notiz.destroy()
        # Im Seiteneditor selbst: Markierung kopieren, keine Meldung.
        app.set_active_list(seite_a["id"])
        ruhe(0.3)
        editor = app.rich_note_editor
        editor.text.insert("end", "\nZweite Zeile")
        editor.text.tag_add("sel", "end-1c linestart", "end-1c")
        editor.text.focus_force()
        ruhe(0.2)
        warnungen.clear()
        editor.text.event_generate(f"<{mod_key}-c>")
        ruhe(0.1)
        assert not warnungen, warnungen
        assert root.clipboard_get() == "Zweite Zeile", repr(root.clipboard_get())
        # Außerhalb von Textfeldern bleibt das Listenkürzel unverändert.
        app.set_active_list(liste["id"])
        ruhe(0.3)
        app.tree.selection_set(punkt)
        app.tree.focus_set()
        ruhe(0.1)
        app.tree.event_generate(f"<{mod_key}-c>")
        ruhe(0.1)
        assert "Punkt eins" in root.clipboard_get(), repr(root.clipboard_get())
        pruefungen.append(f"PAGE-04: {mod_key}+C/V/A in Textfeld und Seite ohne Listenaktion, "
                          "in der Liste kopiert das Kürzel weiterhin den Punkt")

        # --- Anhang umbenennen: Hinweis bricht um ----------------------------
        gemessen = {}

        def messen(dialog, *a, **k):
            dialog.update_idletasks()
            gemessen["breite"] = dialog.winfo_reqwidth()
            dialog.destroy()

        with patch.object(app, "run_modal", side_effect=messen):
            app.ask_attachment_name("Bildschirmfoto 2026-11-26 um 20.16.05.png")
        assert 0 < gemessen["breite"] <= 760, gemessen
        pruefungen.append(f"Anhang umbenennen: Dialog {gemessen['breite']} px breit")

        # --- Dateiablage: Drop sofort quittiert, Ablage im Leerlauf ---------
        gebunden, abgelegt = {}, []
        ziel = mod.tk.Frame(root)
        ziel.drop_target_register = lambda *a: None
        ziel.dnd_bind = lambda sequenz, handler: gebunden.__setitem__(sequenz, handler)
        datei = Path(ordner, "bild.png")
        datei.write_bytes(b"x")
        with patch.object(app, "file_drop_support", return_value=True):
            app._dnd_files_type = getattr(app, "_dnd_files_type", "DND_Files")
            assert app.register_file_drop(ziel, lambda pfade, event: abgelegt.append(pfade))
        antwort = gebunden["<<Drop>>"](SimpleNamespace(data="{" + datei.as_posix() + "}", action="copy"))
        assert antwort == "copy" and not abgelegt, "Ablage lief im Drop-Handler"
        ruhe(0.1)
        assert abgelegt == [[datei.as_posix()]], abgelegt
        ziel.destroy()
        pruefungen.append("Dateiablage: Drop quittiert vor der Ablage")

        # --- UX-04: erweiterte Eingabe als Symbolknopf ----------------------
        app.set_active_list(liste["id"])
        ruhe(0.4)
        symbol = app.advanced_icon_button
        assert symbol.winfo_ismapped(), "Symbolknopf fehlt"
        assert app.ICONS["edit"] in str(getattr(symbol, "text", "")), getattr(symbol, "text", None)
        assert app.ICONS["edit"] not in str(getattr(app.add_button, "text", "")), "eindeutiges Symbol"
        assert symbol.winfo_rootx() < app.add_button.winfo_rootx(), "links vom Plus"
        assert symbol.winfo_rootx() > app.entry_border.winfo_rootx(), "rechts vom Eingabefeld"
        assert symbol.command == app.add_item_advanced, "Symbolknopf ruft nicht dieselbe erweiterte Eingabe"
        assert not app.advanced_add_button.winfo_ismapped(), "alter Textknopf bleibt ausgeblendet (U04)"
        app.update_advanced_button_visibility(SimpleNamespace(width=200))
        assert not symbol.winfo_manager(), "bei schmaler Zeile weicht der Symbolknopf"
        app.update_advanced_button_visibility(SimpleNamespace(width=1200))
        assert symbol.winfo_manager() == "pack"
        pruefungen.append("UX-04: Symbolknopf zwischen Eingabe und Plus, ruft die erweiterte Eingabe, weicht bei 200 px")

        # --- EDITOR-01: Adressen werden beim Tippen und Einfügen Links ------
        _s, link_editor = neue_seite("Links")
        text = link_editor.text
        text.focus_force()
        ruhe(0.2)
        text.insert("insert", "Siehe https://example.org/a?b=1.")
        text.event_generate("<KeyPress-space>", keysym="space")
        ruhe(0.1)
        links = [t for t in text.tag_names() if str(t) in link_editor.links]
        assert len(links) == 1, links
        bereich = text.tag_ranges(links[0])
        assert text.get(bereich[0], bereich[1]) == "https://example.org/a?b=1", text.get(bereich[0], bereich[1])
        assert link_editor.links[str(links[0])] == "https://example.org/a?b=1"
        assert text.get("1.0", "1.end").endswith(". "), repr(text.get("1.0", "1.end"))
        gespeichert = app.page_entry(_s["id"]).get("rich_note") or {}
        assert "https://example.org/a?b=1" in (gespeichert.get("links") or {}).values(), gespeichert
        # Rückgängig nimmt zuerst nur den Link zurück, der Text bleibt.
        link_editor.undo()
        link_editor.undo()
        ruhe(0.1)
        assert "https://example.org/a?b=1" in text.get("1.0", "end")
        assert not [t for t in text.tag_names() if str(t) in link_editor.links and text.tag_ranges(t)], "Link blieb"
        # Code bleibt Code; Einfügen erkennt mehrere Adressen.
        text.delete("1.0", "end")
        text.insert("1.0", "x https://code.example")
        text.tag_add("code", "1.0", "1.end")
        text.mark_set("insert", "1.end")
        text.event_generate("<KeyPress-space>", keysym="space")
        assert not [t for t in text.tag_names("1.5") if str(t) in link_editor.links], "Link in Code"
        text.delete("1.0", "end")
        root.clipboard_clear()
        root.clipboard_append("Mail tim@example.com und www.glide.de")
        link_editor.paste_plain()
        ruhe(0.1)
        urls = sorted(link_editor.links[str(t)] for t in text.tag_names() if str(t) in link_editor.links and text.tag_ranges(t))
        assert urls == ["https://www.glide.de", "mailto:tim@example.com"], urls
        # Kontextmenü auf einem Link: öffnen, kopieren, bearbeiten, entfernen.
        text.mark_set("insert", "1.8")
        menu = link_editor.build_context_menu()
        labels = [menu.entrycget(i, "label") for i in range(menu.index("end") + 1) if menu.type(i) != "separator"]
        for erwartet in ("Link öffnen", "Link kopieren", "Link bearbeiten …", "Link entfernen"):
            assert erwartet in labels, labels
        menu.destroy()
        tag = link_editor.link_tag_at()
        link_editor.copy_link(tag)
        assert root.clipboard_get() == "mailto:tim@example.com"
        link_editor.remove_link(tag)
        assert not text.tag_ranges(tag) and "tim@example.com" in text.get("1.0", "end")
        pruefungen.append("EDITOR-01: Adresse vor Leerzeichen zum Link (Punkt bleibt Text), gespeichert, "
                          "Rückgängig nimmt den Link zurück, Code ausgenommen, Einfügen erkennt E-Mail und www, Linkmenü")

        # --- UX-05: Leerzustände als Handlungsaufforderung ------------------
        leer_liste = app.new_list_object("Leer", [])
        app.lists.append(leer_liste)
        app.set_active_list(leer_liste["id"])
        ruhe(0.4)
        assert app.tree.get_children("") == (app.EMPTY_ROW_ID,)
        # Seit dem Merge mit main (WA-52) kommt der Text aus empty_states; der UX-05-Klickweg bleibt.
        assert app.tree.item(app.EMPTY_ROW_ID, "text") == app.empty_state_for("list").text, \
            app.tree.item(app.EMPTY_ROW_ID, "text")
        assert app.empty_inline_action() == app.focus_new_item_entry
        assert not app.empty_action_button.winfo_ismapped() if getattr(app, "empty_action_button", None) else True, \
            "kein zweiter Anlegen-Knopf (U20)"
        leertext = app.empty_text_label
        assert leertext.winfo_ismapped() and str(leertext.cget("cursor")) == "hand2"
        app.tree.focus_force()
        ruhe(0.1)
        leertext.event_generate("<Button-1>", x=5, y=5)
        ruhe(0.2)
        assert app.current_focus_widget() is app.entry, app.current_focus_widget()
        # Leer durch die Suche: Grund nennen, Klick setzt zurück.
        app.entry.delete(0, "end")
        app.entry.insert(0, "Ein Punkt")
        app.add_item()
        ruhe(0.2)
        app.search_placeholder_active = False
        app.search_var.set("gibtesnicht")
        app.on_filter_changed()
        ruhe(0.4)
        assert app.tree.item(app.EMPTY_ROW_ID, "text") == "Keine Treffer für den aktuellen Filter."
        assert app.empty_inline_action() == app.reset_filters_for_empty_state
        app.empty_text_label.event_generate("<Button-1>", x=5, y=5)
        ruhe(0.4)
        assert app.search_var.get() == "" and app.EMPTY_ROW_ID not in app.tree.get_children(""), "Filter blieb"
        # Übersichten: der leere Abschnitt legt direkt an.
        gefunden = {}
        for name, oeffnen, zaehlen in (
                ("Notizen", app.set_notes_view, lambda: len(app.note_entries())),
                ("Zeichnungen", app.set_drawings_view,
                 lambda: sum(1 for e in app.lists if app.is_drawing_list(e) and not app.is_archived_entry(e)))):
            if zaehlen():
                continue
            oeffnen()
            ruhe(0.4)

            def alle(widget):
                for kind in widget.winfo_children():
                    yield kind
                    yield from alle(kind)
            aufforderung = [w for w in alle(app.home_content) if getattr(w, "_inline_command", None)]
            assert len(aufforderung) >= 1, f"{name}: keine Aufforderung"
            label = aufforderung[-1]
            assert str(label.cget("cursor")) == "hand2" and int(label.cget("takefocus")) == 1
            vorher = zaehlen()
            gefunden[name] = label.cget("text")
            label.focus_force()
            ruhe(0.1)
            label.event_generate("<Return>")
            ruhe(0.5)
            assert zaehlen() == vorher + 1, (name, vorher, zaehlen())
        # UX-05 Rest: Ordner, Notizbuch, Label-Untermenü, Startseitenkacheln.
        ordner = app.new_folder_object("Projekte")
        app.folders.append(ordner)
        app.set_active_folder(ordner["id"])
        ruhe(0.4)
        assert app.tree.item(app.EMPTY_ROW_ID, "text").startswith("Eine neue Liste anlegen"), \
            app.tree.item(app.EMPTY_ROW_ID, "text")
        app.tree.focus_force()
        ruhe(0.1)
        app.empty_text_label.event_generate("<Button-1>", x=5, y=5)
        ruhe(0.2)
        assert app.current_focus_widget() is app.entry, "Ordner: Klick führt in die Eingabe"
        buch = app.new_folder_object("Tagebuch", folder_kind="journal")
        app.folders.append(buch)
        app.set_active_folder(buch["id"])
        ruhe(0.4)
        assert app.tree.item(app.EMPTY_ROW_ID, "text") == app.empty_state_for("journal").text
        vorher = sum(1 for e in app.lists if e.get("folder_id") == buch["id"])
        app.empty_text_label.event_generate("<Button-1>", x=5, y=5)
        ruhe(0.5)
        assert sum(1 for e in app.lists if e.get("folder_id") == buch["id"]) == vorher + 1, "kein Notizbucheintrag"
        menue = app._new_themed_popup_menu()
        with patch.object(app, "labels", [label for label in app.labels if app.is_system_label(label)]):
            app._add_page_label_menu(menue, ordner, "folder")
        unter = root.nametowidget(menue.entrycget(menue.index("end"), "menu")) if menue.type("end") == "cascade" else menue
        eintraege = {unter.entrycget(i, "label"): unter.entrycget(i, "state") for i in range((unter.index("end") or 0) + 1)
                     if unter.type(i) == "command"}
        assert eintraege.get("Neues Label anlegen …") == "normal", eintraege
        menue.destroy()
        app.set_home_view()
        ruhe(0.8)
        kacheln = [w for w in alle(app.home_content) if getattr(w, "_inline_command", None)]
        kachel_texte = sorted(str(w.cget("text")) for w in kacheln)
        galerie = next((w for w in kacheln if "Galerie" in str(w.cget("text"))), None)
        if galerie is not None:
            vorher = sum(1 for e in app.lists if app.is_gallery_list(e))
            galerie.focus_force()
            ruhe(0.1)
            galerie.event_generate("<Return>")
            ruhe(0.5)
            assert sum(1 for e in app.lists if app.is_gallery_list(e)) == vorher + 1, "Kachel legte keine Galerie an"
        pruefungen.append("UX-05 Rest: Ordner führt in die Eingabe, Notizbuch legt Eintrag an, Label-Menü aktiv, "
                          f"Startseite {len(kacheln)} Aufforderung(en) ({'; '.join(kachel_texte) or '–'})")
        pruefungen.append("UX-05: leere Liste fordert auf und führt per Klick in die Eingabe, Filter-Leere setzt "
                          f"per Klick zurück, Übersichten legen direkt an ({', '.join(f'{k}: {v}' for k, v in gefunden.items())})")

        # --- UX-03: Verknüpfungen als Chip im Seitenkopf -------------------
        ziel, ziel_editor = neue_seite("Zielseite")
        ruhe(0.3)
        assert app.page_link_count(ziel["id"]) == (0, 0)
        assert not [w for w in alle(app.page_chip_row) if getattr(w, "_link_chip", False)], "Chip ohne Verknüpfungen"
        assert not ziel_editor._mentions_button.winfo_manager(), "Knopf im Seitenfuß"
        quelle, quell_editor = neue_seite("Quelle")
        quell_editor.text.insert("1.0", "Hier steht die Zielseite im Text.")
        quell_editor.flush()
        app.set_active_list(ziel["id"])
        ruhe(0.5)
        assert app.page_link_count(ziel["id"]) == (0, 1), app.page_link_count(ziel["id"])
        chip = next(w for w in alle(app.page_chip_row) if getattr(w, "_link_chip", False))
        assert chip.cget("text").endswith("1 Verknüpfung") and str(chip.cget("cursor")) == "hand2"
        chip.focus_force()
        ruhe(0.1)
        chip.event_generate("<Return>")
        ruhe(0.3)
        editor = app.rich_note_editor
        assert editor._mentions_open
        assert editor._mentions_rows.winfo_rooty() < editor.text.winfo_rooty(), "Bereich nicht unter dem Kopf"
        verknuepfen = [w for w in alle(editor._mentions_rows) if getattr(w, "text", "") == "Verknüpfen"]
        assert len(verknuepfen) == 1
        verknuepfen[0].command()
        ruhe(0.4)
        assert app.page_link_count(ziel["id"]) == (1, 0), "nach dem Verknüpfen neu gezählt"
        app.toggle_page_links()
        ruhe(0.2)
        assert not app.rich_note_editor._mentions_open
        pruefungen.append("UX-03: Chip „1 Verknüpfung“ nur bei Treffern, Enter klappt den Bereich unter dem Kopf auf, "
                          "Verknüpfen zählt neu (Verweis hierher), Seitenfuß ohne Knopf")

        # --- PIXEL-03: Werkzeugspalte und Radierer --------------------------
        app.create_new_drawing()
        ruhe(0.6)
        zeichner = app.drawing_editor
        assert set(zeichner.tool_buttons) == {key for key, _l, _k in zeichner.TOOLS}
        assert len(zeichner.tool_buttons) == 8 and "eraser" in zeichner.tool_buttons
        assert all(knopf.winfo_ismapped() for knopf in zeichner.tool_buttons.values()), "Spalte nicht sichtbar"
        assert not zeichner.tool_choice.winfo_ismapped(), "Werkzeugwahl doppelt in der Leiste"
        spalte_x = zeichner.tool_buttons["brush"].winfo_rootx()
        assert spalte_x < zeichner.canvas.winfo_rootx(), "Spalte links der Fläche"
        assert zeichner.tool_buttons["brush"].active_fill, "aktives Werkzeug markiert"
        zeichner.tool_buttons["fill"].command()
        assert zeichner.tool == "fill" and zeichner.tool_buttons["fill"].active_fill
        assert not zeichner.tool_buttons["brush"].active_fill
        assert app.ICONS["tool_eraser"] in str(zeichner.tool_buttons["eraser"].text)
        assert "Umschalt+E" in zeichner.tool_buttons["eraser"]._glide_tooltip["source"]
        # Pinsel malt, Radierer setzt den durchsichtigen Grund (Index 0) zurück.
        zeichner.set_tool("brush")
        zeichner.color = "#FF0000"
        zeichner.cursor = (3, 3)
        zeichner.apply_at_cursor()
        assert zeichner.model.color_index_at(3, 3) != 0
        zuletzt = list(app.drawing_tool_settings()["recent_colors"])
        zeichner.canvas.focus_force()
        ruhe(0.1)
        zeichner.canvas.event_generate("<KeyPress>", keysym="E")
        ruhe(0.1)
        assert zeichner.tool == "eraser", zeichner.tool
        assert zeichner.tool_buttons["eraser"].active_fill
        zeichner.apply_at_cursor()
        assert zeichner.model.color_index_at(3, 3) == 0, "Radierer setzt nicht den Grund"
        assert list(app.drawing_tool_settings()["recent_colors"]) == zuletzt, "Radieren änderte „Zuletzt“"
        zeichner.canvas.event_generate("<KeyPress>", keysym="e")
        ruhe(0.1)
        assert zeichner.tool == "ellipse", "e bleibt die Ellipse"
        zeichner.undo()
        assert zeichner.model.color_index_at(3, 3) != 0, "Rückgängig nimmt das Radieren zurück"
        # PIXEL-02: Spiegeln/Drehen (ganze Zeichnung und Auswahl), Rückgängig, Schachbrett nur Anzeige.
        groesse = zeichner.model.width
        zeichner.selection = None
        zeichner.set_tool("brush")
        zeichner.cursor = (0, 0)
        zeichner.apply_at_cursor()
        rot = zeichner.model.color_index_at(0, 0)
        zeichner.canvas.event_generate("<KeyPress>", keysym="h")
        assert zeichner.model.color_index_at(groesse - 1, 0) == rot and zeichner.model.color_index_at(0, 0) == 0
        zeichner.undo()
        assert zeichner.model.color_index_at(0, 0) == rot
        zeichner.canvas.event_generate("<KeyPress>", keysym="t")
        assert zeichner.model.color_index_at(groesse - 1, 0) == rot, "90° rechts: oben links → oben rechts"
        zeichner.undo()
        zeichner.selection = (0, 0, 3, 1)
        zeichner.transform("rotate_cw")
        assert zeichner.selection == (1, 0, 2, 3), zeichner.selection
        zeichner.undo()
        zellen = bytes(zeichner.model.cells)
        zeichner.toggle_checker()
        assert zeichner._cell_color(groesse * 2 + 1) in zeichner.CHECKER_COLORS and bytes(zeichner.model.cells) == zellen
        zeichner.toggle_checker()
        pruefungen.append("PIXEL-02: H spiegelt, T dreht, Auswahl dreht um ihre Mitte, Rückgängig, Schachbrett ändert keine Zelle")
        pruefungen.append("PIXEL-03: 8 Werkzeuge als Spalte links der Fläche, aktives markiert, Leiste ohne "
                          "Werkzeugwahl; Radierer (Umschalt+E) setzt den Grund, ohne „Zuletzt“, rückgängig machbar")

        # --- PAGE-06: zurück an die zuletzt gesehene Stelle ----------------
        lang, lang_editor = neue_seite("Lange Seite")
        lang_editor.text.insert("1.0", "\n".join(f"Zeile {n}" for n in range(1, 301)))
        lang_editor.flush()
        ruhe(0.2)
        lang_editor.text.yview("200.0")
        lang_editor.text.mark_set("insert", "205.3")
        ruhe(0.2)
        oben_vorher = int(lang_editor.text.index("@0,0").split(".")[0])
        assert oben_vorher >= 190, oben_vorher
        viele = app.new_list_object("Viele Punkte", [])
        app.lists.append(viele)
        app.set_active_list(viele["id"])
        ruhe(0.3)
        for n in range(1, 151):
            app.entry.delete(0, "end")
            app.entry.insert(0, f"Punkt {n}")
            app.add_item()
        ruhe(0.3)
        app.tree.yview_moveto(0.5)
        ruhe(0.2)
        liste_oben = app.tree.identify_row(8)
        assert liste_oben, "keine sichtbare Zeile"
        app.set_active_list(lang["id"])
        ruhe(0.4)
        editor = app.rich_note_editor
        oben = int(editor.text.index("@0,0").split(".")[0])
        assert abs(oben - oben_vorher) <= 1, (oben, oben_vorher)
        assert editor.text.index("insert") == "205.3", editor.text.index("insert")
        app.set_active_list(viele["id"])
        ruhe(0.4)
        assert app.tree.identify_row(8) == liste_oben, (app.tree.identify_row(8), liste_oben)
        # Gekürzter Inhalt: die nächste mögliche Stelle statt eines Fehlers.
        app.set_active_list(lang["id"])
        ruhe(0.3)
        app.rich_note_editor.text.delete("50.0", "end")
        app.rich_note_editor.flush()
        app.set_active_list(viele["id"])
        ruhe(0.3)
        app.set_active_list(lang["id"])
        ruhe(0.3)
        assert app.rich_note_editor.text.compare("insert", "<=", "end"), "Schreibmarke außerhalb"
        pruefungen.append(f"PAGE-06: Seite zurück auf Zeile {oben} samt Schreibmarke, Liste auf Zeile {liste_oben}, "
                          "gekürzter Inhalt ohne Fehler")

        ruhe(0.2)
        assert not fehler, fehler
        print("test_befunde_1127: OK; " + "; ".join(pruefungen))
    finally:
        try:
            app.cancel_pending_callbacks()
            getattr(app, "finish_recovery_session", lambda: None)()
            app.release_data_lock()
        except Exception:
            pass
        try:
            root.destroy()
        except mod.tk.TclError:
            pass
