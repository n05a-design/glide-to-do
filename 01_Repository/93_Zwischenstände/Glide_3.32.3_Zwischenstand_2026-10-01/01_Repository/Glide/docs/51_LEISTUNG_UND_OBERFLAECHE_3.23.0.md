# Leistung, Navigation und schmale Fenster – Glide 3.23.0

Stand 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16 · Einstellungen 2

## Ansichtswechsel: der Befund

Der Wechsel zwischen Listen und Übersichten dauerte spürbar. Gemessen wurde
nicht das Gefühl, sondern der Vorgang: ein künstlicher Bestand aus **1.584
Punkten** in zwölf Listen und sechs Ordnern, je zwanzig Ansichtswechsel unter
`cProfile`, dazwischen `root.update()`.

**Ausgangslage: 336 ms je Ansichtswechsel, 13,2 Millionen Funktionsaufrufe.**

### Befund 1 – dieselbe Zeichenkette 347.000-mal geprüft

`normalize_due` baute für jede Datumsprüfung mit `datetime.strptime` ein
`datetime`-Objekt auf, nur um eine Zeichenkette zu prüfen, die sich nicht
geändert hatte. Für zwanzig Ansichtswechsel waren das 347.000 Aufrufe und 2,9
von 11,3 Sekunden Profilerzeit.

Die Datumswerte eines Bestands wiederholen sich stark – in einer Liste steht
dasselbe Datum zwanzigmal untereinander. Ein Zwischenspeicher über den
Eingabetext (`functools.lru_cache`) trifft deshalb fast immer und darf
unbegrenzt leben: Dieselbe Zeichenkette hat immer dasselbe Ergebnis.

### Befund 2 – derselbe Bestand mehrfach je Wechsel durchlaufen

Die Seitenleiste fragt für ihre Zeilen nacheinander nach der Zahl der fälligen
Punkte, der überfälligen, der eingeplanten, der gelabelten und der je Ordner
enthaltenen. **Jede dieser Fragen lief über alle Listen und alle
verschachtelten Punkte.** Danach rechnete `refresh_sidebar_row_texts` dieselben
Zahlen für die Textkürzung noch einmal aus, und die geöffnete Ansicht ein
drittes Mal.

Neu ist ein Zwischenspeicher, der ausschließlich innerhalb eines Aufbaus lebt:

```python
with self.render_pass():
    ...   # Seitenleiste, Baum, Startseite fragen dieselben Kennzahlen
```

Entscheidend ist die Lebensdauer. Ein Speicher, der über den Aufbau hinaus
lebte, müsste bei jeder denkbaren Bestandsänderung geleert werden – und genau
eine vergessene Stelle würde eine falsche Zahl anzeigen. Innerhalb eines
Aufbaus dagegen ändert sich der Bestand nicht: Aufbauten lesen nur. Außerhalb
rechnet jede Abfrage wie bisher frisch.

Geöffnet wird der Durchgang an den Wurzeln: Ansichtswechsel, Listenwechsel,
Ordnerwechsel, Baumaufbau, Seitenleiste, Startseite und Textanpassung.
Verschachtelung ist der Normalfall; nur der äußerste legt den Speicher an.

### Befund 3 – jede Tabellenzeile einzeln vermessen

`content_column_widths` ermittelte die nötige Breite der beiden rechten Spalten
aus `font.measure` für jede einzelne Zeile – 164 Millisekunden je Aufbau und
damit der größte verbliebene Posten. Fälligkeiten und Labelspalten wiederholen
sich massiv; jeder Text wird jetzt einmal gemessen.

### Ergebnis

| Größe | Vorher | Nachher |
|---|---|---|
| Ansichtswechsel | 336 ms | **129 ms** |
| Funktionsaufrufe (20 Wechsel) | 13,2 Mio | **4,6 Mio** |
| `update_sidebar_list` | 272 ms | 61 ms |
| `content_column_widths` | 164 ms | 24 ms |
| `refresh_sidebar_row_texts` | 99 ms | 29 ms |

Der verbleibende Anteil liegt im Zeichnen durch Tk, nicht mehr in Python.

**Es wurde keine Ladeanimation ergänzt.** Bei 129 Millisekunden wäre sie länger
sichtbar als der Vorgang dauert, und sie würde eine Verzögerung behaupten, die
es nicht mehr gibt.

## Navigation

Die Reihenfolge des Systembereichs folgt dem Tagesablauf statt der
Entstehungsgeschichte der Ansichten:

1. Startseite
2. **Mein Tag** – darunter eingerückt der **Eingang**
3. **In Bearbeitung** – darunter eingerückt **Verspätet**
4. Labels
5. Vorlagen
6. Papierkorb

Zwei Zeilen stehen eine Ebene tiefer, weil sie Teilmengen der Zeile darüber
sind: Der Eingang ist der noch nicht eingeplante Teil von „Mein Tag“,
„Verspätet“ der überfällige Teil von „In Bearbeitung“. Der Eingang bleibt eine
echte Liste mit demselben Klickverhalten; er ist nur kein Hauptpunkt mehr.

Ein `ttk.Treeview` mit `show="headings"` zeichnet keine Einrückung. Sie steht
deshalb als Leerraum im Text; welche Zeile eingerückt ist, entscheidet
`system_row_depth` an genau einer Stelle, damit Aufbau und Breitenanpassung
nicht auseinanderlaufen.

## Auf- und Zuklappen

„Zuklappen“ betraf bis 3.22 nur die Punkte der geöffneten Liste. Jetzt klappt
es auch alle Ordner der Seitenleiste zu – mit einer Ausnahme: **Der Pfad zur
geöffneten Liste bleibt offen.** Sonst verschwände genau das aus dem Bild,
woran gerade gearbeitet wird, und man müsste sich zurückklicken.

## Schmale Fenster

Die Regel stand bereits fest: Essentielles bleibt, Sekundäres geht zuerst. Sie
war nirgends umgesetzt – stattdessen schrumpfte der Titel als Einziges, weil er
als Letztes um Platz bat. Am schmalen Rand stand ein „…“ neben vier vollständig
beschrifteten Schaltflächen.

### Kopfzeile: drei Dichtestufen

| Breite des Kopfbereichs | Stufe | Was geschieht |
|---|---|---|
| ab 1120 px | `full` | alles mit Beschriftung |
| 900–1119 px | `compact` | „Benachrichtigungen“ wird zur Zahl am Symbol |
| unter 900 px | `minimal` | Drucken und Einstellungen wandern ins Überlaufmenü |

### Aktionsreihen

Unter 700 Pixeln Reihenbreite weichen „Liste leeren“, „Löschen“, „Bearbeiten“
und „Rückgängig“. Alle vier bleiben über Kontextmenü, Menüleiste,
Tastenkürzel und das Überlaufmenü erreichbar – das war die Bedingung dafür,
sie überhaupt ausblenden zu dürfen.

### Weitere Angaben

- Die Fortschrittszeile zeigt ab der kompakten Stufe nur ihre ersten Angaben;
  die vollständige Zeile steht im Tooltip.
- „Suche löschen“ erscheint bei schmalem Fenster nur, wenn eine Suche läuft.
- „Anzeige: Erweitert“ wird zu „Anzeige“.
- Auf der Pinnwand bleiben „Raster“, „Finden“ und „Fläche“; „Vorschau“ und
  „Auto“ weichen zuerst.

Weil Schaltflächen jetzt verschwinden können, packt `pack_relative` sie
defensiv: Fehlt das Bezugswidget eines `before=`, wird ohne Bezug gepackt statt
den ganzen Zeilenaufbau mit einem Tk-Fehler abzubrechen.

## Zweispaltige Startseite

Die Schwellen für die Spaltenzahl waren geraten – 980 und 1500 Pixel für die
Fläche der Startseite. Weil Seitenleiste und Ränder von der Fensterbreite
abgehen, sprang die zweite Spalte erst bei einem Fenster von rund 1300 Pixeln
an; ein auf die Bildschirmhälfte gelegtes Fenster blieb einspaltig.

Seit 3.23 sind sie abgeleitet: Eine Kachel ist ab `HOME_TILE_MIN_WIDTH` = 300
Pixeln lesbar – dieselbe Breite, die auch eine Pinnwandkarte in der Vorgabe
hat. Daraus folgen 616 Pixel für zwei und 932 für drei Spalten. Gemessen wird
weiterhin die tatsächlich verfügbare Fläche, nicht die Bildschirmauflösung.

## Globale Aktionsleiste

Die Druckausgabe gibt es seit 3.17, aber sie lag ausschließlich im Menü
„Datei“ und hinter Strg+P. Wer beides nicht durchsucht, erfährt nie, dass Glide
drucken kann. Sie steht jetzt als Schaltfläche neben dem Seitenleistenschalter
– beide wirken auf die geöffnete Ansicht und nicht auf einen ausgewählten
Punkt.

Bewusst genau **eine** zusätzliche Schaltfläche. Der Bereich soll keine zweite
Werkzeugleiste werden; alles Weitere liegt im Überlaufmenü, das bei schmalem
Fenster ohnehin gebraucht wird.
