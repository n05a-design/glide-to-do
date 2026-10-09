"""Paket Wissen und Seiten 3.34.0: B4, G14h, D-03, H-02r und N08 über echte Einstiege.

B4: Bilder auf aufeinanderfolgenden Absätzen überlappen in keiner Umflusskombination;
„Drucken und PDF …“ aus dem Seitenmenü bettet die Bilder als Daten-URL ein;
„Markdown kopieren“ verweist auf die gespeicherten Bilddateien, „Als Markdown
speichern …“ legt sie daneben, und der Rückweg (Zwischenablage bzw. „Markdown als
Seite öffnen“) macht daraus wieder Seitenbilder.
G14h: Ein Inhaltstreffer aus der Suche markiert nach Enter alle Fundstellen mit
Umlautgleichheit; Tippen oder Esc hebt die Markierung auf, gespeichert wird sie nie.
D-03: In einem gespeicherten Filter erklärt „Warum steht das hier?“ jede Bedingung,
der Kopf nennt „Ausgeblendet: N“, „Filter erklären …“ die Gründe; Daten bleiben gleich.
H-02r: Alt+Pfeile in den Bereichsbäumen ordnen um, rücken ein und aus, melden Ziel und
Wirkung mit Rückgängig und überstehen einen Neustart; im Spaltenboard nennt Alt+→
die Zielspalte.
N08: Mit erzwungenem Linux-Weg wandelt `djpeg` JPEG für Vorschau und Referenz; ohne
Werkzeug bleibt der Platzhalter mit verständlicher Meldung.

--app wählt den Quellstand; mit der unveränderten 3.33.21 muss die Suite rot sein
(Gegenprobe). Künstliche Daten in einem temporären GLIDE_DATA_DIR.
"""
import argparse
import copy
import hashlib
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def eintraege(menu):
    ende = menu.index("end")
    return {menu.entrycget(i, "label"): i for i in range((ende if ende is not None else -1) + 1)
            if menu.type(i) in ("command", "cascade")}


def schnitt(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def sha(pfad):
    return hashlib.sha256(Path(pfad).read_bytes()).hexdigest()


with tempfile.TemporaryDirectory(prefix="glide-wissen-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_wissen_test", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    fehler, toasts, infos = [], [], []
    root = app = None
    pruefungen = []

    def ruhe(sekunden=0.15):
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            root.update()
            time.sleep(0.01)

    def starten():
        global root, app
        root = mod.tk.Tk()
        root.geometry("1280x840+20+20")
        root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
        app = mod.ListApp(root)
        app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
        app.show_info = lambda *a, **k: infos.append(a)
        original = app.show_undo_toast
        app.show_undo_toast = lambda text, restore=None: (toasts.append(text), original(text, restore))[1]
        ruhe()

    def beenden():
        app.cancel_pending_callbacks()
        app.release_data_lock()
        for job in root.tk.call("after", "info"):
            root.tk.call("after", "cancel", job)
        root.destroy()

    starten()
    try:
        # --- Testbilder ---------------------------------------------------------
        bilder = []
        for n, (b, h, farbe) in enumerate(((220, 160, "#3366CC"), (200, 140, "#CC6633"), (240, 120, "#33AA66"))):
            bild = mod.tk.PhotoImage(master=root, width=b, height=h)
            bild.put(farbe, to=(0, 0, b, h))
            pfad = os.path.join(ordner, f"Bild {n}.png")
            bild.write(pfad, format="png")
            bilder.append(pfad)

        # --- B4 (1): keine Überlappung ------------------------------------------
        seite = app.new_page_from_markdown("# Bildseite\n\n" + "\n\n".join(
            f"Absatz {i}. Ein kurzer Satz." for i in range(30)))
        ruhe(0.3)
        editor = app.rich_note_editor
        assert isinstance(editor, mod.PageEditor) and editor.entry_id == seite["id"]
        for pfad, zeile in zip(bilder, ("3.0", "5.0", "7.0")):
            editor.insert_images([pfad], zeile)
        ruhe(0.4)
        schluessel = editor.image_keys()
        assert len(schluessel) == 3, schluessel
        kombinationen = [("left", "left", "left"), ("left", "right", "center"), ("right", "right", "left"),
                         ("center", "left", "right"), ("right", "left", "left")]
        for kombination in kombinationen:
            for key, modus in zip(schluessel, kombination):
                if editor.images[key]["mode"] != modus:
                    editor.set_image_mode(key, modus)
            ruhe(0.2)
            editor.layout_images()
            ruhe(0.2)
            rechtecke = {}
            for key in schluessel:
                ansicht = editor._image_views[key]
                assert ansicht.winfo_ismapped(), (kombination, key)
                rechtecke[key] = (ansicht.winfo_x(), ansicht.winfo_y(), ansicht.winfo_x() + ansicht.winfo_width(),
                                  ansicht.winfo_y() + ansicht.winfo_height())
            paare = [(a, b) for i, a in enumerate(schluessel) for b in schluessel[i + 1:]
                     if schnitt(rechtecke[a], rechtecke[b])]
            assert not paare, (kombination, rechtecke)
        gespeichert = mod.RichNoteEditor.normalize(app.page_entry(seite["id"])["rich_note"])
        assert not any(span["tag"].startswith("imgpush:") for span in gespeichert["spans"])
        pruefungen.append(f"B4: drei Bilder in {len(kombinationen)} Umflusskombinationen ohne Überlappung, "
                          "Ausweichabstand nicht im Dokument")

        # --- B4 (2): Drucken und PDF aus dem Seitenmenü ---------------------------
        gedruckt = []
        menues = []
        app.open_print_html = lambda html, name, titel: gedruckt.append((html, name, titel)) or "break"
        with patch.object(editor, "popup", side_effect=menues.append):
            editor.show_page_menu()
        menu = menues[-1]
        menu.invoke(eintraege(menu)["Drucken und PDF …"])
        ruhe()
        html, name, titel = gedruckt[-1]
        assert name == "glide_seite" and titel == "Seite drucken"
        assert "<h1>Bildseite</h1>" in html and "Absatz 29." in html
        assert html.count('src="data:image/png;base64,') == 3, html.count("data:image")
        assert "file:" not in html and 'src="http' not in html
        menu.destroy()
        pruefungen.append("B4: „Drucken und PDF …“ bettet alle drei Bilder als Daten-URL ein, ohne Dateiverweis")

        # --- B4 (3): Markdown kopieren, speichern und zurück ------------------------
        menues.clear()
        with patch.object(editor, "popup", side_effect=menues.append):
            editor.show_page_menu()
        menu = menues[-1]
        menu.invoke(eintraege(menu)["Markdown kopieren"])
        ruhe()
        kopiert = root.clipboard_get()
        anhaenge = app.page_image_attachments(seite["id"])
        assert len(anhaenge) == 3
        for anhang in anhaenge:
            uri = Path(app.resolve_attachment_path(anhang)).resolve().as_uri()
            assert f"]({uri})" in kopiert, (uri, kopiert[:400])
        assert toasts[-1] == "Seite als Markdown kopiert"
        vorher = len(app.lists)
        tiefe = len(app.undo_stack)
        app.new_page_from_clipboard()
        ruhe(0.3)
        kopie = app.lists[-1]
        assert len(app.lists) == vorher + 1 and kopie["title"] == "Bildseite"
        dokument = mod.RichNoteEditor.normalize(kopie["rich_note"])
        assert len(dokument["images"]) == 3 and len(kopie["attachments"]) == 3, (dokument["images"], kopie["attachments"])
        assert sorted(sha(app.resolve_attachment_path(a)) for a in kopie["attachments"]) == sorted(map(sha, bilder))
        assert {span["tag"] for span in dokument["spans"]} >= set(dokument["images"])
        assert len(app.undo_stack) == tiefe + 1
        app.undo_last_change()
        ruhe(0.2)
        assert len(app.lists) == vorher
        pruefungen.append("B4: „Markdown kopieren“ verweist auf die Bilddateien; aus der Zwischenablage "
                          "entsteht eine Seite mit denselben drei Bildern, ein Undo")

        app.set_active_list(seite["id"])
        ruhe(0.3)
        editor = app.rich_note_editor
        ziel = os.path.join(ordner, "export", "Bild Seite.md")
        os.makedirs(os.path.dirname(ziel))
        menues.clear()
        with patch.object(editor, "popup", side_effect=menues.append), \
                patch.object(mod.filedialog, "asksaveasfilename", return_value=ziel):
            editor.show_page_menu()
            menu = menues[-1]
            menu.invoke(eintraege(menu)["Als Markdown speichern …"])
            ruhe()
        text = Path(ziel).read_text(encoding="utf-8")
        assert "](Bild%20Seite%20Bilder/" in text and "file:" not in text, text[:300]
        daneben = sorted(Path(ziel).parent.joinpath("Bild Seite Bilder").iterdir())
        assert sorted(sha(p) for p in daneben) == sorted(map(sha, bilder))
        with patch.object(mod.filedialog, "askopenfilename", return_value=ziel):
            app.import_markdown_page()
        ruhe(0.3)
        rueck = app.lists[-1]
        dokument = mod.RichNoteEditor.normalize(rueck["rich_note"])
        assert rueck["id"] != seite["id"] and rueck["title"] == "Bildseite"
        assert len(dokument["images"]) == 3 and sorted(sha(app.resolve_attachment_path(a))
                                                       for a in rueck["attachments"]) == sorted(map(sha, bilder))
        # Ohne Ordnerangabe bleiben relative Verweise benannte Textverweise (nichts wird gesucht).
        fremd = app.page_document_from_markdown("![Logo](Bild%20Seite%20Bilder/x.png)\n", rueck["id"])
        assert not fremd.get("images") and "Bild: Logo" in fremd["text"]
        pruefungen.append("B4: „Als Markdown speichern …“ legt die Bilder daneben, „Markdown als Seite öffnen“ "
                          "holt sie als Seitenbilder zurück; relative Verweise ohne Ordner bleiben Text")

        # --- G14h: Treffer hervorheben ---------------------------------------------
        fund = app.new_list_object("Maße", [], list_kind=app.LIST_KIND_PAGE)
        fund["rich_note"] = {"text": "Die Größe zählt.\n" + "Füllzeile\n" * 80
                                     + "Mehr zur GRÖSSE später; groesse am Ende.", "spans": [], "links": {}}
        app.lists.append(fund)
        app.save_items()
        app.set_home_view()
        ruhe()
        app.show_quick_open()
        ruhe()
        feld = app._quick_open["entry"]
        feld.insert(0, "größe")
        ruhe()
        treffer = next(r for r in app.quick_open_results("größe") if r["target"] == ("list", fund["id"]))
        assert treffer.get("highlight") == app.search_key("größe")
        assert app._quick_open["results"][0]["target"] == ("list", fund["id"]) \
            if "results" in app._quick_open else True
        feld.focus_force()
        ruhe()
        feld.event_generate("<Return>")
        ruhe(0.3)
        editor = app.rich_note_editor
        assert app.active_list_id == fund["id"] and isinstance(editor, mod.PageEditor)
        bereiche = editor.text.tag_ranges("search_hit")
        markiert = [editor.text.get(bereiche[i], bereiche[i + 1]) for i in range(0, len(bereiche), 2)]
        assert markiert == ["Größe", "GRÖSSE", "groesse"], markiert
        assert editor.text.compare("insert", "==", bereiche[0])
        app.flush_rich_note()
        assert not any(span["tag"] == "search_hit" for span in app.page_entry(fund["id"])["rich_note"]["spans"])
        editor.text.focus_force()
        ruhe()
        editor.text.event_generate("<Escape>")
        ruhe()
        assert not editor.text.tag_ranges("search_hit")
        editor.highlight_matches(app.search_key("groesse"))
        assert len(editor.text.tag_ranges("search_hit")) == 6
        vorher_text = editor.text.get("1.0", "end-1c")
        editor.text.event_generate("<Key-x>")
        ruhe()
        assert not editor.text.tag_ranges("search_hit")
        editor.text.delete("1.0", "end-1c")
        editor.text.insert("1.0", vorher_text)
        app.flush_rich_note()
        pruefungen.append("G14h: Enter auf einem Inhaltstreffer markiert „Größe/GRÖSSE/groesse“, zeigt die erste "
                          "Fundstelle; Esc und Tippen heben auf; nie gespeichert")

        # --- D-03: Filter erklären -------------------------------------------------
        label = app.new_label_object("Kunde") if hasattr(app, "new_label_object") else None
        if label is None:
            label = {"id": "lbl-kunde", "name": "Kunde", "color": None}
        app.labels.append(label)
        a = app.new_item("Passt", importance=3)
        a["labels"] = [label["id"]]
        b = app.new_item("Zu unwichtig", importance=1)
        b["labels"] = [label["id"]]
        c = app.new_item("Schon erledigt", importance=3)
        c["labels"] = [label["id"]]
        c["done"] = True
        d = app.new_item("Ohne Label", importance=3)
        liste = app.new_list_object("Filterliste", [a, b, c, d])
        app.lists.append(liste)
        app.settings["saved_filters"] = [{"id": "f-wichtig", "name": "Wichtig für Kunden", "query": "",
                                          "list_ids": [liste["id"]], "label_ids": [label["id"]],
                                          "status": "open", "importance": "3", "due": "any",
                                          "label_mode": "any", "source": "all"}]
        app.save_items()
        app.save_settings()
        bestand = copy.deepcopy((app.lists, app.settings["saved_filters"]))
        assert app.saved_filters.open("f-wichtig")
        ruhe(0.3)
        assert [eintrag[4]["id"] for eintrag in app.saved_filters.entries()] == [a["id"]]
        aktion = next(e for e in app.app_action_entries() if e["id"] == "explain_saved_filter")
        kopf = app._stats_full_text
        assert "1 passende Aufgaben" in kopf and "Ausgeblendet: 3" in kopf, kopf
        assert f"({aktion['path']} › Filter erklären)" in kopf, (kopf, aktion["path"])
        zeile = next(row for row, quelle in app.in_progress_item_sources.items() if quelle[1] == a["id"])
        menu = app.build_in_progress_context_menu(zeile)
        menu.invoke(eintraege(menu)["Warum steht das hier? …"])
        ruhe()
        titel, text = infos[-1][:2]
        assert titel == "Warum steht „Passt“ hier?", titel
        assert text.splitlines() == ["✓  Liste: steht in „Filterliste“", "✓  Status: verlangt: nur offene · Punkt ist offen",
                                     "✓  Wichtigkeit: verlangt: hoch · Punkt: hoch",
                                     "✓  Labels: mindestens eines der gewählten Labels"], text
        erklaert = app.saved_filters.explain_item(liste["id"], d["id"])
        assert [(e["key"], e["ok"]) for e in erklaert] == [("list", True), ("status", True), ("importance", True),
                                                           ("labels", False)]
        assert "fehlt: Kunde" in erklaert[-1]["detail"]
        app.invoke_app_action(aktion)
        ruhe()
        titel, text = infos[-1][:2]
        assert titel == "Filter „Wichtig für Kunden“", titel
        assert "Passend: 1 · Ausgeblendet: 3" in text and "• Status: 1" in text and "• Wichtigkeit: 1" in text \
            and "• Labels: 1" in text, text
        assert copy.deepcopy((app.lists, app.settings["saved_filters"])) == bestand, "Erklären darf nichts ändern"
        app.set_home_view()
        ruhe()
        app.explain_saved_filter()
        assert "Öffne zuerst einen gespeicherten Filter" in infos[-1][1] and aktion["path"] in infos[-1][1], infos[-1]
        pruefungen.append("D-03: „Warum steht das hier?“ mit ✓/✗ je Bedingung, Kopf „Ausgeblendet: 3“ mit echtem "
                          "Menüpfad, „Filter erklären …“ nach erster verfehlter Bedingung, Daten unverändert")

        # --- H-02r: Bereichsbäume per Tastatur ------------------------------------
        ordner_seiten = app.new_folder_object("Projektordner")
        app.folders.append(ordner_seiten)
        app.locate_sidebar_root("folder", ordner_seiten["id"], "pages")
        seiten = [app.new_list_object(f"Notizseite {n}", [], list_kind=app.LIST_KIND_PAGE) for n in range(3)]
        app.lists.extend(seiten)
        app.save_items()
        app.save_settings()
        app.update_sidebar_list()
        ruhe(0.2)
        baum = app.pages_listbox
        for bereich in (app.pages_listbox, app.notes_listbox, app.drawings_listbox):
            for folge in ("<Alt-Up>", "<Alt-Down>", "<Alt-Left>", "<Alt-Right>"):
                assert bereich.bind(folge), (bereich, folge)

        def geschwister():
            return [k for k in mod.glide_sidebar.sibling_ids(app.sidebar_policy(), "list", seiten[0]["id"])
                    if k in {s["id"] for s in seiten}]

        def taste(folge, kennung):
            iid = "list:" + kennung
            baum.see(iid)
            baum.selection_set(iid)
            baum.focus(iid)
            baum.focus_force()
            ruhe(0.05)
            baum.event_generate(folge)
            ruhe(0.2)

        start = geschwister()
        letzte = start[-1]
        name = next(s["title"] for s in seiten if s["id"] == letzte)
        tiefe = len(app.undo_stack)
        taste("<Alt-Up>", letzte)
        nachher = geschwister()
        assert nachher.index(letzte) == start.index(letzte) - 1, (start, nachher)
        assert toasts[-1] == f"„{name}“ nach oben verschoben", toasts[-1]
        assert len(app.undo_stack) == tiefe + 1
        knopf = app._undo_toast["button"]
        knopf.command()
        ruhe(0.2)
        assert geschwister() == start
        taste("<Alt-Down>", start[0])
        assert geschwister().index(start[0]) == 1 and toasts[-1].endswith("nach unten verschoben"), toasts[-1]
        taste("<Alt-Right>", letzte)
        verschoben = next(e for e in app.lists if e["id"] == letzte)
        assert verschoben.get("folder_id") == ordner_seiten["id"], (infos[-1:], toasts[-1:])
        assert toasts[-1] == f"„{name}“ in „Projektordner“ verschoben", toasts[-1]
        assert app.get_sidebar_tree_for_iid("list:" + letzte) is app.pages_listbox
        app.sidebar_folder_open_states[ordner_seiten["id"]] = True
        app.update_sidebar_list()
        ruhe(0.2)
        taste("<Alt-Left>", letzte)
        assert not next(e for e in app.lists if e["id"] == letzte).get("folder_id")
        assert toasts[-1] == f"„{name}“ aus dem Ordner heraus verschoben", toasts[-1]
        assert app.sidebar_section_for("list", letzte) == "pages"
        taste("<Alt-Up>", letzte)
        reihenfolge = geschwister()
        beenden()
        starten()
        assert geschwister() == reihenfolge, (geschwister(), reihenfolge)
        pruefungen.append("H-02r: Alt+↑/↓/→/← im Seitenbaum ordnen um, rücken in den Ordner und heraus, "
                          "melden Ziel und Wirkung mit Rückgängig, Reihenfolge übersteht den Neustart")

        # Spaltenboard: Alt+→ nennt Zielspalte und gesetztes Feld.
        karte = app.new_item("Boardkarte", importance=1)
        brett = app.new_list_object("Brett", [karte])
        app.lists.append(brett)
        app.save_items()
        app.set_active_list(brett["id"])
        ruhe()
        ws = app.workspace
        ws.set_mode("board")
        ws.configure_board("layout", "columns")
        ws.set_board_group_field("importance")
        ruhe(0.3)
        schluessel = [spalte["key"] for spalte in ws.column_order]
        eigene = [key for _box, kennung, key, _tag in ws.column_hits if kennung == karte["id"]]
        assert len(eigene) == 1, eigene
        ziel = next(spalte for spalte in ws.column_order[schluessel.index(eigene[0]) + 1:]
                    if spalte.get("settable", True))
        ws.focus_card(karte["id"])
        ws.canvas.focus_force()
        ruhe(0.1)
        tiefe = len(app.undo_stack)
        ws.canvas.event_generate("<Alt-Right>")
        ruhe(0.3)
        assert [key for _box, kennung, key, _tag in ws.column_hits if kennung == karte["id"]] == [ziel["key"]]
        assert toasts[-1] == f"„Boardkarte“ → Spalte „{ziel['title']}“ · Wichtigkeit gesetzt", toasts[-1]
        assert len(app.undo_stack) == tiefe + 1
        app._undo_toast["button"].command()
        ruhe(0.3)
        assert app.find_item_in_lists(karte["id"])[0]["importance"] == 1
        ws.set_mode("list")
        ruhe()
        pruefungen.append(f"H-02r: Spaltenboard Alt+→ nach „{ziel['title']}“ mit Hinweis und einem Rückgängig")

        # --- N08: JPEG über djpeg (Linux-Weg erzwungen) ----------------------------
        jpeg = os.path.join(ordner, "foto.jpg")
        ppm = os.path.join(ordner, "foto.ppm")
        quelle = mod.tk.PhotoImage(master=root, width=96, height=64)
        quelle.put("#AA3355", to=(0, 0, 96, 64))
        quelle.write(ppm, format="ppm")
        if shutil.which("cjpeg"):
            subprocess.run(["cjpeg", "-outfile", jpeg, ppm], check=True, capture_output=True)
        elif shutil.which("sips"):
            subprocess.run(["sips", "-s", "format", "jpeg", ppm, "--out", jpeg], check=True, capture_output=True)
        vorschau = app.previews
        echtes_which = shutil.which  # `patch` ersetzt es modulweit
        if os.path.isfile(jpeg) and shutil.which("djpeg"):
            vorschau.PLATFORM = "linux"
            try:
                with patch.object(mod.glide_image_preview.glide_preview_tools.shutil, "which",
                                  side_effect=lambda name: echtes_which(name) if name == "djpeg" else None):
                    assert vorschau.needs_conversion(root, jpeg) and vorschau.can_convert(jpeg)
                    umgewandelt = vorschau.convert(jpeg)
                    assert umgewandelt and umgewandelt.endswith(".ppm"), umgewandelt
                    assert vorschau.natural_size(root, jpeg) == (96, 64)
                    assert not vorschau.needs_conversion(root, jpeg)
                    png = app.reference_png_path(jpeg)
                    assert png.endswith(".png") and mod.tk.PhotoImage(master=root, file=png).width() == 96
                with patch.object(mod.glide_image_preview.glide_preview_tools.shutil, "which", return_value=None):
                    zweites = os.path.join(ordner, "zweites.jpg")
                    shutil.copy2(jpeg, zweites)
                    os.utime(zweites, ns=(1, 1))
                    assert not vorschau.can_convert(zweites) and not vorschau.needs_conversion(root, zweites)
                    assert vorschau.natural_size(root, zweites) is None
                    try:
                        app.reference_png_path(zweites)
                        raise AssertionError("ohne Werkzeug darf keine Referenz entstehen")
                    except mod.glide_drawing.DrawingFormatError as meldung:
                        assert "nicht umwandeln" in str(meldung), meldung
            finally:
                vorschau.PLATFORM = None
            pruefungen.append("N08: Linux-Weg mit djpeg – Vorschau 96×64 aus PPM, Referenz als PNG; "
                              "ohne Werkzeug Platzhalter und Meldung")
        else:
            pruefungen.append("N08: übersprungen – djpeg oder JPEG-Erzeugung fehlt in dieser Umgebung")

        ruhe(0.2)
        assert not fehler, fehler
        print("test_wissen3340: OK; " + "; ".join(pruefungen))
    finally:
        try:
            beenden()
        except Exception:
            pass
