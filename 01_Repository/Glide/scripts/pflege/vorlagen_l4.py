# SPDX-License-Identifier: MPL-2.0
"""Pflegt die drei L4-Referenzvorlagen im mitgelieferten Vorlagenkatalog (Glide 1.1.0).

Aufruf aus `01_Repository/Glide`:
    python3 -B scripts/pflege/vorlagen_l4.py            # deutschen Katalog und vorlagen_en.json schreiben
    python3 -B scripts/pflege/vorlagen_l4.py --pruefen  # nur abgleichen
    python3 -B scripts/pflege/vorlagen_englisch.py      # danach englischen Katalog erzeugen

Die Vorlagen entstehen hier als vollständige Format-26-Bestände (Vorlagenformat 2,
`payload`), nicht als lose Titellisten: Glide übernimmt sie über den additiven
Sicherungsimport mit neuen Kennungen und verschiebt Fälligkeit und
Bearbeitungstag relativ zu `schedule_anchor`. Kennungen sind aus Vorlage und
Pfad abgeleitet (MD5) und damit über Läufe stabil. Deutsche Texte stehen hier,
die englischen Gegenstücke trägt das Werkzeug in `vorlagen_en.json` nach, aus
dem `vorlagen_englisch.py` den englischen Katalog erzeugt (D93).

Referenz: `00_Arbeitsvorbereitung/Referenzvorlagen/` (Inhaltsskizzen, kein
Vorlagenformat-2-Bestand) und Entwicklungsplan §4.3 L4.
"""
import argparse
from datetime import date, timedelta
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
KATALOG = ROOT / "src/glide/resources/templates/glide_vorlagen.glidetemplates"
KERN = pathlib.Path(__file__).with_name("vorlagen_en.json")
ANKER = date(2026, 9, 14)  # Montag; Fälligkeiten verschieben sich relativ dazu
STAMP = "2026-09-14T00:00:00+02:00"
L4_IDS = ("client-project", "design-project", "weekly-review")

# Systemlabels wie in den übrigen Katalogvorlagen (gleiche Kennungen, damit der
# Import sie zusammenführt statt zu verdoppeln).
SYSTEM_LABELS = (
    {"id": "1c73a83195775d98a82d78312646c08e", "name": "Langtext", "color": "clear", "system": "long"},
    {"id": "a8c3814c91b754aea845578e7da8ad7f", "name": "Zwischenüberschrift", "color": "accent", "system": "heading"},
)
HEADING_LABEL = SYSTEM_LABELS[1]["id"]


def kennung(*teile):
    return hashlib.md5(":".join(("glide-l4",) + teile).encode("utf-8")).hexdigest()


def tag(offset):
    return None if offset is None else (ANKER + timedelta(days=offset)).isoformat()


# Texte DE → EN. Jede deutsche Zeichenkette dieser Datei braucht ihr Gegenstück.
UEBERSETZUNG = {}


def de(text, en):
    UEBERSETZUNG[text] = en
    return text


def punkt(vorlage, pfad, text, *, beschreibung="", kind="task", due=None, due_time=None, planned=None,
          minuten=None, wichtig=0, labels=(), checkliste=(), blockiert=()):
    return {
        "id": kennung(vorlage, pfad), "text": text, "done": False, "importance": wichtig,
        "due": tag(due), "due_time": due_time, "description": beschreibung, "attachments": [],
        "color": None, "kind": kind,
        "labels": ([HEADING_LABEL] if kind == "heading" else []) + list(labels),
        "repeat": None, "reminder": None, "planned_date": tag(planned), "estimated_minutes": minuten,
        "checklist": [{"id": kennung(vorlage, pfad, "c", str(i)), "text": eintrag, "done": False}
                      for i, eintrag in enumerate(checkliste)],
        "links": [], "blocked_by": [kennung(vorlage, ziel) for ziel in blockiert],
        "planned_time": None, "time_spent_minutes": None, "done_at": None, "children": [],
    }


def ueberschrift(vorlage, pfad, text):
    return punkt(vorlage, pfad, text, kind="heading")


def liste(vorlage, schluessel, titel, notiz, punkte, *, folder_id=None, labels=()):
    return {
        "id": kennung(vorlage, "list", schluessel), "title": titel, "folder_id": folder_id, "color": "clear",
        "note": notiz, "list_kind": "tasks", "rich_note": {"text": "", "spans": [], "links": {}},
        "created_at": STAMP, "updated_at": STAMP,
        "journal": {"favorite": False, "mood": "", "location": "", "moment_date": ANKER.isoformat(), "prompt": ""},
        "system_role": None, "labels": list(labels), "attachments": [], "icon": None,
        "archived": False, "archived_at": None, "items": punkte,
    }


def ordner(vorlage, titel, notiz, labels):
    return {"id": kennung(vorlage, "folder"), "title": titel, "color": "accent", "note": notiz,
            "labels": list(labels), "attachments": [], "folder_kind": "standard", "parent_id": None,
            "icon": None, "archived": False, "archived_at": None}


def label(vorlage, name, farbe="clear"):
    return {"id": kennung(vorlage, "label", name), "name": name, "color": farbe}


def bestand(lists, folders, labels, aktiv):
    return {"app": "Glide", "app_version": None, "version": 26, "exported_at": "2026-09-14T00:00:00",
            "lists": lists, "folders": folders, "labels": list(SYSTEM_LABELS) + labels,
            "trash": [], "active_list_id": aktiv, "active_folder_id": None}


def kundenprojekt():
    v = "client-project"
    meilenstein = label(v, de("Meilenstein", "Milestone"), "due_action")
    kunde = label(v, de("Kunde", "Client"), "accent")
    fid = kennung(v, "folder")
    briefing = liste(v, "briefing", de("Briefing und Anforderungen", "Briefing and requirements"),
                     de("Kundenbriefing, Ziele und Anforderungen klären, bevor Umfang und Preis feststehen.",
                        "Clarify the client briefing, goals and requirements before scope and price are fixed."), [
        ueberschrift(v, "b.h1", de("Kundenbriefing", "Client briefing")),
        punkt(v, "b.gespraech", de("Briefinggespräch mit {{Kunde}} führen und protokollieren",
                                        "Hold and minute the briefing call with {{Client}}"),
              beschreibung=de("Anlass, Zielgruppe, gewünschtes Ergebnis und Rahmen in eigenen Worten festhalten.",
                              "Record occasion, audience, desired result and constraints in your own words."),
              due=0, minuten=60, wichtig=2, labels=[kunde["id"]]),
        punkt(v, "b.kontakte", de("Ansprechpartner und Entscheidungswege notieren", "Note contacts and decision paths"),
              due=1, minuten=15),
        punkt(v, "b.rahmen", de("Budget- und Zeitrahmen bestätigen lassen", "Have budget and timeframe confirmed"),
              due=2, minuten=20, wichtig=2, labels=[kunde["id"]]),
        ueberschrift(v, "b.h2", de("Ziele und Anforderungen", "Goals and requirements")),
        punkt(v, "b.ziele", de("Projektziele messbar formulieren", "Phrase measurable project goals"),
              due=3, minuten=30, checkliste=(de("Was ist am Ende anders?", "What is different at the end?"),
                                             de("Woran wird Erfolg gemessen?", "How is success measured?"))),
        punkt(v, "b.abgrenzung", de("Anforderungen und Abgrenzung festhalten", "Record requirements and exclusions"),
              beschreibung=de("Auch festhalten, was ausdrücklich nicht zum Auftrag gehört.",
                              "Also record what is explicitly not part of the job."), due=3, minuten=45),
        punkt(v, "b.angebot", de("Leistungsbeschreibung und Angebot freigeben lassen",
                                 "Get the scope statement and quote approved"),
              due=5, wichtig=2, labels=[meilenstein["id"]], blockiert=("b.ziele", "b.abgrenzung")),
    ], folder_id=fid)
    phasen = liste(v, "phasen", de("Phasen und Meilensteine", "Phases and milestones"),
                   de("Projektphasen mit Terminen. Fälligkeiten verschieben sich beim Anwenden auf den gewählten Starttag.",
                      "Project phases with dates. Due dates shift to the chosen start day when the template is applied."), [
        ueberschrift(v, "p.h1", de("Phase 1 – Konzept", "Phase 1 – Concept")),
        punkt(v, "p.konzept", de("Konzept ausarbeiten", "Work out the concept"), planned=7, minuten=240),
        punkt(v, "p.m1", de("Meilenstein: Konzept vorgestellt", "Milestone: concept presented"), due=10,
              due_time="10:00", wichtig=2, labels=[meilenstein["id"]], blockiert=("p.konzept",)),
        ueberschrift(v, "p.h2", de("Phase 2 – Umsetzung", "Phase 2 – Delivery")),
        punkt(v, "p.pakete", de("Arbeitspakete in Aufgaben zerlegen", "Break work packages into tasks"),
              beschreibung=de("Je Paket ein Ergebnis, eine Schätzung und einen Bearbeitungstag festlegen.",
                              "Give each package an outcome, an estimate and a planned day."), planned=11, minuten=45),
        punkt(v, "p.umsetzung", de("Umsetzung und Qualitätsprüfung", "Delivery and quality check"), planned=14, minuten=480),
        punkt(v, "p.m2", de("Meilenstein: Zwischenstand abgestimmt", "Milestone: interim status agreed"), due=21,
              wichtig=2, labels=[meilenstein["id"]], blockiert=("p.umsetzung",)),
        ueberschrift(v, "p.h3", de("Phase 3 – Abschluss", "Phase 3 – Wrap-up")),
        punkt(v, "p.m3", de("Meilenstein: Endabnahme", "Milestone: final acceptance"), due=28, wichtig=2,
              labels=[meilenstein["id"]]),
    ], folder_id=fid)
    feedback = liste(v, "feedback", de("Feedback und Abnahme", "Feedback and acceptance"),
                     de("Rückmeldungen gebündelt einholen, Korrekturen nachvollziehbar umsetzen, Abnahme schriftlich festhalten.",
                        "Collect feedback in bundles, apply corrections traceably, record acceptance in writing."), [
        punkt(v, "f.runde", de("Feedbackrunde terminieren", "Schedule the feedback round"), due=11, minuten=10,
              labels=[kunde["id"]]),
        punkt(v, "f.sammeln", de("Feedback sammeln und priorisieren", "Collect and prioritise feedback"), planned=12,
              minuten=30, checkliste=(de("Muss", "Must"), de("Sollte", "Should"), de("Später", "Later"))),
        punkt(v, "f.korrektur", de("Korrekturen umsetzen", "Apply corrections"), planned=15, minuten=180,
              blockiert=("f.sammeln",)),
        punkt(v, "f.abnahme", de("Abnahme schriftlich einholen", "Obtain written acceptance"), due=28, wichtig=2,
              labels=[meilenstein["id"], kunde["id"]], blockiert=("f.korrektur",)),
    ], folder_id=fid)
    uebergabe = liste(v, "uebergabe", de("Übergabe und Abschluss", "Handover and close"),
                      de("Ergebnisse, Unterlagen und Rechnung sauber übergeben. Zugangsdaten nie im Klartext ablegen.",
                         "Hand over results, documents and invoice cleanly. Never store credentials in plain text."), [
        punkt(v, "u.dateien", de("Ergebnisse und Quelldateien übergeben", "Hand over results and source files"), due=29,
              minuten=45),
        punkt(v, "u.doku", de("Kurze Projektdokumentation übergeben", "Hand over a short project documentation"), due=29,
              minuten=60),
        punkt(v, "u.rechnung", de("Rechnung stellen", "Send the invoice"), due=30, minuten=20, wichtig=2,
              blockiert=("u.dateien",)),
        punkt(v, "u.rueckblick", de("Rückblick: Was nehme ich mit?", "Retrospective: what do I take away?"), planned=31,
              minuten=20),
    ], folder_id=fid)
    folders = [ordner(v, de("Freelance-Kundenprojekt", "Freelance client project"),
                      de("Ein Kundenprojekt vom Briefing über Meilensteine und Feedback bis zu Abnahme, Übergabe und Rechnung.",
                         "A client project from briefing via milestones and feedback to acceptance, handover and invoice."),
                      [kunde["id"]])]
    return v, "folder", bestand([briefing, phasen, feedback, uebergabe], folders, [meilenstein, kunde], briefing["id"])


def designprojekt():
    v = "design-project"
    runde = label(v, de("Entwurfsrunde", "Design round"), "accent")
    freigabe = label(v, de("Freigabe", "Approval"), "export")
    fid = kennung(v, "folder")
    inspiration = liste(v, "inspiration", de("Inspiration und Moodboard", "Inspiration and mood board"),
                        de("Referenzen sammeln, Stimmung und Farbklima festlegen, bevor entworfen wird.",
                           "Collect references and settle mood and colour climate before designing."), [
        punkt(v, "i.referenzen", de("Referenzen sammeln", "Collect references"),
              beschreibung=de("Quellen und Nutzungsrechte zu jeder Referenz notieren.",
                              "Note source and usage rights for each reference."), planned=0, minuten=60),
        punkt(v, "i.moodboard", de("Moodboard auf einer Pinnwand anlegen", "Create a mood board on a board"),
              planned=1, minuten=60, blockiert=("i.referenzen",)),
        punkt(v, "i.farben", de("Farbklima und Typografie festhalten", "Record colour climate and typography"),
              planned=2, minuten=45),
    ], folder_id=fid)
    konzept = liste(v, "konzept", de("Konzept und Entwurfsrunden", "Concept and design rounds"),
                    de("Ein Konzept, dann Entwürfe in Runden. Jede Runde endet mit einer Auswahl.",
                       "One concept, then drafts in rounds. Each round ends with a selection."), [
        punkt(v, "k.konzept", de("Gestaltungskonzept in drei Sätzen", "Design concept in three sentences"), due=3,
              minuten=45, wichtig=2),
        ueberschrift(v, "k.h1", de("Entwurfsrunde 1", "Design round 1")),
        punkt(v, "k.skizzen", de("Skizzen anfertigen", "Make sketches"), planned=4, minuten=120, labels=[runde["id"]],
              blockiert=("k.konzept",)),
        punkt(v, "k.varianten", de("Drei Varianten ausarbeiten", "Work out three variants"), planned=5, minuten=240,
              labels=[runde["id"]], checkliste=(de("Variante A", "Variant A"), de("Variante B", "Variant B"),
                                               de("Variante C", "Variant C"))),
        ueberschrift(v, "k.h2", de("Entwurfsrunde 2", "Design round 2")),
        punkt(v, "k.verfeinern", de("Gewählte Variante verfeinern", "Refine the chosen variant"), planned=9,
              minuten=240, labels=[runde["id"]]),
    ], folder_id=fid)
    revision = liste(v, "revision", de("Feedback und Revisionen", "Feedback and revisions"),
                     de("Rückmeldungen je Runde bündeln; der Revisionsstand bleibt nachvollziehbar.",
                        "Bundle feedback per round; the revision state stays traceable."), [
        punkt(v, "r.feedback", de("Feedback zur Variantenauswahl einholen", "Get feedback on the variant selection"),
              due=7, minuten=30),
        punkt(v, "r.revision1", de("Revision 1 umsetzen", "Apply revision 1"), planned=8, minuten=120,
              blockiert=("r.feedback",)),
        punkt(v, "r.revision2", de("Revision 2 umsetzen", "Apply revision 2"), planned=11, minuten=90),
        punkt(v, "r.stand", de("Revisionsstand dokumentieren", "Document the revision state"), planned=11, minuten=15),
    ], folder_id=fid)
    abschluss = liste(v, "abschluss", de("Freigabe und Asset-Übergabe", "Approval and asset handover"),
                      de("Freigabe festhalten und die finalen Dateien vollständig übergeben.",
                         "Record approval and hand over the final files completely."), [
        punkt(v, "a.freigabe", de("Freigabe einholen", "Obtain approval"), due=14, wichtig=2,
              labels=[freigabe["id"]], blockiert=("r.revision2",)),
        punkt(v, "a.export", de("Finale Assets exportieren", "Export final assets"), planned=15, minuten=60,
              blockiert=("a.freigabe",), checkliste=(de("Druckdaten", "Print files"), de("Bildschirmformate", "Screen formats"),
                                                     de("Quelldateien", "Source files"))),
        punkt(v, "a.uebergabe", de("Assets und Nutzungshinweise übergeben", "Hand over assets and usage notes"),
              due=16, minuten=30, labels=[freigabe["id"]]),
    ], folder_id=fid)
    folders = [ordner(v, de("Kreatives Designprojekt", "Creative design project"),
                      de("Vom Moodboard über Entwurfsrunden und Revisionen bis zu Freigabe und Asset-Übergabe.",
                         "From mood board via design rounds and revisions to approval and asset handover."),
                      [runde["id"]])]
    return v, "folder", bestand([inspiration, konzept, revision, abschluss], folders, [runde, freigabe],
                                inspiration["id"])


def wochenplanung():
    v = "weekly-review"
    fokus = label(v, de("Fokus", "Focus"), "accent")
    puffer = label(v, de("Puffer", "Buffer"), "clear")
    woche = liste(v, "woche", de("Persönliche Wochenplanung", "Personal weekly plan"),
                  de("Absichten, Fokus, Termine und Puffer für eine Woche – und am Ende ein ruhiger Rückblick ohne Bewertung.",
                     "Intentions, focus, appointments and buffers for one week – and a calm review at the end, without scores."), [
        ueberschrift(v, "w.h1", de("Wochenabsichten", "Weekly intentions")),
        punkt(v, "w.absicht1", de("Absicht 1: …", "Intention 1: …"),
              beschreibung=de("Was soll diese Woche gut werden? Ein Satz genügt.",
                              "What should go well this week? One sentence is enough."), planned=0, minuten=5),
        punkt(v, "w.absicht2", de("Absicht 2: …", "Intention 2: …"), planned=0, minuten=5),
        punkt(v, "w.absicht3", de("Absicht 3: …", "Intention 3: …"), planned=0, minuten=5),
        ueberschrift(v, "w.h2", de("Fokusziele", "Focus goals")),
        punkt(v, "w.fokus1", de("Fokusblock für das wichtigste Ergebnis", "Focus block for the most important outcome"),
              planned=1, minuten=90, wichtig=2, labels=[fokus["id"]]),
        punkt(v, "w.fokus2", de("Zweiter Fokusblock", "Second focus block"), planned=3, minuten=90, labels=[fokus["id"]]),
        ueberschrift(v, "w.h3", de("Termine", "Appointments")),
        punkt(v, "w.termin", de("Feste Termine der Woche eintragen", "Enter the week's fixed appointments"),
              beschreibung=de("Termine mit Uhrzeit als Fälligkeit setzen; der Kalender zeigt sie dann am Tag.",
                              "Set appointments as due dates with a time; the calendar then shows them on the day."),
              due=0, due_time="09:00", minuten=10),
        ueberschrift(v, "w.h4", de("Puffer", "Buffers")),
        punkt(v, "w.puffer1", de("Puffer freihalten (Mitte der Woche)", "Keep a buffer free (mid-week)"), planned=2,
              minuten=60, labels=[puffer["id"]]),
        punkt(v, "w.puffer2", de("Puffer freihalten (Freitag)", "Keep a buffer free (Friday)"), planned=4, minuten=60,
              labels=[puffer["id"]]),
        ueberschrift(v, "w.h5", de("Aufgaben der Woche", "Tasks for the week")),
        punkt(v, "w.aufgabe", de("Wichtige Aufgabe der Woche", "Important task of the week"), planned=1, minuten=60,
              wichtig=1),
        punkt(v, "w.erledigen", de("Kleinkram bündeln und erledigen", "Bundle and clear small tasks"), planned=3,
              minuten=45),
        ueberschrift(v, "w.h6", de("Wochenrückblick", "Weekly review")),
        punkt(v, "w.rueckblick", de("Wochenrückblick KW {{KW}}", "Weekly review, week {{week}}"),
              beschreibung=de("Was lief gut? Was wird übertragen? Was lasse ich bewusst los?",
                              "What went well? What carries over? What do I deliberately let go?"),
              planned=4, minuten=20,
              checkliste=(de("Was lief gut?", "What went well?"), de("Was wird übertragen?", "What carries over?"),
                          de("Was lasse ich los?", "What do I let go?"))),
    ], labels=[fokus["id"]])
    return v, "list", bestand([woche], [], [fokus, puffer], woche["id"])


def vorlagen(app_version):
    ergebnis = []
    for bauer in (kundenprojekt, designprojekt, wochenplanung):
        vid, art, payload = bauer()
        payload["app_version"] = app_version
        wurzel = payload["folders"][0] if art == "folder" else payload["lists"][0]
        ergebnis.append({
            "id": vid, "kind": art, "items": [], "payload": payload, "files": {},
            "title": wurzel["title"], "note": wurzel["note"], "labels": list(wurzel["labels"]),
            "color": wurzel["color"], "schedule_anchor": ANKER.isoformat(),
        })
    return ergebnis


def erzeugen():
    katalog = json.loads(KATALOG.read_text(encoding="utf-8"))
    vorhandene = [t for t in katalog["templates"] if t.get("id") not in L4_IDS]
    app_version = next((t["payload"].get("app_version") for t in vorhandene if t.get("payload")), None)
    katalog["templates"] = vorhandene + vorlagen(app_version)
    kern = json.loads(KERN.read_text(encoding="utf-8"))
    for deutsch, english in UEBERSETZUNG.items():
        # Vorhandene Übersetzungen gelten weiter (gleicher Satz, gleiche Fassung im ganzen Katalog).
        kern.setdefault(deutsch, english)
    return (json.dumps(katalog, ensure_ascii=False, indent=2) + "\n",
            json.dumps(kern, ensure_ascii=False, indent=1) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--pruefen", action="store_true", help="nur abgleichen, nichts schreiben")
    args = parser.parse_args()
    katalog, kern = erzeugen()
    if args.pruefen:
        aktuell = KATALOG.read_text(encoding="utf-8") == katalog and KERN.read_text(encoding="utf-8") == kern
        print("L4-Vorlagen", "aktuell" if aktuell else "veraltet – Werkzeug ausführen")
        return 0 if aktuell else 1
    KATALOG.write_text(katalog, encoding="utf-8", newline="\n")
    KERN.write_text(kern, encoding="utf-8", newline="\n")
    print("geschrieben:", KATALOG.relative_to(ROOT), "und", KERN.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
