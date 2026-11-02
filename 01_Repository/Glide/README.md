# Glide – lokale Aufgaben, Notizen und Pinnwände

Stand 02.11.2026 · Glide 3.50.0 · Erster öffentlicher Stand (intern: öffentliche erste Beta) · Aufgabenformat 26

**3.50-Fertigstellung, 02.11.2026:** Erster öffentlicher Stand (intern öffentliche erste Beta). Neue UI-Funktionen, Python-Abgleich und tatsächliche Paket-/Prüfergebnisse im [aktuellen Nachweis](tests/qa-3.50.0/oeffentliche_beta_2026-11-02/README.md). Frühere datierte Absätze beschreiben ihren damaligen Stand. Screenreader-Abnahme ist bis Bedarf zurückgestellt; menschliche Prüfung folgt anschließend.


**Abschlussfortsetzung 31.10.2026:** Python/Showcase und eigenständiges macOS-arm64-Paket 3.49.0 geliefert, Windows-Paket weiterhin 3.45.0. Native Tk-9.1-Matrix: 126 Schritte einschließlich aller 108 Integrationssuiten grün; Programm-, Test-, Fixture- und Ressourcenstand entsprechen dem eingefrorenen Nachweis; anschließende Anleitungspflege separat geprüft. Neue Grundstufe mit 235 Werkzeugtests und zweimal 1.082 Fachtests grün. 56 Mutationsfälle und zwölf native Accessibility-Proben grün. WA-41A/B, Windows-/Linux-Endmatrix, echte Readerketten, übrige appweite Architektur-/Performanceumfänge und Menschenabnahme bleiben offen. [Prüf- und Liefernachweis](tests/qa-3.49.0/gesamtabschluss_2026-10-31/README.md), [aktueller Rest in §21.37](../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2137-abschlussfortsetzung-mutationen-prüfablauf-tk-91-und-lieferung). Frühere datierte Absätze bewahren ihren damaligen Stand.

Glide ist eine deutschsprachige Desktop-Anwendung für Aufgaben, Listen, Notizen, Seiten, Notizbücher, Pinnwände, Galerien und Pixelzeichnungen. Sie läuft lokal mit Python 3.14 und Tk 9 (Tk 8.6 eingeschränkt), braucht weder Konto noch Cloudservice und hält Nutzerdaten außerhalb des Programmordners.

> **Projektstatus:** Glide **3.50.0**, Aufgabenformat 26, Erster öffentlicher Stand (öffentliche erste Beta). Hintergrundfarben, volle Seitenleiste und Blockziehen ergänzen die bisherigen Funktionen. Tatsächliche Lieferungen, Tests und verbleibende technische Grenzen stehen im aktuellen QA-Nachweis. Screenreader ist bis Bedarf zurückgestellt; menschliche Prüfung folgt nach der technischen Fertigstellung.

Funktionsumfang im Überblick: [Projekt-README](../../README.md#was-glide-kann); Verhalten im Einzelnen: [Funktionen](docs/20_FUNKTIONEN.md); Entwicklung je Version: [Änderungsverlauf](CHANGELOG.md).

## Schnellstart aus dem Quellstand

Voraussetzung ist Python mit Tk; zusätzliche Laufzeitpakete sind nicht nötig.

```bash
python3 src/glide/app.pyw          # Windows: python src\glide\app.pyw
```

Eigenständige 3.50-Pakete: Windows unter `build/windows/Glide-3.50.0/Glide.exe`, macOS unter `build/macos/Glide.app` bzw. im Archiv `Glide-3.50.0-macos-arm64.tar.gz`. Das TAR nativ entpacken, damit POSIX-Links und Dateimodi erhalten bleiben. Tatsächliche Bereitstellung und SHA-256 im [aktuellen QA-Nachweis](docs/07_QA_BERICHT.md). Die [Paketierung](packaging/README.md#eigenständige-entwicklungspakete-paket-7) beschreibt den reproduzierbaren Bau.

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
python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.50.0/lokaler_lauf --timeout 900
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
