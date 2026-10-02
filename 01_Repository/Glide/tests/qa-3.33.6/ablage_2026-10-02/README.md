# Schlanke Ablage 3.33.6 – Nachweis

Datiert 02.10.2026 · App unverändert 3.33.6 · Ablage-, Werkzeug- und Dokumentationsnachlauf, keine Produktionsversion

## Anlass

- **Beobachtung des Inhabers:** Der Projektordner belegte plötzlich deutlich mehr Speicher.
- **Befund:** Mit dem Pull Request für 3.33.1–3.33.6 (n05a-design/glide-to-do#9) wuchs der versionierte Stand von 1,2 auf 2,0 GB. 544 Dateien kamen hinzu, rund 794 MB netto.
- **Ursachen:**
  - `versionswechsel.py` legte bei jedem Versionswechsel vollständige Kopien von Showcase, Beispieldaten und Rundgang in `tests/fixtures/**/archiv` ab, je Wechsel rund 75 MB.
  - `showcase_abgleich.py` kopierte bei jedem Lauf die bisherige Lieferfassung nach `05_Probelisten_Testdaten/Showcase/archiv`, je Lauf rund 73 MB.
  - Jede Vollprüfung brachte im Ordner `fenster/` rund 25 MB Bildschirmfotos mit, auch Fehlversuche.
  - Eine abgebrochene Übertragung hinterließ `Glide-Showcase_App.glideapp.fetch` (36 MB).
- **Git hält alle Vorfassungen ohnehin vor.** Die Archive waren sogar doppelt: `05_Probelisten_Testdaten/Showcase/archiv` und `tests/fixtures/showcase/archiv` enthielten dieselben Showcase-Fassungen paarweise bytegleich.
- **Entscheidung des Inhabers:** Archivkopien entfernen, Werkzeuge ändern, von den Fensterbildern nur die letzte Vollprüfung je Version behalten und künftig nur Ergebnis und README versionieren.

## Umsetzung

| Bereich | Änderung | Umfang |
|---|---|---|
| `05_Probelisten_Testdaten/Showcase/archiv` | gelöscht | 24 Dateien, 438 MB |
| `tests/fixtures/showcase/archiv` | gelöscht | 23 Dateien, 291 MB |
| `tests/fixtures/beispiele/archiv` | Versionsschritt-Kopien gelöscht. Behalten wird die ursprüngliche Beispieldatei vor dem Showcase (24 KB), die der Dokumentationsindex als Vorsicherung verlinkt | 14 Dateien, 13 MB |
| `tests/fixtures/showcase/Glide-Showcase_App.glideapp.fetch` | Fehlrest gelöscht | 1 Datei, 36 MB |
| Fensterbilder | Überholte Vollprüfungen je Version entfernt. Ergebnis und README jedes Laufs bleiben (siehe unten) | 273 Dateien, 134 MB |
| [`versionswechsel.py`](../../../scripts/pflege/versionswechsel.py), [`showcase_abgleich.py`](../../../scripts/pflege/showcase_abgleich.py) | Legen keine Archivkopien mehr an | – |
| `.gitignore` (Wurzel und Quellbaum) | Schließen `*.fetch`, Archivordner unter `tests/fixtures` und `05_Probelisten_Testdaten/Showcase` sowie `tests/qa-*/**/fenster/` aus. Bereits versionierte Dateien bleiben erhalten | – |
| CI-Schritt „Ablagegröße“ | Neu: [`ablagegroesse.py`](../../tools/ablagegroesse.py) mit [Werkzeugtests](../../tools/test_ablagegroesse.py) | – |
| Regeln | D09 in Arbeitsrichtung und Entscheidungsvorlage, Dokumentenpflege, `CLAUDE.md`, Übergabe, READMEs, Testplan, Showcase-Vertrag, CHANGELOG | – |

**Ergebnis:** 335 Dateien mit 912 MB entfernt. Der versionierte Stand sinkt von 2016 MB in 5315 Dateien auf rund 1104 MB.

### Entfernte Fensterbilder (überholte Läufe)

| Version | Entfernt | Behalten (letzte Vollprüfung) |
|---|---|---|
| 3.31.0 | `nachpruefung_erster_lauf_2026-09-30` (Exit 1) | `nachpruefung_2026-09-30` |
| 3.32.0 | `etappe1_vor_bildseite_2026-09-30` (Exit 1) | `etappe1_2026-09-30` |
| 3.32.3 | `karten_performance_2026-10-01/vollpruefung` | `showcase_2026-10-01/vollpruefung_isoliert` |
| 3.33.1 | `bereiche_fenster_2026-10-01/vollpruefung` (Exit 1), `abschluss_2026-10-01/vollpruefung_2` (Exit 1) | `abschluss_2026-10-01/vollpruefung_3` |
| 3.33.2 | `startseite_2026-10-02/vollpruefung_versuch1` (Exit 1) | `startseite_2026-10-02/vollpruefung` |

Für 3.30.0, 3.32.1, 3.32.2, 3.33.0 und 3.33.3–3.33.6 gab es nur einen Lauf mit Bildern; er bleibt.

## Ablagegröße (neuer CI-Schritt)

| Regel | Wirkung |
|---|---|
| Fehlreste | Keine `*.fetch`-Dateien |
| Archivkopien | Keine `.glidebackup`, `.glideapp` oder `.glidetemplates` in Archivordnern unter `tests/fixtures` und `05_Probelisten_Testdaten/Showcase`; einzige Ausnahme ist die verlinkte Vorsicherung |
| Fensterbilder | Keine PNG in `fenster/` von Vollprüfungen nach 3.33.6 |
| Dateigröße | Keine Datei über 50 MB (GitHub warnt ab 50 MB und lehnt ab 100 MB ab) |

## Prüfung (Linux-Container, Python 3.14.0rc2, Tk 8.6.14)

- **Werkzeugtests:** `test_ablagegroesse.py` mit 7 Fällen bestanden, darunter Gegenproben je Regel und erlaubte Fälle (aktuelle Fixtures, Vorsicherung, bestehende Fensterbilder, `ergebnis.json` neuer Läufe).
- **Gegenprobe gegen den Stand vor der Bereinigung:** Für `8ded10f` meldet die Regel 46 Archivkopien und einen Fehlrest.
- **`.gitignore`:**
  - Neue Dateien in `fenster/`, Archivordnern und `*.fetch` erscheinen nicht als unversioniert; `ergebnis.json` neuer Läufe weiterhin schon.
  - Die 50 bestehenden Fensterbilder von 3.33.6 bleiben versioniert.
- **CI-Grundstufe:** alle Schritte bestanden, einschließlich Ablagegröße ([Ergebnis](grundstufe/ergebnis.json)).
- **Kein Test liest Archivdateien:** Die Fixtureprüfung überspringt `archiv`; kein Werkzeug und keine Suite verweist auf die gelöschten Dateien.

## Grenzen

- **Git-Historie unverändert:** Die gelöschten Dateien bleiben in der Historie. Ein frischer Klon lädt weiterhin rund 606 MB komprimierte Historie, vor dem Pull Request für 3.33.1–3.33.6 waren es 379 MB. Kleiner würde der Klon nur durch Umschreiben der Historie (Force-Push auf `main`, alle Arbeitskopien neu klonen); das war nicht beauftragt.
- **Lokale Arbeitskopie:** Nach dem Pull verschwinden die Dateien aus dem Projektordner. Ignorierte lokale Reste, etwa alte Rohprotokolle und Fensterbilder, löscht Git nicht; sie zeigt `git status --ignored`.
- **Nicht angefasst:**
  - Vorlagenarchiv `src/glide/resources/templates/archiv` (10 MB). Es gehört zum Lieferstand und wird nur in einer Produktionsrunde geändert.
  - `07_Python-Versionen/Archiv` (148 MB, Ablösung über `abgleich_07.py`).
  - `50_Ablage`, `20_Grafik_Master`.
