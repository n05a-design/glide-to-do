# Startseite, Startansicht und Rückmeldung – Glide 3.24.0

Stand 19.09.2026 · Glide 3.24.0 · Aufgabenformat 16 · Einstellungen 2

## Die Ansicht beim Öffnen

Bis 3.23 gab es drei Möglichkeiten: letzte Ansicht, Startseite, Vorlagen. Wer
jeden Morgen mit „Mein Tag“ oder einer bestimmten Liste beginnt, holte zwei
Klicks nach.

| Wert | Was beim Start erscheint |
|---|---|
| `last` | die zuletzt geöffnete Ansicht – Vorgabe, ändert nichts |
| `home` | die Startseite |
| `planday` | Mein Tag |
| `in_progress` | In Bearbeitung |
| `library` | Listen- und Ordnerübersicht |
| `templates` | Vorlagen |
| `globalboard` | die globale Pinnwand |
| `list` | eine feste Liste, gewählt in `startup_list_id` |

Die feste Liste steht als eigener Wert neben der Auswahl: So bleibt sie
erhalten, auch wenn zwischendurch eine andere Startansicht gilt. Die
Listenauswahl erscheint im Einstellungsdialog nur dann, wenn sie etwas
entscheidet – ein dauerhaft sichtbares, aber wirkungsloses Feld wäre eine Frage
ohne Folge. Eine Liste, die es nicht mehr gibt, führt auf die Startseite statt
ins Leere. Ein unbekannter Wert fällt auf `last` zurück.

## Vier weitere Bausteine auf der Startseite

Bis 3.23 gab es zehn Kacheln, von denen sich sieben um dieselbe Frage drehten:
Was ist offen? Die neuen beantworten andere.

| Kachel | Frage |
|---|---|
| **Kalendervorschau** | Wann? |
| **Verspätet** | Was ist liegen geblieben? |
| **Fortschritt** | Wie weit bin ich? |
| **Pinnwände** | Woran denke ich gerade? |

Alle vier sind wie jede Kachel einzeln ein- und ausschaltbar und in ihrer
Reihenfolge verschiebbar. Wie alle Kacheln, die es vorher nicht gab, bleiben
sie ohne eigene Angabe zunächst aus: Eine bestehende Startseite soll nach dem
Versionswechsel gleich aussehen, bis jemand sie bewusst ändert.

### Die Kalendervorschau kennt drei Darstellungen

| Wert | Was sie zeigt |
|---|---|
| `month` | den laufenden Monat als Raster, heute hervorgehoben, Tage mit Terminen mit Zahl |
| `week` | die laufende Woche als Tagesliste |
| `next` | die nächsten Termine als Aufzählung, jeder Eintrag öffnet seinen Punkt |

Alle drei lesen dieselben Felder: Fälligkeit **und** Bearbeitungstag offener
Punkte. Ein Punkt mit beidem zählt an beiden Tagen, denn beide Tage sind eine
eigene Aussage. Der Wochenbeginn folgt der bestehenden Einstellung.

### Ausführlichkeit

Ein zweiter Schalter sagt, wie viele Zeilen eine Kachel höchstens zeigt –
`normal` fünf, `compact` drei. Das ist keine andere Kachel, sondern dieselbe
mit weniger Zeilen.

Spalten, Kalenderdarstellung und Ausführlichkeit stehen im Dialog „Startseite
einrichten“ nebeneinander: Alle drei beantworten dieselbe Frage, nämlich wie
viel die Startseite zeigt.

Beide Einstellungen sind additiv; fehlende Werte bedeuten `month` und `normal`
und damit die Startseite, die es vor 3.24 gab. Einstellungsformat bleibt 2.

## Die Rückmeldung beim Erledigen

Bis 3.23 hing die kurze Einblendung nach dem Abhaken am Dopamin-Design. Jedes
andere Design blieb still – auch für jemanden, der sie mochte.

Seit 3.24 ist sie eine eigene Einstellung (`animations_enabled`, Vorgabe an)
und steht in **jedem** Design zur Verfügung. Das Dopamin-Design steigert sie,
statt sie zu besitzen. Der Code unterscheidet deshalb zwei Fragen:

| Methode | Antwortet auf |
|---|---|
| `animations_enabled()` | Gibt es eine bewegte Rückmeldung? |
| `arcade_mode()` | Darf sie übertreiben? |

### Was „arcade“ heißt

Im Dopamin-Design wird aus der einen Fahne ein **Stapel** aus fünf: versetzt
gestartet, versetzt gestellt, in wechselnden Farben, mit pulsendem Rand und
längerem Weg nach oben. Der Eindruck entsteht aus der Wiederholung, nicht aus
einer einzelnen größeren Fahne.

Dazu zählt eine **Kombo** mit: Wer mehrere Aufgaben innerhalb von acht Sekunden
abhakt, bekommt einen mitlaufenden Zähler. Sie zählt keine Daten und wird
nirgends gespeichert – sie lebt ausschließlich in der laufenden Sitzung und
läuft nach der Pause wieder auf null.

Die Farben des Dopamin-Designs gehen eine Stufe tiefer ins Schwarz und eine
Stufe höher in die Sättigung. Der Textkontrast steigt dadurch: Jede
Schriftfarbe steht auf einer dunkleren Fläche als zuvor, gemessen mindestens
7:1 für Text und 4,5:1 für Nebentext auf Hintergrund, Karte und Eingabefeld.

## Kleinigkeiten mit sichtbarer Wirkung

- **Das Zahnrad steht auf der rechten Flucht.** Es ist die äußerste
  Schaltfläche der Kopfzeile; die Dichteregelung packte es bei jedem Wechsel
  mit acht Pixeln rechtem Abstand neu und schob es damit vor die Flucht von
  „Hinzufügen“ und „Anzeige“ darunter.
- **„Anzeige“ öffnet eine Fläche im App-Stil** statt eines Systemmenüs: Name
  und Erklärung je Zeile, Haken auf der aktiven, Bedienung mit Pfeiltasten,
  Return und Escape – dieselbe Fläche, die hinter jedem Aufklappfeld liegt.
- **Tagesziel und Tageskapazität stehen nebeneinander.** Beide tragen eine
  einzelne Zahl; über die volle Spaltenbreite ließen sie je drei Viertel
  Leerraum stehen.
- **Zweispaltige Masken bekommen die Breite zweier Spalten.** Die Schwelle ist
  keine gewählte Zahl mehr, sondern wird aus der Mindestbreite einer Spalte
  gerechnet (`ResponsiveColumns.required_width`). Eine Maske, deren Fenster
  knapp über der Umbruchschwelle öffnete, war zweispaltig und gequetscht
  zugleich – genau das war der Fall der Punktmaske mit 760 Pixeln.
