# Dokumentationsindex

Stand 06.10.2026 · Glide 3.33.8 · Aufgabenformat 20 · Einstellungen 2 · Vorlagenformat 2

Seit 03.10.2026 zwölf Dokumente und fünf Einzelentscheidungen statt 53: Funktionsverträge 45–79, Projektübergabe, Startkontext, Entwicklungsnotizen, Sitzungsprotokoll, Releasecheckliste und Lizenz-, Signierungs- und Vertriebsentwürfe sind in die Dokumente unten eingegangen. Ältere Fassungen trägt Git (`git log --follow docs/<Datei>`). Am 05.10.2026 mit einer gekürzten Fassung aus der Windows-Arbeitskopie zusammengeführt; deren Synchronisationskopien und die wiederaufgetauchte Projektübergabe sind aufgelöst. Regeln: [Dokumentenpflege](DOKUMENTENPFLEGE.md).

## Einstieg

- **Neue Sitzung:** [Übergabe](../../../00_Arbeitsvorbereitung/Glide_Uebergabe.md), dann [Arbeitsregeln](../AGENTS.md).
- **Was als Nächstes ansteht:** [Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md).
- **Was entschieden ist:** [Arbeitsrichtung](ARBEITSRICHTUNG.md).

## Dokumente

| Dokument | Inhalt |
|---|---|
| [01 Produktgrenzen und Prinzipien](01_PRODUCT_CONSTRAINTS.md) | Was Glide ist und nicht wird, sechs Produktprinzipien, Prinzipien-Check, Grenzen einzelner Funktionen |
| [02 Architektur](02_ARCHITECTURE.md) | Module, Speicherweg, Bausteine der Oberfläche, Performance-Regeln, Tk-Fallstricke |
| [05 Prüfplan](05_QA_TESTPLAN.md) | Prüfstufen, Regeln, Schritte, Integrationssuiten nach Bereich, manuelle Kontrollmatrix |
| [06 Daten, Backups und Migration](06_DATA_BACKUP_MIGRATION.md) | Format 20, Formatstufen, Startprüfung, Sicherungen, Einstellungen, Austauschformat |
| [07 QA-Bericht](07_QA_BERICHT.md) | Geprüfter Stand der Versionen 3.33.0–3.33.8, ältere Ergebnisse, offene manuelle Prüfungen |
| [10 Veröffentlichung](10_VEROEFFENTLICHUNG.md) | Releasecheckliste, Signierung, Vertrieb und Marke, GitHub-Auftritt, Lizenzentwurf, Inhaberangaben, Produktdatenblatt |
| [20 Funktionen](20_FUNKTIONEN.md) | Gültiges Verhalten je Bereich mit Pflichtsuiten und Herkunft (frühere Verträge 45–79) |
| [27 Vorlagen im Unternehmensalltag](27_VORLAGEN_PRAXISANLEITUNG.md) | Praxisanleitung zum Vorlagenkatalog |
| [Arbeitsrichtung](ARBEITSRICHTUNG.md) | Auftrag, Leitgedanken des Inhabers, Entscheidungen D01–D17 und frühere gültige Antworten, Arbeitsablauf |
| [Dokumentenpflege](DOKUMENTENPFLEGE.md) | Ein Thema, ein Dokument; Aufbewahrung; Zuständigkeiten |
| [Fehlerdiagnose Logo](diagnosen/LOGO_KANTENGLAETTUNG.md) | Logo ohne Kantenglättung unter Tk 8.6: Ursache, Nachweise, Lösungswege; gelöscht, sobald die gewählten Wege umgesetzt sind |

## Einzelentscheidungen

| Entscheidung | Gegenstand |
|---|---|
| [Produktregister](decisions/PRODUCT_IDENTITY.md) | Technisch belegte Werte und offene Inhaber-/Store-Angaben; Quelle für Build- und Store-Konfigurationen |
| [tkinterdnd2](decisions/ABHAENGIGKEIT_TKDND.md) | Einzige mitgelieferte Bibliothek für das Ziehen aus Finder/Explorer |
| [Arbeitsbegleiter](decisions/ARBEITSBEGLEITER.md) | Gismo als Markenfigur, Zustände, Grenzen |
| [Gruppe, Ordner, Überschrift](decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md) | Wann welches Gliederungsmittel |
| [Systembenachrichtigungen](decisions/SYSTEMBENACHRICHTIGUNGEN.md) | Betriebszustände und Grenzen der Erinnerungszustellung |

## Begriffe

- **Punkt:** Oberbegriff für die Einträge einer Liste; Arten: **Aufgabe** (`task`), **Gruppe** (`group`), **Long-Task** (`long`, mehrzeilig; Zielbegriff „Langtext“, U16), **Zwischenüberschrift** (`heading`). Wann Gruppe, Ordner oder Überschrift: [Entscheidung](decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md).
- **Aufgabenliste** (`tasks`): Punkte als Liste, Tabelle oder Pinnwand. **Pinnwand:** Ansicht auf Aufgaben einer Liste, eines Ordners oder des Bestands, frei oder als Spaltenboard; kein eigener Inhaltstyp.
- **Notiz** (`note`): Rich-Text mit Aufgabenbereich darüber. **Seite** (`page`): langes Dokument mit echten Aufgaben, ohne Unterseiten. **Galerie** (`gallery`): Bildersammlung aus Anhängen. **Zeichnung** (`drawing`): Pixelfläche mit 16–128 Zellen.
- **Ordner, Buch** (`library`, früher „Bibliothek“), **Notizbuch** (`journal`, früher „Tagebuch“): Ordnerarten; das Notizbuch ordnet nach Momentdatum.
- **Heute** (früher „Mein Tag“) und **Demnächst** (früher „In Bearbeitung“): die zwei Hauptansichten (D14).
- **Bearbeitungstag** (`planned_date`): wann man etwas anfasst. **Fälligkeit** (`due`): bis wann es fertig sein muss.
- **Archiv:** Status `archived` einer Liste oder eines Ordners; zurückholbar.

## Weitere Orte

- Arbeitsregeln: [AGENTS.md](../AGENTS.md) · Änderungsverlauf: [CHANGELOG.md](../CHANGELOG.md) · Sicherheit: [SECURITY.md](../SECURITY.md)
- Prüfwerkzeuge: [tests/README.md](../tests/README.md), [tests/tools/README.md](../tests/tools/README.md) · Pflegewerkzeuge: [scripts/pflege/README.md](../scripts/pflege/README.md)
- Code: [src/glide/README.md](../src/glide/README.md) · Paketierung: [packaging/README.md](../packaging/README.md) · Lizenzstatus: [LICENSE.md](../LICENSE.md)
- Showcase: [tests/fixtures/showcase/README.md](../tests/fixtures/showcase/README.md)
- Planung, Markt und Vorbilder, manuelle Prüfung: [00_Arbeitsvorbereitung](../../../00_Arbeitsvorbereitung/README.md)
