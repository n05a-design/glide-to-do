# Glide – lokale Aufgaben, Notizen und Pinnwände

Stand 25.10.2026 · Glide 3.44.0 · Python-Lieferung 3.44.0 in `07_Python-Versionen`; eigenständige Pakete weiterhin 3.42.0

[![Glide-Prüfung](https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml)

Glide ist eine deutschsprachige Desktop-Anwendung für Aufgaben, Listen, Seiten, Notizbücher, Pinnwände und Pixelzeichnungen. Sie läuft lokal mit Python und Tk, braucht weder Konto noch Cloud und hält alle Nutzerdaten außerhalb des Programmordners.

Dieses Repository ist die maßgebliche Projektablage (Entscheidung D09): Die Wurzel ist der Projektordner, der Quellcode liegt in [`01_Repository/Glide`](01_Repository/Glide/README.md).

## Stand

- **3.44.0 – Phasenabschluss (22.10.2026):** Die seit 3.43.1 entwickelten Pakete sind gemeinsam versioniert, eingefroren geprüft und als Python-Fassung nach `07_Python-Versionen` geliefert ([Phasennachweis](01_Repository/Glide/tests/qa-3.44.0/phasenabschluss_2026-10-22/README.md)). Neu für Nutzer:
  - **Wiederholen nach Rückgängig** (FP-01) über Menü, Palette, Strg/Cmd+Umschalt+Z und unter Windows Strg+Y.
  - **Eigene Rhythmen** (FP-02): mehrere Wochentage, Monats-/Jahresintervalle, n-ter oder letzter Wochentag, Monatsende, Vorschau, Erledigungsbezug, Pause, begrenzte Anzahl, deutsche Chips und Kalender-Rundweg. **Aufgabenformat 26** mit Vorsicherung; die alte 3.43.1 öffnet den umgestellten Bestand nur schreibgeschützt.
  - **Gespeicherte Ansichten** (FP-03): zusätzliche Bedingungen mit Alle/Oder sowie eigene Darstellung als Liste, Tabelle oder Spaltenboard mit Gruppierung, Sortierung und Spaltenbreiten; „Als Ansicht speichern …“.
  - **Seiten und Notizen als Pinnwandkarten** (FP-04), **unverknüpfte Erwähnungen** (FP-05), **fünf lokale KI-Aufträge mit vollständiger Vorschau** (FP-06) und **Alles als Markdown-Ordner exportieren** (FP-07 Stufe 1).
  - **Verlässlicher und schneller:** Bildvorschauen im Hintergrund (WA-26), Schutzrunde gegen Bestandsverlust (WA-27–WA-30), lokaler Schreibbesitz (WA-31), schnellere Mehrfachaktionen (WA-36), ehrliche Speicher-/Folgefehlerergebnisse (WA-37/38/40) und Kalender ohne überholte Auswertung.
- **Weiterhin offen:** Mac-Vollprüfung, Mac-Bundle und eigenständige Pakete 3.44.0 (Pakete bleiben 3.42.0), native Linux-/Mac-Matrix sowie menschliche Bedien-, DPI- und Screenreaderabnahme. [Aktuelle Prüf- und Liefermatrix](01_Repository/Glide/docs/07_QA_BERICHT.md).
- **In Arbeit (lokal, nicht versioniert, nicht geliefert):** Arbeitsmodi und Seitenbedienung (D55) – Kompaktmodus, Nebenansicht im Inspektorbereich, durchsuchbare Seiten- und Blockaktionen mit Blockgriff; gezielt geprüft, GitHub-Prüfung des gepushten Zwischenstands (#148) vollständig grün ([Plan §21.11](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2111-viertes-umsetzungspaket-arbeitsmodi-und-seitenbedienung-d55)).
- **3.43.0 und 3.43.1:** UI-/UX-Paket aus Nutzerbeobachtungen sowie Kürzelkorrektur unter Linux/Tk 9.1; Einzelheiten im [Änderungsverlauf](01_Repository/Glide/CHANGELOG.md).
- **Zuletzt vollständig einschließlich Paketen geliefert:** eigenständige Mac-/Windows-Entwicklungspakete 3.42.0; davor Notion-Import und Seitenwiederherstellung 3.41.0, Pixelanimation 3.40.0, Wiederholungen 3.39.1, Tagesplanung 3.39.0 und Aufgabenoberfläche 3.38.0.
- **Zentrale Roadmap:** Der [aktuelle Entwicklungsplan §21](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#21-roadmap-abgleich-vom-21102026) trennt Umsetzung, Prüf-/Lieferabschlüsse und neue Vorschläge; der Abschluss von 3.44.0 und die nächsten Schritte stehen in [§21.10](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2110-phasenabschluss-3440), die technische Härtung aus dem Sicherheits- und Architekturgutachten vom 25.10.2026 in [§21.12](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2112-technische-folge-aus-dem-sicherheits--und-architekturgutachten). Neue Leistungs-, Schutz-, Design- und Integrationsbelege stehen in Analyse/Markt; die appweiten [Design Richtlinien](01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) führen jede neue oder angefasste Oberfläche. Pflege je Entwicklungsrunde und zusätzlich zweiwöchentlich; keine automatische Feature- oder Releasefreigabe.
- **Offen:** manuelle Bedien-/DPI-/Mehrmonitor-/Screenreaderabnahme sowie die gesonderten Veröffentlichungstore (u. a. Lizenz, öffentliche Signatur und Marke). Status je Aufgabe im [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md), Entscheidungen in der [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md), Gestaltungsregeln in den [Design Richtlinien](01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md).

## Schnellstart

Die gelieferten Entwicklungspakete (noch 3.42.0) starten unter macOS aus `01_Repository/Glide/build/macos/Glide.app` und unter Windows aus `01_Repository/Glide/build/windows/Glide-3.42.0/Glide.exe`, jeweils mit eingebettetem Python/Tcl-Tk. Die Python-Fassung trägt bereits 3.44.0. Bau und Prüfgrenzen: [Paketierung](01_Repository/Glide/packaging/README.md#eigenständige-entwicklungspakete-paket-7).

Für den weiterhin verfügbaren Python-Startweg ist Python mit Tk erforderlich, empfohlen Python 3.14 mit Tk 9. Mit Tk 8.6 startet Glide ebenfalls, nur ohne Systemmitteilungen und SVG-Vorschau. Zusätzliche Pakete sind nicht nötig.

```bash
python3 07_Python-Versionen/Schnellstart.pyw
```

Unter Windows: `python 07_Python-Versionen\Schnellstart.pyw`. Weitere Startwege (aus dem Quellstand, macOS-Entwicklungsbundle) stehen in der [README des Quellbaums](01_Repository/Glide/README.md#schnellstart-aus-dem-quellstand).

**Hinweis für bestehende Daten:** 3.44.0 stellt den Bestand beim ersten Start auf Aufgabenformat 26 um (vorher 25); die eigenständigen Pakete 3.42.0 lesen ihn danach nur schreibgeschützt. Nach einem Formatwechsel keine ältere Fassung mit dem umgestellten Bestand starten. Seit 3.30 öffnen ältere Fassungen einen neueren Bestand nur schreibgeschützt; Glide 3.29 und älter überschreiben ihn bei der ersten Eingabe. Vor jeder Umstellung entsteht eine Vorsicherung `liste_vor_format<N>_*.json`.

## Was Glide kann

- **Planen:** Aufgaben mit Unterpunkten, Checklisten, Fälligkeit und Bearbeitungstag, Wiederholungen mit eigenen Rhythmen (mehrere Wochentage, n-ter Wochentag, Monatsende, ab Erledigung, Pause, Anzahl; auch Termin überspringen), Erinnerungen, Wichtigkeit, Labels, Aufwand und Zeiterfassung; „Heute“ und „Demnächst“ mit Tagesvorschlag, Routinen, Fokus, Stundenraster, eingebetteter Wochen-/Monatsplanung, Kapazität, Tagesbeginn, Tagesabschluss und Wochenrückblick; Schnelleingabe in Alltagssprache mit Feldchips.
- **Ansichten:** Liste, Tabelle, Kalender, Karten, Spaltenboard und Pinnwand auf demselben Bestand; gespeicherte Ansichten mit Alle-/Oder-Bedingungen, eigener Darstellung, Gruppierung, Sortierung und Spalten; Gruppieren nach Feld einschließlich Eisenhower; Pinnwand mit Bereichen, Verbindungen, Seiten-/Notizkarten und Präsentation; Startseite „Ruhig“ zum Anpassen.
- **Wissen:** Seiten mit Markdown, Bildern (auch in Druck/PDF und Markdown), Titelbildern, echten Aufgaben und eingebetteten Live-Listen; Notizen, Notizbücher, Bücher und Galerien; lokale Verweise und Rückverweise sowie unverknüpfte Erwähnungen; gemeinsame Suche und Befehlspalette (Strg/Cmd+O) mit markierten Fundstellen; gespeicherte Filter, die erklären, warum etwas erscheint.
- **Pixel-Werkstatt:** Zeichnungen mit 16–128 Zellen, Formen, Symmetrie, Mustern, Paletten mit Umfärben und Vorschau, PNG- und ICO-Export mit Symbolvorschau, Pixelsymbole.
- **Daten:** atomares Speichern, Sicherungen nur bei Änderung, Vorsicherung je Formatstufe, Tagesstände, Sicherungen vergleichen; Voll-, Teil- und App-Backup, Notion-Import mit Quellenvergleich, einzelne Seiten aus Sicherungen wiederherstellen, Vorlagen, CSV, Markdown (auch der ganze Bestand als Markdown-Ordner), ICS, Austauschformat für KI mit fünf fertigen Aufträgen, vollständiger Vorschau und geprüften Änderungsvorschlägen; Rückgängig und Wiederholen für alles.
- **Gestaltung:** zehn Designs mit Kontrast nach WCAG AA, automatisch hell/dunkel nach System, Akzentfarben und Hintergrundverläufe, schmale Seitenleiste, abschaltbare Bedienhinweise; Mindestgröße 860 × 700. Regeln in den [Design Richtlinien](01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md).

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

- **Glide-Prüfung** (`.github/workflows/python-app.yml`): verpflichtende Grundstufe sowie vollständige Linux-/Windows-Prüfmatrix. Jede Lieferung erhält zusätzlich ihre eingefrorene Mac-Vollprüfung. Gezielte Diagnoseläufe ersetzen keine Vollmatrix; menschliche Bedien- und Readerabnahmen bleiben getrennt.
- **CodeQL:** `.github/workflows/codeql.yml` liegt bereit, ist aber seit 01.10.2026 vom Inhaber deaktiviert. Wieder einschalten unter *Actions → CodeQL → Enable workflow*, nie zusammen mit der CodeQL-Standardeinrichtung. Solange er aus ist, läuft nur die Standardeinrichtung; sie liest keine `.pyw`-Dateien und damit voraussichtlich nicht die Hauptdatei ([Entwicklungsplan I12](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#11-nur-durch-den-inhaber)).
- **Dependabot:** schlägt wöchentlich Aktualisierungen der verwendeten GitHub Actions vor; diese sind noch über Versionstags statt Commit-SHA eingebunden (WA-43).
- **Secret Scanning:** aktiv; Schlüssel, Zertifikate und Signing-Secrets gehören nie ins Repository.
- **Schwachstellen melden:** vertraulich über *Security → Report a vulnerability*, nicht über öffentliche Issues ([Sicherheitsrichtlinie](SECURITY.md)). Technische Regeln der Anwendung: [SECURITY.md](01_Repository/Glide/SECURITY.md).

## Weitere Unterlagen

- **Einstieg:** [Übergabe](00_Arbeitsvorbereitung/Glide_Uebergabe.md) · [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) · [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md) · [Dokumentationsindex](01_Repository/Glide/docs/00_INDEX.md)
- **Fachlich:** [Funktionen](01_Repository/Glide/docs/20_FUNKTIONEN.md) · [Architektur](01_Repository/Glide/docs/02_ARCHITECTURE.md) · [Daten und Migration](01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md) · [Vorlagen](01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md) · [Systemmitteilungen](01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md)
- **Prüfung und Veröffentlichung:** [Prüfplan](01_Repository/Glide/docs/05_QA_TESTPLAN.md) · [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md) · [Manuelle Prüfung](00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) · [Veröffentlichung](01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md)

## Lizenz

Das Repository ist öffentlich sichtbar, für Glide ist aber noch keine öffentliche Softwarelizenz festgelegt. Der Quelltext räumt derzeit keine allgemeinen Nutzungs-, Änderungs- oder Weiterverteilungsrechte ein; maßgeblich ist der [Lizenzstatus](01_Repository/Glide/LICENSE.md).
