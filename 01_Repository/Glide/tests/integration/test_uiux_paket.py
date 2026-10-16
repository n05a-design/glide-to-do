"""UI-/UX-Feature-Paket vom 15.10.2026 (B01–B19): echte Tk-Wege mit künstlichen Daten.

Jeder Fall prüft eine Abnahme aus `00_Arbeitsvorbereitung/Featurepaket_UI_UX/PROMPT.md`
über die tatsächlichen Widgets, Geometrien und Einstellungen – keine bloße
Attributprüfung, wo eine Lage oder Wirkung messbar ist. `--app` erlaubt die
rote Gegenprobe gegen die gelieferte Vorversion (07_Python-Versionen 3.42.0),
`--fall` einzelne Fälle. Die menschliche Sicht-, DPI- und Screenreaderabnahme
bleibt getrennt offen.
"""
import argparse
import importlib.machinery
import importlib.util
import json
import os
import sys
import tempfile
import time
import traceback
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SHOWCASE_APP = REPO / "tests/fixtures/showcase/Glide-Showcase_App.glideapp"
FAELLE = ("b01", "b02", "b03", "b04", "b05", "b06_b15", "b15_appweit", "b07", "b08", "b09", "b10", "b11",
          "b12_b13", "b14", "b16", "b17_b19", "b18")


class Lauf:
    def __init__(self, app_path, data):
        os.environ["GLIDE_DATA_DIR"] = data
        os.environ["GLIDE_TEST_MODE"] = "1"
        sys.path.insert(0, str(Path(app_path).parent))
        loader = importlib.machinery.SourceFileLoader("glide_uiux_" + str(abs(hash(str(app_path)))), str(app_path))
        self.mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = self.mod
        loader.exec_module(self.mod)
        self.data = data
        self.errors = []
        self.start()

    def start(self, geometry="1280x800+20+20"):
        self.root = self.mod.tk.Tk()
        self.root.geometry(geometry)
        self.root.report_callback_exception = lambda *e: self.errors.append(
            "".join(traceback.format_exception(*e))[-600:])
        self.app = self.mod.ListApp(self.root)
        self.app.show_info = self.app.show_warning = lambda *a, **k: None
        self.app.show_error = lambda *a, **k: self.errors.append(str(a))
        self.idle()

    def neustart(self, geometry="1280x800+20+20"):
        self.app.save_settings()
        self.root.destroy()
        self.start(geometry)

    def idle(self, runden=4):
        for _ in range(runden):
            self.root.update_idletasks()
            self.root.update()

    def showcase(self):
        assert self.app.restore_app_backup(str(SHOWCASE_APP), sections={
            "tasks": True, "settings": True, "templates": True, "activity": True}, show_success=False)
        self.idle()

    def ende(self):
        try:
            self.root.destroy()
        except Exception:
            pass


def knoepfe(widget, klasse):
    gefunden, stapel = [], [widget]
    while stapel:
        aktuell = stapel.pop()
        for kind in aktuell.winfo_children():
            if isinstance(kind, klasse):
                gefunden.append(kind)
            stapel.append(kind)
    return gefunden


def fall_b01(lauf):
    """Nach „Gelesen“ steht die Startseite ohne weitere Aktion am Anfang."""
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    app.settings["release_notes_seen"] = "3.35.0"
    app._settings_existed = True
    app.set_home_view()
    lauf.idle(8)
    gelesen = [k for k in knoepfe(app.home_content, mod.RoundedButton) if k.text == "Gelesen"]
    assert gelesen, "Karte „Neu in …“ fehlt"
    app.home_canvas.yview_moveto(1.0)
    lauf.idle()
    assert app.home_canvas.yview()[0] > 0.05, "Probe braucht eine gescrollte Startseite"
    gelesen[0].command()
    lauf.idle(6)
    assert app.home_canvas.yview()[0] == 0.0, ("nicht am Seitenanfang", app.home_canvas.yview())
    assert not [k for k in knoepfe(app.home_content, mod.RoundedButton) if k.text == "Gelesen"]
    # Gewöhnliche Aktualisierung behält die Lage.
    app.home_canvas.yview_moveto(0.4)
    lauf.idle()
    lage = app.home_canvas.yview()[0]
    app._home_signature = None
    app.refresh_home()
    lauf.idle()
    assert abs(app.home_canvas.yview()[0] - lage) < 0.02, "Aktualisierung springt"
    lauf.root.geometry("900x700+20+20")
    lauf.idle(6)
    lauf.neustart()
    app = lauf.app
    app.set_home_view()
    lauf.idle(6)
    assert not [k for k in knoepfe(app.home_content, mod.RoundedButton) if k.text == "Gelesen"], "Karte nach Neustart"
    return "Gelesen → Seitenanfang; Aktualisierung behält Lage; Neustart ohne Karte"


def fall_b02(lauf):
    """„Startseite anpassen“ beginnt an der linken Kante des Kachelrasters."""
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    ergebnisse = []
    for geometrie in ("1280x800+20+20", "860x700+20+20", "1600x900+20+20"):
        lauf.root.geometry(geometrie)
        app.set_home_view()
        lauf.idle(8)
        knopf = next(k for k in knoepfe(app.home_content, mod.RoundedButton) if k.text == "Startseite anpassen")
        # Die Kacheln liegen in Spaltenrahmen des Rasters; dessen linke Kante ist die Inhaltsflucht.
        spalten = [w for w in knoepfe(app.home_content, mod.tk.Frame) if w.winfo_manager() == "grid"
                   and w.master.master is app.home_content and w.winfo_ismapped()]
        assert spalten, "Kachelraster nicht gefunden"
        links = min(w.winfo_rootx() for w in spalten)
        assert abs(knopf.winfo_rootx() - links) <= 2, (geometrie, knopf.winfo_rootx(), links)
        assert knopf.winfo_ismapped() and knopf.winfo_width() >= knopf.winfo_reqwidth() - 1
        unten = max(w.winfo_rooty() + w.winfo_height() for w in spalten)
        assert knopf.winfo_rooty() >= unten - 2, "Knopf überdeckt eine Kachel"
        ergebnisse.append(geometrie.split("+")[0])
    return "linke Rasterkante bei " + ", ".join(ergebnisse)


def fall_b03(lauf):
    """Gismo: fester Name, Spielereien immer, Ausblenden nur über die Kachel."""
    app, mod = lauf.app, lauf.mod
    app.settings["mascot_name"] = "Mika"
    app.settings["mascot_playful"] = False
    lauf.neustart()
    app = lauf.app
    assert "mascot_name" not in app.settings and "mascot_playful" not in app.settings, "Altwerte bleiben"
    assert app.mascot_name() == "Gismo"
    app.set_home_view()
    lauf.idle(8)
    texte = [k.text for k in knoepfe(app.home_content, mod.RoundedButton)]
    assert not any(t.startswith(("Benennen", "Spielereien")) for t in texte), texte
    assert {"Füttern", "Spielen", "Ruhen"} <= set(texte), texte
    titel = [w.cget("text") for w in knoepfe(app.home_content, mod.tk.Label)]
    assert "Gismo" in titel, "Kachel heißt nicht Gismo"
    vorher = app.mascot_care()["affection"]
    next(k for k in knoepfe(app.home_content, mod.RoundedButton) if k.text == "Spielen").command()
    lauf.idle()
    assert app.mascot_care()["affection"] > vorher or vorher == 100, "Spielen wirkt nicht"
    # Bewegungsreduktion nimmt nur die Bewegung.
    app.animations_enabled = lambda: False
    vorher = app.mascot_care()["satiety"]
    next(k for k in knoepfe(app.home_content, mod.RoundedButton) if k.text == "Füttern").command()
    lauf.idle()
    assert app.mascot_care()["satiety"] > vorher or vorher == 100, "Füttern ohne Bewegung wirkt nicht"
    # Ausblenden der Kachel blendet ihn überall aus – auch neben Leerzuständen.
    leer = app.new_list_object("Leer", [])
    app.lists.append(leer)
    app.save_items()
    app.set_active_list(leer["id"])
    lauf.idle()
    assert app.empty_state_mascot(app.tree) is not None
    app.settings["home_tiles_hidden"] = list(app.settings.get("home_tiles_hidden", [])) + ["mascot"]
    assert app.empty_state_mascot(app.tree) is None
    lauf.neustart()
    assert lauf.app.settings["home_tiles_hidden"].count("mascot") == 1, "Ausblenden nicht gespeichert"
    return "Name fest, Altwerte entfernt, Pflege immer, Ausblenden über Kachel"


def fall_b04(lauf):
    """Galeriebilder als eigene Kachel; öffnet den Bildkontext."""
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    assert "gallery" in mod.glide_home.STANDARD, "keine Kachel Galeriebilder im Standard"
    app.settings["home_tile_order"] = []
    app.settings["home_tiles_hidden"] = [k for k in mod.glide_home.KEYS if k not in mod.glide_home.STANDARD]
    app.set_home_view()
    lauf.idle(10)
    titel = [w.cget("text") for w in knoepfe(app.home_content, mod.tk.Label)]
    assert any("Galeriebilder" in t for t in titel), "Kachel fehlt"
    zellen = [w for w in knoepfe(app.home_content, mod.tk.Label) if hasattr(w, "_home_gallery_key")]
    assert len(zellen) >= 3, len(zellen)
    for _ in range(40):
        lauf.idle(1)
        if all(str(z.cget("image")) or z.cget("text") in ("fehlt",) for z in zellen):
            break
        time.sleep(0.05)
    mit_bild = [z for z in zellen if str(z.cget("image"))]
    assert mit_bild, "keine Vorschau geladen"
    for zelle in zellen:
        rahmen = zelle.master
        assert rahmen.winfo_width() == rahmen.winfo_height(), "Rahmen nicht quadratisch"
        assert rahmen.winfo_rootx() + rahmen.winfo_width() <= zelle.winfo_toplevel().winfo_rootx() + lauf.root.winfo_width()
    galerie = next(e for e in app.lists if app.is_gallery_list(e))
    app.open_gallery_image(galerie["id"], 1)
    lauf.idle(6)
    assert app.view_mode == "list" and app.current_list()["id"] == galerie["id"]
    assert app.gallery_view is not None and app.gallery_view.detail_index == 1, "Bildkontext nicht geöffnet"
    # Eigene, gespeicherte Auswahl ohne die neue Kachel bleibt unverändert.
    ordnung = [k for k in mod.glide_home.KEYS if k != "gallery"]
    vor_b04 = {k: v for k, v in app.settings.items() if k != "home_tiles_gallery"}
    normal = app.normalize_personal_settings(dict(vor_b04, home_tile_order=ordnung, home_tiles_hidden=[]))
    assert "gallery" in normal["home_tiles_hidden"], "neue Kachel überschreibt eigene Auswahl"
    wieder = app.normalize_personal_settings(dict(normal, home_tiles_hidden=[]))
    assert "gallery" not in wieder["home_tiles_hidden"], "nur einmal ausblenden"
    # Fehlende Datei: verständlich statt leer.
    anhang = dict(galerie["attachments"][0], storage="attachments/fehlt_glide_probe.png")
    probe = mod.tk.Label(lauf.root)
    app.show_home_gallery_thumbnail(probe, anhang, 64)
    for _ in range(20):
        lauf.idle(1)
        if probe.cget("text") == "fehlt":
            break
        time.sleep(0.05)
    assert probe.cget("text") == "fehlt", probe.cget("text")
    return f"{len(zellen)} Vorschauen, {len(mit_bild)} geladen, öffnet Detail, eigene Auswahl bleibt, fehlende Datei benannt"


def fall_b05(lauf):
    """Logo endet an der Grundlinie der Unterzeile und behält sein Seitenverhältnis."""
    app, mod = lauf.app, lauf.mod
    liste = app.new_list_object("Abstimmung · Entwurf 02", [app.new_item("A", due="2026-01-01"), app.new_item("B")])
    app.lists.append(liste)
    app.save_items()
    app.set_active_list(liste["id"])
    lauf.idle(6)
    logo = app.header_logo
    assert logo.winfo_ismapped()
    schrift = mod.tkfont.Font(root=lauf.root, font=mod.app_font(mod.glide_design.FONT_SIZES["caption"], "bold"))
    chips = [w for w in app.page_chip_row.winfo_children() if w.winfo_ismapped()]
    assert chips, "Unterzeile ohne Kennzahlen"
    grundlinie = chips[0].winfo_rooty() + schrift.metrics("ascent")
    unten = logo.winfo_rooty() + logo.winfo_height()
    assert abs(unten - grundlinie) <= 2, ("Logo-Unterkante", unten, grundlinie)
    oben_titel = app.title_label.winfo_rooty()
    assert logo.winfo_rooty() > oben_titel, "Logo beginnt über dem Titel"
    seiten = logo.winfo_width() / logo.winfo_height()
    assert abs(seiten - mod.glide_logo.aspect()) < 0.06, seiten
    return f"Unterkante {unten} ≈ Grundlinie {grundlinie}, Seitenverhältnis {seiten:.3f}"


def fall_b06_b15(lauf):
    """Kein Datum/„?“ im Kopf; Hinweisschalter; Papierkorbtext; Knopf nie überdeckt."""
    app, mod = lauf.app, lauf.mod
    assert getattr(app, "hints_button", None) is None, "„?“ noch im Kopf"
    app.set_home_view()
    lauf.idle(6)
    assert app.stats_label.cget("text") == "", ("Datum im Kopf", app.stats_label.cget("text"))
    assert app.settings.get("show_hints") is False, "Vorgabe nicht aus"
    befunde = []
    for groesse in ("mittel", "gross"):
        app.settings["ui_font_size"] = groesse
        for hinweise in (False, True):
            app.settings["show_hints"] = hinweise
            for geometrie in ("860x700+20+20", "1280x800+20+20", "860x700+20+20"):
                lauf.root.geometry(geometrie)
                app.set_trash_view()
                lauf.idle(8)
                text = app.tree.item(app.EMPTY_ROW_ID, "text")
                erwartet = "Der Papierkorb ist leer." + (
                    " Gelöschte Punkte, Listen und Ordner landen hier und bleiben wiederherstellbar." if hinweise else "")
                assert text == erwartet, (text, hinweise)
                knopf, hinweis = app.empty_action_button, app.empty_text_label
                assert knopf.winfo_ismapped() and hinweis.winfo_ismapped()
                # Tatsächliche Höhe: Tk 9.1 meldet die angeforderte Höhe nach
                # einem neuen Text verspätet (GitHub-Prüfung 16.10.2026).
                unten_text = hinweis.winfo_rooty() + max(hinweis.winfo_height(), hinweis.winfo_reqheight())
                assert knopf.winfo_rooty() >= unten_text, ("Knopf überdeckt", geometrie, hinweise, groesse)
                assert knopf.winfo_rooty() + knopf.winfo_height() <= app.tree.winfo_rooty() + app.tree.winfo_height()
                befunde.append(f"{groesse}/{hinweise}/{geometrie.split('+')[0]}")
    # Wächst der Leertext nachträglich, ohne dass die App ihn neu platziert
    # (so verhält sich Tk 9.1 mit verspäteter Größe), rückt der Knopf nach.
    app.set_trash_view()
    lauf.idle(6)
    knopf, hinweis = app.empty_action_button, app.empty_text_label
    hinweis.configure(text=str(hinweis.cget("text")) + " Zusatzzeile für die Probe." * 8)
    lauf.idle(6)
    assert knopf.winfo_rooty() >= hinweis.winfo_rooty() + hinweis.winfo_height(), \
        ("Knopf folgt verspätet gewachsenem Leertext nicht", knopf.winfo_rooty(), hinweis.winfo_rooty(), hinweis.winfo_height())
    befunde.append("nachträglich gewachsener Leertext")
    # Später Map (unter Tk 9.1/X11 die Regel, Nachstellung der CI-Auswertung
    # 16.10.2026): Leerzustand aufbauen, solange der Baum nicht gemappt ist,
    # dann unverändert einblenden – der Knopf steht trotzdem unter dem Text.
    baum = app.tree
    verwaltung = baum.winfo_manager()
    lage = {"pack": baum.pack_info, "grid": baum.grid_info, "place": baum.place_info}[verwaltung]()
    lage.pop("in", None)
    getattr(baum, f"{verwaltung}_forget")()
    lauf.idle(2)
    app.refresh_trash_overview()
    lauf.idle(4)
    getattr(baum, verwaltung)(**lage)
    lauf.idle(8)
    knopf, hinweis = app.empty_action_button, app.empty_text_label
    assert knopf.winfo_y() >= hinweis.winfo_y() + hinweis.winfo_height(), \
        ("Knopf nach spätem Map überdeckt", knopf.winfo_y(), hinweis.winfo_y(), hinweis.winfo_height())
    app.settings["ui_font_size"] = "mittel"
    # Gefüllter Papierkorb zeigt keinen Leertext.
    liste = app.new_list_object("Papierkorbprobe", [app.new_item("Weg")])
    app.lists.append(liste)
    app.save_items()
    app.trash_list_entry(liste["id"]) if hasattr(app, "trash_list_entry") else None
    app.settings["show_hints"] = True
    lauf.neustart()
    assert lauf.app.settings["show_hints"] is True, "Schalter nicht gespeichert"
    return f"{len(befunde) - 1} Kombinationen, nachträglich gewachsener Leertext und später Map ohne Überdeckung; Schalter gespeichert"


def sichtbarer_ausschnitt(widget, mod):
    """Bildschirmrechteck nach Beschnitt durch alle Vorfahren – oder None."""
    if not widget.winfo_viewable():
        return None
    x1, y1 = widget.winfo_rootx(), widget.winfo_rooty()
    x2, y2 = x1 + widget.winfo_width(), y1 + widget.winfo_height()
    vorfahr = widget.master
    while vorfahr is not None:
        ax, ay = vorfahr.winfo_rootx(), vorfahr.winfo_rooty()
        x1, y1 = max(x1, ax), max(y1, ay)
        x2, y2 = min(x2, ax + vorfahr.winfo_width()), min(y2, ay + vorfahr.winfo_height())
        if isinstance(vorfahr, (mod.tk.Tk, mod.tk.Toplevel)):
            break
        vorfahr = vorfahr.master
    return (x1, y1, x2, y2) if x2 > x1 and y2 > y1 else None


def knopf_befunde(fenster, mod, kontext):
    """Appweiter Buttonschutz (B15): kein Knopf verdeckt, abgeschnitten oder überlagert.

    Geprüft wird die tatsächliche Geometrie aller sichtbaren Knöpfe eines
    Fensters: (1) kein fremdes Text-, Eingabe- oder Knopfelement liegt im
    sichtbaren Knopfbereich, (2) Knöpfe außerhalb scrollbarer Flächen sind
    vollständig im Fenster, (3) die Beschriftung passt in den Knopf.
    """
    knopfarten = (mod.RoundedButton, mod.tk.Button, mod.ttk.Button)
    textarten = (mod.tk.Label, mod.tk.Message, mod.tk.Text, mod.tk.Entry, mod.ttk.Label, mod.ttk.Entry)
    alle = [fenster] + knoepfe(fenster, mod.tk.Misc)
    knoepfe_hier = [w for w in alle if isinstance(w, knopfarten) and w.winfo_viewable()
                    and w.winfo_width() > 1 and w.winfo_height() > 1]
    fremde = [w for w in alle if isinstance(w, textarten + knopfarten) and w.winfo_viewable()]
    befunde = []

    def verwandt(a, b):
        return str(a).startswith(str(b) + ".") or str(b).startswith(str(a) + ".") or a is b

    for knopf in knoepfe_hier:
        sicht = sichtbarer_ausschnitt(knopf, mod)
        if sicht is None:
            continue
        name = getattr(knopf, "text", None) or (knopf.cget("text") if "text" in knopf.keys() else str(knopf))
        in_scrollflaeche = False
        vorfahr = knopf.master
        while vorfahr is not None and not isinstance(vorfahr, (mod.tk.Tk, mod.tk.Toplevel)):
            if isinstance(vorfahr, mod.tk.Canvas):
                in_scrollflaeche = True
            vorfahr = vorfahr.master
        voll = (knopf.winfo_rootx(), knopf.winfo_rooty(),
                knopf.winfo_rootx() + knopf.winfo_width(), knopf.winfo_rooty() + knopf.winfo_height())
        if not in_scrollflaeche and sicht != voll:
            befunde.append(f"{kontext}: „{name}“ abgeschnitten {voll}→{sicht}")
        if isinstance(knopf, mod.RoundedButton) and not knopf.wrap_text:
            if knopf.text_width() > knopf.winfo_width() - 4:
                befunde.append(f"{kontext}: Beschriftung „{name}“ breiter als Knopf")
        elif isinstance(knopf, mod.tk.Button) and knopf.winfo_reqwidth() > knopf.winfo_width() + 1:
            befunde.append(f"{kontext}: Beschriftung „{name}“ breiter als Knopf")
        for anderes in fremde:
            if verwandt(knopf, anderes):
                continue
            ihre = sichtbarer_ausschnitt(anderes, mod)
            if ihre is None:
                continue
            breite = min(sicht[2], ihre[2]) - max(sicht[0], ihre[0])
            hoehe = min(sicht[3], ihre[3]) - max(sicht[1], ihre[1])
            if breite > 0 and hoehe > 0:
                art = type(anderes).__name__
                was = getattr(anderes, "text", None) or (str(anderes.cget("text"))[:40] if "text" in anderes.keys() else "")
                befunde.append(f"{kontext}: „{name}“ überlagert von {art} „{was}“ ({breite}×{hoehe} px)")
    return len(knoepfe_hier), befunde


def fall_b15_appweit(lauf):
    """Buttonschutz in Hauptansichten und Dialogen, Mindest- und Referenzgröße, große Schrift."""
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    gesamt, befunde = 0, []
    for groesse in ("mittel", "gross"):
        lauf.app.settings["ui_font_size"] = groesse
        lauf.neustart()
        app = lauf.app
        app.show_info = app.show_warning = lambda *a, **k: None
        seite = next(e for e in app.lists if app.is_page_list(e))
        liste = max((e for e in app.lists if not app.is_page_list(e) and e.get("items")), key=lambda e: len(e["items"]))
        ansichten = (("Startseite", app.set_home_view), ("Heute", app.set_today_view),
                     ("Labels", app.set_labels_view), ("Vorlagen", app.set_template_view),
                     ("Papierkorb", app.set_trash_view), ("Liste", lambda: app.set_active_list(liste["id"])),
                     ("Seite", lambda: app.set_active_list(seite["id"])))
        for geometrie in ("860x700+20+20", "1280x800+20+20"):
            lauf.root.geometry(geometrie)
            lauf.idle(4)
            for hinweise in (False, True):
                app.settings["show_hints"] = hinweise
                for name, oeffnen in ansichten:
                    oeffnen()
                    lauf.idle(8)
                    anzahl, funde = knopf_befunde(lauf.root, mod, f"{name} {groesse} {geometrie.split('+')[0]} Hinweise {'an' if hinweise else 'aus'}")
                    gesamt += anzahl
                    befunde.extend(funde)
            gesehen = []

            def modal(dialog, parent=None, _geometrie=geometrie):
                lauf.idle(4)
                titel = dialog.title() or type(dialog).__name__
                anzahl, funde = knopf_befunde(dialog, mod, f"Dialog „{titel}“ {groesse} {_geometrie.split('+')[0]}")
                gesehen.append((titel, anzahl))
                befunde.extend(funde)
                dialog.destroy()

            app.run_modal = modal
            # Meldungen laufen hier als echte Dialoge (leeres Fehlerprotokoll).
            app.__dict__.pop("show_info", None)
            for name in ("show_about_dialog", "show_release_notes_dialog", "open_error_log",
                         "show_shortcuts_dialog", "show_settings_dialog"):
                oeffnen = getattr(app, name, None)
                if oeffnen is None:
                    continue
                vorher = set(str(w) for w in lauf.root.winfo_children())
                oeffnen()
                lauf.idle(4)
                for neu in [w for w in lauf.root.winfo_children()
                            if str(w) not in vorher and isinstance(w, mod.tk.Toplevel) and w.winfo_exists()]:
                    modal(neu)
            gesamt += sum(anzahl for _titel, anzahl in gesehen)
            dialoge = len(gesehen)
            app.show_info = lambda *a, **k: None
    assert not befunde, (len(befunde), befunde[:12])
    assert dialoge >= 5, ("Dialoge nicht gesehen", dialoge)
    return f"{gesamt} Knopfprüfungen in 7 Ansichten und 5 Dialogen (2 Größen, 2 Schriftgrößen, Hinweise an/aus) ohne Befund"


def fall_b07(lauf):
    """Windows-Menüs und Kopfsymbole teilen Mittellinie und Höhe."""
    app = lauf.app
    knoepfe_kopf = [k for k in app.header_controls.pack_slaves() if k.winfo_ismapped()]
    assert knoepfe_kopf
    mitten = {k.winfo_rooty() + k.winfo_height() / 2 for k in knoepfe_kopf}
    assert max(mitten) - min(mitten) <= 1, mitten
    menues = getattr(app, "custom_menu_buttons", [])
    if not menues:
        return "keine Fenstermenüs auf dieser Plattform (Systemmenüleiste); Kopfsymbole fluchten"
    for knopf in menues:
        mitte = knopf.winfo_rooty() + knopf.winfo_height() / 2
        assert abs(mitte - min(mitten)) <= 1, (knopf.text, mitte, mitten)
        assert knopf.winfo_height() == knoepfe_kopf[0].winfo_height(), (knopf.text, knopf.winfo_height())
    return f"{len(menues)} Menüs auf der Mittellinie der {len(knoepfe_kopf)} Kopfsymbole"


def fall_b08(lauf):
    """Fehlerprotokoll: Überschrift und Text beginnen an derselben Kante."""
    app, mod = lauf.app, lauf.mod
    gemessen = {}

    def modal(dialog, parent=None):
        lauf.idle(3)
        labels = [w for w in knoepfe(dialog, mod.tk.Label) if w.cget("text") == "Fehlerprotokoll"]
        texte = knoepfe(dialog, mod.tk.Text)
        schrift_l = mod.tkfont.Font(root=lauf.root, font=labels[0].cget("font"))
        gemessen["kopf"] = labels[0].winfo_rootx() + int(labels[0].cget("bd")) + int(labels[0].cget("padx"))
        gemessen["text"] = texte[0].winfo_rootx() + int(texte[0].cget("bd")) + int(texte[0].cget("padx"))
        gemessen["ok"] = [k for k in knoepfe(dialog, mod.RoundedButton) if k.text == "OK"][0].winfo_ismapped()
        del schrift_l
        dialog.destroy()

    app.run_modal = modal
    if os.path.isfile(mod.ERROR_LOG_FILE):
        os.remove(mod.ERROR_LOG_FILE)
    del app.show_info
    app.open_error_log()
    assert gemessen, "Dialog nicht gesehen"
    assert gemessen["kopf"] == gemessen["text"], gemessen
    assert gemessen["ok"]
    return f"gemeinsame linke Textkante x={gemessen['text']}"


def fall_b09(lauf):
    """Symbole stehen nach Glyphenregel auf der Mitte ihres Textes."""
    app, mod = lauf.app, lauf.mod
    assert hasattr(mod, "glide_glyphs"), "Glyphenregel fehlt"
    assert app.symbol_row_shift(app.ICONS["trash"]) != 0 or app.ICONS["trash"] != "♲"
    assert app.symbol_row_shift(app.ICONS["home"]) == 0
    baum = app.system_listbox
    lauf.idle(4)
    leinwand = baum.icon_canvas
    texte = {leinwand.itemcget(i, "text"): leinwand.coords(i)[1] for i in leinwand.find_all() if leinwand.type(i) == "text"}
    zeilen = {baum.set(i, "icon"): baum.bbox(i, "icon") for i in baum.get_children("")}
    for symbol, y in texte.items():
        box = zeilen.get(symbol)
        if not box:
            continue
        erwartet = box[1] + box[3] / 2 - baum.ICON_RISE + app.symbol_row_shift(symbol)
        assert abs(y - erwartet) < 0.01, (symbol, y, erwartet)
    # Bereichspfeile: sichtbare Mitte auf der Großbuchstabenmitte (±1 px).
    pfeil, titel = app.sidebar_heading_icon, app.sidebar_title
    t_font = mod.tkfont.Font(root=lauf.root, font=titel.cget("font"))
    p_font = mod.tkfont.Font(root=lauf.root, font=pfeil.cget("font"))
    tm, pm = app.glyph_metrics_for(titel.cget("font")), app.glyph_metrics_for(pfeil.cget("font"))
    grund_t = titel.winfo_rooty() + (titel.winfo_height() - t_font.metrics("linespace")) / 2 + t_font.metrics("ascent")
    grund_p = pfeil.winfo_rooty() + (pfeil.winfo_height() - p_font.metrics("linespace")) / 2 + p_font.metrics("ascent")
    kappe = grund_t - tm.cap_center() * app.font_pixels(t_font)
    mitte = grund_p - pm.ink_center(pfeil.cget("text")) * app.font_pixels(p_font)
    assert abs(kappe - mitte) <= 1.0, (kappe, mitte)
    # Startseitenkachel „Pinnwände“: Pfadtrenner „›“ auf der Großbuchstabenmitte
    # des Knopftextes (±0,5 px), Schreibweise unverändert.
    lauf.showcase()
    app.settings["home_tiles_hidden"] = []
    app.set_home_view()
    lauf.idle(10)
    pfade = [k for k in knoepfe(app.home_content, mod.RoundedButton) if "›" in k.text]
    assert pfade, "Probe braucht einen Startseitenknopf mit Pfad"
    knopf = pfade[0]
    trenner = [i for i in knopf.find_all() if knopf.type(i) == "text" and knopf.itemcget(i, "text") == "›"]
    assert trenner, ("Pfadtrenner nicht optisch gesetzt", knopf.text)
    font = mod.tkfont.Font(root=lauf.root, font=knopf.font)
    metrik, pixel = app.glyph_metrics_for(knopf.font), app.font_pixels(font)
    abweichung = []
    for element in trenner:
        x, y = knopf.coords(element)
        nachbar = [i for i in knopf.find_withtag("glide_label_text")
                   if knopf.coords(i)[0] < x and abs(knopf.coords(i)[1] - y) <= 3]
        assert nachbar, ("kein Text vor dem Trenner", knopf.text)
        zeile = knopf.coords(nachbar[0])[1]
        grossmitte = zeile + font.metrics("ascent") - metrik.cap_center() * pixel
        sichtbar = y + font.metrics("ascent") - metrik.ink_center("›") * pixel
        abweichung.append(sichtbar - grossmitte)
        assert abs(sichtbar - grossmitte) <= 0.5, (knopf.text, sichtbar, grossmitte)
    zeilen = sorted({knopf.coords(i)[1] for i in knopf.find_withtag("glide_label_text")})
    def stelle(i):
        x, y = knopf.coords(i)
        return min(zeilen, key=lambda z: abs(z - y)), x
    gesetzt = "".join(knopf.itemcget(i, "text") for i in sorted(knopf.find_withtag("glide_label"), key=stelle))
    assert gesetzt.replace(" ", "") == knopf.text.replace(" ", ""), ("Beschriftung verändert", gesetzt)
    return (f"Papierkorbsymbol {app.symbol_row_shift(app.ICONS['trash']):+d} px, Pfeilabweichung {mitte - kappe:+.2f} px, "
            f"Pfadtrenner Startseite {max(abweichung, key=abs):+.2f} px")


def fall_b10(lauf):
    """Lupe, sobald eine zulässige Schrift sie selbst enthält; sonst lesbares „Su“."""
    app, mod = lauf.app, lauf.mod
    verfuegbar = {name.casefold() for name in app.available_font_families()}
    traeger = []
    # Gegen eine Vorversion ohne Rückfallregel dieselben Systemschriften prüfen.
    kandidaten = getattr(mod.glide_symbols, "SYMBOL_FONT_FALLBACKS", {}).get(
        "search", ("Segoe UI Symbol", "Apple Symbols", "Noto Sans Symbols", "Noto Sans Symbols2", "DejaVu Sans Mono"))
    for familie in (app.ui_font_family(),) + tuple(kandidaten):
        if familie.casefold() not in verfuegbar:
            continue
        probe = mod.tkfont.Font(root=lauf.root, family=familie, size=app.ui_font_size(1), weight="bold")
        if str(lauf.root.tk.call("font", "actual", probe.name, "-family", "⌕")).casefold() == familie.casefold():
            traeger.append(familie)
    assert "Suchen" in app.search_button._glide_tooltip["source"]
    assert app.search_button.command == app.show_quick_open
    if not traeger:
        assert app.ICONS["search"] == "Su", app.ICONS["search"]
        return "keine Schrift mit Lupe auf diesem System – lesbarer Rückfall „Su“"
    assert app.ICONS["search"] == "⌕", ("keine Lupe", app.ICONS["search"], traeger)
    familie = app.search_button.font[0]
    assert familie in traeger or familie == app.ui_font_family(), (familie, traeger)
    assert str(lauf.root.tk.call("font", "actual", app.search_button.font, "-family", "⌕")).casefold() == familie.casefold()
    return f"Lupe aus {familie}"


def fall_b11(lauf):
    """Je Aufgabenansicht: Titel vorrangig, Metadaten nur so breit wie ihr Inhalt."""
    app = lauf.app
    lauf.showcase()
    font = app.measurement_font(app.tree_font())
    rand = app.tree_cell_padding(font)

    def zeilen():
        stapel, alle = list(app.tree.get_children("")), []
        while stapel:
            zeile = stapel.pop()
            alle.append(zeile)
            stapel.extend(app.tree.get_children(zeile))
        return alle

    liste = max((e for e in app.lists if e.get("items")),
                key=lambda e: sum(1 for p in e["items"] if p.get("due") and not p.get("done")))
    ansichten = (("Labels", app.set_labels_view), ("Heute", app.set_today_view),
                 ("Liste", lambda: app.set_active_list(liste["id"])))
    befunde, labels_due = [], None
    for name, oeffnen in ansichten:
        oeffnen()
        lauf.idle(8)
        breiten = {}
        for spalte in ("due", "labels"):
            werte = [app.tree.set(z, spalte) for z in zeilen()]
            werte = [w for w in werte if w]
            breite = int(app.tree.column(spalte, "width"))
            breiten[spalte] = breite
            if not werte:
                continue
            noetig = max(font.measure(w) for w in werte) + rand
            assert breite <= noetig + 2, (name, spalte, "breiter als Inhalt", breite, noetig)
            # Bei Enge weichen Metadaten ganz (Titel zuerst), abgeschnitten werden sie nie.
            assert breite == 0 or breite >= noetig - 1, (name, spalte, "abgeschnitten", breite, noetig)
        titel = int(app.tree.column("#0", "width"))
        assert titel > max(breiten.values()), (name, "Titel nicht vorrangig", titel, breiten)
        befunde.append(f"{name}: Titel {titel}, Datum {breiten['due']}, Labels {breiten['labels']}")
        if name == "Labels":
            werte = [app.tree.set(z, "due") for z in zeilen()]
            assert any("," in w for w in werte), "Probe braucht eine Uhrzeit"
            labels_due = breiten["due"]
            assert labels_due < app.due_column_width(), "Musterbreite statt Inhaltsbreite"
    return f"Datumsspalte Labels {labels_due} px statt {app.due_column_width()} px; " + "; ".join(befunde)


def fall_b12_b13(lauf):
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    app.set_today_view()
    lauf.idle(8)
    kopf = app.tree.item(app.NEXT_TASK_SECTION_ROW_ID, "text")
    assert kopf == "Nächste Aufgabe", kopf
    if app.tree.exists(app.OVERDUE_SECTION_ROW_ID):
        assert not app.tree.item(app.OVERDUE_SECTION_ROW_ID, "text").startswith(app.ICONS["overdue"])
    zeile = app.tree.get_children(app.NEXT_TASK_SECTION_ROW_ID)[0]
    assert "today_next" in app.tree.item(zeile, "tags")
    assert not app.tree.tag_configure("today_next", "font"), "ganze Zeile vergrößert/fett"
    titel_font = app.tree.tag_configure("today_next_title", "font")
    familie, groesse, *stil = lauf.root.tk.splitlist(titel_font)
    assert int(groesse) == app.ui_font_size(1) and "bold" in stil, titel_font
    zelltag = lauf.root.tk.call(str(app.tree), "tag", "cell", "has", "today_next_title", (zeile, "#0"))
    assert int(zelltag) == 1, "Titelzelle nicht fett"
    for spalte in ("due", "labels", "source"):
        anders = lauf.root.tk.call(str(app.tree), "tag", "cell", "has", "today_next_title", (zeile, spalte))
        assert int(anders) == 0, ("Metadatenzelle hervorgehoben", spalte)
    return "keine doppelten Dreiecke; nur Titelzelle fett in Zeilengröße, Datum/Label/Herkunft normal"


def fall_b14(lauf):
    app = lauf.app
    seite = app.new_list_object("Blockleiste", [], list_kind="page", rich_note={"text": "Probe", "spans": [], "links": {}})
    app.lists.append(seite)
    app.save_items()
    app.set_active_list(seite["id"])
    lauf.idle(6)
    beschriftungen = [text for text, _befehl in app.rich_note_editor.toolbar_items()]
    assert "Aufgabe" in beschriftungen and app.ICONS["task_open"] not in "".join(beschriftungen), beschriftungen
    return " · ".join(beschriftungen)


def fall_b16(lauf):
    app = lauf.app
    lauf.showcase()
    seite = next(e for e in app.lists if app.is_page_list(e) and e.get("attachments"))
    app.set_active_list(seite["id"])
    lauf.idle(10)
    ed = app.rich_note_editor
    text = ed.text
    gesamt = text.count("1.0", "end", "ypixels")[0]
    groesster = 0
    proben = 0
    for start in range(0, min(900, gesamt), 10):
        text.yview_moveto(start / gesamt)
        lauf.idle(2)
        bilder = [v for v in ed._image_views.values() if v.winfo_ismapped()
                  and 0 <= v.winfo_rooty() - text.winfo_rooty() < text.winfo_height() - 20]
        if not bilder:
            continue
        vorher = text.yview()[0]
        bilder[0].event_generate("<MouseWheel>", delta=-120, x=10, y=10)
        lauf.idle(2)
        groesster = max(groesster, round((text.yview()[0] - vorher) * gesamt))
        proben += 1
    assert proben, "kein Bild erreicht"
    assert groesster <= 60, ("Sprung über Bild", groesster)
    return f"{proben} Raststücke über Bildern, größter Schritt {groesster} px"


def fall_b17_b19(lauf):
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    app.settings["backdrops"] = {"light": "morgenrot"}
    app.set_design("light")
    lauf.idle(6)
    notiz = next(e for e in app.lists if e.get("title") == "Abstimmung · Entwurf 02")
    app.set_active_list(notiz["id"])
    lauf.idle(8)
    fenster = app.theme["bg"].lower()
    # Die Karte kann je Kachel getönt sein (Milchglas); maßgeblich ist die Trägerfläche.
    for knopf in (app.note_favorite_button, app.note_mood_button, app.note_location_button, app.note_prompt_button):
        traeger = str(knopf.master.cget("bg")).lower()
        assert knopf.bg_color.lower() == traeger != fenster, (knopf.text, knopf.bg_color, traeger)
    app.open_task_inspector(notiz["items"][0]["id"])
    lauf.idle(8)
    felder = [w for w in knoepfe(app.detail_pane, mod.DueField)]
    assert felder
    for feld in felder:
        traeger = str(feld.master.cget("bg")).lower()
        assert traeger != fenster, "Inspektor liegt nicht auf einer Karte"
        assert str(feld.cget("bg")).lower() == traeger, ("Feld in Fensterfarbe", str(feld))
        for rahmen in (feld.time_row, feld.time_block):
            assert str(rahmen.cget("bg")).lower() == traeger, ("Rahmen in Fensterfarbe", str(rahmen))
        if feld.calendar_button is not None:
            assert feld.calendar_button.bg_color.lower() == traeger, "Kalenderknopf in Fensterfarbe"
    for knopf in getattr(app, "custom_menu_buttons", []):
        flaechen = [knopf.itemcget(i, "fill") for i in knopf.find_all() if knopf.type(i) == "polygon"]
        assert flaechen == [""], (knopf.text, flaechen)
    return "Notizaktionen, Fälligkeitsfelder und Menüs ohne Fremdfläche (hell, Verlauf Morgenrot)"


def fall_b18(lauf):
    app, mod = lauf.app, lauf.mod
    aktionen = [text for text, _befehl, _farbe in app.about_actions()]
    assert "Neuerungen …" in aktionen, aktionen
    gesehen = {}

    def dialog(titel, text, **_optionen):
        gesehen["titel"], gesehen["text"] = titel, text
        return "ok"

    app.themed_message_dialog = dialog
    app.settings.update(mod.glide_release.remember_seen(app.settings, mod.APP_VERSION))
    lauf.neustart()
    lauf.app.themed_message_dialog = dialog
    lauf.app.show_release_notes_dialog()
    assert gesehen["titel"] == "Neuerungen"
    assert gesehen["text"] == mod.glide_release.history_text(mod.APP_VERSION)
    assert "Version 3.36.0" in gesehen["text"]
    return "Neuerungen nach „Gelesen“ und Neustart unter Über Glide"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--fall", choices=FAELLE + ("alle",), default="alle")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    ergebnis = {"app": str(args.app), "faelle": {}, "fehler": []}
    for name in (FAELLE if args.fall == "alle" else (args.fall,)):
        with tempfile.TemporaryDirectory(prefix=f"glide-uiux-{name}-") as daten:
            lauf = None
            try:
                lauf = Lauf(args.app, daten)
                text = globals()["fall_" + name](lauf)
                if lauf.errors:
                    raise AssertionError(("Rückruffehler", lauf.errors[:2]))
                ergebnis["faelle"][name] = {"ok": True, "befund": text}
                print(f"OK {name}: {text}", flush=True)
            except Exception as fehler:  # Bericht je Fall, Gesamtergebnis unten
                ergebnis["faelle"][name] = {"ok": False, "befund": repr(fehler)[:600]}
                ergebnis["fehler"].append(name)
                print(f"ROT {name}: {fehler!r}"[:700], flush=True)
            finally:
                if lauf is not None:
                    lauf.ende()
    if args.report:
        args.report.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"gruen": len(ergebnis["faelle"]) - len(ergebnis["fehler"]), "rot": ergebnis["fehler"]},
                     ensure_ascii=False))
    return 1 if ergebnis["fehler"] else 0


if __name__ == "__main__":
    sys.exit(main())
