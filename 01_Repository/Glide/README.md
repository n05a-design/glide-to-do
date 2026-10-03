# Glide – lokale Aufgaben, Notizen und Pinnwände

Glide ist eine deutschsprachige Desktop-Anwendung für Aufgaben, Listen, Notizen, Seiten, Notizbücher, Pinnwände, Galerien und Pixelzeichnungen. Sie läuft lokal mit Python 3.14 und Tk 9 (Tk 8.6 eingeschränkt), braucht weder Konto noch Cloudservice und hält Nutzerdaten außerhalb des Programmordners.

> **Projektstatus:** interner Entwicklungsstand **3.33.6** · Datenformat 20 · keine veröffentlichte oder signierte Releasefassung. Der [QA-Bericht](docs/07_QA_BERICHT.md) nennt bestandene Prüfungen und offene Plattformtests.

Funktionsumfang im Überblick: [Projekt-README](../../README.md#was-glide-kann); Verhalten im Einzelnen: [Funktionen](docs/20_FUNKTIONEN.md); Entwicklung je Version: [Änderungsverlauf](CHANGELOG.md).

## Schnellstart aus dem Quellstand

Voraussetzung ist Python mit Tk; zusätzliche Laufzeitpakete sind nicht nötig.

```bash
python3 src/glide/app.pyw          # Windows: python src\glide\app.pyw
```

Die Ressourcen unter `src/glide/resources` müssen neben der Anwendung liegen. Startbare Lieferfassung: `07_Python-Versionen/Schnellstart.pyw`. Unter macOS lässt sich ein Entwicklungsbundle bauen (nutzt das installierte Python, nicht zur Weitergabe):

```bash
python3 packaging/macos/baue_app.py --ziel build/macos
```

Die isolierte Bedienprobe der Zeichenfläche (2026-09-24) startet mit `python3 src/glide/drawing_prototype.pyw`.

## Daten und Datenschutz

Glide arbeitet ohne eigenen Netzwerkzugriff. Nutzerdaten und Anhänge liegen im lokalen Datenordner des Betriebssystems oder einer bewusst gewählten Ablage. Vor Tests muss `GLIDE_DATA_DIR` auf ein temporäres Verzeichnis zeigen. Details: [Daten und Migration](docs/06_DATA_BACKUP_MIGRATION.md), [Sicherheitshinweise](SECURITY.md).

Das Repository ist öffentlich: Rohprotokolle (`*.log`) bleiben lokal, veröffentlichte Prüfergebnisse enthalten keine Benutzerpfade (`python3 -B scripts/pflege/pfade_bereinigen.py tests/qa-<Version>/<Lauf>`, CI-Schritt „Datenschutz“). Sicherheitsfunde vertraulich über *Security → Report a vulnerability* ([Sicherheitsrichtlinie](../../SECURITY.md)).

## Entwicklung und Prüfung

Vollprüfung auf dem Referenz-Mac (aus `01_Repository/Glide`):

```bash
python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.33.6/lokaler_lauf --timeout 900
```

CI-Grundstufe, wie GitHub sie bei jedem Push und Pull Request auf `main` ausführt (Syntax, Versionen, Dokumentation, Unit- und Werkzeugtests, fünf Analysen, Startprobe, Lieferstand, Fremdcode, Datenschutz, Ablagegröße):

```bash
python3 -B tests/tools/ci_grundstufe.py
```

Sie ersetzt nicht die Vollprüfung auf dem Mac. Ein nicht vollständig grüner Lauf ist keine Releasefreigabe. Einzelheiten: [Prüfplan](docs/05_QA_TESTPLAN.md).

## Struktur

| Pfad | Inhalt |
|---|---|
| `src/glide/` | Anwendung, Tk-freie Fachmodule, Ressourcen, `vendor/tkinterdnd2` ([Modulübersicht](src/glide/README.md)) |
| `tests/` | Integrationssuiten, Unit-Tests, Fixtures, Prüfwerkzeuge und Nachweise der sieben neuesten Versionen ([Übersicht](tests/README.md)) |
| `docs/` | Produkt, Architektur, Funktionen, Daten, Prüfung, Veröffentlichung, Entscheidungen ([Index](docs/00_INDEX.md)) |
| `scripts/pflege/` | Versionswechsel, Abgleich nach 07, Kürzen der Ablage, Messungen ([Übersicht](scripts/pflege/README.md)) |
| `packaging/` | macOS-Entwicklungsbundle, Windows-Verknüpfung, Programmsymbole ([Übersicht](packaging/README.md)) |
| `assets/icons/` | erzeugte Paketsymbole ([Herkunft](assets/README.md)) |
| `requirements/` | Laufzeit-, Entwicklungs- und Build-Abhängigkeiten |

## Mitwirken und Lizenz

Vor Änderungen gelten die [Arbeitsregeln](AGENTS.md) mit dem Arbeitsablauf; Leitbild, Prinzipien und Entscheidungen stehen in der [Richtung](../../00_Arbeitsvorbereitung/Glide_Richtung.md). Änderungen müssen zum Datenmodell passen, Nutzerdaten schützen und mit den betroffenen Tests und der Dokumentation abgeschlossen werden.

Für Glide ist noch keine öffentliche Softwarelizenz festgelegt; der Quelltext räumt derzeit keine Nutzungs-, Änderungs- oder Weiterverteilungsrechte ein ([Lizenzstatus](LICENSE.md)).
