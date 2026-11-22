# SPDX-License-Identifier: MPL-2.0
"""T335 · D93 Etappe 2: vollständige DE/EN-Oberfläche, geprüft in echtem Tk.

Jeder Fall schaltet auf Englisch, öffnet echte Dialoge, Menüs und Ansichten
mit künstlichen Daten und sammelt alle sichtbaren Texte. Geprüft wird, dass
erwartete englische Texte erscheinen und kein deutscher Oberflächentext
übrig bleibt; danach dieselben Wege auf Deutsch als Gegenprobe. Benutzerdaten
(Titel, Notizen) und Datumsangaben sind keine Oberflächentexte und werden
aus künstlichen, sprachneutralen Werten gebildet. Eine menschliche Sprach-
und Sichtabnahme ersetzt der Test nicht.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import traceback
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tests/integration"))
from test_uiux_paket import Lauf  # noqa: E402

DEUTSCH = re.compile(
    r"[äöüÄÖÜß]|\b(und|oder|nicht|keine?|Aufgaben?|Listen?|Seiten?|Ordner|Datei|Fehler|Zeichnung|wählen|"
    r"Abbrechen|Speichern|Schließen|Weiter|Zurück|Ansicht|Bitte|Neue?r?|Heute|Morgen|Woche|Tag|Tage|"
    r"Hinweise?|Kalender|Termine?|Uhrzeit|Einstellungen|Erledigt|Offen|Bearbeiten|Öffnen|Übernehmen)\b")


# Null deutsche Reste verlangt T335 ab Paket L8, wenn auch Klassentabellen und Module übersetzt sind;
# davor prüfen die Fälle die erwarteten englischen Texte ihres Pakets.
STRENG = True


def deutsche_reste(texte):
    return sorted({text for text in texte if text and DEUTSCH.search(text)})


def widget_texte(widget, mod):
    """Sichtbare Texte eines Fensters: Beschriftungen, Knöpfe, Textfelder und Canvas-Texte."""
    gefunden = []
    try:
        if widget.winfo_class() == "Toplevel":
            gefunden.append(widget.title())
    except mod.tk.TclError:
        pass
    for kind in widget.winfo_children():
        text = getattr(kind, "text", None)
        if isinstance(text, str):
            gefunden.append(text)
        try:
            klasse = kind.winfo_class()
            if klasse in ("Label", "Button", "Checkbutton", "Radiobutton", "TLabel", "TButton", "TCheckbutton",
                          "TRadiobutton", "Labelframe", "TLabelframe"):
                gefunden.append(str(kind.cget("text")))
            elif klasse == "Text":
                gefunden.append(kind.get("1.0", "end-1c"))
            elif klasse == "Canvas":
                for item in kind.find_all():
                    if kind.type(item) == "text":
                        gefunden.append(str(kind.itemcget(item, "text")))
            elif klasse == "Treeview":
                for spalte in ("#0",) + tuple(kind.cget("columns") or ()):
                    gefunden.append(str(kind.heading(spalte, "text")))
        except mod.tk.TclError:
            pass
        gefunden.extend(widget_texte(kind, mod))
    return [text for text in gefunden if text and text.strip()]


def modal_texte(lauf, aktion):
    """Führt `aktion` aus und sammelt die Texte jedes modal geöffneten Dialogs, statt auf ihn zu warten."""
    app, mod = lauf.app, lauf.mod
    gesehen = []

    def erfassen(dialog, *args, **kwargs):
        lauf.idle(2)
        gesehen.append(widget_texte(dialog, mod))
        dialog.destroy()

    with patch.object(app, "run_modal", side_effect=erfassen):
        aktion()
    lauf.idle(2)
    assert gesehen, "kein modaler Dialog geöffnet"
    return [text for texte in gesehen for text in texte]


def menue_texte(menu):
    """Beschriftungen eines Menüs einschließlich aller Untermenüs."""
    texte = []
    ende = menu.index("end")
    for index in range(0 if ende is None else ende + 1):
        art = menu.type(index)
        if art in ("command", "cascade", "checkbutton", "radiobutton"):
            texte.append(str(menu.entrycget(index, "label")))
        if art == "cascade":
            name = str(menu.entrycget(index, "menu"))
            if name:
                texte.extend(menue_texte(menu.nametowidget(name)))
    return texte


def beide_sprachen(lauf, pruefung):
    """Englisch ohne deutsche Reste, dann Deutsch als Gegenprobe."""
    i18n = lauf.mod.glide_i18n
    vorher = i18n.get_language()
    try:
        i18n.set_language("en")
        englisch = pruefung("en")
        reste = deutsche_reste(englisch)
        assert not STRENG or not reste, f"deutsche Reste auf Englisch: {reste}"
        i18n.set_language("de")
        deutsch = pruefung("de")
        assert deutsche_reste(deutsch), "Gegenprobe: deutsche Fassung zeigt keinen deutschen Text"
    finally:
        i18n.set_language(vorher)
    return len(englisch), len(deutsch)


def fall_l1_tageshinweise(lauf):
    """L1: Tageshinweise und ihre Einstellungen, Speicherstatus-Knöpfe und Mondphasen.

    Seit Paket L8 zählt auch der Berichtstext aus `storage_health`.
    """
    app, mod = lauf.app, lauf.mod

    def pruefung(sprache):
        texte = modal_texte(lauf, app.show_daily_hint_settings)
        texte += modal_texte(lauf, app.show_daily_hints)
        texte += modal_texte(lauf, app.show_storage_status)
        texte += [mod.moon_phase_info(mod.date(2026, 11, 21))["name"]]
        erwartet = {"en": {"Set up daily hints", "Daily hints", "Storage status", "Cancel", "Save", "Close"},
                    "de": {"Tageshinweise einstellen", "Tageshinweise", "Speicherstatus", "Abbrechen", "Speichern",
                           "Schließen"}}
        fehlt = erwartet[sprache] - set(texte)
        assert not fehlt, f"{sprache}: fehlt {sorted(fehlt)}"
        return texte

    en, de = beide_sprachen(lauf, pruefung)
    return f"Tageshinweise, Einstellungen, Speicherstatus und Mondphase: {en} englische, {de} deutsche Texte"


def fall_l2_tag_und_start(lauf):
    """L2: Tag entlasten mit eingeplanten Aufgaben und Startseite einrichten."""
    app, mod = lauf.app, lauf.mod
    heute = mod.date.today().isoformat()
    for titel in ("Alpha 1", "Alpha 2"):
        item = app.new_item(titel)
        item["planned_date"] = heute
        item["estimated_minutes"] = 30
        app.items.append(item)
    assert app.save_items()
    lauf.idle(2)

    def pruefung(sprache):
        texte = modal_texte(lauf, lambda: app.show_day_relief(days=[mod.date.today().isoformat()]))
        texte += modal_texte(lauf, app.show_home_tiles_dialog)
        erwartet = {"en": {"Lighten the day", "Reschedule", "Cancel", "Set up home", "Save", "Restore default"},
                    "de": {"Tag entlasten", "Umplanen", "Abbrechen", "Startseite einrichten", "Speichern",
                           "Standard wiederherstellen"}}
        fehlt = erwartet[sprache] - set(texte)
        assert not fehlt, f"{sprache}: fehlt {sorted(fehlt)}"
        return [text for text in texte if not text.startswith("Alpha")]

    en, de = beide_sprachen(lauf, pruefung)
    return f"Tag entlasten und Startseite einrichten: {en} englische, {de} deutsche Texte"


def fall_l3_punkte_und_labels(lauf):
    """L3: Punktmaske, Labelmanager und Tabellenspalten als echte Dialoge."""
    app = lauf.app
    item = app.new_item("Beta 1")
    app.items.append(item)
    assert app.save_items()
    lauf.idle(2)

    def pruefung(sprache):
        texte = modal_texte(lauf, lambda: app.item_form_dialog(mode="create"))
        texte += modal_texte(lauf, app.open_label_manager)
        texte += modal_texte(lauf, app.show_table_columns_dialog)
        erwartet = {"en": {"New item", "Title", "Importance", "Due date", "Repeat", "Rename",
                           "Table columns", "Reset view"},
                    "de": {"Neuer Punkt", "Titel", "Wichtigkeit", "Fälligkeit", "Wiederholung",
                           "Umbenennen", "Tabellenspalten", "Ansicht zurücksetzen"}}
        fehlt = erwartet[sprache] - set(texte)
        assert not fehlt, f"{sprache}: fehlt {sorted(fehlt)}"
        # Die festen Systemlabels „Langtext“ und „Zwischenüberschrift“ sind gespeicherte Labelnamen (Daten).
        return [text for text in texte if not text.startswith("Beta") and text not in ("Langtext", "Zwischenüberschrift")]

    en, de = beide_sprachen(lauf, pruefung)
    return f"Punktmaske, Labelmanager und Tabellenspalten: {en} englische, {de} deutsche Texte"


def fall_l4_menues_und_anlegen(lauf):
    """L4: Kontextmenüs von Liste, Ordner und Systemansicht sowie der Anlegen-Dialog."""
    app = lauf.app
    liste = app.new_list_object("Gamma Liste", [])
    app.lists.append(liste)
    ordner = app.new_folder_object("Gamma Ordner") if hasattr(app, "new_folder_object") else None
    if ordner is not None:
        app.folders.append(ordner)
    assert app.save_items()
    lauf.idle(2)

    def pruefung(sprache):
        texte = menue_texte(app.build_list_menu(liste["id"]))
        if ordner is not None:
            texte += menue_texte(app.build_folder_menu(ordner["id"]))
        texte += menue_texte(app.build_smart_view_menu("in_progress"))
        texte += modal_texte(lauf, lambda: app.create_container_dialog("list"))
        erwartet = {"en": {"Rename", "Duplicate", "Export", "Move to trash", "Archive", "New list", "Create",
                           "Cancel", "Open calendar …"},
                    "de": {"Umbenennen", "Duplizieren", "Exportieren", "In den Papierkorb", "Archivieren",
                           "Neue Liste", "Anlegen", "Abbrechen", "Kalender öffnen …"}}
        fehlt = erwartet[sprache] - set(texte)
        assert not fehlt, f"{sprache}: fehlt {sorted(fehlt)}"
        return [text for text in texte if "Gamma" not in text]

    en, de = beide_sprachen(lauf, pruefung)
    return f"Listen-, Ordner- und Ansichtsmenü, Anlegen-Dialog: {en} englische, {de} deutsche Texte"


def fall_l5_erinnerungen_und_erfassung(lauf):
    """L5: Benachrichtigungen, Schnellerfassung und das Kontextmenü der leeren Liste."""
    app = lauf.app
    item = app.new_item("Delta 1")
    app.items.append(item)
    assert app.save_items()
    lauf.idle(2)

    def pruefung(sprache):
        texte = modal_texte(lauf, app.open_reminders)
        texte += modal_texte(lauf, app.show_quick_capture)
        texte += menue_texte(app.build_tree_background_menu())
        erwartet = {"en": {"Notifications", "Close", "Quick capture", "Capture", "Cancel", "Sort", "Alphabetical"},
                    "de": {"Benachrichtigungen", "Schließen", "Schnellerfassung", "Erfassen", "Abbrechen", "Sortieren",
                           "Alphabetisch"}}
        fehlt = erwartet[sprache] - set(texte)
        assert not fehlt, f"{sprache}: fehlt {sorted(fehlt)}"
        return [text for text in texte if "Delta" not in text]

    en, de = beide_sprachen(lauf, pruefung)
    return f"Benachrichtigungen, Schnellerfassung, Listenmenü: {en} englische, {de} deutsche Texte"


def fall_l6_drucken_und_sicherungen(lauf):
    """L6: Drucken und PDF, Sicherungsübersicht, Sicherungsvergleich und „Für KI bereitstellen“."""
    app = lauf.app
    item = app.new_item("Epsilon 1")
    app.items.append(item)
    assert app.save_items()
    lauf.idle(2)

    def pruefung(sprache):
        texte = modal_texte(lauf, app.show_print_dialog)
        texte += modal_texte(lauf, app.show_backup_catalog)
        texte += modal_texte(lauf, app.show_backup_compare_dialog)
        texte += modal_texte(lauf, app.show_exchange_export_dialog)
        erwartet = {"en": {"Print and PDF", "Open and print", "Backup overview", "Compare backups", "Older state",
                           "Provide for AI", "Purpose", "Scope"},
                    "de": {"Drucken und PDF", "Öffnen und drucken", "Sicherungsübersicht", "Sicherungen vergleichen",
                           "Älterer Stand", "Für KI bereitstellen", "Zweck", "Umfang"}}
        fehlt = erwartet[sprache] - set(texte)
        assert not fehlt, f"{sprache}: fehlt {sorted(fehlt)}"
        return [text for text in texte if "Epsilon" not in text and ".glide" not in text]

    en, de = beide_sprachen(lauf, pruefung)
    return f"Drucken, Sicherungen und KI-Austausch: {en} englische, {de} deutsche Texte"


def fall_l7_kalender_verlauf_kuerzel(lauf):
    """L7: Kalenderexport, Änderungsverlauf und Tastenkürzel als echte Dialoge."""
    app = lauf.app

    def pruefung(sprache):
        texte = modal_texte(lauf, app.show_calendar_export_dialog)
        texte += modal_texte(lauf, app.show_history_dialog)
        texte += modal_texte(lauf, app.show_shortcuts_dialog)
        erwartet = {"en": {"Calendar file (ICS)", "Save and open", "Change history", "Clear history",
                           "Keyboard shortcuts", "Keys / action", "Effect"},
                    "de": {"Kalenderdatei (ICS)", "Speichern und öffnen", "Änderungsverlauf", "Verlauf leeren",
                           "Tastenkürzel", "Tasten / Aktion", "Wirkung"}}
        fehlt = erwartet[sprache] - set(texte)
        assert not fehlt, f"{sprache}: fehlt {sorted(fehlt)}"
        return texte

    en, de = beide_sprachen(lauf, pruefung)
    return f"Kalenderexport, Änderungsverlauf und Tastenkürzel: {en} englische, {de} deutsche Texte"


def fall_l8_handbuch_und_bericht(lauf):
    """L8: eingebautes Handbuch, vollständiger Speicherstatus-Bericht und Klassentabellen der Pinnwand."""
    app = lauf.app

    def pruefung(sprache):
        texte = modal_texte(lauf, app.show_manual_dialog)
        texte += modal_texte(lauf, app.show_storage_status)
        texte += [name for _key, name in lauf.mod.tr_table(lauf.mod.ItemWorkspace.BOARD_LAYOUTS)]
        handbuch = {titel for titel, _eintraege in app.manual_sections()}
        erwartet = {"en": {"Manual", "Board", "Help", "Keyboard shortcuts", "Free layout"},
                    "de": {"Handbuch", "Pinnwand", "Hilfe", "Tastenkürzel", "Frei anordnen"}}
        fehlt = erwartet[sprache] - set(texte) - handbuch
        assert not fehlt, f"{sprache}: fehlt {sorted(fehlt)}"
        # Gewollt deutsch zitiert: Eingabewörter der Schnellerfassung und Vorlagenplatzhalter.
        zitiert = ("{{Datum}}", "German phrases")
        return [text for text in texte if not any(marke in text for marke in zitiert)] + sorted(handbuch)

    en, de = beide_sprachen(lauf, pruefung)
    return f"Handbuch, Speicherstatus und Pinnwand-Anordnungen: {en} englische, {de} deutsche Texte"


def fall_v178_austausch_und_vorlagen(lauf):
    """V1.78: mitgelieferte Vorlagen, Standardtitel, Eingang und TXT/CSV-Austausch in beiden Sprachen.

    Unveränderte mitgelieferte Vorlagen wechseln mit der Sprache, neue Objekte
    tragen Standardtitel der Sprache, und TXT/CSV-Exporte in einer Sprache
    lassen sich in beiden Sprachen wieder einlesen.
    """
    app, mod = lauf.app, lauf.mod
    csv_pfad = Path(tempfile.mkdtemp(prefix="glide-csv-")) / "export.csv"

    def austausch():
        punkt = app.new_item("Alpha")
        punkt.update(description="Zeile", due="2026-12-01", planned_date="2026-11-30", estimated_minutes=30)
        punkt["repeat"] = app.normalize_repeat({"art": app.REPEAT_WEEKDAYS, "tage": [0, 2]}, default_start="2026-12-01")
        zeilen = []

        class Datei:
            def write(self, text):
                zeilen.append(text)
        app.write_items_to_txt(Datei(), [punkt], [])
        txt = "".join(zeilen)
        with open(csv_pfad, "w", encoding="utf-8-sig", newline="") as datei:
            schreiber = mod.csv.writer(datei, delimiter=";")
            schreiber.writerow([mod.glide_i18n.t(f"csv.header.{key}", name) for key, name in app.CSV_EXPORT_HEADERS])
            app.write_items_to_csv(schreiber, [punkt], [])
        return punkt, txt

    def einlesen(punkt, txt):
        """Beide Sprachen lesen den Export: gleiche Felder wie vorher."""
        ergebnis = app.parse_txt_items(txt.splitlines(True))
        gelesen = (ergebnis[0] if isinstance(ergebnis, tuple) else ergebnis)[0]
        for feld in ("text", "description", "due", "planned_date", "estimated_minutes"):
            assert gelesen.get(feld) == punkt.get(feld), ("TXT", feld, gelesen.get(feld), punkt.get(feld))
        assert (gelesen.get("repeat") or {}).get("tage") == [0, 2], ("TXT", gelesen.get("repeat"))
        tabelle = app.read_csv_table(str(csv_pfad))
        zuordnung = app.csv_auto_mapping(tabelle)
        punkte, _bericht = app.csv_rows_to_items(tabelle, zuordnung, dry_run=True)
        for feld in ("text", "description", "due", "planned_date", "estimated_minutes"):
            assert punkte[0].get(feld) == punkt.get(feld), ("CSV", feld, punkte[0].get(feld), punkt.get(feld))

    exporte = {}

    def pruefung(sprache):
        app.templates = app.localize_builtin_templates(app.templates)
        vorlagen = {vorlage["id"]: vorlage for vorlage in app.templates}
        texte = [vorlagen[key][feld] for key in ("daily", "shopping", "folder-project", "construction", "journal-note")
                 for feld in ("title", "note")]
        texte += [titel for _key, titel, _markdown in app.page_template_entries()]
        texte += [app.journal_note_document(key)["text"] for key in ("journal-note", "journal-gratitude", "journal-weekly")]
        with patch.object(app, "confirm_template_preview", return_value=True):
            liste = app.create_list_from_template("daily")
        assert liste is not None, "Vorlage „daily“ nicht angelegt"
        texte += [liste["title"].rsplit(" ", 1)[0]] + [punkt["text"] for punkt in liste.get("items", [])]
        texte += [punkt.get("description", "") for punkt in liste.get("items", [])]
        texte += [mod.glide_i18n.t("ui.default_title.daily_note", "Tagesnotiz · {date}", date="01.12.2026"),
                  mod.glide_i18n.t("ui.default_title.new_list", "Neue Liste")]
        app.ensure_inbox_list()
        eingang = next(entry for entry in app.lists if app.is_inbox_list(entry))
        texte.append(eingang["title"])
        punkt, txt = austausch()
        exporte[sprache] = (punkt, txt, csv_pfad.read_text(encoding="utf-8-sig"))
        texte += [zeile for zeile in txt.splitlines() if zeile.strip() and "Alpha" not in zeile and "Zeile" not in zeile]
        texte += csv_pfad.read_text(encoding="utf-8-sig").splitlines()[:1]
        erwartet = {"en": {"Daily plan", "Shopping", "Project", "Inbox", "Report", "New list"},
                    "de": {"Tagesplanung", "Einkauf", "Projekt", "Eingang", "Bericht", "Neue Liste"}}
        fehlt = erwartet[sprache] - set(texte)
        assert not fehlt, (sprache, fehlt)
        return texte

    en, de = beide_sprachen(lauf, pruefung)
    i18n = mod.glide_i18n
    vorher = i18n.get_language()
    try:
        for leser in ("de", "en"):
            i18n.set_language(leser)
            for schreiber, (punkt, txt, csv_text) in exporte.items():
                csv_pfad.write_text(csv_text, encoding="utf-8-sig")
                einlesen(punkt, txt)
    finally:
        i18n.set_language(vorher)
    return (f"Vorlagen, Standardtitel, Eingang und TXT/CSV: {en} englische, {de} deutsche Texte; "
            "Export in beiden Sprachen in beiden Sprachen wieder eingelesen")


def fall_v179_startseite(lauf):
    """V1.79: Startseite mit Tageskachel, Kacheln und Knöpfen in beiden Sprachen.

    Die Kachel „Heute“ (home_task_tiles) und die Startseitenknöpfe waren bis
    V1.78 teils deutsch; geprüft wird das ganze Hauptfenster mit künstlichen,
    sprachneutralen Aufgaben.
    """
    app, mod = lauf.app, lauf.mod
    heute = mod.date.today().isoformat()
    liste = app.new_list_object("Alpha", [app.new_item("Beta", due=heute, planned_date=heute, estimated_minutes=30),
                                          app.new_item("Gamma", due=heute)])
    app.lists.append(liste)
    app.save_items()

    def pruefung(sprache):
        app.create_menubar()
        app._home_signature = None  # Sprachwechsel: Startseite neu aufbauen
        app.set_home_view()
        lauf.idle(6)
        # Nur die neu aufgebaute Startseite: Feste Leisten des Hauptfensters wechseln die
        # Sprache erst nach einem Neustart (Hinweis im Einstellungsdialog).
        texte = [text for text in widget_texte(app.home_content, mod) if text not in ("Alpha", "Beta", "Gamma")]
        erwartet = {"en": {"Previous day", "Next day", "Date"}, "de": {"Voriger Tag", "Nächster Tag", "Datum"}}
        fehlt = erwartet[sprache] - set(texte)
        assert not fehlt, (sprache, fehlt)
        return texte

    en, de = beide_sprachen(lauf, pruefung)
    return f"Startseite mit Tageskachel: {en} englische, {de} deutsche Texte"


FAELLE = ("l1_tageshinweise", "l2_tag_und_start", "l3_punkte_und_labels", "l4_menues_und_anlegen",
          "l5_erinnerungen_und_erfassung", "l6_drucken_und_sicherungen", "l7_kalender_verlauf_kuerzel",
          "l8_handbuch_und_bericht", "v178_austausch_und_vorlagen",
          "v179_startseite")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--fall", choices=FAELLE + ("alle",), default="alle")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = {"app_sha256": hashlib.sha256(args.app.read_bytes()).hexdigest(),
              "test_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "faelle": {}, "fehler": []}
    for name in (FAELLE if args.fall == "alle" else (args.fall,)):
        with tempfile.TemporaryDirectory(prefix="glide-lokalisierung-") as data:
            lauf = None
            try:
                lauf = Lauf(args.app, data)
                detail = globals()["fall_" + name](lauf)
                assert not lauf.errors, lauf.errors
                result["faelle"][name] = {"ok": True, "befund": detail}
                print("OK", name, detail, flush=True)
            except Exception:
                detail = traceback.format_exc().replace(str(Path.home()), "~")[-2400:]
                result["faelle"][name] = {"ok": False, "befund": detail}
                result["fehler"].append(name)
                print("ROT", name, detail, flush=True)
            finally:
                if lauf is not None:
                    lauf.ende()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("T335 Lokalisierung:", "OK" if not result["fehler"] else "ROT " + ", ".join(result["fehler"]), flush=True)
    return 1 if result["fehler"] else 0


if __name__ == "__main__":
    sys.exit(main())
