# Glide 3.6.0 – Kachelübersicht und weiterer UI-Nachtrag

Stand: 07.09.2026. Interner Stand von 3.6.0; Aufgabenformat 11,
Einstellungen 2 und Vorlagenformat 1 bleiben unverändert. Die folgenden
Änderungen ergänzen die [ersten 14 UI-Nachbesserungen](22_UI_NACHBESSERUNG_3.6.0.md).
Maßgeblich sind die Nutzeraufträge; die Screenshots sind visuelle Referenzen.

## Listen und Ordner als Kacheln

„Listen“ in der linken Seitenleiste trägt nun das zentrale Textsymbol ☷ und
öffnet per Klick, Enter oder Leertaste die Bestandsübersicht im Hauptbereich.
Die aktive Überschrift verwendet die eingestellte Auswahlfarbe und reagiert
auf Hover. Der Plusbutton daneben legt weiterhin eine neue Liste an.

Die Übersicht enthält alle normalen Listen und Ordner einschließlich
Unterordnern in der Reihenfolge der Seitenleiste. Der Eingang bleibt die
eigene Systemansicht. Jede Kachel zeigt Symbol und vorhandene Farbe, Titel,
Ordnerpfad, offene und erledigte Aufgaben sowie eine kurze Inhaltsvorschau.
Ordner zeigen die enthaltenen Listen/Unterordner; Listen zeigen bis zu drei
offene Aufgaben, ersatzweise erledigte Aufgaben. Vorhandene Beschreibungen
werden ebenfalls angezeigt. Vorschauen sind bewusst Ausschnitte; der Klick
auf Kachel oder Öffnen-Button führt zum vollständigen Inhalt.

Je nach Breite entstehen eine, zwei oder drei Spalten. Vertikales Scrollen
zeigt den gesamten Bestand. Neue Liste, Neuer Ordner, Liste importieren und
Listen/Ordner hinzufügen stehen in zwei gerundeten Aktionsgruppen fest unten.
Bei schmalem Platz rücken die Gruppen und nötigenfalls ihre Buttons untereinander.
Die Übersicht verändert beim Öffnen keine Aufgaben oder Ordner. Bei der
Starteinstellung „Letzte Ansicht“ wird sie auch nach einem Neustart geöffnet.
Die zuletzt gespeicherte Systemansicht hat dabei Vorrang vor einem älteren
Ordnerverweis in der Aufgabenablage.

## Vorlagen

- Keine zusätzliche Hinweiszeile oberhalb der Vorlagen.
- Keine reservierte leere Spalte für eine unsichtbare Scrollleiste; ohne
  Überlauf nutzen die Kacheln die volle Breite des Hauptbereichs.
- Gerundete Einzelkacheln mit derselben Kontur/Glaskante wie die anderen Kacheln.
- Eine gemeinsame, nach Titelbreite bemessene Namensspalte; die Beschreibung
  folgt unmittelbar daneben und bleibt linksbündig. Bei wenig Platz steht
  sie darunter. Lange Titel und Beschreibungen brechen um.
- Die vier unteren Aktionen sitzen in zwei gerundeten Zwischenflächen wie
  die Aktionspaare in normalen Listen. Alle Texte bleiben vollständig sichtbar.

## Jahresanzeige

Die fehlenden älteren Tage waren ein Anzeigefehler: Der bisherige Ausdruck
`activity_history or completion_history` wechselte nach der ersten erfassten
Bearbeitung vollständig zur neuen Historie. Beim schreibgeschützten Prüfen
der lokalen Einstellungen waren die früheren Erledigungen weiterhin vorhanden.
Es war keine Wiederherstellung und keine Änderung der Nutzerdaten nötig.

Für die Jahresansicht werden beide Historien nun tageweise zusammengeführt.
Pro Tag gilt der größere Zähler: Eine Erledigung ist zugleich eine Bearbeitung
und darf nicht doppelt addiert werden. Ältere Erledigungen bleiben damit als
bekannte Aktivität erhalten; vor Beginn der Bearbeitungshistorie lassen sich
andere, damals nicht erfasste Änderungen nicht nachträglich bestimmen.
Die gespeicherten Historien und die separate Sieben-Tage-Erledigungsanzeige
bleiben unverändert. Raster und Jahreskennzahlen nutzen dieselbe Zusammenführung.

Mo, Do und So stehen mittig neben ihren jeweiligen Zeilen. Die feste Obergrenze
für die Zellgröße entfällt: Das Jahresraster nutzt dieselbe Zeichenbreite wie
die Sieben-Tage-Anzeige. Seine Höhe folgt weiterhin sieben vollständigen Zeilen,
damit die untere Kante bei großen Zellen nicht abgeschnitten wird.

## Prüfung

Vor den Änderungen lief `test_ui_polish36.py` erfolgreich mit temporärem
`GLIDE_DATA_DIR`. Die [Ausgangssicherung](../tests/qa-3.6.0/vorlagen-jahresanzeige/ausgang-app.txt)
und der [Ausgangsnachweis](../tests/qa-3.6.0/vorlagen-jahresanzeige/ausgangspruefung.json)
bleiben erhalten. Echte Nutzerdaten wurden zur Diagnose ausschließlich gelesen.

Die zusätzliche Suite `test_ui_followup36.py` prüft:

- Vorlagen ansehen/bearbeiten in Hell/Dunkel bei 860, 1280 und 1660 Pixel Breite;
  Kachelbreiten, Rundungen, Textabstände, vollständige Aktionsbuttons.
- Zusammenführung alter und neuer Tageswerte, Überschneidungen ohne
  Doppelzählung, Erhaltung der gespeicherten Historien, Diagrammachsen und -breiten.
- Alle Listen und verschachtelten/leeren Ordner, ein bis drei Spalten,
  Scrollen bei festem Aktionsbereich, Klickziele, unveränderte Inhalte und Neustart.

```powershell
C:\Python312\python.exe tests/integration/test_ui_followup36.py --screenshots tests/qa-3.6.0/vorlagen-jahresanzeige/screenshots
C:\Python312\python.exe tests/tools/pruefen.py --modus schnell --timeout 600 --protokoll tests/qa-3.6.0/vorlagen-jahresanzeige/automatisch
```

Der aktuelle Nachtrag ist auch in das reguläre Prüfwerkzeug aufgenommen.
Es umfasst damit neun App-/Audit-Suiten. Die abschließenden maschinellen
Ergebnisse stehen im [Prüfprotokoll](../tests/qa-3.6.0/vorlagen-jahresanzeige/automatisch/ergebnis.json):
Abschluss 07.09.2026, 15:34:30, **Exitcode 0**, neun erfolgreiche Suiten,
zwei Analysen und die Syntax-, Versions-, Dokumentations- und Fixtureprüfungen.
Die drei im Schnellmodus übersprungenen Schritte sind Daten-Erzeuger-Reproduktion,
Screenshot-Erzeugung durch den Orchestrator und dessen pauschaler Sichtprüfstatus.
Die unten verlinkten Bilder wurden separat erzeugt und visuell geprüft.
Frühere QA-Stände bleiben erhalten.

Die startbare Datei unter `07_Python-Versionen` ist bytegleich mit dem
kanonischen Quelltext. Ihre vorherige Fassung liegt im dortigen `Archiv`.
[Dateihashes und Ablagepfade](../tests/qa-3.6.0/vorlagen-jahresanzeige/dateien.sha256.json)
 halten den Abgleich fest. Eine zusätzliche Abschlussprüfung deckt auch den
Neustart und die Höhenreserve beim Ein-/Ausblenden der Scrollleiste ab; diese
Reserve verhindert, dass das gleichzeitig breiter/höher werdende Jahresraster
die Leiste an einer knappen Höhenkante fortlaufend ein- und ausblendet.

Auch diese [zusätzliche Abschlussprüfung](../tests/qa-3.6.0/vorlagen-jahresanzeige/abschluss-nachtrag.json)
ist erfolgreich: 07.09.2026, 15:37:21, Test-Exitcode 0. Der Nachweis enthält
den SHA-256 des abschließend geprüften Quelltexts.

Visuell geprüfte Aufnahmen aus isolierten Testdaten:

- [Listen/Ordner, dunkel, zwei Spalten](../tests/qa-3.6.0/vorlagen-jahresanzeige/screenshots/listen-ordner-dark-1280.png)
- [Listen/Ordner, hell, schmal](../tests/qa-3.6.0/vorlagen-jahresanzeige/screenshots/listen-ordner-light-860.png)
- [Jahresanzeige, dunkel, breit](../tests/qa-3.6.0/vorlagen-jahresanzeige/screenshots/jahresanzeige-dark-1660.png)
- [Vorlagen, hell, schmal und bearbeitbar](../tests/qa-3.6.0/vorlagen-jahresanzeige/screenshots/vorlagen-light-860-bearbeiten.png)
- [Listen/Ordner, hell, drei Spalten](../tests/qa-3.6.0/vorlagen-jahresanzeige/screenshots/listen-ordner-light-1660.png)

Der [Sichtprüfvermerk](../tests/qa-3.6.0/vorlagen-jahresanzeige/sichtpruefung.json)
fasst die visuell kontrollierten Ansichten zusammen.

Die Windows-Tests vermessen echte Tk-Widgets. Die zusätzlichen Testfenster
werden ohne Taskleisteneintrag transparent betrieben; PrintWindow erfasst
ihren eigenen Inhalt. Andere Desktopfenster werden nicht aufgenommen.
Weitere DPI-Skalierungen, Mehrmonitorbedienung und macOS sind damit nicht
vollständig visuell abgenommen.
