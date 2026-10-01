# Glide 3.4.0 – Nachtrag: Startseite, Symbole und Fälligkeitsspalte

Stand: 05.09.2026 · App-Version 3.4.0 · Aufgabendatenformat 10

Dieser Nachtrag ergänzt [Oberfläche 3.4.0](13_OBERFLAECHE_3.4.0.md); alles dort
Beschriebene gilt weiter. Die App-Version bleibt **3.4.0** – die Änderungen sind
reiner Oberflächen-Feinschliff ohne Auswirkung auf Datenformat, Migration oder
gespeicherte Angaben. Ein Sprung auf 3.4.1 wäre möglich; er verlangt zusätzlich,
die Releaseplanung in `tests/tools/releasedaten.py` gegen den neuen Stand zu
prüfen und fortzuschreiben (ein Wächter dort erzwingt genau das).
Der Quellstand bleibt `src/glide/app.pyw`.

## Was sich in der Bedienung ändert

**Symbole:** Die Startseite trägt `▣` statt `⌂`, „Verspätet“ trägt `▲` statt `‼`.
Beide alten Zeichen fielen in der Systemspalte der Seitenleiste aus der Reihe:
Das Häuschen ist eine feine Umrisslinie und wirkt neben `▼` und `◐` kleiner und
leichter; das doppelte Ausrufezeichen ist ein Satzzeichen aus einer anderen
Zeichenfamilie. Die Ersatzzeichen stammen aus demselben Unicode-Block
„Geometrische Formen“ (U+25A0–U+25FF) wie `▼`, `◐`, `◈` und `▦`. Dessen Zeichen
sind gefüllt, sitzen in derselben optischen Box und haben dieselbe Strichstärke.

**Startseite:** Die Kacheln sind abgerundet – derselbe Radius wie bei
Seitenleiste, Eingabefeld und Listenrahmen. Oben und unten liegt jetzt genau so
viel Luft wie zwischen Seitenleiste und Inhaltsbereich. Der Zwischenraum steht
zwischen den Kacheln und nicht mehr zusätzlich hinter der letzten.

**Begrüßung:** Statt eines festen Satzes gibt es sieben Formulierungen. Gewechselt
wird beim Zurückkehren zur Startseite. Ein Neuaufbau derselben Ansicht – etwa
nach dem Abhaken einer Aufgabe – behält den Satz. Ist unter **Bearbeiten →
Einstellungen** ein Name gesetzt, steht er in jeder Variante.

**Fälligkeitsspalte:** Datum und Uhrzeit passen jetzt immer vollständig in die
Zeile. Vorher fehlte am rechten Ende bis zu ein Zeichen.

## Symbolvergleich

Die Spalte „Jetzt“ bezeichnet die eingebaute Auswahl. Alternativen sind Vorschläge
und lassen sich in `ICONS` mit einem Zeichen austauschen. Alle Einträge sind
Schriftzeichen; kein Iconpaket und kein Bild ist erforderlich.

| Verwendung | Bisher | Jetzt | Weitere Möglichkeit |
|---|---|---|---|
| Startseite | ⌂ | ▣ | ◉, ▩, ◧ |
| Eingang | ▼ | ▼ | ⇩, ▾ |
| In Bearbeitung | ◐ | ◐ | ◉, ◑ |
| Labels | ◈ | ◈ | ◆, ◇ |
| Verspätet | ‼ | ▲ | ◆, ◉, ‼ |
| Papierkorb | 🗑 | 🗑 | ⌧, ⊗, × |
| Fälligkeit/Kalender | ▦ | ▦ | ▣, ▩ |
| Gruppe | ▸ | ▸ | ▹, ▰ |
| Beschreibung | ≡ | ≡ | ¶, § |
| Anhang | ⊕ | ⊕ | ⊞, + |
| Wichtigkeit niedrig/mittel/hoch | ⚐ / ⚑ / ⚑⚑ | ⚐ / ⚑ / ⚑⚑ | ! / !! / !!! |
| Theme dunkel/hell | ☾ / ☀ | ☾ / ☀ | ◐ / ◑ |

Drei Gruppen bleiben bewusst außerhalb der geometrischen Familie, weil dort
keine geometrische Form die Bedeutung trägt:

- **Papierkorb `🗑`** – die Entscheidung aus 3.4.0 bleibt bestehen, einschließlich
  des Verzichts auf den Text-Variationsselektor, der unter Windows/Tk 8.6
  zusätzlichen Leerraum erzeugt.
- **Themenschalter `☾`/`☀`** – beide stehen in einem beschrifteten Knopf, nicht
  in der Symbolspalte, und Mond und Sonne sind eindeutiger als jede Halbfläche.
- **Wichtigkeit `⚐`/`⚑`/`⚑⚑`** – die Fähnchen sind eingeführt, farbig codiert und
  tragen mit einem und zwei Zeichen eine eigene Abstufung.

Die genaue Form hängt weiterhin von Betriebssystem und Schrift ab. Eine
pixelgleiche Darstellung wird nicht zugesagt.

## Zweiter Nachtrag: Startseite neu aufgebaut

**Kopfzeile.** Über allem liegt jetzt eine flache, breite Zeile: links eine
analoge Uhr, daneben der ausgeschriebene Wochentag mit Datum und darunter der
nächste anstehende Termin in der Farbe seiner Liste, rechts der Sprung in die
Kalenderansicht. Die Uhr ist aus Tk-Grundformen gezeichnet (`AnalogClock`) –
kein Bild, keine zusätzliche Abhängigkeit. Ihr Zeitgeber hängt am Widget und
endet mit ihm; die Startseite baut ihre Kacheln bei jedem Aufbau neu.

„Als Nächstes" meint ausschließlich die eigenen Fälligkeiten, nicht einen
externen Kalender – das Nicht-Ziel aus den Produktgrenzen bleibt unberührt.
Überfälliges bleibt außen vor, dafür gibt es „Verspätet".

**Willkommenskachel.** Das Textlogo steht links als farbige Fläche, rechts
daneben die Begrüßung und darunter eine wechselnde Aufforderung. Aus sieben
Grüßen und sieben Aufforderungen entstehen viele Kombinationen; beide wechseln
beim Zurückkehren zur Startseite.

**Textlogo.** Das Monogramm ist keine farbige Schrift mehr, sondern eine
farbige Fläche mit derselben Rechnung wie ein Labelchip (`MonogramTile`,
`monogram_colors`). Die Farbe kommt aus der Palette von Listen, Aufgaben und
Labels und ist unter **Bearbeiten → Einstellungen** wählbar – mit sofortiger
Vorschau neben der Auswahl.

**Tägliche Herausforderung.** In den Einstellungen lässt sich ein Tagesziel
setzen (erledigte Aufgaben pro Tag, 0 schaltet es ab). Die Startseite zeigt den
Stand als Balken. Gezählt wird ausschließlich der Übergang offen → erledigt,
zentral in `item_change`; ein wieder geöffneter Punkt zieht nichts ab. Import,
Rückgängig und Wiederherstellen aus dem Papierkorb laufen nicht über diesen Weg
und verändern die Tageszahl nicht.

**Verweise.** Die Schnellzugriffe stehen nebeneinander statt untereinander und
führen zu Eingang, In Bearbeitung, Verspätet, Labels, neuer Liste und den
Einstellungen. Jede anklickbare Fläche der Startseite nimmt unter dem Zeiger
dieselbe Hervorhebung an wie eine Zeile in der Seitenleiste.

**Reihenfolge.** „Dein aktueller Bestand" steht jetzt ganz unten: Er ist
Rückblick, keine Handlungsaufforderung. Seine drei Kennzahlen tragen eigene
Farben – erledigt grün, offen orange, Listen blau –, dazu Verweise auf „In
Bearbeitung" und „Verspätet" sowie ein Balkendiagramm der letzten sieben Tage.

**Zuletzt bearbeitet** zeigt drei statt sechs Einträge; gespeichert werden
weiterhin mehr, damit eine gelöschte Liste keine Lücke hinterlässt.

**Vorlagen.** Aus drei sind zehn geworden. Angeboten werden jeweils drei, und
welche das sind, wechselt beim Zurückkehren zur Startseite.

**Listenfarben.** Listen und Ordner tragen auf der Startseite ihre Farbe. In
den Übersichten „In Bearbeitung" und „Verspätet" erbt ein Punkt ohne eigene
Aufgabenfarbe die Farbe seiner Liste, ersatzweise die des nächsten Ordners
(`inherited_list_color`). In „Verspätet" steht die Herkunft vor dem
Fälligkeitszustand – dort ist ausnahmslos alles überfällig, Rot sagt nichts
mehr. In „In Bearbeitung" bleibt der Fälligkeitszustand vorn, weil sich dort
überfällig, heute und später mischen.

Eine `ttk.Treeview` färbt immer die ganze Zeile; mehrere Farben innerhalb einer
Zeile sind mit ihr nicht möglich. Es bleibt deshalb bei genau einer Farbe je
Punkt. Echte Mehrfarbigkeit erforderte, die Aufgabenliste von der Treeview auf
eine eigene Canvas-Liste umzubauen – mit allem, was daran hängt: Drag & Drop,
Mehrfachauswahl, Tastaturbedienung, Bildlauf.

**Labelnamen** dürfen bei der Eingabe höchstens 14 Zeichen lang sein
(`LABEL_NAME_INPUT_LIMIT`) – genau so viel zeigt die Labelspalte, Maßstab ist
„Freigabe nötig". Die Speichergrenze bleibt bei 40 Zeichen, damit vorhandene
längere Namen unangetastet bleiben.

## Symbole auf verschiedenen Systemen

Dasselbe Zeichen sieht auf zwei Rechnern verschieden aus, wenn die eingestellte
Schrift es nicht selbst enthält: Das System springt still auf eine Ersatzschrift
um – unter Windows meist Segoe UI Symbol, unter Linux DejaVu Sans. Beide
zeichnen dieselbe Form unterschiedlich groß und unterschiedlich stark.

`tests/tools/symbolpruefung.py` beantwortet das für den jeweiligen Rechner: Es
fragt Tk je Zeichen, aus welcher Familie es tatsächlich gezeichnet wird, und
markiert jede Ersatzschrift. Aufruf aus dem Quellordner:

```
python tests/tools/symbolpruefung.py
```

Erst der Befund, dann die Entscheidung – entweder Zeichen wählen, die die
Systemschrift selbst mitbringt, oder eine Schrift für die Symbole festlegen.

## Technische Umsetzung

| Zweck | Ort im Code |
|---|---|
| Symbolauswahl | `ListApp.ICONS` |
| Begrüßungen | `ListApp.HOME_GREETINGS`, `home_greeting`, `advance_home_greeting` |
| Kachelgeometrie | `HOME_EDGE_GAP`, `HOME_CARD_GAP`, `HOME_CARD_RADIUS`, `HOME_CARD_PAD_X/Y` |
| Abgerundete Box mit mitwachsender Höhe | `RoundedContainer(auto_height=True)` |
| Spaltenreserve der Fälligkeit | `TREE_CELL_RESERVE_CHARS`, `tree_cell_padding` |

`HOME_EDGE_GAP` trägt denselben Wert wie der Abstand zwischen Seitenleiste und
Inhaltsbereich. Wird dieser Abstand geändert, ist der Wert mitzuziehen.

Die Begrüßung wechselt in `_activate_system_view`, und zwar nur beim Wechsel aus
einer anderen Ansicht. Der Index liegt allein im Arbeitsspeicher; `settings.json`
bleibt unverändert, und persönliche Angaben sind weiterhin nicht Bestandteil
eines Aufgabenbackups.

Die Fälligkeitsspalte wird weiter mit der Listenschrift gemessen. Neu ist eine
an dieser Schrift bemessene Reserve für zwei Ziffernbreiten. Sie deckt zwei
Dinge ab, die in der reinen Textmessung nicht vorkommen: den inneren Rand der
Treeview-Zelle und Symbolzeichen, die Windows aus einer Ersatzschrift zeichnet,
die breiter ausfällt als die gemessene. Steht in der Ansicht irgendwo eine
Uhrzeit, gilt zusätzlich die volle Musterbreite („▦ 30.12.26, 22:30“) als
Untergrenze. Die Mindestbreite der Spalte bleibt 0, damit sie im schmalen
Fenster weiterhin vollständig weichen kann.

## Prüfung und Grenzen

Die fünf Suiten, beide Analysen sowie Syntax-, Versions- und Fixture-Prüfung
laufen unverändert. Geprüft wurde unter Linux/Tk 8.6 mit isoliertem
`GLIDE_DATA_DIR`; der Windows-Prüflauf mit `C:/Python312/python.exe` steht noch
aus und ist die maßgebliche Abnahme. Die Reserve der Fälligkeitsspalte wirkt
sich unter Windows deutlicher aus als unter Linux, weil dort die
Ersatzschrift-Zeichnung auftritt.

Offen bleiben die in [Oberfläche 3.4.0](13_OBERFLAECHE_3.4.0.md) genannten
Punkte: macOS und Linux als Zielplattformen, weitere Anzeigeskalierungen,
mehrere Monitore, längere reale Mausbedienung sowie Installer, Signierung und
Store-Veröffentlichung. Es gibt keine neue Laufzeitabhängigkeit.
