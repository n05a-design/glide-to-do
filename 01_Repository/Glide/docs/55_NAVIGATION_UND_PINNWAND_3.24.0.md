# Navigation und Pinnwand – Glide 3.24.0

Stand 19.09.2026 · Glide 3.24.0 · Aufgabenformat 16 · Einstellungen 2

## Zwei Zeilen weniger in der Seitenleiste

3.23 stellte Eingang und „Verspätet“ eingerückt unter die Ansicht, deren
Teilmenge sie sind. Das war richtig gedacht und trotzdem eine Zeile zu viel:
Acht Systemzeilen beantworten sieben Fragen, und zwei davon führten zu einem
Bestand, der ohnehin schon sichtbar war.

Seit 3.24 hat der Systembereich sechs Zeilen – Startseite, Mein Tag, In
Bearbeitung, Labels, Vorlagen, Papierkorb. Die beiden Teilmengen stehen dort,
wo sie gebraucht werden:

| Was | Wo es seit 3.24 steht |
|---|---|
| Eingang | Abschnitt am Ende von „Mein Tag“, überschrieben mit `Eingang · N ohne Bearbeitungstag` |
| Verspätet | Erster Abschnitt von „In Bearbeitung“, überschrieben mit `Verspätet · N überfällig` |

Beide Abschnitte sind Überschriftszeilen ohne eigene Punktzuordnung: Sie
lassen sich nicht auswählen, nicht ziehen und zählen in keiner Statistik mit.
Ein **Doppelklick** auf sie führt dorthin, wofür sie stehen – auf den Eingang
als Liste beziehungsweise in die Ansicht „Verspätet“.

Beide Ziele bleiben außerdem einzeln erreichbar: im Ansichtsmenü, in den
durchsuchbaren App-Aktionen (Gruppe „Ansichten“) und im Schnellzugriff der
Startseite. Die Ansicht „Verspätet“ selbst ist unverändert; nur ihr Weg dorthin
führt nicht mehr über eine eigene Zeile.

Gibt es nichts Überfälliges, entfällt die Abschnittsüberschrift und „In
Bearbeitung“ sieht aus wie vorher. Eine Überschrift ohne Inhalt wäre eine
Frage, die niemand hat.

## Pinnwand: mehrere Karten auswählen

`Strg` (macOS: `Cmd`) und Klick nimmt eine Karte zur Auswahl hinzu oder nimmt
sie wieder heraus. Die Auswahl ist eine **Reihenfolge**, keine Menge: Die
zuerst gewählte Karte ist der Anker und trägt einen stärkeren Rahmen.

Daraus folgt für die Aktionen:

- **Verbinden** bei mehreren ausgewählten Karten verbindet den Anker mit jeder
  weiteren. Das ist der Sternfall und damit die Form, in der eine Hierarchie
  entsteht; eine Kette baut man, indem man die Schritte einzeln verbindet.
- **Erledigt umschalten**, **Kartengröße** und **Von Pinnwand entfernen**
  wirken auf die gesamte Auswahl.
- Ein Klick auf die freie Fläche hebt die Auswahl auf, `Escape` ebenfalls –
  vor allem anderen, was `Escape` sonst tut.

Eine Karte, die gerade weggefiltert ist, fällt aus der Auswahl: Sonst träfe die
nächste Aktion etwas, das niemand sieht.

## Verbindungen haben eine Richtung

Bis 3.23 war eine Verbindung ungerichtet und wurde als sortiertes Paar
gespeichert. Seit 3.24 trägt sie zusätzlich eine **Art**:

| Art | Bedeutung |
|---|---|
| `line` | Linie ohne Richtung – der bisherige Fall und die Vorgabe |
| `forward` | Pfeil von der ersten zur zweiten Karte |
| `backward` | Pfeil von der zweiten zur ersten Karte |
| `both` | Pfeil in beide Richtungen |

Die Art wird gespeichert, nicht die gezeichnete Spitze. Eine Austauschdatei
kann sie deshalb auswerten, ohne eine Zeichenfläche zu haben. Die zuletzt
gewählte Art gilt für die nächste Verbindung dieser Pinnwand und steht als
Aufklappfeld bei den übrigen Flächeneinstellungen.

Zwischen zwei Karten liegt weiterhin **höchstens eine** Verbindung; geprüft
wird das über das ungeordnete Paar. Ein unbekannter Wert fällt beim
Normalisieren auf `line` zurück, die Verbindung selbst bleibt erhalten. Die
Pfeilspitzen erscheinen auch in der Druckausgabe.

## Kartengröße als Hierarchie

Eine Fläche kennt keine Einrückung. Was in einer Liste die Ebene ist, ist hier
die Größe. Jede Karte trägt deshalb einen Maßstab:

| Maßstab | Faktor | Gedacht für |
|---|---|---|
| `large` | 1,30 | Hauptgedanke |
| `normal` | 1,00 | Normalfall und Vorgabe |
| `small` | 0,78 | Randnotiz |

Der Faktor wirkt auf Kartenbreite, Titelgröße und die Stärke des
Akzentstreifens gemeinsam – eine große Karte zeigt mehr Text, nicht mehr Rand.
In der geordneten Ansicht bestimmt die Spaltenbreite die Breite aller Karten;
dort wirkt der Maßstab allein über die Titelgröße, sonst bräche das Raster
auseinander.

Der Maßstab hängt an der **Karte**, nicht am Punkt: Derselbe Punkt kann auf der
Listenpinnwand ein Hauptgedanke und auf der globalen eine Randnotiz sein. Ein
fehlender Wert bedeutet `normal` und damit genau die Karte aus 3.23.

## Neue Punkte entstehen in der vollständigen Maske

Ein Doppelklick auf die freie Fläche öffnete bis 3.23 eine einzeilige Eingabe.
Auf der Karte stehen aber Beschreibung, Labels, Termin, Checkliste und Anhänge
– wer sie anlegt, soll sie gleich eintragen können. Seit 3.24 öffnet sich
dieselbe vollständige Punktmaske wie hinter „Erweitert“ in der Liste.

Auf der Listenpinnwand ist die Zielliste die Liste der Pinnwand. Auf der
Ordner- und der globalen Pinnwand wählt die Maske sie aus, vorbelegt mit der
ersten Liste des Bereichs beziehungsweise mit dem Eingang. Der bisherige Weg
über „Punkte anheften …“ bleibt unverändert.

## Vollbild heißt Vollbild

Der Schalter hieß „Fläche“ – ein Wort, das in derselben Zeile auch die
Arbeitsfläche selbst meinen konnte. Er heißt jetzt **Vollbild** und trägt im
eingeschalteten Zustand dieselbe dauerhafte Füllung wie „Raster“, „Vorschau“
und „Auto“.

Der Rückweg stellt die ausgeblendeten Zeilen wieder an ihrer Stelle her.
`pack_info()` beschreibt Seite, Füllung und Abstände, aber nicht die Stelle in
der Packreihenfolge; ein später wieder gepacktes Widget landet am Ende seines
Elternteils. Genau daran lag es, dass Kopfzeile und Eingabezeile nach der
Rückkehr unter der Liste standen. Gemerkt wird deshalb zusätzlich der erste
nachfolgende Nachbar, der sichtbar bleibt; an ihm richtet sich der Rückweg aus.

## Aktionen in drei Gruppen

Elf gleich aussehende Schaltflächen in einer Reihe sind keine Ordnung, sondern
eine Aufzählung – und sie kosteten bei schmalem Fenster vier Zeilen Höhe, die
der Fläche fehlten.

Sichtbar bleibt, was man beim Arbeiten anfasst: „Punkte anheften …“, „Neue
Aufgabe“, „Bearbeiten“, „Verbinden …“. Alles Übrige steht unter **Weitere
Aktionen …** in drei benannten Gruppen, deren Reihenfolge die Reihenfolge des
Arbeitswegs ist:

1. **Inhalt** – was auf die Fläche kommt
2. **Ausgewählte Karte** – was mit der Auswahl geschieht
3. **Fläche** – wie die Fläche selbst aussieht und was aus ihr herausgeht

Jede Aktion steht in genau einer Gruppe. Anordnung, Labelfilter, Kartenbreite
und Verbindungsart bleiben als Aufklappfelder in einer Zeile darunter, weil man
sie im Blick behalten will, statt sie zu suchen.

## Die globale Pinnwand

Eine Pinnwand über den gesamten Bestand – jede Liste, gleich in welchem Ordner
sie liegt. Sie ist kein zweiter Kartenspeicher, sondern eine Pinnwand wie jede
andere, nur mit einem anderen Bereich: derselbe Bereichsschlüssel-Mechanismus,
dieselben Karten, dieselben Verbindungen, dieselben Einstellungen.

| | |
|---|---|
| Bereichsschlüssel | `global` neben `list:<id>` und `folder:<id>` |
| Ansicht | `globalboard`, eine eigene Ansicht ohne Seitenleistenzeile |
| Erreichbar über | Listen- und Ordnerübersicht, Startseite, Ansichtsmenü, App-Aktionen |
| Zurück mit | `Escape` – in die Listen- und Ordnerübersicht, denn eine Liste gibt es hier nicht |

Neue Punkte entstehen auch hier in einer echten Liste; die Maske fragt, in
welcher. Beim Hinzufügen einer fremden Datei wird die globale Pinnwand des
Gebers **nicht** übernommen: Sonst bliebe offen, welche von beiden gilt.

## Die Anordnung reist mit

Bis 3.23 lagen Kartenpositionen und Verbindungen ausschließlich in den
persönlichen Einstellungen. Sie reisten damit nur im vollständigen App-Backup
mit; ein Komplettbackup und eine exportierte Liste verloren sie.

Seit 3.24 trägt **jedes** Komplettbackup einen Abschnitt `pinboards` neben den
Aufgabenfeldern. Er steht bewusst neben ihnen und nicht in ihnen: Derselbe
Punkt kann auf mehreren Pinnwänden liegen – in seiner Liste, im Ordner darüber
und auf der globalen Fläche – und dort jeweils woanders. Eine Koordinate am
Punkt könnte nur eine davon tragen.

- **Vollständiger Import**: Die Anordnung wird unverändert übernommen; die
  Kennungen bleiben dieselben.
- **Listen/Ordner hinzufügen**: Listen, Ordner und Punkte bekommen neue
  Kennungen. Karten und Verbindungen wandern mit; was sich nicht zuordnen
  lässt, fällt weg, statt auf fremde Objekte zu zeigen.
- Ältere Glide-Fassungen lesen dieselbe Datei weiterhin und übergehen den
  Abschnitt. **Kein Formatsprung**: Aufgabenformat bleibt 16.

Damit lässt sich eine Pinnwand auf einem Gerät bauen, als Backup oder als
exportierte Liste mitnehmen und auf einem anderen Gerät genau an der Stelle
weiterbearbeiten, an der man aufgehört hat.

## Grenzen

- Höchstens 500 Karten und 200 Verbindungen je Pinnwand.
- Eine Verbindung ohne zwei vorhandene Karten wird beim Normalisieren
  verworfen; eine entfernte Karte nimmt ihre Verbindungen mit.
- Die Pinnwandeinstellungen liegen in den persönlichen Einstellungen
  (Einstellungsformat bleibt 2). Im Backup stehen sie zusätzlich – gelesen wird
  beim Import der Backupabschnitt.
