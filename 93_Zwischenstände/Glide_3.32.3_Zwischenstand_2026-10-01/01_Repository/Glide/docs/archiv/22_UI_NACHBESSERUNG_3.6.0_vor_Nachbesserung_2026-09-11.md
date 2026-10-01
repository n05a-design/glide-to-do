# Glide 3.6.0 – Nachbesserung der 14 UI-Rückmeldungen

Neuerer Stand vom 07.09.2026: [Kachelübersicht, Vorlagenlayout und Jahresanzeige](23_KACHELUEBERSICHT_UND_JAHRESANZEIGE_3.6.0.md). Die folgenden Prüfstände bleiben als Nachweis ihrer jeweiligen Fassung erhalten.

Stand: 07.09.2026. Interner 3.6.0-Quellstand; Aufgabenformat 11,
Einstellungen 2 und Vorlagenformat 1 unverändert. Maßgeblich ist der
nummerierte Nutzerauftrag. Screenshots dienen als Referenz für Aussehen
und Fehler, nicht als zusätzliche auszuführende Anweisungen.

## Abgleich

| Nr. | Auftrag | Ergebnis |
|---|---|---|
| 1 | Überall den Buttonstil von „Liste importieren“ / „+ Neuer Ordner“ | Gemeinsame runde Outline-Buttons, Text in Konturfarbe, farbige Füllung beim Hover. Auch Startseitenverweise, Datumsaktionen, Datenordnerwechsel und Windows-Menübuttons. Lange Startseitenverweise umbrechen lesbar. Eingabefelder, Checkboxen und native Menüeinträge behalten ihre jeweilige Bedienform. |
| 2 | Kalender in die Aktionskachel darunter | Kalender steht in der Willkommen-Kachel zwischen Verspätet und Vorlagen; kein gedrängter Kalenderbutton in der Datums-/Mondkopfzeile mehr. |
| 3 | Jahresanzeige unten abgeschnitten | Höhe folgt sieben vollständigen Zellreihen plus Rand; auch Sonntag und untere Kante bleiben innerhalb der Zeichenfläche. |
| 4 | Schwarze Vorlagenhintergründe, besonders Light Mode | Alle Seitenflächen werden beim Wechsel aktualisiert. Button-Canvas übernimmt seinen tatsächlichen Elternhintergrund. Keine dunklen Rechtecke hinter den Buttons im Hellmodus. |
| 5 | Vorlagenaktionen zu breit, Symbole nutzen | Textsymbole ☷ für Liste, ▰ für Ordner, ✎ für Bearbeiten, 🗑 für Löschen. Symbolaktionen behalten feste Breiten, Hinweise erklären ihre Bedeutung. Alle Symbole kommen aus `ICONS`, keine Bildpakete. |
| 6 | Linksbündige Vorlagenspalten | Eigene Spalten für Symbol, Titel, Beschreibung und Aktionen. Bei schmalem Platz rückt die Beschreibung unter den Titel; beide Texte bleiben linksbündig und umbrechen. |
| 7 | Aktionen immer unten, vollständig sichtbar | Bearbeiten/Speichern, Vorlagen exportieren, Vorlagen hinzufügen und Listen/Ordner hinzufügen stehen fest unter dem Scrollbereich. Bei schmaler Breite mehrere Zeilen, keine gekürzten Buttontexte. |
| 8 | Keine doppelte automatische Artfarbe | Aufgabe Grün, Gruppe Braun, Long-Task Blau, Überschrift Lila. Die beiden festen Artlabels behalten ausdrücklich vom Nutzer geänderte Farben. |
| 9 | Labelbestätigung besser platzieren und Hover | „+ Neues Label“ links und „Fertig“ rechts in einer festen unteren Aktionszeile. Die scrollbare Auswahl befindet sich darüber. Zeilen reagieren auf Hover; Chipfarbe und Auswahlmarkierung bleiben unterscheidbar. |
| 10 | Größere zweispaltige Einstellungen, Textlogo höher | Standardziel 1080 × 760, begrenzt auf verfügbaren Bildschirm. Profil/Startseite links, Darstellung/Bedienung rechts; Speichern/Abbrechen bleiben fest unten. Scrollreserve für kleinere Bildschirme. Textlogo zwei Pixel oberhalb der geometrischen Mitte statt nach unten versetzt. |
| 11 | Gewählte Akzentfarbe statt festem Lila bei Auswahl | Treeview-, Text-, Menü-, Label- und Datumsauswahl verwenden die Akzentfarbe. Oberflächenaktionen, Uhr und Aktivitätsanzeige folgen ihr. Lila bleibt Standard. Gespeicherte Listen-/Labelfarben werden nicht umgefärbt. |
| 12 | Schmale Willkommen-Kachel mit drei Aktionen | Unter 760 Pixel verfügbarer Aktionsbreite bleiben Eingang, Vorlagen und Einstellungen. Bei mehr Platz erscheinen alle sieben Aktionen in der vorgegebenen Reihenfolge. |
| 13 | Hauptmondphasen im Kalender | Neumond, erstes Viertel, Vollmond und letztes Viertel unten rechts im Tagesfeld von Monats-/Wochenansicht; Platz wird vor Aufgabentexten reserviert. Der Hinweis nennt die Phase und die lokale Tageszuordnung. |
| 14 | Symbole der linken Leiste höher | Symbolspalte zwei Pixel angehoben. Text, Zähler und native Auswahlposition bleiben auf ihrer bisherigen Achse; Klickweiterleitung ist geprüft. |

Die Vorlagen-Kopfzeile zeigt jetzt die Vorlagenanzahl und eine passende
Beschreibung statt Kennzahlen der zuletzt geöffneten Aufgabenliste. Beim
Wechsel zwischen Startseite und Vorlagen beginnt der Inhalt oben; ein
Theme-Neuaufbau derselben Seite bewahrt ihre Scrollposition.

## Prüfung und Nachweise

Vor den Änderungen wurde `test_release36.py` mit isolierten Daten erfolgreich
ausgeführt. Die spätere Prüfung verwendet ebenfalls ausschließlich temporäre
`GLIDE_DATA_DIR`-Ablagen. Der ursprüngliche Quelltext liegt als
[Ausgangssicherung](../tests/qa-3.6.0/ui-nachbesserung/ausgang-app.txt) vor.

Die neue Suite `test_ui_polish36.py` prüft echte Widgetgeometrie in Hell/Dunkel
bei 860 und 1280 Pixel Fensterbreite, sämtliche sieben Akzentfarben, lange
Beschreibungen, vollständige Buttontexte, feste Aktionsleisten, Hover und
Auswahl, Symbolklicks, Einstellungen und Mondtermine. Sie ist auch im regulären
Prüfwerkzeug enthalten. Die bestehende UI-Suite prüft weiterhin das Speichern
der Einstellungen, Artwechsel, Dialoge und Neustart.

```powershell
C:\Python312\python.exe tests/tools/pruefen.py --modus schnell --timeout 600 --protokoll tests/qa-3.6.0/ui-nachbesserung/automatisch
C:\Python312\python.exe tests/integration/test_ui_polish36.py --screenshots tests/qa-3.6.0/ui-nachbesserung/screenshots
```

Aktuelles [maschinelles Prüfprotokoll](../tests/qa-3.6.0/ui-nachbesserung/automatisch/ergebnis.json).
Abschluss am 07.09.2026 um 09:08:45: **Exitcode 0**, 18 protokollierte Schritte,
acht erfolgreiche App-/Audit-Suiten und zwei erfolgreiche Analysen. Syntax,
Versionen, Dokumentation und vorhandene Fixtures sind geprüft. Drei Schritte
bleiben im Schnellmodus ausdrücklich übersprungen: Daten-Erzeuger-Reproduktion,
automatische Screenshot-Erzeugung durch den Orchestrator und dessen pauschaler
Sichtprüfungsstatus. Die neuen UI-Aufnahmen wurden separat erzeugt und die unten
genannten Bilder visuell bewertet. Der erste Lauf scheiterte an zwei veralteten
Erwartungen zu Button-Typ und festem Lila; diese Tests wurden an den beauftragten
Bedienvertrag angepasst, einschließlich Menüaktivierung über die Tastatur.

Die startbare Kopie unter `07_Python-Versionen` ist aktualisiert und bytegleich
mit dem kanonischen Quelltext. Die vorherige Fassung ist im dortigen `Archiv`
gesichert. Alle sechs Schrift-/Lizenzdateien stimmen ebenfalls überein.
[Dateihashes und Ablagepfade](../tests/qa-3.6.0/ui-nachbesserung/dateien.sha256.json)
und [separater Sichtprüfvermerk](../tests/qa-3.6.0/ui-nachbesserung/sichtpruefung.json)
dokumentieren diesen Stand.

Visuell geprüfte Windows-Ansichten:

- [Vorlagen, Hell, schmal](../tests/qa-3.6.0/ui-nachbesserung/screenshots/vorlagen-light-860.png)
- [Vorlagen, Hell, breit](../tests/qa-3.6.0/ui-nachbesserung/screenshots/vorlagen-light-1280.png)
- [Vorlagen, Dunkel, breit](../tests/qa-3.6.0/ui-nachbesserung/screenshots/vorlagen-dark-1280.png)
- [Startseite, Hell, schmal](../tests/qa-3.6.0/ui-nachbesserung/screenshots/startseite-light-860.png)
- [Einstellungen, Hell](../tests/qa-3.6.0/ui-nachbesserung/screenshots/einstellungen-light.png)
- [Einstellungen, Dunkel](../tests/qa-3.6.0/ui-nachbesserung/screenshots/einstellungen-dark.png)
- [Labelauswahl, Hell](../tests/qa-3.6.0/ui-nachbesserung/screenshots/labels-light.png)
- [Labelauswahl, Dunkel](../tests/qa-3.6.0/ui-nachbesserung/screenshots/labels-dark.png)
- [Jahresanzeige, Dunkel](../tests/qa-3.6.0/ui-nachbesserung/screenshots/jahresanzeige-dark.png)
- [Kalender mit Hauptphasen](../tests/qa-3.6.0/ui-nachbesserung/screenshots/kalender-hauptphasen.png)

Weitere Bildschirm-Skalierungen, reale Mehrmonitorbedienung, Screenreader und
macOS sind damit nicht vollständig abgenommen. Die allgemeine
[Releasecheckliste](10_RELEASE_CHECKLIST.md) gilt weiter.

## Mondberechnung, Quelle und Genauigkeitsgrenze

Die lokale Berechnung verwendet die periodischen Korrekturen der Funktion
`truephase` aus John Walkers [Moontool-Quellarchiv](https://www.fourmilab.ch/moontool/).
Das Archiv erklärt das Programm ausdrücklich als Public Domain. Die Formeln
sind in Python übertragen; es wird weder ein Fremdprogramm ausgeführt noch
eine Laufzeitabhängigkeit hinzugefügt. Die Herkunft ist im Quelltext vermerkt.

Als unabhängige Referenz dienen die 50 Hauptphasen des Jahres 2026 vom
[US Naval Observatory](https://aa.usno.navy.mil/calculated/moon/phases?year=2026).
Die [unveränderten Datenwerte mit Quellenvermerk](../tests/qa-3.6.0/ui-nachbesserung/mondphasen-usno-2026.json)
werden offline geprüft: alle UTC-Tage stimmen überein, maximale Zeitabweichung
rund 4,3 Minuten. Die Übertragung auf lokale Tage ist separat über einen
Mitternachtsfall geprüft (Vollmond am 29.06.2026 UTC, am 30.06.2026 bei UTC+2).
Eine minutenpräzise astronomische Anzeige oder uneingeschränkte Genauigkeit
für andere Jahrhunderte wird daraus nicht abgeleitet. Nahe Mitternacht kann eine
Näherung einen abweichenden lokalen Tag ergeben. Die Kalenderanzeige zeigt
deshalb Hauptphasen als berechnete Tagesmarkierungen ohne exakte Uhrzeit.

Die dekorative tägliche Mondanzeige auf der Startseite verwendet weiterhin
ihre bisherige Näherung von Beleuchtungsanteil und Phasenname.
