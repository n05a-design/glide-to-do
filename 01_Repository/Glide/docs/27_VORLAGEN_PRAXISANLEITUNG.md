# Vorlagen im Unternehmensalltag

Stand 16.10.2026 · Glide 3.43.1 · Aufgabenformat 25 · Vorlagenformat 2

3.28 ergänzt vier integrierte Tagebuchvorlagen: Tagesnotiz, Dankbarkeit,
Wochenrückblick und Jahresordner mit Quartalen. Sie verwenden Notizseiten und
Tagebuch-Metadaten; bestehende eigene Vorlagen werden nicht überschrieben.
Seit dem 27.09.2026 heißen sie „Notizbuch – Tagesnotiz“ usw.; unveränderte
mitgelieferte Namen ziehen in bestehenden Vorlagendateien mit.

Seit dem 27.09.2026 gibt es außerdem Seitenvorlagen (Bericht, Besprechung,
Projektseite und eigene Seiten) im „+“ neben „Seiten“.

## Die passende Datei

- **[glide_vorlagen.glidetemplates](../src/glide/resources/templates/glide_vorlagen.glidetemplates)**: 16 wiederverwendbare portable Vorlagen; kanonischer aktueller Katalog im Ressourcenordner.
  Auf „Vorlagen“ unten „Vorlagen hinzufügen …“ wählen. Die Datei ergänzt den
  Katalog. Bei gleichem Vorlagen-ID wird eine unabhängige Kopie ergänzt.
- **[glide_beispieldaten.glidebackup](../tests/fixtures/beispiele/glide_beispieldaten.glidebackup)**: künstlicher Aufgabenbestand zum
  Ausprobieren von Ansichten, Wiederholungen, Labels und Anhängen. Die Liste „Kalender, Erinnerungen und Tagesplanung“ deckt zusätzlich Erinnerungen, Tagesplanung und den Kalenderrundlauf ab.
- **[glide_releaseplanung_3.42.0.glidebackup](../tests/fixtures/beispiele/glide_releaseplanung_3.42.0.glidebackup)**: interne Aufgaben zur Veröffentlichung
  von Glide. Dies ist keine allgemeine Unternehmensvorlage und keine Releasefreigabe.

Die beiden `.glidebackup`-Dateien über **Listen/Ordner hinzufügen …** ergänzen.
Ein Komplettimport ersetzt den Aufgabenbestand nach vorheriger Sicherung.
Vorlagen, persönliche Einstellungen und Aktivitätshistorie gehören nicht zum
Aufgabenbackup. Den Vorlagenkatalog separat exportieren; den gesamten Datenordner
bei geschlossener App kopieren, wenn wirklich alle Einstellungen mitgesichert werden sollen.

## Katalog

| Vorlage | Geeigneter Einsatz | Vorbereitet |
|---|---|---|
| Tagesplanung | Heute fokussiert arbeiten | Ergebnis, Eingang, Zeitfenster, Tagesabschluss; Wichtigkeit und heutige Termine |
| Projektstart | Kleinen Auftrag strukturieren | Ziel, Anforderungen, Schritte, nächster Schritt, Abnahme |
| Einkauf | Konkreten Bedarf sammeln | Warengruppen mit Hinweisen zu Mengen und Vorräten |
| Wochenplanung | Kapazität und Zusagen planen | Rückblick, Schwerpunkte, Fristen, Puffer, Wochenabschluss |
| Besprechung | Entscheidungen vorbereiten | Ziel, Teilnehmende, Agenda, Unterlagen, Protokoll, Nachhalten |
| Reise | Reise vorbereiten | Route, Buchungen, Dokumente, Packen, Abwesenheit |
| Einarbeitung | Neue Person begleiten | Arbeitsplatz, Ansprechperson, erste Woche, Abläufe, Feedback |
| Veröffentlichung | Beitrag produzieren | Zielgruppe, Gliederung, Text, Rechte, Korrektur, Veröffentlichung |
| Haushalt | Wiederkehrende Aufgaben | Wöchentliche Wiederholungen, konkrete Ausführungshinweise |
| Rückblick | Abläufe verbessern | Ergebnisse, Hindernisse, Weglassen, drei nächste Verbesserungen |
| Projekt | Kundenprojekt steuern | Drei Phasen, Freigaben, Unterpunkte, Entscheidungsnotizen und Anhänge |
| Veranstaltung | Firmenveranstaltung organisieren | Vorbereitung, Durchführung, Nachbereitung |
| Immobilienvermarktung | Objekt für den Vertrieb aufbereiten | Unterlagen, Exposé, Objektseite, fachliche Freigabe und Anfrageweg |
| WordPress-Relaunch | Website erneuern | Bestand, Design, Umsetzung, Staging-Abnahme, Livegang und Pflege |
| WEG-Verwaltung | Objektbezogene Vorgänge bearbeiten | Eingang, Zuständigkeit, Dienstleister, Nachweise und Wiedervorlage |
| Baukommunikation | Bauabschnitte kommunizieren | Fakten, Zielgruppen, Freigaben, Veröffentlichung und Aktualisierung |

## Empfohlener Ablauf

1. Vorlage auswählen und einmal am konkreten Auftrag prüfen.
2. Über „Bearbeiten“ den Entwurf öffnen. Titel und Beschreibung an das Projekt anpassen.
3. Unter „Vorlagendetails“ Farbe, Labels und allgemeine Unterlagen pflegen.
4. Im Strukturbaum jeden Punkt über „Bearbeiten“ konkretisieren. Verantwortliche
   Person in der Beschreibung nennen; Glide besitzt kein separates Zuweisungsfeld.
5. Überflüssige Punkte entfernen, fehlende Punkte oder Unterpunkte ergänzen.
   Auf- und Abwärtsschaltflächen verschieben den gesamten Eintrag samt Unterpunkten.
6. Termine und Wiederholungen prüfen. Die relative Option verschiebt alle Termine
   gemeinsam ab dem angezeigten Bezugsdatum; ohne die Option bleiben sie absolut.
7. „Übernehmen“, anschließend auf der Vorlagenseite „Vorlagen speichern“.
8. „Verwenden“ erzeugt neue Arbeitslisten und Ordner. Aufgaben beginnen unerledigt.
   Anschließend tatsächliche Ansprechpartner, Datenquellen und verbindliche Termine ergänzen.

Eine geänderte Vorlage aktualisiert keine bereits daraus angelegten Listen.
Die Beispielanhänge „Projektbriefing“, „Abnahmecheck“ und „Entscheidungsnotiz“ sind
kleine bearbeitbare Textdateien. Eigene Freigabedokumente können sie ersetzen.
Keine Zugangsdaten in Beschreibungen oder ungeschützt exportierten Anhängen ablegen.

## Bedienung des überarbeiteten Editors

Der Strukturbaum verwendet dieselben Hell-/Dunkelfarben wie die Listenansicht.
Eintrag auswählen und „Bearbeiten“, F2, Enter oder Doppelklick verwenden, um die
Details zu öffnen. Eingeklappte Zweige bleiben beim Aktualisieren erhalten.
Metadaten passen sich der Fensterbreite an; Abschlussaktionen bleiben unten erreichbar.

Auf dem Mac erscheinen Auswahlfelder und ihre Auswahlliste in App-Farben.
Pfeiltasten wählen einen Eintrag, Enter übernimmt, Escape verwirft die Auswahl.
Das vorherige Dialogfenster bleibt danach bedienbar. Unter Windows bleibt der
bisherige Dropdown-Typ erhalten.

## Funktionsabdeckung

Der Katalog zeigt alle vier Punktarten, Gruppen/Unterpunkte, Labels an Punkten,
Listen und Ordnern, Farben, Wichtigkeit, Datum und Uhrzeit, Wiederholung,
Beschreibungen, Anhänge auf allen drei Ebenen sowie leere Unterordner. Die
Funktionsvorschau ergänzt erledigte/überfällige Punkte, Papierkorb, Kalender,
Jahresraster, Tabellenansicht, „Heute“, Reiter, Pinnwand und konkrete
Prüfaufgaben für Scrollen und Vorlagenbearbeitung.

Einstellungen, Kalender, Startseite, Suche, Undo und Datenordnerwahl sind
Bedienfunktionen der Anwendung. Eine Vorlagendatei speichert diese Einstellungen
nicht und führt keine Veröffentlichung, Kontaktaufnahme oder Webaktion aus.

[Daten und Backups](06_DATA_BACKUP_MIGRATION.md)

Seit 3.14 übernehmen Vorlagen Bearbeitungstag und geschätzten Aufwand. Bei relativen Vorlagen verschiebt sich der Bearbeitungstag um denselben Abstand wie die Fälligkeit, auch ohne Frist am Punkt. Feste Vorlagen lassen die Daten unverändert. Der Aufwand bleibt konstant. Aktuelle mitgelieferte Teilpayloads verwenden Aufgabenformat 25; das Vorlagencontainerformat bleibt 2. Ältere importierte Teilpayloads werden nach den unterstützten Migrationsregeln behandelt, der aktuelle Katalog darf nicht in eine ältere Fassung zurückkopiert werden.

## Eingabefelder in Vorlagen (seit 3.30)

**Platzhalter anlegen:** Eine Vorlage kann Platzhalter tragen, zum Beispiel
`{{Projektname}}`, `{{Kunde}}` oder `{{Datum}}`. Sie stehen einfach im Text –
in Listentitel, Punkten, Beschreibungen, Checklisten oder im Notiztext. Dann
die Liste wie gewohnt als Vorlage speichern.

**Vorlage verwenden:** Seit 3.33.18 auch über „Neu → Aus Vorlage …“ in der Bibliothek bzw. im Anlegen-Menü. Nach dem Ausfüllen zeigt Glide vor dem Anlegen die vorbereiteten Inhalte, Unteraufgaben, Termine und gegebenenfalls das Titelbild. „Anlegen“ bzw. Return übernimmt genau diese vorbereiteten Werte; Abbrechen bzw. Escape erhält den Bestand. Der Vorlagenkatalog bleibt ebenfalls als Einstieg verfügbar.

- Glide fragt jeden Namen einmal in einem kleinen Dialog ab (höchstens zwölf).
- Die Angabe steht danach überall, wo der Platzhalter stand.
- Vorbelegt sind `{{Datum}}`, `{{Heute}}` und `{{Tag}}` mit dem heutigen
  Datum und `{{Jahr}}` mit dem Jahr.
- Abbrechen legt nichts an.
- Die Vorlage selbst bleibt unverändert.
- Formatierungen im Notiztext verschieben sich mit, sodass fett oder kursiv
  gesetzte Stellen erhalten bleiben.

