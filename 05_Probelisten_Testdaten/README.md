# Probedaten

Stand 14.11.2026 · Glide 3.61.0 · Speicherstufe 26 · Vorlagen 2

Der [Showcase „Werkhaus West“](Showcase/README.md) enthält 14 bearbeitbare Projektdokumente, vier Stock-Referenzen, beschriftete Pinnwände, Tagesplanung, Vorlagen und einen JSON-Canvas-Export. Der Starter hält den Bestand im eigenen Arbeitsordner `Arbeitsstand-Werkhaus`.

## Weitere Probebestände (Quelle im Repository)

| Bestand | Ort | Erzeuger |
|---|---|---|
| Rundgang (je eine Liste, Notiz, Seite mit Bildern, Zeichnung) | `01_Repository/Glide/tests/fixtures/beispiele/glide_rundgang.glidebackup` | `tests/tools/rundgang.py` |
| Funktionsvorschau (künstliche Arbeitslisten, alle Punktarten) | `…/beispiele/glide_beispieldaten.glidebackup` | `tests/tools/beispieldaten.py` |
| Releaseplanung der aktuellen Quellversion | `…/beispiele/glide_releaseplanung_3.55.1.glidebackup` | `tests/tools/releasedaten.py` |
| Praxisvorlagen | `01_Repository/Glide/src/glide/resources/templates/glide_vorlagen.glidetemplates` | `tests/tools/vorlagendaten.py` |

Über **Datei → Listen/Ordner hinzufügen …** ergänzen sie einen Bestand; Vorlagen über den Vorlagendialog. Anleitung: [Vorlagen in der Praxis](../01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md). Die bis 02.10.2026 hier liegenden Nutzerkopien von 3.30.0 und das Archiv älterer Fassungen sind gelöscht; Vorfassungen trägt Git.

## Umgang mit echten Daten

Alle Dateien sind künstlich und enthalten keine echten Personen-, Kunden- oder Objektdaten. Backups behalten beim Import ihre konkreten Termine; ein am Erzeugungstag fälliger Punkt ist später überfällig. Zum Ausprobieren eine getrennte Ablage (`GLIDE_DATA_DIR`) oder den Starter verwenden: Das Wiederherstellen eines App-Backups **ersetzt** den vorhandenen Bestand.
