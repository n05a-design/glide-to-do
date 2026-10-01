"""Seitenart „Seite“ und Ordnertypen (26.09.2026).

- Markdown ↔ Seite: Überschriften, Listen, Aufgaben, Zitat, Code, Tabellen,
  Trennlinien, Inline-Formate und Links; der Rundlauf bleibt stabil.
- Eine Seite aus Markdown (der Weg für KI-Berichte): Aufgaben werden echte
  Punkte der Seite – findbar, abhakbar, in „Mein Tag“ einplanbar.
- Im Editor: Titel ändern, Enter setzt Aufgaben fort, leere Aufgabe beendet
  die Liste, gelöschte Aufgabenzeile legt den Punkt in den Papierkorb,
  Rückgängig im Editor holt ihn zurück; Markdown-Kürzel beim Tippen.
- Seitenübersicht: Favoriten und Zuletzt nur mit Seiten; Einstellungen
  bereinigt; Seiten ohne Eingabezeile und ohne Punktliste.
- Ordnertypen Ordner, Bibliothek, Notizbuch; in einer Bibliothek entstehen
  Seiten.
- Speichern und Laden: Seitenart, Text und Aufgabenmarken überstehen einen
  Neustart.
"""
import importlib.machinery
import importlib.util
import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src/glide"))
sys.dont_write_bytecode = True
import page_markdown  # noqa: E402

# --- Markdown ↔ Seite --------------------------------------------------------
BERICHT = """# Quartalsbericht

Einleitung mit **fett**, *kursiv*, ~~alt~~, `code` und [Quelle](https://example.com). 5 * 3 bleibt.

## Ergebnisse

- Umsatz gestiegen
  - Region Nord
- Kosten gesunken

1. Erster Schritt
2. Zweiter Schritt

- [ ] Angebot senden
- [x] Daten prüfen

> Zitat

| Region | Umsatz |
|---|---|
| Nord | 1,2 Mio |

---

```
x = 1
```
"""
dokument = page_markdown.markdown_to_page(BERICHT)
tags = {span["tag"] for span in dokument["spans"]}
for erwartet in ("h1", "h2", "bold", "italic", "strike", "code", "bullet", "indent1", "number", "task",
                 "quote", "table", "divider", "codeblock"):
    assert erwartet in tags, erwartet
assert "5 * 3 bleibt" in dokument["text"], "ungeschlossenes Sternchen bleibt Text"
assert [aufgabe["done"] for aufgabe in dokument["tasks"]] == [False, True]
assert list(dokument["links"].values()) == ["https://example.com"]
zurueck = page_markdown.page_to_markdown(dokument)
nochmal = page_markdown.markdown_to_page(zurueck)
assert nochmal["text"] == dokument["text"], "Rundlauf stabil"
assert page_markdown.looks_like_markdown(BERICHT)
assert not page_markdown.looks_like_markdown("Ein einfacher Satz.")

with tempfile.TemporaryDirectory(prefix="glide-seiten-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_seiten", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1300x860+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *args, **kwargs: None

    def ruhe(runden=6):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    try:
        assert "Seite" in [info["label"] for info in app.LIST_KINDS.values()]
        # --- Seite aus Markdown ----------------------------------------------
        seite = app.new_page_from_markdown(BERICHT)
        ruhe()
        assert seite["title"] == "Quartalsbericht" and seite["list_kind"] == "page"
        assert [(item["text"], item["done"]) for item in seite["items"]] == [("Angebot senden", False),
                                                                            ("Daten prüfen", True)]
        editor = app.rich_note_editor
        assert isinstance(editor, mod.PageEditor)
        assert app.list_frame.winfo_manager() == "" and app.input_frame.winfo_manager() == "", \
            "Seite ohne Punktliste und Eingabezeile"
        assert len(editor.task_boxes()) == 2
        erste = seite["items"][0]["id"]
        # Echte Punkte: auffindbar und in „Mein Tag“ einplanbar.
        assert app.find_item_in_lists(erste)
        app.update_in_progress_item(erste, "planned_date", app.plan_day())
        ruhe()
        assert erste in [eintrag[4]["id"] for eintrag in app.plan_day_entries(apply_filters=False)]
        app.set_active_list(seite["id"])
        ruhe()
        editor = app.rich_note_editor
        # Abhaken über das Kästchen.
        kasten = next(box for box in editor.task_boxes() if box._item_id == erste)
        editor.toggle_task(kasten)
        ruhe()
        assert seite["items"][0]["done"] is True
        assert editor.text.tag_ranges("task_done"), "erledigt durchgestrichen"
        # Titel am Zeilenende verlängern.
        bereich = editor.text.tag_ranges("item:" + erste)
        editor.text.mark_set("insert", f"{bereich[0]} lineend")
        editor.text.insert("insert", " heute")
        editor.flush()
        assert seite["items"][0]["text"] == "Angebot senden heute"
        # Enter setzt die Aufgabe fort; der Punkt entsteht mit dem Text.
        editor.text.mark_set("insert", f"{bereich[0]} lineend")
        editor.newline()
        editor.text.insert("insert", "Neue Aufgabe")
        editor.flush()
        assert "Neue Aufgabe" in [item["text"] for item in seite["items"]]
        # Leere Aufgabe + Enter beendet die Liste.
        editor.newline()
        assert "task" in editor.line_blocks()
        editor.newline()
        assert "task" not in editor.line_blocks()
        # Aufgabenzeile löschen: Punkt in den Papierkorb; Rückgängig holt ihn zurück.
        neue = next(item["id"] for item in seite["items"] if item["text"] == "Neue Aufgabe")
        papierkorb = len(app.trash)
        bereich = editor.text.tag_ranges("item:" + neue)
        editor.text.delete(f"{bereich[0]} linestart", f"{bereich[0]} lineend +1c")
        editor.flush()
        assert neue not in [item["id"] for item in seite["items"]] and len(app.trash) == papierkorb + 1
        editor.undo()
        ruhe()
        assert neue in [item["id"] for item in seite["items"]] and len(app.trash) == papierkorb
        # Markdown-Kürzel: „## “ macht eine Überschrift.
        editor.text.mark_set("insert", "end-1c")
        editor.text.insert("insert", "\n")
        for tag in editor.LINE_BLOCKS:
            editor.text.tag_remove(tag, "insert linestart", "end")
        editor.text.insert("insert", "##")
        editor.markdown_shortcut()
        editor.text.insert("insert", "Anhang")
        editor.flush()
        assert "h2" in editor.line_blocks()
        # Eingefügtes Markdown wird Seiteninhalt, Aufgaben werden Punkte.
        vorher = len(seite["items"])
        editor.insert_markdown("## Nachtrag\n\n- [ ] Rückruf planen")
        assert len(seite["items"]) == vorher + 1
        # Export.
        markdown = app.page_markdown(seite["id"])
        assert markdown.startswith("# Quartalsbericht") and "- [x] Angebot senden heute" in markdown
        assert "## Nachtrag" in markdown and "| Region" in markdown
        # --- Seitenübersicht ---------------------------------------------------
        app.toggle_page_favorite(seite["id"])
        app.set_pages_view()
        ruhe()
        assert app.view_mode == app.PAGES_VIEW and app.get_display_title() == "Seiten"
        # Seit 27.09.2026 ein eigener Bereich „Seiten +“ statt einer Systemzeile.
        assert not app.system_listbox.exists(app.PAGES_ROW_ID)
        assert app.pages_listbox.exists(f"list:{seite['id']}")
        assert not app.sidebar_listbox.exists(f"list:{seite['id']}")
        assert app.pages_heading_frame.cget("bg") == app.theme["selection"]
        assert app.settings["page_favorites"] == [seite["id"]] and app.settings["page_recent"][0] == seite["id"]
        texte = []
        stapel = [app.home_content]
        while stapel:
            widget = stapel.pop()
            stapel.extend(widget.winfo_children())
            if isinstance(widget, mod.RoundedButton):
                texte.append(widget.text)
        assert any("Quartalsbericht" in text for text in texte)
        assert not any("Exposé" in text for text in texte), "nur Seiten, keine Listen"
        bereinigt = app.normalize_personal_settings({"page_favorites": ["a", "a", 3, ""], "page_recent": "x",
                                                     "page_full_width": "ja"})
        assert bereinigt["page_favorites"] == ["a"] and bereinigt["page_recent"] == []
        assert bereinigt["page_full_width"] is False
        # --- Ordnertypen -------------------------------------------------------
        assert [info["label"] for info in app.FOLDER_KINDS.values()] == ["Ordner", "Buch", "Notizbuch"]
        assert app.new_folder_object("x", folder_kind="gibtsnicht")["folder_kind"] == "standard"
        bibliothek = app.new_folder_object("Bücher", folder_kind="library")
        app.folders.append(bibliothek)
        app.update_sidebar_list()
        app.set_active_folder(bibliothek["id"])
        ruhe()
        assert app.entry_placeholder_text == "Neue Seite in diesem Buch"
        app.entry.delete(0, "end")
        app.entry_placeholder_active = False
        app.entry.insert(0, "Der Hobbit")
        app.add_item()
        buch = next(entry for entry in app.lists if entry.get("title") == "Der Hobbit")
        assert buch["list_kind"] == "page" and buch["folder_id"] == bibliothek["id"]
        # --- Speichern und Laden ----------------------------------------------
        app.flush_rich_note()
        app.save_items()
        with open(mod.SAVE_FILE, encoding="utf-8") as datei:
            gespeichert = json.load(datei)
        roh = next(entry for entry in gespeichert["lists"] if entry["id"] == seite["id"])
        assert roh["list_kind"] == "page"
        assert any(span["tag"].startswith("item:") for span in roh["rich_note"]["spans"])
        geladen = app.new_list_object(roh["title"], roh["items"], list_id=roh["id"], list_kind=roh["list_kind"],
                                      rich_note=roh["rich_note"])
        assert geladen["rich_note"] == mod.RichNoteEditor.normalize(roh["rich_note"])
        assert not fehler, fehler[:1]
    finally:
        app.dirty = False
        root.destroy()

print("test_seiten330: OK; Markdown-Rundlauf, Seite aus Markdown mit echten Aufgaben, Editor "
      "(Abhaken, Titel, Enter, Löschen und Rückgängig, Kürzel, Einfügen), Export, Seitenübersicht, "
      "Ordnertypen und Speichern geprüft.")
