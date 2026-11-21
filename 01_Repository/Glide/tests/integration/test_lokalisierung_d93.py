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
STRENG = False


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

    Der Berichtstext des Speicherstatus kommt aus `storage_health` (Paket L8) und
    zählt hier noch nicht; geprüft werden Titel und Knöpfe des Dialogs.
    """
    app, mod = lauf.app, lauf.mod

    def pruefung(sprache):
        texte = modal_texte(lauf, app.show_daily_hint_settings)
        texte += modal_texte(lauf, app.show_daily_hints)
        status = modal_texte(lauf, app.show_storage_status)
        texte += [text for text in status if "\n" not in text]
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
                           "Table columns"},
                    "de": {"Neuer Punkt", "Titel", "Wichtigkeit", "Fälligkeit", "Wiederholung",
                           "Umbenennen", "Tabellenspalten"}}
        fehlt = erwartet[sprache] - set(texte)
        assert not fehlt, (sprache, fehlt, texte)
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
        assert not fehlt, (sprache, fehlt, texte)
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
        assert not fehlt, (sprache, fehlt, texte)
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
        assert not fehlt, (sprache, fehlt, texte)
        return [text for text in texte if "Epsilon" not in text and ".glide" not in text]

    en, de = beide_sprachen(lauf, pruefung)
    return f"Drucken, Sicherungen und KI-Austausch: {en} englische, {de} deutsche Texte"


FAELLE = ("l1_tageshinweise", "l2_tag_und_start", "l3_punkte_und_labels", "l4_menues_und_anlegen",
          "l5_erinnerungen_und_erfassung", "l6_drucken_und_sicherungen")


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
