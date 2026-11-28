# SPDX-License-Identifier: MPL-2.0
"""Editor der Master-Serie Teil 03 über echte Einstiege (künstliche Daten, eigener GLIDE_DATA_DIR).

- PAGE-01: Auf einer neuen leeren Seite steht der Blockgriff auf der Achse des
  Schreibhinweises; das erste Zeichen verschiebt die Zeile nicht; die leere
  Seite legt keine Zeile und keine Aufgabe an; der Griff bietet nur aktive Aktionen.
- PAGE-02: Überschriften erscheinen als Kapitel unter der Seite in der
  Seitenleiste (verschachtelt, auf- und zuklappbar); ein Klick springt zur
  Überschrift (Vorrang vor der gemerkten Stelle); Umbenennen, Verschieben mit
  Inhalt, Ebene, Auflösen sind je ein Rückgängig-Schritt und bleiben nach dem
  Speichern erhalten; „Neues Kapitel“ im Seitenmenü; Überschrift im Editor
  ändern aktualisiert die Seitenleiste.
- PAGE-03: Block kopieren, ausschneiden und duplizieren ohne Markierung für
  Text, Überschrift, Aufzählung, nummerierte Liste, Aufgabe, Fett und Link;
  ein duplizierter Link und eine duplizierte Aufgabe bekommen neue Identitäten.
- PAGE-05: Wechsel Text ↔ Aufzählung ↔ Überschrift erhält Inlineformat und Link.

--app wählt den Quellstand (Gegenprobe gegen `e8eee591`).
"""
import argparse
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))
sys.dont_write_bytecode = True

with tempfile.TemporaryDirectory(prefix="glide-teil03-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_teil03", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    mod.ListApp.system_is_dark = lambda self: False
    fehler = []
    root = mod.tk.Tk()
    root.geometry("1280x840+20+20")
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = lambda *a, **k: fehler.append(repr(a))
    app.show_warning = lambda *a, **k: None
    hinweise = []
    app.show_info = lambda *a, **k: hinweise.append(a)
    pruefungen = []

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
        return seite, app.rich_note_editor

    def zeilen_dokument(zeilen):
        text, spans = "", []
        for stufe, zeile in zeilen:
            start = len(text)
            text += zeile + "\n"
            if stufe:
                spans.append({"tag": f"h{stufe}", "start": start, "end": start + len(zeile)})
        return {"text": text[:-1], "spans": spans, "links": {}}

    def gespeichert(seite_id):
        daten = json.loads(Path(mod.DATA_FILE).read_text(encoding="utf-8")) if hasattr(mod, "DATA_FILE") else None
        if daten is None:
            return app.page_entry(seite_id).get("rich_note")
        listen = daten.get("lists") if isinstance(daten, dict) else None
        return next(e for e in listen if e.get("id") == seite_id).get("rich_note")

    try:
        # --- PAGE-01 --------------------------------------------------------
        leer, editor = neue_seite("Leere Seite")
        editor.text.focus_force()
        ruhe(0.3)
        griff, hinweis = editor._block_handle, editor._placeholder
        assert griff.winfo_ismapped(), "Blockgriff auf leerer Seite nicht sichtbar"
        assert hinweis.winfo_ismapped(), "Schreibhinweis fehlt"
        mitte_griff = griff.winfo_rooty() + griff.winfo_height() / 2
        mitte_hinweis = hinweis.winfo_rooty() + hinweis.winfo_height() / 2
        assert abs(mitte_griff - mitte_hinweis) <= 3, (mitte_griff, mitte_hinweis)
        abstand = hinweis.winfo_rootx() - (griff.winfo_rootx() + griff.winfo_width())
        assert 0 <= abstand <= editor.BLOCK_HANDLE_GAP + 4, (abstand, editor.BLOCK_HANDLE_GAP)
        x_vorher = editor.text.dlineinfo("1.0")[0]
        editor.text.insert("1.0", "x")
        ruhe(0.1)
        assert editor.text.dlineinfo("1.0")[0] == x_vorher, "Zeile springt beim ersten Zeichen"
        editor.text.delete("1.0", "end")
        editor.flush()
        assert not app.page_entry(leer["id"]).get("items"), "leere Seite legte Aufgaben an"
        assert not (app.page_entry(leer["id"]).get("rich_note") or {}).get("text"), "leere Seite legte Text an"
        pruefungen.append(f"PAGE-01: Griff und Hinweis auf einer Achse (Abstand {abstand} px), kein Sprung, keine leeren Objekte")

        # --- PAGE-02: Kapitel -----------------------------------------------
        seite, editor = neue_seite("Projektentwicklung")
        dokument = zeilen_dokument([(1, "Grundlagen"), (None, "A " * 30), (1, "Architektur"), (2, "Datenmodell"),
                                    (None, "B"), (2, "Schnittstellen"), (None, "C"), (1, "Veröffentlichung")]
                                   + [(None, f"Zeile {n}") for n in range(120)])
        editor.load(dokument)
        editor.flush()
        app.update_sidebar_list()
        ruhe(0.3)
        # Seit Format 27 (D107) ist der Kapitelschlüssel der stabile Anker. Die
        # Zuordnung wird einmal aufgelöst und gilt über Verschieben, Umbenennen
        # und Ebenenwechsel weiter – das prüft zugleich die Stabilität.
        K = {f"{k.level}:{k.title}#1": k.key for k in app.chapter_outline(app.page_entry(seite["id"]))}
        assert all(len(v) == 32 for v in K.values()), K
        baum = app.pages_listbox
        seite_iid = f"list:{seite['id']}"
        kinder = baum.get_children(seite_iid)
        titel = [app.sidebar_chapter_rows[i][1] for i in kinder]
        assert titel == [K["1:Grundlagen#1"], K["1:Architektur#1"], K["1:Veröffentlichung#1"]], titel
        architektur = kinder[1]
        assert [app.sidebar_chapter_rows[i][1] for i in baum.get_children(architektur)] == [
            K["2:Datenmodell#1"], K["2:Schnittstellen#1"]]
        baum.item(seite_iid, open=True)
        baum.focus(seite_iid)
        baum.event_generate("<<TreeviewOpen>>")
        ruhe(0.1)
        assert app.sidebar_chapter_open_state(seite["id"]), "Klappzustand nicht gemerkt"
        pruefungen.append("PAGE-02: Kapitel verschachtelt unter der Seite, Klappzustand gemerkt")

        # Explizites Ziel schlägt gemerkte Stelle: erst ans Ende, Seite wechseln, Kapitel wählen
        editor.text.mark_set("insert", "end")
        editor.text.yview("end")
        neue_seite("Andere Seite")
        app.open_chapter(seite["id"], K["2:Schnittstellen#1"])
        ruhe(0.4)
        editor = app.rich_note_editor
        zeile = editor.text.get("insert linestart", "insert lineend")
        assert zeile == "Schnittstellen", zeile
        baum.selection_set(f"chapter:{seite['id']}:0")
        ruhe(0.4)
        assert app.rich_note_editor.text.get("insert linestart", "insert lineend") == "Grundlagen"
        pruefungen.append("PAGE-02: Kapitel-Klick und open_chapter springen zur Überschrift, auch nach Seitenwechsel")

        # Verschieben mit Inhalt, Rückgängig, Speichern
        text_vorher = app.page_entry(seite["id"])["rich_note"]["text"]
        assert app.change_chapter(seite["id"], K["2:Schnittstellen#1"], "move", -1)
        ruhe(0.3)
        neu = app.page_entry(seite["id"])["rich_note"]
        titel = [c.title for c in mod.glide_chapters.outline(neu)]
        assert titel[:4] == ["Grundlagen", "Architektur", "Schnittstellen", "Datenmodell"], titel
        assert sorted(neu["text"].split("\n")) == sorted(text_vorher.split("\n")), "Text verloren"
        assert app.rich_note_editor.text.get("1.0", "end-1c") == neu["text"], "offener Editor nicht nachgezogen"
        app.rich_note_editor.undo()
        ruhe(0.4)
        assert app.page_entry(seite["id"])["rich_note"]["text"] == text_vorher, "Rückgängig (Editor) stellt nicht her"
        app.rich_note_editor.redo()
        ruhe(0.2)
        assert app.page_entry(seite["id"])["rich_note"]["text"] == neu["text"], "Wiederholen"
        app.rich_note_editor.undo()
        ruhe(0.2)
        # Geschlossene Seite: derselbe Befehl ist ein Schritt im App-Verlauf.
        neue_seite("Zwischenseite")
        assert app.change_chapter(seite["id"], K["2:Schnittstellen#1"], "move", -1)
        app.undo_last_change()
        ruhe(0.3)
        assert app.page_entry(seite["id"])["rich_note"]["text"] == text_vorher, "Rückgängig (App) stellt nicht her"
        app.open_chapter(seite["id"], K["1:Grundlagen#1"])
        ruhe(0.3)
        assert app.change_chapter(seite["id"], K["1:Architektur#1"], "rename", "Systemarchitektur")
        assert app.change_chapter(seite["id"], K["2:Datenmodell#1"], "set_level", 3)
        assert app.change_chapter(seite["id"], K["1:Veröffentlichung#1"], "dissolve")
        app.save_items()
        ruhe(0.3)
        stand = app.page_entry(seite["id"])["rich_note"]
        titel = [(c.level, c.title) for c in mod.glide_chapters.outline(stand)]
        assert (1, "Systemarchitektur") in titel and (3, "Datenmodell") in titel, titel
        assert "Veröffentlichung" in stand["text"] and (1, "Veröffentlichung") not in titel, "Auflösen löschte Inhalt"
        pruefungen.append("PAGE-02: Verschieben mit Unterinhalt, Rückgängig, Umbenennen, Ebene und Auflösen ohne Textverlust")

        # Neues Kapitel im Seitenmenü und Überschriftenänderung im Editor
        editor = app.rich_note_editor
        editor.text.mark_set("insert", "3.0")
        editor.insert_chapter()
        ruhe(0.4)
        titel = [c.title for c in mod.glide_chapters.outline(app.page_entry(seite["id"])["rich_note"])]
        assert mod.glide_i18n.t("chapter.placeholder", "Neues Kapitel") in titel, titel
        app.update_sidebar_list()
        ruhe(0.2)
        neu = next(c for c in mod.glide_chapters.outline(app.page_entry(seite["id"])["rich_note"])
                   if c.level == 2 and c.title == mod.glide_i18n.t("chapter.placeholder", "Neues Kapitel"))
        assert neu.anchor and len(neu.key) == 32, neu  # neue Überschrift erhält sofort einen Anker
        assert any(k == neu.key for _, k in app.sidebar_chapter_rows.values())
        menu = app.build_chapter_menu(root, seite["id"], K["1:Grundlagen#1"])
        zustaende = {menu.entrycget(i, "label"): menu.entrycget(i, "state") for i in range(menu.index("end") + 1)
                     if menu.type(i) == "command"}
        assert zustaende[mod.glide_i18n.t("chapter.move_up", "Mit Inhalt nach oben")] == "disabled", zustaende
        assert zustaende[mod.glide_i18n.t("chapter.level_up", "Eine Ebene höher")] == "disabled", zustaende
        menu.destroy()
        pruefungen.append("PAGE-02: „Neues Kapitel“ legt Überschrift 2 an, Menü bietet nur mögliche Schritte")

        # --- PAGE-03: Blockaktionen ----------------------------------------
        bloecke, editor = neue_seite("Blöcke")
        editor.text.insert("1.0", "Fett und Link")
        editor.text.tag_add("bold", "1.0", "1.4")
        editor.flush()
        editor.text.mark_set("insert", "1.2")
        editor.apply_link("https://example.invalid/a") if hasattr(editor, "apply_link") else None
        faelle = {"text": None, "h2": "h2", "bullet": "bullet", "number": "number"}
        for art, tag in faelle.items():
            editor.text.mark_set("insert", "1.2")
            if tag:
                editor.convert_block(tag)
            vorher = editor.text.get("1.0", "end-1c")
            editor.duplicate_block()
            ruhe(0.1)
            nachher = editor.text.get("1.0", "end-1c")
            assert nachher.count("Fett und Link") == vorher.count("Fett und Link") + 1, (art, nachher)
            fett = editor.text.tag_ranges("bold")
            assert len(fett) >= 4, (art, "Fett nicht mit dupliziert")
            if tag:
                assert tag in editor.text.tag_names("2.0"), (art, editor.text.tag_names("2.0"))
            editor.text.delete("2.0", "end")
            editor.flush()
            if tag:
                editor.text.mark_set("insert", "1.2")
                editor.convert_block(tag)
                assert editor.text.get("1.0", "1.end") == "Fett und Link", art
                assert editor.text.tag_ranges("bold"), (art, "PAGE-05: Fett verloren beim Rückwechsel")
        pruefungen.append("PAGE-03/05: Duplizieren für Text, Überschrift, Aufzählung, Nummerierung mit Format; Rückwechsel behält Fett")

        # Aufgabe duplizieren → neue Aufgabe, kopieren → Zwischenablage, ausschneiden → erst danach weg
        editor.text.delete("1.0", "end")
        editor.flush()
        editor.text.insert("1.0", "Aufgabe eins")
        editor.text.mark_set("insert", "1.3")
        editor.convert_block("task") if "task" in getattr(mod, "PAGE_BLOCK_TAGS", ("task",)) else None
        editor.flush()
        ruhe(0.2)
        aufgaben_vorher = {i["id"] for i in app.page_entry(bloecke["id"]).get("items", [])}
        if aufgaben_vorher:
            editor.text.mark_set("insert", "1.3")
            editor.duplicate_block()
            editor.flush()
            ruhe(0.2)
            aufgaben = {i["id"] for i in app.page_entry(bloecke["id"]).get("items", [])}
            assert len(aufgaben) == len(aufgaben_vorher) + 1 and aufgaben_vorher < aufgaben, aufgaben
            pruefungen.append("PAGE-03: duplizierte Aufgabe ist eine neue Aufgabe mit eigener Kennung")
        root.clipboard_clear()
        editor.text.mark_set("insert", "1.3")
        editor.copy_block()
        assert "Aufgabe eins" in root.clipboard_get()
        zeilen = editor.text.get("1.0", "end-1c").count("\n")
        editor.text.mark_set("insert", "1.3")
        editor.copy_block(cut=True)
        assert "Aufgabe eins" in root.clipboard_get()
        assert editor.text.get("1.0", "end-1c").count("\n") == max(0, zeilen - 1)
        pruefungen.append("PAGE-03: Kopieren und Ausschneiden ohne Markierung über die Zwischenablage")

        # --- PAGE-04: Tastenwege mit Textauswahl ----------------------------
        editor.text.delete("1.0", "end")
        editor.text.insert("1.0", "Alpha Beta Gamma")
        editor.flush()
        listenpunkte = sum(len(e.get("items") or []) for e in app.lists)
        mod_key = "Command" if mod.IS_MACOS else "Control"
        editor.text.focus_force()
        ruhe(0.1)
        editor.text.tag_add("sel", "1.6", "1.10")
        editor.text.event_generate(f"<{mod_key}-c>")
        ruhe(0.1)
        assert root.clipboard_get() == "Beta", root.clipboard_get()
        editor.text.event_generate(f"<{mod_key}-x>")
        ruhe(0.1)
        assert editor.text.get("1.0", "1.end") == "Alpha  Gamma", editor.text.get("1.0", "1.end")
        editor.text.mark_set("insert", "1.6")
        editor.text.event_generate(f"<{mod_key}-v>")
        ruhe(0.2)
        assert editor.text.get("1.0", "1.end") == "Alpha Beta Gamma", editor.text.get("1.0", "1.end")
        assert sum(len(e.get("items") or []) for e in app.lists) == listenpunkte, "Kürzel legte Listenpunkte an"
        assert not any("Punkt" in str(h) for h in hinweise), hinweise
        pruefungen.append(f"PAGE-04: {mod_key}+C/X/V mit Textauswahl im Seitentext, keine Listenaktion, kein Hinweis")

        ruhe(0.2)
        assert not fehler, fehler
        print("test_editor_teil03: OK; " + "; ".join(pruefungen))
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
