# Pinnwand als Arbeitsfläche – Glide 3.23.0

Stand 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16 · Einstellungen 2

## Stufenplan

Die Pinnwand wird nicht in einem Schritt zum Whiteboard. Der Ausbau ist in
Stufen geteilt, und diese Fassung setzt die erste vollständig um.

| Stufe | Inhalt | Stand |
|---|---|---|
| 1 | Vollbild, Verbindungen, Punkte auf der Fläche anlegen, Druck und PDF | **3.23.0 umgesetzt** |
| 2 | Freies Zeichnen, Zoom, Bereiche (Rahmen) | offen |
| 3 | Übersichtskarte, Präsentationsmodus über Bereiche | offen |
| 4 | Verbindungen mit Bedeutung (Abhängigkeit, Reihenfolge) | offen, eigene Entscheidung nötig |

## Vollbild

Die Fläche teilt sich das Fenster mit Seitenleiste, Kopfzeile, Eingabezeile,
Filterzeile und zwei Aktionsreihen. Wer auf ihr arbeitet, braucht keine davon –
aber jede kostet Höhe, und die Höhe ist genau das, was einer Pinnwand fehlt.

Der Schalter **„Fläche“** in der Reiterzeile blendet sie aus und gibt der
Pinnwand das ganze Fenster. **F11** tut dasselbe.

**Escape arbeitet sich von innen nach außen:**

1. Ist das Verbinden eingeschaltet, bricht es das ab.
2. Ist das Vollbild an, verlässt es das Vollbild.
3. Sonst verlässt es die Pinnwand.

Ohne diese Reihenfolge führte eine einzige Taste je nach Zustand an drei
verschiedene Orte.

**Die Scrollposition bleibt in beide Richtungen erhalten.** Ein Modus, der beim
Betreten und Verlassen an den Anfang springt, ist unbrauchbar für eine Fläche,
auf der man gerade an einer bestimmten Stelle arbeitet.

## Verbindungen

Zwei angeheftete Punkte lassen sich verbinden: Karte auswählen, „Verbinden …“,
dann die zweite Karte anklicken. Ein zweiter Durchgang über dasselbe Paar nimmt
die Verbindung zurück. Ein Klick ins Leere bricht ab; danach ist der Modus
wieder aus – eine Betriebsart, die stillschweigend anbleibt, führt zu Linien,
die niemand wollte.

### Was gespeichert wird

```json
"pinboards": {
  "list:…": {
    "cards": [ { "item_id": "…", "list_id": "…", "x": 320, "y": 180 } ],
    "connections": [ { "from": "…", "to": "…" } ]
  }
}
```

**Gespeichert wird eine Beziehung zwischen zwei Punktkennungen, nicht eine
gezeichnete Linie.** Das ist der entscheidende Unterschied:

- Eine Linie mit festen Koordinaten wäre falsch, sobald eine Karte verschoben
  wird. Die Beziehung wird bei jedem Aufbau neu gezeichnet und stimmt deshalb
  immer – auch nach dem Verschieben, nach einem Filter, nach dem Wechsel in die
  geordnete Ansicht und nach dem Neustart.
- Eine Linie wäre für jede andere Ansicht bedeutungslos. Eine Beziehung lässt
  sich auslesen – von einer späteren Abhängigkeitsansicht ebenso wie von einer
  Austauschdatei.
- Fällt eine Karte weg, verschwindet ihre Verbindung mit. Eine Verbindung
  gehört zu zwei Karten; fehlt eine, hat die Linie kein Ende mehr.

**Ungerichtet.** „A hängt mit B zusammen“ ist dasselbe wie umgekehrt. Eine
verbindliche Reihenfolge wäre eine Aufgabenabhängigkeit und damit eine eigene
Funktion mit eigener Prüfung auf Kreise – nicht etwas, das nebenbei aus einer
gezogenen Linie entsteht. Das bleibt Stufe 4.

Grenze: 200 Verbindungen je Pinnwand. Darüber ist keine Fläche mehr lesbar.

## Punkte auf der Fläche

- **„Neue Aufgabe“** und **„Neue Notiz“** legen einen Punkt an und heften ihn
  an. Eine Notiz ist ein Long-Task – ein mehrzeiliger, textorientierter Punkt.
- **Doppelklick ins Leere** legt an derselben Stelle an. Bis 3.22 öffnete er
  die Auswahl vorhandener Punkte; auf einer Fläche, die zum Denken da ist,
  erwartet man an dieser Stelle etwas Neues. Der bisherige Weg bleibt über
  „Punkte anheften …“.

**Was hier entsteht, ist ein ganz normaler Punkt in der Quellliste.** Das ist
der Unterschied zu einem Whiteboard-Programm: Die Notiz steht anschließend auch
in der Liste, in der Tabelle, im Kalender, im Änderungsverlauf und im Backup.
Es gibt keine zweite Datenhaltung, die auseinanderlaufen könnte.

Auf der Ordnerpinnwand entstehen keine neuen Punkte: Sie gehört zu keiner
Liste, und ein Punkt braucht eine. Der Hinweis sagt das.

## Drucken und PDF

**Gedruckt wird die belegte Fläche, nicht der Bildschirmausschnitt.** Aus den
Kartenpositionen entsteht ein umschließendes Rechteck; dessen linke obere Ecke
ist der Nullpunkt, und das Papierformat folgt seinem Seitenverhältnis. Leerraum
ringsum fällt weg, und eine Fläche, die breiter als hoch ist, wird nicht in ein
Hochformat gezwängt.

Auf der Seite stehen:

- die Karten als positionierte Kästen mit Titel, Frist, Checklistenstand und
  Labels,
- die Verbindungen als SVG-Linien unter den Karten – wie am Bildschirm,
- eine Kopfzeile mit Listenname, Kartenzahl, Verbindungszahl und Zeitpunkt.

Der Weg ist derselbe wie bei jeder anderen Druckausgabe in Glide: eine
eigenständige HTML-Seite ohne externe Verweise, die das Standardprogramm druckt
oder als PDF sichert. Eine eigene PDF-Bibliothek würde eine neue
Laufzeitabhängigkeit bedeuten – und die Regel, dass Glide ohne
Zusatzinstallation läuft, wiegt schwerer als ein selbst erzeugtes PDF.

## Bewusst nicht in Stufe 1

- **Freies Zeichnen.** Ein Strich ist kein Punkt; er bräuchte eine eigene
  Datenhaltung auf der Pinnwand. Das ist machbar, aber es ist der erste
  Schritt zu einem zweiten Bestand neben den Aufgaben – und der verlangt eine
  eigene Entscheidung darüber, was mit ihm bei Export, Backup und
  Formatwechsel geschieht.
- **Zoom.** Eine Tk-Canvas kann skalieren, aber Text skaliert dabei nicht
  mit; eine halbierte Karte wäre unlesbar. Sinnvoller wäre eine
  Übersichtskarte, die zeigt, wo etwas liegt.
- **Notizzettel ohne zugehörigen Punkt.** Siehe oben: dieselbe Frage.

## Grenzen

- 500 Karten und 200 Verbindungen je Pinnwand.
- Kartenpositionen und Verbindungen stehen in `settings.json` und damit **im
  vollständigen App-Backup**, nicht im Aufgabenbackup.
- Die Bildvorschau liest PNG, GIF und PPM über Tk; andere Formate zeigen
  weiterhin nur den Anhangzähler.
