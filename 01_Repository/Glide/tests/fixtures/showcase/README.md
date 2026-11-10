# Glide · aktiver Showcase

Stand 10.11.2026 · Glide 3.54.0 · Erster öffentlicher Stand · Quellfixtures und Lieferung in Speicherstufe 26

Das fiktive Projekt **Parkquartier** zeigt fertige, bearbeitbare Arbeitsdokumente: Briefing, Abstimmungsnotiz, Aufgabenliste, Bildgalerie, Pixelskizze mit Bildfolge, Routinen, Wiedervorlagen und Projekttagebuch. Die sechs Originalmotive liegen unverändert unter `tests/fixtures/showcase/bilder`; Herkunft und Prüfsummen stehen in `quellen.json`. Seit 03.10.2026 liegen sie ausschließlich in dieser Fixture-Ablage, zuvor zusätzlich im Grafikmaster. Sie illustrieren Themen; sie zeigen kein reales Verkaufsobjekt. Personen und Projektangaben sind fiktiv.

## Neu in diesem Showcase (06.11.2026)

Der bisherige Showcase stammte inhaltlich aus 3.44.0. Diese Fassung macht sichtbar, was seither dazugekommen ist, ohne neue Dokumente oder Datenformate:

| Bereich | Wo im Showcase | Seit |
|---|---|---|
| Realistischer Tag: Kapazität je Wochentag (Mo–Fr 4–6 Stunden) und Tagesziel 4 | Heute, Kalender, „Was passt heute?“, Tag entlasten | 3.33.17, je Wochentag mit D57 |
| Erweiterte Rhythmen: zweiter Dienstag im Monat, Abstand nach Erledigung, begrenzte Anzahl (noch 3), pausierte Reihe | Wiedervorlagen · Projektrhythmus | 3.44.0 (FP-02) |
| Gespeicherte Ansicht „Diese Woche · Eisenhower“: Oder-Bedingungen, Tabelle, Eisenhower-Gruppen, eigene Spalten | Seitenleiste › gespeicherte Ansichten; „Filter erklären …“ | 3.44.0 (FP-03) |
| Seiten- und Notizkarten mit Originaltitel und Verbindungen zu Aufgaben | Globale Pinnwand | 3.44.0 (FP-04) |
| Unverknüpfte Erwähnung: der Rückblick nennt „Vermarktung · Umsetzung“ ohne Verweis | Liste öffnen › „Verweise und Rückverweise“ bzw. Seitenfuß „Erwähnt ohne Verweis“ | 3.44.0 (FP-05) |
| Eigener KI-Auftrag „Rückmeldungen zu Aufgaben bündeln“ mit vollständiger Vorschau | Datei › Für KI bereitstellen | 3.44.0 (FP-06) |
| Live-Liste: das Briefing zeigt den aktuellen Stand der Umsetzungsliste | Parkquartier · Briefing und Freigabe | 3.33.15 |
| Lokale Verweise: die Abstimmungsnotiz verweist auf Briefing und Umsetzungsliste, Rückverweise entstehen automatisch | Abstimmung · Entwurf 02 | 3.33.17 |
| Bildfolge mit vier Bildern (ziehende Wolke), abspielbar und als Spritesheet exportierbar | Quartier · Pixelskizze › Bilder / Abspielen | 3.40.0 |
| Zwei Aufgaben als Reiter geöffnet | Ansicht › Reiter | 3.10.0, erstmals im Showcase vorbelegt |
| Startseiten-Suchfeld, Vorlagenfilter, Titelgrenzen, einzeilige Werkzeugleisten | überall, ohne eigene Daten | 3.50.5 |

## Starten und weiterbenutzen

[Showcase_starten.pyw](Showcase_starten.pyw) mit dem für Glide verwendeten Python öffnen. Der Starter verwendet die aktuelle Fassung aus `07_Python-Versionen` und legt neben sich den separaten Ordner `Arbeitsstand` an. Beim ersten Start lädt er das App-Backup. Weitere Starts behalten deine Bearbeitungen. Der normale Glide-Datenordner wird dabei nicht geöffnet. Wer den neuen Showcase sehen möchte, benennt einen vorhandenen `Arbeitsstand` bei geschlossener App um und startet erneut.

Falls macOS `.pyw` nicht direkt öffnet: im Terminal `python3` eingeben, den Starter hineinziehen und Enter drücken. Das für Glide eingerichtete Python mit Tk verwenden.

## Die Dateien

| Datei | Zweck |
|---|---|
| [Glide-Showcase.glidebackup](Glide-Showcase.glidebackup) | Projekt mit zehn Dokumenten und zwei Projektpinnwänden über **Datei → Listen/Ordner hinzufügen …** ergänzen. Bestehende Aufgaben und Einstellungen bleiben erhalten. |
| [Glide-Showcase_App.glideapp](Glide-Showcase_App.glideapp) | Vollständiger Demostand mit Eingang, Startseite, angehefteten Dokumenten, zwei gespeicherten Ansichten, Kapazität, Reitern, eigenem KI-Auftrag, globaler Pinnwand mit Seitenkarten und Vorlagen. Der Starter lädt ihn nur in den eigenen Arbeitsstand. |
| [Glide-Showcase.glidetemplates](Glide-Showcase.glidetemplates) | Zwei zusätzliche, portable Vorlagen: Abstimmung mit selbstfüllenden Datumsfeldern und Projektabfrage sowie Wochenstart-Checkliste. |
| [manifest.json](manifest.json) | Erzeugungstag, Dokumente und SHA-256 der gelieferten Basisdateien. |

Die Wiederherstellung eines App-Backups ersetzt den gewählten Bestand und seine gewählten Zusatzbereiche. Zum Showcase den Starter verwenden. Die Teilbackup-Datei ist für das Hinzufügen in einen bestehenden Bestand vorgesehen.

## Rundgang durch einen Arbeitstag

1. **Startseite:** eingeplante Aufgaben, Fortschritt, nächste Aufgabe und angeheftetes Briefing ansehen. Im Feld „Global suchen“ etwa „Freigabe“ eingeben und mit Enter in die globale Suche wechseln.
2. **Heute:** Steckbrief um 09:00 und Bildauswahl um 10:30; die Fälligkeit ist gesondert gesetzt. Oben rechts steht die Kapazität des Tages. „Was passt heute?“ erklärt den Vorschlag, „Tag entlasten“ zeigt vor dem Verschieben die Bilanz vorher und nachher und lässt Fälligkeiten unverändert.
3. **Briefing:** Architekturmotiv, Wohnatmosphäre, Planungsmotiv und den geschlossenen Block „Details der Bildauswahl“ öffnen. Die Live-Liste zeigt den aktuellen Stand von „Vermarktung · Umsetzung“; Aufgaben im Text lassen sich abhaken. Blöcke am Sechspunktgriff ziehen, Rechtsklick öffnet die Blockaktionen.
4. **Vermarktung · Umsetzung:** Steckbrief, Bildauswahl, Entwurf und Übergabe mit Wichtigkeit, Labels, Beschreibung, Checkliste, Anhängen, Bearbeitungstag, Uhrzeit, Aufwand, erfasster Zeit und Abhängigkeiten. Liste, Tabelle und Spaltenboard ausprobieren; zwei Aufgaben sind bereits als Reiter geöffnet.
5. **Gespeicherte Ansichten:** „Parkquartier · Freigabe“ filtert nach Label; „Diese Woche · Eisenhower“ zeigt Aufgaben dieser Woche oder mit mindestens 30 Minuten Aufwand als Tabelle in Eisenhower-Gruppen. „Filter erklären …“ nennt den Grund je Aufgabe.
6. **Pinnwände:** Den obersten Showcase-Ordner öffnen: fünf Karten, zwei beschriftete Verbindungen und ein benannter Bereich; die Pixelskizze ist als Dokumentverweis angeheftet. Die globale Pinnwand verbindet Briefing- und Notizkarte mit echten Aufgaben.
7. **Notiz, Verweise und Notizbuch:** Die Abstimmungsnotiz verweist auf Briefing und Umsetzungsliste; „Verweise und Rückverweise“ zeigt beide Richtungen. Der Rückblick erwähnt die Umsetzungsliste ohne Verweis und erscheint dort unter „Erwähnt ohne Verweis“. Notizbuchseiten tragen Datum, Stimmung, Ort und Favorit im Mehr-Menü. Die archivierte Vorbereitung ist über die Archivansicht zurückholbar.
8. **Pixel-Werkstatt:** In „Zeichnungen“ die Pixelskizze öffnen. „Bilder …“ zeigt vier Bilder, „Abspielen …“ die ziehende Wolke; Mehr › Bildfolge exportiert Spritesheet oder Einzelbilder mit Zeitachse. 32 × 32 Zeichnung mit PNG-Referenz, 16 × 16 Symbol und ICO-Anhang. GPL-/HEX-Paletten, CSV-Steckbrief und TXT-Übergabe liegen an der Umsetzungsliste.
9. **Wiedervorlagen:** alle sieben Wiederholungsarten, Serien am letzten Werktag und am zweiten Dienstag, „Atelierpflanzen gießen“ drei Tage nach Erledigung, „Fototermin bestätigen“ nur noch dreimal und der pausierte „Newsletter-Entwurf“.
10. **KI-Austausch:** Datei › Für KI bereitstellen zeigt fünf mitgelieferte Aufträge und den eigenen Auftrag „Rückmeldungen zu Aufgaben bündeln“ mit vollständiger Vorschau. Glide verbindet sich dabei mit keinem Dienst.
11. **Vorlagen:** `{{Wochentag}}` und `{{KW}}` werden automatisch gefüllt; nur `{{Projekt}}` wird abgefragt. Die Notizvorlage enthält Aufgaben und einen Bildanhang. Das Suchfeld filtert Vorlagen nach Titel, Beschreibung und Inhalt.
12. **Tagesabschluss:** offene Tagesaufgaben umplanen und den Rückblick in die Tagesnotiz übernehmen. Die Wochenstart-Checkliste öffnet sich nach vollständigem Abhaken wieder.

## Abdeckung und Prüfgrenzen

Alle fünf Dokumentarten, alle drei Ordnertypen, alle vier Punktarten, alle sieben Wiederholungsarten einschließlich der erweiterten Serienoptionen (n-ter und letzter Werktag, Bezug auf Erledigung, Anzahl, Pause) und beide Erinnerungsarten sind enthalten. Die App-Variante enthält 33 Punkte in elf Dokumenten einschließlich Eingang; das Teilbackup die zehn Projektdokumente. 15 Anhangdateien sind vollständig eingebettet, darunter JPEG, PNG, ICO, GPL, HEX, CSV und TXT. Das App-Backup ergänzt die globale Pinnwand mit Seitenkarten, zwei gespeicherte Ansichten, Kapazität und Tagesziel, zwei Reiter, einen eigenen KI-Auftrag und den Katalog mit 22 Vorlagen.

Ein Showcase kann nicht jede Bedienhandlung als gespeicherten Inhalt darstellen. Automatisierte Prüfungen kontrollieren zusätzlich Import/Export, ID-Zuordnung, Bilder, Klappblock, Undo, Vorlagen und Neustart. Klappmechanismen, Drag-and-drop, Datumsaktionen, Pixel-/Palettenexport und Performance werden durch die vorhandenen Pflichtsuiten geprüft. Eine lokale Kalenderdatei als Belegzeit ist bewusst nicht enthalten, weil sie auf einen Pfad des eigenen Rechners zeigt. OS-Druckdialog, physische Maus/Trackpad, Windows/Linux und Screenreader bleiben manuelle Abnahme.

Backups behalten ihre konkreten Termine beim Import. Der Bearbeitungstag dieses Bestands ist gemäß `manifest.json` **06.11.2026**; später erscheinen alte Aufgaben überfällig. Zum Auffrischen aus `01_Repository/Glide`:

```sh
GLIDE_QA_HINTERGRUND=1 PYTHONPATH=tests/tools/hintergrund python3 -B tests/tools/showcase.py
python3 -B scripts/pflege/showcase_abgleich.py
```

Der Abgleich prüft die Demo vor der Auslieferung und ersetzt die Basisdateien; frühere Fassungen hält Git vor. Dein bearbeiteter `Arbeitsstand` bleibt erhalten. Für eine neue Demo den bisherigen Arbeitsstand bei geschlossener App umbenennen und den Starter erneut öffnen.

Mobile Nutzung, GIF-Animationsexport und allgemeine Typkonvertierung gehören nicht zur aktuellen App. Maßgeblich sind die aktuelle Arbeitsrichtung mit D01–D63 (D49 mit Korrekturvorbehalt) und der Entwicklungsplan; die menschliche Prüfung folgt anschließend; Screenreader ist bis Bedarf zurückgestellt.
