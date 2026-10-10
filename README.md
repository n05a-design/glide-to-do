# Glide – lokale Aufgaben, Notizen und Pinnwände

[![Glide-Prüfung](https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml)

Glide ist eine deutschsprachige Desktop-Anwendung für Aufgaben, Listen, Seiten, Notizbücher, Pinnwände und Pixelzeichnungen. Sie läuft lokal mit Python und Tk, braucht weder Konto noch Cloud und hält alle Nutzerdaten außerhalb des Programmordners.

Dieses Repository ist die maßgebliche Projektablage (Entscheidung D09): Die Wurzel ist der Projektordner, der Quellcode liegt in [`01_Repository/Glide`](01_Repository/Glide/README.md).

## Stand

- **Entwicklungsstand 3.36.0 vom 09.10.2026**, Datenformat 23; keine veröffentlichte oder signierte Releasefassung.
- **Zuletzt geliefert (Sprint 08./09.10.2026):** Tempo (3.33.19), Komfort im Alltag (3.33.20), ruhige Oberfläche mit hell/dunkel nach System (3.33.21), Wissen und Seiten mit Bildern in Druck und Markdown, markierten Fundstellen und erklärten Filtern (3.34.0) sowie Pixel und Austausch mit geprüften KI-Änderungsvorschlägen und Sicherungsvergleich (3.35.0). Jede Version ist auf dem Referenz-Mac automatisch vollständig geprüft und bytegleich nach `07_Python-Versionen` geliefert; Windows zuletzt 3.33.18. Einzelheiten im [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md).
- **Offen:** Lizenz, Signatur, Markenprüfung, Store, Windows-Prüfung des aktuellen Stands und die manuelle Abnahme unter Windows, Linux, DPI-Skalierung und Bildschirmleser.
- **Nächste Schritte:** [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) mit Status je Aufgabe und den offenen Entscheidungen des Inhabers; Entscheidungen in der [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md).

## Schnellstart

Voraussetzung ist Python mit Tk, empfohlen Python 3.14 mit Tk 9. Mit Tk 8.6 startet Glide ebenfalls, nur ohne Systemmitteilungen und SVG-Vorschau. Zusätzliche Pakete sind nicht nötig.

```bash
python3 07_Python-Versionen/Schnellstart.pyw
```

Unter Windows: `python 07_Python-Versionen\Schnellstart.pyw`. Weitere Startwege (aus dem Quellstand, macOS-Entwicklungsbundle) stehen in der [README des Quellbaums](01_Repository/Glide/README.md#schnellstart-aus-dem-quellstand).

**Hinweis für bestehende Daten:** Nach einem Formatwechsel (zuletzt Format 23) keine ältere Fassung mit dem umgestellten Bestand starten. Seit 3.30 öffnen ältere Fassungen einen neueren Bestand nur schreibgeschützt; Glide 3.29 und älter überschreiben ihn bei der ersten Eingabe. Vor jeder Umstellung entsteht eine Vorsicherung `liste_vor_format<N>_*.json`.

## Was Glide kann

- **Planen:** Aufgaben mit Unterpunkten, Checklisten, Fälligkeit und Bearbeitungstag, Wiederholungen (auch Termin überspringen), Erinnerungen, Wichtigkeit, Labels, Aufwand und Zeiterfassung; „Heute“ und „Demnächst“ mit Tagesvorschlag, Routinen, Fokus, Stundenraster, eingebetteter Wochen-/Monatsplanung, Kapazität, Tagesbeginn, Tagesabschluss und Wochenrückblick; Schnelleingabe in Alltagssprache mit Feldchips.
- **Ansichten:** Liste, Tabelle, Kalender, Karten, Spaltenboard und Pinnwand auf demselben Bestand; Gruppieren nach Feld einschließlich Eisenhower; Pinnwand mit Bereichen, Verbindungen und Präsentation; Startseite „Ruhig“ zum Anpassen.
- **Wissen:** Seiten mit Markdown, Bildern (auch in Druck/PDF und Markdown), Titelbildern, echten Aufgaben und eingebetteten Live-Listen; Notizen, Notizbücher, Bücher und Galerien; lokale Verweise und Rückverweise; gemeinsame Suche und Befehlspalette (Strg/Cmd+O) mit markierten Fundstellen; gespeicherte Filter, die erklären, warum etwas erscheint.
- **Pixel-Werkstatt:** Zeichnungen mit 16–128 Zellen, Formen, Symmetrie, Mustern, Paletten mit Umfärben und Vorschau, PNG- und ICO-Export mit Symbolvorschau, Pixelsymbole.
- **Daten:** atomares Speichern, Sicherungen nur bei Änderung, Vorsicherung je Formatstufe, Tagesstände, Sicherungen vergleichen; Voll-, Teil- und App-Backup, Vorlagen, CSV, Markdown, ICS, Austauschformat für KI mit geprüften Änderungsvorschlägen; Rückgängig für alles.
- **Gestaltung:** zehn Designs mit Kontrast nach WCAG AA, automatisch hell/dunkel nach System, Akzentfarben und Hintergrundverläufe, schmale Seitenleiste; Mindestgröße 860 × 700.

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
