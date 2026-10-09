# Probedaten

Stand 09.10.2026 · Glide 3.35.0 · Aufgabenformat 23 · Vorlagen 2

Hier liegt nur noch der **[Showcase](Showcase/README.md)**: das fiktive Projekt „Parkquartier“ mit zehn bearbeitbaren Dokumenten in allen fünf Arten, sechs Originalmotiven aus `20_Grafik_Master/06_Beispielbilder`, Projekt- und Demo-Pinnwand, Tagesplanung, Tagebuch, Archiv und zwei Vorlagen. `Showcase_starten.pyw` hält den Demobestand im eigenen Ordner `Arbeitsstand` (nicht versioniert) und öffnet nie den normalen Datenordner.

Die Dateien sind bytegleiche Kopien von `01_Repository/Glide/tests/fixtures/showcase` (Abgleich `scripts/pflege/showcase_abgleich.py`, SHA-256 in `manifest.json`). Git speichert gleiche Inhalte nur einmal.

## Weitere Probebestände (Quelle im Repository)

| Bestand | Ort | Erzeuger |
|---|---|---|
| Rundgang (je eine Liste, Notiz, Seite mit Bildern, Zeichnung) | `01_Repository/Glide/tests/fixtures/beispiele/glide_rundgang.glidebackup` | `tests/tools/rundgang.py` |
| Funktionsvorschau (künstliche Arbeitslisten, alle Punktarten) | `…/beispiele/glide_beispieldaten.glidebackup` | `tests/tools/beispieldaten.py` |
| Releaseplanung der aktuellen Version | `…/beispiele/glide_releaseplanung_3.33.18.glidebackup` | `tests/tools/releasedaten.py` |
| Praxisvorlagen | `01_Repository/Glide/src/glide/resources/templates/glide_vorlagen.glidetemplates` | `tests/tools/vorlagendaten.py` |

Über **Datei → Listen/Ordner hinzufügen …** ergänzen sie einen Bestand; Vorlagen über den Vorlagendialog. Anleitung: [Vorlagen in der Praxis](../01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md). Die bis 02.10.2026 hier liegenden Nutzerkopien von 3.30.0 und das Archiv älterer Fassungen sind gelöscht; Vorfassungen trägt Git.

## Umgang mit echten Daten

Alle Dateien sind künstlich und enthalten keine echten Personen-, Kunden- oder Objektdaten. Backups behalten beim Import ihre konkreten Termine; ein am Erzeugungstag fälliger Punkt ist später überfällig. Zum Ausprobieren eine getrennte Ablage (`GLIDE_DATA_DIR`) oder den Starter verwenden: Das Wiederherstellen eines App-Backups **ersetzt** den vorhandenen Bestand.
