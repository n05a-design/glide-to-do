"""Druck- und PDF-Ausgabe: Formate, Optionen, Escaping, Dateien und Dialog."""
import copy
import importlib.machinery
import importlib.util
import os
import re
import tempfile
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def titel_von(html):
    treffer = re.search(r"<h1>(.*?)</h1>", html, re.S)
    return treffer.group(1) if treffer else ""


with tempfile.TemporaryDirectory(prefix="glide-features317-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features317", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    callbacks = []
    root.report_callback_exception = lambda *args: callbacks.append(args)
    app = mod.ListApp(root)
    messages = []
    app.show_warning = app.show_error = lambda *args, **kwargs: messages.append(args)
    app.show_info = lambda *args, **kwargs: None
    app.ask_yes_no = lambda *args, **kwargs: True
    geoeffnet = []
    app.open_external_path = lambda pfad: geoeffnet.append(pfad) or True
    try:
        heute = date.today().isoformat()
        morgen = (date.today() + timedelta(days=1)).isoformat()
        assert app.MAX_PRINT_ITEMS == 2000
        assert [key for key, _text in app.PRINT_FORMATS] == ["today", "list", "planday", "checklist"]
        vorgaben = app.print_default_options()
        assert set(vorgaben) == {key for key, _text in app.PRINT_OPTION_LABELS}
        assert vorgaben["done"] is False and vorgaben["boxes"] is True

        # --- Bestand mit Sonderzeichen, Struktur und Zusatzangaben ----------
        liste = app.new_list_object('Besichtigung <Musterstr. 5> & "Hof"', [])
        haupt = app.new_item('Zählerstände & "Heizung" prüfen', due=heute, due_time="09:30",
                             planned_date=heute, estimated_minutes=45, importance=3)
        haupt["description"] = "Foto vom Zähler machen <wichtig>"
        erledigt = app.new_item("Schon abgehakt")
        erledigt["done"] = True
        gruppe = app.new_item("Außenbereich", kind=app.ITEM_KIND_GROUP)
        unterpunkt = app.new_item("Garage öffnen", planned_date=morgen, estimated_minutes=20)
        gruppe["children"] = [unterpunkt]
        ueberfaellig = app.new_item("Alte Frist", due="2020-01-02")
        liste["items"] = [haupt, erledigt, gruppe, ueberfaellig]
        app.lists.append(liste)
        app.set_active_list(liste["id"])
        label = app.ensure_label_by_name("Vor Ort")
        haupt["labels"] = [label["id"]] if isinstance(label, dict) and label.get("id") else []
        app.update_today_plan([haupt["id"]], add=True)
        assert app.save_items() and app.save_settings()

        # --- Grundgerüst aller vier Formate ---------------------------------
        for key, _text in app.PRINT_FORMATS:
            html = app.build_print_html(key)
            assert html.startswith("<!DOCTYPE html>") and html.rstrip().endswith("</html>"), key
            assert '<meta charset="utf-8">' in html and "@page" in html, key
            # Eigenständig: keine externen Verweise, kein Skript, kein Nachladen.
            for verboten in ("http://", "https://", "<script", "<link", "<img", "@import", "url("):
                assert verboten not in html, (key, verboten)
            assert mod.APP_NAME in html and "gedruckt am" in html, key
        try:
            app.build_print_html("unbekannt")
        except ValueError:
            pass
        else:
            raise AssertionError("Ein unbekanntes Druckformat wurde angenommen")

        # --- Escaping --------------------------------------------------------
        html = app.build_print_html("list")
        assert "&lt;Musterstr. 5&gt; &amp; &quot;Hof&quot;" in titel_von(html), titel_von(html)
        assert "Zählerstände &amp; &quot;Heizung&quot; prüfen" in html
        assert "&lt;wichtig&gt;" in html
        assert "<Musterstr" not in html.replace("<!DOCTYPE html>", "")

        # --- Optionen wirken einzeln ----------------------------------------
        aus = {key: False for key, _text in app.PRINT_OPTION_LABELS}
        schlicht = app.build_print_html("list", aus)
        assert "Schon abgehakt" not in schlicht, "Erledigte bleiben ohne Option draußen."
        assert 'class="box"' not in schlicht and 'class="meta"' not in schlicht
        assert "Foto vom Zähler" not in schlicht and "Vor Ort" not in schlicht
        assert 'class="lines"' not in schlicht
        assert "Schon abgehakt" in app.build_print_html("list", dict(aus, done=True))
        assert 'class="box"' in app.build_print_html("list", dict(aus, boxes=True))
        assert "Foto vom Zähler" in app.build_print_html("list", dict(aus, description=True))
        assert "Vor Ort" in app.build_print_html("list", dict(aus, labels=True))
        mit_frist = app.build_print_html("list", dict(aus, due=True))
        assert "Fällig:" in mit_frist and "09:30" in mit_frist
        mit_aufwand = app.build_print_html("list", dict(aus, effort=True))
        assert "Bearbeitungstag:" in mit_aufwand and "45 min" in mit_aufwand
        assert "Aufwand: 45 min" in mit_aufwand
        assert 'class="lines"' in app.build_print_html("list", dict(aus, notes=True))

        # --- Formate zeigen die richtige Menge -------------------------------
        tageszettel = app.build_print_html("today")
        # Seit 3.22 gibt es einen Tagesabschnitt statt zweier.
        assert "Mein Tag" in tageszettel and "Bearbeitungstag heute" not in tageszettel
        assert "Heute fällig" in tageszettel and "Überfällig" in tageszettel
        assert "Aus: Besichtigung" in tageszettel, "Übersichten nennen die Quellliste."
        planung = app.build_print_html("planday", day=morgen)
        assert "Garage öffnen" in planung and "Zählerstände" not in planung
        assert app.format_due_display(morgen) in planung
        leer = app.build_print_html("planday", day="2091-01-01")
        assert "nichts zu drucken" in leer, leer
        checkliste = app.build_print_html("checklist")
        assert "Checkliste" in checkliste and 'class="box"' in checkliste
        # Gruppen erscheinen mit ihrer Art und rücken ihre Unterpunkte ein.
        assert app.ITEM_KIND_NAMES[app.ITEM_KIND_GROUP] in checkliste
        assert "padding-left: 12pt" in checkliste

        # Ordneransicht fasst alle enthaltenen Listen zusammen.
        ordner = app.new_folder_object("Objekte", color="accent")
        app.folders.append(ordner)
        liste["folder_id"] = ordner["id"]
        zweite = app.new_list_object("Zweite Wohnung", [app.new_item("Schlüssel holen")])
        zweite["folder_id"] = ordner["id"]
        app.lists.append(zweite)
        assert app.save_items()
        app.set_active_folder(ordner["id"])
        ordnerdruck = app.build_print_html("list")
        assert titel_von(ordnerdruck) == "Objekte"
        assert "Schlüssel holen" in ordnerdruck and "Zählerstände" in ordnerdruck
        app.set_active_list(liste["id"])

        # --- Obergrenze -------------------------------------------------------
        gross = app.new_list_object("Massenprobe", [app.new_item(f"Punkt {nummer}")
                                                    for nummer in range(app.MAX_PRINT_ITEMS + 25)])
        app.lists.append(gross)
        app.set_active_list(gross["id"])
        begrenzt = app.build_print_html("list")
        assert "abgeschnitten" in begrenzt and str(app.MAX_PRINT_ITEMS) in begrenzt
        assert begrenzt.count("<li") == app.MAX_PRINT_ITEMS, begrenzt.count("<li")
        app.set_active_list(liste["id"])

        # --- Datei schreiben --------------------------------------------------
        ziel = os.path.join(folder, "unterordner", "druck.html")
        pfad = app.write_print_document(ziel, "checklist")
        assert os.path.isfile(pfad) and pfad == os.path.abspath(ziel)
        inhalt = Path(pfad).read_text(encoding="utf-8")
        assert inhalt.startswith("<!DOCTYPE html>") and "Garage öffnen" in inhalt
        assert not list(Path(os.path.dirname(pfad)).glob(".glide-print-*")), "Temporärdatei blieb liegen."
        vorher = copy.deepcopy(app.data_payload())
        app.write_print_document(ziel, "today")
        assert app.data_payload() == vorher, "Drucken verändert keine Daten."
        try:
            app.write_print_document(mod.SAVE_FILE, "list")
        except ValueError:
            pass
        else:
            raise AssertionError("Die Nutzdatendatei wurde als Druckziel akzeptiert")

        # --- Dialog in Hell und Dunkel ---------------------------------------
        root.deiconify()
        root.geometry("1100x780+10+10")
        for theme in ("light", "dark"):
            app.set_design(theme, apply_now=False)
            app.apply_theme()
            geoeffnet.clear()

            def drucken(dialog, parent=None):
                dialog.geometry("780x640")
                dialog.update()
                widgets = list(descendants(dialog))
                haken = {key: next(w for w in widgets if w.winfo_name() == "print_" + key)
                         for key, _text in app.PRINT_OPTION_LABELS}
                # „active" heißt nur, dass der Zeiger über dem Feld liegt.
                zustaende = {key: str(w.cget("state")) for key, w in haken.items()}
                assert all(wert != "disabled" for wert in zustaende.values()), zustaende
                haken["notes"].invoke()
                knopf = next(w for w in widgets if isinstance(w, mod.RoundedButton)
                             and w.text == "Öffnen und drucken")
                assert knopf.winfo_ismapped()
                assert (knopf.winfo_rooty() + knopf.winfo_height()
                        <= dialog.winfo_rooty() + dialog.winfo_height())
                knopf.command()
            app.run_modal = drucken
            assert app.show_print_dialog() == "break"
            assert len(geoeffnet) == 1, geoeffnet
            erzeugt = Path(geoeffnet[0])
            assert erzeugt.is_file() and erzeugt.suffix == ".html"
            gedruckt = erzeugt.read_text(encoding="utf-8")
            assert 'class="lines"' in gedruckt, "Die angehakte Option wirkt in der Ausgabe."
            erzeugt.unlink()

            def abbrechen(dialog, parent=None):
                dialog.update()
                next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)
                     and w.text == "Abbrechen").command()
            app.run_modal = abbrechen
            geoeffnet.clear()
            zustand = copy.deepcopy(app.data_payload())
            app.show_print_dialog()
            assert not geoeffnet and app.data_payload() == zustand
        assert not callbacks, callbacks
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK: Druckansicht in vier Formaten, Optionen, Escaping, Ordnerdruck, Obergrenze, Dateien und Dialog")
