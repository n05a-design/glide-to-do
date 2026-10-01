# Manuelle Prüfung – Glide 3.23.0

Stand: 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16

Die automatisierten Prüfungen sind grün: 27 Suiten, vier Analysen, beide
Reproduktionsabgleiche. Diese Liste enthält, was **eine Person am Gerät**
prüfen muss – alles, was von Plattform, Eingabegerät oder Augenmaß abhängt.

**Vorher:** Ein vollständiges App-Backup anlegen (Datei → Vollständiges
App-Backup speichern). 3.23 bringt keinen Formatsprung; die Einstellungen
werden aber beim ersten Start um `design` ergänzt.

Diese Liste prüft die Änderungen des Stands. Was Plattform und Umgebung
beantworten – Skalierung, zweiter Monitor, Ruhezustand, Systemzeitzone,
synchronisierter Ordner, fremde Programme, Hilfsmittel – steht in der
[Abnahme am Gerät](Checklisten/Abnahme_Windows_macOS_3.23.0.md); sie führt die
Schritte von hier weiter und wird im
[Prüfprotokoll](Checklisten/Protokoll_Abnahme_3.23.0.md) festgehalten.

## 1. Designübernahme (Punkt 3)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 1.1 | 3.22 im Dunkelmodus mit eingeschalteter Materialoptik verlassen, 3.23 starten | Design steht auf „Liquid Glass · dunkel“, das Bild ist unverändert |
| 1.2 | Dasselbe mit Dopamin-Modus | Design steht auf „Dopamin · kräftige Farben“ |
| 1.3 | Dasselbe mit Kontrastmodus im Hellmodus | Design steht auf „Kontrast hell“ |
| 1.4 | `settings.json` ansehen | `design` gesetzt; `theme`, `color_mode`, `glass_mode` passen dazu |
| 1.5 | Design wechseln, Glide beenden und neu starten | Die Wahl ist erhalten |

## 2. Alle sieben Designs ansehen (Punkte 3, 4, 19)

Für **jedes** der sieben Designs einmal durchgehen:

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 2.1 | Startseite, Liste, Tabelle, Pinnwand, Kalender öffnen | Nichts ist unlesbar, keine Fläche bleibt ungefärbt |
| 2.2 | Mit dem Zeiger über Tabellenüberschriften fahren | Die Überschrift bleibt lesbar – **das war der Fehler** |
| 2.3 | Eine Zeile auswählen | Auswahltext lesbar auf der Auswahlfläche |
| 2.4 | In den beiden Liquid-Glass-Designs eine Karte ansehen | Oberes Drittel heller, Verlauf ohne Streifen an der Ecke |
| 2.5 | Hell-/Dunkel-Schalter drücken | Bleibt im gewählten Design; im Dopamin-Design tut er nichts |
| 2.6 | Unter Windows: Titelleiste eines Dialogs | Folgt dem Design, auch bei der Schnellerfassung |

## 3. Eingabegeräte (Punkte 15, 17 aus 3.22, hier erneut)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 3.1 | Pinnwand: Mausrad gedrückt halten und ziehen | Die Fläche folgt |
| 3.2 | Shift und Mausrad | Waagerechtes Scrollen |
| 3.3 | Trackpad: zwei Finger waagerecht | Waagerechtes Scrollen |
| 3.4 | macOS: Rechtsklick und Ctrl-Klick | Kontextmenü, kein Ziehen |

## 4. Pinnwand (Punkte 12, 13, 14)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 4.1 | Zwei Karten verbinden | Linie unter den Karten, betont bei ausgewählter Karte |
| 4.2 | Eine verbundene Karte verschieben | Die Linie folgt ohne Flackern |
| 4.3 | Glide beenden und neu starten | Verbindung ist noch da |
| 4.4 | Karte von der Pinnwand entfernen | Verbindung verschwindet, der Punkt bleibt in der Liste |
| 4.5 | Doppelklick auf freie Fläche, Text eingeben | Neue Karte an der Klickstelle; der Punkt steht auch in der Liste |
| 4.6 | „Fläche“ drücken | Vollbild, Scrollposition erhalten |
| 4.7 | Escape drücken | Zurück, Scrollposition erhalten |
| 4.8 | „Verbinden …“, dann Escape | Bricht nur das Verbinden ab, bleibt auf der Pinnwand |
| 4.9 | „Drucken und PDF …“ auf der Pinnwand | Seite zeigt alle Karten und Linien, kein Leerraum ringsum |
| 4.10 | Im Druckdialog als PDF sichern | Lesbar, Karten nicht abgeschnitten |
| 4.11 | Bildanhang an einem Punkt (PNG), Vorschau ein | Vorschau auf der Karte |

## 5. Schmale Fenster (Punkte 28 bis 32)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 5.1 | Fenster langsam schmaler ziehen | Erst „Benachrichtigungen“ zur Zahl, dann Drucken und Einstellungen ins ⋯-Menü |
| 5.2 | Weiter schmaler | Titel bleibt lesbar, Aktionspaare weichen |
| 5.3 | ⋯-Menü öffnen | Drucken, Einstellungen, Liste leeren, Löschen, Bearbeiten, Rückgängig |
| 5.4 | Windows + Pfeil links (halber Bildschirm), Startseite | **Zweispaltig** – das war der Wunsch |
| 5.5 | Pinnwand bei schmalem Fenster | „Raster“, „Finden“, „Fläche“ bleiben |
| 5.6 | Wieder breit ziehen | Alles kommt zurück, nichts bleibt hängen |

## 6. Dialoge (Punkte 10, 11, 20, 27)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 6.1 | Schnellerfassung öffnen | Fensterleiste im Design, Beschreibungsfeld, Kalenderknopf |
| 6.2 | Kalenderknopf drücken, Datum wählen | Datum steht im Feld, Vorschau stimmt |
| 6.3 | Im Beschreibungsfeld Enter | Neue Zeile; Strg+Enter speichert |
| 6.4 | Tab von der Beschreibung aus | Springt weiter, fügt keinen Tabulator ein |
| 6.5 | Punktdetails bei breitem Fenster | Zwei Spalten: links Termine, rechts Inhalt |
| 6.6 | Fenster schmaler ziehen | Eine Spalte, Uhrzeit unter dem Datum, nichts gequetscht |
| 6.7 | Benachrichtigungen öffnen | Hinweistext auf der linken Flucht, „Zeitpunkt (Ortszeit)“ vollständig |
| 6.8 | Spaltentrennlinien im Benachrichtigungsfenster ziehen | Lassen sich ziehen |
| 6.9 | Wiederholung mit Enddatum, Kalenderknopf | Serienende über den Kalender wählbar |

## 7. Tabelle (Punkte 15, 16, 25)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 7.1 | „Spalten …“ in der Tabellenansicht | Fenster mit neun Kästchen – **war leer** |
| 7.2 | Spaltenbreite ziehen, Liste wechseln, zurück | Breite ist erhalten |
| 7.3 | Auf eine Überschrift klicken, dreimal | aufsteigend, absteigend, Listenreihenfolge |
| 7.4 | „Breiten und Sortierung zurücksetzen“ | Standardbreiten zurück |

## 8. Anzeigemodi (Punkte 33, 34)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 8.1 | „Anzeige“ auf „Checklisten“ | Schritte stehen eingerückt unter ihrem Punkt |
| 8.2 | Auf eine Schrittzeile klicken bzw. Leertaste | Der Schritt wird abgehakt, der Punkt bleibt offen |
| 8.3 | „Anzeige“ auf „Erweitert“ | Zusätzlich Anhänge und Beschreibungsanfang |
| 8.4 | „Anzeige“ auf „Kompakt“ | Nur Titel, Termin, Labels |
| 8.5 | Liste mit 200 Punkten in „Erweitert“ | Bleibt flüssig bedienbar |

## 9. Austauschformat (Punkte 36 bis 40)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 9.1 | Datei → Für KI bereitstellen, Umfang „Aktuelle Liste“ | `.glideexchange` entsteht, lesbar im Texteditor |
| 9.2 | Datei ansehen | Keine internen Kennungen (32-stellige Hex-Werte) |
| 9.3 | Datei → KI-Ergebnis importieren, dieselbe Datei | Vorschau zeigt die richtigen Zahlen |
| 9.4 | Importieren, dann Strg+Z | Die angelegten Listen sind wieder weg |
| 9.5 | In der Datei ein Feld erfinden, erneut importieren | Vorschau nennt das Feld, Fokus auf „Abbrechen“ |
| 9.6 | Eine Markdown-Gliederung als `.md` importieren | Wird gelesen, Checklisten erkannt |
| 9.7 | Datei → Austauschformat anzeigen, kopieren | Text in der Zwischenablage |
| 9.8 | Einer KI diesen Text plus ein Dokument geben, Antwort importieren | Struktur entsteht wie beschrieben |

## 10. Navigation und Startseite (Punkte 6, 7, 8, 22, 23)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 10.1 | Seitenleiste ansehen | Startseite, Mein Tag, ⟶ Eingang, In Bearbeitung, ⟶ Verspätet, Labels, Vorlagen, Papierkorb |
| 10.2 | Auf „Eingang“ klicken | Öffnet die Eingangsliste wie bisher |
| 10.3 | „Mein Tag“ öffnen, Pfeile ansehen | ◀ links, ▶ rechts |
| 10.4 | Liste in einem Unterordner öffnen, „Zuklappen“ | Der Pfad dorthin bleibt offen, alles andere schließt |
| 10.5 | Startseite ansehen | Eine Kachel „Heute“ mit „Eingeplant“ und „Heute fällig“ |

## 11. Leistung (Punkt 9)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 11.1 | Großen Bestand laden, zwischen Listen wechseln | Kein spürbares Warten |
| 11.2 | Zwischen „In Bearbeitung“, „Mein Tag“, „Verspätet“ wechseln | Dasselbe |
| 11.3 | Nach einer Änderung sofort die Seitenleiste ansehen | Zähler stimmen – kein veralteter Wert |

## 12. Nach der Prüfung

- Ergebnis in [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md),
  [Weitergabe](Glide_Weitergabe_neuer_Chat_2026-09-18.md) und
  [Technische Fakten](Notizen/Technische_Fakten_3.23.0.md) **derselben**
  Version eintragen.
- Screenshots über `tests/tools/screenshots.py` erzeugen und ansehen; das
  läuft nur auf einer Zielplattform mit ImageMagick.
- Danach die [Abnahme am Gerät](Checklisten/Abnahme_Windows_macOS_3.23.0.md)
  durchgehen: Sie enthält die Blöcke, die hier bewusst fehlen, und die
  Windows-Erstabnahme der seit Längerem unveränderten Funktionen.
