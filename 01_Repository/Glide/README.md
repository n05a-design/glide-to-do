# Glide – lokale Aufgaben, Notizen und Pinnwände

Stand 29.10.2026 · Glide 3.49.0 · Aufgabenformat 26 · Quelle 3.49.0 (Prüfkandidat); Python-Lieferung 3.47.0; eigenständige Pakete 3.45.0

**Fortsetzung 29.10.2026:** Mutationsreste einschließlich „Liste leeren“ gezielt geschlossen (40 Appfälle grün); PC-01 AMD, PC-02 Intel und MacBook M2 mit getrennten Quell-/Prüfständen vergleichen. Erster M2-Lauf ausgewertet, drei gemeinsame Fehlerursachen korrigiert, WA-41A nur auf PC-02 ([Gerätevergleich](tests/qa-3.49.0/geraetevergleich_2026-10-29/README.md)); native Mac-Abnahme offen. Letzte breite Intel-CI rot; Gesamtauftrag und Liefer-/Abnahmetore bleiben offen. [Aktueller Nachweis](tests/qa-3.49.0/abschlussreste_2026-10-29/README.md).

**Abnahme und Dokumentstand 29.10.2026:** [Abnahmebericht](tests/qa-3.49.0/abnahme_2026-10-28/README.md) lokal eingearbeitet; [Datei-/Dokumentabgleich](tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md). A01-Pflichtfolge nach begründeten Adapter-/Prüfplatzkorrekturen in 13 Bereichssuiten/136 Fällen grün; danach WA-09-Unterfelder und fremde Karten lokal umgesetzt, fünf Appfälle und 21 Regressionen grün. [Fortsetzung und aktueller Prüfstand](tests/qa-3.49.0/abschlussreste_2026-10-29/README.md). Nicht alle begonnenen Arbeiten abgeschlossen. Technische Restumfänge, WA-41 und aktuelle Lieferung/native/Menschenabnahme bleiben offen.

**Aktuell funktional erweitert (3.49.0-Kandidat):** Wochenwahl in der Tageskachel, gemeinsame Fälligkeit/Aufwand und Kopieren/Hauptöffnen/Verknüpfen von Verweisen in der Nebenansicht. [Tatsächlicher Umfang und Prüfstand](tests/qa-3.49.0/funktionspakete_2026-10-28/README.md). Lieferung weiterhin Python 3.47.0/native 3.45.0; WA-41 und vollständige Endabnahme offen.

Glide ist eine deutschsprachige Desktop-Anwendung für Aufgaben, Listen, Notizen, Seiten, Notizbücher, Pinnwände, Galerien und Pixelzeichnungen. Sie läuft lokal mit Python 3.14 und Tk 9 (Tk 8.6 eingeschränkt), braucht weder Konto noch Cloudservice und hält Nutzerdaten außerhalb des Programmordners.

> **Projektstatus:** lokaler Prüfkandidat **3.49.0**, Aufgabenformat 26: gemeinsame abgesicherte Prüfabläufe, geschützter Wiederanlauf und lokale Absturzdiagnose. Die 3.48.0-Tages-/Nebenansichtsfeatures bleiben enthalten. Python/Showcase 3.47.0, eigenständige Pakete 3.45.0; WA-41 und breite/native Abnahme offen. [Prüfung und Liefergrenzen](tests/qa-3.49.0/robustheit_2026-10-28/README.md).

Funktionsumfang im Überblick: [Projekt-README](../../README.md#was-glide-kann); Verhalten im Einzelnen: [Funktionen](docs/20_FUNKTIONEN.md); Entwicklung je Version: [Änderungsverlauf](CHANGELOG.md).

## Schnellstart aus dem Quellstand

Voraussetzung ist Python mit Tk; zusätzliche Laufzeitpakete sind nicht nötig.

```bash
python3 src/glide/app.pyw          # Windows: python src\glide\app.pyw
```

Gelieferte eigenständige Entwicklungspakete 3.45.0: `build/windows/Glide-3.45.0/Glide.exe` und `build/macos/Glide-3.45.0-macos-arm64.tar.gz`. Das Mac-TAR nativ entpacken und die enthaltene `Glide.app` starten. `build/macos/Glide.app` ist auf diesem Windows-Rechner eine geprüfte Inspektionskopie mit NT-Linkzielen. Python/Tcl-Tk sind eingebettet; [Paketierung und Grenzen](packaging/README.md#eigenständige-entwicklungspakete-paket-7).

Die Ressourcen unter `src/glide/resources` müssen neben der Anwendung liegen. Startbare Lieferfassung: `07_Python-Versionen/Schnellstart.pyw`. Unter macOS lässt sich ein Entwicklungsbundle bauen (nutzt das installierte Python, nicht zur Weitergabe):

```bash
python3 packaging/macos/baue_app.py --ziel build/macos-vorstufe
```

Die isolierte Bedienprobe der Zeichenfläche (2026-09-24) startet mit `python3 src/glide/drawing_prototype.pyw`.

## Daten und Datenschutz

Glide arbeitet ohne eigenen Netzwerkzugriff. Nutzerdaten und Anhänge liegen im lokalen Datenordner des Betriebssystems oder einer bewusst gewählten Ablage. Vor Tests muss `GLIDE_DATA_DIR` auf ein temporäres Verzeichnis zeigen. Details: [Daten und Migration](docs/06_DATA_BACKUP_MIGRATION.md), [Sicherheitshinweise](SECURITY.md).

Das Repository ist öffentlich: Rohprotokolle (`*.log`) bleiben lokal, veröffentlichte Prüfergebnisse enthalten keine Benutzerpfade (`python3 -B scripts/pflege/pfade_bereinigen.py tests/qa-<Version>/<Lauf>`, CI-Schritt „Datenschutz“). Sicherheitsfunde vertraulich über *Security → Report a vulnerability* ([Sicherheitsrichtlinie](../../SECURITY.md)).

## Entwicklung und Prüfung

Vollprüfung auf dem Referenz-Mac (aus `01_Repository/Glide`):

```bash
python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.49.0/lokaler_lauf --timeout 900
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
| `packaging/` | eigenständige Mac-/Windows-Pakete, Entwicklungsbundle, Windows-Verknüpfung, Programmsymbole ([Übersicht](packaging/README.md)) |
| `assets/icons/` | erzeugte Paketsymbole ([Herkunft](assets/README.md)) |
| `requirements/` | Laufzeit-, Entwicklungs- und Build-Abhängigkeiten |

## Mitwirken und Lizenz

Vor Änderungen gelten die [Arbeitsregeln](AGENTS.md); Entscheidungen und Arbeitsablauf stehen in der [Arbeitsrichtung](docs/ARBEITSRICHTUNG.md). Änderungen müssen zum Datenmodell passen, Nutzerdaten schützen und mit den betroffenen Tests und der Dokumentation abgeschlossen werden.

Für Glide ist noch keine öffentliche Softwarelizenz festgelegt; der Quelltext räumt derzeit keine Nutzungs-, Änderungs- oder Weiterverteilungsrechte ein ([Lizenzstatus](LICENSE.md)).
