# Werkhaus West · Glide-Showcase

Stand 14.11.2026 · Glide 3.60.0 · Aufgabenformat 26 · Vorlagen 2

Ein kleines Studio bereitet einen offenen Werkstatttag vor. Lea prüft den Weg vom Hof zur Modellwand, Mira wartet auf das Papiermuster, und Jona bringt die Materialplatten aus dem Lager. Die Aufnahmen zeigen denselben Arbeitsstand aus mehreren Blickwinkeln.

## Öffnen und bearbeiten

Im Projektordner unter Windows `py -3.14 05_Probelisten_Testdaten/Showcase/Showcase_starten.pyw` ausführen. Der Starter lädt die App-Sicherung beim ersten Öffnen in den Ordner `Arbeitsstand-Werkhaus`. Eigene Änderungen bleiben dort gespeichert. Die Beispieldaten sind auf Freitag, den 13.11.2026, bezogen. In Heute und Kalender lässt sich dieser Tag direkt auswählen.

| Datei | Verwendung |
|---|---|
| [Glide-Showcase_App.glideapp](Glide-Showcase_App.glideapp) | Gesamtes Beispiel mit Startseite, globaler Pinnwand, Einstellungen und Studiojournal. Für einen separaten Datenordner. |
| [Glide-Showcase.glidebackup](Glide-Showcase.glidebackup) | Bearbeitbares Projekt über **Datei → Listen/Ordner hinzufügen …** in einen Bestand übernehmen. |
| [Glide-Showcase.glidetemplates](Glide-Showcase.glidetemplates) | Kurzprotokoll mit Datums- und Projektfeldern sowie die wiederkehrende Checkliste fürs Aufschließen. |
| [Werkhaus-West.canvas](Werkhaus-West.canvas) | JSON Canvas 1.0 aus der globalen Pinnwand. Enthält Karten, Positionen und beschriftete Verbindungen. |
| [manifest.json](manifest.json) | Dokumente, Formatversion und SHA-256 der vier Dateien. |

## Ein Rundgang durch die Funktionen

- Auf der **globalen Pinnwand** führt die Seite zum Laufweg, die Freitagsnotiz liefert Rückfragen und das Einladungsmotiv verweist auf das Leitschild. Die Karten öffnen ihre Originale. Dieselbe Karte lässt sich in alternativen Arbeitskontexten über **Fundorte anzeigen** finden. Über das Pinnwandmenü ist der JSON-Canvas-Export verfügbar.
- Die **Startseite** zeigt Terminwoche und Arbeitsstand. **Heute** und der **Kalender** tragen Bearbeitungstag und Fälligkeit getrennt. Am 13.11. sind 200 Minuten bei 150 Minuten Kapazität eingeplant. In **Tag entlasten** lässt sich der Druckentwurf auf einen anderen Bearbeitungstag schieben und die Bilanz vorab ansehen. Der **Wochenrückblick** führt den Aufwand und das Erledigte zusammen.
- **Studioroutinen** kombiniert farbige Labels, reguläre Fälligkeiten, wiederkehrende Aufgaben und Serienregeln. **Offene Werkstatt** zeigt Anhänge, Prioritäten, Abhängigkeiten und die Bearbeitung im Punktinspektor. Zwei gespeicherte Ansichten führen zu Freigaben und einer nach Eisenhower gruppierten Wochenübersicht.
- Das **Werkstattbuch** hat fünf Seiten. Die Rundgangsseite enthält Bilder, Blöcke, eine eingebettete Live-Liste und einen Klappblock. Die **Nebenansicht** hält den Rundgang beim Bearbeiten des Boards lesbar und hat Suche, Abschnitte, Verweise und Verlauf.
- In **Raumstudien** liegen vier vorhandene Architektur- und Innenraummotive mit Arbeitskommentaren. In der **Pixel-Fabrik** lässt sich das Leitschild in vier Lichtstufen bearbeiten und abspielen. Die Freitagsnotiz, das Studiojournal und der archivierte Probelauf ergänzen den aktuellen Stand.

Der Showcase verwendet fiktive Texte und vorhandene Stock-Referenzen aus dem Grafikmaster. Der [Quellennachweis](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/tests/fixtures/showcase/quellen.json) nennt die Originaldateien und die Prüfsummen der komprimierten Arbeitskopien. Die [GitHub-Galerie](https://github.com/n05a-design/glide-to-do#ein-blick-hinein) zeigt die Windows-Aufnahmen.

## Aktualisieren

Im Verzeichnis `01_Repository/Glide` den Bestand mit `py -3.14 -B tests/tools/showcase.py --tag 2026-11-13` erzeugen. `py -3.14 -B scripts/pflege/showcase_abgleich.py` prüft Import, Vorlagen, Referenzen, Export und Neustart und gleicht die Dateien ab. Der [Aufnahmeablauf](https://github.com/n05a-design/glide-to-do/blob/main/20_Grafik_Master/README.md#projektaufnahmen-erneuern) erzeugt die Projektbilder.
