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
    texte = []
    ende = menu.index("end")
    for index in range(0 if ende is None else ende + 1):
        if menu.type(index) in ("command", "cascade", "checkbutton", "radiobutton"):
            texte.append(str(menu.entrycget(index, "label")))
    return texte


def beide_sprachen(lauf, pruefung):
    """Englisch ohne deutsche Reste, dann Deutsch als Gegenprobe."""
    i18n = lauf.mod.glide_i18n
    vorher = i18n.get_language()
    try:
        i18n.set_language("en")
        englisch = pruefung("en")
        reste = deutsche_reste(englisch)
        assert not reste, f"deutsche Reste auf Englisch: {reste}"
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
        assert not fehlt, (sprache, fehlt, texte)
        return texte

    en, de = beide_sprachen(lauf, pruefung)
    return f"Tageshinweise, Einstellungen, Speicherstatus und Mondphase: {en} englische, {de} deutsche Texte"


FAELLE = ("l1_tageshinweise",)


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
