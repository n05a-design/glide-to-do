# Glide – lokale Aufgaben, Notizen und Pinnwände

[![Glide-Prüfung](https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml)

Glide ist eine deutschsprachige Desktop-Anwendung für Aufgaben, Listen, Seiten, Notizbücher, Pinnwände und Pixelzeichnungen. Sie läuft lokal mit Python und Tk, braucht weder Konto noch Cloud und hält alle Nutzerdaten außerhalb des Programmordners.

Dieses Repository ist die maßgebliche Projektablage (Entscheidung D09): Die Wurzel ist der Projektordner, der Quellcode liegt in [`01_Repository/Glide`](01_Repository/Glide/README.md).

## Stand

- **Entwicklungsstand 3.43.1 vom 16.10.2026**, Datenformat 25. Dies ist eine Entwicklungsfassung.
- **3.43.1 – Kürzel in Listen unter Linux/Tk 9.1:** Strg+Umschalt+P (Einplanen) und die übrigen Strg+Buchstaben-Kürzel verschieben unter Linux mit Tk 9.1 nicht mehr die Auswahl in Listen. Dazu erzeugen zwei Prüfungen die Tk-9.1-Ereignisse wie unter X11; damit sind die drei roten Linux-Suiten der GitHub-Vollmatrix behoben. Seit PR #32 ist die ganze GitHub-Prüfung grün: Linux und Windows mit eigener Tk 9.1 sowie das eigenständige Windows-Paket. Windows und macOS unverändert.
- **3.43.0 – UI-/UX-Paket aus Nutzerbeobachtungen:** ruhigere Kopfzeile mit Lupe und Hinweisschalter, Galeriebilder auf der Startseite, fester Begleiter Gismo, Titel mit mehr Platz, geschützte Bedienelemente, gleichmäßiges Scrollen über Bildern und dauerhaft nachlesbare Neuerungen. Automatisch geprüft (Pflichtsuite mit roter Gegenprobe gegen 3.42.0, appweite Knopfschutzprüfung, eingefrorene Windows-Vollprüfung) und in die Python-Fassung übernommen; in `main` seit PR #27. Die GitHub-Vollmatrix mit eigener Tk 9.1 war seit der Vorbereitung von Paket 8 (PR #26) rot und ist mit 3.43.1 wieder vollständig grün; Mac-Vollprüfung, Mac-Bundle und eigenständige Pakete 3.43.0 stehen noch aus. Einzelheiten im [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md).
- **Zuletzt vollständig einschließlich Paketen geliefert:** eigenständige Mac-/Windows-Entwicklungspakete 3.42.0; davor Notion-Import und Seitenwiederherstellung 3.41.0, Pixelanimation 3.40.0, Wiederholungen 3.39.1, Tagesplanung 3.39.0 und Aufgabenoberfläche 3.38.0.
- **Nächste Schritte:** Auswahl zu Kompaktmodus, zwei Inhalten gleichzeitig und Notion-Mustern (Entscheidungsvorlagen E-U1–E-U3), danach der pausierte zugängliche Aufgaben-Kernablauf 4.0.0 mit eigener Tk-9.1-Laufzeit.
- **Offen:** manuelle Bedien-/DPI-/Mehrmonitor-/Screenreaderabnahme sowie die gesonderten Veröffentlichungstore (u. a. Lizenz, öffentliche Signatur und Marke). Status je Aufgabe im [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md), Entscheidungen in der [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md), Gestaltungsregeln in den [Design Richtlinien](01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md).

## Schnellstart

Die gelieferten Entwicklungspakete (noch 3.42.0) starten unter macOS aus `01_Repository/Glide/build/macos/Glide.app` und unter Windows aus `01_Repository/Glide/build/windows/Glide-3.42.0/Glide.exe`, jeweils mit eingebettetem Python/Tcl-Tk. Die Python-Fassung trägt bereits 3.43.1. Bau und Prüfgrenzen: [Paketierung](01_Repository/Glide/packaging/README.md#eigenständige-entwicklungspakete-paket-7).

Für den weiterhin verfügbaren Python-Startweg ist Python mit Tk erforderlich, empfohlen Python 3.14 mit Tk 9. Mit Tk 8.6 startet Glide ebenfalls, nur ohne Systemmitteilungen und SVG-Vorschau. Zusätzliche Pakete sind nicht nötig.

```bash
python3 07_Python-Versionen/Schnellstart.pyw
```

Unter Windows: `python 07_Python-Versionen\Schnellstart.pyw`. Weitere Startwege (aus dem Quellstand, macOS-Entwicklungsbundle) stehen in der [README des Quellbaums](01_Repository/Glide/README.md#schnellstart-aus-dem-quellstand).

**Hinweis für bestehende Daten:** Nach einem Formatwechsel (zuletzt Format 25) keine ältere Fassung mit dem umgestellten Bestand starten. Seit 3.30 öffnen ältere Fassungen einen neueren Bestand nur schreibgeschützt; Glide 3.29 und älter überschreiben ihn bei der ersten Eingabe. Vor jeder Umstellung entsteht eine Vorsicherung `liste_vor_format<N>_*.json`.

## Was Glide kann

- **Planen:** Aufgaben mit Unterpunkten, Checklisten, Fälligkeit und Bearbeitungstag, Wiederholungen (auch Termin überspringen), Erinnerungen, Wichtigkeit, Labels, Aufwand und Zeiterfassung; „Heute“ und „Demnächst“ mit Tagesvorschlag, Routinen, Fokus, Stundenraster, eingebetteter Wochen-/Monatsplanung, Kapazität, Tagesbeginn, Tagesabschluss und Wochenrückblick; Schnelleingabe in Alltagssprache mit Feldchips.
- **Ansichten:** Liste, Tabelle, Kalender, Karten, Spaltenboard und Pinnwand auf demselben Bestand; Gruppieren nach Feld einschließlich Eisenhower; Pinnwand mit Bereichen, Verbindungen und Präsentation; Startseite „Ruhig“ zum Anpassen.
- **Wissen:** Seiten mit Markdown, Bildern (auch in Druck/PDF und Markdown), Titelbildern, echten Aufgaben und eingebetteten Live-Listen; Notizen, Notizbücher, Bücher und Galerien; lokale Verweise und Rückverweise; gemeinsame Suche und Befehlspalette (Strg/Cmd+O) mit markierten Fundstellen; gespeicherte Filter, die erklären, warum etwas erscheint.
- **Pixel-Werkstatt:** Zeichnungen mit 16–128 Zellen, Formen, Symmetrie, Mustern, Paletten mit Umfärben und Vorschau, PNG- und ICO-Export mit Symbolvorschau, Pixelsymbole.
- **Daten:** atomares Speichern, Sicherungen nur bei Änderung, Vorsicherung je Formatstufe, Tagesstände, Sicherungen vergleichen; Voll-, Teil- und App-Backup, Notion-Import mit Quellenvergleich, einzelne Seiten aus Sicherungen wiederherstellen, Vorlagen, CSV, Markdown, ICS, Austauschformat für KI mit geprüften Änderungsvorschlägen; Rückgängig für alles.
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
