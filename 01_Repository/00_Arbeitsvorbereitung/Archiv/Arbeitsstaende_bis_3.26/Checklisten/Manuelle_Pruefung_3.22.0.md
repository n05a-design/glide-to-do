# Manuelle Prüfung – Glide 3.22.0

Stand: 17.09.2026 · Glide 3.22.0 · Aufgabenformat 16

Die automatisierten Prüfungen sind grün (26 Suiten, drei Analysen, beide
Reproduktionsabgleiche). Diese Liste enthält, was **eine Person am Gerät**
prüfen muss. Jede Zeile beschreibt eine Handlung und das erwartete Ergebnis.

**Vorher:** Ein vollständiges App-Backup anlegen (Datei → Vollständiges
App-Backup speichern). Der erste Start von 3.22 hebt das Aufgabenformat und
schreibt `backups/liste_vor_format16_<Zeitstempel>.json`; prüfen, dass diese
Datei nach dem ersten Speichern existiert.

## 1. Erster Start und Migration

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 1.1 | Vor dem Wechsel in 3.21 Aufgaben über „Für Mein Tag einplanen“ auswählen, Glide beenden, 3.22 starten | Dieselben Aufgaben stehen in „Mein Tag“ und tragen den heutigen Bearbeitungstag |
| 1.2 | Nach dem ersten Speichern in den Backup-Ordner sehen | `liste_vor_format16_*.json` vorhanden, Inhalt unverändert Format 15 |
| 1.3 | `settings.json` ansehen | `today_plan_migrated: true`, kein `today_plan` mehr |
| 1.4 | Ein Aufgabenbackup aus 3.21 laden | Lädt ohne Meldung; alle Punkte haben eine leere Checkliste |

## 2. Mein Tag

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 2.1 | Seitenleiste ansehen | Genau eine Tageszeile „Mein Tag“, keine zweite „Tagesplanung“ |
| 2.2 | „◀“ und „▶“ drücken | Titel und Zähler wechseln den Tag; „heute“ steht nur beim heutigen |
| 2.3 | Im Eingang eine Aufgabe ohne Termin anlegen, dann „Mein Tag“ öffnen | Sie steht unten im Block „Eingang · n ohne Bearbeitungstag“ |
| 2.4 | Rechtsklick darauf → „Auf … einplanen“ | Sie wandert nach oben in den Tag; der Block schrumpft |
| 2.5 | Über Mitternacht offen lassen oder Systemdatum vorstellen | Die Planung des Vortags bleibt an ihrem Tag; „heute“ ist leer, nicht verloren |

## 3. Checkliste

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 3.1 | Punktdetails öffnen, drei Schritte mit Enter anlegen | Stand rechts oben zählt mit; Liste zeigt ☐/✓ |
| 3.2 | Einen Schritt abhaken, speichern | Zeile im Baum zeigt `☑ 1/3` |
| 3.3 | Art auf „Gruppe“ stellen | Der Checklistenabschnitt verschwindet; nach Zurückstellen ist er wieder zwischen Beschreibung und Anhängen |
| 3.4 | 51 Schritte versuchen | Meldung ab dem 51.; die ersten 50 bleiben |
| 3.5 | Liste als Markdown exportieren und als PDF drucken | Kästchenliste im Markdown, „Checkliste: 1 von 3“ im Druck |

## 4. Tabelle

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 4.1 | Tabelle öffnen | Überschriften stehen links über ihren Werten |
| 4.2 | Auf „Fälligkeit“ klicken, dreimal | aufsteigend ▲ → absteigend ▼ → Listenreihenfolge ohne Pfeil; Zeilen ohne Termin bleiben in beiden Richtungen unten |
| 4.3 | Eine Trennlinie ziehen, Liste wechseln, zurückwechseln | Die Breite steht noch |
| 4.4 | „Spalten …“ → „Breiten und Sortierung zurücksetzen“ | Standardbreiten, keine Sortierung |
| 4.5 | In der Tabelle den Schalter rechts ansehen | Er heißt „Liste“ und führt zurück |

## 5. Filterzeile

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 5.1 | Rechte Kante von „Pinnwand“ mit der Kante von „Hinzufügen“ darüber vergleichen | Beide enden auf derselben Linie |
| 5.2 | Abstände zwischen „Suche löschen“, „Tabelle“ und „Pinnwand“ ansehen | Gleichmäßig, kein Nullabstand |
| 5.3 | Startseite öffnen | „Gespeicherte Filter“ steht nicht mehr in der Seitenleiste; „Ansicht → Gespeicherte Filter …“ öffnet den Manager |

## 6. Pinnwand

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 6.1 | Pinnwand öffnen | Raster, Vorschau, Auto und Finden stehen oben neben „Liste · Pinnwand“; keine Zeile „n von m Karten“ |
| 6.2 | Eine Karte ziehen | **Kein Flackern.** Die Karte selbst folgt dem Zeiger; beim Loslassen springt die Ansicht nicht |
| 6.3 | Eine Aufgabe ohne Beschreibung, Labels und Termin anheften | Ihre Karte ist deutlich niedriger als eine vollständig gefüllte |
| 6.4 | Ein PNG an eine Aufgabe hängen | Die Karte zeigt es verkleinert; „Vorschau“ blendet es aus |
| 6.5 | „Auto“ einschalten, neue Aufgabe in der Liste anlegen | Sie erscheint ohne weiteres Zutun als Karte |
| 6.6 | Eine Karte weit nach rechts unten ziehen, dann „Finden“ | Alle Karten stehen wieder im Bild; die Betriebsart bleibt „Frei anordnen“ |
| 6.7 | Waagerechte Bildlaufleiste ansehen | Gerundet und im Theme, nicht im Systemstil |

## 7. Maus und Tastatur

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 7.1 | Mausrad gedrückt halten und ziehen – im Aufgabenbaum, in der Seitenleiste, auf der Startseite, auf der Pinnwand | Der Inhalt folgt; der Zeiger wechselt zur Hand; **kein Kontextmenü** |
| 7.2 | Shift halten und scrollen – Pinnwand und Tabelle | Der Inhalt schiebt sich quer |
| 7.3 | Rechtsklick an denselben Stellen | Kontextmenü wie gewohnt |
| 7.4 | *Nur macOS:* dieselben Schritte | Knopf 2 öffnet weiterhin das Kontextmenü; kein Ziehen |

## 8. Startseite

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 8.1 | Fenster von schmal auf breit ziehen | Eine, zwei, drei Spalten; kein Flackern zwischen den Schwellen |
| 8.2 | „Startseite einrichten …“, Kacheln ein- und ausschalten, ordnen | Die Startseite folgt; Neustart behält die Wahl |
| 8.3 | Alle Kacheln ausschalten | Hinweis mit Schaltfläche „Startseite einrichten …“ statt leerer Seite |
| 8.4 | Kachel „Fokus“ einschalten | Nennt eine konkrete Aufgabe oder bleibt leer – erfindet nichts |

## 9. Farbmodi

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 9.1 | Einstellungen → Farbmodus „Kontrast“ | Text deutlich kräftiger; Linien sichtbar; Glaskanten aus |
| 9.2 | Mit Rot-Grün-Simulation (z. B. Windows-Farbfilter „Deuteranopie“) prüfen | Erledigt, Verspätet und Wichtigkeit bleiben unterscheidbar – notfalls über Zeichen und Text |
| 9.3 | Farbmodus „Dopamin“ | Dunkler Grund, kräftige Farben; beim Abhaken kurze Rückmeldung; beim Erreichen des Tagesziels eigener Text |
| 9.4 | Zurück auf „Standard“ | Alles wie vor dem Wechsel, Glaskanten wieder nach Einstellung |
| 9.5 | Beide Modi mit Hell und mit Dunkel kombinieren | Vier lesbare Kombinationen |

## 10. Abschluss

| Nr. | Handlung | Erwartet |
| --- | --- | --- |
| 10.1 | `python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.22.0/abschluss` auf der Zielplattform | Exitcode 0; übersprungen bleiben nur Screenshots und Sichtprüfung |
| 10.2 | Screenshots ansehen | Keine abgeschnittenen Beschriftungen, keine überlappenden Schaltflächen |
| 10.3 | Ergebnis in `docs/07_QA_BERICHT.md` eintragen | Plattform, Python-Version, Datum, Uhrzeit, Exitcode, Schrittzahl |
