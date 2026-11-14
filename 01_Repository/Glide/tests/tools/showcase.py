#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Erzeugt den aktiven Showcase mit echten App-APIs in einem temporären Bestand.

Bildquellen: PNG-Arbeitskopien unter tests/fixtures/showcase/bilder.
Alle Termine beziehen sich auf --tag; ohne Angabe auf den Erzeugungstag.
Kein Zugriff auf den persönlichen Glide-Datenordner, keine Laufzeitänderung.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import tempfile
from datetime import date, timedelta

from rundgang import load_module, ruhe

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "tests/fixtures/showcase"
STOCK = TARGET / "bilder"
BRIEFING_TITLE = "Werkhaus West · Rundgang"
MAIN_TITLE = "Offene Werkstatt"
FOCUS_TASK = "Laufweg im Erdgeschoss abnehmen"
PHOTO_TITLE = "Raumstudien"
PIXEL_TITLE = "Leitschild · Lichtwechsel"
NOTIZ_TITLE = "Freitagsrunde · Offene Fragen"
PHOTOS = [
    (STOCK / "Planstudie.png", "Vom Plan zum Raum", "Referenz für den Einstieg: Linie und Modell in einem Bild."),
    (STOCK / "Licht-zum-Hof.png", "Licht zum Hof", "Modellstudie für den letzten Abschnitt des Rundgangs."),
    (STOCK / "Materialwand.png", "Ruhiger Hintergrund", "Wandfläche und Einfassung für die kleine Materialschau."),
    (STOCK / "Sitzbereich.png", "Sitzen und sprechen", "Referenz für die Bank am Ende des Rundgangs."),
]

BRIEFING = """## Die Tür ist der Anfang

Beim Probelauf sind drei Leute direkt zur Modellwand gegangen. Ab Samstag beginnt der Rundgang am Tisch neben der Tür. Dort liegen der Plan und zwei Materialproben. An der Modellwand bleibt Platz für Fragen.

### 1. Ankommen und orientieren

PLAN: Die Zeichnung zeigt, wie wenig Text eine gute Orientierung braucht. Das ist die Richtung für das Schild am Eingang.

- [x] Türöffnung und Weg durch den Hof geprüft
- [ ] Schild bei eingeschaltetem Licht aus fünf Metern lesen
- [ ] Mit Lea den Engpass an der Modellwand ablaufen

### 2. Am Modell stehen bleiben

HOF: Am Modell bleibt nur die Leuchte über dem Hof an. Die zweite nimmt Spiegelungen aus der Scheibe. Beim Probelauf hat das am besten funktioniert.

> Für den Rundgang reichen zwölf Minuten. Wer länger am Modell bleiben will, kann sich danach in Ruhe dazustellen.

### 3. Material in die Hand nehmen

BANK: Zwei Hölzer und ein Putzmuster liegen an der Bank bereit. Die Karte daneben trägt nur Materialname und Einsatzort.

Offene Fragen aus dem Probelauf
"""

MEETING = """## Freitag am großen Tisch

Lea hat den Eingang mit einer Klebebandlinie markiert. Die Gruppe sieht das Modell jetzt erst nach der kurzen Begrüßung. Das nimmt am Anfang etwas Unruhe raus.

- Jona bringt um halb zehn die beiden Musterplatten aus dem Lager.
- Mira wartet noch auf die Druckerei. Falls der Karton bis Montag fehlt, drucken wir die kleinen Karten im Studio.
- Beim Probelauf bitte einmal mit jemandem testen, der den Raum noch nie gesehen hat.

> Die Bank am Fenster bleibt frei. Da legen wir keine Kisten ab.
"""


def letzter_werktag(anchor):
    """Letzter Montag–Freitag des Monats von `anchor`, sonst des Folgemonats."""
    jahr, monat = anchor.year, anchor.month
    while True:
        tag = date(jahr + monat // 12, monat % 12 + 1, 1) - timedelta(days=1)
        while tag.weekday() > 4:
            tag -= timedelta(days=1)
        if tag >= anchor:
            return tag
        jahr, monat = jahr + monat // 12, monat % 12 + 1


def zweiter_dienstag(anchor):
    """Zweiter Dienstag des Monats von `anchor`, sonst des Folgemonats."""
    jahr, monat = anchor.year, anchor.month
    while True:
        erster = date(jahr, monat, 1)
        tag = erster + timedelta(days=(1 - erster.weekday()) % 7 + 7)
        if tag >= anchor:
            return tag
        jahr, monat = (jahr + 1, 1) if monat == 12 else (jahr, monat + 1)


def leitschild(mod, light):
    """Rastermotiv für das Leitschild am Eingang, mit wechselnder Signalleuchte."""
    bild = mod.glide_drawing.DrawingModel.blank(32)
    def rechteck(x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                bild.set_cell(xx, yy, color)

    rechteck(0, 0, 32, 32, "#14292E")
    rechteck(2, 2, 28, 28, "#275355")
    rechteck(3, 3, 26, 26, "#193438")
    rechteck(6, 6, 20, 16, "#295254")
    rechteck(7, 7, 18, 14, "#DCE5CC")
    rechteck(10, 13, 10, 3, "#183538")
    for delta in range(5):
        rechteck(17 + delta, 10 + delta, 3, 2, "#183538")
        rechteck(17 + delta, 18 - delta, 3, 2, "#183538")
    rechteck(8, 25, 10, 2, "#6B8B7C")
    rechteck(22, 24, 4, 3, light)
    return bild


def bildfolge(mod):
    colors = ("#DCA553", "#FFDB79", "#FFD16A", "#A66C34")
    frames = [{"id": f"frame-{index}", "drawing": leitschild(mod, color).to_document(), "duration_ms": None}
              for index, color in enumerate(colors, 1)]
    return {"format": mod.glide_animation.FORMAT, "format_version": mod.glide_animation.FORMAT_VERSION,
            "width": 32, "height": 32, "duration_ms": 300, "frames": frames}


def build(app, mod, root, anchor):
    """Zusammenhängende Dokumente; zurückgegeben wird die portable Projektwahl."""
    tag = lambda offset: (anchor + timedelta(days=offset)).isoformat()
    app.flush_rich_note()
    app.settings["daily_hints"] = {}
    app.lists = [entry for entry in app.lists if entry.get("system_role") == "inbox"]
    app.folders = []
    labels = {}
    for name, color in (("Werkhaus", "accent"), ("Raum", "clear"), ("Freigabe", "flag"),
                        ("Einladung", "export"), ("Warten", "due_action")):
        label = app.new_label_object(name, color=color)
        app.labels.append(label)
        labels[name] = label["id"]
    icon = mod.glide_drawing.DrawingModel.blank(16)
    for y in range(5, 14):
        for x in range(3, 13):
            icon.set_cell(x, y, "#1C6A77" if y > 8 else "#E8AD43")
    icon_doc = icon.to_document()
    attachments_dir = Path(mod.BASE_DIR) / "showcase-quellen"
    attachments_dir.mkdir(parents=True, exist_ok=True)
    model = leitschild(mod, "#FFDB79")
    generated = {
        "Leitschild-Entwurf.png": model.to_png(scale=8),
        "Werkhaus-Symbol.ico": icon.to_ico(),
        "Werkhaus-Palette.gpl": mod.glide_drawing.palette_to_gpl("Werkhaus", ["#1C6A77", "#E8AD43", "#CFE8F7"]).encode(),
        "Werkhaus-Palette.hex": mod.glide_drawing.palette_to_hex(["#1C6A77", "#E8AD43", "#CFE8F7"]).encode(),
        "Raumplan.csv": "Station;Ort;Status\n01;Eingang;markiert\n02;Modellwand;offen\n".encode(),
        "Uebergabe.txt": "Werkhaus West\nMontag: Einladung und Wegführung am Eingang gegenprüfen.\nDie Bank am Fenster bleibt frei.\n".encode(),
    }
    generated_attachments = []
    for name, content in generated.items():
        path = attachments_dir / name
        path.write_bytes(content)
        generated_attachments.append(app.store_attachment(str(path)))
    project = app.new_folder_object("Werkhaus West", color="accent", icon=icon_doc,
                                    note="Offene Werkstatt: Rundgang, Einladung und Vorbereitung.")
    library = app.new_folder_object("Werkstattbuch", parent_id=None, folder_kind="library")
    journal = app.new_folder_object("Studiojournal", parent_id=None, folder_kind="journal")
    archive = app.new_folder_object("Archiv · Probelauf", parent_id=project["id"], archived=True,
                                    archived_at=tag(-7)+"T16:00:00+02:00")
    app.folders.extend([project, library, journal, archive])
    stored = {name: app.store_attachment(str(name)) for name, _title, _note in PHOTOS}
    assert all(stored.values()), "Ein Beispielbild konnte nicht eingelesen werden."
    # Ein Anhang am Ordner bleibt beim Projektimport und bei der Vorlage erhalten.
    project["attachments"] = [copy.deepcopy(stored[PHOTOS[3][0]])]
    def task(text, **kwargs):
        return app.new_item(text, **kwargs)
    specification = task(FOCUS_TASK, due=tag(0), due_time="11:00", importance=3,
        planned_date=tag(0), planned_time="09:00", estimated_minutes=75, time_spent_minutes=20,
        labels=[labels["Einladung"], labels["Freigabe"]],
        description="Lea läuft den Weg vom Hoftor bis zur Modellwand ab. Die Kisten am Abzweig vorher wegräumen.",
        attachments=[copy.deepcopy(stored[PHOTOS[3][0]])],
        checklist=[{"text":"Eingang markiert", "done":True}, {"text":"Engpass an der Modellwand prüfen"}, {"text":"Schild am Abzweig markieren"}])
    images = task("Motiv für die Einladung auswählen", due=tag(1), planned_date=tag(0), planned_time="11:00",
        estimated_minutes=45, importance=2, labels=[labels["Raum"], labels["Freigabe"]],
        attachments=[copy.deepcopy(stored[PHOTOS[0][0]]), copy.deepcopy(stored[PHOTOS[1][0]])],
        description="Mira bevorzugt die Planstudie. Den Ausschnitt für Handy und Druck zusammen prüfen.")
    design = task("Druckdatei für den Eingang bauen", kind=app.ITEM_KIND_LONG, due=tag(2),
        planned_date=tag(0), planned_time="13:30", estimated_minutes=80, importance=2, labels=[labels["Raum"]],
        description="A3 am Eingang, kleine Karte am Modell. Der Pfeil muss bei Gegenlicht aus fünf Metern erkennbar sein.",
        links=[images["id"]], blocked_by=[specification["id"]], color="clear",
        checklist=[{"text":"Maß und Papier geklärt", "done":True}, {"text":"Hell-Dunkel-Probe"}, {"text":"PDF an die Druckerei"}])
    release = task("Einladung an den Verteiler geben", due=tag(4), importance=3,
        labels=[labels["Freigabe"]], blocked_by=[design["id"]], links=[specification["id"]],
        attachments=[copy.deepcopy(generated_attachments[-1])],
        reminder={"mode":"fixed", "at":app.local_reminder_time(tag(4), "10:00")},
        description="Text und Bild freigeben, anschließend den Termin im Rundbrief ankündigen.")
    completed = task("Schlüssel fürs Hoftor abgeholt", done=True, done_at=tag(-1)+"T14:30:00+02:00",
                     planned_date=tag(-1), estimated_minutes=60, time_spent_minutes=55)
    missing = task("Papiermuster bei der Druckerei anfragen", due=tag(-1), importance=1,
                   labels=[labels["Warten"]], description="Mira hat angerufen. Rückruf wegen des ungestrichenen Kartons steht noch aus.")
    checklist = task("Kiste für den Eingang packen", kind=app.ITEM_KIND_GROUP, children=[
        task("Klemmbrett und Klebeband einpacken", due=tag(3), estimated_minutes=15),
        task("Drei Ersatzkarten mitnehmen", due=tag(3), estimated_minutes=30),
        task("Stifte nachgefüllt", done=True, done_at=tag(0)+"T08:30:00+02:00")])
    main = app.new_list_object(MAIN_TITLE, [
        task("Vor Ort und im Studio", kind=app.ITEM_KIND_HEADING), completed, specification, images, design,
        missing, task("Vor dem Öffnen", kind=app.ITEM_KIND_HEADING), checklist, release], folder_id=project["id"],
        labels=[labels["Werkhaus"]], icon=icon_doc, color="accent", attachments=generated_attachments[2:],
        note="Vor dem nächsten Rundgang. Mira übernimmt die Einladung, Lea den Weg durchs Haus.")
    note = app.new_list_object(NOTIZ_TITLE, [task("Jona wegen Musterplatten schreiben", due=tag(0)),
        task("Ausschnitt prüfenen vom Probelauf sortieren", planned_date=tag(1), estimated_minutes=30)],
        folder_id=project["id"], list_kind="note", rich_note=mod.glide_page_markdown.markdown_to_page(MEETING),
        labels=[labels["Werkhaus"]], attachments=[copy.deepcopy(stored[PHOTOS[2][0]])])
    gallery = app.new_list_object(PHOTO_TITLE, [], folder_id=project["id"],
        list_kind="gallery", attachments=[copy.deepcopy(stored[name]) for name, _, _ in PHOTOS],
        note="Was wir für den Rundgang, das Schild und die Einladung aus den Referenzen mitnehmen.")
    animation = bildfolge(mod)
    drawing = app.new_list_object(PIXEL_TITLE, [], folder_id=None, list_kind="drawing",
        drawing=copy.deepcopy(animation["frames"][0]["drawing"]), animation=animation, icon=icon_doc,
        attachments=generated_attachments[:2],
        drawing_reference={"attachment_id":generated_attachments[0]["id"], "mode":"fit", "zoom_percent":100},
        note="Leitschild mit vier Lichtstufen, "
             "PNG-Referenz und separatem 16-Pixel-Symbol.")
    app.lists.extend([main, note, gallery, drawing])
    for name, title, caption in PHOTOS:
        app.set_gallery_caption(gallery["id"], stored[name]["id"], title, caption)
    routines = app.new_list_object("Aufschließen · Wiederkehrende Checkliste", [task("Hoftor aufschließen"),
        task("Weg im Hof freihalten", done=True), task("Karten und Stifte nachlegen")],
        folder_id=project["id"], recurring_checklist=True, color="due_action")
    repeats = []
    for index, (title, rule, offset) in enumerate([
        ("Postfach der Werkstatt prüfen", {"art":"taeglich"}, 0),
        ("Montagsrunde im Studio", {"art":"woechentlich"}, 1),
        ("Musterregal abgleichen", {"art":"tage", "abstand":14}, 2),
        ("Abholzeiten aktualisieren", {"art":"wochentage", "tage":[0,4]}, 3),
        ("Bildarchiv sichern", {"art":"monatlich"}, 5),
        ("Jahresrückblick zusammentragen", {"art":"jaehrlich"}, 7),
        # Serie aus FP-02 (3.44.0): erster Termin ist der nächste letzte Werktag.
        ("Monatsrückblick ins Journal schreiben", {"art":"serie", "rrule":"FREQ=MONTHLY;INTERVAL=1;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1"},
         (letzter_werktag(anchor) - anchor).days),
        # Erweiterte Rhythmen FP-02 Stufe 2 (3.44.0): n-ter Wochentag, Bezug auf
        # Erledigung, begrenzte Anzahl und Pause.
        ("Materialrunde im Studio", {"art":"serie", "rrule":"FREQ=MONTHLY;INTERVAL=1;BYDAY=2TU"},
         (zweiter_dienstag(anchor) - anchor).days),
        ("Pflanzen am Hoftor gießen", {"art":"tage", "abstand":3, "bezug":"erledigt"}, 1),
        ("Fototermin nachfassen", {"art":"woechentlich", "rest":3}, 4),
        ("Einladungsliste aufräumen", {"art":"monatlich", "pausiert":True}, 10)]):
        repeats.append(task(title, due=tag(offset), repeat=rule, reminder={"mode":"relative", "minutes":30},
                            due_time="09:00", estimated_minutes=15,
                            labels=[labels[("Einladung", "Raum", "Freigabe", "Warten")[index % 4]]]))
    rhythm = app.new_list_object("Studioroutinen", repeats, folder_id=project["id"],
                                 note="Alle sieben Wiederholungsarten, Serien am letzten Werktag und am zweiten "
                                      "Dienstag, Abstand nach Erledigung, begrenzte Anzahl und eine pausierte Reihe; "
                                      "Systembenachrichtigungen sind im Showcase ausgeschaltet.")
    rhythm["items"].insert(2, task("Karten vom letzten Termin aktualisieren", due=tag(3),
        planned_date=tag(2), labels=[labels["Einladung"], labels["Raum"]], estimated_minutes=30))
    app.lists.extend([routines, rhythm])
    inbox = next(entry for entry in app.lists if entry.get("system_role") == "inbox")
    inbox["items"] = [task("Foto vom Schild am Hoftor ablegen", labels=[labels["Raum"]]),
                       task("Nachbarin wegen Hofzugang zurückrufen", description="Sie kommt voraussichtlich mit dem Lastenrad.")]
    for offset, mood, title, text in [
        (-1, "grateful", "Erster Lauf durch den Hof", "Das Schlüsselschild war zu klein. Lea hat das Tor mit einer gelben Karte markiert. Beim nächsten Test gehen wir Warteraum und Modellwand getrennt ab."),
        (0, "thoughtful", "Freitag · Das Licht am Modell", "Die Streiflichtprobe am Modell war besser als gedacht. Nur das Fenster spiegelt, wenn beide Lampen an sind. Den zweiten Stromkreis nach dem Abnahmelauf ausschalten.")]:
        app.lists.append(app.new_list_object(title, [], folder_id=journal["id"], list_kind="note",
            rich_note=mod.glide_page_markdown.markdown_to_page("# "+title+"\n\n"+text),
            journal={"moment_date":tag(offset), "mood":mood, "favorite":offset==-1,
                     "location":"Studio am Hof", "prompt":"Was möchte ich von heute bewahren?"}))
    app.lists.append(app.new_list_object("Probelauf am Donnerstag", [task("Gruppengröße für Rundgang klären", done=True,
        done_at=tag(-7)+"T12:00:00+02:00"), task("Rundgang intern testen", done=True,
        done_at=tag(-7)+"T15:00:00+02:00")], folder_id=archive["id"], archived=True,
        archived_at=tag(-7)+"T16:00:00+02:00"))
    app.save_items()
    pages = []
    for title, text in (
        ("Schilder und Druck", "## Am Hoftor\n\nA3 quer, ein Pfeil, darunter der Zugang zum Studio.\n\n## Am Modell\n\nVier schmale Karten mit Material und Einsatzort. Die große Platte bleibt beschriftungsfrei."),
        ("Material am Modell", "## Die kleine Auswahl\n\nEiche geölt, Sperrholz roh und das helle Putzmuster aus dem Lager. Jona stellt die Kiste morgens an die Bank."),
        ("Einladung & Ablauf", "## Samstag im Werkhaus\n\nKurzer Rundgang ab 14 Uhr. Die Tür zum Hof bleibt offen. Die Führung startet jeweils am Klebeband vor dem ersten Tisch."),
        ("Rückblick · Probelauf", "## Wege und Wartezeiten\n\nZwei Gruppen nacheinander funktionieren besser als ein großer Rundgang. Wer warten möchte, bleibt im Hof."),
    ):
        pages.append(app.new_page_from_markdown(text, title=title, folder_id=library["id"]))
    briefing = app.new_page_from_markdown(BRIEFING, title=BRIEFING_TITLE, folder_id=library["id"])
    ruhe(root)
    app.set_active_list(briefing["id"])
    ruhe(root)
    editor = app.rich_note_editor
    # Richtige Editor-Anker verwenden; Bilder gehören als Anhänge zur Seite.
    for prefix, filename, mode, width in reversed([
        ("PLAN:", PHOTOS[0][0], "center", 590),
        ("BANK:", PHOTOS[1][0], "left", 250),
        ("HOF:", PHOTOS[2][0], "right", 300)]):
        lines = editor.text.get("1.0", "end-1c").splitlines()
        index = f"{next(i for i, line in enumerate(lines, 1) if line.startswith(prefix))}.0"
        key = editor.insert_images([str(filename)], index)[0]
        editor.images[key].update(mode=mode, width=width)
    # Klappblock mit echten semantischen Tags, keine gemalte Attrappe.
    lines = editor.text.get("1.0", "end-1c").splitlines()
    line = next(i for i, text in enumerate(lines, 1) if text.startswith("Offene Fragen aus dem Probelauf"))
    editor.text.delete(f"{line}.0", f"{line}.end")
    editor.text.insert(f"{line}.0", "Offene Fragen aus dem Probelauf\nBlenden die beiden Leuchten an der Modellwand?\n"
                       "Reicht der Durchgang, wenn eine Gruppe am Tisch wartet?\n"
                       "Nach dem letzten Gast Schild und Klemmbrett ins Studio zurückbringen.")
    editor.text.mark_set("insert", f"{line}.0")
    editor.convert_block("toggle")
    for number in range(line+1, line+4):
        editor.text.tag_add("indent1", f"{number}.0", f"{number}.end")
    editor.set_toggle_open(f"{line}.0", False)
    editor.flush()
    ruhe(root)
    # Live-Liste und lokale Verweise (G29/G08): Die Seite zeigt den aktuellen
    # Stand der Umsetzungsliste, die Abstimmungsnotiz verweist auf Seite und
    # Liste; Rückverweise entstehen daraus ohne zweiten Bestand.
    briefing = next(entry for entry in app.lists if entry["id"] == briefing["id"])
    briefing["live_lists"] = mod.glide_pages.live_lists([mod.glide_objects.uri("list", main["id"])])
    note["references"] = mod.glide_objects.normalize([mod.glide_objects.uri("item", specification["id"]),
                                                      mod.glide_objects.uri("list", briefing["id"]),
                                                      mod.glide_objects.uri("list", main["id"])])
    app.save_items()
    ruhe(root)
    # Zwei kleine, portable Vorlagen ergänzen den vorhandenen Katalog.
    meeting_template = app.capture_template(list_id=note["id"])
    meeting_template = next(t for t in app.templates if t["id"] == meeting_template["id"])
    meeting_template["title"] = "{{Wochentag}} KW {{KW}} · {{Projekt}}"
    meeting_template["note"] = "Datumsfelder füllen sich selbst; Projekt wird abgefragt. Aufgaben und Anhang bleiben enthalten."
    routine_template = app.capture_template(list_id=routines["id"])
    routine_template = next(t for t in app.templates if t["id"] == routine_template["id"])
    routine_template["title"] = "Werkhaus · Aufschließen"
    meeting_template = next(t for t in app.templates if t["id"] == meeting_template["id"])
    settings = copy.deepcopy(app.settings)
    board_cards = [{"list_id":main["id"], "item_id":item["id"], "x":x, "y":y, "scale":"normal"}
        for item, x, y in [(specification,24,60), (images,320,60), (design,320,500), (release,640,60)]]
    board_cards.append({"list_id":drawing["id"], "item_id":mod.ItemWorkspace.PAGE_CARD_PREFIX+drawing["id"],
                        "x":24, "y":500, "scale":"small"})
    folder_scope = "folder:"+project["id"]
    list_scope = "list:"+main["id"]
    settings.update(profile_name="Studio am Hof", start_on_home=True, show_home_stats=True,
        sidebar_sections_visible={"pages":True,"lists":True,"notes":True,"drawings":True},
        sidebar_locations={},
        mascot_name="Gismo", mascot_playful=False, system_notifications=False,
        pinned_pages=[{"kind":"list", "id":briefing["id"]}, {"kind":"folder", "id":library["id"]}],
        recent_lists=[{"id":entry["id"], "edited_at":tag(0)+"T10:00:00+02:00"} for entry in [briefing,note,drawing]],
        page_favorites=[briefing["id"], pages[0]["id"]], page_recent=[briefing["id"], pages[1]["id"]],
        gallery_tile_size={gallery["id"]:"large"},
        list_group_by={main["id"]:"importance"},
        saved_filters=[{"id":"showcase-freigabe", "name":"Werkhaus · Freigaben", "query":"",
                        "label_ids":[labels["Freigabe"]], "list_ids":[main["id"]], "status":"open"},
                       {"id":"showcase-woche", "name":"Diese Woche · Eisenhower", "query":"",
                        "label_ids":[], "list_ids":[], "status":"open"}],
        # FP-03 (3.44.0): gespeicherte Bedingungen und Darstellung je Ansicht.
        saved_view_conditions_v1={"showcase-woche":{"mode":"any", "planned":"this_week", "effort":"at_least",
                                                    "minutes":30}},
        saved_view_layouts_v1={"showcase-woche":{"display":"table", "group":"eisenhower", "sort":"due",
                                                 "columns":["title", "source", "due", "planned_date",
                                                            "estimated_minutes", "importance"]}},
        # Realistischer Tag (D57/WA-12): Kapazität je Wochentag und Tagesziel.
        daily_capacity_by_weekday=[300, 360, 300, 240, 150, 120, None], daily_goal=4,
        completion_history={tag(-1): 1, tag(0): 3},
        # Reiter (bis zwölf) und ein eigener KI-Auftrag für den Dateiaustausch (FP-06).
        open_tabs=[{"list_id":main["id"], "item_id":specification["id"], "used":1},
                   {"list_id":main["id"], "item_id":design["id"], "used":2}],
        exchange_recipes=[{"id":"showcase-rueckmeldung", "title":"Ausschnitt prüfenen zu Aufgaben bündeln",
                           "mode":"patch", "instruction":"Fasse die Ausschnitt prüfenen in den Beschreibungen "
                           "der ausgewählten Aufgaben knapp zusammen und schlage höchstens eine "
                           "Checkliste je Aufgabe vor. Ändere keine Termine."}],
        active_tab={folder_scope:"board", list_scope:"list"},
        pinboards={folder_scope:{"cards":board_cards, "layout":"free", "background":"dots", "width":260,
            "areas":[{"id":"showcase-inhalt", "name":"Rundgang vorbereiten", "color":"accent", "x":8,"y":16,"w":940,"h":940}],
            "connections":[{"from":specification["id"],"to":design["id"],"label":"Weg vor Druck","dash":True},
                           {"from":design["id"],"to":release["id"],"label":"danach ankündigen"}],
            "show_description":True, "show_checklist":True, "color_mode":"header"},
            list_scope:{"cards":board_cards[:-1], "layout":"columns", "group_by":"planned", "background":"grid",
                        "show_checklist":True, "color_mode":"stripe"},
            mod.ItemWorkspace.GLOBAL_SCOPE:{
                "cards": [
                    {"list_id":briefing["id"], "item_id":"page:"+briefing["id"], "x":34, "y":63, "scale":"normal"},
                    {"list_id":note["id"], "item_id":"page:"+note["id"], "x":34, "y":355, "scale":"normal"},
                    {"list_id":main["id"], "item_id":specification["id"], "x":390, "y":64, "scale":"normal"},
                    {"list_id":main["id"], "item_id":images["id"], "x":735, "y":58, "scale":"normal"},
                    {"list_id":drawing["id"], "item_id":"page:"+drawing["id"], "x":735, "y":470, "scale":"small"},
                ],
                "layout":"free", "width":238, "background":"dots", "show_checklist":True,
                "connections":[
                    {"from":"page:"+briefing["id"], "to":specification["id"], "label":"Weg ablaufen"},
                    {"from":"page:"+note["id"], "to":specification["id"], "label":"Rückfragen klären"},
                    {"from":specification["id"], "to":images["id"], "label":"Eingang zeigen"},
                    {"from":images["id"], "to":"page:"+drawing["id"], "label":"Pfeil abstimmen"},
                ]}})
    app.settings = app.normalize_personal_settings(settings)
    app.save_settings()
    app.save_templates()
    app.set_active_list(briefing["id"])
    app.sync_all_item_kind_labels()
    app.save_items()
    payload = app.partial_backup_payload([drawing["id"]], [project["id"], library["id"], journal["id"]])
    payload["pinboards"] = {scope:board for scope, board in app.exportable_pinboards().items()
                           if scope != mod.ItemWorkspace.GLOBAL_SCOPE}
    return payload, [meeting_template, routine_template]


def export(target, anchor):
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="glide-showcase-erzeugen-") as directory:
        mod = load_module(Path(directory)/"Glide")
        root = mod.tk.Tk()
        root.geometry("1440x960+20+30")
        errors = []
        root.report_callback_exception = lambda *args: errors.append(str(args[1]))
        app = mod.ListApp(root)
        app.show_info = lambda *a, **k: None
        app.show_warning = app.show_error = lambda *a, **k: errors.append(str(a))
        try:
            ruhe(root)
            payload, templates = build(app, mod, root, anchor)
            paths = [target/"Glide-Showcase.glidebackup", target/"Glide-Showcase_App.glideapp",
                     target/"Glide-Showcase.glidetemplates"]
            app.write_complete_backup(str(paths[0]), payload)
            app.write_complete_backup(str(paths[1]), app.app_backup_payload())
            app.write_json_atomic(str(paths[2]), {"format_version":app.TEMPLATE_FORMAT_VERSION,"templates":templates})
            # Zeilenenden wie im Repository (LF): Unter Windows schreibt die App
            # CRLF, und die Prüfsumme im Manifest passte nach dem Einchecken nicht.
            paths[2].write_bytes(paths[2].read_bytes().replace(b"\r\n", b"\n"))
            app.open_global_board()
            ruhe(root)
            canvas = target / "Werkhaus-West.canvas"
            assert app.export_board_json_canvas(str(canvas)) == str(canvas)
            canvas.write_bytes(canvas.read_bytes().replace(b"\r\n", b"\n"))
            paths.append(canvas)
            ruhe(root)
            assert not errors, errors
            manifest = {"app_version":mod.APP_VERSION,"format_version":app.DATA_SCHEMA_VERSION,
                "thema":"Werkhaus West", "bearbeitungstag":anchor.isoformat(), "dokumente":[{"titel":e["title"],"art":e["list_kind"]} for e in payload["lists"]],
                "bilder":len(PHOTOS), "seitenbilder":sum(len((e.get("rich_note") or {}).get("images") or {}) for e in payload["lists"]),
                "projektpinnwaende":len(payload["pinboards"]), "vorlagen":len(templates),
                "dateien":{p.name:{"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}}
            (target/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",
                                                newline="\n")
            print(json.dumps(manifest,ensure_ascii=False,indent=2))
        finally:
            root.destroy()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ziel", type=Path, default=TARGET)
    parser.add_argument("--tag", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    export(args.ziel.expanduser().resolve(), args.tag)


if __name__ == "__main__":
    main()
