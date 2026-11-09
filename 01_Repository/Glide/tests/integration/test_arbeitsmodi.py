# SPDX-License-Identifier: MPL-2.0
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
import faulthandler
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import traceback
from types import SimpleNamespace
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tests/tools"))
from arbeitsmodi_gruppen import GRUPPEN, gruppen  # noqa: E402
sys.path.insert(0, str(REPO / "tests/integration"))
from test_uiux_paket import Lauf, knopf_befunde, knoepfe, sichtbarer_ausschnitt  # noqa: E402

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
    if hasattr(lauf, 'compact_trace'):
        lauf.compact_trace.append({'synthetic': sequenz, 'before': compact_snapshot(lauf)})
    widget.event_generate(sequenz)
    idle(lauf, 3)
    if hasattr(lauf, 'compact_trace'):
        lauf.compact_trace.append({'synthetic': sequenz, 'after': compact_snapshot(lauf)})


def compact_snapshot(lauf):
    focus = lauf.root.focus_get()
    return {'compact': lauf.app.compact_mode_active(),
            'down': bool(getattr(lauf.app, '_compact_shortcut_down', False)),
            'minsize': list(lauf.root.minsize()),
            'focus': str(focus) if focus is not None else None,
            'focus_class': focus.winfo_class() if focus is not None else None}


def trace_compact_events(lauf):
    """Beobachtete Ereignisse ohne Textinhalte; bei roten CI-Fällen im JSON behalten."""
    if not hasattr(lauf, 'compact_trace'):
        lauf.compact_trace = []
    handler = lauf.app.handle_compact_shortcut

    def observe(event):
        row = {'type': str(event.type), 'state': int(event.state), 'key': event.keysym,
               'time': event.time, 'before': compact_snapshot(lauf)}
        lauf.compact_trace.append(row)
        try:
            return handler(event)
        finally:
            row['after'] = compact_snapshot(lauf)

    for sequence in ('<Control-Shift-K>', '<Control-Shift-k>', '<KeyRelease-K>', '<KeyRelease-k>'):
        lauf.root.bind(sequence, observe)
    if lauf.mod.IS_MACOS:
        for sequence in ('<Command-Shift-K>', '<Command-Shift-k>'):
            lauf.root.bind(sequence, observe)


def klick(widget, lauf, x=4, y=4):
    widget.event_generate("<Enter>", x=x, y=y)
    widget.event_generate("<ButtonPress-1>", x=x, y=y)
    widget.event_generate("<ButtonRelease-1>", x=x, y=y)
    # Wie die echte Maus: Verlassen beendet auch den vorgemerkten Tooltip.
    if widget.winfo_exists():
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
    # Ein echter Klick aktiviert das Fenster; der synthetische nicht. Ohne
    # Vordergrund meldet Windows sonst keinen Fokus für das Suchfeld.
    editor.text.focus_force()
    idle(lauf)
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
    griff.event_generate("<ButtonRelease-1>", x=3, y=3)
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
    """D71 (Abnahme 07.11.2026): Seitentitel nur im Kopf; Symbol und Titelbild über „Mehr“, Text beginnt oben."""
    app, mod = lauf.app, lauf.mod
    seite, editor = seite_anlegen(lauf, SEITE_MD.replace("# Wochenplanung Parkquartier", "# Notiz", 1))
    titel = editor.title_label
    assert not editor.TITLE_IN_CONTENT
    for geometrie in ("1280x800", "860x700"):
        lauf.root.geometry(geometrie + "+20+20")
        idle(lauf, 8)
        editor.fit_title()
        idle(lauf)
        assert not titel.winfo_manager(), ("Seitentitel steht doppelt im Inhalt", geometrie)
        assert not editor._head_row.winfo_ismapped(), ("Kopfverweise ohne Titelzeile sichtbar", geometrie)
        assert app.title_label.cget("text").startswith(app.page_entry(seite["id"])["title"][:4]), app.title_label.cget("text")
        # Der Text beginnt unmittelbar unter Titelbild/Rand, nicht unter einer zweiten Titelzeile.
        abstand = editor.text.winfo_rooty() - editor.winfo_rooty()
        assert abstand <= 60, ("Text beginnt zu tief", geometrie, abstand)
    nativ = editor.build_page_menu()
    eintraege = native_blaetter(lauf, nativ) | {((), l) for _k, l, p, a, _g, art in app.menu_rows(nativ) if not p}
    nativ.destroy()
    assert ((), "Pixelsymbol …") in eintraege, sorted(eintraege)[:8]
    assert any(pfad[:1] == ("Titelbild",) for pfad, _l in eintraege), "Titelbild über Mehr"
    anzahl, befunde = befunde_b15(lauf, "Seite ohne Inhaltstitel 860x700")
    assert not befunde, befunde[:4]
    # Pixelsymbol (Inhaberwunsch 07.11.2026): fest oben im Leserand links neben der Griffspalte ⋮⋮,
    # scrollt nicht mit; der Griff überdeckt es nie.
    rechteck = lambda w: (w.winfo_rootx(), w.winfo_rooty(),
                          w.winfo_rootx() + w.winfo_width(), w.winfo_rooty() + w.winfo_height())
    schneidet = lambda a, b: not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])
    lauf.root.geometry("1280x800+20+20")
    idle(lauf, 8)
    eintrag = app.page_entry(seite["id"])
    eintrag["icon"] = mod.glide_drawing.DrawingModel.blank(app.PAGE_ICON_SIZE).to_document()
    editor.refresh_page_head()  # derselbe Weg wie nach „Pixelsymbol …“
    editor.text.insert("end", "\n" + "\n".join(f"Zeile {n}" for n in range(120)))
    editor.text.yview_moveto(0.0)
    idle(lauf, 6)
    icon = editor._title_icon_label
    griff = editor._block_handle
    assert icon.master is editor.text, "Symbol ist kein Kind des Textfelds"
    assert editor._title_icon is not None and icon.winfo_ismapped(), "Pixelsymbol fehlt in der Seite"
    assert editor._title_icon.transparency_get(0, 0), "Pixelsymbol mit weißem Grund statt durchsichtig"
    editor.show_block_handle("1.0", "focus")
    idle(lauf)
    assert griff.winfo_ismapped() and icon.winfo_ismapped()
    assert icon.winfo_rootx() + icon.winfo_width() + 8 <= griff.winfo_rootx() + 1, (
        "Symbol nicht links der Griffspalte", rechteck(icon), rechteck(griff))
    assert icon.winfo_rootx() >= editor.text.winfo_rootx(), "Symbol ragt aus dem Leserand"
    zeile = editor.text.dlineinfo("1.0")
    oben = icon.winfo_rooty() - editor.text.winfo_rooty()
    assert zeile[1] <= oben <= zeile[1] + zeile[3], (zeile, oben)
    editor.hide_block_handle()
    aufrufe = []
    editor.choose_page_icon = lambda: aufrufe.append("symbol") or "break"
    icon.event_generate("<Button-1>", x=4, y=4)
    idle(lauf)
    taste(icon, "<Return>", lauf)
    taste(icon, "<space>", lauf)
    assert aufrufe == ["symbol"] * 3, "Pixelsymbol per Maus und Tastatur erreichbar"
    # Fest: weder Pixel-Scrollen, Mausrad noch Sprung ans Ende bewegen es.
    start = rechteck(icon)
    editor.text.yview_scroll(12, "pixels")
    idle(lauf, 4)
    for _runde in range(4):
        editor.text.event_generate("<MouseWheel>", delta=-1, x=40, y=40)
        idle(lauf, 4)
    editor.text.yview_moveto(0.6)
    idle(lauf, 4)
    assert icon.winfo_manager() == "place" and rechteck(icon) == start, ("Symbol scrollt mit", start, rechteck(icon))
    # Griff an Zeilen unter dem Symbol: keine Überdeckung, bei beiden Breiten.
    for geometrie in ("1280x800", "860x700"):
        lauf.root.geometry(geometrie + "+20+20")
        idle(lauf, 8)
        oberste = editor.text.index("@0,0")
        editor.show_block_handle(oberste, "pointer")
        idle(lauf)
        if icon.winfo_ismapped():
            assert not schneidet(rechteck(griff), rechteck(icon)), (geometrie, rechteck(griff), rechteck(icon))
        editor.hide_block_handle()
        idle(lauf)
        assert icon.winfo_ismapped(), ("Symbol kehrt nach dem Griff nicht zurück", geometrie)
    return (f"Titel nur im Kopf (1280/860 px), Text beginnt oben, Symbol/Titelbild über Mehr, "
            f"Pixelsymbol fest links der Griffspalte (Klick/Return/Leertaste, scrollt nicht mit), {anzahl} Knopfprüfungen")

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
    # Auch bei fehlendem Inhalt bleibt die neue lesende Rücknavigation offen.
    assert beschriftungen == ["Zurück", "Vorwärts", "Verlauf", "Schließen"], beschriftungen
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
    text.see(marken[0]._w)
    idle(lauf, 5)
    assert marken[0].winfo_ismapped(), "Das echte Kästchen ist vor dem Klick sichtbar"
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


def pruefe_rueckmeldung_ueber_rueckgaengig(lauf):
    """Ein später erscheinender Verlaufshinweis bleibt unter der laufenden Fahne."""
    app, root, mod = lauf.app, lauf.root, lauf.mod
    app.hide_undo_toast()
    scheduled = []
    original_after = root.after

    def remember(delay, callback=None, *args):
        identity = original_after(delay, callback, *args)
        if delay == 38:
            scheduled.append((identity, callback))
        return identity

    banner = None
    try:
        with patch.object(root, 'after', side_effect=remember):
            app._draw_celebration('Geprüfte Rückmeldung')
            banner = next(widget for widget in app.main_area.winfo_children()
                          if isinstance(widget, mod.tk.Label) and widget.cget('text') == 'Geprüfte Rückmeldung')
            toast = app._place_history_toast('Geprüfte Änderung', 'Rückgängig', lambda: None)
            root.update_idletasks()
            identity, advance = scheduled[0]
            root.after_cancel(identity)
            advance()
            root.update_idletasks()
            assert banner.winfo_rooty() + banner.winfo_height() <= toast.winfo_rooty() - 8, (
                'Laufende Rückmeldung überdeckt den späteren Rückgängig-Hinweis',
                banner.winfo_rooty(), banner.winfo_height(), toast.winfo_rooty())
    finally:
        app.hide_undo_toast()
        if banner is not None and banner.winfo_exists():
            banner.destroy()


def fall_verweisvorschau_grenzen(lauf):
    app, mod = lauf.app, lauf.mod
    pruefe_rueckmeldung_ueber_rueckgaengig(lauf)
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
    trace_compact_events(lauf)
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
    normal_breite, normal_hoehe, normal_x, normal_y = lauf.mod.glide_compact.parse(normal)
    _links, _oben, _desktop_breite, desktop_hoehe = app.desktop_bounds()
    assert breite == 480 and x + breite == normal_x + normal_breite, lauf.root.geometry()
    assert 560 <= hoehe <= normal_hoehe and y == normal_y, lauf.root.geometry()
    if normal_hoehe <= desktop_hoehe - lauf.mod.glide_compact.SCREEN_RESERVE:
        assert hoehe == normal_hoehe, "Bei ausreichender Arbeitsfläche bleibt die Höhe erhalten"
    else:
        assert hoehe == max(560, desktop_hoehe - lauf.mod.glide_compact.SCREEN_RESERVE), lauf.root.geometry()
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
    assert not app.compact_mode_active(), compact_snapshot(lauf)
    assert tuple(lauf.root.minsize()) == (860, 700), compact_snapshot(lauf)
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
    trace_compact_events(lauf)
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


def fall_kompakt_verlorenes_loslassen(lauf):
    """Fehlendes K-Loslassen, Modifierende und Fensterfokusverlust über echte Bindungen."""
    app = lauf.app
    trace_compact_events(lauf)
    taste(lauf.root, '<Control-Shift-K>', lauf)
    assert app.compact_mode_active(), compact_snapshot(lauf)
    taste(lauf.root, '<KeyRelease-Control_L>', lauf)
    assert not getattr(app, '_compact_shortcut_down', False), compact_snapshot(lauf)
    taste(lauf.root, '<Control-Shift-K>', lauf)
    assert not app.compact_mode_active(), compact_snapshot(lauf)
    lauf.root.event_generate('<KeyRelease-k>')
    idle(lauf)
    # Interner Fokuswechsel erhält die Paarzuordnung; nur das Hauptfensterende setzt zurück.
    app._compact_shortcut_down = True
    app.entry.event_generate('<FocusOut>')
    idle(lauf)
    assert app._compact_shortcut_down, 'Interner Fokuswechsel verliert das Ereignispaar'
    # Ein zweiter Tk-Interpreter ist unter Cocoa keine andere Anwendung.
    # Dort die eingebaute Finder-App aktivieren; Fokusverlust weiterhin messen,
    # nicht durch ein gefälschtes FocusOut oder einen Mock ersetzen.
    ausserhalb = None
    focus_out = []
    binding = lauf.root.bind('<FocusOut>', lambda event: focus_out.append(str(event.widget)), add='+')
    try:
        if sys.platform == 'darwin':
            subprocess.run(['/usr/bin/open', '-a', 'Finder'], check=True, timeout=10,
                           capture_output=True, text=True)
        else:
            ausserhalb = lauf.mod.tk.Tk()
            ausserhalb.geometry('180x100+30+30')
            ausserhalb.update()
            ausserhalb.focus_force()
        deadline = time.monotonic() + 5
        while lauf.root.focus_get() is not None and time.monotonic() < deadline:
            idle(lauf, 2)
            time.sleep(.02)
        idle(lauf, 6)
        lauf.compact_trace.append({'external_focus': 'Finder' if sys.platform == 'darwin' else 'Tk',
                                   'focus_out': focus_out, 'after': compact_snapshot(lauf)})
        assert lauf.root.focus_get() is None, compact_snapshot(lauf)
        if sys.platform == 'darwin':
            assert str(lauf.root) in focus_out, 'Kein echter Hauptfenster-FocusOut beim App-Wechsel'
        else:
            lauf.root.event_generate('<FocusOut>')
        idle(lauf, 4)
        assert not app._compact_shortcut_down, compact_snapshot(lauf)
    finally:
        lauf.root.unbind('<FocusOut>', binding)
        if ausserhalb is not None:
            ausserhalb.destroy()
    taste(lauf.root, '<Control-Shift-K>', lauf)
    assert app.compact_mode_active(), compact_snapshot(lauf)
    lauf.root.event_generate('<KeyRelease-k>')
    idle(lauf)
    return 'Fehlendes K-Loslassen blockiert nach Modifierende/Fensterfokusverlust nicht das nächste Kürzel; interner Fokuswechsel erhält das Paar'


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
        visible_editors = [child for child in app.list_frame_outer.inner.winfo_children()
                           if isinstance(child, lauf.mod.PageEditor) and child.winfo_manager()]
        assert visible_editors == [editor], (name, "mehrere aktive Seiteneditoren", visible_editors)
        editor.reveal_page_head(True)
        editor.text.focus_force()
        editor.text.mark_set("insert", "3.0")
        editor.show_block_handle("insert", "focus")
        seiteninhalt = editor.text.get("1.0", "end-1c")
        idle(lauf, 4)
        if name == "hell_eng":
            # Deterministische Lebensdauer-Gegenprobe: derselbe reguläre
            # Neuaufbau wie bei ungültiger Themesignatur. Der alte Host muss
            # wirklich verschwinden; der vollständige Knopfschutz folgt danach.
            app._rich_note_signature = None
            app.sync_rich_note_view()
            idle(lauf, 4)
            assert not editor.winfo_exists(), "Gegenprobe ersetzt den Seitenhost nicht"
        anzahl, funde = befunde_b15(lauf, f"{name} Seite")
        gesamt += anzahl
        befunde.extend(funde)
        bild(lauf.root, f"{name}_seite")
        # _sync_rich_note_view ersetzt den Host bei geänderter Themesignatur.
        # Nach Idle-/Mess-/Aufnahmeschritten bedient ein Nutzer den jetzt
        # sichtbaren Editor, nicht die zuvor gespeicherte Widgetinstanz.
        vorher = editor
        editor = app.rich_note_editor
        assert app.current_list()["id"] == seite["id"], (name, "Seitenziel verändert")
        assert editor is not None and editor.winfo_exists() and editor.winfo_ismapped(), (name, "kein aktiver Seiteneditor")
        assert editor.text.get("1.0", "end-1c") == seiteninhalt, (name, "Seiteninhalt beim Neuaufbau verändert")
        lauf.editor_host_trace = getattr(lauf, "editor_host_trace", []) + [
            dict(context=name,old_widget=str(vorher),active_widget=str(editor),content_preserved=True)]
        editor.text.focus_force()
        editor.text.mark_set("insert", "3.0")
        editor.show_block_actions()
        idle(lauf, 4)
        assert app.action_chooser_open(), (name, "Blockaktionen nicht geöffnet")
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


def fall_tagessteuerung(lauf):
    """Neue Startseitenaktionen über echte Knöpfe/Menüs und vorhandene Mutationswege."""
    from datetime import date, timedelta
    app, mod = lauf.app, lauf.mod
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    source = app.new_list_object('Tagessteuerung')
    task = app.new_item('Angebot prüfen', due=today, planned_date=today, estimated_minutes=30)
    blocker = app.new_item('Freigabe abwarten', planned_date=today)
    blocked = app.new_item('Noch blockiert', planned_date=today, blocked_by=[blocker['id']])
    source['items'] = [task, blocker, blocked]
    app.lists, app.folders, app.labels, app.trash = [source], [], [], []
    app.items, app.active_list_id = source['items'], source['id']
    app.settings['home_tile_order'] = ['today', 'focus']
    app.settings['home_tiles_hidden'] = [key for key in app.HOME_TILE_KEYS if key not in ('today', 'focus')]
    app.settings['release_notes_seen'] = mod.APP_VERSION
    app.settings['daily_capacity_minutes'] = 60
    app.settings.pop('daily_capacity_by_weekday', None)
    app.clear_render_cache()
    assert app.save_items()
    app.undo_stack.clear()
    app.set_home_view()
    idle(lauf)
    more = next(w for w in knoepfe(app.home_content, mod.RoundedButton)
                if getattr(w, '_home_task_actions_id', None) == task['id'])
    choices = [key for key, text in mod.glide_planning.CHOICES]
    selected = []

    def choose_tomorrow(menu, x, y):
        try:
            plan = menu.nametowidget(menu.entrycget(0, 'menu'))
            assert 'frei' in plan.entrycget(0, 'label') or 'verplant' in plan.entrycget(0, 'label')
            plan.invoke(choices.index('tomorrow'))
            selected.append(True)
        finally:
            menu.unpost()

    # Menüobjekt und Tcl-Befehl bleiben echt; nur die modale OS-Menüschleife
    # wird durch die konkrete Auswahl ersetzt, ohne fremde Fenstereingaben.
    with patch.object(mod.tk.Menu, 'tk_popup', new=choose_tomorrow):
        klick(more, lauf)
    assert selected, lauf.errors
    idle(lauf)
    current = app.find_item_in_lists(task['id'])[0]
    assert current['planned_date'] == tomorrow and current['due'] == today
    assert len(app.undo_stack) == 1 and app.view_mode == app.HOME_VIEW
    app.undo_last_change()
    idle(lauf)
    assert app.find_item_in_lists(task['id'])[0]['planned_date'] == today
    depth = len(app.undo_stack)
    with patch.object(app, 'themed_due_dialog', return_value=None):
        app.choose_home_plan('date', (task['id'],))
    assert len(app.undo_stack) == depth
    with patch.object(app, 'themed_due_dialog', return_value=(tomorrow, None)) as dialog:
        app.choose_home_plan('date', (task['id'],))
    assert dialog.call_args.kwargs['planning_preview_ids'] == (task['id'],)
    assert app.find_item_in_lists(task['id'])[0]['planned_date'] == tomorrow
    app.choose_home_plan('unplan', (task['id'],))
    assert app.find_item_in_lists(task['id'])[0]['planned_date'] is None
    depth = len(app.undo_stack)
    with patch.object(app, 'refresh_data_lock', return_value=False):
        app.choose_home_plan('today', (task['id'],))
        assert not app.start_home_focus(task['id'])
    assert len(app.undo_stack) == depth
    blocked_menu = app.build_home_task_menu(blocked['id'])
    assert blocked_menu.entrycget(1, 'state') == 'disabled'
    blocked_menu.destroy()
    with patch.object(app, 'save_settings', return_value=False):
        assert not app.start_home_focus(task['id'])
    assert not app.running_timer()
    app.choose_home_plan('today', (task['id'],))
    focus = next(w for w in knoepfe(app.home_content, mod.RoundedButton) if w.text == 'Fokus starten')
    klick(focus, lauf)
    assert app.running_timer()['item_id'] == task['id'] and app.running_timer()['focus']
    saved = json.loads(Path(mod.SETTINGS_FILE).read_text(encoding='utf-8'))
    assert saved['time_tracking']['item_id'] == task['id']
    return 'Mehr-Menü mit Kapazität, Morgen/Datum/Abbruch/ohne Tag, Fälligkeit erhalten, Undo, Sperre/Blockierung, Fokusfehler und echter gespeicherter Fokusstart'


def fall_nebenansicht_navigation(lauf):
    """Such-/Abschnittswege erhalten Haupteditor, Modell und gespeicherte Bytes."""
    app, mod = lauf.app, lauf.mod
    main, editor = seite_anlegen(lauf, '# Hauptarbeit\n\nOffener Entwurf\n')
    other = app.new_page_from_markdown('# Überblick\n\n🎵 Straße und STRASSE. [x]\n\n'
        + '\n\n'.join(f'Absatz {number}' for number in range(35))
        + '\n\n## Abschluss\n\nEine weitere Straße.\n\n- [ ] Straße-Aufgabe\n')
    app.set_active_list(main['id'])
    idle(lauf)
    editor = app.rich_note_editor
    assert app.open_side_view(other['id'])
    idle(lauf)
    editor.text.insert('end-1c', '\nNoch nicht verlassen')
    idle(lauf, 1)
    if editor._job is not None:
        editor.after_cancel(editor._job)
        editor._job = None  # Nur Navigationswirkung messen; normaler Autosave separat.
    draft = editor.text.get('1.0', 'end-1c')
    model = copy.deepcopy(app.lists)
    written = Path(mod.SAVE_FILE).read_bytes()
    depth = len(app.undo_stack)
    search = next(w for w in knoepfe(app.side_pane, mod.RoundedButton) if w.text == 'Suchen')
    klick(search, lauf)
    field = app._side_search_entry
    field.insert(0, 'STRASSE')
    taste(field, '<KeyRelease-e>', lauf)
    assert len(app._side_search_matches) == 4, app._side_search_matches
    assert app._side_search_counter.cget('text') == '1 / 4 Treffer'
    body = app._side_view_body
    ranges = body.tag_ranges('search_current')
    assert body.get(*ranges) == 'Straße'
    app.move_side_search(-1)
    assert body.get(*body.tag_ranges('search_current')) == 'Straße', 'Versatz nach eingebettetem Kästchen'
    app.move_side_search(1)
    taste(field, '<Return>', lauf)
    assert app._side_search_index == 1
    taste(field, '<Shift-Return>', lauf)
    assert app._side_search_index == 0
    field.delete(0, 'end'); field.insert(0, '[x]')
    app.update_side_search()
    assert len(app._side_search_matches) == 1
    field.delete(0, 'end'); field.insert(0, 'Nicht vorhanden')
    app.update_side_search()
    assert app._side_search_counter.cget('text') == 'Keine Treffer.'
    field.delete(0, 'end'); field.insert(0, 'STRASSE')
    app.update_side_search()
    app.sync_side_view(force=True)
    idle(lauf)
    assert app._side_search_entry.get() == 'STRASSE' and len(app._side_search_matches) == 4
    assert app._side_search_entry is not field
    section = mod.glide_side_view.sections(other)[-1]
    outline = next(w for w in knoepfe(app.side_pane, mod.RoundedButton)
                   if w.text == mod.RoundedButton.action_text('Abschnitte …'))

    def choose_section(menu, x, y):
        try:
            # Seit 3.50.0 nennt die Abschnittsauswahl bei aktiver Suche die Treffer je Abschnitt.
            assert menu.entrycget('end', 'label').lstrip('✓ ') == section['title'] + ' · 2 Treffer'
            menu.invoke('end')
        finally:
            menu.unpost()

    with patch.object(mod.tk.Menu, 'tk_popup', new=choose_section):
        klick(outline, lauf)
    idle(lauf)
    assert app._side_view_body.yview()[0] > 0
    assert app.active_list_id == main['id'] and app.rich_note_editor is editor
    assert editor.text.get('1.0', 'end-1c') == draft
    assert app.lists == model and Path(mod.SAVE_FILE).read_bytes() == written and len(app.undo_stack) == depth
    # Escape: Suchtext, Suchzeile, dann Nebenansicht; Hauptinhalt bleibt.
    taste(app._side_search_entry, '<Escape>', lauf)
    assert app.side_view_open() and app._side_search_entry.get() == ''
    taste(app._side_search_entry, '<Escape>', lauf)
    assert app.side_view_open() and not app._side_search_open
    taste(app._side_view_body, '<Control-f>', lauf)
    assert app._side_search_open
    taste(app._side_search_entry, '<Escape>', lauf)
    taste(app._side_view_body, '<Escape>', lauf)
    assert not app.side_view_open()
    listing = app.new_list_object('Nachschlageliste')
    group = app.new_item('Abschnitt Nord', kind=app.ITEM_KIND_GROUP)
    a, b = app.new_item('Straße prüfen'), app.new_item('STRASSE messen')
    group['children'] = [a, b]
    listing['items'] = [group]
    app.lists.append(listing)
    app.open_side_view(listing['id'])
    app.open_side_search()
    field = app._side_search_entry
    field.insert(0, 'strasse'); app.update_side_search()
    assert len(app._side_search_matches) == 2
    app.move_side_search(1)
    assert app._side_view_body.selection() == (b['id'],)
    app.jump_side_section(listing['id'], mod.glide_side_view.sections(listing)[0])
    assert app._side_view_body.selection() == (group['id'],)
    app._data_read_only = True
    app.sync_side_view(force=True)
    assert app._side_search_entry.get() == 'strasse' and len(app._side_search_matches) == 2
    app._data_read_only = False
    app.close_side_view()
    assert app.rich_note_editor is editor and editor.text.get('1.0', 'end-1c') == draft
    return 'Wörtliche Unicode-Suche, Trefferwechsel/Tasten, kein Treffer, Neuaufbau, Überschriften/Gruppen, readonly und dreistufiges Esc; Haupteditor und offene Eingaben erhalten'


def fall_home_mehrfachplanung(lauf):
    """Auswahl über Seiten und Listen, ein Planungs-Undo, frische Ziele nach Dialogen."""
    from datetime import date, timedelta
    app, mod = lauf.app, lauf.mod
    today, tomorrow = date.today().isoformat(), (date.today()+timedelta(days=1)).isoformat()
    tasks = [app.new_item(f'Tagesaufgabe {n:02}', planned_date=today, due=today, estimated_minutes=15)
             for n in range(23)]
    tasks[0]['done'] = tasks[1]['done'] = True
    first, second = app.new_list_object('Erste Quelle', tasks[:12]), app.new_list_object('Zweite Quelle', tasks[12:])
    archived = app.new_list_object('Archiv', [app.new_item('Nicht auswählen', planned_date=today)])
    archived['archived'] = True
    app.lists, app.items, app.active_list_id = [first, second, archived], first['items'], first['id']
    app.settings['home_tile_order'] = ['today']
    app.settings['home_tiles_hidden'] = [key for key in app.HOME_TILE_KEYS if key != 'today']
    app.settings['release_notes_seen'] = mod.APP_VERSION
    app.settings['daily_capacity_minutes'] = 480
    app.settings.pop('daily_capacity_by_weekday', None)
    assert app.save_items()
    app.undo_stack.clear()
    app.set_home_view(); idle(lauf)

    def button(title):
        return next(w for w in knoepfe(app.home_content, mod.RoundedButton)
                    if w.text.rstrip(' .…') == title.rstrip(' .…'))

    before = Path(mod.SAVE_FILE).read_bytes()
    klick(button('Mehrere auswählen'), lauf)
    checks = [w for w in knoepfe(app.home_content, mod.RoundedButton) if hasattr(w, '_home_selection_id')]
    assert len(checks) == 10
    klick(checks[0], lauf)
    selected = set(app.home_selection_projection()['selected'])
    klick(button('Weitere Seite'), lauf)
    checks = [w for w in knoepfe(app.home_content, mod.RoundedButton) if hasattr(w, '_home_selection_id')]
    klick(checks[0], lauf)
    assert len(app.home_selection_projection()['selected']) == 2
    assert selected < set(app.home_selection_projection()['selected'])
    assert Path(mod.SAVE_FILE).read_bytes() == before and not app.undo_stack
    assert sum(item['done'] for item in tasks) == 2
    klick(button('Alle auswählen'), lauf)
    identities = app.home_selection_projection()['selected']
    assert len(identities) == 21 and app.home_selection_projection()['pages'] == 3
    assert archived['items'][0]['id'] not in identities

    labels = []
    def choose(menu, *args, **kwargs):
        labels.extend(menu.entrycget(n, 'label') for n in range(menu.index('end')+1))
        menu.invoke(next(n for n, text in enumerate(labels) if text.startswith('Morgen')))
    with patch.object(mod.tk.Menu, 'tk_popup', choose):
        klick(button('Auswahl planen'), lauf)
    assert len(app.undo_stack) == 1
    assert all(app.find_item_in_lists(identity)[0]['planned_date'] == tomorrow for identity in identities)
    assert all(app.find_item_in_lists(identity)[0]['due'] == today for identity in identities)
    assert not app.home_selection_projection()['selected']
    assert any('Morgen' in text and '·' in text for text in labels)
    app.undo_last_change(); idle(lauf)
    assert all(app.find_item_in_lists(identity)[0]['planned_date'] == today for identity in identities)
    app.redo_last_change(); idle(lauf)
    assert all(app.find_item_in_lists(identity)[0]['planned_date'] == tomorrow for identity in identities)
    app.undo_last_change(); idle(lauf)

    app.change_home_selection('all')
    identities = app.home_selection_projection()['selected']
    depth = len(app.undo_stack)
    with patch.object(app, 'themed_due_dialog', return_value=None) as dialog:
        app.choose_home_selection_plan('date', identities)
        assert dialog.call_args.kwargs['planning_preview_ids'] == identities
    assert len(app.undo_stack) == depth
    with patch.object(app, 'refresh_data_lock', return_value=False):
        app.choose_home_selection_plan('tomorrow', identities)
    assert all(app.find_item_in_lists(identity)[0]['planned_date'] == today for identity in identities)
    def change_during_dialog(*args, **kwargs):
        app.find_item_in_lists(identities[0])[0]['done'] = True
        return (tomorrow, None)
    with patch.object(app, 'themed_due_dialog', side_effect=change_during_dialog):
        app.choose_home_selection_plan('date', identities)
    assert all(app.find_item_in_lists(identity)[0]['planned_date'] == today for identity in identities)
    assert len(app.undo_stack) == depth
    app.find_item_in_lists(identities[0])[0]['done'] = False
    app.change_home_selection('clear')
    app.choose_home_selection_plan('tomorrow', identities)  # altes Menü nach neuer Auswahl
    assert len(app.undo_stack) == depth
    app.change_home_selection('all')
    app.choose_home_selection_plan('unplan', app.home_selection_projection()['selected'])
    assert all(app.find_item_in_lists(identity)[0]['planned_date'] is None for identity in identities)
    app.undo_last_change(); idle(lauf)
    app._home_plan_selection['day'] = (date.today()-timedelta(days=1)).isoformat()
    app.refresh_home(); idle(lauf)
    assert app._home_plan_selection is None
    app.change_home_selection('start')
    app._data_read_only = True
    app.refresh_home(); idle(lauf)
    assert app._home_plan_selection is None
    assert not any(hasattr(w, '_home_selection_id') for w in knoepfe(app.home_content, mod.RoundedButton))
    app._data_read_only = False
    return '21 offene Aufgaben aus zwei Listen über drei Seiten; Auswahl ohne Schreiben/Erledigen, Morgen/ohne Tag mit einem Undo/Redo, Fälligkeit, Dialogabbruch/Alterung, Sperre, Tageswechsel und readonly grün'


def fall_side_history(lauf):
    """Echter Sitzungsverlauf mit Suche, Scrollen, Tastatur und erhaltenem Hauptentwurf."""
    app, mod = lauf.app, lauf.mod
    source, tasks, main = bestand(lauf)
    page = app.new_list_object('Nachschlagen', [])
    page['list_kind'] = 'page'
    page['rich_note'] = {'text':'Straße zuerst\n' + '\n'.join(f'Zeile {n}' for n in range(100))+'\nStraße zuletzt', 'spans':[]}
    other = app.new_list_object('Weiterlesen', [])
    other['list_kind'] = 'page'
    other['rich_note'] = {'text':'\n'.join(f'Absatz {n}' for n in range(160)), 'spans':[]}
    app.lists.extend([page, other]); assert app.save_items()
    app.set_active_list(main['id']); idle(lauf)
    editor = app.rich_note_editor
    assert app.open_side_view(page['id']); idle(lauf)
    editor.text.insert('end-1c', '\nOffener Hauptentwurf')
    idle(lauf, 1)
    # Die vorhandene 400-ms-Notizspeicherung separat halten: Hier messen wir,
    # ob Navigation einen offenen Hauptentwurf zwangsweise übernimmt.
    if editor._job is not None:
        editor.after_cancel(editor._job)
        editor._job = None
    draft = editor.text.get('1.0','end-1c')
    before, depth = Path(mod.SAVE_FILE).read_bytes(), len(app.undo_stack)
    app.open_side_search()
    app._side_search_entry.insert(0,'STRASSE'); app.move_side_search(1); idle(lauf)
    assert app._side_search_index == 1
    assert app.open_side_view(source['id'],item_id=tasks[1]['id']); idle(lauf)
    assert app.open_side_view(other['id']); idle(lauf)
    app._side_view_body.yview_moveto(0.65); idle(lauf)
    scroll = app._side_view_body.yview()[0]
    app.move_side_history(-1); idle(lauf)
    assert app.side_view_entry()['id'] == source['id']
    assert app._side_view_body.selection() == (tasks[1]['id'],)
    app.move_side_history(-1); idle(lauf)
    assert app.side_view_entry()['id'] == page['id']
    assert app._side_search_query == 'STRASSE' and app._side_search_index == 1
    assert app._side_view_body.get(*app._side_view_body.tag_ranges('search_current')) == 'Straße'
    taste(app._side_view_body,'<Alt-Right>',lauf)
    assert app.side_view_entry()['id'] == source['id']
    app.move_side_history(1); idle(lauf)
    assert app.side_view_entry()['id'] == other['id']
    assert abs(app._side_view_body.yview()[0]-scroll) < 0.05
    assert app.rich_note_editor is editor and editor.text.get('1.0','end-1c') == draft
    assert Path(mod.SAVE_FILE).read_bytes() == before and len(app.undo_stack) == depth
    page['title'] = 'Aktueller Titel'
    labels = []
    def inspect(menu,*args,**kwargs):
        labels.extend(menu.entrycget(n,'label') for n in range(menu.index('end')+1) if menu.type(n)=='command')
    with patch.object(mod.tk.Menu,'tk_popup',inspect): app.show_side_history()
    assert labels[0] == 'Inhalt wechseln …' and any('Aktueller Titel' in label for label in labels)
    old_choose = app.choose_side_view
    called = []
    app.choose_side_view = lambda: called.append(True)
    with patch.object(mod.tk.Menu,'tk_popup',lambda menu,*a,**k:menu.invoke(0)): app.show_side_history()
    idle(lauf)
    app.choose_side_view = old_choose
    assert called == [True]
    app.lists.remove(source)
    app.move_side_history(-1); idle(lauf)
    assert app.side_view_entry()['id'] == page['id'], 'Gelöschte Station wird übersprungen'
    assert app.open_side_view(other['id']); idle(lauf)
    assert app.side_history().index == len(app.side_history().entries)-1
    app.lists.remove(other)
    app.sync_side_view(force=True); idle(lauf)
    back = next(w for w in knoepfe(app.side_pane,mod.RoundedButton) if w.text=='Zurück')
    klick(back,lauf)
    assert app.side_view_entry()['id'] == page['id'], 'Auch aus fehlendem Inhalt zurück'
    app._data_read_only = True
    app.close_side_view(); assert app.open_side_view(page['id']); idle(lauf)
    assert app.side_history().entries
    with patch.object(mod,'SAVE_FILE',Path(lauf.mod.SAVE_FILE).with_name('anderer-bestand.json')):
        assert app.side_history() == mod.glide_side_view.History()
    app._data_read_only = False
    return 'Zurück/Vorwärts/Alt-Pfeile, Suchbegriff/aktiver Treffer, Leseposition und Zeilenauswahl, aktueller Verlauf/Inhaltswechsel, gelöschte Ziele, fehlender Inhalt, readonly und Bestandsgrenze; Hauptentwurf und Dateibytes erhalten'


def fall_folgepaket_gestaltung(lauf):
    return fall_zweierpaket_gestaltung(lauf, selecting=True)


def fall_zweierpaket_gestaltung(lauf, selecting=False):
    """Neue Tagessteuerung/Suchnavigation bei kleiner Breite, großer Schrift und Verlauf."""
    from datetime import date
    app, mod = lauf.app, lauf.mod
    source, points, page = bestand(lauf)
    for point in points:
        point['planned_date'] = date.today().isoformat()
    if selecting:
        source['items'].extend(app.new_item(f'Weitere Tagesaufgabe {n}', planned_date=date.today().isoformat())
                               for n in range(11))
    points[0]['text'] = 'Lange Tagesaufgabe für die Abstimmung mit Planung und Projektleitung'
    app.settings['home_tile_order'] = ['today', 'focus']
    app.settings['home_tiles_hidden'] = [key for key in app.HOME_TILE_KEYS if key not in ('today', 'focus')]
    app.settings['release_notes_seen'] = mod.APP_VERSION
    assert app.save_items()
    configurations = [('light', '860x700', 'gross', False), ('dark', '1280x800', 'mittel', False),
                      ('glass_light', '1280x800', 'gross', False), ('light', '480x560', 'gross', True)]
    checked = 0

    def inspect(name):
        nonlocal checked
        count, findings = befunde_b15(lauf, name)
        checked += count
        assert not findings, findings[:6]
        if getattr(lauf, 'capture', None) is not None and sys.platform == 'win32':
            sys.path.insert(0, str(REPO / 'tests/tools'))
            from releasedaten import save_windows_screenshot
            lauf.capture.mkdir(parents=True, exist_ok=True)
            save_windows_screenshot(lauf.root, lauf.capture / (name + '.png'))

    for design, geometry, font, compact in configurations:
        app.settings['ui_font_size'] = font
        app.apply_ui_font()
        app.set_design(design)
        if design.startswith('glass'):
            app.set_backdrop_choice(mod.glide_backdrop.presets_for(design)[0].key)
        if compact:
            app.enter_compact_mode()
        lauf.root.geometry(geometry + '+20+20')
        app.set_home_view()
        if selecting:
            app.change_home_selection('start')
            app.change_home_selection('all')
        idle(lauf, 8)
        for position in (0, 0.5, 1):
            app.home_canvas.yview_moveto(position)
            idle(lauf)
            inspect(f'Tagessteuerung-{design}-{geometry}-{position}')
        if compact:
            app.leave_compact_mode()
        else:
            app.set_active_list(source['id'])
            app.settings['side_view_width'] = 280
            assert app.open_side_view(page['id'])
            app.open_side_search()
            app._side_search_entry.insert(0, 'Muster')
            app.update_side_search()
            idle(lauf, 6)
            inspect(f'Nebenansicht-{design}-{geometry}')
            app.close_side_view()
    return f'{checked} Knopfprüfungen; Tagessteuerung in vier Größen-/Schrift-/Designkonfigurationen und drei Scrolllagen, Nebenansicht mit Suche an Mindestbreite in drei Konfigurationen'


def phase348_bestand(lauf):
    from datetime import date, timedelta
    app, mod = lauf.app, lauf.mod
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    tasks = [app.new_item(f'Aufgabe {n:02}', planned_date=today, due=tomorrow, estimated_minutes=15)
             for n in range(12)]
    future = app.new_item('Morgen geplant, heute fällig', planned_date=tomorrow, due=today, estimated_minutes=30)
    first, second = app.new_list_object('Erste Quelle', tasks[:6]), app.new_list_object('Zweite Quelle', tasks[6:] + [future])
    app.lists, app.folders, app.trash = [first, second], [], []
    app.items, app.active_list_id = first['items'], first['id']
    app.settings['home_tile_order'] = ['today']
    app.settings['home_tiles_hidden'] = [key for key in app.HOME_TILE_KEYS if key != 'today']
    app.settings['release_notes_seen'] = mod.APP_VERSION
    app.settings['daily_capacity_minutes'] = 240
    app.settings.pop('daily_capacity_by_weekday', None)
    assert app.save_items()
    app.undo_stack.clear()
    app.set_home_view(); idle(lauf)
    return today, tomorrow, first, second, tasks, future


def phase348_button(lauf, title):
    return next(w for w in knoepfe(lauf.app.home_content, lauf.mod.RoundedButton)
                if w.text.rstrip(' .…').endswith(title.rstrip(' .…')))


def fall_home_tagesnavigation(lauf):
    app, mod = lauf.app, lauf.mod
    today, tomorrow, first, second, tasks, future = phase348_bestand(lauf)
    disk, depth = Path(mod.SAVE_FILE).read_bytes(), len(app.undo_stack)
    klick(phase348_button(lauf, 'Nächster Tag'), lauf)
    assert app.home_day() == tomorrow
    rows = [w for w in knoepfe(app.home_content, mod.RoundedButton) if hasattr(w, '_home_task_actions_id')]
    assert [w._home_task_actions_id for w in rows] == [future['id']]
    content = app.home_today_content({'today'}, app.home_summary(), lambda _: 'accent')
    assert not content.is_today and content.next_task is None and not content.show_goal
    assert content.open_total == 1 and 'Morgen' in content.day_title
    assert '30' in content.planning
    assert sum('12 offen' in row[0] for row in content.due_lists) == 0
    assert sum(int(row[0].rsplit('·', 1)[1].strip().split()[0]) for row in content.due_lists) == 12
    klick(phase348_button(lauf, 'Mehrere auswählen'), lauf)
    app.change_home_selection('all'); idle(lauf)
    assert app.home_selection_projection()['selected'] == (future['id'],)
    stale = app.build_home_batch_menu()
    klick(phase348_button(lauf, 'Heute'), lauf)
    assert app.home_day() == today and app.home_selection_projection() is None
    child = stale.nametowidget(stale.entrycget(0, 'menu'))
    child.invoke(3); idle(lauf)
    stale.destroy()
    assert app.find_item_in_lists(future['id'])[0]['importance'] == 0
    with patch.object(app, 'themed_due_dialog', return_value=None):
        app.choose_home_day()
    assert app.home_day() == today
    with patch.object(app, 'themed_due_dialog', return_value=(tomorrow, None)):
        klick(phase348_button(lauf, 'Datum'), lauf)
    assert app.home_day() == tomorrow
    assert Path(mod.SAVE_FILE).read_bytes() == disk and len(app.undo_stack) == depth
    klick(phase348_button(lauf, 'Tagesplan öffnen'), lauf)
    assert app.plan_day() == tomorrow and app.view_mode == app.PLAN_DAY_VIEW
    app.set_home_view(); app.change_home_day(); idle(lauf)
    app._data_read_only = True
    app.change_home_day(tomorrow); idle(lauf)
    assert app.home_day() == tomorrow and not app.home_today_content({'today'}, app.home_summary(), lambda _: 'accent').writable
    app._data_read_only = False
    # Datenpfadgrenze ohne Dateizugriff an einem fremden Ort.
    with patch.object(mod, 'SAVE_FILE', Path(lauf.data) / 'other' / 'liste.json'):
        assert app.home_day() == today
    return 'Tag vor/zurück/Datum/Heute, separate Plan-/Fälligkeitsbilanz, Auswahlgrenze, Abbruch, readonly und Bestandswechsel ohne Aufgaben-/Undo-Wirkung'


def fall_home_mehrfachfelder(lauf):
    app, mod = lauf.app, lauf.mod
    today, tomorrow, first, second, tasks, future = phase348_bestand(lauf)
    label = app.new_label_object('Gemeinsam')
    own = app.new_label_object('Bleibt bestehen')
    app.labels.extend([label, own])
    tasks[0]['labels'] = [own['id']]
    assert app.save_items()
    app.undo_stack.clear()
    klick(phase348_button(lauf, 'Mehrere auswählen'), lauf)
    klick(phase348_button(lauf, 'Alle auswählen'), lauf)
    identities = app.home_selection_projection()['selected']
    assert len(identities) == 12
    menu = app.build_home_batch_menu()
    importance = menu.nametowidget(menu.entrycget(0, 'menu'))
    importance.invoke(3); idle(lauf)
    menu.destroy()
    assert len(app.undo_stack) == 1
    assert all(app.find_item_in_lists(value)[0]['importance'] == 3 for value in identities)
    assert all(app.find_item_in_lists(value)[0]['due'] == tomorrow for value in identities)
    assert len(app.home_selection_projection()['selected']) == 12
    assert not app.apply_home_batch(identities, today, 'importance', 3)
    assert len(app.undo_stack) == 1
    app.undo_last_change(); idle(lauf)
    assert all(app.find_item_in_lists(value)[0]['importance'] == 0 for value in identities)
    app.redo_last_change(); idle(lauf)
    assert all(app.find_item_in_lists(value)[0]['importance'] == 3 for value in identities)
    depth = len(app.undo_stack)
    assert app.apply_home_batch(identities, today, 'label_add', label['id'])
    idle(lauf)
    assert len(app.undo_stack) == depth + 1
    assert own['id'] in app.find_item_in_lists(tasks[0]['id'])[0]['labels']
    assert all(label['id'] in app.find_item_in_lists(value)[0]['labels'] for value in identities)
    assert not app.apply_home_batch(identities, today, 'label_add', label['id'])
    assert app.apply_home_batch(identities, today, 'label_remove', label['id'])
    assert own['id'] in app.find_item_in_lists(tasks[0]['id'])[0]['labels']
    depth, disk = len(app.undo_stack), Path(mod.SAVE_FILE).read_bytes()
    with patch.object(app, 'refresh_data_lock', return_value=False):
        assert not app.apply_home_batch(identities, today, 'importance', 1)
    app._data_read_only = True
    assert not app.apply_home_batch(identities, today, 'importance', 1)
    app._data_read_only = False
    app.change_home_selection('clear')
    assert not app.apply_home_batch(identities, today, 'importance', 1)
    assert Path(mod.SAVE_FILE).read_bytes() == disk and len(app.undo_stack) == depth
    app.change_home_selection('all')
    with patch.object(app, 'save_items', return_value=False), patch.object(app, 'show_undo_toast') as feedback:
        assert not app.apply_home_batch(identities, today, 'importance', 1)
        feedback.assert_not_called()
    assert Path(mod.SAVE_FILE).read_bytes() == disk
    app.undo_last_change(); idle(lauf)
    klick(phase348_button(lauf, 'Auswahl bearbeiten'), lauf)
    assert app._action_chooser is not None
    app.close_action_chooser()
    assert not lauf.errors
    return '12 Aufgaben aus zwei Listen: Wichtigkeit/Labels, vorhandene Labels, No-op, ein Undo/Redo, stale Auswahl, Sperre/readonly und Schreibfehler ohne Erfolg'


def fall_side_verweisnavigation(lauf):
    app, mod = lauf.app, lauf.mod
    source, tasks, main = bestand(lauf)
    first = app.new_list_object('Quelle zum Nachschlagen', [])
    first['list_kind'] = 'page'
    target = app.new_list_object('Ziel mit Rückverweis', [])
    target['list_kind'] = 'page'
    value = mod.glide_objects.uri('list', target['id'])
    first['rich_note'] = {'text': 'Ziel öffnen\nWeiterer Text',
                         'spans': [{'tag':'link:ziel', 'start':0, 'end':11}], 'links': {'link:ziel':value}}
    app.lists.extend([first, target]); assert app.save_items()
    app.set_active_list(main['id']); idle(lauf)
    editor = app.rich_note_editor
    assert app.open_side_view(first['id']); idle(lauf)
    editor.text.insert('end-1c', '\nUnveränderter Hauptentwurf')
    # Das noch wartende <<Modified>> synchron verarbeiten, bevor sein
    # 400-ms-Schreibauftrag angehalten wird. Sonst entsteht der Auftrag erst
    # im nächsten idle() und schreibt bei langsamer Navigation im Hintergrund.
    editor.modified()
    assert editor._job is not None, "Die Textänderung hat ihren regulären Schreibauftrag angelegt"
    if editor._job is not None:
        editor.after_cancel(editor._job); editor._job = None
    assert 'Unveränderter Hauptentwurf' not in str(app.page_entry(main['id']).get('rich_note'))
    draft = editor.text.get('1.0', 'end-1c')
    disk, depth = Path(mod.SAVE_FILE).read_bytes(), len(app.undo_stack)
    body = app._side_view_body
    assert body.get(*body.tag_ranges('side_link_0')) == 'Ziel öffnen'
    box = body.bbox('1.2'); assert box
    body.event_generate('<Motion>', x=box[0]+2, y=box[1]+2)
    body.event_generate('<Button-1>', x=box[0]+2, y=box[1]+2)
    idle(lauf)
    assert app.side_view_entry()['id'] == target['id']
    assert app.active_list_id == main['id'] and app.rich_note_editor is editor
    menu = app.build_side_references_menu()
    incoming = menu.nametowidget(menu.entrycget(1, 'menu'))
    assert first['title'] in incoming.entrycget(0, 'label')
    incoming.invoke(0); idle(lauf); menu.destroy()
    assert app.side_view_entry()['id'] == first['id']
    app.move_side_history(-1); idle(lauf)
    assert app.side_view_entry()['id'] == target['id']
    app.move_side_history(1); idle(lauf)
    app.show_side_references(); idle(lauf)
    assert app._action_chooser is not None
    app.close_action_chooser()
    assert editor.text.get('1.0','end-1c') == draft
    assert Path(mod.SAVE_FILE).read_bytes() == disk and len(app.undo_stack) == depth
    app._data_read_only = True
    assert app.follow_side_reference(value, ('list', first['id']))
    app.move_side_history(-1); idle(lauf)
    app._data_read_only = False
    first['rich_note']['links'] = {}; app.clear_render_cache()
    assert not app.follow_side_reference(value, ('list', first['id']))
    assert app.side_view_entry()['id'] == first['id']
    assert Path(mod.SAVE_FILE).read_bytes() == disk
    return 'Echter Textlink, Rückverweis, Suchauswahl, Verlauf, readonly und veralteter Link; Hauptentwurf/Datei/Undo unverändert'


def fall_dreierpaket_gestaltung(lauf):
    app, mod = lauf.app, lauf.mod
    today, tomorrow, first, second, tasks, future = phase348_bestand(lauf)
    checked = 0
    for design, geometry, font in [('light', '860x700', 'mittel'), ('dark', '1280x800', 'gross'),
                                   ('glass_light', '860x700', 'gross'), ('light', '480x560', 'gross')]:
        app.settings['ui_font_size'] = font; app.apply_ui_font(); app.set_design(design)
        if design.startswith('glass'):
            app.set_backdrop_choice(mod.glide_backdrop.presets_for(design)[0].key)
        app.settings[mod.glide_interaction.HINTS_SETTING] = geometry != '860x700'
        compact = geometry == '480x560'
        if compact:
            app.enter_compact_mode()
        lauf.root.geometry(geometry + '+20+20')
        app.set_home_view(); app.change_home_day(tomorrow); idle(lauf, 8)
        app.change_home_selection('start'); app.change_home_selection('all'); idle(lauf, 8)
        for scroll in (0, 0.5, 1):
            app.home_canvas.yview_moveto(scroll); idle(lauf)
            count, findings = befunde_b15(lauf, f'dreierpaket-{design}-{geometry}-{scroll}')
            checked += count
            assert not findings, findings[:6]
            if scroll == 0 and lauf.capture is not None and sys.platform == 'win32':
                sys.path.insert(0, str(REPO / 'tests/tools'))
                from releasedaten import save_windows_screenshot
                lauf.capture.mkdir(parents=True, exist_ok=True)
                save_windows_screenshot(lauf.root, lauf.capture / (f'Tagesauswahl-{design}-{geometry}.png'))
        if compact:
            app.leave_compact_mode()
            continue
        app.set_active_list(first['id']); app.settings['side_view_width'] = 280
        assert app.open_side_view(second['id']); idle(lauf, 8)
        tree = app._side_view_body
        if 'due' in tree['displaycolumns']:
            assert tree.column('due', 'width') >= max(
                mod.tkfont.Font(font=mod.app_font(11)).measure(str(tree.item(i, 'values')[0])) + 18
                for i in tree.get_children())
        count, findings = befunde_b15(lauf, f'verweise-{design}-{geometry}')
        checked += count; assert not findings, findings[:6]
        if lauf.capture is not None and sys.platform == 'win32':
            sys.path.insert(0, str(REPO / 'tests/tools'))
            from releasedaten import save_windows_screenshot
            lauf.capture.mkdir(parents=True, exist_ok=True)
            save_windows_screenshot(lauf.root, lauf.capture / (f'Verweise-{design}-{geometry}.png'))
        app.close_side_view()
    return f'{checked} Knopfprüfungen; vier Größen-/Schrift-/Designkonfigurationen einschließlich Kompaktmodus, drei Scrolllagen, Nebenansicht 280 px und vollständige Datumswerte'


def fall_home_wochenwahl(lauf):
    app, mod = lauf.app, lauf.mod
    today, tomorrow, first, second, tasks, future = phase348_bestand(lauf)
    before, depth = Path(mod.SAVE_FILE).read_bytes(), len(app.undo_stack)
    klick(phase348_button(lauf, 'Woche'), lauf)
    assert app._action_chooser is not None
    app.close_action_chooser()
    menu = app.build_home_week_menu()
    days = menu.nametowidget(menu.entrycget(1, 'menu'))
    choices = mod.glide_task_tiles.week_choices(today)
    chosen = next(i for i, (value, _) in enumerate(choices) if value != today)
    app.change_home_selection('start'); app.change_home_selection('all')
    days.invoke(chosen); idle(lauf)
    assert app.home_day() == choices[chosen][0] and app.home_selection_projection() is None
    # Ein altes Menü darf nach dem Kontextwechsel keinen weiteren Tag setzen.
    days.invoke((chosen + 1) % len(choices)); idle(lauf)
    assert app.home_day() == choices[chosen][0]
    menu.destroy()
    app._data_read_only = True
    menu = app.build_home_week_menu()
    days = menu.nametowidget(menu.entrycget(2, 'menu')); days.invoke(0); idle(lauf)
    assert app.home_day() == mod.glide_task_tiles.week_choices(choices[chosen][0], 1)[0][0]
    menu.destroy(); app._data_read_only = False
    assert Path(mod.SAVE_FILE).read_bytes() == before and len(app.undo_stack) == depth
    return 'Echter Wochenknopf/Suchauswahl und Datumsmenü, Auswahlreset, alte Menüs wirkungslos, readonly lesend ohne Schreib-/Undo-Effekt'


def fall_home_faelligkeit_aufwand(lauf):
    app, mod = lauf.app, lauf.mod
    today, tomorrow, first, second, tasks, future = phase348_bestand(lauf)
    app.change_home_selection('start'); app.change_home_selection('all')
    identities = app.home_selection_projection()['selected']
    due = mod.glide_task_tiles.shift_day(tomorrow, 7)
    menu = app.build_home_batch_menu()
    effort = menu.nametowidget(menu.entrycget(menustelle(menu, 'Aufwand je Aufgabe'), 'menu'))
    effort.invoke(2); idle(lauf); menu.destroy()
    assert all(app.find_item_in_lists(i)[0]['estimated_minutes'] == 45 for i in identities)
    labels = [str(widget.cget('text')) for widget in knoepfe(app.home_content, mod.tk.Label)]
    assert any(app.format_estimated_minutes(12 * 45) in label for label in labels), labels
    assert len(app.undo_stack) == 1
    app.undo_last_change(); idle(lauf)
    assert all(app.find_item_in_lists(i)[0]['estimated_minutes'] == 15 for i in identities)
    app.redo_last_change(); idle(lauf)
    with patch.object(app, 'themed_due_dialog', return_value=(due, None)):
        assert app.choose_home_batch_value(identities, today, 'due')
    assert all(app.find_item_in_lists(i)[0]['due'] == due and
               app.find_item_in_lists(i)[0]['planned_date'] == today for i in identities)
    with patch.object(app, 'themed_input_dialog', return_value='1,5 h'):
        assert app.choose_home_batch_value(identities, today, 'estimated_minutes')
    assert all(app.find_item_in_lists(i)[0]['estimated_minutes'] == 90 for i in identities)
    saved, depth = Path(mod.SAVE_FILE).read_bytes(), len(app.undo_stack)
    with patch.object(app, 'themed_input_dialog', return_value=None):
        assert not app.choose_home_batch_value(identities, today, 'estimated_minutes')
    with patch.object(app, 'themed_due_dialog', return_value=None):
        assert not app.choose_home_batch_value(identities, today, 'due')
    assert Path(mod.SAVE_FILE).read_bytes() == saved and len(app.undo_stack) == depth
    def stale(*a, **kw):
        app.change_home_selection('clear')
        return '30'
    with patch.object(app, 'themed_input_dialog', side_effect=stale):
        assert not app.choose_home_batch_value(identities, today, 'estimated_minutes')
    assert Path(mod.SAVE_FILE).read_bytes() == saved
    app.change_home_selection('all')
    task = app.find_item_in_lists(identities[0])[0]
    task['repeat'] = {'art': 'taeglich'}
    before = copy.deepcopy(app.lists)
    assert not app.apply_home_batch(identities, today, 'due', tomorrow)
    assert app.lists == before
    menu = app.build_home_batch_menu()
    pos = next(i for i in range(menu.index('end') + 1) if menu.entrycget(i, 'label').startswith('Fälligkeit'))
    assert menu.entrycget(pos, 'state') == 'disabled'; menu.destroy()
    task['repeat'] = None
    app._data_read_only = True
    assert not app.apply_home_batch(identities, today, 'estimated_minutes', None)
    app._data_read_only = False
    with patch.object(app, 'save_items', return_value=False), patch.object(app, 'show_undo_toast') as success:
        assert not app.apply_home_batch(identities, today, 'estimated_minutes', 120)
        success.assert_not_called()
    assert Path(mod.SAVE_FILE).read_bytes() == saved
    app.undo_last_change(); idle(lauf)
    return '12 Aufgaben: echte Aufwandmenüaktion, ein Undo/Redo, Fälligkeit getrennt vom Bearbeitungstag, eigene Dauer, Abbruch/stale/Serien/readonly/Schreibfehler geschützt'


def fall_side_verweisaktionen(lauf):
    app, mod = lauf.app, lauf.mod
    source, tasks, main = bestand(lauf)
    first = app.new_list_object('Nachschlageliste', [])
    target = app.new_list_object('Verweisziel', [])
    other = app.new_list_object('Weiteres Ziel', [])
    value = mod.glide_objects.uri('list', target['id'])
    extra = mod.glide_objects.uri('list', other['id'])
    first['references'] = [value]
    fresh = lambda: next(entry for entry in app.lists if entry['id'] == first['id'])
    app.lists.extend([first, target, other]); assert app.save_items()
    app.set_active_list(main['id']); assert app.open_side_view(first['id']); idle(lauf)
    before, depth = Path(mod.SAVE_FILE).read_bytes(), len(app.undo_stack)
    menu = app.build_side_references_menu()
    actions = menu.nametowidget(menu.entrycget(menustelle(menu, 'Verweisaktionen'), 'menu'))
    row = actions.nametowidget(actions.entrycget(0, 'menu'))
    row.invoke(menustelle(row, 'Verweis kopieren')); idle(lauf)
    assert lauf.root.clipboard_get() == value and app.active_list_id == main['id']
    assert Path(mod.SAVE_FILE).read_bytes() == before and len(app.undo_stack) == depth
    menu.destroy()
    snapshot = app.snapshot_undo
    def replace_objects(*args, **kwargs):
        result = snapshot(*args, **kwargs)
        app.lists = copy.deepcopy(app.lists)
        app.sync_current_list_reference()
        return result
    with patch.object(app, 'themed_choice_dialog', return_value=extra), patch.object(app, 'snapshot_undo', side_effect=replace_objects):
        assert app.link_side_reference(('list', first['id']))
    idle(lauf)
    assert extra in fresh()['references'] and app.active_list_id == main['id']
    assert len(app.undo_stack) == depth + 1
    app.undo_last_change(); idle(lauf)
    assert extra not in fresh()['references']
    app.redo_last_change(); idle(lauf)
    assert extra in fresh()['references']
    fresh()['archived'] = True
    with patch.object(app, 'themed_choice_dialog') as choice:
        assert not app.link_side_reference(('list', first['id']))
        choice.assert_not_called()
    fresh()['archived'] = False
    app._data_read_only = True
    with patch.object(app, 'themed_choice_dialog') as choice:
        assert not app.link_side_reference(('list', first['id']))
        choice.assert_not_called()
    assert app.follow_side_reference(value, ('list', first['id']), action='copy')
    app._data_read_only = False
    def context_changed(*args, **kwargs):
        app.open_side_view(other['id'])
        return extra
    with patch.object(app, 'themed_choice_dialog', side_effect=context_changed):
        assert not app.link_side_reference(('list', first['id']))
    assert app.open_side_view(first['id']); idle(lauf)
    assert app.follow_side_reference(value, ('list', first['id']), action='main')
    assert app.active_list_id == target['id']
    app.open_side_view(first['id']); idle(lauf)
    fresh()['references'] = []
    assert not app.follow_side_reference(value, ('list', first['id']), action='copy')
    return 'Echte Verweisaktionen: Kopieren ohne Mutation, Hauptbereich öffnen, gezielt verknüpfen mit einem Undo/Redo, readonly und Dialog-/Beziehungswechsel geschützt'


def fall_side_trefferuebersicht(lauf):
    """Trefferübersicht der Nebenansicht: Abschnitt/Ausschnitt, Ansteuern, veraltete Einträge, Grenzen (31.10.2026)."""
    app, mod = lauf.app, lauf.mod
    main, editor = seite_anlegen(lauf, '# Hauptarbeit\n\nOffener Entwurf\n')
    other = app.new_page_from_markdown('# Überblick\n\n🎵 Straße und STRASSE. [x]\n\n'
        + '\n\n'.join(f'Absatz {number}' for number in range(35))
        + '\n\n## Abschluss\n\nEine weitere Straße.\n\n- [ ] Straße-Aufgabe\n')
    app.set_active_list(main['id']); idle(lauf)
    editor = app.rich_note_editor
    assert app.open_side_view(other['id']); idle(lauf)
    draft = editor.text.get('1.0', 'end-1c')
    model = copy.deepcopy(app.lists)
    written = Path(mod.SAVE_FILE).read_bytes()
    depth = len(app.undo_stack)
    klick(next(w for w in knoepfe(app.side_pane, mod.RoundedButton) if w.text == 'Suchen'), lauf)
    app._side_search_entry.insert(0, 'STRASSE'); app.update_side_search(); idle(lauf)
    assert len(app._side_search_matches) == 4

    def treffer_knopf():
        return next(w for w in knoepfe(app.side_pane, mod.RoundedButton)
                    if w.text == mod.RoundedButton.action_text('Treffer …'))
    menues = []

    def abfangen(menu, x, y):
        menues.append([(menu.type(i), menu.entrycget(i, 'label') if menu.type(i) != 'separator' else '',
                        menu.entrycget(i, 'state') if menu.type(i) != 'separator' else '')
                       for i in range(menu.index('end') + 1)])
        try:
            menu.invoke(2)
        finally:
            menu.unpost()

    with patch.object(mod.tk.Menu, 'tk_popup', new=abfangen):
        klick(treffer_knopf(), lauf)
    idle(lauf)
    eintraege = menues[-1]
    assert len(eintraege) == 4 and all(art == 'command' for art, _l, _s in eintraege), eintraege
    # Die erste Überschrift ist Seitentitel; Treffer davor tragen nur den Ausschnitt.
    assert ' · ' not in eintraege[0][1] and 'Straße' in eintraege[0][1], eintraege
    assert eintraege[3][1].startswith('Abschluss · '), eintraege
    assert all(len(label) <= 90 and '\n' not in label for _a, label, _s in eintraege)
    assert app._side_search_index == 2 and app._side_search_counter.cget('text') == '3 / 4 Treffer'
    body = app._side_view_body
    assert body.get(*body.tag_ranges('search_current')).casefold() == 'strasse'
    # Abschnittsauswahl nennt bei aktiver Suche die Treffer je Abschnitt (vor dem ersten Abschnitt keine Zeile).
    abschnitte = []

    def abschnitte_lesen(menu, x, y):
        abschnitte.extend(menu.entrycget(i, 'label').lstrip('✓ ') for i in range(menu.index('end') + 1))
        menu.unpost()
    with patch.object(mod.tk.Menu, 'tk_popup', new=abschnitte_lesen):
        klick(next(w for w in knoepfe(app.side_pane, mod.RoundedButton)
                   if w.text == mod.RoundedButton.action_text('Abschnitte …')), lauf)
    assert abschnitte == ['Abschluss · 2 Treffer'], abschnitte
    # Veralteter Eintrag: Suchtext geändert, Index bleibt, Zustand wird benannt.
    app._side_search_entry.delete(0, 'end'); app._side_search_entry.insert(0, 'Absatz 3'); app.update_side_search()
    vorher = app._side_search_index
    app.jump_side_match(other['id'], 'STRASSE', 1)
    assert app._side_search_index == vorher
    # Ohne Treffer kein Menü, Statuszeile bleibt maßgeblich.
    app._side_search_entry.delete(0, 'end'); app._side_search_entry.insert(0, 'Nicht vorhanden'); app.update_side_search()
    anzahl = len(menues)
    with patch.object(mod.tk.Menu, 'tk_popup', new=abfangen):
        klick(treffer_knopf(), lauf)
    assert len(menues) == anzahl and app._side_search_counter.cget('text') == 'Keine Treffer.'
    assert app.active_list_id == main['id'] and app.rich_note_editor is editor
    assert editor.text.get('1.0', 'end-1c') == draft
    assert app.lists == model and Path(mod.SAVE_FILE).read_bytes() == written and len(app.undo_stack) == depth
    app.close_side_view()
    # Viele Treffer: höchstens 50 Einträge, danach gesperrter Hinweis.
    viel = app.new_page_from_markdown('# Viele\n\n' + '\n\n'.join(f'Treffer {n}' for n in range(60)) + '\n')
    assert app.open_side_view(viel['id']); app.open_side_search(); idle(lauf)
    app._side_search_entry.insert(0, 'Treffer'); app.update_side_search()

    def nur_lesen(menu, x, y):
        menues.append([(menu.type(i), menu.entrycget(i, 'label') if menu.type(i) != 'separator' else '',
                        menu.entrycget(i, 'state') if menu.type(i) != 'separator' else '')
                       for i in range(menu.index('end') + 1)])
        menu.unpost()
    with patch.object(mod.tk.Menu, 'tk_popup', new=nur_lesen):
        klick(treffer_knopf(), lauf)
    eintraege = menues[-1]
    befehle = [e for e in eintraege if e[0] == 'command' and e[2] != 'disabled']
    assert len(befehle) == 50 and eintraege[-1][2] == 'disabled' and '10 weitere Treffer' in eintraege[-1][1], eintraege[-3:]
    app.close_side_view()
    # Liste: Gruppen sind Abschnitte, Treffer zeigen den Aufgabentitel.
    listing = app.new_list_object('Nachschlageliste')
    group = app.new_item('Abschnitt Nord', kind=app.ITEM_KIND_GROUP)
    group['children'] = [app.new_item('Straße prüfen'), app.new_item('STRASSE messen')]
    listing['items'] = [app.new_item('Vor der Gruppe Straße'), group]
    app.lists.append(listing)
    assert app.open_side_view(listing['id']); app.open_side_search(); idle(lauf)
    app._side_search_entry.insert(0, 'strasse'); app.update_side_search()
    with patch.object(mod.tk.Menu, 'tk_popup', new=nur_lesen):
        klick(treffer_knopf(), lauf)
    # Beschriftung wie die sichtbare Zeile, einschließlich Kästchenzeichen.
    labels = [label.replace(app.ICONS['task_open'] + ' ', '') for art, label, _s in menues[-1] if art == 'command']
    assert labels == ['Vor der Gruppe Straße', 'Abschnitt Nord · Straße prüfen', 'Abschnitt Nord · STRASSE messen'], labels
    # B15: Knopfzeile mit offener Suche in schmaler Nebenansicht.
    geprueft = 0
    app.set_active_list(main['id'])
    for design, geometry, font in [('light', '860x700', 'mittel'), ('dark', '1280x800', 'gross'),
                                   ('glass_light', '860x700', 'gross')]:
        app.settings['ui_font_size'] = font; app.apply_ui_font(); app.set_design(design)
        if design.startswith('glass'):
            app.set_backdrop_choice(mod.glide_backdrop.presets_for(design)[0].key)
        lauf.root.geometry(geometry + '+20+20'); app.settings['side_view_width'] = 280
        assert app.open_side_view(other['id']); app.open_side_search(); idle(lauf, 8)
        app._side_search_entry.insert(0, 'Straße'); app.update_side_search(); idle(lauf)
        treffer_knopf()
        count, findings = befunde_b15(lauf, f'trefferuebersicht-{design}-{geometry}')
        geprueft += count
        assert not findings, findings[:6]
        app.close_side_view()
    return (f'Abschnitt/Ausschnitt je Treffer, Ansteuern über den Suchweg, veraltete Einträge und kein Treffer wirkungslos, '
            f'50er-Grenze, Listengruppen; Modell/Datei/Undo/Haupteditor unverändert; {geprueft} Knopfprüfungen')


def fall_side_nachschlagen(lauf):
    """Markierung im Haupteditor in der Nebenansicht nachschlagen: Sperrgrund, Suche, readonly, nichts geändert."""
    app, mod = lauf.app, lauf.mod
    main, editor = seite_anlegen(lauf, '# Hauptarbeit\n\nBitte die Straße prüfen.\n')
    other = app.new_page_from_markdown('# Überblick\n\nStraße und STRASSE.\n\n## Abschluss\n\nEine weitere Straße.\n')
    app.set_active_list(main['id']); idle(lauf)
    editor = app.rich_note_editor
    start = editor.text.search('Straße', '1.0', 'end')
    editor.text.tag_add('sel', start, f'{start}+6c'); idle(lauf, 1)
    label = mod.glide_action_menu.SIDE_LOOKUP_LABEL

    def eintrag(menu):
        return next(i for i in range(menu.index('end') + 1)
                    if menu.type(i) == 'command' and menu.entrycget(i, 'label') == label)
    menu = editor.build_context_menu()
    assert menu.entrycget(eintrag(menu), 'state') == 'disabled', 'ohne Nebenansicht gesperrt'
    assert mod.glide_action_menu.reason_for(label, (), editor.action_context()) == mod.glide_action_menu.SIDE_VIEW_REASON
    menu.destroy()
    assert app.open_side_view(other['id']); idle(lauf)
    draft = editor.text.get('1.0', 'end-1c')
    model = copy.deepcopy(app.lists)
    written = Path(mod.SAVE_FILE).read_bytes()
    depth = len(app.undo_stack)
    menu = editor.build_context_menu()
    assert menu.entrycget(eintrag(menu), 'state') == 'normal'
    menu.invoke(eintrag(menu)); menu.destroy(); idle(lauf)
    assert app._side_search_open and app._side_search_entry.get() == 'Straße'
    assert len(app._side_search_matches) == 3 and app._side_search_counter.cget('text') == '1 / 3 Treffer'
    body = app._side_view_body
    assert body.get(*body.tag_ranges('search_current')) == 'Straße'
    assert app.active_list_id == main['id'] and app.rich_note_editor is editor
    assert editor.text.get('1.0', 'end-1c') == draft
    assert app.lists == model and Path(mod.SAVE_FILE).read_bytes() == written and len(app.undo_stack) == depth
    # Ohne Markierung gesperrt mit Markierungsgrund; im Schreibschutz weiter verfügbar.
    editor.text.tag_remove('sel', '1.0', 'end')
    menu = editor.build_context_menu()
    assert menu.entrycget(eintrag(menu), 'state') == 'disabled'
    assert mod.glide_action_menu.reason_for(label, (), editor.action_context()) == mod.glide_action_menu.SELECTION_REASON
    menu.destroy()
    app._data_read_only = True
    try:
        bitte = editor.text.search('Bitte', '1.0', 'end')
        editor.text.tag_add('sel', bitte, f'{bitte}+5c')
        menu = editor.build_context_menu()
        assert menu.entrycget(eintrag(menu), 'state') == 'normal', 'lesend auch im Schreibschutz'
        menu.destroy()
        assert editor.search_selection_in_side_view() == 'break' and app._side_search_entry.get() == 'Bitte'
    finally:
        app._data_read_only = False
    # Durchsuchbare Blockaktionen enthalten denselben Eintrag aus dem Kontextmenü.
    zeilen = editor.build_context_menu()
    try:
        assert label in [zeilen.entrycget(i, 'label') for i in range(zeilen.index('end') + 1) if zeilen.type(i) == 'command']
    finally:
        zeilen.destroy()
    app.close_side_view()
    # Aufgaben-Kontextmenü: Titel einer Zeile nachschlagen, nur mit offener Nebenansicht.
    liste = app.new_list_object('Nachschlagen aus Liste')
    aufgabe = app.new_item('Straße')
    liste['items'] = [aufgabe]; app.lists.append(liste); assert app.save_items()
    app.set_active_list(liste['id']); idle(lauf)
    app.tree.selection_set(aufgabe['id']); app.tree.focus(aufgabe['id'])
    kontext = app.build_item_context_menu()
    assert 'Titel in Nebenansicht suchen' not in [kontext.entrycget(i, 'label') for i in range(kontext.index('end') + 1)
                                                if kontext.type(i) == 'command']
    kontext.destroy()
    assert app.open_side_view(other['id']); idle(lauf)
    app.tree.selection_set(aufgabe['id']); app.tree.focus(aufgabe['id'])
    model = copy.deepcopy(app.lists); written = Path(mod.SAVE_FILE).read_bytes(); depth = len(app.undo_stack)
    kontext = app.build_item_context_menu()
    index = next(i for i in range(kontext.index('end') + 1)
                 if kontext.type(i) == 'command' and kontext.entrycget(i, 'label') == 'Titel in Nebenansicht suchen')
    kontext.invoke(index); idle(lauf); kontext.destroy()
    assert app._side_search_entry.get() == 'Straße' and len(app._side_search_matches) == 3
    assert app.lists == model and Path(mod.SAVE_FILE).read_bytes() == written and len(app.undo_stack) == depth
    app.close_side_view()
    return ('Sperrgrund ohne Nebenansicht/Markierung, Suche mit erstem Treffer, readonly verfügbar, Blockaktionen, '
            'Aufgabentitel aus dem Kontextmenü; Modell/Datei/Undo/Haupteditor unverändert')


def fall_home_fokusdauer(lauf):
    """Fokusdauer 15/25/50 Minuten: Mehr-Menü startet und merkt die Vorgabe, Intervall, Sperre, Fehler, Neustart."""
    from datetime import date, datetime, timedelta
    app, mod = lauf.app, lauf.mod
    today = date.today().isoformat()
    source = app.new_list_object('Fokusdauer')
    task = app.new_item('Konzept schreiben', planned_date=today, estimated_minutes=30)
    weitere = app.new_item('Antwort formulieren', planned_date=today)
    blocker = app.new_item('Freigabe abwarten', planned_date=today)
    blocked = app.new_item('Noch blockiert', planned_date=today, blocked_by=[blocker['id']])
    source['items'] = [task, weitere, blocker, blocked]
    app.lists, app.folders, app.labels, app.trash = [source], [], [], []
    app.items, app.active_list_id = source['items'], source['id']
    app.settings['release_notes_seen'] = mod.APP_VERSION
    app.settings.pop('focus_minutes', None)
    app.clear_render_cache(); assert app.save_items(); app.set_home_view(); idle(lauf)

    def dauer_menue(item_id):
        menu = app.build_home_task_menu(item_id)
        index = next(i for i in range(menu.index('end') + 1)
                     if menu.type(i) == 'cascade' and menu.entrycget(i, 'label') == 'Fokus für')
        unter = menu.nametowidget(menu.entrycget(index, 'menu'))
        return menu, index, unter
    menu, index, unter = dauer_menue(task['id'])
    labels = [unter.entrycget(i, 'label') for i in range(unter.index('end') + 1) if unter.type(i) == 'command']
    # Aufwand 30 Minuten der Aufgabe als eigene Sitzungsdauer, keine Vorgabe.
    assert [l.strip() for l in labels] == ['15 Minuten', '✓ 25 Minuten', '50 Minuten', 'Aufwand · 30 Minuten'], labels
    assert menu.entrycget(1, 'label') == 'Fokus starten' and menu.entrycget(index, 'state') == 'normal'
    # Speicherfehler: kein Timer, Vorgabe unverändert. Menübefehle laufen unter macOS über after_idle,
    # deshalb den Leerlauf noch innerhalb des simulierten Fehlers abarbeiten.
    with patch.object(app, 'save_settings', return_value=False):
        unter.invoke(0); idle(lauf)
    assert not app.running_timer() and app.settings.get('focus_minutes') == 25
    menu.destroy()
    menu, index, unter = dauer_menue(task['id'])
    unter.invoke(0); idle(lauf); menu.destroy()
    timer = app.running_timer()
    assert timer['item_id'] == task['id'] and timer['goal_seconds'] == 900 and timer['interval_seconds'] == 900
    saved = json.loads(Path(mod.SETTINGS_FILE).read_text(encoding='utf-8'))
    assert saved['focus_minutes'] == 15 and saved['time_tracking']['interval_seconds'] == 900
    menu, index, unter = dauer_menue(task['id'])
    assert unter.entrycget(0, 'label').startswith('✓'), 'neue Vorgabe markiert'
    menu.destroy()
    app.stop_time_tracking()
    # „Fokus starten“ nutzt jetzt 15 Minuten; nach Intervallende verlängert Fortsetzen um 15.
    start = datetime.now().astimezone() - timedelta(minutes=16)
    assert app.start_focus(weitere['id'], now=start); idle(lauf)
    assert app.running_timer()['goal_seconds'] == 900 and app.timer_minutes() == 15
    app.toggle_focus_pause(); app.toggle_focus_pause()
    assert app.running_timer()['goal_seconds'] == 1800, app.running_timer()
    app.stop_time_tracking()
    # +5 Minuten im Fokusfeld: am Intervallende weiter um fünf Minuten; Speicherfehler ändert nichts.
    assert app.start_focus(weitere['id'], now=datetime.now().astimezone() - timedelta(minutes=16)); idle(lauf)
    app.update_timer_indicator()
    assert app.running_timer()['started_at'] is None and app.running_timer()['goal_seconds'] == 900
    vorher = app.running_timer()
    with patch.object(app, 'save_settings', return_value=False):
        app.extend_focus()
    assert app.running_timer() == vorher
    app.sync_focus_panel(); idle(lauf)
    klick(next(w for w in knoepfe(app.focus_panel, mod.RoundedButton) if w.text == '+5 Minuten'), lauf)
    timer = app.running_timer()
    assert timer['goal_seconds'] == 1200 and timer['started_at'] is not None, timer
    assert app.focus_clock_label.cget('text').startswith('Noch 0'), app.focus_clock_label.cget('text')
    app.stop_time_tracking()
    # Aufwand: 30 Minuten nur für diese Sitzung; die Vorgabe bleibt 15.
    app.set_home_view(); idle(lauf)
    menu, index, unter = dauer_menue(task['id'])
    unter.invoke(unter.index('end')); idle(lauf); menu.destroy()
    assert app.running_timer()['interval_seconds'] == 1800 and app.running_timer()['goal_seconds'] == 1800
    assert app.settings['focus_minutes'] == 15
    app.stop_time_tracking()
    # Ohne Aufwand oder mit einer Vorgabedauer als Aufwand kein Zusatzeintrag.
    app.set_home_view(); idle(lauf)
    menu, index, unter = dauer_menue(weitere['id'])
    assert [unter.entrycget(i, 'label').strip() for i in range(unter.index('end') + 1) if unter.type(i) == 'command'] == \
        ['✓ 15 Minuten', '25 Minuten', '50 Minuten']
    menu.destroy()
    # Blockierte Aufgabe: Untermenü gesperrt.
    app.set_home_view(); idle(lauf)
    menu, index, unter = dauer_menue(blocked['id'])
    assert menu.entrycget(index, 'state') == 'disabled'
    menu.destroy()
    # Aufgaben-Kontextmenü › Beziehungen und Zeit: Fokus mit Vorgabe bzw. nach Aufwand.
    app.set_active_list(source['id']); idle(lauf)

    def zeitmenue(item_id):
        app.tree.selection_set(item_id); app.tree.focus(item_id)
        kontext = app.build_item_context_menu()
        index = next(i for i in range(kontext.index('end') + 1)
                     if kontext.type(i) == 'cascade' and kontext.entrycget(i, 'label') == 'Beziehungen und Zeit')
        return kontext, kontext.nametowidget(kontext.entrycget(index, 'menu'))
    kontext, zeit = zeitmenue(task['id'])
    eintraege = {zeit.entrycget(i, 'label'): i for i in range(zeit.index('end') + 1) if zeit.type(i) == 'command'}
    assert 'Fokus starten · 15 Minuten' in eintraege and 'Fokus nach Aufwand · 30 Minuten' in eintraege, eintraege
    zeit.invoke(eintraege['Fokus nach Aufwand · 30 Minuten']); idle(lauf); kontext.destroy()
    assert app.running_timer()['interval_seconds'] == 1800 and app.settings['focus_minutes'] == 15
    app.stop_time_tracking()
    app.set_active_list(source['id']); idle(lauf)
    kontext, zeit = zeitmenue(task['id'])
    eintraege = {zeit.entrycget(i, 'label'): i for i in range(zeit.index('end') + 1) if zeit.type(i) == 'command'}
    zeit.invoke(eintraege['Fokus starten · 15 Minuten']); idle(lauf); kontext.destroy()
    assert app.running_timer()['interval_seconds'] == 900
    app.stop_time_tracking()
    app.set_active_list(source['id']); idle(lauf)
    kontext, zeit = zeitmenue(blocked['id'])
    zustand = {zeit.entrycget(i, 'label'): zeit.entrycget(i, 'state') for i in range(zeit.index('end') + 1) if zeit.type(i) == 'command'}
    assert zustand['Fokus starten · 15 Minuten'] == 'disabled', zustand
    kontext.destroy()
    # Neustart: Vorgabe bleibt, laufende 50-Minuten-Sitzung behält ihr Intervall.
    app.set_home_view(); idle(lauf)  # Fokusstart wechselt nach Heute; das Mehr-Menü gehört zur Startseite.
    menu, index, unter = dauer_menue(task['id'])
    unter.invoke(2); idle(lauf); menu.destroy()
    assert app.running_timer()['interval_seconds'] == 3000 and app.settings['focus_minutes'] == 50
    lauf.neustart(); app, mod = lauf.app, lauf.mod
    assert app.settings['focus_minutes'] == 50 and app.running_timer()['interval_seconds'] == 3000
    app.stop_time_tracking()
    return ('Mehr-Menü „Fokus für“ mit Vorgabe-Häkchen, Start 15/50 min, Aufwand 30 min ohne Vorgabe, gespeicherte Vorgabe, '
            'Intervall/Fortsetzen, +5 Minuten, Sperre, Speicherfehler, Neustart, Aufgaben-Kontextmenü')


def fall_fokus_wechseln(lauf):
    """Fokusfeld „Wechseln zu …“: nächste Tagesaufgaben in Rangfolge, Wechsel bucht, veraltete Wahl wirkungslos."""
    from datetime import date, datetime, timedelta
    from unittest.mock import MagicMock
    app, mod = lauf.app, lauf.mod
    today = date.today().isoformat()
    source = app.new_list_object('Fokuswechsel')
    aktuell = app.new_item('Konzept schreiben', planned_date=today)
    wichtig = app.new_item('Angebot prüfen', planned_date=today, importance=3)
    normal = app.new_item('Antwort formulieren', planned_date=today)
    blocker = app.new_item('Freigabe abwarten', planned_date=today)
    blockiert = app.new_item('Noch blockiert', planned_date=today, blocked_by=[blocker['id']])
    erledigt = app.new_item('Schon erledigt', planned_date=today, done=True)
    morgen = app.new_item('Erst morgen', planned_date=(date.today() + timedelta(days=1)).isoformat())
    # Ungekürzter Altbestand bleibt lesbar; neue Titel sind seit D63 auf 40 begrenzt.
    lang = app.new_item('Sehr langer Aufgabentitel ' * 5, planned_date=today, preserve_title=True)
    source['items'] = [aktuell, wichtig, normal, blocker, blockiert, erledigt, morgen, lang]
    app.lists, app.folders, app.labels, app.trash = [source], [], [], []
    app.items, app.active_list_id = source['items'], source['id']
    app.settings['release_notes_seen'] = mod.APP_VERSION
    app.clear_render_cache(); assert app.save_items(); app.set_home_view(); idle(lauf)
    aufgabe = lambda item: app.find_item_in_lists(item['id'])[0]

    assert app.start_focus(aktuell['id'], now=datetime.now().astimezone() - timedelta(minutes=3)); idle(lauf)
    app.sync_focus_panel(); idle(lauf)
    knopf = next(w for w in knoepfe(app.focus_panel, mod.RoundedButton)
                 if w.text in ('Wechseln zu …', mod.RoundedButton.action_text('Wechseln zu …')))
    assert app.focus_switch_button is knopf
    assert knopf._accessible_name == 'Fokus zu einer anderen Tagesaufgabe wechseln'
    # Der Knopf öffnet das Menü (Popup als Attrappe, damit der Lauf nicht modal hängt).
    attrappe = MagicMock()
    with patch.object(app, 'build_focus_switch_menu', return_value=attrappe):
        klick(knopf, lauf)
    assert attrappe.tk_popup.called and attrappe.grab_release.called
    kandidaten = app.focus_candidates(exclude=aktuell['id'])
    ids = [item['id'] for item in kandidaten]
    assert set(ids) == {wichtig['id'], normal['id'], blocker['id'], lang['id']}, ids
    assert ids[0] == wichtig['id'] == app.focus_candidate(exclude=aktuell['id'])['id']
    menu = app.build_focus_switch_menu()
    labels = [menu.entrycget(i, 'label') for i in range(menu.index('end') + 1)]
    assert labels[0] == 'Zeit buchen und wechseln zu' and menu.entrycget(0, 'state') == 'disabled', labels
    assert [l.strip() for l in labels[1:]] == [mod.glide_focus.switch_label(item['text']) for item in kandidaten], labels
    assert all(len(l.strip()) <= mod.glide_focus.SWITCH_TITLE_LIMIT for l in labels[1:])
    assert any(l.endswith('…') for l in labels), labels
    # Wechsel: laufende Zeit gebucht, gewählte Aufgabe im Fokus.
    menu.invoke(1 + ids.index(normal['id'])); idle(lauf); menu.destroy()
    assert app.running_timer()['item_id'] == normal['id'] and app.running_timer().get('focus')
    assert (aufgabe(aktuell).get('time_spent_minutes') or 0) >= 3, aufgabe(aktuell)
    # Veraltete Wahl: Ziel inzwischen erledigt – Warnung, Sitzung bleibt.
    menu = app.build_focus_switch_menu()
    eintrag = next(i for i in range(menu.index('end') + 1)
                   if menu.entrycget(i, 'label').strip() == mod.glide_focus.switch_label(wichtig['text']))
    assert app.toggle_item_done_anywhere(wichtig['id']); idle(lauf)
    vorher = app.running_timer()
    with patch.object(app, 'show_warning') as warnung:
        menu.invoke(eintrag); idle(lauf)
    menu.destroy()
    assert warnung.called and 'erneut öffnen' in warnung.call_args.args[1], warnung.call_args
    assert app.running_timer() == vorher
    # Speicherfehler beim Start: nichts gewechselt, keine Buchung verloren.
    menu = app.build_focus_switch_menu()
    with patch.object(app, 'save_settings', return_value=False):
        menu.invoke(1); idle(lauf)
    menu.destroy()
    assert app.running_timer() is None or app.running_timer()['item_id'] == normal['id'], app.running_timer()
    app.stop_time_tracking()
    # Keine weitere Aufgabe: einziger, gesperrter Hinweis.
    for item in (normal, blocker, blockiert, lang):
        aufgabe(item)['done'] = True
    app.clear_render_cache(); assert app.save_items(); idle(lauf)
    assert app.start_focus(aktuell['id']); idle(lauf)
    menu = app.build_focus_switch_menu()
    assert menu.index('end') == 0 and menu.entrycget(0, 'label') == 'Keine weitere offene Aufgabe für heute'
    assert menu.entrycget(0, 'state') == 'disabled'
    menu.destroy()
    app.stop_time_tracking()
    # Ohne laufenden Fokus bewirkt ein Wechsel nichts.
    assert app.switch_focus(normal['id']) == 'break' and app.running_timer() is None
    # Mehr als fünf Kandidaten: fünf wählbar, danach gesperrt die Zahl der übrigen.
    source['items'].extend(app.new_item(f'Weitere Aufgabe {n}', planned_date=today) for n in range(7))
    app.clear_render_cache(); assert app.save_items(); idle(lauf)
    assert app.start_focus(aktuell['id']); idle(lauf)
    menu = app.build_focus_switch_menu()
    labels = [menu.entrycget(i, 'label') for i in range(menu.index('end') + 1)]
    assert len(labels) == 1 + mod.glide_focus.SWITCH_LIMIT + 1, labels
    assert labels[-1].strip() == '… und 2 weitere für heute' and menu.entrycget('end', 'state') == 'disabled', labels
    assert all(menu.entrycget(i, 'state') == 'normal' for i in range(1, 1 + mod.glide_focus.SWITCH_LIMIT))
    menu.destroy()
    app.stop_time_tracking()
    return ('Fokusfeld „Wechseln zu …“: Knopf öffnet Menü, bis zu fünf Tagesaufgaben in Rangfolge von „Nächste Aufgabe“ '
            'ohne Blockierte/Erledigte/andere Tage, gekürzte Titel, Wechsel bucht Zeit, veraltete Wahl mit Warnung, '
            'Speicherfehler, leere Wahl, Zahl der übrigen jenseits der Grenze')


def fall_side_suchverlauf(lauf):
    """Letzte Suchen der Nebenansicht: nur bewusst genutzte Suchen mit Treffer, erneut suchen, Grenze, lesend (01.11.2026)."""
    app, mod = lauf.app, lauf.mod
    main, editor = seite_anlegen(lauf, '# Hauptarbeit\n\nOffener Entwurf\n')
    other = app.new_page_from_markdown('# Überblick\n\nAngebot und Termin.\n\nNoch ein Angebot.\n\n'
                                       '## Abschluss\n\nTermin bestätigt.\n')
    app.set_active_list(main['id']); idle(lauf)
    editor = app.rich_note_editor
    assert app.open_side_view(other['id']); idle(lauf)
    draft = editor.text.get('1.0', 'end-1c')
    model = copy.deepcopy(app.lists)
    written = Path(mod.SAVE_FILE).read_bytes()
    depth = len(app.undo_stack)
    klick(next(w for w in knoepfe(app.side_pane, mod.RoundedButton) if w.text == 'Suchen'), lauf)

    def knopf(text):
        return next(w for w in knoepfe(app.side_pane, mod.RoundedButton)
                    if w.text in (text, mod.RoundedButton.action_text(text)))

    def suchen(text):
        feld = app._side_search_entry
        feld.delete(0, 'end'); feld.insert(0, text); app.update_side_search()
    menues = []

    def lesen(menu, x, y):
        menues.append([('—', '') if menu.type(i) == 'separator' else (menu.entrycget(i, 'label'), menu.entrycget(i, 'state'))
                       for i in range(menu.index('end') + 1)])
        menu.unpost()
    with patch.object(mod.tk.Menu, 'tk_popup', new=lesen):
        klick(knopf('Letzte Suchen …'), lauf)
    assert menues[-1] == [('Noch keine Suche in dieser Sitzung', 'disabled')], menues
    # Tippen allein merkt nichts; „Weiter“ merkt die genutzte Suche mit Treffer.
    for teil in ('A', 'An', 'Angebot'):
        suchen(teil)
    assert app.side_recent_searches() == []
    klick(knopf('Weiter'), lauf)
    assert app.side_recent_searches() == ['Angebot']
    # Ohne Treffer wird nichts gemerkt.
    suchen('Nicht vorhanden'); klick(knopf('Weiter'), lauf)
    assert app.side_recent_searches() == ['Angebot']
    suchen('Termin'); klick(knopf('Zurück'), lauf)
    assert app.side_recent_searches() == ['Termin', 'Angebot']
    # Nachschlagen aus der Markierung zählt als Nutzung.
    app.search_side_view('Abschluss'); idle(lauf)
    assert app.side_recent_searches() == ['Abschluss', 'Termin', 'Angebot']
    with patch.object(mod.tk.Menu, 'tk_popup', new=lesen):
        klick(knopf('Letzte Suchen …'), lauf)
    assert [label for label, _s in menues[-1]] == ['✓ Abschluss', '    Termin', '    Angebot', '—', '    Liste leeren'], menues[-1]
    # Häkchenspalte: „✓ “ und die Leerstelle sind in der Menüschrift fast gleich breit (Design Richtlinien, 01.11.2026).
    import tkinter.font as tkfont
    probe = app._new_themed_popup_menu()
    schrift = tkfont.Font(root=app.root, font=probe.cget('font'))
    versatz = abs(schrift.measure('✓ ') - schrift.measure(mod.glide_action_menu.CHECK_PAD))
    probe.destroy()
    assert versatz <= 2, (schrift.actual(), versatz)
    # Wahl sucht den Begriff erneut und zeigt den ersten Treffer.

    def waehlen(menu, x, y):
        try:
            menu.invoke(2)
        finally:
            menu.unpost()
    with patch.object(mod.tk.Menu, 'tk_popup', new=waehlen):
        klick(knopf('Letzte Suchen …'), lauf)
    idle(lauf)
    assert app._side_search_entry.get() == 'Angebot' and app._side_search_query == 'Angebot'
    assert app._side_search_counter.cget('text') == '1 / 2 Treffer', app._side_search_counter.cget('text')
    assert app.side_recent_searches() == ['Angebot', 'Abschluss', 'Termin']
    # Grenze: höchstens acht Begriffe, der zuletzt genutzte vorn.
    for teil in ('An', 'Ang', 'Ange', 'Angeb', 'Angebo', 'Ter', 'Term', 'Termi'):
        app.search_side_view(teil)
    assert len(app.side_recent_searches()) == mod.glide_side_view.RECENT_LIMIT
    assert app.side_recent_searches()[0] == 'Termi'
    # Pfeil hoch/runter im Suchfeld blättert, ohne die Liste zu ändern; die Suche folgt.
    stand = list(app.side_recent_searches())
    feld = app._side_search_entry
    feld.delete(0, 'end'); feld.insert(0, 'getippt'); feld.focus_force(); idle(lauf)
    for taste, erwartet in (('<Up>', stand[0]), ('<Up>', stand[1]), ('<Down>', stand[0]), ('<Down>', stand[0])):
        feld.event_generate(taste); idle(lauf)
        assert feld.get() == erwartet, (taste, feld.get(), erwartet)
    assert app._side_search_query == stand[0] and app.side_recent_searches() == stand
    # „Liste leeren“ als letzter Eintrag verwirft die Begriffe; Suchfeld und Treffer bleiben.
    feld_vorher, treffer_vorher = app._side_search_entry.get(), len(app._side_search_matches)

    def leeren(menu, x, y):
        letzte = menu.index('end')
        assert menu.type(letzte - 1) == 'separator' and menu.entrycget(letzte, 'label').strip() == 'Liste leeren'
        try:
            menu.invoke(letzte)
        finally:
            menu.unpost()
    with patch.object(mod.tk.Menu, 'tk_popup', new=leeren):
        klick(knopf('Letzte Suchen …'), lauf)
    idle(lauf)
    assert app.side_recent_searches() == []
    assert app._side_search_entry.get() == feld_vorher and len(app._side_search_matches) == treffer_vorher
    with patch.object(mod.tk.Menu, 'tk_popup', new=lesen):
        klick(knopf('Letzte Suchen …'), lauf)
    assert menues[-1] == [('Noch keine Suche in dieser Sitzung', 'disabled')], menues[-1]
    app.search_side_view('Termi')
    # Anderer Datenordner: keine Begriffe aus einem anderen Bestand.
    with patch.object(mod, 'SAVE_FILE', Path(mod.SAVE_FILE).with_name('anderer.json')):
        assert app.side_recent_searches() == []
    # Lesend: Hauptarbeit, Modell, Datei und Undo unverändert.
    assert app.active_list_id == main['id'] and app.rich_note_editor is editor
    assert editor.text.get('1.0', 'end-1c') == draft
    assert app.lists == model and Path(mod.SAVE_FILE).read_bytes() == written and len(app.undo_stack) == depth
    anzahl, befunde = befunde_b15(lauf, 'Nebenansicht Letzte Suchen')
    assert anzahl and not befunde, befunde[:4]
    app.close_side_view()
    return ('Nebenansicht „Letzte Suchen …“: leer gesperrt, Tippen merkt nichts, Weiter/Zurück/Nachschlagen merken nur '
            'Suchen mit Treffer, ✓ am aktuellen Begriff, Wahl sucht erneut, Grenze 8, Pfeiltasten, Liste leeren, Datenordnergrenze, lesend, Knopfprüfung')


def fall_fokus_als_naechstes(lauf):
    """Fokusfeld „Als Nächstes: …“: dieselbe Aufgabe wie „Nächste Aufgabe“, folgt Änderungen und Undo, kein Sekundentakt-Scan."""
    from datetime import date
    app, mod = lauf.app, lauf.mod
    today = date.today().isoformat()
    source = app.new_list_object('Als Nächstes')
    aktuell = app.new_item('Konzept schreiben', planned_date=today)
    wichtig = app.new_item('Angebot prüfen', planned_date=today, importance=3)
    normal = app.new_item('Antwort formulieren', planned_date=today)
    source['items'] = [aktuell, wichtig, normal]
    app.lists, app.folders, app.labels, app.trash = [source], [], [], []
    app.items, app.active_list_id = source['items'], source['id']
    app.settings['release_notes_seen'] = mod.APP_VERSION
    app.clear_render_cache(); assert app.save_items(); app.set_home_view(); idle(lauf)
    assert app.start_focus(aktuell['id']); idle(lauf)
    app.sync_focus_panel(); idle(lauf)
    text = lambda: app.focus_next_label.cget('text')
    assert text() == 'Als Nächstes: Angebot prüfen · danach noch 1 Aufgabe', text()
    assert app.focus_next_label.winfo_viewable()
    # Sekundentakt ohne Bestandsänderung bestimmt nichts neu.
    with patch.object(app, 'focus_candidates', wraps=app.focus_candidates) as bestimmen:
        app.sync_focus_panel(); app.update_timer_indicator(); app.sync_focus_panel()
    assert bestimmen.call_count == 0, bestimmen.call_count
    # Bestandsänderung: die wichtigere Aufgabe ist erledigt.
    assert app.toggle_item_done_anywhere(wichtig['id']); idle(lauf); app.sync_focus_panel(); idle(lauf)
    assert text() == 'Als Nächstes: Antwort formulieren', text()
    # „Nächste Aufgabe“ nimmt genau die angezeigte; danach steht die übrige da.
    klick(next(w for w in knoepfe(app.focus_panel, mod.RoundedButton)
               if w.text in ('Nächste Aufgabe', mod.RoundedButton.action_text('Nächste Aufgabe'))), lauf)
    idle(lauf)
    assert app.running_timer()['item_id'] == normal['id'], app.running_timer()
    app.sync_focus_panel(); idle(lauf)
    assert text() == 'Als Nächstes: Konzept schreiben', text()
    assert app.toggle_item_done_anywhere(aktuell['id']); idle(lauf); app.sync_focus_panel(); idle(lauf)
    assert text() == 'Danach keine weitere Aufgabe für heute', text()
    app.undo_last_change(); idle(lauf); app.sync_focus_panel(); idle(lauf)
    assert text() == 'Als Nächstes: Konzept schreiben', text()
    anzahl, befunde = befunde_b15(lauf, 'Fokusfeld Als Nächstes')
    assert anzahl and not befunde, befunde[:4]
    app.stop_time_tracking()
    return ('Fokusfeld „Als Nächstes: …“: Aufgabe von „Nächste Aufgabe“ mit Zahl der übrigen, folgt Erledigen/Wechsel/Undo, '
            'keine Neubestimmung im Sekundentakt, leerer Zustand, Knopfprüfung')


def fall_fokus_menue(lauf):
    """Fokusfeld-Befehle über Menü „Ansichten“ und Aktionsauswahl: Hinweis ohne Sitzung, Pause, +5, Wechseln, Beenden."""
    from datetime import date, datetime, timedelta
    app, mod = lauf.app, lauf.mod
    today = date.today().isoformat()
    source = app.new_list_object('Fokusmenü')
    aktuell = app.new_item('Konzept schreiben', planned_date=today)
    weitere = app.new_item('Antwort formulieren', planned_date=today)
    source['items'] = [aktuell, weitere]
    app.lists, app.folders, app.labels, app.trash = [source], [], [], []
    app.items, app.active_list_id = source['items'], source['id']
    app.settings['release_notes_seen'] = mod.APP_VERSION
    app.clear_render_cache(); assert app.save_items(); app.set_home_view(); idle(lauf)
    namen = {'focus_pause': 'Fokus pausieren oder fortsetzen', 'focus_extend': 'Fokus um 5 Minuten verlängern',
             'focus_switch': 'Fokus wechseln zu …', 'focus_finish': 'Fokus beenden und Zeit buchen'}
    eintraege = {e['id']: e for e in app.app_action_entries()}
    for kennung, label in namen.items():
        e = eintraege[kennung]
        assert e['label'] == label and e['group'] == 'Planen und einordnen' and 'Ansichten' in e['path'], e
    gefunden = {r['title'] for r in app.quick_open_results('> Fokus')}
    assert set(namen.values()) <= gefunden, gefunden

    def ausfuehren(kennung):
        assert app.invoke_app_action(eintraege[kennung]) is not False
        idle(lauf)
    # Ohne Sitzung: Hinweis statt stiller Wirkungslosigkeit, nichts gestartet.
    for kennung in namen:
        with patch.object(app, 'show_info') as hinweis:
            ausfuehren(kennung)
        assert hinweis.called and 'keine Fokussitzung' in hinweis.call_args.args[1], (kennung, hinweis.call_args)
        assert app.running_timer() is None
    assert app.start_focus(aktuell['id'], now=datetime.now().astimezone() - timedelta(minutes=3)); idle(lauf)
    ausfuehren('focus_pause')
    assert app.running_timer()['started_at'] is None
    ausfuehren('focus_pause')
    assert app.running_timer()['started_at'] is not None
    ziel = app.running_timer()['goal_seconds']
    ausfuehren('focus_extend')
    assert app.running_timer()['goal_seconds'] > ziel, app.running_timer()
    menues = []

    def lesen(menu, x, y):
        menues.append([menu.entrycget(i, 'label').strip() for i in range(menu.index('end') + 1)])
        menu.unpost()
    with patch.object(mod.tk.Menu, 'tk_popup', new=lesen):
        ausfuehren('focus_switch')
    assert menues and menues[-1] == ['Zeit buchen und wechseln zu', 'Antwort formulieren'], menues
    ausfuehren('focus_finish')
    assert app.running_timer() is None
    assert (app.find_item_in_lists(aktuell['id'])[0].get('time_spent_minutes') or 0) >= 3
    return ('Menü „Ansichten“/Aktionsauswahl: vier Fokusbefehle mit Gruppe „Planen und einordnen“, Hinweis ohne Sitzung, '
            'Pause/Fortsetzen, +5 Minuten, Wechseln zu …, Beenden und Buchen')


def fall_home_fokus_laeuft(lauf):
    """Startseitenkachel „Nächste Aufgabe“: laufende Fokussitzung benannt, „Fokus anzeigen“ ohne Neustart."""
    from datetime import date, datetime, timedelta
    app, mod = lauf.app, lauf.mod
    today = date.today().isoformat()
    source = app.new_list_object('Kachelfokus')
    task = app.new_item('Konzept schreiben', planned_date=today, importance=3)
    source['items'] = [task, app.new_item('Antwort formulieren', planned_date=today)]
    app.lists, app.folders, app.labels, app.trash = [source], [], [], []
    app.items, app.active_list_id = source['items'], source['id']
    app.settings['release_notes_seen'] = mod.APP_VERSION
    # Eigene Auswahl mit der Kachel „Nächste Aufgabe“ (die Standardauswahl zeigt sie nicht).
    app.settings['home_tile_order'] = ['focus', 'today']
    app.settings['home_tiles_hidden'] = [key for key in app.HOME_TILE_KEYS if key not in ('today', 'focus')]
    app.clear_render_cache(); assert app.save_items(); app.set_home_view(); idle(lauf)

    def knoepfe_texte():
        return [w.text for w in knoepfe(app.home_content, mod.RoundedButton)]

    def texte():
        return [w.cget('text') for w in knoepfe(app.home_content, mod.tk.Label)]
    assert 'Fokus starten' in knoepfe_texte() and 'Läuft gerade im Fokus.' not in texte(), knoepfe_texte()
    start = datetime.now().astimezone() - timedelta(minutes=2)
    assert app.start_focus(task['id'], now=start); idle(lauf)
    app.set_home_view(); idle(lauf)
    assert 'Fokus anzeigen' in knoepfe_texte() and 'Fokus starten' not in knoepfe_texte(), knoepfe_texte()
    assert 'Läuft gerade im Fokus.' in texte()
    vorher = app.running_timer()
    klick(next(w for w in knoepfe(app.home_content, mod.RoundedButton) if w.text == 'Fokus anzeigen'), lauf)
    idle(lauf)
    assert app.view_mode == app.PLAN_DAY_VIEW and app.running_timer() == vorher
    app.stop_time_tracking(); app.set_home_view(); idle(lauf)
    assert 'Fokus starten' in knoepfe_texte() and 'Läuft gerade im Fokus.' not in texte()
    return 'Kachel „Nächste Aufgabe“: laufender Fokus benannt, „Fokus anzeigen“ öffnet Heute ohne Neustart, danach wieder „Fokus starten“'


def fall_side_abschnitte(lauf):
    """Alt+Pfeil springt in der Nebenansicht zum nächsten/vorherigen Abschnitt, Ränder melden, lesend (01.11.2026)."""
    app, mod = lauf.app, lauf.mod
    main, editor = seite_anlegen(lauf, '# Hauptarbeit\n\nOffener Entwurf\n')
    fuell = lambda name: '\n\n'.join(f'{name} {number}' for number in range(40))
    other = app.new_page_from_markdown('# Überblick\n\n## Einleitung\n\n' + fuell('Absatz') + '\n\n## Mitte\n\n'
                                       + fuell('Zeile') + '\n\n## Abschluss\n\nEnde.\n')
    gruppen = [app.new_item('Vorab'),
               app.new_item('Planung', kind=app.ITEM_KIND_GROUP, children=[app.new_item('Entwurf')]),
               app.new_item('Zwischen'),
               app.new_item('Bau', kind=app.ITEM_KIND_GROUP, children=[app.new_item('Rohbau')])]
    liste = app.new_list_object('Projektphasen', gruppen)
    flach = app.new_list_object('Ohne Gliederung', [app.new_item('Einzeln')])
    app.lists.extend([liste, flach])
    assert app.save_items()
    app.set_active_list(main['id']); idle(lauf)
    editor = app.rich_note_editor
    draft = editor.text.get('1.0', 'end-1c')
    model = copy.deepcopy(app.lists)
    written = Path(mod.SAVE_FILE).read_bytes()
    depth = len(app.undo_stack)

    def status():
        return app._side_view_status.cget('text')

    # Seite: Abschnitte über die Einfügemarke, sichtbar angesteuert.
    assert app.open_side_view(other['id']); idle(lauf)
    abschnitte = {section['title']: section['key'] for section in mod.glide_side_view.sections(other)}
    assert list(abschnitte)[-3:] == ['Einleitung', 'Mitte', 'Abschluss'], abschnitte
    body = app._side_view_body
    # Ohne sichtbare Einfügemarke zählt die oberste sichtbare Zeile.
    assert isinstance(body, mod.tk.Text) and body.index('@0,0') == '1.0'
    vorwaerts = [titel for titel, zeile in abschnitte.items() if zeile > 1]
    for titel in vorwaerts:
        taste(body, '<Alt-Down>', lauf)
        assert status() == f'Abschnitt: {titel}', status()
        assert body.index('insert') == f'{abschnitte[titel]}.0' and body.bbox('insert'), (titel, body.index('insert'))
    taste(body, '<Alt-Down>', lauf)
    assert status() == 'Kein weiterer Abschnitt.' and body.index('insert') == f"{abschnitte['Abschluss']}.0"
    # „Abschnitte …“ markiert dieselbe Lesestelle mit ✓, nur einmal.
    menues = []

    def lesen(menu, x, y):
        menues.append([menu.entrycget(i, 'label') for i in range(menu.index('end') + 1)])
        menu.unpost()
    with patch.object(mod.tk.Menu, 'tk_popup', new=lesen):
        klick(next(w for w in knoepfe(app.side_pane, mod.RoundedButton)
                   if w.text == mod.RoundedButton.action_text('Abschnitte …')), lauf)
    markiert = [label for label in menues[-1] if label.startswith('✓ ')]
    assert len(markiert) == 1 and markiert[0].strip().endswith('Abschluss'), menues[-1]
    for titel in reversed(list(abschnitte)[:-1]):
        taste(body, '<Alt-Up>', lauf)
        assert status() == f'Abschnitt: {titel}', status()
        assert body.index('insert') == f'{abschnitte[titel]}.0' and body.bbox('insert')
    taste(body, '<Alt-Up>', lauf)
    assert status() == 'Kein vorheriger Abschnitt.'
    # Liste: Gruppen in Anzeigereihenfolge; ohne Fokus führt „weiter“ zur ersten Gruppe.
    assert app.open_side_view(liste['id']); idle(lauf)
    baum = seitenbaum(app)
    assert not baum.focus()
    erwartet = [gruppen[1]['id'], gruppen[3]['id']]
    for ziel in erwartet:
        taste(baum, '<Alt-Down>', lauf)
        baum = seitenbaum(app)
        assert baum.focus() == ziel and baum.selection() == (ziel,), (baum.focus(), ziel)
    taste(baum, '<Alt-Down>', lauf)
    assert status() == 'Kein weiterer Abschnitt.' and seitenbaum(app).focus() == erwartet[-1]
    with patch.object(mod.tk.Menu, 'tk_popup', new=lesen):
        klick(next(w for w in knoepfe(app.side_pane, mod.RoundedButton)
                   if w.text == mod.RoundedButton.action_text('Abschnitte …')), lauf)
    assert [label for label in menues[-1] if label.startswith('✓ ')] == ['✓ Bau'], menues[-1]
    taste(seitenbaum(app), '<Alt-Up>', lauf)
    assert seitenbaum(app).focus() == erwartet[0] and status() == 'Abschnitt: Planung'
    taste(seitenbaum(app), '<Alt-Up>', lauf)
    assert status() == 'Kein vorheriger Abschnitt.' and seitenbaum(app).focus() == erwartet[0]
    # Ohne Überschriften/Gruppen: Hinweis statt Sprung.
    assert app.open_side_view(flach['id']); idle(lauf)
    taste(seitenbaum(app), '<Alt-Down>', lauf)
    assert status() == 'Diese Ansicht hat keine Abschnitte.'
    # Lesend: Hauptarbeit, Modell, Datei und Undo unverändert.
    assert app.active_list_id == main['id'] and app.rich_note_editor is editor
    assert editor.text.get('1.0', 'end-1c') == draft
    assert app.lists == model and Path(mod.SAVE_FILE).read_bytes() == written and len(app.undo_stack) == depth
    app.close_side_view()
    # Hilfe › Tastenkürzel nennt die Kürzel der Nebenansicht (Gesamtprüfung 01.11.2026).
    texte = []
    def sammeln(dialog, parent=None):
        stapel = [dialog]
        while stapel:
            widget = stapel.pop()
            stapel.extend(widget.winfo_children())
            if 'text' in widget.keys():
                texte.append(str(widget.cget('text')))
        dialog.destroy()
    with patch.object(app, 'run_modal', sammeln):
        app.show_shortcuts_dialog()
    for kuerzel in ('Nebenansicht: Alt + ↑ / ↓', 'Nebenansicht: Alt + ← / →', 'Nächster / vorheriger Abschnitt'):
        assert kuerzel in texte, (kuerzel, [x for x in texte if 'Nebenansicht' in x])
    return ('Nebenansicht Alt+Pfeil runter/hoch: Seite über Einfügemarke und Liste über Gruppen in Anzeigereihenfolge, '
            'sichtbar angesteuert, ✓ am aktuellen Abschnitt, Ränder und fehlende Abschnitte gemeldet, lesend, in Hilfe › Tastenkürzel')


def fall_eckenlabels(lauf):
    """Labels oben rechts in der Kartenecke: Liste, Ordner, Tabelle, Pinnwand und Seite ohne Überdeckung."""
    app = lauf.app
    rechteck = lambda w: (w.winfo_rootx(), w.winfo_rooty(),
                          w.winfo_rootx() + w.winfo_width(), w.winfo_rooty() + w.winfo_height())
    schneidet = lambda a, b: not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])
    text, kunde = app.new_label_object("Text", color="export"), app.new_label_object("Kunde", color="clear")
    app.labels.extend([text, kunde])
    punkt = app.new_item("Unterlagen prüfen")
    punkt["due"], punkt["labels"] = "2026-11-05", [kunde["id"]]
    ordner = app.new_folder_object("Kundenordner")
    app.folders.append(ordner)
    liste = app.new_list_object("Projekt", [punkt, app.new_item("Angebot")], folder_id=ordner["id"])
    ohne = app.new_list_object("Ohne Labels", [app.new_item("Eins")])
    app.lists.extend([liste, ohne])
    app.save_items()
    seite, _editor = seite_anlegen(lauf, SEITE_MD.replace(
        "# Wochenplanung Parkquartier", "# Wochenplanung Parkquartier mit einem langen Titel bis in die Ecke", 1))
    # Echter Zuweisungsweg wie im Kontextmenü der Seitenleiste.
    for art, ziel, label in (("list", liste, text), ("list", liste, kunde), ("folder", ordner, text),
                             ("list", seite, text), ("list", seite, kunde)):
        app.toggle_page_label(art, ziel["id"], label["id"])
    assert liste["labels"] == [text["id"], kunde["id"]] and ordner["labels"] == [text["id"]]
    karte = app.list_frame_outer.inner
    for breite in (1280, 860):
        lauf.root.geometry(f"{breite}x800+20+20")
        idle(lauf)
        app.set_active_list(ohne["id"])
        idle(lauf)
        kopf = app.subtitle_row.winfo_height()
        assert app.page_labels_frame.winfo_manager() == "" and app.page_labels_spacer.winfo_manager() == ""
        for name, oeffnen in (("liste", lambda: (app.set_active_list(liste["id"]), app.open_list_view())),
                              ("tabelle", app.set_table_view), ("pinnwand", app.open_board_view),
                              ("ordner", lambda: (app.open_list_view(), app.set_active_folder(ordner["id"])))):
            oeffnen()
            idle(lauf)
            chips = rechteck(app.page_labels_frame)
            assert app.page_labels_frame.winfo_manager() == "place", (breite, name)
            assert [c.chip_text for c in app.page_label_widgets] == (["Text"] if name == "ordner" else ["Text", "Kunde"])
            # Rechts oben in der Karte, mit festem Abstand zur Innenkante.
            assert chips[2] == karte.winfo_rootx() + karte.winfo_width() - app.CONTENT_LABEL_INSET_X, (name, chips)
            assert chips[1] == karte.winfo_rooty() + app.CONTENT_LABEL_INSET_Y, (name, chips)
            assert karte.pack_slaves()[0] is app.page_labels_spacer, name
            if app.tree.winfo_ismapped() and app.tree.get_children():
                zeile = app.tree.bbox(app.tree.get_children()[0])
                if zeile:
                    links, oben = app.tree.winfo_rootx(), app.tree.winfo_rooty()
                    zeile = (links + zeile[0], oben + zeile[1], links + zeile[0] + zeile[2], oben + zeile[1] + zeile[3])
                    assert not schneidet(chips, zeile), (breite, name, chips, zeile)
            leiste = getattr(app.workspace, "bar", None)
            if leiste is not None and leiste.winfo_ismapped():
                assert not schneidet(chips, rechteck(leiste)), (breite, name)
            # Der Kopf trägt keine Labels mehr und behält seine Höhe.
            assert app.subtitle_row.winfo_height() == kopf, (breite, name, kopf,
                                                           app.subtitle_row.winfo_height())
        app.open_list_view()
        for voll in (False, True):
            app.settings["page_full_width"] = voll
            app.set_active_list(liste["id"])
            app.set_active_list(seite["id"])
            idle(lauf)
            editor = app.rich_note_editor
            chips = rechteck(app.page_labels_frame)
            # Seit D71 (07.11.2026) ohne Titel im Inhalt: Freiraum in Chiphöhe wie bei Listen.
            assert app.page_labels_spacer.winfo_manager() == "pack", (breite, voll)
            assert app.page_labels_frame.winfo_manager() == "place"
            assert rechteck(editor.text)[1] >= chips[3] - 1, (breite, voll, chips, rechteck(editor.text))
    app.settings["page_full_width"] = False
    # Labels lösen: Ecke und Titelreserve verschwinden sofort.
    app.clear_page_labels("list", seite["id"])
    idle(lauf)
    assert app.page_labels_frame.winfo_manager() == "" and app.rich_note_editor._corner_reserve == 0
    return "Liste, Tabelle, Pinnwand, Ordner und Seite bei 1280/860 px: Chips in der Kartenecke, ohne Überdeckung"


def fall_hinweisplatz(lauf):
    """Weicht das Logo (schmale Breite) oder ist der Kompaktmodus an, weichen alle Bedienhinweise."""
    app = lauf.app
    app.settings["show_hints"] = True
    punkte = [app.new_item("Unterlagen prüfen"), app.new_item("Angebot")]
    liste = app.new_list_object("Projekt", punkte)
    app.lists.append(liste)
    app.save_items()
    seite, _editor = seite_anlegen(lauf)

    def oeffnen(name):
        app.open_list_view()
        if name == "seite":
            app.set_active_list(seite["id"])
        else:
            app.set_active_list(liste["id"])
            app.open_list_view()
            if name == "tabelle":
                app.set_table_view()
            elif name == "pinnwand":
                app.open_board_view()
        idle(lauf)

    def hinweise(name):
        """Sichtbare Hinweistexte der Ansicht `name` (leer, wenn alle weichen)."""
        texte = []
        if name == "liste":
            if app.card_foot_mode() == "hint" and app.card_foot.winfo_manager():
                texte.append(app.hint_label.cget("text"))
        elif name == "seite":
            texte.append(app.tool_band_hint.cget("text"))
        else:
            notiz = app.header_note_text()
            if notiz:
                texte.append(notiz)
            hinweis = getattr(app.workspace, "notice", None)
            if hinweis is not None and hinweis.winfo_exists() and hinweis.winfo_manager():
                texte.append(hinweis.cget("text"))
        return [t for t in texte if t]

    ansichten = ("liste", "tabelle", "pinnwand", "seite")
    lauf.root.geometry("1280x800+20+20")
    idle(lauf, 6)
    assert app.header_logo.winfo_manager(), "Logo bei voller Breite sichtbar"
    for name in ansichten:
        oeffnen(name)
        assert hinweise(name), (name, "Hinweise bei voller Breite und eingeschaltetem Schalter")
    # Schmal: Das Logo weicht, mit ihm jeder Hinweis – in jeder Ansicht.
    lauf.root.geometry("860x700+20+20")
    idle(lauf, 6)
    assert app.header_density() == "minimal" and not app.header_logo.winfo_manager()
    for name in ansichten:
        oeffnen(name)
        assert not hinweise(name), (name, hinweise(name))
    # Die Liste nutzt den frei gewordenen Kartenfuß.
    oeffnen("liste")
    assert app.card_foot.winfo_manager() == ""
    # Die Auswahlzahl der Pinnwand ist ein Zustand und bleibt auch schmal sichtbar.
    oeffnen("pinnwand")
    app.workspace.pin([p["id"] for p in punkte])
    idle(lauf)
    werk = app.workspace
    werk.selected_ids = [p["id"] for p in punkte]
    werk.selected_id = punkte[-1]["id"]
    assert len(werk.selection()) == 2, (werk.selection(), list(werk.card_boxes))
    werk.update_selection_notice()
    assert werk.notice.winfo_manager() and werk.notice.cget("text") == "2 Karten ausgewählt", werk.notice.cget("text")
    werk.selected_ids, werk.selected_id = [], None
    werk.update_selection_notice()
    assert not werk.notice.winfo_manager(), "ohne Auswahl und ohne Hinweis keine leere Zeile"
    # Breit wieder: Hinweise kehren zurück, der Schalter blieb unverändert.
    lauf.root.geometry("1280x800+20+20")
    idle(lauf, 6)
    for name in ansichten:
        oeffnen(name)
        assert hinweise(name), (name, "nach Rückkehr zur vollen Breite")
    assert app.settings["show_hints"] is True
    # Kompaktmodus: keine Hinweise, danach wieder da.
    oeffnen("liste")
    app.enter_compact_mode()
    idle(lauf, 6)
    for name in ("liste", "seite"):
        oeffnen(name)
        assert not hinweise(name), ("kompakt", name, hinweise(name))
    app.leave_compact_mode()
    lauf.root.geometry("1280x800+20+20")
    idle(lauf, 6)
    for name in ("liste", "seite"):
        oeffnen(name)
        assert hinweise(name), ("nach Kompaktmodus", name)
    return "Liste, Tabelle, Pinnwand, Seite: Hinweise bei 1280 px, keine bei 860 px und im Kompaktmodus; Schalter unverändert"


def fall_werkzeugzeile(lauf):
    """Abstand Werkzeugzeile ↔ Karte, Pinnwand auf Kartenfarbe, Ansichtssymbole ganz rechts."""
    app = lauf.app
    punkte = [app.new_item("Unterlagen prüfen"), app.new_item("Angebot")]
    liste = app.new_list_object("Projekt", punkte)
    app.lists.append(liste)
    app.save_items()
    seite, _editor = seite_anlegen(lauf)
    karte = app.list_frame_outer
    befunde = []
    for design in ("light", "dark"):
        app.set_design(design)
        for breite in (1280, 860):
            lauf.root.geometry(f"{breite}x800+20+20")
            idle(lauf, 6)
            for name, oeffnen in (("liste", lambda: (app.set_active_list(liste["id"]), app.open_list_view())),
                                  ("tabelle", app.set_table_view), ("pinnwand", app.open_board_view)):
                oeffnen()
                idle(lauf)
                feld = app.search_border
                abstand = karte.winfo_rooty() - (feld.winfo_rooty() + feld.winfo_height())
                assert abstand >= app.CONTENT_TOOLBAR_GAP, (design, breite, name, abstand)
                umschalter = app.view_switch
                assert umschalter.winfo_ismapped(), (name, "Umschalter fehlt")
                rechts = umschalter.winfo_rootx() + umschalter.winfo_width()
                zeile = app.search_frame.winfo_rootx() + app.search_frame.winfo_width()
                assert rechts == zeile, (design, breite, name, "Umschalter nicht ganz rechts", rechts, zeile)
                andere = [w for w in app.search_frame.pack_slaves()
                          if w is not umschalter and w.winfo_ismapped() and w.winfo_rootx() >= umschalter.winfo_rootx()]
                assert not andere, (design, breite, name, [str(w) for w in andere])
                if name == "pinnwand":
                    flaeche = app.workspace.canvas
                    assert flaeche.cget("bg") == app.theme["card"], (design, flaeche.cget("bg"), app.theme["card"])
                    assert flaeche.cget("highlightbackground") == app.theme["card"]
                befunde.append(f"{design}/{breite}/{name}:{abstand}")
            app.open_list_view()
            app.set_active_list(seite["id"])
            idle(lauf)
            band = app.tool_band
            if band.winfo_ismapped():
                abstand = karte.winfo_rooty() - (band.winfo_rooty() + band.winfo_height())
                assert abstand >= app.CONTENT_TOOLBAR_GAP, (design, breite, "seite", abstand)
    # Spaltenknopf der Tabelle steht links vom Umschalter.
    lauf.root.geometry("1280x800+20+20")
    app.set_active_list(liste["id"])
    app.set_table_view()
    idle(lauf, 6)
    spalten = app.table_columns_button
    if spalten.winfo_ismapped():
        assert spalten.winfo_rootx() + spalten.winfo_width() <= app.view_switch.winfo_rootx()
    # Seitenfuß: „Erwähnt ohne Verweis …“ und Statusmeldung in einer Zeile (02.11.2026).
    app.open_list_view()
    app.set_active_list(seite["id"])
    idle(lauf)
    editor = app.rich_note_editor
    editor.status.configure(text="Schreibgeschützter Bestand")
    idle(lauf)
    knopf, status = editor._mentions_button, editor.status
    assert knopf.master is status.master is editor._foot_row
    mitte = lambda w: w.winfo_rooty() + w.winfo_height() / 2
    assert abs(mitte(knopf) - mitte(status)) <= 2, (mitte(knopf), mitte(status))
    assert status.winfo_rootx() >= knopf.winfo_rootx() + knopf.winfo_width()
    # Aufgeklappte Fundstellen liegen über der Fußzeile.
    editor._mentions_button.command()
    idle(lauf)
    assert editor._mentions_rows.winfo_rooty() + editor._mentions_rows.winfo_height() <= editor._foot_row.winfo_rooty()
    editor._mentions_button.command()
    return f"{len(befunde)} Messungen: Abstand ≥ {app.CONTENT_TOOLBAR_GAP} px, Umschalter rechts, Pinnwand auf Kartenfarbe; Seitenfuß einzeilig"


def fall_beta350(lauf):
    """3.50: gespeicherte Hintergrundfarbe, Fluchten und echter Griff-Ziehweg."""
    app, mod = lauf.app, lauf.mod
    for design in app.DESIGN_ORDER:
        app.set_design(design)
        for _label, key in mod.glide_appearance.BACKGROUND_CHOICES:
            app.settings['background_color'] = key
            palette = app.active_theme()
            for role in app.TEXT_ROLE_KEYS:
                for surface in ('bg', 'card', 'input'):
                    assert mod.contrast_ratio(palette[role], palette[surface]) >= 4.49, (design, key, role, surface)
        app.settings['background_color'] = 'surface'
        app.set_design(design)
        idle(lauf)
        assert app.theme['bg'] == app.theme['card'], (design, app.theme)
        assert not app.glass_enabled() and not app.theme['glass_gradient']
        assert not app.backdrop_request()
        assert all(not box.glass_mode for box in app.rounded_containers if box.winfo_exists())
    app.set_design('minimal_light')
    app.settings['background_color'] = 'clear'
    blue = app.active_theme()['bg']
    assert int(blue[5:7], 16) > int(blue[1:3], 16), blue
    app.set_design('light')
    app.set_background_color('clear')
    idle(lauf)
    assert app.theme['bg'] != app.theme['card']
    assert app.theme['card'] == app.THEMES['light']['card']
    assert app.normalize_personal_settings({'background_color': 'falsch'})['background_color'] == 'default'
    lauf.neustart()
    app = lauf.app
    assert app.settings['background_color'] == 'clear'
    for geometry in ('860x700+20+20', '1280x800+20+20', '1700x1000+20+20'):
        lauf.root.geometry(geometry)
        idle(lauf, 8)
        assert app.sidebar_shell.winfo_rooty() == app.header_frame.winfo_rooty()
        assert app.sidebar_shell.winfo_rootx() < app.header_frame.winfo_rootx()
        assert abs(app.header_frame.winfo_rootx() - app.content_frame.winfo_rootx()) <= 1
        assert abs(app.sidebar_shell.winfo_rooty() + app.sidebar_shell.winfo_height()
                   - app.content_frame.winfo_rooty() - app.content_frame.winfo_height()) <= 2
        count, issues = befunde_b15(lauf, 'beta350-' + geometry)
        assert count and not issues, issues
    app.set_backdrop_choice(mod.glide_backdrop.NONE_KEY)
    idle(lauf)
    assert app.settings['background_color'] == 'default'
    assert app.theme['bg'] == app.THEMES['light']['bg']
    page, editor = seite_anlegen(lauf, '# Erste\n\nAbsatz 😀\n\n## Zweite\n\nEnde')
    prior = editor.document()
    text = editor.text
    source = zeile_mit(text, 'Absatz 😀')
    destination = zeile_mit(text, 'Ende')
    editor.show_block_handle(f'{source}.0', 'pointer')
    idle(lauf)
    handle = editor._block_handle
    box = text.dlineinfo(f'{destination}.0')
    px = text.winfo_rootx() + int(float(text.cget('padx'))) + 30
    py = text.winfo_rooty() + box[1] + box[3] - 1
    handle.event_generate('<ButtonPress-1>', x=3, y=3)
    handle.event_generate('<B1-Motion>', x=px-handle.winfo_rootx(), y=py-handle.winfo_rooty(), rootx=px, rooty=py)
    idle(lauf)
    assert editor._block_drop_marker.winfo_ismapped()
    marker = editor._block_drop_marker
    target_line = editor._block_drag['target'] + 1
    target_box = text.dlineinfo(f'{target_line}.0')
    assert abs(marker.winfo_rootx() - (text.winfo_rootx() + box[0])) <= 1, 'Einfügemarke muss an der Textkante stehen'
    target_y = target_box[1] if target_box else box[1] + box[3]
    assert abs(marker.winfo_rooty() - (text.winfo_rooty() + target_y)) <= 1, 'Einfügemarke muss an der Zielzeile stehen'
    handle.event_generate('<ButtonRelease-1>', x=px-handle.winfo_rootx(), y=py-handle.winfo_rooty(), rootx=px, rooty=py)
    idle(lauf)
    assert not app.action_chooser_open()
    assert editor.document()['text'].index('Absatz 😀') > editor.document()['text'].index('Ende')
    assert editor.document() == app.page_entry(page['id'])['rich_note']
    editor.undo()
    idle(lauf)
    assert editor.document() == prior
    editor.redo()
    idle(lauf)
    assert editor.document()['text'].index('Absatz 😀') > editor.document()['text'].index('Ende')
    # Abbruch und Schreibschutz dürfen weder Text noch gespeicherte Bytes ändern.
    app.sidebar_listbox.focus_force()
    idle(lauf)
    # Fokusverlust darf speichern und die Darstellung erneuern. Der folgende
    # echte Griffzug gehört zur weiterhin geöffneten Seite und ihrem aktuellen
    # Editor, nicht zu einer zuvor festgehaltenen Widgetinstanz.
    assert app.current_list()["id"] == page["id"]
    editor = app.rich_note_editor
    assert editor is not None and editor.entry_id == page["id"]
    editor.show_block_handle('1.0', 'pointer')
    idle(lauf)
    handle = editor._block_handle
    before = editor.document()
    saved = Path(mod.SAVE_FILE).read_bytes()
    handle.event_generate('<ButtonPress-1>', x=3, y=3)
    handle.event_generate('<B1-Motion>', x=px-handle.winfo_rootx(), y=py-handle.winfo_rooty(), rootx=px, rooty=py)
    assert lauf.root.focus_get() is editor.text, 'Ein Griffzug übernimmt den Textfokus für Escape'
    editor.text.event_generate('<Escape>')
    idle(lauf)
    assert editor._block_drag is None
    handle.event_generate('<ButtonRelease-1>', x=3, y=3)
    assert editor.document() == before and Path(mod.SAVE_FILE).read_bytes() == saved
    app._data_read_only = True
    handle.event_generate('<ButtonPress-1>', x=3, y=3)
    assert editor._block_drag is None
    app._data_read_only = False
    # Echte Aufgaben und Bilder behalten beim Ziehen ihre Identität/Anhänge.
    page, editor = seite_anlegen(lauf, '# Medien\n\n- [ ] Aufgabe behalten\n\nSchluss')
    picture = mod.tk.PhotoImage(master=lauf.root, width=12, height=12)
    picture.put('#2277AA', to=(0, 0, 12, 12))
    image_path = Path(lauf.data) / 'blockbild.png'
    picture.write(str(image_path), format='png')
    editor.text.mark_set('insert', 'end-1c')
    editor.insert_images([str(image_path)])
    assert editor.flush()
    idle(lauf, 8)
    identities = set(editor.item_ids(owned=True))
    assert identities
    before = editor.document()
    assert before.get('images')
    image_line = next(int(editor.text.index(str(editor.text.tag_ranges(tag)[0])).split('.')[0])
                      for tag in editor.images if editor.text.tag_ranges(tag))
    def drag_to_top(row):
        editor.text.see(f'{row}.0')
        editor.text.mark_set('insert', f'{row}.0')
        editor.text.focus_force()
        idle(lauf)
        editor.show_block_handle(f'{row}.0', 'focus')
        idle(lauf)
        assert editor._block_handle_line == row, (editor._block_handle_line, row)
        grip = editor._block_handle
        grip.event_generate('<ButtonPress-1>', x=3, y=3)
        editor.text.yview_moveto(0)
        idle(lauf)
        box = editor.text.dlineinfo('1.0')
        x = editor.text.winfo_rootx() + int(float(editor.text.cget('padx'))) + 30
        y = editor.text.winfo_rooty() + box[1] + 1
        if editor.text.get('1.0', '1.1') == editor.IMAGE_ANCHOR:
            first_image = next(view for key, view in editor._image_views.items()
                               if str(editor.text.tag_ranges(key)[0]).startswith('1.'))
            x = first_image.winfo_rootx() + first_image.winfo_width() // 2
            y = first_image.winfo_rooty() + 1
        grip.event_generate('<B1-Motion>', x=x-grip.winfo_rootx(), y=y-grip.winfo_rooty(), rootx=x, rooty=y)
        assert editor._block_drag and editor._block_drag['active'], editor._block_drag
        assert editor._block_drag['target'] == 0, editor._block_drag
        grip.event_generate('<ButtonRelease-1>', x=x-grip.winfo_rootx(), y=y-grip.winfo_rooty(), rootx=x, rooty=y)
        idle(lauf, 6)
    drag_to_top(image_line)
    assert editor.document()['images'] == before['images']
    assert set(editor.item_ids(owned=True)) == identities
    task_line = zeile_mit(editor.text, 'Aufgabe behalten')
    drag_to_top(task_line)
    assert set(editor.item_ids(owned=True)) == identities
    assert editor.document()['text'].lstrip().startswith('Aufgabe behalten'), repr(editor.document())
    assert editor.document() == app.page_entry(page['id'])['rich_note']
    page, editor = seite_anlegen(lauf, '# Struktur\n\nStart\n\n- Eltern\n  - Kind\n\nSchluss')
    parent_line = zeile_mit(editor.text, app.ICONS['bullet'] + ' Eltern')
    drag_to_top(parent_line)
    assert editor.document()['text'].startswith(app.ICONS['bullet'] + ' Eltern\n' + app.ICONS['bullet'] + ' Kind')
    assert any(span['tag'] == 'indent1' for span in editor.document()['spans'])
    assert editor.document() == app.page_entry(page['id'])['rich_note']
    before = editor.document()
    saved = Path(mod.SAVE_FILE).read_bytes()
    undo_depth = len(editor._undo)
    normalize = editor.normalize
    def limited(value):
        if value.get('text') != before['text']:
            raise ValueError('Zu viele Formatierungen.')
        return normalize(value)
    with patch.object(editor, 'normalize', side_effect=limited):
        drag_to_top(zeile_mit(editor.text, 'Start'))
    assert editor.document() == before and Path(mod.SAVE_FILE).read_bytes() == saved
    assert len(editor._undo) == undo_depth and 'Zu viele Formatierungen' in editor.status.cget('text')
    return 'Hintergrundfarben in zehn Designs, Speicherung/Neustart, drei Größen, volle Seitenleiste, Blockziehen/Undo/Redo/Abbruch/Schreibschutz'


def fall_ansichtssymbole(lauf):
    app = lauf.app
    task = app.new_item('Symbole und Tastatur prüfen')
    listing = app.new_list_object('Ansichtssymbole', [task])
    app.lists.append(listing)
    app.save_items()
    app.set_active_list(listing['id'])
    idle(lauf)
    checked = 0
    for size in ('mittel', 'gross'):
        app.settings['ui_font_size'] = size
        app.apply_ui_font()
        app.apply_theme()
        for geometry in ('860x700+20+20', '1280x800+20+20'):
            lauf.root.geometry(geometry)
            idle(lauf)
            for mode, name, caption in (('table', 'table_button', 'Tabelle'),
                                        ('board', 'board_button', 'Pinnwand'),
                                        ('list', 'list_view_button', 'Liste')):
                button = getattr(app, name)
                assert button.text == app.ICONS[mode] and button._accessible_name == caption
                taste(button, '<Return>', lauf)
                assert app._view_switch_active == mode and button.active_fill == app.theme['active']
                assert button.winfo_ismapped() and button.winfo_width() >= 38
                for part in button.find_all():
                    if button.type(part) == 'text':
                        left, top, right, bottom = button.bbox(part)
                        assert 2 <= left < right <= button.winfo_width() - 2
                        assert 2 <= top < bottom <= button.winfo_height() - 2
                checked += 1
    app.tree.selection_set(task['id'])
    app.tree.focus(task['id'])
    idle(lauf)
    app.show_quick_plan_row()
    idle(lauf)
    assert app.row_action_target() and app.row_overflow_button.winfo_ismapped()
    with patch.object(app, 'show_item_context_menu') as more:
        taste(app.row_overflow_button, '<space>', lauf)
        assert app.tree.identify_row(more.call_args.args[0].y) == task['id']
    return f'{checked} Ansichtswechsel mit Symbol, Klartextname und aktivem Zustand; eine dauerhafte Zeilenaktion per Tastatur auf stabiler Aufgaben-ID'


def fall_abnahme3505(lauf):
    app = lauf.app
    lauf.showcase()
    checks = 0
    for design, size in (("light", "mittel"), ("dark", "mittel"), ("glass_light", "gross"), ("glass_dark", "gross")):
        app.settings["ui_font_size"] = size
        app.apply_ui_font()
        app.set_design(design)
        for geometry, visible in (("860x800", True), ("1280x800", True), ("1720x900", True),
                                  ("860x800", False), ("860x800", True)):
            app.settings.update(sidebar_visible=visible, sidebar_narrow=False)
            app._apply_sidebar_visibility()
            lauf.root.geometry(geometry + "+20+20")
            app.set_today_view()
            idle(lauf, 8)
            assert lauf.root.winfo_width() == int(geometry.split("x")[0]), ("Prüfbreite nicht erreicht", geometry, lauf.root.geometry())
            context = (design, size, geometry, visible)
            field, row = app.search_border, app.search_frame
            if app.header_density() == "minimal":
                assert not field.winfo_ismapped(), ("Heute-Suche bei Enge gequetscht", context)
            if not field.winfo_ismapped():
                assert app.plan_day_prev_button.winfo_rootx() == row.winfo_rootx(), (
                    "Lücke links vom Tagespfeil", context, app.plan_day_prev_button.winfo_rootx(), row.winfo_rootx())
            else:
                assert field.winfo_width() >= 160, ("Heute-Suchfeld zu schmal", context, field.winfo_width())
            for widget in row.pack_slaves():
                if widget.winfo_ismapped():
                    assert widget.winfo_rootx() >= row.winfo_rootx()
                    assert widget.winfo_rootx() + widget.winfo_width() <= row.winfo_rootx() + row.winfo_width()
                    assert widget is field or widget.winfo_width() >= widget.winfo_reqwidth(), ("Heute-Knopf gequetscht", context)
            app.clear_search_placeholder()
            app.search_var.set("Briefing")
            idle(lauf, 8)
            assert app.clear_search_button.winfo_ismapped(), "Aktiver Filter muss löschbar bleiben"
            assert all(w is field or w.winfo_width() >= w.winfo_reqwidth() for w in row.pack_slaves() if w.winfo_ismapped()), (
                "Heute-Knopf bei aktivem Filter gequetscht", context)
            assert not field.winfo_ismapped() or field.winfo_width() >= 160
            if not app.detail_button.winfo_ismapped():
                with patch.object(app, "show_option_panel") as options:
                    app.show_detail_mode_menu()
                    assert options.call_args.args[0] is app.plan_day_mode_button
            with patch.object(app, "show_option_panel") as options:
                app.show_plan_day_mode_menu()
                assert {"grid", "display"} <= {value[0] for value in options.call_args.args[1]}
            assert app.plan_day_prev_button.winfo_rootx() == row.winfo_rootx() if app._today_search_hidden else True
            app.clear_search()
            idle(lauf, 6)
            if visible:
                for key in ("pages", "lists", "notes", "drawings"):
                    if not app.sidebar_section_open(key):
                        app.toggle_sidebar_section(key)
                idle(lauf, 5)
                pairs = [(app.sidebar_listbox, app.sidebar_title_row)] + [
                    (getattr(app, key + "_listbox"), getattr(app, key + "_title_row"))
                    for key in ("pages", "notes", "drawings")]
                for tree, heading in pairs:
                    rows = [i for i in tree.get_children() if tree.bbox(i)]
                    if tree.winfo_ismapped() and rows:
                        gap = tree.winfo_rooty() + tree.bbox(rows[0])[1] - (heading.winfo_rooty() + heading.winfo_height())
                        assert 0 <= gap <= 2, ("Abschnitt zu weit vom Inhalt", context, gap)
            checks += 1
        app.set_home_view()
        idle(lauf, 8)
        assert app.overview_search_entry.winfo_ismapped(), "Startseiten-Suche fehlt"
        app.overview_search_var.set("Briefing")
        taste(app.overview_search_entry, "<Return>", lauf)
        assert app._quick_open["entry"].get() == "Briefing"
        assert app._quick_open["results"], "Globale Suche ohne Bestandstreffer"
        app.close_quick_open()
        app.set_template_view()
        idle(lauf, 8)
        assert app.overview_search_entry.winfo_ismapped(), "Vorlagen-Suche fehlt"
        assert app.overview_search_var.get() == "", "Startseiten-Anfrage filtert Vorlagen"
        app.overview_search_var.set("Projektstart")
        pending = app._template_search_after_id
        idle(lauf, 8)
        assert app._template_search_after_id is None and pending not in app._after_ids, "Erledigter Suchauftrag bleibt registriert"
        assert len(app.template_cards) == len(lauf.mod.glide_search.matching_templates(app.templates, "Projektstart")) > 0
        app.overview_search_var.set("kein-treffer-52af")
        idle(lauf, 8)
        assert not app.template_cards
        taste(app.overview_search_entry, "<Escape>", lauf)
        assert len(app.template_cards) == len(app.templates)
        app.set_home_view()
        idle(lauf, 6)
        assert app.overview_search_var.get() == "Briefing"
        app.overview_search_var.set("")
    return f"{checks} Heute-/Abschnitts-Geometrien und vier Suchabläufe: globaler Bestandstreffer, Vorlagenfilter/Trefferleerstand/Escape, getrennte Suchzustände"


def fall_titellaenge3504(lauf):
    """Tatsächlich gezeichnete Beschriftungen statt ungekürzter Quelldaten messen."""
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    page = app.new_page_from_markdown("# " + "W" * 40 + "\n\nPrüfseite")
    legacy = ("Bestehender vollständiger Aufgabentitel " * 3).strip()
    item = app.new_item("Alttitel", item_id="legacy-title-probe")
    item["text"] = legacy
    assert item["text"] == legacy
    app.settings["page_recent"] = [page["id"]]
    checks = 0
    for design in ("light", "dark"):
        app.set_design(design)
        for style in mod.glide_fonts.STYLES:
            app.settings["ui_font_family"] = style.family
            for size in ("mittel", "gross"):
                app.settings["ui_font_size"] = size
                app.apply_ui_font()
                for geometry in ("860x700", "1280x800"):
                    lauf.root.geometry(geometry + "+20+20")
                    app.set_pages_view()
                    idle(lauf, 6)
                    assert lauf.root.winfo_width() == int(geometry.split("x")[0])
                    buttons = [w for w in knoepfe(app.home_content, mod.RoundedButton)
                               if page["title"] in w.text and w.winfo_ismapped()]
                    assert buttons, "Seitenübersicht braucht lange Titelknöpfe"
                    for button in buttons:
                        shown = "".join(button.itemcget(i, "text") for i in button.find_all()
                                        if button.type(i) == "text")
                        assert shown.endswith("..."), ("Langer Titel ohne Auslassung", shown)
                        assert len(shown) <= 24
                        for i in button.find_all():
                            if button.type(i) == "text":
                                box = button.bbox(i)
                                assert box[0] >= 10 and box[2] <= button.winfo_width() - 10, (
                                    "Titel außerhalb des Knopfinnenraums", box, button.winfo_width())
                        assert page["title"] in button.text, "Volltext für Zugriff/Tooltip verloren"
                        assert callable(button._glide_tooltip["source"])
                        assert page["title"] in button._glide_tooltip["source"]()
                    checks += 1
                    if getattr(lauf, "capture", None) and style.key == "rubik" and geometry == "860x700":
                        sys.path.insert(0, str(REPO / "tests/tools"))
                        from releasedaten import save_windows_screenshot
                        lauf.capture.mkdir(parents=True, exist_ok=True)
                        save_windows_screenshot(lauf.root, lauf.capture / f"titellaenge-{design}-{size}.png")
                    note = next(e for e in app.lists if e.get("list_kind") == "note")
                    app.set_active_list(note["id"])
                    idle(lauf, 6)
                    editor = app.rich_note_editor
                    assert app.active_list_id == note["id"], ("Notizwechsel gescheitert", note["title"], app.get_display_title())
                    assert isinstance(editor, mod.NoteEditor) and editor.winfo_ismapped(), (
                        "Notizeditor nicht sichtbar", note["title"], type(editor).__name__)
                    assert not app.note_journal_actions.winfo_ismapped(), "Zusätzliche Journal-Knopfreihe vor dem Inhalt"
                    assert len([r for r in editor.toolbar._rows if r.winfo_manager()]) == 1, "Notizwerkzeuge mehrzeilig"
                    with patch.object(app, "toggle_journal_favorite") as favorite:
                        menu = editor.build_page_menu()
                        labels = {i: menu.entrycget(i, "label") for i in range(menu.index("end") + 1)
                                  if menu.type(i) == "command"}
                        assert sum(label == "Schreibimpuls" for label in labels.values()) == 1
                        assert any(label.startswith("Stimmung:") for label in labels.values())
                        assert any(label.startswith("Ort:") for label in labels.values())
                        index = next(i for i, label in labels.items() if "Favorit" in label)
                        menu.invoke(index)
                        favorite.assert_called_once()
                        menu.destroy()
                    if getattr(lauf, "capture", None) and style.key == "rubik" and geometry == "860x700":
                        save_windows_screenshot(lauf.root, lauf.capture / f"notiz-kompakt-{design}-{size}.png")
    assert len(app.new_item("W" * 100)["text"]) == 40
    assert app.new_item("W" * 100)["text"].endswith("...")
    assert len(app.new_item("W" * 100, item_id="neue-feste-id")["text"]) == 40
    old = app.new_item(legacy, preserve_title=True)
    old["children"] = [app.new_item(legacy, preserve_title=True)]
    restored = app.copy_items_with_new_ids([old])[0]
    copied = app.copy_items_with_new_ids([old], preserve_titles=False)[0]
    assert restored["text"] == legacy and restored["children"][0]["text"] == legacy
    assert old["text"] == legacy and old["children"][0]["text"] == legacy
    for fresh in app.walk_items([copied]):
        assert len(fresh["text"]) <= 40 and legacy in fresh["description"]
    assert app.normalize_items([item])[0]["text"] == legacy, "Alttitel beim Laden gekürzt"
    target = next(e for e in app.lists if app.list_accepts_items(e))
    target["items"].append(item)
    app.set_active_list(target["id"])
    app.save_items()
    details = app.item_details_snapshot(item)
    details["description"] = "Metadaten ändern, Alttitel bewahren"
    app.apply_task_edit(item, details)
    assert item["text"] == legacy
    details["text"] = ("Neuer Titel " * 10).strip()
    app.apply_task_edit(item, details)
    assert len(item["text"]) == 40 and item["text"].endswith("...")
    assert details["text"] in item["description"], "Original der Titeländerung fehlt"
    app.tree.selection_set(item["id"])
    app.begin_item_rename(item["id"])
    entry = app._item_rename_entry
    entry.delete(0, "end")
    entry.insert(0, "X" * 41)
    assert len(entry.get()) <= 40, "Inline-Eingabe erlaubt 41 Zeichen"
    entry.insert(0, "X" * 40)
    assert entry.get() == "X" * 40
    taste(entry, "<Return>", lauf)
    assert app.find_item_in_lists(item["id"])[0]["text"] == "X" * 40
    # TXT-Fortsetzungen werden erst nach dem vollständigen Einlesen begrenzt:
    # auch ein bereits langer erster Satz und vorhandene Beschreibungen bleiben erhalten.
    for first in ("Kurz", "W" * 80):
        original = first + "\n" + "Z" * 60 + "\nLetzte Zeile"
        imported = app.parse_txt_items([
            "1. " + first, "Text: " + "Z" * 60,
            "Beschreibung: Vorhandene Beschreibung", "Text: Letzte Zeile", "1.1. Kind"])
        assert len(imported[0]["text"]) == 40 and imported[0]["text"].endswith("...")
        assert original in imported[0]["description"], "TXT-Fortsetzung oder Originaltitel verloren"
        assert imported[0]["description"].startswith("Vorhandene Beschreibung")
        assert imported[0]["description"].count("Originaltitel:") == 1
        assert imported[0]["children"][0]["text"] == "Kind"
    # Auch der Speichereinstieg des Vorlageneditors muss die Grenze sichern,
    # unabhängig von der Eingabevalidierung. Unveränderte Alttitel bleiben erhalten.
    for initial, changed, expected in (("Kurz", "V" * 41, mod.glide_design.clip_title("V" * 41)),
                                       (("Alter Titel " * 6).strip(), None, ("Alter Titel " * 6).strip())):
        template = copy.deepcopy(app.default_template_records()[0])
        template["title"] = initial
        with mod.TemplateDraft(app, template) as draft:
            draft.title_var = mod.tk.StringVar(value=initial if changed is None else changed)
            draft.relative_var = mod.tk.BooleanVar(value=False)
            draft.dialog = mod.tk.Toplevel(lauf.root)
            draft.submit()
            assert draft.result["title"] == expected.strip()
            assert draft.result["payload"]["lists"][0]["title"] == expected.strip()
    return f"{checks} Seitenübersichts-Konfigurationen: vier Schriftstile, zwei Größen/Designs/Breiten, sichtbare Auslassung und echte Canvas-Innenkanten; 40-Zeichen-Neuanlage, TXT-Fortsetzungen, Vorlagenspeicherung und unveränderter Alttitel"


def fall_suchbreite3504(lauf):
    """Suchzeile endet an der Inhaltskante; Abstand nur vor echten Folgeknöpfen."""
    app = lauf.app
    lauf.showcase()
    library = next(e for e in app.folders if e.get("folder_kind") == "library")
    source = next(e for e in app.lists if "Wiedervorlagen" in e["title"])
    checks = 0

    def pruefen(context):
        nonlocal checks
        field, row, toolbar = app.search_border, app.search_frame, app.content_toolbar
        assert field.winfo_ismapped(), ("Suchfeld fehlt", context)
        card = app.list_frame_outer
        right = card.winfo_rootx() + card.winfo_width()
        assert toolbar.winfo_rootx() + toolbar.winfo_width() == right, (
            "Werkzeugzeile endet vor äußerer Inhaltskarte", context)
        assert row.winfo_rootx() + row.winfo_width() == right, ("Suchzeile endet vor Inhaltskante", context)
        field_right = field.winfo_rootx() + field.winfo_width()
        controls = [widget for widget in row.pack_slaves() if widget is not field and widget.winfo_ismapped()]
        if not controls:
            assert field_right == right, (
                "Suchfeld lässt rechts ungenutzte Breite", context,
                {"suchfeld_rechts": field_right, "inhaltskante": right, "luecke": right - field_right})
        else:
            first = min(widget.winfo_rootx() for widget in controls)
            assert first - field_right >= 10, ("Suchfeld überdeckt Folgeknopf", context, field_right, first)
            assert max(widget.winfo_rootx() + widget.winfo_width() for widget in controls) == right, (
                "Suchzeilenknöpfe enden vor Inhaltskante", context)
            assert all(widget.winfo_width() >= widget.winfo_reqwidth() for widget in controls), (
                "Suchzeilenknopf gequetscht", context)
        assert bool(app.current_search_query()) == bool(app.clear_search_button.winfo_ismapped()), (
            "Suche-löschen-Zustand falsch", context)
        checks += 1

    for design, size in (("light", "mittel"), ("dark", "mittel"),
                         ("glass_light", "gross"), ("glass_dark", "gross")):
        app.settings["ui_font_size"] = size
        app.apply_ui_font()
        app.set_design(design)
        for geometry, visible, narrow in (("860x700", True, False), ("1280x800", True, False),
                                         ("860x700", True, True), ("860x700", False, False),
                                         ("1280x800", False, False), ("860x700", True, False)):
            app.settings.update(sidebar_visible=visible, sidebar_narrow=narrow)
            app._apply_sidebar_visibility()
            lauf.root.geometry(geometry + "+20+20")
            idle(lauf, 6)
            # Auch Größen-/Seitenleistenwechsel im bereits geöffneten Buch.
            if app.is_library_view():
                pruefen((design, size, geometry, visible, narrow, "direkter Layoutwechsel"))
            for view in ("buch", "labels", "liste"):
                app.clear_search()
                if view == "buch":
                    app.set_active_folder(library["id"])
                elif view == "labels":
                    app.set_labels_view()
                else:
                    app.set_active_list(source["id"])
                    app.open_list_view()
                idle(lauf, 6)
                context = (design, size, geometry, visible, narrow, view)
                pruefen((*context, "ohne Suchanfrage"))
                app.clear_search_placeholder()
                app.search_var.set("Parkquartier")
                idle(lauf, 6)
                pruefen((*context, "mit Suche löschen"))
                app.clear_search()
                idle(lauf, 6)
                pruefen((*context, "nach Suche löschen"))
            app.set_active_folder(library["id"])
            idle(lauf, 6)
        if getattr(lauf, "capture", None):
            sys.path.insert(0, str(REPO / "tests/tools"))
            from releasedaten import save_windows_screenshot
            lauf.capture.mkdir(parents=True, exist_ok=True)
            save_windows_screenshot(lauf.root, lauf.capture / f"suchbreite-{design}-{size}.png")
    return f"{checks} Suchbreitenprüfungen: Inhaltskante statt Eigenbreite, Buch/Labels/Liste, leer/Suche/löschen, vier Design-/Schriftkombinationen, Mindestbreite/breit, volle/schmale/ausgeblendete Seitenleiste und Rückwechsel; Folgeknöpfe ohne Überdeckung"


def fall_seitenleistenzeilen3507(lauf):
    """Reale Zeilenhöhen wachsen mit allen vier Schriften ohne vertikalen Beschnitt."""
    app = lauf.app
    font = lauf.mod.app_font(31, root=app.root)
    filler = lauf.mod.glide_design.HAIR_SPACE
    # Dieselbe Schrift kann nach der Symbolauflösung andere Aufgabenzeichen
    # verwenden. Der MacBook-Befund wechselte von OK/[] zu ✓/□.
    for done_mark, open_mark in (("OK", "[]"), ("✓", "□"), ("OK", "[]")):
        with patch.dict(app.ICONS, check=done_mark, task_open=open_mark):
            assert app.task_marker(True, font).rstrip(filler) == done_mark
            assert app.task_marker(False, font).rstrip(filler) == open_mark
    lauf.showcase()
    checks, rows = 0, 0
    for index, schrift in enumerate(lauf.mod.glide_fonts.STYLES):
        app = lauf.app
        def schrift_waehlen(dialog, parent=None):
            dialog.update_idletasks()
            auswahl = next(feld for feld in knoepfe(dialog, lauf.mod.AppOptionMenu)
                           if tuple(feld.options) == lauf.mod.glide_fonts.LABELS)
            auswahl.menu.invoke(index)
            idle(lauf)
            speichern = next(knopf for knopf in knoepfe(dialog, lauf.mod.RoundedButton)
                             if knopf.text == "Speichern")
            speichern.command()
        with patch.object(app, "run_modal", schrift_waehlen):
            app.show_settings_dialog()
        idle(lauf)
        assert app.ui_font_family() == schrift.default_family, (schrift.label, app.ui_font_family())
        for size in ("klein", "mittel", "gross"):
            app.settings["ui_font_size"] = size
            app.apply_ui_font()
            for design in ("light", "dark"):
                app.set_design(design)
                for geometry in ("860x700", "1280x800"):
                    app.settings.update(sidebar_visible=True, sidebar_narrow=False)
                    app._apply_sidebar_visibility()
                    lauf.root.geometry(geometry + "+20+20")
                    idle(lauf, 4)
                    context = (schrift.label, size, design, geometry)
                    font_height = app.sidebar_row_font().metrics("linespace")
                    for name, style, minimum, padding in (
                            ("system_listbox", "System.Treeview", 28, 8),
                            ("sidebar_listbox", "Sidebar.Treeview", 30, 10),
                            ("notes_listbox", "Sidebar.Treeview", 30, 10),
                            ("drawings_listbox", "Sidebar.Treeview", 30, 10)):
                        tree = getattr(app, name, None)
                        if tree is None or not tree.winfo_ismapped():
                            continue
                        assert app.style.tk is tree.tk, (context, "Stil gehört zu fremdem Tk-Interpreter")
                        height = int(app.style.lookup(style, "rowheight"))
                        assert height >= minimum and height >= font_height + padding, (context, name, height, font_height)
                        for item in tree.get_children():
                            box = tree.bbox(item)
                            if box:
                                assert box[3] == height, (context, name, box, height)
                                rows += 1
                    # Auch angeheftete Zeilen müssen nach dem Designwechsel lesbar bleiben.
                    for _, pinned_row in app.pinned_sidebar_rows:
                        text_role = "selection_text" if pinned_row.cget("bg") == app.theme["selection"] else "text"
                        for label in pinned_row.winfo_children():
                            assert label.cget("fg") == app.theme[text_role], (
                                context, label.cget("text"), label.cget("fg"), app.theme[text_role])
                    assert app.SIDEBAR_ROW_HEIGHT == 30 and app.SYSTEM_ROW_HEIGHT == 28
                    assert app.SIDEBAR_LISTS_GAP == 18 and app.SIDEBAR_HEADER_BOTTOM_GAP == 0
                    if lauf.capture and size == "gross" and geometry == "860x700":
                        sys.path.insert(0, str(REPO / "tests/tools"))
                        from releasedaten import save_windows_screenshot
                        lauf.capture.mkdir(parents=True, exist_ok=True)
                        save_windows_screenshot(lauf.root, lauf.capture / f"seitenleiste-{schrift.key}-{design}.png")
                    checks += 1
        lauf.neustart()
        assert lauf.app.settings["ui_font_family"] == schrift.family
        idle(lauf, 4)
        for style in ("Sidebar.Treeview", "System.Treeview"):
            assert int(lauf.app.style.lookup(style, "rowheight")) >= 28
    assert checks == 48 and rows > checks, (checks, rows)
    return f"{checks} Konfigurationen, {rows} sichtbare Zeilen: vier Schriften, drei Größen, hell/dunkel, Mindestbreite/breit; vier Neustarts, Mindesthöhen 30/28 und Schriftreserve, Bereichsabstände 18/0"


def fall_seitenleistenabstand3504(lauf):
    """Die erste Hover-Zeile hat oben denselben Kartenabstand wie seitlich."""
    app = lauf.app
    lauf.showcase()
    app.set_labels_view()
    checks = 0

    def pruefen(context):
        nonlocal checks
        tree, card = app.system_listbox, app.sidebar_shell
        row = tree.get_children()[0]
        x, y, width, height = tree.bbox(row)
        tree.event_generate("<Motion>", x=x + width // 2, y=y + height // 2)
        idle(lauf, 3)
        assert "hover" in tree.item(row, "tags"), ("Hover fehlt", context)
        assert row not in tree.selection(), ("Hoverprobe ist ausgewählt", context)
        gaps = {
            "oben": tree.winfo_rooty() + y - card.winfo_rooty(),
            "links": tree.winfo_rootx() + x - card.winfo_rootx(),
            "rechts": card.winfo_rootx() + card.winfo_width()
                      - (tree.winfo_rootx() + x + width),
        }
        assert gaps["oben"] == gaps["links"] == gaps["rechts"], (
            "Erste Hover-Zeile hat ungleiche Kartenabstände", context, gaps)
        # Der separat gezeichnete Symbolhintergrund muss dieselbe Hover-Zeile nutzen.
        canvas = tree.icon_canvas
        rect = next(item for item in canvas.find_all()
                    if canvas.type(item) == "rectangle" and canvas.coords(item)[1] == y)
        assert canvas.itemcget(rect, "fill") == app.theme["hover"]
        tree.event_generate("<Leave>")
        idle(lauf, 2)
        assert "hover" not in tree.item(row, "tags")
        checks += 1

    for design, size in (("light", "mittel"), ("dark", "mittel"),
                         ("glass_light", "gross"), ("glass_dark", "gross")):
        app.settings["ui_font_size"] = size
        app.apply_ui_font()
        app.set_design(design)
        for geometry in ("860x700", "1280x800"):
            app.settings.update(sidebar_visible=True, sidebar_narrow=False)
            app._apply_sidebar_visibility()
            lauf.root.geometry(geometry + "+20+20")
            idle(lauf, 6)
            pruefen((design, size, geometry, "volle Seitenleiste"))
            for visible, narrow in ((True, True), (False, False), (True, False)):
                app.settings.update(sidebar_visible=visible, sidebar_narrow=narrow)
                app._apply_sidebar_visibility()
                idle(lauf, 4)
            pruefen((design, size, geometry, "nach Einklappen/Ausblenden"))
            if getattr(lauf, "capture", None) and geometry == "860x700":
                sys.path.insert(0, str(REPO / "tests/tools"))
                from releasedaten import save_windows_screenshot
                tree = app.system_listbox
                x, y, width, height = tree.bbox(tree.get_children()[0])
                tree.event_generate("<Motion>", x=x + width // 2, y=y + height // 2)
                idle(lauf, 3)
                lauf.capture.mkdir(parents=True, exist_ok=True)
                save_windows_screenshot(lauf.root, lauf.capture / f"seitenleistenabstand-{design}-{size}.png")
    # Inhaberwunsch 07.11.2026: engere Zeilen (Systemzeilen enger), größerer Abstand zwischen
    # den Abteilungen, kein Zusatzabstand unter der Abteilungsüberschrift.
    app = lauf.app
    hoehe = lambda stil: int(app.style.lookup(stil, "rowheight"))
    assert hoehe("System.Treeview") >= 28 and hoehe("Sidebar.Treeview") >= 30
    assert hoehe("System.Treeview") < hoehe("Sidebar.Treeview"), (hoehe("System.Treeview"), hoehe("Sidebar.Treeview"))
    assert getattr(app, "SIDEBAR_LISTS_GAP", 0) >= 18 and getattr(app, "SIDEBAR_HEADER_BOTTOM_GAP", 2) == 0
    for name in ("lists_title_row", "notes_title_row", "drawings_title_row"):
        zeile = getattr(app, name, None)
        if zeile is not None and zeile.winfo_manager() == "pack":
            oben, unten = zeile.pack_info()["pady"] if isinstance(zeile.pack_info()["pady"], tuple) else (zeile.pack_info()["pady"],) * 2
            assert int(oben) >= 18 and int(unten) == 0, (name, zeile.pack_info()["pady"])
    return f"{checks} Hover-Geometrieprüfungen gegen die äußere Seitenleistenkarte: oben/links/rechts gleich, vier Design-/Schriftkombinationen, Mindestbreite/breit, Rückkehr aus schmal/ausgeblendet; Symbolhintergrund und Hover-Ende"


def fall_buchbreite3503(lauf):
    """Buchbaum und Spalten nutzen die Karteninnenbreite, nicht nur ihre eigene Breite."""
    app = lauf.app
    lauf.showcase()
    library = next(e for e in app.folders if e.get("folder_kind") == "library")
    app.set_active_folder(library["id"])
    checks = 0

    def full_width(context):
        tree = app.tree
        card = app.list_frame
        assert tree.winfo_rootx() == card.winfo_rootx(), (
            "Buchtabelle beginnt nicht an der linken Karteninnenkante", context,
            tree.winfo_rootx(), card.winfo_rootx())
        right = (app.scrollbar.winfo_rootx() if app.scrollbar.winfo_ismapped()
                 else card.winfo_rootx() + card.winfo_width())
        assert tree.winfo_rootx() + tree.winfo_width() == right, (
            "Buchtabelle nutzt nicht die Karteninnenbreite", context,
            tree.winfo_width(), card.winfo_width())
        columns = ("#0", *tree.cget("displaycolumns"))
        widths = {key: int(tree.column(key, "width")) for key in columns}
        used = sum(widths.values())
        assert used == tree.winfo_width(), (
            "Buch nutzt nicht die volle Innenbreite", context,
            {"used": used, "available": tree.winfo_width(), "columns": widths})
        rows = [row for row in tree.get_children() if tree.bbox(row)]
        assert rows, "Buchprobe braucht eine sichtbare Seite"
        last = tree.bbox(rows[0], columns[-1])
        assert last[0] + last[2] == tree.winfo_width(), (
            "Buchzeile endet vor der rechten Innenkante", context, last, tree.winfo_width())
        assert "note" not in columns, "Leere Beschreibung belegt eine Spalte"
        assert not any(b.winfo_ismapped() for b in getattr(app, "_row_action_buttons", ()))

    for design, size in (("light", "mittel"), ("dark", "mittel"),
                         ("glass_light", "gross"), ("glass_dark", "gross")):
        app.settings["ui_font_size"] = size
        app.apply_ui_font()
        app.set_design(design)
        layouts = (("860x700", True, False), ("1280x800", True, False),
                   ("860x700", True, False), ("860x700", True, True),
                   ("1280x800", True, True), ("860x700", False, False),
                   ("1280x800", False, False), ("860x700", True, False))
        for geometry, sidebar_visible, sidebar_narrow in layouts:
            app.settings.update(sidebar_visible=sidebar_visible, sidebar_narrow=sidebar_narrow)
            app._apply_sidebar_visibility()
            lauf.root.geometry(geometry + "+20+20")
            idle(lauf, 8)
            context = (design, size, geometry, sidebar_visible, sidebar_narrow)
            # Größen-/Seitenleistenwechsel im bereits geöffneten Buch,
            # nicht erst nach dessen erneutem Aufbau.
            full_width(("direkter Layoutwechsel", *context))
            app.set_labels_view()
            idle(lauf, 4)
            app.set_active_folder(library["id"])
            idle(lauf, 8)
            full_width(("Ansichtswechsel", *context))
            checks += 2
    return f"{checks} Buchbreitenprüfungen bis zu beiden Karteninnenkanten: Mindestbreite/breit, volle/schmale/ausgeblendete Seitenleiste und Rückwechsel, vier Design-/Schriftkombinationen, Wechsel aus Labels"


def fall_menschen3503(lauf):
    """Inhaberbefunde: nutzbare Breite, einzeilige Werkzeuge und bewusster Zeichencursor."""
    app, tk = lauf.app, lauf.mod.tk
    lauf.showcase()
    page = next(e for e in app.lists if app.is_page_list(e) and "Briefing" in e["title"])
    library = next(e for e in app.folders if e.get("folder_kind") == "library")
    source = next(e for e in app.lists if "Wiedervorlagen" in e["title"])
    drawing = next(e for e in app.lists if app.is_drawing_list(e))
    checks = 0

    def one_row(flow):
        rows = [row for row in flow._rows if row.winfo_manager()]
        assert len(rows) == 1, ("mehrzeilige Werkzeugleiste", len(rows))
        for button, _key in flow.entries:
            if button.winfo_ismapped():
                assert button.winfo_rootx() >= flow.winfo_rootx()
                assert button.winfo_rootx() + button.winfo_width() <= flow.winfo_rootx() + flow.winfo_width(), button

    def right_padding(widget):
        value = widget.pack_info()["padx"]
        return int((value if isinstance(value, (tuple, list)) else lauf.root.tk.splitlist(str(value)))[-1])

    def capture(name):
        if getattr(lauf, "capture", None):
            sys.path.insert(0, str(REPO / "tests/tools"))
            from releasedaten import save_windows_screenshot
            lauf.capture.mkdir(parents=True, exist_ok=True)
            save_windows_screenshot(lauf.root, lauf.capture / f"menschen3503-{design}-{size}-{name}.png")

    configurations = (("light", "1280x800", "mittel"), ("dark", "860x700", "mittel"),
                      ("glass_light", "860x700", "gross"), ("glass_dark", "1280x800", "gross"))
    for design, geometry, size in configurations:
        app.settings["ui_font_size"] = size
        app.settings["show_hints"] = size == "gross"
        app.apply_ui_font()
        app.set_design(design)
        lauf.root.geometry(geometry + "+20+20")
        idle(lauf, 8)
        app.set_labels_view()
        idle(lauf, 6)
        # Abgeleitete Labelzeilen haben keine rechten Aktionsknöpfe.
        right = right_padding(app.tree)
        assert int(right) == 14, ("Labels reserviert ungenutzte Aktionsbreite", right)
        assert not any(b.winfo_ismapped() for b in getattr(app, "_row_action_buttons", ()))
        app.set_active_folder(library["id"])
        idle(lauf, 6)
        right = right_padding(app.tree)
        assert int(right) == 0, ("Buch reserviert ungenutzte Karteninnenbreite", right)
        if getattr(app, "_header_actions_docked", False):
            assert str(app.header_controls.pack_info()["in"]) == str(app.input_frame)
            assert app.add_button.winfo_ismapped(), "Hinzufügen bei Kopfumbau verdrängt"
            assert app.add_button.winfo_rootx() + app.add_button.winfo_width() <= app.header_controls.winfo_rootx()
            assert app.title_label.cget("text").startswith("Wissen"), app.title_label.cget("text")
            assert all(button.winfo_rooty() < app.input_frame.winfo_rooty()
                       for button in getattr(app, "custom_menu_buttons", ()))
        assert int(app.tree.column("#0", "width")) >= min(220, app.tree.winfo_width() - 4)
        assert sum(int(app.tree.column(key, "width")) for key in ("#0", *app.tree.cget("displaycolumns"))) <= app.tree.winfo_width(), "Buchspalten außerhalb der Fläche"
        capture("buch")

        app.set_active_list(source["id"])
        app.set_table_view()
        idle(lauf, 8)
        columns = list(app.tree.cget("displaycolumns"))
        total = sum(int(app.tree.column(key, "width")) for key in columns)
        if "tree" in str(app.tree.cget("show")):
            total += int(app.tree.column("#0", "width"))
        assert total <= app.tree.winfo_width(), ("Tabelle ragt über Baumkante", total, app.tree.winfo_width())
        if "due" in columns:
            for row in app.tree.get_children():
                if not app.tree.bbox(row):
                    continue
                text = app.tree.set(row, "due")
                box = app.tree.bbox(row, "due")
                assert app.tree_cell_font(row, "due").measure(text) + app.tree_cell_padding(app.task_row_font()) <= box[2], (text, box)
                assert box[0] + box[2] <= app.tree.winfo_width(), ("Frist rechts abgeschnitten", box)
        buttons = [b for b in app._row_action_buttons if b.winfo_ismapped()]
        assert len(buttons) >= 2, "Aktionen erst bei Hover sichtbar"
        positions = [(b.winfo_x(), b.winfo_y()) for b in buttons]
        app.tree.event_generate("<Leave>", x=0, y=0)
        idle(lauf)
        assert positions == [(b.winfo_x(), b.winfo_y()) for b in buttons]
        with patch.object(app, "show_item_context_menu") as menu:
            buttons[0].command()
            assert app.tree.identify_row(menu.call_args.args[0].y) == app.row_action_target()[1]
        if app.input_frame.winfo_y() < app.search_frame.winfo_y():
            assert app.search_frame.winfo_rooty() - (app.input_frame.winfo_rooty() + app.input_frame.winfo_height()) >= 8
        capture("tabelle")

        app.open_list_view()
        app.set_active_list(page["id"])
        idle(lauf, 8)
        editor = app.rich_note_editor
        one_row(editor.toolbar)
        assert "Überschrift" not in editor._toolbar_buttons and "Code" not in editor._toolbar_buttons
        assert editor._toolbar_buttons["Mehr"].winfo_ismapped()
        for button in editor._toolbar_buttons.values():
            assert button.height == app.add_button.height == 38
            assert button.radius == app.add_button.radius
            assert button.bg_color == app.theme["bg"]
            assert button.border_color == app.theme[button.color_key]
        assert int(editor._foot_row.pack_info()["padx"]) == 10
        assert editor._mentions_button.winfo_reqwidth() < 250
        capture("seite")

        app.set_active_list(drawing["id"])
        idle(lauf, 8)
        editor = app.drawing_editor
        one_row(editor.toolbar)
        one_row(editor.context_row)
        one_row(editor.animation_toolbar)
        assert not hasattr(editor, "color_button"), "Doppelter Farbweg in derselben Leiste"
        editor.canvas.focus_force()
        idle(lauf)
        assert editor.cursor_item is None, "Fokus allein erzeugt Zellmarkierung"
        editor.move_cursor(1, 0)
        idle(lauf)
        assert editor.cursor_item is not None, "Tastaturcursor fehlt"
        editor._motion(SimpleNamespace(x=20, y=20))
        assert editor.cursor_item is None, "Mausbewegung lässt Tastaturcursor stehen"
        for tool, _label, _key in editor.TOOLS:
            editor.set_tool(tool)
            idle(lauf)
            one_row(editor.context_row)
        capture("zeichnung")
        checks += 1
    # Teilweise sichtbare Randzeilen dürfen keine Aktion in den Kartenfuß
    # schieben. Scrollen richtet die Knöpfe auf die tatsächlichen Zeilen aus.
    many = app.new_list_object("Randzeilen", [app.new_item(f"Randaufgabe {i}") for i in range(50)])
    app.lists.append(many)
    app.save_items()
    app.set_active_list(many["id"])
    idle(lauf, 8)
    # Tk 9 kann einzelne Zeilentypen schmaler zeichnen als die Basisrolle.
    app.style.configure("Abnahme3503.App.Treeview", rowheight=26)
    app.tree.configure(style="Abnahme3503.App.Treeview")
    for position in (0, .37, 1):
        app.tree.yview_moveto(position)
        idle(lauf, 6)
        visible = [button for button in app._row_action_buttons if button.winfo_ismapped()]
        assert visible
        for button in visible:
            assert button.winfo_y() >= app.tree.winfo_y()
            assert button.winfo_y() + button.winfo_height() <= app.tree.winfo_y() + app.tree.winfo_height(), "Randaktion überdeckt Kartenfuß"
        ordered = sorted(visible, key=lambda button: button.winfo_y())
        assert all(a.winfo_y() + a.winfo_height() <= b.winfo_y() for a, b in zip(ordered, ordered[1:])), "Zeilenaktionen überdecken sich"
    # Eine inzwischen gelöschte Aufgabe darf über einen alten Knopfbefehl
    # keine andere Zeile öffnen.
    button = visible[0]
    stale = button.command
    y = button.winfo_y() - app.tree.winfo_y() + button.winfo_height() // 2
    removed = app.tree.identify_row(y)
    many["items"][:] = [item for item in many["items"] if item["id"] != removed]
    app.refresh_tree()
    idle(lauf)
    with patch.object(app, "show_item_context_menu") as menu:
        stale()
        assert not menu.called, "Veraltete Zeilenaktion öffnet anderes Ziel"
    return f"{checks} Konfigurationen: Tabelle/Buch/Labels, dauerhafte Zeilenaktion, Abstand, gemeinsame Außenknöpfe, einzeilige Seiten-/Zeichenwerkzeuge, Maus-/Tastaturcursor"


# beta350 zuletzt: Nach seinem Neustart erhält unter Windows das nächste frische
# Fenster keinen Vordergrund, und `focus_set` der Aktionsauswahl griffe nicht.
def fall_schriftstile(lauf):
    """Vier Stilklassen über die echten Einstellungen speichern und neu laden."""
    mod = lauf.mod
    assert lauf.app.ui_font_family() == "Rubik", lauf.app.ui_font_family()
    expected = ("Modern: Rubik", "Technisch: Roboto Mono",
                "Kreativ: Playfair Display", "Klassisch: Fraunces")
    assert mod.glide_fonts.LABELS == expected
    for index in (1, 2, 3, 0):
        app = lauf.app
        style = mod.glide_fonts.STYLES[index]

        def auswaehlen(dialog, parent=None):
            dialog.update_idletasks()
            felder = knoepfe(dialog, mod.AppOptionMenu)
            auswahl = next(feld for feld in felder if tuple(feld.options) == expected)
            assert auswahl.variable.get() == mod.glide_fonts.style_for(app.settings.get("ui_font_family")).label
            auswahl.menu.invoke(index)
            idle(lauf)
            assert auswahl.variable.get() == style.label, (index, auswahl.variable.get(), style.label)
            groesse = next(feld for feld in felder if tuple(feld.options) == tuple(app.UI_FONT_SIZE_CHOICES))
            groesse.menu.invoke(0 if style.body_family else 1)
            idle(lauf)
            speichern = next(knopf for knopf in knoepfe(dialog, mod.RoundedButton) if knopf.text == "Speichern")
            speichern.command()

        with patch.object(app, "run_modal", auswaehlen):
            app.show_settings_dialog()
        idle(lauf)
        assert app.settings["ui_font_family"] == style.family
        assert app.ui_font_family() == style.default_family, (
            style.label, app.ui_font_family(), style.default_family,
            mod.tkfont.Font(root=lauf.root, family=style.default_family, size=12).actual(),
            [name for name in app.available_font_families() if 'playfair' in name.lower() or 'fraunces' in name.lower()])
        for gewicht in ("normal", "bold"):
            for neigung in ("roman", "italic"):
                familie = mod.glide_fonts.family_for_weight(style.default_family, gewicht == "bold", neigung == "italic")
                font = mod.tkfont.Font(root=lauf.root, family=familie, size=12,
                                       weight=gewicht, slant=neigung)
                assert font.actual("family") == mod.glide_fonts.actual_family(familie), (style.label, font.actual())
                assert font.measure("Glide ÄÖÜ äöü ß 0123456789") > 0
                assert mod.bundled_glyph_metrics(gewicht == "bold", familie, neigung == "italic") is not None
        if style.body_family:
            for size in (8, 9, 10, 11):
                for gewicht in ("normal", "bold"):
                    specification = mod.app_font(size, *(() if gewicht == "normal" else ("bold",)), root=lauf.root)
                    font = mod.ui_font_object(root=lauf.root, font=specification)
                    familie = style.default_family if gewicht == "normal" else style.tk_family
                    assert font.cget("family") == familie, (style.label, size, font.cget("family"))
                    assert font.actual("family") == mod.glide_fonts.actual_family(familie), (style.label, size, font.actual())
                    # Tk meldet den physischen 600er-Schnitt unter Windows als
                    # bold, obwohl normal angefordert wird. Familie + Tupel
                    # unterscheiden SemiBold und den echten 700er-Schnitt.
                    assert ("bold" in specification[2:]) == (gewicht == "bold")
            assert app.tree_font()[0] == style.default_family
            assert app.sidebar_section_font()[0] == style.tk_family
            assert app.header_title_font()[0] == style.tk_family
            assert app.settings["ui_font_size"] == "klein"
            lauf.root.geometry("860x700+20+20")
            app.set_design("light")
            liste = app.new_list_object(style.label, [app.new_item("ÄÖÜ äöü ß · kleine Schrift: g j p q y 0123456789")])
            app.lists.append(liste)
            app.save_items()
            app.set_active_list(liste["id"])
            app.open_list_view()
            idle(lauf, 6)
            assert app.task_row_font().actual("family") == mod.glide_fonts.actual_family(style.default_family)
            assert app.tree.bbox(liste["items"][0]["id"]), style.label
        assert all(app.ICONS[key] == type(app).ICONS[key] for key in ("home", "today", "settings"))
        lauf.neustart()
        assert lauf.app.settings["ui_font_family"] == style.family
        assert lauf.app.ui_font_family() == style.default_family
        if style.body_family:
            app = lauf.app
            lauf.root.geometry("860x700+20+20")
            heading = mod.tkfont.Font(root=lauf.root, font=app.sidebar_title.cget("font"))
            assert heading.actual("family") == style.tk_family
            app.set_active_list(liste["id"])
            app.open_list_view()
            idle(lauf, 6)
            assert app.task_row_font().actual("family") == mod.glide_fonts.actual_family(style.default_family)
            if getattr(lauf, "capture", None) is not None and sys.platform == "win32":
                sys.path.insert(0, str(REPO / "tests/tools"))
                from releasedaten import save_windows_screenshot
                lauf.capture.mkdir(parents=True, exist_ok=True)
                for design in ("light", "dark"):
                    app.set_design(design)
                    idle(lauf, 6)
                    save_windows_screenshot(lauf.root, lauf.capture / f"{style.key}-klein-{design}.png")
    return "Vier korrigierte Stilklassen gespeichert und nach Neustart erhalten; Playfair/Fraunces SemiBold normal, echtes Bold bei 8–11 pt, Metriken einschließlich Italic; Rubik Vorgabe, Symbole vollständig"


def fall_kartenflaechen(lauf):
    """Hintergrundwechsel darf keine veralteten Farbstile in den Karten hinterlassen."""
    app = lauf.app
    liste = app.new_list_object("Kartenfläche", [app.new_item("Themenfarbe behalten")])
    app.lists.append(liste)
    app.save_items()
    app.set_active_list(liste["id"])
    app.open_list_view()
    namen = ("system_listbox", "sidebar_listbox", "pages_listbox", "notes_listbox", "drawings_listbox", "tree")
    geprueft = 0

    def pruefen(kontext):
        nonlocal geprueft
        idle(lauf, 6)
        card = app.theme["card"]
        for name in namen:
            baum = getattr(app, name)
            stil = str(baum.cget("style"))
            for option in ("background", "fieldbackground"):
                farbe = app.style.lookup(stil, option)
                assert farbe == card, (kontext, name, stil, option, farbe, card)
            if hasattr(baum, "icon_canvas"):
                assert baum.icon_canvas.cget("bg") == card, (kontext, name, "Symbolfläche",
                                                           baum.icon_canvas.cget("bg"), card)
        for karte in (app.sidebar_shell, app.list_frame_outer):
            assert karte.fill_color == card, (kontext, str(karte), karte.fill_color, card)
            assert karte.inner.cget("bg") == card
        assert lauf.root.cget("bg") == app.theme["bg"]
        geprueft += 1

    for design in ("light", "dark", "minimal_light", "minimal_dark", "glass_light", "glass_dark", "light"):
        app.set_design(design)
        for key in ("surface", "import", "clear", "default", "surface", "accent"):
            app.set_background_color(key)
            pruefen((design, key))
        app.set_table_view()
        pruefen((design, "Tabelle"))
        app.open_board_view()
        idle(lauf)
        assert app.workspace.canvas.cget("bg") == app.theme["card"]
        app.open_list_view()
        pruefen((design, "Liste nach Pinnwand"))
        if design in ("light", "dark") and getattr(lauf, "capture", None) is not None:
            sys.path.insert(0, str(REPO / "tests/tools"))
            if sys.platform == "win32":
                from releasedaten import save_windows_screenshot
                lauf.capture.mkdir(parents=True, exist_ok=True)
                save_windows_screenshot(lauf.root, lauf.capture / f"kartenflaechen-{design}.png")
    # Ein echter Verlauf darf abgeleitete Stile anlegen. Eine anschließende
    # feste Farbe entfernt sie wieder, auch wenn vorher Milchglas aktiv war.
    app.set_design("glass_light")
    app.set_backdrop_choice(lauf.mod.glide_backdrop.presets_for("glass_light")[0].key)
    # Der Test wartet auf den aktuellen aktiven Verlauf, auch wenn ein
    # Configure erst beim Pumpen der Ereignisse den nächsten Auftrag anlegt.
    # Die bestehende Gesamtfrist bleibt 30 s; keine Prüfung wird übersprungen.
    deadline = time.monotonic() + 30.0
    while app.active_backdrop() is None and time.monotonic() < deadline:
        app.wait_for_backdrop(timeout=max(0, deadline - time.monotonic()))
        idle(lauf, 2)
    assert app.active_backdrop() is not None
    app.sync_backdrop_surfaces()
    app.set_background_color("accent")
    pruefen("Feste Farbe nach Glasverlauf")
    app.set_design("light")
    pruefen("Hell nach Glasverlauf")
    lauf.neustart()
    app = lauf.app
    pruefen("Neustart")
    assert app.settings["background_color"] == "accent"
    return f"{geprueft} Farb-/Design-/Ansichtswechsel und Neustart: sechs Bäume und beide Karten auf Themenfarbe, Hintergrund dahinter"


def abnahme3505_ansichten(app, lauf):
    """Hauptansichten und typische Dokumente des Showcase (D66-Prüfungen, 07.11.2026)."""
    seite = next(e for e in app.lists if e["title"].startswith("Parkquartier · Briefing"))
    liste = next(e for e in app.lists if e["title"].startswith("Vermarktung"))
    zeichnung = next(e for e in app.lists if app.is_drawing_list(e))
    buch = next(f for f in app.folders if f.get("folder_kind") == "library")
    return (("Startseite", app.set_home_view), ("Heute", app.set_today_view), ("Labels", app.set_labels_view),
            ("Vorlagen", app.set_template_view), ("Papierkorb", app.set_trash_view),
            ("Liste", lambda: app.set_active_list(liste["id"])), ("Seite", lambda: app.set_active_list(seite["id"])),
            ("Zeichnung", lambda: app.set_active_list(zeichnung["id"])),
            ("Buch", lambda: app.set_active_folder(buch["id"])), ("Seiten", app.set_pages_view),
            ("Notizen", app.set_notes_view), ("Zeichnungen", app.set_drawings_view),
            ("Listen und Ordner", app.set_library_view), ("Pinnwand", app.open_global_board),
            ("Verspätet", app.set_overdue_view), ("Demnächst", app.set_in_progress_view))


def fall_altbestandteile(lauf):
    """D66: keine Systemelemente im Altstil (Scrollleisten u. a.) in Ansichten, Live-Liste und Dialogen."""
    sys.path.insert(0, str(REPO / "tests/tools"))
    import altbestandteile as alt
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    app.settings["release_notes_seen"] = mod.APP_VERSION
    funde, gesehen = [], []
    for design in ("light", "dark"):
        app.set_design(design)
        for name, oeffnen in abnahme3505_ansichten(app, lauf):
            oeffnen()
            idle(lauf, 8)
            funde.extend((design, name, pfad, klasse) for pfad, klasse in alt.fremdklassen(lauf.root))
            funde.extend(auswahlfeld_befunde(lauf.root, mod, (design, name)))
            gesehen.append(name)
    assert not funde, ("Systemelemente im Altstil oder verdeckte Auswahl", funde[:8])
    # Die gemeldete Stelle: Live-Liste einer Seite mit gezeichneter Leiste.
    seite = next(e for e in app.lists if e["title"].startswith("Parkquartier · Briefing"))
    app.set_active_list(seite["id"])
    idle(lauf, 8)
    editor = app.rich_note_editor
    baum = getattr(editor, "live_tree", None)
    assert baum is not None and baum.winfo_exists(), "Showcase-Seite ohne Live-Liste"
    leisten = [w for w in knoepfe(baum.master, mod.ThemedAutoScrollbar)]
    assert leisten, "Live-Liste ohne Glide-Leiste"
    dialoge = []

    def einsammeln(dialog):
        idle(lauf, 4)
        if not dialog.winfo_exists():
            return
        try:
            funde.extend((dialog.title(), "", pfad, klasse) for pfad, klasse in alt.fremdklassen(dialog))
            funde.extend(auswahlfeld_befunde(dialog, mod, dialog.title()))
            dialoge.append(dialog.title())
            dialog.destroy()
        except mod.tk.TclError:
            pass  # beim Prüfen von einer inneren Rückfrage geschlossen

    app.run_modal = lambda dialog, parent=None: einsammeln(dialog)
    app.__dict__.pop("show_info", None)
    seite = next(e for e in app.lists if e["title"].startswith("Parkquartier · Briefing"))
    liste = next(e for e in app.lists if e["title"].startswith("Vermarktung"))
    dialoge_auf = [getattr(app, name) for name in (
        "show_settings_dialog", "show_about_dialog", "show_release_notes_dialog", "open_error_log",
        "show_shortcuts_dialog", "show_storage_status", "show_backup_catalog", "show_quick_capture")]
    # Unabhängige Prüfung 07.11.2026 (R3): auch Formulare mit vielen Auswahlfeldern.
    dialoge_auf += [lambda: (app.set_active_list(liste["id"]), app.add_item_advanced()),
                    lambda: app.create_container_dialog("list"),
                    lambda: app.edit_list_details(seite["id"])]
    for oeffnen_dialog in dialoge_auf:
        vorher = {str(w) for w in lauf.root.winfo_children()}
        oeffnen_dialog()
        idle(lauf, 6)
        for neu in [w for w in lauf.root.winfo_children()
                    if str(w) not in vorher and isinstance(w, mod.tk.Toplevel) and w.winfo_exists()]:
            einsammeln(neu)
    app.show_info = lambda *a, **k: None
    assert not funde, funde[:8]
    assert {"Speicherstatus", "Sicherungsübersicht", "Schnellerfassung"} <= set(dialoge), dialoge
    assert len(dialoge) >= 10, dialoge
    bestand = alt.bestandsklassen(lauf.root)
    return (f"{len(gesehen)} Ansichten (hell/dunkel) und {len(dialoge)} Dialoge ohne Systemleisten/-elemente; "
            f"Live-Liste mit Glide-Leiste; Restbestand zur Laufzeit {bestand or 'keiner'}")


def unterzeile_teile(app):
    """Sichtbare Texte der Unterzeile unter dem Titel, von links nach rechts."""
    teile = []
    for widget in [app.stats_label] + list(app.page_chip_row.winfo_children()):
        if widget.winfo_ismapped() and str(widget.cget("text")).strip():
            teile.append((widget.winfo_rootx(), widget))
    return [widget for _x, widget in sorted(teile, key=lambda eintrag: eintrag[0])]


def fall_unterzeile(lauf):
    """D66: Steht das Logo, steht direkt unter dem Titel eine Unterzeile – in jeder Ansicht."""
    app, mod = lauf.app, lauf.mod
    geprueft = 0
    # Leerer Erststart: auch ohne Bestand nie eine leere Zeile neben dem Logo.
    for name, oeffnen in (("Startseite", app.set_home_view), ("Heute", app.set_today_view),
                          ("Vorlagen", app.set_template_view), ("Papierkorb", app.set_trash_view),
                          ("Seiten", app.set_pages_view), ("Notizen", app.set_notes_view),
                          ("Zeichnungen", app.set_drawings_view), ("Labels", app.set_labels_view)):
        lauf.root.geometry("1440x900+20+20")
        oeffnen()
        idle(lauf, 8)
        assert app.header_logo.winfo_ismapped(), ("Logo fehlt bei 1440 px", name)
        assert unterzeile_teile(app), ("leere Unterzeile im leeren Bestand", name)
        geprueft += 1
    lauf.showcase()
    app.settings["release_notes_seen"] = mod.APP_VERSION
    for groesse, design in (("mittel", "light"), ("gross", "dark")):
        app.settings["ui_font_size"] = groesse
        app.apply_ui_font()
        app.set_design(design)
        for hinweise in (False, True):
            app.settings["show_hints"] = hinweise
            for geometrie in ("1280x800", "1720x900"):
                lauf.root.geometry(geometrie + "+20+20")
                for name, oeffnen in abnahme3505_ansichten(app, lauf):
                    oeffnen()
                    idle(lauf, 8)
                    kontext = (name, groesse, design, hinweise, geometrie)
                    if not app.header_logo.winfo_ismapped():
                        continue
                    teile = unterzeile_teile(app)
                    assert teile, ("Unterzeile neben dem Logo leer", kontext)
                    titel = app.title_label
                    assert abs(teile[0].winfo_rootx() - titel.winfo_rootx()) <= 1, (
                        "Unterzeile nicht bündig unter dem Titel", kontext, teile[0].winfo_rootx(), titel.winfo_rootx())
                    for teil in teile:
                        assert teil.winfo_rooty() >= titel.winfo_rooty() + titel.winfo_height() - 1, ("über dem Titel", kontext)
                        assert teil.winfo_rootx() + teil.winfo_width() <= app.subtitle_row.winfo_rootx() + app.subtitle_row.winfo_width() + 1, (
                            "Unterzeile ragt hinaus", kontext)
                    if name == "Startseite":
                        assert "heute" in teile[0].cget("text").lower(), kontext
                    geprueft += 1
    assert geprueft >= 100, geprueft
    return f"{geprueft} Ansichtsprüfungen: Unterzeile vorhanden, bündig unter dem Titel, auch leer, groß/dunkel und mit Hinweisen"


def fall_neuerungen3(lauf):
    """D66: Die Karte „Neu in …“ zeigt höchstens drei Versionen; „Gelesen“ ohne Scrollen erreichbar."""
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    rn = mod.glide_release
    befund = []
    from itertools import product
    for schrift, groesse, design, geometry in product(
            mod.glide_fonts.STYLES, ("mittel", "gross"),
            ("light", "dark", "pixel"), ("860x700", "1280x800")):
        app.settings["ui_font_family"] = schrift.key
        app._ui_font_family = None
        assert app.ui_font_family() == schrift.default_family, (schrift.key, app.ui_font_family())
        app.settings["ui_font_size"] = groesse
        app.apply_ui_font()
        app.set_design(design)
        lauf.root.geometry(geometry + "+20+20")
        app.settings["release_notes_seen"] = rn.BEFORE_CATALOG
        app._settings_existed = True
        app._home_signature = None
        app.set_home_view()
        idle(lauf, 10)
        texte = [str(w.cget("text")) for w in knoepfe(app.home_content, mod.tk.Label)]
        versionen = [text for text in texte if text.startswith("Version ")]
        # Entscheidung D66: höchstens drei; der Katalog hat mehr, also genau drei.
        assert len(rn.history(mod.APP_VERSION)) > 3
        assert len(versionen) == 3, ("Karte zeigt nicht genau drei Versionen", len(versionen), versionen[:6])
        assert versionen[0] == f"Version {mod.APP_VERSION}", versionen
        gelesen = [k for k in knoepfe(app.home_content, mod.RoundedButton) if k.text == "Gelesen"]
        assert gelesen, "„Gelesen“ fehlt"
        unten = gelesen[0].winfo_rooty() + gelesen[0].winfo_height()
        sicht = app.home_canvas.winfo_rooty() + app.home_canvas.winfo_height()
        kontext = (schrift.key, groesse, design, geometry)
        befund.append(kontext)
        assert unten <= sicht, ("„Gelesen“ erst nach Scrollen", groesse, unten, sicht)
        assert gelesen[0].winfo_rooty() >= app.home_canvas.winfo_rooty(), kontext
        assert gelesen[0].winfo_rootx() >= app.home_canvas.winfo_rootx(), kontext
        assert gelesen[0].winfo_rootx() + gelesen[0].winfo_width() <= app.home_canvas.winfo_rootx() + app.home_canvas.winfo_width(), kontext
        assert len([text for text in texte if text.startswith("• ")]) == sum(
            len(points) for _, points in rn.notes_since(rn.BEFORE_CATALOG, mod.APP_VERSION)), ("Neuerungstext fehlt", kontext)
        if lauf.capture and sys.platform == 'win32' and schrift.key == 'roboto_mono' and groesse == 'gross':
            from releasedaten import save_windows_screenshot
            lauf.capture.mkdir(parents=True, exist_ok=True)
            save_windows_screenshot(lauf.root, lauf.capture / f'neuerungen_{design}_{geometry}.png')
        gelesen[0].command()
        idle(lauf, 6)
        assert app.settings["release_notes_seen"] == mod.APP_VERSION
    return f"{len(befund)} Konfigurationen: vier Schriften, mittel/groß, hell/dunkel/Pixel, Mindestgröße/breit; drei Versionen ohne Textkürzung, Gelesen ohne Scrollen erreichbar und wirksam"


def warte(lauf, sekunden):
    ende = time.monotonic() + sekunden
    while time.monotonic() < ende:
        idle(lauf, 2)
        time.sleep(0.02)


def fall_titelzaehler(lauf):
    """D67: Restzähler „noch N“, klare Meldung an der Grenze, keine stille Kürzung."""
    app, mod = lauf.app, lauf.mod
    tk = mod.tk
    grenze = app.CONTAINER_TITLE_MAX
    befund = []
    # 1) Feld im Feldrahmen (wie Eingabedialoge): Zähler rechts im Rahmen.
    fenster = tk.Toplevel(lauf.root)
    rahmen, feld = app._make_field(fenster)
    rahmen.pack(fill="x", padx=20, pady=20)
    feld.pack(fill="x", padx=1, pady=1)
    eingabe = tk.Entry(feld, font=mod.app_font(12))
    eingabe.pack(fill="x", padx=8, pady=6)
    zaehler = app.limit_title_entry(eingabe)
    warte(lauf, 0.2)
    assert zaehler.winfo_ismapped() and zaehler.master is feld, "Zähler nicht im Feldrahmen"
    assert zaehler.cget("text") == f"noch {grenze}", zaehler.cget("text")
    eingabe.insert(0, "x" * 37)
    warte(lauf, 0.1)
    assert zaehler.cget("text") == "noch 3", zaehler.cget("text")
    eingabe.insert("end", "yyyy")
    warte(lauf, 0.1)
    assert len(eingabe.get()) == 37, "Eingabe über die Grenze angenommen"
    assert zaehler.cget("text") == "max. 40" and str(zaehler.cget("fg")).lower() == app.theme["delete"].lower(), (
        "keine klare Meldung an der Grenze", zaehler.cget("text"), zaehler.cget("fg"))
    assert zaehler.winfo_rootx() >= eingabe.winfo_rootx() + eingabe.winfo_width(), "Zähler überdeckt den Text"
    eingabe.delete(0, "end")
    lauf.root.clipboard_clear()
    lauf.root.clipboard_append("z" * 57)
    eingabe.event_generate("<<Paste>>")
    warte(lauf, 0.1)
    assert len(eingabe.get()) == grenze and zaehler.cget("text") == "17 gekürzt", (len(eingabe.get()), zaehler.cget("text"))
    befund.append("Feldrahmen: noch 40 → noch 3 → max. 40 → 17 gekürzt")
    # 2) Formularspalte (Feld mit Geschwistern): Zähler als Zeile darunter.
    spalte = tk.Frame(fenster)
    spalte.pack(fill="x", padx=20)
    tk.Label(spalte, text="Titel").pack(anchor="w")
    zweite = tk.Entry(spalte)
    zweite.pack(fill="x")
    tk.Label(spalte, text="Weiter").pack(anchor="w")
    unter = app.limit_title_entry(zweite)
    warte(lauf, 0.2)
    assert unter.winfo_ismapped() and unter.winfo_rooty() >= zweite.winfo_rooty() + zweite.winfo_height(), "Zähler nicht unter dem Feld"
    fenster.destroy()
    # 3) Inline-Umbenennen in der Seitenleiste: Zähler rechts daneben, keine Überdeckung.
    lauf.showcase()
    app.settings["release_notes_seen"] = mod.APP_VERSION
    liste = next(e for e in app.lists if e["title"].startswith("Vermarktung"))
    app.set_active_list(liste["id"])
    warte(lauf, 0.3)
    app.begin_sidebar_rename()
    warte(lauf, 0.3)
    editor = getattr(app, "_sidebar_rename_entry", None) or next(
        (w for w in knoepfe(lauf.root, tk.Entry) if getattr(w, "_glide_limit_counter", None) is not None
         and w.winfo_manager() == "place"), None)
    assert editor is not None, "Umbenennen ohne Editor"
    leiste = editor._glide_limit_counter
    assert leiste.winfo_ismapped() and leiste.winfo_rootx() >= editor.winfo_rootx() + editor.winfo_width() - 1, "Zähler überdeckt den Inline-Editor"
    assert leiste.cget("text").startswith("noch"), leiste.cget("text")
    editor.event_generate("<Escape>")
    warte(lauf, 0.2)
    befund.append("Inline-Umbenennen mit Zähler rechts")
    # 4) Haupteingabe: Zähler nach erkanntem Titel, Ablehnung mit Zeichenzahl.
    meldungen = []
    app.show_warning = lambda titel, text, **k: meldungen.append(text)
    app.set_active_list(liste["id"])
    warte(lauf, 0.3)
    app.clear_entry_placeholder()
    app.entry.insert(0, "Kurzer Titel morgen")
    app.update_entry_limit()
    warte(lauf, 0.1)
    assert app.entry_limit_label.winfo_ismapped() and app.entry_limit_label.cget("text") == f"noch {grenze - len('Kurzer Titel')}", app.entry_limit_label.cget("text")
    app.clear_entry_text()
    app.entry.insert(0, "L" * 45)
    app.update_entry_limit()
    assert app.entry_limit_label.cget("text") == "5 zu viel", app.entry_limit_label.cget("text")
    vorher = len(liste["items"])
    app.add_item()
    assert len(liste["items"]) == vorher and meldungen and "45 Zeichen" in meldungen[-1], meldungen[-1:]
    app.clear_entry_text()
    warte(lauf, 0.1)
    assert not app.entry_limit_label.winfo_ismapped(), "Zähler bleibt bei leerer Eingabe"
    # 5) Ordneransicht: kein stilles Kürzen eines Listentitels.
    ordner = next(f for f in app.folders if f.get("folder_kind") != "library")
    app.set_active_folder(ordner["id"])
    warte(lauf, 0.3)
    listen_vorher = len(app.lists)
    app.clear_entry_placeholder()
    app.entry.insert(0, "O" * 44)
    app.add_item()
    assert len(app.lists) == listen_vorher and "44 Zeichen" in meldungen[-1], meldungen[-1:]
    app.clear_entry_text()
    # 6) Mehrzeiliges Einfügen: Rückfrage statt stiller Kürzung.
    app.set_active_list(liste["id"])
    warte(lauf, 0.3)
    lauf.root.clipboard_clear()
    lauf.root.clipboard_append("Kurz eins\n" + "W" * 55 + "\nKurz zwei")
    fragen = []
    app.themed_choice_dialog = lambda *a, **k: "einzeln"
    app.ask_yes_no = lambda titel, text, **k: (fragen.append(text), False)[1]
    vorher = len(liste["items"])
    app.paste_into_entry()
    assert len(liste["items"]) == vorher and fragen and "1 von 3 Zeilen" in fragen[-1], fragen[-1:]
    app.ask_yes_no = lambda titel, text, **k: True
    app.paste_into_entry()
    neue = liste["items"][vorher:]
    assert len(neue) == 3 and all(len(i["text"]) <= grenze for i in neue), [i["text"] for i in neue]
    assert any("W" * 55 in str(i.get("description") or "") for i in neue), "Volltext nicht in der Beschreibung"
    befund.append("Haupteingabe/Ordner/Einfügen: Zähler, Ablehnung mit Zeichenzahl, Rückfrage")
    # 7) Schnellerfassung: Zähler über den erkannten Titel (Prüfbefund F5).
    gesehen = {}

    def schnell(dialog, parent=None):
        idle(lauf, 4)
        zaehler = app._quick_capture_counter
        feld = next(w for w in knoepfe(dialog, tk.Entry) if w.master is zaehler.master)
        gesehen["leer"] = zaehler.cget("text")
        feld.insert(0, "Q" * 45 + " morgen")
        idle(lauf, 3)
        gesehen["lang"] = (zaehler.cget("text"), str(zaehler.cget("fg")).lower())
        gesehen["rechts"] = zaehler.winfo_rootx() >= feld.winfo_rootx() + feld.winfo_width() - 1
        dialog.destroy()

    app.run_modal = schnell
    app.show_quick_capture()
    idle(lauf, 3)
    assert gesehen.get("leer") == f"noch {grenze}", gesehen
    assert gesehen["lang"] == ("5 zu viel", app.theme["delete"].lower()), gesehen
    assert gesehen["rechts"], "Zähler überdeckt das Feld"
    befund.append("Schnellerfassung: Zähler über den erkannten Titel")
    return "; ".join(befund)


def fall_anhangsnamen(lauf):
    """D67: Anhangsnamen höchstens 40 Zeichen – Umbenennen erzwingen, Bestand kürzen und melden."""
    import os
    app, mod = lauf.app, lauf.mod
    grenze, speichergrenze = 40, 73  # D67: Name und Speichername
    lauf.showcase()
    app.settings["release_notes_seen"] = mod.APP_VERSION
    galerie = next(e for e in app.lists if app.is_gallery_list(e))
    quelle = Path(lauf.data) / "quelle"
    quelle.mkdir(exist_ok=True)
    langer_name = "Parkquartier Fassadenstudie Haus B Variante mit Abendlicht final.jpg"
    datei = quelle / langer_name
    datei.write_bytes(Path(app.resolve_attachment_path(galerie["attachments"][0])).read_bytes())
    vorher = len(galerie["attachments"])
    # Abbrechen: Datei wird nicht übernommen.
    fragen = []
    app.themed_input_dialog = lambda titel, prompt="", initial="", **k: (fragen.append((titel, initial)), None)[1]
    assert app.add_gallery_images(galerie["id"], [str(datei)]) == [] and len(galerie["attachments"]) == vorher
    assert fragen and fragen[0][0] == "Anhang umbenennen" and len(fragen[0][1]) <= grenze and fragen[0][1].endswith(".jpg"), fragen
    # Umbenennen ohne Endung: Endung bleibt erhalten.
    app.themed_input_dialog = lambda titel, prompt="", initial="", **k: "Fassade Abendlicht"
    neu = app.add_gallery_images(galerie["id"], [str(datei)])
    assert len(neu) == 1 and neu[0]["name"] == "Fassade Abendlicht.jpg", neu
    speicher = neu[0]["storage"].rsplit("/", 1)[-1]
    assert len(speicher) <= speichergrenze, speicher
    # Automatischer Weg (ohne Rückfrage): kürzen und klar melden.
    meldungen = []
    app.show_info = lambda titel, text, **k: meldungen.append((titel, text))
    automatisch = app.store_attachment(str(datei))
    assert len(automatisch["name"]) <= grenze and automatisch["name"].endswith(".jpg"), automatisch["name"]
    warte(lauf, 0.8)
    assert meldungen and meldungen[-1][0] == "Anhangsnamen gekürzt", meldungen
    os.remove(app.resolve_attachment_path(automatisch))
    # Bestand: alter langer Name und langer Speichername werden beim Laden gekürzt.
    alt_speicher = "attachments/" + "a" * 32 + "_" + "Sehr langer historischer Anhangsname aus einem alten Bestand.jpg"
    ziel = Path(app.resolve_attachment_path({"storage": alt_speicher}))
    ziel.write_bytes(datei.read_bytes())
    galerie["attachments"].append({"id": "a" * 32, "name": "Sehr langer historischer Anhangsname aus einem alten Bestand.jpg",
                                   "storage": alt_speicher, "size": ziel.stat().st_size, "mime": "image/jpeg",
                                   "added_at": "2026-11-01T10:00:00"})
    # Prüfbefund Codex (PR #69): Notion-Quellseite mit langem Speichernamen und sauberer Zuordnung.
    import hashlib
    sys.path.insert(0, str(REPO / "src/glide"))
    from notion_reimport import SourceRecord, content_fingerprint
    notion_speicher = "attachments/" + "b" * 32 + "_" + "Historischer Notion-Anhang mit sehr langem Dateinamen.png"
    notion_datei = Path(app.resolve_attachment_path({"storage": notion_speicher}))
    notion_datei.write_bytes(datei.read_bytes())
    notion_hash = hashlib.sha256(notion_datei.read_bytes()).hexdigest()
    notion_seite = app.new_list_object("Notion-Quellseite", [], list_kind=app.LIST_KIND_PAGE)
    notion_seite["attachments"] = [{"id": "b" * 32, "name": "Foto.png", "storage": notion_speicher,
                                    "size": notion_datei.stat().st_size, "mime": "image/png",
                                    "added_at": "2026-11-01T10:00:00"}]
    notion_seite["notion_source"] = SourceRecord("notion:" + "c" * 32, notion_seite["id"], "d" * 64,
                                                 content_fingerprint(notion_seite, {"b" * 32: notion_hash}),
                                                 "Quellseite.md").to_document()
    app.lists.append(notion_seite)
    assert app.save_items()
    meldungen = []
    # Lauf.start schaltet Hinweise vor seinem ersten Leerlauf stumm; die
    # 650-ms-Meldung kann schon dort laufen. Den echten Meldungserzeuger über
    # die gesamte Start-/Leerlaufphase beobachten, nicht erst danach.
    original_notice = lauf.mod.ListApp.show_attachment_name_notice
    def notice_beobachten(instanz, *args, **kwargs):
        with patch.object(instanz, "show_info",
                          lambda titel, text, **k: meldungen.append((titel, text))):
            return original_notice(instanz, *args, **kwargs)
    with patch.object(lauf.mod.ListApp, "show_attachment_name_notice", notice_beobachten):
        lauf.neustart()
        app, mod = lauf.app, lauf.mod
        app.show_info = lambda titel, text, **k: meldungen.append((titel, text))
        warte(lauf, 1.2)
    galerie = next(e for e in app.lists if e["id"] == galerie["id"])
    notion_neu = next(e for e in app.lists if e["id"] == notion_seite["id"])
    assert notion_neu["attachments"][0]["storage"] != notion_speicher, "Notion-Anhang nicht gekürzt"
    assert content_fingerprint(notion_neu, {"b" * 32: notion_hash}) == notion_neu["notion_source"]["local_hash"], \
        "saubere Notion-Zuordnung nach dem Anhangsumzug nicht neu verankert"
    alt = next(a for a in galerie["attachments"] if a["id"] == "a" * 32)
    assert len(alt["name"]) <= grenze and alt["name"].endswith(".jpg"), alt["name"]
    assert len(alt["storage"].rsplit("/", 1)[-1]) <= speichergrenze, alt["storage"]
    neu_pfad = Path(app.resolve_attachment_path(alt))
    assert neu_pfad.read_bytes() == datei.read_bytes(), "Inhalt nach Umbenennen verändert"
    assert not ziel.exists(), "alte Datei mit langem Namen bleibt liegen"
    # Prüfbefund PR #69: ältere JSON-Sicherungen finden den Anhang über die Umbenennungsliste.
    if hasattr(app, "attachment_renames"):
        umbenannt = app.attachment_renames()
        assert umbenannt.get(alt_speicher) == alt["storage"], umbenannt
    sicherungen = list((Path(lauf.data) / "backups").glob("liste_vor_anhangkuerzung_*.zip"))
    assert sicherungen, "keine Vorsicherung"
    import zipfile
    with zipfile.ZipFile(sicherungen[0]) as archiv:
        inhalt = set(archiv.namelist())
        assert "liste_speicher.json" in inhalt and alt_speicher in inhalt, inhalt
        assert archiv.read(alt_speicher) == datei.read_bytes(), "Vorsicherung ohne Originalbytes"
        assert "Sehr langer historischer Anhangsname" in archiv.read("liste_speicher.json").decode("utf-8")
    assert meldungen and meldungen[-1][0] == "Anhangsnamen gekürzt" and "2 Datei(en)" in meldungen[-1][1], meldungen
    # Gespeichert: ein weiterer Neustart meldet nichts mehr.
    lauf.neustart()
    app = lauf.app
    meldungen = []
    app.show_info = lambda titel, text, **k: meldungen.append((titel, text))
    warte(lauf, 1.0)
    assert not meldungen, meldungen
    # Schreibschutz: Kürzung im Speicher vollständig zurück, über die Kennung (R2/H1).
    galerie = next(e for e in app.lists if app.is_gallery_list(e))
    probe = {"id": "c" * 32, "name": "x" * 40, "storage": "attachments/" + "c" * 32 + "_x.jpg"}
    zweite = {"id": "d" * 32, "name": "x" * 40, "storage": "attachments/" + "d" * 32 + "_x.jpg"}
    galerie["attachments"] += [probe, zweite]
    app._clipped_attachment_names = [("d" * 32, "Original mit sehr langem Namen für die Probe.jpg", "x" * 40)]
    app._data_read_only = True
    assert app.back_up_before_attachment_renaming() is False
    app._data_read_only = False
    assert probe["name"] == "x" * 40 and zweite["name"].startswith("Original"), (probe["name"], zweite["name"])
    galerie["attachments"] = [a for a in galerie["attachments"] if a not in (probe, zweite)]
    # Speicherfehler nach dem Kopieren: Datensätze zurück auf die alten Dateien, Kopien bleiben liegen (R1).
    alt2 = "attachments/" + "e" * 32 + "_" + "Noch ein sehr langer historischer Anhangsname im Bestand.jpg"
    pfad2 = Path(app.resolve_attachment_path({"storage": alt2}))
    pfad2.write_bytes(datei.read_bytes())
    anhang2 = {"id": "e" * 32, "name": "Bild.jpg", "storage": alt2, "size": pfad2.stat().st_size, "mime": "image/jpeg",
               "added_at": "2026-11-01T10:00:00"}
    galerie["attachments"].append(anhang2)
    app._clipped_attachment_names = []
    assert app.back_up_before_attachment_renaming() is True
    neu2 = anhang2["storage"]
    assert neu2 != alt2
    assert app._attachment_rename_pending is not None, "kein Umbenennungsplan"
    original_speichern = app.save_items
    app.save_items = lambda *a, **k: False
    try:
        app.finish_attachment_renaming()
    finally:
        app.save_items = original_speichern
    assert anhang2["storage"] == alt2 and pfad2.exists(), "Rücknahme zeigt nicht auf die alte Datei"
    assert Path(app.resolve_attachment_path({"storage": neu2})).exists(), "Kopie bei Rücknahme gelöscht"
    # Prüfbefund PR #69: gleicher Anfang (1 MiB), anderes Ende – beide Dateien sind verschieden.
    liste = next(e for e in app.lists if e["title"].startswith("Vermarktung"))
    app.set_active_list(liste["id"])
    warte(lauf, 0.3)
    punkt = next(i for i in app.iter_tree_ids() if app.find_item_in_lists(i))
    app.open_task_inspector(punkt)
    warte(lauf, 0.3)
    kopf = b"x" * (1024 * 1024)
    eins, zwei, drei = quelle / "anfang_a.bin", quelle / "anfang_b.bin", quelle / "anfang_a_kopie.bin"
    eins.write_bytes(kopf + b"1"); zwei.write_bytes(kopf + b"2"); drei.write_bytes(kopf + b"1")
    vorher_anh = len(app._detail_state["fields"].get("attachments") or [])
    echt_dialog = mod.filedialog.askopenfilenames
    mod.filedialog.askopenfilenames = lambda **k: (str(eins), str(zwei), str(drei))
    try:
        app.add_detail_pane_attachments()
    finally:
        mod.filedialog.askopenfilenames = echt_dialog
    warte(lauf, 0.2)
    nachher_anh = len(app._detail_state["fields"].get("attachments") or [])
    assert nachher_anh - vorher_anh == 2, ("gleicher Anfang galt als Dublette", vorher_anh, nachher_anh)
    app.close_task_inspector(discard=True)
    return ("Umbenennen erzwungen (Abbruch übernimmt nichts, Endung bleibt), Speichername ≤ 73, automatische Kürzung "
            "gemeldet, Bestand nach ZIP-Vorsicherung (Datendatei und Originalbytes) gekürzt, alte Datei entfernt; "
            "Schreibschutz nimmt per Kennung zurück, Speicherfehler lässt Kopien liegen")


def fall_themenfarbe(lauf):
    """D68: Der Titel der aktuellen Ansicht trägt die Themenfarbe – lesbar in jedem Design."""
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    app.settings["release_notes_seen"] = mod.APP_VERSION
    liste = next(e for e in app.lists if e["title"].startswith("Vermarktung"))
    seite = next(e for e in app.lists if e["title"].startswith("Parkquartier · Briefing"))
    buch = next(f for f in app.folders if f.get("folder_kind") == "library")
    ansichten = (("Liste", lambda: app.set_active_list(liste["id"])), ("Seite", lambda: app.set_active_list(seite["id"])),
                 ("Buch", lambda: app.set_active_folder(buch["id"])), ("Heute", app.set_today_view),
                 ("Startseite", app.set_home_view), ("Vorlagen", app.set_template_view))
    lauf.root.geometry("1440x900+20+20")
    akzente = [key for _label, key in app.ACCENT_COLOR_CHOICES]
    geprueft = 0
    for design in app.DESIGN_ORDER:
        for akzent in ("accent", "export", "flag", "clear", "muted"):
            if akzent not in akzente:
                continue
            app.settings["accent_color"] = akzent
            app.set_design(design)
            idle(lauf, 4)
            # Erwartung unabhängig von der neuen Rolle: Themenfarbe, bei Kontrastgrau normale Schrift.
            erwartet = app.theme["text"] if akzent == "muted" else app.theme.get("view_title", app.theme["ui_accent"])
            if akzent == "muted":
                assert erwartet == app.theme["text"], (design, "Kontrastgrau dämpft den Titel")
            for name, oeffnen in ansichten:
                oeffnen()
                idle(lauf, 5)
                farbe = str(app.title_label.cget("fg")).upper()
                kontext = (design, akzent, name)
                assert farbe == erwartet.upper(), ("Titel nicht in der Themenfarbe", kontext, farbe, erwartet)
                assert mod.contrast_ratio(farbe, app.theme["bg"]) >= 4.49, ("Titel schlecht lesbar", kontext)
                geprueft += 1
            # Mit farbiger Themenfarbe ist der Titel sichtbar farbig, nicht die neutrale Schrift.
            if akzent != "muted":
                assert erwartet.upper() != app.theme["text"].upper(), (design, akzent, "Titel bleibt neutral")
    # Kompaktmodus: derselbe Titel, dieselbe Rolle.
    app.settings["accent_color"] = "export"
    app.set_design("light")
    app.set_active_list(liste["id"])
    idle(lauf, 4)
    if hasattr(app, "toggle_compact_mode"):
        app.toggle_compact_mode()
        idle(lauf, 6)
        kompakt = getattr(app, "compact_title", None)
        if kompakt is not None and kompakt.winfo_exists():
            assert str(kompakt.cget("fg")).upper() == app.theme.get("view_title", app.theme["ui_accent"]).upper(), "Kompakttitel ohne Themenfarbe"
        app.toggle_compact_mode()
        idle(lauf, 4)
    return f"{geprueft} Titelprüfungen in {len(app.DESIGN_ORDER)} Designs × 5 Themenfarben, Kontrast ≥ 4,5:1, Kontrastgrau neutral"


def auswahlfeld_befunde(wurzel, mod, kontext):
    """D69: Jedes sichtbare Auswahlfeld zeigt seinen Text vollständig; der Pfeil berührt ihn nicht."""
    funde = []
    for feld in knoepfe(wurzel, mod.AppOptionMenu):
        if not feld.winfo_viewable() or feld.winfo_width() <= 1:
            continue
        text = str(feld.cget("text"))
        if not text:
            continue
        if sichtbarer_ausschnitt(feld, mod) is None:
            continue  # aus einer scrollbaren Fläche hinausgescrollt
        schrift = mod.ui_font_object(font=feld.cget("font"))
        rand = int(float(feld.cget("padx") or 0)) + int(float(feld.cget("bd") or 0))
        textende = feld.winfo_rootx() + rand + schrift.measure(text)
        if feld.winfo_width() < rand + schrift.measure(text):
            funde.append((kontext, "Auswahltext abgeschnitten", text, feld.winfo_width(), rand + schrift.measure(text)))
            continue
        pfeil = getattr(feld, "arrow", None)
        if pfeil is not None and pfeil.winfo_viewable() and pfeil.winfo_rootx() < textende:
            funde.append((kontext, "Pfeil verdeckt den Auswahltext", text))
    return funde


def gruppe_zeilen_pruefen(app, mod):
    """Zeilen (y-Lagen) der sichtbaren Leistenknöpfe der Pinnwand; leer bei einer Zeile."""
    lagen = sorted({knopf.winfo_rooty() for knopf in knoepfe(app.workspace.bar, mod.RoundedButton)
                    if knopf.winfo_ismapped()})
    return lagen if len(lagen) > 1 else []


def fall_pinnwandleiste(lauf):
    """D69: Pinnwand-Leiste – Anordnung als vollständiger Leistenknopf, nichts abgeschnitten oder überdeckt."""
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    app.settings["release_notes_seen"] = mod.APP_VERSION
    liste = next(e for e in app.lists if e["title"].startswith("Vermarktung"))
    ordner = next(f for f in app.folders if f.get("title", "").startswith("Showcase"))
    schrift = mod.ui_font_object(font=mod.app_font(10, "bold"))
    feldschrift = mod.ui_font_object(font=mod.app_font(11))
    geprueft, befunde = 0, []
    for groesse, design, hinweise, oeffnen in (
            ("mittel", "light", True, lambda: app.set_active_folder(ordner["id"])),
            ("mittel", "light", False, lambda: app.set_active_list(liste["id"])),
            ("gross", "dark", True, lambda: app.set_active_list(liste["id"])),
            ("gross", "dark", False, lambda: app.set_active_folder(ordner["id"]))):
        app.settings["show_hints"] = hinweise
        app.settings["ui_font_size"] = groesse
        app.apply_ui_font()
        app.set_design(design)
        # 1000 px entspricht dem Inhaberbild (MacBook, 2000 px Retina-Aufnahme).
        for geometrie in ("1000x760", "1100x800", "1280x800", "1720x900"):
            lauf.root.geometry(geometrie + "+20+20")
            for layout, name in (("free", "Frei anordnen"), ("grid", "Geordnete Karten"), ("columns", "Spalten")):
                oeffnen()
                idle(lauf, 4)
                app.workspace.set_mode("board")
                app.workspace.configure_board("layout", layout)
                warte(lauf, 0.4)
                kontext = (groesse, design, geometrie, layout, app.view_mode, hinweise)
                knopf = app.workspace.layout_choice
                def sichtbare_breite(widget):
                    rechteck = sichtbarer_ausschnitt(widget, mod)
                    return rechteck[2] - rechteck[0] if rechteck else 0
                if isinstance(knopf, mod.RoundedButton):
                    sichtbar, text = knopf.winfo_ismapped(), knopf.text
                    breite, noetig = sichtbare_breite(knopf), schrift.measure(text) + 16
                else:  # Vorfassung: Auswahlfeld in der Leiste
                    feld = next((w for w in knoepfe(app.workspace.bar, mod.AppOptionMenu)
                                 if w.winfo_ismapped() and name in str(w.cget("text"))), None)
                    sichtbar = feld is not None
                    text = str(feld.cget("text")) if feld else ""
                    breite = sichtbare_breite(feld) if feld else 0
                    noetig = feldschrift.measure(text)
                if sichtbar:
                    assert text.startswith(name), ("Anordnung nicht vollständig", kontext, text)
                    assert breite >= noetig, ("Anordnung abgeschnitten", kontext, breite, noetig)
                elif geometrie == "1720x900":
                    befunde.append(("Anordnung bei breitem Fenster ausgeblendet", kontext))
                if layout == "columns":
                    gruppe = getattr(app.workspace, "group_button", None)
                    if gruppe is not None:  # seit 07.11.2026 Leistenknopf in derselben Zeile
                        assert gruppe.winfo_ismapped() or geometrie != "1720x900", ("Gruppieren fehlt", kontext)
                        if gruppe.winfo_ismapped():
                            assert sichtbare_breite(gruppe) >= schrift.measure(gruppe.text) + 16, ("Gruppieren abgeschnitten", kontext)
                    felder = [w for w in knoepfe(app.workspace.body, mod.AppOptionMenu) if w.winfo_ismapped()]
                    for feld in felder:  # Vorfassung: eigene Optionszeile
                        text = str(feld.cget("text"))
                        rand = feld.master.master
                        assert rand.winfo_width() >= feldschrift.measure(text) + 30, ("Gruppieren abgeschnitten", kontext, text)
                # Höchstens eine Leistenzeile (Abnahme 07.11.2026): alle sichtbaren Leistenknöpfe auf einer Höhe.
                if geometrie == "1720x900" and gruppe_zeilen_pruefen(app, mod):
                    breiten = [(knopf.text, knopf.winfo_reqwidth())
                               for knopf in knoepfe(app.workspace.bar, mod.RoundedButton)
                               if knopf.winfo_ismapped()]
                    befunde.append(("Pinnwandleiste mehrzeilig", kontext,
                                    gruppe_zeilen_pruefen(app, mod),
                                    app.workspace.bar.winfo_width(), breiten))
                anzahl, funde = befunde_b15(lauf, f"Pinnwand {kontext}")
                befunde.extend(funde)
                befunde.extend(auswahlfeld_befunde(lauf.root, mod, kontext))
                geprueft += anzahl
    assert not befunde, befunde[:6]
    # Die Wahl über den Knopf wirkt wie bisher und bleibt gespeichert.
    lauf.root.geometry("1720x900+20+20")
    app.set_active_list(liste["id"])
    app.workspace.set_mode("board")
    app.workspace.configure_board("layout", "free")
    warte(lauf, 0.4)
    menue = app.workspace.layout_choice.choices_menu()
    eintraege = [menue.entrycget(i, "label") for i in range(menue.index("end") + 1)]
    assert any(e.startswith("✓") and "Frei anordnen" in e for e in eintraege), eintraege
    menue.invoke(next(i for i, e in enumerate(eintraege) if "Spalten" in e))
    warte(lauf, 0.4)
    assert app.workspace.board()["layout"] == "columns"
    assert app.workspace.layout_choice.text.startswith("Spalten")
    return f"{geprueft} Knopfprüfungen in 3 Anordnungen, 4 Breiten (1000–1720 px), Liste und Ordner, Hinweise an/aus, 2 Schriften, hell/dunkel; Wahl über das Menü wirkt"


def fall_ruecktaste(lauf):
    """Abnahmebefund 07.11.2026: Rücktaste/Entf in einem Textfeld löscht nie den markierten Punkt."""
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    app.settings["release_notes_seen"] = mod.APP_VERSION
    meldungen = []
    app.show_info = app.show_warning = lambda *a, **k: meldungen.append(a[:2])
    liste = next(e for e in app.lists if e["title"].startswith("Vermarktung"))
    andere = next(e for e in app.lists if e["title"].startswith("Abstimmung"))
    papierkorb = len(app.trash)
    # 1) Pinnwand: Karte markiert, Seitenansicht offen, Rücktaste im Titelfeld (Inhaberablauf).
    app.set_active_list(liste["id"])
    warte(lauf, 0.3)
    w = app.workspace
    w.set_mode("board")
    w.configure_board("layout", "columns")
    warte(lauf, 0.6)
    karte = next(iter(w.card_boxes))
    w.select_card(karte)
    w.edit()
    warte(lauf, 0.6)
    feld = app._detail_state["fields"]["text"]
    vorher = feld.get()
    feld.focus_force()
    warte(lauf, 0.2)
    feld.icursor("end")
    feld.selection_clear()
    for taste in ("<BackSpace>", "<BackSpace>", "<Delete>"):
        feld.event_generate(taste)
        warte(lauf, 0.05)
    assert len(app.trash) == papierkorb, "Rücktaste im Titelfeld hat einen Punkt gelöscht"
    assert feld.get() == vorher[:-2], (vorher, feld.get())
    assert not [m for m in meldungen if "Punkt auswählen" in str(m)], meldungen
    app.set_active_list(andere["id"])
    warte(lauf, 0.5)
    assert app.current_list()["id"] == andere["id"], "Wechsel nach Bearbeiten blockiert"
    # 2) Liste: markierter Punkt, Fokus im Titelfeld der Seitenansicht.
    app.set_active_list(liste["id"])
    w = app.workspace
    w.set_mode("list")
    warte(lauf, 0.4)
    # Die Liste ist gruppiert; Punkte stehen unter Gruppenzeilen.
    erster = next(i for i in app.iter_tree_ids() if app.find_item_in_lists(i))
    app.tree.see(erster)
    app.tree.selection_set(erster)
    app.tree.focus(erster)
    app.open_task_inspector(erster) if hasattr(app, "open_task_inspector") else None
    warte(lauf, 0.4)
    feld = app._detail_state["fields"].get("text")
    # Prüfhinweis R5: der Inspektorteil darf nicht still entfallen.
    assert feld is not None and feld.winfo_exists(), "Inspektor mit Titelfeld nicht geöffnet"
    feld.focus_force()
    warte(lauf, 0.2)
    feld.event_generate("<BackSpace>")
    warte(lauf, 0.1)
    assert len(app.trash) == papierkorb, "Rücktaste im Inspektor hat den markierten Punkt gelöscht"
    # Gesperrter Wechsel meldet den Grund bei jedem neuen Versuch, schnelle Wiederholung nur einmal.
    echt_commit = app.commit_detail_pane
    app.commit_detail_pane = lambda *a, **k: None
    app._detail_commit_error = "Der Titel darf nicht leer sein."
    try:
        zahl = lambda: sum(1 for m in meldungen if m and m[0] == "Bearbeitung offen")
        assert app.prepare_inspector_switch() is False and zahl() == 1, meldungen[-2:]
        assert app.prepare_inspector_switch() is False and zahl() == 1, "Doppelklick meldet doppelt"
        fehler, zeit = app._detail_commit_error_shown
        app._detail_commit_error_shown = (fehler, zeit - 3)
        assert app.prepare_inspector_switch() is False and zahl() == 2, "späterer Versuch bleibt stumm"
    finally:
        app._detail_commit_error = None
        app.commit_detail_pane = echt_commit
    # 3) Bisheriges Verhalten bleibt: Rücktaste mit Fokus in der Liste löscht den markierten Punkt.
    app.close_task_inspector(discard=True) if hasattr(app, "close_task_inspector") else None
    warte(lauf, 0.3)
    app.tree.selection_set(erster)
    app.tree.focus_force()
    warte(lauf, 0.2)
    # Echte Taste am Baum (Prüfhinweis R5), nicht nur der Rückgriff auf den Fokus.
    app.tree.event_generate("<Delete>")
    warte(lauf, 0.3)
    assert len(app.trash) == papierkorb + 1, "Entf mit Listenfokus wirkt nicht mehr"
    return ("Rücktaste/Entf im Titelfeld (Pinnwand und Liste) löscht keinen Punkt, Wechsel möglich, gesperrter Wechsel "
            "meldet jeden neuen Versuch; Entf am Baum löscht wie bisher")



def restflaechen_befunde(wurzel):
    """Leere Rahmen, die die Größe entfernter Kinder behalten (Tk setzt sie nicht zurück).

    Bewusst ohne App-Hilfsfunktion, damit die Gegenprobe auf älteren Ständen läuft.
    """
    funde, stapel = [], [wurzel]
    while stapel:
        w = stapel.pop()
        for k in w.winfo_children():
            stapel.append(k)
            if k.winfo_class() != "Frame" or not k.winfo_ismapped():
                continue
            if k.pack_slaves() or k.grid_slaves() or k.place_slaves():
                continue
            try:
                if int(float(k.cget("height"))) or int(float(k.cget("width"))):
                    continue
            except Exception:
                continue
            if k.winfo_reqheight() > 1 or k.winfo_reqwidth() > 1:
                funde.append(f"{str(k)[-48:]} {k.winfo_reqwidth()}×{k.winfo_reqheight()} px")
    return funde


def fall_restflaechen(lauf):
    """Mac-Abnahme 07.11.2026: Nach Öffnen/Schließen bleibt keine leere Fläche stehen (appweite Aktionsprüfung)."""
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    app.settings["release_notes_seen"] = mod.APP_VERSION
    app.show_info = app.show_warning = lambda *a, **k: None
    seite = next(e for e in app.lists if e["title"].startswith("Parkquartier · Briefing"))
    liste = next(e for e in app.lists if e["title"].startswith("Vermarktung"))
    zeichnung = next(e for e in app.lists if app.is_drawing_list(e))
    befunde, schritte = [], []

    def pruefe(schritt):
        warte(lauf, 0.15)
        idle(lauf, 4)
        funde = restflaechen_befunde(lauf.root)
        schritte.append(schritt)
        befunde.extend(f"{schritt}: {f}" for f in funde)

    def gleich(schritt, vorher, nachher, toleranz=1):
        if abs(vorher - nachher) > toleranz:
            befunde.append(f"{schritt}: Höhe {vorher} → {nachher} px")

    lauf.root.geometry("1280x800+20+20")
    for design in ("light", "dark"):
        app.set_design(design)
        idle(lauf, 4)
        for name, oeffnen in abnahme3505_ansichten(app, lauf):
            oeffnen()
            pruefe(f"{design} {name}")
    app.set_design("light")
    # 1) Seite: „Erwähnt ohne Verweis“ auf und zu (Inhaberbefund).
    app.set_active_list(seite["id"])
    warte(lauf, 0.3)
    ed = app.rich_note_editor
    # Live-Liste ohne Lücke: Ihr Rahmen ist nicht höher als die Liste (Befund 07.11.2026,
    # die Glide-Leiste beanspruchte als Canvas 265 px Standardhöhe).
    tabelle = ed.live_tree.master
    if tabelle.winfo_height() > ed.live_tree.winfo_height() + 2:
        befunde.append(f"Live-Liste: Rahmen {tabelle.winfo_height()} px, Liste {ed.live_tree.winfo_height()} px")
    hoehe = ed.text.winfo_height()
    for runde in range(2):
        ed.toggle_mentions()
        pruefe(f"Erwähnt auf {runde + 1}")
        ed.toggle_mentions()
        pruefe(f"Erwähnt zu {runde + 1}")
        gleich(f"Erwähnt zu {runde + 1}: Seitentext", hoehe, ed.text.winfo_height())
    # 2) Titelbild setzen und entfernen.
    app.change_page_feature(seite["id"], "cover", {"kind": "drawing", "document": zeichnung["drawing"]})
    pruefe("Titelbild gesetzt")
    app.change_page_feature(seite["id"], "cover", None)
    pruefe("Titelbild entfernt")
    ed = app.rich_note_editor
    gleich("Titelbild entfernt: Seitentext", hoehe, ed.text.winfo_height())
    # 3) Live-Liste lösen (Inhaberbefund „Verknüpfung“): der Text bekommt den Platz.
    ziele = list(app.page_entry(seite["id"]).get("live_lists", []))
    assert ziele, "Showcase-Seite ohne Live-Liste"
    for ziel in ziele:
        app.remove_live_list(seite["id"], ziel)
    pruefe("Live-Liste gelöst")
    ed = app.rich_note_editor
    if ed._live_host.winfo_reqheight() > 1:
        befunde.append(f"Live-Liste gelöst: Bereich {ed._live_host.winfo_reqheight()} px hoch")
    ohne = ed.text.winfo_height()
    app.change_page_feature(seite["id"], "live_lists", ziele)
    pruefe("Live-Liste wieder verknüpft")
    app.change_page_feature(seite["id"], "live_lists", [])
    pruefe("Live-Liste erneut gelöst")
    gleich("Live-Liste erneut gelöst: Seitentext", ohne, app.rich_note_editor.text.winfo_height())
    # 4) Liste: Inspektor und Nebenansicht auf und zu.
    app.set_active_list(liste["id"])
    warte(lauf, 0.3)
    flaeche = app.list_frame_outer
    masse = (flaeche.winfo_width(), flaeche.winfo_height())
    erster = next(i for i in app.iter_tree_ids() if app.find_item_in_lists(i))
    app.open_task_inspector(erster)
    pruefe("Inspektor offen")
    app.close_task_inspector(discard=True)
    pruefe("Inspektor zu")
    app.open_side_view(seite["id"])
    pruefe("Nebenansicht offen")
    app.close_side_view()
    pruefe("Nebenansicht zu")
    nachher = (flaeche.winfo_width(), flaeche.winfo_height())
    gleich("Inspektor/Nebenansicht zu: Breite", masse[0], nachher[0])
    gleich("Inspektor/Nebenansicht zu: Höhe", masse[1], nachher[1])
    # 5) Pinnwand: Vollbild an/aus; Seitenleiste und Kompaktmodus hin und zurück.
    w = app.workspace
    w.set_mode("board")
    warte(lauf, 0.4)
    w.toggle_board_focus()
    pruefe("Vollbild an")
    app.workspace.toggle_board_focus()
    pruefe("Vollbild aus")
    app.workspace.set_mode("list")
    for umschalten, name in ((app.toggle_sidebar, "Seitenleiste"), (app.toggle_compact_mode, "Kompaktmodus")):
        umschalten()
        pruefe(f"{name} um")
        umschalten()
        pruefe(f"{name} zurück")
    assert not befunde, befunde[:6]
    return f"{len(schritte)} Ansichten und Aktionsschritte ohne Restfläche; Seitentext und Liste nach dem Schließen wieder gleich groß"


def fall_markenkante(lauf):
    """Mac-Abnahme 07.11.2026: Erledigte und offene Zeilen beginnen an derselben Textkante (✓/□ gleich breit)."""
    app, mod = lauf.app, lauf.mod
    lauf.showcase()
    app.settings["release_notes_seen"] = mod.APP_VERSION
    befunde, geprueft = [], 0

    def kanten(name, texte, schrift):
        nonlocal geprueft
        mass = mod.tkfont.Font(root=lauf.root, font=schrift)
        stufen = {}
        for text in texte:
            eingerueckt = len(text) - len(text.lstrip(" "))
            rest = text.lstrip(" ")
            if "  " not in rest:
                continue
            vorsatz = rest[:rest.index("  ") + 2].rstrip(" ") + "  "
            stufen.setdefault(eingerueckt, set()).add(mass.measure(vorsatz))
            geprueft += 1
        for stufe, breiten in stufen.items():
            if max(breiten) - min(breiten) > 1:
                befunde.append(f"{name} Stufe {stufe}: Textkante {sorted(breiten)} px")

    for groesse in ("mittel", "gross"):
        app.settings["ui_font_size"] = groesse
        lauf.neustart() if hasattr(lauf, "neustart") else None
        app = lauf.app
        app.settings["release_notes_seen"] = mod.APP_VERSION
        seite = next(e for e in app.lists if e["title"].startswith("Parkquartier · Briefing"))
        app.set_active_list(seite["id"])
        warte(lauf, 0.4)
        ed = app.rich_note_editor
        baum = ed.live_tree
        texte = [baum.item(i, "text") for i in baum.get_children("")]
        assert any(app.ICONS["check"] in x for x in texte) and any(app.ICONS["task_open"] in x for x in texte), texte
        kanten(f"Live-Liste {groesse}", texte, app.style.lookup(baum.cget("style"), "font") or "TkDefaultFont")
    assert geprueft >= 8, geprueft
    assert not befunde, befunde
    return f"{geprueft} Zeilen in der Live-Liste (mittlere/große Schrift): erledigt und offen an derselben Textkante"

def fall_fensterende3507(lauf):
    """Root-Abbau leert eigene Tcl-Aufträge, nicht die anderer Fenster/Interpreter."""
    root, app, tk = lauf.root, lauf.app, lauf.mod.tk
    fremd = tk.Tk()
    fremd.withdraw()
    fremder_job = fremd.after(60000, lambda: None)
    try:
        kind = tk.Toplevel(root)
        eigener_job = app._register_after(root.after(60000, lambda: None))
        kind.destroy()
        idle(lauf)
        assert eigener_job in root.tk.splitlist(root.tk.call("after", "info")), "Kindfenster beendet Root-Aufträge"
        assert not getattr(app, "_root_destroyed", False)
        # Ein früher Dialogschluss während eines DWM-Retrys darf keinen
        # gelöschten Tcl-Befehl zurücklassen. Auch ohne Windows-API prüfen;
        # ausschließlich der native Farbauftrag wird durch False ersetzt.
        chrome_errors = []
        original_bgerror = bool(root.tk.call("info", "commands", "bgerror"))
        if original_bgerror:
            root.tk.call("rename", "bgerror", "_glide_original_bgerror")
        root.tk.createcommand("bgerror", lambda message: chrome_errors.append(str(message)))
        try:
            dialog = tk.Toplevel(root)
            with patch.object(lauf.mod, "IS_WINDOWS", True), \
                    patch.object(app, "WINDOWS_CHROME_RETRY_DELAYS_MS", (0,)), \
                    patch.object(app, "_apply_windows_chrome_theme", return_value=False):
                app._schedule_windows_chrome_theme(dialog)
                assert dialog._glide_chrome_jobs, "Gegenprobe plant keinen Farbauftrag"
                dialog.destroy()
                idle(lauf, 4)
            assert not chrome_errors, ("Tcl-Fehler nach Dialogschluss", chrome_errors)
            assert not dialog._glide_chrome_jobs, "Abgeschlossener Farbauftrag bleibt registriert"
            assert eigener_job in root.tk.splitlist(root.tk.call("after", "info")), "Dialogschluss beendet fremden Root-Auftrag"
        finally:
            root.tk.deletecommand("bgerror")
            if original_bgerror:
                root.tk.call("rename", "_glide_original_bgerror", "bgerror")
        app.cancel_pending_callbacks()
        app.finish_recovery_session()
        app.release_data_lock()
        # Echte Destroy-/Unmap-Bindungen bleiben aktiv. Sie können während
        # des Abbaus neue Idle-Aufträge anlegen, nachdem oben schon geleert wurde.
        root.destroy()
        eigene_reste = root.tk.splitlist(root.tk.call("after", "info"))
        assert not eigene_reste, ("Tcl-Aufträge nach Root-Ende", eigene_reste)
        assert fremder_job in fremd.tk.splitlist(fremd.tk.call("after", "info")), "Fremder Interpreter verändert"
        assert getattr(app, "_root_destroyed", False)
    finally:
        fremd.tk.call("after", "cancel", fremder_job)
        fremd.destroy()
    return "Kindfenster erhält Root-Aufträge; Root-Ende ohne Tcl-Reste; fremder Interpreter unverändert"


FAELLE = ("kartenflaechen", "schriftstile", "seitenaktionen", "blockaktionen", "schreibschutz", "kopfverweise", "notiz", "nebenansicht_liste",
          "nebenansicht_seite", "nebenansicht_inspektor", "nebenansicht_einstiege", "verweisvorschau",
          "verweisvorschau_grenzen", "seitenleiste_kontext", "kompakt",
          "kompakt_ansichten", "kompakt_verlorenes_loslassen", "gestaltung", "tagessteuerung", "nebenansicht_navigation",
          "zweierpaket_gestaltung", "home_mehrfachplanung", "side_history", "folgepaket_gestaltung",
          "home_tagesnavigation", "home_mehrfachfelder", "side_verweisnavigation", "dreierpaket_gestaltung",
          "home_wochenwahl", "home_faelligkeit_aufwand", "side_verweisaktionen", "side_trefferuebersicht", "side_nachschlagen", "home_fokusdauer",
          "fokus_wechseln", "side_suchverlauf", "fokus_als_naechstes",
          "fokus_menue", "home_fokus_laeuft", "side_abschnitte", "ansichtssymbole", "eckenlabels", "hinweisplatz", "werkzeugzeile", "menschen3503", "buchbreite3503", "seitenleistenabstand3504", "seitenleistenzeilen3507", "suchbreite3504", "titellaenge3504", "abnahme3505", "altbestandteile", "unterzeile", "neuerungen3", "titelzaehler", "anhangsnamen", "themenfarbe", "pinnwandleiste", "ruecktaste", "restflaechen", "markenkante", "beta350", "fensterende3507")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--fall", choices=FAELLE + ("alle",))
    selection.add_argument("--gruppe", choices=GRUPPEN)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--capture", type=Path)
    args = parser.parse_args()
    selected = gruppen(FAELLE)[args.gruppe] if args.gruppe else (FAELLE if args.fall in (None, "alle") else (args.fall,))
    ergebnis = {"app_sha256": hashlib.sha256(args.app.read_bytes()).hexdigest(), "faelle": {}, "fehler": [],
                "gruppe": args.gruppe, "vorgesehene_faelle": selected}

    def bericht_sichern():
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            temporary = args.report.with_name(args.report.name + ".tmp")
            temporary.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            temporary.replace(args.report)

    for name in selected:
        started = time.monotonic()
        wall_started = time.time()
        ergebnis["laufender_fall"] = {"name": name, "phase": "setup", "gestartet_unix": wall_started}
        bericht_sichern()
        print(f"START {name}", flush=True)
        # Diagnose ohne geändertes Zeitlimit oder abgefangene Testfehler.
        faulthandler.dump_traceback_later(120, repeat=True)
        with tempfile.TemporaryDirectory(prefix=f"glide-arbeitsmodi-{name}-") as daten:
            lauf = None
            try:
                lauf = Lauf(args.app, daten)
                lauf.runtime = {'python': sys.version.split()[0], 'platform': sys.platform,
                                'tk': str(lauf.root.tk.call('package', 'provide', 'Tk'))}
                lauf.capture = args.capture
                ergebnis["laufender_fall"]["phase"] = "test"
                bericht_sichern()
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
                ergebnis["laufender_fall"]["phase"] = "teardown"
                bericht_sichern()
                if lauf is not None:
                    ergebnis['faelle'][name]['runtime'] = getattr(lauf, 'runtime', {})
                    if hasattr(lauf, 'compact_trace'):
                        ergebnis['faelle'][name]['event_trace'] = lauf.compact_trace[-256:]
                    if hasattr(lauf, 'editor_host_trace'):
                        ergebnis['faelle'][name]['editor_host_trace'] = lauf.editor_host_trace
                    abbauen(lauf)
        faulthandler.cancel_dump_traceback_later()
        ergebnis["faelle"][name]["dauer_s"] = round(time.monotonic() - started, 3)
        ergebnis["faelle"][name]["gestartet_unix"] = wall_started
        print(f"ENDE {name}: {ergebnis['faelle'][name]['dauer_s']:.3f} s", flush=True)
        ergebnis["laufender_fall"] = None
        bericht_sichern()
    print(json.dumps({"gruen": len(ergebnis["faelle"]) - len(ergebnis["fehler"]), "rot": ergebnis["fehler"]},
                     ensure_ascii=False))
    return 1 if ergebnis["fehler"] else 0


if __name__ == "__main__":
    sys.exit(main())
