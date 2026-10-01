# Glide 3.5.0 – Wiederkehrende Aufgaben

Stand: 05.09.2026 · App-Version 3.5.0 · **Aufgabendatenformat 11**

Die startbare Einzeldatei liegt unter
`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.5.0.pyw`, der Quellstand
bleibt `src/glide/app.pyw`. Version 3.4.0 bleibt erhalten.

## Was sich in der Bedienung ändert

Eine Aufgabe mit Fälligkeit kann sich wiederholen. Die Auswahl steht in der
erweiterten Eingabe direkt unter der Fälligkeit – dort, weil ohne Datum nichts
zu wiederholen ist. Zur Wahl stehen:

| Auswahl | Bedeutung |
|---|---|
| täglich | jeden Tag |
| alle N Tage | jeden N-ten Tag, N von 1 bis 365 |
| an bestimmten Wochentagen | Mo–So einzeln ankreuzbar |
| wöchentlich | alle sieben Tage |
| monatlich | derselbe Tag im Folgemonat |
| jährlich | derselbe Tag im Folgejahr |

Jede Regel nimmt wahlweise ein **Enddatum**. Bleibt es leer, läuft die Reihe
ohne Ende.

**Beim Abhaken** rückt der Punkt auf seinen nächsten Termin vor und steht
wieder offen. Er bleibt derselbe Punkt an derselben Stelle, mit Beschreibung,
Labels, Anhängen und Unterpunkten. In der Liste steht `↻` hinter dem Text.

**Am Ende der Reihe** – Enddatum überschritten oder kein Termin mehr in Sicht –
bleibt der Punkt erledigt und verliert seine Regel. Er ist dann eine
gewöhnliche, abgeschlossene Aufgabe.

**Rückgängig** nimmt das Vorrücken zurück: Der Punkt steht wieder auf seinem
alten Termin.

## Zwei Entscheidungen, die man merken sollte

**Es entsteht keine zweite Zeile.** Die naheliegende Alternative wäre, den
abgehakten Punkt stehen zu lassen und daneben eine neue Instanz anzulegen. Eine
tägliche Aufgabe hinterließe so in einem Jahr 365 abgehakte Zeilen in derselben
Liste. Was geschafft wurde, hält stattdessen die Tageszahl fest; der Verlauf der
letzten sieben Tage steht auf der Startseite.

**Monats- und Jahresabstände rechnen vom ursprünglichen Termin**, nicht vom
letzten. Der 31. Januar wird zum 28. Februar – und danach wieder zum 31. März.
Würde vom jeweils letzten Termin aus weitergezählt, rutschte die Reihe über
einen einzigen Februar dauerhaft auf den 28.

## Was ausdrücklich nicht dazugehört

Glide erzeugt nichts im Voraus, prüft nichts im Hintergrund und meldet sich
nicht von selbst. Es gibt keine Erinnerung, keine Benachrichtigung und keinen
Dienst, der außerhalb des Programms läuft. Das frühere Nicht-Ziel nannte
Wiederholungen und Benachrichtigungen in einem Atemzug; getrennt betrachtet
braucht nur die zweite Hälfte etwas, das Glide nicht sein will. Die
Produktgrenzen in `docs/01_PRODUCT_CONSTRAINTS.md` sind entsprechend getrennt.

## Datenformat 11

Die Regel hängt als Feld `repeat` am Punkt:

```json
{"art": "monatlich", "start": "2026-01-31", "ende": "2026-12-31"}
```

- `art` – `taeglich`, `tage`, `wochentage`, `woechentlich`, `monatlich`, `jaehrlich`
- `abstand` – nur bei `tage`: jeder N-te Tag
- `tage` – nur bei `wochentage`: 0 = Montag … 6 = Sonntag
- `start` – Ursprungstermin der Reihe, Anker für Monats- und Jahresabstände
- `ende` – letzter zulässiger Termin oder `null`

**Migration aus Format 10 ist additiv.** Ein fehlendes Feld heißt „wiederholt
sich nicht"; alte Daten werden nicht umgeschrieben. Eine unvollständige oder
unbekannte Regel wird verworfen statt geraten – eine falsch geratene Regel
erzeugte Termine, die niemand gesetzt hat, und das ist schlimmer als gar keine
Wiederholung. Portable Backups werden weiterhin ab Format 4 angenommen.

Ältere Glide-Versionen lesen ein Format-11-Backup nicht. Für den Austausch mit
einem Rechner, der noch 3.4 fährt, ist der TXT-Export der richtige Weg; er
schreibt die Wiederholung als Klartextzeile `Wiederholung: monatlich` und liest
sie auch wieder ein.

## Technische Umsetzung

| Zweck | Ort im Code |
|---|---|
| Prüfung und feste Form einer Regel | `normalize_repeat` |
| Nächster Termin | `next_repeat_date`, `add_months` |
| Vorrücken beim Abhaken | `advance_repeating_items`, aufgerufen in `toggle_done` |
| Klartext hin und zurück | `describe_repeat`, `parse_repeat_text` |
| Auswahl in der Maske | `item_form_dialog`, Abschnitt „Wiederholung" |

`REPEAT_MAX_LOOKAHEAD_DAYS` begrenzt die Suche nach dem nächsten Termin. Ohne
diese Schranke könnte eine Regel, die nie zutrifft, endlos rechnen.

Die Zusatzfelder der Maske – Abstand, Wochentage, Enddatum – erscheinen nur zu
der Art, zu der sie gehören. Ein Feld, das gerade nichts bedeutet, ist eine
Fehlerquelle.

## Prüfung und Grenzen

Alle fünf Suiten, beide Analysen sowie Syntax-, Versions- und Fixture-Prüfung
laufen. Neu geprüft werden die Rechenregel für jede Art, das Vorrücken beim
Abhaken, das Rückgängigmachen, das Ende einer Reihe, der Klartextweg für den
TXT-Export sowie die Format-11-Referenzdatei
`tests/fixtures/current_v11/reference_v11.json` – der Format-10-Bestand bleibt
Teil derselben Regressionsprüfung.

**Geprüft wurde unter Linux mit Python 3.12.3 und Tcl/Tk 8.6.** Der
Windows-Prüflauf ist die maßgebliche Abnahme und steht noch aus. Besonders
anzusehen: die erweiterte Eingabemaske mit ein- und ausgeblendeten
Zusatzfeldern bei kleiner Fensterhöhe.

Nicht geprüft: ein Wechsel der Zeitzone oder der Systemuhr während einer
laufenden Reihe. Gerechnet wird mit dem lokalen Datum.
