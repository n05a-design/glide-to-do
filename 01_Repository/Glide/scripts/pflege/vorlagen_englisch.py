# SPDX-License-Identifier: MPL-2.0
"""Erzeugt den englischen Vorlagenkatalog aus dem deutschen (D93).

Aufruf aus `01_Repository/Glide`:
    python3 -B scripts/pflege/vorlagen_englisch.py            # schreiben
    python3 -B scripts/pflege/vorlagen_englisch.py --pruefen  # nur abgleichen

Quelle ist `resources/templates/glide_vorlagen.glidetemplates`, Ziel
`glide_vorlagen.en.glidetemplates`. Übersetzt werden nur sichtbare Texte
(Titel, Notizen, Aufgabentexte, Beschreibungen, Label- und Anhangnamen,
Anhanginhalte); Kennungen, Farben, Termine und Speicherpfade bleiben gleich,
damit Glide unveränderte mitgelieferte Vorlagen zwischen den Sprachen
austauschen kann. Kernsätze stehen in `vorlagen_en.json`; wiederkehrende
Satzbausteine setzt das Werkzeug zusammen. Ein „Originaltitel“-Nachsatz
entfällt, weil die englischen Titel die Titelgrenze einhalten. Nach jeder
Änderung des deutschen Katalogs erneut ausführen; `--pruefen` meldet einen
fehlenden Satz oder einen veralteten englischen Katalog.
"""
import argparse
import base64
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUELLE = ROOT / "src/glide/resources/templates/glide_vorlagen.glidetemplates"
ZIEL = ROOT / "src/glide/resources/templates/glide_vorlagen.en.glidetemplates"
KERN = json.loads((pathlib.Path(__file__).with_name("vorlagen_en.json")).read_text(encoding="utf-8"))
TEXTFELDER = {"text", "title", "note", "description", "name", "prompt", "location"}
BAUSTEINE = (
    (" Konkrete Ergebnisse, Labels und Detailbeschreibungen sind vorbereitet; Namen und Fristen beim Einsatz anpassen.",
     " Concrete outcomes, labels and detailed descriptions are prepared; adjust names and deadlines when you use it."),
    ("\nAbschluss: Das beschriebene Ergebnis liegt nachvollziehbar in der Projektablage vor.",
     "\nDone when: the described result is filed traceably in the project folder."),
    (" Beispielablauf: Umfang, Zuständigkeiten und Terminabstände mit dem konkreten Auftrag abstimmen.",
     " Sample workflow: align scope, responsibilities and intervals with the actual assignment."),
)
BRIEFING = ("\n\nObjekt / Projektkennung:\nVerantwortliche Person:\nFreigabe durch:\nAbnahmekriterien:\nAblagepfad:\n\n"
            "Nur bestätigte Angaben eintragen. Diese Vorlage enthält keine Zugangsdaten.\n",
            "\n\nProperty / project ID:\nOwner:\nApproved by:\nAcceptance criteria:\nFile path:\n\n"
            "Enter confirmed details only. This template contains no credentials.\n")


def englisch(text):
    if text in KERN:
        return KERN[text]
    text = text.split("\n\nOriginaltitel:\n")[0]
    if text in KERN:
        return KERN[text]
    for deutsch, english in BAUSTEINE:
        if text.endswith(deutsch):
            return englisch(text[:-len(deutsch)]) + english
    if text.endswith(BRIEFING[0]):
        titel, ziel = re.fullmatch(r"(.*)\n\nZiel: (.*)", text[:-len(BRIEFING[0])], re.S).groups()
        return KERN[titel] + "\n\nGoal: " + KERN[ziel] + BRIEFING[1]
    phase = re.fullmatch(r"(.*\.) Phase (\d): (.*)\.", text, re.S)
    if phase:
        return f"{KERN[phase.group(1)]} Phase {phase.group(2)}: {KERN[phase.group(3)]}."
    if text.startswith("Arbeitspaket: "):
        return "Work package: " + KERN[text[len("Arbeitspaket: "):]]
    raise KeyError(text)


def uebersetzen(knoten):
    if isinstance(knoten, dict):
        for schluessel, wert in list(knoten.items()):
            if schluessel in TEXTFELDER and isinstance(wert, str) and wert.strip():
                knoten[schluessel] = englisch(wert)
            elif schluessel == "items" and isinstance(wert, list) and wert and all(isinstance(x, str) for x in wert):
                knoten[schluessel] = [englisch(x) for x in wert]
            elif schluessel == "files" and isinstance(wert, dict):
                knoten[schluessel] = {pfad: base64.b64encode(englisch(base64.b64decode(inhalt).decode("utf-8"))
                                                             .encode("utf-8")).decode("ascii")
                                      for pfad, inhalt in wert.items()}
            else:
                uebersetzen(wert)
    elif isinstance(knoten, list):
        for wert in knoten:
            uebersetzen(wert)


def groessen(knoten, dateien):
    if isinstance(knoten, dict):
        if knoten.get("storage") in dateien and "size" in knoten:
            knoten["size"] = len(base64.b64decode(dateien[knoten["storage"]]))
        for wert in knoten.values():
            groessen(wert, dateien)
    elif isinstance(knoten, list):
        for wert in knoten:
            groessen(wert, dateien)


def erzeugen():
    daten = json.loads(QUELLE.read_text(encoding="utf-8"))
    uebersetzen(daten["templates"])
    for vorlage in daten["templates"]:
        groessen(vorlage.get("payload"), vorlage.get("files") or {})
    return json.dumps(daten, ensure_ascii=False, indent=2) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--pruefen", action="store_true", help="nur abgleichen, nichts schreiben")
    args = parser.parse_args()
    try:
        text = erzeugen()
    except KeyError as exc:
        print("Übersetzung fehlt in vorlagen_en.json:", repr(exc.args[0])[:200])
        return 1
    if args.pruefen:
        aktuell = ZIEL.is_file() and ZIEL.read_text(encoding="utf-8") == text
        print("Englischer Vorlagenkatalog", "aktuell" if aktuell else "veraltet – Werkzeug ausführen")
        return 0 if aktuell else 1
    ZIEL.write_text(text, encoding="utf-8")
    print("geschrieben:", ZIEL.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
