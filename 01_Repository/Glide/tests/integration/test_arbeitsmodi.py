"""D55 (23.10.2026): Kompaktmodus (E-U1 A), Nebenansicht (E-U2 A) und Seitenbedienung (E-U3 A).

Echte Tk-Wege mit künstlichen Daten: Tastenereignisse, Klicks auf Griff,
Kästchen und Knöpfe, gespeicherte Einstellungen, Neustart, Rückgängig und
Geometrie nach dem appweiten Knopfschutz (B15). `--fall` wählt einzelne Fälle,
`--capture ORDNER` speichert Fensterbilder (nur zur Sichtprüfung, nicht
versioniert). Eine menschliche Sicht-, DPI- und Screenreaderabnahme ersetzt
das nicht.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
from types import SimpleNamespace
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tests/integration"))
from test_uiux_paket import Lauf, knopf_befunde, knoepfe  # noqa: E402

SEITE_MD = ("# Wochenplanung Parkquartier\n\nKurzer Überblick über die offenen Punkte der Woche.\n\n"
            "## Freigaben\n\n- Grundriss Haus B prüfen\n- Fassadenmuster bestellen\n\n"
            "Noch ein Absatz mit etwas längerem Text, damit die Zeile umbricht und der Griff an der ersten "
            "Zeile des Absatzes steht.\n\n### Termine\n\n> Abnahme mit dem Bauherrn am Freitag\n")


TRAEGER = "Trägerfläche"


def befunde_b15(lauf, kontext):
    """Knopfschutz (B15) wie `b15_appweit`; Bildstreifen des Verlaufs sind keine fremden Elemente.

    Im Verlauf malen textlose, per `place` gesetzte Bildlabels die Trägerfläche
    unter Werkzeugleisten (B17/B19). Sie liegen unter den Knöpfen und meldeten
    sich in der Vorversion identisch; alle übrigen Befunde bleiben bestehen.
    """
    for label in knoepfe(lauf.root, lauf.mod.tk.Label):
        try:
            if not label.cget("text") and str(label.cget("image")) and label.winfo_manager() == "place":
                label.text = TRAEGER
        except lauf.mod.tk.TclError:
            pass
    anzahl, funde = knopf_befunde(lauf.root, lauf.mod, kontext)
    return anzahl, [fund for fund in funde if f"„{TRAEGER}“" not in fund]


def idle(lauf, runden=4):
    lauf.idle(runden)


def seite_anlegen(lauf, markdown=SEITE_MD):
    app = lauf.app
    seite = app.new_page_from_markdown(markdown)
    idle(lauf)
    app.set_active_list(seite["id"])
    idle(lauf, 6)
    return seite, app.rich_note_editor


def zeile_mit(text_widget, inhalt):
    letzte = int(text_widget.index("end-1c").split(".")[0])
    return next(i for i in range(1, letzte + 1) if text_widget.get(f"{i}.0", f"{i}.end").strip() == inhalt)


def taste(widget, sequenz, lauf):
    """Tastendruck wie vom Benutzer: Tk leitet Tasten an den Fensterfokus, nicht an `widget`.

    Ohne Fenstermanager folgt der X-Fokus unter Xvfb dem Mauszeiger; ohne
    `focus_force` hinge das Ergebnis von der Bildschirmgröße ab.
    """
    widget.focus_force()
    idle(lauf, 2)
    widget.event_generate(sequenz)
    idle(lauf, 3)


def klick(widget, lauf, x=4, y=4):
    widget.event_generate("<Enter>", x=x, y=y)
    widget.event_generate("<ButtonPress-1>", x=x, y=y)
    widget.event_generate("<ButtonRelease-1>", x=x, y=y)
    # Wie die echte Maus: Verlassen beendet auch den vorgemerkten Tooltip.
    widget.event_generate("<Leave>", x=x, y=y)
    idle(lauf, 3)


def abbauen(lauf):
    """Fall vollständig abbauen; jeder Fall braucht ein eigenes Tk als Standardwurzel.

    Bleibt ein Hauptfenster stehen, binden spätere `StringVar` ohne Master an
    den alten Interpreter, und Eingaben filtern nicht mehr.
    """
    lauf.ende()
    import tkinter
    try:
        if lauf.root.winfo_exists():
            lauf.root.destroy()
    except tkinter.TclError:
        pass
    tkinter._default_root = None


def native_blaetter(lauf, menu):
    """Alle aktiven Blatteinträge eines nativen Menüs als (Pfad, Beschriftung)."""
    sauber = lauf.mod.glide_action_menu.clean_label
    werte = set()
    for _schluessel, beschriftung, pfad, aktiv, _gruppe, art in lauf.app.menu_rows(menu):
        if aktiv and art == "command" and sauber(beschriftung)[0] not in lauf.mod.glide_action_menu.PLACEHOLDER_LABELS:
            werte.add((tuple(sauber(teil)[0] for teil in pfad), sauber(beschriftung)[0]))
    return werte


def chooser_labels(app):
    return [wert.label for wert in app._action_chooser["results"].values()]


def fall_seitenaktionen(lauf):
    """„Mehr“ zeigt alle Einträge des Seitenmenüs durchsuchbar und führt genau sie aus."""
    app, mod = lauf.app, lauf.mod
    _seite, editor = seite_anlegen(lauf)
    nativ = editor.build_page_menu()
    erwartet = native_blaetter(lauf, nativ)
    nativ.destroy()
    mehr = editor._toolbar_buttons["Mehr"]
    klick(mehr, lauf, 10, 10)
    zustand = app._action_chooser
    assert zustand and app.action_chooser_open(), "Auswahl nicht geöffnet"
    gezeigt = {(wert.path, wert.label) for wert in zustand["entries"] if wert.enabled}
    assert erwartet <= gezeigt, ("fehlende Einträge", sorted(erwartet - gezeigt)[:5])
    gesperrt = {wert.label: wert.reason for wert in zustand["entries"] if not wert.enabled}
    assert gesperrt.get("Titelbild entfernen") == mod.glide_action_menu.NO_COVER_REASON, gesperrt
    # Unter „Mehr“ verankert, rechtsbündig, vollständig im Fenster.
    buehne = zustand["stage"]
    assert buehne.winfo_rooty() >= mehr.winfo_rooty() + mehr.winfo_height()
    assert buehne.winfo_rootx() + buehne.winfo_width() <= lauf.root.winfo_rootx() + lauf.root.winfo_width()
    assert lauf.root.focus_get() is zustand["entry"]
    # Inhaberentscheidung 25.10.2026: „Seite“ statt „Markdown“, außer in Formatlisten.
    zustand["entry"].insert(0, "seite")
    idle(lauf)
    treffer = chooser_labels(app)
    assert treffer[:2] == ["Seite aus Zwischenablage einfügen", "Seite kopieren"], treffer
    # Esc schließt ohne Wirkung und gibt den Fokus an die Seite zurück.
    taste(zustand["entry"], "<Escape>", lauf)
    idle(lauf)
    assert not app.action_chooser_open() and lauf.root.focus_get() is editor.text
    vorher = bool(app.settings.get("page_full_width"))
    editor.show_page_actions()
    idle(lauf)
    app._action_chooser["entry"].insert(0, "volle breite")
    idle(lauf)
    assert chooser_labels(app)[0] == "Volle Breite"
    taste(app._action_chooser["entry"], "<Return>", lauf)
    idle(lauf)
    assert bool(app.settings.get("page_full_width")) is not vorher, "Befehl nicht ausgeführt"
    assert not app.action_chooser_open()
    # Gliederung: Sprung über die Auswahl wie über das Menü.
    editor.show_page_actions()
    idle(lauf)
    app._action_chooser["entry"].insert(0, "termine")
    idle(lauf)
    assert chooser_labels(app)[0] == "Termine", chooser_labels(app)
    taste(app._action_chooser["entry"], "<Return>", lauf)
    idle(lauf)
    assert editor.text.index("insert").split(".")[0] == str(zeile_mit(editor.text, "Termine"))
    # Kein Treffer: verständlicher Zustand, Enter ohne Wirkung.
    editor.show_page_actions()
    idle(lauf)
    app._action_chooser["entry"].insert(0, "xyzzy")
    idle(lauf)
    assert app._action_chooser["status"].cget("text") == "Keine passende Aktion"
    taste(app._action_chooser["entry"], "<Return>", lauf)
    idle(lauf)
    assert app.action_chooser_open()
    app.close_action_chooser()
    return f"{len(erwartet)} aktive Seitenmenüeinträge auffindbar; Filter, Esc/Fokus, Ausführen, Gliederung, leere Treffer"


def fall_blockaktionen(lauf):
    """Strg+/ und Griff öffnen dieselben Blockaktionen; ein Undo je Umwandlung."""
    app, mod = lauf.app, lauf.mod
    _seite, editor = seite_anlegen(lauf)
    text = editor.text
    zeile = zeile_mit(text, "• Grundriss Haus B prüfen")
    text.mark_set("insert", f"{zeile}.4")
    taste(text, "<Control-slash>", lauf)
    zustand = app._action_chooser
    assert zustand, "Strg+/ öffnet keine Blockaktionen"
    assert zustand["stage"].nametowidget(zustand["stage"].winfo_children()[0]).winfo_children()[0].cget(
        "text") == "Blockaktionen · Aufzählung"
    eintraege = {wert.label: wert for wert in zustand["entries"]}
    assert eintraege["Aufzählung"].checked and eintraege["Aufzählung"].section == "Umwandeln in"
    assert not eintraege["Kopieren"].enabled and eintraege["Kopieren"].reason == mod.glide_action_menu.SELECTION_REASON
    assert "Blockaktionen suchen …" not in eintraege
    # Reihenfolge: zuerst „Umwandeln in“ (wie Notion), dann die Zeilenaktionen.
    abschnitte = [zustand["tree"].set(iid, "label") for iid in zustand["tree"].get_children()
                  if iid.startswith("group:")]
    assert abschnitte[:2] == ["Umwandeln in", "Zeile"], abschnitte
    tiefe = len(app.undo_stack)
    zustand["entry"].insert(0, "ueberschrift 2")
    idle(lauf)
    assert chooser_labels(app)[0] == "Überschrift 2"
    taste(zustand["entry"], "<Return>", lauf)
    idle(lauf)
    assert "h2" in editor.line_blocks(f"{zeile}.0"), editor.line_blocks(f"{zeile}.0")
    assert len(app.undo_stack) == tiefe + 1, (tiefe, len(app.undo_stack))
    assert lauf.root.focus_get() is text
    # Griff an der Schreibmarke, solange die Seite den Fokus hat.
    absatz = zeile_mit(text, "Kurzer Überblick über die offenen Punkte der Woche.")
    text.mark_set("insert", f"{absatz}.3")
    text.event_generate("<KeyRelease>", keysym="Down")
    idle(lauf)
    griff = editor._block_handle
    assert griff.winfo_ismapped() and editor._block_handle_line == absatz
    box = text.bbox(f"{absatz}.0")
    assert griff.winfo_rootx() + griff.winfo_width() <= text.winfo_rootx() + box[0], "Griff überdeckt den Text"
    mitte_griff = griff.winfo_rooty() + griff.winfo_height() / 2
    mitte_zeile = text.winfo_rooty() + box[1] + box[3] / 2
    assert abs(mitte_griff - mitte_zeile) <= 4, (mitte_griff, mitte_zeile)
    # Tippen beruhigt die Zeile; Mausbewegung über einer anderen Zeile versetzt den Griff.
    text.event_generate("<KeyPress>", keysym="a")
    idle(lauf)
    assert not griff.winfo_ismapped(), "Tippen blendet den Griff aus"
    lange = zeile_mit(text, "Noch ein Absatz mit etwas längerem Text, damit die Zeile umbricht und der Griff an der "
                            "ersten Zeile des Absatzes steht.")
    x, y, _b, h = text.bbox(f"{lange}.10")
    text.event_generate("<Motion>", x=x, y=y + h // 2)
    idle(lauf)
    assert griff.winfo_ismapped() and editor._block_handle_line == lange
    erste = text.bbox(f"{lange}.0")
    assert abs((griff.winfo_rooty() + griff.winfo_height() / 2) - (text.winfo_rooty() + erste[1] + erste[3] / 2)) <= 4
    # Klick auf den Griff: Schreibmarke auf die Zeile, Auswahl daneben.
    griff.event_generate("<Button-1>", x=3, y=3)
    idle(lauf)
    assert app.action_chooser_open() and text.index("insert").split(".")[0] == str(lange)
    buehne = app._action_chooser["stage"]
    assert buehne.winfo_rootx() >= griff.winfo_rootx() + griff.winfo_width()
    app._action_chooser["entry"].insert(0, "zitat")
    idle(lauf)
    taste(app._action_chooser["entry"], "<Return>", lauf)
    idle(lauf)
    assert "quote" in editor.line_blocks(f"{lange}.0")
    app.undo_last_change()
    idle(lauf)
    editor = app.rich_note_editor
    assert "quote" not in editor.line_blocks(f"{lange}.0"), "Undo nimmt die Umwandlung zurück"
    # Rechtsklickmenü nennt den Weg; das Menü selbst bleibt nativ.
    menus = []
    editor.popup = menus.append
    editor.show_context_menu(None)
    labels = [menus[0].entrycget(i, "label") for i in range(menus[0].index("end") + 1) if menus[0].type(i) != "separator"]
    assert "Blockaktionen suchen …" in labels and "Umwandeln in" in labels
    return "Strg+/, Griff an Schreibmarke und Mauszeiger, Umwandeln mit einem Undo, Sperrgründe, Rechtsklick nennt den Weg"


def fall_schreibschutz(lauf):
    """Schreibgeschützter Bestand: Aktionen sichtbar, Änderungen gesperrt mit Grund; keine Kopfverweise."""
    app, mod = lauf.app, lauf.mod
    _seite, editor = seite_anlegen(lauf)
    app._data_read_only = True
    editor.refresh_page_head()
    idle(lauf)
    assert not editor._head_signature and not editor._head_row.winfo_manager()
    zeile = zeile_mit(editor.text, "• Fassadenmuster bestellen")
    editor.text.mark_set("insert", f"{zeile}.2")
    editor.show_block_actions()
    idle(lauf)
    werte = {wert.label: wert for wert in app._action_chooser["entries"]}
    assert not werte["Aufgabe verknüpfen …"].enabled
    assert werte["Aufgabe verknüpfen …"].reason == mod.glide_action_menu.READ_ONLY_REASON
    app.close_action_chooser()
    editor.show_page_actions()
    idle(lauf)
    werte = {wert.label: wert for wert in app._action_chooser["entries"]}
    assert not werte["Pixelsymbol …"].enabled
    app.close_action_chooser()
    app._data_read_only = False
    return "Lesbare Aktionen bleiben, Änderungen gesperrt mit Grund, keine Kopfverweise"


def fall_kopfverweise(lauf):
    """Ruhiger Seitenkopf: reservierter Platz am Ende der Titelzeile, Überfahren/Fokus, Symbol vor dem Titel."""
    app, mod = lauf.app, lauf.mod
    seite, editor = seite_anlegen(lauf)
    titel = editor.title_label
    zeile = editor._head_row
    assert editor._head_signature == ("icon", "cover")
    knoepfe_ = editor._head_buttons
    assert not zeile.winfo_manager() and not any(k.winfo_ismapped() for k in knoepfe_.values()), "in Ruhe verborgen"
    # Keine zusätzliche Bedienzeile und kein früherer Umbruch: Der Titel bleibt, wie er ohne Verweise wäre.
    oben = titel.winfo_rooty()
    umbruch = int(float(titel.cget("wraplength")))
    assert editor._head_fits, "kurzer Titel lässt Platz für die Verweise"
    titel.event_generate("<Enter>")
    idle(lauf)
    assert all(k.winfo_ismapped() for k in knoepfe_.values())
    assert titel.winfo_rooty() == oben, "Der Titel verschiebt sich nicht"
    # Rechtsbündig zur Lesespalte, auf der Mitte der ersten Titelzeile (B02/B07).
    letzter = knoepfe_["cover"]
    assert abs(letzter.winfo_rootx() + letzter.winfo_width() - (titel.winfo_rootx() + titel.winfo_width())) <= 2
    linie = mod.tkfont.Font(font=titel.cget("font")).metrics("linespace")
    for knopf in knoepfe_.values():
        mitte = knopf.winfo_rooty() + knopf.winfo_height() / 2
        assert abs(mitte - (titel.winfo_rooty() + linie / 2)) <= 3, (mitte, titel.winfo_rooty(), linie)
    assert knoepfe_["icon"].winfo_rootx() + knoepfe_["icon"].winfo_width() < letzter.winfo_rootx()
    anzahl, befunde = befunde_b15(lauf, "Seitenkopf 1280x800")
    assert not befunde, befunde[:4]
    titel.event_generate("<Leave>")
    idle(lauf)
    # Mauszeiger außerhalb des Kopfes, ohne den echten Zeiger zu bewegen (kein `warp`):
    # Unter Windows liefe die Prüfung sonst dem Benutzer über den Bildschirm.
    editor.winfo_pointerx = editor.winfo_pointery = lambda: -10000
    editor.page_head_check()
    del editor.winfo_pointerx, editor.winfo_pointery
    idle(lauf)
    assert not any(k.winfo_ismapped() for k in knoepfe_.values())
    # Tastatur: Fokus auf dem Titel zeigt die Verweise; Tab erreicht sie.
    titel.focus_force()
    idle(lauf)
    assert all(k.winfo_ismapped() for k in knoepfe_.values())
    assert titel.tk_focusNext() is knoepfe_["icon"], titel.tk_focusNext()
    # Langer Titel: Die Verweise weichen ganz (kein früherer Umbruch) und bleiben über „Mehr“ erreichbar.
    eintrag = app.page_entry(seite["id"])
    eintrag["title"] = "Sehr lange Seitenüberschrift für die Abstimmung der Fassadenmuster im Parkquartier Haus B"
    editor.refresh_page_head()
    idle(lauf)
    assert not editor._head_fits and not zeile.winfo_manager()
    assert int(float(titel.cget("wraplength"))) == umbruch, "der Titel bricht nicht wegen der Verweise um"
    titel.event_generate("<Enter>")
    idle(lauf)
    assert not any(k.winfo_ismapped() for k in knoepfe_.values())
    nativ = editor.build_page_menu()
    eintraege = native_blaetter(lauf, nativ) | {((), l) for _k, l, p, a, _g, art in app.menu_rows(nativ) if not p}
    nativ.destroy()
    assert ((), "Pixelsymbol …") in eintraege, sorted(eintraege)[:8]
    assert any(pfad[:1] == ("Titelbild",) for pfad, _l in eintraege), "Titelbild über Mehr"
    titel.event_generate("<Leave>")
    idle(lauf)
    # Schmale Spalte (860 × 700): ebenfalls kein Platz, nichts verschoben.
    eintrag["title"] = "Wochenplanung Parkquartier"
    editor.refresh_page_head()
    lauf.root.geometry("860x700+20+20")
    idle(lauf, 8)
    if titel.winfo_manager():
        breite_spalte = editor.text.winfo_width() - 2 * (editor._read_pad or 28)
        bedarf = mod.tkfont.Font(font=titel.cget("font")).measure(titel.cget("text"))
        assert editor._head_fits == (bedarf + editor.HEAD_ACTION_GAP + editor.page_head_width() <= breite_spalte)
    lauf.root.geometry("1280x800+20+20")
    idle(lauf, 8)
    # Pixelsymbol gesetzt: steht vor dem Titel, nur noch „Titelbild hinzufügen“.
    eintrag["title"] = "Wochenplanung Parkquartier"
    eintrag["icon"] = mod.glide_drawing.DrawingModel.blank(app.PAGE_ICON_SIZE).to_document()
    editor.refresh_page_head()
    idle(lauf)
    assert editor._title_icon is not None and str(titel.cget("image"))
    assert titel.cget("text").strip() == eintrag["title"]
    assert editor._head_signature == ("cover",)
    aufrufe = []
    editor.choose_page_icon = lambda: aufrufe.append("symbol") or "break"
    titel.event_generate("<Button-1>", x=4, y=4)
    idle(lauf)
    assert aufrufe == ["symbol"], "Klick aufs Symbol ändert es"
    umbenennen = []
    editor.rename_page = lambda: umbenennen.append(True)
    titel.event_generate("<Button-1>", x=editor._title_icon.width() + 40, y=4)
    idle(lauf)
    assert umbenennen, "Klick auf den Titel benennt um"
    # Mit Titelbild und Symbol: nichts reserviert, Titel nutzt die ganze Spalte.
    eintrag["cover"] = {"kind": "drawing", "document": eintrag["icon"]}
    editor.refresh_page_head()
    idle(lauf)
    assert editor._head_signature == () and editor.page_head_width() == 0 and not zeile.winfo_manager()
    return (f"keine Zusatzzeile, Verweise am Titelende nur bei freiem Platz, Überfahren/Fokus/Tab, langer Titel "
            f"und schmale Spalte weichen ganz (Mehr), Symbol vor dem Titel, {anzahl} Knöpfe ohne Befund")


def fall_notiz(lauf):
    """Notizen: eigene Notizaktionen, derselbe Griff und dieselben Blockaktionen."""
    app = lauf.app
    notiz = app.new_list_object("Besprechung Bauherr", [], list_kind=app.LIST_KIND_NOTE) \
        if "list_kind" in app.new_list_object.__code__.co_varnames else app.new_list_object("Besprechung Bauherr", [])
    notiz["list_kind"] = app.LIST_KIND_NOTE
    notiz["rich_note"] = {"text": "Protokoll\nOffene Fragen zur Fassade", "spans": [], "links": {}}
    app.lists.append(notiz)
    assert app.save_items()
    app.set_active_list(notiz["id"])
    idle(lauf, 6)
    editor = app.rich_note_editor
    assert type(editor).__name__ == "NoteEditor"
    editor.show_page_actions()
    idle(lauf)
    zustand = app._action_chooser
    abschnitte = {wert.section for wert in zustand["entries"]}
    assert {"Notiz", "Einfügen", "Präsentieren"} <= abschnitte, abschnitte
    assert zustand["stage"].winfo_children()[0].winfo_children()[0].cget("text") == "Notizaktionen"
    app.close_action_chooser()
    editor.text.mark_set("insert", "2.3")
    taste(editor.text, "<Control-slash>", lauf)
    assert app.action_chooser_open()
    app.close_action_chooser()
    editor.show_block_handle("insert", "focus")
    idle(lauf)
    assert editor._block_handle.winfo_ismapped()
    return "Notizaktionen mit eigenen Abschnitten, Blockaktionen und Griff wie in Seiten"


def bestand(lauf):
    app = lauf.app
    punkte = [app.new_item(text) for text in ("Statik Haus B prüfen", "Gerüstbau beauftragen",
                                               "Fassadenmuster freigeben")]
    punkte[1]["due"] = "2026-10-30"
    liste = app.new_list_object("Bauleitung Parkquartier", punkte)
    app.lists.append(liste)
    assert app.save_items()
    seite, _editor = seite_anlegen(lauf)
    return liste, punkte, seite


def seitenbaum(app):
    return app.side_pane.nametowidget(str(app._side_view_body))


def fall_nebenansicht_liste(lauf):
    """Liste neben einer Seite: abhaken mit einem Undo, Umbenennen, Papierkorb, Öffnen."""
    app = lauf.app
    liste, punkte, seite = bestand(lauf)
    assert app.open_side_view(liste["id"])
    idle(lauf, 5)
    assert app.side_pane.winfo_ismapped() and app.side_pane.winfo_width() == app.side_view_width()
    # Die Seite bleibt bedienbar und rückt nach links; nichts überlappt.
    editor = app.rich_note_editor
    assert editor.winfo_ismapped()
    assert editor.winfo_rootx() + editor.winfo_width() <= app.side_pane.winfo_rootx()
    baum = seitenbaum(app)
    zeilen = list(baum.get_children())
    assert zeilen == [p["id"] for p in punkte], zeilen
    assert baum.set(punkte[1]["id"], "due"), "Fälligkeit sichtbar"
    tiefe = len(app.undo_stack)
    x, y, _w, h = baum.bbox(punkte[0]["id"])
    baum.event_generate("<Button-1>", x=26, y=y + h // 2)
    idle(lauf, 5)
    assert app.find_item_in_lists(punkte[0]["id"])[0]["done"], "Kästchen hakt ab"
    assert len(app.undo_stack) == tiefe + 1
    baum = seitenbaum(app)
    assert app.ICONS["check"] in baum.item(punkte[0]["id"], "text")
    # Klick auf den Text hakt nicht ab.
    x, y, _w, h = baum.bbox(punkte[2]["id"])
    baum.event_generate("<Button-1>", x=x + 200, y=y + h // 2)
    idle(lauf, 3)
    assert not app.find_item_in_lists(punkte[2]["id"])[0].get("done")
    app.undo_last_change()
    idle(lauf, 5)
    assert not app.find_item_in_lists(punkte[0]["id"])[0].get("done")
    assert app.ICONS["task_open"] in seitenbaum(app).item(punkte[0]["id"], "text"), "Undo erreicht die Nebenansicht"
    app.redo_last_change()
    idle(lauf, 5)
    assert app.find_item_in_lists(punkte[0]["id"])[0]["done"]
    # Leertaste auf der Auswahl.
    baum = seitenbaum(app)
    baum.focus_force(); baum.selection_set(punkte[2]["id"]); baum.focus(punkte[2]["id"])
    taste(baum, "<space>", lauf)
    idle(lauf, 5)
    assert app.find_item_in_lists(punkte[2]["id"])[0]["done"]
    # Umbenennen der Liste erscheint nebenan.
    eintrag = next(e for e in app.lists if e["id"] == liste["id"])
    with app.sidebar_change() as change:
        eintrag["title"] = "Bauleitung Haus B"
        change.mark()
    idle(lauf, 5)
    texte = [w.cget("text") for w in knoepfe(app.side_pane, lauf.mod.tk.Label)]
    assert "Bauleitung Haus B" in texte, texte
    # Papierkorb: verständlicher Zustand, kein Öffnen-Knopf; Wiederherstellen zeigt den Inhalt.
    app.ask_yes_no = lambda *_a, **_k: True
    app.delete_list_by_id(liste["id"])
    idle(lauf, 5)
    texte = " ".join(w.cget("text") for w in knoepfe(app.side_pane, lauf.mod.tk.Label))
    assert "Papierkorb" in texte, texte
    beschriftungen = [k.text for k in knoepfe(app.side_pane, lauf.mod.RoundedButton)]
    assert beschriftungen == ["Schließen"], beschriftungen
    app.undo_last_change()
    idle(lauf, 5)
    beschriftungen = [k.text for k in knoepfe(app.side_pane, lauf.mod.RoundedButton)]
    assert "Öffnen" in beschriftungen
    # Öffnen: Inhalt im Hauptbereich, Nebenansicht zu, Auswahl erhalten.
    oeffnen = next(k for k in knoepfe(app.side_pane, lauf.mod.RoundedButton) if k.text == "Öffnen")
    oeffnen.command()
    idle(lauf, 5)
    assert app.active_list_id == liste["id"] and not app.side_view_open() and not app.side_pane.winfo_ismapped()
    return "Abhaken per Kästchen/Leertaste mit einem Undo/Redo, Text klickt nicht, Umbenennen, Papierkorb, Öffnen"


def fall_nebenansicht_seite(lauf):
    """Seite neben einer Liste: Blockarten, echtes Aufgabenkästchen, Bildzeile, Esc schließt."""
    app = lauf.app
    liste, punkte, seite = bestand(lauf)
    editor = app.rich_note_editor
    # Eine echte Aufgabe in der Seite.
    editor.text.mark_set("insert", "end")
    editor.text.insert("end", "\nAngebot Gerüstbau vergleichen")
    editor.text.mark_set("insert", "end-1c")
    editor.set_block("task")
    editor.flush()
    idle(lauf)
    eintrag = app.page_entry(seite["id"])
    aufgabe = next(iter(lauf.mod.glide_task_refs.document_ids(eintrag["rich_note"])))
    app.set_active_list(liste["id"])
    idle(lauf, 5)
    assert app.open_side_view(seite["id"])
    idle(lauf, 5)
    text = seitenbaum(app)
    assert isinstance(text, lauf.mod.tk.Text) and str(text.cget("state")) == "disabled"
    inhalt = text.get("1.0", "end")
    assert "Kurzer Überblick" in inhalt and "Abnahme mit dem Bauherrn" in inhalt
    titel = [w.cget("text") for w in knoepfe(app.side_pane, lauf.mod.tk.Label)]
    assert "Wochenplanung Parkquartier" in titel, titel
    zweite = zeile_mit(text, "Freigaben")
    assert "h2" in text.tag_names(f"{zweite}.0")
    assert "bullet" in text.tag_names(f"{zeile_mit(text, '• Grundriss Haus B prüfen')}.0")
    zitat = zeile_mit(text, "Abnahme mit dem Bauherrn am Freitag")
    assert "quote" in text.tag_names(f"{zitat}.0")
    marken = [w for w in text.winfo_children() if isinstance(w, lauf.mod.tk.Label)
              and w.cget("text") in (app.ICONS["task_open"], app.ICONS["check"])]
    assert len(marken) == 1
    tiefe = len(app.undo_stack)
    marken[0].event_generate("<Button-1>")
    idle(lauf, 5)
    assert app.find_item_in_lists(aufgabe)[0]["done"] and len(app.undo_stack) == tiefe + 1
    text = seitenbaum(app)
    marken = [w for w in text.winfo_children() if isinstance(w, lauf.mod.tk.Label)
              and w.cget("text") == app.ICONS["check"]]
    assert marken, "Erledigt-Zustand nach dem Neuaufbau"
    # Esc in der Nebenansicht schließt sie; Hauptbereich bleibt.
    text.focus_force()
    idle(lauf)
    taste(text, "<Escape>", lauf)
    idle(lauf, 3)
    assert not app.side_view_open() and app.active_list_id == liste["id"]
    return "Blockarten, echtes Kästchen mit einem Undo, lesend gesperrt, Esc schließt"


def fall_nebenansicht_inspektor(lauf):
    """Gleicher Platz wie der Aufgabeninspektor: Vorrang, Rückkehr, schmales Fenster."""
    app = lauf.app
    liste, punkte, seite = bestand(lauf)
    app.set_active_list(liste["id"])
    idle(lauf, 4)
    app.settings["detail_pane"] = True
    app.tree.selection_set(punkte[0]["id"]); app.tree.focus(punkte[0]["id"])
    app.sync_detail_pane(force=True)
    idle(lauf, 4)
    assert app.detail_pane.winfo_ismapped(), "automatischer Inspektor"
    assert app.open_side_view(seite["id"])
    idle(lauf, 5)
    assert app.side_pane.winfo_ismapped() and not app.detail_pane.winfo_ismapped(), "Nebenansicht hat Vorrang"
    assert app.open_task_inspector(punkte[1]["id"])
    idle(lauf, 5)
    assert app.detail_pane.winfo_ismapped() and not app.side_pane.winfo_ismapped(), "ausdrücklicher Inspektor"
    app.close_task_inspector()
    idle(lauf, 5)
    assert app.side_pane.winfo_ismapped(), "Nebenansicht kehrt zurück"
    # Schmales Fenster: über der Inhaltsfläche wie der Inspektor, Schließen bleibt erreichbar.
    lauf.root.geometry("900x700+20+20")
    idle(lauf, 8)
    app.sync_side_view(force=True)
    idle(lauf, 4)
    assert app._side_narrow and app.side_pane.winfo_ismapped()
    schliessen = next(k for k in knoepfe(app.side_pane, lauf.mod.RoundedButton) if k.text == "Schließen")
    assert schliessen.winfo_ismapped()
    anzahl, befunde = befunde_b15(lauf, "Nebenansicht 900x700")
    assert not befunde, befunde[:4]
    schliessen.command()
    idle(lauf, 5)
    assert not app.side_view_open() and app.list_frame_outer.winfo_ismapped()
    app.settings["detail_pane"] = False
    return f"Vorrang und Rückkehr gegenüber dem Inspektor, schmal als Überlagerung, {anzahl} Knöpfe ohne Befund"


def fall_nebenansicht_einstiege(lauf):
    """Seitenleiste, Suche mit Umschalt+Enter, eigene Auswahl; Zeichnung nur über Öffnen."""
    app = lauf.app
    liste, punkte, seite = bestand(lauf)
    menu = app.build_list_menu(liste["id"])
    labels = {menu.entrycget(i, "label"): i for i in range(menu.index("end") + 1) if menu.type(i) == "command"}
    assert "In Nebenansicht öffnen" in labels
    menu.invoke(labels["In Nebenansicht öffnen"])
    idle(lauf, 5)
    assert app._side_view == {"kind": "list", "id": liste["id"]}
    app.close_side_view()
    zeichnung = app.new_list_object("Fassade Skizze", [])
    zeichnung["list_kind"] = app.LIST_KIND_DRAWING
    app.lists.append(zeichnung)
    menu = app.build_list_menu(zeichnung["id"])
    stelle = next(i for i in range(menu.index("end") + 1) if menu.type(i) == "command"
                  and menu.entrycget(i, "label") == "In Nebenansicht öffnen")
    assert menu.entrycget(stelle, "state") == "disabled"
    assert not app.open_side_view(zeichnung["id"])
    # Suche: Umschalt+Enter auf einer Liste.
    app.show_quick_open()
    idle(lauf)
    eingabe = app._quick_open["entry"]
    eingabe.insert(0, "Bauleitung")
    idle(lauf)
    eingabe.focus_force()
    taste(eingabe, "<Shift-Return>", lauf)
    idle(lauf, 5)
    assert app._quick_open is None and app._side_view == {"kind": "list", "id": liste["id"]}
    # Eigene Auswahl zeigt nur Listen, Seiten und Notizen.
    app.choose_side_view()
    idle(lauf)
    eingabe = app._quick_open["entry"]
    eingabe.insert(0, "Heute")
    idle(lauf)
    arten = {(wert.get("target") or ("",))[0] for wert in app._quick_open["results"]}
    assert arten <= {"list"}, arten
    app.close_quick_open()
    app.close_side_view()
    return "Kontextmenü, Zeichnung gesperrt, Umschalt+Enter, eigene Auswahl nur mit Listen/Seiten/Notizen"


def verweisbestand(lauf):
    app, mod = lauf.app, lauf.mod
    liste, punkte, zielseite = bestand(lauf)
    editor = app.rich_note_editor
    editor.text.insert('end', '\nVerlinkte Seitenaufgabe')
    editor.text.mark_set('insert', 'end-1c')
    editor.set_block('task')
    assert editor.flush()
    idle(lauf)
    page_task = next(iter(mod.glide_task_refs.document_ids(app.page_entry(zielseite['id'])['rich_note'])))
    quelle, editor = seite_anlegen(lauf, '# Hauptarbeit\n\nDieser Kontext bleibt offen.\n')
    values = [mod.glide_objects.uri('list', zielseite['id']),
              mod.glide_objects.uri('item', punkte[1]['id']), mod.glide_objects.uri('item', page_task)]
    for value in values:
        editor.text.mark_set('insert', 'end-1c')
        editor.text.insert('insert', '\n')
        editor.insert_object_reference(value)
    idle(lauf)
    assert app.save_items()
    return liste, punkte, zielseite, page_task, quelle, editor, values


def verweis_position(editor, value, lauf):
    tag = next(tag for tag, target in editor.links.items() if target == value)
    position = editor.text.tag_ranges(tag)[0]
    editor.text.see(position)
    idle(lauf)
    box = editor.text.bbox(position)
    assert box, (value, position)
    return box[0] + 2, box[1] + 2


def menustelle(menu, label):
    return next(i for i in range((menu.index('end') or 0) + 1)
                if menu.type(i) in ('command', 'cascade') and menu.entrycget(i, 'label') == label)


def fall_verweisvorschau(lauf):
    app, mod = lauf.app, lauf.mod
    liste, punkte, zielseite, page_task, quelle, editor, values = verweisbestand(lauf)
    before, disk, depth = copy.deepcopy(app.lists), Path(mod.SAVE_FILE).read_bytes(), len(app.undo_stack)
    editor.text.focus_force(); idle(lauf)
    x, y = verweis_position(editor, values[0], lauf)
    editor.text.event_generate('<Control-Shift-Button-1>', x=x, y=y)
    idle(lauf, 5)
    assert app.side_view_entry()['id'] == zielseite['id']
    assert app.active_list_id == quelle['id'] and app.rich_note_editor is editor
    assert app.lists == before and Path(mod.SAVE_FILE).read_bytes() == disk and len(app.undo_stack) == depth
    taste(seitenbaum(app), '<Escape>', lauf)
    assert not app.side_view_open() and app.active_list_id == quelle['id']

    # Ein Rechtsklick innerhalb einer Auswahl verwendet das Ziel unter dem
    # Zeiger, auch wenn die Einfügemarke auf einer anderen Zeile steht.
    x, y = verweis_position(editor, values[1], lauf)
    editor.text.tag_add('sel', '1.0', 'end-1c')
    editor.text.mark_set('insert', '1.0')
    menus = []
    with patch.object(editor, 'popup', side_effect=menus.append):
        editor.show_context_menu(SimpleNamespace(x=x, y=y))
    menu = menus[-1]
    menu.invoke(menustelle(menu, 'Verweis in Nebenansicht öffnen'))
    idle(lauf, 5)
    tree = seitenbaum(app)
    assert isinstance(tree, mod.ttk.Treeview) and tree.selection() == (punkte[1]['id'],)
    assert app.active_list_id == quelle['id'] and app.rich_note_editor is editor
    assert app.lists == before and len(app.undo_stack) == depth

    # Das vorhandene Verweismenü enthält ausgehende und eingehende Ziele;
    # sein alter Callback löst nach Objektaustausch die aktuelle ID auf.
    app.page_entry(zielseite['id'])['references'] = [mod.glide_objects.uri('list', quelle['id'])]
    graph_menu = app.build_object_reference_menu(('list', quelle['id']))
    preview = graph_menu.nametowidget(graph_menu.entrycget(menustelle(graph_menu, 'In Nebenansicht öffnen'), 'menu'))
    target_index = menustelle(preview, mod.glide_objects.caption(('list', zielseite['id']), app.object_graph()[0])[1])
    replacement = copy.deepcopy(app.page_entry(zielseite['id']))
    replacement['title'] = 'Aktueller Titel nach Objektaustausch'
    app.lists = [replacement if entry['id'] == zielseite['id'] else entry for entry in app.lists]
    preview.invoke(target_index)
    idle(lauf, 5)
    assert app.side_view_entry() is replacement
    assert any(w.cget('text') == replacement['title'] for w in knoepfe(app.side_pane, mod.tk.Label))
    assert app.active_list_id == quelle['id']
    assert app.open_object_reference(values[2], side=True)
    idle(lauf, 4)
    text = seitenbaum(app)
    ranges = text.tag_ranges('reference_target')
    assert ranges and 'Verlinkte Seitenaufgabe' in text.get(*ranges[:2])
    assert str(text.cget('state')) == 'disabled'

    # Vorhandener Haupteditor samt noch nicht übernommenem Text bleibt.
    editor.text.tag_remove('sel', '1.0', 'end')
    editor.text.insert('end-1c', '\nNoch nicht abgeschlossener Absatz')
    assert app.open_object_reference(values[0], side=True)
    assert app.rich_note_editor is editor and 'Noch nicht abgeschlossener Absatz' in editor.text.get('1.0', 'end')
    idle(lauf)
    # Der bisherige Strg-Klick öffnet weiter im Hauptbereich.
    app.close_side_view()
    x, y = verweis_position(editor, values[0], lauf)
    with patch.object(app, 'open_object_reference', wraps=app.open_object_reference) as opened:
        editor.text.event_generate('<Control-Button-1>', x=x, y=y)
        idle(lauf, 5)
        assert app.active_list_id == zielseite['id'], (app.active_list_id, zielseite['id'], opened.call_args)
    return 'Echter Strg+Umschalt-Klick, Kontext unter Auswahl, Verweis-/Rückverweismenü, frische IDs/Titel, Taskmarkierung in Liste/Seite, Haupteditor und offener Text erhalten; alter Strg-Klick bleibt'


def fall_verweisvorschau_grenzen(lauf):
    app, mod = lauf.app, lauf.mod
    liste, punkte, zielseite, page_task, quelle, editor, values = verweisbestand(lauf)
    # Derselbe neue Textweg funktioniert im Notizeditor.
    note = app.new_list_object('Notiz mit Verweis', [])
    note['list_kind'] = app.LIST_KIND_NOTE
    note['rich_note'] = {'text': 'Nachschlagen', 'links': {'link:probe': values[0]},
                         'spans': [{'tag': 'link:probe', 'start': 0, 'end': 12}]}
    app.lists.append(note); assert app.save_items()
    app.set_active_list(note['id']); idle(lauf, 5)
    editor = app.rich_note_editor
    x, y = verweis_position(editor, values[0], lauf)
    editor.text.event_generate('<Control-Shift-Button-1>', x=x, y=y)
    idle(lauf)
    assert app.active_list_id == note['id'] and app.side_view_entry()['id'] == zielseite['id']
    # Externe Adressen werden vom Vorschaukürzel nicht geöffnet.
    editor.text.configure(state='normal')
    editor.text.insert('end-1c', '\nExtern', ('link:extern',))
    editor.links['link:extern'] = 'https://example.invalid/'
    assert editor.flush()  # Fixture abschließen, bevor Undo der Aufgabenaktion geprüft wird.
    idle(lauf)
    x, y = verweis_position(editor, editor.links['link:extern'], lauf)
    with patch('webbrowser.open') as browser:
        editor.text.event_generate('<Control-Shift-Button-1>', x=x, y=y)
        idle(lauf)
        browser.assert_not_called()
    app.page_entry(zielseite['id'])['archived'] = True
    app._data_read_only = True
    try:
        assert app.open_object_reference(values[0], side=True)
        idle(lauf)
        assert str(seitenbaum(app).cget('state')) == 'disabled'
        assert app.active_list_id == note['id']
    finally:
        app._data_read_only = False
    app.open_object_reference(values[1], side=True); idle(lauf)
    app.toggle_side_view_task(punkte[1]['id']); idle(lauf)
    assert app.find_item_in_lists(punkte[1]['id'])[0]['done']
    app.undo_last_change(); idle(lauf)
    assert not app.find_item_in_lists(punkte[1]['id'])[0]['done']
    assert app.open_object_reference(values[1], side=True)
    assert seitenbaum(app).selection() == (punkte[1]['id'],)
    # Bereits gebautes Menü, danach Papierkorb: Callback muss erneut prüfen.
    menu = app.build_object_reference_menu(('list', quelle['id']))
    preview = menu.nametowidget(menu.entrycget(menustelle(menu, 'In Nebenansicht öffnen'), 'menu'))
    label = mod.glide_objects.caption(('list', zielseite['id']), app.object_graph()[0])[1]
    stale_index = menustelle(preview, label)
    deleted = app.page_entry(zielseite['id'])
    app.lists = [entry for entry in app.lists if entry['id'] != zielseite['id']]
    app.trash.append(app.new_trash_entry(app.TRASH_KIND_LIST, deleted))
    with patch.object(app, 'show_warning') as warning:
        preview.invoke(stale_index)
        idle(lauf, 4)
        assert warning.called, (preview.entrycget(stale_index, 'state'),
                                mod.glide_objects.caption(('list', zielseite['id']), app.object_graph()[0]),
                                lauf.errors)
    assert app.side_view_entry()['id'] == liste['id']
    for value in (mod.glide_objects.uri('list', 'fehlt'), mod.glide_objects.uri('item', 'fehlt')):
        with patch.object(app, 'show_warning'):
            assert app.open_object_reference(value, side=True) is False
    drawing = app.new_list_object('Kein Vorschauziel', []); drawing['list_kind'] = 'drawing'; app.lists.append(drawing)
    assert app.open_object_reference(mod.glide_objects.uri('list', drawing['id']), side=True) is False
    app.toggle_compact_mode(); idle(lauf)
    assert app.open_object_reference(values[1], side=True) is False
    app.toggle_compact_mode(); idle(lauf)
    count = 0
    for geometry in ('860x700', '1280x800'):
        for font in ('mittel', 'gross'):
            for design in ('light', 'dark'):
                app.settings['ui_font_size'] = font
                app.set_design(design, apply_now=False); app.apply_ui_font(); app.apply_theme()
                lauf.root.geometry(geometry); idle(lauf)
                assert app.open_object_reference(values[1], side=True)
                idle(lauf)
                n, errors = befunde_b15(lauf, f'Verweisvorschau {geometry}/{font}/{design}')
                assert not errors, errors
                count += n
    return f'Notiz, kein externer Browser, Archiv/Schreibschutz, Undo/frische IDs, stale Menü/Papierkorb/fehlend/Zeichnung/Kompaktmodus; {count} Knopfprüfungen in acht Konfigurationen'


def fall_seitenleiste_kontext(lauf):
    """Rechtsklick wählt das Menü-Ziel, ohne den Hauptinhalt auszutauschen."""
    app = lauf.app
    liste, _punkte, seite = bestand(lauf)
    zweite = app.new_list_object("Zweite Bauliste", [])
    notiz = app.new_list_object("Baunotiz", [], list_kind="note")
    zeichnung = app.new_list_object("Bauskizze", [], list_kind="drawing")
    ordner = app.new_folder_object("Bauordner")
    app.lists.extend((zweite, notiz, zeichnung))
    app.folders.append(ordner)
    assert app.save_items()
    app.update_sidebar_list()
    idle(lauf)

    def kontext(row):
        iid = app.get_sidebar_iid_for_row(row)
        baum = app.get_sidebar_tree_for_iid(iid)
        baum.see(iid)
        idle(lauf)
        x, y, breite, hoehe = baum.bbox(iid)
        vorher = (app.view_mode, app.active_list_id, app.active_folder_id)
        waehrend = []

        def zeigen(menu, *_args):
            # Die native Windows-Menüsitzung ist nicht per Tk-after steuerbar.
            # Nur die Darstellung ersetzen; echte Auswahlereignisse verarbeiten.
            idle(lauf)
            waehrend.append((app.view_mode, app.active_list_id, app.active_folder_id))

        original = lauf.mod.tk.Menu.tk_popup
        lauf.mod.tk.Menu.tk_popup = zeigen
        try:
            baum.event_generate("<Button-3>", x=x + min(60, breite // 2), y=y + hoehe // 2)
        finally:
            lauf.mod.tk.Menu.tk_popup = original
        idle(lauf)
        assert waehrend == [vorher], ("Rechtsklick öffnet den Hauptinhalt", row, vorher, waehrend)
        assert (app.view_mode, app.active_list_id, app.active_folder_id) == vorher
        assert iid in baum.selection(), ("Menüziel nicht ausgewählt", row)
        assert baum.focus() == iid
        menu = app._sidebar_context_menu
        assert menu is not None, ("Kontextmenü fehlt", row)
        return baum, iid, menu

    # Gerade dieser Weg darf die offene Seite und ihren Editor nicht ersetzen.
    editor = app.rich_note_editor
    baum, iid, menu = kontext(("list", liste["id"]))
    assert app.rich_note_editor is editor and editor.winfo_ismapped()
    stelle = next(i for i in range(menu.index("end") + 1) if menu.type(i) == "command"
                  and menu.entrycget(i, "label") == "In Nebenansicht öffnen")
    menu.invoke(stelle)
    idle(lauf)
    assert app.active_list_id == seite["id"] and app._side_view["id"] == liste["id"]
    app.close_side_view()
    # Ein Linksklick auf dieselbe, bereits per Rechtsklick ausgewählte Zeile öffnet.
    x, y, breite, hoehe = baum.bbox(iid)
    klick(baum, lauf, x=x + min(60, breite // 2), y=y + hoehe // 2)
    assert app.active_list_id == liste["id"], "Linksklick nach Kontextmenü öffnet nicht"
    app.cancel_sidebar_rename()
    # Pfeiltasten bleiben ein gleichwertiger Öffnungsweg.
    taste(baum, "<Down>", lauf)
    assert app.active_list_id == zweite["id"], "Tastaturnavigation öffnet nicht"
    app.set_active_list(seite["id"])
    idle(lauf)
    baum, _iid, _menu = kontext(("list", liste["id"]))
    taste(baum, "<Down>", lauf)
    assert app.active_list_id == zweite["id"], "Pfeiltaste nach Rechtsklick öffnet nicht"
    taste(baum, "<Up>", lauf)
    assert app.active_list_id == liste["id"], "Rückkehr zum früheren Menüziel öffnet nicht"

    for row in (("list", seite["id"]), ("list", notiz["id"]), ("list", zeichnung["id"]),
                ("folder", ordner["id"]), ("view", "trash")):
        kontext(row)
    # Rechtsklick in eine Mehrfachauswahl behält sie und ihre gemeinsamen Aktionen.
    app.set_active_list(seite["id"])
    idle(lauf)
    baum = app.sidebar_listbox
    ids = tuple(app.get_sidebar_iid_for_row(("list", eintrag["id"])) for eintrag in (liste, zweite))
    baum.selection_set(ids)
    idle(lauf)
    _baum, _iid, menu = kontext(("list", liste["id"]))
    assert set(baum.selection()) == set(ids)
    assert str(menu.entrycget(0, "label")).startswith("Auswahl: 2 Liste(n)")
    app._destroy_sidebar_context_menu()
    return "Rechtsklick auf Liste/Seite/Notiz/Zeichnung/Ordner/Systemzeile ohne Öffnen; Nebenansicht, Linksklick, Pfeiltaste und Mehrfachauswahl erhalten"


def kompakt_knoepfe(app):
    return [app.compact_search_button, app.compact_capture_button, app.compact_menu_button, app.compact_exit_button]


def fall_kompakt(lauf):
    """Ein und aus per Kürzel, Mindestmaß, getrennte Fensterlagen, Neustart, Nebenansicht wartet."""
    app = lauf.app
    liste, punkte, seite = bestand(lauf)
    lauf.root.geometry("1280x800+40+30")
    idle(lauf, 6)
    app.open_side_view(liste["id"])
    idle(lauf, 4)
    normal = lauf.root.geometry()
    taste(lauf.root, "<Control-Shift-K>", lauf)
    lauf.root.event_generate("<Control-Shift-KeyRelease-K>")
    idle(lauf, 6)
    assert app.compact_mode_active(), "Drücken und Loslassen schalten genau einmal ein"
    assert tuple(lauf.root.minsize()) == (480, 560)
    breite, hoehe, x, y = lauf.mod.glide_compact.parse(lauf.root.geometry())
    assert breite == 480 and hoehe == 800 and x == 40 + 1280 - 480, lauf.root.geometry()
    assert not app.header_frame.winfo_ismapped() and app.compact_header.winfo_ismapped()
    assert not app.sidebar_shell.winfo_ismapped() and not app.sidebar_rail.winfo_ismapped()
    assert app.settings.get("sidebar_visible", True), "Seitenleisteneinstellung unberührt"
    assert not app.side_pane.winfo_ismapped() and app.side_view_open(), "Nebenansicht wartet"
    # Kopf: eine Zeile, gleiche Höhe und Mittellinie (B07), Titel gekürzt statt verdrängt.
    hoehen = {k.winfo_height() for k in kompakt_knoepfe(app)}
    assert hoehen == {app.HEADER_CONTROL_HEIGHT}, hoehen
    mitten = {k.winfo_rooty() + k.winfo_height() // 2 for k in kompakt_knoepfe(app)}
    assert len(mitten) == 1, mitten
    assert app.compact_title.winfo_width() >= 120 and app.compact_title.cget("text")
    anzahl, befunde = befunde_b15(lauf, "Kompakt 480x800")
    assert not befunde, befunde[:4]
    # Mindestgröße wirklich nutzbar.
    lauf.root.geometry("480x560")
    idle(lauf, 8)
    anzahl2, befunde = befunde_b15(lauf, "Kompakt 480x560")
    assert not befunde, befunde[:4]
    taste(lauf.root, "<Control-Shift-K>", lauf)
    lauf.root.event_generate("<Control-Shift-KeyRelease-K>")
    idle(lauf, 6)
    assert not app.compact_mode_active() and tuple(lauf.root.minsize()) == (860, 700)
    assert lauf.root.geometry() == normal, (lauf.root.geometry(), normal)
    assert app.header_frame.winfo_ismapped() and app.sidebar_shell.winfo_ismapped()
    assert app.side_pane.winfo_ismapped(), "Nebenansicht kehrt zurück"
    assert app.settings["compact_window"].startswith("480x560"), app.settings["compact_window"]
    # Zweiter Eintritt nutzt die gemerkte Kompaktlage.
    app.enter_compact_mode()
    idle(lauf, 6)
    assert lauf.root.geometry().startswith("480x560"), lauf.root.geometry()
    # Schließen im Kompaktmodus: window.conf trägt die Normallage.
    app.save_window_geometry()
    gespeichert = (Path(lauf.data) / "window.conf").read_text(encoding="utf-8")
    assert gespeichert == normal, (gespeichert, normal)
    lauf.neustart()
    app = lauf.app
    assert not app.compact_mode_active() and tuple(lauf.root.minsize()) == (860, 700)
    assert app.settings["compact_window"].startswith("480x560")
    # Unter Windows/Tk 9.0.4 kam nativ nur KeyRelease-K mit Strg+Shift an.
    # Die alte Prüfung erzeugte nur KeyPress am Hauptfenster und übersah das.
    app.set_active_list(seite["id"])
    idle(lauf)
    text = app.rich_note_editor.text
    vorher = text.get("1.0", "end-1c")
    for widget in (text, lauf.root):
        for key in ("K", "k"):
            taste(widget, f"<Control-Shift-KeyRelease-{key}>", lauf)
            assert app.compact_mode_active(), "Reines Loslassen schaltet nicht ein"
            taste(widget, f"<Control-Shift-KeyRelease-{key}>", lauf)
            assert not app.compact_mode_active(), "Reines Loslassen schaltet nicht aus"
    # Auch beim vollständigen Ereignispaar im Editor darf nichts doppelt wirken.
    taste(text, "<Control-Shift-K>", lauf)
    text.event_generate("<Control-Shift-KeyRelease-K>")
    idle(lauf)
    assert app.compact_mode_active(), "Editor-Ereignispaar schaltet doppelt"
    taste(text, "<Control-Shift-K>", lauf)
    # Werden die Modifiertasten zuerst losgelassen, muss die Merkung trotzdem enden.
    text.event_generate("<KeyRelease-k>")
    idle(lauf)
    assert not app.compact_mode_active()
    for sequence in ("<KeyRelease-k>", "<Shift-KeyRelease-K>", "<Control-KeyRelease-k>"):
        taste(text, sequence, lauf)
        assert not app.compact_mode_active(), ("Falsche Modifiertasten schalten um", sequence)
    assert text.get("1.0", "end-1c") == vorher, "Kürzel verändert den Seitentext"
    ansicht = next(menu for titel, menu in app.action_menus if titel == "Ansicht")
    assert ansicht.type(0) == "command" and ansicht.entrycget(0, "label") == "Kompaktmodus", \
        "Kompaktmodus muss im Menü Ansicht direkt an erster Stelle stehen"
    ansicht.invoke(0)
    idle(lauf)
    assert app.compact_mode_active(), "Menüeintrag schaltet nicht in den Kompaktmodus"
    ansicht.invoke(0)
    idle(lauf)
    assert not app.compact_mode_active(), "Menüeintrag kehrt nicht zur Normalansicht zurück"
    return f"Kompaktmodus direkt als erster Menüeintrag; Kürzel mit Drücken/Loslassen und reinem Loslassen im Editor/Hauptfenster, keine Doppelwirkung; 480×560, getrennte Lagen über Neustart, Kopf B07, {anzahl + anzahl2} Knöpfe ohne Befund"


def fall_kompakt_ansichten(lauf):
    """Kompakt mit großer Schrift: Liste, Heute, Seite, Startseite und Menü ohne verdeckte Kernfunktionen."""
    lauf.showcase()
    lauf.app.settings["ui_font_size"] = "gross"
    lauf.neustart()
    app = lauf.app
    seite = next(e for e in app.lists if app.is_page_list(e))
    liste = max((e for e in app.lists if not app.is_page_list(e) and e.get("items")), key=lambda e: len(e["items"]))
    app.enter_compact_mode()
    idle(lauf, 6)
    lauf.root.geometry("480x560")
    idle(lauf, 6)
    gesamt, befunde = 0, []
    for hinweise in (False, True):
        app.settings["show_hints"] = hinweise
        for name, oeffnen in (("Liste", lambda: app.set_active_list(liste["id"])), ("Heute", app.set_today_view),
                              ("Seite", lambda: app.set_active_list(seite["id"])), ("Startseite", app.set_home_view)):
            oeffnen()
            idle(lauf, 8)
            anzahl, funde = befunde_b15(lauf, f"Kompakt {name} groß Hinweise {'an' if hinweise else 'aus'}")
            gesamt += anzahl
            befunde.extend(funde)
            # Eingabe bzw. Inhalt bleibt sichtbar.
            assert app.compact_title.cget("text"), name
    assert not befunde, (len(befunde), befunde[:6])
    # Menü bündelt alle aktiven Menübefehle und führt sie aus.
    app.show_compact_menu()
    idle(lauf)
    zustand = app._action_chooser
    gezeigt = {(w.path, w.label) for w in zustand["entries"] if w.enabled}
    fehlend = native_blaetter(lauf, app.menubar) - gezeigt
    assert not fehlend, sorted(fehlend)[:5]
    buehne = zustand["stage"]
    assert buehne.winfo_rootx() >= lauf.root.winfo_rootx() and \
        buehne.winfo_rootx() + buehne.winfo_width() <= lauf.root.winfo_rootx() + lauf.root.winfo_width()
    zustand["entry"].insert(0, "heute")
    idle(lauf)
    ziel = next(iid for iid, w in zustand["results"].items() if w.label == "Heute" and w.path == ("Ansicht", "Ansichten"))
    zustand["tree"].selection_set(ziel)
    zustand["tree"].focus(ziel)
    taste(zustand["entry"], "<Return>", lauf)
    idle(lauf, 6)
    assert app.view_mode == app.PLAN_DAY_VIEW or "heute" in str(app.view_mode).lower(), app.view_mode
    # Nebenansicht im Kompaktmodus: verständliche Meldung statt verdeckter Fläche.
    meldungen = []
    app.show_info = lambda *a, **k: meldungen.append(a)
    assert not app.open_side_view(liste["id"]) and meldungen
    return f"{gesamt} Knopfprüfungen in vier Ansichten bei 480×560 und großer Schrift; Menü mit allen Befehlen"


def fall_gestaltung(lauf):
    """Sichtbelege: hell/dunkel/Verlauf, 860×700/1280×800/kompakt, Schrift mittel/groß, Hinweise an/aus."""
    lauf.showcase()
    app = lauf.app
    capture = getattr(lauf, "capture", None)

    def bild(widget, name):
        if not capture:
            return
        capture.mkdir(parents=True, exist_ok=True)
        idle(lauf, 4)
        x, y, b, h = widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_width(), widget.winfo_height()
        if sys.platform.startswith("linux"):
            subprocess.run(["import", "-window", "root", "-crop", f"{b}x{h}+{x}+{y}", str(capture / f"{name}.png")],
                           check=False)
        else:
            sys.path.insert(0, str(REPO / "tests/tools"))
            from releasedaten import save_windows_screenshot
            save_windows_screenshot(widget, capture / f"{name}.png")

    konfigurationen = (("hell_eng", "light", "860x700+0+0", "mittel", False, False),
                       ("dunkel_breit", "dark", "1280x800+0+0", "gross", True, False),
                       ("verlauf_breit", "glass_light", "1280x800+0+0", "mittel", True, False),
                       ("kompakt_hell", "light", "480x560", "gross", False, True),
                       ("kompakt_verlauf", "glass_dark", "480x760", "mittel", True, True))
    gesamt, befunde = 0, []
    for name, design, geometrie, schrift, hinweise, kompakt in konfigurationen:
        app.settings["ui_font_size"] = schrift
        app.settings["show_hints"] = hinweise
        app.apply_ui_font()
        app.set_design(design)
        if design.startswith("glass"):
            app.set_backdrop_choice(lauf.mod.glide_backdrop.presets_for(design)[0].key)
        if kompakt and not app.compact_mode_active():
            app.enter_compact_mode()
        if not kompakt and app.compact_mode_active():
            app.leave_compact_mode()
        lauf.root.geometry(geometrie)
        idle(lauf, 8)
        seite = next(e for e in app.lists if app.is_page_list(e) and not e.get("cover"))
        liste = max((e for e in app.lists if not app.is_page_list(e) and e.get("items")),
                    key=lambda e: len(e["items"]))
        app.set_active_list(seite["id"])
        idle(lauf, 8)
        editor = app.rich_note_editor
        editor.reveal_page_head(True)
        editor.text.focus_force()
        editor.text.mark_set("insert", "3.0")
        editor.show_block_handle("insert", "focus")
        idle(lauf, 4)
        anzahl, funde = befunde_b15(lauf, f"{name} Seite")
        gesamt += anzahl
        befunde.extend(funde)
        bild(lauf.root, f"{name}_seite")
        editor.show_block_actions()
        bild(lauf.root, f"{name}_blockaktionen")
        app.close_action_chooser()
        if not kompakt:
            app.set_active_list(liste["id"])
            idle(lauf, 6)
            app.open_side_view(seite["id"])
            idle(lauf, 6)
            anzahl, funde = befunde_b15(lauf, f"{name} Liste mit Nebenansicht")
            gesamt += anzahl
            befunde.extend(funde)
            bild(lauf.root, f"{name}_nebenansicht")
            app.close_side_view()
        else:
            app.set_active_list(liste["id"])
            idle(lauf, 6)
            anzahl, funde = befunde_b15(lauf, f"{name} Liste")
            gesamt += anzahl
            befunde.extend(funde)
            bild(lauf.root, f"{name}_liste")
            app.show_compact_menu()
            bild(lauf.root, f"{name}_menue")
            app.close_action_chooser()
    if app.compact_mode_active():
        app.leave_compact_mode()
    assert not befunde, (len(befunde), befunde[:6])
    return f"{gesamt} Knopfprüfungen in fünf Konfigurationen ohne Befund" + (" · Aufnahmen gespeichert" if capture else "")


FAELLE = ("seitenaktionen", "blockaktionen", "schreibschutz", "kopfverweise", "notiz", "nebenansicht_liste",
          "nebenansicht_seite", "nebenansicht_inspektor", "nebenansicht_einstiege", "verweisvorschau",
          "verweisvorschau_grenzen", "seitenleiste_kontext", "kompakt",
          "kompakt_ansichten", "gestaltung")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--fall", choices=FAELLE + ("alle",), default="alle")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--capture", type=Path)
    args = parser.parse_args()
    ergebnis = {"app_sha256": hashlib.sha256(args.app.read_bytes()).hexdigest(), "faelle": {}, "fehler": []}
    for name in (FAELLE if args.fall == "alle" else (args.fall,)):
        with tempfile.TemporaryDirectory(prefix=f"glide-arbeitsmodi-{name}-") as daten:
            lauf = None
            try:
                lauf = Lauf(args.app, daten)
                lauf.capture = args.capture
                text = globals()["fall_" + name](lauf)
                if lauf.errors:
                    raise AssertionError(("Rückruffehler", lauf.errors[:2]))
                ergebnis["faelle"][name] = {"ok": True, "befund": text}
                print(f"OK {name}: {text}", flush=True)
            except Exception:
                fehler = traceback.format_exc().replace(str(Path.home()), "~")[-1800:]
                ergebnis["faelle"][name] = {"ok": False, "befund": fehler}
                ergebnis["fehler"].append(name)
                print(f"ROT {name}: {fehler}", flush=True)
            finally:
                if lauf is not None:
                    abbauen(lauf)
    if args.report:
        args.report.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"gruen": len(ergebnis["faelle"]) - len(ergebnis["fehler"]), "rot": ergebnis["fehler"]},
                     ensure_ascii=False))
    return 1 if ergebnis["fehler"] else 0


if __name__ == "__main__":
    sys.exit(main())
