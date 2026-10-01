#!/usr/bin/env python3
"""Reproduzierbarer Vorlagenkatalog; ausschließlich temporäre Daten, keine GUI."""
import base64
from datetime import date, timedelta
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[2]
ANCHOR = date(2026, 9, 11)
TARGET = ROOT / 'src/glide/resources/templates/glide_vorlagen.glidetemplates'

# Titel, Zweck, drei Phasen mit konkreten Ergebnissen. Inhalte sind Beispiele,
# keine Rechtsprüfung, verbindlichen Fristen oder automatisierten Integrationen.
PROJECTS = [
    ('folder-project', 'Projekt', 'Ein Kundenprojekt vom Briefing bis zur dokumentierten Übergabe.', [
        ('Briefing und Planung', [('Ziel und Abnahmekriterien vereinbaren', 'Ergebnis, Zielgruppe, Umfang und drei prüfbare Abnahmekriterien festhalten.'), ('Leistungen und Ausschlüsse festhalten', 'Welche Lieferobjekte gehören zum Auftrag? Was benötigt einen Folgeauftrag?'), ('Meilensteine und Zuständigkeiten abstimmen', 'Für jeden Meilenstein eine verantwortliche Person, ein Ergebnis und einen Freigabeweg benennen.')]),
        ('Umsetzung und Abstimmung', [('Ersten prüfbaren Entwurf erstellen', 'Arbeitsstand mit Versionsdatum, offenen Fragen und dem nächsten Entscheidungspunkt bereitstellen.'), ('Rückmeldungen konsolidieren', 'Doppelte Wünsche zusammenführen; Konflikte und Auswirkungen auf Umfang und Termin sichtbar machen.'), ('Freigabestand dokumentieren', 'Freigebende Person, Datum, freigegebene Version und verbleibende Auflagen festhalten.')]),
        ('Übergabe und Abschluss', [('Lieferumfang prüfen und übergeben', 'Dateien, Zugangshinweise und Pflegeanleitung gegen die Abnahmekriterien prüfen.'), ('Projektablage abschließen', 'Freigegebene Master, Exporte und Entscheidungsstand geordnet ablegen.'), ('Erfahrungen für den Folgeauftrag festhalten', 'Aufwand, Verzögerungsgründe und Verbesserungen in einer kurzen Nachbesprechung dokumentieren.')]),
    ]),
    ('folder-event', 'Veranstaltung', 'Eine Unternehmensveranstaltung mit Vorbereitung, Ablauf und Nachbereitung organisieren.', [
        ('Vorbereitung', [('Ziel, Teilnehmerzahl und Budget abstimmen', 'Erwartetes Ergebnis, Kostenrahmen und Freigabe der verantwortlichen Person festhalten.'), ('Ort, Technik und Dienstleister bestätigen', 'Ansprechpersonen, Lieferumfang, Aufbauzeiten und Stornobedingungen prüfen.'), ('Einladung und Anmeldung vorbereiten', 'Zielgruppe, Einladungstext, Antwortfrist und sparsame Verarbeitung der Anmeldedaten abstimmen.')]),
        ('Durchführung', [('Ablauf mit Zuständigkeiten durchgehen', 'Aufbau, Empfang, Programmpunkte, Pausen und Abbau mit Zeitpuffern planen.'), ('Technik und Beschilderung vor Ort testen', 'Ton, Präsentation, Wegweisung und Ausweichlösung mit den Beteiligten durchspielen.'), ('Offene Punkte während des Termins protokollieren', 'Rückfragen mit Kontaktperson und nächstem Schritt erfassen; keine sensiblen Gästelisten in frei geteilten Unterlagen.')]),
        ('Nachbereitung', [('Rückmeldungen und Zusagen bearbeiten', 'Jede Zusage als Aufgabe mit zuständiger Person und bestätigtem Termin festhalten.'), ('Kosten und Leistungen abgleichen', 'Rechnungen gegen Angebote und tatsächlich erbrachte Leistungen prüfen.'), ('Ergebnisse und Material archivieren', 'Freigegebene Fotos, Ablaufplan und Lernpunkte geordnet ablegen; Löschfristen für Teilnehmerdaten intern klären.')]),
    ]),
    ('real-estate', 'Immobilienvermarktung', 'Ein Objekt vom Unterlagencheck über Exposé und Landingpage bis zur Vertriebsübergabe vorbereiten.', [
        ('Objekt und Unterlagen', [('Objektsteckbrief mit Vertrieb abstimmen', 'Objektkennung, Lage, Zielgruppe, Ausstattungsmerkmale, Ansprechpartner und Freigabeverantwortung erfassen.'), ('Flächen, Grundrisse und Pflichtangaben prüfen lassen', 'Aktuelle Pläne und Quellen sammeln. Flächen- und Energieangaben durch die zuständige Fachperson bestätigen lassen.'), ('Bildmaterial und Nutzungsrechte klären', 'Bildliste mit Motiven, Fotograf, Bearbeitungsstand, erlaubten Medien und Ablauf der Nutzungsrechte anlegen.')]),
        ('Exposé und Objektseite', [('Nutzenargumentation und Texte entwickeln', 'Drei belegbare Objektvorteile ausarbeiten; Umgebung und Ausstattung konkret beschreiben, ungeprüfte Versprechen vermeiden.'), ('Exposé und Grundrisse produzieren', 'Versionierte Druck- und Webdateien erstellen. Lesbarkeit kleiner Grundrissbeschriftungen und Druckränder prüfen.'), ('Objektseite mit klarer Kontaktstrecke bauen', 'Mobile Galerie, Grundrisse, Ansprechpartner und Kontaktformular prüfen. Externe Karte erst nach Zustimmung laden.')]),
        ('Freigabe und Vertrieb', [('Objektdaten kanalübergreifend freigeben', 'Exposé, Website und Portaltexte gegen dieselbe bestätigte Datenquelle abgleichen.'), ('Veröffentlichung und Anfrageweg testen', 'Links, Telefonnummer, E-Mail, Formularzustellung und Darstellung auf Smartphone prüfen.'), ('Vertriebsfeedback nachhalten', 'Wiederkehrende Rückfragen, fehlerhafte Angaben und notwendige Aktualisierungen als konkrete Aufgaben sammeln.')]),
    ]),
    ('wordpress', 'WordPress-Relaunch', 'Eine Unternehmenswebsite von der Bestandsaufnahme bis zur kontrollierten Übergabe erneuern.', [
        ('Bestand und Konzept', [('Seitenbestand und Conversion-Ziele erfassen', 'Bestehende URLs, wichtige Einstiegsseiten, Formulare und messbare Kontaktziele inventarisieren.'), ('Inhaltsstruktur und Seitentypen abstimmen', 'Navigation, Verantwortliche für Inhalte, Templates und den Freigabeweg festlegen.'), ('Testumgebung und Rückfallkopie vorbereiten', 'Dateien und Datenbank sichern; Wiederherstellung in einer getrennten Umgebung prüfen. Zugangsdaten nicht in der Aufgabenbeschreibung speichern.')]),
        ('Design und Umsetzung', [('Responsive Seitentemplates umsetzen', 'Abstände, Typografie, Kontraste, Tastaturfokus und Semantik auf schmalen und breiten Ansichten prüfen.'), ('Formulare und externe Inhalte prüfen', 'Pflichtfelder, Fehlermeldungen, Mailzustellung und Einwilligung für Karten oder Videos durchspielen.'), ('Inhalte und Weiterleitungen vorbereiten', 'Texte, Bildgrößen, Alt-Texte, Metadaten und URL-Zuordnung kontrollieren.')]),
        ('Qualität und Livegang', [('Abnahme auf Staging durchführen', 'Wichtige Nutzerwege mit Tastatur, Smartphone und Desktop prüfen; offene Abweichungen priorisieren.'), ('Livegang mit Rückfallplan durchführen', 'Freigegebenen Stand bereitstellen, Weiterleitungen prüfen, Formular testen und Rückfallkopie bis zur Abnahme behalten.'), ('Pflege an das Unternehmen übergeben', 'Redaktionsrollen, Aktualisierungsprozess, Backupzuständigkeit und Supportweg dokumentieren.')]),
    ]),
    ('property-management', 'WEG-Verwaltung', 'Objektbezogene Vorgänge sammeln, Dienstleister koordinieren und Ergebnisse nachvollziehbar ablegen.', [
        ('Eingang und Vorgänge', [('Meldung einem Objekt und Vorgang zuordnen', 'Objektkennung, Eingang, Sachverhalt, Rückrufkontakt und vorhandene Belege erfassen; personenbezogene Daten sparsam verwenden.'), ('Dringlichkeit und Zuständigkeit klären', 'Zuständige Fachperson entscheidet über Sofortmaßnahme, Beauftragung und rechtliche Frist. Vorlagenfristen sind keine gesetzlichen Fristen.'), ('Nächste Rückmeldung terminieren', 'Konkreten nächsten Schritt und zugesagten Rückmeldetermin mit Uhrzeit eintragen.')]),
        ('Dienstleister und Maßnahmen', [('Angebote mit gleichem Leistungsumfang anfordern', 'Leistungsbeschreibung, Terminfenster, Zugang und Vergleichskriterien festhalten.'), ('Freigabe und Beauftragung dokumentieren', 'Freigabegrundlage und berechtigte Person prüfen; Auftrag mit Referenz auf Angebot ablegen.'), ('Leistung und Restpunkte kontrollieren', 'Ausführung, Belege und offene Mängel mit der zuständigen Person durchgehen.')]),
        ('Ablage und Nachverfolgung', [('Rückmeldung an Beteiligte vorbereiten', 'Sachstand, erledigte Maßnahme und nächstes Vorgehen in einem kurzen Entwurf festhalten.'), ('Rechnung und Leistungsnachweis abgleichen', 'Objekt, Auftrag, Betrag und sachliche Freigabe vor Weitergabe prüfen.'), ('Vorgang abschließen oder Wiedervorlage setzen', 'Abschlusskriterium dokumentieren; nur bei echtem Folgebedarf Wiederholung einrichten.')]),
    ]),
    ('construction', 'Baukommunikation', 'Baufortschritt, Anwohnerinformation und Freigaben eines Bauprojekts koordinieren.', [
        ('Abstimmung und Fakten', [('Bauabschnitt mit Projektleitung abgleichen', 'Zeitraum, Ansprechpartner und freigegebene Aussagen sammeln; Planstand mit Datum kennzeichnen.'), ('Betroffene Zielgruppen und Kanäle festlegen', 'Anwohner, Erwerber, interne Teams und Presse getrennt betrachten.'), ('Bild- und Planmaterial auswählen', 'Aktualität, Rechte, Bildunterschriften und Freigabestatus prüfen.')]),
        ('Information und Veröffentlichung', [('Baustelleninformation entwerfen', 'Was passiert wann, welche Auswirkungen sind bekannt und wo können Rückfragen gestellt werden?'), ('Text, Aushang und Website freigeben lassen', 'Fachfreigabe, Kommunikationsfreigabe und Versionsstand dokumentieren.'), ('Verteilung und Erreichbarkeit kontrollieren', 'Freigegebene Kanäle bedienen; Kontakte, Links und Lesbarkeit des Aushangs testen.')]),
        ('Rückfragen und Aktualisierung', [('Rückfragen nach Thema bündeln', 'Fachliche Antworten durch zuständige Stellen bestätigen lassen und offenen Punkten einen Verantwortlichen zuordnen.'), ('Änderungen am Bauablauf nachführen', 'Überholte Angaben in allen veröffentlichten Medien berichtigen; Datum der Aktualisierung festhalten.'), ('Kommunikationsstand für die nächste Phase sichern', 'Freigegebene Texte, Motive und wesentliche Entscheidungen geordnet archivieren.')]),
    ]),
]

GUIDES = {
    'daily': ['Ein beobachtbares Ergebnis formulieren. Umfang auf heute begrenzen und Wichtigkeit setzen.', 'Eingang sichten; jede Aufgabe mit einem Verb und einem klaren Ergebnis notieren.', 'Ein realistisches Zeitfenster wählen und Fälligkeit mit Uhrzeit setzen.', 'Erledigtes abhaken, offene Punkte neu planen und einen kurzen Lernpunkt notieren.'],
    'project': ['Zielgruppe, gewünschtes Ergebnis und Abnahmekriterien in der Beschreibung festhalten.', 'Anforderungen mit Quelle, Priorität und offenen Fragen sammeln.', 'Arbeitspakete mit prüfbaren Ergebnissen und Verantwortlichen planen.', 'Einen unmittelbar ausführbaren Schritt mit Termin und Label festlegen.', 'Ergebnis mit Auftraggeber prüfen, Restpunkte erfassen und Ablage abschließen.'],
    'shopping': ['Mengen und benötigte Sorten ergänzen; Vorräte vorher prüfen.', 'Bedarf für die geplanten Mahlzeiten notieren und Menge ergänzen.', 'Menge, Transport und vorhandene Vorräte prüfen.', 'Konkrete Artikel und Größen ergänzen; erledigte Käufe abhaken.'],
    'week': ['Offene Zusagen prüfen und überholte Aufgaben bewusst streichen oder verschieben.', 'Drei überprüfbare Wochenergebnisse formulieren und priorisieren.', 'Bestätigte Termine mit Datum und Uhrzeit eintragen.', 'Freie Kapazität für Rückfragen und unerwartete Aufgaben reservieren.', 'Ergebnisse festhalten, Wiedervorlagen prüfen und nächste Woche vorbereiten.'],
    'meeting': ['Gewünschte Entscheidung oder Ergebnis formulieren.', 'Nur notwendige Teilnehmende einplanen und Zuständigkeiten benennen.', 'Themen mit Ziel und Zeitbedarf notieren.', 'Versionierte Unterlagen vorab bereitstellen; sensible Daten gesondert behandeln.', 'Entscheidungen, offene Fragen und Freigaben nachvollziehbar dokumentieren.', 'Jede Zusage als Aufgabe mit verantwortlicher Person und bestätigter Frist erfassen.'],
    'trip': ['Ziel, Reisetage, Budget und notwendige Termine festhalten.', 'Buchung, Adresse, Storno- und Check-in-Angaben kontrollieren.', 'Verbindung, Reservierung, Umstiegspuffer und Rückreise prüfen.', 'Gültigkeit und tatsächlich benötigte Dokumente anhand des Reiseziels prüfen.', 'Kleidung, Technik, Ladegeräte und persönliche Dinge als Unterpunkte ergänzen.', 'Post, Schlüssel, Versorgung und erreichbare Kontaktperson organisieren.'],
    'onboarding': ['Geräte, Rollen und erforderliche Zugänge mit IT abstimmen; Passwörter getrennt übergeben.', 'Zuständige Begleitperson und Vertretung benennen.', 'Einführungen, erste Übungsaufgabe und kurze Rückmeldetermine planen.', 'Abläufe an echten Beispielen zeigen und Anleitung bereitstellen.', 'Offene Fragen, Zugangsprobleme und Lernziele gemeinsam nachhalten.'],
    'content': ['Zielgruppe, Kommunikationsziel und zentrale Aussage festlegen.', 'Einstieg, Hauptargumente und Handlungsaufforderung strukturieren.', 'Belegbare Fakten verwenden; Quellen und offene Angaben kennzeichnen.', 'Urheber, erlaubte Nutzung, Motivfreigabe und erforderliche Hinweise prüfen.', 'Fakten, Sprache, Links und mobile Darstellung gegenlesen lassen.', 'Nur freigegebenen Stand veröffentlichen und Link sowie Zeitpunkt dokumentieren.'],
    'household': ['Sortieren, waschen, trocknen und einräumen als Unterpunkte ergänzen.', 'Vorräte prüfen und konkrete Artikel mit Menge auflisten.', 'Reinigungsbedarf konkret festlegen und Mittel bereitstellen.', 'Räume und benötigte Geräte ergänzen.', 'Örtliche Abholtermine prüfen und tatsächliche Fälligkeit eintragen.', 'Post bearbeiten, offene Zahlungen prüfen und Unterlagen richtig ablegen.'],
    'review': ['Konkrete Ergebnisse und wirksame Vorgehensweisen notieren.', 'Hindernisse mit Ursache und beeinflussbarem nächsten Schritt beschreiben.', 'Unnötige Arbeit, doppelte Ablagen oder unklare Abläufe benennen.', 'Höchstens drei konkrete Verbesserungen mit Termin auswählen.'],
}

# Wiederholungsarten je Vorlage. Schluessel ist entweder (Vorlage, Index) fuer
# einen einzelnen Punkt oder die Vorlage allein als Vorgabe fuer alle ihre
# Punkte. Zusammen deckt der Katalog alle sechs Arten ab, eine davon mit
# Enddatum – genau die Form, die beim Kalenderrundlauf am empfindlichsten ist.
REPEAT_PLAN = {
    ("daily", 0): {"art": "taeglich"},
    ("week", 2): {"art": "wochentage", "tage": [0, 4],
                  "ende": (ANCHOR + timedelta(days=90)).isoformat()},
    ("week", 4): {"art": "woechentlich"},
    ("household", 0): {"art": "woechentlich"},
    ("household", 1): {"art": "tage", "abstand": 14},
    ("household", 2): {"art": "monatlich"},
    ("household", 3): {"art": "jaehrlich"},
    ("review", 0): {"art": "monatlich"},
    # Vorgabe fuer alle uebrigen Haushaltspunkte: Bis 3.21.1 wiederholte sich
    # dort jeder Punkt woechentlich. Die Varianten oben ersetzen nur die ersten
    # vier – ohne diese Vorgabe verloeren die restlichen ihre Wiederholung.
    "household": {"art": "woechentlich"},
}

# Geschaetzter Aufwand in Minuten je Vorlagenpunkt. Nur dort gesetzt, wo eine
# Schaetzung inhaltlich Sinn hat; ein Punkt ohne Schaetzung ist beabsichtigt,
# weil die Tagesplanung solche Punkte getrennt auszaehlt.
PLAN_MINUTES = {
    "daily": {0: 15, 1: 20, 2: 90, 3: 15},
    "week": {0: 30, 1: 45, 2: 20, 4: 40},
    "household": {0: 45, 2: 60},
}

# Bearbeitungstag als Abstand zum Fristanker. Die Tagesplanung bekommt alles
# auf einen Tag, die Wochenplanung verteilt ueber die Woche.
PLAN_OFFSET = {
    "daily": {0: 0, 1: 0, 2: 0, 3: 0},
    "week": {0: 0, 1: 0, 2: 1, 4: 4},
    "household": {0: 0, 2: 7},
}


def build(mod):
    app = mod.ListApp.__new__(mod.ListApp)
    app.labels = []
    app.ensure_system_labels()
    records = []
    def labels(*names):
        result = []
        for name in names:
            label = app.get_label_by_name(name)
            if label is None:
                label = app.new_label_object(name, color='accent' if name == 'Freigabe' else 'clear')
                app.labels.append(label)
            result.append(label['id'])
        return result
    def attach(name, content):
        identity = uuid.uuid4().hex
        storage = 'attachments/' + app.safe_attachment_filename(name, identity)
        raw = content.encode('utf-8')
        return {'id': identity, 'name': name, 'storage': storage, 'size': len(raw), 'mime': 'text/plain', 'added_at': ANCHOR.isoformat()}, (storage, base64.b64encode(raw).decode('ascii'))
    def finish(key, kind, holder, lists, folders, files):
        used = {value for obj in lists + folders + list(app.walk_items([item for page in lists for item in page['items']])) for value in obj.get('labels', [])}
        payload = {'app': mod.APP_NAME, 'app_version': mod.APP_VERSION, 'version': app.DATA_SCHEMA_VERSION,
                   'exported_at': ANCHOR.isoformat()+'T00:00:00', 'lists': lists, 'folders': folders,
                   'labels': [label for label in app.labels if label['id'] in used or app.is_system_label(label)],
                   'trash': [], 'active_list_id': lists[0]['id'] if lists else None, 'active_folder_id': holder['id'] if kind == 'folder' else None}
        record = {'id': key, 'kind': kind, 'items': [], 'payload': payload, 'files': files,
                  **{field: holder[field] for field in ('title', 'note', 'labels', 'color')}}
        if any(item.get('due') for page in lists for item in app.walk_items(page['items'])):
            record['schedule_anchor'] = ANCHOR.isoformat()
        app.validate_template_payload(record)
        records.append(record)
    for key, (title, note, texts) in app.LIST_TEMPLATES.items():
        items = []
        for index, (text, description) in enumerate(zip(texts, GUIDES[key])):
            due = ANCHOR.isoformat() if key == 'daily' else (ANCHOR+timedelta(days=index)).isoformat() if key == 'week' else (ANCHOR+timedelta(days=7)).isoformat() if key == 'household' else None
            # Wiederholung, Bearbeitungstag und Aufwand je Vorlage. Bis 3.21.1
            # trugen die Vorlagen nur eine einzige Wiederholungsart und weder
            # Bearbeitungstag noch Aufwand – eine Planungsvorlage konnte die
            # Tagesplanung aus 3.15 damit nicht bedienen. Erinnerungen bleiben
            # bewusst draussen: Eine Vorlage soll beim Import keine
            # Benachrichtigungen anlegen.
            repeat = REPEAT_PLAN.get((key, index), REPEAT_PLAN.get(key))
            plan = PLAN_MINUTES.get(key, {}).get(index)
            task = app.new_item(text, description=description, labels=labels('Planung' if index == 0 else 'Umsetzung'),
                                importance=2 if index == 0 and key != 'shopping' else 0, due=due,
                                due_time='09:00' if key == 'daily' and index == 0 else None, repeat=repeat,
                                planned_date=(ANCHOR + timedelta(days=PLAN_OFFSET.get(key, {}).get(index, 0))).isoformat()
                                if plan is not None else None,
                                estimated_minutes=plan)
            if key not in ('daily', 'shopping') and index == 0:
                task['children'] = [app.new_item('Offene Angaben ergänzen', description='Fehlende Fakten oder Ansprechpartner erfassen.'),
                                    app.new_item('Ergebnis mit Beteiligten bestätigen', description='Die abgestimmte Fassung und den nächsten Schritt dokumentieren.', labels=labels('Freigabe'))]
            items.append(task)
        holder = app.new_list_object(title, items, note=note+' Konkrete Ergebnisse, Labels und Detailbeschreibungen sind vorbereitet; Namen und Fristen beim Einsatz anpassen.', color='confirm' if key in ('shopping','household') else 'clear', labels=labels('Alltag' if key in ('shopping','household','trip') else 'Planung'))
        finish(key, 'list', holder, [holder], [], {})
    for key, title, note, phases in PROJECTS:
        root = app.new_folder_object(title, color='accent', note=note+' Beispielablauf: Umfang, Zuständigkeiten und Terminabstände mit dem konkreten Auftrag abstimmen.', labels=labels('Projekt'))
        lists, folders, files = [], [root], {}
        for index, (phase, tasks) in enumerate(phases):
            children = []
            for offset, (text, description) in enumerate(tasks):
                task = app.new_item(text, description=description+'\nAbschluss: Das beschriebene Ergebnis liegt nachvollziehbar in der Projektablage vor.', labels=labels('Freigabe' if 'freigeben' in text.lower() or 'bestätigen' in text.lower() else 'Umsetzung'), importance=2 if offset == 0 else 1,
                                    due=(ANCHOR+timedelta(days=index*7+offset+1)).isoformat(), due_time='15:00' if offset == 2 else None)
                task['children'] = [app.new_item('Verantwortliche Person und Datenquelle festhalten', description='Name/Rolle und Quelle im Beschreibungstext ergänzen.'),
                                    app.new_item('Ergebnis prüfen und nächsten Schritt festlegen', description='Offene Abweichungen als eigene Aufgabe erfassen.', labels=labels('Qualität'))]
                children.append(task)
            group = app.new_item('Arbeitspaket: '+phase, kind=app.ITEM_KIND_GROUP, children=children, description='Die Gruppe strukturiert den Ablauf; erledigt werden ihre Aufgaben.')
            memo = app.new_item('Projektentscheidung\nAnlass und bestätigtes Ergebnis ergänzen', kind=app.ITEM_KIND_LONG,
                               description='Entscheidung, Datum, verantwortliche Person und Auswirkungen auf Umfang oder Termin hier festhalten.', labels=labels('Abstimmung'))
            listing = app.new_list_object(phase, [app.new_item('Ziel und Arbeitsstand', kind=app.ITEM_KIND_HEADING), memo, group],
                         folder_id=root['id'], note=f'{note} Phase {index+1}: {phase}.', labels=labels('Planung' if index==0 else 'Qualität' if index==2 else 'Umsetzung'), color='clear')
            lists.append(listing)
        child_folder = app.new_folder_object('Freigegebene Unterlagen', parent_id=root['id'], color='export', note='Freigegebene Master und Nachweise hier zuordnen. Der leere Unterordner bleibt beim Export erhalten.', labels=labels('Freigabe'))
        folders.append(child_folder)
        attachment, pair = attach('Projektbriefing.txt', f'{title}\n\nZiel: {note}\n\nObjekt / Projektkennung:\nVerantwortliche Person:\nFreigabe durch:\nAbnahmekriterien:\nAblagepfad:\n\nNur bestätigte Angaben eintragen. Diese Vorlage enthält keine Zugangsdaten.\n')
        root['attachments'] = [attachment]; files[pair[0]] = pair[1]
        attachment, pair = attach('Abnahmecheck.txt', 'Abnahme\n\n[ ] Ziel erreicht\n[ ] Inhalt fachlich geprüft\n[ ] Darstellung und Bedienung geprüft\n[ ] Freigabestand dokumentiert\n[ ] Pflegeverantwortung übergeben\n')
        lists[-1]['attachments'] = [attachment]; files[pair[0]] = pair[1]
        attachment, pair = attach('Entscheidungsnotiz.txt', 'Anlass:\nGeprüfte Optionen:\nEntscheidung:\nVerantwortliche Person:\nDatum:\nNächster Schritt:\n')
        lists[0]['items'][1]['attachments'] = [attachment]; files[pair[0]] = pair[1]
        finish(key, 'folder', root, lists, folders, files)
    # Stabile IDs machen den Erzeuger diffbar und einfach reproduzierbar.
    for record in records:
        stable_timestamp = ANCHOR.isoformat() + 'T00:00:00+02:00'
        def stabilize_timestamps(value):
            if isinstance(value, dict):
                for field in ('created_at', 'updated_at'):
                    if field in value:
                        value[field] = stable_timestamp
                # Das Momentdatum wird ohne Vorgabe aus der Erzeugungszeit
                # abgeleitet und wäre sonst vom Erzeugungstag abhängig.
                if isinstance(value.get('journal'), dict) and 'moment_date' in value['journal']:
                    value['journal']['moment_date'] = ANCHOR.isoformat()
                for child in value.values():
                    stabilize_timestamps(child)
            elif isinstance(value, list):
                for child in value:
                    stabilize_timestamps(child)
        stabilize_timestamps(record)
        mapping = {}
        def collect(value):
            if isinstance(value, dict):
                if isinstance(value.get('id'), str):
                    mapping.setdefault(value['id'], uuid.uuid5(uuid.NAMESPACE_URL, 'glide/templates/'+record['id']+'/'+str(len(mapping))).hex)
                for child in value.values(): collect(child)
            elif isinstance(value, list):
                for child in value: collect(child)
        collect(record['payload'])
        raw = json.dumps(record, ensure_ascii=False)
        for old, new in mapping.items(): raw = raw.replace(old, new)
        record.clear(); record.update(json.loads(raw))
    return {'format_version': app.TEMPLATE_FORMAT_VERSION, 'templates': records}

if __name__ == '__main__':
    with tempfile.TemporaryDirectory(prefix='glide-template-build-') as temporary:
        os.environ['GLIDE_DATA_DIR'] = temporary
        loader = importlib.machinery.SourceFileLoader('glide_template_build', str(ROOT/'src/glide/app.pyw'))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        mod = importlib.util.module_from_spec(spec); loader.exec_module(mod)
        data = build(mod)
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        # newline='\n': Der Katalog soll auf jeder Plattform Byte für Byte
        # gleich entstehen. Ohne diese Angabe schreibt Windows CRLF, und die
        # Prüfsumme gegen den kanonischen Stand geht auseinander, ohne dass
        # sich ein Inhalt geändert hätte.
        TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n',
                          encoding='utf-8', newline='\n')
        print(f'{len(data["templates"])} vollständige Vorlagen: {TARGET}')
