# Dokumentationsindex

Stand 05.11.2026 · Glide 3.50.5 · Erster öffentlicher Stand (intern: öffentliche erste Beta) · Aufgabenformat 26

Am 04.11.2026 zusammengeführt und gekürzt: ersetzte Sitzungsstände und historische Prioritäten aus dem Einstieg entfernt. Dieser Index beschreibt Zuständigkeiten; datierte Prüfungsergebnisse stehen im QA-Bericht.

## Einstieg nach Aufgabe

- **Neue Sitzung und aktueller Stand:** [Übergabe](../../../00_Arbeitsvorbereitung/Glide_Uebergabe.md), danach [Arbeitsregeln](../AGENTS.md).
- **Aufgaben und nächste Auswahl:** [einzige Roadmap, Plan §21.62](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2162-stand-roadmap-und-mehrwertanalyse-vom-04112026).
- **Prüfung und Lieferung:** [QA-Bericht](07_QA_BERICHT.md); Versionsnummer, gezielte Prüfung, Vollmatrix, Paketlieferung und menschliche Abnahme getrennt beurteilen.
- **Produktentscheidungen und Gestaltung:** [Arbeitsrichtung](ARBEITSRICHTUNG.md), [Design Richtlinien](DESIGN_RICHTLINIEN.md).
- **Dokumente ändern oder löschen:** [Dokumentenpflege](DOKUMENTENPFLEGE.md).

## Dokumente

| Dokument | Inhalt |
|---|---|
| [01 Produktgrenzen und Prinzipien](01_PRODUCT_CONSTRAINTS.md) | Was Glide ist und nicht wird, sechs Produktprinzipien, Prinzipien-Check, Grenzen einzelner Funktionen |
| [02 Architektur](02_ARCHITECTURE.md) | Module, Speicherweg, Bausteine der Oberfläche, Performance-Regeln, Tk-Fallstricke |
| [05 Prüfplan](05_QA_TESTPLAN.md) | Prüfstufen, Regeln, Schritte, Integrationssuiten nach Bereich, manuelle Kontrollmatrix |
| [06 Daten, Backups und Migration](06_DATA_BACKUP_MIGRATION.md) | Format 26, ältere Formatstufen, Startprüfung, Sicherungen, Einstellungen, Austauschformat |
| [07 QA-Bericht](07_QA_BERICHT.md) | Quelle/Python 3.50.5, Abnahmekorrekturen und native Lieferstände getrennt, A01-Fortsetzung, WA-09, ursprüngliches Abnahmeaudit, WA-41-Diagnose, Liefergrenzen und Datei-/Dokumentabgleich; historische Ergebnisse und offene Abnahmen |
| [10 Veröffentlichung](10_VEROEFFENTLICHUNG.md) | Releasecheckliste, Signierung, Vertrieb und Marke, GitHub-Auftritt, Lizenzentwurf, Inhaberangaben, Produktdatenblatt |
| [20 Funktionen](20_FUNKTIONEN.md) | Gültiges Verhalten je Bereich mit Pflichtsuiten und Herkunft (frühere Verträge 45–79) |
| [27 Vorlagen im Unternehmensalltag](27_VORLAGEN_PRAXISANLEITUNG.md) | Praxisanleitung zum Vorlagenkatalog |
| [Arbeitsrichtung](ARBEITSRICHTUNG.md) | Auftrag, Leitgedanken, Entscheidungen D01–D63 (D49 mit Korrekturvorbehalt), frühere gültige Antworten und Arbeitsablauf |
| [Dokumentenpflege](DOKUMENTENPFLEGE.md) | Ein Thema, ein Dokument; Aufbewahrung; Zuständigkeiten |
| [Design Richtlinien](DESIGN_RICHTLINIEN.md) | Belegte UI-/UX-Vorgaben, Buttonschutz, Informationshierarchie, Fluchten, Symbole und Pflege; appweiter Gestaltungsvertrag, Kontext-/Komponentenmatrix und getrennte menschliche Abnahme |

## Einzelentscheidungen

| Entscheidung | Gegenstand |
|---|---|
| [Produktregister](decisions/PRODUCT_IDENTITY.md) | Technisch belegte Werte und offene Inhaber-/Store-Angaben; Quelle für Build- und Store-Konfigurationen |
| [tkinterdnd2](decisions/ABHAENGIGKEIT_TKDND.md) | Einzige mitgelieferte Bibliothek für das Ziehen aus Finder/Explorer |
| [Arbeitsbegleiter](decisions/ARBEITSBEGLEITER.md) | Gismo als Markenfigur, Zustände, Grenzen |
| [Gruppe, Ordner, Überschrift](decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md) | Wann welches Gliederungsmittel |
| [Systembenachrichtigungen](decisions/SYSTEMBENACHRICHTIGUNGEN.md) | Betriebszustände und Grenzen der Erinnerungszustellung |

## Begriffe

- **Punkt:** Oberbegriff für die Einträge einer Liste; Arten: **Aufgabe** (`task`), **Gruppe** (`group`), **Langtext** (`long`, mehrzeilig; bis 3.33.15 „Long-Task“, U16), **Zwischenüberschrift** (`heading`). Wann Gruppe, Ordner oder Überschrift: [Entscheidung](decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md).
- **Aufgabenliste** (`tasks`): Punkte als Liste, Tabelle oder Pinnwand. **Pinnwand:** Ansicht auf Aufgaben einer Liste, eines Ordners oder des Bestands, frei oder als Spaltenboard; kein eigener Inhaltstyp.
- **Notiz** (`note`): Rich-Text mit Aufgabenbereich darüber. **Seite** (`page`): langes Dokument mit echten Aufgaben, ohne Unterseiten. **Galerie** (`gallery`): Bildersammlung aus Anhängen. **Zeichnung** (`drawing`): Pixelfläche mit 16–128 Zellen.
- **Ordner, Buch** (`library`, früher „Bibliothek“), **Notizbuch** (`journal`, früher „Tagebuch“): Ordnerarten; das Notizbuch ordnet nach Momentdatum.
- **Heute** (früher „Mein Tag“) und **Demnächst** (früher „In Bearbeitung“): die zwei Hauptansichten (D14).
- **Bearbeitungstag** (`planned_date`): wann man etwas anfasst. **Fälligkeit** (`due`): bis wann es fertig sein muss.
- **Archiv:** Status `archived` einer Liste oder eines Ordners; zurückholbar.

## Weitere Orte

- Arbeitsregeln: [AGENTS.md](../AGENTS.md) · Änderungsverlauf: [CHANGELOG.md](../CHANGELOG.md) · Sicherheit und Vertrauensgrenzen: [SECURITY.md](../SECURITY.md#vertrauensgrenzen)
- Prüfwerkzeuge: [tests/README.md](../tests/README.md), [tests/tools/README.md](../tests/tools/README.md) · Pflegewerkzeuge: [scripts/pflege/README.md](../scripts/pflege/README.md)
- Code: [src/glide/README.md](../src/glide/README.md) · Paketierung: [packaging/README.md](../packaging/README.md) · Lizenzstatus: [LICENSE.md](../LICENSE.md)
- Showcase: [tests/fixtures/showcase/README.md](../tests/fixtures/showcase/README.md)
- Planung, Markt und Vorbilder, manuelle Prüfung: [00_Arbeitsvorbereitung](../../../00_Arbeitsvorbereitung/README.md)
- Neuer UI-/UX-Auftrag: [Ausführungsprompt mit Originalauftrag und 28 Bildreferenzen](../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/PROMPT.md); Aufgabenstatus im Entwicklungsplan §17. Originalbilder nur in der lokalen Ablage.

**Logo-Wechsel (D62):** [Zentrale Fundorte, Symbole und Aktualisierungsschritte](../../../20_Grafik_Master/README.md); [aktueller Logo-/Darkmode-Nachweis](../tests/qa-3.50.3/logo_2026-11-05/README.md).
