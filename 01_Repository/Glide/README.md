# Glide – Desktop-Planer

Stand 12.11.2026 · Quellstand 3.55.1 · Aufgabenformat 26

Glide ist ein Desktop-Planer für Projekte, Aufgaben, Tagesplanung, Pinnwände und Pixel-Zeichnungen. Seiten, Notizen und Galerien ergänzen die Arbeit. Technische Grundlage ist Python 3.14 mit Tk 9 (Tk 8.6 eingeschränkt); Nutzerdaten liegen außerhalb des Programmordners.

> **Projektstatus:** Lokaler Prüfstand Glide 3.55.1, Aufgabenformat 26, Einstellungen 2 und Vorlagen 2. Der [QA-Bericht](docs/07_QA_BERICHT.md#plattformprüfung-und-pakete-auf-main-12112026) nennt die geprüften Commits, Paketbauten und offenen Abnahmen. Die [Übergabe](../../00_Arbeitsvorbereitung/Glide_Uebergabe.md) bündelt den aktuellen Arbeitsstand.

**Verbindliche technische Gesamtliste:** [Glide-System](src/glide/README.md), eigenständig versioniert in [`GLIDE_SYSTEM_VERSION`](GLIDE_SYSTEM_VERSION) (Start **V1.0**) – Module, Features, Wiederverwendung, Bausteine, Tests und System-und-Modulpflege. Diese Katalogversion ist unabhängig von Glides Anwendungs- und Datenformatversion.

Für Folgeprojekte wie Steps nennt der [Übernahmevertrag](src/glide/README.md#9-grundlage-für-steps-und-weitere-projekte) die vorhandenen Grundlagen, Abhängigkeiten, Produktkopplungen, Prüfgrenzen und die erste Übergabefolge. Technische Systemfähigkeiten sind direkt in der dortigen Featureübersicht enthalten. Ein unabhängiges Framework ist daraus noch nicht abgenommen.

Funktionsumfang im Überblick: [Projekt-README](../../README.md#was-glide-kann); Verhalten im Einzelnen: [Funktionen](docs/20_FUNKTIONEN.md); Entwicklung je Version: [Änderungsverlauf](CHANGELOG.md).

## Schnellstart aus dem Quellstand

Voraussetzung ist Python mit Tk; zusätzliche Laufzeitpakete sind nicht nötig.

```bash
python3 src/glide/app.pyw          # Windows: python src\glide\app.pyw
```

Eigenständige Paketstände, Quellhashes und Verfügbarkeit werden im [aktuellen QA-/Liefernachweis](docs/07_QA_BERICHT.md) getrennt geführt. Native Entwicklungsbauten sind ihrem jeweiligen Quellcommit zugeordnet; ein bestätigtes eigenständiges Linux-Paket fehlt. Ein frischer Clone enthält keine ignorierten lokalen Bauartefakte. Öffentliche Release-Downloads sind noch nicht freigegeben.

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
python3 -B tests/tools/pruefen.py --zugang-nativ --modus voll --protokoll build/lokale-qa --timeout 900
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

Der [Contributing-Einstieg](../../CONTRIBUTING.md) führt durch die Mitarbeit. Vor Änderungen gelten die [Arbeitsregeln](AGENTS.md); Entscheidungen und Arbeitsablauf stehen in der [Arbeitsrichtung](docs/ARBEITSRICHTUNG.md). Die [Pflegematrix](docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) bestimmt die betroffenen Fachquellen. [Architektur](docs/02_ARCHITECTURE.md), [Systembestand](src/glide/README.md) und [Shell-Zielbild](docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md) werden entsprechend ihrer Zuständigkeit abgeglichen.

Der Projektcode steht unter **MPL-2.0**, einschließlich kommerzieller Nutzung nach den Lizenzbedingungen. [Vollständiger Lizenztext](../../LICENSE) und [Hinweise zu Drittkomponenten und Weitergabe](LICENSE.md).

Logo-Master, Betriebssystem-/Vorschau-/Paketsymbole und künftige Aktualisierungsschritte: [zentrale Logo-Übersicht](../../20_Grafik_Master/README.md).
