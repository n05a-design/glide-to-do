# Probedaten

Stand 03.11.2026 · Glide 3.50.2 · Erster öffentlicher Stand · Speicherstufe 26 · Vorlagen 2

Hier liegt nur noch der **[Showcase](Showcase/README.md)**: das fiktive Projekt „Parkquartier“ mit zehn bearbeitbaren Dokumenten in allen fünf Arten, sechs Originalmotiven aus der kanonischen Fixture-Ablage `01_Repository/Glide/tests/fixtures/showcase/bilder`, Projekt- und Demo-Pinnwand, Tagesplanung, Notizbuch, Archiv und zwei Vorlagen. Herkunft und Prüfsummen stehen in `showcase/quellen.json` des Quellbaums; die Motive lagen früher zusätzlich im Grafikmaster. `Showcase_starten.pyw` hält den Demobestand im eigenen Ordner `Arbeitsstand` (nicht versioniert) und öffnet nie den normalen Datenordner.

Quellfixtures und Showcase-Lieferung sind für 3.50.2 mit künstlichen Daten zum 03.11.2026 reproduziert und über echten Import/Neustart sowie SHA-256 abgeglichen. Der bearbeitete separate Arbeitsstand wird dabei nicht ersetzt. Die konkreten Archivhashes stehen im jeweiligen `manifest.json`; Prüfungen und tatsächliche Pakete im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md). Menschliche Prüfung anschließend; Screenreader bis Bedarf zurückgestellt.

## Weitere Probebestände (Quelle im Repository)

| Bestand | Ort | Erzeuger |
|---|---|---|
| Rundgang (je eine Liste, Notiz, Seite mit Bildern, Zeichnung) | `01_Repository/Glide/tests/fixtures/beispiele/glide_rundgang.glidebackup` | `tests/tools/rundgang.py` |
| Funktionsvorschau (künstliche Arbeitslisten, alle Punktarten) | `…/beispiele/glide_beispieldaten.glidebackup` | `tests/tools/beispieldaten.py` |
| Releaseplanung der aktuellen Quellversion | `…/beispiele/glide_releaseplanung_3.50.2.glidebackup` | `tests/tools/releasedaten.py` |
| Praxisvorlagen | `01_Repository/Glide/src/glide/resources/templates/glide_vorlagen.glidetemplates` | `tests/tools/vorlagendaten.py` |

Über **Datei → Listen/Ordner hinzufügen …** ergänzen sie einen Bestand; Vorlagen über den Vorlagendialog. Anleitung: [Vorlagen in der Praxis](../01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md). Die bis 02.10.2026 hier liegenden Nutzerkopien von 3.30.0 und das Archiv älterer Fassungen sind gelöscht; Vorfassungen trägt Git.

## Umgang mit echten Daten

Alle Dateien sind künstlich und enthalten keine echten Personen-, Kunden- oder Objektdaten. Backups behalten beim Import ihre konkreten Termine; ein am Erzeugungstag fälliger Punkt ist später überfällig. Zum Ausprobieren eine getrennte Ablage (`GLIDE_DATA_DIR`) oder den Starter verwenden: Das Wiederherstellen eines App-Backups **ersetzt** den vorhandenen Bestand.
