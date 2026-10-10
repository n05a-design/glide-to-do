# Glide · aktiver Showcase

Stand 10.10.2026 · Glide 3.37.0 · Aufgabenformat 23

Das fiktive Projekt **Parkquartier** zeigt fertige, bearbeitbare Arbeitsdokumente: Briefing, Abstimmungsnotiz, Aufgabenliste, Bildgalerie, Pixelskizze, Routinen und Projekttagebuch. Die sechs Originalmotive stammen unverändert aus `20_Grafik_Master/06_Beispielbilder`. Sie illustrieren Themen; sie zeigen kein reales Verkaufsobjekt. Personen und Projektangaben sind fiktiv.

## Starten und weiterbenutzen

[Showcase_starten.pyw](Showcase_starten.pyw) mit dem für Glide verwendeten Python öffnen. Der Starter verwendet die aktuelle Fassung aus `07_Python-Versionen` und legt neben sich den separaten Ordner `Arbeitsstand` an. Beim ersten Start lädt er das App-Backup. Weitere Starts behalten deine Bearbeitungen. Der normale Glide-Datenordner wird dabei nicht geöffnet.

Falls macOS `.pyw` nicht direkt öffnet: im Terminal `python3` eingeben, den Starter hineinziehen und Enter drücken. Das für Glide eingerichtete Python mit Tk verwenden.

## Die Dateien

| Datei | Zweck |
|---|---|
| [Glide-Showcase.glidebackup](Glide-Showcase.glidebackup) | Projekt mit zehn Dokumenten und zwei Projektpinnwänden über **Datei → Listen/Ordner hinzufügen …** ergänzen. Bestehende Aufgaben und Einstellungen bleiben erhalten. |
| [Glide-Showcase_App.glideapp](Glide-Showcase_App.glideapp) | Vollständiger Demostand mit Eingang, Startseite, angehefteten Dokumenten, gespeicherter Freigabesuche, globaler Pinnwand und Vorlagen. Der Starter lädt ihn nur in den eigenen Arbeitsstand. |
| [Glide-Showcase.glidetemplates](Glide-Showcase.glidetemplates) | Zwei zusätzliche, portable Vorlagen: Abstimmung mit selbstfüllenden Datumsfeldern und Projektabfrage sowie Wochenstart-Checkliste. |
| [manifest.json](manifest.json) | Erzeugungstag, Dokumente und SHA-256 der gelieferten Basisdateien. |

Die Wiederherstellung eines App-Backups ersetzt den gewählten Bestand und seine gewählten Zusatzbereiche. Zum Showcase den Starter verwenden. Die Teilbackup-Datei ist für das Hinzufügen in einen bestehenden Bestand vorgesehen.

## Rundgang durch einen Arbeitstag

1. **Startseite:** eingeplante Aufgaben, Fortschritt, nächste Aufgabe und angeheftetes Briefing ansehen.
2. **Briefing:** Architekturmotiv, Wohnatmosphäre, Planungsmotiv und den geschlossenen Block „Details der Bildauswahl“ öffnen. Die drei Bildpositionen sind mittig, links und rechts. Aufgaben im Text lassen sich abhaken.
3. **Bildwelt:** sechs Bilder mit Titeln und Kommentaren; Doppelklick zeigt ein Motiv groß. Die Originale sind im Backup enthalten.
4. **Vermarktung · Umsetzung:** Steckbrief, Bildauswahl, Entwurf und Übergabe mit Wichtigkeit, Labels, Beschreibung, Checkliste, Anhängen, Bearbeitungstag, Uhrzeit, Aufwand, erfasster Zeit und Abhängigkeiten. Liste, Tabelle und Pinnwand ausprobieren.
5. **Projektpinnwand:** den obersten Showcase-Ordner öffnen. Fünf Karten, zwei beschriftete Verbindungen und ein benannter Bereich; die Pixelskizze ist als Dokumentverweis angeheftet.
6. **Mein Tag:** Steckbrief um 09:00 und Bildauswahl um 10:30. Die Fälligkeit ist gesondert gesetzt. Ziehen in einen bezeichneten Terminkontext wirkt auf dessen Feld.
7. **Notiz und Tagebuch:** Aufgaben stehen oberhalb des Protokolls. Tagebuchnotizen tragen Datum, Stimmung, Ort und Favorit. Die archivierte Vorbereitung ist über die Archivansicht zurückholbar.
8. **Pixel-Werkstatt:** In „Zeichnungen“ die Pixelskizze öffnen. Bücher/Seiten, Notizbuch und Zeichnung haben jetzt eigene Bereiche; die gemischte Projektarbeit bleibt in Listen. In den Einstellungen Bereiche ausblenden und ihre vollständigen Zweige weiter in Listen öffnen. 32 × 32 Zeichnung mit PNG-Referenz, 16 × 16 Symbol und ICO-Anhang. GPL-/HEX-Paletten, CSV-Steckbrief und TXT-Übergabe liegen an der Umsetzungsliste.
9. **Vorlagen:** `{{Wochentag}}` und `{{KW}}` werden automatisch gefüllt; nur `{{Projekt}}` wird abgefragt. Die Notizvorlage enthält Aufgaben und einen Bildanhang.
10. **Tagesabschluss:** offene Tagesaufgaben umplanen und den Rückblick in die Tagesnotiz übernehmen. Die Wochenstart-Checkliste öffnet sich nach vollständigem Abhaken wieder.

## Abdeckung und Prüfgrenzen

Alle fünf Dokumentarten, alle drei Ordnertypen, alle vier Punktarten, alle sechs Wiederholungsarten und beide Erinnerungsarten sind enthalten. Die App-Variante enthält 28 Punkte in elf Dokumenten einschließlich Eingang; das Teilbackup 26 Punkte in zehn Projektdokumenten. 15 Anhangdateien sind vollständig eingebettet, darunter JPEG, PNG, ICO, GPL, HEX, CSV und TXT. Das App-Backup ergänzt die globale Pinnwand und den Katalog mit 22 Vorlagen.

Ein Showcase kann nicht jede Bedienhandlung als gespeicherten Inhalt darstellen. Automatisierte Prüfungen kontrollieren zusätzlich Import/Export, ID-Zuordnung, Bilder, Klappblock, Undo, Vorlagen und Neustart. Klappmechanismen, Drag-and-drop, Datumsaktionen, Pixel-/Palettenexport und Performance werden durch die vorhandenen Pflichtsuiten geprüft. OS-Druckdialog, physische Maus/Trackpad, Windows/Linux und Screenreader bleiben manuelle Abnahme.

Backups behalten ihre konkreten Termine beim Import. Dieser Stand wurde am **01.10.2026** erzeugt; später erscheinen alte Aufgaben überfällig. Zum Auffrischen aus `01_Repository/Glide`:

```sh
GLIDE_QA_HINTERGRUND=1 PYTHONPATH=tests/tools/hintergrund python3 -B tests/tools/showcase.py
python3 -B scripts/pflege/showcase_abgleich.py
```

Der Abgleich prüft die Demo vor der Auslieferung und ersetzt die Basisdateien; frühere Fassungen hält Git vor. Dein bearbeiteter `Arbeitsstand` bleibt erhalten. Für eine neue Demo den bisherigen Arbeitsstand bei geschlossener App umbenennen und den Starter erneut öffnen.

Mobile Nutzung, GIF-Animationsexport, allgemeine Typkonvertierung und die noch offene Richtungswahl sind nicht Bestandteil der aktuellen App. Die bestehenden Entscheidungen D01–D08 bleiben maßgeblich.
