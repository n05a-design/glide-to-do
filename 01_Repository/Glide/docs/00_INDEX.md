# Dokumentationsindex

Stand 24.11.2026 · Glide 1.0.3 · Aufgabenformat 26 · Glide-System V1.87

Am 04.11.2026 zusammengeführt und gekürzt: ersetzte Sitzungsstände und historische Prioritäten aus dem Einstieg entfernt. Dieser Index beschreibt Zuständigkeiten; datierte Prüfungsergebnisse stehen im QA-Bericht.

## Einstieg nach Aufgabe

- **Erster Einstieg und Mitwirkung:** [Projektübersicht](../../../README.md) und [An Glide arbeiten](../../../CONTRIBUTING.md).
- **Englische Benutzerdokumentation:** [Glide user guide](user-guide/README.md) als kontrollierte Übersetzung von [20 Funktionen](20_FUNKTIONEN.md).
- **Neue Sitzung und aktueller Stand:** [Übergabe](../../../00_Arbeitsvorbereitung/Glide_Uebergabe.md), danach [Arbeitsregeln](../AGENTS.md).
- **Aufgaben und nächste Auswahl:** [einzige Roadmap](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) und [Meilenstein-Plan v1.0](../../../00_Arbeitsvorbereitung/Glide_Meilenstein_v1_Plan.md).
- **System-und-Modulpflege:** [Glide-System](../src/glide/README.md) – verbindliches vollständiges Modul-, Feature-, Baustein-, QA- und Testinventar; unabhängig versioniert über [`GLIDE_SYSTEM_VERSION`](../GLIDE_SYSTEM_VERSION) (Start V1.0), Änderungen samt Versionsverlauf im selben Commit.
- **Prüfung und Lieferung:** [QA-Bericht](07_QA_BERICHT.md); Versionsnummer, gezielte Prüfung, Vollmatrix, Paketlieferung und menschliche Abnahme getrennt beurteilen.
- **Produktentscheidungen und Gestaltung:** [Arbeitsrichtung](ARBEITSRICHTUNG.md), [Design Richtlinien](DESIGN_RICHTLINIEN.md).
- **Architektur, Bestand und Zielbild:** [Architektur](02_ARCHITECTURE.md), [Glide-System](../src/glide/README.md) und [Shell-Konzept](GLIDE_SHELL_FRAMEWORK_KONZEPT.md) haben getrennte Zuständigkeiten.
- **An der Glide Shell arbeiten:** [Arbeitshandbuch für KI-Agenten](GLIDE_SHELL_KI_HANDBUCH.md), Nutzung für Folgeprojekte in [`glide_shell/README.de.md`](../src/glide/glide_shell/README.de.md).
- **Am Glide Bento Box System arbeiten:** [Bento-Konzept](GLIDE_BENTO_SYSTEM_KONZEPT.md), Gestaltungsvertrag in [`glide_bento/BENTO_DESIGN_CONTRACT.md`](../src/glide/glide_bento/BENTO_DESIGN_CONTRACT.md), Nutzung für Folgeprojekte in [`glide_bento/README.de.md`](../src/glide/glide_bento/README.de.md).
- **Bestehende Anwendung in die Glide Shell überführen (KI-Agenten):** [`glide_shell/KI_MIGRATION_BESTEHENDE_ANWENDUNG.md`](../src/glide/glide_shell/KI_MIGRATION_BESTEHENDE_ANWENDUNG.md) ([English](../src/glide/glide_shell/AI_MIGRATION_EXISTING_APPS.md)) – Ablauf in 16 Schritten, Datenschutz, konkurrierende Komponenten, Tests, Abschluss, Startprompt; verbindlich dazu der [Shell-First-Vertrag](../src/glide/glide_shell/DESIGN_RICHTLINIEN.md#5-shell-first-vertrag-d105-d106).
- **Mit der Glide Shell ein neues Projekt bauen (KI-Agenten):** [`glide_shell/KI_ANLEITUNG_NEUE_PROJEKTE.md`](../src/glide/glide_shell/KI_ANLEITUNG_NEUE_PROJEKTE.md) ([English](../src/glide/glide_shell/AI_GUIDE_NEW_PROJECTS.md)) – Aufbau von Glide, Glide-System und Shell, Architekturregeln, Design-Richtlinien, Prozesse, Prüfungen und Prüflisten; fertiger Startprompt für neue Sitzungen in [`glide_shell/STARTPROMPT_KI.md`](../src/glide/glide_shell/STARTPROMPT_KI.md).
- **Shell-Migration vorbereiten:** [Fable-Masterprompt](FABLE_GLIDE_SHELL_MIGRATION_PROMPT.md) mit Quellstand, Planungsauftrag und Freigabegrenzen.
- **Änderungen übergreifend abgleichen und Dokumente konsolidieren:** [Pflegematrix](DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) und [Abgleich ohne doppelte Pflege](DOKUMENTENPFLEGE.md#abgleich-ohne-doppelte-pflege).

## Dokumente

| Dokument | Inhalt |
|---|---|
| [01 Produktgrenzen und Prinzipien](01_PRODUCT_CONSTRAINTS.md) | Was Glide ist und nicht wird, sechs Produktprinzipien, Prinzipien-Check, Grenzen einzelner Funktionen |
| [02 Architektur](02_ARCHITECTURE.md) | Module, Speicherweg, Bausteine der Oberfläche, Performance-Regeln, Tk-Fallstricke |
| [05 Prüfplan](05_QA_TESTPLAN.md) | Prüfstufen, Regeln, Schritte, Integrationssuiten nach Bereich, manuelle Kontrollmatrix |
| [06 Daten, Backups und Migration](06_DATA_BACKUP_MIGRATION.md) | Format 26, ältere Formatstufen, Startprüfung, Sicherungen, Einstellungen, Austauschformat |
| [07 QA-Bericht](07_QA_BERICHT.md) | Commitbezogene Prüfstände, plattformübergreifende CI, native Lieferstände, Archivabgleich, historische Ergebnisse und offene Abnahmen |
| [10 Veröffentlichung](10_VEROEFFENTLICHUNG.md) | Releasecheckliste, Signierung, Vertrieb und Marke, GitHub-Auftritt, MPL-2.0, Inhaberangaben, Produktkommunikation und Produktdatenblatt |
| [20 Funktionen](20_FUNKTIONEN.md) | Gültiges Verhalten je Bereich mit Pflichtsuiten und Herkunft (frühere Verträge 45–79) |
| [English user guide](user-guide/README.md) | Kontrollierte englische Übersetzung von 20 Funktionen für Nutzer, keine zweite Fachautorität; Lokalisierungsstand der Oberfläche |
| [27 Vorlagen im Unternehmensalltag](27_VORLAGEN_PRAXISANLEITUNG.md) | Praxisanleitung zum Vorlagenkatalog |
| [Arbeitsrichtung](ARBEITSRICHTUNG.md) | Auftrag, Leitgedanken, Entscheidungen D01–D106 (D49 mit Korrekturvorbehalt), frühere gültige Antworten und Arbeitsablauf |
| [Dokumentenpflege](DOKUMENTENPFLEGE.md) | Zentrale Pflegematrix mit führenden Quellen und Änderungsbezügen; Konsolidierung, Aufbewahrung und Prüfgrenzen |
| [Gemini-Wissensbasis](ai/gemini/README.md) | Englischsprachige, quellengebundene Wissensbasis für Gemini; abgeleitete Zusammenfassung, keine zusätzliche Fachautorität |
| [Glide Shell – Arbeitshandbuch für KI-Agenten](GLIDE_SHELL_KI_HANDBUCH.md) | Einstieg für Agenten: Bausteine, Host-Verträge, erzwungene Regeln, Tests T055/T312–T336, Prüfwege, Versionierung, Übernahme, Git-Ablauf und Prüfliste für neue Bausteine; verweist auf die führenden Quellen |
| [Glide Shell Framework](GLIDE_SHELL_FRAMEWORK_KONZEPT.md) | Architektur- und Entkopplungskonzept für das wiederverwendbare Desktop-Fundament, Fensterorchestrierung und Migrationspfad |
| [Glide Bento Box System](GLIDE_BENTO_SYSTEM_KONZEPT.md) | Architektur- und UI-Kompositionskonzept für das wiederverwendbare kartenbasierte Bento-System (Ebene B, D100) |
| [Arbeitsvorlage zur Shell-Migration](FABLE_GLIDE_SHELL_MIGRATION_PROMPT.md) | Arbeitsübergabe für die Shell-Migration: Abschnitt 1 und die Pakete 1–2c sind mit 3.60.0 umgesetzt; jedes Folgepaket braucht eine eigene Freigabe ([Plan §21.89](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2189-glide-3600-erste-shell-schnitte-start-baseline-und-beruhigter-einstellungsdialog-13112026)) |
| [Design Richtlinien](DESIGN_RICHTLINIEN.md) | Belegte UI-/UX-Vorgaben, Buttonschutz, Informationshierarchie, Fluchten, Symbole und Pflege; appweiter Gestaltungsvertrag, Kontext-/Komponentenmatrix und getrennte menschliche Abnahme |

### English user guide – Themenseiten

| Nr. | Seite |
|---|---|
| 1 | [Getting started](user-guide/01-getting-started.md) |
| 2 | [Installation](user-guide/02-installation.md) |
| 3 | [Tasks and lists](user-guide/03-tasks-and-lists.md) |
| 4 | [Day planning](user-guide/04-day-planning.md) |
| 5 | [Calendar](user-guide/05-calendar.md) |
| 6 | [Pages and notes](user-guide/06-pages-and-notes.md) |
| 7 | [Pinboards](user-guide/07-pinboards.md) |
| 8 | [Pixel workshop](user-guide/08-pixel-workshop.md) |
| 9 | [Import and export](user-guide/09-import-and-export.md) |
| 10 | [Backups](user-guide/10-backups.md) |
| 11 | [Keyboard shortcuts](user-guide/11-keyboard-shortcuts.md) |
| 12 | [Troubleshooting](user-guide/12-troubleshooting.md) |

### Gemini-Wissensbasis – Einzelmodule

| Modul | Dokument |
|---|---|
| 01 | [Project overview](ai/gemini/01_PROJECT_OVERVIEW.md) |
| 02 | [Gemini master context](ai/gemini/02_GEMINI_MASTER_CONTEXT.md) |
| 03 | [Glossary and ontology](ai/gemini/03_GLOSSARY_AND_ONTOLOGY.md) |
| 04 | [System architecture](ai/gemini/04_SYSTEM_ARCHITECTURE.md) |
| 05 | [Codebase reference](ai/gemini/05_CODEBASE_REFERENCE.md) |
| 06 | [Data model and persistence](ai/gemini/06_DATA_MODEL_AND_PERSISTENCE.md) |
| 07 | [Feature inventory](ai/gemini/07_FEATURE_INVENTORY.md) |
| 08 | [User workflows](ai/gemini/08_USER_WORKFLOWS.md) |
| 09 | [UX/UI design system](ai/gemini/09_UX_UI_DESIGN_SYSTEM.md) |
| 10 | [Internationalization](ai/gemini/10_INTERNATIONALIZATION.md) |
| 11 | [Development guide](ai/gemini/11_DEVELOPMENT_GUIDE.md) |
| 12 | [Testing and quality](ai/gemini/12_TESTING_AND_QUALITY.md) |
| 13 | [Security, privacy, and reliability](ai/gemini/13_SECURITY_PRIVACY_RELIABILITY.md) |
| 14 | [Roadmap and backlog](ai/gemini/14_ROADMAP_AND_BACKLOG.md) |
| 15 | [Product research and competition](ai/gemini/15_PRODUCT_RESEARCH_AND_COMPETITION.md) |
| 16 | [Product strategy and marketing](ai/gemini/16_PRODUCT_STRATEGY_AND_MARKETING.md) |
| 17 | [Decisions and history](ai/gemini/17_DECISIONS_AND_HISTORY.md) |
| 18 | [Known issues and technical debt](ai/gemini/18_KNOWN_ISSUES_AND_TECH_DEBT.md) |
| 19 | [Integrations and ecosystem](ai/gemini/19_INTEGRATIONS_AND_ECOSYSTEM.md) |
| 20 | [AI development playbook](ai/gemini/20_AI_DEVELOPMENT_PLAYBOOK.md) |
| Support | [Core Knowledge Pack](ai/gemini/GEMINI_CORE_KNOWLEDGE_PACK.md), [Source Manifest](ai/gemini/SOURCE_MANIFEST.md), [Knowledge Gaps](ai/gemini/KNOWLEDGE_GAPS.md), [Import Guide](ai/gemini/GEMINI_IMPORT_GUIDE.md), [Knowledge Changelog](ai/gemini/KNOWLEDGE_CHANGELOG.md), [Final Audit](ai/gemini/FINAL_AUDIT.md) |

## Einzelentscheidungen

| Entscheidung | Gegenstand |
|---|---|
| [Produktregister](decisions/PRODUCT_IDENTITY.md) | Technisch belegte Werte und offene Inhaber-/Store-Angaben; Quelle für Build- und Store-Konfigurationen |
| [Post-Release Entscheidungsvorlagen](decisions/POST_RELEASE_ENTSCHEIDUNGSVORLAGEN.md) | 14 vollständige Entscheidungsvorlagen (M01–M15) für die strategische Weiterentwicklung nach v1.0.2 |
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
- Code: [src/glide/README.md](../src/glide/README.md) · Glide Shell für Folgeprojekte: [Anleitung](../src/glide/glide_shell/README.de.md) ([English](../src/glide/glide_shell/README.md)) · Paketierung: [packaging/README.md](../packaging/README.md) · Lizenzstatus: [LICENSE.md](../LICENSE.md)
- Showcase: [tests/fixtures/showcase/README.md](../tests/fixtures/showcase/README.md)
- Planung, Markt und Vorbilder, manuelle Prüfung: [00_Arbeitsvorbereitung](../../../00_Arbeitsvorbereitung/README.md)
- Neuer UI-/UX-Auftrag: [Ausführungsprompt mit Originalauftrag und 28 Bildreferenzen](../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/PROMPT.md); Aufgabenstatus im Entwicklungsplan §17. Originalbilder nur in der lokalen Ablage.

**Logo-Wechsel (D62):** [Zentrale Fundorte, Symbole und Aktualisierungsschritte](../../../20_Grafik_Master/README.md); [Logo-/Darkmode-Nachweis in Git-Fassung vom 05.11.2026](https://github.com/n05a-design/glide-to-do/blob/d55ff46da11f1ffb57cd1a71dbdc828565e3ffff/01_Repository/Glide/tests/qa-3.50.3/logo_2026-11-05/README.md).
