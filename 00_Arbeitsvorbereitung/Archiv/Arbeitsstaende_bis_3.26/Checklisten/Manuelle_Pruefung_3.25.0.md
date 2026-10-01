# Manuelle Prüfung – Glide 3.25.0

Stand: 19.09.2026 · Glide 3.25.0 · Aufgabenformat 16

Die automatisierten Prüfungen sind in einer Linux-Vorabumgebung grün: 30
Suiten – darunter die neue Breitenprüfung, die jede Ansicht in jedem Design in
drei Fensterbreiten aufbaut –, fünf Analysen, Vorlagen- und Releasedaten.
Diese Liste enthält, was **eine Person am Gerät** prüfen muss: alles, was von
Plattform, Eingabegerät oder Augenmaß abhängt. Der maßgebliche Vollprüflauf am
Arbeitsgerät steht ebenfalls noch aus.

**Vorher:** Ein vollständiges App-Backup anlegen (Datei → Sicherung →
Vollständiges App-Backup speichern). 3.25 bringt keinen Formatsprung; die
Einstellungen werden beim ersten Start um die neuen additiven Felder ergänzt.

Was Plattform und Umgebung beantworten – Skalierung, zweiter Monitor,
Ruhezustand, Systemzeitzone, synchronisierter Ordner, Hilfsmittel – steht in
der [Abnahme am Gerät](Abnahme_Windows_macOS_3.23.0.md); sie gilt für 3.25
unverändert weiter.

## 1. Der gemeldete Stillstand (5.2)

Der wichtigste Abschnitt. Die Ursache ist gefunden und behoben; was fehlt, ist
der Nachweis am Gerät.

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 1.1 | Glide normal starten und eine Stunde wie gewohnt arbeiten | Die Kopfleiste bleibt in ihrer Designfarbe; die App nimmt jederzeit Eingaben an |
| 1.2 | Hilfe → Fehlerprotokoll öffnen | Entweder „noch kein Fehler aufgetreten“ oder eine Textdatei mit Zeitstempeln |
| 1.3 | Tritt der Stillstand doch auf: Fehlerprotokoll sichern **bevor** Glide neu gestartet wird | Die Datei `fehlerprotokoll.txt` liegt neben den Daten (Pfad in „Über Glide“) |
| 1.4 | Steht dort ein Eintrag, ihn vollständig weitergeben | Traceback mit Datei und Zeilennummer – damit ist die Stelle bestimmbar |
| 1.5 | Nach dem ersten Fehler einer Sitzung erscheint einmal ein Hinweisfenster | Weitere Fehler derselben Sitzung werden nur noch protokolliert, nicht gemeldet |

**Wenn der Stillstand weiterhin auftritt und das Protokoll leer bleibt**, liegt
die Ursache außerhalb der Ereignisschleife – dann sind Virenschutz,
Ordnersynchronisierung und Grafiktreiber die nächsten Verdächtigen, und die
Uhrzeit des Vorfalls ist die wichtigste Angabe.

## 2. Schaltflächen und Masken (1.1, 1.7, 2.1)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 2.1 | Datei → Exportieren → Drucken und PDF öffnen | „Als HTML speichern“ und „Öffnen und drucken“ stehen vollständig da, nichts ist abgeschnitten |
| 2.2 | Einstellungen → Darstellung → Schriftgröße auf „groß“ und Dialog erneut öffnen | Die Flächen sind breiter geworden; kein Text läuft über den Rand |
| 2.3 | Einstellungen → Persönliches | Die Felder für Tagesziel und Tageskapazität stehen mit ihrer Oberkante auf einer Linie, auch wenn die linke Beschriftung umbricht |
| 2.4 | Einen Punkt per F2 öffnen | Art/Wichtigkeit und Farbe/Zielliste stehen paarweise auf einer Linie; beide Spalten sind gleich breit |
| 2.5 | Dasselbe Fenster schmal ziehen | Unter etwa 950 Pixeln rutschen die Spalten untereinander, statt zu quetschen |
| 2.6 | „Erweitert“ in einer Liste öffnen | Das Fenster öffnet breiter als in 3.24 und zeigt zwei vollständige Spalten |

## 3. „Erweitert“ in abgeleiteten Ansichten (1.2, 1.3)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 3.1 | „Mein Tag“ öffnen, „Erweitert“ drücken | Die Eingabemaske öffnet sich – **kein** Hinweis „Öffne die Aufgabe per Doppelklick“ |
| 3.2 | Im Feld „Bearbeitungstag“ nachsehen | Der betrachtete Tag ist vorbelegt |
| 3.3 | Punkt anlegen, ohne die Zielliste zu ändern | Er erscheint in „Mein Tag“ und in der vorbelegten Liste |
| 3.4 | Dasselbe in „In Bearbeitung“ und „Verspätet“ | Maske öffnet, Hinweistext nennt die Zielliste |
| 3.5 | In „Labels“ eine Labelgruppe anklicken, dann „Erweitert“ | Das Label der Gruppe ist vorbelegt |
| 3.6 | Alle vier Ansichten mit leerem Bestand | Sinnvolle Meldung statt Absturz |

## 4. Abschnitte und nächste Aufgabe (1.5, 1.6, 2.2)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 4.1 | „In Bearbeitung“ mit mindestens drei offenen Punkten öffnen | Ganz oben „▶ Nächste Aufgabe“ mit genau einer Zeile darunter |
| 4.2 | Dieselbe Zeile in den Abschnitten darunter suchen | Sie steht dort **nicht** noch einmal |
| 4.3 | Pfeil vor „Verspätet“ anklicken | Der Abschnitt klappt zu, die Zahl in der Überschrift bleibt |
| 4.4 | Glide beenden und neu starten | Der Abschnitt ist weiterhin zugeklappt |
| 4.5 | „Mein Tag“ mit gefülltem Eingang öffnen, Eingang zuklappen | Die Tagesplanung steht wieder oben im Bild |
| 4.6 | Startseite → Kachel „Nächste Aufgabe“ | Sie nennt dieselbe Aufgabe wie der Abschnitt |
| 4.7 | Dort „Im Abschnitt zeigen“ drücken | „In Bearbeitung“ öffnet sich, die Zeile ist ausgewählt und sichtbar |
| 4.8 | Einen überfälligen Punkt mit hoher Wichtigkeit anlegen | Er wird zur nächsten Aufgabe |

## 5. Anzeigeauswahl und Menüs (1.4, 1.9, 1.10)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 5.1 | In einer Liste „Anzeige“ anklicken | Die Fläche öffnet **unter** der Schaltfläche, rechte Kanten fluchten |
| 5.2 | Die fünf Zeilen lesen | Je eine kurze Zeile, kein ganzer Satz |
| 5.3 | Fenster schmal ziehen, erneut öffnen | Die Fläche bleibt im Fenster und unter ihrem Auslöser |
| 5.4 | Menü „Ansicht“ öffnen | Sechs Gruppen statt einer langen Liste |
| 5.5 | Menü „Datei“ öffnen | Sieben Gruppen; Drucken liegt unter „Exportieren“ |
| 5.6 | Aktionen durchsuchen (Kopfzeile) | Jede Aktion ist weiterhin auffindbar, mit ihrem Pfad |
| 5.7 | F1 drücken | Das Handbuch öffnet sich |
| 5.8 | Im Handbuch „pinnwand“ eintippen | Nur passende Zeilen bleiben stehen |
| 5.9 | Eine Zeile aus dem Handbuch nachschlagen | Der genannte Ort stimmt mit der App überein |

## 6. Arbeitsdateien verschieben (1.8)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 6.1 | Hilfe → Über Glide | Version, Text und der Pfad der Datenablage stehen da |
| 6.2 | Die drei Schaltflächen prüfen | „Arbeitsdateien verschieben …“, „Standardordner benutzen“, „Ordner öffnen“ |
| 6.3 | **Mit Backup:** in einen leeren Cloudordner verschieben | Rückfrage, dann arbeitet Glide dort; der Bestand ist vollständig |
| 6.4 | Glide beenden, neu starten | Der neue Ordner ist weiterhin aktiv |
| 6.5 | Auf einem zweiten Gerät denselben Ordner wählen | Derselbe Bestand; **nicht gleichzeitig öffnen** – die Sperrdatei meldet das |
| 6.6 | „Standardordner benutzen“ | Zurück im Standardordner, nichts verloren |

## 7. Minimaldesigns (1.11)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 7.1 | Einstellungen → Darstellung → „Minimal hell“ | Kein Farbton mehr im Fenster – nur Grau, Schwarz und Weiß |
| 7.2 | Eine Liste mit überfälligen, heute fälligen und erledigten Punkten ansehen | Die drei Zustände sind über die Helligkeit unterscheidbar |
| 7.3 | Dasselbe in „Minimal dunkel“ | Umgekehrte Reihenfolge: je dringender, desto heller |
| 7.4 | Auswahl, Hover und Eingabefelder prüfen | Text bleibt überall gut lesbar |
| 7.5 | Startseite, Pinnwand, Kalender und Einstellungen durchgehen | Nirgends ein farbiger Rest |
| 7.6 | Mit dem Designschalter hell/dunkel wechseln | Wechsel innerhalb der Minimalfamilie, nicht zurück ins Standarddesign |

## 8. Rückmeldung auf jede Aktion (1.12)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 8.1 | Dopamin-Design wählen, eine Liste anlegen | Eine Fahne „Liste angelegt“ |
| 8.2 | Kopieren, einfügen, gruppieren, duplizieren, rückgängig | Jedes Mal eine passende Rückmeldung |
| 8.3 | Zwei Karten auf der Pinnwand verbinden und wieder trennen | „Verbunden“ und „Verbindung gelöst“ |
| 8.4 | Mehrere Punkte auf einmal löschen | „N in den Papierkorb“ mit der richtigen Zahl |
| 8.5 | In ein anderes Design wechseln und dasselbe tun | Nur Erledigtes und erreichte Ziele melden sich |
| 8.6 | Einstellungen → „Wann eine Rückmeldung erscheint“ → „Bei jeder Aktion“ | Auch außerhalb des Dopamin-Designs meldet sich alles |
| 8.7 | „Bewegte Rückmeldung“ ganz abschalten | Nichts meldet sich mehr, in keiner Stufe |
| 8.8 | Beurteilen: Macht es Spaß oder stört es? | Freitextantwort – davon hängt ab, ob die Voreinstellung bleibt |

## 9. Pinnwand (3.1 bis 3.4)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 9.1 | Zwei Karten verbinden, Art „Pfeil vorwärts“ | Die Spitze ist vollständig sichtbar und berührt die Karte nicht |
| 9.2 | Karten dicht nebeneinander schieben | Die Linie bleibt sichtbar, die Spitze schrumpft mit |
| 9.3 | Karten übereinanderschieben | Die Linie verschwindet, statt als Fleck stehen zu bleiben |
| 9.4 | Die Fläche drucken | Die Linien liegen wie auf dem Bildschirm |
| 9.5 | Globale Pinnwand öffnen | Links in der Reiterzeile steht „◂ Übersicht“ |
| 9.6 | Darauf klicken | Zurück in Listen und Ordner |
| 9.7 | Einen Punkt mit langem Titel als Reiter öffnen | Der Reiter ist kurz, am Wortende geschnitten; der Tooltip zeigt den vollen Titel |
| 9.8 | Rechtsklick auf eine Karte | Menü mit den Aktionen dieser Karte, sie ist ausgewählt |
| 9.9 | Rechtsklick auf freie Fläche | Menü mit „Neue Aufgabe hier“ – der Punkt entsteht an der geklickten Stelle |

## 10. Startseite (4.1 bis 4.3)

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 10.1 | Startseite öffnen | Der Schnellzugriff zeigt vier Flächen und „Weitere …“ |
| 10.2 | „Weitere …“ öffnen | Drei Gruppen: Ansichten, Anlegen, Einrichten |
| 10.3 | Fenster schmal ziehen | „Mein Tag“ und „Weitere …“ bleiben stehen |
| 10.4 | Kachel „Pinnwand“ ansehen, während die globale Fläche Karten trägt | Die Vorschau zeigt die echten Positionen und Verbindungslinien |
| 10.5 | Auf die Vorschau klicken | Die globale Pinnwand öffnet sich |
| 10.6 | Karten verschieben, zurück zur Startseite | Die Vorschau ist nachgezogen |
| 10.7 | Ohne Karten | Eine Andeutung aus drei verbundenen Flächen statt eines leeren Rahmens |
| 10.8 | Kachel „Begleiter“ mit überfälligen Punkten | Die Figur sieht besorgt aus; darunter steht, warum |
| 10.9 | Alles Überfällige erledigen, Tagesziel erreichen | Die Figur freut sich |
| 10.10 | Auf die Figur klicken | Sie hüpft und grüßt, danach zurück in ihren Zustand |
| 10.11 | „Benennen …“ und einen Namen vergeben | Der Kacheltitel trägt den Namen; er übersteht den Neustart |
| 10.12 | Die Figur in allen neun Designs ansehen | Überall sichtbar und lesbar, auch in den Minimaldesigns |
| 10.13 | Beurteilen: Trägt die gezeichnete Figur, oder braucht es Bilddateien? | Freitextantwort – davon hängt ab, ob Assets beauftragt werden |

## 11. Vollprüflauf am Gerät

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 11.1 | `python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.25.0/abschluss --timeout 900` | Exitcode 0; 30 Suiten und 5 Analysen grün |
| 11.2 | Die Dokumentprüfung beachten | Sie kann **nur** am Gerät vollständig laufen: Der Index verweist auf rund 400 archivierte Dokumente, die in einer Vorabumgebung nicht vorliegen |
| 11.3 | Screenshots erzeugen und ansehen | Hell und Dunkel, 860 und 1280 Pixel |
| 11.4 | Ergebnis ablegen | `tests/qa-3.25.0/abschluss/ergebnis.json` |

## Was nach der Prüfung zu beantworten ist

1. Ist der Stillstand mit weißer Kopfleiste wieder aufgetreten? Wenn ja: Was
   steht im Fehlerprotokoll?
2. Ist die Rückmeldung auf jede Aktion ein Gewinn oder eine Störung – und soll
   sie außerhalb des Dopamin-Designs die Vorgabe werden?
3. Trägt die gezeichnete Figur, oder sollen Assets nach der Lieferliste in
   `docs/decisions/ARBEITSBEGLEITER.md` beauftragt werden?
4. Sind die beiden Minimaldesigns so brauchbar, oder fehlt ihnen ein
   Akzentton für die Auswahl?
