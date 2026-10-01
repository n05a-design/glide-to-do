#!/usr/bin/env python3
"""Erzeugt und prüft die drei Arbeitslisten zur Releaseplanung von Glide 3.5.0.

Aufruf: python tests/tools/releasedaten.py [--ziel PFAD] [--stichtag JJJJ-MM-TT]
       [--screenshot PFAD.png] (Windows: hell und dunkel)

Das Komplettbackup ersetzt beim Einlesen den gesamten Bestand. Zum Ausprobieren
eine getrennte, über GLIDE_DATA_DIR isolierte Ablage verwenden. Alle Fristen sind
Planungsvorschläge relativ zum Erzeugungstag, keine beschlossenen Releasetermine.
Die Webquellen wurden am 04.09.2026 gelesen; ein neuer Erzeugungslauf aktualisiert
nur Planungsfristen, nicht den belegten Recherche- oder Funktionsstand.
"""

from __future__ import annotations

import argparse
import ctypes
from datetime import date
import json
import pathlib
import os
import struct
import sys
import tempfile
import zipfile
import zlib

from beispieldaten import Builder, REPOSITORY_ROOT, load_module, summarise


APP_VERSION = "3.5.0"
RESEARCH_DATE = "2026-09-04"
DEFAULT_TARGET = REPOSITORY_ROOT / "tests/fixtures/beispiele/glide_releaseplanung_3.5.0.glidebackup"
LIST_TITLES = ("Unterlagen & Assets", "Vermarktungsstrategie", "Feature-Übersicht")

SOURCES = {
    "win_icon": "https://learn.microsoft.com/en-us/windows/apps/design/style/iconography/app-icon-construction",
    "mac_icon": "https://developer.apple.com/library/archive/documentation/Xcode/Reference/xcode_ref-Asset_Catalog_Format/IconSetType.html",
    "mac_icon_build": "https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html",
    "win_shots": "https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/screenshots-and-images",
    "msix_shots": "https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/screenshots-and-images",
    "mac_shots": "https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/",
    "win_text": "https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/add-and-edit-store-listing-info",
    "win_keywords": "https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/add-on/write-great-app-description",
    "mac_info": "https://developer.apple.com/help/app-store-connect/reference/app-information/app-information",
    "mac_text": "https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/",
    "win_sign": "https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/app-package-requirements",
    "mac_sign": "https://developer.apple.com/developer-id/",
    "mac_notary": "https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution",
    "mac_review": "https://developer.apple.com/app-store/review/guidelines/",
    "mac_privacy": "https://developer.apple.com/app-store/app-privacy-details/",
    "win_age": "https://learn.microsoft.com/de-de/windows/apps/publish/publish-your-app/msi/age-ratings",
    "imprint": "https://www.gesetze-im-internet.de/ddg/__5.html",
    "things": "https://culturedcode.com/things/support/articles/2803586/",
    "taskcoach": "https://taskcoach.org/features.html",
    "todotxt": "https://benrhughes.github.io/todotxt.net/",
    "todotxtmac": "https://mjdescy.github.io/TodoTxtMac/",
}


def web(text, *keys):
    return text + "\n\nRecherchiert; Abrufdatum: " + RESEARCH_DATE + "\n" + "\n".join(
        "Quelle: " + SOURCES[key] for key in keys
    )


def code(text, *names):
    return text + "\n\nCodebeleg: src/glide/app.pyw – " + ", ".join(names) + ". Stand: 3.5.0 / Datenformat 11."


class ReleaseBuilder(Builder):
    def __init__(self, app, today):
        super().__init__(app)
        self.today = today

    def todo(self, text, description, *labels, days=None, importance=0):
        labels = list(labels)
        if days is not None:
            description += f"\n\nPlanungsvorschlag: {days} Tage nach Erzeugungsstichtag {self.today.isoformat()}; kein zugesagter Termin. Nach Freigabe anpassen."
            if "Annahme" not in labels:
                labels.append("Annahme")
        return self.task(text, description=description, labels=self.ids(*labels),
                         due=self.day(days) if days is not None else None,
                         importance=importance)

    def memo(self, text, description, *labels):
        return self.note(text, description=description, labels=self.ids(*labels))

    def feature(self, text, description, *names):
        return self.task(text, description=code(description, *names))


def assets(b):
    return [
        b.heading("Start und Freigaben"),
        b.memo("Releaseplanung für Glide 3.5.0\nDatenformat 11 · Recherche 04.09.2026\nDrei Arbeitslisten in einer Sicherung", 
               "Diese Datei enthält Arbeitsmaterial, keine Veröffentlichung. Ein Komplettbackup ersetzt den gesamten aktuellen Bestand. Vorher eigenes Komplettbackup erstellen; zum Prüfen GLIDE_DATA_DIR auf eine getrennte Ablage setzen. Fristen sind Vorschläge. Store-Kanäle, Identitäten, Lizenz und Preis bleiben Inhaberentscheidungen. Die Häkchen der Featureliste dienen der redaktionellen Übernahme, nicht als Nachweis einer Plattformfreigabe."),
        b.todo("Vertriebswege und erste Zielarchitekturen freigeben lassen",
               "Inhaberentscheidung: Direktdownload, Microsoft Store und/oder Mac App Store. Die Anforderungen unterscheiden sich. Windows und macOS sind gleichwertige Produktziele, aber ein Einreichungsdatum ist nicht beschlossen. Windows-Zielarchitektur und macOS-Minimum erst anhand echter Builds und Gerätetests festlegen.", "Blocker", days=2, importance=3),
        b.group("Produkt- und Plattformidentität", [
            b.todo("Publisher und Copyright-Zeile verbindlich eintragen", "Inhaberentscheidung offen. Genaue juristische Anbieterbezeichnung, Rechteinhaber und Jahr klären; keine Platzhalter veröffentlichen. Beleg: docs/decisions/PRODUCT_IDENTITY.md.", "Blocker", "Recht"),
            b.todo("Support-E-Mail und erreichbare Supportseite festlegen", web("Inhaberentscheidung offen. Apple verlangt eine Support-URL mit tatsächlicher Kontaktmöglichkeit. Adresse und Zuständigkeit vor Freigabe testen.", "mac_text"), "Blocker", "Text"),
            b.todo("Website und Datenschutz-URL festlegen", web("Inhaberentscheidung offen. Für Apple muss die Datenschutzerklärung öffentlich über eine URL erreichbar sein. Domain und Betreiberangaben nicht erfinden.", "mac_privacy"), "Blocker", "Recht"),
            b.todo("Lizenzmodell und Preis freigeben lassen", "Inhaberentscheidung offen. Optionen und Folgen stehen in der Vermarktungsstrategie. Im Code gibt es keinen Lizenzserver oder Aboverwaltung; diese Funktionen nicht voraussetzen. Beleg: docs/01_PRODUCT_CONSTRAINTS.md.", "Blocker", "Recht"),
            b.todo("Windows AppUserModelID und Inno-Setup-AppId vergeben lassen", "Stabile technische Identitäten nach Publisher- und Namensentscheidung in PRODUCT_IDENTITY.md festhalten; keine neuen IDs aus einem geratenen Publisher ableiten. Upgradepfad anschließend testen.", "Blocker", "Windows"),
            b.todo("macOS Bundle Identifier vergeben lassen", "Stabiler eindeutiger Identifier nach Anbieter- und Domainentscheidung. Beleg: docs/decisions/PRODUCT_IDENTITY.md. Danach konsistent in Build, Signatur und Store verwenden.", "Blocker", "macOS"),
            b.todo("Nutzbarkeit des Namens Glide fachlich prüfen lassen", "Markenrisiko und Verwechslungen offen. Relevante Länder, Waren-/Dienstleistungsklassen, Namen und Domains professionell prüfen lassen; eine Store-Namensreservierung ersetzt keine Markenfreigabe. Ergebnis mit Datum und Verantwortlichem dokumentieren.", "Blocker", "Recht"),
        ]),
        b.heading("Grafik und Screenshots"),
        b.group("Anwendungssymbole aus dem freigegebenen Master", [
            b.todo("Windows-ICO mit fünf Mindestgrößen ausleiten", web("Für Win32 ein mehrteiliges .ico mit 16, 24, 32, 48 und 256 px je Kante herstellen. Jede Größe in kleiner Originalansicht prüfen; nicht nur das 256-px-Motiv skalieren. MSIX-Manifest-Assets sind ein zusätzlicher, paketabhängiger Satz.", "win_icon"), "Windows", "Grafik", days=7),
            b.todo("macOS-Iconset und .icns herstellen", web("Für die klassische .icns-Buildroute PNG-Paare für 16, 32, 128, 256 und 512 Punkte anlegen, jeweils @1x und @2x: effektive Pixelkanten 16/32/64/128/256/512/1024. Mit iconutil zum .icns bündeln. Die verlinkten Apple-Seiten sind archivierte technische Formatspezifikationen; aktuelle Gestaltung und Kompatibilität vor Einreichung am gewählten macOS/Xcode prüfen.", "mac_icon", "mac_icon_build"), "macOS", "Grafik", days=7),
            b.todo("Wortmarke und Logo als neutrale Masterdateien ausleiten", "Produktionsvorschlag: editierbarer Vektormaster plus SVG und PDF; PNG für helle/dunkle Hintergründe, jeweils transparent und mit definierter Fläche. Wortmarke, Bildmarke und Kombination getrennt. Kein Logoentwurf wird hier freigegeben. Exportgrößen aus den bestätigten Zielmedien ableiten.", "Grafik", "Annahme", days=7),
            b.todo("Microsoft Store Box Art separat herstellen", web("MSI/EXE verlangt 1:1 Box Art; 2:3 Poster Art wird empfohlen. Die aktuelle Seite nennt keine verbindlichen Pixelabmessungen. Diese deshalb im Partner-Center-Formular prüfen und vor dem finalen Export dokumentieren.", "win_shots"), "Windows", "Grafik", "Annahme"),
        ]),
        b.group("Aufnahmen aus der echten Zielplattform", [
            b.todo("Windows-Screenshots mit Testdaten aufnehmen", web("Für MSI/EXE: mindestens 1, höchstens 10; Empfehlung 4 oder mehr. Szenen: Arbeitsliste, Details/Anhänge, Kalender, dunkle Ansicht. Die aktuelle MSI/EXE-Seite nennt keine Pixelmaße: Mindestauflösung vor Upload in Partner Center verifizieren. Produktionsvorschlag bis dahin: 1920 × 1080. Nur die MSIX-Seite nennt Desktop mindestens 1366 × 768; diese Zahl nicht als bestätigte MSI/EXE-Pflicht ausgeben.", "win_shots", "msix_shots"), "Windows", "Grafik", "Annahme", days=14),
            b.todo("Mac-App-Store-Screenshots in erlaubtem 16:10-Raster aufnehmen", web("1–10 Aufnahmen, JPEG oder PNG ohne Alpha/Transparenz. Mac erlaubt exakt 1280 × 800, 1440 × 900, 2560 × 1600 oder 2880 × 1800. Aufnahme am Mac mit tatsächlich laufendem Build. Empfohlene Motivauswahl wie Windows; keine Linux-Aufnahme als macOS ausgeben.", "mac_shots"), "macOS", "Grafik", days=14),
            b.todo("Sichtprüfung und Store-Material getrennt freigeben", "tests/tools/screenshots.py erzeugt technische Sichtprüfungen. Diese ersetzen keine Aufnahme und Freigabe des ausgelieferten Builds unter Windows bzw. macOS. Schrift, Symbole, echte Menüleiste, Dialoge und die gewählte Skalierung prüfen. Nur künstliche Daten verwenden.", "Grafik", days=14),
        ]),
        b.heading("Store-Texte und rechtliche Arbeitsunterlagen"),
        b.group("Texte aus der Feature-Übersicht ableiten", [
            b.todo("Microsoft-Store-Texte innerhalb der Grenzen verfassen", web("MSI/EXE: Beschreibung höchstens 10.000 Zeichen, Kurzbeschreibung höchstens 1.000 (unter 270 empfohlen), bis zu 20 Features à 200 Zeichen. Neuerungen höchstens 1.500 Zeichen; bei erster Einreichung leer lassen. Interne App-Version bleibt 3.5.0, auch wenn es die erste Store-Einreichung ist.", "win_text"), "Windows", "Text", days=10),
            b.todo("Microsoft-Suchbegriffe im gewählten Einreichungsweg prüfen", web("Microsoft nennt allgemein bis zu 7 Suchbegriffe mit jeweils 30 Zeichen. Die MSI/EXE-Textseite listet kein eigenes Keywordfeld. Vor Einplanung im aktuellen Formular bestätigen; Begriffe wie lokale Aufgaben, Listen und offline nur passend zur App verwenden.", "win_keywords", "win_text"), "Windows", "Text", "Annahme"),
            b.todo("Mac-App-Store-Texte und Keywords vorbereiten", web("Name und Untertitel jeweils höchstens 30 Zeichen. Beschreibung höchstens 4.000 Zeichen. Keywords laut aktueller Referenz zusammen höchstens 100 Bytes, nicht 100 Zeichen; Umlaute bei UTF-8 mitzählen. Neuerungen höchstens 4.000 Zeichen, für die erste Store-Version nicht verfügbar. Untertitel als Kurztext nutzen; ein zusätzliches Promo-Feld nicht ohne Mac-Formularprüfung voraussetzen.", "mac_info", "mac_text"), "macOS", "Text", days=10),
            b.todo("Installations-, Backup- und Restore-Kurzanleitung freigeben", code("Einstieg ohne Konto erklären, Datenordner nennen, komplettes Backup vor einem Import empfehlen und das Ersetzen sämtlicher Listen ausdrücklich nennen. TXT/Markdown/CSV sind Austauschformate; für vollständige Anhänge das .glidebackup verwenden.", "get_app_data_dir", "import_full_backup", "complete_backup_payload"), "Text", days=12),
        ]),
        b.group("Rechtliches und Datenschutz prüfen lassen", [
            b.todo("Datenschutzerklärung für App, Website und Support trennen", web(code("Der gelesene App-Code enthält keine Netzwerkbibliothek, Anmeldung oder Telemetrie; Daten werden lokal gespeichert. Das ist keine Zusage über Store, Website, Zahlungsanbieter, Betriebssystem oder Support-Mails. Apple unterscheidet reine lokale Verarbeitung von Übermittlung; öffentlich erreichbare Datenschutz-URL bereitstellen. Den tatsächlich ausgelieferten Build vor Einreichung erneut prüfen.", "Importblock", "get_app_data_dir", "save_items"), "mac_privacy"), "Recht", "Text", days=10),
            b.todo("Impressumsangaben fachlich prüfen und veröffentlichungsfähig machen", web("Anbieter, Rechtsform und tatsächliches Angebot bestimmen die erforderlichen Angaben. Für einen geschäftsmäßigen digitalen Dienst den Anwendungsbereich und die Pflichtangaben aus § 5 DDG prüfen lassen. Hier werden weder Anbieteridentität noch fertige Rechtsberatung ersetzt.", "imprint"), "Recht", days=10),
            b.todo("Lizenztext und Hinweise für mitgelieferte Komponenten erstellen", "Inhaber entscheidet Lizenz und Nutzungsbedingungen. Tatsächlich gebündelte Python-/Tcl-/Tk-Komponenten, Installer und Buildwerkzeuge auf Weitergabebedingungen prüfen; Texte im Releasepaket und auf der Website konsistent halten. Buildinventar fehlt noch, daher keine abgeschlossene Lizenzfreigabe behaupten.", "Recht", "Blocker"),
            b.todo("Altersfreigabe-Fragebögen pro Store beantworten", web("Microsoft nutzt IARC; Apple hat einen eigenen Fragebogen im Einreichungsprozess. Fragen anhand der finalen App und Demo-Inhalte beantworten. Keine Altersstufe aus der Aufgaben-App-Kategorie ableiten oder vorab versprechen.", "win_age", "mac_review"), "Recht", days=14),
        ]),
        b.heading("Build, Signierung und Abnahme"),
        b.group("Nach der Identitätsfreigabe", [
            b.todo("Reproduzierbare Windows- und macOS-Builds herstellen", "Noch offene Releasearbeit: PyInstaller-OneDir als vorgesehene Buildroute prüfen; Windows-Installer und macOS-App/DMG auf echten Zielsystemen bauen. Das ist keine neue Laufzeitabhängigkeit der App. Architektur, Tk-Bündelung, Installieren/Update/Deinstallieren und SHA-256-Manifest belegen. Siehe docs/10_RELEASE_CHECKLIST.md.", "Blocker", importance=3),
            b.todo("Windows-Signatur und Store-Installer verifizieren", web("MSI/EXE-Store: Installer und sämtliche PE-Dateien müssen eine Codesignatur mit Kette zu einer CA des Microsoft Trusted Root Program tragen. Keine selbstsignierte Veröffentlichung. Versionierte unveränderliche HTTPS-Download-URL, eigenständiger Offline-Installer und Silent-Installation sind nötig. Anbieter/Kosten erst nach Identitäts- und Vertriebsentscheidung auswählen.", "win_sign"), "Blocker", "Windows", importance=3),
            b.todo("Apple-Developer-Zugang und Developer-ID-Signatur vorbereiten", web("Für den Direktvertrieb Developer-ID-Zertifikat über die Mitgliedschaft im Apple Developer Program beschaffen. Signieridentität und Schlüssel bleiben außerhalb des Repositorys. Erst unter bestätigtem Anbieter anlegen; keine Account- oder Zertifikatsbeschaffung automatisch ausführen.", "mac_sign"), "Blocker", "macOS"),
            b.todo("Mac-Direktdownload notarisiert und gestapelt prüfen", web("Direktvertrieb: ausführbaren Code mit Developer ID signieren, Hardened Runtime und sicheren Zeitstempel verwenden, per notarytool einreichen, Ticket mit stapler anheften und Gatekeeper-Start testen. Notarisierung ist keine App-Store-Prüfung. Für den Mac App Store ist eine separate Notarisierung nicht nötig, da dort gleichwertige Sicherheitsprüfungen stattfinden.", "mac_notary", "mac_sign"), "Blocker", "macOS", importance=3),
            b.todo("Mac-App-Store-Eignung der Tk-App gesondert prüfen", web("Nur falls Mac App Store gewählt wird: App Sandbox ist gemäß Richtlinie 2.4.5 erforderlich. Dateidialoge, externe Anhänge, Datenpfade und Tcl/Tk-Bündel im signierten Sandbox-Build praktisch prüfen. Das vorhandene Python-Skript ist noch kein nachgewiesen Store-tauglicher Build.", "mac_review"), "Blocker", "macOS", "Annahme"),
            b.todo("Manuelle Windows-/macOS-Abnahmematrix abschließen", "Keine Freigabe allein aus automatisierten Tests ableiten. Reale längere Bedienung, Strg-/Cmd-Auswahl, mehrere Monitore, Schrift/DPI und verschachtelte Dialoge prüfen. Das gemeldete Einfrieren wurde nie reproduziert; die Griffkorrektur ersetzt keinen belastbaren Praxistest. Beleg: docs/05_QA_TESTPLAN.md und docs/07_QA_BERICHT.md.", "Blocker", importance=3),
            b.todo("Backup und Restore mit Kopien echter Testbestände abnehmen", "Ausschließlich kopierte Daten in GLIDE_DATA_DIR verwenden. Bestandszahlen, Unterpunkte, Labels, Papierkorb und Anhänge vor/nach Import vergleichen; Sicherung vor Import und erneuten App-Start prüfen. Originaldaten bleiben unberührt.", "Blocker", importance=3),
        ]),
    ]


def strategy(b):
    return [
        b.heading("Positionierung und Zielgruppe"),
        b.memo("Lokale Arbeitslisten für den eigenen Arbeitsplatz\nDeutsch · ohne Konto · ohne Cloudpflicht",
               code("Glide verbindet Aufgaben, Gliederung, kurze Notizen und lokale Anhänge. Die deutsche Oberfläche und der Einzelplatzbetrieb sind der konkrete Zuschnitt. Keine Team-Suite, keine Cloud-Synchronisation, kein externer Kalender, keine Telemetrie, keine Benachrichtigungen oder Wiederholungen. Nicht-Ziele: docs/01_PRODUCT_CONSTRAINTS.md.", "get_app_data_dir", "new_item", "open_calendar_view")),
        b.todo("Primäre Zielgruppe mit fünf kurzen Gesprächen prüfen", "Arbeitshypothese: deutschsprachige Einzelanwender in Design, Marketing und Projektorganisation, die Arbeitslisten mit Gliederung, Notizen und lokalen Dateien auf einem Desktop führen. Aus Funktionsumfang abgeleitet, noch keine Marktforschung. Fünf Gespräche zu echtem Ablauf, Dateianhängen, Backup und Zahlungsbereitschaft führen; keine Marktgröße behaupten.", "Annahme", days=7, importance=2),
        b.memo("Geeignet: persönlicher Desktop-Arbeitsplatz\nZu prüfen: Solo-Kreative und kleine Projektrollen\nUngeeignet: gemeinsame Live-Projektsteuerung",
               "Einschätzung aus der Produktgrenze: Teammitglieder können Glide einzeln nutzen, aber nicht gleichzeitig denselben Bestand bearbeiten. Deutsch begrenzt die Ansprache; keine internationale Breite oder Zusammenarbeit versprechen.", "Annahme"),
        b.group("Belegbare Stärken als Kombination formulieren", [
            b.todo("Offline und Kontofreiheit mit einem realen Ablauf zeigen", code("Kernfunktionen ohne Anmeldung und Netzwerkbedarf. Ein Beispielablauf vom Eingang über Gliederung bis Backup erklärt den Nutzen besser als pauschale Datenschutz-Superlative. Keine Alleinstellung behaupten: andere lokale Apps existieren.", "get_app_data_dir", "save_items", "import_full_backup"), "Text"),
            b.todo("Vier Punktarten und lokale Anhänge verständlich demonstrieren", code("Aufgabe, Gruppe, Long-Task und Zwischenüberschrift teilen ein Modell. Die Kombination aus Gliederung, Fälligkeiten, Notizen und verwalteten Dateikopien ist eine belegte Stärke, keine bewiesene Markt-Alleinstellung.", "new_item", "item_kind", "sync_item_kind_label", "store_attachment"), "Text"),
            b.todo("Datenkontrolle konkret statt absolut versprechen", code("JSON lokal, portable ZIP-Sicherung mit Anhängen, TXT/Markdown/CSV-Ausgabe, Papierkorb und Rückgängig. Kein Verschlüsselungsversprechen: das JSON und die Archive sind im Code nicht verschlüsselt. Bestandswächter reduziert konkrete Verlustrisiken, garantiert keine Unfehlbarkeit.", "complete_backup_payload", "write_complete_backup", "guarded_structural_change"), "Text"),
        ]),
        b.heading("Wettbewerb – Herstellerangaben, keine Installationstests"),
        b.memo("Things: ohne Things Cloud auf einem Gerät nutzbar\nKontofreiheit allein unterscheidet Glide nicht",
               web("Cultured Code bestätigt Nutzung ohne Things Cloud bei einem Gerät. Synchronisation zu weiteren Apple-Geräten benötigt ein kostenloses Things-Cloud-Konto; Echtzeit-Zusammenarbeit wird nicht unterstützt. Einordnung: Glide adressiert auch Windows, während Things ein Apple-Ökosystem anbietet. Glide liegt beim verfügbaren Geräteverbund zurück. Kein praktischer Vergleichstest und keine pauschale Datenschutzgleichsetzung.", "things")),
        b.memo("Task Coach: lokaler Aufgabenbaum mit mehr Planungstiefe\nWiederholungen, Erinnerungen und Zeiterfassung",
               web("Die Herstellerseite nennt Windows/Mac/Linux, Aufgaben und Unteraufgaben, lokale XML-Dateien, Wiederholungen, optionale Erinnerungen, Zeiterfassung und Anhänge per Drag & Drop. Einordnung: Glide bietet bewusst weniger Zeitplanung; reine Lokalität ist auch hier keine Alleinstellung. Die Seite zeigt noch Release 1.4.6 von 2019; aktuelle Betriebssystemtauglichkeit wurde nicht durch Installation geprüft.", "taskcoach")),
        b.memo("todotxt.net / TodoTxtMac: dateibasierte Alternativen\nEinfaches Austauschformat, stärkerer Tastaturfokus",
               web("todotxt.net ist eine minimale Windows-Oberfläche für eine lokale todo.txt; TodoTxtMac eine zugehörige macOS-Alternative. Kontofreie lokale Dateinutzung ist aus dem Dateikonzept abgeleitet, kein eigener Datenschutz-Audit. Glide ergänzt eine integrierte visuelle Hierarchie und Anhänge, hat dafür ein eigenes Datenformat. Kompatibilität und Pflegezustand der Alternativen vor einer verbindlichen Empfehlung testen.", "todotxt", "todotxtmac"), "Annahme"),
        b.todo("Wettbewerbsvergleich an drei echten Aufgaben überprüfen", "Vorschlag: denselben Ablauf mit einem Aufgabenbaum, einer längeren Notiz und Backup/Restore in Glide und zwei Alternativen testen. Kriterien: Anlaufaufwand, Tastaturbedienung, Dateianhänge, Lesbarkeit, lokale Datenkontrolle, Plattformen. Keine Rangfolge allein aus Herstellertexten veröffentlichen.", "Annahme", days=12),
        b.heading("Preismodell – Optionen zur Inhaberentscheidung"),
        b.memo("Einmalkauf\nKlarer Preis und einfaches Nutzenversprechen",
               "Option: dauerhaft nutzbare gekaufte Version. Vorteil: passt zum lokalen Einzelplatzmodell. Nachteil: langfristige Pflege und Support brauchen kalkulierbare Einnahmen. Kostenpflichtige große Updates sind eine zusätzliche mögliche Regel, keine beschlossene Zusage. Preis und Lizenzumfang bleiben offen.", "Annahme"),
        b.memo("Kostenlos mit freiwilliger Unterstützung\nNiedrige Zugangsschwelle, unsichere Erlöse",
               "Option: kostenlose App, freiwillige Beiträge oder bezahlte Zusatzleistungen außerhalb der Kernfunktion. Vorteil: leichteres Ausprobieren. Nachteil: Beiträge tragen Entwicklung nicht verlässlich; Supportaufwand bleibt. Offenlegung des Quellcodes wäre eine eigene Lizenzentscheidung, nicht die automatische Folge kostenloser Nutzung.", "Annahme"),
        b.memo("Bezahlte Pflege oder Abonnement\nLaufende Finanzierung braucht laufenden Nutzen",
               "Option nur zur Prüfung: laufende Pflegeleistung oder Abo. Vorteil: planbarere Finanzierung. Nachteil: für eine lokale App schwerer zu vermitteln und vertraglich aufwendiger. Eine Kontopflicht, Lizenzserver oder Aboverwaltung sind nicht vorhanden und wären ein Konflikt mit dem heutigen Produktzuschnitt. Keine Umsetzung oder Preisfreigabe.", "Annahme"),
        b.todo("Kosten- und Supportmodell als Entscheidungsvorlage rechnen", "Inhaber klärt Zielumsatz, Pflegekapazität, Signierung, Website, Support, Vertrieb und steuerliche Abwicklung. Drei Preisvarianten mit offen ausgewiesenen Annahmen rechnen; keine Marktpreise, Gebühren oder Margen aus dem Gedächtnis einsetzen.", "Annahme", days=10),
        b.heading("Kanäle und Reihenfolge"),
        b.group("Vor einer Veröffentlichung", [
            b.todo("Kleinen begleiteten Pilottest vorbereiten", "Vorschlag: fünf bis acht passende Einzelanwender, darunter Windows und Mac, mit kopierten Testdaten und vereinbartem Feedback. Aufwandsschätzung: 0,5 Tag Vorbereitung plus 2 Stunden je Rückmelderunde. Direkte Ansprache erst nach Freigabe der Kontakte und Texte.", "Annahme", days=14),
            b.todo("Eine deutschsprachige Produktseite vorbereiten", "Vorschlag: Problem/Nutzen, echte Screenshots, Systemgrenzen, Download nach Freigabe, Backup-Kurzanleitung und Support. Aufwandsschätzung: ein bis zwei Arbeitstage mit vorhandenen Assets. Datenschutz der Website separat planen; keine App-Telemetrie einbauen.", "Text", "Annahme", days=18),
            b.todo("Release-Gates vor Kanalstart abnehmen", "Pflicht vor jeder Ankündigung mit Download: Plattform-QA, Einfrier-Risiko, Restore, Identität, Lizenz, Signaturen und Installationspakete. Der konkrete Starttag entsteht aus bestandenen Gates; die hier eingetragenen Planungsfristen sind kein Releaseversprechen.", "Blocker", importance=3),
        ]),
        b.group("Nach bestandenem Release-Gate", [
            b.todo("Eine fachliche Demonstration für das eigene Netzwerk planen", "Vorschlag: ein kurzer deutschsprachiger Beitrag mit realem Arbeitsablauf für Design-/Marketingkontakte, etwa auf LinkedIn oder im eigenen Newsletter. Aufwandsschätzung: zwei bis vier Stunden; nur vorhandene, zulässig nutzbare Verteiler einsetzen. Kein automatischer Versand beauftragt.", "Text", "Annahme"),
            b.todo("Zwei passende Fachcommunities gezielt bewerten", "Vorschlag: deutschsprachige Design-/Produktivitätsforen oder lokale Kreativnetzwerke auswählen, deren Regeln Eigenwerbung erlauben. Aufwandsschätzung: zwei Stunden Recherche plus individuelle Demonstration. Relevanz und Rückmeldungen zählen, nicht möglichst viele Plattformen.", "Annahme"),
            b.todo("Store-Auftritt nach Kanalentscheidung fertigstellen", "Store kann Auffindbarkeit und Installationsvertrauen unterstützen, bringt aber Prüf-, Paket- und Pflegeaufwand. Aufwand zunächst offen: erst aus gewähltem Storeweg und lauffähiger Buildkette schätzen. Mindestanforderungen stehen in Unterlagen & Assets.", "Annahme"),
            b.todo("Vier Wochen nach Start Nutzen und Supportaufwand auswerten", "Relativer Meilenstein zum noch unbeschlossenen Starttag: häufige Supportfragen, freiwillige Rückmeldungen, Download-/Storezahlen soweit rechtmäßig verfügbar und erfolgreiche Wiederherstellungen betrachten. Keine verdeckte App-Nutzungsmessung. Erste Korrekturen vor zusätzlichem Funktionsumfang priorisieren.", "Annahme"),
        ]),
    ]


def features(b):
    return [
        b.heading("Stand und Verwendung"),
        b.memo("Funktionsbestand Glide 3.5.0 / Format 11\nCodebelege in den Beschreibungen\nHäkchen für die redaktionelle Übernahme",
               code("Die folgenden Punkte beschreiben vorhandenen Code. Ein Häkchen kann bei Übernahme in Produkttexte gesetzt werden; es bestätigt keine Plattformfreigabe. Die drei automatisierten Suiten wurden am 04.09.2026 unter Windows bestanden. Manuelle Langzeitprüfung, vollständige Plattformmatrix und macOS bleiben offen. Prüfergebnis und bekannte Randfälle: docs/07_QA_BERICHT.md und docs/11_BESTANDSANALYSE.md.", "APP_VERSION", "DATA_SCHEMA_VERSION")),
        b.heading("Struktur"),
        b.feature("Listen mit eigenen Aufgaben und Beschreibung", "Jede Liste enthält einen Aufgabenbaum sowie eigene Farbe, Beschreibung und Labels.", "new_list_object", "new_item"),
        b.feature("Ordner und Unterordner bis fünf Ebenen", "Ordner können Listen und andere Ordner enthalten; Zyklen und zu große Tiefe werden geprüft.", "new_folder_object", "MAX_FOLDER_DEPTH", "normalize_folder_parents"),
        b.group("Gliederung innerhalb einer Liste", [
            b.feature("Gruppen halten zusammengehörige Unterpunkte", "Gruppen haben keinen eigenen Erledigtstatus, Termin oder Wichtigkeitswert; sie zählen nicht als Aufgabe.", "ITEM_KIND_GROUP", "is_schedulable_item", "normalize_items"),
            b.feature("Zwischenüberschriften setzen eine Zäsur", "Zwischenüberschriften gliedern die Liste und starten die Nummerierung neu; das Systemlabel bleibt in der Listenansicht ausgeblendet.", "ITEM_KIND_HEADING", "insert_tree_items", "sync_item_kind_label"),
        ], description=code("Zwei verschiedene Arten im gemeinsamen Punktmodell.", "new_item", "item_kind")),
        b.heading("Aufgaben und Details"),
        b.feature("Vier Punktarten: Aufgabe, Gruppe, Long-Task, Überschrift", "Die Art bestimmt Darstellung und Planbarkeit. Nur Aufgabe und Long-Task sind planbar.", "ITEM_KIND_TASK", "ITEM_KIND_GROUP", "ITEM_KIND_LONG", "ITEM_KIND_HEADING", "is_schedulable_item"),
        b.feature("Long-Task mit eigenen Zeilenumbrüchen", "Bis zu 40 gespeicherte Textzeilen, davon bis zu fünf in der Liste sichtbar; weitere Inhalte im Detailfenster lesen.", "normalize_item_text", "MAX_LONG_TASK_TEXT_LINES", "LONG_TASK_MAX_LINES"),
        b.feature("Fälligkeit mit optionaler Uhrzeit", "Drei Zustände: kein Termin, Datum, Datum und Uhrzeit. Ohne Datum bleibt die Uhrzeit leer. Keine Erinnerung per Benachrichtigung.", "normalize_due", "normalize_due_time", "DueField"),
        b.feature("Wichtigkeit von 0 bis 3 und individuelle Punktfarbe", "Wichtigkeit und Farbe sind getrennte Eigenschaften. Gruppen/Überschriften tragen keine Wichtigkeit.", "clamp_importance", "set_item_color_selected", "new_item"),
        b.feature("Beschreibungstext und lokale Dateianhänge", "Dateien werden als verwaltete lokale Kopie abgelegt. Ein Anhang wird beim Öffnen dem Betriebssystem übergeben; Verhalten des externen Programms gehört nicht zur Offline-Zusage von Glide.", "store_attachment", "resolve_attachment_path", "item_form_dialog"),
        b.heading("Labels"),
        b.feature("Labels an Punkten, Listen und Ordnern", "Bis zu 80 Labels; vorgesehen sind höchstens 20 Zuordnungen je Eintrag und sieben Palettenfarben. Mehrfachauswahl über Aufklappfeld. Bekannter Randfall: Bei 20 Labels kann ein zusätzliches festes Artlabel die Grenze auf 21 überschreiten; vor Release klären.", "MAX_LABELS", "MAX_LABELS_PER_ITEM", "LABEL_COLOR_KEYS", "LabelDropdown", "toggle_page_label", "sync_item_kind_label"),
        b.feature("Feste Artlabels Long-Task und Überschrift", "Art und festes Label werden zentral synchronisiert; Labelzuweisung kann deshalb die Punktart ändern.", "sync_item_kind_label", "sync_all_item_kind_labels"),
        b.feature("Labelchips im Kopf; kompakte Labels im Aufgabenbaum", "Im Kopf echte Chips, in der Aufgabenliste ein sichtbarer Labelname plus Zähler weiterer Labels. Keine Chips in ttk.Treeview-Wertspalten.", "pack_label_chips", "format_item_label_names", "LABEL_COLUMN_MAX_VISIBLE"),
        b.heading("Ansichten"),
        b.feature("Geschützter Eingang", "Systemliste als Ablage unsortierter Punkte; wird über system_role erkannt und gesichert.", "is_inbox_list", "ensure_inbox_list"),
        b.feature("In Bearbeitung und Verspätet", "Abgeleitete Aufgabenansichten über Listen hinweg; Gruppen/Überschriften werden nicht als planbare Aufgaben gezählt.", "get_in_progress_items", "get_overdue_items", "is_schedulable_item"),
        b.feature("Lokaler Kalender als Wochen- oder Monatsraster", "Zeigt eigene Fälligkeiten und erlaubt Zugriff auf die Aufgaben. Keine externe Kalenderanbindung oder Synchronisation.", "open_calendar_view"),
        b.feature("Ordnerübersicht mit Listen und Unterordnern", "Eigene Übersicht und Aktionen für den Inhalt eines Ordners.", "refresh_folder_overview", "build_folder_overview_menu"),
        b.feature("Papierkorb mit bis zu 200 Einträgen", "Listen, Ordner und einzelne Punkte samt Unterpunkten und Herkunft können wiederhergestellt werden; referenzierte Anhänge gehören ins Komplettbackup.", "MAX_TRASH_ENTRIES", "new_trash_entry", "restore_trash_entry", "collect_attachment_sources"),
        b.heading("Bedienung"),
        b.feature("Mehrfachauswahl und gemeinsame Aktionen", "Strg unter Windows, Cmd unter macOS werden im Code unterschieden; echte Plattformbedienung separat abnehmen.", "selection_modifier_name", "selection_modifier_pressed", "selected_items_for_change"),
        b.feature("Drag & Drop im Aufgabenbaum und in der Seitenleiste", "Punkte, Gruppen, Listen und Ordner lassen sich gemäß erlaubter Struktur verschieben. Das ist kein Datei-Drop für Anhänge.", "on_drag_end", "on_sidebar_drag_end", "drop_items_on_list", "guarded_structural_change"),
        b.feature("Umbenennen direkt in der Seitenleiste", "Verzögerter Klick, F2 und Kontextmenü; Ordner auf-/zuklappen soll nicht umbenennen. Eingang bleibt geschützt.", "begin_sidebar_rename", "on_sidebar_release_for_rename", "SIDEBAR_RENAME_DELAY_MS"),
        b.feature("Suche, Offen-Filter und Sortierung", "Suche und Nur offene Punkte in der aktuellen Ansicht; Sortierung nach Fälligkeit, Wichtigkeit oder Alphabet. Kein eigener Labelfilter.", "current_search_query", "item_matches_status_filter", "sort_current_list"),
        b.feature("Tastenkürzel und Kontextmenüs", "Plattformabhängige Beschriftungen und Tastenkürzel; vollständige Liste im Hilfedialog. Nicht pauschal alle Mac-Kürzel als praktisch geprüft ausgeben.", "accel", "show_shortcuts_dialog", "build_item_context_menu"),
        b.heading("Daten und Sicherheit"),
        b.feature("Automatisches Speichern außerhalb des Programmordners", "Plattformgerechter Benutzerordner; GLIDE_DATA_DIR kann eine separate Ablage festlegen. Atomisches JSON-Schreiben schützt vor Teilständen.", "get_app_data_dir", "save_items", "write_json_atomic"),
        b.feature("Rotierende Sicherungen bis 40 Stände", "Rotation folgt zusätzlich Zeit- und Schutzregeln; kein Ersatz für ein externes Backup und keine Zusage von 40 immer verfügbaren Zeitpunkten.", "MAX_BACKUPS", "write_backup_copy", "prune_backups"),
        b.feature("Komplettbackup als ZIP mit data.json und Anhängen", "Format 11; portable Backups werden ab Format 4 akzeptiert. Import prüft Struktur und Pfade, sichert vorher den alten Stand und ersetzt dann den gesamten Bestand.", "MIN_PORTABLE_BACKUP_SCHEMA_VERSION", "write_complete_backup", "inspect_backup_archive", "validate_backup_schema", "import_full_backup"),
        b.feature("TXT-Import sowie TXT-, Markdown- und CSV-Export", "CSV nutzt Semikolon und UTF-8-BOM. Austauschformate haben nicht denselben Umfang wie ein komplettes Backup mit Anhängen; ein CSV- oder Markdown-Import ist nicht vorhanden.", "parse_txt_items", "export_as_txt", "export_as_markdown", "export_as_csv"),
        b.feature("Rückgängig mit bis zu 20 Schritten", "Schnappschüsse im laufenden Programm; wirkungslose Änderungen sollen keinen ältesten Schritt verbrauchen. Kein über Neustarts fortgeschriebenes Änderungsarchiv.", "MAX_UNDO_STEPS", "snapshot_undo", "trim_undo_stack", "undo_last_change"),
        b.feature("Bestandswächter für Strukturänderungen", "Vergleicht Punkt-IDs vor/nach Umbauaktionen und rollt unerwartete Verluste zurück. Zusätzliche Absicherung, kein absolutes Versprechen gegen jeden Datenverlust.", "guarded_structural_change", "DataIntegrityError"),
        b.feature("Ansicht „Labels“ mit Zuordnung per Ziehen", "Vierte Systemansicht neben Eingang, In Bearbeitung, Verspätet und Papierkorb: der gesamte Bestand nach Labels gruppiert, Punkte in der Labelfarbe. Ein Punkt mit mehreren Labels steht in jeder Gruppe. Ein Zug in eine andere Gruppe ersetzt genau das Label der Herkunftsgruppe; „Ohne Label“ nimmt es zurück. Systemlabels bilden bewusst keine Gruppe.", "LABELS_VIEW", "refresh_label_overview", "move_item_to_label_group", "label_view_groups"),
        b.heading("Darstellung und offene Grenzen"),
        b.feature("Hellmodus dunkelblau, Dunkelmodus grau", "Hellmodus verwendet #15243C; dunkle Flächen #111113/#1C1C1E/#2C2C2E. Theme und Fensterzustand werden gespeichert.", "apply_theme", "toggle_theme", "save_settings"),
        b.feature("Zentrale Textsymbole mit verbliebenen Ausnahmen", "ICONS enthält Textzeichen, darunter Anhang ⊕, Kalender ▦, Labels ◈. IMPORTANCE_MARKERS[3], GROUP_MARKER und description_suffix in Aufgabenübersichten sind noch Emoji; daher nicht 'vollständig emoji-frei' bewerben.", "ICONS", "IMPORTANCE_MARKERS", "GROUP_MARKER", "description_suffix"),
        b.feature("Persönliche Startseite und Einstellungen", "Bearbeiten > Einstellungen speichert einen Begrüßungsnamen, ein Textmonogramm, Startansicht und die Anzeige lokaler Bestandszahlen. Die Startseite nennt heute fällige und zuletzt tatsächlich bearbeitete Listen sowie drei Vorlagen. Es gibt keine Zeiterfassung oder Telemetrie.", "show_settings_dialog", "home_summary", "create_list_from_template"),
        b.feature("Farbige Eingaben und wechselnde Punktarten", "Farbnamen und Wichtigkeitsfähnchen sind auch ausgewählt farbig. Long-Task und Überschrift stehen in der erweiterten Labelauswahl und wechseln unmittelbar die Eingabemaske. Die Schaltflächen bleiben unten sichtbar.", "item_form_dialog", "importance_choice_text"),
        b.feature("Hilfe im App-Theme", "Über Glide, Tastenkürzel, Meldungen und Rückfragen benutzen das Theme. Die Tastenkürzel stehen fett in einer eigenen linken Spalte. Native Dateiauswahldialoge folgen weiterhin dem Betriebssystem.", "show_about_dialog", "show_shortcuts_dialog", "themed_message_dialog"),
        b.feature("Anpassbare Spalten und Mindestfenster 860 × 700", "Fälligkeits- und Labelspalte folgen seit 3.3.0 dem tatsächlichen Inhalt und sind links ausgerichtet; die Musterbreite bleibt Obergrenze. Im schmalen Fenster weichen erst die Labels, dann die Fälligkeit. DPI, kleine Fenster und mehrere Monitore bleiben praktische Prüffelder.", "task_tree_column_widths", "content_column_widths", "advanced_button_min_width", "create_ui"),
        b.memo("Grenzen: keine Cloud, kein Team, keine Wiederholung\nKeine Chipdarstellung im Aufgabenbaum\nKein Drag & Drop für Dateianhänge",
               code("Die Produktgrenzen schließen Wiederholungen, Benachrichtigungen, Konten und externe Kalender aus. ttk.Treeview trägt keine Labelchips in Wertspalten. Anhänge werden über Dialoge hinzugefügt; Datei-Drop ist nicht implementiert und würde eine gesonderte Architekturentscheidung benötigen. Quelle zusätzlich: docs/01_PRODUCT_CONSTRAINTS.md.", "create_ui", "item_form_dialog", "store_attachment")),
        b.feature("Wiederkehrende Aufgaben ohne Hintergrunddienst", "Eine Aufgabe mit Faelligkeit kann sich taeglich, alle N Tage, an festen Wochentagen, woechentlich, monatlich oder jaehrlich wiederholen, wahlweise mit Enddatum. Beim Abhaken rueckt der Punkt auf seinen naechsten Termin vor; es wird nichts im Voraus erzeugt. Erinnerungen mit Benachrichtigung bleiben ausgeschlossen - sie braeuchten einen Hintergrunddienst. Datenformat 11 mit additiver Migration aus Format 10.", "normalize_repeat", "next_repeat_date", "advance_repeating_items", "DATA_SCHEMA_VERSION"),
        b.todo("Lange reale Windows-Nutzung und komplette macOS-Abnahme dokumentieren", "Feature vorhanden heißt nicht plattformweit abgenommen. Besonders das frühere Einfrieren bei verschachtelten Dialogen wurde nie reproduziert. Aktuelle automatische Windows-Ergebnisse und verbleibende manuelle Punkte stehen in docs/07_QA_BERICHT.md; keine abgeschlossene macOS-Prüfung behaupten.", "Blocker", importance=3),
        b.todo("Artwechsel an der Labelgrenze vor Release korrigieren", code("Belegter Randfall aus der Bestandsanalyse: 20 vorhandene Labels plus automatisch synchronisiertes Artlabel ergeben 21. Entscheidung über das zulässige Verhalten und gezielte Regression erforderlich; die drei bisherigen Suiten erfassen den Fall nicht. Keine Korrektur als bereits umgesetzt ausgeben.", "sync_item_kind_label", "MAX_LABELS_PER_ITEM"), "Blocker", importance=3),
        b.todo("Einrücken an der maximalen Punkttiefe absichern", code("Belegter Randfall aus der Bestandsanalyse: make_subitem kann einen zuvor gültigen Bestand auf Tiefe 101 bringen; spätere Normalisierung lehnt ihn ab. Guard vor der Strukturänderung und Wiederlade-Test nötig. Vor Release beheben; keine pauschale Datenverlustgarantie aus dem Bestandswächter ableiten.", "make_subitem", "MAX_ITEM_DEPTH", "normalize_items"), "Blocker", importance=3),
    ]


def build(app, mod, today=None):
    if mod.APP_VERSION != APP_VERSION or app.DATA_SCHEMA_VERSION != 11:
        raise ValueError("Releaseinhalte zuerst gegen den neuen App-Stand prüfen und fortschreiben.")
    b = ReleaseBuilder(app, today or date.today())
    for name, color in (("Blocker", "delete"), ("Windows", "accent"), ("macOS", "import"),
                        ("Text", "export"), ("Grafik", "clear"), ("Recht", "flag"), ("Annahme", "due_action")):
        b.label(name, color)
    inbox = next(entry for entry in app.lists if app.is_inbox_list(entry))
    app.lists[:] = [inbox]
    inbox["items"][:] = []
    b.open_list(inbox)
    folder = b.folder("Releaseplanung 3.5.0", "accent",
                      "Erste Veröffentlichung vorbereiten; App-Version 3.5.0 bleibt erhalten. Recherche 04.09.2026.")
    for title, content, labels in zip(LIST_TITLES, (assets(b), strategy(b), features(b)),
                                      (("Grafik", "Text"), ("Annahme",), ("Text",))):
        entry = b.listing(title, content, folder=folder, color="accent",
                          labels=b.ids(*labels),
                          note=f"Stand 3.5.0 / Format 11 · Recherche {RESEARCH_DATE} · Planungsstichtag {b.today.isoformat()}. Fristen sind unverbindliche Vorschläge. Quellen und Belege stehen in den Punktbeschreibungen.")
        if title == LIST_TITLES[0]:
            first = entry
    app.sync_all_item_kind_labels()
    b.open_list(first)
    app.save_items()
    return app.complete_backup_payload()


def verify_import(app, mod, target, payload):
    """Echter Import, nur Dateiauswahl und Bestätigungsdialoge werden ersetzt."""
    with zipfile.ZipFile(target) as archive:
        app.inspect_backup_archive(archive)
        data = json.loads(archive.read("data.json"))
    app.validate_backup_schema(data, portable=True)
    old = {"folders": app.folders, "labels": app.labels, "trash": app.trash}
    try:
        lists, _ = app.normalize_lists_data(data)
        app.normalize_trash_data(data.get("trash"))
        known = {label["id"] for label in app.labels}
        for listing in lists:
            for item in app.walk_items(listing["items"]):
                assert set(item.get("labels", [])).issubset(known)
    finally:
        for name, value in old.items():
            setattr(app, name, value)
    calls = []
    original_open = mod.filedialog.askopenfilename
    original_yes = mod.ListApp.ask_yes_no
    original_info = mod.ListApp.show_info
    original_error = mod.ListApp.show_error
    try:
        mod.filedialog.askopenfilename = lambda **kwargs: str(target)
        mod.ListApp.ask_yes_no = staticmethod(lambda *args, **kwargs: True)
        mod.ListApp.show_info = staticmethod(lambda *args, **kwargs: calls.append(("ok", args)))
        mod.ListApp.show_error = staticmethod(lambda *args, **kwargs: calls.append(("error", args)))
        app.import_full_backup()
    finally:
        mod.filedialog.askopenfilename = original_open
        mod.ListApp.ask_yes_no = original_yes
        mod.ListApp.show_info = original_info
        mod.ListApp.show_error = original_error
    assert [kind for kind, _ in calls] == ["ok"], calls
    assert [entry["title"] for entry in app.lists if not app.is_inbox_list(entry)] == list(LIST_TITLES)
    expected = {item["id"] for entry in payload["lists"] for item in app.walk_items(entry["items"])}
    actual = {item["id"] for entry in app.lists for item in app.walk_items(entry["items"])}
    assert actual == expected, "Punktbestand wurde beim Import verändert."
    assert app.app_title == LIST_TITLES[0]


def save_windows_screenshot(root, target):
    """Erfasst ausschließlich das eigene Testfenster per PrintWindow als PNG.

    Kein Zusatzpaket und keine Aufnahme anderer Fenster. Die Zielplattform
    liefert damit den Bildnachweis des tatsächlich importierten Bestands.
    """
    from ctypes import wintypes
    user = ctypes.WinDLL("user32", use_last_error=True)
    gdi = ctypes.WinDLL("gdi32", use_last_error=True)
    user.GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
    user.GetAncestor.restype = wintypes.HWND
    user.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    user.GetDC.argtypes = [wintypes.HWND]
    user.GetDC.restype = wintypes.HDC
    user.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
    user.PrintWindow.argtypes = [wintypes.HWND, wintypes.HDC, wintypes.UINT]
    gdi.CreateCompatibleDC.argtypes = [wintypes.HDC]
    gdi.CreateCompatibleDC.restype = wintypes.HDC
    gdi.CreateDIBSection.argtypes = [wintypes.HDC, ctypes.c_void_p, wintypes.UINT,
                                   ctypes.POINTER(ctypes.c_void_p), wintypes.HANDLE, wintypes.DWORD]
    gdi.CreateDIBSection.restype = wintypes.HBITMAP
    gdi.SelectObject.argtypes = [wintypes.HDC, wintypes.HGDIOBJ]
    gdi.SelectObject.restype = wintypes.HGDIOBJ
    gdi.DeleteObject.argtypes = [wintypes.HGDIOBJ]
    gdi.DeleteDC.argtypes = [wintypes.HDC]
    hwnd = user.GetAncestor(root.winfo_id(), 2)
    rect = wintypes.RECT()
    if not user.GetWindowRect(hwnd, ctypes.byref(rect)):
        raise ctypes.WinError(ctypes.get_last_error())
    width, height = rect.right - rect.left, rect.bottom - rect.top
    dc = user.GetDC(hwnd)
    memory = gdi.CreateCompatibleDC(dc)
    header = ctypes.create_string_buffer(struct.pack("<IiiHHIIiiII", 40, width, -height,
                                                     1, 32, 0, width * height * 4, 0, 0, 0, 0))
    bits = ctypes.c_void_p()
    bitmap = gdi.CreateDIBSection(dc, header, 0, ctypes.byref(bits), None, 0)
    if not bitmap:
        gdi.DeleteDC(memory)
        user.ReleaseDC(hwnd, dc)
        raise ctypes.WinError(ctypes.get_last_error())
    previous = gdi.SelectObject(memory, bitmap)
    try:
        if not user.PrintWindow(hwnd, memory, 2):
            raise ctypes.WinError(ctypes.get_last_error())
        bgra = ctypes.string_at(bits, width * height * 4)
        rgb = bytearray(width * height * 3)
        rgb[0::3], rgb[1::3], rgb[2::3] = bgra[2::4], bgra[1::4], bgra[0::4]
        pixels = b"".join(b"\0" + rgb[y * width * 3:(y + 1) * width * 3] for y in range(height))
        def chunk(kind, data):
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        image = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
                 + chunk(b"IDAT", zlib.compress(pixels)) + chunk(b"IEND", b""))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(image)
    finally:
        gdi.SelectObject(memory, previous)
        gdi.DeleteObject(bitmap)
        gdi.DeleteDC(memory)
        user.ReleaseDC(hwnd, dc)


def screenshots(app, root, target):
    root.geometry("1380x950+0+0")
    root.deiconify()
    for theme, path in (("light", target), ("dark", target.with_stem(target.stem + "_dunkel"))):
        app.theme_name = theme
        app.apply_theme()
        app.update_sidebar_list()
        app.refresh_tree()
        root.update()
        # Tk malt native Titelleiste und Schrift nach dem Mapping asynchron.
        root.tk.call("after", 200, "set", "::glide_capture_ready", "1")
        root.tk.call("vwait", "::glide_capture_ready")
        root.update()
        save_windows_screenshot(root, path)
        print(f"Sichtnachweis ({theme}): {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ziel", default=str(DEFAULT_TARGET))
    parser.add_argument("--stichtag", type=date.fromisoformat, default=None,
                        help="Bezugstag für relative Planungsfristen; Standard: heute")
    parser.add_argument("--screenshot", type=pathlib.Path,
                        help="Windows: eigenes importiertes Fenster als PNG, zusätzlich *_dunkel.png")
    args = parser.parse_args()
    if args.screenshot and os.name != "nt":
        parser.error("--screenshot verwendet PrintWindow und benötigt Windows.")
    target = pathlib.Path(args.ziel).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="glide-release-") as temporary:
        mod = load_module(pathlib.Path(temporary) / "Glide")
        root = mod.tk.Tk()
        root.withdraw()
        app = mod.ListApp(root)
        try:
            payload = build(app, mod, args.stichtag)
            app.write_complete_backup(str(target), payload)
            verify_import(app, mod, target, payload)
            if args.screenshot:
                screenshots(app, root, args.screenshot.expanduser().resolve())
            print(f"Geschrieben und über import_full_backup eingelesen: {target}")
            for name, value in summarise(app).items():
                print(f"  {value:4d}  {name}")
            print("Import ersetzt alle Listen. Fristen: Planungsvorschläge; Recherche unverändert 04.09.2026.")
        finally:
            app.cancel_pending_callbacks()
            root.destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
