"""Paket Tempo 3.33.19: P06r, P04, P03r und E01 über echte Einstiege.

Prüft je Aktion höchstens einen Seitenleistenaufbau und einen geschriebenen
Einstellungsstand, die Schreibsemantik der gebündelten Einstellungen (einmal
schreiben, auch nach Fehler; gleiche Inhalte nicht erneut; Schreibfehler
bleiben sichtbar), die Sperrdatei, das inkrementelle Bildlayout gegen einen
vollständigen Neuaufbau (Differenzprobe), das Stehenlassen der Startseite und
den gebündelten Umbruch im Einstellungsfenster.

--app wählt den Quellstand; mit der unveränderten 3.33.18 muss die Suite rot
sein (Gegenprobe). Künstliche Daten in einem temporären GLIDE_DATA_DIR.
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


with tempfile.TemporaryDirectory(prefix="glide-tempo-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_tempo_test", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    fehler = []
    root = mod.tk.Tk()
    root.geometry("1280x840+20+20")
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
    app.show_info = lambda *a, **k: None
    app.ask_yes_no = lambda *a, **k: True
    pruefungen = []

    def ruhe(sekunden=0.15):
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            root.update()
            time.sleep(0.01)

    try:
        # --- P06r: Anforderungen je Aktion ---------------------------------
        ordner_eintrag = app.new_folder_object("Projekte")
        app.folders.append(ordner_eintrag)
        listen = []
        for nummer in range(3):
            eintrag = app.new_list_object(f"Liste {nummer}", [app.new_item(f"Aufgabe {nummer}.{i}") for i in range(30)])
            app.lists.append(eintrag)
            listen.append(eintrag)
        app.save_items()
        app.set_active_list(listen[0]["id"])
        ruhe()
        zaehler = {"seitenleiste": 0, "einstellungen": 0, "sperre": 0, "daten": 0}
        aufbau = app._update_sidebar_list

        def seitenleiste(*a, **k):
            zaehler["seitenleiste"] += 1
            return aufbau(*a, **k)
        app._update_sidebar_list = seitenleiste
        schreiben = app.write_json_atomic

        def geschrieben(pfad, daten):
            name = os.path.basename(pfad)
            schluessel = {"settings.json": "einstellungen", "glide.lock": "sperre",
                          "liste_speicher.json": "daten"}.get(name)
            if schluessel:
                zaehler[schluessel] += 1
            return schreiben(pfad, daten)
        app.write_json_atomic = geschrieben

        def auswaehlen(liste_id):
            app.set_active_list(liste_id)
            ruhe(0.05)
            kennung = next(e for e in app.lists if e["id"] == liste_id)["items"][0]["id"]
            app.tree.selection_set(kennung)
            app.tree.focus(kennung)

        def ausfuehren(name, vorbereitung, aktion, grenzen):
            vorbereitung()
            ruhe(0.05)
            for schluessel in zaehler:
                zaehler[schluessel] = 0
            # Die Sperrdatei trägt einen sekundengenauen Zeitstempel und wird
            # höchstens einmal je Sekunde geschrieben. Überschreitet die Aktion
            # unter Last eine Sekundengrenze, ist ein zweites Schreiben richtig.
            sekunde = int(time.time())
            aktion()
            ruhe(0.05)
            sekunden = int(time.time()) - sekunde + 1
            for schluessel, grenze in grenzen.items():
                erlaubt = grenze * sekunden if schluessel == "sperre" else grenze
                assert zaehler[schluessel] <= erlaubt, (name, dict(zaehler), sekunden)
            assert zaehler["daten"] == 1, (name, dict(zaehler))
            return dict(zaehler)

        keine = lambda: None  # noqa: E731
        ergebnis = {
            "Abhaken": ausfuehren("Abhaken", lambda: auswaehlen(listen[0]["id"]), app.toggle_done,
                                  {"seitenleiste": 1, "einstellungen": 1, "sperre": 1}),
            "Rückgängig": ausfuehren("Rückgängig", keine, app.undo_last_change,
                                     {"seitenleiste": 1, "einstellungen": 1, "sperre": 1}),
            "Umbenennen": ausfuehren("Umbenennen", keine,
                                     lambda: app.apply_sidebar_rename(("list", listen[2]["id"]), "Umbenannt"),
                                     {"seitenleiste": 1, "einstellungen": 1, "sperre": 1}),
            "Archivieren": ausfuehren("Archivieren", keine, lambda: app.set_archived("list", listen[2]["id"], True),
                                      {"seitenleiste": 1, "einstellungen": 1, "sperre": 1}),
            "Zurückholen": ausfuehren("Zurückholen", keine, lambda: app.set_archived("list", listen[2]["id"], False),
                                      {"seitenleiste": 1, "einstellungen": 1, "sperre": 1}),
            "Kopieren": ausfuehren("Kopieren", keine, lambda: app.duplicate_list(listen[1]["id"]),
                                   {"seitenleiste": 2, "einstellungen": 2, "sperre": 1}),
            "Löschen": ausfuehren("Löschen", keine, lambda: app.delete_list_by_id(listen[2]["id"]),
                                  {"seitenleiste": 1, "einstellungen": 1, "sperre": 1}),
            "Papierkorb leeren": ausfuehren("Papierkorb leeren", keine, app.empty_trash,
                                            {"seitenleiste": 1, "einstellungen": 1, "sperre": 1}),
        }
        app.write_json_atomic = schreiben
        app._update_sidebar_list = aufbau
        # Das Ergebnis der Aktionen bleibt gleich: archiviert/zurück, gelöscht im Papierkorb, geleert.
        assert all(e["id"] != listen[2]["id"] for e in app.lists) and not app.trash
        pruefungen.append("P06r: je Aktion höchstens ein Seitenleistenaufbau, ein Einstellungs- und ein Sperrschreiben "
                          + json.dumps(ergebnis, ensure_ascii=False))

        # --- Schreibsemantik der Einstellungen ------------------------------
        assert hasattr(app, "settings_write_batch"), "P06r: gebündeltes Schreiben der Einstellungen fehlt"
        datei = Path(mod.SETTINGS_FILE)
        app.save_settings()
        stand = datei.stat().st_mtime_ns
        with patch.object(app, "write_json_atomic", wraps=app.write_json_atomic) as writer:
            assert app.save_settings() is True
            assert not writer.called, "gleicher Inhalt wird nicht erneut geschrieben"
        datei.unlink()
        assert app.save_settings() is True and datei.exists(), "gelöschte Datei wird neu geschrieben"
        app.settings["glide_test_wert"] = 1
        with patch.object(app, "write_json_atomic", side_effect=OSError("Test: voll")):
            assert app.save_settings() is False
        assert app.save_settings() is True
        assert json.loads(datei.read_text(encoding="utf-8"))["glide_test_wert"] == 1
        # Aufschub: genau ein Schreiben am Ende, auch wenn die Aktion abbricht.
        with patch.object(app, "write_json_atomic", wraps=app.write_json_atomic) as writer:
            try:
                with app.settings_write_batch():
                    app.settings["glide_test_wert"] = 2
                    assert app.save_settings(defer=True) is True
                    app.settings["glide_test_zweiter"] = 3
                    assert app.save_settings(defer=True) is True
                    assert not writer.called
                    raise RuntimeError("Test: Abbruch in der Aktion")
            except RuntimeError:
                pass
            assert writer.call_count == 1
        gespeichert = json.loads(datei.read_text(encoding="utf-8"))
        assert gespeichert["glide_test_wert"] == 2 and gespeichert["glide_test_zweiter"] == 3
        # Außerhalb eines Rahmens schreibt auch ein aufschiebbarer Aufruf sofort.
        app.settings["glide_test_wert"] = 4
        app.save_settings(defer=True)
        assert json.loads(datei.read_text(encoding="utf-8"))["glide_test_wert"] == 4
        pruefungen.append("Einstellungen: gleicher Inhalt ohne Schreiben, gelöschte Datei, Schreibfehler, "
                          "Aufschub mit einmaligem Schreiben auch nach Abbruch")

        # --- Sperrdatei: Prüfung bleibt, gleiches Schreiben entfällt ---------
        sperre = Path(mod.LOCK_FILE)
        with patch.object(app, "write_json_atomic", wraps=app.write_json_atomic) as writer:
            app.refresh_data_lock()
            app.refresh_data_lock()
            assert writer.call_count <= 1
        fremd = json.loads(sperre.read_text(encoding="utf-8"))
        fremd["token"] = "fremdes-geraet"
        sperre.write_text(json.dumps(fremd), encoding="utf-8")
        app.refresh_data_lock()
        assert app._data_read_only is True, "fremde Belegung wird weiter erkannt"
        app._data_read_only = False
        app._read_only_reason = None
        sperre.write_text(json.dumps(app._lock_token), encoding="utf-8")
        pruefungen.append("Sperrdatei: Fremdbelegung erkannt, gleicher Inhalt einmal je Sekunde")

        # --- P04: inkrementelles Bildlayout = vollständiges -----------------
        pfade = []
        for nummer, (breite, hoehe) in enumerate(((160, 120), (300, 180), (900, 300))):
            bild = mod.tk.PhotoImage(master=root, width=breite, height=hoehe)
            bild.put(("#3366CC", "#CC6633", "#33AA66")[nummer], to=(0, 0, breite, hoehe))
            pfad = os.path.join(ordner, f"bild{nummer}.png")
            bild.write(pfad, format="png")
            pfade.append(pfad)
        absatz = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 5
        app.new_page_from_markdown("# Bildseite\n\n" + "\n\n".join(f"Absatz {i}. {absatz}" for i in range(24)))
        ruhe(0.3)
        editor = app.rich_note_editor
        for i in range(9):
            editor.insert_images([pfade[i % 3]], f"{4 + i * 5}.0")
        ruhe(0.5)
        text = editor.text

        def layoutstand():
            editor.layout_images()
            root.update()
            raender = {str(tag): tuple(map(str, text.tag_ranges(tag))) for tag in text.tag_names()
                       if str(tag).startswith(("imgflow:", "imgpad:", "imgend:"))}
            orte = {key: (view.winfo_x(), view.winfo_y(), view.winfo_ismapped(), getattr(view, "_size", None))
                    for key, view in editor._image_views.items()}
            return raender, orte

        def vergleichen(fall):
            inkrementell = layoutstand()
            editor._image_layout_signature = None
            for view in editor._image_views.values():
                view._render_signature = None
            voll = layoutstand()
            assert inkrementell == voll, (fall, inkrementell, voll)

        schluessel = editor.image_keys()
        links_bilder = [key for key in schluessel if editor.images[key]["mode"] == "left"]
        mitte_bilder = [key for key in schluessel if editor.images[key]["mode"] == "center"]
        faelle = 0
        for breite in (1280, 860):
            root.geometry(f"{breite}x840+20+20")
            ruhe(0.3)
            vergleichen(f"Breite {breite}")
            faelle += 1
            for key in links_bilder[:2] + mitte_bilder[:1]:
                stelle = text.index(f"{text.tag_ranges(key)[0]} +1l lineend")
                for zeichen in ("x", " weiterer Text, der eine Zeile umbrechen lässt " * 2, "\n"):
                    text.insert(stelle, zeichen)
                    ruhe(0.2)
                    vergleichen(f"Tippen neben {key} bei {breite}")
                    faelle += 1
            text.insert("2.0", "Fern ")
            ruhe(0.2)
            vergleichen(f"Tippen fern bei {breite}")
            faelle += 1
        editor.set_image_mode(links_bilder[0], "right")
        ruhe(0.2)
        vergleichen("Modus rechts")
        editor.set_image_width(links_bilder[0], 220)
        ruhe(0.2)
        vergleichen("Breite geändert")
        editor.select_image(links_bilder[0])
        ruhe(0.1)
        vergleichen("Auswahl")
        faelle += 3
        # Tippen fern ohne Umfluss: kein Rand neu, kein Bild neu gezeichnet.
        with patch.object(editor, "flow_around", wraps=editor.flow_around) as fluss:
            gezeichnet = {key: view.find_all() for key, view in editor._image_views.items()}
            text.insert("2.0", "y")
            ruhe(0.3)
            assert not fluss.called, "Tippen fern berechnet keinen Umfluss"
            assert gezeichnet == {key: view.find_all() for key, view in editor._image_views.items()}
        with patch.object(editor, "flow_around", wraps=editor.flow_around) as fluss:
            key = links_bilder[1]
            # Am Anfang der Zeile neben dem Bild: sicher im Umflussbereich (das
            # Ende der logischen Zeile kann schon unter dem Bild liegen).
            stelle = text.index(f"{text.tag_ranges(key)[0]} +1l linestart +3c")
            assert any(text.compare(stelle, "<", ende) for ende in text.tag_ranges("imgflow:" + key[4:])[1::2])
            text.insert(stelle, "z")
            ruhe(0.3)
            assert fluss.call_count == 1, fluss.call_count
        assert faelle >= 20, faelle
        pruefungen.append(f"P04: {faelle} Fälle inkrementell = vollständig; fern 0 Umflüsse/0 Zeichnungen, nah genau 1")

        # --- P03r: Startseite bleibt stehen, solange nichts sich ändert -----
        app.set_home_view()
        ruhe(0.3)
        erste = set(map(str, descendants(app.home_content)))
        app.set_active_list(listen[0]["id"])
        ruhe(0.2)
        app.set_home_view()
        ruhe(0.3)
        assert set(map(str, descendants(app.home_content))) == erste, "Rückkehr ohne Änderung baut nicht neu"
        flaechen = tuple(app.home_content.winfo_children())
        texte_vorher = [w.cget("text") for w in descendants(app.home_content) if isinstance(w, mod.tk.Label)]
        aufgabe = listen[0]["items"][1]
        app.toggle_item_done_anywhere(aufgabe["id"])
        ruhe(0.3)
        app.set_home_view()
        ruhe(0.3)
        nach_aenderung = set(map(str, descendants(app.home_content)))
        assert [w.cget("text") for w in descendants(app.home_content) if isinstance(w, mod.tk.Label)] != texte_vorher, "Datenänderung aktualisiert sichtbare Inhalte"
        assert tuple(app.home_content.winfo_children()) == flaechen, "Datenänderung erhält Startseitenflächen"
        versteckt = next(key for key in app.home_tile_order() if app.home_tile_visible(key))
        app.set_home_tile_hidden(versteckt, True)
        app.set_home_view()
        ruhe(0.3)
        assert set(map(str, descendants(app.home_content))) != nach_aenderung, "Kachelauswahl baut neu"
        app.set_home_tile_hidden(versteckt, False)
        vorher = set(map(str, descendants(app.home_content)))
        app.set_design("dark", apply_now=True)
        app.set_home_view()
        ruhe(0.3)
        assert set(map(str, descendants(app.home_content))) != vorher, "Designwechsel baut neu"
        assert app.home_content.cget("bg") == app.theme["bg"]
        app.set_design("light", apply_now=True)
        pruefungen.append("P03r: Rückkehr ohne Änderung ohne Neuaufbau; Daten aktualisieren Inhalte; Kachelauswahl und Design invalidieren")

        # --- E01: Umbruch je Spalte -----------------------------------------
        geprueft = {}

        def run_modal(dialog, *a, **k):
            dialog.update()
            spalten = {}
            for widget in descendants(dialog):
                if isinstance(widget, (mod.tk.Label, mod.tk.Checkbutton)) and str(widget.cget("justify")) == "left":
                    umbruch = int(float(widget.cget("wraplength") or 0))
                    if umbruch:
                        spalten.setdefault(str(widget.master), set()).add(umbruch)
            geprueft["spalten"] = spalten
            dialog.destroy()
        with patch.object(app, "run_modal", side_effect=run_modal):
            app.show_settings_dialog()
        ruhe(0.1)
        assert geprueft["spalten"] and all(len(werte) == 1 for werte in geprueft["spalten"].values()), geprueft
        pruefungen.append("E01: Einstellungsfenster setzt den Umbruch je Spalte einheitlich")

        ruhe(0.2)
        assert not fehler, fehler
        print("test_tempo33319: OK; " + "; ".join(pruefungen))
    finally:
        try:
            app.cancel_pending_callbacks()
            app.release_data_lock()
        except Exception:
            pass
        try:
            root.destroy()
        except mod.tk.TclError:
            pass
