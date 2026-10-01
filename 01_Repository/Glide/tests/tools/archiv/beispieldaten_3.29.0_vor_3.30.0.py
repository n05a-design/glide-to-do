#!/usr/bin/env python3.12
"""Erzeugt ein Komplettbackup mit ausführlichen Beispieldaten.

Kein Test, sondern ein Werkzeug. Es baut einen Bestand auf, wie ihn ein
Grafik- und Marketingarbeitsplatz im Wohn- und Städtebau tatsächlich führt –
Exposé-Produktion, Kampagne, Baustellenkommunikation, Gestaltungsregelwerk –
und schreibt ihn als `.glidebackup`. Die Datei lässt sich über
„Datei → Komplettbackup einlesen“ in eine leere Glide-Ablage importieren.

Warum als Backup und nicht als Speicherdatei: Ein Backup ist der einzige Weg,
Daten in eine bestehende Installation zu bringen, ohne dort von Hand Dateien
zu ersetzen. Und es durchläuft beim Import dieselbe Schemaprüfung wie jedes
andere Backup – was hier erzeugt wird, ist damit nachweislich gültig.

Der Bestand deckt bewusst jedes Merkmal ab, das die Anwendung kennt:
verschachtelte Ordner, Listen mit Beschreibungstext und Labels,
Zwischenüberschriften, Gruppen mit Unterpunkten, Long-Tasks als Notiz,
Fälligkeiten mit und ohne Uhrzeit, überfällige und erledigte Punkte, alle
sieben Palettenfarben und einen gefüllten Papierkorb.

Aufruf:

    python3.12 tests/tools/beispieldaten.py [--ziel PFAD]

Alle Fristen entstehen relativ zum Ausführungstag. Wer die Datei in einem
halben Jahr importiert, sieht deshalb eine plausible, aber verschobene Lage –
das ist gewollt: Ein fester Stichtag wäre nach zwei Wochen komplett überfällig.
"""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import os
import pathlib
import sys
import tempfile
from datetime import date, timedelta

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
APP_PATH = REPOSITORY_ROOT / "src" / "glide" / "app.pyw"
# Der Name im Repository ist kleingeschrieben. Unter macOS und Windows
# spielt das keine Rolle, unter Linux schon: Ein abweichend geschriebenes
# Ziel legt dort eine zweite Datei an, die auf den Zielplattformen die
# erste überschreibt.
DEFAULT_TARGET = REPOSITORY_ROOT / "tests" / "fixtures" / "beispiele" / "glide_beispieldaten.glidebackup"


def load_module(data_dir):
    """Lädt app.pyw mit isoliertem Datenverzeichnis.

    GLIDE_DATA_DIR muss vor dem Import gesetzt sein: Ein Erzeugungslauf darf
    die echten Nutzerdaten unter keinen Umständen berühren.
    """
    os.environ["GLIDE_DATA_DIR"] = str(data_dir)
    loader = importlib.machinery.SourceFileLoader("glide_app", str(APP_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules["glide_app"] = module
    loader.exec_module(module)
    return module


class Builder:
    """Kleine Hülle um die Anwendungsobjekte, damit der Inhalt unten lesbar bleibt."""

    def __init__(self, app):
        self.app = app
        self.today = date.today()
        self.labels = {}

    # --- Bausteine ------------------------------------------------------
    def day(self, offset):
        return (self.today + timedelta(days=offset)).isoformat()

    def label(self, name, color):
        entry = self.app.new_label_object(name, None, self._farbe(color))
        self.app.labels.append(entry)
        self.labels[name] = entry["id"]
        return entry["id"]

    def ids(self, *names):
        return [self.labels[name] for name in names]

    def task(self, text, **kwargs):
        """Eine gewöhnliche Aufgabe."""
        return self.app.new_item(text, **kwargs)

    def heading(self, text):
        """Zwischenüberschrift: Zäsur ohne Inhalt und ohne Status."""
        return self.app.new_item(text, kind=self.app.ITEM_KIND_HEADING)

    def note(self, text, **kwargs):
        """Long-Task: mehrzeilige Notiz, die in der Liste vollständig steht."""
        return self.app.new_item(text, kind=self.app.ITEM_KIND_LONG, **kwargs)

    def group(self, text, children, **kwargs):
        entry = self.app.new_item(text, kind=self.app.ITEM_KIND_GROUP, **kwargs)
        entry["children"] = list(children)
        return entry

    def open_list(self, entry):
        """Macht eine Liste zur aktiven – vollständig, mit allen drei Feldern.

        `app_title` gehört dazu: `sync_current_list_reference` schreibt diesen
        Wert beim Speichern in den Titel der aktiven Liste zurück. Wer ihn
        vergisst, benennt beim nächsten `save_items()` eine Liste um.
        """
        self.app.active_list_id = entry["id"]
        self.app.items = entry["items"]
        self.app.app_title = entry["title"]
        return entry

    def _farbe(self, color):
        """Die App verwirft eine unbekannte Farbe still (`raw.get("color") in
        LIST_COLOR_KEYS`). Genau so trug die Liste „Kalender, Erinnerungen und
        Tagesplanung" seit 3.21.2 keine Farbe, obwohl der Erzeuger `due_soon`
        setzte und die Dokumentation es behauptete. Der Fixture-Abgleich kann
        das nicht finden: Die Neuerzeugung verwirft denselben Wert genauso."""
        if color is not None and color not in self.app.LIST_COLOR_KEYS:
            raise ValueError(
                f"Unbekannte Farbe {color!r}; erlaubt sind "
                + ", ".join(self.app.LIST_COLOR_KEYS))
        return color

    def folder(self, title, color=None, note="", parent=None, labels=None):
        color = self._farbe(color)
        entry = self.app.new_folder_object(
            title, None, color, note, labels or [], parent
        )
        self.app.folders.append(entry)
        return entry["id"]

    def listing(self, title, items, folder=None, color=None, note="", labels=None):
        color = self._farbe(color)
        entry = self.app.new_list_object(
            title, [], None, folder, color, note, None, labels or []
        )
        entry["items"][:] = items
        self.app.lists.append(entry)
        return entry


def build(app, mod):
    """Der eigentliche Inhalt. Reihenfolge = Reihenfolge in der Seitenleiste."""
    b = Builder(app)

    # --- Labels: alle sieben Palettenfarben, damit die Chips vollständig
    # nachprüfbar sind -----------------------------------------------------
    b.label("Kunde", "accent")
    b.label("Intern", "flag")
    b.label("Druck", "export")
    b.label("Freigabe offen", "delete")
    b.label("Web", "clear")
    b.label("Foto", "import")
    b.label("Archiv", "due_action")

    # --- Eingang: was noch nicht einsortiert ist --------------------------
    # Ausdrücklich über is_inbox_list gesucht: current_list() zeigt beim ersten
    # Start auf die mitgelieferte Standardliste, nicht auf den Eingang.
    inbox = next(entry for entry in app.lists if app.is_inbox_list(entry))
    # Die Standardliste „Meine Liste" wird durch die Beispieldaten ersetzt. Die
    # aktive Liste muss dabei mitwandern: save_items() schreibt am Ende
    # app.items in die aktive Liste zurück, und die darf nicht die soeben
    # entfernte sein – sonst landet ein leerer Inhalt im Eingang.
    app.lists[:] = [entry for entry in app.lists if entry is inbox]
    b.open_list(inbox)
    inbox["note"] = (
        "Alles, was hereinkommt und noch keinen Platz hat. Einmal täglich leeren – "
        "was hier länger als eine Woche liegt, ist entweder eine Aufgabe oder es "
        "war nie eine."
    )
    inbox["items"][:] = [
        b.task("Rückruf Druckerei wegen Papiermuster Naturpapier 300 g",
               due=b.day(0), due_time="14:00", importance=3, labels=b.ids("Druck")),
        b.task("Angebot Drohnenaufnahmen Parkquartier prüfen",
               due=b.day(2), planned_date=b.day(0), estimated_minutes=45, labels=b.ids("Foto")),
        b.task("Kollegin fragt nach der Vorlage für Baustellenschilder",
               labels=b.ids("Intern")),
        b.note(
            "Idee für den Messeauftritt im Herbst:\n"
            "Statt Objektfotos an der Rückwand ein einziges großformatiges "
            "Lageplan-Rendering, davor die Modelle. Wer den Stand betritt, sieht "
            "zuerst das Quartier und erst dann die einzelnen Häuser.\n"
            "Vorteil: funktioniert ohne Text und ohne Erklärung.\n"
            "Zu klären: Druckdienstleister für Rückwand 4 × 2,5 m, Vorlaufzeit, "
            "Budgetrahmen aus der Marketingplanung.",
            labels=b.ids("Intern")),
    ]

    # ---------------------------------------------------------------
    # Ordner „Marketing"
    # ---------------------------------------------------------------
    marketing = b.folder(
        "Marketing", "accent",
        "Alles, was nach außen geht. Verantwortlich für Freigabe: Geschäftsführung.",
        labels=b.ids("Kunde"),
    )

    b.listing(
        "Exposé-Produktion", [
            b.heading("Vorbereitung"),
            b.task("Objektdaten aus onOffice ziehen und auf Vollständigkeit prüfen",
                   done=True, labels=b.ids("Intern")),
            b.task("Grundrisse vom Architekturbüro anfordern (DWG, nicht PDF)",
                   due=b.day(-4), importance=3, labels=b.ids("Freigabe offen")),
            b.note(
                "Warum DWG und nicht PDF:\n"
                "Aus dem PDF lassen sich Linienstärken und Schraffuren nicht sauber "
                "auf unsere Darstellung umstellen. Jeder Grundriss müsste von Hand "
                "nachgezeichnet werden – das sind pro Wohnungstyp rund zwei Stunden.\n"
                "Mit DWG ist es ein Import und eine Layerzuweisung."),

            b.heading("Gestaltung"),
            b.group("Titelseite", [
                b.task("Bildauswahl mit der Geschäftsführung abstimmen",
                       due=b.day(1), due_time="09:30", importance=2,
                       labels=b.ids("Kunde", "Freigabe offen")),
                b.task("Objektbezeichnung und Untertitel setzen"),
                b.task("Störer „Provisionsfrei\" platzieren", done=True),
            ], labels=b.ids("Kunde")),
            b.group("Innenseiten", [
                b.task("Grundrisse aufbereiten, Möblierung ergänzen", importance=2),
                b.task("Ausstattungsliste kürzen – aktuell zwei Seiten zu lang"),
                b.task("Energieausweis-Angaben einsetzen",
                       due=b.day(3), importance=3,
                       description="Pflichtangaben nach GEG §87: Energieträger, "
                                   "Baujahr, Endenergiebedarf, Effizienzklasse. "
                                   "Fehlt eine Angabe, ist die Anzeige abmahnfähig."),
                b.task("Lageplan mit Infrastruktur-Punkten anlegen", labels=b.ids("Kunde")),
            ]),
            b.group("Rückseite", [
                b.task("Kontaktdaten und Ansprechpartner aktualisieren"),
                b.task("QR-Code auf die Objektseite setzen", labels=b.ids("Web")),
            ]),

            b.heading("Produktion"),
            b.task("Reinzeichnung: Beschnitt, Überfüllung, Schwarzaufbau prüfen",
                   due=b.day(6), importance=3, labels=b.ids("Druck")),
            b.task("Druck-PDF nach PDF/X-4 exportieren", labels=b.ids("Druck")),
            b.task("Digitalproof anfordern und gegen den Bildschirm halten",
                   due=b.day(8), labels=b.ids("Druck")),
            b.task("Freigabe zum Druck schriftlich einholen",
                   due=b.day(9), importance=3, labels=b.ids("Freigabe offen")),
        ],
        folder=marketing, color="accent",
        note="Standardablauf für ein Objektexposé, 16 Seiten, Auflage 250. "
             "Von der Datenübernahme bis zur Druckfreigabe rechnen wir mit "
             "zwölf Arbeitstagen – die Freigabeschleifen sind darin enthalten.",
        labels=b.ids("Kunde", "Druck"),
    )

    b.listing(
        "Website & Social Media", [
            b.heading("Objektseiten"),
            b.task("Bildergalerie Parkquartier auf 12 Motive kürzen",
                   labels=b.ids("Web", "Foto")),
            b.task("Alt-Texte für alle Objektbilder nachtragen",
                   due=b.day(5), importance=2, labels=b.ids("Web"),
                   description="Barrierefreiheit und Auffindbarkeit. Kein "
                               "„Bild1.jpg\", sondern was zu sehen ist: "
                               "„Südfassade mit Loggien, Blick von der Parkseite\"."),
            b.task("Ladezeit prüfen – Startseite liegt bei 4,2 s",
                   importance=3, labels=b.ids("Web")),

            b.heading("Redaktionsplan"),
            b.group("Beitragsreihe „Vom Rohbau zum Quartier\"", [
                b.task("Teil 1: Baugrube und Gründung", done=True, labels=b.ids("Foto")),
                b.task("Teil 2: Rohbau Erdgeschoss", done=True, labels=b.ids("Foto")),
                b.task("Teil 3: Richtfest – Termin steht noch aus",
                       due=b.day(14), labels=b.ids("Foto")),
                b.task("Teil 4: Fassade und Fenster"),
            ]),
            b.note(
                "Tonalität für die Reihe:\n"
                "Sachlich, in der dritten Person, keine Superlative. Wir zeigen "
                "Bauabschnitte, keine Traumwelten – das Publikum sind Anwohner und "
                "künftige Käufer, die den Fortschritt beurteilen wollen.\n"
                "Bildunterschriften nennen immer Bauabschnitt und Monat.\n"
                "Keine Personen ohne Einverständnis, keine erkennbaren Kennzeichen.",
                labels=b.ids("Intern")),
            b.task("Beitragsbilder auf 1200 × 1200 zuschneiden", labels=b.ids("Web")),
            b.task("Veröffentlichung terminieren", due=b.day(-1), importance=2,
                   labels=b.ids("Web")),
        ],
        folder=marketing, color="clear",
        note="Objektseiten und begleitende Beiträge. Freigabe für Beiträge läuft "
             "über die Geschäftsführung, Bildrechte über das Sekretariat.",
        labels=b.ids("Web"),
    )

    # Unterordner: zeigt die Verschachtelung in der Seitenleiste
    kampagnen = b.folder("Kampagnen", "flag", parent=marketing)

    b.listing(
        "Frühjahrskampagne Parkquartier", [
            b.heading("Konzept"),
            b.task("Kernaussage festlegen", done=True, labels=b.ids("Kunde")),
            b.note(
                "Kernaussage, abgestimmt am Donnerstag:\n"
                "„Wohnen am Park – zehn Minuten in die Stadt.\"\n"
                "Die Lage ist das Argument, nicht die Ausstattung. Jede Anzeige, "
                "jedes Banner und jede Seite führt diesen Gedanken weiter; "
                "Ausstattungsmerkmale kommen erst im Exposé.",
                labels=b.ids("Kunde")),
            b.task("Mediaplan mit Budgetverteilung aufstellen",
                   due=b.day(4), importance=3, labels=b.ids("Intern")),

            b.heading("Umsetzung"),
            b.group("Printanzeigen", [
                b.task("Anzeige 1/1 Tageszeitung, Format 285 × 440",
                       due=b.day(7), labels=b.ids("Druck")),
                b.task("Anzeige 1/4 Stadtmagazin", labels=b.ids("Druck")),
                b.task("Daten an beide Verlage übermitteln", due=b.day(10)),
            ], labels=b.ids("Druck")),
            b.group("Außenwerbung", [
                b.task("Bauzaunbanner 6 × 1 m gestalten",
                       due=b.day(-3), importance=3, labels=b.ids("Druck", "Freigabe offen")),
                b.task("Montagetermin mit dem Bauleiter abstimmen"),
                b.task("Großfläche 18/1 – Motiv anpassen"),
            ]),
            b.group("Digital", [
                b.task("Landingpage aufsetzen", labels=b.ids("Web")),
                b.task("Anzeigenmotive in vier Seitenverhältnissen ausleiten",
                       description="1:1, 4:5, 9:16 und 16:9. Der Text muss in "
                                   "jedem Verhältnis vollständig sichtbar "
                                   "bleiben – nicht nur skalieren.",
                       labels=b.ids("Web")),
                b.task("Kontaktformular testen", done=True, labels=b.ids("Web")),
            ]),

            b.heading("Nachbereitung"),
            b.task("Reichweiten und Anfragen auswerten", due=b.day(35)),
            b.task("Kampagnenordner archivieren", labels=b.ids("Archiv")),
        ],
        folder=kampagnen, color="flag",
        note="Laufzeit acht Wochen ab Vermarktungsstart. Budget und Mediaplan "
             "liegen im Sekretariat, Motive in der Ablage unter 05_Kampagnen.",
        labels=b.ids("Kunde", "Druck", "Web"),
    )

    # ---------------------------------------------------------------
    # Ordner „Projekte"
    # ---------------------------------------------------------------
    projekte = b.folder("Projekte", "export",
                        "Ein Ordner je Bauvorhaben. Listen darin folgen immer "
                        "demselben Zuschnitt, damit man sich zurechtfindet.")
    parkquartier = b.folder("Neubau Parkquartier", None, parent=projekte)

    b.listing(
        "Vermarktungsstart", [
            b.heading("Vor dem Start"),
            b.task("Verkaufsunterlagen vollständig?", importance=3,
                   labels=b.ids("Freigabe offen")),
            b.task("Preisliste in der Endfassung erhalten", done=True),
            b.task("Musterwohnung fotografieren lassen",
                   due=b.day(11), due_time="08:00", labels=b.ids("Foto")),
            b.note(
                "Fototermin Musterwohnung – Vorbereitung:\n"
                "Termin morgens, das Licht kommt von Osten in den Wohnraum.\n"
                "Vorher: Baustellenstaub entfernen lassen, Fenster putzen, "
                "Etiketten von Armaturen und Scheiben ziehen.\n"
                "Mitbringen: Stellprobe Möbel, zwei Pflanzen, Textilien in Grau "
                "und Sand – keine kräftigen Farben, die datieren die Bilder.\n"
                "Aufnahmeliste: Wohnraum von zwei Seiten, Küche, Bad, Loggia, "
                "Blick aus dem Fenster nach Süden.",
                labels=b.ids("Foto")),

            b.heading("Startwoche"),
            b.group("Unterlagen versenden", [
                b.task("Interessentenliste aus onOffice bereinigen",
                       labels=b.ids("Intern")),
                b.task("Exposé als PDF beilegen, unter 8 MB halten"),
                b.task("Versandvorlage im System hinterlegen",
                       description="Betreffzeile, Anrede, Signatur und "
                                   "Datenschutzhinweis sind vorgegeben. "
                                   "Freitext nur im mittleren Block."),
            ]),
            b.task("Portale schalten: Objektdaten und Bilder hochladen",
                   due=b.day(13), importance=3, labels=b.ids("Web")),
            b.task("Verkaufsschild am Grundstück aufstellen", labels=b.ids("Druck")),

            b.heading("Danach"),
            b.task("Wöchentliche Anfragenübersicht einrichten", labels=b.ids("Intern")),
            b.task("Nachfassaktion nach vier Wochen planen", due=b.day(30)),
        ],
        folder=parkquartier, color="export",
        note="42 Wohneinheiten, drei Bauabschnitte. Verkaufsbeginn für den ersten "
             "Abschnitt ist beschlossen; die beiden weiteren folgen im Abstand "
             "von je einem Quartal.",
        labels=b.ids("Kunde"),
    )

    b.listing(
        "Baustellenkommunikation", [
            b.heading("Beschilderung"),
            b.task("Bauschild 3 × 2 m: Beteiligte prüfen und ergänzen",
                   due=b.day(-6), importance=3, labels=b.ids("Druck", "Freigabe offen"),
                   description="Bauherr, Architekt, Statik, Bauleitung, "
                               "ausführende Gewerke. Reihenfolge und Logogrößen "
                               "sind vertraglich geregelt – Vertrag liegt im "
                               "Projektordner."),
            b.task("Hinweisschilder für Zufahrt und Besucherparkplatz",
                   labels=b.ids("Druck")),
            b.task("Alte Schilder vom Vorgängerprojekt abbauen lassen", done=True),

            b.heading("Anwohner"),
            b.note(
                "Anwohnerinformation, Grundhaltung:\n"
                "Wir informieren vor der Störung, nicht danach. Ein Aushang "
                "zwei Wochen vor einer lauten Phase kostet nichts und verhindert "
                "die meisten Beschwerden.\n"
                "Jede Information nennt: was passiert, ab wann, wie lange, und "
                "wen man anrufen kann. Der letzte Punkt ist der wichtigste.\n"
                "Ton: nüchtern und konkret. Keine Entschuldigungsformeln, die "
                "nichts erklären.",
                labels=b.ids("Intern")),
            b.task("Aushang zur Spundwandphase entwerfen",
                   due=b.day(2), importance=2),
            b.task("Verteiler für die Nachbarschaft aktualisieren"),
            b.task("Ansprechpartner und Telefonnummer am Bauzaun anbringen",
                   importance=3),

            b.heading("Dokumentation"),
            b.task("Monatliche Baufortschrittsfotos vom selben Standpunkt",
                   labels=b.ids("Foto"),
                   description="Immer derselbe Standpunkt, dieselbe Brennweite, "
                               "möglichst dieselbe Tageszeit. Nur dann ergibt "
                               "die Reihe am Ende eine brauchbare Abfolge."),
            b.task("Bilder monatlich in die Projektablage sortieren",
                   labels=b.ids("Archiv")),
        ],
        folder=parkquartier, color="flag",
        note="Alles, was am Bauzaun, im Briefkasten oder am Schild steht. "
             "Verantwortlich gemeinsam mit der Bauleitung.",
        labels=b.ids("Intern"),
    )

    # ---------------------------------------------------------------
    # Ordner „Vorlagen & Standards"
    # ---------------------------------------------------------------
    standards = b.folder("Vorlagen & Standards", "clear",
                         "Was für alle Projekte gilt. Änderungen hier nur nach "
                         "Absprache – sonst driften die Projekte auseinander.")

    b.listing(
        "Corporate Design – Regelwerk", [
            b.heading("Farbe"),
            b.note(
                "Hausfarben:\n"
                "Dunkelblau #15243C – Grundfarbe für Flächen, Überschriften und "
                "Linien. Ersetzt seit der letzten Überarbeitung jedes reine "
                "Schwarz in Layouts.\n"
                "Warmgrau #6B6B66 – Fließtext auf hellem Grund, Bildunterschriften.\n"
                "Akzent Terrakotta #B4552D – ausschließlich für Handlungsaufrufe "
                "und Störer. Nie flächig, nie als Textfarbe für Fließtext.\n"
                "Papierweiß #F7F5F1 – Grundfläche in Print. Reines Weiß nur dort, "
                "wo der Bedruckstoff es ohnehin vorgibt."),
            b.task("Farbwerte in CMYK und Pantone gegenprüfen lassen",
                   due=b.day(20), labels=b.ids("Druck")),
            b.task("Farbfelder in die InDesign-Vorlagen übernehmen", done=True),

            b.heading("Schrift"),
            b.note(
                "Schriftfamilien:\n"
                "Überschriften in der halbfetten Schnittweite, Laufweite leicht "
                "negativ, Versalien nur bis vier Wörter.\n"
                "Fließtext 9,5 pt auf 14 pt Zeilenabstand in Print, 17 px auf "
                "27 px im Web.\n"
                "Zahlen in Tabellen immer als Versalziffern, im Fließtext als "
                "Mediävalziffern – sonst stören sie das Schriftbild.\n"
                "Keine dritte Schrift. Wo eine Auszeichnung nötig ist, arbeiten "
                "wir mit Schnitt und Größe, nicht mit einer weiteren Familie."),
            b.task("Weblizenz für die Hausschrift verlängern",
                   due=b.day(45), importance=2, labels=b.ids("Web")),

            b.heading("Logo"),
            b.note(
                "Logoanwendung:\n"
                "Schutzraum ringsum entspricht der Höhe des Wortmarken-Versal.\n"
                "Mindestbreite 24 mm in Print, 120 px im Web – darunter wird die "
                "Bildmarke allein verwendet.\n"
                "Auf Bildern nur die einfarbige Fassung, hell oder dunkel je nach "
                "Untergrund. Keine Schatten, keine Konturen, keine Verläufe.\n"
                "Das Logo wird nicht gedreht, nicht verzerrt und nicht "
                "eingefärbt."),
            b.task("Logodateien in allen Formaten neu ausleiten",
                   labels=b.ids("Archiv")),
            b.task("Alte Logofassung aus dem Serverordner entfernen",
                   labels=b.ids("Archiv")),

            b.heading("Bildsprache"),
            b.note(
                "Bildsprache:\n"
                "Architektur immer mit Umgebung – ein Haus ohne Kontext sagt "
                "nichts über die Lage, und die Lage ist unser Argument.\n"
                "Menschen im Bild sind erwünscht, aber nicht gestellt und nie im "
                "Anschnitt der Bildmitte.\n"
                "Himmel: leicht bewölkt bevorzugt. Ein makellos blauer Himmel "
                "wirkt gerendert, auch wenn er echt ist.\n"
                "Keine Weitwinkelverzerrung in Innenräumen über 24 mm "
                "Kleinbildäquivalent.\n"
                "Nachbearbeitung zurückhaltend: Perspektive korrigieren, "
                "Weißabgleich neutral, Sättigung unverändert."),
        ],
        folder=standards, color="accent",
        note="Verbindlich für alle Drucksachen, Anzeigen und Webauftritte. "
             "Wer davon abweichen will, klärt das vorher – nicht in der "
             "Korrekturschleife.",
        labels=b.ids("Intern", "Kunde"),
    )

    b.listing(
        "Druckdatenprüfung", [
            b.note(
                "Diese Liste wird vor jeder Datenübergabe von oben nach unten "
                "abgearbeitet.\n"
                "Sie ersetzt keinen Preflight, sondern fängt das ab, was ein "
                "Preflight nicht sieht: falsches Endformat, fehlende "
                "Pflichtangaben, ein Schwarz, das technisch stimmt und trotzdem "
                "falsch aufgebaut ist.\n"
                "Wer abhakt, hat geprüft – nicht angenommen."),
            b.heading("Dokument"),
            b.task("Endformat und Beschnitt stimmen mit der Bestellung überein",
                   importance=3),
            b.task("3 mm Beschnittzugabe ringsum vorhanden"),
            b.task("Sicherheitsabstand zum Rand eingehalten (mind. 5 mm)"),
            b.task("Seitenzahl durch vier teilbar (nur bei Broschüren)"),

            b.heading("Farbe"),
            b.task("Alle Elemente in CMYK, keine RGB-Reste", importance=3,
                   labels=b.ids("Druck")),
            b.task("Sonderfarben entweder eingebaut oder umgewandelt"),
            b.task("Schwarzaufbau geprüft: Text 100 K, Flächen als Tiefschwarz",
                   description="Tiefschwarz bei uns: 60/40/40/100. Fließtext "
                               "niemals mehrfarbig aufbauen – jede Passerdifferenz "
                               "wird sonst sichtbar."),
            b.task("Gesamtfarbauftrag unter 300 %"),

            b.heading("Bilder und Schrift"),
            b.task("Bildauflösung mindestens 300 dpi im Endformat", importance=2),
            b.task("Keine verknüpften Bilder fehlend oder verändert"),
            b.task("Schriften eingebettet oder in Pfade gewandelt", importance=3),
            b.task("Haarlinien unter 0,25 pt beseitigt"),

            b.heading("Übergabe"),
            b.task("Export als PDF/X-4, Profil geprüft", labels=b.ids("Druck")),
            b.task("Dateiname nach Schema: Projekt_Produkt_Datum_Version"),
            b.task("Freigabevermerk im Projektordner abgelegt",
                   labels=b.ids("Freigabe offen")),
        ],
        folder=standards, color="export",
        note="Checkliste vor jeder Druckfreigabe. Ein einziger übersehener Punkt "
             "kostet im Zweifel die gesamte Auflage.",
        labels=b.ids("Druck"),
    )

    b.listing(
        "Textbausteine & Tonalität", [
            b.heading("Grundsätze"),
            b.note(
                "Wie wir schreiben:\n"
                "Kurze Sätze, aktive Formulierungen, keine Substantivketten.\n"
                "Konkret statt werblich: „zehn Minuten zum Hauptbahnhof\" statt "
                "„hervorragende Verkehrsanbindung\".\n"
                "Keine Superlative, die wir nicht belegen können. „Einzigartig\" "
                "ist fast nie wahr und immer austauschbar.\n"
                "Zahlen nennen: Quadratmeter, Baujahr, Entfernungen, Kosten. "
                "Wer Zahlen liest, glaubt den Rest eher."),
            b.task("Formulierungsliste um die Rückmeldungen aus dem Vertrieb ergänzen",
                   due=b.day(16), labels=b.ids("Intern")),

            b.heading("Bausteine"),
            b.group("Objektbeschreibung", [
                b.task("Einleitung Lage (drei Varianten: Stadt, Rand, Land)"),
                b.task("Absatz Ausstattung – modular nach Standard und gehoben"),
                b.task("Absatz Energie und Technik", done=True),
            ]),
            b.group("E-Mail-Vorlagen", [
                b.task("Erstkontakt nach Anfrage über ein Portal"),
                b.task("Terminbestätigung Besichtigung"),
                b.task("Nachfassen nach Besichtigung", done=True),
                b.task("Absage bei vergebener Einheit – freundlich und kurz"),
            ], labels=b.ids("Intern")),

            b.heading("Pflichtangaben"),
            b.task("Energieausweis-Formulierung juristisch prüfen lassen",
                   due=b.day(25), importance=3, labels=b.ids("Freigabe offen")),
            b.task("Widerrufsbelehrung in der aktuellen Fassung hinterlegen"),
            b.task("Impressumsangaben auf allen Kanälen abgleichen",
                   labels=b.ids("Web")),
        ],
        folder=standards, color="due_action",
        note="Wiederverwendbare Texte. Wer einen Baustein ändert, ändert ihn "
             "hier – nicht im einzelnen Dokument.",
        labels=b.ids("Intern"),
    )

    # --- Liste ohne Ordner und ohne Labels: zeigt den ruhigen Kopfbereich ---
    b.listing(
        "Ablage & Ideen", [
            b.task("Papiermuster-Ordner sortieren"),
            b.task("Schriftmuster der letzten Messe einscannen"),
            b.note(
                "Notiz an mich:\n"
                "Die Vorlagen für Baustellenschilder liegen in drei Fassungen "
                "auf dem Server, zwei davon veraltet. Vor der nächsten Bestellung "
                "aufräumen, sonst greift wieder jemand zur falschen."),
            b.task("Farbfächer nachbestellen", done=True),
        ],
        color=None,
        note="Was keinen Platz hat und trotzdem nicht verloren gehen soll.",
    )

    # Aktuelle Funktionen an einem direkt prüfbaren Unternehmensablauf.
    workflow_folder = b.folder("Website-Betrieb", "clear", "Wöchentliche Pflege und nachvollziehbare Übergabe einer Unternehmenswebsite.", labels=b.ids("Web"))
    checks = b.listing("Wartung und Freigaben", [
        b.heading("Wiederkehrende Qualitätssicherung"),
        b.task("Kontaktformular und Anfragezustellung testen", due=b.day(1), due_time="09:00",
               repeat={"art": "woechentlich"}, importance=2, labels=b.ids("Web"),
               description="Testanfrage mit künstlichen Daten absenden, Zustellung und Fehlermeldung prüfen. Beim Abhaken wandert die Fälligkeit zur nächsten Woche."),
        b.task("Freigaben und offene Inhalte nachhalten", due=b.day(2),
               repeat={"art": "tage", "abstand": 14, "ende": b.day(84)}, labels=b.ids("Freigabe offen"),
               description="Bestätigte Text- und Bildstände gegen die Website abgleichen. Beispielregel: alle 14 Tage, für 12 Wochen."),
        b.group("Neue Vorlagen und Bedienwege prüfen", [
            b.task("Vorlage WordPress-Relaunch importieren und bearbeiten", description="Vorlagen → Vorlagen hinzufügen: die mitgelieferte .glidetemplates-Datei auswählen. Bearbeiten → Vorlagendetails bietet Farbe, Labels und Anhänge."),
            b.task("Punktdetails und verschachtelte Unterpunkte bearbeiten", description="Im Vorlageneditor einen Punkt markieren und Bearbeiten öffnen. Art, Wichtigkeit, Fälligkeit, Uhrzeit, Wiederholung, Labels, Beschreibung und Anhänge prüfen."),
            b.task("Abbruch und erneuten Aufruf prüfen", description="Einen Entwurf ändern und Abbrechen wählen. Die Vorlage muss unverändert bleiben. Erst Übernehmen und Vorlagen speichern schreiben den Katalog."),
            b.task("Mac-Trackpad auf Startseite und Diagrammen testen", description="Mit zwei Fingern über Text, Schaltflächen und Jahresraster in beide Richtungen scrollen; auch kleine Bewegungen prüfen."),
            b.task("Listenübersicht bei kleiner Fensterbreite prüfen", description="Ein bis drei Spalten, getrennte nächste Aufgaben und unten erreichbare Aktionen prüfen."),
        ]),
    ], folder=workflow_folder, color="clear", note="Praxisprobe für Wiederholungen, Vorlagendetails, Anhänge und Scrollen.", labels=b.ids("Web"))
    # Drei kleine echte Dateien zeigen den Rundlauf auf allen Besitzerebenen.
    #
    # ``newline="\n"`` ist hier nicht Geschmack, sondern Bedingung: Ohne diese
    # Angabe übersetzt der Textmodus jeden Zeilenumbruch in den der Plattform,
    # und unter Windows wächst jede Datei um ein Byte je Zeile. Der
    # Beispieldaten-Abgleich vergleicht auch die Anhanggrößen und konnte dort
    # deshalb nie gleich ausfallen – aufgefallen ist es erst im ersten
    # Windows-Vollprüflauf, weil es vorher keinen gab.
    with tempfile.TemporaryDirectory(prefix="glide-example-files-") as source_dir:
        for owner, name, content in (
            (app.get_folder(workflow_folder), "Projektbriefing.txt", "Projektkennung: Demo\nVerantwortung: intern ergänzen\nFreigabeweg: intern abstimmen\n"),
            (checks, "Pflegecheckliste.txt", "Formularzustellung prüfen\nInhalte aktualisieren\nFreigabe dokumentieren\n"),
            (checks["items"][1], "Formulartest.txt", "Nur künstliche Kontaktdaten verwenden. Ergebnis und Datum dokumentieren.\n"),
        ):
            source = pathlib.Path(source_dir) / name
            source.write_text(content, encoding="utf-8", newline="\n")
            owner["attachments"] = [app.store_attachment(str(source))]

    # --- Kalender, Erinnerungen und Tagesplanung -------------------------
    # Diese Liste ist der Prüfbestand für alles, was seit 3.14 hinzugekommen
    # ist. Vorher deckte die Datei Erinnerungen überhaupt nicht ab, führte nur
    # einen Bearbeitungstag und einen Aufwand und kannte von den sechs
    # Wiederholungsarten nur zwei – die Tagesplanung liess sich damit nicht
    # sinnvoll ausprobieren und der ICS-Rundlauf nur zur Haelfte.
    planung_liste = b.listing("Kalender, Erinnerungen und Tagesplanung", [
        b.heading("Tagesplanung: ein vollständig verplanter Tag"),
        # Vier Punkte auf denselben Bearbeitungstag, Summe 225 Minuten. Damit
        # zeigt die Tagesplanung eine echte Summe und die Tageskapazität
        # (Einstellungen, Vorgabe 0 = kein Vergleich) einen echten Vergleich.
        b.task("Grundrisse Parkquartier zeichnen", planned_date=b.day(0),
               estimated_minutes=90, due=b.day(4), importance=3, labels=b.ids("Foto"),
               description="Aufwand 90 Minuten, Bearbeitungstag heute, Fälligkeit später – die drei Felder sind absichtlich verschieden."),
        b.task("Bildauswahl mit der Redaktion abstimmen", planned_date=b.day(0),
               estimated_minutes=60, due=b.day(2), due_time="14:30", labels=b.ids("Foto"),
               description="Termin mit Uhrzeit: So entsteht beim Kalenderexport ein Zeittermin, kein Ganztagstermin."),
        b.task("Korrekturen aus der Freigabe einarbeiten", planned_date=b.day(0),
               estimated_minutes=45, labels=b.ids("Freigabe offen"),
               description="Bearbeitungstag ohne Fälligkeit – erlaubt und in der Tagesplanung sichtbar."),
        b.task("Exposé gegenlesen", planned_date=b.day(0), estimated_minutes=30, done=True,
               description="Erledigt und trotzdem in der Tagessumme: So ist die Rechenregel aus 3.15 festgelegt."),
        b.task("Angebot ohne Schätzung", planned_date=b.day(0), labels=b.ids("Kunde"),
               description="Ohne Aufwand: Die Tagesplanung zählt solche Punkte getrennt aus."),
        b.task("Nächster Tag zum Umschalten", planned_date=b.day(1),
               estimated_minutes=120, description="Liegt auf morgen, damit der Tageswechsel etwas zu zeigen hat."),

        b.heading("Erinnerungen: beide Arten"),
        # Vorher enthielt die Datei keine einzige Erinnerung, obwohl die
        # Anleitung das Gegenteil behauptete. Beide Arten werden gebraucht:
        # relativ wird beim Kalenderexport ein Alarm mit Abstand, fest ein
        # Alarm mit Zeitpunkt.
        b.task("Rückruf Bauträger", due=b.day(1), due_time="10:00",
               reminder={"mode": "relative", "minutes": 30}, importance=3, labels=b.ids("Kunde"),
               description="Relative Erinnerung, 30 Minuten vor dem Termin. Im Kalenderexport wird daraus TRIGGER:-PT30M."),
        b.task("Angebotsfrist Parkquartier", due=b.day(5),
               reminder={"mode": "fixed", "at": app.local_reminder_time(b.day(4), "08:00")},
               importance=2, labels=b.ids("Kunde"),
               description="Feste Erinnerung am Vortag um 8 Uhr. Gespeichert wird sie in UTC, angezeigt in Ortszeit."),

        b.heading("Wiederholungen: alle abbildbaren Arten"),
        # Erst mit diesen vier Punkten deckt die Datei alle Arten ab, die der
        # Kalenderexport als RRULE schreiben und der Import zurücklesen kann.
        b.task("Backup der Arbeitsdateien prüfen", due=b.day(1),
               repeat={"art": "taeglich"}, labels=b.ids("Web"),
               description="Täglich – im Kalenderexport FREQ=DAILY."),
        b.task("Baustellenbegehung Mo und Mi", due=b.day(1), due_time="07:30",
               repeat={"art": "wochentage", "tage": [0, 2], "ende": b.day(140)},
               importance=2, labels=b.ids("Foto"),
               description="Bestimmte Wochentage MIT Enddatum. Genau dieser Fall verschob sich bis 3.21.0 beim Rundlauf um einen Tag, weil UNTIL in UTC geschrieben wurde."),
        b.task("Monatsabschluss Belege sortieren", due=b.day(12),
               repeat={"art": "monatlich"}, labels=b.ids("Freigabe offen"),
               description="Monatlich – FREQ=MONTHLY."),
        b.task("Jahresabgleich Bildrechte", due=b.day(30),
               repeat={"art": "jaehrlich"}, importance=1,
               description="Jährlich – FREQ=YEARLY. Zusammen mit den drei Punkten darüber und der 14-Tage-Regel in „Wartung und Freigaben\" sind alle sechs Arten vertreten."),

        b.heading("Kalenderrundlauf zum Ausprobieren"),
        b.note(
            "So prüft man den Rundlauf aus 3.20 und 3.21 mit dieser Liste:\n"
            "1. Diese Liste öffnen, Datei → Kalenderausgabe als ICS, Umfang „Aktuelle Liste\".\n"
            "2. Die Datei in einem Texteditor ansehen: Ganztags- und Zeittermine, RRULE je\n"
            "   Wiederholungsart, VALARM für beide Erinnerungen. UNTIL steht ohne „Z\".\n"
            "3. Datei → Kalenderdatei (ICS) importieren, dieselbe Datei wählen. Der Bericht\n"
            "   muss alle Termine als Duplikate überspringen – die eigenen UIDs werden erkannt.\n"
            "4. Zum Gegentest die UIDs im Editor ersetzen und erneut importieren: Jetzt\n"
            "   entstehen Aufgaben, und das Enddatum der Serie muss der 140. Tag bleiben.",
            labels=b.ids("Web"),
        ),
    ], folder=workflow_folder, color="import",
        note="Prüfbestand für Tagesplanung, Erinnerungen, Wiederholungen und den Kalenderrundlauf.",
        labels=b.ids("Web"))
    # Ein Anhang an dieser Liste zeigt, dass Anhänge und Kalenderausgabe
    # einander nicht behindern: Die Ausgabe ist rein lesend.
    with tempfile.TemporaryDirectory(prefix="glide-example-cal-") as cal_dir:
        quelle = pathlib.Path(cal_dir) / "Kalenderpruefung.txt"
        quelle.write_text(
            "Rundlauf: exportieren, ansehen, importieren, Duplikate prüfen.\n"
            "Enddatum der Serie muss erhalten bleiben – auch in anderen Zeitzonen.\n",
            encoding="utf-8",
            newline="\n",
        )
        planung_liste["attachments"] = [app.store_attachment(str(quelle))]

    # --- Zeichnung (Format 19): eine kleine, feste Pixelskizze. Sie zeigt die
    # Listenart im Ordner und reist durch Backup und Wiederherstellung.
    skizze = mod.glide_drawing.DrawingModel.blank()
    for x in range(32, 97):
        skizze.set_cell(x, 96, "#2B2B2B")
        skizze.set_cell(x, 60, "#2B2B2B")
    for y in range(60, 97):
        skizze.set_cell(32, y, "#2B2B2B")
        skizze.set_cell(96, y, "#2B2B2B")
    for step in range(33):
        skizze.set_cell(32 + step, 60 - step, "#B03A2E")
        skizze.set_cell(96 - step, 60 - step, "#B03A2E")
    skizze.fill(64, 80, "#F4D58D")
    for x in range(56, 73):
        for y in range(76, 97):
            skizze.set_cell(x, y, "#5B7DB1")
    zeichnung = app.new_list_object(
        "Skizze Musterhaus", [], None, workflow_folder, None,
        "Pixelskizze mit 128 × 128 Zellen. Bearbeitbar mit Pinsel, Füllen und Pipette.", None, [],
        list_kind="drawing", drawing=skizze.to_document(),
    )
    app.lists.append(zeichnung)

    # --- Papierkorb: eine gelöschte Liste, ein Ordner und ein einzelner Punkt
    geloeschte_liste = app.new_list_object(
        "Kampagne Herbst (abgesagt)", [], None, None, "delete",
        "Wurde zugunsten der Frühjahrskampagne zurückgestellt.", None, [],
    )
    geloeschte_liste["items"][:] = [
        b.task("Motive sichten"),
        b.task("Budget anmelden", done=True),
    ]
    app.trash.append(app.new_trash_entry(app.TRASH_KIND_LIST, geloeschte_liste))

    alter_ordner = app.new_folder_object("Archiv 2024", None, "due_action")
    app.trash.append(app.new_trash_entry(app.TRASH_KIND_FOLDER, alter_ordner))

    verworfener_punkt = b.task(
        "Anzeigenmotiv mit Luftbild – vom Kunden abgelehnt",
        importance=1, labels=b.ids("Kunde"),
    )
    app.trash.append(
        app.new_trash_entry(
            app.TRASH_KIND_ITEM, verworfener_punkt,
            origin={"list_id": app.lists[0].get("id"), "parent_id": None, "index": 0},
        )
    )

    # Art und festes Label müssen deckungsgleich sein, bevor gespeichert wird.
    app.sync_all_item_kind_labels()
    # Beim Import soll die erste inhaltliche Liste offen sein, nicht der Eingang:
    # Wer die Datei einliest, will sehen, was drin ist.
    b.open_list(next(entry for entry in app.lists if entry["title"].startswith("Exposé")))
    app.save_items()
    return app.complete_backup_payload()


def summarise(app):
    """Kennzahlen des erzeugten Bestands – der Beleg, dass er wirklich voll ist."""
    kinds = {}
    tasks = 0
    for entry in app.lists:
        for item in app.walk_items(entry.get("items", [])):
            kind = app.item_kind(item)
            kinds[kind] = kinds.get(kind, 0) + 1
            tasks += 1
    return {
        "Ordner": len(app.folders),
        "Listen": len(app.lists),
        "Punkte gesamt": tasks,
        "davon Aufgaben": kinds.get(app.ITEM_KIND_TASK, 0),
        "davon Gruppen": kinds.get(app.ITEM_KIND_GROUP, 0),
        "davon Long-Tasks": kinds.get(app.ITEM_KIND_LONG, 0),
        "davon Überschriften": kinds.get(app.ITEM_KIND_HEADING, 0),
        "Labels": len(app.labels),
        "Papierkorb": len(app.trash),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ziel", default=str(DEFAULT_TARGET))
    args = parser.parse_args()

    target = pathlib.Path(args.ziel).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_root:
        mod = load_module(pathlib.Path(temp_root) / "Glide")
        root = mod.tk.Tk()
        root.withdraw()
        app = mod.ListApp(root)
        root.update_idletasks()

        payload = build(app, mod)
        app.write_complete_backup(str(target), payload)

        print(f"Geschrieben: {target}")
        for name, value in summarise(app).items():
            print(f"  {value:4d}  {name}")
        root.destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
