"""Bilder in Seiten, Tk-9-Vorschauen, Systemmitteilungen, „/“-Befehle,
wiederkehrende Checklisten und Tempo (27.09.2026).

- Vorschaumodul: rationale Skalierung, Formate, Größe, SVG unter Tk 9,
  Windows-Befehl mit sicheren Anführungszeichen.
- Seitendokument: `images` wird geprüft, verwaist Verweise fallen weg, Seiten
  ohne Bilder bleiben bytegleich.
- Seitenbilder: einfügen, links/rechts umfließen, mittig, Breite ziehen,
  verschieben, entfernen, Rückgängig, Neustart, Markdown mit Bildordner,
  `.glidepage` mit neuen Anhangskennungen.
- Systemmitteilung: Sammeltext, Schalter aus = keine Mitteilung, eine
  Mitteilung je Prüflauf.
- „/“-Befehle: Titel und Felder, Vorschlagszeile, Tab ergänzt.
- Wiederkehrende Checkliste: öffnet sich nach dem letzten Haken wieder,
  Rückgängig, bleibt nach dem Laden erhalten.
- Tempo: gleiche Bytes beim Schreiben, schnelle leere Verlaufswerte.
- Start: Fenster sofort in gespeicherter Größe.
- Ziehen aus Finder/Explorer: tkdnd lädt (wenn für das System vorhanden).
"""
import importlib.machinery
import importlib.util
import io
import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src/glide"))
sys.dont_write_bytecode = True
import image_preview  # noqa: E402
import page_markdown  # noqa: E402

# --- Vorschaumodul ohne Tk ---------------------------------------------------
assert image_preview.rational_factor(1.0) == (1, 1)
assert image_preview.rational_factor(2.6) == (2, 1)
zoom, teiler = image_preview.rational_factor(0.47)
assert zoom / teiler <= 0.47 and zoom / teiler > 0.4
assert image_preview.is_image_name("Foto.JPEG") and image_preview.is_image_name("x.svg")
assert not image_preview.is_image_name("bericht.pdf")
befehl = image_preview.windows_convert_command("C:\\Bilder\\O'Neil.jpg", "C:\\t.png")
assert befehl[0] == "powershell" and "'C:\\Bilder\\O''Neil.jpg'" in befehl[-1], "Anführungszeichen verdoppelt"

with tempfile.TemporaryDirectory(prefix="glide-bilder-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_bilder", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)

    # --- Seitendokument ------------------------------------------------------
    norm = mod.RichNoteEditor.normalize
    ohne = norm({"text": "Hallo", "spans": [], "links": {}})
    assert "images" not in ohne, "Seiten ohne Bilder bleiben unverändert"
    doc = norm({"text": "\ufffc\nText", "spans": [{"tag": "img:0123456789abcdef", "start": 0, "end": 1}],
                "links": {}, "images": {
                    "img:0123456789abcdef": {"attachment": "abc", "mode": "quer", "width": 99999},
                    "img:fedcba9876543210": {"attachment": "def", "mode": "left", "width": 200},
                    "img:kaputt": {"attachment": "x"}}})
    assert list(doc["images"]) == ["img:0123456789abcdef"], "nur verwendete, gültige Bilder"
    assert doc["images"]["img:0123456789abcdef"] == {"attachment": "abc", "mode": "center", "width": 4000}
    try:
        norm({"text": "", "spans": [], "images": []})
        raise AssertionError("images muss ein Objekt sein")
    except ValueError:
        pass
    # Markdown: Bild als Zeile, Rest der Zeile bleibt.
    md = page_markdown.page_to_markdown(doc, image_source=lambda info: ("Blume", "Bilder/blume.png"))
    assert "![Blume](Bilder/blume.png)" in md and "Text" in md

    root = mod.tk.Tk()
    root.geometry("1280x860+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    meldungen = []
    app.show_info = app.show_warning = app.show_error = lambda *args, **kwargs: meldungen.append(args)

    def ruhe(runden=6):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    try:
        # --- Testbilder ------------------------------------------------------
        png = Path(ordner, "quadrat.png")
        bild = mod.tk.PhotoImage(master=root, width=120, height=80)
        bild.put("#3366CC", to=(0, 0, 120, 80))
        bild.write(str(png), format="png")
        breit = Path(ordner, "breit.png")
        bild2 = mod.tk.PhotoImage(master=root, width=1600, height=400)
        bild2.put("#CC6633", to=(0, 0, 1600, 400))
        bild2.write(str(breit), format="png")
        vorschau = app.previews
        assert vorschau.natural_size(root, str(png)) == (120, 80)
        klein = vorschau.image(root, str(png), width=60)
        assert (klein.width(), klein.height()) == (60, 40)
        assert vorschau.image(root, str(png), width=60) is klein, "Zwischenspeicher"
        kachel = vorschau.image(root, str(breit), box=200)
        assert kachel.width() <= 200 and kachel.height() <= 200
        if image_preview.has_svg(root):
            svg = Path(ordner, "form.svg")
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">'
                           '<rect width="100" height="50" fill="red"/></svg>', encoding="utf-8")
            assert vorschau.image(root, str(svg), width=300).width() == 300, "SVG unter Tk 9"
        assert vorschau.image(root, str(Path(ordner, "fehlt.png")), width=10) is None

        # --- Seitenbilder -----------------------------------------------------
        text = "# Bilder\n\n" + "\n\n".join(f"Absatz {i}. " + "Lorem ipsum dolor sit amet. " * 12 for i in range(6))
        seite = app.new_page_from_markdown(text)
        ruhe()
        editor = app.rich_note_editor
        assert isinstance(editor, mod.PageEditor)
        neu = editor.insert_images([str(png)], "3.0")
        ruhe()
        assert len(neu) == 1
        key = neu[0]
        info = seite["rich_note"]["images"][key]
        assert info["mode"] == "left", "kleines Bild steht links im Text"
        assert any(anhang["id"] == info["attachment"] for anhang in seite["attachments"])
        anker = editor.text.index(editor.text.tag_ranges(key)[0])
        assert anker.endswith(".0"), "Anker am Zeilenanfang"
        assert "imganchor" in editor.text.tag_names(anker), "Anker unsichtbar"
        editor.layout_images()
        ruhe()
        fluss = "imgflow:" + key[4:]
        assert editor.text.tag_ranges(fluss), "Textzeilen neben dem Bild eingerückt"
        assert int(editor.text.tag_cget(fluss, "lmargin2")) >= 120
        view = editor._image_views[key]
        assert view.winfo_ismapped() and view._size == (120, 80)
        # Bild steht links an der Spalte, auf Höhe seiner Zeile.
        links, spalte = editor.column_bounds()
        assert abs(view.winfo_x() - links) <= 2, (view.winfo_x(), links)
        assert abs(view.winfo_y() - (editor.line_top(anker) + 2)) <= 2

        # Rechts umfließen, dann mittig.
        editor.set_image_mode(key, "right")
        ruhe()
        assert int(editor.text.tag_cget(fluss, "rmargin")) >= 120
        assert abs(view.winfo_x() + 120 - (links + spalte)) <= 2
        editor.set_image_mode(key, "center")
        ruhe()
        assert editor.text.tag_ranges("imgpad:" + key[4:]) and not editor.text.tag_ranges(fluss)
        assert seite["rich_note"]["images"][key]["mode"] == "center"

        # Breite ziehen: Griff unten rechts, 60 Pixel nach rechts (mittig: doppelt).
        editor.select_image(key)
        ruhe()
        breite, hoehe = view._size
        druck = SimpleNamespace(x=breite - 4, y=hoehe - 4, x_root=500, y_root=500)
        editor.image_press(key, druck)
        editor.image_motion(key, SimpleNamespace(x=0, y=0, x_root=530, y_root=500))
        editor.image_release(key, SimpleNamespace(x=0, y=0, x_root=530, y_root=500))
        ruhe()
        assert seite["rich_note"]["images"][key]["width"] == 180, seite["rich_note"]["images"][key]
        assert view._size == (180, 120), "Seitenverhältnis bleibt"

        # Verschieben per Ziehen an den Anfang von Absatz 4, links in der Spalte.
        ziel_zeile = next(i for i in range(1, 40)
                          if editor.text.get(f"{i}.0", f"{i}.0 lineend").startswith("Absatz 4"))
        editor.text.see(f"{ziel_zeile}.0")
        ruhe()
        oben = editor.line_top(f"{ziel_zeile}.0")
        editor.image_press(key, SimpleNamespace(x=20, y=20, x_root=300, y_root=300))
        editor.image_motion(key, SimpleNamespace(x=0, y=0, x_root=editor.text.winfo_rootx() + links + 10,
                                                 y_root=editor.text.winfo_rooty() + oben + 4))
        editor.image_release(key, SimpleNamespace(x=0, y=0, x_root=0, y_root=0))
        ruhe()
        anker = editor.text.index(editor.text.tag_ranges(key)[0])
        assert editor.text.get(f"{anker} +2c", f"{anker} +2c lineend").startswith("Absatz 4"), \
            editor.text.get(anker, f"{anker} +40c")
        assert seite["rich_note"]["images"][key]["mode"] == "left"

        # Zweites Bild, großes: füllt die Spalte.
        zweites = editor.insert_images([str(breit)], "end")[0]
        ruhe()
        assert seite["rich_note"]["images"][zweites]["mode"] == "center"
        assert editor._image_views[zweites]._size[0] <= spalte

        # Neu laden (Seite wechseln und zurück): alles bleibt.
        andere = app.new_page_from_markdown("# Andere\n\nText")
        ruhe()
        app.set_active_list(seite["id"])
        ruhe()
        editor = app.rich_note_editor
        assert set(editor.image_keys()) == {key, zweites}

        # Markdown-Export mit Bildordner.
        ziel = Path(ordner, "export", "seite.md")
        ziel.parent.mkdir()
        mod.filedialog.asksaveasfilename = lambda **kwargs: str(ziel)
        app.export_page_markdown(seite["id"])
        inhalt = ziel.read_text(encoding="utf-8")
        assert "](seite%20Bilder/quadrat.png)" in inhalt, inhalt
        assert Path(ordner, "export", "seite Bilder", "quadrat.png").is_file()

        # Entfernen und Rückgängig im Editor.
        editor.remove_image(key)
        ruhe()
        assert key not in (seite["rich_note"].get("images") or {})
        editor.undo()
        ruhe()
        assert key in seite["rich_note"]["images"], "Rückgängig holt das Bild zurück"

        # .glidepage: neue Anhangskennungen, Bilder zeigen weiter auf ihren Anhang.
        paket = Path(ordner, "seite.glidepage")
        mod.filedialog.asksaveasfilename = lambda **kwargs: str(paket)
        app.export_glide_pages([seite["id"]], [])
        vorher = {entry["id"] for entry in app.lists}
        app.import_glide_pages(str(paket))
        ruhe()
        kopie = next(entry for entry in app.lists if entry["id"] not in vorher)
        kopie_bilder = kopie["rich_note"]["images"]
        kopie_anhaenge = {anhang["id"] for anhang in kopie["attachments"]}
        assert kopie_bilder and all(info["attachment"] in kopie_anhaenge for info in kopie_bilder.values())
        assert not kopie_anhaenge & {anhang["id"] for anhang in seite["attachments"]}, "neue Kennungen"

        # Ziehen aus Finder/Explorer: Nur Bilder werden eingesetzt.
        app.set_active_list(seite["id"])
        ruhe()
        editor = app.rich_note_editor
        anzahl = len(editor.images)
        editor.drop_files([str(Path(ordner, "liste_speicher.json")), str(png)], None)
        ruhe()
        assert len(editor.images) == anzahl + 1
        if sys.platform == "darwin":
            assert app.file_drop_support(), getattr(app, "_file_drop_error", "")

        # --- Galerie über das neue Vorschaumodul -----------------------------
        galerie = app.new_list_object("Fotos", [], list_kind="gallery")
        app.lists.append(galerie)
        app.save_items()
        app.set_active_list(galerie["id"])
        ruhe()
        app.add_gallery_images(galerie["id"], [str(png), str(Path(ordner, "fehlt.jpg"))])
        ruhe(10)
        assert len(galerie["attachments"]) == 1, "nicht vorhandene Datei übersprungen"
        ansicht = app.gallery_view
        assert ansicht.thumbnail(galerie["attachments"][0], 100) is not None

        # --- Systemmitteilung --------------------------------------------------
        assert app.settings.get("system_notifications") is False, "standardmäßig aus"
        assert app.reminder_notification_text(["A"]) == ("Glide – Erinnerung", "A")
        titel, text = app.reminder_notification_text(["A", "B", "C", "D", "E"])
        assert titel == "Glide – 5 Erinnerungen fällig" and text.endswith("und 2 weitere")
        gesendet = []
        app._system_notification_backend = lambda t, m: gesendet.append((t, m))
        assert app.send_reminder_notification(["A"]) is False and not gesendet, "aus heißt aus"
        app.settings["system_notifications"] = True
        assert app.send_reminder_notification(["A", "B"]) is True
        assert gesendet == [("Glide – 2 Erinnerungen fällig", "A · B")]
        assert isinstance(mod.ListApp.tk_has_sysnotify(root), bool)
        # Normierung: fehlender Wert = aus, Unsinn = aus.
        assert mod.ListApp.normalize_personal_settings({"system_notifications": "ja"})["system_notifications"] is False

        # --- „/“-Befehle --------------------------------------------------------
        liste = app.new_list_object("Einkauf", [])
        app.lists.append(liste)
        app.save_items()
        app.set_active_list(liste["id"])
        ruhe()
        app.clear_entry_text()
        app.entry.insert(0, "Milch /morgen /wichtig")
        app.entry.icursor("end")
        app.entry_placeholder_active = False
        app.update_slash_hint()
        ruhe()
        assert app._slash_hint.winfo_ismapped() and "fällig morgen" in app._slash_hint.cget("text"), \
            (app.view_mode, getattr(app, "_slash_hint", None) and app._slash_hint.cget("text"))
        app.add_item()
        ruhe()
        punkt = liste["items"][-1]
        assert punkt["text"] == "Milch" and punkt["importance"] == 3 and punkt["due"], punkt
        app.entry.insert(0, "Brot /mo")
        app.entry.icursor("end")
        assert app.complete_slash_command() == "break"
        assert app.entry.get() == "Brot /morgen ", app.entry.get()
        app.clear_entry_text()
        app.hide_slash_hint()

        # --- Wiederkehrende Checkliste -----------------------------------------
        liste["items"] = [app.new_item("Pass"), app.new_item("Ladekabel")]
        app.save_items()
        app.refresh_tree()
        assert app.set_recurring_checklist(liste["id"], True)
        assert liste["recurring_checklist"] is True
        app.CHECKLIST_RESET_DELAY_MS = 1
        for punkt in liste["items"]:
            app.toggle_item_done_anywhere(punkt["id"])
        ruhe(10)
        root.after(20)
        ruhe(10)
        assert not any(punkt["done"] for punkt in liste["items"]), "wieder offen"
        app.undo_last_change()
        ruhe()
        liste = next(entry for entry in app.lists if entry["id"] == liste["id"])
        assert all(punkt["done"] for punkt in liste["items"]), "Rückgängig zeigt den erledigten Stand"
        gespeichert = json.loads(Path(ordner, "liste_speicher.json").read_text(encoding="utf-8"))
        eintrag = next(entry for entry in gespeichert["lists"] if entry["id"] == liste["id"])
        assert eintrag.get("recurring_checklist") is True
        menue = app.build_list_menu(liste["id"])
        beschriftungen = [menue.entrycget(i, "label") for i in range(menue.index("end") + 1)
                          if menue.type(i) == "command"]
        assert "✓ Wiederkehrende Checkliste" in beschriftungen and "Alle Punkte wieder öffnen" in beschriftungen
        normiert = app.new_list_object("Zeichnung", list_kind="drawing", recurring_checklist=True)
        assert "recurring_checklist" not in normiert, "nur Aufgabenlisten"

        # --- Tempo ---------------------------------------------------------------
        nutzlast = {"a": [1, {"ü": "ß"}], "b": None}
        datei = Path(ordner, "probe.json")
        app.write_json_atomic(str(datei), nutzlast)
        puffer = io.StringIO()
        json.dump(nutzlast, puffer, ensure_ascii=False, indent=4)
        assert datei.read_text(encoding="utf-8") == puffer.getvalue(), "dieselben Bytes wie vorher"
        assert mod.ListApp.history_value({"links": []}, "links") == json.dumps([])
        assert mod.ListApp.history_value({"repeat": {}}, "repeat") == json.dumps({})

        # --- Start: Fenster sofort --------------------------------------------------
        Path(mod.BASE_DIR, "window.conf").write_text("1000x720+40+50", encoding="utf-8")
        zweites_fenster = mod.tk.Toplevel(root)
        platzhalter = mod.show_start_window(zweites_fenster)
        assert zweites_fenster.geometry().startswith("1000x720"), zweites_fenster.geometry()
        platzhalter.destroy()
        zweites_fenster.destroy()

        # --- Rundgang (Probedaten 27.09.2026): Liste, Notiz, Seite, Zeichnung ----
        vorher = {entry["id"] for entry in app.lists}
        app.import_full_backup(additive=True, path=str(REPO / "tests/fixtures/beispiele/glide_rundgang.glidebackup"),
                               show_success=False, confirm=False)
        ruhe()
        rundgang = [entry for entry in app.lists if entry["id"] not in vorher]
        arten = sorted(entry.get("list_kind") for entry in rundgang)
        assert arten == ["drawing", "note", "page", "tasks"], arten
        rg_seite = next(entry for entry in rundgang if entry.get("list_kind") == "page")
        rg_bilder = rg_seite["rich_note"]["images"]
        assert len(rg_bilder) == 5
        for info in rg_bilder.values():
            anhang = app.page_attachment(rg_seite["id"], info["attachment"])
            assert anhang and os.path.isfile(app.resolve_attachment_path(anhang)), info

        assert not fehler, fehler
    finally:
        try:
            root.destroy()
        except Exception:
            pass

print("test_bilder330: ok")
