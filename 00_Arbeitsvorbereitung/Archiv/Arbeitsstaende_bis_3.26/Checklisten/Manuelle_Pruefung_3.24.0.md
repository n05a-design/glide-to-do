# Manuelle Prüfung – Glide 3.24.0

Stand: 19.09.2026 · Glide 3.24.0 · Aufgabenformat 16

Die automatisierten Prüfungen sind in einer Linux-Vorabumgebung grün: 28
Suiten, die Analysen, Vorlagen- und Releasedaten. Diese Liste enthält, was
**eine Person am Gerät** prüfen muss – alles, was von Plattform, Eingabegerät
oder Augenmaß abhängt. Der maßgebliche Vollprüflauf am Arbeitsgerät steht
ebenfalls noch aus.

**Vorher:** Ein vollständiges App-Backup anlegen (Datei → Vollständiges
App-Backup speichern). 3.24 bringt keinen Formatsprung; die Einstellungen
werden beim ersten Start um die neuen additiven Felder ergänzt.

Was Plattform und Umgebung beantworten – Skalierung, zweiter Monitor,
Ruhezustand, Systemzeitzone, synchronisierter Ordner, Hilfsmittel – steht in
der [Abnahme am Gerät](Abnahme_Windows_macOS_3.23.0.md); sie gilt für 3.24
unverändert weiter.

## 1. Seitenleiste und Abschnitte (Punkte 1, 2)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 1.1 | Glide starten | Der Systembereich zeigt genau sechs Zeilen: Startseite, Mein Tag, In Bearbeitung, Labels, Vorlagen, Papierkorb |
| 1.2 | „Mein Tag“ öffnen, wenn Punkte ohne Bearbeitungstag im Eingang liegen | Unten steht der Abschnitt „Eingang · N ohne Bearbeitungstag“ |
| 1.3 | Doppelklick auf diese Überschrift | Der Eingang öffnet sich als Liste |
| 1.4 | „In Bearbeitung“ mit mindestens einem überfälligen Punkt öffnen | Oben „Verspätet · N überfällig“, darunter „Noch offen · N“ |
| 1.5 | Doppelklick auf „Verspätet“ | Die Ansicht „Verspätet“ öffnet sich |
| 1.6 | Alles Überfällige erledigen, Ansicht neu aufbauen | Die Abschnittsüberschriften verschwinden, die Liste ist flach |
| 1.7 | Aktionen durchsuchen nach „Eingang“ und „Verspätet“ | Beide stehen in der Gruppe „Ansichten“ |

## 2. Kopfzeile (Punkt 3)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 2.1 | Fenster breit ziehen | Zahnrad, „Hinzufügen“ und „Anzeige“ enden auf derselben senkrechten Kante |
| 2.2 | Fenster schmal ziehen und wieder breit | Die Flucht stimmt weiterhin – auch nach dem Stufenwechsel |
| 2.3 | Fenster unter 900 Pixel ziehen | Drucken und Einstellungen wandern ins Überlaufmenü, das dann außen steht |

## 3. Pinnwand mit der Maus (Punkte 4, 9, 10)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 3.1 | Drei Karten anheften, erste anklicken, zweite und dritte mit Strg (macOS: Cmd) dazu | Alle drei tragen einen Rahmen, die erste einen stärkeren |
| 3.2 | Dieselbe Karte noch einmal mit Strg anklicken | Sie fällt aus der Auswahl |
| 3.3 | Auf die freie Fläche klicken | Die Auswahl ist aufgehoben |
| 3.4 | Mit drei ausgewählten Karten „Verbinden …“ | Zwei Linien: von der ersten zu den beiden anderen |
| 3.5 | Verbindungsart auf „Pfeil vorwärts“ stellen, zwei Karten verbinden | Die Spitze zeigt von der zuerst gewählten Karte weg |
| 3.6 | Karte verschieben | Die Linie wandert mit, die Spitze bleibt an derselben Seite |
| 3.7 | „Drucken und PDF …“ | Die Pfeilspitzen erscheinen auch auf dem Papier |
| 3.8 | Kartengröße „Groß“ und „Klein“ setzen | Breite und Titelgröße folgen sichtbar; in der geordneten Anordnung bleibt das Raster intakt |
| 3.9 | Mehrere Karten auswählen, „Erledigt umschalten“ | Alle ausgewählten Punkte wechseln den Zustand |

## 4. Anlegen, Vollbild, Gruppen (Punkte 5, 6, 7, 11)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 4.1 | Doppelklick auf die freie Fläche | Die vollständige Punktmaske öffnet sich, nicht eine Textzeile |
| 4.2 | Dort Beschreibung, Label und Anhang setzen, anlegen | Die Karte trägt die Angaben; der Punkt steht auch in der Liste |
| 4.3 | Dasselbe auf einer Ordnerpinnwand | Die Maske fragt zusätzlich nach der Zielliste |
| 4.4 | „Vollbild“ einschalten | Der Schalter ist gefüllt und heißt „Vollbild beenden“ |
| 4.5 | Mit Escape oder F11 zurück | Kopfzeile, Eingabezeile, Suchzeile und Aktionsreihen stehen wieder **oben**, in der alten Reihenfolge |
| 4.6 | „Weitere Aktionen …“ öffnen | Drei Gruppen: Inhalt, Ausgewählte Karte, Fläche |
| 4.7 | Fenster auf 860 × 700 stellen, Pinnwand öffnen | Die Fläche selbst bleibt sichtbar nutzbar |

## 5. Globale Pinnwand und Portabilität (Punkte 8, 12)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 5.1 | Listen- und Ordnerübersicht öffnen, „Globale Pinnwand“ | Die Fläche öffnet sich, der Titel lautet „Globale Pinnwand“ |
| 5.2 | Punkte aus verschiedenen Listen anheften | Alle erscheinen; die Fußzeile nennt ihre Herkunft |
| 5.3 | Escape | Zurück in die Listen- und Ordnerübersicht |
| 5.4 | Karten anordnen, verbinden, Komplettbackup speichern, Glide neu starten, Backup laden | Anordnung und Verbindungen stehen unverändert |
| 5.5 | Dasselbe Backup über „Listen/Ordner hinzufügen …“ in einen anderen Bestand laden | Die Listenpinnwände kommen mit; die globale Fläche des Gebers wird bewusst nicht übernommen |

## 6. Anzeige, Startansicht, Fensterbreiten (Punkte 13, 14, 20)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 6.1 | „Anzeige“ anklicken | Eine Fläche in App-Farben mit Name, Erklärung und Haken – kein Systemmenü |
| 6.2 | Mit Pfeiltasten und Return wählen, mit Escape schließen | Beides funktioniert, die Wahl greift sofort |
| 6.3 | Einstellungen → Ansicht beim Öffnen → „Eine feste Liste“ | Die Listenauswahl erscheint darunter |
| 6.4 | Glide neu starten | Die gewählte Liste steht offen |
| 6.5 | Gewählte Liste löschen, neu starten | Die Startseite erscheint statt einer leeren Ansicht |
| 6.6 | Punktmaske öffnen (F2 oder „Erweitert“) | Zwei Spalten mit Luft; keine umgebrochenen Beschriftungen, keine zweizeiligen Datumsfelder |

## 7. Einstellungen und Rückmeldung (Punkte 15–19)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 7.1 | Einstellungen öffnen | Tagesziel und Tageskapazität stehen nebeneinander |
| 7.2 | Im Design „Liquid Glass · dunkel“ eine Aufgabe abhaken | Eine Fahne erscheint und löst sich auf |
| 7.3 | „Bewegte Rückmeldung“ abschalten, abhaken | Keine Fahne |
| 7.4 | Design „Dopamin“, mehrere Aufgaben schnell hintereinander abhaken | Mehrere Fahnen gleichzeitig, versetzt, in wechselnden Farben; ab der zweiten Erledigung ein Kombo-Zähler |
| 7.5 | Dopamin-Design ansehen | Flächen dunkler, Farben kräftiger; Text bleibt überall gut lesbar |
| 7.6 | Startseite einrichten → alle vier neuen Kacheln einschalten | Kalendervorschau, Verspätet, Fortschritt und Pinnwände erscheinen |
| 7.7 | Kalendervorschau auf Monat, Woche, Nächste Termine stellen | Jede Darstellung baut vollständig auf; heute ist hervorgehoben |
| 7.8 | Ausführlichkeit auf „Kompakt“ | Die Kacheln zeigen weniger Zeilen |

## 8. Bestandsschutz

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 8.1 | Eine Pinnwand aus 3.23 öffnen | Karten und Verbindungen stehen; die Verbindungen sind Linien ohne Spitze |
| 8.2 | Einstellungsdatei nach dem ersten Start ansehen | `theme`, `color_mode` und `glass_mode` stehen weiterhin abgeleitet darin |
| 8.3 | Ein Komplettbackup aus 3.23 laden | Lädt ohne Meldung; die Pinnwände bleiben die des eigenen Geräts |
