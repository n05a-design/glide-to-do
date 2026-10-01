#!/usr/bin/env python3
"""Erzeugt den aktiven Showcase mit echten App-APIs in einem temporären Bestand.

Originalbilder: tests/fixtures/showcase/bilder (unveränderte Inhaberdateien).
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

from rundgang import load_module, ruhe, zeichnung

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "tests/fixtures/showcase/bilder"
TARGET = ROOT / "tests/fixtures/showcase"
PHOTOS = [
    ("Haus-in-weiß-1114004174.jpeg", "Architektur · Referenz", "Modellmotiv für das Briefing; kein reales Verkaufsobjekt."),
    ("Haus-in-gelb-666269411.jpeg", "Farbwelt · Akzent", "Warmer Akzent für die Kampagnenentwicklung."),
    ("Architektin-171340787.jpeg", "Planung · Menschen", "Symbolmotiv für die Abstimmung; keine Projektbeteiligte."),
    ("Helm-auf-Zeichnung-23388604.jpeg", "Planung · Detail", "Unterlagen und Bauplanung als Bildthema."),
    ("Haus-auf-Statistik-1172003382.jpeg", "Markt · Auswertung", "Symbolmotiv; die abgebildeten Zahlen sind keine Projektdaten."),
    ("Tipps-in-der-Einrichtung-02.png", "Wohnen · Atmosphäre", "Einrichtungsmotiv für die Bildsprache."),
]

BRIEFING = """# Parkquartier · Projektbriefing

Ein fiktives Vermarktungsprojekt für vier Stadthäuser. Atelier Nord entwickelt Exposé, Landingpage und eine kleine Bildstrecke. Ziel dieser Arbeitsseite ist ein klarer, freigegebener Stand für Gestaltung und Vertrieb.

## Architektur und Zielgruppe

ARCHITEKTUR: Die helle Modellansicht steht für eine ruhige, verständliche Darstellung. Sie ist ein Referenzmotiv aus der Beispielablage und zeigt kein reales Verkaufsobjekt.

Gesucht wird ein Zuhause mit Platz für Familie und konzentriertes Arbeiten. Die Seite führt zuerst zum Wohngefühl, dann zur Ausstattung und schließlich zum Kontakt. Flächen, Preise und Energieangaben bleiben Platzhalter, bis der Vertrieb belastbare Angaben liefert.

## Bildsprache

WOHNGEFÜHL: Warmes Licht, ein gezielter Farbakzent und großzügige Details machen die Motive zugänglich. Die Galerie enthält sechs Originalbilder mit eigenständigen Bildunterschriften.

PLANUNG: Menschen und Planungsdetails ergänzen die Architektur. Die Motive illustrieren Themen; sie werden nicht als Fotos des fiktiven Objekts ausgegeben.

## Lieferumfang und Abnahme

- Exposé: Titel, Objektübersicht, Grundrissplatzhalter und Kontakt
- Landingpage: Einstieg, Ausstattung, Bilder, FAQ und Kontaktformular
- Übergabe: freigegebene Dateien, Bildzuordnung und Pflegehinweise

1. Entwurf gemeinsam prüfen
2. Rückmeldungen in der Aufgabenliste bündeln
3. Freigabe im Protokoll dokumentieren

- [x] Ziel und Lieferumfang abgestimmt
- [ ] Bildauswahl mit dem Vertrieb freigeben
- [ ] Exposé und Landingpage gegen das Briefing prüfen

> Freigabe bedeutet: Inhalt, Gestaltung und Verantwortliche sind dokumentiert. Eine Zeichnung, eine Liste und eine Notiz behalten dabei ihren eigenen Zweck.

## Technische Übergabe

```text
Projekt: Parkquartier / PQ-04
Stand: Entwurf 02
Nächster Schritt: konsolidierte Rückmeldung
```

[Projektkennung und Dateien](https://example.invalid/parkquartier)

## Entscheidungen und Hintergrund

Details der Bildauswahl
Die weiße Architekturansicht bleibt das Leitmotiv.
Der gelbe Akzent erscheint sparsam in der Bildstrecke.
Einrichtung und Planung ergänzen den sachlichen Einstieg.

## Arbeitsstand

Die verknüpften Aufgaben in „Vermarktung · Umsetzung“ tragen Bearbeitungstag, Aufwand und Fälligkeit getrennt. Abhängigkeiten markieren die Freigabe vor der Veröffentlichung. Die Projektpinnwand ordnet Karten, verbindet Entscheidungen und zeigt die Zeichnung als Verweis.
"""

MEETING = """# Abstimmung · Entwurf 02

**Teilnehmende:** Mara (Gestaltung), Jonas (Vertrieb), Lea (Projektkoordination). Alle Namen und Projektdaten sind fiktiv.

## Beschlossen

- Ruhiger Architektureinstieg, danach Wohngefühl und Ausstattung
- Eine gemeinsame Rückmeldung statt mehrerer widersprüchlicher Dateien
- Kontaktformular mit klarer Bestätigung nach dem Absenden

## Offene Rückmeldung

Die Liste der Ausstattungsmerkmale benötigt noch eine bestätigte Quelle. Jonas liefert den freigegebenen Steckbrief. Lea prüft anschließend Exposé und Website gemeinsam.

> „Erst den Inhalt bestätigen, dann den freigegebenen Stand gestalten.“

## Nächste Schritte

1. Bildauswahl im Briefing vergleichen
2. Rückfragen in der Aufgabenliste klären
3. Freigabe mit Datum und Stand dokumentieren

## Pflegehinweis

Aufgaben stehen bei einer Notiz oberhalb des freien Textes. Einzelne Aufgaben bleiben echte Punkte; diese Notiz wird dadurch keine Seite.
"""


def build(app, mod, root, anchor):
    """Zusammenhängende Dokumente; zurückgegeben wird die portable Projektwahl."""
    tag = lambda offset: (anchor + timedelta(days=offset)).isoformat()
    app.flush_rich_note()
    app.lists = [entry for entry in app.lists if entry.get("system_role") == "inbox"]
    app.folders = []
    labels = {}
    for name, color in (("Parkquartier", "accent"), ("Gestaltung", "clear"), ("Freigabe", "flag"),
                        ("Vertrieb", "export"), ("Warten", "due_action")):
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
    model = mod.glide_drawing.DrawingModel.from_document(zeichnung(mod))
    generated = {
        "Quartier-Skizze.png": model.to_png(scale=8),
        "Quartier-Symbol.ico": icon.to_ico(),
        "Parkquartier-Palette.gpl": mod.glide_drawing.palette_to_gpl("Parkquartier", ["#1C6A77", "#E8AD43", "#CFE8F7"]).encode(),
        "Parkquartier-Palette.hex": mod.glide_drawing.palette_to_hex(["#1C6A77", "#E8AD43", "#CFE8F7"]).encode(),
        "Objektsteckbrief.csv": "Objektkennung;Projekt;Status\nPQ-04;Parkquartier;Fiktiver Entwurf\n".encode(),
        "Uebergabe.txt": "Parkquartier · Entwurf 02\nExposé, Landingpage und Bildzuordnung gemeinsam prüfen.\nAlle Projektangaben sind fiktiv.\n".encode(),
    }
    generated_attachments = []
    for name, content in generated.items():
        path = attachments_dir / name
        path.write_bytes(content)
        generated_attachments.append(app.store_attachment(str(path)))
    project = app.new_folder_object("Showcase · Parkquartier", color="accent", icon=icon_doc,
                                    note="Fiktives Arbeitsprojekt: Briefing, Umsetzung, Bilder und Rückblick.")
    library = app.new_folder_object("Wissen und Bildmaterial", parent_id=None, folder_kind="library")
    journal = app.new_folder_object("Projekttagebuch", parent_id=None, folder_kind="journal")
    archive = app.new_folder_object("Abgeschlossene Vorbereitung", parent_id=project["id"], archived=True,
                                    archived_at=tag(-7)+"T16:00:00+02:00")
    app.folders.extend([project, library, journal, archive])
    stored = {name: app.store_attachment(str(ASSETS / name)) for name, _title, _note in PHOTOS}
    assert all(stored.values()), "Ein Beispielbild konnte nicht eingelesen werden."
    # Ein Anhang am Ordner bleibt beim Projektimport und bei der Vorlage erhalten.
    project["attachments"] = [copy.deepcopy(stored[PHOTOS[3][0]])]
    def task(text, **kwargs):
        return app.new_item(text, **kwargs)
    specification = task("Objektsteckbrief bestätigen", due=tag(0), due_time="11:00", importance=3,
        planned_date=tag(0), planned_time="09:00", estimated_minutes=45, time_spent_minutes=20,
        labels=[labels["Vertrieb"], labels["Freigabe"]],
        description="Jonas bestätigt Ausstattungsmerkmale und die Quelle jeder Objektangabe.",
        attachments=[copy.deepcopy(stored[PHOTOS[3][0]])],
        checklist=[{"text":"Objektkennung PQ-04", "done":True}, {"text":"Ausstattung bestätigt"}, {"text":"Quellen dokumentiert"}])
    images = task("Bildauswahl freigeben", due=tag(1), planned_date=tag(0), planned_time="10:30",
        estimated_minutes=30, importance=2, labels=[labels["Gestaltung"], labels["Freigabe"]],
        attachments=[copy.deepcopy(stored[PHOTOS[0][0]]), copy.deepcopy(stored[PHOTOS[5][0]])],
        description="Leitmotiv Architektur und ergänzende Wohnatmosphäre nebeneinander prüfen.")
    design = task("Landingpage · Entwurf 02 ausarbeiten", kind=app.ITEM_KIND_LONG, due=tag(2),
        planned_date=tag(1), estimated_minutes=120, importance=2, labels=[labels["Gestaltung"]],
        description="Hero, Ausstattungsabschnitt und Kontaktbereich gemeinsam aufbauen.\nAbnahme: klare Reihenfolge, lesbare Bildunterschriften und erreichbarer Kontakt.",
        links=[images["id"]], blocked_by=[specification["id"]], color="clear",
        checklist=[{"text":"Hero und Einstieg", "done":True}, {"text":"Kontaktbestätigung"}, {"text":"Tastatur und Fokus prüfen"}])
    release = task("Freigabestand an den Vertrieb übergeben", due=tag(4), importance=3,
        labels=[labels["Freigabe"]], blocked_by=[design["id"]], links=[specification["id"]],
        attachments=[copy.deepcopy(generated_attachments[-1])],
        reminder={"mode":"fixed", "at":app.local_reminder_time(tag(4), "10:00")},
        description="Exposé, Website und Bildzuordnung als einen dokumentierten Stand übergeben.")
    completed = task("Ziel und Lieferumfang abstimmen", done=True, done_at=tag(-1)+"T14:30:00+02:00",
                     planned_date=tag(-1), estimated_minutes=60, time_spent_minutes=55)
    missing = task("Rückfrage zur Ausstattung nachhalten", due=tag(-1), importance=1,
                   labels=[labels["Warten"]], description="Eine bewusst überfällige Aufgabe für den Arbeitsüberblick.")
    checklist = task("Vertriebsübergabe vorbereiten", kind=app.ITEM_KIND_GROUP, children=[
        task("Dateinamen und Versionsstand prüfen", due=tag(3), estimated_minutes=15),
        task("Pflegehinweise ergänzen", due=tag(3), estimated_minutes=30),
        task("Ansprechpersonen dokumentieren", done=True, done_at=tag(0)+"T08:30:00+02:00")])
    main = app.new_list_object("Vermarktung · Umsetzung", [
        task("Entwurf und Freigabe", kind=app.ITEM_KIND_HEADING), completed, specification, images, design,
        missing, task("Übergabe", kind=app.ITEM_KIND_HEADING), checklist, release], folder_id=project["id"],
        labels=[labels["Parkquartier"]], icon=icon_doc, color="accent", attachments=generated_attachments[2:],
        note="Ein aktiver Projektstand mit abgeschlossenen und offenen Arbeitspaketen.")
    note = app.new_list_object("Abstimmung · Entwurf 02", [task("Steckbrief von Jonas einholen", due=tag(0)),
        task("Gemeinsame Rückmeldung bündeln", planned_date=tag(1), estimated_minutes=30)],
        folder_id=project["id"], list_kind="note", rich_note=mod.glide_page_markdown.markdown_to_page(MEETING),
        labels=[labels["Parkquartier"]], attachments=[copy.deepcopy(stored[PHOTOS[2][0]])])
    gallery = app.new_list_object("Bildwelt · Auswahl mit Kommentaren", [], folder_id=project["id"],
        list_kind="gallery", attachments=[copy.deepcopy(stored[name]) for name, _, _ in PHOTOS],
        note="Sechs Motive aus der Beispielablage: Originale, Bildunterschriften und Kontext.")
    drawing = app.new_list_object("Quartier · Pixelskizze", [], folder_id=None, list_kind="drawing",
        drawing=zeichnung(mod), icon=icon_doc, attachments=generated_attachments[:2],
        drawing_reference={"attachment_id":generated_attachments[0]["id"], "mode":"fit", "zoom_percent":100},
        note="Bearbeitbare 32 × 32 Zeichnung mit passendem 16 × 16 Symbol, PNG-Referenz und ICO-Export.")
    app.lists.extend([main, note, gallery, drawing])
    for name, title, caption in PHOTOS:
        app.set_gallery_caption(gallery["id"], stored[name]["id"], title, caption)
    routines = app.new_list_object("Wochenstart · Wiederkehrende Checkliste", [task("Eingang sichten"),
        task("Wochenergebnisse priorisieren", done=True), task("Kapazität und Rückfragen einplanen")],
        folder_id=project["id"], recurring_checklist=True, color="due_action")
    repeats = []
    for title, rule, offset in [
        ("Eingang kurz sichten", {"art":"taeglich"}, 0),
        ("Projektstatus besprechen", {"art":"woechentlich"}, 1),
        ("Bildmaterial nachhalten", {"art":"tage", "abstand":14}, 2),
        ("Redaktionsplan aktualisieren", {"art":"wochentage", "tage":[0,4]}, 3),
        ("Ablage und Sicherungen prüfen", {"art":"monatlich"}, 5),
        ("Jahresrückblick vorbereiten", {"art":"jaehrlich"}, 7)]:
        repeats.append(task(title, due=tag(offset), repeat=rule, reminder={"mode":"relative", "minutes":30},
                            due_time="09:00", estimated_minutes=15))
    rhythm = app.new_list_object("Wiedervorlagen · Projektrhythmus", repeats, folder_id=project["id"],
                                 note="Alle sechs Wiederholungsarten; Systembenachrichtigungen sind im Showcase ausgeschaltet.")
    app.lists.extend([routines, rhythm])
    inbox = next(entry for entry in app.lists if entry.get("system_role") == "inbox")
    inbox["items"] = [task("Neue Bildidee für die nächste Abstimmung sichten", labels=[labels["Gestaltung"]]),
                       task("Rückfrage aus dem Vertrieb einordnen", description="Noch ohne Termin: erst klären, dann einplanen.")]
    for offset, mood, title, text in [
        (-1, "grateful", "Rückblick · Briefing freigegeben", "Das Briefing ist klar. Ein gemeinsamer Rückmeldestand spart Abstimmungsaufwand.\n\nMorgen: Bildauswahl bestätigen und den Kontaktbereich ausarbeiten."),
        (0, "thoughtful", "Tagesnotiz · Gestaltung und Freigabe", "Heute stehen Steckbrief und Bildauswahl im Mittelpunkt.\n\n**Fortschritt:** Hero-Struktur ist vorbereitet.\n\n**Offen:** Ausstattung braucht die bestätigte Quelle.\n\n**Lernpunkt:** Abhängigkeiten vor dem Entwurf sichtbar machen.")]:
        app.lists.append(app.new_list_object(title, [], folder_id=journal["id"], list_kind="note",
            rich_note=mod.glide_page_markdown.markdown_to_page("# "+title+"\n\n"+text),
            journal={"moment_date":tag(offset), "mood":mood, "favorite":offset==-1,
                     "location":"Atelier Nord", "prompt":"Was möchte ich von heute bewahren?"}))
    app.lists.append(app.new_list_object("Vorbereitung · abgeschlossen", [task("Briefing einsammeln", done=True,
        done_at=tag(-7)+"T12:00:00+02:00"), task("Lieferumfang bestätigen", done=True,
        done_at=tag(-7)+"T15:00:00+02:00")], folder_id=archive["id"], archived=True,
        archived_at=tag(-7)+"T16:00:00+02:00"))
    app.save_items()
    briefing = app.new_page_from_markdown(BRIEFING, title="Parkquartier · Briefing und Freigabe", folder_id=library["id"])
    ruhe(root)
    app.set_active_list(briefing["id"])
    ruhe(root)
    editor = app.rich_note_editor
    # Richtige Editor-Anker verwenden; Bilder gehören als Anhänge zur Seite.
    for prefix, filename, mode, width in reversed([
        ("ARCHITEKTUR:", PHOTOS[0][0], "center", 620),
        ("WOHNGEFÜHL:", PHOTOS[5][0], "left", 250),
        ("PLANUNG:", PHOTOS[2][0], "right", 300)]):
        lines = editor.text.get("1.0", "end-1c").splitlines()
        index = f"{next(i for i, line in enumerate(lines, 1) if line.startswith(prefix))}.0"
        key = editor.insert_images([str(ASSETS/filename)], index)[0]
        editor.images[key].update(mode=mode, width=width)
    # Klappblock mit echten semantischen Tags, keine gemalte Attrappe.
    lines = editor.text.get("1.0", "end-1c").splitlines()
    line = next(i for i, text in enumerate(lines, 1) if text.startswith("Details der Bildauswahl"))
    editor.text.delete(f"{line}.0", f"{line}.end")
    editor.text.insert(f"{line}.0", "Details der Bildauswahl\nDie weiße Architekturansicht bleibt das Leitmotiv.\n"
                       "Der gelbe Akzent erscheint sparsam in der Bildstrecke.\n"
                       "Einrichtung und Planung ergänzen den sachlichen Einstieg.")
    editor.text.mark_set("insert", f"{line}.0")
    editor.convert_block("toggle")
    for number in range(line+1, line+4):
        editor.text.tag_add("indent1", f"{number}.0", f"{number}.end")
    editor.set_toggle_open(f"{line}.0", False)
    editor.flush()
    ruhe(root)
    # Zwei kleine, portable Vorlagen ergänzen den vorhandenen Katalog.
    meeting_template = app.capture_template(list_id=note["id"])
    meeting_template = next(t for t in app.templates if t["id"] == meeting_template["id"])
    meeting_template["title"] = "{{Wochentag}} KW {{KW}} · {{Projekt}}"
    meeting_template["note"] = "Datumsfelder füllen sich selbst; Projekt wird abgefragt. Aufgaben und Anhang bleiben enthalten."
    routine_template = app.capture_template(list_id=routines["id"])
    routine_template = next(t for t in app.templates if t["id"] == routine_template["id"])
    routine_template["title"] = "Showcase · Wochenstart"
    meeting_template = next(t for t in app.templates if t["id"] == meeting_template["id"])
    settings = copy.deepcopy(app.settings)
    board_cards = [{"list_id":main["id"], "item_id":item["id"], "x":x, "y":y, "scale":"normal"}
        for item, x, y in [(specification,24,60), (images,320,60), (design,320,500), (release,640,60)]]
    board_cards.append({"list_id":drawing["id"], "item_id":mod.ItemWorkspace.PAGE_CARD_PREFIX+drawing["id"],
                        "x":24, "y":500, "scale":"small"})
    folder_scope = "folder:"+project["id"]
    list_scope = "list:"+main["id"]
    settings.update(profile_name="Atelier Nord · Showcase", start_on_home=True, show_home_stats=True,
        sidebar_sections_visible={"pages":True,"lists":True,"notes":True,"drawings":True},
        sidebar_locations={},
        mascot_name="Gismo", mascot_playful=False, system_notifications=False,
        pinned_pages=[{"kind":"list", "id":briefing["id"]}, {"kind":"folder", "id":library["id"]}],
        recent_lists=[{"id":entry["id"], "edited_at":tag(0)+"T10:00:00+02:00"} for entry in [briefing,note,drawing]],
        page_favorites=[briefing["id"]], gallery_tile_size={gallery["id"]:"medium"},
        list_group_by={main["id"]:"importance"},
        saved_filters=[{"id":"showcase-freigabe", "name":"Parkquartier · Freigabe", "query":"",
                        "label_ids":[labels["Freigabe"]], "list_ids":[main["id"]], "status":"open"}],
        active_tab={folder_scope:"board", list_scope:"board"},
        pinboards={folder_scope:{"cards":board_cards, "layout":"free", "background":"dots", "width":260,
            "areas":[{"id":"showcase-inhalt", "name":"Inhalt und Freigabe", "color":"accent", "x":8,"y":16,"w":940,"h":940}],
            "connections":[{"from":specification["id"],"to":design["id"],"label":"Inhalt vor Gestaltung","dash":True},
                           {"from":design["id"],"to":release["id"],"label":"prüfen und übergeben"}],
            "show_description":True, "show_checklist":True, "color_mode":"header"},
            list_scope:{"cards":board_cards[:-1], "layout":"columns", "group_by":"planned", "background":"grid",
                        "show_checklist":True, "color_mode":"stripe"},
            mod.ItemWorkspace.GLOBAL_SCOPE:{"cards":board_cards[:2], "layout":"grid", "width":260}})
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
            ruhe(root)
            assert not errors, errors
            manifest = {"app_version":mod.APP_VERSION,"format_version":app.DATA_SCHEMA_VERSION,
                "bearbeitungstag":anchor.isoformat(), "dokumente":[{"titel":e["title"],"art":e["list_kind"]} for e in payload["lists"]],
                "bilder":len(PHOTOS), "seitenbilder":sum(len((e.get("rich_note") or {}).get("images") or {}) for e in payload["lists"]),
                "projektpinnwaende":len(payload["pinboards"]), "vorlagen":len(templates),
                "dateien":{p.name:{"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}}
            (target/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
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
