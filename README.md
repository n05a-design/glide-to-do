# Glide – lokale Aufgaben, Notizen und Pinnwände

[![Glide-Prüfung](https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml)

Glide ist eine deutschsprachige Desktop-Anwendung für Aufgaben, Listen, Seiten, Notizbücher, Pinnwände und Pixelzeichnungen. Sie läuft lokal mit Python und Tk, braucht weder Konto noch Cloud und hält alle Nutzerdaten außerhalb des Programmordners.

Dieses Repository ist die maßgebliche Projektablage (Entscheidung D09): Die Wurzel ist der Projektordner, der Quellcode liegt in [`01_Repository/Glide`](01_Repository/Glide/README.md).

## Stand

- **Entwicklungsstand 3.33.6 vom 02.10.2026**, Datenformat 20.
- **Geprüft und lokal ausgeliefert am 02.10.2026, keine Releasefassung:** Vollprüfung auf dem Referenz-Mac grün ([Ergebnis](01_Repository/Glide/tests/qa-3.33.6/heute_2026-10-02/vollpruefung/ergebnis.json)); Python-Fassung und Entwicklungsbundle bytegleich ([QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md)).
- **Offen:** Signatur, Markenprüfung, Store und die manuelle Abnahme unter Windows, Linux, DPI-Skalierung und Bildschirmleser.
- **Nächste Schritte:** [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) mit Status je Aufgabe; Entscheidungen in der [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md).

## Schnellstart

Voraussetzung ist Python mit Tk, empfohlen Python 3.14 mit Tk 9. Mit Tk 8.6 startet Glide ebenfalls, nur ohne Systemmitteilungen und SVG-Vorschau. Zusätzliche Pakete sind nicht nötig.

```bash
python3 07_Python-Versionen/Schnellstart.pyw
```

Unter Windows: `python 07_Python-Versionen\Schnellstart.pyw`. Weitere Startwege (aus dem Quellstand, macOS-Entwicklungsbundle) stehen in der [README des Quellbaums](01_Repository/Glide/README.md#schnellstart-aus-dem-quellstand).

**Hinweis für bestehende Daten:** Nach dem Update auf Format 20 Glide 3.29 nicht mehr starten. Es überschreibt einen Bestand im Format 20 bei der ersten Eingabe; zurück geht es dann nur über die Vorsicherung `liste_vor_format20_*.json`.

## Was Glide kann

- **Planen:** Aufgaben mit Unterpunkten, Checklisten, Fälligkeit und Bearbeitungstag, Wiederholungen, Erinnerungen, Wichtigkeit, Labels, Aufwand und Zeiterfassung; „Heute“ und „Demnächst“ mit Stundenraster, Kapazität, Tagesbeginn, Tagesabschluss und Wochenrückblick; Schnelleingabe in Alltagssprache mit Feldchips.
- **Ansichten:** Liste, Tabelle, Kalender, Karten, Spaltenboard und Pinnwand auf demselben Bestand; Gruppieren nach Feld einschließlich Eisenhower; Pinnwand mit Bereichen, Verbindungen und Präsentation; Startseite „Ruhig“ zum Anpassen.
- **Wissen:** Seiten mit Markdown, Bildern und echten Aufgaben, Notizen, Notizbücher, Bücher und Galerien; Suche über Seiten, Punkte und Befehle (Strg/Cmd+O).
- **Pixel-Werkstatt:** Zeichnungen mit 16–128 Zellen, Formen, Symmetrie, Mustern, Paletten, PNG- und ICO-Export, Pixelsymbole.
- **Daten:** atomares Speichern, Sicherungen nur bei Änderung, Vorsicherung je Formatstufe, Tagesstände; Voll-, Teil- und App-Backup, Vorlagen, CSV, Markdown, ICS, Austauschformat für KI; Rückgängig für alles.
- **Gestaltung:** zehn Designs mit Kontrast nach WCAG AA, Hell/Dunkel, Akzentfarben und Hintergrundverläufe; Mindestgröße 860 × 700.

Verhalten im Einzelnen: [Funktionen](01_Repository/Glide/docs/20_FUNKTIONEN.md). Entwicklung je Version: [Änderungsverlauf](01_Repository/Glide/CHANGELOG.md).

## Ablage

| Ordner | Zweck |
|---|---|
| [01_Repository/Glide](01_Repository/Glide/README.md) | Kanonischer Quellcode, Tests, Prüfwerkzeuge und technische Dokumentation |
| [07_Python-Versionen](07_Python-Versionen/README.md) | Startbare, bytegleich gehaltene Python-Fassung; im Archiv die Hauptdateien der sieben neuesten Versionen |
| [05_Probelisten_Testdaten](05_Probelisten_Testdaten/README.md) | Showcase mit eigenem Starter (bytegleiche Lieferkopie der Fixture) |
| [00_Arbeitsvorbereitung](00_Arbeitsvorbereitung/README.md) | Übergabe, Entwicklungsplan, Markt und Vorbilder, manuelle Prüfliste |
| [20_Grafik_Master](20_Grafik_Master/README.md) | Logo, App-Symbol und Fav-Icon als SVG und PNG, Affinity-Quelle, Inspiration, Beispielbilder |
| `.github` | Prüf-Workflow (Glide-Prüfung), Dependabot; CodeQL-Workflow deaktiviert |

## Arbeitsweise mit dem Repository

- **Struktur:** Uploads und Commits immer in diese Struktur, nie in einen Unterordner; sonst brechen die Querverweise. Lokale Arbeitskopie: `Github/glide-to-do`.
- **Prüfung:** Jeder Push und Pull Request auf `main` startet die [Glide-Prüfung](01_Repository/Glide/tests/README.md). Sie umfasst Syntax, Versionen, Dokumentationslinks, Unit-Tests, Analysen, Startprobe, Lieferstand, Herkunft des Fremdcodes, Datenschutz und Ablagegröße. Pull Requests erst mergen, wenn sie grün ist.
- **Schlanke Ablage (03.10.2026):** Archive und Prüfnachweise nur der sieben neuesten Versionen, Fensterbilder nur der drei neuesten, keine Archivkopien – frühere Fassungen hält Git vor. `scripts/pflege/ablage_kuerzen.py` kürzt beim Versionswechsel automatisch.
- **Öffentliches Repository:** Rohprotokolle (`*.log`) bleiben lokal. Veröffentlicht werden Zusammenfassungen ohne Benutzerpfade; vor dem Hochladen neuer Prüfergebnisse `python3 -B scripts/pflege/pfade_bereinigen.py <Ordner>` im Quellbaum ausführen. Was `.gitignore` abfängt und was nicht, steht in ihrem Kopf.
- **Regeln:** [Arbeitsregeln für Claude Code](CLAUDE.md) und [AGENTS.md](01_Repository/Glide/AGENTS.md).
- **Dokumente:** Ein Thema, ein Dokument; zusammenführen und löschen statt archivieren, Erledigtes im Entwicklungsplan markieren ([Dokumentenpflege](01_Repository/Glide/docs/DOKUMENTENPFLEGE.md)).

## Qualität und Sicherheit

- **Glide-Prüfung** (`.github/workflows/python-app.yml`): CI-Grundstufe unter Linux. Die Integrationssuiten unter Linux lassen sich zusätzlich von Hand starten; maßgeblich bleibt die Vollprüfung auf dem Mac.
- **CodeQL:** `.github/workflows/codeql.yml` liegt bereit, ist aber seit 01.10.2026 vom Inhaber deaktiviert. Wieder einschalten unter *Actions → CodeQL → Enable workflow*, nie zusammen mit der CodeQL-Standardeinrichtung.
- **Dependabot:** schlägt wöchentlich Aktualisierungen der verwendeten GitHub Actions vor.
- **Secret Scanning:** aktiv; Schlüssel, Zertifikate und Signing-Secrets gehören nie ins Repository.
- **Schwachstellen melden:** vertraulich über *Security → Report a vulnerability*, nicht über öffentliche Issues ([Sicherheitsrichtlinie](SECURITY.md)). Technische Regeln der Anwendung: [SECURITY.md](01_Repository/Glide/SECURITY.md).

## Weitere Unterlagen

- **Einstieg:** [Übergabe](00_Arbeitsvorbereitung/Glide_Uebergabe.md) · [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) · [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md) · [Dokumentationsindex](01_Repository/Glide/docs/00_INDEX.md)
- **Fachlich:** [Funktionen](01_Repository/Glide/docs/20_FUNKTIONEN.md) · [Architektur](01_Repository/Glide/docs/02_ARCHITECTURE.md) · [Daten und Migration](01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md) · [Vorlagen](01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md) · [Systemmitteilungen](01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md)
- **Prüfung und Veröffentlichung:** [Prüfplan](01_Repository/Glide/docs/05_QA_TESTPLAN.md) · [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md) · [Manuelle Prüfung](00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) · [Veröffentlichung](01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md)

## Lizenz

Das Repository ist öffentlich sichtbar, für Glide ist aber noch keine öffentliche Softwarelizenz festgelegt. Der Quelltext räumt derzeit keine allgemeinen Nutzungs-, Änderungs- oder Weiterverteilungsrechte ein; maßgeblich ist der [Lizenzstatus](01_Repository/Glide/LICENSE.md).
