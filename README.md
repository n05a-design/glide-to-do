# Glide – lokale Aufgaben, Notizen und Pinnwände

[![Glide-Prüfung](https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml)
[![CodeQL](https://github.com/n05a-design/glide-to-do/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/n05a-design/glide-to-do/actions/workflows/codeql.yml)

Glide ist eine deutschsprachige Desktop-Anwendung für Aufgaben, Listen, Seiten, Notizbücher, Pinnwände und Pixelzeichnungen. Sie läuft lokal mit Python und Tk, braucht weder Konto noch Cloud und hält alle Nutzerdaten außerhalb des Programmordners.

Dieses Repository ist die maßgebliche Projektablage (Entscheidung D09): Die Wurzel ist der Projektordner, der Quellcode liegt in [`01_Repository/Glide`](01_Repository/Glide/README.md).

## Stand

- **Entwicklungsstand 3.33.1 vom 01.10.2026**, Datenformat 20.
- **Prüfkandidat, keine Releasefassung:** Die Vollprüfung auf dem Referenz-Mac endete mit 4 nicht bestandenen Schritten ([Ergebnis](01_Repository/Glide/tests/qa-3.33.1/bereiche_fenster_2026-10-01/vollpruefung/ergebnis.json)). Zuletzt vollständig geprüft und ausgeliefert wurde 3.33.0 ([QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md)).
- **Offen:** Signatur, Markenprüfung, Store und die manuelle Abnahme unter Windows, Linux, DPI-Skalierung und Bildschirmleser.
- **Nächste Schritte:** [Entwicklungsplan ab 3.33](00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md) mit den [beschlossenen Entscheidungen D09–D17](00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md).

## Schnellstart

Voraussetzung ist Python mit Tk, empfohlen Python 3.14 mit Tk 9. Mit Tk 8.6 startet Glide ebenfalls, nur ohne Systemmitteilungen und SVG-Vorschau. Zusätzliche Pakete sind nicht nötig.

```bash
python3 07_Python-Versionen/Schnellstart.pyw
```

Unter Windows: `python 07_Python-Versionen\Schnellstart.pyw`. Weitere Startwege (aus dem Quellstand, macOS-Entwicklungsbundle) stehen in der [README des Quellbaums](01_Repository/Glide/README.md#schnellstart-aus-dem-quellstand).

**Hinweis für bestehende Daten:** Nach dem Update auf Format 20 Glide 3.29 nicht mehr starten. Es überschreibt einen Bestand im Format 20 bei der ersten Eingabe; zurück geht es dann nur über die Vorsicherung `liste_vor_format20_*.json`.

## Was Glide kann

- **Planen:** Aufgaben mit Unterpunkten, Fälligkeit, Bearbeitungstag, Wiederholung, Erinnerung, Wichtigkeit, Labels und Aufwand; „Mein Tag“ mit Stundenraster, Tagesbeginn und Wochenrückblick.
- **Ansichten:** Liste, Tabelle, Kalender, Karten, Spaltenboard und Pinnwand auf demselben Bestand; Startseite zum direkten Anpassen.
- **Wissen:** Seiten mit Markdown und Bildern, Notizbücher, Bibliotheken und Galerien; Suche über Seiten, Punkte und Befehle (Strg/Cmd+O).
- **Pixel-Werkstatt:** Zeichnungen von 16 bis 128 Zellen mit Werkzeugen, Symmetrie, Paletten, PNG-Export und Pixelsymbolen.
- **Austausch und Sicherheit der Daten:** Vorlagen, CSV, Markdown, ICS und Glide-Formate; atomares Speichern, Vorsicherungen je Formatstufe, Tagesstände und Rückgängig für alles.
- **Gestaltung:** zehn Designs mit lesbarem Kontrast nach WCAG AA, Hell/Dunkel, Akzentfarben und Hintergrundverläufe.

Vollständige Übersicht: [Was Glide bereits kann](01_Repository/Glide/README.md#was-glide-bereits-kann). Entwicklung je Version: [Änderungsverlauf](01_Repository/Glide/CHANGELOG.md).

## Ablage

| Ordner | Zweck |
|---|---|
| [01_Repository/Glide](01_Repository/Glide/README.md) | Kanonischer Quellcode, Tests, Prüfwerkzeuge und technische Dokumentation |
| [07_Python-Versionen](07_Python-Versionen/README.md) | Startbare, bytegleich gehaltene Python-Fassung mit Ressourcen |
| [05_Probelisten_Testdaten](05_Probelisten_Testdaten/README.md) | 16 Praxisvorlagen, Beispielsicherungen, „Rundgang“ und Showcase |
| [00_Arbeitsvorbereitung](00_Arbeitsvorbereitung/README.md) | Planung, Entscheidungen, Übergaben, manuelle Prüflisten |
| [20_Grafik_Master](20_Grafik_Master/README.md) | Logo, App-Symbol und Fav-Icon als SVG und PNG, Stilvorlagen |
| [40_Store_Material](40_Store_Material/README.md) | Entwürfe für die Veröffentlichung |
| [50_Ablage](50_Ablage/README.md) | Historische Prüfungen, Screenshots und Rückfallstände |
| `.github` | Prüf- und Sicherheits-Workflows (Glide-Prüfung, CodeQL), Dependabot |

## Arbeitsweise mit dem Repository

- **Struktur:** Uploads und Commits immer in diese Struktur, nie in einen Unterordner; sonst brechen die Querverweise. Lokale Arbeitskopie: `Github/glide-to-do`.
- **Prüfung:** Jeder Push und Pull Request auf `main` startet die [Glide-Prüfung](01_Repository/Glide/tests/README.md). Sie umfasst Syntax, Versionen, Dokumentationslinks, Unit-Tests, Analysen, Startprobe, Lieferstand, Herkunft des Fremdcodes und Datenschutz. Pull Requests erst mergen, wenn sie grün ist.
- **Öffentliches Repository:** Rohprotokolle (`*.log`) bleiben lokal. Veröffentlicht werden Zusammenfassungen ohne Benutzerpfade; vor dem Hochladen neuer Prüfergebnisse `python3 -B scripts/pflege/pfade_bereinigen.py <Ordner>` im Quellbaum ausführen.
- **Regeln:** [Arbeitsregeln für Claude Code](CLAUDE.md) und [AGENTS.md](01_Repository/Glide/AGENTS.md).
- **Dokumentationspflege:** Seit dem Auftrag vom 01.10.2026 werden doppelte und überholte Dokumente nach Wissensabgleich gelöscht; aktuelle Quellen werden fortgeschrieben, Git trägt die Historie ([Wissenseinstieg und Bereinigungsnachweis](01_Repository/Glide/docs/75_DOKUMENTATIONSREDUKTION_UND_LOGOS_3.33.1.md)).

## Qualität und Sicherheit

- **Glide-Prüfung** (`.github/workflows/python-app.yml`): CI-Grundstufe unter Linux. Die Integrationssuiten unter Linux lassen sich zusätzlich von Hand starten; maßgeblich bleibt die Vollprüfung auf dem Mac.
- **CodeQL** (`.github/workflows/codeql.yml`): statische Sicherheitsanalyse für Python und die Workflows; Funde unter *Security → Code scanning*.
- **Dependabot:** schlägt wöchentlich Aktualisierungen der verwendeten GitHub Actions vor.
- **Secret Scanning:** aktiv; Schlüssel, Zertifikate und Signing-Secrets gehören nie ins Repository.
- **Schwachstellen melden:** vertraulich über *Security → Report a vulnerability*, nicht über öffentliche Issues ([Sicherheitsrichtlinie](SECURITY.md)). Technische Regeln der Anwendung: [SECURITY.md](01_Repository/Glide/SECURITY.md).

## Weitere Unterlagen

- **Einstieg:** [Sitzungsübergabe](00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md) · [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md) · [Dokumentationsindex](01_Repository/Glide/docs/00_INDEX.md) · [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md)
- **Aktuelle Verträge:** [Fundament 3.33.0](01_Repository/Glide/docs/73_FUNDAMENT_3.33.0.md) · [Bereiche und Fenster 3.33.1](01_Repository/Glide/docs/74_BEREICHE_UND_FENSTER_3.33.1.md) · [Modernisierung 3.30](01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md) · [Zeichnungsseite 3.29](01_Repository/Glide/docs/65_ZEICHNUNGSSEITE_3.29.0.md) · [Tagebuch und UI 3.28](01_Repository/Glide/docs/59_TAGEBUCH_UND_UI_3.28.0.md) · [Flackern und Ablageprüfung 3.28](01_Repository/Glide/docs/60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md)
- **Bedienung einzelner Bereiche:** [Erinnerungen](01_Repository/Glide/docs/archiv/31_ERINNERUNGEN_3.8.0.md) · [Systemmitteilungen](01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md) · [Vorlagen](01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md) · [Kalenderimport (ICS)](01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md) · [Kalenderausgabe (ICS)](01_Repository/Glide/docs/archiv/44_KALENDERAUSGABE_3.20.0.md) · [Änderungsverlauf in der App](01_Repository/Glide/docs/archiv/43_AENDERUNGSVERLAUF_3.19.0.md) · [CSV-Import](01_Repository/Glide/docs/archiv/42_CSV_IMPORT_3.18.0.md) · [Druck und PDF](01_Repository/Glide/docs/archiv/41_DRUCK_UND_PDF_3.17.0.md) · [Bearbeitungstag und Aufwand](01_Repository/Glide/docs/archiv/37_PLANUNG_UND_AUFWAND_3.14.0.md) · [Tabellenansicht](01_Repository/Glide/docs/archiv/36_TABELLENANSICHT_3.13.0.md)
- **Konzepte und frühere Entscheidungen:** [Seiten wie Notion](00_Arbeitsvorbereitung/Glide_Konzept_Seiten_wie_Notion_2026-09-26.md) · [Bestandsprüfung 27.09.2026](00_Arbeitsvorbereitung/Glide_Bestandspruefung_und_Entscheidungen_2026-09-27.md) · [Übersicht 29.09.2026](00_Arbeitsvorbereitung/Glide_Uebersicht_und_Entscheidungen_2026-09-29.md) · [Zeichenfläche](00_Arbeitsvorbereitung/Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md) · [Ablageprotokoll](01_Repository/Glide/docs/archiv/28_ABLAGEPRUEFUNG_2026-09-11.md)

## Lizenz

Das Repository ist öffentlich sichtbar, für Glide ist aber noch keine öffentliche Softwarelizenz festgelegt. Der Quelltext räumt derzeit keine allgemeinen Nutzungs-, Änderungs- oder Weiterverteilungsrechte ein; maßgeblich ist der [Lizenzstatus](01_Repository/Glide/LICENSE.md).
