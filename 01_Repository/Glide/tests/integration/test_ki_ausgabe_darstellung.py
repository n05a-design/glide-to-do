# SPDX-License-Identifier: MPL-2.0
"""KI-Ausgaben in der echten Oberfläche (WA-61): Zeigt Glide, was ein Agent mit dem Skill anlegt?

Zentrale Darstellungsprüfung für die Vollprüfung. Sie führt `tests/tools/ki_ausgabe.py`
mit echter Glide-Instanz aus: jede Datei anlegen, speichern, Glide in einem neuen
Prozess neu starten, Bestand vergleichen und die Anzeige ablesen (Zeilen der Liste,
Text und Aufgabenkästchen von Seite und Notiz, Zeichenfläche). Gegenproben
verfälschen danach die Anzeige und verlangen, dass die Ablesung das bemerkt.

Geprüft werden alle Beispiele des Skills, eine Vollprobe an den Grenzen des
Austauschformats und eine absichtlich fehlerhafte KI-Ausgabe, deren Abweichungen
einzeln erkannt werden müssen. Nur künstliche Daten in einem temporären Ordner.
"""
import contextlib
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tests" / "tools"))
sys.dont_write_bytecode = True
import ki_ausgabe  # noqa: E402

BEISPIELE = REPO / "skills" / "glide-to-do" / "assets" / "beispiele"
NAMEN = ("einkaufsliste.glideexchange", "projekt.glideexchange", "notiz.glideexchange",
         "zeichnung.glideexchange", "recherchebericht.md")


def vollprobe():
    """Alle übernommenen Felder an ihren Grenzen: Titel mit 40 Zeichen, 12 Ebenen, 50 Schritte."""
    tiefe = {"type": "task", "title": "Ebene 12"}
    for ebene in range(11, 0, -1):
        tiefe = {"type": "group" if ebene % 2 else "task", "title": f"Ebene {ebene}", "children": [tiefe]}
    return {
        "format": "glide.exchange", "format_version": 2, "mode": "create",
        "generator": {"type": "ai", "name": "glide-to-do"},
        "labels": [{"key": f"l{n}", "name": name} for n, name in enumerate(("Büro", "Zuhause", "Ä-ö-ü ß", "🚲 Rad"))],
        "folders": [{"key": "o1", "title": "Oberste Ebene", "description": "Zeile 1\nZeile 2"},
                    {"key": "o2", "title": "Mitte", "parent": "o1"},
                    {"key": "o3", "title": "Unten", "parent": "o2", "description": "Drei Ebenen tief"}],
        "lists": [
            {"key": "a", "title": "x" * 40, "folder": "o3", "description": "Titel mit genau 40 Zeichen",
             "items": [
                 {"type": "task", "title": "Alles gesetzt", "description": "Mehrzeilig\nmit Umlauten äöüß und 🚀",
                  "importance": 3, "due": "2026-12-31", "due_time": "23:59", "planned_date": "2026-12-30",
                  "estimated_minutes": 60000, "labels": ["l0", "l1", "l2", "l3"], "done": False,
                  "checklist": [{"text": f"Schritt {n}", "done": n % 3 == 0} for n in range(1, 51)]},
                 {"type": "task", "title": "Erledigt", "done": True, "importance": 1},
                 {"type": "long", "title": "Langtext", "description": "Erklärender Text ohne Termin."},
                 {"type": "heading", "title": "Abschnitt"},
                 tiefe,
             ]},
            {"key": "b", "title": "Notiz mit Sonderzeichen", "list_kind": "note",
             "rich_note": {"text": "Zeile mit 🚀 und 👩‍💻\n\nAbsatz – „Anführung“ · 100 %", "spans": [], "links": {}},
             "items": [{"title": "Folgeaufgabe", "due": "2027-01-04"}]},
        ],
    }


VOLLSEITE = """# Vollprobe Seite

Absatz mit **fett**, *kursiv*, ~~durchgestrichen~~, `Code` und [Link](https://example.org).

## Abschnitt

- Punkt
  - Unterpunkt
    - Unter-Unterpunkt
1. Erstens
2. Zweitens

### Aufgaben

- [ ] Offen mit Emoji 🚀
- [x] Erledigt
  - [ ] Eingerückt

#### Tabelle

| Spalte | Wert |
|---|---|
| ä | ö |

> Zitat

---

```
code block
```
"""

FEHLERHAFT = {
    "format": "glide.exchange", "format_version": 2, "mode": "create",
    "labels": [{"key": "l1", "name": "Team", "color": "accent"}],
    "folders": [{"key": "f2", "title": "Kind", "parent": "f1"}, {"key": "f1", "title": "Eltern"}],
    "lists": [{"key": "a", "title": "Planung für das große Sommerfest im Garten", "folder": "f1", "labels": ["l1"],
               "items": [{"type": "task", "title": "Getränke", "due": "27.11.2026", "repeat": "weekly"},
                         {"type": "heading", "title": "Abschnitt", "due": "2026-11-27"},
                         {"type": "task", "title": "Uhrzeit allein", "due_time": "09:00"}]}],
}

arbeit = Path(tempfile.mkdtemp(prefix="glide-ki-darstellung-"))
mod, ordner = ki_ausgabe.glide_laden()
try:
    (arbeit / "vollprobe.glideexchange").write_text(json.dumps(vollprobe(), ensure_ascii=False), encoding="utf-8")
    (arbeit / "vollprobe.md").write_text(VOLLSEITE, encoding="utf-8")
    (arbeit / "fehlerhaft.glideexchange").write_text(json.dumps(FEHLERHAFT, ensure_ascii=False), encoding="utf-8")
    dateien = [BEISPIELE / name for name in NAMEN] + [arbeit / "vollprobe.glideexchange", arbeit / "vollprobe.md",
                                                     arbeit / "fehlerhaft.glideexchange"]
    with contextlib.redirect_stdout(io.StringIO()):
        ergebnisse = ki_ausgabe.pruefe_mit_oberflaeche(mod, [str(p) for p in dateien], gegenprobe=True)
    print(ki_ausgabe.bericht_text(ergebnisse))
    nach_name = {Path(e.datei).name: e for e in ergebnisse}

    for name in (*NAMEN, "vollprobe.glideexchange", "vollprobe.md"):
        ergebnis = nach_name[name]
        assert ergebnis.bestanden, ki_ausgabe.bericht_text([ergebnis])
        assert not ergebnis.arten(ki_ausgabe.GRENZE), name
        assert not ergebnis.arten(ki_ausgabe.FEHLER), name
    assert nach_name["vollprobe.glideexchange"].angelegt == {"ordner": 3, "listen": 2, "punkte": 17}, \
        nach_name["vollprobe.glideexchange"].angelegt
    assert nach_name["vollprobe.md"].angelegt == {"seiten": 1, "punkte": 3}, nach_name["vollprobe.md"].angelegt

    fehlerhaft = nach_name["fehlerhaft.glideexchange"]
    assert not fehlerhaft.bestanden
    abweichungen = " | ".join(b.text for b in fehlerhaft.arten(ki_ausgabe.ABWEICHUNG))
    for erwartet in ("liegt auf oberster Ebene", "Titel auf 40 Zeichen gekürzt", "due: Datei '27.11.2026'",
                     "an einer Gliederung", "Uhrzeit ohne Fälligkeitsdatum"):
        assert erwartet in abweichungen, (erwartet, abweichungen)
    grenzen = " | ".join(b.text for b in fehlerhaft.arten(ki_ausgabe.GRENZE))
    for erwartet in ("„repeat“", "„color“", "„labels“"):
        assert erwartet in grenzen, (erwartet, grenzen)
    # Auch die fehlerhafte Datei wird angezeigt, wie Glide sie gespeichert hat; die Gegenprobe greift.
    assert not [b for b in fehlerhaft.befunde if b.ort.startswith(("Anzeige", "Neustart", "Gegenprobe"))], \
        ki_ausgabe.bericht_text([fehlerhaft])
    print("KI-Ausgaben in der Oberfläche: Beispiele, Vollprobe und Gegenproben bestanden")
finally:
    shutil.rmtree(arbeit, ignore_errors=True)
    shutil.rmtree(ordner, ignore_errors=True)
